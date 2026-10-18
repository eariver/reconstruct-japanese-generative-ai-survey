#!/usr/bin/env python3
"""P3S saved-patch apply PROOF B3 — DRAFT (NOT EXECUTED, root readback).

B3 repairs B2 smoke fatal (os.lexists has no such attribute; every gate now
uses os.path.lexists) + adds actual detached-HEAD guard (symbolic-ref -q
HEAD rc==1 expected, active freeze AND source-post) + canonical exact
inherited18 keyset check (not arbitrary supplied map). Preserves B1/B2
bytes/reports (untouched).

B2 deltas vs B1 (proof_apply21_b1.py):
- B3: --patch/--patch-hash resolved to ABSOLUTE paths immediately after arg
  parse; `git apply` receives absolute saved-patch path (relative cwd bug
  fixed); pinned raw bytes hashed once and reused.
- B4: full recorded cache removal in disposable ONLY — inventoried
  __pycache__/* regular files unlinked individually (lstat alias-checked)
  plus top-level *.pyc unlinked; __pycache__ dirs removed only after file
  removal; removal confined to copyrepo (prefix-checked); survivors fail.
- B5: KeyboardInterrupt path added (primary 130, still attempts checked
  source-POST, handles always closed via single _emit).
- B6: static inputs read RAW ONCE (pinned bytes -> sha + json on same
  bytes; patch bytes hashed once; hash file decoded once).
- B7: pin files pass lstat alias/nlink/type refusal before first read;
  cache wrapper key "files" explicitly required.
- POST-on-failure: every failure after active freeze (incl. exception /
  interrupt) still attempts checked source-POST (_freeze_full + per-file
  sha vs active + input re-hash) and preserves primary + secondary errors;
  no catch-print-return before POST. Refusals before outdir reservation
  return 40 console-only (no durable location) — documented limit.
- Minors: single shebang; hoisted hashlib (no inner import); started_utc /
  ended_utc / elapsed_s parity; parents=False; os.path.lexists gates.

Consumes ONLY SAVED complete21 patch + hash manifest + static21. New
independent byte-copied DB/worktree under REQUIRED /tmp/opencode scratch
root. No notes nested DBs, no archive/fakeRoot/borrowedGit. Clean freeze
never reads removed NEW bytes (absence only). One-off tool, not generic
certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat as _stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
FIXED_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
EXPECTED_INERT_URL = "https://example.invalid/rephase-candidate-recovery.git"
EXPECTED_REMOTE_LINES = frozenset({
    "origin\t" + EXPECTED_INERT_URL + " (fetch)",
    "origin\t" + EXPECTED_INERT_URL + " (push)",
})
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
INHERITED18 = frozenset(MODIFIED3) | frozenset(NEW15_INHERITED)
EXPECTED_STATUS21 = frozenset({" M " + m for m in MODIFIED3} | {"?? " + n for n in NEW18})


class ProofFailed(RuntimeError):
    pass


def _git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file"})
    return env


def _git(repo: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess:
    resolved = str(Path(repo).resolve())
    try:
        proc = subprocess.run(["git", "-c", "safe.directory=" + resolved, *args],
                              cwd=repo, capture_output=True, text=True,
                              env=env, timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise ProofFailed("git " + " ".join(args) + " timeout") from exc
    return proc


def _git_checked(repo: Path, env: dict[str, str], *args: str) -> str:
    proc = _git(repo, env, *args)
    if proc.returncode != 0:
        raise ProofFailed("git " + " ".join(args) + " rc=" + str(proc.returncode) +
                          ": " + proc.stderr.strip()[:1000])
    return proc.stdout


def _check_detached(repo: Path, env: dict[str, str], label: str) -> tuple[int, str, str]:
    proc = _git(repo, env, "symbolic-ref", "-q", "HEAD")
    if proc.returncode not in (0, 1):
        raise ProofFailed(label + " symbolic-ref rc=" + str(proc.returncode) +
                          " (expected 0 attached or 1 detached): " + proc.stderr.strip()[:500])
    return proc.returncode, proc.stdout, proc.stderr


def _require_regular(path: Path, label: str) -> None:
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise ProofFailed(label + " lstat failed: " + str(path) + ": " + str(exc)) from exc
    if _stat.S_ISLNK(st.st_mode):
        raise ProofFailed(label + " is symlink (alias refusal): " + str(path))
    if _stat.S_ISFIFO(st.st_mode):
        raise ProofFailed(label + " is FIFO: " + str(path))
    if _stat.S_ISSOCK(st.st_mode):
        raise ProofFailed(label + " is socket: " + str(path))
    if not _stat.S_ISREG(st.st_mode):
        raise ProofFailed(label + " not regular: " + str(path) + " mode=" + oct(st.st_mode))
    if st.st_nlink != 1:
        raise ProofFailed(label + " nlink!=1: " + str(path) + " nlink=" + str(st.st_nlink))


def _pin_file_bytes(path: Path, label: str) -> bytes:
    _require_regular(path, label + " pin")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ProofFailed(label + " pin read failed: " + str(path) + ": " + str(exc)) from exc


def _load_json_once(path: Path, label: str) -> tuple[bytes, object]:
    raw = _pin_file_bytes(path, label)
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProofFailed(label + " JSON parse failed: " + type(exc).__name__ + ": " + str(exc)) from exc
    return raw, parsed


def _git_entries_all(repo: Path) -> tuple[dict[str, tuple[int, int, int]], dict[str, tuple[int, int]], list[str]]:
    gitdir = repo / ".git"
    regular: dict[str, tuple[int, int, int]] = {}
    dirs: dict[str, tuple[int, int]] = {}
    problems: list[str] = []
    try:
        top = os.lstat(gitdir)
    except OSError as exc:
        raise ProofFailed(".git top lstat failed: " + str(exc)) from exc
    if not _stat.S_ISDIR(top.st_mode) or _stat.S_ISLNK(top.st_mode):
        raise ProofFailed(".git top is not a real directory")
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


def _check_remote_config(repo: Path, env: dict[str, str], label: str) -> tuple[str, str]:
    rem = _git(repo, env, "remote", "-v")
    cfg = _git(repo, env, "config", "--list", "--show-origin")
    if rem.returncode != 0:
        raise ProofFailed(label + " remote rc=" + str(rem.returncode) + ": " + rem.stderr[:500])
    if cfg.returncode != 0:
        raise ProofFailed(label + " config rc=" + str(cfg.returncode) + ": " + cfg.stderr[:500])
    if set(rem.stdout.splitlines()) != set(EXPECTED_REMOTE_LINES):
        raise ProofFailed(label + " remote lines != exact inert pair: " + str(sorted(rem.stdout.splitlines())))
    urls = [ln.split("=", 1)[1] for ln in cfg.stdout.splitlines()
            if ".url=" in ln and ln.split("=", 1)[0].endswith("url")]
    if not urls:
        raise ProofFailed(label + " config has no remote url entries")
    for u in urls:
        if u != EXPECTED_INERT_URL:
            raise ProofFailed(label + " config remote url not exact inert: " + repr(u))
    alt = repo / ".git" / "objects" / "info" / "alternates"
    try:
        alt_exists = os.lstat(alt) is not None
    except FileNotFoundError:
        alt_exists = False
    except OSError as exc:
        raise ProofFailed(label + " alternates unreadable: " + str(exc)) from exc
    if alt_exists:
        raise ProofFailed(label + " has alternates")
    return rem.stdout, cfg.stdout


def _git_show_bytes(repo: Path, env: dict[str, str], rel: str) -> bytes:
    resolved = str(Path(repo).resolve())
    proc = subprocess.run(["git", "-c", "safe.directory=" + resolved, "show", "HEAD:" + rel],
                          cwd=repo, capture_output=True, env=env, timeout=60)
    if proc.returncode != 0:
        raise ProofFailed("git show HEAD:" + rel + " rc=" + str(proc.returncode))
    out = proc.stdout
    if isinstance(out, str):
        out = out.encode("utf-8")
    return out


def _freeze_full(repo: Path, env: dict[str, str]) -> dict:
    out: dict = {}
    out["head"] = _git_checked(repo, env, "rev-parse", "HEAD").strip()
    out["tree"] = _git_checked(repo, env, "rev-parse", "HEAD^{tree}").strip()
    out["status"] = _git_checked(repo, env, "status", "--porcelain=v1", "-uall")
    out["index"] = _git_checked(repo, env, "diff", "--cached", "--name-only")
    files: dict = {}
    for rel in sorted(set(MODIFIED3) | set(NEW18)):
        p = repo / rel
        _require_regular(p, "freeze")
        data = p.read_bytes()
        files[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                      "mode": oct(p.stat().st_mode & 0o777), "bytes": p.stat().st_size}
    out["files"] = files
    return out


def _freeze_clean(repo: Path, env: dict[str, str]) -> dict:
    out: dict = {}
    out["head"] = _git_checked(repo, env, "rev-parse", "HEAD").strip()
    out["tree"] = _git_checked(repo, env, "rev-parse", "HEAD^{tree}").strip()
    out["status"] = _git_checked(repo, env, "status", "--porcelain=v1", "-uall")
    out["index"] = _git_checked(repo, env, "diff", "--cached", "--name-only")
    new_present: list[str] = []
    for n in NEW18:
        p = repo / n
        try:
            exists = p.exists()
        except OSError:
            exists = True
        try:
            is_link = p.is_symlink()
        except OSError:
            is_link = True
        if exists or is_link:
            new_present.append(n)
        # Never read NEW file bytes here: absence only, no absent-file read.
    if new_present:
        raise ProofFailed("clean copy still holds reverted NEW files: " + str(new_present))
    out["new_absent"] = list(NEW18)
    matched: list[str] = []
    for m in MODIFIED3:
        live = (repo / m).read_bytes()
        head_bytes = _git_show_bytes(repo, env, m)
        if live != head_bytes:
            raise ProofFailed("clean copy MODIFIED differs from HEAD bytes: " + m)
        matched.append(m)
    out["modified_match_head"] = matched
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="P3S B2 saved-patch apply proof (DRAFT)")
    parser.add_argument("--source", required=True)
    parser.add_argument("--patch", required=True)
    parser.add_argument("--patch-hash", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--scratch-root", required=True, help="existing dir under /tmp/opencode for clean409 byte copy")
    parser.add_argument("--cache-inventory", default=str(DEFAULT_CACHE_STATIC))
    parser.add_argument("--p2v-expected18", default=str(DEFAULT_P2V_EXPECTED18))
    args = parser.parse_args()
    source = Path(args.source)
    patch_arg = Path(args.patch)
    patch_hash_arg = Path(args.patch_hash)
    manifest_p = Path(args.manifest)
    outdir = Path(args.outdir)
    scratch_root = Path(args.scratch_root)
    cache_inv_p = Path(args.cache_inventory)
    p2r_exp_p = Path(args.p2v_expected18)
    try:
        scratch_resolved = scratch_root.resolve()
    except OSError as exc:
        print("PROOF_REFUSAL: scratch-root unresolvable: " + str(exc))
        return 40
    if str(scratch_resolved) != "/tmp/opencode" and not str(scratch_resolved).startswith("/tmp/opencode/"):
        print("PROOF_REFUSAL: scratch-root must be under /tmp/opencode: " + str(scratch_root))
        return 40
    if not scratch_root.is_dir():
        print("PROOF_REFUSAL: scratch-root missing (must pre-exist under /tmp/opencode): " + str(scratch_root))
        return 40
    try:
        patch_abs = patch_arg.resolve()
        patch_hash_abs = patch_hash_arg.resolve()
    except OSError as exc:
        print("PROOF_REFUSAL: patch path unresolvable: " + str(exc))
        return 40
    out_stdout = outdir / "proof_apply21_b3.stdout.txt"
    out_stderr = outdir / "proof_apply21_b3.stderr.txt"
    out_exit = outdir / "proof_apply21_b3.exit"
    out_clean = outdir / "proof-freeze-clean-b2.json"
    out_applied = outdir / "proof-freeze-applied-b2.json"
    out_meta = outdir / "proof_apply21_b3.meta.json"
    if os.path.lexists(outdir):
        print("PROOF_REFUSAL: outdir exists (not overwriting): " + str(outdir))
        return 40
    for name in (out_stdout.name, out_stderr.name, out_exit.name,
                 out_clean.name, out_applied.name, out_meta.name):
        if os.path.lexists(outdir / name):
            print("PROOF_REFUSAL: proof output exists: " + name)
            return 40
    if not os.path.lexists(patch_arg) or not patch_arg.is_file():
        print("PROOF_REFUSAL: saved patch missing/non-regular: " + str(patch_arg))
        return 40
    if not os.path.lexists(patch_hash_arg) or not patch_hash_arg.is_file():
        print("PROOF_REFUSAL: saved hash manifest missing/non-regular: " + str(patch_hash_arg))
        return 40
    if not os.path.lexists(manifest_p) or not manifest_p.is_file():
        print("PROOF_REFUSAL: static manifest missing/non-regular")
        return 40
    if not os.path.lexists(cache_inv_p) or not cache_inv_p.is_file():
        print("PROOF_REFUSAL: static cache inventory missing/non-regular")
        return 40
    if not os.path.lexists(p2r_exp_p) or not p2r_exp_p.is_file():
        print("PROOF_REFUSAL: static p2v expected18 missing/non-regular")
        return 40
    if not source.is_dir():
        print("PROOF_REFUSAL: source missing: " + str(source))
        return 40
    try:
        static_raw, static_parsed = _load_json_once(manifest_p, "manifest")
        cache_raw, cache_parsed = _load_json_once(cache_inv_p, "cache-inventory")
        p2v_raw, p2v_parsed = _load_json_once(p2r_exp_p, "p2v-expected18")
        patch_raw = _pin_file_bytes(patch_arg, "saved-patch")
        hash_raw = _pin_file_bytes(patch_hash_arg, "saved-hash")
    except ProofFailed as exc:
        print("PROOF_REFUSAL: static pin/read failed: " + str(exc))
        return 40
    except Exception as exc:
        print("PROOF_REFUSAL: static inputs unreadable: " + type(exc).__name__ + ": " + str(exc))
        return 40
    if not isinstance(static_parsed, dict):
        print("PROOF_REFUSAL: static21 root not object")
        return 40
    if not isinstance(cache_parsed, dict) or "files" not in cache_parsed or not isinstance(cache_parsed["files"], dict):
        print("PROOF_REFUSAL: cache inventory wrapper lacks dict 'files' (no silent default)")
        return 40
    if not isinstance(p2v_parsed, dict):
        print("PROOF_REFUSAL: p2v expected18 root not object")
        return 40
    static21: dict = static_parsed
    cache_static: dict = cache_parsed["files"]
    p2v_expected18: dict = p2v_parsed
    static_sha = hashlib.sha256(static_raw).hexdigest()
    cache_inv_sha = hashlib.sha256(cache_raw).hexdigest()
    p2v_sha = hashlib.sha256(p2v_raw).hexdigest()
    patch_sha = hashlib.sha256(patch_raw).hexdigest()
    try:
        hash_text = hash_raw.decode("utf-8").strip().split()[0]
    except (UnicodeDecodeError, IndexError) as exc:
        print("PROOF_REFUSAL: saved hash manifest undecodable/empty: " + type(exc).__name__)
        return 40
    if not re.fullmatch(r"[0-9a-f]{64}", hash_text):
        print("PROOF_REFUSAL: saved hash manifest is not 64-hex")
        return 40
    if patch_sha != hash_text:
        print("PROOF_REFUSAL: saved patch sha differs from hash manifest: computed=" + patch_sha + " saved=" + hash_text)
        return 40
    try:
        this_script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        this_script_sha = "unreadable"
    copyrepo = (scratch_root / (outdir.name + "-clean409-copy")).resolve()
    if str(copyrepo) != "/tmp/opencode" and not str(copyrepo).startswith("/tmp/opencode/"):
        print("PROOF_REFUSAL: copy escapes /tmp/opencode: " + str(copyrepo))
        return 40
    log_lines: list[str] = []
    def _log(msg: str) -> None:
        log_lines.append(msg)
    out_fh = None
    err_fh = None
    exit_fh = None
    try:
        outdir.mkdir(parents=False, exist_ok=False)
    except FileExistsError:
        print("PROOF_REFUSAL: outdir raced into existence: " + str(outdir))
        return 40
    except OSError as exc:
        print("PROOF_REFUSAL: cannot create outdir: " + str(exc))
        return 40
    try:
        out_fh = open(out_stdout, "xb")
        err_fh = open(out_stderr, "xb")
        exit_fh = open(out_exit, "xb")
    except OSError as exc:
        print("PROOF_REFUSAL: cannot reserve proof outputs: " + str(exc))
        return 40
    def _emit(code: int) -> int:
        exit_recorded: str | None = None
        try:
            out_fh.write(("\n".join(log_lines) + "\n").encode("utf-8"))
            out_fh.flush()
        except (OSError, ValueError) as exc:
            print("PROOF_REFUSAL: cannot write stdout handle: " + str(exc))
            if code == 0:
                code = 5
        try:
            err_fh.write(b"")
            err_fh.flush()
        except (OSError, ValueError) as exc:
            print("PROOF_REFUSAL: cannot write stderr handle: " + str(exc))
            if code == 0:
                code = 5
        try:
            exit_fh.write((str(code) + "\n").encode("utf-8"))
            exit_fh.flush()
            exit_recorded = str(code)
        except (OSError, ValueError) as exc:
            print("PROOF_REFUSAL: cannot write exit handle: " + str(exc))
            if code == 0:
                code = 5
        close_errors: list[str] = []
        for fh, nm in ((out_fh, "stdout"), (err_fh, "stderr"), (exit_fh, "exit")):
            try:
                fh.flush()
            except (OSError, ValueError) as exc:
                close_errors.append(nm + " flush: " + type(exc).__name__ + ": " + str(exc))
            try:
                fh.close()
            except (OSError, ValueError) as exc:
                close_errors.append(nm + " close: " + type(exc).__name__ + ": " + str(exc))
        if close_errors:
            print("PROOF_LIMIT: handle flush/close failed: " + "; ".join(close_errors))
            if exit_recorded is not None and exit_recorded == "0" and code != 0:
                print("PROOF_LIMIT: exit file already records 0 before close error; returned " + str(code) +
                      " reflects suppressed error (no overwrite repair; not atomically persistable)")
            if code == 0:
                code = 5
        return code
    primary_error: str | None = None
    secondary_errors: list[str] = []
    interrupted = False
    active: dict | None = None
    started = datetime.now(timezone.utc)
    try:
        env = _git_env()
        with open(out_meta, "x") as f:
            json.dump({"argv": sys.argv, "cwd": os.getcwd(), "python": sys.version,
                       "sys_executable": sys.executable, "source": str(source),
                       "patch": str(patch_abs), "patch_arg": str(patch_arg),
                       "patch_hash": str(patch_hash_abs),
                       "manifest": str(manifest_p),
                       "scratch_root": str(scratch_root), "copyrepo": str(copyrepo),
                       "proof_sha256": this_script_sha,
                       "started_utc": started.isoformat(),
                       "input_ids": {
                           "manifest": {"sha256": static_sha, "bytes": len(static_raw)},
                           "cache_inventory": {"sha256": cache_inv_sha, "bytes": len(cache_raw)},
                           "p2v_expected18": {"sha256": p2v_sha, "bytes": len(p2v_raw)},
                           "patch": {"sha256": patch_sha, "bytes": len(patch_raw)},
                       },
                       "forced_git": {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                                      "GIT_ALLOW_PROTOCOL": "file"}}, f, indent=1)
        if set(static21.keys()) != set(CANONICAL21):
            primary_error = "static21 keyset != canonical21: missing=" + \
                str(sorted(set(CANONICAL21) - set(static21.keys()))) + " extra=" + \
                str(sorted(set(static21.keys()) - set(CANONICAL21)))
            _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            for rel in sorted(NEW_P3S3):
                if rel not in static21:
                    primary_error = "static21 lacks new P3S path: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
        if primary_error is None:
            _log("saved patch sha256=" + patch_sha + " bytes=" + str(len(patch_raw)) + " (matches hash manifest, absolute " + str(patch_abs) + ")")
            try:
                active = _freeze_full(source, env)
            except ProofFailed as exc:
                primary_error = "active freeze failed: " + str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None and active is not None:
            if active.get("head") != FIXED_HEAD:
                primary_error = "active HEAD moved: " + repr(active.get("head"))
            elif active.get("tree") != FIXED_TREE:
                primary_error = "active tree moved: " + repr(active.get("tree"))
            elif (active.get("index") or "").strip() != "":
                primary_error = "active index non-empty"
            if primary_error is not None:
                _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None and active is not None:
            for rel in sorted(CANONICAL21):
                exp = static21.get(rel)
                got = active["files"].get(rel, {})
                if got.get("sha256") != exp.get("sha256") or got.get("mode") != exp.get("mode") \
                        or got.get("bytes") != exp.get("bytes"):
                    primary_error = "active static21 mismatch: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
        if primary_error is None:
            if set(p2v_expected18.keys()) != set(INHERITED18):
                primary_error = "p2v expected18 keyset != canonical inherited18: missing=" + \
                    str(sorted(set(INHERITED18) - set(p2v_expected18.keys()))) + " extra=" + \
                    str(sorted(set(p2v_expected18.keys()) - set(INHERITED18)))
                _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            try:
                det_rc, _det_out, _det_err = _check_detached(source, env, "active")
            except ProofFailed as exc:
                primary_error = str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
            else:
                if det_rc != 1:
                    primary_error = "active HEAD not detached (git symbolic-ref -q HEAD rc=" + \
                        str(det_rc) + " expected 1)"
                    _log("PROOF_REFUSAL: " + primary_error)
                else:
                    _log("active HEAD detached (symbolic-ref rc=1)")
        if primary_error is None:
            for rel in sorted(p2v_expected18.keys()):
                if static21.get(rel) != p2v_expected18.get(rel):
                    primary_error = "inherited18 drift vs P2V: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
        if primary_error is None and active is not None:
            s_status = _git(source, env, "status", "--porcelain=v1", "--untracked-files=all")
            if s_status.returncode != 0:
                primary_error = "active status rc=" + str(s_status.returncode)
                _log("PROOF_REFUSAL: " + primary_error)
            else:
                s_rows = set(s_status.stdout.splitlines())
                expected_cache_rows = {"?? " + c for c in cache_static.keys()}
                expected_full = set(EXPECTED_STATUS21) | expected_cache_rows
                if len(cache_static) != 84:
                    primary_error = "cache static len != 84: " + str(len(cache_static))
                    _log("PROOF_REFUSAL: " + primary_error)
                elif s_rows != expected_full or len(s_status.stdout.splitlines()) != 105:
                    primary_error = "active full status != exact 21+84 (105): missing=" + \
                        str(sorted(expected_full - s_rows)[:10]) + " extra=" + \
                        str(sorted(s_rows - expected_full)[:10])
                    _log("PROOF_REFUSAL: " + primary_error)
                else:
                    for rel in sorted(cache_static.keys()):
                        f = source / rel
                        try:
                            _require_regular(f, "active cache")
                        except ProofFailed as exc:
                            primary_error = str(exc)
                            _log("PROOF_REFUSAL: " + primary_error)
                            break
                        data = f.read_bytes()
                        exp = cache_static[rel]
                        if hashlib.sha256(data).hexdigest() != exp["sha256"] or len(data) != exp["bytes"] \
                                or oct(f.stat().st_mode & 0o777) != exp["mode"]:
                            primary_error = "active cache mismatch: " + rel
                            _log("PROOF_REFUSAL: " + primary_error)
                            break
        if primary_error is None and active is not None:
            try:
                active_remote, active_config = _check_remote_config(source, env, "active")
                _log("active 21 match static manifest + 84 caches + HEAD/tree/index pinned")
            except ProofFailed as exc:
                primary_error = str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
                active_remote, active_config = "", ""
        else:
            active_remote, active_config = "", ""
        if primary_error is None:
            if os.path.lexists(copyrepo):
                primary_error = "copy destination exists: " + str(copyrepo)
                _log("PROOF_REFUSAL: " + primary_error)
            else:
                cp = subprocess.run(["cp", "-a", "--reflink=never", str(source), str(copyrepo)],
                                    capture_output=True, text=True, timeout=300)
                if cp.returncode != 0:
                    primary_error = "byte-copy failed: " + cp.stderr[:1000]
                    _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            for rel in sorted(set(MODIFIED3) | set(NEW18)):
                is_f = (copyrepo / rel).is_file()
                c_data = (copyrepo / rel).read_bytes() if is_f else None
                if c_data is None:
                    primary_error = "copy incomplete, missing right after byte-copy: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
                if c_data != (source / rel).read_bytes():
                    primary_error = "copy incomplete, byte mismatch right after byte-copy: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
            if primary_error is None:
                _log("copy completeness verified: all 21 present and byte-equal active")
        if primary_error is None:
            try:
                a_reg, a_dirs, a_prob = _git_entries_all(source)
                c_reg, c_dirs, c_prob = _git_entries_all(copyrepo)
            except ProofFailed as exc:
                primary_error = "all-entry walk failed: " + str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
            else:
                _log("active .git regular=" + str(len(a_reg)) + " dirs=" + str(len(a_dirs)) + " problems=" + str(a_prob))
                _log("copy .git regular=" + str(len(c_reg)) + " dirs=" + str(len(c_dirs)) + " problems=" + str(c_prob))
                if a_prob:
                    primary_error = "active .git problems: " + str(a_prob[:10])
                    _log("PROOF_REFUSAL: " + primary_error)
                elif c_prob:
                    primary_error = "copy .git problems: " + str(c_prob[:10])
                    _log("PROOF_REFUSAL: " + primary_error)
                else:
                    a_pairs = {(d, i) for (d, i, _n) in a_reg.values()} | set(a_dirs.values())
                    c_pairs = {(d, i) for (d, i, _n) in c_reg.values()} | set(c_dirs.values())
                    shared = a_pairs & c_pairs
                    if shared:
                        primary_error = "copy shares .git (dev,ino) pairs with active: " + str(sorted(shared)[:10])
                        _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            try:
                copy_remote, copy_config = _check_remote_config(copyrepo, env, "copy")
                _log("copy remote observed (bounded scope, whole outputs persisted)")
            except ProofFailed as exc:
                primary_error = str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
                copy_remote, copy_config = "", ""
        else:
            copy_remote, copy_config = "", ""
        if primary_error is None:
            caches_before = sorted(str(p.relative_to(copyrepo).as_posix())
                                   for base in ("scripts", "tests", "schemas")
                                   for p in list((copyrepo / base).glob("__pycache__/*")) +
                                   list((copyrepo / base).glob("*.pyc")))
            _log("copy caches before declared removal (" + str(len(caches_before)) + ")")
            removed: list[str] = []
            try:
                for relpos in caches_before:
                    target = (copyrepo / relpos)
                    if str(target.resolve()).startswith(str(copyrepo.resolve()) + os.sep) is False and target.resolve() != copyrepo.resolve():
                        raise ProofFailed("cache removal escapes copyrepo: " + relpos)
                    try:
                        st = os.lstat(target)
                    except FileNotFoundError:
                        raise ProofFailed("cache inventoried but missing at removal: " + relpos)
                    if _stat.S_ISLNK(st.st_mode):
                        raise ProofFailed("cache removal refuses symlink: " + relpos)
                    if _stat.S_ISDIR(st.st_mode):
                        continue
                    if not _stat.S_ISREG(st.st_mode):
                        raise ProofFailed("cache removal refuses special: " + relpos)
                    if st.st_nlink != 1:
                        raise ProofFailed("cache removal refuses nlink!=1: " + relpos)
                    target.unlink()
                    removed.append(relpos)
                for cache_dir in (copyrepo / "scripts" / "__pycache__", copyrepo / "tests" / "__pycache__",
                                  copyrepo / "schemas" / "__pycache__"):
                    try:
                        if cache_dir.is_dir() and not cache_dir.is_symlink():
                            shutil.rmtree(cache_dir, ignore_errors=False)
                    except OSError as exc:
                        raise ProofFailed("copy cache dir removal failed: " + str(exc))
                survivors = sorted(str(p.relative_to(copyrepo).as_posix())
                                   for base in ("scripts", "tests", "schemas")
                                   for p in list((copyrepo / base).glob("__pycache__/*")) +
                                   list((copyrepo / base).glob("*.pyc"))
                                 + [s for s in caches_before if (copyrepo / s).exists() or (copyrepo / s).is_symlink()])
                if survivors:
                    raise ProofFailed("copy cache survivors after declared removal: " + str(survivors[:10]))
            except ProofFailed as exc:
                primary_error = str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
            else:
                _log("copy caches removed files=" + str(len(removed)) + " (disposable only)")
                r = _git(copyrepo, env, "checkout", "HEAD", "--", *MODIFIED3)
                if r.returncode != 0:
                    primary_error = "copy checkout HEAD -- 3M failed: " + r.stderr[:1000]
                    _log("PROOF_REFUSAL: " + primary_error)
                else:
                    for n in NEW18:
                        try:
                            (copyrepo / n).unlink()
                        except FileNotFoundError:
                            primary_error = "copy new file already absent (copy incomplete): " + n
                            _log("PROOF_REFUSAL: " + primary_error)
                            break
                        except OSError as exc:
                            primary_error = "copy unlink failed: " + n + ": " + str(exc)
                            _log("PROOF_REFUSAL: " + primary_error)
                            break
        if primary_error is None:
            try:
                clean = _freeze_clean(copyrepo, env)
            except ProofFailed as exc:
                primary_error = "clean freeze failed: " + str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
                clean = {}
            else:
                if clean.get("head") != FIXED_HEAD:
                    primary_error = "clean-copy HEAD moved"
                elif clean.get("tree") != FIXED_TREE:
                    primary_error = "clean-copy tree moved"
                elif (clean.get("index") or "").strip() != "":
                    primary_error = "clean-copy index non-empty"
                elif (clean.get("status") or "") != "":
                    primary_error = "copy not clean409: status=" + repr(clean.get("status")[:500])
                if primary_error is not None:
                    _log("PROOF_REFUSAL: " + primary_error)
                else:
                    try:
                        with open(out_clean, "x") as f:
                            json.dump({"head": clean["head"], "tree": clean["tree"], "status": clean["status"],
                                       "index": clean["index"], "new_absent": clean["new_absent"],
                                       "modified_match_head": clean["modified_match_head"],
                                       "caches_removed": caches_before,
                                       "caches_removed_files": removed,
                                       "active_remote": active_remote, "active_config": active_config,
                                       "copy_remote": copy_remote, "copy_config": copy_config}, f, indent=2)
                            f.write("\n")
                    except OSError as exc:
                        primary_error = "clean freeze write failed: " + str(exc)
                        _log("PROOF_REFUSAL: " + primary_error)
                    else:
                        _log("copy is clean409; applying EXACT saved patch")
        if primary_error is None:
            r = _git(copyrepo, env, "apply", "--check", str(patch_abs))
            if r.returncode != 0:
                primary_error = "apply --check failed: " + r.stderr[:2000]
                _log("PROOF_REFUSAL: " + primary_error)
            else:
                r = _git(copyrepo, env, "apply", str(patch_abs))
                if r.returncode != 0:
                    primary_error = "apply failed: " + r.stderr[:2000]
                    _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            try:
                applied = _freeze_full(copyrepo, env)
            except ProofFailed as exc:
                primary_error = "applied freeze failed: " + str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
                applied = {}
            else:
                if applied.get("head") != FIXED_HEAD:
                    primary_error = "applied-copy HEAD moved"
                elif applied.get("tree") != FIXED_TREE:
                    primary_error = "applied-copy tree moved"
                elif (applied.get("index") or "").strip() != "":
                    primary_error = "applied-copy index non-empty"
                if primary_error is not None:
                    _log("PROOF_REFUSAL: " + primary_error)
                else:
                    for rel in sorted(CANONICAL21):
                        exp = static21.get(rel)
                        got = applied["files"].get(rel, {})
                        if got.get("sha256") != exp.get("sha256") or got.get("mode") != exp.get("mode") \
                                or got.get("bytes") != exp.get("bytes"):
                            primary_error = "applied-copy static21 mismatch: " + rel
                            _log("PROOF_REFUSAL: " + primary_error)
                            break
        if primary_error is None:
            try:
                copy_remote2, copy_config2 = _check_remote_config(copyrepo, env, "applied-copy")
            except ProofFailed as exc:
                primary_error = str(exc)
                _log("PROOF_REFUSAL: " + primary_error)
                copy_remote2, copy_config2 = "", ""
            else:
                try:
                    with open(out_applied, "x") as f:
                        json.dump({"head": applied["head"], "tree": applied["tree"], "status": applied["status"],
                                   "index": applied["index"], "files": applied["files"],
                                   "copy_remote_post": copy_remote2, "copy_config_post": copy_config2,
                                   "active_remote": active_remote, "active_config": active_config}, f, indent=2)
                        f.write("\n")
                except OSError as exc:
                    primary_error = "applied freeze write failed: " + str(exc)
                    _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            for rel in sorted(CANONICAL21):
                if (source / rel).read_bytes() != (copyrepo / rel).read_bytes():
                    primary_error = "byte mismatch after apply: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
                if oct((source / rel).stat().st_mode & 0o777) != oct((copyrepo / rel).stat().st_mode & 0o777):
                    primary_error = "mode mismatch after apply: " + rel
                    _log("PROOF_REFUSAL: " + primary_error)
                    break
        if primary_error is None:
            status_rows = set(applied["status"].splitlines())
            if status_rows != set(EXPECTED_STATUS21):
                primary_error = "applied status != exact expected21 rows: missing=" + \
                    str(sorted(set(EXPECTED_STATUS21) - status_rows)) + " extra=" + \
                    str(sorted(status_rows - set(EXPECTED_STATUS21)))
                _log("PROOF_REFUSAL: " + primary_error)
            elif len(applied["status"].splitlines()) != 21:
                primary_error = "applied status len != 21"
                _log("PROOF_REFUSAL: " + primary_error)
        if primary_error is None:
            _log("APPLY_PROOF_OK head=" + str(applied["head"]) + " files=21 patch=" + patch_sha[:12])
    except KeyboardInterrupt as exc:
        primary_error = "interrupted: " + type(exc).__name__ + ": " + str(exc)
        interrupted = True
        try:
            _log("PROOF_REFUSAL: " + primary_error)
        except Exception:
            pass
    except (ProofFailed, RuntimeError, OSError) as exc:
        primary_error = "proof_failed: " + type(exc).__name__ + ": " + str(exc)
        try:
            _log("PROOF_REFUSAL: " + primary_error)
        except Exception:
            pass
    except Exception as exc:
        primary_error = "fatal: " + type(exc).__name__ + ": " + str(exc)
        try:
            _log("PROOF_REFUSAL: " + primary_error)
        except Exception:
            pass
    try:
        if active is not None:
            try:
                post_env = _git_env()
                post_check = _freeze_full(source, post_env)
                for rel in sorted(CANONICAL21):
                    if post_check["files"].get(rel, {}).get("sha256") != active["files"].get(rel, {}).get("sha256"):
                        secondary_errors.append("source changed during proof: " + rel)
                        break
                try:
                    post_det_rc, _post_det_out, _post_det_err = _check_detached(source, post_env, "source-post")
                except ProofFailed as exc:
                    secondary_errors.append("source-post detached check failed: " + str(exc))
                else:
                    if post_det_rc != 1:
                        secondary_errors.append("source-post HEAD not detached (symbolic-ref rc=" +
                                                str(post_det_rc) + " expected 1)")
            except (ProofFailed, RuntimeError, OSError) as exc:
                secondary_errors.append("source-post freeze failed: " + type(exc).__name__ + ": " + str(exc))
            except Exception as exc:
                secondary_errors.append("source-post computation failed: " + type(exc).__name__ + ": " + str(exc))
            try:
                for label2, p2, raw0 in (("manifest", manifest_p, static_raw),
                                         ("cache-inventory", cache_inv_p, cache_raw),
                                         ("p2v-expected18", p2r_exp_p, p2v_raw),
                                         ("saved-patch", patch_arg, patch_raw),
                                         ("saved-hash", patch_hash_arg, hash_raw)):
                    try:
                        cur = _pin_file_bytes(p2, "post-reverify " + label2)
                    except ProofFailed as exc:
                        secondary_errors.append("post-reverify pin failed (" + label2 + "): " + str(exc))
                        continue
                    if hashlib.sha256(cur).hexdigest() != hashlib.sha256(raw0).hexdigest():
                        secondary_errors.append("static input changed post guard (" + label2 + ")")
            except Exception as exc:
                secondary_errors.append("post-reverify computation failed: " + type(exc).__name__ + ": " + str(exc))
        else:
            secondary_errors.append("no active freeze available; checked source-POST skipped")
    except Exception as exc:
        secondary_errors.append("post-block fatal: " + type(exc).__name__ + ": " + str(exc))
    if interrupted:
        code = 130
    elif primary_error is not None:
        code = 40
    elif secondary_errors:
        code = 3
    else:
        code = 0
    elapsed = (datetime.now(timezone.utc) - started).total_seconds()
    try:
        _log("PROOF secondary=[" + "; ".join(secondary_errors) + "] elapsed_s=" + str(round(elapsed, 3)))
    except Exception:
        pass
    terminal_note = {"ended_utc": datetime.now(timezone.utc).isoformat(), "elapsed_s": elapsed,
                     "primary_error": primary_error, "secondary_errors": secondary_errors,
                     "interrupted": interrupted}
    try:
        with open(outdir / "proof_apply21_b3.terminal-note.json", "x") as f:
            json.dump(terminal_note, f, indent=1)
    except OSError:
        pass
    return _emit(code)

if __name__ == "__main__":
    sys.exit(main())
