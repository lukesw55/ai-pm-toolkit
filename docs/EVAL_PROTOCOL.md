# Recording and comparing actual skill runs

The repository provides prompts and deterministic assertions. A fixture tests the
grader; it does not establish that a skill improves an assistant's output. No live
pilot is published yet. The recorder stores output from an actual external run;
it does not invoke models or turn an expected answer into benchmark evidence.

## Pilot design

Use every eval in `pm-phase-discover` (6), `pm-transversal-comms` (5) and
`pm-prioritization-regua-comum` (4). Fifteen prompts, two configurations and two
harnesses produce 60 outputs. Recount manifests if the dataset changes. Within
each harness, hold the model, repo commit, settings and prompt fixed. Record the
actual model identifier and the session/transcript source, never an inferred name.

For each output start a fresh session in an isolated directory with no inherited
conversation, project memory, AGENTS/CLAUDE instructions, automatic skills or
hooks. Baseline receives only the eval prompt. With-skill receives that same
prompt plus the target SKILL.md and explicitly selected dependencies. Record the
loaded files and their hashes in the session transcript. Do not expose expected
outputs, assertion source, fixtures or the opposite configuration to either run.
Use identical tool access in both configurations and record any unavoidable
harness differences. Randomize which configuration runs first. A paired single
run is a smoke pilot, not a statistical estimate of general effectiveness.

## Record outputs

Save the assistant output as UTF-8 without editing it. In a clean checkout at the
measured commit, record each configuration, for example:

```bash
python3 scripts/record_eval_run.py pm-phase-discover opportunity-tree-from-synthesis \
  --config with_skill --iteration iteration-codex-1 --harness codex \
  --model '<actual model>' --source '<session or transcript identifier>' \
  --output '<saved output path>'
```

Repeat with `--config without_skill`. Use `iteration-claude-1` and
`--harness claude-code` for the other harness. Tokens and duration are optional
`--tokens` and `--duration-ms` values; leave them absent when unreported.

The recorder validates the manifest identity and saves outputs/output.md,
meta.json and timing.json below each eval's configuration directory in the
skill workspace. Metadata includes repo commit, prompt/skill/output hashes,
harness, model, timestamp and source. Existing runs are never overwritten.
Use a new iteration when rerunning. Metadata identifies provenance but cannot
independently prove that a submitted transcript actually came from a model.

## Grade and report

```bash
python3 scripts/grade_evals.py --iteration iteration-codex-1
python3 scripts/grade_evals.py --iteration iteration-claude-1
```

The grader rejects missing metadata, changed output, unknown eval identity,
unpaired configurations and mismatched model/harness/commit/prompt within a pair.
An iteration also cannot mix harnesses, models or repository revisions.
Old manually created runs must be recorded with provenance before grading. Keep
the JSON/HTML report for each harness before running the other, because root
benchmark_all.json and eval-report.html are replaced. Skill workspace outputs
remain ignored by Git.

Commit a concise report under docs/benchmarks with run date, exact commit and
model, loaded dependencies, number of complete pairs, per-skill pass rates for
each configuration and harness, paired delta, failures and limitations. Cite
transcript identifiers so the run is auditable. Review failed assertions against
the output; a regex score is a proxy, not proof of factual correctness. Do not
publish a favorable aggregate that omits missing pairs or blends different models.
