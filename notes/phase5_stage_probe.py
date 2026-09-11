"""Isolated real-Git stage probe. No production mutation or external dispatch.

Linux: python3 -B notes/phase5_stage_probe.py .phase4-lab-snapshot notes/phase5-stage-results.json
Uses jsonschema==4.23.0 and pypdf==6.16.2. Creates disposable local Git fixtures with explicitly local
test identity. These commits are not production approvals or trust admissions.
"""
import copy
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

NOTES = Path(__file__).resolve().parent


def harden(source):
    helper = '''def _load_factual_card(path: Path) -> dict[str, Any]:
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate Evidence Card JSON key: {key}")
            result[key] = value
        return result
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError("Evidence Card must be an object")
    return value


'''
    anchor = 'def validate_evidence_card(\n'
    assert source.count(anchor) == 1
    source = source.replace(anchor, helper + anchor)
    anchor = '    if card.get("schema_version") != "2.0-rc1":\n'
    addition = '''    if repo_root is not None:
        try:
            schema_gate.validate_instance(card, repo_root / CARD_SCHEMA, label="Evidence Card")
        except ValueError as exc:
            return [str(exc)]
    verification = card.get("verification")
    targets = verification.get("targets", []) if isinstance(verification, dict) else []
    if not isinstance(targets, list) or any(not isinstance(row, dict) for row in targets):
        return ["Evidence verification targets must be objects"]
    actual_targets = [row.get("target") for row in targets]
    expected_targets = task.get("verification_targets", [])
    if (any(not isinstance(value, str) for value in actual_targets)
            or len(actual_targets) != len(set(actual_targets))
            or set(actual_targets) != set(expected_targets)):
        return ["Evidence targets must cover the exact task set once each"]
'''
    assert source.count(anchor) == 1
    source = source.replace(anchor, addition + anchor)
    for old, new in [('card = core.load_json(result_path)', 'card = _load_factual_card(result_path)'),
                     ('card = core.load_json(result_files[name])', 'card = _load_factual_card(result_files[name])')]:
        assert source.count(old) == 1
        source = source.replace(old, new)
    return source


