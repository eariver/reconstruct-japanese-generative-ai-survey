#!/usr/bin/env python3
"""Direct runner for bare-function tests (no pytest, no pip, no network).

Enumerates callables _pytest-style test_* with only actual required fixture
args via inspect (functions may take no args), executes actual assertions via
direct calls (not pytest, not unittest wrapper), traces results per test,
child exit 0 on full PASS (fail-closed otherwise). Uses valid original
fixtures (real files + FD-safe reads, real repo via RENEWAL_TEST_REPO or file
ancestors), not minimal noGit archives. No performance padding (no timing
asserts, no extra perf tests).

Owned: tests/test_versioned_renewal_freeze_transitive_correction_20261025.py
(6 funcs) + tests/test_group_c_editorial_consumers_v2.py (9 funcs).
"""
from __future__ import annotations

import inspect
import sys
import traceback
from pathlib import Path


def _repo_root() -> Path:
    override = Path(__file__).resolve()
    # Runner lives in notes/.../test-fixture-corrections/, repo is workspace root
    # with .rephase-1-editorial-runtime/. Find via ancestors.
    cur = override
    for parent in [cur.parent, *cur.parents]:
        if (parent / ".rephase-1-editorial-runtime").is_dir():
            return parent
    # Fallback: env or TESTSRC via arg?
    import os
    env = os.environ.get("RENEWAL_TEST_REPO", "")
    if env:
        return Path(env).resolve()
    raise RuntimeError("cannot locate repo root for bare runner")


def _load_module(repo: Path, modname: str):
    import importlib
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    try:
        return importlib.import_module(modname)
    finally:
        # Keep repo first for subsequent loads (same root, no drift).
        pass


def _collect(mod) -> list:
    out = []
    for name, fn in inspect.getmembers(mod, predicate=inspect.isfunction):
        if name.startswith("test_"):
            out.append((name, fn))
    return sorted(out, key=lambda x: x[0])


def _call_with_fixtures(name: str, fn) -> None:
    # Only actual required fixture args via inspect; functions may take no args.
    # Currently all 15 take no args (verified). If future bare funcs require
    # fixtures, provide valid original fixtures here (real files, not minimal
    # noGit archives), never dummy. No performance padding.
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())
    # Filter out *args/**kwargs? Bare tests take no args; if they take args,
    # fail closed (do not invent fixtures).
    required = [p for p in params if p.default is inspect.Parameter.empty and p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)]
    if required:
        raise AssertionError(f"bare {name} requires fixture args {[p.name for p in required]} (no dummy fixtures)")
    # No args: direct call, actual assertions inside.
    fn()


def main() -> int:
    import os
    repo_arg = os.environ.get("RENEWAL_TEST_REPO", "")
    if len(sys.argv) > 1:
        repo = Path(sys.argv[1]).resolve()
    elif repo_arg:
        repo = Path(repo_arg).resolve()
    else:
        # Default: TESTSRC new DST (own patch snapshot) via sibling runtime?
        # Runner lives in notes, repo is workspace root's TESTSRC new DST?
        # Use env or arg; fallback to reconstruct root's TESTSRC new DST?
        # For final evidence, pass DST explicitly via argv or env.
        # Fallback: find TESTSRC new DST via .rephase-1-editorial-runtime?
        base = _repo_root()
        # New OWN test-source snapshot (before authority, with OWN patches).
        cand = base / ".rephase-1-editorial-runtime" / "versioned-renewal-test-fixture-corrections-20261025T153000Z" / "test-source"
        if cand.is_dir():
            repo = cand
        else:
            # Fallback to affected-regress TESTSRC (old, for local dev only).
            repo = base / ".rephase-1-editorial-runtime" / "versioned-renewal-affected-regress-20261025T143000Z" / "test-source"
    if not (repo / "scripts" / "survey_publication_v2.py").exists():
        print(f"FAIL: repo root missing scripts/survey_publication_v2.py: {repo}", file=sys.stderr)
        return 1
    # Ensure repo first (same root for loaded modules and repo_root, no overriding).
    if str(repo) in sys.path:
        sys.path.remove(str(repo))
    sys.path.insert(0, str(repo))
    # Also ensure notes runner dir not shadowing tests.
    mods = [
        "tests.test_versioned_renewal_freeze_transitive_correction_20261025",
        "tests.test_group_c_editorial_consumers_v2",
    ]
    total = 0
    passed = 0
    failed = 0
    details: list[str] = []
    for modname in mods:
        try:
            mod = _load_module(repo, modname)
        except Exception as exc:
            print(f"FAIL load {modname}: {exc}", file=sys.stderr)
            traceback.print_exc()
            return 1
        for name, fn in _collect(mod):
            total += 1
            label = f"{modname}.{name}"
            try:
                _call_with_fixtures(name, fn)
                passed += 1
                details.append(f"PASS {label}")
                print(f"PASS {label}")
            except Exception as exc:
                failed += 1
                tb = traceback.format_exc()
                details.append(f"FAIL {label}: {exc}\n{tb}")
                print(f"FAIL {label}: {exc}")
                print(tb)
    print(f"bare-direct: {passed}/{total} PASS, {failed} FAIL")
    return 0 if (failed == 0 and total == 15) else 1


if __name__ == "__main__":
    raise SystemExit(main())
