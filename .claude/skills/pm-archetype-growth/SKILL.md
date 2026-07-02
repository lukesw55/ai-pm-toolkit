---
name: pm-archetype-growth
description: Growth PM archetype lens. Invoke when the focus is acquisition, activation, retention, expansion, monetisation, or funnel conversion — experimentation-heavy, analytical before prescriptive. Covers AARRR funnels, North Star → KPI tree cascades, hypothesis-driven A/B tests, primary metric + guardrail design, decision rules (ship/iterate/kill), winner's-curse traps, novelty effects, segment interactions. Trigger on "acquisition", "activation", "retention", "expansion", "monetisation", "AARRR", "funil", "funnel", "conversion", "drop-off", "onboarding flow", "upgrade flow", "pricing test", "lifecycle", "habit formation", "cohort retention", "viral coefficient", "NRR", "ARPU", "LTV/CAC", "ship/iterate/kill", "experiment design", "A/B test", "experimento", "primary metric", "guardrail metric", "novelty effect", "winner's curse", "novel funnel hipótese", "como melhorar a ativação?". Pairs with `pm-phase-define` (KPI trees + pricing), `pm-phase-develop` (instrumentation), `pm-phase-deliver` (experiment interpretation, metric quality, post-launch monitoring), `pm-transversal-analysis` (triangulating quali+quant when numbers move), and `data-science-analyst` (validating the SQL / experiment maths). For non-growth launch readouts (release notes, generic post-launch monitoring, A/B tests on features that aren't funnel-shaped), use `pm-phase-deliver` instead — this skill is the lens that brings growth-experimentation discipline.
---

# PM Archetype — Growth products

> Product-type lens. Pairs with phase skills when the work is funnel / experimentation / monetisation. The phase skills cover *when* and *how to sequence*; this skill covers *the discipline of running many small bets where most will fail*.

## Prime directive

**Learning rate > shipped count.** In growth, most tested ideas fail. The job is to set up the test apparatus so the 10% that work compound, and the 90% that don't are killed quickly without leaving technical or product debt.

## When to invoke

The work is about moving a funnel-stage metric or a monetisation outcome:

- acquisition (signups, traffic sources, CAC)
- activation (% signups hitting first-value within activation window; activation-funnel drop-offs)
- retention (week-N / month-N cohort retention; habit-formation indicators)
- expansion (upgrade rate, seat growth, feature adoption leading to plan change, NRR)
- referral (viral coefficient, invitation conversion)
- revenue (MRR growth, ARPU, LTV:CAC)

Also invoke when the team is about to run an A/B test and the metric / decision-rule design needs to be tightened.

## Required reading before output

- `.ai/rules.md`, `.ai/app.md`, `.ai/memory/active-context.md`
- relevant project memory — **prior experiment logs are load-bearing**; without them the team re-tests dead ideas
- live PostHog data (use the `mcp__claude_ai_PostHog__*` tools) when sizing the bet — never propose without baseline

## References this skill chains to

- `.claude/skills/pm-phase-define/references/kpi-tree.md` — growth trees cascade from North Star into funnel stages
- `.claude/skills/pm-phase-define/references/pricing-packaging.md` — monetisation is often growth territory
- `.claude/skills/pm-phase-develop/references/tracking-plan-design.md` — growth lives or dies on instrumentation
- `.claude/skills/pm-phase-deliver/references/experiment-interpretation.md` — daily reference
- `.claude/skills/pm-phase-deliver/references/metric-quality-guardrails.md` — second-daily reference
- `.claude/skills/pm-phase-deliver/references/product-analytics.md` — funnels, cohorts, retention
- `.claude/skills/pm-transversal-analysis/` — especially triangulation (why does the number move?)
- `data-science-analyst` skill — for validating SQL, A/B maths, leakage checks

## AARRR + guardrails

Pair every growth metric with at least one guardrail:

| Stage | Primary | Guardrail |
|---|---|---|
| Acquisition | signups, CAC | quality of signup (activation rate downstream) |
| Activation | % first-value within window | retention week-2 (activation theatre check) |
| Retention | cohort retention week-N | support load, NPS / sentiment |
| Expansion | upgrade rate, NRR | downgrade / churn signal |
| Referral | viral coefficient | invitation spam complaints |
| Revenue | MRR, ARPU | gross-margin, refund rate |

## Workflow

1. **State the AARRR layer** — which stage of the funnel is this about?
2. **Read the current data** — baseline + segment patterns. Pull from PostHog directly when possible.
3. **Form a hypothesis** — `if [change], [segment] will [behaviour], moving [metric] by [magnitude], because [mechanism]`.
4. **Design the minimum test** — cheapest way to learn; A/B only when it fits (see `experiment-interpretation.md`).
5. **Pre-declare metrics + decision rule** — primary, guardrails, ship / iterate / kill thresholds.
6. **Stress-test the metric setup** — loop in your QA lead for tracking-plan QA + experiment validity. For statistical correctness, chain to `data-science-analyst`.
7. **Run + interpret** — triangulate with quali if something surprises.
8. **Decide + document** — ship / iterate / kill; log learning.
9. **Update memory** — `experiments.md`, `decisions.md`, any triangulation memos.

## Growth-specific anti-patterns

- **Local funnel optimisation that hurts retention.** Pushing users through step 3 at the cost of step 5.
- **Over-testing low-value tweaks.** 50 button-colour tests; 0 user-outcome tests.
- **Activation theatre.** Moving activation rate by redefining "activation" instead of improving product.
- **"Everything is a conversion problem."** Some product problems are not about conversion; they're about product-market fit.
- **Winner's curse.** Stat-sig "wins" that don't replicate at scale.
- **Pricing changes without migration plans.** New price, old customers, no communication → churn bomb.
- **Ignoring long-horizon outcomes.** Shipping on week-1 metrics; week-N metric regresses.
- **Single-segment obsession.** Helping free users; harming paid; net zero or worse.

## Output format

```text
## pm-archetype-growth recommendation

### AARRR layer
...

### Baseline + current state
metric, segment, trend (from PostHog or warehouse)

### Hypothesis
if [change], [segment] will [behaviour], moving [metric] by [magnitude], because [mechanism]

### Minimum test
method, sample, duration, decision rule

### Primary metric + guardrails
...

### Expected learning
what we'll know if green / yellow / red

### Risks to validity
confounds, novelty, interaction with other tests

### Follow-up experiments (if green)
...

### Memory updates
...
```

## Integration

- Upstream: `pm-phase-define` (KPI tree, cascade, North Star).
- Build phase: `pm-phase-develop` (tracking plan + feature flag strategy + experiment scaffolding).
- Launch phase: `pm-phase-deliver` (experiment interpretation, metric quality, decision).
- Transversals: `pm-transversal-analysis` (when a number moves and you need to know why), `pm-transversal-docs` (experiment log structure in Confluence, Jira ticket hygiene around variants).
- Engineering pairings: your QA lead (tracking-plan QA, experiment integrity), `data-science-analyst` (validate SQL / A/B maths), your engineering architecture partner when feature-flag plumbing crosses services.
- Copilot mirror: [.github/agents/pm-growth.agent.md](../../../.github/agents/pm-growth.agent.md).

## Success criteria

- funnel metrics move because of shipped work (not seasonality)
- kill rate on experiments is high — bad ideas drop quickly
- retention improves alongside activation (no local optimisation)
- the experiment log teaches the team what works and what doesn't
- instrumentation is trustworthy; no surprise metric drift
