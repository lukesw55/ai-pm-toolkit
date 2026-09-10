# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-10: session log

B37: added skills/pm-transversal-analysis/references/batch-interview-synthesis.md (shared codebook first, one excerpt log per transcript, fan-out where the harness offers subagents with a sequential fallback, merge by participants with counter-evidence, saturation and recency checks, PII kept in raw-evidence) and references/connector-task-recipes.md (recipe contract plus launch retro from Jira tickets, feature adoption from analytics, behaviour-split retention; numbers only from tool results, source links, persistence with query text, TBD rules), sub-skills 5 and 6, load and persist steps and the MCP integration bullet in the SKILL.md, two progressive-loading rows, root SKILL and README blurbs, the AGENTS known-degradation note, and evals 3 (standard batch synthesis) and 4 (skill-functional-adversarial: refuse the 2x retention claim no tool returned) with assertions and fixture pairs. Validation: validate_repo both parsers, test_grade_evals 99 fixtures, test_frontmatter, mirrors synced.

## 2026-09-10: session log

B36: added skills/pm-transversal-stakeholder/references/review-panel.md (five stakeholder lenses with cards, the rule that no objection is a valid output and a manufactured one is a doctrine-7 failure, panel report template, sequential default with subagent fan-out where available, consolidation into the dissent protocol and the assumption map, never a gate), sub-skill 4 and persist path in the SKILL.md, progressive-loading row, one sentence in the WORKFLOW shadow-gate paragraph, an AGENTS known-degradation note for Codex, root SKILL and README blurbs, and evals 3 (skill-functional-adversarial: hidden discount-revenue exposure) and 4 (negative-control: clean PRD cleared without an invented objection) with assertions and fixture pairs. Validation: validate_repo both parsers, test_grade_evals 95 fixtures, mirrors synced.

## 2026-09-10: session log

B34: added skills/pm-phase-develop/references/prototyping-ladder.md (three prototype tiers by where they live and what they cost engineering: throwaway, code prototype on a disposable branch of the real codebase via a coding agent, PM-authored PR for copy/config/flags/minor UI and never core logic; sandbox repo request and prototype decision record templates; decision table; link to the stage-6 gate), sub-skill 7 and persist path in the SKILL.md, progressive-loading row, WORKFLOW stage-6 row now cites the reference and records the tier, stage_context fallback string, README and root SKILL rows, and eval 4 choose-prototype-tier-for-billing-change with assertions and fixture pair. Validation: validate_repo both parsers, test_grade_evals 91 fixtures, test_context_scripts, mirrors synced.

