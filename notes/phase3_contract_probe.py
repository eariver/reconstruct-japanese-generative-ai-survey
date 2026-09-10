"""Analysis only: fixed-source function extraction, synthetic cards, persisted delta.

Run: python -B -X utf8 notes/phase3_contract_probe.py
No production imports/writes/acceptance/stage validation. jsonschema is required.
Reads reuse semantic_handoff_probe's fixed-ref, disposable external cache.
"""
import ast
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import semantic_handoff_probe as p

CURRENT_W34 = '2b49ad77eafc4128f5d7dbf7004f767d8e29c078'
R1 = '558d29b091313747fa373a71110e169c3e31b214'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def isolated_validator():
    source = p.txt('scripts/survey_evidence_v2.py')
    names = {'_source_class', '_check_subject_role', 'validate_evidence_card'}
    constants = {'CARD_KEYS', 'EVIDENCE_CLASSES', 'SUBJECT_ROLES', 'SOURCE_CLASS_MAP'}
    nodes = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            nodes.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants for t in node.targets):
            nodes.append(node)

    def instant(value):
        # Only dependency shim. Fixtures use valid UTC instants; time parsing is not tested.
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None:
            raise ValueError('offset required')
        return result

    env = {'Any': Any, 'Path': Path, 'json': json, 'core': SimpleNamespace(parse_instant=instant)}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'fixed-evidence-validator-extract', 'exec'), env)
    return env['validate_evidence_card'], digest(source.encode()), sorted(names)


def fixture():
    instant = '2026-09-10T00:00:00Z'
    task = {'issue_id': 'ANALYSIS-ONLY', 'evidence_task_id': 'synthetic-task',
            'screening_basis': {'screening_acceptance_sha256': 'b' * 64},
            'verification_targets': ['Compare A and B under the same protocol'],
            'source_records': [{'locator': 'https://example.invalid/a', 'source_type': 'PRIMARY_PAPER'},
                               {'locator': 'https://example.invalid/b', 'source_type': 'PRIMARY_REPOSITORY'}]}
    package = {'prompt': {'sha256': 'c' * 64}, 'contracts': {'card': {'sha256': 'd' * 64}}}
    card = {'schema_version': '2.0-rc1', 'issue_id': task['issue_id'], 'evidence_task_id': task['evidence_task_id'],
            'basis': {'task_sha256': 'a' * 64, 'screening_acceptance_sha256': 'b' * 64,
                      'prompt_sha256': 'c' * 64, 'result_contract_sha256': 'd' * 64},
            'status': 'PARTIAL',
            'entities': [{'entity_id': x, 'canonical_name': x, 'entity_type': 'MODEL',
                          'organization': None, 'canonical_url': None} for x in ['A', 'B']],
            'artifact': {'primary_subject_id': 'A', 'artifact_type': 'MODEL', 'canonical_name': 'A', 'canonical_url': None},
            'temporal': {'observed_at': instant, 'events': []},
            'sources': [{'source_id': 'src-' + str(i), 'url': s['locator'], 'source_class': s['source_type'],
                         'title': 'Synthetic source ' + str(i), 'published_at': None, 'accessed_at': instant,
                         'role': 'Synthetic fixture only'} for i, s in enumerate(task['source_records'], 1)],
            'claims': [{'statement_id': 'claim-a', 'text': 'A reports a result under protocol P.',
                        'subject_id': 'A', 'subject_role': 'PRIMARY_SUBJECT', 'evidence_class': 'AUTHOR_CLAIM',
                        'source_ids': ['src-1'], 'context': 'Synthetic locator: table 2; no factual assertion.'},
                       {'statement_id': 'claim-b', 'text': 'B protocol remains unspecified.',
                        'subject_id': 'B', 'subject_role': 'COMPARATOR', 'evidence_class': 'PROJECT_CLAIM',
                        'source_ids': ['src-2'], 'context': 'Synthetic README observation only.'}],
            'metrics': [{'metric_id': 'metric-a', 'name': 'score', 'value': '72', 'unit': '%',
                         'context': 'Synthetic protocol P; B comparability UNRESOLVED, not a ranking.',
                         'subject_id': 'A', 'subject_role': 'PRIMARY_SUBJECT', 'comparison_subject_ids': ['B'],
                         'evidence_class': 'AUTHOR_CLAIM', 'source_ids': ['src-1']}],
            'limitations': [], 'verification': {'targets': [{'target': task['verification_targets'][0],
                'status': 'UNRESOLVED', 'finding': 'B protocol not established; cannot infer a winner.',
                'subject_ids': ['A', 'B'], 'source_ids': ['src-1', 'src-2']}],
                'unresolved_questions': ['B protocol'], 'contradictions': []}}
    return task, package, card


def target_guard(card, task):
    actual = [r['target'] for r in card['verification']['targets']]
    expected = task['verification_targets']
    return len(actual) == len(set(actual)) and set(actual) == set(expected)


