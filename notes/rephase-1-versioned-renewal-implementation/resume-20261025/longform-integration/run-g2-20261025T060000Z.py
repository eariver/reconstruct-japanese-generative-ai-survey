#!/usr/bin/env python3
"""LONGFORM G2 — style+Core comment epoch + U-fail (expected) + C1 success.
- G2 commit: style comment + HIGH comment (schema/semantic unchanged)
- U-fail: high-ufail-longform REUSE should REFUSE REUSE_TARGET_MISMATCH (style diff), preserve inert
- C1: high-c1-longform RENDER with real TL build + postrender reviews, then finalize/activate/history
"""
import subprocess, sys, json, os, hashlib, pathlib, shutil
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-g2-20261025T060000Z"
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
U_QA = open(REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-u1-20261025T060000Z.py").read().split('U_QA = r"""')[1].split('"""')[0] if False else None
# Re-define U_QA and C_QA builders (small helpers, fixture-first)
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
scope = f"renewal {rid} fresh U re-assertion LONGFORM G2 (exact current bytes)"
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
                 "evidence": "LONGFORM G2 fresh U re-assertion.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
print(str(checks_path.relative_to(root_p)))
"""
C_QA_BUILDER = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, issue, prop, rid, now_iso, executor = sys.argv[1:7]
from pathlib import Path
root_p = Path(root)
sys.path.insert(0, str(root_p))
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader_pub
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture import origin"
import os
print(f"C_QA child PID={os.getpid()}", flush=True)
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
basis = json.loads((root_p / f"{r_dir}/renewal-basis.json").read_bytes())
proof = json.loads((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes())
proof_ref = {"path": f"{r_dir}/renewal-source-proof.json",
             "sha256": __import__("hashlib").sha256((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes()).hexdigest()}
man_rel = f"{r_dir}/reader-manuscript-v2.json"
trio = proof["output_trio_refs"]
from pypdf import PdfReader
brec = json.loads((root_p / f"{r_dir}/build-record.json").read_bytes())
pdf_rel = brec["outputs"]["publication-pdf"]["path"]
pages = len(PdfReader(str(root_p / pdf_rel)).pages)
rev_dir = root_p / r_dir / "reviews"
rev_dir.mkdir(parents=True, exist_ok=True)
out = {}
man_doc = json.loads((root_p / man_rel).read_bytes())
if basis["research_profile"] == "THEMATIC":
    from scripts import survey_reader_fidelity_v2 as _fid
    try:
        _cov, _fin = _fid._locations_from_manifest(man_doc)
        _cov_locs, _fin_locs = sorted(_cov), sorted(_fin)
    except Exception:
        _cov_locs = sorted({r["reader_locations"][0] for r in man_doc.get("architecture_coverage", []) if r.get("reader_locations")})
        _fin_locs = [man_doc.get("architecture_coverage", [{}])[0].get("reader_locations", ["main.tex:summary"])[0] if man_doc.get("architecture_coverage") else "main.tex:summary"]
    _arch = json.loads((root_p / man_doc["architecture"]["path"]).read_bytes())
    _pids = [r["package_id"] for r in _arch.get("packages", [])]
    _fin_pkg = max(_arch.get("packages", [{"package_id": "pkg-001", "drafting_order": 0}]), key=lambda r: r.get("drafting_order", 0))["package_id"]
    _pp = (_arch.get("page_plan") or {}).get("target_pages", 12)
    try:
        _tgt = int(float(_pp)) if float(_pp).is_integer() else str(_pp)
    except Exception:
        _tgt = 12
    def _ev(cid):
        ev = [f"renewal-c1:{rid}:main.pdf"]
        if cid in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
            ev = sorted({f"package:{pid}" for pid in _pids} | set(_cov_locs))
            if cid == "LONGFORM_TECHNICAL_DEPTH":
                ev = sorted(set(ev) | {f"page-plan:{pages}/{_tgt}", "density-review:below-target-substantive"})
        elif cid == "FINAL_SYNTHESIS_QUALITY":
            ev = sorted(set(_fin_locs) | {"reader-role:final-synthesis", f"package:{_fin_pkg}"})
        elif cid == "LONGFORM_MIXED_LAYOUT":
            ev = ["reader-layout:wide-surfaces-full-width", "reader-layout:references-one-column",
                  "reader-layout:balanced-two-column-narrative"]
        return ev
else:
    def _ev(cid):
        return [f"renewal-c1:{rid}:{trio['primary']['path']}"]
for kind_name, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"),
                         ("VISUAL", "visual-review-v2.json")):
    checks = [{"check_id": cid, "status": "PASS",
               "detail": f"Renewal C1 fixture synthetic {kind_name} reviewer on new R targets; no genuine approval.",
               "evidence_locations": _ev(cid)}
              for cid in sorted(reader_pub._expected_review_checks(root_p, core.load_json(root_p / basis["profile_ref"]["path"]), kind_name))]
    reader_pub.build_review_record(
        root_p, root_p / man_rel, root_p / pdf_rel, pages, kind_name, checks,
        f"renewal-c1-fixture synthetic {kind_name} reviewer; no genuine approval",
        __import__("datetime").datetime.fromisoformat(now_iso), rev_dir / fname,
        renewal_source_proof_ref=dict(proof_ref))
    out[kind_name] = str((rev_dir / fname).relative_to(root_p))
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
qroot = root_p / r_dir / "quality"
qroot.mkdir(parents=True, exist_ok=True)
scope = f"renewal {rid} fresh C deterministic re-assertion on new R targets LONGFORM G2"
main_bytes = (root_p / trio["primary"]["path"]).read_bytes()
pdf_bytes = (root_p / pdf_rel).read_bytes()
payloads = {
    "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
        "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio["primary"]["path"], "scope": scope},
    "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(main_bytes),
        "inspected_identifiers": [issue] + (["Target Model"] if basis["research_profile"] == "THEMATIC" else []),
        "scope": scope},
    "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
        "pdf_sha256": core.sha256_bytes(pdf_bytes), "byte_count": len(pdf_bytes), "scope": scope},
}
if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
    payloads["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
        "inspected_paths": [trio["primary"]["path"]], "scope": scope}
assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
rows = []
for cid in sorted(payloads):
    p = qroot / f"{cid.lower()}.json"
    p.write_bytes(core.json_bytes(payloads[cid]))
    rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": executor,
                 "evidence": "Renewal C1 fresh deterministic re-assertion: exact new R bytes inspected.",
                 "recorded_at": now_iso,
                 "result": {"path": str(p.relative_to(root_p)), "sha256": core.sha256_file(p)}})
checks_path = root_p / pdir / f"renewal-qa-checks-{rid}.json"
checks_path.write_bytes(core.json_bytes({"checks": rows}))
out["checks"] = str(checks_path.relative_to(root_p))
print(json.dumps(out, indent=1))
"""
def main():
    (EVID/"commands.log").write_text(f"LONGFORM G2 start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    # verify pre-G2 HEAD is U1's G1 (381c...)
    run_tag("g2-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    run_tag("g2-pre-log", ["git","-C",str(FIX),"log","--oneline","-3"])
    # check old E still untracked, no E rewrite yet
    run_tag("g2-pre-status", ["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"])
    # Make G2 style+Core comment changes (comment only, schema/semantic unchanged)
    style_path = FIX/"templates/survey/jgaisurvey.sty"
    high_path = FIX/"scripts/survey_versioned_renewal_v2.py"
    style_text = style_path.read_text(encoding="utf-8")
    assert "% G2 LONGFORM" not in style_text, "G2 style already applied"
    style_path.write_text(style_text + "\n% G2 LONGFORM eligible style comment — schema/semantic unchanged (comment only)\n", encoding="utf-8")
    high_text = high_path.read_text(encoding="utf-8")
    assert "# G2 LONGFORM" not in high_text
    # insert after first line
    lines = high_text.splitlines(True)
    lines.insert(1, "# G2 LONGFORM eligible Core comment — schema/semantic unchanged (comment only)\n")
    high_path.write_text("".join(lines), encoding="utf-8")
    print("G2 edits applied", flush=True)
    # verify SHAs changed but only comments
    run_tag("g2-style-sha", [sys.executable,"-c","import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())", str(style_path)])
    run_tag("g2-high-sha", [sys.executable,"-c","import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())", str(high_path)])
    run_tag("g2-status", ["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"])
    # SOURCE-only add: only those two M files
    run_tag("g2-add", ["git","-C",str(FIX),"add","--","templates/survey/jgaisurvey.sty","scripts/survey_versioned_renewal_v2.py"])
    run_tag("g2-diff-cached", ["git","-C",str(FIX),"diff","--cached","--name-only"])
    run_tag("g2-head-pre", ["git","-C",str(FIX),"rev-parse","HEAD"])
    c = run_tag("g2-commit", ["git","-C",str(FIX),"commit","-m","LONGFORM TEST-ONLY: G2 eligible style+Core comment (schema/semantic unchanged)","--no-verify"])
    assert c.returncode==0, "G2 commit failed"
    run_tag("g2-head-post", ["git","-C",str(FIX),"rev-parse","HEAD"])
    run_tag("g2-log-post", ["git","-C",str(FIX),"log","--oneline","-4"])
    # Verify OLD history styleT? Old history rows at 721+G1 still valid? The new style is at new epoch, old E not rewritten (check E still ??)
    run_tag("g2-status-post", ["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"])
    # Now U-fail: high-ufail-longform REUSE should REFUSE REUSE_TARGET_MISMATCH
    issue="SP001"; prop="lf-boot-1"; rid_fail="high-ufail-longform"
    state=f"sources/{issue}/production-state.json"
    pdir=f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
    now_fail=datetime.now(timezone.utc).isoformat()
    open(EVID/"now-iso-ufail.txt","w").write(now_fail+"\n")
    print(f"now_fail={now_fail}", flush=True)
    # ensure now_fail >= prior r2 recorded_at
    py_inline(r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
r2=json.load(open(root/"sources/SP001/publication/v2/publication-surface-revalidation-r2.json"))
print(f"r2 recorded_at={r2['recorded_at']} now_fail={sys.argv[2]}")
assert sys.argv[2] >= r2['recorded_at']
print("CHRONO_OK r2<=now_fail")
""", [str(FIX), now_fail], "chrono-r2-ufail")
    pf = cli(str(FIX), ["prepare","--root",str(FIX),"--state",state,"--renewal-id",rid_fail,"--intent","REUSE_TARGETS","--manuscript-spec",f"{pdir}/manuscript-spec.json","--executor","longform-g2-ufail","--recorded-at",now_fail], "ufail-prepare")
    print(f"ufail prepare exit={pf.returncode} (expected 0, failure comes at finalize)", flush=True)
    # If prepare succeeds, QA then finalize should refuse
    if pf.returncode==0:
        basis_rel=f"{pdir}/renewals/{rid_fail}/renewal-basis.json"
        r_dir=f"{pdir}/renewals/{rid_fail}"
        qf = py_inline(U_QA_BUILDER, [str(FIX), basis_rel, r_dir, pdir, now_fail, "longform-g2-ufail"], "ufail-qa")
        print(f"ufail qa exit={qf.returncode}", flush=True)
        if qf.returncode==0:
            checks_rel=open(EVID/"ufail-qa-stdout.txt").read().strip().splitlines()[-1].strip()
            ff = cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",checks_rel,"--executor","longform-g2-ufail","--recorded-at",now_fail], "ufail-finalize")
            print(f"ufail finalize exit={ff.returncode} (expected 2 REUSE_TARGET_MISMATCH)", flush=True)
            assert ff.returncode==2, f"U-fail should refuse 2, got {ff.returncode} stdout={open(EVID/'ufail-finalize-stdout.txt').read()[:2000]} stderr={open(EVID/'ufail-finalize-stderr.txt').read()[:3000]}"
            assert "REUSE_TARGET_MISMATCH" in open(EVID/"ufail-finalize-stderr.txt").read() or "REUSE_TARGET_MISMATCH" in open(EVID/"ufail-finalize-stdout.txt").read(), "expected REUSE_TARGET_MISMATCH"
            print("U-FAIL REFUSAL CONFIRMED, inert preserved", flush=True)
            # verify inert: no publication-set? finalize refused before seal, so no set; check dir exists but no set
            run_tag("ufail-inert-ls", ["ls", str(FIX/pdir/f"renewals/{rid_fail}")])
        else:
            print("ufail QA failed (also acceptable as U refusal, but need to check)", flush=True)
    else:
        print("ufail prepare refused (also U refusal, check code)", flush=True)
        assert pf.returncode==2
    # Preserve failed U inert: do NOT cleanup, do NOT reuse same ID for C
    # Now C1: high-c1-longform RENDER with real TL build
    rid="high-c1-longform"
    now_c=datetime.now(timezone.utc).isoformat()
    # ensure monotonic: now_c >= now_fail
    assert now_c >= now_fail, f"now_c {now_c} < now_fail {now_fail}"
    open(EVID/"now-iso-c1.txt","w").write(now_c+"\n")
    print(f"now_c={now_c}", flush=True)
    # C prepare needs toolchain-spec (exists in prop dir)
    run_tag("c1-tspec-cat", ["cat", str(FIX/pdir/"toolchain-spec.json")])
    pc = cli(str(FIX), ["prepare","--root",str(FIX),"--state",state,"--renewal-id",rid,"--intent","RENDER_TARGETS","--manuscript-spec",f"{pdir}/manuscript-spec.json","--toolchain-spec",f"{pdir}/toolchain-spec.json","--executor","longform-g2-c1","--recorded-at",now_c], "c1-prepare")
    assert pc.returncode==0, f"c1 prepare failed {open(EVID/'c1-prepare-stderr.txt').read()[:4000]}"
    basis_rel=f"{pdir}/renewals/{rid}/renewal-basis.json"
    pt = cli(str(FIX), ["prepare-targets","--root",str(FIX),"--basis",basis_rel,"--executor","longform-g2-c1","--recorded-at",now_c], "c1-targets")
    assert pt.returncode==0, f"c1 targets failed {open(EVID/'c1-targets-stderr.txt').read()[:5000]}"
    print(open(EVID/"c1-targets-stdout.txt").read()[:3000], flush=True)
    # verify real PDF: check trio + build-record + PDF pages
    py_inline(r"""
import sys, json, pathlib, hashlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); rid=sys.argv[2]
pdir=f"sources/SP001/publication/v2/editorial-corrections/lf-boot-1"
r_dir=f"{pdir}/renewals/{rid}"
proof=json.loads((root/f"{r_dir}/renewal-source-proof.json").read_bytes())
print(f"proof disposition={proof.get('comparison',{}).get('disposition')}")
trio=proof["output_trio_refs"]
for k,v in trio.items():
    data=(root/v["path"]).read_bytes()
    print(k, v["path"], len(data), hashlib.sha256(data).hexdigest()[:12])
    assert hashlib.sha256(data).hexdigest()==v["sha256"]
brec=json.loads((root/f"{r_dir}/build-record.json").read_bytes())
print(f"build_record variant={brec.get('variant') or brec.get('build_variant') or list(brec.keys())[:5]}")
pdf_rel=brec["outputs"]["publication-pdf"]["path"]
from pypdf import PdfReader
pages=len(PdfReader(str(root/pdf_rel)).pages)
print(f"PDF {pdf_rel} pages={pages}")
assert pages>=1
# ensure no fake P3S manifest: check that staged-source is at renewal R path, not old P3S path
assert r_dir in trio["primary"]["path"], f"trio not at new R path {trio['primary']['path']}"
# ensure no companions sidecar: check no extra files in R beyond expected 9? List
import os
files=list((root/r_dir).rglob("*"))
print(f"R files count={len(files)}")
# check build-record has EXECUTED_BUILD (not REUSED)
print(json.dumps({k:brec.get(k) for k in list(brec.keys())[:10]}, indent=1)[:2000])
""", [str(FIX), rid], "c1-verify-targets")
    # C reviews + QA
    qc = py_inline(C_QA_BUILDER, [str(FIX), issue, prop, rid, now_c, "longform-g2-c1"], "c1-reviews-qa")
    assert qc.returncode==0, f"c1 reviews-qa failed {open(EVID/'c1-reviews-qa-stderr.txt').read()[:4000]}"
    outs=json.loads(open(EVID/"c1-reviews-qa-stdout.txt").read())
    print(f"c1 reviews outs={outs}", flush=True)
    # finalize C requires semantic+visual
    fc = cli(str(FIX), ["finalize","--root",str(FIX),"--state",state,"--basis",basis_rel,"--checks",outs["checks"],"--semantic-review",outs["SEMANTIC_EDITORIAL"],"--visual-review",outs["VISUAL"],"--executor","longform-g2-c1","--recorded-at",now_c], "c1-finalize")
    assert fc.returncode==0, f"c1 finalize failed {open(EVID/'c1-finalize-stderr.txt').read()[:5000]}"
    fin=json.loads(open(EVID/"c1-finalize-stdout.txt").read())
    print(f"c1 finalize set={fin['set_path']} disposition={fin['disposition']}", flush=True)
    assert fin["disposition"]=="NEW_TARGETS"
    # activate C
    ac = cli(str(FIX), ["activate","--root",str(FIX),"--state",state,"--set",fin["set_path"],"--reason","Core change: LONGFORM G2 style+Core comment with new rendered targets (real TL build)","--executor","longform-g2-c1","--recorded-at",now_c], "c1-activate")
    assert ac.returncode==0, f"c1 activate failed {open(EVID/'c1-activate-stderr.txt').read()[:4000]}"
    act=json.loads(open(EVID/"c1-activate-stdout.txt").read())
    print(f"c1 activate {act}", flush=True)
    # history
    hc = cli(str(FIX), ["history","--root",str(FIX),"--record",act["record_path"]], "c1-history")
    assert hc.returncode==0
    print(open(EVID/"c1-history-stdout.txt").read()[:4000], flush=True)
    print("G2 C1 DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
