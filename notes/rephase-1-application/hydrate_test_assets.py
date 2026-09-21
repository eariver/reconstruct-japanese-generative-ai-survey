"""Materialize only fixed-tree assets required by blocked/skipped local tests."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
CACHE = ROOT / '.rephase-1-inputs' / BASE
FIXTURE = Path('/tmp/jgas-rephase-application-r2')
ACCEPTED = 'sources/SP001/evidence/v2/accepted/3785dc9ee87378b6682cc6d45a064cba1c9325bba4339dc04e460d441dcfb430/'


def main():
    rows = json.loads((CACHE/'tree.json').read_text())['tree']
    selected = [r for r in rows if r['type']=='blob' and (
        (r['path'].startswith('sources/') and len(r['path'].split('/'))==3 and r['path'].endswith('/release-manifest.json'))
        or r['path']=='sources/2026-W32/freeze-v0.2.md'
        or (r['path'].startswith(ACCEPTED) and r['path'].endswith('.json')))]
    assert sum(r['size'] for r in selected) < 5000000
    def acquire(row):
        path = row['path']
        assert not Path(path).is_absolute() and '..' not in Path(path).parts
        cached = CACHE / path
        hit = cached.exists()
        raw = cached.read_bytes() if hit else urlopen(f'https://raw.githubusercontent.com/eariver/japanese-generative-ai-survey/{BASE}/{path}', timeout=30).read()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['sha']
        if not hit:
            cached.parent.mkdir(parents=True, exist_ok=True)
            cached.write_bytes(raw)
        destination = FIXTURE / path
        if destination.exists():
            assert destination.read_bytes() == raw
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
        return dict(path=path, bytes=len(raw), git_blob=row['sha'], sha256=hashlib.sha256(raw).hexdigest(), cache_hit=hit)
    with ThreadPoolExecutor(max_workers=6) as pool:
        report = list(pool.map(acquire, selected))
    (HERE/'test-assets.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(files=len(report), bytes=sum(r['bytes'] for r in report), network_files=sum(not r['cache_hit'] for r in report))))


if __name__=='__main__':
    main()
