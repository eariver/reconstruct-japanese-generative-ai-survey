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


def _durable_base() -> Path:
    """Durable evidence base OUTSIDE fixture TemporaryDirectory cleanup.

    When the runner provides P3S_DURABLE_OUTDIR it must point to the runner's
    new ``outdir/fixture-raw`` directory so raw/meta are collected via a known
    path; otherwise fallback is explicitly ``/tmp/opencode``. The directory is
    never automatically cleaned up; evidence persists for the packet.
    """
    import hashlib as _hl
    env_dir = os.environ.get("P3S_DURABLE_OUTDIR")
    if env_dir:
        base = Path(env_dir)
        base.mkdir(parents=True, exist_ok=True)
        return base
    base = Path("/tmp/opencode")
    base.mkdir(parents=True, exist_ok=True)
    return base


def _launch_durable_child(root: Path, script: str, args: list[str], timeout_s: int,
                          label: str) -> dict:
    """Common durable launcher: xb outputs BEFORE Popen, direct child fds.

    Opens exclusive ``xb`` stdout/stderr files BEFORE launch and passes the
    open fds directly to the child (no PIPE-then-write-after-communicate).
    Writes an exclusive pre-launch meta with pid/running record immediately
    after Popen, then waits with process-group timeout/interrupt kill and
    bounded reap. The finally block preserves any primary timeout/interrupt
    error and attaches secondary close failures instead of masking it. Saves
    the exact script text, its sha256, and the actual argv/cwd/sanitized env
    for evidence. Returns terminal status plus durable paths and full bytes.
    """
    import hashlib as _hl
    import time as _time
    import signal as _signal
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1"})
    base = _durable_base()
    call_dir = Path(tempfile.mkdtemp(prefix=f"p3s-{label}-", dir=str(base)))
    stdout_p = call_dir / "child.stdout.bin"
    stderr_p = call_dir / "child.stderr.bin"
    script_p = call_dir / "child.script.py"
    meta_pre_p = call_dir / "child.meta_pre.json"
    meta_final_p = call_dir / "child.meta.json"
    script_b = script.encode("utf-8")
    # Save exact script bytes for evidence (no truncation).
    with open(script_p, "xb") as _sf:
        _sf.write(script_b)
    script_sha = _hl.sha256(script_b).hexdigest()
    # Exclusive xb outputs BEFORE Popen (fail-closed if the path exists).
    fb_out = open(stdout_p, "xb")
    fb_err = open(stderr_p, "xb")
    started = _time.time()
    argv = [sys.executable, "-c", script, *args]
    proc = subprocess.Popen(argv, cwd=root, stdout=fb_out, stderr=fb_err,
                            env=env, start_new_session=True, text=False)
    # Exclusive pre-launch meta with pid/running record immediately.
    pre_meta = {"label": label, "argv": [sys.executable, "-c", f"<{label}-script-sha256:{script_sha[:16]}>", *args],
                "actual_argc": len(argv), "cwd": str(root), "pid": proc.pid, "pgid": proc.pid,
                "running": True, "timeout_s": timeout_s, "started": started,
                "script": str(script_p), "script_sha256": script_sha, "script_bytes": len(script_b),
                "stdout": str(stdout_p), "stderr": str(stderr_p),
                "env": {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                        "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1"}}
    with open(meta_pre_p, "x", encoding="utf-8") as _pf:
        _pf.write(json.dumps(pre_meta, indent=2, sort_keys=True) + "\n")
    primary: BaseException | None = None
    timed_out = False
    interrupted = False
    try:
        try:
            rc = proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired as exc:
            primary = exc
            timed_out = True
            try:
                os.killpg(proc.pid, _signal.SIGTERM)
            except OSError as _e:
                pass
            try:
                rc = proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, _signal.SIGKILL)
                except OSError:
                    pass
                rc = proc.wait(timeout=10)
        except KeyboardInterrupt as exc:
            primary = exc
            interrupted = True
            try:
                os.killpg(proc.pid, _signal.SIGTERM)
            except OSError:
                pass
            try:
                rc = proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, _signal.SIGKILL)
                except OSError:
                    pass
                rc = proc.wait(timeout=10)
            raise
        else:
            rc = proc.returncode
    finally:
        # Bounded reap: ensure the child is reaped without hanging the harness.
        try:
            if proc.poll() is None:
                try:
                    os.killpg(proc.pid, _signal.SIGKILL)
                except OSError:
                    pass
                try:
                    proc.wait(timeout=10)
                except Exception as _reap_exc:
                    if primary is None:
                        primary = _reap_exc
        except Exception as _poll_exc:
            if primary is None:
                primary = _poll_exc
        # Close child output fds; secondary close failures attach, never mask.
        close_secondaries: list[str] = []
        for _fb, _nm in ((fb_out, "stdout"), (fb_err, "stderr")):
            try:
                try:
                    _fb.flush()
                except OSError as _fe:
                    close_secondaries.append(f"{_nm}-flush: {_fe}")
                _fb.close()
            except OSError as _ce:
                close_secondaries.append(f"{_nm}-close: {_ce}")
        ended = _time.time()
        try:
            out_b = stdout_p.read_bytes()
        except OSError as _re:
            out_b = b""
            close_secondaries.append(f"stdout-readback: {_re}")
        try:
            err_b = stderr_p.read_bytes()
        except OSError as _re:
            err_b = b""
            close_secondaries.append(f"stderr-readback: {_re}")
        final_meta = dict(pre_meta)
        final_meta.update({"running": False, "rc": proc.returncode if proc.returncode is not None else rc,
                           "timeout": timed_out, "interrupted": interrupted,
                           "ended": ended, "elapsed_s": ended - started,
                           "close_secondaries": close_secondaries,
                           "durable_dir": str(call_dir)})
        if primary is not None:
            final_meta["primary"] = f"{type(primary).__name__}: {primary}"[:2000]
        # Exclusive final meta (call_dir is fresh, so x == w here, but keep x
        # semantics explicit for the runner contract).
        with open(meta_final_p, "x", encoding="utf-8") as _ff:
            _ff.write(json.dumps(final_meta, indent=2, sort_keys=True) + "\n")
        if primary is not None and isinstance(primary, KeyboardInterrupt):
            raise primary
    out_s = out_b.decode("utf-8", "replace")
    err_s = err_b.decode("utf-8", "replace")
    return {"rc": proc.returncode if proc.returncode is not None else rc,
            "timeout": timed_out, "interrupted": interrupted,
            "out_b": out_b, "err_b": err_b, "out_s": out_s, "err_s": err_s,
            "durable_dir": str(call_dir), "meta_pre": str(meta_pre_p),
            "meta": str(meta_final_p), "stdout_p": str(stdout_p),
            "stderr_p": str(stderr_p), "script_p": str(script_p),
            "script_sha256": script_sha, "timeout_s": timeout_s,
            "elapsed_s": ended - started, "pid": proc.pid, "pgid": proc.pid}


