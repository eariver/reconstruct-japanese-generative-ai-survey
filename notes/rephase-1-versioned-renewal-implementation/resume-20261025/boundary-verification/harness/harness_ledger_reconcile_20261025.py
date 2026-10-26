#!/usr/bin/env python3
"""Boundary verification — failure ledger reconcile (read-only, no fixture).

TEST-only, no product edits. Reads actual raw case dirs under
failure-resume-verification/raw/case-*, extracts named IDs, actual source
(stale 9a vs CURRENT 1dad1ad/H74275d/S2290ddd via result content + manifest),
and terminal exits (exit.txt). NO new counts from guessing; reports actual
completed coverage vs remaining; whole unit no CommitPoint/independent PASS.

Old 16 sum confused: testmatrix S6 counted 12 fault HIT (11+1 depth double-count
ambiguity) + 3 partial + 3 seam-miss; S9 revised to 16 HIT (11+5) + 5 partial +
3 seam-miss + 5 defects + 11 OPEN. Confusion came from double-counting depth
(high-prepare-33 in both healthy and fault), counting H-ACT setup inside
already-active/alias/orphan setups as separate methods, and mixing stale vs
CURRENT sources. This ledger reconciles by named ID with actual source/exit,
splitting distinct methods/subcases/harness errors/earlier-guard controls.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


STALE_MARKERS = ("fr-u1-weekly", "e211e6e", "9a0469ef", "6fe86e78", "20f63eaf")
CURRENT_MARKERS = ("cu1-weekly", "4851523", "1dad1ad", "74275d", "2290ddd")


def main() -> int:
    packet = Path(sys.argv[1]).resolve()
    raw_root = packet.parent / "failure-resume-verification" / "raw"
    # packet here is boundary-verification; parent is resume-20261025.
    # Actually argv[1] = resume-20261025 dir.
    resume_dir = Path(sys.argv[1]).resolve()
    raw_root = resume_dir / "failure-resume-verification" / "raw"
    out_json = Path(sys.argv[2]).resolve()
    rows = []
    for d in sorted(raw_root.glob("case-*")):
        cid = d.name
        exit_path = d / "exit.txt"
        if exit_path.is_file():
            try:
                exit_code = exit_path.read_text(encoding="utf-8").strip().split()[0]
            except Exception:  # noqa: BLE001
                exit_code = "READ_ERROR"
        else:
            exit_code = "MISSING (timeout-incomplete, preserved, NOT adopted)"
        results = sorted(d.glob("result*.json"))
        codes = []
        for r in results:
            try:
                doc = json.loads(r.read_text(encoding="utf-8"))
                codes.append({"file": r.name, "code": doc.get("code"), "phase": doc.get("phase"), "detail": str(doc.get("detail") or "")[:200]})
            except Exception as exc:  # noqa: BLE001
                codes.append({"file": r.name, "code": f"READ_ERROR {exc}"})
        # Source inference: scan result + commands.log + stdout for markers.
        blob = ""
        for f in list(results) + [d / "commands.log"]:
            try:
                if f.is_file():
                    blob += f.read_text(encoding="utf-8", errors="replace")[:8000]
            except Exception:  # noqa: BLE001
                pass
        src = "unknown"
        if any(m in blob for m in CURRENT_MARKERS):
            src = "CURRENT 1dad1ad/H74275d/S2290ddd (4851523 epoch, cu1-weekly)" if any(m in blob for m in ("1dad1ad", "74275d", "4851523", "cu1-weekly")) else "CURRENT-marker"
        if any(m in blob for m in STALE_MARKERS) and src == "unknown":
            src = "STALE 9a0469ef/H6fe/S20f (e211e6e epoch, fr-u1-weekly)"
        # Refine: check manifest-known CURRENT cases by ID.
        if cid in ("case-postreplace-true-mismatch-20261026T000200Z", "case-parent-alias-same-leaf-20261026T000200Z", "case-cycle-proper-rehash-20261026T000200Z", "case-sequence-nonincreasing-time-20261026T000200Z", "case-high-prepare-33-current-20261026T000400Z", "case-healthy-activate-current-20261026T000500Z"):
            src = "CURRENT 1dad1ad/H74275d/S2290ddd (4851523, cu1-weekly)"
        elif cid == "case-high-prepare-33-current-20261026T000300Z":
            src = "CURRENT attempt but harness defect (exit 1, no result; _copy requires renewal modules absent in R6 typed33)"
        elif cid.startswith("case-") and src == "unknown":
            # Default old cases are stale 9a per testmatrix S6/S8 (pinned OWN 740, fixture e211e6e).
            src = "STALE 9a0469ef/H6fe/S20f (e211e6e, fr-u1-weekly) [inferred from testmatrix S6/S8; result blob lacked explicit pin]"
        rows.append({"case": cid, "exit": exit_code, "results": codes, "source": src})
    summary = {
        "raw_case_dirs": len(rows),
        "exit_0": sum(1 for r in rows if str(r["exit"]).strip() == "0"),
        "exit_1": sum(1 for r in rows if str(r["exit"]).strip() == "1"),
        "exit_missing": sum(1 for r in rows if "MISSING" in str(r["exit"])),
        "note": "Counts are raw dirs only (distinct UTC dirs, NOT methods/subcases). Methods/subcases/harness errors/earlier-guard controls split in reconciled table (see boundary-verification README/table). NO new counts from guessing; NO whole-unit/independent PASS.",
    }
    out = {"rows": rows, "summary": summary}
    out_json.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
