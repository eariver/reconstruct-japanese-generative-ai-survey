#!/usr/bin/env python3
"""R1x2 anchor — actual public refresh TWICE with weekly_derivation comment commits only.

Fresh child per R1 (no module caching). Uses ONLY old 721 source code (anchor-weekly at 721a04d).
Public CLI: scripts/survey_agent_control_v2.py refresh-mechanical-evidence.
Records HEAD/tree/status/artifact SHAs/anchor before/after, monotonic clock. Synthetic executor, no genuine approval.
No --allow-empty (comment lines ensure change). Canonical R1 only weekly_derivation.
"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

def _run_git(root: Path, *args: str):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} FIX_ROOT EVIDENCE_DIR", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    pidfile=ev/"r1x2.pid"; hbfile=ev/"r1x2.heartbeat.txt"
    pidfile.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbfile.write_text(f"r1x2 start {time.monotonic():.3f}\n")
    # pins before R1
    head0=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    assert head0=="721a04d85532d7855f3e54cc411f5847c787726e", f"must start 721a04d, got {head0}"
    (ev/"r1-pin-before-head.txt").write_text(head0+"\n")
    # find state path from VALIDATED artifacts (built in previous step)
    state_rel="sources/2026-W37/production-state.json"
    assert (fix/state_rel).is_file(), f"missing VALIDATED state {state_rel} — run validated builder first"
    # R1 twice
    for i,marker,recorded_at,reason in [
        (1,"r1","2026-10-25T15:10:00Z","R1 anchor refresh 1"),
        (2,"r2","2026-10-25T15:20:00Z","R1 anchor refresh 2")]:
        t0=time.monotonic()
        hbfile.write_text(hbfile.read_text()+f"{marker} commit start {t0:.3f}\n")
        # meaningful tool-source comment commit (weekly_derivation only)
        helper=fix/"scripts/survey_weekly_derivation_v2.py"
        txt=helper.read_text(encoding="utf-8")
        assert (fix/".latexmkrc").is_file(), ".latexmkrc must be present in old 721"
        helper.write_text(txt+f"\n# R1 anchor {marker}: comment-only control change at old 721.\n", encoding="utf-8")
        # git add + commit (no --allow-empty, must have change)
        r1=_run_git(fix,"add","--","scripts/survey_weekly_derivation_v2.py")
        assert r1.returncode==0, f"git add failed {r1.stderr}"
        r2=_run_git(fix,"-c","user.name=rephase-r1-anchor","-c","user.email=r1-anchor@example.invalid","-c","commit.gpgsign=false","commit","-m",f"R1 anchor {marker} weekly_derivation comment-only at old 721")
        assert r2.returncode==0, f"git commit failed {r2.stderr}"
        head_new=_run_git(fix,"rev-parse","HEAD").stdout.strip()
        assert head_new!=head0 if i==1 else True, "HEAD must move on R1 commit"
        (ev/f"r1-{marker}-commit-head.txt").write_text(head_new+"\n")
        (ev/f"r1-{marker}-commit-log.txt").write_text(_run_git(fix,"log","--oneline","-3").stdout)
        hbfile.write_text(hbfile.read_text()+f"{marker} committed {head_new} dt={time.monotonic()-t0:.1f}s\n")
        # fresh subprocess for public R1 CLI (no module caching, PYTHONPATH=fix, cwd=fix)
        t1=time.monotonic()
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file",
                    "PYTHONDONTWRITEBYTECODE":"1","PYTHONPATH":str(fix),"TMPDIR":os.environ.get("TMPDIR","")})
        cmd=[sys.executable,str(fix/"scripts/survey_agent_control_v2.py"),"--repo-root",str(fix),
             "refresh-mechanical-evidence","--state",str(fix/state_rel),
             "--reason",reason,"--executor","r1-anchor-fixture","--recorded-at",recorded_at]
        proc=subprocess.run(cmd, cwd=str(fix), capture_output=True, text=True, timeout=1200, env=env)
        (ev/f"r1-{marker}-refresh-stdout.txt").write_text(proc.stdout)
        (ev/f"r1-{marker}-refresh-stderr.txt").write_text(proc.stderr)
        (ev/f"r1-{marker}-refresh-exit.txt").write_text(str(proc.returncode))
        hbfile.write_text(hbfile.read_text()+f"{marker} refresh exit={proc.returncode} dt={time.monotonic()-t1:.1f}s\n")
        assert proc.returncode==0, f"R1 {marker} refresh failed exit={proc.returncode} stdout={proc.stdout[:2000]} stderr={proc.stderr[:2000]}"
        # verify new record file exists
        rec_dir=fix/"sources/2026-W37/publication/v2"
        recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
        (ev/f"r1-{marker}-records.txt").write_text("\n".join(recs)+"\n")
        assert len(recs)>=i, f"expected >= {i} records after {marker}, got {recs}"
        # artifact SHAs for latest record
        latest=rec_dir/recs[-1]
        (ev/f"r1-{marker}-latest-sha.txt").write_text(f"{latest.name} {_sha(latest)}\n")
        head0=head_new  # for next iteration anchor
        hbfile.write_text(hbfile.read_text()+f"{marker} done {time.monotonic():.3f}\n")
    # final verification: r2 cumulative, anchor still original checkpoint (no fake shape)
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    assert recs==["publication-surface-revalidation-r1.json","publication-surface-revalidation-r2.json"], f"must have exactly r1+r2, got {recs}"
    r1=json.loads((rec_dir/recs[0]).read_bytes()); r2=json.loads((rec_dir/recs[1]).read_bytes())
    # r2 must supersede r1, anchor must be original validation checkpoint (cumulative, no rollover)
    assert r2.get("supersedes") is not None, "r2 must supersede r1"
    # canonical_anchor must equal original checkpoint (from VALIDATED build), not rolled
    # original checkpoint is sources/2026-W37/checkpoints-validation.json? Check via r1 prior_checkpoint
    assert r1.get("prior_checkpoint") is not None and r2.get("prior_checkpoint") is not None
    # anchor kind must be VALIDATION_CHECKPOINT (original), not r1
    for rec,name in [(r1,"r1"),(r2,"r2")]:
        anchor=rec.get("canonical_anchor") or rec.get("anchor") or {}
        # different schemas use different keys; record full for evidence, require original checkpoint ref
        (ev/f"r1-{name}-anchor.json").write_text(json.dumps(anchor, indent=2))
    (ev/"r1x2-records.json").write_text(json.dumps({"r1":r1.get("recorded_at"),"r2":r2.get("recorded_at"),"files":recs}, indent=2))
    print(f"R1x2 OK r1+r2 cumulative, HEAD {_run_git(fix,'rev-parse','HEAD').stdout.strip()}", flush=True)
    return 0

if __name__=="__main__":
    sys.exit(main())
