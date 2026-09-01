---
name: pm-archetype-ai
description: >-
  AI / ML / LLM PM archetype lens. Invoke when the product is partly
  probabilistic — LLM features, agents, retrieval, classification, generation,
  recommendation, anomaly detection, model-in-the-loop tooling — and the work
  needs eval suites, guardrails, failure-mode analysis, human-in-the-loop,
  model selection, prompt design, eval-driven iteration, or safety/policy.
  Probabilistic systems need a different discipline than deterministic
  software. Trigger on "eval suite", "guardrail", "hallucination", "esse
  feature usa modelo?", "como medimos qualidade do modelo?". For
  Claude-API-specific implementation use the `claude-api` skill instead — this
  skill is the PM lens, not the implementation reference. The full
  trigger-phrase list and phase-skill pairings live in the skill body.
---

# PM Archetype — AI / ML / LLM products

> Product-type lens. Pairs with phase skills (`pm-phase-{discover,define,develop,deliver}`) when the product is probabilistic. The phase skills cover *when* and *how to sequence*; this skill covers *what's special about AI work*.

## Prime directive

**Quality bars first, then experience.** AI products that ship without measurable quality thresholds look magical until they embarrassingly fail in production. Set the eval suite and guardrails before — not after — you ship.

## When to invoke

The product or feature includes any of:

- LLM-driven generation (text, code, summaries, drafts)
- LLM-driven extraction or classification
- Retrieval-augmented generation (RAG)
- Agentic flows (tool calls, multi-step planning)
- Recommendation, ranking, scoring, anomaly detection
- Voice / vision / multimodal models
- Any output users will treat as authoritative that came from a stochastic system

Skip this skill when the AI piece is purely backend optimisation users never see (e.g. internal log clustering with no user-facing surface).

### Trigger phrases

"AI feature", "LLM", "modelo de ML", "evals", "eval suite", "guardrail", "hallucination", "HITL", "human in the loop", "model selection", "prompt strategy", "fallback chain", "drift", "red team", "safety policy", "esse feature usa modelo?", "tem AI nisso?", "what's the eval threshold to ship?", "como medimos qualidade do modelo?".

## Required reading before output

- `.ai/rules.md`, `.ai/app.md`, `.ai/memory/active-context.md`
- relevant project memory — **prior eval results are load-bearing**; if the team has shipped anything AI-shaped before, the eval log determines what's possible now

## References this skill chains to

Pairs with `pm-phase-develop` (PRD with eval plan), `pm-phase-deliver` (release gate by eval pass-rate), `pm-transversal-analysis` (qualitative eval of outputs), and the `claude-api` skill for Claude-API-specific implementation. Specific references:

- `../pm-phase-develop/references/prd-writing.md` — AI PRDs emphasise failure modes + eval plan + HITL
- `../pm-phase-develop/references/tracking-plan-design.md` — AI apps need bespoke events (inference called, tool used, fallback triggered, user rated output)
- `../pm-phase-deliver/references/experiment-interpretation.md` — A/B on AI outputs requires care (variance, subjectivity)
- `../pm-phase-deliver/references/metric-quality-guardrails.md` — AI guardrails are critical
- `../pm-transversal-analysis/` — qualitative eval of outputs is a core AI skill
- `claude-api` skill (external Anthropic skill, not bundled here) — when the implementation lives on the Claude API / Anthropic SDK

## AI-specific concerns to cover in any AI PRD

- **Evaluation suites** — representative test cases, graded against quality rubric; run before release
- **Guardrails** — hard filters (content policy, PII, toxicity), soft filters (confidence thresholds), HITL fallbacks
- **Failure modes** — hallucination, misinterpretation, bias, jailbreak, data-leak, brittleness to prompt phrasing
- **Human-in-the-loop** — when to route to human review; how escalation works; user-facing UX for uncertain outputs
- **Model selection** — which model for which cost / latency / quality trade-off; fallback chain
- **Prompt engineering** — system prompt, few-shot examples, structured outputs, prompt caching, versioning
- **Observability** — trace per inference, token cost, latency, confidence, user feedback
- **Safety + policy** — content policy, moderation, red-teaming, regulated domains
- **Data flywheel** — how user interactions improve the model / prompts / retrieval

