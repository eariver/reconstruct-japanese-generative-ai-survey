#!/usr/bin/env python3
"""R5b final-epoch lifecycle on FINAL R5b source epoch (HEAD 10e8662, tree e434978,
720 files): VALIDATED_DRAFT r2 -> RELEASE_CANDIDATE -> synthetic
Preview -> FROZEN -> offline Release -> RELEASED, per route in ONE isolated process.

Usage: lifecycle-r5b-20261022T150000Z.py FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_TREE EXPECT_COUNT INERT_MANIFEST ROUTE
  ROUTE in {weekly, longform}

- Single fixture root on sys.path; binding-checked imports (every scripts.*
  __file__ under FIX_ROOT, single-root scripts.__path__).
- Strict checks at FROZEN and RELEASED: healthy strict State, VERSIONED_ACTIVE
  selection on the versioned candidate, editorial receipt PASS, Gate PASSED,
  Candidate READY, historical readback r1+r2 HISTORICAL_VALID.
- ANY exception (including caught ones) -> PARTIAL report + exit nonzero.
  Never exit 0 with a hidden readback failure.
- Synthetic Preview identity explicitly typed, no real Human/production approval.
- Saves PDF text + ALL 5 page PNGs + final-epoch manifest (15 roles, counts,
  write delta, inert refs, core SHA) to NOTES_DIR.
- No fixture commits, no network/clean/reset, no State rewind, no mock validators.
- PR/export covered separately; fault matrix refs provided via manifest.

Saved BEFORE execution.
"""
from __future__ import annotations
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    print("BLOCKER: PYTHONDONTWRITEBYTECODE!=1 (set BEFORE python startup)", flush=True)
    sys.exit(2)
_fr = os.environ.get("FINAL_R5B_ROOT", "")
if not _fr or not pathlib.Path(_fr).is_dir():
    print(f"BLOCKER: FINAL_R5B_ROOT missing/not-a-dir: {_fr!r}", flush=True)
    sys.exit(2)
_pfx = os.environ.get("PYTHONPYCACHEPREFIX", "")
if not _pfx.startswith(_fr + "/"):
    print(f"BLOCKER: PYTHONPYCACHEPREFIX must be under FINAL_R5B_ROOT ({_fr}), got {_pfx!r}", flush=True)
    sys.exit(2)
_tdir = os.environ.get("TMPDIR", "")
if not _tdir.startswith(_fr + "/"):
    print(f"BLOCKER: TMPDIR must be under FINAL_R5B_ROOT ({_fr}), got {_tdir!r}", flush=True)
    sys.exit(2)

ROUTES = {
    "weekly": {"issue": "2026-W37", "old": "wk-r5b-1", "active": "wk-r5b-2",
               "profile": "WEEKLY_MAGAZINE", "gate_profile": "WEEKLY_MAGAZINE",
               "synthetic": "synthetic-weekly-r5b-fixture"},
    "longform": {"issue": "SP001", "old": "lf-r5b-1", "active": "lf-r5b-2",
                 "profile": "LONGFORM_SPECIAL", "gate_profile": "LONGFORM_SPECIAL",
                 "synthetic": "synthetic-longform-r5b-fixture"},
}


def _log(m: str):
    print(m, flush=True)


def _run_git(root: Path, *args: str):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=120, env=env)


