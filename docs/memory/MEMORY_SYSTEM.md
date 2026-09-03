# Memory System

Umberto needs memory that survives switching between projects, products, and stakeholders.

This system is inspired by navigable memory structures: information is easier to recover when it is stored with **context, place, and purpose**, not as one flat running summary.

## Principles

1. Keep **raw signal** when it matters.
2. Summaries should point back to evidence.
3. Project memory and people memory should stay separate.
4. Durable decisions deserve their own log.
5. Experiments should record both result and confidence.

## Layout

```text
.ai/memory/
├── active-context.md        # hot pointer (≤2 KB), written by init/park/activate
├── index.md                 # one line per known project
├── inbox.md                 # manual scratch — no script reads or writes it
├── context-events.jsonl     # context-switch log (memory.py + context_watch.py)
├── people/                  # optional, manual-only PII notes; no script creates or touches it
├── projects/
│   └── <slug>/
│       ├── state.md             # read FIRST on resume; park/close blocks
│       ├── session-kickoff.md   # working agreement; read after state.md
│       ├── changelog.md         # 3 newest entries (memory.py log)
│       ├── changelog-archive.md # older entries, rotated verbatim; index block on top
│       ├── state-archive.md     # oldest state blocks, folded verbatim by memory.py distill
│       ├── decisions-archive.md # same, for decisions.md
│       ├── .distill/            # transient fold package: manifest.json, blocks.md, synthesis.md
│       ├── profile.md
│       ├── decisions.md
│       ├── experiments.md
│       ├── glossary.md
│       └── retrospective.md
└── _templates/
```

Every `*-archive.md` opens with an index block, one line per archived block, regenerated on every append and rebuilt by `memory.py index <slug>`. It is the entry point for cold-layer retrieval: the index answers "what is in there" without opening a block.

## File roles

### `active-context.md`
The single source for what project is currently in focus.

### `index.md`
One line per known project, appended by `init_context.py`.

### `inbox.md`
Temporary raw notes, copied facts, rough observations, meeting snippets, or loose findings that are not yet organized. Manual only: no script creates, reads, or rotates it.

### `projects/<slug>/state.md`
Where things stand. Newest-first park/close blocks written by `memory.py park`; the pointer names it as the first file to read on resume.

### `projects/<slug>/session-kickoff.md`
The project's working agreement — goal, wedge, metric, stakeholders, traps. Read after `state.md`; `memory.py distill` warns when it grows past its soft cap.

### `projects/<slug>/changelog.md`
Session history via `memory.py log`. Keeps the 3 newest entries; older ones rotate verbatim into `changelog-archive.md`.

### `projects/<slug>/profile.md`
The project's operating profile:
- mission
- target users
- constraints
- success metrics
- current wedge
- important links

### `projects/<slug>/decisions.md`
Decision log with:
- date
- title
- status
- context
- choice
- tradeoffs
- follow-up

### `projects/<slug>/experiments.md`
Experiment log with:
- hypothesis
- probe
- metric
- result
- confidence
- next decision

### `projects/<slug>/glossary.md`
Terms, acronyms, product language, domain vocabulary.

### `projects/<slug>/retrospective.md`
Patterns, lessons, recurring pitfalls, and what to repeat.

## Layers (hot / warm / cold)

The layering in `CLAUDE.md` maps onto these files. Nothing in the cold layer is read wholesale.

| Layer | Files | Read when |
|---|---|---|
| Hot | `active-context.md` (pointer, ≤2 KB) | injected at session start by `stage_context.py` |
| Warm | `projects/<slug>/state.md`, `session-kickoff.md`, `decisions.md`, `profile.md`, the 3 newest `changelog.md` entries | working on that project |
| Cold | `changelog-archive.md`, `state-archive.md`, `decisions-archive.md`, `raw-evidence/`, transcripts | grep-first: the archive index (`memory.py index <slug>`) or `grep -n` for a term or date, then only the matching block |

## Caps and consolidation

Warm files carry soft caps. `memory.py doctor` warns above them; `memory.py distill <slug>` lists the offenders (exit 2) and the protocol.

