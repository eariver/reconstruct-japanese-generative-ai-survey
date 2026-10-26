#!/usr/bin/env python3
"""Fresh controlled H baseline measurement — read-only, no saved-runner exec.

Measures verify_versioned_history on real high24 weekly r1 (EDITORIAL chain1)
and r8 (VERSIONED chain8) using CURRENT candidate H code, counting Git child
calls and wall time + cProfile. Does NOT mutate fixtures, candidate, or DB.
"""
from __future__ import annotations
import cProfile
import hashlib
import io
import json
import pstats
import subprocess
import sys
import time
from pathlib import Path

CANDIDATE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work")
FIXTURE_WEEKLY = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly")

sys.path.insert(0, str(CANDIDATE))
sys.path.insert(0, str(CANDIDATE / "scripts"))

# Count git subprocess calls
orig_run = subprocess.run
counts = {"git_show": 0, "git_lstree": 0, "git_catfile_e": 0, "git_other": 0, "total_git": 0}
def counting_run(*args, **kwargs):
    cmd = args[0] if args else kwargs.get("args", [])
    if isinstance(cmd, list) and cmd and cmd[0] == "git":
        counts["total_git"] += 1
        joined = " ".join(cmd)
        if cmd[1:2] == ["show"]:
            counts["git_show"] += 1
        elif cmd[1:2] == ["ls-tree"]:
            counts["git_lstree"] += 1
        elif cmd[1:3] == ["cat-file", "-e"]:
            counts["git_catfile_e"] += 1
        else:
            counts["git_other"] += 1
            # record other for diagnosis
            # print("OTHER GIT:", joined[:300])
    return orig_run(*args, **kwargs)

subprocess.run = counting_run

from scripts import survey_versioned_renewal_history_v2 as H

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run_one(record_rel: str):
    counts_before = dict(counts)
    t0 = time.monotonic()
    pr = cProfile.Profile()
    pr.enable()
    try:
        result = H.verify_versioned_history(FIXTURE_WEEKLY, record_rel)
        ok = True
        err = None
    except Exception as e:
        result = None
        ok = False
        err = f"{type(e).__name__}: {e}"
    pr.disable()
    t1 = time.monotonic()
    elapsed = t1 - t0
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("cumulative")
    ps.print_stats(40)
    profile_text = s.getvalue()
    # Extract top git-related cumulative
    counts_after = dict(counts)
    delta = {k: counts_after[k]-counts_before[k] for k in counts}
    return {
        "record": record_rel,
        "ok": ok,
        "err": err,
        "elapsed_sec": elapsed,
        "git_delta": delta,
        "chain_length": result.get("chain_length") if ok else None,
        "n_bindings": len(result.get("observed_source_bindings", [])) if ok else None,
        "profile_top40": profile_text,
    }

if __name__ == "__main__":
    out = {}
    out["candidate_H_sha256"] = sha256_file(CANDIDATE / "scripts/survey_versioned_renewal_history_v2.py")
    out["candidate_H_lines"] = sum(1 for _ in (CANDIDATE / "scripts/survey_versioned_renewal_history_v2.py").read_text().splitlines())
    # fixture guard
    import subprocess as sp
    def git(repo: Path, *a):
        r = orig_run(["git", *a], cwd=str(repo), capture_output=True, text=True, timeout=30, env={"GIT_OPTIONAL_LOCKS": "0", "PATH": "/usr/bin:/bin"})
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    head, _, _ = git(FIXTURE_WEEKLY, "rev-parse", "HEAD")
    status, _, _ = git(FIXTURE_WEEKLY, "status", "--porcelain=v1", "--untracked-files=all")
    out["fixture_weekly_HEAD"] = head
    out["fixture_weekly_status_first2000"] = status[:2000]
    out["results"] = []
    for rel in [
        "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json",
        "sources/2026-W37/publication/v2/publication-surface-revalidation-r8.json",
    ]:
        # reset counts per run for clarity but keep global
        r = run_one(rel)
        out["results"].append(r)
        print(f"RECORD {rel}: ok={r['ok']} elapsed={r['elapsed_sec']:.3f}s git={r['git_delta']} chain={r['chain_length']} n_bind={r['n_bindings']}")
        if not r["ok"]:
            print("  ERR:", r["err"][:2000])
    out["total_git_counts"] = dict(counts)
    dest = Path(__file__).parent / "baseline-measure-20261025.json"
    dest.write_text(json.dumps(out, indent=2))
    print(f"WROTE {dest}")
    # also write profile texts separately
    for r in out["results"]:
        tag = "r1" if "r1.json" in r["record"] else "r8"
        (Path(__file__).parent / f"baseline-profile-{tag}-20261025.txt").write_text(r["profile_top40"])
    print("DONE")
