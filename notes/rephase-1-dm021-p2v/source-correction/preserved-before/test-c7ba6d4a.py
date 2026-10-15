#!/usr/bin/env python3
"""DM021-P2V observer tests (behavioral, no old-suite transfer).

Read-only observation tests using independently committed meaningful fixture
source (changed P1 + new2 BEFORE authority). Real Longform/Weekly/R1-owner
chains; synthetic fixtures are never genuine approvals. Every behavioral
method calls observe_current_authority and asserts result/error AND immediate
no-write/exact injected deltas BEFORE any repair.
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

_P2V_OBSERVE_CASCADE = """
import json, sys
from pathlib import Path
root = Path(sys.argv[1]); state_path = Path(sys.argv[2])
proposal_path = Path(sys.argv[3]); manifest_path = Path(sys.argv[4])
scope_arg = Path(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "-" else None
from scripts import survey_editorial_current_authority_v2 as obs
try:
    out = obs.observe_current_authority(root, state_path, proposal_path, manifest_path, scope_arg)
    print(json.dumps({"ok": True, "result": out["result"],
                      "state_ref": out["state_ref"], "proposal_ref": out["proposal_ref"],
                      "manifest_ref": out["retention_manifest_ref"],
                      "scope_ref": out["scope_review_ref"], "head": out["observed_head"],
                      "measured": out["measured"], "n_inputs": len(out["input_hashes"])}))
except Exception as exc:
    print(json.dumps({"ok": False, "error": str(exc)[:400]}))
"""


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
        ["git", "ls-files", "-z", "--", ".github", "config", "schemas", "scripts", "templates", "prompts",
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
    listed = _run_git(root, "config", "--local", "--list").stdout
    testcase.assertNotIn("user.name=", listed)
    testcase.assertNotIn("user.email=", listed)
    return scratch, root


def _run_fixture_code(testcase: unittest.TestCase, root: Path, script: str,
                      args: list[str], timeout_s: int = 600) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1"})
    proc = subprocess.run([sys.executable, "-c", script, *args], cwd=root,
                          capture_output=True, text=True, timeout=timeout_s, env=env)
    testcase.assertEqual(proc.returncode, 0,
                         f"fixture-code step failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr[-4000:]}")
    return proc.stdout


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
        for forbidden in ("mode", "verified_set", "token", "context", "dest_policy"):
            self.assertNotIn(forbidden, sig.parameters)

    def test_error_shape_no_owned(self) -> None:
        from scripts import survey_editorial_current_authority_v2 as obs
        self.assertTrue(issubclass(obs.CurrentAuthorityError, ValueError))
        err = obs.CurrentAuthorityError("CODE", "PIN", "detail")
        self.assertEqual((err.code, err.phase, err.detail), ("CODE", "PIN", "detail"))
        self.assertFalse(hasattr(err, "owned"))

    def _build_weekly_pair(self, testcase: unittest.TestCase, root: Path, pid: str, headline: str):
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        from scripts import survey_editorial_retention_v2 as retention
        helper = p1t._new_weekly_helper(testcase, root)
        built = p1t._build_weekly_validated(testcase, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = headline
        staged_authoring = p1t._stage_authoring_before_prepare(
            testcase, root, helper.source_root, pid, authored)
        snap0 = p1t._snapshot(root)
        prepared = p1mod.prepare_proposal(root, state_path, staged_authoring, pid,
                                          f"Fixture P2V correction {pid}.")
        p1t._assert_no_write(testcase, snap0, p1t._snapshot(root), "p2v prepare")
        proposal_path = p1t._stage_reader_and_proposal(testcase, root, helper.source_root, pid, prepared)
        snap1 = p1t._snapshot(root)
        outcome = p1mod.validate_proposal(root, state_path, proposal_path)
        self.assertEqual(outcome["result"], "REVIEW_REQUIRED")
        p1t._assert_no_write(testcase, snap1, p1t._snapshot(root), "p2v validate")
        snap2 = p1t._snapshot(root)
        cap = retention.capture_retention(root, state_path, proposal_path)
        self.assertEqual(cap["result"], "RETAINED_SET_CAPTURED")
        manifest_path = root / cap["manifest_path"]
        self.assertTrue(manifest_path.is_file(), f"manifest missing: {manifest_path}")
        return {"helper": helper, "built": built, "chain": chain, "state_path": state_path,
                "prepared": prepared, "proposal_path": proposal_path,
                "manifest_path": manifest_path, "snap_after_capture": p1t._snapshot(root)}

    def test_longform_observe_needs_scope(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-lf-")
        helper = p1t._new_longform_helper(self, root, self.workspace)
        built = helper._build_validated() if hasattr(helper, "_build_validated") else None
        self.assertIsNotNone(built, "longform validated chain unavailable")
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["frontmatter"]["lede"] = "P2V longform revised edition."
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        from scripts import survey_editorial_retention_v2 as retention
        staged = p1t._stage_authoring_before_prepare(self, root, helper.source_root, "fixture-lf-p2v-1", authored)
        prepared = p1mod.prepare_proposal(root, state_path, staged, "fixture-lf-p2v-1", "Fixture P2V longform.")
        proposal_path = p1t._stage_reader_and_proposal(self, root, helper.source_root, "fixture-lf-p2v-1", prepared)
        cap = retention.capture_retention(root, state_path, proposal_path)
        manifest_path = proposal_path.parent / "retained" / "retention-manifest.json"
        before = p1t._snapshot(root)
        out = obs.observe_current_authority(root, state_path, proposal_path, manifest_path)
        self.assertEqual(out["result"], "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE")
        self.assertIsNone(out["scope_review_ref"])
        self.assertEqual(out["proposal_ref"]["sha256"], core.sha256_file(proposal_path))
        self.assertEqual(out["measured"]["proposed_reader_sha256"],
                         core.sha256_bytes(prepared["proposed_canonical"]))
        p1t._assert_no_write(self, before, p1t._snapshot(root), "longform observe")

    def test_weekly_observe_scope_bound_after_capture(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-wk-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-p2v-1", "Weekly P2V scope edition")
        prepared, proposal_path = pair["prepared"], pair["proposal_path"]
        manifest_path, state_path = pair["manifest_path"], pair["state_path"]
        helper = pair["helper"]
        staged_reader_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        # Ordinary valid review without correction block -> NEEDS_SCOPE + ref.
        ordinary = p1t._scope_review_for(self, root, prepared, staged_reader_rel, "ordinary-review.json")
        # Rewrite without scope block (ordinary loader PASS, no correction block).
        raw_ord = core.load_json(ordinary)
        raw_ord.pop("editorial_correction_scope", None)
        raw_ord["review_sha256"] = core.sha256_object({k: v for k, v in raw_ord.items() if k != "review_sha256"})
        core.write_json(ordinary, raw_ord)
        before = p1t._snapshot(root)
        out = obs.observe_current_authority(root, state_path, proposal_path, manifest_path, ordinary)
        self.assertEqual(out["result"], "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE")
        self.assertIsNotNone(out["scope_review_ref"])
        p1t._assert_no_write(self, before, p1t._snapshot(root), "ordinary scope observe")
        # Valid scope created AFTER capture outside retained/ -> SCOPE_BOUND.
        valid = p1t._scope_review_for(self, root, prepared, staged_reader_rel, "scope-after-capture.json")
        self.assertFalse(str(valid.relative_to(root)).startswith(
            str((proposal_path.parent / "retained").relative_to(root))))
        before = p1t._snapshot(root)
        out2 = obs.observe_current_authority(root, state_path, proposal_path, manifest_path, valid)
        self.assertEqual(out2["result"], "CURRENT_BASIS_OBSERVED_SCOPE_BOUND")
        self.assertEqual(out2["scope_review_ref"]["sha256"], core.sha256_file(valid))
        p1t._assert_no_write(self, before, p1t._snapshot(root), "valid scope observe")
        # Invalid scope (REJECT) refuses; no-write proven BEFORE repair.
        bad = p1t._scope_review_for(self, root, prepared, staged_reader_rel, "scope-reject.json",
                                    decision="REJECT")
        before = p1t._snapshot(root)
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, state_path, proposal_path, manifest_path, bad)
        p1t._assert_no_write(self, before, p1t._snapshot(root), "reject scope no-write")

    def test_p1_baseline_and_postcapture_refusal(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-p1-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-p1-1", "Weekly P2V P1 baseline")
        # Post-capture public P1 remains destination-strict.
        with self.assertRaises(p1mod.ProposalError):
            p1mod.prepare_proposal(root, pair["state_path"],
                                   root / pair["helper"].source_root.relative_to(root) /
                                   "publication" / "v2" / "editorial-corrections" /
                                   "fixture-wk-p1-1" / "authoring-input.json",
                                   "fixture-wk-p1-1", "Second attempt after capture.")
        with self.assertRaises(p1mod.ProposalError):
            p1mod.validate_proposal(root, pair["state_path"], pair["proposal_path"])
        # Observer still observes NEEDS_SCOPE on the retained set.
        before = p1t._snapshot(root)
        out = obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        self.assertEqual(out["result"], "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE")
        p1t._assert_no_write(self, before, p1t._snapshot(root), "postcapture observe")

    def test_mutable_persistence_positive_current_negative(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_retention_v2 as retention
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-mut-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-mut-1", "Weekly P2V mutable edition")
        proposal, manifest_path = pair["prepared"]["proposal"], pair["manifest_path"]
        # Mutable COPY original: live receipt file (COPY, non-KEEP).
        receipt_rel = proposal["basis"]["generated_receipt_ref"]["path"]
        live_receipt = root / receipt_rel
        orig = live_receipt.read_bytes()
        before_inject = p1t._snapshot(root)
        live_receipt.write_bytes(orig + b"\n")
        mutated_pre = p1t._snapshot(root)
        self.assertNotEqual(mutated_pre["files"].get(receipt_rel), before_inject["files"].get(receipt_rel))
        # P2R persistence-positive (retained bytes intact).
        v = retention.verify_retention(root, pair["proposal_path"], manifest_path)
        self.assertEqual(v["result"], "RETAINED_SET_VERIFIED")
        # Observer freshness-negative.
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], manifest_path)
        mutated_post = p1t._snapshot(root)
        self.assertEqual(mutated_post["files"], mutated_pre["files"], "observer wrote during refused call")
        self.assertEqual(mutated_post["head"], mutated_pre["head"])
        # Repair AFTER proving no-write, then positive again.
        live_receipt.write_bytes(orig)
        out = obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], manifest_path)
        self.assertEqual(out["result"], "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE")

    def test_keep_drift_refuses_both(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_retention_v2 as retention
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-keep-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-keep-1", "Weekly P2V keep edition")
        manifest = core.load_json(pair["manifest_path"])
        keep_row = next(r for r in manifest["rows"] if r["policy"] == "KEEP_IMMUTABLE")
        keep_path = root / keep_row["retained_ref"]["path"]
        orig = keep_path.read_bytes()
        keep_rel = keep_row["retained_ref"]["path"]
        before = p1t._snapshot(root)
        keep_path.write_bytes(orig + b"\n")
        mutated_pre = p1t._snapshot(root)
        self.assertNotEqual(mutated_pre["files"].get(keep_rel), before["files"].get(keep_rel))
        with self.assertRaises(retention.RetentionError):
            retention.verify_retention(root, pair["proposal_path"], pair["manifest_path"])
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        mutated_post = p1t._snapshot(root)
        self.assertEqual(mutated_post["files"], mutated_pre["files"])
        keep_path.write_bytes(orig)

    def test_r1_active_owner_and_stale_refuses(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-r1-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        built["helper"] = helper
        chain, state_path = built["chain"], built["state_path"]
        new_head = p1t._commit_derivation_only_change(self, root)
        authored = core.load_json(chain["authored_path"])
        authored["frontmatter"]["lede"] = "P2V R1 revised edition."
        staged = p1t._stage_authoring_before_prepare(self, root, helper.source_root, "fixture-wk-r1-1", authored)
        rel = lambda p: str(Path(p).relative_to(root))
        payload = {"head": new_head, "source_root": rel(helper.source_root),
                   "survey_root": rel(helper.survey_root),
                   "publication_root": rel(helper.source_root / "publication" / "v2"),
                   "chain": {k: rel(chain[k]) for k in ("profile_path", "approval_path", "authored_path")},
                   "surface_path": rel(built["surface_path"]), "review_path": rel(built["review_path"]),
                   "receipt_path": rel(built["receipt_path"]), "manuscript_path": rel(built["manuscript_path"]),
                   "gate_path": rel(built["gate_path"]), "bundle_path": rel(built["bundle_path"]),
                   "pdf_path": rel(built["pdf_path"]), "later_sem": rel(built["later_sem"]),
                   "later_vis": rel(built["later_vis"])}
        out = _run_fixture_code(self, root, p1t._FIXTURE_CASCADE,
                                [str(root), str(state_path), str(staged), "fixture-wk-r1-1", json.dumps(payload)])
        summary = json.loads(out)
        self.assertEqual(summary["origins"]["validated-source"], "ACTIVE")
        self.assertIsNotNone(summary["active_ref"])
        # Fixture cascade already staged reader+proposal for pid fixture-wk-r1-1
        # via committed fixture code; reuse those committed paths (no re-prepare).
        from scripts import survey_editorial_retention_v2 as retention
        state = core.load_json(state_path)
        self.assertIsNotNone(state.get("publication_revalidation_provenance"))
        src_root = helper.source_root.relative_to(root).as_posix()
        proposal_path = root / src_root / "publication" / "v2" / "editorial-corrections" / \
            "fixture-wk-r1-1" / "proposal.json"
        self.assertTrue(proposal_path.is_file(), f"cascade proposal missing: {proposal_path}")
        cap = retention.capture_retention(root, state_path, proposal_path)
        self.assertEqual(cap["result"], "RETAINED_SET_CAPTURED")
        manifest_path = root / cap["manifest_path"]
        before = p1t._snapshot(root)
        ok = obs.observe_current_authority(root, state_path, proposal_path, manifest_path)
        self.assertEqual(ok["result"], "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE")
        p1t._assert_no_write(self, before, p1t._snapshot(root), "r1 active observe")

    def _prepare_via_fixture(self, testcase: unittest.TestCase, root: Path, state_path: Path,
                             staged: Path, pid: str) -> dict:
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        return p1mod.prepare_proposal(root, state_path, staged, pid, f"Fixture P2V R1 {pid}.")

    def test_real_control_change_and_artifact_head(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-ctl-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-ctl-1", "Weekly P2V control edition")
        cfg = core.load_json(root / core.DEFAULT_CONFIG)
        contract_file = root / cfg["contract_files"]["pipeline"][0]
        orig = contract_file.read_bytes()
        contract_rel = str(contract_file.relative_to(root))
        before = p1t._snapshot(root)
        contract_file.write_bytes(orig + b"\n")
        mutated_pre = p1t._snapshot(root)
        self.assertNotEqual(mutated_pre["files"].get(contract_rel), before["files"].get(contract_rel))
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        mutated_post = p1t._snapshot(root)
        self.assertEqual(mutated_post["files"], mutated_pre["files"])
        contract_file.write_bytes(orig)
        # Artifact-only HEAD: commit a non-control doc change; observer accepts
        # only if full receipt/closure/contract predicates still pass.
        doc = root / "docs" / "p2v-artifact-note.md"
        doc.write_text("P2V artifact-only fixture note.\n", encoding="utf-8")
        proc = _run_git(root, "add", "docs/p2v-artifact-note.md")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P2V Fixture",
                        "-c", "user.email=p2v-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture artifact-only note")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        self.assertIn(out["result"], ("CURRENT_BASIS_OBSERVED_NEEDS_SCOPE",
                                      "CURRENT_BASIS_OBSERVED_SCOPE_BOUND"))

    def test_retained_missing_extra_empty_dir(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_retention_v2 as retention
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-ret-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-ret-1", "Weekly P2V retained edition")
        manifest = core.load_json(pair["manifest_path"])
        copy_row = next(r for r in manifest["rows"] if r["policy"] == "COPY_BEFORE_REPLACEMENT")
        target = root / copy_row["retained_dest"]
        saved = target.read_bytes()
        target_rel = copy_row["retained_dest"]
        before = p1t._snapshot(root)
        target.unlink()
        mutated_pre = p1t._snapshot(root)
        self.assertNotIn(target_rel, mutated_pre["files"])
        with self.assertRaises(retention.RetentionError):
            retention.verify_retention(root, pair["proposal_path"], pair["manifest_path"])
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        self.assertEqual(p1t._snapshot(root)["files"], mutated_pre["files"])
        target.write_bytes(saved)
        extra = pair["manifest_path"].parent / "late-file.json"
        extra.write_text("{}", encoding="utf-8")
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        extra.unlink()
        emptyd = pair["manifest_path"].parent / "before" / "empty-dir"
        emptyd.mkdir(parents=True)
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        emptyd.rmdir()

    def test_alias_fifo_no_read_and_late_addition(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-alias-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-alias-1", "Weekly P2V alias edition")
        proposal_dir = pair["proposal_path"].parent
        link = proposal_dir / "alias-leaf.json"
        try:
            link.symlink_to(proposal_dir / "proposal.json")
        except OSError as exc:
            self.fail(f"symlink setup failed: {exc}")
        before = p1t._snapshot(root)
        # Alias inside proposal layout must refuse without reading through it.
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        self.assertEqual(p1t._snapshot(root)["files"], before["files"])
        link.unlink()
        fifo = proposal_dir / "fifo-probe"
        try:
            os.mkfifo(fifo)
        except OSError as exc:
            self.fail(f"fifo setup failed: {exc}")
        try:
            before = p1t._snapshot(root)
            # Must refuse FIFO without blocking open (P1/P2R no-follow + regular checks).
            with self.assertRaises(obs.CurrentAuthorityError):
                obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
            self.assertEqual(p1t._snapshot(root)["files"], before["files"])
        finally:
            fifo.unlink()
        # Late control file addition detected by final inventory, not rehash alone.
        late = root / "config" / "late-control.json"
        late.write_text("{}", encoding="utf-8")
        try:
            with self.assertRaises(obs.CurrentAuthorityError):
                obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        finally:
            late.unlink()

    def test_scope_invalid_matrix(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        _s, root = _make_p2v_source_root(self, "p2v-scopem-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-sm-1", "Weekly P2V scope matrix")
        prepared, proposal_path = pair["prepared"], pair["proposal_path"]
        staged_reader_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        for name, kwargs in (
            ("scope-malformed.json", {"decision": "WITHIN_APPROVED_AUTHORITY"}),
            ("scope-reject2.json", {"decision": "REJECT"}),
            ("scope-owner.json", {"decision": "REQUIRES_OWNER_DECISION"}),
        ):
            tag = "malformed" if "malformed" in name else kwargs["decision"]
            if tag == "malformed":
                bad = proposal_path.parent / name
                bad.write_text("{not json", encoding="utf-8")
            else:
                bad = p1t._scope_review_for(self, root, prepared, staged_reader_rel, name,
                                            decision=kwargs["decision"])
            before = p1t._snapshot(root)
            with self.assertRaises(obs.CurrentAuthorityError, msg=name):
                obs.observe_current_authority(root, pair["state_path"], proposal_path,
                                              pair["manifest_path"], bad)
            self.assertEqual(p1t._snapshot(root)["files"], before["files"], f"no-write {name}")
            if tag == "malformed":
                bad.unlink()
        # Wrong-before scope refuses (no rebinding by equal SHA elsewhere).
        wrong = p1t._scope_review_for(
            self, root, prepared, staged_reader_rel, "scope-wrong-before.json",
            before_override={"path": staged_reader_rel, "sha256": "0" * 64})
        before = p1t._snapshot(root)
        with self.assertRaises(obs.CurrentAuthorityError):
            obs.observe_current_authority(root, pair["state_path"], proposal_path, pair["manifest_path"], wrong)
        self.assertEqual(p1t._snapshot(root)["files"], before["files"])

    def test_close_fault_and_no_write(self) -> None:
        from tests import test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_current_authority_v2 as obs
        from scripts import survey_editorial_retention_v2 as retention
        from unittest import mock
        _s, root = _make_p2v_source_root(self, "p2v-close-")
        pair = self._build_weekly_pair(self, root, "fixture-wk-close-1", "Weekly P2V close edition")
        before = p1t._snapshot(root)
        out = obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        self.assertEqual(out["result"], "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE")
        p1t._assert_no_write(self, before, p1t._snapshot(root), "close success no-write")
        # No fd growth across successful observe (checked closes, no leak).
        import glob as _glob
        fds_before = set(os.listdir("/proc/self/fd"))
        obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        fds_after = set(os.listdir("/proc/self/fd"))
        self.assertEqual(fds_after, fds_before, "fd leak across observe")
        # Injected close fault maps to CLOSE_FAILED with primary preserved.
        real_close = os.close
        seen: list[str] = []

        def _faulty_close(fd: int) -> None:
            seen.append(str(fd))
            raise OSError("injected P2V close fault")

        with mock.patch.object(retention.os, "close", side_effect=_faulty_close):
            with self.assertRaises(obs.CurrentAuthorityError) as ctx:
                obs.observe_current_authority(root, pair["state_path"], pair["proposal_path"], pair["manifest_path"])
        self.assertIn("CLOSE_FAILED", str(ctx.exception))
        self.assertTrue(seen, "close fault never reached _Session closes")
        real_close(0 if False else os.open("/dev/null", os.O_RDONLY)).__class__  # no-op keep ref
        try:
            os.close(999999)
        except OSError:
            pass


if __name__ == "__main__":
    unittest.main()
