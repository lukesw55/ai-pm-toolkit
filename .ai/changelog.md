# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B31: removed the stray identity check in grade_evals.render_html (lines 1092-1095 referenced grade_all locals and raised NameError on the first recorded run); added test_report_renders_recorded_pair in scripts/test_record_eval_run.py, which failed with NameError before the fix and passes after. Validation: full docs/REPO_HEALTH.md battery green.

## 2026-09-10: Remaining backlog implementation

Implemented B24, B22, B28, B26, B27 and B30 in one consolidated change. Added B25 recorder and protocol; the real 60-output pilot remains pending because authenticated Claude Code and Codex runners are unavailable. B21 and B23 recorded as already integrated. Validation results are recorded in the PR; binding decisions are in docs/DECISIONS.md.

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

