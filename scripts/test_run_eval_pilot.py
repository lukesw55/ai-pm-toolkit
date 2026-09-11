"""Pilot runner regressions with a fake harness: no real CLI, no model, no network."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import grade_evals as ge
import record_eval_run as rr
import run_eval_pilot as rp

FAKE_HARNESS = r'''
import hashlib, json, os, sys
if "--version" in sys.argv:
    print("fake 0.0"); sys.exit(0)
payload = sys.stdin.read()
last = payload.rstrip().splitlines()[-1] if payload.strip() else ""
if payload.startswith("Reply with exactly two lines"):
    text = "TOOLS: Bash, Read\nINSTRUCTIONS: a CLAUDE.md was loaded" if os.environ.get("FAKE_UNISOLATED") else "TOOLS: none\nINSTRUCTIONS: none"
else:
    text = "" if os.environ.get("FAKE_EMPTY") else "Deterministic fake answer for: " + last[:60]
if os.environ.get("FAKE_FORMAT") == "codex":
    events = [{"type": "thread.started", "thread_id": "fake-thread"},
              {"type": "item.completed", "item": {"type": "agent_message", "text": text}},
              {"type": "turn.completed", "usage": {"input_tokens": 10, "cached_input_tokens": 0, "output_tokens": 5}}]
    for event in events:
        print(json.dumps(event))
else:
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": text,
                      "session_id": "fake-" + hashlib.sha256(payload.encode()).hexdigest()[:8],
                      "duration_ms": 12,
                      "usage": {"input_tokens": 10, "output_tokens": 5, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0},
                      "modelUsage": {"fake-model-1": {"inputTokens": 10, "outputTokens": 5}}}))
'''


class PilotRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        deps = json.loads((rp.ROOT / 'docs/benchmarks/pilot-deps.json').read_text(encoding='utf-8'))
        self.skills = list(deps['skills'])
        for skill in self.skills:
            shutil.copytree(rp.ROOT / 'skills' / skill, self.root / 'skills' / skill, ignore=shutil.ignore_patterns('workspace', '__pycache__'))
        shutil.copy(rp.ROOT / 'skills/DOCTRINE.md', self.root / 'skills/DOCTRINE.md')
        (self.root / 'docs/benchmarks').mkdir(parents=True)
        manifest = json.loads((rp.ROOT / 'docs/benchmarks/pilot-deps.json').read_text(encoding='utf-8'))
        manifest['verified_harness_versions'] = {'claude-code': ['fake 0.0'], 'codex': ['fake 0.0']}
        (self.root / 'docs/benchmarks/pilot-deps.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '-A'], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture'], check=True)
        self.fake = Path(self.tmp.name) / 'fake_harness.py'; self.fake.write_text(FAKE_HARNESS)
        # The fake ignores the isolation flags; the runner's configuration check reads them.
        self.template = f'{sys.executable} {self.fake} -p --output-format json --model {{model}} --safe-mode --strict-mcp-config --tools "" --permission-prompts none'
        self.codex_template = f'{sys.executable} {self.fake} exec --json --model {{model}} --sandbox read-only --skip-git-repo-check'
        self.codex_home = Path(self.tmp.name) / 'codex-home'; self.codex_home.mkdir(); (self.codex_home / 'auth.json').write_text('{}')
        self.args = argparse.Namespace(harness='claude-code', iteration='iteration-fake', model='fake-model-1', seed=7,
                                       harness_cmd=self.template, deps='docs/benchmarks/pilot-deps.json', skill=None, eval=None,
                                       dry_run=False, skip_recorded=False, allow_dirty=False, timeout=60,
                                       work_dir=str(Path(self.tmp.name) / 'work'),
                                       skip_probe=False, allow_unisolated=False, allow_unverified=False)

    def metas(self):
        return sorted(self.root.glob('skills/*/workspace/iteration-fake/eval-*/*/meta.json'))

    def attempts(self):
        path = rp.attempts_path(self.root, 'iteration-fake')
        return [json.loads(l) for l in path.read_text().splitlines() if l.strip()] if path.exists() else []

    def unlist_version(self):
        path = self.root / 'docs/benchmarks/pilot-deps.json'
        manifest = json.loads(path.read_text()); manifest['verified_harness_versions'] = {'claude-code': [], 'codex': []}
        path.write_text(json.dumps(manifest, indent=2) + '\n')
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qam', 'unlist'], check=True)

    def test_records_every_pilot_run_with_provenance(self):
        recorded = rp.run_pilot(self.args, self.root)
        deps = rp.load_deps(self.root, Path(self.args.deps))
        expected = 2 * len(rp.pilot_evals(self.root, deps))
        self.assertEqual(len(recorded), expected); self.assertEqual(len(self.metas()), expected)
        for meta_path in self.metas():
            meta = json.loads(meta_path.read_text()); prov = json.loads((meta_path.parent / 'provenance.json').read_text())
            self.assertEqual(meta['model'], 'fake-model-1'); self.assertEqual(meta['harness'], 'claude-code')
            self.assertTrue(meta['source'].startswith('claude-code session fake-')); self.assertEqual(meta['total_tokens'], 15)
            self.assertEqual(prov['seed'], 7); self.assertEqual(prov['model_source'], 'harness'); self.assertEqual(prov['harness_version'], 'fake 0.0')
            self.assertEqual(sorted(prov['config_order']), ['with_skill', 'without_skill'])
            self.assertEqual(prov['output_sha256'], meta['output_sha256']); self.assertEqual(prov['schema'], rp.PROVENANCE_SCHEMA)
            self.assertTrue(prov['isolation_probe']['isolated']); self.assertTrue(prov['isolation_probe']['path'].startswith('docs/benchmarks/iteration-fake/probes/'))
            self.assertTrue(all(prov['isolation_config'].values()), prov['isolation_config']); self.assertFalse(prov['skip_probe'])
            spec = rr.eval_spec(self.root, meta['skill'], meta['eval_name'])
            self.assertEqual(rr.validate_run(meta_path.parent, meta['skill'], spec, meta['config'])['output_sha256'], meta['output_sha256'])
            if meta['config'] == 'with_skill':
                self.assertEqual(prov['loaded_files'][0]['path'], f"skills/{meta['skill']}/SKILL.md")
                for entry in prov['loaded_files']:
                    self.assertEqual(entry['sha256'], hashlib.sha256((self.root / entry['path']).read_bytes()).hexdigest())
                self.assertTrue(prov['payload'].endswith(spec['prompt']))
            else:
                self.assertEqual(prov['loaded_files'], []); self.assertEqual(prov['payload'], spec['prompt'])
        with patch.object(ge, 'REPO', self.root), patch.object(ge, 'SKILLS_DIR', self.root / 'skills'):
            runs = ge.grade_all('iteration-fake')
            benchmark = ge.aggregate_benchmark(runs, 'iteration-fake')
        self.assertEqual(benchmark['overall']['n_evals'], expected // 2)
        probes = sorted(rp.probe_dir(self.root, 'iteration-fake').glob('*.json')); self.assertEqual(len(probes), 1)
        probe = json.loads(probes[0].read_text())
        self.assertTrue(probe['isolated']); self.assertTrue(probe['format_ok']); self.assertEqual(probe['tools'], 'none'); self.assertEqual(probe['harness_version'], 'fake 0.0')
        attempts = self.attempts()
        self.assertEqual(len(attempts), expected); self.assertEqual({a['status'] for a in attempts}, {'recorded'})
        self.assertTrue(all(a['output_sha256'] and a['stdout_sha256'] and a['when'] for a in attempts))

    def test_config_order_is_seeded(self):
        deps = rp.load_deps(self.root, Path(self.args.deps)); evals = rp.pilot_evals(self.root, deps)
        orders7 = [order for _e, order in rp.plan_runs(evals, 7)]
        self.assertEqual(orders7, [order for _e, order in rp.plan_runs(evals, 7)])
        self.assertNotEqual(orders7, [order for _e, order in rp.plan_runs(evals, 8)])
        self.assertEqual({tuple(o) for o in orders7}, {('with_skill', 'without_skill'), ('without_skill', 'with_skill')})

    def test_refuses_empty_output_and_records_nothing(self):
        with patch.dict(os.environ, {'FAKE_EMPTY': '1'}):
            with self.assertRaisesRegex(ValueError, 'empty'): rp.run_pilot(self.args, self.root)
        self.assertEqual(self.metas(), [])
        attempts = self.attempts()
        self.assertEqual(len(attempts), 1); self.assertEqual(attempts[0]['status'], 'failed'); self.assertIn('empty', attempts[0]['error'])
        self.assertTrue((Path(attempts[0]['cwd']) / 'harness_stdout.txt').exists()); self.assertTrue((Path(attempts[0]['cwd']) / 'harness_stderr.txt').exists())

    def test_isolation_probe_fails_closed(self):
        with patch.dict(os.environ, {'FAKE_UNISOLATED': '1'}):
            with self.assertRaisesRegex(ValueError, 'isolation probe'): rp.run_pilot(self.args, self.root)
            self.assertEqual(self.metas(), []); self.assertEqual(self.attempts(), [])
            probes = sorted(rp.probe_dir(self.root, 'iteration-fake').glob('*.json')); self.assertEqual(len(probes), 1)
            probe = json.loads(probes[0].read_text())
            self.assertFalse(probe['isolated']); self.assertEqual(probe['tools'], 'Bash, Read')
            self.args.allow_unisolated = True; self.args.skill = self.skills[2]
            recorded = rp.run_pilot(self.args, self.root)
        self.assertTrue(recorded)
        prov = json.loads((recorded[0] / 'provenance.json').read_text()); self.assertFalse(prov['isolation_probe']['isolated'])
        self.assertEqual(len(list(rp.probe_dir(self.root, 'iteration-fake').glob('*.json'))), 2)
        self.assertTrue(rp.parse_probe('TOOLS: none.\nINSTRUCTIONS: None')['isolated'])
        for text in ('I have no tools.', 'TOOLS: none\nINSTRUCTIONS: none\nTOOLS: Bash\nINSTRUCTIONS: global instructions',
                     'INSTRUCTIONS: none\nTOOLS: none', 'TOOLS: none\nINSTRUCTIONS: none\nThat is all.', 'TOOLS: none'):
            with self.subTest(text=text):
                parsed = rp.parse_probe(text); self.assertFalse(parsed['isolated']); self.assertFalse(parsed['format_ok'])

    def test_configuration_checks_refuse_an_unsafe_template(self):
        self.args.harness_cmd = f'{sys.executable} {self.fake} --model {{model}}'
        with self.assertRaisesRegex(ValueError, 'isolation configuration incomplete.*safe_mode'): rp.run_pilot(self.args, self.root)
        self.assertEqual(self.metas(), [])
        self.args.allow_unisolated = True; self.args.skill = self.skills[2]
        recorded = rp.run_pilot(self.args, self.root)
        prov = json.loads((recorded[0] / 'provenance.json').read_text())
        self.assertFalse(prov['isolation_config']['safe_mode']); self.assertTrue(prov['isolation_config']['cwd_outside_repo'])
        config = rp.isolation_config('codex', ['codex', 'exec', '--sandbox', 'read-only', '--skip-git-repo-check'], Path(self.tmp.name) / 'w', self.root, {'CODEX_HOME': str(self.codex_home)})
        self.assertTrue(all(config.values()), config)
        (self.codex_home / 'AGENTS.md').write_text('loaded instructions')
        self.assertFalse(rp.isolation_config('codex', ['codex', 'exec', '--sandbox', 'read-only', '--skip-git-repo-check'], Path(self.tmp.name) / 'w', self.root, {'CODEX_HOME': str(self.codex_home)})['codex_home_clean'])

    def test_probe_is_immutable_per_invocation_and_bound_to_validation(self):
        self.args.skill = self.skills[1]
        first = rp.run_pilot(self.args, self.root)
        self.args.skill = self.skills[2]; self.args.skip_recorded = True
        second = rp.run_pilot(self.args, self.root)
        probes = sorted(rp.probe_dir(self.root, 'iteration-fake').glob('*.json')); self.assertEqual(len(probes), 2)
        for target in (*first, *second):
            meta = json.loads((target / 'meta.json').read_text()); spec = rr.eval_spec(self.root, meta['skill'], meta['eval_name'])
            rr.validate_run(target, meta['skill'], spec, meta['config'])
        prov_first = json.loads((first[0] / 'provenance.json').read_text()); prov_second = json.loads((second[0] / 'provenance.json').read_text())
        self.assertNotEqual(prov_first['isolation_probe']['path'], prov_second['isolation_probe']['path'])
        target = first[0]; meta = json.loads((target / 'meta.json').read_text()); spec = rr.eval_spec(self.root, meta['skill'], meta['eval_name'])
        probe_file = self.root / prov_first['isolation_probe']['path']; original = probe_file.read_bytes()
        probe_file.write_bytes(original.replace(b'"isolated": true', b'"isolated": false'))
        with self.assertRaisesRegex(ValueError, 'isolation probe hash'): rr.validate_run(target, meta['skill'], spec, meta['config'])
        probe_file.unlink()
        with self.assertRaisesRegex(ValueError, 'isolation probe file missing'): rr.validate_run(target, meta['skill'], spec, meta['config'])
        probe_file.write_bytes(original)
        rr.validate_run(target, meta['skill'], spec, meta['config'])
        sidecar = target / 'provenance.json'; prov = json.loads(sidecar.read_text()); prov['isolation_probe'] = None; sidecar.write_text(json.dumps(prov))
        with self.assertRaisesRegex(ValueError, 'isolation probe missing'): rr.validate_run(target, meta['skill'], spec, meta['config'])

    def test_unverified_version_refused_unless_smoke(self):
        self.unlist_version()
        with self.assertRaisesRegex(ValueError, 'verified_harness_versions'): rp.run_pilot(self.args, self.root)
        self.assertEqual(self.metas(), [])
        skill = self.skills[2]; name = json.loads((self.root / 'skills' / skill / 'evals/evals.json').read_text())['evals'][0]['name']
        self.args.skill = skill; self.args.eval = name
        self.assertEqual(len(rp.run_pilot(self.args, self.root)), 2)
        self.args.eval = None; self.args.skip_recorded = True; self.args.allow_unverified = True
        self.assertTrue(rp.run_pilot(self.args, self.root))

    def test_sidecar_is_bound_to_validation(self):
        self.args.skill = self.skills[2]
        recorded = rp.run_pilot(self.args, self.root)
        target = next(t for t in recorded if t.name == 'with_skill')
        meta = json.loads((target / 'meta.json').read_text()); spec = rr.eval_spec(self.root, meta['skill'], meta['eval_name'])
        rr.validate_run(target, meta['skill'], spec, 'with_skill')
        sidecar = target / 'provenance.json'; original = sidecar.read_text()
        for field, value, message in (('output_sha256', 'a' * 64, 'output_sha256'), ('payload', 'edited payload', 'payload_sha256'), ('loaded_files', [], 'SKILL.md')):
            prov = json.loads(original); prov[field] = value; sidecar.write_text(json.dumps(prov))
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, message): rr.validate_run(target, meta['skill'], spec, 'with_skill')
        sidecar.write_text(original)
        rr.validate_run(target, meta['skill'], spec, 'with_skill')

    def test_refuses_mixed_harness_before_running(self):
        output = self.root / 'seed.md'; output.write_text('Synthetic pipeline fixture; not model evidence.')
        skill = self.skills[0]; name = json.loads((self.root / 'skills' / skill / 'evals/evals.json').read_text())['evals'][0]['name']
        rr.record(argparse.Namespace(skill=skill, eval=name, config='with_skill', iteration='iteration-fake', harness='codex', model='other',
                                     source='synthetic-test-only', output=output, tokens=None, duration_ms=None), self.root)
        with self.assertRaisesRegex(ValueError, 'already holds'): rp.run_pilot(self.args, self.root)
        self.assertEqual(list(self.root.glob('skills/*/workspace/**/provenance.json')), [])

    def test_refuses_recorded_run_unless_skipping(self):
        self.args.skill = self.skills[1]
        first = rp.run_pilot(self.args, self.root)
        with self.assertRaisesRegex(ValueError, 'already recorded'): rp.run_pilot(self.args, self.root)
        self.args.skip_recorded = True
        self.assertEqual(rp.run_pilot(self.args, self.root), [])
        self.assertEqual(len(self.metas()), len(first))

    def test_refuses_dirty_tree(self):
        (self.root / 'skills' / self.skills[0] / 'SKILL.md').write_text('edited after commit')
        with self.assertRaisesRegex(ValueError, 'uncommitted'): rp.run_pilot(self.args, self.root)
        self.args.allow_dirty = True; self.args.skill = self.skills[2]
        self.assertTrue(rp.run_pilot(self.args, self.root))

    def test_dry_run_writes_nothing(self):
        self.args.dry_run = True
        self.assertEqual(rp.run_pilot(self.args, self.root), [])
        self.assertEqual(list(self.root.glob('skills/*/workspace')), [])
        self.assertFalse((Path(self.tmp.name) / 'work').exists())
        self.assertFalse(rp.attempts_path(self.root, 'iteration-fake').exists()); self.assertFalse(rp.probe_dir(self.root, 'iteration-fake').exists())

    def test_codex_event_stream_parsed(self):
        skill = self.skills[1]; name = json.loads((self.root / 'skills' / skill / 'evals/evals.json').read_text())['evals'][0]['name']
        self.args.harness = 'codex'; self.args.model = 'fake-codex'; self.args.skill = skill; self.args.eval = name
        self.args.harness_cmd = self.codex_template
        with patch.dict(os.environ, {'FAKE_FORMAT': 'codex', 'CODEX_HOME': str(self.codex_home)}):
            recorded = rp.run_pilot(self.args, self.root)
        self.assertEqual(len(recorded), 2)
        for target in recorded:
            meta = json.loads((target / 'meta.json').read_text()); prov = json.loads((target / 'provenance.json').read_text())
            self.assertEqual(meta['model'], 'fake-codex'); self.assertEqual(meta['source'], 'codex thread fake-thread')
            self.assertEqual(meta['total_tokens'], 15); self.assertEqual(prov['model_source'], 'flag')

    def test_rejects_bad_envelopes(self):
        with self.assertRaisesRegex(ValueError, 'JSON'): rp.parse_claude_json('not json', 'm')
        with self.assertRaisesRegex(ValueError, 'not a successful'): rp.parse_claude_json(json.dumps({'type': 'result', 'is_error': True}), 'm')
        with self.assertRaisesRegex(ValueError, 'exactly one'): rp.parse_claude_json(json.dumps({'type': 'result', 'result': 'x', 'session_id': 's', 'modelUsage': {}}), 'm')
        with self.assertRaisesRegex(ValueError, 'thread.started'): rp.parse_codex_jsonl('{"type":"item.completed"}', None, 'm')


if __name__ == '__main__': unittest.main()
