#!/usr/bin/env python3
"""Depth32-full finalize/activate33: attempt finalize+activate after prepare33 success, must REFUSE.

TEST-only. Uses workspace TMPDIR, per-phase 1200, owned PID/heartbeat/terminal exit.
Prepare33 succeeded (dir high-u33 + basis exist, State unchanged, no r33). Now attempt
finalize (fresh checks) then activate (should refuse: chain 33 exceeds max32).
Record exact gate + inventory. No cleanup, no duplicate child.
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
    pidf=ev/"finalize33.pid"; hbf=ev/"finalize33.heartbeat.txt"
    pidf.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbf.write_text(f"finalize33 start {time.monotonic():.3f}\n")
    rec_dir=fix/"sources/2026-W37/publication/v2"
    state_path=fix/"sources/2026-W37/production-state.json"
    state_before_sha=_sha(state_path)
    (ev/"finalize33-pin-state-before.txt").write_text(state_before_sha+"\n")
    rid="high-u33-depth32-full"
    basis_rel=f"sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/{rid}/renewal-basis.json"
    assert (fix/basis_rel).is_file(), f"basis missing {basis_rel} (prepare33 must have succeeded)"
    hbf.write_text(hbf.read_text()+f"basis present {time.monotonic():.3f}\n")
    sys.path.insert(0, str(fix))
    from scripts import survey_production_v2 as core
    from scripts import survey_versioned_renewal_v2 as high
    from scripts import survey_agent_control_v2 as agent
    state_rel="sources/2026-W37/production-state.json"
    # Fresh checks (same as renewal32, re-inspect editorial deterministic-checks)
    old_checks_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/deterministic-checks.json"
    old_doc=core.load_json(fix/old_checks_rel)
    fresh=[]
    for row in old_doc["checks"]:
        rp=row["result"]["path"]
        live=fix/rp
        assert live.is_file()
        fresh.append({"check_id":row["check_id"],"kind":"DETERMINISTIC","status":"PASS","executor":"depth32-full 33rd fresh (synthetic)","evidence":f"Exact bytes: {rp}","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":rp,"sha256":_sha(live)}})
    fresh_rel=f"sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/{rid}/renewal-u-fresh-checks.json"
    # If fresh already exists from prepare? No, prepare does not create fresh; finalize needs fresh. Write it (this is NEW file in existing renewal dir, counts as R? But finalize has not yet refused, so writing fresh is allowed? Actually finalize writes fresh? No, fresh is input to finalize, written before finalize. If finalize refuses, fresh file remains as part of incomplete dir (preserved). Good.)
    core.write_json(fix/fresh_rel, {"checks":fresh})
    hbf.write_text(hbf.read_text()+f"FRESH {time.monotonic():.3f}\n")
    fin_code=None; fin_phase=None; fin_disp=None; fin_detail=None; fin_ok=False; fin_keys=[]
    try:
        fin=high.finalize_renewal(fix, state_rel, basis_rel, fresh_rel, None, None, "depth32-full-fixture", datetime.now(timezone.utc))
        fin_ok=True
        fin_keys=sorted(fin.keys())
        fin_detail=f"UNEXPECTED FINALIZE SUCCESS keys={fin_keys}"
    except Exception as exc:
        fin_code=getattr(exc,"code",None) or type(exc).__name__
        fin_phase=getattr(exc,"phase",None) or ""
        fin_disp=getattr(exc,"disposition",None) or ""
        fin_detail=(getattr(exc,"detail",None) or str(exc))[:2000]
    inv_after_fin={"recs":sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")),"state_sha":_sha(state_path),"rid_dir_exists":(fix/f"sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewals/{rid}").exists()}
    (ev/"finalize33-result.json").write_text(json.dumps({"code":fin_code,"phase":fin_phase,"disposition":fin_disp,"detail":fin_detail,"finalize_ok":fin_ok,"keys":fin_keys,"inv":inv_after_fin,"state_before":state_before_sha}, indent=2, sort_keys=True)+"\n")
    hbf.write_text(hbf.read_text()+f"FINALIZE33 {fin_code} {fin_phase} {fin_disp} ok={fin_ok} {time.monotonic():.3f}\n")
    # Attempt activate33 only if finalize succeeded (needs set). If finalize refused, activate cannot proceed (no set), record as refused before R/State (no r33, State unchanged).
    act_code=None; act_phase=None; act_disp=None; act_detail=None; act_ok=False
    if fin_ok:
        # Find set from fin
        set_rel=None
        for k in ("set","set_path","publication-set","set_ref"):
            v=fin.get(k)
            if isinstance(v,str) and (fix/v).is_file(): set_rel=v; break
            if isinstance(v,dict) and "path" in v and (fix/v["path"]).is_file(): set_rel=v["path"]; break
        if not set_rel:
            act_detail=f"finalize succeeded but set missing keys={fin_keys}"
        else:
            try:
                res=high.activate_renewal(fix, state_rel, set_rel, f"Depth32-full 33rd {rid} (should refuse chain exceeds max32)", "depth32-full-fixture", datetime.now(timezone.utc))
                act_ok=True
                act_detail=f"UNEXPECTED ACTIVATE SUCCESS {res}"
            except Exception as exc:
                act_code=getattr(exc,"code",None) or type(exc).__name__
                act_phase=getattr(exc,"phase",None) or ""
                act_disp=getattr(exc,"disposition",None) or ""
                act_detail=(getattr(exc,"detail",None) or str(exc))[:2000]
    else:
        act_detail=f"finalize refused ({fin_code} {fin_phase}), activate not attempted (no set from refused finalize, no new R/State)"
        act_code=fin_code; act_phase=fin_phase; act_disp=fin_disp
    inv_final={"recs":sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r")),"rec_count":len(list(rec_dir.glob("publication-surface-revalidation-r*.json"))),"state_sha":_sha(state_path)}
    (ev/"activate33-result.json").write_text(json.dumps({"code":act_code,"phase":act_phase,"disposition":act_disp,"detail":act_detail,"activate_ok":act_ok,"inv_final":inv_final,"state_before":state_before_sha}, indent=2, sort_keys=True)+"\n")
    hbf.write_text(hbf.read_text()+f"ACTIVATE33 {act_code} {act_phase} {act_disp} ok={act_ok} {time.monotonic():.3f}\n")
    print(json.dumps({"finalize_ok":fin_ok,"finalize_code":fin_code,"activate_ok":act_ok,"activate_code":act_code,"inv_final":inv_final}, indent=2))
    # Must REFUSE at finalize or activate (not succeed both). Record exact gate.
    assert not (fin_ok and act_ok), f"33rd must REFUSE (finalize+activate both succeeded unexpectedly)"
    # Verify no new r33, State unchanged (before NEW R/State writes for r33 record + State)
    assert inv_final["rec_count"]==32, f"no new r33 must exist, got {inv_final['rec_count']}"
    assert inv_final["state_sha"]==state_before_sha, f"State must be unchanged, before {state_before_sha[:12]} after {inv_final['state_sha'][:12]}"
    print(f"REFUSE33-FINALIZE/ACTIVATE OK finalize_ok={fin_ok} {fin_code} {fin_phase} activate_ok={act_ok} {act_code} {act_phase} no r33 State unchanged", flush=True)
    return 0

if __name__=="__main__":
    import sys
    sys.exit(main())
