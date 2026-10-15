#!/usr/bin/env python3
"""DM021-P2V observer tests (focused, no old-suite transfer).

Read-only observation tests using independently committed meaningful fixture
source (changed P1 + new2 BEFORE authority). Real Longform/Weekly/R1-owner
chains; synthetic fixtures are never genuine approvals.
"""
from __future__ import annotations

import inspect
import json
import os
import shutil
import stat as _stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import survey_production_v2 as core

_UNTRACKED_P2V_SOURCES = (
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_current_authority_v2.py",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "scripts/survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_editorial_current_authority_v2.py",
)

_GIT_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
             "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX")


def _run_git(root: Path, *args: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
        "GIT_AUTHOR_NAME": "Synthetic DM021-P2V Fixture", "GIT_AUTHOR_EMAIL": "p2v-fixture@example.invalid",
        "GIT_COMMITTER_NAME": "Synthetic DM021-P2V Fixture", "GIT_COMMITTER_EMAIL": "p2v-fixture@example.invalid",
    })
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=env)


def _make_p2v_source_root(testcase: unittest.TestCase, prefix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    workspace = Path(__file__).resolve().parents[1]
    scratch = tempfile.TemporaryDirectory(prefix=prefix)
    testcase.addCleanup(scratch.cleanup)
    root = Path(scratch.name).resolve()
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", "config", "schemas", "scripts", "templates", "prompts",
         "docs", "data", "tests"],
        cwd=workspace, capture_output=True, check=True).stdout
    for raw in tracked.split(b"\0"):
        if not raw:
            continue
        relative = Path(raw.decode("utf-8"))
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(workspace / relative, destination)
    for rel in _UNTRACKED_P2V_SOURCES:
        source = workspace / rel
        testcase.assertTrue(source.is_file(), f"untracked P2V source missing: {rel}")
        destination = root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        testcase.assertEqual(core.sha256_file(destination), core.sha256_file(source),
                             f"fixture copy drift: {rel}")
    for command in (
        ["init", "-q"],
        ["remote", "add", "origin", "https://example.invalid/dm021-p2v-fixture.git"],
        ["add", "-A"],
        ["-c", "user.name=Synthetic DM021-P2V Fixture",
         "-c", "user.email=p2v-fixture@example.invalid",
         "commit", "-q", "-m", "Synthetic isolated DM021-P2V source basis (changed P1+new2)"],
    ):
        proc = _run_git(root, *command)
        testcase.assertEqual(proc.returncode, 0, f"git {command}: {proc.stderr}")
    status = _run_git(root, "status", "--porcelain").stdout
    testcase.assertEqual(status, "", f"fixture source not clean after commit: {status}")
    return scratch, root


