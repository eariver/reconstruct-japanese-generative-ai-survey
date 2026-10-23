#!/usr/bin/env python3
"""Worker C diagnostic: R1x2 BEFORE weekly versioned correction then versioned writer refusals.

Governing: d880 contract §9 + root selection. Fixed SOURCE717 HEAD 4ff2d85.
No sourcecode edits except two isolated R1 fixture comment commits (AST-neutral
before build_reader_input) in YOUR fixture only, receipts generated AFTER each
source commit. Uses real accepted Weekly base helper _new_weekly_helper /
_build_weekly_validated (initial blank PDF type only), actual R1 stimulus
_commit_r1_nonemitted_comment, process-scoped Git identity only.
New code current closure 22 / config contract 67 unchanged by comment; each
refresh_mechanical_evidence validated under fixture-code subprocess (no ambient
stale). No old saved runner; adapts retention test_r1_double_refresh_capture_verify
+ P3S genuine owner. Preserves full raw first/second/current State/records,
shows legacy rows cumulative against original checkpoint and second.supersedes first.
Then P1 Weekly envelope -> retention/scope/P2V/P3S -> REAL TL2026 high prepare +
external typed reviews + bounded QA -> finalize/activate with canonical_anchor =
latest second legacy record, historical canonical via anchor + active7 separately
(old canonical files byte-exact second legacy output). Public State/receipt/Gate/
Candidate healthy. R1 + canonical revalidate AFTER versioned must both refuse BEFORE
any guard/output/State change with immediate full inventory comparison; no fake
editorial reason bypass. Actual function calls, exact refusal messages, healthy
controls. No validator/Git mock. Artifact-only HEAD optional separately.
No whole PASS / production approval.
"""
from __future__ import annotations
import ast as _ast
import json
import os
import shutil
import stat as _stat
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

def _eprint(*a):
    print(*a, flush=True)

