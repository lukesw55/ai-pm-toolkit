# Metric quality and guardrails

## What it is

Ensuring the metrics used for decisions are **well-defined, trustworthy, and interpreted with awareness of bias, novelty effects, and side-effects**. Designing guardrails so the company does not optimise locally and harm retention, trust, or reliability.

## Why it matters

Experienced PMs must know whether a measured change is **real, meaningful, and safe to ship**. Most "wins" that turn into regrets fail because metric quality was weak or guardrails were missing.

## The three failure modes

### 1. Definition drift
The metric formula or cohort changes silently between when it was designed and when it's reported. Nobody catches it; everyone trusts numbers that mean different things over time.

**Counter:** metric dictionary, change log, QA on any formula change.

### 2. Measurement bias
The instrumentation misses a population (adblocker users, mobile safari, specific regions) or double-counts another. The headline number is wrong in a predictable direction.

**Counter:** server-side for critical events, SRM checks, segment sanity comparisons.

### 3. Interpretation bias
The number is correct but interpreted wrong. Example: "conversion went up" actually means "we killed low-intent traffic", not "we converted better".

**Counter:** segment view, guardrail set, causal reasoning discipline.

## Ready-to-use template — Metric dictionary entry

```markdown
## Metric: [name]

**Definition (plain English):** [what it measures]
**Formula:** [precise math, e.g. `count(distinct user_id where fired project_created within 24h of signup) / count(distinct user_id where fired signup_completed)`]
**Unit:** [%, count, ms, $]
**Source event(s):** [list]
**Cohort scope:** [which users are included]
**Exclusion rules:** [bots, internal users, test accounts]
**Timezone / window:** [UTC / user-local / business day]
**Owner:** @name
**Canonical dashboard:** [link]
**Aliases (deprecated):** [old names]
**Change log:**
- [date] initial definition
- [date] excluded bot traffic (retroactively? or going forward?)
```

## Guardrail set — what to include

A guardrail set is the **list of metrics that must not degrade** when a change ships. Typical guardrails:

### Reliability
- p95 / p99 latency for the affected flow
- error rate (user-observable + server-side)
- crash rate (mobile / web)
- uptime / availability SLI

### User health
- retention cohort (not just new-user adoption)
- churn signal
- session length + depth (both directions matter)
- NPS / CSAT drift
- support ticket volume (per 1k users, category-specific)

### Trust + safety
- privacy-related escalations
- security incidents
- compliance violations
- moderation volume (for UGC / community products)

### Business health
- revenue / conversion (for monetisation-adjacent changes)
- CAC impact (for acquisition changes)
- unit-economics impact (for pricing / usage changes)

### Segment-level guardrails
The most important and most-missed: **does the change help one segment and hurt another?**

- enterprise vs self-serve
- power users vs new users
- paid vs free
- geography
- platform (web, mobile, API)

## Ready-to-use template — Guardrail scorecard

```markdown
# Guardrail scorecard — [launch / experiment / period] — [YYYY-MM-DD]

| Metric | Baseline | Current | Δ | Tolerance | Status |
|---|---|---|---|---|---|
| p95 latency | 250ms | 260ms | +4% | +/- 5% | ✅ |
| error rate | 0.3% | 0.4% | +33% | not worse | ⚠️ watch |
| support tix / 1k users | 4.2 | 4.5 | +7% | +/- 10% | ✅ |
| retention (wk 2 cohort) | 48% | 46% | -2pp | not worse | ⚠️ watch |
| churn signal | - | - | - | - | too early |

## Active watches / breaches
- [metric]: [what's happening, what we're doing]

## Decision rule
If any guardrail is RED: pause rollout, investigate. If YELLOW: continue but monitor daily. If GREEN: expand cohort / ship.
```

## Causal reasoning discipline

When a metric moves, ask in order:

1. **Is the measurement itself correct?** Did instrumentation change? Definition drift? Tracking gap?
2. **What else changed at the same time?** Other launches, seasonality, marketing campaign, pricing change, upstream data-source change?
3. **Is the move segment-wide or concentrated?** Overall +5% could be +20% in one segment and 0 elsewhere.
4. **Is it novelty or sustained?** Week 1 excitement decays; sustained effects matter.
5. **Is there a plausible causal story?** If you can't articulate the mechanism, be humble about the attribution.
6. **What would a counterfactual cohort show?** If a holdout exists, use it. If not, construct one.

"Metric moved because we shipped X" is a hypothesis, not a conclusion. Treat it as such.

## Common bias patterns to watch for

### Sample ratio mismatch (SRM)
Variant split is supposed to be 50/50 but is 48/52. Red flag — something is broken.

### Novelty effect
New thing is exciting → metric jumps → settles back. Measure week-1 separately from week-N.

### Segment composition shift
Your cohort composition changes over time (more free users, fewer paid → headline metric shifts without underlying behaviour change).

### Survivorship bias
Measuring retained users only → biased up. Always include churned users in retention denominators.

### Selection bias
Users who opted into a beta are not representative. Generalising to the full population requires correction.

### Simpson's paradox
Trend in segments reverses at aggregate level. Always view segments before drawing conclusions from averages.

### Goodhart's law
When a metric becomes a target, it ceases to be a good metric. Teams optimise the measure, not the underlying value.

## Common anti-patterns

- **One-metric obsession.** Pushing North Star without watching guardrails.
- **No SRM check.** Experiments analysed without confirming the variant split.
- **Shipping on averages that hide segment harm.** Paid users improved; free users regressed; aggregate flat → "no effect".
- **Novelty-driven ship decisions.** Week-1 win; it's gone by week 4.
- **Silent definition change.** "We updated the formula" — dashboards shift; nobody told downstream consumers.
- **Ignoring support / trust / reliability.** Product metric looks great; support queue is exploding.
- **Confirming instead of falsifying.** Data analysed to find evidence for the decision already made.
- **Comparing incomparable cohorts.** Last year vs this year for a fast-growing product is rarely apples-to-apples.

## Launch-gate criteria (pre-GA)

Before any launch ships to 100%:

- [ ] primary metric + MDE + target defined
- [ ] guardrail set agreed + thresholds written
- [ ] SRM check automated in experiment config (if A/B)
- [ ] segment view implemented in dashboard
- [ ] roll-back criteria + process written
- [ ] metric dictionary entries current
- [ ] owner named for each guardrail

No launch reaches GA without these.

## Seniority signals

- **Beginner:** understands that not all metrics are equally reliable.
- **Intermediate:** uses guardrails in launch and experiment reviews.
- **Advanced:** spots misleading improvements and bad metric setups; challenges team's interpretation when warranted.
- **Expert:** designs evaluation systems that protect the company from false positives and local optimisation; raises org-wide measurement quality.

## Files

Metric dictionary → `.ai/memory/projects/<slug>/metric-dictionary.md`. Guardrail definitions → alongside launch plans. Active scorecards → launch pages. Breach investigations → `.ai/memory/projects/<slug>/incidents/` (even if no user incident, a metric breach deserves a short writeup).
