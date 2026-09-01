# Jira ticket hygiene

## What it is

Ticket structure that **survives refinement** and lets engineers start work without re-asking basics. Covers the anatomy of each ticket type (story, task, epic, bug, spike), the fields that matter, and the "Definition of Ready" checklist.

## Why it matters

The cost of a bad ticket is paid on sprint-day-one, every sprint, every sprint. Small up-front investment compounds.

## Ticket types — when to use which

| Type | Purpose | Size | Owner |
|---|---|---|---|
| **Epic** | a coherent bet delivered over multiple sprints | multi-sprint | PM |
| **Story** | one vertical slice of user-observable value | fits in 1 sprint | PM + Eng |
| **Task** | implementation step under a story | hours-to-days | Eng |
| **Bug** | defect or regression | varies | Eng |
| **Spike** | timeboxed investigation to de-risk a story | hours-to-days | Eng (with PM input on scope) |
| **Chore / Tech-debt** | non-user-facing work (refactor, upgrade, ops) | varies | Eng-led |

Don't use "Task" for what's actually a story — you lose the user-value framing.

## Ready-to-use template — Story

```markdown
## Title
[User outcome, imperative — e.g. "Allow users to export dashboard data as CSV"]

## User value
As a [segment user], I want to [do X], so that [outcome / reason].

## Acceptance criteria
- [ ] Given [context], when [action], then [observable result]
- [ ] Given [edge case], when [action], then [expected result]
- [ ] Given [error state], when [action], then [error handling]

## Scope IN
- [what this story covers]

## Scope OUT
- [explicitly not covered — deferred or belongs elsewhere]

## Design
[link to Figma / mockup]

## Tracking events
- [event_name] — fires on [trigger] — properties: [list]

## Non-functional requirements
- latency: [target]
- a11y: [WCAG level + specific checks]
- mobile / responsive: [yes/no]
- internationalisation: [yes/no]

## Links
- PRD: [link]
- Parent epic: [link]
- Design file: [link]
- Tracking plan: [link]
- Blocks / is blocked by: [tickets]

## Labels
- area/[name]
- priority/[level]
- stage/[discovery-phase-slug if applicable]

## Components
- [relevant component tags]

## Estimate
- [story points or t-shirt size]

## Definition of Done
- [ ] code merged + deployed behind feature flag
- [ ] unit tests green
- [ ] integration tests (if applicable) green
- [ ] instrumentation live + verified in staging
- [ ] design review passed
- [ ] a11y check passed (for UI)
- [ ] support briefed (if user-facing material change)
- [ ] docs / release-notes drafted (if applicable)
- [ ] PRD ↔ ticket links bidirectional
```

## Ready-to-use template — Epic

```markdown
## Title
[Bet name — maps to a One Pager / PRD]

## Bet
If we [ship this], [segment] will [behaviour change], moving [metric] from [X] to [Y].

## Primary metric
[link to KPI tree]

## Stories (as they're refined, they become child tickets)
- [ ] Story 1 — [user outcome]
- [ ] Story 2
- [ ] Story 3
- ...

## Non-goals
[what the epic explicitly does NOT include]

## Links
- PRD: [link]
- One Pager: [link]
- RAID: [link]
- Launch plan (when created): [link]

## Labels + components

## Target window
[quarter / sprint range]

## Owner
- PM: @name
- Tech Lead: @name
```

## Ready-to-use template — Bug

```markdown
## Title
[Symptom as user would describe it — e.g. "Dashboard fails to load after 30 min of inactivity"]

## Steps to reproduce
1. ...
2. ...
3. ...

## Expected behaviour
[what should happen]

## Actual behaviour
[what happens]

## Environment
- browser / OS / app version:
- user account type (plan / role):
- timestamp + user ID (if reported):
- logs / screenshots:

## Impact
- who's affected (segment + scale):
- workaround (if any):
- severity (P0 / P1 / P2 / P3):

## Links
- customer ticket / report:
- related PRD / story (if regression):
```

