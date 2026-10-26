#!/usr/bin/env python3
"""LONGFORM renewal->editorial retry after alias cleanup (lf-ed-2)."""
import subprocess, sys, json, os, pathlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-ed-direct-20261025T060000Z"
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
TIMEOUT=1200
def run_tag(tag, cmd, timeout=TIMEOUT):
    proc=subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
probe_code = r"""
import sys, json, faulthandler
sys.path.insert(0, sys.argv[1])
root_arg=sys.argv[1]; prop_new=sys.argv[2]
faulthandler.dump_traceback_later(300, exit=True)
from pathlib import Path
root_p=Path(root_arg)
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as p1mod
import os
print(f"ED retry child PID={os.getpid()}", flush=True)
issue="SP001"
pdir_old=f"sources/{issue}/publication/v2/editorial-corrections/lf-boot-1"
pdir_new=f"sources/{issue}/publication/v2/editorial-corrections/{prop_new}"
old_auth=json.loads((root_p/pdir_old/"authoring-input.json").read_bytes())
new_auth=json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"]="LONGFORM renewal-editorial retry headline: fixture-local changed reader after versioned renewal U3b; no genuine approval."
new_auth["cover"]["deck"]="Changed deck retry for P1 on U3b-active prior (LONGFORM lf-ed-2)."
new_auth["final_summary"]["paragraphs"]=["Changed retry paragraph: must NOT trip NO_EDITORIAL_CHANGE; prior KEEP with fresh COPY. LONGFORM lf-ed-2."]
assert json.dumps(new_auth,sort_keys=True)!=json.dumps(old_auth,sort_keys=True)
dest=root_p/pdir_new/"authoring-input.json"
dest.parent.mkdir(parents=True, exist_ok=True)
if dest.exists():
    print(json.dumps({"probe":"REFUSED_TARGET_EXISTS","path":str(dest.relative_to(root_p))}))
    sys.exit(0)
dest.write_bytes(core.json_bytes(new_auth))
print(f"staged {dest.relative_to(root_p)}", flush=True)
res=p1mod.prepare_proposal(root_p, root_p/f"sources/{issue}/production-state.json", dest, prop_new, "LONGFORM renewal-to-editorial retry: changed reader on U3b-active prior (synthetic)")
print(json.dumps({"probe":"PREPARED","proposal_id":prop_new,"keys":sorted(res.keys()) if isinstance(res,dict) else type(res).__name__}))
"""
p = run_tag("ed-probe-retry", [sys.executable,"-c",probe_code, str(FIX), "lf-ed-2"], timeout=1200)
print(open(EVID/"ed-probe-retry-stdout.txt").read()[:5000])
print(open(EVID/"ed-probe-retry-stderr.txt").read()[:8000])