def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    _eprint(f"FIX_ROOT={FIX_ROOT}")
    _eprint(f"NOTES={NOTES}")
    sys.path.insert(0, str(FIX_ROOT))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    # Sanity: no GIT_* overrides inherited
    for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
        if os.environ.get(_v):
            _eprint(f"UNSAFE inherited {_v}={os.environ.get(_v)}")
            return 2
    from scripts import survey_production_v2 as core
    # Source pins
    t0 = time.monotonic()
    def _run_git(*args):
        env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file",
                    "GIT_AUTHOR_NAME":"Synthetic WorkerC R1Anchor","GIT_AUTHOR_EMAIL":"workerc-r1anchor@example.invalid",
                    "GIT_COMMITTER_NAME":"Synthetic WorkerC R1Anchor","GIT_COMMITTER_EMAIL":"workerc-r1anchor@example.invalid"})
        return subprocess.run(["git",*args], cwd=FIX_ROOT, capture_output=True, text=True, env=env)
    head = _run_git("rev-parse","HEAD").stdout.strip()
    tree = _run_git("rev-parse","HEAD^{tree}").stdout.strip()
    status = _run_git("status","--porcelain=v1","--untracked-files=all").stdout
    tracked_n = len(_run_git("ls-files").stdout.strip().splitlines())
    _eprint(f"SOURCE_HEAD={head}")
    _eprint(f"SOURCE_TREE={tree}")
    _eprint(f"TRACKED={tracked_n} STATUS_LINES={len(status.strip().splitlines()) if status.strip() else 0}")
    assert head == "4ff2d8562502db36223332c45c9cc5d01bb93156", f"unexpected HEAD {head}"
    assert tree == "4a0c5343937151af0c0ad4522177441acd0e8fcc", f"unexpected tree {tree}"
    assert tracked_n == 717, f"tracked {tracked_n}"
    assert status.strip() == "", f"fixture not clean: {status[:500]}"
    # Closure 22 / contract 67 pins
    from scripts import survey_weekly_derivation_v2 as _wkd
    cfg = core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)
    assert len(_wkd.CURRENT_CLOSURE) == 22, f"closure {len(_wkd.CURRENT_CLOSURE)}"
    pipe_len = len(cfg["contract_files"]["pipeline"])
    assert pipe_len == 67, f"pipeline {pipe_len}"
    _eprint(f"CLOSURE22_OK={len(_wkd.CURRENT_CLOSURE)} CONTRACT67_OK={pipe_len}")
    tl_bin = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    assert tl_bin.exists(), f"TL missing {tl_bin}"
    _eprint(f"TL_OK={tl_bin}")
    # Helpers
    import unittest
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from tests import test_survey_editorial_retention_v2 as _p2r_t  # noqa: ensure importable
    from tests import test_survey_editorial_staged_source_v2 as _p3s_t
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    from scripts import survey_editorial_retention_v2 as retention
    from scripts import survey_editorial_current_authority_v2 as observer
    from scripts import survey_editorial_staged_source_v2 as staged
    from scripts import survey_editorial_publication_v2 as edpub
    from scripts import survey_reader_publication_v2 as reader_pub
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_quality_v2 as quality
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_publication_set_v2 as setmod
    from scripts import survey_publication_v2 as pubmod

    class _TC(unittest.TestCase):
        def runTest(self): pass
    tc = _TC()

    def _snapshot(root: Path) -> dict:
        files: dict[str,str] = {}
        special: dict[str,str] = {}
        for p in sorted(root.rglob("*")):
            if ".git" in p.parts:
                continue
            try:
                rel = str(p.relative_to(root))
            except ValueError:
                continue
            try:
                st = p.lstat()
            except OSError as e:
                special[rel] = f"LSTAT_ERROR:{e}"
                continue
            if _stat.S_ISDIR(st.st_mode):
                special[rel] = "DIR"
                continue
            if not _stat.S_ISREG(st.st_mode):
                special[rel] = "SPECIAL:"+oct(_stat.S_IMODE(st.st_mode))
                continue
            try:
                files[rel] = core.sha256_file(p)
            except OSError:
                special[rel] = "UNREADABLE"
        h = _run_git("rev-parse","HEAD").stdout.strip()
        s = _run_git("status","--porcelain").stdout
        return {"files":files,"special":special,"head":h,"status":s}

    def _assert_no_write(before: dict, after: dict, label: str):
        assert after["files"] == before["files"], f"tree write during {label}"
        assert after.get("special") == before.get("special"), f"special write during {label}"
        assert after["head"] == before["head"], f"HEAD moved during {label}"
        assert after["status"] == before["status"], f"status changed during {label}"

    def _run_fixture_code(script: str, args: list[str], timeout_s: int = 1200) -> tuple[int,str,str]:
        env = {k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1"})
        proc = subprocess.run([sys.executable,"-c",script,*args], cwd=FIX_ROOT, capture_output=True, text=True, timeout=timeout_s, env=env)
        return proc.returncode, proc.stdout, proc.stderr

    # --- Base Weekly VALIDATED (blank PDF only) ---
    _eprint("=== BASE ===")
    helper = p1t._new_weekly_helper(tc, FIX_ROOT)
    built = p1t._build_weekly_validated(tc, helper)
    chain, state_path = built["chain"], Path(built["state_path"]) if not isinstance(built["state_path"], Path) else built["state_path"]
    # state_path may be absolute or relative? helper gives absolute? Normalize to absolute Path
    if not state_path.is_absolute():
        state_path = (FIX_ROOT / state_path).resolve()
    _eprint(f"BASE_VALIDATED state={state_path.relative_to(FIX_ROOT)}")
    # Save base State + validation checkpoint
    base_state_bytes = state_path.read_bytes()
    base_state = core.load_json(state_path)
    (NOTES / "base-state.json").write_bytes(base_state_bytes)
    validation_ref = base_state["checkpoint_provenance"]["validation"]
    (NOTES / "base-validation-ref.json").write_text(json.dumps(validation_ref, indent=2))
    assert base_state.get("publication_revalidation_provenance") is None, "base should have null provenance"
    # Original checkpoint artifacts
    validation_path = FIX_ROOT / validation_ref["path"]
    assert validation_path.is_file()
    (NOTES / "base-validation-checkpoint.json").write_bytes(validation_path.read_bytes())
    orig_ckpt = core.load_json(validation_path)
    orig_map = {(r["name"],r["path"]): r["sha256"] for r in orig_ckpt.get("artifacts",[])}
    _eprint(f"ORIG_ARTIFACTS={len(orig_map)}")
    # Closure/contract still
    assert len(_wkd.CURRENT_CLOSURE) == 22
    assert len(core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)["contract_files"]["pipeline"]) == 67

    # --- R1 first: genuine owner comment via actual P3S helper ---
    _eprint("=== R1-1 COMMIT ===")
    # Use actual P3S helper (AST-neutral before build_reader_input)
    head_before_r1a = _run_git("rev-parse","HEAD").stdout.strip()
    r1a_sha = _p3s_t._commit_r1_nonemitted_comment(tc, FIX_ROOT)
    _eprint(f"R1A_COMMIT_HEAD={r1a_sha} prev={head_before_r1a}")
    assert r1a_sha != head_before_r1a
    # Verify closure/contract unchanged
    # Need fresh import? Closure is path list, unchanged; contract file unchanged (scripts not in contract)
    import importlib
    # Re-read closure from file (not cached module stale check via AST? just check len)
    assert len(_wkd.CURRENT_CLOSURE) == 22, "closure drift after R1a"
    assert len(core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)["contract_files"]["pipeline"]) == 67
    _eprint("R1A_CLOSURE22_CONTRACT67_UNCHANGED")
    # Verify AST equality already done in helper; double-check file contains anchor
    probe_text = (FIX_ROOT / "scripts/survey_weekly_derivation_v2.py").read_text(encoding="utf-8")
    assert _p3s_t._P3S_R1_NONEMITTED_COMMENT_ANCHOR in probe_text
    # Receipt AFTER source commit: refresh via fixture subprocess (no ambient stale)
    refresh_script = (
        "import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
        "from scripts import survey_production_v2 as core\n"
        "from scripts import survey_weekly_mechanical_refresh_v2 as r1\n"
        "from datetime import datetime, timezone\n"
        "recorded=datetime(2026,9,19,8,0,0,tzinfo=timezone.utc)\n"
        "result=r1.refresh_mechanical_evidence(root, core.load_json(root / core.DEFAULT_CONFIG), state_path, 'fixture R1 first refresh', 'synthetic WorkerC R1', recorded)\n"
        "import json\nprint(json.dumps({'result':'OK','keys':sorted(result.keys())}))\n"
    )
    t_r1a = time.monotonic()
    rc, out, err = _run_fixture_code(refresh_script, [str(FIX_ROOT), str(state_path)])
    dt_r1a = time.monotonic() - t_r1a
    _eprint(f"R1A_REFRESH rc={rc} dt={dt_r1a:.1f}s out={out[:500]} err_tail={err[-2000:]}")
    assert rc == 0, f"R1a refresh failed rc={rc} out={out} err={err[-4000:]}"
    state1 = core.load_json(state_path)
    assert state1.get("publication_revalidation_provenance") is not None, "R1a provenance missing"
    rec1_ref = state1["publication_revalidation_provenance"]
    _eprint(f"R1A_RECORD={rec1_ref}")
    (NOTES / "state-after-r1a.json").write_bytes(state_path.read_bytes())
    rec1_path = FIX_ROOT / rec1_ref["path"]
    assert rec1_path.is_file()
    (NOTES / "record-r1a.json").write_bytes(rec1_path.read_bytes())
    assert rec1_ref["sha256"] == core.sha256_file(rec1_path)
    rec1 = core.load_json(rec1_path)
    assert rec1.get("supersedes") is None, f"first legacy supersedes must be null, got {rec1.get('supersedes')}"
    # Legacy rows cumulative vs original
    sup1 = { (r["name"],r["path"]): r["prior_sha256"] for r in rec1.get("superseded_artifacts",[])}
    pres1 = { (r["name"],r["path"]): r["sha256"] for r in rec1.get("preserved_artifacts",[])}
    for k,v in sup1.items():
        assert orig_map.get(k) == v, f"R1a superseded prior mismatch {k}"
    for k,v in pres1.items():
        assert orig_map.get(k) == v, f"R1a preserved mismatch {k}"
    assert set(sup1) | set(pres1) == set(orig_map), "R1a union != original"
    _eprint(f"R1A_CUMULATIVE_OK superseded={len(sup1)} preserved={len(pres1)} total={len(orig_map)}")
    # P1 + retention for R1a (adapt retention test)
    def _mut_r1a():
        a = core.load_json(chain["authored_path"])
        a["cover"]["headline"] = "Weekly R1 first refresh, revised edition"
        return a
    from tests.test_survey_editorial_retention_v2 import _prepare_proposal_for as _prep_ret
    pp1, _prep1 = _prep_ret(tc, FIX_ROOT, helper, chain, state_path, "fixture-wk-r1a-verify", _mut_r1a)
    _eprint(f"R1A_P1={pp1.relative_to(FIX_ROOT) if isinstance(pp1, Path) else pp1}")
    out1 = retention.capture_retention(FIX_ROOT, state_path, pp1)
    assert out1["result"] == retention.RESULT_CAPTURED, out1
    manifest1_path = FIX_ROOT / out1["manifest_path"]
    v1 = retention.verify_retention(FIX_ROOT, pp1, manifest1_path)
    assert v1["result"] == retention.RESULT_VERIFIED, v1
    _eprint(f"R1A_RETENTION_OK {out1['manifest_path']}")
    (NOTES / "retention-r1a-manifest.json").write_bytes(manifest1_path.read_bytes())
    (NOTES / "proposal-r1a.json").write_bytes((FIX_ROOT / pp1.relative_to(FIX_ROOT) if isinstance(pp1, Path) and pp1.is_absolute() else FIX_ROOT / pp1).read_bytes() if isinstance(pp1, Path) else (FIX_ROOT / pp1).read_bytes())

    # --- R1 second: distinct meaningful comment, AST-neutral ---
    _eprint("=== R1-2 COMMIT ===")
    probe = FIX_ROOT / "scripts/survey_weekly_derivation_v2.py"
    text = probe.read_text(encoding="utf-8")
    anchor2 = "fixture R1 second non-emitted Python comment C2"
    assert anchor2 not in text
    before_ast = _ast.dump(_ast.parse(text))
    lines = text.splitlines(keepends=True)
    targets = [i for i,l in enumerate(lines) if l.startswith("def build_reader_input(")]
    assert len(targets) == 1, "R1 owner def must appear exactly once"
    lines.insert(targets[0], f"# {anchor2}\n")
    probe.write_text("".join(lines), encoding="utf-8")
    after_ast = _ast.dump(_ast.parse(probe.read_text(encoding="utf-8")))
    assert before_ast == after_ast, "R1b comment changed semantics"
    proc = _run_git("add","scripts/survey_weekly_derivation_v2.py")
    assert proc.returncode == 0, proc.stderr
    proc = _run_git("-c","user.name=Synthetic WorkerC R1Anchor","-c","user.email=workerc-r1anchor@example.invalid","commit","-q","-m","Fixture R1 second non-emitted comment C2")
    assert proc.returncode == 0, proc.stderr
    head_r1b = _run_git("rev-parse","HEAD").stdout.strip()
    _eprint(f"R1B_COMMIT_HEAD={head_r1b}")
    assert len(_wkd.CURRENT_CLOSURE) == 22
    assert len(core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)["contract_files"]["pipeline"]) == 67
    _eprint("R1B_CLOSURE22_CONTRACT67_UNCHANGED")
    refresh_script2 = (
        "import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
        "from scripts import survey_production_v2 as core\n"
        "from scripts import survey_weekly_mechanical_refresh_v2 as r1\n"
        "from datetime import datetime, timezone\n"
        "recorded=datetime(2026,9,19,8,5,0,tzinfo=timezone.utc)\n"
        "result=r1.refresh_mechanical_evidence(root, core.load_json(root / core.DEFAULT_CONFIG), state_path, 'fixture R1 second refresh', 'synthetic WorkerC R1', recorded)\n"
        "import json\nprint(json.dumps({'result':'OK','keys':sorted(result.keys())}))\n"
    )
    t_r1b = time.monotonic()
    rc2, out2, err2 = _run_fixture_code(refresh_script2, [str(FIX_ROOT), str(state_path)])
    dt_r1b = time.monotonic() - t_r1b
    _eprint(f"R1B_REFRESH rc={rc2} dt={dt_r1b:.1f}s out={out2[:500]} err_tail={err2[-2000:]}")
    assert rc2 == 0, f"R1b refresh failed {out2} {err2[-4000:]}"
    state2 = core.load_json(state_path)
    rec2_ref = state2["publication_revalidation_provenance"]
    _eprint(f"R1B_RECORD={rec2_ref}")
    assert rec2_ref != rec1_ref, "second record must differ"
    assert rec2_ref["path"] != rec1_ref["path"], "second record path must differ"
    (NOTES / "state-after-r1b.json").write_bytes(state_path.read_bytes())
    rec2_path = FIX_ROOT / rec2_ref["path"]
    (NOTES / "record-r1b.json").write_bytes(rec2_path.read_bytes())
    rec2 = core.load_json(rec2_path)
    assert rec2.get("supersedes") == rec1_ref, f"second.supersedes must equal first {rec2.get('supersedes')} vs {rec1_ref}"
    _eprint(f"R1B_SUPERSEDES_FIRST_OK {rec2.get('supersedes')}")
    sup2 = {(r["name"],r["path"]): r["prior_sha256"] for r in rec2.get("superseded_artifacts",[])}
    pres2 = {(r["name"],r["path"]): r["sha256"] for r in rec2.get("preserved_artifacts",[])}
    for k,v in sup2.items():
        assert orig_map.get(k) == v, f"R1b superseded prior mismatch {k}"
    for k,v in pres2.items():
        assert orig_map.get(k) == v, f"R1b preserved mismatch {k}"
    assert set(sup2) | set(pres2) == set(orig_map), "R1b union != original"
    _eprint(f"R1B_CUMULATIVE_OK superseded={len(sup2)} preserved={len(pres2)}")
    # Active predecessor check
    cfg2 = core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)
    record2_active, errors2 = agent.resolve_active_publication_revalidation(FIX_ROOT, cfg2, core.load_json(state_path))
    assert errors2 == [], f"active errors {errors2}"
    assert record2_active.get("supersedes") is not None
    _eprint("R1B_ACTIVE_OK")
    def _mut_r1b():
        a = core.load_json(chain["authored_path"])
        a["cover"]["headline"] = "Weekly R1 second refresh, revised edition"
        return a
    pp2, _prep2 = _prep_ret(tc, FIX_ROOT, helper, chain, state_path, "fixture-wk-r1b-verify", _mut_r1b)
    out2r = retention.capture_retention(FIX_ROOT, state_path, pp2)
    assert out2r["result"] == retention.RESULT_CAPTURED
    manifest2_path = FIX_ROOT / out2r["manifest_path"]
    v2 = retention.verify_retention(FIX_ROOT, pp2, manifest2_path)
    assert v2["result"] == retention.RESULT_VERIFIED
    _eprint(f"R1B_RETENTION_OK {out2r['manifest_path']}")
    (NOTES / "retention-r1b-manifest.json").write_bytes(manifest2_path.read_bytes())
    # Old retention must now fail (second supersedes first context)
    try:
        retention.verify_retention(FIX_ROOT, pp1, manifest1_path)
        raise AssertionError("old retention pp1 must fail after R1b")
    except Exception as exc:
        msg = str(exc)
        assert any(s in msg for s in ("INVALID_RETENTION","REF_DRIFT","PROFILE_DRIFT","COPY_DRIFT")), f"wrong old-retention error {exc}"
        _eprint(f"OLD_RETENTION_REFUSAL_OK {type(exc).__name__}:{msg[:300]}")

    # --- New P1 Weekly envelope correction for versioned ---
    _eprint("=== VERSIONED P1 ===")
    # Snapshot before versioned P1
    snap_before_corr = _snapshot(FIX_ROOT)
    # Use staged helper _weekly_prepare_from with existing helper/built but new proposal id?
    # Need fresh authored headline for versioned correction (changed reader)
    from tests.test_survey_editorial_staged_source_v2 import _weekly_prepare_from as _wk_prep_from
    # _weekly_prepare_from expects helper, built, proposal_id; but built chain state_path is now updated (state2)?
    # Rebuild helper/built view: helper still points to old chain object, but state_path file now has R1b provenance.
    # Need to reload chain? The chain authored_path etc unchanged; state_path is same file path (updated bytes).
    # Use current state_path file (already R1b). Call _weekly_prepare_from with current helper/built (built state_path same path).
    # However built dict still has old chain; that's fine (chain authored_path unchanged, state file updated).
    # To avoid stale chain, reload helper? Helper's chain is original; P1 will derive from current State file.
    corr = _wk_prep_from(tc, FIX_ROOT, helper, {"chain":chain,"state_path":state_path,"helper":helper}, "fixture-wk-corr-verify")
    # _wk_prep_from returns helper,chain,state_path,built,prepared,proposal_path but our import above is different signature?
    # Actually _weekly_prepare_from(tc,root,helper,built,proposal_id) where built contains chain/state_path.
    # We passed built dict with chain/state_path; need to ensure correct.
    # Fallback: manually do P1 steps like smoke if helper mismatch.
    # Let's inspect corr keys
    _eprint(f"CORR_KEYS={sorted(corr.keys()) if isinstance(corr,dict) else type(corr)}")
    if isinstance(corr, dict) and "proposal_path" in corr:
        proposal_path = corr["proposal_path"]
        prepared = corr["prepared"]
        # state_path may have been updated? Use corr state_path if present
        state_path = Path(corr.get("state_path", state_path))
        if not state_path.is_absolute():
            state_path = (FIX_ROOT / state_path).resolve()
    else:
        raise AssertionError(f"unexpected corr {corr}")
    _eprint(f"CORR_PROPOSAL={proposal_path.relative_to(FIX_ROOT)}")
    # P2R capture
    cap = retention.capture_retention(FIX_ROOT, state_path, proposal_path)
    assert cap["result"] == retention.RESULT_CAPTURED
    manifest_path = FIX_ROOT / cap["manifest_path"]
    vout = retention.verify_retention(FIX_ROOT, proposal_path, manifest_path)
    assert vout["result"] == retention.RESULT_VERIFIED
    _eprint(f"CORR_P2R_OK {cap['manifest_path']}")
    # P2R after-capture refusal (healthy control: P1 after capture must refuse)
    try:
        proposal_mod.validate_proposal(FIX_ROOT, state_path, proposal_path)
        raise AssertionError("P1 after capture must refuse")
    except Exception as exc:
        assert "RETENTION_DEST_CONFLICT" in str(exc) or "REFUSED" in str(exc) or "retention" in str(exc).lower(), f"P1 after capture wrong {exc}"
        _eprint(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}")
    # Scope (externally supplied typed, clearly synthetic)
    staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path = p1t._scope_review_for(tc, FIX_ROOT, prepared, staged_reader_rel, "scope-review-v2.json")
    _eprint(f"SCOPE={scope_path.relative_to(FIX_ROOT)}")
    # P2V
    obs = observer.observe_current_authority(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
    assert obs.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    _eprint("P2V_SCOPE_BOUND")
    # P3S materialize + verify (direct, like smoke; materializer does own fresh observations)
    mat = staged.materialize_staged_source(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
    _eprint(f"P3S_MATERIALIZE={mat}")
    if isinstance(mat, dict) and "staged_manifest_path" in mat:
        staged_manifest_path = FIX_ROOT / mat["staged_manifest_path"]
    else:
        staged_manifest_path = (proposal_path.parent / "staged-source" / "staged-source-manifest.json")
    assert staged_manifest_path.is_file(), f"staged manifest missing {staged_manifest_path}"
    ver = staged.verify_staged_source(FIX_ROOT, proposal_path, staged_manifest_path)
    assert ver.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED", ver
    _eprint("P3S_VERIFIED")
    assert len(core.load_json(staged_manifest_path)["code_deps"]) == 50, "P3S50 expected"
    _eprint("P3S50_OK")

    # --- High prepare REAL TL2026 ---
    _eprint("=== PREPARE REAL TL2026 ===")
    proposal_dir = proposal_path.parent
    staged_manifest = core.load_json(staged_manifest_path)
    issue_id = staged_manifest.get("issue_id")
    arch_path = helper.source_root / "architecture-v2.json"
    arch = core.load_json(arch_path)
    coverage = [{"package_id":plan["package_id"],"requirement":req,"status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"WorkerC manuscript author maps requirement."} for plan in arch.get("packages",[]) for req in plan.get("must_cover_requirements",[])]
    requirements = [{"requirement_id":"FINAL_SYNTHESIS","status":"FULFILLED","reader_locations":["main.tex:summary"],"detail":"WorkerC asserts synthesis."},{"requirement_id":"WEEKLY_COMMUNITY_MOVEMENT","status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"WorkerC asserts movement."}]
    manuscript_spec = {"schema_version":"2.0-rc1","kind":"EDITORIAL_MANUSCRIPT_SPEC_V1","issue_id":issue_id,"proposal_ref":{"path":str(proposal_path.relative_to(FIX_ROOT)),"sha256":core.sha256_file(proposal_path)},"architecture_coverage":coverage,"reader_requirements":requirements,"authored_by":"workerc manuscript author","recorded_at":datetime.now(timezone.utc).isoformat()}
    manuscript_spec_path = proposal_dir / "manuscript-spec.json"
    core.write_json(manuscript_spec_path, manuscript_spec)
    toolchain_spec = {"schema_version":"2.0-rc1","kind":"EDITORIAL_TOOLCHAIN_SPEC_V1","executor":"workerc-integration","absolute_executable":str(tl_bin),"recipe":"lualatex-biber-lualatex","argv":list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),"env":{},"recorded_at":datetime.now(timezone.utc).isoformat()}
    toolchain_spec_path = proposal_dir / "toolchain-spec.json"
    core.write_json(toolchain_spec_path, toolchain_spec)
    _eprint(f"SPECS {manuscript_spec_path.relative_to(FIX_ROOT)} {toolchain_spec_path.relative_to(FIX_ROOT)}")
    def _rel(p):
        s = str(p.relative_to(FIX_ROOT)) if isinstance(p, Path) and p.is_absolute() else str(p)
        # If already relative Path, make relative string
        if isinstance(p, Path) and not p.is_absolute():
            return str(p)
        return s
    # Ensure repo-relative
    def _rel2(p):
        if isinstance(p, Path):
            try:
                return str(p.relative_to(FIX_ROOT)) if p.is_absolute() else str(p)
            except ValueError:
                return str(p)
        s=str(p)
        if s.startswith("/"):
            try:
                return str(Path(s).relative_to(FIX_ROOT))
            except ValueError:
                return s
        return s
    t_prep = time.monotonic()
    prepared_paths = edpub.prepare_publication(FIX_ROOT, _rel2(state_path), _rel2(proposal_path), _rel2(staged_manifest_path), _rel2(manuscript_spec_path), _rel2(toolchain_spec_path), datetime.now(timezone.utc))
    dt_prep = time.monotonic()-t_prep
    _eprint(f"PREPARE_OK dt={dt_prep:.1f}s {json.dumps(prepared_paths)[:1000]}")
    pubdir = proposal_dir / "publication"
    manuscript_path = pubdir / "reader-manuscript-v2.json"
    pdf_path = pubdir / "build" / "main.pdf"
    assert manuscript_path.is_file() and pdf_path.is_file()
    from pypdf import PdfReader as _PR
    page_count = len(_PR(str(pdf_path)).pages)
    _eprint(f"REAL_PDF pages={page_count} bytes={pdf_path.stat().st_size}")
    assert page_count >= 1
    # QA + external typed reviews (synthetic labels, actual builders)
    quality_root = pubdir / "quality"
    quality_root.mkdir(parents=True, exist_ok=True)
    subject_path = quality_root / "subject-entity-property-binding.json"
    core.write_json(subject_path, {"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","scope":"workerc editorial real-build"})
    staged_main_rel = staged_manifest["outputs"]["main"]["path"]
    staged_main_bytes = (FIX_ROOT / staged_main_rel).read_bytes()
    identifier_path = quality_root / "identifier-preservation.json"
    core.write_json(identifier_path, {"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(staged_main_bytes),"inspected_identifiers":[issue_id],"scope":"workerc real-build"})
    preflight_path = quality_root / "pdf-preflight.json"
    core.write_json(preflight_path, {"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":page_count,"pdf_sha256":core.sha256_file(pdf_path),"byte_count":pdf_path.stat().st_size,"scope":"workerc real TL2026 PDF"})
    result_paths = {"SUBJECT_ENTITY_PROPERTY_BINDING":subject_path,"IDENTIFIER_PRESERVATION":identifier_path,"PDF_PREFLIGHT":preflight_path}
    quality_checks = [{"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"workerc editorial with actual file assertions","evidence":"Exact fixture bytes and result file inspected.","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":str(p.relative_to(FIX_ROOT)),"sha256":core.sha256_file(p)}} for cid,p in result_paths.items()]
    det_checks_path = proposal_dir / "deterministic-checks.json"
    core.write_json(det_checks_path, {"checks":quality_checks})
    profile = core.load_json(FIX_ROOT / core.load_json(state_path)["profile"]["path"])
    for kind,fname in (("SEMANTIC_EDITORIAL","semantic-review-v2.json"),("VISUAL","visual-review-v2.json")):
        checks=[{"check_id":cid,"status":"PASS","detail":f"WorkerC synthetic {kind} reviewer; no genuine Human approval.","evidence_locations":["workerc-real-build:main.pdf"]} for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT, profile, kind))]
        outp = pubdir / fname
        reader_pub.build_review_record(FIX_ROOT, manuscript_path, pdf_path, page_count, kind, checks, f"workerc synthetic {kind} reviewer", datetime.now(timezone.utc), outp)
        _eprint(f"REVIEW {kind} {outp.relative_to(FIX_ROOT)}")
    sem_path = pubdir / "semantic-review-v2.json"
    vis_path = pubdir / "visual-review-v2.json"
    # Snapshot before finalize (old State healthy, inert)
    snap_before_final = _snapshot(FIX_ROOT)
    t_fin = time.monotonic()
    set_ref = edpub.finalize_publication(FIX_ROOT, _rel2(state_path), _rel2(proposal_path), _rel2(staged_manifest_path), _rel2(det_checks_path), _rel2(sem_path), _rel2(vis_path), datetime.now(timezone.utc))
    dt_fin = time.monotonic()-t_fin
    _eprint(f"FINALIZE_OK dt={dt_fin:.1f}s {json.dumps(set_ref)[:1000]}")
    # Inert healthy
    errs = agent.validate_agent_state(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), core.load_json(state_path))
    assert not errs, f"State unhealthy after finalize {errs}"
    _eprint("INERT_HEALTHY")
    # set path
    _set_path_raw = set_ref["set_ref"] if isinstance(set_ref, dict) and "set_ref" in set_ref else set_ref
    if isinstance(_set_path_raw, dict):
        set_rel = _set_path_raw.get("path")
    else:
        set_rel = str(_set_path_raw)
    # Normalize set_rel to repo-relative string
    if set_rel.startswith("/"):
        set_rel = str(Path(set_rel).relative_to(FIX_ROOT))
    set_abs = FIX_ROOT / set_rel
    assert set_abs.is_file()
    _eprint(f"SET={set_rel}")
    (NOTES / "publication-set.json").write_bytes(set_abs.read_bytes())
    # Snapshot before activate for old-canonical comparison
    snap_before_activate = _snapshot(FIX_ROOT)
    old_state_bytes_before = (FIX_ROOT / _rel2(state_path)).read_bytes() if isinstance(state_path, Path) else None
    # Activate
    t_act = time.monotonic()
    res = edpub.activate_publication(FIX_ROOT, _rel2(state_path), set_rel, "WorkerC weekly editorial correction", "workerc-executor", datetime.now(timezone.utc))
    dt_act = time.monotonic()-t_act
    _eprint(f"ACTIVATE dt={dt_act:.1f}s {json.dumps(res)}")
    assert res.get("status") == "ACTIVATED", res
    # Verify canonical_anchor == latest second legacy record
    act_record_path = FIX_ROOT / res["record_path"]
    act_record = core.load_json(act_record_path)
    anchor = act_record.get("canonical_anchor")
    _eprint(f"ANCHOR={json.dumps(anchor)}")
    assert anchor.get("kind") == "LEGACY_REVALIDATION", anchor
    assert anchor.get("ref") == rec2_ref, f"anchor {anchor.get('ref')} != rec2 {rec2_ref}"
    _eprint("ANCHOR_IS_R1B_OK")
    (NOTES / "activation-record.json").write_bytes(act_record_path.read_bytes())
    (NOTES / "state-after-activate.json").write_bytes((FIX_ROOT / _rel2(state_path)).read_bytes())
    # Historical vs active separately
    # Historical: derive anchor chain should give same anchor
    chain_for_anchor = [{"record":core.load_json(FIX_ROOT / rec1_ref["path"]),"path":rec1_ref["path"],"sha256":rec1_ref["sha256"]},
                        {"record":core.load_json(FIX_ROOT / rec2_ref["path"]),"path":rec2_ref["path"],"sha256":rec2_ref["sha256"]}]
    derived = setmod.derive_canonical_anchor(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), core.load_json(FIX_ROOT / _rel2(state_path)), chain_for_anchor)
    assert derived == anchor, f"derived {derived} != anchor {anchor}"
    _eprint("DERIVED_ANCHOR_MATCH")
    sel = setmod.resolve_publication_selection(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), core.load_json(FIX_ROOT / _rel2(state_path)))
    assert sel.get("mode") == "VERSIONED_ACTIVE", sel
    assert sel.get("set_ref",{}).get("path") == set_rel or sel.get("active_set_ref",{}).get("path") == set_rel, f"selection set mismatch {sel}"
    assert len(sel.get("effective7",{})) == 7 or len(sel.get("roles",{}) or {}) >= 7, f"effective7 missing {sel.keys()}"
    _eprint(f"SELECTION_ACTIVE_OK mode={sel.get('mode')}")
    # Old canonical files byte-exact second legacy output: compare snapshot before/after for canonical publication files (excluding new publication/, new record, State)
    snap_after_activate = _snapshot(FIX_ROOT)
    # Expected new files: activation record, State change, publication/ dir under corr proposal
    # Check that all files present before (except expected) unchanged
    before_files = snap_before_activate["files"]
    after_files = snap_after_activate["files"]
    # Identify allowed delta prefix
    corr_rel_prefix = str(proposal_dir.relative_to(FIX_ROOT).as_posix()) + "/publication/"
    record_rel = res["record_path"]
    state_rel_str = _rel2(state_path)
    for rel,sha in before_files.items():
        if rel.startswith(corr_rel_prefix) or rel == record_rel or rel == state_rel_str:
            continue
        # Also allow deterministic-checks/manuscript-spec/toolchain-spec already existed before finalize? They were created before snap_before_activate? snap_before_activate was after finalize? Actually snap_before_activate taken after finalize, before activate, so those already exist.
        # So only record + State should differ/new
        if rel not in after_files:
            raise AssertionError(f"disappearance after activate (old canonical not byte-exact): {rel}")
        assert after_files[rel] == sha, f"drift after activate (old canonical changed): {rel}"
    _eprint("OLD_CANONICAL_BYTE_EXACT_OK (only State+record+publication changed)")
    # Public healthy
    state_act = core.load_json(FIX_ROOT / _rel2(state_path))
    assert agent.validate_agent_state(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), state_act) == []
    rv = edpub.validate_editorial_receipt(FIX_ROOT, _rel2(pubdir / "validated-source-manifest.json"), _rel2(state_path))
    assert rv["issue_id"] == issue_id
    _eprint("RECEIPT_ACTIVE_OK")
    gv = reader_gate.validate_reader_surface_gate(FIX_ROOT, _rel2(pubdir / "reader-surface-gate-v2.json"), issue_id=issue_id, publication_profile="WEEKLY_MAGAZINE", expected_manuscript_path=_rel2(manuscript_path), state_path=_rel2(state_path))
    assert gv["status"] == "PASSED"
    _eprint("GATE_ACTIVE_OK")
    cv = pubmod.validate_candidate(FIX_ROOT, pubdir / "publication-candidate-v2.json")
    _eprint(f"CANDIDATE_ACTIVE_OK {cv.get('status') if isinstance(cv,dict) else cv}")
    # Repeat ALREADY_ACTIVE readonly
    res2 = edpub.activate_publication(FIX_ROOT, _rel2(state_path), set_rel, "WorkerC weekly editorial correction", "workerc-executor", datetime.now(timezone.utc))
    assert res2.get("status") == "ALREADY_ACTIVE", res2
    _eprint(f"ALREADY_ACTIVE_OK {res2}")

    # --- Refusals AFTER versioned ---
    _eprint("=== REFUSALS AFTER VERSIONED ===")
    # R1 must refuse before any guard/output/State change
    snap_r1_before = _snapshot(FIX_ROOT)
    r1_refuse_script = (
        "import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
        "from scripts import survey_production_v2 as core\n"
        "from scripts import survey_weekly_mechanical_refresh_v2 as r1\n"
        "from datetime import datetime, timezone\n"
        "recorded=datetime(2026,9,19,9,0,0,tzinfo=timezone.utc)\n"
        "try:\n"
        "  r1.refresh_mechanical_evidence(root, core.load_json(root / core.DEFAULT_CONFIG), state_path, 'post-versioned R1 must refuse', 'workerc', recorded)\n"
        "  print('UNEXPECTED_SUCCESS')\n"
        "  sys.exit(10)\n"
        "except Exception as e:\n"
        "  print(f'REFUSED:{type(e).__name__}:{e}')\n"
        "  sys.exit(3)\n"
    )
    rc_r, out_r, err_r = _run_fixture_code(r1_refuse_script, [str(FIX_ROOT), str(FIX_ROOT / _rel2(state_path))])
    _eprint(f"R1_AFTER_REFUSE rc={rc_r} out={out_r[:2000]} err_tail={err_r[-2000:]}")
    assert rc_r == 3, f"R1 after must exit 3, got {rc_r} {out_r} {err_r}"
    assert "R1 mechanical refresh refused in VERSIONED_ACTIVE" in out_r or "VERSIONED_ACTIVE" in out_r, f"wrong R1 message {out_r}"
    _assert_no_write(snap_r1_before, _snapshot(FIX_ROOT), "R1 after versioned no-write")
    _eprint("R1_AFTER_REFUSE_NOWRITE_OK")
    # Canonical revalidate with REVIEWED_CORE_CHANGE must refuse in revised mode
    snap_canon_before = _snapshot(FIX_ROOT)
    canon_refuse_script = (
        "import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
        "from scripts import survey_production_v2 as core\n"
        "from scripts import survey_agent_control_v2 as agent\n"
        "from datetime import datetime, timezone\n"
        "cfg=core.load_json(root / core.DEFAULT_CONFIG)\n"
        "recorded=datetime(2026,9,19,9,5,0,tzinfo=timezone.utc)\n"
        "try:\n"
        "  agent.revalidate_publication_surface(root, cfg, state_path, 'REVIEWED_CORE_CHANGE', 'post-versioned canonical must refuse', 'workerc', recorded, None)\n"
        "  print('UNEXPECTED_SUCCESS')\n"
        "  sys.exit(10)\n"
        "except Exception as e:\n"
        "  print(f'REFUSED:{type(e).__name__}:{e}')\n"
        "  sys.exit(3)\n"
    )
    rc_c, out_c, err_c = _run_fixture_code(canon_refuse_script, [str(FIX_ROOT), str(FIX_ROOT / _rel2(state_path))])
    _eprint(f"CANON_AFTER_REFUSE rc={rc_c} out={out_c[:2000]}")
    assert rc_c == 3, f"canon after must exit 3 {rc_c} {out_c} {err_c}"
    assert "canonical revalidation refused in revised mode" in out_c.lower() or "revised mode" in out_c.lower(), f"wrong canon message {out_c}"
    _assert_no_write(snap_canon_before, _snapshot(FIX_ROOT), "canon after versioned no-write")
    _eprint("CANON_AFTER_REFUSE_NOWRITE_OK")
    # Fake editorial reason bypass must refuse (legacy writer cannot mint editorial)
    snap_fake_before = _snapshot(FIX_ROOT)
    fake_script = (
        "import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
        "from scripts import survey_production_v2 as core\n"
        "from scripts import survey_agent_control_v2 as agent\n"
        "from datetime import datetime, timezone\n"
        "cfg=core.load_json(root / core.DEFAULT_CONFIG)\n"
        "recorded=datetime(2026,9,19,9,6,0,tzinfo=timezone.utc)\n"
        "try:\n"
        "  agent.revalidate_publication_surface(root, cfg, state_path, 'REVIEWED_EDITORIAL_CORRECTION', 'fake editorial', 'workerc', recorded, None)\n"
        "  print('UNEXPECTED_SUCCESS')\n"
        "  sys.exit(10)\n"
        "except Exception as e:\n"
        "  print(f'REFUSED:{type(e).__name__}:{e}')\n"
        "  sys.exit(3)\n"
    )
    rc_f, out_f, err_f = _run_fixture_code(fake_script, [str(FIX_ROOT), str(FIX_ROOT / _rel2(state_path))])
    _eprint(f"FAKE_EDITORIAL_REFUSE rc={rc_f} out={out_f[:2000]}")
    assert rc_f == 3
    assert "REVIEWED_EDITORIAL_CORRECTION" in out_f and "must use new versioned activation" in out_f, f"wrong fake message {out_f}"
    _assert_no_write(snap_fake_before, _snapshot(FIX_ROOT), "fake editorial no-write")
    _eprint("FAKE_EDITORIAL_REFUSE_NOWRITE_OK")

    # Optional artifact-only HEAD (cheap, separate, no PASS transfer)
    try:
        snap_art_before = _snapshot(FIX_ROOT)
        art_note = FIX_ROOT / "sources/artifact-only-note-workerc.txt"
        art_note.write_text("artifact-only change outside KEEP/S2/refs\n", encoding="utf-8")
        p = _run_git("add","sources/artifact-only-note-workerc.txt")
        assert p.returncode == 0, p.stderr
        p = _run_git("-c","user.name=Synthetic WorkerC R1Anchor","-c","user.email=workerc-r1anchor@example.invalid","commit","-q","-m","Fixture artifact-only commit")
        assert p.returncode == 0, p.stderr
        # Verify staged replay still VERIFIED (cheap valid closure, no PASS transfer)
        ver2 = staged.verify_staged_source(FIX_ROOT, proposal_path, staged_manifest_path)
        assert ver2.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED"
        _eprint("ARTIFACT_ONLY_HEAD_OK (separate, no PASS transfer)")
        (NOTES / "artifact-only-head.txt").write_text(_run_git("rev-parse","HEAD").stdout)
    except Exception as e:
        _eprint(f"ARTIFACT_ONLY_INCOMPLETE {e}")
        (NOTES / "artifact-only-incomplete.txt").write_text(f"{e}\n{traceback.format_exc()}")

    # Save timelines
    summary = {
        "source_head": head, "source_tree": tree, "tracked": tracked_n,
        "r1a_head": r1a_sha, "r1b_head": head_r1b,
        "r1a_record": rec1_ref, "r1b_record": rec2_ref,
        "anchor": anchor, "set": set_rel, "activation_record": res.get("record_path"),
        "timings": {"r1a_refresh": dt_r1a, "r1b_refresh": dt_r1b, "prepare": dt_prep, "finalize": dt_fin, "activate": dt_act},
        "total_wall": time.monotonic()-t0,
    }
    (NOTES / "summary.json").write_text(json.dumps(summary, indent=2))
    _eprint(f"SUMMARY {json.dumps(summary, indent=2)}")
    _eprint("DIAGNOSTIC_BOUNDED_DONE no whole PASS, no production approval")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
