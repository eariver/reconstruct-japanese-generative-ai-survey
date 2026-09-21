"""Compile/JSON preflights with fixed-ref release manifests; no edition writes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
CACHE = ROOT / '.rephase-1-inputs' / BASE
FIXTURE = Path('/tmp/jgas-rephase-application-r2')


def main():
    assert sys.version_info[:2] == (3, 12)
    expected = json.loads((HERE / 'application-candidate.json').read_text())
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=FIXTURE, text=True).strip() == expected['candidate_head']
    compiled = subprocess.run([sys.executable, '-m', 'compileall', '-q', 'scripts', 'tests'], cwd=FIXTURE, capture_output=True, text=True)
    (HERE / 'compile.txt').write_text(compiled.stdout + compiled.stderr)
    compiled.check_returncode()
    paths = sorted(p for name in ['config','schemas'] for p in (FIXTURE/name).rglob('*.json') if p.is_file())
    assert paths
    for p in paths:
        json.loads(p.read_text(encoding='utf-8'))
    tree = json.loads((CACHE/'tree.json').read_text())
    assert tree['sha'] == BASE and not tree['truncated']
    rows = [r for r in tree['tree'] if r['type']=='blob' and r['path'].startswith('sources/')
            and len(r['path'].split('/'))==3 and r['path'].endswith('/release-manifest.json')]
    assert sum(r['size'] for r in rows) < 3000000
    captured = []
    for row in rows:
        path = CACHE / row['path']
        cached = path.exists()
        raw = path.read_bytes() if cached else urlopen(f'https://raw.githubusercontent.com/eariver/japanese-generative-ai-survey/{BASE}/{row["path"]}', timeout=30).read()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['sha']
        json.loads(raw)
        if not cached:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        captured.append(dict(path=row['path'], sha256=hashlib.sha256(raw).hexdigest(), git_blob=row['sha'], cached=cached))
    report = dict(head=expected['candidate_head'], python=sys.version, compileall_returncode=compiled.returncode,
                  compiled_files=sum(1 for folder in ['scripts','tests'] for p in (FIXTURE/folder).rglob('*.py')),
                  parsed_config_schema_json=len(paths), parsed_fixed_release_manifests=captured,
                  scope='Local workflow compile/JSON equivalent; cached release-manifest parse is not edition validation or live Actions')
    (HERE / 'workflow-checks.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(head=report['head'], compiled_files=report['compiled_files'], parsed_json=len(paths), release_manifests=len(rows))))


if __name__ == '__main__':
    main()
