#!/usr/bin/env python3
"""LONGFORM editorial completion for lf-ed-3: stage reader+proposal, P2R, P2V, P3S63, build, reviews, finalize, activate.
1200s per phase, fresh child per epoch.
"""
import subprocess, sys, json, os, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-ed-20261025T090000Z"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired as e:
        (EVID/f"{tag}-stdout.txt").write_text("",encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s in {tag}\n",encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT",encoding="utf-8")
        with open(EVID/"commands.log","a",encoding="utf-8") as fh:
            fh.write(f"$ ... tag={tag} -> TIMEOUT\n")
        print(f"{tag}: TIMEOUT",flush=True)
        return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
def py_inline(code, argv, tag, timeout=TIMEOUT):
    return run_tag(tag, [sys.executable,"-c",code]+argv, timeout=timeout)
def main():
    prop_new="lf-ed-3"
    issue="SP001"
    # Re-run P1 to get full prepared dict and stage reader+proposal (idempotent: authoring already staged)
    code_p1_stage = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
import os
print(f"P1-stage child PID={os.getpid()}", flush=True)
issue="SP001"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
dest=root_p/pdir_new/"authoring-input.json"
assert dest.exists(), "authoring missing"
res=p1mod.prepare_proposal(root_p, root_p/f"sources/{issue}/production-state.json", dest, prop_new, "LONGFORM renewal-to-editorial: changed reader on U4-active prior (synthetic)")
# stage reader + proposal (operator writes, P1 writes nothing)
proposal_dir=root_p/pdir_new
(reader_file, proposal_file)=(proposal_dir/"reader-surface-input-v2.json", proposal_dir/"proposal.json")
if not reader_file.exists():
    reader_file.write_bytes(res["proposed_canonical"])
    print(f"staged reader {reader_file.relative_to(root_p)}", flush=True)
else:
    print(f"reader exists, verify bytes match", flush=True)
    assert reader_file.read_bytes()==res["proposed_canonical"], "reader bytes drift"
if not proposal_file.exists():
    core.write_json(proposal_file, res["proposal"])
    print(f"staged proposal {proposal_file.relative_to(root_p)}", flush=True)
else:
    print(f"proposal exists, verify", flush=True)
print(f"STAGED proposal_dir={pdir_new}")
"""
    p = py_inline(code_p1_stage, [str(FIX), prop_new], "ed-p1-stage")
    assert p is not None and p.returncode==0, f"P1 stage failed {open(EVID/'ed-p1-stage-stderr.txt').read()[:8000]}"
    # P2R capture
    code_p2r = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_retention_v2 as p2r
import os
print(f"P2R child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
res=p2r.capture_retention(str(root_p), f"sources/{issue}/production-state.json", proposal)
print(f"P2R manifest={res.get('manifest_path')}", flush=True)
# verify
from scripts import survey_editorial_retention_v2 as p2r2
v=p2r2.verify_retention(str(root_p), proposal, res.get('manifest_path'))
print(f"P2R verify OK {v.get('manifest_path') if isinstance(v,dict) else 'ok'}", flush=True)
"""
    q = py_inline(code_p2r, [str(FIX), prop_new], "ed-p2r-full", timeout=1200)
    assert q is not None and q.returncode==0, f"P2R failed {open(EVID/'ed-p2r-full-stderr.txt').read()[:8000]}"
    # P2V observe (need manifest + scope? For initial, scope_review may be None? Let's try with manifest)
    code_p2v = r"""
import sys, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_current_authority_v2 as p2v
import os, glob
print(f"P2V child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
# find retention manifest
cands=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}").rglob("*retention*.json"))
print(f"cands={[str(p.relative_to(root_p)) for p in cands]}", flush=True)
manifest=None
for p in cands:
    if "manifest" in p.name:
        manifest=str(p.relative_to(root_p))
        break
print(f"manifest={manifest}", flush=True)
res=p2v.observe_current_authority(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest)
print(f"P2V keys={sorted(res.keys()) if isinstance(res,dict) else type(res)}", flush=True)
"""
    r = py_inline(code_p2v, [str(FIX), prop_new], "ed-p2v-full", timeout=1200)
    assert r is not None and r.returncode==0, f"P2V failed {open(EVID/'ed-p2v-full-stderr.txt').read()[:8000]}"
    print("P2R/P2V DONE, P3S next", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
