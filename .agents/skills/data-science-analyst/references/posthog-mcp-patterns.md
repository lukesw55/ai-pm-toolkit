# PostHog MCP Patterns

When the analytical question lives in product data (events, persons, sessions, experiments, feature flags, warehouse), prefer the PostHog MCP over asking the user for a CSV export. Scope to your PostHog project; tool calls are scoped to it automatically — no need to switch.

This file is **complementary** to the canonical PostHog skills (`posthog:query-examples`, `posthog:exploring-autocapture-events`, `posthog:configuring-experiment-analytics`, etc.). Pull those for the deep mechanics; this file gives the analyst-flavoured recipes that map to the modes in `SKILL.md`.

## Discovery before query

Always discover before writing HogQL — schemas drift, names change, and PoE mode means person properties on events reflect ingest-time values. Don't guess columns.

| Need | Tool |
|---|---|
| What events exist? | `event-definitions-list` |
| What properties on event X? | `properties-list` (event_names: ["X"]) |
| Find an experiment / dashboard / cohort by fuzzy name | `entity-search` |
| Is the SDK healthy / are events arriving? | `sdk-doctor-get` |
| Is the warehouse data fresh? | `data-warehouse-data-health-issues-retrieve` |

Anti-pattern: writing a HogQL `SELECT properties.foo` without confirming `foo` exists on that event.

## Mode A — EDA on product data

Substitute for "analyse this CSV" when the data is in events/persons.

1. `event-definitions-list` — confirm the event exists, see volume.
2. `properties-list` for that event — list candidate breakdown dimensions.
3. `query-run` with HogQL: shape (count), distinct users, time range, distribution per property.
4. Document grain (event vs person), time window, exclusions.

```sql
-- Profile shape of an event
SELECT
  count() AS events,
  count(DISTINCT person_id) AS persons,
  min(timestamp) AS first_seen,
  max(timestamp) AS last_seen
FROM events
WHERE event = 'device_provisioned'
  AND timestamp >= now() - INTERVAL 90 DAY
```

Person-on-events caveat: when slicing by `person.properties.X`, values reflect what was set at ingest time, not the person's current value — same person can carry different values on different events. State this explicitly in the report.

## Mode C — SQL / metric definition (cohort, funnel, retention)

Use `posthog:query-examples` for the canonical HogQL patterns. The analyst contract is the same as in `references/sql-patterns.md`:

1. Write the metric definition in plain language first.
2. State grain, filters, edge cases.
3. Build the query with named CTEs.
4. Add a validation query (row counts at each step, duplicate-key check).
5. State timezone (confirm your PostHog project's timezone).

For cohorts that other dashboards/insights will reuse, persist them via `cohorts-create` so the team doesn't re-derive the same logic.

## Mode D — Experiment analysis

When the user hands over an experiment name or asks "did the A/B work?":

1. `entity-search` or `experiment-list` to resolve to an experiment id.
2. `experiment-get` — confirm hypothesis, primary metric, variants, dates, status.
3. `experiment-stats` and `experiment-results-get` — pull the engine's stats (effect, CI).
4. Cross-check against your own HogQL count to validate exposure logic — engines occasionally surprise.
5. SRM check: assignment counts per variant via `query-run` against `$feature_flag_called`.
6. Report: effect size + CI + practical significance + SRM status + caveats.

If the user wants to *interpret* results for product action ("should we ship?"), chain to `pm-phase-deliver` (post-launch + experiment interpretation) and `pm-transversal-analysis` (triangulation).

## Mode G — Code review for data work in PostHog land

When reviewing how a service emits events for product analytics:

- Are event names stable and documented? (`event-definitions-list` shows what's actually arriving)
- Are property names consistent across emit sites? (`properties-list` per event)
- Is the SDK version healthy? (`sdk-doctor-get`)
- Are warehouse syncs degraded? (`data-warehouse-data-health-issues-retrieve`)
- Are feature flags or experiments tied to events the user will rely on? (`feature-flag-get-all`)

For PR-level review of the emit code itself, chain to a code-review pass (Scala/Go/TS lens) and `pm-phase-develop` (instrumentation/tracking-plan lens).

## When NOT to use the PostHog MCP

- The data is exclusively in customer-internal sources (CRM, billing, Power BI export staged on OneDrive). A churn-analysis project may be this — the Power BI export is the source of truth, not PostHog. Use file-level patterns (`scripts/profile_dataset.py`, `references/python-patterns.md`).
- The user is in **Discover** stage and the question is "what's broken?" before any KPI is defined. Premature instrumentation queries belong to Define/Develop.
- The deliverable is a new dashboard. Build the metric here; hand off the dashboard work to BI/PostHog UI.

## Linking out

- `posthog:query-examples` — full HogQL syntax + canonical patterns (trends, funnels, retention, paths, lifecycle, stickiness, web analytics).
- `posthog:exploring-autocapture-events` — selectors, actions, click-tracking analysis.
- `posthog:configuring-experiment-analytics` — exposure criteria + metric setup before reading results.
- `posthog:diagnosing-failed-warehouse-syncs` — when warehouse data is the upstream problem.
- `posthog:auditing-experiments-flags` — hygiene pass on experiments / flags.
- `posthog:diagnosing-sdk-health` — when events are not arriving.
