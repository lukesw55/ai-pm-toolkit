---
name: humanize-deliverables
description: >-
  Force a humanizer pass before delivering ANY user-facing prose artefact — Confluence pages, Slack
  messages, emails, release notes, exec memos, PRDs, DACI rationale, customer-facing copy, status
  reports, FAQs, knowledge-base articles, public docs. Trigger BEFORE the artefact leaves the
  workspace, never after the user has already seen the "final" draft. Pull
  `../humanizer/SKILL.md` and apply its 29-pattern catalog. Skip ONLY for inline
  conversational replies to the user, raw machine output (logs/JSON/CSV), code/config, and structured
  ticket fields. Pushy by design — when in doubt, humanize. Trigger phrases: "post to Confluence",
  "send to Slack", "draft the release notes", "memo for leadership", "customer email", "publica essa
  página", "manda no Slack", "rascunha o comms", "final draft", or whenever about to call MCP tools
  that publish/send text (`createConfluencePage`, `updateConfluencePage`, `slack_send_message`,
  `slack_send_message_draft`).
---

# Humanize-deliverables: voice gate before delivery

This skill is a **gate**, not a writer. It sits between drafting and delivery and ensures every external-facing prose artefact has been stripped of AI tells before another human reads it.

## Why this exists

Your deliverables — exec memos, PRDs, Confluence pages, Slack updates, customer comms — get read by leadership, customers, and cross-functional partners. Text that smells like ChatGPT erodes credibility silently. The `humanizer` skill (`../humanizer/SKILL.md`) catalogues 29 universal AI-writing patterns. This gate enforces a pass through those before the artefact ships.

## When to trigger

**Always trigger before:**

- calling `mcp__claude_ai_Atlassian_Rovo__createConfluencePage` / `updateConfluencePage` / `createConfluenceFooterComment` / `createConfluenceInlineComment`
- calling `mcp__claude_ai_Slack__slack_send_message` / `slack_send_message_draft` / `slack_create_canvas` / `slack_update_canvas`
- calling Jira comment tools (`addCommentToJiraIssue`)
- pasting "here is the final X" into chat for the user to copy-paste elsewhere
- producing release notes, launch comms, FAQs, public-docs copy
- producing exec memos, status reports, QBR slide text, DACI rationale narrative
- producing customer-facing copy (B2B emails, KB articles, in-app strings, marketing-adjacent text)
- producing PRDs that will be circulated outside the immediate team

**Skip when:**

- replying conversationally to the user in this session ("yes, here's what I found")
- emitting raw machine output: JSON, logs, CSVs, terminal commands
- writing/editing code, config, schemas
- structured ticket fields (Jira labels, components, fixVersion) — only the *prose body* of a ticket is in scope
- internal notes / scratchpads / `.ai/memory/` updates that nobody outside the user will read

When unsure → run the gate. The cost of an unnecessary pass is seconds; the cost of shipping AI-tinted prose to a customer or to leadership is real reputational drag.

## How to run the gate

1. **Draft normally.** Don't pre-censor while drafting — easier to clean up than to write under constraint.

