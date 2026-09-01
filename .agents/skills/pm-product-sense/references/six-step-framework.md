# BUILD — six-step decision framework

## What it is

A six-step structure for reasoning through an ambiguous product decision: **clarifying questions → strategy/goal → user types → pain points → solutions → MVP**. Adapted from Exponent's Product Sense Interview guide. Each step constrains the next — the discipline is in the order, not in any single step being clever.

## Why it matters

The most common product-sense failure is skipping straight to a solution. A confident, well-argued solution built on an unexamined user type or an unranked pain point is still a guess — it just doesn't feel like one. Working the steps in order is what turns "this feels right" into something someone else can audit.

## The six steps

### 1. Clarifying questions

Don't silently pick an interpretation of an ambiguous ask. Name the ambiguity and ask (or state the assumption explicitly if this is a written exercise with no one to ask): what's the scope, what's the platform, what's the business context, what's already been tried.

**Contract:** at least one real ambiguity named, not a rhetorical question with an obvious answer.

Checklist:
- [ ] scope (which product surface, which market, which user segment) is confirmed or explicitly assumed
- [ ] the underlying business goal is at least roughly known before proceeding
- [ ] no interpretation has been silently locked in

### 2. Strategy / goal

State what this decision is meant to serve — a company goal, a metric, a strategic bet. Without this, step 6 (MVP / prioritisation) has nothing to prioritise against.

**Contract:** one explicit sentence naming the goal this decision serves.

Checklist:
- [ ] the goal is a specific outcome, not "make the product better"
- [ ] the goal is stated before any user type or solution is named

### 3. User types

Enumerate the plausible user types before picking one. Naming several and choosing deliberately signals more judgement than jumping straight to a single assumed persona — and often surfaces a better target than the first guess.

**Contract:** at least two distinct user types named, with an explicit choice (and reason) of which to focus on.

Checklist:
- [ ] more than one user type considered
- [ ] the chosen type is justified against the strategy/goal from step 2, not picked arbitrarily

### 4. Pain points

Surface pain points per user type, and rank them by severity/frequency rather than listing them flat. A pain point search that stays at the surface ("it's slow") without probing for the more severe, more specific pain underneath is a shallow pass.

**Contract:** pain points tied to a named user type, with at least a rough severity ranking.

Checklist:
- [ ] pain points are specific to the chosen user type, not generic
- [ ] at least a rough ranking (most severe first) is given, not a flat list
- [ ] the pain point, not a proposed fix, is what's being described

### 5. Solutions

Generate solution candidates, each tied back to a specific pain point from step 4. Reject weak candidates explicitly, with a stated reason — silently dropping an option looks like it was never considered.

**Contract:** at least one solution proposed, at least one considered and explicitly rejected with a reason, each mapped back to a pain point.

Checklist:
- [ ] every solution traces to a named pain point, not a feature idea in isolation
- [ ] at least one alternative was rejected, with a reason stated
- [ ] a vision/pitch line exists — a concise, compelling one- or two-sentence statement of what the solution does, not just a feature list

### 6. MVP

Cut scope against the goal from step 2: what's in, what's explicitly out, and how success will be measured. This is where the framework converges — everything upstream justifies why this particular MVP, not a bigger or smaller one.

**Contract:** explicit in/out scope and a named success metric, both traceable to earlier steps.

Checklist:
- [ ] scope cut is justified against the goal (step 2) and the top pain point (step 4), not "everything we thought of"
- [ ] what's explicitly excluded is stated, not left implicit
- [ ] a success metric is named — what would tell us this worked
- [ ] pitfalls/trade-offs are named: what wasn't evaluated, what could go wrong, what would change the recommendation

## Mapping to the One Pager

BUILD's six steps map onto `pm-phase-define/references/one-pager.md`'s **Five Unlocks** quality bar:

| BUILD step | One Pager unlock |
|---|---|
| Clarifying questions + user types | **Who?** — specific segment, not "users" |
| Pain points | **What's the real problem?** — evidenced, not hypothesized |
| Solutions | **What would we do about it?** — direction, not exhaustive spec |
| MVP (success metric) | **What will change?** — metric + magnitude + confidence |
| Strategy/goal | **Why now / why this / why us?** — strategic fit + timing |

A BUILD walk-through that hits all six steps cleanly should convert into a One Pager with minimal rework — if it doesn't, a step was skipped or under-specified.

## Common anti-patterns

- **Solution-first.** Naming a feature before naming the user type and pain point it addresses.
- **Single user type, no enumeration.** Picking the first plausible user out of the gate instead of considering a few and choosing deliberately.
- **Flat pain-point list.** No ranking, no sense of which pain point actually matters most.
- **No rejected alternatives.** A solution section with one option looks like the only option existed.
- **No MVP cut.** A feature list with no explicit in/out boundary or success metric — "we'll build all of it and see."
- **No vision line.** Features described without ever stating, in one clear sentence, what the thing actually is or does for the user.

## Calibration examples (from Product Sense interview transcripts)

Paraphrased, not quoted; source videos linked. See `../evaluation-rubric.md` for the EVALUATE-side calibration and `../../DOCTRINE.md` for the calibrated-disagreement material these overlap with.

- **Enumerate before picking.** The framework's own walkthrough (a library redesign) explicitly warns against picking one user "out of the gate" — enumerate children, parents, and community members first, then choose deliberately which to focus on. ([Answer Product Sense Interview Questions Like A Pro](https://www.youtube.com/watch?v=WE0KeryvpXE))
- **Rank pain points, don't list them flat.** The same walkthrough distinguishes a shallow pain point ("libraries are boring") from a more specific, more severe one tied to a particular user (a college student who can't find research material) — and treats the ranking itself as part of the answer, not an afterthought.
- **State a vision mid-answer, not just a feature list.** A concise, compelling pitch line ("libraries are never going to be boring again") mid-interview signals the ability to both reason through a decision and persuade a team to align on it — the same discipline `pm-transversal-comms`'s SCQA/BLUF asks for in shorter form.
- **Prioritise against the stated goal, not against feature appeal.** The same source ties every proposed feature back to the pain point and vision named earlier — a feature that doesn't serve the stated goal gets deprioritised explicitly, not quietly dropped.
- **Think one level above the immediate task.** At the principal level, a strong answer named the big-picture impact and worked with others to clear a vague problem space into a roadmap, rather than waiting to be handed a scoped problem — the proactive-framing habit BUILD's step 1-2 sequence is meant to formalise. ([Principal AI PM Mock Interview](https://www.youtube.com/watch?v=udB8AUO4dvM))
- **Name what wasn't anticipated.** A strong retrospective answer named a concrete miss (unanticipated fraud vector in a payments pilot) rather than a generic "we'd communicate better" — the same honesty BUILD's step-6 pitfalls checklist asks for. ([Amazon PM Mock Interview: Solving Pain Points](https://www.youtube.com/watch?v=CR8Niz9DrWU))

## Files

- BUILD walk-throughs tied to a real decision: `.ai/memory/projects/<slug>/decisions.md` or directly into the One Pager draft once the six steps are worked through
