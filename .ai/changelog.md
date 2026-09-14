# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: Grader tests: every eval carries a strict pair

The coverage check in scripts/test_grade_evals.py stops filtering the manifests by category: every eval of every skill now needs a fixture that must score at or above 0.80, a fixture that must score at or below 0.34, and a strict pair with keyword_only and near_miss, so the derived punctuation and label-soup attacks run against all 85 blocks. The docstring, the comments and the PASS and failure messages say "every eval" instead of "every graded eval". No fixture changes: the 43 standard pairs landed one skill per commit before this. Full REPO_HEALTH battery green.

## 2026-09-14: B41 pm-archetype-platform: relations, not terms, in one standard block; strict pair

deprecate-v1-webhooks-with-migration grows from five to seven assertions: a dated sunset window with the number attached to the window or the stop date, the consumer inventory with the prompt's numbers in a relation, the migration tooling tied to the window with a verb, the comms cadence with intervals plus the direct outreach to the partners, migration tracked with SLOs held during the transition, version skew handled with a rollback path, and the decision left as a written record of why v1 goes. The pair carries keyword_only and near_miss fixtures; the bad fixture switches v1 off next quarter on a newsletter notice. Full REPO_HEALTH battery green.

## 2026-09-14: B41 pm-archetype-growth: relations, not terms, in one standard block; strict pair

design-activation-experiment grows from five to seven assertions: the hypothesis in the if/then/because form with content between the connectors and the baseline moved to a target, the primary metric as a field plus at least two guardrails with a direction, the sample and duration derived from the signup volume with a verb, ship, iterate and kill thresholds as numbers, at least two validity risks each with its check, the follow-up if the result is green, and the funnel layer with its baseline. The pair carries keyword_only and near_miss fixtures; the bad fixture runs it for a couple of weeks and ships if it looks better. Full REPO_HEALTH battery green.

