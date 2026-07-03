#!/usr/bin/env python3
"""
stage_context.py — Surface the current workflow stage to Claude Code.

Called by the UserPromptSubmit hook in .claude/settings.json. Reads
`.ai/memory/active-context.md` for the "Current stage" field and writes a short
context block to stdout. Claude Code injects stdout from this hook into the
conversation before the user prompt is processed, so every turn starts
stage-aware.

Safe to remove: if the hook or this script is missing, skills still work.
"""

import re
import sys
from pathlib import Path

STAGES = [
    "discovery-prioritization",
    "impact-brief",
    "discovery",
    "one-pager",
    "product-prioritization",
    "prd",
    "tech-kickoff",
    "delivery",
]

STAGE_TO_SKILL = {
    "discovery-prioritization": "pm-phase-define (prioritisation-frameworks.md, opportunity-level)",
    "impact-brief": "pm-phase-discover (impact-brief.md)",
    "discovery": "pm-phase-discover",
    "one-pager": "pm-phase-define (one-pager.md)",
    "product-prioritization": "pm-phase-define (prioritisation-frameworks.md, build-level)",
    "prd": "pm-phase-develop (prd-writing.md + prototype loop)",
    "tech-kickoff": "pm-phase-develop (tech-team-kickoff.md)",
    "delivery": "pm-phase-deliver (launch-readiness.md + release-notes.md + post-launch-monitoring.md)",
}

# Legacy slugs that map onto a canonical stage above.
STAGE_ALIASES = {
    "discover": "discovery",
}

# Human-readable "Stage" labels in WORKFLOW.md mapped to canonical slugs.
LABEL_TO_SLUG = {
    "discovery prioritization": "discovery-prioritization",
    "impact brief (gtm)": "impact-brief",
    "discovery": "discovery",
    "one pager": "one-pager",
    "product prioritization": "product-prioritization",
    "prd + prototype + refinement": "prd",
    "tech team kickoff": "tech-kickoff",
    "delivery": "delivery",
}


def load_stage_contract(workflow_path: Path) -> dict[str, dict[str, str]]:
    """Parse the "Stage -> Skill -> Artefact map" table in WORKFLOW.md.

    Returns {slug: {pm, reference, artefact, gate}}. WORKFLOW.md is the
    single source of truth; this avoids a second hand-maintained mapping that
    would drift. Returns {} on any problem so the caller falls back to
    STAGE_TO_SKILL.
    """
    try:
        text = workflow_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    contract: dict[str, dict[str, str]] = {}
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break  # table ended
            continue
        cells = [c.replace("`", "").strip() for c in stripped.strip("|").split("|")]
        if not in_table:
            lowered = [c.lower() for c in cells]
            if "stage" in lowered and "pm skill" in lowered:
                in_table = True
            continue
        if set("".join(cells)) <= {"-"}:
            continue  # |---|---| separator row
        if len(cells) < 6:
            continue
        _num, stage_label, pm, reference, artefact, gate = cells[:6]
        slug = LABEL_TO_SLUG.get(stage_label.lower())
        if not slug:
            continue
        contract[slug] = {
            "pm": pm,
            "reference": reference,
            "artefact": artefact,
            "gate": gate,
        }
    return contract


def build_stage_block(stage: str, contract: dict[str, dict[str, str]]) -> list[str]:
    """ICM-style stage contract (Inputs / Process / Output-gate), or a fallback line."""
    try:
        idx = STAGES.index(stage) + 1
    except ValueError:
        idx = None
    pos = f" ({idx}/{len(STAGES)})" if idx else ""

    row = contract.get(stage)
    if not row:
        hint = STAGE_TO_SKILL.get(stage, "see .claude/skills/WORKFLOW.md for mapping")
        return [
            f"Current workflow stage: {stage}{pos}",
            f"Recommended skill/reference: {hint}",
        ]

    layer4 = (
        "warm set (session-kickoff.md, state.md, decisions.md, +3 newest "
        "changelog) per CLAUDE.md memory rules"
    )
    if idx and idx > 1:
        layer4 += "; plus previous stage artefact"

    return [
        f"Current workflow stage: {stage}{pos}",
        "## Inputs",
        f"- Layer 3 (reference, stable): {row['pm']}; ref: {row['reference']}",
        f"- Layer 4 (working, this project): {layer4}",
        "## Process",
        "Produce the stage artefact with the reference skills above; transversais apply at every stage.",
        "## Output / gate",
        f"- Artefact: {row['artefact']}",
        f"- Advance when: {row['gate']}",
    ]


def read_active_context(path: Path) -> tuple[str | None, str | None]:
    """Return (project, stage) parsed from active-context.md, or (None, None)."""
    if not path.exists():
        return None, None
    text = path.read_text(encoding="utf-8", errors="replace")

    project_match = re.search(r"^\s*-?\s*\*{0,2}Project\*{0,2}\s*:\s*(.+?)$", text, re.MULTILINE)
    stage_match = re.search(
        r"^\s*-?\s*\*{0,2}Current\s+stage\*{0,2}\s*:\s*([A-Za-z0-9\-_]+)",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    # Fallback: old "Current phase" field
    if stage_match is None:
        stage_match = re.search(
            r"^\s*-?\s*\*{0,2}Current\s+phase\*{0,2}\s*:\s*([A-Za-z0-9\-_]+)",
            text,
            re.MULTILINE | re.IGNORECASE,
        )

    project = project_match.group(1).strip() if project_match else None
    stage = stage_match.group(1).strip().lower() if stage_match else None
    if stage is not None:
        stage = STAGE_ALIASES.get(stage, stage)
    return project, stage


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    ctx_path = repo_root / ".ai" / "memory" / "active-context.md"
    project, stage = read_active_context(ctx_path)

    lines = ["<umberto-stage-context>"]
    if project:
        lines.append(f"Active project: {project}")
    if stage:
        contract = load_stage_contract(repo_root / ".claude" / "skills" / "WORKFLOW.md")
        lines.extend(build_stage_block(stage, contract))
    elif not ctx_path.exists():
        # Fresh clone: advance_stage.py exits 2 without a pointer, so point
        # at the bootstrap that creates it.
        lines.append('No project context yet. Run: python scripts/init_context.py "<project-name>"')
    else:
        lines.append("No active stage set. Run: python scripts/advance_stage.py <stage-slug>")
        lines.append(f"Valid stages: {', '.join(STAGES)}")
    lines.append("(From .ai/memory/active-context.md — source of truth for workflow position.)")
    lines.append("</umberto-stage-context>")

    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
