# Decision memo / DACI / ADR

## What it is

Writing documents that make a **recommendation explicit**, clarify trade-offs, and enable informed asynchronous decision-making. Strong senior PMs work through written alignment, not through meetings.

## When to use which form

| Form | Use when | Key artefact |
|---|---|---|
| **Decision memo** (narrative) | One-off decisions with multiple options and stakeholders | 1–3 page memo with recommendation |
| **DACI** (role-first) | Multi-function decisions that need role clarity | DACI page in Confluence |
| **ADR** (Architecture Decision Record) | Technical/product decisions worth preserving long-term | Short, numbered, immutable record |
| **PRFAQ** | Major bets requiring outcome-first exec alignment | See `business-case-prfaq.md` |
| **Comment on ticket/PR** | Small, low-impact, easily reversible | Written in-place |

## Ready-to-use template — Decision memo

```markdown
# Decision memo — [topic] — [date]

**Status:** Draft | In review | **Decided** | Superseded by [memo X]
**Decision type:** one-way door | two-way door
**Driver:** @name
**Approver:** @name (or DACI link)
**Target decision date:** YYYY-MM-DD
**Cross-links:** PRD / strategy / discovery / sizing / stakeholder map

## TL;DR
One paragraph: what's decided (or what we recommend), why, and what changes as a result.

## Context
What prompted this decision. Evidence and constraints. 3–6 sentences.

## Options considered
### Option A — [name]
- description:
- pros:
- cons / risks:
- cost (effort + ongoing):
- reversibility:

### Option B — [name]
- ...

### Option C — [name]
- ...

## Recommendation
Option [X]. Rationale in 1 paragraph. What specifically this optimises for, and what we accept giving up.

## Trade-offs (explicit)
- we prioritise [value] over [value]:
- we accept [cost] because [reason]:

## Dependencies + risks
- depends on:
- risks:
- mitigations:

## Ask (what we need from whom, by when)
- [approver]: approve recommendation by [date]
- [eng]: feasibility confirmation by [date]
- [PMM]: GTM input by [date]

## How we'll know this was a good decision
Outcome criteria to revisit in N weeks/months.

## Refresh trigger
What would force a re-look (new data, failed assumption).

## Discussion log
- [date] [commenter]: [concern / input]
- [date] [commenter]: [concern / input]
```

## Ready-to-use template — DACI page

```markdown
# DACI — [decision title] — [date]

**Status:** Decision pending | **Decided** | Implemented

## Decision at stake
One sentence: the question being decided.

## One-way or two-way door
- reversibility:
- cost of being wrong:

## Roles
- **Driver:** @name (owns the process, ensures decision happens on time)
- **Approver:** @name (final say; typically one person)
- **Contributors:** @names (bring expertise; consulted before decision)
- **Informed:** @names (told after decision; no input needed)

## Recommendation (1 paragraph)
From the Driver.

## Options
- Option A — [1-line]
- Option B — [1-line]
- Option C — [1-line]

Link to decision memo for deeper context.

## Trade-offs and risks
Short list. Read in 2 minutes.

## Open questions
Things contributors must answer before approver signs off.

## Decision + date
- decided: [option]
- date: YYYY-MM-DD
- approver signature: @name

## Follow-up actions
- [ ] communicate to [informed list]
- [ ] update related docs ([links])
- [ ] create implementation tickets
```

## Ready-to-use template — ADR

Short, numbered, immutable.

```markdown
# ADR-[NNN] — [short title]

**Status:** Proposed | **Accepted** | Superseded by ADR-MMM
**Date:** YYYY-MM-DD
**Deciders:** @names

## Context
Why we need a decision here. 2–4 sentences.

## Decision
What we decided. Present tense.

## Consequences
- positive:
- negative:
- neutral / trade-offs:

## Alternatives considered (brief)
- [alt] — rejected because [reason]
```

ADRs are append-only. When superseded, mark the old one "superseded by ADR-MMM" and create a new one — don't overwrite.

## Writing discipline

- **Recommendation first.** Exec scan-ability requires TL;DR + recommendation in the first page.
- **Options with honest cons.** If Option B has no listed cons, the analysis is weak.
- **Trade-offs on the record.** "We prioritise X over Y" must be explicit, not implied.
- **One-way vs two-way door labelled.** Exec time is scarce; it should scale to reversibility.
- **Ask is specific.** "Approve by Friday" beats "thoughts?"
- **Done means decided.** Mark status. Update related docs. Close the loop.

## Common anti-patterns

- **Status-as-decision.** "Here's what's happening" without a recommendation = not a decision memo.
- **Hidden trade-offs.** The decision looks costless on paper → nobody believes it.
- **Burying the ask.** Reader reaches the bottom without knowing what's expected of them.
- **Endless consultation.** DACI without time-boxing decays into permanent "in review".
- **Silent superseding.** New decision contradicts old one; the old one is still the first Google result.
- **Meeting substitutes for writing.** "We'll discuss it in the sync" → nothing recorded, re-argued next quarter.

## Seniority signals

- **Beginner:** documents outcomes after discussion.
- **Intermediate:** writes clear recommendations on one decision stream.
- **Advanced:** uses writing to drive alignment *before* meetings and unblocks senior stakeholders async.
- **Expert:** creates a culture of crisp written decisions — institutional memory compounds.

## Files

`.ai/memory/projects/<slug>/decisions.md` (log) + `decisions/<topic>-<date>.md` (individual memos) + `daci/<topic>.md`. Follow the existing `.ai/memory/_templates/decision-log.md` template for consistency.
