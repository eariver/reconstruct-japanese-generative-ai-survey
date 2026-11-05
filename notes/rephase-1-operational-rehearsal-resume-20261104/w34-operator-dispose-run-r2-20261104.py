#!/usr/bin/env python3
"""W34 dispose + normal-run one-use wrapper r2 — SOURCE REVIEW ONLY, DO NOT EXECUTE.

r2 preserves v1 (`w34-operator-dispose-run-20261104.py`) untouched and fixes
independent review B1-B3 (source-only blockers, no execution yet):

 B1 invented accepted-dir fields: v1 passed
     `manifest["original_authority"].get("accepted_evidence_dirs",[])` (keys do
     not exist -> []) so old bf208/f744 counted as new -> definite post-run
     `len(new)!=1` failure. r2 derives known old dirs from FROZEN
     `w34_tree_full` directory entries + accepted file pins, asserts exactly
     one old ev dir + one old view dir before run, and passes those real sets.
 B2 no after-import re-hash: v1 pinned 10 modules + 771 BEFORE import but never
     re-hashed after import nor refused `__pycache__`. r2 re-hashes every module
     after import (hash == pre hash, root inside e84) + refuses `__pycache__`.
 B3 State strictness: v1 used `json.loads` for State; r2 uses
     `R6._strict_json` duplicate-key strict for State.
 Also: READY exact `retained_pkg_dir` path verified (no glob guess); no
 fallback metadata/default invented facts (exact keys required, no `.get`
 defaults for authority/counts); gates/CP absence via full tree + real State
 (no false absent-path labels); EFFECTIVE 439 path retained for
 Ledger/Completeness validators/counts (not SP root 369).

Single bounded operation: guarded removal of the two exact unaccepted
CAND-owned files (Ledger 76ac.../186202B, then Completeness 93db.../71532B,
both 0o664) + ONE ordinary normal Evidence retry via existing public
`rn.run` (current e84 strict facade, no outer facade). Preserves r1 preflight
and SP successes untouched. No new Raw/supplement; existing supplement
ce6f... reused; ONLY staged r2 input 1ea562... is consumed.

Reuses pinned r6 low-level helpers (2c6f1aeb... verified before import):
stdlib pinning, source771 + triangulated test, full-tree compare. W34-specific
State/tree/gates logic only; no SP-hardcoded state helpers, no SP-shaped
READY/verified-dict fabrication, no global mutation to bypass.

Phases (STOP + preserve + no auto-restore/retry on first failure):
 P0 pinning: wrapper/manifest/READY/r6-tool bytes == externally recorded
     hashes; umask recorded/restored; manifest clean; READY is preflight-only
     binding expected manifest. No active writes.
 P1 pre-disposal reads only: live HEAD == READY live impl == manifest head;
     strict W34 CAND State; full tree == baseline 1781 + staged 1 (1782);
     all771 + test pin; staged input pin vs READY + r2 packet pin;
     supplement428 rows + FULL normal supplement validation (facade);
     retained 409-task package basis validation (facade); checkpoints/accepted
     pins; State/Profile/Ledger/Completeness pins; SP completed NEW products
     snapshot (SP READY c7cd05a8... + SP DISPOSE cf26a23c... still present,
     no SP invoke). Zero active writes on failure.
 P2 NEW packet retention (DIRECTLY under resume packet) + O_EXCL backups of
     both files (chmod 0664, readback). Manifest binds old/new path, SHA,
     bytes, mode, live-verified 64-char State SHA, UTC. No rename onto names.
 P3 ledger gate: strict State + 1782 tree + all771 + same manifest/READY +
     BOTH backups re-verified + both present-pinned. Unlink ledger ONLY;
     verify absent + not-symlink; re-verify retained copy. State SHA64 checked.
 P4 completeness gate: strict State + 1781 tree (ledger absent EXPECTED,
     completeness present) + same pins + backups re-verified. Unlink
     completeness ONLY; verify both absent (1780); re-verify retained copy.
 P5 post-disposal: 1780 tree; old accepted byte-identical; State CAND unchanged.
 P6 ONE rn.run(repo, state, staged_input, existing_supplement). Owns facade.
     Preserve exact partials on failure; no retry.
 P7 post-run: State CAND + bytes unchanged; exact delta (only exact2
     regenerated + 2 NEW accepted dirs, 5 top + 409/409/409); archived input
     == NEW accepted archive path + staged bytes; package authority ==
     existing supplement; actual counts 409 results / 439 ledger rows /
     3 obligations LIMITED from files; validators use ACTUAL EFFECTIVE 439
     path (not SP root 369). Modes == recorded umask. No advance.
 P8 return gate (same captured pins, not reseal) + DISPOSE_RUN record.
     No semantic approval.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("REFUSE: PYTHONDONTWRITEBYTECODE=1 required")

REPO_ROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work")
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
SRC_REL = Path("sources/2026-W34")
ISSUE = "2026-W34"
HIST_IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
R6_TOOL = RESUME / "sp-operator-prepare-r6-20261104.py"
R6_TOOL_SHA = "2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664"
R2_INPUT = RESUME / "w34-corrected-input-r2-20261104.json"
LEDGER_REL = SRC_REL / "materiality-ledger-v2.json"
COMP_REL = SRC_REL / "profile-completeness-v2.json"
HEX64_RE = re.compile(r"[0-9a-f]{64}")
HEX40_RE = re.compile(r"[0-9a-f]{40}")


def _load_r6():
    data = R6_TOOL.read_bytes()
    if hashlib.sha256(data).hexdigest() != R6_TOOL_SHA:
        raise ValueError("r6 helper drift vs pinned 2c6f1aeb... (refuse)")
    import importlib.util
    spec = importlib.util.spec_from_file_location("r6prepare", R6_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _check_retention_root(ret_dir: Path, base: Path = RESUME) -> Path:
    abs_ret = ret_dir if ret_dir.is_absolute() else (Path.cwd() / ret_dir)
    abs_ret = Path(os.path.normpath(str(abs_ret)))
    if abs_ret.parent != base.resolve():
        raise ValueError(f"retention must sit DIRECTLY under packet (refuse): {ret_dir}")
    return abs_ret


def _verify_ready_self(ready_path: Path, expected_sha: str) -> dict:
    if not HEX64_RE.fullmatch(expected_sha or ""):
        raise ValueError("expected READY SHA must be 64-hex")
    raw = ready_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha:
        raise ValueError("READY bytes drift vs externally recorded hash (refuse)")
    val = json.loads(raw.decode("utf-8"))
    if not isinstance(val, dict) or val.get("ready") is not True or val.get("stage") != "preflight-only":
        raise ValueError("READY is not a preflight-only READY record (refuse)")
    if val.get("manifest", {}).get("sha256") is None:
        raise ValueError("READY lacks manifest binding (refuse)")
    return val


def _read_umask() -> tuple[int, int]:
    prev = os.umask(0)
    os.umask(prev)
    return prev, (0o666 & ~prev)


def _derive_old_accepted_dirs(manifest: dict) -> tuple[list[str], list[str]]:
    """Known old accepted dirs from FROZEN tree + accepted file pins.

    No invented `.get(..., [])` defaults: manifest MUST contain
    `w34_tree_full.{files,dirs}` and accepted file pins; otherwise refuse.
    Asserts exactly one old ev dir + one old view dir before run so post-run
    `len(new)==1` detection cannot misclassify bf208/f744 as new.
    """
    if "w34_tree_full" not in manifest or "dirs" not in manifest["w34_tree_full"]:
        raise ValueError("manifest lacks frozen w34_tree_full dirs (refuse)")
    dirs = [e["rel"] for e in manifest["w34_tree_full"]["dirs"]]
    ev_root = f"{SRC_REL.as_posix()}/evidence/v2/accepted"
    view_root = f"{SRC_REL.as_posix()}/evidence/v2/views/accepted"
    old_ev = sorted(d for d in dirs if d.startswith(ev_root + "/") and d.count("/") == len(ev_root.split("/")) and d != ev_root)
    old_view = sorted(d for d in dirs if d.startswith(view_root + "/") and d.count("/") == len(view_root.split("/")) and d != view_root)
    if len(old_ev) != 1 or len(old_view) != 1:
        raise ValueError(f"frozen old accepted dirs != 1+1 (got ev={old_ev} views={old_view})")
    # Cross-check against accepted file pins (parents must match derived dirs)
    pin_parents: set[str] = set()
    for key, pin in manifest["original_authority"].items():
        if not (isinstance(pin, dict) and "rel" in pin):
            continue
        if key.startswith("accepted_") and (key.endswith("_evidence-accepted.json") or key.endswith("_json")):
            pin_parents.add(str(Path(pin["rel"]).parent.as_posix()))
    if old_ev[0] not in pin_parents or old_view[0] not in pin_parents:
        raise ValueError(f"derived old dirs lack accepted file-pin parents (got {old_ev} {old_view} vs {sorted(pin_parents)})")
    return old_ev, old_view


def _bind_roots_after_import_strict(repo: Path, pre: dict, M: dict) -> dict:
    """After-import source re-hash (B2): every bound module file hash MUST equal
    its pre-import pin and live under e84; refuse `__pycache__`."""
    roots: dict = {}
    import_map = {"survey_evidence_v2": "survey_evidence_v2.py", "run_evidence_v2_interactive": "run_evidence_v2_interactive.py",
                  "survey_research_authority_v2": "survey_research_authority_v2.py", "survey_agent_tool_v2": "survey_agent_tool_v2.py",
                  "survey_agent_control_v2": "survey_agent_control_v2.py", "survey_production_v2": "survey_production_v2.py",
                  "survey_screening_v2": "survey_screening_v2.py", "survey_discovery_v2": "survey_discovery_v2.py",
                  "survey_completeness_v2": "survey_completeness_v2.py", "survey_schema_v2": "survey_schema_v2.py"}
    for name, fname in import_map.items():
        mod = M[name]
        f = Path(mod.__file__)
        if repo.resolve() not in f.resolve().parents:
            raise ValueError(f"module root outside e84: {name}")
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        rel = next(r for r in ("scripts/" + fname,) if True)
        # pre keys are full rels (scripts/<name>); match by basename
        pre_key = next(k for k in pre if Path(k).name == fname)
        if h != pre[pre_key]:
            raise ValueError(f"source changed across import: {name}")
        roots[name] = {"file": str(f), "sha256": h}
    if list((repo / "scripts").rglob("__pycache__")):
        raise ValueError("__pycache__ present in active source (refuse)")
    return roots


def _backup_owned(R6, repo: Path, rel: Path, ret_dir: Path, state_sha_hex: str, expect_pin: dict, allowed_root: Path) -> dict:
    if not HEX64_RE.fullmatch(state_sha_hex or ""):
        raise ValueError("backup requires live-verified 64-char State SHA")
    live = R6._pin_live(repo, rel, expect_pin, mode="0o664")
    dest = ret_dir / rel.name
    got = R6._stage_bytes_exclusive_under(dest, allowed_root, (repo / rel).read_bytes())
    if got["sha256"] != live["sha256"]:
        raise ValueError(f"backup SHA mismatch (preserve, STOP): {rel}")
    return {"old": rel.as_posix(), "new": dest.name, "sha256": got["sha256"],
            "bytes": got["bytes"], "mode": "0o664", "state_sha": state_sha_hex,
            "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}


def _verify_tree_phase(R6, repo: Path, exp_files: dict, exp_dirs: set, label: str) -> None:
    live_files, live_dirs, walk_errs = R6._walk_sp_tree_stdlib(repo, SRC_REL)
    if walk_errs:
        raise ValueError(f"{label}: W34 walk FAILED:\n- " + "\n- ".join(walk_errs[:10]))
    errs = R6._compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs)
    if errs:
        raise ValueError(f"{label}: tree mismatch (preserve, STOP):\n- " + "\n- ".join(errs[:10]))


def _gate_phase(R6, M, repo: Path, manifest: dict, manifest_path: Path, ready: dict, ready_path: Path,
                exp_manifest_sha: str, exp_ready_sha: str, exp_files: dict, exp_dirs: set, ret_dir: Path | None,
                label: str, expect_ledger: bool, expect_comp: bool) -> None:
    errs: list[str] = []
    try:
        if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
            errs.append(f"{label} manifest changed mid-run (refuse)")
        if hashlib.sha256(ready_path.read_bytes()).hexdigest() != exp_ready_sha:
            errs.append(f"{label} READY changed mid-run (refuse)")
    except OSError as e:
        errs.append(f"{label} pin re-read: {e}")
    try:
        _strict_w34_state_and_ready(R6, repo, M, manifest)
    except ValueError as e:
        errs.append(f"{label} state/readiness: {e}")
    try:
        live_files, live_dirs, walk_errs = R6._walk_sp_tree_stdlib(repo, SRC_REL)
        errs.extend(f"{label} walk: {e}" for e in walk_errs)
        if not walk_errs:
            errs.extend(f"{label} tree: {e}" for e in R6._compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs))
    except ValueError as e:
        errs.append(f"{label} walk exception: {e}")
    try:
        errs.extend(f"{label} intended: {e}" for e in R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    except ValueError as e:
        errs.append(f"{label} intended exception: {e}")
    try:
        if expect_ledger:
            R6._pin_live(repo, LEDGER_REL, manifest["original_authority"]["ledger"], mode="0o664")
        else:
            R6._require_absent(repo, LEDGER_REL)
        if expect_comp:
            R6._pin_live(repo, COMP_REL, manifest["original_authority"]["completeness"], mode="0o664")
        else:
            R6._require_absent(repo, COMP_REL)
    except ValueError as e:
        errs.append(f"{label} material pins: {e}")
    if ret_dir is not None:
        try:
            for key in ("ledger", "completeness"):
                expect = manifest["original_authority"][key]
                back = ret_dir / Path(expect["rel"]).name
                if os.path.islink(back) or not back.is_file():
                    errs.append(f"{label} retained backup missing/unsafe: {key}")
                    continue
                st = os.lstat(back)
                if (hashlib.sha256(back.read_bytes()).hexdigest() != expect["sha256"] or back.stat().st_size != expect["bytes"]
                        or oct(st.st_mode & 0o777) != "0o664" or st.st_nlink != 1):
                    errs.append(f"{label} retained backup drift (preserve, STOP): {expect['rel']}")
        except OSError as e:
            errs.append(f"{label} backup re-read: {e}")
    if errs:
        raise ValueError(f"{label} FAILED (preserve partials, STOP, no restore, no retry):\n- " + "\n- ".join(errs[:15]))


def _strict_w34_state_and_ready(R6, repo: Path, M: dict, manifest: dict):
    cfg = M["core"].load_json(repo / M["core"].DEFAULT_CONFIG)
    # B3: strict duplicate-key JSON for destructive gates (not json.loads)
    state = R6._strict_json(repo / (SRC_REL / "production-state.json"))
    if state.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("State drift: lifecycle must be CANDIDATES_NORMALIZED")
    mc = state.get("machine_checkpoints", {})
    if not (mc.get("evidence") == "pending" and mc.get("materiality") == "pending" and mc.get("completeness") == "pending"):
        raise ValueError("State drift: machine must be pending")
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


def stage_dispose_run(ret_dir: Path, ready_path: Path, manifest_path: Path, exp_ready_sha: str, exp_manifest_sha: str) -> dict:
    R6 = _load_r6()
    manifest = R6._verify_manifest_self(manifest_path, exp_manifest_sha)
    ready = _verify_ready_self(ready_path, exp_ready_sha)
    if ready.get("manifest", {}).get("sha256") != exp_manifest_sha:
        raise ValueError("READY does not bind the expected manifest (refuse)")
    repo = REPO_ROOT.resolve()
    errs: list[str] = []
    ctx: dict = {}
    try:
        umask_val, umask_file_mode = _read_umask()
        ctx["umask"] = oct(umask_val)
        ctx["umask_file_mode"] = umask_file_mode
        pre = {}
        for rel in ("scripts/survey_evidence_v2.py", "scripts/run_evidence_v2_interactive.py",
                    "scripts/survey_research_authority_v2.py", "scripts/survey_agent_tool_v2.py",
                    "scripts/survey_agent_control_v2.py", "scripts/survey_production_v2.py",
                    "scripts/survey_screening_v2.py", "scripts/survey_discovery_v2.py",
                    "scripts/survey_completeness_v2.py", "scripts/survey_schema_v2.py"):
            pin = R6._pin_live(repo, Path(rel), manifest["original_authority"][f"module_{Path(rel).name}"])
            pre[rel] = pin["sha256"]
        errs.extend(R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    except ValueError as e:
        raise ValueError(f"phase0 source precheck: {e}") from e
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
    # B2: after-import re-hash (pre-import pins already in `pre`) + no pycache
    _mod_files = ((ev, "survey_evidence_v2.py"), (rn, "run_evidence_v2_interactive.py"), (low, "survey_research_authority_v2.py"),
                  (at, "survey_agent_tool_v2.py"), (agent, "survey_agent_control_v2.py"), (core, "survey_production_v2.py"),
                  (sc, "survey_screening_v2.py"), (disc, "survey_discovery_v2.py"), (comp, "survey_completeness_v2.py"))
    _roots: dict = {}
    for _mod, _fname in _mod_files:
        _f = Path(_mod.__file__)
        if repo.resolve() not in _f.resolve().parents:
            raise ValueError(f"module root outside e84: {_fname}")
        _h = hashlib.sha256(_f.read_bytes()).hexdigest()
        _pre_key = next(k for k in pre if Path(k).name == _fname)
        if _h != pre[_pre_key]:
            raise ValueError(f"source changed across import: {_fname}")
        _roots[_fname] = {"file": str(_f), "sha256": _h}
    if list((repo / "scripts").rglob("__pycache__")):
        raise ValueError("__pycache__ present in active source (refuse)")
    M = {"ev": ev, "rn": rn, "low": low, "at": at, "agent": agent, "core": core, "sc": sc, "disc": disc, "comp": comp}
    M["roots"] = _roots
    # READY exact keys required (no invented defaults)
    for _rk in ("live_implementation_sha", "new_input", "retained_pkg_dir", "package_json_sha"):
        if _rk not in ready:
            raise ValueError(f"READY lacks required key {_rk} (refuse invented defaults)")
    if not isinstance(ready["new_input"], dict) or not all(k in ready["new_input"] for k in ("rel", "sha256", "bytes")):
        raise ValueError("READY new_input lacks rel/sha256/bytes (refuse)")
    try:
        live_impl = core.repository_commit_sha(repo)
        if not HEX40_RE.fullmatch(live_impl or ""):
            errs.append(f"live impl SHA not 40-hex: {live_impl!r}")
        ctx["live_implementation_sha"] = live_impl
        if live_impl != ready["live_implementation_sha"]:
            errs.append(f"live HEAD drift vs READY live impl: {live_impl} != {ready['live_implementation_sha']}")
        if live_impl != manifest["active_instance"]["recorded_head"]:
            errs.append("live HEAD drift vs recorded e84 head (refuse)")
        cfg, state, state_path, profile_path = _strict_w34_state_and_ready(R6, repo, M, manifest)
        ctx["state_path"] = state_path
        # full tree == baseline 1781 + staged 1 (1782)
        new_rels = [ready["new_input"]["rel"]]
        if len(new_rels) != 1:
            errs.append("READY new set != 1 (W34 has no new Raw/supplement)")
        exp_files_1782 = {e["rel"]: e for e in manifest["w34_tree_full"]["files"]}
        exp_files_1782[ready["new_input"]["rel"]] = {"sha256": ready["new_input"]["sha256"], "bytes": ready["new_input"]["bytes"], "mode": "0o664", "nlink": 1}
        exp_dirs = {e["rel"] for e in manifest["w34_tree_full"]["dirs"]}
        ctx["exp_files_1782"], ctx["exp_dirs"] = exp_files_1782, exp_dirs
        _verify_tree_phase(R6, repo, exp_files_1782, exp_dirs, "pre-disposal")
        erv = R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"])
        errs.extend(f"pre-disposal intended: {e}" for e in erv)
        r2_raw = R2_INPUT.read_bytes()
        if hashlib.sha256(r2_raw).hexdigest() != manifest["corrected"]["input"]["sha256"]:
            errs.append("r2 input bytes drift vs manifest")
        try:
            r2 = json.loads(r2_raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as e:
            errs.append(f"r2 input JSON invalid: {e}")
            r2 = {}
        if r2 and (r2.get("issue_id") != ISSUE or r2.get("schema_version") != "2.0-rc1"):
            errs.append("r2 input identity mismatch")
        if r2 and ("records" not in r2 or "completeness" not in r2 or "obligations" not in r2["completeness"]):
            errs.append("r2 input missing records/completeness/obligations (refuse invented defaults)")
        elif r2:
            if len(r2["records"]) != 409 or len(r2["completeness"]["obligations"]) != 3:
                errs.append("r2 input counts != 409/3")
        ctx["new_input_rel"] = ready["new_input"]["rel"]
        try:
            R6._pin_live(repo, Path(ctx["new_input_rel"]), {"sha256": ready["new_input"]["sha256"], "bytes": ready["new_input"]["bytes"]}, mode="0o664")
        except ValueError as e:
            errs.append(f"staged NEW drift: {e}")
        with at.current_stage_basis_override():
            accepted_discovery = disc.validate_acceptance(repo, (repo / SRC_REL) / "discovery/discovery-accepted-v2.json")
            root_path = core.repo_local_path(repo, accepted_discovery["discovery_path"], "accepted Discovery JSONL")
            active = sc.resolve_active_screening_acceptance(repo, state_path, live_impl)
            _sp = Path(active["path"])
            screening_path = _sp if _sp.is_absolute() else (repo / _sp)
            effective = sc.resolve_effective_discovery_basis(repo, screening_path.parent / "package.json", live_impl, accepted_root_path=root_path)
        # DERIVED R/E authority (not token presence): validated lists, no defaults
        if "root_records" not in effective or "records" not in effective or "path" not in effective:
            errs.append("effective basis missing root_records/records/path (refuse invented defaults)")
            root_recs, disc_recs = [], []
        else:
            root_recs, disc_recs = effective["root_records"], effective["records"]
            if len(root_recs) != 369:
                errs.append(f"effective root_records != 369 (got {len(root_recs)})")
            if len(disc_recs) != 439:
                errs.append(f"effective records != 439 (got {len(disc_recs)})")
        ctx["screening_acc_path"] = screening_path if screening_path.is_absolute() else (repo / screening_path)
        ctx["effective_path"] = Path(effective["path"]) if Path(effective["path"]).is_absolute() else (repo / effective["path"])
        ctx["disc_recs"], ctx["root_recs"] = disc_recs, root_recs
        # FULL normal supplement validation BEFORE destructive ops (existing API, facade)
        with at.current_stage_basis_override():
            _real_acc, _, _real_disc = ev.validate_screening_acceptance(repo, ctx["screening_acc_path"], ctx["effective_path"], ISSUE, live_impl)
            ev.validate_evidence_authority_supplement(repo, repo / Path(manifest["original_authority"]["supplement_r2"]["rel"]), live_impl,
                expected_issue_id=ISSUE, expected_source_root=(repo / SRC_REL).resolve(),
                expected_discovery_path=ctx["effective_path"], expected_screening_acceptance_path=ctx["screening_acc_path"],
                screening_acceptance=_real_acc, discoveries=_real_disc)
            ctx["real_acc"], ctx["real_disc"] = _real_acc, _real_disc
        # retained 409-task package at READY exact path (no glob guess)
        prep_ret = ready_path.parent
        if "retained_pkg_dir" not in ready or "package_json_sha" not in ready:
            errs.append("READY lacks retained_pkg_dir/package_json_sha (refuse invented defaults)")
        else:
            ctx["pkg_path"] = prep_ret / ready["retained_pkg_dir"] / "package.json"
            if not ctx["pkg_path"].is_file() or os.path.islink(ctx["pkg_path"]):
                errs.append(f"retained package missing/unsafe at READY exact path: {ctx['pkg_path']}")
            else:
                ctx["package"] = json.loads(ctx["pkg_path"].read_bytes().decode("utf-8"))
                if hashlib.sha256(ctx["pkg_path"].read_bytes()).hexdigest() != ready["package_json_sha"]:
                    errs.append("retained package.json drift vs READY (refuse)")
                else:
                    with at.current_stage_basis_override():
                        ev.validate_evidence_package_basis(repo, ctx["pkg_path"], ctx["package"], live_impl)
        if "package" not in ctx or "tasks" not in ctx["package"]:
            errs.append("retained package missing tasks (refuse invented defaults)")
        elif len(ctx["package"]["tasks"]) != 409:
            errs.append("retained package tasks != 409")
        # checkpoints/accepted/preserved pins (no false absent labels; tree + State cover gates)
        for name in ("DISCOVERY_COLLECTED", "ISSUE_INITIALIZED"):
            try:
                R6._pin_live(repo, SRC_REL / "orchestration/v2/checkpoints" / f"{name}.json",
                             manifest["original_authority"][f"checkpoint_{name}"])
            except ValueError as e:
                errs.append(f"checkpoint {name}: {e}")
        for key, pin in manifest["original_authority"].items():
            if key.startswith("accepted_") and isinstance(pin, dict) and "rel" in pin:
                try:
                    R6._pin_live(repo, Path(pin["rel"]), pin)
                except ValueError as e:
                    errs.append(f"authority {key}: {e}")
        for key in ("state", "profile", "ledger", "completeness", "supplement_r2", "config"):
            try:
                R6._pin_live(repo, Path(manifest["original_authority"][key]["rel"]), manifest["original_authority"][key])
            except ValueError as e:
                errs.append(f"preserved {key}: {e}")
        # B1: known old accepted dirs from FROZEN tree + accepted file pins (no invented defaults)
        try:
            old_ev_dirs, old_view_dirs = _derive_old_accepted_dirs(manifest)
            ctx["old_ev_dirs"], ctx["old_view_dirs"] = old_ev_dirs, old_view_dirs
        except ValueError as e:
            errs.append(f"old accepted dirs: {e}")
        # SP completed NEW products snapshot (no SP invoke): both retentions still present
        for sp_ready, sp_sha in (("retention-SP-20261104T162747Z/READY.json", "c7cd05a888106b2cdf0f4e984fb22412678a8ff792deda1ad7ff94e3b31e7643"),
                                 ("retention-SP-dispose-20261105T000554Z/DISPOSE_RUN.json", "cf26a23c06a01058a432ccfa7677a7931a2457e77edcc2094e77ffd8d7434ecf")):
            p = RESUME / sp_ready
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != sp_sha:
                errs.append(f"SP completed product drift/missing (preserve, STOP): {sp_ready}")
        ctx["supplement_abs"] = repo / Path(manifest["original_authority"]["supplement_r2"]["rel"])
        ctx["staged_input_abs"] = repo / Path(ctx["new_input_rel"])
    except ValueError as e:
        errs.append(f"phase1 exception: {e}")
    if errs:
        raise ValueError("pre-disposal verification FAILED (zero active writes performed):\n- " + "\n- ".join(errs[:25]))
    # ---- P2 NEW retention + backups ----
    try:
        ret_dir = _check_retention_root(ret_dir, RESUME)
        R6._require_absent_under(RESUME.resolve(), ret_dir)
        ret_dir.parent.mkdir(parents=True, exist_ok=True)
    except (ValueError, OSError) as e:
        raise ValueError(f"retention path refused: {e}") from e
    try:
        ret_dir.mkdir(exist_ok=False)
    except FileExistsError:
        raise ValueError(f"single-use refuse: retention exists: {ret_dir}")
    try:
        state_sha_live = hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest()
        if state_sha_live != manifest["original_authority"]["state"]["sha256"]:
            raise ValueError("State drift at backup time (STOP, preserve)")
    except OSError as e:
        raise ValueError(f"State re-read failed: {e}") from e
    journal: list[dict] = [{"step": "phase1", "result": "pass", "live_impl": ctx["live_implementation_sha"], "umask": ctx["umask"]}]
    man = {"ledger": _backup_owned(R6, repo, LEDGER_REL, ret_dir, state_sha_live, manifest["original_authority"]["ledger"], RESUME.resolve()),
           "completeness": _backup_owned(R6, repo, COMP_REL, ret_dir, state_sha_live, manifest["original_authority"]["completeness"], RESUME.resolve())}
    man["context"] = {"issue": ISSUE, "retained_from_ready": ready_path.name, "ready_sha256": exp_ready_sha,
                      "manifest_sha256": exp_manifest_sha,
                      "state_sha256": state_sha_live, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                      "note": "immutable linkage old->new; O_EXCL-created, chmod 0o664, readback-verified; no rename onto backup names; no automatic restore"}
    journal.append({"step": "backup-2", "ledger": man["ledger"]["sha256"], "completeness": man["completeness"]["sha256"]})
    R6._stage_bytes_exclusive_under(ret_dir / "retention-manifest.json", RESUME.resolve(),
                                    (json.dumps(man, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    # ---- P3 ledger gate -> unlink ONLY ----
    _gate_phase(R6, {"core": core, "agent": agent, "low": low}, repo, manifest, manifest_path, ready, ready_path,
                exp_manifest_sha, exp_ready_sha, ctx["exp_files_1782"], ctx["exp_dirs"], ret_dir, "gate-ledger", True, True)
    R6._pin_live(repo, LEDGER_REL, manifest["original_authority"]["ledger"], mode="0o664")
    R6._pin_live(repo, COMP_REL, manifest["original_authority"]["completeness"], mode="0o664")
    _strict_w34_state_and_ready(R6, repo, {"core": core, "agent": agent, "low": low}, manifest)
    os.unlink(repo / LEDGER_REL)
    R6._require_absent(repo, LEDGER_REL)
    if hashlib.sha256((ret_dir / "materiality-ledger-v2.json").read_bytes()).hexdigest() != manifest["original_authority"]["ledger"]["sha256"]:
        raise ValueError("retention Ledger drift after unlink (preserve partials, STOP, no restore)")
    journal.append({"step": "unlink-ledger", "result": "absent-verified"})
    # ---- P4 completeness gate -> unlink ONLY ----
    exp_files_1781 = dict(ctx["exp_files_1782"])
    del exp_files_1781[LEDGER_REL.as_posix()]
    _gate_phase(R6, {"core": core, "agent": agent, "low": low}, repo, manifest, manifest_path, ready, ready_path,
                exp_manifest_sha, exp_ready_sha, exp_files_1781, ctx["exp_dirs"], ret_dir, "gate-completeness", False, True)
    R6._pin_live(repo, COMP_REL, manifest["original_authority"]["completeness"], mode="0o664")
    _strict_w34_state_and_ready(R6, repo, {"core": core, "agent": agent, "low": low}, manifest)
    os.unlink(repo / COMP_REL)
    R6._require_absent(repo, COMP_REL)
    R6._require_absent(repo, LEDGER_REL)
    if hashlib.sha256((ret_dir / "profile-completeness-v2.json").read_bytes()).hexdigest() != manifest["original_authority"]["completeness"]["sha256"]:
        raise ValueError("retention Completeness drift after unlink (preserve partials, STOP, no restore)")
    journal.append({"step": "unlink-completeness", "result": "both-absent-verified"})
    # ---- P5 post-disposal: 1780 set, accepted unchanged, State CAND ----
    exp_files_1780 = dict(exp_files_1781)
    del exp_files_1780[COMP_REL.as_posix()]
    _verify_tree_phase(R6, repo, exp_files_1780, ctx["exp_dirs"], "post-disposal")
    for key, pin in manifest["original_authority"].items():
        if key.startswith("accepted_") and isinstance(pin, dict) and "rel" in pin:
            R6._pin_live(repo, Path(pin["rel"]), pin)
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        raise ValueError("State bytes changed during disposal (STOP, preserve)")
    _strict_w34_state_and_ready(R6, repo, {"core": core, "agent": agent, "low": low}, manifest)
    journal.append({"step": "post-disposal-verify", "result": "pass"})
    # ---- P6 ONE ordinary retry (existing public API owns facade) ----
    result = rn.run(repo, state_path, ctx["staged_input_abs"], ctx["supplement_abs"])
    journal.append({"step": "run", "result": result})
    if result.get("evidence_result_count") != 409:
        raise ValueError(f"run result count != 409 (preserve, STOP): {result.get('evidence_result_count')}")
    # ---- P7 post-run: CAND + layout + EFFECTIVE 439 validators/counts ----
    st_after = R6._strict_json(repo / (SRC_REL / "production-state.json"))
    if st_after.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("State advanced by run (refuse; expected still CAND)")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        raise ValueError("State bytes changed by run (STOP, preserve)")
    baseline_files = {e["rel"]: e for e in manifest["w34_tree_full"]["files"]}
    baseline_files[ready["new_input"]["rel"]] = {"sha256": ready["new_input"]["sha256"], "bytes": ready["new_input"]["bytes"], "mode": "0o664"}
    baseline_dirs = {e["rel"] for e in manifest["w34_tree_full"]["dirs"]}
    if "umask_file_mode" not in ctx:
        raise ValueError("missing recorded umask_file_mode (refuse invented default)")
    umask_file_mode = ctx["umask_file_mode"]
    bindings = _check_post_run_layout(repo, SRC_REL, baseline_files, baseline_dirs,
                                      [{"rel": ready["new_input"]["rel"], "sha256": ready["new_input"]["sha256"], "bytes": ready["new_input"]["bytes"]}],
                                      LEDGER_REL.as_posix(), COMP_REL.as_posix(),
                                      ctx["old_ev_dirs"],
                                      ctx["old_view_dirs"],
                                      409, ready["new_input"]["rel"], ready["new_input"]["sha256"],
                                      manifest["original_authority"]["supplement_r2"]["rel"], manifest["original_authority"]["supplement_r2"]["sha256"],
                                      439, 3, "LIMITED", umask_file_mode)
    with at.current_stage_basis_override():
        ev_acc_path = repo / bindings["ev_acceptance"]
        view_acc_path = repo / bindings["views_acceptance"]
        ev.validate_evidence_acceptance(repo, ev_acc_path, ctx["live_implementation_sha"])
        ev.validate_edition_views_acceptance(repo, repo / (SRC_REL / "production-profile.json"), ev_acc_path, view_acc_path, ctx["live_implementation_sha"])
        # EFFECTIVE 439 path (not SP root 369) for Ledger/Completeness
        ledger_doc = json.loads((repo / bindings["ledger"]).read_bytes().decode("utf-8"))
        ev.validate_materiality_ledger(ledger_doc, repo, repo / (SRC_REL / "production-profile.json"),
            ctx["effective_path"], ctx["screening_acc_path"], ev_acc_path, view_acc_path, ctx["live_implementation_sha"])
        comp_doc = json.loads((repo / bindings["completeness"]).read_bytes().decode("utf-8"))
        comp_errs = comp.validate_profile_completeness(comp_doc, repo, repo / (SRC_REL / "production-profile.json"),
            ctx["effective_path"], ctx["screening_acc_path"], ev_acc_path, view_acc_path, repo / bindings["ledger"], ctx["live_implementation_sha"])
        if comp_errs:
            raise ValueError("produced Completeness invalid: " + "; ".join(comp_errs))
    journal.append({"step": "post-run-verify", "result": "pass", "bindings": bindings})
    # ---- P8 return gate (same captured pins, not reseal) + record ----
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
        raise ValueError("manifest changed during run (refuse record)")
    if hashlib.sha256(ready_path.read_bytes()).hexdigest() != exp_ready_sha:
        raise ValueError("READY changed during run (refuse record)")
    ret_in = R6._pin_live(repo, Path(ctx["new_input_rel"]) if "new_input_rel" in ctx else Path(ready["new_input"]["rel"]), {"sha256": ready["new_input"]["sha256"], "bytes": ready["new_input"]["bytes"]}, mode="0o664")
    for _rel_key, _sha_key in (("ledger", "ledger_sha"), ("completeness", "completeness_sha")):
        _cur = (repo / bindings[_rel_key]).read_bytes()
        if hashlib.sha256(_cur).hexdigest() != bindings[_sha_key]:
            raise ValueError(f"{_rel_key} bytes changed since post-run validation (refuse record)")
    ret_errs = R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"])
    if ret_errs:
        raise ValueError("return-gate intended FAILED:\n- " + "\n- ".join(ret_errs[:10]))
    ready_out = {"ready": False, "stage": "dispose-run-complete", "no_removal_beyond_exact2": True,
                 "manifest": {"path": manifest_path.name, "sha256": exp_manifest_sha},
                 "ready_in": {"path": ready_path.name, "sha256": exp_ready_sha},
                 "live_implementation_sha": ctx["live_implementation_sha"], "historical_implementation_sha": HIST_IMPL,
                 "new_input": ready["new_input"], "supplement_reused": manifest["original_authority"]["supplement_r2"],
                 "task_count": result.get("evidence_result_count"), "completeness_status": result.get("completeness_status"),
                 "bindings": bindings, "journal": journal}
    rp = ret_dir / "DISPOSE_RUN.json"
    R6._stage_bytes_exclusive_under(rp, RESUME.resolve(), (json.dumps(ready_out, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    R6._stage_bytes_exclusive_under(ret_dir / "journal.json", RESUME.resolve(), (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"result": str(rp), "tasks": result.get("evidence_result_count"), "completeness": result.get("completeness_status")}


def _check_post_run_layout(repo: Path, src_rel: Path, baseline_files: dict, baseline_dirs: set, staged_new: list,
                           old_ledger_rel: str, old_comp_rel: str, old_ev_dirs: list, old_view_dirs: list,
                           exp_results_n: int, staged_input_rel: str, staged_input_sha: str,
                           staged_supp_rel: str, staged_supp_sha: str,
                           exp_disc_n: int, exp_oblig_n: int, input_closure_status: str,
                           umask_file_mode: int) -> dict:
    um = oct(umask_file_mode)
    files: dict[str, dict] = {}
    dirs: set[str] = set()
    errs: list[str] = []
    for p in sorted((repo / src_rel).rglob("*")):
        rel = p.relative_to(repo).as_posix()
        if p.is_symlink():
            errs.append(f"symlink in W34 tree: {rel}")
            continue
        if p.is_dir():
            dirs.add(rel)
        elif p.is_file():
            st = os.lstat(p)
            if not stat.S_ISREG(st.st_mode):
                errs.append(f"special entry: {rel}")
                continue
            data = p.read_bytes()
            files[rel] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                          "mode": oct(st.st_mode & 0o777), "nlink": st.st_nlink}
        else:
            errs.append(f"special entry: {rel}")
    if errs:
        raise ValueError("post-run walk FAILED:\n- " + "\n- ".join(errs[:10]))
    ev_root = f"{src_rel}/evidence/v2/accepted"
    view_root = f"{src_rel}/evidence/v2/views/accepted"
    old_ev = {f"{ev_root}/{d}" for d in old_ev_dirs}
    old_view = {f"{view_root}/{d}" for d in old_view_dirs}
    new_ev = sorted(d for d in dirs if d.startswith(ev_root + "/") and d.count("/") == len(ev_root.split("/")) and d not in old_ev and d != ev_root)
    new_view = sorted(d for d in dirs if d.startswith(view_root + "/") and d.count("/") == len(view_root.split("/")) and d not in old_view and d != view_root)
    if len(new_ev) != 1 or len(new_view) != 1:
        raise ValueError(f"expected exactly 1 NEW accepted dir per root, got ev={new_ev} views={new_view}")
    new_ev_rel, new_view_rel = new_ev[0], new_view[0]
    exp_new_files = {f"{new_ev_rel}/evidence-accepted.json", f"{new_ev_rel}/package.json",
                     f"{new_ev_rel}/interactive-evidence.json", f"{new_ev_rel}/interactive-audit.json",
                     f"{new_view_rel}/edition-views-accepted.json"}
    copy_files = sorted(r for r in files if r.startswith(new_ev_rel + "/tasks/") or r.startswith(new_ev_rel + "/results/"))
    view_files = sorted(r for r in files if r.startswith(new_view_rel + "/views/"))
    task_files = sorted(r for r in copy_files if "/tasks/" in r)
    result_files = sorted(r for r in copy_files if "/results/" in r)
    if len(task_files) != exp_results_n or len(result_files) != exp_results_n or len(view_files) != exp_results_n:
        errs.append(f"produced copy counts != {exp_results_n}: tasks={len(task_files)} results={len(result_files)} views={len(view_files)}")
    top_new = {r for r in files if r in exp_new_files}
    if top_new != exp_new_files:
        errs.append(f"new accepted top files mismatch: missing={sorted(exp_new_files-top_new)[:5]}")
    for e in staged_new:
        got = files.get(e["rel"])
        if got is None or got["sha256"] != e["sha256"] or got["bytes"] != e["bytes"]:
            errs.append(f"staged file drift after run: {e['rel']}")
        elif got["mode"] != "0o664" or got.get("nlink", 1) != 1:
            errs.append(f"staged file identity drift after run: {e['rel']}")
    for rel, exp in baseline_files.items():
        if rel in (old_ledger_rel, old_comp_rel):
            continue
        got = files.get(rel)
        if got is None:
            errs.append(f"old file missing after run: {rel}")
        elif got["sha256"] != exp["sha256"] or got["bytes"] != exp["bytes"] or got["mode"] != exp["mode"]:
            errs.append(f"old file changed by run (must be byte-identical): {rel}")
    for rel in (old_ledger_rel, old_comp_rel):
        got = files.get(rel)
        exp_old = baseline_files.get(rel)
        if got is None or exp_old is None:
            errs.append(f"exact2 path missing: {rel}")
        elif got["sha256"] == exp_old["sha256"]:
            errs.append(f"exact2 NOT regenerated (still old bytes): {rel}")
        elif got["mode"] != um or got.get("nlink", 1) != 1:
            errs.append(f"exact2 identity drift (expected recorded umask mode {um}/nlink 1): {rel} got {got['mode']}/nlink {got.get('nlink')}")
    for r in sorted(exp_new_files):
        got = files.get(r)
        if got is None:
            continue
        want = "0o664" if r.endswith("/interactive-evidence.json") else um
        if got["mode"] != want or got.get("nlink", 1) != 1:
            errs.append(f"new output mode drift (expected {want}): {r} got {got['mode']}")
    for r in task_files + result_files + view_files:
        got = files[r]
        if got["mode"] != um or got.get("nlink", 1) != 1:
            errs.append(f"new copy mode drift (expected umask {um}): {r} got {got['mode']}")
    unexpected = set(files) - set(baseline_files) - {e["rel"] for e in staged_new} - exp_new_files - set(task_files) - set(result_files) - set(view_files)
    # staged input already in baseline (1781+1); exclude it from unexpected (it is in staged_new AND baseline)
    unexpected = {u for u in unexpected if u not in {e["rel"] for e in staged_new}}
    if unexpected:
        errs.append(f"unexpected active writes by run: {sorted(unexpected)[:8]}")
    exp_dirs = set(baseline_dirs) | {new_ev_rel, f"{new_ev_rel}/tasks", f"{new_ev_rel}/results", new_view_rel, f"{new_view_rel}/views"}
    if errs:
        raise ValueError("post-run layout FAILED (preserve, STOP):\n- " + "\n- ".join(errs[:12]))
    if dirs != exp_dirs:
        raise ValueError(f"post-run dir set drift: missing={sorted(exp_dirs-dirs)[:5]} extra={sorted(dirs-exp_dirs)[:5]}")
    ev_acc = json.loads((repo / f"{new_ev_rel}/evidence-accepted.json").read_bytes().decode("utf-8"))
    if ev_acc.get("result_count") != exp_results_n or len(ev_acc.get("results", [])) != exp_results_n:
        raise ValueError(f"evidence results != {exp_results_n}")
    pkg = json.loads((repo / f"{new_ev_rel}/package.json").read_bytes().decode("utf-8"))
    auth = pkg.get("authority_supplement") or {}
    if auth.get("path") != staged_supp_rel or auth.get("sha256") != staged_supp_sha:
        raise ValueError("package supplement reference != existing supplement (refuse)")
    audit = json.loads((repo / f"{new_ev_rel}/interactive-audit.json").read_bytes().decode("utf-8"))
    inp = audit.get("interactive_input") or {}
    if inp.get("path") != f"{new_ev_rel}/interactive-evidence.json" or inp.get("sha256") != staged_input_sha:
        raise ValueError("audit input reference != NEW accepted archive path + staged bytes (refuse)")
    arch = (repo / f"{new_ev_rel}/interactive-evidence.json").read_bytes()
    if hashlib.sha256(arch).hexdigest() != staged_input_sha:
        raise ValueError("archived input bytes differ from staged input (refuse)")
    view_acc = json.loads((repo / f"{new_view_rel}/edition-views-accepted.json").read_bytes().decode("utf-8"))
    if len(view_acc.get("views", [])) != exp_results_n:
        raise ValueError(f"views != {exp_results_n}")
    if view_acc.get("view_set_sha256") != new_view_rel.rsplit("/", 1)[-1]:
        raise ValueError("views set != new dir name")
    res_by_task = {r["evidence_task_id"]: r for r in ev_acc["results"]}
    for v in view_acc["views"]:
        r = res_by_task.get(v.get("evidence_task_id"))
        if r is None or v.get("evidence_sha256") != r.get("sha256"):
            raise ValueError(f"view/card binding broken: {v.get('evidence_task_id')}")
    ledger_raw = (repo / old_ledger_rel).read_bytes()
    comp_raw = (repo / old_comp_rel).read_bytes()
    ledger = json.loads(ledger_raw.decode("utf-8"))
    if len(ledger.get("rows", [])) != exp_disc_n:
        raise ValueError(f"ledger rows {len(ledger.get('rows', []))} != effective {exp_disc_n}")
    comp = json.loads(comp_raw.decode("utf-8"))
    if len(comp.get("obligations", [])) != exp_oblig_n:
        raise ValueError(f"completeness obligations {len(comp.get('obligations', []))} != {exp_oblig_n}")
    if comp.get("overall_status") != input_closure_status:
        raise ValueError(f"completeness status {comp.get('overall_status')!r} != {input_closure_status!r}")
    return {"new_ev_dir": new_ev_rel, "new_view_dir": new_view_rel,
            "ev_acceptance": f"{new_ev_rel}/evidence-accepted.json", "views_acceptance": f"{new_view_rel}/edition-views-accepted.json",
            "ledger": old_ledger_rel, "completeness": old_comp_rel,
            "ledger_sha": hashlib.sha256(ledger_raw).hexdigest(), "ledger_bytes": len(ledger_raw),
            "completeness_sha": hashlib.sha256(comp_raw).hexdigest(), "completeness_bytes": len(comp_raw),
            "task_files": len(task_files), "result_files": len(result_files), "view_files": len(view_files),
            "ledger_rows": len(ledger.get("rows", [])), "ev_results": len(ev_acc["results"]), "ev_views": len(view_acc["views"]),
            "comp_obligations": len(comp.get("obligations", [])), "comp_status": comp.get("overall_status")}


def main() -> int:
    global REPO_ROOT
    ap = argparse.ArgumentParser(description="W34 dispose + normal-run one-use wrapper (review only, do not run yet)")
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--ready-path", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=RESUME / "w34-prepare-expected-manifest-20261104.json")
    ap.add_argument("--expected-tool-sha", type=str, required=True)
    ap.add_argument("--expected-ready-sha", type=str, required=True)
    ap.add_argument("--expected-manifest-sha", type=str, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    a = ap.parse_args()
    REPO_ROOT = a.repo_root
    try:
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != a.expected_tool_sha:
            raise ValueError("wrapper bytes drift vs externally recorded tool hash (refuse)")
        out = stage_dispose_run(a.retention_dir, a.ready_path, a.manifest, a.expected_ready_sha, a.expected_manifest_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            rd = a.retention_dir
            if rd.is_dir() and not os.path.islink(rd):
                partials = sorted(p.relative_to(rd).as_posix() for p in rd.rglob("*") if p.is_file())
                R6b = _load_r6()
                R6b._stage_bytes_exclusive_under(rd / "FAILURE.json", RESUME.resolve(),
                    (json.dumps({"stage": "dispose-run", "exit": 2, "error": str(exc)[:4000], "retained_partials": partials}, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        except OSError:
            pass
        print(f"DISPOSE_RUN_REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"stage": "dispose-run", "exit": 0, **out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
