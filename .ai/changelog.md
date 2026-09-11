# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-11: Stale rubric labels are reported, never counted

Round 3 of PR #21, finding 2: a label whose rubric_version differs from the eval's current prompt and expected output is stale. label_eval_run.split_by_rubric separates current from stale labels; grade_all keeps only current labels for the human verdict and the rates, reports stale ones in grading.json and the benchmark (labels_stale), warns per stale label, and label() lets the same labeler relabel against the current rubric without --supersede while the old record stays in the file (then counted as superseded). Regression: change only expected_output after labelling; the verdict becomes null, labels_stale is 1, relabelling works. Protocol and REPO_HEALTH updated. Validation: test_label_eval_run 13, runner and recorder suites, full REPO_HEALTH battery green.

## 2026-09-11: Artefact anchors and punctuation-variant regression for the six new blocks

Round 3 of PR #21, finding 1: the six new assertion blocks now require artefacts a keyword list cannot supply (a URL, HogQL text or insight id as the source; an analytics/<file>.md path for persistence; at least two of the weekly numbers; the behaviour-split query with its cohorts; the evidence gap phrased as a question with an owner role; a lens name next to its no-objection verdict with a reason that never crosses a semicolon; the PRD as the object of the kickoff decision; a participant plus a verb in the counter-evidence and saturation checks; role, verb and object for who builds what). test_grade_evals derives four punctuation variants (semicolon, comma, newline, and) of every keyword-only fixture and requires each at or below 0.34; the owner's semicolon variant of the adoption fixture drops from 6/7 to 2/7. Validation: test_grade_evals 118 fixtures, 24 variants, 6 strict pairs, 42/42 covered; full REPO_HEALTH battery green.

## 2026-09-11: Round 2 closing: review section, B40 candidate, recounts

Round 2 of PR #21 closed: backlog gained the 'Revisão da PR #21' section mapping the owner's seven points to the follow-up commits, the B40 candidate (54 of 79 pre-batch assertion blocks pass a keyword-only reply; the six new blocks were rewritten, the old ones are next), recounted totals (85 evals, 32 pairs with 6 strict, 118 fixtures, 42/42 covered, mirrors 138, suites hooks 33, contract 9, memory 48, context 11, recorder 6, runner 12, labels 12, validator 54, frontmatter 5); tasks updated; README describes the strict fixture pairs. Validation: validate_repo both parsers, doctor, git diff --check.

