"""Connect unchanged navigation bytes to real fixture Gate revision/approval.

Uses the upstream synthetic research fixture and real authority/Git validators.
It does not establish complete operational prose or real Human review quality.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FIXTURE=Path(os.environ.get('REPHASE_FIXTURE_DIR', str(ROOT/'.rephase-1-inputs/integration-r2'))).resolve()


def main():
    assert sys.platform.startswith('linux') and sys.flags.isolated
    setup=json.loads((HERE/'setup.json').read_text())
    def git(*args):
        return subprocess.run(['git',*args],cwd=FIXTURE,check=True,capture_output=True,text=True).stdout.strip()
    assert Path(git('rev-parse','--show-toplevel')).resolve()==FIXTURE.resolve()
    assert Path(git('rev-parse','--absolute-git-dir')).resolve()==FIXTURE/'.git'
    assert git('rev-parse','HEAD')==setup['synthetic_r2_commit']
    assert git('remote','get-url','origin')=='https://example.invalid/rephase-fixture.git'
    for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
        assert not os.environ.get(key),key
    index_hash=hashlib.sha256((FIXTURE/'.git/index').read_bytes()).hexdigest()
    tempfile.tempdir=str(FIXTURE/'.fixture-scratch')
    os.chdir(FIXTURE);sys.path.insert(0,str(FIXTURE))
    from tests.test_survey_human_gate_v2 import SurveyHumanGateV2Tests
    from scripts import survey_execution_record_v2 as execution
    from scripts import survey_human_gate_v2 as human
    from scripts import survey_production_v2 as core
    SurveyHumanGateV2Tests.setUpClass()
    fixture=SurveyHumanGateV2Tests(methodName='test_architecture_request_changes_regenerates_r2_then_approves')
    points=[]
    try:
        fixture.setUp()
        nav,session=execution.initialize(FIXTURE,fixture.cfg,fixture.profile_path,fixture.state_path,
            session_id='navigation-fixture',started_at='2026-08-24T00:00:00Z',main_sha=fixture.impl,
            branch_head=fixture.impl,objective='Synthetic navigation integration only.',requested_stop='ARCHITECTURE_REVIEW')
        original=nav.read_bytes()
        def check(label):
            assert execution.validate(FIXTURE,fixture.cfg,fixture.profile_path,fixture.state_path)==[]
            assert nav.read_bytes()==original
            state=core.load_json(fixture.state_path)
            points.append(dict(point=label,state=state['lifecycle_state'],gate=state['human_gates']['architecture_review'],
                active_approval=state['human_gate_provenance']['architecture_review'],
                index_sha256=hashlib.sha256(original).hexdigest(),state_sha256=core.sha256_file(fixture.state_path)))
        check('INITIALIZED')
        fixture._advance_to_selection()
        fixture._reach_architecture_gate('SYNTHETIC Architecture r1','2026-08-24T00:05:00Z')
        check('PENDING_R1')
        reviewed_r1=fixture._snapshot_review_commit()
        _,r1,history,_=human.request_architecture_revision(FIXTURE,fixture.cfg,fixture.state_path,
            'SELECTION_COMPLETE','Synthetic fixture clarification.','SYNTHETIC_HUMAN_FIXTURE',
            core.parse_instant('2026-08-24T00:06:00Z'),'fixture:architecture:r1',
            expected_revision=1,reviewed_commit_sha=reviewed_r1)
        check('REQUEST_CHANGES_R1')
        assert core.load_json(r1)['decision']=='REQUEST_CHANGES'
        fixture._reach_architecture_gate('SYNTHETIC Architecture r2','2026-08-24T00:07:00Z')
        check('PENDING_R2')
        reviewed_r2=fixture._snapshot_review_commit()
        _,r2,history=human.record_architecture_approval(FIXTURE,fixture.cfg,fixture.state_path,
            'SYNTHETIC_HUMAN_FIXTURE',core.parse_instant('2026-08-24T00:09:00Z'),'fixture:architecture:r2',
            expected_revision=2,reviewed_commit_sha=reviewed_r2)
        check('APPROVED_R2')
        reviews=core.load_json(history)['reviews']
        assert [(r['revision'],r['decision']) for r in reviews]==[(1,'REQUEST_CHANGES'),(2,'APPROVED')]
        # An absent active approval is rejected, even with historical APPROVED present.
        active=core.load_json(fixture.state_path)['human_gate_provenance']['architecture_review']
        approval=FIXTURE/active['path'];raw=approval.read_bytes()
        approval.unlink()
        try:
            errors=execution.validate(FIXTURE,fixture.cfg,fixture.profile_path,fixture.state_path)
            assert errors
        finally:
            approval.write_bytes(raw)
        check('RESTORED_APPROVAL')
        report=dict(success=True,scope='REAL_STATE_NAVIGATION_AUTHORITY_LINKS_SYNTHETIC_RESEARCH_AND_HUMAN_DECISIONS',
            fixture_commit=fixture.impl,reviewed_commits=[reviewed_r1,reviewed_r2],points=points,
            missing_active_approval_errors=errors,history_approved_did_not_restore_authority=True,
            mocks=False,index_changed=False,full_operational_prose_verified=False)
        (HERE/'navigation-results.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:report[k] for k in ('success','scope','index_changed','history_approved_did_not_restore_authority')},indent=2))
    finally:
        assert fixture.doCleanups()
    assert git('rev-parse','HEAD')==setup['synthetic_r2_commit']
    assert hashlib.sha256((FIXTURE/'.git/index').read_bytes()).hexdigest()==index_hash
    assert 'refs/remotes/' not in git('for-each-ref','--format=%(refname)')


if __name__=='__main__':main()
