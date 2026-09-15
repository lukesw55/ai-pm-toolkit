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

## What the pilot measures

The runner injects the skill and its references into the prompt, disables tools and runs in an
empty directory outside the repository. What it measures is therefore the effect of an
instruction bundle on one response to a fixed prompt, and only that. It does not measure the
toolkit at runtime: routing to the right skill, progressive loading, hooks, memory and MCP
connectors stay outside the pilot, and a result here says nothing about them. Comparisons are
paired inside one harness (with_skill against without_skill on the same model, commit and
prompt); two harnesses running different models differ by model, and no difference between
their iterations may be attributed to the harness. A fake-harness test suite validates the
runner's code paths, not compatibility with the real CLIs; compatibility for a given version is
established by the smoke run below and recorded in `verified_harness_versions` in
`docs/benchmarks/pilot-deps.json`.

## Assertion and fixture contract

Every graded eval (doctrine-adversarial, skill-functional-adversarial and negative-control) is
scored by an assertion block in `scripts/grade_evals.py` and defended by a strict fixture pair in
`scripts/fixtures/adversarial_outputs.json`. The contract, enforced by `scripts/test_grade_evals.py`:

1. A positive assertion checks a relation, never a co-occurrence: two anchors from the prompt (a
   number, a name, an id, a role) with a relation word between them (a verb, "because", "not",
   "vs", a destination preposition) inside one clause, or an artefact a list cannot supply (a
   fraction with its denominator, a path, an id with a verb, a labelled field with content, an
   ordered sequence, a count of two or three of the same structure). The relation may also be
   carried by adjacency (a subject and its state side by side, as a terse status line puts them)
   or by structure (a table row whose cells hold the check and its result): the assertion accepts
   the forms the deliverable allows and never demands a verb or a prose repetition the prompt did
   not ask for.
