#!/usr/bin/env python3
"""Freeze-transitive late-swap oracles — 7 categories must refuse with zero new Freeze/Manifest.
Uses U1c r3 Candidate + synthetic Preview approval (lifecycle-u1c-weekly) + new targets per category.
Real file swaps (not string tests), FD-safe, 1200s bound, PID logs, exact byte repair.
Preserves V1/V2/V3 + FULL Freeze success (not deleted).
"""
import os, sys, json, subprocess, time, hashlib
from datetime import datetime, timezone
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
FIX = REPO / ".rephase-1-editorial-runtime/versioned-renewal-freeze-transitive-20261025T120000Z/renewal-weekly"
STAMP = "20261025T124000Z"
EVID = REPO / f"notes/rephase-1-versioned-renewal-implementation/resume-20261025/freeze-transitive-correction/late-swap-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")
def log_cmd(cmd, tag, rc, dur=None):
    with open(LOG, "a") as fh:
        fh.write(f"$ {' '.join(cmd[:8])}... # {tag} -> exit={rc} dur={dur}\n")
def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["LC_ALL"] = "C"
        tmpdir = FIX.parent / "tmp-tex"
        tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = str(tmpdir); env["TMP"] = str(tmpdir); env["TEMP"] = str(tmpdir)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        if os.environ.get(k):
            raise RuntimeError(f"inherited {k}")
    print(f"START {tag} pid={os.getpid()} timeout={timeout}s", flush=True)
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        dur = time.time() - t0
        print(f"TIMEOUT {tag} after {dur:.1f}s", flush=True)
        (EVID/f"{tag}-timeout.txt").write_text(f"timeout after {dur:.1f}s\n")
        raise
    dur = time.time() - t0
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    (EVID/f"{tag}-dur.txt").write_text(f"{dur:.2f}\n", encoding="utf-8")
    log_cmd(cmd, tag, proc.returncode, f"{dur:.2f}s")
    print(f"DONE {tag} exit={proc.returncode} dur={dur:.2f}s", flush=True)
    return proc
