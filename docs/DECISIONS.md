# Toolkit decisions

These decisions govern the toolkit. Their sources are the integrated PRs linked
below and the current execution request. They do not describe a customer project.

| Decision | Rationale and consequence | Source |
|---|---|---|
| Canonical skills plus generated, committed mirrors | Edit `skills/`; synchronize both harness mirrors with `scripts/sync_skills.py`. Hooks remain canonical under `hooks/`. | [PR #1](https://github.com/lukesw55/ai-pm-toolkit/pull/1) |
| Calibrated disagreement | Challenge weak premises, accept sound evidence and test both behaviors. Do not reward automatic agreement or automatic opposition. | [PR #7](https://github.com/lukesw55/ai-pm-toolkit/pull/7) |
| Four eval categories and manifest/grader parity | Every skill has at least three evals, one adversarial case; doctrine skills also require a negative control. Counts are measurements, not targets. | [PR #7](https://github.com/lukesw55/ai-pm-toolkit/pull/7) |
| Storyline first, rendering optional | Markdown is the shared deck deliverable; a renderer is a separate harness capability. | [PR #4](https://github.com/lukesw55/ai-pm-toolkit/pull/4) |
| Pinned upstream with documented overlays | Humanizer content lineage is auditable; local changes are distinguished from upstream material. | [PR #6](https://github.com/lukesw55/ai-pm-toolkit/pull/6) |
| Lossless memory archival before warm rewrites | Verify archive content before replacing warm state; PII paths are excluded. Atomic replacement does not promise post-replace rollback. | [PR #9](https://github.com/lukesw55/ai-pm-toolkit/pull/9) |
| Soft session-close reminder | A reminder never becomes a blocking gate; lifecycle writes are not equivalent to logging work. | [PR #10](https://github.com/lukesw55/ai-pm-toolkit/pull/10) |
| Copilot agents inherit the model | Canonical tool allowlists are repository policy; stricter policy must not be attributed to the provider schema. | [PR #14](https://github.com/lukesw55/ai-pm-toolkit/pull/14) |
| Configurable prioritization dimensions | Business impact and strategic/risk dimensions use contextual anchors; Abrangência and its explicit exception remain shared rules. | [PR #13](https://github.com/lukesw55/ai-pm-toolkit/pull/13), [PR #15](https://github.com/lukesw55/ai-pm-toolkit/pull/15) |
| Neutral current examples | Use fictional document-collaboration examples without employer or sector associations. Preserve Git history unless separately authorized. | [PR #18](https://github.com/lukesw55/ai-pm-toolkit/pull/18) |
| Python 3.10 minimum | Enforce the advertised floor rather than expanding support to 3.9 without demand. Test 3.10 and 3.11 behind a stable validate check. | Remaining-backlog execution, authorized 2026-09-10 |
| Context files belong to a project | Initialize app/design/tasks per slug. Explicit migration copies only missing destinations and retains legacy sources. | Remaining-backlog execution, authorized 2026-09-10 |
| Real evals require provenance and isolated baselines | Synthetic fixtures validate assertions; only actual isolated harness runs support effectiveness claims. An unavailable pilot stays pending. | Remaining-backlog execution, authorized 2026-09-10 |
| Shared org layer, project memory stays per slug | Personas as archetypes, competitors as organisations and cycle goals live once under `.ai/memory/org/`, read on demand by every skill and never injected by hooks. The toolkit ships templates and `init_context.py --org`; upstream keeps the layer ignored and a fork versions its real content; `people/` and `raw-evidence/` stay PII and untracked; `org` is a reserved slug; no standing refresh ritual. | References batch, authorized 2026-09-10 |
| Archetype references only when a real need appears | The four lenses stay compositional. `pm-archetype-ai` carries `skills/pm-archetype-ai/references/eval-design.md` because PM-owned eval design had no home in any phase skill; the other three stay single-file until they show the same need. | References batch, authorized 2026-09-10 |
| Eval design is a PM-owned method | A scenario sheet, four hazards, four numeric limits, a golden set with a real failure and a block rule above the pass rate come before any extra scoring dimension; synthetic rows are practice and real traces decide. Adapted from Dean Peters in original text with the licence stated. | References batch, authorized 2026-09-10 |
| Review panel never blocks and never manufactures | A lens returns an objection with its evidence gap and owner, or no objection; a manufactured objection is a calibrated-disagreement failure. Companion to the shadow gate at stages 4 and 6; formal gates unchanged. | References batch, authorized 2026-09-10 |
| Human labels are tracked and bound to the run | Verdicts live in `docs/benchmarks/<iteration>/labels.jsonl`, appended only. A label names the run (iteration, skill, eval id, configuration), binds to the output hash and carries the rubric version; a correction is a new record with `--supersede` that keeps the history. A tie between labelers is a split awaiting resolution, never the worse verdict. The grader reports human and grader disagreement separately; above the threshold set before the run (0.10 default) it flags the grader for investigation, and drift is claimed only against the previous iteration. The pilot itself runs on the owner's machine with both CLIs authenticated. | References batch, authorized 2026-09-10; revised after the PR #21 review |

Record toolkit changes with `python3 scripts/memory.py log repo "<change and validation>"`.
Project work is logged under the relevant slug. Review corrections use additive
commits; do not rewrite a head someone has already reviewed. An author's own
validation is not independent approval.
