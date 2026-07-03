---
name: humanizer
version: 3.0.0
description: >-
  Remove signs of AI-generated writing from text so it passes production AI
  detectors (GPTZero, Copyleaks, Originality.ai, Turnitin AI, Winston, Sapling,
  Pangram). Use when editing or reviewing any prose that needs to read as
  human-written: essays, exec memos, Confluence pages, Slack messages, release
  notes, customer comms, ghostwritten drafts, any AI-generated text that needs
  rewriting. Methodology rooted in the three signal layers detectors combine —
  token-level perplexity, sentence-level burstiness, and n-gram / lexical /
  structural fingerprints — with concrete counter-moves for each. For purely
  structural tells (label-colon bullets, emoji headings) use anti-slop instead;
  this skill owns the prose. Trigger on "humanise this", "passa no detector",
  "remove AI tells", "esse texto tá com cara de IA", "GPTZero" — full trigger
  list and related skills live in the skill body.
license: MIT
compatibility: claude-code opencode
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer

Remove signs of AI-generated writing from prose so it reads as human-written and passes production AI detectors (GPTZero, Copyleaks, Originality.ai, Turnitin AI, Winston, Sapling, Pangram).

The methodology is rooted in what these detectors actually compute, not vibes. Vocabulary cleanup alone fails — detectors operate on three signal layers and every layer must be unremarkable for the text to pass.

## Trigger phrases

Invoke on: "humanise this", "passa no detector", "remove AI tells", "make this sound human", "fix the AI tone", "GPTZero", "Copyleaks", "Originality", "esse texto tá com cara de IA", "tira o ar de ChatGPT", "detector de IA", "burstiness", "perplexity", "stylometry", "AI-written".

Typical material: essays, articles, blog posts, exec memos, Confluence pages, Slack messages, release notes, customer comms, LinkedIn posts, ghostwritten drafts, AI-generated text that needs rewriting.

## Related skills

Pairs with `anti-slop`, which owns the structural patterns (label-colon bullets, decorative emoji headings, follow-up spam); this skill owns the prose, and when text mixes prose and structure both apply. This skill is also the hard gate inside `humanize-deliverables` for outbound prose — the note at the end of the Pattern catalogue section has the details.

## Progressive loading

Load this `SKILL.md` first. For large or specialized tasks, use `references/progressive-loading.md` to choose the narrowest supporting reference before reading more.

## Your task

When given text to humanise:

1. **Run three sweeps in order** — Surface → Rhythm → Voice. Each catches what the others miss. Don't merge them.
2. **Self-audit against six axes** that mirror what detectors measure. Rewrite any axis that fails.
3. **Preserve meaning.** Keep substance, evidence, names, numbers, claims. Strip filler. A humanised draft that lost the recipient-actionable substance is worse than the AI original.
4. **Match the intended voice.** Formal exec memo, casual Slack, technical PR — different shapes. When a voice sample exists, match it. Otherwise default to the Personality and Soul section below.

## Detector mental model

Detectors are not single classifiers. They are ensembles of three signal layers. The text has to be unremarkable across all three to pass.

**Layer 1 — Token surprise (perplexity).** A reference language model scores how surprised it is by each next token. LLMs minimise surprise; their output sits in a narrow band. Human writing escapes the band routinely — regional idioms, specific concrete nouns, technical jargon, names, dates, numbers, contractions, deliberate roughness. A long run of low-surprise tokens is the strongest single AI signal.

**Layer 2 — Sentence variance (burstiness).** Standard deviation of per-sentence perplexity or length. Human writing alternates surprising and unsurprising sentences; AI output is metronomic. GPTZero made this famous; every detector now includes a variant.

**Layer 3 — Phrase and structural fingerprints.** Multi-word units that survive paraphrase ("in today's fast-paced world", "delve into", "stands as a testament", "play a crucial role"), plus structural tells (Rule of Three, label-colon bullets, discourse-marker openers, uniform paragraph length). This is the layer that catches drafts which scored clean on vocabulary alone, because the skeleton is the giveaway.

For the full mental model, per-tool weighting, and reference papers, load `references/detector-methodology.md`.

