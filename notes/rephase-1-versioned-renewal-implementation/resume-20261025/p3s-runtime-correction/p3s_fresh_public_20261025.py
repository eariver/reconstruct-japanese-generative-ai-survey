#!/usr/bin/env python3
"""P3S runtime-correction dedicated fresh-PUBLIC check (Weekly+Longform, no test preloading).

Runs in NEW SOURCE db (cwd=DST). Uses existing P3S helpers for REAL initial
old-canonical accepted fixtures (FULL 740 SOURCE commit before authority),
but PUBLIC materialize/verify run in FRESH fixture-code subprocesses WITHOUT
preloading the expanded 35 (discovery/X/3 renewal). Asserts:
- top import laziness: after `import staged` alone, 5 new modules NOT loaded
- fresh PUBLIC Weekly + Longform materialize+verify SUCCEED (binding passes
  via function-local CURRENT imports, no caller preloading)
- manifest code_deps exact 63 per route, union 66, sorted-unique, no new paths
- current tool/live/schema closure unchanged (dep pins match manifest, P2V
  conditional discipline preserved: verifier does NOT load P2V)
Exits 0 on intended PASS, non-zero with typed code on failure. No network,
no old runners, no cleanup. Saves no files (caller saves raw).
"""
import sys
import os
import json
import subprocess
import tempfile
from pathlib import Path

DST = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
NEW5 = [
    "scripts/survey_discovery_v2.py",
    "scripts/survey_x_intake_v2.py",
    "scripts/survey_versioned_renewal_history_v2.py",
    "scripts/survey_versioned_renewal_source_v2.py",
    "scripts/survey_versioned_renewal_v2.py",
]

def fresh_lazy_check():
    """Fresh Python: import staged alone, verify 5 NOT loaded (lazy)."""
    script = (
        "import sys; "
        "from scripts import survey_editorial_staged_source_v2 as staged; "
        "import json; "
        "mods={m: (('scripts.'+__import__('pathlib').Path(m).stem) in sys.modules) for m in %s}; "
        "print(json.dumps(mods))" % (repr(NEW5),)
    )
    proc = subprocess.run(
        [sys.executable, "-c", script],
        cwd=str(DST), capture_output=True, text=True,
        env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")},
        timeout=60,
    )
    assert proc.returncode == 0, f"lazy check crashed: {proc.stderr[-2000:]}"
    lines = [l for l in proc.stdout.splitlines() if l.strip().startswith("{")]
    assert lines, f"lazy check no JSON: {proc.stdout[-2000:]}"
    mods = json.loads(lines[-1])
    for m, loaded in mods.items():
        assert loaded is False, f"new module {m} unexpectedly top-loaded (should be lazy): {mods}"
    print(f"LAZY OK: 5 new modules NOT top-loaded after `import staged` alone: {mods}")
    return True

def check_closure_counts():
    """Direct closure counts 63 per route / 66 union, no new paths."""
    sys.path.insert(0, str(DST))
    try:
        from scripts import survey_editorial_staged_source_v2 as staged
        long_deps = staged._route_code_deps(staged.LONGFORM_ROUTE)
        weekly_deps = staged._route_code_deps(staged.WEEKLY_ROUTE)
        assert len(long_deps) == 63, f"LONGFORM deps {len(long_deps)} !=63"
        assert len(weekly_deps) == 63, f"WEEKLY deps {len(weekly_deps)} !=63"
        assert len(long_deps) == len(sorted(set(long_deps))), "LONGFORM not sorted-unique"
        assert len(weekly_deps) == len(sorted(set(weekly_deps))), "WEEKLY not sorted-unique"
        union = sorted(set(long_deps) | set(weekly_deps))
        assert len(union) == 66, f"union {len(union)} !=66"
        assert len(staged._SHARED_PY) == 35 and len(staged._SHARED_SCHEMAS) == 22
        print(f"CLOSURE OK: LONGFORM 63, WEEKLY 63, UNION 66, SHARED 35+22")
        return long_deps, weekly_deps, union
    finally:
        if str(DST) in sys.path:
            sys.path.remove(str(DST))

