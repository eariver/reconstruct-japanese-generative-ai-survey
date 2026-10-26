#!/usr/bin/env python3
"""Healthy NEW U SEALED_INERT with CURRENT product (1dad1ad/H74275d/S2290ddd, no stale 9a).

Public prepare/finalize, real PDF/reviews reuse, short chain, 721 ancestry preserved.
Usage: python3 harness_healthy_current.py FIXTURE_ROOT RENEWAL_ID NOW_ISO OUT_JSON
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

def main()->int:
    if len(sys.argv)!=5:
        print(f"usage: {sys.argv[0]} FIXTURE RENEWAL_ID NOW_ISO OUT_JSON", flush=True)
        return 2
    ROOT=Path(sys.argv[1]).resolve()
    RID=sys.argv[2].strip()
    NOW_ISO=sys.argv[3].strip()
    OUT=Path(sys.argv[4]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True)
            return 2
    sys.path.insert(0, str(ROOT))
    sys.dont_write_bytecode=True
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    from scripts import survey_production_v2 as core
    from scripts import survey_quality_v2 as quality
    from scripts import survey_versioned_renewal_v2 as high
    import subprocess
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    head=subprocess.run(["git","rev-parse","HEAD"],cwd=str(ROOT),capture_output=True,text=True,timeout=30,env=env).stdout.strip()
    print(f"HEAD={head}", flush=True)
    # Verify CURRENT pins (no stale 9a)
    import hashlib
    def _sha(p: Path)->str:
        h=hashlib.sha256()
        with p.open("rb") as f:
            for c in iter(lambda: f.read(1<<20), b""):
                h.update(c)
        return h.hexdigest()
    for rel, expect in (("scripts/survey_versioned_renewal_v2.py","1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb"),
                        ("scripts/survey_versioned_renewal_history_v2.py","74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d"),
                        ("scripts/survey_versioned_renewal_source_v2.py","2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb")):
        got=_sha(ROOT/rel)
        print(f"PIN {rel} {got[:12]} expect {expect[:12]} {'OK' if got==expect else 'MISMATCH (stale?)'}", flush=True)
        if got!=expect:
            return 2
    print("PRODUCT_PIN_CURRENT_OK (no stale 9a/6fe/20f)", flush=True)
    state_rel="sources/2026-W37/production-state.json"
    mspec_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json"
    prep=high.prepare_renewal(str(ROOT),state_rel,RID,"REUSE_TARGETS",mspec_rel,None,"fault-resume-fixture",NOW_ISO)
    print(f"PREPARE_OK {prep.get('basis_path')}", flush=True)
    basis_rel=prep["basis_path"]
    basis=json.loads((ROOT/basis_rel).read_bytes())
    r_dir=f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/{RID}"
    pdir=f"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1"
    cfg=json.loads((ROOT/"config/survey-production-v2.json").read_bytes())
    kinds=quality.expected_checks_by_kind(cfg,basis["research_profile"],basis["publication_profile"],{"DETERMINISTIC"})
    prior_seal=json.loads((ROOT/basis["prior_selected_ref"]["path"]).read_bytes())
    roles=prior_seal["roles"]
    trio_primary=roles["validated-source"]
    pdf_role=roles["publication-pdf"]
    main_bytes=(ROOT/trio_primary["path"]).read_bytes()
    pdf_bytes=(ROOT/pdf_role["path"]).read_bytes()
    try:
        from pypdf import PdfReader
        pages=len(PdfReader(str(ROOT/pdf_role["path"])).pages)
    except Exception as e:
        print(f"QA PDF unreadable: {e}", flush=True)
        return 2
    qroot=ROOT/r_dir/"quality"
    qroot.mkdir(parents=True,exist_ok=True)
    scope=f"renewal {RID} fresh U (CURRENT 1dad1ad, no stale 9a)"
    payloads={
        "SUBJECT_ENTITY_PROPERTY_BINDING":{"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","trio_sha256":core.sha256_bytes(main_bytes),"trio_path":trio_primary["path"],"scope":scope},
        "IDENTIFIER_PRESERVATION":{"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(main_bytes),"inspected_identifiers":[basis["issue_id"]],"scope":scope},
        "PDF_PREFLIGHT":{"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_bytes(pdf_bytes),"byte_count":len(pdf_bytes),"scope":scope},
    }
    if "EMPTY_WRAPPER_SUPPRESSION" in kinds:
        payloads["EMPTY_WRAPPER_SUPPRESSION"]={"check_id":"EMPTY_WRAPPER_SUPPRESSION","status":"PASS","inspected_paths":[trio_primary["path"]],"scope":scope}
    if set(payloads)!=set(kinds):
        print(f"QA kinds mismatch", flush=True)
        return 2
    rows=[]
    for cid in sorted(payloads):
        p=qroot/f"{cid.lower()}.json"
        p.write_bytes(core.json_bytes(payloads[cid]))
        rows.append({"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"fault-resume-fixture","evidence":"CURRENT fresh deterministic re-assertion.","recorded_at":NOW_ISO,"result":{"path":str(p.relative_to(ROOT)),"sha256":core.sha256_file(p)}})
    checks_path=ROOT/pdir/f"renewal-qa-checks-{RID}.json"
    checks_path.write_bytes(core.json_bytes({"checks":rows}))
    print(f"QA_OK {checks_path.relative_to(ROOT)}", flush=True)
    fin=high.finalize_renewal(str(ROOT),state_rel,basis_rel,str(checks_path.relative_to(ROOT)),None,None,"fault-resume-fixture",NOW_ISO)
    print(f"FINALIZE_OK {fin.get('set_path')} {fin.get('disposition')}", flush=True)
    v=high.validate_prepared_renewal_set(str(ROOT),state_rel,fin["set_path"])
    print(f"VALIDATE_OK", flush=True)
    OUT.write_text(json.dumps({"basis_path":basis_rel,"set_path":fin["set_path"],"proof_path":fin["proof_path"],"receipt_path":fin["receipt_path"],"checks_path":str(checks_path.relative_to(ROOT)),"head":head,"state_sha":core.sha256_file(ROOT/state_rel)},indent=1),encoding="utf-8")
    print("HEALTHY_CURRENT_OK", flush=True)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
