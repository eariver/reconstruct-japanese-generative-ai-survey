#!/usr/bin/env python3
"""Weekly-final ED final: specs->prepare(real TL)->Weekly QA (derived, no EMPTY)->finalize seal->activate r3->history/current/receipt/Candidate readback.
SHORT chain, current 741, style 035, NEW63 epoch, nonlegacy anchor, synthetic NO-GO labels.
Fresh subprocess per public call, no preload/caching/overrides/synthetic State, bounded 1200s.
"""
import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z"
FIX = BASE / "renewal-weekly-final"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/ed-final-20261025T235500Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
CTRL_HB = EVID / "controller-heartbeat.txt"
CTRL_RES = EVID / "controller-result.txt"
CTRL_EXIT = EVID / "controller-exit.txt"
import datetime as _dt
import atexit as _atexit
CTRL_HB.write_text(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} final start pid={os.getpid()}\n", encoding="utf-8")
CTRL_RES.write_text("RUNNING\n", encoding="utf-8")
if not CTRL_EXIT.exists():
    CTRL_EXIT.write_text("running\n", encoding="utf-8")
def beat(msg):
    with open(CTRL_HB, "a", encoding="utf-8") as fh:
        fh.write(f"{_dt.datetime.now(_dt.timezone.utc).isoformat()} {msg} pid={os.getpid()}\n")
beat("init")
def _finalize_exit():
    try:
        cur = CTRL_EXIT.read_text(encoding="utf-8").strip() if CTRL_EXIT.exists() else "missing"
    except Exception:
        cur = "unreadable"
    if cur == "running":
        try:
            CTRL_RES.write_text("UNREPORTED_FAIL (atexit)\n", encoding="utf-8")
            CTRL_EXIT.write_text("1\n", encoding="utf-8")
            beat("atexit UNREPORTED_FAIL -> 1")
        except Exception:
            pass
_atexit.register(_finalize_exit)
def log(m):
    print(m, flush=True)
    open(LOG, "a").write(m+"\n")
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env=dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_CONFIG_GLOBAL"]="/dev/null"; env["GIT_OPTIONAL_LOCKS"]="0"
        tmpdir=BASE/"tmp-tex"; tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
        tlbin="/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux"
        env["PATH"]=tlbin+":"+env.get("PATH","")
    log(f"$ {' '.join(cmd[:6])}... # {tag} timeout={timeout}s")
    beat(f"start {tag}")
    try:
        proc=subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"Timeout ({timeout}s) PID-parent={os.getpid()}\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        log(f"DONE {tag} TIMEOUT"); beat(f"TIMEOUT {tag}"); return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}"); beat(f"done {tag} exit={proc.returncode}"); return proc
