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

## The measured iteration

Three rules govern an iteration from its first recorded output to its published report. Two are new
here. The third restates an instruction that Record outputs already carried and makes it stricter.
Breaking any of them invalidates the iteration rather than weakening it.

**1. The measurement instrument is frozen for the whole iteration.** The instrument is not only the
grader. It is the repository commit, the eval manifests and their prompts, the expected outputs, the
skill bundle and the dependency hashes in `docs/benchmarks/pilot-deps.json`, the assertion blocks,
the fixtures, the thresholds, the model, the harness version, the runner arguments and the isolation
configuration. Change any one of them and the runs recorded before the change stop being comparable
with the runs after it, so the change starts a new iteration under a new identifier. This matters
more now that the proposal loop exists: applying a proposal in the middle of an iteration swaps the
grader underneath outputs that are already recorded.

**2. A model output is never edited by hand.** Record outputs already says to save the assistant
output as UTF-8 without editing it. What "without editing" covers is stated here: not formatting,
not whitespace, not a change that makes an assertion match. An output that cannot be parsed is a
failed attempt and is kept as one, never repaired into a recorded output.

**3. The decision criteria are pre-registered in a tracked file, in two phases.** The file is
`docs/benchmarks/<measured-iteration>/pre-registration.md`, and it is written across two commits so
that nothing in it ever has to name its own commit.

Before the smoke, commit the decision criteria: for each pilot skill the conditions that would make
it a keep, a fix, a simplify or a remove, plus any critical failure that blocks keep on its own, and
the name of the annotated tag the measured iteration will run from. That block is immutable from
that commit onward. Criteria written once the results are in describe the results.

After the smoke, add the factual metadata the smoke established, which is the harness, the verified
harness version and the model, without touching the criteria block. Commit that state and tag it
`pilot-<harness>-<n>-instrument`. The measured iteration runs from that tag, which is the one exact
revision the whole iteration is measured at.

The pre-registration names that tag and never a commit identifier of its own, because a file cannot
carry the identifier of the commit that contains that version of the file. The 40-character
identifier the tag resolves to is carried by the run metadata instead: `record_eval_run.py` writes
`repo_commit` from `git rev-parse HEAD` into every recorded run, and the report quotes it from
there.

Naming both is not the same as binding them, so the binding is checked at both ends. Before the
measured iteration records anything, resolve the tag and require the checkout to match it:
`git rev-parse <tag>^{commit}` and `git rev-parse HEAD` must give the same value. At report time,
require every recorded run's `meta.json.repo_commit` to equal that same value. Without both checks
the failure is silent and plausible: the tag is created correctly, HEAD moves or never matched, the
iteration runs, and the run metadata is internally consistent while describing a different
instrument from the pre-registered one. A single mismatch invalidates the iteration rather than
costing it one run, because a matching output cannot be told apart from a non-matching one without
already knowing which revision produced it. The report records the resolved identifier next to the
tag name, and the pre-registration still contains no identifier of its own, so the circularity stays
solved. Neither check exists in the runner today; enforcing them there is tracked under B46,
post-B25 hardening, and is not a promise this section makes.

### The order of operations

This sequences what the sections below specify. It does not replace them.

The smoke run and the measured run are deliberately different iterations. Step 4 changes
`docs/benchmarks/pilot-deps.json`, and rule 1 forbids that inside an iteration that has already
recorded outputs, which a smoke `--eval` has: it records both configurations. Nothing in the runner
catches the mix for you, because `existing_identity` compares the harness and the model on resume
and not the repository revision or the manifest. Keeping the identifiers apart is the operator's
job, and so is running the measured iteration from the tag rather than from whatever HEAD happens
to be.

1. Commit the decision criteria and the intended tag name. They are immutable from here.
2. Run one real smoke `--eval` per harness, under `iteration-<harness>-smoke-<n>`.
3. Inspect that smoke for compatibility only: the envelope, the provenance sidecar, the isolation
   configuration, the probe, the harness version, the model identifier and the session identifier.
   Not output quality, and not at any later point either.
