# Repo health and validation

Use this checklist before publishing or packaging `ai-pm-toolkit`.

## Structural checks

```bash
bash scripts/check_requirements.sh
python3 -m py_compile scripts/*.py
for hook in hooks/*.sh; do bash -n "$hook" || exit; done
python3 scripts/sync_skills.py --check
python3 scripts/validate_repo.py
python3 -S scripts/validate_repo.py
python3 scripts/test_hooks.py
python3 scripts/test_hook_contract.py
python3 scripts/test_grade_evals.py
python3 scripts/test_memory.py
python3 scripts/test_context_scripts.py
python3 scripts/test_record_eval_run.py
python3 scripts/test_run_eval_pilot.py
python3 scripts/test_label_eval_run.py
python3 scripts/test_propose_eval_updates.py
python3 scripts/test_validate_repo.py
python3 scripts/test_frontmatter.py
python3 scripts/grade_evals.py
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-dry-run --model dry-run --dry-run --allow-dirty
```

`validate_repo.py` covers:

- `SKILL.md` YAML frontmatter for the root skill and every skill under the canonical `skills/` tree.
- Local markdown links and backtick-quoted file paths (canonical + repo docs; the `.claude/skills/` and `.agents/skills/` mirrors are byte copies, checked separately by drift).
- `skills/WORKFLOW.md` parsing into the canonical eight-stage contract.
- `.claude/settings.json` and `.codex/hooks.json` hook shape, unsupported matchers, timeout units, and that every referenced command target exists.
- Hook wiring contract: every route in `hooks/contract.json` (event, tool, ordered handlers, per harness) resolves to exactly those handlers in the adapter, using separate matcher semantics: Claude Code accepts exact-name lists or regex; Codex uses regex, without Claude's comma-separated-list rule; malformed adapter JSON produces findings, never a traceback.
- Progressive-loading maps: every support file under a mapped skill is named in the skill's `progressive-loading.md` map.
- Hook shell syntax, and that shared `hooks/*.sh` scripts carry no harness-specific paths (`CLAUDE_PROJECT_DIR`, `.claude/`, `.codex/`, `.agents/`) — enforcement logic must work under both harnesses identically.
- Mirror drift: `.claude/skills/` and `.agents/skills/` match `skills/` exactly (`scripts/sync_skills.py --check`).
- Memory bootstrap compatibility between `init_context.py` (a project and the `--org` shared layer), `memory.py doctor`, and `stage_context.py`.
- Eval coverage: every canonical skill has an `evals/evals.json` whose `skill_name` matches its directory, with at least three cases, unique ids and names, valid categories, at least one adversarial case (the five doctrine skills also need a negative control), and one-to-one parity with the assertion blocks in `scripts/grade_evals.py`.
- GitHub custom agents in `.github/agents/`, where the validator enforces the published schema **and** a narrower repo policy, and says which is which in every message.
  - **Schema**: `description` is a non-empty string; `user-invocable` is a boolean; `name` is *not* required, because the filename is the identifier. An unrecognized tool name is an error here precisely because GitHub ignores it silently, so a typo costs a capability with no signal.
  - **What GitHub accepts**: `tools` as a YAML list *or* a comma-separated string, `[]` to disable every tool, `["*"]` to enable every tool, omission to default to all, aliases matched case-insensitively, documented compatible spellings (`Bash`, `NotebookRead`, `MultiEdit`, `WebSearch`, `TodoWrite`, and the rest), and MCP tools as `server/tool` or `server/*`.
  - **Repo policy, narrower on purpose**: `model` is absent, so every agent inherits the default and no model identifier lives in the repository; `tools` is an explicit non-empty list of canonical lowercase aliases, because an allowlist is reviewable; and `agents`, which GitHub does not document, is checked only for internal consistency — each name resolves to a file, and a non-empty list carries the `agent` tool.
  - **Contract**: exactly one `## Required reading` section per agent, naming `.ai/rules.md`, `.ai/memory/projects/<slug>/app.md`, the active context and project memory by its own expression; and one `AGENTS.md` table row per agent file.

