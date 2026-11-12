#!/usr/bin/env python3
"""NEW CURRENT proof for supplement-carry bounded repair (packet-only, not shipping).

Genuine CURRENT_PROOF_VALID via real verify_renewal_source_proof on NEW runtime
snapshot (frozen author workcopy 773 files, LOW d50282/HIGH f312), weekly route only
via LayerB full_valid_proof (no HIGH finalize toolchain, no PDF build, no stub).

Strict: new independent DB, env identity only (no git config, no HOME rewrite,
no remote, no --allow-empty, no rootDB sharing, no alternates/hardlinks),
loader roots = fixture work before authority, real validator + explicit
CURRENT_PROOF_VALID True, SAME stored proof drift refusal (no rewritten rows),
before/after/restore controlled, no code coercion, no synthetic Human approval.

Reference DATA only (not executed): prior evidence-scaling CURRENT supplement
packet current-supplement-20261104T003000Z (weekly final139, 70 rows). This harness
is NEW code, does NOT rerun old saved harness.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import datetime as _dt

# Frozen author workcopy (new runtime snapshot, NOT shipping candidate)
WORKCOPY = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work")
# Bootstrap weekly (existing legitimate fixture, read-only)
BOOT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly")
# Packet (durable evidence under notes/, created by outer wrapper)
PACKET = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-supplement-carry-repair-20261106/current-proof-20261107T035000Z")
# Fixbase parent (ignored runtime, no full DB in packet)
FIXBASE_PARENT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/supplement-carry-current-proof-20261107T035000Z")

# Expected frozen bounds (worktree SHA256, sizes)
EXP_LOW_SHA = "d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd"
EXP_LOW_N = 239978
EXP_HIGH_SHA = "f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90"
EXP_HIGH_N = 97844
EXP_FOCUSED_SHA = "5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00"
EXP_FOCUSED_N = 60569
EXP_SCALE_SHA = "7118092f80b1a7a23f198b887926ec1631c7adf9f3503c7016cc693254644668"
EXP_SCALE_N = 27736
EXP_CTEST_SHA = "1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31"
EXP_HEAD = "5eef790bd8d492c557cc4db9c29425e3e410d47d"

_SOURCE_PATHS = ("scripts", "schemas", "config", "templates", "tests", "docs", ".github")

def _sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for ch in iter(lambda: fh.read(65536), b""):
            h.update(ch)
    return h.hexdigest()

def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def _run_git(work: Path, *args: str, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(work), capture_output=True, timeout=120, env=env)

def _copy_tree_no_git(src: Path, dst: Path) -> None:
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            if fn.endswith(".pyc"):
                continue
            full = Path(dirpath) / fn
            rel = full.relative_to(src)
            if rel.parts and rel.parts[0] == ".rephase-1-editorial-runtime":
                continue
            tgt = dst / rel
            tgt.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(full, tgt)

def _workcopy_773_list() -> list[Path]:
    # 771 tracked via git ls-files --cached (workcopy only, never reconstruct root)
    # plus 2 known untracked new tests. No `git -C .`.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"})
    proc = subprocess.run(["git", "-C", str(WORKCOPY), "ls-files", "--cached", "-z"],
                          capture_output=True, timeout=60, env=env)
    assert proc.returncode == 0, f"workcopy ls-files failed: {proc.stderr[:500]}"
    tracked = [WORKCOPY / p for p in proc.stdout.decode().split("\x00") if p]
    assert len(tracked) == 771, f"workcopy tracked must be 771, got {len(tracked)}"
    extra = [WORKCOPY / "tests/test_dm022_supplement_carry_v2.py",
             WORKCOPY / "tests/test_dm022_supplement_carry_scale_v2.py"]
    for p in extra:
        assert p.is_file(), f"untracked new test missing: {p}"
    # ensure extra not already in tracked (they are untracked)
    tracked_set = set(str(p.relative_to(WORKCOPY).as_posix()) for p in tracked)
    assert "tests/test_dm022_supplement_carry_v2.py" not in tracked_set
    assert "tests/test_dm022_supplement_carry_scale_v2.py" not in tracked_set
    return sorted(tracked + extra, key=lambda p: p.relative_to(WORKCOPY).as_posix())

def _hash_773(paths: list[Path]) -> list[str]:
    rows = []
    for p in paths:
        rel = p.relative_to(WORKCOPY).as_posix()
        rows.append(f"{_sha_file(p)} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {rel}")
    return sorted(rows)

def main() -> int:
    print("CURRENT proof (supplement-carry new runtime): frozen workcopy check", flush=True)
    # --- frozen bounds, no writes to workcopy/proof/e84 ---
    assert WORKCOPY.is_dir(), f"workcopy missing: {WORKCOPY}"
    assert BOOT.is_dir(), f"bootstrap weekly missing: {BOOT}"
    # HEAD via file read (no git binary for e84/proof, minimal git for workcopy bounds only)
    wc_head_ref = (WORKCOPY / ".git/HEAD").read_text().strip()
    assert wc_head_ref == "ref: refs/heads/main", f"workcopy HEAD ref unexpected: {wc_head_ref}"
    wc_head = (WORKCOPY / ".git/refs/heads/main").read_text().strip()
    assert wc_head == EXP_HEAD, f"workcopy HEAD mismatch: {wc_head}"
    cfg_txt = (WORKCOPY / ".git/config").read_text()
    assert "https://invalid.invalid/inert.git" in cfg_txt, "workcopy origin not inert"
    assert not (WORKCOPY / ".git/objects/info/alternates").exists(), "workcopy alternates must not exist"
    # expected file pins (worktree)
    checks = [
        ("scripts/survey_research_authority_v2.py", EXP_LOW_SHA, EXP_LOW_N),
        ("scripts/survey_prearchitecture_acceptance_v2.py", EXP_HIGH_SHA, EXP_HIGH_N),
        ("tests/test_dm022_supplement_carry_v2.py", EXP_FOCUSED_SHA, EXP_FOCUSED_N),
        ("tests/test_dm022_supplement_carry_scale_v2.py", EXP_SCALE_SHA, EXP_SCALE_N),
        ("tests/test_dm022_c_direct_operation_v2.py", EXP_CTEST_SHA, None),
    ]
    for rel, exp_sha, exp_n in checks:
        p = WORKCOPY / rel
        sha = _sha_file(p)
        n = p.stat().st_size
        assert sha == exp_sha, f"workcopy pin mismatch {rel}: {sha} != {exp_sha}"
        if exp_n is not None:
            assert n == exp_n, f"workcopy size mismatch {rel}: {n} != {exp_n}"
        print(f"workcopy {rel} OK {sha[:12]} {n}", flush=True)
    # full 773 list + hash before
    paths773 = _workcopy_773_list()
    assert len(paths773) == 773, f"intended must be 773, got {len(paths773)}"
    pins_before = _hash_773(paths773)
    assert len(pins_before) == 773
    print(f"workcopy 773 before OK ({len(pins_before)} files)", flush=True)
    # proof/e84 unchanged pre-check via stat only (no writes, no git binary)
    proof_low = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60/scripts/survey_research_authority_v2.py")
    e84_head_path = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/.git/HEAD")
    proof_stat_before = (proof_low.stat().st_mtime_ns, proof_low.stat().st_size)
    e84_head_before = e84_head_path.read_text().strip()
    assert e84_head_before.startswith("e84a82aca000c990597ea8cf60f548e2ff187bd1"), f"e84 HEAD unexpected: {e84_head_before[:40]}"
    print(f"proof/e84 pre OK (proof mtime {proof_stat_before[0]}, e84 {e84_head_before[:12]})", flush=True)

    # --- packet dirs (durable evidence, not source commit) ---
    data = PACKET / "data"
    rawdir = PACKET / "raw"
    # PACKET already created by outer wrapper; ensure data/raw exist
    data.mkdir(parents=True, exist_ok=True)
    rawdir.mkdir(parents=True, exist_ok=True)
    (data / "pins-workcopy-773-before.txt").write_text("\n".join(pins_before) + "\n", encoding="utf-8")

    # --- new independent fixture under ignored runtime ---
    assert FIXBASE_PARENT.parent.exists(), f"ignored runtime parent missing: {FIXBASE_PARENT.parent}"
    FIXBASE_PARENT.mkdir(parents=True, exist_ok=True)
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fixbase = FIXBASE_PARENT / f"fixture-{ts}"
    fixbase.mkdir(parents=True, exist_ok=False)
    work = fixbase / "work"
    shutil.copytree(BOOT, work, symlinks=False)
    _copy_tree_no_git(WORKCOPY, work)
    print(f"fixture work {work}", flush=True)

    # process-scoped identity only, no git config, no HOME rewrite, no remote
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_AUTHOR_NAME": "supplement-carry-current-proof",
        "GIT_AUTHOR_EMAIL": "supplement-carry-current-proof@example.invalid",
        "GIT_COMMITTER_NAME": "supplement-carry-current-proof",
        "GIT_COMMITTER_EMAIL": "supplement-carry-current-proof@example.invalid",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
    })
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_SYSTEM"] = "/dev/null"
    executor_id = {"GIT_AUTHOR_NAME": env["GIT_AUTHOR_NAME"], "GIT_AUTHOR_EMAIL": env["GIT_AUTHOR_EMAIL"],
                   "GIT_COMMITTER_NAME": env["GIT_COMMITTER_NAME"], "GIT_COMMITTER_EMAIL": env["GIT_COMMITTER_EMAIL"],
                   "pid": os.getpid(), "ppid": os.getppid()}
    print(f"executor {executor_id}", flush=True)

    r = _run_git(work, "init", "-q", env=env)
    assert r.returncode == 0, f"git init failed: {r.stderr[:500]}"
    assert not (work / ".git/objects/info/alternates").exists(), "alternates must not exist"
    for rel in ["scripts/survey_evidence_v2.py", "scripts/survey_versioned_renewal_source_v2.py"]:
        st = (work / rel).stat()
        assert st.st_nlink == 1, f"hardlink suspected {rel} nlink={st.st_nlink}"
    r = _run_git(work, "add", *_SOURCE_PATHS, env=env)
    assert r.returncode == 0, f"git add failed: {r.stderr[:1000]}"
    msg = "supplement-carry CURRENT proof: exact new-runtime 773 source snapshot (weekly, NOT ordinary candidate)"
    r = _run_git(work, "commit", "-q", "-m", msg, env=env)
    assert r.returncode == 0, f"git commit failed (empty? no --allow-empty used): {r.stderr[:1000]}"
    assert r.stderr.decode().strip() == "", f"unexpected commit stderr: {r.stderr[:500]}"
    head = _run_git(work, "rev-parse", "HEAD", env=env).stdout.decode().strip()
    assert len(head) == 40 and head == head.lower() and all(c in "0123456789abcdef" for c in head), f"HEAD not 40-hex: {head}"
    print(f"fixture HEAD {head}", flush=True)
    src_status = _run_git(work, "status", "--short", "--", *_SOURCE_PATHS, env=env).stdout.decode().strip()
    assert src_status == "", f"source paths not clean: {src_status[:1000]}"

    # strict loader roots: fixture work before authority
    if str(work) not in sys.path:
        sys.path.insert(0, str(work))
    for m in [m for m in list(sys.modules) if m == "scripts" or m.startswith("scripts.")]:
        sys.modules.pop(m, None)
    import importlib
    src = importlib.import_module("scripts.survey_versioned_renewal_source_v2")
    hist = importlib.import_module("scripts.survey_versioned_renewal_history_v2")
    high = importlib.import_module("scripts.survey_versioned_renewal_v2")
    core = importlib.import_module("scripts.survey_production_v2")
    for mod, name in [(src, "source"), (hist, "history"), (high, "high")]:
        f = Path(mod.__file__).resolve()
        assert str(f).startswith(str(work.resolve())), f"{name} not from fixture work: {f}"
        print(f"loaded {name} from fixture {f}", flush=True)
    # fixture blobs match running modules + WORKCOPY before authority (committed tool bytes)
    for rel in ["scripts/survey_versioned_renewal_source_v2.py",
                "scripts/survey_versioned_renewal_history_v2.py",
                "scripts/survey_versioned_renewal_v2.py",
                "scripts/survey_research_authority_v2.py",
                "scripts/survey_evidence_v2.py"]:
        live = _sha_file(work / rel)
        shown = subprocess.run(["git", "-C", str(work), "show", f"HEAD:{rel}"],
                               capture_output=True, env=env).stdout
        assert _sha_bytes(shown) == live, f"fixture blob mismatch {rel}"
        assert live == _sha_file(WORKCOPY / rel), f"fixture vs WORKCOPY mismatch {rel}"
    print("fixture blobs match running modules + WORKCOPY (new runtime)", flush=True)
    # helper hash (existing test helper, DATA reuse, not old harness rerun)
    helper_rel = "tests/test_versioned_renewal_source_phase_s.py"
    helper_sha = _sha_file(work / helper_rel)
    helper_workcopy_sha = _sha_file(WORKCOPY / helper_rel)
    assert helper_sha == helper_workcopy_sha, "helper drift vs WORKCOPY"
    print(f"helper {helper_rel} {helper_sha[:12]}", flush=True)

    # derive issue/prop (weekly only, same as prior supplement logic, DATA reference)
    states = sorted(work.glob("sources/*/production-state.json"))
    states = [s for s in states if s.parent.name in ("2026-W37", "2026-W33", "SP001") or s.parent.parent.name == "sources"]
    states = [s for s in states if "2026-W" in str(s)]
    assert len(states) == 1, f"weekly State ambiguous: {states}"
    issue = json.loads(states[0].read_bytes()).get("issue_id") or states[0].parent.name
    cands = sorted((work / f"sources/{issue}/publication/v2/editorial-corrections").glob("*/publication/publication-set.json"))
    assert len(cands) == 1, f"prop ambiguous: {cands}"
    prop = cands[0].parts[-3]
    print(f"issue {issue} prop {prop}", flush=True)
    state_rel = f"sources/{issue}/production-state.json"
    live_state_before = _sha_file(work / state_rel)

    # LayerB genuine positive via real _basis_for + _full_valid_proof (existing helpers, no HIGH toolchain)
    import importlib as _il2
    tmod = _il2.import_module("tests.test_versioned_renewal_source_phase_s")
    tfile = Path(tmod.__file__).resolve()
    assert str(tfile).startswith(str(work.resolve())), f"test helpers not from fixture work: {tfile}"
    print(f"loaded test helpers from fixture {tfile}", flush=True)
    _basis_for = getattr(tmod, "_basis_for")
    _full_valid_proof = getattr(tmod, "_full_valid_proof")
    class _Sc:
        def p(self, *parts: str) -> Path:
            return self.work.joinpath(*parts)
        def j(self, rel: str) -> dict:
            return json.loads((self.work / rel).read_bytes())
    sc = _Sc()
    sc.tag = "supplement-carry-current-w1"
    sc.kind = "weekly"
    sc.work = work
    sc.issue = issue
    sc.prop = prop
    sc.head = head
    basis_rel, basis = _basis_for(sc, "supplement-carry-current-w1")
    assert (work / basis_rel).is_file(), "basis missing"
    print(f"basis {basis_rel} {basis.get('basis_sha256','')[:12]}", flush=True)
    proof_rel, proof = _full_valid_proof(sc, basis_rel, basis)
    assert (work / proof_rel).is_file(), "proof missing"
    out = src.verify_renewal_source_proof(work, basis_rel, proof_rel)
    assert out.get("CURRENT_PROOF_VALID") is True, f"CURRENT_PROOF_VALID not True: {out}"
    assert out.get("basis_file_sha256") == _sha_file(work / basis_rel), "basis FILE digest mismatch"
    basis_self = json.loads((work / basis_rel).read_bytes())["basis_sha256"]
    assert out.get("basis_self_sha256") == basis_self, "basis SELF digest mismatch"
    print(f"POSITIVE CURRENT_PROOF_VALID True basis_file {out.get('basis_file_sha256')[:12]}", flush=True)
    assert _sha_file(work / state_rel) == live_state_before, "positive mutated live State"
    print("live State unchanged after positive", flush=True)
    # persist basis/proof/manifest/closure/pins
    shutil.copyfile(work / basis_rel, data / "renewal-basis.json")
    shutil.copyfile(work / proof_rel, data / "renewal-source-proof.json")
    basis_doc = json.loads((work / basis_rel).read_bytes())
    proof_doc = json.loads((work / proof_rel).read_bytes())
    closure = proof_doc.get("dependency_closure", [])
    (data / "current-code-closure.json").write_text(json.dumps(closure, indent=1, sort_keys=True), encoding="utf-8")
    def _pins_root(root: Path):
        rows = []
        for p in sorted(root.rglob("*")):
            if ".git" in p.parts or "__pycache__" in p.parts or p.suffix == ".pyc" or p.is_dir():
                continue
            rows.append(f"{_sha_file(p)} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {p.relative_to(root).as_posix()}")
        return rows
    # workcopy 773 already have pins_before; also record fixture source subset
    work_src_rows = []
    for sp in _SOURCE_PATHS:
        for p in sorted((work / sp).rglob("*")):
            if p.is_dir() or "__pycache__" in p.parts or p.suffix == ".pyc":
                continue
            work_src_rows.append(f"{_sha_file(p)} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {(p.relative_to(work)).as_posix()}")
    (data / "pins-fixture-source.txt").write_text("\n".join(sorted(work_src_rows)) + "\n", encoding="utf-8")
    (data / "helper-sha.txt").write_text(f"{helper_sha} {helper_rel}\n", encoding="utf-8")
    manifest = {
        "workcopy": str(WORKCOPY), "workcopy_head": EXP_HEAD,
        "workcopy_pins": {"low": EXP_LOW_SHA, "high": EXP_HIGH_SHA, "focused": EXP_FOCUSED_SHA, "scale": EXP_SCALE_SHA, "ctest": EXP_CTEST_SHA},
        "intended_773_before": len(pins_before),
        "fixture_work": str(work), "fixture_head": head,
        "issue": issue, "prop": prop, "route": "WEEKLY_GENERATED_V2",
        "basis_rel": basis_rel, "proof_rel": proof_rel,
        "basis_sha256": basis_doc.get("basis_sha256"), "proof_sha256": proof_doc.get("proof_sha256"),
        "basis_file_sha256": out.get("basis_file_sha256"), "closure_len": len(closure),
        "executor": executor_id, "executor_note": "synthetic test executor only, NOT Human approval; no PDF/RELEASED claim",
        "scope": "weekly only via LayerB full_valid_proof (no HIGH finalize toolchain, no PDF); longform via existing 7/8/3 consumers + family 6/graph 8 (labelled, not re-proven here)",
        "helper_sha256": helper_sha, "helper_path": helper_rel,
    }
    (data / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (data / "verify-positive.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"persisted basis/proof/manifest closure_len={len(closure)}", flush=True)

    # SAME stored proof drift (no rewritten rows/digest) on disposable fixture LOW file only
    proof_before = (work / proof_rel).read_bytes()
    basis_before = (work / basis_rel).read_bytes()
    target_rel = "scripts/survey_research_authority_v2.py"
    target = work / target_rel
    orig = target.read_bytes()
    target.write_bytes(orig + b"\n# supplement-carry CURRENT drift probe\n")
    try:
        try:
            src.verify_renewal_source_proof(work, basis_rel, proof_rel)
            raise SystemExit("DRIFT_UNEXPECTED_PASS: SAME proof passed after CURRENT tool mutation (must refuse)")
        except SystemExit as se:
            raise
        except Exception as e:
            msg_e = f"{type(e).__name__}: {e}"
            assert "BASIS_CURRENT_TOOL_DRIFT" in msg_e or "RENEWAL_PROOF_DIGEST" in msg_e or "HISTORY_TOOL_EPOCH_DRIFT" in msg_e, f"wrong refusal code: {msg_e[:500]}"
            print(f"DRIFT_REFUSED {msg_e[:300]}", flush=True)
            (data / "drift-refusal.txt").write_text(msg_e + "\n", encoding="utf-8")
        assert (work / proof_rel).read_bytes() == proof_before, "proof file rewritten during drift (must use SAME stored proof)"
        assert (work / basis_rel).read_bytes() == basis_before, "basis file rewritten during drift"
        print("SAME stored proof/basis bytes unchanged during refusal", flush=True)
    finally:
        target.write_bytes(orig)
    # repair controlled separate: restore -> positive again (no coercion)
    out2 = src.verify_renewal_source_proof(work, basis_rel, proof_rel)
    assert out2.get("CURRENT_PROOF_VALID") is True, f"repair positive failed: {out2}"
    print("REPAIR_POSITIVE CURRENT_PROOF_VALID True (restored byte, separate step)", flush=True)
    (data / "repair-positive.txt").write_text(f"CURRENT_PROOF_VALID True after restore\n", encoding="utf-8")
    (data / "verify-repair.json").write_text(json.dumps(out2, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("historical basis/proof data unchanged (SAME bytes)", flush=True)

    # post 773 snapshot (workcopy must be unchanged; fixture drift restored)
    pins_after = _hash_773(_workcopy_773_list())
    (data / "pins-workcopy-773-after.txt").write_text("\n".join(pins_after) + "\n", encoding="utf-8")
    assert pins_after == pins_before, "workcopy 773 changed during CURRENT proof (must be unchanged)"
    print("workcopy 773 after == before YES", flush=True)
    # proof/e84 unchanged (stat only)
    proof_stat_after = (proof_low.stat().st_mtime_ns, proof_low.stat().st_size)
    e84_head_after = e84_head_path.read_text().strip()
    assert proof_stat_after == proof_stat_before, f"proof-copy mutated: {proof_stat_before} != {proof_stat_after}"
    assert e84_head_after == e84_head_before, "e84 HEAD changed"
    print("proof/e84 unchanged YES", flush=True)
    print("CURRENT_SUPPLEMENT_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
