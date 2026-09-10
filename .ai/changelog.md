# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B35: wired the shared org layer into the read and persist paths: a required-reading bullet in the four archetype skills, an org hint in the load-context step of discover, define, develop, deliver, analysis, stakeholder and comms, an enrichment clause in the persist step of discover, define and deliver, and a required-reading bullet in the ten Copilot agents. Validation: validate_repo (both parsers), test_validate_repo, mirrors synced.

## 2026-09-10: session log

B35: shared org layer (.ai/memory/org/: company, personas, competitors, goals) with templates under _templates/org/, init_context.py --org bootstrap that never overwrites, reserved slug 'org', doctor soft caps for org files and the new per-project insights.md template; missing templates now fail with a message instead of a traceback; canonical research paths reconciled in pm-transversal-analysis references (raw-evidence for PII, research/<topic>/sessions for excerpt logs, discovery/<topic>/synthesis.md for memos, insights.md for ranked themes); docs updated (MEMORY_SYSTEM tree and roles, memory README, README, AGENTS, CLAUDE, REPO_HEALTH, repo-doctor). Validation: test_context_scripts 11 tests, test_memory 45 cases, full REPO_HEALTH battery green, mirrors synced.

## 2026-09-10: session log

B31: removed the stray identity check in grade_evals.render_html (lines 1092-1095 referenced grade_all locals and raised NameError on the first recorded run); added test_report_renders_recorded_pair in scripts/test_record_eval_run.py, which failed with NameError before the fix and passes after. Validation: full docs/REPO_HEALTH.md battery green.

