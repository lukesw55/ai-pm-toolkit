# Contributing

Three rules are not guessable from the tree. Everything else follows the code you are editing.

## 1. Run the battery before every commit

`docs/REPO_HEALTH.md` holds the full checklist. These are the commands that run on a clean clone in any state, from the repo root:

```bash
bash scripts/check_requirements.sh
python3 -m py_compile scripts/*.py
for hook in hooks/*.sh; do bash -n "$hook" || exit; done
python3 scripts/sync_skills.py --check
python3 scripts/validate_repo.py
python3 -S scripts/validate_repo.py
python3 scripts/test_hooks.py
python3 scripts/test_hook_contract.py
python3 scripts/test_grade_evals.py
python3 scripts/test_memory.py
python3 scripts/test_context_scripts.py
python3 scripts/test_record_eval_run.py
python3 scripts/test_run_eval_pilot.py
python3 scripts/test_label_eval_run.py
python3 scripts/test_propose_eval_updates.py
python3 scripts/test_golden_set.py
python3 scripts/test_validate_repo.py
python3 scripts/test_frontmatter.py
python3 scripts/grade_evals.py
python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-dry-run --model dry-run --dry-run --allow-dirty
```

`python3 -S scripts/validate_repo.py` is the second run on purpose: it disables site packages, so the validator has to parse frontmatter without PyYAML and reach the same verdict. CI runs both ways on Python 3.10 and 3.11.

`memory.py doctor` is absent on purpose. Real memory is gitignored, so a fresh checkout has no active project and the command exits 1 by definition; CI bootstraps a throwaway project before calling it, and the bootstrap smoke test in `docs/REPO_HEALTH.md` is the sequence to run by hand. You lose no coverage by leaving it out: `validate_repo.py` already runs that whole bootstrap in a copy of the tree, so the contract is checked without writing to the memory in your clone.

Toolkit changes are logged with `python3 scripts/memory.py log repo "<what changed and how it was validated>"`, which writes the versioned changelog. A `Stop` hook reminds you when files changed and no entry followed.

## 2. `skills/` is canonical; the two mirrors are generated

Skills are hand-edited in `skills/` and nowhere else. `.claude/skills/` and `.agents/skills/` are byte copies produced by `python3 scripts/sync_skills.py`, committed alongside the change. `validate_repo.py` fails on drift, so an edit to a mirror is caught rather than silently overwritten later.

`hooks/` is canonical too, used directly by both adapters. What differs per harness is only the wiring: `.claude/settings.json` and `.codex/hooks.json`, and the routing contract both must satisfy is `hooks/contract.json`.

## 3. An eval case needs an assertion block

Every skill carries `evals/evals.json` with at least three cases, one of them adversarial, and the five doctrine skills also need a negative control. Each case must have a matching block in the `ASSERTIONS` dictionary of `scripts/grade_evals.py`, one to one, and a fixture pair in `scripts/fixtures/adversarial_outputs.json`. The contract those fixtures have to satisfy is written in `docs/EVAL_PROTOCOL.md`: a good answer scores at least 0.80, a plausible wrong answer at most 0.30, a keyword-only reply at most 0.34 in five punctuation joins, and the block's own assertion labels, read back as an answer, fail too.

That last one is the point of the exercise. An assertion a list of the right words can satisfy is matching vocabulary, not behaviour.

## The README is checked

`validate_repo.py` derives the skill, hook, agent and eval counts from the tree and compares them against the sentences in `README.md`, requires a row in the scripts table for every file in `scripts/`, and requires the contents list to match the headings. Adding a skill or a script therefore turns CI red until the README says so.

That is deliberate: a README that drifts is worse than no README, because it is read as current. Each validated count is written once, as a digit, and the error message names both numbers.

## Pull requests

Record the validation you ran against the exact head you are asking someone to review, and say what you did not check. A self-review is not independent approval. If the work is separable, open separate pull requests.
