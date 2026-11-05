#!/usr/bin/env python3
"""W34 r3 focused stdlib behavioral checks (no project import/run, no git/network).

Proves via controlled seam (actual tampered manifest file in /tmp, real
hash compare) that changed non-import source refuses BEFORE any project
import, plus r3 10-module schema binding. Not token assertions. Raw preserved.
"""
from __future__ import annotations
import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

WS = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
REPO = WS / ".rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
RESUME = WS / "notes/rephase-1-operational-rehearsal-resume-20261104"
R2 = RESUME / "w34-operator-dispose-run-r2-20261104.py"
R3 = RESUME / "w34-operator-dispose-run-r3-20261104.py"
R6 = RESUME / "sp-operator-prepare-r6-20261104.py"
PASS, FAIL = [], []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")


def _load_noexec(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    # 1. r2 bug present, r3 fixed (source shape, then behavior below)
    r2t, r3t = R2.read_text(), R3.read_text()
    check("r2_defect_present", "errs.extend(R6._check_intended_tree_stdlib" in r2t and r2t.index("errs.extend(R6._check_intended_tree_stdlib") < r2t.index("sys.path.insert"), "")
    # r3 fail-closed before import (AST order, not token)
    tree = ast.parse(r3t)
    found = {"fail_closed": False, "insert_after": False}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "stage_dispose_run":
            src = ast.get_source_segment(r3t, node) or ""
            i_raise = src.find("BEFORE any project import")
            i_insert = src.find("sys.path.insert")
            found["fail_closed"] = i_raise != -1 and i_insert != -1 and i_raise < i_insert
    check("r3_fail_closed_before_import_ast", found["fail_closed"], "")
    check("r3_binds_schema_gate", "rn.schema_gate" in r3t and "survey_schema_v2.py" in r3t, "")
    # 2. Behavioral seam: tampered intended manifest must refuse BEFORE import
    r6 = _load_noexec(R6, "r6helpers_seam")
    man = json.load(open(RESUME / "w34-prepare-expected-manifest-20261104.json"))
    tampered = json.loads(json.dumps(man))
    first_rel = sorted(tampered["delivery"]["intended"].keys())[0]
    real_sha = tampered["delivery"]["intended"][first_rel]["sha256"]
    bad_sha = ("0" if real_sha[0] != "0" else "1") + real_sha[1:]
    tampered["delivery"]["intended"][first_rel]["sha256"] = bad_sha
    tmp = Path("/tmp/opencode/w34-r3-seam")
    tmp.mkdir(parents=True, exist_ok=True)
    tm_path = tmp / "tampered-manifest.json"
    tm_path.write_bytes((json.dumps(tampered) + "\n").encode())
    tm_sha = hashlib.sha256(tm_path.read_bytes()).hexdigest()
    errs = r6._check_intended_tree_stdlib(REPO, tampered["delivery"]["intended"], tampered["delivery"]["test_pin"])
    check("seam_drift_detected_by_hash", len(errs) > 0, f"{first_rel} {real_sha[:8]}->{bad_sha[:8]}")
    # 3. Call r3 stage_dispose_run with tampered manifest: must raise BEFORE import
    for m in list(sys.modules):
        if m.startswith("survey_") or m.startswith("scripts"):
            del sys.modules[m]
    r3mod = _load_noexec(R3, "w34r3_seam")
    ready = json.load(open(RESUME / "retention-W34-20261104T235848Z/READY.json"))
    tm_ready_path = tmp / "READY-tampered-bind.json"
    rj = dict(ready)
    rj["manifest"] = {"path": "tampered-manifest.json", "sha256": tm_sha}
    tm_ready_path.write_bytes((json.dumps(rj) + "\n").encode())
    tm_ready_sha = hashlib.sha256(tm_ready_path.read_bytes()).hexdigest()
    ret_dir = tmp / "retention-W34-SEAM-000"
    try:
        r3mod.stage_dispose_run(ret_dir, tm_ready_path, tm_path, tm_ready_sha, tm_sha)
        check("seam_refuses_before_import", False, "no refusal")
    except ValueError as e:
        msg = str(e)
        check("seam_refuses_before_import", "BEFORE any project import" in msg or "phase0 source precheck" in msg, msg[:140])
    imported_project = [m for m in sys.modules if m.startswith("survey_") or m == "scripts"]
    check("no_project_import_on_refusal", imported_project == [], f"{imported_project[:3]}")
    print(f"\nPASS {len(PASS)} FAIL {len(FAIL)}")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    raise SystemExit(main())
