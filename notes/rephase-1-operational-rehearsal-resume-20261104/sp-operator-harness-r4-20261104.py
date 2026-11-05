#!/usr/bin/env python3
"""SP single-use operator harness r4 — SOURCE REVIEW ONLY, DO NOT EXECUTE YET.

Replaces rejected r3 execution authority (r3 preserved untouched, never run).
SP-efficient-llm-2026 owned-unaccepted Ledger/Completeness recovery ONLY.
No shipping source changes; all new files stay under the resume packet.

Fixed vs r3 (root rejection): real Path.mkdir(exist_ok=False) exclusive
(no nonexistent exclusive=True); true O_EXCL|O_NOFOLLOW backup/staging
(no check-then-copy2 claimed exclusive); no ineffective pass branch (real
stable_task_id/_source_class + coverage/binding enforcement); exact State
keys (lifecycle_state, 12 machine_checkpoints, null provenances) plus real
validate_agent_state + require_research_operation_ready before every removal;
phase-specific expected inventories (pre-2a both present / pre-2b ledger
absent EXPECTED / post-both absent, no reseal); restricted paths/ancestors,
State/CP/Human/products/source invariance, no blanket-prefix mutation.

Stages: --stage=prepare (packet P1 + active P2 staging/build/FULL
Raw-present validation -> READY, STOPS; no canonical removal) and
--stage=dispose (requires READY + explicit Root auth file; guarded backup
then exact2 unlink, no retry here). Retry is a SEPARATE Root decision using
the existing run() API (see operation note); this harness never auto-retries
or restores.
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
SRC_REL = Path("sources/SP-efficient-llm-2026")
SRC = REPO_ROOT / SRC_REL
ISSUE = "SP-efficient-llm-2026"
IMPL = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
PIN_EVID = "487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a"
PIN_RUN = "5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543"
PIN_LOW = "0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b"
LEDGER_REL = SRC_REL / "materiality-ledger-v2.json"
LEDGER_SHA = "ee13b8ee5626ea0e7198d85aa0fddf6bcadb42679d11621834f6c97ee8ab796d"
LEDGER_N = 66865
COMP_REL = SRC_REL / "profile-completeness-v2.json"
COMP_SHA = "c60a96242a5157ebd7c3509cf1500f45deb277c4c9854343cf2a5f790a106c86"
COMP_N = 32511
STATE_REL = SRC_REL / "production-state.json"
STATE_SHA = "4865998b99ab2902954619b2a7761c4ae0de77695b06ddd5b5e25d49dff4eb89"
STATE_N = 3454
PROF_REL = SRC_REL / "production-profile.json"
PROF_SHA = "aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45"
DISC_REL = SRC_REL / "discovery/discovery-v2.jsonl"
SCRN_REL = SRC_REL / "screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json"
RESUME = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")
R2_INPUT = RESUME / "sp-corrected-input-r2-20261104.json"
R2_SUPP = RESUME / "sp-corrected-supplement-r2-20261104.json"


def _hex64(v: str, label: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", v or ""):
        raise ValueError(f"malformed SHA (must be 64 hex): {label}={v!r}")


def _strict_json(path: Path) -> dict:
    raw = path.read_bytes()
    def _hook(pairs):
        o = {}
        for k, v in pairs:
            if k in o:
                raise ValueError(f"duplicate JSON key refused: {k!r} in {path}")
            o[k] = v
        return o
    val = json.loads(raw.decode("utf-8"), object_pairs_hook=_hook)
    if not isinstance(val, dict):
        raise ValueError(f"expected JSON object: {path}")
    return val


def _no_symlink_parents(repo_root: Path, rel: Path) -> None:
    cur = repo_root
    for part in rel.parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink ancestor forbidden: {cur}")
    abs_p = repo_root / rel
    try:
        abs_p.resolve().relative_to(repo_root.resolve())
    except ValueError:
        raise ValueError(f"path escapes repo_root: {rel}")


def _require_file(repo_root: Path, rel: Path, sha: str, n: int) -> Path:
    _hex64(sha, str(rel))
    _no_symlink_parents(repo_root, rel)
    abs_p = repo_root / rel
    if os.path.islink(abs_p) or not abs_p.is_file():
        raise ValueError(f"missing/unsafe regular file: {rel}")
    st = os.lstat(abs_p)
    if not stat.S_ISREG(st.st_mode) or oct(st.st_mode & 0o777) != "0o664" or st.st_nlink != 1:
        raise ValueError(f"identity/mode/nlink drift: {rel} mode={oct(st.st_mode & 0o777)} nlink={st.st_nlink}")
    data = abs_p.read_bytes()
    if len(data) != n or hashlib.sha256(data).hexdigest() != sha:
        raise ValueError(f"bytes/SHA drift: {rel}")
    return abs_p


def _require_absent(repo_root: Path, rel: Path) -> None:
    abs_p = repo_root / rel
    if os.path.islink(abs_p) or abs_p.exists():
        raise ValueError(f"must be absent (no symlink, no file): {rel}")


def _excl_write(dest: Path, data: bytes) -> Path:
    if os.path.islink(dest) or dest.exists():
        raise ValueError(f"refusing overwrite (must be absent): {dest}")
    parent = dest.parent
    if os.path.islink(parent) or not parent.is_dir():
        raise ValueError(f"unsafe/absent parent: {parent}")
    fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o664)
    try:
        view = memoryview(data)
        while view:
            w = os.write(fd, view)
            view = view[w:]
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(dest, 0o664)
    st = os.lstat(dest)
    if not stat.S_ISREG(st.st_mode) or os.path.islink(dest) or oct(st.st_mode & 0o777) != "0o664":
        raise ValueError(f"exclusive write identity failed: {dest}")
    back = dest.read_bytes()
    if back != data:
        raise ValueError(f"exclusive write bytes mismatch: {dest}")
    return dest


def _invariance() -> dict:
    sys.path.insert(0, str(REPO_ROOT))
    from scripts import survey_evidence_v2 as ev, run_evidence_v2_interactive as rn, survey_research_authority_v2 as lw  # noqa: E402
    mods = {"survey_evidence_v2": (ev, PIN_EVID), "run_evidence_v2_interactive": (rn, PIN_RUN), "survey_research_authority_v2": (lw, PIN_LOW)}
    roots = {}
    for name, (mod, pin) in mods.items():
        f = Path(mod.__file__)
        if REPO_ROOT.resolve() not in f.resolve().parents:
            raise ValueError(f"module root outside e84: {name} -> {f}")
        if hashlib.sha256(f.read_bytes()).hexdigest() != pin:
            raise ValueError(f"source invariance failed: {name}")
        roots[name] = str(f)
    if list((REPO_ROOT / "scripts").rglob("__pycache__")):
        raise ValueError("__pycache__ present in active source (refuse)")
    return roots


def _state_cand() -> tuple[dict, dict, Path, Path]:
    sys.path.insert(0, str(REPO_ROOT))
    from scripts import survey_agent_control_v2 as agent  # noqa: E402
    from scripts import survey_production_v2 as core  # noqa: E402
    from scripts import survey_research_authority_v2 as low  # noqa: E402
    cfg = core.load_json(REPO_ROOT / core.DEFAULT_CONFIG)
    state = _strict_json(REPO_ROOT / STATE_REL)
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
    if state.get("implementation", {}).get("repository_commit_sha") != IMPL:
        raise ValueError("State drift: implementation SHA must be 48082356")
    if state.get("profile", {}).get("sha256") != PROF_SHA:
        raise ValueError("State drift: profile SHA must be aff05fd5")
    errs = agent.validate_agent_state(REPO_ROOT, cfg, state)
    if errs:
        raise ValueError("strict agent State invalid: " + "; ".join(errs))
    low.require_research_operation_ready(REPO_ROOT, REPO_ROOT / STATE_REL)
    return cfg, state, REPO_ROOT / STATE_REL, REPO_ROOT / PROF_REL


RETAINED = [STATE_REL, PROF_REL, DISC_REL, SRC_REL / "discovery/discovery-accepted-v2.json", SCRN_REL,
    SRC_REL / "evidence/proposed-input/interactive-evidence.json",
    SRC_REL / "external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json",
    SRC_REL / "evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/evidence-accepted.json",
    SRC_REL / "evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/package.json",
    SRC_REL / "evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/interactive-audit.json",
    SRC_REL / "evidence/v2/views/accepted/50c919b93436eae63db156d78134e167e7651c167912de1ae7a02a5bc8503a39/edition-views-accepted.json",
    LEDGER_REL, COMP_REL]


def _no_unexpected(extra_ok: set[str]) -> None:
    for p in (REPO_ROOT / SRC_REL).rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        rel = (p.relative_to(REPO_ROOT)).as_posix()
        if rel in {r.as_posix() for r in RETAINED} or rel in extra_ok:
            continue
        if rel.startswith("sources/SP-efficient-llm-2026/orchestration/"):
            continue
        if rel.startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-"):
            continue
        if rel.startswith("sources/SP-efficient-llm-2026/screening/") or rel.startswith("sources/SP-efficient-llm-2026/discovery/"):
            continue
        raise ValueError(f"unexpected addition (preserve, STOP): {rel}")


def stage_prepare(ret_dir: Path, new_id: str, map_file: Path) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}", new_id or ""):
        raise ValueError(f"bad supplement_id: {new_id!r}")
    if RESUME not in ret_dir.resolve().parents:
        raise ValueError("retention must be packet-local under resume packet")
    try:
        ret_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise ValueError(f"single-use refuse: retention exists: {ret_dir}")
    (ret_dir / "raw").mkdir(exist_ok=False)
    roots = _invariance()
    _require_file(REPO_ROOT, STATE_REL, STATE_SHA, STATE_N)
    _require_file(REPO_ROOT, LEDGER_REL, LEDGER_SHA, LEDGER_N)
    _require_file(REPO_ROOT, COMP_REL, COMP_SHA, COMP_N)
    cfg, state, state_path, profile_path = _state_cand()
    _no_unexpected(set())
    _excl_write(ret_dir / "historical-context.json", (json.dumps({"state_sha": STATE_SHA, "issue": ISSUE, "impl": IMPL, "module_roots": roots}, indent=2) + "\n").encode())
    sys.path.insert(0, str(REPO_ROOT))
    from scripts import survey_evidence_v2 as ev  # noqa: E402
    from scripts import run_evidence_v2_interactive as rn  # noqa: E402
    from scripts import survey_agent_tool_v2 as at  # noqa: E402
    from scripts import survey_screening_v2 as sc  # noqa: E402
    rows = json.loads(Path(map_file).read_text())["staging_rows"]
    if len(rows) != 17:
        raise ValueError("staging map must have exactly 17 rows")
    r2supp = json.loads(R2_SUPP.read_text())
    by_sid = {s["supplement_source_id"]: s for s in r2supp["sources"]}
    for row in rows:  # every row enforced; malformed hex refuses (no silent skip)
        _hex64(row["sha256"], str(row["dest_active_rel"]))
        s = by_sid.get(row["supplement_source_id"])
        if s is None or s["raw_path"] != row["dest_active_rel"] or s["raw_sha256"] != row["sha256"] or s["byte_count"] != row["bytes"] or s["discovery_id"] != row["did"] or s["evidence_task_id"] != row["evidence_task_id"]:
            raise ValueError(f"staging row mismatches r2 supplement (no guessing): {row}")
        if row["did"] == "EFF-D123":
            raise ValueError("BLOCKED row EFF-D123: r2 pin 65-char malformed; corrected row + re-review required before prepare")
        dest_rel = Path(row["dest_active_rel"])
        if dest_rel.parts[:2] != ("sources", "SP-efficient-llm-2026"):
            raise ValueError(f"dest escapes SP source_root: {dest_rel}")
        src = Path(row["src_packet_data"])
        if not src.is_absolute():
            src = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey") / src
        if os.path.islink(src) or not src.is_file():
            raise ValueError(f"unsafe packet source: {src}")
        raw = src.read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError(f"packet source SHA/bytes mismatch: {src}")
        _require_absent(REPO_ROOT, dest_rel)
        _excl_write(REPO_ROOT / dest_rel, raw)
    for r in rows:  # post-stage presence pinned (sp17 set now expected)
        _require_file(REPO_ROOT, Path(r["dest_active_rel"]), r["sha256"], r["bytes"])
    new_supp_rel = SRC_REL / f"external/evidence-supplement/evidence-authority-supplement-{new_id}.json"
    _require_absent(REPO_ROOT, new_supp_rel)
    with at.current_stage_basis_override():
        new_supp = ev.build_evidence_authority_supplement(repo_root=REPO_ROOT, issue_id=ISSUE, source_root=SRC, discovery_path=REPO_ROOT / DISC_REL, screening_acceptance_path=REPO_ROOT / SCRN_REL, sources=r2supp["sources"], output_path=REPO_ROOT / new_supp_rel, supplement_id=new_id, implementation_sha=IMPL)
    active = sc.resolve_active_screening_acceptance(REPO_ROOT, state_path, IMPL)
    eff = sc.resolve_effective_discovery_basis(REPO_ROOT, Path(active["path"]).parent / "package.json", IMPL)
    # Real screening acceptance + discoveries via canonical validator (no fabricated lists).
    with at.current_stage_basis_override():
        real_acc, _, real_disc = ev.validate_screening_acceptance(REPO_ROOT, REPO_ROOT / SCRN_REL, REPO_ROOT / DISC_REL, ISSUE, IMPL)
    ev.validate_evidence_authority_supplement(repo_root=REPO_ROOT, supplement_path=new_supp, implementation_sha=IMPL, expected_issue_id=ISSUE, expected_source_root=SRC, expected_discovery_path=REPO_ROOT / DISC_REL, expected_screening_acceptance_path=REPO_ROOT / SCRN_REL, screening_acceptance=real_acc, discoveries=real_disc)
    r2input = json.loads(R2_INPUT.read_text())
    new_in_rel = SRC_REL / f"evidence/proposed-input/interactive-evidence-{new_id}.json"
    _require_absent(REPO_ROOT, new_in_rel)
    _excl_write(REPO_ROOT / new_in_rel, (json.dumps(r2input, ensure_ascii=False, indent=2) + "\n").encode())
    profile = _strict_json(REPO_ROOT / PROF_REL)
    doc = _strict_json(REPO_ROOT / new_in_rel)
    import tempfile  # noqa: E402
    with tempfile.TemporaryDirectory() as tmp:
        with at.current_stage_basis_override():
            pkg_path = ev.prepare_evidence_package(REPO_ROOT, state_path, REPO_ROOT / DISC_REL, REPO_ROOT / SCRN_REL, Path(tmp) / "pkg", IMPL, new_supp)
        pkg = _strict_json(pkg_path)
        expected_ids = {m["discovery_ids"][0] for m in pkg["tasks"]}
        root_recs, eff_recs = eff["root_records"], eff["records"]
        with at.current_stage_basis_override():
            ctx = ev._resolve_phase_supplement_context(REPO_ROOT, pkg, implementation_sha=IMPL, screening_acceptance=real_acc, discoveries=real_disc)
        pins = ev._capture_phase_pins(tuple([("Evidence package", pkg_path)] + [(f"Evidence Task {m['evidence_task_id']}", pkg_path.parent / m["path"]) for m in pkg["tasks"]]))
        tids: dict[str, set[str]] = {}
        for did, meta in {m["discovery_ids"][0]: m for m in pkg["tasks"]}.items():
            task = _strict_json(pkg_path.parent / meta["path"])
            tids[did] = set(ev._merge_supplement_task_sources(ev._discovery_task_sources(task), task, ctx["entries"]))
        by_id, runner, _ = rn.validate_interactive_input(doc, profile, expected_ids, tids, discovery_records=eff_recs, root_discovery_records=root_recs)
        for did in sorted({m["discovery_ids"][0] for m in pkg["tasks"]}):
            meta = next(m for m in pkg["tasks"] if m["discovery_ids"][0] == did)
            task = _strict_json(pkg_path.parent / meta["path"])
            auth = ev._merge_supplement_task_sources(ev._discovery_task_sources(task), task, ctx["entries"])
            card = ev._build_card_core(task, meta, pkg, by_id[did], runner, auth)
            errs = ev._validate_card_core(card, task, meta["sha256"], pkg, lambda _t=task: ev._merge_supplement_task_sources(ev._discovery_task_sources(_t), _t, ctx["entries"]))
            if errs:
                raise ValueError(f"card invalid {did}: {'; '.join(errs)}")
            view = rn._build_view(profile, meta["evidence_task_id"], card["sha256"] if "sha256" in card else meta["sha256"], by_id[did])
            verrs = ev.validate_edition_view(view, profile, view["evidence_sha256"], by_id[did]["status"])
            if verrs:
                raise ValueError(f"view invalid {did}: {'; '.join(verrs)}")
        for s in ev._load_pinned_json(ev._capture_phase_pins((("New supplement", new_supp),))[0])["sources"]:
            if s["evidence_task_id"] != ev.stable_task_id(ISSUE, s["discovery_id"]):
                raise ValueError(f"task_id mismatch (real function): {s['discovery_id']}")
            if s["source_class"] != ev._source_class(s["source_type"]):
                raise ValueError(f"source_class mismatch (real function): {s['discovery_id']}")
    ready = {"ready": True, "new_supplement": new_supp_rel.as_posix(), "new_supplement_sha": hashlib.sha256((REPO_ROOT / new_supp_rel).read_bytes()).hexdigest(), "new_input": new_in_rel.as_posix(), "new_input_sha": hashlib.sha256((REPO_ROOT / new_in_rel).read_bytes()).hexdigest(), "module_roots": roots, "state_sha": STATE_SHA, "task_count": len(expected_ids)}
    rp = _excl_write(ret_dir / "READY.json", (json.dumps(ready, indent=2) + "\n").encode())
    return rp


def stage_dispose(ret_dir: Path, auth_file: Path) -> None:
    if not (ret_dir / "READY.json").is_file():
        raise ValueError("REFUSE: READY barrier not passed")
    if not auth_file.is_file():
        raise ValueError("REFUSE: Root auth file required (existence is permission, not semantic PASS)")
    ready = json.loads((ret_dir / "READY.json").read_text())
    _invariance()
    for rel, sha, n in [(LEDGER_REL, LEDGER_SHA, LEDGER_N), (COMP_REL, COMP_SHA, COMP_N)]:
        _require_file(REPO_ROOT, rel, sha, n)
    _state_cand()
    staged = {r["dest_active_rel"] for r in json.loads((RESUME / "sp-staging-expected-manifest-r4-20261104.json").read_text())["staging_rows"]}
    _no_unexpected({ready["new_supplement"], ready["new_input"]} | staged)
    man = {"ledger": {"old": LEDGER_REL.as_posix(), "new": "materiality-ledger-v2.json", "sha": LEDGER_SHA, "bytes": LEDGER_N, "mode": "0o664", "state": STATE_SHA}, "completeness": {"old": COMP_REL.as_posix(), "new": "profile-completeness-v2.json", "sha": COMP_SHA, "bytes": COMP_N, "mode": "0o664", "state": STATE_SHA}}
    for key, rel, sha in [("ledger", LEDGER_REL, LEDGER_SHA), ("completeness", COMP_REL, COMP_SHA)]:
        _excl_write(ret_dir / man[key]["new"], (REPO_ROOT / rel).read_bytes())
        if hashlib.sha256((ret_dir / man[key]["new"]).read_bytes()).hexdigest() != sha:
            raise ValueError(f"backup SHA mismatch (preserve partials, STOP, no restore): {key}")
    _excl_write(ret_dir / "retention-manifest.json", (json.dumps(man, indent=2) + "\n").encode())
    _require_file(REPO_ROOT, LEDGER_REL, LEDGER_SHA, LEDGER_N)
    _require_file(REPO_ROOT, COMP_REL, COMP_SHA, COMP_N)
    _state_cand()
    os.unlink(REPO_ROOT / LEDGER_REL)
    _require_absent(REPO_ROOT, LEDGER_REL)
    if hashlib.sha256((ret_dir / "materiality-ledger-v2.json").read_bytes()).hexdigest() != LEDGER_SHA:
        raise ValueError("retention Ledger drift after 2a (preserve partials, STOP, no restore)")
    _require_absent(REPO_ROOT, LEDGER_REL)
    _require_file(REPO_ROOT, COMP_REL, COMP_SHA, COMP_N)
    _state_cand()
    os.unlink(REPO_ROOT / COMP_REL)
    _require_absent(REPO_ROOT, LEDGER_REL)
    _require_absent(REPO_ROOT, COMP_REL)


def main() -> int:
    ap = argparse.ArgumentParser(description="SP single-use r4 harness (review only, do not run yet)")
    ap.add_argument("--stage", choices=["prepare", "dispose"], required=True)
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--new-supplement-id", type=str, default="")
    ap.add_argument("--staging-map-file", type=Path, default=None)
    ap.add_argument("--root-auth-file", type=Path, default=None)
    a = ap.parse_args()
    if a.stage == "prepare":
        if not a.new_supplement_id or a.staging_map_file is None:
            print("REFUSE: --new-supplement-id + --staging-map-file required", file=sys.stderr)
            return 2
        rp = stage_prepare(a.retention_dir, a.new_supplement_id, a.staging_map_file)
        print(json.dumps({"stage": "prepare", "ready": str(rp), "exit": 0}, indent=2))
        return 0
    if a.root_auth_file is None:
        print("REFUSE: --root-auth-file required for dispose", file=sys.stderr)
        return 2
    stage_dispose(a.retention_dir, a.root_auth_file)
    print(json.dumps({"stage": "dispose", "retention": str(a.retention_dir), "exit": 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
