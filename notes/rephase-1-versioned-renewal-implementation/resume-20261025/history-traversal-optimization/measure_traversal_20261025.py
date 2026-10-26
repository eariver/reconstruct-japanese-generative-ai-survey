#!/usr/bin/env python3
"""AUTHOR traversal-opt: before/after measure on real high24 r1/r8, NEW isolated copies not needed for before (read-only on fixture).

Captures cProfile + git counts + wall time + full public results (chain, bindings, lineage) + source pins.
Read-only on fixture high24 weekly (no writes), no old runners, no network, no cleanup.
Saves to this dir: before/after JSON + profiles.
"""
from __future__ import annotations
import cProfile, hashlib, io, json, pstats, subprocess, sys, time
from pathlib import Path

def _ws() -> Path:
    return Path(__file__).resolve().parents[4]

def main(tag: str):
    ws = _ws()
    cand = ws / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
    fixture = ws / ".rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly"
    sys.path.insert(0, str(cand))
    sys.path.insert(0, str(cand / "scripts"))
    import subprocess as spmod
    orig_run = spmod.run
    counts = {"git_show":0,"git_lstree":0,"git_catfile_e":0,"git_other":0,"total_git":0}
    def counting(*a, **k):
        cmd = a[0] if a else k.get("args", [])
        if isinstance(cmd, list) and cmd and cmd[0]=="git":
            counts["total_git"]+=1
            if cmd[1:2]==["show"]:
                counts["git_show"]+=1
            elif cmd[1:2]==["ls-tree"]:
                counts["git_lstree"]+=1
            elif cmd[1:3]==["cat-file","-e"]:
                counts["git_catfile_e"]+=1
            else:
                counts["git_other"]+=1
        return orig_run(*a, **k)
    spmod.run = counting
    from scripts import survey_versioned_renewal_history_v2 as H
    import importlib
    importlib.reload(H)
    def sha_file(p: Path)->str:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    out = {}
    out["candidate_H_sha256"]=sha_file(cand/"scripts/survey_versioned_renewal_history_v2.py")
    out["candidate_H_lines"]=len((cand/"scripts/survey_versioned_renewal_history_v2.py").read_text().splitlines())
    # fixture guard read-only
    def git(repo: Path,*a):
        r=orig_run(["git",*a],cwd=str(repo),capture_output=True,text=True,timeout=30,env={"GIT_OPTIONAL_LOCKS":"0","PATH":"/usr/bin:/bin"})
        return r.stdout.strip(),r.stderr.strip(),r.returncode
    head,_,_=git(fixture,"rev-parse","HEAD")
    status,_,_=git(fixture,"status","--porcelain=v1","--untracked-files=all")
    out["fixture_weekly_HEAD"]=head
    out["fixture_weekly_status_first2000"]=status[:2000]
    out["results"]=[]
    for rel in ["sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json","sources/2026-W37/publication/v2/publication-surface-revalidation-r8.json"]:
        before=dict(counts)
        t0=time.monotonic()
        pr=cProfile.Profile()
        pr.enable()
        try:
            res=H.verify_versioned_history(fixture,rel)
            ok=True; err=None
        except Exception as e:
            res=None; ok=False; err=f"{type(e).__name__}: {e}"
        pr.disable()
        t1=time.monotonic()
        s=io.StringIO(); ps=pstats.Stats(pr,stream=s).sort_stats("cumulative"); ps.print_stats(40)
        prof=s.getvalue()
        after=dict(counts)
        delta={k:after[k]-before[k] for k in counts}
        # capture full public results for equality (bindings, lineage, refs)
        entry={"record":rel,"ok":ok,"err":err,"elapsed_sec":t1-t0,"git_delta":delta,"profile_top40":prof}
        if ok:
            entry["chain_length"]=res.get("chain_length")
            entry["n_bindings"]=len(res.get("observed_source_bindings",[]))
            entry["observed_refs"]=res.get("observed_refs")
            entry["observed_source_bindings"]=res.get("observed_source_bindings")
            entry["materialization_lineage"]=res.get("materialization_lineage")
            entry["anchor_kind"]=res.get("anchor_kind")
            # counts for _validate etc from profile? parse ncalls for _validate
            # also direct count via profile stats? keep top40 only, plus full validate counts via manual? Use profile stats object?
            # For event trace, count _validate calls by re-parsing profile? Simpler: count via monkey-patch in test, here just profile.
        out["results"].append(entry)
        print(f"RECORD {rel}: ok={ok} elapsed={t1-t0:.3f}s git={delta} chain={entry.get('chain_length')} n_bind={entry.get('n_bindings')}")
        if not ok:
            print(" ERR:",err[:2000])
    out["total_git_counts"]=dict(counts)
    dest=Path(__file__).parent / f"{tag}-measure-20261025.json"
    dest.write_text(json.dumps(out,indent=2))
    print(f"WROTE {dest}")
    for r in out["results"]:
        t="r1" if "r1.json" in r["record"] else "r8"
        (Path(__file__).parent / f"{tag}-profile-{t}-20261025.txt").write_text(r["profile_top40"])
    print("DONE")
    spmod.run=orig_run

if __name__=="__main__":
    tag=sys.argv[1] if len(sys.argv)>1 else "before"
    main(tag)
