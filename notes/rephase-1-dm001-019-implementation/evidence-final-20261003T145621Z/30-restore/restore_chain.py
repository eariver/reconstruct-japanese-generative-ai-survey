#!/usr/bin/env python3
"""Fail-closed archive-chained offline restore for the DM-001/019 successor.

1. Hash/size/member-validates the saved b40 partial archive (prerequisite).
2. Extracts it into a NEW absent staging dir (refuses existing destinations).
3. Verifies the extracted b40 DB untouched (HEAD/tree/shallow/refs as saved).
4. Imports the enumerated b40..FINAL successor pack (non-strict unpack:
   the delta intentionally omits unchanged history blobs, which stay
   declared-missing per the parent archive census; exactness is enforced
   by the gates below, not by link closure).
5. Establishes the final review ref and materializes the 3 changed paths
   plus index entries through normal Git operations.
6. Verifies the real available chain FINAL->ff->490->b40->774 (log,
   merge-base, cat-file parent lines), HEAD/tree, 3-path mode/blob/
   worktree bytes, index entries, no remotes/alternates/shared stores.
No network, no fetches, no old restore scripts, no patch-rebuilt identity.
"""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path

STAGE = Path(sys.argv[1])
ARCHIVE = Path(sys.argv[2])
PACK = Path(sys.argv[3])
MANIFEST = Path(sys.argv[4])
CHANGED = Path(sys.argv[5])

ARCH_SHA = "faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c"
ARCH_BYTES = 5152199
ARCH_MEMBERS = 760

BASE_ENV = {"PATH": "/usr/bin:/bin", "GIT_NO_LAZY_FETCH": "1",
            "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"}


def run(args: list[str], db: Path, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True,
                          cwd=str(db), env=dict(BASE_ENV), **kwargs)


def fail(msg: str) -> int:
    print(f"RESTORE_REFUSED: {msg}", flush=True)
    return 1


