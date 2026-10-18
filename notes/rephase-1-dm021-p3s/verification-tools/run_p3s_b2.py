#!/usr/bin/env python3
"""P3S runner B2 — DRAFT (NOT EXECUTED, for root readback before any long run).

B2 repairs independent pre-execution review B6/B7 + QUALs; preserves B1
otherwise. B1 files/reports untouched. Read-only refs: fixed contract
42eb8dbb, S1–S5, §7, P2V run_p2v_b4.py / proof_apply18_b4v2.py (known limits).

B2 deltas vs B1 (run_p3s_b1.py):
- B6: static inputs read RAW ONCE (pinned bytes -> sha + json.loads on same
  bytes); input_ids reuse those hashes, never a second read_bytes().
- B7: every pin file (--manifest/--cache-inventory/--p2v-expected18) passes
  lstat alias/nlink/type refusal BEFORE first read; cache wrapper key
  "files" explicitly required (no silent {}.get fallback).
- QUAL mode: _observe reuses _require_regular lstat mode/size, no second
  f.stat() for mode.
- QUAL pip: `pip freeze` inherits sanitized git_env (GIT_* stripped).
- QUAL cache-prefix: os.lexists pre + post (catches broken symlink).
- Existence gates use os.lexists (broken-symlink safe) + is_file/is_dir.
- Outdir mkdir parents=False (no unintended tree creation).
- POST re-pins static inputs and reports silent post-guard changes as
  secondary errors (no silently changed manifests).
- Runner already attempts checked finally-POST on all paths (kept).

Static assumptions (no candidate reads at authoring time; static21 NOT read
here — root concurrently corrects new3, do not treat any half-written
static21 as finalized):
- Fixed actual409 HEAD=409b292756dd1277b9dfae87679934c0d2ce251c
  tree=8ce3699861505f32d1d60bdc185d4d4f635aedb2, detached, empty index.
- Future composite 21 (3M+18A) + 84 P2R static caches = 105 rows.
- New P3S3 (subset of NEW18):
    scripts/survey_editorial_staged_source_v2.py
    schemas/editorial-staged-source-manifest-v2.schema.json
    tests/test_survey_editorial_staged_source_v2.py
- Inherited18 subset must byte-equal P2V expected18-source-correction-v5.json
  (supplied at execution via --p2v-expected18).
- Caches: 84 entries {sha256,bytes,mode}, regular non-symlink.
- Timeout default/max 18000s. No cleanup. Cache prefix absent, never mkdir'd.
- Child: python -u -m unittest, own process group, TERM->KILL on own pgid
  + reap; double-forked orphans escaping pgid are a known limit.
- No return in finally; wrapper_rc ladder preserved.

Usage (after CoWorkerA return + root approval only, different OUTDIR per run):
  python3 run_p3s_b2.py --manifest <immutable-static21.json> --candidate <path>
    --outdir <new-dir> [--cache-inventory <path>] [--p2v-expected18 <path>]
    [--timeout <s<=18000>] [-- <test selectors...>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import stat as _stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
FIXED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
DEFAULT_CACHE_STATIC = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/cache-inventory-static.json")
DEFAULT_P2V_EXPECTED18 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json")
TIMEOUT_DEFAULT = 18000
TIMEOUT_MAX = 18000
P1_MODULE = "scripts/survey_editorial_correction_proposal_v2.py"

NEW_P3S3 = sorted([
    "schemas/editorial-staged-source-manifest-v2.schema.json",
    "scripts/survey_editorial_staged_source_v2.py",
    "tests/test_survey_editorial_staged_source_v2.py",
])
MODIFIED3 = sorted([
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
])
NEW15_INHERITED = sorted([
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_current_authority_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_current_authority_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
])
NEW18 = sorted(set(NEW15_INHERITED) | set(NEW_P3S3))
CANONICAL21 = frozenset(MODIFIED3) | frozenset(NEW18)
FORCED_ENV_KEYS = ("GIT_NO_LAZY_FETCH", "GIT_OPTIONAL_LOCKS", "GIT_ALLOW_PROTOCOL",
                   "PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX", "TMPDIR")


class GuardFailed(RuntimeError):
    pass


def _git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file"})
    return env


def _child_env(cache_prefix: Path, tmpdir: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("GIT_") and k not in ("PYTHONPATH", "PYTHONHOME")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPYCACHEPREFIX": str(cache_prefix), "TMPDIR": str(tmpdir)})
    return env


def _run_git(cwd: Path, env: dict[str, str], *args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    resolved = str(Path(cwd).resolve())
    try:
        proc = subprocess.run(["git", "-c", "safe.directory=" + resolved, *args],
                              cwd=cwd, capture_output=True, text=True,
                              env=env, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise GuardFailed("git " + " ".join(args) + " timeout after " + str(timeout) + "s") from exc
    return proc


def _require_regular(path: Path, label: str) -> tuple[int, int]:
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise GuardFailed(label + " lstat failed: " + str(path) + ": " + str(exc)) from exc
    if _stat.S_ISLNK(st.st_mode):
        raise GuardFailed(label + " is symlink (alias refusal): " + str(path))
    if _stat.S_ISFIFO(st.st_mode):
        raise GuardFailed(label + " is FIFO (alias refusal): " + str(path))
    if _stat.S_ISSOCK(st.st_mode):
        raise GuardFailed(label + " is socket (alias refusal): " + str(path))
    if not _stat.S_ISREG(st.st_mode):
        raise GuardFailed(label + " is not regular file: " + str(path) + " mode=" + oct(st.st_mode))
    if st.st_nlink != 1:
        raise GuardFailed(label + " nlink!=1: " + str(path) + " nlink=" + str(st.st_nlink))
    return (st.st_mode & 0o777, st.st_size)


def _pin_file_bytes(path: Path, label: str) -> bytes:
    _require_regular(path, label + " pin")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise GuardFailed(label + " pin read failed: " + str(path) + ": " + str(exc)) from exc


def _load_json_once(path: Path, label: str) -> tuple[bytes, object]:
    raw = _pin_file_bytes(path, label)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GuardFailed(label + " JSON parse failed: " + type(exc).__name__ + ": " + str(exc)) from exc
    return raw, parsed


def _observe(candidate: Path, git_env: dict[str, str], expected_manifest: dict,
             cache_static: dict, label: str) -> dict:
    procs: dict[str, subprocess.CompletedProcess] = {}
    procs["rev-parse HEAD"] = _run_git(candidate, git_env, "rev-parse", "HEAD")
    procs["rev-parse tree"] = _run_git(candidate, git_env, "rev-parse", "HEAD^{tree}")
    procs["status"] = _run_git(candidate, git_env, "status", "--porcelain=v1", "--untracked-files=all")
    procs["index"] = _run_git(candidate, git_env, "diff", "--cached", "--name-only")
    procs["diff_wt"] = _run_git(candidate, git_env, "diff", "--name-only")
    git_details: dict[str, dict] = {}
    for name, proc in procs.items():
        git_details[name] = {"rc": proc.returncode, "stdout": proc.stdout,
                             "stderr": proc.stderr}
        if proc.returncode != 0:
            raise GuardFailed("observe " + label + ": git " + name + " rc=" +
                              str(proc.returncode) + ": " + proc.stderr.strip()[:500])
    head = procs["rev-parse HEAD"].stdout.strip()
    tree = procs["rev-parse tree"].stdout.strip()
    status_raw = procs["status"].stdout
    index_raw = procs["index"].stdout
    diff_wt_raw = procs["diff_wt"].stdout
    status_rows = status_raw.splitlines()
    files: dict[str, dict] = {}
    for rel in sorted(expected_manifest.keys()):
        f = candidate / rel
        try:
            mode, _size = _require_regular(f, label + " source")
        except GuardFailed as exc:
            files[rel] = {"error": str(exc)}
            continue
        try:
            data = f.read_bytes()
        except OSError as exc:
            files[rel] = {"error": "read failed: " + str(exc)}
            continue
        files[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                      "bytes": len(data), "mode": oct(mode)}
    cache_detail: dict[str, dict] = {}
    for rel in sorted(cache_static.keys()):
        f = candidate / rel
        try:
            cmode, _csize = _require_regular(f, label + " cache")
        except GuardFailed as exc:
            cache_detail[rel] = {"error": str(exc)}
            continue
        try:
            data = f.read_bytes()
        except OSError as exc:
            cache_detail[rel] = {"error": "read failed: " + str(exc)}
            continue
        cache_detail[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                             "bytes": len(data), "mode": oct(cmode)}
    return {"label": label, "head": head, "tree": tree, "status_raw": status_raw,
            "status_rows": status_rows, "index_raw": index_raw,
            "diff_wt_raw": diff_wt_raw, "git_details": git_details,
            "files": files, "cache_detail": cache_detail}


def _check_pins(obs: dict, expected_manifest: dict, p2v_expected18: dict,
                cache_static: dict, where: str) -> list[str]:
    errors: list[str] = []
    if obs["head"] != FIXED_HEAD:
        errors.append(where + " HEAD mismatch: " + repr(obs["head"]))
    if obs["tree"] != FIXED_TREE:
        errors.append(where + " tree mismatch: " + repr(obs["tree"]))
    if (obs["index_raw"] or "").strip() != "":
        errors.append(where + " index non-empty: " + repr(obs["index_raw"][:500]))
    if set(expected_manifest.keys()) != set(CANONICAL21):
        errors.append(where + " manifest keyset != canonical21: missing=" +
                      str(sorted(set(CANONICAL21) - set(expected_manifest.keys()))) +
                      " extra=" + str(sorted(set(expected_manifest.keys()) - set(CANONICAL21))))
    if set(MODIFIED3) | set(NEW18) != set(CANONICAL21):
        errors.append(where + " internal MODIFIED3+NEW18 != canonical21 (tool defect)")
    if set(NEW_P3S3) - set(NEW18):
        errors.append(where + " internal NEW_P3S3 not subset of NEW18 (tool defect)")
    if len(NEW18) != 18:
        errors.append(where + " internal NEW18 len " + str(len(NEW18)) + " != 18 (tool defect)")
    for rel in sorted(CANONICAL21):
        exp = expected_manifest.get(rel)
        if exp is None:
            errors.append(where + " manifest lacks canonical path: " + rel)
            continue
        if set(exp.keys()) != {"sha256", "bytes", "mode"}:
            errors.append(where + " manifest entry malformed: " + rel + ": " + str(sorted(exp.keys())))
            continue
        got = obs["files"].get(rel, {})
        if "error" in got:
            errors.append(where + " source unreadable/alias: " + rel + ": " + str(got["error"]))
            continue
        if got.get("sha256") != exp.get("sha256") or got.get("bytes") != exp.get("bytes") \
                or got.get("mode") != exp.get("mode"):
            errors.append(where + " static21 mismatch: " + rel + ": got=" + str(got) + " exp=" + str(exp))
    for rel in sorted(p2v_expected18.keys()):
        exp = p2v_expected18.get(rel)
        got_manifest = expected_manifest.get(rel)
        if got_manifest != exp:
            errors.append(where + " inherited18 drift vs P2V v5 (must stay byte-identical): " + rel +
                          ": static21=" + str(got_manifest) + " p2v=" + str(exp))
        got_obs = obs["files"].get(rel, {})
        if "error" not in got_obs:
            if got_obs.get("sha256") != exp.get("sha256") or got_obs.get("bytes") != exp.get("bytes") \
                    or got_obs.get("mode") != exp.get("mode"):
                errors.append(where + " inherited18 live drift: " + rel + ": got=" + str(got_obs))
    if P1_MODULE not in expected_manifest:
        errors.append(where + " manifest lacks P1 module (tool defect): " + P1_MODULE)
    for rel in sorted(NEW_P3S3):
        if rel not in expected_manifest:
            errors.append(where + " manifest lacks new P3S path: " + rel)
    if len(cache_static) != 84:
        errors.append(where + " cache static len " + str(len(cache_static)) + " != 84")
    for rel, pin in cache_static.items():
        if set(pin.keys()) != {"sha256", "bytes", "mode"}:
            errors.append(where + " cache static entry malformed: " + rel)
            break
    for rel, pin in cache_static.items():
        got = obs["cache_detail"].get(rel, {})
        if "error" in got:
            errors.append(where + " cache unreadable/alias: " + rel + ": " + str(got["error"]))
            continue
        if got.get("sha256") != pin.get("sha256") or got.get("bytes") != pin.get("bytes") \
                or got.get("mode") != pin.get("mode"):
            errors.append(where + " cache mismatch: " + rel + ": got=" + str(got) + " exp=" + str(pin))
    rows = obs.get("status_rows", [])
    if len(rows) != 105:
        errors.append(where + " full status rows len " + str(len(rows)) + " != 105 (21+84)")
    if len(set(rows)) != len(rows):
        errors.append(where + " duplicate status rows present")
    expected_source_rows = {" M " + m for m in MODIFIED3} | {"?? " + n for n in NEW18}
    expected_cache_rows = {"?? " + rel for rel in cache_static.keys()}
    expected_full = expected_source_rows | expected_cache_rows
    if len(expected_full) != 105:
        errors.append(where + " internal expected full set len " + str(len(expected_full)) + " != 105 (tool defect)")
    if set(rows) != expected_full:
        errors.append(where + " full status != exact 21+84 rows: missing=" +
                      str(sorted(expected_full - set(rows))[:10]) + " extra=" +
                      str(sorted(set(rows) - expected_full)[:10]))
    return errors


def _kill_reap(proc: subprocess.Popen, terminal: dict, how: str) -> None:
    pgid = proc.pid
    terminal[how + "_pgid"] = "own session pgid=pid " + str(pgid) + " (start_new_session=True; signals only own session; double-forked orphans escaping pgid are a known limit, not claimed reaped)"
    try:
        os.killpg(pgid, signal.SIGTERM)
        terminal[how + "_sigterm"] = "sent to pgid " + str(pgid)
    except ProcessLookupError:
        terminal[how + "_sigterm"] = "already-exited"
    except OSError as exc:
        terminal[how + "_sigterm"] = "failed: " + type(exc).__name__ + ": " + str(exc)
    try:
        proc.wait(timeout=120)
        terminal[how + "_reap_term"] = "rc=" + str(proc.returncode)
        return
    except subprocess.SubprocessError:
        pass
    except Exception as exc:
        terminal[how + "_reap_term"] = "failed: " + type(exc).__name__ + ": " + str(exc)
    try:
        os.killpg(pgid, signal.SIGKILL)
        terminal[how + "_sigkill"] = "sent to pgid " + str(pgid)
    except ProcessLookupError:
        terminal[how + "_sigkill"] = "already-exited"
    except OSError as exc:
        terminal[how + "_sigkill"] = "failed: " + type(exc).__name__ + ": " + str(exc)
    try:
        proc.wait(timeout=120)
        terminal[how + "_reap_kill"] = "rc=" + str(proc.returncode)
    except Exception as exc:
        terminal[how + "_reap_kill"] = "failed: " + type(exc).__name__ + ": " + str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="P3S B2 runner (DRAFT, root readback required)")
    parser.add_argument("--manifest", required=True, help="immutable static21 JSON path (supplied after CoWorkerA return)")
    parser.add_argument("--candidate", required=True, help="candidate worktree path (supplied after CoWorkerA return)")
    parser.add_argument("--outdir", required=True, help="new output dir (must not exist; use different OUTDIR per smoke/full)")
    parser.add_argument("--cache-inventory", default=str(DEFAULT_CACHE_STATIC))
    parser.add_argument("--p2v-expected18", default=str(DEFAULT_P2V_EXPECTED18))
    parser.add_argument("--timeout", type=int, default=TIMEOUT_DEFAULT)
    parser.add_argument("tests", nargs="*", help="explicit unittest selectors (default full P3S test module)")
    args = parser.parse_args()
    manifest_p = Path(args.manifest)
    outdir = Path(args.outdir)
    candidate = Path(args.candidate)
    cache_inv_p = Path(args.cache_inventory)
    p2v_exp_p = Path(args.p2v_expected18)
    timeout_s = int(args.timeout)
    if timeout_s <= 0 or timeout_s > TIMEOUT_MAX:
        print("RUNNER_REFUSAL: timeout must be 1.." + str(TIMEOUT_MAX) + ", got " + str(timeout_s), file=sys.stderr)
        return 40
    if not os.lexists(manifest_p) or not manifest_p.is_file():
        print("RUNNER_REFUSAL: manifest missing/non-regular: " + str(manifest_p), file=sys.stderr)
        return 40
    if not os.lexists(cache_inv_p) or not cache_inv_p.is_file():
        print("RUNNER_REFUSAL: cache inventory missing/non-regular: " + str(cache_inv_p), file=sys.stderr)
        return 40
    if not os.lexists(p2v_exp_p) or not p2v_exp_p.is_file():
        print("RUNNER_REFUSAL: p2v expected18 missing/non-regular: " + str(p2v_exp_p), file=sys.stderr)
        return 40
    if os.lexists(outdir):
        print("RUNNER_REFUSAL: outdir exists (not overwriting, use different OUTDIR version): " + str(outdir), file=sys.stderr)
        return 40
    tmpdir = Path("/tmp/opencode") / (outdir.name + "-tmpdir")
    cache_prefix = Path("/tmp/opencode") / (outdir.name + "-nocache-absent")
    if os.lexists(tmpdir):
        print("RUNNER_REFUSAL: own TMPDIR exists: " + str(tmpdir), file=sys.stderr)
        return 40
    if os.lexists(cache_prefix):
        print("RUNNER_REFUSAL: cache prefix exists (must stay absent, never mkdir'd): " + str(cache_prefix), file=sys.stderr)
        return 40
    if not candidate.is_dir():
        print("RUNNER_REFUSAL: candidate missing: " + str(candidate), file=sys.stderr)
        return 40
    try:
        this_script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        this_script_sha = "unreadable"
    try:
        manifest_raw, manifest_parsed = _load_json_once(manifest_p, "manifest")
        cache_raw, cache_parsed = _load_json_once(cache_inv_p, "cache-inventory")
        p2v_raw, p2v_parsed = _load_json_once(p2v_exp_p, "p2v-expected18")
    except GuardFailed as exc:
        print("RUNNER_REFUSAL: static pin/read failed: " + str(exc), file=sys.stderr)
        return 40
    except Exception as exc:
        print("RUNNER_REFUSAL: static JSON unreadable: " + type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 40
    if not isinstance(manifest_parsed, dict):
        print("RUNNER_REFUSAL: manifest root not object", file=sys.stderr)
        return 40
    if not isinstance(cache_parsed, dict) or "files" not in cache_parsed or not isinstance(cache_parsed["files"], dict):
        print("RUNNER_REFUSAL: cache inventory wrapper lacks dict 'files' (no silent default)", file=sys.stderr)
        return 40
    if not isinstance(p2v_parsed, dict):
        print("RUNNER_REFUSAL: p2v expected18 root not object", file=sys.stderr)
        return 40
    expected_manifest = manifest_parsed
    cache_static = cache_parsed["files"]
    p2v_expected18 = p2v_parsed
    manifest_sha = hashlib.sha256(manifest_raw).hexdigest()
    cache_sha = hashlib.sha256(cache_raw).hexdigest()
    p2v_sha = hashlib.sha256(p2v_raw).hexdigest()
    stdout_p = outdir / "run_p3s_b2.stdout.txt"
    stderr_p = outdir / "run_p3s_b2.stderr.txt"
    exit_p = outdir / "run_p3s_b2.exit"
    pre_p = outdir / "run_p3s_b2.pre.json"
    post_p = outdir / "run_p3s_b2.post.json"
    meta_p = outdir / "run_p3s_b2.meta.json"
    stage_reserved_p = outdir / "run_p3s_b2.stage-reserved.json"
    stage_running_p = outdir / "run_p3s_b2.stage-running.json"
    stage_done_p = outdir / "run_p3s_b2.stage-done.json"
    terminal: dict = {"runner": "run_p3s_b2.py", "pid": os.getpid(),
                      "runner_sha256": this_script_sha}
    out_fh = None
    err_fh = None
    proc: subprocess.Popen | None = None
    child_rc: int | None = None
    pre: dict | None = None
    wrapper_rc = 40
    post_errors: list[str] = []
    try:
        outdir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        print("RUNNER_REFUSAL: outdir raced into existence: " + str(outdir), file=sys.stderr)
        return 40
    except OSError as exc:
        print("RUNNER_REFUSAL: cannot create outdir: " + str(exc), file=sys.stderr)
        return 40
    try:
        try:
            tmpdir.mkdir(parents=False, exist_ok=False)
        except FileExistsError as exc:
            raise GuardFailed("own TMPDIR raced into existence: " + str(tmpdir)) from exc
        out_fh = open(stdout_p, "xb")
        err_fh = open(stderr_p, "xb")
        started = datetime.now(timezone.utc)
        terminal.update({"started_utc": started.isoformat(), "candidate": str(candidate),
                         "manifest": str(manifest_p), "cache_inventory": str(cache_inv_p),
                         "p2v_expected18": str(p2v_exp_p), "timeout_s": timeout_s,
                         "argv": sys.argv, "cwd": os.getcwd(),
                         "python": sys.version, "sys_executable": sys.executable,
                         "cache_prefix": str(cache_prefix), "tmpdir": str(tmpdir),
                         "phase": "reserved"})
        with open(stage_reserved_p, "x") as f:
            json.dump(terminal, f, indent=1)
        child_env = _child_env(cache_prefix, tmpdir)
        forced = {k: child_env.get(k) for k in FORCED_ENV_KEYS}
        redacted = len(child_env) - len([k for k in child_env if k in FORCED_ENV_KEYS])
        git_env = _git_env()
        meta: dict = dict(terminal)
        meta["forced_env"] = forced
        meta["env_other_withheld"] = "redacted (" + str(redacted) + " additional inherited keys withheld, no values persisted)"
        meta["requested_tests"] = list(args.tests) if args.tests else []
        meta["input_ids"] = {
            "manifest": {"path": str(manifest_p), "sha256": manifest_sha, "bytes": len(manifest_raw)},
            "cache_inventory": {"path": str(cache_inv_p), "sha256": cache_sha, "bytes": len(cache_raw)},
            "p2v_expected18": {"path": str(p2v_exp_p), "sha256": p2v_sha, "bytes": len(p2v_raw)},
        }
        try:
            import unittest  # noqa
            meta["unittest"] = "available"
        except Exception as exc:
            meta["unittest"] = type(exc).__name__ + ": " + str(exc)
        try:
            pip = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                                 capture_output=True, text=True, timeout=60,
                                 env=git_env)
            meta["pip_freeze_rc"] = pip.returncode
            meta["pip_freeze"] = pip.stdout[:6000]
            meta["pip_freeze_stderr"] = pip.stderr[:1000]
        except Exception as exc:
            meta["pip_freeze_error"] = type(exc).__name__ + ": " + str(exc)
        with open(meta_p, "x") as f:
            json.dump(meta, f, indent=1)
        pre = _observe(candidate, git_env, expected_manifest, cache_static, "pre")
        with open(pre_p, "x") as f:
            json.dump(pre, f, indent=1)
        pre_errors = _check_pins(pre, expected_manifest, p2v_expected18, cache_static, "pre")
        if pre_errors:
            terminal["pre_errors"] = pre_errors
            msg = "PRE-GUARD FAILED:\n" + "\n".join(pre_errors) + "\n"
            out_fh.write(msg.encode())
            out_fh.flush()
            err_fh.write(msg.encode())
            err_fh.flush()
        else:
            selectors = list(args.tests) if args.tests else ["tests.test_survey_editorial_staged_source_v2"]
            cmd = [sys.executable, "-u", "-m", "unittest", *selectors, "-v"]
            t0 = datetime.now(timezone.utc)
            proc = subprocess.Popen(cmd, cwd=candidate, stdout=out_fh, stderr=err_fh,
                                    env=child_env, start_new_session=True)
            with open(stage_running_p, "x") as f:
                json.dump({"phase": "child-running", "child_pid": proc.pid,
                           "child_cmd": cmd, "child_cwd": str(candidate),
                           "sys_executable": sys.executable,
                           "child_env_forced": forced,
                           "child_env_other": "redacted (" + str(redacted) + " additional inherited keys withheld)",
                           "started_utc": t0.isoformat(),
                           "tmpdir": str(tmpdir), "cache_prefix": str(cache_prefix),
                           "orphan_limit": "pgid kill covers own session only; double-forked orphans escaping pgid are not claimed reaped"}, f, indent=1)
            print("b2 child pid=" + str(proc.pid) + " group=" + str(proc.pid) +
                  " redirected to " + stdout_p.name + " " + stderr_p.name, flush=True)
            try:
                child_rc = proc.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                terminal["timed_out"] = True
                _kill_reap(proc, terminal, "timeout")
                child_rc = proc.returncode if proc.returncode is not None else 124
            terminal["child_rc"] = child_rc
            terminal["elapsed_s"] = (datetime.now(timezone.utc) - t0).total_seconds()
    except KeyboardInterrupt as exc:
        terminal["interrupted"] = type(exc).__name__ + ": " + str(exc)
        if proc is not None:
            _kill_reap(proc, terminal, "interrupt")
            child_rc = proc.returncode if proc.returncode is not None else 130
            terminal["child_rc"] = child_rc
    except GuardFailed as exc:
        terminal["guard_failed"] = str(exc)
        terminal["launch_rc"] = 2
        if proc is not None and child_rc is None:
            _kill_reap(proc, terminal, "launch-failure")
            child_rc = proc.returncode
            terminal["child_rc"] = child_rc
    except RuntimeError as exc:
        terminal["runtime_error"] = type(exc).__name__ + ": " + str(exc)
        terminal["launch_rc"] = 2
        if proc is not None and child_rc is None:
            _kill_reap(proc, terminal, "launch-failure")
            child_rc = proc.returncode
            terminal["child_rc"] = child_rc
    except Exception as exc:
        terminal["fatal"] = type(exc).__name__ + ": " + str(exc)
        terminal["launch_rc"] = 1
        if proc is not None and child_rc is None:
            _kill_reap(proc, terminal, "launch-failure")
            child_rc = proc.returncode
            terminal["child_rc"] = child_rc
    finally:
        try:
            git_env2 = _git_env()
            post = _observe(candidate, git_env2, expected_manifest, cache_static, "finally-post")
            post_ok = True
        except GuardFailed as exc:
            post = {"label": "finally-post", "observe_error": type(exc).__name__ + ": " + str(exc)}
            post_ok = False
        except Exception as exc:
            post = {"label": "finally-post", "observe_error": type(exc).__name__ + ": " + str(exc)}
            post_ok = False
        try:
            with open(post_p, "x") as f:
                json.dump(post, f, indent=1)
        except OSError as exc:
            terminal["post_write_error"] = type(exc).__name__ + ": " + str(exc)
            post_ok = False
        post_errors = []
        if not post_ok:
            post_errors.append("post observation failed: " + str(post.get("observe_error", post.get("post_write_error"))))
        else:
            try:
                post_errors = _check_pins(post, expected_manifest, p2v_expected18, cache_static, "post")
                if pre is not None and isinstance(pre.get("status_rows"), list) and isinstance(post.get("status_rows"), list):
                    if set(post.get("status_rows", [])) != set(pre.get("status_rows", [])):
                        post_errors.append("post full status rows differ from pre")
                if os.lexists(cache_prefix):
                    post_errors.append("cache prefix appeared during run (bytecode write unexpected): " + str(cache_prefix))
            except Exception as exc:
                post_errors.append("post guard computation failed: " + type(exc).__name__ + ": " + str(exc))
        try:
            for label2, p2, raw0 in (("manifest", manifest_p, manifest_raw),
                                     ("cache-inventory", cache_inv_p, cache_raw),
                                     ("p2v-expected18", p2v_exp_p, p2v_raw)):
                try:
                    cur = _pin_file_bytes(p2, "post-reverify " + label2)
                except GuardFailed as exc:
                    post_errors.append("post-reverify pin failed (" + label2 + "): " + str(exc))
                    continue
                if hashlib.sha256(cur).hexdigest() != hashlib.sha256(raw0).hexdigest():
                    post_errors.append("static input changed post guard (" + label2 + "): sha differs from pre-guard pin")
        except Exception as exc:
            post_errors.append("post-reverify computation failed: " + type(exc).__name__ + ": " + str(exc))
        flush_errors: list[str] = []
        if terminal.get("interrupted"):
            wrapper_rc = 130
        elif terminal.get("timed_out"):
            wrapper_rc = 124
        elif terminal.get("launch_rc") is not None:
            wrapper_rc = int(terminal["launch_rc"])
        elif terminal.get("pre_errors"):
            wrapper_rc = 2
        elif terminal.get("guard_failed"):
            wrapper_rc = 2
        elif proc is not None and child_rc is None:
            terminal["note"] = "child launched but never reported rc"
            wrapper_rc = 1
        elif proc is None and child_rc is None and not terminal.get("pre_errors") \
                and terminal.get("launch_rc") is None and not terminal.get("guard_failed"):
            terminal["note"] = "no child, no pre-errors, no launch error recorded"
            wrapper_rc = 1
        elif child_rc is not None and child_rc != 0:
            wrapper_rc = int(child_rc)
        else:
            wrapper_rc = 0
        terminal["wrapper_rc"] = wrapper_rc
        terminal["post_errors"] = post_errors
        if post_errors and wrapper_rc == 0:
            wrapper_rc = 3
            terminal["wrapper_rc"] = wrapper_rc
        terminal["ended_utc"] = datetime.now(timezone.utc).isoformat()
        try:
            if out_fh is not None and not out_fh.closed:
                out_fh.write(("\n[WRAPPER child_rc=" + str(child_rc) + " wrapper_rc=" + str(wrapper_rc) +
                               " timed_out=" + str(bool(terminal.get("timed_out"))) +
                               " interrupted=" + str(bool(terminal.get("interrupted"))) + "]\n").encode())
                if post_errors:
                    out_fh.write(("POST-GUARD: " + "; ".join(post_errors) + "\n").encode())
                out_fh.flush()
        except (OSError, ValueError) as exc:
            terminal["trailer_write_error"] = type(exc).__name__ + ": " + str(exc)
            if wrapper_rc == 0:
                wrapper_rc = 5
                terminal["wrapper_rc"] = wrapper_rc
        for fh, name in ((out_fh, "stdout"), (err_fh, "stderr")):
            if fh is not None and not fh.closed:
                try:
                    fh.flush()
                except (OSError, ValueError) as exc:
                    flush_errors.append(name + " flush: " + type(exc).__name__ + ": " + str(exc))
                try:
                    fh.close()
                except (OSError, ValueError) as exc:
                    flush_errors.append(name + " close: " + type(exc).__name__ + ": " + str(exc))
        if flush_errors:
            terminal["flush_errors"] = flush_errors
            if wrapper_rc == 0:
                wrapper_rc = 5
                terminal["wrapper_rc"] = wrapper_rc
        try:
            with open(exit_p, "x") as f:
                f.write(str(wrapper_rc) + "\n")
                f.flush()
        except OSError as exc:
            terminal["exit_write_error"] = type(exc).__name__ + ": " + str(exc)
            print("RUNNER_REFUSAL: cannot record " + exit_p.name + ": " + str(exc), file=sys.stderr)
            if wrapper_rc == 0:
                wrapper_rc = 6
                terminal["wrapper_rc"] = wrapper_rc
            print("RUNNER_LIMIT: exit record failed; returning " + str(wrapper_rc) +
                  " without overwriting existing exit (no repair attempt)", file=sys.stderr)
        try:
            with open(stage_done_p, "x") as f:
                json.dump(terminal, f, indent=1)
                f.flush()
        except OSError as exc:
            terminal["stage_done_write_error"] = type(exc).__name__ + ": " + str(exc)
            print("RUNNER_REFUSAL: cannot record stage-done: " + str(exc) + "; terminal=" +
                  json.dumps(terminal)[:2000], file=sys.stderr)
            if wrapper_rc == 0:
                wrapper_rc = 6
                terminal["wrapper_rc"] = wrapper_rc
            print("RUNNER_LIMIT: stage-done not atomically persistable with return; " +
                  "returned " + str(wrapper_rc) + " reflects artifact failure (no overwrite)", file=sys.stderr)
    print("child_rc=" + str(child_rc) + " wrapper_rc=" + str(wrapper_rc) + " post_errors=" + str(post_errors))
    return wrapper_rc


if __name__ == "__main__":
    sys.exit(main())
