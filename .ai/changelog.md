# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B34: added skills/pm-phase-develop/references/prototyping-ladder.md (three prototype tiers by where they live and what they cost engineering: throwaway, code prototype on a disposable branch of the real codebase via a coding agent, PM-authored PR for copy/config/flags/minor UI and never core logic; sandbox repo request and prototype decision record templates; decision table; link to the stage-6 gate), sub-skill 7 and persist path in the SKILL.md, progressive-loading row, WORKFLOW stage-6 row now cites the reference and records the tier, stage_context fallback string, README and root SKILL rows, and eval 4 choose-prototype-tier-for-billing-change with assertions and fixture pair. Validation: validate_repo both parsers, test_grade_evals 91 fixtures, test_context_scripts, mirrors synced.

## 2026-09-10: session log

B33: added skills/pm-archetype-ai/references/eval-design.md (PM-owned eval method for AI features: scenario sheet, four hazards, four numeric limits, golden set with a real failure, block rule above the pass rate, validation and judge verification; original text adapted from Dean Peters with licence note) plus the skill's progressive-loading map, narrowed the single-file paragraph in that SKILL.md only, pointed workflow steps 3 and 6 and the pm-ai agent at it, added launch-gate and PRD one-liners, and eval 4 design-golden-set-and-block-rule-for-summariser with assertions and a good/bad fixture pair. README archetype and references sentences no longer carry a hard-coded count. Validation: validate_repo both parsers, test_grade_evals 89 fixtures, mirrors synced.

## 2026-09-10: session log

B35: wired the shared org layer into the read and persist paths: a required-reading bullet in the four archetype skills, an org hint in the load-context step of discover, define, develop, deliver, analysis, stakeholder and comms, an enrichment clause in the persist step of discover, define and deliver, and a required-reading bullet in the ten Copilot agents. Validation: validate_repo (both parsers), test_validate_repo, mirrors synced.

