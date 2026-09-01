# KPI architecture and metric-tree design

## What it is

A measurement system that links **customer value → product outcomes → business results** through a North Star metric and supporting input metrics, plus explicit guardrails.

## Why it matters

Without a coherent metric tree, teams chase vanity metrics or argue about what "success" means. A good tree lets anyone on the team trace "what I'm working on" to "what matters to the business".

## Anatomy

```
                       [Business outcome]
                              |
                      [North Star metric]
                         /    |    \
              [Input 1] [Input 2] [Input 3]
                /  \       |        |  \
            [lvl3] [lvl3] [lvl3] [lvl3] [lvl3]
```

Plus **guardrails** sitting to the side: metrics that must NOT degrade when North Star improves.

## North Star

The one metric the whole team rallies around. It should:

- **Reflect user value delivered** (not just company revenue)
- **Lead business outcomes** (improving it reliably improves the business)
- **Be actionable** (teams can directly move it)
- **Be measurable** (with known lag and confidence)

Classic examples:
- Airbnb: nights booked
- Spotify: time spent listening
- Slack: daily active users sending 2k+ messages
- Figma: monthly active editors

**Bad North Star candidates:** revenue (too lagging, too affected by pricing), DAU alone (doesn't reflect value), NPS (too noisy, too slow).

## Metric tree template

```markdown
# [Product area] KPI tree — [version / date]

## Business outcome
[e.g. annual recurring revenue]

## North Star metric
**Definition:** [plain English]
**Formula:** [precise math]
**Unit:** [what each point represents]
**Baseline:** [current value + date + sample]
**Target:** [value + horizon]
**Owner:** [@name]
**Cadence:** [weekly / monthly]

## Input metrics (level 2)
Each input answers "what do we do that moves the North Star?"

### Input 1: [name]
- definition + formula:
- baseline:
- target:
- owner:
- relationship to North Star (leading indicator? multiplicative? additive?):
- level-3 breakdown:
  - [finer-grained metric 1]
  - [finer-grained metric 2]

### Input 2: [name]
...

## Guardrails
Metrics that must NOT degrade when North Star improves. Each with:
- definition:
- current value:
- threshold (alarm if crosses):
- owner:

## Leading vs lagging classification
| Metric | Leading / Lagging | Lag (days) |
|---|---|---|
| ... | ... | ... |

## Review cadence
- weekly business review: [which metrics]
- monthly review: [which metrics]
- quarterly: [which metrics]

## Change log
When metric definitions change, record here. Metric definitions that drift silently destroy trust.
```

## Common shapes

**Activation → Retention → Expansion:**
```
Business outcome: net revenue retention
  North Star: monthly active paying users
    Input 1: signup → activated conversion
    Input 2: weekly retention (wk1, wk4, wk12)
    Input 3: expansion rate
```

**Engagement depth:**
```
Business outcome: revenue growth
  North Star: sessions per user per week
    Input 1: % users hitting habit threshold
    Input 2: average session depth
    Input 3: re-engagement from notifications
```

## Guardrail examples

- reliability (p95 latency, error rate, incident count)
- support load (tickets per 1k users, CSAT)
- trust (privacy-related escalations, security incidents)
- platform health (test coverage, deploy frequency, MTTR)

## Anti-patterns

- **Vanity North Star.** Signups. Page views. Anything that moves without value being delivered.
- **Revenue-only.** Business outcome ≠ North Star. Revenue is downstream.
- **Metric sprawl.** 40 metrics in the scorecard, 40 owners, 40 priorities = no priorities.
- **Mixing health and target.** A metric can be a target OR a guardrail, not both at once.
- **Silent definition drift.** Changing the formula mid-stream without a change log → nobody trusts the numbers.
- **No owners.** A metric without an owner is a metric nobody is accountable for.

## Validation — is the tree good?

- [ ] every team in the area can name the North Star without checking notes
- [ ] moving any input metric ≥ X% moves the North Star in a predictable direction
- [ ] guardrails have alarms, not just definitions
- [ ] the tree is < 3 layers deep (depth-4 is noise for most teams)
- [ ] a new team member can be taught the tree in 15 minutes
- [ ] operating reviews reference the tree; ad-hoc metrics are escalated to add to it

## Files

`.ai/memory/projects/<slug>/kpis.md` (main tree) + `metric-dictionary.md` (formulas + sources). Link from strategy memo and every PRD/experiment brief.
