#!/usr/bin/env python3
"""SP input-only preflight r7 (D165 fix) — SOURCE REVIEW ONLY, DO NOT EXECUTE YET.

Stages exactly ONE new active file (verbatim r5 bytes) after authorization;
17 Raw + supplement ffcd... are retained inputs (NOT new writes). Reuses pinned
r6 helpers (hash-verified before import) + actual normal package/input
validation. No State/CP/Human/source/config/schema/test mutation.
Baseline NOW 1056/37 (new r7 manifest); old backups preserved; later exact2
regen still required before retry with current canonical 253cb2ea/18a05292.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("REFUSE: PYTHONDONTWRITEBYTECODE=1 required")

REPO_ROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work")
WSROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
SRC_REL = Path("sources/SP-efficient-llm-2026")
ISSUE = "SP-efficient-llm-2026"
HIST_IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
R6_TOOL = RESUME / "sp-operator-prepare-r6-20261104.py"
R6_TOOL_SHA = "2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664"
GEN_MANIFEST = RESUME / "sp-prepare-expected-manifest-r7-D165fix-20261105.json"
R5_INPUT = RESUME / "sp-corrected-input-r5-D165fix-20261105.json"
R4_SUPP = RESUME / "sp-corrected-supplement-r4-20261104.json"
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}")
HEX64_RE = re.compile(r"[0-9a-f]{64}")
HEX40_RE = re.compile(r"[0-9a-f]{40}")


def _load_r6():
    data = R6_TOOL.read_bytes()
    if hashlib.sha256(data).hexdigest() != R6_TOOL_SHA:
        raise ValueError("r6 helper drift (refuse)")
    import importlib.util
    spec = importlib.util.spec_from_file_location("r6prepare", R6_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def stage_preflight(ret_dir: Path, new_id: str, manifest_path: Path, exp_manifest_sha: str) -> dict:
    if not ID_RE.fullmatch(new_id or ""):
        raise ValueError(f"bad new input id: {new_id!r}")
    R6 = _load_r6()
    manifest = R6._verify_manifest_self(manifest_path, exp_manifest_sha)
    repo = REPO_ROOT.resolve()
    errs: list[str] = []
    try:
        pre = R6._phase0_source_precheck(repo, manifest)
    except ValueError as e:
        raise ValueError(f"phase0: {e}") from e
    M = R6._bind_roots_after_import(repo, pre)
    core = M["core"]
    ctx: dict = {}
    try:
        live_impl = core.repository_commit_sha(repo)
        if not HEX40_RE.fullmatch(live_impl or ""):
            errs.append(f"live impl not 40-hex: {live_impl!r}")
        ctx["live_impl"] = live_impl
        if live_impl != manifest["active_instance"]["recorded_head"]:
            errs.append("live HEAD drift vs recorded e84 (refuse)")
        cfg, state, state_path, profile_path = R6._strict_state_and_ready(repo, M, manifest)
        ctx["state_path"] = state_path
        live_files, live_dirs, werr = R6._walk_sp_tree_stdlib(repo, SRC_REL)
        errs.extend(werr)
        if not werr:
            exp_f = {e["rel"]: e for e in manifest["sp_tree_full"]["files"]}
            exp_d = {e["rel"] for e in manifest["sp_tree_full"]["dirs"]}
            if len(exp_f) != 1056 or len(exp_d) != 37:
                errs.append(f"manifest baseline not 1056/37: {len(exp_f)}/{len(exp_d)}")
            errs.extend(R6._compare_sp_tree(live_files, live_dirs, exp_f, exp_d))
        errs.extend(f"intended: {e}" for e in R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
        r5_raw = R5_INPUT.read_bytes()
        if hashlib.sha256(r5_raw).hexdigest() != manifest["corrected"]["input"]["sha256"]:
            errs.append("r5 packet DATA drift vs new manifest (refuse)")
        r4_raw = R4_SUPP.read_bytes()
        if hashlib.sha256(r4_raw).hexdigest() != manifest["corrected"]["supplement"]["sha256"]:
            errs.append("r4 supplement drift vs manifest")
        r5 = json.loads(r5_raw.decode("utf-8"))
        r4supp = json.loads(r4_raw.decode("utf-8"))
        if len(r5.get("records", [])) != 160 or len(r5.get("completeness", {}).get("obligations", [])) != 15:
            errs.append("r5 counts != 160/15 (refuse)")
        if r5.get("issue_id") != ISSUE or r5.get("schema_version") != "2.0-rc1":
            errs.append("r5 identity mismatch")
        rec = next((x for x in r5["records"] if x.get("discovery_id") == "EFF-D165"), None)
        if rec is None or "Bound PR body fully consumed" not in rec["claims"][0].get("context", ""):
            errs.append("r5 D165 context fix absent")
        if "chronology corroboration only" not in rec["verification"][0].get("finding", ""):
            errs.append("r5 D165 finding fix absent")
        if "per commit messages +" in rec["verification"][0].get("finding", ""):
            errs.append("r5 still claims per-commit-messages authority (refuse)")
        errs.extend(f"rows: {e}" for e in R6._check_supplement_rows_stdlib(repo, r4supp["sources"], manifest["supplement30"], WSROOT))
        for s in r4supp["sources"]:
            if s["evidence_task_id"] != M["ev"].stable_task_id(ISSUE, s["discovery_id"]):
                errs.append(f"task_id mismatch: {s['discovery_id']}")
        with M["at"].current_stage_basis_override():
            acc_disc = M["disc"].validate_acceptance(repo, (repo / SRC_REL) / "discovery/discovery-accepted-v2.json")
            root_p = core.repo_local_path(repo, acc_disc["discovery_path"], "accepted Discovery JSONL")
            active = M["sc"].resolve_active_screening_acceptance(repo, state_path, live_impl)
            _sp = Path(active["path"])
            scr_p = _sp if _sp.is_absolute() else (repo / _sp)
            eff = M["sc"].resolve_effective_discovery_basis(repo, scr_p.parent / "package.json", live_impl, accepted_root_path=root_p)
        if not eff.get("root_records") or not eff.get("records"):
            errs.append("effective basis empty")
        ctx.update({"scr_p": scr_p, "disc_p": Path(eff["path"]) if Path(eff["path"]).is_absolute() else (repo / eff["path"]),
                    "disc_recs": eff["records"], "root_recs": eff["root_records"], "r5": r5, "r5_raw": r5_raw})
        new_rel = SRC_REL / f"evidence/proposed-input/interactive-evidence-{new_id}.json"
        ctx["new_rel"] = new_rel.as_posix()
        try:
            R6._require_absent(repo, new_rel)
        except ValueError as e:
            errs.append(str(e))
        # retained inputs must be present-pinned (NOT new writes)
        for rel_key in ("retained_17",):
            pass
        errs.extend(f"gates: {e}" for e in R6._check_gates_absent(repo))
        errs.extend(f"refs: {e}" for e in R6._scan_ledger_refs(repo, manifest["stage_ledger_ref_scan"]))
        for key in ("state", "profile", "ledger", "completeness"):
            try:
                R6._pin_live(repo, Path(manifest["original_authority"][key]["rel"]), manifest["original_authority"][key])
            except ValueError as e:
                errs.append(f"canonical {key}: {e}")
        for key, pin in manifest["original_authority"].items():
            if key.startswith("accepted_") and isinstance(pin, dict) and "rel" in pin:
                try:
                    R6._pin_live(repo, Path(pin["rel"]), pin)
                except ValueError as e:
                    errs.append(f"accepted {key}: {e}")
    except ValueError as e:
        errs.append(f"phase1 exception: {e}")
    if errs:
        raise ValueError("preflight FAILED (zero active writes):\n- " + "\n- ".join(errs[:25]))
    try:
        _r = ret_dir if ret_dir.is_absolute() else (Path.cwd() / ret_dir)
        _r = Path(os.path.normpath(str(_r)))
        R6._require_absent_under(WSROOT, ret_dir)
        _r.parent.mkdir(parents=True, exist_ok=True)
    except (ValueError, OSError) as e:
        raise ValueError(f"retention refused: {e}") from e
    try:
        _r.mkdir(exist_ok=False)
    except FileExistsError:
        raise ValueError(f"single-use refuse: retention exists: {_r}")
    ret_dir = _r
    journal: list[dict] = [{"step": "phase1", "result": "pass", "live_impl": ctx["live_impl"]}]
    new_abs = repo / Path(ctx["new_rel"])
    got = R6._stage_bytes_exclusive(new_abs, repo, ctx["r5_raw"])
    journal.append({"step": "stage-1-input", "rel": ctx["new_rel"], **got})
    pkg_dir = ret_dir / f"pkg-{new_id}"
    R6._require_absent_under(WSROOT, pkg_dir)
    supp_abs = repo / SRC_REL / "external/evidence-supplement/evidence-authority-supplement-r6-sp17-20261104T162747Z.json"
    with M["at"].current_stage_basis_override():
        pkg_path = M["ev"].prepare_evidence_package(repo, ctx["state_path"], ctx["disc_p"], ctx["scr_p"], pkg_dir, ctx["live_impl"], supp_abs)
    package = json.loads(pkg_path.read_bytes().decode("utf-8"))
    task_meta = {m["discovery_ids"][0]: m for m in package["tasks"]}
    with M["at"].current_stage_basis_override():
        rs, _, rd = M["ev"].validate_screening_acceptance(repo, ctx["scr_p"], ctx["disc_p"], ISSUE, ctx["live_impl"])
        rctx = M["ev"]._resolve_phase_supplement_context(repo, package, implementation_sha=ctx["live_impl"], screening_acceptance=rs, discoveries=rd)
        rpins = M["ev"]._capture_phase_pins((("Evidence package", pkg_path),) + tuple((f"Evidence Task {m['evidence_task_id']}", pkg_path.parent / m["path"]) for m in package["tasks"]))
    tsids: dict[str, set[str]] = {}
    for did, meta in task_meta.items():
        t = json.loads((pkg_path.parent / meta["path"]).read_bytes().decode("utf-8"))
        tsids[did] = set(M["ev"]._merge_supplement_task_sources(M["ev"]._discovery_task_sources(t), t, rctx["entries"]))
    doc = json.loads(new_abs.read_bytes().decode("utf-8"))
    profile = core.load_json(repo / (SRC_REL / "production-profile.json"))
    by_id, runner, _ = M["rn"].validate_interactive_input(doc, profile, set(task_meta), tsids, discovery_records=ctx["disc_recs"], root_discovery_records=ctx["root_recs"])
    journal.append({"step": "package+validate-input", "pkg": pkg_dir.name, "tasks": len(task_meta), "records": len(by_id)})
    lf, ld, w4 = R6._walk_sp_tree_stdlib(repo, SRC_REL)
    if w4:
        raise ValueError("terminal walk FAILED:\n- " + "\n- ".join(w4[:10]))
    exp = {e["rel"]: e for e in manifest["sp_tree_full"]["files"]}
    exp[ctx["new_rel"]] = {"sha256": got["sha256"], "bytes": got["bytes"], "mode": "0o664", "nlink": 1}
    terr = R6._compare_sp_tree(lf, ld, exp, {e["rel"] for e in manifest["sp_tree_full"]["dirs"]})
    if terr:
        raise ValueError("terminal tree FAILED:\n- " + "\n- ".join(terr[:10]))
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
        raise ValueError("manifest changed mid-run (refuse READY)")
    R6._strict_state_and_ready(repo, M, manifest)
    ready = {"ready": True, "stage": "preflight-only", "no_removal": True, "no_retry": True,
             "manifest": {"path": manifest_path.name, "sha256": exp_manifest_sha},
             "live_implementation_sha": ctx["live_impl"], "historical_implementation_sha": HIST_IMPL,
             "supplement_id": "r6-sp17-20261104T162747Z",
             "new_supplement": {"rel": "sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r6-sp17-20261104T162747Z.json",
                                "bytes": 30922, "sha256": "ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3", "mode": "0o664", "retained": True},
             "new_input": {"rel": ctx["new_rel"], **got},
             "staged_raw": [{"rel": r["raw_path"], "sha256": r["raw_sha256"], "bytes": r["byte_count"], "mode": "0o664", "retained": True} for r in manifest["supplement30"] if r["raw_path"].startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/raw/sp17-")],
             "task_count": len(task_meta), "input_records": len(by_id),
             "retained_pkg_dir": pkg_dir.name, "journal": journal}
    R6._stage_bytes_exclusive_local(ret_dir / "READY.json", (json.dumps(ready, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    R6._stage_bytes_exclusive_local(ret_dir / "journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"ready": str(ret_dir / "READY.json"), "tasks": len(task_meta), "records": len(by_id)}


def main() -> int:
    global REPO_ROOT
    ap = argparse.ArgumentParser(description="SP input-only preflight r7 (review only, do not run yet)")
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--new-input-id", type=str, required=True)
    ap.add_argument("--manifest", type=Path, default=GEN_MANIFEST)
    ap.add_argument("--expected-manifest-sha", type=str, required=True)
    ap.add_argument("--expected-tool-sha", type=str, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    a = ap.parse_args()
    REPO_ROOT = a.repo_root
    try:
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != a.expected_tool_sha:
            raise ValueError("wrapper drift vs expected tool hash (refuse)")
        out = stage_preflight(a.retention_dir, a.new_input_id, a.manifest, a.expected_manifest_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"PREFLIGHT_REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"stage": "preflight-only", "exit": 0, **out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