`scripts/test_hooks.py` runs synthetic payloads against the shared gates and the Codex `apply_patch` adapter to confirm both harness paths block and unblock correctly. It also covers the soft memory reminder in a sandboxed git repo: work newer than the last changelog entry warns, a changelog entry newer than the last work stays silent, and no commit timestamp enters either side.

`scripts/test_grade_evals.py` runs hand-written outputs through the real assertion blocks. The pedagogical fixtures at the top of the file pin exact bands, and every pair in `scripts/fixtures/adversarial_outputs.json` must score its good text in 0.80 to 1.00 and its bad text at 0.30 or below, with a gap of at least 0.50. Every eval, the standard ones included since B41, carries a strict pair: a keyword-only reply that stays at or below 0.34 in five punctuation joins, a near miss that fails exactly one named assertion, and the block's own labels read back as a reply in the same five joins, also at or below 0.34. Every good text is also re-wrapped at 72 columns, alone, beside an unwrapped paragraph (after a blank line and glued with a single newline) and half wrapped, and all four must stay in its band, because the grader reads each assertion through its soft-wrap normaliser (each break is decided from the two lines it joins; blank lines, headings, list items, enumerated labels, table rows and labelled fields under a heading stay boundaries), and the newline joins of the two attacks pass through the same normaliser. Coverage is derived from the manifests: an eval without a high fixture, a low fixture or a strict pair fails the suite. The contract the fixtures enforce is written in `docs/EVAL_PROTOCOL.md`.

`scripts/test_memory.py` runs `memory.py` and `init_context.py` in a throwaway repo skeleton: caps, the `distill --prepare/--apply` fold (verbatim archive, stale and oversized packages refused, undated blocks never folded), the cold-layer archive index (regenerated on append, rebuilt and listed by `memory.py index`, every heading shape, and the staged-then-verified swap that leaves the archive byte-for-byte intact when a rebuild fails before it), the in-code PII denylist, and the soft-cap warnings for the shared org layer and `insights.md`.

`scripts/test_validate_repo.py` feeds the eval coverage check valid JSON with unexpected shapes (a list or object where a category, id or name string is expected; a non-list `evals`; a non-object top level) and asserts a validation finding comes back rather than a traceback. It does the same for the agent check against synthetic `.agent.md` fixtures, running **every case twice, with and without PyYAML**, and requiring the same verdict in both. Two cases must produce **no** finding, because `server/tool` and `server/*` are legitimate MCP tools and a closed allowlist of built-in aliases would reject valid configuration. One case checks a parsed *value* rather than the absence of a finding: a folded `description: >-` must come back as its text, since the fallback used to record the `>-` marker itself and pass.

`scripts/test_record_eval_run.py` records a synthetic pair in a disposable repository and checks the recorder's contract: provenance fields, refusal to overwrite, tamper detection through the output hash, unpaired configurations and mixed iterations rejected, and the HTML report rendering from a recorded pair.

