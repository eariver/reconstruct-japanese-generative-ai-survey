#!/usr/bin/env python3
"""SP PREPARE-ONLY operator tool r6 — SOURCE REVIEW ONLY, DO NOT EXECUTE YET.

Narrow successor of r5 (preserved unchanged). Still prepare-only: NO disposition,
NO removal, NO retry, NO auth-file framework. Replaces r5 execution authority
shape where independent review found overstatement. No shipping source changes.

Fixes vs r5 (root direction):
 (1) No hardcoded 0o664 for all771: source modes checked vs recorded
     delivery physical_mode per file (one 0o775 executable recorded); exact
     0o664 enforced ONLY for explicitly expected new/owned files. Triangulated
     exact test d486 pin (delivered/intended vs live e84 vs r3-recorded),
     never skipped, never resealed from fresh reads.
 (2) 771 preflight moved BEFORE project imports (phase 0, stdlib-only);
     full all771 rechecked at terminal (phase 4 prepost).
 (3) Terminal recheck is FULL: original SP552 files + 32 dirs + expected exact
     19 new, byte/mode/nlink/type/set-equal, accepted cards/CP/gates/ref-scan
     re-verified; symlinks/special entries refuse (no silent skips).
 (4) Lexical paths passed to the exclusive writer (no .resolve() at callsites,
     which would normalize a swapped ancestor away); retention ancestors
     validated before mkdir. Checks are fail-closed snapshots, NOT atomic vs
     concurrent modification (single-operator assumption; no race claim).
 (5) Expected manifest pinned at invocation (--expected-manifest-sha, recorded
     externally in the authorize command) and rechecked before READY (same
     captured hash, not fresh-read reseal). Retained package/tasks authority
     rechecked at phase end via existing _finish_authority_phase with the pins
     + context captured at initial package validation (no dummy context, no
     third validator), inside the needed current facade.
 (6) Package scratch: absent required, never pre-created (the API creates it;
     it also accepts an existing empty dir, which we refuse as non-single-use).

LIVE implementation_sha ALWAYS from core.repository_commit_sha(repo_root) in
the explicit isolated e84 repo (the single selected isolated call, mirrors
run() line 599). State480 is historical provenance only, never passed as live.
"""
from __future__ import annotations
import argparse
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
WSROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
SRC_REL = Path("sources/SP-efficient-llm-2026")
ISSUE = "SP-efficient-llm-2026"
HIST_IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
GEN_MANIFEST = RESUME / "sp-prepare-expected-manifest-r6-20261104.json"
R4_INPUT = RESUME / "sp-corrected-input-r4-20261104.json"
R4_SUPP = RESUME / "sp-corrected-supplement-r4-20261104.json"
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


def _strict_json(path: Path) -> dict:
    raw = path.read_bytes()

    def _hook(pairs):
        o = {}
        for k, v in pairs:
            if k in o:
                raise ValueError(f"duplicate JSON key in {path}: {k!r}")
            o[k] = v
        return o

    val = json.loads(raw.decode("utf-8"), object_pairs_hook=_hook)
    if not isinstance(val, dict):
        raise ValueError(f"expected JSON object: {path}")
    return val


def _ancestors_ok(repo_root: Path, rel: Path) -> Path:
    """Lexical ancestor walk (NO resolve: resolve would normalize a mid-path
    symlink away and hide an ancestor swap). Every component islink-free."""
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"path must be repo-relative without traversal: {rel}")
    root = repo_root.resolve()
    cur = root
    for part in rel.parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink ancestor forbidden: {cur} (rel {rel})")
    return root / rel


def _pin_live(repo_root: Path, rel: Path, expect: dict | None = None, *, mode: str | None = None) -> dict:
    """Pin a live file. Mode rule: manifest-recorded mode in expect wins;
    else explicit mode; new/owned files pass mode='0o664'. Never hardcoded."""
    _ancestors_ok(repo_root, rel)
    abs_p = repo_root.resolve() / rel
    if os.path.islink(abs_p) or not abs_p.is_file():
        raise ValueError(f"missing/unsafe live file: {rel}")
    st = os.lstat(abs_p)
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
        raise ValueError(f"identity drift (type/nlink): {rel} nlink={st.st_nlink}")
    want = (expect.get("mode") if expect and "mode" in expect else mode)
    if want is not None and oct(st.st_mode & 0o777) != want:
        raise ValueError(f"mode drift: {rel} got {oct(st.st_mode & 0o777)} expected {want}")
    data = abs_p.read_bytes()
    pin = {"rel": rel.as_posix(), "bytes": len(data),
           "sha256": hashlib.sha256(data).hexdigest(), "mode": oct(st.st_mode & 0o777)}
    if expect is not None and (pin["sha256"] != expect["sha256"] or pin["bytes"] != expect["bytes"]):
        raise ValueError(f"pin drift vs manifest: {rel} live {pin['sha256']}/{pin['bytes']} != expected {expect['sha256']}/{expect['bytes']}")
    return pin