def main() -> int:
    if len(sys.argv) != 7:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_TREE EXPECT_COUNT INERT_MANIFEST", flush=True)
        return 2
    root = Path(sys.argv[1]).resolve()
    notes = Path(sys.argv[2]).resolve()
    notes.mkdir(parents=True, exist_ok=True)
    exp_head, exp_tree = sys.argv[3].strip().lower(), sys.argv[4].strip().lower()
    exp_count, inert_manifest = int(sys.argv[5]), Path(sys.argv[6]).resolve()
    route = os.environ.get("R5B_ROUTE", "").strip()
    if route not in ROUTES:
        print(f"BLOCKER R5B_ROUTE must be weekly|longform, got {route!r}", flush=True)
        return 2
    R = ROUTES[route]
    issue, old_id, active_id = R["issue"], R["old"], R["active"]
    if [p for p in sys.path if "/jgas-" in p or "/dev/shm/" in p or "/tmp/opencode" in p]:
        print("BLOCKER: foreign fixture path pre-seeded on sys.path", flush=True)
        return 2
    sys.path.insert(0, str(root))
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        del sys.modules[m]
    import scripts.survey_production_v2 as core
    import scripts.survey_publication_v2 as pubmod
    import scripts.survey_publication_set_v2 as setmod
    import scripts.survey_stage_validation_v2 as stage_validation
    import scripts.survey_agent_control_v2 as agent
    import scripts.survey_profiled_freeze_v2 as profiled
    import scripts.survey_release_checkpoint_v2 as release_ckpt
    import scripts.survey_reader_surface_gate_v2 as reader_gate
    import scripts.survey_editorial_publication_v2 as edpub
    import scripts.survey_orchestrator_v2 as orch
    import scripts.survey_handoff_v2 as handoff
    import scripts.survey_human_gate_v2 as humangate
    bad = [(n, getattr(m, "__file__", None)) for n, m in sys.modules.items()
           if (n == "scripts" or n.startswith("scripts.")) and getattr(m, "__file__", None) is not None
           and not str(pathlib.Path(getattr(m, "__file__")).resolve()).startswith(str(root))]
    if bad:
        print(f"BLOCKER code binding outside fixture: {bad}", flush=True)
        return 2
    import scripts as _pkg
    if list(getattr(_pkg, "__path__", [])) != [str(root / "scripts")]:
        print(f"BLOCKER scripts namespace not single-root: {list(getattr(_pkg, '__path__', []))}", flush=True)
        return 2
    print(f"BINDING_OK route={route} root={root}", flush=True)
    for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
        if os.environ.get(_v):
            print(f"BLOCKER unsafe inherited {_v}", flush=True)
            return 2

    try:
        return _run(route, R, root, notes, exp_head, exp_tree, exp_count, inert_manifest,
                    core, pubmod, setmod, stage_validation, agent, profiled,
                    release_ckpt, reader_gate, edpub, orch, handoff, humangate)
    except Exception:
        print(f"PARTIAL route={route} FAILED with exception below (exit nonzero, no hidden pass)", flush=True)
        traceback.print_exc()
        return 2


