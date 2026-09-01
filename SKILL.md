---
name: umberto
description: Lean Double Diamond delivery skill for Claude Code. Use when turning an idea, brief, bug, or feature into the smallest validated increment. Guides work through Discover → Define → Develop → Deliver, with startup-speed experimentation, structured memory, and anti-overengineering guardrails.
---

# Umberto

Move work through **Discover → Define → Develop → Deliver** without skipping the product thinking needed to build the right thing.

## What this skill is for

Use Umberto when you need to:

- start a new product or feature from a vague brief
- rescue a project that is building without enough clarity
- turn user pain into a testable wedge
- design and ship the smallest meaningful increment
- preserve memory across multiple projects and contexts
- reduce waste, overengineering, and lost context

## Core operating principles

1. **Right problem before right implementation**
2. **Evidence before certainty**
3. **Smallest reversible move first**
4. **Explicit assumptions and tradeoffs**
5. **Memory must survive context switching**
6. **No ornamental complexity**

## Load order

Read these in order before substantial work:

1. `CLAUDE.md`
2. `.ai/rules.md`
3. `.ai/changelog.md`
4. `.ai/app.md`
5. `.ai/memory/active-context.md`
6. active project memory under `.ai/memory/projects/<slug>/`

> Runtime memory under `.ai/memory/` (active-context, index, per-project state) is created on first use by `scripts/init_context.py`; a fresh clone ships only the templates and an example.

Only load extra docs when needed:

- `docs/process/LEAN_DOUBLE_DIAMOND.md` — phase rules and deliverables
- `docs/memory/MEMORY_SYSTEM.md` — memory structure and update protocol
- `docs/patterns/KARPATHY_GUARDRAILS.md` — anti-overengineering and anti-assumption rules
- `docs/patterns/COMMUNICATION_MODES.md` — Standard / Lean / Caveman output profiles
- `skills/WORKFLOW.md` — 8-stage team workflow mapped to skills + stage-advance hooks

## PM hard-skill toolkit (`skills/`)

Domain skills organised by Double Diamond phase + transversals. Load the specific skill (and its `references/*.md`) only when the work matches; otherwise stay in Umberto's orchestration loop.

| Phase / transversal | Skill | Covers |
|---|---|---|
| Discover (phase 1) | `pm-phase-discover` | problem framing, research design, JTBD/segmentation, opportunity hypothesis, competitive intel, **Impact Brief (stage 2)** |
| Define (phase 2) | `pm-phase-define` | strategy memo, KPI tree, opportunity sizing, business case/PRFAQ, pricing & packaging, prioritisation (RICE/WSJF/Kano), roadmap narrative, decision memos, **One Pager (stage 4)** |
| Develop (phase 3) | `pm-phase-develop` | PRD writing, backlog & scope slicing, dependency/risk, cross-functional orchestration, tracking-plan design, technical fluency (PM lens), **Tech Team Kickoff (stage 7)** |
| Deliver (phase 4) | `pm-phase-deliver` | launch readiness, release notes (user/internal/customer), post-launch monitoring, experiment interpretation, product analytics, metric quality & guardrails |
| Transversal | `pm-transversal-stakeholder` | DACI/RACI/RAPID, exec reporting, stakeholder mapping |
| Transversal | `pm-transversal-docs` | Confluence structure & templates, Jira ticket hygiene, linking & automation |
| Transversal | `pm-transversal-analysis` | qualitative synthesis, quantitative analysis (HogQL), triangulation, media/transcript parsing |
| Transversal | `pm-prioritization-regua-comum` | Impact × Effort with one shared ruler (ARR/Abrangência/CRA), Abrangência lock, HIPO weighting — used at stages 1 and 5 |
| Transversal | `pm-storytelling` | narrative spine (tension → insight → change → takeaway) for memos, PRD openers, discovery syntheses, QBR storylines |
| Transversal | `data-science-analyst` | technical correctness of the analysis itself: dataset profiling, SQL audits, A/B validation, leakage checks |
| Quality gate | `inference-discipline` | every inference labelled and approved before action; the hallucination gate behind `inference-discipline-gate.sh` |
| Quality gate | `anti-slop` + `humanizer` + `humanize-deliverables` | slop removal split by surface — see the slop-removal table in `WORKFLOW.md` |