def _require_absent(repo_root: Path, rel: Path) -> None:
    _ancestors_ok(repo_root, rel)
    abs_p = repo_root.resolve() / rel
    if os.path.islink(abs_p) or abs_p.exists():
        raise ValueError(f"must be absent (creation expected only here): {rel}")


def _require_absent_under(allowed_root: Path, dest: Path) -> None:
    """Lexical containment + non-existence for packet-local exclusive paths.
    dest may be relative (joined to cwd lexically); never resolved before the
    ancestor walk, so a swapped ancestor cannot hide behind normalization."""
    p = dest if dest.is_absolute() else (Path.cwd() / dest)
    root = allowed_root.resolve()
    norm = os.path.normpath(str(p))
    if norm != str(root) and not norm.startswith(str(root) + os.sep):
        raise ValueError(f"dest escapes allowed root {root}: {dest}")
    rel = Path(norm).relative_to(root)
    cur = root
    for part in rel.parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink ancestor forbidden: {cur}")
    if os.path.islink(Path(norm)) or Path(norm).exists():
        raise ValueError(f"must be absent: {dest}")


def _stage_bytes_exclusive_under(abs_dest: Path, allowed_root: Path, data: bytes) -> dict:
    """O_CREAT|O_EXCL|O_NOFOLLOW buffer write. Lexical ancestor walk (no resolve
    before the check). Snapshot checks only — NOT atomic vs concurrent
    modification; single-operator assumption, no race-atomicity claim."""
    if not abs_dest.is_absolute():
        raise ValueError(f"dest must be absolute: {abs_dest}")
    root = allowed_root.resolve()
    norm = os.path.normpath(str(abs_dest))  # lexical only; no fs access
    if norm != str(root) and not norm.startswith(str(root) + os.sep):
        raise ValueError(f"dest escapes allowed root {root}: {abs_dest}")
    rel = Path(norm).relative_to(root)
    cur = root
    for part in rel.parts[:-1]:
        cur = cur / part
        if os.path.islink(cur) or not cur.is_dir():
            raise ValueError(f"unsafe/missing ancestor: {cur}")
    parent = root / rel.parent
    if os.path.islink(parent) or not parent.is_dir():
        raise ValueError(f"unsafe/missing parent: {parent}")
    abs_dest = Path(norm)
    if os.path.islink(abs_dest) or abs_dest.exists():
        raise ValueError(f"refusing overwrite (must be absent): {abs_dest}")
    fd = os.open(abs_dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o664)
    try:
        mv = memoryview(data)
        while mv:
            n = os.write(fd, mv)
            mv = mv[n:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(abs_dest, 0o664)
    st = os.lstat(abs_dest)
    if not stat.S_ISREG(st.st_mode) or os.path.islink(abs_dest) or oct(st.st_mode & 0o777) != "0o664" or st.st_nlink != 1:
        raise ValueError(f"exclusive write identity failed: {abs_dest}")
    back = abs_dest.read_bytes()
    if back != data:
        raise ValueError(f"exclusive write bytes mismatch: {abs_dest}")
    return {"bytes": len(back), "sha256": hashlib.sha256(back).hexdigest(), "mode": "0o664"}


def _stage_bytes_exclusive(abs_dest: Path, repo_root: Path, data: bytes) -> dict:
    """Active-tree writer: exclusive write contained under the repo root. Caller
    MUST pass a lexical path (no .resolve() at the callsite)."""
    return _stage_bytes_exclusive_under(abs_dest, repo_root.resolve(), data)


def _stage_bytes_exclusive_local(abs_dest: Path, data: bytes) -> dict:
    """Packet-local writer: exclusive write contained under the workspace root.
    Caller MUST pass a lexical path."""
    return _stage_bytes_exclusive_under(abs_dest, WSROOT, data)


def _verify_manifest_self(manifest_path: Path, expected_sha: str) -> dict:
    """Pin the expected manifest itself: file hash must equal the externally
    recorded command hash. Returns parsed manifest (clean required)."""
    if not HEX64_RE.fullmatch(expected_sha or ""):
        raise ValueError("expected manifest SHA must be 64-hex (externally recorded)")
    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha:
        raise ValueError("expected manifest drift vs externally recorded hash (refuse)")
    manifest = _strict_json(manifest_path)
    if not manifest.get("clean"):
        raise ValueError("generated manifest not clean; refuse")
    manifest["_self_sha256"] = expected_sha
    return manifest


def _walk_sp_tree_stdlib(repo_root: Path, src_rel: Path) -> tuple[dict, dict, list]:
    """Full SP walk, no skips: symlinks and special entries are errors, not skips."""
    files: dict = {}
    dirs: set = set()
    errs: list = []
    for p in sorted((repo_root / src_rel).rglob("*")):
        rel = p.relative_to(repo_root).as_posix()
        if p.is_symlink():
            errs.append(f"symlink in SP tree (refuse): {rel}")
            continue
        if p.is_dir():
            dirs.add(rel)
        elif p.is_file():
            st = os.lstat(p)
            if not stat.S_ISREG(st.st_mode):
                errs.append(f"special entry in SP tree (refuse): {rel}")
                continue
            data = p.read_bytes()
            files[rel] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                          "mode": oct(st.st_mode & 0o777), "nlink": st.st_nlink}
        else:
            errs.append(f"special entry in SP tree (refuse): {rel}")
    return files, dirs, errs


