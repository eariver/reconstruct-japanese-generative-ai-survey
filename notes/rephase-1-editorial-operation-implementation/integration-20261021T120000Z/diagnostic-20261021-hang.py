#!/usr/bin/env python3
"""Bounded hang diagnostic for same-process repeat ALREADY_ACTIVE (DIAG copy of FIX23).

Runs ONLY post-activated repeat path (no entire chain/build rerun):
- before/after hash guards (State, r1 record, set) + git status (no writes expected)
- fresh-process equivalent is covered by separate subprocess launches (see shell wrapper);
  this script covers SAMEPROCESS multiple calls in one process, matching failing smoke sequence:
  validate_prepared_set → validate_editorial_receipt → validate_reader_surface_gate →
  validate_candidate → activate_publication(ALREADY_ACTIVE) ×2
- faulthandler.dump_traceback_later(30s, exit=False) + explicit per-call wallclock;
  parent bash timeout 120s stops child cleanly; INCOMPLETE recorded if no progress.
- instrumentation wrappers count calls and delegate to originals (explicit scope:
  survey_editorial_publication_v2.{validate_prepared_set,validate_editorial_receipt,
  activate_publication}, survey_reader_surface_gate_v2.validate_reader_surface_gate,
  survey_publication_v2.validate_candidate, survey_editorial_staged_source_v2.verify_staged_source);
  no behavior change, no validator-success stubs.
- checks actual schema/call branches and result-profile loops via counts (no guess).

Usage: SMOKE_FIX_ROOT=<diag-copy> PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/opencode/int-pycache TMPDIR=/tmp/opencode PYTHONPATH=<diag-copy> python3 diagnostic-20261021-hang.py
Outputs raw to stdout/stderr + returns 0 on complete, 2 on guarded failure, 124 on timeout (parent).
"""
from __future__ import annotations
import faulthandler
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# 30s stack dump if hung (does not exit, parent timeout 120s will stop).
faulthandler.enable()
try:
    faulthandler.dump_traceback_later(30, exit=False)
except Exception as e:
    print(f"faulthandler setup failed: {e}", flush=True)

