# ai-pm-toolkit

Product management skills, workflow orchestration, and project memory for Claude Code and Codex.

For PMs and product builders using a coding agent to frame problems, prioritise opportunities, write PRDs, plan experiments, and prepare launches. The toolkit gives the agent reusable methods and keeps project context, evidence gaps, and decisions in files between sessions.

Start with a specific task or let the orchestrator select a path from discovery to delivery. You review the artefacts and decisions as the work progresses.

## Quick start

### Set up your workspace

You need a working Claude Code or Codex installation, bash, Python 3.10+, `jq`, `git`, and either `sha256sum` or `shasum -a 256`.

The setup below uses this repository as your PM workspace:

```bash
git clone https://github.com/lukesw55/ai-pm-toolkit.git
cd ai-pm-toolkit
bash scripts/check_requirements.sh
python3 scripts/validate_repo.py
python3 scripts/init_context.py "my-product"
```

The checks verify local requirements and repository structure. The final command creates project memory and makes `my-product` active, initially at the Discovery stage.

Open the cloned repository in Claude Code or Codex. Claude Code reads the project configuration. In Codex, run `/hooks` to trust the hooks by content hash; repeat after editing `hooks/*.sh` or `.codex/hooks.json`.

### Run your first task

Paste this example request, or replace its product context with your own:

```text
Read SKILL.md and the active memory for my-product.

Our team is considering onboarding tooltips. We have no research
or funnel data yet. Use pm-phase-discover to draft a research plan
that tests whether new users face a problem worth solving.

Separate hypotheses from evidence. Ask for the user segment and
the decision we need to make before filling in missing details.

Save the plan to .ai/memory/projects/my-product/research-plan.md.
Update project memory with what we know and what remains unknown.
```

Open the saved plan and review the research questions, method, and evidence gaps before moving on to solution design. Unfilled project fields remain unknown; the agent should ask for missing context rather than invent it.

To resume later, ask the agent to read `SKILL.md` and the active project's memory before continuing.

## How it works

### Workflow and skills

Umberto, the root [SKILL.md](SKILL.md), selects a working mode: Kickoff for an unclear brief, Feature for a defined problem, Bug for a failure to investigate, or Rescue for a project that needs reframing.

It sequences four phases:

| Phase | Work |
|---|---|
| Discover | Frame the problem, gather evidence, and map opportunities |
| Define | Choose a direction, define success, and record trade-offs |
| Develop | Slice scope, write the PRD, prototype, and plan measurement |
| Deliver | Prepare the launch, monitor outcomes, and interpret results |

The [team workflow](skills/WORKFLOW.md) maps these phases to eight stages, from Discovery Prioritization to Delivery, with deliverables and review criteria. Evidence can justify returning to an earlier stage or skipping one with a recorded rationale. Moving the stage pointer does not validate an artefact or approve a decision.

Each skill defines its method in a `SKILL.md`. Most include a progressive-loading map, such as the [discovery reference map](skills/pm-phase-discover/references/progressive-loading.md), that directs the agent to the reference needed for the task, such as research design, PRD writing, or launch readiness. This is progressive loading: instructions select supporting material as work requires it.

Phase skills can be combined with stakeholder, analysis, documentation, and communication skills. AI, enterprise, growth, and platform lenses add domain-specific concerns.

### Project memory

The active project pointer and project index are injected at session start; the current workflow stage is injected on each prompt. The agent reads project state, decisions, and recent changes when working on that project. Older entries are retrieved through an archive index, then selected blocks.

Memory updates depend on the agent following its instructions. A session-close hook reminds it to log changed work, without blocking the session.

Use `memory.py` to record work or switch projects:

```bash
python3 scripts/memory.py log my-product "Research plan drafted; user segment still unknown."
python3 scripts/memory.py park my-product
python3 scripts/init_context.py "second-product"
```

The log command records an entry; it does not establish that the claim is true. Parking preserves the current context before another project becomes active. Initialisation refuses to replace a different active project.

The [memory guide](docs/memory/MEMORY_SYSTEM.md) covers reactivation, shared organisation context, archives, and legacy migration. Runtime project memory is gitignored in the upstream repository.

### Quality checks and evals

Skills guide the agent's work. Four blocking hooks enforce specific checks on configured tool calls or at the end of a reply:

