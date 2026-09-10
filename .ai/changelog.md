# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B33: added skills/pm-archetype-ai/references/eval-design.md (PM-owned eval method for AI features: scenario sheet, four hazards, four numeric limits, golden set with a real failure, block rule above the pass rate, validation and judge verification; original text adapted from Dean Peters with licence note) plus the skill's progressive-loading map, narrowed the single-file paragraph in that SKILL.md only, pointed workflow steps 3 and 6 and the pm-ai agent at it, added launch-gate and PRD one-liners, and eval 4 design-golden-set-and-block-rule-for-summariser with assertions and a good/bad fixture pair. README archetype and references sentences no longer carry a hard-coded count. Validation: validate_repo both parsers, test_grade_evals 89 fixtures, mirrors synced.

## 2026-09-10: session log

B35: wired the shared org layer into the read and persist paths: a required-reading bullet in the four archetype skills, an org hint in the load-context step of discover, define, develop, deliver, analysis, stakeholder and comms, an enrichment clause in the persist step of discover, define and deliver, and a required-reading bullet in the ten Copilot agents. Validation: validate_repo (both parsers), test_validate_repo, mirrors synced.

## 2026-09-10: session log

B35: shared org layer (.ai/memory/org/: company, personas, competitors, goals) with templates under _templates/org/, init_context.py --org bootstrap that never overwrites, reserved slug 'org', doctor soft caps for org files and the new per-project insights.md template; missing templates now fail with a message instead of a traceback; canonical research paths reconciled in pm-transversal-analysis references (raw-evidence for PII, research/<topic>/sessions for excerpt logs, discovery/<topic>/synthesis.md for memos, insights.md for ranked themes); docs updated (MEMORY_SYSTEM tree and roles, memory README, README, AGENTS, CLAUDE, REPO_HEALTH, repo-doctor). Validation: test_context_scripts 11 tests, test_memory 45 cases, full REPO_HEALTH battery green, mirrors synced.

