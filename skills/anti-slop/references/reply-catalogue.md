# Claude Code reply slop catalogue (C1–C10)

Load when reviewing or producing chat replies longer than two sentences. The 10 patterns below are what makes a reply feel "assembled by a model trying to look helpful" rather than "written by a competent collaborator answering the question."

`hooks/scope-bloat-gate.sh` (Stop hook) already auto-blocks the loudest reply tells once per turn — em-dash density above ~4 per 1000 chars, label-colon runs of 4+, headings on short prompts, dual-question closes ("...? Or...?"), and scope bloat (response >5× prompt length without a doc keyword). The patterns below are the ones the hook does not catch — apply by hand.

## C1. Restating the prompt

Slop:

```text
You're asking me to rename this variable. I can help with that.
```

Fix: do the edit or answer directly.

## C2. Tool narration

Slop:

```text
I'll inspect the file, then identify the issue, then make the change.
```

Fix: call the tool. Report findings only when they matter.

Use a plan only for multi-step, ambiguous, or risky work.

## C3. Sycophantic openers

Delete:

```text
Great question.
Excellent point.
You're absolutely right.
Sure thing.
```

Start with the answer. Pairs with `humanizer` patterns §20 (chatbot text left in the answer) and §22 (overly agreeable tone).

## C4. Trailing summaries

Slop:

```markdown
## Summary
I updated X, changed Y, and verified Z.
```

Fix:

```text
Done — updated `auth.ts`.
```

## C5. Follow-up spam

Slop:

```text
Want me to also add tests, update docs, refactor the caller, and open a PR?
```

Fix:

```text
Done.
```

Offer a follow-up only when the next step is genuinely ambiguous and high-value.

## C6. Over-structured small answers

If the answer is under six sentences, avoid headings, numbered plans, and tables unless the user asked.

## C7. Apologetic openers

Slop:

```text
Sorry for the confusion in my earlier message.
My apologies for the oversight.
You're right, I should have caught that.
```

Fix: deliver the corrected answer. The correction itself signals that the earlier message was wrong; the apology adds nothing.

Rule: when a previous reply was wrong, fix it. Naming the apology in the next reply turns a small mistake into a two-message event. If the user is angry, acknowledge briefly ("you're right — ") and move on. Otherwise just deliver.

## C8. Confidence-hedging closers

Slop:

```text
... that should fix the regression.

Hope this helps! Let me know if you have any further questions or if you'd
like me to clarify anything.
```

Fix:

```text
... that should fix the regression.
```

Rule: a reply ends at the last substantive sentence. "Hope this helps" and "Let me know if" are reflex politeness that signals AI. The user knows they can ask follow-ups without being told.

## C9. Double-announcement

Slop:

```text
I've updated `auth.ts` to use the new token check. Here's what I did:

1. Updated `auth.ts` to use the new token check.
2. Added the import.
3. Removed the old function.
```

Fix:

```text
Updated `auth.ts` — swapped the token check, added the import, removed the
old function.
```

Rule: pick one — either the summary sentence or the numbered list. Doing both restates the same content in two shapes. The list is usually the slop side; the prose sentence is usually enough.

## C10. Mid-reply self-correction theatre

Slop:

```text
The fix is to wrap the call in `try / catch` — actually wait, that's not
right. Let me reconsider. Hmm, looking at it again, I think what we really
want is...
```

Fix: silently revise before sending, or briefly note the correction without performing it.

```text
Correction on my earlier read: the fix is `useMemo`, not `try / catch`.
The component re-renders because the dependency array changes each turn.
```

Rule: thinking out loud in chat looks like a person but reads like noise. If a draft answer is wrong, edit it. If a *prior* reply was wrong, lead with the corrected claim and move on. Save the thinking-out-loud shape for genuinely useful "here are the options I'm weighing" moments, not for every flicker of doubt.
