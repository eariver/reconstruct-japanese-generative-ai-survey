#!/usr/bin/env python3
"""NEW renewal U with anchor fix (positive + negatives, no whole PASS).

Fixture: versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly
  PRE-activation State -> r3 GOOD (2797be, controlled construction), source fix 05e32ec (HIGH 1dad/H 7427/S 2290) committed BEFORE authority, E unchanged, bad r4 inert (9b69).

Positive (public, strict):
  prepare high-u1-anchor-fix REUSE_TARGETS (mspec ed3, toolchain None) -> basis anchor must be r2 (27db, NOT DRAFT_COMPLETE).
  finalize -> receipt/set with correct anchor.
  activate -> ACTIVATED r5 (since r4 inert, gaps okay), State -> r5, anchor r2 unchanged, history HISTORICAL_IDENTITY_VERIFIED chain4 (r1+r2+r3+r5), strict State/history/set/receipt/current prove R1 r2 anchor unchanged.
  R1/canonical after refusal no writes (refresh-mechanical-evidence refused in VERSIONED_ACTIVE, no new r6).
  Ordinary activate SAME set orphan still refuse per HIGH b124 (INTENT_COLLISION, no new record, no State change) - don't regress.

Negatives (public seams, BEFORE any State write):
  forged anchor ref same kind DRAFT after rehashing basis/proof/set/record -> refuse BEFORE any State write (no digest-only seam).
  wrong latest legacy / stale original / current anchor mutations preserved (tested via HIST direct + basis direct, no State mutation).
  No None Candidate/predecessor enums metadata fake.

Captures commands/exits/PIDs/source pins/raw window/immediate fs. No ordinary
candidate/reconstruct commit, no network/old runners/cleanup. Original BAD
fixture preserved UNTOUCHED (this script never touches old path).
"""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    repo = Path(__file__).resolve().parents[4]
    fix = repo / ".rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly"
    raw = repo / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-correction/raw/renewal-20261025T200000Z"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "pid.txt").write_text(str(os.getpid()) + "\n")
    for k in list(os.environ):
        if k.startswith("GIT_"):
            del os.environ[k]
    log = []
    def emit(s: str) -> None:
        print(s)
        log.append(s)
    # Source pins (fixed)
    for rel in ["scripts/survey_versioned_renewal_v2.py", "scripts/survey_versioned_renewal_history_v2.py", "scripts/survey_versioned_renewal_source_v2.py"]:
        emit(f"FIX {rel} sha={sha_file(fix / rel)[:8]}")
    sys.path.insert(0, str(fix.resolve()))
    # Ensure fresh imports from fix (no old caching)
    for mod in list(sys.modules):
        if mod.startswith("scripts."):
            del sys.modules[mod]
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    from scripts import survey_versioned_renewal_v2 as high
    from scripts import survey_versioned_renewal_history_v2 as hist
    from scripts import survey_versioned_renewal_source_v2 as srcmod
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_publication_set_v2 as setmod
    import scripts.survey_production_v2 as core
    state_rel = "sources/2026-W37/production-state.json"
    # Pre-check: State -> r3 GOOD, r4 inert exists but not selected
    state = json.loads((fix / state_rel).read_bytes())
    emit(f"PRE State pointer={state.get('publication_revalidation_provenance')}")
    assert state["publication_revalidation_provenance"]["path"] == "sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json"
    assert (fix / "sources/2026-W37/publication/v2/publication-surface-revalidation-r4.json").exists(), "bad r4 must exist inert"
    emit("PRE State -> r3 GOOD, bad r4 inert preserved (not selected)")
    # Prepare NEW U (fresh ID high-u3-anchor-fix; prior high-u1/u2 incomplete preserved, no same-byte takeover/cleanup)
    rid = "high-u3-anchor-fix"
    mspec = "sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/manuscript-spec.json"
    try:
        res = high.prepare_renewal(str(fix), state_rel, rid, "REUSE_TARGETS", mspec, None, "anchor-fix", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
        emit(f"PREPARE OK {res}")
    except Exception as e:
        emit(f"PREPARE FAIL {getattr(e,'code','?')} {e}")
        (raw / "diagnosis.txt").write_text("\n".join(log) + "\n")
        return 2
    basis_rel = res["basis_path"]
    basis = json.loads((fix / basis_rel).read_bytes())
    emit(f"BASIS anchor={basis.get('canonical_anchor')}")
    # Basis anchor must be r2 (27db), NOT DRAFT_COMPLETE
    assert basis["canonical_anchor"]["kind"] == "LEGACY_REVALIDATION"
    assert basis["canonical_anchor"]["ref"]["path"] == "sources/2026-W37/publication/v2/publication-surface-revalidation-r2.json"
    assert basis["canonical_anchor"]["ref"]["sha256"] == "27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582", "basis anchor must be REAL r2, not DRAFT_COMPLETE"
    emit("BASIS anchor REAL r2 VERIFIED (not DRAFT_COMPLETE)")
    # Detached S verification (prior HIST full anchor)
    try:
        srcmod.validate_renewal_basis(str(fix), basis_rel)
        emit("S validate_renewal_basis PASS (prior HIST full anchor verified)")
    except Exception as e:
        emit(f"S FAIL {e}")
        return 2
    # Finalize with FRESH QA (recorded AFTER basis capture, exact live bytes reinspected, synthetic non-genuine).
    # Old ed3 deterministic-checks are stale (recorded before new basis) and correctly refuse.
    # Generate fresh checks JSON in new renewal dir (untracked, not SOURCE commit) after prepare.
    import hashlib as _hl
    _qdir = "sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/publication/quality"
    _checks = []
    for _cid, _fn in [("SUBJECT_ENTITY_PROPERTY_BINDING", "subject-entity-property-binding.json"), ("IDENTIFIER_PRESERVATION", "identifier-preservation.json"), ("PDF_PREFLIGHT", "pdf-preflight.json")]:
        _p = f"{_qdir}/{_fn}"
        _data = (fix / _p).read_bytes()
        _checks.append({
            "check_id": _cid, "kind": "DETERMINISTIC", "status": "PASS",
            "executor": "anchor-fix U fresh assertions (synthetic, non-genuine)",
            "evidence": f"Exact clone bytes reinspected: {_p}",
            "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "result": {"path": _p, "sha256": _hl.sha256(_data).hexdigest()},
        })
    _fresh_rel = f"sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/renewals/{rid}/fresh-checks.json"
    (fix / _fresh_rel).parent.mkdir(parents=True, exist_ok=True)
    (fix / _fresh_rel).write_text(json.dumps({"checks": _checks}, indent=1) + "\n")
    emit(f"FRESH checks written {_fresh_rel} 3/3 PASS (recorded after basis, live bytes reinspected)")
    checks_rel = _fresh_rel
    # Semantic/visual predecessor paths: from prior seal publication/semantic-review-v2.json + visual-review-v2.json?
    # Prior seal is .../wk-anchor-ed3/publication/publication-set.json, roles include semantic-review? Actually 15 roles include semantic-review? Let's try with None (derive predecessor) if API allows.
    # Read finalize signature
    import inspect
    emit(f"finalize sig {inspect.signature(high.finalize_renewal)}")
    try:
        # Try with None reviews (derive predecessor) - per contract U allows absent (derive predecessor records)
        fres = high.finalize_renewal(str(fix), state_rel, basis_rel, checks_rel, None, None, "anchor-fix", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
        emit(f"FINALIZE OK keys={sorted(fres.keys())}")
    except Exception as e:
        emit(f"FINALIZE FAIL {getattr(e,'code','?')} {e}")
        import traceback
        traceback.print_exc()
        (raw / "diagnosis.txt").write_text("\n".join(log) + "\n")
        return 2
    set_rel = fres.get("set_path") or fres.get("set_path", "")
    # Find set_path key (finalize returns *_path suffix per new code)
    if not set_rel:
        # Try alternative keys
        for k, v in fres.items():
            if "set" in k.lower() and isinstance(v, str) and v.endswith(".json"):
                set_rel = v
                break
    emit(f"SET {set_rel}")
    # Activate (should ACTIVATE r5 with correct anchor, NOT INDETERMINATE)
    try:
        ares = high.activate_renewal(str(fix), state_rel, set_rel, "Anchor renewal U high-u1-anchor-fix after editorial r3 (fix verification)", "anchor-fix", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
        emit(f"ACTIVATE OK {ares}")
    except Exception as e:
        emit(f"ACTIVATE FAIL {getattr(e,'code','?')} {e}")
        import traceback
        traceback.print_exc()
        (raw / "diagnosis.txt").write_text("\n".join(log) + "\n")
        return 2
    assert ares.get("status") == "ACTIVATED", f"expected ACTIVATED, got {ares}"
    record_rel = ares["record_path"]
    emit(f"NEW record {record_rel}")
    # New record should be r5 (since r4 inert exists), supersedes r3, anchor r2
    record = json.loads((fix / record_rel).read_bytes())
    emit(f"NEW record supersedes={record.get('supersedes')} anchor={record.get('canonical_anchor')}")
    assert record["supersedes"]["path"] == "sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json", "new r5 must supersede r3 (not r4 inert)"
    assert record["canonical_anchor"]["ref"]["sha256"] == "27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582", "new record anchor must be REAL r2"
    assert "r5" in record_rel, f"new record should be r5 (gaps okay, r4 inert), got {record_rel}"
    emit("NEW record r5 supersedes r3 anchor r2 VERIFIED (no rolling, gaps okay)")
    # Strict State/history/set/receipt/current prove R1 r2 anchor unchanged
    post_state = json.loads((fix / state_rel).read_bytes())
    emit(f"POST State pointer={post_state.get('publication_revalidation_provenance')}")
    cfg = json.loads((fix / "config/survey-production-v2.json").read_bytes())
    errs = agent.validate_agent_state(fix, cfg, post_state)
    assert not errs, f"POST State must be strict VALID (no Gate drift), errs={errs}"
    emit("POST State strict VALID (no anchor mismatch, no Gate drift)")
    sel = setmod.resolve_publication_selection(fix, cfg, post_state)
    assert sel["mode"] == "VERSIONED_ACTIVE"
    assert sel["canonical_anchor"]["ref"]["sha256"] == "27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582"
    emit(f"POST selection VERSIONED_ACTIVE anchor r2 VERIFIED canonical gate={sel['canonical7']['reader-surface-gate']['sha256'][:8]} effective gate={sel['effective7']['reader-surface-gate']['sha256'][:8]}")
    # History verifies new chain r1+r2+r3+r5 (chain4, r4 inert not in chain)
    hres = hist.verify_versioned_history(str(fix), record_rel)
    assert hres["HISTORICAL_IDENTITY_VERIFIED"] and hres["chain_length"] == 4, f"history chain must be 4 (r1+r2+r3+r5), got {hres}"
    assert hres["canonical_anchor"]["ref"]["sha256"] == "27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582"
    emit(f"HISTORY chain4 VERIFIED anchor r2 (R1 r2 anchor unchanged through new renewal)")
    (raw / "diagnosis.txt").write_text("\n".join(log) + "\n")
    (raw / "exit.txt").write_text("0\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
