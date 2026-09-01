# Business case and PRFAQ

## What it is

Translating a product initiative into expected **costs, benefits, risks, operating implications, and return logic** suitable for investment decisions. Two complementary artefact forms:

- **Business case / investment memo** — financial-first, cost & benefit driven
- **PRFAQ** — "press release + FAQ" — customer-outcome-first, works backwards from the press release the launch would deserve

Use PRFAQ when the decision needs executive alignment on the *outcome*. Use business case when the decision needs justification on the *economics*. Large bets get both.

## Why it matters

Senior PMs increasingly need to justify material bets, not just explain features. A business case / PRFAQ translates judgement into an auditable, comparable artefact.

## PRFAQ — ready-to-use template

```markdown
# PRFAQ — [initiative name] — [date]

## Press release (written as if the launch already happened)

### Headline
[Customer + benefit + category] — e.g. "Acme launches Remote Fleet Update, cutting device OTA rollouts from days to hours for embedded-systems teams."

### Subheadline
One sentence — benefit + who benefits.

### Lead paragraph
City, date — [Company] announced [product/feature] that [core benefit]. [Target customer] can now [concrete new capability]. [Why it matters / what it replaces].

### Customer problem
The specific pain that used to exist. Vivid. Concrete. Quote a (hypothetical) customer if helpful.

### Solution description
How the product solves it. One or two paragraphs. No internal jargon.

### Customer quote (hypothetical, realistic)
"[Quote that a real customer would say] — [Name], [Role], [Company]"

### Getting started / availability
How customers access it. Pricing if relevant.

## FAQ

### Customer-facing Qs
- What is it?
- Who is it for?
- How is it different from [competitor / alternative / doing nothing]?
- How much does it cost?
- When is it available?
- What are the limitations?

### Internal Qs (for leadership)
- Why now?
- What's the business case (size, cost, return, risk)?
- What is NOT included?
- What are the biggest risks, and how are we mitigating?
- What would kill this initiative?
- How will we measure success 3 / 6 / 12 months in?
- Staging: what's phase 1, 2, 3 and what does each phase prove?
- What do we need from each team (eng, design, PMM, sales, support, legal)?
```

## Business case / investment memo — ready-to-use template

```markdown
# Business case — [initiative] — [date]

## TL;DR
Recommendation + investment ask + expected return.

## Context
What's prompting the investment now. Link to strategy memo.

## Opportunity
Link to sizing memo. Summary: size, confidence, segment.

## Proposed approach
What we'd build / change, at which scope. Link to PRD outline.

## Costs
| Cost category | Year 1 | Year 2 | Notes |
|---|---|---|---|
| Eng headcount | $X | $X | [N FTE at fully-loaded cost] |
| Design + PM + Analytics | $X | $X | ... |
| Infra / cloud | $X | $X | ... |
| GTM enablement | $X | $X | ... |
| Support ramp | $X | $X | ongoing |
| One-time migration | $X | — | ... |
| **Total** | **$X** | **$X** | |

## Expected benefits
| Benefit | Year 1 | Year 2 | Mechanism |
|---|---|---|---|
| New revenue | $X | $X | [from sizing model] |
| Retention / margin impact | $X | $X | [reduced churn] |
| Cost avoidance | $X | $X | [e.g. deprecation of legacy] |
| **Total** | **$X** | **$X** | |

## Net + return logic
- Net year 1: $X
- Payback: N months
- NPV [horizon, discount rate]: $X
- IRR: %

## Baseline + counterfactual
- baseline: what happens if we do nothing (be specific — often revenue still grows on its own)
- counterfactual: value of the best alternative use of the same resources

## Staged investment plan
Gate the investment. Don't commit the full amount upfront.

- **Phase 1 (Spend $X to learn Y)** — discovery + prototype + concept test. Decision gate: [criterion].
- **Phase 2 ($X to build limited MVP)** — gated cohort. Decision gate: [metric threshold].
- **Phase 3 ($X to scale)** — full rollout. Decision gate: [guardrails hold + primary metric on track].

## Risks + mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ... | ... | ... | ... |

## Assumptions (load-bearing)
Top 3 with invalidation conditions.

## Recommendation
Fund / don't fund / fund phase 1 only.
```

## Rules for honest numbers

- **Baseline matters.** "Revenue +$X" means nothing without "vs doing nothing, which would have delivered $Y."
- **Fully-loaded cost.** Include benefits, overhead, infra, support ramp — not just salary.
- **Ongoing cost counts.** A feature that needs 2 engineers to maintain forever has a real cost.
- **Migration cost counts.** Telling customers to change behaviour has a cost (support tickets, churn risk).
- **Confidence bands.** If you can't produce lower/upper bounds, your model is a guess.

## PRFAQ vs business case — when to use which

| Situation | PRFAQ | Business case | Both |
|---|---|---|---|
| New product launch | ✓ | optional | ideal |
| Feature in existing product | maybe | ✓ | |
| Pricing change | — | ✓ | |
| Major UX overhaul | ✓ | ✓ | ✓ |
| Platform / infra investment | — | ✓ | |
| Market entry | ✓ | ✓ | ✓ |
| Deprecation | — | ✓ | |
| Acquisition rationale | ✓ | ✓ | ✓ |

## Common anti-patterns

- **Upside as certainty.** Using the best-case number as "expected return".
- **Ignoring ops cost.** The feature shipped, then ongoing support ate 30% of an engineer for 2 years.
- **No baseline.** Growth would have happened anyway; claiming credit for it.
- **Single-point estimate.** No confidence band, no scenarios.
- **Migration invisible.** "Customers will just adopt it" — they won't, and the migration costs real money.
- **PRFAQ as marketing fiction.** Press release that makes claims the product can't meet.

## Files

`.ai/memory/projects/<slug>/business-cases/<initiative>.md` and/or `.ai/memory/projects/<slug>/prfaqs/<initiative>.md`. Link to sizing model + strategy memo.
