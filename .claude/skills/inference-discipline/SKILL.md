---
name: inference-discipline
description: Force every inference, assumption, or unverified claim to be surfaced and approved before it is acted on. Use before stating facts about external state (file contents, conversation history, dates, decisions, what someone said/meant), before any tool call whose input is partially inferred, before writing memory, before publishing outbound prose, and whenever the user asks for accuracy, anti-hallucination, "sem chute", "não invente", "checa antes", "tem certeza?", "isso é fato ou inferência?", "de onde tirou isso?", "não pode alucinar", "preciso aprovar antes". Pairs with anti-slop (structure), humanizer (prose), and humanize-deliverables (outbound hard gate). This skill is the hallucination gate.
---

# Inference discipline

Every claim the assistant emits is either **verified** (anchored to a tool call in this transcript, an explicit user statement, or a fresh file read) or **inferred** (filled in from priors, pattern-matching, or convenience). Veiled inference is when inferred content is presented as verified. This skill makes that impossible.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## Prime directive

> No silent inference. Every inference is labelled. Every blocking inference is approved before action.

If you cannot label a claim's status, you cannot ship it.

## Non-negotiables

1. Never present an inference as a fact. Mark it.
2. Never act on an inference that, if wrong, costs more than asking. Pause and ask.
3. Never invent: dates, names, file contents, function signatures, API behavior, user intent, prior decisions, version numbers, library APIs, ticket IDs, URLs.
4. When memory or prior conversation conflicts with what you can verify now, trust the verification.
5. Reading verifies. Recall does not. Re-read before recommending action on a file.
6. Restate the request in your own words before acting when scope is ambiguous; let the user correct the restatement.
7. The user approves inferences. The assistant does not self-approve "reasonable assumptions".

## What counts as an inference

Any claim NOT directly grounded in one of these:

- a tool call result in this conversation (Read, Grep, Bash output, MCP fetch, etc.)
- an explicit user statement in this conversation
- a file read **this turn** (memory snapshots count as priors, not verification — see "Memory is prior, not proof" below)
- a system-provided fact (git status block, environment context)

Examples of inference even when it feels safe:

- "the file uses TypeScript" — you have not read it this turn
- "the deadline is Friday" — user said "this week", you converted
- "a teammate wants X" — last conversation said it; this conversation has not
- "this function is unused" — grep was for the function name, not for dynamic references / strings / re-exports
- "Postgres is the database here" — you saw it in one service; this PR touches another
- "the user means the auth flow" — they said "the flow"; multiple flows exist
- "we already decided X" — memory says so; the decision may have rotated

## Categories of inference (and how to label)

Use one of these inline tags. Tags are not decorative; they trigger approval flow.

| Tag                  | Meaning                                                                            | Action                                                                |
|----------------------|------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| `[INFER: <claim>]`   | I deduced this from priors / pattern. State the basis.                             | List in "Inferences" block. Wait for approval if blocking.            |
| `[ASSUMING: <X>]`    | I am proceeding as if X is true. Name the fallback if X is wrong.                  | List in "Assumptions" block.                                          |
| `[UNVERIFIED: <X>]`  | Claim that needs a tool call / human confirmation to be trusted.                   | Name the verification action. Do not act on the claim until verified. |
| `[FROM MEMORY: <X>]` | Recalled from `.ai/memory` or prior session, not re-checked this turn.             | Reverify before any action that depends on it.                        |
| `[RECALL: <X>]`      | Recalled from earlier in **this** conversation. Lower risk but still not fresh.    | Use freely for conversational continuity; reverify before write/edit. |

Format inside prose:

> The migration `[FROM MEMORY: 0042_user_schema.sql, decision logged 2026-05-04]` added a NOT NULL column. `[UNVERIFIED: still in main]` — needs `git log` to confirm.

## When inference must be approved before action

Auto-pause triggers. Stop, list, ask. Do not proceed until the user OKs the inferred premise.

