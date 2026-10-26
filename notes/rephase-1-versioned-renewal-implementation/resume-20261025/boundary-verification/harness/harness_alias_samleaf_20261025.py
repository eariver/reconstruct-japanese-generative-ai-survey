#!/usr/bin/env python3
"""Boundary verification — alias same-leaf hardlink (public) + helper defensive.

TEST-only, no product edits. OWN CURRENT 741 (HIGH 1dad1ad, H 74275d, S 2290ddd).
Forks byte-independent (cp -a, no -l) from existing H-ACT CURRENT fork
(raw/case-healthy-activate-current-20261026T000500Z/fork-healthy-activate-current,
ACTIVATED r2, State new) to avoid duplicate live writers. No new source commit
(worktree authorities only, source pins unchanged). No network/old-runner/
candidate/reconstruct commit/cleanup. No deletion of failed partial/foreign.

Public attempt: real dir alias-R (NOT symlink) + hardlink
alias-R/publication-set.json -> cu1-weekly/publication-set.json (same leaf
publication-set.json, different parent spelling, same inode/SHA, nlink==2,
no symlink ancestor). Activate with alias path. Expected per task: if earlier
SEAL_BIND/HIGH_MODE legitimate path guard refuses BEFORE writes (no record,
State unchanged, NOT ALREADY_ACTIVE), classify as legitimate public refusal;
do NOT invent bypass to reach alias-identity. True RECORD_COLLISION
alias-identity (NOT ALREADY_ACTIVE, BEFORE writes) is intended B3 seam; if
registry forbids all alias paths, test helper _check_already_active_set
directly (defensive standalone unit, counted separately, NOT public).

Root: no duplicate case count standalone unit vs public distinct.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def file_id(p: Path) -> tuple[int, int, int, str]:
    st = os.lstat(p)
    import hashlib

    h = hashlib.sha256(p.read_bytes()).hexdigest()
    return (st.st_dev, st.st_ino, st.st_nlink, h)


def main() -> int:
    own_src = Path(sys.argv[1]).resolve()
    fork_src = Path(sys.argv[2]).resolve()  # H-ACT CURRENT fork (ACTIVATED)
    work_fork = Path(sys.argv[3]).resolve()  # new work fork (to be created by caller via cp -a)
    out_json = Path(sys.argv[4]).resolve()
    # Use work_fork's own code (same CURRENT pins, verified) to avoid wrong-root
    # (product _verify_module_roots correctly refuses code from different root).
    # OWN snapshot pins guard against torn read; verify fork code matches OWN.
    import hashlib as _hl

    for _name, _pin in (
        ("survey_versioned_renewal_history_v2.py", "74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d"),
        ("survey_versioned_renewal_v2.py", "1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb"),
        ("survey_versioned_renewal_source_v2.py", "2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb"),
    ):
        _fp = work_fork / "scripts" / _name
        _h = _hl.sha256(_fp.read_bytes()).hexdigest()
        assert _h == _pin, f"fork code drift for {_name}: {_h} != {_pin} (fail-closed, no stale)"
    sys.path.insert(0, str(work_fork))
    from scripts import survey_versioned_renewal_v2 as high

    repo = work_fork.resolve()
    # Canonical set (from cu1-weekly, ACTIVATED via r2).
    # Discover canonical set via State selection (ACTIVATED).
    state_rel = "sources/2026-W37/production-state.json"
    state = json.loads((repo / state_rel).read_bytes().decode("utf-8"))
    prov = state.get("publication_revalidation_provenance") or {}
    record_rel = str(prov.get("path") or "")
    assert record_rel, "work fork State not ACTIVATED (no provenance path)"
    record = json.loads((repo / record_rel).read_bytes().decode("utf-8"))
    canonical_set_rel = str((record.get("set_ref") or {}).get("path") or "")
    assert canonical_set_rel.endswith("/publication-set.json"), canonical_set_rel
    canonical_abs = repo / canonical_set_rel
    assert canonical_abs.is_file() and not canonical_abs.is_symlink()
    c_dev, c_ino, c_nlink_before, c_sha = file_id(canonical_abs)
    state_before = (repo / state_rel).read_bytes()
    import hashlib

    state_sha_before = hashlib.sha256(state_before).hexdigest()

    # Create real alias dir + hardlink same leaf.
    alias_dir_rel = str(Path(canonical_set_rel).parent.parent.as_posix() + "/alias-r-samleaf")
    alias_dir_abs = repo / alias_dir_rel
    alias_dir_abs.mkdir(parents=True, exist_ok=True)
    alias_set_rel = alias_dir_rel + "/publication-set.json"
    alias_abs = repo / alias_set_rel
    if alias_abs.exists() or alias_abs.is_symlink():
        alias_abs.unlink()
    os.link(canonical_abs, alias_abs)
    a_dev, a_ino, a_nlink_after, a_sha = file_id(alias_abs)
    c_dev2, c_ino2, c_nlink_after, c_sha2 = file_id(canonical_abs)
    same_inode = (a_dev == c_dev2 and a_ino == c_ino2)
    same_sha = (a_sha == c_sha2)
    different_spelling = (alias_set_rel != canonical_set_rel)
    same_leaf = (Path(alias_set_rel).name == Path(canonical_set_rel).name == "publication-set.json")

    # Public attempt: activate with alias set path (same leaf, different parent).
    code = None
    detail = ""
    phase = None
    try:
        high.activate_renewal(str(repo), state_rel, alias_set_rel, "Core change: alias samleaf public probe", "boundary-worker-20261025")
    except Exception as exc:  # noqa: BLE001
        code = getattr(exc, "code", None) or type(exc).__name__
        detail = getattr(exc, "detail", None) or str(exc)
        phase = getattr(exc, "phase", None)
    else:
        code = "ACTIVATED_UNEXPECTED"
        detail = "alias activate unexpectedly succeeded"

    state_after = (repo / state_rel).read_bytes()
    state_sha_after = hashlib.sha256(state_after).hexdigest()
    # No new record? Check parent dir for new rN beyond existing max.
    parent = str(Path(record_rel).parent.as_posix())
    names = sorted(p.name for p in (repo / parent).iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    result = {
        "unit": "alias-samleaf-public (public, real dir + hardlink same leaf)",
        "source_pins": {
            "HIGH": "1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb",
            "H": "74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d",
            "S": "2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb",
        },
        "canonical_set": canonical_set_rel,
        "alias_set": alias_set_rel,
        "same_leaf": same_leaf,
        "different_spelling": different_spelling,
        "same_inode": bool(same_inode),
        "same_sha": bool(same_sha),
        "nlink_before": c_nlink_before,
        "nlink_after": c_nlink_after,
        "code": code,
        "phase": phase,
        "detail": detail[:800],
        "state_unchanged": bool(state_sha_before == state_sha_after),
        "records_after": names,
        "alias_preserved": bool(alias_abs.exists()),
        "is_path_guard": bool(code in ("SEAL_BIND", "HIGH_MODE", "HIGH_PATH", "HIGH_UNREADABLE") if isinstance(code, str) else False),
        "is_alias_identity": bool(isinstance(code, str) and code == "RECORD_COLLISION" and "alias" in detail.lower()),
        "is_already": bool(isinstance(code, str) and "ALREADY" in code),
        "label": "legitimate public refusal/no writes if earlier SEAL_BIND/HIGH_MODE; RECORD_COLLISION alias-identity if reached; never ALREADY_ACTIVE by same SHA",
    }
    # Defensive helper unit (standalone, NOT public): direct _check_already_active_set
    # with same inode different spelling (no registry bypass, no product edit).
    helper: dict = {}
    try:
        from scripts.survey_versioned_renewal_v2 import _check_already_active_set, _file_identity

        # Selected ref = canonical (from live State selection? Use canonical path+SHA).
        sel_ref = {"path": canonical_set_rel, "sha256": c_sha2}
        # Supplied = alias (different spelling, same SHA/inode).
        try:
            hit = _check_already_active_set(repo, alias_set_rel, a_sha, sel_ref, "ALREADY_ACTIVE set")
            helper = {"returned": bool(hit), "note": "helper returned without refusal (unexpected for alias)"}
        except Exception as hexc:  # noqa: BLE001
            helper = {
                "code": getattr(hexc, "code", None) or type(hexc).__name__,
                "detail": (getattr(hexc, "detail", None) or str(hexc))[:500],
                "is_alias_refusal": bool((getattr(hexc, "code", None) == "RECORD_COLLISION") and ("alias" in str(getattr(hexc, "detail", "") or "").lower())),
            }
    except Exception as exc:  # noqa: BLE001
        helper = {"error": str(exc)[:300]}

    result["helper_defensive"] = helper
    out_json.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=1, sort_keys=True))
    # Success if public refuses before writes (any REFUSED_PRE_WRITE, NOT ALREADY, State unchanged, alias preserved).
    refused = isinstance(code, str) and ("REFUS" in detail.upper() or code in ("RECORD_COLLISION", "SEAL_BIND", "HIGH_MODE", "HIGH_UNREADABLE", "HIGH_PATH"))
    ok = bool(refused and result["state_unchanged"] and result["alias_preserved"] and not result["is_already"])
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
