#!/usr/bin/env python3
"""Regressions for malformed envelopes and real adapter routing."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import validate_repo as vr

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('adapter', ROOT/'.codex/adapters/pretooluse.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class HookContractTests(unittest.TestCase):
    def test_malformed_envelopes_block(self):
        for value in ([], None, {}, {'tool_name': 3},
                      {'tool_name': 'apply_patch', 'tool_input': []},
                      {'tool_name': 'apply_patch', 'tool_input': {'command': 3}},
                      {'tool_name': 'Write', 'tool_input': {'file_path': 'x'}}):
            with self.subTest(value=value):
                r = subprocess.run([sys.executable, str(ROOT/'.codex/adapters/pretooluse.py')], input=json.dumps(value), text=True, capture_output=True)
                self.assertEqual(r.returncode, 2, r.stderr)
                self.assertNotIn('Traceback', r.stderr)

    def test_gate_failures_block(self):
        for exc in (OSError('missing shell'), subprocess.TimeoutExpired('gate', 3)):
            with patch.object(adapter.subprocess, 'run', side_effect=exc):
                self.assertEqual(adapter.run_gates({})[0], 2)
        with patch.object(adapter.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, b'', b'bad gate')):
            self.assertEqual(adapter.run_gates({}), (2, 'bad gate'))

    def test_real_contract(self):
        errors = []
        vr.check_hook_contract(errors)
        self.assertEqual(errors, [])

    def test_broken_shapes(self):
        for data in ([], {'hooks': []}, {'hooks': {'Stop': {}}},
                     {'hooks': {'Stop': [None]}}, {'hooks': {'Stop': [{'hooks': [None]}]}},
                     {'hooks': {'Stop': [{'hooks': [{'type': 'command', 'command': 2}]}]}}):
            with tempfile.TemporaryDirectory() as td:
                path = Path(td)/'adapter.json'
                path.write_text(json.dumps(data))
                errors = []
                with patch.object(vr, 'rel', lambda p: str(p)):
                    self.assertIsNone(vr._check_hook_wiring(path, set(), errors))
                self.assertTrue(errors)

    def test_missing_and_misrouted_handlers(self):
        for relative in ('.claude/settings.json', '.codex/hooks.json'):
            original = json.loads((ROOT/relative).read_text())
            for event in original['hooks']:
                changed = copy.deepcopy(original)
                del changed['hooks'][event]
                original_read = Path.read_text
                def read(path, *args, **kwargs):
                    return json.dumps(changed) if path == ROOT/relative else original_read(path, *args, **kwargs)
                with patch.object(Path, 'read_text', read):
                    errors = []
                    vr.check_hook_contract(errors)
                    self.assertTrue(errors, event)
            changed = copy.deepcopy(original)
            for block in changed['hooks']['PreToolUse']:
                block['matcher'] = 'wrong-tool'
            with patch.object(Path, 'read_text', lambda path, *a, **kw: json.dumps(changed) if path == ROOT/relative else original_read(path, *a, **kw)):
                errors = []
                vr.check_hook_contract(errors)
                self.assertTrue(errors)

    def test_configured_write_commands(self):
        marker = '[' + 'UNVERIFIED: fixture]'
        for relative, tool, inp in (
            ('.claude/settings.json', 'Write', {'file_path': '/tmp/fixture/doc.md', 'content': marker}),
            ('.codex/hooks.json', 'apply_patch', {'command': '*** Begin Patch\n*** Add File: /tmp/fixture/doc.md\n+'+marker+'\n*** End Patch'}),
        ):
            data = json.loads((ROOT/relative).read_text())
            commands = vr.matching_handlers(data, 'PreToolUse', tool)
            env = dict(os.environ, CLAUDE_PROJECT_DIR=str(ROOT))
            codes = [subprocess.run(['bash', '-c', command], input=json.dumps({'tool_name': tool, 'tool_input': inp}), text=True, capture_output=True, cwd=ROOT, env=env).returncode for command in commands]
            self.assertIn(2, codes, (relative, codes))


if __name__ == '__main__':
    unittest.main()
