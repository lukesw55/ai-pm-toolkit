#!/usr/bin/env bash
# humanize-gate.sh — PreToolUse hook for the humanize-deliverables hard gate.
#
# Blocks Confluence/Slack/Jira publish tools unless a sha256 sentinel flag
# matching the prose body exists in .claude/.humanized/<hash>.flag.
# The flag is written by .claude/hooks/humanize-mark.sh after the humanizer
# pass produces the FINAL bytes that will be passed to the tool.
#
# Body extraction strategy: the longest string value (recursive) in tool_input.
# Channel IDs, page IDs, titles, and labels are short; the prose body is long.
# Picking the longest avoids per-tool field name brittleness.

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

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
INPUT="$(cat)"
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // "unknown"')
BODY=$(printf '%s' "$INPUT" | jq -r '
  .tool_input
  | [.. | strings]
  | map(select(length > 0))
  | sort_by(-length)
  | .[0] // empty
')

if [ -z "$BODY" ]; then
  cat >&2 <<EOF
humanize-gate: BLOCKED — could not extract any prose body from tool_input for $TOOL_NAME.

Either the tool has no string fields, or its shape changed. The gate fails closed
on purpose: silently allowing publish without a humanizer pass defeats the gate.

If $TOOL_NAME does not carry user-facing prose and should be exempt, narrow the
matcher in .claude/settings.local.json (or .claude/settings.json) instead of
loosening this script.
EOF
  exit 2
fi

HASH=$(printf '%s' "$BODY" | hash_stdin)
FLAG_DIR="$PROJECT_ROOT/.claude/.humanized"
FLAG="$FLAG_DIR/$HASH.flag"

if [ -f "$FLAG" ]; then
  exit 0
fi

cat >&2 <<EOF
humanize-gate: BLOCKED — $TOOL_NAME is in scope of the humanize-deliverables hard gate.

The longest prose string in tool_input has not passed through the humanizer.

Required workflow:

  1. Apply .claude/skills/humanizer/SKILL.md to the prose body
     (the 29-pattern catalogue: em-dashes, rule of three, link-words,
     inflated vocabulary, promotional register, passive voice, hedging
     stacks, superficial -ing analyses, vague attributions, filler).

  2. Mark the EXACT FINAL bytes you intend to publish:
        $PROJECT_ROOT/.claude/hooks/humanize-mark.sh "<final prose body>"
     Or via stdin (recommended for multi-line bodies):
        printf '%s' "<final body>" | $PROJECT_ROOT/.claude/hooks/humanize-mark.sh -

  3. Re-call $TOOL_NAME with that exact text.

Hash expected for this call: $HASH
Flag file the gate looked for: $FLAG

Any byte change between step 2 and step 3 — even one trailing newline, one
swapped emoji — invalidates the hash. Always mark AFTER humanization with
the precise bytes that will go to the tool.
EOF
exit 2