def _compare_sp_tree(live_files: dict, live_dirs: set, exp_files: dict, exp_dirs: set) -> list:
    """Byte/mode/nlink/type/set equality vs expected file+dir sets."""
    errs: list = []
    if set(live_files) != set(exp_files):
        errs.append(f"SP tree file set drift: missing={sorted(set(exp_files)-set(live_files))[:8]} extra={sorted(set(live_files)-set(exp_files))[:8]}")
        return errs
    if live_dirs != exp_dirs:
        errs.append(f"SP tree dir set drift: missing={sorted(exp_dirs-live_dirs)[:5]} extra={sorted(live_dirs-exp_dirs)[:5]}")
        return errs
    for rel, exp in exp_files.items():
        got = live_files[rel]
        if (got["sha256"] != exp["sha256"] or got["bytes"] != exp["bytes"]
                or got["mode"] != exp["mode"] or got.get("nlink", 1) != exp.get("nlink", 1)):
            errs.append(f"SP tree file drift: {rel}")
            break
    return errs


def _check_intended_tree_stdlib(repo_root: Path, intended: dict, test_pin: dict) -> list:
    """All771 vs original intended pins (recorded physical modes, incl. 0o775
    executable). Test file triangulated, never skipped. No project imports."""
    errs: list = []
    if test_pin.get("rel") not in intended:
        return [f"test file missing from intended map: {test_pin.get('rel')}"]
    for rel, exp in intended.items():
        if rel == test_pin["rel"]:
            continue
        try:
            got = _pin_live(repo_root, Path(rel), {"sha256": exp["sha256"], "bytes": exp["bytes"]},
                             mode=exp.get("physical_mode"))
            _ = got
        except ValueError as e:
            errs.append(f"intended {rel}: {e}")
            break
    if errs:
        return errs
    # triangulated test pin: live == recorded live == r3 e84; intended == recorded delivered == r3 delivered; live != delivered
    try:
        live = _pin_live(repo_root, Path(test_pin["rel"]))
    except ValueError as e:
        return [f"test file unreadable: {e}"]
    rec_live, rec_del = test_pin["live_e84"], test_pin["delivered"]
    r3 = test_pin.get("r3_recorded", {})
    if live["sha256"] != rec_live["sha256"] or live["bytes"] != rec_live["bytes"]:
        errs.append("live test drift vs recorded e84 pin (refuse; d486 expected)")
    if live["mode"] != rec_live.get("mode", "0o664"):
        errs.append(f"live test mode drift: {live['mode']}")
    if intended[test_pin["rel"]]["sha256"] != rec_del["sha256"] or intended[test_pin["rel"]]["bytes"] != rec_del["bytes"]:
        errs.append("intended test pin drift vs recorded delivered pin (refuse reseal)")
    if live["sha256"] == rec_del["sha256"]:
        errs.append("known test diff violated: live equals delivered")
    if not live["sha256"].startswith(r3.get("e84_prefix16", "")) or not rec_del["sha256"].startswith(r3.get("delivered_prefix16", "")):
        errs.append("test pins diverge from r3-recorded prefixes")
    return errs


def _check_supplement_rows_stdlib(repo_root: Path, supp_sources: list, manifest_rows: list, wsroot: Path) -> list[str]:
    """Pure stdlib pre-validation of all30 rows (hex/pins/bytes, packet + active).
    No writes, no project imports. Returns error list (empty = clean)."""
    errs: list[str] = []
    man_by_sid = {r["supplement_source_id"]: r for r in manifest_rows}
    for s in supp_sources:
        sid = s.get("supplement_source_id")
        exp = man_by_sid.get(sid)
        if exp is None or exp.get("sha256") != s.get("raw_sha256") or exp.get("bytes") != s.get("byte_count"):
            errs.append(f"supplement row drift vs manifest: {s.get('discovery_id')}")
            continue
        if not HEX64_RE.fullmatch(s.get("raw_sha256") or ""):
            errs.append(f"row SHA not 64-hex: {s.get('discovery_id')}")
            continue
        if str(s.get("raw_path", "")).startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-"):
            try:
                _pin_live(repo_root, Path(s["raw_path"]), {"sha256": s["raw_sha256"], "bytes": s["byte_count"]},
                          mode="0o664")
            except ValueError as e:
                errs.append(f"existing Raw {s.get('discovery_id')}: {e}")
        else:
            pkt_rel = (exp.get("packet") or {}).get("path")
            if pkt_rel is None:
                errs.append(f"no packet locator for {s.get('discovery_id')}")
                continue
            pkt = wsroot / pkt_rel
            if os.path.islink(pkt) or not pkt.is_file():
                errs.append(f"unsafe packet source for {s.get('discovery_id')}: {pkt_rel}")
                continue
            data = pkt.read_bytes()
            if hashlib.sha256(data).hexdigest() != s["raw_sha256"] or len(data) != s["byte_count"]:
                errs.append(f"packet bytes drift {s.get('discovery_id')}")
    return errs


