#!/usr/bin/env python3
"""DM021-P3S staged-source tests (behavioral O1-O14 + R1, no old-suite transfer).

Independent meaningful fixture source (new3 BEFORE authority, .github
included). Real Longform recipe (helper._complete(helper._chain()) /
_state_path / _advance_to_validated_draft / _authored + narrative_sections
text delta), real Weekly recipe (_build_weekly_validated + cover/headline
delta), genuine R1 owner (committed non-emitted Python comment + actual
refresh_mechanical_evidence in fixture-code subprocesses, SAME chain into
materialization with basis binding). Public P3S writer/verifier operations
run in fresh fixture-code subprocesses (fixture root code, never the
candidate checkout); assertions use exact typed codes/phases. Raw-safe
lstat snapshots (dirs/identities/types/walk errors, no alias-follow, no
FIFO reads) with immediate fault-present comparison. During-write faults
use scoped wrappers around ACTUAL os operations inside the fixture
subprocess (not mock-replacement of authority/P2V/replay). No mock-as-oracle,
no no-write-after-repair, no placeholder coverage.
"""
from __future__ import annotations

import ast as _ast
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
        source = workspace / relative
        # Deliberate materialized-source handling: every ls-files entry must
        # exist in this database (no sparse assumption, no network fetch).
        testcase.assertTrue(source.is_file(), f"tracked P3S source missing: {relative}")
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
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
    """Raw-safe inventory: lstat only, no alias-follow, no nonregular reads.

    Regular files record bytes; dirs record (dev,ino,mode); symlinks record
    target; FIFOs/specials record kind WITHOUT opening (no block). Walk
    errors fail loudly with the path. `__pycache__` excluded by policy.
    Byte equality alone never proves the file+directory write window, so
    dirs/identities/types are part of every comparison.
    """
    out: dict = {}
    errors: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False,
                                                onerror=lambda e: errors.append(str(e))):
        for name in dirnames:
            full = Path(dirpath) / name
            rel = full.relative_to(root).as_posix()
            if "__pycache__" in Path(rel).parts:
                continue
            try:
                st = os.lstat(full)
            except OSError as exc:
                errors.append(f"{rel}: {exc}")
                continue
            if _stat.S_ISLNK(st.st_mode):
                try:
                    out[rel] = ("symlink", os.readlink(full))
                except OSError as exc:
                    errors.append(f"{rel}: {exc}")
            elif _stat.S_ISDIR(st.st_mode):
                out[rel] = ("dir", st.st_dev, st.st_ino, _stat.S_IMODE(st.st_mode))
            else:
                out[rel] = ("other", oct(st.st_mode))
        for name in filenames:
            full = Path(dirpath) / name
            rel = full.relative_to(root).as_posix()
            if "__pycache__" in Path(rel).parts:
                continue
            try:
                st = os.lstat(full)
            except OSError as exc:
                errors.append(f"{rel}: {exc}")
                continue
            if _stat.S_ISREG(st.st_mode) and not full.is_symlink():
                try:
                    out[rel] = ("file", full.read_bytes(), st.st_size, st.st_dev, st.st_ino)
                except OSError as exc:
                    errors.append(f"{rel}: {exc}")
            elif _stat.S_ISLNK(st.st_mode):
                try:
                    out[rel] = ("symlink", os.readlink(full))
                except OSError as exc:
                    errors.append(f"{rel}: {exc}")
            elif _stat.S_ISFIFO(st.st_mode):
                out[rel] = ("fifo",)
            else:
                out[rel] = ("other", oct(st.st_mode))
    if errors:
        raise AssertionError(f"snapshot walk errors (fail-closed, no silent skip): {errors}")
    return out


def _assert_no_write(testcase: unittest.TestCase, before: dict, after: dict, label: str) -> None:
    testcase.assertEqual(set(after), set(before), f"{label}: entry set changed")
    for rel, data in before.items():
        testcase.assertEqual(after.get(rel), data, f"{label}: entry changed: {rel}")


def _assert_no_write_except(testcase: unittest.TestCase, before: dict, after: dict,
                            allowed_new: set[str], allowed_changed: set[str],
                            label: str) -> None:
    """Immediate comparison WITH the injected fault present (before repair).

    Only explicitly listed new/changed entries may differ; everything else
    (files, dirs, identities, types) must be byte-identical, including the
    fault artifacts themselves.
    """
    testcase.assertEqual(set(after) - set(before), allowed_new, f"{label}: unexpected new entries")
    for rel, data in before.items():
        if rel in allowed_changed:
            testcase.assertIn(rel, after, f"{label}: allowed-changed entry removed: {rel}")
            continue
        testcase.assertIn(rel, after, f"{label}: entry removed: {rel}")
        testcase.assertEqual(after[rel], data, f"{label}: entry changed: {rel}")