def worker(root, case):
    os.chdir(root)
    sys.path.insert(0, str(root))
    from scripts import survey_production_v2 as core
    from scripts import survey_evidence_v2 as evidence
    from scripts import survey_screening_v2 as screening
    from scripts import survey_discovery_v2 as discovery
    from scripts import survey_x_intake_v2 as xintake
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_agent_tool_v2 as runtime
    from scripts import survey_stage_validation_v2 as stage
    from tests import test_survey_evidence_v2 as fixture
    fixture.IMPLEMENTATION_SHA = core.repository_commit_sha(root)
    impl = fixture.IMPLEMENTATION_SHA
    helper = fixture.SurveyEvidenceV2Tests()
    helper.setUp()
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    profile, state = helper.init_profile(root, cfg, 'THEMATIC')
    now = core.parse_instant('2026-09-11T00:00:00Z')
    sr = root / 'sources/SP001'
    (root / 'raw').mkdir()
    (root / 'raw/source.json').write_text('{"fixture": true}\n')
    dp = sr / 'discovery/discovery.jsonl'
    records = [helper.discovery('SP001', 'target-source')]
    screening.write_jsonl(dp, records)
    xm = xintake.build_manifest(root, cfg, profile, {'decision': 'NOT_REQUIRED',
        'rationale': 'Synthetic integration fixture, no community-signal question', 'series_context': None, 'runs': []})
    da = discovery.build_acceptance(root, dp, xm, 'SP001', sr / 'discovery/discovery-accepted-v2.json')

    def advance(artifacts, label):
        report = stage.validate_stage(root, cfg, state, artifacts, sr / (label + '-validation.json'), now)
        reviews = sr / (label + '-reviews.json')
        core.write_json(reviews, {'reviews': [{'check_id': 'CORE_STAGE_CONTRACT', 'kind': 'DETERMINISTIC',
            'executor': 'ISOLATED_TEST_ONLY', 'evidence': 'Actual stage validator in synthetic fixture; no semantic review',
            'result_path': report.relative_to(root).as_posix()}]})
        cp = agent.build_stage_checkpoint(root, cfg, state, artifacts, reviews, 'Isolated machine test only', now)
        agent.advance_with_checkpoint(root, cfg, state, cp)

    advance({'discovery-acceptance': da}, 'discovery')
    with runtime.current_stage_basis_override():
        dp, sa = helper.make_screening(root, state, records, {'target-source': 'KEEP'})
    advance({'screening-acceptance': sa}, 'screening')
    with runtime.current_stage_basis_override():
        pp = evidence.prepare_evidence_package(root, state, dp, sa, sr / 'evidence/package', impl)
        package = core.load_json(pp)
        meta = package['tasks'][0]
        card = helper.card_for_task(root, pp, meta)
        if case == 'missing_target': card['verification']['targets'] = []
        if case == 'duplicate_target': card['verification']['targets'] *= 2
        if case == 'missing_text': card['claims'][0].pop('text')
        results = pp.parent / 'results'
        result = results / Path(meta['path']).name
        core.write_json(result, card)
        if case == 'duplicate_key':
            result.write_text(result.read_text().replace('"status": "VERIFIED"', '"status": "PARTIAL", "status": "VERIFIED"', 1))
        before_state = state.read_bytes()
        try:
            accepted = evidence.accept_evidence_results(root, pp, results, sr / 'evidence/accepted', impl)
        except ValueError as exc:
            assert before_state == state.read_bytes()
            assert not (sr / 'evidence/accepted').exists()
            return {'case': case, 'stopped_at': 'candidate_acceptance', 'error': str(exc),
                    'state_unchanged_on_reject': True, 'no_accepted_directory': True}
        views = helper.make_views(root, profile, accepted)
        ledger = evidence.build_materiality_ledger(root, profile, dp, sa, accepted, views, impl)
        lp = evidence.write_materiality_ledger(sr / 'materiality.json', ledger)
        prof = core.load_json(profile)
        comp = {'schema_version': '2.0-rc1', 'issue_id': 'SP001', 'research_profile': 'THEMATIC',
            'basis': {'production_profile_sha256': core.sha256_file(profile), 'materiality_ledger_sha256': core.sha256_file(lp)},
            'overall_status': 'READY', 'obligations': [
                {'obligation_id': obligation['obligation_id'], 'dimension': obligation['dimension'], 'description': obligation['description'],
                 'status': 'SATISFIED', 'discovery_ids': ['target-source'], 'evidence_task_ids': [meta['evidence_task_id']],
                 'rationale': 'Fixture only, not a semantic completion claim'} for obligation in prof['research_scope']['initial_obligations']],
            'residual_limitations': [], 'closure': {'expansion_passes': 1, 'final_pass_new_sources': 0,
                'final_pass_new_material_obligations': 0, 'final_pass_new_material_obligations_open': 0,
                'targeted_gap_fill_completed': True, 'open_material_obligations': 0, 'limitations': [], 'status': 'COMPLETE'}}
        comp_path = sr / 'completeness.json'
        core.write_json(comp_path, comp)
    artifacts = {'evidence-acceptance': accepted, 'edition-views-acceptance': views,
                 'materiality-ledger': lp, 'profile-completeness': comp_path}
    advance(artifacts, 'evidence')
    final = core.load_json(state)
    assert final['lifecycle_state'] == 'EVIDENCE_REVIEWED'
    assert final['human_gates'] == {'architecture_review': 'pending', 'publication_preview': 'pending'}
    return {'case': case, 'stopped_at': 'EVIDENCE_REVIEWED', 'human_gates_pending': True,
            'actual_fixture_commit': impl, 'stage_contract_pass': True}


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == '--prepare-history':
    import semantic_handoff_probe as p
    samples = json.loads((NOTES / 'semantic-handoff-probe-results.json').read_text(encoding='utf-8-sig'))
    values = []
    for sample in samples['samples']:
        ref = p.SPECIAL if sample['discovery_id'] == 'SP001-D008' else p.W34
        raw = p.read(sample['paths']['card'], ref)
        assert hashlib.sha256(raw).hexdigest() == sample['card_sha256']
        values.append({'id': sample['discovery_id'], 'ref': ref, 'card_text': raw.decode('utf-8'),
                       'task': p.obj(sample['paths']['task'], ref)})
    (Path(sys.argv[2]) / 'analysis-history-inputs.json').write_text(json.dumps(values), encoding='utf-8')
elif __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == '--worker':
    print(json.dumps(worker(Path(sys.argv[2]).resolve(), sys.argv[3])))
