"""Independent read-only candidate/source identity check; no Core imports or fixtures."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/tmp/jgas-rephase-application-r2')
OUT = Path(__file__).resolve().parent
WORKSPACE = OUT.parents[2]
BASE = '774dd39a951c9ac3818e83dfffd4c7666efb0a20'
HEAD = 'd38f023ce200619f7f49ce17a348755f05e0e021'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}, text=True).strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

packet = json.loads((OUT.parent / 'application-candidate.json').read_text())
paths = git('diff', '--name-only', BASE, HEAD).splitlines()
assert paths == sorted(row['path'] for row in packet['candidate_files'])
assert git('rev-parse', 'HEAD') == HEAD
assert git('rev-parse', HEAD + '^') == BASE
assert git('rev-parse', HEAD + '^{tree}') == packet['candidate_tree']
files = []
for row in packet['candidate_files']:
    actual = sha(ROOT / row['path'])
    assert actual == row['proposed_sha256'], row['path']
    files.append({'path': row['path'], 'sha256': actual})

historical = json.loads((WORKSPACE / 'notes/phase-5-upstream-reconciliation/inputs.json').read_text())
unchanged = []
for row in historical:
    if row['path'].startswith(('scripts/', 'schemas/', 'tests/')):
        actual = sha(ROOT / row['path'])
        assert actual == row['sha256'], row['path']
        assert git('rev-parse', HEAD + ':' + row['path']) == row['git_blob_sha1']
        unchanged.append({'path': row['path'], 'sha256': actual})

stage = ast.parse((ROOT / 'scripts/survey_stage_validation_v2.py').read_text())
required = next(ast.literal_eval(n.value) for n in stage.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'REQUIRED_CURRENT' for t in n.targets))
schema = json.loads((ROOT / 'schemas/stage-checkpoint-v2.schema.json').read_text())
freeze = schema['$defs']['freezeArtifacts']['then']['properties']['artifacts']['allOf']
schema_required = {v['contains']['properties']['name']['const'] for v in freeze}
assert schema_required - required['RELEASE_CANDIDATE'] == {'visual-review-record'}

result = {
    'scope': 'Independent source and identity inspection; not a new workflow test or final seven-point audit',
    'head': HEAD,
    'tree': packet['candidate_tree'],
    'parent': BASE,
    'origin': git('remote', 'get-url', 'origin'),
    'git_dir': git('rev-parse', '--absolute-git-dir'),
    'alternates_exists': (ROOT / '.git/objects/info/alternates').exists(),
    'candidate_files': files,
    'historical_witness_input_bytes_still_exact': unchanged,
    'freeze_artifact_static_conflict': {
        'runtime_required_exact_set': sorted(required['RELEASE_CANDIDATE']),
        'schema_required_set': sorted(schema_required),
        'runtime_rejects_extras': 'scripts/survey_stage_validation_v2.py:173-176',
        'consequence': 'Providing schema-required visual-review-record as current artifact is rejected by the local stage validator.'
    }
}
assert result['origin'] == 'https://example.invalid/rephase-application.git'
assert not result['alternates_exists']
(OUT / 'source-checks.json').write_text(json.dumps(result, indent=2) + '\n')
(OUT / 'candidate.diff').write_text(git('diff', BASE, HEAD) + '\n')
print(json.dumps(result, indent=2))