PY=sys.executable
ISSUE="2026-W37"
STATE=f"sources/{ISSUE}/production-state.json"
PROP_NEW="wk-ed-final-1"
PDIR_NEW=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}"
proposal_rel=f"{PDIR_NEW}/proposal.json"
staged_manifest_rel=f"{PDIR_NEW}/staged-source/staged-source-manifest.json"
log(f"prereq staged {(FIX/staged_manifest_rel).is_file()} proposal {(FIX/proposal_rel).is_file()}")
assert (FIX/staged_manifest_rel).is_file() and (FIX/proposal_rel).is_file(), "P3S must be done before final"
log("owner EDPUB survey_editorial_publication_v2.prepare_publication (fixed858 real TL lualatex/biber)")
log("owner QA survey_quality_v2.expected_checks_by_kind/validate_checks (Weekly families, no EMPTY_WRAPPER_SUPPRESSION)")
log("owner Reader survey_reader_publication_v2.build_review_record/validate_review_record + _exact_pdf_page_count")
log("owner EDPUB finalize_publication/activate_publication/verify_activation_history/validate_editorial_receipt")
log("owner agent survey_agent_control_v2.validate_agent_state (strict LIVE)")
# Specs: manuscript-spec + toolchain-spec from wk-boot-1 (siblings, not children of publication)
SPECS=r"""
import sys, json, hashlib, datetime as _dt
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1]); prop_new=sys.argv[2]
from scripts import survey_production_v2 as core
issue="2026-W37"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
old_spec=json.loads((root/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json").read_bytes())
new_sha=hashlib.sha256((root/pdir_new/"proposal.json").read_bytes()).hexdigest()
new_spec=dict(old_spec)
new_spec["proposal_ref"]={"path":f"{pdir_new}/proposal.json","sha256":new_sha}
new_spec["authored_by"]=f"weekly-final {prop_new} (changed reader, synthetic)"
new_spec["recorded_at"]=_dt.datetime.now(_dt.timezone.utc).isoformat()
mspec_path=root/pdir_new/"manuscript-spec.json"
if not mspec_path.exists():
    mspec_path.write_bytes(core.json_bytes(new_spec))
    print(f"WROTE {mspec_path.relative_to(root)}")
else:
    print(f"EXISTS manuscript-spec")
old_tool=json.loads((root/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/toolchain-spec.json").read_bytes())
new_tool=dict(old_tool)
new_tool["executor"]=f"weekly-final-{prop_new}"
new_tool["recorded_at"]=_dt.datetime.now(_dt.timezone.utc).isoformat()
tool_path=root/pdir_new/"toolchain-spec.json"
if not tool_path.exists():
    tool_path.write_bytes(core.json_bytes(new_tool))
    print(f"WROTE {tool_path.relative_to(root)}")
else:
    print(f"EXISTS toolchain")
"""
pspec=run([PY,"-c",SPECS,str(FIX),PROP_NEW],REPO,"specs-build",timeout=300)
if pspec is None or pspec.returncode!=0:
    log("FATAL specs")
    CTRL_RES.write_text("FAIL specs\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail specs"); sys.exit(1)
