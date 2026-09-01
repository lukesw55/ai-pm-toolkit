# Executive email (SCQA)

## What it is

**Situation–Complication–Question–Answer** — a structure for writing to someone with less time and context than you have, so the point survives even if they only read the first two lines. Originated as a Minto Pyramid Principle technique; here it's the default shape for any PM email that needs a decision, a status read, or a specific ask.

## Why it matters

Execs skim. An email that opens with three paragraphs of context and lands the ask in paragraph four gets a "can we hop on a call?" reply — which costs more of everyone's time than the email itself. SCQA front-loads the point so the reader can act from the first screen.

## What SCQA email is NOT

- **A narrative.** "First we did X, then Y happened, then we realised Z." Chronology is not structure.
- **A status report in disguise.** If there's no ask, it's not an SCQA email — it's an update (shorter, no decision required).
- **A hedge-everything memo.** SCQA states a position. If every option looks equally viable, that itself is the finding — say so, don't pad around it.

## What SCQA email IS

- **Situation** — the shared context the reader already has, in one or two sentences. Don't re-explain what they know.
- **Complication** — what changed, what's at risk, or what's new since the situation was last stable.
- **Question** — the implicit question the complication raises. Making it explicit is what lets the reader see the Answer as, well, an answer.
- **Answer** — the recommendation, decision, or ask. This is the paragraph that matters; everything above exists to make it land.

## Ready-to-use template — Decision email

```text
Subject: [Decision needed by <date>] <topic>

Hi <name>,

<Situation — 1-2 sentences, what you both already know>

<Complication — 1-2 sentences, what changed / what's at risk>

<Question, stated or implied — "so the question is whether we X or Y">

<Answer — your recommendation, with the 1-line reason. Options in 2-3 bullets
if more than one is live, each with a one-line trade-off.>

Ask: <specific action, specific date>

<Optional: link to the fuller memo/DACI if this decision has more depth than
an email should carry — see pm-transversal-stakeholder>
```

Default length: **≤300 words for the body of a decision email** (excludes subject, greeting, sign-off). Editable — a genuinely complex decision can run longer, but check first whether it should be a memo instead (→ `pm-transversal-stakeholder`) rather than a long email.

## Ready-to-use template — Status email (no ask)

```text
Subject: <topic> — status, <date>

<Situation — where things stood>
<What moved — 2-4 bullets, outcome-led not activity-led>
<What's at risk, if anything — named, with owner>
<No ask, or: "flagging, no action needed">
```

If there's an ask, it's not a status email — use the decision template.

## Ready-to-use template — Ask email

```text
Subject: [Ask] <specific thing needed> by <date>

<Situation — 1 sentence>
<Why now — 1 sentence: what depends on this>
<The ask — specific, sized, with the date>
<What happens if the date slips, briefly, if material>
```

## Writing discipline

- **Subject line names the action**, not the topic. "Decision needed: pricing v2 rollback by Friday" beats "Pricing v2 update".
- **Situation is shared context, not new information.** If it's new to the reader, it belongs in Complication.
- **One ask per email.** Multiple unrelated asks get separate emails or a numbered, unambiguous list.
- **State the recommendation before the reasoning.** Reasoning supports the answer; it doesn't have to arrive first for the answer to be credible.
- **Specificity over hedging.** "Revenue impact is roughly $40k/month" beats "there could be some revenue impact."

## Common anti-patterns

- **Narrative lead-in.** Three paragraphs of "so basically what happened was..." before the point.
- **Buried ask.** The actual request is the last line of paragraph five.
- **No date on the ask.** "Let me know your thoughts" instead of "need your go/no-go by Thursday 5pm."
- **Reasoning-first.** Explaining the whole analysis before stating the recommendation, forcing the reader to hold the thread until the end.
- **CC-as-alignment.** Copying everyone instead of naming who the decision is actually for.

## Seniority signals

- **Beginner:** writes clear status emails, no ask confusion.
- **Intermediate:** writes decision emails that get a yes/no reply instead of "let's discuss."
- **Advanced:** compresses complex trade-offs into a 300-word decision email without losing the substance.
- **Expert:** execs forward these emails as-is because the structure already does the persuading.

## Files

- decision emails tied to a project: link or paste into `.ai/memory/projects/<slug>/decisions.md` after sending, so the ask and outcome are on record
- status emails: no persistent file needed unless the project changelog benefits from the same summary
