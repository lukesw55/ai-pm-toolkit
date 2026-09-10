# Toolkit tasks

Project tasks live in `.ai/memory/projects/<slug>/tasks.md`. Toolkit implementation status is tracked in `.ai/backlog.md`.

- [x] Replace sector-specific examples with fictional collaboration scenarios (PR #18).
- [x] Implement and locally validate B24, B22, B28, B26, B27 and B30.
- [x] Provide the B25 recording protocol and validated run format.
- [x] Implement and locally validate B32 to B37 and B39 (grader fix, org layer, eval-design, prototyping ladder, review panel, batch synthesis and connector recipes, pilot runner, human labels).
- [ ] Execute the real B25 pilot with `scripts/run_eval_pilot.py` on a machine where both CLIs are authenticated, one iteration per harness.
- [ ] Label the recorded outputs with `scripts/label_eval_run.py` and publish `docs/benchmarks/<iteration>/report.md` per harness.
- [ ] Integrate the consolidated implementation after CI validation.
- [ ] B38 candidate for a next cycle: positioning/GTM, build-vs-buy and win/loss references.
