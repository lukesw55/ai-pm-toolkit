# Detector methodology — what real AI detectors actually measure

Load this file when you need to understand WHY a specific humanisation axis matters, or when you are debugging a draft that "feels clean" but still gets flagged.

This is a working model of how production detectors score text, derived from their public technical disclosures, papers, and reverse-engineering writeups. It is not a black box description for any single product — it is a synthesis of the signal layers that GPTZero, Copyleaks, Originality.ai, Turnitin AI, Winston AI, Sapling, and Pangram all combine.

## Table of contents

1. The three-layer detection stack
2. Per-tool focus
3. Stylometric features that survive paraphrase
4. Why "humanising" by vocabulary swap fails
5. Reference papers and disclosures

---

## 1. The three-layer detection stack

Production detectors are not single classifiers. They are ensembles. A draft has to be unremarkable across all three layers to score below the AI-likely threshold.

### Layer 1 — Token-level statistics (perplexity)

A reference language model (often a frozen GPT-2 / GPT-Neo or a fine-tuned probe) scores each token's surprise given the prior context. The aggregate per-text perplexity number is the headline feature.

LLMs minimise perplexity at generation time by design. Their output sits inside a narrow band of "next tokens the reference model also expected". Human writing escapes that band routinely: regional idioms, specific concrete nouns, technical jargon used precisely, deliberate roughness, contractions, dialect, swearing, names, dates, numbers.

A text whose mean per-token perplexity stays below the human floor for 100+ tokens in a row is the strongest single AI signal. This is why detectors flag short texts unreliably — there's not enough run length.

**What raises perplexity (human-like):**

- Specific concrete nouns ("the Ryzen 7840U", "Mira at the fintech") over generic ones ("a processor", "a developer").
- Real numbers and dates over hedged ones ("47.3%", "2026-05-08" over "roughly half", "recently").
- Idioms and regionalisms that the LLM training set under-represents.
- Technical jargon used precisely, not decoratively.
- Contractions, slang, mild profanity, where register allows.
- Deliberate sentence-shape roughness — a sub-five-word fragment, a run-on, a parenthetical aside.

**What lowers perplexity (AI-like):**

- Generic adjective-noun pairs ("comprehensive solution", "robust framework", "seamless experience"). These are LLM training-data fossils.
- Filler that adds no information ("It is important to note that", "In today's fast-paced world").
- Hedging that says nothing ("could potentially", "may have some effect").
- The list of ~150 "AI words" detectors track (see lexical fingerprint).

### Layer 2 — Sentence-level variance (burstiness)

Burstiness is the standard deviation of per-sentence perplexity (or, in cheaper detectors, of sentence length). Human writing alternates surprising and unsurprising sentences; AI output is metronomic.

GPTZero made burstiness famous, but every detector now includes some variant — Copyleaks measures "stylistic uniformity", Originality.ai weighs sentence-level consistency, Turnitin AI computes a "rhythm" feature.

**Target burstiness profile (sentence length):**

- Mean: 14-20 words per sentence (your domain may shift this).
- Standard deviation: ≥ 8-10 words.
- At least one sub-7-word sentence per paragraph.
- At least one ≥ 25-word sentence per ~5 paragraphs.

**Counter-moves:**

- Add deliberate fragments. "Not always." "Worth it." "Depends."
- Combine two short, similarly-shaped AI sentences into one with a comma or "and".
- Split a long AI sentence at the natural breath into one long + one short.
- Vary sentence-opener types. Don't open three sentences in a row with subject-verb.

### Layer 3 — N-gram and stylistic fingerprints

This is the layer that survives paraphrase, which is why this layer is the most dangerous.

Detectors maintain large multi-word-unit lists ("phrase fingerprints") that show up at 100-1000× their human rate. "In today's fast-paced world", "delve into", "ranging from X to Y", "play a crucial role", "stands as a testament", "in the realm of", "navigate the complex landscape". These survive synonym swaps because the skeleton — the syntactic shape and the supporting function words — stays intact.

They also measure structural fingerprints:

- **Rule-of-Three frequency.** Three parallel clauses, three parallel bullets. Humans use triplets too, but at a much lower rate.
- **Label-colon bullets.** `**Speed:** ...` `**Quality:** ...` `**Adoption:** ...`. Almost never appears in spontaneous human writing.
- **Discourse-marker openers.** Sentences opening with However / Moreover / Furthermore / Additionally / Indeed / Notably / Consequently. AI rate: ~5-8% of sentence opens. Human rate: ~1-2%.
- **Uniform paragraph length.** AI paragraphs cluster at 3-5 sentences each. Human paragraphs vary visibly.
- **Adjective-stacking.** "Comprehensive, intuitive, and powerful" style triplets.

A draft that scores clean on perplexity and burstiness can still flag on this layer because the structure is the giveaway.

---

## 2. Per-tool focus

Detectors all use the three-layer stack but weight them differently. Knowing the bias of the tool you're trying to beat helps you allocate effort.

### GPTZero

Headline features: perplexity + burstiness. Marketed those terms; they shaped the field.

What it weights heavily: sentence-length variance, sentence-level perplexity variance, opening burstiness ("the first 100 words").

What it weights less: phrase fingerprints, lexical blacklist.

