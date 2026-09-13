"""Bounded, GET-only production evidence capture; no production execution."""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent
CACHE = ROOT / '.phase-5-inputs'
REPO = 'eariver/japanese-generative-ai-survey'


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', '--method', 'GET', f'repos/{REPO}/{path}']))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def get(ref, path):
    assert len(ref) == 40 and all(c in '0123456789abcdef' for c in ref)
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    meta = api(f'contents/{path}?ref={ref}')
    raw = base64.b64decode(meta['content']) if meta.get('encoding') == 'base64' else base64.b64decode(api('git/blobs/' + meta['sha'])['content'])
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert blob == meta['sha']
    local = CACHE / ref / path
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_bytes(raw)
    manifest = DEST / 'inputs.json'
    rows = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
    rows = [r for r in rows if (r['ref'], r['path']) != (ref, path)]
    rows.append(dict(ref=ref, path=path, git_blob_sha1=blob, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw), url=f'https://github.com/{REPO}/blob/{ref}/{path}'))
    save(manifest, rows)
    return raw


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1] == 'observe':
        main = api('git/ref/heads/main')['object']['sha']
        head = api('git/ref/heads/weekly/2026-W34-v2-work')['object']['sha']
        base = '8480f4dfffb57b456d1147fcc5360f7864bb19df'
        diff = api(f'compare/{base}...{head}')
        state = json.loads(get(head, 'sources/2026-W34/production-state.json'))
        record = dict(observed_at_utc=datetime.now(timezone.utc).isoformat(), scope='READ_ONLY_REFS_STATE_DIFF_NOT_VALIDATION_OR_QUALITY_APPROVAL', reconstruct_head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), reconstruct_remote_main=subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/main'], cwd=ROOT, text=True).split()[0], main=main, weekly_head=head, previous_weekly_head=base, total_commits=diff['total_commits'], commits=[dict(sha=c['sha'], message=c['commit']['message']) for c in diff['commits']], files=[{k:f[k] for k in ('filename', 'status', 'additions', 'deletions')} for f in diff.get('files', [])], state=state)
        save(DEST / 'observation.json', record)
        print(json.dumps(record, ensure_ascii=False, indent=2))
    else:
        print(get(sys.argv[1], sys.argv[2]).decode('utf-8'))
