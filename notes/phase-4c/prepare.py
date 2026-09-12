"""Freeze lab contracts and derive readable text; no production execution/writes."""
import base64
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = Path(__file__).resolve().parent
REF = '005e59841272464307386abfc11f5b09228f0814'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if not self.skip and tag in ('p','div','section','h1','h2','h3','h4','tr','li','figcaption'):
            ident = dict(attrs).get('id')
            self.parts.append('\n' + ('[' + ident + '] ' if ident else ''))
    def handle_endtag(self, tag):
        if tag in ('script','style') and self.skip:
            self.skip -= 1
        if not self.skip and tag in ('td','th'):
            self.parts.append(' | ')
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)
    def result(self):
        return '\n'.join(' '.join(x.split()) for x in ''.join(self.parts).splitlines() if x.strip()) + '\n'

if __name__ == '__main__':
    basis = json.loads((ROOT/'notes/phase-4/basis.json').read_text(encoding='utf-8'))
    previous = {(x['ref'],x['path']):x for x in basis['inputs']}
    paths = ['schemas/'+name+'.schema.json' for name in (
        'evidence-v2-task','evidence-v2-card','edition-evidence-view',
        'candidate-selection-v2','draft-v2-package','draft-v2-result')]
    paths += ['config/prompts/evidence-verification-v2.md','config/prompts/article-drafting-v2.md']
    records = []
    for name in paths:
        dst = LAB/'contracts'/name
        cached = ROOT/'.phase-4-inputs'/REF/name
        if (REF,name) in previous and cached.exists():
            raw = cached.read_bytes()
            expected = previous[(REF,name)]
            assert sha(raw) == expected['sha256']
            blob = expected['git_blob_sha1']
            method = 'verified Phase 4-A cache'
        else:
            r = json.loads(subprocess.check_output(['gh','api',f'repos/eariver/japanese-generative-ai-survey/contents/{name}?ref={REF}']))
            raw = base64.b64decode(r['content'])
            blob = r['sha']
            method = 'GitHub GET at fixed ref'
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == blob
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(raw)
        records.append({'path':str(dst.relative_to(ROOT)).replace('\\','/'),'upstream_path':name,'ref':REF,'git_blob_sha1':blob,'sha256':sha(raw),'method':method})
    save(LAB/'contract-manifest.json',{'captured_at':datetime.now(timezone.utc).isoformat(),'contracts':records})
    extracted = []
    for row in json.loads((LAB/'source-manifest.json').read_text(encoding='utf-8'))['sources']:
        raw = (ROOT/row['path']).read_bytes()
        assert sha(raw) == row['sha256']
        parser = Text()
        parser.feed(raw.decode('utf-8'))
        dst = LAB/'sources'/(row['source_id']+'.txt')
        dst.write_text(parser.result(),encoding='utf-8')
        extracted.append({'source_id':row['source_id'],'raw_sha256':sha(raw),'text_path':str(dst.relative_to(ROOT)).replace('\\','/'),'text_sha256':sha(dst.read_bytes())})
    save(LAB/'extraction-manifest.json',{'method':'prepare.py stdlib HTMLParser; scripts/styles removed; no completeness guarantee; raw authoritative','script_sha256':sha(Path(__file__).read_bytes()),'extractions':extracted})
    print(json.dumps({'contracts':len(records),'sources':len(extracted)}))
