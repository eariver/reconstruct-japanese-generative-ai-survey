#!/usr/bin/env python3
"""LONGFORM G3/G4 + C->U->U (U2 r4, U3 r5).
G3: H comment only; G4: S comment only; style unchanged.
U2 (prior C1 r3) -> U3 (prior U2 r4), each prepare/finalize/activate/history + readback.
Chronology strictly >= predecessor (raw recorded_at inspect).
"""
import subprocess, sys, json, os, hashlib, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-g34-uu-20261025T060000Z"
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
scope = f"renewal {rid} fresh U LONGFORM G3/G4 (exact current bytes)"
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
                 "evidence": "LONGFORM G3/G4 fresh U.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
def do_u(rid, reason, tag_prefix):
    issue="SP001"; prop="lf-boot-1"
    state=f"sources/{issue}/production-state.json"
    pdir=f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
    r_dir=f"{pdir}/renewals/{rid}"
    basis_rel=f"{r_dir}/renewal-basis.json"
    # inspect predecessor recorded_at
    pred_info = py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
ptr=state.get("publication_revalidation_provenance",{})
print(f"current State pointer={ptr}")
rec=json.load(open(root/ptr["path"]))
print(f"predecessor record {ptr['path']} recorded_at={rec['recorded_at']} kind={rec.get('kind')}")
""", [str(FIX)], f"{tag_prefix}-pred-inspect")
    # choose now strictly >= predecessor
    import time
    time.sleep(1)
    now_iso=datetime.now(timezone.utc).isoformat()
    open(EVID/f"now-iso-{rid}.txt","w").write(now_iso+"\n")
    print(f"{rid} now_iso={now_iso}", flush=True)
    # verify chrono >= predecessor
    c = py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); now=sys.argv[2]
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
ptr=state.get("publication_revalidation_provenance",{})
rec=json.load(open(root/ptr["path"]))
print(f"pred {rec['recorded_at']} now {now}")
assert now >= rec['recorded_at'], f"now {now} < pred {rec['recorded_at']}"
print("CHRONO_OK")
""", [str(FIX), now_iso], f"{tag_prefix}-chrono")
    assert c.returncode==0
    p = cli(str(FIX), ["prepare","--root",str(FIX),"--state",state,"--renewal-id",rid,"--intent","REUSE_TARGETS","--manuscript-spec",f"{pdir}/manuscript-spec.json","--executor",f"longform-{tag_prefix}","--recorded-at",now_iso], f"{tag_prefix}-prepare")
    assert p.returncode==0, f"prepare failed {open(EVID/f'{tag_prefix}-prepare-stderr.txt').read()[:4000]}"
    q = py_inline(U_QA_BUILDER, [str(FIX), basis_rel, r_dir, pdir, now_iso, f"longform-{tag_prefix}"], f"{tag_prefix}-qa")
    assert q.returncode==0, f"qa failed {open(EVID/f'{tag_prefix}-qa-stderr.txt').read()[:3000]}"
    checks_rel=open(EVID/f"{tag_prefix}-qa-stdout.txt").read().strip().splitlines()[-1].strip()
    f = cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",checks_rel,"--executor",f"longform-{tag_prefix}","--recorded-at",now_iso], f"{tag_prefix}-finalize")
    assert f.returncode==0, f"finalize failed {open(EVID/f'{tag_prefix}-finalize-stderr.txt').read()[:5000]}"
    fin=json.loads(open(EVID/f"{tag_prefix}-finalize-stdout.txt").read())
    print(f"finalize {fin['set_path']} {fin['disposition']}", flush=True)
    # verify older embedded C proof lineage HIST not forced latest: check proof's prior? For U, proof should bind immediate predecessor, stored manuscript/build proof may be older ancestor. We record proof basis.
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); basis_rel=sys.argv[2]
basis=json.loads((root/basis_rel).read_bytes())
print(f"basis prior_selected={basis['prior_selected_ref']}")
print(f"basis prior_record={basis['prior_record_ref']}")
# prior_selected should be immediate predecessor (C1 for U2, U2 for U3)
""", [str(FIX), basis_rel], f"{tag_prefix}-lineage-inspect")
    a = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason",reason,"--executor",f"longform-{tag_prefix}","--recorded-at",now_iso], f"{tag_prefix}-activate")
    assert a.returncode==0, f"activate failed exit={a.returncode} {open(EVID/f'{tag_prefix}-activate-stderr.txt').read()[:5000]}"
    act=json.loads(open(EVID/f"{tag_prefix}-activate-stdout.txt").read())
    print(f"activate {act}", flush=True)
    h = cli(str(FIX), ["history","--root",str(FIX),"--record",act["record_path"]], f"{tag_prefix}-history")
    assert h.returncode==0
    print(open(EVID/f"{tag_prefix}-history-stdout.txt").read()[:3000], flush=True)
    # current new proof every readback: verify proof with CURRENT tools
    v = py_inline(r"""
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1]); basis_rel=sys.argv[2]; proof_rel=sys.argv[3]
from scripts import survey_versioned_renewal_source_v2 as srcmod
srcmod.verify_renewal_source_proof(str(root), basis_rel, proof_rel)
print("CURRENT_PROOF_READBACK_OK")
""", [str(FIX), basis_rel, fin["proof_path"]], f"{tag_prefix}-proof-readback")
    assert v.returncode==0, f"proof readback failed {open(EVID/f'{tag_prefix}-proof-readback-stderr.txt').read()[:3000]}"
    return act, fin
def main():
    (EVID/"commands.log").write_text(f"LONGFORM G3/G4 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("g34-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    # record style SHA before G3/G4 (must stay unchanged after C)
    style_path = FIX/"templates/survey/jgaisurvey.sty"
    style_before = hashlib.sha256(style_path.read_bytes()).hexdigest()
    print(f"style_before={style_before}", flush=True)
    open(EVID/"style-before.txt","w").write(style_before+"\n")
    # G3: H comment only
    h_path = FIX/"scripts/survey_versioned_renewal_history_v2.py"
    ht = h_path.read_text(encoding="utf-8")
    assert "# G3 LONGFORM" not in ht
    lines=ht.splitlines(True); lines.insert(1, "# G3 LONGFORM eligible Core comment — hashed implementation only, style unchanged\n")
    h_path.write_text("".join(lines), encoding="utf-8")
    run_tag("g3-add", ["git","-C",str(FIX),"add","--","scripts/survey_versioned_renewal_history_v2.py"])
    run_tag("g3-commit", ["git","-C",str(FIX),"commit","-m","LONGFORM TEST-ONLY: G3 eligible H comment (hashed impl only, style unchanged)","--no-verify"])
    assert run_tag("g3-head", ["git","-C",str(FIX),"rev-parse","HEAD"]).returncode==0
    # verify style unchanged
    style_g3 = hashlib.sha256(style_path.read_bytes()).hexdigest()
    assert style_g3==style_before, f"style changed at G3 {style_g3} vs {style_before}"
    print(f"G3 style unchanged OK {style_g3[:12]}", flush=True)
    # G4: S comment only
    s_path = FIX/"scripts/survey_versioned_renewal_source_v2.py"
    st = s_path.read_text(encoding="utf-8")
    assert "# G4 LONGFORM" not in st
    lines=st.splitlines(True); lines.insert(1, "# G4 LONGFORM eligible Core comment — hashed implementation only, style unchanged\n")
    s_path.write_text("".join(lines), encoding="utf-8")
    run_tag("g4-add", ["git","-C",str(FIX),"add","--","scripts/survey_versioned_renewal_source_v2.py"])
    run_tag("g4-commit", ["git","-C",str(FIX),"commit","-m","LONGFORM TEST-ONLY: G4 eligible S comment (hashed impl only, style unchanged)","--no-verify"])
    run_tag("g4-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    run_tag("g4-log", ["git","-C",str(FIX),"log","--oneline","-5"])
    style_g4 = hashlib.sha256(style_path.read_bytes()).hexdigest()
    assert style_g4==style_before, f"style changed at G4"
    print(f"G4 style unchanged OK", flush=True)
    # U2
    act2, fin2 = do_u("high-u2-longform", "Core change: LONGFORM G3 H comment advancing tool chain (C->U link)", "u2")
    # verify no old State equality after switch: State should be r4, not r3
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
ptr=state["publication_revalidation_provenance"]
print(f"post-U2 State pointer={ptr}")
assert "r4" in ptr["path"], f"expected r4 after U2, got {ptr['path']}"
# old r3 still exists immutable?
assert (root/"sources/SP001/publication/v2/publication-surface-revalidation-r3.json").exists()
print("NO_OLD_STATE_EQUALITY_OK (r4 active, r3 preserved immutable)")
""", [str(FIX)], "u2-state-switch")
    # U3
    act3, fin3 = do_u("high-u3-longform", "Core change: LONGFORM G4 S comment advancing tool chain (U repeat, completes C->U->U)", "u3")
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
state=json.loads((root/"sources/SP001/production-state.json").read_bytes())
ptr=state["publication_revalidation_provenance"]
print(f"post-U3 State pointer={ptr}")
assert "r5" in ptr["path"], f"expected r5 after U3, got {ptr['path']}"
# verify C->U->U chain: r1 editorial, r2 U1, r3 C1, r4 U2, r5 U3
from scripts import survey_versioned_renewal_history_v2 as hist
v=hist.verify_versioned_history(str(root), ptr["path"])
print(f"chain_length={v['chain_length']} n_bindings={len(v['observed_source_bindings'])}")
for ref in v["observed_refs"]:
    print(ref["kind"], ref["record_sha"][:12])
assert v["chain_length"]==5, f"expected 5, got {v['chain_length']}"
print("C_TO_U_TO_U_OK")
""", [str(FIX)], "u3-chain-verify")
    print("G3/G4 U2/U3 DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
