# Confluence templates

Ready-to-paste Confluence templates for the PM artefacts produced most. Each template is scan-friendly and consistent with the relevant phase skill. Markdown here renders in Confluence's Markdown import or can be pasted into Confluence wiki markup with minor tweaks.

---

## Template — Strategy memo

```markdown
# [Area] Strategy — [Horizon, e.g. 2026 H1]

**Status:** Draft | In review | **Approved** | Superseded
**Owner:** @name   **Sponsors:** @exec
**Last updated:** YYYY-MM-DD
**Related:** KPI tree / prior strategy / roadmap

## TL;DR
Two sentences. Where we play + how we win.

## Where we play
- segment(s) we serve:
- jobs we help users do:
- category (as the customer sees it):

## How we win
- unique value:
- why customers switch and stay:
- what we compound (the moat):

## Strategic pillars (3–5)
1. **[Pillar name]** — [1-line rationale]
2. ...

## Strategic bets (this horizon)
1. [Bet] — pillar: [X] — outcome: [metric movement] — confidence: [L/M/H]
2. ...

## What we are NOT doing
- ...

## Assumptions (with invalidation conditions)
- ...

## Metrics we watch
North Star:
Inputs:
Guardrails:

## Risks + refresh cadence
```

---

## Template — KPI tree

```markdown
# [Area] KPI tree — [Version / Date]

**Owner:** @analytics   **Last updated:** YYYY-MM-DD

## Business outcome
[e.g. annual recurring revenue]

## North Star
**Definition:** ...
**Formula:** ...
**Baseline / target:** ...
**Owner:** @name

## Input metrics
### Input 1 — [name]
- definition, baseline, target, owner, level-3 breakdown

### Input 2 — ...

## Guardrails
- reliability, support, trust, retention — thresholds + owners

## Review cadence
- weekly, monthly, quarterly

## Change log
```

---

## Template — Impact Brief (GTM) — stage 2

```markdown
# Impact Brief — [Topic] — YYYY-MM-DD

**Status:** Draft | **Approved for discovery** | Rejected
**PM:** @name   **PMM:** @name

## TL;DR
Two sentences.

## Problem (what we're hearing)
Segment + evidence. ≤ 150 words.

## Target segment
Behavioural + reachability

## Business impact (rough)
Order of magnitude. Primary-metric direction. Strategic-fit note.

## GTM considerations
Pricing / sales motion / partner / comms sensitivity / positioning.

## Risks that would kill this
2-3 things that would make this not worth pursuing.

## What discovery must answer
- Q1, Q2, Q3

## Discovery plan (lightweight)
Method + sample + timebox + owner.

## Invalidation condition
"We will NOT advance if [specific finding]."

## Decision ask
```

---

## Template — One Pager — stage 4

```markdown
# One Pager — [Initiative] — YYYY-MM-DD

**Status:** Draft | **Approved for build** | Parked
**PM:** @name
**Links:** Impact Brief / Discovery synthesis

## TL;DR (3 sentences)
Problem + direction + expected primary-metric movement.

## Problem (validated)
Segment + pain + evidence.

## JTBD
Concise.

## Proposed direction
High-level approach; 1 alternative considered.

## Expected impact
| Metric | Current | Expected | Confidence |

## Strategic fit + effort + timing + non-goals + risks + dependencies + ask
```

---

## Template — PRD

Full template in `pm-phase-develop/references/prd-writing.md`. Confluence version keeps the same structure plus a front-matter panel:

```markdown
# PRD — [Feature] — YYYY-MM-DD

| Status | Owner | Contributors | Jira epic | Design | Tracking plan |
|---|---|---|---|---|---|
| Draft | @pm | @design @eng @analytics @pmm | [link] | [link] | [link] |

## TL;DR
## Problem
## Goals + non-goals
## Success metrics
## Requirements (MVP + nice-to-have)
## Acceptance criteria
## User flow
## Scope IN / OUT
## Dependencies
## Risks
## Open questions
## Release plan
## Tracking plan summary
## Technical notes (light)
## Decision log
## Appendix
```

---

## Template — DACI

