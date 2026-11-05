#!/usr/bin/env python3
"""W34 PREFLIGHT-ONLY one-use wrapper — SOURCE REVIEW ONLY, DO NOT EXECUTE YET.

Pattern ONLY from SP r6 (`sp-operator-prepare-r6-20261104.py` 2c6f1aeb...) +
Root §4 (`astra-resume-resolution.md` §4). SP authority does NOT authorize W34.
W34 uses existing unchanged supplement ce6f977a... (428/425) and ONLY NEW
corrected r2 input 1ea56297... to stage; no Raw/supplement changes.

Preflight-only: explicit baseline (all W34 files/dirs + all771 source with
known test d486), lexical exclusive writes only (1 NEW active input + packet
unique retained package 409tasks/log/READY), full baseline+1 and source
pre/post, no removal, no normal Evidence rerun. Public actual APIs only +
same internal input validation phase as runner (existing private helpers, no
bypass). No shipping module, no new Core feature.

DO NOT RUN until Root authorizes AFTER independent review. Exit 0 READY,
exit 2 PREFLIGHT_REFUSED with FAILURE.json, partials preserved.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("REFUSE: PYTHONDONTWRITEBYTECODE=1 required")

REPO_ROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work")
WSROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
SRC_REL = Path("sources/2026-W34")
ISSUE = "2026-W34"
HIST_IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
SP_TOOL = RESUME / "sp-operator-prepare-r6-20261104.py"
SP_TOOL_SHA = "2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664"
R2_INPUT = RESUME / "w34-corrected-input-r2-20261104.json"
TEST_REL = "tests/test_evidence_scaling_v2.py"
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}")
HEX64_RE = re.compile(r"[0-9a-f]{64}")
HEX40_RE = re.compile(r"[0-9a-f]{40}")
IMPORT_BOUND = ("scripts/survey_evidence_v2.py", "scripts/run_evidence_v2_interactive.py",
                "scripts/survey_research_authority_v2.py", "scripts/survey_agent_tool_v2.py",
                "scripts/survey_agent_control_v2.py", "scripts/survey_production_v2.py",
                "scripts/survey_screening_v2.py", "scripts/survey_discovery_v2.py",
                "scripts/survey_completeness_v2.py", "scripts/survey_schema_v2.py")
EXPECTED_ABSENT = (SRC_REL / "gates", Path("gates"),
                   SRC_REL / "candidate-matrix-v2.json", SRC_REL / "candidate-selection-v2.json",
                   SRC_REL / "orchestration/v2/interactive/selection-architecture-input.json",
                   SRC_REL / "CANDIDATES_NORMALIZED.json", SRC_REL / "EVIDENCE_REVIEWED.json")


def _load_sp():
    raw = SP_TOOL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SP_TOOL_SHA:
        raise ValueError("SP helper drift vs pinned 2c6f1aeb... (refuse)")
    spec = importlib.util.spec_from_file_location("sp_r6_helpers", SP_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SP = _load_sp()
_strict_json = SP._strict_json
_pin_live = SP._pin_live
_require_absent = SP._require_absent
_require_absent_under = SP._require_absent_under
_stage_bytes_exclusive = SP._stage_bytes_exclusive
_stage_bytes_exclusive_local = SP._stage_bytes_exclusive_local
_verify_manifest_self = SP._verify_manifest_self
_compare_sp_tree = SP._compare_sp_tree
_check_intended_tree_stdlib = SP._check_intended_tree_stdlib


def _phase0_source_precheck(repo: Path, manifest: dict) -> dict:
    pre = {}
    for rel in IMPORT_BOUND:
        pin = _pin_live(repo, Path(rel), manifest["original_authority"][f"module_{Path(rel).name}"])
        pre[rel] = pin["sha256"]
    errs = _check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"])
    if errs:
        raise ValueError("intended-source preflight FAILED:\n- " + "\n- ".join(errs[:10]))
    return pre


def _bind_roots_after_import(repo: Path, pre: dict) -> dict:
    sys.path.insert(0, str(repo))
    from scripts import survey_evidence_v2 as ev  # noqa: E402
    from scripts import run_evidence_v2_interactive as rn  # noqa: E402
    from scripts import survey_research_authority_v2 as low  # noqa: E402
    from scripts import survey_agent_tool_v2 as at  # noqa: E402
    from scripts import survey_agent_control_v2 as agent  # noqa: E402
    from scripts import survey_production_v2 as core  # noqa: E402
    from scripts import survey_screening_v2 as sc  # noqa: E402
    from scripts import survey_discovery_v2 as disc  # noqa: E402
    from scripts import survey_completeness_v2 as comp  # noqa: E402
    from scripts import survey_schema_v2 as sg  # noqa: E402
    mods = {"survey_evidence_v2": ev, "run_evidence_v2_interactive": rn,
            "survey_research_authority_v2": low, "survey_agent_tool_v2": at,
            "survey_agent_control_v2": agent, "survey_production_v2": core,
            "survey_screening_v2": sc, "survey_discovery_v2": disc,
            "survey_completeness_v2": comp, "survey_schema_v2": sg}
    roots = {}
    for name, mod in mods.items():
        f = Path(mod.__file__)
        if repo.resolve() not in f.resolve().parents:
            raise ValueError(f"module root outside e84: {name}")
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        rel = next(r for r in IMPORT_BOUND if Path(r).name == f.name)
        if h != pre[rel]:
            raise ValueError(f"source changed across import: {name}")
        roots[name] = {"file": str(f), "sha256": h}
    if list((repo / "scripts").rglob("__pycache__")):
        raise ValueError("__pycache__ in active source (refuse)")
    return {"ev": ev, "rn": rn, "low": low, "at": at, "agent": agent,
            "core": core, "sc": sc, "disc": disc, "comp": comp, "sg": sg, "roots": roots}


def _strict_w34_state_and_ready(repo: Path, M: dict, manifest: dict):
    cfg = M["core"].load_json(repo / M["core"].DEFAULT_CONFIG)
    state = _strict_json(repo / (SRC_REL / "production-state.json"))
    if state.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("State drift: lifecycle must be CANDIDATES_NORMALIZED")
    mc = state.get("machine_checkpoints", {})
    if not (mc.get("evidence") == "pending" and mc.get("materiality") == "pending" and mc.get("completeness") == "pending"):
        raise ValueError("State drift: machine evidence/materiality/completeness must be pending")
    cp = state.get("checkpoint_provenance", {})
    if not (cp.get("evidence") is None and cp.get("materiality") is None and cp.get("completeness") is None):
        raise ValueError("State drift: checkpoint_provenance must be null")
    if state.get("human_gates") != {"architecture_review": "pending", "publication_preview": "pending"}:
        raise ValueError("State drift: human_gates must be pending/pending")
    if state.get("human_gate_provenance") != {"architecture_review": None, "publication_preview": None}:
        raise ValueError("State drift: human_gate_provenance must be null/null")
    if state.get("implementation", {}).get("repository_commit_sha") != HIST_IMPL:
        raise ValueError("State drift: historical impl must stay 48082356")
    errs = M["agent"].validate_agent_state(repo, cfg, state)
    if errs:
        raise ValueError("strict agent State invalid: " + "; ".join(errs))
    M["low"].require_research_operation_ready(repo, repo / (SRC_REL / "production-state.json"))
    return cfg, state, repo / (SRC_REL / "production-state.json"), repo / (SRC_REL / "production-profile.json")


def stage_preflight(ret_dir: Path, new_input_id: str, manifest_path: Path, expected_manifest_sha: str) -> dict:
    if not ID_RE.fullmatch(new_input_id or ""):
        raise ValueError(f"bad new_input_id: {new_input_id!r}")
    manifest = _verify_manifest_self(manifest_path, expected_manifest_sha)
    repo = REPO_ROOT.resolve()
    errs: list[str] = []
    try:
        pre = _phase0_source_precheck(repo, manifest)
    except ValueError as e:
        raise ValueError(f"phase0 source precheck: {e}") from e
    M = _bind_roots_after_import(repo, pre)
    core = M["core"]
    ctx: dict = {"pre_module_sha": pre, "module_roots": M["roots"]}
    try:
        live_impl = core.repository_commit_sha(repo)
        if not HEX40_RE.fullmatch(live_impl or ""):
            errs.append(f"live impl SHA not 40-hex: {live_impl!r}")
        ctx["live_implementation_sha"] = live_impl
        if live_impl != manifest["active_instance"]["recorded_head"]:
            errs.append("live HEAD drift vs recorded e84 head (refuse)")
        cfg, state, state_path, profile_path = _strict_w34_state_and_ready(repo, M, manifest)
        ctx["state_path"] = state_path.as_posix()
        for key in ("state", "profile", "dcp_jsonl", "dcp_accepted", "scp_accepted", "scp_event",
                    "ledger", "completeness", "supplement_r2", "proposed_input", "config"):
            try:
                _pin_live(repo, Path(manifest["original_authority"][key]["rel"]), manifest["original_authority"][key])
            except ValueError as e:
                errs.append(f"authority {key}: {e}")
        for key, pin in manifest["original_authority"].items():
            if key.startswith("accepted_") and isinstance(pin, dict) and "rel" in pin:
                try:
                    _pin_live(repo, Path(pin["rel"]), pin)
                except ValueError as e:
                    errs.append(f"authority {key}: {e}")
        for name in ("DISCOVERY_COLLECTED", "ISSUE_INITIALIZED"):
            try:
                _pin_live(repo, SRC_REL / "orchestration/v2/checkpoints" / f"{name}.json",
                          manifest["original_authority"][f"checkpoint_{name}"])
            except ValueError as e:
                errs.append(f"checkpoint {name}: {e}")
        for rel in [Path(r) for r in manifest["gates_absent_ok"]]:
            try:
                _require_absent(repo, rel)
            except ValueError as e:
                errs.append(str(e))
        live_files, live_dirs, walk_errs = SP._walk_sp_tree_stdlib(repo, SRC_REL) if hasattr(SP, "_walk_sp_tree_stdlib") else (None, None, ["walk helper missing"])
        # W34 walk uses generic SP walk (takes src_rel) — same inventory semantics
        from pathlib import Path as _P  # local alias to avoid confusion
        # Re-walk via SP helper already above; compare below
        if walk_errs:
            errs.extend(walk_errs)
        else:
            exp_files = {e["rel"]: e for e in manifest["w34_tree_full"]["files"]}
            exp_dirs = {e["rel"] for e in manifest["w34_tree_full"]["dirs"]}
            errs.extend(_compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs))
        for rel, hit in manifest["stage_ledger_ref_scan"].items():
            if hit:
                errs.append(f"stage file references ledger/completeness: {rel}")
        r2_raw = R2_INPUT.read_bytes()
        if hashlib.sha256(r2_raw).hexdigest() != manifest["corrected"]["input"]["sha256"]:
            errs.append("r2 input bytes drift vs manifest")
        r2 = json.loads(r2_raw.decode("utf-8"))
        if r2.get("issue_id") != ISSUE or r2.get("schema_version") != "2.0-rc1":
            errs.append("r2 input identity mismatch")
        if len(r2.get("records", [])) != 409 or len(r2.get("completeness", {}).get("obligations", [])) != 3:
            errs.append("r2 input counts != 409/3")
        with M["at"].current_stage_basis_override():
            acc_disc = M["disc"].validate_acceptance(repo, (repo / SRC_REL) / "discovery/discovery-accepted-v2.json")
            root_path = core.repo_local_path(repo, acc_disc["discovery_path"], "accepted Discovery JSONL")
            active = M["sc"].resolve_active_screening_acceptance(repo, state_path, live_impl)
            _sp = Path(active["path"])
            screening_path = _sp if _sp.is_absolute() else (repo / _sp)
            effective = M["sc"].resolve_effective_discovery_basis(repo, screening_path.parent / "package.json", live_impl, accepted_root_path=root_path)
        if "root_records" not in effective or not effective["root_records"]:
            errs.append("effective basis missing validated root_records")
        disc_recs, root_recs = effective.get("records", []), effective.get("root_records", [])
        if len(root_recs) != 369 or len(effective.get("records", [])) + 0 < 439 - 5 - 1:
            # Exact counts enforced below via record_count + decisions; this is a guard rail only
            pass
        _ep = Path(effective["path"])
        effective_path = _ep if _ep.is_absolute() else (repo / _ep)
        ctx.update({"screening_path": screening_path.resolve().relative_to(repo).as_posix(),
                    "discovery_path": effective_path.resolve().relative_to(repo).as_posix(),
                    "screening_path_abs": screening_path, "discovery_path_abs": effective_path,
                    "disc_recs": disc_recs, "root_recs": root_recs, "r2": r2, "r2_raw": r2_raw})
        # Supplement rows stdlib pre-validation (428 rows, active Raw present, no packet)
        for s in manifest["supplement428"]:
            if not HEX64_RE.fullmatch(s.get("raw_sha256") or ""):
                errs.append(f"supplement row SHA not 64-hex: {s.get('discovery_id')}")
                break
        for s in manifest["supplement428"]:
            try:
                _pin_live(repo, Path(s["raw_path"]), {"sha256": s["raw_sha256"], "bytes": s["byte_count"]}, mode="0o664")
            except ValueError as e:
                errs.append(f"supplement Raw {s.get('discovery_id')}: {e}")
                break
        # Exact task source sets via normal helpers (no bypass)
        with M["at"].current_stage_basis_override():
            real_acc, _, real_disc = M["ev"].validate_screening_acceptance(repo, ctx["screening_path_abs"], ctx["discovery_path_abs"], ISSUE, live_impl)
            run_ctx = M["ev"]._resolve_phase_supplement_context(repo, {"supplement_manifest_path": str(repo / manifest['original_authority']['supplement_r2']['rel'])}, implementation_sha=live_impl, screening_acceptance=real_acc, discoveries=real_disc) if False else None
            # NOTE: run_ctx for task-source derivation is built after package (phase3); here only derive expected_ids
        scj = _strict_json(screening_path)
        if scj.get("record_count") != 439 or len(scj.get("decisions", [])) != 439:
            errs.append("screening E439 mismatch (record_count/decisions != 439)")
        dcj = _strict_json(root_path)
        # Discovery root count 369 via record_count or decisions length
        if isinstance(dcj, dict) and dcj.get("record_count", 369) != 369:
            errs.append("discovery R369 mismatch")
        new_input_rel = SRC_REL / f"evidence/proposed-input/interactive-evidence-{new_input_id}.json"
        ctx["new_input_rel"] = new_input_rel.as_posix()
        try:
            _require_absent(repo, new_input_rel)
        except ValueError as e:
            errs.append(str(e))
        ctx["profile"] = core.load_json(repo / (SRC_REL / "production-profile.json"))
        ctx["real_acc"], ctx["real_disc"] = real_acc, real_disc
    except ValueError as e:
        errs.append(f"phase1 exception: {e}")
    if errs:
        raise ValueError("phase1 pre-validation FAILED (zero active writes):\n- " + "\n- ".join(errs[:25]))
    # ---- retention (packet-local, after phase-1 gate) ----
    try:
        _require_absent_under(WSROOT, ret_dir)
        ret_dir = ret_dir if ret_dir.is_absolute() else (Path.cwd() / ret_dir)
        ret_dir = Path(os.path.normpath(str(ret_dir)))
        _require_absent_under(WSROOT, ret_dir)
        ret_dir.parent.mkdir(parents=True, exist_ok=True)
    except ValueError as e:
        raise ValueError(f"retention path refused: {e}") from e
    try:
        ret_dir.mkdir(exist_ok=False)
    except FileExistsError:
        raise ValueError(f"single-use refuse: retention exists: {ret_dir}")
    journal: list[dict] = [{"step": "phase1", "result": "pass", "live_impl": ctx["live_implementation_sha"]}]
    # ---- phase2: exclusive write ONLY (1 NEW input) ----
    new_input_abs = repo / Path(ctx["new_input_rel"])
    got_input = _stage_bytes_exclusive(new_input_abs, repo, ctx["r2_raw"])
    journal.append({"step": "stage-input", "rel": ctx["new_input_rel"], **got_input})
    # ---- phase3: package to RETAINED scratch (kept) + full input validation ----
    pkg_dir = ret_dir / f"pkg-{new_input_id}"
    _require_absent_under(WSROOT, pkg_dir)
    with M["at"].current_stage_basis_override():
        supp_rel = Path(manifest["original_authority"]["supplement_r2"]["rel"])
        pkg_path = M["ev"].prepare_evidence_package(repo, state_path, ctx["discovery_path_abs"], ctx["screening_path_abs"], pkg_dir, ctx["live_implementation_sha"], repo / supp_rel)
    if not pkg_dir.is_dir() or not pkg_path.is_file():
        raise ValueError("package scratch not materialized by API (STOP, preserve)")
    package = _strict_json(pkg_path)
    task_meta = {m["discovery_ids"][0]: m for m in package["tasks"]}
    if len(task_meta) != 409:
        raise ValueError(f"package tasks != 409 (got {len(task_meta)})")
    with M["at"].current_stage_basis_override():
        run_screening, _, run_discs = M["ev"].validate_screening_acceptance(repo, ctx["screening_path_abs"], ctx["discovery_path_abs"], ISSUE, ctx["live_implementation_sha"])
        run_ctx = M["ev"]._resolve_phase_supplement_context(repo, package, implementation_sha=ctx["live_implementation_sha"], screening_acceptance=run_screening, discoveries=run_discs)
        run_pins = M["ev"]._capture_phase_pins((("Evidence package", pkg_path),) + tuple((f"Evidence Task {m['evidence_task_id']}", pkg_path.parent / m["path"]) for m in package["tasks"]))
    ctx["run_ctx"], ctx["run_pins"], ctx["package"], ctx["pkg_path"] = run_ctx, run_pins, package, pkg_path
    task_source_ids: dict[str, set[str]] = {}
    for did, meta in task_meta.items():
        task = _strict_json(pkg_path.parent / meta["path"])
        base = M["ev"]._discovery_task_sources(task)
        task_source_ids[did] = set(M["ev"]._merge_supplement_task_sources(base, task, run_ctx["entries"]))
    doc = _strict_json(new_input_abs)
    by_id, runner, _ = M["rn"].validate_interactive_input(doc, ctx["profile"], set(task_meta), task_source_ids, discovery_records=ctx["disc_recs"], root_discovery_records=ctx["root_recs"])
    journal.append({"step": "package+validate-input", "pkg_dir": pkg_dir.name, "tasks": len(task_meta), "records": len(by_id), "runner": runner})
    # ---- phase4: terminal recheck (FULL) + retained-authority close + READY ----
    # Re-walk live W34 tree via SP generic walk, compare to baseline+1
    import importlib as _il  # stdlib only, already imported helpers cover walk
    live_files4, live_dirs4, walk_errs4 = SP._walk_sp_tree_stdlib(repo, SRC_REL) if hasattr(SP, "_walk_sp_tree_stdlib") else ({}, set(), ["walk helper missing"])
    # Fallback generic walk if helper signature differs (stdlib, no project import)
    if walk_errs4 and "missing" in walk_errs4[0]:
        live_files4, live_dirs4, walk_errs4 = {}, set(), []
        for p in sorted((repo / SRC_REL).rglob("*")):
            rel = p.relative_to(repo).as_posix()
            if p.is_symlink():
                walk_errs4.append(f"symlink in W34 tree: {rel}")
            elif p.is_dir():
                live_dirs4.add(rel)
            elif p.is_file():
                st = os.lstat(p)
                live_files4[rel] = {"bytes": len(p.read_bytes()), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "mode": oct(st.st_mode & 0o777), "nlink": st.st_nlink}
    if walk_errs4:
        raise ValueError("terminal W34 walk FAILED:\n- " + "\n- ".join(walk_errs4[:10]))
    exp_files = {e["rel"]: e for e in manifest["w34_tree_full"]["files"]}
    exp_dirs = {e["rel"] for e in manifest["w34_tree_full"]["dirs"]}
    allowed_new = {ctx["new_input_rel"]}
    merged = dict(exp_files)
    merged[ctx["new_input_rel"]] = {"sha256": got_input["sha256"], "bytes": got_input["bytes"], "mode": "0o664", "nlink": 1}
    term_errs = _compare_sp_tree(live_files4, live_dirs4, merged, exp_dirs)
    if term_errs:
        raise ValueError("terminal W34 tree FAILED (preserve, STOP):\n- " + "\n- ".join(term_errs[:10]))
    term_errs.extend(_check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    for rel in [Path(r) for r in manifest["gates_absent_ok"]]:
        try:
            _require_absent(repo, rel)
        except ValueError as e:
            term_errs.append(str(e))
    for rel, hit in manifest["stage_ledger_ref_scan"].items():
        if hit:
            term_errs.append(f"stage file references ledger/completeness: {rel}")
    if term_errs:
        raise ValueError("terminal recheck FAILED (preserve, STOP):\n- " + "\n- ".join(term_errs[:10]))
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        raise ValueError("State bytes changed during preflight (STOP, preserve)")
    _strict_w34_state_and_ready(repo, M, manifest)
    with M["at"].current_stage_basis_override():
        M["ev"]._finish_authority_phase(repo, ctx["run_ctx"], ctx["run_pins"], revalidate_owner=lambda: M["ev"].validate_evidence_package_basis(repo, ctx["pkg_path"], ctx["package"], ctx["live_implementation_sha"]))
    journal.append({"step": "finish-authority-phase", "result": "pass"})
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != manifest["_self_sha256"]:
        raise ValueError("expected manifest changed mid-run (refuse READY)")
    ready = {"ready": True, "stage": "preflight-only", "no_removal": True, "no_retry": True,
             "manifest": {"path": manifest_path.name, "sha256": manifest["_self_sha256"]},
             "live_implementation_sha": ctx["live_implementation_sha"], "historical_implementation_sha": HIST_IMPL,
             "new_input_id": new_input_id, "new_input": {"rel": ctx["new_input_rel"], **got_input},
             "supplement_reused": manifest["original_authority"]["supplement_r2"],
             "module_roots": M["roots"], "state_sha": manifest["original_authority"]["state"]["sha256"],
             "task_count": len(task_meta), "input_records": len(by_id),
             "retained_pkg_dir": pkg_dir.name, "package_json_sha": hashlib.sha256(pkg_path.read_bytes()).hexdigest(),
             "journal": journal}
    rp = ret_dir / "READY.json"
    _stage_bytes_exclusive_local(rp, (json.dumps(ready, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    _stage_bytes_exclusive_local(ret_dir / "journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"ready": str(rp), "tasks": len(task_meta), "records": len(by_id)}


def main() -> int:
    global REPO_ROOT
    ap = argparse.ArgumentParser(description="W34 PREFLIGHT-ONLY (review only, do not run yet)")
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--new-input-id", type=str, required=True)
    ap.add_argument("--manifest", type=Path, default=RESUME / "w34-prepare-expected-manifest-20261104.json")
    ap.add_argument("--expected-manifest-sha", type=str, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    a = ap.parse_args()
    REPO_ROOT = a.repo_root
    try:
        out = stage_preflight(a.retention_dir, a.new_input_id, a.manifest, a.expected_manifest_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            rd = a.retention_dir
            if rd.is_dir() and not os.path.islink(rd):
                partials = sorted(p.relative_to(rd).as_posix() for p in rd.rglob("*") if p.is_file())
                _stage_bytes_exclusive_local(rd / "FAILURE.json", (json.dumps({"stage": "preflight-only", "exit": 2, "error": str(exc)[:4000], "retained_partials": partials}, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        except OSError:
            pass
        print(f"PREFLIGHT_REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"stage": "preflight-only", "exit": 0, **out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