ROOT = Path(os.environ.get("SMOKE_FIX_ROOT", "/tmp/opencode/jgas-editorial-diag-20261021T000000Z/candidate-partial-b40de60"))
sys.path.insert(0, str(ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from scripts import survey_production_v2 as core

STATE_REL = "sources/2026-W37/production-state.json"
SET_REL = "sources/2026-W37/publication/v2/editorial-corrections/wk-smoke-1/publication/publication-set.json"
RECEIPT_REL = "sources/2026-W37/publication/v2/editorial-corrections/wk-smoke-1/publication/validated-source-manifest.json"
GATE_REL = "sources/2026-W37/publication/v2/editorial-corrections/wk-smoke-1/publication/reader-surface-gate-v2.json"
MANUSCRIPT_REL = "sources/2026-W37/publication/v2/editorial-corrections/wk-smoke-1/publication/reader-manuscript-v2.json"
CAND_REL = "sources/2026-W37/publication/v2/editorial-corrections/wk-smoke-1/publication/publication-candidate-v2.json"
RECORD_REL = "sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json"

def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def _git_status(root: Path) -> tuple[int, str, str]:
    a = subprocess.run(["git", "status", "--short"], cwd=root, capture_output=True, text=True)
    b = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
    return (a.returncode, a.stdout, b.stdout.strip())

def main() -> int:
    t0 = time.monotonic()
    print(f"DIAG_START root={ROOT} pid={os.getpid()} fix_head={_git_status(ROOT)[2]}", flush=True)
    # Before guards (no writes expected for ALREADY_ACTIVE).
    before = {}
    for rel in (STATE_REL, RECORD_REL, SET_REL, RECEIPT_REL, GATE_REL, CAND_REL):
        p = ROOT / rel
        before[rel] = _sha(p) if p.is_file() else "MISSING"
    rc, status_before, head_before = _git_status(ROOT)
    print(f"BEFORE_HEAD {head_before} STATUS_RC={rc} STATUS_LINES={len(status_before.splitlines())}", flush=True)
    print(f"BEFORE_HASHES {json.dumps(before, sort_keys=True)}", flush=True)

    # Instrumentation: count calls, delegate original (explicit scope, no behavior change).
    import scripts.survey_editorial_publication_v2 as edpub
    import scripts.survey_reader_surface_gate_v2 as gate
    import scripts.survey_publication_v2 as pubmod
    import scripts.survey_editorial_staged_source_v2 as staged
    counts: dict[str, int] = {}
    def _wrap(mod, name: str):
        orig = getattr(mod, name)
        def _w(*a, **k):
            counts[name] = counts.get(name, 0) + 1
            print(f"CALL {mod.__name__}.{name} #{counts[name]} t={time.monotonic()-t0:.1f}s", flush=True)
            r = orig(*a, **k)
            print(f"RETURN {mod.__name__}.{name} #{counts[name]} t={time.monotonic()-t0:.1f}s", flush=True)
            return r
        setattr(mod, name, _w)
        return orig
    _orig_validate_set = _wrap(edpub, "validate_prepared_set")
    _orig_validate_receipt = _wrap(edpub, "validate_editorial_receipt")
    _orig_activate = _wrap(edpub, "activate_publication")
    _orig_gate = _wrap(gate, "validate_reader_surface_gate")
    _orig_cand = _wrap(pubmod, "validate_candidate")
    _orig_verify = _wrap(staged, "verify_staged_source")

    # SAMEPROCESS sequence matching smoke failing tail (post-CANDIDATE repeat).
    # Order in smoke: finalize already done, activate done, receipt/gate/candidate done, then repeat.
    # Here we repeat that tail twice to catch second-call hang vs first-call slow.
    for i in (1, 2):
        print(f"=== SAMEPROCESS_ROUND {i} t={time.monotonic()-t0:.1f}s ===", flush=True)
        # 1. validate_prepared_set (calls receipt→P3S→etc.)
        s = time.monotonic()
        vs = edpub.validate_prepared_set(str(ROOT), STATE_REL, SET_REL)
        print(f"VALIDATE_SET_OK round={i} dt={time.monotonic()-s:.1f}s set_sha={vs.get('set_sha256','?')[:12] if isinstance(vs, dict) else '?'}", flush=True)
        # 2. receipt directly
        s = time.monotonic()
        rv = edpub.validate_editorial_receipt(str(ROOT), RECEIPT_REL, STATE_REL)
        print(f"RECEIPT_OK round={i} dt={time.monotonic()-s:.1f}s issue={rv.get('issue_id')}", flush=True)
        # 3. gate directly (early-scope path, same as finalize)
        s = time.monotonic()
        gv = gate.validate_reader_surface_gate(str(ROOT), GATE_REL, issue_id="2026-W37", publication_profile="WEEKLY_MAGAZINE", expected_manuscript_path=MANUSCRIPT_REL, state_path=STATE_REL)
        print(f"GATE_OK round={i} dt={time.monotonic()-s:.1f}s status={gv.get('status')}", flush=True)
        # 4. candidate directly
        s = time.monotonic()
        cv = pubmod.validate_candidate(ROOT, ROOT / CAND_REL)
        print(f"CAND_OK round={i} dt={time.monotonic()-s:.1f}s status={cv.get('status') if isinstance(cv, dict) else cv}", flush=True)
        # 5. activate ALREADY_ACTIVE (read-only expected)
        s = time.monotonic()
        res = edpub.activate_publication(str(ROOT), STATE_REL, SET_REL, "Smoke weekly editorial correction", "smoke-executor", datetime.now(timezone.utc))
        print(f"ACTIVATE round={i} dt={time.monotonic()-s:.1f}s res={json.dumps(res)}", flush=True)
        if res.get("status") != "ALREADY_ACTIVE":
            print(f"UNEXPECTED_STATUS round={i} {res}", flush=True)
            return 2

    print(f"COUNTS {json.dumps(counts, sort_keys=True)}", flush=True)
    after = {}
    for rel in (STATE_REL, RECORD_REL, SET_REL, RECEIPT_REL, GATE_REL, CAND_REL):
        p = ROOT / rel
        after[rel] = _sha(p) if p.is_file() else "MISSING"
    rc2, status_after, head_after = _git_status(ROOT)
    print(f"AFTER_HEAD {head_after} STATUS_RC={rc2} STATUS_LINES={len(status_after.splitlines())}", flush=True)
    print(f"AFTER_HASHES {json.dumps(after, sort_keys=True)}", flush=True)
    print(f"HEAD_SAME={head_before==head_after} HASHES_SAME={before==after} STATUS_SAME={status_before==status_after}", flush=True)
    print(f"DIAG_COMPLETE t={time.monotonic()-t0:.1f}s", flush=True)
    try:
        faulthandler.cancel_dump_traceback_later()
    except Exception:
        pass
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
