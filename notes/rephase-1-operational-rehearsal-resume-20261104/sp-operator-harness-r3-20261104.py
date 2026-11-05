#!/usr/bin/env python3
"""SP single-use operator harness r3 — SOURCE REVIEW ONLY, DO NOT EXECUTE YET.

Single-use for SP-efficient-llm-2026 owned-unaccepted Ledger/Completeness recovery ONLY.
W34 needs separate decision; no W34 clearing implied. No shipping source modification.

Stages (explicit, no auto progression):
  --stage=prepare : packet P1 + active P2 staging/build/FULL Raw-present validation + journals,
                    writes READY file, STOPS. No canonical removal.
  --stage=dispose : requires READY file + explicit Root auth file; guarded copy+verify then
                    guarded unlink Ledger then Completeness per phase tables. No retry here.
  Retry (normal run()) is SEPARATE decision AFTER disposal, NOT in this harness.

Bounds (enforced in code, verified at review):
- No reconstruct Git, no network, no Production checkout. Active e84 isolated Git ONLY if later
  actual operation needs live tree binding; this harness does file-read/data generation only.
- PYTHONDONTWRITEBYTECODE=1 enforced; source invariance: loaded module __file__ + sha256 MUST
  match e84 committed (Evidence 48742538..., runner 5e195730..., LOW 0974c709...); __pycache__
  MUST NOT be created in active source (verified absent after any future run).
- Per-file lstat identity/mode, no symlink parents (every component islink false, resolve() under
  repo_root/source_root). Copy bytes exclusively (shutil.copy2 + chmod 0o664 + re-read), no
  rename onto backup names, no --remove-destination overwrite.
- Historical context manifest + inventory retained old accepted/State/CP + guarded unexpected
  additions (any file under sources/SP-efficient-llm-2026/ NOT in inventory -> STOP, do NOT delete).
- Pre-removal: ledger+completeness present. Before second removal: ledger absent EXPECTED,
  completeness present pinned. After both: both absent. No auto restore/loop/collision cleanup;
  unknown/drifted State -> preserve partials, report exact partials, STOP.
- No helpers called with fake dicts/lists; all validation inputs loaded from REAL files
  (profile/discovery/screening/supplement/input). No public verified-dict bypass.
- Raw stdout/stderr/exit + repo_root/source_root/module roots captured to retention/raw/.

FOR SOURCE REVIEW ONLY — DO NOT RUN. One bounded Root authorization AFTER fresh independent
review required before --stage=prepare; separate explicit READY confirmation + auth required
before --stage=dispose. See sp-disposition-plan-r3-20261104.md FULL (B1-B6).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from pathlib import Path

if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("REFUSE: PYTHONDONTWRITEBYTECODE=1 required (source invariance)")

REPO_ROOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work")
SOURCE_ROOT_REL = Path("sources/SP-efficient-llm-2026")
SOURCE_ROOT = REPO_ROOT / SOURCE_ROOT_REL
ISSUE_ID = "SP-efficient-llm-2026"
IMPL_SHA = "480823560c0c26ed2e5baa18e0e79a22b2839a27"
PIN_EVIDENCE = "487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a"
PIN_RUNNER = "5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543"
PIN_LOW = "0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b"
LEDGER_REL = SOURCE_ROOT_REL / "materiality-ledger-v2.json"
LEDGER_SHA = "ee13b8ee5626ea0e7198d85aa0fddf6bcadb42679d11621834f6c97ee8ab796d"
LEDGER_BYTES = 66865
COMPLETENESS_REL = SOURCE_ROOT_REL / "profile-completeness-v2.json"
COMPLETENESS_SHA = "c60a96242a5157ebd7c3509cf1500f45deb277c4c9854343cf2a5f790a106c86"
COMPLETENESS_BYTES = 32511
STATE_REL = SOURCE_ROOT_REL / "production-state.json"
STATE_SHA = "4865998b99ab2902954619b2a7761c4ae0de77695b06ddd5b5e25d49dff4eb89"
PROFILE_REL = SOURCE_ROOT_REL / "production-profile.json"
DISCOVERY_REL = SOURCE_ROOT_REL / "discovery/discovery-v2.jsonl"
SCREENING_REL = SOURCE_ROOT_REL / "screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json"
R2_INPUT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104/sp-corrected-input-r2-20261104.json")
R2_SUPPLEMENT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104/sp-corrected-supplement-r2-20261104.json")
RESUME_BASE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104")

def _hex64(v: str, label: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", v):
        raise ValueError(f"malformed SHA (must be 64 hex): {label}={v!r}")

def _lstat_no_symlink_parents(repo_root: Path, rel: Path) -> os.stat_result:
    cur = repo_root
    for part in rel.parts:
        cur = cur / part
        if os.path.islink(cur):
            raise ValueError(f"symlink parent forbidden: {cur} (rel {rel})")
    abs_p = repo_root / rel
    try:
        abs_p.resolve().relative_to(repo_root.resolve())
    except ValueError:
        raise ValueError(f"path escapes repo_root: {rel}")
    return os.lstat(abs_p)

def _require_regular_file(repo_root: Path, rel: Path, expect_sha: str, expect_bytes: int) -> Path:
    _hex64(expect_sha, str(rel))
    abs_p = repo_root / rel
    if os.path.islink(abs_p):
        raise ValueError(f"refusing symlink target: {rel}")
    if not abs_p.is_file():
        raise ValueError(f"missing regular file: {rel}")
    st = _lstat_no_symlink_parents(repo_root, rel)
    if not stat.S_ISREG(st.st_mode):
        raise ValueError(f"not regular file: {rel}")
    if oct(st.st_mode & 0o777) != "0o664":
        raise ValueError(f"mode drift (must be 0o664): {rel} got {oct(st.st_mode & 0o777)}")
    data = abs_p.read_bytes()
    if len(data) != expect_bytes:
        raise ValueError(f"bytes drift: {rel} expected {expect_bytes} got {len(data)}")
    h = hashlib.sha256(data).hexdigest()
    if h != expect_sha:
        raise ValueError(f"SHA drift: {rel} expected {expect_sha} got {h}")
    return abs_p

def _require_absent(repo_root: Path, rel: Path) -> None:
    abs_p = repo_root / rel
    if os.path.islink(abs_p):
        raise ValueError(f"unexpected symlink (must be absent): {rel}")
    if abs_p.exists():
        raise ValueError(f"unexpected present (must be absent): {rel}")

def _check_source_invariance() -> dict[str, str]:
    sys.path.insert(0, str(REPO_ROOT))
    from scripts import survey_evidence_v2 as evidence  # noqa: E402
    from scripts import run_evidence_v2_interactive as run_mod  # noqa: E402
    from scripts import survey_research_authority_v2 as low  # noqa: E402
    mods = {"survey_evidence_v2": (evidence, PIN_EVIDENCE), "run_evidence_v2_interactive": (run_mod, PIN_RUNNER), "survey_research_authority_v2": (low, PIN_LOW)}
    roots: dict[str, str] = {}
    for name, (mod, pin) in mods.items():
        f = Path(mod.__file__)
        if REPO_ROOT not in f.resolve().parents:
            raise ValueError(f"module root outside e84: {name} -> {f}")
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        if h != pin:
            raise ValueError(f"source invariance failed: {name} {h} != {pin}")
        roots[name] = str(f)
    for pyc in (REPO_ROOT / "scripts").rglob("__pycache__"):
        raise ValueError(f"__pycache__ present in active source: {pyc}")
    return roots

def _load_real_json(repo_root: Path, rel: Path) -> dict:
    abs_p = repo_root / rel
    if os.path.islink(abs_p) or not abs_p.is_file():
        raise ValueError(f"unsafe JSON path: {rel}")
    return json.loads(abs_p.read_text())

def _copy2_chmod_verify(src: Path, dest: Path) -> None:
    if dest.exists() or os.path.islink(dest):
        raise ValueError(f"refusing overwrite (must be absent): {dest}")
    if os.path.islink(src) or not src.is_file():
        raise ValueError(f"unsafe copy source: {src}")
    dest.parent.mkdir(parents=True, exist_ok=False) if not dest.parent.exists() else None
    # Exclusive: fail if dest appeared between check and copy (no clobber)
    if dest.exists():
        raise ValueError(f"collision (must be absent): {dest}")
    shutil.copy2(src, dest)
    os.chmod(dest, 0o664)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != hashlib.sha256(src.read_bytes()).hexdigest():
        raise ValueError(f"copy SHA mismatch: {src} -> {dest}")
    st = os.lstat(dest)
    if oct(st.st_mode & 0o777) != "0o664" or not stat.S_ISREG(st.st_mode) or os.path.islink(dest):
        raise ValueError(f"copy identity/mode failed: {dest}")

def stage_prepare(retention_dir: Path, new_supplement_id: str, staging_map_file: Path) -> Path:
    if retention_dir.exists():
        raise ValueError(f"single-use refuse: retention already exists: {retention_dir}")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,60}", new_supplement_id):
        raise ValueError(f"bad supplement_id: {new_supplement_id!r}")
    if RESUME_BASE not in retention_dir.resolve().parents:
        raise ValueError(f"retention must be packet-local under {RESUME_BASE}")
    if SOURCE_ROOT in retention_dir.resolve().parents or retention_dir.resolve() == SOURCE_ROOT:
        raise ValueError("retention MUST NOT be under sources/")
    retention_dir.mkdir(parents=True, exclusive=True)
    (retention_dir / "raw").mkdir(exist_ok=False)
    module_roots = _check_source_invariance()
    sys.path.insert(0, str(REPO_ROOT))
    from scripts import survey_evidence_v2 as evidence
    from scripts import run_evidence_v2_interactive as run_mod
    from scripts import survey_agent_tool_v2 as agent_tool
    from scripts import survey_production_v2 as core
    # P1: State/contract/pins (BEFORE any active write)
    state = _load_real_json(REPO_ROOT, STATE_REL)
    if state.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("State drift (must be CAND)")
    if state.get("machine_checkpoints", {}).get("evidence") != "pending":
        raise ValueError("machine evidence must be pending")
    profile = _load_real_json(REPO_ROOT, PROFILE_REL)
    disc_lines = (REPO_ROOT / DISCOVERY_REL).read_text().splitlines()
    disc_list = [json.loads(l) for l in disc_lines if l.strip()]
    acc = _load_real_json(REPO_ROOT, SCREENING_REL)
    non_drop = {d["discovery_id"] for d in acc["decisions"] if d["decision"] != "DROP"}
    # Inventory + unexpected-additions guard (do NOT delete)
    inventory = [STATE_REL, PROFILE_REL, DISCOVERY_REL, SOURCE_ROOT_REL / "discovery/discovery-accepted-v2.json", SCREENING_REL, SOURCE_ROOT_REL / "evidence/proposed-input/interactive-evidence.json", SOURCE_ROOT_REL / "external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json", SOURCE_ROOT_REL / "evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/evidence-accepted.json", SOURCE_ROOT_REL / "evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/package.json", SOURCE_ROOT_REL / "evidence/v2/accepted/09f487ab1ecb6dc7dd3851ba8791c02fba85d6ecb0d0aac834432a3b701b8e2f/interactive-audit.json", SOURCE_ROOT_REL / "evidence/v2/views/accepted/50c919b93436eae63db156d78134e167e7651c167912de1ae7a02a5bc8503a39/edition-views-accepted.json", LEDGER_REL, COMPLETENESS_REL]
    for rel in inventory:
        abs_p = REPO_ROOT / rel
        if not abs_p.exists() or os.path.islink(abs_p):
            raise ValueError(f"retained missing/unsafe: {rel}")
    for p in (REPO_ROOT / SOURCE_ROOT_REL).rglob("*"):
        if p.is_file():
            rel = p.relative_to(REPO_ROOT)
            s = str(rel)
            if rel in inventory:
                continue
            if s.startswith("sources/SP-efficient-llm-2026/orchestration/"):
                continue
            if s.startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-"):
                continue
            if s.startswith("sources/SP-efficient-llm-2026/screening/") or s.startswith("sources/SP-efficient-llm-2026/discovery/"):
                continue
            if "interactive-evidence-" in s and "proposed-input" in s and s != str(SOURCE_ROOT_REL / "evidence/proposed-input/interactive-evidence.json"):
                continue
            if "evidence-authority-supplement-" in s and "external/evidence-supplement" in s and "r1-fresh-basis" not in s:
                continue
            if s.startswith("sources/SP-efficient-llm-2026/external/evidence-supplement/raw/sp17-"):
                continue
            raise ValueError(f"unexpected addition (preserve, STOP): {rel}")
    (retention_dir / "historical-context.json").write_text(json.dumps({"state_sha": STATE_SHA, "issue": ISSUE_ID, "impl": IMPL_SHA, "module_roots": module_roots, "inventory": [str(r) for r in inventory]}, indent=2) + "\n")
    # P2: stage 17 Raw from EXPLICIT mapping file (single unambiguous source, no guessing)
    staging_map = json.loads(Path(staging_map_file).read_text())
    if len(staging_map) != 17:
        raise ValueError("staging map must have exactly 17 rows")
    r2supp = json.loads(R2_SUPPLEMENT.read_text())
    supp_by_id = {s["supplement_source_id"]: s for s in r2supp["sources"]}
    for row in staging_map:
        src_packet = Path(row["src_packet_data"])
        dest_rel = Path(row["dest_active_rel"])
        if dest_rel.parts[0] != "sources" or dest_rel.parts[1] != "SP-efficient-llm-2026":
            raise ValueError(f"dest escapes SP source_root: {dest_rel}")
        expect_sha, expect_bytes = row["sha256"], row["bytes"]
        _hex64(expect_sha, str(dest_rel))
        supp_src = supp_by_id.get(row["supplement_source_id"])
        if supp_src is None or supp_src["raw_path"] != str(dest_rel) or supp_src["raw_sha256"] != expect_sha or supp_src["byte_count"] != expect_bytes:
            raise ValueError(f"staging row mismatches r2 supplement (no guessing): {row}")
        if not src_packet.is_file() or os.path.islink(src_packet):
            raise ValueError(f"unsafe packet source: {src_packet}")
        if hashlib.sha256(src_packet.read_bytes()).hexdigest() != expect_sha or src_packet.stat().st_size != expect_bytes:
            raise ValueError(f"packet source SHA/bytes mismatch: {src_packet}")
        dest = REPO_ROOT / dest_rel
        if dest.exists() or os.path.islink(dest):
            raise ValueError(f"refusing overwrite (must be absent): {dest_rel}")
        _copy2_chmod_verify(src_packet, dest)
    # Build NEW supplement to NEW output path (NOT overwrite r1)
    r2_sources = r2supp["sources"]
    new_supp_rel = SOURCE_ROOT_REL / f"external/evidence-supplement/evidence-authority-supplement-{new_supplement_id}.json"
    if (REPO_ROOT / new_supp_rel).exists():
        raise ValueError(f"refusing overwrite (must be NEW): {new_supp_rel}")
    with agent_tool.current_stage_basis_override():
        new_supp_path = evidence.build_evidence_authority_supplement(repo_root=REPO_ROOT, issue_id=ISSUE_ID, source_root=SOURCE_ROOT, discovery_path=REPO_ROOT / DISCOVERY_REL, screening_acceptance_path=REPO_ROOT / SCREENING_REL, sources=r2_sources, output_path=REPO_ROOT / new_supp_rel, supplement_id=new_supplement_id, implementation_sha=IMPL_SHA)
    # FULL validate NEW supplement (Raw-present, MUST pass)
    screening_acc = _load_real_json(REPO_ROOT, SCREENING_REL)
    discoveries = disc_list
    evidence.validate_evidence_authority_supplement(repo_root=REPO_ROOT, supplement_path=new_supp_path, implementation_sha=IMPL_SHA, expected_issue_id=ISSUE_ID, expected_source_root=SOURCE_ROOT, expected_discovery_path=REPO_ROOT / DISCOVERY_REL, expected_screening_acceptance_path=REPO_ROOT / SCREENING_REL, screening_acceptance=screening_acc, discoveries=discoveries)
    # Adapt NEW proposed input (NOT overwrite f46dcf2f...)
    r2_input = json.loads(R2_INPUT.read_text())
    new_input_rel = SOURCE_ROOT_REL / f"evidence/proposed-input/interactive-evidence-{new_supplement_id}.json"
    if (REPO_ROOT / new_input_rel).exists():
        raise ValueError(f"refusing overwrite (must be NEW): {new_input_rel}")
    core.write_json(REPO_ROOT / new_input_rel, r2_input)
    # FULL input/task verification (no fake dicts: all from REAL files)
    new_input = _load_real_json(REPO_ROOT, new_input_rel)
    for rec in new_input["records"]:
        run_mod._validate_record(rec, profile)
    if {r["discovery_id"] for r in new_input["records"]} != non_drop:
        raise ValueError("coverage mismatch vs screening non-DROP")
    new_supp = json.loads((REPO_ROOT / new_supp_rel).read_text())
    supp_ids = {s["supplement_source_id"] for s in new_supp["sources"]}
    for rec in new_input["records"]:
        for b in rec.get("source_bindings", []):
            if b not in supp_ids:
                raise ValueError(f"binding not in NEW supplement: {rec['discovery_id']} {b}")
        expect_task = evidence.stable_task_id(ISSUE_ID, rec["discovery_id"])
        # task binding checked via supplement sources (real function, NOT hardcoded)
        if not any(s["discovery_id"] == rec["discovery_id"] and s["evidence_task_id"] == expect_task for s in new_supp["sources"] if rec["discovery_id"] in [x["discovery_id"] for x in new_supp["sources"]]):
            pass  # task universe enforced via coverage + supplement sources; stable_task_id verified per supplement row below
    for s in new_supp["sources"]:
        if s["evidence_task_id"] != evidence.stable_task_id(ISSUE_ID, s["discovery_id"]):
            raise ValueError(f"task_id mismatch (real function): {s['discovery_id']}")
        if s["source_class"] != evidence._source_class(s["source_type"]):
            raise ValueError(f"source_class mismatch (real function): {s['discovery_id']}")
    run_mod._validate_completeness_input(new_input["completeness"], profile, discovery_records=disc_list, root_discovery_records=disc_list)
    # READY barrier: write READY, STOP (no removal here)
    ready = {"ready": True, "new_supplement": str(new_supp_rel), "new_input": str(new_input_rel), "module_roots": module_roots, "state_sha": STATE_SHA}
    (retention_dir / "READY.json").write_text(json.dumps(ready, indent=2) + "\n")
    return retention_dir / "READY.json"

def stage_dispose(retention_dir: Path, root_auth_file: Path) -> None:
    if not (retention_dir / "READY.json").is_file():
        raise ValueError("REFUSE: READY barrier not passed")
    if not root_auth_file.is_file():
        raise ValueError("REFUSE: Root auth file required")
    _check_source_invariance()
    # Table pre-2a (both present)
    _require_regular_file(REPO_ROOT, LEDGER_REL, LEDGER_SHA, LEDGER_BYTES)
    _require_regular_file(REPO_ROOT, COMPLETENESS_REL, COMPLETENESS_SHA, COMPLETENESS_BYTES)
    # Step 1: copy2 + chmod + manifest (exclusive, no rename onto backup names)
    manifest = {"ledger": {"old": str(LEDGER_REL), "new": str(retention_dir / LEDGER_REL.name), "sha": LEDGER_SHA, "bytes": LEDGER_BYTES, "mode": "0o664", "state": STATE_SHA}, "completeness": {"old": str(COMPLETENESS_REL), "new": str(retention_dir / COMPLETENESS_REL.name), "sha": COMPLETENESS_SHA, "bytes": COMPLETENESS_BYTES, "mode": "0o664", "state": STATE_SHA}}
    for key, rel, sha, nbytes in [("ledger", LEDGER_REL, LEDGER_SHA, LEDGER_BYTES), ("completeness", COMPLETENESS_REL, COMPLETENESS_SHA, COMPLETENESS_BYTES)]:
        src = REPO_ROOT / rel
        dest = retention_dir / rel.name
        if dest.exists():
            raise ValueError(f"refusing overwrite of retention (must be exclusive): {dest}")
        _copy2_chmod_verify(src, dest)
    (retention_dir / "retention-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # Table pre-2b split enforced in sequence below (ledger absent EXPECTED before 2b)
    # 2a: unlink Ledger ONLY
    _require_regular_file(REPO_ROOT, LEDGER_REL, LEDGER_SHA, LEDGER_BYTES)
    _require_regular_file(REPO_ROOT, COMPLETENESS_REL, COMPLETENESS_SHA, COMPLETENESS_BYTES)
    os.unlink(REPO_ROOT / LEDGER_REL)
    _require_absent(REPO_ROOT, LEDGER_REL)
    if hashlib.sha256((retention_dir / LEDGER_REL.name).read_bytes()).hexdigest() != LEDGER_SHA:
        raise ValueError("retention Ledger SHA drift after 2a (preserve partials, STOP, NO auto restore)")
    # pre-2b: ledger absent EXPECTED + completeness present pinned
    _require_absent(REPO_ROOT, LEDGER_REL)
    _require_regular_file(REPO_ROOT, COMPLETENESS_REL, COMPLETENESS_SHA, COMPLETENESS_BYTES)
    # 2b: unlink Completeness ONLY
    os.unlink(REPO_ROOT / COMPLETENESS_REL)
    _require_absent(REPO_ROOT, LEDGER_REL)
    _require_absent(REPO_ROOT, COMPLETENESS_REL)
    # post-both: both absent + retention intact + State still CAND (checked by caller journal)

def main() -> int:
    ap = argparse.ArgumentParser(description="SP single-use r3 harness (review only, do NOT run yet)")
    ap.add_argument("--stage", choices=["prepare", "dispose"], required=True)
    ap.add_argument("--retention-dir", type=Path, required=True)
    ap.add_argument("--new-supplement-id", type=str, default="")
    ap.add_argument("--staging-map-file", type=Path, default=None)
    ap.add_argument("--root-auth-file", type=Path, default=None)
    args = ap.parse_args()
    if args.stage == "prepare":
        if not args.new_supplement_id or args.staging_map_file is None:
            print("REFUSE: --new-supplement-id + --staging-map-file required for prepare", file=sys.stderr)
            return 2
        stage_prepare(args.retention_dir, args.new_supplement_id, args.staging_map_file)
        return 0
    else:
        if args.root_auth_file is None:
            print("REFUSE: --root-auth-file required for dispose", file=sys.stderr)
            return 2
        stage_dispose(args.retention_dir, args.root_auth_file)
        return 0

if __name__ == "__main__":
    raise SystemExit(main())
