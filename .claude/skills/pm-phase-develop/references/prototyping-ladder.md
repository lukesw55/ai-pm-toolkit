# Prototyping ladder — where the prototype lives and what it costs engineering

## What it is

Three tiers for a stage-6 prototype, ordered by where the artefact lives and how much engineering time it consumes, not by how real it looks. Tier A is a throwaway prototype outside the codebase. Tier B is a code prototype on a disposable branch of the real codebase, built with a coding agent such as Claude Code or Codex. Tier C is a small change the PM ships as a pull request that engineering reviews. The ladder complements the cost-of-learning hierarchy in `pm-phase-discover/references/opportunity-hypothesis.md`: that list picks how much evidence to buy for a risk; this one picks where to build the artefact that buys it. Its rung 4 ("clickable, no backend") is tier A here.

## Why it matters

With coding agents on every PM's machine the question is no longer whether the PM can build something. It is where that artefact should live and who reviews it. The wrong tier costs in three ways: a hosted demo gets mistaken for a feasibility proof, PM-written code lands in logic the team has to own, or engineering spends a sprint answering a comprehension question a mock would have settled in a day.

## The three tiers

| Tier | Lives in | Fidelity | Engineering cost | Answers | Never used for |
|---|---|---|---|---|---|
| A. Throwaway | a hosted builder or a standalone mock; no real components or data model | looks right, behaves approximately | none | desirability, comprehension, flow order | feasibility, integration shape |
| B. Code prototype | a disposable branch of the real codebase, or a sandbox repo, built with a coding agent | real components, routes and mock data | a look at the branch, a sandbox refresh | interaction fidelity, integration shape, state coverage | production; the branch is never merged as-is |
| C. Shipped change | a pull request the PM authors and engineering reviews and merges | production | a code review | copy, configuration, flags, small UI in existing components | core logic, data model, billing, auth, permissions, migrations |

The rule behind tier C: the PM does not ship code inferior to the team's next to the team's. If the change needs the team's judgement to be safe, the team writes it.

## Ready-to-use template — Sandbox repo request

```markdown
# Sandbox repo request — <product>

- **Owner**: <engineering role who keeps it current>
- **Contents**: base UI elements, styles, routes, pages and components; a mock data store with seed data; no environment variables; no backend services
- **Refresh**: on request before a prototype round, not continuous
- **PM promises**: branches only, never a merge into the product; the branch is deleted once the decision record is written
```

## Ready-to-use template — Prototype decision record

```markdown
# Prototype — <feature>

- **Question it must answer**: <the one thing the PRD cannot decide without it>
- **Tier and why**: A / B / C, with the risk if wrong (money, security, data), the fidelity the question needs and the engineering cost tolerated
- **Participants and test plan**: <who, how many, task, date>
- **Result**: <the answer, with locators>
- **Feeds the PRD**: <section updated>
- **Disposal date**: <when the branch or link dies>
```

## Decision table

| The question is about | Risk if wrong | Fidelity needed | Tier |
|---|---|---|---|
| whether users understand a flow or a concept | low | approximate | A |
| whether a layout works with the real design system and its states | low | real components | B |
| how a change integrates with existing routes, data and permissions | medium | real codebase, mock data | B |
| copy, a setting, a flag default, a small UI tweak in existing components | low, reversible behind a flag | production | C |
| anything that moves money, touches auth or permissions, or changes a data model | high | production | never C: B to explore, engineering ships |

## From prototype to the stage-6 gate

"Prototype validated" in `skills/WORKFLOW.md` means the decision record's question has an answer with named participants and locators, not that a demo went well. The answer moves into the PRD (`references/prd-writing.md`: user flow, states, decision log). The kickoff pre-read item "Prototype link works + current" in `references/tech-team-kickoff.md` points at the tier A link or the tier B branch. A tier C change is delivery, not prototyping: it runs behind a flag with a rollback path per `pm-phase-deliver/references/launch-readiness.md`.

## Lock the loop in

When the same tier B loop repeats across features (same sandbox, same prompt shape, same review), write it down as a skill or a reference the team shares. Instructions that live in one PM's head are what this ladder exists to replace.

## Common anti-patterns

- **Demo mistaken for feasibility.** A hosted prototype proves nothing about the real components or data.
- **Merging the branch.** A tier B branch that ships becomes unreviewed production code.
- **PM as junior engineer.** Tier C on logic the team would have written differently.
- **Tier C without a flag or rollback.** A small change is still a release.
- **Polishing before the risk is resolved.** The "build-then-validate" failure named in `pm-phase-discover/references/opportunity-hypothesis.md`.
- **Sandbox as a second product.** A sandbox that drifts from the codebase answers questions about itself.

## Files

Decision record → `.ai/memory/projects/<slug>/prototypes/<feature>.md`, linked from `prds/<feature>.md`. Sandbox request → the same folder, once per product.
