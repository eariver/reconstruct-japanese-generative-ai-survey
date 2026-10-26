#!/usr/bin/env python3
"""LF-ED-4 finalize: fresh QA + synthetic postrender reviews + finalize + activate + history.
Uses real TL2026 build outputs from prepare (manuscript + PDF). 1200s per phase.
"""
import subprocess, sys, pathlib, os, json
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-ed-lf4-finalize-20261025T100000Z"
EVID.mkdir(parents=True, exist_ok=True)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/tmp"
os.environ["TMPDIR"]=str(TMP)
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        print(f"{tag}: TIMEOUT", flush=True)
        return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ ... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def py_inline(code, argv, tag, timeout=TIMEOUT):
    return run_tag(tag, [sys.executable,"-c",code]+argv, timeout=timeout)
def main():
    (EVID/"commands.log").write_text(f"LF-ED-4 FINALIZE start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    prop_new="lf-ed-4"; issue="SP001"
    # 1. fresh QA + reviews (synthetic, no genuine approval) + finalize
    qa_code = r"""
import sys, json, pathlib, datetime
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]; now_iso=sys.argv[3]
from pathlib import Path
root_p=Path(root_arg)
import importlib
for m in ["scripts.render_article_draft_tex","scripts.survey_agent_control_v2","scripts.survey_agent_tool_v2","scripts.survey_architecture_v2","scripts.survey_architecture_v2_base","scripts.survey_bibliography_access_provenance_v2","scripts.survey_completeness_v2","scripts.survey_discovery_v2","scripts.survey_drafting_citation_refs_v2","scripts.survey_drafting_v2","scripts.survey_drafting_v2_base","scripts.survey_x_intake_v2","scripts.survey_editorial_correction_proposal_v2","scripts.survey_editorial_current_authority_v2","scripts.survey_editorial_publication_v2","scripts.survey_editorial_retention_v2","scripts.survey_evidence_v2","scripts.survey_longform_derivation_v2","scripts.survey_longform_generated_v2","scripts.survey_production_v2","scripts.survey_publication_set_v2","scripts.survey_publication_v2","scripts.survey_quality_v2","scripts.survey_reader_fidelity_v2","scripts.survey_reader_publication_v2","scripts.survey_reader_surface_gate_v2","scripts.survey_review_attention_v2","scripts.survey_schema_v2","scripts.survey_screening_v2","scripts.survey_versioned_renewal_history_v2","scripts.survey_versioned_renewal_source_v2","scripts.survey_versioned_renewal_v2","scripts.survey_weekly_derivation_v2","scripts.validate_article_draft","scripts.weekly_pipeline"]:
    importlib.import_module(m)
from scripts import survey_production_v2 as core
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_quality_v2 as quality
import os
print(f"QA child PID={os.getpid()}", flush=True)
issue="SP001"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
# staged + pdf from prepare
staged_manifest=json.loads((root_p/pdir_new/"staged-source/staged-source-manifest.json").read_bytes())
staged_main_rel=staged_manifest["outputs"]["main"]["path"]
pdf_rel=f"{pdir_new}/publication/build/main.pdf"
manuscript_rel=f"{pdir_new}/publication/reader-manifest.json" if False else f"{pdir_new}/publication/reader-manuscript-v2.json"
# actual bytes
staged_main_bytes=(root_p/staged_main_rel).read_bytes()
pdf_bytes=(root_p/pdf_rel).read_bytes()
from pypdf import PdfReader
import io as _io
pages=len(PdfReader(_io.BytesIO(pdf_bytes)).pages)
print(f"staged {staged_main_rel} {len(staged_main_bytes)} pdf {pdf_rel} {len(pdf_bytes)} pages {pages}", flush=True)
# quality result dir
qdir=root_p/pdir_new/"publication/quality"
qdir.mkdir(parents=True, exist_ok=True)
# subject (same as lf-boot-1, generic)
subject={"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","issue_id":issue,"cited_discovery_count":1,"bindings":[{"discovery_id":"d01","canonical_name":"Target Model","canonical_url":"https://example.invalid/target","materiality":"MATERIAL","status":"VERIFIED","source_accessed_at":"2026-08-22T02:10:00+09:00"}]}
# identifier with NEW staged main sha
identifier={"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(staged_main_bytes),"inspected_identifiers":[issue,"Target Model"],"scope":f"G7 lf-ed-4 fresh U5 editorial (exact current bytes)"}
# pdf preflight with NEW pdf
preflight={"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":f"G7 lf-ed-4 real TL2026 PDF"}
# empty wrapper with NEW staged path
empty={"check_id":"EMPTY_WRAPPER_SUPPRESSION","status":"PASS","scope":f"G7 lf-ed-4 carries no empty wrapper","inspected_paths":[staged_main_rel]}
for name, payload in [("subject_entity_property_binding.json",subject),("identifier_preservation.json",identifier),("pdf_preflight.json",preflight),("empty_wrapper_suppression.json",empty)]:
    (qdir/name).write_bytes(core.json_bytes(payload))
    print(f"wrote quality {name}", flush=True)
# deterministic-checks.json under proposal dir (like lf-boot-1)
checks=[]
for cid, fname in [("SUBJECT_ENTITY_PROPERTY_BINDING","subject_entity_property_binding.json"),("IDENTIFIER_PRESERVATION","identifier_preservation.json"),("PDF_PREFLIGHT","pdf_preflight.json"),("EMPTY_WRAPPER_SUPPRESSION","empty_wrapper_suppression.json")]:
    p=qdir/fname
    checks.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"G7 lf-ed-4 fresh QA (exact current bytes, synthetic fixture, no genuine approval)","evidence":"Exact fixture bytes and result file inspected.","recorded_at":now_iso,"result":{"path":str(p.relative_to(root_p)),"sha256":core.sha256_file(p)}})
det_path=root_p/pdir_new/"deterministic-checks.json"
det_path.write_bytes(core.json_bytes({"checks":checks}))
print(f"wrote {det_path.relative_to(root_p)}", flush=True)
# validate checks now (fail fast)
cfg=json.loads((root_p/"config/survey-production-v2.json").read_bytes())
quality.validate_checks(root_p, cfg, "THEMATIC", "LONGFORM_SPECIAL", checks, required_kinds={"DETERMINISTIC"})
print("DETERMINISTIC validate OK", flush=True)
# semantic/visual reviews via build_review_record (synthetic, no genuine approval)
# reuse lf-boot-1 checks (known PASS families)
old_sem=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/lf-boot-1/publication/semantic-review-v2.json").read_bytes())
old_vis=json.loads((root_p/f"sources/{issue}/publication/v2/editorial-corrections/lf-boot-1/publication/visual-review-v2.json").read_bytes())
# build new reviews binding NEW manuscript/PDF
manuscript_file=root_p/manuscript_rel
pdf_file=root_p/pdf_rel
# page_count from actual PDF
from scripts import survey_reader_publication_v2 as _r
actual_pages=_r._exact_pdf_page_count(pdf_file)
print(f"actual pages {actual_pages}", flush=True)
# semantic
sem_out=root_p/pdir_new/"publication/semantic-review-v2.json"
if not sem_out.exists():
    _r.build_review_record(root_p, manuscript_file, pdf_file, actual_pages, "SEMANTIC_EDITORIAL", old_sem["checks"], "synthetic LONGFORM semantic reviewer G7 (no genuine approval)", datetime.datetime.fromisoformat(now_iso), sem_out)
    print(f"built semantic {sem_out.relative_to(root_p)}", flush=True)
else:
    print(f"semantic exists", flush=True)
vis_out=root_p/pdir_new/"publication/visual-review-v2.json"
if not vis_out.exists():
    _r.build_review_record(root_p, manuscript_file, pdf_file, actual_pages, "VISUAL", old_vis["checks"], "synthetic LONGFORM visual reviewer G7 (no genuine approval)", datetime.datetime.fromisoformat(now_iso), vis_out)
    print(f"built visual {vis_out.relative_to(root_p)}", flush=True)
else:
    print(f"visual exists", flush=True)
print("QA+REVIEWS DONE", flush=True)
"""
    import time as _t; _t.sleep(1)
    now_iso=datetime.now(timezone.utc).isoformat()
    open(EVID/"now-iso-finalize.txt","w").write(now_iso+"\n")
    q=py_inline(qa_code, [str(FIX), prop_new, now_iso], "ed-qa-reviews", timeout=1200)
    assert q is not None and q.returncode==0, open(EVID/"ed-qa-reviews-stderr.txt").read()[:15000]
    print("QA+REVIEWS OK", flush=True)
    # 2. finalize
    fin_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]; now_iso=sys.argv[3]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_publication_v2 as edpub
