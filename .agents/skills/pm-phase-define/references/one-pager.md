# One Pager — stage 4

## What it is

A **concise synthesis** of validated problem + proposed solution direction + expected impact, produced right after Discovery (stage 3) and before Product Prioritisation (stage 5). It's the artefact that lets the team pick the bet to build.

Think of it as the **bridge between "we understand the problem" and "we're committing to build something"**.

## Why it matters

Without the One Pager, Discovery insight goes into a deck nobody reads, or gets lost in a Slack thread, or prematurely hardens into a PRD before priorities are set. The One Pager forces synthesis and comparability — you can rank One Pagers against each other.

## Ready-to-use template — One Pager

```markdown
# One Pager — [Initiative name] — [YYYY-MM-DD]

**Status:** Draft | In review | **Approved for build** | Parked | Rejected
**PM:** @name
**Links:** impact-brief.md / discovery synthesis / strategy memo / sizing (if done)
**Stage:** One Pager (stage 4 of 8)

## TL;DR
Three sentences:
1. Problem + segment (1 sentence).
2. Proposed solution direction (1 sentence — not detailed).
3. Expected primary-metric movement + confidence (1 sentence).

## Problem (validated)
What discovery confirmed. ≤ 100 words.
- segment:
- pain moment:
- frequency + severity:
- evidence: [N interviews + quant signal + competitive check]

## JTBD (concise)
The job users are hiring this solution for, in their words. 1-2 sentences.
Link to full JTBD in discovery synthesis if needed.

## Proposed direction
High-level approach. NOT a detailed solution. 2-3 sentences.
Mention 1 alternative you considered and rejected.

## Expected impact
| Dimension | Current | Expected | Confidence |
|---|---|---|---|
| Primary metric | [baseline] | [target] | low / med / high |
| Secondary metric | [baseline] | [target] | low / med / high |
| Guardrail risk | [current] | [at-risk threshold] | watch |

Confidence justification in 1 line.

## Strategic fit
Which pillar of the strategy memo this serves. If it doesn't map cleanly, say so and argue for inclusion.

## Effort + timing
- rough effort: [team-weeks]
- rough timing: [quarter or window]
- staging: [MVP → beta → GA]

## Non-goals
What we explicitly do NOT include in this bet.

## Risks (top 3)
- risk → mitigation

## Dependencies
- [team] for [what] by [when]

## Ask
- approve to prioritise for build (advance to stage 5)
- decline with rationale
- park with refresh trigger
- request more discovery
```

## Length

**One page**. Discipline matters: if it doesn't fit, it's not synthesized yet.

## The Five Unlocks — a One Pager quality bar

A One Pager is ready when it unlocks these five questions in under 5 minutes of reading:

1. **Who?** — specific segment, not "users".
2. **What's the real problem?** — evidenced, not hypothesized.
3. **What would we do about it?** — direction, not exhaustive spec.
4. **What will change?** — metric + magnitude + confidence.
5. **Why now / why this / why us?** — strategic fit + competitive timing.

Missing any of the five → not yet a One Pager.

## One Pager vs Impact Brief

| Aspect | Impact Brief (stage 2) | One Pager (stage 4) |
|---|---|---|
| Purpose | should we invest discovery? | should we invest build? |
| Evidence depth | rough, order-of-magnitude | validated, discovery-backed |
| Solution? | no — just problem worth investigating | yes — direction, not detail |
| Length | 1 page | 1 page |
| Decision | advance to Discovery / reject | prioritise for build / park / reject |

## Common anti-patterns

- **Mini-PRD.** Too much implementation detail. One Pager is about the bet, not the build.
- **Unvalidated problem.** If discovery didn't close the loop, don't write a One Pager — go back to stage 3.
- **Vague impact.** "Users will love it" is not impact. Metric + direction + magnitude + confidence.
- **No alternatives considered.** A One Pager without a rejected alternative looks like the only option existed — usually means the thinking wasn't deep enough.
- **Spreading across 3 pages.** The discipline of one page is the skill. Multi-page = skip this stage.

## Ranking multiple One Pagers

When stage 5 (Product Prioritization) evaluates competing One Pagers, each should be scoreable against:

- expected impact × confidence
- effort
- strategic-fit
- dependency cost
- competitive timing

See `prioritisation-frameworks.md` for RICE / WSJF / scorecard templates adapted to this stage.

## Who signs off

- **Driver:** PM
- **Approver:** area product director
- **Contributors:** design lead (for direction feasibility), tech lead (for effort sanity-check), PMM (for positioning)
- **Informed:** CS, sales (if user-facing), analytics (for measurement design)

## Files

`.ai/memory/projects/<slug>/one-pagers/<initiative>.md`. Publish to Confluence via `pm-transversal-docs` when approved. Linked from the Impact Brief it evolved from and from `priorities.md`.
