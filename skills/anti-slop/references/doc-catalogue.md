# Documentation slop catalogue (B1–B12)

Load when writing or reviewing markdown docs, READMEs, PR descriptions, ADRs, tickets, changelogs, or migration notes. The 12 patterns below are the most common shapes of "doc that looks complete because it has the expected sections, but adds no real signal."

The `humanizer` skill covers parallel patterns for prose-heavy text. When a doc mixes structure (headings, bullets) with prose, run this catalogue for the structure and `humanizer` for the prose; the rules complement each other rather than overlap.

## B1. Template sections

Slop:

```markdown
## Overview
## Details
## Conclusion
```

Fix with load-bearing sections:

```markdown
## What changed
## Why it changed
## Risk
## Rollback
```

Rule: a heading should say something specific about this artifact.

## B2. README that repeats the repo name

Slop:

```markdown
# auth-service

This service handles authentication.
```

Fix:

```markdown
# auth-service

OIDC issuer (e.g. Keycloak/Auth0). Validates client JWTs and issues short-lived API tokens.
```

Rule: start with what `ls`, the repo name, and the folder name cannot tell you.

## B3. Label-colon bullets

Slop:

```markdown
- **Speed:** faster page loads
- **Reliability:** fewer errors
- **Cost:** lower bills
```

Fix:

```markdown
- p95 page load dropped from 1.8s to 600ms
- 500 rate fell from 0.3% to 0.05%
- egress is down about $400/month
```

Rule: replace categories with evidence. Pairs with `humanizer` pattern §16 (lists with bold mini-headings) for prose contexts. The Stop hook `scope-bloat-gate.sh` flags runs of 4+ consecutive label-colon bullets in replies.

## B4. Forced symmetry

Slop: three pros, three cons, three risks, three next steps when only two are real.

Fix: keep the real count.

Rule: reality is usually uneven. Pairs with `humanizer` pattern §10 (forced groups of three) in prose contexts.

## B5. Static metadata nobody maintains

Slop:

```markdown
Status: Active
Last updated: 2026-05-08
Owner: TBD
```

Fix: delete unless a process keeps it accurate.

## B6. Decorative emoji

Slop:

```markdown
## 🚀 Launch
## ✅ Next steps
```

Fix:

```markdown
## Launch
## Next steps
```

Rule: use emoji only when the surrounding project already uses it. Note: decorative emoji at the start of a new markdown heading is hard-blocked by `hooks/anti-slop-gate.sh` (a small whitelist covers domain emoji that are part of the project's existing convention). Pairs with `humanizer` pattern §18 (emojis) in prose.

## B7. Table of contents on short docs

Slop:

```markdown
# Auth migration plan

## Table of contents
- Background
- Approach
- Risks

## Background
A few sentences.

## Approach
Two paragraphs.

## Risks
Three bullets.
```

Fix: delete the TOC. The doc is one screen long and the headings act as their own index.

Rule: TOCs earn their place around 300-400 lines of doc, or in artefacts that ship as standalone reference (specs, runbooks). For PRDs, design docs, ADRs, plans under that length, a TOC is decoration that the writer maintains and the reader skips.

## B8. Glossary for terms the audience knows

Slop:

```markdown
## Glossary
- **API:** Application Programming Interface. How one system calls another.
- **SLA:** Service Level Agreement. A commitment to an availability or latency target.
- **PR:** Pull request. A change proposal in ...
```

Fix: delete unless the doc will be read by an audience that genuinely does not know these terms. For internal docs read by the team that lives this vocabulary daily, the glossary is condescension.

Rule: glossaries earn their place in onboarding docs, external customer docs, and docs that cross a real audience boundary (engineering → legal, product → customer). Inside the team, define terms inline the first time they appear, only if non-obvious.

## B9. "Prerequisites" / "Assumptions" sections listing the obvious

Slop:

```markdown
## Prerequisites
- You have access to the repo.
- You have Docker installed.
- You know basic Git.
- You have read access to the staging environment.
```

Fix: delete the obvious entries. Keep only the non-obvious ones (specific permissions, specific tool versions, account setups the reader cannot guess).

Rule: prerequisites earn their place when getting them wrong silently breaks the procedure. "You have access to the repo" is not that.

## B10. PR template N/A rows

Slop:

```markdown
## Type of change
- [x] Bug fix

## Test plan
- [x] Unit tests

## Linked issues
- N/A

## Breaking changes
- N/A

## Migration notes
- N/A

## Screenshots
- N/A

## Reviewers
- N/A
```

Fix: keep only the rows that carry information for this PR. Delete the rest. If the team's PR template is so rigid that empty rows must stay, that is a process problem to raise — not a content problem to fill with placeholder text.

Rule: an empty template field signals "the template demands a section here but this PR doesn't need it". A reader is forced to scan past the noise. The fix is fewer fields, not more `N/A`.

## B11. Version history tables inside the doc

Slop:

```markdown
## Version history

| Version | Date       | Author | Changes               |
|---------|------------|--------|-----------------------|
| 1.0     | 2025-11-02 | Mira   | Initial draft         |
| 1.1     | 2025-11-15 | Mira   | Added section 3       |
| 1.2     | 2025-12-08 | Jake   | Reorganised section 2 |
```

Fix: delete. Confluence, Notion, Google Docs, and Git all track version history natively. The table inside the doc is duplicated state that decays the moment someone forgets to update it.

Rule: version history tables earn their place only when the doc lives in a system that does not track revisions, or when the audience must understand *why* a change happened beyond the diff (rare for working docs, occasional for shipped standards).

## B12. "About this document" meta-sections

Slop:

```markdown
## About this document

This document describes the proposed architecture for the new auth service.
It is intended for engineers, product managers, and team leads. It should be
read before the implementation kicks off. Updates to this document should
be discussed in #auth-channel.
```

Fix: delete. The title says what the document is. The audience reveals itself by who reads it. The discussion-channel rule belongs in the channel topic or the team handbook, not in every doc that touches the area.

Rule: meta-sections about the document itself almost never pay rent. The reader landed on the page; they know what it is. Spend the opening on the actual substance.