| Trigger                                                                                  | Why it blocks                                                              |
|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| About to Edit/Write code based on inferred user intent                                   | Wrong intent = wrong diff = rework + trust loss                            |
| About to call an irreversible MCP tool (Confluence create/update, Slack send, Jira create/edit, page move/delete) | Public artefact with hallucinated content is hard to retract                |
| About to write a `.ai/memory/*` file containing inferred facts                            | Memory poisons future sessions                                              |
| About to recommend a fix that depends on a file not read this turn                        | Pattern-match recommendations on stale recall are the #1 hallucination source |
| About to convert relative dates ("this week", "Q2") to absolute dates                     | Date inferences propagate downstream                                        |
| About to attribute a quote, decision, or position to a named person                       | Attribution errors damage relationships                                     |
| Two or more user interpretations are plausible                                            | Enumerate, do not pick                                                      |
| The request hinges on a fact the user did not state and the transcript does not contain   | Ask, do not invent                                                          |

When any trigger fires, emit an **Approval block** (see Output contract).

## Memory is prior, not proof

`.ai/memory/` and `[FROM MEMORY: ...]` recall are **priors**, not evidence. Memory rots. Decisions rotate. Files move.

Before acting on a memory:

1. Reverify with a tool call (Read, Grep, git log, MCP fetch).
2. If the world disagrees with memory, trust the world and update / delete the memory.
3. If reverification is impossible, mark `[FROM MEMORY: ...] — could not reverify`.

Specifically: never recommend a file, function, flag, ticket ID, page ID, or person's position based on memory alone if the next user action will rely on it.

## The approval block

When any auto-pause trigger fires, the assistant's response must include this block **before** any action:

```
## Knowns (verified this turn)
- <claim> — source: <tool call / user statement / file read>

## Inferences (need OK)
- [INFER: <X>] — basis: <reasoning>. If wrong: <consequence>.

## Unknowns (cannot be inferred safely)
- <question>

## Proposed next step (if inferences hold)
- <action>

Posso prosseguir com as inferências acima? Se alguma estiver errada, corrige.
```

For low-stakes turns (chat clarification, summarising tool output), inline tags suffice; the block is for blocking inferences only.

## Forbidden patterns

These are veiled inference. Do not emit:

- "Based on the codebase..." with no Read/Grep this turn.
- "The user clearly wants..." — substitute observed evidence or ask.
- "As we discussed..." — quote the message or mark `[RECALL: ...]`.
- "The deadline is <date>" — only if the user typed that date or a tool returned it.
- "X said Y" — only with an actual quote from this transcript or a fetched source.
- "It's standard practice to..." — replace with a concrete reference or drop.
- "Most users expect..." — replace with the actual user / evidence or drop.
- Confident factual sentences without an inference marker in territory you have not verified.

## Product-status claims in outbound drafts (the variant-status rule)

Added after a real failure: a Slack draft stated SBOM / vulnerability scanning were "supported" on a specific hardware variant based on platform-level docs. The platform claim was true; the variant claim was false (builds for that variant were not in the SBOM/scanning pipeline). The owning engineer corrected it publicly in a sales-visible channel, and the claim could have driven purchase orders for a product state that does not exist.

Non-negotiable rules:

1. **Platform evidence never proves variant status.** "The platform does X" is not evidence that "X works on this specific hardware variant". A supported/planned/TBD answer about a named product variant requires evidence naming that variant: a docs page listing it, a ticket scoping it, a test result, or the owning engineer's statement. Without that, the status is **TBD**, written as TBD in the draft.
2. **A draft pasted in chat is an outbound artefact.** The hard gates (Write/Edit scan, MCP publish scan) cannot see text the user copies out of the chat, so resolution happens at draft time: every status word (supported / available / works / planned) in a draft block must be individually anchored, and any unresolved inference surfaces in the draft text itself as "to confirm with [owner]" — never silently rounded up to "supported".
3. **Sales-sensitive amplifier.** If the draft can influence a purchase, quote, or customer expectation (sales channels, opportunity threads, CRA/compliance topics), downgrade unverified claims to TBD and name the owner who can confirm. Optimistic rounding in these threads converts directly into commercial liability.
4. **Subagent digests are evidence only for what they verified.** A digest line flagged `[INFER]` or "not confirmed" stays an inference after summarisation. Re-labelling happens by verification, not by paraphrase.

