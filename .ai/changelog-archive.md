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

