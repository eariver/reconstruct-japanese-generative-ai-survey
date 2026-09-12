"""Read-only, fixed-ref Phase 4 comparison-basis capture; never invokes production Core.

Run from the reconstruct root. Only GitHub GETs and reconstruct-local writes.
The ignored cache is disposable; manifest SHA-256 / Git blob IDs identify inputs.
This is an investigation aid, not an authoring adapter or production authority.
"""
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent
CACHE = ROOT / '.phase-4-inputs'
REPO = 'eariver/japanese-generative-ai-survey'
MAIN = '005e59841272464307386abfc11f5b09228f0814'
EDITION = '601481acd9b82ee8fa0c2eb28a2ca28636165d60'
BRANCH = 'weekly/2026-W34-v2-work'
PREFIX = 'sources/2026-W34/'
RUN = PREFIX + 'execution/luna/w34-screening-evidence-after-sol-discovery-r2/'
records = {}


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/{path}']))


def get(ref, path):
    if path.startswith('/') or '..' in Path(path).parts:
        raise ValueError('Invalid repository-relative path')
    cached = CACHE / ref / path
    # Always obtain the fixed-ref GitHub object identity before reusing cached bytes.
    data = api(f'contents/{path}?ref={ref}')
    if not isinstance(data, dict) or data.get('type') != 'file':
        raise ValueError(f'Expected file: {path}')
    if cached.is_file():
        raw = cached.read_bytes()
    elif data.get('encoding') == 'base64':
        raw = base64.b64decode(data['content'])
    else:
        raw = base64.b64decode(api('git/blobs/' + data['sha'])['content'])
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != data['sha']:
        raise ValueError(f'Git blob mismatch: {path}')
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(raw)
    records[(ref, path)] = {
        'ref': ref, 'path': path, 'git_blob_sha1': blob,
        'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
        'url': f'https://github.com/{REPO}/blob/{ref}/{path}',
    }
    return raw


def obj(ref, path):
    return json.loads(get(ref, path))


def bound(path, expected):
    raw = get(EDITION, path)
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError(f'Binding mismatch: {path}')
    return json.loads(raw)


def one(rows, key, value):
    matches = [row for row in rows if row[key] == value]
    if len(matches) != 1:
        raise ValueError(f'Expected unique {key}: {value}')
    return matches[0]


