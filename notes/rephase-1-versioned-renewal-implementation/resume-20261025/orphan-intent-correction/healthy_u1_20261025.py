#!/usr/bin/env python3
"""NEW healthy SEALED_U (or1-weekly) via public prepare/finalize, fixed code.

Real existing PDF/reviews reuse from wk-boot-1. No activation. No validator
mocks. Fresh Python child, fixture-first sys.path, no inherited GIT_*.

Usage: python3 healthy_u1_20261025.py FIXTURE_ROOT RENEWAL_ID NOW_ISO OUT_JSON
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} FIXTURE_ROOT RENEWAL_ID NOW_ISO OUT_JSON", flush=True)
        return 2
    ROOT = Path(sys.argv[1]).resolve()
    RID = sys.argv[2].strip()
    NOW_ISO = sys.argv[3].strip()
    OUT = Path(sys.argv[4]).resolve()
    for v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            return 2
    sys.path.insert(0, str(ROOT))
    sys.dont_write_bytecode = True
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    from scripts import survey_production_v2 as core
    from scripts import survey_quality_v2 as quality
    from scripts import survey_versioned_renewal_v2 as high
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT), capture_output=True, text=True, timeout=30, env=env).stdout.strip()
    print(f"HEAD={head}", flush=True)
    state_rel = "sources/2026-W37/production-state.json"
    mspec_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json"
    prep = high.prepare_renewal(str(ROOT), state_rel, RID, "REUSE_TARGETS", mspec_rel, None, "orphanfix-fixture", NOW_ISO)
    print(f"PREPARE_OK basis={prep.get('basis_path')}", flush=True)
    basis_rel = prep["basis_path"]
    basis = json.loads((ROOT / basis_rel).read_bytes())
    r_dir = f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/{RID}"
    pdir = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1"
    cfg = json.loads((ROOT / "config/survey-production-v2.json").read_bytes())
    kinds = quality.expected_checks_by_kind(cfg, basis["research_profile"], basis["publication_profile"], {"DETERMINISTIC"})
    prior_seal = json.loads((ROOT / basis["prior_selected_ref"]["path"]).read_bytes())
    roles = prior_seal["roles"]
    trio_primary = roles["validated-source"]
    pdf_role = roles["publication-pdf"]
    main_bytes = (ROOT / trio_primary["path"]).read_bytes()
    pdf_bytes = (ROOT / pdf_role["path"]).read_bytes()
    try:
        from pypdf import PdfReader
        pages = len(PdfReader(str(ROOT / pdf_role["path"])).pages)
    except Exception as exc:
        print(f"QA PDF unreadable: {exc}", flush=True)
        return 2
    qroot = ROOT / r_dir / "quality"
    qroot.mkdir(parents=True, exist_ok=True)
    scope = f"renewal {RID} fresh U re-assertion (orphanfix healthy base)"
    payloads = {
        "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS", "trio_sha256": core.sha256_bytes(main_bytes), "trio_path": trio_primary["path"], "scope": scope},
        "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS", "source_sha256": core.sha256_bytes(main_bytes), "inspected_identifiers": [basis["issue_id"]], "scope": scope},
        "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages, "pdf_sha256": core.sha256_bytes(pdf_bytes), "byte_count": len(pdf_bytes), "scope": scope},
    }
    if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
        payloads["EMPTY_WRAPPER_SUPPRESSION"] = {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS", "inspected_paths": [trio_primary["path"]], "scope": scope}
    if set(payloads) != set(kinds):
        print(f"QA kinds mismatch {sorted(payloads)} vs {sorted(kinds)}", flush=True)
        return 2
    rows = []
    for cid in sorted(payloads):
        p = qroot / f"{cid.lower()}.json"
        p.write_bytes(core.json_bytes(payloads[cid]))
        rows.append({"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": "orphanfix-fixture", "evidence": "Renewal fresh deterministic re-assertion: exact current bytes inspected.", "recorded_at": NOW_ISO, "result": {"path": str(p.relative_to(ROOT)), "sha256": core.sha256_file(p)}})
    checks_path = ROOT / pdir / f"renewal-qa-checks-{RID}.json"
    checks_path.write_bytes(core.json_bytes({"checks": rows}))
    print(f"QA_OK checks={checks_path.relative_to(ROOT)}", flush=True)
    fin = high.finalize_renewal(str(ROOT), state_rel, basis_rel, str(checks_path.relative_to(ROOT)), None, None, "orphanfix-fixture", NOW_ISO)
    print(f"FINALIZE_OK set={fin.get('set_path')} disp={fin.get('disposition')}", flush=True)
    v = high.validate_prepared_renewal_set(str(ROOT), state_rel, fin["set_path"])
    print(f"VALIDATE_SET_OK {v.get('SET_VALID')}", flush=True)
    OUT.write_text(json.dumps({"basis_path": basis_rel, "set_path": fin["set_path"], "proof_path": fin["proof_path"], "receipt_path": fin["receipt_path"], "checks_path": str(checks_path.relative_to(ROOT)), "head": head, "state_sha": core.sha256_file(ROOT / state_rel)}, indent=1), encoding="utf-8")
    print("HEALTHY_OR1_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
