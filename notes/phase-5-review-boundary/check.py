"""Verify the fixed case's bytes and limited bindings, without running production.

Inputs are in the ignored .phase-5-inputs/<ref>/<path> cache. Restore a missing
input with phase-5b/capture.py's get(ref, path), overriding DEST to this folder.
This is a historical witness, not a defect detector or a publication validator.
"""
import hashlib
import json
from pathlib import Path
import re
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CACHE = ROOT / '.phase-5-inputs'
OLD = 'c7faf207515e7429dd74abd5adaf2962725587ef'
NEW = '6be0f462d8f02284f8513d7165c778c3797dcaf4'
REVIEWED = 'f9f3e040843cf49bafbabf76bf6e49c0650e6b98'
PUB = 'sources/2026-W34/publication/v2/'
SURVEY = 'surveys/weekly/2026-W34/'
LEAK = 'regional processing is NOT part of this package after Selection r2; it belongs to Package 4'
REPAIR = 'Regional processing is outside the scope of this section and is discussed with deployment and model-distribution conditions'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def raw(ref, path):
    return (CACHE / ref / path).read_bytes()


def load(ref, path):
    return json.loads(raw(ref, path))


inputs = json.loads((BASE / 'inputs.json').read_text(encoding='utf-8'))
for row in inputs:
    data = raw(row['ref'], row['path'])
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['git_blob_sha1']

manifest = load(OLD, PUB + 'reader-manuscript-v2.json')
semantic = load(OLD, PUB + 'semantic-editorial-review-v2.json')
visual = load(OLD, PUB + 'visual-review-v2.json')
for review in (semantic, visual):
    assert review['reader_manuscript']['sha256'] == sha(raw(OLD, PUB + 'reader-manuscript-v2.json'))
assert semantic['pdf'] == visual['pdf']
for path in (SURVEY + 'sections/20-agent-workflows.tex', SURVEY + 'references.bib'):
    ref = next(r for r in manifest['supporting_files'] if r['path'] == path)
    assert ref['sha256'] == sha(raw(OLD, path)) and ref['byte_count'] == len(raw(OLD, path))

old_tex = raw(OLD, SURVEY + 'sections/20-agent-workflows.tex').decode('utf-8')
new_tex = raw(NEW, SURVEY + 'sections/20-agent-workflows.tex').decode('utf-8')
assert old_tex.count(LEAK) == 1 and LEAK not in new_tex
assert old_tex.replace(LEAK, REPAIR) == new_tex
draft = load(OLD, 'sources/2026-W34/draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-result.json')
block = next(b for b in draft['blocks'] if b['block_type'] == 'CLAIM_BOUNDARY')
assert LEAK in block['text'] and block['text'] in old_tex
boundary_check = next(c for c in semantic['checks'] if c['check_id'] == 'PUBLICATION_BOUNDARY')
assert boundary_check['status'] == 'PASS' and 'sections/20-agent-workflows.tex' in boundary_check['evidence_locations']

bibs = [raw(r, SURVEY + 'references.bib').decode('utf-8') for r in (OLD, NEW)]
dates = [re.findall(r'urldate = \{([^}]+)\}', t) for t in bibs]
assert dates[0] == ['2026-08-21'] * 41 and dates[1] == ['2026-09-08'] * 41
assert re.sub(r'urldate = \{[^}]+\}', 'urldate = {DATE}', bibs[0]) == re.sub(r'urldate = \{[^}]+\}', 'urldate = {DATE}', bibs[1])

state = load(NEW, 'sources/2026-W34/production-state.json')
approval_path = 'sources/2026-W34/gates/publication-preview-approval.json'
approval = load(NEW, approval_path)
review3 = load(NEW, 'sources/2026-W34/gates/reviews/publication-r3.json')
candidate_path = PUB + 'publication-candidate-v2.json'
candidate = load(NEW, candidate_path)
assert state['human_gate_provenance']['publication_preview']['sha256'] == sha(raw(NEW, approval_path))
assert state['checkpoint_provenance']['publication_preview']['sha256'] == sha(raw(NEW, approval_path))
assert raw(NEW, approval_path) == raw(NEW, review3['approval']['path'])
assert review3['approval']['sha256'] == sha(raw(NEW, approval_path))
assert review3['reviewed_repository_commit_sha'] == REVIEWED
assert review3['reviewed_state']['sha256'] == sha(raw(REVIEWED, 'sources/2026-W34/production-state.json'))
assert approval['publication_candidate_sha256'] == sha(raw(NEW, candidate_path))
assert candidate['pdf']['sha256'] == approval['pdf_sha256'] == sha(raw(NEW, SURVEY + 'main.pdf'))
for ref in review3['reviewed_artifacts']:
    assert ref['sha256'] == sha(raw(NEW, ref['path']))
assert state['human_gates']['publication_preview'] == 'approved'
assert state['next_action'] == 'stage:freeze'
assert state['machine_checkpoints']['freeze'] == state['machine_checkpoints']['release'] == 'pending'

report = dict(
    checked_at_utc=datetime.now(timezone.utc).isoformat(), passed=True,
    scope='FIXED_CASE_IDENTITY_AND_LOCAL_BINDINGS_NOT_FULL_STATE_QUALITY_OR_COST_VALIDATION',
    input_files_sha256_and_git_blob_checked=len(inputs),
    old_review_bound_manuscript_and_two_affected_files_match=True,
    old_review_pdf_sha256=semantic['pdf']['sha256'],
    old_pdf_fetched_or_visually_reviewed=False,
    manuscript_author=manifest['authored_by'], semantic_reviewer=semantic['reviewed_by'],
    visual_reviewer=visual['reviewed_by'],
    old_boundary_pass=boundary_check,
    boundary_text_in_draft_and_bound_tex=True,
    single_boundary_replacement_explains_tex_diff=True,
    bibliography_entries_changed_only_in_access_date=41,
    new_approval_local_bindings_match=True,
    current_candidate_raw_sha256=sha(raw(NEW, candidate_path)),
    current_candidate_payload_sha256=candidate['candidate_sha256'],
    current_pdf_sha256=candidate['pdf']['sha256'],
    state_next_action=state['next_action'],
    limits=[
        'This verifies recorded assertions and identity, not what an agent actually read or its independence.',
        'The two old reviews name the same PDF. Its actual historical PDF bytes were not downloaded here.',
        'Current PDF bytes were hashed only; no render, page review or full Candidate dependency closure.',
        'No Core tests, production execution, gate/freeze/release, semantic-quality PASS or savings measurement.',
        'The 41 canonical access resolutions are reported in upstream maintenance evidence; this script checks the bibliography delta, not all accepted source cards.'
    ])
(BASE / 'check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'passed': True, 'input_files': len(inputs), 'approval_bindings': True, 'old_bound_content_witness': True}))
