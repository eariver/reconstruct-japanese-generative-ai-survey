"""Count delegated validation work on an unmodified, fixed-current-main export.

Linux: PYTHONPATH=.../.phase4-linux-deps python3 -B notes/phase6_validation_work_probe.py
No production writes; synthetic fixture identity is not trusted runtime admission.
"""
from collections import Counter
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import sys
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / '.phase6-lab-snapshot'
os.chdir(SNAPSHOT)
sys.path.insert(0, str(SNAPSHOT))
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from tests.test_survey_evidence_v2 import SurveyEvidenceV2Tests, IMPLEMENTATION_SHA

def measure(n):
    helper = SurveyEvidenceV2Tests()
    helper.setUp()
    temp, root, cfg = helper.sandbox()
    with temp:
        profile, state = helper.init_profile(root, cfg, 'THEMATIC')
        before_state = state.read_bytes()
        issue = core.load_json(state)['issue_id']
        records = [helper.discovery(issue, f'source-{i}') for i in range(n)]
        discovery, screening = helper.make_screening(root, state, records,
            {r['discovery_id']: 'KEEP' for r in records})
        issue_root = root / 'sources' / issue
        sources = []
        for i, record in enumerate(records):
            raw = issue_root / 'raw' / f'authority-{i}.html'
            raw.parent.mkdir(parents=True, exist_ok=True)
            data = f'exact synthetic authority {i}\n'.encode()
            raw.write_bytes(data)
            sources.append({'supplement_source_id': f'supplement-src-{i:016x}',
                'discovery_id': record['discovery_id'],
                'evidence_task_id': evidence.stable_task_id(issue, record['discovery_id']),
                'locator': record['source']['locator'], 'source_type': 'paper',
                'source_class': 'PRIMARY_PAPER', 'title': 'Synthetic authority',
                'published_at': '2026-08-22T00:00:00Z', 'accessed_at': '2026-08-23T00:00:00Z',
                'raw_path': raw.relative_to(root).as_posix(),
                'raw_sha256': hashlib.sha256(data).hexdigest(), 'byte_count': len(data),
                'relation': 'synthetic scaling fixture'})
        manifest = evidence.build_evidence_authority_supplement(root, issue, issue_root,
            discovery, screening, sources, issue_root / 'supplement.json',
            supplement_id='work-count-probe', implementation_sha=IMPLEMENTATION_SHA)
        package_path = evidence.prepare_evidence_package(root, state, discovery, screening,
            root / 'evidence-package', IMPLEMENTATION_SHA, manifest)
        package = core.load_json(package_path)
        result_dir = root / 'candidate-results'
        by_task = {s['evidence_task_id']: s for s in sources}
        for meta in package['tasks']:
            card = helper.card_for_task(root, package_path, meta)
            src = by_task[meta['evidence_task_id']]
            sid = src['supplement_source_id']
            card['sources'][0].update({
                'source_id': sid, 'url': src['locator'], 'source_class': src['source_class'],
                'title': src['title'], 'published_at': src['published_at'], 'accessed_at': src['accessed_at']})
            for item in card['claims'] + card['limitations'] + card['verification']['targets']:
                item['source_ids'] = [sid]
            core.write_json(result_dir / Path(meta['path']).name, card)
        accepted = evidence.accept_evidence_results(root, package_path, result_dir,
            root / 'accepted', IMPLEMENTATION_SHA)
        counts = Counter()
        original_hash = core.sha256_file
        raw_paths = {str((root / s['raw_path']).resolve()) for s in sources}
        def counted_hash(path):
            counts['all_sha256_file_calls'] += 1
            if str(Path(path).resolve()) in raw_paths:
                counts['supplement_raw_sha256_file_calls'] += 1
            return original_hash(path)
        with mock.patch.object(core, 'sha256_file', side_effect=counted_hash), \
             mock.patch.object(evidence, 'validate_evidence_authority_supplement', wraps=evidence.validate_evidence_authority_supplement) as supplement, \
             mock.patch.object(evidence, '_supplement_entries_for_package', wraps=evidence._supplement_entries_for_package) as entries:
            start = time.perf_counter()
            evidence.validate_evidence_acceptance(root, accepted, IMPLEMENTATION_SHA)
            seconds = time.perf_counter() - start
            counts['supplement_validation_calls'] = supplement.call_count
            counts['supplement_entries_calls'] = entries.call_count
        assert state.read_bytes() == before_state
        # A second independent invocation must detect changed Raw; no PASS carry-over.
        raw = root / sources[0]['raw_path']
        original_raw = raw.read_bytes()
        raw.write_bytes(b'!' + original_raw[1:])
        try:
            evidence.validate_evidence_acceptance(root, accepted, IMPLEMENTATION_SHA)
        except ValueError as exc:
            rejection = str(exc)
        else:
            raise AssertionError('Raw tamper accepted')
        row = {'cards': n, 'supplement_sources': n, 'counts': dict(counts),
            'synthetic_seconds': seconds, 'state_unchanged': True, 'later_raw_tamper_rejected': rejection}
        print(json.dumps(row), flush=True)
        return row

if __name__ == '__main__':
    modules = ['tests.test_survey_drafting_basis_v2', 'tests.test_survey_evidence_v2']
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log).run(unittest.defaultTestLoader.loadTestsFromNames(modules))
    assert result.wasSuccessful(), log.getvalue()
    print(log.getvalue(), flush=True)
    rows = [measure(n) for n in [2, 4, 8, 16]]
    output = {'scope': 'UNMODIFIED_CURRENT_CORE_SYNTHETIC_EVIDENCE_ACCEPTANCE_REVALIDATION',
        'fixed_main': '005e59841272464307386abfc11f5b09228f0814',
        'fixture_implementation_sha': IMPLEMENTATION_SHA,
        'python': platform.python_version(), 'system': platform.system(),
        'tests': {'modules': modules, 'run': result.testsRun, 'passed': result.wasSuccessful()},
        'module_sha256': hashlib.sha256((SNAPSHOT / 'scripts/survey_evidence_v2.py').read_bytes()).hexdigest(),
        'instrumentation': 'Delegating wrappers; no return values bypassed or cached. Counts exclude fixture creation.',
        'rows': rows, 'production_execution': False, 'optimization_tested': False}
    (ROOT / 'notes/phase6-validation-work-results.json').write_text(json.dumps(output, indent=2) + '\n')
