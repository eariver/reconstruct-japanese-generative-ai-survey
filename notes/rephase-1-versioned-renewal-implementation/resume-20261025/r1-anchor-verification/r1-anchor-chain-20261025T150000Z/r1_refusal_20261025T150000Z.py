#!/usr/bin/env python3
"""R1-after-versioned refusal check — old R1 must refuse with no writes when State is versioned/INDETERMINATE.

Uses OLD 721? No — current epoch is NEW 740 (after overlay). R1 helper is weekly_derivation (same file in both epochs).
Public CLI refresh-mechanical-evidence must refuse (versioned mode), no new r5, no HEAD move, no E mutation beyond preserved r4.
Fresh child, no module caching.
"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

def _run_git(root: Path, *a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def main():
    if len(sys.argv)!=3: print(f"usage {sys.argv[0]} FIX EVID", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    (ev/"r1-refusal-pin-before-head.txt").write_text(head_before+"\n")
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs_before=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    (ev/"r1-refusal-records-before.txt").write_text("\n".join(recs_before)+"\n")
    state_rel="sources/2026-W37/production-state.json"
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file",
                "PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":str(fix),"TMPDIR":os.environ.get("TMPDIR","")})
    cmd=[sys.executable,str(fix/"scripts/survey_agent_control_v2.py"),"--repo-root",str(fix),
         "refresh-mechanical-evidence","--state",str(fix/state_rel),
         "--reason","R1 after versioned must refuse","--executor","r1-refusal-check","--recorded-at","2026-10-25T17:00:00Z"]
    proc=subprocess.run(cmd, cwd=str(fix), capture_output=True, text=True, timeout=600, env=env)
    (ev/"r1-refusal-stdout.txt").write_text(proc.stdout)
    (ev/"r1-refusal-stderr.txt").write_text(proc.stderr)
    (ev/"r1-refusal-exit.txt").write_text(str(proc.returncode))
    # Must refuse (non-zero), no new record, no HEAD move
    recs_after=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    (ev/"r1-refusal-records-after.txt").write_text("\n".join(recs_after)+"\n")
    head_after=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    (ev/"r1-refusal-pin-after-head.txt").write_text(head_after+"\n")
    assert proc.returncode!=0, f"R1 after versioned must refuse, got exit 0 {proc.stdout[:1000]}"
    assert recs_after==recs_before, f"no new record on refusal, before {recs_before} after {recs_after}"
    assert head_after==head_before, f"no HEAD move on refusal {head_before} -> {head_after}"
    print(f"R1-REFUSAL OK exit={proc.returncode} no writes", flush=True)
    return 0

if __name__=="__main__":
    import sys
    sys.exit(main())
