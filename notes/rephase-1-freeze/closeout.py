"""Root evidence binding; not an independent review signature."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git',*args],cwd=root).decode().strip()


def main():
    manifest = json.loads((HERE/'candidate.json').read_text())
    fix = Path(manifest['fixture'])
    assert git(fix,'rev-parse','HEAD') == manifest['candidate_head']
    assert git(fix,'rev-parse','HEAD^{tree}') == manifest['candidate_tree']
    assert git(fix,'rev-parse','HEAD^') == manifest['parent']
    assert git(fix,'rev-parse','HEAD^^') == manifest['production_baseline']
    assert git(fix,'rev-parse','--absolute-git-dir') == str(fix/'.git')
    assert git(fix,'remote','get-url','origin') == 'https://example.invalid/rephase-application.git'
    assert not (fix/'.git/objects/info/alternates').exists()
    assert not git(fix,'diff','--name-only') and not git(fix,'diff','--cached','--name-only')
    for row in manifest['files']:
        assert sha(fix/row['path']) == row['sha256']
    prior = HERE.parent/'rephase-1-application'
    old = json.loads((prior/'application-candidate.json').read_text())
    for row in old['candidate_files']:
        assert sha(fix/row['path']) == row['proposed_sha256']
    seal = json.loads((prior/'review-input.json').read_text())
    for row in seal['evidence']:
        assert sha(ROOT/row['path']) == row['sha256'], row['path']
    source = Path(old['fixture'])
    assert git(source,'rev-parse','HEAD') == old['candidate_head']
    assert not git(source,'diff','--name-only') and not git(source,'diff','--cached','--name-only')
    result = json.loads((HERE/'targeted-regression.json').read_text())
    assert result['head'] == manifest['candidate_head'] and result['exit_code'] == 0
    log = (HERE/'targeted-regression.log').read_text()
    assert 'Ran 24 tests' in log and log.rstrip().endswith('OK')
    assert (HERE/'auditor/review.md').is_file()
    docs = [ROOT/'AGENTS.md',ROOT/'README.md',ROOT/'handoff/rephase-1-continuation.md',
            ROOT/'outputs/rephase-1-freeze-assessment.md',HERE/'README.md']
    links = 0
    for doc in docs:
        for link in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8-sig')):
            if '://' in link or link.startswith('#'):
                continue
            assert (doc.parent/link.split('#')[0]).exists(), (doc,link)
            links += 1
    (HERE/'candidate-commit.txt').write_bytes(subprocess.check_output(['git','cat-file','commit',manifest['candidate_head']],cwd=fix))
    evidence = [dict(path=str(path.relative_to(ROOT)),sha256=sha(path))
                for path in sorted(HERE.rglob('*')) if path.is_file() and path.name!='closeout.json']
    final = dict(candidate_head=manifest['candidate_head'],candidate_tree=manifest['candidate_tree'],
                 final_seven_point_audit_started=False,whole_candidate_readiness='NOT_READY; B3 and broader acceptance remain',
                 prior_sealed_evidence_verified=len(seal['evidence']),unchanged_a1_files=len(old['candidate_files']),
                 targeted_tests_passed=24,local_links_checked=links,evidence=evidence,
                 untracked_fixture=git(fix,'status','--porcelain').splitlines(),
                 original_a1_fixture_unchanged=True,production_mutated=False,production_adopted=False)
    (HERE/'closeout.json').write_text(json.dumps(final,indent=2)+'\n')
    print(json.dumps({k:v for k,v in final.items() if k!='evidence'},indent=2))


if __name__=='__main__':
    main()
