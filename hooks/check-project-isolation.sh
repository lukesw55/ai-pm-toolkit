#!/usr/bin/env bash
# Soft project-isolation guard.
# PreToolUse hook on Read|Edit|Write|NotebookEdit. Warns (does not block)
# when a tool touches `.ai/memory/projects/<slug>/...` and <slug> is not
# the active project recorded in `.ai/memory/active-context.md`.
#
# Same customer can legitimately appear in two projects on different
# product surfaces — but the warning forces an explicit confirmation
# before evidence/decisions cross compartments.
#
# Fails OPEN: any unexpected condition exits 0 silently. The hook is a
# safety net, not a gate.

set -euo pipefail

INPUT="$(cat)"
FILE_PATH="$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' <<<"$INPUT")"
TOOL_NAME="$(jq -r '.tool_name // "?"' <<<"$INPUT")"

[[ -z "$FILE_PATH" ]] && exit 0

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ACTIVE_CTX="$ROOT/.ai/memory/active-context.md"
[[ -f "$ACTIVE_CTX" ]] || exit 0

ACTIVE_SLUG="$(grep -m1 -E '^- \*\*Slug\*\*:' "$ACTIVE_CTX" | grep -oE '`[^`]+`' | tr -d '`' || true)"
[[ -z "$ACTIVE_SLUG" ]] && exit 0

PATH_SLUG="$(echo "$FILE_PATH" | grep -oE '\.ai/memory/projects/[^/]+' | head -1 | sed -E 's|.*/projects/||' || true)"
[[ -z "$PATH_SLUG" ]] && exit 0
[[ "$PATH_SLUG" == "$ACTIVE_SLUG" ]] && exit 0

MSG="⚠️ Project isolation: $TOOL_NAME is touching projects/$PATH_SLUG/ while active project is '$ACTIVE_SLUG'. Confirm cross-reference is explicit, not a bleed."
CTX="Cross-project file access: file_path contains projects/$PATH_SLUG/ but active is '$ACTIVE_SLUG'. Per feedback_project_isolation.md, evidence stays in its origin project; only proceed if this is an explicit cross-reference, not silent bleed."

jq -n --arg msg "$MSG" --arg ctx "$CTX" '{
  systemMessage: $msg,
  hookSpecificOutput: { hookEventName: "PreToolUse", additionalContext: $ctx }
}'
