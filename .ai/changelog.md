# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: Round 4: isolation guarantee before any harness call, independent of the probe; CODEX_HOME config.toml checked

The owner's revalidation of head ad4f467 found the configuration guarantee evaluated only inside the probe (so --skip-probe skipped it), reached only after the harness had already run once, and a codex_home_clean check that ignored config.toml. check_isolation now evaluates isolation_config on the run argv and the environment before the harness is started for anything, version query and probe included, refuses unless --allow-unisolated, and every sidecar records the checks whether or not the probe ran; --skip-probe skips the diagnostic only. codex_home_clean accepts only auth.json, the artefacts Codex writes while running and a config.toml limited to model and approval keys: any table, developer_instructions, model_instructions_file, notify, prompts, rules or any other entry is refused; a new no_config_overrides check refuses -c and --config on the argv; docs say a read-only sandbox proves nothing about attached tools. Regressions: an invalid template is refused with zero run_harness calls with and without --skip-probe and no probe or attempt written; --skip-probe with a valid configuration records the checks; a home with instructions and an MCP server is refused before any call while the same home with a model key passes; probe immutability stays green. Protocol, runbook, REPO_HEALTH, backlog and tasks updated. Full REPO_HEALTH battery green.

## 2026-09-14: B40 closing: protocol contract, repo health, README, decisions, backlog (B41 candidate), tasks

docs/EVAL_PROTOCOL.md gains the "Assertion and fixture contract" section (relations not co-occurrence, one decision assertion per block, at most two list-satisfied assertions with n >= 3k, labels without tokens, the four fixtures per pair, the two derived attacks, a strict pair required for every graded eval). docs/REPO_HEALTH.md describes what test_grade_evals.py enforces; the README row for the test names the five joins and the label-soup attack; docs/DECISIONS.md records "Assertions check relations, fixtures attack them". .ai/backlog.md marks B40 done with the before/after measurement (55 of 85 blocks passed their own labels, now 0 of 42 graded; 32 pairs with 6 strict, now 45 all strict; 201 fixtures; 13 in-code fixtures migrated) and opens B41 as a candidate for the 30 standard blocks that still pass their labels (34 standard evals without a fixture); the consolidated table and counts follow. .ai/tasks.md marks B40 and lists B41. validate_repo green in both modes; full REPO_HEALTH battery green.

## 2026-09-14: Grader tests: every graded eval carries a strict pair

The coverage check in scripts/test_grade_evals.py, derived from the manifests, now also requires a strict pair (keyword_only plus near_miss) in the fixture JSON for every negative-control and adversarial eval, so the punctuation-variant and label-soup attacks run against every graded block rather than the ones someone remembered to harden. Standard evals may carry a strict pair; graded evals must. 42 of 42 graded evals pass; 45 pairs, all strict; 201 fixtures. Full REPO_HEALTH battery green.

