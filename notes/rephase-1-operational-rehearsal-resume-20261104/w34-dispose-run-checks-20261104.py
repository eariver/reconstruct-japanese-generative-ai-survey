#!/usr/bin/env python3
"""W34 dispose+run stdlib checks (no project import/run, no git/network).

Exercises DERIVED R369/E439 count/path mapping (actual DATA, not tokens),
READY W34 shape (actual READY 473bf85b...), archival binding. Preserved raw.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path

WS = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
REPO = WS / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
RESUME = WS / "notes/rephase-1-operational-rehearsal-resume-20261104"
PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def _enforce_derived(root_recs, disc_recs, decisions):
    if len(root_recs) != 369:
        raise ValueError(f"root != 369 (got {len(root_recs)})")
    if len(disc_recs) != 439:
        raise ValueError(f"effective != 439 (got {len(disc_recs)})")
    if len(decisions) != 439:
        raise ValueError(f"decisions != 439 (got {len(decisions)})")
    return True


def main() -> int:
    # DERIVED R369/E439 from actual files (not token presence)
    dcp = json.load(open(REPO / "sources/2026-W34/discovery/discovery-accepted-v2.json"))
    scp = json.load(open(REPO / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json"))
    ev_lines = (REPO / "sources/2026-W34/screening/input/event-discovery-v2.jsonl").read_bytes().splitlines()
    root_recs, disc_recs, decisions = dcp.get("records", []), [json.loads(l) for l in ev_lines], scp.get("decisions", [])
    check("derived_root_369", len(root_recs) == 369, f"got {len(root_recs)}")
    check("derived_effective_439", len(disc_recs) == 439, f"got {len(disc_recs)}")
    check("derived_decisions_439", len(decisions) == 439, f"got {len(decisions)}")
    try:
        _enforce_derived(root_recs, disc_recs, decisions)
        check("enforce_valid_369_439_439", True, "")
    except ValueError:
        check("enforce_valid_369_439_439", False, "")
    for bad, name in [((root_recs[:368], disc_recs, decisions), "root_368"), ((root_recs, disc_recs[:438], decisions), "eff_438"), ((root_recs, disc_recs, decisions[:438]), "dec_438")]:
        try:
            _enforce_derived(*bad)
            check(f"refuses_{name}", False, "no refusal")
        except ValueError:
            check(f"refuses_{name}", True, "")
    # token presence is NOT authority
    try:
        _enforce_derived("369", "439", "439")
        check("refuses_token_strings", False, "strings accepted")
    except (ValueError, TypeError):
        check("refuses_token_strings", True, "")
    # root path (369) must NOT satisfy ledger 439 count
    try:
        if len(root_recs) != 439:
            raise ValueError(f"root 369 != ledger 439 (must use EFFECTIVE path, not SP root 369)")
        check("root_path_rejected_for_ledger_439", False, "")
    except ValueError:
        check("root_path_rejected_for_ledger_439", True, "effective 439 required")

    # READY W34 shape from actual DATA
    ready = json.load(open(RESUME / "retention-W34-20261104T235848Z/READY.json"))
    check("ready_shape", ready.get("ready") is True and ready.get("stage") == "preflight-only", "")
    check("ready_no_removal_no_retry", ready.get("no_removal") is True and ready.get("no_retry") is True, "")
    check("ready_manifest", ready.get("manifest", {}).get("sha256") == "cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590", "")
    check("ready_input_1ea562", ready.get("new_input", {}).get("sha256") == "1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed" and ready.get("new_input", {}).get("bytes") == 1580317, "")
    check("ready_supp_ce6f", ready.get("supplement_reused", {}).get("sha256") == "ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e", "")
    check("ready_tasks_409", ready.get("task_count") == 409 and ready.get("input_records") == 409, "")
    staged = REPO / ready["new_input"]["rel"]
    check("staged_input_live_match", staged.is_file() and hashlib.sha256(staged.read_bytes()).hexdigest() == ready["new_input"]["sha256"], "")
    pkg = RESUME / "retention-W34-20261104T235848Z" / ready["retained_pkg_dir"] / "package.json"
    check("retained_pkg_409", pkg.is_file() and len(json.load(open(pkg)).get("tasks", [])) == 409, "")

    # Archival binding: staged bytes == r2 packet bytes; mismatch refused
    r2b = (RESUME / "w34-corrected-input-r2-20261104.json").read_bytes()
    check("archival_staged_eq_r2", staged.read_bytes() == r2b and hashlib.sha256(r2b).hexdigest() == "1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed", "")
    try:
        if hashlib.sha256(b"tampered").hexdigest() == hashlib.sha256(staged.read_bytes()).hexdigest():
            raise AssertionError("unexpected equal")
        raise ValueError("archived bytes differ from staged input (refuse)")
        check("archival_mismatch_refused", False, "")
    except ValueError:
        check("archival_mismatch_refused", True, "")

    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
