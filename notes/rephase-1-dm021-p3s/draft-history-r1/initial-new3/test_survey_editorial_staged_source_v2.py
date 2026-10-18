#!/usr/bin/env python3
"""DM021-P3S staged-source tests (behavioral O1-O14, no old-suite transfer).

Independent meaningful fixture source (new3 BEFORE authority, .github
included). Real Longform recipe (helper._complete(helper._chain()) /
_state_path / _advance_to_validated_draft / _authored + narrative_sections
text delta), real Weekly recipe (_build_weekly_validated + cover/headline
delta), genuine R1 owner (committed non-emitted Python comment change +
actual refresh_mechanical_evidence in fixture-code subprocesses). Every
behavioral method calls the actual P3S writer/verifier (plus real P1/P2R/P2V
seams) and asserts result/error AND immediate no-write/exact owned deltas
BEFORE any repair. No mock-as-oracle, no no-write-after-repair, no
placeholder coverage. Fixture-code execution uses fresh subprocesses with
sanitized env (especially R1); parent-imported changed files are never used
as fixture authority.
"""
from __future__ import annotations

import json
import os
import shutil
import stat as _stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import survey_editorial_retention_v2 as retention
from scripts import survey_production_v2 as core
from scripts import survey_editorial_staged_source_v2 as staged
from tests import test_survey_editorial_correction_proposal_v2 as p1t
from tests import test_survey_editorial_current_authority_v2 as p2vt

_GIT_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
             "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX")

UNTRACKED_P3S_SOURCES = (
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_current_authority_v2.py",
    "scripts/survey_editorial_staged_source_v2.py",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/editorial-staged-source-manifest-v2.schema.json",
    "scripts/survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_editorial_current_authority_v2.py",
    "tests/test_survey_editorial_staged_source_v2.py",
)


def _run_git(root: Path, *args: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
        "GIT_AUTHOR_NAME": "Synthetic DM021-P3S Fixture", "GIT_AUTHOR_EMAIL": "p3s-fixture@example.invalid",
        "GIT_COMMITTER_NAME": "Synthetic DM021-P3S Fixture", "GIT_COMMITTER_EMAIL": "p3s-fixture@example.invalid",
    })
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=env)


