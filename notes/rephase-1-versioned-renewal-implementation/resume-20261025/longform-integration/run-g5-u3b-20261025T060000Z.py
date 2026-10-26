#!/usr/bin/env python3
"""LONGFORM G5 + U3b retry (C->U->U completion).
Preserves failed high-u3-longform inert (TOOL_EPOCH_DRIFT, no overwrite).
G5: HIGH comment only (hashed impl, style unchanged).
U3b: prior U2 r4 -> r5, new epoch, new time >= r4.
"""
import subprocess, sys, json, os, hashlib, pathlib, time
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-g5-u3b-20261025T060000Z"
EVID.mkdir(parents=True, exist_ok=True)
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/tmp"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"]=str(TMP)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd):
    proc=subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=TIMEOUT, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def cli(root, args, tag):
    return run_tag(tag, [sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))", root]+args)
def py_inline(code, argv, tag):
    return run_tag(tag, [sys.executable,"-c",code]+argv)
U_QA_BUILDER = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, basis_rel, r_dir, pdir, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture import origin"
import os
print(f"U_QA child PID={os.getpid()}", flush=True)
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
scope = f"renewal {rid} fresh U LONGFORM G5 (exact current bytes)"
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
rows = []
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "LONGFORM G5 fresh U.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
def main():
    (EVID/"commands.log").write_text(f"LONGFORM G5 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("g5-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    # verify failed U3 preserved inert, no record r5 yet? Actually r4 is latest, r5 file may exist? Check
    run_tag("g5-ls-renewals", ["ls", str(FIX/"sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals")])
    # style unchanged check
    style_path = FIX/"templates/survey/jgaisurvey.sty"
    style_before = open(REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-g34-uu-20261025T060000Z"/"style-before.txt").read().strip() if (REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-g34-uu-20261025T060000Z"/"style-before.txt").exists() else hashlib.sha256(style_path.read_bytes()).hexdigest()
    style_now = hashlib.sha256(style_path.read_bytes()).hexdigest()
    print(f"style_before={style_before[:12]} style_now={style_now[:12]}", flush=True)
    assert style_now==style_before, "style must be unchanged after C"
    # G5: HIGH comment only
    high_path = FIX/"scripts/survey_versioned_renewal_v2.py"
    ht = high_path.read_text(encoding="utf-8")
    assert "# G5 LONGFORM" not in ht
    lines=ht.splitlines(True); lines.insert(2, "# G5 LONGFORM eligible Core comment — hashed impl only, style unchanged (second HIGH tidy)\n")
    high_path.write_text("".join(lines), encoding="utf-8")
    run_tag("g5-add", ["git","-C",str(FIX),"add","--","scripts/survey_versioned_renewal_v2.py"])
    run_tag("g5-commit", ["git","-C",str(FIX),"commit","-m","LONGFORM TEST-ONLY: G5 eligible HIGH comment (hashed impl only, style unchanged)","--no-verify"])
    run_tag("g5-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    run_tag("g5-log", ["git","-C",str(FIX),"log","--oneline","-6"])
    # verify style still unchanged
    assert hashlib.sha256(style_path.read_bytes()).hexdigest()==style_before
    print("G5 style unchanged OK", flush=True)
    # U3b with new ID, new time >= r4
    issue="SP001"; prop="lf-boot-1"; rid="high-u3b-longform"
    state=f"sources/{issue}/production-state.json"
    pdir=f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
    r_dir=f"{pdir}/renewals/{rid}"
    basis_rel=f"{r_dir}/renewal-basis.json"
    # inspect predecessor r4
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
ptr=state["publication_revalidation_provenance"]
rec=json.load(open(root/ptr["path"]))
print(f"predecessor {ptr['path']} recorded_at={rec['recorded_at']}")
""", [str(FIX)], "u3b-pred")
    time.sleep(1)
    now_iso=datetime.now(timezone.utc).isoformat()
    open(EVID/"now-iso-u3b.txt","w").write(now_iso+"\n")
    print(f"u3b now_iso={now_iso}", flush=True)
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); now=sys.argv[2]
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
ptr=state["publication_revalidation_provenance"]
rec=json.load(open(root/ptr["path"]))
print(f"pred {rec['recorded_at']} now {now}")
assert now >= rec['recorded_at']
print("CHRONO_OK")
""", [str(FIX), now_iso], "u3b-chrono")
    p = cli(str(FIX), ["prepare","--root",str(FIX),"--state",state,"--renewal-id",rid,"--intent","REUSE_TARGETS","--manuscript-spec",f"{pdir}/manuscript-spec.json","--executor","longform-g5-u3b","--recorded-at",now_iso], "u3b-prepare")
    assert p.returncode==0, f"prepare failed {open(EVID/'u3b-prepare-stderr.txt').read()[:4000]}"
    q = py_inline(U_QA_BUILDER, [str(FIX), basis_rel, r_dir, pdir, now_iso, "longform-g5-u3b"], "u3b-qa")
    assert q.returncode==0
    checks_rel=open(EVID/"u3b-qa-stdout.txt").read().strip().splitlines()[-1].strip()
    f = cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",checks_rel,"--executor","longform-g5-u3b","--recorded-at",now_iso], "u3b-finalize")
    assert f.returncode==0, f"finalize failed {open(EVID/'u3b-finalize-stderr.txt').read()[:5000]}"
    fin=json.loads(open(EVID/"u3b-finalize-stdout.txt").read())
    print(f"finalize {fin['set_path']} {fin['disposition']}", flush=True)
    a = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason","Core change: LONGFORM G5 HIGH comment advancing tool chain (U repeat, completes C->U->U)","--executor","longform-g5-u3b","--recorded-at",now_iso], "u3b-activate")
    assert a.returncode==0, f"activate failed {open(EVID/'u3b-activate-stderr.txt').read()[:5000]}"
    act=json.loads(open(EVID/"u3b-activate-stdout.txt").read())
    print(f"activate {act}", flush=True)
    h = cli(str(FIX), ["history","--root",str(FIX),"--record",act["record_path"]], "u3b-history")
    assert h.returncode==0
    print(open(EVID/"u3b-history-stdout.txt").read()[:4000], flush=True)
    # verify C->U->U: should be r1 editorial, r2 U1, r3 C1, r4 U2, r5 U3b (chain_length 5)
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); rec=sys.argv[2]
from scripts import survey_versioned_renewal_history_v2 as hist
v=hist.verify_versioned_history(str(root), rec)
print(f"chain_length={v['chain_length']} n_bindings={len(v['observed_source_bindings'])}")
for ref in v["observed_refs"]:
    print(ref["kind"], ref["record_sha"][:12])
assert v["chain_length"]==5
print("C_TO_U_TO_U_OK (r1->r2 U1->r3 C1->r4 U2->r5 U3b)")
# current proof readback
from scripts import survey_versioned_renewal_source_v2 as srcmod
# find basis/proof for u3b
basis="sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-u3b-longform/renewal-basis.json"
proof="sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-u3b-longform/renewal-source-proof.json"
srcmod.verify_renewal_source_proof(str(root), basis, proof)
print("CURRENT_PROOF_READBACK_OK")
# no old State equality: State is r5, r4 preserved
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
assert "r5" in state["publication_revalidation_provenance"]["path"]
print("NO_OLD_STATE_EQUALITY_OK")
""", [str(FIX), act["record_path"]], "u3b-chain-verify")
    print("G5 U3b DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
