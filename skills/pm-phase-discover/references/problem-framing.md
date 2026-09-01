# Problem framing

## What it is

Turning scattered requests, symptoms, and observations into a clear statement of **user + problem + desired outcome + assumptions + constraints**.

## Why it matters

Strong delivery is impossible if the team is solving the wrong problem or a vaguely defined one. Senior PMs ship the wrong thing on time less often than junior PMs ship something on time.

## When to use

- a brief arrives as a solution ("let's add a share button")
- multiple stakeholders describe the problem differently
- the frame was set 2 quarters ago and evidence has changed
- the team is about to build but cannot answer "and we know this because…"

## Template

```markdown
# Problem brief — [short name]

## Target user
Who, described specifically enough that engineering and design can picture one person.
- segment:
- situation / moment:
- what they are trying to do (the job):

## The problem
In one or two sentences. No solution. No jargon.

## Why this matters now
Evidence + business context. Why the frame is worth the team's time.

## Desired outcome
What changes in the user's life if we solve this? Observable, not metaphorical.

## Evidence (what we know)
- [ ] interviews / quotes / research (N=, segment, date)
- [ ] behavioural data / funnel / retention (source, cohort)
- [ ] support / sales / CS themes (volume, trend)

## Assumptions (what we believe but have not verified)
- [assumption] — how to test / falsify

## Constraints
- technical, legal, timing, headcount, budget

## What success looks like
A paragraph. Then one metric (or two) that would move if we solved it.

## Non-goals
What we will NOT solve even if tempting.

## Invalidation condition
"This frame is wrong if ___."
```

## Checklist — "is this frame sharp?"

- [ ] target user is described as a person, not a role
- [ ] problem statement contains no solution
- [ ] evidence distinguishes hard signal from hearsay
- [ ] assumptions are separated from evidence
- [ ] success is observable, not metaphorical
- [ ] non-goals are explicit
- [ ] invalidation condition is concrete

## Common anti-patterns

- **Solution-first framing.** "Users need a faster checkout button" contains the solution. Rewrite as "Users abandon at step 3 because ___".
- **Infinite scope.** "Improve UX" is not a problem. "Reduce time-to-first-value for new free-tier users" is.
- **Mixed stakeholder asks.** Sales wants X, support wants Y, leadership wants Z. Name them as stakeholder asks; the user problem is separate.
- **No invalidation.** If no evidence could make you drop this frame, it is a belief, not a hypothesis.

## Example

**Brief as received:** "We need to add onboarding tooltips to improve engagement."

**Reframed:**

> **Target user:** New free-tier users in the first session after signup (B2B SaaS admin).
>
> **Problem:** 62% of first-session users never reach the "create first project" step. They see the empty dashboard and bounce.
>
> **Evidence:** Funnel drop-off measured across 3k signups last quarter. 8 interviews in the last month mentioned "I didn't know where to start" unprompted.
>
> **Outcome:** New users create their first project within the first session, without needing support.
>
> **Success metric:** % of signups that reach `project_created` in session 1 (currently 38% → target 60%).
>
> **Non-goals:** Re-architecting the dashboard. Power-user features. Mobile parity.
>
> **Invalidation:** If session-1 activation holds below 45% after fixing the empty-state, the bottleneck is earlier (signup-to-first-session, not first-session-to-activation).

Tooltips may or may not be the answer. That is a Develop-phase decision.

## Files

Persist to `.ai/memory/projects/<slug>/discovery.md` or a dedicated `problem-brief-<topic>.md`. Link from the project profile.