def _make_p3s_source_root(testcase: unittest.TestCase, prefix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
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
    for rel in UNTRACKED_P3S_SOURCES:
        source = workspace / rel
        testcase.assertTrue(source.is_file(), f"untracked P3S source missing: {rel}")
        destination = root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        testcase.assertEqual(core.sha256_file(destination), core.sha256_file(source),
                             f"fixture copy drift: {rel}")
    for command in (
        ["init", "-q"],
        ["remote", "add", "origin", "https://example.invalid/dm021-p3s-fixture.git"],
        ["add", "-A"],
        ["-c", "user.name=Synthetic DM021-P3S Fixture",
         "-c", "user.email=p3s-fixture@example.invalid",
         "commit", "-q", "-m", "Synthetic isolated DM021-P3S source basis (changed P1+new3)"],
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
    out: dict[str, bytes] = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            full = Path(dirpath) / name
            rel = full.relative_to(root).as_posix()
            if "__pycache__" in Path(rel).parts:
                continue
            out[rel] = full.read_bytes()
    return out


def _assert_no_write(testcase: unittest.TestCase, before: dict, after: dict, label: str) -> None:
    testcase.assertEqual(set(after), set(before), f"{label}: file set changed")
    for rel, data in before.items():
        testcase.assertEqual(after[rel], data, f"{label}: bytes changed: {rel}")


def _assert_owned_delta_only(testcase: unittest.TestCase, before: dict, after: dict,
                             allowed_new: set[str], label: str) -> None:
    testcase.assertEqual(set(after) - set(before), allowed_new, f"{label}: unexpected new files")
    for rel, data in before.items():
        testcase.assertIn(rel, after, f"{label}: live file removed: {rel}")
        testcase.assertEqual(after[rel], data, f"{label}: live file changed: {rel}")


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


_P3S_R1_NONEMITTED_COMMENT_ANCHOR = "fixture R1 non-emitted refresh"
_P3S_R1_PYTHON_PROBE = "r1_probe_value = 1  # " + _P3S_R1_NONEMITTED_COMMENT_ANCHOR


def _commit_r1_nonemitted_comment(testcase: unittest.TestCase, root: Path) -> str:
    """Genuine R1 owner change: real committed non-emitted Python comment.

    Edits a Python-only comment line (never rendered into reader/TeX output),
    commits it, then the executor runs actual refresh_mechanical_evidence in
    fixture code. The reason string alone is not the change; the emitted
    TeX-comment path (_commit_derivation_only_change) is NOT used here.
    """
    probe = root / "scripts" / "survey_weekly_mechanical_refresh_v2.py"
    text = probe.read_text(encoding="utf-8")
    testcase.assertNotIn(_P3S_R1_NONEMITTED_COMMENT_ANCHOR, text)
    marker = '"""Execute one bounded mechanical receipt/Gate refresh.'
    testcase.assertIn(marker, text)
    probe.write_text(text.replace(marker, _P3S_R1_PYTHON_PROBE + "\n" + marker, 1),
                     encoding="utf-8")
    proc = _run_git(root, "add", "scripts/survey_weekly_mechanical_refresh_v2.py")
    testcase.assertEqual(proc.returncode, 0, proc.stderr)
    proc = _run_git(root, "-c", "user.name=Synthetic DM021-P3S Fixture",
                    "-c", "user.email=p3s-fixture@example.invalid",
                    "commit", "-q", "-m", "Fixture R1 non-emitted Python comment change")
    testcase.assertEqual(proc.returncode, 0, proc.stderr)
    return core.repository_commit_sha(root)


def _lf_prepare(testcase: unittest.TestCase, root: Path, workspace: Path,
                proposal_id: str) -> dict:
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    helper = p1t._new_longform_helper(testcase, root, workspace)
    chain = helper._complete(helper._chain())
    state_path = helper._state_path(chain)
    built = helper._advance_to_validated_draft(chain, state_path)
    testcase.assertEqual(core.load_json(state_path)["lifecycle_state"], "VALIDATED_DRAFT")
    authored = helper._authored(chain, helper.worker)
    authored["longform_revision"]["packages"][0]["narrative_sections"][0]["paragraphs"][0]["text"] += \
        " Revised fixture sentence within approved evidence."
    staged_authoring = p1t._stage_authoring_before_prepare(
        testcase, root, helper.source_root, proposal_id, authored)
    before = _snapshot(root)
    prepared = proposal_mod.prepare_proposal(root, state_path, staged_authoring, proposal_id,
                                             "Fixture longform prose correction.")
    _assert_no_write(testcase, before, _snapshot(root), "lf prepare")
    proposal_path = p1t._stage_reader_and_proposal(testcase, root, helper.source_root,
                                                   proposal_id, prepared)
    outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
    testcase.assertEqual(outcome["result"], "REVIEW_REQUIRED")
    return {"helper": helper, "chain": chain, "state_path": state_path, "built": built,
            "prepared": prepared, "proposal_path": proposal_path}


def _weekly_prepare(testcase: unittest.TestCase, root: Path, proposal_id: str) -> dict:
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    helper = p1t._new_weekly_helper(testcase, root)
    built = p1t._build_weekly_validated(testcase, helper)
    chain, state_path = built["chain"], built["state_path"]
    authored = core.load_json(chain["authored_path"])
    authored["cover"]["headline"] = "Weekly tested method, revised edition"
    staged_authoring = p1t._stage_authoring_before_prepare(
        testcase, root, helper.source_root, proposal_id, authored)
    prepared = proposal_mod.prepare_proposal(root, state_path, staged_authoring, proposal_id,
                                             "Fixture weekly envelope correction.")
    proposal_path = p1t._stage_reader_and_proposal(testcase, root, helper.source_root,
                                                   proposal_id, prepared)
    outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
    testcase.assertEqual(outcome["result"], "REVIEW_REQUIRED")
    return {"helper": helper, "chain": chain, "state_path": state_path, "built": built,
            "prepared": prepared, "proposal_path": proposal_path}


def _capture(testcase: unittest.TestCase, root: Path, state_path: Path, proposal_path: Path) -> Path:
    before = _snapshot(root)
    out = retention.capture_retention(root, state_path, proposal_path)
    testcase.assertEqual(out["result"], retention.RESULT_CAPTURED)
    manifest_path = root / out["manifest_path"]
    testcase.assertTrue(manifest_path.is_file())
    testcase.assertEqual(core.sha256_file(manifest_path), out["manifest_sha256"])
    vout = retention.verify_retention(root, proposal_path, manifest_path)
    testcase.assertEqual(vout["result"], retention.RESULT_VERIFIED)
    _assert_owned_delta_only(testcase, before, _snapshot(root),
                             {out["manifest_path"]} | {r["retained_dest"] for r in
                              core.load_json(manifest_path)["rows"]
                              if r["policy"] == "COPY_BEFORE_REPLACEMENT"},
                             "retention capture owned delta")
    return manifest_path


def _scope_for(testcase: unittest.TestCase, root: Path, prepared: dict,
               proposal_path: Path, name: str) -> Path:
    staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    return p1t._scope_review_for(testcase, root, prepared, staged_reader_rel, name)


class EditorialStagedSourceV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in _GIT_VARS:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override: {name}")
        self.workspace = Path(__file__).resolve().parents[1]

    def _materialize(self, root: Path, state_path: Path, proposal_path: Path,
                     manifest_path: Path, scope_path: Path) -> tuple[dict, Path]:
        from scripts import survey_editorial_current_authority_v2 as observer
        obs = observer.observe_current_authority(root, state_path, proposal_path,
                                                 manifest_path, scope_path)
        self.assertEqual(obs["result"], observer.RESULT_SCOPE_BOUND)
        before = _snapshot(root)
        result = staged.materialize_staged_source(root, state_path, proposal_path,
                                                  manifest_path, scope_path)
        self.assertEqual(result["result"], staged.RESULT_MATERIALIZED)
        staged_dir = root / proposal_path.parent.relative_to(root) / staged.STAGED_DIRNAME
        allowed = {str((staged_dir / name).relative_to(root).as_posix())
                   for name in (staged.MAIN_FILENAME, staged.BIBLIOGRAPHY_FILENAME,
                                staged.STYLE_FILENAME, staged.MANIFEST_FILENAME)}
        _assert_owned_delta_only(self, before, _snapshot(root), allowed, "materialize owned delta")
        staged_manifest = staged_dir / staged.MANIFEST_FILENAME
        self.assertTrue(staged_manifest.is_file())
        return result, staged_manifest

    def test_o1_longform_materialize_and_replay(self) -> None:
        """O1 healthy Longform staged set + independent replay (real prose delta)."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o1-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-1")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-1.json")
        result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        self.assertEqual(result["observed_head"], core.repository_commit_sha(root))
        manifest = core.load_json(staged_manifest)
        self.assertEqual(manifest["status"], "STAGED_ONLY")
        self.assertEqual(manifest["route"], "LONGFORM_GENERATED_V1")
        self.assertEqual(manifest["basis"], prep["prepared"]["proposal"]["basis"])
        self.assertEqual(set(manifest["outputs"]), {"main", "bibliography", "style"})
        self.assertEqual(len(manifest["code_deps"]), 37)
        self.assertEqual([d["path"] for d in manifest["code_deps"]],
                         sorted(d["path"] for d in manifest["code_deps"]))
        main_text = (staged_manifest.parent / "main.tex").read_text(encoding="utf-8")
        self.assertIn("Revised fixture sentence within approved evidence.", main_text)
        vout = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)

    def test_o2_weekly_materialize_and_replay(self) -> None:
        """O2 healthy Weekly staged set + independent replay (real envelope delta)."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o2-")
        prep = _weekly_prepare(self, root, "fixture-wk-p3s-1")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-2.json")
        _result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        manifest = core.load_json(staged_manifest)
        self.assertEqual(manifest["route"], "WEEKLY_GENERATED_V2")
        main_text = (staged_manifest.parent / "main.tex").read_text(encoding="utf-8")
        self.assertIn("Weekly tested method, revised edition", main_text)
        vout = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)

    def test_o3_coexistence_p1_refuse_p2r_p2v(self) -> None:
        """O3 P1 still refuses retained destination; P2R/P2V coexist (no TeX use)."""
        from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
        from scripts import survey_editorial_current_authority_v2 as observer
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o3-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-3")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-3.json")
        self._materialize(root, prep["state_path"], prep["proposal_path"],
                          manifest_path, scope_path)
        snap = _snapshot(root)
        with self.assertRaises(Exception):
            proposal_mod.validate_proposal(root, prep["state_path"], prep["proposal_path"])
        _assert_no_write(self, snap, _snapshot(root), "o3 P1 post-retention refusal")
        vout = retention.verify_retention(root, prep["proposal_path"], manifest_path)
        self.assertEqual(vout["result"], retention.RESULT_VERIFIED)
        obs = observer.observe_current_authority(root, prep["state_path"], prep["proposal_path"],
                                                 manifest_path, scope_path)
        self.assertEqual(obs["result"], observer.RESULT_SCOPE_BOUND)

    def test_o4_live_state_mutation_replay_ok_materializer_refuses(self) -> None:
        """O4 live-State drift: artifact replay VERIFIED, fresh writer refuses."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o4-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-4")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-4.json")
        self._materialize(root, prep["state_path"], prep["proposal_path"],
                          manifest_path, scope_path)
        staged_manifest = (prep["proposal_path"].parent / staged.STAGED_DIRNAME
                           / staged.MANIFEST_FILENAME)
        live_state = core.load_json(prep["state_path"])
        live_state["p3s_artifact_probe"] = "mutable non-KEEP live change"
        core.write_json(prep["state_path"], live_state)
        snap = _snapshot(root)
        vout = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)
        _assert_no_write(self, snap, _snapshot(root), "o4 replay after live-State drift")
        with self.assertRaises(staged.StagedSourceError):
            staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                              manifest_path, scope_path)

    def test_o5_artifact_only_head_independence(self) -> None:
        """O5 artifact-only commit keeps replay VERIFIED without HEAD comparison."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o5-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-5")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-5.json")
        result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        head_before = result["observed_head"]
        note = root / "sources" / "artifact-only-note.txt"
        note.write_text("artifact-only change outside KEEP/S2/refs\n", encoding="utf-8")
        proc = _run_git(root, "add", "sources/artifact-only-note.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P3S Fixture",
                        "-c", "user.email=p3s-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture artifact-only commit")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        head_after = core.repository_commit_sha(root)
        self.assertNotEqual(head_before, head_after)
        vout = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)

    def test_o6a_tool_drift_reaches_check(self) -> None:
        """O6a TOOL_DRIFT without earlier KEEP/schema failure (import-only dep)."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o6a-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-6a")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-6a.json")
        target = root / "scripts" / "survey_review_attention_v2.py"
        snap = _snapshot(root)
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n# Fixture TOOL_DRIFT probe (import-only dep).\n",
                          encoding="utf-8")
        try:
            snap_fault = _snapshot(root)
            with self.assertRaisesRegex(staged.StagedSourceError, "TOOL_DRIFT"):
                staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                                  manifest_path, scope_path)
            _assert_no_write(self, snap_fault, _snapshot(root), "o6a TOOL_DRIFT no-write")
        finally:
            target.write_text(text, encoding="utf-8")
        _assert_no_write(self, snap, _snapshot(root), "o6a restored")

    def test_o6b_keep_drift_preempts_honestly(self) -> None:
        """O6b KEEP-byte drift reports the earlier KEEP refusal, not TOOL_DRIFT."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o6b-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-6b")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-6b.json")
        manifest = core.load_json(manifest_path)
        keep = next(r for r in manifest["rows"] if r["policy"] == "KEEP_IMMUTABLE")
        kept = root / keep["retained_ref"]["path"]
        original = kept.read_bytes()
        snap = _snapshot(root)
        kept.write_bytes(original + b"\n")
        try:
            snap_fault = _snapshot(root)
            with self.assertRaisesRegex(staged.StagedSourceError,
                                        "PROFILE_DRIFT|INVALID_RETENTION|P2R_REFUSED|RETAINED"):
                staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                                  manifest_path, scope_path)
            _assert_no_write(self, snap_fault, _snapshot(root), "o6b KEEP drift no-write")
        finally:
            kept.write_bytes(original)
        _assert_no_write(self, snap, _snapshot(root), "o6b restored")

    def test_o7_scope_refusals(self) -> None:
        """O7 missing/ordinary/malformed/stale scope refuses pre-write with no-write."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o7-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-7")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-7.json")
        base = _snapshot(root)
        missing = scope_path.parent / "scope-missing.json"
        with self.assertRaises(staged.StagedSourceError):
            staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                              manifest_path, missing)
        _assert_no_write(self, base, _snapshot(root), "o7 missing scope")
        ordinary = p1t._scope_review_for(self, root, prep["prepared"],
                                         prep["prepared"]["proposal"]["proposed"]
                                         ["proposed_reader_ref"]["path"],
                                         "scope-ordinary.json",
                                         decision="NEEDS_SCOPE_DETAIL")
        with self.assertRaisesRegex(staged.StagedSourceError, "SCOPE_"):
            staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                              manifest_path, ordinary)
        _assert_no_write(self, base, _snapshot(root), "o7 ordinary scope")
        malformed = scope_path.parent / "scope-malformed.json"
        malformed.write_bytes(b"{not json", encoding="utf-8")
        try:
            with self.assertRaisesRegex(staged.StagedSourceError, "SCOPE_|PIN_"):
                staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                                  manifest_path, malformed)
            _assert_no_write(self, base, _snapshot(root), "o7 malformed scope")
        finally:
            malformed.unlink()
        _assert_no_write(self, base, _snapshot(root), "o7 restored")

    def test_o8_path_ref_schema_inventory_tamper(self) -> None:
        """O8 wrong-path refs / bad schema-shape / inventory tamper refuse read-only."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o8-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-8")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-8.json")
        result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        staged_dir = staged_manifest.parent
        (staged_dir / "extra-aux-file.txt").write_bytes(b"aux outside closed set\n")
        try:
            snap = _snapshot(root)
            with self.assertRaisesRegex(staged.StagedSourceError, "STAGED_SET_MISMATCH"):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
            _assert_no_write(self, snap, _snapshot(root), "o8 extra-file inventory")
        finally:
            (staged_dir / "extra-aux-file.txt").unlink()
        dup = staged_dir / "dup-manifest.json"
        dup.write_bytes(b'{"a": 1, "a": 2}', encoding="utf-8")
        try:
            with self.assertRaises(staged.StagedSourceError):
                staged.verify_staged_source(root, prep["proposal_path"], dup)
        finally:
            dup.unlink()

    def test_o9_alias_fifo_no_read(self) -> None:
        """O9 alias/FIFO inputs refuse without read or hang (timeout-guarded)."""
        import concurrent.futures
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o9-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-9")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-9.json")
        base = _snapshot(root)
        reader_rel = prep["prepared"]["proposal"]["proposed"]["proposed_reader_ref"]["path"]
        alias = prep["proposal_path"].parent / "alias-reader.json"
        try:
            alias.symlink_to(Path(reader_rel).name)
            with self.assertRaisesRegex(staged.StagedSourceError, "PATH_ALIAS"):
                staged.materialize_staged_source(
                    root, prep["state_path"], prep["proposal_path"], manifest_path, alias)
        finally:
            if alias.is_symlink() or alias.exists():
                alias.unlink()
        _assert_no_write(self, base, _snapshot(root), "o9 alias no-read")
        fifo = scope_path.parent / "scope-fifo.json"
        os.mkfifo(fifo)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(staged.materialize_staged_source, root,
                                     prep["state_path"], prep["proposal_path"],
                                     manifest_path, fifo)
                try:
                    future.result(timeout=60)
                    self.fail("FIFO scope path must refuse, not succeed")
                except staged.StagedSourceError:
                    pass
                except concurrent.futures.TimeoutError:
                    self.fail("FIFO scope open blocked beyond 60s (no-read guard missing)")
        finally:
            fifo.unlink()
        _assert_no_write(self, base, _snapshot(root), "o9 fifo no-read")

    def test_o10_same_inode_vs_new_inode(self) -> None:
        """O10 same-inode edit vs new-inode same-byte swap are distinct refusals."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o10-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-10")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-10.json")
        _result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        main_tex = staged_manifest.parent / "main.tex"
        original = main_tex.read_bytes()
        with main_tex.open("r+b") as handle:
            handle.seek(0)
            handle.write(b"%")
            handle.flush()
        try:
            snap = _snapshot(root)
            with self.assertRaises(staged.StagedSourceError):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
            _assert_no_write(self, snap, _snapshot(root), "o10 same-inode edit")
        finally:
            main_tex.write_bytes(original)
        swapped = main_tex.parent / "main.tex.swap"
        swapped.write_bytes(original)
        os.replace(swapped, main_tex)
        try:
            snap = _snapshot(root)
            with self.assertRaisesRegex(staged.StagedSourceError,
                                        "FILE_REPLACED|STABILITY_VIOLATION|OUTPUT_DRIFT|REPLAY_"):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
            _assert_no_write(self, snap, _snapshot(root), "o10 new-inode swap")
        finally:
            main_tex.write_bytes(original)

    def test_o11_root_file_replacement_and_midcall_drift(self) -> None:
        """O11 pre-existing root refuses; staged output swap after readback refuses."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o11-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-11")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-11.json")
        staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                      + "/" + staged.STAGED_DIRNAME)
        (root / staged_rel).mkdir(parents=True)
        try:
            snap = _snapshot(root)
            with self.assertRaisesRegex(staged.StagedSourceError, "STAGED_ROOT_EXISTS"):
                staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                                  manifest_path, scope_path)
            _assert_no_write(self, snap, _snapshot(root), "o11 pre-existing root")
        finally:
            (root / staged_rel).rmdir()
        _result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        bib = staged_manifest.parent / "references.bib"
        original = bib.read_bytes()
        swapped = bib.parent / "references.bib.swap"
        swapped.write_bytes(original + b"% appended post-readback drift\n")
        os.replace(swapped, bib)
        try:
            snap = _snapshot(root)
            with self.assertRaises(staged.StagedSourceError):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
            _assert_no_write(self, snap, _snapshot(root), "o11 post-readback drift")
        finally:
            bib.write_bytes(original)

    def test_o12_partial_manifest_and_zeroed_output(self) -> None:
        """O12 truncated manifest / extra empty dir / zeroed output refuse on verify."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12.json")
        _result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        original_manifest = staged_manifest.read_bytes()
        staged_manifest.write_bytes(original_manifest[: len(original_manifest) // 2])
        try:
            snap = _snapshot(root)
            with self.assertRaises(staged.StagedSourceError):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
            _assert_no_write(self, snap, _snapshot(root), "o12 truncated manifest")
        finally:
            staged_manifest.write_bytes(original_manifest)
        (staged_manifest.parent / "empty-subdir").mkdir()
        try:
            with self.assertRaisesRegex(staged.StagedSourceError, "STAGED_SET_MISMATCH"):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        finally:
            (staged_manifest.parent / "empty-subdir").rmdir()
        main_tex = staged_manifest.parent / "main.tex"
        original_main = main_tex.read_bytes()
        main_tex.write_bytes(b"")
        try:
            snap = _snapshot(root)
            with self.assertRaises(staged.StagedSourceError):
                staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
            _assert_no_write(self, snap, _snapshot(root), "o12 zeroed output")
        finally:
            main_tex.write_bytes(original_main)

    def test_o13_immediate_no_write_before_repair(self) -> None:
        """O13 every refusal proves no-write with the fault still present."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o13-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-13")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-13.json")
        base = _snapshot(root)
        target = root / "scripts" / "survey_completeness_v2.py"
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n# Fixture o13 TOOL_DRIFT probe.\n", encoding="utf-8")
        try:
            snap_fault = _snapshot(root)
            with self.assertRaisesRegex(staged.StagedSourceError, "TOOL_DRIFT"):
                staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                                  manifest_path, scope_path)
            _assert_no_write(self, snap_fault, _snapshot(root), "o13 fault-present no-write")
        finally:
            target.write_text(text, encoding="utf-8")
        _assert_no_write(self, base, _snapshot(root), "o13 restored")
        missing = scope_path.parent / "scope-absent-o13.json"
        with self.assertRaises(staged.StagedSourceError):
            staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                              manifest_path, missing)
        _assert_no_write(self, base, _snapshot(root), "o13 missing-scope no-write")

    def test_o14_byte_equal_existing_root_refuses(self) -> None:
        """O14 byte-equal pre-existing staged set still refuses writer takeover."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o14-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-14")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-14.json")
        _result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        vout = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)
        snap = _snapshot(root)
        with self.assertRaisesRegex(staged.StagedSourceError, "STAGED_ROOT_EXISTS"):
            staged.materialize_staged_source(root, prep["state_path"], prep["proposal_path"],
                                              manifest_path, scope_path)
        _assert_no_write(self, snap, _snapshot(root), "o14 byte-equal no-takeover")
        vout2 = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout2["result"], staged.RESULT_VERIFIED)

    def test_r1_genuine_owner_binds_materialization(self) -> None:
        """R1 genuine owner: committed non-emitted Python comment + fixture-code refresh."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-r1-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        head_before = core.repository_commit_sha(root)
        _commit_r1_nonemitted_comment(self, root)
        self.assertNotEqual(core.repository_commit_sha(root), head_before)
        out = _run_fixture_code(self, root, p2vt._R1_REFRESH_SCRIPT, [str(root), str(state_path)])
        self.assertTrue(out.strip(), "R1 fixture refresh produced no output")
        prep = _weekly_prepare(self, root, "fixture-wk-p3s-r1")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-r1.json")
        result, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        self.assertEqual(result["result"], staged.RESULT_MATERIALIZED)
        vout = staged.verify_staged_source(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)


if __name__ == "__main__":
    unittest.main()
        

