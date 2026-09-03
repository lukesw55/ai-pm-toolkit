#!/usr/bin/env bash
# memory-reminder.sh — Stop hook that speaks up when the work outran the log.
#
# Reminder, never a gate: it always exits 0 and at most prints one
# systemMessage. Wired by both harness lifecycle adapters on Stop, after the
# reply gate.
#
# Temporal invariant. The stamp written at session start is the baseline;
# latest_work is the newest mtime among the paths git reports as changed (the
# working tree, plus every file touched by commits made after the stamp), and
# latest_memory is the newest mtime of the changelogs that `memory.py log`
# writes. Work newer than memory means this session changed things without
# recording what changed, so the reminder fires. Nothing changed since the
# stamp, or memory written last, and it stays quiet.
#
# No commit timestamp enters either side: a commit persists content written
# earlier, so it is neither when the work happened nor when the log did.
#
# Never: reads a transcript, descends into raw-evidence/, people/ or data/,
# blocks anything, or writes a file. Fails open on every unexpected
# condition, which means silence, never a false alarm.

set -uo pipefail

INPUT="$(cat)"

# Loop guard: the gate runs at most once per turn.
STOP_ACTIVE=$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo "false")
[[ "$STOP_ACTIVE" == "true" ]] && exit 0

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MARK="$ROOT/.ai/gates/session/started"
[[ -f "$MARK" ]] || exit 0

command -v git >/dev/null 2>&1 || exit 0
command -v python3 >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0

SESSION="$(tr -dc '0-9' < "$MARK" 2>/dev/null || echo "")"
[[ -n "$SESSION" ]] || exit 0

# One python3 call per group: the newest mtime over the paths handed in as
# argv, so a path holding a space or a newline survives intact. A path that
# no longer exists falls back to the nearest existing parent directory, whose
# mtime POSIX bumps on removal: an approximation that is never earlier than
# the deletion. stat(1) is avoided on purpose, since -c is GNU and -f is BSD.
max_mtime() {
  python3 - "$@" <<'PY' 2>/dev/null || echo 0
import os
import sys

newest = 0
for path in sys.argv[1:]:
    while path and not os.path.exists(path):
        parent = os.path.dirname(path)
        if parent == path:
            path = ""
            break
        path = parent
    if not path:
        continue
    try:
        newest = max(newest, int(os.path.getmtime(path)))
    except OSError:
        pass
print(newest)
PY
}

# Both loops read from process substitution, never a pipeline: a pipeline
# would run the body in a subshell and lose the paths collected here.
WORK_PATHS=()
skip_old_name=0
while IFS= read -r -d '' entry; do
  if [[ "$skip_old_name" == 1 ]]; then
    skip_old_name=0
    continue
  fi
  [[ ${#entry} -gt 3 ]] || continue
  # 'XY <path>': M, A, D and ?? name the path directly; after an R or C the
  # next record is the old name and carries no mtime of its own.
  [[ "${entry:0:2}" == *[RC]* ]] && skip_old_name=1
  WORK_PATHS+=("$ROOT/${entry:3}")
done < <(git -C "$ROOT" status --porcelain=v1 -z --untracked-files=all 2>/dev/null)

# Committed work with a clean tree. No pathspec excludes anything: tracked
# files under .ai/ are real work, and the runtime paths there are gitignored,
# so they never show up here in the first place.
while IFS= read -r -d '' entry; do
  [[ -n "$entry" ]] || continue
  WORK_PATHS+=("$ROOT/$entry")
done < <(git -C "$ROOT" log --since="@$SESSION" --name-only --format='' -z 2>/dev/null)

[[ ${#WORK_PATHS[@]} -gt 0 ]] || exit 0
WORK="$(max_mtime "${WORK_PATHS[@]}")"
# Dirt inherited from before the session does not count as this session's work.
[[ "$WORK" -gt "$SESSION" ]] || exit 0

# The whitelist of a semantic memory write: the changelog is the one file
# whose writing is the canonical "log what changed", and it is exactly what
# the reminder asks for. Lifecycle writes (park, activate), archive rebuilds
# and index files are deliberately out of the signal. Only files that exist
# are measured, so a missing changelog cannot borrow a directory's mtime.
MEM_PATHS=()
[[ -f "$ROOT/.ai/changelog.md" ]] && MEM_PATHS+=("$ROOT/.ai/changelog.md")
for changelog in "$ROOT"/.ai/memory/projects/*/changelog.md; do
  [[ -f "$changelog" ]] || continue
  slug="$(basename "$(dirname "$changelog")")"
  case "$slug" in
    raw-evidence | people | data) continue ;;
  esac
  MEM_PATHS+=("$changelog")
done

LAST_MEM=0
[[ ${#MEM_PATHS[@]} -gt 0 ]] && LAST_MEM="$(max_mtime "${MEM_PATHS[@]}")"
[[ "$WORK" -gt "$LAST_MEM" ]] || exit 0

MSG="memory-reminder: files changed after the last changelog entry that memory.py log wrote. Reminder, not a block: run python3 scripts/memory.py log <slug> \"<what changed>\" --title \"<title>\" before closing."
jq -n --arg msg "$MSG" '{systemMessage: $msg}'
exit 0
