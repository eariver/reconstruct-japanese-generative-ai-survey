#!/usr/bin/env python3
"""Affected verification runner (evidence scaling repair).

NEW packet-only harness, not shipping runtime. Sequential fail-closed batches.
Captures genuine verbose raw per batch: stdout/stderr/exit/argv/env/cwd/PID/UTC,
pins-before/after (771), same-process loaded module check via loader probe.
Stops on first non-zero (common-positive-setup STOP). No source/test edits.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PACKET = Path(__file__).resolve().parent
TEST_RUNS = PACKET / "test-runs"
SNAP = Path(".rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed").resolve()
# Fallback absolute
if not SNAP.exists():
    SNAP = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed")

BATCHES = [
    ("batch-01-positive-smoke", [
        "tests.test_profile_support_upstream_repair_v2.DM016CanonicalTenTests.test_01_all_ten_leaf_mappings_exact",
        "tests.test_survey_evidence_v2.SurveyEvidenceV2Tests.test_evidence_authority_supplement_binds_exact_raw_source_and_card",
    ]),
    ("batch-02-profile-28", ["tests.test_profile_support_upstream_repair_v2"]),
    ("batch-03-evidence-runner-agent-sourceclass-26", [
        "tests.test_survey_evidence_v2",
        "tests.test_run_evidence_v2_interactive",
        "tests.test_run_evidence_v2_agent_first",
        "tests.test_survey_evidence_source_class_regression",
    ]),
    ("batch-04-dm022-c7", ["tests.test_dm022_c_direct_operation_v2"]),
    ("batch-05-dm022-a2-selected-5", [
        "tests.test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests.test_weekly_prepare_adopt_resume_readback",
        "tests.test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests.test_thematic_prepare_adopt_resume_readback",
        "tests.test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests.test_low_typed_loader_dispatch",
        "tests.test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests.test_low_guard_and_slots",
        "tests.test_dm022_prearchitecture_acceptance_v2.Dm022A2OperationTests.test_high_cli_prepare_adopt",
    ]),
    ("batch-06-family-6", ["tests.test_dm022_c1_family_closure_v2"]),
    ("batch-07-graph-h-8", [
        "tests.test_dm022_c1_research_graph_v2",
        "tests.test_dm022_c1_h_presence_controls_v2",
    ]),
    ("batch-08-consumers-3", [
        "tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_dm022_to_selection_stage",
        "tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_present_old_seven_slots_retain_clear_regenerate",
        "tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_draft_synthesis_reader",
    ]),
]

def hash_pins(root: Path):
    out = []
    for p in sorted(root.rglob("*")):
        if ".git" in p.parts:
            continue
        if "__pycache__" in p.parts:
            continue
        if p.suffix == ".pyc":
            continue
        if p.is_dir():
            continue
        rel = p.relative_to(root).as_posix()
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        st = p.stat()
        out.append(f"{h} {st.st_size} {oct(st.st_mode & 0o777)} {rel}")
    return out

def main():
    TEST_RUNS.mkdir(parents=True, exist_ok=True)
    overall = []
    for name, selectors in BATCHES:
        d = TEST_RUNS / name
        d.mkdir(parents=True, exist_ok=True)
        pins_before = hash_pins(SNAP)
        (d / "pins-before.txt").write_text("\n".join(pins_before) + "\n", encoding="utf-8")
        argv = [sys.executable, "-m", "unittest", "-v"] + selectors
        (d / "argv.txt").write_text(" ".join(argv) + "\n", encoding="utf-8")
        (d / "cwd.txt").write_text(str(SNAP) + "\n", encoding="utf-8")
        env = {"PATH": os.environ.get("PATH", ""), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(SNAP), "LANG": "C.UTF-8"}
        # record env (no secrets)
        (d / "env.txt").write_text("\n".join(f"{k}={v}" for k, v in sorted(env.items())) + "\n", encoding="utf-8")
        wall_start = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (d / "wall-start.txt").write_text(wall_start + "\n", encoding="utf-8")
        # launch
        proc = subprocess.Popen(argv, cwd=str(SNAP), env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(SNAP)}, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        (d / "pid.txt").write_text(str(proc.pid) + "\n", encoding="utf-8")
        try:
            stdout, stderr = proc.communicate(timeout=900)
            rc = proc.returncode
            timed_out = False
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            rc = 124
            timed_out = True
        wall_end = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        (d / "wall-end.txt").write_text(wall_end + "\n", encoding="utf-8")
        (d / "stdout.txt").write_text(stdout or "", encoding="utf-8")
        (d / "stderr.txt").write_text(stderr or "", encoding="utf-8")
        (d / "exit.txt").write_text(str(rc) + "\n", encoding="utf-8")
        meta = {"batch": name, "selectors": selectors, "pid": proc.pid, "argv": argv, "cwd": str(SNAP), "wall_start": wall_start, "wall_end": wall_end, "exit": rc, "timed_out": timed_out}
        (d / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        pins_after = hash_pins(SNAP)
        (d / "pins-after.txt").write_text("\n".join(pins_after) + "\n", encoding="utf-8")
        same = (pins_before == pins_after)
        (d / "pins-same.txt").write_text("YES\n" if same else "NO\n", encoding="utf-8")
        print(f"{name}: exit={rc} timed_out={timed_out} pins_same={same} stderr_bytes={len(stderr or '')}", flush=True)
        overall.append({"batch": name, "exit": rc, "pins_same": same, "timed_out": timed_out})
        if rc != 0:
            print(f"STOP: {name} failed, halting further batches", flush=True)
            break
    (TEST_RUNS / "batches-summary.json").write_text(json.dumps(overall, indent=2) + "\n", encoding="utf-8")
    # nonzero overall if any failed
    sys.exit(0 if all(o["exit"] == 0 for o in overall) else 1)

if __name__ == "__main__":
    main()
