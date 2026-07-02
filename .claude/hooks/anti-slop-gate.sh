#!/usr/bin/env bash
# anti-slop-gate.sh — PreToolUse hook for the anti-slop hard gate.
#
# Blocks Write / Edit / NotebookEdit when the target file or content matches
# the high-signal subset of .claude/skills/anti-slop/SKILL.md:
#
#   1. Forbidden file basenames (D1: PLAN.md, NOTES.md, IMPLEMENTATION.md,
#      SUMMARY.md, CHANGES.md, ANALYSIS.md, TODO.md — case-insensitive).
#      Applied only on Write (creation/overwrite). Edit on an existing
#      forbidden file is allowed — the slop already exists, blocking the
#      cleanup is worse than the original sin.
#
#   2. Banner comments (A10: comment-line composed entirely of '=' chars,
#      5+ in a row). Diff-aware: only blocks if the banner appears in the
#      new content but NOT in the old content (i.e. is being added).
#
#   3. Decorative emoji headings in markdown (B6). Diff-aware: same logic.
#
# Overridable per-content via sha256 sentinel:
#   anti-slop-mark.sh "<final content>"  → .claude/.anti-slop/<hash>.flag
#
# False-positive mitigations:
#   - Banner regex requires the comment line to be ONLY '=' chars after the
#     marker — eliminates URL/test-data/embedded-equals false positives.
#   - Diff-awareness — Edit that preserves an existing banner / emoji passes.
#   - Vendored / generated paths skip entirely (node_modules, mirrors, dist,
#     build, .venv, __pycache__, external skills).
#   - Forbidden-basename rule only applies on Write, never on Edit.
#
# Noisier patterns (try/except, generic identifiers, comments restating code)
# stay in the skill catalogue — gating them via regex misfires more than helps.

set -uo pipefail

hash_stdin() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 | awk '{print $1}'
  else
    echo "hash: need sha256sum or shasum" >&2
    return 127
  fi
}

INPUT="$(cat)"
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null || echo "unknown")
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null || echo "")