def trace_slice():
    state = obj(EDITION, PREFIX + 'production-state.json')
    profile = bound(state['profile']['path'], state['profile']['sha256'])
    cp_ref = state['checkpoint_provenance']['evidence']
    cp = bound(cp_ref['path'], cp_ref['sha256'])
    ea_ref = one(cp['artifacts'], 'name', 'evidence-acceptance')
    va_ref = one(cp['artifacts'], 'name', 'edition-views-acceptance')
    ea = bound(ea_ref['path'], ea_ref['sha256'])
    va = bound(va_ref['path'], va_ref['sha256'])
    ebase = str(Path(ea_ref['path']).parent).replace('\\', '/')
    vbase = str(Path(va_ref['path']).parent).replace('\\', '/')
    package = bound(ebase + '/package.json', ea['package_sha256'])
    supplement = bound(package['authority_supplement']['path'], package['authority_supplement']['sha256'])
    ledger = [json.loads(line) for line in get(EDITION, RUN + 'authority-consumption-ledger.jsonl').splitlines() if line.strip()]
    matrix = obj(EDITION, PREFIX + 'candidate-matrix-v2.json')
    selection = obj(EDITION, PREFIX + 'candidate-selection-v2.json')
    architecture = obj(EDITION, PREFIX + 'architecture-v2.json')
    # Check only named bindings for this read-only trace, not full admission closure.
    for name, expected in [('evidence_acceptance_sha256', ea_ref['sha256']),
                           ('edition_views_acceptance_sha256', va_ref['sha256'])]:
        if matrix['basis'][name] != expected:
            raise ValueError('Matrix does not name the checkpoint Evidence/View pair')
    bound(PREFIX + 'candidate-matrix-v2.json', selection['basis']['candidate_matrix_sha256'])
    bound(PREFIX + 'candidate-selection-v2.json', architecture['basis']['candidate_selection_sha256'])
    samples = []
    for did in ['w34-event-c019', 'w34-event-c045', 'w34-event-c033', 'w34-event-arxiv-2608-20771']:
        rows = [r for r in matrix['rows'] if did in r['discovery_ids']]
        if len(rows) != 1:
            raise ValueError(f'Ambiguous matrix row: {did}')
        row = rows[0]
        tid = row['evidence_task_id']
        er = one(ea['results'], 'evidence_task_id', tid)
        vr = one(va['views'], 'evidence_task_id', tid)
        task_meta = one(package['tasks'], 'evidence_task_id', tid)
        task_path = ebase + '/' + task_meta['path']
        task = bound(task_path, task_meta['sha256'])
        card_path = ebase + '/results/' + er['filename']
        card = bound(card_path, row['evidence_sha256'])
        if er['sha256'] != row['evidence_sha256'] or card['basis']['task_sha256'] != task_meta['sha256']:
            raise ValueError('Card/task/acceptance mismatch')
        filename = 'view-' + hashlib.sha256(tid.encode()).hexdigest()[:20] + '.json'
        view_path = vbase + '/views/' + filename
        view = bound(view_path, row['edition_view_sha256'])
        if vr['view_sha256'] != row['edition_view_sha256'] or view['evidence_sha256'] != row['evidence_sha256']:
            raise ValueError('View binding mismatch')
        assigned = one(selection['assignments'], 'candidate_id', row['candidate_id'])
        placements = [p for p in architecture['packages']
                      if row['candidate_id'] in p['primary_candidate_ids'] + p['supporting_candidate_ids']]
        samples.append({
            'discovery_id': did, 'matrix_row': row,
            'task_path': task_path, 'verification_targets': task['verification_targets'],
            'card_path': card_path, 'card': card,
            'view_path': view_path, 'view': view,
            'selection': assigned,
            'reported_consumption': one(ledger, 'discovery_id', did),
            'architecture_placements': [{k: p[k] for k in ['package_id', 'purpose', 'must_cover_requirements', 'boundaries']} for p in placements],
            'source_body_semantic_review_in_this_probe': 'NOT_PERFORMED',
            'reader_text_and_repair_trial': 'NOT_PERFORMED',
        })
    paper_source = one(supplement['sources'], 'supplement_source_id', 'supplement-src-459d624844945528')
    paper_raw = get(EDITION, paper_source['raw_path'])
    if hashlib.sha256(paper_raw).hexdigest() != paper_source['raw_sha256']:
        raise ValueError('Paper Raw binding mismatch')
    anchors = {anchor: paper_raw.find(('id="' + anchor + '"').encode())
               for anchor in ['S3.SS2', 'S3.SS4', 'S4.SS1', 'S4.SS2', 'S7']}
    if any(offset < 0 for offset in anchors.values()):
        raise ValueError('Expected source section missing')
    result = {
        'scope': 'PURPOSIVE_HISTORICAL_CALIBRATION_NOT_BLIND_AB_TRIAL',
        'research_scope': profile['research_scope'],
        'state_summary': {k: state[k] for k in ['lifecycle_state', 'human_gates', 'next_action', 'machine_checkpoints']},
        'active_evidence_ref': ea_ref, 'active_views_ref': va_ref,
        'selection_summary': selection['summary'], 'samples': samples,
        'paper_source_check': {
            'source': paper_source, 'section_byte_offsets_zero_based': anchors,
            'scope': 'Raw hash and section presence checked here; targeted semantic source comparison is recorded in outputs/astra-phase-4-comparison-basis.md section 3. Not a full-paper or independent trial review.',
        },
        'checks': 'Named Git blobs and SHA-256 bindings checked; production Core, Raw closure, complete historical validation, semantic quality and independence NOT checked.',
    }
    (DEST / 'trace.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'trace': 'notes/phase-4/trace.json', 'sample_count': len(samples)}


def save_manifest(extra=None):
    result = {
        'scope': 'READ_ONLY_COMPARISON_BASIS_NOT_CORE_VALIDATION',
        'observed_at_utc': datetime.now(timezone.utc).isoformat(),
        'main_observed': api('git/ref/heads/main')['object']['sha'],
        'edition_branch': BRANCH,
        'edition_observed': api('git/ref/heads/' + BRANCH)['object']['sha'],
        'analysis_main': MAIN, 'analysis_edition': EDITION,
        'inputs': sorted(records.values(), key=lambda r: (r['ref'], r['path'])),
        **(extra or {}),
    }
    (DEST / 'basis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    for path in [
        'docs/survey-production-core-v2-sol-luna-review-governance.md',
        'docs/survey-production-core-v2-session-bootstrap.md',
        'config/prompts/evidence-verification-v2.md',
        'config/prompts/article-drafting-v2.md',
        'config/prompts/profile-synthesis-v2.md',
        'schemas/evidence-v2-task.schema.json',
        'schemas/evidence-v2-card.schema.json',
        'schemas/edition-evidence-view.schema.json',
        'schemas/draft-v2-package.schema.json',
        'scripts/run_drafting_synthesis_v2_agent.py',
        'scripts/run_drafting_synthesis_v2_interactive.py',
        'scripts/run_selection_architecture_v2_interactive.py',
        'scripts/survey_evidence_v2.py',
    ]:
        get(MAIN, path)
    for path in [
        'production-state.json', 'production-profile.json',
        'candidate-matrix-v2.json', 'candidate-selection-v2.json', 'architecture-v2.json',
        'orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json',
        'execution/index.md',
        'execution/reviews/sol-evidence-authority-consumption-review-20260909-r1.md',
        'execution/reviews/sol-selection-directive-20260910-r2.md',
        'execution/reviews/sol-selection-review-20260910-r2.md',
        'execution/reviews/sol-architecture-directive-20260910-r1.md',
        'execution/requests/sol-post-core487-drafting-resume-20260912-r1.md',
    ]:
        get(EDITION, PREFIX + path)
    for filename in ['generate_evidence_input.py', 'body_extract.py', 'product_overrides.py',
                     'session-worklog-evidence-resume.md']:
        get(EDITION, RUN + filename)
    save_manifest(trace_slice())
    print('Captured fixed-ref comparison basis; no production validation or mutation.')
