#!/usr/bin/env python3
"""Run the eval pilot through a harness CLI and record every output with provenance.

For each pilot eval (the skills named in docs/benchmarks/pilot-deps.json) the runner
builds two payloads, without_skill (the manifest prompt, byte for byte) and with_skill
(the prompt preceded by SKILL.md and the listed references, each tagged with its
sha256), runs the harness command in a fresh empty directory outside the repository
with the payload on stdin, parses the harness result, and hands the text to
record_eval_run.record() with the real model, session and timing. A provenance.json
sidecar next to each meta.json keeps argv, harness version, seed, config order,
loaded files and the raw envelope. Nothing here fabricates an output: an empty
result, a failed process, a dirty tree or a mixed iteration stops the run.

What the pilot measures: the effect of an instruction bundle (SKILL.md plus the listed
references) on one response to a fixed prompt, with no tools, no project memory and no
hooks. It does not measure the toolkit at runtime: routing, progressive loading, hooks,
memory and MCP stay out of scope. with_skill is compared against without_skill inside
one harness; two harnesses running different models differ by model, never by harness.

Three guards make the measurement auditable. An isolation probe runs first and records
what the harness reports as available tools and loaded instructions; anything but
"none" stops the run unless --allow-unisolated. Every harness invocation, recorded or
failed, appends one line to docs/benchmarks/<iteration>/attempts.jsonl, so failures
are never dropped from the record. The harness version must be listed under
verified_harness_versions in the dependency manifest, which happens only after a smoke
run (--eval) has parsed that version's envelope; until then a full run is refused.

Usage:
    python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --dry-run
    python3 scripts/run_eval_pilot.py --harness claude-code --iteration iteration-claude-1 --model <model> --seed 7
    python3 scripts/run_eval_pilot.py --harness codex --iteration iteration-codex-1 --model <model> --harness-cmd "<template>"
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import random
import re
import secrets
import shlex
import subprocess
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parents[1]
CONFIGS = ("with_skill", "without_skill")
HARNESSES = ("claude-code", "codex")
DEFAULT_DEPS = Path("docs/benchmarks/pilot-deps.json")
ITERATION_RE = re.compile(r"iteration-[a-z0-9-]+")
# Flags confirmed in `claude -p --help` 2.1.267: --safe-mode disables CLAUDE.md, skills,
# plugins, hooks, MCP servers, commands and agents while keeping auth and model selection;
# --tools "" leaves both configurations with identical (no) tool access. The codex
# template follows the published CLI docs and is verified on the machine that runs it.
DEFAULT_CMDS = {
    "claude-code": 'claude -p --output-format json --model {model} --safe-mode --strict-mcp-config --tools "" --permission-prompts none',
    "codex": "codex exec --json --model {model} --sandbox read-only --ask-for-approval never --skip-git-repo-check --cd {cwd} --output-last-message {output_file} -",
}
PREAMBLE = ("The files below are the skill and its references, loaded for this task. "
            "Apply them. The task follows the last file.")
PROBE_PROMPT = ("Reply with exactly two lines and nothing else.\n"
                "TOOLS: <comma-separated names of the tools you can call in this session, or none>\n"
                "INSTRUCTIONS: <one line naming any project, user or system instructions you were given "
                "before this message, or none>")
PROBE_SCHEMA = 1
PROVENANCE_SCHEMA = 2
CLAUDE_TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
CODEX_TOKEN_FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens")


@dataclass
class HarnessResult:
    text: str
    model: str
    session_id: str
    total_tokens: int | None
    duration_ms: int | None
    model_source: str  # "harness" when the envelope named the model, "flag" when only --model did
    raw: object


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest(root: Path, path: Path) -> dict:
    data = json.loads((root / path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("skills"), dict):
        raise ValueError(f"{path}: expected {{\"schema\": 1, \"skills\": {{...}}}}")
    for skill, files in data["skills"].items():
        if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
            raise ValueError(f"{path}: dependencies of {skill} must be a list of paths")
        for rel in (f"skills/{skill}/SKILL.md", *files):
            if not (root / rel).is_file():
                raise ValueError(f"{path}: {rel} does not exist")
    versions = data.get("verified_harness_versions", {})
    if not isinstance(versions, dict) or any(h not in HARNESSES or not isinstance(v, list) or not all(isinstance(s, str) for s in v)
                                             for h, v in versions.items()):
        raise ValueError(f"{path}: verified_harness_versions must map a harness to a list of version strings")
    return data


def load_deps(root: Path, path: Path) -> dict[str, list[str]]:
    return load_manifest(root, path)["skills"]


def verified_versions(root: Path, path: Path, harness: str) -> list[str]:
    """Versions whose flags and result envelope a smoke run on a pilot machine has parsed.
    The list starts empty for every harness; the runbook says when to add one."""
    return list(load_manifest(root, path).get("verified_harness_versions", {}).get(harness, []))


def pilot_evals(root: Path, deps: dict[str, list[str]], only_skill: str | None = None,
                only_eval: str | None = None) -> list[dict]:
    evals = []
    for skill in deps:
        if only_skill and skill != only_skill:
            continue
        manifest = json.loads((root / "skills" / skill / "evals" / "evals.json").read_text(encoding="utf-8"))
        for entry in manifest["evals"]:
            if only_eval and entry["name"] != only_eval:
                continue
            evals.append({"skill": skill, "id": entry["id"], "name": entry["name"], "prompt": entry["prompt"]})
    if not evals:
        raise ValueError("no pilot eval matched the manifest and filters")
    return evals


def plan_runs(evals: list[dict], seed: int) -> list[tuple[dict, list[str]]]:
    """Randomise which configuration runs first, per eval, from one seed."""
    rng = random.Random(seed)
    plan = []
    for entry in evals:
        order = list(CONFIGS)
        rng.shuffle(order)
        plan.append((entry, order))
    return plan


def build_payload(root: Path, skill: str, prompt: str, config: str,
                  deps: dict[str, list[str]]) -> tuple[str, list[dict]]:
    if config == "without_skill":
        return prompt, []
    loaded, blocks = [], []
    for rel in (f"skills/{skill}/SKILL.md", *deps[skill]):
        data = (root / rel).read_bytes()
        digest = sha256_bytes(data)
        loaded.append({"path": rel, "sha256": digest, "bytes": len(data)})
        blocks.append(f'<file path="{rel}" sha256="{digest}">\n{data.decode("utf-8")}\n</file>')
    return PREAMBLE + "\n\n" + "\n\n".join(blocks) + "\n\n" + prompt, loaded


def harness_argv(template: str, **fields: str) -> list[str]:
    tokens = shlex.split(template, posix=os.name != "nt")
    return [token.format(**fields) for token in tokens]


def executable_prefix(argv: list[str]) -> list[str]:
    """The tokens that identify the harness: the executable, plus the script when the
    command is a script run through a Python interpreter (a wrapper, or the test fake)."""
    prefix = argv[:1]
    if len(argv) > 1 and re.fullmatch(r"python(?:\d(?:\.\d+)?)?(?:\.exe)?", Path(argv[0]).name, re.IGNORECASE):
        prefix = argv[:2]
    return prefix


def harness_version(argv: list[str]) -> str | None:
    try:
        res = subprocess.run([*executable_prefix(argv), "--version"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    out = (res.stdout or res.stderr).strip()
    return out.splitlines()[0] if out else None


def _keep(cwd: Path, name: str, data) -> None:
    if isinstance(data, bytes):
        data = data.decode("utf-8", errors="replace")
    (cwd / name).write_text(data or "", encoding="utf-8")


def run_harness(argv: list[str], payload: str, cwd: Path, timeout: int) -> str:
    """Run the harness once. stdout and stderr are kept in the run directory whether the
    process succeeded or not, so a failed attempt leaves the same evidence as a recorded one."""
    try:
        res = subprocess.run(argv, input=payload, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        _keep(cwd, "harness_stdout.txt", exc.stdout)
        _keep(cwd, "harness_stderr.txt", exc.stderr)
        raise RuntimeError(f"harness timed out after {timeout}s in {cwd}") from exc
    except OSError as exc:
        raise RuntimeError(f"cannot start harness {argv[0]!r}: {exc}") from exc
    _keep(cwd, "harness_stdout.txt", res.stdout)
    _keep(cwd, "harness_stderr.txt", res.stderr)
    if res.returncode != 0:
        raise RuntimeError(f"harness exited {res.returncode} in {cwd}: {res.stderr.strip()[-2000:]}")
    return res.stdout


def attempts_path(root: Path, iteration: str) -> Path:
    return root / "docs" / "benchmarks" / iteration / "attempts.jsonl"


def log_attempt(root: Path, iteration: str, record: dict) -> None:
    """One line per harness invocation, recorded or failed, appended before anything else
    is decided about the result. The file is tracked so the report can state attempts
    against recorded runs; a pilot that hides its failures is not a pilot."""
    path = attempts_path(root, iteration)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"when": datetime.now().astimezone().isoformat(), **record}, sort_keys=True) + "\n")


def probe_dir(root: Path, iteration: str) -> Path:
    return root / "docs" / "benchmarks" / iteration / "probes"


def parse_probe(text: str) -> dict:
    """Exactly two non-empty lines, TOOLS then INSTRUCTIONS, each saying none. An extra
    line, a repeated field, a contradiction or any other shape is not isolated: the probe
    fails closed and records format_ok so the report can tell a bad answer from a bad
    session."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    fields: dict[str, str] = {}
    format_ok = len(lines) == 2
    for index, line in enumerate(lines):
        m = re.match(r"(tools|instructions)\s*:\s*(.*)$", line, re.IGNORECASE)
        name = m.group(1).lower() if m else None
        if not m or name in fields or name != ("tools", "instructions")[min(index, 1)]:
            format_ok = False
        if m and name not in fields:
            fields[name] = m.group(2).strip().strip(".").strip("`'\"").strip()
    isolated = format_ok and set(fields) == {"tools", "instructions"} and all(v.lower() in ("none", "nothing") for v in fields.values())
    return {"tools": fields.get("tools"), "instructions": fields.get("instructions"), "format_ok": format_ok, "isolated": isolated}


