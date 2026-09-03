---
name: pm-phase-discover
description: Lean Double Diamond **Discover phase** skill for PMs. Invoke whenever the work upstream of building is still soft — vague brief, pile of feature requests, conflicting stakeholder asks, a new market/segment, or any moment where "what exactly are we solving and for whom?" is fuzzy. Also trigger when the user mentions user research, JTBD, personas, opportunity assessment, competitive analysis, problem statements, entrevistas com usuários, or asks to "understand the problem" / "entender o problema" — even without naming "discovery". Covers problem framing, research design/synthesis, segmentation/JTBD, opportunity & hypothesis design (including the opportunity solution tree and assumption map that bridge to the one-pager), and competitive/market intelligence. For qualitative synthesis of interviews, triangulation with quant data, or parsing of videos/transcripts, also pull in `pm-transversal-analysis`.
---

# PM Phase — Discover

> Double Diamond Phase 1 of 4. See also `pm-phase-define`, `pm-phase-develop`, `pm-phase-deliver`.

Convert scattered requests, symptoms, and anecdotes into a sharp, evidence-backed picture of **who has which problem, how painful it is, and what would count as a useful learning step**.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## When to use this skill

Invoke this skill whenever the work upstream of building is still soft:

- a brief is vague or solution-shaped when the problem is not yet clear
- stakeholders disagree about what "the user" wants
- the team is being asked to build before anyone has talked to real customers
- a segment, JTBD, or persona needs to be defined or refined
- you need to rank opportunities or design the smallest useful test
- a synthesis needs to become an opportunity solution tree, a solution needs its assumptions mapped, or a solution arrives with no parent opportunity ("árvore de oportunidades", "mapear premissas")
- a competitor's move is triggering a reactive response and you need to separate signal from panic

If the work is already clearly framed and evidence is solid, skip this skill and use `pm-phase-define` directly.

The stage-2 artefact this skill commonly produces is the **Impact Brief** — see `references/impact-brief.md` for the template (stage 2 of 8 in `../WORKFLOW.md`).

The stage-3 handoff artefact is the **Opportunity Solution Tree** — see `references/opportunity-solution-tree.md`; it bridges `discovery/<topic>/synthesis.md` to the stage-4 One Pager (stage 3 of 8 in `../WORKFLOW.md`).

## Prime directive

**Learn the smallest thing that changes the decision.** Research is cheap when targeted and expensive when performative. Expert PMs do not treat interviews as sales calls, do not collect quotes without synthesis, and do not polish a prototype before the underlying risk is resolved.

## Calibrated disagreement

The default failure in Discover is accepting solution-first framing at face value. Challenge the assumption behind a request that arrives as a solution ("build X") before researching it as if the problem were already settled — see `../DOCTRINE.md`.

## Core sub-skills

This skill covers five discovery competences. Each has a load-order hint: stay at the SKILL.md level for routine work; open a reference file only when you need the full template, checklist, or anti-pattern list.

### 1. Problem framing

Turn scattered requests into an explicit statement of **user + problem + desired outcome + assumptions + constraints**. Strong delivery is impossible if the team is solving the wrong problem or one defined so loosely that every interpretation fits.

Typical output: a one-page problem brief with target user, pain description, evidence base, assumptions log, and what would have to be true for the frame to be wrong.

Anti-patterns: starting with a favoured solution, broad goals ("improve UX"), mixing user pain with internal asks, never revisiting the frame as evidence changes.

→ Deep-dive: `references/problem-framing.md`

### 2. Customer research design and synthesis

Plan, run, and synthesise research fit for the decision at hand. Expert PMs do not "talk to customers"; they pick a method, a sample, and a synthesis approach that actually reduces the specific uncertainty blocking the team.

Typical outputs: research brief, screener, interview guide, thematic synthesis, insight repository entry, implications for product.

Anti-patterns: treating interviews as sales calls, selecting only loud customers, solution-first questions, collecting quotes without synthesis, using one method for every question.

→ Deep-dive: `references/research-design.md`

