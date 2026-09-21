"""Prepare a sparse, authentic fixed-parent candidate in a separate Linux Git DB.

Fetch only the Human-fixed SHA. Never resolve main. Remove the acquisition
remote after sparse materialization so tests cannot lazily contact production.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
TARGET = Path('/tmp/jgas-rephase-application-r2')


def git(*args):
    result = subprocess.run(['git', *args], cwd=TARGET, capture_output=True, text=True)
    with (HERE / 'acquisition.log').open('a', encoding='utf-8') as log:
        log.write(json.dumps(list(args)) + '\n' + result.stdout + result.stderr)
    result.check_returncode()
    return result.stdout.strip()


def main():
    assert os.name == 'posix' and not TARGET.exists()
    assert not any(k.startswith('GIT_') for k in os.environ), 'No inherited Git overrides'
    TARGET.mkdir()
    git('init', '-b', 'codex/rephase-application-r2')
    assert git('rev-parse', '--absolute-git-dir') == str(TARGET / '.git')
    git('config', 'user.name', 'Rephase Application Review Fixture')
    git('config', 'user.email', 'rephase-fixture@example.invalid')
    git('config', 'commit.gpgsign', 'false')
    git('config', 'core.autocrlf', 'false')
    git('remote', 'add', 'fixed-input', 'https://github.com/eariver/japanese-generative-ai-survey.git')
    git('config', 'remote.fixed-input.promisor', 'true')
    git('config', 'remote.fixed-input.partialclonefilter', 'blob:none')
    git('fetch', '--no-tags', '--depth=1', '--filter=blob:none', 'fixed-input', BASE)
    assert git('rev-parse', 'FETCH_HEAD') == BASE
    git('sparse-checkout', 'init', '--cone')
    git('sparse-checkout', 'set', '.github', 'config', 'docs', 'schemas', 'scripts', 'tests', 'templates', 'specials')
    git('reset', '--hard', BASE)
    git('remote', 'remove', 'fixed-input')
    git('remote', 'add', 'origin', 'https://example.invalid/rephase-application.git')
    assert git('remote', '-v').count('example.invalid') == 2
    assert not (TARGET / '.git/objects/info/alternates').exists()
    rows = json.loads((HERE.parent / 'rephase-1-connection/candidate-files.json').read_text())
    for row in rows:
        source = ROOT / '.rephase-1-inputs/contract-candidate-r2' / row['path']
        raw = source.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['proposed_sha256']
        assert hashlib.sha256((TARGET / row['path']).read_bytes()).hexdigest() == row['baseline_sha256']
        (TARGET / row['path']).write_bytes(raw)
    git('add', '--', *[r['path'] for r in rows])
    git('commit', '-m', 'Local review candidate: r2 operating-rule and live-status separation')
    head = git('rev-parse', 'HEAD')
    assert git('rev-parse', 'HEAD^') == BASE
    assert sorted(git('diff', '--name-only', BASE, head).splitlines()) == sorted(r['path'] for r in rows)
    assert not git('status', '--porcelain')
    report = dict(baseline=BASE, candidate_head=head, candidate_tree=git('rev-parse', 'HEAD^{tree}'),
                  fixture=str(TARGET), git_dir=git('rev-parse', '--absolute-git-dir'),
                  origin=git('remote', 'get-url', 'origin'), authentic_fixed_parent=True,
                  sparse_worktree=True, full_tree_preserved=True, candidate_files=rows,
                  note='Local isolated review commit only. Not production branch/adoption or reconstruct final commit.')
    (HERE / 'candidate.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