4. Add the verified harness version to `verified_harness_versions`, and the harness, version and
   model to the pre-registration, leaving the criteria block untouched.
5. Commit that state and tag it `pilot-<harness>-<n>-instrument`. That tag is the measured revision.
6. Resolve the tag and confirm the checkout matches it before anything is recorded:
   `git rev-parse <tag>^{commit}` and `git rev-parse HEAD` must agree.
7. Start a fresh `iteration-<harness>-<n>` from that tag and record 30 outputs per harness: 15
   prompts in both configurations.
8. A fresh isolated session for every output.
9. Keep every attempt, the failed ones included.
10. Label each output `good`, `weak` or `fail`, with a classification and a reason.
11. Blind the first human read to the configuration where the tooling allows it. Where it does not,
    say so in the report rather than leaving the read to look blind.
12. Report paired counts, critical failures, negative controls, grader disagreement, token cost and
    duration.
13. Before the report is written, confirm every recorded run's `meta.json.repo_commit` equals the
    commit the tag resolves to. One mismatch invalidates the iteration.
14. Write one report per harness, with the smoke outputs excluded from it and the resolved
    40-character identifier recorded beside the tag name.
15. Attribute no difference to the harness when the models differ.
16. Write the keep, fix, simplify or remove decision for each pilot skill, against the conditions
    the pre-registration set.

### What the per-skill counts can carry

The three pilot skills contribute different numbers of prompts, so there is no single per-skill
denominator and no single step size:

| Skill | Prompts per harness | Pairs | What one pair is worth |
|---|---|---|---|
| `pm-phase-discover` | 6 | 6 | 16.7 points |
| `pm-transversal-comms` | 5 | 5 | 20 points |
| `pm-prioritization-regua-comum` | 4 | 4 | 25 points |

The report names the pair count and the denominator for each skill instead of describing all three
as one sample size. Report paired cases and counts: how many pairs moved, in which direction, which
ones they were, and what the critical failures were. A percentage over four to six cases is another
way of writing a count, not an estimate with a confidence interval, and the report must not present
it as one.

### Reading the pilot as a whole

Rule 3 pre-registers a decision for each pilot skill. It does not say what the pilot as a whole
means, and deciding that after the results are in has the same defect as writing the per-skill
criteria then: the outcome describes the results. So the verdict for the run as a whole is
pre-registered in the same file and the same commit as the per-skill conditions, before any
measured output exists.

Nothing below is a statistical test. Each line is a way of describing counts over 6, 5 and 4 pairs.

**Useful signal**, when all of these hold:

- at least two of the three skills show a consistent paired improvement;
- no skill regresses on critical failures;
- negative controls do not get materially worse;
- the improvement is not explained by length alone;
- the grader's direction and the human judgement broadly agree.

**Inconclusive**, when any of these holds:

- gains and regressions are mixed across skills;
- human and grader disagreement is wide enough that the pairs cannot be read;
- harness or model failures contaminate pairs that matter;
- the reading depends on a handful of ambiguous cases.

**Negative signal**, when any of these holds:

- no material paired improvement anywhere;
- critical failures increase;
- the apparent gain is mostly verbosity or rubric gaming;
- cost or latency rises without a proportional gain in quality.

"Material" is a judgement recorded with its evidence, not a number: the report names which pairs
moved and in which direction, per skill, against that skill's denominator. A reader who disagrees
with the verdict can therefore check the pairs rather than argue with a threshold.

Inconclusive is a legitimate outcome and the likely one at this size. It is not a failure to be
argued away, and it does not license a second reading of the same outputs under different criteria.
Changing the criteria means a new pre-registration and a new iteration, by rule 1.


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
   failure is stated, or one remedy says it covers them all, and a sentence that states a new
   failure with its own remedy does not settle the one before it; and an isolated "all green"
   that names no check passes neither branch.

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

