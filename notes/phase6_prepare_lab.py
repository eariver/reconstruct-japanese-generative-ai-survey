"""Read-only GitHub fixed-tree export; no fetch/pull or production writes."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess

REF = '005e59841272464307386abfc11f5b09228f0814'
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / '.phase6-lab-snapshot'
def api(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', 'repos/eariver/japanese-generative-ai-survey/' + endpoint]))

if __name__ == '__main__':
    assert not DEST.exists(), 'Refuse overwriting a prior export'
    tree = api(f'git/trees/{REF}?recursive=1')
    assert not tree['truncated']
    rows = []
    for entry in tree['tree']:
        rel = entry['path']
        if entry['type'] != 'blob' or rel.split('/')[0] not in {'scripts','schemas','config','docs','tests','.github'}:
            continue
        old = ROOT / '.phase4-lab-snapshot' / rel
        data = old.read_bytes() if old.is_file() else b''
        def blob_sha(value):
            return hashlib.sha1(b'blob ' + str(len(value)).encode() + b'\0' + value).hexdigest()
        reused = blob_sha(data) == entry['sha']
        if not reused:
            blob = api('git/blobs/' + entry['sha'])
            assert blob['encoding'] == 'base64'
            data = base64.b64decode(blob['content'])
        assert blob_sha(data) == entry['sha']
        target = DEST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        rows.append({'path': rel, 'git_blob_sha': entry['sha'], 'reused_exact_bytes': reused})
    manifest = {'fixed_main': REF, 'tree_sha': tree['sha'], 'files': rows}
    (ROOT / 'notes/phase6-lab-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'verified_files': len(rows), 'downloaded': sum(not r['reused_exact_bytes'] for r in rows)}))
