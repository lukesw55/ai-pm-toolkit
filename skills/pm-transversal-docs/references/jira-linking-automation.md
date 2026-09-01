# Jira linking + automation

## What it is

Cross-ticket linking (blocks / is blocked by / relates to / duplicates), parent-child hierarchies, automations worth having, and how to keep Confluence ↔ Jira bidirectional links alive.

## Why it matters

A backlog without links is a pile. A backlog with good links is a navigable graph that survives reorgs, PM handoffs, and six months later questions.

## Linking types — when to use which

| Link type | Meaning | Example |
|---|---|---|
| **is blocked by / blocks** | hard dependency — cannot proceed without | Story A is blocked by Story B (API done first) |
| **relates to** | soft dependency or related topic | two stories improving same flow |
| **duplicates / is duplicated by** | same problem | two bug reports same root cause |
| **parent / child** (epic → story) | hierarchy | story belongs to epic |
| **is caused by** | bug traces to a specific change | regression linked to change ticket |
| **is cloned from** | structured copy | repeated task (launch sequence) |

**Rule:** use "blocks/is blocked by" sparingly — only for HARD dependencies. Over-use erodes trust and makes every story look blocked.

## Linking hierarchy — the desired graph

```
[One Pager / Confluence] ←→ [Epic / Jira]
                                |
                    [Story] ← child of Epic
                       |
                       ├─ [Task] ← child of Story
                       ├─ [Task]
                       ├─ [blocks: Story] (cross-team dep)
                       ├─ [is blocked by: Story]
                       └─ [relates to: Story]

[PRD / Confluence] ←→ [Epic / Jira]
                       |
                [Design / Figma] ←→ [Story]
                       |
                [Tracking plan / Confluence] ←→ [Story] (event-by-event)
                       |
                [Release notes / Confluence] ←→ [Epic] (after ship)
```

Every artefact has a two-way link with its counterpart. No orphans.

## Epic ↔ Story discipline

- every story has a parent epic (chores/tech-debt can be under a "Tech health" epic)
- epics have clear boundaries — when they're done, they're closed
- don't have 30 stories under one epic — if you do, the epic is actually multiple epics

## Bidirectional Confluence ↔ Jira

- every Confluence PRD has a "Jira epic:" link in the front-matter
- every Jira epic has a "PRD:" link in the description
- when either changes (PRD amends scope; epic scope changes), update both
- Jira macros in Confluence can render live ticket status — use them for dashboards, not for source-of-truth

## Useful automations (if your Jira admin supports automations)

1. **Auto-transition stories to "In Progress"** when someone creates a branch named `<TICKET-ID>/...` or opens a PR linked to the ticket.
2. **Auto-transition epics to "Done"** when all child stories are Done.
3. **Notify PM** when a story transitions to "Ready for PM review" or "Blocked".
4. **Flag stale tickets** — if a ticket in "In Progress" has no update in 5 days, add label `stale/needs-update`.
5. **Link parent automatically** — when stories are created via template, pre-fill parent epic.
6. **Auto-label** based on component or assignee's team.
7. **Post to Slack** when a P0/P1 bug is opened in a watched component.
8. **Deadline escalation** — when a ticket's due date is 3 days away and not Done, notify the PM + assignee.

Avoid over-automating transitions that remove human judgement (e.g., auto-closing tickets; auto-assigning without context).

## JQL patterns worth saving

```sql
-- Epics in flight in my area
project = "AREA" AND issuetype = Epic AND status in ("In progress", "In review")

-- Stories ready to plan
project = "AREA" AND issuetype = Story AND status = "Ready" AND "Story Points" is not EMPTY
ORDER BY priority DESC, Rank ASC

-- Stale in-progress stories
project = "AREA" AND status = "In progress" AND updated < -5d

-- Bugs by severity in last 30 days
project = "AREA" AND issuetype = Bug AND created > -30d ORDER BY priority DESC

-- Stories blocking others
project = "AREA" AND issueFunction in hasLinks("blocks")

-- Stories attached to the current sprint
project = "AREA" AND sprint in openSprints() ORDER BY Rank ASC
```

Save named filters for the ones you use weekly. Dashboard widgets beat re-typing queries.

## Using MCP for Jira

If MCP Atlassian is available (tool names below are the `<tool>` suffix of `mcp__<server>__<tool>` — the server prefix varies by environment):

```
searchJiraIssuesUsingJql
  with: jql = "your JQL query"
```

Create issues:
```
createJiraIssue
  with: projectKey, issuetype, summary, description, fields (links, labels, components, parent)
```

Link issues:
```
createIssueLink
  with: inwardIssueKey, outwardIssueKey, linkTypeName (e.g. "Blocks")
```

Transition:
```
transitionJiraIssue
  with: issueKey, transitionId (check via getTransitionsForJiraIssue first)
```

## Epic close-out discipline

When an epic is ready to close:

- [ ] all child stories are Done (or explicitly descoped)
- [ ] launch-plan Confluence page linked + status = GA or equivalent
- [ ] close-out memo linked
- [ ] lessons learned captured
- [ ] PRD status updated to "Shipped" or "Archived"
- [ ] release notes published

Only then: transition epic to Done.

## Component + label strategy

- **Components** = technical surface (auth, billing, dashboard, api-gateway). Owned by Eng.
- **Labels** = cross-cutting attributes (area, priority, stage-in-workflow, flag-gated, discovery-phase, platform).

Examples:
- `area/onboarding`
- `priority/p1`
- `flag-gated/new-onboarding-v2`
- `discovery-phase/one-pager`
- `platform/ios`

Pin the taxonomy in the "About this space" Confluence page. Drifting labels destroy JQL filters.

## Anti-patterns

- **Links only on some tickets.** Incomplete graph; discoverability half-broken.
- **Over-using "blocks".** Everything blocks everything; planning stalls; nobody trusts "blocked".
- **Automations that remove judgement.** Auto-closing stale tickets destroys visible work.
- **Confluence-Jira link rot.** PRD renamed; Jira link 404s.
- **Shadow backlogs.** Team maintains a spreadsheet or Notion doc because Jira feels heavy → two sources of truth.
- **Over-automated notifications.** Every change notifies everyone → everyone mutes.
- **Label sprawl.** 400 labels, no convention, filters useless.

## Files

JQL filters + automation recipes documented in the "About this space" Confluence landing page + pinned in team README. Shared JQL queries saved as "team filters" in Jira.
