#!/usr/bin/env python3
"""DM022 normal-writer late-guard tests (General test-author/executor ONLY).

Proves late seam: guard created between ENTRY and PREPUBLISH is refused at
prepublish by the REAL low.require_research_operation_ready (no mock PASS).

Each case:
  healthy counterpart reaches a REAL write (new legitimate output path, no
  clearing of accepted data), then a FRESH independent copy injects an owned
  synthetic guard AFTER entry succeeds and BEFORE the actual prepublish READY
  read. The wrapper records caller file/func/line for entry vs prepublish and
  asserts the exact target seam was reached (no approximate second-call counts).

No existing runtime/test edits. No new acceptance flags, no caller-verified
tokens, no authority mocking. Synthetic fault nonce explicit; ANY guard
refuses (no legal HIGH owner required). No global CAS claim. Injection is
before the checked seam, not after the final checkpoint.

Fixtures:
  - selection seven writes: fresh EVIDENCE_REVIEWED via full-lifecycle helpers
  - execution_record: fresh C2 ready root with NEW session_id
  - publication/manuscript/gate: DURABLE VALIDATED_DRAFT copies with NEW out
  - retention: P1 scope fixture (genuine capture) with NEW temp copy
  - evidence/draft/agent/humangate/editorial: full-lifecycle helpers where
    feasible; otherwise reported as missing capability (no waiver).
"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

FAULT_NONCE_PREFIX = "synthetic-late-guard-v2-"


def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_json(p: Path, payload: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _snapshot_files(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        try:
            if p.is_symlink() or not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
        except ValueError:
            continue
        if rel.startswith(".git/"):
            continue
        if "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        out[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_ALLOW_PROTOCOL": "file",
        "GIT_AUTHOR_NAME": "Synthetic DM022 Late-Guard Fixture",
        "GIT_AUTHOR_EMAIL": "late-guard@example.invalid",
        "GIT_COMMITTER_NAME": "Synthetic DM022 Late-Guard Fixture",
        "GIT_COMMITTER_EMAIL": "late-guard@example.invalid",
    })
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True, env=env)


def _copy_durable_to_temp(testcase: unittest.TestCase, durable_path: Path, prefix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    td = tempfile.TemporaryDirectory(prefix=prefix)
    testcase.addCleanup(td.cleanup)
    dst = Path(td.name).resolve() / "fixture"
    # Byte copy incl .git (needed for HEAD pins where used), no hardlinks,
    # no pycache. Original outside packet is never mutated.
    shutil.copytree(
        durable_path, dst, symlinks=False,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    # Safety: no alternates, no inherited GIT_* (checked by caller env).
    return td, dst


class LateGuardInjector:
    """Wraps REAL low.require_research_operation_ready.

    Records (direct caller file/line/fn, outer caller file/line/fn) for every
    call. Injects an owned synthetic guard ONLY when the outer caller matches
    the exact prepublish seam (file substring, func, line). Otherwise passes
    through to the REAL helper. Asserts target reached.
    """

    def __init__(self, guard_path: Path, target_file_sub: str, target_fn: str, target_line: int, entry_line: int | None = None, entry_fn: str | None = None):
        self.guard_path = guard_path
        self.target_file_sub = target_file_sub
        self.target_fn = target_fn
        self.target_line = target_line
        self.entry_line = entry_line
        self.entry_fn = entry_fn if entry_fn is not None else target_fn
        self.calls: list[dict] = []
        self.injected = False
        self.target_reached = False
        self.entry_reached = False
        from scripts import survey_research_authority_v2 as low
        self._orig = low.require_research_operation_ready
        self._low = low

    def _outer_frame(self) -> tuple[str, int, str, str, int, str]:
        # stack[0]=_outer_frame, [1]=__call__ (fixture), [2]=_dm022 wrapper, [3]=business fn
        st = inspect.stack()
        try:
            direct = st[2] if len(st) > 2 else st[1]
            outer = st[3] if len(st) > 3 else (st[2] if len(st) > 2 else st[1])
            return (
                direct.filename, direct.lineno, direct.function,
                outer.filename, outer.lineno, outer.function,
            )
        finally:
            del st

    def __call__(self, repo_root: Path, state_path: Path) -> None:
        d_file, d_line, d_fn, o_file, o_line, o_fn = self._outer_frame()
        self.calls.append({
            "direct_file": d_file, "direct_line": d_line, "direct_fn": d_fn,
            "outer_file": o_file, "outer_line": o_line, "outer_fn": o_fn,
        })
        is_target = (
            self.target_file_sub in o_file
            and o_fn == self.target_fn
            and o_line == self.target_line
        )
        is_entry = (
            self.entry_line is not None
            and self.target_file_sub in o_file
            and o_fn == self.entry_fn
            and o_line == self.entry_line
        )
        if is_entry:
            self.entry_reached = True
        if is_target:
            self.target_reached = True
            if not self.injected:
                # Owned synthetic fault guard: ANY present refuses, no legal
                # HIGH owner required. Explicit synthetic nonce.
                self.guard_path.parent.mkdir(parents=True, exist_ok=True)
                nonce = f"{FAULT_NONCE_PREFIX}{self.target_fn}-{self.target_line}-{os.getpid()}"
                _write_json(self.guard_path, {"phase": "TEST", "nonce": nonce})
                self.injected = True
        # Always call REAL helper (never mock PASS).
        return self._orig(repo_root, state_path)

    def install(self, testcase: unittest.TestCase) -> None:
        from scripts import survey_research_authority_v2 as low
        orig = low.require_research_operation_ready
        testcase.assertIs(orig, self._orig, "low.require changed before install")
        low.require_research_operation_ready = self  # type: ignore
        def _restore() -> None:
            low.require_research_operation_ready = orig  # type: ignore
        testcase.addCleanup(_restore)
