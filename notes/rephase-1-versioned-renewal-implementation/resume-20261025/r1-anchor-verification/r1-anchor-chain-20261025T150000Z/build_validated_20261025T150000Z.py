#!/usr/bin/env python3
"""NEW canonical Weekly VALIDATED builder under old 721 — fresh child, no old-module caching.

Uses OLD source's own test library (anchor-weekly at 721a04d):
  tests.test_survey_editorial_correction_proposal_v2._new_weekly_helper
  tests.test_survey_editorial_correction_proposal_v2._build_weekly_validated
NOT old notes saved runners (read-only API ref). Fresh interpreter, PYTHONPATH=anchor DB.
Records HEAD/tree/status before/after, artifact SHAs, monotonic clock. Synthetic reviews, no genuine approval.
"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

def _run_git(root: Path, *args: str):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} FIX_ROOT EVIDENCE_DIR", flush=True)
        return 2
    fix=Path(sys.argv[1]).resolve()
    ev=Path(sys.argv[2]).resolve()
    # guards
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v):
            print(f"UNSAFE {v}", flush=True); return 2
    tmpdir=os.environ.get("TMPDIR","")
    if not tmpdir or "/tmp"==tmpdir[:4] and "r1-anchor" not in tmpdir:
        print(f"BLOCKER TMPDIR must be workspace r1-anchor tmp, got {tmpdir!r}", flush=True); return 2
    sys.dont_write_bytecode=True
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    # pin before
    t0=time.monotonic()
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    tree_before=_run_git(fix,"rev-parse","HEAD^{tree}").stdout.strip()
    status_before=_run_git(fix,"status","--porcelain=v1","--untracked-files=all").stdout
    (ev/"validated-pin-before-head.txt").write_text(head_before+"\n")
    (ev/"validated-pin-before-tree.txt").write_text(tree_before+"\n")
    (ev/"validated-pin-before-status.txt").write_text(status_before)
    assert head_before=="721a04d85532d7855f3e54cc411f5847c787726e", f"must start 721a04d, got {head_before}"
    assert status_before=="", f"must start clean, got {status_before[:500]}"
    # heartbeat PID
    pidfile=ev/"validated-build.pid"
    hbfile=ev/"validated-build.heartbeat.txt"
    pidfile.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbfile.write_text(f"start {time.monotonic():.3f} HEAD {head_before}\n")
    # fresh import from FIX_ROOT (old 721), NOT from 740 TESTSRC
    sys.path.insert(0, str(fix))
    import unittest
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    # dummy testcase for helper (needs assert methods, addCleanup)
    class Dummy(unittest.TestCase):
        def runTest(self): pass
    dummy=Dummy()
    # _new_weekly_helper needs root with config, etc. — use fix as root
    helper=p1t._new_weekly_helper(dummy, fix)
    hbfile.write_text(hbfile.read_text()+f"helper {time.monotonic():.3f} issue {p1t.W_ISSUE}\n")
    built=p1t._build_weekly_validated(dummy, helper)
    hbfile.write_text(hbfile.read_text()+f"built {time.monotonic():.3f} keys {sorted(built.keys()) if isinstance(built,dict) else type(built).__name__}\n")
    # record artifacts
    head_after=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    status_after=_run_git(fix,"status","--porcelain=v1","--untracked-files=all").stdout
    (ev/"validated-pin-after-head.txt").write_text(head_after+"\n")
    (ev/"validated-pin-after-status.txt").write_text(status_after)
    # HEAD must NOT move (no commits yet, E untracked)
    assert head_after==head_before, f"HEAD moved during VALIDATED build {head_before} -> {head_after}"
    # status must show untracked E (new edition files), no tracked mods
    assert " M " not in status_after, f"tracked mods during VALIDATED build: {status_after[:1000]}"
    assert "??" in status_after, f"expected untracked E after VALIDATED build, got clean"
    # artifact SHAs (canonical state, receipt, manuscript, gate, pdf)
    arts={}
    for rel in [str(helper.source_root.relative_to(fix)/"production-state.json"),
                str((helper.source_root/"publication/v2/validated-source-manifest.json").relative_to(fix)),
                str((helper.source_root/"publication/v2/reader-manuscript-v2.json").relative_to(fix)),
                str((helper.source_root/"publication/v2/reader-surface-gate-v2.json").relative_to(fix)),
                str((helper.survey_root/"main.pdf").relative_to(fix))]:
        p=fix/rel
        assert p.is_file(), f"missing {rel}"
        arts[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
    (ev/"validated-artifacts.json").write_text(json.dumps({"head":head_after,"artifacts":arts,"built_keys":sorted(built.keys()) if isinstance(built,dict) else str(type(built)),"monotonic_dt":time.monotonic()-t0}, indent=2))
    hbfile.write_text(hbfile.read_text()+f"done {time.monotonic():.3f} dt={time.monotonic()-t0:.1f}s\n")
    print(f"VALIDATED OK HEAD {head_after} E_untracked {len(status_after.splitlines())} dt={time.monotonic()-t0:.1f}s", flush=True)
    return 0

if __name__=="__main__":
    sys.exit(main())