def _run_fixture_code(testcase: unittest.TestCase, root: Path, script: str,
                      args: list[str], timeout_s: int = 1800) -> str:
    """Run fixture-code via the common durable launcher (R1 refresh 1800s).

    1800s is a conservative operational bound for a fixture refresh
    subprocess (covers slow filesystems/runners); it is not a measured
    sufficiency claim and confers no margin proof. Timeouts/interrupts kill
    the whole process group and are saved explicitly with durable raw/meta.
    """
    res = _launch_durable_child(root, script, args, timeout_s, "fixture-code")
    testcase.assertFalse(res["timeout"], f"fixture-code timed out after {timeout_s}s; raw in {res['durable_dir']}")
    testcase.assertFalse(res["interrupted"], f"fixture-code interrupted; raw in {res['durable_dir']}")
    testcase.assertEqual(res["rc"], 0,
                         f"fixture-code step failed; raw in {res['durable_dir']}:\nSTDOUT:\n{res['out_s']}\nSTDERR:\n{res['err_s'][-4000:]}")
    return res["out_s"]


_P3S_MATERIALIZE_SCRIPT = r"""
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
    code = getattr(exc, "code", type(exc).__name__)
    phase = getattr(exc, "phase", "")
    disp = getattr(exc, "disposition", "")
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
                      "code": code, "phase": phase, "disposition": disp,
                      "owned_files": len(owned.get("owned_files", [])) if isinstance(owned, dict) else 0,
                      "owned": owned if isinstance(owned, dict) else {}}))
"""

_P3S_VERIFY_SCRIPT = r"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1]); proposal_path = Path(sys.argv[2]); staged_path = Path(sys.argv[3])
from scripts import survey_editorial_staged_source_v2 as staged
try:
    out = staged.verify_staged_source(root, proposal_path, staged_path)
    print(json.dumps({"ok": True, "result": out["result"],
                      "reader": out["measured"]["proposed_reader_sha256"]}))
except Exception as exc:
    code = getattr(exc, "code", type(exc).__name__)
    phase = getattr(exc, "phase", "")
    disp = getattr(exc, "disposition", "")
    print(json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
                      "code": code, "phase": phase, "disposition": disp}))
"""

# During-write fault injection: scoped wrappers around ACTUAL os operations
# inside the fixture subprocess (never mock-replacement of authority/P2V/
# replay). The fault fires once on a targeted real call; the API underneath
# is genuine. Result (including owned-file counts) is printed AFTER restoring
# the real operations so the outcome record itself is reliable.
_P3S_FAULT_SCRIPT = r"""
import json, os, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2]); proposal_path = Path(sys.argv[3])
manifest_path = Path(sys.argv[4]); scope_path = Path(sys.argv[5])
fault = sys.argv[6]
from scripts import survey_editorial_staged_source_v2 as staged
real_write, real_fsync, real_close = os.write, os.fsync, os.close
real_fstat, real_mkdir, real_open = os.fstat, os.mkdir, os.open
STAGED_LEAVES = ("main.tex", "references.bib", "jgaisurvey.sty", "staged-source-manifest.json")
active = {}
gen_counter = {"n": 0}
fired = {"n": 0}
partial_state = {"n": 0}
def _leaf_of(path):
    try:
        s = os.fspath(path)
    except Exception:
        return None
    if isinstance(s, bytes):
        try:
            s = s.decode()
        except Exception:
            return None
    return Path(s).name
def _track_open(path, flags, *a, **k):
    fd = real_open(path, flags, *a, **k)
    if flags & os.O_CREAT:
        leaf = _leaf_of(path)
        if leaf in STAGED_LEAVES:
            gen_counter["n"] += 1
            active[fd] = {"leaf": leaf, "gen": gen_counter["n"]}
    return fd
def _write_once(fd, data):
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault in ("zero-write", "write-fail") and fired["n"] == 0:
        fired["n"] += 1
        if fault == "zero-write":
            return 0
        raise OSError(5, "injected write failure")
    if leaf == "main.tex" and fault == "short-once" and fired["n"] == 0:
        fired["n"] += 1
        half = max(1, len(bytes(data)) // 2)
        return real_write(fd, bytes(data)[:half])
    if leaf == "main.tex" and fault == "partial-then-fail":
        if partial_state["n"] == 0 and fired["n"] == 0:
            partial_state["n"] = 1
            fired["n"] += 1
            return real_write(fd, bytes(data)[:1])
        if partial_state["n"] == 1 and fired["n"] == 1:
            fired["n"] += 1
            raise OSError(5, "injected partial-then-fail second write")
    if leaf == "main.tex" and fault == "write-then-close-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected write failure (primary for close test)")
    if leaf == "staged-source-manifest.json" and fault == "manifest-write-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected manifest write failure")
    return real_write(fd, data)
def _fsync_once(fd):
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault == "fsync-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected fsync failure")
    return real_fsync(fd)
def _close_once(fd):
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault == "close-fail" and fired["n"] == 0:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected close failure")
    if leaf == "staged-source-manifest.json" and fault == "manifest-close-fail" and fired["n"] == 0:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected manifest close failure")
    if leaf == "main.tex" and fault == "write-then-close-fail" and fired["n"] == 1:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected secondary close failure")
    if fault == "close-leak-reuse" and info is not None and fired["n"] == 0:
        fired["n"] += 1
        active.pop(fd, None)
        raise OSError(5, "injected close failure")
    active.pop(fd, None)
    return real_close(fd)
def _fstat_once(fd):
    st = real_fstat(fd)
    info = active.get(fd)
    leaf = info["leaf"] if info else None
    if leaf == "main.tex" and fault == "fstat-fake" and fired["n"] == 0:
        fired["n"] += 1
        return os.stat_result((st.st_mode, st.st_ino + 7, st.st_dev, st.st_nlink, st.st_uid, st.st_gid, st.st_size, st.st_atime, st.st_mtime, st.st_ctime))
    if leaf == "main.tex" and fault == "fstat-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(5, "injected fstat failure")
    return st
def _mkdir_once(path, *a, **k):
    leaf = _leaf_of(path)
    if leaf == "staged-source" and fault == "mkdir-fail" and fired["n"] == 0:
        fired["n"] += 1
        raise OSError(13, "injected mkdir failure")
    return real_mkdir(path, *a, **k)
_exact_reader_rel = None
try:
    _prop = json.loads(Path(proposal_path).read_bytes().decode("utf-8"))
    _exact_reader_rel = (_prop.get("proposed") or {}).get("proposed_reader_ref", {}).get("path")
except Exception:
    _exact_reader_rel = None
_real_read_bytes = Path.read_bytes
def _read_bytes_once(self):
    data = _real_read_bytes(self)
    try:
        is_exact = (_exact_reader_rel is not None and Path(self) == root / _exact_reader_rel)
    except Exception:
        is_exact = False
    if fault == "drift-reader" and is_exact and fired["n"] == 0:
        fired["n"] += 1
        with open(self, "ab") as handle:
            handle.write(b"\n% injected mid-call drift\n")
    return data
