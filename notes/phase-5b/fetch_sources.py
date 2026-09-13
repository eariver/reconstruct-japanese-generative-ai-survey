"""Capture fixed arXiv versions; preserve prior captures; no production writes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request
import sys

ROOT = Path(__file__).resolve().parent
SOURCES = [('mem0', '2504.19413v1'), ('a-mem', '2502.12110v5'), ('memos', '2507.03724v1')]
manifest = ROOT / 'source-manifest.json'
rows = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else []
for name, version in SOURCES:
    if len(sys.argv) > 1 and name != sys.argv[1]:
        continue
    for kind in ('abs', 'html'):
        url = f'https://arxiv.org/{kind}/{version}'
        at = datetime.now(timezone.utc).isoformat()
        request = urllib.request.Request(url, headers={'User-Agent': 'J-GAS-reconstruct-research/1.0'})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                final_url = response.url
                content_type = response.headers.get('Content-Type')
            target = ROOT / 'sources' / 'raw' / f'{name}-{version}-{kind}.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            row = dict(name=name, version=version, kind=kind, requested_url=url, final_url=final_url, accessed_at_utc=at, content_type=content_type, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), path=target.relative_to(ROOT).as_posix())
        except Exception as error:
            row = dict(name=name, version=version, kind=kind, requested_url=url, accessed_at_utc=at, error=str(error))
        rows = [r for r in rows if (r['name'], r['version'], r['kind']) != (name, version, kind)]
        rows.append(row)
        (ROOT / 'source-manifest.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(row, ensure_ascii=False), flush=True)
