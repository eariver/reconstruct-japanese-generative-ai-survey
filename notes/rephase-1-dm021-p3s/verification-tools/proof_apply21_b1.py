#!/usr/bin/env python3
# Co-Worker B local P3S B1 draft of proof_apply21 (new, no preserved byte-identical original).
# Fixes P2V B4 lessons: disposable copy/index live ONLY under REQUIRED
# /tmp/opencode scratch root (never nested under notes outdir); absolute
# GIT_INDEX_FILE is not used here (copy uses its own .git/index); no
# return-in-finally; flush/close errors force nonzero.
#!/usr/bin/env python3
"""P3S saved-patch apply PROOF B1 — DRAFT (NOT EXECUTED, root readback).

Consumes ONLY SAVED complete21 patch + hash manifest + static21 (generated
by gen_complete21_b1.py after final pins; never generates patch here).
Uses a NEW independent byte-copied DB/worktree under REQUIRED /tmp/opencode
scratch root; validates active21 before; only declared 3M revert-from-HEAD /
18NEW absence + explicit copy cache removal; clean freeze never reads removed
NEW files.

Checks: clean HEAD/tree/index/status + 3M bytes==HEAD bytes; all-entry .git
lstat (walk errors/dirs/nlink/symlink/special refusal), full inode-SET cross
comparison source/copy (nlink1), source unchanged pre/post, exact effective
inert remote + config persisted (bounded scope, not generic matcher).
Applies SAVED patch via --check/apply, then all21 sha/mode/size + full
EXACT21 status/index/HEAD/tree; source caches preserved untouched.

Usage:
  python3 proof_apply21_b1.py --source <candidate> --patch <saved.patch>
    --patch-hash <saved.sha256> --manifest <static21.json>
    --outdir <new-durable-dir> --scratch-root <new-or-existing-/tmp/opencode-root>
    [--cache-inventory <path>] [--p2v-expected18 <path>]
Output-exists refusal writes nothing (console only). All other outputs are
exclusive xb/x with full failure paths recorded. Flush/close errors force
nonzero exit (no suppressed-logger flaw). No source cleanup. One-off tool,
not generic certification.
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
    parser = argparse.ArgumentParser(description="P3S B1 saved-patch apply proof (DRAFT)")
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
    patch = Path(args.patch)
    patch_hash_p = Path(args.patch_hash)
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
    out_stdout = outdir / "proof_apply21_b1.stdout.txt"
    out_stderr = outdir / "proof_apply21_b1.stderr.txt"
    out_exit = outdir / "proof_apply21_b1.exit"
    out_clean = outdir / "proof-freeze-clean-b1.json"
    out_applied = outdir / "proof-freeze-applied-b1.json"
    out_meta = outdir / "proof_apply21_b1.meta.json"
    if outdir.exists():
        print("PROOF_REFUSAL: outdir exists (not overwriting): " + str(outdir))
        return 40
    for name in (out_stdout.name, out_stderr.name, out_exit.name,
                 out_clean.name, out_applied.name, out_meta.name):
        if (outdir / name).exists():
            print("PROOF_REFUSAL: proof output exists: " + name)
            return 40
    if not patch.is_file():
        print("PROOF_REFUSAL: saved patch missing: " + str(patch))
        return 40
    if not patch_hash_p.is_file():
        print("PROOF_REFUSAL: saved hash manifest missing: " + str(patch_hash_p))
        return 40
    if not manifest_p.is_file() or not cache_inv_p.is_file() or not p2r_exp_p.is_file():
        print("PROOF_REFUSAL: static inputs missing")
        return 40
    if not source.is_dir():
        print("PROOF_REFUSAL: source missing: " + str(source))
        return 40
    try:
        static21 = json.loads(manifest_p.read_bytes())
        cache_static = json.loads(cache_inv_p.read_bytes()).get("files", {})
        p2v_expected18 = json.loads(p2r_exp_p.read_bytes())
    except Exception as exc:
        print("PROOF_REFUSAL: static JSON unreadable: " + str(exc))
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
        outdir.mkdir(parents=True, exist_ok=False)
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
    def _fail(msg: str) -> int:
        _log("PROOF_REFUSAL: " + msg)
        return _emit(40)
    try:
        env = _git_env()
        with open(out_meta, "x") as f:
            json.dump({"argv": sys.argv, "cwd": os.getcwd(), "python": sys.version,
                       "sys_executable": sys.executable, "source": str(source),
                       "patch": str(patch), "patch_hash": str(patch_hash_p),
                       "manifest": str(manifest_p),
                       "scratch_root": str(scratch_root), "copyrepo": str(copyrepo),
                       "proof_sha256": this_script_sha,
                       "input_ids": {
                           "manifest": {"sha256": hashlib.sha256(manifest_p.read_bytes()).hexdigest(), "bytes": manifest_p.stat().st_size},
                           "cache_inventory": {"sha256": hashlib.sha256(cache_inv_p.read_bytes()).hexdigest(), "bytes": cache_inv_p.stat().st_size},
                           "p2v_expected18": {"sha256": hashlib.sha256(p2r_exp_p.read_bytes()).hexdigest(), "bytes": p2r_exp_p.stat().st_size},
                       },
                       "forced_git": {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                                      "GIT_ALLOW_PROTOCOL": "file"}}, f, indent=1)
        if set(static21.keys()) != set(CANONICAL21):
            return _fail("static21 keyset != canonical21: missing=" +
                         str(sorted(set(CANONICAL21) - set(static21.keys()))) + " extra=" +
                         str(sorted(set(static21.keys()) - set(CANONICAL21))))
        for rel in sorted(NEW_P3S3):
            if rel not in static21:
                return _fail("static21 lacks new P3S path: " + rel)
        try:
            saved_hash = patch_hash_p.read_text(encoding="utf-8").strip().split()[0]
        except OSError as exc:
            return _fail("saved hash unreadable: " + str(exc))
        if not re.fullmatch(r"[0-9a-f]{64}", saved_hash):
            return _fail("saved hash manifest is not 64-hex")
        try:
            patch_sha = hashlib.sha256(patch.read_bytes()).hexdigest()
        except OSError as exc:
            return _fail("saved patch unreadable: " + str(exc))
        if patch_sha != saved_hash:
            return _fail("saved patch sha differs from hash manifest: computed=" + patch_sha +
                         " saved=" + saved_hash)
        _log("saved patch sha256=" + patch_sha + " bytes=" + str(patch.stat().st_size) + " (matches hash manifest)")
        active = _freeze_full(source, env)
        if active.get("head") != FIXED_HEAD:
            return _fail("active HEAD moved: " + repr(active.get("head")))
        if active.get("tree") != FIXED_TREE:
            return _fail("active tree moved: " + repr(active.get("tree")))
        if (active.get("index") or "").strip() != "":
            return _fail("active index non-empty")
        for rel in sorted(CANONICAL21):
            exp = static21.get(rel)
            got = active["files"].get(rel, {})
            if got.get("sha256") != exp.get("sha256") or got.get("mode") != exp.get("mode") \
                    or got.get("bytes") != exp.get("bytes"):
                return _fail("active static21 mismatch: " + rel)
        for rel in sorted(p2v_expected18.keys()):
            if static21.get(rel) != p2v_expected18.get(rel):
                return _fail("inherited18 drift vs P2V: " + rel)
        s_status = _git(source, env, "status", "--porcelain=v1", "--untracked-files=all")
        if s_status.returncode != 0:
            return _fail("active status rc=" + str(s_status.returncode))
        s_rows = set(s_status.stdout.splitlines())
        expected_cache_rows = {"?? " + c for c in cache_static.keys()}
        expected_full = set(EXPECTED_STATUS21) | expected_cache_rows
        if len(cache_static) != 84:
            return _fail("cache static len != 84: " + str(len(cache_static)))
        if s_rows != expected_full or len(s_status.stdout.splitlines()) != 105:
            return _fail("active full status != exact 21+84 (105): missing=" +
                         str(sorted(expected_full - s_rows)[:10]) + " extra=" +
                         str(sorted(s_rows - expected_full)[:10]))
        for rel in sorted(cache_static.keys()):
            f = source / rel
            try:
                _require_regular(f, "active cache")
            except ProofFailed as exc:
                return _fail(str(exc))
            import hashlib as _hl
            data = f.read_bytes()
            exp = cache_static[rel]
            if _hl.sha256(data).hexdigest() != exp["sha256"] or len(data) != exp["bytes"] \
                    or oct(f.stat().st_mode & 0o777) != exp["mode"]:
                return _fail("active cache mismatch: " + rel)
        active_remote, active_config = _check_remote_config(source, env, "active")
        _log("active 21 match static manifest + 84 caches + HEAD/tree/index pinned")
        if copyrepo.exists():
            return _fail("copy destination exists: " + str(copyrepo))
        cp = subprocess.run(["cp", "-a", "--reflink=never", str(source), str(copyrepo)],
                            capture_output=True, text=True, timeout=300)
        if cp.returncode != 0:
            return _fail("byte-copy failed: " + cp.stderr[:1000])
        for rel in sorted(set(MODIFIED3) | set(NEW18)):
            c_data = (copyrepo / rel).read_bytes() if (copyrepo / rel).is_file() else None
            if c_data is None:
                return _fail("copy incomplete, missing right after byte-copy: " + rel)
            if c_data != (source / rel).read_bytes():
                return _fail("copy incomplete, byte mismatch right after byte-copy: " + rel)
        _log("copy completeness verified: all 21 present and byte-equal active")
        a_reg, a_dirs, a_prob = _git_entries_all(source)
        c_reg, c_dirs, c_prob = _git_entries_all(copyrepo)
        _log("active .git regular=" + str(len(a_reg)) + " dirs=" + str(len(a_dirs)) + " problems=" + str(a_prob))
        _log("copy .git regular=" + str(len(c_reg)) + " dirs=" + str(len(c_dirs)) + " problems=" + str(c_prob))
        if a_prob:
            return _fail("active .git problems: " + str(a_prob[:10]))
        if c_prob:
            return _fail("copy .git problems: " + str(c_prob[:10]))
        a_pairs = {(d, i) for (d, i, _n) in a_reg.values()} | set(a_dirs.values())
        c_pairs = {(d, i) for (d, i, _n) in c_reg.values()} | set(c_dirs.values())
        shared = a_pairs & c_pairs
        if shared:
            return _fail("copy shares .git (dev,ino) pairs with active: " + str(sorted(shared)[:10]))
        copy_remote, copy_config = _check_remote_config(copyrepo, env, "copy")
        _log("copy remote observed (bounded scope, whole outputs persisted)")
        caches_before = sorted(str(p.relative_to(copyrepo).as_posix())
                               for base in ("scripts", "tests", "schemas")
                               for p in list((copyrepo / base).glob("__pycache__/*")) +
                               list((copyrepo / base).glob("*.pyc")))
        _log("copy caches before declared removal (" + str(len(caches_before)) + ")")
        r = _git(copyrepo, env, "checkout", "HEAD", "--", *MODIFIED3)
        if r.returncode != 0:
            return _fail("copy checkout HEAD -- 3M failed: " + r.stderr[:1000])
        for n in NEW18:
            try:
                (copyrepo / n).unlink()
            except FileNotFoundError:
                return _fail("copy new file already absent (copy incomplete): " + n)
            except OSError as exc:
                return _fail("copy unlink failed: " + n + ": " + str(exc))
        for cache_dir in (copyrepo / "scripts" / "__pycache__", copyrepo / "tests" / "__pycache__",
                          copyrepo / "schemas" / "__pycache__"):
            try:
                if cache_dir.is_dir() and not cache_dir.is_symlink():
                    shutil.rmtree(cache_dir, ignore_errors=False)
            except OSError as exc:
                return _fail("copy cache removal failed: " + str(exc))
        clean = _freeze_clean(copyrepo, env)
        if clean.get("head") != FIXED_HEAD:
            return _fail("clean-copy HEAD moved")
        if clean.get("tree") != FIXED_TREE:
            return _fail("clean-copy tree moved")
        if (clean.get("index") or "").strip() != "":
            return _fail("clean-copy index non-empty")
        if (clean.get("status") or "") != "":
            return _fail("copy not clean409: status=" + repr(clean.get("status")[:500]))
        with open(out_clean, "x") as f:
            json.dump({"head": clean["head"], "tree": clean["tree"], "status": clean["status"],
                       "index": clean["index"], "new_absent": clean["new_absent"],
                       "modified_match_head": clean["modified_match_head"],
                       "caches_removed": caches_before,
                       "active_remote": active_remote, "active_config": active_config,
                       "copy_remote": copy_remote, "copy_config": copy_config}, f, indent=2)
            f.write("\n")
        _log("copy is clean409; applying EXACT saved patch")
        r = _git(copyrepo, env, "apply", "--check", str(patch))
        if r.returncode != 0:
            return _fail("apply --check failed: " + r.stderr[:2000])
        r = _git(copyrepo, env, "apply", str(patch))
        if r.returncode != 0:
            return _fail("apply failed: " + r.stderr[:2000])
        applied = _freeze_full(copyrepo, env)
        if applied.get("head") != FIXED_HEAD:
            return _fail("applied-copy HEAD moved")
        if applied.get("tree") != FIXED_TREE:
            return _fail("applied-copy tree moved")
        if (applied.get("index") or "").strip() != "":
            return _fail("applied-copy index non-empty")
        for rel in sorted(CANONICAL21):
            exp = static21.get(rel)
            got = applied["files"].get(rel, {})
            if got.get("sha256") != exp.get("sha256") or got.get("mode") != exp.get("mode") \
                    or got.get("bytes") != exp.get("bytes"):
                return _fail("applied-copy static21 mismatch: " + rel)
        copy_remote2, copy_config2 = _check_remote_config(copyrepo, env, "applied-copy")
        with open(out_applied, "x") as f:
            json.dump({"head": applied["head"], "tree": applied["tree"], "status": applied["status"],
                       "index": applied["index"], "files": applied["files"],
                       "copy_remote_post": copy_remote2, "copy_config_post": copy_config2,
                       "active_remote": active_remote, "active_config": active_config}, f, indent=2)
            f.write("\n")
        for rel in sorted(CANONICAL21):
            if (source / rel).read_bytes() != (copyrepo / rel).read_bytes():
                return _fail("byte mismatch after apply: " + rel)
            if oct((source / rel).stat().st_mode & 0o777) != oct((copyrepo / rel).stat().st_mode & 0o777):
                return _fail("mode mismatch after apply: " + rel)
        status_rows = set(applied["status"].splitlines())
        if status_rows != set(EXPECTED_STATUS21):
            return _fail("applied status != exact expected21 rows: missing=" +
                         str(sorted(set(EXPECTED_STATUS21) - status_rows)) + " extra=" +
                         str(sorted(status_rows - set(EXPECTED_STATUS21))))
        if len(applied["status"].splitlines()) != 21:
            return _fail("applied status len != 21")
        post_check = _freeze_full(source, env)
        for rel in sorted(CANONICAL21):
            if post_check["files"].get(rel, {}).get("sha256") != active["files"].get(rel, {}).get("sha256"):
                return _fail("source changed during proof: " + rel)
        _log("APPLY_PROOF_OK head=" + str(applied["head"]) + " files=21 patch=" + patch_sha[:12])
        return _emit(0)
    except (ProofFailed, RuntimeError, OSError) as exc:
        try:
            _log("PROOF_REFUSAL: " + type(exc).__name__ + ": " + str(exc))
        except Exception:
            pass
        return _emit(40)

if __name__ == "__main__":
    import sys as _sys
    _sys.exit(main())
