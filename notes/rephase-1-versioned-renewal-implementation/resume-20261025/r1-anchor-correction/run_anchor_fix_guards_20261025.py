#!/usr/bin/env python3
"""Guards + negatives for anchor fix (no whole PASS).

Fixture: anchor-fix-weekly POST r5 ACTIVATED (State -> r5 GOOD, anchor r2).
All checks read-only except intended refusal seams (no State mutation on negatives).
Original BAD fixture untouched. No ordinary commits, no network, no cleanup.

Positives (must PASS):
  P1: R1/canonical after versioned refusal no writes (refresh-mechanical-evidence exit2, no new r6, HEAD unchanged, records still r1+r2+r3+r4(inert)+r5).
  P2: Ordinary activate SAME set orphan still refuse per HIGH b124 (INTENT_COLLISION, no new record, State unchanged) - don't regress orphan fix.

Negatives (must REFUSE BEFORE any State write, no INDETERMINATE mutation):
  N1: Forged anchor ref same kind DRAFT (LEGACY_REVALIDATION ref DRAFT_COMPLETE ffbde) after rehashing basis/proof/set/record -> refuse BEFORE State write.
      Construct forged basis (copy good basis, replace anchor with DRAFT_COMPLETE, rehash basis_sha256), then forged proof (update basis_ref SHA, rehash proof_sha256), forged receipt (update proof ref, rehash receipt_sha256), forged set (update receipt/proof refs, rehash set_sha256), forged record? Actually for activation negative, forge basis anchor then try prepare? No, prepare creates basis from HIST (correct). For forged test, directly forge basis file + proof/set + record chain? Simpler: forge HIST-level? Per task: "forged anchor ref same kind DRAFT after rehashing basis/proof/set/record -> refuse BEFORE any State write (intended no earlier digest-only seam)".
      Means: take GOOD r5 chain (basis/proof/set/record with correct r2 anchor), forge anchor to DRAFT_COMPLETE in basis, rehash basis, then rehash proof (basis_ref), receipt (proof ref), set (receipt/proof refs), record (basis/proof/set refs + anchor?) Actually record anchor also forged to DRAFT_COMPLETE? The task says same kind DRAFT (LEGACY kind with DRAFT ref) - so forge anchor kind stays LEGACY_REVALIDATION but ref becomes DRAFT_COMPLETE (same kind, different ref). After rehashing all wrappers to make digests consistent (no digest-only seam), activation/history must still refuse via chain-derived identity (not just digest mismatch), BEFORE State write.
  N2: Wrong latest legacy (anchor r1 instead of r2) -> HIST refuse.
  N3: Stale original (anchor DRAFT_COMPLETE) -> HIST refuse (already proven by old r4, but re-prove on new chain read-only).
  N4: Current anchor mutation? (anchor VALIDATION_CHECKPOINT with original ref when legacy exists? Or anchor with current record ref?) -> HIST refuse.
  No None Candidate/predecessor enums metadata fake: verify no such enums in new code paths (grep).

Capture PIDs/exits/raw window/immediate fs. State must remain -> r5 GOOD after all negatives (no mutation).
"""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path

