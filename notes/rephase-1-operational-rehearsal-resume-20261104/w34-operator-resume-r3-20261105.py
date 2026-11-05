#!/usr/bin/env python3
"""W34 resume-only one-use wrapper r3 — SOURCE REVIEW ONLY, DO NOT EXECUTE.

r3 preserves r2 (`w34-operator-resume-r2-20261105.py`) untouched and fixes the
blocked full post branch (no execution yet):

- Bare-name NameErrors: r2 full branch calls undefined `_derive_old_accepted_dirs`
  / `LEDGER_REL` / `COMP_REL`. r3 defines LEDGER_REL/COMP_REL + a resume-aware
  `_derive_old_accepted_dirs_resume` (ORIGINAL pinned w34-prepare manifest
  `cede7e46...` accepted pins, cross-checked with local current-tree helper;
  no faked authority dict / missing defaults).
- Resume-manifest adaptation: D3 `_derive_old_accepted_dirs` requires
  `w34_tree_full`; resume manifest carries `w34_tree_current`. r3 never calls
  it; derivation above is used instead.
- Post-layout adaptation: D3 `_check_post_run_layout` expects BOTH old
  canonical entries in baseline for regen compare (resume 1780 baseline
  excludes them -> `exp_old None`). r3 supplies explicit observation-only
  expected old2 (PINNED backups + old manifest, no claim originals exist)
  plus current baseline 1780+new input; the adapted check excludes old2 from
  the preserved loop and verifies actual new outputs.
- Terminal post pins AFTER final validators (not only before run):
  source771 + State + whole current baseline inputs/supp + manifest SAME hash
  + new Ledger/Completeness expected post pins.
- Guard backups-both/source/input/supp/manifest SAME hash before READY and
  before full run. Umask correct (single read/restore, as r2); journals stay
  distinct (`preflight-journal.json` vs `journal.json`).

CONTINUE ABSENT: exact2 stay absent, backups preserved, no restore/removal.

- Pre-import fail-closed (r1 collected intended drift into errs then
  imported); r2 raises BEFORE any project import.
- After-import 10-module match (`rn.schema_gate` 10th) + no `__pycache__`.
- Single umask read/restore (r1 double-`os.umask(0)` left mask 0 and wrong
  mode); r2 records exact `0o666 & ~prev`.
- Supplement 428 rows derived from validated supp FILE `ce6f...` (verify
  file hash first, then exact manifest Raw pins); no empty-default skip.
- No fictitious view validation: preflight retains actual canonical card
  bytes (`core.json_bytes`) outside active + honest card-only claim (views
  proven only in full branch via real acceptance path).
- Full shared guards (baseline+new/source771/State/absent2/backups/supp/
  input/self-manifest SAME hash) run BEFORE READY even with --prepare-only;
  READY manifest field binds externally recorded hash (no fresh-read reseal).
- Distinct journals: `preflight-journal.json` (preflight) vs `journal.json`
  (final); second O_EXCL write can no longer collide.
- Full branch reuses proven W34 dispo-r3 post-layout/actual validators via
  explicit pin `48be5879...` (stdlib-only import verified; its disposal never
  executed), with current+old2 inventory, exact old accepted sets,
  EFFECTIVE 439 paths, card/archive/umask bindings.
- Failure logger absolutizes packet path before best-effort write without
  masking the original error; launcher always captures stdout/stderr/exit.

CONTINUE ABSENT: exact2 stay absent, backups preserved, no restore/removal.
Only NEW r3 input staged, then nonpublishing SAME canonical card-core
preflight (ALL 409) + Raw closure, then ONE normal run only after Root auth.
--prepare-only stops at READY (retained cards + journal); without it, same
invocation continues full guard+run. No remove code (no os.unlink). No SP
mutation (stable anchors only).
"""
from __future__ import annotations
import argparse
import datetime
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
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
PACKET = RESUME
SRC_REL = Path("sources/2026-W34")
ISSUE = "2026-W34"
HIST_IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
R6_TOOL = RESUME / "sp-operator-prepare-r6-20261104.py"
R6_TOOL_SHA = "2c6f1aebfae91d95ed1f10e2cae6db6e8665e653d3ec5ecd881e988cab56d664"
DISPO_R3_TOOL = RESUME / "w34-operator-dispose-run-r3-20261104.py"
DISPO_R3_TOOL_SHA = "48be58796e7ee2ef31ce0873e3223d7c0f78fb6de08aed3012f06b593f2846b8"
ORIG_PREP_MANIFEST = RESUME / "w34-prepare-expected-manifest-20261104.json"
ORIG_PREP_MANIFEST_SHA = "cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590"
LEDGER_REL = SRC_REL / "materiality-ledger-v2.json"
COMP_REL = SRC_REL / "profile-completeness-v2.json"
BACKUP_RETENTION = RESUME / "retention-W34-dispose-20261105T003915Z"
R3_INPUT = RESUME / "w34-corrected-input-r3-20261104.json"
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}")
HEX64_RE = re.compile(r"[0-9a-f]{64}")
HEX40_RE = re.compile(r"[0-9a-f]{40}")
IMPORT_BOUND = ("scripts/survey_evidence_v2.py", "scripts/run_evidence_v2_interactive.py",
                "scripts/survey_research_authority_v2.py", "scripts/survey_agent_tool_v2.py",
                "scripts/survey_agent_control_v2.py", "scripts/survey_production_v2.py",
                "scripts/survey_screening_v2.py", "scripts/survey_discovery_v2.py",
                "scripts/survey_completeness_v2.py", "scripts/survey_schema_v2.py")


