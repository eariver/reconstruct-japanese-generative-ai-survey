"""Read-only fixed-byte/local-binding checks; not Core or public-asset replay."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
CACHE = ROOT / '.phase-5-inputs'
MAIN = '3e3eebe0cda3a32ac88ae764d279b37768f6bfca'
BRANCH = '3bad8a57cf2b246c7f71cb749ba3105fa318b073'
PUB = 'sources/2026-W34/publication/v2/'
STATE = 'sources/2026-W34/production-state.json'


def raw(ref, path):
    return (CACHE/ref/path).read_bytes()


def load(ref, path):
    return json.loads(raw(ref,path))


def sha(data):
    return hashlib.sha256(data).hexdigest()


inputs = json.loads((BASE/'inputs.json').read_bytes())
for row in inputs:
    data = raw(row['ref'],row['path'])
    assert len(data)==row['bytes'] and sha(data)==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
main_state, branch_state = load(MAIN,STATE), load(BRANCH,STATE)
assert main_state['lifecycle_state']=='RELEASED' and main_state['next_action'] is None and main_state['terminal_reason']=='COMPLETE'
assert branch_state['lifecycle_state']=='FROZEN' and branch_state['next_action']=='stage:release'
candidate=load(MAIN,PUB+'publication-candidate-v2.json')
approval_path='sources/2026-W34/gates/publication-preview-approval.json'
approval=load(MAIN,approval_path)
freeze=load(BRANCH,PUB+'freeze-record-v2.json')
manifest=load(BRANCH,PUB+'release-manifest-v2.json')
release=load(MAIN,PUB+'release-record-v2.json')
freeze_checkpoint=load(BRANCH,'sources/2026-W34/orchestration/v2/checkpoints/RELEASE_CANDIDATE.json')
release_checkpoint=load(MAIN,'sources/2026-W34/orchestration/v2/checkpoints/FROZEN.json')
assert freeze['publication_candidate_sha256']==approval['publication_candidate_sha256']==sha(raw(MAIN,PUB+'publication-candidate-v2.json'))
assert freeze['publication_preview_approval_sha256']==sha(raw(MAIN,approval_path))
assert main_state['human_gate_provenance']['publication_preview']['sha256']==sha(raw(MAIN,approval_path))
assert freeze['visual_review_sha256']==candidate['visual_review']['sha256']
pdf_sha=sha(raw(MAIN,'surveys/weekly/2026-W34/main.pdf'))
assert all(x==pdf_sha for x in [candidate['pdf']['sha256'],approval['pdf_sha256'],freeze['pdf_sha256'],manifest['pdf_sha256'],release['pdf_sha256']])
assert manifest['freeze_record_sha256']==sha(raw(BRANCH,PUB+'freeze-record-v2.json'))
assert release['release_manifest_sha256']==sha(raw(BRANCH,PUB+'release-manifest-v2.json'))
assert release['merge_verification_sha256']==sha(raw(MAIN,PUB+'merge-verification-v2.json'))
for name,ref in [('freeze',BRANCH),('release',MAIN)]:
    ptr=main_state['checkpoint_provenance'][name]
    assert ptr['sha256']==sha(raw(ref,ptr['path']))
for row in freeze_checkpoint['artifacts']:
    if row['name'] in ('freeze-record','release-manifest'):
        assert row['sha256']==sha(raw(BRANCH,row['path']))
for row in release_checkpoint['artifacts']:
    assert row['sha256']==sha(raw(MAIN,row['path']))
recovery=load(MAIN,PUB+'release-recovery-audit-r1.json')
assert recovery['final_state_sha256']==sha(raw(MAIN,STATE))
assert recovery['release_record']['sha256']==sha(raw(MAIN,PUB+'release-record-v2.json'))
public=json.loads((BASE/'public-release.json').read_bytes())
assert not public['draft'] and public['tag_name']=='weekly/2026-W34'
asset=next(a for a in public['assets'] if a['name']=='Japanese_Generative_AI_Technical_Survey_2026-W34.pdf')
assert asset['digest']=='sha256:'+pdf_sha and asset['size']==len(raw(MAIN,'surveys/weekly/2026-W34/main.pdf'))
code_paths=['scripts/survey_reader_publication_v2.py','docs/survey-production-core-v2-sol-luna-review-governance.md','config/publication-review-v2.json','scripts/survey_weekly_semantic_publication_v2.py']
for path in code_paths:
    assert raw(MAIN,path)==raw('74708eb26a357ec11a839a59de62ab62cd246eef',path)
witness=json.loads((BASE/'runtime-witness.json').read_bytes())
for path,digest in witness['captured_input_sha256'].items():
    assert sha(raw(MAIN,path))==digest
report=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),passed=True,scope='CAPTURE_HASHES_AND_SELECTED_AUTHORITY_BINDINGS_NOT_FULL_CORE_OR_QUALITY_VALIDATION',input_files=len(inputs),main=MAIN,weekly_branch=BRANCH,main_lifecycle='RELEASED',weekly_lifecycle='FROZEN',candidate_raw_sha256=sha(raw(MAIN,PUB+'publication-candidate-v2.json')),candidate_payload_sha256=candidate['candidate_sha256'],pdf_sha256=pdf_sha,freeze_release_local_bindings_match=True,public_asset_server_digest_matches=True,public_asset_downloaded=False,selected_code_unchanged_from_prior_main=code_paths,runtime_witness_inputs_match=True,limits=['Source TeX and visual review actual bytes/dependency closure not rechecked here; visual reference digest agrees with approved Candidate.', 'No full State/schema/CI/quality/PDF visual or external release execution.', 'Public Release verification here is metadata and server digest, not independent asset download.', 'Prior W33/SP001 recurrence remains a production audit report, not an independently replayed result.'])
with (BASE/'check.json').open('w',encoding='utf-8',newline='\n') as f:
    f.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'input_files':len(inputs),'main':'RELEASED','branch':'FROZEN','asset_digest_matches':True}))
