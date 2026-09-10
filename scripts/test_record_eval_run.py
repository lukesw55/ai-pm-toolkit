"""Recorder integration uses explicitly synthetic outputs in disposable repositories."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import grade_evals as ge
import record_eval_run as rr


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.skill='pm-prioritization-regua-comum'
        shutil.copytree(rr.ROOT/'skills'/self.skill,self.root/'skills'/self.skill)
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--allow-empty','-qm','fixture'],check=True)
        output=self.root/'synthetic.md';output.write_text('Synthetic pipeline fixture; not model evidence.')
        self.args=argparse.Namespace(skill=self.skill,eval='score-and-rank-features',config='with_skill',iteration='iteration-test',harness='codex',model='fixture',source='synthetic-test-only',output=output,tokens=None,duration_ms=None)
        manifest=json.loads((self.root/'skills'/self.skill/'evals/evals.json').read_text())
        self.args.eval=manifest['evals'][0]['name']

    def test_roundtrip_pair(self):
        target=rr.record(self.args,self.root)
        meta=rr.validate_run(target,self.skill,rr.eval_spec(self.root,self.skill,self.args.eval),'with_skill')
        self.assertEqual(meta['source'],'synthetic-test-only')
        self.args.config='without_skill';rr.record(self.args,self.root)
        with patch.object(ge,'REPO',self.root),patch.object(ge,'SKILLS_DIR',self.root/'skills'):
            runs=ge.grade_all('iteration-test')
        self.assertEqual(len(runs[self.skill]),2)
        with patch.object(ge,'SKILLS_DIR',self.root/'skills'):
            self.assertEqual(ge.aggregate_benchmark(runs,'iteration-test')['overall']['n_evals'],1)

    def test_overwrite_and_tamper(self):
        target=rr.record(self.args,self.root)
        with self.assertRaises(ValueError):rr.record(self.args,self.root)
        (target/'outputs/output.md').write_text('tampered')
        with self.assertRaises(ValueError):rr.validate_run(target,self.skill,rr.eval_spec(self.root,self.skill,self.args.eval),'with_skill')

    def test_missing_pair_and_model_mismatch(self):
        rr.record(self.args,self.root)
        with patch.object(ge,'REPO',self.root),patch.object(ge,'SKILLS_DIR',self.root/'skills'):
            with self.assertRaises(OSError):ge.grade_all('iteration-test')
        self.args.config='without_skill';self.args.model='another-model';rr.record(self.args,self.root)
        with patch.object(ge,'REPO',self.root),patch.object(ge,'SKILLS_DIR',self.root/'skills'):
            with self.assertRaises(ValueError):ge.grade_all('iteration-test')

    def test_mixed_iteration(self):
        manifest=json.loads((self.root/'skills'/self.skill/'evals/evals.json').read_text())
        for i,spec in enumerate(manifest['evals'][:2]):
            self.args.eval=spec['name'];self.args.model=f'model-{i}'
            for config in ('with_skill','without_skill'):
                self.args.config=config;rr.record(self.args,self.root)
        with patch.object(ge,'REPO',self.root),patch.object(ge,'SKILLS_DIR',self.root/'skills'):
            with self.assertRaisesRegex(ValueError,'mixed harness'):ge.grade_all('iteration-test')

    def test_reject_invalid_inputs(self):
        for key,value in [('skill','../escape'),('iteration','../../escape'),('tokens',-1),('model','')]:
            args=argparse.Namespace(**vars(self.args));setattr(args,key,value)
            with self.subTest(key=key),self.assertRaises(ValueError):rr.record(args,self.root)


if __name__=='__main__':unittest.main()
