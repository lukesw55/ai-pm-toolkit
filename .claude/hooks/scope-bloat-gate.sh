#!/usr/bin/env bash
# scope-bloat-gate.sh — Stop hook that blocks AI-slop responses.
#
# Heuristic gate that fires AFTER the assistant finishes a turn and BEFORE
# the response is shown. Reads the JSONL transcript, extracts the last
# assistant text and the prompt it answered, then checks for patterns of
# off-topic verbosity, padding, and AI-tell structure. If any rule fires,
# exits 2 with the reason in stderr — Claude Code re-prompts the model with
# that feedback so the assistant rewrites tighter.
#
# stop_hook_active short-circuit prevents infinite loops: the gate runs at
# most once per turn. If the model fails the second pass, the response
# ships anyway.
#
# Fail-open on parse / read errors (any unexpected condition exits 0).
# This script is a slop filter, not a correctness gate; never let a bash
# bug block legitimate work.

set -uo pipefail

INPUT="$(cat)"

# Loop guard
STOP_ACTIVE=$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null || echo "false")
[[ "$STOP_ACTIVE" == "true" ]] && exit 0

TRANSCRIPT=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")
[[ -z "$TRANSCRIPT" || ! -f "$TRANSCRIPT" ]] && exit 0

# Last 300 events is enough to find the most recent assistant + user turn.
TAIL=$(tail -n 300 "$TRANSCRIPT" 2>/dev/null) || exit 0
[[ -z "$TAIL" ]] && exit 0

