"""Prepare disposable fixed-source lab on Windows; never changes upstream Git.

Run from reconstruct root before the Linux experiment. Refuses an existing lab.
Requirements for Core experiment: jsonschema==4.23.0 (Linux).
Source candidate regeneration additionally uses beautifulsoup4==4.13.5.
"""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

import semantic_handoff_probe as p

workspace = Path(__file__).resolve().parent.parent
destination = workspace / '.phase4-lab-snapshot'
if destination.exists():
    raise ValueError('lab already exists; use a fresh verified workspace for replay')
data = subprocess.check_output(['git', '-C', p.REPO, 'archive', p.MAIN,
    'scripts', 'schemas', 'config', 'docs', 'tests', '.github'])
destination.mkdir()
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    members = archive.getmembers()
    assert all((destination / m.name).resolve().is_relative_to(destination.resolve())
               and (m.isfile() or m.isdir()) for m in members)
    archive.extractall(destination)
samples = json.loads((workspace / 'notes/semantic-handoff-probe-results.json').read_text(encoding='utf-8-sig'))
sample = next(x for x in samples['samples'] if 'arxiv' in x['discovery_id'])
source = sample['sources'][0]
raw = p.read(source['path'], p.W34)
assert hashlib.sha256(raw).hexdigest() == source['sha256']
(destination / 'analysis-paper.raw').write_bytes(raw)
print(json.dumps({'main': p.MAIN, 'archive_sha256': hashlib.sha256(data).hexdigest(),
    'archive_bytes': len(data), 'members': len(members), 'raw_sha256': source['sha256']}))
