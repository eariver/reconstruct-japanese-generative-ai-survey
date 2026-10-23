#!/usr/bin/env python3
"""R6 readonly candidate-selection proof (no writes, no predicate exec).

Usage: readonly-selection-r6-20261023T010000Z.py FIX_ROOT EXPECT_HEAD EXPECT_TREE EXPECT_COUNT ISSUE ACTIVE_ID

Readonly: loads the canonical current State (validated Profile/config), runs
the real low-level resolve_publication_selection, and asserts the State-bound
selection is VERSIONED_ACTIVE on the exact expected versioned candidate with
byte-identical SHA. No State/receipt/Gate/Candidate writes, no git writes,
no network. Proves the readonly candidate SHA selects the right one of the
two sealed candidates (r6-1 superseded vs r6-2 active).

Saved BEFORE execution.
"""
from __future__ import annotations
import hashlib
import os
import pathlib
import subprocess
import sys
import traceback
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER: PYTHONDONTWRITEBYTECODE!=1 (set BEFORE python startup)", flush=True)
    sys.exit(2)
_fr = os.environ.get("FINAL_R6_ROOT", "")
if not _fr or not Path(_fr).is_dir():
    print(f"BLOCKER: FINAL_R6_ROOT missing/not-a-dir: {_fr!r}", flush=True)
    sys.exit(2)
for _k in ("PYTHONPYCACHEPREFIX", "TMPDIR"):
    if not os.environ.get(_k, "").startswith(_fr + "/"):
        print(f"BLOCKER {_k} must be under FINAL_R6_ROOT, got {os.environ.get(_k)!r}", flush=True)
        sys.exit(2)
for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
    if os.environ.get(_v):
        print(f"BLOCKER unsafe inherited {_v}", flush=True)
        sys.exit(2)


def _log(m: str):
    print(m, flush=True)


def _run_git(root: Path, *args: str):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, timeout=120, env=env)


def main() -> int:
    if len(sys.argv) != 7:
        print(f"usage: {sys.argv[0]} FIX_ROOT EXPECT_HEAD EXPECT_TREE EXPECT_COUNT ISSUE ACTIVE_ID",
              flush=True)
        return 2
    root = Path(sys.argv[1]).resolve()
    exp_head, exp_tree = sys.argv[2].strip().lower(), sys.argv[3].strip().lower()
    exp_count, issue, active_id = int(sys.argv[4]), sys.argv[5], sys.argv[6]
    if [p for p in sys.path if "/jgas-" in p or "/dev/shm/" in p or "/tmp/opencode" in p]:
        print("BLOCKER: foreign fixture path pre-seeded on sys.path", flush=True)
        return 2
    sys.path.insert(0, str(root))
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    import scripts as _pkg
    if list(getattr(_pkg, "__path__", [])) != [str(root / "scripts")]:
        print(f"BLOCKER scripts namespace not single-root", flush=True)
        return 2
    try:
        return _run(root, exp_head, exp_tree, exp_count, issue, active_id)
    except SystemExit:
        raise
    except BaseException:
        print("READONLY_SELECTION FAILED (exit nonzero, never a hidden pass)", flush=True)
        traceback.print_exc()
        return 2


def _run(root, exp_head, exp_tree, exp_count, issue, active_id) -> int:
    import scripts.survey_production_v2 as core
    import scripts.survey_publication_set_v2 as setmod
    for n, m in list(sys.modules.items()):
        if (n == "scripts" or n.startswith("scripts.")) and getattr(m, "__file__", None) is not None:
            if not str(Path(getattr(m, "__file__")).resolve()).startswith(str(root)):
                print(f"BLOCKER code binding outside fixture: {n}", flush=True)
                return 2
    head = _run_git(root, "rev-parse", "HEAD").stdout.strip()
    tree = _run_git(root, "rev-parse", "HEAD^{tree}").stdout.strip()
    if head != exp_head or tree != exp_tree:
        print(f"BLOCKER source identity mismatch: {head}/{tree}", flush=True)
        return 2
    if len(_run_git(root, "ls-files").stdout.strip().splitlines()) != exp_count:
        print("BLOCKER LSFILES count mismatch", flush=True)
        return 2
    top = _run_git(root, "rev-parse", "--show-toplevel").stdout.strip()
    gdir = _run_git(root, "rev-parse", "--absolute-git-dir").stdout.strip()
    if Path(top) != root or Path(gdir) != root / ".git":
        print(f"BLOCKER fixture .git not owned", flush=True)
        return 2
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    before = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}
    st = core.load_json(root / f"sources/{issue}/production-state.json")
    sel = setmod.resolve_publication_selection(root, cfg, st)
    assert sel.get("mode") == "VERSIONED_ACTIVE", sel.get("mode")
    exp_rel = (f"sources/{issue}/publication/v2/editorial-corrections/"
               f"{active_id}/publication/publication-candidate-v2.json")
    pin = sel.get("candidate_ref") or {}
    assert pin.get("path") == exp_rel, (pin.get("path"), exp_rel)
    actual_sha = hashlib.sha256((root / exp_rel).read_bytes()).hexdigest()
    assert actual_sha == pin.get("sha256"), (actual_sha, pin.get("sha256"))
    old_rel = exp_rel.replace(active_id, active_id[:-1] + "1")
    assert old_rel != exp_rel and (root / old_rel).is_file(), "superseded r6-1 candidate must exist"
    assert pin.get("path") != old_rel, "selection must not point at superseded r6-1"
    after = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}
    assert after == before, "readonly proof wrote files"
    _log(f"READONLY_SELECTION_OK issue={issue} mode=VERSIONED_ACTIVE candidate={exp_rel} "
         f"sha={actual_sha[:12]} superseded-distinct-ok nowrite-ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException:
        print("PARTIAL readonly-selection (unexpected, nonzero)", flush=True)
        traceback.print_exc()
        sys.exit(2)
