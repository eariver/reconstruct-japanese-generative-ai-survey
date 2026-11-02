"""Build NEW X manifests tied to fresh Profiles (honest archival reuse) + record archived results.

Normal public APIs only: x_intake.build_manifest + record_result + validate_manifest.
NO new Grok request; rendered task is local re-render with explicit rationale.
Old manifests/tasks/raws stay archived in intake (provenance); nothing overwritten there.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core, survey_x_intake_v2 as xintake

INTAKE = Path("notes/rephase-1-operational-rehearsal-20261101")
IMPORTED_NOW = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
print(f"REAL-LOCAL-IMPORT-TIME {IMPORTED_NOW} (current clock; old observed_at values preserved per run)")

cfgspec = [
    ("2026-W34", "intake-20261101T023147Z-p4-20261101T031826Z/DATA.p4x01.x-source-intake-v2.json"),
    ("SP-efficient-llm-2026", "intake-20261101T023147Z-p4-20261101T031826Z/DATA.p4x02.x-source-intake-v2.json"),
]

for issue, rel in cfgspec:
    print(f"===== {issue} =====")
    arch = json.loads((INTAKE / rel).read_bytes())
    assert arch["issue_id"] == issue, "archived manifest issue mismatch"
    assert arch["decision"] == "REQUIRED", "archived decision must be REQUIRED for reuse"
    assert len(arch["runs"]) == 1, "expected single archived run"
    arun = arch["runs"][0]
    ares = arun["result"]
    assert ares and ares["status"] == "SUCCESS", "archived result must be historical SUCCESS"
    old_prof = arch["production_profile"]
    print(f"archived manifest profile ref: {old_prof} (OLD hash, NOT installed; kept archived)")

    prof_path = WORK / f"sources/{issue}/production-profile.json"
    prof = core.load_json(prof_path)
    assert prof["issue_id"] == issue
    print(f"fresh profile contract: {prof['contract']['pipeline_contract_version']} ... (fresh code authority)")

    # Scope check: archived run must cover current target unchanged; SOCIAL = reception lead
    print(f"archived purpose: {arun['purpose'][:120]}")
    print(f"archived time_scope: {arun['time_scope'][:160]}")
    print(f"archived disposition: {ares['discovery_disposition']} ids={ares['discovery_ids']}")

    spec = {
        "decision": "REQUIRED",
        "series_context": arch.get("series_context"),
        "rationale": (
            f"Archival reuse for isolated rehearsal (no new Grok request): same historical edition {issue} "
            f"and window as fixed-ref source; reuses archived run {arun['run_id']} criteria verbatim "
            f"(purpose/questions/coverage/time_scope/filename) from {rel} (old profile {old_prof['sha256'][:12]}... kept archived); "
            f"old external observed_at {ares['observed_at']} preserved; current local import time is real ({IMPORTED_NOW}); "
            f"rendered task is local re-render for stage plumbing, NOT a new external request; "
            f"SOCIAL/X remains reception lead per archived result rationale, not primary truth."
        ),
        "runs": [{
            "run_id": arun["run_id"],
            "purpose": arun["purpose"],
            "research_questions": list(arun["research_questions"]),
            "coverage_focus": list(arun["coverage_focus"]),
            "time_scope": arun["time_scope"],
            "expected_result_filename": arun["expected_result_filename"],
        }],
    }
    cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
    mpath = xintake.build_manifest(WORK, cfg, prof_path, spec)
    print(f"NEW manifest built: {mpath.relative_to(WORK)}")
    newm = core.load_json(mpath)
    assert newm["production_profile"]["sha256"] == core.sha256_file(prof_path), "new manifest must bind NEW profile"
    assert newm["status"] == "AWAITING_GROK" and newm["runs"][0]["result"] is None
    print(f"new manifest binds fresh profile sha {newm['production_profile']['sha256'][:12]}..., status AWAITING_GROK")

    raw_rel = ares["raw"]["path"]
    raw_path = WORK / raw_rel
    assert raw_path.is_file(), f"archived result raw must be staged: {raw_rel}"
    assert core.sha256_file(raw_path) == ares["raw"]["sha256"], "staged raw must equal archived raw sha"
    assert raw_path.stat().st_size == ares["raw"]["byte_count"], "staged raw byte count must match"
    print(f"result raw staged OK: {raw_rel} {ares['raw']['byte_count']}B sha {ares['raw']['sha256'][:12]}...")

    xintake.record_result(
        WORK, cfg, mpath,
        run_id=arun["run_id"],
        raw_path=raw_path,
        drive_file_name=ares["drive_file_name"],
        observed_at=ares["observed_at"],
        imported_at=IMPORTED_NOW,
        result_status=ares["status"],
        discovery_disposition=ares["discovery_disposition"],
        discovery_ids=list(ares["discovery_ids"]),
        rationale=(
            f"Archival re-import (no new external completion): result raw historically {ares['status']} "
            f"({ares['drive_file_name']}, observed {ares['observed_at']}) re-imported from fixed-ref bytes "
            f"(sha {ares['raw']['sha256'][:12]}..., {ares['raw']['byte_count']}B); imported_at is real current local time {IMPORTED_NOW}; "
            f"disposition {ares['discovery_disposition']} {ares['discovery_ids']} preserved; "
            f"X-only claims remain non-technical leads per archived rationale."
        ),
    )
    final = xintake.validate_manifest(WORK, cfg, mpath, require_complete=True)
    assert final["status"] == "COMPLETE"
    print(f"recorded + validated COMPLETE: {mpath.relative_to(WORK)} status={final['status']}")
print("DONE-ALL")
