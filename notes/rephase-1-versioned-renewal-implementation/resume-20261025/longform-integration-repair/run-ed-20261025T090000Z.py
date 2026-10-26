#!/usr/bin/env python3
"""LONGFORM renewal->EDITORIAL full P1->P2R->P2V->P3S63->build/postrender->finalize/activate.
NEW P lf-ed-3 from current authoring, proper 3 paragraphs, 1200s per phase.
"""
import subprocess, sys, json, os, pathlib, time, traceback
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-ed-20261025T090000Z"
EVID.mkdir(parents=True, exist_ok=True)
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/tmp"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"]=str(TMP)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    import subprocess as sp
    try:
        proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    except sp.TimeoutExpired as e:
        # record blocker with profile/stacks
        (EVID/f"{tag}-stdout.txt").write_text((e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")) if e.stdout else "", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"TIMEOUT {timeout}s in {tag} (no PASS, blocker, no infinite retry)\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        with open(EVID/"commands.log","a",encoding="utf-8") as fh:
            fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> TIMEOUT {timeout}s\n")
        print(f"{tag}: TIMEOUT {timeout}s", flush=True)
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
    (EVID/"commands.log").write_text(f"LONGFORM ED start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("ed-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    # pins
    py_inline(r"""
import sys, hashlib, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1])
for p in ["scripts/survey_versioned_renewal_history_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py"]:
    print(p, hashlib.sha256((root/p).read_bytes()).hexdigest())
""", [str(FIX)], "ed-pins")
    issue="SP001"; prop_old="lf-boot-1"; prop_new="lf-ed-3"
    pdir_old=f"sources/{issue}/publication/v2/editorial-corrections/{prop_old}"
    pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
    state_rel=f"sources/{issue}/production-state.json"
    # create NEW P authoring from current authoring, proper 3 paragraphs
    prep_auth = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root=pathlib.Path(sys.argv[1]); prop_new=sys.argv[2]
pdir_old=f"sources/SP001/publication/v2/editorial-corrections/lf-boot-1"
pdir_new=f"sources/SP001/publication/v2/editorial-corrections/{prop_new}"
old_auth=json.loads((root/pdir_old/"authoring-input.json").read_bytes())
new_auth=json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"]="LONGFORM renewal-editorial headline: fixture-local changed reader after U4 repair; no genuine approval."
new_auth["cover"]["deck"]="Changed deck for U4-active prior: same accepted research/Draft/Architecture, changed reader bytes."
new_auth["final_summary"]["paragraphs"]=[
    "The edition surveys accepted lineage sources with a fixture-local editorial amendment after versioned renewal.",
    "The claims remain attributed to their origins under the same accepted research and Draft.",
    "The synthesis stays inside authorized evidence."
]
# ensure changed
assert json.dumps(new_auth,sort_keys=True)!=json.dumps(old_auth,sort_keys=True)
# ensure 3 paragraphs and required sentence
assert len(new_auth["final_summary"]["paragraphs"])==3
assert "The synthesis stays inside authorized evidence." in new_auth["final_summary"]["paragraphs"][2]
# longform_revision: change one narrative paragraph text slightly to ensure reader change, keep structure
try:
    pkgs=new_auth["longform_revision"]["packages"]
    if pkgs and pkgs[0].get("narrative_sections"):
        secs=pkgs[0]["narrative_sections"]
        if secs and secs[0].get("paragraphs"):
            paras=secs[0]["paragraphs"]
            if paras and isinstance(paras[0], dict) and "text" in paras[0]:
                paras[0]["text"]="Fixture narrative-one paragraph one for pkg-001. Revised fixture sentence within approved evidence with LONGFORM editorial amendment."
except Exception as e:
    print(f"longform_revision tweak skipped: {e}")
dest=root/pdir_new/"authoring-input.json"
dest.parent.mkdir(parents=True, exist_ok=True)
if dest.exists():
    print(f"EXISTS {dest}")
    import sys as _s; _s.exit(2)
from scripts import survey_production_v2 as core
dest.write_bytes(core.json_bytes(new_auth))
print(f"staged {dest.relative_to(root)}")
"""
    pa = py_inline(prep_auth, [str(FIX), prop_new], "ed-stage-auth")
    assert pa is not None and pa.returncode==0, "stage auth failed"
    # P1 prepare_proposal 1200s (not 300)
    p1_code = r"""
import sys, json, faulthandler, os
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
faulthandler.dump_traceback_later(1100, exit=False)
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
import os as _os
print(f"P1 child PID={_os.getpid()}", flush=True)
issue="SP001"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
dest=root_p/pdir_new/"authoring-input.json"
print(f"P1 prepare {prop_new} start", flush=True)
res=p1mod.prepare_proposal(root_p, root_p/f"sources/{issue}/production-state.json", dest, prop_new, "LONGFORM renewal-to-editorial: changed reader on U4-active prior (synthetic, no genuine approval)")
print(f"P1 PREPARED keys={sorted(res.keys()) if isinstance(res,dict) else type(res).__name__}", flush=True)
# save proposal path for next steps
print(f"proposal {res.get('proposal',{}).get('path') if isinstance(res,dict) else 'unknown'}")
"""
    p1 = py_inline(p1_code, [str(FIX), prop_new], "ed-p1-prepare", timeout=1200)
    if p1 is None:
        print("P1 TIMEOUT blocker (1200s, no PASS)", flush=True)
        return 1
    assert p1.returncode==0, f"P1 failed {open(EVID/'ed-p1-prepare-stderr.txt').read()[:8000]}"
    print("P1 PREPARE OK", flush=True)
    # P2R capture_retention
    p2r_code = r"""
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
print(f"P2R CAPTURED {res.get('manifest_path') if isinstance(res,dict) else res}", flush=True)
"""
    p2r = py_inline(p2r_code, [str(FIX), prop_new], "ed-p2r-capture", timeout=1200)
    assert p2r is not None and p2r.returncode==0, f"P2R failed {open(EVID/'ed-p2r-capture-stderr.txt').read()[:8000] if (EVID/'ed-p2r-capture-stderr.txt').exists() else 'timeout'}"
    print("P2R OK", flush=True)
    # P2R verify
    # need manifest path: find via proposal dir? capture returns manifest_path, parse from stdout
    # For simplicity, call verify via python that discovers manifest
    p2r_verify_code = r"""
import sys, json, pathlib
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_retention_v2 as p2r
import os, glob
print(f"P2R-verify child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
# find manifest: look for retention-manifest.json under proposal dir
cands=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}").rglob("*retention*.json"))
print(f"cands={cands}")
# capture output manifest path is in previous stdout; re-derive: usually <proposal_dir>/retention-manifest.json or similar
# Try common names
for cand in cands:
    print(cand.relative_to(root_p))
# Use the one that verify expects: need manifest_path from capture; parse from capture stdout
import pathlib as pl
prev_out=open(pl.Path("notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-ed-20261025T090000Z/ed-p2r-capture-stdout.txt").read())
print(prev_out[:2000])
"""
    # Actually parse manifest from capture stdout file
    import re
    cap_out=open(EVID/"ed-p2r-capture-stdout.txt").read()
    print(f"P2R capture out: {cap_out[:2000]}", flush=True)
    # Continue to P2V, P3S etc. in next steps (to keep this runner bounded, do P2V now)
    p2v_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_editorial_current_authority_v2 as p2v
import os
print(f"P2V child PID={os.getpid()}", flush=True)
issue="SP001"
proposal=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}/proposal.json"
# find retention manifest
import glob as _g
cands=list((root_p/f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}").rglob("*.json"))
# filter retention
ret=[str(p.relative_to(root_p)) for p in cands if "retention" in p.name.lower()]
print(f"retention cands={ret}")
# pick first manifest that looks like retention-manifest
manifest=ret[0] if ret else None
print(f"manifest={manifest}")
# scope review may be None for initial observe? Try without scope
res=p2v.observe_current_authority(str(root_p), f"sources/{issue}/production-state.json", proposal, manifest)
print(f"P2V OBSERVED keys={sorted(res.keys()) if isinstance(res,dict) else type(res).__name__}", flush=True)
"""
    p2v = py_inline(p2v_code, [str(FIX), prop_new], "ed-p2v-observe", timeout=1200)
    if p2v is None:
        print("P2V TIMEOUT blocker", flush=True)
        return 1
    assert p2v.returncode==0, f"P2V failed {open(EVID/'ed-p2v-observe-stderr.txt').read()[:8000]}"
    print("P2V OK", flush=True)
    print("ED P1/P2R/P2V DONE (P3S/build/finalize/activate continue in next runner)", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
