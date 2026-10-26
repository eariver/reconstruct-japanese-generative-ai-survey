#!/usr/bin/env python3
"""P3S runtime-correction dedicated negatives (wrongroot + modulebytes dirty with repair).

Runs in NEW SOURCE db (cwd=DST). All PUBLIC calls in FRESH fixture-code
subprocesses (no test preloading). Uses REAL initial fixtures for dirty
control (verifier TOOL_DRIFT with repair) and direct binding for wrongroot.

- WRONGROOT: preload discovery from OTHER repo (old affected-regress TESTSRC
  at 143000Z, same bytes but different root) in fresh child, then call
  PUBLIC materialize. Must refuse RUNTIME_BINDING_PATH (not PASS), must NOT
  auto-reload/rebind (sys.modules still points to other repo after refusal).
  Fresh child without preload must then PASS (repair = fresh process).
- DIRTY: healthy staged set, tamper discovery (one of New5) on disk, verifier
  must refuse TOOL_DRIFT PIN/INVALID with no-write, then restore and verify
  PASS again (repair). Targets New5 to prove expanded-35 pins are strict.
Exits 0 on intended PASS. No network, no old runners, no cleanup.
"""
import sys
import os
import json
import subprocess
from pathlib import Path

DST = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
OTHER = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-affected-regress-20261025T143000Z/test-source")

def run_child(root, script, args, timeout_s=600):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1"})
    # Workspace TMPDIR/P3S_DURABLE_OUTDIR are inherited from parent env (already workspace-local)
    proc = subprocess.run([sys.executable, "-c", script, *args], cwd=str(root),
                          capture_output=True, text=True, env=env, timeout=timeout_s)
    assert proc.returncode == 0, f"child crashed rc={proc.returncode} STDOUT:{proc.stdout[-2000:]} STDERR:{proc.stderr[-2000:]}"
    lines = [l for l in proc.stdout.splitlines() if l.strip().startswith("{")]
    assert lines, f"child no JSON: {proc.stdout[-2000:]}"
    return json.loads(lines[-1])

def wrongroot_check():
    sys.path.insert(0, str(DST))
    try:
        import unittest
        from tests.test_survey_editorial_staged_source_v2 import (
            _make_p3s_source_root, _weekly_prepare, _capture, _scope_for, _run_p3s_fixture,
            _P3S_MATERIALIZE_SCRIPT,
        )
        from scripts import survey_editorial_staged_source_v2 as staged

        class _TC(unittest.TestCase):
            def runTest(self):
                pass
        tc = _TC()
        tc.workspace = DST
        _scratch, root = _make_p3s_source_root(tc, "jgas-p3s-wrongroot-")
        prep = _weekly_prepare(tc, root, "fixture-wk-wrongroot-1")
        man = _capture(tc, root, prep["state_path"], prep["proposal_path"])
        scope = _scope_for(tc, root, prep["prepared"], prep["proposal_path"], "scope-wrongroot-1.json")

        # Fresh child that preloads discovery from OTHER repo, then calls PUBLIC materialize.
        # Must refuse, must NOT auto-reload (still points to OTHER after).
        script = (
            "import sys\n"
            "sys.path.insert(0, %r)\n"
            "import scripts.survey_discovery_v2 as _foreign\n"
            "_fpath=_foreign.__file__\n"
            "from pathlib import Path\n"
            "import json\n"
            "root=Path(sys.argv[1])\n"
            "sp=Path(sys.argv[2])\n"
            "pp=Path(sys.argv[3])\n"
            "mp=Path(sys.argv[4])\n"
            "scp=Path(sys.argv[5])\n"
            "from scripts import survey_editorial_staged_source_v2 as staged\n"
            "import sys as _sys\n"
            "try:\n"
            "    out=staged.materialize_staged_source(root, sp, pp, mp, scp)\n"
            "    print(json.dumps({'ok': True, 'result': out['result']}))\n"
            "except Exception as exc:\n"
            "    code=getattr(exc,'code',type(exc).__name__)\n"
            "    phase=getattr(exc,'phase','')\n"
            "    disp=getattr(exc,'disposition','')\n"
            "    cur=_sys.modules.get('scripts.survey_discovery_v2')\n"
            "    curfile=getattr(cur,'__file__','?') if cur else '?'\n"
            "    print(json.dumps({'ok': False, 'code': code, 'phase': phase, 'disposition': disp, 'error': str(exc)[:2000], 'foreign_file': _fpath, 'cur_file': curfile}))\n"
        ) % (str(OTHER),)
        out = run_child(root, script, [str(root), str(prep["state_path"]), str(prep["proposal_path"]), str(man), str(scope)], timeout_s=1800)
        assert out.get("ok") is False, f"wrongroot must refuse, got PASS: {out}"
        assert out.get("code") == "RUNTIME_BINDING_PATH", f"wrongroot must be RUNTIME_BINDING_PATH, got {out}"
        # Must NOT have rebound to fixture root (still foreign)
        assert "affected-regress-20261025T143000Z" in str(out.get("cur_file", "")), f"wrongroot auto-reloaded/rebound (must preserve foreign): {out}"
        print(f"WRONGROOT OK: refused {out.get('code')} [{out.get('phase')}/{out.get('disposition')}], no auto-reload (still {out.get('cur_file')})")

        # Repair = fresh child without preload must PASS (same fixture, staged root absent? materialize refused pre-write, so no staged dir)
        # Use standard fresh materialize (no preload) - should succeed now
        out2 = _run_p3s_fixture(tc, root, _P3S_MATERIALIZE_SCRIPT,
                                [str(root), str(prep["state_path"]), str(prep["proposal_path"]), str(man), str(scope)])
        assert out2.get("ok") and out2.get("result") == staged.RESULT_MATERIALIZED, f"wrongroot repair (fresh) must PASS: {out2}"
        print(f"WRONGROOT REPAIR OK: fresh without preload PASS")
        return True
    finally:
        if str(DST) in sys.path:
            sys.path.remove(str(DST))