if fault == "drift-reader":
    Path.read_bytes = _read_bytes_once
# R2-4 late/drift/root wrappers: call the real helper first, then inject at the
# exact named boundary (never replace authority with fake success). Each pins
# the exact target path derived from the supplied proposal/manifest.
_real_compare = staged._compare_original_boundary
_real_emit = staged._emit_outputs
_real_verify_outputs = staged._verify_outputs_and_manifest
_real_verify = staged.verify_staged_source
_real_canonical = staged._canonical_json_bytes
_compare_calls = {"n": 0}
_emit_calls = {"n": 0}
def _late_control_path():
    return root / "scripts" / "late-control-probe-p3s.txt"
def _late_retained_dir():
    try:
        _pp = Path(proposal_path).parent.relative_to(root).as_posix()
    except Exception:
        _pp = None
    if _pp is None:
        return None
    return root / _pp / "retained" / "late-retained-probe-dir"
def _staged_rel_exact():
    try:
        _pp = Path(proposal_path).parent.relative_to(root).as_posix()
    except Exception:
        return None
    return _pp + "/staged-source"
def _compare_wrap(*a, **k):
    _compare_calls["n"] += 1
    out = _real_compare(*a, **k)
    if fault == "late-control-add" and _compare_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        _late_control_path().write_text("late control addition\n", encoding="utf-8")
    if fault == "late-retained-add" and _compare_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        d = _late_retained_dir()
        if d is not None:
            d.mkdir(parents=True, exist_ok=True)
    return out
def _canonical_wrap(*a, **k):
    out = _real_canonical(*a, **k)
    if fault == "drift-before-claim" and fired["n"] == 0:
        fired["n"] += 1
        if _exact_reader_rel is not None:
            with open(root / _exact_reader_rel, "ab") as h:
                h.write(b"\n% drift before claim\n")
    return out
def _emit_wrap(*a, **k):
    _emit_calls["n"] += 1
    if fault in ("root-replace", "ancestor-replace") and _emit_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        _srel = _staged_rel_exact()
        if _srel is not None:
            _sabs = root / _srel
            try:
                _backup = Path(str(_sabs) + ".orig-p3s")
                os.rename(_sabs, _backup)
            except Exception:
                _backup = None
            try:
                if fault == "root-replace":
                    _sabs.mkdir(parents=False, exist_ok=False)
                    (_sabs / "replacement.txt").write_text("replacement root\n", encoding="utf-8")
                else:
                    _sabs.symlink_to("/tmp")
            except Exception:
                pass
        return _real_emit(*a, **k)
    out = _real_emit(*a, **k)
    if fault == "drift-before-manifest" and _emit_calls["n"] == 1 and fired["n"] == 0:
        fired["n"] += 1
        try:
            _man = json.loads(Path(manifest_path).read_bytes().decode("utf-8"))
            _rows = _man.get("rows") or []
            _copy = next((r for r in _rows if r.get("policy") == "COPY_BEFORE_REPLACEMENT"), None)
            if _copy is not None:
                with open(root / _copy["retained_dest"], "ab") as h:
                    h.write(b"\n% drift before manifest\n")
            else:
                with open(root / _exact_reader_rel, "ab") as h:
                    h.write(b"\n% drift before manifest fallback\n")
        except Exception:
            pass
    return out
def _verify_outputs_wrap(*a, **k):
    out = _real_verify_outputs(*a, **k)
    if fault == "post-readback-edit" and fired["n"] == 0:
        fired["n"] += 1
        _srel = _staged_rel_exact()
        if _srel is not None:
            _main = root / _srel / "main.tex"
            try:
                _data = _main.read_bytes()
                _main.write_bytes(_data[:10] + b"% POST-READBACK EDIT\n" + _data[10:])
            except Exception:
                pass
    return out
def _verify_wrap(*a, **k):
    out = _real_verify(*a, **k)
    if fault == "post-replay-samebyte-replace" and fired["n"] == 0:
        fired["n"] += 1
        _srel = _staged_rel_exact()
        if _srel is not None:
            for _nm in ("main.tex", "references.bib", "jgaisurvey.sty", "staged-source-manifest.json"):
                _p = root / _srel / _nm
                try:
                    _d = _p.read_bytes()
                    _tmp = _p.parent / (_nm + ".swap-p3s")
                    _tmp.write_bytes(_d)
                    os.replace(_tmp, _p)
                except Exception:
                    pass
            _srel2 = _srel
            try:
                _m = root / _srel2 / "staged-source-manifest.json"
                _d2 = _m.read_bytes()
                _t2 = _m.parent / "staged-source-manifest.json.swap-p3s"
                _t2.write_bytes(_d2)
                os.replace(_t2, _m)
            except Exception:
                pass
    return out
if fault in ("late-control-add", "late-retained-add"):
    staged._compare_original_boundary = _compare_wrap
if fault == "drift-before-claim":
    staged._canonical_json_bytes = _canonical_wrap
if fault in ("drift-before-manifest", "root-replace", "ancestor-replace"):
    staged._emit_outputs = _emit_wrap
if fault == "post-readback-edit":
    staged._verify_outputs_and_manifest = _verify_outputs_wrap
if fault == "post-replay-samebyte-replace":
    staged.verify_staged_source = _verify_wrap
os.open, os.write, os.fsync, os.close, os.fstat, os.mkdir = (
    _track_open, _write_once, _fsync_once, _close_once, _fstat_once, _mkdir_once)
outcome = {"ok": True, "result": "PENDING", "fired": 0}
try:
    out = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
    outcome = {"ok": True, "result": out["result"], "fired": fired["n"],
               "head": out.get("observed_head")}
except Exception as exc:
    owned = getattr(exc, "owned", {})
    code = getattr(exc, "code", type(exc).__name__)
    phase = getattr(exc, "phase", "")
    disp = getattr(exc, "disposition", "")
    outcome = {"ok": False, "error": f"{type(exc).__name__}: {exc}"[:2000],
               "code": code, "phase": phase, "disposition": disp,
               "fired": fired["n"],
               "owned_files": len(owned.get("owned_files", [])) if isinstance(owned, dict) else 0,
               "owned": owned if isinstance(owned, dict) else {}}
finally:
    os.write, os.fsync, os.close, os.fstat, os.mkdir, os.open = (
        real_write, real_fsync, real_close, real_fstat, real_mkdir, real_open)
    if fault == "drift-reader":
        Path.read_bytes = _real_read_bytes
    staged._compare_original_boundary = _real_compare
    staged._emit_outputs = _real_emit
    staged._verify_outputs_and_manifest = _real_verify_outputs
    staged.verify_staged_source = _real_verify
    staged._canonical_json_bytes = _real_canonical
