#!/usr/bin/env python3
"""DM021-P1 R4 FINAL exclusive runner — NEW, authored 2026-10-12T072355Z.

Focused P1 (9 methods) + affected gate controls (27) once, timeout 5400s
(prior 3255s measured). Explicit-raise, exclusive O_EXCL logs, sanitized
no-network Git for PARENT and CHILD (forced GIT_NO_LAZY_FETCH=1,
GIT_OPTIONAL_LOCKS=0, GIT_ALLOW_PROTOCOL=file), reject inherited GIT_* /
PYTHONPATH / PYTHONHOME / optimize BEFORE any candidate Git calls, check every
Git rc, record argv/cwd/interpreter/env, compare all13 hashes/modes/named-status/
base pre AND finally-post, preserve timeout partials. NEVER delete/repair
source/cache before comparison; record caches separately (no cleanup).
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261012T072355Z-correction4")
MODULES = ["tests.test_survey_editorial_correction_proposal_v2",
           "tests.test_survey_reader_surface_gate_v2"]
TIMEOUT_S = 5400
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
EXPECTED_ROWS = sorted([f" M {p}" for p in EXPECTED_MODIFIED] + [f"?? {p}" for p in EXPECTED_NEW])
FORCED_GIT = {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"}


def fail(msg: str) -> int:
    print(f"RUNNER_REFUSAL: {msg}", flush=True)
    return 40


def xwrite_text(path: Path, text: str) -> None:
    # Atomic exclusive creation (O_EXCL); refuses if exists (no clobber race).
    try:
        with open(path, "x", encoding="utf-8") as fh:
            fh.write(text)
    except FileExistsError:
        raise RuntimeError(f"log output already exists (exclusivity): {path.name}") from None


def sanitized_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("PYTHONPATH", "PYTHONHOME")}
    env.update(FORCED_GIT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def git_parent(*args: str) -> subprocess.CompletedProcess:
    # Sanitized no-network Git for PARENT (forced 3 vars), rc checked by caller.
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True,
                          env=sanitized_env())


def freeze() -> dict:
    # Every parent Git rc checked explicitly (no silent empty head/tree/status).
    head = git_parent("rev-parse", "HEAD")
    if head.returncode != 0:
        raise RuntimeError(f"parent git rev-parse HEAD rc={head.returncode}: {head.stderr[:500]}")
    tree = git_parent("rev-parse", "HEAD^{tree}")
    if tree.returncode != 0:
        raise RuntimeError(f"parent git rev-parse tree rc={tree.returncode}: {tree.stderr[:500]}")
    status = git_parent("status", "--porcelain")
    if status.returncode != 0:
        raise RuntimeError(f"parent git status rc={status.returncode}: {status.stderr[:500]}")
    state: dict = {"head": head.stdout.strip(), "tree": tree.stdout.strip(),
                   "status": status.stdout, "files": {}}
    for rel in EXPECTED_MODIFIED + EXPECTED_NEW:
        full = REPO / rel
        data = full.read_bytes()
        state["files"][rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                               "mode": oct(stat.S_IMODE(full.lstat().st_mode)),
                               "bytes": len(data)}
    return state


def named_status(status_text: str) -> list[str]:
    # Named-status: only the 13 expected overlay rows (caches ignored, recorded separately).
    rows = []
    for line in status_text.splitlines():
        for exp in EXPECTED_ROWS:
            if line == exp:
                rows.append(line)
                break
    return sorted(rows)


def list_caches() -> dict:
    # Record cache side effects separately (no deletion, no repair).
    found: dict[str, list[str]] = {}
    for base in ("scripts/__pycache__", "tests/__pycache__", "schemas/__pycache__"):
        full = REPO / base
        if full.is_dir():
            try:
                found[base] = sorted(p.name for p in full.iterdir())
            except OSError as exc:
                found[base] = [f"UNREADABLE: {exc}"]
    return found


def main() -> int:
    # Reject inherited routing/optimize BEFORE any candidate Git calls.
    if sys.flags.optimize != 0:
        return fail(f"optimized mode (optimize={sys.flags.optimize})")
    bad_git = sorted(k for k in os.environ if k.startswith("GIT_"))
    if bad_git:
        return fail(f"inherited Git routing present before Git calls: {bad_git}")
    bad_py = sorted(k for k in ("PYTHONPATH", "PYTHONHOME") if k in os.environ)
    if bad_py:
        return fail(f"inherited Python routing present: {bad_py}")
    EVID.mkdir(parents=True, exist_ok=True)
    # Record exact argv/cwd/interpreter/env (sanitized forced Git3 for evidence).
    try:
        xwrite_text(EVID / "runner-meta.json", json.dumps({
            "argv": sys.argv, "cwd": os.getcwd(), "interpreter": sys.executable,
            "python": sys.version, "optimize": sys.flags.optimize,
            "forced_git": FORCED_GIT,
            "inherited_git_rejected": bad_git, "inherited_python_rejected": bad_py,
        }, indent=1) + "\n")
    except RuntimeError as exc:
        return fail(str(exc))
    # Exclusive deps log (atomic, no existence-then-write race).
    try:
        with open(EVID / "deps.txt", "x", encoding="utf-8") as handle:
            handle.write(f"python={sys.version}\n")
            handle.write(f"optimize={sys.flags.optimize}\n")
            handle.write(f"interpreter={sys.executable}\n")
            handle.write(f"argv={sys.argv}\n")
            handle.write(f"cwd={os.getcwd()}\n")
            for probe in ("jsonschema", "pypdf", "yaml"):
                try:
                    module = __import__(probe)
                    handle.write(f"{probe}=present {getattr(module, '__version__', 'unknown')}\n")
                except ImportError:
                    handle.write(f"{probe}=MISSING\n")
            gv = git_parent("--version")
            if gv.returncode != 0:
                return fail(f"parent git --version rc={gv.returncode}")
            handle.write(f"{gv.stdout.strip()}\n")
            handle.write(f"forced_git={FORCED_GIT}\n")
    except FileExistsError:
        return fail("log output already exists (exclusivity): deps.txt")
    deps = (EVID / "deps.txt").read_text(encoding="utf-8")
    print(deps, end="", flush=True)
    if "MISSING" in deps:
        return fail("runtime dependency missing (blocker, no network)")
    try:
        pre = freeze()
    except RuntimeError as exc:
        return fail(str(exc))
    try:
        xwrite_text(EVID / "freeze-pre.json", json.dumps(pre, indent=1) + "\n")
    except RuntimeError as exc:
        return fail(str(exc))
    print(f"pre head={pre['head']} tree={pre['tree']}", flush=True)
    if sorted(named_status(pre["status"])) != EXPECTED_ROWS:
        print("observed named-status:", flush=True)
        print("\n".join(named_status(pre["status"])), flush=True)
        return fail("pre-run named overlay is not exactly 3M10A")
    print("pre-freeze 3M10A named exact", flush=True)
    if pre["head"] != "409b292756dd1277b9dfae87679934c0d2ce251c":
        return fail(f"pre HEAD not actual409: {pre['head']}")
    if pre["tree"] != "8ce3699861505f32d1d60bdc185d4d4f635aedb2":
        return fail(f"pre tree not base 8ce: {pre['tree']}")
    print(f"sanitized parent+child forced Git: {sorted(FORCED_GIT)}", flush=True)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", *MODULES, "-v"],
            cwd=REPO, capture_output=True, text=True, timeout=TIMEOUT_S,
            env=sanitized_env())
        try:
            xwrite_text(EVID / "run.stdout.txt", proc.stdout)
        except RuntimeError as exc:
            return fail(str(exc))
        try:
            xwrite_text(EVID / "run.stderr.txt", proc.stderr)
        except RuntimeError as exc:
            return fail(str(exc))
        try:
            xwrite_text(EVID / "run.exit", f"exit={proc.returncode}\n")
        except RuntimeError as exc:
            return fail(str(exc))
        print(f"tests exit={proc.returncode}", flush=True)
        print("--- unittest tail ---", flush=True)
        print("\n".join((proc.stdout + proc.stderr).splitlines()[-20:]), flush=True)
    except subprocess.TimeoutExpired as exc:
        partial_out = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        partial_err = (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        try:
            xwrite_text(EVID / "run.stdout.txt", partial_out)
            xwrite_text(EVID / "run.stderr.txt", partial_err + "\nRUNNER_TIMEOUT_PARTIAL\n")
            xwrite_text(EVID / "run.exit", "exit=TIMEOUT\n")
        except RuntimeError as exc2:
            return fail(str(exc2))
        print("RUNNER_TIMEOUT_PARTIAL: partial output preserved", flush=True)
    finally:
        # NO cleanup/deletion before comparison. Record caches separately.
        try:
            caches = list_caches()
        except Exception as exc:
            return fail(f"cache inventory failed: {exc}")
        try:
            xwrite_text(EVID / "caches-post.json", json.dumps(caches, indent=1) + "\n")
        except RuntimeError as exc:
            return fail(str(exc))
        print(f"caches recorded (not deleted): {caches}", flush=True)
        try:
            post = freeze()
        except RuntimeError as exc:
            return fail(str(exc))
        try:
            xwrite_text(EVID / "freeze-post.json", json.dumps(post, indent=1) + "\n")
        except RuntimeError as exc:
            return fail(str(exc))
        same_files = post["files"] == pre["files"]
        same_head = post["head"] == pre["head"] and post["tree"] == pre["tree"]
        same_named = named_status(post["status"]) == named_status(pre["status"])
        print(f"post head={post['head']} files_same={same_files} head_same={same_head} named_same={same_named}", flush=True)
        if not (same_files and same_head and same_named):
            return fail("source moved during tests (files/head/named-status)")
    exit_text = (EVID / "run.exit").read_text(encoding="utf-8").strip()
    if exit_text != "exit=0":
        return fail(f"tests did not exit 0: {exit_text}")
    print("RUNNER_COMPLETE_PASS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
