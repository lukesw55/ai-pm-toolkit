#!/usr/bin/env bash
# inference-discipline-gate.sh — PreToolUse hook enforcing the inference-discipline skill.
#
# Blocks when committed-or-outbound content carries unresolved inference markers:
#
#   [INFER: ...]        the assistant deduced this; needs user OK
#   [ASSUMING: ...]     proceeding as if X is true; needs user OK
#   [UNVERIFIED: ...]   needs a tool call / human confirmation
#   [FROM MEMORY: ...]  recalled from .ai/memory, not reverified this turn
#   [RECALL: ...]       recalled from earlier in this turn (lower risk but still raw)
#
# These tags are CONVERSATION-ONLY scaffolding for the approval flow. If they
# end up in a file the user will read as truth, or in an outbound artefact
# (Confluence / Slack / Jira), the approval loop was skipped.
#
# Scope:
#   - PreToolUse on Write / Edit / NotebookEdit  → scan new content
#   - PreToolUse on outbound MCP publish tools   → scan body / message fields
#
# Override per-content via sha256 sentinel (same mechanism as anti-slop-mark.sh):
#   hooks/inference-discipline-mark.sh "<final content>"
#   → writes .ai/gates/inference-discipline/<hash>.flag
#
# Skipped paths (the gate would block itself otherwise):
#   - skills/inference-discipline/** (canonical and both mirrors carry the tags)
#   - hooks/*.sh                       (the shell gates reference them)
#   - CLAUDE.md, AGENTS.md                      (both harnesses' doctrine documents the tags)
#   - vendored / generated / external paths
#
# Fail-open on parse / read errors. This script is a discipline gate, not a
# correctness gate — a bash bug must never block legitimate work.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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

# Skip paths where the tags are documented or vendored.
case "$FILE_PATH" in
  */skills/inference-discipline/*|skills/inference-discipline/*|*/hooks/*.sh|hooks/*.sh|*/CLAUDE.md|CLAUDE.md|*/AGENTS.md|AGENTS.md|*/node_modules/*|*/dist/*|*/build/*|*/.venv/*|*/venv/*|*/__pycache__/*|*/.git/*|*/coverage/*|*/.next/*|*/.nuxt/*|*/target/*)
    exit 0
    ;;
esac

# Extract content to inspect — varies by tool. MCP tool names are matched by
# suffix (*ServerName__toolName), not a fixed server prefix: the same logical
# server (Atlassian Rovo, Slack) can be registered under a different prefix
# per environment (a connector name, a plugin scope, or none at all). The
# server segment stays in the glob so a same-named tool on an unrelated
# server can't collide. The settings.json / .codex/hooks.json matcher is the
# real gatekeeper of *when* this runs; these arms just need to recognise the
# tool once routed here.
CONTENT=""
case "$TOOL_NAME" in
  Write|Edit|NotebookEdit)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      .tool_input.new_string // .tool_input.content // .tool_input.new_source // empty
    ' 2>/dev/null || echo "")
    ;;
  *Atlassian_Rovo__createConfluencePage|*Atlassian_Rovo__updateConfluencePage)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      [.tool_input.title // empty, .tool_input.body // empty] | join("\n")
    ' 2>/dev/null || echo "")
    ;;
  *Atlassian_Rovo__createJiraIssue|*Atlassian_Rovo__editJiraIssue)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      [.tool_input.summary // empty, .tool_input.description // empty, (.tool_input.fields // {} | tostring)] | join("\n")
    ' 2>/dev/null || echo "")
    ;;
  *Atlassian_Rovo__addCommentToJiraIssue|*Atlassian_Rovo__createConfluenceFooterComment|*Atlassian_Rovo__createConfluenceInlineComment)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      .tool_input.body // .tool_input.commentBody // .tool_input.comment // empty
    ' 2>/dev/null || echo "")
    ;;
  *Slack__slack_send_message|*Slack__slack_send_message_draft|*Slack__slack_schedule_message)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      .tool_input.text // .tool_input.message // empty
    ' 2>/dev/null || echo "")
    ;;
  *Slack__slack_create_canvas|*Slack__slack_update_canvas)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      [.tool_input.title // empty, .tool_input.content // empty, .tool_input.document_content // empty] | join("\n")
    ' 2>/dev/null || echo "")
    ;;
  *)
    exit 0
    ;;
esac

[ -z "$CONTENT" ] && exit 0

# Sentinel override.
HASH=$(printf '%s' "$CONTENT" | hash_stdin)
FLAG="$ROOT/.ai/gates/inference-discipline/$HASH.flag"
if [ -f "$FLAG" ]; then
  exit 0
fi

# Scan for tags. POSIX-friendly regex.
TAGS_FOUND=()
for tag in "INFER" "ASSUMING" "UNVERIFIED" "FROM MEMORY" "RECALL"; do
  if printf '%s' "$CONTENT" | grep -qE "\[${tag}:"; then
    TAGS_FOUND+=("$tag")
  fi
done

if [ ${#TAGS_FOUND[@]} -eq 0 ]; then
  exit 0
fi

# Build the violation report.
{
  echo "inference-discipline-gate: BLOCKED — content contains unresolved inference markers."
  echo
  echo "Tool: $TOOL_NAME"
  [ -n "$FILE_PATH" ] && echo "Path: $FILE_PATH"
  echo
  echo "Markers found: ${TAGS_FOUND[*]}"
  echo
  echo "Resolution required:"
  echo "  1. Verify each inference (Read the file, Grep the symbol, ask the user)."
  echo "  2. Replace the tag with the verified claim — or remove the claim entirely."
  echo "  3. Outbound artefacts (Confluence / Slack / Jira / committed code) must never"
  echo "     carry these tags. They are conversation-only scaffolding for the approval flow."
  echo
  echo "If this is a legitimate exception (writing memory that audits inferred premises,"
  echo "or a draft the user explicitly asked to keep with markers), override per-content:"
  echo "  hooks/inference-discipline-mark.sh \"<final content>\""
  echo
  echo "See skills/inference-discipline/SKILL.md for the full discipline."
} >&2
exit 2
