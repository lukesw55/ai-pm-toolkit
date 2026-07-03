#!/usr/bin/env bash
# SessionStart hook: inject the hot memory layer (index + active-context pointer).
# Both files are policy-capped (pointer <=2 KB, index ~1 line/project); the 8 KB
# guard below only trips if that policy drifts -- memory.py doctor flags it first.
# Registered in .claude/settings.json under hooks.SessionStart.

set -u

MEM="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}/.ai/memory"

idx="(missing)"
active="(missing)"
[ -f "$MEM/index.md" ] && idx="$(cat "$MEM/index.md")"
[ -f "$MEM/active-context.md" ] && active="$(cat "$MEM/active-context.md")"

ctx="## umberto memory index ($MEM/index.md)
$idx

## umberto active-context ($MEM/active-context.md)
$active"

# Hard cap: never inject more than 8 KB even if the files re-bloat.
ctx="$(printf '%s' "$ctx" | head -c 8192)"

jq -n --arg ctx "$ctx" \
  '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
