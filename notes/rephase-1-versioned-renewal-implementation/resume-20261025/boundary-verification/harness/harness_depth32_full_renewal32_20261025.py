#!/usr/bin/env python3
"""Depth32-full renewal32: overlay CURRENT + PUBLIC renewal U as 32 (CURRENT, anchor r30).

TEST-only, no product edits, no candidate/reconstruct commits, no network/old-runners,
no cleanup failed fixture/cache purge. Workspace TMPDIR, per-phase 1200 with owned
PID/heartbeats/terminal exit, don't duplicate child on return. Fresh Python per
SOURCE epoch (CURRENT after overlay), no shared execution, no dummy SHA.

- Overlay CURRENT full source SOURCE-only commit preserving all old E, genuine
  Core change, coreStyle old unchanged baseline035 (style 035645ca... same OLD/CURRENT).
- Run PUBLIC renewal U prepare/finalize/activate as 32 (REUSE_TARGETS, mspec from
  ed31, toolchain None) with CURRENT code (1dad1ad/H74275d/S2290ddd), anchor r30
  unchanged, supersedes r31, strict State/current proof/history passes chain32.
- Code/validator no changes (use existing CURRENT fixed validators, no further edits),
  no dummy sha or rows invalid schema.
"""
import hashlib, json, os, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

