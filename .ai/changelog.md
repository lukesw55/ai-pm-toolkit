# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: Round 4: isolation guarantee before any harness call, independent of the probe; CODEX_HOME config.toml checked

The owner's revalidation of head ad4f467 found the configuration guarantee evaluated only inside the probe (so --skip-probe skipped it), reached only after the harness had already run once, and a codex_home_clean check that ignored config.toml. check_isolation now evaluates isolation_config on the run argv and the environment before the harness is started for anything, version query and probe included, refuses unless --allow-unisolated, and every sidecar records the checks whether or not the probe ran; --skip-probe skips the diagnostic only. codex_home_clean accepts only auth.json, the artefacts Codex writes while running and a config.toml limited to model and approval keys: any table, developer_instructions, model_instructions_file, notify, prompts, rules or any other entry is refused; a new no_config_overrides check refuses -c and --config on the argv; docs say a read-only sandbox proves nothing about attached tools. Regressions: an invalid template is refused with zero run_harness calls with and without --skip-probe and no probe or attempt written; --skip-probe with a valid configuration records the checks; a home with instructions and an MCP server is refused before any call while the same home with a model key passes; probe immutability stays green. Protocol, runbook, REPO_HEALTH, backlog and tasks updated. Full REPO_HEALTH battery green.

## 2026-09-11: Round 3 closing: review section and recounts

Round 3 of PR #21 closed: backlog gained the 'Revisão do head 23fd183' section mapping the five reproduced findings to commits dad9608, 994632b, d917af4, 9d955e2 and a4d009c, with the counts recounted (runner 15, labels 13, context 12, 24 punctuation variants); tasks updated. The five reproductions were re-run on the fixed tree and none reproduces. Validation: validate_repo both parsers, doctor, git diff --check.

## 2026-09-11: Org bootstrap confines the destination before writing

Round 3 of PR #21, finding 5: init_context.py --org checks confinement before creating anything: when .ai/memory or .ai/memory/org is, or sits behind, a symlink, it exits 1 and writes nothing (the old guard only resolved the path once org/ existed, so a symlinked ancestor let the four files land outside the repository). Regression relocates .ai/memory behind a symlink and requires exit 1 with nothing created outside. MEMORY_SYSTEM states the rule. Validation: test_context_scripts 12, full REPO_HEALTH battery green.

