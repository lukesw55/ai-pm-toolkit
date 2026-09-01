# Channel-fit rules

## What it is

A decision guide for picking chat, email, a doc, or a call — and for recognising when a conversation has outgrown the channel it started in. Most communication friction isn't a wording problem, it's a channel-fit problem: a decision negotiated in DMs, a status update that needed to be a dashboard, an escalation that should have been a memo.

## Why it matters

The wrong channel doesn't just waste time — it loses the record. A decision made across 20 scattered Slack messages is functionally undocumented: nobody can point to it a month later, and two people will remember it differently. Channel choice is a documentation choice as much as a communication one.

## Decision guide

| Need | Default channel | Why |
|---|---|---|
| Quick status, no ask | Chat (BLUF) | Low stakes, ephemeral, fast |
| Ask needing a yes/no by a date | Chat (BLUF) or short email | Fast, but needs a clear, findable ask |
| Decision with options and trade-offs | Email (SCQA) or memo | Needs to be read once, carefully, and referenced later |
| Decision involving 3+ stakeholders or conflicting incentives | Doc / DACI (`pm-transversal-stakeholder`) | Needs a driver, an approver, and a written record |
| Negotiation or real disagreement | Call, then written summary | Synchronous is faster for genuine back-and-forth; the summary is what survives |
| Anything that needs to be found again in 3 months | Doc, not chat | Chat search is unreliable; docs are the record |

## The 3-exchange rule

If a chat thread crosses **3 back-and-forth exchanges** without resolving, stop typing and do one of:

- **move to a call** — if it's a genuine disagreement that needs real-time back-and-forth
- **move to a doc** — if it's actually a decision with options and trade-offs (escalate to `pm-transversal-stakeholder`)
- **summarise and close** — if the exchanges actually resolved it, post the one-line outcome so it's findable later

Default: **3 exchanges**. Editable — a fast, low-stakes clarification can go a couple rounds past that; a heated or high-stakes topic should escalate sooner, not later. The rule exists to catch the failure mode where a decision quietly happens in chat and nobody writes it down.

## What channel-fit is NOT

- **A rule against chat.** Chat is the right tool for most day-to-day communication — this is about catching the cases where it isn't.
- **An excuse to avoid writing.** "Let's just hop on a call" used to dodge putting a decision in writing is the opposite of good channel-fit; the call still needs a written summary.
- **A reason to escalate everything to a doc.** Most updates genuinely are chat-sized. Over-formalising routine status is its own anti-pattern.

## Escalating out of chat

When a chat thread is really a decision:

1. Say so explicitly in the thread: "this looks like a real decision — let me pull it into a doc so we have a record."
2. Summarise the options and trade-offs surfaced so far (don't restart from scratch).
3. Hand off to `pm-transversal-stakeholder` for the DACI/memo structure.
4. Post the doc link back in the original thread so anyone following it can find the resolution.

## Common anti-patterns

- **DM sprawl.** A negotiation conducted across private messages with no shared record — nobody outside the DM knows the decision or the reasoning.
- **Meeting-as-avoidance.** Scheduling a call instead of writing a two-line async message, for something that didn't need real-time discussion.
- **Chat-as-permanent-record.** Treating a Slack thread as if it were a decision log; it isn't searchable or citable the way a doc is.
- **Doc-for-everything.** Writing a full memo for a decision that was genuinely a two-message chat exchange — this wastes the reader's time in the other direction.
- **Escalating without a summary.** Moving a thread to a doc but pasting the raw chat log instead of synthesising the actual options and trade-offs.

## Files

- decisions that escalate out of chat: `.ai/memory/projects/<slug>/decisions.md`, with a one-line pointer back to the original thread if useful for context
