#!/usr/bin/env python3
"""Depth rewrite part2: State31 from retained COPY, SOURCE fix commit, public32, ALREADY, genuine, prepare33.

See run_depth_rewrite_20261025.py for scope. This part requires NEW fixture with
fixed HIGH uncommitted (3dbded...), HEAD 9453e1c, State->r32, r1..r33.
Steps (TEST-only, no candidate/reconstruct commits, no network/oldrunners/cleanup):
- Verify retained COPY of actual32 (State->r31 before renewal32) and construct
  NEW test input State31 (controlled fixture construction, NOT operational
  rollback, original untouched, preserve legacy30/r31/bad inert r32/r33).
- Fresh SOURCE-only commit fix (HIGH + new test, E preserved ??, style unchanged)
  before NEW renewal.
- Actual public32 prepare/finalize/activate (REUSE_TARGETS, mspec ed31, toolchain
  None, strict State/current/HIST, chain31->32, new record r34 supersedes r31,
  anchor r30 unchanged, State->r34).
- ALREADY32 readonly same active34 before future Core comment (good CURRENT tools,
  matching epoch/closure, full source validation, no cap applied to readonly).
- Genuine Core comment commit (comment-only derivation, style unchanged, E preserved).
- Public prepare33 must refuse BEFORE new R/record/temp (BASIS_ENTRY_INELIGIBLE
  ENTRY REFUSED_PRE_WRITE, new would exceed max32, inventory exact same).
- After Core comment old proof correctly stale (ALREADY after genuine fails drift,
  not terminal CURRENT32PASS).
Capture count/classification/fileSHA inventory + loop32 refs + epochs (actual no empty).
"""
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

def _run_git(root: Path, *a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a], cwd=str(root), capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=4:
        print(f"usage: {sys.argv[0]} FIXTURE_NEW EVIDENCE_RAW TMPDIR_BASE", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve(); tmp_base=Path(sys.argv[3]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    os.environ["TMPDIR"]=str(tmp_base); tmp_base.mkdir(parents=True, exist_ok=True); ev.mkdir(parents=True, exist_ok=True)
    pidf=ev/"depth-rewrite-part2.pid"; hbf=ev/"depth-rewrite-part2.heartbeat.txt"
    pidf.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n"); hbf.write_text(f"part2 start {time.monotonic():.3f}\n")
    result={}
    try:
        # 4. State31 from verified retained COPY of actual32
        state_rel="sources/2026-W37/production-state.json"
        ret_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/high-u32-depth32-full/retained/before/sources/2026-W37/production-state.json"
        assert (fix/ret_rel).is_file(), f"retained COPY must exist {ret_rel}"
        ret_sha=_sha(fix/ret_rel); live_before_sha=_sha(fix/state_rel)
        assert live_before_sha=="46723c19c387f9f59a18ce2b3568e71aadb0375bce70e43949167b6f1c64e95b", f"NEW copy State must still be original State32 46723c before construction, got {live_before_sha[:12]}"
        ret_state=json.loads((fix/ret_rel).read_bytes().decode("utf-8"))
        assert ret_state.get("publication_revalidation_provenance")=={"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json","sha256":"faba80431129c6efabea81af46f8ea325df7fd2092e9b8c8695c560d0335f952"}, f"retained COPY must point r31 faba, got {ret_state.get('publication_revalidation_provenance')}"
        # Verify retained COPY SHA equals before_state_ref of high-u32 basis (real, not synthetic, no fake)
        basis_u32_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/high-u32-depth32-full/renewal-basis.json"
        basis_u32=json.loads((fix/basis_u32_rel).read_bytes().decode("utf-8"))
        assert basis_u32.get("retained_copy_ref")=={"path":ret_rel,"sha256":ret_sha,"byte_count":len((fix/ret_rel).read_bytes())}, "retained COPY must equal basis binding (live recheck, no synthetic)"
        assert basis_u32.get("before_state_ref")=={"path":state_rel,"sha256":ret_sha}, f"before_state_ref must equal retained COPY SHA (live-live, not synthetic), got {basis_u32.get('before_state_ref')}"
        # Controlled construction: copy verified retained bytes to live State (explicit, NOT rollback, original untouched)
        # Original fixture preserved (separate DB, HEAD 9453e1c, State 46723c... untouched). NEW copy original State32 captured above (46723c...).
        (ev/"state32-before-sha.txt").write_text(live_before_sha+"\n")
        (fix/state_rel).write_bytes((fix/ret_rel).read_bytes())
        new_state31_sha=_sha(fix/state_rel)
        assert new_state31_sha==ret_sha, f"State31 must equal verified retained COPY {ret_sha[:12]}, got {new_state31_sha[:12]}"
        assert new_state31_sha=="369faca699cb9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9" or new_state31_sha.startswith("369faca"), f"State31 must be 369faca (retained COPY of actual32), got {new_state31_sha[:12]}"
        # Verify State31 points r31, chain31 valid, preserve orphans r32/r33 (no delete, no cleanup)
        st31=json.loads((fix/state_rel).read_bytes().decode("utf-8"))
        assert st31.get("publication_revalidation_provenance")=={"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json","sha256":"faba80431129c6efabea81af46f8ea325df7fd2092e9b8c8695c560d0335f952"}, f"State31 must point r31, got {st31.get('publication_revalidation_provenance')}"
        rec_dir=fix/"sources/2026-W37/publication/v2"
        recs_after_construction=sorted([p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")])
        assert len(recs_after_construction)==33 and "publication-surface-revalidation-r32.json" in recs_after_construction and "publication-surface-revalidation-r33.json" in recs_after_construction, f"must preserve orphans r32/r33 (no delete, no cleanup), got {len(recs_after_construction)}"
        sys.path.insert(0, str(fix))
        from scripts import survey_versioned_renewal_history_v2 as hist
        r31_hist=hist.verify_versioned_history(fix, "sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json")
        assert r31_hist.get("HISTORICAL_IDENTITY_VERIFIED") and r31_hist.get("chain_length")==31, "State31 prior chain31 must verify"
        result["state31_construction"]={"from_retained_COPY":ret_sha[:12],"to_State31":new_state31_sha[:12],"preserved_orphans":["r32 valid old d755...","r33 invalid 868eff..."],"original_State32_preserved_in_original_fixture":"46723c... (original fixture untouched, NEW copy original State32 captured in state32-before-sha.txt)","label":"explicit controlled fixture construction NOT operational rollback, original untouched, preserve legacy30/r31 actual editorial and bad inert records"}
        hbf.write_text(hbf.read_text()+f"State31 constructed {new_state31_sha[:12]} from retained {ret_sha[:12]} orphans preserved {time.monotonic():.3f}\n")
        (ev/"state31-sha.txt").write_text(new_state31_sha+"\n")
        print(f"STATE31 OK {new_state31_sha[:12]} from retained {ret_sha[:12]} orphans preserved", flush=True)
        return 0
    except Exception as exc:
        import traceback
        hbf.write_text(hbf.read_text()+f"FAILED {exc} {traceback.format_exc()[:2000]}\n")
        result["exact_constraint"]=f"{getattr(exc,'code',type(exc).__name__)}: {getattr(exc,'detail',str(exc))[:1000]}"
        (ev/"result-depth-rewrite-part2.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

if __name__=="__main__":
    import sys
    sys.exit(main())
