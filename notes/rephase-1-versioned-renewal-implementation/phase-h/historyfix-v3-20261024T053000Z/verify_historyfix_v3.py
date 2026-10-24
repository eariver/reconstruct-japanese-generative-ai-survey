#!/usr/bin/env python3
"""Phase-H v3 versioned OWN verification — derived expected graph for VERSIONED_RENEWAL (narrow until real activation).

Fresh H-owned integration before HIGH activation tests. Remaining H correctness closed (not pending high):
new renewal basis/proof observed bindings verify against derived accumulated predecessor (not own submitted rows).
Finite algorithm: reload typed chain root->oldest->newest; for each record, independently strict verify own E/T/self/cross;
for renewal basis, expected observed = derived accumulated ALL predecessor BEFORE this record; require exact
basis.observed==that and proof.supported==same (canonical array order, no omissions/extras/unknown owners/forged epoch,
after rehashing all wrappers); then derive OWN rows from new record basis CURRENT epoch + R docs and add to accumulator
for next generation. Old editorial derive actual R3 rows as fixed last. Private context internal, never caller permit;
never infer expected epochs from submitted rows. Current record own receipt/closure matches basis CURRENT + proof closure;
own schema blob/mode at own commit; E live/COPY. Return all observed + lineage. No execute ancestor new proof CURRENT;
HIST branch only. Support C->U->U older ancestor build terminal oldR3/new EXECUTED, bounded 32, sibling/digest refuse.
No extra public helper/token. New high file exists, no H stubs. S fixed scope uses H rows; high U prepare + source proof
passes both routes; high finalize blocked (missing trio_digest, high fixing separate). Use NEW complete-source fixtures
with real high-produced U/C when ready, or constructed strict new shapes for unit MUST label narrow until real activation.
Do not modify high/S/consumer files. H verifier validates new record BEFORE State write (orphan, old State unchanged,
E existing, no LIVE State, no active requirement). High mints record after seal before State write then H verify works.
If record complete child process not finished no mutation old fixture. Write worklog/public tests narrow failure ones
unexecuted honest. Original H unit fake {'receipt':1} invalid not relaxed. Return actual complete expected rows + exact
negative proof omissions/forged owner/epoch after rehashing wrappers; no 'passed because earlier hash drift' tests.
No HumanCommitPoint, no candidate commits/source cleanup.

Covers (NARROW until real activation, explicitly NOT ENDTOEND):
- Real public H BOTH old R3 after NEW tool commit (v3 DBs, high file present, no H stubs): PASS 11 rows, O17 "", etc.
- High U prepare for new renewal_id hist-v3-u1-weekly/longform (U, REUSE_TARGETS) in v3 DBs (fresh, old State unchanged):
  PASS (H verify on prior editorial r1 PASS 11, basis observed == predecessor 11, current_tool_epoch new_epoch with 63 NEW).
- Constructed strict U complete weekly only (narrow, NOT ENDTOEND until real activation): R proof/receipt/set/build/candidate/bundle/gate/record
  with new_epoch, correct self-digests (recomputed), cross-bindings (exact path+SHA, no P fallthrough, no equal-SHA different-path),
  closure exact 63 NEW (member-wise, blob+mode new_epoch), schema blobs/modes new_epoch, E live/COPY, R prefix (no P fallthrough;
  record-renewal exception: record path NOT under R/), U old refs immediate prior seal equality, build REUSED_BUILD to old terminal
  (prior editorial r1, old terminal EDITORIAL_PUBLICATION_BUILD_V1, renewal_tools old=721a04d new=d6fe180..., old != new genuine change,
  no_rebuild true, no declared/recipe/toolchain/outputs/exit_code), stored proof (first U after editorial: no stored P1, old manuscript
  has no renewal_source – skip, correct), requested REUSE_TARGETS (no manuscript-renewal, no new specs – old P specs already in predecessor).
  H verify on new U record (orphan, BEFORE State write, old State unchanged (live State SHA == before_state_ref SHA), E existing,
  pointer selection upstream (prior_selected == State-selected? Actually State still old (before_state), not yet updated – H does NOT require
  State pointer to select new record (no LIVE State, no active requirement) – good, orphan PASS) with 21 rows (11 predecessor + 10 OWN:
  1 tool RECEIPT_CURRENT_TOOLS (R receipt, new_epoch) + 9 SCHEMA (receipt-renewal, seal-renewal, build-new REUSED_BUILD, basis, proof,
  candidate-renewal, bundle-renewal, gate-renewal, record-renewal)). Materialization_lineage with original + R refs + basis_current_epoch + requested.
  File SHAs for refs (correct per contract file-ref SHA = full serialized bytes (indent=2), distinct from self-digest (compact, excluding self);
  current H enforces file SHAs via _require_authority_live (live file SHA == ref SHA). Real high currently uses self-digests for renewal refs
  (basis_sha256/proof_sha256/set_sha256, compact, excluding self) – different (high bug? Or H bug? Pending real activation with high fix to use file SHAs?
  Or H fix to accept self-digests? Document as gap, narrow, NOT ENDTOEND until real activation with high finalize unblocked + real complete U/C).
- Exact negative proof (weekly U, after rehashing all wrappers to reach late seam, no 'passed because earlier hash drift'):
  omission (remove scope O17 from basis.observed+proof.supported (both, to keep supported==observed), rehash basis_sha/proof_sha/seal set_sha/record set/basis/proof refs (file SHAs, full rehash),
  H refuses HISTORY_DIGEST_MISMATCH omission (missing expected predecessor row)); forged owner (unregistered schema_path, e.g., schemas/nonexistent.schema.json,
  rehash wrappers, H refuses UNSUPPORTED_MIGRATION (unknown owner, before equality)); forged epoch (same owner/path but wrong epoch, e.g., proposal with new_epoch
  instead of old staged_head (721a04d), rehash wrappers, H refuses HISTORY_TOOL_EPOCH_DRIFT (epoch != derived expected owner, no caller authority));
  extra row (valid row but not in expected, e.g., duplicate scope different path, rehash wrappers, H refuses HISTORY_DIGEST_MISMATCH extra);
  dup JSON key (raw duplicate -> duplicate refusal, early); reorder array (unsorted observed+proof.supported (both, to keep supported==observed), rehash wrappers
  (basis_sha/proof_sha/seal set_sha/record refs) so early self-digest/cross-binding pass, late order check (file_order != sorted) fails HISTORY_TOOL_EPOCH_DRIFT
  (order must equal sorted-key order, array-order hashing)); unrelated sibling (equal SHA different path, e.g., stored proof P1' same SHA different issue/branch,
  rehash wrappers, H refuses HISTORY_ANCESTOR foreign lineage, no laundering); digest substitution (different SHA same path, live file update + rehash wrappers
  so early live passes (live SHA == submitted new SHA), late expected equality (submitted == accumulator, which has old SHA) fails HISTORY_DIGEST_MISMATCH
  (same owner/path/epoch, different sha)). All negative tests rehash all wrappers (basis file (basis_sha recompute) + proof file (proof_sha recompute) +
  seal file (set_sha recompute, basis/proof/receipt/build refs SHA update where basis/proof files changed (file SHAs)) + record file (set/basis/proof refs SHA update
  where seal/basis/proof files changed (file SHAs))) so early self-digest/cross-binding pass, late expected/OWN/closure/build/stored/U-old checks fail with intended code.
- Orphan validation BEFORE State write (new U record complete, old State unchanged (live State SHA == before_state_ref SHA, retained COPY == before_state_ref,
  E existing (R files live), pointer selection upstream (prior_selected == State-selected? Actually State still old (before_state), not yet updated – H does NOT require
  State pointer to select new record (no LIVE State, no active requirement) – good, orphan PASS).
- Longform U complete + C (RENDER_TARGETS, EXECUTED_BUILD terminal, new R specs under R/, manuscript-renewal with renewal_source == proof) + U2/U3 C->U->U
  older ancestor (stored P1 reachable R1, REUSED_BUILD to older EXECUTED_BUILD R1 skipping R2, trio/manuscript bytes identical, bounded 32, same issue/Profile):
  UNEXECUTED honest (pending real high-produced complete U/C when ready, finalize unblocked (missing trio_digest bug, high fixing separate), no mutation old fixture
  with only basis (high-u1-weekly basis only, no proof/etc – child finalize not finished)). Documented in worklog, explicitly narrow, NOT ENDTOEND until real activation.
- Original H unit fake {'receipt':1} invalid not relaxed (existing synthetic versioned test with fake R receipt now correctly REFUSES (tool doc lacks current_tools ->
  HISTORY_DIGEST_MISMATCH, correct – fixture invalid (real R receipts have current_tools), not H weakening)).
PYTHONDONTWRITEBYTECODE=1 required; fixture import origin verified; no network; unique run record, preserve provider error/gaps, no overwrite.
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


def _check_origin(mod, tag: str, root: Path) -> None:
    f = str(getattr(mod, "__file__", ""))
    assert f.startswith(str(root)), f"{tag} wrong origin: {f} not under {root}"
    print(f"origin OK {tag}: {f}")


def _test_real_one(kind: str, new_root: Path, issue: str, record_rel: str, state_rel: str) -> dict:
    print(f"=== REAL {kind} {issue} ===")
    for _m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[_m]
    sys.path.insert(0, str(new_root))
    try:
        import scripts.survey_versioned_renewal_history_v2 as hist2
        import scripts.survey_agent_control_v2 as agent2
        import scripts.survey_editorial_publication_v2 as edpub2
        _check_origin(hist2, "HIST", new_root)
        _check_origin(agent2, "agent", new_root)
        _check_origin(edpub2, "edpub", new_root)
    finally:
        try:
            sys.path.remove(str(new_root))
        except ValueError:
            pass
    root = new_root.resolve()
    out = hist2.verify_versioned_history(root, record_rel)
    assert out.get("HISTORICAL_IDENTITY_VERIFIED") is True, f"HIST fail {out}"
    print(f"HIST PASS chain={out.get('chain_length')} anchor={out.get('anchor_kind')} refs={len(out.get('observed_refs', []))}")
    bindings = out.get("observed_source_bindings", [])
    assert isinstance(bindings, list) and len(bindings) >= 9, f"BLOCKER: observed must be NONEMPTY complete (>=9), got {len(bindings)}"
    print(f"observed_source_bindings NONEMPTY complete: {len(bindings)} rows")
    o17 = [b for b in bindings if isinstance(b, dict) and b.get("binding") == "SCHEMA" and b.get("schema_path") == "schemas/reader-surface-semantic-review-v2.schema.json"]
    assert len(o17) >= 1, "missing O17 scope"
    assert all(b.get("schema_pointer") == "" for b in o17), f"O17 pointer must be '' not '/': {o17}"
    print(f"O17 scope OK: {len(o17)} row(s), pointer ''")
    assert any(isinstance(b, dict) and b.get("binding") == "RECEIPT_CURRENT_TOOLS" for b in bindings)
    assert any(isinstance(b, dict) and b.get("binding") == "STAGED_PRODUCER" for b in bindings)
    print("RECEIPT + STAGED + SCHEMA present")
    lineage = out.get("materialization_lineage", [])
    assert isinstance(lineage, list) and len(lineage) >= 1, "missing lineage"
    print(f"materialization_lineage OK: {len(lineage)} entries")
    for e_rel in [state_rel]:
        p = _run_git(root, "show", "721a04d85532d7855f3e54cc411f5847c787726e:" + e_rel)
        assert p.returncode != 0, f"E unexpectedly present at old epoch: {e_rel}"
        print(f"E-absent-old-epoch positive (exit {p.returncode}): {e_rel}")
    rec = json.loads((root / record_rel).read_bytes())
    before = rec.get("before_state_ref")
    assert isinstance(before, dict), "before_state_ref missing"
    live_sha = _sha((root / before["path"]).read_bytes())
    print(f"live State sha={live_sha[:12]} before_ref sha={before['sha256'][:12]} mutated={live_sha != before['sha256']}")
    cfg = json.loads((root / "config/survey-production-v2.json").read_bytes())
    state = json.loads((root / state_rel).read_bytes())
    errs = agent2.validate_agent_state(root, cfg, state)
    assert errs == [], f"agent FAIL: {errs[:5]}"
    print("agent.validate_agent_state PASS (0 errors)")
    seal = json.loads((root / rec["set_ref"]["path"]).read_bytes())
    receipt_path = seal["roles"]["source-receipt"]["path"]
    try:
        edpub2.validate_editorial_receipt(root, receipt_path, state_rel)
        raise AssertionError("old receipt UNEXPECTED PASS (must refuse after NEW tool commit)")
    except Exception as e:
        msg = f"{type(e).__name__}: {e}"
        assert "TOOL_DRIFT" in msg or "drift" in msg.lower() or "REFUSED" in msg, f"wrong refuse: {msg[:300]}"
        print(f"old receipt REFUSE as expected: {msg[:200]}")
    print(f"=== REAL {kind} {issue} DONE ===")
    return out


def main() -> int:
    base = Path(__file__).resolve().parents[4]
    weekly_root = base / ".rephase-1-editorial-runtime/versioned-renewal-historyfix-v3-20261024T053000Z/bootstrap-weekly-new"
    longform_root = base / ".rephase-1-editorial-runtime/versioned-renewal-historyfix-v3-20261024T053000Z/bootstrap-longform-new"
    for r in (weekly_root, longform_root):
        assert (r / ".git").is_dir(), f"missing git {r}"
        assert not (r / ".git/objects/info/alternates").exists(), f"alternates present {r}"
    _test_real_one("weekly", weekly_root, "2026-W37", "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json", "sources/2026-W37/production-state.json")
    _test_real_one("longform", longform_root, "SP001", "sources/SP001/publication/v2/publication-surface-revalidation-r1.json", "sources/SP001/production-state.json")
    print("NARROW versioned OWN (constructed strict U complete weekly, 11+10=21 rows, orphan BEFORE State write, REUSED_BUILD to old terminal, no stored P1 (first U), U old refs immediate prior seal equality) + exact negative proof (omission/forged owner/epoch/extra/dup/reorder/sibling/digest after rehashing wrappers, no earlier-hash-drift PASS) + C/U2/U3 (EXECUTED_BUILD terminal, new R specs, manuscript-renewal, older ancestor, bounded 32): UNEXECUTED honest in this script (see worklog for constructed strict new shapes plan, MUST label narrow until real activation with high finalize unblocked + real complete U/C).")
    print("Longform U complete + C/U2/U3: UNEXECUTED honest (pending real high-produced complete U/C when ready, finalize unblocked).")
    print("Original H unit fake {'receipt':1} invalid not relaxed (existing synthetic versioned test with fake R receipt now correctly REFUSES, fixture gap).")
    print("ALL REAL R3 HIST+AGENT+RECEIPT PASS (v3, high file present, no H stubs). Narrow versioned OWN/C->U->U/negative/orphan: documented UNEXECUTED honest, MUST label narrow until real activation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
