# Tech Team Kickoff — stage 7

## What it is

The **structured handoff moment** from product+design to engineering. Ensures the tech team starts with full context (problem, solution direction, PRD, prototype, tracking plan, NFRs, dependencies) and leaves the kickoff with refined tickets, named owners, and zero pending ambiguity at sprint-start.

## Why it matters

A bad kickoff guarantees rework. Eng discovers open questions mid-sprint, re-clarifies scope, rebuilds after spec changes. A good kickoff collapses the first two sprints' ambiguity into one morning.

## Ready-to-use template — Kickoff agenda (90 min)

```markdown
# Tech Team Kickoff — [Initiative] — [YYYY-MM-DD]

**Attendees:** PM, Tech Lead, Designer, Engineers, Analytics, QA (if distinct), PMM (15 min cameo)
**Facilitator:** @pm
**Duration:** 90 min
**Links:** PRD / prototype / tracking plan / RAID / one-pager

## Pre-reads (sent 48h before, read before meeting)
- PRD
- Prototype link
- Tracking plan
- RAID log
- One Pager (for the "why")

## Agenda

### 0. Purpose (2 min) — PM
- restate bet + expected outcome
- ground in primary metric

### 1. Problem + segment recap (5 min) — PM
- who, what pain, what evidence
- what success looks like in 3 / 6 / 12 weeks

### 2. Solution direction + prototype walkthrough (15 min) — PM + Design
- walk the prototype end-to-end
- show state coverage (empty, error, edge cases)
- explain trade-offs already made
- call out what is **still open** for eng design choices

### 3. PRD review — requirements + acceptance (20 min) — PM + Eng
- go through must-haves one by one
- eng flags anything unclear, oversized, or technically problematic
- adjust acceptance criteria on the spot if needed
- confirm non-goals

### 4. Technical shape (15 min) — Tech Lead
- proposed approach (components, APIs, data flow)
- NFRs (latency, availability, privacy, security)
- reversibility / migration considerations
- observability plan

### 5. Tracking plan walkthrough (10 min) — PM + Analytics
- event schema review
- primary metric + guardrails check
- implementation ownership (web, mobile, backend)
- QA before launch

### 6. Dependencies + risks (10 min) — PM + Tech Lead
- cross-team dependencies: owner + by-when + plan B
- top risks + mitigations
- escalation path

### 7. Slicing + first-sprint plan (10 min) — Tech Lead + Eng
- confirm epic → stories breakdown
- identify the first sprint's 3-5 stories
- story-point / effort estimate (rough)
- spike needed? timebox it

### 8. Launch readiness preview (3 min) — PMM
- GTM timeline (beta → GA)
- enablement needs
- launch comms (release notes drafted in parallel)

### 9. Close: go/no-go to sprint-plan (5 min) — all
- open items + owners + deadlines
- green = proceed to sprint planning
- yellow = fix items in 48h, then proceed
- red = re-plan; back to PM

## Kickoff outputs (produced during / right after)
- [ ] sprint-ready backlog (first 5 stories refined in Jira)
- [ ] dependency list with owners + dates (in RAID)
- [ ] tracking-plan ownership table filled in
- [ ] NFR list approved by tech lead
- [ ] launch-readiness placeholder page created in Confluence
- [ ] meeting recording + summary posted in #init-<name>
```

## Pre-kickoff checklist (PM prep)

48h before:

- [ ] PRD status = Approved
- [ ] Prototype link works + current
- [ ] Tracking plan drafted (not necessarily final — ready for review)
- [ ] RAID updated
- [ ] One Pager linked (for the "why" context)
- [ ] Pre-read sent + RSVP confirmed
- [ ] Design walkthrough rehearsed (don't improvise in the meeting)

If any of these aren't ready, **delay the kickoff**. A half-prepared kickoff wastes 8+ people × 90 min = ~12 person-hours. Better to slip by a few days.

## Who says what

- **PM** facilitates; owns "why" + metric + priority.
- **Tech Lead** owns "how" + feasibility + architecture.
- **Designer** owns UX direction + state coverage.
- **Engineers** flag ambiguity, challenge sizing, propose alternatives.
- **Analytics** confirms tracking plan feasibility.
- **PMM** previews launch constraints.

PM's job is NOT to answer every technical question. PM's job is to ensure every technical question gets to the right person and gets closed.

## Kickoff anti-patterns

- **Spec theatre.** Reading the PRD aloud for 60 minutes. Eng already read it; they're here for discussion.
- **Solution dictation.** PM telling eng how to implement. Wrong forum.
- **Ambiguity tolerance.** "We'll figure it out later" = 3 sprints of rework.
- **Missing stakeholders.** No analytics → tracking plan drifts. No design → UX drift. No tech lead → architecture drift.
- **No decisions.** Meeting ends without owners + deadlines → kickoff didn't happen, a 90-min sync did.
- **Too late.** Kickoff after sprint 1 already started. Rework guaranteed.

## After the kickoff

Within 24h:
- PM posts kickoff summary (decisions + open items + owners + deadlines) in Confluence + Slack
- Tech Lead confirms sprint-1 stories are refined in Jira
- Designer updates prototype with any decisions that changed
- Analytics confirms tracking-plan implementation ownership
- PMM updates launch-timeline placeholder

Within 1 week:
- any "yellow" open items closed; if not, kickoff was too early → re-plan

## Seniority signals

- **Beginner:** attends kickoffs, takes notes.
- **Intermediate:** runs a kickoff with a checklist; decisions mostly get closed.
- **Advanced:** runs kickoffs where eng enters sprint-1 without re-asking context; pre-reads are truly read; open items are rare.
- **Expert:** designs the kickoff mechanics for the org (template, rituals, measured effectiveness) so other PMs inherit a good default.

## Files

Kickoff page → `.ai/memory/projects/<slug>/kickoffs/<initiative>.md`. Confluence publication via `pm-transversal-docs`. Linked from PRD and RAID.