def _load_r6():
    data = R6_TOOL.read_bytes()
    if hashlib.sha256(data).hexdigest() != R6_TOOL_SHA:
        raise ValueError("r6 helper drift vs pinned 2c6f1aeb... (refuse)")
    spec = importlib.util.spec_from_file_location("r6helpers", R6_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R6 = _load_r6()
_strict_json = R6._strict_json
_pin_live = R6._pin_live
_require_absent = R6._require_absent
_stage_bytes_exclusive = R6._stage_bytes_exclusive
_verify_manifest_self = R6._verify_manifest_self
_compare_sp_tree = R6._compare_sp_tree
_check_intended_tree_stdlib = R6._check_intended_tree_stdlib


def _require_under_packet(dest: Path) -> Path:
    p = dest if dest.is_absolute() else (Path.cwd() / dest)
    norm = os.path.normpath(str(p))
    root = PACKET.resolve()
    if norm != str(root) and not norm.startswith(str(root) + os.sep):
        raise ValueError(f"dest escapes resume packet {root}: {dest}")
    rel = Path(norm).relative_to(root)
    if ".." in rel.parts:
        raise ValueError("traversal forbidden")
    cur = root
    for part in rel.parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink ancestor forbidden: {cur}")
    if os.path.islink(Path(norm)) or Path(norm).exists():
        raise ValueError(f"must be absent under packet: {dest}")
    return Path(norm)


def _stage_bytes_exclusive_packet(abs_dest: Path, data: bytes) -> dict:
    _require_under_packet(abs_dest)
    root = PACKET.resolve()
    norm = os.path.normpath(str(abs_dest if abs_dest.is_absolute() else (Path.cwd() / abs_dest)))
    rel = Path(norm).relative_to(root)
    cur = root
    for part in rel.parts[:-1]:
        cur = cur / part
        if os.path.islink(cur) or not cur.is_dir():
            raise ValueError(f"unsafe/missing packet ancestor: {cur}")
    parent = root / rel.parent
    if os.path.islink(parent) or not parent.is_dir():
        raise ValueError(f"unsafe/missing packet parent: {parent}")
    target = Path(norm)
    if os.path.islink(target) or target.exists():
        raise ValueError(f"refusing overwrite (must be absent): {target}")
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o664)
    try:
        mv = memoryview(data)
        while mv:
            n = os.write(fd, mv)
            mv = mv[n:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(target, 0o664)
    st = os.lstat(target)
    if not stat.S_ISREG(st.st_mode) or os.path.islink(target) or oct(st.st_mode & 0o777) != "0o664" or st.st_nlink != 1:
        raise ValueError(f"packet exclusive write identity failed: {target}")
    if target.read_bytes() != data:
        raise ValueError("packet exclusive write bytes mismatch")
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "mode": "0o664"}


