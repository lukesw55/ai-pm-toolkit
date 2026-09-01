# Media + transcript parsing (video, audio, transcripts)

## What it is

Processing **videos, audio files, transcripts, and session replays** (interviews, user tests, sales calls, exec recordings) to extract insight. Preserves raw signal + timestamps; synthesises in a second pass.

## Why it matters

User research and internal strategy increasingly lives in video/audio. PMs who "watched the video and vibed with it" lose evidence. PMs who process media structurally — timestamped excerpts, coded themes, preserved originals — compound understanding.

## Input types + handling

| Input | Handling | Tools |
|---|---|---|
| **Transcript (text)** | Primary input — read with `Read` tool; code directly | Any text-reading tool |
| **Video file** | Request / generate transcript first; timestamps as locators | Zoom / Gong / Otter / Rev |
| **Audio file** | Request / generate transcript first | Same |
| **Session replay with narration** | Transcript + screenshots at key moments | FullStory / Hotjar / LogRocket |
| **Live call notes** | Should have a transcript alongside; treat notes as a complement, not a replacement | CRM / call-recorder |

**Rule:** always work from a transcript if available. If only audio/video is available, generate or request a transcript before analysis. Raw audio analysis loses searchability and shareability.

## The three-pass approach for a transcript

### Pass 1 — Orientation (10-15 min per 1h recording)
Skim the transcript for:
- overall arc of the conversation
- moments that stand out (surprises, strong emotions, jargon shifts)
- timestamps or line numbers of these moments

Make a rough map at the top of the synthesis doc:
```
00:04 — opening + context
08:22 — user describes current workflow
14:10 — friction moment 1 (quoted below)
22:15 — friction moment 2
31:40 — tangent (ignore?)
42:05 — summary statement
```

### Pass 2 — Open coding (same as qualitative-synthesis.md)
Go through the full transcript. For each interesting excerpt:
- capture the quote verbatim
- note the timestamp
- tag with open codes

Don't try to group yet.

### Pass 3 — Synthesis + cross-source
Group open codes across multiple transcripts into themes (see `qualitative-synthesis.md`). Each theme's evidence references specific timestamps across sources — a reviewer can jump back to the original in < 10 seconds.

## Ready-to-use template — Media excerpt log

```markdown
# Media excerpt log — [Session type + participant] — YYYY-MM-DD

**Participant:** [ID / pseudonym]
**Segment:** [target segment]
**Interview / test context:** [research question + script version]
**Date of recording:** YYYY-MM-DD
**Raw source:** [link to video / audio / transcript]
**Duration:** [HH:MM]

## Orientation map
Rough arc of the session (timestamps → topics). Helps reviewers skim.

## Coded excerpts

### [Timestamp] — [Short theme tag]
> "[verbatim quote, 1-3 sentences]"

**Open codes:** #code1 #code2
**Context:** [1 sentence — what preceded this]
**Observation:** [non-quote behaviour worth noting — tone, hesitation, screen-share moment]

### [Timestamp] — [Tag]
...

## Session-level observations
- [patterns observed across the session but not tied to one moment]
- [discrepancy between what they said early vs late]
- [body-language / tone signals (only if video; note sparingly)]

## Follow-up questions for next session
- [things this session exposed that you want to test with the next participant]

## Raw source preserved at:
[link — don't delete / don't overwrite]
```

## Ready-to-use template — Cross-source synthesis

For multiple sessions on the same topic:

```markdown
# Media synthesis — [Research topic] — YYYY-MM-DD

**Sessions analysed:** [N] ([list with dates])
**Total media duration:** [e.g., 8 hours]
**Segment coverage:** [segments represented + counts]

## Top themes (ranked)
### Theme 1: [short name]
- frequency: [N / total sessions]
- segment pattern: [where strongest]
- representative quotes (3, with timestamps):
  > "..." — P01 @ 14:10
  > "..." — P03 @ 08:45
  > "..." — P07 @ 22:15
- counter-evidence: [who didn't mention + possible reason]
- interpretation + implication

### Theme 2: ...

## Unexpected observations
- [surprises worth flagging]

## Quality notes
- sample bias: [who we didn't get — segment gaps]
- recency: [how fresh is this data]
- methodology: [interview / task / open-ended discussion]

## Triangulation next
- quant signals to check:
- follow-up research needed:

## Links
- individual excerpt logs: [list]
- raw transcripts + recordings: [folder link]
```

## Working with transcripts via Claude Code

When the user hands over a transcript file (text, markdown, or similar):

1. **Read the file** with `Read`. For long transcripts, use `offset` + `limit` to read chunks.
2. **Do NOT summarise before coding.** Summary loses the signal you're trying to extract.
3. **Work in passes** — the three-pass approach above. Don't try to do it all at once.
4. **Preserve timestamps** — every quote you extract should have its timestamp / line number.
5. **Keep the raw source link** — in the synthesis, always point back to the original.

If the user hands over a video or audio file without a transcript, ask if they can generate one (most platforms — Zoom, Gong, Otter, Rev, OpenAI Whisper — produce transcripts in minutes). Working directly from audio loses searchability, shareability, and is cognitively expensive.

## Handling session replays

Session replays (FullStory, Hotjar, LogRocket) often lack a verbal transcript. For these:

- take timestamped screenshots at key moments
- write a "narrated transcript" — short descriptive notes per moment (e.g., "14:22 — user clicks filter, scrolls, clicks again — appears to be searching for a specific state")
- treat the replay and the narrated transcript as a unit

## Common anti-patterns

- **"I watched it and got the gist."** The gist is vibes; evidence requires specificity.
- **Summarising before coding.** You lose the exact phrasing that is the whole point of the media.
- **No timestamps.** A quote without timestamp can't be verified; a reviewer can't jump back.
- **Transcript as truth without audio check.** Transcripts (especially auto-generated) mishear key words. On load-bearing quotes, confirm against the audio.
- **Losing the raw.** Copying quotes without keeping the original file accessible → reviewers have no way to verify; months later, the context is gone.
- **Over-interpretation of body language.** Tone and hesitation are weak signals unless you have extensive training; note them, don't build arguments on them.
- **Single-session generalisation.** "One user said X in the video; users want X." N=1.

## Privacy + consent

- user-research recordings require consent; confirm before processing
- redact PII from transcripts before sharing broadly (names, companies, emails)
- respect geographic data-handling (EU transcripts may need EU storage)
- delete recordings per the research protocol retention policy

## Seniority signals

- **Beginner:** watches videos, reports impressions.
- **Intermediate:** produces timestamped excerpts + basic synthesis.
- **Advanced:** produces cross-source syntheses with evidence strength + counter-evidence; preserves raw; triangulates.
- **Expert:** defines the team's media-processing practice (tooling, retention, templates); raises research evidence quality.

## Integration

- Upstream: research plan in `pm-phase-discover/references/research-design.md`.
- Synthesis flow: this reference → `qualitative-synthesis.md` → `triangulation.md` → discovery artefacts (Impact Brief, One Pager).
- MCP: `Read` for transcripts. No direct video-parsing MCP tools are typically available, so generate transcripts externally when needed.

## Files

Individual excerpt logs → `.ai/memory/projects/<slug>/research/<topic>/sessions/P<NN>.md`. Cross-source syntheses → `.ai/memory/projects/<slug>/research/<topic>/synthesis-<date>.md`. Raw sources kept in a linked folder (not committed to git if privacy-sensitive; use external storage + link).
