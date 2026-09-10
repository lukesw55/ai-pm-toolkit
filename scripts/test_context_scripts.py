#!/usr/bin/env python3
"""Context boundaries, lifecycle preservation and preflight regressions."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        shutil.copytree(ROOT / 'scripts', self.root / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / '.ai/memory/_templates', self.root / '.ai/memory/_templates')
        self.pointer = self.root / '.ai/memory/active-context.md'
        self.projects = self.root / '.ai/memory/projects'
        self.assertEqual(self.run_script('init_context.py', 'Alpha').returncode, 0)

    def run_script(self, script, *args):
        return subprocess.run([sys.executable, str(self.root/'scripts'/script), *args], cwd=self.root, capture_output=True, text=True)

    def test_traversal(self):
        original = self.pointer.read_text()
        outside = Path(self.tmp.name)/'outside'
        outside.mkdir()
        for slug in ('../../../../outside', '../../../escape', str(outside), '-bad', 'bad/name'):
            with self.subTest(slug=slug):
                self.pointer.write_text(original.replace('`alpha`', f'`{slug}`'))
                for script, args in [('validate_context.py', ()), ('log_decision.py', ('Decision','Choice')), ('memory.py', ('doctor',)), ('memory.py', ('log',slug,'body')), ('memory.py', ('activate',slug))]:
                    result=self.run_script(script,*args)
                    self.assertNotEqual(result.returncode,0,(script,slug,result.stdout))
                    self.assertNotIn('Traceback',result.stderr)
                self.assertEqual(list(outside.iterdir()),[])
                self.assertFalse((self.root/'changelog.md').exists())

    def test_symlink_escape(self):
        outside=Path(self.tmp.name)/'outside';outside.mkdir()
        (self.projects/'escape').symlink_to(outside, target_is_directory=True)
        for args in [('log','escape','x'),('activate','escape'),('index','escape'),('distill','escape','--prepare')]:
            self.assertEqual(self.run_script('memory.py',*args).returncode,1)
        target=outside/'stolen.md';target.write_text('untouched')
        (self.projects/'alpha/changelog.md').unlink()
        (self.projects/'alpha/changelog.md').symlink_to(target)
        self.assertEqual(self.run_script('memory.py','log','alpha','x').returncode,1)
        self.assertEqual(target.read_text(),'untouched')
        self.assertEqual(self.run_script('memory.py','doctor').returncode,1)
        (self.projects/'alpha/changelog.md').unlink()
        (self.projects/'alpha/changelog.md').write_text('## 2026-01-01: first\n\nold\n\n## 2026-01-02: next\n\nnew\n')
        pkg=self.projects/'alpha/.distill';pkg.mkdir()
        (pkg/'blocks.md').symlink_to(target)
        self.assertEqual(self.run_script('memory.py','distill','alpha','--prepare','--file','changelog').returncode,1)
        self.assertEqual(target.read_text(),'untouched')
        self.assertFalse((pkg/'manifest.json').exists())

    def test_bootstrap_and_switch(self):
        self.assertEqual(self.run_script('advance_stage.py','prd').returncode,0)
        before=self.pointer.read_bytes()
        (self.projects/'alpha/app.md').write_text('Alpha evidence')
        self.assertEqual(self.run_script('init_context.py','Alpha').returncode,0)
        self.assertEqual(self.pointer.read_bytes(),before)
        self.assertEqual((self.projects/'alpha/app.md').read_text(),'Alpha evidence')
        self.assertEqual(self.run_script('init_context.py','Beta').returncode,2)
        self.assertEqual(self.run_script('memory.py','park','alpha').returncode,0)
        self.assertEqual(self.run_script('init_context.py','Beta').returncode,0)
        self.assertNotEqual((self.projects/'beta/app.md').read_text(),'Alpha evidence')
        self.assertEqual(self.run_script('memory.py','park','beta').returncode,0)
        self.assertEqual(self.run_script('init_context.py','Alpha').returncode,0)
        self.assertIn('**Current stage**: prd',self.pointer.read_text())
        self.assertIn('`beta`:',self.pointer.read_text())
        for slug in ('alpha','beta'):
            for name in ('app.md','design.md','tasks.md'):
                self.assertTrue((self.projects/slug/name).is_file())

    def test_explicit_migration(self):
        legacy=self.root/'.ai/app.md';legacy.write_text('Legacy evidence')
        self.assertEqual(self.run_script('init_context.py','--migrate-legacy','Alpha').returncode,0)
        self.assertNotEqual((self.projects/'alpha/app.md').read_text(),'Legacy evidence')
        (self.projects/'alpha/app.md').unlink()
        self.assertEqual(self.run_script('init_context.py','--migrate-legacy','Alpha').returncode,0)
        self.assertEqual((self.projects/'alpha/app.md').read_text(),'Legacy evidence')
        self.assertEqual(legacy.read_text(),'Legacy evidence')

    def test_stages(self):
        import advance_stage, validate_context
        self.assertEqual(advance_stage.STAGES,validate_context.STAGES)
        self.assertEqual(self.run_script('advance_stage.py','--list').returncode,0)
        for args in [('discover',),('--next',),('delivery',),('--next',)]:
            self.assertEqual(self.run_script('advance_stage.py',*args).returncode,0)
        before=self.pointer.read_bytes()
        self.assertEqual(self.run_script('advance_stage.py','delivery').returncode,0)
        self.assertEqual(self.pointer.read_bytes(),before)
        self.assertNotEqual(self.run_script('advance_stage.py','invalid').returncode,0)
        self.assertEqual(self.pointer.read_bytes(),before)

    def test_decisions_and_missing_fields(self):
        self.pointer.write_text(self.pointer.read_text().replace('**Slug**: `alpha`','**Slug**: alpha'))
        self.assertEqual(self.run_script('log_decision.py','D','C').returncode,0)
        self.assertIn('**Choice**: C',(self.projects/'alpha/decisions.md').read_text())
        self.pointer.write_text(self.pointer.read_text().replace('- **Project**: Alpha',''))
        self.assertEqual(self.run_script('validate_context.py').returncode,1)
        self.pointer.unlink()
        result=self.run_script('log_decision.py','D','C')
        self.assertEqual(result.returncode,1)
        self.assertNotIn('Traceback',result.stderr)

    def test_watch_pure_and_corrupt_lines(self):
        events=self.root/'.ai/memory/context-events.jsonl'
        content='broken\n[]\n{"ts":"bad","slug":"alpha"}\n{"ts":"2026-01-01T00:00:00+00:00","slug":"alpha"}\n'
        events.write_text(content)
        for mode in ('status','report'):
            result=self.run_script('context_watch.py',mode)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(events.read_text(),content)

    def test_preflight_version(self):
        bin_dir=Path(self.tmp.name)/'bin';bin_dir.mkdir()
        python=bin_dir/'python3'
        for version,code in [('3.9.23',1),('3.10.0',0),('3.11.0',0)]:
            python.write_text(f'#!/bin/sh\nif [ "$1" = "--version" ]; then echo Python {version}; exit 0; fi\nexit {code}\n')
            python.chmod(0o755)
            env=dict(os.environ,PATH=str(bin_dir)+os.pathsep+os.environ['PATH'])
            result=subprocess.run(['bash','scripts/check_requirements.sh'],cwd=self.root,env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,code,result.stderr)
            if code:self.assertIn('python3 >= 3.10',result.stderr)


if __name__=='__main__':
    unittest.main()
