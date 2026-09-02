# Quality rubric

Score each dimension 1–5 before finalising complex outputs. Skip the scorecard for trivial requests where the user only wants the final story.

## 1. Assignment alignment

1 — Does not answer the assignment
3 — Addresses the topic but misses constraints or criteria
5 — Directly satisfies objective, deliverable, audience, and rubric

## 2. Narrative spine

1 — No clear story arc
3 — Has structure but weak tension or takeaway
5 — Clear protagonist, friction, turning point, takeaway — passes the spine sentence test

## 3. Specificity

1 — Generic and abstract
3 — Some concrete details
5 — Vivid, relevant details from the source, no filler

## 4. Evidence integrity

1 — Invents or overclaims
3 — Mostly grounded but has unsupported claims
5 — Uses only provided information; gaps marked clearly with `[NEEDS SOURCE]` or `[NEEDS METRIC]`

## 5. Audience fit

1 — Tone and depth mismatched
3 — Mostly appropriate
5 — Feels tailored to the actual reader, viewer, or evaluator

## 6. Format fit

1 — Wrong structure or length
3 — Close but needs formatting work
5 — Matches requested format, length, and delivery channel

## 7. Memorability

1 — Forgettable or cliché
3 — One useful idea but little emotional pull
5 — Strong contrast, image, example, or final line

## Minimum bar

Do not deliver final work below:

- 4 in Assignment alignment
- 4 in Evidence integrity
- 3 in Narrative spine

If any score is below the minimum, revise — or ask for missing source details rather than papering over the gap.

---

## Pre-delivery gate (outbound prose only)

Before any artefact ships outside the immediate team, the following two items are **binary pre-requisites**, not scored. Both must be checked.

| Gate | Required when | How |
|---|---|---|
| `humanizer` pass run | Voice quality matters: long-form, exec-facing, customer-facing, public-facing | Read `../../humanizer/SKILL.md`, apply its pattern catalogue, and run its mandatory final pass ("what still makes this AI-generated?") |
| `humanize-deliverables` mark applied | The artefact will be sent via the publish/send MCP tools (Confluence, Slack, customer email, Jira comments) | Read `../../humanize-deliverables/SKILL.md` and apply step 6 (sentinel marking). The hook hard-blocks the call without it. |

Skip both gates only for: internal scratchpads, `.ai/memory/` updates, raw machine output, code/config, structured ticket fields. When in doubt, run them — the cost is seconds.

If the artefact is outbound and either gate is unchecked, the work is **not** done — regardless of how high it scores on dimensions 1–7.
