# AGENTS.md

Lean registry for the Umberto agent system.

## Shared source of truth

All agents must treat these files as authoritative:

1. `.ai/rules.md`
2. `.ai/app.md`
3. `.ai/design.md`
4. `.ai/changelog.md`
5. `.ai/memory/active-context.md`
6. active project memory under `.ai/memory/projects/<slug>/`

## Repository memory files

| File or folder | Purpose |
|---|---|
| `.ai/memory/active-context.md` | Current project/context in focus |
| `.ai/memory/index.md` | Memory map across projects, people, and domains |
| `.ai/memory/inbox.md` | Raw notes waiting to be sorted |
| `.ai/memory/projects/` | Durable project memory |
| `.ai/memory/people/` | Stakeholder and collaborator notes |
| `.ai/memory/_templates/` | Reusable memory templates |

## Agents

### Core

| Agent | File | Purpose |
|---|---|---|
| Lang | `.github/agents/lang.agent.md` | Kickstarts a new project or re-frames a drifting one using Discover and Define |
| Umberto | `.github/agents/umberto.agent.md` | Main builder; runs work through Lean Double Diamond and ships validated increments |
| Torvalds | `.github/agents/torvalds.agent.md` | Architecture and tradeoffs; protects reversibility and codebase coherence |
| Margaret | `.github/agents/margaret.agent.md` | TDD, failure analysis, metric quality & experiment integrity |
| Rand | `.github/agents/rand.agent.md` | Design planning and review; keeps UX aligned with the design system |
| Mnemosyne | `.github/agents/mnemosyne.agent.md` | Memory steward; captures durable context, decisions, experiments, and retrieval hints |

### PM archetypes (load when the product context matches)

| Agent | File | Purpose |
|---|---|---|
| pm-platform | `.github/agents/pm-platform.agent.md` | Platform / API / infra PMs — reliability, adoption, abstraction, migration, deprecation |
| pm-growth | `.github/agents/pm-growth.agent.md` | Growth PMs — AARRR funnels, activation/retention, monetisation experiments |
| pm-enterprise | `.github/agents/pm-enterprise.agent.md` | Enterprise PMs — RBAC, SSO, audit, compliance, admin UX, procurement |
| pm-ai | `.github/agents/pm-ai.agent.md` | AI/ML PMs — evaluation suites, guardrails, failure modes, human-in-the-loop |

## PM skill toolkit

Agents load skills under `.claude/skills/` (see `SKILL.md` for the mapping). The 8-stage team workflow is in `.claude/skills/WORKFLOW.md`.

## Default orchestration

### New project
Lang → (pm-phase-discover) → Torvalds → Mnemosyne

### Feature or bug
Umberto → (pm-phase-develop) → Torvalds → Margaret → Rand (if UI) → (pm-phase-deliver on launch) → Mnemosyne

### Rescue / re-scope
Lang or Umberto → (pm-phase-discover / pm-phase-define as needed) → Torvalds → Mnemosyne

### Specialised context
Appropriate archetype (pm-platform / pm-growth / pm-enterprise / pm-ai) leads + core agents support.

## Agent conventions

Every agent should:

- name assumptions explicitly
- prefer the smallest meaningful change
- log learning that should survive the session
- avoid duplicating rules already defined elsewhere
- update memory when durable context changes

## Operating rules (summary)

This is a PM workspace, not a deployable app: no build, test, or deploy step.

- **Editable**: `.claude/skills/`, `.claude/hooks/`, `scripts/`, `docs/`, `.ai/*.md`, `.ai/memory/_templates/`.
- **Off-limits without explicit OK**: `.ai/memory/projects/**/data`, `**/raw-evidence/`, any `people/` notes (PII).
- **Safe**: `git status`, `git ls-files`, `rg --files`, `python3 scripts/stage_context.py`, `python3 -m py_compile scripts/*.py`, `git check-ignore -v <path>`.
- **OK per command**: history/remote-rewriting git, `rm` of tracked files, deleting memory, publishing to Slack / Jira / Confluence.
- Run `repo-doctor` before committing under `.claude/`. Output: separate verified fact / inference / needs-confirmation.
