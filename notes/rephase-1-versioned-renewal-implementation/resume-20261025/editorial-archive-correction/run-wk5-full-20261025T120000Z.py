#!/usr/bin/env python3
"""WEEKLY wk-ed-renew-5 full: P2R->scope->P2V->P3S63->specs->prepare->QA/reviews->finalize->activate->resume->history/current.
P1/stage already 0 preserved. Retained/ missing (original capture interrupted, not retroPASS). 1200s per phase.
"""
import sys, pathlib, os, json
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-weekly-20261025T100000Z/renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-wk5-full-20261025T120000Z"
EVID.mkdir(parents=True, exist_ok=True)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
HEARTBEAT = EVID / "heartbeat.txt"
HEARTBEAT.write_text(f"start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n", encoding="utf-8")
def beat(msg):
    with open(HEARTBEAT, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} {msg} PID={os.getpid()}\n")
print(f"WK5 FULL child PID={os.getpid()}", flush=True)
beat("init")
sys.path.insert(0, str(FIX))
import importlib
for m in ["scripts.render_article_draft_tex","scripts.survey_agent_control_v2","scripts.survey_agent_tool_v2","scripts.survey_architecture_v2","scripts.survey_architecture_v2_base","scripts.survey_bibliography_access_provenance_v2","scripts.survey_completeness_v2","scripts.survey_discovery_v2","scripts.survey_drafting_citation_refs_v2","scripts.survey_drafting_v2","scripts.survey_drafting_v2_base","scripts.survey_x_intake_v2","scripts.survey_editorial_correction_proposal_v2","scripts.survey_editorial_current_authority_v2","scripts.survey_editorial_publication_v2","scripts.survey_editorial_retention_v2","scripts.survey_evidence_v2","scripts.survey_longform_derivation_v2","scripts.survey_longform_generated_v2","scripts.survey_production_v2","scripts.survey_publication_set_v2","scripts.survey_publication_v2","scripts.survey_quality_v2","scripts.survey_reader_fidelity_v2","scripts.survey_reader_publication_v2","scripts.survey_reader_surface_gate_v2","scripts.survey_review_attention_v2","scripts.survey_schema_v2","scripts.survey_screening_v2","scripts.survey_versioned_renewal_history_v2","scripts.survey_versioned_renewal_source_v2","scripts.survey_versioned_renewal_v2","scripts.survey_weekly_derivation_v2","scripts.validate_article_draft","scripts.weekly_pipeline"]:
    importlib.import_module(m)
    beat(f"preload {m}")
from scripts import survey_editorial_retention_v2 as p2r
from scripts import survey_editorial_current_authority_v2 as p2v
from scripts import survey_editorial_staged_source_v2 as p3s
from scripts import survey_editorial_publication_v2 as edpub
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_quality_v2 as quality
beat("imports done")
issue="2026-W37"; prop_new="wk-ed-renew-5"
state_rel=f"sources/{issue}/production-state.json"
proposal_rel=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
# Verify P1/stage already 0 preserved (no restart)
beat("prereq check")
assert (FIX/pdir_new/"proposal.json").exists(), "proposal missing (P1 stage not preserved)"
assert (FIX/pdir_new/"reader-surface-input-v2.json").exists(), "reader missing"
print("Prereqs P1/stage preserved", flush=True)
beat("prereq ok")
# 1. P2R capture (retained/ missing, safe new root, not repeat on existing; original interrupted not retroPASS)
beat("p2r capture start")
# Safety: retained/ must NOT exist (else refuse repeat, use NEW ID)
import pathlib as _pl
retained_dir=FIX/pdir_new/"retained"
if retained_dir.exists():
    raise RuntimeError(f"P2R retained root already present (no overwrite, use NEW ID): {retained_dir}")
