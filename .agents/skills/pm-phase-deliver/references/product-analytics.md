# Product analytics and dashboard interpretation

## What it is

Using product analytics (funnels, retention, cohorts, segmentation, feature adoption) to **turn behavioural data into decisions** — not just dashboards.

## Why it matters

Analytics is a core input to prioritisation, validation, and post-launch iteration. PMs who only *consume* dashboards fall behind; PMs who can *interpret and challenge* dashboards sharpen priorities and catch problems early.

## Core analyses (and what they tell you)

### Funnel
Sequence of events with drop-off between steps.

- tells you: **where users get stuck**
- doesn't tell you: **why** (triangulate with quali)
- watch: step definitions (fire once per session? per user?), attribution window

### Retention
Proportion of users returning over time.

- tells you: **whether users found real value**
- types: day-N, week-N (weekly cohort retention), rolling retention
- watch: cohort definition, active-user definition

### Cohort analysis
Groups of users defined by shared start (signup week, feature-enabled date, plan).

- tells you: **how groups evolve differently**
- useful for: comparing onboarding changes, pricing changes, feature rollouts over time
- watch: cohort size consistency, seasonal effects

### Segmentation
Breakdown of a metric by user trait or behaviour.

- tells you: **the average hides what**
- essential for: spotting segment-specific harm or benefit
- watch: segment definition consistency, sample size per segment

### Feature adoption
Usage of a specific feature over time.

- tells you: **did people find it + is it sticky**
- watch: baseline usage before launch, novelty-effect decay

### Path analysis
Sequences of events users take.

- tells you: **what journeys users actually follow** (often not what you designed)
- useful for: finding unexpected patterns, dead-ends
- watch: tree explosion (group similar events to make it readable)

## Dashboard hierarchy

```
Executive (monthly)           → North Star + business outcomes + top bets
  ↓
Team weekly review            → KPI tree + area scorecards
  ↓
PM operational               → funnel/retention/cohort by area
  ↓
Feature-level (per PRD)     → launch scorecard + experiment readouts
```

Each layer should **cascade** — feature-level metrics feed area, area feeds team, team feeds exec. Mismatched definitions between layers = trust destroyed.

## Ready-to-use template — Weekly business review (WBR)

```markdown
# WBR — [Area] — week of [YYYY-MM-DD]

**Presenter:** @pm   **Distro:** team + leadership

## North Star + primary KPIs
| Metric | Baseline | Target | This wk | Prior wk | Trend |
|---|---|---|---|---|---|

## What changed + why
- [movement]: [likely cause — shipped X, seasonality, upstream change]
- [surprise]: [investigating; owner; by when]

## Launches in flight
- [launch]: status + early signals + next milestone

## Experiments live
- [experiment]: expected completion, interim signal

## Top 3 issues / risks
- [issue]: owner + mitigation + ETA

## Decisions sought this week
- [decision ask]

## Follow-ups from last WBR
- [item]: status
```

## Ready-to-use template — Funnel analysis

```markdown
# Funnel analysis — [flow] — [YYYY-MM-DD]

## Scope
- users: [cohort definition]
- window: [dates]
- attribution: [first-touch, last-touch, session-based]

## Funnel
| Step | Count | Conversion from previous | Drop-off |
|---|---|---|---|
| 1. [event] | 10,000 | — | — |
| 2. [event] | 6,200 | 62% | 3,800 |
| 3. [event] | 3,100 | 50% | 3,100 |
| 4. [event] | 2,400 | 77% | 700 |

## Where the drop is
Largest absolute drop: step [2 → 3] (3,800 users). Largest relative drop: step [2 → 3] (50%).

## Segment view
| Segment | Step 1 → 2 | 2 → 3 | 3 → 4 | End-to-end |
|---|---|---|---|---|
| Free | ... | ... | ... | ... |
| Pro | ... | ... | ... | ... |

## Qualitative signal (triangulation)
- support tickets around step [X]:
- session-replay observations:
- interview evidence:

## Interpretation
- why is the drop-off there?
- what change would most move the funnel?
- what would a test to verify look like?

## Recommended action
- [clear recommendation + owner + confidence]
```

