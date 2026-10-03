#!/usr/bin/env python3
"""Generate successor packaging manifest from parsed git output (no manual SHA transcription)."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

IMPL = Path("/tmp/opencode/jgas-dm001019-impl-20261003T100801Z")
OUT = Path(sys.argv[1])
# Declared enumeration base: the fixed-baseline recovery candidate. All
# counts, chains and object IDs below are read from Git, not transcribed.
RANGE_BASE = "b40de600e9ed1f80cb278213ccf17aa5f3cd9de3"


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(IMPL), *args],
        capture_output=True, text=True, check=True,
        env={"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
             "GIT_ALLOW_PROTOCOL": "file", "PATH": "/usr/bin:/bin"},
    )
    return proc.stdout


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


head = git("rev-parse", "HEAD").strip()
tree = git("rev-parse", "HEAD^{tree}").strip()
parent = git("rev-parse", "HEAD^").strip()
parent_tree = git("rev-parse", "HEAD^{tree}^").strip() if False else None

files = []
for line in git("ls-tree", "-r", "--format=%(objectmode) %(objectname) %(path)", "HEAD",
                "--", "scripts/survey_publication_v2.py",
                "scripts/survey_profiled_freeze_v2.py",
                "tests/test_survey_dm001_019_freeze_equivalence_v2.py").splitlines():
    mode, blob, path = line.split(" ", 2)
    files.append({"path": path, "mode": mode, "blob": blob,
                  "worktree_sha256": sha256_file(IMPL / path)})

patch_path = OUT / "successor.patch"
patch_bytes = subprocess.run(
    ["git", "-C", str(IMPL), "format-patch", "--stdout",
     f"{RANGE_BASE}..{head}", "--",
     "scripts/survey_publication_v2.py",
     "scripts/survey_profiled_freeze_v2.py",
     "tests/test_survey_dm001_019_freeze_equivalence_v2.py"],
    capture_output=True, check=True,
    env={"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
         "GIT_ALLOW_PROTOCOL": "file", "PATH": "/usr/bin:/bin"},
).stdout
patch_path.write_bytes(patch_bytes)

objects = []
for line in git("rev-list", "--objects", f"{RANGE_BASE}..{head}").splitlines():
    parts = line.split(" ", 1)
    objects.append({"sha": parts[0], "path": parts[1] if len(parts) > 1 else None})

manifest = {
    "head": head,
    "tree": tree,
    "direct_parent": parent,
    "parent_tree": git("rev-parse", f"{parent}^{{tree}}").strip(),
    "branch": git("branch", "--show-current").strip(),
    "chain": git("log", "--format=%H", f"{RANGE_BASE}..{head}").split(),
    "chain_base": RANGE_BASE,
    "tree_entry_count": sum(1 for _ in git("ls-tree", "-r", head).splitlines()),
    "files": files,
    "patch": {"path": "successor.patch",
              "sha256": hashlib.sha256(patch_bytes).hexdigest(),
              "bytes": len(patch_bytes)},
    "new_objects": objects,
    "log": git("log", "--format=%H %P %s").strip(),
}
(OUT / "successor-manifest.json").write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps({"head": head, "tree": tree, "parent": parent,
                  "files": len(files), "objects": len(objects)}, indent=1))
