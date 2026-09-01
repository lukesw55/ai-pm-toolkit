# Quantitative analysis

## What it is

Interpreting behavioural data (funnels, retention, cohorts, segmentation) and structuring queries that answer product questions. The **quant** half of triangulation — complements qualitative synthesis.

## Why it matters

Numbers without interpretation are trivia. Interpretation without numbers is opinion. PMs who can run or direct meaningful quant analysis turn dashboards into decisions.

## The analysis workflow

1. **Define the question.** "Are new users activating?" is a real question; "look at the data" is not.
2. **Define the metric.** Formula, cohort, window. No ambiguity.
3. **Pick the right analysis type** (funnel / retention / cohort / segment / path). See `pm-phase-deliver/references/product-analytics.md`.
4. **Check data quality first.** Before drawing conclusions, verify definitions haven't drifted, cohorts aren't biased, instrumentation is live.
5. **Look for segments.** The average hides heterogeneity.
6. **Write interpretation alongside numbers.** Never just a number.
7. **Triangulate with quali.** Quant says *what*; quali explains *why*.
8. **State confidence.** Low / medium / high, with reasons.

## Using PostHog (product analytics)

When PostHog MCP tools are available, useful entry points:

- `mcp__claude_ai_PostHog__query-run` — run a HogQL query (see `posthog:query` skill and `posthog:query-examples` for patterns)
- `mcp__claude_ai_PostHog__insight-query` — pre-built insight types
- `mcp__claude_ai_PostHog__insights-list` / `insight-get` — browse existing insights
- `mcp__claude_ai_PostHog__dashboards-get-all` — see existing dashboards
- `mcp__claude_ai_PostHog__event-definitions-list` — verify events before writing queries
- `mcp__claude_ai_PostHog__properties-list` — check available properties

Always verify event/property definitions before querying. A query with a bad property name returns 0 silently.

## HogQL patterns (ready to adapt)

### Activation funnel
```sql
SELECT
  count(DISTINCT if(event = 'signup_completed', person_id, null)) AS signups,
  count(DISTINCT if(event = 'project_created' AND timestamp < signup_ts + INTERVAL 24 HOUR, person_id, null)) AS activated
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
  AND person.properties.plan IN ('free', 'pro')
```

### Retention cohort
```sql
WITH cohort AS (
  SELECT person_id, min(timestamp) AS first_seen
  FROM events
  WHERE event = 'signup_completed'
    AND timestamp >= now() - INTERVAL 90 DAY
  GROUP BY person_id
)
SELECT
  toStartOfWeek(first_seen) AS cohort_week,
  count(DISTINCT person_id) AS cohort_size,
  count(DISTINCT if(e.timestamp BETWEEN c.first_seen + INTERVAL 7 DAY AND c.first_seen + INTERVAL 14 DAY, e.person_id, null)) / count(DISTINCT c.person_id) AS week_2_retention
FROM cohort c
LEFT JOIN events e ON e.person_id = c.person_id
GROUP BY cohort_week
ORDER BY cohort_week
```

### Segment comparison
```sql
SELECT
  person.properties.plan AS plan,
  count(DISTINCT person_id) AS users,
  countIf(event = 'project_created') AS projects_created,
  avg(countIf(event = 'project_opened')) AS avg_opens_per_user
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY plan
```

More patterns: `posthog:query-examples` reference (available via the skill system).

## Ready-to-use template — Quant analysis memo

```markdown
# Quant analysis — [Question] — YYYY-MM-DD

**PM / analyst:** @name
**Tools used:** PostHog / warehouse / internal BI
**Links:** tracking plan / KPI tree / related PRD

## Question
[One sentence. Specific.]

## Method
- data source:
- date range:
- cohort / filter:
- metric formula:
- query saved: [link]

## Result (numbers)
| Metric | Value | Change vs baseline | Confidence (CI / sample size) |
|---|---|---|---|

## Segment breakdown
| Segment | Metric value | Note |
|---|---|---|

## Time trend
[chart link or verbal description — is this stable, rising, falling, seasonal?]

## Data-quality checks
- [ ] event definitions current (spot-checked in tracking plan)
- [ ] cohort size makes sense (matches expected user volume)
- [ ] no SRM / exclusion anomalies
- [ ] segment filters match definitions used elsewhere

## Interpretation
What this tells us, in plain English. 2-4 sentences.

## What it does NOT tell us
Explicit limitations. What you'd need to answer fully.

## Triangulation
- quali signal: [aligned / contradicts / unknown — link to synthesis if available]
- other quant sources: [dashboard X shows Y]

## Confidence
low / medium / high — and why.

## Implication
[decision impact — what should change, or what to investigate next]

## Next steps
- deeper analysis: [what]
- triangulation: [what quali to pull]
- experiment: [if this is a hypothesis worth testing]
```

## Statistical reasoning — the minimum bar for PMs

- **Practical vs statistical significance.** A 0.3% lift can be stat-sig with a huge sample — still not worth shipping. A 5% lift with N=200 might be noise. Pin both.
- **Confidence intervals > point estimates.** "12%" is a point; "10-14% (95% CI)" is decision-useful.
- **Baseline + counterfactual.** "X went up 10%" — vs what? vs before the launch? vs a control cohort? vs seasonal expectation?
- **Correlation ≠ causation.** Shipped X on day Y; metric Z moved day Y+1. Could be X, could be seasonality, could be another launch.
- **Segment before averaging.** Always.
- **Novelty effects.** Week 1 spike on new thing; settled by week 4. Measure beyond novelty window.
- **SRM checks.** Experiments/rollouts with unexpected ratio imbalances = something broken.

## SQL / HogQL sanity checks before trusting a number

- Does the number match the dashboard it's supposed to feed?
- Does the cohort size match expected user volume for the filter?
- Are test accounts / bots excluded consistently?
- Is the timezone what you think it is (UTC vs user-local)?
- Are "events per user" counted at the right level (session / day / period)?
- Are joins producing expected row counts (no explosion)?

Numbers that look surprising usually ARE surprising because something's wrong with the query, not because the user base changed overnight. Check first.

## Common anti-patterns

- **Confirmation analysis.** Querying until you find the cut that supports the hypothesis.
- **Single-point obsession.** No CI, no segments, no baseline, no counterfactual.
- **Correlation stories.** "Shipped X; metric moved; therefore X caused it."
- **Segment silence.** Reporting averages when one segment is collapsing.
- **Time-range cherry-picking.** Picking the window where the effect looks best.
- **Unverified cohort definitions.** Using inconsistent filters across related analyses.
- **Metric name collision.** "Active users" defined differently in three dashboards.
- **No interpretation.** Just tables and charts; no narrative.

## Seniority signals

- **Beginner:** reads dashboards correctly; asks analytics for specific cuts.
- **Intermediate:** runs HogQL / SQL for simple questions independently; validates assumptions.
- **Advanced:** designs analyses that expose hidden patterns; challenges interpretation bias; catches data-quality issues.
- **Expert:** shapes the analytical narrative for an area; raises team-wide quant standards.

## Integration

- Use alongside `qualitative-synthesis.md` + `triangulation.md` for full pictures.
- PRDs and experiment briefs cite specific analyses by link.
- Analyses with lasting decisions → persist to `.ai/memory/projects/<slug>/analyses/`.

## Files

`.ai/memory/projects/<slug>/analyses/<question>-<date>.md`. Query itself linked or embedded (+ link to saved query in analytics tool for reproducibility).
