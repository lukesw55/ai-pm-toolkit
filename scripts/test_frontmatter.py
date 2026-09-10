#!/usr/bin/env python3
"""Portable frontmatter values and validation outcomes."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import validate_repo as vr


class FrontmatterTests(unittest.TestCase):
    def parse(self, raw, use_yaml):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'SKILL.md'
            p.write_text('---\n'+raw+'\n---\nbody\n', encoding='utf-8')
            errors=[]
            with patch.object(vr,'yaml', vr.yaml if use_yaml else None), patch.object(vr,'rel',lambda p:str(p)):
                result=vr.parse_frontmatter(p,errors)
            return result, errors

    def test_valid_values_match(self):
        if vr.yaml is None:
            self.skipTest('PyYAML is unavailable; cross-parser equality is not verified')
        for description in ('plain text', '"quoted, text"', "'it''s quoted'", '>\n  folded\n  text', '|\n  literal\n  text'):
            raw='name: example\ndescription: '+description
            a, ae=self.parse(raw,True)
            b, be=self.parse(raw,False)
            self.assertEqual(ae,[])
            self.assertEqual(be,[])
            self.assertEqual(a,b)
        self.assertEqual(vr.parse_inline_list('["read,one", true, 3, null]'), ['read,one',True,3,None])

    def test_portable_values(self):
        self.assertEqual(vr.parse_inline_list('["read,one", true, 3, null]'), ['read,one',True,3,None])
        data, errors = self.parse('name: example\ndescription: >\n  folded\n  text', False)
        self.assertEqual(errors, [])
        self.assertEqual(data['description'], 'folded text')

    def test_bad_types_stop_dependent_checks(self):
        for value in ('42','true','null','[read, search]','{x: y}','""','"unterminated','&alias hello'):
            for key in ('name','description'):
                raw='name: example\ndescription: valid\n'
                raw='\n'.join(key+': '+value if line.startswith(key+':') else line for line in raw.splitlines())
                for mode in (True,False):
                    result,errors=self.parse(raw,mode)
                    self.assertIsNone(result,(raw,mode))
                    self.assertTrue(errors)

    def test_duplicate_field_is_invalid(self):
        for mode in (True,False):
            data,errors=self.parse('name: first\nname: second\ndescription: ok',mode)
            self.assertIsNone(data)
            self.assertTrue(errors)


    def test_skill_name_must_match_directory(self):
        with tempfile.TemporaryDirectory() as td:
            skills = Path(td)/'skills'
            (skills/'alpha').mkdir(parents=True)
            skill_md = skills/'alpha'/'SKILL.md'
            for use_yaml in (True, False):
                for name, want_finding in (('beta', True), ('alpha', False)):
                    skill_md.write_text(f'---\nname: {name}\ndescription: valid\n---\nbody\n', encoding='utf-8')
                    errors = []
                    with patch.object(vr, 'yaml', vr.yaml if use_yaml else None), patch.object(vr, 'SKILLS', skills), patch.object(vr, 'rel', lambda p: str(p)):
                        vr.check_skill_frontmatter(errors)
                    hits = [e for e in errors if 'does not match directory' in e]
                    self.assertEqual(bool(hits), want_finding, (name, use_yaml, errors))


if __name__=='__main__':
    unittest.main()
