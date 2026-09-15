"""Closeout checks and aggregation; does not rerun tests."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FIXTURE=Path(os.environ.get('REPHASE_FIXTURE_DIR', str(ROOT/'.rephase-1-inputs/integration-r2'))).resolve()


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    first=(HERE/'linux-guard-attempt-suite.txt').read_text(encoding='utf-8')
    last=(HERE/'upstream-suite.txt').read_text(encoding='utf-8')
    def passed(text):
        return {cls+'.'+name for name,cls in re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. ok$',text,re.M)}
    expected={cls+'.'+name for name,cls in re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\.',first,re.M)}
    covered=passed(first)|passed(last)
    final=json.loads((HERE/'upstream-results.json').read_text())
    assert final['success'] and not final['blocked_operations']
    assert covered==expected and len(covered)==27
    setup=json.loads((HERE/'setup.json').read_text())
    inputs=json.loads((HERE/'inputs.json').read_text())
    candidate={r['path']:r['proposed_sha256'] for r in setup['candidate_files']}
    for row in inputs:
        assert sha(FIXTURE/row['path'])==candidate.get(row['path'],row['sha256']),row['path']
    def git(root,*args):
        return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True,text=True).stdout.strip()
    assert git(FIXTURE,'rev-parse','HEAD')==setup['synthetic_r2_commit']
    refs=git(FIXTURE,'for-each-ref','--format=%(refname)')
    assert 'refs/remotes/' not in refs
    assert not git(FIXTURE,'diff','--name-only')
    assert not git(FIXTURE,'diff','--cached','--name-only')
    for name in ('cli-results.json','navigation-results.json'):
        assert json.loads((HERE/name).read_text())['success']
    proof=json.loads((HERE.parent/'rephase-1-connection/independent-review-input.json').read_text())
    for row in proof['packet_files']:assert sha(ROOT/row['path'])==row['sha256']
    for row in proof['candidate_files']:
        assert sha(ROOT/'.rephase-1-inputs/contract-candidate-r2'/row['path'])==row['proposed_sha256']
    report=dict(production_baseline=setup['production_baseline'],candidate='r2',
        scope='BOUNDED_SYNTHETIC_GIT_INTEGRATION_NOT_FULL_PUBLICATION_OR_ADOPTION',
        upstream_unique_passes=len(covered),first_linux_passes=len(passed(first)),followup_passes=len(passed(last)),
        passing_test_ids=sorted(covered),cli=json.loads((HERE/'cli-results.json').read_text()),
        navigation=json.loads((HERE/'navigation-results.json').read_text()),
        captured_control_files_unchanged=True,reviewed_r2_and_packet_unchanged=True,
        fixture_head=setup['synthetic_r2_commit'],fixture_refs=refs.splitlines(),
        reconstruct_head=git(ROOT,'rev-parse','HEAD'),production_mutation=False,
        final_audit=False,independent_integration_review=False,net_savings_measured=False)
    (HERE/'results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('scope','upstream_unique_passes','first_linux_passes','followup_passes','captured_control_files_unchanged','reviewed_r2_and_packet_unchanged')},indent=2))


if __name__=='__main__':main()
