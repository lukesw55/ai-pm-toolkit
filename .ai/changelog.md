# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Pilot runner: measurement scope, isolation probe, attempts log, sidecar validation

B39 revised after the owner's review of PR #21: run_eval_pilot.py states what the pilot measures (an instruction bundle's effect on one response; not routing, progressive loading, hooks, memory or MCP; comparisons only inside one harness), runs an isolation probe before the runs and fails closed when the session reports tools or instructions (docs/benchmarks/<iteration>/isolation-probe.json, referenced from every sidecar), appends every invocation to docs/benchmarks/<iteration>/attempts.jsonl with status and error so failures stay on record, keeps stdout and stderr in the run directory on failure too, writes output_sha256 into provenance.json which record_eval_run.validate_run now checks against the run (output hash, payload hash, loaded SKILL.md), and refuses a full iteration on a harness version not listed under verified_harness_versions in pilot-deps.json (empty until a smoke run parses the envelope). Protocol gained 'What the pilot measures' and the isolation checklist; REPO_HEALTH and README say the fake-harness suite tests code paths, not CLI compatibility. Validation: test_run_eval_pilot 12 tests, recorder and label suites, dry run, full REPO_HEALTH battery green.

## 2026-09-11: Composite label identity, supersede, split verdicts, two disagreement rates

B32 revised after the owner's review of PR #21: labels.jsonl moves to schema 2 with a composite run identity (iteration, skill, eval_id, config, output_sha256), rubric_version (12 hex of prompt + expected_output), corrections through --supersede with the history kept in the file, a tie between labelers reported as a split awaiting resolution instead of the worse verdict, and the grader reporting human disagreement and grader disagreement separately with investigate_grader (threshold set before the run) replacing grader_drift, since drift needs a comparison across iterations. Protocol, DECISIONS, README, REPO_HEALTH and backlog updated. Validation: test_label_eval_run 12 tests including identical text under both configurations keeping separate labels; recorder, runner and grader suites; full REPO_HEALTH battery green.

## 2026-09-10: Two-anchor assertions and strict fixture pairs for the six new evals

B33-B37 evals rewritten after the owner's review of PR #21: the six new assertion blocks use two- or three-anchor sentence checks (in_one_sentence, count_at_least, anchors), one decision assertion per block and at most two negatives, so a keyword-only reply scores at most 2/6; the eval-design prompt drops the exact-four/twenty/thirty/10% numbers for task-proportional sizing with a threshold set beforehand, and the panel prompt drops 'with all lenses'. Each of the six fixture pairs now carries good, plausible bad, keyword_only (<= 0.34) and near_miss (fails exactly one named assertion); test_grade_evals registers the four and checks the near-miss failing set. Validation: test_grade_evals 118 fixtures, 6 strict pairs, 42/42 graded evals covered; grader smoke; validate_repo both parsers; mirrors synced; full REPO_HEALTH battery green.

