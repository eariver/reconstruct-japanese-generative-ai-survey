#!/usr/bin/env python3
"""Continuation lifecycle — normal DIRECT on r6 U4 with G5 PUB fix."""
import os, sys, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/continuation-lifecycle-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def run(cmd,cwd,tag,timeout=1200,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        tmpdir=FIX.parent/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    print(f"START {tag}",flush=True)
    proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(LOG,"a") as fh: fh.write(f"$ {' '.join(cmd[:7])}... # {tag} -> exit={proc.returncode}\n")
    print(f"DONE {tag} exit={proc.returncode}",flush=True)
    return proc
PY=sys.executable
ISSUE="2026-W37"; PROP="wk-boot-1"; RID="high-u4-weekly"
now_iso=datetime.now(timezone.utc).isoformat()
LIFECYCLE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, issue, prop, rid, now_iso = sys.argv[1:6]
from pathlib import Path
from datetime import datetime
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod
assert str(Path(core.__file__).resolve()).startswith(str(root_p.resolve())), "fixture origin"
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / f"sources/{issue}/production-state.json"
state = json.loads(state_path.read_bytes())
sel = setmod.resolve_publication_selection(root_p, cfg, state)
assert sel.get("mode") == "VERSIONED_ACTIVE", sel.get("mode")
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
seal = json.loads((root_p / f"{r_dir}/publication-set.json").read_bytes())
roles = seal["roles"]
supplied = {"publication-candidate": root_p / roles["publication-candidate"]["path"],}
now = datetime.fromisoformat(now_iso)
stage_out = root_p / pdir / f"lifecycle-stage-{rid}-continuation.json"
stage.validate_stage(root_p, cfg, state_path, supplied, stage_out, now)
lc_dir = root_p / pdir / f"lifecycle-{rid}-continuation"
lc_dir.mkdir(parents=True, exist_ok=True)
appr = lc_dir / "preview-approval.json"
pubmod.build_preview_approval(root_p, supplied["publication-candidate"], appr,
    "continuation lifecycle synthetic preview; NO genuine Human approval",
    now, f"continuation:{rid}:synthetic-preview")
pubmod.validate_preview_approval(root_p, appr, issue_id=issue)
frz = lc_dir / "freeze-record.json"
man = lc_dir / "release-manifest.json"
pubmod.build_freeze(root_p, supplied["publication-candidate"], appr, now, frz, man)
pubmod.validate_release_manifest(root_p, man)
import subprocess as _sp
head = _sp.run(["git","rev-parse","HEAD"],cwd=str(root_p),capture_output=True,text=True).stdout.strip()
mv = lc_dir / "merge-verification.json"
pubmod.build_merge_verification(root_p, man, head, now, mv)
rel = lc_dir / "release-record.json"
pubmod.build_release_record(root_p, man, mv, now, f"continuation:{rid}:synthetic-release", rel)
from pypdf import PdfReader
pdf_path = root_p / roles["publication-pdf"]["path"]
pages = len(PdfReader(str(pdf_path)).pages)
print(json.dumps({"stage":str(stage_out.relative_to(root_p)),"approval":str(appr.relative_to(root_p)),
 "freeze":str(frz.relative_to(root_p)),"manifest":str(man.relative_to(root_p)),
 "merge":str(mv.relative_to(root_p)),"release":str(rel.relative_to(root_p)),
 "pdf_pages":pages,"head":head},indent=1))
"""
state_before=(FIX/f"sources/{ISSUE}/production-state.json").read_bytes()
lc=run([PY,"-c",LIFECYCLE, str(FIX), ISSUE, PROP, RID, now_iso], REPO, "cl-lifecycle")
print(f"lifecycle exit {lc.returncode}",flush=True)
if lc.returncode!=0:
    try: print(open(EVID/"cl-lifecycle-stderr.txt").read()[:8000],flush=True)
    except: pass
    sys.exit(1)
state_after=(FIX/f"sources/{ISSUE}/production-state.json").read_bytes()
print(f"State pinned={state_before==state_after} (artifact-level, no State mutation expected for this low-level path; public agent transitions to RELEASED separate)",flush=True)
print("LIFECYCLE DONE",flush=True)