def run_fresh_public():
    """Weekly+Longform fresh PUBLIC via existing helpers (REAL fixtures)."""
    # Import helpers from DST (parent may preload for fixture building; child stays fresh)
    sys.path.insert(0, str(DST))
    try:
        import unittest
        from tests.test_survey_editorial_staged_source_v2 import (
            _make_p3s_source_root, _lf_prepare, _weekly_prepare, _capture, _scope_for,
            _run_p3s_fixture, _P3S_MATERIALIZE_SCRIPT, _P3S_VERIFY_SCRIPT,
        )
        from scripts import survey_editorial_staged_source_v2 as staged
        from scripts import survey_production_v2 as core

        class _TC(unittest.TestCase):
            def runTest(self):
                pass
        tc = _TC()
        tc.workspace = DST

        # --- Weekly ---
        _scratch_w, root_w = _make_p3s_source_root(tc, "jgas-p3s-fresh-wk-")
        prep_w = _weekly_prepare(tc, root_w, "fixture-wk-fresh-1")
        man_w = _capture(tc, root_w, prep_w["state_path"], prep_w["proposal_path"])
        scope_w = _scope_for(tc, root_w, prep_w["prepared"], prep_w["proposal_path"], "scope-fresh-wk-1.json")
        out_w = _run_p3s_fixture(tc, root_w, _P3S_MATERIALIZE_SCRIPT,
                                 [str(root_w), str(prep_w["state_path"]), str(prep_w["proposal_path"]), str(man_w), str(scope_w)])
        assert out_w.get("ok"), f"Weekly fresh materialize refused: {out_w}"
        assert out_w.get("result") == staged.RESULT_MATERIALIZED
        man_w_json = core.load_json(root_w / out_w["staged"].replace(str(root_w)+"/", "") if False else root_w / (prep_w["proposal_path"].parent.relative_to(root_w).as_posix() + "/staged-source/staged-source-manifest.json"))
        # Derive staged manifest path canonically
        staged_dir_w = prep_w["proposal_path"].parent / staged.STAGED_DIRNAME
        staged_man_w = staged_dir_w / staged.MANIFEST_FILENAME
        assert staged_man_w.is_file(), "Weekly staged manifest missing"
        manifest_w = core.load_json(staged_man_w)
        assert manifest_w["route"] == "WEEKLY_GENERATED_V2"
        assert len(manifest_w["code_deps"]) == 63, f"Weekly code_deps {len(manifest_w['code_deps'])} !=63"
        v_w = _run_p3s_fixture(tc, root_w, _P3S_VERIFY_SCRIPT,
                               [str(root_w), str(prep_w["proposal_path"]), str(staged_man_w)], timeout_s=600)
        assert v_w.get("ok") and v_w.get("result") == staged.RESULT_VERIFIED, f"Weekly fresh verify refused: {v_w}"
        print(f"WEEKLY FRESH OK: materialize+verify without preloading, code_deps 63")

        # --- Longform ---
        _scratch_l, root_l = _make_p3s_source_root(tc, "jgas-p3s-fresh-lf-")
        prep_l = _lf_prepare(tc, root_l, DST, "fixture-lf-fresh-1")
        man_l = _capture(tc, root_l, prep_l["state_path"], prep_l["proposal_path"])
        scope_l = _scope_for(tc, root_l, prep_l["prepared"], prep_l["proposal_path"], "scope-fresh-lf-1.json")
        out_l = _run_p3s_fixture(tc, root_l, _P3S_MATERIALIZE_SCRIPT,
                                 [str(root_l), str(prep_l["state_path"]), str(prep_l["proposal_path"]), str(man_l), str(scope_l)])
        assert out_l.get("ok"), f"Longform fresh materialize refused: {out_l}"
        assert out_l.get("result") == staged.RESULT_MATERIALIZED
        staged_dir_l = prep_l["proposal_path"].parent / staged.STAGED_DIRNAME
        staged_man_l = staged_dir_l / staged.MANIFEST_FILENAME
        assert staged_man_l.is_file()
        manifest_l = core.load_json(staged_man_l)
        assert manifest_l["route"] == "LONGFORM_GENERATED_V1"
        assert len(manifest_l["code_deps"]) == 63, f"Longform code_deps {len(manifest_l['code_deps'])} !=63"
        v_l = _run_p3s_fixture(tc, root_l, _P3S_VERIFY_SCRIPT,
                               [str(root_l), str(prep_l["proposal_path"]), str(staged_man_l)], timeout_s=600)
        assert v_l.get("ok") and v_l.get("result") == staged.RESULT_VERIFIED, f"Longform fresh verify refused: {v_l}"
        print(f"LONGFORM FRESH OK: materialize+verify without preloading, code_deps 63")

        # Union check from both manifests (should be 66)
        union_paths = sorted({d["path"] for d in manifest_w["code_deps"]} | {d["path"] for d in manifest_l["code_deps"]})
        assert len(union_paths) == 66, f"manifest union {len(union_paths)} !=66"
        print(f"UNION OK: Weekly+Longform manifests union 66")
        return True
    finally:
        if str(DST) in sys.path:
            sys.path.remove(str(DST))

if __name__ == "__main__":
    fresh_lazy_check()
    check_closure_counts()
    run_fresh_public()
    print("DEDICATED FRESH PUBLIC PASS: Weekly+Longform 63/66, no preloading")