mspec_rel=f"{PDIR_NEW}/manuscript-spec.json"
tspec_rel=f"{PDIR_NEW}/toolchain-spec.json"
# Prepare (real TL2026, disposable, TMPDIR workspace-local, no /tmp writes except read-only TL)
PREP=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.prepare_publication(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
print(json.dumps({"keys":sorted(res.keys()) if isinstance(res,dict) else str(type(res)),"res":str(res)[:2000]},indent=1))
"""
pprep=run([PY,"-c",PREP,str(FIX),STATE,proposal_rel,staged_manifest_rel,mspec_rel,tspec_rel],REPO,"ed-prepare",timeout=1200)
if pprep is None:
    log("PREPARE TIMEOUT — record, not retro PASS")
    CTRL_RES.write_text("TIMEOUT prepare\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout prepare"); sys.exit(2)
if pprep.returncode!=0:
    log("FATAL prepare")
    CTRL_RES.write_text("FAIL prepare\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail prepare"); sys.exit(1)
log("PREPARE OK real TL2026")
# QA + reviews: Weekly-applicable ONLY deterministic (derive families, no EMPTY), semantic/visual via builders
# Derive kinds first to prove fix (no EMPTY_WRAPPER_SUPPRESSION for Weekly)
QA_DERIVE=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
root=Path(sys.argv[1])
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
kinds=quality.expected_checks_by_kind(cfg, "WEEKLY", "WEEKLY_MAGAZINE", {"DETERMINISTIC"})
print(json.dumps({"weekly_det":sorted(kinds)},indent=1))
assert "EMPTY_WRAPPER_SUPPRESSION" not in kinds, "EMPTY must not be Weekly-applicable (harness bug)"
assert set(kinds)=={"IDENTIFIER_PRESERVATION","PDF_PREFLIGHT","SUBJECT_ENTITY_PROPERTY_BINDING"}, f"unexpected Weekly det {kinds}"
"""
pqderive=run([PY,"-c",QA_DERIVE,str(FIX)],REPO,"qa-derive-weekly",timeout=300)
if pqderive is None or pqderive.returncode!=0:
    log("FATAL qa derive (Weekly families)")
    CTRL_RES.write_text("FAIL qa-derive\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail qa-derive"); sys.exit(1)
log("QA derive Weekly 3 DET OK (no EMPTY)")
QA_BUILD=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s=sys.argv[1]
from pathlib import Path
root=Path(root_s)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
import datetime as _dt
issue="2026-W37"; prop_new="wk-ed-final-1"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
staged_manifest=json.loads((root/pdir_new/"staged-source/staged-source-manifest.json").read_bytes())
staged_main_rel=staged_manifest["outputs"]["main"]["path"]
pdf_rel=f"{pdir_new}/publication/build/main.pdf"
manuscript_rel=f"{pdir_new}/publication/reader-manuscript-v2.json"
staged_main_bytes=(root/staged_main_rel).read_bytes()
pdf_bytes=(root/pdf_rel).read_bytes()
from pypdf import PdfReader
import io as _io
pages=len(PdfReader(_io.BytesIO(pdf_bytes)).pages)
print(f"staged {staged_main_rel} pdf {pdf_rel} pages {pages}",flush=True)
# Derive Weekly families (no EMPTY)
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
kinds=quality.expected_checks_by_kind(cfg, "WEEKLY", "WEEKLY_MAGAZINE", {"DETERMINISTIC"})
assert set(kinds)=={"IDENTIFIER_PRESERVATION","PDF_PREFLIGHT","SUBJECT_ENTITY_PROPERTY_BINDING"}
now_iso=_dt.datetime.now(_dt.timezone.utc).isoformat()
qdir=root/pdir_new/"publication/quality"
qdir.mkdir(parents=True,exist_ok=True)
scope="weekly-final fresh editorial (exact bytes, synthetic, no genuine approval, Production semantic NO-GO)"
# Payloads for Weekly 3 DET only
subject={"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","issue_id":issue,"cited_discovery_count":1,"bindings":[{"discovery_id":"d01","canonical_name":"Weekly Test","canonical_url":"https://example.invalid/weekly","materiality":"MATERIAL","status":"VERIFIED","source_accessed_at":"2026-08-22T02:10:00+09:00"}]}
identifier={"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(staged_main_bytes),"inspected_identifiers":[issue],"scope":scope}
preflight={"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":scope+" real TL2026 PDF"}
for name, payload in [("subject_entity_property_binding.json",subject),("identifier_preservation.json",identifier),("pdf_preflight.json",preflight)]:
    (qdir/name).write_bytes(core.json_bytes(payload))
checks=[]
for cid, fname in [("SUBJECT_ENTITY_PROPERTY_BINDING","subject_entity_property_binding.json"),("IDENTIFIER_PRESERVATION","identifier_preservation.json"),("PDF_PREFLIGHT","pdf_preflight.json")]:
    p=qdir/fname
    checks.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"weekly-final fresh QA (exact bytes, synthetic, no genuine)","evidence":"Exact fixture bytes and result file inspected.","recorded_at":now_iso,"result":{"path":str(p.relative_to(root)),"sha256":core.sha256_file(p)}})
