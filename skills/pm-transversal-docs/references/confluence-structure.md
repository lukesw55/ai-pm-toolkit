# Confluence structure

## What it is

The **information architecture, page anatomy, and linking convention** for PM docs in Confluence. Structure that teammates can navigate in 30 seconds, not search for for 5 minutes.

## Why it matters

Confluence is where PM decisions, strategies, PRDs, launches, and retros live. Without structure, the same team's space looks different per PM, contains duplicate-ish docs, and the "source of truth" becomes unknowable. Structure is a durable productivity multiplier.

## Space-level structure (product area)

```
📚 [Product area] — Confluence space
├── 📘 About this space (landing page — what lives where, conventions, owners)
├── 📂 Strategy
│   ├── Strategy memo (current horizon)
│   ├── KPI tree
│   ├── Prior strategy memos (versioned)
│   └── Competitive + market
├── 📂 Discovery
│   ├── Impact Briefs
│   ├── Research synthesis
│   ├── JTBD + segments
│   └── Insight repository
├── 📂 Priorities
│   ├── Discovery prioritisation (stage 1 output)
│   ├── Product prioritisation (stage 5 output)
│   └── Roadmap narrative
├── 📂 One Pagers
│   └── [per-initiative pages]
├── 📂 PRDs
│   └── [per-initiative pages]
├── 📂 Launches
│   ├── Launch plans
│   ├── Release notes (public + internal)
│   └── Close-out memos
├── 📂 Decisions
│   ├── Decision log (index)
│   ├── DACI pages
│   └── ADRs
├── 📂 Operating
│   ├── Weekly reports
│   ├── Monthly operating reviews
│   ├── QBRs
│   └── Meeting notes (rotating)
├── 📂 Playbooks + templates
└── 📂 Archive (old + superseded)
```

Adapt to your org — but the principle is **one folder per artefact type**, not per sprint or per quarter.

## Page anatomy (works for every PM page)

```markdown
# [Page title]

**Status:** Draft | In review | **Decided** | Shipped | Archived
**Owner:** @name
**Last updated:** YYYY-MM-DD by @name
**Related:** [linked pages — PRD, strategy, DACI, design, tracking plan]
**Stage:** (optional — which of the 8 workflow stages this page serves)

## TL;DR
One paragraph. Recommendation or conclusion + why. If the reader stops here, they got the essential.

## Context
3-6 sentences. What prompted this, what this covers, what it doesn't.

## [Body — specific to artefact type]
Each artefact type follows its own template (see `confluence-templates.md`).

## Open questions
- [ ] Q: ... — owner — by when

## Appendix / sources
- links to raw data, research, prior docs
```

## Title conventions

Pick one and stick with it. Examples:

- `[PRD] Feature name — YYYY-MM-DD`
- `[DACI] Decision title — YYYY-MM-DD`
- `[Launch] Initiative — YYYY-MM-DD`
- `[One Pager] Initiative — YYYY-MM-DD`

Or flat: `PRD — Feature name`, `DACI — Topic`, `Launch plan — Initiative`.

Date in the title prevents "which version is the real one?" searches.

## Status lifecycle

Every page has a status. Transitions are:

```
Draft → In review → Decided/Approved → Implemented/Shipped → Archived
                                                              ↑
                                        Superseded by [new page] → Archived
```

- Draft = PM still writing; others can review but expect change
- In review = contributors should read + comment by a named date
- Decided/Approved = artefact is the source of truth; changes are versioned
- Implemented/Shipped = the work the artefact describes has landed; maintain for reference
- Archived = moved to Archive folder; link preserved but no longer the source of truth

## Linking conventions

### Bidirectional links

Every PRD links to:
- the Jira epic (downward)
- the One Pager it came from (upward)
- the strategy memo it serves
- the design file
- the tracking plan
- the launch plan

Every Jira epic links back to the PRD. Every launch plan links back to the PRD. Every release note links back to the launch plan.

Unlinked pages rot. Orphan pages get re-created instead of updated.

### "Related" block

At the top of every page, a short "Related:" section with the 4-6 most important links. No digging.

### Cross-space consistency

When linking across spaces (e.g. from product area to shared engineering space), use full URLs, not relative links — they survive space moves better.

## Macros worth using

Confluence macros that PMs benefit from:

- **Info / Note / Warning panels** for status, migration notes, risks
- **Status lozenges** (green/yellow/red/grey) for sections with health signals
- **Table of contents** at the top of long pages
- **Roadmap planner** / **page properties** for dashboardable views
- **Jira issue / filter** macros for live ticket status
- **Include page** for re-using common sections (e.g. team disclaimer, KPI definition)

Avoid:

- nested toggles 3+ deep (lost)
- tables of 30+ columns (unreadable)
- decorative GIFs (loads slow, distracts)

## Ownership + maintenance

- each folder has an owner (typically the area PM or lead PM)
- each page has an owner (the person responsible for it being accurate)
- stale pages (> 3 months no edits, status: Draft or In review) auto-flagged for refresh or archive
- "About this space" landing page names conventions + owners — read on day 1 by new team members

## Anti-patterns

- **Dumping ground spaces.** Every PM creates under their own folder; space becomes untraceable.
- **No TL;DR.** Reader has to scroll to know what the page is about.
- **No status block.** Is this the current source of truth, or superseded?
- **Orphan pages.** No links in or out; nobody updates them.
- **Inconsistent titles.** Hard to scan, hard to search, hard to trust.
- **Deeply nested hierarchies.** 6 levels deep; users can't navigate.
- **Page-as-project-log.** One long page capturing every Slack discussion. Unreadable.

## Migration pattern (for existing chaos)

If the space is already messy:

1. **Do NOT rewrite everything.** Focus on the next 3 months of new work.
2. Create the folder structure above (empty folders with READMEs).
3. New work follows the new structure from day one.
4. Opportunistically move existing pages when you touch them.
5. At quarter boundary, do a 1-hour prune of the chaos folder.

Don't let perfect migration paralyse new work.

## Files

Confluence is the "publish" target. Draft in `.ai/memory/projects/<slug>/` in markdown, then publish. If MCP Atlassian is available, use `createConfluencePage` / `updateConfluencePage` / `getConfluencePage` (Atlassian MCP; the server prefix varies by environment) — see `jira-linking-automation.md` for patterns.
