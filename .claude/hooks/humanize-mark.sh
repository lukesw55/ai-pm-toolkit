#!/usr/bin/env bash
# humanize-mark.sh — write the sha256 sentinel flag that unlocks the
# humanize-gate.sh PreToolUse hook for one specific prose body.
#
# Usage:
#   humanize-mark.sh "<final prose body>"
#   printf '%s' "<final body>" | humanize-mark.sh -
#
# Run AFTER applying .claude/skills/humanizer/SKILL.md, with the EXACT bytes
# that will go to the publish tool. The hash must match what the gate computes
# on tool_input — any byte change invalidates the flag.

set -euo pipefail

if [ "$#" -ge 1 ] && [ "$1" != "-" ]; then
  BODY="$1"
else
  BODY="$(cat)"
fi

if [ -z "$BODY" ]; then
  echo "humanize-mark: refusing to mark an empty body" >&2
  exit 1
fi

HASH=$(printf '%s' "$BODY" | sha256sum | awk '{print $1}')
DIR="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/.humanized"
mkdir -p "$DIR"
touch "$DIR/$HASH.flag"
echo "$HASH"