def _assert_owned_delta_only(testcase: unittest.TestCase, before: dict, after: dict,
                             allowed_new: set[str], label: str) -> None:
    _assert_no_write_except(testcase, before, after, allowed_new, set(), label)


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


_P3S_MATERIALIZE_SCRIPT = """
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2]); proposal_path = Path(sys.argv[3])
manifest_path = Path(sys.argv[4]); scope_path = Path(sys.argv[5])
from scripts import survey_editorial_staged_source_v2 as staged
try:
    out = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
    print(json.dumps({"ok": True, "result": out["result"],
                      "staged": out["staged_manifest_ref"]["path"],
                      "digest": out["manifest_digest"], "head": out["observed_head"]}))
except Exception as exc:
    owned = getattr(exc, "owned", {})
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
                      "owned_files": len(owned.get("owned_files", [])) if isinstance(owned, dict) else 0}))
"""

_P3S_VERIFY_SCRIPT = """
import json, sys
from pathlib import Path
root = Path(sys.argv[1]); proposal_path = Path(sys.argv[2]); staged_path = Path(sys.argv[3])
from scripts import survey_editorial_staged_source_v2 as staged
try:
    out = staged.verify_staged_source(root, proposal_path, staged_path)
    print(json.dumps({"ok": True, "result": out["result"],
                      "reader": out["measured"]["proposed_reader_sha256"]}))
except Exception as exc:
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000]}))
"""

# During-write fault injection: scoped wrappers around ACTUAL os operations
# inside the fixture subprocess (never mock-replacement of authority/P2V/
# replay). The fault fires once on a targeted real call; the API underneath
# is genuine. Result (including owned-file counts) is printed AFTER restoring
# the real operations so the outcome record itself is reliable.
_P3S_FAULT_SCRIPT = """
import json, os, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2]); proposal_path = Path(sys.argv[3])
manifest_path = Path(sys.argv[4]); scope_path = Path(sys.argv[5])
fault = sys.argv[6]
from scripts import survey_editorial_staged_source_v2 as staged
real_write, real_fsync, real_close = os.write, os.fsync, os.close
real_fstat, real_mkdir, real_open = os.fstat, os.mkdir, os.open
created = []
fired = {"n": 0}
def _track_open(path, flags, *a, **k):
    fd = real_open(path, flags, *a, **k)
    if flags & os.O_CREAT:
        created.append(fd)
    return fd
def _write_once(fd, data):
    if fault in ("zero-write", "write-fail") and fd in created and fired["n"] == 0:
        fired["n"] += 1
        if fault == "zero-write":
            return 0
        raise OSError(5, "injected write failure")
    if fault == "manifest-write-fail" and fd in created and len(created) >= 4 and fd == created[3]:
        raise OSError(5, "injected manifest write failure")
    return real_write(fd, data)
def _fsync_once(fd):
    if fault == "fsync-fail" and fd in created and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected fsync failure")
    return real_fsync(fd)
def _close_once(fd):
    if fault in ("close-fail", "manifest-close-fail") and fd in created:
        if fault == "close-fail" and fired["n"] == 0 and fd == created[0]:
            fired["n"] += 1
            raise OSError(5, "injected close failure")
        if fault == "manifest-close-fail" and len(created) >= 4 and fd == created[3] and fired["n"] == 0:
            fired["n"] += 1
            raise OSError(5, "injected manifest close failure")
    return real_close(fd)
def _fstat_once(fd):
    st = real_fstat(fd)
    if fault == "fstat-fake" and fd in created and fired["n"] == 0:
        fired["n"] += 1
        return os.stat_result((st.st_mode, st.st_ino + 7, st.st_dev, st.st_nlink,
                               st.st_uid, st.st_gid, st.st_size, st.st_atime,
                               st.st_mtime, st.st_ctime))
    if fault == "fstat-fail" and fd in created and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected fstat failure")
    return st
def _mkdir_once(path, *a, **k):
    if fault == "mkdir-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(13, "injected mkdir failure")
    return real_mkdir(path, *a, **k)
_real_read_bytes = Path.read_bytes
def _read_bytes_once(self):
    data = _real_read_bytes(self)
    if fault == "drift-reader" and self.name == "reader-surface-input-v2.json" and fired["n"] == 0:
        fired["n"] += 1
        with open(self, "ab") as handle:
            handle.write(b"\n% injected mid-call drift\n")
    return data
if fault == "drift-reader":
    Path.read_bytes = _read_bytes_once
os.open, os.write, os.fsync, os.close, os.fstat, os.mkdir = (
    _track_open, _write_once, _fsync_once, _close_once, _fstat_once, _mkdir_once)
    outcome = {"ok": True, "result": "PENDING"}
    try:
        out = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
        outcome = {"ok": True, "result": out["result"]}
    except Exception as exc:
        owned = getattr(exc, "owned", {})
        outcome = {"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
                   "owned_files": len(owned.get("owned_files", [])) if isinstance(owned, dict) else 0}
    finally:
        os.write, os.fsync, os.close, os.fstat, os.mkdir, os.open = (
            real_write, real_fsync, real_close, real_fstat, real_mkdir, real_open)
        if fault == "drift-reader":
            Path.read_bytes = _real_read_bytes
    print(json.dumps(outcome))
"""


