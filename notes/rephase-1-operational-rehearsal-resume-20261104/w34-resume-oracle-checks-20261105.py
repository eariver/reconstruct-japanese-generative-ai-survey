#!/usr/bin/env python3
"""W34 resume oracle checks (stdlib only; no project import/run, no git/network).

Reproduces actual r2 task-target failure (split vs exact task set, as the
live run hit on c001) and proves r3 corrected ALL 409 via stdlib source-read
of retained package tasks + packet inputs (not tokens, not runtime).
"""
from __future__ import annotations
import json
from pathlib import Path

WS = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
PKG = WS / "notes/rephase-1-operational-rehearsal-resume-20261104/retention-W34-20261104T235848Z/pkg-w34-r2-20261104T235848Z"
R2 = WS / "notes/rephase-1-operational-rehearsal-resume-20261104/w34-corrected-input-r2-20261104.json"
R3 = WS / "notes/rephase-1-operational-rehearsal-resume-20261104/w34-corrected-input-r3-20261104.json"
PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def main() -> int:
    tm = {}
    for p in PKG.glob("tasks/task-*.json"):
        tj = json.loads(p.read_bytes().decode("utf-8"))
        tm[tj["discovery_ids"][0]] = tj.get("verification_targets", [])
    check("tasks_409_single_target", len(tm) == 409 and all(len(v) == 1 for v in tm.values()), "")
    r2 = {r["discovery_id"]: [v["target"] for v in r["verification"]] for r in json.loads(R2.read_bytes().decode("utf-8"))["records"]}
    r3 = {r["discovery_id"]: [v["target"] for v in r["verification"]] for r in json.loads(R3.read_bytes().decode("utf-8"))["records"]}
    # r2 failure reproduction (same exact-set rule as _build_card_core)
    bad2 = [did for did in tm if set(r2.get(did, [])) != set(tm[did])]
    check("r2_mismatch_14", len(bad2) == 14, f"{len(bad2)}")
    c001_missing = sorted(set(tm["w34-event-c001"]) - set(r2["w34-event-c001"]))
    c001_extra = sorted(set(r2["w34-event-c001"]) - set(tm["w34-event-c001"]))
    check("r2_c001_exact_failure", c001_missing == [tm["w34-event-c001"][0]] and len(c001_extra) == 2, f"missing={len(c001_missing)} extra={len(c001_extra)}")
    # r3 corrected ALL 409
    bad3 = [did for did in tm if set(r3.get(did, [])) != set(tm[did])]
    check("r3_all409_exact", len(bad3) == 0, f"mismatches={bad3[:3]}")
    r3rec = json.loads(R3.read_bytes().decode("utf-8"))["records"]
    from collections import Counter
    check("r3_counts_363_38_8", Counter(r["status"] for r in r3rec) == Counter({"PARTIAL": 363, "VERIFIED": 38, "NEEDS_MORE": 8}), "")
    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