## Propose, decide, check

The disagreement rate says the grader and the humans differ; it does not say which assertion
is wrong. `scripts/propose_eval_updates.py` turns each disagreement into a proposal a person
decides on, and then re-runs the suite against what that person pasted.

```bash
python3 scripts/propose_eval_updates.py propose --iteration iteration-claude-1
python3 scripts/propose_eval_updates.py check --skill <skill> --eval <eval-name>
```

`propose` reads the labels for the iteration, re-grades the recorded output rather than
trusting a `grading.json` that an edited assertion block may have left stale, and writes a
markdown proposal with a JSON sibling under `docs/benchmarks/<iteration>/proposals/`, plus an
index naming every label key and its outcome. Five categories: a run whose labels are all
against another rubric asks for a relabel, not a correction; a split is reported and never
resolved to the worse verdict; an `eval-defect` handle outranks a false accept and a false
reject, though a stale rubric and a split are read before it, and it counts how many labels go
stale if the prompt or the expected output changes; and a false accept or a false reject
carries a fixture candidate. Agreement in either direction proposes nothing, and neither does a
run nobody labelled: a proposal exists because a human wrote a verdict and a reason, and
harvesting an unlabelled run would be the grader learning from the output it is meant to judge.

It proposes and never applies. No code path writes to an eval manifest, to the assertion blocks
in `scripts/grade_evals.py` or to `scripts/fixtures/adversarial_outputs.json`, and the test
suite asserts all three are byte-identical after a pass. No regex is generated either: the
proposal names a direction and a rule in plain English composed only from the assertion labels
involved and the labeler's reason, and the Python block is commented out end to end, because a
pattern written from one output matches that output and the person who writes it has to own it.

The fixture candidate is a replacement for one slot of the pair that already exists, never a
second object: the file holds exactly one object per eval and all of them exist, and the
coverage checks are subset tests that would not notice a duplicate. Direction is recorded
because it decides whether the loop hardens the grader or corrupts it. A negative fixture taken
from a run that really failed defends against a failure that happened. A positive one copied
from a model's own output makes the grader agree with that model by construction, so a `good`
candidate, which comes from a run the grader rejected and a human accepted, is marked for a
rewrite by hand, and the test that the rewrite worked is that the reworded text still scores in
band: if only the original passes, the assertion memorised a phrasing rather than a behaviour.

`check` runs after a person has pasted a candidate. It judges the shape of the pasted object
first, so a missing key or a duplicate is a sentence rather than a traceback, then runs the
suite once and reports every fixture the suite ran for that eval against its band, the eight
derived from the pair and any written in code beside them, the declared against the actual
near-miss failure, the discrimination gap, the nine derived attacks, and any fixture the change
moved elsewhere in the suite. A green run means the fixtures the suite has do not contradict
the assertion. It does not mean the assertion is right.

A proposal carries no model text by default. Runs live under `skills/*/workspace/`, which is
gitignored, while `docs/` is tracked, and `record_eval_run.py` records whatever output its
caller hands it, so nothing in a card proves the text came from the isolated pilot. Publishing
it by default would put arbitrary model output into git permanently and grow a corpus of it one
directory from where the next assertion author would look. Two things would carry it: the
excerpt and the fixture candidate, which is that same output. Both are withheld, and the card
carries the output hash, the run path, whether a provenance sidecar exists, the grading and the
labeler's reason, which is what the decision rests on. `--embed-output` writes the bounded
excerpt and the candidate text in when someone wants them there, `--full-output` drops the
bound, and embedding a run with no provenance sidecar warns.

This is the toolkit's own evals. The product-side equivalent, a golden set for a feature a team
is shipping, lives in the project's memory and is written with `scripts/golden_set.py`, per
`skills/pm-archetype-ai/references/eval-design.md`.

As of this writing no iteration has been recorded, so the loop has been exercised against
synthetic runs only; the first real input arrives with the pilot.

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
