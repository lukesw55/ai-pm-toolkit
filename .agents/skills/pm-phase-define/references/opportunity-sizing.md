# Opportunity sizing and demand modelling

## What it is

Estimating the **scale, quality, and accessibility** of an opportunity through segment × behaviour × economics models. Blend top-down (TAM/SAM/SOM) with bottoms-up (users × behaviour × unit economics) and stress-test the load-bearing assumptions.

## Why it matters

Expert PMs compare opportunities using more than intuition. Without a defensible sizing, prioritisation is vibes and business cases are fiction.

## Ready-to-use template — opportunity sizing memo

```markdown
# Opportunity sizing — [opportunity name] — [date]

## TL;DR
One paragraph: the size, the confidence, and the recommendation.

## Opportunity statement
Who has what problem, what would change for them, and why solving it creates value.
(Link to discovery problem brief.)

## Top-down view (TAM / SAM / SOM)
| View | Definition | Estimate | Source |
|---|---|---|---|
| TAM — Total Addressable Market | everyone who could theoretically buy | e.g. $X | analyst / public data |
| SAM — Serviceable Addressable Market | those we could reach with current GTM | $Y | our ICP + channel reach |
| SOM — Serviceable Obtainable Market | realistically capturable in [horizon] | $Z | our share + growth rate |

## Bottoms-up view (preferred for product decisions)
Model the opportunity as: **users × behaviour × unit economics × time**.

| Driver | Value | Source / assumption |
|---|---|---|
| Target segment size | [N users] | [query / survey / analyst] |
| Penetration assumption | [X%] | [benchmark / prior experiment] |
| Activation rate | [Y%] | [our data or benchmark] |
| Frequency / month | [Z sessions] | [our data] |
| Value per event | [$V or time saved] | [pricing / willingness-to-pay] |
| Retention factor (year 1) | [R%] | [cohort data] |
| **Estimated annual value** | = N × X × Y × Z × V × R | |

## Scenarios
| Scenario | Key assumption change | Result |
|---|---|---|
| Base | defaults above | $... |
| Upside | penetration +50%, retention +10pp | $... |
| Downside | penetration -50%, retention -10pp | $... |

## Load-bearing assumptions (top 3)
Assumptions whose change most moves the answer. For each:
- [assumption] — current value — if it were X, answer changes by Y%
- ...

## Sensitivity
Brief sensitivity analysis on the top 3 assumptions (±30% each).

## Reachability constraints
- acquisition channels + cost
- onboarding friction
- pricing / packaging constraints
- technical / integration constraints
- timeline to first revenue

## Comparison vs alternatives
Rank this opportunity vs at least 2 others the team could fund instead.

## Confidence + recommendation
Confidence: [low / med / high] because [reason].
Recommendation: fund / don't fund / fund a smaller learning step.

## Appendix
Model spreadsheet / notebook link. Raw data sources.
```

## How to pick assumptions honestly

- **Start with our data.** If we have a behavioural benchmark from a similar feature or segment, use it with a named sample size.
- **Use external benchmarks critically.** Industry "average conversion rate 2.5%" is usually median of a wide distribution. Don't treat as baseline.
- **Two anchors, not one.** For every load-bearing assumption, have a lower and an upper bound — single-point estimates hide uncertainty.
- **Name what you cannot know.** "Willingness to pay for this exact bundle is unknown; proxy = existing add-on pricing" is honest. "WTP = $15/mo" is false precision.

## Common anti-patterns

- **TAM theatre.** "$X billion market" with no reachability analysis. Every SaaS pitch deck does this.
- **False precision.** "Revenue will be $4,237,891 in year 1." No.
- **One heroic adoption curve.** S-curve assumption applied to a segment that has no evidence of fast adoption.
- **Ignoring acquisition constraints.** You cannot capture the market if you can't reach it at a sustainable CAC.
- **No comparison.** Sizing an opportunity alone, not against alternatives that share the same resource pool.
- **Assumptions unflagged.** Burying an assumption as if it were data.

## When sizing is enough vs when it isn't

- **Good enough:** prioritising within a known product area where signals are familiar. Quick bottoms-up + scenarios.
- **Needs more rigor:** new market entry, major investment (>1 quarter of team capacity), public commitment, M&A rationale, pricing redesign. Pair with a finance partner.

## Seniority signals

- **Beginner:** uses rough top-down numbers.
- **Intermediate:** produces a basic, defensible estimate.
- **Advanced:** blends market, usage, and channel assumptions realistically; sensitivity analysis.
- **Expert:** creates decision-grade models that improve portfolio sequencing.

## Files

`.ai/memory/projects/<slug>/sizing/<opportunity>.md`. Keep model (spreadsheet or notebook) linked, not embedded.
