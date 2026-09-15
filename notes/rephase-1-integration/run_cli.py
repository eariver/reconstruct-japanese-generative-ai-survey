"""Authentic-loader CLI checks in the independent fixture; no authority mocks."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

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
    head=git('rev-parse','HEAD')
    assert head==setup['synthetic_r2_commit']
    assert git('remote','get-url','origin')=='https://example.invalid/rephase-fixture.git'
    for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
        assert not os.environ.get(key),key
    commands=[]
    def cli(module,*args,expected=0):
        cmd=[sys.executable,'-B','-X','utf8','-m','scripts.'+module,*args]
        result=subprocess.run(cmd,cwd=FIXTURE,capture_output=True,text=True)
        commands.append(dict(module=module,args=list(args),expected=expected,returncode=result.returncode,stdout=result.stdout,stderr=result.stderr))
        (HERE/'cli-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
        assert result.returncode==expected,(cmd,result.stdout,result.stderr)
        return result
    spec_rel='.fixture-scratch/thematic-spec.json'
    spec=dict(issue_id='REPHASE-CLI',question='Synthetic r2 CLI integration only; not a production edition.',
        temporal_mode='OPEN_HISTORY_AS_OF',as_of='2026-09-15T00:00:00Z',scope_dimensions=['execution-record initialization'],
        source_root='sources/REPHASE-CLI',survey_root='surveys/special/REPHASE-CLI',work_branch='test/rephase-cli')
    (FIXTURE/spec_rel).write_text(json.dumps(spec)+'\n')
    initializers=[
        ('weekly','survey_production_v2',['init-weekly','--now','2026-09-08T00:00:00Z','--issue-id','2026-W36']),
        ('thematic','survey_production_v2',['init-thematic','--spec',spec_rel,'--recorded-at','2026-09-15T00:00:00Z']),
        ('retrospective','survey_period_v2',['initialize','--special-slug','2026-M07','--recorded-at','2026-09-15T00:00:00Z'])]
    cases=[]
    for kind,module,args in initializers:
        initialized=json.loads(cli(module,*args).stdout)
        profile,state=initialized['profile'],initialized['state']
        cli('survey_production_v2','validate-state','--state',state)
        profile_path=FIXTURE/profile
        profile_raw=profile_path.read_bytes()
        source=profile_path.parent
        index=source/'execution/index.md'
        init_args=['init','--profile',profile,'--state',state,'--session-id','integration-session',
            '--started-at','2026-09-15T00:00:00Z','--main-sha',head,'--branch-head',head,
            '--objective','SYNTHETIC integration verification, not a production session.','--requested-stop','ARCHITECTURE_REVIEW']
        # Real hash binding must reject even a schema-preserving byte drift before writing index.
        profile_path.write_bytes(profile_raw+b' ')
        try:
            rejected=cli('survey_execution_record_v2',*init_args,expected=2)
            assert 'Production Profile bytes differ from initialized State authority' in rejected.stderr,rejected.stderr
            assert not index.exists()
        finally:
            profile_path.write_bytes(profile_raw)
        cli('survey_execution_record_v2',*init_args)
        index_raw=index.read_bytes()
        assert b'Current lifecycle:' not in index_raw and b'Current State SHA-256:' not in index_raw
        cli('survey_execution_record_v2','validate','--profile',profile,'--state',state)
        repeat=cli('survey_execution_record_v2',*init_args,expected=2)
        assert 'execution index already exists' in repeat.stderr
        assert index.read_bytes()==index_raw
        # Authentic State/Profile issue mismatch, then restore original bytes.
        state_path=FIXTURE/state;state_raw=state_path.read_bytes();bad=json.loads(state_raw)
        bad['issue_id']='WRONG-EDITION'
        state_path.write_text(json.dumps(bad)+'\n')
        try:
            cli('survey_execution_record_v2','validate','--profile',profile,'--state',state,expected=2)
        finally:
            state_path.write_bytes(state_raw)
        cases.append(dict(profile=kind,source=source.relative_to(FIXTURE).as_posix(),
            state_sha256=hashlib.sha256(state_raw).hexdigest(),index_sha256=hashlib.sha256(index_raw).hexdigest(),
            profile_temporal_mode=json.loads(profile_raw)['research_scope']['temporal_policy']['mode']))
    assert git('rev-parse','HEAD')==head
    report=dict(scope='REAL_LOADER_CLI_INITIALIZATION_AND_NEGATIVES_SYNTHETIC_EDITIONS',cases=cases,
        command_count=len(commands),success=True,mocks=False,fixture_commit=head,production_adoption=False)
    (HERE/'cli-results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
