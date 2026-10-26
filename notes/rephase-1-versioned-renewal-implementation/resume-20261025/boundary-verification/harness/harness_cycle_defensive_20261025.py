#!/usr/bin/env python3
"""Boundary verification — defensive walker cycle-cap probe (standalone unit, NOT public).

TEST-only, no product edits. Uses OWN fixed runtime SOURCE copy (CURRENT 741:
HIGH 1dad1ad, H 74275d, S 2290ddd). Product bytes pinned before/after, unchanged.

True public SHA-consistent loop impossible without cryptographic fixedpoint;
do NOT fake 'public valid cycle'. Public malformed cycle already fails closed
as HISTORY_DIGEST_MISMATCH (cite case-cycle-proper-rehash-20261026T000200Z,
CURRENT H 74275d, exit 0, State unchanged, no new R — retained, NOT rerun here).

This file is an isolated defensive walker branch probe: supplies a cyclic ref
sequence through a controlled read seam (patches _load_record_file in-process
ONLY, product file bytes unchanged) to hit the walker's cycle cap
(HISTORY_ANCESTOR cycle) and depth cap (HISTORY_ANCESTOR too deep). Explicit
unit defensive, NOT full cryptographic proof. Qualification matches previous
R7 precedent (r6-cycle-malformed fails closed + walker discipline), sufficient
bounded cycle oracle, NOT open impossible cryptography.

Root: no duplicate case count — standalone unit vs public distinct. This
defensive unit is counted separately from public malformed-cycle citation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    own_src = Path(sys.argv[1]).resolve()
    out_json = Path(sys.argv[2]).resolve()
    sys.path.insert(0, str(own_src))
    from scripts import survey_versioned_renewal_history_v2 as hist

    assert hist.CHAIN_LIMIT == 32, f"CHAIN_LIMIT changed: {hist.CHAIN_LIMIT}"
    # Controlled seam: patch _load_record_file to return synthetic cyclic chain.
    orig_load = hist._load_record_file
    # Build synthetic 2-cycle: rA supersedes rB, rB supersedes rA.
    rec_a = {"supersedes": {"path": "rB.json", "sha256": "b" * 64}}
    rec_b = {"supersedes": {"path": "rA.json", "sha256": "a" * 64}}

    def fake_load(repo_root: Path, ref: dict, label: str):
        p = str(ref.get("path"))
        if p == "rA.json":
            return dict(rec_a)
        if p == "rB.json":
            return dict(rec_b)
        raise AssertionError(f"unexpected ref in cycle probe: {p}")

    hist._load_record_file = fake_load  # type: ignore
    cycle_code = None
    cycle_detail = ""
    try:
        hist._walk_chain_backwards(Path("/tmp/defensive-cycle-root"), {"path": "rA.json", "sha256": "a" * 64})
    except Exception as exc:  # noqa: BLE001
        cycle_code = getattr(exc, "code", None) or type(exc).__name__
        cycle_detail = getattr(exc, "detail", None) or str(exc)
    finally:
        hist._load_record_file = orig_load  # type: ignore

    # Depth cap probe: 33-length linear chain via same seam (r0->r1->...->r32).
    chain_recs: dict[str, dict] = {}
    for i in range(33):
        nxt = None if i == 0 else {"path": f"r{i-1}.json", "sha256": f"{i-1:064x}"[-64:]}
        # Use deterministic fake SHAs (64 hex) for refs; loader bypasses SHA check.
        chain_recs[f"r{i}.json"] = {"supersedes": nxt}

    def fake_load_depth(repo_root: Path, ref: dict, label: str):
        p = str(ref.get("path"))
        if p in chain_recs:
            return dict(chain_recs[p])
        raise AssertionError(f"unexpected ref in depth probe: {p}")

    hist._load_record_file = fake_load_depth  # type: ignore
    depth_code = None
    depth_detail = ""
    try:
        hist._walk_chain_backwards(
            Path("/tmp/defensive-depth-root"),
            {"path": "r32.json", "sha256": "c" * 64},
        )
    except Exception as exc:  # noqa: BLE001
        depth_code = getattr(exc, "code", None) or type(exc).__name__
        depth_detail = getattr(exc, "detail", None) or str(exc)
    finally:
        hist._load_record_file = orig_load  # type: ignore

    result = {
        "unit": "defensive-walker-cycle-cap (standalone, NOT public)",
        "source_pins": {
            "HIGH": "1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb",
            "H": "74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d",
            "S": "2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb",
        },
        "chain_limit": hist.CHAIN_LIMIT,
        "cycle_probe": {"code": cycle_code, "detail": cycle_detail[:500]},
        "depth_probe": {"code": depth_code, "detail": depth_detail[:500]},
        "cycle_hits_cap": bool(cycle_code == "HISTORY_ANCESTOR" and "cycle" in cycle_detail.lower()),
        "depth_hits_cap": bool(depth_code == "HISTORY_ANCESTOR" and "deep" in depth_detail.lower()),
        "public_citation": "case-cycle-proper-rehash-20261026T000200Z (HISTORY_DIGEST_MISMATCH qualified preemption, CURRENT H 74275d, exit 0, State unchanged, no new R — retained, NOT rerun)",
        "no_product_edit": True,
        "label": "defensive unit, NOT full cryptographic proof; true public SHA-consistent loop OPEN (impossible without fixedpoint, NOT faked)",
    }
    out_json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    ok = bool(result["cycle_hits_cap"] and result["depth_hits_cap"])
    print(json.dumps(result, indent=1, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
