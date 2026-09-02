---
name: pm-transversal-stakeholder
description: Cross-phase skill for **stakeholder alignment, decision-rights design, and executive-ready reporting** — the hard-skill version of "stakeholder management". Invoke whenever multiple functions or leaders must converge on a decision, when "who decides what" is unclear, when an exec review/QBR is due, when a recommendation memo is needed, or when an escalation is being prepared. Trigger on "align stakeholders", "alinhe com time X", "exec review", "QBR", "write a memo for leadership", "DACI", "RACI", "escalation", "decision rights", "status report", "quem decide?", "briefar o diretor". Works across all Double Diamond phases. Produces DACI pages, stakeholder maps, exec memos, review packs, and escalation notes.
---

# PM Transversal — Stakeholder alignment, decision-rights, exec reporting

> Transversal skill — useful in every Double Diamond phase whenever humans must converge on a decision. Complements the phase skills with explicit decision-architecture artefacts.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke when:

- a decision involves more than 2 functions or 1 level of seniority above the PM
- "who decides?" is unclear or has drifted
- an executive review or QBR is being prepared
- a recommendation memo is needed (one-way vs two-way door framing)
- an escalation is imminent — and needs to be clean, not messy
- status reporting is absorbing too much time for too little decision-value
- a DACI, RACI, or RAPID needs to be designed or updated

Skip for decisions that are genuinely within PM authority and can be made in a PRD or decision log (→ `pm-phase-define/references/decision-memo-daci.md` for the artefact template itself).

## Prime directive

**Stakeholder management becomes a hard skill only when it produces concrete structures that reduce ambiguity and latency.** "I had a meeting with X" is not alignment. A named driver, an approver, a decision date, and a written recommendation is alignment.

## Core sub-skills

### 1. Stakeholder mapping and decision-rights design

Explicitly define who **drives, approves, contributes, and is informed** for important product decisions. Time-box decision windows. Document decision forums.

Outputs: DACI page, RACI matrix, stakeholder map (influence × interest), decision calendar, escalation protocol.

Anti-patterns: inviting everyone without clarifying roles, endless consultation, changing decision-maker mid-stream, status-sharing mistaken for alignment.

→ Deep-dive: `references/decision-rights-daci.md`

### 2. Executive-ready reporting and operating reviews

Translate product work into concise reporting that clarifies outcomes, trade-offs, risks, asks, and next decisions for senior stakeholders.

Outputs: executive memo, review deck (exception-based), KPI scorecard, portfolio recommendation note, decision/ask summary.

Anti-patterns: traffic-light reports without decisions, presenting too much detail, reporting outputs instead of outcomes, burying the ask or risk.

→ Deep-dive: `references/exec-reporting.md`

### 3. Stakeholder mapping (tactical)

Who are the stakeholders for this specific decision/initiative, what do they need to know/decide, what are their constraints and incentives, and how should they be engaged (sync/async, depth/summary)?

Outputs: stakeholder map, engagement plan, FAQ anticipating concerns, escalation ladder.

Anti-patterns: treating stakeholders as a single undifferentiated group, engaging everyone at the same depth, no plan for dissent.

→ Deep-dive: `references/stakeholder-mapping.md`

## Workflow

1. **Load context** — the decision at stake, the phase it's in, and existing `.ai/memory/projects/<slug>/decisions.md` entries.
2. **Classify the ask** — decision rights, exec reporting, or stakeholder map?
3. **Name the driver and approver explicitly** — no "TBD", no "we'll figure it out".
4. **Frame one-way vs two-way door** — the rigor required scales with reversibility.
5. **Write the recommendation before the meeting** — meetings are for friction, not for drafting.
6. **Persist** — decision artefact → `.ai/memory/projects/<slug>/decisions.md`; stakeholder map → `stakeholders.md`; exec memo → `.ai/memory/projects/<slug>/exec-memos/<topic>.md`.

## Output contract

```text
## [DACI / Exec memo / Stakeholder map]

### Decision at stake
### One-way or two-way door
### Roles
- Driver: ...
- Approver: ...
- Contributors: ...
- Informed: ...
### Recommendation (1 paragraph)
### Options considered
### Trade-offs and risks
### Ask (what we need from whom, by when)
### Decision date
### Memory updates
```

## Integration

- Every phase: `pm-phase-discover`, `pm-phase-define`, `pm-phase-develop`, `pm-phase-deliver` all need decision-rights clarity at key moments.
- Paired: `pm-transversal-docs` (DACI published in Confluence), `pm-phase-define/references/decision-memo-daci.md` (template).
- Agents: invoked implicitly by every agent when cross-function decisions arise; explicitly by `@pm-orchestrator` and archetype agents for launch decisions, pricing changes, deprecation decisions, etc.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is a 1-page DACI + recommendation; Standard is the full memo with options and trade-offs; Caveman is a 4-line driver / approver / ask / date.

## Success criteria

- decisions are made by named people within declared windows
- meetings leave with decisions, not "we'll sync again"
- exec reports prompt decisions, not information dumps
- escalations are clean: one memo, two options, one recommendation
- stakeholder surprises drop quarter over quarter