2. One assertion per block checks the decision itself, with its verb and object ("does not write
   the one-pager as it stands", "ship to 100%", "sign-off given", "the gate stays").
3. At most two assertions per block are satisfied by a list of terms (negatives,
   `no_manufactured_objection`, `hedged`, size caps), and the block has at least three times as
   many assertions as that, so a list or the rubric scores at most 0.34.
4. Labels describe the check without quoting its tokens ("cites the sample size the prompt
   gives", not "cites 84 accounts").
5. Each pair carries four fixtures: `good`, natural prose that should score 1.00 and must land in
   0.80 to 1.00; `bad`, a plausible wrong answer (the one that complies, flatters or fabricates)
   at 0.30 or below, never a collection of forbidden phrases; `keyword_only`, one fragment per
   assertion made of the terms it looks for, in assertion order, never relating two anchors, at
   0.34 or below; `near_miss`, a complete and plausible answer that fails exactly the one
   assertion it names.
6. When the expected output says "either ... or", the assertion accepts both routes and the near
   miss omits another item.
7. Line breaks inside a paragraph are not behaviour. Every assertion reads the reply through
   `unwrap_soft_breaks` in `scripts/grade_evals.py`, which decides each break from the two
   lines it joins: when the next line's first word would have pushed the line before past the
   longer of the two, the break is a soft wrap and rejoins, and no other line of the reply
   takes part, so an unwrapped paragraph elsewhere changes nothing. Blank lines, headings,
   list items, enumerated labels ("Story 2:", "Slide 3 —"), table rows, block quotes, code
   fences and slide headers stay boundaries; a labelled field is never folded into the heading
   above it; a block whose longest line is under 40 characters, a list of tokens one per line,
   is left as it is. The same answer wrapped at any width scores the same, with or without
   unwrapped paragraphs beside it, and a token list joined by newlines still scores as a list.
8. An assertion that counts findings, failures or remedies accepts the honest zero when the
   reply names the checks it stands on: one real failure needs one path and one remedy, never a
   second failure to reach a count; each failure is followed by its remedy before the next
   failure is stated, or one remedy says it covers them all; and an isolated "all green" that
   names no check passes neither branch.

The test derives three more kinds of text from each strict pair: the good text wrapped at 72
columns, the same beside an unwrapped paragraph (after a blank line, and glued with a single
newline) and a half-wrapped copy, all held to the good band; the keyword list re-joined with
"; ", ", ", a newline and " and "; and the block's own labels joined the same five ways. Every
derived attack must stay at or below 0.34. A strict pair is required for every eval, the standard ones included since B41. The bands are a property of the grader, not of any skill: a good fixture at
1.00 says the assertions accept the intended answer, nothing about how often a model produces it.

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
files with hashes, the raw envelope and the output hash the recorder wrote, and `validate_run`
checks the sidecar against the run (same output hash, a payload that hashes to what it claims,
the SKILL.md the meta names, and the referenced isolation probe present with its recorded
hash), so a sidecar that describes another run, or points at a probe that no longer exists,
fails grading and labelling. Four guards precede the runs: the harness version must be listed
under `verified_harness_versions` in the manifest, which only a parsed `--eval` smoke run earns;
the process configuration is checked before the harness is started for anything, the probe
included, and recorded in every sidecar (for Claude Code `--safe-mode`, `--strict-mcp-config`,
`--tools ""` and `--permission-prompts none` in the argv; for Codex `--sandbox read-only`,
`--skip-git-repo-check`, no `-c`/`--config` override and no `-p`/`--profile` selector in any
spelling (separate, attached or with `=`), a `--cd`/`-C` directory that resolves to the runner's
own working directory when the template sets one, and a `CODEX_HOME` that holds only the
authentication file, the artefacts Codex writes while running and at most a `config.toml`
limited to model and approval keys, so no AGENTS.md, skills, hooks, prompts, instruction keys or
MCP servers; for both, a working directory outside the repository), and a missing check stops
the run unless `--allow-unisolated`, which records the failed checks instead; `--skip-probe`
skips only the diagnostic that follows; an isolation probe then asks the harness, through the same argv, what tools it
can call and what instructions it was given, and stops unless the answer is exactly two lines
both saying "none" (a repeated field, an extra line or a contradiction fails closed). The probe
is a diagnostic on top of the configuration checks, not the guarantee: a model's statement
about its own tools does not prove what the process loaded. Each invocation writes its own
probe file under `docs/benchmarks/<iteration>/probes/`, never overwriting an earlier one, so
every sidecar keeps pointing at evidence that exists (`--allow-unisolated` records anyway and the
sidecar carries the probe result and the failed checks); and every invocation, recorded or
failed, appends one line to
`docs/benchmarks/<iteration>/attempts.jsonl` with its status, attempt number, error and stdout
hash, while `harness_stdout.txt` and `harness_stderr.txt` stay in the run directory either way;
each attempt runs in its own `attempt-NN` directory, so a resume after a failure keeps the
failed attempt's evidence, and a Codex stream is a result only when its turn completed (a
`turn.failed` or `error` event, or a missing `turn.completed`, is refused). An empty
result, a failed process, a dirty tree under `skills/`, a mixed iteration or an already-recorded
run stops it; nothing is fabricated and no failure disappears from the record.

```bash
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --dry-run
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --eval <one eval name> --skill <its skill>
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --seed <n>
python3 scripts/run_eval_pilot.py --harness codex --iteration iteration-codex-1 --model <model> --seed <n>
```

Order of work on the pilot machine: `--dry-run` to see the thirty planned runs and the argv;
one `--eval` smoke run to confirm the harness envelope has the shape the parser expects
(session id, model, usage) and that the isolation probe reports "none" twice; add the version
the runner printed to `verified_harness_versions` in the manifest and commit it; the full
iteration; then grading. Until the version is listed, a full iteration is refused
(`--allow-unverified` overrides and the sidecar shows the unlisted version). `--skip-recorded` resumes an
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
it. A label whose `rubric_version` differs from the eval's current prompt and expected output
is stale: the grader reports it, warns, and never counts it as a current verdict, and the run
is relabelled against the current rubric without `--supersede`. The consolidated human verdict
is the majority; a tie between labelers is a split awaiting
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
model, harness version and the isolation probe result, attempts against recorded runs
(from `attempts.jsonl`; a report that counts only the recorded runs is incomplete),
loaded dependencies, number of complete pairs, per-skill pass rates for
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

Isolation checklist, in two layers. The configuration layer is what the runner verifies before
any harness call, whether or not the probe runs, and records in every sidecar: the documented
flags for a session without customisations (Claude Code: `--safe-mode`, `--strict-mcp-config`,
`--tools ""`, `--permission-prompts none`; Codex: `--sandbox read-only`, `--skip-git-repo-check`,
no `-c`/`--config` override and no `-p`/`--profile` selector in any spelling, the `--cd`/`-C`
directory equal to the runner's own when the template sets one, `CODEX_HOME` pointing at a
directory that holds only the
authentication file; the session and log artefacts Codex writes and a `config.toml` limited to
model and approval keys are tolerated, while AGENTS.md, skills, hooks, prompts, any
`[mcp_servers]` table and any instruction key are refused), the working directory outside the
repository and empty, the same flags for both configurations. A read-only sandbox limits what a
tool may do and proves nothing about which tools are attached; the home and override checks and
the probe carry that part. The probe layer is a diagnostic: the harness must answer exactly
`TOOLS: none` and `INSTRUCTIONS: none`, and `--skip-probe` skips this layer only. A failed check
or a probe that names a tool or an instruction means the isolation is broken for that harness on
that machine; fix the flags or the environment before recording, and never compare a run
recorded under a broken probe with one recorded under a clean one.

Claude Code (flags confirmed in `claude -p --help` 2.1.267; the envelope is not confirmed until
the smoke run parses it, so 2.1.267 is not yet listed as verified): the default template is
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
AGENTS.md, skills, hooks, prompts or `config.toml` customisations (MCP servers, instruction
files) load; the runner refuses the run when the home holds any of them. Keep the working
directory outside the repository for the same reason. The parser reads `thread.started` for the thread id, the last agent message or
`--output-last-message` for the text, and `turn.completed.usage` for tokens; when no event
names the model, the recorded model is the `--model` value and `provenance.json` says so with
`model_source: flag`. Pass a corrected template with `--harness-cmd` if the flags differ.

After both iterations are graded and labelled, commit `docs/benchmarks/<iteration>/labels.jsonl`
and `docs/benchmarks/<iteration>/report.md` per harness, update the README sentence on the
pilot, and close B25 in `.ai/backlog.md`.
