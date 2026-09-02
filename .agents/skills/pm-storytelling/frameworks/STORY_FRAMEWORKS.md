# Story frameworks

Frameworks for transforming assignments, briefs, drafts, evidence dossiers, and AI-generated content into a narrative with a spine. Pick **one** primary framework. The selection heuristic at the bottom helps when the right choice is not obvious.

The first nine frameworks are general-purpose. Frameworks 10–13 are PM-specific and were added when this skill was forked into the PM skills repo.

---

## 1. SCQA + Insight Arc

Best for: academic assignments, consulting-style briefs, business explanations, strategic narratives.

1. **Situation** — context the audience needs
2. **Complication** — tension, contradiction, or problem
3. **Question** — what the complication forces us to ask
4. **Answer** — conclusion, recommendation, or insight that resolves it
5. **Implication** — why the answer matters

Use when the assignment asks for analysis, explanation, recommendation, or argument.

## 2. Before → After → Bridge

Best for: product stories, transformation stories, personal development, marketing.

1. Before — current pain or limitation
2. After — desired future state
3. Bridge — method, idea, tool, or decision that enables the change

Use when the source material has a clear transformation.

## 3. Problem → Stakes → Evidence → Recommendation

Best for: persuasive essays, policy proposals, business recommendations.

1. Define the problem concretely
2. Explain why the problem matters now
3. Show available evidence
4. Interpret what the evidence means
5. Recommend a specific action

Use when the assignment expects argument and proof.

## 4. Moment → Conflict → Realisation → Change

Best for: reflection assignments, personal essays, learning journals, leadership narratives.

1. A specific moment
2. A conflict, doubt, or obstacle
3. A realisation or reframing
4. A change in behaviour, belief, or next action

Use when the output should feel personal or experiential.

## 5. Hook → Tension → Reveal → Payoff → CTA

Best for: short-form video, social posts, scripts, campaign content.

1. Hook — immediate curiosity
2. Tension — why the viewer should keep watching
3. Reveal — the insight or twist
4. Payoff — useful meaning
5. CTA — next action

Use when attention and pacing matter.

## 6. Curiosity Gap → Explanation → Example → Application

Best for: teaching, tutorials, educational storytelling.

1. Open with a puzzle or misconception
2. Explain the concept simply
3. Show one concrete example
4. Give the audience a way to apply it
5. Close with a reflection or check-for-understanding

Use when clarity and learning transfer matter.

## 7. Case Study Arc

Best for: client work, product outcomes, portfolio stories, business cases.

1. Context — who or what was involved
2. Challenge — what was hard
3. Approach — what was done
4. Evidence — what changed
5. Learning — what this proves or suggests
6. Next step — where to go from here

Never invent results. Use `[NEEDS METRIC]` when proof is missing.

## 8. Pitch Narrative

Best for: startup, initiative, product, campaign, internal buy-in.

1. Why now
2. Pain or opportunity
3. Existing alternatives and why they fall short
4. New shift or insight
5. Solution
6. Proof
7. Ask

Use when the output needs momentum toward a decision.

## 9. Slide Story Arc

Best for: presentations, decks, workshops, QBRs.

1. Title / promise
2. Problem scene
3. Stakes
4. Insight
5. Framework or solution
6. Proof / example
7. Implications
8. Action / closing

Rules:
- One message per slide
- Slide titles are claims, not labels
- The slide body proves exactly the title; narrow the title until it matches what the evidence shows
- Dense evidence belongs in speaker notes or appendix
- Full deck contract (per-slide fields, QBR slide budget, optional render): `references/deck-storyline.md`

---

## 10. Discovery Synthesis Arc *(PM)*

Best for: turning interview piles, transcripts, and quant signals into a synthesis the team can act on. Pairs with `pm-phase-discover` and `pm-transversal-analysis`.

