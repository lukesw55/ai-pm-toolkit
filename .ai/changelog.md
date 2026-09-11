# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: B40 pm-phase-develop: relations, not terms

B40 pm-phase-develop: the two graded blocks (challenge-unjustified-scope-expansion, solid-prd-scope-agree) now check relations between the prompt's anchors (the additions and what they lack, the kept scope and its evidence, the non-goals and their reason, the rollout and its rollback path), one explicit decision assertion each, at most two trivially satisfied (n 6, 8). Strict pairs in the JSON with plausible bad answers (the bundled PRD; the thin-evidence delay plus SCIM). Validation: full REPO_HEALTH battery green.

## 2026-09-11: B40 pm-phase-define: relations, not terms

B40 pm-phase-define: the four graded blocks (challenge-weak-prioritisation-rationale, solid-prioritisation-rationale-agree, refuse-orphan-solution-in-one-pager, select-validated-bet-and-slice-v1) now check relations between the prompt's anchors, carry one explicit decision assertion each and at most two trivially satisfied ones (n 6, 7, 7, 9). Strict pairs in the JSON; the B12 and stage-5 in-code fixtures moved into the JSON as the pairs' good and bad; the bad answers are the compliant rationale and the RICE rerun, not lists of forbidden phrases. Keyword list worst join 0.29, label soup worst 0.17. Validation: full REPO_HEALTH battery green.

## 2026-09-11: B40 pm-phase-discover: relations, not terms

B40 pm-phase-discover: the three graded blocks (resist-solution-first-dashboard-premise, solid-research-plan-agree, update-impact-brief-and-test-feasibility-during-discovery) now check two anchors with a verb or connector between them, carry one explicit decision assertion each and at most two trivially satisfied ones (n 6, 8, 8). Strict pairs added to the fixture JSON (plausible bad, keyword list, near miss failing one named assertion); the B11/B31 in-code fixtures for these evals moved into the JSON as the pairs' good and bad; the pedagogical fixture 1 was rewrapped so its first sentence sits on one line (spans stop at line breaks, like the sentence splitter). Keyword list worst join 0.25, label soup worst 0.17. Validation: full REPO_HEALTH battery green (test_grade_evals 125 fixtures, 9 strict pairs, 36 variants, 45 soup texts).

