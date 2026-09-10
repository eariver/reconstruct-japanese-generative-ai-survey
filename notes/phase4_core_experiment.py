"""Linux isolated integration experiment using unmodified fixed upstream modules.

Usage: python3 -B phase4_core_experiment.py SNAPSHOT_DIR RAW_FILE OUTPUT_JSON
Dependencies: jsonschema==4.23.0. Snapshot files and Raw prepared per report.
Synthetic test implementation identity is upstream's fixture constant, not a
trusted runtime admission. No stage transition / Human Gate / production write.
"""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import unittest

NOTES = Path(__file__).resolve().parent
SNAPSHOT = Path(sys.argv[1]).resolve()
RAW = Path(sys.argv[2]).resolve().read_bytes()
OUTPUT = Path(sys.argv[3]).resolve()
assert SNAPSHOT.is_relative_to(NOTES.parent)
os.chdir(SNAPSHOT)
sys.path.insert(0, str(SNAPSHOT))
from tests.test_survey_evidence_v2 import SurveyEvidenceV2Tests, IMPLEMENTATION_SHA
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_screening_v2 as screening
from canonical_candidate_check import check_candidate


def screening_for(helper, root, state, record, target):
    issue = record['issue_id']
    path = root / 'sources' / issue / 'discovery/discovery.jsonl'
    screening.write_jsonl(path, [record])
    package_path = screening.prepare_package(root, state, path, root / 'screening-package', IMPLEMENTATION_SHA)
    package = core.load_json(package_path)
    results = package_path.parent / 'results'
    for batch in package['input']['batches']:
        result = {'schema_version': '2.0-rc1', 'issue_id': issue, 'batch_id': batch['batch_id'],
            'basis': screening.expected_result_basis(root, package_path, package, batch),
            'decisions': [{'discovery_id': record['discovery_id'], 'decision': 'KEEP',
                'reason': 'Isolated integration test, not an editorial selection', 'scope_tags': ['lineage'],
                'duplicate_group': None, 'verification_targets': [target], 'confidence': 'high'}]}
        core.write_json(results / (batch['batch_id'] + '.json'), result)
    return path, screening.accept_results(root, package_path, results, root / 'screening-accepted', IMPLEMENTATION_SHA)