1. **Question** — the discovery question we set out to answer
2. **Method** — how we collected evidence (n, segments, instruments)
3. **Finding** — what the evidence shows, in plain language
4. **Pattern** — recurring shape across customers / sessions / segments
5. **Implication** — what the pattern means for the product / segment / bet
6. **Open** — what's still unknown or unfalsifiable with current evidence

Rules:
- Quote the evidence by ID, not paraphrased into oblivion
- Don't smuggle a recommendation into the synthesis — that belongs in the one-pager
- Mark every assumption with `[ASSUMPTION]` and every gap with `[NEEDS SOURCE]`

## 11. PRD Opener / Problem Statement *(PM)*

Best for: the first 200–400 words of a PRD or one-pager. Hooks the reader on customer friction before the solution is named.

1. **Customer + JTBD** — who is this for, in one sentence
2. **Friction observed** — what they actually do today, with cited evidence
3. **What we tried (or didn't)** — prior attempts or absence of attempts
4. **Why now** — the specific change in context that makes this the right moment
5. **The bet** — one sentence stating what we'll build and why

Rules:
- Open on the customer's behaviour, not on internal framing
- Cite the evidence inline (interview ID, dashboard link, ticket reference)
- The bet is a sentence, not a feature list. Feature scope lives later in the PRD.

## 12. Decision Memo Narrative (DACI rationale) *(PM)*

Best for: exec memos, ADRs, DACI write-ups where leadership needs to follow the reasoning, not just the verdict.

1. **Decision** — the call, in the first sentence
2. **Why now** — the trigger that forced the decision
3. **Context** — minimum required background
4. **Options considered** — at least the chosen option and one credible alternative, each with their main trade-off
5. **Choice + reasoning** — why this option won, in one or two sentences
6. **Acknowledged risk** — what could go wrong, named not buried
7. **Owner + reversibility** — who owns the call and how reversible it is

Rules:
- The reader should be able to read just sentence 1 and know what was decided
- Trade-offs over advocacy. If the chosen option has no acknowledged downside, the memo is not finished.
- Pair with `pm-transversal-stakeholder` if the memo is going to leadership

## 13. Release Notes Narrative *(PM)*

Best for: external release notes, in-product changelogs, customer-facing updates. Avoids the "we are thrilled to announce" register.

1. **What changed for the user** — described in their language, not internal naming
2. **Why it matters** — one short line, only when the change is non-obvious
3. **How to use it** — short pointer to the place in the product, doc, or API
4. **What's next** — only when there's a credible follow-up, otherwise omit

Rules:
- One section per change, ordered by user-impact (largest first)
- No internal codenames in the title
- No fake excitement — flat tone is fine if the change is small
- Bullet trivia ("Various bug fixes and improvements") is acceptable for true trivia; do not pad it

---

## Framework selection heuristic

Ask, in order:

1. Is this a discovery synthesis from interviews / transcripts / signals? → **Discovery Synthesis Arc**
2. Is this the opening of a one-pager or PRD? → **PRD Opener**
3. Is this an exec memo or decision write-up? → **Decision Memo Narrative**
4. Is this user-facing release content? → **Release Notes Narrative**
5. Is the deliverable analytical (essay, brief, recommendation)? → **SCQA** or **Problem-Stakes-Evidence-Recommendation**
6. Is there a clear transformation in the source? → **Before → After → Bridge**
7. Is it personal / reflective? → **Moment → Conflict → Realisation → Change**
8. Is it educational? → **Curiosity → Explanation → Example → Application**
9. Is it short-form media (video, social)? → **Hook → Tension → Reveal → Payoff → CTA**
10. Is it a customer / portfolio proof story? → **Case Study Arc**
11. Is it a deck or pitch? → **Pitch Narrative** or **Slide Story Arc**

If two frameworks fit, pick the one closer to the audience's expectations — a leadership audience expects Decision Memo cadence; a customer audience expects Release Notes or Case Study cadence; an academic audience expects SCQA.
