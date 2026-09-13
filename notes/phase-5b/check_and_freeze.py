"""Local identity/reference checks, not semantic review or Core admission."""
import hashlib
import json
from pathlib import Path
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / '.phase-5-inputs/python-deps'))
from bs4 import BeautifulSoup

revision = sys.argv[1]
assert revision in ('r1', 'r2')
folder = ROOT / revision
manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
source_rows = {(r['name'], r['version'], r['kind']): r for r in manifest if 'path' in r}
for row in source_rows.values():
    data = (ROOT / row['path']).read_bytes()
    assert len(data) == row['bytes']
    assert hashlib.sha256(data).hexdigest() == row['sha256']
research = json.loads((folder / 'research.json').read_text(encoding='utf-8'))
composition = json.loads((folder / 'composition.json').read_text(encoding='utf-8'))
ids = []
for card in research['cards']:
    for key in ('claims', 'metrics', 'limitations'):
        ids.extend(row['id'] for row in card[key])
assert len(ids) == len(set(ids))
def walk(value):
    if isinstance(value, dict):
        if 'refs' in value:
            assert all(ref in ids for ref in value['refs']), value['refs']
        for item in value.values():
            walk(item)
    elif isinstance(value, list):
        for item in value:
            walk(item)
walk(research)
walk(composition)
soups = {}
for source_id, identity in research['active_source_versions'].items():
    name, version = identity.split('/')
    row = source_rows[name, version, 'html']
    soups[source_id] = BeautifulSoup((ROOT / row['path']).read_bytes(), 'html.parser')
for card in research['cards']:
    for key in ('claims','metrics','limitations'):
        for row in card[key]:
            locators = row.get('locators', [row['locator']] if 'locator' in row else [])
            for locator in locators:
                if not locator.startswith('abs:'):
                    assert soups[card['source']].find(id=locator) is not None, (row['id'],locator)
for version, fragment in re.findall(r'https://arxiv.org/html/([^#)]+)#([^\s)]+)',(folder/'manuscript.md').read_text(encoding='utf-8')):
    assert version != '2507.03724v1', 'HOLD source used in reader manuscript'
    source_id = next(k for k,v in research['active_source_versions'].items() if v.endswith('/'+version))
    assert soups[source_id].find(id=fragment) is not None, fragment

workcopy = folder / 'work-record-at-freeze.md'
if not workcopy.exists():
    workcopy.write_bytes((ROOT/'work-record.md').read_bytes())
paths = [ROOT/'protocol.md', ROOT/'source-manifest.json']
paths += [ROOT/r['path'] for r in source_rows.values()]
paths += [folder/name for name in ('research.json','composition.json','manuscript.md','work-record-at-freeze.md')]
if (folder / 'repair-record.md').exists():
    paths.append(folder / 'repair-record.md')
record = dict(frozen_at_utc=datetime.now(timezone.utc).isoformat(), revision=revision, scope='LOCAL_BYTES_REFERENCES_LOCATORS_NOT_INDEPENDENT_QUALITY_OR_PRODUCTION_ADMISSION', author_read_reviewer_expectations_before_r1_freeze=False, ids_checked=len(ids), passed=True, files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in paths])
target=ROOT/f'{revision}-freeze.json'
assert not target.exists(), 'Refusing to replace a frozen revision'
target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(revision=revision, files=len(paths), ids=len(ids), passed=True),ensure_ascii=False))
