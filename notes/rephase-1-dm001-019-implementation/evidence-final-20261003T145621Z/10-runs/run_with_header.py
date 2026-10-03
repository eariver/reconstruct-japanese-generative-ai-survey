#!/usr/bin/env python3
"""Header-bound module runner: per-module HEAD/tree/parent/source-hash + argv/env/exit.

Usage: run_with_header.py <impl-dir> <venv-python> <out-dir> <test-file>...
Each module runs in its own subprocess with cwd=impl-dir. Combined log per
module: header, stdout, stderr, footer. Exit nonzero if any module fails.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path

IMPL = Path(sys.argv[1]).resolve()
VENV_PY = sys.argv[2]
OUT = Path(sys.argv[3])
MODULES = sys.argv[4:]

BASE_ENV = {
    "PATH": "/usr/bin:/bin",
    "PYTHONDONTWRITEBYTECODE": "1",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_ALLOW_PROTOCOL": "file",
    "PYTHONPATH": str(IMPL),
}

TRACKED = [
    "scripts/survey_publication_v2.py",
    "scripts/survey_profiled_freeze_v2.py",
    "tests/test_survey_dm001_019_freeze_equivalence_v2.py",
]


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(IMPL), *args], capture_output=True, text=True,
        env={"PATH": "/usr/bin:/bin", "GIT_NO_LAZY_FETCH": "1",
             "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"},
        check=True,
    )
    return proc.stdout.strip()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    parent = git("rev-parse", "HEAD^")
    status = git("status", "--porcelain=v1", "--untracked-files=no")
    sources = []
    for rel in TRACKED:
        blob = git("ls-files", "-s", "--", rel).split()[1]
        work = hashlib.sha256((IMPL / rel).read_bytes()).hexdigest()
        sources.append(f"{rel} blob={blob} worktree_sha256={work}")
    failures = 0
    for mod in MODULES:
        argv = [VENV_PY, mod, "-v"]
        start = time.time()
        proc = subprocess.run(
            argv, capture_output=True, text=True, cwd=str(IMPL), env=dict(BASE_ENV),
            timeout=3600,
        )
        elapsed = time.time() - start
        log = OUT / (Path(mod).stem + ".log")
        log.write_text(
            "=== header ===\n"
            f"HEAD={head}\nTREE={tree}\nPARENT={parent}\n"
            f"STATUS_CLEAN={status == ''}\n"
            + "".join(f"SOURCE_{row}\n" for row in sources)
            + f"ARGV={' '.join(argv)}\nRUNTIME={VENV_PY}\n"
            + "".join(f"ENV_{k}={v}\n" for k, v in sorted(BASE_ENV.items()))
            + f"ELAPSED_S={elapsed:.3f}\nEXIT={proc.returncode}\n"
            + "=== stdout ===\n" + proc.stdout
            + "=== stderr ===\n" + proc.stderr,
            encoding="utf-8",
        )
        print(f"{mod}: exit={proc.returncode} elapsed={elapsed:.1f}s", flush=True)
        if proc.returncode != 0:
            failures += 1
    print(f"HEAD={head} TREE={tree} PARENT={parent} failures={failures}", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
