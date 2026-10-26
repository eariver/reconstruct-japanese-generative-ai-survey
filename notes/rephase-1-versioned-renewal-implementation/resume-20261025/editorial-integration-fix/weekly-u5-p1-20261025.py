#!/usr/bin/env python3
"""Weekly U5 (after second P1 fix) + P1 editorial."""
import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = REPO / ".rephase-1-editorial-runtime/versioned-renewal-editorial-fix-20261025T063145Z"
FIX = BASE / "renewal-weekly-fix"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-integration-fix/weekly-20261025T063145Z/u5-p1-20261025T070000Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def log(m):
    print(m,flush=True)
    open(LOG,"a").write(m+"\n")
def run(cmd,cwd,tag,timeout=1200,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_CONFIG_GLOBAL"]="/dev/null"; env["GIT_OPTIONAL_LOCKS"]="0"
        tmpdir=BASE/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    log(f"$ {' '.join(cmd[:5])}... # {tag}")
    try:
        proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    except subprocess.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("",encoding="utf-8"); (EVID/f"{tag}-stderr.txt").write_text(f"Timeout {timeout}s\n",encoding="utf-8"); (EVID/f"{tag}-exit.txt").write_text("TIMEOUT",encoding="utf-8")
        log(f"DONE {tag} TIMEOUT"); return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8"); (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8"); (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}"); return proc
PY=sys.executable; ISSUE="2026-W37"; STATE=f"sources/{ISSUE}/production-state.json"
state=json.loads((FIX/STATE).read_bytes())
active=state.get("publication_revalidation_provenance",{}).get("path","")
log(f"active {active}")
r6=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r6.json").read_bytes())
prev_max=r6.get("recorded_at"); log(f"prior r6 {prev_max}")
prev_dt=datetime.fromisoformat(prev_max); wall_now=datetime.now(timezone.utc); synthetic=max(wall_now, prev_dt+timedelta(seconds=5)); now_iso=synthetic.isoformat()
(EVID/"recorded-at.json").write_text(json.dumps({"wall":wall_now.isoformat(),"prev":prev_max,"syn":now_iso},indent=1)); log(f"syn {now_iso}")
U_ID="high-u5-fix-weekly"
PREP=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.prepare_renewal(root, root/sys.argv[2], sys.argv[3], "REUSE_TARGETS", "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json", None, "weekly-fix-u5", sys.argv[4])
print(json.dumps(out,indent=1))
"""
p1=run([PY,"-c",PREP,str(FIX),STATE,U_ID,now_iso],REPO,"u5-prepare",timeout=600)
if p1 is None or p1.returncode!=0: log("FATAL prepare"); sys.exit(1)
basis_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/renewal-basis.json"
# QA
import json as _js
u3_qa=_js.loads((FIX/f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewal-qa-checks-high-u4-fix-weekly.json").read_bytes())
checks=u3_qa["checks"] if isinstance(u3_qa,dict) and "checks" in u3_qa else u3_qa
for c in checks: c["recorded_at"]=now_iso
new_qa_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewal-qa-checks-{U_ID}.json"
WQA=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]; data=json.loads(sys.argv[3])
p=root/rel
if p.exists(): print(f"EXISTS {rel}"); sys.exit(1)
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes({"checks": data} if isinstance(data,list) else data))
print(f"WROTE {rel}")
"""
pq=run([PY,"-c",WQA,str(FIX),new_qa_rel,json.dumps(checks)],REPO,"u5-qa-write",timeout=120)
if pq is None or pq.returncode!=0: log("FATAL qa"); sys.exit(1)
FIN=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.finalize_renewal(root, root/sys.argv[2], root/sys.argv[3], root/sys.argv[4], None, None, "weekly-fix-u5", sys.argv[5])
print(json.dumps(out,indent=1))
"""
p2=run([PY,"-c",FIN,str(FIX),STATE,basis_rel,new_qa_rel,now_iso],REPO,"u5-finalize",timeout=600)
if p2 is None or p2.returncode!=0: log("FATAL finalize"); sys.exit(1)
set_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/publication-set.json"
act_iso=(synthetic+timedelta(seconds=5)).isoformat()
ACT=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
out=high.activate_renewal(root, root/sys.argv[2], root/sys.argv[3], "Renewal Core change: P1 second fix verification (truthful, synthetic)", "weekly-fix-u5", sys.argv[4])
print(json.dumps(out,indent=1))
"""
p3=run([PY,"-c",ACT,str(FIX),STATE,set_rel,act_iso],REPO,"u5-activate",timeout=600)
if p3 is None or p3.returncode!=0: log("FATAL activate"); sys.exit(1)
state2=json.loads((FIX/STATE).read_bytes()); new_rec=state2.get("publication_revalidation_provenance",{}).get("path",""); log(f"new active {new_rec}")
HIST=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_versioned_renewal_v2 as high
root=Path(sys.argv[1])
v=high.verify_renewal_history(root, root/sys.argv[2])
print(json.dumps({"HIST":v.get("HISTORICAL_IDENTITY_VERIFIED"),"len":v.get("chain_length")},indent=1))
"""
p4=run([PY,"-c",HIST,str(FIX),new_rec],REPO,"u5-history",timeout=600)
if p4 is None or p4.returncode!=0: log("FATAL history"); sys.exit(1)
# P1
PROP_NEW="wk-ed-fix-2"
OLD_AUTH=json.loads((FIX/f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/authoring-input.json").read_bytes())
NEW_AUTH=json.loads(json.dumps(OLD_AUTH))
NEW_AUTH["cover"]["headline"]="Weekly tested method, revised edition + P1-fix2 editorial (changed-reader)"
NEW_AUTH["cover"]["deck"]="Source-based survey with P1-fix2 renewal-editorial amendment; synthetic, no genuine approval."
NEW_AUTH["final_summary"]["paragraphs"]=["The edition surveys one source with P1-fix2 renewal-editorial changed reader.","The claims remain attributed; renewal proof fresh, tool epoch fix2.","The accepted source authors describe the tested method."]
STAGE=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]; data=json.loads(sys.argv[3])
p=root/rel
if p.exists(): print(f"EXISTS {rel}"); sys.exit(1)
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes(data))
print(f"WROTE {rel}")
"""
dest_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}/authoring-input.json"
ps=run([PY,"-c",STAGE,str(FIX),dest_rel,json.dumps(NEW_AUTH)],REPO,"p1-stage",timeout=120)
if ps is None or ps.returncode!=0: log("FATAL stage"); sys.exit(1)
P1C=r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_editorial_correction_proposal_v2 as p1mod
root=Path(sys.argv[1])
res=p1mod.prepare_proposal(root, root/sys.argv[2], root/sys.argv[3], sys.argv[4], sys.argv[5])
print(json.dumps({"id":sys.argv[4],"nodes":len(res["graph"]["nodes"]),"edges":len(res["graph"]["edges"])},indent=1))
"""
pp=run([PY,"-c",P1C,str(FIX),STATE,dest_rel,PROP_NEW,"P1-fix2 renewal-to-editorial on r7-active (Weekly, synthetic)"],REPO,"p1-prepare",timeout=1200)
log(f"P1 exit={pp.returncode if pp else 'TIMEOUT'}")
if pp is None or pp.returncode!=0: log("P1 FAILED"); sys.exit(1)
log("WEEKLY U5+P1 SUCCESS")