**Implication:** Burstiness is the single biggest lever against GPTZero. A draft with perfect vocabulary but metronomic sentence rhythm still flags.

### Copyleaks

Multi-layered: their public docs emphasise n-gram patterns, paraphrase resistance, and a neural classifier trained across many model families.

What it weights heavily: n-gram fingerprints (phrase skeletons), paraphrase-resistant features.

What it weights less: short-text perplexity (their model handles short text by leaning on phrase fingerprints).

**Implication:** N-gram blacklist work is the biggest lever against Copyleaks. Vocabulary swaps that keep the phrase skeleton still flag — "navigate the complex landscape" → "traverse the complex landscape" is still caught.

### Originality.ai

Neural classifier first, trained per-model-family (GPT-3.5, GPT-4, Claude, Llama). Sentence-level scoring with a heavy lexical blacklist.

What it weights heavily: AI vocabulary words (delve, navigate, robust, comprehensive, ...), sentence-level perplexity, discourse markers.

What it weights less: paragraph-level structure.

**Implication:** Lexical fingerprint work is the biggest lever against Originality.ai. Their classifier reacts strongly to a handful of high-signal words.

### Turnitin AI / Winston / Sapling / Pangram

Variations on the same three-layer stack. Turnitin emphasises perplexity + sentence rhythm. Winston aggregates many small signals. Sapling uses a neural classifier with sentence-level breakdowns. Pangram benchmarks itself as the most robust against paraphrase — which suggests heavy n-gram fingerprinting + structural features.

**Implication for a universal pass:** if you tune for GPTZero burstiness + Copyleaks n-gram + Originality lexical, you cover the major surface.

---

## 3. Stylometric features that survive paraphrase

These are the features detectors compute regardless of vocabulary. A vocabulary-only humanisation pass leaves them unchanged. Address each:

| Feature                          | AI default                                              | Human target                                                    |
|----------------------------------|---------------------------------------------------------|-----------------------------------------------------------------|
| Mean sentence length             | 18-22 words                                             | 14-20 words                                                     |
| Sentence length stddev           | 4-6 words                                               | 8-10+ words                                                     |
| Type-token ratio (lexical div.)  | low (vocabulary loops)                                  | higher; rare words appear                                       |
| Function-word distribution       | smooth, evenly distributed                              | uneven; preferences show                                        |
| Punctuation rates (commas/sent.) | high and uniform                                        | varies                                                          |
| Em-dash density                  | high (clustered)                                        | low; isolated                                                   |
| Semicolon rate                   | very low                                                | sometimes present                                               |
| Passive-voice rate               | high (15-20% of sentences)                              | lower (5-10%)                                                   |
| Hedging-vocabulary rate          | high ("could", "might", "may", "potentially")           | lower; humans commit more                                       |
| Discourse-marker opener rate     | 5-8% of sentences                                       | 1-2%                                                            |
| Paragraph length stddev          | low                                                     | high                                                            |
| Adjective-stacking rate          | high (3+ adjective sequences)                           | low                                                             |
| First-person pronouns            | suppressed (third-person, neutral)                      | when fitting, "I"/"we" used                                     |
| Contractions                     | suppressed                                              | used when register allows                                       |
| Concrete-anchor density          | low (1 per ~200 words)                                  | higher (1 per ~30-60 words): names, dates, numbers, places      |

---

## 4. Why "humanising" by vocabulary swap fails

The common humaniser pattern — swap "leverage" for "use", "delve" for "explore", "robust" for "strong" — fixes Originality.ai's lexical pass but leaves GPTZero's burstiness pass and Copyleaks's n-gram pass intact. The text still flags.

This is why the methodology insists on three sweeps:

- **Sweep 1 — Surface (vocabulary + n-gram).** Kills the most obvious 80% of detector hits. Necessary but not sufficient.
- **Sweep 2 — Rhythm (burstiness + structure).** Defeats GPTZero. The text must hear unevenly.
- **Sweep 3 — Voice (perplexity injection + personality).** Defeats classifier-style detectors that score sentence-level perplexity. Concrete anchors per paragraph; one sentence per draft that would not survive a corporate edit.

Skipping any sweep leaves a detector surface. The text has to be unremarkable on all three layers.

---

## 5. Reference papers and disclosures

The methodology here synthesises:

- Tian, E. "GPTZero — burstiness and perplexity" (public blog and academic presentations, 2023).
- Copyleaks AI Content Detector technical FAQ — n-gram pattern detection and paraphrase resistance claims.
- Originality.ai model-family-aware classifier documentation and per-model evaluation reports.
- Sadasivan, V. et al. "Can AI-Generated Text be Reliably Detected?" (arXiv 2303.11156, 2023) — discusses paraphrase robustness, perplexity limits, and watermarking.
- Chakraborty, S. et al. "On the Possibilities of AI-Generated Text Detection" (arXiv 2304.04736, 2023) — theoretical bounds.
- Mitchell, E. et al. "DetectGPT" (arXiv 2301.11305, 2023) — local curvature in log-probability space.
- Pillutla, K. et al. MAUVE (NeurIPS 2021) — gap measurement between machine and human text distributions.
- Wikipedia: Signs of AI writing (the foundation of the pattern catalogue in this skill).

The detector market evolves quickly. Treat per-tool weighting above as a working approximation; the three-layer stack itself has been stable across all major tools since 2023.
