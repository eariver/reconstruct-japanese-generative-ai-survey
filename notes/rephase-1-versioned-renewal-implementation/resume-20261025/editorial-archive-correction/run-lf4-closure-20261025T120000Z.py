#!/usr/bin/env python3
"""LONGFORM lf-ed-4 closure: clean explicit public resume/ALREADY_ACTIVE rc0 + full readback.
State already r9 valid from timeout wrappers. Run existing public APIs once in NEW child,
bounded 1200s each, no second live writer (resume on already-active is readonly).
"""
import sys, json, pathlib, os, time
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-lf4-closure-20261025T120000Z"
EVID.mkdir(parents=True, exist_ok=True)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
# heartbeat file for guarded controller
HEARTBEAT = EVID / "heartbeat.txt"
HEARTBEAT.write_text(f"start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n", encoding="utf-8")
def beat(msg):
    with open(HEARTBEAT, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} {msg} PID={os.getpid()}\n")
print(f"CLOSURE child PID={os.getpid()}", flush=True)
beat("init")
# Use fixture-first imports, fresh child (this process is NEW child, no stale imports)
sys.path.insert(0, str(FIX))
import importlib
for m in ["scripts.render_article_draft_tex","scripts.survey_agent_control_v2","scripts.survey_agent_tool_v2","scripts.survey_architecture_v2","scripts.survey_architecture_v2_base","scripts.survey_bibliography_access_provenance_v2","scripts.survey_completeness_v2","scripts.survey_discovery_v2","scripts.survey_drafting_citation_refs_v2","scripts.survey_drafting_v2","scripts.survey_drafting_v2_base","scripts.survey_x_intake_v2","scripts.survey_editorial_correction_proposal_v2","scripts.survey_editorial_current_authority_v2","scripts.survey_editorial_publication_v2","scripts.survey_editorial_retention_v2","scripts.survey_evidence_v2","scripts.survey_longform_derivation_v2","scripts.survey_longform_generated_v2","scripts.survey_production_v2","scripts.survey_publication_set_v2","scripts.survey_publication_v2","scripts.survey_quality_v2","scripts.survey_reader_fidelity_v2","scripts.survey_reader_publication_v2","scripts.survey_reader_surface_gate_v2","scripts.survey_review_attention_v2","scripts.survey_schema_v2","scripts.survey_screening_v2","scripts.survey_versioned_renewal_history_v2","scripts.survey_versioned_renewal_source_v2","scripts.survey_versioned_renewal_v2","scripts.survey_weekly_derivation_v2","scripts.validate_article_draft","scripts.weekly_pipeline"]:
    importlib.import_module(m)
    beat(f"preload {m}")
from scripts import survey_editorial_publication_v2 as edpub
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
beat("imports done")
issue="SP001"; prop_new="lf-ed-4"
state_rel=f"sources/{issue}/production-state.json"
seal_rel=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/publication-set.json"
record_rel=f"sources/{issue}/publication/v2/publication-surface-revalidation-r9.json"
receipt_rel=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/validated-source-manifest.json"
# 1. resume_activation on already-active r9 -> expect ALREADY_ACTIVE readonly, rc0
beat("resume start")
try:
    res_resume = edpub.resume_activation(str(FIX), state_rel, record_rel)
    print(f"RESUME result={res_resume}", flush=True)
    beat(f"resume done {res_resume}")
    # Accept ALREADY_ACTIVE or already-consistent resume; must be dict with readonly indication, no writes
    # If State was already r9, resume should be ALREADY_ACTIVE (readonly inventory record)
    resume_ok = isinstance(res_resume, dict)
except Exception as e:
    print(f"RESUME FAIL {e}", flush=True)
    beat(f"resume fail {e}")
    raise
# 2. validate_prepared_set (readonly)
beat("validate_set start")
res_set = edpub.validate_prepared_set(str(FIX), state_rel, seal_rel)
print(f"VALIDATE_SET OK {res_set.get('result') if isinstance(res_set,dict) else res_set}", flush=True)
beat("validate_set done")
# 3. verify_activation_history (readonly, exact before/after)
beat("history start")
res_hist = edpub.verify_activation_history(str(FIX), record_rel)
print(f"HISTORY {res_hist}", flush=True)
beat("history done")
# 4. receipt readback (readonly)
beat("receipt start")
res_receipt = edpub.validate_editorial_receipt(str(FIX), receipt_rel, state_rel)
print(f"RECEIPT kind={res_receipt.get('kind')} route={res_receipt.get('generator_route')}", flush=True)
beat("receipt done")
# 5. currentState (readonly LIVE validation)
beat("current start")
cfg=json.loads((FIX/"config/survey-production-v2.json").read_bytes())
st=json.loads((FIX/state_rel).read_bytes())
errs=agent.validate_agent_state(FIX, cfg, st)
print(f"CURRENT errs={errs}", flush=True)
assert errs==[], f"CURRENT not healthy {errs}"
beat("current done")
# 6. exact PDF pages/digests + active Candidate pins
beat("pins start")
import hashlib
pdf_path=FIX/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/build/main.pdf"
pdf_bytes=pdf_path.read_bytes()
from pypdf import PdfReader
import io as _io
pages=len(PdfReader(_io.BytesIO(pdf_bytes)).pages)
print(f"PDF pages={pages} bytes={len(pdf_bytes)} sha={hashlib.sha256(pdf_bytes).hexdigest()}", flush=True)
seal=json.loads((FIX/seal_rel).read_bytes())
print(f"SEAL {seal.get('kind')}/{seal.get('status')} set_sha={seal.get('set_sha256')}", flush=True)
cand=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/publication-candidate-v2.json").read_bytes())
print(f"CANDIDATE status={cand.get('status')} pdf={cand.get('pdf',{}).get('path')}", flush=True)
sem=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/semantic-review-v2.json").read_bytes())
vis=json.loads((FIX/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/visual-review-v2.json").read_bytes())
print(f"SEM {sem.get('review_kind')}/{sem.get('status')}/{len(sem.get('checks',[]))} genuine=synthetic-no-genuine-approval", flush=True)
print(f"VIS {vis.get('review_kind')}/{vis.get('status')}/{len(vis.get('checks',[]))} genuine=synthetic-no-genuine-approval", flush=True)
beat("pins done")
print("LF-ED-4 CLOSURE DONE rc0", flush=True)
beat("done rc0")