def _run_git(root: Path, *a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

PINS={
 "H":"74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d",
 "S":"2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb",
 "HIGH":"1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb",
 "P1":"825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b",
 "PUB":"3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6",
 "edpub":"85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a",
 "P3S":"9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1",
 "Reader":"098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c",
}

def main():
    if len(sys.argv)!=4:
        print(f"usage: {sys.argv[0]} FIX_ROOT EVIDENCE_DIR CURRENT_SRC_REPO", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve(); cur_repo=Path(sys.argv[3]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    pidf=ev/"renewal32.pid"; hbf=ev/"renewal32.heartbeat.txt"
    pidf.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbf.write_text(f"renewal32 start {time.monotonic():.3f}\n")
    # Must be r1..r31 (31 files) before renewal32, HEAD 36c679cc, State->r31
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs=set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    expected_set=set(f"publication-surface-revalidation-r{i}.json" for i in range(1,32))
    assert recs==expected_set, f"need r1..r31 before renewal32, got len={len(recs)}"
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    assert head_before=="36c679cc5ed3291c11d4a01bdee906807cace8c4", f"must be 36c679cc before overlay, got {head_before}"
    state=json.loads((fix/"sources/2026-W37/production-state.json").read_bytes().decode("utf-8"))
    prov=state.get("publication_revalidation_provenance",{})
    r31_sha=_sha(rec_dir/"publication-surface-revalidation-r31.json")
    assert prov.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json" and prov.get("sha256")==r31_sha, f"State must point r31, got {prov}"
    r30_sha=_sha(rec_dir/"publication-surface-revalidation-r30.json")
    hbf.write_text(hbf.read_text()+f"r1..r31 present r30={r30_sha[:12]} r31={r31_sha[:12]} {time.monotonic():.3f}\n")
    # Overlay CURRENT full source SOURCE-only commit preserving all old E, genuine Core change
    # Verify style unchanged baseline035 in OLD and CURRENT before overlay
    old_style=fix/"templates/survey/jgaisurvey.sty"
    assert old_style.is_file()
    assert _sha(old_style)=="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec", f"old style drift {_sha(old_style)[:12]}"
    # CURRENT source from cur_repo HEAD 4851523 (741 tracked files, CURRENT pins committed)
    # Use git archive to list tracked files (no E), then extract to fix (overwrites tracked, preserves E)
    # First verify cur_repo HEAD pins (working tree? Actually cur_repo HEAD 4851523 has CURRENT pins committed, not just working tree)
    # Check cur_repo's scripts pins at HEAD (via git show)
    for fname,pin in [("scripts/survey_versioned_renewal_history_v2.py",PINS["H"]),("scripts/survey_versioned_renewal_source_v2.py",PINS["S"]),("scripts/survey_versioned_renewal_v2.py",PINS["HIGH"])]:
        proc=subprocess.run(["git","show",f"HEAD:{fname}"], cwd=str(cur_repo), capture_output=True, timeout=120)
        assert proc.returncode==0, f"git show {fname} failed"
        got=hashlib.sha256(proc.stdout).hexdigest()
        assert got==pin, f"CURRENT pin mismatch {fname}: {got[:12]} != {pin[:12]}"
    # Verify CURRENT style same baseline035
    proc=subprocess.run(["git","show","HEAD:templates/survey/jgaisurvey.sty"], cwd=str(cur_repo), capture_output=True, timeout=120)
    assert proc.returncode==0
    assert hashlib.sha256(proc.stdout).hexdigest()=="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec", "CURRENT style must be baseline035 unchanged"
    hbf.write_text(hbf.read_text()+f"style baseline035 verified OLD+CURRENT {time.monotonic():.3f}\n")
    # Extract CURRENT tracked files to fix via git archive (byte-independent, no hardlinks, preserves E since archive only has tracked)
    t0=time.monotonic()
    proc1=subprocess.run(["git","archive","HEAD"], cwd=str(cur_repo), capture_output=True, timeout=1200)
    assert proc1.returncode==0, f"git archive failed {proc1.stderr[:500]}"
    # Write archive to temp file in workspace TMPDIR (not /tmp to avoid EDQUOT? Use ev as TMPDIR? Use fix's tmp? Use ev)
    arch_path=ev/"current-741.tar"
    arch_path.write_bytes(proc1.stdout)
    # Extract with tar (no hardlinks? tar preserves? Use tar -x, which creates new files, no hardlinks from archive? Archive has no hardlinks (git archive creates regular files). Good.)
    proc2=subprocess.run(["tar","-x","-f",str(arch_path),"-C",str(fix)], capture_output=True, text=True, timeout=1200)
    assert proc2.returncode==0, f"tar extract failed {proc2.stderr[:500]}"
    hb_dur=time.monotonic()-t0
    hbf.write_text(hbf.read_text()+f"overlay extract dt={hb_dur:.1f}s {time.monotonic():.3f}\n")
    # Verify pins after extract (working tree files must be CURRENT)
    for fname,pin in [("scripts/survey_versioned_renewal_history_v2.py",PINS["H"]),("scripts/survey_versioned_renewal_source_v2.py",PINS["S"]),("scripts/survey_versioned_renewal_v2.py",PINS["HIGH"]),("scripts/survey_editorial_correction_proposal_v2.py",PINS["P1"]),("scripts/survey_publication_v2.py",PINS["PUB"]),("scripts/survey_editorial_publication_v2.py",PINS["edpub"]),("scripts/survey_editorial_staged_source_v2.py",PINS["P3S"]),("scripts/survey_reader_publication_v2.py",PINS["Reader"])]:
        got=_sha(fix/fname)
        assert got==pin, f"overlay pin mismatch {fname}: {got[:12]} != {pin[:12]}"
    # Verify style still baseline035 after overlay
    assert _sha(fix/"templates/survey/jgaisurvey.sty")=="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec", "style must stay baseline035 after overlay"
    # Verify E preserved (untracked still ??, old E preserved): sources/2026-W37/publication/v2/r1..r31 must still exist, State still points r31, etc.
    assert (fix/"sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json").is_file()
    assert (fix/"sources/2026-W37/publication/v2/publication-surface-revalidation-r30.json").is_file()
    assert (fix/"sources/2026-W37/production-state.json").is_file()
    # git status: tracked M/A + untracked ?? (E preserved). Must have no deletion of E? Check E still untracked, not committed.
    st=_run_git(fix,"status","--short")
    assert st.returncode==0
    # Count tracked changes: should be many M/A (721->741 diff, genuine Core change, not artifact-only). Verify at least one Core file changed (e.g., scripts/survey_versioned_renewal_history_v2.py is new? Actually OLD at 36c679 has no versioned files, CURRENT has them as new files (A). Good genuine change (new files, not artifact-only). Also style unchanged (not M).
    # Verify style NOT in status M (unchanged)
    assert "templates/survey/jgaisurvey.sty" not in st.stdout, f"style should be unchanged, status shows {st.stdout[:500]}"
    hbf.write_text(hbf.read_text()+f"overlay pins verified E preserved {time.monotonic():.3f}\n")
    (ev/"overlay-status.txt").write_text(st.stdout[:4000]+"\n")
    # SOURCE-only commit preserving all old E, genuine Core change
    # git add only tracked source paths (741 paths from CURRENT HEAD), E stays ??
    # Get list of tracked files in CURRENT (741) via git ls-files in cur_repo
    proc_ls=subprocess.run(["git","ls-files"], cwd=str(cur_repo), capture_output=True, text=True, timeout=120)
    assert proc_ls.returncode==0
    tracked=proc_ls.stdout.strip().splitlines()
    assert len(tracked)==741, f"CURRENT tracked must be 741, got {len(tracked)}"
    # git add -- <tracked> (only SOURCE, E stays ??)
    # To avoid command line too long (741 args), use git add -A? No, that would add E (untracked sources/ etc.) which we must NOT add (E stays ??). Use git add -- <tracked> via xargs? Or git add -u + git add for new files? Simpler: git add --all with pathspec? Use `git add -- <tracked>` in batches.
    # First, verify E currently untracked (sources/ etc. should be ??)
    assert "sources/" in st.stdout or "sources/2026-W37" in st.stdout or "??" in st.stdout, "E should be untracked"
    # Add in batches of 100
    for i in range(0,len(tracked),100):
        batch=tracked[i:i+100]
        r=_run_git(fix,"add","--",*batch)
        assert r.returncode==0, f"git add batch {i} failed {r.stderr[:500]}"
    # Verify staged only SOURCE (741 paths? Actually 721->741 diff: some M, some A, total staged should be 741? Or less? Let's check staged status)
    st2=_run_git(fix,"status","--short")
    # E must still be ?? (not staged)
    assert "?? sources/" in st2.stdout or "?? sources" in st2.stdout or "??" in st2.stdout, f"E must stay ?? after add, got {st2.stdout[:1000]}"
    # Commit SOURCE-only with genuine Core change message, preserving E
    r=_run_git(fix,"-c","user.name=depth32-full-overlay","-c","user.email=overlay@example.invalid","-c","commit.gpgsign=false","commit","-m","TEST-ONLY: overlay CURRENT 741 SOURCE before renewal U32, E preserved (r1..r31 + State->r31), genuine Core change, style baseline035 unchanged")
    assert r.returncode==0, f"overlay commit failed {r.stderr[:1000]}"
    new_head=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    assert new_head!=head_before, "HEAD must move on overlay"
    (ev/"overlay-commit.txt").write_text(f"{head_before} -> {new_head}\n")
    hbf.write_text(hbf.read_text()+f"overlay commit {new_head[:12]} {time.monotonic():.3f}\n")
    # Verify overlay commit: parent 36c679cc, 741 tracked? ls-files count?
    r=_run_git(fix,"ls-files")
    assert r.returncode==0
    assert len(r.stdout.strip().splitlines())==741, f"overlay tracked must be 741, got {len(r.stdout.strip().splitlines())}"
    # Verify E preserved untracked after commit
    r=_run_git(fix,"status","--short")
    assert "??" in r.stdout, "E must still be untracked after overlay commit"
    # Now run PUBLIC renewal U prepare/finalize/activate as 32 with CURRENT code (after overlay, PYTHONPATH=fix CURRENT)
    sys.path.insert(0, str(fix))
    from scripts import survey_production_v2 as core
    from scripts import survey_versioned_renewal_v2 as high
    from scripts import survey_agent_control_v2 as agent
    state_rel="sources/2026-W37/production-state.json"
    mspec_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/manuscript-spec.json"
    assert (fix/mspec_rel).is_file(), f"missing mspec {mspec_rel} for U prepare (same-reader, reuse targets)"
    rid="high-u32-depth32-full"
    t1=time.monotonic()
    prep=high.prepare_renewal(fix, state_rel, rid, "REUSE_TARGETS", mspec_rel, None, "depth32-full-fixture", datetime.now(timezone.utc))
    basis_rel=prep.get("basis_path")
    if not basis_rel:
        # Try alternative keys (basis_ref path?)
        br=prep.get("basis_ref",{})
        if isinstance(br,dict): basis_rel=br.get("path")
    assert basis_rel and (fix/basis_rel).is_file(), f"basis missing {prep.keys()}"
    hbf.write_text(hbf.read_text()+f"PREPARE {time.monotonic():.3f} basis={basis_rel}\n")
    (ev/"renewal32-prepare.json").write_text(json.dumps({"rid":rid,"basis":basis_rel}, indent=2))
    # Fresh checks: re-inspect editorial deterministic-checks live files (like anchor renewal)
    old_checks_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/deterministic-checks.json"
    old_doc=core.load_json(fix/old_checks_rel)
    fresh=[]
    for row in old_doc["checks"]:
        rp=row["result"]["path"]
        live=fix/rp
        assert live.is_file(), f"QA file missing {rp}"
        fresh.append({"check_id":row["check_id"],"kind":"DETERMINISTIC","status":"PASS","executor":"depth32-full renewal U fresh assertions (synthetic, non-genuine)","evidence":f"Exact clone bytes reinspected: {rp}","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":rp,"sha256":_sha(live)}})
    fresh_rel="sources/2026-W37/publication/v2/editorial-corrections/wk-depth32-ed31/renewal-u-fresh-checks.json"
    core.write_json(fix/fresh_rel, {"checks":fresh})
    hbf.write_text(hbf.read_text()+f"FRESH_CHECKS {time.monotonic():.3f}\n")
    fin=high.finalize_renewal(fix, state_rel, basis_rel, fresh_rel, None, None, "depth32-full-fixture", datetime.now(timezone.utc))
    def _get(d,*keys):
        for k in keys:
            if k in d and isinstance(d[k],str) and (fix/d[k]).is_file(): return d[k]
        return None
    receipt_rel=_get(fin,"receipt","receipt_path","validated-source-manifest")
    assert receipt_rel, f"finalize must return receipt path, got {sorted(fin.keys())}"
    hbf.write_text(hbf.read_text()+f"FINALIZE {time.monotonic():.3f} receipt={receipt_rel}\n")
    (ev/"renewal32-finalize-keys.json").write_text(json.dumps(sorted(fin.keys()), indent=2))
    set_rel=None
    for k in ("set","set_path","publication-set","set_ref"):
        v=fin.get(k)
        if isinstance(v,str) and (fix/v).is_file(): set_rel=v; break
        if isinstance(v,dict) and "path" in v and (fix/v["path"]).is_file(): set_rel=v["path"]; break
    assert set_rel, f"set missing in finalize {sorted(fin.keys())}"
    res=high.activate_renewal(fix, state_rel, set_rel, f"Depth32-full renewal U {rid} after editorial r31 (anchor r30)", "depth32-full-fixture", datetime.now(timezone.utc))
    assert res.get("status")=="ACTIVATED", res
    hbf.write_text(hbf.read_text()+f"ACTIVATE {time.monotonic():.3f} {str(res)[:500]}\n")
    (ev/"renewal32-activate.json").write_text(json.dumps({"status":res.get("status"),"record":res.get("record_path") or res.get("record")}, indent=2))
    # Verify chain32: r1..r32 (32 files), r32 supersedes r31, anchor r30 unchanged, strict State/current proof/history passes
    new_recs=set(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    expected_set=set(f"publication-surface-revalidation-r{i}.json" for i in range(1,33))
    assert new_recs==expected_set, f"must have r1..r32, got len={len(new_recs)}"
    r32_path=rec_dir/"publication-surface-revalidation-r32.json"
    # Actually renewal record filename? Is it r32.json? Or different? High activation creates rN.json? For renewal, activation record is versioned? Should be r32.json (next sequence). Verify.
    assert r32_path.is_file(), f"r32 missing, recs={sorted(new_recs)[-5:]}"
    r32=json.loads(r32_path.read_bytes().decode("utf-8"))
    assert r32.get("kind")=="VERSIONED_RENEWAL_ACTIVATION_V1" and r32.get("reason_class")=="REVIEWED_VERSIONED_CORE_RENEWAL", f"r32 kind wrong {r32.get('kind')}"
    r31_sha=_sha(rec_dir/"publication-surface-revalidation-r31.json")
    sup=r32.get("supersedes")
    assert sup.get("sha256")==r31_sha and sup.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json", f"r32 must supersede r31, got {sup}"
    anchor=r32.get("canonical_anchor")
    assert anchor=={"kind":"LEGACY_REVALIDATION","ref":{"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r30.json","sha256":r30_sha}}, f"r32 anchor must stay r30, got {anchor}"
    # State must now point r32
    new_state=json.loads((fix/"sources/2026-W37/production-state.json").read_bytes().decode("utf-8"))
    new_prov=new_state.get("publication_revalidation_provenance",{})
    r32_sha=_sha(r32_path)
    assert new_prov.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r32.json" and new_prov.get("sha256")==r32_sha, f"State must point r32, got {new_prov}"
    # Strict hist verify chain32 with CURRENT (strict)
    hist_out=high.verify_renewal_history(fix, str(r32_path.relative_to(fix).as_posix()))
    assert hist_out.get("HISTORICAL_IDENTITY_VERIFIED") or hist_out.get("historical_identity_verified"), f"hist chain32 failed {hist_out}"
    # Strict State/current proof: public old? Actually CURRENT agent validate_state (strict) must pass (no anchor mismatch, no Gate drift)
    cfg=core.load_json(fix/core.DEFAULT_CONFIG) if hasattr(core,"DEFAULT_CONFIG") else core.load_json(fix/"config/survey-production-v2.json")
    # Load config correctly: use core.load_json for config path?
    try:
        cfg_path=fix/"config/survey-production-v2.json"
        cfg_doc=json.loads(cfg_path.read_bytes().decode("utf-8"))
    except Exception as e:
        raise AssertionError(f"config load failed {e}")
    errs=agent.validate_agent_state(fix, cfg_doc, new_state)
    assert not errs, f"State unhealthy after renewal32 {errs[:5]}"
    (ev/"renewal32-r32.json").write_text(json.dumps({"r32_sha":r32_sha[:12],"supersedes":sup,"anchor":anchor}, indent=2))
    print(f"RENEWAL32 OK r32 supersedes r31 anchor r30 chain32, r32={r32_sha[:12]}", flush=True)
    return 0

if __name__=="__main__":
    import sys
    sys.exit(main())
