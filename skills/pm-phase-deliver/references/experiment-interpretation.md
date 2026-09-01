# Experiment design and A/B interpretation

## What it is

Designing and interpreting controlled tests and other product experiments with **explicit hypotheses, primary metrics, guardrails, validity assumptions, and decision rules**. Knowing what counts as trustworthy evidence — and knowing when NOT to use A/B.

## Why it matters

Mature PM teams learn through experiments; expert PMs understand what counts as trustworthy evidence. Bad experiment interpretation ships wrong bets or kills good ones.

## When A/B fits — and when it doesn't

A/B is right when:
- you can randomly assign users to variants
- effects are measurable within a reasonable window (days to weeks)
- sample size is large enough for statistical power
- the change is independent enough not to interact with other experiments

A/B is **wrong** for:
- small teams / small user bases (underpowered)
- long-lag outcomes (annual contract renewals)
- new-product launches with no baseline
- changes that need qualitative understanding first (go discover it)
- brand / positioning / major-UX overhaul (holistic evaluation beats A/B)
- network-effect products where variant assignment violates independence

Alternatives when A/B doesn't fit:
- cohort comparison (pre/post with matched controls)
- difference-in-differences (with a control cohort that didn't get the change)
- interrupted time series
- qualitative usability + subsequent scaled rollout
- holdouts at segment level rather than user level

## Ready-to-use template — Experiment brief (pre-launch)

```markdown
# Experiment brief — [Name] — [YYYY-MM-DD]

**Status:** Design | **Running** | Complete | Rolled back
**PM:** @name   **Analytics:** @name   **Eng:** @name
**Linked:** PRD / tracking plan / launch plan
**Variant live:** v1 / v2 / v3

## Hypothesis
We believe that [change] will cause [effect] for [segment], because [reasoning].

## Primary metric
- definition:
- formula + event(s) it depends on:
- baseline (last 30d):
- minimum detectable effect (MDE): X% relative / absolute
- practical significance threshold: move at least [Y] to be worth shipping

## Guardrail metrics (must not degrade)
| Metric | Current | Tolerance |
|---|---|---|
| reliability p95 | | +/- 5% |
| support ticket rate | | not worse |
| churn cohort signal | | not worse |
| retention 7d | | not worse |

## Secondary metrics (informational)
- [metric] — interpretation note

## Variants
- **Control (v0):** current experience
- **Treatment v1:** [description of change]
- **Treatment v2 (optional):** [description of change]

## Sample size + duration
- expected sample per variant per week: N
- required sample for MDE at 80% power, alpha=0.05: M
- expected duration: [weeks]
- minimum duration: [1-2 weekly cycles to capture weekday patterns]
- maximum duration: [to avoid novelty or seasonality confounds]

## Exposure logic
- how users are assigned (random hash? seat? account?)
- what defines "exposure" (saw the variant? took an action?)
- opt-in / opt-out handling
- carryover between variants (can a user switch?)

## Decision rules
- **Ship v1:** primary moves ≥ threshold AND guardrails hold AND no segment harm
- **Keep v0:** primary does not move OR moves below threshold
- **Rollback:** guardrail breached at any point
- **Iterate:** primary moves in right direction but below threshold → targeted v2
- **Hold:** inconclusive; extend by 1-2 weeks if feasible, else call inconclusive

## Analysis plan (before looking at results)
- segments to analyse: [list]
- heterogeneous effects to check: [segment × variant interaction]
- novelty effect check: compare week 1 vs week N+ within treatment

## Validity checks
- [ ] no sample ratio mismatch (SRM)
- [ ] no interaction with other running experiments
- [ ] cohort definitions consistent with tracking plan
- [ ] exposure timing makes sense (no look-ahead bias)
```

## Ready-to-use template — Results readout

```markdown
# Results readout — [Experiment] — [YYYY-MM-DD]

## TL;DR
One sentence recommendation: ship / iterate / kill / extend.

## Primary metric
| Variant | N | Value | Δ vs control | p-value / CI | Practical? |
|---|---|---|---|---|---|
| Control v0 | | | — | — | — |
| Treatment v1 | | | +X% | p=0.03 (CI [0.5%, 4.2%]) | yes / no |

## Guardrails
All held / [specific breach + detail].

## Secondary metrics
| Metric | Variant | Δ | Interpretation |
|---|---|---|---|

## Segment breakdown
| Segment | Δ primary (v1 vs v0) | Note |
|---|---|---|

Watch for:
- effect concentrated in one segment (is that OK?)
- segment harm hidden by average (is that OK?)

## Novelty / time effects
Week 1 vs week N: [same / decay / build]

## Qualitative signal
- support tickets in period:
- user comments:
- sales / CS anecdotes:

## Validity notes
- SRM check:
- interaction with other tests:
- any data-quality concerns:

## Recommendation + rationale
- decision:
- why:
- what would change this (e.g. if guardrail tightens, if segment view changes):

## Follow-ups
- if ship: rollout plan, release notes, close experiment
- if iterate: what the v2 test should be
- if kill: close-out memo + lessons learned
```

## Statistical traps to avoid

- **Peeking.** Looking at results before pre-registered sample size is reached → inflated false-positive rate. Use sequential methods or commit to fixed-horizon.
- **P-hacking.** Running 10 metric × segment combinations and cherry-picking the one that hit p<0.05. Pre-declare primary + a small set of secondaries.
- **Hypothesis rewriting after seeing results.** "We expected X, but actually we're now interested in Y." That's a new experiment.
- **Underpowered tests.** Not enough sample for the MDE you'd find practically meaningful → failing to detect real effects OR seeing noise.
- **SRM (sample ratio mismatch).** If assignment should be 50/50 but you see 48/52, something is broken before you even analyse results.
- **Multiple comparisons.** Claiming significance on one of many tested variants without correction.
- **Novelty effects treated as permanent.** Users click new things for a week because they're new, then stop.
- **Interaction effects.** Your experiment is running alongside 3 others; your effect might be driven by theirs.

## When results are inconclusive

Inconclusive ≠ "it doesn't work". It means the data didn't distinguish. Options:

- extend duration if sample budget allows
- narrow to the segment most likely to show effect
- re-examine whether the change was large enough to matter (was MDE realistic?)
- decide to ship anyway if the change is cheap, reversible, and the downside is small
- kill if the cost of continuing outweighs the potential upside

Don't claim success from inconclusive data.

## Non-A/B alternatives — when to use

- **Holdout:** ship to 90%, keep 10% on control indefinitely. Lets you measure long-term effect over months.
- **Pre/post with matched cohort:** useful when randomisation is impossible (marketing campaigns, full rollouts).
- **Difference-in-differences:** two cohorts, one gets the treatment, compare trajectories.
- **Interrupted time series:** single cohort, measure trend before and after intervention.
- **Feature-flag canary:** not an experiment — a rollout de-risker.

## Common anti-patterns

- **No primary metric.** "We'll look at everything." You'll find something significant by chance.
- **Peeking + stopping early on favourable results.** Classic bias amplifier.
- **Shipping on noisy deltas.** +0.2% with CI [-1%, 1.4%] is not a signal.
- **Ignoring guardrails.** Primary moved; churn moved too; we ship anyway. No.
- **No practical threshold.** Stat-sig ≠ business-meaningful.
- **Celebrating over-interpretation.** "Checkout converted 12% better in the test!" — with N=150, that's noise.

## Integration

- Pre-launch experiment brief — drafted in `pm-phase-develop` alongside PRD
- Tracking plan alignment — primary metric + guardrails must be in the tracking plan before launch
- Post-launch interpretation — this reference
- Metric quality + guardrails — see `metric-quality-guardrails.md`

## Seniority signals

- **Beginner:** participates in established test programs.
- **Intermediate:** defines sensible hypotheses and metrics.
- **Advanced:** designs sound experiments and interprets results without common statistical traps.
- **Expert:** raises experimentation quality across teams; knows when not to A/B.

## Files

Experiment briefs + readouts → `.ai/memory/projects/<slug>/experiments.md` using the template in `.ai/memory/_templates/experiment-log.md`. Close out on ship or kill — no orphan experiments.
