"""Local Python 3.12 workflow diagnostics against the exact application head."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
FIXTURE = Path('/tmp/jgas-rephase-application-r2')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=FIXTURE, text=True).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--selected', nargs='*')
    args = parser.parse_args()
    expected = json.loads((HERE / 'application-candidate.json').read_text())
    assert sys.version_info[:2] == (3, 12)
    assert git('rev-parse', '--absolute-git-dir') == str(FIXTURE / '.git')
    assert git('rev-parse', 'HEAD') == expected['candidate_head']
    assert git('remote', 'get-url', 'origin') == expected['origin']
    assert not (FIXTURE / '.git/objects/info/alternates').exists()
    assert not git('diff', '--name-only') and not git('diff', '--cached', '--name-only')
    name = 'targeted' if args.selected else 'full'
    command = [sys.executable, '-B', '-m', 'unittest']
    command += args.selected + ['-v'] if args.selected else ['discover', '-s', 'tests', '-p', 'test_*.py', '-v']
    start = time.time()
    with (HERE / f'{name}-unittest.txt').open('w') as output:
        result = subprocess.run(command, cwd=FIXTURE, stdout=output, stderr=subprocess.STDOUT)
    report = dict(head=expected['candidate_head'], command=command, cwd=str(FIXTURE),
                  python=sys.version, elapsed_seconds=round(time.time()-start, 3), returncode=result.returncode,
                  dependencies={p:importlib.metadata.version(p) for p in ['jsonschema','pypdf','attrs','referencing','rpds-py','jsonschema-specifications','typing-extensions']},
                  head_after=git('rev-parse','HEAD'), tracked_delta_after=git('diff','--name-only'), staged_delta_after=git('diff','--cached','--name-only'))
    (HERE / f'{name}-results.json').write_text(json.dumps(report, indent=2)+'\n')
    assert report['head_after'] == expected['candidate_head'] and not report['tracked_delta_after'] and not report['staged_delta_after']
    for row in expected['candidate_files']:
        assert hashlib.sha256((FIXTURE / row['path']).read_bytes()).hexdigest() == row['proposed_sha256']
    print(json.dumps(report, indent=2))
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