## Six-axis methodology

For every pass, address all six axes. Fixing one without the others leaves a detectable surface.

### Axis 1 — Token surprise (perplexity injection)

**Signal:** long run of tokens each highly likely given the prior context.

**Target:** one concrete, specific, or unexpected choice every 30-60 words. Real names, dates, numbers, regional terms, idioms, technical jargon used precisely.

**Counter-moves:**

- Replace generic nouns with specific ones. Not "tools" but "Copilot, Cursor, Cline". Not "developers" but "Mira at the fintech, Jake on the platform team".
- Replace generic verbs with specific ones. Not "leverage" but "use", "lean on", "wire in", "abuse".
- Use uncommon but accurate words when register allows. "Slippery" beats "complex" if the actual quality is slipperiness.
- Inject one anchor per paragraph: a number, a date, a name, a place, a quoted phrase.
- Kill adjective-noun pairs from the lexical blacklist ("comprehensive solution", "robust framework", "seamless experience"). These are training-data fossils.

### Axis 2 — Sentence-length variance (burstiness)

**Signal:** mean sentence length ~18-22 words, standard deviation ~4-6 words. Uniform.

**Target:** mean 14-20 words, standard deviation ≥ 8-10 words. At least one sub-7-word sentence per paragraph. At least one ≥ 25-word sentence per ~5 paragraphs.

**Counter-moves:**

- Add deliberate fragments. "Not always." "Worth it." "Depends."
- Combine two short, similarly-shaped AI sentences into one with a comma or "and".
- Split a long AI sentence at the natural breath into one long + one short.
- Vary sentence-opener types. Don't open three sentences in a row with subject-verb.

### Axis 3 — N-gram fingerprints

**Signal:** multi-word units that appear in AI output at 100-1000× the human rate. Survive paraphrase because detectors hash the skeleton, not the surface.

**Target:** zero appearances of the phrases in `references/n-gram-blacklist.md`. When you reach for one, rewrite around the idea, not around the phrase.

**Counter-moves:**

- Cut the phrase entirely if it was filler.
- Replace with a specific concrete substitute that says the same thing in your own words.
- Never paraphrase the skeleton ("navigate the landscape" → "traverse the landscape" still flags).

### Axis 4 — Lexical fingerprint

**Signal:** a list of ~150 words appears in AI output at 5-50× the human rate. Examples: delve, navigate, tapestry, embark, robust, leverage, ensure, foster, comprehensive, seamless, dynamic, intricate, vibrant, multifaceted, holistic, paradigm, pivotal, transformative, groundbreaking, enduring, testament, realm, journey, landscape, ecosystem.

**Target:** zero blacklisted words unless used with deliberate irony or genuine register fit.

**Counter-moves:**

- Search the draft against `references/n-gram-blacklist.md`.
- For each hit, ask: what specifically am I trying to say? Then write that.

### Axis 5 — Discourse markers

**Signal:** sentences opening with However / Moreover / Furthermore / Additionally / Indeed / Notably / Consequently at > ~5% of sentence opens. Humans use these closer to 1-2%.

**Target:** ≤ 1 formal opener per 10 sentences. Prefer informal connectors (but, and, so, still) or just start with the new point.

**Counter-moves:**

- Strip the marker. The logical connection often survives without it.
- Replace formal markers with informal ones.
- Don't add a marker between every paragraph; some transitions can be implicit.

### Axis 6 — Structural symmetry

**Signal:** Rule of Three (three parallel clauses or three-bullet lists), label-colon bullets, uniform paragraph length, parallel syntactic shapes across paragraphs.

**Target:** broken symmetry. Pairs over triplets. Mixed bullet shapes. Varied paragraph length.

**Counter-moves:**

- Convert a triplet to a pair, or a singleton with a "for instance" tail.
- Convert label-colon bullets to running prose, or to varied bullet shapes (no labels, plain dashes, mixed-length items).
- Make one paragraph dramatically shorter or longer than its neighbours.
- Don't repeat the same syntactic shape across consecutive paragraphs.

## Process — three sweeps

