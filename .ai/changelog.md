# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-14: B41 inference-discipline: relations, not terms, in two standard blocks; strict pairs

ambiguous-flow-approval grows from four to six assertions: the question that names both candidate flows in one sentence with a question mark, the scope reading tagged as an inference with its basis, knowns and unknowns as filled fields (heading plus bullet, or field plus content), the edit held until the user approves with the verb, the cost of guessing wrong spelled out, and the word resolved against the repo first. memory-not-proof grows from three to five: memory called a prior with the linking verb, who or what confirms the date, the two steps sequenced with a connector in a comma-free span, the date in the draft marked with a marker adjacent to it or a verb form, and both branches (confirmed sends as fact, unconfirmed hedges) present. Both pairs carry keyword_only and near_miss fixtures; bad fixtures are the plausible wrong answers that edit or send on the prior. Full REPO_HEALTH battery green.

## 2026-09-14: B41 humanizer: relations, not terms, in three standard blocks; strict pairs

humanize-exec-memo goes from four assertions, three of them the same absence check, to five: at least two removed phrases named with the removal verb, what stayed intact with its object, a short and a long sentence in the text, the team's voice kept in the rewrite, and the stock phrases absent from the unquoted prose as one check. preserve-technical-meaning grows from three to six: the metric with its migration date in one clause, the latency SLO with its number and its fate, the legacy dashboard with its end date, each fact named twice (rewrite and intact list), the cuts named with the cutting verb, and the three facts as three short sentences with a verb each. keep-attributive-hyphens grows from four to seven, keeping the two negatives that separate the upstream hyphen rule from the old fork: the noun phrase followed by its verb, the predicate form after the verb, the date carried from the rewrite into the intact list, the stakeholder filler trimmed and said so, and the remaining-patterns field. The pedagogical 6b fixtures keep their exact bands; the exec-memo one is re-wrapped at a sentence boundary with the same words, since a hard wrap inside a sentence breaks the spans the contract relies on. All three pairs carry keyword_only and near_miss fixtures. Full REPO_HEALTH battery green.

## 2026-09-14: B41 humanize-deliverables: relations, not terms, in one standard block; strict pair

gate-before-slack-send grows from four to nine assertions: the ship date stated with its verb, the bug count as a fraction plus the FAQ with its owner, the open bug with its ETA, the launch date linked to the outcome of the fix, the three steps ordered with connectors (pass, mark, send), what the hook hashes, what it does without the mark, the rule that a byte change after marking needs a new mark, and a negative on sending before the gate. Anchors sit next to their verbs so a comma-joined list of the same terms does not pass. The pair carries keyword_only and near_miss fixtures; the bad fixture is the plausible wrong answer that posts first and humanizes if the hook complains. Full REPO_HEALTH battery green.