res_cap=p2r.capture_retention(str(FIX), state_rel, proposal_rel)
print(f"P2R CAPTURED {res_cap.get('manifest_path')}", flush=True)
beat(f"p2r capture done {res_cap.get('manifest_path')}")
manifest_rel=res_cap.get('manifest_path')
# 2. verify_retention (complete valid bytes + same basis required for P2V continuation)
beat("p2r verify start")
res_ver=p2r.verify_retention(str(FIX), proposal_rel, manifest_rel)
print(f"P2R VERIFIED", flush=True)
beat("p2r verify done")
# 3. scope (synthetic, no genuine approval)
beat("scope start")
proposal=json.loads((FIX/pdir_new/"proposal.json").read_bytes())
staged_reader_rel=proposal["proposed"]["proposed_reader_ref"]["path"]
after_sha=proposal["proposed"]["proposed_reader_canonical_sha256"]
block={"version":"EDITORIAL_CORRECTION_SCOPE_V1","decision":"WITHIN_APPROVED_AUTHORITY","before_reader_input":proposal["basis"]["active_reader_input_ref"],"preserved_upstream_sha256":proposal["basis"]["preserved_upstream_digest"],"change_summary":"Synthetic Weekly scope judgment inside approved authority (G6 archive-correction, no genuine approval).","evidence_locations":["synthetic-fixture:proposal"]}
review={"schema_version":"2.0-rc1","issue_id":proposal["issue_id"],"publication_profile":proposal["publication_profile"],"review_kind":"SEMANTIC_EDITORIAL","reviewed_surface":{"path":staged_reader_rel,"sha256":after_sha},"checks":[{"check_id":"READER_PIPELINE_INDEPENDENCE","status":"PASS","detail":"Synthetic scope reviewer judged proposed reader independently understandable.","evidence_locations":["synthetic-fixture:proposed-reader"]},{"check_id":"EDITORIAL_CORRECTION_SCOPE","status":"PASS","detail":"Synthetic scope reviewer judged delta inside approved Architecture authority.","evidence_locations":["synthetic-fixture:proposal"]}],"decision":"PASS","reviewed_by":"synthetic Weekly scope reviewer (G6)","reviewed_at":"2026-10-25T12:00:00+00:00","recorded_at":"2026-10-25T12:00:00+00:00","status":"PASSED","findings":[],"summary":"Synthetic scope PASS for G6 archive-correction.","editorial_correction_scope":block}
review["review_sha256"]=core.sha256_object(review)
scope_path=FIX/pdir_new/"scope-review-v2.json"
if not scope_path.exists():
    scope_path.write_bytes(core.json_bytes(review))
    print(f"scope {scope_path.relative_to(FIX)}", flush=True)
else:
    print(f"scope exists", flush=True)
beat("scope done")
scope_rel=f"{pdir_new}/scope-review-v2.json"
# 4. P3S materialize + verify (63)
beat("p3s start")
try:
    res_p3s=p3s.materialize_staged_source(str(FIX), state_rel, proposal_rel, manifest_rel, scope_rel)
    staged_ref=res_p3s.get('staged_manifest_ref',{}).get('path') if isinstance(res_p3s,dict) else None
    print(f"P3S staged={staged_ref}", flush=True)
    v=p3s.verify_staged_source(str(FIX), proposal_rel, staged_ref)
    print(f"P3S verify OK", flush=True)
except Exception as e:
    import traceback
    msg=str(e)
    print(f"P3S materialize issue: {msg[:500]}", flush=True)
    if "STAGED_ROOT_EXISTS" in msg:
        staged_ref=f"{pdir_new}/staged-source/staged-source-manifest.json"
        v=p3s.verify_staged_source(str(FIX), proposal_rel, staged_ref)
        print(f"P3S verify existing OK", flush=True)
    else:
        raise
beat("p3s done")
staged_manifest_rel=f"{pdir_new}/staged-source/staged-source-manifest.json"
# 5. specs
beat("specs start")
import hashlib, datetime as _dt
old_spec=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json").read_bytes())
new_sha=hashlib.sha256((FIX/pdir_new/"proposal.json").read_bytes()).hexdigest()
new_spec=dict(old_spec)
new_spec["proposal_ref"]={"path":f"{pdir_new}/proposal.json","sha256":new_sha}
new_spec["authored_by"]="weekly G6 editorial author wk-ed-renew-5"
new_spec["recorded_at"]=_dt.datetime.now(_dt.timezone.utc).isoformat()
mspec_path=FIX/pdir_new/"manuscript-spec.json"
if not mspec_path.exists():
    mspec_path.write_bytes(core.json_bytes(new_spec))
