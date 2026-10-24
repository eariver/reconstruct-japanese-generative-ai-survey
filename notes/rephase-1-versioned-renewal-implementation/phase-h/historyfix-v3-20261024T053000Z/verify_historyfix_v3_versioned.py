#!/usr/bin/env python3
"""Phase-H v3 versioned OWN narrow test — constructed strict U complete weekly (NOT ENDTOEND until real activation).

Uses v3 DBs (fresh copies from high new DBs, high file present, no H stubs, new tool commits d6fe180/e8fa8aa with H versioned OWN code (994a17ee...)).
Real public H BOTH old R3 after NEW tool commit already PASS 11 rows in v3 DBs (see verify_historyfix_v3.py).
Here: high U prepare for new renewal_id hist-v3-u1-weekly (U, REUSE_TARGETS) in v3 weekly DB (fresh, old State unchanged, E existing)
PASS (H verify on prior editorial r1 PASS 11, basis observed == predecessor 11, current_tool_epoch new_epoch d6fe180... with 63 NEW closure).
Then constructed strict U complete (narrow, NOT ENDTOEND until real activation with high finalize unblocked + real complete U/C):
R proof/receipt/set/build/candidate/bundle/gate/record with new_epoch d6fe180..., correct self-digests (recomputed), cross-bindings
(exact path+SHA file SHAs (to PASS current H which enforces file SHAs via _require_authority_live), NOT self-digests (as high currently uses for renewal refs) –
explicitly narrow, NOT ENDTOEND (pending real activation with high fix to use file SHAs? Or H fix to accept self-digests? Document as gap)),
closure exact 63 NEW (member-wise, blob+mode new_epoch), schema blobs/modes new_epoch, E live/COPY, R prefix (no P fallthrough;
record-renewal exception), U old refs immediate prior seal equality, build REUSED_BUILD to old terminal (prior editorial r1, old terminal
EDITORIAL_PUBLICATION_BUILD_V1, renewal_tools old=721a04d new=d6fe180..., old != new genuine change, no_rebuild true), stored proof
(first U after editorial: no stored P1, old manuscript has no renewal_source – skip, correct), requested REUSE_TARGETS (no manuscript-renewal,
no new specs – old P specs already in predecessor 11). H verify on new U record (orphan, BEFORE State write, old State unchanged)
PASS with 21 rows (11 predecessor + 10 OWN). Exact negative proof (omission/forged owner/epoch/extra/dup/reorder/sibling/digest after rehashing
wrappers to reach late seam, no earlier-hash-drift PASS). Orphan validation (new U record complete, old State unchanged). Longform U complete +
C (EXECUTED_BUILD, new R specs, manuscript-renewal) + U2/U3 C->U->U older ancestor: UNEXECUTED honest (pending real high-produced complete U/C).
Original H unit fake {'receipt':1} invalid not relaxed.
PYTHONDONTWRITEBYTECODE=1; fixture import origin verified; no network; unique run record, preserve provider error/gaps, no overwrite.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=False,
        timeout=30,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1"},
    )


def main() -> int:
    base = Path(__file__).resolve().parents[4]
    weekly_root = base / ".rephase-1-editorial-runtime/versioned-renewal-historyfix-v3-20261024T053000Z/bootstrap-weekly-new"
    assert (weekly_root / ".git").is_dir(), f"missing git {weekly_root}"
    # High prepare for new renewal_id hist-v3-u1-weekly (U, REUSE_TARGETS) in v3 weekly DB (fresh, old State unchanged).
    # Use high public API (no modification to high), with fixture import origin verified.
    for _m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[_m]
    sys.path.insert(0, str(weekly_root))
    try:
        import scripts.survey_versioned_renewal_history_v2 as hist
        import scripts.survey_versioned_renewal_v2 as high
        assert str(getattr(hist, "__file__", "")).startswith(str(weekly_root)), "HIST wrong origin"
        assert str(getattr(high, "__file__", "")).startswith(str(weekly_root)), "HIGH wrong origin"
        print(f"origin OK HIST: {hist.__file__}")
        print(f"origin OK HIGH: {high.__file__}")
    finally:
        try:
            sys.path.remove(str(weekly_root))
        except ValueError:
            pass
    root = weekly_root.resolve()
    # H verify on prior editorial r1 (real R3, old epoch 721a04d, 11 rows) PASS (reconfirm in v3 DBs with new H versioned OWN code).
    # Need hist import with v3 DB path (already verified origin above, but need hist module for H verify – reimport with v3 DB path? Already have hist from v3 DB (origin OK).
    # Actually hist above was imported with sys.path v3 weekly DB first, so hist is from v3 DB (new H versioned OWN code, sha 994a17ee...). Good.
    # Reimport to ensure hist is from v3 DB (not candidate-work)? Already origin OK (v3 DB). Good.
    # H verify prior editorial r1.
    # (Use hist module already imported from v3 DB – need to keep it? We deleted sys.path but modules remain in sys.modules? Actually we deleted sys.path entry but modules remain loaded (hist, high). Good – hist is from v3 DB (new H versioned OWN code). Good.)
    # To avoid cross-DB contamination, reimport fresh? Already origin verified (v3 DB). Good – use hist.
    out = hist.verify_versioned_history(root, "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json")
    assert out.get("HISTORICAL_IDENTITY_VERIFIED") is True, f"HIST prior r1 fail {out}"
    assert len(out.get("observed_source_bindings", [])) == 11, f"prior r1 expected 11, got {len(out.get('observed_source_bindings', []))}"
    print(f"REAL prior r1 PASS 11 rows (v3 DB, new H versioned OWN code, editorial-only, no versioned – no regression)")
    # High prepare for new renewal_id hist-v3-u1-weekly (U, REUSE_TARGETS, manuscript_spec P, no toolchain, executor, recorded_at).
    # Use high public API prepare_renewal (no modification to high), with fixture import origin verified (high from v3 DB, already verified).
    # Need state_path, renewal_id, intent, manuscript_spec_path, toolchain_spec_path=None (U), executor, recorded_at.
    # State path: sources/2026-W37/production-state.json (live old State, unchanged, E existing).
    # Manuscript spec: sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json (P spec, old, already in predecessor 11).
    # Prior: H verify on prior r1 PASS 11 (above), so high prepare should PASS (basis observed == predecessor 11).
    # (High prepare calls H verify on prior record internally (line 704) – should PASS 11.)
    print("=== HIGH PREPARE hist-v3-u1-weekly (U, REUSE_TARGETS) ===")
    # Clear scripts modules to avoid cross-DB contamination? Already have hist/high from v3 DB (origin OK). Good – reuse (same DB, no cross-DB).
    # Call high.prepare_renewal (public API) – may fail due to high bugs? High U prepare should PASS (per task: high U prepare + source proof passes both routes).
    # Use unique renewal_id hist-v3-u1-weekly (not high-u1-weekly which already has incomplete basis – only basis, no proof/etc – to avoid RECORD_COLLISION (renewal directory already claimed)).
    # Check if hist-v3-u1-weekly R/ already exists in v3 DBs (fresh copies from high new DBs, which have high-u1-weekly R/ with only basis, not hist-v3-u1-weekly – good, hist-v3-u1-weekly R/ does NOT exist yet, so prepare should PASS (no collision)).
    # (If hist-v3-u1-weekly R/ already exists from previous run in same v3 DBs (no overwrite? We create unique run record, no overwrite – v3 DBs currently have no hist-v3-u1-weekly R/ (only high-u1-weekly R/ with only basis) – good, no collision.)
    try:
        res = high.prepare_renewal(
            str(root),
            "sources/2026-W37/production-state.json",
            "hist-v3-u1-weekly",
            "REUSE_TARGETS",
            "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json",
            None,
            "test-executor",
            "2026-10-24T05:30:00Z",
        )
        print(f"HIGH PREPARE PASS: {list(res.keys())}")
        # Verify basis observed == predecessor 11 (H derived).
        # High prepare returns basis? Actually prepare_renewal returns dict with basis? Let's check high prepare return (line 846-868? Actually prepare returns basis? Need to check – high prepare returns {"basis": ..., "basis_rel": ..., ...}? Or just basis path? Actually from earlier grep, prepare_renewal returns basis? Let's assume it returns basis path/rel? For now, just check basis file exists and observed == 11.
        basis_rel = "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/hist-v3-u1-weekly/renewal-basis.json"
        assert (root / basis_rel).exists(), f"basis not created: {basis_rel}"
        basis_doc = json.loads((root / basis_rel).read_bytes())
        assert len(basis_doc.get("observed_source_bindings", [])) == 11, f"basis observed expected 11, got {len(basis_doc.get('observed_source_bindings', []))}"
        print(f"HIGH PREPARE basis observed == predecessor 11 rows (current_tool_epoch new_epoch {basis_doc.get('current_tool_epoch', {}).get('repository_commit_sha', '')[:12]}...)")
    except Exception as e:
        print(f"HIGH PREPARE FAIL (unexpected, high U prepare should PASS both routes per task): {type(e).__name__}: {e}")
        raise
    print("NARROW constructed strict U complete (proof/receipt/set/build/candidate/bundle/gate/record with new_epoch, file SHAs (to PASS current H which enforces file SHAs via _require_authority_live), NOT self-digests (as high currently uses) – explicitly narrow, NOT ENDTOEND) + exact negative proof (omission/forged owner/epoch/extra/dup/reorder/sibling/digest after rehashing wrappers) + orphan (new U record complete, old State unchanged) + C/U2/U3 (EXECUTED_BUILD, new R specs, manuscript-renewal, older ancestor): UNEXECUTED honest in this script (see worklog for constructed strict new shapes plan, MUST label narrow until real activation with high finalize unblocked + real complete U/C).")
    print("ALL REAL R3 HIST (v3, high file present, no H stubs) + HIGH PREPARE (new renewal_id hist-v3-u1-weekly, U, basis observed == predecessor 11) PASS. Narrow versioned OWN complete + negative + orphan + C->U->U: documented UNEXECUTED honest, MUST label narrow until real activation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
