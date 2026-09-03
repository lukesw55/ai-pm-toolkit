# Backlog structuring and scope slicing

## What it is

Breaking work into **coherent increments that maximise learning and value** while remaining feasible for delivery teams. Strong PMs shape the *grain size* of delivery so teams learn faster and waste less.

## Why it matters

Expert PMs don't only choose what to do — they shape how it moves. Giant epics destroy learning cycles. Thin slices preserve optionality.

## Key concepts

- **Epic** — a coherent bet delivered over multiple sprints (weeks-to-months). Has its own PRD.
- **Story** — one vertical slice of user-observable value. Should fit in 1 sprint.
- **Task** — implementation step under a story. Eng-owned.
- **MVP** — Minimum Viable Product: the smallest thing that proves or disproves the bet.
- **MVC** — Minimum Viable Change: smaller than MVP; an A/B-able increment.
- **Thin slice** — vertical slice (end-to-end) rather than horizontal layer (just the UI, just the API).

## Story slicing — principles

1. **Slice by user outcome, not by component.** "Users see empty state" beats "Build the empty-state API endpoint".
2. **Each slice must deliver observable user value.** If a slice doesn't change what a user can do or see, it's probably a task, not a story.
3. **Smallest slice that teaches us something.** Optimise for learning rate, not for parallelism.
4. **Vertical over horizontal.** Better to ship one complete flow than all the APIs with no UI.
5. **Flag-protect risky slices.** Feature flags let you ship code without exposing incomplete value.

## Story map — template

A story map organises slices visually by user journey × release:

```
User journey →    [Signup]    [First use]    [Core task]    [Upgrade]
                     |            |               |             |
MVP (release 1)    [slice]      [slice]         [slice]       [slice]     ← happy path only
R2                 [slice]      [slice]         [slice]                   ← top friction
R3                                              [slice]                   ← depth / delight
Later              ...          ...             ...           ...
```

Write as markdown table or maintain in a Jira board aligned to this shape.

## Ready-to-use template — epic breakdown

```markdown
# Epic — [name]

**PRD:** [link]
**Primary metric:** [link to KPI tree entry]

## Bet (1 sentence)
If we [ship this], [user/segment] will [behaviour change], moving [metric] from [X] to [Y].

## Slicing strategy
How we're breaking this down and why (vertical by journey stage, by segment, by risk, etc).

## Release plan

### MVP (Release 1 — N weeks)
**Goal:** prove [specific belief] by observing [metric movement / behaviour].
- [ ] Story 1 — [user outcome]
- [ ] Story 2 — [user outcome]
- [ ] Story 3 — [user outcome]

**Learning outcomes:**
- if [metric moves X] → [decision]
- if [metric doesn't move] → [decision: iterate / kill]

### Release 2 (if learning is green)
- top 2–3 improvements based on observed friction
- additional segment support

### Release 3+
Directional only; commit at the time.

## What this epic explicitly does NOT include
- non-goals at the epic level
```

## Ready-to-use template — user story

```markdown
[Type] [Short verb-phrase title]

## User value
As a [segment user], I want to [do X], so that [outcome].

## Acceptance criteria
- [ ] Given [context], when [action], then [observable result]
- [ ] ...

## Scope IN
- [what's covered]

## Scope OUT
- [explicitly not covered in this story]

## Design
[link]

## Tracking events (if any)
- [event-name] — fires on [trigger], properties: [list]

## Links
PRD: ...
Parent epic: ...
Design: ...
Related stories: blocks / is blocked by

## Definition of Done
- [ ] code merged + deployed behind flag
- [ ] unit + integration tests green
- [ ] instrumentation live + verified
- [ ] design review passed
- [ ] accessibility checked (for UI)
- [ ] support briefed (if user-facing material change)
- [ ] PRD + ticket links bidirectional
```

## Sizing heuristics (not estimates)

- **XS** (half day) — config change, copy change, flag toggle
- **S** (1–2 days) — small story inside an existing flow
- **M** (3–5 days) — typical user story
- **L** (1–2 sprints) — multi-surface story; consider slicing further
- **XL** (>2 sprints) — not a story, it's an epic; slice it

Rule of thumb: if a story is L or XL and isn't sliced, go back and slice it. L+ stories are where surprises live.

## Backlog hygiene — what a healthy backlog looks like

- **Top 10–15 items are ready** for planning (clear acceptance criteria, sized, linked).
- **Next 15–30 items are refined but unsized** (problem + direction known).
- **Further items are themes/bets**, not stories.
- **No zombies.** Items older than 6 months without movement should be archived or re-promoted deliberately.
- **Parent-child links are bidirectional.**
- **Labels are consistent** (area, priority, discovery-phase).

## Common anti-patterns

- **Giant epics that never close.** "Improve onboarding" sitting open for 18 months.
- **Backlog as dumping ground.** Every stakeholder idea lands in the backlog and stays; signal-to-noise collapses.
- **Slicing by component, not user need.** "Backend API" story + "Frontend" story + "iOS" story for one user outcome. Ship nothing until all three merge.
- **Output granularity as customer value.** Lots of small tasks ≠ lots of value.
- **No explicit MVP.** Everything is "must have". Team can't start.
- **Ready-criteria drift.** Stories enter sprints under-defined; rework explodes.

## Scope negotiation — the questions to ask

When eng says "this is bigger than we thought":

1. What specifically is bigger — can we slice again?
2. What could we ship WITHOUT (non-goals)?
3. What can we defer to a follow-up slice?
4. Is there a cheaper way to test the same belief?
5. What do we lose if we ship a thinner slice?

The PM's job is to preserve the learning, not the feature list.

## Seniority signals

- **Beginner:** writes and refines backlog items with help.
- **Intermediate:** keeps one team's backlog healthy and usable.
- **Advanced:** turns complex bets into learning-friendly increments; says "no" well.
- **Expert:** teaches teams to scope smaller without losing strategic intent.

## Files

The stage-5 selection and release slices live in `.ai/memory/projects/<slug>/scope-slices.md`. Epic breakdowns live under `.ai/memory/projects/<slug>/epics/<epic>.md` or in Jira with a link from the PRD.
