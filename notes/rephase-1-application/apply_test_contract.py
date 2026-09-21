"""Add the reviewed test-contract adjustment to a fixed-parent local candidate."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
TARGET = Path('/tmp/jgas-rephase-application-r2')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=TARGET, text=True).strip()


def main():
    initial = json.loads((HERE / 'candidate.json').read_text())
    assert git('rev-parse', '--absolute-git-dir') == str(TARGET / '.git')
    assert git('rev-parse', 'HEAD') == initial['candidate_head']
    assert not git('diff', '--name-only') and not git('diff', '--cached', '--name-only')
    patch = HERE / 'worker/test-contract-update.patch'
    path = 'tests/test_survey_findings_v2.py'
    before = hashlib.sha256((TARGET / path).read_bytes()).hexdigest()
    git('apply', '--check', str(patch))
    git('apply', str(patch))
    assert git('diff', '--name-only') == path
    git('add', '--', path)
    tree = git('write-tree')
    # Keep the original five-file candidate reachable; do not rewrite its commit.
    git('update-ref', 'refs/heads/codex/rephase-r2-original', initial['candidate_head'])
    head = git('commit-tree', tree, '-p', initial['baseline'], '-m',
               'Local application review: r2 plus operating-rule test contract')
    git('update-ref', 'refs/heads/codex/rephase-application-r2', head, initial['candidate_head'])
    assert git('rev-parse', 'HEAD^') == initial['baseline']
    assert not git('diff', '--name-only') and not git('diff', '--cached', '--name-only')
    result = dict(initial)
    result.update(candidate_head=head, candidate_tree=tree, original_r2_head=initial['candidate_head'],
                  application_revision='a1; five r2 production files unchanged plus one contract-test adjustment')
    result['candidate_files'] = initial['candidate_files'] + [dict(path=path, baseline_sha256=before,
                                      proposed_sha256=hashlib.sha256((TARGET/path).read_bytes()).hexdigest())]
    assert sorted(git('diff', '--name-only', initial['baseline'], head).splitlines()) == sorted(r['path'] for r in result['candidate_files'])
    (HERE / 'application-candidate.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(head=head, tree=tree, changed_files=len(result['candidate_files']))))


if __name__ == '__main__':
    main()