# Extract last assistant text (concatenated text blocks of the last
# assistant message that has any text content).
LAST_ASSISTANT=$(printf '%s' "$TAIL" | jq -rs '
  map(select(.type == "assistant"))
  | map(.message.content)
  | map(if type == "array" then [.[] | select(.type == "text") | .text] | join("\n") else "" end)
  | map(select(. != null and . != ""))
  | last // ""
' 2>/dev/null) || exit 0

# Extract last user prompt text (excludes tool_result blocks).
LAST_USER=$(printf '%s' "$TAIL" | jq -rs '
  map(select(.type == "user"))
  | map(.message.content)
  | map(
      if type == "string" then .
      elif type == "array" then [.[] | select(.type == "text") | .text] | join("\n")
      else "" end
    )
  | map(select(. != null and . != ""))
  | last // ""
' 2>/dev/null) || exit 0

[[ -z "$LAST_ASSISTANT" ]] && exit 0

# Strip code fences from prose-only checks (em-dash, label-colon counts).
PROSE=$(printf '%s' "$LAST_ASSISTANT" | awk '
  BEGIN { in_code = 0 }
  /^```/ { in_code = 1 - in_code; next }
  !in_code { print }
')

ASSISTANT_LEN=${#LAST_ASSISTANT}
PROSE_LEN=${#PROSE}
USER_LEN=${#LAST_USER}

REASONS=()

# Doc-request keywords — when present, length rules relax.
DOC_REGEX='doc|prd|p[áa]gina|page|post|memo|release notes|confluence|propos[ta]|escreva|draft|elabor|gere|crie a|construa|monta|expanda|detalh|completo|long-form|full|todos os|all the|enumere|liste'

# Rule 1: scope bloat. Short prompt, long answer, no doc keyword.
# Measured on PROSE (code fences stripped): a short question legitimately
# answered with a large diff or code block is not bloat.
if [[ $USER_LEN -gt 0 && $USER_LEN -lt 400 ]]; then
  if [[ $PROSE_LEN -gt $((USER_LEN * 5)) ]]; then
    if ! printf '%s' "$LAST_USER" | grep -qiE "$DOC_REGEX"; then
      REASONS+=("Scope bloat: resposta tem $PROSE_LEN chars de prosa vs prompt de $USER_LEN chars (razão >5×). Pergunta curta sem pedido de doc — encolha pra responder só o que foi perguntado.")
    fi
  fi
fi

# Rule 2: em-dash density (prose only, excludes code fences and block
# quotes — quoted material reproduces someone else's punctuation).
if [[ $PROSE_LEN -gt 200 ]]; then
  EMDASH=$(printf '%s' "$PROSE" | grep -v '^[[:space:]]*>' | grep -o '—' | wc -l | tr -d ' ')
  EMDASH=${EMDASH:-0}
  DENSITY=$(( EMDASH * 1000 / PROSE_LEN ))
  if [[ $DENSITY -gt 4 ]]; then
    REASONS+=("Em-dashes (—) acima de 4/1000 chars (atual: $EMDASH em $PROSE_LEN chars de prosa). Troque por períodos, dois-pontos, ou parênteses.")
  fi
fi

# Rule 3: label-colon bullet runs (3+ in a row breaks the human-prose feel).
LABEL_RUN=$(printf '%s' "$PROSE" | awk '
  BEGIN { run = 0; max = 0 }
  /^[[:space:]]*[-*][[:space:]]+\*\*[^*]+\*\*:/ { run++; if (run > max) max = run; next }
  /^[[:space:]]*[-*][[:space:]]+[A-Z][^:]{1,40}:[[:space:]]/ { run++; if (run > max) max = run; next }
  /^[[:space:]]*[0-9]+\.[[:space:]]+\*\*[^*]+\*\*:/ { run++; if (run > max) max = run; next }
  { run = 0 }
  END { print max }
')
LABEL_RUN=${LABEL_RUN:-0}
if [[ $LABEL_RUN -gt 3 ]]; then
  REASONS+=("$LABEL_RUN bullets seguidos no padrão 'Label: descrição' (estrutura repetitiva AI-tell). Quebre — escreva como prosa, varie a forma, ou colapse em uma sentença.")
fi

# Rule 4: section headers when prompt is a one-liner with no doc request.
USER_LINES=$(printf '%s' "$LAST_USER" | grep -c '.' || true)
USER_LINES=${USER_LINES:-0}
HEADER_COUNT=$(printf '%s' "$PROSE" | grep -cE '^##+[[:space:]]|^\*\*[^*]+\*\*:[[:space:]]*$' || true)
HEADER_COUNT=${HEADER_COUNT:-0}
if [[ $USER_LINES -le 2 && $USER_LEN -lt 300 && $HEADER_COUNT -gt 0 ]]; then
  if ! printf '%s' "$LAST_USER" | grep -qiE "$DOC_REGEX"; then
    REASONS+=("$HEADER_COUNT header(s) numa resposta a pergunta de $USER_LINES linha(s)/$USER_LEN chars. Resposta curta não precisa de seção — escreva inline.")
  fi
fi

# Rule 5: dual-question close ("...? Or...?" / "...? Ou...?").
LAST_LINES=$(printf '%s' "$PROSE" | tail -5)
if printf '%s' "$LAST_LINES" | grep -qiE '\?[[:space:]]*$' && \
   printf '%s' "$LAST_LINES" | grep -qiE '(^|[[:space:]])(Ou |Or |Prefere |Quer que|Want me to|Or would|Or should)'; then
  REASONS+=("Fecho com dual-question ('...? Ou...?' / '...? Or...?'). Faça uma pergunta só, ou nenhuma.")
fi

if [[ ${#REASONS[@]} -eq 0 ]]; then
  exit 0
fi

# Emit block with structured reasons.
{
  echo "scope-bloat-gate: BLOCKED — resposta tem padrões de AI slop."
  echo
  for i in "${!REASONS[@]}"; do
    echo "$((i+1)). ${REASONS[$i]}"
  done
  echo
  echo "Reescreva endereçando SÓ o que foi perguntado. Length proporcional. Sem padding."
  echo "Se o gate estiver errado neste caso (ex: pergunta curta mas legitimamente requer detalhe),"
  echo "explique brevemente no início da resposta — o gate só bloqueia uma vez por turn."
} >&2
exit 2
