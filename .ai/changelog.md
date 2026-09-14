# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: PR history: #22 integrated

docs/PR_HISTORY.md gains the row for PR #22 (B40), merged into main on 2026-09-14T22:24:50Z as the merge commit b51ddd3, verified against the fetched main; the intro sentence now says the rows for #19 to #22 were added from the PR metadata. .ai/tasks.md closes #22 in the integration line and leaves #23 open. Docs only; full battery green before the commit.

## 2026-09-14: B41 review: soft wraps are not structure; repo-doctor accepts the honest zero

The grader reads every assertion through unwrap_soft_breaks: a line break after a full line (the next word would pass the reply's longest multi-word line, which is how a wrapper breaks) is a soft wrap and rejoins; blank lines, headings, list items, table rows, block quotes, fences, slide headers and a labelled field under a heading stay boundaries; a line that is not full stays a paragraph end; a reply whose longest line is under 40 characters is left alone. The ASSERTIONS dict is wrapped after definition, so grade_run and the tests' direct calls see the same text, and the deck fields no longer need a line start. validate-skill-repo-health: a failure needs its path (a failure state, not any verb) and one remedy; a clean tree passes both assertions on the strength of at least two check-and-result relations; a bare "all green" that names no check passes neither. near_miss.fails follows the new label. test_grade_evals: <eval>-good-wrapped for all 85 pairs at floor 0.80 (all score 1.00), zero- and one-finding repo-doctor controls (1.00, also wrapped) and a bare all-clear at 0.00, unit checks for the normaliser. 446 fixtures; keyword-only variants and label soups stay at 0.33 or below, the newline joins now through the normaliser. Docs: EVAL_PROTOCOL contract rules 7 and 8, REPO_HEALTH, README, backlog section for the review, tasks. Validation: full docs/REPO_HEALTH.md battery green before the commit.

## 2026-09-14: PR history: #19 to #21 integrated

docs/PR_HISTORY.md gains the rows for the three pull requests merged since the backfill, each with its UTC merge time and the merge commit on main verified against the GitHub API: #19 (7650b2d, 2026-09-10), #20 (474ce87, 2026-09-10) and #21 (4929635, 2026-09-14, a merge commit, not a squash, so the stacked branches need no base merge). The intro sentence records the addition date. .ai/tasks.md closes the integration line with the same references. No code change. Full REPO_HEALTH battery green.

