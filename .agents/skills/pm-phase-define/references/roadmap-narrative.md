# Roadmap narrative

## What it is

A roadmap that tells a story: **strategy → sequenced bets → dependencies → expected outcomes**. Roadmaps create understanding, not just visibility.

## Why it matters

An expert PM's roadmap is a decision-quality artefact. Stakeholders should be able to look at it and answer: "why this bet, why this quarter, what's at risk, what are we not doing?"

## Roadmap types — pick the right one

| Type | Strength | When to use |
|---|---|---|
| **Outcome roadmap** | Ties work to user/business outcomes | Outcome-led orgs, leadership reviews |
| **Theme roadmap** | Groups by strategic theme | Multi-team areas, mid-term horizon |
| **Now / Next / Later** | Honest about commitment gradient | Startups, fast-moving contexts |
| **Timeline roadmap** (Gantt-ish) | Hard date commitments | Regulated launches, partner commitments, contract deadlines |
| **Portfolio roadmap** | Cross-area investment visibility | Exec / org-wide view |

Default for most software PM contexts: **outcome + now/next/later hybrid**. Use timeline only when dates are genuine commitments.

## Structure (outcome + now/next/later)

```markdown
# [Product area] roadmap — [horizon]

## TL;DR
Two sentences: what we're sequencing and why.

## Strategy recap
One paragraph linking back to strategy memo pillars.

## North Star
What moves if this roadmap executes.

## Now (committed — in flight)
### [Initiative]
- outcome: [user or business outcome expected]
- why now: [dependency, timing, evidence]
- success criteria: [metric + baseline → target]
- team: [people / roles]
- risks: [top 1–2]
- links: [PRD, design, tracking plan]

### [Initiative]
...

## Next (planned — queued)
### [Initiative]
- outcome:
- why this next: [what it unblocks, or why it's higher confidence than "later"]
- open questions:
- readiness: [what has to be true before it moves to "now"]

## Later (candidates — directional)
Brief list with 1-line rationale each. Commitment level: directional, not promised.

## Explicit non-goals this horizon
- [what we are NOT doing, with 1-line rationale]

## Dependencies + timing risks
Cross-team or external dependencies that affect the roadmap sequencing.

## Refresh cadence
- review: [weekly / bi-weekly]
- refresh: [monthly / quarterly]
- change-log link:
```

## Roadmap narrative — the short-form version

When presenting the roadmap (not just publishing it), prepare a 5-slide / 1-page narrative:

1. **The bet.** What user/business outcome we're going after.
2. **Why now.** Evidence + timing.
3. **What we're sequencing.** Now / Next / Later (with outcomes, not features).
4. **What we're NOT doing.** Explicit non-goals.
5. **What would change this.** Trigger conditions for replanning.

## Updating the roadmap

When reality shifts:

- **Evidence arrived** (experiment result, market change) → update Now/Next/Later and log what changed.
- **A commitment slips** → move to "at risk" explicitly; don't silently re-date.
- **A dependency breaks** → flag and re-sequence; don't hide it.
- **A bet invalidates** → move to "dropped" with rationale; don't leave zombies in "later".

## Common anti-patterns

- **Date theatre.** Fake dates that nobody believes, picked for political reasons.
- **Feature laundry list.** A Gantt chart of features with no outcomes, no rationale, no strategy link.
- **Roadmap without rationale.** "Trust me, it's prioritised."
- **Conflating commitment levels.** "Now" that's actually a bet, "later" that's actually dropped.
- **Static roadmap.** Updated quarterly with no visible log of changes — nobody trusts what they read.
- **100% committed.** A roadmap with no slack = a roadmap that will miss every surprise.

## Stakeholder-specific versions

Same roadmap, different lens:

- **Engineering leadership:** emphasise dependencies, tech debt, platform work.
- **Sales / CS:** emphasise what customers will see, when, and how to talk about it.
- **Executive:** emphasise strategic pillars, bets, and expected outcomes.
- **Customers (external):** directional, no dates unless committed, clear about what's not coming soon.

Don't create 4 roadmaps; create 1 roadmap and 3 summaries linked to it.

## Validation

Roadmap is working when:
- anyone on the team can explain the top 3 bets and why in 2 minutes
- "why are we doing X before Y?" has an answer
- the roadmap survives a round of stakeholder questions without the PM "taking it offline"
- "later" items cycle to dropped or promoted — not a permanent holding pen
- non-goals prevent re-arguing the same requests month after month

## Files

`.ai/memory/projects/<slug>/roadmap.md` + `roadmap-faq.md` (anticipated questions). Versioned (`roadmap-2026-Q1.md` etc.) so changes are visible. Linked from strategy + priorities.
