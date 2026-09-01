---
name: pm-phase-deliver
description: >-
  Lean Double Diamond **Deliver phase** skill for PMs. Invoke when a
  feature/product is shipping or just shipped and the team needs **launch
  readiness, release communications, post-launch monitoring, experiment
  interpretation, or decision on next move** (iterate/scale/rollback/stop).
  Covers GTM launch readiness, release notes (user + internal + customer
  comms), post-launch monitoring, A/B experiment interpretation, product
  analytics narratives, and metric quality/guardrails. Trigger on "prepare a
  launch", "write release notes", "post-launch review", "did the A/B work?",
  "release notes para o time comercial". For funnel-shaped or growth-specific
  A/B tests (acquisition/activation/retention/monetisation), use
  `pm-archetype-growth` for the interpretation lens — this skill covers
  feature-level A/B and post-launch decisions across all product types.
---

# PM Phase — Deliver

> Double Diamond Phase 4 of 4. Release is the start of proof, not the end of the work.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke when:

- a launch is imminent and readiness needs to be verified
- release notes or customer/internal comms need to be drafted
- a feature has shipped and adoption/impact must be monitored
- an A/B test has finished and the ship/iterate/rollback decision is open
- a launch scorecard is due
- a post-launch review or close-out is being written
- metric quality or guardrails have thrown a flag

Trigger phrases: "prepare a launch", "write release notes", "post-launch review", "did the A/B work?", "interpret these results", "launch scorecard", "did adoption happen?", "should we ship the variant?", "release notes para o time comercial".

Don't use for discovery/strategy (→ earlier phase skills) or for post-mortem of a technical incident (that's eng's loop). For funnel-shaped or growth-specific A/B tests (acquisition / activation / retention / monetisation experiments where the discipline matters more than the launch readout), use `pm-archetype-growth` for the interpretation lens — this skill covers feature-level A/B and post-launch decisions across all product types.

## Prime directive

**A release is a hypothesis meeting reality.** Expert PMs plan the learning interval as carefully as the launch itself — with a scorecard, a rollback criterion, and a close-out memo that captures what was actually learned, not what was hoped.

## Calibrated disagreement

The default failure in Deliver is declaring victory on vanity metrics or conclusions the data doesn't support. Challenge premature success claims and name confounds before endorsing a launch narrative — see `../DOCTRINE.md`.

## Core sub-skills

### 1. Launch readiness and GTM coordination

Coordinate cross-functional work to bring a product/feature to market successfully and safely. A strong feature can fail commercially if readiness is weak.

Outputs: launch plan, beta plan, enablement checklist, launch FAQ, readiness sign-off, go/no-go memo.

Anti-patterns: GTM involved too late, no launch owner, missing support readiness, no launch measurement plan, "release = adoption" assumption.

→ Deep-dive: `references/launch-readiness.md`

### 2. Release notes (user + internal + customer)

Write release communications that are **fit for audience**: user-facing changelog (what's new, why they'll care), internal enablement (for sales/support/CS), and customer comms (email, in-app, migration notices). Release notes are the product's written face after each ship.

Outputs: public changelog entry, internal enablement one-pager, customer email, in-app release note, migration FAQ (if needed).

Anti-patterns: treating release notes as marketing, using eng-ticket language with customers, no support preparation, dumping every merged PR, vague "improvements and bug fixes" when there's a material change.

→ Deep-dive: `references/release-notes.md`

### 3. Post-launch monitoring and iteration

Run the weeks after launch as an explicit learning phase. Monitor usage, funnel, reliability, and support signals; compare actuals to hypothesis; decide iterate/scale/rollback/stop.

Outputs: launch dashboard, readout memo, close-out report, iteration backlog, rollback criteria.

Anti-patterns: launch-and-leave, measuring output volume only, no baseline, no support/rollback plan, no documented learning capture.

→ Deep-dive: `references/post-launch-monitoring.md`

### 4. Experiment design and interpretation

