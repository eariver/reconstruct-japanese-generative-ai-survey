#!/usr/bin/env python3
"""Bounded hang/slow diagnostic v2 — stack paths/counts, no behavior change.

Same scope as v1, plus per-verify caller stacks (file:line:function) via traceback.extract_stack()
in wrapper (explicit instrumentation scope, delegate original). No validator-success stubs.
Runs SAMEPROCESS rounds only (fresh covered separately); before/after hash guards.
faulthandler.dump_traceback_later(30) retained; plus periodic Python-stack sampler
(threading.Timer every 5s dumping main-thread stack to stderr) to capture expensive/
infinite loops with actual paths/counts (not guesses).
"""
from __future__ import annotations
import faulthandler
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

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

def _git_status(root: Path):
    a = subprocess.run(["git", "status", "--short"], cwd=root, capture_output=True, text=True)
    b = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
    return (a.returncode, a.stdout, b.stdout.strip())

_stop_sampler = False
def _sampler():
    import threading as _th
    main_tid = _th.main_thread().ident
    while not _stop_sampler:
        time.sleep(5)
        frames = sys._current_frames()
        f = frames.get(main_tid)
        if f is not None:
            stack = traceback.extract_stack(f)
            # Last 8 frames with file:line:function (actual paths, not guesses).
            tail = stack[-8:]
            print("SAMPLER_STACK " + " | ".join(f"{Path(x.filename).name}:{x.lineno}:{x.name}" for x in tail), flush=True)

def main() -> int:
    global _stop_sampler
    t0 = time.monotonic()
    print(f"DIAG_V2_START root={ROOT} pid={os.getpid()}", flush=True)
    before = {rel: (_sha(ROOT / rel) if (ROOT / rel).is_file() else "MISSING") for rel in (STATE_REL, RECORD_REL, SET_REL, RECEIPT_REL, GATE_REL, CAND_REL)}
    rc, status_before, head_before = _git_status(ROOT)
    print(f"BEFORE_HEAD {head_before} STATUS_LINES={len(status_before.splitlines())}", flush=True)
    print(f"BEFORE_HASHES {json.dumps(before, sort_keys=True)}", flush=True)

    import scripts.survey_editorial_publication_v2 as edpub
    import scripts.survey_reader_surface_gate_v2 as gate
    import scripts.survey_publication_v2 as pubmod
    import scripts.survey_editorial_staged_source_v2 as staged
    counts: dict[str, int] = {}
    stacks: dict[str, dict[str, int]] = {}
    def _wrap(mod, name: str):
        orig = getattr(mod, name)
        def _w(*a, **k):
            counts[name] = counts.get(name, 0) + 1
            # Actual caller stack (file:line:function), top 6 excluding wrapper.
            st = traceback.extract_stack()[:-2][-6:]
            key = " <- ".join(f"{Path(x.filename).name}:{x.lineno}:{x.name}" for x in st)
            d = stacks.setdefault(name, {})
            d[key] = d.get(key, 0) + 1
            print(f"CALL {mod.__name__}.{name} #{counts[name]} t={time.monotonic()-t0:.1f}s", flush=True)
            r = orig(*a, **k)
            print(f"RETURN {mod.__name__}.{name} #{counts[name]} t={time.monotonic()-t0:.1f}s", flush=True)
            return r
        setattr(mod, name, _w)
        return orig
    _wrap(edpub, "validate_prepared_set")
    _wrap(edpub, "validate_editorial_receipt")
    _wrap(edpub, "activate_publication")
    _wrap(gate, "validate_reader_surface_gate")
    _wrap(pubmod, "validate_candidate")
    _wrap(staged, "verify_staged_source")

    th = threading.Thread(target=_sampler, daemon=True)
    th.start()
    try:
        for i in (1, 2):
            print(f"=== SAMEPROCESS_ROUND {i} t={time.monotonic()-t0:.1f}s ===", flush=True)
            s = time.monotonic()
            vs = edpub.validate_prepared_set(str(ROOT), STATE_REL, SET_REL)
            print(f"VALIDATE_SET_OK round={i} dt={time.monotonic()-s:.1f}s", flush=True)
            s = time.monotonic()
            rv = edpub.validate_editorial_receipt(str(ROOT), RECEIPT_REL, STATE_REL)
            print(f"RECEIPT_OK round={i} dt={time.monotonic()-s:.1f}s", flush=True)
            s = time.monotonic()
            gv = gate.validate_reader_surface_gate(ROOT, ROOT / GATE_REL, issue_id="2026-W37", publication_profile="WEEKLY_MAGAZINE", expected_manuscript_path=ROOT / MANUSCRIPT_REL, state_path=ROOT / STATE_REL)
            print(f"GATE_OK round={i} dt={time.monotonic()-s:.1f}s status={gv.get('status')}", flush=True)
            s = time.monotonic()
            cv = pubmod.validate_candidate(ROOT, ROOT / CAND_REL)
            print(f"CAND_OK round={i} dt={time.monotonic()-s:.1f}s", flush=True)
            s = time.monotonic()
            res = edpub.activate_publication(str(ROOT), STATE_REL, SET_REL, "Smoke weekly editorial correction", "smoke-executor", datetime.now(timezone.utc))
            print(f"ACTIVATE round={i} dt={time.monotonic()-s:.1f}s res={json.dumps(res)}", flush=True)
            if res.get("status") != "ALREADY_ACTIVE":
                print(f"UNEXPECTED_STATUS round={i} {res}", flush=True)
                return 2
    finally:
        _stop_sampler = True
    print(f"COUNTS {json.dumps(counts, sort_keys=True)}", flush=True)
    # Stack paths/counts (actual, not guesses). Truncate to top 5 per function for readability.
    for fn, d in sorted(stacks.items()):
        top = sorted(d.items(), key=lambda kv: -kv[1])[:5]
        print(f"STACKS {fn} " + json.dumps(top)[:2000], flush=True)
    after = {rel: (_sha(ROOT / rel) if (ROOT / rel).is_file() else "MISSING") for rel in (STATE_REL, RECORD_REL, SET_REL, RECEIPT_REL, GATE_REL, CAND_REL)}
    rc2, status_after, head_after = _git_status(ROOT)
    print(f"AFTER_HEAD {head_after} STATUS_LINES={len(status_after.splitlines())}", flush=True)
    print(f"HASHES_SAME={before==after} HEAD_SAME={head_before==head_after} STATUS_SAME={status_before==status_after}", flush=True)
    print(f"DIAG_V2_COMPLETE t={time.monotonic()-t0:.1f}s", flush=True)
    try:
        faulthandler.cancel_dump_traceback_later()
    except Exception:
        pass
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        import traceback as _tb
        _tb.print_exc()
        sys.exit(2)
