"""GET-only fixed-ref evidence capture; never execute or modify production code."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent
REF = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
RECONSTRUCT = 'ec6a502e9ae37e956d677f96f29af6c4e4591fc4'
REPO = 'eariver/japanese-generative-ai-survey'
CACHE = ROOT / '.rephase-1-inputs' / REF


def api(repo, path):
    return json.loads(subprocess.check_output(
        ['gh', 'api', '--method', 'GET', f'repos/{repo}/{path}']))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    record_path = DEST / 'evidence.json'
    if sys.argv[1] == 'observe':
        tree = api(REPO, f'git/trees/{REF}?recursive=1')
        assert not tree['truncated']
        save(CACHE / 'tree.json', tree)
        record = {
            'observed_at_utc': datetime.now(timezone.utc).isoformat(),
            'scope': 'FIXED_REF_SOURCE_AND_RECORD_READING_NOT_EXECUTION_OR_QUALITY_CERTIFICATION',
            'reconstruct_baseline': RECONSTRUCT,
            'production_baseline': REF,
            'reconstruct_local_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'reconstruct_remote_main': api('eariver/reconstruct-japanese-generative-ai-survey', 'git/ref/heads/main')['object']['sha'],
            'production_remote_main': api(REPO, 'git/ref/heads/main')['object']['sha'],
            'tree_truncated': tree['truncated'],
            'tree_entry_count': len(tree['tree']),
            'inputs': [],
        }
        save(record_path, record)
        print(json.dumps({k: v for k, v in record.items() if k != 'inputs'}, indent=2))
        return
    record = json.loads(record_path.read_text(encoding='utf-8'))
    tree = json.loads((CACHE / 'tree.json').read_text(encoding='utf-8'))
    blobs = {r['path']: r['sha'] for r in tree['tree'] if r['type'] == 'blob'}
    for path in sys.argv[1:]:
        assert path in blobs and '..' not in Path(path).parts and not Path(path).is_absolute()
        raw = None
        for candidate in (CACHE / path, ROOT / '.phase-5-inputs' / REF / path,
                          ROOT / '.phase-5-inputs/upstream-reconciliation' / path):
            if candidate.is_file():
                data = candidate.read_bytes()
                if hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == blobs[path]:
                    raw = data
                    break
        if raw is None:
            raw = base64.b64decode(api(REPO, 'git/blobs/' + blobs[path])['content'])
        digest = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert digest == blobs[path]
        target = CACHE / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        row = dict(path=path, git_blob_sha1=digest, sha256=hashlib.sha256(raw).hexdigest(),
                   bytes=len(raw), url=f'https://github.com/{REPO}/blob/{REF}/{path}')
        record['inputs'] = [r for r in record['inputs'] if r['path'] != path] + [row]
        save(record_path, record)
        print(f'{len(raw):8d} {path}')


if __name__ == '__main__':
    main()
