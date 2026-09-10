"""Human labels: append-only file, hash binding, and the grader's disagreement rate."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import grade_evals as ge
import label_eval_run as lr
import record_eval_run as rr


class LabelTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.skill='pm-prioritization-regua-comum'
        shutil.copytree(rr.ROOT/'skills'/self.skill,self.root/'skills'/self.skill,ignore=shutil.ignore_patterns('workspace','__pycache__'))
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--allow-empty','-qm','fixture'],check=True)
        manifest=json.loads((self.root/'skills'/self.skill/'evals/evals.json').read_text())
        self.eval=manifest['evals'][0]['name']
        self.iteration='iteration-test'
        for config,text in (('with_skill','alpha beta: synthetic fixture, not model evidence'),('without_skill','gamma: synthetic fixture, not model evidence')):
            out=self.root/f'{config}.md';out.write_text(text)
            rr.record(argparse.Namespace(skill=self.skill,eval=self.eval,config=config,iteration=self.iteration,harness='codex',model='fixture',source='synthetic-test-only',output=out,tokens=None,duration_ms=None),self.root)
        self.assertions={self.skill:{self.eval:[('mentions alpha',ge.has('alpha')),('mentions beta',ge.has('beta'))]}}

    def label_args(self,**over):
        base=dict(skill=self.skill,eval=self.eval,config='with_skill',iteration=self.iteration,verdict='good',classification=[],reason='usable as delivered',labeler='lucas',labels_file=None)
        base.update(over);return argparse.Namespace(**base)

    def grade(self):
        labels=lr.load_labels(lr.labels_path(self.root,self.iteration),self.iteration)
        report={}
        with patch.object(ge,'REPO',self.root),patch.object(ge,'SKILLS_DIR',self.root/'skills'),patch.dict(ge.ASSERTIONS,self.assertions):
            runs=ge.grade_all(self.iteration,labels=labels,report=report)
            benchmark=ge.aggregate_benchmark(runs,self.iteration)
            ge.render_html(benchmark,runs,self.root/'eval-report.html',self.iteration)
        return runs,benchmark,report,(self.root/'eval-report.html').read_text(encoding='utf-8')

    def test_append_and_duplicate_refusal(self):
        path=lr.label(self.label_args(),self.root)
        self.assertEqual(path,self.root/'docs/benchmarks'/self.iteration/'labels.jsonl')
        lines=path.read_text().splitlines();self.assertEqual(len(lines),1)
        record=json.loads(lines[0]);self.assertEqual(record['verdict'],'good');self.assertEqual(record['eval_name'],self.eval)
        self.assertIsNotNone(__import__('datetime').datetime.fromisoformat(record['labeled_at']).tzinfo)
        with self.assertRaisesRegex(ValueError,'already labeled'):lr.label(self.label_args(),self.root)
        lr.label(self.label_args(labeler='ana',verdict='weak',classification=['incomplete']),self.root)
        self.assertEqual(len(path.read_text().splitlines()),2)

    def test_hash_mismatch_and_unknown_run_refused(self):
        target=self.root/'skills'/self.skill/'workspace'/self.iteration
        run_dir=next(target.glob('eval-*'))/'with_skill'
        (run_dir/'outputs/output.md').write_text('tampered')
        with self.assertRaises(ValueError):lr.label(self.label_args(),self.root)
        with self.assertRaises(OSError):lr.label(self.label_args(iteration='iteration-other'),self.root)

    def test_invalid_inputs(self):
        for over in [dict(verdict='meh'),dict(verdict='weak',classification=['nonsense']),dict(verdict='weak',classification=[]),dict(reason='  '),dict(labeler=''),dict(config='sideways')]:
            with self.subTest(over=over),self.assertRaises(ValueError):lr.label(self.label_args(**over),self.root)
        self.assertFalse(lr.labels_path(self.root,self.iteration).exists())

    def test_disagreement_and_drift(self):
        lr.label(self.label_args(config='with_skill',verdict='fail',classification=['invented-fact']),self.root)
        lr.label(self.label_args(config='without_skill',verdict='fail',classification=['skipped-method']),self.root)
        runs,benchmark,report,html=self.grade()
        summary=benchmark['skills'][self.skill]['summary']
        self.assertEqual(summary['labeled_runs'],2);self.assertEqual(summary['disagreement_rate'],0.5);self.assertTrue(summary['grader_drift'])
        self.assertEqual(benchmark['overall']['labeled_runs'],2);self.assertTrue(benchmark['overall']['grader_drift'])
        self.assertEqual(benchmark['overall']['classification_counts'],{'invented-fact':1,'skipped-method':1})
        entry=benchmark['skills'][self.skill]['evals'][0]
        self.assertEqual(entry['with_skill']['human_verdict'],'fail');self.assertFalse(entry['with_skill']['agrees'])
        self.assertEqual(entry['without_skill']['human_verdict'],'fail');self.assertTrue(entry['without_skill']['agrees'])
        grading=json.loads(next((self.root/'skills'/self.skill/'workspace'/self.iteration).glob('eval-*/with_skill/grading.json')).read_text())
        self.assertEqual(len(grading['labels']),1);self.assertEqual(grading['human_verdict'],'fail')
        self.assertIn('drift',html);self.assertIn('Human',html);self.assertEqual(report,{'labels_unmatched':0})

    def test_no_labels_leaves_fields_null(self):
        runs,benchmark,report,html=self.grade()
        summary=benchmark['skills'][self.skill]['summary']
        self.assertEqual(summary['labeled_runs'],0);self.assertIsNone(summary['disagreement_rate']);self.assertIsNone(summary['grader_drift'])
        entry=benchmark['skills'][self.skill]['evals'][0]
        self.assertIsNone(entry['with_skill']['human_verdict']);self.assertIsNone(entry['with_skill']['agrees'])
        self.assertNotIn('badge-fail\'>drift',html);self.assertIn('no labels',html)

    def test_unmatched_label_warns_not_fails(self):
        path=lr.labels_path(self.root,self.iteration);path.parent.mkdir(parents=True)
        record=dict(schema=1,iteration=self.iteration,skill=self.skill,eval_id=0,eval_name=self.eval,config='with_skill',output_sha256='a'*64,verdict='good',classification=[],verdict_reason='x',labeler='lucas',labeled_at='2026-09-10T10:00:00+00:00')
        path.write_text(json.dumps(record)+'\n')
        runs,benchmark,report,html=self.grade()
        self.assertEqual(report['labels_unmatched'],1);self.assertEqual(benchmark['overall']['labeled_runs'],0)

    def test_iteration_mismatch_and_bad_lines_refused(self):
        path=self.root/'labels.jsonl'
        path.write_text(json.dumps(dict(schema=1,iteration='iteration-other',skill=self.skill,eval_id=0,eval_name=self.eval,config='with_skill',output_sha256='a'*64,verdict='good',classification=[],verdict_reason='x',labeler='l',labeled_at='2026-09-10T10:00:00+00:00'))+'\n')
        with self.assertRaisesRegex(ValueError,'iteration'):lr.load_labels(path,self.iteration)
        path.write_text('not json\n')
        with self.assertRaisesRegex(ValueError,'JSON'):lr.load_labels(path,self.iteration)
        self.assertEqual(lr.load_labels(self.root/'missing.jsonl',self.iteration),{})

    def test_verdict_majority_and_tie(self):
        mk=lambda v:{'verdict':v}
        self.assertIsNone(lr.human_verdict([]))
        self.assertEqual(lr.human_verdict([mk('good'),mk('good'),mk('fail')]),'good')
        self.assertEqual(lr.human_verdict([mk('good'),mk('weak')]),'weak')
        self.assertFalse(lr.binarize([mk('good'),mk('fail')]));self.assertTrue(lr.binarize([mk('good')]))

    def test_handles_documented(self):
        text=(rr.ROOT/'docs/EVAL_PROTOCOL.md').read_text(encoding='utf-8')
        for handle in lr.CLASSIFICATIONS:
            self.assertIn(f'`{handle}`',text,handle)


if __name__=='__main__':unittest.main()
