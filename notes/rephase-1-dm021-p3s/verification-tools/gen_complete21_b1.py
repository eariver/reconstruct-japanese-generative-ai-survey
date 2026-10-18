#!/usr/bin/env python3
"""P3S complete21 patch GENERATOR B1 — DRAFT (NOT EXECUTED, root readback).

Generates saved complete21 patch directly vs clean actual409 (contains all
prior overlays incl. P2V18) + saved sha256 hash manifest, using ONLY a NEW
independent byte-copied DB/index under REQUIRED /tmp/opencode scratch root,
separately from the durable outdir. No temp index objects in active DB, no
commits, no network, no source cleanup. Consumed later by proof_apply21_b1.py.

Static assumptions (no candidate reads at authoring time):
- Fixed actual409 HEAD=409b292756dd1277b9dfae87679934c0d2ce251c
  tree=8ce3699861505f32d1d60bdc185d4d4f635aedb2, detached, empty index.
- Canonical 21 (3M+18A) + 84 P2R static caches = 105 status rows.
  New P3S3 (part of NEW18):
    scripts/survey_editorial_staged_source_v2.py
    schemas/editorial-staged-source-manifest-v2.schema.json
    tests/test_survey_editorial_staged_source_v2.py
  Inherited18 must equal P2V expected18-source-correction-v5.json.
- Disposable DB/index live ONLY under --scratch-root (must be under
  /tmp/opencode); durable patch/meta/logs live ONLY under --outdir.
  Absolute GIT_INDEX_FILE (resolved) — never a relative index path.
- No active `git add`, no object writes in active DB, no output overwrites.

Usage (after CoWorkerA return + root approval only):
  python3 gen_complete21_b1.py --manifest <immutable-static21.json>
    --candidate <path> --outdir <new-durable-dir>
    --scratch-root <new-or-existing-/tmp/opencode-root>
    [--cache-inventory <path>] [--p2v-expected18 <path>]
Outputs (all exclusive x, no overwrites, no cleanup):
  <outdir>/complete-p3s-21path.patch (binary diff --cached)
  <outdir>/complete-p3s-21path.sha256 ("<sha>  <name>\\n")
  <outdir>/gen_complete21_b1.meta.json, .source-pre.json/.source-post.json,
  <outdir>/gen_complete21_b1.exit, .stage-done.json,
  <outdir>/gen_complete21_b1.stdout.txt/.stderr.txt
  <scratch-root>/<outdir-name>-disposable-copy/ (independent byte copy)
  <scratch-root>/<outdir-name>-disposable-index (absolute index file)
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
    parser = argparse.ArgumentParser(description="P3S B1 complete21 generator (DRAFT)")
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
    if outdir.exists():
        print("GEN_REFUSAL: outdir exists (not overwriting): " + str(outdir), file=sys.stderr)
        return 40
    if not manifest_p.is_file() or not cache_inv_p.is_file() or not p2r_exp_p.is_file():
        print("GEN_REFUSAL: static inputs missing", file=sys.stderr)
        return 40
    if not source.is_dir():
        print("GEN_REFUSAL: source missing: " + str(source), file=sys.stderr)
        return 40
    try:
        manifest = json.loads(manifest_p.read_bytes())
        cache_static = json.loads(cache_inv_p.read_bytes()).get("files", {})
        p2v_expected18 = json.loads(p2r_exp_p.read_bytes())
    except Exception as exc:
        print("GEN_REFUSAL: static JSON unreadable: " + str(exc), file=sys.stderr)
        return 40
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
    meta_p = outdir / "gen_complete21_b1.meta.json"
    pre_p = outdir / "gen_complete21_b1.source-pre.json"
    post_p = outdir / "gen_complete21_b1.source-post.json"
    exit_p = outdir / "gen_complete21_b1.exit"
    done_p = outdir / "gen_complete21_b1.stage-done.json"
    stdout_p = outdir / "gen_complete21_b1.stdout.txt"
    stderr_p = outdir / "gen_complete21_b1.stderr.txt"
    terminal: dict = {"gen": "gen_complete21_b1.py", "pid": os.getpid(),
                      "gen_sha256": this_script_sha}
    wrapper_rc = 40
    out_fh = None
    err_fh = None
    log_lines: list[str] = []
    def _log(msg: str) -> None:
        log_lines.append(msg)
    try:
        outdir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("GEN_REFUSAL: outdir raced into existence: " + str(outdir), file=sys.stderr)
        return 40
    except OSError as exc:
        print("GEN_REFUSAL: cannot create outdir: " + str(exc), file=sys.stderr)
        return 40
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
                             "manifest": {"sha256": hashlib.sha256(manifest_p.read_bytes()).hexdigest(), "bytes": manifest_p.stat().st_size},
                             "cache_inventory": {"sha256": hashlib.sha256(cache_inv_p.read_bytes()).hexdigest(), "bytes": cache_inv_p.stat().st_size},
                             "p2v_expected18": {"sha256": hashlib.sha256(p2r_exp_p.read_bytes()).hexdigest(), "bytes": p2r_exp_p.stat().st_size},
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
            raise GenFailed("source-pre guard failed: " + "; ".join(pre_errors))
        _log("source-pre 21+84 exact HEAD/tree/index/status pinned")
        if disp.exists() or disp_index.exists() or patch_p.exists() or hash_p.exists():
            raise GenFailed("disposable outputs already exist (not overwriting): copy=" + str(disp) + " index=" + str(disp_index))
        cp = subprocess.run(["cp", "-a", "--reflink=never", str(source), str(disp)],
                            capture_output=True, text=True, timeout=300)
        if cp.returncode != 0:
            raise GenFailed("byte-copy failed rc=" + str(cp.returncode) + ": " + cp.stderr[:1000])
        terminal["copy_rc"] = cp.returncode
        terminal["copy_stderr"] = cp.stderr[:1000]
        for rel in sorted(set(MODIFIED3) | set(NEW18)):
            c_data = (disp / rel).read_bytes() if (disp / rel).is_file() else None
            if c_data is None:
                raise GenFailed("copy incomplete, missing right after byte-copy: " + rel)
            if c_data != (source / rel).read_bytes():
                raise GenFailed("copy incomplete, byte mismatch right after byte-copy: " + rel)
        _log("copy completeness verified: all 21 present and byte-equal source")
        a_reg, a_dirs, a_prob = _git_entries_all(source)
        c_reg, c_dirs, c_prob = _git_entries_all(disp)
        terminal["source_git_regular"] = len(a_reg)
        terminal["source_git_dirs"] = len(a_dirs)
        terminal["copy_git_regular"] = len(c_reg)
        terminal["copy_git_dirs"] = len(c_dirs)
        if a_prob:
            raise GenFailed("source .git problems: " + str(a_prob[:10]))
        if c_prob:
            raise GenFailed("copy .git problems: " + str(c_prob[:10]))
        a_pairs = {(d, i) for (d, i, _n) in a_reg.values()} | set(a_dirs.values())
        c_pairs = {(d, i) for (d, i, _n) in c_reg.values()} | set(c_dirs.values())
        shared = a_pairs & c_pairs
        if shared:
            raise GenFailed("copy shares .git (dev,ino) pairs with source: " + str(sorted(shared)[:10]))
        for label, repo in (("source", source), ("copy", disp)):
            rem = _run_git(repo, git_env, "remote", "-v")
            cfg = _run_git(repo, git_env, "config", "--list", "--show-origin")
            if rem.returncode != 0 or cfg.returncode != 0:
                raise GenFailed(label + " remote/config rc nonzero")
            if set(rem.stdout.splitlines()) != set(EXPECTED_REMOTE_LINES):
                raise GenFailed(label + " remote lines != exact inert pair")
            urls = [ln.split("=", 1)[1] for ln in cfg.stdout.splitlines()
                    if ".url=" in ln and ln.split("=", 1)[0].endswith("url")]
            if not urls:
                raise GenFailed(label + " config has no remote url entries")
            for u in urls:
                if u != EXPECTED_INERT_URL:
                    raise GenFailed(label + " config remote url not exact inert: " + repr(u))
            alt = repo / ".git" / "objects" / "info" / "alternates"
            try:
                alt_exists = os.lstat(alt) is not None
            except FileNotFoundError:
                alt_exists = False
            if alt_exists:
                raise GenFailed(label + " has alternates")
            terminal[label + "_remote"] = rem.stdout
            terminal[label + "_config"] = cfg.stdout
        _log("all-entry separation + inert remote/config observed (bounded scope, whole outputs persisted)")
        denv = dict(git_env)
        denv["GIT_INDEX_FILE"] = str(disp_index)
        if disp_index.exists():
            raise GenFailed("disposable index exists (not overwriting): " + str(disp_index))
        raw_cmds: list[dict] = []
        r1 = _run_git(disp, denv, "read-tree", "HEAD")
        raw_cmds.append({"cmd": ["read-tree", "HEAD"], "rc": r1.returncode, "stderr": r1.stderr[:1000]})
        if r1.returncode != 0:
            raise GenFailed("disposable read-tree rc=" + str(r1.returncode) + ": " + r1.stderr[:1000])
        r2 = _run_git(disp, denv, "add", "--", *MODIFIED3, *NEW18)
        raw_cmds.append({"cmd": ["add", "--"] + MODIFIED3 + NEW18, "rc": r2.returncode, "stderr": r2.stderr[:1000]})
        if r2.returncode != 0:
            raise GenFailed("disposable add rc=" + str(r2.returncode) + ": " + r2.stderr[:1000])
        r3 = _run_git(disp, denv, "diff", "--cached", "--binary")
        raw_cmds.append({"cmd": ["diff", "--cached", "--binary"], "rc": r3.returncode, "stderr": r3.stderr[:1000]})
        if r3.returncode != 0:
            raise GenFailed("disposable diff rc=" + str(r3.returncode) + ": " + r3.stderr[:1000])
        terminal["raw_git_sequence"] = raw_cmds
        terminal["disposable_index_absolute"] = str(disp_index)
        diff_bytes = r3.stdout.encode("utf-8")
        if len(diff_bytes) == 0:
            raise GenFailed("generated patch empty (overlay missing?)")
        with open(patch_p, "xb") as f:
            f.write(diff_bytes)
            f.flush()
        sha = hashlib.sha256(patch_p.read_bytes()).hexdigest()
        with open(hash_p, "x") as f:
            f.write(sha + "  " + patch_p.name + "\n")
        terminal["patch_sha256"] = sha
        terminal["patch_bytes"] = patch_p.stat().st_size
        _log("saved complete21 patch bytes=" + str(patch_p.stat().st_size) + " sha=" + sha[:12])
        post = _observe_source(source, git_env, manifest, cache_static, "source-post")
        with open(post_p, "x") as f:
            json.dump(post, f, indent=1)
        if set(post.get("status_rows", [])) != set(pre.get("status_rows", [])):
            raise GenFailed("source changed during GEN (pre/post status differ)")
        for rel in sorted(manifest.keys()):
            if post["files"].get(rel, {}).get("sha256") != pre["files"].get(rel, {}).get("sha256"):
                raise GenFailed("source file changed during GEN: " + rel)
        _log("source-post unchanged (no active objects/commits/cleanup)")
        wrapper_rc = 0
    except GenFailed as exc:
        terminal["gen_failed"] = str(exc)
        wrapper_rc = 40
    except KeyboardInterrupt as exc:
        terminal["interrupted"] = type(exc).__name__ + ": " + str(exc)
        wrapper_rc = 130
    except Exception as exc:
        terminal["fatal"] = type(exc).__name__ + ": " + str(exc)
        wrapper_rc = 1
    finally:
        flush_errors: list[str] = []
        terminal["ended_utc"] = datetime.now(timezone.utc).isoformat()
        terminal["wrapper_rc"] = wrapper_rc
        try:
            if out_fh is not None and not out_fh.closed:
                out_fh.write(("\n".join(log_lines) + "\n").encode("utf-8"))
                out_fh.write(("GEN wrapper_rc=" + str(wrapper_rc) + "\n").encode("utf-8"))
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