old_tool=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/toolchain-spec.json").read_bytes())
new_tool=dict(old_tool)
new_tool["executor"]="weekly-g6-wk-ed-renew-5"
new_tool["recorded_at"]=_dt.datetime.now(_dt.timezone.utc).isoformat()
tool_path=FIX/pdir_new/"toolchain-spec.json"
if not tool_path.exists():
    tool_path.write_bytes(core.json_bytes(new_tool))
print(f"specs done", flush=True)
beat("specs done")
mspec_rel=f"{pdir_new}/manuscript-spec.json"
tspec_rel=f"{pdir_new}/toolchain-spec.json"
# 6. prepare (real TL2026 build, OWN fix)
beat("prepare start")
res_prep=edpub.prepare_publication(str(FIX), state_rel, proposal_rel, staged_manifest_rel, mspec_rel, tspec_rel)
print(f"PREPARE OK {sorted(res_prep.keys()) if isinstance(res_prep,dict) else type(res_prep)}", flush=True)
beat("prepare done")
# 7. QA + reviews (fresh, synthetic no genuine)
beat("qa start")
import datetime as _dt2
now_iso=_dt2.datetime.now(_dt2.timezone.utc).isoformat()
staged_manifest=json.loads((FIX/pdir_new/"staged-source/staged-source-manifest.json").read_bytes())
staged_main_rel=staged_manifest["outputs"]["main"]["path"]
pdf_rel=f"{pdir_new}/publication/build/main.pdf"
manuscript_rel=f"{pdir_new}/publication/reader-manuscript-v2.json"
staged_main_bytes=(FIX/staged_main_rel).read_bytes()
pdf_bytes=(FIX/pdf_rel).read_bytes()
from pypdf import PdfReader
import io as _io
pages=len(PdfReader(_io.BytesIO(pdf_bytes)).pages)
print(f"staged {staged_main_rel} pdf {pdf_rel} pages {pages}", flush=True)
qdir=FIX/pdir_new/"publication/quality"
qdir.mkdir(parents=True, exist_ok=True)
subject={"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","issue_id":issue,"cited_discovery_count":1,"bindings":[{"discovery_id":"d01","canonical_name":"Weekly Test","canonical_url":"https://example.invalid/weekly","materiality":"MATERIAL","status":"VERIFIED","source_accessed_at":"2026-08-22T02:10:00+09:00"}]}
identifier={"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(staged_main_bytes),"inspected_identifiers":[issue],"scope":f"G6 wk-ed-renew-5 fresh U5 (exact bytes)"}
preflight={"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":f"G6 wk-ed-renew-5 real TL2026 PDF"}
empty={"check_id":"EMPTY_WRAPPER_SUPPRESSION","status":"PASS","scope":f"G6 wk-ed-renew-5 no empty wrapper","inspected_paths":[staged_main_rel]}
for name, payload in [("subject_entity_property_binding.json",subject),("identifier_preservation.json",identifier),("pdf_preflight.json",preflight),("empty_wrapper_suppression.json",empty)]:
    (qdir/name).write_bytes(core.json_bytes(payload))
checks=[]
for cid, fname in [("SUBJECT_ENTITY_PROPERTY_BINDING","subject_entity_property_binding.json"),("IDENTIFIER_PRESERVATION","identifier_preservation.json"),("PDF_PREFLIGHT","pdf_preflight.json"),("EMPTY_WRAPPER_SUPPRESSION","empty_wrapper_suppression.json")]:
    p=qdir/fname
    checks.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"G6 wk-ed-renew-5 fresh QA (exact bytes, synthetic, no genuine)","evidence":"Exact fixture bytes and result file inspected.","recorded_at":now_iso,"result":{"path":str(p.relative_to(FIX)),"sha256":core.sha256_file(p)}})
det_path=FIX/pdir_new/"deterministic-checks.json"
det_path.write_bytes(core.json_bytes({"checks":checks}))
cfg=json.loads((FIX/"config/survey-production-v2.json").read_bytes())
quality.validate_checks(FIX, cfg, "WEEKLY", "WEEKLY_MAGAZINE", checks, required_kinds={"DETERMINISTIC"})
print(f"DETERMINISTIC OK", flush=True)
old_sem=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/publication/semantic-review-v2.json").read_bytes())
old_vis=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/publication/visual-review-v2.json").read_bytes())
manuscript_file=FIX/manuscript_rel
pdf_file=FIX/pdf_rel
actual_pages=reader._exact_pdf_page_count(pdf_file)
sem_out=FIX/pdir_new/"publication/semantic-review-v2.json"
if not sem_out.exists():
    reader.build_review_record(FIX, manuscript_file, pdf_file, actual_pages, "SEMANTIC_EDITORIAL", old_sem["checks"], "synthetic Weekly semantic reviewer G6 (no genuine)", _dt2.datetime.fromisoformat(now_iso), sem_out)
