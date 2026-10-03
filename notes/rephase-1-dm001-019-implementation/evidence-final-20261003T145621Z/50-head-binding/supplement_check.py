#!/usr/bin/env python3
"""Head-binding supplement: actual restored HEAD/worktree + object accounting.

Read-only verification (no writes, no checkouts, no ref moves) over the
archive-chained restore DB after its normal `git switch dm001019-final`.
Machine-counts successor object types from Git, compares donor-vs-restored
object inodes (real no-sharing proof), and writes the final operational
manifest. Fails (exit 1) on any mismatch; preserves raw output.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

RESTORED = Path(sys.argv[1])
DONOR = Path(sys.argv[2])
OBJECT_LIST = Path(sys.argv[3])
PACK = Path(sys.argv[4])
ARCHIVE = Path(sys.argv[5])
OUT = Path(sys.argv[6])
PACK_MANIFEST = Path(sys.argv[7])

BASE_ENV = {"PATH": "/usr/bin:/bin", "GIT_NO_LAZY_FETCH": "1",
            "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"}


def git(args: list[str], db: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(db), *args], capture_output=True,
                          text=True, env=dict(BASE_ENV))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    raw: list[str] = []
    ok = True

    def check(label: str, passed: bool, detail: str = "") -> None:
        nonlocal ok
        raw.append(f"{label}={'PASS' if passed else 'FAIL'} {detail}")
        if not passed:
            ok = False

    shas = [line.split()[0] for line in OBJECT_LIST.read_text().splitlines() if line.strip()]
    # 1. Object types machine-counted from Git (restored DB proves availability).
    batch = subprocess.run(
        ["git", "-C", str(RESTORED), "cat-file", "--batch-check"],
        input="".join(s + "\n" for s in shas),
        capture_output=True, text=True, env=dict(BASE_ENV))
    types: dict[str, int] = {}
    present = 0
    for line in batch.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] in ("commit", "tree", "blob"):
            types[parts[1]] = types.get(parts[1], 0) + 1
            present += 1
    check("object-count", present == len(shas), f"{present}/{len(shas)}")
    check("object-types", types == {"commit": 3, "tree": 9, "blob": 8}, json.dumps(types, sort_keys=True))
    # 2. Restored HEAD/worktree binding.
    head = git(["rev-parse", "HEAD"], RESTORED).stdout.strip()
    tree = git(["rev-parse", "HEAD^{tree}"], RESTORED).stdout.strip()
    symref = git(["symbolic-ref", "HEAD"], RESTORED).stdout.strip()
    check("head-branch", symref == "refs/heads/dm001019-final", symref)
    st_tracked = git(["status", "--porcelain=v1", "--untracked-files=no"], RESTORED)
    check("tracked-clean", st_tracked.stdout.strip() == "", "")
    st_full = git(["status", "--porcelain=v1"], RESTORED)
    check("worktree-clean", st_full.stdout.strip() == "", st_full.stdout.strip()[:200])
    check("diff-head-empty", git(["diff", "HEAD", "--stat"], RESTORED).stdout.strip() == "", "")
    check("diff-cached-empty", git(["diff", "--cached", "--stat"], RESTORED).stdout.strip() == "", "")
    log = git(["log", "--format=%H %P"], RESTORED).stdout.splitlines()
    heads = [line.split()[0] for line in log]
    check("chain-head", heads[0] == head, heads[0][:12])
    base_check = git(["merge-base", "--is-ancestor", heads[-2], head], RESTORED)
    check("chain-ancestor", base_check.returncode == 0, "")
    # 3. Donor-vs-restored inode comparison (real no-sharing proof).
    def inventory(root: Path) -> dict[tuple[int, int], str]:
        table: dict[tuple[int, int], str] = {}
        for dirpath, _dirnames, filenames in os.walk(root / ".git/objects"):
            for name in filenames:
                p = Path(dirpath) / name
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                table.setdefault((st.st_dev, st.st_ino), str(p))
        return table
    donor_files = inventory(DONOR)
    restored_files = inventory(RESTORED)
    shared = [p for key, p in restored_files.items() if key in donor_files]
    check("no-shared-inodes", not shared, f"{len(restored_files)} restored files, shared={shared[:3]}")
    multi_linked = []
    for dirpath, _dirnames, filenames in os.walk(RESTORED / ".git/objects"):
        for name in filenames:
            p = Path(dirpath) / name
            try:
                if os.lstat(p).st_nlink != 1:
                    multi_linked.append(str(p))
            except OSError:
                pass
    check("no-hardlinks", not multi_linked, f"{multi_linked[:3]}")
    check("donor-no-alternates", not (DONOR / ".git/objects/info/alternates").exists(), "")
    check("restored-no-alternates",
          not (RESTORED / ".git/objects/info/alternates").exists(), "")
    # 4. Operational manifest.
    ls3 = {}
    for rel in ("scripts/survey_publication_v2.py",
                "scripts/survey_profiled_freeze_v2.py",
                "tests/test_survey_dm001_019_freeze_equivalence_v2.py"):
        ls = git(["ls-tree", "HEAD", "--", rel], RESTORED).stdout.strip().split()
        work = hashlib.sha256((RESTORED / rel).read_bytes()).hexdigest()
        ls3[rel] = {"mode": ls[0], "blob": ls[2], "worktree_sha256": work}
    pack_manifest = json.loads(PACK_MANIFEST.read_text(encoding="utf-8"))
    manifest = {
        "source_db": str(DONOR),
        "restored_db": str(RESTORED),
        "restored_head": head,
        "restored_tree": tree,
        "restored_branch": symref,
        "parent_chain": heads,
        "final_commit_unchanged": head == pack_manifest["head"] and tree == pack_manifest["tree"],
        "paths": ls3,
        "parent_archive": {
            "path": str(ARCHIVE),
            "sha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
            "bytes": ARCHIVE.stat().st_size,
        },
        "successor_pack": {
            "path": str(PACK),
            "sha256": hashlib.sha256(PACK.read_bytes()).hexdigest(),
            "bytes": PACK.stat().st_size,
            "object_total": len(shas),
            "object_types": types,
        },
    }
    (OUT / "final-operational-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (OUT / "supplement-raw.log").write_text("\n".join(raw) + "\n", encoding="utf-8")
    for line in raw:
        print(line, flush=True)
    print(f"SUPPLEMENT_RESULT={'OK' if ok else 'FAIL'}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
