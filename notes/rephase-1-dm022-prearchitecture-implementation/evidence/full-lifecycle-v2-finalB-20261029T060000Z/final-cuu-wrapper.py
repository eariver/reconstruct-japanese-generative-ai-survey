#!/usr/bin/env python3
"""Final CUU executor wrapper — outside candidate, evidence-only (no runtime patch, no accepted metadata rebind).

Runs existing two C→U→U→RELEASED tests as-is (no test code changes) with NEW private CURRENT source
freeze (768f, new B/A HIGH + C2/H/S + frozen 2 tests), pinning exact source before data, capturing
ACTUAL FINAL C outputs (PDF+TeX/bib/style/manuscript/reader/det/sem/vis/proof/receipt/buildRecord/full TeX logs
+ hashes + exact original target paths) BEFORE TempDirectory cleanup (which would otherwise delete them,
as in old f048 runs where only c_* stdout pages 5 remained, NO PDF bytes — truthful loss recorded in
c-pdf-retention-resolution.md). Uses existing retention helper pattern (copytree R dir + reviews dir,
excluding .git/__pycache__, no GitDB in packet), NOT silent rebuild, NOT copy editorial as C.

Records: exact wrapper script (this file) + source binding (pins before each run, runtime/scripts/env/PID),
full raw stdout/stderr/exits, manifest output roles (initial/editorial/C per route, U same-byte reuse NO duplicate),
unique UTC dirs, no old log reuse/no cleanup (of packet)/ordinary commit/Gitconfig/network/Human readback.

Usage (from NEW private exec root, e.g. .rephase-1-editorial-runtime/dm022-full-lifecycle-finalB-*/):
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /tmp/opencode/final-cuu-wrapper.py
"""
from __future__ import annotations
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# New private exec root (CWD) for tests import (no candidate edit, wrapper-only sys.path).
_REPO = Path.cwd().resolve()
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

# --- source binding (NEW private CURRENT source freeze, pinned before data) ---
# New private exec root is CWD when wrapper runs (must be NEW private freeze with new B/A HIGH).
REPO_ROOT = Path.cwd().resolve()
EVID_BASE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence")
PACKET_NEW = EVID_BASE / "full-lifecycle-v2-finalB-20261029T060000Z"
PACKET_NEW.mkdir(parents=True, exist_ok=True)
RUN_STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def _pins() -> dict:
    def _sha_rel(rel: str) -> str:
        return _sha_file(REPO_ROOT / rel)
    return {
        "frozen": str(REPO_ROOT),
        "HEAD": subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT), capture_output=True, text=True, check=True).stdout.strip(),
        "B2_agent": _sha_rel("scripts/survey_agent_control_v2.py")[:16],
        "B_human": _sha_rel("scripts/survey_human_gate_v2.py")[:16],
        "B_orch": _sha_rel("scripts/survey_orchestrator_v2.py")[:16],
        "B_bridge": _sha_rel("scripts/survey_core_execution_bridge_v2.py")[:16],
        "A_HIGH": _sha_rel("scripts/survey_prearchitecture_acceptance_v2.py")[:16],
        "LOW": _sha_rel("scripts/survey_research_authority_v2.py")[:16],
        "C2_release": _sha_rel("scripts/survey_release_checkpoint_v2.py")[:16],
        "C2_pub": _sha_rel("scripts/survey_publication_v2.py")[:16],
        "own_test": _sha_rel("tests/test_dm022_full_lifecycle_v2.py")[:16],
        "runtime": f"{sys.version.split()[0]}",
        "pid": os.getpid(),
        "run_stamp": RUN_STAMP,
    }

