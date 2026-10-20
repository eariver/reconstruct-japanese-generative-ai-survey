#!/usr/bin/env python3
"""Final22 positive orchestrator: runs per-route worker as subprocess (fixture-isolated).

Saves NOTHING except evidence; workers do all fixture writes. Captures raw
stdout/stderr/exit per route into evidence (never overwrite: files checked absent).
Verifies source22 candidate unchanged + fixture SOURCE heads before launch.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TS = "20261019T145007Z"
EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-supplement-20261019T145007Z")
SOURCE = Path("/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60")
FIXROOT = Path("/tmp/opencode/jgas-supplement-fixtures-20261019T145007Z")
BUILDROOT = Path("/tmp/opencode/jgas-supplement-builds-20261019T145007Z")
FIXMAP = {"weekly": "weekly-supp5", "special": "special-supp5"}
TOOLROOT = Path("/tmp/opencode/jgas-texlive-20261019T133205Z")
POSITIVE_EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-integration-20261019T135318Z")
ORIG_SURFACE = {"weekly": "136c0dd8a2bf4c5b4323993ff3882524c760d902f2a463b93bcd6fe95a948635",
                "special": "f40db7f6f88f099e13162f51296d0b74922d80a7ef31fd85329b85a957cd5"}
EXPECT_HEAD = {"weekly": "51b0e42b4540e963c317fc273d0c9639a0b53b6a",
               "special": "9917a6ff0e53229fe4f20702c58876cc904a8dab"}
SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

def git(args, cwd):
    env = dict(os.environ)
    for k in SANITIZE:
        env.pop(k, None)
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0"})
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                          capture_output=True, text=True, env=env)

def main() -> int:
    import argparse as _ap
    _pa = _ap.ArgumentParser()
    _pa.add_argument("--only-route", default=None, choices=("weekly", "special"))
    _pa.add_argument("--suffix", default="")
    _pargs = _pa.parse_args()
    only = _pargs.only_route
    suf = _pargs.suffix
    routes = (only,) if only else ("weekly", "special")
    for k in SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    if git(["rev-parse", "HEAD"], SOURCE).stdout.strip() != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("source HEAD moved", file=sys.stderr); return 3
    for route in routes:
        fix = FIXROOT / FIXMAP[route]
        h = git(["rev-parse", "HEAD"], fix).stdout.strip()
        if h != EXPECT_HEAD[route]:
            print(f"{route} fixture HEAD {h} != {EXPECT_HEAD[route]}", file=sys.stderr); return 4
        for name in (f"{route}-worker-stdout{suf}.txt", f"{route}-worker-stderr{suf}.txt", f"{route}-worker-exit{suf}.txt"):
            if (EVIDENCE / name).exists():
                print(f"refusing overwrite {name}", file=sys.stderr); return 5
    results = {}
    for route in routes:
        fix = FIXROOT / FIXMAP[route]
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = str(fix)
        if suf:
            env["EVID_SUFFIX"] = suf
        for k in SANITIZE:
            env.pop(k, None)
        t0 = time.time()
        p = subprocess.run(
            [sys.executable, str(EVIDENCE / "worker_supplement_route.py"),
              "--fixture", str(fix), "--route", route, "--evidence", str(EVIDENCE),
              "--buildroot", str(BUILDROOT), "--orig-surface-sha", ORIG_SURFACE[route],
              "--toolroot", str(TOOLROOT),
              "--positive-evidence", str(POSITIVE_EVIDENCE)],
            capture_output=True, text=True, env=env, cwd=str(EVIDENCE))
        dt = time.time() - t0
        (EVIDENCE / f"{route}-worker-stdout{suf}.txt").write_text(p.stdout or "")
        (EVIDENCE / f"{route}-worker-stderr{suf}.txt").write_text(p.stderr or "")
        (EVIDENCE / f"{route}-worker-exit{suf}.txt").write_text(str(p.returncode))
        with open(EVIDENCE / "commands-supplement-stages.log", "a") as f:
            f.write(f"CMD worker {route} suffix={suf or '-'} exit={p.returncode} duration_s={dt:.1f}\n")
        results[route] = {"exit": p.returncode, "duration_s": round(dt, 1)}
        print(f"worker {route}: exit={p.returncode} duration_s={dt:.1f}", flush=True)
        if p.returncode != 0:
            print(f"--- {route} stderr tail ---", flush=True)
            print((p.stderr or "")[-3000:], flush=True)
            break
    (EVIDENCE / f"supplement-summary{suf}.json").write_text(json.dumps(results, indent=2))
    return 0 if all(v["exit"] == 0 for v in results.values()) else 10

if __name__ == "__main__":
    open(Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-supplement-20261019T145007Z") / "commands-supplement-stages.log", "w").write("# supplement stage runs\n")
    raise SystemExit(main())
