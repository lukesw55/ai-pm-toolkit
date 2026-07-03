---
name: pm-phase-define
description: Lean Double Diamond **Define phase** skill for PMs. Invoke when discovery evidence exists but the team has not yet chosen what to build, how to measure success, how to sequence bets, or how to justify the investment. Trigger on requests for product vision/strategy, North Star metrics, KPI trees, opportunity sizing (TAM/SAM/SOM, bottoms-up), business cases, PRFAQs, pricing & packaging, prioritisation (RICE/WSJF/Kano/cost-of-delay), roadmap narratives, or decision memos (DACI/ADR). Also trigger on "o que priorizar?", "construa árvore de KPI", "write the annual plan", "choose what not to do", "build a scorecard", "justify this investment". Outputs strategic choices that are explicit, non-goals that are named, and measurement that shapes behaviour.
---

# PM Phase — Define

> Double Diamond Phase 2 of 4. Turns discovery evidence into explicit choices and a measurement architecture that makes the choices legible and auditable.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke when:

- discovery has produced evidence but the team has not committed to a specific problem/metric/sequence
- a roadmap exists without clear rationale ("why this, why now, why not X?")
- metrics are proliferating but success is ambiguous
- an initiative needs a credible size or business case before funding
- leadership asks "what's our strategy/North Star/priority order?"
- pricing/packaging decisions are being discussed
- multiple stakeholders are pulling in different directions and a crisp recommendation memo is needed
- quarterly or annual planning is starting

Skip to `pm-phase-develop` if the wedge is already defined and the work is about execution. Go back to `pm-phase-discover` if the underlying problem is still fuzzy.

## Prime directive

**Define is choices + measurement.** A strategy that avoids trade-offs is not a strategy. KPIs that cannot be moved by anyone on the team are not KPIs. Priorities without invalidation conditions are opinions. Expert PMs leave this phase with: one sharp problem, one measurable outcome, ranked bets, and a set of things explicitly NOT being done.

## Core sub-skills

### 1. Strategy formulation

Define direction, strategic pillars, and the set of bets that connect customer evidence, market conditions, and business goals. Seniority shows up in horizon, ambiguity tolerance, and willingness to commit to non-goals on the record.

Outputs: strategy memo (1–3 pages), vision statement, "where we play / how we win" narrative, explicit non-goals.

Anti-patterns: calling a roadmap a strategy, confusing goals with initiatives, avoiding trade-offs, overfitting to the latest escalation.

→ Deep-dive: `references/strategy-memo.md`

### 2. KPI architecture and metric-tree design

Build a measurement system that links customer value → product outcomes → business results via a North Star and supporting input metrics.

Outputs: North Star with formula, 2–3 layer metric tree, metric dictionary with owners, guardrail set, leading-vs-lagging taxonomy.

Anti-patterns: metrics that are easy to query but not causal, revenue-only scorecards, mixing health and target metrics, changing definitions mid-stream.

→ Deep-dive: `references/kpi-tree.md`

### 3. Opportunity sizing and demand modelling

Estimate scale × reachability × economics. Blend top-down TAM/SAM/SOM with bottoms-up cohort-level reasoning and stress-test the 3 load-bearing assumptions.

Outputs: sizing model, scenario table (base/upside/downside), assumptions sheet, sensitivity analysis.

Anti-patterns: TAM theatre, false precision, one heroic adoption curve, ignoring acquisition constraints.

→ Deep-dive: `references/opportunity-sizing.md`

The stage-4 artefact this skill commonly produces is the **One Pager** — see `references/one-pager.md` for the template (stage 4 of 8 in `.claude/skills/WORKFLOW.md`).

### 4. Business case and PRFAQ reasoning

Translate an initiative into costs, benefits, operating implications, and return logic — suitable for investment decisions. Use PRFAQ when the decision needs executive-level alignment or when working backwards from a press-release-quality outcome sharpens the bet.

Outputs: investment memo or PRFAQ, cost/benefit model with baseline, staged gate plan, downside scenario.

Anti-patterns: upside-as-certainty, ignoring ongoing ops cost, no baseline, single-point estimates, no migration cost.

