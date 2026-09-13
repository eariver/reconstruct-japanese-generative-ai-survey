"""Known-input expressiveness witnesses, not author-cost or production QA tests.

Execute only _refs/_ref_rows from fixed production source. No CLI, writer,
State, Gate, full admission, renderer or model is executed.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path
from typing import Any
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
LAB = Path(__file__).resolve().parent
MAIN = '14781409f6fb8d79e3eb4ad6b4c457764a038fde'
OLD = 'c1703f772837317b81735cd4cc851c715fff1a3b'
PID = 'w34-collaborative-agent-workflows-retrieval'
PACKAGE = f'sources/2026-W34/draft/v2/packages/{PID}/draft-package.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def main():
    rows = read(LAB/'inputs.json')
    oldrow = next(r for r in read(ROOT/'notes/phase-4d/inputs.json')
                  if r['ref'] == OLD and r['path'] == PACKAGE)
    used = rows + [oldrow]
    for row in used:
        raw = (ROOT/'.phase-4-inputs'/row['ref']/row['path']).read_bytes()
        assert len(raw) == row['bytes']
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['git_blob_sha1']
    draft = read(ROOT/'notes/phase-4e/draft-result.lab.json')
    card = read(ROOT/'notes/phase-4f/card-corrective.lab.json')
    package_path = ROOT/'.phase-4-inputs'/OLD/PACKAGE
    package = read(package_path)
    assert digest(package_path) == draft['basis']['draft_package_sha256']
    schemas = ROOT/'.phase-4-inputs'/MAIN/'schemas'
    jsonschema.validate(draft, read(schemas/'draft-v2-result.schema.json'))
    jsonschema.validate(card, read(schemas/'evidence-v2-card.schema.json'))

    path = ROOT/'.phase-4-inputs'/MAIN/'scripts/run_drafting_synthesis_v2_interactive.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'_refs', '_ref_rows'}]
    assert len(functions) == 2
    ns = {'Any': Any}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), ns)
    task_id = card['evidence_task_id']
    item = next(i for i in package['evidence_inputs'] if i['evidence_task_id'] == task_id)
    candidate = next(r for r in package['candidate_matrix']['rows'] if r['candidate_id'] == item['candidate_id'])
    did = candidate['discovery_ids'][0]
    modes = ['NONE', 'CLAIMS', 'LIMITATIONS', 'CLAIMS_AND_LIMITATIONS']
    outputs = {mode: ns['_refs'](package, [] if mode == 'NONE' else [did], mode) for mode in modes}
    target = next(r for r in outputs['CLAIMS'] if r['evidence_id'] == 'claim-2')
    assert len(outputs['CLAIMS']) > 1
    assert all(value != [target] for value in outputs.values())
    # A larger candidate selection only unions more rows. It cannot remove the
    # unwanted claim from this candidate; no exhaustive subset search is needed.
    sources = {s['source_id']: s for s in card['sources']}
    claim_sources = {r['statement_id']: [sources[s]['url'] for s in r['source_ids']] for r in card['claims']}
    assert claim_sources['claim-1'] != claim_sources['claim-2']
    # The 4-F Card is an independent LAB specimen, NOT substituted into the
    # immutable Package above. It illustrates why selecting a row can matter.

    # Two existing-schema Draft variants carry the same text and block identity
    # but distinct row selection. No new body is authored; both are reference
    # discrimination fixtures, NOT asserted source-sufficient prose.
    variants = []
    for ref in outputs['CLAIMS'][:2]:
        variant = copy.deepcopy(draft)
        variant['deck_evidence_refs'] = [ref]
        jsonschema.validate(variant, read(schemas/'draft-v2-result.schema.json'))
        variants.append(variant)
    assert variants[0]['deck_evidence_refs'] != variants[1]['deck_evidence_refs']
    a, b = [copy.deepcopy(v) for v in variants]
    a.pop('deck_evidence_refs'); b.pop('deck_evidence_refs')
    assert a == b
    # These are not full validator passes: attribution/text sufficiency and
    # canonical admission are intentionally outside this reference witness.

    locations = {}
    for row in rows:
        if not row['path'].endswith('.py'):
            continue
        parsed = ast.parse((ROOT/'.phase-4-inputs'/MAIN/row['path']).read_text(encoding='utf-8'))
        locations[row['path']] = {n.name: {'start': n.lineno, 'end': n.end_lineno}
                                 for n in parsed.body if isinstance(n, ast.FunctionDef)}
    result = {
        'scope': 'KNOWN_INPUT_DESIGN_WITNESSES_ONLY_NO_COST_OR_QUALITY_WIN',
        'fixed_inputs_verified': used,
        'lab_inputs': {p: digest(ROOT/p) for p in ['notes/phase-4e/draft-result.lab.json', 'notes/phase-4f/card-corrective.lab.json']},
        'draft_ref_selector': {'discovery_id': did, 'task_id': task_id, 'requested': [target], 'mode_outputs': outputs,
                               'exact_single_claim_reachable': False},
        'card_specimen_claim_urls': claim_sources,
        'schema_only_draft_variants': {'count': 2, 'sole_changed_field': 'deck_evidence_refs',
                                      'same_text_and_identity': True, 'full_validator_or_quality_checked': False},
        'function_locations': locations,
        'limits': ['No comparative author/reviewer timing or token data', 'No independent source review',
                   'No full Core admission, production repair or renderer implementation',
                   'No Special or historical replay execution', 'No proof that direct canonical authoring is cheaper'],
    }
    save(LAB/'comparison-result.json', result)
    print('PASS: 8 fixed inputs; two canonical schemas; current compact selector cannot select one requested claim; two schema-valid reference variants distinguished')


if __name__ == '__main__':
    main()