def _flag_value(argv: list[str], flag: str) -> str | None:
    return argv[argv.index(flag) + 1] if flag in argv and argv.index(flag) + 1 < len(argv) else None


def isolation_config(harness: str, argv: list[str], cwd: Path, root: Path, env: dict | None = None) -> dict[str, bool]:
    """Explicit, verifiable process configuration: the flags the harness documents for a
    session without customisations, and a working directory outside the repository. This
    is the isolation guarantee; the probe is a diagnostic on top of it, because a model's
    statement about its own tools does not prove what the process loaded."""
    env = os.environ if env is None else env
    outside = not cwd.resolve().is_relative_to(root.resolve())
    if harness == "claude-code":
        return {
            "safe_mode": "--safe-mode" in argv,
            "strict_mcp_config": "--strict-mcp-config" in argv,
            "no_tools": _flag_value(argv, "--tools") == "",
            "no_permission_prompts": _flag_value(argv, "--permission-prompts") == "none",
            "cwd_outside_repo": outside,
        }
    home = env.get("CODEX_HOME")
    home_path = Path(home) if home else None
    clean = bool(home_path and home_path.is_dir() and not any((home_path / name).exists() for name in ("AGENTS.md", "skills", "hooks")))
    return {
        "read_only_sandbox": _flag_value(argv, "--sandbox") == "read-only",
        "skip_git_repo_check": "--skip-git-repo-check" in argv,
        "codex_home_set": bool(home),
        "codex_home_clean": clean,
        "cwd_outside_repo": outside,
    }


