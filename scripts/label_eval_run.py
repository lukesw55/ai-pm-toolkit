#!/usr/bin/env python3
"""Attach a human verdict to a recorded eval run; the grader reads it back.

Labels are the ground truth the assertions are checked against. One JSON object per
line in docs/benchmarks/<iteration>/labels.jsonl, tracked in git (the workspace runs
are not). A label names the run it judges, iteration + skill + eval_id + config, and
binds to the exact output by its sha256; the hash alone is not the identity, because
the same text can come back for two prompts or for both configurations. The file is
appended, never edited: a labeler who changes their mind appends a correcting record
with --supersede, the loader keeps the latest record per run and labeler, and the
history stays in the file. A tie between labelers is reported as a split awaiting
resolution, never resolved to the worse verdict.

Usage:
    python3 scripts/label_eval_run.py <skill> <eval-name> --config with_skill \
        --iteration iteration-claude-1 --verdict weak --classification skipped-method \
        --reason "Ranks opportunities but never scores evidence strength" --labeler <role>
    python3 scripts/label_eval_run.py ... --supersede   # same labeler, same run: a correction
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 2
CONFIGS = ("with_skill", "without_skill")
VERDICTS = ("good", "weak", "fail")
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
# The run a label judges. The output hash binds the label to the exact text; the other
# three say which run produced it, because one text can appear under two prompts or in
# both configurations. The iteration is the file.
RUN_KEY = ("skill", "eval_id", "config", "output_sha256")
ITERATION_RE = re.compile(r"iteration-[a-z0-9-]+")
SHA_RE = re.compile(r"[a-f0-9]{64}")
RUBRIC_RE = re.compile(r"[a-f0-9]{12}")


def labels_path(root: Path, iteration: str) -> Path:
    return root / "docs" / "benchmarks" / iteration / "labels.jsonl"


def rubric_version(spec: dict) -> str:
    """Twelve hex characters of the eval's prompt and expected output, the rubric the
    labeler read. A changed prompt or expectation is a different rubric."""
    text = spec["prompt"] + "\n" + spec.get("expected_output", "")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def run_key(record: dict) -> tuple:
    return tuple(record[k] for k in RUN_KEY)


def parse_label(line: str, iteration: str) -> dict:
    try:
        record = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError(f"label line is not JSON: {exc}") from exc
    if not isinstance(record, dict) or record.get("schema") != SCHEMA:
        raise ValueError(f"label must be an object with schema {SCHEMA}")
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
    if not isinstance(record.get("rubric_version"), str) or not RUBRIC_RE.fullmatch(record["rubric_version"]):
        raise ValueError("label rubric_version must be 12 hex characters")
    if record.get("verdict") not in VERDICTS:
        raise ValueError(f"label verdict must be one of {', '.join(VERDICTS)}")
    classification = record.get("classification")
    if not isinstance(classification, list) or any(c not in CLASSIFICATIONS for c in classification):
        raise ValueError(f"label classification must be a list drawn from {', '.join(CLASSIFICATIONS)}")
    if record["verdict"] != "good" and not classification:
        raise ValueError("weak and fail labels need at least one classification handle")
    if type(record.get("supersedes", False)) is not bool:
        raise ValueError("label supersedes must be a boolean")
    stamp = datetime.fromisoformat(str(record.get("labeled_at", "")))
    if stamp.tzinfo is None:
        raise ValueError("labeled_at must include a timezone")
    return record


def read_labels(path: Path, iteration: str) -> list[dict]:
    """Every record in file order, validated. A missing file is an empty list."""
    records: list[dict] = []
    if not path.is_file():
        return records
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(parse_label(line, iteration))
        except ValueError as exc:
            raise ValueError(f"{path}:{number}: {exc}") from exc
    return records


def load_labels(path: Path, iteration: str) -> dict[tuple, list[dict]]:
    """run key -> current labels, the latest record per labeler. Earlier records by the
    same labeler are history: they stay in the file and superseded_count() counts them.
    A missing file is {}, never an error."""
    current: dict[tuple, dict[str, dict]] = {}
    for record in read_labels(path, iteration):
        current.setdefault(run_key(record), {})[record["labeler"]] = record
    return {key: list(by_labeler.values()) for key, by_labeler in current.items()}


def superseded_count(path: Path, iteration: str) -> int:
    records = read_labels(path, iteration)
    return len(records) - len({(run_key(r), r["labeler"]) for r in records})


def _verdict_counts(labels: list[dict]) -> dict[str, int]:
    counts = {v: 0 for v in VERDICTS}
    for record in labels:
        counts[record["verdict"]] += 1
    return counts


def is_split(labels: list[dict]) -> bool:
    """Two or more labelers whose verdicts tie at the top: a disagreement awaiting a
    resolution, reported as such rather than resolved to the worse verdict."""
    if len(labels) < 2:
        return False
    counts = _verdict_counts(labels)
    top = max(counts.values())
    return sum(1 for n in counts.values() if n == top) > 1


def is_mixed(labels: list[dict]) -> bool:
    """Two or more labelers who did not all give the same verdict."""
    return len(labels) >= 2 and len({r["verdict"] for r in labels}) > 1


def human_verdict(labels: list[dict]) -> str | None:
    """Majority verdict; None without labels and None on a split (see is_split)."""
    if not labels or is_split(labels):
        return None
    counts = _verdict_counts(labels)
    return max(counts, key=counts.__getitem__)


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
    key = (args.skill, spec["id"], args.config, meta["output_sha256"])
    prior = [r for r in load_labels(path, args.iteration).get(key, []) if r["labeler"] == labeler]
    supersede = bool(getattr(args, "supersede", False))
    if prior and not supersede:
        raise ValueError(f"run already labeled by {labeler}; pass --supersede to append a correcting record (the earlier one stays in the file)")
    if supersede and not prior:
        raise ValueError(f"--supersede given but {labeler} has no label on this run yet")
    record = {
        "schema": SCHEMA, "iteration": args.iteration, "skill": args.skill, "eval_id": spec["id"],
        "eval_name": spec["name"], "config": args.config, "output_sha256": meta["output_sha256"],
        "rubric_version": rubric_version(spec), "verdict": args.verdict, "classification": classification,
        "verdict_reason": reason, "labeler": labeler, "labeled_at": datetime.now().astimezone().isoformat(),
        "supersedes": supersede,
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
    p.add_argument("--supersede", action="store_true", help="append a correcting record for a run this labeler already labeled; the earlier record stays as history")
    p.add_argument("--labels-file", help="override docs/benchmarks/<iteration>/labels.jsonl")
    args = p.parse_args()
    try:
        print(label(args))
    except (ValueError, OSError, KeyError) as exc:
        p.exit(1, f"label_eval_run: {exc}\n")


if __name__ == "__main__":
    main()
