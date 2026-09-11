# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Grader tests: strict pairs also fail their own labels

B40 commit 1: test_grade_evals.py joins each strict block's assertion labels the five ways it joins the keyword list (full stop, semicolon, comma, newline, and) and requires every text at or below 0.34, the attack the PR #21 review applied by hand. The six strict blocks' labels now describe the check without the tokens it looks for, so the derived soup fails them (worst join 0.33, against 0.83 before on the prototype block); two near_miss targets follow their labels; the docstring states the strict-pair contract. Validation: full REPO_HEALTH battery green (test_grade_evals 118 fixtures, 24 punctuation variants, 30 label-soup texts).

## 2026-09-11: Round 3 closing: review section and recounts

Round 3 of PR #21 closed: backlog gained the 'Revisão do head 23fd183' section mapping the five reproduced findings to commits dad9608, 994632b, d917af4, 9d955e2 and a4d009c, with the counts recounted (runner 15, labels 13, context 12, 24 punctuation variants); tasks updated. The five reproductions were re-run on the fixed tree and none reproduces. Validation: validate_repo both parsers, doctor, git diff --check.

## 2026-09-11: Org bootstrap confines the destination before writing

Round 3 of PR #21, finding 5: init_context.py --org checks confinement before creating anything: when .ai/memory or .ai/memory/org is, or sits behind, a symlink, it exits 1 and writes nothing (the old guard only resolved the path once org/ existed, so a symlinked ancestor let the four files land outside the repository). Regression relocates .ai/memory behind a symlink and requires exit 1 with nothing created outside. MEMORY_SYSTEM states the rule. Validation: test_context_scripts 12, full REPO_HEALTH battery green.