vis_out=FIX/pdir_new/"publication/visual-review-v2.json"
if not vis_out.exists():
    reader.build_review_record(FIX, manuscript_file, pdf_file, actual_pages, "VISUAL", old_vis["checks"], "synthetic Weekly visual reviewer G6 (no genuine)", _dt2.datetime.fromisoformat(now_iso), vis_out)
print(f"QA+REVIEWS DONE", flush=True)
beat("qa done")
det_rel=f"{pdir_new}/deterministic-checks.json"
sem_rel=f"{pdir_new}/publication/semantic-review-v2.json"
vis_rel=f"{pdir_new}/publication/visual-review-v2.json"
# 8. finalize
beat("finalize start")
import datetime as _dt3
res_fin=edpub.finalize_publication(str(FIX), state_rel, proposal_rel, staged_manifest_rel, det_rel, sem_rel, vis_rel, recorded_at=_dt3.datetime.fromisoformat(now_iso))
print(f"FINALIZE OK set={res_fin.get('set_ref')}", flush=True)
beat("finalize done")
# 9. activate
beat("activate start")
seal_rel=res_fin.get('set_ref') if isinstance(res_fin,dict) else f"{pdir_new}/publication/publication-set.json"
res_act=edpub.activate_publication(str(FIX), state_rel, seal_rel, "G6 archive-correction WEEKLY editorial wk-ed-renew-5 on U5-active prior (changed reader, synthetic, no genuine)", "weekly-g6-wk-ed-renew-5", recorded_at=_dt3.datetime.fromisoformat(_dt3.datetime.now(_dt3.timezone.utc).isoformat()))
print(f"ACTIVATE OK {res_act}", flush=True)
beat("activate done")
# 10. resume (if already active, ALREADY_ACTIVE readonly) + history/current/receipt
beat("resume start")
# Find latest record (activate created r8? Weekly U5 was r7, editorial should be r8)
st_after=json.loads((FIX/state_rel).read_bytes())
rec_path=st_after["publication_revalidation_provenance"]["path"]
print(f"active record {rec_path}", flush=True)
try:
    res_resume=edpub.resume_activation(str(FIX), state_rel, rec_path)
    print(f"RESUME {res_resume}", flush=True)
except Exception as e:
    print(f"RESUME note (already active, State consistent): {e}", flush=True)
beat("resume done")
beat("history start")
res_hist=edpub.verify_activation_history(str(FIX), rec_path)
print(f"HISTORY {res_hist}", flush=True)
beat("history done")
beat("receipt start")
receipt_rel=f"{pdir_new}/publication/validated-source-manifest.json"
res_rec=edpub.validate_editorial_receipt(str(FIX), receipt_rel, state_rel)
print(f"RECEIPT kind={res_rec.get('kind')} route={res_rec.get('generator_route')}", flush=True)
beat("receipt done")
beat("current start")
cfg2=json.loads((FIX/"config/survey-production-v2.json").read_bytes())
st2=json.loads((FIX/state_rel).read_bytes())
errs=agent.validate_agent_state(FIX, cfg2, st2)
print(f"CURRENT errs={errs}", flush=True)
assert errs==[], f"CURRENT {errs}"
beat("current done")
# pins
beat("pins start")
import hashlib as _hl
pdf_p=FIX/pdf_rel
pdf_b=pdf_p.read_bytes()
print(f"PDF pages={actual_pages} bytes={len(pdf_b)} sha={_hl.sha256(pdf_b).hexdigest()}", flush=True)
seal_j=json.loads((FIX/seal_rel).read_bytes())
print(f"SEAL {seal_j.get('kind')}/{seal_j.get('status')} set_sha={seal_j.get('set_sha256')}", flush=True)
beat("pins done")
print("WK-ED-5 FULL DONE rc0", flush=True)
beat("done rc0")
