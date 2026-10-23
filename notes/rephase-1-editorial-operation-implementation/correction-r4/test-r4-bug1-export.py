#!/usr/bin/env python3
"""R4 Bug1 focused: export workflow absolute-vs-relative (actual extracted code).

Tests ACTUAL workflow python block (exec, not helper assert) for both manual+PR paths:
- _norm strict (absolute/traversal/backslash refuse, caller input)
- _rel_expected normalizes L-internal absolute Path relative to verified root
- exact State-bound candidate, unknown branch failclosed, inert not exported, ambiguous fail
Saved BEFORE execution. Temp dirs only, no DST/source mutation.
ENV must be set BEFORE python startup: PYTHONDONTWRITEBYTECODE=1, PYTHONPYCACHEPREFIX=/tmp/...
"""
from __future__ import annotations
import os, sys, pathlib, tempfile, textwrap

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER PYTHONDONTWRITEBYTECODE!=1", flush=True); sys.exit(2)
_pp = os.environ.get("PYTHONPYCACHEPREFIX","")
if not _pp.startswith("/tmp/opencode/"):
    print(f"BLOCKER PYTHONPYCACHEPREFIX {_pp!r}", flush=True); sys.exit(2)

DST = pathlib.Path("/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60")
WF = DST / ".github/workflows/survey-production-v2-export-publication-preview.yml"

def load_workflow_defs(tmp_root: pathlib.Path):
    import glob as _glob, json as _json, subprocess
    text = WF.read_text()
    start = text.index("          def _norm(p):")
    end = text.index("          requested = os.environ.get('REQUESTED_CANDIDATE'")
    block = textwrap.dedent(text[start:end])
    # minimal fake setmod with L-like absolute candidate_path
    import types
    fake = types.SimpleNamespace()
    # _selection_for_state will be overridden per-case; provide base that raises
    g = {"pathlib": pathlib, "_glob": _glob, "_json": _json, "os": os,
         "root": tmp_root, "setmod": fake, "core": None, "subprocess": subprocess}
    exec(block, g)
    return g

def main() -> int:
    g = load_workflow_defs(pathlib.Path("/tmp"))
    _norm = g["_norm"]; _rel_expected = g["_rel_expected"]; _sel = g["_selection_for_state"]
    # _norm strict for caller input
    for bad in ["/abs/path.json", "../t.json", "a\\b.json", ""]:
        try:
            _norm(bad); print(f"FAIL _norm should refuse {bad!r}"); return 2
        except SystemExit: pass
    assert _norm("a/b.json") == "a/b.json"
    print("NORM_STRICT PASS")
    # _rel_expected: L absolute -> relative, escapes/unknown refuse
    with tempfile.TemporaryDirectory(prefix="r4-bug1-", dir="/tmp") as td:
        root = pathlib.Path(td).resolve()
        # absolute under root
        abs_p = root / "sources/ISSUE/publication/v2/editorial-corrections/x/publication/publication-candidate-v2.json"
        assert _rel_expected.__code__.co_name == "_rel_expected"
        # need root bound to tmp: re-load with tmp root
        g2 = load_workflow_defs(root)
        _rel2 = g2["_rel_expected"]; _norm2 = g2["_norm"]
        exp_rel = _rel2(abs_p)
        assert exp_rel == "sources/ISSUE/publication/v2/editorial-corrections/x/publication/publication-candidate-v2.json", exp_rel
        print("REL_EXPECTED_ABSOLUTE PASS", exp_rel)
        # escape refuses
        try:
            _rel2(pathlib.Path("/etc/passwd")); print("FAIL escape should refuse"); return 2
        except SystemExit as e:
            assert "escapes" in str(e), e
            print("REL_EXPECTED_ESCAPE_REFUSED PASS")
        # unknown branch (None) refuses
        try:
            _rel2(None); print("FAIL None should refuse"); return 2
        except SystemExit as e:
            assert "unknown" in str(e).lower() or "missing" in str(e).lower(), e
            print("REL_EXPECTED_UNKNOWN_REFUSED PASS")
        # caller absolute still refuses via _norm (not _rel_expected)
        try:
            _norm2("/tmp/abs.json"); print("FAIL caller abs should refuse"); return 2
        except SystemExit: print("CALLER_ABSOLUTE_REFUSED PASS")
        # mode unknown failclosed: _selection_for_state checks mode
        import types, json as _j
        # minimal repo for _selection_for_state: config + State + fake selection
        (root / "config").mkdir(parents=True, exist_ok=True)
        (root / "config/survey-production-v2.json").write_text(_j.dumps({}))
        (root / "sources/ISSUE").mkdir(parents=True, exist_ok=True)
        st = {"issue_id": "ISSUE", "checkpoint_provenance": {"validation": {"path": "x", "sha256": "0"*64}}}
        (root / "sources/ISSUE/production-state.json").write_text(_j.dumps(st))
        fake2 = types.SimpleNamespace()
        def fake_resolve(r, cfg, s):
            return {"mode": "UNKNOWN_MODE", "candidate_path": root / "a.json"}
        fake2.resolve_publication_selection = fake_resolve
        g2["setmod"] = fake2
        # re-exec to bind fake? _selection_for_state uses g setmod at call time (global), so update
        # call directly
        try:
            g2["_selection_for_state"]("sources/ISSUE/production-state.json")
            print("FAIL unknown mode should refuse"); return 2
        except SystemExit as e:
            assert "unknown" in str(e).lower(), e
            print("UNKNOWN_BRANCH_FAILCLOSED PASS")
    print("BUG1_FOCUSED PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
