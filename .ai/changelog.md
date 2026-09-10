# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: Two-anchor assertions and strict fixture pairs for the six new evals

B33-B37 evals rewritten after the owner's review of PR #21: the six new assertion blocks use two- or three-anchor sentence checks (in_one_sentence, count_at_least, anchors), one decision assertion per block and at most two negatives, so a keyword-only reply scores at most 2/6; the eval-design prompt drops the exact-four/twenty/thirty/10% numbers for task-proportional sizing with a threshold set beforehand, and the panel prompt drops 'with all lenses'. Each of the six fixture pairs now carries good, plausible bad, keyword_only (<= 0.34) and near_miss (fails exactly one named assertion); test_grade_evals registers the four and checks the near-miss failing set. Validation: test_grade_evals 118 fixtures, 6 strict pairs, 42/42 graded evals covered; grader smoke; validate_repo both parsers; mirrors synced; full REPO_HEALTH battery green.

## 2026-09-10: Merge main and renumber B31 to B39

Merged origin/main (PR #20, 474ce87) into the references batch: conflicts in the two changelog files, README and REPO_HEALTH resolved keeping both sides (PR #20 entries archived in chronological order, one README row per script, Frontmatter parsing heading kept). The pre-merge B31 item (render_html fix, pilot runner, runbook) is renumbered B39 in the backlog, tasks and this branch's changelog entries because PR #20 owns B31; commits cc054d7 and a9c490f keep the old label. Validation: full REPO_HEALTH battery green on the merged tree (106 fixtures, 42/42 graded evals covered, memory 46, context 11, contract 9, frontmatter 5, mirrors 138).

## 2026-09-10: session log

B32-B39 closing: protocol gained the runner section and the per-harness runbook, REPO_HEALTH and README list the new scripts and tests, CI runs the pilot-runner and label suites plus a manifest dry run, README eval counts recounted from the manifests (85 cases: 43/11/15/16) with no other hard-coded totals left, backlog rows B32-B39 with GUT and detail sections plus the batch table and the updated B25 pendency, five binding decisions in docs/DECISIONS.md, tasks updated. Validation: full REPO_HEALTH battery green including the two new suites and the dry run; mirrors 138 files each.

