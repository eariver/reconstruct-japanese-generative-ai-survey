"""Independent read-only input identity capture for the bounded B3 design review."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = Path('/tmp/jgas-rephase-freeze-b1b2')
HEAD = 'bf32edf98ba8f605169d7188bbc764de74ee4f6e'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=SOURCE)

def sha(data):
    return hashlib.sha256(data).hexdigest()

assert git('rev-parse', 'HEAD').decode().strip() == HEAD
assert not git('diff', '--name-only').strip()
assert not git('diff', '--cached', '--name-only').strip()
paths = [
    'scripts/survey_weekly_semantic_publication_v2.py',
    'scripts/survey_reader_surface_gate_v2.py',
    'scripts/survey_reader_publication_v2.py',
    'scripts/survey_stage_validation_v2.py',
    'scripts/survey_drafting_v2_base.py',
    'schemas/reader-surface-input-v2.schema.json',
    'schemas/draft-v2-result.schema.json',
    'tests/test_survey_reader_surface_gate_v2.py',
]
sources = []
for path in paths:
    data = (SOURCE / path).read_bytes()
    assert data == git('show', f'{HEAD}:{path}')
    sources.append({'path': path, 'sha256': sha(data), 'matches_committed': True})
root_paths = ['probe.py', 'probe-results.json', 'contract-decision.md', 'worker-analysis.md']
inputs = [{'path': name, 'sha256': sha((HERE.parent / name).read_bytes())} for name in root_paths]
result = {
    'scope': 'INDEPENDENT_BOUNDED_DESIGN_REVIEW_NOT_IMPLEMENTATION_OR_SEVEN_POINT_AUDIT',
    'head': HEAD,
    'tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
    'tracked_worktree_and_index_clean': True,
    'sources': sources,
    'design_inputs': inputs,
    'auditor_tests_executed': False,
    'production_or_network_access': False,
}
(HERE / 'input-hashes.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
