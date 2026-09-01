# Strategy memo

## What it is

A concise written artefact that defines long-term direction, strategic pillars, strategic bets, and — critically — **what the team will NOT do**. It's the answer to "what are we choosing?"

## Why it matters

Without a written strategy, teams default to local optimisation, random feature accumulation, and re-arguing priorities every quarter. A strategy memo converts judgement into an auditable, shareable choice.

## What a strategy memo is NOT

- **Not a roadmap.** Roadmap = sequencing; strategy = why that sequencing.
- **Not a vision statement.** Vision = aspiration ("the best X in the world"); strategy = choices ("we win by doing A, not B").
- **Not a KPI list.** KPIs instrument the strategy; they don't replace it.

## Template (1–3 pages)

```markdown
# [Product area] strategy — [horizon, e.g. 2026]

## TL;DR
Two sentences. Where we play + how we win.

## Where we play
- segment(s) we serve:
- jobs we help users do:
- channels / markets:
- what category we compete in (as the customer sees it)

## How we win
- unique value we deliver:
- why customers switch to us (and why they stay):
- what capability we are compounding (moat):

## Strategic pillars (3–5)
Each pillar is a sustained investment area, not a quarterly theme. Pillar:
1. [Name] — [1-line rationale — what user/business outcome it drives]
2. ...
3. ...

## Strategic bets (this horizon)
Concrete initiatives that operationalise the pillars, ranked by impact × confidence:
1. [Bet] — pillar: [X] — expected outcome: [metric movement] — confidence: [low/med/high]
2. ...

## What we are NOT doing (explicit non-goals)
- segments we don't serve this horizon:
- features we don't build (even if requested):
- markets we don't enter:
- integrations we defer:

## Assumptions (load-bearing, with invalidation conditions)
- [assumption] — invalidated if [observation]
- ...

## Metrics we watch (link to KPI tree)
- North Star:
- leading input metrics:
- guardrails:

## Risks
- strategic:
- execution:
- market:

## Refresh cadence
When we revisit this memo and what would force an earlier refresh.
```

## Writing tips

- **Start with non-goals.** It's often easier to write what you're NOT doing than what you are. Non-goals force the trade-off.
- **Name the moat.** If you can't say what you're compounding, you probably don't have a strategy — you have a feature list.
- **One horizon per memo.** A 3-year vision and a 1-year strategy should be separate documents linked together.
- **Keep it < 3 pages.** If it's 10 pages, nobody reads it. If nobody reads it, it's not a strategy.
- **Dates > adjectives.** "Significantly improve" means nothing. "Move primary metric from 38% to 55% by end of Q3" means something.

## Common anti-patterns

- **Roadmap disguised as strategy.** A list of features with quarters attached. No "why", no "why not", no trade-offs.
- **Everything is a pillar.** 9 pillars = no pillars. 3–5 forces choice.
- **Goals without bets.** "We will be the leader in X" without initiatives is a wish.
- **Strategy that couldn't be wrong.** If no observation would force a rewrite, it's a belief, not a strategy.
- **Silent non-goals.** Choosing not to do X without writing it down → stakeholders keep asking for X, team keeps re-arguing.

## Seniority signals in strategy writing

- **Beginner:** writes product area strategy from existing guidance.
- **Intermediate:** shapes strategy for a defined scope, names pillars clearly.
- **Advanced:** writes strategy in ambiguous spaces with limited guidance; names trade-offs.
- **Expert:** sets direction across teams or product lines; strategy shapes investment allocation.

## Files

`.ai/memory/projects/<slug>/strategy.md`. Cross-link from project profile and from KPI tree. Keep a version history (`strategy-2026-Q1.md`, etc.) so changes are visible.
