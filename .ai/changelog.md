# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Codex results need a completed turn; one directory per attempt

Round 3 of PR #21, finding 4: parse_codex_jsonl accepts a stream only when its turn completed (turn.failed or error refused, missing turn.completed refused), and every harness attempt runs in its own attempt-NN directory so a resume with --skip-recorded in the same work directory records the pair while the failed attempt's stdout and stderr stay in place; attempts.jsonl carries the attempt number. Validation: test_run_eval_pilot 15 (partial stream with turn.failed refused, fail then resume keeps attempt-01), recorder and label suites, full REPO_HEALTH battery green.

## 2026-09-11: Strict probe, explicit configuration checks, immutable probes bound to validation

Round 3 of PR #21, finding 3: parse_probe accepts only two lines, TOOLS then INSTRUCTIONS, and fails closed on an extra line, a repeated field or a contradiction (format_ok recorded); isolation_config checks the process explicitly per harness (Claude Code: --safe-mode, --strict-mcp-config, --tools '', --permission-prompts none; Codex: --sandbox read-only, --skip-git-repo-check, CODEX_HOME without AGENTS.md, skills or hooks; both: cwd outside the repo) and a missing check refuses the run unless --allow-unisolated; every invocation writes its own probe file under docs/benchmarks/<iteration>/probes/ and never overwrites one; the sidecar carries the probe reference, the config and skip_probe, and record_eval_run.validate_run requires the referenced probe to exist with the recorded hash and content. Protocol and REPO_HEALTH describe the probe as a diagnostic on top of the configuration guarantee. Validation: test_run_eval_pilot 14 (contradictory probe, unsafe template refused, two invocations keep both probes valid, tampered or missing probe fails validation), recorder and label suites, full REPO_HEALTH battery green.

## 2026-09-11: Stale rubric labels are reported, never counted

Round 3 of PR #21, finding 2: a label whose rubric_version differs from the eval's current prompt and expected output is stale. label_eval_run.split_by_rubric separates current from stale labels; grade_all keeps only current labels for the human verdict and the rates, reports stale ones in grading.json and the benchmark (labels_stale), warns per stale label, and label() lets the same labeler relabel against the current rubric without --supersede while the old record stays in the file (then counted as superseded). Regression: change only expected_output after labelling; the verdict becomes null, labels_stale is 1, relabelling works. Protocol and REPO_HEALTH updated. Validation: test_label_eval_run 13, runner and recorder suites, full REPO_HEALTH battery green.

