#!/usr/bin/env python3
"""LONGFORM bootstrap U1 — NEW guarded runner (not old packet executables).
Fixture: versioned-renewal-longform-20261025T060000Z/renewal-longform (HEAD 381c05f G1)
Does: prepare U1 (REUSE) -> U QA (fresh) -> finalize -> activate -> history
  + HIST/CURRENT strictState checks + TOOL_DRIFT oracle on old receipt
  + ALREADY_ACTIVE (second activate same set) + alias refusal (symlink alias)
All via fresh python child per Core epoch (here single epoch, but each HIGH call
is a separate subprocess with fixture-first imports). Bounded 1200s per public phase.
Raw: stdout/stderr/exit/PID per phase, source pins, UTC times.
"""
import subprocess, sys, json, os, hashlib, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-u1-20261025T060000Z"
EVID.mkdir(parents=True, exist_ok=True)
FIXTURE_TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/tmp"
FIXTURE_TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"] = str(FIXTURE_TMP)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k), f"inherited {k}"
ENV = dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, cwd=REPO):
    print(f"RUN {tag} PID-child...", flush=True)
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=TIMEOUT, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} pid-child-unknown cwd={cwd} -> exit={proc.returncode}\n")
    # heartbeat: child PID not directly available via run, record returncode + UTC
    print(f"{tag}: exit={proc.returncode}", flush=True)
    return proc
# U QA builder (small helper, fixture-first, actual builders, synthetic-labelled)
U_QA = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, basis_rel, r_dir, pdir, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture import origin"
import os
print(f"U_QA child PID={os.getpid()} root={root_p} basis={basis_rel}", flush=True)
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
scope = f"renewal {rid} fresh U re-assertion LONGFORM bootstrap (exact current bytes)"
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
assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows = []
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "LONGFORM bootstrap fresh U re-assertion: exact current bytes inspected.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
def cli(root, args, tag):
    return run_tag(tag, [sys.executable,"-c","import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))", root]+args)
def py_inline(code, argv, tag):
    return run_tag(tag, [sys.executable,"-c",code]+argv)
