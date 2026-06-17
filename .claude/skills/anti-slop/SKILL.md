---
name: anti-slop
description: Detect and remove AI slop from Claude Code outputs before they reach the repo or the user. Use before writing or editing code, comments, docstrings, markdown docs, README sections, PR descriptions, Jira/Linear tickets, ADRs, plans, or chat replies longer than two sentences. Also use when reviewing diffs, PRs, generated files, or anything the user calls "AI-generated", "slop", "too verbose", "boilerplate", "generic", "ChatGPT-ish", "Claude-ish", "com cara de IA", "tá com slop", or "tira o ruído". Pairs with humanizer for prose and Stop hooks for runtime enforcement.
---

# Anti-slop

Remove AI tells from code, comments, docs, repo structure, PR text, and Claude Code replies.

This skill is a **gate**, not a writing style guide. Use it before producing or modifying anything that might enter the codebase or a developer workflow.

## Non-negotiables

1. Ship the smallest useful change.
2. Trust internal contracts unless a boundary is involved.
3. Delete generic structure instead of polishing it.
4. Do not create files the user did not ask for.
5. Do not narrate obvious tool use.
6. Do not add abstractions for hypothetical reuse.
7. Preserve substance while removing slop.

If removing "AI slop" removes evidence, behavior, constraints, or useful context, you removed too much.

## When to invoke

Invoke before:

- writing or editing code
- adding comments or docstrings
- creating or expanding markdown docs
- drafting README, PR, ADR, issue, ticket, changelog, or migration text
- reviewing a diff or generated file
- responding with more than two sentences and any structured format
- creating any new file that was not explicitly requested
- adding defensive checks, helper functions, interfaces, wrappers, logs, or config

Invoke when the user says:

- remove AI slop
- kill the slop
- clean this up
- less verbose
- make it leaner
- this looks AI-generated
- review for AI tells
- corta o boilerplate
- tira o ruído
- tá com cara de ChatGPT
- esse código tá com slop
- essa resposta tá com cara de IA

Skip only when:

- returning raw logs, JSON, CSV, terminal output, or machine-readable data
- answering with one factual sentence
- making a tiny mechanical edit the user already specified exactly
- the user explicitly asks for a verbose, template-heavy, or defensive style

## Operating modes

### 1. Gate mode

Use when creating new output.

Apply the catalogue silently. The user should only see the lean result.

Before final output, ask internally:

> What still makes this look AI-generated?

Then remove that tell unless it is load-bearing.

### 2. Sweep mode

Use when reviewing existing material.

Return:

`````markdown
## Findings
- path:line — TAG short issue

## Rewrites
```diff
...
```

## Remaining smell

One sentence naming what still feels AI-generated, or `None`.
`````

Do not rewrite the whole file unless the user asked.

### 3. Diff mode

Use when reviewing code changes.

Prioritize comments that change behavior, reduce risk, or delete needless code. Avoid taste-only comments unless the slop is obvious.

Format:

```markdown
- `path:line` — TAG issue. Suggested change: ...
```

## Catalogues

The slop patterns themselves live in four references — load only the one that matches what you're about to write or review. Each reference is independent; skip the others.

| When you're about to... | Load |
|---|---|
| Write or review code, comments, types, identifiers | [`references/code-catalogue.md`](references/code-catalogue.md) — A1–A10 |
| Write or review markdown docs, READMEs, PR/ADR/ticket bodies | [`references/doc-catalogue.md`](references/doc-catalogue.md) — B1–B12 |
| Write a chat reply longer than two sentences | [`references/reply-catalogue.md`](references/reply-catalogue.md) — C1–C10 |
| Write or review test files (unit / integration / E2E / fixtures) | [`references/test-catalogue.md`](references/test-catalogue.md) — E1–E8 |

Some patterns are hard-blocked by `.claude/hooks/anti-slop-gate.sh` (PreToolUse on Write/Edit/NotebookEdit) and `.claude/hooks/scope-bloat-gate.sh` (Stop): forbidden file basenames (see File artifact rules below), banner `=====` lines (A10), decorative emoji headings (B6), and reply-shape signals (em-dash density, label-colon runs of 4+, headings on short prompts, dual-question close, response >5× prompt length without a doc keyword). To intentionally allow flagged content, use `.claude/hooks/anti-slop-mark.sh "<final content>"` to write a per-content sha256 sentinel. Everything else applies by hand.

## 30-second pre-output scan

Run this scan against any output before sending it — diff, doc, reply, test file. It catches the highest-frequency slop in under thirty seconds; anything that survives goes to the per-domain catalogue.

```
Code & tests
  [ ] Defensive check at an internal boundary?          → A1, delete
  [ ] try/except without real recovery?                  → A2, let it throw
  [ ] Single-use helper / constant / interface?          → A3 / A9, inline
  [ ] Generic identifier (data/result/helper/manager)?   → A4, name the domain
  [ ] Comment restating code below it?                   → A5, delete
  [ ] Log line narrating the function?                   → A6, delete
  [ ] Verbose test name "should ... when ..."?           → E1, shorten
  [ ] AAA comments in a short test?                      → E8, delete

Docs & artefacts
  [ ] Template-shaped heading (Overview/Details/...)?    → B1, name what changed
  [ ] Label-colon bullets with no evidence?              → B3, replace with facts
  [ ] Forced symmetry (3 pros / 3 cons / 3 risks)?       → B4, keep the real count
  [ ] Static metadata block (Status / Owner / Date)?     → B5, delete
  [ ] Decorative emoji heading?                          → B6, delete (also hook-blocked)
  [ ] TOC / glossary / "About this doc" on short doc?    → B7-B12, delete
  [ ] About to create PLAN.md / NOTES.md / SUMMARY.md?   → file-artifact rule, do not create
  [ ] Banner line of '=' or '-' (5+)?                    → A10, delete (also hook-blocked)

Replies
  [ ] Restating the prompt before answering?             → C1, answer directly
  [ ] Narrating tool calls before making them?           → C2, just call
  [ ] Sycophantic opener (Great question / Of course)?   → C3, start with the answer
  [ ] Trailing ## Summary / "Here's what I did"?         → C4 / C9, end at substance
  [ ] "Want me to also X, Y, Z?" follow-up spam?         → C5, stop
  [ ] Heading / bullets in a < 6-sentence answer?        → C6, inline
  [ ] Apologetic opener ("Sorry for the confusion")?     → C7, deliver the fix
  [ ] "Hope this helps! Let me know..."?                 → C8, delete
  [ ] Mid-reply "actually wait, let me reconsider..."?   → C10, edit silently
  [ ] Em-dash density obviously high?                    → hook-blocked, fix anyway
```

