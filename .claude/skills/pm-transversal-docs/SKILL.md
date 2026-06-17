---
name: pm-transversal-docs
description: Cross-phase skill for **PM documentation in Confluence and Jira** — structure, templates, voice, linking, and hygiene. Invoke whenever the user is creating or improving Confluence pages (PRDs, strategy memos, DACI, launch plans, retros, FAQs) or Jira tickets/epics (ticket hygiene, linking, parent/child, labels, components, automations). Trigger on "Confluence", "Jira", "cria a página", "estruture o PRD na Confluence", "abre os tickets", "epic structure", "ticket hygiene", "linking", "release page", "documentation", "wiki", "wiki template". Produces doc structures that colleagues actually read and tickets that survive backlog refinement without rework. Complements the MCP Atlassian/Rovo integration when available — this skill is instructional (how to write), not automated execution.
---

# PM Transversal — Confluence & Jira documentation

> Transversal skill. Applies to every Double Diamond phase. The question is never "do we need docs?" — it's "where does this live, what template, and how does it stay alive?"

## When to use this skill

Invoke when:

- a Confluence page is being created for a PRD, strategy, DACI, launch plan, release notes, FAQ, or retro
- a Jira epic/story/task is being structured or restructured
- documentation is drifting from reality and needs a hygiene pass
- PM → Eng handoff artefacts need consistent structure across tickets
- linking (PRD ↔ epic ↔ design ↔ tracking plan ↔ release notes) needs to be designed

This skill is about **how to write and structure** — not about executing API calls. If MCP Atlassian/Rovo integration is available, the skill can be paired with those tools to actually create/update pages and tickets; otherwise the output is content ready to paste.

## Prime directive

**Docs that teammates read > docs that are thorough but ignored.** Structure, voice, and linking are hard skills. Dumping a slack log into a Confluence page is not documentation; it's a graveyard.

## Core sub-skills

### 1. Confluence structure

The anatomy of a PM Confluence page: title convention, metadata block, TL;DR, context, decision/recommendation, appendices. Scan-friendly before it is deep.

Outputs: page template, information architecture for a product space, cross-page linking convention.

Anti-patterns: walls of text, no TL;DR, decision buried at the bottom, no "last updated" signal, no links to related pages.

→ Deep-dive: `references/confluence-structure.md`

### 2. Confluence templates

Concrete templates for the artefacts PMs produce most: PRD, strategy memo, DACI, launch plan, release notes, retrospective, FAQ. Each template is scan-friendly and consistent with the phase skills.

Outputs: ready-to-paste Confluence markdown/wiki markup for each artefact, with placeholders.

→ Deep-dive: `references/confluence-templates.md`

### 3. Jira ticket hygiene

Ticket structure that survives refinement: title, problem, acceptance criteria, scope, links, labels, components, estimate, definition-of-done. Epic/story/task hierarchy matching the backlog grain.

Outputs: ticket template by type, epic structure, labelling convention, "definition of ready" checklist.

Anti-patterns: tickets without acceptance criteria, giant stories disguised as tasks, no links to PRD, inconsistent labels, estimates pulled from thin air.

→ Deep-dive: `references/jira-ticket-hygiene.md`

### 4. Jira linking and automation hints

Cross-ticket linking (blocks/is blocked by, relates to, duplicates), parent/child relationships, automations worth having (transition on label, notify on stall, auto-close stale bugs), and how to keep Confluence-Jira bidirectional links alive.

Outputs: linking map, automation recipe list, Confluence ↔ Jira integration hints.

→ Deep-dive: `references/jira-linking-automation.md`

## Workflow

1. **Classify the artefact** — which Confluence page or Jira ticket type? Pull the matching template.
2. **Anchor on the source of truth** — a PRD page is the source of truth for scope; Jira is the source of truth for status. Don't duplicate what lives elsewhere.
3. **Write TL;DR first** — the first paragraph should let a busy colleague decide whether to read more.
4. **Link explicitly** — every PRD has epic links; every epic has PRD link; every release note has launch-plan link. Orphan docs rot.
5. **Keep "last updated" honest** — add a status block (draft / in review / decided / implemented / archived).
6. **When MCP Atlassian is available** — use `mcp__claude_ai_Atlassian_Rovo__createConfluencePage` / `createJiraIssue` / `editJiraIssue` to persist; otherwise output content for paste.

## Output contract (Confluence page)

```text
# [Page title — convention: {Space-code} / {Type} / {Topic}]

**Status:** Draft | In review | Decided | Implemented | Archived
**Owner:** @name
**Last updated:** YYYY-MM-DD
**Related:** links to Jira epic, design, tracking plan, previous page

## TL;DR
One paragraph. Recommendation + why.

## Context
What prompted this. 3–5 sentences.

## [Body — matches the phase skill artefact contract]

## Open questions
## Appendix / sources
```

## Output contract (Jira ticket)

```text
[Type] [Short title — imperative + user value, e.g. "Allow users to export CSV from dashboard"]

**Problem / user value:**
**Acceptance criteria:**
- [ ] ...
- [ ] ...
**Scope IN:**
**Scope OUT:**
**Links:** PRD, design, tracking-plan event, parent epic
**Labels:** area/X, priority/Y, discovery-phase/Z
**Components:** ...
**Estimate:** ...
**Definition of Done:**
- [ ] instrumentation live
- [ ] docs updated
- [ ] release notes drafted (if user-facing)
```

## Integration

- Every phase: `pm-phase-define` publishes strategy/DACI in Confluence; `pm-phase-develop` publishes PRDs and opens Jira epics; `pm-phase-deliver` publishes release notes and monitoring dashboards with Confluence context.
- Transversais: `pm-transversal-stakeholder` publishes DACI via this skill's Confluence template; `pm-transversal-analysis` publishes interview synthesis in Confluence insight repo.
- MCP tools: when `mcp__claude_ai_Atlassian_Rovo__*` is available, this skill's templates can be pushed directly.
- Agents: `@umberto` uses this skill on every PRD + ticket creation; `@lang` for discovery-page publication; archetype agents for area-specific templates.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is a compact template with TL;DR + body + open questions; Standard is a full Confluence page with appendices; Caveman is the ticket-sized minimum viable write-up.

## Success criteria

- teammates find the right doc in < 30 seconds
- tickets arrive at sprint planning already refined
- PRD ↔ epic ↔ design ↔ release-notes links are bidirectional and alive
- archived pages are archived (not rotting as "most recent")
- onboarding new team members becomes markedly easier