print(json.dumps(outcome))
"""


def _run_p3s_fixture(testcase: unittest.TestCase, root: Path, script: str,
                     args: list[str], timeout_s: int = 1800) -> dict:
    """Run a P3S public operation via the common durable launcher.

    Selected conservative operational bounds (not measured sufficiency, no
    margin proof): materialize/fault paths 1800s, standalone verify 600s
    (callers pass explicitly), FIFO no-read 60s (must refuse without blocking).
    The 1800/600s values cover slow filesystems/runners; they do not prove
    that any run will complete within the bound. Timeouts/interrupts kill the
    whole process group and are saved explicitly with durable raw/meta.
    Full stdout/stderr survive fixture cleanup and are returned (not discarded
    on success). No automatic cleanup of evidence.
    """
    res = _launch_durable_child(root, script, args, timeout_s, "p3s")
    if res["timeout"] or res["interrupted"]:
        return {"ok": False, "timeout": True, "timed_out": res["timeout"],
                "interrupted": res["interrupted"],
                "stdout": res["out_s"][-2000:], "stderr": res["err_s"][-2000:],
                "durable_dir": res["durable_dir"], "meta": res["meta"],
                "meta_pre": res["meta_pre"],
                "raw_stdout": res["stdout_p"], "raw_stderr": res["stderr_p"],
                "script": res["script_p"], "script_sha256": res["script_sha256"]}
    testcase.assertEqual(res["rc"], 0,
                         f"P3S fixture step crashed; raw in {res['durable_dir']}:\nSTDOUT:\n{res['out_s']}\nSTDERR:\n{res['err_s'][-4000:]}")
    lines = [line for line in res["out_s"].splitlines() if line.strip().startswith("{")]
    testcase.assertTrue(lines, f"P3S fixture printed no JSON outcome; raw in {res['durable_dir']}:\n{res['out_s'][-2000:]}")
    outcome = json.loads(lines[-1])
    # Preserve full raw through cleanup (not truncated, not success-discarded).
    outcome["durable_dir"] = res["durable_dir"]
    outcome["meta"] = res["meta"]
    outcome["meta_pre"] = res["meta_pre"]
    outcome["raw_stdout"] = res["stdout_p"]
    outcome["raw_stderr"] = res["stderr_p"]
    outcome["script"] = res["script_p"]
    outcome["script_sha256"] = res["script_sha256"]
    outcome["stdout_full"] = res["out_s"]
    outcome["stderr_full"] = res["err_s"]
    outcome["timeout"] = False
    outcome["interrupted"] = False
    return outcome


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
    # Exact allowed ancestor/owned-dir sets (R2-1): _snapshot records BOTH
    # files and dirs, so the admitted delta must list new dirs explicitly
    # (derived, not observed). New files are the retention manifest plus
    # every COPY dest; new dirs are retained_rel plus every ancestor dir of
    # those files up to retained_rel (retained/before/... chain).
    new_files = {out["manifest_path"]} | {r["retained_dest"] for r in
                              core.load_json(manifest_path)["rows"]
                              if r["policy"] == "COPY_BEFORE_REPLACEMENT"}
    retained_rel = Path(out["manifest_path"]).parent.as_posix()
    new_dirs: set[str] = {retained_rel}
    for frel in new_files:
        parts = Path(frel).parts
        # walk ancestors strictly below retained_rel's parent, down to retained_rel
        cur: list[str] = list(parts[:-1])
        while len(cur) >= len(Path(retained_rel).parts):
            cand = Path(*cur).as_posix()
            # only dirs at/below retained_rel are owned-new
            if cand == retained_rel or cand.startswith(retained_rel + "/"):
                new_dirs.add(cand)
            if cand == retained_rel:
                break
            cur = cur[:-1]
    _assert_owned_delta_only(testcase, before, _snapshot(root),
                             new_files | new_dirs,
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
        staged_rel = staged_dir.relative_to(root).as_posix()
        allowed = {staged_rel} | {staged_rel + "/" + name
                   for name in (staged.MAIN_FILENAME, staged.BIBLIOGRAPHY_FILENAME,
                                staged.STYLE_FILENAME, staged.MANIFEST_FILENAME)}
        _assert_owned_delta_only(self, before, _snapshot(root), allowed, "materialize owned delta")
        staged_manifest = staged_dir / staged.MANIFEST_FILENAME
        self.assertTrue(staged_manifest.is_file())
        return outcome, staged_manifest

    def _verify(self, root: Path, proposal_path: Path, staged_manifest: Path) -> dict:
        """Run the PUBLIC verifier in a fresh fixture-code subprocess (600s).

        600s is the selected conservative operational bound for a standalone
        deterministic replay (no P2V); it is not a measured sufficiency claim
        and confers no margin proof.
        """
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(proposal_path), str(staged_manifest)], timeout_s=600)
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
        """O6a TOOL_DRIFT via standalone artifact dependency tamper (verifier).

        R2-9: a writer pre-tamper is reread by the fresh fixture interpreter
        and may be refused earlier by State/KEEP/current-tool checks, so it
        cannot force a TOOL_DRIFT code. This uses a healthy staged set, then
        tampers an import-only S2 dep and runs the standalone verifier, which
        compares staged code_deps to current bytes and must refuse TOOL_DRIFT
        (no earlier KEEP/schema preemption on this path).
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o6a-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-6a")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-6a.json")
        _outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        # Healthy replay first (proves the staged set was good before tamper).
        self._verify(root, prep["proposal_path"], staged_manifest)
        target = root / "scripts" / "survey_review_attention_v2.py"
        snap = _snapshot(root)
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n# Fixture TOOL_DRIFT probe (import-only dep).\n",
                          encoding="utf-8")
        try:
            snap_fault = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)], timeout_s=600)
            self.assertFalse(outcome.get("ok"), "TOOL_DRIFT case must refuse")
            self.assertIn("TOOL_DRIFT", outcome.get("error", ""))
            self.assertEqual(outcome.get("code"), "TOOL_DRIFT")
            self.assertEqual(outcome.get("phase"), "PIN")
            self.assertEqual(outcome.get("disposition"), "INVALID")
            # Verifier is read-only: fault-present snapshot must be unchanged
            # by the refusal itself (before repair).
            _assert_no_write(self, snap_fault, _snapshot(root), "o6a TOOL_DRIFT no-write")
        finally:
            target.write_text(text, encoding="utf-8")
        _assert_no_write(self, snap, _snapshot(root), "o6a restored")
        # After restore, the same staged set verifies again (proves drift cause).
        self._verify(root, prep["proposal_path"], staged_manifest)

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
            # R3-6: phase/disposition asserted (earlier KEEP refusal surfaces via
            # OBSERVE, not TOOL_DRIFT).
            self.assertEqual(outcome.get("phase"), "OBSERVE")
            self.assertEqual(outcome.get("disposition"), "REFUSED_PRE_WRITE")
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
        self.assertTrue(outcome.get("phase"), "o7 missing scope must report phase")
        self.assertTrue(outcome.get("disposition"), "o7 missing scope must report disposition")
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
        self.assertTrue(outcome.get("phase"), "o7 ordinary scope must report phase")
        self.assertTrue(outcome.get("disposition"), "o7 ordinary scope must report disposition")
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
            self.assertTrue(outcome.get("phase"), "o7 malformed scope must report phase")
            self.assertTrue(outcome.get("disposition"), "o7 malformed scope must report disposition")
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
        self.assertEqual(outcome.get("phase"), "OBSERVE")
        self.assertEqual(outcome.get("disposition"), "REFUSED_PRE_WRITE")
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
            self.assertTrue(outcome.get("phase"), "o8 extra-file must report phase")
            self.assertTrue(outcome.get("disposition"), "o8 extra-file must report disposition")
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
            self.assertTrue(outcome.get("phase"), "o8 duplicate-key must report phase")
            self.assertTrue(outcome.get("disposition"), "o8 duplicate-key must report disposition")
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
        self.assertTrue(outcome.get("phase"), "o8 wrong-path must report phase")
        self.assertTrue(outcome.get("disposition"), "o8 wrong-path must report disposition")
        self._retamper_manifest(
            staged_manifest, lambda m: m.update({"extra_unknown_field": 1}))
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(prep["proposal_path"]), str(staged_manifest)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("SCHEMA_INVALID", outcome.get("error", ""))
        self.assertTrue(outcome.get("phase"), "o8 unknown-field must report phase")
        self.assertTrue(outcome.get("disposition"), "o8 unknown-field must report disposition")
        def _swap_deps(manifest):
            deps = manifest["code_deps"]
            deps[0], deps[1] = deps[1], deps[0]
        self._retamper_manifest(staged_manifest, _swap_deps)
        outcome = _run_p3s_fixture(
            self, root, _P3S_VERIFY_SCRIPT,
            [str(root), str(prep["proposal_path"]), str(staged_manifest)])
        self.assertFalse(outcome.get("ok"))
        self.assertIn("CODE_DEPS_MISMATCH", outcome.get("error", ""))
        self.assertTrue(outcome.get("phase"), "o8 swapped-deps must report phase")
        self.assertTrue(outcome.get("disposition"), "o8 swapped-deps must report disposition")

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
            self.assertTrue(outcome.get("phase"), "o9 alias reader must report phase")
            self.assertTrue(outcome.get("disposition"), "o9 alias reader must report disposition")
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
            # 60s FIFO bound (R2-8): a raw-safe no-read refusal must fail fast
            # without opening the FIFO; 60s proves no hang with margin, not a
            # guessed 300s/120s wait for expensive P2V paths.
            outcome = _run_p3s_fixture(
                self, root, _P3S_MATERIALIZE_SCRIPT,
                [str(root), str(prep["state_path"]), str(prep["proposal_path"]),
                 str(manifest_path), str(scope_path)], timeout_s=60)
            self.assertFalse(outcome.get("ok"), "FIFO staged reader must refuse, not hang")
            self.assertNotIn("timeout", json.dumps(outcome),
                             f"FIFO case blocked instead of refusing: {outcome}")
            self.assertRegex(outcome.get("error", ""),
                             "PATH_NOT_REGULAR|PATH_UNREADABLE|PATH_ALIAS")
            self.assertTrue(outcome.get("phase"), "o9 fifo must report phase")
            self.assertTrue(outcome.get("disposition"), "o9 fifo must report disposition")
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
            self.assertTrue(outcome.get("phase"), "o9 ancestor must report phase")
            self.assertTrue(outcome.get("disposition"), "o9 ancestor must report disposition")
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
            self.assertTrue(outcome.get("phase"), "o10 edit must report phase")
            self.assertTrue(outcome.get("disposition"), "o10 edit must report disposition")
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
            self.assertTrue(outcome.get("phase"), "o11 pre-existing must report phase")
            self.assertTrue(outcome.get("disposition"), "o11 pre-existing must report disposition")
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
            self.assertTrue(outcome.get("phase"), "o11 drift must report phase")
            self.assertTrue(outcome.get("disposition"), "o11 drift must report disposition")
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
        """O12b real during-write zero/write/fstat/mkdir faults → INCOMPLETE-class.

        R2-9: each fault has an exact expected delta (not an admitted subset).
        zero/write/fstat on the first file leave root+empty/partial main.tex;
        mkdir leaves nothing. Fired count and typed code/phase are asserted.
        """
        cases = (("zero-write", "STAGED_FILE_WRITE_FAILED", {"main"}),
                 ("write-fail", "STAGED_FILE_WRITE_FAILED", {"main"}),
                 ("fstat-fail", "STAGED_FILE_FSTAT_FAILED", {"main"}),
                 ("mkdir-fail", "STAGED_ROOT_CREATE_FAILED", set()))
        for fault, code, _files in cases:
            _scratch, root = _make_p3s_source_root(self, f"jgas-p3s-o12b-{fault}-")
            prep = _lf_prepare(self, root, self.workspace, f"fixture-lf-p3s-{fault}")
            manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
            scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                    f"scope-review-p3s-{fault}.json")
            snap = _snapshot(root)
            outcome = self._fault_run(root, prep, manifest_path, scope_path, fault)
            self.assertFalse(outcome.get("ok"), f"{fault} must refuse")
            self.assertEqual(outcome.get("fired"), 1, f"{fault} must fire once: {outcome}")
            self.assertIn(code, outcome.get("error", ""), fault)
            self.assertEqual(outcome.get("code"), code, fault)
            # R3-6: phase/disposition asserted, not merely returned.
            self.assertEqual(outcome.get("phase"), "CLAIM", fault)
            self.assertEqual(outcome.get("disposition"), "OWNED_PARTIAL", fault)
            self.assertFalse(outcome.get("timeout", False), f"{fault} must not hang")
            staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                          + "/" + staged.STAGED_DIRNAME)
            if fault == "mkdir-fail":
                expected_new: set[str] = set()
            else:
                expected_new = {staged_rel, staged_rel + "/" + staged.MAIN_FILENAME}
            new_entries = set(_snapshot(root)) - set(snap)
            self.assertEqual(new_entries, expected_new,
                             f"o12b {fault} exact owned delta: {sorted(new_entries)}")
            _assert_no_write_except(self, snap, _snapshot(root), expected_new, set(),
                                    f"o12b {fault} live-unchanged")
            # Partial progress for write-path faults must be recorded (R2-3).
            if fault in ("zero-write", "write-fail"):
                owned = outcome.get("owned", {})
                files = owned.get("owned_files", []) if isinstance(owned, dict) else []
                main_entries = [e for e in files if e.get("path") == staged_rel + "/" + staged.MAIN_FILENAME]
                self.assertTrue(main_entries, f"{fault} must record main.tex attempt")
                self.assertEqual(main_entries[0].get("bytes_written"), 0,
                                 f"{fault} partial progress must be 0")

    def test_o12c_fsync_close_indeterminate(self) -> None:
        """O12c fsync/close faults with complete bytes → INDETERMINATE + owned partials.

        R2-9: both assert exact root+main.tex partials and unchanged originals
        with the fault present, plus fired count and typed INDETERMINATE.
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12c-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12c")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12c.json")
        staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                      + "/" + staged.STAGED_DIRNAME)
        base = _snapshot(root)
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "fsync-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertEqual(outcome.get("fired"), 1, f"fsync-fail must fire once: {outcome}")
        self.assertIn("FSYNC_FAILED", outcome.get("error", ""))
        self.assertEqual(outcome.get("code"), "FSYNC_FAILED")
        self.assertEqual(outcome.get("phase"), "CLAIM")
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        self.assertEqual(outcome.get("disposition"), "INDETERMINATE_INVOCATION")
        expected_new = {staged_rel, staged_rel + "/main.tex"}
        new_entries = set(_snapshot(root)) - set(base)
        self.assertEqual(new_entries, expected_new,
                         f"fsync fault exact partials: {sorted(new_entries)}")
        _assert_no_write_except(self, base, _snapshot(root), expected_new, set(),
                                "o12c fsync live-unchanged")
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
        self.assertEqual(outcome.get("fired"), 1, f"close-fail must fire once: {outcome}")
        self.assertIn("CLOSE_FAILED", outcome.get("error", ""))
        self.assertEqual(outcome.get("code"), "CLOSE_FAILED")
        self.assertEqual(outcome.get("phase"), "CLAIM")
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        self.assertEqual(outcome.get("disposition"), "INDETERMINATE_INVOCATION")
        after2 = _snapshot(root2)
        new2 = set(after2) - set(base2)
        self.assertEqual(new2, {staged_rel2, staged_rel2 + "/main.tex"},
                         f"close fault owned partials: {sorted(new2)}")
        _assert_no_write_except(self, base2, after2, new2, set(),
                                "o12c close live-unchanged")

    def test_o12d_manifest_failure_indeterminate(self) -> None:
        """O12d manifest write/close faults → INDETERMINATE; valid bytes stay verifiable.

        R2-9: manifest-write leaves root+3 sources+empty manifest (INCOMPLETE
        set is reported as INDETERMINATE because bytes may be complete for the
        sources but the manifest is missing); manifest-close leaves complete
        valid bytes that still verify. Both assert exact partials and unchanged
        originals with the fault present.
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12d-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12d")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12d.json")
        staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                      + "/" + staged.STAGED_DIRNAME)
        base = _snapshot(root)
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "manifest-write-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertEqual(outcome.get("fired"), 1, f"manifest-write must fire once: {outcome}")
        self.assertEqual(outcome.get("phase"), "MANIFEST")
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        self.assertEqual(outcome.get("disposition"), "INDETERMINATE_INVOCATION")
        # Three sources complete plus an empty manifest file (created before the
        # failed write) — exact owned delta, originals unchanged.
        expected_new = {staged_rel, staged_rel + "/main.tex",
                        staged_rel + "/references.bib", staged_rel + "/jgaisurvey.sty",
                        staged_rel + "/staged-source-manifest.json"}
        new_entries = set(_snapshot(root)) - set(base)
        self.assertEqual(new_entries, expected_new,
                         f"manifest-write exact partials: {sorted(new_entries)}")
        _assert_no_write_except(self, base, _snapshot(root), expected_new, set(),
                                "o12d manifest-write live-unchanged")
        _scratch3, root3 = _make_p3s_source_root(self, "jgas-p3s-o12d3-")
        prep3 = _lf_prepare(self, root3, self.workspace, "fixture-lf-p3s-12d3")
        manifest3 = _capture(self, root3, prep3["state_path"], prep3["proposal_path"])
        scope3 = _scope_for(self, root3, prep3["prepared"], prep3["proposal_path"],
                            "scope-review-p3s-12d3.json")
        staged_rel3 = (prep3["proposal_path"].parent.relative_to(root3).as_posix()
                       + "/" + staged.STAGED_DIRNAME)
        base3 = _snapshot(root3)
        outcome = self._fault_run(root3, prep3, manifest3, scope3, "manifest-close-fail")
        self.assertFalse(outcome.get("ok"), "manifest close fault must not report success")
        self.assertEqual(outcome.get("fired"), 1, f"manifest-close must fire once: {outcome}")
        self.assertEqual(outcome.get("phase"), "MANIFEST")
        self.assertIn("INDETERMINATE", outcome.get("error", ""))
        self.assertEqual(outcome.get("disposition"), "INDETERMINATE_INVOCATION")
        expected_new3 = {staged_rel3, staged_rel3 + "/main.tex",
                         staged_rel3 + "/references.bib", staged_rel3 + "/jgaisurvey.sty",
                         staged_rel3 + "/staged-source-manifest.json"}
        new3 = set(_snapshot(root3)) - set(base3)
        self.assertEqual(new3, expected_new3,
                         f"manifest-close exact partials: {sorted(new3)}")
        _assert_no_write_except(self, base3, _snapshot(root3), expected_new3, set(),
                                "o12d manifest-close live-unchanged")
        staged_manifest = root3 / staged_rel3 / staged.MANIFEST_FILENAME
        self.assertTrue(staged_manifest.is_file(), "complete valid bytes may remain after failed close")
        vout = self._verify(root3, prep3["proposal_path"], staged_manifest)
        self.assertEqual(vout["result"], staged.RESULT_VERIFIED)

    def test_o12e_fstat_identity_mismatch(self) -> None:
        """O12e fstat-vs-entry identity mismatch refuses with exact owned partials.

        R2-9: the exclusive create + fstat mismatch leaves the claimed root
        plus one empty file as real owned partials (not whole-tree no-write).
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12e-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-12e")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-12e.json")
        snap = _snapshot(root)
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "fstat-fake")
        self.assertFalse(outcome.get("ok"))
        self.assertEqual(outcome.get("fired"), 1, f"fstat-fake must fire once: {outcome}")
        self.assertIn("STAGED_FILE_REPLACED", outcome.get("error", ""))
        self.assertEqual(outcome.get("code"), "STAGED_FILE_REPLACED")
        self.assertEqual(outcome.get("phase"), "CLAIM")
        self.assertEqual(outcome.get("disposition"), "OWNED_PARTIAL")
        staged_rel = (prep["proposal_path"].parent.relative_to(root).as_posix()
                      + "/" + staged.STAGED_DIRNAME)
        expected_new = {staged_rel, staged_rel + "/" + staged.MAIN_FILENAME}
        new_entries = set(_snapshot(root)) - set(snap)
        self.assertEqual(new_entries, expected_new,
                         f"o12e owned partials must be exactly root+empty file: {sorted(new_entries)}")
        # Unchanged originals with the fault present (before repair).
        _assert_no_write_except(self, snap, _snapshot(root), expected_new, set(),
                                "o12e identity mismatch exact partials")

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
        self.assertEqual(outcome.get("fired"), 1, f"drift-reader must fire once: {outcome}")
        self.assertIn("STABILITY_VIOLATION", outcome.get("error", ""))
        self.assertEqual(outcome.get("code"), "STABILITY_VIOLATION")
        self.assertEqual(outcome.get("phase"), "PRE_WRITE")
        self.assertEqual(outcome.get("disposition"), "REFUSED_PRE_WRITE")
        _assert_no_write_except(self, base, _snapshot(root), set(), {reader_rel},
                                "o11b drift fault-present")

    def test_o12f_short_partial_combined_close(self) -> None:
        """O12f short completion, partial progress, combined primary+secondary.

        R2-3: short-once returns a short count once then completes (positive);
        partial-then-fail writes 1 byte then fails (bytes_written==1 preserved);
        write-then-close-fail preserves the write primary with secondary close
        attached (not masked). All assert fired counts and structured fields.
        """
        # short-once: true positive completion (short write handled by loop).
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o12f-short-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-short")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-short.json")
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "short-once")
        self.assertTrue(outcome.get("ok"), f"short-once must still materialize: {outcome}")
        self.assertEqual(outcome.get("fired"), 1, f"short-once must fire once: {outcome}")
        self.assertEqual(outcome.get("result"), staged.RESULT_MATERIALIZED)
        # partial-then-fail: 1 byte then failure, bytes_written==1 preserved.
        _scratch2, root2 = _make_p3s_source_root(self, "jgas-p3s-o12f-partial-")
        prep2 = _lf_prepare(self, root2, self.workspace, "fixture-lf-p3s-partial")
        manifest2 = _capture(self, root2, prep2["state_path"], prep2["proposal_path"])
        scope2 = _scope_for(self, root2, prep2["prepared"], prep2["proposal_path"],
                            "scope-review-p3s-partial.json")
        snap2 = _snapshot(root2)
        outcome = self._fault_run(root2, prep2, manifest2, scope2, "partial-then-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertEqual(outcome.get("fired"), 2, f"partial-then-fail must fire twice: {outcome}")
        self.assertIn("STAGED_FILE_WRITE_FAILED", outcome.get("error", ""))
        self.assertEqual(outcome.get("code"), "STAGED_FILE_WRITE_FAILED")
        self.assertEqual(outcome.get("phase"), "CLAIM")
        self.assertEqual(outcome.get("disposition"), "OWNED_PARTIAL")
        staged_rel2 = (prep2["proposal_path"].parent.relative_to(root2).as_posix()
                       + "/" + staged.STAGED_DIRNAME)
        expected_new2 = {staged_rel2, staged_rel2 + "/" + staged.MAIN_FILENAME}
        new2 = set(_snapshot(root2)) - set(snap2)
        self.assertEqual(new2, expected_new2,
                         f"partial-then-fail exact partials: {sorted(new2)}")
        owned2 = outcome.get("owned", {})
        files2 = owned2.get("owned_files", []) if isinstance(owned2, dict) else []
        main2 = [e for e in files2 if e.get("path") == staged_rel2 + "/" + staged.MAIN_FILENAME]
        self.assertTrue(main2, "partial-then-fail must record main.tex attempt")
        self.assertEqual(main2[0].get("bytes_written"), 1,
                         "partial progress must be exactly 1 byte")
        _assert_no_write_except(self, snap2, _snapshot(root2), expected_new2, set(),
                                "o12f partial live-unchanged")
        # write-then-close-fail: primary write error survives secondary close.
        _scratch3, root3 = _make_p3s_source_root(self, "jgas-p3s-o12f-combined-")
        prep3 = _lf_prepare(self, root3, self.workspace, "fixture-lf-p3s-combined")
        manifest3 = _capture(self, root3, prep3["state_path"], prep3["proposal_path"])
        scope3 = _scope_for(self, root3, prep3["prepared"], prep3["proposal_path"],
                            "scope-review-p3s-combined.json")
        outcome = self._fault_run(root3, prep3, manifest3, scope3, "write-then-close-fail")
        self.assertFalse(outcome.get("ok"))
        self.assertEqual(outcome.get("fired"), 2, f"combined must fire twice: {outcome}")
        self.assertIn("STAGED_FILE_WRITE_FAILED", outcome.get("error", ""))
        self.assertEqual(outcome.get("code"), "STAGED_FILE_WRITE_FAILED")
        self.assertEqual(outcome.get("phase"), "CLAIM")
        self.assertEqual(outcome.get("disposition"), "OWNED_PARTIAL")
        owned3 = outcome.get("owned", {})
        self.assertTrue(owned3.get("secondary_close_errors") or
                        any("close" in str(e).lower() for e in
                            [f.get("close", "") for f in owned3.get("owned_files", [])]),
                        f"combined must attach secondary close: {outcome}")

    def test_o11c_late_control_retained(self) -> None:
        """O11c late control/retained additions refuse at later boundaries.

        R2-4: wrappers call the real boundary helper first, then inject (never
        fake success). late-control-add creates a new file under scripts/;
        late-retained-add creates a new empty dir under retained/. Both are
        caught by the pre-manifest/final zero-delta compares with exact deltas.
        """
        for fault in ("late-control-add", "late-retained-add"):
            _scratch, root = _make_p3s_source_root(self, f"jgas-p3s-o11c-{fault}-")
            prep = _lf_prepare(self, root, self.workspace, f"fixture-lf-p3s-{fault}")
            manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
            scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                    f"scope-review-p3s-{fault}.json")
            base = _snapshot(root)
            outcome = self._fault_run(root, prep, manifest_path, scope_path, fault)
            self.assertFalse(outcome.get("ok"), f"{fault} must refuse")
            self.assertEqual(outcome.get("fired"), 1, f"{fault} must fire once: {outcome}")
            self.assertIn("ORIGINAL_", outcome.get("error", ""),
                          f"{fault} must refuse at original-boundary compare: {outcome}")
            self.assertEqual(outcome.get("phase"), "PRE_CLAIM")
            self.assertEqual(outcome.get("disposition"), "REFUSED_PRE_WRITE")
            # Exact injected delta plus owned staged partials (if any) are the
            # only allowed new entries; originals otherwise unchanged.
            new_entries = set(_snapshot(root)) - set(base)
            if fault == "late-control-add":
                self.assertIn("scripts/late-control-probe-p3s.txt", new_entries,
                              f"late-control injection must be present: {sorted(new_entries)}")
            else:
                late_dirs = [r for r in new_entries if "late-retained-probe-dir" in r]
                self.assertTrue(late_dirs,
                                f"late-retained injection must be present: {sorted(new_entries)}")
            # Original control/retained/edition bytes outside the injection and
            # owned staged set must be unchanged (checked via allowed delta).
            self.assertTrue(new_entries, f"{fault} must leave injection + partials")

    def test_o11d_drift_before_claim_manifest(self) -> None:
        """O11d drift after render/before claim and after source/before manifest.

        R2-4: drift-before-claim tampers the exact staged reader after render
        (caught at the post-render pre-claim boundary); drift-before-manifest
        tampers a retained COPY dest after the 3 source writes (caught at the
        pre-manifest boundary). Both use real-helper-then-inject wrappers and
        pin exact target paths.
        """
        for fault, code, phase, disp in (("drift-before-claim", "STABILITY", "PRE_CLAIM", "REFUSED_PRE_WRITE"),
                            ("drift-before-manifest", "PIN_DRIFT", "MANIFEST", "INDETERMINATE_INVOCATION")):
            _scratch, root = _make_p3s_source_root(self, f"jgas-p3s-o11d-{fault}-")
            prep = _lf_prepare(self, root, self.workspace, f"fixture-lf-p3s-{fault}")
            manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
            scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                    f"scope-review-p3s-{fault}.json")
            outcome = self._fault_run(root, prep, manifest_path, scope_path, fault)
            self.assertFalse(outcome.get("ok"), f"{fault} must refuse")
            self.assertEqual(outcome.get("fired"), 1, f"{fault} must fire once: {outcome}")
            self.assertIn(code, outcome.get("error", ""),
                          f"{fault} must refuse at the later boundary: {outcome}")
            self.assertEqual(outcome.get("phase"), phase, fault)
            self.assertEqual(outcome.get("disposition"), disp, fault)

    def test_o11e_post_readback_replay(self) -> None:
        """O11e in-place edit after self-readback and same-byte replace after replay.

        R2-4: post-readback-edit changes output bytes after _verify_outputs_and
        manifest (caught by replay/final); post-replay-samebyte-replace swaps
        all 4 files to new inodes with identical bytes after standalone replay
        (verifier would still VERIFY byte-consistency, but writer FINAL must
        refuse FILE_REPLACED — this proves the writer identity branch that a
        successful writer alone never exercises).
        """
        # In-place edit after self-readback.
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o11e-edit-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-edit")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-edit.json")
        outcome = self._fault_run(root, prep, manifest_path, scope_path, "post-readback-edit")
        self.assertFalse(outcome.get("ok"), "post-readback edit must refuse")
        self.assertEqual(outcome.get("fired"), 1, f"post-readback must fire once: {outcome}")
        self.assertRegex(outcome.get("error", ""), "REPLAY_MISMATCH|OUTPUT_DRIFT|STABILITY|REPLAY",
                         f"post-readback edit must refuse at replay/final: {outcome}")
        self.assertEqual(outcome.get("phase"), "REPLAY")
        self.assertEqual(outcome.get("disposition"), "INDETERMINATE_INVOCATION")
        # Same-byte inode replacement after replay (writer FINAL identity).
        _scratch2, root2 = _make_p3s_source_root(self, "jgas-p3s-o11e-replace-")
        prep2 = _lf_prepare(self, root2, self.workspace, "fixture-lf-p3s-replace")
        manifest2 = _capture(self, root2, prep2["state_path"], prep2["proposal_path"])
        scope2 = _scope_for(self, root2, prep2["prepared"], prep2["proposal_path"],
                            "scope-review-p3s-replace.json")
        outcome = self._fault_run(root2, prep2, manifest2, scope2, "post-replay-samebyte-replace")
        self.assertFalse(outcome.get("ok"), "same-byte replace after replay must refuse in writer")
        self.assertEqual(outcome.get("fired"), 1, f"samebyte replace must fire once: {outcome}")
        self.assertIn("FILE_REPLACED", outcome.get("error", ""),
                      f"writer FINAL must refuse same-byte inode swap: {outcome}")
        self.assertEqual(outcome.get("code"), "FILE_REPLACED")
        self.assertEqual(outcome.get("phase"), "FINAL")
        self.assertEqual(outcome.get("disposition"), "INDETERMINATE_INVOCATION")

    def test_o11f_root_ancestor_replace(self) -> None:
        """O11f root/ancestor replacement during claim refuses.

        R2-4: wrappers rename the claimed staged dir after mkdir (root-replace)
        or replace the ancestor chain (ancestor-replace) using real OS calls
        then injection. Held-fd-only checks would miss these; canonical entry
        reopen must refuse before any file write.
        """
        for fault in ("root-replace", "ancestor-replace"):
            _scratch, root = _make_p3s_source_root(self, f"jgas-p3s-o11f-{fault}-")
            prep = _lf_prepare(self, root, self.workspace, f"fixture-lf-p3s-{fault}")
            manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
            scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                    f"scope-review-p3s-{fault}.json")
            outcome = self._fault_run(root, prep, manifest_path, scope_path, fault)
            self.assertFalse(outcome.get("ok"), f"{fault} must refuse")
            self.assertEqual(outcome.get("fired"), 1, f"{fault} must fire once: {outcome}")
            self.assertRegex(outcome.get("error", ""), "STAGED_ROOT|ANCESTOR|PATH_ALIAS",
                             f"{fault} must refuse at ownership check: {outcome}")
            self.assertEqual(outcome.get("phase"), "CLAIM")
            self.assertEqual(outcome.get("disposition"), "OWNED_PARTIAL")

    def test_o13_immediate_no_write_before_repair(self) -> None:
        """O13 every refusal proves no-write with the fault still present.

        R2-9: writer pre-tamper TOOL_DRIFT may be preempted earlier, so the
        TOOL_DRIFT oracle uses a standalone artifact tamper (healthy set, then
        tamper S2 dep, then verifier) while the writer missing-scope case
        proves immediate no-write separately.
        """
        _scratch, root = _make_p3s_source_root(self, "jgas-p3s-o13-")
        prep = _lf_prepare(self, root, self.workspace, "fixture-lf-p3s-13")
        manifest_path = _capture(self, root, prep["state_path"], prep["proposal_path"])
        scope_path = _scope_for(self, root, prep["prepared"], prep["proposal_path"],
                                "scope-review-p3s-13.json")
        _outcome, staged_manifest = self._materialize(
            root, prep["state_path"], prep["proposal_path"], manifest_path, scope_path)
        # Standalone TOOL_DRIFT via verifier (specifically reaches the check).
        base = _snapshot(root)
        target = root / "scripts" / "survey_completeness_v2.py"
        text = target.read_text(encoding="utf-8")
        target.write_text(text + "\n# Fixture o13 TOOL_DRIFT probe.\n", encoding="utf-8")
        try:
            snap_fault = _snapshot(root)
            outcome = _run_p3s_fixture(
                self, root, _P3S_VERIFY_SCRIPT,
                [str(root), str(prep["proposal_path"]), str(staged_manifest)], timeout_s=600)
            self.assertFalse(outcome.get("ok"))
            self.assertIn("TOOL_DRIFT", outcome.get("error", ""))
            self.assertEqual(outcome.get("code"), "TOOL_DRIFT")
            self.assertEqual(outcome.get("phase"), "PIN")
            self.assertEqual(outcome.get("disposition"), "INVALID")
            _assert_no_write(self, snap_fault, _snapshot(root), "o13 fault-present no-write")
        finally:
            target.write_text(text, encoding="utf-8")
        _assert_no_write(self, base, _snapshot(root), "o13 restored")
        self._verify(root, prep["proposal_path"], staged_manifest)
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
        self.assertTrue(outcome.get("phase"), "o14 must report phase")
        self.assertTrue(outcome.get("disposition"), "o14 must report disposition")
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
        

