"""Proposals from labelled disagreements: what is proposed, what deliberately is not, and that nothing is ever applied."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import grade_evals as ge
import label_eval_run as lr
import propose_eval_updates as pe
import record_eval_run as rr


class ProposeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.skill='pm-prioritization-regua-comum'
        shutil.copytree(rr.ROOT/'skills'/self.skill,self.root/'skills'/self.skill,ignore=shutil.ignore_patterns('workspace','__pycache__'))
        (self.root/'scripts').mkdir(parents=True,exist_ok=True)
        shutil.copy(rr.ROOT/'scripts'/'grade_evals.py',self.root/'scripts'/'grade_evals.py')
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--allow-empty','-qm','fixture'],check=True)
        manifest=json.loads((self.root/'skills'/self.skill/'evals/evals.json').read_text())
        self.spec=manifest['evals'][0];self.eval=self.spec['name']
        self.iteration='iteration-test'
        self.good='alpha beta: synthetic fixture, not model evidence'
        self.bad='gamma: synthetic fixture, not model evidence'
        self.record_pair(self.iteration,{'with_skill':self.good,'without_skill':self.bad})
        self.assertions={self.skill:{self.eval:[('mentions alpha',ge.has('alpha')),('mentions beta',ge.has('beta'))]}}

    # -- sandbox helpers, in the shape of test_label_eval_run.py --------------------
    def record_pair(self,iteration,texts):
        for config,text in texts.items():
            out=self.root/f'{iteration}-{config}.md';out.write_text(text)
            rr.record(argparse.Namespace(skill=self.skill,eval=self.eval,config=config,iteration=iteration,harness='codex',model='fixture',source='synthetic-test-only',output=out,tokens=None,duration_ms=None),self.root)

    def label(self,**over):
        base=dict(skill=self.skill,eval=self.eval,config='with_skill',iteration=self.iteration,verdict='good',classification=[],reason='usable as delivered',labeler='lucas',labels_file=None,supersede=False)
        base.update(over);lr.label(argparse.Namespace(**base),self.root)

    def write_fixture_pair(self,**over):
        path=self.root/pe.FIXTURES;path.parent.mkdir(parents=True,exist_ok=True)
        pair={'skill':self.skill,'eval':self.eval,'good':self.good,'bad':'delta: a plausible wrong answer',
              'keyword_only':'alpha. beta.','near_miss':{'text':'alpha only','fails':'mentions beta'}}
        pair.update(over)
        path.write_text(json.dumps([pair],indent=2)+'\n',encoding='utf-8')
        return pair

    def five_checks(self):
        """alpha, beta, synthetic and fixture pass on self.good; epsilon does not."""
        return {self.skill:{self.eval:[('mentions alpha',ge.has('alpha')),('mentions beta',ge.has('beta')),
                                       ('mentions synthetic',ge.has('synthetic')),('mentions fixture',ge.has('fixture')),
                                       ('mentions epsilon',ge.has('epsilon'))]}}

    def meta(self,config='with_skill'):
        directory=pe.run_dir(self.root,self.iteration,self.skill,self.spec['id'],self.eval,config)
        return json.loads((directory/'meta.json').read_text(encoding='utf-8'))

    def raw_label(self,drop=(),**over):
        """A label written straight into the file, for shapes the CLI refuses to produce."""
        base=dict(schema=lr.SCHEMA,iteration=self.iteration,skill=self.skill,eval_id=self.spec['id'],eval_name=self.eval,
                  config='with_skill',output_sha256=self.meta()['output_sha256'],rubric_version=lr.rubric_version(self.spec),
                  verdict='good',classification=[],verdict_reason='x',labeler='lucas',
                  labeled_at='2026-09-16T10:00:00+00:00',supersedes=False)
        base.update(over)
        for key in drop:
            base.pop(key,None)
        path=lr.labels_path(self.root,self.iteration);path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('a',encoding='utf-8') as handle:
            handle.write(json.dumps(base,sort_keys=True,ensure_ascii=False)+'\n')

    def args(self,**over):
        base=dict(iteration=self.iteration,labels=None,skill=None,eval=None,out=None,
                  excerpt_chars=pe.EXCERPT_CHARS,full_output=False,force=False,dry_run=False)
        base.update(over);return argparse.Namespace(**base)

    def propose(self,**over):
        with patch.dict(ge.ASSERTIONS,self.assertions):
            return pe.propose(self.args(**over),self.root)

    def out_dir(self):
        return pe.proposals_dir(self.root,self.iteration)

    def written(self):
        return sorted(p.name for p in self.out_dir().iterdir()) if self.out_dir().is_dir() else []

    def one_proposal(self):
        files=[p for p in self.out_dir().iterdir() if p.suffix=='.json' and p.stem!='index']
        self.assertEqual(len(files),1,self.written())
        return json.loads(files[0].read_text(encoding='utf-8')),files[0].with_suffix('.md').read_text(encoding='utf-8')

    # -- the five categories --------------------------------------------------------
    def test_false_accept(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='Scores every dimension but never applies the lock')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['false-accept'])
        proposal,markdown=self.one_proposal()
        self.assertEqual(proposal['category'],'false-accept')
        self.assertEqual(proposal['grader']['pass_rate'],1.0)
        self.assertIs(proposal['grader']['agrees'],False)
        self.assertEqual(proposal['human']['verdict'],'weak')
        self.assertEqual(proposal['fixture_suggestion']['slot'],'near_miss')
        self.assertIn('Scores every dimension but never applies the lock',markdown)
        self.assertIn(self.meta()['output_sha256'],markdown)
        # every assertion passed, so the candidates are the ones a wrong answer also satisfies
        self.assertEqual(proposal['implicated_assertions']['already_failing'],[])
        self.assertEqual(proposal['implicated_assertions']['labels'],['mentions alpha','mentions beta'])

    def test_a_false_accept_reports_the_failing_check_without_targeting_it(self):
        """A binarised pass is the rate clearing the threshold, not a clean sheet. The check that
        already fails is diagnostic: tightening it cannot move a rate it contributes nothing to."""
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='Scores every dimension but never applies the lock')
        with patch.dict(ge.ASSERTIONS,self.five_checks()):
            pe.propose(self.args(),self.root)
        proposal,markdown=self.one_proposal()
        self.assertEqual(proposal['category'],'false-accept')
        self.assertEqual(proposal['grader']['pass_rate'],0.8)
        self.assertEqual(proposal['implicated_assertions']['already_failing'],['mentions epsilon'])
        self.assertNotIn('mentions epsilon',proposal['assertion_change']['targets'])
        self.assertIn('4 of 5 assertions passed',markdown)
        self.assertIn('They are not the ones to change',markdown)
        self.assertNotIn('Every assertion passed',markdown)

    def test_a_false_accept_targets_a_check_that_can_flip_it(self):
        """The remediation candidate is a check that passes today, so changing it can actually
        take the rate under the threshold. Here 4 of 5 pass and 3 of 5 is 0.60."""
        self.write_fixture_pair(bad='alpha, but delta is the wrong call')
        self.label(verdict='weak',classification=['skipped-method'],reason='Applies the ruler but never the lock')
        with patch.dict(ge.ASSERTIONS,self.five_checks()):
            pe.propose(self.args(),self.root)
        proposal,markdown=self.one_proposal()
        marks,change=proposal['implicated_assertions'],proposal['assertion_change']
        passing=[e['text'] for e in proposal['grader']['expectations'] if e['passed']]
        self.assertEqual(change['targets'],['mentions alpha'])
        self.assertTrue(set(change['targets']) <= set(passing),'a target has to be a check that passes today')
        self.assertEqual(marks['already_failing'],['mentions epsilon'])
        self.assertEqual(change['checks_to_flip'],1)
        grader=proposal['grader']
        self.assertLess((grader['passed']-change['checks_to_flip'])/grader['total'],grader['threshold'],
                        'flipping that many checks has to put the rate under the threshold')
        self.assertIn('first candidates to tighten',markdown)

    def test_a_false_accept_without_a_mechanical_target_says_so(self):
        self.write_fixture_pair(keyword_only='delta. epsilon.')
        self.label(verdict='weak',classification=['skipped-method'],reason='Applies the ruler but never the lock')
        with patch.dict(ge.ASSERTIONS,self.five_checks()):
            pe.propose(self.args(),self.root)
        proposal,markdown=self.one_proposal()
        self.assertEqual(proposal['assertion_change']['targets'],[])
        self.assertIn('no mechanical candidate',markdown)
        self.assertIn('the reviewer picks what to write',markdown)

    def test_checks_to_flip_counts_what_a_change_has_to_move(self):
        """One check is enough at 4 of 5 and is not at 9 of 10, which is the difference between
        a card that asks for one assertion and one that says a single change cannot get there."""
        self.assertEqual(pe.checks_to_flip({'passed':4,'total':5}),1)
        self.assertEqual(pe.checks_to_flip({'passed':9,'total':10}),2)
        self.assertEqual(pe.checks_to_flip({'passed':8,'total':8}),2)
        self.assertIsNone(pe.checks_to_flip({'passed':3,'total':5}),'not a binarised pass')

    def test_an_eval_without_assertions_is_reported_not_proposed(self):
        """A card would name the assertions to change and have none to name."""
        self.label(verdict='good',reason='usable as delivered')
        with patch.dict(ge.ASSERTIONS,{self.skill:{}}):
            index=pe.propose(self.args(),self.root)
        self.assertEqual([row['outcome'] for row in index['outcomes']],['no-assertions'])
        self.assertEqual(self.written(),['index.json','index.md'])

    def test_false_reject(self):
        self.write_fixture_pair()
        self.label(config='without_skill',verdict='good',reason='Right call, written another way')
        proposal,_=self.one_proposal() if self.propose() else (None,None)
        self.assertEqual(proposal['category'],'false-reject')
        self.assertEqual(proposal['implicated_assertions']['labels'],['mentions alpha','mentions beta'])
        self.assertEqual(proposal['fixture_suggestion']['slot'],'good')
        self.assertIs(proposal['fixture_suggestion']['rewrite_required'],True)

    def test_agreement_proposes_nothing(self):
        self.label(verdict='good',reason='usable as delivered')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['agreement'])
        self.assertEqual(self.written(),['index.json','index.md'])

    def test_agreement_when_both_reject_proposes_nothing(self):
        """The other direction of agreement: the assertions rejected the run and so did a human."""
        self.label(config='without_skill',verdict='fail',classification=['wrong-decision'],reason='wrong call')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['agreement'])
        self.assertEqual(self.written(),['index.json','index.md'])

    def test_split_is_reported_not_proposed(self):
        self.label(verdict='good',reason='fine',labeler='lucas')
        self.label(verdict='fail',classification=['wrong-decision'],reason='wrong call',labeler='ana')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['split'])
        self.assertEqual(self.written(),['index.json','index.md'])

    def test_stale_rubric_only(self):
        self.raw_label(rubric_version='b'*12,verdict='fail',classification=['incomplete'],reason='against an older expectation')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['stale-rubric'])
        proposal,markdown=self.one_proposal()
        self.assertIsNone(proposal['fixture_suggestion'])
        self.assertIsNone(proposal['assertion_change'])
        self.assertIsNone(proposal['human']['verdict'])
        self.assertEqual(len(proposal['human']['stale_labels']),1)
        self.assertIn('label_eval_run.py',markdown)
        self.assertNotIn('--supersede',markdown)

    def test_stale_label_beside_a_current_one_yields_one_card(self):
        self.write_fixture_pair()
        self.raw_label(labeler='ana',rubric_version='b'*12,verdict='fail',classification=['incomplete'],reason='older rubric')
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock',labeler='lucas')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['false-accept'])
        proposal,_=self.one_proposal()
        self.assertEqual([r['labeler'] for r in proposal['human']['stale_labels']],['ana'])
        self.assertEqual([r['labeler'] for r in proposal['human']['labels']],['lucas'])

    def test_eval_defect_beats_false_accept_and_counts_the_rubric_blast(self):
        self.label(verdict='fail',classification=['eval-defect'],reason='The expected output asks for a field the prompt never gives')
        self.label(config='without_skill',verdict='good',reason='fine',labeler='ana')
        index=self.propose()
        outcomes=sorted(row['outcome'] for row in index['outcomes'])
        self.assertEqual(outcomes,['eval-defect','false-reject'])
        defect=[json.loads(p.read_text()) for p in self.out_dir().iterdir() if p.suffix=='.json' and p.stem!='index']
        defect=[d for d in defect if d['category']=='eval-defect'][0]
        self.assertIsNone(defect['fixture_suggestion'])
        self.assertEqual(defect['rubric_impact']['labels_invalidated_if_rubric_changes'],2)

    # -- the guarantees -------------------------------------------------------------
    def test_json_shape_and_no_regex_is_invented(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        proposal,markdown=self.one_proposal()
        self.assertEqual(set(proposal),{'schema','kind','category','status','generated_by','never_edits','run','human',
                                        'grader','implicated_assertions','fixture_suggestion','assertion_change',
                                        'rubric_impact','human_decisions','excerpt','content_sha256','generated_at'})
        self.assertEqual(proposal['schema'],pe.SCHEMA)
        self.assertEqual(proposal['status'],'proposed')
        self.assertIsNone(proposal['assertion_change']['regex'])
        self.assertNotIn('re.compile',markdown)
        inside,offenders=False,[]
        for line in markdown.splitlines():
            if line.startswith('```python'):
                inside=True;continue
            if inside and line.startswith('```'):
                inside=False;continue
            if inside and line.strip() and not line.lstrip().startswith('#'):
                offenders.append(line)
        self.assertEqual(offenders,[],'the proposed assertion block must be entirely commented out')

    def test_nothing_is_applied(self):
        pair=self.write_fixture_pair()
        before={p:p.read_bytes() for p in (self.root/pe.FIXTURES,
                                          self.root/'skills'/self.skill/'evals/evals.json',
                                          self.root/'scripts'/'grade_evals.py')}
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        for path,payload in before.items():
            self.assertEqual(path.read_bytes(),payload,f'{path.name} must not change')
        self.assertEqual(json.loads((self.root/pe.FIXTURES).read_text()),[pair])
        directory=pe.run_dir(self.root,self.iteration,self.skill,self.spec['id'],self.eval,'with_skill')
        self.assertFalse((directory/'grading.json').exists(),'propose must not write the grading record')
        self.assertFalse((self.root/'benchmark_all.json').exists())

    def test_idempotence_and_the_hand_edit_guard(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        markdown_path=[p for p in self.out_dir().iterdir() if p.suffix=='.md' and p.stem!='index'][0]
        first=markdown_path.read_bytes()
        self.propose()
        self.assertEqual(markdown_path.read_bytes(),first,'a second pass over an unchanged run must not churn the file')
        markdown_path.write_bytes(first+b'\nA reviewer note.\n')
        self.propose()
        self.assertTrue(markdown_path.read_text().endswith('A reviewer note.\n'),'an edited proposal must not be overwritten')
        self.propose(force=True)
        self.assertEqual(markdown_path.read_bytes(),first)

    def test_a_changed_verdict_is_reported(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        self.label(verdict='fail',classification=['wrong-decision'],reason='wrong call',labeler='ana')
        self.label(verdict='fail',classification=['wrong-decision'],reason='wrong call too',labeler='bea')
        self.propose()
        proposal,_=self.one_proposal()
        self.assertEqual(proposal['human']['verdict'],'fail')
        self.assertEqual(proposal['fixture_suggestion']['slot'],'bad')

    def second_eval(self):
        """A second labelled run in the same skill, so a --eval filter has something to leave out."""
        spec=json.loads((self.root/'skills'/self.skill/'evals/evals.json').read_text())['evals'][1]
        out=self.root/'second.md';out.write_text(self.good)
        rr.record(argparse.Namespace(skill=self.skill,eval=spec['name'],config='with_skill',iteration=self.iteration,
                                     harness='codex',model='fixture',source='synthetic-test-only',output=out,
                                     tokens=None,duration_ms=None),self.root)
        lr.label(argparse.Namespace(skill=self.skill,eval=spec['name'],config='with_skill',iteration=self.iteration,
                                    verdict='weak',classification=['skipped-method'],reason='misses it here too',
                                    labeler='lucas',labels_file=None,supersede=False),self.root)
        block=self.assertions[self.skill][self.eval]
        return spec,{self.skill:{self.eval:block,spec['name']:block}}

    def test_a_filtered_pass_keeps_the_index_of_the_iteration(self):
        """The index says it covers every label in the iteration, so a --eval pass may not shrink
        it to the one eval it visited and leave the other card on disk, unreferenced."""
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        spec,both=self.second_eval()
        with patch.dict(ge.ASSERTIONS,both):
            self.assertEqual(len(pe.propose(self.args(),self.root)['outcomes']),2)
            index=pe.propose(self.args(eval=spec['name']),self.root)
        self.assertEqual(sorted(row['key']['eval_name'] for row in index['outcomes']),sorted([self.eval,spec['name']]))
        written=json.loads((self.out_dir()/'index.json').read_text())
        named={row['stem'] for row in written['outcomes'] if row.get('stem')}
        on_disk={path.stem for path in self.out_dir().iterdir() if path.suffix=='.json' and path.stem!='index'}
        self.assertEqual(named,on_disk,'a filtered pass must not orphan a card')

    def test_the_index_does_not_churn(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        first=(self.out_dir()/'index.json').read_bytes()
        self.propose()
        self.assertEqual((self.out_dir()/'index.json').read_bytes(),first,'a pass that changed nothing must write no diff')

    def test_a_card_whose_labels_stopped_disagreeing_is_retracted(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        self.label(verdict='good',reason='sound on a second read',labeler='ana')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['split'])
        proposal,markdown=self.one_proposal()
        self.assertEqual(proposal['status'],'retracted')
        self.assertEqual(proposal['retracted_because'],'split')
        self.assertTrue(markdown.startswith('> Retracted:'),markdown[:80])
        self.assertEqual(index['outcomes'][0].get('state'),'retracted')
        self.assertEqual(index['outcomes'][0].get('stem'),[p.stem for p in self.out_dir().iterdir()
                                                           if p.suffix=='.json' and p.stem!='index'][0])
        before=markdown
        self.propose()
        self.assertEqual(self.one_proposal()[1],before,'retracting twice must not stack banners')

    def test_a_card_a_human_decided_is_never_retracted(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        card=[p for p in self.out_dir().iterdir() if p.suffix=='.json' and p.stem!='index'][0]
        record=json.loads(card.read_text());record['status']='accepted'
        card.write_text(json.dumps(record,indent=2)+'\n')
        self.label(verdict='good',reason='sound on a second read',labeler='ana')
        self.propose()
        self.assertEqual(json.loads(card.read_text())['status'],'accepted')

    def test_dry_run_writes_nothing(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose(dry_run=True)
        self.assertFalse(self.out_dir().exists())

    def test_filters(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        index=self.propose(skill='another-skill')
        self.assertEqual(index['outcomes'],[])
        index=self.propose(eval='another-eval')
        self.assertEqual(index['outcomes'],[])

    def test_slot_replacement_not_a_second_object(self):
        pair=self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        self.propose()
        proposal,markdown=self.one_proposal()
        suggestion=proposal['fixture_suggestion']
        self.assertIs(suggestion['pair_exists'],True)
        self.assertEqual(suggestion['pair_index'],0)
        expected=hashlib.sha256(json.dumps(pair['near_miss'],sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
        self.assertEqual(suggestion['current_value_sha256'],expected)
        self.assertEqual(list(suggestion['snippet']),list(pe.FIXTURE_KEYS))
        self.assertIn('not a second object',markdown)
        # the markdown carries only the slot being replaced, not the whole object again
        self.assertEqual(markdown.count('"keyword_only"'),0)
        self.assertIn('"near_miss"',markdown)

    def test_a_candidate_that_equals_another_slot_is_called_out(self):
        pair=self.write_fixture_pair()
        self.assertEqual(pair['good'],self.good)   # the labelled run is the text the good slot holds
        self.label(verdict='fail',classification=['wrong-decision'],reason='wrong call')
        self.propose()
        proposal,markdown=self.one_proposal()
        self.assertEqual(proposal['fixture_suggestion']['slot'],'bad')
        self.assertEqual(proposal['fixture_suggestion']['collides_with_slots'],['good'])
        self.assertIn('cannot be both the answer to accept and the answer to reject',markdown)

    def test_excerpt_is_bounded_unless_asked(self):
        long_text='alpha beta '+('padding '*400)
        self.record_pair('iteration-long',{'with_skill':long_text,'without_skill':'gamma'})
        self.label(iteration='iteration-long',verdict='weak',classification=['skipped-method'],reason='misses the lock')
        with patch.dict(ge.ASSERTIONS,self.assertions):
            pe.propose(self.args(iteration='iteration-long',excerpt_chars=100),self.root)
        out=pe.proposals_dir(self.root,'iteration-long')
        proposal=json.loads([p for p in out.iterdir() if p.suffix=='.json' and p.stem!='index'][0].read_text())
        self.assertIs(proposal['excerpt']['truncated'],True)
        self.assertEqual(proposal['excerpt']['chars'],100)
        self.assertEqual(proposal['excerpt']['output_chars'],len(long_text))
        with patch.dict(ge.ASSERTIONS,self.assertions):
            pe.propose(self.args(iteration='iteration-long',full_output=True,force=True),self.root)
        proposal=json.loads([p for p in out.iterdir() if p.suffix=='.json' and p.stem!='index'][0].read_text())
        self.assertIs(proposal['excerpt']['truncated'],False)

    # -- inputs the pass does not control ---------------------------------------------
    @staticmethod
    def headings_outside_fences(markdown):
        """Every heading a renderer would show, and whether the fences balance. A model output
        with a fence of its own used to close the card's and turn its headings into the card's."""
        headings,opener=[],''
        for line in markdown.splitlines():
            match=re.match(r'^(`{3,})(.*)$',line)
            if match and not opener:
                opener=match.group(1);continue
            if match and opener and len(match.group(1))>=len(opener) and not match.group(2).strip():
                opener='';continue
            if not opener and line.startswith('## '):
                headings.append(line)
        return headings,opener==''

    def test_a_corrupt_grading_record_does_not_abort_the_pass(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='misses the lock')
        directory=pe.run_dir(self.root,self.iteration,self.skill,self.spec['id'],self.eval,'with_skill')
        for broken in ('{"pass_rate": 1.0','[1, 2]','not json at all'):
            (directory/'grading.json').write_text(broken,encoding='utf-8')
            index=self.propose(force=True)
            self.assertEqual([row['outcome'] for row in index['outcomes']],['false-accept'],broken)
            proposal,_=self.one_proposal()
            self.assertIsNone(proposal['grader']['stored_grading_pass_rate'],broken)

    def test_a_label_line_without_supersedes_is_read(self):
        """label_eval_run accepts the key as optional and inserts no default, so a hand-merged
        file can hold a line without it; reading it with [] killed the pass over every label."""
        self.write_fixture_pair()
        self.raw_label(drop=('supersedes',),verdict='weak',classification=['skipped-method'],reason='misses the lock')
        line=lr.labels_path(self.root,self.iteration).read_text(encoding='utf-8').splitlines()[0]
        self.assertNotIn('supersedes',line)
        self.assertEqual(lr.parse_label(line,self.iteration)['verdict'],'weak')
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['false-accept'])
        proposal,_=self.one_proposal()
        self.assertIs(proposal['human']['labels'][0]['supersedes'],False)

    def test_a_fence_in_the_output_cannot_break_the_card(self):
        fenced='alpha beta: synthetic fixture\n\n```python\nprint("hi")\n```\n\n## Verdict from the model\n\nShip it.\n'
        self.record_pair('iteration-fenced',{'with_skill':fenced,'without_skill':self.bad})
        self.label(iteration='iteration-fenced',verdict='weak',classification=['skipped-method'],reason='misses the lock')
        with patch.dict(ge.ASSERTIONS,self.assertions):
            pe.propose(self.args(iteration='iteration-fenced'),self.root)
        out=pe.proposals_dir(self.root,'iteration-fenced')
        markdown=[p for p in out.iterdir() if p.suffix=='.md' and p.stem!='index'][0].read_text(encoding='utf-8')
        headings,balanced=self.headings_outside_fences(markdown)
        self.assertTrue(balanced,'the card\'s fences must balance')
        self.assertNotIn('## Verdict from the model',headings)
        self.assertIn('## What you decide, in this order',headings)

    def test_a_pipe_in_a_reason_stays_in_its_cell(self):
        self.write_fixture_pair()
        self.label(verdict='weak',classification=['skipped-method'],reason='ranks by ARR | ignores the lock')
        self.propose()
        _,markdown=self.one_proposal()
        row=[line for line in markdown.splitlines() if line.startswith('| lucas |')][0]
        self.assertIn(r'ranks by ARR \| ignores the lock',row)
        self.assertEqual(len(re.findall(r'(?<!\\)\|',row)),6)

    # -- runs the proposer cannot use -----------------------------------------------
    def test_label_without_a_run_is_reported_never_an_error(self):
        self.raw_label(config='with_skill',output_sha256='c'*64)
        index=self.propose()
        self.assertEqual([row['outcome'] for row in index['outcomes']],['hash-mismatch'])
        self.assertEqual(self.written(),['index.json','index.md'])

    def test_missing_and_invalid_runs(self):
        self.label()
        shutil.rmtree(self.root/'skills'/self.skill/'workspace'/self.iteration)
        self.assertEqual([row['outcome'] for row in self.propose()['outcomes']],['no-run-here'])
        self.record_pair(self.iteration,{'with_skill':self.good,'without_skill':self.bad})
        directory=pe.run_dir(self.root,self.iteration,self.skill,self.spec['id'],self.eval,'with_skill')
        (directory/'outputs/output.md').write_text('tampered')
        self.assertEqual([row['outcome'] for row in self.propose()['outcomes']],['invalid-run'])

    def test_bad_iteration_and_malformed_labels(self):
        with self.assertRaises(ValueError):
            pe.propose(self.args(iteration='nope'),self.root)
        path=lr.labels_path(self.root,self.iteration);path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('{"schema": 2}\n',encoding='utf-8')
        with self.assertRaises(ValueError) as caught:
            self.propose()
        self.assertIn('labels.jsonl:1:',str(caught.exception))


class CheckTests(unittest.TestCase):
    """The check mode runs the real suite, so the green path uses the real tree read-only and
    the red paths use a copy of the two directories the suite reads."""

    def check_args(self,**over):
        base=dict(skill='repo-doctor',eval='validate-skill-repo-health',timeout=600)
        base.update(over);return argparse.Namespace(**base)

    def copy_tree(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        root=Path(tmp.name)
        ignore=shutil.ignore_patterns('workspace','__pycache__')
        shutil.copytree(rr.ROOT/'scripts',root/'scripts',ignore=ignore)
        shutil.copytree(rr.ROOT/'skills',root/'skills',ignore=ignore)
        return root

    def edit_pairs(self,root,mutate):
        path=root/pe.FIXTURES
        pairs=json.loads(path.read_text(encoding='utf-8'))
        mutate(pairs)
        path.write_text(json.dumps(pairs,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

    def run_check(self,root,**over):
        from io import StringIO
        from contextlib import redirect_stdout
        buffer=StringIO()
        with redirect_stdout(buffer):
            code=pe.check(self.check_args(**over),root)
        return code,buffer.getvalue()

    def test_green_pair_reports_every_step(self):
        code,text=self.run_check(rr.ROOT)
        self.assertEqual(code,0,text)
        for step in range(1,8):
            self.assertIn(f'step {step}/7',text)
        for suffix in ('-good','-good-wrapped','-good-wrapped-plus-paragraph','-good-wrapped-plus-line',
                       '-good-half-wrapped','-bad','-keyword-only','-near-miss'):
            self.assertIn(f'validate-skill-repo-health{suffix}:',text)
        self.assertIn('does not mean the assertion is right',text)

    def test_a_candidate_outside_its_band_is_named(self):
        root=self.copy_tree()
        def swap(pairs):
            pair=next(p for p in pairs if p['eval']=='validate-skill-repo-health')
            pair['near_miss']['text']=pair['bad']          # a near miss that is really a bad answer
        self.edit_pairs(root,swap)
        code,text=self.run_check(root)
        self.assertEqual(code,1)
        self.assertIn('FAIL  validate-skill-repo-health-near-miss',text)
        self.assertIn('step 4/7',text)
        self.assertIn('Change the near-miss text, not the assertions.',text)

    def test_a_declared_label_no_assertion_carries(self):
        root=self.copy_tree()
        def rename(pairs):
            next(p for p in pairs if p['eval']=='validate-skill-repo-health')['near_miss']['fails']='no assertion says this'
        self.edit_pairs(root,rename)
        code,text=self.run_check(root)
        self.assertEqual(code,1)
        self.assertIn("declared  'no assertion says this'",text)
        self.assertIn('a near miss must fail exactly the assertion it names',text)

    def test_shape_problems_stop_before_the_suite(self):
        root=self.copy_tree()
        def duplicate(pairs):
            pairs.append(json.loads(json.dumps(next(p for p in pairs if p['eval']=='validate-skill-repo-health'))))
        self.edit_pairs(root,duplicate)
        code,text=self.run_check(root)
        self.assertEqual(code,1)
        self.assertIn('a second object for an eval that already has one',text)
        self.assertIn('The suite is not run',text)
        self.assertNotIn('step 2/7',text)

    def test_a_malformed_paste_is_a_sentence_not_a_traceback(self):
        root=self.copy_tree()
        def break_keys(pairs):
            pair=next(p for p in pairs if p['eval']=='validate-skill-repo-health')
            pair.pop('keyword_only')
        self.edit_pairs(root,break_keys)
        code,text=self.run_check(root)
        self.assertEqual(code,1)
        self.assertIn('keys are',text)
        self.assertNotIn('Traceback',text)


if __name__=='__main__':
    unittest.main(verbosity=2)
