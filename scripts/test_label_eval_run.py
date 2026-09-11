"""Human labels: append-only file, run identity, supersede and split rules, the grader's two disagreement rates."""
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
        self.spec=manifest['evals'][0];self.eval=self.spec['name']
        self.iteration='iteration-test'
        self.record_pair(self.iteration,{'with_skill':'alpha beta: synthetic fixture, not model evidence','without_skill':'gamma: synthetic fixture, not model evidence'})
        self.assertions={self.skill:{self.eval:[('mentions alpha',ge.has('alpha')),('mentions beta',ge.has('beta'))]}}

    def record_pair(self,iteration,texts):
        for config,text in texts.items():
            out=self.root/f'{iteration}-{config}.md';out.write_text(text)
            rr.record(argparse.Namespace(skill=self.skill,eval=self.eval,config=config,iteration=iteration,harness='codex',model='fixture',source='synthetic-test-only',output=out,tokens=None,duration_ms=None),self.root)

    def label_args(self,**over):
        base=dict(skill=self.skill,eval=self.eval,config='with_skill',iteration=self.iteration,verdict='good',classification=[],reason='usable as delivered',labeler='lucas',labels_file=None,supersede=False)
        base.update(over);return argparse.Namespace(**base)

    def grade(self,iteration=None):
        iteration=iteration or self.iteration
        labels=lr.load_labels(lr.labels_path(self.root,iteration),iteration)
        report={}
        with patch.object(ge,'REPO',self.root),patch.object(ge,'SKILLS_DIR',self.root/'skills'),patch.dict(ge.ASSERTIONS,self.assertions):
            runs=ge.grade_all(iteration,labels=labels,report=report)
            benchmark=ge.aggregate_benchmark(runs,iteration)
            ge.render_html(benchmark,runs,self.root/'eval-report.html',iteration)
        return runs,benchmark,report,(self.root/'eval-report.html').read_text(encoding='utf-8')

    def orphan(self,**over):
        base=dict(schema=lr.SCHEMA,iteration=self.iteration,skill=self.skill,eval_id=0,eval_name=self.eval,config='with_skill',output_sha256='a'*64,rubric_version='b'*12,verdict='good',classification=[],verdict_reason='x',labeler='lucas',labeled_at='2026-09-10T10:00:00+00:00',supersedes=False)
        base.update(over);return base

    def test_append_supersede_and_history(self):
        path=lr.label(self.label_args(),self.root)
        self.assertEqual(path,self.root/'docs/benchmarks'/self.iteration/'labels.jsonl')
        record=json.loads(path.read_text().splitlines()[0])
        self.assertEqual(record['verdict'],'good');self.assertEqual(record['eval_name'],self.eval);self.assertFalse(record['supersedes'])
        self.assertEqual(record['rubric_version'],lr.rubric_version(self.spec))
        self.assertIsNotNone(__import__('datetime').datetime.fromisoformat(record['labeled_at']).tzinfo)
        with self.assertRaisesRegex(ValueError,'supersede'):lr.label(self.label_args(),self.root)
        with self.assertRaisesRegex(ValueError,'no label on this run'):lr.label(self.label_args(labeler='ana',supersede=True),self.root)
        lr.label(self.label_args(verdict='weak',classification=['incomplete'],supersede=True),self.root)
        lr.label(self.label_args(labeler='ana',verdict='weak',classification=['incomplete']),self.root)
        self.assertEqual(len(path.read_text().splitlines()),3)
        current=lr.load_labels(path,self.iteration)
        self.assertEqual(len(current),1)
        (labels,)=current.values()
        self.assertEqual(sorted((r['labeler'],r['verdict'],r['supersedes']) for r in labels),[('ana','weak',False),('lucas','weak',True)])
        self.assertEqual(lr.superseded_count(path,self.iteration),1)
        self.assertEqual(len(lr.read_labels(path,self.iteration)),3)

    def test_identity_is_the_run_not_the_text(self):
        same='iteration-same';text='alpha beta: identical text under both configurations'
        self.record_pair(same,{'with_skill':text,'without_skill':text})
        lr.label(self.label_args(iteration=same,config='with_skill',verdict='good'),self.root)
        lr.label(self.label_args(iteration=same,config='without_skill',verdict='fail',classification=['invented-fact']),self.root)
        current=lr.load_labels(lr.labels_path(self.root,same),same)
        self.assertEqual(len(current),2)
        runs,benchmark,report,html=self.grade(same)
        entry=benchmark['skills'][self.skill]['evals'][0]
        self.assertEqual(entry['with_skill']['human_verdict'],'good');self.assertEqual(entry['without_skill']['human_verdict'],'fail')
        self.assertFalse(entry['with_skill']['human_split']);self.assertFalse(entry['without_skill']['human_split'])
        self.assertEqual(report,{'labels_unmatched':0,'labels_stale':0})

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
        for over,message in [(dict(schema=1),'schema'),(dict(rubric_version='zz'),'rubric_version'),(dict(supersedes='yes'),'supersedes')]:
            with self.subTest(over=over),self.assertRaisesRegex(ValueError,message):lr.parse_label(json.dumps(self.orphan(**over)),self.iteration)

    def test_grader_disagreement_and_investigate_flag(self):
        lr.label(self.label_args(config='with_skill',verdict='fail',classification=['invented-fact']),self.root)
        lr.label(self.label_args(config='without_skill',verdict='fail',classification=['skipped-method']),self.root)
        runs,benchmark,report,html=self.grade()
        summary=benchmark['skills'][self.skill]['summary']
        self.assertEqual(summary['labeled_runs'],2);self.assertEqual(summary['grader_disagreement_rate'],0.5);self.assertTrue(summary['investigate_grader'])
        self.assertEqual(summary['human_split_runs'],0);self.assertIsNone(summary['human_disagreement_rate'])
        self.assertEqual(benchmark['overall']['labeled_runs'],2);self.assertTrue(benchmark['overall']['investigate_grader'])
        self.assertEqual(benchmark['overall']['classification_counts'],{'invented-fact':1,'skipped-method':1})
        entry=benchmark['skills'][self.skill]['evals'][0]
        self.assertEqual(entry['with_skill']['human_verdict'],'fail');self.assertFalse(entry['with_skill']['agrees'])
        self.assertEqual(entry['without_skill']['human_verdict'],'fail');self.assertTrue(entry['without_skill']['agrees'])
        grading=json.loads(next((self.root/'skills'/self.skill/'workspace'/self.iteration).glob('eval-*/with_skill/grading.json')).read_text())
        self.assertEqual(len(grading['labels']),1);self.assertEqual(grading['human_verdict'],'fail');self.assertFalse(grading['human_split'])
        self.assertIn('investigate',html);self.assertIn('Human',html);self.assertNotIn('drift',html);self.assertEqual(report,{'labels_unmatched':0,'labels_stale':0})

    def test_split_is_pending_not_worse(self):
        lr.label(self.label_args(verdict='good'),self.root)
        lr.label(self.label_args(labeler='ana',verdict='fail',classification=['wrong-decision']),self.root)
        runs,benchmark,report,html=self.grade()
        entry=benchmark['skills'][self.skill]['evals'][0]['with_skill']
        self.assertIsNone(entry['human_verdict']);self.assertTrue(entry['human_split']);self.assertIsNone(entry['agrees']);self.assertEqual(entry['labelers'],2);self.assertTrue(entry['human_mixed'])
        summary=benchmark['skills'][self.skill]['summary']
        self.assertEqual(summary['labeled_runs'],1);self.assertEqual(summary['human_split_runs'],1);self.assertEqual(summary['human_disagreement_rate'],1.0)
        self.assertIsNone(summary['grader_disagreement_rate']);self.assertIsNone(summary['investigate_grader'])
        self.assertIn('split',html)

    def test_no_labels_leaves_fields_null(self):
        runs,benchmark,report,html=self.grade()
        summary=benchmark['skills'][self.skill]['summary']
        self.assertEqual(summary['labeled_runs'],0);self.assertIsNone(summary['grader_disagreement_rate']);self.assertIsNone(summary['investigate_grader']);self.assertIsNone(summary['human_disagreement_rate'])
        entry=benchmark['skills'][self.skill]['evals'][0]
        self.assertIsNone(entry['with_skill']['human_verdict']);self.assertIsNone(entry['with_skill']['agrees']);self.assertEqual(entry['with_skill']['labelers'],0)
        self.assertNotIn("badge-fail'>investigate",html);self.assertIn('no labels',html)

    def test_unmatched_label_warns_not_fails(self):
        path=lr.labels_path(self.root,self.iteration);path.parent.mkdir(parents=True)
        path.write_text(json.dumps(self.orphan())+'\n')
        runs,benchmark,report,html=self.grade()
        self.assertEqual(report['labels_unmatched'],1);self.assertEqual(benchmark['overall']['labeled_runs'],0)

    def test_iteration_mismatch_and_bad_lines_refused(self):
        path=self.root/'labels.jsonl'
        path.write_text(json.dumps(self.orphan(iteration='iteration-other'))+'\n')
        with self.assertRaisesRegex(ValueError,'iteration'):lr.load_labels(path,self.iteration)
        path.write_text('not json\n')
        with self.assertRaisesRegex(ValueError,'JSON'):lr.load_labels(path,self.iteration)
        self.assertEqual(lr.load_labels(self.root/'missing.jsonl',self.iteration),{})
        self.assertEqual(lr.superseded_count(self.root/'missing.jsonl',self.iteration),0)

    def test_verdict_majority_split_and_mixed(self):
        mk=lambda v:{'verdict':v}
        self.assertIsNone(lr.human_verdict([]));self.assertFalse(lr.is_split([]));self.assertFalse(lr.is_mixed([mk('good')]))
        self.assertEqual(lr.human_verdict([mk('good'),mk('good'),mk('fail')]),'good');self.assertTrue(lr.is_mixed([mk('good'),mk('good'),mk('fail')]))
        self.assertIsNone(lr.human_verdict([mk('good'),mk('weak')]));self.assertTrue(lr.is_split([mk('good'),mk('weak')]))
        self.assertEqual(lr.human_verdict([mk('weak'),mk('weak'),mk('good'),mk('fail')]),'weak')
        self.assertIsNone(lr.binarize([mk('good'),mk('fail')]));self.assertTrue(lr.binarize([mk('good')]));self.assertFalse(lr.binarize([mk('weak')]))

    def test_stale_rubric_label_is_flagged_not_counted(self):
        lr.label(self.label_args(verdict='good'),self.root)
        manifest_path=self.root/'skills'/self.skill/'evals/evals.json'
        manifest=json.loads(manifest_path.read_text())
        entry=next(e for e in manifest['evals'] if e['name']==self.eval)
        entry['expected_output']=entry.get('expected_output','')+' Revised expectation.'
        manifest_path.write_text(json.dumps(manifest))
        runs,benchmark,report,html=self.grade()
        entry_ws=benchmark['skills'][self.skill]['evals'][0]['with_skill']
        self.assertIsNone(entry_ws['human_verdict']);self.assertEqual(entry_ws['labelers'],0);self.assertEqual(entry_ws['stale_labels'],1)
        self.assertEqual(report,{'labels_unmatched':0,'labels_stale':1})
        self.assertEqual(benchmark['skills'][self.skill]['summary']['labeled_runs'],0)
        grading=json.loads(next((self.root/'skills'/self.skill/'workspace'/self.iteration).glob('eval-*/with_skill/grading.json')).read_text())
        self.assertEqual(grading['labels'],[]);self.assertEqual(grading['stale_labels'][0]['labeler'],'lucas')
        # relabelling against the current rubric needs no --supersede and keeps the history
        path=lr.label(self.label_args(verdict='weak',classification=['incomplete']),self.root)
        self.assertEqual(len(path.read_text().splitlines()),2)
        runs,benchmark,report,html=self.grade()
        entry_ws=benchmark['skills'][self.skill]['evals'][0]['with_skill']
        # the relabel supersedes the stale record for that labeler: nothing stale remains, the history is counted as superseded
        self.assertEqual(entry_ws['human_verdict'],'weak');self.assertEqual(entry_ws['stale_labels'],0);self.assertEqual(report['labels_stale'],0)
        self.assertEqual(lr.superseded_count(path,self.iteration),1)

    def test_rubric_version_follows_prompt_and_expectation(self):
        version=lr.rubric_version(self.spec)
        self.assertRegex(version,'^[a-f0-9]{12}$')
        self.assertEqual(version,lr.rubric_version(dict(self.spec)))
        self.assertNotEqual(version,lr.rubric_version({**self.spec,'expected_output':self.spec.get('expected_output','')+' changed'}))

    def test_handles_documented(self):
        text=(rr.ROOT/'docs/EVAL_PROTOCOL.md').read_text(encoding='utf-8')
        for handle in lr.CLASSIFICATIONS:
            self.assertIn(f'`{handle}`',text,handle)


if __name__=='__main__':unittest.main()
