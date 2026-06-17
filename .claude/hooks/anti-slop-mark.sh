#!/usr/bin/env bash
# anti-slop-mark.sh — write the sha256 sentinel that unlocks anti-slop-gate.sh
# for one specific Write / Edit / NotebookEdit content blob.
#
# Usage:
#   anti-slop-mark.sh "<final content>"
#   printf '%s' "<final content>" | anti-slop-mark.sh -
#
# Run AFTER deciding the gate-flagged content is legitimate, with the EXACT
# bytes that will go to the tool. The hash must match what the gate computes
# on tool_input — any byte change invalidates the flag.

set -euo pipefail

if [ "$#" -ge 1 ] && [ "$1" != "-" ]; then
  BODY="$1"
else
  BODY="$(cat)"
fi

if [ -z "$BODY" ]; then
  echo "anti-slop-mark: refusing to mark an empty body" >&2
  exit 1
fi

HASH=$(printf '%s' "$BODY" | sha256sum | awk '{print $1}')
DIR="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/.anti-slop"
mkdir -p "$DIR"
touch "$DIR/$HASH.flag"
echo "$HASH"