import os
from datetime import datetime
print(f"finalize child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
staged=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/staged-source/staged-source-manifest.json"
det=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/deterministic-checks.json"
sem=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/semantic-review-v2.json"
vis=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/visual-review-v2.json"
res=edpub.finalize_publication(str(root_p), f"sources/{issue}/production-state.json", proposal, staged, det, sem, vis, recorded_at=datetime.fromisoformat(now_iso))
print(f"finalize OK set={res.get('set_ref')} sha={res.get('set_sha256')}", flush=True)
import json as _j
print(_j.dumps(res, indent=1))
"""
    f=py_inline(fin_code, [str(FIX), prop_new, now_iso], "ed-finalize", timeout=1200)
    assert f is not None and f.returncode==0, open(EVID/"ed-finalize-stderr.txt").read()[:15000]
    print("FINALIZE OK", flush=True)
    # 3. activate
    act_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]; now_iso=sys.argv[3]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_publication_v2 as edpub
import os, json
from datetime import datetime
print(f"activate child PID={os.getpid()}", flush=True)
issue="SP001"
# find seal
import glob as _g
seals=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication").glob("publication-set.json"))
assert len(seals)==1, f"seal count {seals}"
seal_rel=str(seals[0].relative_to(root_p))
print(f"seal {seal_rel}", flush=True)
res=edpub.activate_publication(str(root_p), f"sources/{issue}/production-state.json", seal_rel, "G7 archive-correction LONGFORM editorial lf-ed-4 on U5-active prior (changed reader, synthetic, no genuine approval)", "longform-g7-lf-ed-4", recorded_at=datetime.fromisoformat(now_iso))
print(f"activate OK {res}", flush=True)
import json as _j
print(_j.dumps(res, indent=1))
"""
    a=py_inline(act_code, [str(FIX), prop_new, now_iso], "ed-activate", timeout=1200)
    assert a is not None and a.returncode==0, open(EVID/"ed-activate-stderr.txt").read()[:15000]
    print("ACTIVATE OK", flush=True)
    # 4. history + current
    hist_code = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_publication_v2 as edpub
import os
print(f"history child PID={os.getpid()}", flush=True)
issue="SP001"
# find record: latest activation record for lf-ed-4? Activation creates record under sources/SP001/publication/v2/publication-surface-revalidation-*.json
# Find latest by mtime? Or read State pointer
st=json.loads((root_p/f"sources/{issue}/production-state.json").read_bytes())
rec_path=st["publication_revalidation_provenance"]["path"]
print(f"active record {rec_path}", flush=True)
res=edpub.verify_activation_history(str(root_p), rec_path)
print(f"history {res.get('HISTORICAL_IDENTITY_VERIFIED') if isinstance(res,dict) else res}", flush=True)
import json as _j
print(_j.dumps({k:v for k,v in res.items() if k in ['HISTORICAL_IDENTITY_VERIFIED','chain_length','observed_refs']}, indent=1)[:4000] if isinstance(res,dict) else str(res)[:2000])
# current
from scripts import survey_agent_control_v2 as agent
cfg=json.loads((root_p/"config/survey-production-v2.json").read_bytes())
st2=json.loads((root_p/f"sources/{issue}/production-state.json").read_bytes())
errs=agent.validate_agent_state(root_p, cfg, st2)
print(f"CURRENT errs={errs}", flush=True)
assert errs==[], f"CURRENT not healthy {errs}"
print("CURRENT OK", flush=True)
# receipt readback
rec=json.loads((root_p/rec_path).read_bytes())
# find set? Use resolve?
from scripts import survey_publication_set_v2 as low
# validate receipt via edpub
import pathlib as _pl
# receipt path from seal? Find editorial receipt for lf-ed-4
receipt_rel=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/publication/validated-source-manifest.json"
rr=edpub.validate_editorial_receipt(str(root_p), receipt_rel, f"sources/{issue}/production-state.json")
print(f"RECEIPT readback OK kind={rr.get('kind')} route={rr.get('generator_route')}", flush=True)
"""
    h=py_inline(hist_code, [str(FIX), prop_new], "ed-history-current", timeout=1200)
    assert h is not None and h.returncode==0, open(EVID/"ed-history-current-stderr.txt").read()[:15000]
    print("HISTORY+CURRENT OK", flush=True)
    print("LF-ED-4 FULL DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