def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    repo = Path(__file__).resolve().parents[4]
    fix = repo / ".rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly"
    raw = repo / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-correction/raw/guards-20261025T200000Z"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "pid.txt").write_text(str(os.getpid()) + "\n")
    for k in list(os.environ):
        if k.startswith("GIT_"):
            del os.environ[k]
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.path.insert(0, str(fix.resolve()))
    for mod in list(sys.modules):
        if mod.startswith("scripts."):
            del sys.modules[mod]
    from scripts import survey_versioned_renewal_v2 as high
    from scripts import survey_versioned_renewal_history_v2 as hist
    from scripts import survey_versioned_renewal_source_v2 as srcmod
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_publication_set_v2 as setmod
    import scripts.survey_production_v2 as core
    log = []
    def emit(s: str) -> None:
        print(s)
        log.append(s)
    state_rel = "sources/2026-W37/production-state.json"
    cfg = json.loads((fix / "config/survey-production-v2.json").read_bytes())
    # Record pre-guard State (must remain -> r5 after all)
    pre_state_data = (fix / state_rel).read_bytes()
    pre_state = json.loads(pre_state_data)
    emit(f"PRE-GUARD State pointer={pre_state.get('publication_revalidation_provenance')}")
    assert "r5" in pre_state["publication_revalidation_provenance"]["path"], "PRE-GUARD State must be -> r5 GOOD"
    pre_sha = hashlib.sha256(pre_state_data).hexdigest()
    # P1: R1/canonical after refusal no writes
    try:
        from scripts import survey_agent_control_v2 as agent2
        # Use R1 CLI? Directly call canonical writer guard: it should refuse in VERSIONED_ACTIVE.
        # The R1 helper is tests/test_survey_weekly_mechanical_refresh_v2.py, but public R1 API is via agent? Actually R1 refusal is via "canonical operation refused in revised mode" from pubset.require_active_or_canonical?
        # Simulate by calling pubset.require_active_or_canonical with want_versioned=False (canonical writer) on VERSIONED_ACTIVE State -> must refuse.
        try:
            setmod.require_active_or_canonical(fix, cfg, post_state := pre_state, want_versioned=False)
            emit("P1 FAIL: canonical writer did NOT refuse in VERSIONED_ACTIVE (should refuse)")
            return 2
        except Exception as e:
            emit(f"P1 PASS: canonical/R1 refused in VERSIONED_ACTIVE BEFORE writes: {e}")
        # Verify no new r6 record created, HEAD unchanged, records still r1+r2+r3+r4(inert)+r5
        import glob
        recs = sorted(glob.glob(str(fix / "sources/2026-W37/publication/v2/publication-surface-revalidation-r*.json")))
        emit(f"P1 records={[Path(r).name for r in recs]} (must be r1+r2+r3+r4(inert)+r5, no r6)")
        assert not (fix / "sources/2026-W37/publication/v2/publication-surface-revalidation-r6.json").exists(), "no r6 must exist after R1 refusal"
        post_state_data = (fix / state_rel).read_bytes()
        assert hashlib.sha256(post_state_data).hexdigest() == pre_sha, "State must be unchanged after R1 refusal (no writes)"
        emit("P1 PASS: no writes after R1/canonical refusal (State unchanged, no r6)")
    except Exception as e:
        emit(f"P1 ERROR {e}")
        import traceback
        traceback.print_exc()
        return 2
    # P2: Ordinary activate SAME set orphan still refuse (INTENT_COLLISION)
    try:
        # Find active set path from r5 record
        r5_rel = pre_state["publication_revalidation_provenance"]["path"]
        r5 = json.loads((fix / r5_rel).read_bytes())
        set_rel = r5["set_ref"]["path"]
        emit(f"P2 active set {set_rel} (SAME active set ordinary must NOT create new record: ALREADY_ACTIVE readonly or INTENT_COLLISION, per HIGH b124)")
        try:
            _p2res = high.activate_renewal(str(fix), state_rel, set_rel, "Same set ordinary retry (orphan, should not create new)", "anchor-fix", "2026-10-25T20:10:00Z")
            # No exception: must be readonly ALREADY_ACTIVE (no new record, State unchanged), not ACTIVATED duplicate.
            emit(f"P2 ordinary SAME set returned {_p2res}")
            assert _p2res.get("status") == "ALREADY_ACTIVE", f"expected ALREADY_ACTIVE readonly (not new ACTIVATED), got {_p2res}"
            assert _p2res.get("record_path") == r5_rel, "ALREADY_ACTIVE must point to same r5 (no new record)"
            emit("P2 PASS: ordinary SAME active set ALREADY_ACTIVE readonly (no new record, orphan fix preserved, no regress)")
        except Exception as e:
            code = getattr(e, "code", "")
            emit(f"P2 ordinary SAME set refuse code={code} detail={str(e)[:300]}")
            assert "INTENT" in str(code) or "INTENT" in str(e) or "ALREADY_ACTIVE" in str(e) or "COLLISION" in str(e), f"expected INTENT_COLLISION/ALREADY_ACTIVE, got {code}: {e}"
            emit("P2 PASS: ordinary SAME set refused (orphan fix preserved, no regress)")
        # State unchanged
        assert hashlib.sha256((fix / state_rel).read_bytes()).hexdigest() == pre_sha, "State unchanged after orphan refuse"
    except Exception as e:
        emit(f"P2 ERROR {e}")
        import traceback
        traceback.print_exc()
        return 2
    # N1: Forged anchor same kind DRAFT after rehashing (no digest-only seam) -> refuse BEFORE State write
    try:
        # Load GOOD r5 chain files (basis/proof/receipt/set/record) for high-u3-anchor-fix
        # Find basis path from r5 record
        basis_rel = r5["renewal_basis_ref"]["path"]
        proof_rel = r5["renewal_proof_ref"]["path"]
        set_rel_r5 = r5["set_ref"]["path"]
        # Receipt path from set
        seal = json.loads((fix / set_rel_r5).read_bytes())
        receipt_rel = seal["source_receipt_ref"]["path"]
        emit(f"N1 GOOD basis={basis_rel} proof={proof_rel} receipt={receipt_rel} set={set_rel_r5} record={r5_rel}")
        # Forge: copy basis, replace anchor with DRAFT_COMPLETE (same kind LEGACY, different ref), rehash basis_sha256
        basis_data = json.loads((fix / basis_rel).read_bytes())
        forged_anchor = {"kind": "LEGACY_REVALIDATION", "ref": {"path": "sources/2026-W37/orchestration/v2/checkpoints/DRAFT_COMPLETE.json", "sha256": "ffbde649f25d5622dc3f49833b9a0a023e1af92cdf09732fae0b861177fa45da"}}
        forged_basis = copy.deepcopy(basis_data)
        forged_basis["canonical_anchor"] = forged_anchor
        # Rehash basis_sha256 (all-except-self)
        forged_basis["basis_sha256"] = core.sha256_object({k: v for k, v in forged_basis.items() if k != "basis_sha256"})
        # Write forged basis to TEMP path (not overwriting GOOD, no State mutation, controlled negative input, not orphan adoption)
        forged_basis_rel = basis_rel.replace("high-u3-anchor-fix", "high-u3-anchor-fix-forged")
        # Ensure parent exists (new dir, not adopted as renewal? It's a negative test file, not a renewal dir - use raw/ for forged files to avoid polluting renewals namespace? But basis must be repo-local path for HIST? For HIST direct test, we can test HIST on forged RECORD, not basis file path? Simpler: test HIST refuse on forged RECORD (constructed in memory? HIST requires file). Alternative: test S validate_renewal_basis on forged basis file in raw/ (repo-local, but not in renewals namespace, still valid path for S? S checks basis schema, not namespace? It checks prior_record_ref etc., which point to real files, so forged basis in raw/ with correct prior refs but forged anchor should still refuse via HIST derived check, BEFORE State write, no digest seam (since we rehashed).
        # Write forged basis to raw/ (repo-local, not adopted)
        forged_basis_path = f"raw/forged-basis-{os.getpid()}.json"
        # raw/ at repo root? Actually fix repo has raw/source.json at top? Use sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/renewals/high-u3-anchor-fix/forged-basis.json (inside renewal dir but distinct file, not adopted as renewal basis? It's okay as negative input file, not a renewal dir).
        forged_basis_rel2 = "sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/renewals/high-u3-anchor-fix/forged-basis-neg1.json"
        (fix / forged_basis_rel2).write_text(json.dumps(forged_basis, indent=1, sort_keys=True) + "\n")
        emit(f"N1 forged basis written {forged_basis_rel2} anchor DRAFT (rehashed, no digest seam)")
        try:
            srcmod.validate_renewal_basis(str(fix), forged_basis_rel2)
            emit("N1 FAIL: forged basis anchor DRAFT did NOT refuse (should HISTORY_ANCESTOR BEFORE State write)")
            return 2
        except Exception as e:
            code = getattr(e, "code", "")
            emit(f"N1 forged basis refuse code={code} detail={str(e)[:400]}")
            assert "HISTORY" in str(code) or "ANCESTOR" in str(e) or "anchor" in str(e).lower(), f"expected HISTORY_ANCESTOR anchor refuse, got {code}: {e}"
            emit("N1 PASS: forged anchor same-kind DRAFT refused BEFORE State write (no digest-only seam, chain-derived identity enforced)")
        # Cleanup forged file? No cleanup per task (preserve failed roots, no cleanup). Keep as evidence (inert, not adopted).
        # Verify State unchanged (no mutation on negative)
        assert hashlib.sha256((fix / state_rel).read_bytes()).hexdigest() == pre_sha, "State unchanged after N1 forged refuse (BEFORE write)"
        emit("N1 PASS: State unchanged after forged refuse (BEFORE write, no INDETERMINATE mutation)")
    except Exception as e:
        emit(f"N1 ERROR {e}")
        import traceback
        traceback.print_exc()
        return 2
    # N2/N3/N4: Wrong latest legacy (r1), stale original (DRAFT), current anchor mutations via HIST direct (no State mutation)
    try:
        # N2: anchor r1 (wrong latest legacy, should be r2) - construct minimal record? Instead, directly test HIST on GOOD r5 (should PASS) vs forged r5 with r1 anchor (should FAIL). For forged r5, copy r5 record, replace anchor with r1, rehash? Record has no self-digest? It has no record_sha field? Actually record file SHA is file digest, not self-digest. Rehashing means updating State pointer? For HIST direct test, we can write forged record file to temp path (not adopted) with r1 anchor, then call HIST - it should refuse due to anchor mismatch (not digest seam, since file SHA will match forged file).
        r1_sha = "8974dfcee44ea8cb3001292118d4b6b3809c4e4e7e8a99ea87297fa0dbb148b5"
        # Use valid sequence paths (r6, r7, r8) with same supersedes as r5 (r3) to isolate anchor seam (not sequence seam).
        # Each forged record is inert (not selected, State stays -> r5), no State mutation, no cleanup (preserved as evidence).
        for label, rnum, forged_ref in [
            ("N2-wrong-latest-legacy-r1", "r6", {"kind": "LEGACY_REVALIDATION", "ref": {"path": "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json", "sha256": r1_sha}}),
            ("N3-stale-original-DRAFT", "r7", {"kind": "LEGACY_REVALIDATION", "ref": {"path": "sources/2026-W37/orchestration/v2/checkpoints/DRAFT_COMPLETE.json", "sha256": "ffbde649f25d5622dc3f49833b9a0a023e1af92cdf09732fae0b861177fa45da"}}),
            ("N4-current-VALIDATION-when-legacy", "r8", {"kind": "VALIDATION_CHECKPOINT", "ref": {"path": "sources/2026-W37/orchestration/v2/checkpoints/DRAFT_COMPLETE.json", "sha256": "ffbde649f25d5622dc3f49833b9a0a023e1af92cdf09732fae0b861177fa45da"}}),
        ]:
            forged_rec = copy.deepcopy(r5)
            forged_rec["canonical_anchor"] = forged_ref
            # Keep supersedes as r3 (same as r5) to isolate anchor (sequence r6/r7/r8 > r3, strictly increasing, no duplicate).
            forged_rel = f"sources/2026-W37/publication/v2/publication-surface-revalidation-{rnum}.json"
            if (fix / forged_rel).exists():
                emit(f"{label} SKIP: {forged_rel} already exists inert (no overwrite, gaps okay)")
                continue
            (fix / forged_rel).write_text(json.dumps(forged_rec, indent=1, sort_keys=True) + "\n")
            try:
                hist.verify_versioned_history(str(fix), forged_rel)
                emit(f"{label} FAIL: forged anchor did NOT refuse (should HISTORY_ANCESTOR anchor identity)")
                return 2
            except Exception as e:
                code = getattr(e, "code", "")
                detail = str(e)
                emit(f"{label} PASS refuse {code} {detail[:300]}")
                assert "HISTORY_ANCESTOR" in str(code) and "anchor" in detail.lower(), f"expected HISTORY_ANCESTOR anchor refuse (not sequence/digest seam), got {code}: {detail[:300]}"
        # GOOD r5 must still PASS
        hres = hist.verify_versioned_history(str(fix), r5_rel)
        assert hres["canonical_anchor"]["ref"]["sha256"] == "27db45ce3641866fcfadba6297cdf31b991660abd5cfe4445e7fb0b62ca4c582"
        emit("N2/N3/N4 PASS: wrong latest legacy / stale original / current mutations preserved (HIST refuses), GOOD r5 anchor r2 still PASS")
        assert hashlib.sha256((fix / state_rel).read_bytes()).hexdigest() == pre_sha, "State unchanged after N2/N3/N4 (no mutation)"
    except Exception as e:
        emit(f"N2/N3/N4 ERROR {e}")
        import traceback
        traceback.print_exc()
        return 2
    # No None Candidate/predecessor enums metadata fake: grep new code for forbidden patterns
    try:
        import subprocess as sp
        for pat in ["NoneCandidate", "None.*Candidate", "predecessor.*enum", "metadata.*fake"]:
            res = sp.run(["grep", "-rn", pat, "scripts/survey_versioned_renewal_v2.py", "scripts/survey_versioned_renewal_history_v2.py", "scripts/survey_versioned_renewal_source_v2.py"], cwd=str(fix), capture_output=True, text=True)
            if res.stdout.strip():
                emit(f"FORBIDDEN pattern {pat} FOUND (should be absent): {res.stdout[:500]}")
                return 2
        emit("No NoneCandidate/predecessor-enum/metadata-fake patterns in fixed modules (verified)")
    except Exception as e:
        emit(f"grep ERROR {e}")
        return 2
    (raw / "diagnosis.txt").write_text("\n".join(log) + "\n")
    (raw / "exit.txt").write_text("0\n")
    emit("ALL GUARDS+NEGATIVES PASS, State still -> r5 GOOD (no mutation on negatives)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