# Skip vendored / generated / external paths.
case "$FILE_PATH" in
  */node_modules/*|*/dist/*|*/build/*|*/.venv/*|*/venv/*|*/__pycache__/*|*/.git/*|*/coverage/*|*/.next/*|*/.nuxt/*|*/target/*)
    exit 0
    ;;
esac

# Content under inspection.
NEW=$(printf '%s' "$INPUT" | jq -r '
  .tool_input.new_string // .tool_input.content // .tool_input.new_source // empty
' 2>/dev/null || echo "")

OLD=$(printf '%s' "$INPUT" | jq -r '
  .tool_input.old_string // empty
' 2>/dev/null || echo "")

# Sentinel override: if the user marked the exact NEW content, allow.
if [ -n "$NEW" ]; then
  HASH=$(printf '%s' "$NEW" | hash_stdin)
  FLAG="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/.anti-slop/$HASH.flag"
  if [ -f "$FLAG" ]; then
    exit 0
  fi
else
  HASH=""
fi

REASONS=()

# Rule 1: forbidden file basenames (D1) — only on Write.
if [ "$TOOL_NAME" = "Write" ] && [ -n "$FILE_PATH" ]; then
  BASENAME=$(basename "$FILE_PATH")
  BASENAME_LC=$(printf '%s' "$BASENAME" | tr '[:upper:]' '[:lower:]')
  case "$BASENAME_LC" in
    plan.md|notes.md|implementation.md|summary.md|changes.md|analysis.md|todo.md)
      REASONS+=("Forbidden file '$BASENAME' (anti-slop D1: auto-generated planning docs). The change explanation belongs in the PR body or commit message, not in a parallel markdown file. If the user explicitly asked for this file (e.g. repo convention requires it), mark and retry.")
      ;;
  esac
fi

# Rule 2: banner comments (A10) — comment line that is purely '=' after the
# marker, 5+ in a row. Skip on markdown to avoid setext-heading collisions.
# Diff-aware: only block if the banner is in NEW but not in OLD.
if [ -n "$NEW" ] && [ -n "$FILE_PATH" ]; then
  EXT="${FILE_PATH##*.}"
  EXT_LC=$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')
  if [ "$EXT_LC" != "md" ] && [ "$EXT_LC" != "markdown" ]; then
    BANNER_RE='^[[:space:]]*(#|//|\*)[[:space:]]*={5,}[[:space:]]*$'
    if printf '%s' "$NEW" | grep -qE "$BANNER_RE"; then
      if [ -z "$OLD" ] || ! printf '%s' "$OLD" | grep -qE "$BANNER_RE"; then
        REASONS+=("Banner comment detected (e.g. '# =====' line composed entirely of '=' chars). Anti-slop A10: delete banners — if a file needs them to be readable, split it or improve names. If the project convention genuinely requires banner separators (rare), mark and retry.")
      fi
    fi
  fi
fi

# Rule 3: decorative emoji headings in markdown (B6).
# Diff-aware: only block if the emoji heading is in NEW but not in OLD.
if [ -n "$NEW" ] && [ -n "$FILE_PATH" ]; then
  EXT="${FILE_PATH##*.}"
  EXT_LC=$(printf '%s' "$EXT" | tr '[:upper:]' '[:lower:]')
  if [ "$EXT_LC" = "md" ] || [ "$EXT_LC" = "markdown" ]; then
    EMOJI_RE=$'^#{1,6}[[:space:]]+(\xf0\x9f\x9a\x80|\xe2\x9c\x85|\xf0\x9f\x92\xa1|\xf0\x9f\x93\x9d|\xe2\x9a\xa1|\xf0\x9f\x8e\xaf|\xf0\x9f\x94\xa5|\xe2\x9c\xa8|\xf0\x9f\x93\x8a|\xf0\x9f\x93\x88|\xf0\x9f\x8e\x89|\xf0\x9f\x8c\x9f|\xe2\xad\x90|\xf0\x9f\x92\xaa|\xf0\x9f\x9a\xa8|\xe2\x9a\xa0|\xf0\x9f\x9b\xa0|\xf0\x9f\x94\xa7|\xf0\x9f\x8e\xa8|\xf0\x9f\x93\x8c|\xf0\x9f\x94\x91|\xf0\x9f\x92\x8e)'
    if printf '%s' "$NEW" | grep -qE "$EMOJI_RE"; then
      if [ -z "$OLD" ] || ! printf '%s' "$OLD" | grep -qE "$EMOJI_RE"; then
        REASONS+=("Decorative emoji heading detected at start of an H1-H6 line. Anti-slop B6: use emoji only when the surrounding project already uses them. If the project does, mark and retry.")
      fi
    fi
  fi
fi

if [ ${#REASONS[@]} -eq 0 ]; then
  exit 0
fi

{
  echo "anti-slop-gate: BLOCKED — $TOOL_NAME on ${FILE_PATH:-<no path>} hit ${#REASONS[@]} anti-slop rule(s):"
  echo
  for i in "${!REASONS[@]}"; do
    echo "  $((i+1)). ${REASONS[$i]}"
  done
  echo
  echo "Fix the violation, OR — if this is legitimate (intentional banner in a"
  echo "tool config that demands it, emoji that the project already uses,"
  echo "user explicitly asked for the file) — mark the EXACT bytes:"
  echo
  echo "    \$CLAUDE_PROJECT_DIR/.claude/hooks/anti-slop-mark.sh \"<final content>\""
  echo "    printf '%s' \"<final content>\" | \$CLAUDE_PROJECT_DIR/.claude/hooks/anti-slop-mark.sh -"
  echo
  if [ -n "$HASH" ]; then
    echo "Hash expected for this call: $HASH"
    echo "Flag file the gate looked for: ${CLAUDE_PROJECT_DIR:-\$PWD}/.claude/.anti-slop/$HASH.flag"
    echo
  fi
  echo "Full catalogue and override examples: .claude/skills/anti-slop/SKILL.md"
} >&2
exit 2
