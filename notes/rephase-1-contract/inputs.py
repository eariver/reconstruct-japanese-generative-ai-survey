"""Read fixed-baseline blobs; no Git commands, refs, production execution or writes."""
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
REF = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
CACHE = ROOT / '.rephase-1-inputs' / REF
DEST = Path(__file__).resolve().parent


def capture(paths):
    tree = json.loads((CACHE / 'tree.json').read_text(encoding='utf-8'))
    assert tree['sha'] == REF and not tree['truncated']
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
    manifest = DEST / 'inputs.json'
    rows = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
    for path in paths:
        assert path in blobs and '..' not in Path(path).parts and not Path(path).is_absolute()
        raw = None
        for candidate in (CACHE / path, ROOT / '.phase-5-inputs' / REF / path,
                          ROOT / '.phase-5-inputs/upstream-reconciliation' / path):
            if candidate.is_file():
                data = candidate.read_bytes()
                if hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blobs[path]:
                    raw = data
                    break
        url = f'https://raw.githubusercontent.com/eariver/japanese-generative-ai-survey/{REF}/{path}'
        if raw is None:
            with urlopen(url, timeout=30) as response:
                raw = response.read()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == blobs[path]
        target = CACHE / path
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        else:
            assert target.read_bytes() == raw
        rows = [r for r in rows if r['path'] != path] + [dict(
            ref=REF, path=path, sha256=hashlib.sha256(raw).hexdigest(),
            git_blob_sha1=blobs[path], bytes=len(raw), url=url)]
        manifest.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(path)


if __name__ == '__main__':
    capture(sys.argv[1:])