def run_profile(profile_name):
    helper = SurveyEvidenceV2Tests()
    helper.setUp()
    temp, root, cfg = helper.sandbox()
    with temp:
        if profile_name == 'RETROSPECTIVE_PERIOD':
            value = core.thematic_profile(root, cfg, {'issue_id': 'PERIOD-LAB',
                'question': 'Isolated bounded-period contract exercise', 'temporal_mode': 'OPEN_HISTORY_AS_OF',
                'as_of': '2026-09-10T00:00:00Z', 'scope_dimensions': ['lineage']})
            value['research_profile'] = profile_name
            value['research_scope']['temporal_policy'] = {'mode': 'BOUNDED_PERIOD',
                'start': '2026-08-01T00:00:00Z', 'end': '2026-09-01T00:00:00Z',
                'as_of': '2026-09-10T00:00:00Z', 'timezone': 'UTC'}
            value['contract'] = core.contract_identity(root, cfg, profile_name, 'LONGFORM_SPECIAL')
            profile, state = core.initialize(root, cfg, value, IMPLEMENTATION_SHA,
                'ARCHITECTURE_REVIEW', core.parse_instant('2026-09-10T00:00:00Z'))
        else:
            profile, state = helper.init_profile(root, cfg, profile_name)
        issue = core.load_json(state)['issue_id']
        state_before = state.read_bytes()
        authored = json.loads((NOTES / 'phase4-paper-candidate.json').read_text(encoding='utf-8'))
        trace = json.loads((NOTES / 'phase4-source-trace.json').read_text(encoding='utf-8'))
        assert hashlib.sha256(RAW).hexdigest() == trace['raw_sha256']
        record = helper.discovery(issue, 'target-source')
        record['source']['locator'] = authored['sources'][0]['url']
        record['source']['title'] = authored['artifact']['canonical_name']
        target = authored['verification']['targets'][0]['target']
        discovery, accepted_screening = screening_for(helper, root, state, record, target)
        source_root = root / 'sources' / issue
        raw_path = source_root / 'raw/paper.html'
        raw_path.parent.mkdir(parents=True)
        raw_path.write_bytes(RAW)
        source = authored['sources'][0]
        supplement = {'supplement_source_id': source['source_id'], 'discovery_id': 'target-source',
            'evidence_task_id': evidence.stable_task_id(issue, 'target-source'), 'locator': source['url'],
            'source_type': 'paper', 'source_class': source['source_class'], 'title': source['title'],
            'published_at': source['published_at'], 'accessed_at': source['accessed_at'],
            'raw_path': raw_path.relative_to(root).as_posix(), 'raw_sha256': trace['raw_sha256'],
            'byte_count': len(RAW), 'relation': 'Fixed Raw replay in synthetic fixture; no fresh external capture'}
        manifest = evidence.build_evidence_authority_supplement(root, issue, source_root, discovery,
            accepted_screening, [supplement], source_root / 'supplement.json',
            supplement_id='isolated-paper-replay', implementation_sha=IMPLEMENTATION_SHA)
        package_path = evidence.prepare_evidence_package(root, state, discovery, accepted_screening,
            root / 'evidence-package', IMPLEMENTATION_SHA, manifest)
        package = core.load_json(package_path)
        meta = package['tasks'][0]
        scaffold = helper.card_for_task(root, package_path, meta)
        candidate = copy.deepcopy(authored)
        for key in ['schema_version', 'issue_id', 'evidence_task_id', 'basis']:
            candidate[key] = scaffold[key]
        result_dir = root / 'candidate-results'
        candidate_path = result_dir / Path(meta['path']).name
        core.write_json(candidate_path, candidate)
        package_sha = core.sha256_file(package_path)
        before = {str(x.relative_to(root)): core.sha256_file(x) for x in root.rglob('*') if x.is_file()}
        assert check_candidate(root, package_path, candidate_path, package_sha, IMPLEMENTATION_SHA) == candidate
        after = {str(x.relative_to(root)): core.sha256_file(x) for x in root.rglob('*') if x.is_file()}
        assert before == after
        accepted = evidence.accept_evidence_results(root, package_path, result_dir, root / 'accepted', IMPLEMENTATION_SHA)
        evidence.validate_evidence_acceptance(root, accepted, IMPLEMENTATION_SHA)
        accepted_card = accepted.parent / 'results' / candidate_path.name
        assert accepted_card.read_bytes() == candidate_path.read_bytes()
        views = helper.make_views(root, profile, accepted, materiality='CONTEXT')
        evidence.validate_edition_views_acceptance(root, profile, accepted, views, IMPLEMENTATION_SHA)
        assert state.read_bytes() == state_before

        cases = []
        for name in ['missing_target', 'duplicate_target', 'missing_claim_text', 'wrong_subject',
                     'stale_basis', 'supplement_metadata_drift', 'raw_tamper', 'extra_result_file', 'duplicate_json_key']:
            changed = copy.deepcopy(candidate)
            if name == 'missing_target': changed['verification']['targets'] = []
            if name == 'duplicate_target': changed['verification']['targets'] *= 2
            if name == 'missing_claim_text': changed['claims'][0].pop('text')
            if name == 'wrong_subject': changed['metrics'][0]['subject_id'] = 'absent'
            if name == 'stale_basis': changed['basis']['task_sha256'] = '0' * 64
            if name == 'supplement_metadata_drift': changed['sources'][0]['title'] += ' changed'
            case_dir = root / name
            case_file = case_dir / candidate_path.name
            core.write_json(case_file, changed)
            if name == 'duplicate_json_key':
                text = case_file.read_text(encoding='utf-8')
                case_file.write_text(text.replace('"status": "PARTIAL"', '"status": "VERIFIED", "status": "PARTIAL"', 1), encoding='utf-8')
            if name == 'raw_tamper': raw_path.write_bytes(b'!' + RAW[1:])
            if name == 'extra_result_file': (case_dir / 'unexpected.txt').write_text('extra', encoding='utf-8')
            errors = {}
            for route in ['candidate_check', 'direct_core_acceptance']:
                try:
                    if route == 'candidate_check':
                        check_candidate(root, package_path, case_file, package_sha, IMPLEMENTATION_SHA)
                    else:
                        evidence.accept_evidence_results(root, package_path, case_dir,
                            root / (name + '-accepted'), IMPLEMENTATION_SHA)
                    errors[route] = None
                except ValueError as exc:
                    errors[route] = str(exc)
            if name == 'raw_tamper': raw_path.write_bytes(RAW)
            cases.append({'case': name, **errors})
        by_case = {x['case']: x for x in cases}
        for name in ['missing_target', 'duplicate_target', 'missing_claim_text', 'duplicate_json_key']:
            assert by_case[name]['candidate_check'] and by_case[name]['direct_core_acceptance'] is None
        for name in ['wrong_subject', 'stale_basis', 'supplement_metadata_drift', 'raw_tamper']:
            assert by_case[name]['candidate_check'] and by_case[name]['direct_core_acceptance']
        assert by_case['extra_result_file']['candidate_check'] is None
        assert by_case['extra_result_file']['direct_core_acceptance']
        assert state.read_bytes() == state_before
        # Historical accepted bytes still validate after candidate-only failures.
        evidence.validate_evidence_acceptance(root, accepted, IMPLEMENTATION_SHA)
        return {'profile': profile_name, 'accepted_card_exact_bytes': True,
            'accepted_views_validated': True, 'state_bytes_unchanged': True,
            'preflight_no_writes': True, 'prior_acceptance_revalidated': True,
            'card_entities': len(candidate['entities']), 'metrics': len(candidate['metrics']),
            'negative_cases': cases, 'candidate_sha256': core.sha256_file(candidate_path)}


log = io.StringIO()
suite = unittest.defaultTestLoader.loadTestsFromTestCase(SurveyEvidenceV2Tests)
baseline = unittest.TextTestRunner(stream=log, verbosity=1).run(suite)
assert baseline.wasSuccessful(), log.getvalue()
results = [run_profile(name) for name in ['WEEKLY', 'THEMATIC', 'RETROSPECTIVE_PERIOD']]
out = {'scope': 'ISOLATED_REAL_CORE_FUNCTIONS_WITH_SYNTHETIC_FIXTURE_NOT_STAGE_OR_PRODUCTION_ADMISSION',
       'fixed_main': '6d748a962d57beff89da7c1b20cb5a9a86c8e261',
       'python': platform.python_version(), 'system': platform.system(),
       'fixture_implementation_sha': IMPLEMENTATION_SHA,
       'baseline_tests': {'run': baseline.testsRun, 'passed': baseline.wasSuccessful()},
       'profiles': results, 'independent_semantic_review': False, 'stage_transition_tested': False}
OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'baseline_tests': baseline.testsRun, 'profiles': len(results), 'output': str(OUTPUT)}))
