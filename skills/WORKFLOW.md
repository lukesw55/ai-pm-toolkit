# Workflow — 8-stage gate progression

This toolkit maps to a realistic product-team flow. Each stage has an owner, an artefact, a "Definition of Done" gate, and a recommended skill to invoke. Transitions are flexible: any stage can move to any other based on evidence, though the typical path runs left to right.

```
START
  ↓
[1] Discovery Prioritization
  ↓
[2] Impact Brief (GTM)
  ↓
[3] Discovery
  ↓
[4] One Pager
  ↓
[5] Product Prioritization
  ↓
[6] PRD + Prototype + Refinement
  ↓
[7] Tech Team Kickoff
  ↓
[8] Delivery
```

## Stage → Skill → Artefact map

| # | Stage | PM skill | Key reference | Artefact | Gate to advance |
|---|---|---|---|---|---|
| 1 | Discovery Prioritization | `pm-phase-define` | `pm-prioritization-regua-comum` (opportunity-level) | `discovery-priorities.md` | top N candidate problems selected with rationale |
| 2 | Impact Brief (GTM) | `pm-phase-discover` | `references/impact-brief.md` | `impact-brief-<topic>.md` | business + GTM impact articulated, invalidation conditions named |
| 3 | Discovery | `pm-phase-discover` | `research-design.md` + `jtbd-segmentation.md` + `opportunity-hypothesis.md` | `discovery/<topic>/synthesis.md` | problem framed, JTBD validated, hypothesis ranked |
| 4 | One Pager | `pm-phase-define` | `references/one-pager.md` | `one-pager-<topic>.md` | one-pager approved by stakeholders + mandatory pm-product-sense shadow evaluation (non-blocking; formal gate unchanged) |
| 5 | Product Prioritization | `pm-phase-define` | `pm-prioritization-regua-comum` (build-level) | `priorities.md` update | bet approved for build |
| 6 | PRD + Prototype + Refinement | `pm-phase-develop` | `prd-writing.md` + prototype loops | `prds/<feature>.md` + prototype | PRD approved, prototype validated + mandatory pm-product-sense shadow evaluation (non-blocking; formal gate unchanged) |
| 7 | Tech Team Kickoff | `pm-phase-develop` | `references/tech-team-kickoff.md` | kickoff deck + epic | team aligned, tickets refined, dependencies & NFRs clear |
| 8 | Delivery | `pm-phase-deliver` | `launch-readiness.md` + `release-notes.md` + `post-launch-monitoring.md` | launch kit + close-out | GA shipped, impact measured |

Transversal skills (`pm-transversal-stakeholder`, `pm-transversal-docs`, `pm-transversal-analysis`, `pm-transversal-comms`, `data-science-analyst`) apply at **every stage**: use them whenever cross-function alignment, Confluence/Jira publication, quali+quant synthesis, short-form comms (email/chat), or technical data-work (audit a CSV export, validate SQL, check leakage, A/B-test analysis, baseline ML) is needed. The first four are the PM lens; `data-science-analyst` is the technical lens under them. `pm-transversal-analysis` decides what the data *means for product*; `data-science-analyst` decides whether *the analysis itself* is sound. `pm-transversal-comms` covers the highest-frequency artefacts of the four — email and chat — while `pm-transversal-stakeholder` and `pm-transversal-docs` handle longer-form memos/decision-rights and Confluence/Jira respectively. They chain. In Discover, `data-science-analyst` is fine for file-level audit, but ML/forecasting and instrumentation queries stay out until Define and Develop.

### Shadow gate: pm-product-sense at stages 4 and 6

Stages 4 (One Pager) and 6 (PRD) each carry a **mandatory non-blocking shadow evaluation**: running `pm-product-sense` EVALUATE mode against the artefact is required before advancing, but its score never blocks the advance — the formal gate in the table above stays the sole authority on whether the stage is done. Treat a low shadow score as a strong signal to sharpen the artefact before it moves on, not as a hard stop; `advance_stage.py` has no score- or marker-based blocking logic, by design, in this batch. See `pm-product-sense/references/evaluation-rubric.md` for the scoring rule and the explicit criteria that would justify promoting this to a formal (blocking) gate in the future — promotion should prefer dimension-level blocking over a single aggregate-score threshold when it happens.

### Slop-removal transversals (every stage, every artefact)

Three skills plus one runtime hook split the "kill AI tells" job by surface:

| Surface | What it owns | Trigger |
|---|---|---|
| Prose (memos, PRDs, Confluence/Slack/customer comms) | `humanizer` (29-pattern engine) + `humanize-deliverables` (publish gate, sha256 sentinel) | before any prose ships outbound |
| Code, comments, identifiers, doc structure, replies, file artefacts | `anti-slop` | before writing/editing code, comments, README/PR/ticket structure, planning docs, or any reply longer than two sentences |
| Reply-time runtime gate | `hooks/scope-bloat-gate.sh` (Stop hook, wired in both `.claude/settings.json` and `.codex/hooks.json`) | auto-blocks once per turn: em-dash density, label-colon runs, headers on short prompts, dual-question close, scope bloat |

`humanizer` owns prose, `anti-slop` owns everything else (code, structure, replies, unsolicited files), the Stop hook owns runtime enforcement. When in doubt, run the matching skill: a sweep costs seconds; shipping AI-tinted material costs credibility.

Two more transversals apply at every stage:

- `inference-discipline` — the hallucination gate. Every claim about external state is either verified this turn or labelled and approved before action; `inference-discipline-gate.sh` blocks writes and outbound publishes that still carry unresolved markers.
- `pm-storytelling` — the narrative layer. Any stage artefact meant to persuade (impact brief, one-pager, PRD opener, launch comms) gets a spine (tension → insight → change → takeaway) before `humanizer` polishes the voice.

## Why two prioritisations

- **Discovery Prioritization (stage 1)** decides *which problems to invest discovery on*. Cheap inputs (hunch + limited evidence); picks the top N bets to research.
- **Product Prioritization (stage 5)** decides *which one-pagers to build*. Richer inputs (validated problems, sized impact); picks the bet that clears the build bar.

A single prioritisation collapses these and under-funds either discovery or delivery. Keeping them separate protects both ends of the pipeline.

## Active context

The current stage lives in `.ai/memory/active-context.md` under "Current stage". Update it manually or via:

```bash
python scripts/advance_stage.py <stage-slug>
# e.g.
python scripts/advance_stage.py product-prioritization
```

Valid slugs: `discovery-prioritization`, `impact-brief`, `discovery`, `one-pager`, `product-prioritization`, `prd`, `tech-kickoff`, `delivery`.

Agents and hooks read this file to orient before suggesting the next move.

## Hooks (optional)

`.claude/settings.json` (Claude Code) and `.codex/hooks.json` (Codex) each define a `UserPromptSubmit` hook that injects the current stage into every turn, making the agent stage-aware automatically in both harnesses. See `scripts/stage_context.py` for the implementation. Removing the hook is safe: the skills and agents still work, you just lose automatic stage-surfacing and read `active-context.md` manually.

## Bypass when appropriate

The flow is a default, not a cage. Any stage can be skipped with explicit rationale:

- Bug fix → skip to stage 6 (PRD) or 8 (Delivery) with a one-paragraph fix memo
- Spike / learning week → stage 3 plus optional 4
- Deprecation → decision memo (`pm-phase-define/references/decision-memo-daci.md`) plus stages 7 and 8 only

When skipping, record the rationale in the project changelog so the team knows why the usual gates did not apply.