→ Deep-dive: `references/business-case-prfaq.md`

### 5. Pricing and packaging

Design value metrics, plans, tiers, and monetisation structures aligned to customer value and GTM model. Shared with Product Marketing and Finance; this skill frames the PM share of the work.

Outputs: pricing memo, tier matrix, packaging proposal, migration FAQ, willingness-to-pay estimate, monetisation experiment plan.

Anti-patterns: copying competitors mechanically, cost-plus anchoring, changing price without packaging clarity, ignoring migration friction.

→ Deep-dive: `references/pricing-packaging.md`

### 6. Prioritisation frameworks

Apply an explicit method to compare options and rank work according to impact, effort, confidence, timing, and strategic alignment. The expert move is choosing and adapting the framework to context, not treating the score as truth.

Outputs: prioritisation matrix, scoring rubric, ranked initiative list, rationale memo.

Anti-patterns: treating the score as truth, hiding judgement behind arithmetic, scoring with weak evidence, never recalibrating.

→ Deep-dive: `references/prioritisation-frameworks.md`

### 7. Roadmap narrative

Build a roadmap that tells a story: strategy → sequenced bets → dependencies → expected outcomes. Roadmaps create understanding, not just visibility.

Outputs: roadmap narrative + deck + FAQ, now-next-later view, stage gates, review pack.

Anti-patterns: date theatre, feature laundry lists, roadmap without rationale, failing to distinguish commitments from bets from options.

→ Deep-dive: `references/roadmap-narrative.md`

### 8. Decision documentation (DACI / PRFAQ / ADR)

Write docs that make a recommendation explicit, clarify trade-offs, and enable asynchronous decision-making. Senior PMs increasingly work through written alignment.

Outputs: decision memo, DACI page, ADR record, PRFAQ (cross-posted with §4).

Anti-patterns: status without recommendation, hidden trade-offs, burying the ask, no record of who decided what.

→ Deep-dive: `references/decision-memo-daci.md`

## Workflow

1. **Load context** — `.ai/memory/active-context.md`, project profile, prior `decisions.md` and `experiments.md`, any existing strategy/KPI artefact. Pull discovery outputs if `pm-phase-discover` produced them.
2. **Classify the ask** — strategy, KPI, sizing, business case, pricing, prioritisation, roadmap, or decision memo? State it explicitly in one line.
3. **Name the choices** — every artefact must include "what we chose NOT to do" and why.
4. **Ground in evidence** — cite discovery outputs, data, or assumptions (flagged as such). Missing evidence → name it explicitly.
5. **Stress-test assumptions** — for sizing/business case, identify top 3 load-bearing assumptions and show sensitivity.
6. **Persist** — strategy → `.ai/memory/projects/<slug>/strategy.md`; decisions → `decisions.md`; KPI tree → `kpis.md`; priorities → `priorities.md`.

## Output contract

```text
## [Sub-skill] — [short title]

### Context read
### Choice / definition
### Rationale (why this over alternatives)
### What we are NOT doing
### Assumptions (load-bearing, with invalidation conditions)
### Evidence / baseline
### Risks and downside
### Next step (what would make this firm or force a re-look)
### Memory updates
```

## Integration

- Upstream: `pm-phase-discover` feeds segments, opportunities, hypotheses.
- Downstream: `pm-phase-develop` (KPIs become PRD success criteria, priorities become backlog order), `pm-phase-deliver` (tree becomes dashboard + experiment primary metric).
- Transversais: `pm-transversal-stakeholder` for DACI/exec reporting, `pm-transversal-docs` for Confluence/Jira publication.
- Archetype lenses adapt the framing to the product type during the Define phase.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is the 1-page choice + rationale + non-goals; Standard is the full memo for leadership; Caveman is a 5-line bet / metric / size / risk / next.

## Success criteria

- every roadmap initiative traces to a strategic pillar
- KPIs move because of shipped work (not just collected)
- sizing/business cases survive finance scrutiny
- the team can cite 2 bets killed this quarter and why
- priorities change only with new evidence, not with loud voices
