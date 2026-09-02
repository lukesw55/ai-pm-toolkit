# Humanizer

Rewrites AI-sounding prose so it reads like the writer, without changing what it says. The method and the pattern catalogue come from [blader/humanizer](https://github.com/blader/humanizer) (Wikipedia's "Signs of AI writing", 35 patterns at the pinned version); this repo reorganises that single file for progressive loading and adds a thin overlay that wires it to `anti-slop`, the publish gate, and `inference-discipline`. It runs on Claude Code and Codex alike through the repo's generated mirrors.

## Files

| File | Role |
|---|---|
| `SKILL.md` | Method: what to do, voice matching, personality, false positives, how to return the result, rewrite process. Frontmatter carries the upstream pin. |
| `references/patterns-1-13-content-and-language.md` | Patterns 1–13, upstream text verbatim plus one `Toolkit note:` |
| `references/patterns-14-35-style-and-filler.md` | Patterns 14–35, upstream text verbatim plus four `Toolkit note:` lines |
| `references/n-gram-blacklist.md` | Toolkit vocabulary supplement to §7 and §23 (fork-original) |
| `references/progressive-loading.md` | Which file to open for which text |
| `evals/evals.json` | Three evals; graded by `scripts/grade_evals.py` |
| `LICENSE` | Upstream MIT license, byte-identical |

## Lineage

- Upstream: [blader/humanizer](https://github.com/blader/humanizer), by Siqi Chen, MIT.
- Pinned version: 2.11.2, commit `e2e92e7b4b8229253ed5c8e81dc65463fdeddda5` (2026-08-18), the upstream `main` at sync time (2026-09-02). The pin is machine-readable in `SKILL.md` frontmatter (`metadata.version`, `metadata.upstream-commit`, `metadata.synced`).
- Previous base in this repo: upstream 2.5.1 (`8b3a178`, patterns 1–29) plus a fork-original layer versioned 3.0.0 (detector mental model, six axes, three sweeps, a detector methodology reference). That layer was replaced by this re-sync: the toolkit keeps only the adaptations the hybrid setup needs, and upstream is the core.
- Upstream is append-only on pattern numbers: 1–29 keep their numbers forever, 30 arrived in 2.7.0, 31–33 in 2.8.0, 34–35 in 2.10.0; titles were rewritten in plain language in 2.11.0. Cross-references by `§number` elsewhere in this repo therefore stay valid across upstream releases.

## Provenance by layer

Three layers, each reconstructible on the next re-sync:

| Where | Layer | Source or rule |
|---|---|---|
| `SKILL.md` title and intro, What to do, Match the writer's voice, Add personality only when it fits, Check for false positives, How to return the result, Rewrite process, Source | upstream 2.11.2 | upstream `SKILL.md` lines 13–17, 19–28, 30–38, 40–46, 393–428, 432–438, 440–450, 452–456 |
| `references/patterns-1-13-content-and-language.md` body | upstream 2.11.2 | upstream `SKILL.md` lines 48–177 |
| `references/patterns-14-35-style-and-filler.md` body | upstream 2.11.2 | upstream `SKILL.md` lines 179–391 |
| `LICENSE` | upstream 2.11.2 | byte-identical |
| The split of one upstream file into `SKILL.md` + two pattern references; the two-line header at the top of each pattern reference; the Pattern catalogue table and section order in `SKILL.md`; `references/progressive-loading.md` | structural | reorganisation for progressive loading, no normative change |
| `SKILL.md` frontmatter `description` (repo style, no harness names) and `metadata` (pin); sections Trigger phrases, Related skills, Progressive loading | toolkit overlay | wholly local sections, listed here |
| `Toolkit note:` lines: one after §10, four after §14, §16, §18, §22, one inside How to return the result | toolkit overlay | inline insertions inside upstream blocks |
| `references/n-gram-blacklist.md` | toolkit overlay | fork-original vocabulary supplement; kept because eval 1 asserts the removal of words absent from upstream §7 |
| `evals/evals.json` | toolkit overlay | local behavioural contract for the upstream method and toolkit integration |
| `README.md` (this file) | toolkit overlay | local |

Convention: upstream content carries no inline marking. A local insertion inside an upstream block starts with `Toolkit note:`. Wholly local sections and files are identified in this table. `grep -c '^Toolkit note:'` over the skill (line-anchored, so the reference headers and this paragraph, which only name the convention, do not count) reconstructs only the inline share of the overlay; this table is the source of truth for the complete overlay, and `diff` against the pinned upstream snapshot reconstructs the upstream and structural layers.

Removed from the fork on this re-sync, by rule (keep only adaptations the hybrid toolkit needs): the detector mental model, the six-axis methodology, the three sweeps, the inline voice-calibration and personality sections (upstream's own sections replace them), the full example, the detector methodology reference, and the frontmatter keys `compatibility` and `allowed-tools` (upstream removed them in 2.9.1).

## Re-sync procedure

1. Clone upstream at the new tag and note the commit.
2. Diff upstream `SKILL.md` against the previous pinned commit; read the changelog for new pattern numbers (append-only) and title changes.
3. Replace the upstream layer: the eight `SKILL.md` sections and the two pattern-reference bodies, using the new line spans; re-add the `Toolkit note:` lines at the same patterns; regenerate the Pattern catalogue table and `progressive-loading.md` if the split points moved.
4. Update the `metadata` pin (`version`, `upstream-commit`, `synced`), this table's line spans, and any `§` title parentheticals in `anti-slop`'s catalogues.
5. Run `python3 scripts/sync_skills.py`, then the repo battery (`docs/REPO_HEALTH.md`); the humanizer evals and their grader fixtures are the behavioural check.

## Evals

`evals/evals.json` holds three standard evals: an exec-memo rewrite that must drop stock words (`fast-paced`, `leverage`, `crucial`) while keeping the memo's substance; a technical PRD excerpt whose metrics, dates, and constraints must survive; and an attributive-hyphen case (`cross-functional team` stays hyphenated, `the roadmap is high-quality` loses its hyphen) that separates upstream's §26 rule from the old fork's "drop hyphens on common pairs". Assertions live in `scripts/grade_evals.py`; deterministic fixtures in `scripts/test_grade_evals.py`.

## License

MIT, upstream's license kept verbatim in `LICENSE`. The repo's root `LICENSE` covers the toolkit; the root README's License section points here.