PINS = _pins()
(PACKET_NEW / f"pins-wrapper-{RUN_STAMP}.json").write_text(json.dumps(PINS, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"[wrapper] pins: {json.dumps(PINS, sort_keys=True)}", flush=True)

# --- Temp preservation (existing retention helper pattern, evidence-only) ---
# Patch TemporaryDirectory.cleanup to copy C-relevant outputs (R dir for C + reviews dir for C)
# to NEW unique packet retention BEFORE original cleanup deletes Temp (which caused old loss).
# Excludes .git/__pycache__ (no GitDB in packet). Records exact original target paths + hashes.
_ORIG_CLEANUP = tempfile.TemporaryDirectory.cleanup
_PRESERVED: list[Path] = []

def _copy_c_outputs(tmp_path: Path) -> Path | None:
    # Find C renewal dirs (RENDER_TARGETS, EXECUTED_BUILD) with new PDFs (final source, NOT old editorial).
    # C renewal IDs for chained tests: ren-weekly-cuu-c-v2 (WEEKLY) and ren-thematic-cuu-c-v2 (THEMATIC).
    # Also support ren-weekly-c-v2 / ren-thematic-c-v2 (C before Preview, for completeness).
    dest_base = PACKET_NEW / f"c-visual-{tmp_path.name}-{RUN_STAMP}"
    found = False
    for rdir in list(tmp_path.glob("**/renewals/ren-*-c-v2")):
        if not rdir.is_dir():
            continue
        # Check for C PDF (new build, REAL TinyTeX, NOT old editorial).
        pdfs = list(rdir.glob("**/main.pdf"))
        if not pdfs:
            continue
        dest_base.mkdir(parents=True, exist_ok=True)
        # Copy entire R dir (C trio/manuscript/proof/receipt/buildRecord/PDF/logs/QA/gate/candidate/set, exact original structure, no .git).
        _dst_r = dest_base / "renewal-c" / rdir.name
        _dst_r.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(rdir, _dst_r, symlinks=False, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        found = True
        # Copy reviews dir for C (exact new paths, NOT old editorial): .../publication/renewal-c*-v2/
        for rev in list((tmp_path / "sources").glob("**/publication/renewal-c*-v2")):
            if rev.is_dir():
                _dst_rev = dest_base / "renewal-c-reviews" / rev.name
                _dst_rev.parent.mkdir(parents=True, exist_ok=True)
                if not _dst_rev.exists():
                    shutil.copytree(rev, _dst_rev, symlinks=False, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        # Record exact original target paths + hashes (manifest, no GitDB).
        _manifest = {
            "tmp_name": tmp_path.name,
            "renewal_dir": str(rdir.relative_to(tmp_path)) if rdir.is_relative_to(tmp_path) else str(rdir),
            "pdfs": [],
            "trio": [],
        }
        for _pdf in pdfs:
            try:
                _rel = str(_pdf.relative_to(tmp_path))
            except ValueError:
                _rel = str(_pdf)
            _manifest["pdfs"].append({"path": _rel, "sha256": _sha_file(_pdf), "bytes": _pdf.stat().st_size})
        for _tri in ["main.tex", "references.bib", "jgaisurvey.sty"]:
            _tp = rdir / "staged-source" / _tri
            if _tp.is_file():
                try:
                    _rel2 = str(_tp.relative_to(tmp_path))
                except ValueError:
                    _rel2 = str(_tp)
                _manifest["trio"].append({"path": _rel2, "sha256": _sha_file(_tp), "bytes": _tp.stat().st_size})
        for _key in ["renewal-source-proof.json", "validated-source-manifest.json", "build-record.json", "reader-manuscript-v2.json"]:
            _fp = rdir / _key
            if _fp.is_file():
                _manifest[_key] = {"path": str(_fp.relative_to(tmp_path)) if _fp.is_relative_to(tmp_path) else str(_fp),
                                   "sha256": _sha_file(_fp), "bytes": _fp.stat().st_size}
        (_dst_r.parent / "exact-original-target-paths.json").write_text(json.dumps(_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if found:
        _PRESERVED.append(dest_base)
        print(f"[wrapper] preserved C outputs from {tmp_path} -> {dest_base}", flush=True)
        return dest_base
    return None

def _patched_cleanup(self: tempfile.TemporaryDirectory) -> None:
    try:
        _tmp_path = Path(self.name)
        if _tmp_path.is_dir():
            try:
                _copy_c_outputs(_tmp_path)
            except Exception as _e:
                print(f"[wrapper] preserve failed for {_tmp_path}: {_e}", flush=True)
    except Exception as _e2:
        print(f"[wrapper] preserve wrapper failed: {_e2}", flush=True)
    return _ORIG_CLEANUP(self)

tempfile.TemporaryDirectory.cleanup = _patched_cleanup  # type: ignore[method-assign]
print("[wrapper] TemporaryDirectory.cleanup patched for C retention (evidence-only, no runtime patch, no metadata rebind)", flush=True)

# --- run existing two CUU tests as-is (no test code changes) ---
import unittest
loader = unittest.TestLoader()
suite = unittest.TestSuite()
from tests import test_dm022_full_lifecycle_v2 as _mod
suite.addTest(_mod.Dm022FullLifecycleWitnessTests("test_weekly_renewal_c_u_u_release"))
suite.addTest(_mod.Dm022FullLifecycleWitnessTests("test_thematic_renewal_c_u_u_release"))
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
print(f"[wrapper] tests run={result.testsRun} failures={len(result.failures)} errors={len(result.errors)} skipped={len(result.skipped)}", flush=True)
(PACKET_NEW / f"wrapper-result-{RUN_STAMP}.json").write_text(json.dumps({
    "run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
    "wasSuccessful": result.wasSuccessful(), "pins": PINS,
    "preserved": [str(p) for p in _PRESERVED],
}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
sys.exit(0 if result.wasSuccessful() else 1)
