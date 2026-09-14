# Batch interview synthesis — many transcripts, one codebook, one memo

## What it is

The five-to-ten-transcript case of qualitative synthesis. One shared codebook is fixed first, every transcript gets its own excerpt log in a fixed schema, and a merge step turns the logs into a ranked synthesis memo. Where the harness offers subagents, one worker per transcript writes its log in parallel; otherwise the same steps run sequentially, one file at a time. The method is the three-pass approach in `references/media-transcript-parsing.md` and the coding discipline in `references/qualitative-synthesis.md`; this reference adds what changes when there are many transcripts and possibly many hands.

## Why it matters

Parallel workers drift without a shared codebook: the same pain gets three names and the memo counts it three times. Counting quotes instead of participants inflates a theme that one talkative interviewee carried alone. A lead who reads raw transcripts wholesale re-does the workers' job and drags names and PII into the memo. Batch synthesis is faster only when the merge is disciplined.

## Inputs convention

- Raw transcripts and recordings live in `.ai/memory/projects/<slug>/raw-evidence/<topic>/`. That path is PII by definition: no script reads, rotates or indexes it, and nothing from it is pasted into chat or into a warm memory file.
- An optional manual manifest at `raw-evidence/<topic>/index.md` lists one line per file: id (P01, P02, ...), date, segment, consent recorded, file name, duration. The manifest is the only thing a worker needs to open the right file.
- Participants appear everywhere else as pseudonyms (P01) and locators (P01 @ 14:10, P03 L212), never by name.

## Step 0 — shared codebook

Before any transcript is opened, write the codebook and freeze it:

```markdown
| code | definition | include when | exclude when | research question |
|---|---|---|---|---|
| stall-point | a moment the approval stops moving | the participant names where it waits | general complaints about speed | RQ1 |
| unclear-request | the approver cannot tell what is being asked | ... | ... | RQ2 |
```

Codes come from the research questions in `pm-phase-discover/references/research-design.md` and from an orientation pass over the first transcript. Workers apply the codebook; they do not extend it. A code that does not fit goes back to the lead as a proposal, and the lead decides whether the whole batch gets it.

## Step 1 — one worker per transcript

Each worker produces one excerpt log in the schema of the "Media excerpt log" template in `references/media-transcript-parsing.md`, with two fields added per excerpt: the codebook code, and whether the line is `verbatim` or `inferred`. Worker rules:

- verbatim quotes with a locator; no paraphrase in the quote column
- codes only from the codebook; no theme building, no recommendations
- pseudonym only, even when the transcript carries the real name
- anything the worker concluded rather than heard is marked `inferred`

Logs go to `research/<topic>/sessions/P<NN>.md`, pseudonymised, outside the PII path.

## Fan-out and fallback

Where the harness offers subagents, the lead launches one worker per transcript with identical instructions (codebook, schema, rules, target path) and never reads a raw transcript itself; it reads logs. Fewer than four transcripts, or a harness without subagents, means the sequential path: the lead follows "Working with transcripts via Claude Code" in `references/media-transcript-parsing.md`, reading one file at a time with `offset` and `limit`, and writes the same logs to the same paths. Codex subagent support is not verified in this repo; use the sequential path there. The output is identical on both paths; only wall-clock time differs.

## Step 2 — merge rules

- Same codebook or it does not merge: a log with an unknown code goes back to its worker.
- Frequency counts participants, not quotes: a theme with eleven quotes from four people is 4/N, never 11.
- Every theme carries a counter-evidence column: who contradicts it, and why that might be.
- A line marked `inferred` in a log stays inferred in the memo. Paraphrase does not promote it (`inference-discipline/SKILL.md`, the rule on subagent digests).
- Saturation check from "Sampling discipline" in `references/qualitative-synthesis.md`: did the last two transcripts add a code, or only more quotes? Say which.
- Segment coverage and recency: name the segments with fewer than three participants and flag any transcript older than the rest of the round.

## Ready-to-use template — Merge table

```markdown
| theme | participants (N / total) | segments | locators | counter-evidence | evidence strength (1-5) | inferred? | RQ |
|---|---|---|---|---|---|---|---|
| approvers wait for a reply in email | 4 / 6 | admins, approvers | P01 @ 14:10; P03 L212; P05 L88; P06 @ 02:40 | P04 never stalls (one approver, 9 seats) | 4 | no | RQ1 |
```

## Output

The merge table feeds the "Synthesis memo" template in `references/qualitative-synthesis.md`, saved as `discovery/<topic>/synthesis.md` (the stage 3 artefact in `skills/WORKFLOW.md`). Ranked themes roll up into the project's `insights.md` with locators only. Then `references/triangulation.md` for the quantitative check.

## Common anti-patterns

- **No codebook before fan-out.** Workers invent codes and the merge becomes a translation exercise.
- **Counting quotes.** One talkative participant becomes a trend.
- **Lead reads raw transcripts.** Re-does the work and drags PII into the memo.
- **Names in the memo.** Pseudonyms exist so the memo can travel.
- **Dropping counter-evidence.** A theme with no contradiction listed was not tested.
- **Worker inference promoted by paraphrase.** "P03 seems frustrated" becomes "approvers are frustrated".
- **Summarising before coding.** The gist replaces the evidence.

## Files

Raw → `.ai/memory/projects/<slug>/raw-evidence/<topic>/` (PII, script-free). Excerpt logs → `.ai/memory/projects/<slug>/research/<topic>/sessions/P<NN>.md`. Memo → `.ai/memory/projects/<slug>/discovery/<topic>/synthesis.md`. Ranked themes → `insights.md`.