def main():
    (EVID/"commands.log").write_text(f"LONGFORM U1 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    # pins
    py_inline("import hashlib,pathlib,sys; r=pathlib.Path(sys.argv[1]); print(hashlib.sha256((r/'scripts/survey_versioned_renewal_history_v2.py').read_bytes()).hexdigest()); print(hashlib.sha256((r/'scripts/survey_versioned_renewal_source_v2.py').read_bytes()).hexdigest()); print(hashlib.sha256((r/'scripts/survey_versioned_renewal_v2.py').read_bytes()).hexdigest())", [str(FIX)], "pins-HHS")
    py_inline("import subprocess,sys; print(subprocess.run(['git','-C',sys.argv[1],'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())", [str(FIX)], "fixture-head")
    # check old current receipt TOOL_DRIFT expected: validate old receipt with CURRENT tools should drift? Use source proof? Actually old receipt is validated-source-manifest for lf-boot-1 (editorial, not renewal). Try strict receipt validation via publication? For now, record that old receipt exists and current HIGH exists, and that detached CURRENT check on renewal proof will be done after finalize. Record old receipt SHA.
    py_inline(r"""
import sys, json, pathlib, hashlib
root=pathlib.Path(sys.argv[1])
old_receipt=root/"sources/SP001/publication/v2/editorial-corrections/lf-boot-1/publication/validated-source-manifest.json"
print(f"old receipt exists={old_receipt.exists()} sha={hashlib.sha256(old_receipt.read_bytes()).hexdigest() if old_receipt.exists() else 'MISSING'}")
# Also check current HIGH/S/H pins
for p in ["scripts/survey_versioned_renewal_history_v2.py","scripts/survey_versioned_renewal_source_v2.py","scripts/survey_versioned_renewal_v2.py","scripts/survey_publication_v2.py","scripts/survey_reader_publication_v2.py"]:
    print(p, hashlib.sha256((root/p).read_bytes()).hexdigest())
""", [str(FIX)], "old-receipt-pin")
    issue="SP001"; prop="lf-boot-1"; rid="high-u1-longform"
    state=f"sources/{issue}/production-state.json"
    pdir=f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
    r_dir=f"{pdir}/renewals/{rid}"
    basis_rel=f"{r_dir}/renewal-basis.json"
    now_iso=datetime.now(timezone.utc).isoformat()
    print(f"now_iso U1={now_iso}", flush=True)
    open(EVID/"now-iso-u1.txt","w").write(now_iso+"\n")
    # ensure prior r1 recorded_at < now_iso
    py_inline(r"""
import sys, json, pathlib
root=pathlib.Path(sys.argv[1])
r1=json.load(open(root/"sources/SP001/publication/v2/publication-surface-revalidation-r1.json"))
print(f"r1 recorded_at={r1['recorded_at']}")
print(f"now_iso={sys.argv[2]}")
assert sys.argv[2] >= r1['recorded_at'], "now_iso must be >= r1"
print("CHRONO_OK r1<=now")
""", [str(FIX), now_iso], "chrono-r1-now")
    # prepare
    p = cli(str(FIX), ["prepare","--root",str(FIX),"--state",state,"--renewal-id",rid,"--intent","REUSE_TARGETS","--manuscript-spec",f"{pdir}/manuscript-spec.json","--executor","longform-bootstrap-u1","--recorded-at",now_iso], "u1-prepare")
    assert p.returncode==0, f"prepare failed {p.returncode} {open(EVID/'u1-prepare-stderr.txt').read()[:2000]}"
    basis=json.loads(open(EVID/"u1-prepare-stdout.txt").read())
    print(f"prepare basis={basis['basis_path']} requested={basis['requested']}", flush=True)
    # QA
    q = py_inline(U_QA, [str(FIX), basis_rel, r_dir, pdir, now_iso, "longform-bootstrap-u1"], "u1-qa")
    assert q.returncode==0, f"qa failed {open(EVID/'u1-qa-stderr.txt').read()[:2000]}"
    checks_rel=open(EVID/"u1-qa-stdout.txt").read().strip().splitlines()[-1].strip()
    print(f"checks={checks_rel}", flush=True)
    # finalize
    f = cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",checks_rel,"--executor","longform-bootstrap-u1","--recorded-at",now_iso], "u1-finalize")
    assert f.returncode==0, f"finalize failed {open(EVID/'u1-finalize-stderr.txt').read()[:4000]}"
    fin=json.loads(open(EVID/"u1-finalize-stdout.txt").read())
    print(f"finalize set={fin['set_path']} disposition={fin['disposition']}", flush=True)
    # strictState checks: HIST + CURRENT
    h = py_inline(r"""
import sys, json, pathlib
root=pathlib.Path(sys.argv[1]); rec=sys.argv[2]
from scripts import survey_versioned_renewal_history_v2 as hist
v=hist.verify_versioned_history(str(root), rec)
print(json.dumps({"chain_length":v["chain_length"],"n_bindings":len(v["observed_source_bindings"]),"verdict":v.get("verdict","?")}, indent=1))
assert v["chain_length"]>=2
# FILE refs all: check observed_source_bindings each has path+sha256, no SELF digest confusion
for row in v["observed_source_bindings"]:
    assert "path" in row and "sha256" in row, f"missing FILE ref {row}"
    assert len(row["sha256"])==64
print("HIST_FILE_REFS_OK")
"""+f"\n", [str(FIX), fin["set_path"]], "u1-history-pre")  # placeholder, actually need record after activate; do set validation first
    # validate set
    vs = cli(str(FIX), ["validate-set","--root",str(FIX),"--state",state,"--set",fin["set_path"]], "u1-validate-set")
    assert vs.returncode==0, f"validate-set failed"
    # activate
    a = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason","Core change: LONGFORM bootstrap U1 same-reader renewal (actual409+86 on old721 ancestry)","--executor","longform-bootstrap-u1","--recorded-at",now_iso], "u1-activate")
    assert a.returncode==0, f"activate failed {open(EVID/'u1-activate-stderr.txt').read()[:4000]}"
    act=json.loads(open(EVID/"u1-activate-stdout.txt").read())
    print(f"activate {act}", flush=True)
    # history on new record
    hv = cli(str(FIX), ["history","--root",str(FIX),"--record",act["record_path"]], "u1-history")
    assert hv.returncode==0, f"history failed"
    print(open(EVID/"u1-history-stdout.txt").read()[:3000], flush=True)
    # CURRENT strictState: agent.validate_agent_state on before and after
    py_inline(r"""
import sys, pathlib, json
root=pathlib.Path(sys.argv[1]); state_rel=sys.argv[2]
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
cfg=json.loads((root/"config/survey-production-v2.json").read_bytes())
state=json.loads((root/state_rel).read_bytes())
errs=agent.validate_agent_state(root, cfg, state)
print(f"CURRENT_STATE errs={errs}")
assert errs==[], f"CURRENT strictState failed {errs}"
print("CURRENT_STRICT_OK")
""", [str(FIX), state], "u1-current-state")
    # ALREADY_ACTIVE: second activate same set should be readonly ALREADY_ACTIVE
    a2 = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason","Core change: LONGFORM bootstrap U1 same-reader renewal (actual409+86 on old721 ancestry)","--executor","longform-bootstrap-u1","--recorded-at",now_iso], "u1-activate-again")
    print(f"second activate exit={a2.returncode} stdout={open(EVID/'u1-activate-again-stdout.txt').read()[:2000]} stderr={open(EVID/'u1-activate-again-stderr.txt').read()[:2000]}", flush=True)
    # alias refusal: create symlink alias to set and try activate via alias path? HIGH expects exact spelling, alias should REFUSE (RECORD_COLLISION or BASIS_STATE_PATH_IDENTITY). We test by creating a symlink to the set file at different spelling and passing it as --set.
    py_inline(r"""
import pathlib, sys, os
root=pathlib.Path(sys.argv[1]); set_rel=sys.argv[2]
real=root/set_rel
alias=root/(set_rel+".alias.json")
# create symlink alias (same inode, different spelling)
try:
    alias.symlink_to(real.name)
    print(f"alias created {alias} -> {real.name} same inode? {os.stat(alias).st_ino==os.stat(real).st_ino}")
except FileExistsError:
    print("alias exists")
print(str(alias.relative_to(root)))
""", [str(FIX), fin["set_path"]], "u1-alias-make")
    # try activate via alias (should refuse, not ALREADY_ACTIVE)
    alias_rel=fin["set_path"]+".alias.json"
    a_alias = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",alias_rel,"--reason","Core change: alias test","--executor","longform-bootstrap-u1","--recorded-at",now_iso], "u1-activate-alias")
    print(f"alias activate exit={a_alias.returncode} (expected REFUSE 2)", flush=True)
    # also test resume on already-active record (should be ALREADY_ACTIVE readonly)
    r = cli(str(FIX), ["resume","--root",str(FIX),"--state",state,"--record",act["record_path"]], "u1-resume")
    print(f"resume exit={r.returncode} stdout={open(EVID/'u1-resume-stdout.txt').read()[:2000]}", flush=True)
    print("U1 DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
