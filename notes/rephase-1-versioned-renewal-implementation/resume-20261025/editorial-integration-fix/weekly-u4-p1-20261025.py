#!/usr/bin/env python3
"""Weekly U4 (fresh REUSE after P1 fix) + P1 editorial prepare positive.
Fresh Python per tool commit, new IDs time>=prior, preserve invalid orphan.
"""
import os, sys, json, subprocess, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
BASE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-editorial-fix-20261025T063145Z")
FIX = BASE / "renewal-weekly-fix"
# Find latest EVID dir (weekly-*)
EVID_PARENT = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-integration-fix"
candidates = sorted([p for p in (EVID_PARENT).glob("weekly-*") if p.is_dir()])
EVID = candidates[-1] / "u4-p1-20261025T063500Z"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")

def log(m):
    print(m, flush=True)
    with open(LOG, "a") as fh:
        fh.write(m+"\n")

def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env=dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_CONFIG_GLOBAL"]="/dev/null"; env["GIT_OPTIONAL_LOCKS"]="0"
        tmpdir=BASE/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    log(f"$ {' '.join(cmd[:5])}... # {tag} timeout={timeout}s pid={os.getpid()}")
    try:
        proc=subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as exc:
        (EVID/f"{tag}-stdout.txt").write_text("", encoding="utf-8")
        (EVID/f"{tag}-stderr.txt").write_text(f"Timeout ({timeout}s)! PID-parent={os.getpid()}\n", encoding="utf-8")
        (EVID/f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        log(f"DONE {tag} TIMEOUT")
        return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}")
    return proc

