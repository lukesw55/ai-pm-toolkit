# ai-pm-toolkit

A Claude Code operating system for product managers. It turns a vague idea into a shipped increment through four disciplined phases, keeps durable memory across projects, and enforces output quality with runtime hooks instead of good intentions.

This is the company-agnostic core of a working PM toolkit: the skills, agents, hooks, and doctrine I use day to day, with the employer-specific stack and customer evidence stripped out.

## What it is

The toolkit runs work through **Discover → Define → Develop → Deliver** (Lean Double Diamond) with three things most prompt collections skip:

- **Anti-overengineering guardrails** so the model builds the smallest useful slice, not the largest possible one.
- **Structured cross-project memory** so context survives switching between projects and sessions.
- **Runtime enforcement hooks** that block AI-slop prose, unverified claims, and scope bloat before they reach the repo, instead of trusting the model to behave.

## Why it exists

LLM coding agents default to plausible-but-bloated output: speculative abstractions, defensive checks at internal boundaries, confident claims about things they never verified, and prose that reads like a press release. For a PM driving an agent, that failure mode is expensive, because you are accountable for what ships and for what you tell stakeholders.

This toolkit encodes the corrections as reusable skills and as hooks the harness runs automatically. The model does not get to opt out.

## The four phases

| Phase | Skill | Covers |
|---|---|---|
| Discover | `pm-phase-discover` | problem framing, research design and synthesis, JTBD and segmentation, opportunity hypotheses, competitive intel, impact brief |
| Define | `pm-phase-define` | strategy memo, KPI tree, opportunity sizing, business case and PRFAQ, pricing, prioritisation (RICE/WSJF/Kano), roadmap narrative, decision memo (DACI), one-pager |
| Develop | `pm-phase-develop` | PRD writing, scope slicing, dependency and risk management, cross-functional orchestration, tracking-plan design, tech-team kickoff |
| Deliver | `pm-phase-deliver` | launch readiness, release notes, post-launch monitoring, A/B interpretation, product analytics, metric quality |

Transversal skills apply at every phase:

- `pm-transversal-stakeholder` — DACI/RACI/RAPID, exec reporting, stakeholder mapping
- `pm-transversal-docs` — Confluence structure, Jira hygiene, linking and automation
- `pm-transversal-analysis` — qualitative synthesis, quantitative analysis, triangulation, transcript parsing
- `pm-prioritization-regua-comum` — an Impact × Effort × Confidence prioritisation rubric
- `pm-storytelling` — narrative spine for one-pagers, memos, and launch comms
- `data-science-analyst` — the technical lens: audit a dataset, validate SQL, check for leakage, sanity-check an A/B test or a baseline model

Each skill ships a `SKILL.md` plus a `references/` folder with ready-to-paste templates, and most carry an `evals/` set so the skill can be graded rather than trusted.

## Archetype agents

`.github/agents/` holds four PM archetypes for non-default contexts, on top of the six core agents:

- **pm-platform** — APIs, reliability, adoption, abstraction quality, migration, deprecation
- **pm-growth** — AARRR funnels, activation, retention, monetisation experiments
- **pm-enterprise** — RBAC, SSO, audit, compliance, admin UX, procurement
- **pm-ai** — eval suites, guardrails, failure modes, human-in-the-loop

## Quality enforcement (the interesting part)

Three concerns are enforced at runtime by hooks in `.claude/hooks/`, wired through `.claude/settings.json`:

- **anti-slop** (`anti-slop-gate.sh`, `scope-bloat-gate.sh`) — blocks forbidden file artefacts, banner comments, decorative emoji headings, and replies with em-dash density, label-colon runs, or scope bloat.
- **inference-discipline** (`inference-discipline-gate.sh`) — blocks content that smuggles an inference in as fact. Every claim about external state must be verified or explicitly tagged. The matching skill makes the agent pause and ask for approval before acting on inferred intent.
- **humanize-deliverables** (`humanize-gate.sh`) — blocks publishing AI-tinted prose to Confluence, Slack, or Jira until a `humanizer` pass has run, tracked by a per-content sha256 sentinel.

Each gate has an explicit, per-content override for legitimate exceptions, so the enforcement is strict without being a dead end.

## Memory

Project memory is layered so it never floods the context window:

- **Hot** — a capped pointer plus the active project, injected at session start
- **Warm** — a project's kickoff, state, decisions, and recent changelog, read only when working on it
- **Cold** — archives, raw evidence, transcripts, never read wholesale

Writing memory goes through `scripts/memory.py` (`log`, `park`, `activate`, `distill`, `doctor`), which rotates old changelog entries into archives and keeps the pointer under its size cap. PII and raw-evidence paths are never rotated, distilled, or ingested. The shipped tree contains only the templates, so a fresh clone bootstraps its own memory.

## Install

Clone into your Claude Code skills directory:

```bash
git clone https://github.com/lukesw55/ai-pm-toolkit.git ~/.claude/skills/ai-pm-toolkit
```

Then in Claude Code, invoke any skill by name (for example `pm-phase-discover`), or run the orchestration entrypoint described in [`SKILL.md`](SKILL.md). The orchestrator is a skill codenamed **Umberto**: it detects the working mode, sequences the four phases, and loads the right skill at each stage.

## Quickstart

```bash
# 1. Bootstrap a project context
python scripts/init_context.py my-product

# 2. Fill in .ai/app.md and the project profile under .ai/memory/projects/my-product/

# 3. In Claude Code:
#   We are starting my-product. Read the context files.
#   Run Discover and Define. Ask only the highest-leverage missing questions.
#   Create an experiment plan for the smallest viable proof. Update memory when done.
```

## Repository layout

```text
.
├── SKILL.md                 # orchestration entrypoint (the four-phase loop)
├── CLAUDE.md                # working doctrine and guardrails
├── AGENTS.md                # agent registry
├── .claude/
│   ├── settings.json        # hook wiring
│   ├── hooks/               # anti-slop, inference-discipline, humanize, scope-bloat, project-isolation
│   └── skills/
│       ├── WORKFLOW.md      # 8-stage workflow mapped to skills
│       ├── pm-phase-*/      # the four phases
│       ├── pm-transversal-*/, pm-prioritization-*/, pm-storytelling/
│       ├── pm-archetype-*/  # platform / growth / enterprise / ai
│       ├── anti-slop/, humanizer/, humanize-deliverables/, inference-discipline/
│       ├── data-science-analyst/
│       └── repo-doctor/
├── docs/                    # Lean Double Diamond, memory model, guardrails, comms modes
├── scripts/                 # memory.py, stage and context tooling
├── .ai/                     # generic project-brief templates + memory skeleton
└── .github/agents/          # 6 core agents + 4 PM archetypes
```

## Communication modes

Skills support three output profiles (see [`docs/patterns/COMMUNICATION_MODES.md`](docs/patterns/COMMUNICATION_MODES.md)): Standard for full analysis and stakeholder docs, Lean for routine work (the default), Caveman for token-constrained sessions.

## License

MIT. See [LICENSE](LICENSE).
