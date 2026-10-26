#!/usr/bin/env python3
"""Continuation P1 — renewal→editorial changed-reader on r6-active (G5 tools)."""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/continuation-p1-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def run(cmd,cwd,tag,timeout=1200,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        tmpdir=FIX.parent/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    print(f"START {tag} timeout={timeout}s",flush=True)
    proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(LOG,"a") as fh: fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={proc.returncode}\n")
    print(f"DONE {tag} exit={proc.returncode}",flush=True)
    return proc
PY=sys.executable
ISSUE="2026-W37"; PROP_OLD="wk-boot-1"; PROP_NEW="wk-ed-renew-4"
PDIR_OLD=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_OLD}"
PDIR_NEW=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}"
STATE=f"sources/{ISSUE}/production-state.json"
r6=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r6.json").read_bytes())
prev_max=r6.get("recorded_at")
prev_dt=datetime.fromisoformat(prev_max)
wall_now=datetime.now(timezone.utc)
synthetic=max(wall_now, prev_dt+timedelta(seconds=1))
now_iso=synthetic.isoformat()
print(f"wall {wall_now.isoformat()} prev {prev_max} synthetic {now_iso}",flush=True)
(EVID/"recorded-at.json").write_text(json.dumps({"wallclock":wall_now.isoformat(),"prev_max":prev_max,"synthetic":now_iso},indent=1))
old_auth=json.loads((FIX/PDIR_OLD/"authoring-input.json").read_bytes())
new_auth=json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"]="Weekly tested method, revised edition + renewal editorial G5 (changed-reader)"
new_auth["cover"]["deck"]="Source-based survey with G5 renewal-editorial amendment; synthetic fixture, no genuine approval."
new_auth["final_summary"]["paragraphs"]=["The edition surveys one source with G5 renewal-editorial changed reader.",
 "The claims remain attributed; renewal proof fresh, tool epoch G5.",
 "The accepted source authors describe the tested method."]
assert json.dumps(new_auth,sort_keys=True)!=json.dumps(old_auth,sort_keys=True)
dest=FIX/PDIR_NEW/"authoring-input.json"
if dest.exists():
    print(f"FATAL target exists {dest}",flush=True); sys.exit(1)
dest.parent.mkdir(parents=True,exist_ok=True)
write_code = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]
data=json.loads(sys.argv[3])
p=root/rel
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes(data))
print(f"WROTE {rel}")
"""
proc=run([PY,"-c",write_code, str(FIX), str(dest.relative_to(FIX)), json.dumps(new_auth)], REPO, "cp1-stage-authoring")
if proc.returncode!=0: print("FATAL stage",flush=True); sys.exit(1)
P1_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, state_rel, auth_rel, prop_new, change_desc, now_iso = sys.argv[1:7]
from pathlib import Path
root_p=Path(root)
from scripts import survey_editorial_correction_proposal_v2 as p1mod
assert str(Path(p1mod.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
res=p1mod.prepare_proposal(root_p, root_p/state_rel, root_p/auth_rel, prop_new, change_desc)
print(json.dumps({"proposal_id":prop_new,"keys":sorted(res.keys()),"proposal_path":res.get("proposal_path","")},indent=1))
"""
p1=run([PY,"-c",P1_CODE, str(FIX), STATE, str(dest.relative_to(FIX)), PROP_NEW, "Renewal-to-editorial G5: changed reader on r6-active prior (Weekly envelope, synthetic)", now_iso], REPO, "cp1-p1-prepare", timeout=1200)
print(f"P1 exit {p1.returncode}",flush=True)
if p1.returncode!=0:
    print("P1 FAILED",flush=True)
    try: print(open(EVID/"cp1-p1-prepare-stderr.txt").read()[:8000],flush=True)
    except: pass
    sys.exit(1)
print("P1 SUCCESS",flush=True)
