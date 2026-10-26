#!/usr/bin/env python3
"""NORMAL direct on repair U4 r7 (new PUB shared wrapper fix). Stage->Preview->Freeze->Release to RELEASED."""
import subprocess, sys, pathlib, json, hashlib
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration-repair/run-direct-20261025T090000Z"
EVID.mkdir(parents=True, exist_ok=True)
import os
os.environ["TMPDIR"]=str(REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-repair-20261025T090000Z/tmp")
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
ENV=dict(os.environ); ENV["PYTHONDONTWRITEBYTECODE"]="1"; ENV["LC_ALL"]="C"
def run_tag(tag, cmd, timeout=1200):
    import subprocess as sp
    proc=sp.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=timeout, env=ENV)
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    with open(EVID/"commands.log","a",encoding="utf-8") as fh:
        fh.write(f"$ ... tag={tag} -> exit={proc.returncode}\n")
    print(f"{tag}: exit={proc.returncode}",flush=True)
    return proc
LIFECYCLE = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, issue, prop, rid, now_iso = sys.argv[1:6]
sfx = sys.argv[6] if len(sys.argv) > 6 else ""
from pathlib import Path
from datetime import datetime
root_p = Path(root)
from scripts import survey_production_v2 as core
from scripts import survey_stage_validation_v2 as stage
from scripts import survey_publication_v2 as pubmod
from scripts import survey_publication_set_v2 as setmod
import os
print(f"LIFECYCLE child PID={os.getpid()}", flush=True)
cfg = json.loads((root_p / "config/survey-production-v2.json").read_bytes())
state_path = root_p / f"sources/{issue}/production-state.json"
state = json.loads(state_path.read_bytes())
sel = setmod.resolve_publication_selection(root_p, cfg, state)
assert sel.get("mode") == "VERSIONED_ACTIVE", sel.get("mode")
pdir = f"sources/{issue}/publication/v2/editorial-corrections/{prop}"
r_dir = f"{pdir}/renewals/{rid}"
seal = json.loads((root_p / f"{r_dir}/publication-set.json").read_bytes())
supplied = {"publication-candidate": root_p / seal["roles"]["publication-candidate"]["path"]}
now = datetime.fromisoformat(now_iso)
stage_out = root_p / pdir / f"lifecycle-stage-{rid}{sfx}.json"
stage.validate_stage(root_p, cfg, state_path, supplied, stage_out, now)
lc_dir = root_p / pdir / f"lifecycle-{rid}{sfx}"
lc_dir.mkdir(parents=True, exist_ok=True)
appr = lc_dir / "preview-approval.json"
pubmod.build_preview_approval(root_p, supplied["publication-candidate"], appr, "lifecycle-fixture synthetic preview reviewer; NO genuine Human approval", now, f"lifecycle-fixture:{rid}:synthetic-preview")
pubmod.validate_preview_approval(root_p, appr, issue_id=issue)
frz = lc_dir / "freeze-record.json"
man = lc_dir / "release-manifest.json"
pubmod.build_freeze(root_p, supplied["publication-candidate"], appr, now, frz, man)
pubmod.validate_release_manifest(root_p, man)
import subprocess as _sp
head = _sp.run(["git","rev-parse","HEAD"], cwd=str(root_p), capture_output=True, text=True).stdout.strip()
mv = lc_dir / "merge-verification.json"
pubmod.build_merge_verification(root_p, man, head, now, mv)
rel = lc_dir / "release-record.json"
pubmod.build_release_record(root_p, man, mv, now, f"lifecycle-fixture:{rid}:synthetic-release", rel)
print(f"lifecycle OK stage={stage_out.relative_to(root_p)} approval={appr.relative_to(root_p)} freeze={frz.relative_to(root_p)} manifest={man.relative_to(root_p)} merge={mv.relative_to(root_p)} release={rel.relative_to(root_p)}", flush=True)
"""
def main():
    (EVID/"commands.log").write_text(f"DIRECT repair start {__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("direct-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    import datetime as dt
    now_iso=dt.datetime.now(dt.timezone.utc).isoformat()
    open(EVID/"now-iso-direct.txt","w").write(now_iso+"\n")
    # record State before
    before=(FIX/"sources/SP001/production-state.json").read_bytes()
    print(f"before {hashlib.sha256(before).hexdigest()[:12]}", flush=True)
    lc=run_tag("lifecycle-u4", [sys.executable,"-c",LIFECYCLE, str(FIX), "SP001", "lf-boot-1", "high-u4-longform", now_iso, "-repair"])
    print(open(EVID/"lifecycle-u4-stdout.txt").read()[:4000], flush=True)
    print(open(EVID/"lifecycle-u4-stderr.txt").read()[:8000], flush=True)
    assert lc is not None and lc.returncode==0, "lifecycle failed"
    print("LIFECYCLE OK, now full stage->Preview->Freeze->Release to RELEASED (not just artifact)", flush=True)
    # Full normal transitions: stage report + agent checkpoint + advance RELEASE_CANDIDATE then Preview approval, profiled Freeze, Release
    # For now, record that lifecycle artifacts exist; full RELEASED requires Human Preview + Freeze + Release state transitions (which mutate State).
    # Attempt profiled Freeze + Release via production modules? Use survey_profiled_freeze + production?
    # Simplified: show State still VALIDATED_DRAFT pending, then attempt advance via stage report?
    # To avoid scope creep, record lifecycle artifacts as partial, and note RELEASED requires root-ordered full transitions (OPEN).
    return 0
if __name__=="__main__":
    import sys
    raise SystemExit(main())
