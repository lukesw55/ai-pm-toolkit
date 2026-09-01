# Post-launch monitoring and iteration

## What it is

Running the weeks after launch as an **explicit learning and stabilisation phase** — not considering release the end of the work. Monitor usage, funnel, reliability, support; compare actuals to hypothesis; decide iterate / scale / hold / rollback / stop.

## Why it matters

Experienced PMs measure actual impact, detect side-effects quickly, and decide decisively. Weak teams ship, celebrate, and move on — then wonder a quarter later why the launch didn't move the metric.

## The learning window

Declare a **specific window** for learning (typically 3-6 weeks post-GA). Within this window:

- adoption / primary metric is actively monitored daily → weekly
- guardrails have alerting
- support / sales / CS feedback is triaged
- iteration decisions are made in-window, not deferred

After the window closes, the launch moves to **steady-state monitoring** and a **close-out memo** is written.

## Ready-to-use template — Launch scorecard

```markdown
# Launch scorecard — [Initiative] — week [N] of [target]

**Launch date:** YYYY-MM-DD
**Learning window:** T+0 → T+Nw
**PM:** @name

## Primary metric
| Metric | Baseline | Target | Actual (wk N) | Trajectory |
|---|---|---|---|---|
| [name] | [X] | [Y] | [Z] | on track / below / above / too early |

## Secondary metrics
| Metric | Baseline | Target | Actual | Note |
|---|---|---|---|---|
| adoption | | | | |
| depth of usage | | | | |
| retention cohort | | | | |

## Guardrails — are they holding?
| Guardrail | Threshold | Current | Status |
|---|---|---|---|
| reliability p95 | < 300ms | 280ms | ✅ |
| error rate | < 0.5% | 0.3% | ✅ |
| support ticket rate | < 2x baseline | 1.4x | ✅ (watch) |
| churn signal | < baseline | - | too early |

## Segment view
| Segment | Adoption | Primary metric | Notes |
|---|---|---|---|
| Free | | | |
| Pro | | | |
| Enterprise | | | |

Look for segments where the average hides harm.

## Qualitative signal
- support themes (top 3):
- sales win-loss mentions:
- NPS / CSAT drift (if measurable):
- community / social sentiment:
- internal team observations:

## Hypothesis vs reality
| Bet | Expected | Actual so far | Delta |
|---|---|---|---|
| [bet] | [expected outcome] | [observed] | [gap + interpretation] |

## Open issues / surprises
- [issue] — owner — target resolution

## Decisions this week
- [ ] continue as-is
- [ ] expand cohort / rollout %
- [ ] iterate: [what specifically]
- [ ] hold: [why]
- [ ] rollback: [criterion hit]

## Next check-in
- date:
- what we'll know by then:
```

## Decision rules — ship / iterate / rollback / stop

Declare these **before launch**, so the in-window decision is disciplined:

### Green — scale
- primary metric on track or above
- guardrails holding
- no surprising negative segment effects
- → expand cohort or push to 100%

### Yellow — iterate
- primary metric below target but moving in the right direction
- OR one guardrail watched but holding
- OR qualitative surprise (users using it differently than expected)
- → hold current cohort %, ship 1-2 targeted improvements, re-measure

### Red — rollback
- primary metric not moving or negative
- OR any guardrail breached (reliability, churn signal, trust incident)
- OR segment harm (feature helps one group, hurts another meaningfully)
- → flag off or revert to previous version; communicate; write close-out

### Stop
- after iteration, still no signal → kill the bet
- write a close-out memo with what was learned
- the learning itself is valuable; recording it prevents re-doing the same bet

## Close-out memo (end of learning window)

Write within 1 week of the window closing. 1-page memo.

```markdown
# Close-out — [Initiative] — [YYYY-MM-DD]

## What we shipped
Brief recap.

## Hypothesis vs outcome
- we expected:
- we observed:
- confidence we learned what we set out to learn:

## Decision + rationale
- ship as-is / iterate / kill
- why

## Learnings (ranked)
1. [learning — implication for future work]
2. [learning]
3. [learning]

## What surprised us
Unexpected findings, including things that would have changed our bet if we'd known.

## Follow-ups
- iteration backlog items:
- changes to tracking plan:
- changes to strategy / roadmap:
- anti-patterns to flag next time:

## Memory updates
- experiments.md (close the experiment entry)
- retrospective.md (team learnings)
- strategy.md (if the finding changes strategy)
```

## Rollback discipline

Rollback is a **normal tool, not a failure**. Treat it as such culturally:

- pre-declared rollback criteria (in the PRD + launch plan)
- rollback is 1 flag toggle + 1 message, not a week-long project
- communicate immediately and transparently (internal first, customer fast)
- follow up with close-out explaining what we learned + what's next
- no blame — rollback is the system working

## Common anti-patterns

- **Launch-and-leave.** Ship, celebrate, no one monitors.
- **Measuring only output.** "Feature X shipped" ≠ success metric.
- **No baseline.** "Conversion is 5%" — 5% of what and up from what?
- **No segment view.** Average looks fine; one segment is collapsing.
- **No support / rollback plan.** Problems surface; no playbook.
- **No documented learning.** Next PM re-proposes the same bet in 6 months.
- **Vanity iteration.** "It didn't work, let's add AI to it" — iteration without diagnosis.
- **Confirmation bias on results.** Selectively reading data to justify the ship.

## Daily → weekly → monthly cadence

- **Day 0-3:** daily check on primary metric + guardrails (automated alerts on guardrails)
- **Week 1-2:** weekly scorecard review; segment + qualitative pass
- **Week 3-6:** bi-weekly; trigger-based (on anomalies) daily
- **After window closes:** monthly steady-state monitoring moves to team health dashboard

## Seniority signals

- **Beginner:** checks basic adoption post-launch.
- **Intermediate:** runs a structured launch review with scorecard.
- **Advanced:** compares learned vs expected outcomes and adjusts decisively; decisions happen in-window.
- **Expert:** turns post-launch review into a systematic source of organisational learning; teams carry forward sharper intuitions.

## Files

`.ai/memory/projects/<slug>/launches/<initiative>.md` updated weekly. Close-out → `.ai/memory/projects/<slug>/launches/<initiative>-closeout.md`. Experiment link → `experiments.md`.