def main():
    validate, source_sha, functions = isolated_validator()
    schema = p.obj('schemas/evidence-v2-card.schema.json')
    gate = Draft202012Validator(schema, format_checker=FormatChecker())
    task, package, card = fixture()
    results = []
    for name in ['baseline', 'missing_target', 'duplicate_target', 'unbound_source', 'self_comparator', 'stale_basis', 'ui_claim']:
        value = copy.deepcopy(card)
        if name == 'missing_target': value['verification']['targets'] = []
        if name == 'duplicate_target': value['verification']['targets'] *= 2
        if name == 'unbound_source': value['claims'][0]['source_ids'] = ['absent']
        if name == 'self_comparator': value['metrics'][0]['comparison_subject_ids'] = ['A']
        if name == 'stale_basis': value['basis']['task_sha256'] = 'e' * 64
        if name == 'ui_claim': value['claims'][0]['text'] = 'Content selection saved.'
        structural = [e.message for e in gate.iter_errors(value)]
        relational = validate(value, task, 'a' * 64, package)
        results.append({'case': name, 'schema_errors': structural, 'extracted_validator_errors': relational,
                        'proposed_exact_target_guard': target_guard(value, task)})
    by_name = {r['case']: r for r in results}
    for name in ['baseline', 'missing_target', 'duplicate_target', 'ui_claim']:
        assert not by_name[name]['schema_errors'] and not by_name[name]['extracted_validator_errors']
    for name in ['unbound_source', 'self_comparator', 'stale_basis']:
        assert by_name[name]['extracted_validator_errors']
    assert not by_name['missing_target']['proposed_exact_target_guard']
    assert not by_name['duplicate_target']['proposed_exact_target_guard']

    # A+ and B use the SAME prepared machine fields. B removes four top-level
    # fields, then adds them back. This is a representation comparison, not ROI.
    machine = {k: copy.deepcopy(card[k]) for k in ['schema_version', 'issue_id', 'evidence_task_id', 'basis']}
    payload = {k: copy.deepcopy(v) for k, v in card.items() if k not in machine}
    b_output = {**machine, **payload}
    assert b_output == card
    assert not list(gate.iter_errors(b_output))

    path = 'sources/2026-W34/candidate-selection-v2.json'
    old, new = p.obj(path, R1), p.obj(path, CURRENT_W34)
    old_by = {r['candidate_id']: r for r in old['assignments']}
    new_by = {r['candidate_id']: r for r in new['assignments']}
    assert old_by.keys() == new_by.keys()
    delta = {cid: {k: {'before': old_by[cid].get(k), 'after': new_by[cid].get(k)}
                   for k in old_by[cid].keys() | new_by[cid].keys() if old_by[cid].get(k) != new_by[cid].get(k)}
             for cid in old_by if old_by[cid] != new_by[cid]}
    assert len(delta) == 1
    assert set(next(iter(delta.values()))) == {'architecture_role', 'rationale'}
    matrix_path = 'sources/2026-W34/candidate-matrix-v2.json'
    matrix_bytes = p.read(matrix_path, CURRENT_W34)
    assert p.read(matrix_path, R1) == matrix_bytes
    matrix = json.loads(matrix_bytes)
    assert all(new_by[r['candidate_id']]['profile_extensions'] == r['profile_extensions'] for r in matrix['rows'])
    # Exact prior canonical candidate + explicit semantic delta reconstructs new object.
    replay = copy.deepcopy(old)
    replay['selection_version'] = new['selection_version']
    for row in replay['assignments']:
        for key, change in delta.get(row['candidate_id'], {}).items(): row[key] = change['after']
    assert replay == new
    result = {'scope': 'ANALYSIS_ONLY_NOT_FULL_CORE_OR_SEMANTIC_VALIDATION',
              'refs': {'main': p.MAIN, 'w34_r1': R1, 'w34_current_snapshot': CURRENT_W34, 'special': p.SPECIAL},
              'extraction': {'source_sha256': source_sha, 'functions': functions,
                             'dependency_shim': 'offset-aware instant parser; supplement path not exercised'},
              'synthetic_cases': results,
              'authoring_comparison': {'a_plus_prepared_canonical': card, 'b_machine_fields': machine,
                   'b_same_shape_semantic_payload': payload, 'same_canonical_object': b_output == card,
                   'semantic_quality_and_effort_measured': False},
              'persisted_selection': {'old_sha256': digest(p.read(path, R1)), 'new_sha256': digest(p.read(path, CURRENT_W34)),
                   'matrix_sha256': digest(matrix_bytes), 'matrix_unchanged': True, 'assignments': len(new_by),
                   'delta': delta, 'exact_object_replay': replay == new, 'profile_extensions_equal_matrix_all_rows': True}}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