PY=sys.executable
ISSUE="2026-W37"
STATE=f"sources/{ISSUE}/production-state.json"
# Prior r5
r5=json.loads((FIX/f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r5.json").read_bytes())
prev_max=r5.get("recorded_at")
log(f"prior r5 {r5.get('recorded_at')} sha {hashlib.sha256((FIX/f'sources/{ISSUE}/publication/v2/publication-surface-revalidation-r5.json').read_bytes()).hexdigest()[:8]}")
try:
    prev_dt=datetime.fromisoformat(prev_max)
except:
    prev_dt=datetime.now(timezone.utc)-timedelta(seconds=10)
wall_now=datetime.now(timezone.utc)
synthetic=max(wall_now, prev_dt+timedelta(seconds=5))
now_iso=synthetic.isoformat()
(EVID/"recorded-at.json").write_text(json.dumps({"wallclock":wall_now.isoformat(),"prev_max":prev_max,"synthetic":now_iso},indent=1))
log(f"synthetic {now_iso}")

# 0. Old proof stale check (detached CURRENT, must FAIL with new P1 tools)
STALE_CODE = r"""
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root=Path(sys.argv[1])
from scripts import survey_versioned_renewal_v2 as high
try:
    v=high.validate_renewal_receipt(root, sys.argv[2])
    print("STALE_UNEXPECTED_PASS")
    sys.exit(0)
except Exception as e:
    print(f"STALE_REFUSED {type(e).__name__}: {e}")
    sys.exit(2)
"""
old_receipt="sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u3-weekly/validated-source-manifest.json"
p0=run([PY,"-c",STALE_CODE,str(FIX),old_receipt], REPO, "stale-old-u3", timeout=300)
log(f"stale check exit={p0.returncode if p0 else 'TIMEOUT'} (expected 2 REFUSED)")

# 1. Fresh U4 prepare/finalize/activate/history (REUSE_TARGETS, prior r5)
U_ID="high-u4-fix-weekly"
U_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, state_rel, renewal_id, now_iso = sys.argv[1:5]
from pathlib import Path
root=Path(root_s)
from scripts import survey_versioned_renewal_v2 as high
from scripts import survey_production_v2 as core
# prepare
basis=high.prepare_renewal(root, root/state_rel, renewal_id, "REUSE_TARGETS", "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json", None, "weekly-fix-u4", now_iso)
print(json.dumps({"basis":basis["basis_path"],"requested":basis["requested"]}))
"""
# Need manuscript-spec path: check exists
mspec=FIX/"sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json"
log(f"mspec exists={mspec.is_file()}")
# Use fresh subprocess per tool commit as in weekly drivers: prepare, qa, finalize, activate, history each via separate python -c
# For brevity, use high-level sequence via multiple run() calls with distinct code blocks

PREP_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, state_rel, rid, now_iso = sys.argv[1:5]
from pathlib import Path
root=Path(root_s)
from scripts import survey_versioned_renewal_v2 as high
out=high.prepare_renewal(root, root/state_rel, rid, "REUSE_TARGETS", "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json", None, "weekly-fix-u4", now_iso)
print(json.dumps(out, indent=1))
"""
p1=run([PY,"-c",PREP_CODE,str(FIX),STATE,U_ID,now_iso], REPO, "u4-prepare", timeout=600)
if p1 is None or p1.returncode!=0:
    log("FATAL u4-prepare"); sys.exit(1)
# Find basis path from stdout? Parse last json? Simpler: basis path is deterministic: sources/.../renewals/<id>/renewal-basis.json
basis_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/renewal-basis.json"
log(f"basis_rel {basis_rel} exists={(FIX/basis_rel).is_file()}")

# QA checks: need fresh QA file with recorded_at >= basis. Use existing U3 QA as template but update recorded_at to now_iso
import json as _js
u3_qa_path=FIX/f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewal-qa-checks-high-u3-weekly.json"
u3_qa=_js.loads(u3_qa_path.read_bytes())
# u3_qa may be {"checks":[...]} or [...]? Check
log(f"u3_qa keys={list(u3_qa.keys()) if isinstance(u3_qa,dict) else 'list'}")
if isinstance(u3_qa, dict) and "checks" in u3_qa:
    checks=u3_qa["checks"]
else:
    checks=u3_qa
# Update recorded_at to now_iso for freshness
for c in checks:
    c["recorded_at"]=now_iso
new_qa_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewal-qa-checks-{U_ID}.json"
# Write via core.json_bytes in fresh subprocess (no direct write to preserve pin? Actually fixture operator stages QA outside high; direct write via python is okay as operator)
WRITE_QA = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]; data=json.loads(sys.argv[3])
p=root/rel
p.parent.mkdir(parents=True, exist_ok=True)
# Exclusive: refuse if exists
if p.exists():
    print(f"EXISTS {rel}"); sys.exit(1)
p.write_bytes(core.json_bytes({"checks": data} if isinstance(data, list) else data))
print(f"WROTE {rel}")
"""
# Need to pass checks as json arg
pqa_write=run([PY,"-c",WRITE_QA,str(FIX),new_qa_rel,json.dumps(checks)], REPO, "u4-qa-write", timeout=120)
if pqa_write is None or pqa_write.returncode!=0:
    log("FATAL qa write"); sys.exit(1)

FINAL_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, state_rel, basis_rel, qa_rel, now_iso = sys.argv[1:6]
from pathlib import Path
root=Path(root_s)
from scripts import survey_versioned_renewal_v2 as high
out=high.finalize_renewal(root, root/state_rel, root/basis_rel, root/qa_rel, None, None, "weekly-fix-u4", now_iso)
print(json.dumps(out, indent=1))
"""
p2=run([PY,"-c",FINAL_CODE,str(FIX),STATE,basis_rel,new_qa_rel,now_iso], REPO, "u4-finalize", timeout=600)
if p2 is None or p2.returncode!=0:
    log("FATAL u4-finalize"); sys.exit(1)

# Activate: need set path from finalize stdout? Parse? Finalize returns seal path? Let's inspect finalize return keys via stdout
# For simplicity, derive set path deterministic: renewals/<id>/publication-set.json
set_rel=f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/renewals/{U_ID}/publication-set.json"
log(f"set_rel {set_rel} exists={(FIX/set_rel).is_file()}")

ACT_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, state_rel, set_rel, now_iso = sys.argv[1:5]
from pathlib import Path
root=Path(root_s)
from scripts import survey_versioned_renewal_v2 as high
out=high.activate_renewal(root, root/state_rel, root/set_rel, "Renewal Core change: P1 dispatch fix verification (truthful Core-change, synthetic, no genuine approval)", "weekly-fix-u4", now_iso)
print(json.dumps(out, indent=1))
"""
# Need later time for activate (>= finalize)? Use now_iso + 5s
act_iso=(synthetic+timedelta(seconds=5)).isoformat()
(EVID/"recorded-at-activate.json").write_text(json.dumps({"activate":act_iso},indent=1))
p3=run([PY,"-c",ACT_CODE,str(FIX),STATE,set_rel,act_iso], REPO, "u4-activate", timeout=600)
if p3 is None or p3.returncode!=0:
    log("FATAL u4-activate"); sys.exit(1)

HIST_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, record_rel = sys.argv[1:3]
from pathlib import Path
root=Path(root_s)
from scripts import survey_versioned_renewal_v2 as high
v=high.verify_renewal_history(root, root/record_rel)
print(json.dumps({"HISTORICAL_IDENTITY_VERIFIED": v.get("HISTORICAL_IDENTITY_VERIFIED"), "chain_length": v.get("chain_length")}, indent=1))
"""
# Find new record path: sources/.../publication-surface-revalidation-r6.json (since r5 was prior, new should be r6)
# Check which r exists now
import pathlib as _pl
records=sorted((FIX/f"sources/{ISSUE}/publication/v2").glob("publication-surface-revalidation-r*.json"))
log(f"records={[p.name for p in records]}")
# New record should be r6 (since r5 existed, r6 next). Verify via state pointer
state=json.loads((FIX/STATE).read_bytes())
new_rec=state.get("publication_revalidation_provenance",{}).get("path","")
log(f"active record {new_rec}")
p4=run([PY,"-c",HIST_CODE,str(FIX),new_rec], REPO, "u4-history", timeout=600)
if p4 is None or p4.returncode!=0:
    log("FATAL u4-history"); sys.exit(1)

# 2. P1 editorial prepare positive on new r6-active with changed reader (new ID, preserve orphans)
PROP_NEW="wk-ed-fix-1"
PDIR_NEW=f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP_NEW}"
# Stage new authoring via core.json_bytes in fresh subprocess
OLD_AUTH=json.loads((FIX/f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-boot-1/authoring-input.json").read_bytes())
NEW_AUTH=json.loads(json.dumps(OLD_AUTH))
NEW_AUTH["cover"]["headline"]="Weekly tested method, revised edition + P1-fix editorial (changed-reader)"
NEW_AUTH["cover"]["deck"]="Source-based survey with P1-fix renewal-editorial amendment; synthetic fixture, no genuine approval."
NEW_AUTH["final_summary"]["paragraphs"]=["The edition surveys one source with P1-fix renewal-editorial changed reader.",
 "The claims remain attributed; renewal proof fresh, tool epoch fix.",
 "The accepted source authors describe the tested method."]
assert json.dumps(NEW_AUTH,sort_keys=True)!=json.dumps(OLD_AUTH,sort_keys=True)
STAGE_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
from pathlib import Path
from scripts import survey_production_v2 as core
root=Path(sys.argv[1]); rel=sys.argv[2]; data=json.loads(sys.argv[3])
p=root/rel
if p.exists():
    print(f"EXISTS {rel}"); sys.exit(1)
p.parent.mkdir(parents=True,exist_ok=True)
p.write_bytes(core.json_bytes(data))
print(f"WROTE {rel}")
"""
dest_rel=f"{PDIR_NEW}/authoring-input.json"
ps=run([PY,"-c",STAGE_CODE,str(FIX),dest_rel,json.dumps(NEW_AUTH)], REPO, "p1-stage-authoring", timeout=120)
if ps is None or ps.returncode!=0:
    log("FATAL stage"); sys.exit(1)

P1_CODE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root_s, state_rel, auth_rel, prop_new, change_desc = sys.argv[1:6]
from pathlib import Path
root=Path(root_s)
from scripts import survey_editorial_correction_proposal_v2 as p1mod
res=p1mod.prepare_proposal(root, root/state_rel, root/auth_rel, prop_new, change_desc)
print(json.dumps({"proposal_id":prop_new,"graph_nodes":len(res["graph"]["nodes"]),"graph_edges":len(res["graph"]["edges"]),"before_sha":res["proposal"]["basis"]["active_reader_input_ref"]["sha256"][:8],"planned_sha":res["proposal"]["proposed"]["proposed_reader_canonical_sha256"][:8]}, indent=1))
"""
pp=run([PY,"-c",P1_CODE,str(FIX),STATE,dest_rel,PROP_NEW,"P1-fix renewal-to-editorial: changed reader on r6-active prior (Weekly envelope edit, synthetic, no genuine approval)"], REPO, "p1-prepare", timeout=1200)
log(f"P1 prepare exit={pp.returncode if pp else 'TIMEOUT'} (expected 0)")
if pp is None or pp.returncode!=0:
    log("P1 FAILED - see stderr"); sys.exit(1)
log("WEEKLY U4+P1 SUCCESS")
