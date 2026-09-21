"""Independent read-only seal for the bounded B1/B2 review; run with WSL Python."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path('/tmp/jgas-rephase-freeze-b1b2')
OUT = Path(__file__).resolve().parent
UNIT = OUT.parent
EXPECTED = 'bf32edf98ba8f605169d7188bbc764de74ee4f6e'
PARENT = 'd38f023ce200619f7f49ce17a348755f05e0e021'
BASE = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def sha(data):
    return hashlib.sha256(data).hexdigest()

manifest = json.loads((UNIT / 'candidate.json').read_text())
assert git('rev-parse', 'HEAD').decode().strip() == EXPECTED
assert git('rev-parse', 'HEAD^').decode().strip() == PARENT
assert git('rev-parse', 'HEAD^^').decode().strip() == BASE
assert git('rev-parse', 'HEAD^{tree}').decode().strip() == manifest['candidate_tree']
changed = git('diff', '--name-only', PARENT, EXPECTED).decode().splitlines()
assert changed == ['scripts/survey_stage_validation_v2.py', 'tests/test_survey_freeze_stage_boundary_v2.py']
assert not git('diff', '--name-only', 'HEAD').strip()
assert not git('diff', '--cached', '--name-only').strip()
origin = git('remote', 'get-url', 'origin').decode().strip()
assert origin == 'https://example.invalid/rephase-application.git'
git_dir = Path(git('rev-parse', '--absolute-git-dir').decode().strip())
assert git_dir == ROOT / '.git'
assert not (git_dir / 'objects/info/alternates').exists()
files = []
for row in manifest['files']:
    path = row['path']
    worktree = (ROOT / path).read_bytes()
    committed = git('show', EXPECTED + ':' + path)
    assert worktree == committed
    assert sha(committed) == row['sha256']
    prior_unchanged = path not in changed
    if prior_unchanged:
        assert committed == git('show', PARENT + ':' + path)
    files.append(dict(path=path, sha256=sha(committed), unchanged_from_a1=prior_unchanged))
context_paths = [
    'scripts/survey_agent_control_v2.py',
    'scripts/survey_publication_v2.py',
    'schemas/stage-checkpoint-v2.schema.json',
    'schemas/publication-preview-approval-v2.schema.json',
    'tests/test_survey_publication_revalidation_v2.py',
    'tests/test_survey_stage_validation_v2.py',
    'tests/test_survey_agent_control_v2.py',
    'tests/test_survey_publication_v2.py',
]
context = []
for path in context_paths:
    committed = git('show', EXPECTED + ':' + path)
    assert committed == (ROOT / path).read_bytes()
    assert committed == git('show', BASE + ':' + path)
    context.append(dict(path=path, sha256=sha(committed), unchanged_from_fixed_production=True))
evidence = {}
for name in ['before-b1.json', 'before-b1.log', 'before-b2.json', 'before-b2.log', 'targeted-regression.json', 'targeted-regression.log']:
    evidence[name] = sha((UNIT / name).read_bytes())
result = dict(head=EXPECTED, tree=manifest['candidate_tree'], parent=PARENT,
              fixed_production_ancestor=BASE, delta_paths=changed,
              tracked_worktree_and_index_clean=True,
              untracked=git('status', '--porcelain', '--untracked-files=normal').decode().splitlines(),
              git_dir=str(git_dir), origin=origin, alternates=False,
              candidate_files=files, unchanged_context=context, reviewed_root_evidence_sha256=evidence,
              independent_test_runs=0)
(OUT / 'source-checks.json').write_text(json.dumps(result, indent=2) + '\n')
(OUT / 'candidate.diff').write_bytes(git('diff', PARENT, EXPECTED))
print(json.dumps(result, indent=2))
