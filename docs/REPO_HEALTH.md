# Repo health and validation

Use this checklist before publishing or packaging `ai-pm-toolkit`.

## Structural checks

```bash
bash scripts/check_requirements.sh
python3 -m py_compile scripts/*.py
bash -n .claude/hooks/*.sh
python3 scripts/validate_repo.py
```

`validate_repo.py` covers:

- `SKILL.md` YAML frontmatter for the root skill and all project skills.
- Local markdown links.
- `.claude/skills/WORKFLOW.md` parsing into the canonical eight-stage contract.
- `.claude/settings.json` hook shape, unsupported matchers, and timeout units.
- Hook shell syntax.
- Memory bootstrap compatibility between `init_context.py`, `memory.py doctor`, and `stage_context.py`.

## Bootstrap smoke test

```bash
python3 scripts/init_context.py "Validation Demo"
python3 scripts/memory.py doctor
python3 scripts/stage_context.py
```

Expected result: `memory.py doctor` passes and `stage_context.py` emits a stage block with Inputs / Process / Output-gate.

## Hook portability

The content-sentinel hooks support both Linux and macOS hashing:

- Linux: `sha256sum`
- macOS: `shasum -a 256`

If neither exists, the hooks fail closed with an actionable error.
