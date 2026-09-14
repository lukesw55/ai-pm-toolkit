# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: B41 closing: protocol, repo health, README, decisions, backlog, tasks

docs/EVAL_PROTOCOL.md says a strict pair is required for every eval, the standard ones included since B41; docs/REPO_HEALTH.md and the README row for test_grade_evals.py say the same; docs/DECISIONS.md extends the relations-not-terms decision to every eval and names both PRs. .ai/backlog.md marks B41 done with the before and after measurement (30 of 43 standard blocks passed their own label soup, now 0 of 85 with a maximum of 0.33; 45 pairs to 85, one per eval, all strict; 356 fixtures, 340 punctuation variants, 425 label soups), the migrated fixtures, the two tightened deck checks and the new lessons; the consolidated table and the count line follow. .ai/tasks.md closes the B41 line. No code change. Full REPO_HEALTH battery green.

## 2026-09-14: Grader tests: every eval carries a strict pair

The coverage check in scripts/test_grade_evals.py stops filtering the manifests by category: every eval of every skill now needs a fixture that must score at or above 0.80, a fixture that must score at or below 0.34, and a strict pair with keyword_only and near_miss, so the derived punctuation and label-soup attacks run against all 85 blocks. The docstring, the comments and the PASS and failure messages say "every eval" instead of "every graded eval". No fixture changes: the 43 standard pairs landed one skill per commit before this. Full REPO_HEALTH battery green.

## 2026-09-14: B41 pm-archetype-platform: relations, not terms, in one standard block; strict pair

deprecate-v1-webhooks-with-migration grows from five to seven assertions: a dated sunset window with the number attached to the window or the stop date, the consumer inventory with the prompt's numbers in a relation, the migration tooling tied to the window with a verb, the comms cadence with intervals plus the direct outreach to the partners, migration tracked with SLOs held during the transition, version skew handled with a rollback path, and the decision left as a written record of why v1 goes. The pair carries keyword_only and near_miss fixtures; the bad fixture switches v1 off next quarter on a newsletter notice. Full REPO_HEALTH battery green.

