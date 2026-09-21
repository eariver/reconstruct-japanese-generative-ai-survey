"""Seal external evidence and copy the unchanged candidate for independent review.

This records a review input identity, not a final-audit PASS or proof that its
preconditions hold. Auditor must judge preconditions and acceptance independently.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CANDIDATE = Path('/tmp/jgas-rephase-application-r2')
AUDIT = Path('/tmp/jgas-rephase-application-audit-r2')


def git(*args, cwd=CANDIDATE):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()


def main():
    expected = json.loads((HERE / 'application-candidate.json').read_text())
    assert not AUDIT.exists(), 'Never overwrite an earlier audit workspace'
    assert git('rev-parse', 'HEAD') == expected['candidate_head']
    assert git('rev-parse', 'HEAD^{tree}') == expected['candidate_tree']
    assert git('rev-parse', 'HEAD^') == expected['baseline']
    assert git('diff', '--name-only') == '' and git('diff', '--cached', '--name-only') == ''
    # One changed Markdown Status line preserves its existing two-space hard
    # break. Record the raw diagnostic; do not rewrite reviewed r2 formatting.
    whitespace = subprocess.run(['git', 'diff', '--check', expected['baseline'], expected['candidate_head']],
                                cwd=CANDIDATE, capture_output=True, text=True)
    assert whitespace.returncode in (0, 2)
    expected['raw_diff_check'] = dict(returncode=whitespace.returncode, output=whitespace.stdout + whitespace.stderr)
    git('-c', 'core.whitespace=-blank-at-eol', 'diff', '--check', expected['baseline'], expected['candidate_head'])
    rows = expected['candidate_files']
    for row in rows:
        assert hashlib.sha256((CANDIDATE / row['path']).read_bytes()).hexdigest() == row['proposed_sha256']
    delta = subprocess.check_output(['git', 'diff', '--binary', expected['baseline'], expected['candidate_head']], cwd=CANDIDATE)
    (HERE / 'application.patch').write_bytes(delta)
    (HERE / 'candidate-commit.txt').write_bytes(subprocess.check_output(['git', 'cat-file', 'commit', expected['candidate_head']], cwd=CANDIDATE))
    # copy2 copies bytes; no hardlinks or shared alternates/database.
    shutil.copytree(CANDIDATE, AUDIT, copy_function=shutil.copy2, symlinks=True,
                    ignore=shutil.ignore_patterns('__pycache__'))
    assert git('rev-parse', '--absolute-git-dir', cwd=AUDIT) == str(AUDIT / '.git')
    assert not (AUDIT / '.git/objects/info/alternates').exists()
    assert git('remote', 'get-url', 'origin', cwd=AUDIT) == expected['origin']
    assert git('rev-parse', 'HEAD', cwd=AUDIT) == expected['candidate_head']
    assert not git('diff', '--name-only', cwd=AUDIT)
    expected['auditor_fixture'] = str(AUDIT)
    historical = json.loads((ROOT / 'notes/phase-5-upstream-reconciliation/inputs.json').read_text())
    expected['historical_witness_source_continuity'] = []
    for row in historical:
        if row['path'].split('/')[0] not in {'scripts', 'schemas', 'tests'}:
            continue
        actual = hashlib.sha256((CANDIDATE / row['path']).read_bytes()).hexdigest()
        assert actual == row['sha256'] and row['ref'] == expected['baseline']
        expected['historical_witness_source_continuity'].append(dict(path=row['path'], sha256=actual))
    paths = [p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
             and p.name not in ['review-input.json'] and 'auditor' not in p.parts]
    prior = [ROOT / 'notes/phase-5-upstream-reconciliation' / name for name in ['README.md','probe.py','probe-results.json','inputs.json']]
    prior += [ROOT / 'notes/rephase-1-connection' / name for name in ['candidate.patch','candidate-files.json','independent-review.md','independent-review-input.json','independent-review-closeout.json','checks.json']]
    prior += [ROOT / 'notes/rephase-1-integration' / name for name in ['README.md','results.json']]
    expected['evidence'] = [dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(set(paths+prior))]
    expected['status'] = 'SEALED_APPLICATION_REVIEW_INPUT; NOT_FINAL_AUDIT_PASS'
    (HERE / 'review-input.json').write_text(json.dumps(expected, indent=2) + '\n')
    print(json.dumps({'head':expected['candidate_head'],'auditor_fixture':str(AUDIT),'evidence_files':len(expected['evidence'])}))


if __name__ == '__main__':
    main()
