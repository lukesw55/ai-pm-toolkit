# Changelog archive

> Rotated out of `changelog.md`. Full entries, verbatim.

Index (one line per archived block, file order; grep here before opening a block):
- 2026-09-08 session log
- 2026-09-08 session log
- 2026-09-08 session log
- 2026-09-09 Neutral examples audit
- 2026-09-10 Versioned integration history
- 2026-09-10 Remaining backlog implementation
- 2026-09-10 B31 pontas soltas da execução consolidada
- 2026-09-10 B31 matcher review correction
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 session log
- 2026-09-10 Merge main and renumber B31 to B39
- 2026-09-10 Two-anchor assertions and strict fixture pairs for the six new evals
- 2026-09-11 Composite label identity, supersede, split verdicts, two disagreement rates
- 2026-09-11 Pilot runner: measurement scope, isolation probe, attempts log, sidecar validation
- 2026-09-11 Org layer: slug unreserved, precedence rule, verifiable personal-data check
- 2026-09-11 Eval design sized to the task; recipe contract gains completeness, unit and time zone
- 2026-09-11 Review panel selects lenses by risk and names the ones not run
- 2026-09-11 Round 2 closing: review section, B40 candidate, recounts
- 2026-09-11 Artefact anchors and punctuation-variant regression for the six new blocks
- 2026-09-11 Stale rubric labels are reported, never counted
- 2026-09-11 Strict probe, explicit configuration checks, immutable probes bound to validation

## 2026-09-08: session log

B21: validate hook routes and configuration shapes; block malformed Codex writes and gate process errors. Verified on Python 3.11 under WSL: six contract regressions and existing validator, hook, grader, memory and schema suites passed. Live harness integration not yet verified.

## 2026-09-08: session log

B23 in progress: portable typed frontmatter and invalid-result propagation implemented locally. Three new local tests and 31 existing fallback schema cases pass; cross-parser test skipped because PyYAML is unavailable in the Windows runtime. Full Linux validation is blocked by automatic approval review: workspace out of credits. B21 merged as PR #16; remaining batches and the live pilot are not complete.

## 2026-09-08: session log

B23: completed portable typed frontmatter, invalid-result propagation and explicit optional-dependency test skips. Linux validation resumed: 4 frontmatter tests, 54 schema cases and structural validation with and without PyYAML passed.

## 2026-09-09: Neutral examples audit

Audited all 466 tracked files. Replaced sector-specific examples and the incident narrative with fictional document-collaboration scenarios; generalized the matching grader alternative, analytical inputs and backlog wording. All validation suites passed; 132 canonical files match both generated mirrors. Historical commits were not rewritten.

## 2026-09-10: Versioned integration history

Backfill from verified GitHub PR metadata; detailed change mapping and source links: `docs/PR_HISTORY.md`. Original dates below are integration dates, not reconstructed session dates.

- PR #1: 2026-09-01T20:25:01Z, main `51d634c`.
- PR #2: 2026-09-01T21:15:48Z, main `e62396b`.
- PR #3: 2026-09-02T11:15:36Z, main `c76e728`.
- PR #4: 2026-09-02T11:41:12Z, main `1fa55ef`.
- PR #5: 2026-09-02T12:08:02Z, main `cb60626`.
- PR #6: 2026-09-02T15:43:09Z, main `ec53632`.
- PR #7: 2026-09-02T18:53:40Z, main `42d3812`.
- PR #8: 2026-09-03T13:37:55Z, main `401b7bd`.
- PR #9: 2026-09-03T16:23:20Z, main `8974faa`.
- PR #10: 2026-09-03T17:02:29Z, main `a5fdaa4`.
- PR #11: 2026-09-03T19:22:08Z, main `2a7c139`.
- PR #12: 2026-09-03T19:47:46Z, main `0376d22`.
- PR #13: 2026-09-03T21:03:18Z, main `e5ace64`.
- PR #14: 2026-09-04T14:00:49Z, main `cab97b0`.
- PR #15: 2026-09-04T14:26:51Z, main `b97ff17`.
- PR #16: 2026-09-08T17:17:24Z, main `14fb603`.
- PR #17: 2026-09-09T01:15:48Z, main `bd321d0`.
- PR #18: 2026-09-09T17:45:37Z, main `88d2e6b`.

## 2026-09-10: Remaining backlog implementation

Implemented B24, B22, B28, B26, B27 and B30 in one consolidated change. Added B25 recorder and protocol; the real 60-output pilot remains pending because authenticated Claude Code and Codex runners are unavailable. B21 and B23 recorded as already integrated. Validation results are recorded in the PR; binding decisions are in docs/DECISIONS.md.