def _check_gates_absent(repo_root: Path) -> list:
    errs: list = []
    for rel in EXPECTED_ABSENT:
        try:
            _require_absent(repo_root, rel)
        except ValueError as e:
            errs.append(str(e))
    return errs


def _scan_ledger_refs(repo_root: Path, scan_map: dict) -> list:
    errs: list = []
    for rel in scan_map:
        txt = (repo_root / rel).read_text(encoding="utf-8", errors="replace")
        if ("materiality-ledger" in txt) or ("profile-completeness" in txt):
            errs.append(f"stage file references ledger/completeness: {rel}")
    return errs


def _phase0_source_precheck(repo_root: Path, manifest: dict) -> dict:
    """BEFORE any project import (stdlib only): import-bound module bytes +
    FULL all771 intended preflight (recorded physical modes) + triangulated
    test pin. Refuses on any drift vs original intended files."""
    pre = {}
    for rel in IMPORT_BOUND:
        pin = _pin_live(repo_root, Path(rel), manifest["original_authority"][f"module_{Path(rel).name}"])
        pre[rel] = pin["sha256"]
    errs = _check_intended_tree_stdlib(repo_root, manifest["delivery"]["intended"],
                                       manifest["delivery"]["test_pin"])
    if errs:
        raise ValueError("intended-source preflight FAILED:\n- " + "\n- ".join(errs[:10]))
    return pre


def _bind_roots_after_import(repo_root: Path, pre: dict) -> dict:
    sys.path.insert(0, str(repo_root))
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
        if repo_root.resolve() not in f.resolve().parents:
            raise ValueError(f"module root outside e84: {name} -> {f}")
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        rel = next(r for r in IMPORT_BOUND if Path(r).name == f.name)
        if h != pre[rel]:
            raise ValueError(f"source changed across import: {name}")
        roots[name] = {"file": str(f), "sha256": h}
    if list((repo_root / "scripts").rglob("__pycache__")):
        raise ValueError("__pycache__ present in active source (refuse)")
    return {"ev": ev, "rn": rn, "low": low, "at": at, "agent": agent,
            "core": core, "sc": sc, "disc": disc, "comp": comp, "sg": sg, "roots": roots}


def _strict_state_and_ready(repo_root: Path, M, manifest: dict) -> tuple[dict, dict, Path, Path]:
    cfg = M["core"].load_json(repo_root / M["core"].DEFAULT_CONFIG)
    state = _strict_json(repo_root / (SRC_REL / "production-state.json"))
    if state.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("State drift: lifecycle_state must be CANDIDATES_NORMALIZED")
    mc = state.get("machine_checkpoints", {})
    if not (mc.get("evidence") == "pending" and mc.get("materiality") == "pending" and mc.get("completeness") == "pending"):
        raise ValueError("State drift: machine evidence/materiality/completeness must be pending")
    cp = state.get("checkpoint_provenance", {})
    if not (cp.get("evidence") is None and cp.get("materiality") is None and cp.get("completeness") is None):
        raise ValueError("State drift: checkpoint_provenance evidence/materiality/completeness must be null")
    if state.get("human_gates") != {"architecture_review": "pending", "publication_preview": "pending"}:
        raise ValueError("State drift: human_gates must be pending/pending")
    if state.get("human_gate_provenance") != {"architecture_review": None, "publication_preview": None}:
        raise ValueError("State drift: human_gate_provenance must be null/null")
    if state.get("implementation", {}).get("repository_commit_sha") != HIST_IMPL:
        raise ValueError("State drift: historical implementation SHA must stay 48082356 (history, not live)")
    errs = M["agent"].validate_agent_state(repo_root, cfg, state)
    if errs:
        raise ValueError("strict agent State invalid: " + "; ".join(errs))
    M["low"].require_research_operation_ready(repo_root, repo_root / (SRC_REL / "production-state.json"))
    return cfg, state, repo_root / (SRC_REL / "production-state.json"), repo_root / (SRC_REL / "production-profile.json")


