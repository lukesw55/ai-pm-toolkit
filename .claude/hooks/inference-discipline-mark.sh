#!/usr/bin/env bash
# inference-discipline-mark.sh — write the sha256 sentinel that unlocks
# inference-discipline-gate.sh for one specific tool-input content blob.
#
# Usage:
#   inference-discipline-mark.sh "<final content>"
#   printf '%s' "<final content>" | inference-discipline-mark.sh -
#
# Run AFTER deciding the gate-flagged content is legitimate (e.g. writing a
# memory file that audits inferred premises with their tags intact, or a draft
# the user explicitly asked to keep with markers). The hash must match what
# the gate computes on tool_input — any byte change invalidates the flag.

set -euo pipefail

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

if [ "$#" -ge 1 ] && [ "$1" != "-" ]; then
  BODY="$1"
else
  BODY="$(cat)"
fi

if [ -z "$BODY" ]; then
  echo "inference-discipline-mark: refusing to mark an empty body" >&2
  exit 1
fi

HASH=$(printf '%s' "$BODY" | hash_stdin)
DIR="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/.inference-discipline"
mkdir -p "$DIR"
touch "$DIR/$HASH.flag"
echo "$HASH"
