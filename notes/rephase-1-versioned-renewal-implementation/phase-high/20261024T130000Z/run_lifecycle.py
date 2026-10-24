#!/usr/bin/env python3
"""HIGH-phase lifecycle driver — normal direct stage/Preview/Freeze/Release on
U-activated sets (artifact level, NO State mutation).

Runs in the high22 fixtures (U1 ACTIVATED both routes). Per route: direct
stage.validate_stage at VALIDATED_DRAFT with U1-seal-role artifacts (proof
propagates via the threaded stage validators) -> synthetic Preview approval
(artifact only, clearly labelled; NO Human authority, NO lifecycle advance) ->
Freeze record + release manifest -> merge verification + release record, each
validated. State lifecycle is NEVER advanced here (that requires genuine Human
Preview authority); the boundary is explicit, not a silent skip.

Raw outputs/exits/commands/source-pins to the unique run dir (no overwrite).
"""
from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
EVID_BASE = REPO / "notes/rephase-1-versioned-renewal-implementation/phase-high/20261024T130000Z"
EVID = EVID_BASE / (sys.argv[1] if len(sys.argv) > 1 else "run33-20261025T033000Z")
# Absolute fixture roots REQUIRED (agent path resolution is not relative-safe;
# HIGH resolves internally but consumers join against the given root).
PARENT = (REPO / sys.argv[2]).resolve() if len(sys.argv) > 2 else (
    REPO / ".rephase-1-editorial-runtime/versioned-renewal-high22-20261025T030000Z")
FIX = {
    "weekly": {"root": str(PARENT / "renewal-weekly"), "issue": "2026-W37", "prop": "wk-boot-1",
               "rid": (sys.argv[3] if len(sys.argv) > 3 else "high-u1-weekly")},
    "longform": {"root": str(PARENT / "renewal-longform"), "issue": "SP001", "prop": "lf-boot-1",
                 "rid": (sys.argv[4] if len(sys.argv) > 4 else "high-u1-longform")},
}

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
role_paths = {k: root_p / roles[k]["path"] for k in (
    "reader-manuscript", "validated-source", "publication-pdf",
    "quality-regression-bundle", "semantic-review", "visual-review",
    "reader-surface-gate")}
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
"""


def run(cmd: list[str], tag: str, env: dict, timeout_s: int = 900) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                          timeout=timeout_s, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    with open(EVID / "commands.log", "a", encoding="utf-8") as fh:
        fh.write(f"$ {' '.join(cmd[:6])}...  # -> exit={proc.returncode}\n")
    return proc


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / "commands.log").write_text("", encoding="utf-8")
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(name):
            print(f"FATAL: inherited {name}", file=sys.stderr)
            return 1
    if not PARENT.is_dir():
        print("FATAL: parent fixtures missing", file=sys.stderr)
        return 1
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["LC_ALL"] = "C"
    py = sys.executable
    now_iso = datetime.now(timezone.utc).isoformat()
    for kind, fx in FIX.items():
        if len(sys.argv) > 6 and kind != sys.argv[6]:
            continue
        root, issue, prop, rid = fx["root"], fx["issue"], fx["prop"], fx["rid"]
        state_before = Path(root, f"sources/{issue}/production-state.json").read_bytes()
        sfx = sys.argv[5] if len(sys.argv) > 5 else ""
        lc = run([py, "-c", LIFECYCLE_BUILDER, root, issue, prop, rid, now_iso, sfx],
                 f"lifecycle-{kind}", env, timeout_s=2400)
        print(f"lifecycle-{kind}: exit={lc.returncode}", flush=True)
        if Path(root, f"sources/{issue}/production-state.json").read_bytes() != state_before:
            print(f"FATAL: {kind} State mutated by artifact-level lifecycle", file=sys.stderr)
            return 1
    print("STATE-PINNED (no lifecycle State mutation; Preview synthetic, no Human authority)")
    print("DONE LIFECYCLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