`scripts/test_run_eval_pilot.py` drives `run_eval_pilot.py` with a fake harness (a Python script that answers on stdin, never a real CLI): every pilot run recorded with the harness-reported model and a provenance sidecar whose file hashes match and whose output hash the recorder's `validate_run` checks, the with-skill payload ending in the manifest prompt, the seeded configuration order, the configuration checks (a template without the isolation flags is refused before any generation call, with and without `--skip-probe`; a `CODEX_HOME` carrying instructions or MCP servers in `config.toml`, or any entry the session would load, is refused, while runtime artefacts and model keys pass; `-c`/`--config` overrides and `-p`/`--profile` selectors are refused in every spelling (separate, attached, with `=`), and a `--cd`/`-C` that points anywhere but the runner's own directory is refused before generation; `--skip-probe` skips the diagnostic only and the sidecar still records the checks), the isolation probe (a session that reports tools or instructions, or answers in another shape, stops the run; `--allow-unisolated` records it with the probe and the failed checks in the sidecar; one immutable probe file per invocation, and a tampered or missing probe fails `validate_run`), the attempts log with one line per invocation including the failed one, a failed attempt followed by a resume in the same work directory with the first attempt's directory kept, a Codex stream refused when its turn failed or never completed, the verified-version gate (an unlisted harness version is refused for a full iteration and allowed for a smoke run), a tampered sidecar failing validation, refusal of empty output, of a mixed harness, of an uncommitted tree and of an already-recorded run, a dry run that writes nothing, the Codex event stream, and malformed envelopes. The suite tests the runner's code paths, not compatibility with the real CLIs: that is established by the smoke run on the pilot machine and recorded in `verified_harness_versions` in `docs/benchmarks/pilot-deps.json`.

`scripts/test_label_eval_run.py` covers the human-label layer: append-only file with one current label per labeler and corrections through `--supersede`, identity by run (skill, eval id, configuration, output hash) so identical texts under two configurations keep separate labels, refusal of a tampered or unknown run and of invalid verdicts, handles or schema, the split rule for ties, the human and grader disagreement rates and the `investigate_grader` flag computed against controllable assertions, null fields when no labels exist, an orphan label that warns instead of failing, iteration mismatch, the rubric version and the stale rule (a label made against another prompt or expectation is reported and excluded, and the run can be relabelled), and every classification handle documented in `docs/EVAL_PROTOCOL.md`.

`scripts/test_propose_eval_updates.py` covers the proposal pass: which labelled runs become a card and which deliberately do not (agreement in either direction, a split with no consolidated verdict, and any run nobody labelled), the precedence that makes an eval-defect handle outrank a false accept, a stale-rubric card that asks for a relabel rather than a correction, the fixture candidate as a replacement for one slot of the existing pair rather than a second object the coverage checks would not notice, the collision warning when that candidate is already another slot's value, the bounded excerpt, idempotence and the refusal to overwrite a proposal a human annotated, and the guarantee the whole script exists for: after a pass, `evals.json`, the assertion blocks and `scripts/fixtures/adversarial_outputs.json` are byte-identical and no grading record was written.

## Frontmatter parsing

Validated frontmatter fields use a common portable subset in both modes:
plain/quoted scalars, booleans, decimal numbers, nulls, inline lists and text
blocks. Skills require non-empty string names and descriptions. Unsupported
validated values and duplicate keys produce findings; dependent skill checks
receive an explicit invalid result. Other metadata is not interpreted by the
portable parser. When PyYAML is unavailable, tests report its cases as skipped,
not as successful cross-parser verification. A skill's `name` must equal its directory.

## Bootstrap smoke test

```bash
python3 scripts/init_context.py "Validation Demo"
python3 scripts/init_context.py --org
python3 scripts/memory.py doctor
python3 scripts/stage_context.py
```

Expected result: `memory.py doctor` passes and `stage_context.py` emits a stage block with Inputs / Process / Output-gate.

## Hook portability

`hooks/contract.json` declares required routes in each harness. The validator
checks the configured handler order and destinations against that contract.
Malformed write envelopes and gate process failures block in the Codex adapter.
Shared marker scanners retain their documented error policies; these checks
do not establish factual truth or cover writes through arbitrary shell commands.

The content-sentinel hooks support both Linux and macOS hashing:

- Linux: `sha256sum`
- macOS: `shasum -a 256`

If neither exists, the hooks fail closed with an actionable error.

The CI tests Python 3.10 and 3.11; the stable `validate` job requires both matrix jobs to pass. Push runs target `main`; pull requests run once per event, with superseded runs cancelled. The preflight rejects Python below 3.10. Progressive-loading maps must name every support file in their skill. Context tests cover traversal, symlinks, switching, non-destructive migration and read-only status/report commands.
