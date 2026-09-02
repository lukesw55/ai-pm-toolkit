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
│       ├── changelog-archive.md # older entries, rotated verbatim
│       ├── profile.md
│       ├── decisions.md
│       ├── experiments.md
│       ├── glossary.md
│       └── retrospective.md
└── _templates/
```

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

## Retrieval protocol

Before a task:

1. read `active-context.md`
2. read the active project's `state.md`, then `session-kickoff.md`
3. scan `profile.md`, `decisions.md`, `experiments.md`, and the newest `changelog.md` entries

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
