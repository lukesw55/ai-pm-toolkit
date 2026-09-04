# Repo health and validation

Use this checklist before publishing or packaging `ai-pm-toolkit`.

## Structural checks

```bash
bash scripts/check_requirements.sh
python3 -m py_compile scripts/*.py
bash -n hooks/*.sh
python3 scripts/sync_skills.py --check
python3 scripts/validate_repo.py
python3 scripts/test_hooks.py
python3 scripts/test_grade_evals.py
python3 scripts/test_memory.py
python3 scripts/test_validate_repo.py
python3 scripts/grade_evals.py
```

`validate_repo.py` covers:

- `SKILL.md` YAML frontmatter for the root skill and every skill under the canonical `skills/` tree.
- Local markdown links and backtick-quoted file paths (canonical + repo docs; the `.claude/skills/` and `.agents/skills/` mirrors are byte copies, checked separately by drift).
- `skills/WORKFLOW.md` parsing into the canonical eight-stage contract.
- `.claude/settings.json` and `.codex/hooks.json` hook shape, unsupported matchers, timeout units, and that every referenced command target exists.
- Hook shell syntax, and that shared `hooks/*.sh` scripts carry no harness-specific paths (`CLAUDE_PROJECT_DIR`, `.claude/`, `.codex/`, `.agents/`) — enforcement logic must work under both harnesses identically.
- Mirror drift: `.claude/skills/` and `.agents/skills/` match `skills/` exactly (`scripts/sync_skills.py --check`).
- Memory bootstrap compatibility between `init_context.py`, `memory.py doctor`, and `stage_context.py`.
- Eval coverage: every canonical skill has an `evals/evals.json` whose `skill_name` matches its directory, with at least three cases, unique ids and names, valid categories, at least one adversarial case (the five doctrine skills also need a negative control), and one-to-one parity with the assertion blocks in `scripts/grade_evals.py`.
- GitHub custom agents in `.github/agents/`, where the validator enforces the published schema **and** a narrower repo policy, and says which is which in every message.
  - **Schema**: `description` is a non-empty string; `user-invocable` is a boolean; `name` is *not* required, because the filename is the identifier. An unrecognized tool name is an error here precisely because GitHub ignores it silently, so a typo costs a capability with no signal.
  - **What GitHub accepts**: `tools` as a YAML list *or* a comma-separated string, `[]` to disable every tool, `["*"]` to enable every tool, omission to default to all, aliases matched case-insensitively, documented compatible spellings (`Bash`, `NotebookRead`, `MultiEdit`, `WebSearch`, `TodoWrite`, and the rest), and MCP tools as `server/tool` or `server/*`.
  - **Repo policy, narrower on purpose**: `model` is absent, so every agent inherits the default and no model identifier lives in the repository; `tools` is an explicit non-empty list of canonical lowercase aliases, because an allowlist is reviewable; and `agents`, which GitHub does not document, is checked only for internal consistency — each name resolves to a file, and a non-empty list carries the `agent` tool.
  - **Contract**: exactly one `## Required reading` section per agent, naming `.ai/rules.md`, `.ai/app.md`, the active context and project memory by its own expression; and one `AGENTS.md` table row per agent file.

`scripts/test_hooks.py` runs synthetic payloads against the shared gates and the Codex `apply_patch` adapter to confirm both harness paths block and unblock correctly. It also covers the soft memory reminder in a sandboxed git repo: work newer than the last changelog entry warns, a changelog entry newer than the last work stays silent, and no commit timestamp enters either side.

`scripts/test_memory.py` runs `memory.py` and `init_context.py` in a throwaway repo skeleton: caps, the `distill --prepare/--apply` fold (verbatim archive, stale and oversized packages refused, undated blocks never folded), the cold-layer archive index (regenerated on append, rebuilt and listed by `memory.py index`, every heading shape, and the staged-then-verified swap that leaves the archive byte-for-byte intact when a rebuild fails before it), and the in-code PII denylist.

`scripts/test_validate_repo.py` feeds the eval coverage check valid JSON with unexpected shapes (a list or object where a category, id or name string is expected; a non-list `evals`; a non-object top level) and asserts a validation finding comes back rather than a traceback. It does the same for the agent check against synthetic `.agent.md` fixtures, running **every case twice, with and without PyYAML**, and requiring the same verdict in both. Two cases must produce **no** finding, because `server/tool` and `server/*` are legitimate MCP tools and a closed allowlist of built-in aliases would reject valid configuration. One case checks a parsed *value* rather than the absence of a finding: a folded `description: >-` must come back as its text, since the fallback used to record the `>-` marker itself and pass.

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
