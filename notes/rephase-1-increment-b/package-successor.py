import hashlib
import json
import shutil
import subprocess
from pathlib import Path

fixture = Path('/tmp/jgas-rephase-increment-b-sol-implementation')
packet = Path('/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-increment-b')
a = '1a9649129d1745fed0b98db46ef15f014407e6fc'
def git(*args):
    return subprocess.check_output(['git', '-C', str(fixture), *args])
head = git('rev-parse', 'HEAD').decode().strip()
parent = git('rev-parse', 'HEAD^').decode().strip()
tree = git('rev-parse', 'HEAD^{tree}').decode().strip()
assert parent == 'cb96ab97045b0d0767f38806809d33e383bac73d', parent
assert git('status', '--porcelain', '--untracked-files=no').strip() == b''
assert not (fixture / '.git/objects/info/alternates').exists()
paths = [x.decode() for x in git('diff', '--name-only', '-z', a, head).split(b'\0') if x]
assert len(paths) == 21, paths
patch = git('diff', '--binary', a, head)
(packet / 'increment-b.patch').write_bytes(patch)
sha = lambda b: hashlib.sha256(b).hexdigest()
rows = []
for relative in paths:
    source = fixture / relative
    assert source.is_file(), relative
    blob = git('show', f'{head}:{relative}')
    data = source.read_bytes()
    assert data == blob, relative
    target = packet / 'changed-files' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    rows.append({'path': relative, 'sha256': sha(data), 'bytes': len(data)})
manifest = {
    'kind': 'Increment B review candidate (not adoption)',
    'fixed_production_baseline': '774dd39a951c9ac3818e83dfffd4c7666efb0a20',
    'increment_a_parent': a,
    'candidate_commit': head,
    'candidate_tree': tree,
    'candidate_parent': parent,
    'isolated_fixture': str(fixture),
    'inert_origin': 'https://example.invalid/rephase-increment-b.git',
    'patch': {'path': 'increment-b.patch', 'sha256': sha(patch), 'bytes': len(patch)},
    'changed_file_copy_root': 'changed-files',
    'changed_files': rows,
}
(packet / 'candidate.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'head': head, 'tree': tree, 'parent': parent, 'patch_sha256': sha(patch), 'changed_paths': len(paths)}, indent=2))