def _load_dispo_r3():
    data = DISPO_R3_TOOL.read_bytes()
    if hashlib.sha256(data).hexdigest() != DISPO_R3_TOOL_SHA:
        raise ValueError("dispo-r3 helper drift vs pinned 48be5879... (refuse)")
    import importlib.util
    spec = importlib.util.spec_from_file_location("w34dispor3", DISPO_R3_TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _derive_old_accepted_dirs_resume(manifest: dict) -> tuple[list[str], list[str]]:
    """Known old dirs from ORIGINAL pinned w34-prepare manifest (cede7e46...).

    D3's `_derive_old_accepted_dirs` requires `w34_tree_full`; the resume
    manifest carries `w34_tree_current`. Never call it here, never fake
    `accepted_evidence_dirs` defaults. Load the ORIGINAL pinned manifest
    (hash-verified), derive 1+1 dirs from its frozen `w34_tree_full` directory
    entries, cross-check parent dirs of its accepted file pins. Returns DIR
    NAMES (not full rels) to match D3 `_check_post_run_layout` convention
    (`{ev_root}/{d}` join inside the helper).
    """
    raw = ORIG_PREP_MANIFEST.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIG_PREP_MANIFEST_SHA:
        raise ValueError("original prepare manifest drift vs pinned cede7e46... (refuse)")
    orig = json.loads(raw.decode("utf-8"))
    if "w34_tree_full" not in orig or "dirs" not in orig["w34_tree_full"]:
        raise ValueError("original manifest lacks frozen w34_tree_full dirs (refuse)")
    dirs = [e["rel"] for e in orig["w34_tree_full"]["dirs"]]
    ev_root = f"{SRC_REL.as_posix()}/evidence/v2/accepted"
    view_root = f"{SRC_REL.as_posix()}/evidence/v2/views/accepted"
    old_ev_full = sorted(d for d in dirs if d.startswith(ev_root + "/") and d.count("/") == len(ev_root.split("/")) and d != ev_root)
    old_view_full = sorted(d for d in dirs if d.startswith(view_root + "/") and d.count("/") == len(view_root.split("/")) and d != view_root)
    if len(old_ev_full) != 1 or len(old_view_full) != 1:
        raise ValueError(f"original old dirs != 1+1 (got ev={old_ev_full} views={old_view_full})")
    pin_parents: set[str] = set()
    for key, pin in orig.get("original_authority", {}).items():
        if isinstance(pin, dict) and "rel" in pin and key.startswith("accepted_") and (key.endswith("_evidence-accepted.json") or key.endswith("_json")):
            pin_parents.add(str(Path(pin["rel"]).parent.as_posix()))
    if old_ev_full[0] not in pin_parents or old_view_full[0] not in pin_parents:
        raise ValueError(f"derived old dirs lack accepted file-pin parents: {old_ev_full} {old_view_full} vs {sorted(pin_parents)}")
    return [old_ev_full[0].rsplit("/", 1)[-1]], [old_view_full[0].rsplit("/", 1)[-1]]


def _strict_w34_state(R6mod, repo: Path, M: dict):
    cfg = M["core"].load_json(repo / M["core"].DEFAULT_CONFIG)
    state = R6mod._strict_json(repo / (SRC_REL / "production-state.json"))
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


def stage_resume(ret_dir: Path, manifest_path: Path, exp_manifest_sha: str, new_input_id: str, prepare_only: bool) -> dict:
    manifest = _verify_manifest_self(manifest_path, exp_manifest_sha)
    repo = REPO_ROOT.resolve()
    errs: list[str] = []
    ctx: dict = {}
    # P0: source771 BEFORE import (stdlib only), no writes
    try:
        # P0: umask single read/restore (no double-os.umask defect)
        _umask_prev = os.umask(0)
        os.umask(_umask_prev)
        umask_val, umask_file_mode = oct(_umask_prev), (0o666 & ~_umask_prev)
        ctx["umask"] = umask_val
        ctx["umask_file_mode"] = umask_file_mode
        pre = {}
        for rel in IMPORT_BOUND:
            pin = _pin_live(repo, Path(rel), manifest["original_authority"][f"module_{Path(rel).name}"])
            pre[rel] = pin["sha256"]
        errs.extend(R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
        if errs:
            raise ValueError("phase0 source precheck FAILED (refuse BEFORE any project import):\n- " + "\n- ".join(errs[:10]))
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
    # after-import re-hash 9 + transitive schema 10th + no pycache
    _mod_files = ((ev, "survey_evidence_v2.py"), (rn, "run_evidence_v2_interactive.py"), (low, "survey_research_authority_v2.py"),
                  (at, "survey_agent_tool_v2.py"), (agent, "survey_agent_control_v2.py"), (core, "survey_production_v2.py"),
                  (sc, "survey_screening_v2.py"), (disc, "survey_discovery_v2.py"), (comp, "survey_completeness_v2.py"))
    _roots = {}
    for _mod, _fname in _mod_files:
        _f = Path(_mod.__file__)
        if repo.resolve() not in _f.resolve().parents:
            raise ValueError(f"module root outside e84: {_fname}")
        _h = hashlib.sha256(_f.read_bytes()).hexdigest()
        if _h != pre["scripts/" + _fname]:
            raise ValueError(f"source changed across import: {_fname}")
        _roots[_fname] = {"file": str(_f), "sha256": _h}
    _sg = getattr(rn, "schema_gate", None)
    if _sg is None or not hasattr(_sg, "__file__"):
        raise ValueError("transitive schema_gate missing on rn (refuse)")
    _sgf = Path(_sg.__file__)
    if repo.resolve() not in _sgf.resolve().parents:
        raise ValueError("module root outside e84: survey_schema_v2.py (via rn.schema_gate)")
    _sgh = hashlib.sha256(_sgf.read_bytes()).hexdigest()
    if _sgh != pre["scripts/survey_schema_v2.py"]:
        raise ValueError("source changed across import: survey_schema_v2.py (via rn.schema_gate)")
    _roots["survey_schema_v2.py"] = {"file": str(_sgf), "sha256": _sgh}
    if list((repo / "scripts").rglob("__pycache__")):
        raise ValueError("__pycache__ present in active source (refuse)")
    M = {"ev": ev, "rn": rn, "low": low, "at": at, "agent": agent, "core": core, "sc": sc, "disc": disc, "comp": comp, "roots": _roots}
    try:
        live_impl = core.repository_commit_sha(repo)
        if not HEX40_RE.fullmatch(live_impl or ""):
            errs.append(f"live impl SHA not 40-hex: {live_impl!r}")
        ctx["live_implementation_sha"] = live_impl
        if live_impl != manifest["active_instance"]["recorded_head"]:
            errs.append("live HEAD drift vs recorded e84 head (refuse)")
        cfg, state, state_path, profile_path = _strict_w34_state(R6, repo, M)
        ctx["state_path"] = state_path
        # current tree MUST be 1780/80 (1781 + staged r2 - exact2), exact2 absent
        live_files, live_dirs, walk_errs = R6._walk_sp_tree_stdlib(repo, SRC_REL)
        if walk_errs:
            errs.extend(f"walk: {e}" for e in walk_errs)
        else:
            exp_files = {e["rel"]: e for e in manifest["w34_tree_current"]["files"]}
            exp_dirs = {e["rel"] for e in manifest["w34_tree_current"]["dirs"]}
            errs.extend(f"tree: {e}" for e in R6._compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs))
        for rel in ("sources/2026-W34/materiality-ledger-v2.json", "sources/2026-W34/profile-completeness-v2.json"):
            try:
                R6._require_absent(repo, Path(rel))
            except ValueError as e:
                errs.append(f"exact2 must stay absent (CONTINUE ABSENT): {e}")
        for key in ("ledger", "completeness"):
            expect = manifest["backups_pinned"][key]
            back = RESUME / "retention-W34-dispose-20261105T003915Z" / expect["rel"]
            if os.path.islink(back) or not back.is_file():
                errs.append(f"retained backup missing/unsafe: {key}")
            else:
                st = os.lstat(back)
                if hashlib.sha256(back.read_bytes()).hexdigest() != expect["sha256"] or back.stat().st_size != expect["bytes"] or oct(st.st_mode & 0o777) != "0o664" or st.st_nlink != 1:
                    errs.append(f"retained backup drift (STOP): {expect['rel']}")
        for key in ("state", "profile", "dcp_jsonl", "dcp_accepted", "scp_accepted", "scp_event", "proposed_input", "config"):
            pin = manifest["original_authority"][key]
            try:
                _pin_live(repo, Path(pin["rel"]), pin)
            except ValueError as e:
                errs.append(f"preserved {key}: {e}")
        # supplement FILE verified first (ce6f...), then exact 428 Raw pins derived (no empty-default skip)
        _supp_rel = manifest["supplement_reused"]["rel"]
        _supp_pin = {"sha256": manifest["supplement_reused"]["sha256"], "bytes": manifest["supplement_reused"]["bytes"]}
        try:
            _pin_live(repo, Path(_supp_rel), _supp_pin, mode="0o664")
        except ValueError as e:
            errs.append(f"preserved supplement FILE: {e}")
        else:
            _supp_doc = json.loads((repo / _supp_rel).read_bytes().decode("utf-8"))
            _supp_rows = _supp_doc.get("sources", [])
            if len(_supp_rows) != 428 or len(set(s.get("raw_path") for s in _supp_rows)) != 425:
                errs.append(f"supplement rows != 428/425 (got {len(_supp_rows)}/{len(set(s.get('raw_path') for s in _supp_rows))})")
            else:
                for s in _supp_rows:
                    if not HEX64_RE.fullmatch(s.get("raw_sha256") or ""):
                        errs.append(f"supplement row SHA not 64-hex: {s.get('discovery_id')}")
                        break
                    try:
                        _pin_live(repo, Path(s["raw_path"]), {"sha256": s["raw_sha256"], "bytes": s["byte_count"]}, mode="0o664")
                    except ValueError as e:
                        errs.append(f"supplement Raw {s.get('discovery_id')}: {e}")
                        break
                else:
                    ctx["supplement_rows"] = _supp_rows
        # SP stable anchors only (whole SP NOT frozen; preflight may complete soon)
        for f, exp in [("sources/SP-efficient-llm-2026/production-state.json", "4865998b99ab2902954619b2a7761c4ae0de77695b06ddd5b5e25d49dff4eb89"),
                       ("sources/SP-efficient-llm-2026/production-profile.json", "aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45")]:
            try:
                _pin_live(repo, Path(f), {"sha256": exp, "bytes": (repo / f).stat().st_size})
            except ValueError as e:
                errs.append(f"SP anchor drift (STOP): {f}: {e}")
        for f, exp in [("retention-SP-20261104T162747Z/READY.json", "c7cd05a888106b2cdf0f4e984fb22412678a8ff792deda1ad7ff94e3b31e7643"),
                       ("retention-SP-dispose-20261105T000554Z/DISPOSE_RUN.json", "cf26a23c06a01058a432ccfa7677a7931a2457e77edcc2094e77ffd8d7434ecf")]:
            p = RESUME / f
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != exp:
                errs.append(f"SP retention drift (STOP): {f}")
        # B1 fix: known old dirs from ORIGINAL pinned manifest (not invented defaults)
        try:
            _old_ev_dirs, _old_view_dirs = _derive_old_accepted_dirs_resume(manifest)
            ctx["old_ev_dirs"], ctx["old_view_dirs"] = _old_ev_dirs, _old_view_dirs
        except ValueError as e:
            errs.append(f"old accepted dirs: {e}")
        # r3 input schema/task coverage requires effective basis + retained package
        with at.current_stage_basis_override():
            accepted_discovery = disc.validate_acceptance(repo, (repo / SRC_REL) / "discovery/discovery-accepted-v2.json")
            root_path = core.repo_local_path(repo, accepted_discovery["discovery_path"], "accepted Discovery JSONL")
            active = sc.resolve_active_screening_acceptance(repo, state_path, live_impl)
            _sp = Path(active["path"])
            screening_path = _sp if _sp.is_absolute() else (repo / _sp)
            effective = sc.resolve_effective_discovery_basis(repo, screening_path.parent / "package.json", live_impl, accepted_root_path=root_path)
        root_recs, disc_recs = effective.get("root_records"), effective.get("records")
        if not isinstance(root_recs, list) or len(root_recs) != 369:
            errs.append(f"effective root_records != 369 (got {len(root_recs) if isinstance(root_recs, list) else type(root_recs)})")
        if not isinstance(disc_recs, list) or len(disc_recs) != 439:
            errs.append(f"effective records != 439 (got {len(disc_recs) if isinstance(disc_recs, list) else type(disc_recs)})")
        ctx["screening_acc_path"] = screening_path if screening_path.is_absolute() else (repo / screening_path)
        ctx["effective_path"] = Path(effective["path"]) if Path(effective["path"]).is_absolute() else (repo / effective["path"])
        ctx["disc_recs"], ctx["root_recs"] = disc_recs, root_recs
    except ValueError as e:
        errs.append(f"phase1 exception: {e}")
    if errs:
        raise ValueError("preflight reads FAILED (zero active writes):\n- " + "\n- ".join(errs[:25]))
    # ---- retention (packet-only, after read-only gate) ----
    if not ID_RE.fullmatch(new_input_id or ""):
        raise ValueError(f"bad new_input_id: {new_input_id!r}")
    try:
        ret_dir = _require_under_packet(ret_dir)
        ret_dir.parent.mkdir(parents=True, exist_ok=True)
    except ValueError as e:
        raise ValueError(f"retention path refused (must be under resume packet): {e}") from e
    try:
        ret_dir.mkdir(exist_ok=False)
    except FileExistsError:
        raise ValueError(f"single-use refuse: retention exists: {ret_dir}")
    journal: list[dict] = [{"step": "phase1-reads", "result": "pass", "live_impl": ctx["live_implementation_sha"], "umask": ctx["umask"]}]
    # ---- stage ONLY NEW r3 input (exclusive, after schema/task coverage) ----
    r3_raw = R3_INPUT.read_bytes()
    if hashlib.sha256(r3_raw).hexdigest() != manifest["corrected_r3_input"]["sha256"]:
        raise ValueError("r3 input bytes drift vs manifest")
    r3 = json.loads(r3_raw.decode("utf-8"))
    if r3.get("issue_id") != ISSUE or r3.get("schema_version") != "2.0-rc1":
        raise ValueError("r3 input identity mismatch")
    if len(r3.get("records", [])) != 409 or len(r3.get("completeness", {}).get("obligations", [])) != 3:
        raise ValueError("r3 input counts != 409/3")
    ctx["new_input_rel"] = f"sources/2026-W34/evidence/proposed-input/interactive-evidence-{new_input_id}.json"
    try:
        R6._require_absent(repo, Path(ctx["new_input_rel"]))
    except ValueError as e:
        raise ValueError(f"NEW input path must be absent: {e}")
    # task coverage via retained real package (same basis; preflight READY binds exact dir + hash)
    prep_ret = RESUME / "retention-W34-20261104T235848Z"
    prep_ready_path = prep_ret / "READY.json"
    prep_ready_raw = prep_ready_path.read_bytes()
    if hashlib.sha256(prep_ready_raw).hexdigest() != "473bf85bf33b9f8adaf33d0f7c588bea6bbcbe5bd7e3bd33b4772788d6788200":
        raise ValueError("preflight READY drift vs 473bf85b... (refuse)")
    prep_ready = json.loads(prep_ready_raw.decode("utf-8"))
    if "retained_pkg_dir" not in prep_ready or "package_json_sha" not in prep_ready:
        raise ValueError("preflight READY lacks retained_pkg_dir/package_json_sha (refuse invented defaults)")
    pkg_path = prep_ret / prep_ready["retained_pkg_dir"] / "package.json"
    if not pkg_path.is_file() or os.path.islink(pkg_path):
        raise ValueError(f"retained 409-task package missing/unsafe: {pkg_path}")
    package = json.loads(pkg_path.read_bytes().decode("utf-8"))
    if "tasks" not in package or len(package["tasks"]) != 409:
        raise ValueError("retained package tasks != 409 (refuse invented defaults)")
    if hashlib.sha256(pkg_path.read_bytes()).hexdigest() != prep_ready["package_json_sha"]:
        raise ValueError("retained package.json drift vs preflight READY (refuse)")
    with at.current_stage_basis_override():
        ev.validate_evidence_package_basis(repo, pkg_path, package, live_impl)
    task_meta = {m["discovery_ids"][0]: m for m in package["tasks"]}
    ctx["package"], ctx["pkg_path"] = package, pkg_path
    with at.current_stage_basis_override():
        run_screening, _, run_discs = ev.validate_screening_acceptance(repo, ctx["screening_acc_path"], ctx["effective_path"], ISSUE, ctx["live_implementation_sha"])
        run_ctx = ev._resolve_phase_supplement_context(repo, package, implementation_sha=ctx["live_implementation_sha"], screening_acceptance=run_screening, discoveries=run_discs)
        run_pins = ev._capture_phase_pins((("Evidence package", pkg_path),) + tuple((f"Evidence Task {m['evidence_task_id']}", pkg_path.parent / m["path"]) for m in package["tasks"]))
    ctx["run_ctx"], ctx["run_pins"] = run_ctx, run_pins
    task_source_ids: dict[str, set[str]] = {}
    for did, meta in task_meta.items():
        task = json.loads((pkg_path.parent / meta["path"]).read_bytes().decode("utf-8"))
        base = ev._discovery_task_sources(task)
        task_source_ids[did] = set(ev._merge_supplement_task_sources(base, task, run_ctx["entries"]))
    # SAME input validation phase as runner (existing private helpers inside, no bypass)
    with at.current_stage_basis_override():
        real_acc, _, real_disc = ev.validate_screening_acceptance(repo, ctx["screening_acc_path"], ctx["effective_path"], ISSUE, live_impl)
        ev.validate_evidence_authority_supplement(repo, repo / Path(manifest["supplement_reused"]["rel"]), live_impl,
            expected_issue_id=ISSUE, expected_source_root=(repo / SRC_REL).resolve(),
            expected_discovery_path=ctx["effective_path"], expected_screening_acceptance_path=ctx["screening_acc_path"],
            screening_acceptance=real_acc, discoveries=real_disc)
    profile = core.load_json(repo / (SRC_REL / "production-profile.json"))
    # SAME input validation phase as runner (existing private helpers inside, no bypass/mirror)
    from scripts import run_evidence_v2_interactive as _rnmod
    by_id, runner, _ = _rnmod.validate_interactive_input(r3, profile, set(task_meta), task_source_ids, discovery_records=ctx["disc_recs"], root_discovery_records=ctx["root_recs"])
    journal.append({"step": "r3-input-covered", "records": len(by_id), "runner": runner})
    new_input_abs = repo / Path(ctx["new_input_rel"])
    got_input = R6._stage_bytes_exclusive(new_input_abs, repo, r3_raw)
    journal.append({"step": "stage-new-input", "rel": ctx["new_input_rel"], **got_input})
    # ---- SAME canonical card-core preflight ALL 409 (nonpublishing) + Raw closure ----
    # Retain ACTUAL canonical card bytes (core.json_bytes) outside active; no view claim.
    cards_dir = ret_dir / f"cards-{new_input_id}"
    cards_dir.mkdir(exist_ok=False)
    card_ok = 0
    for did in sorted(task_meta):
        meta = task_meta[did]
        task = json.loads((pkg_path.parent / meta["path"]).read_bytes().decode("utf-8"))
        _auth = ev._merge_supplement_task_sources(ev._discovery_task_sources(task), task, run_ctx["entries"])
        card = ev._build_card_core(task, meta, package, by_id[did], runner, _auth)
        errs_c = ev._validate_card_core(card, task, meta["sha256"], package, lambda _t=task: ev._merge_supplement_task_sources(ev._discovery_task_sources(_t), _t, run_ctx["entries"]))
        if errs_c:
            raise ValueError(f"card-core invalid {did}: {'; '.join(errs_c)}")
        card_bytes = core.json_bytes(card)
        cpath = cards_dir / f"card-{did}.json"
        if cpath.exists() or os.path.islink(cpath):
            raise ValueError(f"card retain collision: {did}")
        cpath.write_bytes(card_bytes)
        card_ok += 1
    if card_ok != 409:
        raise ValueError(f"card-core preflight != 409 (got {card_ok})")
    with at.current_stage_basis_override():
        ev._finish_authority_phase(repo, run_ctx, run_pins, revalidate_owner=lambda: ev.validate_evidence_package_basis(repo, pkg_path, package, live_impl))
    journal.append({"step": "card-core-409", "cards": card_ok, "cards_dir": cards_dir.name})
    # ---- shared FULL guards BEFORE READY (even --prepare-only): baseline+1/source/State/absent2/backups/supp/input/self-manifest SAME hash ----
    _pre_ready_errs: list[str] = []
    _live_pre, _dirs_pre, _walk_pre = R6._walk_sp_tree_stdlib(repo, SRC_REL)
    if _walk_pre:
        _pre_ready_errs.extend(f"pre-ready walk: {e}" for e in _walk_pre)
    else:
        _exp_plus1 = {e["rel"]: e for e in manifest["w34_tree_current"]["files"]}
        _exp_plus1[ctx["new_input_rel"]] = {"sha256": got_input["sha256"], "bytes": got_input["bytes"], "mode": "0o664", "nlink": 1}
        _exp_dirs = {e["rel"] for e in manifest["w34_tree_current"]["dirs"]}
        _pre_ready_errs.extend(f"pre-ready tree: {e}" for e in R6._compare_sp_tree(_live_pre, _dirs_pre, _exp_plus1, _exp_dirs))
    _pre_ready_errs.extend(f"pre-ready intended: {e}" for e in R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    for _rel in ("sources/2026-W34/materiality-ledger-v2.json", "sources/2026-W34/profile-completeness-v2.json"):
        try:
            R6._require_absent(repo, Path(_rel))
        except ValueError as e:
            _pre_ready_errs.append(f"exact2 must stay absent before READY: {e}")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        _pre_ready_errs.append("State bytes changed before READY (STOP)")
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
        _pre_ready_errs.append("self-manifest changed before READY (refuse SAME-hash recheck)")
    if _pre_ready_errs:
        raise ValueError("pre-READY recheck FAILED (preserve, STOP):\n- " + "\n- ".join(_pre_ready_errs[:10]))
    _strict_w34_state(R6, repo, M)
    _stage_bytes_exclusive_packet(ret_dir / "preflight-journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    ready = {"ready": True, "stage": "resume-preflight-only", "no_removal": True, "no_restore": True,
             "manifest": {"path": manifest_path.name, "sha256": exp_manifest_sha},
             "live_implementation_sha": ctx["live_implementation_sha"], "historical_implementation_sha": HIST_IMPL,
             "new_input": {"rel": ctx["new_input_rel"], **got_input}, "task_count": 409, "input_records": len(by_id),
             "retained_cards_dir": cards_dir.name, "cards": card_ok, "journal": journal}
    _stage_bytes_exclusive_packet(ret_dir / "READY.json", (json.dumps(ready, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    if prepare_only:
        return {"ready": str(ret_dir / "READY.json"), "tasks": 409, "records": len(by_id), "cards": card_ok, "prepared_only": True}
    # ---- before normal run: recheck baseline+1/source/State/absent2/backups/Raw/input/manifest ----
    live_files2, live_dirs2, walk_errs2 = R6._walk_sp_tree_stdlib(repo, SRC_REL)
    if walk_errs2:
        raise ValueError("pre-run walk FAILED:\n- " + "\n- ".join(walk_errs2[:10]))
    exp_plus1 = {e["rel"]: e for e in manifest["w34_tree_current"]["files"]}
    exp_plus1[ctx["new_input_rel"]] = {"sha256": got_input["sha256"], "bytes": got_input["bytes"], "mode": "0o664", "nlink": 1}
    exp_dirs2 = {e["rel"] for e in manifest["w34_tree_current"]["dirs"]}
    term_errs = R6._compare_sp_tree(live_files2, live_dirs2, exp_plus1, exp_dirs2)
    if term_errs:
        raise ValueError("pre-run tree FAILED (preserve, STOP):\n- " + "\n- ".join(term_errs[:10]))
    term_errs.extend(R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    for rel in ("sources/2026-W34/materiality-ledger-v2.json", "sources/2026-W34/profile-completeness-v2.json"):
        try:
            R6._require_absent(repo, Path(rel))
        except ValueError as e:
            term_errs.append(f"exact2 must stay absent before run: {e}")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        term_errs.append("State bytes changed before run (STOP)")
    if term_errs:
        raise ValueError("pre-run recheck FAILED (preserve, STOP):\n- " + "\n- ".join(term_errs[:10]))
    _strict_w34_state_resume(R6, repo, M)
    # ---- ONE normal run only ----
    result = rn.run(repo, state_path, new_input_abs, repo / Path(manifest["supplement_reused"]["rel"]))
    journal.append({"step": "run", "result": result})
    if result.get("evidence_result_count") != 409:
        raise ValueError(f"run result count != 409 (preserve, STOP): {result.get('evidence_result_count')}")
    # ---- post-run: prove with dispo-r3 helpers (pinned import, disposal never executed) ----
    # Resume adaptation: baseline 1780 excludes old2 (CONTINUE ABSENT); supply
    # explicit observation-only expected old2 from PINNED backups (no claim
    # originals exist live). D3's preserved loop already skips old2 rels; the
    # regen check compares live got vs backup pins (must differ = regenerated).
    # Re-derive old dirs here and require equality with P1 ctx (guard continuity).
    D3 = _load_dispo_r3()
    _old_ev_re, _old_view_re = _derive_old_accepted_dirs_resume(manifest)
    if _old_ev_re != ctx["old_ev_dirs"] or _old_view_re != ctx["old_view_dirs"]:
        raise ValueError(f"old dirs drift P1 vs pre-run (STOP): {ctx['old_ev_dirs']} vs {_old_ev_re}")
    _old_ev, _old_view = ctx["old_ev_dirs"], ctx["old_view_dirs"]
    _base_plus1 = {e["rel"]: e for e in manifest["w34_tree_current"]["files"]}
    _base_plus1[ctx["new_input_rel"]] = {"sha256": got_input["sha256"], "bytes": got_input["bytes"], "mode": "0o664", "nlink": 1}
    _obs_old2 = {
        LEDGER_REL.as_posix(): {"sha256": manifest["backups_pinned"]["ledger"]["sha256"], "bytes": manifest["backups_pinned"]["ledger"]["bytes"], "mode": "0o664", "nlink": 1},
        COMP_REL.as_posix(): {"sha256": manifest["backups_pinned"]["completeness"]["sha256"], "bytes": manifest["backups_pinned"]["completeness"]["bytes"], "mode": "0o664", "nlink": 1},
    }
    _base_plus1_obs = dict(_base_plus1)
    _base_plus1_obs.update(_obs_old2)
    _base_dirs = {e["rel"] for e in manifest["w34_tree_current"]["dirs"]}
    _bindings = D3._check_post_run_layout(repo, SRC_REL, _base_plus1_obs, _base_dirs,
        [{"rel": ctx["new_input_rel"], "sha256": got_input["sha256"], "bytes": got_input["bytes"]}],
        LEDGER_REL.as_posix(), COMP_REL.as_posix(), _old_ev, _old_view,
        409, ctx["new_input_rel"], got_input["sha256"],
        manifest["supplement_reused"]["rel"], manifest["supplement_reused"]["sha256"],
        439, 3, "LIMITED", ctx["umask_file_mode"])
    with at.current_stage_basis_override():
        _ev_acc_path = repo / _bindings["ev_acceptance"]
        _view_acc_path = repo / _bindings["views_acceptance"]
        ev.validate_evidence_acceptance(repo, _ev_acc_path, ctx["live_implementation_sha"])
        ev.validate_edition_views_acceptance(repo, repo / (SRC_REL / "production-profile.json"), _ev_acc_path, _view_acc_path, ctx["live_implementation_sha"])
        _ledger_doc = json.loads((repo / _bindings["ledger"]).read_bytes().decode("utf-8"))
        ev.validate_materiality_ledger(_ledger_doc, repo, repo / (SRC_REL / "production-profile.json"),
            ctx["effective_path"], ctx["screening_acc_path"], _ev_acc_path, _view_acc_path, ctx["live_implementation_sha"])
        _comp_doc = json.loads((repo / _bindings["completeness"]).read_bytes().decode("utf-8"))
        _comp_errs = comp.validate_profile_completeness(_comp_doc, repo, repo / (SRC_REL / "production-profile.json"),
            ctx["effective_path"], ctx["screening_acc_path"], _ev_acc_path, _view_acc_path, repo / _bindings["ledger"], ctx["live_implementation_sha"])
        if _comp_errs:
            raise ValueError("produced Completeness invalid: " + "; ".join(_comp_errs))
    journal.append({"step": "post-run-verify", "result": "pass", "bindings": _bindings})
    # Terminal post pins AFTER final validators (not only before run):
    # source771 + State + old whole current baseline inputs/supp + manifest
    # SAME hash + new Ledger/Completeness expected post pins.
    _term_errs: list[str] = []
    try:
        _term_errs.extend(f"terminal intended: {e}" for e in R6._check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    except ValueError as e:
        _term_errs.append(f"terminal intended exception: {e}")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        _term_errs.append("State bytes changed post-run (STOP)")
    for _key in ("dcp_jsonl", "dcp_accepted", "scp_accepted", "scp_event", "proposed_input", "config"):
        try:
            R6._pin_live(repo, Path(manifest["original_authority"][_key]["rel"]), manifest["original_authority"][_key])
        except ValueError as e:
            _term_errs.append(f"terminal preserved {_key}: {e}")
    try:
        R6._pin_live(repo, Path(manifest["supplement_reused"]["rel"]), {"sha256": manifest["supplement_reused"]["sha256"], "bytes": manifest["supplement_reused"]["bytes"]})
    except ValueError as e:
        _term_errs.append(f"terminal preserved supplement: {e}")
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != exp_manifest_sha:
        _term_errs.append("manifest changed post-run (refuse SAME-hash recheck)")
    for _rel_key, _sha_key in (("ledger", "ledger_sha"), ("completeness", "completeness_sha")):
        _cur = (repo / _bindings[_rel_key]).read_bytes()
        if hashlib.sha256(_cur).hexdigest() != _bindings[_sha_key]:
            _term_errs.append(f"{_rel_key} bytes changed since post-run validation (refuse record)")
    if _term_errs:
        raise ValueError("terminal post-run recheck FAILED (preserve, STOP):\n- " + "\n- ".join(_term_errs[:10]))
    _strict_w34_state_resume(R6, repo, M)
    journal.append({"step": "terminal-post-pins", "result": "pass"})
    _stage_bytes_exclusive_packet(ret_dir / "journal.json", (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"result": "run-complete", "tasks": result.get("evidence_result_count"), "completeness": result.get("completeness_status"), "bindings": _bindings}


def _strict_w34_state_resume(R6mod, repo: Path, M: dict):
    cfg = M["core"].load_json(repo / M["core"].DEFAULT_CONFIG)
    state = R6mod._strict_json(repo / (SRC_REL / "production-state.json"))
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
    return cfg, state


def main() -> int:
    global REPO_ROOT
    ap = argparse.ArgumentParser(description="W34 resume-only (review only, do not run yet)")
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, default=RESUME / "w34-resume-expected-manifest-20261105.json")
    ap.add_argument("--expected-manifest-sha", type=str, required=True)
    ap.add_argument("--expected-tool-sha", type=str, required=True)
    ap.add_argument("--new-input-id", type=str, required=True)
    ap.add_argument("--prepare-only", action="store_true", help="stop at READY (retained cards + journal), no normal run")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    a = ap.parse_args()
    REPO_ROOT = a.repo_root
    try:
        if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != a.expected_tool_sha:
            raise ValueError("wrapper bytes drift vs externally recorded tool hash (refuse)")
        out = stage_resume(a.retention_dir, a.manifest, a.expected_manifest_sha, a.new_input_id, a.prepare_only)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            rd = a.retention_dir
            rdn = Path(os.path.normpath(str(rd if rd.is_absolute() else (Path.cwd() / rd))))
            if PACKET.resolve() == rdn.resolve() or PACKET.resolve() in rdn.resolve().parents:
                if rdn.is_dir() and not os.path.islink(rdn):
                    partials = sorted(p.relative_to(rdn).as_posix() for p in rdn.rglob("*") if p.is_file())
                    try:
                        fd = os.open(rdn / "FAILURE.json", os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o664)
                        try:
                            payload = (json.dumps({"stage": "resume", "exit": 2, "error": str(exc)[:4000], "retained_partials": partials}, ensure_ascii=False, indent=2) + "\n").encode()
                            mv = memoryview(payload)
                            while mv:
                                n = os.write(fd, mv)
                                mv = mv[n:]
                            os.fsync(fd)
                        finally:
                            os.close(fd)
                        os.chmod(rdn / "FAILURE.json", 0o664)
                    except OSError:
                        pass
        except OSError:
            pass
        print(f"RESUME_REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"stage": "resume", "exit": 0, **out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