def dirty_check():
    sys.path.insert(0, str(DST))
    try:
        import unittest
        from tests.test_survey_editorial_staged_source_v2 import (
            _make_p3s_source_root, _lf_prepare, _capture, _scope_for, _run_p3s_fixture,
            _P3S_MATERIALIZE_SCRIPT, _P3S_VERIFY_SCRIPT, _snapshot, _assert_no_write,
        )
        from scripts import survey_editorial_staged_source_v2 as staged
        from scripts import survey_production_v2 as core

        class _TC(unittest.TestCase):
            def runTest(self):
                pass
        tc = _TC()
        tc.workspace = DST
        _scratch, root = _make_p3s_source_root(tc, "jgas-p3s-dirty-")
        prep = _lf_prepare(tc, root, DST, "fixture-lf-dirty-1")
        man = _capture(tc, root, prep["state_path"], prep["proposal_path"])
        scope = _scope_for(tc, root, prep["prepared"], prep["proposal_path"], "scope-dirty-1.json")
        # Healthy materialize+verify first (fresh, no preload)
        out = _run_p3s_fixture(tc, root, _P3S_MATERIALIZE_SCRIPT,
                               [str(root), str(prep["state_path"]), str(prep["proposal_path"]), str(man), str(scope)])
        assert out.get("ok"), f"dirty setup materialize refused: {out}"
        staged_dir = prep["proposal_path"].parent / staged.STAGED_DIRNAME
        staged_man = staged_dir / staged.MANIFEST_FILENAME
        assert staged_man.is_file()
        v0 = _run_p3s_fixture(tc, root, _P3S_VERIFY_SCRIPT,
                              [str(root), str(prep["proposal_path"]), str(staged_man)], timeout_s=600)
        assert v0.get("ok"), f"dirty setup verify refused: {v0}"
        # Tamper one of New5 (discovery) - must be pinned, must refuse TOOL_DRIFT
        target = root / "scripts" / "survey_discovery_v2.py"
        snap = _snapshot(root)
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n# Fixture P3S-New5 TOOL_DRIFT probe (discovery).\n", encoding="utf-8")
        try:
            snap_fault = _snapshot(root)
            out2 = _run_p3s_fixture(tc, root, _P3S_VERIFY_SCRIPT,
                                    [str(root), str(prep["proposal_path"]), str(staged_man)], timeout_s=600)
            assert out2.get("ok") is False, f"dirty must refuse, got PASS: {out2}"
            assert out2.get("code") == "TOOL_DRIFT", f"dirty must be TOOL_DRIFT, got {out2}"
            assert out2.get("phase") == "PIN" and out2.get("disposition") == "INVALID"
            _assert_no_write(tc, snap_fault, _snapshot(root), "dirty no-write")
            print(f"DIRTY OK: discovery tamper refused {out2.get('code')} [{out2.get('phase')}/{out2.get('disposition')}]")
        finally:
            target.write_text(text, encoding="utf-8")
        _assert_no_write(tc, snap, _snapshot(root), "dirty restored")
        v1 = _run_p3s_fixture(tc, root, _P3S_VERIFY_SCRIPT,
                              [str(root), str(prep["proposal_path"]), str(staged_man)], timeout_s=600)
        assert v1.get("ok"), f"dirty repair verify must PASS: {v1}"
        print(f"DIRTY REPAIR OK: restored verifies again")
        return True
    finally:
        if str(DST) in sys.path:
            sys.path.remove(str(DST))

if __name__ == "__main__":
    wrongroot_check()
    dirty_check()
    print("DEDICATED NEGATIVES PASS: wrongroot RUNTIME_BINDING_PATH no-rebind + discovery TOOL_DRIFT with repair")