def probe_isolation(root: Path, args, template: str, work_dir: Path, version: str | None, attempt: int) -> dict:
    """Ask the harness, through the same argv the runs use, what it can call and what it
    was told before the prompt. Every invocation writes its own probe file under
    docs/benchmarks/<iteration>/probes/ and never overwrites an earlier one, so a sidecar
    that references a probe keeps pointing at evidence that still exists."""
    cwd = work_dir / "isolation-probe" / f"attempt-{attempt:02d}"
    cwd.mkdir(parents=True, exist_ok=False)
    prompt_file = cwd / "prompt.md"
    prompt_file.write_text(PROBE_PROMPT, encoding="utf-8")
    output_file = cwd / "last_message.md"
    argv = harness_argv(template, model=args.model, cwd=str(cwd), prompt_file=str(prompt_file), output_file=str(output_file))
    config = isolation_config(args.harness, argv, cwd, root)
    raw = run_harness(argv, PROBE_PROMPT, cwd, args.timeout)
    result = parse_claude_json(raw, args.model) if args.harness == "claude-code" else parse_codex_jsonl(raw, output_file, args.model)
    probe = {"schema": PROBE_SCHEMA, "harness": args.harness, "harness_version": version, "model": result.model,
             "argv": argv, "prompt": PROBE_PROMPT, "text": result.text, **parse_probe(result.text),
             "isolation_config": config, "checked_at": datetime.now().astimezone().isoformat(), "harness_result": result.raw}
    body = (json.dumps(probe, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    sha = sha256_bytes(body)
    directory = probe_dir(root, args.iteration)
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    path = directory / f"{stamp}-{sha[:8]}.json"
    counter = 2
    while path.exists():
        path = directory / f"{stamp}-{sha[:8]}-{counter}.json"
        counter += 1
    path.write_bytes(body)
    return {"path": path.relative_to(root).as_posix(), "sha256": sha, "isolated": probe["isolated"],
            "format_ok": probe["format_ok"], "isolation_config": config}


def parse_claude_json(raw: str, model_flag: str) -> HarnessResult:
    """`claude -p --output-format json` result envelope (SDK-documented shape; the first
    smoke run on the pilot machine confirms it). Fails loudly on anything else."""
    try:
        envelope = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"claude-code did not return a JSON envelope: {exc}") from exc
    if isinstance(envelope, list):
        envelope = next((e for e in reversed(envelope) if isinstance(e, dict) and e.get("type") == "result"), {})
    if not isinstance(envelope, dict) or envelope.get("type") != "result" or envelope.get("is_error") \
            or envelope.get("subtype") not in (None, "success"):
        raise ValueError("claude-code result is not a successful result envelope: "
                         f"type={envelope.get('type') if isinstance(envelope, dict) else None} "
                         f"subtype={envelope.get('subtype') if isinstance(envelope, dict) else None}")
    text = envelope.get("result") or ""
    if not str(text).strip():
        raise ValueError("harness returned empty output")
    session_id = str(envelope.get("session_id") or "").strip()
    if not session_id:
        raise ValueError("claude-code envelope carries no session_id; the protocol needs an auditable source")
    usage = envelope.get("usage") or {}
    total = sum(int(usage.get(k) or 0) for k in CLAUDE_TOKEN_FIELDS) if isinstance(usage, dict) and usage else None
    model_usage = envelope.get("modelUsage") or {}
    if not isinstance(model_usage, dict) or len(model_usage) != 1:
        raise ValueError(f"claude-code envelope names {len(model_usage) if isinstance(model_usage, dict) else 0} "
                         "models in modelUsage; expected exactly one, so the recorded model is never inferred")
    duration = envelope.get("duration_ms")
    duration = int(duration) if isinstance(duration, (int, float)) else None
    return HarnessResult(str(text), next(iter(model_usage)), session_id, total, duration, "harness", envelope)


def parse_codex_jsonl(raw: str, output_file: Path | None, model_flag: str) -> HarnessResult:
    """`codex exec --json` event stream. The field names follow the published docs and are
    verified on the pilot machine; every mismatch fails instead of guessing."""
    events = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    events = [e for e in events if isinstance(e, dict)]
    thread = next((str(e.get("thread_id")) for e in events if e.get("type") == "thread.started" and e.get("thread_id")), None)
    if not thread:
        raise ValueError("codex stream carries no thread.started event; the protocol needs an auditable source")
    if any(e.get("type") in ("turn.failed", "error") for e in events):
        raise ValueError("codex turn failed (turn.failed or error event in the stream); a partial answer is not a result")
    if not any(e.get("type") == "turn.completed" for e in events):
        raise ValueError("codex stream carries no turn.completed event; an unfinished turn is not a result")
    text = output_file.read_text(encoding="utf-8") if output_file and output_file.is_file() else ""
    if not text.strip():
        for event in reversed(events):
            item = event.get("item")
            if isinstance(item, dict) and item.get("type") == "agent_message" and item.get("text"):
                text = str(item["text"])
                break
    if not text.strip():
        raise ValueError("harness returned empty output")
    usage = next((e.get("usage") for e in reversed(events) if e.get("type") == "turn.completed" and isinstance(e.get("usage"), dict)), None)
    total = sum(int(usage.get(k) or 0) for k in CODEX_TOKEN_FIELDS) if usage else None
    model = next((e.get("model") for e in events if isinstance(e.get("model"), str) and e.get("model")), None)
    return HarnessResult(text, model or model_flag, thread, total, None, "harness" if model else "flag", events)


def existing_identity(root: Path, iteration: str) -> tuple[str, str] | None:
    for meta_path in sorted((root / "skills").glob(f"*/workspace/{iteration}/eval-*/*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return str(meta.get("harness")), str(meta.get("model"))
    return None


def dirty_tree(root: Path, paths: list[str]) -> list[str]:
    res = subprocess.run(["git", "status", "--porcelain", "--", *paths], cwd=root, capture_output=True, text=True)
    return [line for line in res.stdout.splitlines() if line.strip() and "/workspace/" not in line]


def run_target(root: Path, iteration: str, entry: dict, config: str) -> Path:
    return root / "skills" / entry["skill"] / "workspace" / iteration / f"eval-{entry['id']}-{entry['name']}" / config


def record_result(root: Path, args, entry: dict, config: str, result: HarnessResult, payload: str,
                  loaded: list[dict], order: list[str], argv: list[str], version: str | None,
                  seed: int, cwd: Path, probe: dict | None = None) -> Path:
    import record_eval_run as rr
    output = cwd / "output.md"
    output.write_text(result.text, encoding="utf-8")
    kind = "thread" if args.harness == "codex" else "session"
    namespace = types.SimpleNamespace(
        skill=entry["skill"], eval=entry["name"], config=config, iteration=args.iteration,
        harness=args.harness, model=result.model, source=f"{args.harness} {kind} {result.session_id}",
        output=output, tokens=result.total_tokens, duration_ms=result.duration_ms)
    target = rr.record(namespace, root)
    provenance = {
        "schema": PROVENANCE_SCHEMA, "runner": "scripts/run_eval_pilot.py", "harness": args.harness,
        "harness_version": version, "argv": argv, "cwd": str(cwd), "seed": seed,
        "config_order": order, "model_source": result.model_source,
        "payload_sha256": sha256_bytes(payload.encode("utf-8")), "payload": payload,
        "output_sha256": sha256_bytes(result.text.encode("utf-8")),
        "loaded_files": loaded, "harness_result": result.raw,
        "isolation_probe": None if probe is None else {k: probe[k] for k in ("path", "sha256", "isolated", "format_ok")},
        "isolation_config": None if probe is None else probe["isolation_config"],
        "skip_probe": probe is None,
    }
    (target / "provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                                            encoding="utf-8")
    return target


def run_pilot(args, root: Path = ROOT) -> list[Path]:
    if args.harness not in HARNESSES:
        raise ValueError(f"unsupported harness {args.harness!r}")
    if not ITERATION_RE.fullmatch(args.iteration):
        raise ValueError("iteration must match iteration-[a-z0-9-]+")
    if not str(args.model).strip():
        raise ValueError("--model must not be empty")
    deps_path = Path(args.deps)
    deps = load_deps(root, deps_path)
    evals = pilot_evals(root, deps, args.skill, args.eval)
    seed = args.seed if args.seed is not None else secrets.randbits(32)
    template = args.harness_cmd or DEFAULT_CMDS[args.harness]
    identity = existing_identity(root, args.iteration)
    if identity and identity[0] != args.harness:
        raise ValueError(f"iteration {args.iteration} already holds {identity[0]} runs; use a new iteration")
    if identity and args.harness == "codex" and identity[1] != args.model:
        raise ValueError(f"iteration {args.iteration} was recorded with model {identity[1]}, not {args.model}")
    if not args.allow_dirty:
        dirty = dirty_tree(root, ["skills", str(deps_path)])
        if dirty:
            raise ValueError("uncommitted changes under skills/ or the deps manifest; commit them or pass --allow-dirty: "
                             + "; ".join(dirty[:5]))
    planned = []
    for entry, order in plan_runs(evals, seed):
        for config in order:
            target = run_target(root, args.iteration, entry, config)
            if target.exists():
                if args.skip_recorded:
                    continue
                raise ValueError(f"run already recorded: {target.relative_to(root).as_posix()}; "
                                 "use --skip-recorded to resume or a new iteration")
            planned.append((entry, config, order))
    if args.dry_run:
        for entry, config, order in planned:
            payload, _loaded = build_payload(root, entry["skill"], entry["prompt"], config, deps)
            argv = harness_argv(template, model=args.model, cwd="<cwd>", prompt_file="<prompt_file>", output_file="<output_file>")
            print(f"{entry['skill']} eval-{entry['id']}-{entry['name']} {config} order={'>'.join(order)} "
                  f"payload={len(payload.encode('utf-8'))}B sha256={sha256_bytes(payload.encode('utf-8'))[:12]} argv={shlex.join(argv)}")
        print(f"seed={seed}; {len(planned)} run(s) planned, nothing executed")
        return []
    work_dir = Path(args.work_dir) if args.work_dir else Path(tempfile.mkdtemp(prefix="pilot-"))
    work_dir.mkdir(parents=True, exist_ok=True)
    version = harness_version(harness_argv(template, model=args.model, cwd="", prompt_file="", output_file=""))
    if version not in verified_versions(root, deps_path, args.harness):
        message = (f"harness version {version!r} is not listed under verified_harness_versions for {args.harness} in "
                   f"{deps_path}; run one --eval smoke, confirm the envelope parsed, then add the version")
        if not (args.eval or getattr(args, "allow_unverified", False)):
            raise ValueError(message)
        print(f"WARN {message}", file=sys.stderr)
    probe = None
    if not getattr(args, "skip_probe", False):
        probe_attempt = 1 + len(list((work_dir / "isolation-probe").glob("attempt-*"))) if (work_dir / "isolation-probe").exists() else 1
        probe = probe_isolation(root, args, template, work_dir, version, probe_attempt)
        failed_checks = sorted(name for name, ok in probe["isolation_config"].items() if not ok)
        if failed_checks:
            message = (f"isolation configuration incomplete for {args.harness}: {', '.join(failed_checks)}; see {probe['path']}. "
                       "Fix the template, CODEX_HOME or the working directory, or pass --allow-unisolated to record anyway")
            if not getattr(args, "allow_unisolated", False):
                raise ValueError(message)
            print(f"WARN {message}", file=sys.stderr)
        if not probe["isolated"]:
            message = (f"isolation probe reports tools or instructions, or answered in another shape; see {probe['path']}. "
                       "Fix the isolation (flags, CODEX_HOME, working directory) or pass --allow-unisolated to record anyway")
            if not getattr(args, "allow_unisolated", False):
                raise ValueError(message)
            print(f"WARN {message}", file=sys.stderr)
    recorded = []
    for entry, config, order in planned:
        # One directory per attempt: a resume after a failure never overwrites the
        # evidence the failed attempt left behind.
        base = work_dir / f"{entry['skill']}-{entry['id']}-{config}"
        attempt_no = 1 + len(list(base.glob("attempt-*"))) if base.exists() else 1
        cwd = base / f"attempt-{attempt_no:02d}"
        cwd.mkdir(parents=True, exist_ok=False)
        payload, loaded = build_payload(root, entry["skill"], entry["prompt"], config, deps)
        prompt_file = cwd / "prompt.md"
        prompt_file.write_text(payload, encoding="utf-8")
        output_file = cwd / "last_message.md"
        argv = harness_argv(template, model=args.model, cwd=str(cwd), prompt_file=str(prompt_file), output_file=str(output_file))
        attempt = {"harness": args.harness, "skill": entry["skill"], "eval_id": entry["id"], "eval_name": entry["name"],
                   "config": config, "attempt": attempt_no, "seed": seed, "cwd": str(cwd), "harness_version": version}
        try:
            raw = run_harness(argv, payload, cwd, args.timeout)
            result = parse_claude_json(raw, args.model) if args.harness == "claude-code" else parse_codex_jsonl(raw, output_file, args.model)
            if identity is None:
                identity = (args.harness, result.model)
            elif result.model != identity[1]:
                raise ValueError(f"model changed inside the iteration: {identity[1]} then {result.model}; stop and use a new iteration")
            target = record_result(root, args, entry, config, result, payload, loaded, order, argv, version, seed, cwd, probe)
        except (RuntimeError, ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
            stdout = cwd / "harness_stdout.txt"
            log_attempt(root, args.iteration, {**attempt, "status": "failed", "error": str(exc)[:500],
                                                "stdout_sha256": sha256_bytes(stdout.read_bytes()) if stdout.exists() else None})
            raise
        log_attempt(root, args.iteration, {**attempt, "status": "recorded", "error": None, "model": result.model,
                                            "stdout_sha256": sha256_bytes((cwd / "harness_stdout.txt").read_bytes()),
                                            "output_sha256": sha256_bytes(result.text.encode("utf-8"))})
        recorded.append(target)
        print(f"recorded {target.relative_to(root).as_posix()} model={result.model} tokens={result.total_tokens}")
    print(f"seed={seed}; {len(recorded)} run(s) recorded in {args.iteration}; attempts in {attempts_path(root, args.iteration).relative_to(root).as_posix()}")
    return recorded


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--harness", required=True, choices=HARNESSES)
    p.add_argument("--iteration", required=True)
    p.add_argument("--model", required=True, help="model to request; the recorded model comes from the harness result when it names one")
    p.add_argument("--seed", type=int, help="seed for the per-eval configuration order; random and printed when omitted")
    p.add_argument("--harness-cmd", help="command template; placeholders {model} {cwd} {prompt_file} {output_file}; the payload also arrives on stdin")
    p.add_argument("--deps", default=str(DEFAULT_DEPS), help="dependency manifest listing the pilot skills and the files loaded with the skill")
    p.add_argument("--skill", help="run one pilot skill only")
    p.add_argument("--eval", help="run one eval name only (smoke run)")
    p.add_argument("--dry-run", action="store_true", help="print the plan and the argv; execute nothing")
    p.add_argument("--skip-recorded", action="store_true", help="resume an interrupted iteration; recorded runs are skipped, never overwritten")
    p.add_argument("--allow-dirty", action="store_true", help="run with uncommitted changes under skills/ (the recorded commit will not describe the payload)")
    p.add_argument("--timeout", type=int, default=900, help="seconds per harness run")
    p.add_argument("--skip-probe", action="store_true", help="do not run the isolation probe first (the provenance records the gap)")
    p.add_argument("--allow-unisolated", action="store_true", help="record even when the probe reports tools or instructions in the session")
    p.add_argument("--allow-unverified", action="store_true", help="run a full iteration on a harness version not yet listed in verified_harness_versions")
    p.add_argument("--work-dir", help="parent directory for the per-run working directories; a fresh temporary directory outside the repo by default")
    args = p.parse_args()
    try:
        run_pilot(args)
    except (ValueError, RuntimeError, OSError, KeyError, json.JSONDecodeError) as exc:
        p.exit(1, f"run_eval_pilot: {exc}\n")


if __name__ == "__main__":
    main()
