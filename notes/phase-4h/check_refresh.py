"""Read-only saved-record bindings; does not execute production validators."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = Path(__file__).resolve().parent
HEAD = '8480f4dfffb57b456d1147fcc5360f7864bb19df'
CACHE = ROOT/'.phase-4-inputs'/HEAD
PREFIX = 'sources/2026-W34/'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    state = read(CACHE/PREFIX/'production-state.json')
    observed = read(LAB/'observation.json')
    changed = {r['filename'] for r in observed['files']}
    bindings = []
    def bind(label, ref):
        assert sha(CACHE/ref['path']) == ref['sha256'], label
        bindings.append({'label': label, **ref})
    bind('State -> active revalidation', state['publication_revalidation_provenance'])
    bind('State -> historical validation checkpoint', state['checkpoint_provenance']['validation'])
    revalidation = read(CACHE/state['publication_revalidation_provenance']['path'])
    assert revalidation['prior_checkpoint'] == state['checkpoint_provenance']['validation']
    assert revalidation['prior_checkpoint']['path'] not in changed
    candidate_path = PREFIX+'publication/v2/publication-candidate-v2.json'
    candidate = read(CACHE/candidate_path)
    checkpoint = read(CACHE/PREFIX/'orchestration/v2/checkpoints/VALIDATED_DRAFT.json')
    bind('New checkpoint -> candidate raw bytes', checkpoint['artifacts'][0])
    bind('New checkpoint -> stage validation', checkpoint['reviews'][0]['result'])
    assert candidate_path not in changed
    assert state['lifecycle_state'] == 'RELEASE_CANDIDATE'
    assert state['human_gates']['publication_preview'] == 'pending'
    assert state['human_gate_provenance']['publication_preview'] is None
    assert state['next_action'] == 'PUBLICATION_PREVIEW'
    for k in ['freeze', 'release']:
        assert state['machine_checkpoints'][k] == 'pending'
    correspondence = {'manuscript': 'reader_manuscript', 'quality_bundle': 'quality_bundle',
                      'semantic_review': 'semantic_review', 'visual_review': 'visual_review', 'pdf': 'pdf'}
    for rk, ck in correspondence.items():
        assert revalidation['validation'][rk]['sha256'] == candidate[ck]['sha256']
        assert candidate[ck]['path'] not in changed
    # Previously captured metadata files are unchanged in the complete compare
    # path list. Validate those bytes, without downloading or certifying the PDF.
    prior = ROOT/'.phase-4-inputs'/observed['previous_weekly_head']
    old_metadata_checks = []
    for ck in ['reader_manuscript', 'quality_bundle', 'semantic_review', 'visual_review']:
        ref = candidate[ck]
        assert sha(prior/ref['path']) == ref['sha256']
        assert (prior/ref['path']).stat().st_size == ref['byte_count']
        old_metadata_checks.append(ck)
    protected = [PREFIX+'architecture-v2.json', PREFIX+'candidate-selection-v2.json',
                 PREFIX+'draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-result.json']
    assert not any(p in changed for p in protected)
    assert not any(p.startswith((PREFIX+'evidence/', 'surveys/weekly/2026-W34/')) for p in changed)
    result = {'scope': 'SAVED_RECORD_BINDINGS_AND_DIFF_NOT_FULL_STATE_VALIDATION',
              'main': observed['main'], 'weekly_head': HEAD,
              'state': state['lifecycle_state'], 'preview': 'pending',
              'bindings': bindings, 'candidate_file_sha256': sha(CACHE/candidate_path),
              'candidate_payload_digest': candidate['candidate_sha256'],
              'candidate_unchanged_from_f50d229': True,
              'historical_checkpoint_unchanged_by_compare': True,
              'old_metadata_bytes_verified_unchanged': old_metadata_checks,
              'pdf_checked': 'metadata correspondence and unchanged path only; not downloaded or viewed',
              'upstream_and_reader_paths_unchanged_by_compare': True,
              'production_full_state_validator': 'NOT_RUN', 'human_approval_generated': False}
    (LAB/'refresh-result.json').write_bytes((json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
    print('PASS: actual RELEASE_CANDIDATE / preview pending; 4 bindings; unchanged Candidate and reader paths. No quality or full State certification.')


if __name__ == '__main__':
    main()
