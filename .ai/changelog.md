# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B31-B38 closing: protocol gained the runner section and the per-harness runbook, REPO_HEALTH and README list the new scripts and tests, CI runs the pilot-runner and label suites plus a manifest dry run, README eval counts recounted from the manifests (85 cases: 43/11/15/16) with no other hard-coded totals left, backlog rows B31-B38 with GUT and detail sections plus the batch table and the updated B25 pendency, five binding decisions in docs/DECISIONS.md, tasks updated. Validation: full REPO_HEALTH battery green including the two new suites and the dry run; mirrors 138 files each.

## 2026-09-10: session log

B32: added scripts/label_eval_run.py (append-only human labels in docs/benchmarks/<iteration>/labels.jsonl, bound to the output sha256, one label per labeler, verdict good/weak/fail with ten classification handles), integrated labels into grade_evals.py (PASS_THRESHOLD 0.8 and DRIFT_THRESHOLD 0.10, human verdict and agreement per run, disagreement rate and grader_drift per skill and overall, classification histogram, labels without a local run counted and warned, --labels flag with a default path, HTML rows and columns), documented the label step and the report fields in docs/EVAL_PROTOCOL.md, and added scripts/test_label_eval_run.py (9 tests: append and duplicate refusal, hash and unknown-run refusal, invalid inputs, 0.5 disagreement with drift, null fields without labels, orphan label warns, iteration mismatch, majority and tie rules, handles documented). Validation: label, recorder, runner and grader suites green; validate_repo both parsers.

## 2026-09-10: session log

B31: added scripts/run_eval_pilot.py (pilot runner: builds the without_skill and with_skill payloads from docs/benchmarks/pilot-deps.json with sha256 per loaded file, runs the harness CLI in a fresh directory outside the repo with the payload on stdin, randomises the config order per eval from a printed seed, parses the Claude Code JSON envelope and the Codex event stream, refuses empty output, mixed harness, dirty tree and already-recorded runs, records through record_eval_run.record() and writes a provenance.json sidecar), the dependency manifest, and scripts/test_run_eval_pilot.py with a fake harness (9 tests: 30 recorded runs graded end to end, seeded order, empty output, mixed harness, resume, dirty tree, dry run, codex stream, bad envelopes). Claude Code flags confirmed against claude -p --help 2.1.267; Codex template to be verified on the pilot machine. Validation: tests, dry run, validate_repo both parsers.

