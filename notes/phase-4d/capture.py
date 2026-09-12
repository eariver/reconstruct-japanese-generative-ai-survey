"""Read-only fixed-ref retrieval for a bounded production work trace."""
import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
DEST=Path(__file__).resolve().parent
CACHE=ROOT/'.phase-4-inputs'
REPO='eariver/japanese-generative-ai-survey'
MAIN='005e59841272464307386abfc11f5b09228f0814'
HEAD='c1703f772837317b81735cd4cc851c715fff1a3b'
BASE='899d3d6ab96c14bb82ea24b0ae12700e798a781f'

def api(path):
    return json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/{path}']))

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def get(ref,path):
    assert not Path(path).is_absolute() and '..' not in Path(path).parts
    meta=api(f'contents/{path}?ref={ref}')
    raw=base64.b64decode(meta['content']) if meta.get('encoding')=='base64' else base64.b64decode(api('git/blobs/'+meta['sha'])['content'])
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert blob==meta['sha']
    dest=CACHE/ref/path
    dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw)
    manifest=DEST/'inputs.json'
    rows=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
    row=dict(ref=ref,path=path,sha256=hashlib.sha256(raw).hexdigest(),git_blob_sha1=blob,bytes=len(raw),url=f'https://github.com/{REPO}/blob/{ref}/{path}')
    rows=[r for r in rows if (r['ref'],r['path'])!=(ref,path)]+[row]
    save(manifest,rows)
    return raw

if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if sys.argv[1]=='observe':
        compare=api(f'compare/{BASE}...{HEAD}')
        record=dict(observed_at=datetime.now(timezone.utc).isoformat(),scope='READ_ONLY_FIXED_PRODUCTION_TRACE_NOT_NEW_TRIAL',main=MAIN,base=BASE,head=HEAD,
            status=compare['status'],total_commits=compare['total_commits'],
            commits=[dict(sha=c['sha'],date=c['commit']['committer']['date'],message=c['commit']['message']) for c in compare['commits']],
            files=[{k:f[k] for k in ('filename','status','additions','deletions')} for f in compare.get('files',[])])
        save(DEST/'observation.json',record)
        print(json.dumps(record,ensure_ascii=False))
    else:
        print(get(sys.argv[1],sys.argv[2]).decode('utf-8'))