## Ready-to-use template — Spike

```markdown
## Title
[Investigation objective — e.g. "Spike: evaluate feasibility of real-time sync for multi-user editing"]

## Purpose
What decision this spike unlocks.

## Questions to answer
- [ ] Q1
- [ ] Q2

## Timebox
[N days — hard limit]

## Out of scope
- no production code
- no permanent infrastructure changes

## Deliverables
- written findings in [doc]
- recommendation for next step
- follow-up ticket(s) if any

## Owner
@eng
```

## Ready-to-use template — Chore / Tech-debt

```markdown
## Title
[Specific refactor / upgrade / ops task]

## Rationale
Why this matters — cost of not doing it.

## Scope
- IN:
- OUT:

## Acceptance
- [ ] observable outcome (tests pass, build faster, X deprecated)

## Risk + rollback plan

## Links
```

## Field discipline

Fields that should be consistently filled:

- **Title** — imperative, user-outcome for stories, specific for other types
- **Description** — template above
- **Acceptance criteria** — bullet list, testable
- **Labels** — consistent set (area, priority, stage, flag-gated, etc.)
- **Components** — accurate (drives downstream filtering)
- **Estimate** — even if rough; absence of estimate = absence of commitment
- **Sprint** — assigned only when truly ready
- **Links** — blocks / is blocked by / relates to / part of epic

## Definition of Ready (for sprint planning)

A story enters sprint planning only when:

- [ ] user value is stated
- [ ] acceptance criteria are clear and testable
- [ ] scope IN/OUT is explicit
- [ ] dependencies are identified and on-track
- [ ] design is final (or explicitly deferred to implementation with PM buy-in)
- [ ] NFRs listed (latency, a11y, etc.)
- [ ] tracking events agreed
- [ ] ticket links bidirectional (PRD, design)
- [ ] estimate assigned
- [ ] someone on the team has read it and asked questions

Stories that fail Ready enter refinement, not planning.

## Common anti-patterns

- **Tickets without acceptance criteria.** "Build the feature" → endless re-clarification mid-sprint.
- **Giant "stories" disguised as stories.** A 3-week story is an epic in disguise; slice it.
- **Implementation-detail titles.** "Add useEffect hook to Dashboard.tsx" is a task, not a story title.
- **No links.** PRD somewhere, ticket somewhere else, design in a third place; nothing connects.
- **Inconsistent labels.** `area/payments`, `Payments`, `PMT`, `billing` — same area, 4 labels. Grepping fails.
- **Estimate-less.** "We'll see how it goes." → no predictability.
- **Stale tickets in sprints.** Tickets hanging over sprint to sprint because they weren't Ready on day 1.
- **Description-free tickets.** Title only. Context missing.
- **Ticket as chat log.** 40 comments; ticket body outdated. Update the body.

## Refinement cadence

- **Weekly refinement session** (~1h) — PM + Tech Lead + 1-2 engs refine top-of-backlog stories toward Ready.
- **Async nudges** — PM drops refinement questions in Slack/Jira; non-blocking for eng.
- **Pre-sprint-planning check** — PM verifies top 5-7 stories are Ready on Friday before Monday's planning.

## Using Jira via MCP

If MCP Atlassian is available (tool names below are the `<tool>` suffix of `mcp__<server>__<tool>` — the server prefix varies by environment):

- `createJiraIssue` — create with the template
- `editJiraIssue` — update fields
- `getJiraIssue` — fetch
- `searchJiraIssuesUsingJql` — run saved queries
- `transitionJiraIssue` — move through workflow (to "In progress", "Done", etc.)

See `jira-linking-automation.md` for linking patterns and automations.

## Files

Ticket templates live in `.ai/memory/_templates/` if you want a local markdown version before pasting into Jira. Or directly in Jira issue templates if your admin supports it.