def stage_prepare(ret_dir: Path, new_id: str, manifest_path: Path, expected_manifest_sha: str) -> dict:
    if not ID_RE.fullmatch(new_id or ""):
        raise ValueError(f"bad supplement_id: {new_id!r}")
    manifest = _verify_manifest_self(manifest_path, expected_manifest_sha)
    repo = REPO_ROOT.resolve()
    errs: list[str] = []

    # ---- phase 0: source bytes BEFORE imports (modules + FULL all771, stdlib only) ----
    try:
        pre = _phase0_source_precheck(repo, manifest)
    except ValueError as e:
        raise ValueError(f"phase0 source precheck: {e}") from e
    M = _bind_roots_after_import(repo, pre)
    core = M["core"]

    # ---- phase 1: ALL reads, zero active writes ----
    ctx: dict = {"pre_module_sha": pre, "module_roots": M["roots"]}
    try:
        live_impl = core.repository_commit_sha(repo)  # single selected isolated call (mirrors run():599)
        if not HEX40_RE.fullmatch(live_impl or ""):
            errs.append(f"live implementation SHA not 40-hex: {live_impl!r}")
        ctx["live_implementation_sha"] = live_impl
        ctx["historical_implementation_sha"] = HIST_IMPL
        if live_impl != manifest["active_instance"]["recorded_head"]:
            errs.append(f"live HEAD drift vs recorded e84 head (refuse blind proceed): live {live_impl} != recorded {manifest['active_instance']['recorded_head']}")
        cfg, state, state_path, profile_path = _strict_state_and_ready(repo, M, manifest)
        ctx["state_path"] = state_path.as_posix()
        for key in ("state", "profile", "dcp_jsonl", "dcp_accepted", "scp_accepted", "ledger",
                    "completeness", "supplement_r1", "proposed_input", "config"):
            rel = manifest["original_authority"][key]["rel"]
            try:
                _pin_live(repo, Path(rel), manifest["original_authority"][key])
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
        errs.extend(_check_gates_absent(repo))
        live_files, live_dirs, walk_errs = _walk_sp_tree_stdlib(repo, SRC_REL)
        errs.extend(walk_errs)
        if not walk_errs:
            exp_files = {e["rel"]: e for e in manifest["sp_tree_full"]["files"]}
            exp_dirs = {e["rel"] for e in manifest["sp_tree_full"]["dirs"]}
            errs.extend(_compare_sp_tree(live_files, live_dirs, exp_files, exp_dirs))
        errs.extend(_scan_ledger_refs(repo, manifest["stage_ledger_ref_scan"]))
        r4supp_raw = R4_SUPP.read_bytes()
        r4input_raw = R4_INPUT.read_bytes()
        if hashlib.sha256(r4supp_raw).hexdigest() != manifest["corrected"]["supplement"]["sha256"]:
            errs.append("r4 supplement bytes drift vs manifest")
        if hashlib.sha256(r4input_raw).hexdigest() != manifest["corrected"]["input"]["sha256"]:
            errs.append("r4 input bytes drift vs manifest")
        r4supp = json.loads(r4supp_raw.decode("utf-8"))
        r4input = json.loads(r4input_raw.decode("utf-8"))
        if r4supp["supplement_id"] == new_id:
            errs.append("new supplement_id must differ from r4 draft id")
        with M["at"].current_stage_basis_override():
            accepted_discovery = M["disc"].validate_acceptance(repo, (repo / SRC_REL) / "discovery/discovery-accepted-v2.json")
            root_discovery_path = core.repo_local_path(repo, accepted_discovery["discovery_path"], "accepted Discovery JSONL")
            active = M["sc"].resolve_active_screening_acceptance(repo, state_path, live_impl)
            _sp = Path(active["path"])
            screening_path = _sp if _sp.is_absolute() else (repo / _sp)
            effective = M["sc"].resolve_effective_discovery_basis(
                repo, screening_path.parent / "package.json", live_impl,
                accepted_root_path=root_discovery_path)
        if "root_records" not in effective or not effective["root_records"]:
            errs.append("effective basis missing validated root_records")
        disc_recs, root_recs = effective.get("records", []), effective.get("root_records", [])
        if not disc_recs:
            errs.append("effective basis records empty")
        _ep = Path(effective["path"])
        effective_path = _ep if _ep.is_absolute() else (repo / _ep)
        ctx["screening_path"] = screening_path.resolve().relative_to(repo).as_posix()
        ctx["discovery_path"] = effective_path.resolve().relative_to(repo).as_posix()
        ctx["screening_path_abs"] = screening_path
        ctx["discovery_path_abs"] = effective_path
        errs.extend(_check_supplement_rows_stdlib(repo, r4supp["sources"], manifest["supplement30"], WSROOT))
        for s in r4supp["sources"]:
            if s["evidence_task_id"] != M["ev"].stable_task_id(ISSUE, s["discovery_id"]):
                errs.append(f"task_id mismatch (real function): {s['discovery_id']}")
            try:
                if s["source_class"] != M["ev"]._source_class(s["source_type"]):
                    errs.append(f"source_class mismatch (real function): {s['discovery_id']}")
            except ValueError as e:
                errs.append(f"source_type unsupported {s['discovery_id']}: {e}")
        if r4input.get("schema_version") != "2.0-rc1" or r4input.get("issue_id") != ISSUE:
            errs.append("corrected input identity mismatch")
        if len(r4input.get("records", [])) != 160 or len(r4input.get("completeness", {}).get("obligations", [])) != 15:
            errs.append("corrected input counts != 160/15")
        new_supp_rel = SRC_REL / f"external/evidence-supplement/evidence-authority-supplement-{new_id}.json"
        new_input_rel = SRC_REL / f"evidence/proposed-input/interactive-evidence-{new_id}.json"
        ctx["new_supplement_rel"] = new_supp_rel.as_posix()
        ctx["new_input_rel"] = new_input_rel.as_posix()
        for row in manifest["supplement30"]:
            if row["live"] is None:
                try:
                    _require_absent(repo, Path(row["raw_path"]))
                except ValueError as e:
                    errs.append(str(e))
        for rel in (new_supp_rel, new_input_rel):
            try:
                _require_absent(repo, rel)
            except ValueError as e:
                errs.append(str(e))
        profile = core.load_json(repo / (SRC_REL / "production-profile.json"))
        ctx["profile"] = profile
        ctx["screening_acc_path"] = ctx["screening_path_abs"]
        ctx["discovery_path_abs"] = ctx["discovery_path_abs"]
        ctx["disc_recs"] = disc_recs
        ctx["root_recs"] = root_recs
        ctx["r4supp"] = r4supp
        ctx["r4input"] = r4input
        ctx["r4supp_raw"] = r4supp_raw
        ctx["r4input_raw"] = r4input_raw
    except ValueError as e:
        errs.append(f"phase1 exception: {e}")
    if errs:
        raise ValueError("phase1 pre-validation FAILED (zero active writes performed):\n- " + "\n- ".join(errs[:25]))

    # ---- retention (packet-local, ancestors validated, created only after phase-1 gate) ----
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

    # ---- phase 2: exclusive writes ONLY (17 staged Raw + corrected input + NEW supplement) ----
    wsroot = WSROOT
    staged_raw = []
    pkt_by_sid = {r["supplement_source_id"]: (r.get("packet") or {}).get("path")
                  for r in manifest["supplement30"]}
    for s in ctx["r4supp"]["sources"]:
        if not s["raw_path"].startswith(f"{SRC_REL}/external/evidence-supplement/raw/sp17-"):
            continue
        dest_rel = Path(s["raw_path"])
        pkt_rel = pkt_by_sid.get(s["supplement_source_id"])
        if not pkt_rel:
            raise ValueError(f"no packet locator for {s['discovery_id']} (preserve staged set, STOP)")
        raw = (wsroot / pkt_rel).read_bytes()
        if hashlib.sha256(raw).hexdigest() != s["raw_sha256"] or len(raw) != s["byte_count"]:
            raise ValueError(f"packet re-read drift at stage time: {s['discovery_id']} (preserve staged set, STOP)")
        got = _stage_bytes_exclusive(repo / dest_rel, repo, raw)
        if got["sha256"] != s["raw_sha256"]:
            raise ValueError(f"staged SHA mismatch: {s['discovery_id']}")
        staged_raw.append({"rel": dest_rel.as_posix(), **got})
    journal.append({"step": "stage-17-raw", "count": len(staged_raw)})
    if len(staged_raw) != 17:
        raise ValueError(f"expected exactly 17 staged Raw, got {len(staged_raw)}")
    new_input_abs = repo / Path(ctx["new_input_rel"])
    got_input = _stage_bytes_exclusive(new_input_abs, repo, ctx["r4input_raw"])
    journal.append({"step": "stage-input", "rel": ctx["new_input_rel"], **got_input})
    # NEW supplement: exclusive stage of corrected schema bytes + schema gate + FULL existing
    # validator. Builder NOT used: it unlinks owned output on validation failure
    # (survey_evidence_v2.py: output_path.unlink(missing_ok=True)); here attempted
    # bytes are always preserved and equivalence is proven by the gates below.
    basis = {
        "source_root": SRC_REL.as_posix(),
        "discovery_path": ctx["discovery_path_abs"].resolve().relative_to(repo).as_posix(),
        "discovery_sha256": hashlib.sha256(ctx["discovery_path_abs"].read_bytes()).hexdigest(),
        "screening_acceptance_path": ctx["screening_acc_path"].resolve().relative_to(repo).as_posix(),
        "screening_acceptance_sha256": hashlib.sha256(ctx["screening_acc_path"].read_bytes()).hexdigest(),
    }
    payload = {"schema_version": "2.0-rc1", "supplement_id": new_id, "issue_id": ISSUE,
               "basis": basis, "sources": ctx["r4supp"]["sources"]}
    M["sg"].validate_instance(payload, repo / M["ev"].SUPPLEMENT_SCHEMA, label="Evidence Authority Supplement")
    supp_bytes = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    new_supp_abs = repo / Path(ctx["new_supplement_rel"])
    got_supp = _stage_bytes_exclusive(new_supp_abs, repo, supp_bytes)
    with M["at"].current_stage_basis_override():
        real_acc, _, real_disc = M["ev"].validate_screening_acceptance(
            repo, ctx["screening_acc_path"], ctx["discovery_path_abs"], ISSUE, ctx["live_implementation_sha"])
        M["ev"].validate_evidence_authority_supplement(
            repo, new_supp_abs, ctx["live_implementation_sha"],
            expected_issue_id=ISSUE, expected_source_root=(repo / SRC_REL).resolve(),
            expected_discovery_path=ctx["discovery_path_abs"],
            expected_screening_acceptance_path=ctx["screening_acc_path"],
            screening_acceptance=real_acc, discoveries=real_disc)
    journal.append({"step": "stage+validate-supplement", "rel": ctx["new_supplement_rel"], **got_supp})
    ctx["real_acc"], ctx["real_disc"] = real_acc, real_disc

    # ---- phase 3: package to RETAINED scratch (kept) + full input validation ----
    # Scratch path: absent required, NEVER pre-created (the API creates it; it
    # would also accept an existing empty dir, which we refuse as non-single-use).
    pkg_dir = ret_dir / f"pkg-{new_id}"
    _require_absent_under(WSROOT, pkg_dir)
    with M["at"].current_stage_basis_override():
        pkg_path = M["ev"].prepare_evidence_package(
            repo, state_path, ctx["discovery_path_abs"], ctx["screening_acc_path"],
            pkg_dir, ctx["live_implementation_sha"], new_supp_abs)
    if not pkg_dir.is_dir() or not pkg_path.is_file():
        raise ValueError("package scratch not materialized by API (STOP, preserve)")
    package = _strict_json(pkg_path)
    task_meta = {m["discovery_ids"][0]: m for m in package["tasks"]}
    expected_ids = set(task_meta)
    with M["at"].current_stage_basis_override():
        run_screening, _, run_discs = M["ev"].validate_screening_acceptance(
            repo, ctx["screening_acc_path"], ctx["discovery_path_abs"], ISSUE, ctx["live_implementation_sha"])
        run_ctx = M["ev"]._resolve_phase_supplement_context(
            repo, package, implementation_sha=ctx["live_implementation_sha"],
            screening_acceptance=run_screening, discoveries=run_discs)
        run_pins = M["ev"]._capture_phase_pins(
            (("Evidence package", pkg_path),)
            + tuple((f"Evidence Task {m['evidence_task_id']}", pkg_path.parent / m["path"]) for m in package["tasks"]))
    ctx["run_ctx"], ctx["run_pins"], ctx["package"], ctx["pkg_path"] = run_ctx, run_pins, package, pkg_path
    task_source_ids: dict[str, set[str]] = {}
    for did, meta in task_meta.items():
        task = _strict_json(pkg_path.parent / meta["path"])
        base = M["ev"]._discovery_task_sources(task)
        task_source_ids[did] = set(M["ev"]._merge_supplement_task_sources(base, task, run_ctx["entries"]))
    doc = _strict_json(new_input_abs)
    by_id, runner, _ = M["rn"].validate_interactive_input(
        doc, ctx["profile"], expected_ids, task_source_ids,
        discovery_records=ctx["disc_recs"], root_discovery_records=ctx["root_recs"])
    journal.append({"step": "package+validate-input", "pkg_dir": pkg_dir.name,
                    "tasks": len(task_meta), "records": len(by_id), "runner": runner})

    # ---- phase 4: terminal recheck (FULL) + retained-authority close + READY ----
    live_files4, live_dirs4, walk_errs4 = _walk_sp_tree_stdlib(repo, SRC_REL)
    if walk_errs4:
        raise ValueError("terminal SP walk FAILED:\n- " + "\n- ".join(walk_errs4[:10]))
    exp_files = {e["rel"]: e for e in manifest["sp_tree_full"]["files"]}
    exp_dirs = {e["rel"] for e in manifest["sp_tree_full"]["dirs"]}
    allowed_new = {r["rel"] for r in staged_raw} | {ctx["new_input_rel"], ctx["new_supplement_rel"]}
    merged_files = dict(exp_files)
    for r in staged_raw:
        merged_files[r["rel"]] = {"sha256": r["sha256"], "bytes": r["bytes"], "mode": "0o664", "nlink": 1}
    merged_files[ctx["new_input_rel"]] = {"sha256": got_input["sha256"], "bytes": got_input["bytes"], "mode": "0o664", "nlink": 1}
    merged_files[ctx["new_supplement_rel"]] = {"sha256": got_supp["sha256"], "bytes": got_supp["bytes"], "mode": "0o664", "nlink": 1}
    term_errs = _compare_sp_tree(live_files4, live_dirs4, merged_files, exp_dirs)
    if term_errs:
        raise ValueError("terminal SP tree FAILED (preserve, STOP):\n- " + "\n- ".join(term_errs[:10]))
    term_errs.extend(_check_intended_tree_stdlib(repo, manifest["delivery"]["intended"], manifest["delivery"]["test_pin"]))
    term_errs.extend(_check_gates_absent(repo))
    term_errs.extend(_scan_ledger_refs(repo, manifest["stage_ledger_ref_scan"]))
    if term_errs:
        raise ValueError("terminal recheck FAILED (preserve, STOP):\n- " + "\n- ".join(term_errs[:10]))
    for s in ctx["r4supp"]["sources"]:
        if s["raw_path"].startswith(f"{SRC_REL}/external/evidence-supplement/raw/supp-"):
            _pin_live(repo, Path(s["raw_path"]), {"sha256": s["raw_sha256"], "bytes": s["byte_count"]}, mode="0o664")
    if hashlib.sha256((repo / (SRC_REL / "production-state.json")).read_bytes()).hexdigest() != manifest["original_authority"]["state"]["sha256"]:
        raise ValueError("State bytes changed during prepare (STOP, preserve)")
    _strict_state_and_ready(repo, M, manifest)  # POST
    with M["at"].current_stage_basis_override():
        M["ev"]._finish_authority_phase(
            repo, ctx["run_ctx"], ctx["run_pins"],
            revalidate_owner=lambda: M["ev"].validate_evidence_package_basis(
                repo, ctx["pkg_path"], ctx["package"], ctx["live_implementation_sha"]))
    journal.append({"step": "finish-authority-phase", "result": "pass"})
    if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != manifest["_self_sha256"]:
        raise ValueError("expected manifest changed mid-run (refuse READY; same-hash recheck failed)")
    ready = {
        "ready": True, "stage": "prepare-only", "no_removal": True, "no_retry": True,
        "manifest": {"path": manifest_path.name, "sha256": manifest["_self_sha256"]},
        "live_implementation_sha": ctx["live_implementation_sha"],
        "historical_implementation_sha": HIST_IMPL,
        "supplement_id": new_id,
        "new_supplement": {**{"rel": ctx["new_supplement_rel"]}, **got_supp},
        "new_input": {**{"rel": ctx["new_input_rel"]}, **got_input},
        "staged_raw": staged_raw,
        "module_roots": M["roots"],
        "module_pre_sha": ctx["pre_module_sha"],
        "state_sha": manifest["original_authority"]["state"]["sha256"],
        "profile_sha": manifest["original_authority"]["profile"]["sha256"],
        "discovery_sha": manifest["original_authority"]["dcp_jsonl"]["sha256"],
        "screening_sha": manifest["original_authority"]["scp_accepted"]["sha256"],
        "ledger_sha": manifest["original_authority"]["ledger"]["sha256"],
        "completeness_sha": manifest["original_authority"]["completeness"]["sha256"],
        "test_pin": manifest["delivery"]["test_pin"],
        "intended_count": len(manifest["delivery"]["intended"]),
        "sp_tree_counts": {"files": len(live_files4), "dirs": len(live_dirs4)},
        "task_count": len(task_meta),
        "input_records": len(by_id),
        "retained_pkg_dir": pkg_dir.name,
        "package_json_sha": hashlib.sha256(pkg_path.read_bytes()).hexdigest(),
        "journal": journal,
    }
    rp = ret_dir / "READY.json"
    _stage_bytes_exclusive_local(rp, (json.dumps(ready, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    _stage_bytes_exclusive_local(ret_dir / "journal.json",
                                 (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"ready": str(rp), "tasks": len(task_meta), "records": len(by_id)}


def main() -> int:
    global REPO_ROOT
    ap = argparse.ArgumentParser(description="SP PREPARE-ONLY r6 (review only, do not run yet)")
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--new-supplement-id", type=str, required=True)
    ap.add_argument("--manifest", type=Path, default=GEN_MANIFEST)
    ap.add_argument("--expected-manifest-sha", type=str, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    a = ap.parse_args()
    REPO_ROOT = a.repo_root
    try:
        out = stage_prepare(a.retention_dir, a.new_supplement_id, a.manifest, a.expected_manifest_sha)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        try:
            rd = a.retention_dir
            if rd.is_dir() and not os.path.islink(rd):
                partials = sorted(p.relative_to(rd).as_posix() for p in rd.rglob("*") if p.is_file())
                _stage_bytes_exclusive_local(
                    rd / "FAILURE.json",
                    (json.dumps({"stage": "prepare-only", "exit": 2, "error": str(exc)[:4000],
                                 "retained_partials": partials}, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        except OSError:
            pass  # best-effort only; original refusal propagates via return 2
        print(f"PREPARE_REFUSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"stage": "prepare-only", "exit": 0, **out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