PY = sys.executable
ISSUE = "2026-W37"; PROP = "wk-boot-1"; RID = "high-u1c-weekly"
now_iso = datetime.now(timezone.utc).isoformat()
print(f"LATE-SWAP STAMP {STAMP} FIX {FIX} HEAD {subprocess.run(['git','--no-optional-locks','rev-parse','HEAD'],cwd=str(FIX),capture_output=True,text=True).stdout.strip()}", flush=True)
(EVID/"now-iso.txt").write_text(now_iso)
# Candidate + approval from FULL Freeze success (lifecycle-u1c-weekly)
CAND = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/renewals/{RID}/publication-candidate-v2.json"
APPR = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/lifecycle-{RID}/preview-approval.json"
# 7 swap targets (repo-relative, all in snapshot per M1-M6 + retention/COPY/config/scope)
TARGETS = {
    "card": "sources/2026-W37/evidence/v2/runs/e29adeddd46abec907bd71303479d05dd152abaef54498e5481704c92ffd4940/results/task-12a1f44ab9a5d18cd288.json",
    "task": "sources/2026-W37/evidence/v2/runs/e29adeddd46abec907bd71303479d05dd152abaef54498e5481704c92ffd4940/tasks/task-12a1f44ab9a5d18cd288.json",
    "raw": "raw/source.json",
    "view": "views-accepted/098e838e49b37f2328e3ed91d7a1713e6a67b2c7e59241c10757c0ddcebeed58/views/view-12a1f44ab9a5d18cd288.json",
    "retentionCOPY": f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/renewals/{RID}/retained/before/sources/{ISSUE}/production-state.json",
    "config": "config/survey-production-v2.json",
    "scope": f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/manuscript-spec.json",
}
(EVID/"targets.json").write_text(json.dumps(TARGETS, indent=1))
LATE = r"""
import sys, json, os
sys.path.insert(0, sys.argv[1])
root, cand_rel, appr_rel, target_rel, swap_tag, out_dir = sys.argv[1:7]
from pathlib import Path
from datetime import datetime
root_p = Path(root)
from scripts import survey_publication_v2 as pubmod
# Prep (pins all M1-M6 + retention/COPY/config/scope)
prep = pubmod._prepare_freeze_inputs(root_p, root_p / cand_rel, root_p / appr_rel)
print(f"PREP_OK snapshot={len(prep['snapshot'])} authority={len(prep['renewal_authority'])}", flush=True)
# Save original bytes for exact repair
tpath = root_p / target_rel
orig = tpath.read_bytes()
print(f"ORIG_SHA {__import__('hashlib').sha256(orig).hexdigest()} bytes {len(orig)}", flush=True)
# Swap AFTER prep BEFORE install (flip last byte, preserve JSON? use different bytes)
swapped = orig[:-1] + (b"}" if orig[-1:] != b"}" else b"]") if len(orig) > 1 else b"X"
tpath.write_bytes(swapped)
print(f"SWAPPED {target_rel} -> swapped bytes {len(swapped)}", flush=True)
# Attempt preflight + install with new targets (must refuse, zero new files)
frz = root_p / out_dir / "freeze-record.json"
man = root_p / out_dir / "release-manifest.json"
# Ensure targets do not exist before (zero-new check baseline)
for p in (frz, man):
    if p.exists():
        print(f"PREEXIST {p} (unexpected, removing for clean test)", flush=True)
        p.unlink()
from scripts import survey_production_v2 as core
cand = prep["candidate"]
# Build freeze payload like build_freeze (pure, no writes)
freeze_payload = pubmod._build_freeze_payload(repo_root=root_p, candidate_path=root_p / cand_rel, candidate=cand, approval_path=root_p / appr_rel, approval=prep["approval"], visual_path=prep["visual_path"], frozen_at=datetime.fromisoformat(sys.argv[7]))
# Preflight must refuse due to swapped snapshot file (recheck before install)
try:
    plan = pubmod._preflight_freeze_pair(root_p, frz, man, prep, freeze_payload, lambda fs, ft: pubmod._build_manifest_payload(repo_root=root_p, freeze_path=ft, freeze_record_sha256=fs, release_identity=pubmod.profile_release_identity(prep["profile"]), source_path=cand["source"]["path"], source_sha256=cand["source"]["sha256"], pdf_path=cand["pdf"]["path"], pdf_sha256=cand["pdf"]["sha256"], page_count=cand["pdf"]["page_count"], issue_id=cand["issue_id"]))
    # If preflight passed (unexpected), try install (should also refuse via recheck)
    try:
        pubmod._install_freeze_pair(root_p, plan)
        print(f"UNEXPECTED_SUCCESS {swap_tag} (should have refused)", flush=True)
        sys.exit(10)
    except ValueError as e:
        print(f"REFUSED_INSTALL {swap_tag}: {e}", flush=True)
        # Verify zero new files
        import os as _os
        frz_exists = frz.exists()
        man_exists = man.exists()
        print(f"ZERO_NEW frz_exists={frz_exists} man_exists={man_exists}", flush=True)
        if frz_exists or man_exists:
            print(f"FAIL_ZERO_NEW {swap_tag} new files created despite refuse", flush=True)
            sys.exit(11)
        print(f"PASS_REFUSE {swap_tag}", flush=True)
        sys.exit(0)
except ValueError as e:
    print(f"REFUSED_PREFLIGHT {swap_tag}: {e}", flush=True)
    frz_exists = frz.exists()
    man_exists = man.exists()
    print(f"ZERO_NEW frz_exists={frz_exists} man_exists={man_exists}", flush=True)
    if frz_exists or man_exists:
        print(f"FAIL_ZERO_NEW {swap_tag}", flush=True)
        sys.exit(11)
    print(f"PASS_REFUSE {swap_tag}", flush=True)
    sys.exit(0)
finally:
    # Exact byte repair (always restore, even on failure, for healthy control)
    tpath.write_bytes(orig)
    print(f"RESTORED {target_rel} orig SHA {__import__('hashlib').sha256(orig).hexdigest()}", flush=True)
"""
for tag, rel in TARGETS.items():
    out = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROP}/lifecycle-{RID}/late-swap-{tag}"
    # Ensure out dir clean (no preexisting freeze/manifest from prior runs? Remove if exists from prior failed? Preserve? For clean test, ensure not exists before prep)
    # Use fresh subprocess per category (1200s bound)
    p = run([PY,"-c",LATE, str(FIX), CAND, APPR, rel, tag, out, now_iso], REPO, f"late-swap-{tag}")
    if p.returncode != 0:
        print(f"FATAL late-swap {tag} failed (expected PASS_REFUSE exit 0, got {p.returncode})", flush=True)
        sys.exit(1)
    # Healthy control: after restore, preflight must pass (no writes) — do via separate call (no swap)
    HEALTHY = r"""
import sys, json
sys.path.insert(0, sys.argv[1])
root, cand_rel, appr_rel, out_dir = sys.argv[1:5]
from pathlib import Path
from datetime import datetime
root_p = Path(root)
from scripts import survey_publication_v2 as pubmod
prep = pubmod._prepare_freeze_inputs(root_p, root_p / cand_rel, root_p / appr_rel)
print(f"HEALTHY_PREP_OK snapshot={len(prep['snapshot'])}", flush=True)
frz = root_p / out_dir / "freeze-record.json"
man = root_p / out_dir / "release-manifest.json"
# Healthy preflight with restored bytes must pass (no writes here, just preflight)
cand = prep["candidate"]
freeze_payload = pubmod._build_freeze_payload(repo_root=root_p, candidate_path=root_p / cand_rel, candidate=cand, approval_path=root_p / appr_rel, approval=prep["approval"], visual_path=prep["visual_path"], frozen_at=datetime.fromisoformat(sys.argv[5]))
plan = pubmod._preflight_freeze_pair(root_p, frz, man, prep, freeze_payload, lambda fs, ft: pubmod._build_manifest_payload(repo_root=root_p, freeze_path=ft, freeze_record_sha256=fs, release_identity=pubmod.profile_release_identity(prep["profile"]), source_path=cand["source"]["path"], source_sha256=cand["source"]["sha256"], pdf_path=cand["pdf"]["path"], pdf_sha256=cand["pdf"]["sha256"], page_count=cand["pdf"]["page_count"], issue_id=cand["issue_id"]))
print(f"HEALTHY_PREFLIGHT_OK frz={frz} man={man}", flush=True)
"""
    h = run([PY,"-c",HEALTHY, str(FIX), CAND, APPR, out, now_iso], REPO, f"healthy-{tag}")
    if h.returncode != 0:
        print(f"FATAL healthy control {tag} failed", flush=True)
        sys.exit(1)
print("ALL LATE-SWAP REFUSE + HEALTHY PASS", flush=True)