### 3. Segmentation, JTBD, and need modelling

Structure demand into meaningful user groups, jobs, contexts, and needs so the team can make targeted trade-offs instead of designing for "everyone". Segmentation is the scaffolding that lets strategy, positioning, and GTM stay coherent as the product grows.

Typical outputs: segment definitions, JTBD map, journey map for the highest-value segment, needs taxonomy.

Anti-patterns: treating marketing demographics as product segments, decorative personas, conflating power users with new users, one-size-fits-all journeys.

→ Deep-dive: `references/jtbd-segmentation.md`

### 4. Opportunity assessment and hypothesis design

Rank opportunities by evidence strength and expected impact, then design the smallest test that reduces the biggest remaining risk. Discovery becomes actionable only when a PM can compare opportunities and commit to a specific learning step.

Typical outputs: hypothesis log (belief + expected evidence + invalidation condition), opportunity scorecard, opportunity solution tree with its assumption map, MVP or fake-door test plan, experiment backlog entry.

Anti-patterns: treating ideas as opportunities, orphan solutions (no parent opportunity), testing too much at once, polishing prototypes before core risks are resolved, "we'll know it when we see it" acceptance criteria.

→ Deep-dive: `references/opportunity-hypothesis.md`
→ Deep-dive: `references/opportunity-solution-tree.md` (stage 3 → 4 bridge)

### 5. Competitive and market intelligence

Collect and interpret competitor, category, and analyst signals to understand positioning, timing, gaps, and defensible advantage. The goal is not feature parity — it's separating market signal from noise so the team sequences bets with awareness of the strategic environment.

Typical outputs: competitive brief, market map, positioning memo, win-loss themes, analyst-note summary.

Anti-patterns: feature-parity obsession, treating competitor launches as strategy, ignoring adjacent substitutes, collecting screenshots without analysing customer trade-offs.

→ Deep-dive: `references/competitive-intel.md`

## Workflow

Use this flow when invoked. Tailor depth to the phase — Lean Double Diamond still applies.

1. **Read active context** — `.ai/memory/active-context.md` and any existing `.ai/memory/projects/<slug>/profile.md`. Do not redo discovery that has already been done; build on top.
2. **Classify the ask** — problem-framing, research, segmentation, opportunity, competitive, or a mix? State this explicitly to the user in one line before producing artefacts.
3. **Produce the smallest useful artefact** — prefer a problem brief + assumptions list over a 10-page research plan. If the decision can be made with what's already known, say so and stop.
4. **Name what would change the answer** — every discovery output must end with "this would flip to a different conclusion if X".
5. **Update memory** — append insights to `.ai/memory/projects/<slug>/` (experiments.md, glossary.md, or a new `discovery.md` note) and update `active-context.md` if the project focus changes.

## Output contract

When generating a discovery artefact, structure it as:

```text
## [Sub-skill] — [short title]

### Context read
- active context / project memory files consulted

### Known
- hard evidence

### Assumed
- beliefs without evidence, flagged as such

### Framing / synthesis
- the actual output (problem statement, segment, hypothesis, etc.)

### Invalidation condition
- what would change this conclusion

### Next learning step
- smallest test or next question to resolve

### Memory updates
- files touched or to touch
```

## Integration

- Invoked during Discover/Define phases, or whenever a feature request comes in without sufficient framing.
- Outputs feed `pm-phase-define` (vision, KPI tree) and prioritisation (scoring opportunities).
- Experiments designed here are logged via `.ai/memory/_templates/experiment-log.md`.

Communication modes follow `CLAUDE.md#communication-modes`. Per-skill: Lean (default) is a compact artefact with explicit assumptions; Standard is a full research brief for cross-functional alignment; Caveman is a terse one-page frame when the user is under time pressure.

## Success criteria

This skill is working when:
- every build decision traces back to a framed problem and an invalidation condition
- research outputs consistently change the team's behaviour (not just accumulate in a repo)
- segmentation models survive three quarters without being rewritten from scratch
- the team can name two opportunities it chose *not* to pursue and why
