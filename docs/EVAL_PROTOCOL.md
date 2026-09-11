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

## Run the pilot with the runner

`scripts/run_eval_pilot.py` drives one harness through the whole pilot and records every
output with real provenance. It reads the pilot skills and the files loaded with each
skill from `docs/benchmarks/pilot-deps.json` (SKILL.md is always first and implicit; every
`references/*.md` except the loading map; `skills/DOCTRINE.md` where the SKILL.md cites it),
builds the baseline payload byte for byte from the manifest prompt and the with-skill
payload as the prompt preceded by each loaded file tagged with its sha256, runs the harness
in a fresh empty directory outside the repository with the payload on stdin, randomises which
configuration runs first per eval from a seed it prints, and hands the text to
`scripts/record_eval_run.py` with the model, session and timing the harness itself reported.
A `provenance.json` beside each `meta.json` keeps argv, harness version, seed, order, loaded
files with hashes and the raw envelope. An empty result, a failed process, a dirty tree under
`skills/`, a mixed iteration or an already-recorded run stops it; nothing is fabricated.

```bash
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --dry-run
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --eval <one eval name> --skill <its skill>
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --seed <n>
python3 scripts/run_eval_pilot.py --harness codex --iteration iteration-codex-1 --model <model> --seed <n>
```

Order of work on the pilot machine: `--dry-run` to see the thirty planned runs and the argv;
one `--eval` smoke run to confirm the harness envelope has the shape the parser expects
(session id, model, usage); the full iteration; then grading. `--skip-recorded` resumes an
interrupted iteration without overwriting anything. Total tokens are the sum of input, output,
cache-creation and cache-read tokens for Claude Code, and input, cached-input and output tokens
for Codex; the recorded model is the one the envelope names, never an inferred alias.

## Record outputs

The runner records through this recorder; the manual path below is the fallback for a harness
the runner does not drive. Save the assistant output as UTF-8 without editing it. In a clean checkout at the
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

## Label runs

Assertions are a proxy. After grading, a human reads each output and records a verdict
with `scripts/label_eval_run.py`; the grader reads the labels back and reports where it
disagrees with the humans.

```bash
python3 scripts/label_eval_run.py pm-phase-discover opportunity-tree-from-synthesis \
  --config with_skill --iteration iteration-claude-1 \
  --verdict weak --classification skipped-method \
  --reason "Ranks opportunities but never scores evidence strength" --labeler <role>
```

Verdicts: `good` (usable as delivered), `weak` (usable only after a material fix), `fail`
(wrong, harmful or unusable). `weak` and `fail` carry at least one classification handle:
`sycophancy` (accepts a weak premise or caves under pressure with no new argument),
`manufactured-objection` (invents a reservation against a sound premise), `invented-fact`
(states unverified or absent facts as true), `skipped-method` (ignores the skill's method
where it applies), `wrong-decision` (applies the method and still lands on the wrong call),
`incomplete` (misses a required part of the deliverable), `format-slop` (structure tells:
label-colon runs, banners, padding), `scope-bloat` (answers beyond the ask), `eval-defect`
(the prompt or the assertion block is at fault, not the output) and `review-needed` (the
labeler wants a second opinion; the verdict still stands).

Labels live in `docs/benchmarks/<iteration>/labels.jsonl`, one JSON object per line, tracked
in git because runs under `workspace/` are not. A label names the run it judges (iteration,
skill, eval id, configuration) and binds to the exact output by its sha256; the hash alone is
not the identity, because the same text can come back for two prompts or for both
configurations. It also carries `rubric_version`, twelve hex characters of the eval's prompt
and expected output, so a label can be traced to the rubric its author read. The file is only
appended: a run carries one current label per labeler, a second opinion is a second line, and
a labeler who changes their mind appends a correcting record with `--supersede`; the loader
keeps the latest record per labeler, the earlier one stays as history and the report counts
it. The consolidated human verdict is the majority; a tie between labelers is a split awaiting
resolution, reported as such and left out of the grader comparison rather than resolved to
the worse verdict.

