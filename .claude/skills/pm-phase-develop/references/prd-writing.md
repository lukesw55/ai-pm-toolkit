# PRD and specification writing

## What it is

A **concise, actionable product requirements document** that explains the problem, target user, success criteria, scope, trade-offs, and open questions. A PRD gives engineering and design **context and room to solve** — it does not dictate the solution pixel by pixel.

## Why it matters

Good requirement writing prevents rework through ambiguity; bad writing triggers rework through over-prescription. A senior PM's PRD tells you the WHY, frames the WHAT, and leaves HOW to the people who will implement it.

## Ready-to-use template — PRD

```markdown
# PRD — [Feature / Initiative] — [YYYY-MM-DD]

**Status:** Draft | In review | **Approved** | Shipped | Archived
**Owner:** @name
**Contributors:** @design @eng-lead @analytics @pmm
**Links:** strategy memo / discovery brief / sizing / tracking plan / Jira epic

## TL;DR
Two–three sentences. User problem + what we're doing + expected outcome.

## Problem
Who has what pain, in what context, and why it matters. Evidence-backed.
(Link to problem brief / discovery.)

### Target user
One or two specific segments. Describe them as people, not roles.

### Current behaviour (as-is)
How they solve this today (in-product, workarounds, competitors). Friction moments.

## Goals + non-goals
### Goals
Specific, observable, tied to metrics.
- G1: ...
- G2: ...

### Non-goals (explicit)
- NG1: ...
- NG2: ...

## Success metrics
### Primary
Metric definition + baseline + target + horizon. Link to KPI tree.

### Secondary
Supporting metrics (adoption, engagement, depth).

### Guardrails
Metrics that must NOT degrade (reliability, support, trust, retention).

## Requirements

### Must-have (MVP)
- [ ] Req 1 — user-facing outcome, not implementation detail
- [ ] Req 2
- [ ] Req 3

### Nice-to-have (post-MVP)
- [ ] ...

### Acceptance criteria (for each must-have)
Given / when / then format, or behavioural bullets. Observable.

## User flow (core happy path)
Annotated flow or 3–6 numbered steps. Cover empty state, error state, success state.

## Scope
### IN
What this PRD covers.

### OUT
What this PRD explicitly does NOT cover (with reason).

## Dependencies
- on other teams: [team — what — by when]
- on external systems:
- on legal / compliance:

## Risks + mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| ... | ... | ... | ... |

## Open questions
- [ ] Q1 — owner — target answer date
- [ ] Q2

## Release plan
- rollout: [dark → internal → beta → GA] + % gates
- feature flag: [name / logic]
- rollback criteria
- release-notes needed: [yes/no — link to `release-notes.md`]
- enablement needed: [sales / support / CS]

## Tracking plan summary
Top events this feature must emit (full plan → `tracking.md`):
- [event] — triggered when — key properties

## Design
Links to Figma / design doc. Component patterns inherited from design system. States covered: empty, loading, error, success, accessibility.

## Technical notes (light)
Anything eng needs to know that isn't implementation detail — API contracts affected, data model implications, NFRs.

## Decision log
As the PRD evolves, log decisions here with date + rationale. Silent drift breaks trust.

## Appendix
- research raw notes
- alternative approaches considered
- prior art (internal or competitive)
```

## How big should a PRD be?

- **Tiny change (1-dev-week):** 1-page. Problem + metric + acceptance + rollout.
- **Typical feature (2–6 wks):** 2–4 pages with the full template above.
- **Major initiative / launch:** 3–6 pages + PRFAQ cross-linked + staged plan.
- **Platform / deprecation / pricing:** special-form doc; use decision memo + ADR.

If your PRD is 10+ pages, something is wrong. Usually it's doing the job of a strategy memo too — extract that out.

## Writing discipline

- **Start with TL;DR.** A busy reviewer should know what's at stake in 30 seconds.
- **Problem before solution.** If you can't explain the problem without using the solution name, go back to discovery.
- **Requirements in user outcomes.** "User can export their dashboard as CSV" beats "Implement a CSV export button in the dashboard header".
- **Acceptance criteria are testable.** "Looks clean" is not an acceptance criterion. "CSV export completes within 3s for datasets up to 10k rows; rows match the filter applied in the dashboard" is.
- **Name non-goals explicitly.** Silent scope drift is the #1 PRD failure mode.
- **Open questions are first-class.** A PRD with no open questions is either finished or dishonest.
- **Keep it alive.** Update it as decisions are made; archive when shipped and stable.

## Common anti-patterns

- **The novel.** 15-page PRD; engineering reads the first 2 pages and asks questions the next 13 pages answer.
- **UI dictation.** "Button should be blue #0066FF, 44px tall, at top-right." Design owns this. PRD should cover patterns/constraints/states, not hex codes.
- **Missing success criteria.** "We'll see if users like it." → won't.
- **Missing non-goals.** Scope creep starts here.
- **Stale docs.** PRD says X, Jira says Y, design shows Z. Nobody knows the source of truth.
- **No tracking plan.** Ship without instrumentation = ship blind.
- **No rollout / rollback plan.** "We'll figure it out at launch."

## Checklist — ready for engineering?

- [ ] Problem is clear and evidence-backed
- [ ] Target user is specific
- [ ] Primary metric + guardrails defined
- [ ] Must-have requirements each have acceptance criteria
- [ ] Non-goals are written
- [ ] Dependencies + owners named
- [ ] Tracking plan drafted
- [ ] Rollout + rollback defined
- [ ] Open questions tracked with owners + dates
- [ ] Reviewed by eng-lead + design + analytics + PMM (as applicable)

## Files

`.ai/memory/projects/<slug>/prds/<feature-name>.md`. Publish to Confluence via `pm-transversal-docs`; open Jira epic + link bidirectionally.
