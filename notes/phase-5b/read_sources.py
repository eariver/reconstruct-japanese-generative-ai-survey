"""Reading aid with section/paragraph/table IDs; raw HTML remains evidence."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / '.phase-5-inputs/python-deps'))
from bs4 import BeautifulSoup

DEST = Path(__file__).resolve().parent
for name, version in [('mem0', '2504.19413v1'), ('a-mem', '2502.12110v5'), ('memos', '2507.03724v1')]:
    raw_path = DEST / 'sources/raw' / f'{name}-{version}-html.html'
    raw = raw_path.read_bytes()
    soup = BeautifulSoup(raw, 'html.parser')
    for node in soup.select('script, style'):
        node.decompose()
    for node in soup.find_all('math'):
        node.replace_with(node.get('alttext') or node.get_text(' ', strip=True))
    article = soup.find('article') or soup
    lines = []
    for node in article.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'table']):
        if node.find_parent('table'):
            continue
        parent = node.find_parent(id=True)
        locator = node.get('id') or (parent.get('id') if parent else '')
        if node.name == 'table':
            text = '\n'.join(' | '.join(cell.get_text(' ', strip=True) for cell in row.find_all(['th','td'], recursive=False)) for row in node.find_all('tr'))
        else:
            text = node.get_text(' ', strip=True)
        lines.append(f'[{locator}] {text}')
    output = DEST / 'sources' / f'{name}-{version}-reading.txt'
    output.write_text('\n\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(dict(name=name, version=version, raw_sha256=hashlib.sha256(raw).hexdigest(), reading_path=output.relative_to(DEST).as_posix(), blocks=len(lines)), ensure_ascii=False))