2. **Pull the catalogue.** Read `../humanizer/SKILL.md` (or the relevant section if you've already loaded it this session). It contains the full 29-pattern list with before/after examples.

3. **Sweep for the patterns that bite hardest in PM/Eng prose** (this is the high-yield subset of humanizer's catalogue):
   - **Em-dash overuse** — every em-dash is suspicious; keep at most one or two per page, replace others with periods, parentheses, or `—` → `:`
   - **Rule of three** — "fast, reliable, and scalable" reads like AI; cut to two or expand to a real list
   - **Link-words as throat-clearing** — "Furthermore", "Moreover", "Additionally", "It is important to note that", "In the context of"
   - **Inflated verbs / vocabulary** — "delve into", "leverage", "underscore", "navigate", "robust", "seamless", "comprehensive", "holistic", "tapestry", "foster", "facilitate"
   - **Vague attributions** — "studies show", "experts agree", "research indicates" without citation
   - **Superficial -ing analyses** — "...highlighting the importance of...", "...showcasing the synergy of...", "...underscoring the need for..."
   - **Promotional / marketing register** — "we are excited to announce", "best-in-class", "cutting-edge", "game-changer"
   - **Negative parallelisms** — "not just X, but Y", "it's not about X — it's about Y" (rarely earns its weight)
   - **Passive voice when active is shorter** — "the decision was made" → "we decided"
   - **Hedging stacks** — "may potentially be able to" → "can"

4. **Final anti-AI pass** (humanizer §6, mandatory). Ask: *"What still makes this obviously AI-generated?"* — name the remaining tells in one short sentence. Then revise.

5. **Substance check.** AI-tell removal can quietly strip the load-bearing content; this pass restores it. For every list of suggestions / findings / actions in the draft, audit each item against three checks:

   - **Does it carry action + example/anchor + why-it-matters?** A bullet that says "cross-team dependency as a first-class concept (#1)" without saying *what to do* or *what fixes* fails. Roughly 2–4 sentences per item is the right density.
   - **Would this bullet read identically if the initiative were a different feature on the same team?** If yes, it's padding. Drop it or rewrite to carry initiative-specific signal.
   - **If the recipient could ignore the message and still understand what was meant just by reading the headlines, is the message too thin?** The recipient should be able to act on at least one item without pinging back for context.

   If any bullet fails, expand or cut — never leave category labels masquerading as content. A 290-word substantive deliverable beats a 70-word polished placeholder.

6. **Preserve voice, strip polish.** Write lean, direct, evidence-first, with explicit decisions and named asks. The gate removes AI texture; it does not remove the author's cadence, jargon, or evidence density. Concretely: keep shorthand the reader shares and drop internal jargon they do not; attribute load-bearing quotes to a named source; drop framework labels lifted into prose; prefer a humble peer voice over a presenter voice.

7. **Mark the final bytes (REQUIRED for hard-gated tools).** A `PreToolUse` hook in `.claude/settings.local.json` blocks the publish/send MCP tools (`createConfluencePage`, `updateConfluencePage`, `createConfluenceFooterComment`, `createConfluenceInlineComment`, `addCommentToJiraIssue`, `slack_send_message`, `slack_send_message_draft`, `slack_create_canvas`, `slack_update_canvas`) until a sha256 sentinel matches the prose body. Run:

   ```bash
   printf '%s' "<final body, exact bytes>" | hooks/humanize-mark.sh -
   ```

   Or pass the body as an argument:

   ```bash
   hooks/humanize-mark.sh "<final body>"
   ```

   The helper writes `.ai/gates/humanized/<hash>.flag` (gitignored). The hook recomputes the hash from `tool_input` (longest string wins) and only allows the call if the flag exists. Any byte change after marking — one extra newline, one swapped emoji — invalidates the flag; mark again with the EXACT bytes that will go to the tool.

8. **Deliver.** Call the publish/send tool, or hand the cleaned text to the user.

## Voice anchors per destination

Different destinations want different shapes; the gate respects that.

- **Exec memos / leadership briefs** — short sentences. Headed claims. Evidence inline (not in footnotes). No throat-clearing. First sentence states the decision or ask.
- **Confluence pages** — headed sections, tables for comparisons, decisions explicit, evidence linked. Status line at top ("Published — informative / factual" / "Draft — pending review").
- **Slack** — first sentence carries the ask or update. No "Hi team, hope you're well". No emoji unless your prior messages in the channel use them.
- **Release notes** — user-language, not internal-language. *"X works now"* beats *"the X experience has been enhanced"*. Skip the "we are thrilled" opening.
- **Customer comms (B2B)** — warm but not effusive. Concrete benefit before brand voice. No "we are excited to announce".
- **PRDs / specs** — problem before solution. Non-goals named. Success criteria measurable. Cut adjectives.

## What the gate does NOT do

- **Does not humanize the user's own writing** — only prose Claude is producing for the user to forward, paste, or publish. If the user pastes text and asks to "review" or "polish", invoke `humanizer` directly; this gate is for outbound deliverables.
- **Does not strip technical precision.** If a phrase looks AI-flavoured but carries load-bearing meaning (a regulated term, an SLA wording, a CRA-compliance phrase), keep it.
- **Does not expand the text.** Humanizing makes prose shorter or the same length, never longer.
- **Does not re-format structure.** Headings, tables, bullet hierarchy stay; only the prose voice changes.

## Enforcement (hard, since 2026-04-27)

The publish/send MCP tools listed in step 7 are **hard-gated** by `hooks/humanize-gate.sh` via a `PreToolUse` hook in `.claude/settings.local.json`. The hook computes sha256 over the longest string in `tool_input` (the prose body, in practice) and blocks the call unless `.ai/gates/humanized/<hash>.flag` exists.

This means: forgetting to humanize → tool call fails with stderr instructions to mark and retry. The skill body still teaches the *what* and *why*; the hook enforces the *that*.

Out-of-scope tools (e.g. reading Confluence, listing Slack channels, structured Jira field updates without prose) are not matched and run normally. To extend the gate, add tool names to the matcher regex in `.claude/settings.local.json`.

If the gate ever needs to be bypassed for a legitimate non-prose call (e.g. Confluence page with only a table and no prose), narrow the matcher rather than disabling the script.