Run the sweeps in order. Each catches what the others miss. Merging them costs you detector axes.

### Sweep 1 — Surface (vocabulary + n-gram)

Run the draft against the lexical and phrase catalogues. Cut or replace every match. Kills ~80% of detector hits but leaves rhythm and voice untouched.

References to load: `references/n-gram-blacklist.md`, `references/patterns-14-29-style-and-filler.md`.

### Sweep 2 — Rhythm (burstiness + structure)

Read aloud, or in your head with intent to hear it. Mark every paragraph by sentence count and average length. Where the rhythm is metronomic, break it. Add fragments. Combine sentences. Vary openings. Break triplets. Vary paragraph length.

This is the sweep that defeats GPTZero. Vocabulary alone will not move its burstiness score.

References to load: `references/patterns-1-13-content-and-language.md` (Rule of Three, negative parallelism, copula avoidance especially).

### Sweep 3 — Voice (perplexity injection + personality)

The text is now clean and rhythmic but probably still feels assembled. Add an anchor per paragraph: a specific name, date, number, place, opinion, contradiction, side comment. Add one sentence that wouldn't survive a corporate edit — slightly too personal, slightly too informal, slightly too uncertain.

This is what raises sentence-level perplexity and gives the text a pulse.

References to load: PERSONALITY AND SOUL section below.

### After the sweeps — self-audit and final ask

Run the **Detector-aware self-audit**. Address any failing axis. Then re-ask: "What would still flag this to GPTZero / Copyleaks / Originality.ai?" Answer honestly in three bullets max. Address each.

## Detector-aware self-audit

Six-question checklist that mirrors what detectors compute. Score each axis pass / marginal / fail and rewrite where you fail. Vocabulary cleanup without this leaves obvious signal.

```
Axis 1 — Token surprise
  [ ] At least one concrete anchor per paragraph (name, date, number, place, quoted phrase)?
  [ ] Zero generic adjective-noun pairs from the lexical blacklist?

Axis 2 — Burstiness
  [ ] Sentence length varies — at least one < 7 words and one > 25 words per ~5 paragraphs?
  [ ] No three consecutive sentences with the same opener type?

Axis 3 — N-gram fingerprints
  [ ] Zero phrases from references/n-gram-blacklist.md?
  [ ] No skeleton paraphrase ("ranging from A to B" → "spanning from A to B" — still flags)?

Axis 4 — Lexical fingerprint
  [ ] Zero blacklisted words (delve, navigate, robust, comprehensive, ...) unless intentional?

Axis 5 — Discourse markers
  [ ] ≤ 1 formal opener per 10 sentences?

Axis 6 — Structural symmetry
  [ ] No Rule of Three pattern (three parallel clauses, three-bullet lists with parallel shape)?
  [ ] Paragraph lengths vary visibly?
  [ ] No label-colon bullets in prose contexts?
```

If three or more axes fail, the draft is still AI-shaped. Rewrite. If one or two fail, target those specifically. If all pass and the text still reads "smooth", you are missing personality — go back to the Soul section.

## Voice calibration (optional)

If the user provides a writing sample (their own previous writing), analyse it before rewriting:

1. **Read the sample first.** Note sentence length patterns, word choice level, paragraph openings, punctuation habits, recurring phrases or verbal tics, transition style.
2. **Match the sample.** Don't just remove AI patterns. Replace them with patterns from the sample. If the sample writes short sentences, don't produce long ones. If the sample uses "stuff" and "things", don't upgrade to "elements" and "components".
3. **No sample** — fall back to the default natural, varied, opinionated voice from the Personality and Soul section.

### How the user supplies a sample

- Inline: "Humanise this text. Here's a sample of my writing for voice matching: [sample]"
- File: "Humanise this text. Use my writing style from [file path] as a reference."

## Personality and Soul

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

### Signs of soulless writing (even if technically clean)

- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when fitting
- No humour, no edge, no personality
- Reads like a Wikipedia article or a press release

### How to add voice

**Have opinions.** Don't just report facts; react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary the rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person is honest, not unprofessional. "I keep coming back to..." or "Here's what gets me..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, half-formed thoughts are human.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

