#!/usr/bin/env python3
"""Weekly STEP4 — renewal→editorial P1 prepare (changed-reader) on r5-active.
Fresh subprocess, 1200s timeout, monotonic recorded_at, wallclock separate.
"""
import os, sys, json, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/step4-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def run(cmd,cwd,tag,timeout=1200,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        tmpdir=FIX.parent/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    print(f"START {tag} timeout={timeout}s pid-parent={os.getpid()}",flush=True)
    proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(LOG,"a") as fh: fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={proc.returncode}\n")
    print(f"DONE {tag} exit={proc.returncode}",flush=True)
    return proc
PY=sys.executable
ISSUE="2026-W37"; PROP_OLD="wk-boot-1"; PROP_NEW="wk-ed-renew-3"
PDIR_OLD=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_OLD}"
PDIR_NEW=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}"
STATE=f"sources/{ISSUE}/production-state.json"
# predecessor max recorded_at (r5)
r5=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r5.json").read_bytes())
prev_max=r5.get("recorded_at","2026-10-25T05:36:08.844297+00:00")
try: prev_dt=datetime.fromisoformat(prev_max)
except: prev_dt=datetime.now(timezone.utc)-timedelta(seconds=10)
wall_now=datetime.now(timezone.utc)
synthetic=max(wall_now, prev_dt+timedelta(seconds=1))
now_iso=synthetic.isoformat()
print(f"wall_now {wall_now.isoformat()} prev_max {prev_max} synthetic recorded_at {now_iso}",flush=True)
(EVID/"recorded-at.json").write_text(json.dumps({"wallclock":wall_now.isoformat(),"prev_max":prev_max,"synthetic_recorded_at":now_iso},indent=1))
# stage new authoring from current authoring (Weekly envelope edit)
old_auth=json.loads((FIX/PDIR_OLD/"authoring-input.json").read_bytes())
new_auth=json.loads(json.dumps(old_auth))
new_auth["cover"]["headline"]="Weekly tested method, revised edition + renewal editorial (changed-reader)"
new_auth["cover"]["deck"]="Source-based survey with renewal-editorial amendment; synthetic fixture, no genuine approval."
new_auth["final_summary"]["paragraphs"]=["The edition surveys one source with renewal-editorial changed reader.",
 "The claims remain attributed; renewal proof fresh, tool epoch G4.",
 "The accepted source authors describe the tested method."]
assert json.dumps(new_auth,sort_keys=True)!=json.dumps(old_auth,sort_keys=True)
dest=FIX/PDIR_NEW/"authoring-input.json"
# ensure new ID not exists (preserve old partials, new id)
if dest.exists():
    print(f"FATAL target exists {dest} (use new id, preserve partial)",flush=True); sys.exit(1)
dest.parent.mkdir(parents=True,exist_ok=True)
# write via fixture core.json_bytes in fresh subprocess (no top-level import)
import hashlib
# Use fixture core via fresh subprocess to write canonical bytes
write_code = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
import sys as _s
root=Path(sys.argv[1]); rel=sys.argv[2]
data=json.loads(sys.argv[3])
p=root/rel
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes(data))
print(f"WROTE {rel}")
"""
# Pass new_auth as JSON arg (may be large, but okay)
proc=run([PY,"-c",write_code, str(FIX), str(dest.relative_to(FIX)), json.dumps(new_auth)], REPO, "s4-stage-authoring")
if proc.returncode!=0: print("FATAL stage authoring",flush=True); sys.exit(1)
# P1 prepare (read-only, no writes by P1)
P1_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, state_rel, auth_rel, prop_new, change_desc, now_iso = sys.argv[1:7]
from pathlib import Path
root_p=Path(root)
from scripts import survey_editorial_correction_proposal_v2 as p1mod
from scripts import survey_production_v2 as core
assert str(Path(p1mod.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
res=p1mod.prepare_proposal(root_p, root_p/state_rel, root_p/auth_rel, prop_new, change_desc)
print(json.dumps({"proposal_id":prop_new,"keys":sorted(res.keys()),"proposal_path":res.get("proposal_path",""),"basis_kind":res.get("proposal",{}).get("kind","")},indent=1))
"""
p1=run([PY,"-c",P1_CODE, str(FIX), STATE, str(dest.relative_to(FIX)), PROP_NEW, "Renewal-to-editorial: changed reader on r5-active prior (Weekly envelope edit, synthetic, no genuine approval)", now_iso], REPO, "s4-p1-prepare", timeout=1200)
print(f"P1 prepare exit {p1.returncode}",flush=True)
if p1.returncode!=0:
    print("P1 FAILED — check stderr for exact file/predicate/oracle",flush=True)
    try: print(open(EVID/"s4-p1-prepare-stderr.txt").read()[:5000],flush=True)
    except: pass
    sys.exit(1)
print("STEP4 P1 SUCCESS",flush=True)
