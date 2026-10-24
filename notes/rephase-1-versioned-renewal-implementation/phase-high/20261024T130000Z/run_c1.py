#!/usr/bin/env python3
"""HIGH-phase C1 driver — genuine C renewals at the same tool epoch T1.

Per route: prepare C (RENDER_TARGETS + real toolchain spec) -> prepare-targets
(proof/trio/manuscript/REAL TL build/receipt) -> C reviews (fresh subprocess,
fixture-first imports, actual builders, synthetic-labelled, real SHAs) + fresh
QA (new outputs) -> finalize C -> activate C (exact basis-ref blocker expected;
recorded, not bypassed) -> H r1 regression check.

No genuine approval implied. Raw outputs/exits/commands/source-pins to the
unique run dir (no overwrite). Old U1 R-dirs stay inert under different ids.
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
# Parent fixtures + evidence dir come from argv (caller runs the U harness
# first with current HIGH, then C1 in those same fixtures under new ids).
# No stale-HIGH reuse: C1 always runs where the U harness just built.
PARENT = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    REPO / ".rephase-1-editorial-runtime/versioned-renewal-high14-20261024T210000Z")
EVID = EVID_BASE / (sys.argv[2] if len(sys.argv) > 2 else "run15-20261024T213000Z")
FIX = {
    "weekly": {"root": str(PARENT / "renewal-weekly"), "issue": "2026-W37", "prop": "wk-boot-1"},
    "longform": {"root": str(PARENT / "renewal-longform"), "issue": "SP001", "prop": "lf-boot-1"},
}

REVIEW_QA_BUILDER = r"""
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
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
basis = json.loads((root_p / f"{r_dir}/renewal-basis.json").read_bytes())
proof = json.loads((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes())
proof_ref = {"path": f"{r_dir}/renewal-source-proof.json",
             "sha256": __import__("hashlib").sha256((root_p / f"{r_dir}/renewal-source-proof.json").read_bytes()).hexdigest()}
man_rel = f"{r_dir}/reader-manuscript-v2.json"
trio = proof["output_trio_refs"]
from pypdf import PdfReader
import subprocess as _sp
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
scope = f"renewal {rid} fresh C deterministic re-assertion on new R targets"
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


def run(cmd: list[str], cwd: Path, tag: str, env: dict) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=900, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}...  # -> exit={proc.returncode}\n")
    return proc


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    if not PARENT.is_dir():
        print("FATAL: parent fixtures missing", file=sys.stderr)
        return 1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    py = sys.executable
    now_iso = datetime.now(timezone.utc).isoformat()
    for kind, fx in FIX.items():
        root, issue, prop = fx["root"], fx["issue"], fx["prop"]
        pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
        state = f"sources/{issue}/production-state.json"
        mspec = f"{pdir}/manuscript-spec.json"
        tspec = f"{pdir}/toolchain-spec.json"
        rid = f"high-c1-{kind}"
        r_dir = f"{pdir}/renewals/{rid}"
        prep = run([py, "-c",
                    "import sys; sys.path.insert(0, sys.argv[1]); "
                    "from scripts import survey_versioned_renewal_v2 as high; "
                    "import json; "
                    f"r = high.prepare_renewal(sys.argv[1], '{state}', '{rid}', "
                    f"'RENDER_TARGETS', '{mspec}', '{tspec}', 'high-phase-fixture', "
                    f"'{now_iso}'); print(json.dumps(r, indent=1))",
                    root], REPO, f"c1-prepare-{kind}", env)
        print(f"c1-prepare-{kind}: exit={prep.returncode}", flush=True)
        if prep.returncode != 0:
            continue
        basis_rel = f"{r_dir}/renewal-basis.json"
        tgt = run([py, "-c",
                   "import sys; sys.path.insert(0, sys.argv[1]); "
                   "from scripts import survey_versioned_renewal_v2 as high; "
                   "import json; "
                   f"r = high.prepare_renewal_targets(sys.argv[1], '{basis_rel}', "
                   f"'high-phase-fixture', '{now_iso}'); print(json.dumps(r, indent=1))",
                   root], REPO, f"c1-targets-{kind}", env)
        print(f"c1-targets-{kind}: exit={tgt.returncode}", flush=True)
        if tgt.returncode != 0:
            continue
        rev = run([py, "-c", REVIEW_QA_BUILDER, root, issue, prop, rid, now_iso,
                   "high-phase-fixture fresh C deterministic re-assertion"],
                  REPO, f"c1-reviews-qa-{kind}", env)
        print(f"c1-reviews-qa-{kind}: exit={rev.returncode}", flush=True)
        if rev.returncode != 0:
            continue
        import json as _json
        outs = _json.loads((EVID / f"c1-reviews-qa-{kind}-stdout.txt").read_text())
        sem_rel = outs["SEMANTIC_EDITORIAL"]
        vis_rel = outs["VISUAL"]
        checks_rel = outs["checks"]
        fin = run([py, "-c",
                   "import sys; sys.path.insert(0, sys.argv[1]); "
                   "from scripts import survey_versioned_renewal_v2 as high; "
                   "import json; "
                   f"r = high.finalize_renewal(sys.argv[1], '{state}', '{basis_rel}', "
                   f"'{checks_rel}', '{sem_rel}', '{vis_rel}', 'high-phase-fixture', "
                   f"'{now_iso}'); print(json.dumps(r, indent=1))",
                   root], REPO, f"c1-finalize-{kind}", env)
        print(f"c1-finalize-{kind}: exit={fin.returncode}", flush=True)
        if fin.returncode != 0:
            continue
        fout = _json.loads((EVID / f"c1-finalize-{kind}-stdout.txt").read_text())
        act = run([py, "-c",
                   "import sys; sys.path.insert(0, sys.argv[1]); "
                   "from scripts import survey_versioned_renewal_v2 as high; "
                   "import json; "
                   f"r = high.activate_renewal(sys.argv[1], '{state}', '{fout['set_path']}', "
                   "'Core change: same-reader renewal with new rendered targets (real TL build)', "
                   f"'high-phase-fixture', '{now_iso}'); print(json.dumps(r, indent=1))",
                   root], REPO, f"c1-activate-{kind}", env)
        print(f"c1-activate-{kind}: exit={act.returncode} (basis-ref blocker expected)", flush=True)
    print("DONE C1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
