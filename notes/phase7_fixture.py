# Fixture setup copied from phase6 probe; no production execution.
from contextlib import contextmanager
import hashlib
from pathlib import Path
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from tests.test_survey_evidence_v2 import SurveyEvidenceV2Tests, IMPLEMENTATION_SHA

@contextmanager
def fixture(n=2):
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
        yield root, state, package_path, result_dir, sources