# Strict: payloads must equal kinds (no skipping, no EMPTY)
assert set([c["check_id"] for c in checks])==set(kinds), f"{sorted([c['check_id'] for c in checks])} != {sorted(kinds)}"
det_path=root/pdir_new/"deterministic-checks.json"
det_path.write_bytes(core.json_bytes({"checks":checks}))
print(f"WROTE det {det_path.relative_to(root)}",flush=True)
quality.validate_checks(root, cfg, "WEEKLY", "WEEKLY_MAGAZINE", checks, required_kinds={"DETERMINISTIC"})
print(f"DETERMINISTIC OK 3",flush=True)
# Semantic/visual via actual builders (synthetic reviewers, no genuine approval)
old_sem=json.loads((root/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/publication/semantic-review-v2.json").read_bytes())
old_vis=json.loads((root/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/publication/visual-review-v2.json").read_bytes())
manuscript_file=root/manuscript_rel
pdf_file=root/pdf_rel
actual_pages=reader._exact_pdf_page_count(pdf_file)
sem_out=root/pdir_new/"publication/semantic-review-v2.json"
if not sem_out.exists():
    reader.build_review_record(root, manuscript_file, pdf_file, actual_pages, "SEMANTIC_EDITORIAL", old_sem["checks"], "synthetic Weekly semantic reviewer weekly-final (no genuine, Production NO-GO)", _dt.datetime.fromisoformat(now_iso), sem_out)
    print(f"BUILT sem",flush=True)
else:
    print(f"EXISTS sem",flush=True)
vis_out=root/pdir_new/"publication/visual-review-v2.json"
if not vis_out.exists():
    reader.build_review_record(root, manuscript_file, pdf_file, actual_pages, "VISUAL", old_vis["checks"], "synthetic Weekly visual reviewer weekly-final (no genuine, Production NO-GO)", _dt.datetime.fromisoformat(now_iso), vis_out)
    print(f"BUILT vis",flush=True)
else:
    print(f"EXISTS vis",flush=True)
print(f"QA+REVIEWS DONE pages={pages}",flush=True)
# Save now_iso for finalize (recorded_at must be >= QA recorded_at? Use same now_iso)
open("/tmp/final_now_iso.txt","w").write(now_iso)
# Also write to EVID via stdout? Return now_iso
print(now_iso)
"""
# Note: /tmp write is not allowed? Use workspace TMPDIR instead. The above writes to /tmp/final_now_iso.txt which violates no /tmp? Actually /tmp/opencode fallback? But task says no cleanup/cache purge, but /tmp writes? Prior run used /tmp? Better to avoid /tmp, use EVID.
# Patch: use EVID file for now_iso
# We'll run QA_BUILD without /tmp write by capturing stdout last line as now_iso
# Redefine without /tmp
QA_BUILD_FIXED=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s=sys.argv[1]
from pathlib import Path
root=Path(root_s)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
import datetime as _dt
issue="2026-W37"; prop_new="wk-ed-final-1"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
staged_manifest=json.loads((root/pdir_new/"staged-source/staged-source-manifest.json").read_bytes())
staged_main_rel=staged_manifest["outputs"]["main"]["path"]
pdf_rel=f"{pdir_new}/publication/build/main.pdf"
manuscript_rel=f"{pdir_new}/publication/reader-manuscript-v2.json"
staged_main_bytes=(root/staged_main_rel).read_bytes()
pdf_bytes=(root/pdf_rel).read_bytes()
from pypdf import PdfReader
import io as _io
pages=len(PdfReader(_io.BytesIO(pdf_bytes)).pages)
print(f"staged {staged_main_rel} pdf {pdf_rel} pages {pages}",flush=True)
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
kinds=quality.expected_checks_by_kind(cfg, "WEEKLY", "WEEKLY_MAGAZINE", {"DETERMINISTIC"})
assert set(kinds)=={"IDENTIFIER_PRESERVATION","PDF_PREFLIGHT","SUBJECT_ENTITY_PROPERTY_BINDING"}
now_iso=_dt.datetime.now(_dt.timezone.utc).isoformat()
qdir=root/pdir_new/"publication/quality"
qdir.mkdir(parents=True,exist_ok=True)
scope="weekly-final fresh editorial (exact bytes, synthetic, no genuine approval, Production semantic NO-GO)"
subject={"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","issue_id":issue,"cited_discovery_count":1,"bindings":[{"discovery_id":"d01","canonical_name":"Weekly Test","canonical_url":"https://example.invalid/weekly","materiality":"MATERIAL","status":"VERIFIED","source_accessed_at":"2026-08-22T02:10:00+09:00"}]}
identifier={"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(staged_main_bytes),"inspected_identifiers":[issue],"scope":scope}
preflight={"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":scope+" real TL2026 PDF"}
for name, payload in [("subject_entity_property_binding.json",subject),("identifier_preservation.json",identifier),("pdf_preflight.json",preflight)]:
    (qdir/name).write_bytes(core.json_bytes(payload))
checks=[]
for cid, fname in [("SUBJECT_ENTITY_PROPERTY_BINDING","subject_entity_property_binding.json"),("IDENTIFIER_PRESERVATION","identifier_preservation.json"),("PDF_PREFLIGHT","pdf_preflight.json")]:
    p=qdir/fname
    checks.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"weekly-final fresh QA (exact bytes, synthetic, no genuine)","evidence":"Exact fixture bytes and result file inspected.","recorded_at":now_iso,"result":{"path":str(p.relative_to(root)),"sha256":core.sha256_file(p)}})
assert set([c["check_id"] for c in checks])==set(kinds)
det_path=root/pdir_new/"deterministic-checks.json"
det_path.write_bytes(core.json_bytes({"checks":checks}))
print(f"WROTE det",flush=True)
quality.validate_checks(root, cfg, "WEEKLY", "WEEKLY_MAGAZINE", checks, required_kinds={"DETERMINISTIC"})
print(f"DETERMINISTIC OK 3",flush=True)
old_sem=json.loads((root/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/publication/semantic-review-v2.json").read_bytes())
old_vis=json.loads((root/f"sources/{issue}/publication/v2/editorial-corrections/wk-boot-1/publication/visual-review-v2.json").read_bytes())
manuscript_file=root/manuscript_rel
pdf_file=root/pdf_rel
actual_pages=reader._exact_pdf_page_count(pdf_file)
sem_out=root/pdir_new/"publication/semantic-review-v2.json"
if not sem_out.exists():
    reader.build_review_record(root, manuscript_file, pdf_file, actual_pages, "SEMANTIC_EDITORIAL", old_sem["checks"], "synthetic Weekly semantic reviewer weekly-final (no genuine, Production NO-GO)", _dt.datetime.fromisoformat(now_iso), sem_out)
    print(f"BUILT sem",flush=True)
else:
    print(f"EXISTS sem",flush=True)
vis_out=root/pdir_new/"publication/visual-review-v2.json"
if not vis_out.exists():
    reader.build_review_record(root, manuscript_file, pdf_file, actual_pages, "VISUAL", old_vis["checks"], "synthetic Weekly visual reviewer weekly-final (no genuine, Production NO-GO)", _dt.datetime.fromisoformat(now_iso), vis_out)
    print(f"BUILT vis",flush=True)
else:
    print(f"EXISTS vis",flush=True)
print(f"QA_DONE pages={pages} now={now_iso}",flush=True)
"""
pqa=run([PY,"-c",QA_BUILD_FIXED,str(FIX)],REPO,"qa-build-weekly",timeout=1200)
if pqa is None:
    log("QA TIMEOUT")
    CTRL_RES.write_text("TIMEOUT qa\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout qa"); sys.exit(2)
if pqa.returncode!=0:
    log("FATAL qa")
    CTRL_RES.write_text("FAIL qa\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail qa"); sys.exit(1)
log("QA Weekly 3 DET + semantic/visual built (synthetic NO-GO)")
det_rel=f"{PDIR_NEW}/deterministic-checks.json"
sem_rel=f"{PDIR_NEW}/publication/semantic-review-v2.json"
vis_rel=f"{PDIR_NEW}/publication/visual-review-v2.json"
# Extract now_iso from qa stdout for finalize recorded_at (use last line now=...)
try:
    txt=(EVID/"qa-build-weekly-stdout.txt").read_text().strip().splitlines()
    last=[l for l in txt if "QA_DONE" in l][-1]
    # format QA_DONE pages=X now=ISO
    now_iso=last.split("now=")[-1].strip()
    log(f"finalize now_iso {now_iso}")
except Exception as e:
    log(f"now parse fail {e}, using wallclock")
    import datetime as _d2
    now_iso=_d2.datetime.now(_d2.timezone.utc).isoformat()
# Finalize seal
FIN=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.finalize_publication(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], recorded_at=__import__("datetime").datetime.fromisoformat(sys.argv[8]))
print(json.dumps({"set_ref":res.get("set_ref") if isinstance(res,dict) else str(res)},indent=1))
"""
pfin=run([PY,"-c",FIN,str(FIX),STATE,proposal_rel,staged_manifest_rel,det_rel,sem_rel,vis_rel,now_iso],REPO,"ed-finalize",timeout=1200)
if pfin is None:
    log("FINALIZE TIMEOUT")
    CTRL_RES.write_text("TIMEOUT finalize\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout finalize"); sys.exit(2)
if pfin.returncode!=0:
    log("FATAL finalize")
    CTRL_RES.write_text("FAIL finalize\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail finalize"); sys.exit(1)
try:
    set_rel=json.loads((EVID/"ed-finalize-stdout.txt").read_text().strip()).get("set_ref")
    log(f"seal {set_rel}")
except Exception as e:
    log(f"seal parse fail {e}")
    set_rel=f"{PDIR_NEW}/publication/publication-set.json"
log(f"seal_rel {set_rel} exists={(FIX/set_rel).is_file() if set_rel else False}")
# Activate EDITORIAL r3 (Source kind EDITORIAL..., NEW63 epoch, nonlegacy anchor)
ACT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.activate_publication(str(root), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], recorded_at=__import__("datetime").datetime.fromisoformat(sys.argv[6]))
print(json.dumps(res,indent=1))
"""
import datetime as _d3
act_iso=_d3.datetime.now(_d3.timezone.utc).isoformat()
(EVID/"recorded-at-activate.json").write_text(json.dumps({"activate":act_iso},indent=1))
pact=run([PY,"-c",ACT,str(FIX),STATE,set_rel,"Weekly-final EDITORIAL wk-ed-final-1 on U1 r2-active (changed reader, synthetic, no genuine, Production NO-GO)","weekly-final-ed",act_iso],REPO,"ed-activate",timeout=1200)
if pact is None:
    log("ACTIVATE TIMEOUT — check explicit resume ALREADY_ACTIVE rc0 if late complete, not retro PASS")
    # Try resume ALREADY_ACTIVE readonly
    try:
        st=json.loads((FIX/STATE).read_bytes())
        rec=st.get("publication_revalidation_provenance",{}).get("path","")
        log(f"state after timeout active {rec}")
        RESUME_CHK=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.resume_activation(str(root), sys.argv[2], sys.argv[3])
print(json.dumps(res,indent=1))
"""
        pr=run([PY,"-c",RESUME_CHK,str(FIX),STATE,rec],REPO,"ed-resume-already",timeout=600)
        if pr is not None and pr.returncode==0:
            log("RESUME ALREADY_ACTIVE rc0 — late complete State, terminal rc0")
        else:
            log("FATAL activate timeout, resume also failed")
            CTRL_RES.write_text("TIMEOUT activate\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout activate"); sys.exit(2)
    except Exception as e:
        log(f"activate timeout exception {e}")
        CTRL_RES.write_text("TIMEOUT activate\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("timeout activate"); sys.exit(2)
elif pact.returncode!=0:
    # Check if already active? Try resume
    log(f"activate exit={pact.returncode}, checking resume")
    try:
        st=json.loads((FIX/STATE).read_bytes())
        rec=st.get("publication_revalidation_provenance",{}).get("path","")
        log(f"state active {rec}")
        RESUME_CHK2=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.resume_activation(str(root), sys.argv[2], sys.argv[3])
print(json.dumps(res,indent=1))
"""
        pr2=run([PY,"-c",RESUME_CHK2,str(FIX),STATE,rec],REPO,"ed-resume-check",timeout=600)
        if pr2 is not None and pr2.returncode==0:
            log("RESUME ALREADY_ACTIVE rc0")
        else:
            log("FATAL activate")
            CTRL_RES.write_text("FAIL activate\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail activate"); sys.exit(1)
    except Exception as e:
        log(f"activate fail {e}")
        CTRL_RES.write_text("FAIL activate\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail activate"); sys.exit(1)
else:
    log("ACTIVATED EDITORIAL r3")
# Readbacks: public history/current receipt/selected Candidate
st_after=json.loads((FIX/STATE).read_bytes())
rec_path=st_after.get("publication_revalidation_provenance",{}).get("path","")
log(f"active record {rec_path}")
HIST=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.verify_activation_history(str(root), sys.argv[2])
print(json.dumps({"HIST":res},indent=1)[:4000])
"""
phist=run([PY,"-c",HIST,str(FIX),rec_path],REPO,"ed-history",timeout=600)
if phist is None or phist.returncode!=0:
    log("FATAL history")
    CTRL_RES.write_text("FAIL history\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail history"); sys.exit(1)
CURR=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_agent_control_v2 as agent
root=Path(sys.argv[1])
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
state=json.loads((root/sys.argv[2]).read_bytes())
errs=agent.validate_agent_state(root, cfg, state)
print(json.dumps({"errs":errs},indent=1))
import sys as _s; _s.exit(0 if errs==[] else 2)
"""
pcurr=run([PY,"-c",CURR,str(FIX),STATE],REPO,"ed-current-state",timeout=600)
if pcurr is None or pcurr.returncode!=0:
    log("FATAL current State")
    CTRL_RES.write_text("FAIL current\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail current"); sys.exit(1)
RECEIPT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_publication_v2 as edpub
root=Path(sys.argv[1])
res=edpub.validate_editorial_receipt(str(root), sys.argv[2], sys.argv[3])
print(json.dumps({"kind":res.get("kind"),"route":res.get("generator_route"),"issue":res.get("issue_id")},indent=1))
"""
receipt_rel=f"{PDIR_NEW}/publication/validated-source-manifest.json"
prec=run([PY,"-c",RECEIPT,str(FIX),receipt_rel,STATE],REPO,"ed-receipt",timeout=600)
if prec is None or prec.returncode!=0:
    log("FATAL receipt")
    CTRL_RES.write_text("FAIL receipt\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail receipt"); sys.exit(1)
# Selected Candidate readback: State-selected seal/Candidate + seal file
CAND=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1])
state=json.loads((root/sys.argv[2]).read_bytes())
# State-selected Candidate? Derive via publication set selection? Use State provenance + seal
prov=state.get("publication_revalidation_provenance",{})
print(json.dumps({"provenance":prov},indent=1))
# Load seal to get Candidate ref
from scripts import survey_publication_set_v2 as setmod
import pathlib as _pl
# Find seal path from record
rec=json.loads((root/sys.argv[3]).read_bytes())
set_ref=rec.get("set_ref") or {}
print(json.dumps({"set_ref":set_ref},indent=1))
seal=json.loads((root/set_ref.get("path")).read_bytes()) if isinstance(set_ref,dict) and "path" in set_ref else {}
print(json.dumps({"seal_kind":seal.get("kind"),"seal_status":seal.get("status"),"candidate_ref":seal.get("candidate_ref") or seal.get("candidate")},indent=1)[:2000])
"""
pcand=run([PY,"-c",CAND,str(FIX),STATE,rec_path],REPO,"ed-candidate",timeout=600)
if pcand is None or pcand.returncode!=0:
    log("FATAL candidate readback")
    CTRL_RES.write_text("FAIL candidate\n",encoding="utf-8"); CTRL_EXIT.write_text("1\n",encoding="utf-8"); beat("fail candidate"); sys.exit(1)
log("ED FINAL SUCCESS r3 HIST CURRENT receipt Candidate all 0")
CTRL_RES.write_text("SUCCESS EDITORIAL r3\n",encoding="utf-8")
CTRL_EXIT.write_text("0\n",encoding="utf-8")
beat("success")
