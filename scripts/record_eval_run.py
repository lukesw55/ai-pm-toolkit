#!/usr/bin/env python3
"""Record an externally executed eval with provenance; never generates model output."""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'[a-z0-9][a-z0-9-]*')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def eval_spec(root, skill, name):
    if not TOKEN.fullmatch(skill) or not TOKEN.fullmatch(name):
        raise ValueError('invalid skill or eval name')
    manifest = json.loads((root/'skills'/skill/'evals/evals.json').read_text(encoding='utf-8'))
    matches = [e for e in manifest['evals'] if e['name'] == name]
    if len(matches) != 1:
        raise ValueError('eval name must resolve to exactly one manifest entry')
    return matches[0]


def validate_run(directory, skill, spec, config):
    meta = json.loads((directory/'meta.json').read_text(encoding='utf-8'))
    output = (directory/'outputs/output.md').read_bytes()
    if not isinstance(meta,dict):
        raise ValueError('metadata must be an object')
    for key, value in {'schema':1,'skill':skill,'eval_id':spec['id'],'eval_name':spec['name'],'config':config,'prompt_sha256':digest(spec['prompt'].encode()),'output_sha256':digest(output)}.items():
        if meta.get(key) != value:
            raise ValueError(f'metadata mismatch: {key}')
    for key in ('model','source','repo_commit','skill_sha256'):
        if not isinstance(meta.get(key),str) or not meta[key].strip():
            raise ValueError(f'missing provenance: {key}')
    if meta.get('harness') not in ('claude-code','codex'):
        raise ValueError('unsupported harness')
    if not re.fullmatch('[a-f0-9]{40}',meta['repo_commit']) or not re.fullmatch('[a-f0-9]{64}',meta['skill_sha256']):
        raise ValueError('invalid provenance hashes')
    stamp=datetime.fromisoformat(meta.get('recorded_at',''))
    if stamp.tzinfo is None:
        raise ValueError('recorded_at must include timezone')
    for key in ('total_tokens','duration_ms'):
        if meta.get(key) is not None and (type(meta[key]) is not int or meta[key]<0):
            raise ValueError(f'{key} must be a nonnegative integer or null')
    if not output.decode('utf-8').strip():
        raise ValueError('output must be nonempty UTF-8')
    sidecar = directory/'provenance.json'
    if sidecar.exists():
        # The runner's sidecar is evidence only while it describes this run: same output,
        # a payload that hashes to what it claims, and the SKILL.md the meta names.
        prov = json.loads(sidecar.read_text(encoding='utf-8'))
        if not isinstance(prov, dict):
            raise ValueError('provenance sidecar must be an object')
        if prov.get('output_sha256') != meta['output_sha256']:
            raise ValueError('provenance sidecar mismatch: output_sha256')
        payload = prov.get('payload')
        if not isinstance(payload, str) or digest(payload.encode('utf-8')) != prov.get('payload_sha256'):
            raise ValueError('provenance sidecar mismatch: payload_sha256')
        loaded = prov.get('loaded_files')
        if not isinstance(loaded, list):
            raise ValueError('provenance sidecar mismatch: loaded_files')
        if config == 'with_skill':
            first = loaded[0] if loaded and isinstance(loaded[0], dict) else {}
            if first.get('path') != f'skills/{skill}/SKILL.md' or first.get('sha256') != meta['skill_sha256']:
                raise ValueError('provenance sidecar mismatch: loaded SKILL.md')
        elif loaded:
            raise ValueError('provenance sidecar mismatch: without_skill lists loaded files')
        probe = prov.get('isolation_probe')
        if probe is None:
            if prov.get('skip_probe') is not True:
                raise ValueError('provenance sidecar mismatch: isolation probe missing without skip_probe')
        else:
            # The referenced probe is evidence only while it exists with the recorded hash.
            resolved = directory.resolve()
            if len(resolved.parents) < 6 or resolved.parents[4].name != 'skills' or resolved.parents[2].name != 'workspace':
                raise ValueError('run directory is not <root>/skills/<skill>/workspace/<iteration>/<eval>/<config>')
            root = resolved.parents[5]
            if not isinstance(probe, dict) or not isinstance(probe.get('path'), str) or not isinstance(probe.get('sha256'), str):
                raise ValueError('provenance sidecar mismatch: isolation probe reference')
            probe_file = root/probe['path']
            if not probe_file.resolve().is_relative_to(root) or not probe_file.is_file():
                raise ValueError('provenance sidecar mismatch: isolation probe file missing')
            if digest(probe_file.read_bytes()) != probe['sha256']:
                raise ValueError('provenance sidecar mismatch: isolation probe hash')
            recorded = json.loads(probe_file.read_text(encoding='utf-8'))
            if not isinstance(recorded, dict) or recorded.get('isolated') != probe.get('isolated') or recorded.get('harness') != meta['harness']:
                raise ValueError('provenance sidecar mismatch: isolation probe content')
    return meta


def record(args, root=ROOT):
    spec=eval_spec(root,args.skill,args.eval)
    if not re.fullmatch(r'iteration-[a-z0-9-]+',args.iteration):
        raise ValueError('iteration must start with iteration- and contain lowercase letters, digits or hyphens')
    base=root/'skills'/args.skill/'workspace'/args.iteration
    target=base/f"eval-{spec['id']}-{spec['name']}"/args.config
    if target.resolve()!=target.absolute():
        raise ValueError('record destination must not traverse symlinks')
    if target.exists():
        raise ValueError('run already exists; use a new iteration, never overwrite a recorded run')
    output=Path(args.output).read_bytes()
    meta={'schema':1,'skill':args.skill,'eval_id':spec['id'],'eval_name':spec['name'],'config':args.config,
          'harness':args.harness,'model':args.model,'source':args.source,
          'recorded_at':datetime.now().astimezone().isoformat(),
          'repo_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
          'skill_sha256':digest((root/'skills'/args.skill/'SKILL.md').read_bytes()),
          'prompt_sha256':digest(spec['prompt'].encode()),'output_sha256':digest(output),
          'total_tokens':args.tokens,'duration_ms':args.duration_ms}
    target.parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix='.record-',dir=target.parent))
    try:
        (staging/'outputs').mkdir()
        (staging/'outputs/output.md').write_bytes(output)
        (staging/'meta.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
        (staging/'timing.json').write_text(json.dumps({'total_tokens':args.tokens,'duration_ms':args.duration_ms}),encoding='utf-8')
        validate_run(staging,args.skill,spec,args.config)
        # mkdir reserves this run; a second recorder cannot replace an existing one.
        target.mkdir()
        for child in staging.iterdir():
            os.replace(child,target/child.name)
    finally:
        shutil.rmtree(staging)
    return target


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('skill');p.add_argument('eval')
    p.add_argument('--config',required=True,choices=('with_skill','without_skill'))
    p.add_argument('--iteration',required=True)
    p.add_argument('--harness',required=True,choices=('claude-code','codex'))
    p.add_argument('--model',required=True)
    p.add_argument('--source',required=True,help='actual session/transcript identifier, never a synthetic fixture')
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--tokens',type=int)
    p.add_argument('--duration-ms',type=int)
    args=p.parse_args()
    try:
        print(record(args))
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as exc:
        p.exit(1,f'record_eval_run: {exc}\n')


if __name__=='__main__':
    main()