## 2026-09-10: B31 pontas soltas da execução consolidada

B31: pontas soltas da execução consolidada (PRs #16 a #19). Actions fixadas por SHA completo; cobertura de fixtures NC/adversarial derivada dos manifests, com 7 fixtures novas (39/39 blocos cobertos, 94 fixtures); código morto removido e semântica de matcher dos harnesses no validador; name do SKILL.md igual ao diretório; regressões novas no contrato de hooks e no frontmatter; README, REPO_HEALTH e AGENTS.md alinhados com as suítes reais; travessão literal no adapter Codex; título default do log derivado da entrada. Validação local em Python 3.11: preflight, py_compile, bash -n por hook, 132 espelhos, validador verde com e sem PyYAML, hooks 33, contrato 8, grader 94, memória 41, contexto 8, gravador 5, validador 54, frontmatter 5, smoke do grader exit 0, doctor verde.

## 2026-09-10: B31 matcher review correction

PR #20 review: separate Claude exact-name/list matcher semantics from Codex regex semantics. Pass the harness through contract validation and test partial names, comma lists, alternation and anchors.

## 2026-09-10: session log

B39: removed the stray identity check in grade_evals.render_html (lines 1092-1095 referenced grade_all locals and raised NameError on the first recorded run); added test_report_renders_recorded_pair in scripts/test_record_eval_run.py, which failed with NameError before the fix and passes after. Validation: full docs/REPO_HEALTH.md battery green.

## 2026-09-10: session log

B35: shared org layer (.ai/memory/org/: company, personas, competitors, goals) with templates under _templates/org/, init_context.py --org bootstrap that never overwrites, reserved slug 'org', doctor soft caps for org files and the new per-project insights.md template; missing templates now fail with a message instead of a traceback; canonical research paths reconciled in pm-transversal-analysis references (raw-evidence for PII, research/<topic>/sessions for excerpt logs, discovery/<topic>/synthesis.md for memos, insights.md for ranked themes); docs updated (MEMORY_SYSTEM tree and roles, memory README, README, AGENTS, CLAUDE, REPO_HEALTH, repo-doctor). Validation: test_context_scripts 11 tests, test_memory 45 cases, full REPO_HEALTH battery green, mirrors synced.

## 2026-09-10: session log

B35: wired the shared org layer into the read and persist paths: a required-reading bullet in the four archetype skills, an org hint in the load-context step of discover, define, develop, deliver, analysis, stakeholder and comms, an enrichment clause in the persist step of discover, define and deliver, and a required-reading bullet in the ten Copilot agents. Validation: validate_repo (both parsers), test_validate_repo, mirrors synced.

## 2026-09-10: session log

B33: added skills/pm-archetype-ai/references/eval-design.md (PM-owned eval method for AI features: scenario sheet, four hazards, four numeric limits, golden set with a real failure, block rule above the pass rate, validation and judge verification; original text adapted from Dean Peters with licence note) plus the skill's progressive-loading map, narrowed the single-file paragraph in that SKILL.md only, pointed workflow steps 3 and 6 and the pm-ai agent at it, added launch-gate and PRD one-liners, and eval 4 design-golden-set-and-block-rule-for-summariser with assertions and a good/bad fixture pair. README archetype and references sentences no longer carry a hard-coded count. Validation: validate_repo both parsers, test_grade_evals 89 fixtures, mirrors synced.

## 2026-09-10: session log

B34: added skills/pm-phase-develop/references/prototyping-ladder.md (three prototype tiers by where they live and what they cost engineering: throwaway, code prototype on a disposable branch of the real codebase via a coding agent, PM-authored PR for copy/config/flags/minor UI and never core logic; sandbox repo request and prototype decision record templates; decision table; link to the stage-6 gate), sub-skill 7 and persist path in the SKILL.md, progressive-loading row, WORKFLOW stage-6 row now cites the reference and records the tier, stage_context fallback string, README and root SKILL rows, and eval 4 choose-prototype-tier-for-billing-change with assertions and fixture pair. Validation: validate_repo both parsers, test_grade_evals 91 fixtures, test_context_scripts, mirrors synced.

## 2026-09-10: session log

B36: added skills/pm-transversal-stakeholder/references/review-panel.md (five stakeholder lenses with cards, the rule that no objection is a valid output and a manufactured one is a doctrine-7 failure, panel report template, sequential default with subagent fan-out where available, consolidation into the dissent protocol and the assumption map, never a gate), sub-skill 4 and persist path in the SKILL.md, progressive-loading row, one sentence in the WORKFLOW shadow-gate paragraph, an AGENTS known-degradation note for Codex, root SKILL and README blurbs, and evals 3 (skill-functional-adversarial: hidden discount-revenue exposure) and 4 (negative-control: clean PRD cleared without an invented objection) with assertions and fixture pairs. Validation: validate_repo both parsers, test_grade_evals 95 fixtures, mirrors synced.

## 2026-09-10: session log

B37: added skills/pm-transversal-analysis/references/batch-interview-synthesis.md (shared codebook first, one excerpt log per transcript, fan-out where the harness offers subagents with a sequential fallback, merge by participants with counter-evidence, saturation and recency checks, PII kept in raw-evidence) and references/connector-task-recipes.md (recipe contract plus launch retro from Jira tickets, feature adoption from analytics, behaviour-split retention; numbers only from tool results, source links, persistence with query text, TBD rules), sub-skills 5 and 6, load and persist steps and the MCP integration bullet in the SKILL.md, two progressive-loading rows, root SKILL and README blurbs, the AGENTS known-degradation note, and evals 3 (standard batch synthesis) and 4 (skill-functional-adversarial: refuse the 2x retention claim no tool returned) with assertions and fixture pairs. Validation: validate_repo both parsers, test_grade_evals 99 fixtures, test_frontmatter, mirrors synced.

## 2026-09-10: session log

B39: added scripts/run_eval_pilot.py (pilot runner: builds the without_skill and with_skill payloads from docs/benchmarks/pilot-deps.json with sha256 per loaded file, runs the harness CLI in a fresh directory outside the repo with the payload on stdin, randomises the config order per eval from a printed seed, parses the Claude Code JSON envelope and the Codex event stream, refuses empty output, mixed harness, dirty tree and already-recorded runs, records through record_eval_run.record() and writes a provenance.json sidecar), the dependency manifest, and scripts/test_run_eval_pilot.py with a fake harness (9 tests: 30 recorded runs graded end to end, seeded order, empty output, mixed harness, resume, dirty tree, dry run, codex stream, bad envelopes). Claude Code flags confirmed against claude -p --help 2.1.267; Codex template to be verified on the pilot machine. Validation: tests, dry run, validate_repo both parsers.

## 2026-09-10: session log

B32: added scripts/label_eval_run.py (append-only human labels in docs/benchmarks/<iteration>/labels.jsonl, bound to the output sha256, one label per labeler, verdict good/weak/fail with ten classification handles), integrated labels into grade_evals.py (PASS_THRESHOLD 0.8 and DRIFT_THRESHOLD 0.10, human verdict and agreement per run, disagreement rate and grader_drift per skill and overall, classification histogram, labels without a local run counted and warned, --labels flag with a default path, HTML rows and columns), documented the label step and the report fields in docs/EVAL_PROTOCOL.md, and added scripts/test_label_eval_run.py (9 tests: append and duplicate refusal, hash and unknown-run refusal, invalid inputs, 0.5 disagreement with drift, null fields without labels, orphan label warns, iteration mismatch, majority and tie rules, handles documented). Validation: label, recorder, runner and grader suites green; validate_repo both parsers.

## 2026-09-10: session log

B32-B39 closing: protocol gained the runner section and the per-harness runbook, REPO_HEALTH and README list the new scripts and tests, CI runs the pilot-runner and label suites plus a manifest dry run, README eval counts recounted from the manifests (85 cases: 43/11/15/16) with no other hard-coded totals left, backlog rows B32-B39 with GUT and detail sections plus the batch table and the updated B25 pendency, five binding decisions in docs/DECISIONS.md, tasks updated. Validation: full REPO_HEALTH battery green including the two new suites and the dry run; mirrors 138 files each.

## 2026-09-10: Merge main and renumber B31 to B39

Merged origin/main (PR #20, 474ce87) into the references batch: conflicts in the two changelog files, README and REPO_HEALTH resolved keeping both sides (PR #20 entries archived in chronological order, one README row per script, Frontmatter parsing heading kept). The pre-merge B31 item (render_html fix, pilot runner, runbook) is renumbered B39 in the backlog, tasks and this branch's changelog entries because PR #20 owns B31; commits cc054d7 and a9c490f keep the old label. Validation: full REPO_HEALTH battery green on the merged tree (106 fixtures, 42/42 graded evals covered, memory 46, context 11, contract 9, frontmatter 5, mirrors 138).

## 2026-09-10: Two-anchor assertions and strict fixture pairs for the six new evals

B33-B37 evals rewritten after the owner's review of PR #21: the six new assertion blocks use two- or three-anchor sentence checks (in_one_sentence, count_at_least, anchors), one decision assertion per block and at most two negatives, so a keyword-only reply scores at most 2/6; the eval-design prompt drops the exact-four/twenty/thirty/10% numbers for task-proportional sizing with a threshold set beforehand, and the panel prompt drops 'with all lenses'. Each of the six fixture pairs now carries good, plausible bad, keyword_only (<= 0.34) and near_miss (fails exactly one named assertion); test_grade_evals registers the four and checks the near-miss failing set. Validation: test_grade_evals 118 fixtures, 6 strict pairs, 42/42 graded evals covered; grader smoke; validate_repo both parsers; mirrors synced; full REPO_HEALTH battery green.

## 2026-09-11: Composite label identity, supersede, split verdicts, two disagreement rates

B32 revised after the owner's review of PR #21: labels.jsonl moves to schema 2 with a composite run identity (iteration, skill, eval_id, config, output_sha256), rubric_version (12 hex of prompt + expected_output), corrections through --supersede with the history kept in the file, a tie between labelers reported as a split awaiting resolution instead of the worse verdict, and the grader reporting human disagreement and grader disagreement separately with investigate_grader (threshold set before the run) replacing grader_drift, since drift needs a comparison across iterations. Protocol, DECISIONS, README, REPO_HEALTH and backlog updated. Validation: test_label_eval_run 12 tests including identical text under both configurations keeping separate labels; recorder, runner and grader suites; full REPO_HEALTH battery green.

## 2026-09-11: Pilot runner: measurement scope, isolation probe, attempts log, sidecar validation

B39 revised after the owner's review of PR #21: run_eval_pilot.py states what the pilot measures (an instruction bundle's effect on one response; not routing, progressive loading, hooks, memory or MCP; comparisons only inside one harness), runs an isolation probe before the runs and fails closed when the session reports tools or instructions (docs/benchmarks/<iteration>/isolation-probe.json, referenced from every sidecar), appends every invocation to docs/benchmarks/<iteration>/attempts.jsonl with status and error so failures stay on record, keeps stdout and stderr in the run directory on failure too, writes output_sha256 into provenance.json which record_eval_run.validate_run now checks against the run (output hash, payload hash, loaded SKILL.md), and refuses a full iteration on a harness version not listed under verified_harness_versions in pilot-deps.json (empty until a smoke run parses the envelope). Protocol gained 'What the pilot measures' and the isolation checklist; REPO_HEALTH and README say the fake-harness suite tests code paths, not CLI compatibility. Validation: test_run_eval_pilot 12 tests, recorder and label suites, dry run, full REPO_HEALTH battery green.

## 2026-09-11: Org layer: slug unreserved, precedence rule, verifiable personal-data check

B35 revised after the owner's review of PR #21: the project slug 'org' is no longer reserved (projects/org/ and org/ are different directories; test replaced by one where both coexist), the precedence rule is explicit in MEMORY_SYSTEM, the four org templates, CLAUDE.md and AGENTS.md (for a project's decisions the project files win; a divergence goes to that project's decisions.md before the org file changes, logged with memory.py log), and the personal-data rule became verifiable: memory.py doctor warns on e-mail and phone patterns in org/*.md, names stay a review rule, pseudonymisation is described as lowering, not removing, re-identification risk. DECISIONS row and backlog updated. Validation: test_context_scripts 11, test_memory 48 (e-mail and phone flagged; dates and counts not), validate_repo both parsers, doctor, mirrors synced; full REPO_HEALTH battery green.

## 2026-09-11: Eval design sized to the task; recipe contract gains completeness, unit and time zone

B33 and B37 revised after the owner's review of PR #21: eval-design.md no longer turns Peters' worked-example numbers into rules (hazard list and limits block sized to the task, each limit with a rationale written before the run, golden set sized and justified, verification against a threshold set beforehand with about thirty cases and one in ten as starting points), the failure taxonomy gained a 'counts as a failure when' column so asking a question or omitting a citation fails only where the task contract requires the opposite, a critical failure is never offset by a high average, and drift is claimed only against the previous verification. connector-task-recipes.md: the contract gained Completeness (paged to the end, total against fetched), Unit and deduplication, and Time zone; each recipe carries the three; Recipe 3 defines the behaviour observation window (days 0 to 7) closed before the retention window and names leakage as a check. Sub-skill 6, DECISIONS and backlog follow. Validation: validate_repo both parsers, test_grade_evals 118, mirrors synced; full REPO_HEALTH battery green.

## 2026-09-11: Review panel selects lenses by risk and names the ones not run

B36 revised after the owner's review of PR #21: the review panel selects lenses by the exposure the artefact touches (exposure-to-lens table in review-panel.md) instead of running five as a ritual, every lens not run is named in the report with a one-line reason, an author's request to skip a lens because it might object is the reason to run it, and a 'ritual panel' anti-pattern was added; sub-skill 4, the WORKFLOW shadow-gate sentence, the progressive-loading row, root SKILL and README blurbs and the backlog say risk-selected instead of five-lens. The adversarial eval (M3) already requires the commercial objection to name the omitted 62% discount exposure. Validation: validate_repo both parsers, test_grade_evals 118, mirrors synced; full REPO_HEALTH battery green.

## 2026-09-11: Round 2 closing: review section, B40 candidate, recounts

Round 2 of PR #21 closed: backlog gained the 'Revisão da PR #21' section mapping the owner's seven points to the follow-up commits, the B40 candidate (54 of 79 pre-batch assertion blocks pass a keyword-only reply; the six new blocks were rewritten, the old ones are next), recounted totals (85 evals, 32 pairs with 6 strict, 118 fixtures, 42/42 covered, mirrors 138, suites hooks 33, contract 9, memory 48, context 11, recorder 6, runner 12, labels 12, validator 54, frontmatter 5); tasks updated; README describes the strict fixture pairs. Validation: validate_repo both parsers, doctor, git diff --check.

## 2026-09-11: Artefact anchors and punctuation-variant regression for the six new blocks

Round 3 of PR #21, finding 1: the six new assertion blocks now require artefacts a keyword list cannot supply (a URL, HogQL text or insight id as the source; an analytics/<file>.md path for persistence; at least two of the weekly numbers; the behaviour-split query with its cohorts; the evidence gap phrased as a question with an owner role; a lens name next to its no-objection verdict with a reason that never crosses a semicolon; the PRD as the object of the kickoff decision; a participant plus a verb in the counter-evidence and saturation checks; role, verb and object for who builds what). test_grade_evals derives four punctuation variants (semicolon, comma, newline, and) of every keyword-only fixture and requires each at or below 0.34; the owner's semicolon variant of the adoption fixture drops from 6/7 to 2/7. Validation: test_grade_evals 118 fixtures, 24 variants, 6 strict pairs, 42/42 covered; full REPO_HEALTH battery green.

## 2026-09-11: Stale rubric labels are reported, never counted

Round 3 of PR #21, finding 2: a label whose rubric_version differs from the eval's current prompt and expected output is stale. label_eval_run.split_by_rubric separates current from stale labels; grade_all keeps only current labels for the human verdict and the rates, reports stale ones in grading.json and the benchmark (labels_stale), warns per stale label, and label() lets the same labeler relabel against the current rubric without --supersede while the old record stays in the file (then counted as superseded). Regression: change only expected_output after labelling; the verdict becomes null, labels_stale is 1, relabelling works. Protocol and REPO_HEALTH updated. Validation: test_label_eval_run 13, runner and recorder suites, full REPO_HEALTH battery green.

## 2026-09-11: Strict probe, explicit configuration checks, immutable probes bound to validation

Round 3 of PR #21, finding 3: parse_probe accepts only two lines, TOOLS then INSTRUCTIONS, and fails closed on an extra line, a repeated field or a contradiction (format_ok recorded); isolation_config checks the process explicitly per harness (Claude Code: --safe-mode, --strict-mcp-config, --tools '', --permission-prompts none; Codex: --sandbox read-only, --skip-git-repo-check, CODEX_HOME without AGENTS.md, skills or hooks; both: cwd outside the repo) and a missing check refuses the run unless --allow-unisolated; every invocation writes its own probe file under docs/benchmarks/<iteration>/probes/ and never overwrites one; the sidecar carries the probe reference, the config and skip_probe, and record_eval_run.validate_run requires the referenced probe to exist with the recorded hash and content. Protocol and REPO_HEALTH describe the probe as a diagnostic on top of the configuration guarantee. Validation: test_run_eval_pilot 14 (contradictory probe, unsafe template refused, two invocations keep both probes valid, tampered or missing probe fails validation), recorder and label suites, full REPO_HEALTH battery green.

