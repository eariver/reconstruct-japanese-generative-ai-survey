#!/usr/bin/env python3
"""DM021-P1 Phase B strict runner — NEW, authored 2026-10-11T16:31:14Z.

Executes exactly: tests.test_survey_editorial_correction_proposal_v2 (new P1
focused tests) + tests.test_survey_reader_surface_gate_v2 (affected existing
control for the shared-schema modification). No other suite, no decoration.

Fail-closed, explicit-raise structure (unittest asserts are evidence, not
safety): dependency availability first, exact 13-path freeze pre AND
finally-post, sanitized routing (no inherited GIT_*, no PYTHONPATH, forced
no-network Git), exclusive logs, timeout with partial output preserved.
"""
from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261011T190450Z-phaseB")
MODULES = ["tests.test_survey_editorial_correction_proposal_v2",
           "tests.test_survey_reader_surface_gate_v2"]
TIMEOUT_S = 3300

EXPECTED_MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
EXPECTED_NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]


def fail(message: str) -> int:
    print(f"RUNNER_REFUSAL: {message}")
    return 40


def freeze() -> dict:
    state: dict = {
        "head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                               capture_output=True, text=True).stdout.strip(),
        "tree": subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=REPO,
                               capture_output=True, text=True).stdout.strip(),
        "status": subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                                 capture_output=True, text=True).stdout,
        "files": {},
    }
    for rel in EXPECTED_MODIFIED + EXPECTED_NEW:
        full = REPO / rel
        data = full.read_bytes()
        state["files"][rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                               "mode": oct(stat.S_IMODE(full.lstat().st_mode)),
                               "bytes": len(data)}
    return state


def main() -> int:
    for name in ("run.stdout.txt", "run.stderr.txt", "run.exit", "freeze-pre.json",
                 "freeze-post.json", "deps.txt"):
        if (EVID / name).exists():
            return fail(f"log output already exists (exclusivity): {name}")
    import json as _json
    EVID.mkdir(parents=True, exist_ok=True)

    with open(EVID / "deps.txt", "w", encoding="utf-8") as handle:
        handle.write(f"python={sys.version}\n")
        for probe in ("jsonschema", "pypdf", "yaml"):
            try:
                module = __import__(probe)
                handle.write(f"{probe}=present {getattr(module, '__version__', 'unknown')}\n")
            except ImportError:
                handle.write(f"{probe}=MISSING\n")
        gitv = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
        handle.write(f"{gitv}\n")
    deps = (EVID / "deps.txt").read_text(encoding="utf-8")
    print(deps, end="")
    if "MISSING" in deps:
        return fail("runtime dependency missing; refusing network setup (blocker)")

    pre = freeze()
    (EVID / "freeze-pre.json").write_text(_json.dumps(pre, indent=1) + "\n", encoding="utf-8")
    print(f"pre head={pre['head']} tree={pre['tree']}")
    rows = sorted(pre["status"].splitlines())
    expected_rows = sorted([f" M {p}" for p in EXPECTED_MODIFIED] + [f"?? {p}" for p in EXPECTED_NEW])
    if rows != expected_rows:
        print("observed status:")
        print(pre["status"], end="")
        return fail("pre-run overlay is not exactly 3M10A")
    print("pre-freeze 3M10A exact")

    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1"})
    print(f"sanitized GIT routes: {[k for k in env if k.startswith('GIT_')]}")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", *MODULES, "-v"],
            cwd=REPO, capture_output=True, text=True, timeout=TIMEOUT_S, env=env)
        (EVID / "run.stdout.txt").write_text(proc.stdout)
        (EVID / "run.stderr.txt").write_text(proc.stderr)
        (EVID / "run.exit").write_text(f"exit={proc.returncode}\n")
        print(f"tests exit={proc.returncode}")
        print("--- unittest tail ---")
        print("\n".join((proc.stdout + proc.stderr).splitlines()[-15:]))
    except subprocess.TimeoutExpired as exc:
        partial_out = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        partial_err = (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        (EVID / "run.stdout.txt").write_text(partial_out)
        (EVID / "run.stderr.txt").write_text(partial_err + "\nRUNNER_TIMEOUT_PARTIAL\n")
        (EVID / "run.exit").write_text("exit=TIMEOUT\n")
        print("RUNNER_TIMEOUT_PARTIAL: partial output preserved")
    finally:
        for cache in ("scripts/__pycache__", "tests/__pycache__"):
            full = REPO / cache
            if full.is_dir():
                import shutil as _shutil
                _shutil.rmtree(full)
                print(f"removed run byproduct dir: {cache}")
        post = freeze()
        (EVID / "freeze-post.json").write_text(_json.dumps(post, indent=1) + "\n", encoding="utf-8")
        same_files = post["files"] == pre["files"]
        same_head = post["head"] == pre["head"] and post["tree"] == pre["tree"]
        same_status = post["status"] == pre["status"]
        print(f"post head={post['head']} files_same={same_files} head_same={same_head} status_same={same_status}")
        if not (same_files and same_head and same_status):
            return fail("restored source moved during test execution")
    exit_text = (EVID / "run.exit").read_text(encoding="utf-8").strip()
    if exit_text != "exit=0":
        return fail(f"test run did not exit 0: {exit_text}")
    print("RUNNER_COMPLETE_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
