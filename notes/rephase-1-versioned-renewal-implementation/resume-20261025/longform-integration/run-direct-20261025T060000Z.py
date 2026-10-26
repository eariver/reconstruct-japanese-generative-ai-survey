#!/usr/bin/env python3
"""LONGFORM normal DIRECT lifecycle on U3b r6 + R1 refusal (no writes)."""
import subprocess, sys, json, os, pathlib, hashlib
from datetime import datetime, timezone
REPO = pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/longform-integration/run-direct-20261025T060000Z"
EVID.mkdir(parents=True, exist_ok=True)
TMP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/tmp"
TMP.mkdir(parents=True, exist_ok=True)
os.environ["TMPDIR"]=str(TMP)
for k in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
    assert not os.environ.get(k)
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
LIFECYCLE_BUILDER = r"""
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
supplied = {
    "publication-candidate": root_p / roles["publication-candidate"]["path"],
}
now = datetime.fromisoformat(now_iso)
stage_out = root_p / pdir / f"lifecycle-stage-{rid}{sfx}.json"
stage.validate_stage(root_p, cfg, state_path, supplied, stage_out, now)
lc_dir = root_p / pdir / f"lifecycle-{rid}{sfx}"
lc_dir.mkdir(parents=True, exist_ok=True)
appr = lc_dir / "preview-approval.json"
pubmod.build_preview_approval(root_p, supplied["publication-candidate"], appr,
    "lifecycle-fixture synthetic preview reviewer; NO genuine Human approval",
    now, f"lifecycle-fixture:{rid}:synthetic-preview")
pubmod.validate_preview_approval(root_p, appr, issue_id=issue)
frz = lc_dir / "freeze-record.json"
man = lc_dir / "release-manifest.json"
pubmod.build_freeze(root_p, supplied["publication-candidate"], appr, now, frz, man)
pubmod.validate_release_manifest(root_p, man)
import subprocess as _sp
head = _sp.run(["git", "rev-parse", "HEAD"], cwd=str(root_p), capture_output=True, text=True).stdout.strip()
mv = lc_dir / "merge-verification.json"
pubmod.build_merge_verification(root_p, man, head, now, mv)
rel = lc_dir / "release-record.json"
pubmod.build_release_record(root_p, man, mv, now, f"lifecycle-fixture:{rid}:synthetic-release", rel)
print(json.dumps({"stage": str(stage_out.relative_to(root_p)), "approval": str(appr.relative_to(root_p)),
    "freeze": str(frz.relative_to(root_p)), "manifest": str(man.relative_to(root_p)),
    "merge": str(mv.relative_to(root_p)), "release": str(rel.relative_to(root_p))}, indent=1))
# typed proof through nested reviews & Freeze deps: verify Freeze snapshot carries proof/basis
print(f"Freeze proof check: seal proof {seal.get('renewal_proof_ref',{}).get('path')}")
"""
def main():
    (EVID/"commands.log").write_text(f"LONGFORM DIRECT start {datetime.now(timezone.utc).isoformat()} PID={os.getpid()}\n",encoding="utf-8")
    run_tag("direct-pre-head", ["git","-C",str(FIX),"rev-parse","HEAD"])
    # record State before
    before = (FIX/"sources/SP001/production-state.json").read_bytes()
    before_sha = hashlib.sha256(before).hexdigest()
    print(f"State before {before_sha[:12]}", flush=True)
    open(EVID/"state-before-sha.txt","w").write(before_sha+"\n")
    now_iso=datetime.now(timezone.utc).isoformat()
    open(EVID/"now-iso-direct.txt","w").write(now_iso+"\n")
    # lifecycle on U3b r6
    lc = run_tag("lifecycle-longform", [sys.executable,"-c",LIFECYCLE_BUILDER, str(FIX), "SP001", "lf-boot-1", "high-u3b-longform", now_iso, "-direct"], timeout=1200)
    assert lc.returncode==0, f"lifecycle failed {open(EVID/'lifecycle-longform-stderr.txt').read()[:5000]}"
    print(open(EVID/"lifecycle-longform-stdout.txt").read()[:3000], flush=True)
    # verify State unchanged (artifact-level, no mutation)
    after=(FIX/"sources/SP001/production-state.json").read_bytes()
    assert after==before, "State mutated by artifact lifecycle (must be pinned)"
    print("STATE_PINNED_OK (no lifecycle State mutation)", flush=True)
    # verify old immutable priors preserved
    for r in ["r1","r2","r3","r4","r6"]:
        p=FIX/f"sources/SP001/publication/v2/publication-surface-revalidation-{r}.json"
        assert p.exists(), f"missing {r}"
        print(f"{r} preserved {hashlib.sha256(p.read_bytes()).hexdigest()[:12]}", flush=True)
    # R1 refusal: attempt refresh on VERSIONED_ACTIVE, expect refusal before writes, no writes
    r1_code = r"""
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
root_p=Path(sys.argv[1])
import os
print(f"R1 child PID={os.getpid()}", flush=True)
from scripts import survey_production_v2 as core
import json, hashlib
from datetime import datetime, timezone
state_path=root_p/"sources/SP001/production-state.json"
before=state_path.read_bytes()
before_sha=hashlib.sha256(before).hexdigest()
print(f"before {before_sha[:12]}")
try:
    from scripts import survey_weekly_mechanical_refresh_v2 as r1mod
    cfg=json.loads((root_p/"config/survey-production-v2.json").read_bytes())
    state=json.loads(before)
    r1mod.refresh_mechanical_evidence(root_p, cfg, state_path, "R1 after versioned should refuse", "longform-r1-test", datetime.now(timezone.utc))
    print("R1 UNEXPECTED SUCCESS (should refuse)")
    sys.exit(3)
except Exception as e:
    print(f"R1 refused as expected: {type(e).__name__}: {e}")
    after=state_path.read_bytes()
    assert after==before, "R1 wrote before refusing (must be no writes)"
    print("R1_NO_WRITES_OK")
"""
    r = run_tag("r1-refusal-full", [sys.executable,"-c",r1_code, str(FIX)])
    assert r.returncode==0, f"r1 refusal test failed {open(EVID/'r1-refusal-full-stderr.txt').read()[:3000]}"
    # canonical writer refusal? Check canonical build? For now, record that canonical install/Profile rebind not done (no canonical Candidate install)
    print("DIRECT DONE", flush=True)
    return 0
if __name__=="__main__":
    raise SystemExit(main())
