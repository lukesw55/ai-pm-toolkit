# Chat messages (BLUF)

## What it is

**Bottom Line Up Front** — the point goes in the first line, supporting detail follows (and can be skipped by a reader in a hurry). Built for Slack/Teams/WhatsApp, where messages are read on a phone, between other things, and a wall of text gets skimmed or ignored regardless of how good the content is.

## Why it matters

Chat is a different contract with the reader than email or a doc: the reader did not choose to sit down and read this. If the point isn't in the first line, most readers never reach it. BLUF also disciplines the writer — if you can't state the bottom line in one line, the message probably isn't ready to send.

## What BLUF chat is NOT

- **A shrunk memo.** Don't compress a five-paragraph argument into five dense sentences — cut the argument down to the one thing the reader needs to know or do.
- **A cliffhanger.** "Quick question..." followed by silence until they respond is not BLUF — ask the actual question in the first message.
- **A decision record.** A decision made in chat and never written down doesn't exist a month later. If it's a real decision, it graduates to a doc (→ `channel-rules.md`).

## What BLUF chat IS

- **Point first.** The takeaway or the ask is line one, not the payoff at the end.
- **Threaded detail.** Supporting context goes in a thread reply or is explicitly marked optional, not stacked in the main message.
- **One ask.** A single, unambiguous next action or answer needed.
- **Skimmable.** Someone reading only the first line still knows what's being asked of them.

## Ready-to-use template — Status update

```text
<Status in one line: on track / at risk / blocked, plus the headline number/fact>
- <supporting point 1, if needed>
- <supporting point 2, if needed>
<No ask, unless one exists>
```

Default length: **≤5 lines** for a routine status update. Editable — genuinely multi-part updates can run longer, but consider whether it should be split into separate messages or moved to a doc instead of growing in place.

## Ready-to-use template — Escalation

```text
@<decision-maker> <the issue, stated as fact you've confirmed, or explicitly
flagged as unconfirmed if you haven't checked yet>
Impact: <what breaks/costs/slips if unresolved>
Ask: <specific action — approve, confirm, join a call — with urgency stated
plainly, not implied through tone>
```

Escalating is not the same as venting. State the confirmed facts, flag anything unconfirmed as unconfirmed, name the impact, and make one specific ask — even when (especially when) the situation is frustrating.

## Ready-to-use template — Quick decision ask

```text
@<decision-maker> Need a call on <thing> by <time/date>.
Option A: <one line> — Option B: <one line>
My rec: <A or B>, because <one clause>
Reply with A/B or "let's talk" if you need more context.
```

## Writing discipline

- **First line carries the message.** If the reader stops there, they still know the point.
- **One ask per message.** Multiple asks compete for attention and none gets answered.
- **Name the decision-maker.** `@here` and `@channel` diffuse responsibility; a named person feels the ask.
- **Confirmed vs. unconfirmed, always distinguished.** Chat moves fast, which is exactly when unverified claims slip out as fact — mark what you haven't checked yet (see `../inference-discipline/SKILL.md`).
- **Urgency stated, not implied.** "ASAP" is not a deadline. Say the actual time.

## Common anti-patterns

- **Wall of text.** Five paragraphs pasted into one Slack message; the ask is somewhere in paragraph three.
- **"Quick question" with no question.** Forces a reply just to unlock the actual ask.
- **Chat-as-negotiation.** A real disagreement worked out over 15 back-and-forth messages with no summary at the end — see the 3-exchange rule in `channel-rules.md`.
- **Blame before confirmation.** Escalating a heated claim ("your deploy broke X") before checking whether it's actually true — the chat-speed version of asserting an unverified claim as fact.
- **Silent channel switching.** Deciding something in a DM that the rest of the team needed to see, with no summary posted back to the shared channel.

## Seniority signals

- **Beginner:** posts clear status updates; asks get answered without follow-up "what do you mean?" replies.
- **Intermediate:** escalates cleanly — confirmed facts, named impact, one ask — without needing a redo.
- **Advanced:** knows when a chat thread has outgrown chat and moves it before it sprawls.
- **Expert:** chat messages read as if they were edited, because the bottom line was found before typing started.

## Files

- routine status updates: no persistent file needed
- escalations and decisions made via chat: summarise into `.ai/memory/projects/<slug>/decisions.md` if the outcome matters beyond the thread — chat history is not a reliable long-term record
