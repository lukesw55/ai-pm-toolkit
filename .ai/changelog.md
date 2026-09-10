# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: Merge main and renumber B31 to B39

Merged origin/main (PR #20, 474ce87) into the references batch: conflicts in the two changelog files, README and REPO_HEALTH resolved keeping both sides (PR #20 entries archived in chronological order, one README row per script, Frontmatter parsing heading kept). The pre-merge B31 item (render_html fix, pilot runner, runbook) is renumbered B39 in the backlog, tasks and this branch's changelog entries because PR #20 owns B31; commits cc054d7 and a9c490f keep the old label. Validation: full REPO_HEALTH battery green on the merged tree (106 fixtures, 42/42 graded evals covered, memory 46, context 11, contract 9, frontmatter 5, mirrors 138).

## 2026-09-10: session log

B32-B39 closing: protocol gained the runner section and the per-harness runbook, REPO_HEALTH and README list the new scripts and tests, CI runs the pilot-runner and label suites plus a manifest dry run, README eval counts recounted from the manifests (85 cases: 43/11/15/16) with no other hard-coded totals left, backlog rows B32-B39 with GUT and detail sections plus the batch table and the updated B25 pendency, five binding decisions in docs/DECISIONS.md, tasks updated. Validation: full REPO_HEALTH battery green including the two new suites and the dry run; mirrors 138 files each.

## 2026-09-10: session log

B32: added scripts/label_eval_run.py (append-only human labels in docs/benchmarks/<iteration>/labels.jsonl, bound to the output sha256, one label per labeler, verdict good/weak/fail with ten classification handles), integrated labels into grade_evals.py (PASS_THRESHOLD 0.8 and DRIFT_THRESHOLD 0.10, human verdict and agreement per run, disagreement rate and grader_drift per skill and overall, classification histogram, labels without a local run counted and warned, --labels flag with a default path, HTML rows and columns), documented the label step and the report fields in docs/EVAL_PROTOCOL.md, and added scripts/test_label_eval_run.py (9 tests: append and duplicate refusal, hash and unknown-run refusal, invalid inputs, 0.5 disagreement with drift, null fields without labels, orphan label warns, iteration mismatch, majority and tie rules, handles documented). Validation: label, recorder, runner and grader suites green; validate_repo both parsers.

