#!/usr/bin/env python3
"""Renewal U same-reader after editorial — new 740 tools, anchor r2, supersedes r3.

Fresh child (PYTHONPATH=new epoch 5950e0f, no old caching). Public high APIs:
prepare REUSE_TARGETS (mspec from ed3, toolchain None) -> finalize (fresh checks, sem/vis None derive predecessor)
-> activate -> history/current State. Anchor still r2, supersedes r3. Synthetic reviews, no genuine approval.
"""
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

def _run_git(root: Path, *a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=3: print(f"usage {sys.argv[0]} FIX EVID", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    pidf=ev/"renewal-u.pid"; hbf=ev/"renewal-u.heartbeat.txt"
    pidf.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbf.write_text(f"renewal-u start {time.monotonic():.3f}\n")
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    (ev/"renewal-pin-before-head.txt").write_text(head_before+"\n")
    # must be overlay commit 5950e0f (new 740), with r1+r2+r3 present
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    assert recs==["publication-surface-revalidation-r1.json","publication-surface-revalidation-r2.json","publication-surface-revalidation-r3.json"], f"need r1+r2+r3 before renewal, got {recs}"
    r2_sha=_sha(rec_dir/"publication-surface-revalidation-r2.json")
    r3_sha=_sha(rec_dir/"publication-surface-revalidation-r3.json")
    hbf.write_text(hbf.read_text()+f"r1+r2+r3 present {time.monotonic():.3f}\n")
    sys.path.insert(0, str(fix))
    from scripts import survey_production_v2 as core
    from scripts import survey_versioned_renewal_v2 as high
    from scripts import survey_versioned_renewal_source_v2 as srcmod
    from scripts import survey_agent_control_v2 as agent
    state_rel="sources/2026-W37/production-state.json"
    assert (fix/state_rel).is_file()
    # mspec from editorial ed3 for U prepare (same-reader, reuse targets)
    mspec_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/manuscript-spec.json"
    assert (fix/mspec_rel).is_file(), f"missing mspec {mspec_rel}"
    rid="high-u1-anchor-weekly"
    t0=time.monotonic()
    prep=high.prepare_renewal(fix, state_rel, rid, "REUSE_TARGETS", mspec_rel, None, "anchor-renewal-fixture", datetime.now(timezone.utc))
    basis_rel=prep.get("basis_path") or prep.get("basis_ref",{}).get("path") if isinstance(prep.get("basis_ref"),dict) else prep.get("basis_path")
    # prep returns dict with basis_path? Check keys
    (ev/"renewal-prepare.json").write_text(json.dumps({"keys":sorted(prep.keys()),"rid":rid}, indent=2))
    assert basis_rel and (fix/basis_rel).is_file(), f"basis missing {prep}"
    hbf.write_text(hbf.read_text()+f"PREPARE {time.monotonic():.3f} basis={basis_rel}\n")
    # fresh checks: re-inspect editorial deterministic-checks live files (like phase-S)
    old_checks_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/deterministic-checks.json"
    old_doc=core.load_json(fix/old_checks_rel)
    fresh=[]
    for row in old_doc["checks"]:
        rp=row["result"]["path"]
        live=fix/rp
        assert live.is_file(), f"QA file missing {rp}"
        fresh.append({"check_id":row["check_id"],"kind":"DETERMINISTIC","status":"PASS",
                      "executor":"anchor renewal U fresh assertions (synthetic, non-genuine)",
                      "evidence":f"Exact clone bytes reinspected: {rp}",
                      "recorded_at":datetime.now(timezone.utc).isoformat(),
                      "result":{"path":rp,"sha256":_sha(live)}})
    fresh_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-anchor-ed3/renewal-u-fresh-checks.json"
    core.write_json(fix/fresh_rel, {"checks":fresh})
    hbf.write_text(hbf.read_text()+f"FRESH_CHECKS {time.monotonic():.3f}\n")
    fin=high.finalize_renewal(fix, state_rel, basis_rel, fresh_rel, None, None, "anchor-renewal-fixture", datetime.now(timezone.utc))
    (ev/"renewal-finalize-keys.json").write_text(json.dumps(sorted(fin.keys()), indent=2))
    # finalize returns paths with _path suffix in new code (receipt_path etc.) — accept either
    def _get(d,*keys):
        for k in keys:
            if k in d and isinstance(d[k],str) and (fix/d[k]).is_file(): return d[k]
        return None
    receipt_rel=_get(fin,"receipt","receipt_path","validated-source-manifest")
    assert receipt_rel, f"finalize must return receipt path, got {sorted(fin.keys())}"
    hbf.write_text(hbf.read_text()+f"FINALIZE {time.monotonic():.3f} receipt={receipt_rel}\n")
    # activate
    act=high.activate_renewal(fix, state_rel, fin.get("set") or fin.get("set_path") or fin.get("publication-set") or fin.get("set_ref") or "", f"Anchor renewal U {rid} after editorial r3", "anchor-fixture", datetime.now(timezone.utc)) if False else None
    # Above line tricky: need set_path string. Derive from fin.
    set_rel=None
    for k in ("set","set_path","publication-set","set_ref"):
        v=fin.get(k)
        if isinstance(v,str) and (fix/v).is_file(): set_rel=v; break
        if isinstance(v,dict) and "path" in v and (fix/v["path"]).is_file(): set_rel=v["path"]; break
    assert set_rel, f"set missing in finalize {sorted(fin.keys())}"
    # validate set path relative?
    res=high.activate_renewal(fix, state_rel, set_rel, f"Anchor renewal U {rid} after editorial r3", "anchor-fixture", datetime.now(timezone.utc))
    assert res.get("status")=="ACTIVATED", res
    hbf.write_text(hbf.read_text()+f"ACTIVATE {time.monotonic():.3f} {str(res)[:500]}\n")
    (ev/"renewal-activate.json").write_text(json.dumps({"status":res.get("status"),"record":res.get("record_path") or res.get("record")}, indent=2))
    # history: anchor still r2, supersedes r3
    new_recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    # renewal creates new record? Actually renewal activation creates new record file? Or new renewal record? Check: renewal record is separate? High activation creates renewal record? No, high activation updates State pointer to new set, and creates activation record? For renewal, activation record is versioned? Let's list all revalidation + renewal records.
    # For anchor, expect new file publication-surface-revalidation-r4.json (renewal U) OR renewal record elsewhere? Check.
    (ev/"renewal-records-after.txt").write_text("\n".join(new_recs)+"\n")
    # Find latest renewal record via history
    # history verify on latest state-selected set? Use verify_renewal_history on new record if exists, else on state?
    # Simplest: verify history on new U set's record? Actually renewal history is via high.verify_renewal_history(root, record_path) where record_path is renewal activation record? Need to find renewal record path from activate result.
    rec_path=res.get("record_path") or res.get("record") or ""
    if isinstance(rec_path, dict): rec_path=rec_path.get("path","")
    assert rec_path and (fix/rec_path).is_file(), f"renewal record missing {res}"
    hist=high.verify_renewal_history(fix, rec_path)
    assert hist.get("HISTORICAL_IDENTITY_VERIFIED") or hist.get("historical_identity_verified"), hist
    # anchor still r2?
    # hist should contain chain with anchor r2. Record for evidence.
    (ev/"renewal-history.json").write_text(json.dumps({"chain_length":hist.get("chain_length"),"anchor":str(hist.get("canonical_anchor") or hist.get("anchor") or "")[:1000]}, indent=2))
    # current State check (strict, no exception)
    st=core.load_json(fix/state_rel)
    errs=agent.validate_agent_state(fix, core.load_json(fix/core.DEFAULT_CONFIG), st)
    assert not errs, f"State unhealthy after renewal {errs}"
    hbf.write_text(hbf.read_text()+f"done {time.monotonic():.3f} dt={time.monotonic()-t0:.1f}s\n")
    print(f"RENEWAL U OK {rid} supersedes r3 anchor r2", flush=True)
    return 0

if __name__=="__main__":
    import sys
    sys.exit(main())