| File | Soft cap | How it shrinks |
|---|---|---|
| `changelog.md` | 6 KB (and 3 entries) | `memory.py log` rotates older entries into `changelog-archive.md`; `distill` folds within the 3 |
| `state.md` | 16 KB | `distill --prepare --file state` → `state-archive.md` |
| `decisions.md` | 12 KB | `distill --prepare --file decisions` → `decisions-archive.md` |
| `session-kickoff.md` | 4 KB | prose: rewrite by hand when flagged |
| `profile.md` | 12 KB | prose: rewrite by hand when flagged |

The fold is model-assisted and two-step so nothing is summarised silently:

1. `python3 scripts/memory.py distill <slug> --prepare [--file changelog|state|decisions]` picks the oldest dated `## ` blocks (never the newest, never an undated block such as the template example) until the file would sit a quarter below its cap, and writes `projects/<slug>/.distill/`: `blocks.md` (the blocks, verbatim), `manifest.json` (sha256 of the source and of each block), `synthesis.md` (rendered from `.ai/memory/_templates/distill-synthesis.md`, with a dated heading and an index line per block). With an explicit `--file` on a file still under its cap, exactly one block is folded.
2. The model replaces the `[Fill in ...]` paragraph in `synthesis.md` with three to six lines: decisions kept, constraints that still bind, open threads. Narration goes.
3. `python3 scripts/memory.py distill <slug> --apply` re-checks the source hash and every block hash, rejects an untouched skeleton, projects the new size (exit 2 and nothing written if the synthesis pushes the file over its cap), appends the blocks to the sibling archive and regenerates its index block, re-reads the archive to confirm each block landed, and only then rewrites the source with the synthesis in the blocks' place.

Guarantees: content is moved, never deleted; the archive is rebuilt into a sibling temporary file, verified block by block, and swapped in with an atomic replace, so a failed run never leaves it half-written; the archive is verified before the source is touched; the newest dated block is never folded; a package whose source changed since `--prepare` is refused and can be replaced by a new `--prepare`.

## PII denylist

`memory.py` refuses, in code, any path with a segment in `PII_DENY = ("raw-evidence", "people", "data")` relative to the repo root: `log`, `park`, `activate`, rotation, `distill --prepare/--apply`, and the archive writes all pass through `guard()`. `doctor` skips such projects with a WARN. A project literally named `data` is therefore unusable through the scripts by design.

## Retrieval protocol

Before a task:

1. read `active-context.md`
2. read the active project's `state.md`, then `session-kickoff.md`
3. scan `profile.md`, `decisions.md`, `experiments.md`, and the newest `changelog.md` entries

From the cold layer (grep-first, read-before-reasoning):

1. list before opening: `python3 scripts/memory.py index <slug>` prints one line per archived block across the three archives (slug `repo` covers the repository-level changelog archive). By term or date: `grep -n -i "<term>" .ai/memory/projects/<slug>/*-archive.md`.
2. open only the block that matched, by its heading: `sed -n '/^## <heading>/,/^## /p' <archive>`. Never read a whole archive into the context.
3. cite the heading and its date when you reason from the block. If the fact matters again, rewrite it into the warm set (`decisions.md`, `state.md`) instead of reopening the archive next session.
4. `raw-evidence/` is PII and script-free: search it in place (`grep -ril "<term>" .ai/memory/projects/<slug>/raw-evidence/`), read only the passage you need, and never paste a transcript into memory or chat. A manual index inside that folder (`.ai/memory/projects/<slug>/raw-evidence/index.md`, one line per file: date, source type, topic) is optional and is never touched or injected by a script.

After a task:

1. append decision or experiment entries when relevant
2. refresh `active-context.md` if focus changed
3. update `index.md` if a new project was added

## What belongs in memory

Store:
- durable decisions
- user truths
- constraints
- working agreements
- rejected paths worth remembering
- experiment results
- terminology

Do not over-store:
- throwaway drafts
- trivial implementation noise
- obvious facts already present in code

## Compression rule

Summarize for speed, but preserve a pointer to the underlying evidence.

The target is not "short memory."
The target is **retrievable memory**.
