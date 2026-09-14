# Connector task recipes — closing a PM to-do through MCP with links back to the source

## What it is

Three worked recipes for finishing a routine PM task end to end through MCP connectors instead of asking someone for an export: a launch retro from tickets, a feature-adoption check from product analytics, and a behaviour-split retention question. Each recipe fixes the question, the tools by suffix name, the discovery step before the query, the query shape, the output with its source links, where the result is persisted, and which claims stay TBD. The tool prefix (`mcp__<server>__`) varies by environment; the suffix names below are stable.

## Why it matters

A connector answers in seconds and forgets in seconds. The number lands in chat, the query is gone, and a week later nobody can say where "11%" came from. Product analytics already states the rule: MCP calls are ephemeral, decisions must be durable (`pm-phase-deliver/references/product-analytics.md`, "Using MCP for PostHog"). A recipe makes the durable part automatic: numerator, denominator, window, link and query text travel with the number. When a recipe repeats across weeks, lock it in as a skill or a reference; a routine that lives in one PM's head is not a workflow.

## The recipe contract

```markdown
# Recipe — <task>

- **Question**: <one sentence, with the decision it feeds>
- **Tools**: <suffix names; the prefix varies by environment>
- **Discovery step**: <schema or field check before the query>
- **Query shape**: <the query, kept verbatim in the output>
- **Output**: <numerator / denominator / window, with its time zone / source link>
- **Completeness**: <the result paged to the end; the tool's total against the rows fetched>
- **Unit and deduplication**: <account, user or event; the key rows are deduplicated on>
- **Time zone**: <the zone the window is evaluated in; the tool's default against the reporting zone>
- **Durability**: <file under the project's memory, query text included>
- **Inference checks**: <what the tools did not return and therefore stays TBD>
```

## Recipe 1 — Launch retro from tickets

- **Question**: what did the launch cost support in its first four weeks, by category, and which issues are still open? Feeds the close-out memo in `pm-phase-deliver/references/post-launch-monitoring.md`.
- **Tools**: `searchJiraIssuesUsingJql`, `getJiraIssue` ("Using MCP for Jira" in `pm-transversal-docs/references/jira-linking-automation.md`).
- **Discovery step**: confirm the project key, the label or component the launch uses, and the resolution values in play; a missing label is unknown, not zero.
- **Query shape**: JQL by project, created window (launch date to launch date plus four weeks), label or component, grouped by category and resolution.
- **Output**: counts per category with the issue keys as links; open versus resolved; the two oldest open issues by key.
- **Completeness, unit, time zone**: page the JQL result to the end and report the tool's total against the issues fetched; the unit is the issue, deduplicated on its key (a ticket linked twice is one ticket); the created window is evaluated in the Jira instance's time zone, which is stated next to the dates.
- **Durability**: `launches/<name>.md` or `retrospective.md`, with the JQL text.
- **Inference checks**: closed is not resolved; a ticket without the label may still belong to the launch; volume says nothing about severity.

## Recipe 2 — Feature adoption

- **Question**: what share of active accounts used the feature in the window, and is the trend early-adoption growth or stickiness? Feeds the ship / iterate / rollback decision.
- **Tools**: `event-definitions-list` and `properties-list` for discovery; `query-run` or `insight-query` for the number ("Discovery before query" in `data-science-analyst/references/posthog-mcp-patterns.md`).
- **Discovery step**: the exact event name, the property that identifies the account, and the definition of an active account in the window.
- **Query shape**: distinct accounts firing the event over active accounts in the window, plus the weekly count for the trend.
- **Output**: N of M accounts (share), window, weekly series, the insight link.
- **Completeness, unit, time zone**: the unit is the account, not the user or the event, deduplicated on the account identifier the event carries; the 28-day window is evaluated in the analytics tool's reporting time zone, stated with the number; when the tool pages results, walk every page before the count is quoted.
- **Durability**: `analytics/<topic>-<date>.md` with the query text and the definition of active account used.
- **Inference checks**: adoption is not retention; a rising weekly count inside the first month is novelty until proven otherwise ("Feature adoption" in `pm-phase-deliver/references/product-analytics.md`); nothing was learnt about accounts that tried once and left.

## Recipe 3 — Behaviour-split retention

- **Question**: do accounts that did X in week one retain better at 30 days than accounts that did not? Feeds a hypothesis for `pm-archetype-growth`, not a launch claim.
- **Tools**: `query-run` with a cohort definition; `insight-query` for the retention curve.
- **Discovery step**: the event that defines X, the account identifier, and whether the analytics tool already exposes a retention insight.
- **Query shape**: two cohorts by whether X happened in the observation window (days 0 to 7 from signup), a window that closes before the retention window opens; 30-day retention per cohort, measured only for accounts whose observation window closed before the query date; cohort sizes. The unit is the account, deduplicated on the account identifier.
- **Output**: retention per cohort with cohort sizes and a confidence interval where the tool gives one; the insight link.
- **Completeness, unit, time zone**: both cohorts drawn from the same complete account list, paged to the end; the account is the unit; observation and retention windows evaluated in one stated time zone, since a day boundary moves accounts between windows.
- **Durability**: `analytics/<topic>-<date>.md` with the query text.
- **Inference checks**: correlation is not cause, and accounts that did X may differ in every other way (the causal discipline in `pm-phase-deliver/references/metric-quality-guardrails.md`); survivorship, because accounts that churned in week one never had the chance to do X; and leakage, because a cohort defined with anything observed inside the retention window compares survivors with themselves.

## When not to run a recipe

- No connector: ask for an export and hand the file to `data-science-analyst`; do not guess the number.
- The claim would influence a sale, a quote or a contract: it stays TBD with the owner who can confirm, per the variant-status rule in `inference-discipline/SKILL.md`.
- Discover stage with no KPI defined yet: a number without a decision to feed is decoration.
- The deliverable is a dashboard: that is `pm-phase-deliver/references/product-analytics.md`, not a recipe.

## Common anti-patterns

- **Stating a number no tool returned.** The most common one, usually under pressure from a stakeholder who already has the number in mind.
- **Ephemeral result without the query.** A share with no way to reproduce it.
- **Percentage without denominator or window.** "11%" of what, when.
- **Adoption read as retention.** Use is not habit.
- **Query before discovery.** Guessing an event name and reporting whatever came back.
- **No link back.** A claim the reader cannot check in one click.

## Files

Connector results → `.ai/memory/projects/<slug>/analytics/<topic>-<date>.md` with the query text. Launch retros → `launches/<name>.md`. Decisions the number changed → `decisions.md`.
