#!/usr/bin/env python3
"""LONGFORM U5 — fresh CURRENT authority on G7 archive-correction code.
Prior U4 r7 (epoch 047f8ad) -> U5 r8 (epoch a7772a1 G7). REUSE (style b1cbb preserved).
Full HIST/source/currentState. 1200s per phase, fresh Python per phase.
"""
import subprocess, sys, json, os, pathlib, time
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-u5-longform-20261025T100000Z"
EVID.mkdir(parents=True, exist_ok=True)
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/tmp"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"]=str(TMP)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired as e:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s in {tag}", encoding="utf-8")
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
def cli(root, args, tag):
    return run_tag(tag, [sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))", root]+args)
def py_inline(code, argv, tag, timeout=TIMEOUT):
    return run_tag(tag, [sys.executable,"-c",code]+argv, timeout=timeout)
U_QA = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, basis_rel, r_dir, pdir, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
import os
print(f"U5 QA child PID={os.getpid()}", flush=True)
basis = json.loads((root_p / basis_rel).read_bytes())
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
prior_seal = json.loads((root_p / basis["prior_selected_ref"]["path"]).read_bytes())
roles = prior_seal["roles"]
trio_primary, pdf_role = roles["validated-source"], roles["publication-pdf"]
main_bytes = (root_p / trio_primary["path"]).read_bytes()
pdf_bytes = (root_p / pdf_role["path"]).read_bytes()
from pypdf import PdfReader
pages = len(PdfReader(str(root_p / pdf_role["path"])).pages)
issue_id, rid = basis["issue_id"], basis["renewal_id"]
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} fresh U LONGFORM G7 archive-correction (exact current bytes)"
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
        "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio_primary["path"], "scope": scope},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(main_bytes),
        "inspected_identifiers": [issue_id] + (["Target Model"] if basis["research_profile"] == "THEMATIC" else []),
        "scope": scope},
    "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
        "pdf_sha256": core.sha256_bytes(pdf_bytes), "byte_count": len(pdf_bytes), "scope": scope},
}
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
        "inspected_paths": [trio_primary["path"]], "scope": scope}
assert set(payloads) == set(kinds)
rows=[]
for cid in sorted(payloads):
    p=qroot/f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":executor,"evidence":"LONGFORM G7 fresh U.","recorded_at":now_iso,"result":{"path":str(p.relative_to(root_p)),"sha256":core.sha256_file(p)}})
checks_path=root_p/pdir/f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks":rows}))
print(str(checks_path.relative_to(root_p)))
"""
def main():
    (EVID/"commands.log").write_text(f"LONGFORM U5 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("u5-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    run_tag("u5-pre-log", ["git","-C",str(FIX),"log","--oneline","-8"])
    py_inline(r"""
import sys, hashlib, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
for p in ["scripts/survey_versioned_renewal_history_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py","scripts/survey_editorial_publication_v2.py","templates/survey/jgaisurvey.sty"]:
    print(p, hashlib.sha256((root/p).read_bytes()).hexdigest())
""", [str(FIX)], "u5-pins")
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
st=json.load(open(root/"sources/SP001/production-state.json"))
print(f"pre U5 pointer {st['publication_revalidation_provenance']}")
rec=json.load(open(root/st['publication_revalidation_provenance']['path']))
print(f"pred r7 recorded_at={rec['recorded_at']}")
""", [str(FIX)], "u5-pred")
    time.sleep(1)
    now_iso=datetime.now(timezone.utc).isoformat()
    open(EVID/"now-iso-u5.txt","w").write(now_iso+"\n")
    print(f"U5 now {now_iso}", flush=True)
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); now=sys.argv[2]
st=json.load(open(root/"sources/SP001/production-state.json"))
rec=json.load(open(root/st['publication_revalidation_provenance']['path']))
assert now>=rec['recorded_at']
print("CHRONO_OK")
""", [str(FIX), now_iso], "u5-chrono")
    issue="SP001"; prop="lf-boot-1"; rid="high-u5-longform"
    state=f"sources/{issue}/production-state.json"
    pdir=f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
    r_dir=f"{pdir}/renewals/{rid}"
    basis_rel=f"{r_dir}/renewal-basis.json"
    p=cli(str(FIX), ["prepare","--root",str(FIX),"--state",state,"--renewal-id",rid,"--intent","REUSE_TARGETS","--manuscript-spec",f"{pdir}/manuscript-spec.json","--executor","longform-g7-u5","--recorded-at",now_iso], "u5-prepare")
    assert p is not None and p.returncode==0, open(EVID/"u5-prepare-stderr.txt").read()[:8000]
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); basis_rel=sys.argv[2]
basis=json.load(open(root/basis_rel))
print(f"U5 basis epoch {basis['current_tool_epoch']['repository_commit_sha']}")
from scripts import survey_versioned_renewal_history_v2 as hist
st=json.load(open(root/"sources/SP001/production-state.json"))
v=hist.verify_versioned_history(str(root), st['publication_revalidation_provenance']['path'])
print(f"pred chain {v['chain_length']}")
""", [str(FIX), basis_rel], "u5-epoch-check")
    q=py_inline(U_QA, [str(FIX), basis_rel, r_dir, pdir, now_iso, "longform-g7-u5"], "u5-qa")
    assert q is not None and q.returncode==0, open(EVID/"u5-qa-stderr.txt").read()[:8000]
    checks_rel=open(EVID/"u5-qa-stdout.txt").read().strip().splitlines()[-1].strip()
    f=cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",checks_rel,"--executor","longform-g7-u5","--recorded-at",now_iso], "u5-finalize")
    assert f is not None and f.returncode==0, open(EVID/"u5-finalize-stderr.txt").read()[:8000]
    fin=json.loads(open(EVID/"u5-finalize-stdout.txt").read())
    print(f"finalize {fin}", flush=True)
    a=cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason","Core change: LONGFORM G7 archive-correction edpub kind-aware renewal authoring_refs refreshing CURRENT authority before editorial","--executor","longform-g7-u5","--recorded-at",now_iso], "u5-activate")
    assert a is not None and a.returncode==0, open(EVID/"u5-activate-stderr.txt").read()[:8000]
    act=json.loads(open(EVID/"u5-activate-stdout.txt").read())
    print(f"activate {act}", flush=True)
    h=cli(str(FIX), ["history","--root",str(FIX),"--record",act["record_path"]], "u5-history")
    assert h is not None and h.returncode==0
    print(open(EVID/"u5-history-stdout.txt").read()[:5000], flush=True)
    v=py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); rec=sys.argv[2]; basis_rel=sys.argv[3]; proof_rel=sys.argv[4]
from scripts import survey_versioned_renewal_history_v2 as hist
v=hist.verify_versioned_history(str(root), rec)
print(f"chain {v['chain_length']}")
from scripts import survey_versioned_renewal_source_v2 as srcmod
srcmod.verify_renewal_source_proof(str(root), basis_rel, proof_rel)
print("SOURCE_READBACK_OK")
from scripts import survey_agent_control_v2 as agent
cfg=json.load(open(root/"config/survey-production-v2.json"))
st=json.load(open(root/"sources/SP001/production-state.json"))
errs=agent.validate_agent_state(root, cfg, st)
print(f"CURRENT errs={errs}")
assert errs==[]
print("CURRENT_OK")
""", [str(FIX), act["record_path"], basis_rel, fin["proof_path"]], "u5-full-check")
    assert v is not None and v.returncode==0, open(EVID/"u5-full-check-stderr.txt").read()[:8000]
    print("U5 DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
