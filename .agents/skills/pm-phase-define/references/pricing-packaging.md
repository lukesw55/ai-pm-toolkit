# Pricing and packaging fundamentals

## What it is

Designing **value metrics, plans, tiers, and monetisation structures** that align with customer value and the company's GTM model. Often shared with Product Marketing and Finance — this reference frames the PM's share of the work.

## Why it matters

In B2B, SaaS, and self-serve growth contexts, pricing & packaging is a strategic lever for adoption, retention, and margin. Done poorly, it constrains the product forever.

## Core concepts in two minutes

- **Value metric** — the unit customers pay against (seats, API calls, data volume, active workflows, revenue processed). A good value metric scales with the value the customer perceives.
- **Plan** — a bundle of capabilities + a price point + a value-metric tier.
- **Tier** — how plans ladder (Free → Pro → Business → Enterprise).
- **Packaging** — which features live in which tier, and why.
- **Anchor** — the plan a customer sees first; shapes willingness-to-pay perception.
- **Grandfathering** — policy for customers on old plans when prices change.

## Ready-to-use template — pricing memo

```markdown
# Pricing & packaging memo — [product or tier change] — [date]

## TL;DR
What's changing, for whom, why, and the expected effect.

## Context
- strategic reason:
- trigger (customer request, competitive, economic):
- link to strategy memo:

## Current state
- existing plans + tiers:
- existing value metric:
- current ARR mix by plan:
- known friction points:

## Proposed change
- new plan / tier / value metric / price point:
- visual: before → after table:

## Value metric choice + rationale
Why this value metric scales with customer-perceived value. What we considered and rejected.

## Packaging logic
| Feature / capability | Free | Pro | Business | Enterprise | Rationale |
|---|---|---|---|---|---|
| ... | ✓ | ✓ | ✓ | ✓ | foundational |
| ... |  | ✓ | ✓ | ✓ | power-user threshold |
| ... |  |  | ✓ | ✓ | team / scale threshold |
| ... |  |  |  | ✓ | compliance / governance |

## Willingness-to-pay evidence
- internal data: current ARPU, conversion by tier, churn by tier
- customer research: interview themes, concept test results
- competitive: competitor pricing pages, win-loss themes
- quantitative: conjoint (if available), price-sensitivity survey

## Migration plan
- grandfathering policy for existing customers:
- communication plan + timeline:
- sales / CS enablement:
- support implications:
- risk of churn:

## Experiment plan (if applicable)
- cohort / region for A/B test:
- primary metric + guardrails:
- stop conditions:

## Financial model
- projected ARR change:
- projected churn impact:
- support / ops cost impact:
- break-even horizon:

## Risks
- commercial:
- positioning:
- operational:
- legal / regional:

## Decision ask
- what we need approved and by whom
- DACI link
```

## Choosing a value metric — checklist

A good value metric:

- [ ] scales with customer perceived value (they don't feel punished for succeeding)
- [ ] is measurable and auditable (clearly counted)
- [ ] predictable for the customer's finance team (no surprise bills)
- [ ] maps to a natural usage pattern (not contrived)
- [ ] aligns with how you incur cost (so margins stay sane)
- [ ] allows segmentation (Free vs Pro vs Enterprise thresholds feel natural)

## Packaging principles

- **Good-better-best with clear jumps.** Tiers should have meaningful gaps, not incremental additions.
- **Feature stratification follows value, not cost.** "Hard to build" ≠ "belongs in higher tier".
- **Don't over-package.** 8 tiers + 14 add-ons = no customer can decide.
- **Enterprise earns its price through control + support + compliance + scale** — not just "the same + more".
- **Free should showcase value and create a real path to paid** — not just limit users into frustration.

## Migration carefully

Pricing changes that touch existing customers require disproportionate care:

- **Grandfather generously when the change is yours, not the customer's.** If you're ratcheting up price because your costs grew, customers didn't cause that.
- **Communicate early and clearly.** The first time a customer hears about a price change should not be at renewal.
- **Offer choice during transition.** Stay on old plan N months, migrate to new plan, or accept a locked rate for renewal.
- **Monitor churn and NPS by cohort post-change.** Expect some churn; compare to your model.

## Anti-patterns

- **Cost-plus pricing.** "It costs us $X to run, so we charge $X × 3." Ignores value.
- **Competitor-copy pricing.** Match a competitor's pricing page without understanding their cost structure or segment.
- **Value metric mismatch.** Per-seat pricing for a product whose value is consumption-based → you leave money on the table or drive customers to share logins.
- **Silent packaging drift.** Moving features between tiers without changelog or communication → trust erosion.
- **Pricing as a growth hack.** One-off promos that anchor customers low forever.
- **Migration ambush.** Announcing the change 30 days before renewal.

## Seniority signals

- **Beginner:** understands current price architecture.
- **Intermediate:** contributes to packaging changes with support from PMM / Finance.
- **Advanced:** owns product-side pricing proposals for an area; runs migration confidently.
- **Expert:** uses pricing & packaging as strategic levers for adoption, retention, and margin across multiple products.

## Files

`.ai/memory/projects/<slug>/pricing/<change>.md`. Link current pricing page, competitor pricing pages, and related decision memo. Keep a version log — pricing changes compound.
