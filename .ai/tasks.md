# Toolkit tasks

Project tasks live in `.ai/memory/projects/<slug>/tasks.md`. Toolkit implementation status is tracked in `.ai/backlog.md`.

- [x] Replace sector-specific examples with fictional collaboration scenarios (PR #18).
- [x] Implement and locally validate B24, B22, B28, B26, B27 and B30.
- [x] Provide the B25 recording protocol and validated run format.
- [x] Implement and locally validate B32 to B37 and B39 (grader fix, org layer, eval-design, prototyping ladder, review panel, batch synthesis and connector recipes, pilot runner, human labels).
- [x] Address the owner's review of PR #21 in the same PR: merge `main`, renumber B31 to B39, rewrite the six new assertion blocks with strict fixtures, composite label identity, runner guards, org corrections, proportional eval design, risk-selected panel.
- [x] Address the owner's second review (head `23fd183`): artefact anchors and punctuation variants, stale rubric labels, strict probe with configuration checks and immutable probe files bound to validation, completed Codex turns and per-attempt directories, org bootstrap confinement.
- [x] Address the owner's revalidation of head `ad4f467`: the configuration guarantee runs before any harness call and independently of `--skip-probe`; a `CODEX_HOME` with instructions or MCP servers in `config.toml`, or any entry the session would load, is refused; `-c`/`--config` overrides are refused.
- [ ] Execute the real B25 pilot with `scripts/run_eval_pilot.py` on a machine where both CLIs are authenticated, one iteration per harness; a smoke `--eval` run first, then list the harness version in `verified_harness_versions`.
- [ ] Label the recorded outputs with `scripts/label_eval_run.py` and publish `docs/benchmarks/<iteration>/report.md` per harness.
- [x] Integrate the consolidated implementation after CI validation: PR #19 merged as `7650b2d` and PR #20 as `474ce87` (2026-09-10), PR #21 as `4929635` (2026-09-14); rows in `docs/PR_HISTORY.md`. PRs #22 and #23 stay open.
- [ ] B38 candidate for a next cycle: positioning/GTM, build-vs-buy and win/loss references.
- [x] B40 (separate PR, 2026-09-14): every graded eval's assertion block checks relations, not terms; strict pairs (keyword-only in five joins, near miss, label soup) for 42 of 42 graded evals; 13 in-code fixtures moved to the JSON.
- [x] B41 (separate PR, 2026-09-14): every standard eval's assertion block checks relations, not terms; strict pairs for 43 of 43 standard evals (85 of 85 in total); the test requires a strict pair for every eval; B12, B18 and B20 in-code fixtures moved to the JSON.
