#!/usr/bin/env python3
"""Independent clean409 saved-patch proof, final v6 code (v2, R6-hardened).

v2 applies the EXACT saved v2 patch (final module 77ee2a3e / test 22f56041)
in a NEW disposable byte-copy reverted to clean409. Hardened vs impl v1 per
R6: whole-.git regular-entry inode separation (every regular .git file must
differ in (dev,ino) between active and copy; symlinks inside .git listed and
refused), alternates absent in BOTH, exact effective remote/config
observations with checked Git rc, full raw status, exact16 sha/bytes/mode
pins vs active. Only declared overlay removals in the disposable COPY
(16 paths + pycache dirs, with pre-removal cache inventory recorded); no
commits/branches/network, no active add-N, no active writes.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat as _stat
import subprocess
import sys
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60")
COPYROOT = Path("/tmp/opencode/jgas-dm021p2r-verify-20261014T000000Z")
COPYREPO = COPYROOT / "candidate-partial-b40de60"
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p2r/evidence-20261013T173500Z-correction")
PATCH = EVID / "complete-p2r-16path-v2.patch"
OUT_STDOUT = EVID / "proof_apply16_v2.stdout.txt"
OUT_STDERR = EVID / "proof_apply16_v2.stderr.txt"
OUT_EXIT = EVID / "proof_apply16_v2.exit"
OUT_CLEAN = EVID / "proof-freeze-clean-v2.json"
OUT_APPLIED = EVID / "proof-freeze-applied-v2.json"
MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]
LOG: list[str] = []


def log(msg: str) -> None:
    LOG.append(msg)
    print(msg)


def fail(msg: str) -> int:
    log(f"PROOF_REFUSAL: {msg}")
    OUT_STDOUT.write_text("\n".join(LOG) + "\n", encoding="utf-8")
    OUT_STDERR.write_text("\n".join(LOG) + "\n", encoding="utf-8")
    OUT_EXIT.write_text("40\n")
    return 40


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)


def git_checked(repo: Path, *args: str) -> str:
    r = git(repo, *args)
    if r.returncode != 0:
        raise RuntimeError(f"git {list(args)} rc={r.returncode}: {r.stderr[:500]}")
    return r.stdout


def git_entries(repo: Path) -> tuple[dict[str, tuple[int, int]], list[str]]:
    """Map every regular .git entry rel -> (dev,ino); list symlinks/others."""
    gitdir = repo / ".git"
    regular: dict[str, tuple[int, int]] = {}
    odd: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(gitdir, followlinks=False):
        for name in filenames:
            fp = Path(dirpath) / name
            try:
                rel = fp.relative_to(gitdir).as_posix()
            except ValueError:
                odd.append(f"escapes-gitdir: {fp}")
                continue
            try:
                st = os.lstat(fp)
            except OSError as exc:
                odd.append(f"unreadable: {rel}: {exc}")
                continue
            if _stat.S_ISLNK(st.st_mode):
                odd.append(f"symlink: {rel}")
            elif _stat.S_ISREG(st.st_mode):
                regular[rel] = (st.st_dev, st.st_ino)
            else:
                odd.append(f"non-regular: {rel}")
    return regular, odd


def freeze(repo: Path) -> dict:
    out: dict = {}
    out["head"] = git_checked(repo, "rev-parse", "HEAD").strip()
    out["tree"] = git_checked(repo, "rev-parse", "HEAD^{tree}").strip()
    out["status"] = git_checked(repo, "status", "--porcelain=v1", "-uall")
    out["index"] = git_checked(repo, "diff", "--cached", "--name-only")
    files: dict = {}
    for rel in MODIFIED + NEW:
        p = repo / rel
        files[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                      "mode": oct(p.stat().st_mode & 0o777), "bytes": p.stat().st_size}
    out["files"] = files
    return out


def main() -> int:
    for name in (OUT_STDOUT.name, OUT_STDERR.name, OUT_EXIT.name,
                 OUT_CLEAN.name, OUT_APPLIED.name):
        if (EVID / name).exists():
            return fail(f"proof output exists: {name}")
    if not PATCH.is_file():
        return fail("saved v2 patch missing")
    if COPYROOT.exists():
        return fail(f"copy destination exists: {COPYROOT}")
    try:
        patch_sha = hashlib.sha256(PATCH.read_bytes()).hexdigest()
        log(f"saved v2 patch sha256={patch_sha} bytes={PATCH.stat().st_size}")
        COPYROOT.mkdir(parents=True)
        proc = subprocess.run(["cp", "-a", "--reflink=never", str(ACTIVE), str(COPYREPO)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            return fail(f"byte-copy failed: {proc.stderr[:1000]}")
        # Whole-.git separation: no shared regular inodes, no symlinks.
        a_reg, a_odd = git_entries(ACTIVE)
        c_reg, c_odd = git_entries(COPYREPO)
        log(f"active .git regular entries={len(a_reg)} odd={a_odd}")
        log(f"copy .git regular entries={len(c_reg)} odd={c_odd}")
        if a_odd:
            return fail(f"active .git has non-regular entries: {a_odd[:10]}")
        if c_odd:
            return fail(f"copy .git has non-regular entries: {c_odd[:10]}")
        shared = [rel for rel in a_reg if rel in c_reg and a_reg[rel] == c_reg[rel]]
        if shared:
            return fail(f"copy shares .git inodes with active: {shared[:10]}")
        for repo, label in ((ACTIVE, "active"), (COPYREPO, "copy")):
            if (repo / ".git" / "objects" / "info" / "alternates").exists():
                return fail(f"{label} has alternates")
        # Exact effective remote/config observations (checked rc).
        for repo, label in ((ACTIVE, "active"), (COPYREPO, "copy")):
            remote = git_checked(repo, "remote", "-v")
            cfg = git_checked(repo, "config", "--list", "--show-origin")
            log(f"{label} remote -v:\n{remote.strip()}")
            if "example.invalid" not in remote:
                return fail(f"{label} origin not inert")
            if "example.invalid" not in cfg:
                return fail(f"{label} config lacks inert origin")
        # Record pre-removal cache inventory (no concealed deltas).
        caches_before = sorted(
            str(p.relative_to(COPYREPO).as_posix())
            for base in ("scripts", "tests", "schemas")
            for p in list((COPYREPO / base).glob("__pycache__/*")) + list((COPYREPO / base).glob("*.pyc")))
        log(f"copy caches before declared removal: {caches_before}")
        # Revert 16 overlays in COPY to clean409 (never in active).
        r = git(COPYREPO, "checkout", "HEAD", "--", *MODIFIED)
        if r.returncode != 0:
            return fail(f"copy checkout failed: {r.stderr[:1000]}")
        for n in NEW:
            try:
                (COPYREPO / n).unlink()
            except FileNotFoundError:
                return fail(f"copy new file already absent: {n}")
        for cache in (COPYREPO / "scripts" / "__pycache__", COPYREPO / "tests" / "__pycache__"):
            shutil.rmtree(cache, ignore_errors=True)
        head = git_checked(COPYREPO, "rev-parse", "HEAD").strip()
        tree = git_checked(COPYREPO, "rev-parse", "HEAD^{tree}").strip()
        status = git_checked(COPYREPO, "status", "--porcelain=v1", "-uall")
        if head != "409b292756dd1277b9dfae87679934c0d2ce251c" or status != "":
            return fail(f"copy not clean409: head={head} status={status[:500]!r}")
        OUT_CLEAN.write_text(json.dumps(
            {"head": head, "tree": tree, "status": status,
             "caches_removed": caches_before}, indent=2) + "\n")
        log("copy is clean409; applying EXACT saved v2 patch")
        r = git(COPYREPO, "apply", "--check", str(PATCH))
        if r.returncode != 0:
            return fail(f"apply --check failed: {r.stderr[:2000]}")
        r = git(COPYREPO, "apply", str(PATCH))
        if r.returncode != 0:
            return fail(f"apply failed: {r.stderr[:2000]}")
        applied = freeze(COPYREPO)
        OUT_APPLIED.write_text(json.dumps(applied, indent=2) + "\n")
        if applied["head"] != "409b292756dd1277b9dfae87679934c0d2ce251c":
            return fail("applied HEAD moved (must stay detached 409, uncommitted)")
        if applied["index"].strip() != "":
            return fail(f"applied index non-empty: {applied['index'][:200]!r}")
        # All16 bytes/modes/sha vs active.
        for rel in MODIFIED + NEW:
            a_data = (ACTIVE / rel).read_bytes()
            c_data = (COPYREPO / rel).read_bytes()
            if a_data != c_data:
                return fail(f"byte mismatch after apply: {rel}")
            if oct((ACTIVE / rel).stat().st_mode & 0o777) != oct((COPYREPO / rel).stat().st_mode & 0o777):
                return fail(f"mode mismatch after apply: {rel}")
        st = applied["status"]
        for m in MODIFIED:
            if f" M {m}" not in st:
                return fail(f"applied status missing M: {m}")
        for n in NEW:
            if f"?? {n}" not in st:
                return fail(f"applied status missing ??: {n}")
        log(f"APPLY_PROOF_OK head={applied['head']} files=16 patch={patch_sha[:12]}")
        OUT_STDOUT.write_text("\n".join(LOG) + "\n", encoding="utf-8")
        OUT_STDERR.write_text("", encoding="utf-8")
        OUT_EXIT.write_text("0\n")
        return 0
    except RuntimeError as exc:
        return fail(str(exc))


if __name__ == "__main__":
    sys.exit(main())