## Ready-to-use template — Retention cohort report

```markdown
# Retention — [cohort type] — [YYYY-MM-DD]

## Cohort setup
- grouping: [e.g. weekly signup cohorts, last 12 weeks]
- active = [event definition]
- measurement windows: wk 1, wk 2, wk 4, wk 8, wk 12

## Retention curve (cohort × week)
| Cohort | wk 1 | wk 2 | wk 4 | wk 8 | wk 12 |
|---|---|---|---|---|---|
| [YYYY-MM-WW] | 100% | 62% | 48% | 40% | 35% |
| [YYYY-MM-WW] | 100% | 68% | 52% | 44% | - |
| ...

## What's changing (if anything)
- cohorts post-[date] shifted [higher / lower] at wk 4 by X pp
- plausible cause: [launch, pricing change, seasonality, cohort composition]

## Segment × cohort
Any segments where retention differs materially?

## Bets informed
- confirm/deny the activation bet
- find where retention decays fastest (target for intervention)

## Risks in interpretation
- cohort composition shifts (segment mix changing → apples-to-oranges)
- sample size in recent cohorts too small
- upstream change confounds

## Action
```

## Using MCP for PostHog (if available)

If a PostHog MCP server is available (tools named `mcp__<server>__<tool>`; the server prefix varies by environment), you can query and build analyses directly in conversation:

- `query-run` — run a HogQL query
- `insight-create` / `insight-query` — pre-built insights (funnel, retention, trends)
- `dashboards-get-all` — see existing dashboards
- `event-definitions-list` — verify tracking plan is honoured
- See `pm-transversal-analysis/references/quantitative-analysis.md` for query patterns

Use MCP to answer ad-hoc questions faster, but persist the interpretation + decision in `.ai/memory/` — MCP calls are ephemeral; decisions must be durable.

## Common anti-patterns

- **Dashboard worship.** Staring at metrics without asking "and so what?"
- **No segments.** Average looks fine; one segment is collapsing.
- **Correlation = causation.** Shipping X the day metric Y moved. Was it X? Or the weekend? Or another team's change?
- **Reporting outputs, not outcomes.** "We added 4 features this quarter" vs "retention moved from X to Y".
- **No baseline.** "We converted at 12%" — of what? Up from what?
- **Feature-click-worship.** "50k clicks on the new button!" — clicks ≠ value.
- **Unowned dashboards.** Nobody maintains; metrics drift; trust decays.
- **Multiple sources of truth.** Eng dashboard says X; analytics says Y; finance says Z. Pick one.
- **Over-granularity.** 9 dashboards for one team. Nobody reads any of them.

## Principles

1. **Every dashboard answers a question the team is asking.** If no one can name the question, archive the dashboard.
2. **Define before drawing.** Formulas, cohort definitions, segment criteria — all explicit.
3. **Segments by default.** "Overall" hides harm. Always show at least one meaningful cut.
4. **Narrative + numbers.** Numbers without interpretation = trivia. Interpretation without numbers = opinion.
5. **Cadence > stare.** A weekly review beats staring at a dashboard daily.

## Seniority signals

- **Beginner:** reads dashboards correctly.
- **Intermediate:** defines dashboards for a team area; interprets outputs.
- **Advanced:** uses segmentation and trend analysis to uncover new opportunities and challenge assumptions.
- **Expert:** builds a measurement narrative that shapes strategy and operating reviews.

## Files

Analyses with lasting implications → `.ai/memory/projects/<slug>/analytics/<topic>-<date>.md`. Dashboards live in analytics tool; documentation of what each shows + who owns it → `.ai/memory/projects/<slug>/dashboards-catalog.md`.
