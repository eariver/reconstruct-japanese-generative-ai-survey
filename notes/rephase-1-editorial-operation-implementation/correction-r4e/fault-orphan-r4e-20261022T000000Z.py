#!/usr/bin/env python3
"""R4e orphan refusal -> explicit resume end-to-end (real public API, no mocks).

Usage: fault-orphan-r4e-20261022T000000Z.py INERT_ROOT ACTIVE_ROOT ISSUE ACTIVE_ID TAG
Temp copies live under $R4E_TMPDIR (default /dev/shm); never /tmp (quota).

Real fault scenario on temp copies only (originals untouched):
  1. cp -a INERT_ROOT -> T1 (State->r1, sealed set2, NO r2 record).
  2. Copy the r2 record file from ACTIVE_ROOT into T1 (complete orphan arrives;
     T1 State file is NEVER rewritten: no rewind).
  3. REAL ordinary activate_publication(T1, state, set2) must REFUSE pre-write
     (RECORD_COLLISION on existing r2 and/or INTENT_COLLISION on same intent;
     never a fork r3, never auto-adoption).
  4. REAL resume_activation(T1, state, r2 record) must fully revalidate and
     install -> RESUMED; State pointer becomes r2; selection VERSIONED_ACTIVE.
  5. Code binding checked: all scripts.* modules resolve under T1.

Saved BEFORE execution. No fixture mutation (writes land in temp T1 only).
Requires PYTHONDONTWRITEBYTECODE=1 + PYTHONPYCACHEPREFIX=/tmp/... BEFORE startup.
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
import pathlib

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER: PYTHONDONTWRITEBYTECODE!=1 (set BEFORE python startup)", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith("/tmp/"):
    print(f"BLOCKER: PYTHONPYCACHEPREFIX must be /tmp/... external, got {_pfx!r}", flush=True)
    sys.exit(2)


def _log(m: str) -> None:
    print(m, flush=True)


def main() -> int:
    if len(sys.argv) != 6:
        print(f"usage: {sys.argv[0]} INERT_ROOT ACTIVE_ROOT ISSUE ACTIVE_ID TAG", flush=True)
        return 2
    inert = pathlib.Path(sys.argv[1]).resolve()
    active = pathlib.Path(sys.argv[2]).resolve()
    issue, active_id, tag = sys.argv[3], sys.argv[4], sys.argv[5]
    for bad in [p for p in sys.path if "/tmp/opencode/jgas-" in p]:
        print(f"BLOCKER: fixture path pre-seeded on sys.path: {bad}", flush=True)
        return 2
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"r4e-orphan-{tag}-", dir=os.environ.get("R4E_TMPDIR", "/dev/shm")))
    t1 = tmp / "t1"
    _log(f"T1={t1}")
    cp = subprocess.run(["cp", "-a", str(inert), str(t1)], capture_output=True, text=True, timeout=300)
    if cp.returncode != 0:
        _log(f"BLOCKER inert cp failed {cp.stderr[:300]}")
        return 2
    rec_rel = f"sources/{issue}/publication/v2/publication-surface-revalidation-r2.json"
    if (t1 / rec_rel).exists():
        _log("BLOCKER inert copy already has r2 (not inert)")
        return 2
    src_rec = active / rec_rel
    if not src_rec.is_file():
        _log(f"BLOCKER active r2 record missing {src_rec}")
        return 2
    shutil.copyfile(src_rec, t1 / rec_rel)
    _log("ORPHAN_PLACED r2 record copied into T1 (State file untouched, no rewind)")
    st_before = json.loads((t1 / f"sources/{issue}/production-state.json").read_bytes())
    assert (st_before.get("publication_revalidation_provenance") or {}).get("path", "").endswith("-r1.json"), st_before.get("publication_revalidation_provenance")
    _log(f"T1_STATE pointer={(st_before.get('publication_revalidation_provenance') or {}).get('path')}")
    sys.path.insert(0, str(t1))
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    import scripts.survey_production_v2 as core
    import scripts.survey_publication_set_v2 as setmod
    import scripts.survey_editorial_publication_v2 as edpub
    import scripts.survey_agent_control_v2 as agent
    badmod = [(n, getattr(m, "__file__", None)) for n, m in sys.modules.items()
              if (n == "scripts" or n.startswith("scripts.")) and not str(getattr(m, "__file__", "")).startswith(str(t1))]
    badmod = [(n, f) for n, f in badmod if f is not None]
    if badmod:
        _log(f"BLOCKER code binding outside T1: {badmod}")
        return 2
    _log("BINDING_OK all scripts.* under T1")
    import scripts as _pkg
    if list(getattr(_pkg, "__path__", [])) != [str(t1 / "scripts")]:
        _log(f"BLOCKER scripts namespace not single-root: {list(getattr(_pkg, '__path__', []))}")
        return 2
    cfg = core.load_json(t1 / core.DEFAULT_CONFIG)
    state_rel = f"sources/{issue}/production-state.json"
    set_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-set.json"
    # 3. Ordinary activate must refuse (existing r2 / same intent).
    try:
        res = edpub.activate_publication(t1, state_rel, set_rel, f"R4c orphan probe {tag}",
                                         f"r4c-orphan-probe-{tag}")
        _log(f"ACTIVATE_UNEXPECTEDLY_SUCCEEDED (BLOCKER): {json.dumps(res)[:300]}")
        return 1
    except Exception as exc:
        msg = f"{type(exc).__name__}: {exc}"
        _log(f"ORDINARY_REFUSED_OK {msg[:300]}")
        if "COLLISION" not in msg and "INTENT_COLLISION" not in msg and "already exists" not in msg and "resume" not in msg.lower():
            _log(f"BLOCKER refusal seam wrong (expected RECORD/INTENT collision): {msg[:300]}")
            return 1
    cur = json.loads((t1 / state_rel).read_bytes())
    assert (cur.get("publication_revalidation_provenance") or {}).get("path", "").endswith("-r1.json"), "State must still point at r1 after refused activate"
    _log("STATE_STILL_R1_OK (no fork, no takeover)")
    # 4. Explicit resume of the exact orphan after full revalidation.
    try:
        rres = edpub.resume_activation(t1, state_rel, rec_rel)
    except Exception:
        _log("RESUME_FAILED (BLOCKER)")
        traceback.print_exc()
        return 1
    _log(f"RESUME_RESULT {json.dumps(rres)[:300]}")
    if rres.get("status") not in ("RESUMED", "ALREADY_ACTIVE"):
        _log(f"BLOCKER unexpected resume status {rres}")
        return 1
    fin = json.loads((t1 / state_rel).read_bytes())
    assert (fin.get("publication_revalidation_provenance") or {}).get("path") == rec_rel, fin.get("publication_revalidation_provenance")
    errs = agent.validate_agent_state(t1, cfg, fin)
    assert not errs, f"resumed State unhealthy {errs}"
    sel = setmod.resolve_publication_selection(t1, cfg, fin)
    assert sel.get("mode") == "VERSIONED_ACTIVE", sel.get("mode")
    _log(f"RESUMED_OK pointer=r2 mode={sel.get('mode')} candidate={(sel.get('candidate_ref') or {}).get('path')}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