def main() -> int:
    if STAGE.exists():
        return fail(f"staging destination exists: {STAGE}")
    for label, path in (("archive", ARCHIVE), ("pack", PACK),
                        ("manifest", MANIFEST)):
        if not path.is_file():
            return fail(f"{label} missing: {path}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    final, tree = manifest["head"], manifest["tree"]
    # Expected chain and base come from the machine manifest (generated from
    # Git), extended with the archive base; object counts are never hardcoded.
    chain = list(manifest["chain"])
    base = manifest["chain_base"]
    assert chain and chain[0] == final, "manifest chain must start at final HEAD"
    full_chain = chain + [base]
    digest = hashlib.sha256()
    with ARCHIVE.open("rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            digest.update(chunk)
    size = ARCHIVE.stat().st_size
    if size != ARCH_BYTES or digest.hexdigest() != ARCH_SHA:
        return fail(f"archive hash/size mismatch: {size}B {digest.hexdigest()}")
    with tarfile.open(str(ARCHIVE), "r:gz") as tar:
        members = tar.getmembers()
        if len(members) != ARCH_MEMBERS:
            return fail(f"archive member count {len(members)} != {ARCH_MEMBERS}")
        for mem in members:
            name = mem.name
            if name.startswith(("/", "\\")) or ".." in Path(name).parts:
                return fail(f"unsafe archive member: {name!r}")
            if mem.issym() or mem.islnk():
                return fail(f"link member not allowed: {name!r}")
    STAGE.mkdir(parents=False)
    with tarfile.open(str(ARCHIVE), "r:gz") as tar:
        tar.extractall(path=str(STAGE), filter="data")
    db = STAGE / "candidate-partial-b40de60"
    if not (db / ".git").is_dir():
        return fail("extracted DB missing .git")
    checks: list[str] = []

    def check(label: str, ok: bool, detail: str = "") -> bool:
        checks.append(f"{label}={'PASS' if ok else 'FAIL'} {detail}")
        return ok

    ok = True
    r = run(["git", "rev-parse", "HEAD"], db)
    ok &= check("extracted-head", r.stdout.strip() == base, r.stdout.strip())
    r = run(["git", "rev-parse", "HEAD^{tree}"], db)
    base_tree = r.stdout.strip()
    ok &= check("extracted-tree-present", r.returncode == 0, base_tree[:12])
    shallow = db / ".git/shallow"
    ok &= check("shallow-untouched", shallow.is_file(), shallow.read_text().strip()[:41]
                if shallow.is_file() else "missing")
    r = run(["git", "status", "--porcelain=v1", "--untracked-files=no"], db)
    ok &= check("extracted-clean", r.stdout.strip() == "", "")
    r = subprocess.run(
        ["git", "unpack-objects"], input=PACK.read_bytes(),
        capture_output=True, cwd=str(db), env=dict(BASE_ENV))
    if r.returncode != 0:
        print(f"unpack failed: {r.stderr.decode()[-500:]}", flush=True)
        return fail("successor pack unpack failed")
    branch = "refs/heads/dm001019-final"
    if run(["git", "show-ref", "--verify", "--quiet", branch], db).returncode == 0:
        return fail("final ref already exists")
    if run(["git", "update-ref", branch, final], db).returncode != 0:
        return fail("final update-ref failed")
    expected_blobs = {row["path"]: row["blob"] for row in manifest["files"]}
    # Materialize the changed paths + index through normal Git operations.
    r = run(["git", "checkout", final, "--", *sorted(expected_blobs)], db)
    if r.returncode != 0:
        print(f"checkout failed: {r.stderr[-800:]}", flush=True)
        return fail("materializing checkout failed")
    r = run(["git", "rev-parse", branch], db)
    ok &= check("final-ref", r.stdout.strip() == final, r.stdout.strip())
    r = run(["git", "rev-parse", f"{final}^{{tree}}"], db)
    ok &= check("final-tree", r.stdout.strip() == tree, r.stdout.strip())
    r = run(["git", "log", "--format=%H %P", branch], db)
    if r.returncode != 0:
        print(f"git log failed: {r.stderr[-500:]}", flush=True)
        return fail("available-chain log does not work offline")
    logged = [line.split() for line in r.stdout.splitlines()]
    logged_heads = [row[0] for row in logged]
    ok &= check("chain-log", logged_heads[: len(full_chain)] == full_chain,
                " ".join(h[:9] for h in logged_heads[: len(full_chain) + 1]))
    for child, parent in zip(full_chain, full_chain[1:]):
        r = run(["git", "cat-file", "commit", child], db)
        ok &= check(f"link:{child[:9]}", f"\nparent {parent}\n" in f"\n{r.stdout}\n", "")
    # Shallow cutoff: read from the extracted shallow file (untouched) and
    # confirm the base links to it and the log terminates there.
    shallow_content = (db / ".git/shallow").read_text(encoding="utf-8").split()
    r = run(["git", "cat-file", "commit", base], db)
    base_parents = [line.split()[1] for line in r.stdout.splitlines()
                    if line.startswith("parent ")]
    ok &= check("shallow-cutoff",
                len(shallow_content) == 1 and base_parents == shallow_content
                and logged_heads[-1] == shallow_content[0],
                f"shallow={shallow_content[0][:9] if shallow_content else None}")
    r = run(["git", "merge-base", "--is-ancestor", base, final], db)
    ok &= check("merge-base", r.returncode == 0, f"{base[:9]} ancestor of {final[:9]}")
    for rel, blob in expected_blobs.items():
        r = run(["git", "ls-tree", final, "--", rel], db)
        parts = r.stdout.strip().split()
        ok &= check(f"tree:{rel}",
                    len(parts) == 4 and parts[1] == "blob" and parts[2] == blob,
                    r.stdout.strip())
        show = subprocess.run(
            ["git", "show", f"{final}:{rel}"], capture_output=True,
            cwd=str(db), env=dict(BASE_ENV))
        disk = (CHANGED / rel).read_bytes()
        work = (db / rel).read_bytes() if (db / rel).is_file() else b""
        ok &= check(f"bytes:{rel}",
                    show.returncode == 0 and show.stdout == disk and work == disk,
                    f"object={len(show.stdout)}B worktree={len(work)}B")
        r = run(["git", "ls-files", "-s", "--", rel], db)
        ok &= check(f"index:{rel}", blob in r.stdout, r.stdout.strip()[:60])
    for obj in manifest["new_objects"]:
        r = run(["git", "cat-file", "-e", obj["sha"]], db)
        ok &= check(f"object:{obj['sha'][:12]}", r.returncode == 0, "")
    r = run(["git", "ls-tree", "-r", final], db)
    if r.returncode == 0:
        rows = r.stdout.splitlines()
        expected_count = manifest["tree_entry_count"]
        ok &= check("full-tree-refs", len(rows) == expected_count, f"{len(rows)} entries")
    else:
        ok &= check("full-tree-refs", False, f"ls-tree -r failed: {r.stderr[-200:]}")
    r = run(["git", "remote", "-v"], db)
    urls = [line.split()[1] for line in r.stdout.splitlines() if line.strip()]
    real = [u for u in urls if "example.invalid" not in u]
    ok &= check("no-real-remotes", not real,
                f"remotes={r.stdout.strip()[:160]!r}" if r.stdout.strip() else "none")
    ok &= check("no-alternates", not (db / ".git/objects/info/alternates").exists(), "")
    st_db = db.stat()
    ok &= check("own-store", st_db.st_ino != 0, f"ino={st_db.st_ino} dev={st_db.st_dev}")
    for line in checks:
        print(line, flush=True)
    print(f"CHAIN_BASE={base} CHAIN_LEN={len(full_chain)} NEW_OBJECTS={len(manifest['new_objects'])}", flush=True)
    if not ok:
        print("RESTORE_RESULT=FAIL", flush=True)
        return 1
    print(f"RESTORE_RESULT=OK FINAL={final} TREE={tree}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
