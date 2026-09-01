# Tracking plan design (pre-launch instrumentation)

## What it is

Defining **what events, properties, and metrics must be captured** so product usage, funnel, and experiment analysis will be trustworthy and useful. Designed *with* the PRD, not patched in after code ships.

## Why it matters

Bad instrumentation creates **false confidence, missing answers, and expensive rework**. The #1 reason post-launch analytics are useless is that the events weren't designed thoughtfully before launch.

## Core concepts

- **Event** — a thing that happened (`project_created`, `checkout_started`, `error_shown`).
- **Property** — metadata on the event (`plan: "pro"`, `step: 3`, `duration_ms: 1240`).
- **User trait** — persistent attribute of the user (`plan`, `signup_date`, `segment`).
- **Session** — a grouping of events within a time window (varies by analytics tool).
- **Cohort** — a group of users defined by behaviour or trait.
- **Funnel** — a sequence of events the user should flow through.

## Naming conventions (pin these)

Choose one, stick with it, document it.

**Object-action convention** (recommended for product events):
```
<object>_<past_tense_verb>
```
Examples: `project_created`, `checkout_completed`, `email_verified`

**Properties** — snake_case, typed consistently:
```
{ "plan": "pro", "step": 3, "duration_ms": 1240, "source": "onboarding" }
```

Anti-pattern names: `clicked_button`, `did_thing`, `User Logged In` (mixed case + spaces), `checkout1`.

## Ready-to-use template — tracking plan

```markdown
# Tracking plan — [feature / initiative] — [date]

**Owner:** @pm + @analytics
**Status:** Draft | In implementation | **Live** | Deprecated
**Linked:** PRD / KPI tree / experiment briefs

## Scope
What user-facing flow(s) this plan covers.

## North Star + primary metric dependency
Which top-level metrics this plan must support.

## Event schema

### Event: `project_created`
**Trigger:** fires on successful creation of a new project (server-confirmed, not client-optimistic)
**Stage:** post-launch GA | beta only
**Owner:** @eng-lead

| Property | Type | Values / format | Required | Notes |
|---|---|---|---|---|
| `project_id` | string | uuid | yes | primary key for analysis |
| `user_id` | string | uuid | yes | user making the action |
| `plan` | string | `free / pro / business / enterprise` | yes | user's current plan |
| `source` | string | `dashboard / cli / api / integration` | yes | where creation originated |
| `template_used` | string | template slug or `null` | no | for templates analysis |
| `is_first_project` | boolean | true/false | yes | distinguishes activation from repeat |

**KPI this feeds:** activation (primary) — `% signups → project_created within 24h`

### Event: `project_opened`
...

### Event: `error_shown`
...

## User traits (persistent)
| Trait | Type | Source | Updated when |
|---|---|---|---|
| `plan` | string | billing system | on plan change |
| `signup_source` | string | acquisition funnel | at signup (immutable) |
| `role` | string | user profile | on profile update |

## Cohort definitions (query-ready)
| Cohort name | Definition |
|---|---|
| Activated users | fired `project_created` within 24h of signup |
| Power users | fired `project_opened` in ≥5 of last 7 days |
| At-risk | no `project_opened` in 14 days (was active before) |

## Funnels (explicit)
### Primary activation funnel
1. `signup_completed` →
2. `first_session_started` →
3. `project_created` →
4. `project_opened_second_time` (retention check)

Goal: % users completing step 1→3 within 24h.

## Guardrail events
Events that must stay healthy:
- `error_shown` with `severity: critical` — must not increase after launch
- `session_ended` with `reason: crash` — guardrail
- `support_contacted` from feature page — guardrail

## Data privacy + governance
- PII handling: [email/name stored? hashed? excluded from event properties?]
- data retention: [N days/months]
- geographic restrictions: [EU residency, etc.]
- opt-out logic: [DNT + user-level opt-out behaviour]

## Implementation ownership
| Platform | Event | Owner | Status |
|---|---|---|---|
| Web | all above | @eng-web | drafted |
| iOS | all above + `push_notification_received` | @eng-ios | not started |
| Backend | `project_created` (server) | @eng-backend | in review |

## QA checklist (before launch)
- [ ] each event fires exactly once per trigger
- [ ] property types match schema (no "1" when it should be 1)
- [ ] PII rules enforced (no raw emails in properties)
- [ ] funnel conversion reproduces expected counts in staging
- [ ] events flow to the primary analytics tool (no lost events)
- [ ] dashboards referencing these events are updated
- [ ] dbt / warehouse models consume the new events correctly (if applicable)

## Changelog
- [date] initial plan
- [date] added `template_used` property
- [date] renamed `proj_create` → `project_created` (migration note)
```

## Design principles

### 1. Start from the question, not the event

"What do we need to answer post-launch?" → list 5–10 questions → design the minimal event set that answers them. Don't start with "let's track every click".

### 2. Fewer events, more properties

Per industry experience: one event with 10 properties beats 10 events that all mean similar things. Properties let you slice; events you can't easily combine.

### 3. Server-side preferred for "did it really happen" events

Purchases, account creations, permission changes — server-confirmed events are truth. Client-side is fine for UX-driven stuff (scrolled, viewed, clicked) but don't put business-critical logic there.

### 4. Versioning from the start

When events change, version them (`checkout_started_v2`) or coordinate migration. Breaking changes destroy dashboards silently.

### 5. Link events to outcomes at design time

Every event should answer "which KPI does this feed?". If you can't answer, the event is probably noise.

### 6. Set a taxonomy owner

Someone (analytics, data eng, platform PM) owns the taxonomy long-term. Without an owner, events sprawl and rot.

## Anti-patterns

- **Event sprawl.** 400 events, nobody knows which ones matter. Signal-to-noise = 0.
- **Inconsistent naming.** `user_signed_up`, `SignupCompleted`, `signup`, `signup_success` all in the same product.
- **"Track everything."** Ship now, figure out analysis later. Answer: you never figure it out.
- **No QA.** Events ship with wrong property types; dashboards quietly produce wrong numbers for 3 months.
- **Client-only for critical events.** Users with adblockers don't fire events; your revenue metric is biased.
- **No owner.** Taxonomy decays. New features add events inconsistently.
- **Events without KPI linkage.** "We tracked it because we might need it." You won't.

## Integration with the PRD

A PRD without a tracking plan is incomplete. Template:
- include a **Tracking plan summary** in the PRD (top 3–5 events)
- full plan lives in `tracking.md` sibling file
- primary metric in the PRD uses the events defined here
- QA checklist blocks "Definition of Done"

## Seniority signals

- **Beginner:** uses existing instrumentation as given.
- **Intermediate:** influences event + property definitions for a product area.
- **Advanced:** designs scalable, decision-ready event taxonomies and catches gaps early.
- **Expert:** raises the org's measurement quality standard across web, mobile, and platform.

## Files

`.ai/memory/projects/<slug>/tracking.md`. If PostHog MCP is available (`event-definitions-list` and related tools; the `mcp__<server>__` prefix varies by environment), validate against existing event definitions before inventing new ones.