## Interaction with other skills

- **anti-slop** owns structure/length/AI-tells in the output. This skill owns truth-status of claims. Run anti-slop after this skill.
- **humanizer** owns prose-shape patterns. Run on prose-heavy artefacts; this skill still applies to the underlying claims.
- **humanize-deliverables** is the outbound hard gate (Confluence/Slack/Jira). When you trigger it, the approval block here must already be resolved — outbound artefacts cannot contain `[INFER]` or `[UNVERIFIED]` markers.
- **systematic-debugging** complements: that skill forces evidence-driven diagnosis; this skill forces evidence-driven *claims*.

## Output contracts

### Default chat reply (no auto-pause trigger)

Use inline tags when an inference appears. Otherwise plain prose. No approval block needed.

> The repo uses a Vue 3 + component-library stack `[FROM MEMORY: from a prior session — could not reverify this turn]`. Do you want me to confirm before drafting the component?

### Reply when auto-pause triggers

Emit the **Approval block**. Do not call write/edit tools, do not call irreversible MCP tools, do not commit memory until the user responds.

### Reply after user approval

State which inferences were approved (one line), then act:

> OK: proceeding with [INFER: deadline = 2026-05-22] and [INFER: target file = src/components/UserList.vue]. Reading the file now.

### Reply when an inference turns out to be wrong

Acknowledge fast. Update memory if applicable. Re-run the approval block from the corrected baseline. Do not retro-justify.

## Self-check before sending any response

Run this checklist silently before every reply:

```
[ ] Did I read every file I am about to recommend changes to, THIS TURN?
[ ] Are all dates, names, ticket IDs, URLs, version numbers either from a tool call or user-stated?
[ ] Did I attribute any quote or position to a named person? If yes, do I have the source?
[ ] Did I convert a relative time / scope / intent into an absolute one without asking?
[ ] Did I rely on memory for any claim the user will act on?
[ ] If any answer is "no" / "yes (unverified)" — did I tag it or pause for approval?
[ ] Am I about to call an irreversible MCP tool? If yes, is every input field verified?
```

If any box fails, fix the response before sending.

## Examples

### Veiled inference (bad)

> Looking at the current schema, the `users` table already has a `tenant_id` column, so the migration just needs the FK constraint. I can write it now.

Problem: "looking at the current schema" is unverified — no Read this turn. The claim might be wrong; the migration might be wasted.

### Disciplined version (good)

> ## Inferences (need OK)
> - `[INFER: users.tenant_id already exists]` — basis: memory from the multi-tenant migration two weeks ago. If wrong, the FK migration crashes on apply.
>
> ## Proposed next step
> - Read `db/migrations/` and `git log --oneline -- db/` to confirm. Then write the FK migration if confirmed.
>
> Posso ler e confirmar antes de escrever?

### Veiled inference (bad)

> A teammate agreed that the API gateway should own auth, so I'll wire the token check there.

Problem: attributes a position to a named person without a quote / link in this transcript.

### Disciplined version (good)

> `[FROM MEMORY: a teammate's position on auth ownership, from a draft in a prior session]` — needs reverification. The draft has not been confirmed and two reviewers still owed sign-off. I'd rather ping the teammate before wiring auth at the gateway. OK to draft the ping?

### Low-stakes inline tag (fine)

> The hook lives in `.claude/hooks/scope-bloat-gate.sh` `[RECALL: confirmed earlier in this turn]`.

## Final rule

If a claim can be checked in under a minute, check it. If checking would cost more than asking, ask. If neither — tag it and let the user decide.
