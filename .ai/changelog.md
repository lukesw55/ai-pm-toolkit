# Changelog

<!-- Toolkit/repo changes (skills, hooks, doctrine, scripts). Project work logs live in each project's memory under .ai/memory/projects/<slug>/changelog.md. Append via: python3 scripts/memory.py log repo "<entry>". -->

> Active log keeps the most recent entries; older entries in `changelog-archive.md`.

## 2026-09-16: B43 closing: backlog, decision and tasks

B43 enters the ranking as done, with the detail section recording what was kept from the requested anatomy, what was adapted, and what was refused with its reason: no generated banner, no fabricated terminal recording, no deploy button that would land a visitor in a terminal where neither CLI is installed, no contributor wall, no issue templates, no code of conduct, no second README in Portuguese. The decision that outlives the rewrite is the one in docs/DECISIONS.md: a count in the README is derived from the tree, never typed. It names the consequence rather than hiding it, since adding a skill or a script turns CI red until the README says so, and CONTRIBUTING.md tells a contributor that before they hit it. Full docs/REPO_HEALTH.md battery green before the commit.

## 2026-09-16: Merge the B42 branch: the corrected decision record

The correction to docs/DECISIONS.md landed on the B42 branch, where the sentence it fixes was introduced. This branch is stacked on that one, so the merge brings it across. Conflicts were in the two changelog files only, resolved by keeping every entry in chronological order: the three most recent stay in the active log and the governance entry rotates into the archive, whose index was rebuilt with memory.py index repo. Full docs/REPO_HEALTH.md battery green before the commit.

## 2026-09-16: B42 review: the decision record carried the sentence the rest of the round corrected

The review round fixed the direction a good fixture candidate comes from in the protocol, in the repo-health checklist, in the script's docstring and in the card's own prose, and missed the line in docs/DECISIONS.md that says the same thing. It still read that the candidate comes from a run the grader already accepts. It does not: a good candidate exists only for a false reject, which is a run the grader rejected and a human accepted. The reason to rewrite it by hand is that it is the model's own output, not that the grader agreed with it. One sentence, in the file that is meant to be the durable version of the rule, so it is the one place where leaving it wrong would outlive the PR. The changelog entries that quote the old wording stay as they are: they record what was written at the time, and the entry for the correction is the record that it changed. Full docs/REPO_HEALTH.md battery green before the commit.