Interpret A/B and other product experiments with explicit hypotheses, primary metrics, guardrails, validity assumptions, and decision rules. Know when NOT to use A/B.

Outputs: experiment brief (cross-link to `pm-phase-develop` pre-launch), results readout, recommendation memo, holdout plan.

Anti-patterns: no primary metric, peeking without method support, underpowered tests, changing hypothesis post-hoc, shipping on noisy deltas.

→ Deep-dive: `references/experiment-interpretation.md`

### 5. Product analytics and dashboard interpretation

Use funnels, retention, cohorts, and segmentation to turn behavioural data into decisions — not just awareness.

Outputs: KPI dashboard spec, funnel analysis, retention report, cohort cut, weekly review pack.

Anti-patterns: dashboard worship, no segments, correlation-as-cause, reporting numbers without decisions.

→ Deep-dive: `references/product-analytics.md`

### 6. Metric quality and guardrails

Ensure metrics used for decisions are well-defined, trustworthy, and interpreted with awareness of bias, novelty effects, and side-effects. Design guardrails so the company does not optimise locally and harm retention, trust, or reliability.

Outputs: metric glossary, guardrail scorecard, experiment QA checklist, interpretation memo, launch-gate criteria.

Anti-patterns: one-metric obsession, shipping on averages that hide segment harm, ignoring support/trust/reliability side-effects, sloppy definitions shared across teams.

→ Deep-dive: `references/metric-quality-guardrails.md`

## Workflow

1. **Load context** — `.ai/memory/active-context.md`, PRD and tracking plan from `pm-phase-develop`, priorities from Define.
2. **Classify the ask** — readiness, release notes, monitoring, A/B interpretation, analytics narrative, or metric-quality check?
3. **Anchor on the hypothesis** — what were we trying to learn/achieve? State it upfront so the readout compares actuals to expectations.
4. **Respect the guardrails** — check reliability, support load, satisfaction, and revenue side-effects before calling a result a "win".
5. **Decide the move** — iterate, scale, hold, rollback, or stop. Decisions beat descriptions.
6. **Persist** — launch memo → `.ai/memory/projects/<slug>/launches/<name>.md`; experiment results → `experiments.md` using the template; close-out → `retrospective.md`.

## Output contract

```text
## [Artefact] — [launch/experiment/release notes title]

### Hypothesis recap
### What shipped
### Primary metric + guardrails (actual vs expected)
### Segments / cohorts
### Side-effects observed
### Decision (iterate / scale / hold / rollback / stop)
### Communications (release notes / internal / customer) — linked or inlined
### Follow-up actions + owners
### Memory updates
```

## Integration

- Upstream: `pm-phase-develop` (PRD, tracking plan, acceptance).
- Transversais: `pm-transversal-docs` (publishing release notes in Confluence, Jira tickets for iterate/rollback), `pm-transversal-analysis` (the bridge for deeper quali+quant synthesis and triangulation on user-feedback post-launch), `pm-transversal-stakeholder` (exec readout, DACI for ship decision).
- Cross-functional pairings: your QA lead stress-tests metric interpretation and experiment integrity; your designer reviews UX post-launch; a data-science partner validates the maths when an A/B looks like a win.
- Archetype lenses (load when the product type warrants): `pm-archetype-growth` for funnel/activation/retention readouts; `pm-archetype-ai` when the launch is a model and the release gate is an eval threshold; `pm-archetype-enterprise` for staged-rollout governance; `pm-archetype-platform` for adoption / migration / SLO tracking.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is a 1-page hypothesis → actuals → decision → follow-up; Standard is the full launch readout with scorecard; Caveman is a 5-line shipped-X / metric-Y-vs-Z / decision / next.

## Success criteria

- every launch has a written hypothesis and a close-out comparing actuals
- release notes are fit for each audience (users ≠ sales ≠ customers)
- decisions are made within a declared learning window, not by drift
- guardrail violations are caught before the feature scales
- the team accumulates a library of "what we learned" that improves the next bet
