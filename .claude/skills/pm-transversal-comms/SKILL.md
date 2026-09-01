---
name: pm-transversal-comms
description: Cross-phase skill for **short-form PM communication** — executive email (SCQA), chat/Slack messages (BLUF), and channel-fit rules — the highest-frequency artefacts a PM writes. Invoke whenever a decision, status, or ask needs to go out as an email or chat message, when it's unclear whether something belongs in chat vs. email vs. a doc, when a thread is spiralling and needs to be pulled into a decision, or when an escalation needs a fact check before sending. Trigger on "write the email", "draft a Slack message", "quick update for the channel", "escalate this in chat", "should this be an email or a doc?", "e-mail para o time", "manda no Slack", "BLUF", "SCQA". Complements `pm-transversal-stakeholder` (longer-form memos/DACI) and `pm-storytelling` (narrative spine). Produces exec emails, chat updates/escalations, channel-fit recommendations. Chains into `humanizer` before anything ships.
---

# PM Transversal — Short-form comms (email, chat, channel fit)

> Transversal skill — useful in every Double Diamond phase whenever a PM needs to write, not present. Complements `pm-transversal-stakeholder`'s longer-form memos/DACI and `pm-storytelling`'s narrative spine with the two formats a PM actually reaches for most on a given day: email and chat.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke when:

- a decision, status, or ask needs to leave as an email, not a doc
- a chat message needs to escalate or land cleanly without turning into a meeting
- it's unclear whether something belongs in chat, email, or a doc
- an update needs to survive being read on a phone in ten seconds
- a chat thread is spiralling and needs to be pulled into a decision or moved to a doc
- an escalation is heated and needs a fact-check before it goes out

Skip for content that's long-form enough to need DACI/exec-memo structure (→ `pm-transversal-stakeholder`) or dedicated narrative work for a deck/QBR (→ `pm-storytelling`). Skip for Confluence/Jira artefacts (→ `pm-transversal-docs`).

## Prime directive

**Every message spends the reader's attention before it spends anything else.** A well-structured 5-line Slack message that gets read beats a well-argued 20-line one that gets skimmed or ignored. Chat and email are not lightweight versions of a memo — they're a different contract with the reader, and that contract is: get to the point first.

## Core sub-skills

### 1. Executive email (SCQA)

Situation–Complication–Question–Answer structure for decision, status, and ask emails to people with less time and context than the PM has.

Outputs: decision email, status email, ask email.

Anti-patterns: burying the ask below the fold, chronological narrative instead of SCQA, a subject line that doesn't name the action needed.

→ Deep-dive: `references/exec-email-scqa.md`

### 2. Chat messages (BLUF)

Bottom-line-up-front structure for Slack/Teams/WhatsApp: the point in line one, supporting detail threaded or collapsed, one ask per message.

Outputs: status update, escalation, quick decision ask.

Anti-patterns: wall of text with the point buried at the end, no explicit next action, letting a chat thread stand in for a decision record.

→ Deep-dive: `references/chat-bluf.md`

### 3. Channel-fit rules

When to use chat vs. email vs. a doc vs. a call; when and how to escalate a chat thread that's outgrown chat.

Outputs: channel recommendation, escalation trigger, hand-off to `pm-transversal-stakeholder` when the thread is actually a decision.

Anti-patterns: defaulting to whichever channel is already open, letting a negotiation sprawl across DMs with no written record, "let's hop on a call" as a way to avoid writing anything down.

→ Deep-dive: `references/channel-rules.md`

## Workflow

1. **Load context** — who's reading, what they already know, what decision or action this message needs to produce.
2. **Classify the ask** — email, chat, or "this actually needs a doc" (→ `pm-transversal-stakeholder`)?
3. **Name the one ask** — one message, one action. Split multi-ask messages.
4. **Draft with the structure, not around it** — SCQA for email, BLUF for chat. The structure is the discipline, not decoration.
5. **Check the claims** — anything asserted as fact that hasn't been verified this turn is inference-discipline's job before it ships (`../inference-discipline/SKILL.md`); this applies as much to a heated three-line Slack message as to a formal memo.
6. **Humanize before sending** — route through `../humanizer/SKILL.md` and the `humanize-deliverables` gate for anything leaving the workspace.

## Output contract

```text
## [Email / Chat message]

### Reader + what they already know
### The one ask (what action, by when)
### Draft
### Channel recommendation (if ambiguous)
### Open verifications (facts not yet confirmed)
```

## Integration

- Every phase: status updates, decision asks, and escalations happen constantly across Discover/Define/Develop/Deliver — this skill is the default for anything short-form.
- Paired: `pm-transversal-stakeholder` (the thread/email escalates into a DACI or exec memo), `pm-storytelling` (a launch-comms email needs a narrative spine before SCQA structuring), `inference-discipline` (claims in a fast, emotional message are exactly where unverified assertions slip through), `humanizer` + `humanize-deliverables` (final pass before anything ships).
- Doctrine: calibrated disagreement applies here too — a chat message under pressure to assert an unverified claim is the same failure mode as a solution-first premise in a discovery brief, just faster-moving. See `../DOCTRINE.md`.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is BLUF/SCQA at the stated defaults; Standard adds the "why" a reader might ask for; Caveman is the ask and the date, nothing else.

## Success criteria

- the reader knows the ask and the deadline from the first line
- nothing asserted as fact in a fast message is actually unverified
- chat threads that are really decisions get pulled into a doc before they're 3 exchanges deep
- emails get replies with decisions, not "can we hop on a call to discuss?"
- escalations land as fact-checked and specific, not as blame with unconfirmed causes
