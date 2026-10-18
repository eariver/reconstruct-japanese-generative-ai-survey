#!/usr/bin/env python3
"""P3S complete21 patch GENERATOR B2 — DRAFT (NOT EXECUTED, root readback).

B2 repairs independent pre-execution review B1/B2/B6/B7/B8 + POST-on-failure;
preserves B1 otherwise. B1 files/reports untouched.

B2 deltas vs B1 (gen_complete21_b1.py):
- B1: _check_source now enforces per-file 84-cache sha/bytes/mode (was len
  only); source-post also compares cache bytes, not only 21 files.
- B2: binary-safe patch capture — new _run_git_bytes (capture bytes, no
  text decode) for `diff --cached --binary`; text path never encodes diff.
- B6: static inputs read RAW ONCE (pinned bytes -> sha + json on same
  bytes); input_ids reuse those hashes.
- B7: pin files pass lstat alias/nlink/type refusal before first read;
  cache wrapper key "files" explicitly required (no silent {}.get).
- B8: meta holds inputs only; raw git sequence + patch sha live in
  stage-done (doc now accurate; code and doc agree).
- POST-on-failure: every failure after pre (incl. GenFailed / exception /
  KeyboardInterrupt) still attempts checked source-POST (_observe +
  _check_source incl. caches + pre/post equality + input re-hash) and
  preserves primary + secondary errors; no catch-print-return before POST.
  Refusals before outdir reservation (bad args/missing pins) still return 40
  console-only (no durable location for POST) — documented limit.
- Minors: manifest entry {sha256,bytes,mode} shape parity; parents=False;
  os.lexists gates; input re-hash detects silent post-guard changes.

Static inputs are pinned files hashed once; no silently changed manifests
post guard (re-hash at POST reports drift as secondary error).

Usage (after CoWorkerA return + root approval only):
  python3 gen_complete21_b2.py --manifest <immutable-static21.json>
    --candidate <path> --outdir <new-durable-dir>
    --scratch-root <new-or-existing-/tmp/opencode-root>
    [--cache-inventory <path>] [--p2v-expected18 <path>]
Durable: <outdir>/complete-p3s-21path.patch(.sha256), gen_complete21_b2.*
Disposable (scratch only): <scratch>/<outdir-name>-disposable-copy|-index
(absolute GIT_INDEX_FILE).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat as _stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
FIXED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
DEFAULT_CACHE_STATIC = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/cache-inventory-static.json")
DEFAULT_P2V_EXPECTED18 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json")
P1_MODULE = "scripts/survey_editorial_correction_proposal_v2.py"
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
NEW_P3S3 = sorted([
    "schemas/editorial-staged-source-manifest-v2.schema.json",
    "scripts/survey_editorial_staged_source_v2.py",
    "tests/test_survey_editorial_staged_source_v2.py",
])
NEW18 = sorted(set(NEW15_INHERITED) | set(NEW_P3S3))
CANONICAL21 = frozenset(MODIFIED3) | frozenset(NEW18)
EXPECTED_INERT_URL = "https://example.invalid/rephase-candidate-recovery.git"
EXPECTED_REMOTE_LINES = frozenset({
    "origin\t" + EXPECTED_INERT_URL + " (fetch)",
    "origin\t" + EXPECTED_INERT_URL + " (push)",
})


class GenFailed(RuntimeError):
    pass


def _git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file"})
    return env


def _run_git(cwd: Path, env: dict[str, str], *args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    resolved = str(Path(cwd).resolve())
    try:
        proc = subprocess.run(["git", "-c", "safe.directory=" + resolved, *args],
                              cwd=cwd, capture_output=True, text=True,
                              env=env, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise GenFailed("git " + " ".join(args) + " timeout") from exc
    return proc


def _run_git_bytes(cwd: Path, env: dict[str, str], *args: str, timeout: int = 60) -> tuple[int, bytes, str]:
    resolved = str(Path(cwd).resolve())
    try:
        proc = subprocess.run(["git", "-c", "safe.directory=" + resolved, *args],
                              cwd=cwd, capture_output=True, env=env, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise GenFailed("git " + " ".join(args) + " timeout") from exc
    try:
        err = proc.stderr.decode("utf-8", errors="replace")
    except Exception:
        err = "<stderr undecodable>"
    return proc.returncode, proc.stdout, err


def _require_regular(path: Path, label: str) -> None:
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise GenFailed(label + " lstat failed: " + str(path) + ": " + str(exc)) from exc
    if _stat.S_ISLNK(st.st_mode):
        raise GenFailed(label + " is symlink (alias refusal): " + str(path))
    if _stat.S_ISFIFO(st.st_mode):
        raise GenFailed(label + " is FIFO: " + str(path))
    if _stat.S_ISSOCK(st.st_mode):
        raise GenFailed(label + " is socket: " + str(path))
    if not _stat.S_ISREG(st.st_mode):
        raise GenFailed(label + " not regular: " + str(path))
    if st.st_nlink != 1:
        raise GenFailed(label + " nlink!=1: " + str(path) + " nlink=" + str(st.st_nlink))


def _pin_file_bytes(path: Path, label: str) -> bytes:
    _require_regular(path, label + " pin")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise GenFailed(label + " pin read failed: " + str(path) + ": " + str(exc)) from exc


def _load_json_once(path: Path, label: str) -> tuple[bytes, object]:
    raw = _pin_file_bytes(path, label)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GenFailed(label + " JSON parse failed: " + type(exc).__name__ + ": " + str(exc)) from exc
    return raw, parsed


def _git_entries_all(repo: Path) -> tuple[dict[str, tuple[int, int, int]], dict[str, tuple[int, int]], list[str]]:
    gitdir = repo / ".git"
    regular: dict[str, tuple[int, int, int]] = {}
    dirs: dict[str, tuple[int, int]] = {}
    problems: list[str] = []
    try:
        top = os.lstat(gitdir)
    except OSError as exc:
        raise GenFailed(".git top lstat failed: " + str(exc)) from exc
    if not _stat.S_ISDIR(top.st_mode) or _stat.S_ISLNK(top.st_mode):
        raise GenFailed(".git top is not a real directory")
    dirs["."] = (top.st_dev, top.st_ino)
    stack = [gitdir]
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(cur) as it:
                entries = sorted(it, key=lambda e: e.name)
        except OSError as exc:
            problems.append("scandir failed: " + str(cur) + ": " + str(exc))
            continue
        for entry in entries:
            try:
                rel = str(Path(entry.path).relative_to(gitdir).as_posix())
            except ValueError:
                problems.append("escapes-gitdir: " + str(entry.path))
                continue
            try:
                st = os.lstat(entry.path)
            except OSError as exc:
                problems.append("unreadable: " + rel + ": " + str(exc))
                continue
            if _stat.S_ISLNK(st.st_mode):
                problems.append("symlink: " + rel)
            elif _stat.S_ISDIR(st.st_mode):
                dirs[rel] = (st.st_dev, st.st_ino)
                stack.append(Path(entry.path))
            elif _stat.S_ISREG(st.st_mode):
                if st.st_nlink != 1:
                    problems.append("nlink!=1: " + rel + " nlink=" + str(st.st_nlink))
                else:
                    regular[rel] = (st.st_dev, st.st_ino, st.st_nlink)
            else:
                problems.append("non-regular non-dir: " + rel)
    return regular, dirs, problems


def _observe_source(candidate: Path, git_env: dict, manifest: dict, cache_static: dict, label: str) -> dict:
    procs: dict[str, subprocess.CompletedProcess] = {}
    procs["rev-parse HEAD"] = _run_git(candidate, git_env, "rev-parse", "HEAD")
    procs["rev-parse tree"] = _run_git(candidate, git_env, "rev-parse", "HEAD^{tree}")
    procs["status"] = _run_git(candidate, git_env, "status", "--porcelain=v1", "--untracked-files=all")
    procs["index"] = _run_git(candidate, git_env, "diff", "--cached", "--name-only")
    procs["diff_wt"] = _run_git(candidate, git_env, "diff", "--name-only")
    git_details: dict[str, dict] = {}
    for name, proc in procs.items():
        git_details[name] = {"rc": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        if proc.returncode != 0:
            raise GenFailed("observe " + label + ": git " + name + " rc=" + str(proc.returncode) +
                            ": " + proc.stderr.strip()[:500])
    files: dict[str, dict] = {}
    for rel in sorted(manifest.keys()):
        f = candidate / rel
        _require_regular(f, label + " source")
        data = f.read_bytes()
        files[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                      "bytes": len(data), "mode": oct(f.stat().st_mode & 0o777)}
    cache_detail: dict[str, dict] = {}
    for rel in sorted(cache_static.keys()):
        f = candidate / rel
        _require_regular(f, label + " cache")
        data = f.read_bytes()
        cache_detail[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                             "bytes": len(data), "mode": oct(f.stat().st_mode & 0o777)}
    return {"label": label, "head": procs["rev-parse HEAD"].stdout.strip(),
            "tree": procs["rev-parse tree"].stdout.strip(),
            "status_raw": procs["status"].stdout,
            "status_rows": procs["status"].stdout.splitlines(),
            "index_raw": procs["index"].stdout, "diff_wt_raw": procs["diff_wt"].stdout,
            "git_details": git_details, "files": files, "cache_detail": cache_detail}


def _check_source(obs: dict, manifest: dict, p2v_expected18: dict, cache_static: dict, where: str) -> list[str]:
    errors: list[str] = []
    if obs["head"] != FIXED_HEAD:
        errors.append(where + " HEAD mismatch: " + repr(obs["head"]))
    if obs["tree"] != FIXED_TREE:
        errors.append(where + " tree mismatch: " + repr(obs["tree"]))
    if (obs["index_raw"] or "").strip() != "":
        errors.append(where + " index non-empty")
    if set(manifest.keys()) != set(CANONICAL21):
        errors.append(where + " manifest keyset != canonical21: missing=" +
                      str(sorted(set(CANONICAL21) - set(manifest.keys()))) + " extra=" +
                      str(sorted(set(manifest.keys()) - set(CANONICAL21))))
    for rel in sorted(CANONICAL21):
        exp = manifest.get(rel)
        if exp is None:
            errors.append(where + " manifest lacks canonical path: " + rel)
            continue
        if not isinstance(exp, dict) or set(exp.keys()) != {"sha256", "bytes", "mode"}:
            errors.append(where + " manifest entry malformed: " + rel)
            continue
        got = obs["files"].get(rel, {})
        if got.get("sha256") != (exp or {}).get("sha256") or got.get("bytes") != (exp or {}).get("bytes") \
                or got.get("mode") != (exp or {}).get("mode"):
            errors.append(where + " static21 mismatch: " + rel)
    for rel in sorted(p2v_expected18.keys()):
        if manifest.get(rel) != p2v_expected18.get(rel):
            errors.append(where + " inherited18 drift vs P2V v5: " + rel)
    for rel in sorted(NEW_P3S3):
        if rel not in manifest:
            errors.append(where + " manifest lacks new P3S path: " + rel)
    if len(cache_static) != 84:
        errors.append(where + " cache static len != 84: " + str(len(cache_static)))
    for _rel, pin in cache_static.items():
        if not isinstance(pin, dict) or set(pin.keys()) != {"sha256", "bytes", "mode"}:
            errors.append(where + " cache static entry malformed: " + _rel)
            break
    for rel, pin in cache_static.items():
        got = obs.get("cache_detail", {}).get(rel, {})
        if "error" in got:
            errors.append(where + " cache unreadable/alias: " + rel + ": " + str(got["error"]))
            continue
        if got.get("sha256") != pin.get("sha256") or got.get("bytes") != pin.get("bytes") \
                or got.get("mode") != pin.get("mode"):
            errors.append(where + " cache mismatch: " + rel + ": got=" + str(got) + " exp=" + str(pin))
    expected_full = {" M " + m for m in MODIFIED3} | {"?? " + n for n in NEW18} | {"?? " + c for c in cache_static.keys()}
    if set(obs.get("status_rows", [])) != expected_full:
        errors.append(where + " full status != exact 21+84: missing=" +
                      str(sorted(expected_full - set(obs.get("status_rows", [])))[:5]) + " extra=" +
                      str(sorted(set(obs.get("status_rows", [])) - expected_full)[:5]))
    if len(obs.get("status_rows", [])) != 105:
        errors.append(where + " status len != 105")
    if len(set(obs.get("status_rows", []))) != len(obs.get("status_rows", [])):
        errors.append(where + " duplicate status rows")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="P3S B2 complete21 generator (DRAFT)")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--scratch-root", required=True, help="existing dir under /tmp/opencode for disposable DB/index")
    parser.add_argument("--cache-inventory", default=str(DEFAULT_CACHE_STATIC))
    parser.add_argument("--p2v-expected18", default=str(DEFAULT_P2V_EXPECTED18))
    args = parser.parse_args()
    manifest_p = Path(args.manifest)
    source = Path(args.candidate)
    outdir = Path(args.outdir)
    scratch_root = Path(args.scratch_root)
    cache_inv_p = Path(args.cache_inventory)
    p2r_exp_p = Path(args.p2v_expected18)
    try:
        scratch_resolved = scratch_root.resolve()
    except OSError as exc:
        print("GEN_REFUSAL: scratch-root unresolvable: " + str(exc), file=sys.stderr)
        return 40
    if str(scratch_resolved) != "/tmp/opencode" and not str(scratch_resolved).startswith("/tmp/opencode/"):
        print("GEN_REFUSAL: scratch-root must be under /tmp/opencode: " + str(scratch_root), file=sys.stderr)
        return 40
    if not scratch_root.is_dir():
        print("GEN_REFUSAL: scratch-root missing (must pre-exist under /tmp/opencode): " + str(scratch_root), file=sys.stderr)
        return 40
    if os.lexists(outdir):
        print("GEN_REFUSAL: outdir exists (not overwriting): " + str(outdir), file=sys.stderr)
        return 40
    if not os.lexists(manifest_p) or not manifest_p.is_file():
        print("GEN_REFUSAL: static manifest missing/non-regular", file=sys.stderr)
        return 40
    if not os.lexists(cache_inv_p) or not cache_inv_p.is_file():
        print("GEN_REFUSAL: static cache inventory missing/non-regular", file=sys.stderr)
        return 40
    if not os.lexists(p2r_exp_p) or not p2r_exp_p.is_file():
        print("GEN_REFUSAL: static p2v expected18 missing/non-regular", file=sys.stderr)
        return 40
    if not source.is_dir():
        print("GEN_REFUSAL: source missing: " + str(source), file=sys.stderr)
        return 40
    try:
        manifest_raw, manifest_parsed = _load_json_once(manifest_p, "manifest")
        cache_raw, cache_parsed = _load_json_once(cache_inv_p, "cache-inventory")
        p2v_raw, p2v_parsed = _load_json_once(p2r_exp_p, "p2v-expected18")
    except GenFailed as exc:
        print("GEN_REFUSAL: static pin/read failed: " + str(exc), file=sys.stderr)
        return 40
    except Exception as exc:
        print("GEN_REFUSAL: static JSON unreadable: " + str(exc), file=sys.stderr)
        return 40
    if not isinstance(manifest_parsed, dict):
        print("GEN_REFUSAL: manifest root not object", file=sys.stderr)
        return 40
    if not isinstance(cache_parsed, dict) or "files" not in cache_parsed or not isinstance(cache_parsed["files"], dict):
        print("GEN_REFUSAL: cache inventory wrapper lacks dict 'files' (no silent default)", file=sys.stderr)
        return 40
    if not isinstance(p2v_parsed, dict):
        print("GEN_REFUSAL: p2v expected18 root not object", file=sys.stderr)
        return 40
    manifest: dict = manifest_parsed
    cache_static: dict = cache_parsed["files"]
    p2v_expected18: dict = p2v_parsed
    manifest_sha = hashlib.sha256(manifest_raw).hexdigest()
    cache_sha = hashlib.sha256(cache_raw).hexdigest()
    p2v_sha = hashlib.sha256(p2v_raw).hexdigest()
    try:
        this_script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        this_script_sha = "unreadable"
    disp = (scratch_root / (outdir.name + "-disposable-copy")).resolve()
    disp_index = (scratch_root / (outdir.name + "-disposable-index")).resolve()
    if str(disp) != "/tmp/opencode" and not str(disp).startswith("/tmp/opencode/"):
        print("GEN_REFUSAL: disposable copy escapes /tmp/opencode: " + str(disp), file=sys.stderr)
        return 40
    if str(disp_index) != "/tmp/opencode" and not str(disp_index).startswith("/tmp/opencode/"):
        print("GEN_REFUSAL: disposable index escapes /tmp/opencode: " + str(disp_index), file=sys.stderr)
        return 40
    patch_p = outdir / "complete-p3s-21path.patch"
    hash_p = outdir / "complete-p3s-21path.sha256"
    meta_p = outdir / "gen_complete21_b2.meta.json"
    pre_p = outdir / "gen_complete21_b2.source-pre.json"
    post_p = outdir / "gen_complete21_b2.source-post.json"
    exit_p = outdir / "gen_complete21_b2.exit"
    done_p = outdir / "gen_complete21_b2.stage-done.json"
    stdout_p = outdir / "gen_complete21_b2.stdout.txt"
    stderr_p = outdir / "gen_complete21_b2.stderr.txt"
    terminal: dict = {"gen": "gen_complete21_b2.py", "pid": os.getpid(),
                      "gen_sha256": this_script_sha}
    wrapper_rc = 40
    out_fh = None
    err_fh = None
    log_lines: list[str] = []
    def _log(msg: str) -> None:
        log_lines.append(msg)
    try:
        outdir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        print("GEN_REFUSAL: outdir raced into existence: " + str(outdir), file=sys.stderr)
        return 40
    except OSError as exc:
        print("GEN_REFUSAL: cannot create outdir: " + str(exc), file=sys.stderr)
        return 40
    primary_error: str | None = None
    secondary_errors: list[str] = []
    pre: dict | None = None
    interrupted = False
    raw_cmds: list[dict] = []
    patch_sha: str | None = None
    patch_bytes = 0
    try:
        out_fh = open(stdout_p, "xb")
        err_fh = open(stderr_p, "xb")
        terminal.update({"started_utc": datetime.now(timezone.utc).isoformat(),
                         "argv": sys.argv, "cwd": os.getcwd(),
                         "python": sys.version, "sys_executable": sys.executable,
                         "source": str(source), "manifest": str(manifest_p),
                         "scratch_root": str(scratch_root),
                         "disposable_copy": str(disp),
                         "disposable_index": str(disp_index),
                         "input_ids": {
                             "manifest": {"sha256": manifest_sha, "bytes": len(manifest_raw)},
                             "cache_inventory": {"sha256": cache_sha, "bytes": len(cache_raw)},
                             "p2v_expected18": {"sha256": p2v_sha, "bytes": len(p2v_raw)},
                         },
                         "timeout_note": "no child; git timeout 60s each"})
        git_env = _git_env()
        terminal["forced_git"] = {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                                  "GIT_ALLOW_PROTOCOL": "file"}
        with open(meta_p, "x") as f:
            json.dump(terminal, f, indent=1)
        pre = _observe_source(source, git_env, manifest, cache_static, "source-pre")
        with open(pre_p, "x") as f:
            json.dump(pre, f, indent=1)
        pre_errors = _check_source(pre, manifest, p2v_expected18, cache_static, "source-pre")
        if pre_errors:
            primary_error = "source-pre guard failed: " + "; ".join(pre_errors)
            _log(primary_error)
        else:
            _log("source-pre 21+84 exact HEAD/tree/index/status pinned")
        if primary_error is None:
            if os.lexists(disp) or os.lexists(disp_index) or os.lexists(patch_p) or os.lexists(hash_p):
                primary_error = "disposable outputs already exist (not overwriting): copy=" + str(disp) + " index=" + str(disp_index)
                _log(primary_error)
        if primary_error is None:
            cp = subprocess.run(["cp", "-a", "--reflink=never", str(source), str(disp)],
                                capture_output=True, text=True, timeout=300)
            if cp.returncode != 0:
                primary_error = "byte-copy failed rc=" + str(cp.returncode) + ": " + cp.stderr[:1000]
                _log(primary_error)
            else:
                terminal["copy_rc"] = cp.returncode
                terminal["copy_stderr"] = cp.stderr[:1000]
        if primary_error is None:
            for rel in sorted(set(MODIFIED3) | set(NEW18)):
                c_data = (disp / rel).read_bytes() if (disp / rel).is_file() else None
                if c_data is None:
                    primary_error = "copy incomplete, missing right after byte-copy: " + rel
                    break
                try:
                    s_data = (source / rel).read_bytes()
                except OSError as exc:
                    primary_error = "source reread failed during copy check: " + rel + ": " + str(exc)
                    break
                if c_data != s_data:
                    primary_error = "copy incomplete, byte mismatch right after byte-copy: " + rel
                    break
            if primary_error is None:
                _log("copy completeness verified: all 21 present and byte-equal source")
            else:
                _log(primary_error)
        if primary_error is None:
            try:
                a_reg, a_dirs, a_prob = _git_entries_all(source)
                c_reg, c_dirs, c_prob = _git_entries_all(disp)
            except GenFailed as exc:
                primary_error = "all-entry walk failed: " + str(exc)
                _log(primary_error)
                a_reg, a_dirs, a_prob, c_reg, c_dirs, c_prob = {}, {}, ["skipped"], {}, {}, ["skipped"]
            else:
                terminal["source_git_regular"] = len(a_reg)
                terminal["source_git_dirs"] = len(a_dirs)
                terminal["copy_git_regular"] = len(c_reg)
                terminal["copy_git_dirs"] = len(c_dirs)
                if a_prob:
                    primary_error = "source .git problems: " + str(a_prob[:10])
                    _log(primary_error)
                elif c_prob:
                    primary_error = "copy .git problems: " + str(c_prob[:10])
                    _log(primary_error)
                else:
                    a_pairs = {(d, i) for (d, i, _n) in a_reg.values()} | set(a_dirs.values())
                    c_pairs = {(d, i) for (d, i, _n) in c_reg.values()} | set(c_dirs.values())
                    shared = a_pairs & c_pairs
                    if shared:
                        primary_error = "copy shares .git (dev,ino) pairs with source: " + str(sorted(shared)[:10])
                        _log(primary_error)
        if primary_error is None:
            for label, repo in (("source", source), ("copy", disp)):
                rem = _run_git(repo, git_env, "remote", "-v")
                cfg = _run_git(repo, git_env, "config", "--list", "--show-origin")
                if rem.returncode != 0 or cfg.returncode != 0:
                    primary_error = label + " remote/config rc nonzero"
                    break
                if set(rem.stdout.splitlines()) != set(EXPECTED_REMOTE_LINES):
                    primary_error = label + " remote lines != exact inert pair"
                    break
                urls = [ln.split("=", 1)[1] for ln in cfg.stdout.splitlines()
                        if ".url=" in ln and ln.split("=", 1)[0].endswith("url")]
                if not urls:
                    primary_error = label + " config has no remote url entries"
                    break
                bad = [u for u in urls if u != EXPECTED_INERT_URL]
                if bad:
                    primary_error = label + " config remote url not exact inert: " + repr(bad[0])
                    break
                alt = repo / ".git" / "objects" / "info" / "alternates"
                try:
                    alt_exists = os.lstat(alt) is not None
                except FileNotFoundError:
                    alt_exists = False
                if alt_exists:
                    primary_error = label + " has alternates"
                    break
                terminal[label + "_remote"] = rem.stdout
                terminal[label + "_config"] = cfg.stdout
            if primary_error is None:
                _log("all-entry separation + inert remote/config observed (bounded scope, whole outputs persisted)")
            else:
                _log(primary_error)
        if primary_error is None:
            denv = dict(git_env)
            denv["GIT_INDEX_FILE"] = str(disp_index)
            if os.lexists(disp_index):
                primary_error = "disposable index exists (not overwriting): " + str(disp_index)
                _log(primary_error)
            else:
                r1 = _run_git(disp, denv, "read-tree", "HEAD")
                raw_cmds.append({"cmd": ["read-tree", "HEAD"], "rc": r1.returncode, "stderr": r1.stderr[:1000]})
                if r1.returncode != 0:
                    primary_error = "disposable read-tree rc=" + str(r1.returncode) + ": " + r1.stderr[:1000]
                    _log(primary_error)
                else:
                    r2 = _run_git(disp, denv, "add", "--", *MODIFIED3, *NEW18)
                    raw_cmds.append({"cmd": ["add", "--"] + MODIFIED3 + NEW18, "rc": r2.returncode, "stderr": r2.stderr[:1000]})
                    if r2.returncode != 0:
                        primary_error = "disposable add rc=" + str(r2.returncode) + ": " + r2.stderr[:1000]
                        _log(primary_error)
                    else:
                        rc3, diff_bytes, err3 = _run_git_bytes(disp, denv, "diff", "--cached", "--binary")
                        raw_cmds.append({"cmd": ["diff", "--cached", "--binary"], "rc": rc3, "stderr": err3[:1000],
                                         "stdout_bytes": len(diff_bytes)})
                        if rc3 != 0:
                            primary_error = "disposable diff rc=" + str(rc3) + ": " + err3[:1000]
                            _log(primary_error)
                        elif len(diff_bytes) == 0:
                            primary_error = "generated patch empty (overlay missing?)"
                            _log(primary_error)
                        else:
                            try:
                                with open(patch_p, "xb") as f:
                                    f.write(diff_bytes)
                                    f.flush()
                            except OSError as exc:
                                primary_error = "patch write failed: " + type(exc).__name__ + ": " + str(exc)
                                _log(primary_error)
                            else:
                                try:
                                    patch_sha = hashlib.sha256(patch_p.read_bytes()).hexdigest()
                                    patch_bytes = patch_p.stat().st_size
                                except OSError as exc:
                                    primary_error = "patch re-hash failed: " + str(exc)
                                    _log(primary_error)
                                else:
                                    try:
                                        with open(hash_p, "x") as f:
                                            f.write(patch_sha + "  " + patch_p.name + "\n")
                                    except OSError as exc:
                                        primary_error = "hash manifest write failed: " + str(exc)
                                        _log(primary_error)
                                    else:
                                        _log("saved complete21 patch bytes=" + str(patch_bytes) + " sha=" + patch_sha[:12])
        if primary_error is not None:
            terminal["primary_error"] = primary_error
            wrapper_rc = 40
    except KeyboardInterrupt as exc:
        primary_error = "interrupted: " + type(exc).__name__ + ": " + str(exc)
        terminal["primary_error"] = primary_error
        interrupted = True
        wrapper_rc = 130
        try:
            _log(primary_error)
        except Exception:
            pass
    except GenFailed as exc:
        primary_error = "gen_failed: " + str(exc)
        terminal["primary_error"] = primary_error
        wrapper_rc = 40
        try:
            _log(primary_error)
        except Exception:
            pass
    except Exception as exc:
        primary_error = "fatal: " + type(exc).__name__ + ": " + str(exc)
        terminal["primary_error"] = primary_error
        wrapper_rc = 1
        try:
            _log(primary_error)
        except Exception:
            pass
    try:
        post_done = False
        if pre is not None:
            try:
                git_env_p = _git_env()
                post = _observe_source(source, git_env_p, manifest, cache_static, "source-post")
                try:
                    with open(post_p, "x") as f:
                        json.dump(post, f, indent=1)
                except OSError as exc:
                    secondary_errors.append("source-post write failed: " + type(exc).__name__ + ": " + str(exc))
                else:
                    post_done = True
                post_errors = _check_source(post, manifest, p2v_expected18, cache_static, "source-post")
                secondary_errors.extend(post_errors)
                if set(post.get("status_rows", [])) != set(pre.get("status_rows", [])):
                    secondary_errors.append("source changed during GEN (pre/post status differ)")
                for rel in sorted(manifest.keys()):
                    if post["files"].get(rel, {}).get("sha256") != pre["files"].get(rel, {}).get("sha256"):
                        secondary_errors.append("source file changed during GEN: " + rel)
                for rel, pin in cache_static.items():
                    if post.get("cache_detail", {}).get(rel, {}).get("sha256") != pre.get("cache_detail", {}).get(rel, {}).get("sha256"):
                        secondary_errors.append("source cache changed during GEN: " + rel)
                        break
            except GenFailed as exc:
                secondary_errors.append("source-post observe failed: " + str(exc))
            except Exception as exc:
                secondary_errors.append("source-post computation failed: " + type(exc).__name__ + ": " + str(exc))
            try:
                for label2, p2, raw0 in (("manifest", manifest_p, manifest_raw),
                                         ("cache-inventory", cache_inv_p, cache_raw),
                                         ("p2v-expected18", p2r_exp_p, p2v_raw)):
                    try:
                        cur = _pin_file_bytes(p2, "post-reverify " + label2)
                    except GenFailed as exc:
                        secondary_errors.append("post-reverify pin failed (" + label2 + "): " + str(exc))
                        continue
                    if hashlib.sha256(cur).hexdigest() != hashlib.sha256(raw0).hexdigest():
                        secondary_errors.append("static input changed post guard (" + label2 + ")")
            except Exception as exc:
                secondary_errors.append("post-reverify computation failed: " + type(exc).__name__ + ": " + str(exc))
            if not post_done and primary_error is None:
                secondary_errors.append("source-post not persisted")
            if primary_error is None and not secondary_errors:
                _log("source-post unchanged (no active objects/commits/cleanup)")
                wrapper_rc = 0
            elif primary_error is None:
                wrapper_rc = 3
        else:
            secondary_errors.append("no pre available; checked source-POST skipped (pre guard never completed)")
            if primary_error is None:
                primary_error = "no pre available"
                terminal["primary_error"] = primary_error
                wrapper_rc = 40
        terminal["secondary_errors"] = secondary_errors
        terminal["raw_git_sequence"] = raw_cmds
        terminal["disposable_index_absolute"] = str(disp_index)
        if patch_sha is not None:
            terminal["patch_sha256"] = patch_sha
            terminal["patch_bytes"] = patch_bytes
    except Exception as exc:
        secondary_errors.append("post-block fatal: " + type(exc).__name__ + ": " + str(exc))
        terminal["secondary_errors"] = secondary_errors
        if wrapper_rc == 0:
            wrapper_rc = 1
    finally:
        flush_errors: list[str] = []
        terminal["ended_utc"] = datetime.now(timezone.utc).isoformat()
        if interrupted:
            wrapper_rc = 130
        terminal["wrapper_rc"] = wrapper_rc
        try:
            if out_fh is not None and not out_fh.closed:
                out_fh.write(("\n".join(log_lines) + "\n").encode("utf-8"))
                out_fh.write(("GEN wrapper_rc=" + str(wrapper_rc) + "\n").encode("utf-8"))
                if secondary_errors:
                    out_fh.write(("GEN secondary: " + "; ".join(secondary_errors) + "\n").encode("utf-8"))
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
            print("GEN_REFUSAL: cannot record exit: " + str(exc), file=sys.stderr)
            if wrapper_rc == 0:
                wrapper_rc = 6
                terminal["wrapper_rc"] = wrapper_rc
            print("GEN_LIMIT: exit not atomically persistable with return; returned " + str(wrapper_rc) +
                  " reflects artifact failure (no overwrite repair)", file=sys.stderr)
        try:
            with open(done_p, "x") as f:
                json.dump(terminal, f, indent=1)
                f.flush()
        except OSError as exc:
            terminal["stage_done_write_error"] = type(exc).__name__ + ": " + str(exc)
            print("GEN_REFUSAL: cannot record stage-done: " + str(exc), file=sys.stderr)
            if wrapper_rc == 0:
                wrapper_rc = 6
                terminal["wrapper_rc"] = wrapper_rc
            print("GEN_LIMIT: stage-done not atomically persistable with return; returned " + str(wrapper_rc) +
                  " reflects artifact failure (no overwrite)", file=sys.stderr)
    print("gen wrapper_rc=" + str(wrapper_rc))
    return wrapper_rc


if __name__ == "__main__":
    sys.exit(main())
