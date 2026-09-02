# Humanizer progressive loading map

Load `SKILL.md` first: it carries the method (what to do, voice matching, false positives, how to return the result, rewrite process). The pattern catalogue lives in the two references below and is loaded only when the text needs it.

| File | Purpose | Load when |
|---|---|---|
| `references/patterns-1-13-content-and-language.md` | Patterns 1–13: inflated claims, name-dropping, -ing analysis, sales language, vague sources, stock challenge sections, overused AI words, avoiding is/are, not X but Y, forced groups of three, synonym cycling, false ranges, passive voice | The text has prose paragraphs whose content or grammar reads inflated, vague, or evasive |
| `references/patterns-14-35-style-and-filler.md` | Patterns 14–35: dashes, bold, bold mini-heading lists, title case, emojis, curly quotes, chatbot leftovers, knowledge-limit disclaimers, agreeable tone, filler, qualifiers, generic endings, hyphenated pairs, fake depth, announcements, repeated headings, previous-version talk, dramatic fragments, sayings, fake-candid openings, unraised objections, fake alternatives | The content reads fine but the surface still feels assembled by a model |
| `references/n-gram-blacklist.md` | Vocabulary supplement to §7 (overused AI words) and §23 (filler): multi-word units and single words that recur in AI output far above human rates | A sweep for stock phrasing, especially in memos and marketing-adjacent prose |
| `references/progressive-loading.md` | This map | Choosing which humanizer file to open |
