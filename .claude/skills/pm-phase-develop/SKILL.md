---
name: pm-phase-develop
description: Lean Double Diamond **Develop phase** skill for PMs. Invoke when the wedge is defined and the team needs to convert it into **context-rich, executable work**: PRD writing, scope slicing, backlog structure, dependency & risk management, cross-functional orchestration, and the **measurement instrumentation** that must be in place before launch. Trigger on "write a PRD", "escreva a spec", "quebre esse épico", "quais dependências?", "tracking plan", "event schema", "instrumentation", "acceptance criteria", "feature flag strategy", or when the team is about to code without a measurement plan. Also covers the PM lens on technical fluency for software products. Bridges to `pm-phase-deliver` for post-launch monitoring and A/B interpretation.
---

# PM Phase — Develop

> Double Diamond Phase 3 of 4. Converts a defined wedge into executable work with explicit scope, acceptance, dependencies, instrumentation, and cross-functional alignment.

## When to use this skill

Invoke when:

- a wedge or initiative is defined and the team is about to start building
- a PRD, spec, or user-story set is needed
- an epic needs to be sliced into learning-rich increments
- dependencies across teams must be surfaced before they bite the timeline
- instrumentation must be designed *before* the code ships (not patched in after)
- cross-functional work (design + eng + analytics + legal + support) needs a shared plan
- a technical trade-off needs a PM lens (cost vs value vs reliability vs speed-to-learn)

Do NOT use for post-launch analysis or A/B result interpretation (→ `pm-phase-deliver`).

## Prime directive

**Executable work, not requirement novels.** Good requirement writing gives engineering and design **context and room to solve** — it does not over-prescribe, does not omit success criteria, does not let scope drift silently. Instrumentation is designed upfront because shipped code without the right events is shipped blindly.

## Core sub-skills

### 1. PRD and specification writing

Write concise, actionable product requirements: problem, target user, success criteria, scope & non-scope, trade-offs, open questions.

Outputs: PRD (1–5 pages), linked acceptance criteria, annotated flows, open-questions section, non-requirements.

Anti-patterns: novels, pixel-by-pixel UI dictation without need, omitting success criteria, leaving scope ambiguities unresolved, letting docs drift from reality.

→ Deep-dive: `references/prd-writing.md`

### 2. Backlog structuring and scope slicing

Break bets into increments that maximise **learning per week**. Strong PMs shape the grain size of delivery; the expert move is keeping options open while moving.

Outputs: story map, backlog hierarchy, MVP/MVC definition, staged rollout plan.

Anti-patterns: giant epics, backlog as dumping ground, confusing output granularity with customer value, slicing by component rather than user need.

→ Deep-dive: `references/backlog-scope-slicing.md`

### 3. Dependency and risk management

Surface cross-team dependencies, delivery risks, and assumption risks **before** they become schedule or quality problems. Maintain a RAID log that people actually read.

Outputs: dependency map, risk register, mitigation plan, escalation note, planning review summary.

Anti-patterns: hidden dependencies, no owners, optimism bias, raising blockers late, conflating likelihood with impact.

→ Deep-dive: `references/dependency-risk.md`

### 4. Cross-functional delivery orchestration

Coordinate design, engineering, analytics, research, legal, ops, support, and GTM so a product change lands coherently. Product value is realised through orchestration, not PM heroics.

Outputs: integrated plan, role map (RACI-lite), blocker log, stakeholder action list, launch-readiness review.

Anti-patterns: owning the "how" instead of enabling domain owners, reliance on heroics, meetings-as-artefact, escalating without options.

→ Deep-dive: `references/cross-functional-orchestration.md`

The stage-7 artefact this skill produces is the **Tech Team Kickoff** — see `references/tech-team-kickoff.md` for the 90-min agenda template (stage 7 of 8 in `.claude/skills/WORKFLOW.md`).

### 5. Tracking-plan design (pre-launch instrumentation)

Define what events, properties, and metrics must exist before code ships, so post-launch analysis and experiments are trustworthy. Design tracking plans alongside the PRD, not after.

Outputs: tracking plan, event schema, instrumentation spec, metric dictionary entry, implementation QA checklist.

Anti-patterns: event sprawl, inconsistent naming, tracking everything, no taxonomy owner, implementing events without first linking them to outcomes.

→ Deep-dive: `references/tracking-plan-design.md`

### 6. Technical fluency (PM lens)

Understand enough of architecture, APIs, data flows, constraints, observability, and feasibility to make sound product trade-offs *with* engineering — not out-engineer them.

Outputs: technical trade-off memo, API/flow diagram annotations, feasibility notes, non-functional requirement list.

Anti-patterns: cargo-cult jargon, promising incoherent solutions, ignoring NFRs, relying on eng to translate every technical implication into product language.

→ Deep-dive: `references/technical-fluency.md`

## Workflow

1. **Load context** — `.ai/memory/active-context.md`, PRD/spec if present, priorities from `pm-phase-define`, tracking plan if any.
2. **Classify the ask** — PRD, slicing, dependency/risk, orchestration, instrumentation, or tech fluency?
3. **Anchor on the wedge** — restate the problem + success criteria + non-goals from Define. If missing, loop back.
4. **Draft the smallest useful artefact** — PRD that fits on ~3 pages, not 20; tracking plan that tracks the 5 events that matter, not 50.
5. **Name dependencies and risks explicitly** — each with owner and mitigation.
6. **Persist** — PRD → `.ai/memory/projects/<slug>/prds/<name>.md`; dependencies → `.ai/memory/projects/<slug>/raid.md`; tracking plan → `tracking.md`.

## Output contract

```text
## [Artefact type] — [short title]

### Wedge recap
### Target user + success criteria
### Scope IN / OUT
### Acceptance criteria or event schema
### Dependencies + owners
### Risks + mitigations
### Open questions
### Files/tickets to produce downstream
```

## Integration

- Upstream: `pm-phase-define` (priorities, KPIs, strategy).
- Downstream: `pm-phase-deliver` (post-launch monitoring uses tracking plan).
- Transversais: `pm-transversal-docs` (PRD in Confluence, tickets in Jira), `pm-transversal-stakeholder` (getting sign-off).
- Cross-functional pairings: your engineering architecture partner for architecture trade-offs; your QA lead for acceptance-criteria stress-test; a code reviewer once a PR exists; your designer for UI scope.
- Archetype lenses (load when the product type warrants): `pm-archetype-ai` for probabilistic features, `pm-archetype-enterprise` for B2B / governance, `pm-archetype-growth` for funnel-shaped work, `pm-archetype-platform` for API/SDK/infra.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is the 1-page PRD + tracking plan + dependency list; Standard is the full PRD with open questions; Caveman is ticket-sized — problem, slice, metric, deps, risk.

## Success criteria

- engineering and design start without re-asking "what are we building and why?"
- scope changes are visible and costed, not silent
- post-launch analysis is possible because instrumentation was right the first time
- cross-functional partners know their slice + handoff by the time coding starts
- dependency surprises drop quarter over quarter