### Before (clean but soulless)

> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

### After (has a pulse)

> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle, but I keep thinking about those agents working through the night.

## Pattern catalogue

The 29 Wikipedia-derived patterns live in three references. The new methodology above sits on top of them; the patterns are still the concrete catch-list for specific tells.

| Audit lens | Reference |
|---|---|
| Content-shape and language/grammar tells: significance inflation, vague attributions, "-ing" tacks, copula avoidance, rule of three, synonym cycling, false ranges, passive voice (patterns 1-13) | `references/patterns-1-13-content-and-language.md` |
| Style, communication, filler tells: em dash overuse, boldface mechanics, inline-header lists, title case, emojis, curly quotes, chatbot artifacts, knowledge-cutoff hedges, sycophantic tone, filler phrases, excessive hedging, generic conclusions, hyphenated word pairs, authority tropes, signposting, fragmented headers (patterns 14-29) | `references/patterns-14-29-style-and-filler.md` |
| Detector technical reference: per-tool weighting, stylometric features that survive paraphrase, reference papers | `references/detector-methodology.md` |
| N-gram and lexical blacklist for Sweep 1 | `references/n-gram-blacklist.md` |

The `anti-slop` skill owns the *structural* twin of several of these patterns (label-colon bullets, decorative emoji headings, follow-up spam). When the text mixes prose and structure, both skills apply. For outbound prose to Confluence / Slack / Jira / customer / leadership, `humanize-deliverables` adds a hard sha256 gate on top of this skill — that is the publish-time enforcer.

## Output format

Provide:

1. Draft rewrite (after Sweeps 1-3).
2. "What would still flag this to GPTZero / Copyleaks / Originality.ai?" — three honest bullets max.
3. Final rewrite addressing those flags.
4. Optional: a brief summary of which axes were the worst offenders in the original.

## Full example

**Before (AI-sounding):**

> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools, nestled at the intersection of research and practice, are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> - **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
> - **Quality:** Output quality has been enhanced through improved training, contributing to higher standards.
> - **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies, the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you'd like me to expand on any section!

**Draft rewrite after Sweeps 1-3:**

> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, repetitive refactors. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped paying attention.
>
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior dev at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library.
>
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless. It means they are tools. They do not replace judgment, and they do not eliminate the need for tests.

**What would still flag this to GPTZero / Copyleaks / Originality.ai?**

- The rhythm is still a bit too tidy — clean contrasts, evenly paced paragraphs. GPTZero would see medium burstiness.
- The named people and study citations read like plausible-but-made-up placeholders unless they're real. Detectors don't catch fabricated anchors, but a human reader will, and the underlying smoothness still scores.
- The closer leans slogan-shaped ("They do not replace judgment...") rather than a person talking.

**Final rewrite:**

> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.

**Which axes were the worst offenders in the original:**

- Axis 4 (lexical): testament, transformative, pivotal, groundbreaking, vital, seamless, intricate, enduring, journey — every paragraph.
- Axis 3 (n-gram): "stands as a testament", "in today's rapidly evolving landscape", "at its core", "in order to", "in conclusion".
- Axis 6 (structure): triple copula-avoidance ("serves as / functions as / stands as"), Rule of Three throughout, label-colon bullets.
- Axis 5 (discourse): "Additionally", "Despite challenges".
- Axis 1 (perplexity): zero concrete anchors. Generic everything.
- Axis 2 (burstiness): every paragraph clusters at 30-50 words across 2-3 sentences of similar length.

## Reference

Methodology synthesises Wikipedia: Signs of AI writing (the foundation of the 29-pattern catalogue, maintained by WikiProject AI Cleanup), GPTZero's perplexity / burstiness disclosures, Copyleaks's n-gram + paraphrase-resistance claims, Originality.ai's per-model-family classifier docs, Turnitin AI's rhythm feature, and the academic literature on detection robustness (Sadasivan 2023, Chakraborty 2023, Mitchell 2023 DetectGPT, Pillutla 2021 MAUVE).

Key insight from Wikipedia, still true: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases." The methodology in this skill works because every counter-move pushes against that median.
