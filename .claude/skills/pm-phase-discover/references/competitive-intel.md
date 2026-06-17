# Competitive and market intelligence

## What it is

Collecting and interpreting competitor, category, and analyst signals to understand positioning, timing, gaps, and defensible advantage.

## Why it matters

Experienced PMs need to understand not only customer demand but also the strategic environment. Winning products are positioned in markets, not just built in backlogs.

## What is NOT competitive intel

- **Feature-parity checklists.** Copying competitor features without customer evidence = reactive roadmap.
- **Screenshot libraries.** Collecting UIs without analysing trade-offs and customer consequences.
- **Panic-driven priority shifts.** Competitor launches a thing → team scrambles. Without judgement, this destroys strategy.

## What good competitive intel does

- sharpens positioning
- informs sequencing ("we have 6 months before X catches up; what do we do with it?")
- spots category gaps nobody is addressing
- surfaces adjacent substitutes (users don't care whether the alternative is in your category)

## Sources + cadence

| Source | Cadence | What you learn |
|---|---|---|
| Competitor product itself | Monthly | Shipped features, UX direction |
| Competitor changelog / release notes | Monthly | Ship velocity, focus areas |
| Competitor pricing page + plans | Quarterly | Positioning, packaging, target segment |
| Competitor job listings | Quarterly | Investment areas (eng, GTM, vertical focus) |
| Analyst reports (Gartner, Forrester) | Annual | Category narrative, enterprise buyer lens |
| Customer win-loss calls | Continuous | Why we won/lost; what competitor did better |
| Sales CRM competitor field | Monthly | Deal-level competitive pressure |
| Reviews (G2, Capterra) | Quarterly | Customer love + hate themes |
| Community (Reddit, Slack, forums) | Continuous | Unfiltered customer signal |
| Conference talks + keynotes | As available | Stated strategy |
| Investor earnings calls / S-1s | Quarterly | Financial shape + strategic claims |

## Competitive brief template

```markdown
# Competitive brief — [competitor name] — [date]

## One-liner
How they position themselves in their own words. Direct quote if possible.

## Target customer
Which segments are they winning in? Which are they losing in?

## Product pillars (what they invest in)
Ranked by evidence (releases, job posts, execs quoted):
1. ...
2. ...

## Strengths (objective — what customers say)
- ...

## Weaknesses (objective)
- ...

## Pricing & packaging
- plans, tiers, value metric:
- anchor:
- migration / grandfathering:

## GTM motion
- sales-led / self-serve / hybrid:
- ICP:
- channel partners:

## Recent moves (last 6 months)
- ship velocity, major launches, M&A, leadership changes:

## What we do better
- evidence-backed:

## What they do better
- evidence-backed:

## Strategic implication for us
- positioning adjustment:
- prioritisation adjustment:
- timing adjustment:
- sequencing bet:
```

## Win-loss analysis

Themes > anecdotes. Patterns from 10+ deals > one loud loss.

Template for a win-loss call:

```
Deal: [name]
Outcome: won / lost / no-decision
Primary reason (from customer):
- user-stated:
- interpreted (behaviour + evidence):
Who else was in the final round:
What was the tie-breaker:
Price / feature / trust / timing / integration / change-management / relationship:
Quote to remember:
```

Synthesise monthly. Look for **pattern shifts** — is the reason we lose changing?

## Positioning memo

```markdown
# Positioning memo — [product or area]

## Category (as the customer thinks of it)
What category do our target customers mentally put us in when they shop?

## Target customer (ICP)
- segment + situation + job + alternative they currently use

## Key problem we solve (in their words)
Not ours. Theirs.

## Frame of reference
What are we "better than" — and concretely how?

## Unique value
What only we can credibly say.

## Proof points
Evidence customers would find credible (data, case studies, logos, technical specifics).

## What we are NOT
Segments and use cases we deliberately don't serve (or serve poorly).
```

## Perceptual map

Pick 2 axes the target customer cares about (e.g. ease-of-use × depth-of-capability, or price × integration-surface). Plot competitors. The gaps are the opportunities (or the deliberate traps).

Keep maps in `references/` — one per axis pair. Don't over-collect; 2–3 live maps is usually enough.

## Anti-patterns

- **Parity obsession.** "We need feature X because competitor Y has it" without customer evidence = reactive roadmap.
- **Category confusion.** Competing in the category you wish customers would use, not the one they use.
- **Analyst worship.** Treating a Gartner quadrant as truth rather than one signal among many.
- **Screenshot hoarding.** Collecting without synthesis.
- **Ignoring adjacent substitutes.** Users don't care if the alternative is in your category. If they solve their JTBD with a spreadsheet or with Notion, that's your competition.

## Files

Persist to `.ai/memory/projects/<slug>/competitive/<competitor>.md` + `positioning.md` + `market-map.md`. Keep each file current — stale competitive docs are worse than missing ones.
