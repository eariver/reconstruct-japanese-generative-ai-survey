#!/usr/bin/env python3
"""Bounded Evidence stage acceptance operator — ONE sequence per edition (stdlib only pre/post + normal CLIs).

Authorized by astra-stage-acceptance-authorization.md. Uses existing public CLIs only:
- scripts/survey_stage_validation_v2.py (validate_stage -> CORE_STAGE_CONTRACT PASS report)
- scripts/survey_agent_control_v2.py advance-stage (build_stage_checkpoint + advance_with_checkpoint)

No monkeypatch/new API/schema/manual State pins. No reconstruct Git readback/network/Production.
PYTHONDONTWRITEBYTECODE=1 required. HOME unchanged. Clean GIT_* required.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("REFUSE: PYTHONDONTWRITEBYTECODE=1 required")

RECON_ROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
REPO_ROOT = RECON_ROOT / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
PACKET = RECON_ROOT / "notes/rephase-1-operational-rehearsal-resume-20261104"
RUN_DIR = PACKET / "stage-acceptance-20261105T125448Z"
MANIFEST = RECON_ROOT / "notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json"

EXPECTED = {
    "2026-W34": {
        "ev_rel": "sources/2026-W34/evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/evidence-accepted.json",
        "ev_sha": "edf21e4de5f7ab8db2d5189f45abc8cc6d0cf6475e532b20bcc56b0ce5660218",
        "ev_bytes": 126592,
        "views_rel": "sources/2026-W34/evidence/v2/views/accepted/574b96ff3ce87f7f2e46fcd78724bf1fbfcdad590e009be1500f03446697b5c5/edition-views-accepted.json",
        "views_sha": "3777133cc09d0189ab97cc1d8ff1f8b420108d43880f69f1745356508b8acfce",
        "views_bytes": 159498,
        "ledger_rel": "sources/2026-W34/materiality-ledger-v2.json",
        "ledger_sha": "f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d",
        "ledger_bytes": 186202,
        "comp_rel": "sources/2026-W34/profile-completeness-v2.json",
        "comp_sha": "e8c432dd6275e81df5286cb8c0d55d99e27aa0812c52a114d870dddaf0d2795f",
        "comp_bytes": 71532,
        "state_rel": "sources/2026-W34/production-state.json",
        "state_sha": "7e6a50c2b84cdc7e526f1560f02efd95184685770edb95ab35bb9a40c633ea58",
        "state_bytes": 3386,
        "review_md_src": PACKET / "reviews/w34-resume-output-review-20261105.md",
        "review_md_sha": "314b22084ae88ce50b7f583d5570f5a8b104f41229caec048656b0350a7a2cf6",
        "review_json_src": PACKET / "reviews/w34-resume-output-decision-map-20261105.json",
        "review_json_sha": "59d14b5578833e88d41a473bdebf6c7f98c2305fff8fb138db7881fd773c8d48",
        "executor": "General independent supervisory reviewer",
        "review_label": "W34 resume output BOUNDED_PROCEED to EVIDENCE_REVIEWED (409/439/3 LIMITED, 363 PARTIAL/38 VERIFIED/8 NEEDS_MORE; exact task-target names; residuals per review)",
    },
    "SP-efficient-llm-2026": {
        "ev_rel": "sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/evidence-accepted.json",
        "ev_sha": "65784e69559f9379412935fa5e7671beddee59b46b8fdb28a848d450e2b68ce0",
        "ev_bytes": 49237,
        "views_rel": "sources/SP-efficient-llm-2026/evidence/v2/views/accepted/5e722402c7e8df6077f87f0da33b2b53355f22ae3f306482dedbd27350b7145f/edition-views-accepted.json",
        "views_sha": "1557fef75b4b737379a0e84eea983d9151b7148077f65da018206a2fae2b0341",
        "views_bytes": 64222,
        "ledger_rel": "sources/SP-efficient-llm-2026/materiality-ledger-v2.json",
        "ledger_sha": "b7c85b4eb009249b355445f94a4041d4374990fccb07c38595b61c1e770c8c60",
        "ledger_bytes": 66850,
        "comp_rel": "sources/SP-efficient-llm-2026/profile-completeness-v2.json",
        "comp_sha": "d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805",
        "comp_bytes": 33683,
        "state_rel": "sources/SP-efficient-llm-2026/production-state.json",
        "state_sha": "4865998b99ab2902954619b2a7761c4ae0de77695b06ddd5b5e25d49dff4eb89",
        "state_bytes": 3454,
        "review_md_src": PACKET / "reviews/sp-evidence-final-rereview-20261105T011000Z.md",
        "review_md_sha": "eac326738edd8dc6e60ae3b129248249388f3bb2ea13af46b4acafa5fb9ebaff",
        "review_json_src": PACKET / "reviews/sp-evidence-final-rereview-20261105T011000Z-machine.json",
        "review_json_sha": "5e3c9d380f22ec3444e1f295b495ac027c82c59bf7c6c1f03810217a9ae95a37",
        "executor": "SAME NEW independent substantive Evidence reviewer",
        "review_label": "SP final BOUNDED_PROCEED to EVIDENCE_REVIEWED (160/165/15 LIMITED, 152 PARTIAL/8 VERIFIED; D165 binds pr.json only; delta 1x2 fields; residuals per review)",
    },
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def fail(msg: str):
    raise RuntimeError(msg)

def check_env():
    home = os.environ.get("HOME")
    if home != "/home/eariver":
        fail(f"HOME unchanged required, got {home!r}")
    bad = [k for k in os.environ if k.startswith("GIT_")]
    if bad:
        fail(f"clean GIT_* required, found {bad}")

def verify_pre(issue: str):
    exp = EXPECTED[issue]
    # State
    sp = REPO_ROOT / exp["state_rel"]
    if sp.is_symlink() or not sp.is_file():
        fail(f"{issue} State missing/unsafe")
    data = sp.read_bytes()
    if len(data) != exp["state_bytes"] or hashlib.sha256(data).hexdigest() != exp["state_sha"]:
        fail(f"{issue} State bytes/sha drift vs pinned pre")
    st = json.loads(data.decode("utf-8"))
    if st.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        fail(f"{issue} State not CAND")
    mc = st.get("machine_checkpoints", {})
    if not (mc.get("discovery")=="passed" and mc.get("screening")=="passed" and mc.get("evidence")=="pending" and mc.get("materiality")=="pending" and mc.get("completeness")=="pending"):
        fail(f"{issue} machine checkpoints unexpected {mc}")
    prov = st.get("checkpoint_provenance", {})
    if not (prov.get("evidence") is None and prov.get("materiality") is None and prov.get("completeness") is None):
        fail(f"{issue} checkpoint_provenance evidence trio must be null")
    if st.get("human_gates") != {"architecture_review":"pending","publication_preview":"pending"}:
        fail(f"{issue} human_gates must be pending/pending")
    if st.get("human_gate_provenance") != {"architecture_review":None,"publication_preview":None}:
        fail(f"{issue} human_gate_provenance must be null/null")
    if (REPO_ROOT / f"sources/{issue}/gates").exists():
        fail(f"{issue} gates dir must be absent")
    # checkpoints absence (allow partial progress: report/reviews may already exist after harness-fix retry, but checkpoint/State must still be pre)
    cp_dir = REPO_ROOT / f"sources/{issue}/orchestration/v2/checkpoints"
    names = sorted(os.listdir(cp_dir))
    if names != ["DISCOVERY_COLLECTED.json","ISSUE_INITIALIZED.json"]:
        fail(f"{issue} checkpoints must be exactly 2 pre (no CAND checkpoint yet), got {names}")
    if (cp_dir / "CANDIDATES_NORMALIZED.json").exists() or (cp_dir / "CANDIDATES_NORMALIZED.json").is_symlink():
        fail(f"{issue} CAND checkpoint must be absent pre")
    if (cp_dir / "EVIDENCE_REVIEWED.json").exists():
        fail(f"{issue} EVIDENCE_REVIEWED must be absent")
    # reviews/validation 2 each pre, or 3 with valid CAND partial (harness-fix resume)
    rv = sorted(os.listdir(REPO_ROOT / f"sources/{issue}/orchestration/v2/stage-reviews"))
    if rv == ["DISCOVERY_COLLECTED-reviews.json","ISSUE_INITIALIZED-reviews.json"]:
        pass
    elif rv == ["CANDIDATES_NORMALIZED-reviews.json","DISCOVERY_COLLECTED-reviews.json","ISSUE_INITIALIZED-reviews.json"]:
        pass  # valid partial reuse checked later
    else:
        fail(f"{issue} stage-reviews must be 2 pre or 3 with CAND partial, got {rv}")
    va = sorted(os.listdir(REPO_ROOT / f"sources/{issue}/orchestration/v2/stage-validation"))
    if va == ["DISCOVERY_COLLECTED-report.json","ISSUE_INITIALIZED-report.json"]:
        pass
    elif va == ["CANDIDATES_NORMALIZED-report.json","DISCOVERY_COLLECTED-report.json","ISSUE_INITIALIZED-report.json"]:
        pass
    else:
        fail(f"{issue} stage-validation must be 2 pre or 3 with CAND partial, got {va}")
    # guard absent
    guard = REPO_ROOT / f"sources/{issue}/orchestration/v2/acceptance-revision.guard.json"
    if guard.exists() or guard.is_symlink():
        fail(f"{issue} DM022 guard must be absent")
    # four artifacts
    for key, rel_key, sha_key, bytes_key in [("ev","ev_rel","ev_sha","ev_bytes"),("views","views_rel","views_sha","views_bytes"),("ledger","ledger_rel","ledger_sha","ledger_bytes"),("comp","comp_rel","comp_sha","comp_bytes")]:
        p = REPO_ROOT / exp[rel_key]
        if p.is_symlink() or not p.is_file():
            fail(f"{issue} {key} missing/unsafe {exp[rel_key]}")
        d = p.read_bytes()
        if len(d) != exp[bytes_key] or hashlib.sha256(d).hexdigest() != exp[sha_key]:
            fail(f"{issue} {key} bytes/sha drift")
    # reviews source bytes
    for rk in ["review_md_src","review_json_src"]:
        src = exp[rk]
        sha_key = "review_md_sha" if "md" in rk else "review_json_sha"
        if not src.is_file():
            fail(f"review src missing {src}")
        if sha256_file(src) != exp[sha_key]:
            fail(f"review src sha drift {src}")
    # Contract8 (pipeline/quality common + research/publication per issue from current-observation)
    contract = st.get("contract", {})
    if contract.get("pipeline_contract_sha256") != "3adfbda22131eac4017ef867aef2ebb2f346f884731c4ea8343e9062392eabd5":
        fail(f"{issue} pipeline contract drift")
    if contract.get("quality_contract_sha256") != "b5b955d524fb438c0f1b2c9490bea1da2083e79028d67a55ca424bbfc20f2958":
        fail(f"{issue} quality contract drift")

def verify_source771():
    m = json.loads(MANIFEST.read_text())
    files = m["files"]
    if len(files) != 771:
        fail(f"manifest 771 expected, got {len(files)}")
    ok = 0
    mismatch = []
    missing = []
    for rel, meta in files.items():
        p = REPO_ROOT / rel
        if not p.is_file() or p.is_symlink():
            missing.append(rel)
            continue
        actual = sha256_file(p)
        if actual == meta["sha256"] and p.stat().st_size == meta["bytes"]:
            ok += 1
        else:
            mismatch.append(rel)
    # expected: 770 ok, 1 mismatch is tests/test_evidence_scaling_v2.py with d486...
    if not (ok == 770 and len(mismatch)==1 and mismatch[0]=="tests/test_evidence_scaling_v2.py" and len(missing)==0):
        fail(f"source771 unexpected ok={ok} mismatch={mismatch} missing={missing[:5]}")
    # verify mismatch is known d486
    tp = REPO_ROOT / "tests/test_evidence_scaling_v2.py"
    if sha256_file(tp) != "d486809c4ae88c0e78784ade8e456cd9227b25a29c12cde9700664a1eec3edad":
        fail("test file not expected d486 pre")
    return {"ok": ok, "mismatch": mismatch, "missing": missing}

def preserve_pre(issue: str, pre_dir: Path):
    exp = EXPECTED[issue]
    # copy State/Profile + checkpoints + four artifacts + inventory
    to_copy = [
        exp["state_rel"],
        f"sources/{issue}/production-profile.json",
        f"sources/{issue}/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json",
        f"sources/{issue}/orchestration/v2/checkpoints/DISCOVERY_COLLECTED.json",
        exp["ev_rel"], exp["views_rel"], exp["ledger_rel"], exp["comp_rel"],
    ]
    if pre_dir.exists():
        # idempotent reuse after harness-fix retry: verify existing matches current
        try:
            existing = json.loads((pre_dir / "pre-inventory.json").read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"pre dir exists but inventory unreadable {pre_dir}: {exc}")
        if existing.get("issue") != issue:
            fail(f"pre dir issue mismatch")
        for rel in to_copy:
            dst = pre_dir / rel.replace("/","__")
            if not dst.is_file() or dst.is_symlink():
                fail(f"pre existing missing {rel}")
            if sha256_file(dst) != sha256_file(REPO_ROOT / rel):
                fail(f"pre existing drift vs current {rel} (no overwrite)")
        inv = existing.get("files", {})
        return inv
    pre_dir.mkdir(parents=True, exist_ok=False)
    inv = {}
    for rel in to_copy:
        src = REPO_ROOT / rel
        dst = pre_dir / Path(rel).name.replace("/","_") if False else pre_dir / f"{Path(rel).name}"
        # use distinct names to avoid collision (evidence-accepted.json appears twice across issues? No, per issue dir separate, but within issue evidence vs views have distinct filenames? evidence-accepted.json vs edition-views-accepted.json distinct, ok)
        # for checkpoint files, names distinct, ok
        # for State/Profile distinct, ok
        # To avoid collision, prefix with subdir
        dst = pre_dir / rel.replace("/","__")
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() or dst.is_symlink():
            fail(f"pre dest must be absent {dst}")
        shutil.copyfile(src, dst)
        inv[rel] = {"bytes": dst.stat().st_size, "sha256": sha256_file(dst)}
        # verify copy
        if sha256_file(dst) != sha256_file(src):
            fail(f"pre copy verify failed {rel}")
    (pre_dir / "pre-inventory.json").write_text(json.dumps({"issue": issue, "files": inv}, indent=2)+"\n", encoding="utf-8")
    return inv

def copy_reviews_exact(issue: str):
    exp = EXPECTED[issue]
    dest_dir = REPO_ROOT / f"sources/{issue}/execution/reviews"
    dest_dir.mkdir(parents=True, exist_ok=True)
    # exclusive names
    if issue == "2026-W34":
        md_name = "w34-resume-output-review-20261105.md"
        js_name = "w34-resume-output-decision-map-20261105.json"
    else:
        md_name = "sp-evidence-final-rereview-20261105T011000Z.md"
        js_name = "sp-evidence-final-rereview-20261105T011000Z-machine.json"
    md_dst = dest_dir / md_name
    js_dst = dest_dir / js_name
    # idempotent reuse after harness-fix retry: if exists, verify exact bytes, else copy exact
    if md_dst.exists() or md_dst.is_symlink() or js_dst.exists() or js_dst.is_symlink():
        if not (md_dst.is_file() and not md_dst.is_symlink() and js_dst.is_file() and not js_dst.is_symlink()):
            fail(f"edition-local review dest unsafe/partial (no overwrite) {dest_dir}")
        if sha256_file(md_dst) != exp["review_md_sha"] or sha256_file(js_dst) != exp["review_json_sha"]:
            fail(f"edition-local review dest exists with divergent bytes (no overwrite) {dest_dir}")
        # reuse verified copies
    else:
        shutil.copyfile(exp["review_md_src"], md_dst)
        shutil.copyfile(exp["review_json_src"], js_dst)
        if sha256_file(md_dst) != exp["review_md_sha"]:
            fail("md copy sha mismatch")
        if sha256_file(js_dst) != exp["review_json_sha"]:
            fail("json copy sha mismatch")
    # return repo-relative posix for evidence strings
    md_rel = f"sources/{issue}/execution/reviews/{md_name}"
    js_rel = f"sources/{issue}/execution/reviews/{js_name}"
    return md_rel, js_rel, md_dst, js_dst

def run_cli(cmd, cwd, env):
    proc = subprocess.run(cmd, cwd=str(cwd), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue", required=True, choices=list(EXPECTED.keys()))
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    issue = args.issue
    run_dir = Path(args.run_dir)
    if run_dir.resolve() != RUN_DIR.resolve():
        fail(f"run-dir must be {RUN_DIR}")
    check_env()
    exp = EXPECTED[issue]
    # raw dir
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    # verify pre + source771
    verify_pre(issue)
    s771_pre = verify_source771()
    pre_dir = run_dir / f"pre-{issue}"
    pre_inv = preserve_pre(issue, pre_dir)
    # copy reviews exact (active write 1-2)
    md_rel, js_rel, md_dst, js_dst = copy_reviews_exact(issue)
    # prepare validate CLI (idempotent reuse after harness-fix retry)
    report_rel = f"sources/{issue}/orchestration/v2/stage-validation/CANDIDATES_NORMALIZED-report.json"
    report_abs = REPO_ROOT / report_rel
    arts = [f"evidence-acceptance={exp['ev_rel']}", f"edition-views-acceptance={exp['views_rel']}", f"materiality-ledger={exp['ledger_rel']}", f"profile-completeness={exp['comp_rel']}"]
    base_env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    base_env["PYTHONDONTWRITEBYTECODE"] = "1"
    base_env["PYTHONPATH"] = str(REPO_ROOT)
    # ensure HOME unchanged already checked; keep as is
    def _report_valid_existing():
        try:
            doc = json.loads(report_abs.read_text(encoding="utf-8"))
        except Exception:
            return False
        if not (doc.get("check_id")=="CORE_STAGE_CONTRACT" and doc.get("status")=="PASS" and doc.get("from_state")=="CANDIDATES_NORMALIZED" and doc.get("to_state")=="EVIDENCE_REVIEWED" and doc.get("issue_id")==issue):
            return False
        if doc.get("production_state",{}).get("sha256") != exp["state_sha"]:
            return False
        arts_doc = {r.get("name"): r.get("sha256") for r in doc.get("artifacts",[]) if isinstance(r, dict)}
        if not (arts_doc.get("evidence-acceptance")==exp["ev_sha"] and arts_doc.get("edition-views-acceptance")==exp["views_sha"] and arts_doc.get("materiality-ledger")==exp["ledger_sha"] and arts_doc.get("profile-completeness")==exp["comp_sha"]):
            return False
        if doc.get("implementation_commit_sha") != "e84a82aca000c990597ea8cf60f548e2ff187bd1":
            return False
        return True
    if report_abs.exists() and not report_abs.is_symlink() and _report_valid_existing():
        report_sha = sha256_file(report_abs)
        report_bytes = report_abs.stat().st_size
        report_doc = json.loads(report_abs.read_text(encoding="utf-8"))
    else:
        if report_abs.exists() or report_abs.is_symlink():
            fail("report exists with divergent bytes (no overwrite)")
        now1 = datetime.now(timezone.utc)
        now1_iso = now1.isoformat().replace("+00:00","Z")
        validate_cmd = [sys.executable, "scripts/survey_stage_validation_v2.py", "--repo-root", ".", "--config", "config/survey-production-v2.json", "--state", exp["state_rel"]] + sum([["--artifact", a] for a in arts], []) + ["--output", report_rel, "--recorded-at", now1_iso]
        # cwd = REPO_ROOT
        vproc = run_cli(validate_cmd, REPO_ROOT, base_env)
        (raw_dir / f"{issue}-validate-stdout.txt").write_text(vproc.stdout, encoding="utf-8")
        (raw_dir / f"{issue}-validate-stderr.txt").write_text(vproc.stderr, encoding="utf-8")
        (raw_dir / f"{issue}-validate-argv.json").write_text(json.dumps({"argv": validate_cmd, "cwd": str(REPO_ROOT), "utc": now1_iso, "pid": os.getpid(), "exit": vproc.returncode}, indent=2)+"\n", encoding="utf-8")
        if vproc.returncode != 0:
            # preserve partials, stop this edition
            out = {"issue": issue, "phase": "validate_stage", "exit": vproc.returncode, "stdout": vproc.stdout[-2000:], "stderr": vproc.stderr[-2000:], "pre771": s771_pre}
            (run_dir / f"{issue}-failure.json").write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
            print(json.dumps(out, indent=2))
            return 2
        if not report_abs.is_file() or report_abs.is_symlink():
            fail("report not created")
        report_sha = sha256_file(report_abs)
        report_bytes = report_abs.stat().st_size
        report_doc = json.loads(report_abs.read_text(encoding="utf-8"))
        if report_doc.get("check_id") != "CORE_STAGE_CONTRACT" or report_doc.get("status") != "PASS" or report_doc.get("from_state") != "CANDIDATES_NORMALIZED" or report_doc.get("to_state") != "EVIDENCE_REVIEWED":
            fail("report identity unexpected")
    # create reviews JSON (active write, idempotent reuse)
    reviews_rel = f"sources/{issue}/orchestration/v2/stage-reviews/CANDIDATES_NORMALIZED-reviews.json"
    reviews_abs = REPO_ROOT / reviews_rel
    det_evidence = f"validate_stage PASS report {report_rel} sha256 {report_sha} on exact current bytes; independent Evidence {exp['review_label']}"
    agent_evidence = f"Independent Evidence BOUNDED_PROCEED for {issue}; {exp['review_label']}; review file {md_rel} sha256 {exp['review_md_sha']} + machine {js_rel} sha256 {exp['review_json_sha']}; packet {exp['review_md_src'].relative_to(RECON_ROOT)} + machine {exp['review_json_src'].relative_to(RECON_ROOT)}; bound artifacts evidence {exp['ev_sha']}/{exp['ev_bytes']} views {exp['views_sha']}/{exp['views_bytes']} ledger {exp['ledger_sha']}/{exp['ledger_bytes']} completeness {exp['comp_sha']}/{exp['comp_bytes']}; executor {exp['executor']} (not Sol/Astra/Human); no Gate decided, no full-corpus semantic/publication PASS"
    reviews_doc = {"reviews": [
        {"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "executor": "General isolated-rehearsal deterministic stage validation (author, not independent reviewer)", "evidence": det_evidence, "result_path": report_rel},
        {"check_id": "EVIDENCE_SUPERVISORY_REVIEW", "kind": "AGENT_RESEARCH", "executor": exp["executor"], "evidence": agent_evidence},
    ]}
    if reviews_abs.exists() and not reviews_abs.is_symlink():
        try:
            existing_rv = json.loads(reviews_abs.read_text(encoding="utf-8"))
        except Exception:
            fail("reviews input exists unreadable (no overwrite)")
        # verify same check_ids/kinds/executors/result_path/report sha bound
        rows = existing_rv.get("reviews", [])
        if not (isinstance(rows, list) and len(rows)==2):
            fail("reviews input exists divergent (no overwrite)")
        r0 = rows[0] if isinstance(rows[0], dict) else {}
        r1 = rows[1] if isinstance(rows[1], dict) else {}
        if not (r0.get("check_id")=="CORE_STAGE_CONTRACT" and r0.get("kind")=="DETERMINISTIC" and r0.get("result_path")==report_rel and r1.get("check_id")=="EVIDENCE_SUPERVISORY_REVIEW" and r1.get("kind")=="AGENT_RESEARCH" and r1.get("executor")==exp["executor"]):
            fail("reviews input exists divergent (no overwrite)")
        # verify det evidence binds current report sha
        if report_sha not in (r0.get("evidence","")):
            fail("reviews input det evidence does not bind current report sha (no overwrite)")
        # reuse verified
    else:
        if reviews_abs.exists() or reviews_abs.is_symlink():
            fail("reviews input must be absent pre")
        reviews_abs.write_text(json.dumps(reviews_doc, indent=2)+"\n", encoding="utf-8")
    # advance-stage (build+advance)
    now2 = datetime.now(timezone.utc)
    now2_iso = now2.isoformat().replace("+00:00","Z")
    summary = f"Evidence authority-consumption BOUNDED_PROCEED for {issue}; advancing CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED via normal checkpoint (4 artifacts + deterministic report + independent review)."
    adv_cmd = [sys.executable, "scripts/survey_agent_control_v2.py", "--repo-root", ".", "--config", "config/survey-production-v2.json", "advance-stage", "--state", exp["state_rel"]] + sum([["--artifact", a] for a in arts], []) + ["--reviews", reviews_rel, "--summary", summary, "--recorded-at", now2_iso]
    aproc = run_cli(adv_cmd, REPO_ROOT, base_env)
    (raw_dir / f"{issue}-advance-stdout.txt").write_text(aproc.stdout, encoding="utf-8")
    (raw_dir / f"{issue}-advance-stderr.txt").write_text(aproc.stderr, encoding="utf-8")
    (raw_dir / f"{issue}-advance-argv.json").write_text(json.dumps({"argv": adv_cmd, "cwd": str(REPO_ROOT), "utc": now2_iso, "pid": os.getpid(), "exit": aproc.returncode}, indent=2)+"\n", encoding="utf-8")
    if aproc.returncode != 0:
        out = {"issue": issue, "phase": "advance-stage", "exit": aproc.returncode, "stdout": aproc.stdout[-2000:], "stderr": aproc.stderr[-2000:], "report": {"path": report_rel, "sha256": report_sha, "bytes": report_bytes}}
        (run_dir / f"{issue}-failure.json").write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(out, indent=2))
        return 3
    # post-verify
    # State must be EVIDENCE_REVIEWED
    st_post = json.loads((REPO_ROOT / exp["state_rel"]).read_text(encoding="utf-8"))
    if st_post.get("lifecycle_state") != "EVIDENCE_REVIEWED":
        fail(f"post State not EVIDENCE_REVIEWED: {st_post.get('lifecycle_state')}")
    # checkpoints evidence trio passed + provenance points to new CAND checkpoint
    mc = st_post.get("machine_checkpoints", {})
    if not (mc.get("evidence")=="passed" and mc.get("materiality")=="passed" and mc.get("completeness")=="passed"):
        fail(f"post checkpoints not passed {mc}")
    prov = st_post.get("checkpoint_provenance", {})
    cand_rel = f"sources/{issue}/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json"
    for k in ["evidence","materiality","completeness"]:
        r = prov.get(k)
        if not isinstance(r, dict) or r.get("path") != cand_rel:
            fail(f"post provenance {k} must point to {cand_rel}, got {r}")
        if r.get("sha256") != sha256_file(REPO_ROOT / cand_rel):
            fail(f"post provenance {k} sha drift")
    if st_post.get("human_gates") != {"architecture_review":"pending","publication_preview":"pending"}:
        fail("post human gates changed")
    # checkpoint file exists and binds 4 artifacts + 2 reviews
    cp = json.loads((REPO_ROOT / cand_rel).read_text(encoding="utf-8"))
    if cp.get("from_state")!="CANDIDATES_NORMALIZED" or cp.get("to_state")!="EVIDENCE_REVIEWED":
        fail("checkpoint lifecycle mismatch")
    # ledger/completeness unchanged
    for rel_key, sha_key in [( "ledger_rel","ledger_sha"),("comp_rel","comp_sha")]:
        if sha256_file(REPO_ROOT / exp[rel_key]) != exp[sha_key]:
            fail(f"post {rel_key} changed (must preserve)")
    # source771 still 770+test-diff
    s771_post = verify_source771()
    result = {
        "issue": issue,
        "lifecycle_state": st_post.get("lifecycle_state"),
        "checkpoint": {"path": cand_rel, "sha256": sha256_file(REPO_ROOT / cand_rel), "bytes": (REPO_ROOT / cand_rel).stat().st_size},
        "report": {"path": report_rel, "sha256": report_sha, "bytes": report_bytes},
        "reviews_input": {"path": reviews_rel, "sha256": sha256_file(REPO_ROOT / reviews_rel), "bytes": (REPO_ROOT / reviews_rel).stat().st_size},
        "edition_reviews": [{"path": md_rel, "sha256": sha256_file(REPO_ROOT / md_rel)}, {"path": js_rel, "sha256": sha256_file(REPO_ROOT / js_rel)}],
        "state": {"path": exp["state_rel"], "sha256": sha256_file(REPO_ROOT / exp["state_rel"]), "bytes": (REPO_ROOT / exp["state_rel"]).stat().st_size},
        "pre771": s771_pre, "post771": s771_post,
        "history_last": st_post.get("history", [])[-1],
    }
    (run_dir / f"{issue}-success.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