| Hook | Checks |
|---|---|
| `anti-slop-gate.sh` | Configured writes: unsolicited PLAN/SUMMARY/NOTES files, banner comments, and decorative emoji headings |
| `inference-discipline-gate.sh` | Configured writes and publishes: five literal unresolved inference markers |
| `humanize-gate.sh` | Listed Confluence, Jira, and Slack publish tools: a humanizer marker matching the exact content |
| `scope-bloat-gate.sh` | Final replies: scope and structural patterns, including excess length for short requests |

These checks do not establish factual accuracy or semantic writing quality. Shell writes bypass the write gates, and each gate has an explicit per-content override. The [hook contract](hooks/contract.json) specifies the routes; [SECURITY.md](SECURITY.md) explains their boundaries.

Each skill also has an `evals/evals.json` manifest. The grader compares recorded outputs with and without the skill, assertion by assertion, and incorporates human labels where available. Fixtures test the grader's discrimination; they do not measure skill effectiveness.

The repository has not published measured skill-effectiveness results. Recording, grading, labelling, and reviewing disagreements are documented in the [eval protocol](docs/EVAL_PROTOCOL.md).

## Claude Code and Codex

Both use the canonical `skills/` and `hooks/`. Skills are mirrored into each agent's discovery directory; separate configuration files wire the shared hooks.

| Component | Claude Code | Codex |
|---|---|---|
| Session instructions | [CLAUDE.md](CLAUDE.md) | [AGENTS.md](AGENTS.md) |
| Hook configuration | [.claude/settings.json](.claude/settings.json) | [.codex/hooks.json](.codex/hooks.json) |
| Generated skill mirror | `.claude/skills/` | `.agents/skills/` |

Codex's `apply_patch` calls pass through an adapter that normalises them for the shared write gates. The project-isolation warning is Claude Code-only.

Other documented differences include sequential fallbacks where Codex subagent support has not been verified, and an optional presentation-rendering step that depends on a Claude-only skill. Read `AGENTS.md` for these limitations and the agent registry.

The mirrors are committed, so the quick start does not require regenerating them.

## Choose a task

Ask the orchestrator to select skills, or name one in your request.

| Task | Skill |
|---|---|
| Frame a problem or design research | [pm-phase-discover](skills/pm-phase-discover/SKILL.md) |
| Prioritise opportunities or write a one-pager | [pm-phase-define](skills/pm-phase-define/SKILL.md) |
| Draft a PRD, slice scope, or design a tracking plan | [pm-phase-develop](skills/pm-phase-develop/SKILL.md) |
| Prepare a launch or interpret an experiment | [pm-phase-deliver](skills/pm-phase-deliver/SKILL.md) |
| Synthesise interviews or triangulate evidence | [pm-transversal-analysis](skills/pm-transversal-analysis/SKILL.md) |
| Design evaluations for an AI product | [pm-archetype-ai](skills/pm-archetype-ai/SKILL.md) |

The [skill map](SKILL.md#pm-hard-skill-toolkit-skills) covers the remaining methods and domain lenses. Individual skill references contain templates and task-specific instructions.

## Documentation

The links above cover orchestration, workflow, memory, enforcement, and evals. For other details:

| Reference | Purpose |
|---|---|
| [Communication modes](docs/patterns/COMMUNICATION_MODES.md) | Lean, Standard, and Caveman output profiles |
| [Repository health](docs/REPO_HEALTH.md) | Validation checklist and bootstrap checks |
| [Toolkit decisions](docs/DECISIONS.md) | Recorded architecture and policy decisions |
| [PR history](docs/PR_HISTORY.md) | Integration history |

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before preparing a change. It defines the required validation, mirror rules, and eval requirements.

Edit skills in `skills/`, then regenerate their committed mirrors:

```bash
python3 scripts/sync_skills.py
python3 scripts/sync_skills.py --check
```

Do not hand-edit `.claude/skills/` or `.agents/skills/`. Eval cases need matching grader assertions and fixtures.

Run the documented validation checklist and report what you checked against the exact revision submitted for review. Record toolkit changes through `memory.py log repo`. Security reports follow the private-reporting instructions in `SECURITY.md`.

## License

[MIT](LICENSE).

The bundled humanizer derives from [blader/humanizer](https://github.com/blader/humanizer) by Siqi Chen. Its [license](skills/humanizer/LICENSE) and [provenance](skills/humanizer/README.md) are retained.
