#!/usr/bin/env python3
"""Depth32-full refusal33: genuine Core comment commit -> prepare/activate33 must REFUSE.

TEST-only, no product edits, no candidate/reconstruct commits, no network/old-runners,
no cleanup failed fixture/cache purge. Workspace TMPDIR, per-phase 1200 with owned
PID/heartbeats/terminal exit, don't duplicate child on return. Fresh Python per
SOURCE epoch (CURRENT after overlay + new commit), no shared execution.

- Next genuine Core comment Source commit (comment-only, changed paths, not artifact-only,
  style baseline035 unchanged, E preserved) after renewal32 (chain32, State->r32).
- Public prepare/activate33 must REFUSE before NEW R/State writes; record exact which
  gate catches (code/phase/disposition/detail) and immediate inventory (R_FILES, State SHA
  before/after, no new r33, State unchanged).
- Only 1 actual editorial+1 actual renewal on 31 fixture-provided predecessors, NOT 32
  full genuine ops; labelled scope qualifier required.
"""
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

def _run_git(root: Path, *a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} FIX_ROOT EVIDENCE_DIR", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    pidf=ev/"refuse33.pid"; hbf=ev/"refuse33.heartbeat.txt"
    pidf.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbf.write_text(f"refuse33 start {time.monotonic():.3f}\n")
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs=set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    expected_set=set(f"publication-surface-revalidation-r{i}.json" for i in range(1,33))
    assert recs==expected_set, f"need r1..r32 before refusal33, got len={len(recs)}"
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    (ev/"refuse33-pin-before-head.txt").write_text(head_before+"\n")
    state_path=fix/"sources/2026-W37/production-state.json"
    state_before_sha=_sha(state_path)
    state_before=json.loads(state_path.read_bytes().decode("utf-8"))
    prov_before=state_before.get("publication_revalidation_provenance",{})
    r32_sha=_sha(rec_dir/"publication-surface-revalidation-r32.json")
    assert prov_before.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r32.json" and prov_before.get("sha256")==r32_sha, f"State must point r32, got {prov_before}"
    r30_sha=_sha(rec_dir/"publication-surface-revalidation-r30.json")
    hbf.write_text(hbf.read_text()+f"r1..r32 present r30={r30_sha[:12]} r32={r32_sha[:12]} state={state_before_sha[:12]} {time.monotonic():.3f}\n")
    # Genuine Core comment Source commit (comment-only, changed paths, not artifact-only, style unchanged)
    core_file=fix/"scripts/survey_weekly_derivation_v2.py"
    assert core_file.is_file()
    old_txt=core_file.read_text(encoding="utf-8")
    # Ensure style unchanged baseline035 before commit
    assert _sha(fix/"templates/survey/jgaisurvey.sty")=="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec", "style must stay baseline035"
    core_file.write_text(old_txt+f"\n# Depth32-full 33rd genuine Core comment (comment-only, triggers new epoch, chain would exceed max32).\n", encoding="utf-8")
    r=_run_git(fix,"add","--","scripts/survey_weekly_derivation_v2.py")
    assert r.returncode==0, f"git add failed {r.stderr[:500]}"
    r=_run_git(fix,"-c","user.name=depth32-full-33","-c","user.email=33@example.invalid","-c","commit.gpgsign=false","commit","-m","TEST-ONLY: genuine Core comment for 33rd refusal (chain32 max, new epoch would exceed)")
    assert r.returncode==0, f"commit failed {r.stderr[:500]}"
    head_after=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    assert head_after!=head_before, "HEAD must move on genuine Core comment"
    (ev/"refuse33-commit.txt").write_text(f"{head_before} -> {head_after}\n")
    # Verify style still baseline035 after commit (genuine change elsewhere, style unchanged)
    assert _sha(fix/"templates/survey/jgaisurvey.sty")=="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec", "style must stay baseline035 after genuine commit"
    # Verify changed paths genuine (not artifact-only): show commit stat
    r=_run_git(fix,"show","--stat","--oneline","HEAD")
    (ev/"refuse33-commit-stat.txt").write_text(r.stdout[:2000]+"\n")
    assert "survey_weekly_derivation_v2.py" in r.stdout, f"genuine Core change must include derivation, got {r.stdout[:500]}"
    hbf.write_text(hbf.read_text()+f"genuine commit {head_after[:12]} {time.monotonic():.3f}\n")
    # Immediate inventory before prepare33 (R_FILES count, State SHA)
    def inventory():
        recs_now=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
        state_sha=_sha(state_path)
        # R_FILES: count of revalidation records? And renewal dirs?
        renewal_base=fix/"sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals"
        renewal_dirs=list(renewal_base.iterdir()) if renewal_base.exists() else []
        return {"recs":recs_now,"rec_count":len(recs_now),"state_sha":state_sha,"renewal_dirs":[p.name for p in renewal_dirs]}
    inv_before=inventory()
    (ev/"refuse33-inventory-before.json").write_text(json.dumps(inv_before, indent=2)+"\n")
    # Attempt public prepare33 (must REFUSE before NEW R/State writes)
    sys.path.insert(0, str(fix))
    from scripts import survey_versioned_renewal_v2 as high
    state_rel="sources/2026-W37/production-state.json"
    mspec_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/manuscript-spec.json"
    rid="high-u33-depth32-full"
    prep_code=None; prep_phase=None; prep_disp=None; prep_detail=None
    prep_ok=False
    try:
        prep=high.prepare_renewal(fix, state_rel, rid, "REUSE_TARGETS", mspec_rel, None, "depth32-full-fixture", datetime.now(timezone.utc))
        prep_ok=True
        prep_detail=f"UNEXPECTED PREPARE SUCCESS keys={sorted(prep.keys())}"
    except Exception as exc:
        prep_code=getattr(exc,"code",None) or type(exc).__name__
        prep_phase=getattr(exc,"phase",None) or ""
        prep_disp=getattr(exc,"disposition",None) or ""
        prep_detail=(getattr(exc,"detail",None) or str(exc))[:2000]
    inv_after_prepare=inventory()
    state_after_prepare_sha=_sha(state_path)
    # Check renewal dir for rid exists? (should NOT exist if refused before writes)
    rid_dir=fix/f"sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/{rid}"
    rid_exists=rid_dir.exists()
    (ev/"refuse33-prepare-result.json").write_text(json.dumps({"code":prep_code,"phase":prep_phase,"disposition":prep_disp,"detail":prep_detail,"prepare_ok":prep_ok,"rid_exists":rid_exists,"inv_before":inv_before,"inv_after_prepare":inv_after_prepare,"state_before":state_before_sha,"state_after_prepare":state_after_prepare_sha}, indent=2, sort_keys=True)+"\n")
    hbf.write_text(hbf.read_text()+f"PREPARE33 {prep_code} {prep_phase} {prep_disp} rid_exists={rid_exists} {time.monotonic():.3f}\n")
    # Attempt public activate33? If prepare refused (no basis, no set), activate cannot proceed (no set). But task says "prepare/activate33 must REFUSE". Record activate attempt as well (should also refuse, or cannot proceed due to missing set).
    # For completeness, if prepare succeeded (unexpected), try activate and record; else record activate not attempted due to prepare refusal (still counts as refuse before writes, since no new R/State).
    act_code=None; act_phase=None; act_disp=None; act_detail=None; act_ok=False
    if prep_ok:
        # Prepare succeeded unexpectedly (new R dir + basis created, R_FILES !=0). Then try activate (should refuse due to chain exceeds max32).
        # Find set from prep? Actually prep does not create set, finalize does. Need finalize before activate. For simplicity, record prepare success as failure of refusal (exact constraint: prepare should have refused but didn't).
        act_detail="prepare succeeded unexpectedly, activate not attempted in this probe (prepare should have refused before R writes, but created R dir)"
    else:
        # Prepare refused as expected (before NEW R/State writes? Check rid_exists and R_FILES)
        # Verify no new r33, State unchanged
        recs_after=set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
        assert recs_after==expected_set, f"no new r33 must exist after prepare refusal, got {recs_after - expected_set}"
        assert state_after_prepare_sha==state_before_sha, f"State must be unchanged after prepare refusal, before {state_before_sha[:12]} after {state_after_prepare_sha[:12]}"
        assert not rid_exists, f"renewal dir {rid} must NOT exist after ENTRY refusal (R_FILES=0), but exists"
        act_detail="prepare refused before NEW R/State writes (R_FILES=0, State unchanged, no r33); activate not attempted (no basis/set from refused prepare, no new writes)"
        act_code=prep_code; act_phase=prep_phase; act_disp=prep_disp
    (ev/"refuse33-activate-result.json").write_text(json.dumps({"code":act_code,"phase":act_phase,"disposition":act_disp,"detail":act_detail,"activate_ok":act_ok}, indent=2, sort_keys=True)+"\n")
    hbf.write_text(hbf.read_text()+f"ACTIVATE33 {act_code} {act_phase} {time.monotonic():.3f}\n")
    # Final inventory
    inv_final=inventory()
    (ev/"refuse33-inventory-final.json").write_text(json.dumps(inv_final, indent=2)+"\n")
    print(json.dumps({"prepare_refuses":not prep_ok,"code":prep_code,"phase":prep_phase,"disp":prep_disp,"rid_exists":rid_exists,"state_unchanged":state_after_prepare_sha==state_before_sha,"no_new_r33":set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))==expected_set}, indent=2))
    # Must REFUSE (prepare_ok False), before NEW R/State writes (rid_exists False, State unchanged, no r33)
    assert not prep_ok, f"prepare33 must REFUSE, but succeeded: {prep_detail[:500]}"
    assert not rid_exists, "renewal dir must NOT exist (R_FILES=0)"
    assert state_after_prepare_sha==state_before_sha, "State must be unchanged"
    print(f"REFUSE33 OK {prep_code} {prep_phase} {prep_disp} R_FILES=0 State unchanged no r33", flush=True)
    return 0

if __name__=="__main__":
    import sys
    sys.exit(main())
