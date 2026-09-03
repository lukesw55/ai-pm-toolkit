# One Pager — stage 4

## What it is

A **concise synthesis** of validated problem + proposed solution direction + expected impact, produced right after Discovery (stage 3) and before Bet Selection + Scope Slicing (stage 5). It lets the team compare validated bets without becoming a mini-PRD.

Think of it as the **bridge between "we understand the problem" and "we're committing to build something"**.

## Why it matters

Without the One Pager, Discovery insight goes into a deck nobody reads, or gets lost in a Slack thread, or prematurely hardens into a PRD before priorities are set. The One Pager forces synthesis and comparability — you can rank One Pagers against each other.

## Ready-to-use template — One Pager

```markdown
# One Pager — [Initiative name] — [YYYY-MM-DD]

**Status:** Draft | In review | **Ready for bet selection** | Parked | Rejected
**PM:** @name
**Links:** impact-brief.md / discovery synthesis / opportunity tree (node O<n>-S<k>) / strategy memo / sizing (if done)
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
Traceability: opportunity O<n> and solution S<k> from the opportunity tree; the rejected alternative is a sibling solution.

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

## Assumptions (mapped)
Open rows of the assumption map for the chosen solution: ID (O<n>-S<k>-A<m>), status (verified / inferred / unverified), and either the test (O<n>-S<k>-E<j>) or the accepted-risk decision: owner, rationale, reconsideration trigger (condition or date). An unverified assumption with neither blocks this handoff.

## Dependencies
- [team] for [what] by [when]

## Ask
- approve for bet selection and scope slicing (advance to stage 5)
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
| Decision | advance to Discovery / reject | select and slice / park / reject |

## Common anti-patterns

- **Mini-PRD.** Too much implementation detail. One Pager is about the bet, not the build.
- **Unvalidated problem.** If discovery didn't close the loop, don't write a One Pager — go back to stage 3.
- **Orphan solution.** A solution with no parent opportunity in the tree is an idea, not a bet. Attach it to an opportunity, map its assumptions, or park it.
- **Vague impact.** "Users will love it" is not impact. Metric + direction + magnitude + confidence.
- **No alternatives considered.** A One Pager without a rejected alternative looks like the only option existed — usually means the thinking wasn't deep enough.
- **Spreading across 3 pages.** The discipline of one page is the skill. Multi-page = skip this stage.

## Selecting and slicing at stage 5

When several validated One Pagers compete for the same capacity, compare them against:

- expected impact × confidence
- effort
- strategic-fit
- dependency cost
- competitive timing

Do not restart problem prioritisation or manufacture new scores. Use the evidence already linked from Discovery and the One Pager. If one bet is already funded, record the selection without ceremony. Then use `../../pm-phase-develop/references/backlog-scope-slicing.md` to define V1, later slices, the learning goal and explicit non-goals before writing the PRD.

## Who signs off

- **Driver:** PM
- **Approver:** area product director
- **Contributors:** design lead (for direction feasibility), tech lead (for effort sanity-check), PMM (for positioning)
- **Informed:** CS, sales (if user-facing), analytics (for measurement design)

## Files

`.ai/memory/projects/<slug>/one-pagers/<initiative>.md`. Publish to Confluence via `pm-transversal-docs` when approved. Linked from the Impact Brief it evolved from and from `priorities.md`.
