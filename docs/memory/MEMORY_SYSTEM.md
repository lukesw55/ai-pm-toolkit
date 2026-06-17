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
├── active-context.md
├── index.md
├── inbox.md
├── people/
├── projects/
│   └── <slug>/
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
A simple map of known projects, people, domains, and where to look next.

### `inbox.md`
Temporary raw notes, copied facts, rough observations, meeting snippets, or loose findings that are not yet organized.

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
2. read the active project's `profile.md`
3. scan `decisions.md` and `experiments.md`
4. check `inbox.md` for fresh raw notes

After a task:

1. move durable findings out of `inbox.md`
2. append decision or experiment entries when relevant
3. refresh `active-context.md` if focus changed
4. update `index.md` if a new project or person was added

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
