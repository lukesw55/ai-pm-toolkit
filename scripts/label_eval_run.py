#!/usr/bin/env python3
"""Attach a human verdict to a recorded eval run; the grader reads it back.

Labels are the ground truth the assertions are checked against. One JSON object per
line in docs/benchmarks/<iteration>/labels.jsonl, tracked in git (the workspace runs
are not), bound to the exact output by its sha256, appended and never edited. A run
carries at most one label per labeler; a second opinion is a second line.

Usage:
    python3 scripts/label_eval_run.py <skill> <eval-name> --config with_skill \
        --iteration iteration-claude-1 --verdict weak --classification skipped-method \
        --reason "Ranks opportunities but never scores evidence strength" --labeler <role>
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = ("with_skill", "without_skill")
VERDICTS = ("good", "weak", "fail")
VERDICT_RANK = {"good": 0, "weak": 1, "fail": 2}
CLASSIFICATIONS = (
    "sycophancy",              # accepts a weak premise or caves under pressure with no new argument
    "manufactured-objection",  # invents a reservation against a sound premise
    "invented-fact",           # states unverified or absent facts as true
    "skipped-method",          # ignores the skill's method where it applies
    "wrong-decision",          # applies the method and still lands on the wrong call
    "incomplete",              # misses a required part of the deliverable
    "format-slop",             # structure tells: label-colon runs, banners, padding
    "scope-bloat",             # answers beyond the ask
    "eval-defect",             # the prompt or the assertion block is at fault, not the output
    "review-needed",           # the labeler wants a second opinion; the verdict still stands
)
ITERATION_RE = re.compile(r"iteration-[a-z0-9-]+")
SHA_RE = re.compile(r"[a-f0-9]{64}")


def labels_path(root: Path, iteration: str) -> Path:
    return root / "docs" / "benchmarks" / iteration / "labels.jsonl"


def parse_label(line: str, iteration: str) -> dict:
    try:
        record = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError(f"label line is not JSON: {exc}") from exc
    if not isinstance(record, dict) or record.get("schema") != 1:
        raise ValueError("label must be an object with schema 1")
    if record.get("iteration") != iteration:
        raise ValueError(f"label belongs to iteration {record.get('iteration')!r}, not {iteration!r}")
    for key in ("skill", "eval_name", "verdict_reason", "labeler"):
        if not isinstance(record.get(key), str) or not record[key].strip():
            raise ValueError(f"label field {key} must be a non-empty string")
    if type(record.get("eval_id")) is not int:
        raise ValueError("label eval_id must be an integer")
    if record.get("config") not in CONFIGS:
        raise ValueError("label config must be with_skill or without_skill")
    if not isinstance(record.get("output_sha256"), str) or not SHA_RE.fullmatch(record["output_sha256"]):
        raise ValueError("label output_sha256 must be 64 hex characters")
    if record.get("verdict") not in VERDICTS:
        raise ValueError(f"label verdict must be one of {', '.join(VERDICTS)}")
    classification = record.get("classification")
    if not isinstance(classification, list) or any(c not in CLASSIFICATIONS for c in classification):
        raise ValueError(f"label classification must be a list drawn from {', '.join(CLASSIFICATIONS)}")
    if record["verdict"] != "good" and not classification:
        raise ValueError("weak and fail labels need at least one classification handle")
    stamp = datetime.fromisoformat(str(record.get("labeled_at", "")))
    if stamp.tzinfo is None:
        raise ValueError("labeled_at must include a timezone")
    return record


def load_labels(path: Path, iteration: str) -> dict[str, list[dict]]:
    """output_sha256 -> labels. A missing file is an empty set, never an error."""
    labels: dict[str, list[dict]] = {}
    if not path.is_file():
        return labels
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = parse_label(line, iteration)
        except ValueError as exc:
            raise ValueError(f"{path}:{number}: {exc}") from exc
        labels.setdefault(record["output_sha256"], []).append(record)
    return labels


def human_verdict(labels: list[dict]) -> str | None:
    """Majority verdict; a tie resolves to the worse verdict; no labels is None."""
    if not labels:
        return None
    counts = {v: 0 for v in VERDICTS}
    for record in labels:
        counts[record["verdict"]] += 1
    top = max(counts.values())
    return max((v for v, n in counts.items() if n == top), key=VERDICT_RANK.__getitem__)


def binarize(labels: list[dict]) -> bool | None:
    verdict = human_verdict(labels)
    return None if verdict is None else verdict == "good"


def label(args, root: Path = ROOT) -> Path:
    import record_eval_run as rr
    if not ITERATION_RE.fullmatch(args.iteration):
        raise ValueError("iteration must match iteration-[a-z0-9-]+")
    if args.config not in CONFIGS:
        raise ValueError("config must be with_skill or without_skill")
    spec = rr.eval_spec(root, args.skill, args.eval)
    directory = root / "skills" / args.skill / "workspace" / args.iteration / f"eval-{spec['id']}-{spec['name']}" / args.config
    if not directory.is_dir():
        raise OSError(f"no recorded run at {directory.relative_to(root).as_posix()}")
    meta = rr.validate_run(directory, args.skill, spec, args.config)
    if args.verdict not in VERDICTS:
        raise ValueError(f"verdict must be one of {', '.join(VERDICTS)}")
    classification = list(args.classification or [])
    unknown = [c for c in classification if c not in CLASSIFICATIONS]
    if unknown:
        raise ValueError(f"unknown classification {', '.join(unknown)}; use {', '.join(CLASSIFICATIONS)}")
    if args.verdict != "good" and not classification:
        raise ValueError("weak and fail labels need at least one classification handle")
    reason = (args.reason or "").strip()
    labeler = (args.labeler or "").strip()
    if not reason or not labeler:
        raise ValueError("--reason and --labeler must not be empty")
    path = Path(args.labels_file) if getattr(args, "labels_file", None) else labels_path(root, args.iteration)
    existing = load_labels(path, args.iteration)
    if any(prior["labeler"] == labeler for prior in existing.get(meta["output_sha256"], [])):
        raise ValueError(f"run already labeled by {labeler}; labels are appended, never replaced")
    record = {
        "schema": 1, "iteration": args.iteration, "skill": args.skill, "eval_id": spec["id"],
        "eval_name": spec["name"], "config": args.config, "output_sha256": meta["output_sha256"],
        "verdict": args.verdict, "classification": classification, "verdict_reason": reason,
        "labeler": labeler, "labeled_at": datetime.now().astimezone().isoformat(),
    }
    parse_label(json.dumps(record), args.iteration)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("skill")
    p.add_argument("eval")
    p.add_argument("--config", required=True, choices=CONFIGS)
    p.add_argument("--iteration", required=True)
    p.add_argument("--verdict", required=True, choices=VERDICTS)
    p.add_argument("--classification", action="append", default=[], help="handle; repeat for several")
    p.add_argument("--reason", required=True, help="one line on why")
    p.add_argument("--labeler", required=True, help="role or initials of the person labelling")
    p.add_argument("--labels-file", help="override docs/benchmarks/<iteration>/labels.jsonl")
    args = p.parse_args()
    try:
        print(label(args))
    except (ValueError, OSError, KeyError) as exc:
        p.exit(1, f"label_eval_run: {exc}\n")


if __name__ == "__main__":
    main()
