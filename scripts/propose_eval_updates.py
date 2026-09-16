#!/usr/bin/env python3
"""Turn labelled grader disagreements into proposals a human decides on.

The grader reports where it disagrees with the humans; nothing until now turned that
signal into a reviewable change. This script reads the labels for an iteration, re-grades
the recorded output, and writes one proposal per disagreement under
docs/benchmarks/<iteration>/proposals/. It never edits an eval manifest, the ASSERTIONS
block in scripts/grade_evals.py, or scripts/fixtures/adversarial_outputs.json. A grader
that rewrote its own assertions from the outputs it grades would stop measuring the model
and start measuring itself, so the proposal is a hypothesis for a human to accept, reject
or rewrite, and the fixture it suggests is a slot replacement staged for a person to paste.

A proposal exists only because a human wrote a verdict and a reason. Unlabelled runs carry
no signal and are never harvested, no matter how they scored.

Usage:
    python3 scripts/propose_eval_updates.py propose --iteration iteration-claude-1
    python3 scripts/propose_eval_updates.py propose --iteration iteration-claude-1 --dry-run
    python3 scripts/propose_eval_updates.py propose --iteration iteration-claude-1 --skill repo-doctor
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))

import grade_evals as ge  # noqa: E402
import label_eval_run as lr  # noqa: E402
import record_eval_run as rr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 1
EXCERPT_CHARS = 1200
FIXTURES = "scripts/fixtures/adversarial_outputs.json"
# The key order of every object in the fixtures file. A suggestion is printed in this
# order so a human can paste it over the existing object without reshuffling the file.
FIXTURE_KEYS = ("skill", "eval", "good", "bad", "keyword_only", "near_miss")
# Written into every proposal. The three paths this script must never touch.
NEVER_EDITS = ("skills/<skill>/evals/evals.json", "scripts/grade_evals.py", FIXTURES)


def proposals_dir(root: Path, iteration: str) -> Path:
    return root / "docs" / "benchmarks" / iteration / "proposals"


def run_dir(root: Path, iteration: str, skill: str, eval_id: int, eval_name: str, config: str) -> Path:
    return root / "skills" / skill / "workspace" / iteration / f"eval-{eval_id}-{eval_name}" / config


def proposal_stem(skill: str, eval_id: int, eval_name: str, config: str, sha: str) -> str:
    """Stable per run, so a second pass rewrites a proposal instead of adding one. Every
    component is already constrained to [a-z0-9-] by record_eval_run.TOKEN."""
    return f"{skill}__eval-{eval_id}-{eval_name}__{config}__{sha[:12]}"


def load_fixture_pairs(root: Path) -> list[dict]:
    path = root / FIXTURES
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def find_pair(pairs: list[dict], skill: str, eval_name: str) -> tuple[int | None, dict | None]:
    for index, pair in enumerate(pairs):
        if pair.get("skill") == skill and pair.get("eval") == eval_name:
            return index, pair
    return None, None


def excerpt(text: str, limit: int, full: bool) -> dict:
    """Bounded by default. The workspace is gitignored and docs/ is tracked, so a full
    output would publish model text into git permanently and grow a corpus of it beside
    the fixtures file, one directory from where an assertion author would look. The hash
    and the run path make the excerpt a pointer with evidence attached."""
    body = text if full else text[:limit]
    return {
        "text": body,
        "chars": len(body),
        "truncated": not full and len(text) > limit,
        "output_chars": len(text),
    }


def classify(current: list[dict], stale: list[dict], grading: dict) -> str:
    """One category per run, in this precedence. A stale-rubric card is emitted only when
    every label on the run is stale, so one run never yields two cards."""
    if not current and stale:
        return "stale-rubric"
    if lr.is_split(current):
        return "split"
    if any("eval-defect" in record["classification"] for record in current):
        return "eval-defect"
    # current is non-empty and not split, so there is a consolidated verdict to compare.
    if ge.agreement(grading):
        return "agreement"
    return "false-accept" if grading["pass_rate"] >= ge.PASS_THRESHOLD else "false-reject"


def implicated(category: str, grading: dict, checks: list, pair: dict | None) -> dict | None:
    """Which assertions the disagreement points at, or None when the category is not about
    the assertions at all. For a false reject the failing ones, exactly. For a false accept
    every assertion passed, so the only mechanical signal is which of them also pass on this
    eval's own bad and keyword-only fixtures: an assertion a wrong answer already satisfies
    is the one least likely to be checking behaviour."""
    if category not in ("false-accept", "false-reject"):
        return None
    labels = [e["text"] for e in grading["expectations"] if not e["passed"]]
    also_bad: list[str] = []
    also_keyword: list[str] = []
    if category == "false-accept" and pair:
        for (label, check), expectation in zip(checks, grading["expectations"]):
            if not expectation["passed"]:
                continue
            try:
                if check(pair["bad"].lower()):
                    also_bad.append(label)
                if check(pair["keyword_only"].lower()):
                    also_keyword.append(label)
            except Exception:  # an assertion that raises is already reported by grade_run
                continue
        labels = []
    return {
        "rule": "failing-assertions" if category == "false-reject" else "passing-assertions",
        "labels": labels,
        "also_pass_on_bad_fixture": also_bad,
        "also_pass_on_keyword_only_fixture": also_keyword,
    }


def fixture_suggestion(category: str, verdict: str | None, index: int | None, pair: dict | None, text: str) -> dict | None:
    """A slot replacement inside the existing object, never a new array element: the file
    holds exactly one object per eval and all of them exist, and a second object for the
    same eval would pass the suite unnoticed because the coverage checks are subset tests.

    The direction matters and is recorded. A negative fixture taken from a run that really
    failed hardens the grader against a failure that happened, which is the point of the
    loop. A positive fixture copied from a run that really passed makes the grader agree
    with that model by construction, so a good candidate is marked for a rewrite by hand.
    """
    if category not in ("false-accept", "false-reject") or pair is None:
        return None
    if category == "false-accept":
        slot = "bad" if verdict == "fail" else "near_miss"
    else:
        slot = "good"
    snippet = {key: pair[key] for key in FIXTURE_KEYS if key in pair}
    if slot == "near_miss":
        value: object = {"text": text, "fails": "<the assertion label you are about to write>"}
        band = [0.50, 0.99]
    else:
        value = text
        band = [0.80, 1.0] if slot == "good" else [0.0, 0.30]
    current_value = json.dumps(pair.get(slot), sort_keys=True, ensure_ascii=False)
    snippet[slot] = value
    # A candidate that equals another slot's current value cannot be right: one text cannot
    # be both the answer to accept and the answer to reject. Usually it means the run that
    # was labelled is the text a fixture already holds.
    collides = sorted(
        key for key in ("good", "bad", "keyword_only")
        if key != slot and isinstance(pair.get(key), str) and pair[key] == text
    )
    return {
        "slot": slot,
        "pair_exists": True,
        "pair_index": index,
        "current_value_sha256": hashlib.sha256(current_value.encode("utf-8")).hexdigest(),
        "band": band,
        "snippet": snippet,
        "collides_with_slots": collides,
        "derived_from": "model output",
        "verbatim": True,
        "rewrite_required": slot == "good",
    }


def assertion_change(category: str, implicated_labels: dict | None, current: list[dict]) -> dict | None:
    """A direction and a rule in plain English, composed only from the assertion labels
    involved and the reason the labeler wrote. No regex is generated: a pattern written
    from one output matches that output, and the person who writes it has to own it."""
    if category not in ("false-accept", "false-reject") or implicated_labels is None:
        return None
    reasons = [record["verdict_reason"] for record in current]
    if category == "false-accept":
        targets = implicated_labels["also_pass_on_bad_fixture"] or implicated_labels["also_pass_on_keyword_only_fixture"]
        direction = "tighten"
        rule = ("An assertion has to reject the behaviour the labeler describes below. "
                "Every assertion passed on this output, so the gap is not a failing check but a missing one.")
    else:
        targets = implicated_labels["labels"]
        direction = "loosen or re-shape"
        rule = ("The assertions below rejected an output a human accepted. Either they demand a form the "
                "prompt never asked for, or they demand it in one phrasing only.")
    return {
        "direction": direction,
        "targets": targets,
        "rule_in_plain_english": rule,
        "reasons_quoted": reasons,
        "regex": None,
        "note": "no regex is generated; the human writes it and owns it",
    }


def rubric_impact(labels_by_key: dict, skill: str, eval_id: int) -> dict:
    """An eval-defect proposal that edits a prompt or an expected output changes the
    rubric version, and every label on that eval becomes stale. Count them first."""
    affected = sum(len(records) for key, records in labels_by_key.items() if key[0] == skill and key[1] == eval_id)
    return {
        "labels_invalidated_if_rubric_changes": affected,
        "note": "changing the prompt or the expected output makes every label above stale; the runs are relabelled, not superseded",
    }


def decisions_for(category: str, run: dict, iteration: str) -> list[dict]:
    """What the human decides, in order, each with the command that answers it."""
    skill, name, config = run["skill"], run["eval_name"], run["config"]
    relabel = (f"python3 scripts/label_eval_run.py {skill} {name} --config {config} "
               f"--iteration {iteration} --verdict <good|weak|fail> --classification <handle> "
               f"--reason \"<one line>\" --labeler <role>")
    if category == "stale-rubric":
        return [{"order": 1, "question": "Re-read the current prompt and expectation, then label the run again. A stale label is relabelled, never superseded.", "command": relabel}]
    if category == "eval-defect":
        return [
            {"order": 1, "question": "Is the prompt or the expected output at fault? Read both before touching an assertion.", "command": f"python3 -c \"import json;print(json.dumps([e for e in json.load(open('skills/{skill}/evals/evals.json'))['evals'] if e['name']=='{name}'][0],indent=2))\""},
            {"order": 2, "question": "If the rubric changes, relabel every run of this eval; the count is in the proposal.", "command": relabel},
        ]
    return [
        {"order": 1, "question": "Does the labeler's reason describe a behaviour an assertion should check? If not, the label is the thing to revisit.", "command": "(read the reason quoted above)"},
        {"order": 2, "question": "Write the assertion change by hand in scripts/grade_evals.py. The proposal names the direction, not the pattern.", "command": "(edit the ASSERTIONS block for " + f"{skill} / {name})"},
        {"order": 3, "question": "Paste the fixture candidate over the existing slot in the fixtures file, then re-run the suite step by step.", "command": f"python3 scripts/propose_eval_updates.py check --skill {skill} --eval {name}"},
    ]


def build_proposal(root: Path, iteration: str, key: tuple, labels_by_key: dict, *, limit: int, full: bool) -> dict:
    """One proposal, or an outcome that explains why there is none. Never raises for a run
    that is simply absent: a label whose run is not on this machine is reported, the way
    grade_all already reports one, and never an error."""
    skill, eval_id, config, sha = key
    records = labels_by_key[key]
    eval_name = records[0]["eval_name"]
    base = {"key": {"skill": skill, "eval_id": eval_id, "eval_name": eval_name, "config": config, "output_sha256": sha}}
    try:
        spec = rr.eval_spec(root, skill, eval_name)
    except (ValueError, OSError, KeyError):
        return {**base, "outcome": "orphan-eval"}
    directory = run_dir(root, iteration, skill, eval_id, eval_name, config)
    if not directory.is_dir():
        return {**base, "outcome": "no-run-here"}
    try:
        meta = rr.validate_run(directory, skill, spec, config)
    except (ValueError, OSError, KeyError) as exc:
        return {**base, "outcome": "invalid-run", "detail": str(exc)}
    if meta["output_sha256"] != sha:
        return {**base, "outcome": "hash-mismatch"}

    output_path = directory / "outputs" / "output.md"
    text = output_path.read_text(encoding="utf-8", errors="replace")
    grading = ge.grade_run(output_path, skill, eval_name)
    if grading is None:
        return {**base, "outcome": "no-output"}
    current, stale = lr.split_by_rubric(records, lr.rubric_version(spec))
    grading["labels"] = current
    grading["human_verdict"] = lr.human_verdict(current)
    grading["human_split"] = lr.is_split(current)
    category = classify(current, stale, grading)
    if category in ("agreement", "split"):
        return {**base, "outcome": category}

    checks = ge.ASSERTIONS.get(skill, {}).get(eval_name, [])
    pairs = load_fixture_pairs(root)
    index, pair = find_pair(pairs, skill, eval_name)
    marks = implicated(category, grading, checks, pair)
    verdict = grading["human_verdict"]
    stored = json.loads((directory / "grading.json").read_text(encoding="utf-8")) if (directory / "grading.json").is_file() else None

    proposal = {
        "schema": SCHEMA,
        "kind": "eval-proposal",
        "category": category,
        "status": "proposed",
        "generated_by": "scripts/propose_eval_updates.py",
        "never_edits": list(NEVER_EDITS),
        "run": {
            "iteration": iteration, "skill": skill, "eval_id": eval_id, "eval_name": eval_name,
            "config": config, "output_sha256": sha, "rubric_version": lr.rubric_version(spec),
            "harness": meta["harness"], "model": meta["model"], "repo_commit": meta["repo_commit"],
            "recorded_at": meta["recorded_at"],
            "output_path": output_path.relative_to(root).as_posix(),
            "output_words": grading["word_count"],
        },
        "human": {
            "verdict": verdict,
            "split": grading["human_split"],
            "handles": sorted({h for record in current for h in record["classification"]}),
            "labels": [{k: record[k] for k in ("labeler", "verdict", "classification", "verdict_reason", "labeled_at", "rubric_version", "supersedes")} for record in current],
            "stale_labels": [{"labeler": r["labeler"], "rubric_version": r["rubric_version"], "verdict": r["verdict"]} for r in stale],
        },
        "grader": {
            "pass_rate": grading["pass_rate"], "passed": grading["passed"], "total": grading["total"],
            "threshold": ge.PASS_THRESHOLD,
            "binarised_pass": grading["pass_rate"] >= ge.PASS_THRESHOLD,
            "agrees": ge.agreement(grading),
            "expectations": [{"text": e["text"], "passed": e["passed"]} for e in grading["expectations"]],
            "stored_grading_pass_rate": None if stored is None else stored.get("pass_rate"),
            "stored_grading_matches": None if stored is None else stored.get("pass_rate") == grading["pass_rate"],
        },
        "implicated_assertions": marks,
        "fixture_suggestion": fixture_suggestion(category, verdict, index, pair, text),
        "assertion_change": assertion_change(category, marks, current),
        "rubric_impact": rubric_impact(labels_by_key, skill, eval_id) if category == "eval-defect" else None,
        "human_decisions": decisions_for(category, {"skill": skill, "eval_name": eval_name, "config": config}, iteration),
        "excerpt": excerpt(text, limit, full),
    }
    return {**base, "outcome": category, "proposal": proposal}


def render_markdown(proposal: dict) -> str:
    """Byte-stable: no timestamp, so a second pass over an unchanged run produces the same
    bytes and content_sha256 detects a human's edits rather than the tool's own churn."""
    run, human, grader = proposal["run"], proposal["human"], proposal["grader"]
    out: list[str] = []
    out.append(f"# Proposal — {run['skill']} / eval {run['eval_id']} {run['eval_name']} / {run['config']}")
    out.append("")
    out.append(f"Category: **{proposal['category']}**. Status: **{proposal['status']}**. "
               "Nothing was applied: this pass did not touch "
               + ", ".join(f"`{p}`" for p in proposal["never_edits"]) + ".")
    out.append("")
    out.append("## Run")
    out.append("")
    out.append("| Field | Value |")
    out.append("|---|---|")
    for label, value in (
        ("iteration", run["iteration"]), ("skill", run["skill"]), ("eval id", run["eval_id"]),
        ("eval name", run["eval_name"]), ("config", run["config"]), ("output sha256", run["output_sha256"]),
        ("rubric version", run["rubric_version"]), ("harness", run["harness"]), ("model", run["model"]),
        ("repo commit", run["repo_commit"]), ("recorded at", run["recorded_at"]), ("words", run["output_words"]),
    ):
        out.append(f"| {label} | {value} |")
    out.append("")
    out.append("## Human verdict")
    out.append("")
    verdict = human["verdict"] or ("split, no consolidated verdict" if human["split"] else "none")
    out.append(f"Consolidated verdict: **{verdict}**. Handles: {', '.join(human['handles']) or 'none'}.")
    out.append("")
    out.append("| Labeler | Verdict | Handles | Reason | Labelled at |")
    out.append("|---|---|---|---|---|")
    for record in human["labels"]:
        out.append(f"| {record['labeler']} | {record['verdict']} | {', '.join(record['classification']) or '—'} "
                   f"| {record['verdict_reason']} | {record['labeled_at']} |")
    if human["stale_labels"]:
        out.append("")
        out.append("Stale labels, made against another rubric and not counted: "
                   + "; ".join(f"{r['labeler']} said {r['verdict']} against rubric {r['rubric_version']}" for r in human["stale_labels"]) + ".")
    out.append("")
    out.append("## Grader")
    out.append("")
    out.append(f"Pass rate {grader['pass_rate']:.2f} ({grader['passed']} of {grader['total']}), "
               f"threshold {grader['threshold']}, binarised {'pass' if grader['binarised_pass'] else 'fail'}, "
               f"agrees with the human: {grader['agrees']}.")
    if grader["stored_grading_matches"] is False:
        out.append("")
        out.append(f"The stored grading.json says {grader['stored_grading_pass_rate']}; this pass re-graded and got "
                   f"{grader['pass_rate']}. The stored report is stale — re-run `scripts/grade_evals.py`.")
    out.append("")
    out.append("| # | Assertion | Result |")
    out.append("|---|---|---|")
    for number, expectation in enumerate(grader["expectations"], start=1):
        out.append(f"| {number} | {expectation['text']} | {'PASS' if expectation['passed'] else 'FAIL'} |")
    out.append("")
    out.append("## Output")
    out.append("")
    ex = proposal["excerpt"]
    out.append(f"sha256 {run['output_sha256']}, {ex['output_chars']} characters, recorded at "
               f"{run['output_path']} (the workspace is not tracked, so this path exists only where the run was recorded).")
    out.append("")
    out.append(f"First {ex['chars']} characters:" if ex["truncated"] else "Full output:")
    out.append("")
    out.append("```text")
    out.append(ex["text"])
    out.append("```")
    out.append("")
    marks = proposal["implicated_assertions"]
    if marks is None:
        out.append("## Assertions")
        out.append("")
        out.append("This category is not about the assertions, so none is named here. The grader table above is the "
                   "whole of what the checks said about this run.")
        out.append("")
    elif marks["rule"] == "failing-assertions":
        out.append("## Implicated assertions")
        out.append("")
        out.append("These assertions rejected the output:")
        out.append("")
        for label in marks["labels"]:
            out.append(f"- {label}")
    else:
        out.append("## Implicated assertions")
        out.append("")
        out.append("Every assertion passed, so no failing check points at the gap. The labeler's reason is the "
                   "only evidence of which behaviour goes unchecked:")
        out.append("")
        for record in human["labels"]:
            out.append(f"> {record['verdict_reason']} — {record['labeler']}")
        if marks["also_pass_on_bad_fixture"]:
            out.append("")
            out.append("Assertions that also pass on this eval's own bad fixture, so they are the least likely to be checking behaviour:")
            out.append("")
            for label in marks["also_pass_on_bad_fixture"]:
                out.append(f"- {label}")
        if marks["also_pass_on_keyword_only_fixture"]:
            out.append("")
            out.append("Assertions that also pass on its keyword-only fixture:")
            out.append("")
            for label in marks["also_pass_on_keyword_only_fixture"]:
                out.append(f"- {label}")
    out.append("")
    if proposal["rubric_impact"]:
        out.append("## Rubric impact")
        out.append("")
        out.append(f"{proposal['rubric_impact']['labels_invalidated_if_rubric_changes']} label(s) on this eval go stale if the "
                   "prompt or the expected output changes. " + proposal["rubric_impact"]["note"] + ".")
        out.append("")
    suggestion = proposal["fixture_suggestion"]
    if suggestion:
        out.append("## Suggested fixture (candidate, not applied)")
        out.append("")
        out.append(f"The fixtures file holds exactly one object per eval and this eval already has one at index "
                   f"{suggestion['pair_index']}. This is a replacement for its `{suggestion['slot']}` slot, not a second object: "
                   "a duplicate would pass the suite unnoticed, because the coverage checks are subset tests. The value it would "
                   f"replace hashes to {suggestion['current_value_sha256'][:12]}. Band for this slot: "
                   f"{suggestion['band'][0]} to {suggestion['band'][1]}.")
        out.append("")
        if suggestion["rewrite_required"]:
            out.append("**Rewrite this before pasting it.** A good fixture copied from a run the grader already accepts makes "
                       "the grader agree with that model by construction. Reword it, keeping the substance, and the test that "
                       "the assertion checks behaviour rather than phrasing is that the reworded text still scores in band.")
        else:
            out.append("This is a negative fixture taken from a run that really failed, which is the direction that hardens the "
                       "grader against a failure that happened. It is the recorded output, verbatim.")
        if suggestion["collides_with_slots"]:
            out.append("")
            out.append("**This candidate is already the value of the `" + "`, `".join(suggestion["collides_with_slots"])
                       + "` slot of the same pair.** One text cannot be both the answer to accept and the answer to reject, so "
                       "pasting it as it stands would make the pair contradict itself. Either the labelled run is a text the "
                       "fixtures already hold, or the label is the thing to revisit.")
        out.append("")
        out.append(f"Replace the `{suggestion['slot']}` value of that object with this, and leave its other keys alone. "
                   "The whole candidate object is in the JSON sibling of this file.")
        out.append("")
        out.append("```json")
        out.append(json.dumps({suggestion["slot"]: suggestion["snippet"][suggestion["slot"]]}, indent=2, ensure_ascii=False))
        out.append("```")
        out.append("")
    change = proposal["assertion_change"]
    if change:
        out.append("## Proposed assertion change (not a regex)")
        out.append("")
        out.append(f"Direction: **{change['direction']}**. {change['rule_in_plain_english']}")
        out.append("")
        if change["targets"]:
            for label in change["targets"]:
                out.append(f"- {label}")
            out.append("")
        out.append("```python")
        out.append("# Written by hand, in scripts/grade_evals.py, by whoever owns this change.")
        out.append("# The tool does not generate a pattern: one written from a single output matches")
        out.append("# that output and nothing else.")
        out.append('#     ("<label describing the check, without its tokens>", hasr(r"<pattern>")),')
        out.append("```")
        out.append("")
    out.append("## What you decide, in this order")
    out.append("")
    for step in proposal["human_decisions"]:
        out.append(f"{step['order']}. {step['question']}")
        out.append("")
        out.append(f"   `{step['command']}`")
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def write_proposal(out_dir: Path, stem: str, proposal: dict, *, force: bool, dry_run: bool) -> tuple[str, str]:
    """(state, detail). States: written, updated, unchanged, refused, dry-run."""
    md_path, json_path = out_dir / f"{stem}.md", out_dir / f"{stem}.json"
    markdown = render_markdown(proposal)
    record = dict(proposal)
    record["content_sha256"] = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    if json_path.is_file():
        existing = json.loads(json_path.read_text(encoding="utf-8"))
        if existing.get("status") not in (None, "proposed"):
            return "decided", f"status {existing.get('status')}"
        if md_path.is_file():
            on_disk = hashlib.sha256(md_path.read_bytes()).hexdigest()
            if existing.get("content_sha256") and on_disk != existing["content_sha256"] and not force:
                return "refused", "the markdown was edited by hand; pass --force to overwrite it"
        comparable_new = {k: v for k, v in record.items() if k != "generated_at"}
        comparable_old = {k: v for k, v in existing.items() if k != "generated_at"}
        if comparable_new == comparable_old and md_path.is_file() and not force:
            return "unchanged", ""
        changes = []
        for field, old, new in (
            ("human.verdict", (existing.get("human") or {}).get("verdict"), record["human"]["verdict"]),
            ("grader.pass_rate", (existing.get("grader") or {}).get("pass_rate"), record["grader"]["pass_rate"]),
            ("category", existing.get("category"), record["category"]),
        ):
            if old != new:
                changes.append(f"{field} {old} -> {new}")
        if dry_run:
            return "dry-run", "; ".join(changes)
        record["generated_at"] = datetime.now().astimezone().isoformat()
        out_dir.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown, encoding="utf-8")
        json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return "updated", "; ".join(changes)
    if dry_run:
        return "dry-run", ""
    record["generated_at"] = datetime.now().astimezone().isoformat()
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return "written", ""


def render_index(iteration: str, rows: list[dict]) -> str:
    out = [f"# Proposal pass — {iteration}", ""]
    out.append("Every label in this iteration and what came of it. A proposal is written only for a run where a "
               "human verdict and the grader disagree, or where the eval itself is in question; agreement, a split "
               "and an unlabelled run are outcomes, not proposals.")
    out.append("")
    out.append("| Skill | Eval | Config | Outcome | Proposal |")
    out.append("|---|---|---|---|---|")
    for row in rows:
        key = row["key"]
        name = f"`{row['stem']}.md`" if row.get("stem") else "—"
        out.append(f"| {key['skill']} | {key['eval_id']} {key['eval_name']} | {key['config']} | {row['outcome']} | {name} |")
    out.append("")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
    out.append("Outcomes: " + ", ".join(f"{name} {n}" for name, n in sorted(counts.items())) + ".")
    return "\n".join(out) + "\n"


def propose(args, root: Path = ROOT) -> dict:
    if not lr.ITERATION_RE.fullmatch(args.iteration):
        raise ValueError("iteration must match iteration-[a-z0-9-]+")
    labels_file = Path(args.labels) if args.labels else lr.labels_path(root, args.iteration)
    labels_by_key = lr.load_labels(labels_file, args.iteration)
    out_dir = Path(args.out) if args.out else proposals_dir(root, args.iteration)
    rows: list[dict] = []
    for key in sorted(labels_by_key):
        skill, eval_id, config, _sha = key
        if args.skill and skill != args.skill:
            continue
        if args.eval and labels_by_key[key][0]["eval_name"] != args.eval:
            continue
        built = build_proposal(root, args.iteration, key, labels_by_key, limit=args.excerpt_chars, full=args.full_output)
        row = {"key": built["key"], "outcome": built["outcome"]}
        if built["outcome"] in ("no-run-here", "hash-mismatch", "invalid-run", "orphan-eval"):
            print(f"WARN {built['outcome']}: {skill} eval {eval_id} {config} output {key[3][:12]}", file=sys.stderr)
        if "proposal" in built:
            stem = proposal_stem(skill, eval_id, built["key"]["eval_name"], config, key[3])
            state, detail = write_proposal(out_dir, stem, built["proposal"], force=args.force, dry_run=args.dry_run)
            row["stem"] = stem
            row["state"] = state
            print(f"{state} {stem}" + (f": {detail}" if detail else ""))
        rows.append(row)
    index = {"schema": SCHEMA, "iteration": args.iteration, "outcomes": rows}
    if not args.dry_run and rows:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.md").write_text(render_index(args.iteration, rows), encoding="utf-8")
        payload = dict(index)
        payload["generated_at"] = datetime.now().astimezone().isoformat()
        (out_dir / "index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    written = sum(1 for row in rows if row.get("state") in ("written", "updated"))
    print(f"{len(rows)} label key(s) read, {written} proposal(s) written or updated"
          + (" (dry run, nothing written)" if args.dry_run else ""))
    return index


def shape_errors(pairs: object, root: Path) -> list[str]:
    """What a human's paste can break that nothing else checks. The suite assumes the file
    is well formed: a missing key or a reordered object surfaces as a KeyError traceback
    rather than a sentence, and a second object for an eval that already has one used to
    pass silently. Run before the suite so the report starts with the paste, not with a
    stack trace."""
    problems: list[str] = []
    if not isinstance(pairs, list):
        return ["the fixtures file must hold a list of objects"]
    seen: set[tuple] = set()
    for position, pair in enumerate(pairs):
        where = f"object {position}"
        if not isinstance(pair, dict):
            problems.append(f"{where}: not an object")
            continue
        if tuple(pair) != FIXTURE_KEYS:
            problems.append(f"{where}: keys are {tuple(pair)}, expected {FIXTURE_KEYS} in that order")
            continue
        where = f"{pair['skill']}/{pair['eval']}"
        for key in ("good", "bad", "keyword_only"):
            if not isinstance(pair[key], str) or not pair[key].strip():
                problems.append(f"{where}: {key} must be a non-empty string")
        near = pair["near_miss"]
        # Order matters for the object's own keys, because a paste should read like the rest
        # of the file; inside near_miss it is cosmetic and the file already mixes both.
        if not isinstance(near, dict) or set(near) != {"text", "fails"}:
            problems.append(f"{where}: near_miss must be an object with exactly text and fails")
        elif not str(near["text"]).strip() or not str(near["fails"]).strip():
            problems.append(f"{where}: near_miss text and fails must be non-empty")
        key = (pair["skill"], pair["eval"])
        if key in seen:
            problems.append(f"{where}: a second object for an eval that already has one; the candidate replaces a slot of the first")
        seen.add(key)
        if not ge.ASSERTIONS.get(pair["skill"], {}).get(pair["eval"]):
            problems.append(f"{where}: no assertion block in scripts/grade_evals.py")
        try:
            rr.eval_spec(root, pair["skill"], pair["eval"])
        except (ValueError, OSError, KeyError):
            problems.append(f"{where}: not an eval in that skill's evals.json")
    return problems


def check(args, root: Path = ROOT) -> int:
    """Run the grader suite against what a human pasted and report it step by step. A green
    suite means the fixtures it has do not contradict the assertion, not that the assertion
    is right; the verdict says so."""
    skill, eval_name = args.skill, args.eval
    print(f"Checking {skill} / {eval_name}\n")

    print("step 1/7  the pasted pair, before anything runs")
    path = root / FIXTURES
    try:
        pairs = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  FAIL  {FIXTURES} does not parse: {exc}")
        return 1
    problems = shape_errors(pairs, root)
    for problem in problems:
        print(f"  FAIL  {problem}")
    index, pair = find_pair(pairs, skill, eval_name)
    if pair is None:
        print(f"  FAIL  no object for {skill} / {eval_name}")
        return 1
    if problems:
        print("\n  The suite is not run: fix the paste first, or the failures below would be about its shape.")
        return 1
    print(f"  ok    one object at index {index}, six keys in order, near miss declared to fail: {pair['near_miss']['fails']!r}")

    print("\nstep 2/7  the grader suite")
    with tempfile.TemporaryDirectory(prefix="propose-check-") as td:
        summary_path = Path(td) / "summary.json"
        completed = subprocess.run(
            [sys.executable, str(root / "scripts" / "test_grade_evals.py"), "--json-summary", str(summary_path)],
            cwd=root, capture_output=True, text=True, timeout=args.timeout,
        )
        if not summary_path.is_file():
            print("  FAIL  the suite wrote no summary; this checkout may predate --json-summary")
            print(completed.stdout[-2000:] or completed.stderr[-2000:])
            return 1
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    counts = summary["counts"]
    print(f"  {'ok   ' if summary['exit_code'] == 0 else 'FAIL '} {counts['fixtures']} fixtures, "
          f"{counts['pairs']} pairs, {counts['failures']} failure(s) in the whole suite")

    mine = [row for row in summary["fixtures"] if (row["skill"], row["eval"]) == (skill, eval_name)]
    print(f"\nstep 3/7  the fixtures derived from this pair ({len(mine)})")
    for row in sorted(mine, key=lambda r: r["name"]):
        print(f"  {'ok   ' if row['ok'] else 'FAIL '} {row['name']}: {row['pass_rate']:.2f} in [{row['min']}, {row['max']}]")
        for expectation in row.get("expectations", []):
            print(f"          {'PASS' if expectation['passed'] else 'FAIL'} {expectation['text']}")

    pair_row = next((row for row in summary["pairs"] if (row["skill"], row["eval"]) == (skill, eval_name)), None)
    print("\nstep 4/7  near miss: declared against actual")
    if pair_row is None:
        print("  FAIL  the suite reported no pair row for this eval")
    else:
        print(f"  declared  {pair_row['near_miss_declared']!r}")
        print(f"  actual    {pair_row['near_miss_failing']}")
        print(f"  {'ok   ' if pair_row['near_miss_ok'] else 'FAIL '} a near miss must fail exactly the assertion it names")

    print("\nstep 5/7  discrimination gap")
    if pair_row:
        print(f"  {'ok   ' if pair_row['gap_ok'] else 'FAIL '} good {pair_row['good_rate']:.2f} - bad "
              f"{pair_row['bad_rate']:.2f} = {pair_row['gap']:.2f} (floor 0.50)")

    print("\nstep 6/7  the derived attacks on this pair")
    if pair_row:
        for kind, rows in (("keyword-only", pair_row["keyword_variants"]), ("label soup", pair_row["label_soup"])):
            for row in rows:
                print(f"  {'ok   ' if row['ok'] else 'FAIL '} {kind} joined by {row['sep']!r}: {row['rate']:.2f} (ceiling 0.34)")

    mine_names = {row["name"] for row in mine}
    collateral = [f for f in summary["failures"] if not any(f.startswith(name) for name in mine_names)
                  and eval_name not in f]
    print(f"\nstep 7/7  collateral elsewhere in the suite ({len(collateral)})")
    for failure in collateral:
        print(f"  FAIL  {failure}")
    if not collateral:
        print("  ok    nothing else moved")

    print("")
    if summary["exit_code"] == 0:
        print("Verdict: green. The suite passing does not mean the assertion is right; it means the fixtures it has "
              "do not contradict it.")
        return 0
    if pair_row and not pair_row["near_miss_ok"]:
        print("Verdict: red. A near miss that fails more than the assertion it names is a bad fixture, not a bad "
              "assertion: loosening the block to let it through would also let the bad fixture through. Change the "
              "near-miss text, not the assertions.")
    elif collateral:
        print("Verdict: red, and not only here. The assertion change moved fixtures in other pairs; those are listed "
              "in step 7 and are the real cost of the change.")
    else:
        print("Verdict: red. Read step 3: the band a fixture missed says whether the candidate or the assertion is wrong.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("propose", help="write a proposal per labelled disagreement")
    p.add_argument("--iteration", default="iteration-1")
    p.add_argument("--labels", help="override docs/benchmarks/<iteration>/labels.jsonl")
    p.add_argument("--skill", help="only this skill")
    p.add_argument("--eval", help="only this eval name")
    p.add_argument("--out", help="override docs/benchmarks/<iteration>/proposals/")
    p.add_argument("--excerpt-chars", type=int, default=EXCERPT_CHARS)
    p.add_argument("--full-output", action="store_true", help="publish the whole output into the tracked proposal")
    p.add_argument("--force", action="store_true", help="overwrite a proposal a human edited")
    p.add_argument("--dry-run", action="store_true", help="print what would be written, write nothing")
    p.set_defaults(func=propose)
    c = sub.add_parser("check", help="run the grader suite against a pasted candidate and report it step by step")
    c.add_argument("--skill", required=True)
    c.add_argument("--eval", required=True)
    c.add_argument("--timeout", type=int, default=600, help="seconds to allow the suite")
    c.set_defaults(func=check)
    args = parser.parse_args()
    try:
        result = args.func(args)
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"propose_eval_updates: {exc}\n")
    # propose returns its index; check returns the exit code the steps earned.
    return result if isinstance(result, int) else 0


if __name__ == "__main__":
    raise SystemExit(main())
