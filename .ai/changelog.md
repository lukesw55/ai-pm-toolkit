# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: B40 pm-phase-discover: relations, not terms

B40 pm-phase-discover: the three graded blocks (resist-solution-first-dashboard-premise, solid-research-plan-agree, update-impact-brief-and-test-feasibility-during-discovery) now check two anchors with a verb or connector between them, carry one explicit decision assertion each and at most two trivially satisfied ones (n 6, 8, 8). Strict pairs added to the fixture JSON (plausible bad, keyword list, near miss failing one named assertion); the B11/B31 in-code fixtures for these evals moved into the JSON as the pairs' good and bad; the pedagogical fixture 1 was rewrapped so its first sentence sits on one line (spans stop at line breaks, like the sentence splitter). Keyword list worst join 0.25, label soup worst 0.17. Validation: full REPO_HEALTH battery green (test_grade_evals 125 fixtures, 9 strict pairs, 36 variants, 45 soup texts).

## 2026-09-11: Grader tests: strict pairs also fail their own labels

B40 commit 1: test_grade_evals.py joins each strict block's assertion labels the five ways it joins the keyword list (full stop, semicolon, comma, newline, and) and requires every text at or below 0.34, the attack the PR #21 review applied by hand. The six strict blocks' labels now describe the check without the tokens it looks for, so the derived soup fails them (worst join 0.33, against 0.83 before on the prototype block); two near_miss targets follow their labels; the docstring states the strict-pair contract. Validation: full REPO_HEALTH battery green (test_grade_evals 118 fixtures, 24 punctuation variants, 30 label-soup texts).

## 2026-09-11: Round 3 closing: review section and recounts

Round 3 of PR #21 closed: backlog gained the 'Revisão do head 23fd183' section mapping the five reproduced findings to commits dad9608, 994632b, d917af4, 9d955e2 and a4d009c, with the counts recounted (runner 15, labels 13, context 12, 24 punctuation variants); tasks updated. The five reproductions were re-run on the fixed tree and none reproduces. Validation: validate_repo both parsers, doctor, git diff --check.

