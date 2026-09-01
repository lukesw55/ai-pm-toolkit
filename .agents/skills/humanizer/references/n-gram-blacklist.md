# N-gram and lexical blacklist

Load this file during **Sweep 1 — Surface** of the humanisation process. These are the multi-word units and single words that production AI detectors (Copyleaks, Originality.ai, Pangram in particular) track as the strongest paraphrase-resistant signal.

## Why paraphrasing is not enough

The skeleton of a phrase survives synonym swap. `"navigate the complex landscape"` becomes `"traverse the complex landscape"` after a thesaurus pass, but the phrase fingerprint — verb + the + adjective + landscape/realm/ecosystem — still matches. Detectors hash the skeleton, not the surface.

**Rule:** when you catch yourself reaching for a blacklisted phrase, rewrite around the **idea**, not around the **phrase**. If you cannot say what the phrase was trying to say in your own words, the phrase was filler. Cut it.

---

## Phrase fingerprints (multi-word units to eliminate)

### Inflated openings and framings

- "In today's fast-paced world / landscape / environment / economy"
- "In the realm of"
- "In the world of"
- "In the ever-evolving landscape of"
- "At its core"
- "When it comes to"
- "It is important to note that"
- "It should be emphasized that"
- "It is worth mentioning that"
- "It goes without saying"
- "Needless to say"
- "First and foremost"
- "Last but not least"

### Significance inflation

- "Stands as a testament to"
- "Serves as a testament to"
- "Marks a pivotal moment"
- "Represents a paradigm shift"
- "Plays a crucial / pivotal / vital role"
- "Holds significant value"
- "Bears witness to"
- "A turning point in"
- "A milestone in"

### Vague attributions

- "Industry observers have noted"
- "Experts agree that"
- "Studies have shown that"
- "It has been argued that"
- "It is widely believed that"
- "Many would argue that"
- "Some have suggested that"

### Filler transitions and connectors

- "In order to" (use "to")
- "With regard to"
- "With respect to"
- "In light of the fact that" (use "because")
- "Due to the fact that" (use "because")
- "For the purpose of"
- "On the basis of"
- "In terms of"
- "As a matter of fact"
- "In conjunction with"
- "In addition to the above"

### Promotional verbs and metaphors

- "Delve into"
- "Embark on a journey"
- "Navigate the complex landscape of"
- "Unlock the potential of"
- "Harness the power of"
- "Foster a culture of"
- "Cultivate an environment of"
- "Empower X to Y"
- "Revolutionise the way we"
- "Transform the way we"
- "Shape the future of"
- "Pave the way for"
- "Set the stage for"
- "Push the boundaries of"
- "Bridge the gap between"

### Synonym-cycling triplets (Rule of Three with copula avoidance)

- "X serves as the catalyst, Y functions as the partner, Z stands as the foundation"
- "Robust, intuitive, and powerful"
- "Seamless, dynamic, and engaging"
- "Innovative, scalable, and reliable"
- "Comprehensive, transformative, and enduring"
- Any triplet of adjectives that could be reordered without loss of meaning.

### Hedging without commitment

- "Could potentially"
- "Might have some effect"
- "May or may not"
- "It could be argued that"
- "While specific details are limited"
- "Based on available information"
- "To some extent"
- "In some cases"
- "Up to a certain point"

### Generic conclusions

- "In conclusion"
- "To conclude"
- "To summarise"
- "In summary"
- "All in all"
- "At the end of the day"
- "The future looks bright"
- "Exciting times lie ahead"
- "The possibilities are endless"
- "Only time will tell"
- "It remains to be seen"

### Negative parallelism

- "It's not just about X; it's about Y"
- "This isn't simply A; it's B"
- "Not only X, but also Y" (when used decoratively)

### False ranges

- "From X to Y, from A to B"
- "Spanning from X to Y"
- "Ranging from X to Y" (when X and Y are picked for rhetorical sweep, not real extremes)

### Sycophantic openers and closers (chat artifacts)

- "Great question!"
- "What a thoughtful question"
- "I'd be happy to help"
- "Certainly!"
- "Of course!"
- "I hope this helps!"
- "Let me know if you'd like me to expand"
- "Feel free to ask if you have any further questions"

### Knowledge-cutoff hedges

- "While specific details may be limited based on my training"
- "I don't have access to real-time information"
- "As of my last update"
- "Based on my knowledge cutoff"

---

## Single-word lexical blacklist

These words appear in AI output at 5-50× their natural human rate. Replace each with a concrete equivalent or cut the sentence. Cases where the word is genuinely the right one and the register fits (a wedding speech can say "journey"; a PR cannot) are rare — when in doubt, replace.

### The high-signal set (Originality.ai's strongest single features)

- delve, delving
- navigate, navigating, navigation (when metaphorical)
- tapestry
- embark
- robust
- leverage (as a verb)
- ensure (when "make sure" would do)
- foster (when metaphorical)
- comprehensive
- seamless, seamlessly
- dynamic (as a vague positive)
- intricate
- vibrant (as a vague positive)
- multifaceted
- holistic
- paradigm
- pivotal
- transformative
- groundbreaking
- enduring (when vague)
- testament
- realm
- journey (when metaphorical)
- landscape (when metaphorical)
- ecosystem (when metaphorical and not literal)
- framework (when used as a vague positive)
- meticulous, meticulously
- crucial (often overused)

### The mid-signal set (frequent but not always wrong)

- nuanced
- intricate
- profound
- elevate, elevated
- empower, empowering
- unlock, unlocked
- streamline, streamlined
- optimise, optimised (when vague)
- harness
- cultivate
- showcase (as verb)
- underscore, underscoring
- highlight, highlighting (when superficial)
- illuminate, illuminating
- demonstrate, demonstrating (often replaceable with "show")
- facilitate
- utilise (use "use")
- vital (often overused)
- essential (often overused)
- significant, significantly (often vague)
- substantial, substantially
- crucial
- noteworthy
- remarkable

### Discourse-marker openers (cap at ≤ 1 per 10 sentences)

When opening a sentence with one of these, ask whether the connection survives without it. Usually yes.

- However
- Moreover
- Furthermore
- Additionally
- Indeed
- Notably
- Consequently
- Thus
- Therefore
- Nevertheless
- Nonetheless
- Subsequently
- Accordingly

Informal swaps that read more human: but, and, so, still, anyway.

---

## Boilerplate structural patterns

### Label-colon bullets

```
- **Speed:** Code generation is significantly faster.
- **Quality:** Output has been enhanced.
- **Adoption:** Usage continues to grow.
```

This shape almost never appears in spontaneous human writing. Detectors flag it on sight. Convert to running prose, or use plain dashes with mixed-length items.

### Triple-adjective stacks

```
"... a comprehensive, intuitive, and powerful solution."
```

Cut to one specific adjective, or drop all three.

### "Not just X, but Y" closer

```
"It's not just about autocomplete; it's about unlocking creativity at scale."
```

A near-universal AI-tell. Rewrite as a direct statement.

---

## How to use this list

1. **During Sweep 1**, search the draft for every entry. Cut or replace.
2. **Do not paraphrase the skeleton.** "Navigate the landscape" → "traverse the landscape" still flags. Rewrite the underlying idea.
3. **Keep a workspace blacklist.** When you spot a new high-signal phrase in your own output, add it to this file.
4. **Treat lexical hits as a smell, not always a fix.** Some uses are genuinely correct. The right test is: would a reader notice if I cut the word? If no, cut it.
