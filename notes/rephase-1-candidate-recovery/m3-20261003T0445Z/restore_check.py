"""Restored-copy positive diagnostic ONLY (no five-test repeat).

Usage: venv-python restore_check.py <restoreroot> <rawdir>
Verifies identity guards then runs current_closure(root) +
_verify_head_bytes(root, EXACT_NEW_HEAD, closure) expecting clean return.
No file mutations. Pinned external venv. Offline (inherits NO_LAZY_FETCH).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

EXACT_NEW_HEAD = "b40de600e9ed1f80cb278213ccf17aa5f3cd9de3"
EXP_TREE = "657032438c6ed8b1c055d5a120b67b4b261a5092"
EXP_PARENT = "774dd39a951c9ac3818e83dfffd4c7666efb0a20"
SCRUB = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
         "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_NAMESPACE",
         "GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM")


def main() -> int:
    root = Path(sys.argv[1])
    raw = Path(sys.argv[2])
    raw.mkdir(parents=True, exist_ok=True)
    for key in SCRUB:
        os.environ.pop(key, None)
    os.environ["GIT_NO_LAZY_FETCH"] = "1"
    os.environ["GIT_ALLOW_PROTOCOL"] = "file"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ.pop("PYTHONPATH", None)
    (raw / "restore-check-argv.txt").write_text(
        f"argv={sys.argv}\ncwd={os.getcwd()}\nroot={root}\ncommit={EXACT_NEW_HEAD}\n"
        "env=GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file PYTHONDONTWRITEBYTECODE=1\n",
        encoding="utf-8")

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(root), *args],
                              capture_output=True, text=True, check=False)

    head = git("rev-parse", "HEAD").stdout.strip()
    tree = git("rev-parse", "HEAD^{tree}").stdout.strip()
    parent = git("log", "--format=%P", "-1").stdout.strip()
    status = git("status", "--porcelain").stdout
    diff = git("diff", "--quiet", "HEAD").returncode
    (raw / "restore-check-identity.txt").write_text(
        f"head={head}\ntree={tree}\nparent={parent}\n"
        f"tracked_diff_exit={diff}\nstatus:\n{status}", encoding="utf-8")
    assert head == EXACT_NEW_HEAD, f"HEAD {head}"
    assert tree == EXP_TREE, f"tree {tree}"
    assert parent == EXP_PARENT, f"parent {parent}"
    assert diff == 0, "tracked bytes differ in restored copy"

    sys.path.insert(0, str(root))
    import scripts.survey_weekly_derivation_v2 as deriv  # noqa: E402
    src = Path(deriv.__file__)
    (raw / "restore-check-source.txt").write_text(
        f"module={deriv.__name__}\nfile={src}\n"
        f"sha256={hashlib.sha256(src.read_bytes()).hexdigest()}\n",
        encoding="utf-8")
    closure = deriv.current_closure(root)
    (raw / "restore-check-rows.txt").write_text(
        json.dumps(closure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    deriv._verify_head_bytes(root, EXACT_NEW_HEAD, closure)
    (raw / "restore-check-positive.txt").write_text(
        f"restored_positive=PASS rows={len(closure)} commit={EXACT_NEW_HEAD}\n",
        encoding="utf-8")
    print(f"restored_positive=PASS rows={len(closure)}")
    after = git("status", "--porcelain").stdout
    assert git("diff", "--quiet", "HEAD").returncode == 0
    assert after == status, "worktree changed by read-only probe"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
