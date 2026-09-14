# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: Grader tests: every graded eval carries a strict pair

The coverage check in scripts/test_grade_evals.py, derived from the manifests, now also requires a strict pair (keyword_only plus near_miss) in the fixture JSON for every negative-control and adversarial eval, so the punctuation-variant and label-soup attacks run against every graded block rather than the ones someone remembered to harden. Standard evals may carry a strict pair; graded evals must. 42 of 42 graded evals pass; 45 pairs, all strict; 201 fixtures. Full REPO_HEALTH battery green.

## 2026-09-14: B40 pm-archetype-platform: relations, not terms, in two blocks; strict pairs

refuse-hidden-breaking-change-as-minor grows from five to seven assertions: the release refused with its object, the change classified by the promise it breaks, the additive or versioned path, the consumers put on the critical path with a verb, the deprecation window and the contract tests tied to both formats, the anti-pattern named by its consequence, and the negative on waving the patch through. additive-change-ships-as-minor grows from five to seven: the release decision with its version, why the change is additive, the contract tests as proof for the existing fields, the changelog and docs as the notice, the partner machinery kept for the cases it exists for, plus the two negatives. Both pairs gain keyword_only and near_miss fixtures; the bad fixtures are plausible wrong answers. Full REPO_HEALTH battery green.

## 2026-09-14: B40 pm-archetype-growth: relations, not terms, in two blocks; strict pairs; in-code fixtures moved to the JSON

challenge-activation-theatre-redefinition grows from five to eight assertions: the note declined with a verb and its object, the move named by what it changes and what it leaves alone, the definition kept for the reason the data gives, retention split with a comparison word, the cost of reporting the redefinition, the honest number with its evidence, the real work in flight, and the negative on delivering the note as briefed. clean-experiment-readout-ship grows from five to eight: ship with its scope, the lift put against the threshold with a verb, the primary result with its sample, at least two validity checks paired with outcomes, the guardrails read by what they did, the follow-up as monitoring, plus the two negatives. The four B11 growth fixtures that lived in the test file are now the good and bad fixtures of the two strict pairs in the JSON; the empty B11 section header is gone. Full REPO_HEALTH battery green.