The grader binarises both sides: an assertion pass rate at or above 0.8 is a pass, a human
`good` is a pass, and a run where the two differ is a grader disagreement. Two rates are
reported separately: human disagreement (runs with two or more labelers who did not agree)
and grader disagreement (grader against the consolidated human verdict). Above the
disagreement threshold set before the run (0.10 by default, a starting point adapted from
Peters' judge verification, not a sufficiency guarantee) the report flags `investigate_grader`:
recalibrate the assertions (or the eval itself, when the handle is `eval-defect`) before
trusting the pass rates. Call it drift only when the rate rose against the previous
iteration's report; one rate is a signal to investigate, not a trend.

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
remain ignored by Git. When `docs/benchmarks/<iteration>/labels.jsonl` exists the grader
reads it by default (`--labels` overrides the path), attaches the consolidated human verdict
and the split flag to every graded run and reports the human and grader disagreement rates
per skill and overall; superseded labels are counted, and labels whose run is not on this
machine are counted and warned about, never an error.

Commit a concise report under docs/benchmarks with run date, exact commit and
model, loaded dependencies, number of complete pairs, per-skill pass rates for
each configuration and harness, paired delta, labelled runs with the human and grader
disagreement rates per skill and overall, split runs, the `investigate_grader` flag and,
from the second iteration on, the comparison against the previous iteration's rate (that
comparison, not one rate, is what drift means), the classification histogram, failures
and limitations. Cite
transcript identifiers so the run is auditable. Review failed assertions against
the output; a regex score is a proxy, not proof of factual correctness. Do not
publish a favorable aggregate that omits missing pairs or blends different models.

## Runbook per harness

Common to both: a clean checkout at the measured commit (`git status --porcelain` empty under
`skills/`), the runner's `--dry-run` first, one `--eval` smoke run, then the full iteration,
then `scripts/grade_evals.py --iteration <iteration>`; keep `benchmark_all.json` and
`eval-report.html` for one harness before grading the other, because both live at the repo
root and are replaced. Never mix harnesses or models in one iteration; start a new one.

Claude Code (flags confirmed in `claude -p --help` 2.1.267): the default template is
`claude -p --output-format json --model <model> --safe-mode --strict-mcp-config --tools ""
--permission-prompts none`. `--safe-mode` disables CLAUDE.md, skills, plugins, hooks, MCP
servers, custom commands and agents while keeping authentication and model selection, which is
the isolation the pilot design requires; `--tools ""` gives both configurations the same (no)
tool access. Do not add `--fallback-model` (it can switch the model inside an iteration) or
`--no-session-persistence` (the session id is the auditable source the protocol records). The
JSON envelope fields the parser reads (`result`, `session_id`, `usage`, `modelUsage`,
`duration_ms`) follow the SDK documentation; the smoke run confirms them.

Codex (template to verify with `codex exec --help` on the machine; this repo has no Codex
binary): the default template is `codex exec --json --model <model> --sandbox read-only
--ask-for-approval never --skip-git-repo-check --cd <cwd> --output-last-message <file> -`.
Point `CODEX_HOME` at a fresh directory holding only the authentication file so no user-level
AGENTS.md, skills or hooks load, and keep the working directory outside the repository for the
same reason. The parser reads `thread.started` for the thread id, the last agent message or
`--output-last-message` for the text, and `turn.completed.usage` for tokens; when no event
names the model, the recorded model is the `--model` value and `provenance.json` says so with
`model_source: flag`. Pass a corrected template with `--harness-cmd` if the flags differ.

After both iterations are graded and labelled, commit `docs/benchmarks/<iteration>/labels.jsonl`
and `docs/benchmarks/<iteration>/report.md` per harness, update the README sentence on the
pilot, and close B25 in `.ai/backlog.md`.
