#!/usr/bin/env python3
"""R4c isolated per-fixture Longform receipt after RELEASED (no harness mixing).

Usage: python3 test-r4c-longform-receipt-isolated.py <fixture-root> <issue-id> <active-id>

Isolation contract (checked, fail-closed):
- Exactly one /tmp/opencode/jgas-* root on sys.path (the fixture itself).
- Purge any pre-imported scripts.* modules, then import from fixture only.
- Verify code binding: every imported scripts.* module __file__ is under fixture root.
- No Weekly/other-fixture namespace in this process.
- Call survey_editorial_publication_v2.validate_editorial_receipt on the
  RELEASED State + active validated-source-manifest (no mocks, no wrapper).

Saved BEFORE execution. No fixture/source mutation, no pycache in source
(requires PYTHONDONTWRITEBYTECODE=1 + PYTHONPYCACHEPREFIX=/tmp/... set BEFORE
python startup).
"""
from __future__ import annotations
import os
import sys
import pathlib

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER: PYTHONDONTWRITEBYTECODE!=1 (set BEFORE python startup)", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith("/tmp/"):
    print(f"BLOCKER: PYTHONPYCACHEPREFIX must be /tmp/... external, got {_pfx!r}", flush=True)
    sys.exit(2)


def main() -> int:
    if len(sys.argv) != 4:
        print(f"usage: {sys.argv[0]} <fixture-root> <issue-id> <active-id>", flush=True)
        return 2
    root = pathlib.Path(sys.argv[1]).resolve()
    issue = sys.argv[2]
    active = sys.argv[3]
    print(f"FIXTURE={root} ISSUE={issue} ACTIVE={active}", flush=True)
    if not (root / "scripts" / "survey_editorial_publication_v2.py").is_file():
        print("BLOCKER: fixture scripts missing", flush=True)
        return 2
    # 1. sys.path must contain exactly this one jgas root (plus stdlib).
    bad = [p for p in sys.path if "/tmp/opencode/jgas-" in p and pathlib.Path(p).resolve() != root]
    if bad:
        print(f"BLOCKER: mixed fixture namespace on sys.path: {bad}", flush=True)
        return 2
    # Put fixture root first, drop any other jgas entries.
    sys.path = [str(root)] + [p for p in sys.path if "/tmp/opencode/jgas-" not in p]
    # 2. Purge pre-imported scripts.* modules.
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    # 3. Import from fixture only.
    import scripts.survey_production_v2 as core
    import scripts.survey_publication_set_v2 as setmod
    import scripts.survey_editorial_publication_v2 as edpub
    # 4. Verify code binding: every scripts.* module file under fixture root.
    import sys as _sys
    badmod = []
    for name, mod in _sys.modules.items():
        if name == "scripts" or name.startswith("scripts."):
            f = getattr(mod, "__file__", None)
            if f is None:
                continue
            try:
                pathlib.Path(f).resolve().relative_to(root)
            except ValueError:
                badmod.append((name, f))
    if badmod:
        print(f"BLOCKER: code binding outside fixture: {badmod}", flush=True)
        return 2
    print(f"BINDING_OK edpub={pathlib.Path(edpub.__file__).resolve()}", flush=True)
    # 5. No Weekly/other-fixture modules: scripts package path must be single-root.
    import scripts as _pkg
    paths = list(getattr(_pkg, "__path__", []))
    if len(paths) != 1 or pathlib.Path(paths[0]).resolve() != (root / "scripts").resolve():
        print(f"BLOCKER: scripts namespace not single-root: {paths}", flush=True)
        return 2
    print(f"NAMESPACE_SINGLE_ROOT_OK {paths}", flush=True)
    # 6. Actual receipt on RELEASED State (no mocks).
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    state_rel = f"sources/{issue}/production-state.json"
    st = core.load_json(root / state_rel)
    print(f"STATE lifecycle={st.get('lifecycle_state')} pointer={(st.get('publication_revalidation_provenance') or {}).get('path')}", flush=True)
    if st.get("lifecycle_state") not in ("FROZEN", "RELEASED"):
        print(f"BLOCKER: expected post-lifecycle State, got {st.get('lifecycle_state')}", flush=True)
        return 2
    sel = setmod.resolve_publication_selection(root, cfg, st)
    print(f"SELECTION mode={sel.get('mode')} cand={(sel.get('candidate_ref') or {}).get('path')}", flush=True)
    receipt_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active}/publication/validated-source-manifest.json"
    if not (root / receipt_rel).is_file():
        print(f"BLOCKER: receipt missing {receipt_rel}", flush=True)
        return 2
    try:
        rv = edpub.validate_editorial_receipt(root, receipt_rel, state_rel)
    except Exception as exc:
        print(f"RECEIPT_FAIL {type(exc).__name__}: {exc}", flush=True)
        import traceback
        traceback.print_exc()
        return 1
    print(f"RECEIPT_PASS issue={rv.get('issue_id')} route={rv.get('generator_route')}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
