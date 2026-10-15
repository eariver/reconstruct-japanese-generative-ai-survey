#!/usr/bin/env python3
"""P2V complete18 patch GENERATOR B4 — DRAFT (NOT EXECUTED, root readback).

Generates saved complete18 patch directly vs clean actual409 (contains all
prior overlays) + saved sha256 hash manifest, using ONLY a NEW independent
byte-copied DB/index. No temp index objects in active DB, no commits, no
network, no source cleanup. Consumed later by proof_apply18_b4.py.

Static assumptions: fixed HEAD409/tree8ce, canonical 18 (3M+15A), P2R
inherited15, 84 P2R caches preserved in source (untouched here).

Usage:
  python3 gen_complete18_b4.py --manifest <immutable-static18.json>
    --outdir <new-dir> [--candidate <path>] [--cache-inventory <path>]
    [--p2r-expected16 <path>]
Outputs (all exclusive x, no overwrites, no cleanup):
  <outdir>/complete-p2v-18path.patch (binary diff --cached)
  <outdir>/complete-p2v-18path.sha256 ("<sha>  <name>\\n")
  <outdir>/gen_complete18_b4.meta.json, .source-pre.json/.source-post.json,
  <outdir>/gen_complete18_b4.exit, .stage-done.json
  <outdir>/disposable-copy/ (independent byte copy) + disposable-index
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
DEFAULT_CANDIDATE = Path("/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60")
DEFAULT_CACHE_STATIC = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/cache-inventory-static.json")
DEFAULT_P2R_EXPECTED16 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/expected16-correction2c.json")
P1_MODULE = "scripts/survey_editorial_correction_proposal_v2.py"
CANONICAL18 = frozenset({
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_current_authority_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_current_authority_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
})
MODIFIED3 = sorted([
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
])
NEW15 = sorted({
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
})
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


def _check_source(obs: dict, manifest: dict, p2r_expected16: dict, cache_static: dict, where: str) -> list[str]:
    errors: list[str] = []
    if obs["head"] != FIXED_HEAD:
        errors.append(where + " HEAD mismatch: " + repr(obs["head"]))
    if obs["tree"] != FIXED_TREE:
        errors.append(where + " tree mismatch: " + repr(obs["tree"]))
    if (obs["index_raw"] or "").strip() != "":
        errors.append(where + " index non-empty")
    if set(manifest.keys()) != set(CANONICAL18):
        errors.append(where + " manifest keyset != canonical18")
    for rel in sorted(CANONICAL18):
        exp = manifest.get(rel)
        got = obs["files"].get(rel, {})
        if got.get("sha256") != (exp or {}).get("sha256") or got.get("bytes") != (exp or {}).get("bytes") \
                or got.get("mode") != (exp or {}).get("mode"):
            errors.append(where + " static18 mismatch: " + rel)
    for rel in sorted(set(p2r_expected16.keys()) - {P1_MODULE}):
        if manifest.get(rel) != p2r_expected16.get(rel):
            errors.append(where + " inherited15 drift: " + rel)
    expected_full = {" M " + m for m in MODIFIED3} | {"?? " + n for n in NEW15} | {"?? " + c for c in cache_static.keys()}
    if set(obs.get("status_rows", [])) != expected_full:
        errors.append(where + " full status != exact 18+84: missing=" +
                      str(sorted(expected_full - set(obs.get("status_rows", [])))[:5]) + " extra=" +
                      str(sorted(set(obs.get("status_rows", [])) - expected_full)[:5]))
    if len(obs.get("status_rows", [])) != 102:
        errors.append(where + " status len != 102")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="P2V B3 complete18 generator (DRAFT)")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--candidate", default=str(DEFAULT_CANDIDATE))
    parser.add_argument("--cache-inventory", default=str(DEFAULT_CACHE_STATIC))
    parser.add_argument("--p2r-expected16", default=str(DEFAULT_P2R_EXPECTED16))
    args = parser.parse_args()
    manifest_p = Path(args.manifest)
    outdir = Path(args.outdir)
    source = Path(args.candidate)
    cache_inv_p = Path(args.cache_inventory)
    p2r_exp_p = Path(args.p2r_expected16)
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
        p2r_expected16 = json.loads(p2r_exp_p.read_bytes())
    except Exception as exc:
        print("GEN_REFUSAL: static JSON unreadable: " + str(exc), file=sys.stderr)
        return 40
    patch_p = outdir / "complete-p2v-18path.patch"
    hash_p = outdir / "complete-p2v-18path.sha256"
    meta_p = outdir / "gen_complete18_b4.meta.json"
    pre_p = outdir / "gen_complete18_b4.source-pre.json"
    post_p = outdir / "gen_complete18_b4.source-post.json"
    exit_p = outdir / "gen_complete18_b4.exit"
    done_p = outdir / "gen_complete18_b4.stage-done.json"
    disp = outdir / "disposable-copy"
    disp_index = outdir / "disposable-index"
    terminal: dict = {"gen": "gen_complete18_b4.py", "pid": os.getpid()}
    wrapper_rc = 40
    out_fh = None
    err_fh = None
    stdout_p = outdir / "gen_complete18_b4.stdout.txt"
    stderr_p = outdir / "gen_complete18_b4.stderr.txt"
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
                         "input_ids": {
                             "manifest": {"sha256": hashlib.sha256(manifest_p.read_bytes()).hexdigest(), "bytes": manifest_p.stat().st_size},
                             "cache_inventory": {"sha256": hashlib.sha256(cache_inv_p.read_bytes()).hexdigest(), "bytes": cache_inv_p.stat().st_size},
                             "p2r_expected16": {"sha256": hashlib.sha256(p2r_exp_p.read_bytes()).hexdigest(), "bytes": p2r_exp_p.stat().st_size},
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
        pre_errors = _check_source(pre, manifest, p2r_expected16, cache_static, "source-pre")
        if pre_errors:
            raise GenFailed("source-pre guard failed: " + "; ".join(pre_errors))
        _log("source-pre 18+84 exact HEAD/tree/index/status pinned")
        if disp.exists() or disp_index.exists() or patch_p.exists() or hash_p.exists():
            raise GenFailed("disposable outputs already exist (not overwriting)")
        cp = subprocess.run(["cp", "-a", "--reflink=never", str(source), str(disp)],
                            capture_output=True, text=True, timeout=300)
        if cp.returncode != 0:
            raise GenFailed("byte-copy failed rc=" + str(cp.returncode) + ": " + cp.stderr[:1000])
        terminal["copy_rc"] = cp.returncode
        terminal["copy_stderr"] = cp.stderr[:1000]
        for rel in sorted(set(MODIFIED3) | set(NEW15)):
            c_data = (disp / rel).read_bytes() if (disp / rel).is_file() else None
            if c_data is None:
                raise GenFailed("copy incomplete, missing right after byte-copy: " + rel)
            if c_data != (source / rel).read_bytes():
                raise GenFailed("copy incomplete, byte mismatch right after byte-copy: " + rel)
        _log("copy completeness verified: all 18 present and byte-equal source")
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
            raise GenFailed("disposable index exists (not overwriting)")
        r1 = _run_git(disp, denv, "read-tree", "HEAD")
        if r1.returncode != 0:
            raise GenFailed("disposable read-tree rc=" + str(r1.returncode) + ": " + r1.stderr[:1000])
        r2 = _run_git(disp, denv, "add", "--", *MODIFIED3, *NEW15)
        if r2.returncode != 0:
            raise GenFailed("disposable add rc=" + str(r2.returncode) + ": " + r2.stderr[:1000])
        r3 = _run_git(disp, denv, "diff", "--cached", "--binary")
        if r3.returncode != 0:
            raise GenFailed("disposable diff rc=" + str(r3.returncode) + ": " + r3.stderr[:1000])
        terminal["diff_rc"] = r3.returncode
        terminal["diff_stderr"] = r3.stderr[:1000]
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
        _log("saved complete18 patch bytes=" + str(patch_p.stat().st_size) + " sha=" + sha[:12])
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
