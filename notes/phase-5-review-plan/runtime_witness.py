"""Offline structural witnesses against fixed current Core, not a full Core run.

Only the artifact-name admission and missing-review guard functions are extracted
from the captured AST and executed. External effects and production imports are
not run. The shape-only safe-file stub is never an authority-validation result.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
REF = '3e3eebe0cda3a32ac88ae764d279b37768f6bfca'
CACHE = ROOT / '.phase-5-inputs' / REF


def tree(path):
    return ast.parse((CACHE / path).read_text(encoding='utf-8'))


def constant(module, name):
    for node in module.body:
        if isinstance(node, ast.Assign) and any(isinstance(n, ast.Name) and n.id == name for n in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(name)


def function(module, name, globals_):
    node = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == name)
    selected = ast.Module(body=[node], type_ignores=[])
    exec(compile(selected, '<captured-production-function>', 'exec'), globals_)
    return globals_[name]


stage = tree('scripts/survey_stage_validation_v2.py')
controller = tree('scripts/survey_agent_control_v2.py')
release = tree('scripts/survey_release_checkpoint_v2.py')
schema = json.loads((CACHE / 'schemas/stage-checkpoint-v2.schema.json').read_bytes())
approval = json.loads((CACHE / 'sources/2026-W34/gates/publication-preview-approval.json').read_bytes())
required = constant(stage, 'REQUIRED_CURRENT')
local_stages = constant(stage, 'LOCAL_STAGES')
schema_names = {
    item['contains']['properties']['name']['const']
    for item in schema['$defs']['freezeArtifacts']['then']['properties']['artifacts']['allOf']
}
assert schema_names - required['RELEASE_CANDIDATE'] == {'visual-review-record'}

safe_file_calls = []
def shape_only_safe_file(root, path, label):
    safe_file_calls.append(str(path))
    return path

admit = function(stage, '_current_artifacts', dict(
    Path=Path, Any=Any, REQUIRED_CURRENT=required, StageValidationError=ValueError,
    _safe_file=shape_only_safe_file))
try:
    admit(ROOT, {'lifecycle_state': 'RELEASE_CANDIDATE'}, {k: Path(k) for k in schema_names})
    raise AssertionError('Expected current runtime to reject schema-required visual record')
except ValueError as exc:
    admission_error = str(exc)
assert admission_error == 'unexpected current stage artifacts: visual-review-record'
assert not safe_file_calls

# A real Human approval cannot also satisfy the required Stage Checkpoint shape.
# _prior_artifacts applies that schema to every non-null checkpoint pointer.
missing_checkpoint_fields = sorted(set(schema['required']) - set(approval))
assert 'from_state' in missing_checkpoint_fields and 'artifacts' in missing_checkpoint_fields
prior = next(n for n in stage.body if isinstance(n, ast.FunctionDef) and n.name == '_prior_artifacts')
prior_source = ast.get_source_segment((CACHE/'scripts/survey_stage_validation_v2.py').read_text(encoding='utf-8'), prior)
assert 'state.get("checkpoint_provenance", {}).values()' in prior_source
assert 'agent.CHECKPOINT_SCHEMA' in prior_source

# Extract the literal check IDs the actual Release producer places in payload.
producer = next(n for n in release.body if isinstance(n, ast.FunctionDef) and n.name == 'build_release_checkpoint')
payload = next(n.value for n in ast.walk(producer) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'payload' for t in n.targets))
reviews_node = next(value for key,value in zip(payload.keys,payload.values) if isinstance(key,ast.Constant) and key.value=='reviews')
producer_ids = [next(ast.literal_eval(v) for k,v in zip(row.keys,row.values) if isinstance(k,ast.Constant) and k.value=='check_id') for row in reviews_node.elts]
assert producer_ids == ['RELEASE_EXACT_BYTE_RECONCILIATION']
guard = function(controller, '_validate_core_stage_report', dict(
    Path=Path, Any=Any, AgentControlError=ValueError,
    CORE_STAGE_REVIEW_ID=constant(controller,'CORE_STAGE_REVIEW_ID')))
try:
    guard(ROOT, {}, {}, [], [{'check_id': name} for name in producer_ids])
    raise AssertionError('Expected missing CORE_STAGE_CONTRACT guard')
except ValueError as exc:
    release_error = str(exc)
assert release_error == 'local Stage Checkpoint requires exactly one CORE_STAGE_CONTRACT review'
assert 'FROZEN' not in local_stages and 'FROZEN' not in required

paths = ['scripts/survey_stage_validation_v2.py', 'schemas/stage-checkpoint-v2.schema.json',
         'scripts/survey_release_checkpoint_v2.py', 'scripts/survey_agent_control_v2.py',
         'sources/2026-W34/gates/publication-preview-approval.json']
report = dict(
    observed_at_utc=datetime.now(timezone.utc).isoformat(), ref=REF,
    status='KNOWN_RUNTIME_CONTRACT_MISMATCHES_REPRODUCED_LOCALLY_NOT_REPAIRED',
    captured_input_sha256={p:hashlib.sha256((CACHE/p).read_bytes()).hexdigest() for p in paths},
    freeze_schema_required_names=sorted(schema_names),
    freeze_runtime_required_names=sorted(required['RELEASE_CANDIDATE']),
    exact_runtime_admission_error=admission_error,
    file_validation_called_during_rejection=False,
    approval_missing_stage_checkpoint_required_fields=missing_checkpoint_fields,
    prior_loader_schema_conflict='STATIC_REQUIRED_FIELD_WITNESS_NOT_FULL_PRIOR_LOADER_EXECUTION',
    release_producer_review_ids=producer_ids, exact_controller_guard_error=release_error,
    compact_stage_validator_supports_frozen=False,
    limits=[
        'Extracted fixed functions exercise only two early rejection guards, not the production module graph.',
        'Minimal state/review inputs isolate shape errors; no claim these fixtures are full valid production states.',
        'No candidate resolution/revalidation, full schema validation, workflow, release, gate mutation or repair implementation ran.',
        'Reported W33/SP001 recurrence is not independently replayed here.',
        'This evidence identifies repair work; it does not measure total lifecycle savings.'
    ])
with (BASE/'runtime-witness.json').open('w',encoding='utf-8',newline='\n') as f:
    f.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'freeze_error':admission_error,'release_error':release_error,'full_core_run':False}))