```markdown
# DACI — [Decision] — YYYY-MM-DD

**Status:** Pending | **Decided** | Implemented

## Decision at stake
## One-way / two-way door
## Roles
- Driver: @name
- Approver: @name
- Contributors: @name, @name
- Informed: @name, @team-channel

## Recommendation
## Options (A, B, C)
## Trade-offs + risks
## Open questions (for approver)
## Decision + date + rationale
## Follow-up actions
```

---

## Template — Launch plan

```markdown
# Launch plan — [Initiative] — YYYY-MM-DD

**Status:** Planning | In progress | **GA** | Paused | Rolled back
**Target GA:** YYYY-MM-DD

## TL;DR + success criteria (3/6/12 wk) + guardrails

## Rollout stages + gates
Dark → Dogfood → Closed beta → Open beta → GA (table)

## Enablement checklist
Sales / CS / Support / Marketing / Docs / Legal / Analytics / Ops

## Launch communications timeline

## Readiness review (T-3d)

## Rollback plan
```

---

## Template — Release notes (public)

```markdown
# Release notes — [Month YYYY]

## [YYYY-MM-DD] — [Feature name]

**One-liner:**
**What it does:**
**Who it's for:**
**How to use it:**
**Availability:**
**Migration note (if any):**
**Learn more:** [docs / blog link]
```

---

## Template — Internal enablement one-pager

```markdown
# Enablement — [Feature] — YYYY-MM-DD

## What shipped (30s)
## Why it matters (60s)
## Who to pitch it to
## Talking points
## Pitfalls + objection handling
## Demo flow
## Support scenarios
## Where to find more
```

---

## Template — Post-launch close-out

```markdown
# Close-out — [Initiative] — YYYY-MM-DD

## What we shipped
## Hypothesis vs outcome
## Decision + rationale
## Learnings (ranked)
## What surprised us
## Follow-ups
## Memory updates
```

---

## Template — Operating review / QBR

```markdown
# [Area] Operating Review — [Period]

**Presenter:** @pm   **Audience:** leadership

## TL;DR (30s)
## Against the plan (bets vs outcomes table)
## KPI tree movement
## What we learned
## What we're changing
## Risks for next period
## Asks of leadership
## Appendix (launch scorecards, experiment readouts, dashboards)
```

---

## Template — Retrospective (team-level)

```markdown
# Retrospective — [Period or Initiative] — YYYY-MM-DD

**Facilitator:** @name   **Attendees:** ...

## What went well
## What didn't
## Surprises
## What we'll change
## Action items + owners + dates
```

---

## Template — Research synthesis

```markdown
# Research synthesis — [Topic] — YYYY-MM-DD

## Research question(s)
## Method + sample
## Themes (ranked by evidence strength)
### Theme 1: [name]
- definition, frequency, segment pattern, representative quotes (3), implication, confidence

### Theme 2: ...

## Triangulation with quant
## Recommendations
## Raw data location (interviews, transcripts, data extract)
```

---

## Template — "About this space" landing page

```markdown
# About this space

## Purpose
What this space is for.

## Conventions
- title conventions
- status lifecycle
- ownership rules

## Folder structure
- Strategy — ...
- Discovery — ...
- Priorities — ...
- (etc.)

## Who to ask
| Topic | Owner |
|---|---|
| strategy | @ |
| prds | @ |
| launches | @ |

## Onboarding new team members
Day 1: read [strategy memo, KPI tree, active PRDs]
Week 1: attend [reviews]
```

---

## Using these templates via MCP

If MCP Atlassian is available, you can create pages directly:

```
mcp__claude_ai_Atlassian_Rovo__createConfluencePage
  with: spaceKey, title, body (in wiki markup or markdown depending on integration)
```

For updates:
```
mcp__claude_ai_Atlassian_Rovo__updateConfluencePage
```

Otherwise: draft locally in markdown, paste into Confluence, adjust formatting.

## Voice + style notes

- imperative, not passive ("Define success metrics" not "Success metrics should be defined")
- specific, not grand ("Reduce time-to-first-value from 5 min to 2 min" not "Improve onboarding")
- reader first: TL;DR on top; appendix at bottom
- date-stamp everything
- link heavily
- name owners (humans, not teams)