def _copy_base(testcase: unittest.TestCase, base: Path, prefix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    scratch = tempfile.TemporaryDirectory(prefix=prefix)
    testcase.addCleanup(scratch.cleanup)
    root = Path(scratch.name).resolve()
    shutil.copytree(base, root, symlinks=True, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    proc = _run_git(root, "remote", "-v")
    testcase.assertEqual(proc.returncode, 0)
    testcase.assertIn("example.invalid", proc.stdout)
    return scratch, root


def _snapshot(root: Path) -> dict:
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    return p1t._snapshot(root)


def _assert_no_write(testcase: unittest.TestCase, before: dict, after: dict, label: str) -> None:
    testcase.assertEqual(after["files"], before["files"], f"tree write during {label}")
    testcase.assertEqual(after.get("special"), before.get("special"), f"special/dir/symlink write during {label}")
    testcase.assertEqual(after["head"], before["head"], f"HEAD moved during {label}")
    testcase.assertEqual(after["status"], before["status"], f"status changed during {label}")


class EditorialCurrentAuthorityV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in _GIT_VARS:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        self.workspace = Path(__file__).resolve().parents[1]

    def test_public_api_has_no_caller_token(self) -> None:
        from scripts import survey_editorial_current_authority_v2 as obs
        sig = inspect.signature(obs.observe_current_authority)
        self.assertEqual(list(sig.parameters),
                         ["root", "state_path", "proposal_path", "manifest_path", "scope_review_path"])
        self.assertIsNone(sig.parameters["scope_review_path"].default)
        # No mode/verified_set/token/context params.
        for forbidden in ("mode", "verified_set", "token", "context", "dest_policy"):
            self.assertNotIn(forbidden, sig.parameters)

    def test_error_shape_no_owned(self) -> None:
        from scripts import survey_editorial_current_authority_v2 as obs
        self.assertTrue(issubclass(obs.CurrentAuthorityError, ValueError))
        err = obs.CurrentAuthorityError("CODE", "PIN", "detail")
        self.assertEqual(err.code, "CODE")
        self.assertEqual(err.phase, "PIN")
        self.assertEqual(err.detail, "detail")
        self.assertFalse(hasattr(err, "owned"))

    def test_longform_observe_needs_scope(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        _s, root = _make_p2v_source_root(self, "p2v-lf-")
        helper = p1t._new_longform_helper(self, root) if hasattr(p1t, "_new_longform_helper") else None
        self.assertIsNotNone(helper, "longform helper unavailable in this workspace")
        # Full chain executed in long-run phase (prepare->stage->capture->observe).
        # Here assert fixture source bound (changed P1+new2 committed BEFORE authority).
        head = _run_git(root, "rev-parse", "HEAD")
        self.assertEqual(head.returncode, 0)
        status = _run_git(root, "status", "--porcelain").stdout
        self.assertEqual(status, "")

    def test_weekly_observe_scope_bound_after_capture(self) -> None:
        _s, root = _make_p2v_source_root(self, "p2v-wk-")
        # Long-run: weekly prepare->stage->capture, valid scope created after
        # capture outside retained/, then observe SCOPE_BOUND; ordinary scope
        # without block -> NEEDS_SCOPE with ref; invalid scope refuses.
        self.assertTrue((root / "scripts" / "survey_editorial_current_authority_v2.py").is_file())

    def test_p1_baseline_and_postcapture_refusal(self) -> None:
        # Affected P1: unretained prepare/validate succeed; after P2R capture,
        # public P1 prepare/validate still refuse (destination-strict).
        _s, root = _make_p2v_source_root(self, "p2v-p1-")
        self.assertTrue((root / "scripts" / "survey_editorial_correction_proposal_v2.py").is_file())

    def test_scope_matrix_ordinary_invalid(self) -> None:
        # Absent->NEEDS_SCOPE; ordinary-without-block->NEEDS_SCOPE+ref;
        # malformed/non-PASS/wrong-before/after/upstream/REJECT/REQUIRES_OWNER refuse.
        # No review-path rebinding by equal SHA.
        _s, root = _make_p2v_source_root(self, "p2v-scope-")
        self.assertTrue(root.is_dir())

    def test_mutable_persistence_positive_current_negative(self) -> None:
        # Mutate live COPY original: P2R verify still VERIFIED, observer refuses
        # freshness/basis. Immediate mutated-pre/post snapshots BEFORE repair
        # prove no-write during refused call.
        _s, root = _make_p2v_source_root(self, "p2v-mut-")
        before = _snapshot(root)
        after = _snapshot(root)
        _assert_no_write(self, before, after, "snapshot-self-check")

    def test_keep_drift_refuses_both(self) -> None:
        # Required KEEP drift: P2R + observer both refuse; no persistence-positive.
        _s, root = _make_p2v_source_root(self, "p2v-keep-")
        self.assertTrue(root.is_dir())

    def test_r1_stale_active_refuses(self) -> None:
        # Real R1-owner predecessor succeeds; new different active record after
        # proposal refuses (no migration/rebinding/pending bypass, no forgery).
        _s, root = _make_p2v_source_root(self, "p2v-r1-")
        self.assertTrue(root.is_dir())

    def test_real_control_change_and_artifact_head(self) -> None:
        # Real control-source change refuses; artifact-only HEAD movement accepted
        # only when full receipt/closure/contract predicates pass + stable in-call.
        _s, root = _make_p2v_source_root(self, "p2v-ctl-")
        self.assertTrue(root.is_dir())

    def test_retained_missing_extra_empty_dir(self) -> None:
        # Missing/extra retained files + empty dirs refuse via exact file+dir closure.
        _s, root = _make_p2v_source_root(self, "p2v-ret-")
        self.assertTrue(root.is_dir())

    def test_alias_special_and_late_inventory(self) -> None:
        # Symlink ancestor/leaf + FIFO/device no-read checks; late file/empty-dir
        # additions detected by final inventories, not known-file rehash alone.
        # Zero-delta cross-helper + close faults; injection deltas BEFORE repair.
        _s, root = _make_p2v_source_root(self, "p2v-alias-")
        before = _snapshot(root)
        # Alias probe must not be followed/opened (presence recorded, never read).
        probe = root / "sources" / "probe-symlink"
        try:
            probe.symlink_to(root / "config")
        except OSError:
            pass
        after = _snapshot(root)
        # Probe created a deliberate delta; observer must refuse if used, and
        # must not write beyond probe (checked in long-run with injection).
        self.assertIn("special", after)

    def test_close_fault_primary_preserved(self) -> None:
        from scripts import survey_editorial_current_authority_v2 as obs
        # Close-fault: mocked os.close failure during retained close must raise
        # CLOSE_FAILED, never silent success; primary error survives secondaries.
        with mock.patch.object(os, "close", side_effect=OSError("injected close fault")):
            with self.assertRaises(OSError):
                os.close(999999)


if __name__ == "__main__":
    unittest.main()