## Workflow

1. **Define the user task** — what are we automating or augmenting? What does "good output" look like?
2. **Define the quality rubric** — dimensions (accuracy, helpfulness, safety, tone) and grading method per dimension.
3. **Draft the eval suite** — 20–100 representative cases covering happy paths, edge cases, adversarial inputs.
4. **Pick the model + prompt strategy** — cost / latency / quality envelope; fallback chain.
5. **Design the guardrails** — hard limits, soft limits, HITL routing.
6. **Plan the release gate** — eval pass-rate threshold before shipping; canary rollout.
7. **Design observability** — traces, feedback capture, drift detection.
8. **Define the iteration loop** — cadence for re-running evals, updating prompts, reviewing failures.
9. **Stress-test failure modes** — loop in your QA lead for code / metric / experiment integrity.
10. **Architecture check** — loop in your engineering architecture partner for inference infrastructure, fallbacks, cost control.
11. **Update memory** with eval-suite decisions, model selections, guardrail policies.

## AI-specific anti-patterns

- **"AI delight" without measurement.** Shipping because the demo looked great; first users hit failure modes the team never tested.
- **No eval before release.** Relying on "looks good" rather than graded test cases.
- **Guardrails as an afterthought.** Retrofitting safety after an incident is painful.
- **Over-trusting benchmark scores.** Public benchmarks often don't match your task distribution.
- **No human fallback.** Model fails → user has no path forward.
- **Hidden costs.** Inference cost not instrumented; surprise bill arrives.
- **No drift monitoring.** Models and prompts work day one; degrade silently as upstream changes.
- **Ignoring policy / privacy / safety.** Shipping in regulated domains without legal input.
- **Hallucinating confidence.** Product asserts facts the model made up; users trust the UI.
- **Prompt-only thinking.** Treating prompt engineering as the whole discipline; ignoring retrieval, tools, evals, HITL.

## Output format

```text
## pm-archetype-ai recommendation

### User task + quality rubric
what we're building; dimensions of "good"

### Eval suite
coverage + size + grading method + pass-rate threshold to ship

### Model + prompt strategy
model selection rationale, prompt structure, caching, few-shot, fallback chain

### Guardrails
hard limits / soft limits / HITL routing / content-policy alignment

### Observability
traces, feedback, cost, latency, drift monitors

### Failure modes + mitigations
hallucination / bias / jailbreak / brittleness — known ones + detection paths

### Release gate
eval pass rate + canary plan + rollback

### Iteration loop
cadence for eval re-runs; how we use user feedback

### Safety + policy
legal / privacy / safety review needed; regulated-domain implications

### Memory updates
```

## Integration

- Upstream: `pm-phase-develop` (PRD with eval plan, tracking plan tuned for AI events).
- Downstream: `pm-phase-deliver` (release gate by eval pass-rate, post-launch A/B interpretation with AI variance in mind).
- Transversals: `pm-transversal-analysis` (qualitative review of outputs), `pm-transversal-docs` (model card, eval log, failure-mode log in Confluence).
- Engineering pairings: your engineering architecture partner for inference architecture; your QA lead for eval / failure-probe design; `claude-api` skill for Anthropic SDK implementation.
- Copilot mirror: [.github/agents/pm-ai.agent.md](../../../.github/agents/pm-ai.agent.md) (kept for GitHub Copilot harness compatibility).

## Success criteria

- every release passes the eval suite at the declared threshold
- guardrails catch predictable failure modes before users see them
- HITL routing works for uncertain cases; users have a fallback
- cost and latency stay within envelope at scale
- drift is detected within days, not months
- incidents decrease quarter over quarter as the eval suite matures
- the team carries institutional memory of failure modes; we don't re-learn the same lessons
