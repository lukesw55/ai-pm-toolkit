# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Review panel selects lenses by risk and names the ones not run

B36 revised after the owner's review of PR #21: the review panel selects lenses by the exposure the artefact touches (exposure-to-lens table in review-panel.md) instead of running five as a ritual, every lens not run is named in the report with a one-line reason, an author's request to skip a lens because it might object is the reason to run it, and a 'ritual panel' anti-pattern was added; sub-skill 4, the WORKFLOW shadow-gate sentence, the progressive-loading row, root SKILL and README blurbs and the backlog say risk-selected instead of five-lens. The adversarial eval (M3) already requires the commercial objection to name the omitted 62% discount exposure. Validation: validate_repo both parsers, test_grade_evals 118, mirrors synced; full REPO_HEALTH battery green.

## 2026-09-11: Eval design sized to the task; recipe contract gains completeness, unit and time zone

B33 and B37 revised after the owner's review of PR #21: eval-design.md no longer turns Peters' worked-example numbers into rules (hazard list and limits block sized to the task, each limit with a rationale written before the run, golden set sized and justified, verification against a threshold set beforehand with about thirty cases and one in ten as starting points), the failure taxonomy gained a 'counts as a failure when' column so asking a question or omitting a citation fails only where the task contract requires the opposite, a critical failure is never offset by a high average, and drift is claimed only against the previous verification. connector-task-recipes.md: the contract gained Completeness (paged to the end, total against fetched), Unit and deduplication, and Time zone; each recipe carries the three; Recipe 3 defines the behaviour observation window (days 0 to 7) closed before the retention window and names leakage as a check. Sub-skill 6, DECISIONS and backlog follow. Validation: validate_repo both parsers, test_grade_evals 118, mirrors synced; full REPO_HEALTH battery green.

## 2026-09-11: Org layer: slug unreserved, precedence rule, verifiable personal-data check

B35 revised after the owner's review of PR #21: the project slug 'org' is no longer reserved (projects/org/ and org/ are different directories; test replaced by one where both coexist), the precedence rule is explicit in MEMORY_SYSTEM, the four org templates, CLAUDE.md and AGENTS.md (for a project's decisions the project files win; a divergence goes to that project's decisions.md before the org file changes, logged with memory.py log), and the personal-data rule became verifiable: memory.py doctor warns on e-mail and phone patterns in org/*.md, names stay a review rule, pseudonymisation is described as lowering, not removing, re-identification risk. DECISIONS row and backlog updated. Validation: test_context_scripts 11, test_memory 48 (e-mail and phone flagged; dates and counts not), validate_repo both parsers, doctor, mirrors synced; full REPO_HEALTH battery green.