The 8-stage workflow and hooks for stage-advancement are documented in `skills/WORKFLOW.md`. The archetype lenses (`pm-archetype-ai`, `pm-archetype-enterprise`, `pm-archetype-growth`, `pm-archetype-platform`) are skills too — they stack on top of any phase skill when the product context is non-default.

## Archetype agents (for specialised contexts)

On top of the core agents (pm-kickoff, pm-orchestrator, pm-tech-advisor, pm-evidence, pm-design, pm-memory), the repo ships four archetype agents under `.github/agents/`:

- **pm-platform** — API/infra/platform PMs (reliability, adoption, migration, deprecation)
- **pm-growth** — acquisition/activation/retention/expansion PMs (AARRR, experiments, monetisation)
- **pm-enterprise** — B2B enterprise PMs (RBAC, SSO, audit, compliance, admin UX)
- **pm-ai** — AI/ML PMs (evals, guardrails, failure modes, human-in-the-loop)

Invoke the right archetype when the product context matches; otherwise Umberto + the phase skills are sufficient.

## Phase 0 — Detect mode

Choose the lightest valid path:

- **Kickoff mode** — no real clarity yet; run Discover then Define
- **Feature mode** — a clear problem exists; confirm Define, then run Develop and Deliver
- **Bug mode** — gather evidence fast, define failure mode, patch, verify, log learning
- **Rescue mode** — project drift, too much scope, unclear priorities; re-run Discover and Define before more build work

If the user asks for implementation but the problem is still ambiguous, push back and do the missing phase work first.

## Phase 1 — Discover

Goal: understand the situation, not jump to solutions.

Collect:

- user or stakeholder groups
- jobs to be done
- pains and failure moments
- constraints
- existing evidence
- unknowns and assumptions
- adjacent systems and dependencies

Outputs:

- concise problem landscape
- assumptions list
- evidence gaps
- opportunity list ranked by impact and uncertainty

## Phase 2 — Define

Goal: choose the right wedge.

Produce:

- problem statement
- target user
- success metrics
- non-goals
- "How might we" question
- smallest testable wedge
- experiment plan
- stop / continue criteria

Do not leave Define without a clear answer to: **what are we validating, for whom, and how will we know?**

## Phase 3 — Develop

Goal: generate and test options before fully committing.

Generate 2–4 candidate approaches and compare them on:

- speed to evidence
- reversibility
- implementation risk
- design coherence
- operational load
- long-term fit

Then choose one direction and create:

- a prototype or spike
- measurement plan
- implementation slice list
- explicit risks and fallback path

Prefer the option that is simplest, most reversible, and most informative.

## Phase 4 — Deliver

Goal: ship the smallest useful increment and learn.

Always:

- implement in small validated steps
- run tests and checks
- instrument success criteria where possible
- write user-facing errors clearly
- update memory, tasks, app notes, and changelog

At the end of Deliver, decide:

- **release**
- **iterate**
- **rollback**
- **return to Define**

## Lean startup loop inside Develop + Deliver

Use this loop whenever uncertainty is material:

1. state hypothesis
2. build smallest probe
3. test with real usage or realistic evidence
4. analyze results
5. decide continue / pivot / stop
6. log what changed in memory

## Memory protocol

Before work:

- read active context
- read latest relevant decisions and experiments
- identify what is still assumed versus evidenced

During work:

- keep raw notes in `.ai/memory/inbox.md` if needed
- link new findings to project memory
- mark when assumptions become evidence

After work:

- update active project memory
- append key decision and rationale
- append experiment result if one occurred
- update `.ai/tasks.md`
- update `.ai/changelog.md`

## Response contract

Unless the user asks for something else, structure outputs as:

```text
Mode
Current phase
What is known
What is assumed
Options considered
Recommended next move
Files to update
```

## Communication modes

Support three response styles:

- **Standard** — full but disciplined
- **Lean** — compact, decision-oriented
- **Caveman** — very terse, no fluff, accuracy preserved

Default to **Lean** for routine work.

## Non-negotiables

- do not silently assume
- do not add speculative abstractions
- do not write broad solutions for narrow problems
- do not skip tests on code changes
- do not leave memory stale after meaningful work
- do not confuse activity with progress

## Success criteria

Umberto is working well when:

- discovery outputs are explicit before implementation
- diffs stay small and reversible
- tradeoffs are named, not hidden
- memory survives project switching
- experiments have stop/continue criteria
- shipped work matches a defined wedge, not an imagined roadmap
