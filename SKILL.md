---
name: umberto
description: Lean Double Diamond delivery skill for Claude Code and Codex. Use when turning an idea, brief, bug, or feature into the smallest validated increment. Guides work through Discover → Define → Develop → Deliver, with startup-speed experimentation, structured memory, and anti-overengineering guardrails.
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

Read the harness instructions and `.ai/rules.md` first. Then load context for the task:

1. `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex)
2. `.ai/rules.md`
3. For toolkit work, the relevant entries in `.ai/changelog.md`, `.ai/backlog.md`, and `docs/DECISIONS.md`
4. For product work, `.ai/memory/active-context.md`; resolve the slug before reading its files
5. Relevant project files under `.ai/memory/projects/<slug>/`

Runtime project memory is created on first use; a fresh clone ships only templates and an example. Bootstrap only when the task needs project memory. If the pointer is absent, do not invent a project or create one for a task that does not need it. Reuse already loaded guidance unless context was lost or freshness matters.

Only load extra docs when needed:

- `docs/process/LEAN_DOUBLE_DIAMOND.md` — phase rules and deliverables
- `docs/memory/MEMORY_SYSTEM.md` — memory structure and update protocol
- `docs/patterns/KARPATHY_GUARDRAILS.md` — anti-overengineering and anti-assumption rules
- `docs/patterns/COMMUNICATION_MODES.md` — Standard / Lean / Caveman output profiles
- `skills/WORKFLOW.md` — 8-stage team workflow mapped to skills + stage-advance hooks
- `skills/DOCTRINE.md` — calibrated disagreement: consult for difficult pushback or concession
- `docs/REPO_HEALTH.md` — the toolkit's own validation suite; run it before committing changes under `skills/`, `hooks/`, or `scripts/`

## PM hard-skill toolkit (`skills/`)

Domain skills organised by Double Diamond phase + transversals. Load the specific skill (and its `references/*.md`) only when the work matches; otherwise stay in Umberto's orchestration loop.

| Phase / transversal | Skill | Covers |
|---|---|---|
| Discover (phase 1) | `pm-phase-discover` | problem framing, research design, JTBD/segmentation, opportunity hypothesis, opportunity solution tree + assumption map (stage 3 → 4 bridge), competitive intel, **Impact Brief (stage 2)** |
| Define (phase 2) | `pm-phase-define` | strategy memo, KPI tree, opportunity sizing, business case/PRFAQ, pricing & packaging, problem prioritisation and validated-bet selection, roadmap narrative, decision memos, **One Pager (stage 4)** |
| Develop (phase 3) | `pm-phase-develop` | scope slicing (stage 5), PRD writing, prototyping ladder (stage 6), backlog structure, dependency/risk, cross-functional orchestration, tracking-plan design, technical fluency (PM lens), **Tech Team Kickoff (stage 7)** |
| Deliver (phase 4) | `pm-phase-deliver` | launch readiness, release notes (user/internal/customer), post-launch monitoring, experiment interpretation, product analytics, metric quality & guardrails |
| Transversal | `pm-transversal-stakeholder` | DACI/RACI/RAPID, exec reporting, stakeholder mapping, risk-selected review panel (non-blocking, before stages 4 and 6 reach stakeholders) |
| Transversal | `pm-transversal-docs` | Confluence structure & templates, Jira ticket hygiene, linking & automation |
| Transversal | `pm-transversal-analysis` | qualitative synthesis (single and batch), quantitative analysis (HogQL), triangulation, media/transcript parsing, connector task recipes (Jira/analytics MCP) |
| Transversal | `pm-transversal-comms` | executive email (SCQA), chat/Slack messages (BLUF), channel-fit rules (chat vs. email vs. doc vs. call) |
| Transversal | `pm-prioritization-regua-comum` | Impact × Effort with one shared ruler (Business impact / Abrangência / Strategic & risk), Abrangência lock, HIPO weighting — stage 1 problem ranking; stage 5 only when validated bets compete |
| Transversal | `pm-storytelling` | narrative spine (tension → insight → change → takeaway) for memos, PRD openers, discovery syntheses, QBR storylines |
| Transversal | `pm-product-sense` | BUILD (6-step decision framework) + EVALUATE (5-dimension rubric); mandatory non-blocking shadow evaluation at stages 4 and 6 |
| Transversal | `data-science-analyst` | technical correctness of the analysis itself: dataset profiling, SQL audits, A/B validation, leakage checks |
| Quality gate | `inference-discipline` | verify material claims, preserve uncertainty, and ask only for a real blocker or missing authorization; `inference-discipline-gate.sh` scans configured routes for five literal markers |
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

If materially different solutions remain after safe investigation, clarify the blocking choice before the dependent implementation. Continue independent work where possible.

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
- update the active project's durable memory and tasks when their state changes
- update toolkit backlog/changelog when toolkit status or history changes

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

Before project work that needs memory:

- read `.ai/memory/active-context.md` when it exists and resolve the slug before opening project files
- if the pointer is absent, do not invent a project; initialize only when durable project context is needed and its name is known
- read relevant decisions, experiments, and state
- when the warm set lacks a fact, search the cold layer grep-first (`memory.py index <slug>`, then the matching block); never read an archive wholesale
- identify material assumptions and evidence gaps

For toolkit work, use `.ai/backlog.md`, `.ai/changelog.md`, and `docs/DECISIONS.md` as relevant. A task without project context does not require creating project memory.

During work:

- keep raw notes in `.ai/memory/inbox.md` if needed (manual scratch; no script reads or writes it)
- link durable findings to project memory when relevant
- mark when assumptions become evidence

After work:

- record durable project changes, decisions, or experiment results in that project's memory
- update project tasks only when their status changes
- log toolkit changes in `.ai/changelog.md` and update `.ai/backlog.md` when toolkit task status changes
- a Stop hook (`hooks/memory-reminder.sh`) reminds you when files changed after the last log; it never blocks or writes the log

## Response contract

Match the response to the request and put the requested answer or artefact first. Include context, uncertainty, options, a recommendation, or file paths only when they affect the decision or are needed to use the deliverable. Do not force headings onto simple answers. Use Lean, Standard, or Caveman as described below without dropping material evidence or constraints.

## Communication modes

Support three response styles:

- **Standard** — full but disciplined
- **Lean** — compact, decision-oriented
- **Caveman** — very terse, no fluff, accuracy preserved

Default to **Lean** for routine work.

## Non-negotiables

- do not present material assumptions as verified facts
- do not add speculative abstractions
- do not write broad solutions for narrow problems
- do not skip tests on code changes
- update durable memory when project or toolkit state changes; do not create entries for transient work
- do not confuse activity with progress

## Success criteria

Umberto is working well when:

- discovery outputs are explicit before implementation
- diffs stay small and reversible
- tradeoffs are named, not hidden
- memory survives project switching
- experiments have stop/continue criteria
- shipped work matches a defined wedge, not an imagined roadmap