def _run_p3s_fixture(testcase: unittest.TestCase, root: Path, script: str,
                     args: list[str], timeout_s: int = 300) -> dict:
    """Run a P3S public operation in a fresh fixture-code subprocess (killable).

    The fixture root's OWN committed code executes (cwd=root, no parent-code
    import). Returns the parsed outcome dict; timeouts kill the process group
    remnant and save the timeout as an explicit outcome (never a hang).
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1"})
    try:
        proc = subprocess.run([sys.executable, "-c", script, *args], cwd=root,
                              capture_output=True, text=True, timeout=timeout_s, env=env)
    except subprocess.TimeoutExpired as exc:
        return {"ok": False, "timeout": True,
                "stdout": (exc.stdout or b"").decode("utf-8", "replace")[-1000:] if exc.stdout else "",
                "stderr": (exc.stderr or b"").decode("utf-8", "replace")[-1000:] if exc.stderr else ""}
    testcase.assertEqual(proc.returncode, 0,
                         f"P3S fixture step crashed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr[-4000:]}")
    lines = [line for line in proc.stdout.splitlines() if line.strip().startswith("{")]
    testcase.assertTrue(lines, f"P3S fixture printed no JSON outcome:\n{proc.stdout[-2000:]}")
    return json.loads(lines[-1])


_P3S_R1_NONEMITTED_COMMENT_ANCHOR = "fixture R1 non-emitted Python comment"


def _commit_r1_nonemitted_comment(testcase: unittest.TestCase, root: Path) -> str:
    """Genuine R1 owner change: a real committed PURE Python comment.

    Inserts one comment-only line (column 0, no code, no docstring edit) above
    `refresh_mechanical_evidence`; AST dumps before/after must be identical,
    proving zero semantic change. The emitted TeX-comment path
    (`_commit_derivation_only_change`) is NOT used here.
    """
    probe = root / "scripts" / "survey_weekly_mechanical_refresh_v2.py"
    text = probe.read_text(encoding="utf-8")
    testcase.assertNotIn(_P3S_R1_NONEMITTED_COMMENT_ANCHOR, text)
    before = _ast.dump(_ast.parse(text))
    lines = text.splitlines(keepends=True)
    targets = [i for i, line in enumerate(lines)
               if line.startswith("def refresh_mechanical_evidence(")]
    testcase.assertEqual(len(targets), 1, "R1 owner def must appear exactly once")
    lines.insert(targets[0], "# " + _P3S_R1_NONEMITTED_COMMENT_ANCHOR + "\n")
    probe.write_text("".join(lines), encoding="utf-8")
    after = _ast.dump(_ast.parse(probe.read_text(encoding="utf-8")))
    testcase.assertEqual(before, after, "R1 comment insertion changed semantics")
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


def _weekly_prepare_from(testcase: unittest.TestCase, root: Path, helper,
                         built: dict, proposal_id: str) -> dict:
    """Weekly prepare/validate on an EXISTING helper+built chain (R1 rebind)."""
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
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


def _weekly_prepare(testcase: unittest.TestCase, root: Path, proposal_id: str) -> dict:
    helper = p1t._new_weekly_helper(testcase, root)
    built = p1t._build_weekly_validated(testcase, helper)
    return _weekly_prepare_from(testcase, root, helper, built, proposal_id)


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
        """Run the PUBLIC writer in a fresh fixture-code subprocess (R1-4).

        The fixture root's own committed code executes; this helper never
        imports the candidate checkout for behavior. No outer P2V here (the
        writer performs its own two fresh observations; O3 asserts
        coexistence separately).
        """
        before = _snapshot(root)
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(state_path), str(proposal_path), str(manifest_path), str(scope_path)])
        self.assertTrue(outcome.get("ok"), f"materialize refused: {outcome}")
        self.assertEqual(outcome.get("result"), staged.RESULT_MATERIALIZED)
        staged_dir = proposal_path.parent / staged.STAGED_DIRNAME
        allowed = {str((staged_dir / name).relative_to(root).as_posix())
                   for name in (staged.MAIN_FILENAME, staged.BIBLIOGRAPHY_FILENAME,
                                staged.STYLE_FILENAME, staged.MANIFEST_FILENAME)}
        _assert_owned_delta_only(self, before, _snapshot(root), allowed, "materialize owned delta")
        staged_manifest = staged_dir / staged.MANIFEST_FILENAME
        self.assertTrue(staged_manifest.is_file())
        return outcome, staged_manifest

    def _verify(self, root: Path, proposal_path: Path, staged_manifest: Path) -> dict:
        """Run the PUBLIC verifier in a fresh fixture-code subprocess."""
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(proposal_path), str(staged_manifest)])
        self.assertTrue(outcome.get("ok"), f"verify refused: {outcome}")
        self.assertEqual(outcome.get("result"), staged.RESULT_VERIFIED)
        return outcome

    def _retamper_manifest(self, staged_manifest: Path, mutate) -> None:
        """Apply a semantic tamper then recompute digest+canonical bytes.

        Recomputing AFTER the tamper (R4) ensures refusal comes from the
        targeted semantic check, not an earlier digest mismatch.
        """
        manifest = core.load_json(staged_manifest)
        mutate(manifest)
        manifest["manifest_digest"] = core.sha256_object(
            {k: v for k, v in manifest.items() if k != "manifest_digest"})
        staged_manifest.write_bytes(core.json_bytes(
            {k: manifest[k] for k in sorted(manifest)}))

    def test_o1_longform_materialize_and_replay(self) -> None:
        """O1 healthy Longform staged set + independent replay (real prose delta)."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o1-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-1")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-1.json")
        outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        self.assertEqual(outcome["head"], core.repository_commit_sha(root))
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
        vout = self._verify(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["reader"],
                         manifest["proposed"]["proposed_reader_canonical_sha256"])

    def test_o2_weekly_materialize_and_replay(self) -> None:
        """O2 healthy Weekly staged set + independent replay (real envelope delta)."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o2-")
        prep = _weekly_prepare(self, root, "fixture-wk-p3s-1")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-2.json")
        _outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        manifest = core.load_json(staged_manifest)
        self.assertEqual(manifest["route"], "WEEKLY_GENERATED_V2")
        main_text = (staged_manifest.parent / "main.tex").read_text(encoding="utf-8")
        self.assertIn("Weekly tested method, revised edition", main_text)
        self._verify(root, prep["proposal_path"], staged_manifest)

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
        with self.assertRaisesRegex(proposal_mod.ProposalError, "RETENTION_DEST_CONFLICT"):
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
        self._verify(root, prep["proposal_path"], staged_manifest)
        _assert_no_write(self, snap, _snapshot(root), "o4 replay after live-State drift")
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(scope_path)])
        self.assertFalse(outcome.get("ok"), "stale-basis writer must refuse")
        self.assertIn("OBSERVER_REFUSED", outcome.get("error", ""))

    def test_o5_artifact_only_head_independence(self) -> None:
        """O5 artifact-only commit keeps replay VERIFIED without HEAD comparison."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o5-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-5")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-5.json")
        outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        head_before = outcome["head"]
        note = root / "sources" / "artifact-only-note.txt"
        note.write_text("artifact-only change outside KEEP/S2/refs\n", encoding="utf-8")
        proc = _run_git(root, "add", "sources/artifact-only-note.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P3S Fixture",
                        "-c", "user.email=p3s-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture artifact-only commit")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotEqual(core.repository_commit_sha(root), head_before)
        self._verify(root, prep["proposal_path"], staged_manifest)

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
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)])
            self.assertFalse(outcome.get("ok"), "TOOL_DRIFT case must refuse")
            self.assertIn("TOOL_DRIFT", outcome.get("error", ""))
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
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)])
            self.assertFalse(outcome.get("ok"), "KEEP drift must refuse")
            self.assertRegex(outcome.get("error", ""),
                             "PROFILE_DRIFT|INVALID_RETENTION|P2R_REFUSED|RETAINED|OBSERVER_REFUSED")
            self.assertNotIn("TOOL_DRIFT", outcome.get("error", ""))
            _assert_no_write(self, snap_fault, _snapshot(root), "o6b KEEP drift no-write")
        finally:
            kept.write_bytes(original)
        _assert_no_write(self, snap, _snapshot(root), "o6b restored")

    def test_o7_scope_refusals(self) -> None:
        """O7 missing/ordinary/malformed/stale-upstream scope refuses pre-write."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o7-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-7")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-7.json")
        base = _snapshot(root)
        missing = scope_path.parent / "scope-missing.json"
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(missing)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("SCOPE_", outcome.get("error", ""))
        _assert_no_write(self, base, _snapshot(root), "o7 missing scope")
        ordinary = p1t._scope_review_for(
            self, root, prep["prepared"],
            prep["prepared"]["proposal"]["proposed"]["proposed_reader_ref"]["path"],
            "scope-ordinary.json", decision="NEEDS_SCOPE_DETAIL")
        snap_ordinary = _snapshot(root)
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(ordinary)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("SCOPE_", outcome.get("error", ""))
        _assert_no_write(self, snap_ordinary, _snapshot(root), "o7 ordinary scope")
        malformed = scope_path.parent / "scope-malformed.json"
        malformed.write_bytes(b"{not json")
        try:
            snap_malformed = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(malformed)])
            self.assertFalse(outcome.get("ok"))
            self.assertRegex(outcome.get("error", ""), "SCOPE_|PIN_")
            _assert_no_write(self, snap_malformed, _snapshot(root), "o7 malformed scope")
        finally:
            malformed.unlink()
        _assert_no_write(self, base, _snapshot(root), "o7 restored")
        stale = p1t._scope_review_for(
            self, root, prep["prepared"],
            prep["prepared"]["proposal"]["proposed"]["proposed_reader_ref"]["path"],
            "scope-stale.json", upstream_override="0" * 64)
        snap_stale = _snapshot(root)
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(stale)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("SCOPE_STALE_UPSTREAM", outcome.get("error", ""))
        _assert_no_write(self, snap_stale, _snapshot(root), "o7 stale upstream")

    def test_o8_path_ref_schema_inventory_tamper(self) -> None:
        """O8 path/ref/schema/inventory tamper refuses read-only with no-write."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o8-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-8")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-8.json")
        _outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        staged_dir = staged_manifest.parent
        (staged_dir / "extra-aux-file.txt").write_text("aux outside closed set\n", encoding="utf-8")
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("STAGED_SET_MISMATCH", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o8 extra-file inventory")
        finally:
            (staged_dir / "extra-aux-file.txt").unlink()
        dup = staged_dir / "dup-manifest.json"
        dup.write_bytes(b'{"a": 1, "a": 2}')
        try:
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(dup)])
            self.assertFalse(outcome.get("ok"), "duplicate-key manifest must refuse")
        finally:
            dup.unlink()
        self._retamper_manifest(
            staged_manifest,
            lambda m: m["outputs"].__setitem__(
                "main", dict(m["outputs"]["main"], path="elsewhere/main.tex")))
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(prep["proposal_path"]), str(staged_manifest)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("OUTPUT_PATH_MISMATCH", outcome.get("error", ""))
        self._retamper_manifest(
            staged_manifest, lambda m: m.update({"extra_unknown_field": 1}))
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(prep["proposal_path"]), str(staged_manifest)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("SCHEMA_INVALID", outcome.get("error", ""))
        def _swap_deps(manifest):
            deps = manifest["code_deps"]
            deps[0], deps[1] = deps[1], deps[0]
        self._retamper_manifest(staged_manifest, _swap_deps)
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(prep["proposal_path"]), str(staged_manifest)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("CODE_DEPS_MISMATCH", outcome.get("error", ""))

    def test_o9_alias_fifo_no_read(self) -> None:
        """O9 alias/FIFO staged-reader + scope + ancestor refuse without read/hang."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o9-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-9")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-9.json")
        base = _snapshot(root)
        reader_rel = prep["prepared"]["proposal"]["proposed"]["proposed_reader_ref"]["path"]
        reader_abs = root / reader_rel
        reader_bytes = reader_abs.read_bytes()
        reader_abs.unlink()
        alias = prep["proposal_path"].parent / "reader-surface-input-v2.json"
        try:
            alias.symlink_to(Path("reader-bytes-copy.json").name)
            (prep["proposal_path"].parent / "reader-bytes-copy.json").write_bytes(reader_bytes)
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("PATH_ALIAS", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o9 alias reader no-read")
        finally:
            if alias.is_symlink() or alias.exists():
                alias.unlink()
            copy = prep["proposal_path"].parent / "reader-bytes-copy.json"
            if copy.exists():
                copy.unlink()
            if not reader_abs.exists():
                reader_abs.write_bytes(reader_bytes)
        _assert_no_write(self, base, _snapshot(root), "o9 alias restored")
        fifo = prep["proposal_path"].parent / "reader-fifo.json"
        os.mkfifo(fifo)
        backup = reader_abs.read_bytes()
        reader_abs.unlink()
        os.mkfifo(reader_abs)
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)], timeout_s=120)
            self.assertFalse(outcome.get("ok"), "FIFO staged reader must refuse, not hang")
            self.assertNotIn("timeout", json.dumps(outcome),
                             f"FIFO case blocked instead of refusing: {outcome}")
            self.assertRegex(outcome.get("error", ""),
                             "PATH_NOT_REGULAR|PATH_UNREADABLE|PATH_ALIAS")
            _assert_no_write(self, snap, _snapshot(root), "o9 fifo reader no-read")
        finally:
            try:
                os.unlink(reader_abs)
            except OSError:
                pass
            reader_abs.write_bytes(backup)
            fifo.unlink()
        _assert_no_write(self, base, _snapshot(root), "o9 fifo restored")
        realdir = scope_path.parent / "scope-realdir"
        realdir.mkdir()
        (realdir / "scope.json").write_bytes(scope_path.read_bytes())
        linkdir = scope_path.parent / "scope-linkdir"
        try:
            linkdir.symlink_to(realdir.name)
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(linkdir / "scope.json")])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("PATH_ALIAS", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o9 ancestor alias no-read")
        finally:
            linkdir.unlink()
            shutil.rmtree(realdir)
        _assert_no_write(self, base, _snapshot(root), "o9 ancestor restored")

    def test_o10_same_inode_vs_new_inode(self) -> None:
        """O10 same-inode edit refuses; same-byte/new-inode verifies (distinct).

        The read-only verifier is byte-consistency only: a same-inode content
        change refuses via replay mismatch, while a different-inode same-byte
        replacement still verifies (no owned-identity oracle in replay).
        Writer FINAL holds the identity oracle for the materialization call.
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o10-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-10")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-10.json")
        self._materialize(root, prep["state_path"], prep["proposal_path"],
                          manifest_path, scope_path)
        staged_manifest = (prep["proposal_path"].parent / staged.STAGED_DIRNAME
                           / staged.MANIFEST_FILENAME)
        main_tex = staged_manifest.parent / "main.tex"
        original = main_tex.read_bytes()
        with main_tex.open("r+b") as handle:
            handle.seek(0)
            handle.write(b"%")
            handle.flush()
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("REPLAY_MISMATCH", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o10 same-inode edit")
        finally:
            main_tex.write_bytes(original)
        swapped = main_tex.parent / "main.tex.swap"
        swapped.write_bytes(original)
        os.replace(swapped, main_tex)
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertTrue(outcome.get("ok"),
                            f"same-byte/new-inode replacement must still verify: {outcome}")
            self.assertEqual(outcome.get("result"), staged.RESULT_VERIFIED)
            _assert_no_write(self, snap, _snapshot(root), "o10 new-inode same-byte")
        finally:
            main_tex.write_bytes(original)

    def test_o11_root_preexisting_and_postreadback_drift(self) -> None:
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
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("STAGED_ROOT_EXISTS", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o11 pre-existing root")
        finally:
            (root / staged_rel).rmdir()
        self._materialize(root, prep["state_path"], prep["proposal_path"],
                          manifest_path, scope_path)
        staged_manifest = (prep["proposal_path"].parent / staged.STAGED_DIRNAME
                           / staged.MANIFEST_FILENAME)
        bib = staged_manifest.parent / "references.bib"
        original = bib.read_bytes()
        swapped = bib.parent / "references.bib.swap"
        swapped.write_bytes(original + b"% appended post-readback drift\n")
        os.replace(swapped, bib)
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("REPLAY_MISMATCH", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o11 post-readback drift")
        finally:
            bib.write_bytes(original)

    def _fresh_lf_root(self, suffix: str) -> tuple:
        """Pristine LF chain per fault case: each fault run needs no staged dir."""
        _scratch, root = _make_p3s_source_root(self, f"jgas-p3s-{suffix}-")
        prep = _lf_prepare(self, root, self.workspace, f"fixture-lf-p3s-{suffix}")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                f"scope-review-p3s-{suffix}.json")
        return root, prep, manifest_path, scope_path

    def _fault_run(self, root, prep, manifest_path, scope_path, fault):
        return _run_p3s_fixture(
            self, root, _P3S_FAULT_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(scope_path), fault])

    def test_o12a_preexisting_tamper_verify(self) -> None:
        """O12a verify-level tamper: truncated manifest / extra dir / zeroed output."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12a-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12.json")
        self._materialize(root, prep["state_path"], prep["proposal_path"],
                          manifest_path, scope_path)
        staged_manifest = (prep["proposal_path"].parent / staged.STAGED_DIRNAME
                           / staged.MANIFEST_FILENAME)
        original_manifest = staged_manifest.read_bytes()
        staged_manifest.write_bytes(original_manifest[: len(original_manifest) // 2])
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("PIN_UNREADABLE", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o12a truncated manifest")
        finally:
            staged_manifest.write_bytes(original_manifest)
        (staged_manifest.parent / "empty-subdir").mkdir()
        try:
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("STAGED_SET_MISMATCH", outcome.get("error", ""))
        finally:
            (staged_manifest.parent / "empty-subdir").rmdir()
        main_tex = staged_manifest.parent / "main.tex"
        original_main = main_tex.read_bytes()
        main_tex.write_bytes(b"")
        try:
            snap = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("REPLAY_MISMATCH", outcome.get("error", ""))
            _assert_no_write(self, snap, _snapshot(root), "o12a zeroed output")
        finally:
            main_tex.write_bytes(original_main)

    def test_o12b_during_write_faults_incomplete(self) -> None:
        """O12b real during-write zero/write/fstat/mkdir faults → INCOMPLETE-class."""
        for fault, code in (("zero-write", "STAGED_FILE_WRITE_FAILED"),
                            ("write-fail", "STAGED_FILE_WRITE_FAILED"),
                            ("fstat-fail", "STAGED_FILE_FSTAT_FAILED"),
                            ("mkdir-fail", "STAGED_ROOT_CREATE_FAILED")):
            _scratch, root = _make_p3s_source_root(self, f"jgas-p3s-o12b-{fault}-")
            prep = _lf_prepare(self, root, self.workspace, f"fixture-lf-p3s-{fault}")
            manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
            scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                    f"scope-review-p3s-{fault}.json")
            snap = _snapshot(root)
            outcome = self._fault_run(root, prep, manifest_path, scope_path, fault)
            self.assertFalse(outcome.get("ok"), f"{fault} must refuse")
            self.assertIn(code, outcome.get("error", ""), fault)
            self.assertFalse(outcome.get("timeout", False), f"{fault} must not hang")
            staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                          + "/" + staged.STAGED_DIRNAME)
            admitted = {staged_rel} | {staged_rel + "/" + name for name in
                                        (staged.MAIN_FILENAME, staged.BIBLIOGRAPHY_FILENAME,
                                         staged.STYLE_FILENAME, staged.MANIFEST_FILENAME)}
            new_entries = set(_snapshot(root)) - set(snap)
            self.assertTrue(new_entries <= admitted,
                            f"o12b {fault} owned delta not admitted: {sorted(new_entries)}")
            _assert_no_write_except(self, snap, _snapshot(root), new_entries, set(),
                                    f"o12b {fault} live-unchanged")

    def test_o12c_fsync_close_indeterminate(self) -> None:
        """O12c fsync/close faults with complete bytes → INDETERMINATE + owned partials."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12c-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12c")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12c.json")
        staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                      + "/" + staged.STAGED_DIRNAME)
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "fsync-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertIn("FSYNC_FAILED", outcome.get("error", ""))
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        _scratch2, root2 = _make_p3s_source_root(self, "jgas-p3s-o12c2-")
        prep2 = _lf_prepare(self, root2, self.workspace, "fixture-lf-p3s-12c2")
        manifest2 = _capture(self, root2, prep2["state_path"], prep2["proposal_path"])
        scope2 = _scope_for(self, root2, prep2["prepared"], prep2["proposal_path"],
                            "scope-review-p3s-12c2.json")
        staged_rel2 = (prep2["proposal_path"].parent.relative_to(root2).as_posix()
                       + "/" + staged.STAGED_DIRNAME)
        base2 = _snapshot(root2)
        outcome = self._fault_run(root2, prep2, manifest2, scope2, "close-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertIn("CLOSE_FAILED", outcome.get("error", ""))
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        after2 = _snapshot(root2)
        new2 = set(after2) - set(base2)
        self.assertEqual(new2, {staged_rel2, staged_rel2 + "/main.tex"},
                         f"close fault owned partials: {sorted(new2)}")

    def test_o12d_manifest_failure_indeterminate(self) -> None:
        """O12d manifest write/close faults → INDETERMINATE; valid bytes stay verifiable."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12d-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12d")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12d.json")
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "manifest-write-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        _scratch3, root3 = _make_p3s_source_root(self, "jgas-p3s-o12d3-")
        prep3 = _lf_prepare(self, root3, self.workspace, "fixture-lf-p3s-12d3")
        manifest3 = _capture(self, root3, prep3["state_path"], prep3["proposal_path"])
        scope3 = _scope_for(self, root3, prep3["prepared"], prep3["proposal_path"],
                            "scope-review-p3s-12d3.json")
        staged_rel3 = (prep3["proposal_path"].parent.relative_to(root3).as_posix()
                       + "/" + staged.STAGED_DIRNAME)
        outcome = self._fault_run(root3, prep3, manifest3, scope3, "manifest-close-fail")
        self.assertFalse(outcome.get("ok"), "manifest close fault must not report success")
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        staged_manifest = root3 / staged_rel3 / staged.MANIFEST_FILENAME
        self.assertTrue(staged_manifest.is_file(), "complete valid bytes may remain after failed close")
        vout = self._verify(root3, prep3["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)

    def test_o12e_fstat_identity_mismatch(self) -> None:
        """O12e fstat-vs-entry identity mismatch refuses before any byte is written."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12e-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12e")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12e.json")
        snap = _snapshot(root)
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "fstat-fake")
        self.assertFalse(outcome.get("ok"))
        self.assertIn("STAGED_FILE_REPLACED", outcome.get("error", ""))
        _assert_no_write(self, snap, _snapshot(root), "o12e identity mismatch no-write")

    def test_o11b_midcall_reader_drift(self) -> None:
        """O11b reader drift between pin and use refuses with exact owned delta.

        The fault tampers the staged reader file after its first pin read
        inside the fixture subprocess; the writer must refuse at the
        stability check with nothing claimed. The injected reader change
        itself is the only allowed delta.
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o11b-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-11b")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-11b.json")
        base = _snapshot(root)
        reader_rel = prep["prepared"]["proposal"]["proposed"]["proposed_reader_ref"]["path"]
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "drift-reader")
        self.assertFalse(outcome.get("ok"), "mid-call reader drift must refuse")
        self.assertIn("STABILITY_VIOLATION", outcome.get("error", ""))
        _assert_no_write_except(self, base, _snapshot(root), set(), {reader_rel},
                                "o11b drift fault-present")

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
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)])
            self.assertFalse(outcome.get("ok"))
            self.assertIn("TOOL_DRIFT", outcome.get("error", ""))
            _assert_no_write(self, snap_fault, _snapshot(root), "o13 fault-present no-write")
        finally:
            target.write_text(text, encoding="utf-8")
        _assert_no_write(self, base, _snapshot(root), "o13 restored")
        missing = scope_path.parent / "scope-absent-o13.json"
        snap_missing = _snapshot(root)
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(missing)])
        self.assertFalse(outcome.get("ok"))
        _assert_no_write(self, snap_missing, _snapshot(root), "o13 missing-scope no-write")

    def test_o14_byte_equal_existing_root_refuses(self) -> None:
        """O14 byte-equal pre-existing staged set still refuses writer takeover."""
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o14-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-14")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-14.json")
        self._materialize(root, prep["state_path"], prep["proposal_path"],
                          manifest_path, scope_path)
        staged_manifest = (prep["proposal_path"].parent / staged.STAGED_DIRNAME
                           / staged.MANIFEST_FILENAME)
        self._verify(root, prep["proposal_path"], staged_manifest)
        snap = _snapshot(root)
        outcome = _run_p3s_fixture(
            self, root, _P3S_MATERIALIZE_SCRIPT,
            [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
             str(manifest_path), str(scope_path)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("STAGED_ROOT_EXISTS", outcome.get("error", ""))
        _assert_no_write(self, snap, _snapshot(root), "o14 byte-equal no-takeover")
        self._verify(root, prep["proposal_path"], staged_manifest)

    def test_r1_genuine_owner_binds_materialization(self) -> None:
        """R1 genuine owner on the SAME chain: comment commit + fixture refresh.

        Refresh runs against the SAME built State that is then prepared,
        captured, scoped and materialized, and the materialized basis is
        bound to the refreshed receipt + R1 commit head.
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-r1-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        head_before = core.repository_commit_sha(root)
        _commit_r1_nonemitted_comment(self, root)
        r1_head = core.repository_commit_sha(root)
        self.assertNotEqual(r1_head, head_before)
        state_before = core.sha256_file(state_path)
        out = _run_fixture_code(self, root, p2vt._R1_REFRESH_SCRIPT,
                                [str(root), str(state_path)])
        self.assertTrue(out.strip(), "R1 fixture refresh produced no output")
        self.assertNotEqual(core.sha256_file(state_path), state_before,
                            "R1 refresh must change the State it ran against")
        prep = _weekly_prepare_from(self, root, helper, built, "fixture-wk-p3s-r1")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-r1.json")
        outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        self.assertEqual(outcome["head"], r1_head)
        manifest = core.load_json(staged_manifest)
        receipt_ref = manifest["basis"]["generated_receipt_ref"]
        self.assertEqual(core.sha256_file(root / receipt_ref["path"]), receipt_ref["sha256"],
                         "materialized basis must bind the refreshed receipt bytes")
        main_text = (staged_manifest.parent / "main.tex").read_text(encoding="utf-8")
        self.assertNotIn("fixture R1 non-emitted Python comment", main_text)
        vout = self._verify(root, prep["proposal_path"], staged_manifest)
        self.assertEqual(vout["reader"],
                         manifest["proposed"]["proposed_reader_canonical_sha256"])


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
        