elif __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == '--revalidate':
    root = Path(sys.argv[2]).resolve()
    os.chdir(root)
    sys.path.insert(0, str(root))
    from scripts import survey_production_v2 as core
    from scripts import survey_evidence_v2 as evidence
    from scripts import survey_agent_tool_v2 as runtime
    source_root = root / 'sources'
    before = {str(p.relative_to(root)): core.sha256_file(p) for p in source_root.rglob('*') if p.is_file()}
    accepted = next((root / 'sources/SP001/evidence/accepted').glob('*/evidence-accepted.json'))
    error = None
    try:
        with runtime.current_stage_basis_override():
            evidence.validate_evidence_acceptance(root, accepted, core.repository_commit_sha(root))
    except ValueError as exc:
        error = str(exc)
    after = {str(p.relative_to(root)): core.sha256_file(p) for p in source_root.rglob('*') if p.is_file()}
    assert before == after
    print(json.dumps({'revalidation_error': error, 'historical_and_state_bytes_unchanged': True}))
elif __name__ == '__main__':
    snapshot, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    original = (snapshot / 'scripts/survey_evidence_v2.py').read_text()
    updated = harden(original)
    (NOTES / 'phase5-evidence-boundary-proposal.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), updated.splitlines(True), fromfile='a/scripts/survey_evidence_v2.py',
        tofile='b/scripts/survey_evidence_v2.py')))
    results = []
    for arm in ['fixed_main', 'experimental_hardened']:
        for case in ['valid', 'missing_target', 'duplicate_target', 'missing_text', 'duplicate_key']:
            with tempfile.TemporaryDirectory(prefix='astra-stage-') as td:
                root = Path(td)
                shutil.copytree(snapshot, root, dirs_exist_ok=True, ignore=shutil.ignore_patterns('analysis-paper.raw'))
                if arm == 'experimental_hardened':
                    (root / 'scripts/survey_evidence_v2.py').write_text(updated)
                for cmd in [['git', 'init', '-q'], ['git', 'add', '.'],
                            ['git', '-c', 'user.name=Isolated Fixture', '-c', 'user.email=fixture@example.invalid',
                             'commit', '-qm', 'Isolated fixed-source test; no production authority']]:
                    subprocess.run(cmd, cwd=root, check=True, capture_output=True)
                result = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--worker', str(root), case],
                    capture_output=True, text=True)
                if result.returncode:
                    raise RuntimeError(result.stderr)
                row = {'arm': arm, **json.loads(result.stdout)}
                if arm == 'fixed_main':
                    (root / 'scripts/survey_evidence_v2.py').write_text(updated)
                    subprocess.run(['git', 'add', 'scripts/survey_evidence_v2.py'], cwd=root, check=True, capture_output=True)
                    subprocess.run(['git', '-c', 'user.name=Isolated Fixture', '-c', 'user.email=fixture@example.invalid',
                        'commit', '-qm', 'Isolated successor validator test only'], cwd=root, check=True, capture_output=True)
                    revalidation = subprocess.run([sys.executable, '-B', str(Path(__file__).resolve()), '--revalidate', str(root)],
                        capture_output=True, text=True)
                    if revalidation.returncode:
                        raise RuntimeError(revalidation.stderr)
                    row['successor_validator'] = json.loads(revalidation.stdout)
                    assert (row['successor_validator']['revalidation_error'] is None) == (case == 'valid')
                results.append(row)
                print(json.dumps(row), flush=True)
    assert all(r['stopped_at'] == 'EVIDENCE_REVIEWED' for r in results if r['arm'] == 'fixed_main')
    assert all(r['stopped_at'] == ('EVIDENCE_REVIEWED' if r['case'] == 'valid' else 'candidate_acceptance')
               for r in results if r['arm'] == 'experimental_hardened')
    output.write_text(json.dumps({'scope': 'ISOLATED_STAGE_AND_CHECKPOINT_NOT_PRODUCTION_OR_SEMANTIC_REVIEW',
        'main': '6d748a962d57beff89da7c1b20cb5a9a86c8e261',
        'base_module_sha256': hashlib.sha256(original.encode()).hexdigest(),
        'patched_module_sha256': hashlib.sha256(updated.encode()).hexdigest(), 'results': results}, indent=2) + '\n')