If the scan flags three or more boxes, the output is shaped wrong. Stop and rewrite — don't paper over slop with one or two edits.

## File artifact rules

Never create these unless the user explicitly asks:

```text
PLAN.md
NOTES.md
IMPLEMENTATION.md
SUMMARY.md
CHANGES.md
ANALYSIS.md
TODO.md
```

Do not create ADRs for reversible implementation details.

Do not add README sections such as Contributing, Roadmap, License, Code of Conduct, Architecture, or Table of Contents unless the repo actually needs them.

The right place for a change explanation is usually the PR body or commit message, not a parallel markdown file.

## Claude Code workflow

Before editing:

1. Identify the smallest file set needed.
2. Check existing style before adding new patterns.
3. Prefer deletion over abstraction.
4. Prefer direct code over wrappers.
5. Prefer existing tests over new scaffolding.

During editing:

1. Avoid broad rewrites.
2. Avoid opportunistic cleanup outside the requested scope.
3. Do not introduce new dependencies for formatting or convenience.
4. Do not create helper files unless required by the requested change.
5. Keep names domain-specific.

After editing:

1. Re-read the diff.
2. Remove any code that exists only because an AI would "be safe".
3. Remove comments that explain obvious code.
4. Remove generic docs, summaries, and headings.
5. Verify the change still preserves the user's requested behavior.

## Review checklist

Use this checklist internally:

```text
[ ] Did I add a guard for something an internal contract already guarantees?
[ ] Did I catch an exception without real recovery?
[ ] Did I create a helper, class, interface, constant, or config with one use?
[ ] Did I add a comment that restates code?
[ ] Did I use generic names like data/result/helper/manager?
[ ] Did I add logs that narrate execution?
[ ] Did I create a doc/file the user did not request?
[ ] Did I add headings, bullets, or symmetry because the output looked nicer?
[ ] Did I end with a summary or follow-up offer the user does not need?
[ ] Did I remove substance while removing slop?
```

## Output contracts

### When asked to clean existing material

Return only:

`````markdown
## Findings
- `path:line` — TAG issue

## Rewrites
```diff
...
```

## Remaining smell

None.
`````

### When asked to write new material

Return the clean artifact only. Do not explain that anti-slop was applied.

### When asked to review a PR or diff

Return concise review comments. Prefer:

```markdown
- `src/foo.ts:42` — A2 try/except without recovery. Let this throw or catch the specific error at the boundary.
```

Avoid:

```markdown
This code is generally good, but here are some suggestions...
```

## Interaction with other skills

Several patterns sit on the seam between anti-slop and `humanizer`. Both skills cover label-colon bullets, em-dashes, decorative emoji, rule-of-three, and hedging — they catch the same shapes from different angles. The split is by *what* in the output you are working on:

| Concern | Owned by |
|---|---|
| Structure: headings, bullets, lists, tables, banners, file artefacts, PR/ADR/ticket shape, code identifiers, comments, logs, repl shape | **anti-slop** |
| Prose shape: sentence rhythm, vocabulary, n-gram fingerprints, detector axes, narrative voice, paragraph length variance | **humanizer** |
| The seam (em-dash density, label-colon runs, emoji headings) | **anti-slop** owns the hard rule, `humanizer` owns the prose-level audit |
| Scope and over-explanation in chat replies | **anti-slop** (catalogue C) |
| Code, comments, types, identifiers, runtime narration (logs, debug prints) | **anti-slop** (catalogue A) |
| Test names, setup ceremony, mocking, snapshots, AAA comments | **anti-slop** (catalogue E) |
| Doc structure (headings, bullets, TOC, glossary, metadata blocks, PR templates) | **anti-slop** (catalogue B) |
| Doc prose body (paragraphs, opening sentences, narrative arc) | **humanizer** |
| Outbound publish gate (Confluence / Slack / Jira) | `humanize-deliverables` (sha256 hard gate via `humanize-gate.sh`) |
| Approval flow for inferences and hallucination claims | `inference-discipline` |
| Visual / UI / design slop | a dedicated visual-design reviewer |

When a single artefact mixes prose and structure (PRD, ADR, exec memo): run anti-slop first for the structural pass, then `humanizer` for the prose paragraphs. The catalogues do not conflict; they catch different surfaces of the same draft.

For prose that ships outbound (Confluence / Slack / customer / leadership), `humanize-deliverables` is the publish-time hard gate. It runs orthogonally to anti-slop — anti-slop catches the structural slop pre-write, humanize-gate catches the prose tells pre-publish. Both must pass.

If multiple skills apply, run the specific skill first, then anti-slop as the final structural gate.

## Final rule

A clean output should feel like it came from a competent maintainer under time pressure: specific, boring where boring is good, and ruthless about anything that does not pay rent.
