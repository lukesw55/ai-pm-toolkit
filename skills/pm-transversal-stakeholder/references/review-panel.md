# Review panel — five lenses before real stakeholders see the artefact

## What it is

A structured pre-review of a stage-4 one-pager or a stage-6 PRD through five stakeholder lenses: commercial, customer success, marketing and positioning, exec and finance, user advocate. Each lens answers one question, "what would make me object, and what evidence would settle it", and returns either an objection with its evidence gap and an owner, or "no objection" with a one-line reason. The technical and evidence lenses are not on the panel because they already exist: `.github/agents/pm-tech-advisor.agent.md` and `.github/agents/pm-evidence.agent.md` where the harness runs agents, `pm-phase-develop/references/technical-fluency.md` and `inference-discipline/SKILL.md` everywhere else.

## Why it matters

The recommendation is written before the meeting (`references/stakeholder-mapping.md`), so the exposures a real stakeholder would raise should be found before the meeting too. The panel finds the unexamined commercial, support, positioning, financial or user exposure while the artefact is still cheap to change. The risk runs the other way as well: a reviewer told to represent a persona will invent an objection to look useful. The rule below exists for that.

## The rule that makes it safe

**No objection is a valid output. A manufactured objection is a doctrine failure.** Calibrated disagreement (`../../DOCTRINE.md`, behaviour 7) agrees when the premise is sound instead of inventing an objection to look critical; the panel is that behaviour applied per lens. An objection counts only when it names the evidence gap that would resolve it and the owner who could close it. A lens with nothing to object says so in one line and stops.

## Lens cards

Each card has four fields: what I optimise for, what would make me object, the evidence I would ask for, and the false objection I must not raise.

| Lens | Optimises for | Would object when | Evidence asked for | False objection to refuse |
|---|---|---|---|---|
| Commercial | revenue, pricing integrity, deal risk, the renewal base | the change touches price, discounts, contract terms or a committed deal without a number attached | accounts affected, revenue at risk or gained, the sales-ops or finance owner's read | "sales will want X" with no named account or number |
| Customer success | ticket load, onboarding, churn signals | the change adds support surface, breaks a playbook or removes a path customers rely on | ticket categories touched, playbook status, the support lead's read | "users will be confused" with no test behind it |
| Marketing and positioning | message, category, competitive response | the change alters what we claim or hands a competitor a story (`.ai/memory/org/competitors.md` when present) | the positioning line affected, the competitor move it invites | "this needs a launch" for an internal change |
| Exec and finance | fit with the cycle's objectives, cost, opportunity cost | the artefact serves no objective in `.ai/memory/org/goals.md`, or hides a cost or a dependency | the objective it moves, the cost line, what it displaces | a strategic-sounding restatement of the artefact |
| User advocate | the job to be done, harm, accessibility | the artefact serves the buyer and not the user, or a persona in `.ai/memory/org/personas.md` loses a path | the persona and locator affected, the harm scenario | speaking for users without a locator |

## Ready-to-use template — Panel report

```markdown
# Panel report — <artefact> (stage <4|6>)

- **Lenses run**: commercial, customer success, marketing, exec, user advocate
- **Date / author**: <date> / <role>

| Lens | Verdict | Reason (one line) | Evidence gap | Owner |
|---|---|---|---|---|
| Commercial | objection / no objection | ... | ... | ... |
| Customer success | ... | ... | ... | ... |
| Marketing | ... | ... | ... | ... |
| Exec / finance | ... | ... | ... | ... |
| User advocate | ... | ... | ... | ... |

## Consolidation
- objections carried into the dissent protocol: ...
- unverified claims added to the assumption map: ...
- verdict: non-blocking; the formal gate is unchanged
```

## When to run

Before a stage-4 one-pager or a stage-6 PRD reaches the people it names, as a companion to the `pm-product-sense` shadow evaluation in `skills/WORKFLOW.md`: product sense scores the judgement in the artefact, the panel predicts the reaction to it. Never for decisions inside the PM's own authority, and never as a gate: the panel informs the author, it does not approve.

## How to run

Default: one session, lens by lens, each card's verdict written before the next card is opened, so a later lens cannot soften an earlier one. Where the harness offers subagents, one per lens in parallel with the same card and the same report contract, then the lead consolidates. Codex subagent support is not verified in this repo; run the lenses sequentially there. Digest rule from `inference-discipline/SKILL.md`: a lens's output is evidence only for what that lens verified, and an objection that cites a number the lens did not read is itself an inference to mark, not a finding.

## Consolidation

- Objections go to the dissent protocol in `references/stakeholder-mapping.md`, on the DACI page, in the same sentence form a real stakeholder's dissent would take.
- Claims the panel could not verify become assumption rows in the tree (`pm-phase-discover/references/opportunity-solution-tree.md`), each with a test or an accepted-risk decision.
- The author decides what changes. The panel never blocks, never re-runs until the answer changes, and never replaces the real stakeholders it rehearses.

## Common anti-patterns

- **Manufactured objection.** A reservation with no evidence gap, raised so the lens looks thorough.
- **Persona cosplay.** Writing in a stakeholder's voice instead of applying their criteria.
- **Panel as gate.** Holding the artefact until every lens is silent.
- **Only the convenient lenses.** Skipping the commercial or finance lens because the author expects them to object.
- **Objection without an evidence gap.** "Risky" with no statement of what would settle it.
- **Re-running until the answer changes.** Shopping for a clean report.

## Files

Panel report → `.ai/memory/projects/<slug>/reviews/<artefact>-panel-<date>.md`. Objections → `decisions.md` through the dissent protocol. Unverified claims → the assumption map of the opportunity tree.
