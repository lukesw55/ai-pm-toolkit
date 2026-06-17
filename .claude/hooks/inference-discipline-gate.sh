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
#   .claude/hooks/inference-discipline-mark.sh "<final content>"
#   → writes .claude/.inference-discipline/<hash>.flag
#
# Skipped paths (the gate would block itself otherwise):
#   - .claude/skills/inference-discipline/**   (the skill doc references the tags)
#   - .claude/hooks/**                          (this script references them)
#   - CLAUDE.md                                 (documents the tags)
#   - vendored / generated / external paths
#
# Fail-open on parse / read errors. This script is a discipline gate, not a
# correctness gate — a bash bug must never block legitimate work.

set -uo pipefail

INPUT="$(cat)"
TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // "unknown"' 2>/dev/null || echo "unknown")
FILE_PATH=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' 2>/dev/null || echo "")

# Skip paths where the tags are documented or vendored.
case "$FILE_PATH" in
  */.claude/skills/inference-discipline/*|*/.claude/hooks/*|*/CLAUDE.md|*/node_modules/*|*/dist/*|*/build/*|*/.venv/*|*/venv/*|*/__pycache__/*|*/.git/*|*/coverage/*|*/.next/*|*/.nuxt/*|*/target/*)
    exit 0
    ;;
esac

# Extract content to inspect — varies by tool.
CONTENT=""
case "$TOOL_NAME" in
  Write|Edit|NotebookEdit)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      .tool_input.new_string // .tool_input.content // .tool_input.new_source // empty
    ' 2>/dev/null || echo "")
    ;;
  mcp__claude_ai_Atlassian_Rovo__createConfluencePage|mcp__claude_ai_Atlassian_Rovo__updateConfluencePage)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      [.tool_input.title // empty, .tool_input.body // empty] | join("\n")
    ' 2>/dev/null || echo "")
    ;;
  mcp__claude_ai_Atlassian_Rovo__createJiraIssue|mcp__claude_ai_Atlassian_Rovo__editJiraIssue)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      [.tool_input.summary // empty, .tool_input.description // empty, (.tool_input.fields // {} | tostring)] | join("\n")
    ' 2>/dev/null || echo "")
    ;;
  mcp__claude_ai_Atlassian_Rovo__addCommentToJiraIssue|mcp__claude_ai_Atlassian_Rovo__createConfluenceFooterComment|mcp__claude_ai_Atlassian_Rovo__createConfluenceInlineComment)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      .tool_input.body // .tool_input.commentBody // .tool_input.comment // empty
    ' 2>/dev/null || echo "")
    ;;
  mcp__claude_ai_Slack__slack_send_message|mcp__claude_ai_Slack__slack_send_message_draft|mcp__claude_ai_Slack__slack_schedule_message)
    CONTENT=$(printf '%s' "$INPUT" | jq -r '
      .tool_input.text // .tool_input.message // empty
    ' 2>/dev/null || echo "")
    ;;
  mcp__claude_ai_Slack__slack_create_canvas|mcp__claude_ai_Slack__slack_update_canvas)
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
HASH=$(printf '%s' "$CONTENT" | sha256sum | awk '{print $1}')
FLAG="${CLAUDE_PROJECT_DIR:-$PWD}/.claude/.inference-discipline/$HASH.flag"
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
  echo "  .claude/hooks/inference-discipline-mark.sh \"<final content>\""
  echo
  echo "See .claude/skills/inference-discipline/SKILL.md for the full discipline."
} >&2
exit 2
