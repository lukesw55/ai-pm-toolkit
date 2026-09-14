# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: B40 closing: protocol contract, repo health, README, decisions, backlog (B41 candidate), tasks

docs/EVAL_PROTOCOL.md gains the "Assertion and fixture contract" section (relations not co-occurrence, one decision assertion per block, at most two list-satisfied assertions with n >= 3k, labels without tokens, the four fixtures per pair, the two derived attacks, a strict pair required for every graded eval). docs/REPO_HEALTH.md describes what test_grade_evals.py enforces; the README row for the test names the five joins and the label-soup attack; docs/DECISIONS.md records "Assertions check relations, fixtures attack them". .ai/backlog.md marks B40 done with the before/after measurement (55 of 85 blocks passed their own labels, now 0 of 42 graded; 32 pairs with 6 strict, now 45 all strict; 201 fixtures; 13 in-code fixtures migrated) and opens B41 as a candidate for the 30 standard blocks that still pass their labels (34 standard evals without a fixture); the consolidated table and counts follow. .ai/tasks.md marks B40 and lists B41. validate_repo green in both modes; full REPO_HEALTH battery green.

## 2026-09-14: Grader tests: every graded eval carries a strict pair

The coverage check in scripts/test_grade_evals.py, derived from the manifests, now also requires a strict pair (keyword_only plus near_miss) in the fixture JSON for every negative-control and adversarial eval, so the punctuation-variant and label-soup attacks run against every graded block rather than the ones someone remembered to harden. Standard evals may carry a strict pair; graded evals must. 42 of 42 graded evals pass; 45 pairs, all strict; 201 fixtures. Full REPO_HEALTH battery green.

## 2026-09-14: B40 pm-archetype-platform: relations, not terms, in two blocks; strict pairs

refuse-hidden-breaking-change-as-minor grows from five to seven assertions: the release refused with its object, the change classified by the promise it breaks, the additive or versioned path, the consumers put on the critical path with a verb, the deprecation window and the contract tests tied to both formats, the anti-pattern named by its consequence, and the negative on waving the patch through. additive-change-ships-as-minor grows from five to seven: the release decision with its version, why the change is additive, the contract tests as proof for the existing fields, the changelog and docs as the notice, the partner machinery kept for the cases it exists for, plus the two negatives. Both pairs gain keyword_only and near_miss fixtures; the bad fixtures are plausible wrong answers. Full REPO_HEALTH battery green.