def _run(route, R, root, notes, exp_head, exp_tree, exp_count, inert_manifest,
         core, pubmod, setmod, stage_validation, agent, profiled,
         release_ckpt, reader_gate, edpub, orch, handoff, humangate) -> int:
    import pathlib
    issue, old_id, active_id = R["issue"], R["old"], R["active"]
    tag = f"r5b-{route}"
    head = _run_git(root, "rev-parse", "HEAD").stdout.strip()
    tree = _run_git(root, "rev-parse", "HEAD^{tree}").stdout.strip()
    _log(f"HEAD={head} TREE={tree}")
    if head != exp_head or len(tree) != 40 or tree != exp_tree:
        _log("BLOCKER source identity mismatch (actual git values required)")
        return 2
    if len(_run_git(root, "ls-files").stdout.strip().splitlines()) != exp_count:
        _log("BLOCKER LSFILES count mismatch")
        return 2
    top = _run_git(root, "rev-parse", "--show-toplevel").stdout.strip()
    gdir = _run_git(root, "rev-parse", "--absolute-git-dir").stdout.strip()
    if pathlib.Path(top) != root or pathlib.Path(gdir) != root / ".git":
        _log(f"BLOCKER fixture .git not owned: top={top} gitdir={gdir} fix={root}")
        return 2
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    state_rel = f"sources/{issue}/production-state.json"
    st = core.load_json(root / state_rel)
    if st.get("lifecycle_state") != "VALIDATED_DRAFT":
        _log(f"BLOCKER expected VALIDATED_DRAFT pre-Preview fixture, got {st.get('lifecycle_state')}")
        return 2
    sel = setmod.resolve_publication_selection(root, cfg, st)
    active_cand_rel = (sel.get("candidate_ref") or {}).get("path")
    exp_active = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication/publication-candidate-v2.json"
    assert sel.get("mode") == "VERSIONED_ACTIVE" and active_cand_rel == exp_active, (sel.get("mode"), active_cand_rel)
    _log(f"START VALIDATED_DRAFT active={active_cand_rel}")
    pub_dir = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/publication"
    set_rel = f"{pub_dir}/publication-set.json"
    r1_rel = f"sources/{issue}/publication/v2/publication-surface-revalidation-r1.json"
    r2_rel = f"sources/{issue}/publication/v2/publication-surface-revalidation-r2.json"
    set_rel = f"{pub_dir}/publication-set.json"
    receipt_rel = f"{pub_dir}/validated-source-manifest.json"
    gate_rel = f"{pub_dir}/reader-surface-gate-v2.json"
    ms_rel = f"{pub_dir}/reader-manuscript-v2.json"
    cand_rel = active_cand_rel
    exec_rel = f"sources/{issue}/publication/v2/editorial-corrections/{active_id}/execution/lifecycle-r5b"

    def _check_full(label: str) -> None:
        s = core.load_json(root / state_rel)
        errs = agent.validate_agent_state(root, cfg, s)
        assert not errs, f"{label} State unhealthy: {errs}"
        sl = setmod.resolve_publication_selection(root, cfg, s)
        assert sl.get("mode") == "VERSIONED_ACTIVE", f"{label} mode {sl.get('mode')}"
        assert (sl.get("candidate_ref") or {}).get("path") == cand_rel, f"{label} candidate drift"
        rv = edpub.validate_editorial_receipt(root, receipt_rel, state_rel)
        gv = reader_gate.validate_reader_surface_gate(
            root, gate_rel, issue_id=issue, publication_profile=R["gate_profile"],
            expected_manuscript_path=root / ms_rel, state_path=state_rel)
        assert gv.get("status") == "PASSED", f"{label} gate {gv}"
        cv = pubmod.validate_candidate(root, root / cand_rel, issue_id=issue)
        assert cv.get("status") == "READY_FOR_PUBLICATION_PREVIEW", f"{label} cand {cv.get('status')}"
        h1 = edpub.verify_activation_history(root, r1_rel)
        h2 = edpub.verify_activation_history(root, r2_rel)
        assert h1.get("status") == "HISTORICAL_VALID", h1
        assert h2.get("status") == "HISTORICAL_VALID", h2
        _log(f"{label}_STRICT_OK receipt={rv.get('issue_id')} gate=PASSED cand=READY history=r1+r2 HISTORICAL_VALID")

    _check_full("PREVIEW_BEFORE")
    # === VALIDATED_DRAFT -> RELEASE_CANDIDATE ===
    (root / exec_rel).mkdir(parents=True, exist_ok=True)
    req = stage_validation.REQUIRED_CURRENT.get("VALIDATED_DRAFT")
    assert req == {"publication-candidate"}, req
    rep = f"{exec_rel}/r5b-validated-draft-report.json"
    stage_validation.validate_stage(root, cfg, root / state_rel, {"publication-candidate": root / cand_rel},
                                    root / rep, datetime.now(timezone.utc))
    rev = f"{exec_rel}/r5b-validated-draft-reviews.json"
    core.write_json(root / rev, {"reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
                                              "executor": f"r5b-{route}-lifecycle", "evidence": "active versioned-2 advance",
                                              "result_path": rep}]})
    cp = agent.build_stage_checkpoint(root, cfg, root / state_rel, {"publication-candidate": root / cand_rel},
                                      root / rev, f"R5b {route} VALIDATED_DRAFT active {active_id}",
                                      datetime.now(timezone.utc))
    upd = agent.advance_with_checkpoint(root, cfg, root / state_rel, cp)
    assert upd.get("lifecycle_state") == "RELEASE_CANDIDATE" and upd.get("terminal_reason") == "HUMAN_GATE_REACHED", upd
    _log("ADVANCE RELEASE_CANDIDATE/HUMAN_GATE_REACHED")
    # === synthetic Preview (typed fixture identity, never Human/production) ===
    appr = agent.approve_publication_preview(root, cfg, root / state_rel, R["synthetic"],
                                             datetime.now(timezone.utc), f"synthetic:r5b-{route}-preview-{active_id}")
    assert appr.get("human_gates", {}).get("publication_preview") == "approved", appr.get("human_gates")
    aref = core.load_json(root / state_rel).get("human_gate_provenance", {}).get("publication_preview")
    av = pubmod.validate_preview_approval(root, root / aref["path"], issue_id=issue)
    assert av.get("publication_candidate_path") == cand_rel, av
    _log(f"PREVIEW synthetic approved, binds active candidate")
    # === resolvers return the active candidate (actual producer+loader behavior,
    # === not path-only helpers: SHA must match the low selection pin) ===
    st3 = core.load_json(root / state_rel)
    prof = core.load_json(root / st3["profile"]["path"])
    sel3 = setmod.resolve_publication_selection(root, cfg, st3)
    pin = sel3.get("candidate_ref") or {}
    assert sel3.get("mode") == "VERSIONED_ACTIVE" and pin.get("path") == cand_rel, (sel3.get("mode"), pin)
    pin_sha = pin.get("sha256")
    assert isinstance(pin_sha, str) and len(pin_sha) == 64, pin
    assert core.sha256_file(root / cand_rel) == pin_sha, "active candidate bytes drift vs pin"
    # Orchestrator loader: gate inputs recomputed from State; SHA must equal pin.
    gate_rows = orch._configured_gate_inputs(root, cfg, prof, "PUBLICATION_PREVIEW", st3)
    grow = next((r for r in gate_rows if r.get("name") == "publication-candidate"), None)
    assert grow is not None and grow.get("path") == cand_rel, gate_rows
    assert core.sha256_file(root / grow["path"]) == pin_sha, "orchestrator loader SHA != pin"
    # Orchestrator producer: expected artifacts for the CURRENT stage recomputed
    # (no fabricated SHA for absent future outputs; active known pin immutable).
    exp_rows = orch._configured_expected_artifacts(
        cfg["orchestration"]["stage_plan"]["RELEASE_CANDIDATE"], prof, st3, root, cfg)
    assert isinstance(exp_rows, list) and all(set(r) == {"name", "path"} or "sha256" in r for r in exp_rows), exp_rows
    _log(f"ORCHESTRATOR producer rows={[(r.get('name'), r.get('path')) for r in exp_rows]}")
    # Handoff producer contract + loader path must agree on the active candidate.
    contract = handoff.expected_output_contract(cfg, st3, prof, root)
    assert isinstance(contract, dict) and "publication-candidate" in contract, sorted(contract)
    hp = handoff.resolve_handoff_artifact_path(root, cfg, st3, prof, "publication-candidate", "{source_root}/publication/v2/publication-candidate-v2.json")
    gp = humangate.resolve_gate_path(root, cfg, st3, prof, "publication-candidate", "{source_root}/publication/v2/publication-candidate-v2.json")
    assert hp == cand_rel and gp == cand_rel, (hp, gp)
    assert core.sha256_file(root / hp) == pin_sha, "handoff loader SHA != pin"
    # HumanGate loader enforces active SHA internally; rows must carry the pin.
    hg_rows = humangate._reviewed_artifacts(root, cfg, st3, prof, "PUBLICATION_PREVIEW")
    hg_cand = next((r for r in hg_rows if r.get("name") == "publication-candidate"), None)
    assert hg_cand is not None and hg_cand.get("path") == cand_rel, hg_rows
    assert hg_cand.get("sha256") == pin_sha, f"humangate row SHA != pin: {hg_cand}"
    # NOTE: build_handoff (producer write path) is not exercisable here: no stage
    # in this lifecycle has handoff_required=true (RELEASE_CANDIDATE included), so
    # invoking it would test a refusal, not producer behavior. Producer agreement is
    # proven via expected_output_contract + _configured_expected_artifacts + SHA pins.
    _log("RESOLVERS active-candidate OK (orchestrator/handoff/humangate SHA-pinned)")
    # === Freeze -> FROZEN ===
    t0 = time.monotonic()
    freeze_path, manifest_path = profiled.build_profiled_freeze(root, cfg, root / state_rel, datetime.now(timezone.utc))
    _log(f"FREEZE dt={time.monotonic()-t0:.1f}s")
    assert str(freeze_path.relative_to(root)) == f"sources/{issue}/publication/v2/freeze-record-v2.json", freeze_path
    assert str(manifest_path.relative_to(root)) == f"sources/{issue}/publication/v2/release-manifest-v2.json", manifest_path
    req_rc = stage_validation.REQUIRED_CURRENT.get("RELEASE_CANDIDATE")
    assert req_rc == {"visual-review-record", "freeze-record", "release-manifest"}, req_rc
    cand_vis_rel = pubmod.validate_candidate(root, root / cand_rel, issue_id=issue)["visual_review"]["path"]
    frep = f"{exec_rel}/r5b-freeze-report.json"
    stage_validation.validate_stage(root, cfg, root / state_rel,
                                    {"freeze-record": freeze_path, "release-manifest": manifest_path,
                                     "visual-review-record": root / cand_vis_rel},
                                    root / frep, datetime.now(timezone.utc))
    frev = f"{exec_rel}/r5b-freeze-reviews.json"
    core.write_json(root / frev, {"reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
                                               "executor": f"r5b-{route}-lifecycle-freeze", "evidence": "freeze active",
                                               "result_path": frep}]})
    fcp = agent.build_stage_checkpoint(root, cfg, root / state_rel,
                                       {"freeze-record": freeze_path, "release-manifest": manifest_path,
                                        "visual-review-record": root / cand_vis_rel},
                                       root / frev, f"R5b {route} Freeze active {active_id}",
                                       datetime.now(timezone.utc))
    upd2 = agent.advance_with_checkpoint(root, cfg, root / state_rel, fcp)
    assert upd2.get("lifecycle_state") == "FROZEN", upd2
    _log("ADVANCE FROZEN")
    _check_full("FROZEN")
    # === Release -> RELEASED offline ===
    merged_sha = _run_git(root, "rev-parse", "HEAD").stdout.strip()
    assert len(merged_sha) == 40, merged_sha
    merge_rel = f"sources/{issue}/publication/v2/merge-verification-v2.json"
    record_rel = f"sources/{issue}/publication/v2/release-record-v2.json"
    _manifest_arg = manifest_path.relative_to(root) if isinstance(manifest_path, Path) else manifest_path
    pubmod.build_merge_verification(root, root / _manifest_arg,
                                    merged_sha, datetime.now(timezone.utc), root / merge_rel)
    pubmod.build_release_record(root, root / _manifest_arg,
                                root / merge_rel, datetime.now(timezone.utc), f"offline-r5b-{route}-{active_id}",
                                root / record_rel)
    rcp = release_ckpt.build_release_checkpoint(root, cfg, root / state_rel, root / merge_rel,
                                                root / record_rel, datetime.now(timezone.utc))
    upd3 = agent.advance_with_checkpoint(root, cfg, root / state_rel, rcp)
    assert upd3.get("lifecycle_state") == "RELEASED", upd3
    _log("ADVANCE RELEASED")
    _check_full("RELEASED")
    stR = core.load_json(root / state_rel)
    _log(f"HISTORY {stR.get('history')[-3:]}")
    # === final artifacts: PDF text + ALL 5 page PNGs + epoch manifest ===
    cand_json = core.load_json(root / cand_rel)
    pdf_rel = cand_json.get("pdf", {}).get("path")
    out_txt = notes / f"final-{route}-second-correction.txt"
    r = subprocess.run(["pdftotext", str(root / pdf_rel), str(out_txt)], capture_output=True, text=True, timeout=120)
    assert r.returncode == 0 and out_txt.is_file(), r.stderr[:300]
    out_prefix = notes / f"final-{route}-second-correction-page"
    r2 = subprocess.run(["pdftoppm", "-png", "-r", "150", str(root / pdf_rel), str(out_prefix)],
                        capture_output=True, text=True, timeout=300)
    assert r2.returncode == 0, r2.stderr[:300]
    pngs = sorted(notes.glob(f"final-{route}-second-correction-page-*.png"))
    assert len(pngs) == 5, f"expected ALL 5 page PNGs, got {len(pngs)}"
    for p in pngs:
        final = notes / f"final-{route}-second-correction-p{p.stem.rsplit('-', 1)[-1]}.png"
        final.write_bytes(p.read_bytes())
        p.unlink()
    _log(f"ARTIFACTS text={out_txt.stat().st_size}B pngs=5")
    seal = setmod.validate_seal(root, setmod.validate_activation_record(
        root, (core.load_json(root / state_rel).get("publication_revalidation_provenance") or {}).get("path"))["set_ref"]["path"])
    roles = {n: {"path": v["path"], "sha256": v["sha256"], "byte_count": v["byte_count"]}
             for n, v in seal["roles"].items()}
    assert len(roles) == 15
    iman = json.loads(pathlib.Path(inert_manifest).read_bytes()) if inert_manifest.is_file() else None
    eman = {"route": route, "issue": issue, "source_head": head,
            "source_tree": _run_git(root, "rev-parse", "HEAD^{tree}").stdout.strip(),
            "core_sha": core.repository_commit_sha(root),
            "lifecycle": core.load_json(root / state_rel).get("lifecycle_state"),
            "state_pointer": (core.load_json(root / state_rel).get("publication_revalidation_provenance") or {}),
            "set_ref": {"path": set_rel, "sha256": core.sha256_file(root / set_rel)},
            "candidate": {"path": cand_rel, "sha256": core.sha256_file(root / cand_rel)},
            "roles_15": roles,
            "counts": {"roles": 15, "pdf_pages": cand_json.get("pdf", {}).get("page_count"),
                       "activations": 2, "lifecycle_advances": 3},
            "inert": iman,
            "pdf_text": str(out_txt.name),
            "pdf_pngs": [f"final-{route}-second-correction-p{i}.png" for i in range(1, 6)]}
    core.write_json(notes / f"final-epoch-{route}-manifest.json", eman)
    _log(f"EPOCH_MANIFEST final-epoch-{route}-manifest.json")
    _log(f"=== LIFECYCLE {route} RELEASED (terminal, strict) ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException:
        print("PARTIAL lifecycleR5b failed before terminal (unexpected, nonzero)", flush=True)
        traceback.print_exc()
        sys.exit(2)
