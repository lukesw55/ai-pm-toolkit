# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Composite label identity, supersede, split verdicts, two disagreement rates

B32 revised after the owner's review of PR #21: labels.jsonl moves to schema 2 with a composite run identity (iteration, skill, eval_id, config, output_sha256), rubric_version (12 hex of prompt + expected_output), corrections through --supersede with the history kept in the file, a tie between labelers reported as a split awaiting resolution instead of the worse verdict, and the grader reporting human disagreement and grader disagreement separately with investigate_grader (threshold set before the run) replacing grader_drift, since drift needs a comparison across iterations. Protocol, DECISIONS, README, REPO_HEALTH and backlog updated. Validation: test_label_eval_run 12 tests including identical text under both configurations keeping separate labels; recorder, runner and grader suites; full REPO_HEALTH battery green.

## 2026-09-10: Two-anchor assertions and strict fixture pairs for the six new evals

B33-B37 evals rewritten after the owner's review of PR #21: the six new assertion blocks use two- or three-anchor sentence checks (in_one_sentence, count_at_least, anchors), one decision assertion per block and at most two negatives, so a keyword-only reply scores at most 2/6; the eval-design prompt drops the exact-four/twenty/thirty/10% numbers for task-proportional sizing with a threshold set beforehand, and the panel prompt drops 'with all lenses'. Each of the six fixture pairs now carries good, plausible bad, keyword_only (<= 0.34) and near_miss (fails exactly one named assertion); test_grade_evals registers the four and checks the near-miss failing set. Validation: test_grade_evals 118 fixtures, 6 strict pairs, 42/42 graded evals covered; grader smoke; validate_repo both parsers; mirrors synced; full REPO_HEALTH battery green.

## 2026-09-10: Merge main and renumber B31 to B39

Merged origin/main (PR #20, 474ce87) into the references batch: conflicts in the two changelog files, README and REPO_HEALTH resolved keeping both sides (PR #20 entries archived in chronological order, one README row per script, Frontmatter parsing heading kept). The pre-merge B31 item (render_html fix, pilot runner, runbook) is renumbered B39 in the backlog, tasks and this branch's changelog entries because PR #20 owns B31; commits cc054d7 and a9c490f keep the old label. Validation: full REPO_HEALTH battery green on the merged tree (106 fixtures, 42/42 graded evals covered, memory 46, context 11, contract 9, frontmatter 5, mirrors 138).

