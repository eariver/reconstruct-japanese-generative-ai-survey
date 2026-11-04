#!/usr/bin/env python3
"""NEW CURRENT supplement proof (packet-only, not shipping).

Genuine CURRENT_PROOF_VALID via real verify_renewal_source_proof on final139
worktree (snapshot-fixed == proof-copy worktree, 0 diff), weekly route only
(other route via existing 7/8/3 consumers, labelled scope).

Strict: new independent DB, env identity only (no `git config`, no HOME rewrite,
no remote, no --allow-empty, no rootDB sharing, no alternates/hardlinks),
loader roots = fixture work before authority, real validator + explicit
CURRENT_PROOF_VALID true, SAME stored proof drift refusal (no rewritten rows),
before/after/restore controlled, no code coercion, no synthetic Human approval.
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

SNAP = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed")
PACKET = Path(__file__).resolve().parent
SUPPLEMENT = PACKET / "current-supplement-20261104T003000Z"
# FIXBASE in ignored runtime (no full DB in packet)
FIXBASE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z")

FINAL_PATCH_SHA = "de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49"
FINAL_PATCH_BYTES = 5408065
FINAL_MANIFEST_SHA = "c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143"
FINAL_MANIFEST_BYTES = 202204

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

def main() -> int:
    print("CURRENT supplement: final139 worktree check", flush=True)
    # verify SNAP == proof-copy worktree already done (0 diff); re-verify 3 runtimes + patch pins here (read-only)
    for rel, exp_sha, exp_n in [
        ("scripts/survey_evidence_v2.py", "487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a", 158943),
        ("scripts/run_evidence_v2_interactive.py", "5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543", 45833),
        ("scripts/survey_research_authority_v2.py", "0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b", 218692),
    ]:
        p = SNAP / rel
        sha = _sha_file(p); n = p.stat().st_size
        assert sha == exp_sha and n == exp_n, f"SNAP runtime mismatch {rel}"
        print(f"SNAP {rel} OK {sha[:12]} {n}", flush=True)
    # final patch/manifest pins (read-only, no network)
    patch = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-409.patch")
    manif = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json")
    assert _sha_file(patch) == FINAL_PATCH_SHA and patch.stat().st_size == FINAL_PATCH_BYTES, "final patch pin mismatch"
    assert _sha_file(manif) == FINAL_MANIFEST_SHA and manif.stat().st_size == FINAL_MANIFEST_BYTES, "final manifest pin mismatch"
    print(f"final patch {FINAL_PATCH_SHA[:12]} {FINAL_PATCH_BYTES} OK", flush=True)
    print(f"final manifest {FINAL_MANIFEST_SHA[:12]} {FINAL_MANIFEST_BYTES} OK", flush=True)

    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fixbase = FIXBASE / f"current-supplement-fixture-{ts}"
    fixbase.mkdir(parents=True, exist_ok=False)
    # bootstrap weekly (existing legitimate fixture, read-only)
    boot = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly")
    assert boot.is_dir(), f"bootstrap weekly missing: {boot}"
    work = fixbase / "work"
    shutil.copytree(boot, work, symlinks=False)
    _copy_tree_no_git(SNAP, work)
    print(f"fixture work {work}", flush=True)

    # process-scoped identity only, no `git config`, no HOME rewrite, no remote
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_AUTHOR_NAME": "current-supplement-proof",
        "GIT_AUTHOR_EMAIL": "current-supplement-proof@example.invalid",
        "GIT_COMMITTER_NAME": "current-supplement-proof",
        "GIT_COMMITTER_EMAIL": "current-supplement-proof@example.invalid",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_OPTIONAL_LOCKS": "0",
    })
    # ensure no global config interference: point global/system to /dev/null via env (process-scoped, no file write)
    # (GIT_CONFIG_GLOBAL/SYSTEM are read-only env, not `git config` writes)
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_SYSTEM"] = "/dev/null"
    executor_id = {"GIT_AUTHOR_NAME": env["GIT_AUTHOR_NAME"], "GIT_AUTHOR_EMAIL": env["GIT_AUTHOR_EMAIL"],
                   "GIT_COMMITTER_NAME": env["GIT_COMMITTER_NAME"], "GIT_COMMITTER_EMAIL": env["GIT_COMMITTER_EMAIL"],
                   "pid": os.getpid(), "ppid": os.getppid()}
    print(f"executor {executor_id}", flush=True)

    r = _run_git(work, "init", "-q", env=env)
    assert r.returncode == 0, f"git init failed: {r.stderr[:500]}"
    # no `git config`, no `git remote` (inert by absence, no push)
    assert not (work / ".git/objects/info/alternates").exists(), "alternates must not exist"
    # no hardlinks: spot-check nlink==1 for a few files
    for rel in ["scripts/survey_evidence_v2.py", "scripts/survey_versioned_renewal_source_v2.py"]:
        st = (work / rel).stat()
        assert st.st_nlink == 1, f"hardlink suspected {rel} nlink={st.st_nlink}"
    r = _run_git(work, "add", *_SOURCE_PATHS, env=env)
    assert r.returncode == 0, f"git add failed: {r.stderr[:1000]}"
    msg = "current-supplement: exact final139 source snapshot (weekly CURRENT proof, NOT ordinary candidate)"
    r = _run_git(work, "commit", "-q", "-m", msg, env=env)
    assert r.returncode == 0, f"git commit failed (empty? no --allow-empty used): {r.stderr[:1000]}"
    assert r.stderr.decode().strip() == "", f"unexpected commit stderr: {r.stderr[:500]}"
    head = _run_git(work, "rev-parse", "HEAD", env=env).stdout.decode().strip()
    assert len(head) == 40, f"HEAD not 40: {head}"
    print(f"fixture HEAD {head}", flush=True)
    # source snapshot clean for source paths
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
    # fixture blobs match running modules before authority (sample: src + LOW + HIGH)
    for rel in ["scripts/survey_versioned_renewal_source_v2.py",
                "scripts/survey_versioned_renewal_history_v2.py",
                "scripts/survey_versioned_renewal_v2.py",
                "scripts/survey_research_authority_v2.py",
                "scripts/survey_evidence_v2.py"]:
        live = _sha_file(work / rel)
        shown = subprocess.run(["git", "-C", str(work), "show", f"HEAD:{rel}"], capture_output=True, env=env).stdout
        assert _sha_bytes(shown) == live, f"fixture blob mismatch {rel}"
        # also match SNAP (final139) since work copied from SNAP
        assert live == _sha_file(SNAP / rel), f"fixture vs SNAP mismatch {rel}"
    print("fixture blobs match running modules + SNAP (final139)", flush=True)

    # derive issue/prop (same as Scratch, no gitconfig)
    states = sorted(work.glob("sources/*/production-state.json"))
    states = [s for s in states if s.parent.name in ("2026-W37", "2026-W33", "SP001") or s.parent.parent.name == "sources"]
    states = [s for s in states if "2026-W" in str(s)]  # weekly scope
    assert len(states) == 1, f"weekly State ambiguous: {states}"
    issue = json.loads(states[0].read_bytes()).get("issue_id") or states[0].parent.name
    cands = sorted((work / f"sources/{issue}/publication/v2/editorial-corrections").glob("*/publication/publication-set.json"))
    assert len(cands) == 1, f"prop ambiguous: {cands}"
    prop = cands[0].parts[-3]
    print(f"issue {issue} prop {prop}", flush=True)
    state_rel = f"sources/{issue}/production-state.json"
    live_state_before = _sha_file(work / state_rel)

    # LayerB genuine positive via real _basis_for + _full_valid_proof (no HIGH finalize toolchain).
    # Reuses legitimate test helpers (read, not swallowing): _basis_for builds basis,
    # _full_valid_proof builds real trio/digests/closure + calls real verify with explicit True.
    # The swallowing test test_layerb_full_reused_positive_weekly (REUSE_TARGET_MISMATCH as success) is NOT used.
    import importlib as _il2
    tmod = _il2.import_module("tests.test_versioned_renewal_source_phase_s")
    tfile = Path(tmod.__file__).resolve()
    assert str(tfile).startswith(str(work.resolve())), f"test helpers not from fixture work: {tfile}"
    print(f"loaded test helpers from fixture {tfile}", flush=True)
    _basis_for = getattr(tmod, "_basis_for")
    _full_valid_proof = getattr(tmod, "_full_valid_proof")
    # minimal sc namespace (no Scratch.__init__ gitconfig)
    class _Sc:
        def p(self, *parts: str) -> Path:
            return self.work.joinpath(*parts)
        def j(self, rel: str) -> dict:
            return json.loads((self.work / rel).read_bytes())
    sc = _Sc()
    sc.tag = "current-supplement-w1"
    sc.kind = "weekly"
    sc.work = work
    sc.issue = issue
    sc.prop = prop
    sc.head = head
    # _basis_for creates basis file (real HIST verdict, real contract, real observed bindings)
    basis_rel, basis = _basis_for(sc, "current-supplement-w1")
    assert (work / basis_rel).is_file(), "basis missing"
    print(f"basis {basis_rel} {basis.get('basis_sha256','')[:12]}", flush=True)
    # _full_valid_proof creates real proof (real trio/old refs/Layer-A digests/CURRENT closure) + verifies True
    proof_rel, proof = _full_valid_proof(sc, basis_rel, basis)
    assert (work / proof_rel).is_file(), "proof missing"
    # explicit True flag (no swallowing): re-verify directly with real validator
    out = src.verify_renewal_source_proof(work, basis_rel, proof_rel)
    assert out.get("CURRENT_PROOF_VALID") is True, f"CURRENT_PROOF_VALID not True: {out}"
    assert out.get("basis_file_sha256") == _sha_file(work / basis_rel), "basis FILE digest mismatch"
    basis_self = json.loads((work / basis_rel).read_bytes())["basis_sha256"]
    assert out.get("basis_self_sha256") == basis_self, "basis SELF digest mismatch"
    print(f"POSITIVE CURRENT_PROOF_VALID True basis_file {out.get('basis_file_sha256')[:12]}", flush=True)
    assert _sha_file(work / state_rel) == live_state_before, "positive mutated live State"
    print("live State unchanged after positive", flush=True)
    # persist basis/proof/manifest/closure/pins (SUPPLEMENT dir already created by wrapper)
    data = SUPPLEMENT / "data"
    data.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(work / basis_rel, data / "renewal-basis.json")
    shutil.copyfile(work / proof_rel, data / "renewal-source-proof.json")
    basis_doc = json.loads((work / basis_rel).read_bytes())
    proof_doc = json.loads((work / proof_rel).read_bytes())
    closure = proof_doc.get("dependency_closure", [])
    (data / "current-code-closure.json").write_text(json.dumps(closure, indent=1, sort_keys=True), encoding="utf-8")
    # pins: 771 intended (excl .git/pycache) for SNAP + work (should match for source paths)
    def _pins(root: Path):
        rows = []
        for p in sorted(root.rglob("*")):
            if ".git" in p.parts or "__pycache__" in p.parts or p.suffix == ".pyc" or p.is_dir():
                continue
            # only intended 771? SNAP has exactly 771; work has bootstrap + authorities extra – record all + source subset
            rows.append(f"{_sha_file(p)} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {p.relative_to(root).as_posix()}")
        return rows
    (data / "pins-snap-771.txt").write_text("\n".join(_pins(SNAP)) + "\n", encoding="utf-8")
    # source-subset pins for work (scripts/schemas/config/templates/tests/docs/.github)
    work_src_rows = []
    for sp in _SOURCE_PATHS:
        for p in sorted((work / sp).rglob("*")):
            if p.is_dir() or "__pycache__" in p.parts or p.suffix == ".pyc":
                continue
            work_src_rows.append(f"{_sha_file(p)} {p.stat().st_size} {oct(p.stat().st_mode & 0o777)} {(p.relative_to(work)).as_posix()}")
    (data / "pins-work-source.txt").write_text("\n".join(sorted(work_src_rows)) + "\n", encoding="utf-8")
    manifest = {
        "final_patch_sha256": FINAL_PATCH_SHA, "final_patch_bytes": FINAL_PATCH_BYTES,
        "final_manifest_sha256": FINAL_MANIFEST_SHA, "final_manifest_bytes": FINAL_MANIFEST_BYTES,
        "snapshot": str(SNAP), "snapshot_head": "e746a5dbb8ad657feb0e2a4c7602a79239c878ba",
        "fixture_work": str(work), "fixture_head": head,
        "issue": issue, "prop": prop, "route": "WEEKLY_GENERATED_V2",
        "basis_rel": basis_rel, "proof_rel": proof_rel,
        "basis_sha256": basis_doc.get("basis_sha256"), "proof_sha256": proof_doc.get("proof_sha256"),
        "basis_file_sha256": out.get("basis_file_sha256"), "closure_len": len(closure),
        "executor": executor_id, "executor_note": "synthetic test executor only, NOT Human approval; no PDF/RELEASED claim",
        "scope": "weekly only; longform via existing 7/8/3 consumers + family 6/graph 8 (labelled, not re-proven here)",
    }
    (data / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"persisted basis/proof/manifest closure_len={len(closure)}", flush=True)

    # SAME stored proof drift refusal (no rewritten rows/digest)
    proof_before = (work / proof_rel).read_bytes()
    basis_before = (work / basis_rel).read_bytes()
    target_rel = "scripts/survey_research_authority_v2.py"  # CURRENT closure member, G76 7-file, Evidence-scaling LOW
    target = work / target_rel
    orig = target.read_bytes()
    target.write_bytes(orig + b"\n# current-supplement drift probe\n")
    try:
        try:
            src.verify_renewal_source_proof(work, basis_rel, proof_rel)
            raise SystemExit("DRIFT_UNEXPECTED_PASS: SAME proof passed after CURRENT tool mutation (must refuse)")
        except Exception as e:
            msg_e = f"{type(e).__name__}: {e}"
            # exact intended freshness refusal: CURRENT tool drift (contract/closure/Git-anchored)
            assert "BASIS_CURRENT_TOOL_DRIFT" in msg_e or "RENEWAL_PROOF_DIGEST" in msg_e or "HISTORY_TOOL_EPOCH_DRIFT" in msg_e, f"wrong refusal code: {msg_e[:500]}"
            print(f"DRIFT_REFUSED {msg_e[:300]}", flush=True)
            (data / "drift-refusal.txt").write_text(msg_e + "\n", encoding="utf-8")
        # SAME stored proof files unchanged (not rewritten)
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
    # historical data unchanged: basis/proof still same SHA as persisted
    assert _sha_file(work / basis_rel) == _sha_bytes(basis_before) or _sha_file(work / basis_rel) == hashlib.sha256(basis_before).hexdigest(), "basis changed"
    print("historical basis/proof data unchanged (SAME bytes)", flush=True)
    print("CURRENT_SUPPLEMENT_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
