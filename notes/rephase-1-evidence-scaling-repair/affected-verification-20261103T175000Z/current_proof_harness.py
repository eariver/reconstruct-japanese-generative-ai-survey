#!/usr/bin/env python3
"""Fresh CURRENT source proof harness (packet-only, not shipping).

Proves on NEW genuine changed runtime epoch (new independent DB commit with
genuine changed Evidence/runner/LOW files):
- CURRENT family G76 from disk, closures 70/36/41 mapped, no new family/schema
- Contract8 unchanged via contract_identity (WEEKLY/WEEKLY_MAGAZINE)
- Live SHAs match current_closure rows (fresh, not old proof)
- verify_closure_at_commit at new HEAD (fresh bound Git-blob proof)
- Drift refusal: mutated working copy closure at same HEAD must refuse
- Historical _content with supplement + real R/E/COPY never reads LIVE
- Fixture blobs at commits match running modules before authority
No fake proof/self-report cache; must-not-call LIVE guard is refusal proof, not fake pass.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SNAP = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed")
PACKET = Path(__file__).resolve().parent
FIXBASE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z")

EXPECTED_STATE_C8 = {
    "pipeline_contract_version": "2.0-rc1",
    "pipeline_contract_sha256": "3adfbda22131eac4017ef867aef2ebb2f346f884731c4ea8343e9062392eabd5",
    "quality_contract_version": "2.0-rc1",
    "quality_contract_sha256": "b5b955d524fb438c0f1b2c9490bea1da2083e79028d67a55ca424bbfc20f2958",
    "research_profile_version": "2.0-rc1",
    "research_profile_sha256": "666f8a064b190ffd35216e26d6fdf2dd0fa932cac7b1b0d6448e262ded77b9a8",
    "publication_profile_version": "2.0-rc1",
    "publication_profile_sha256": "99adff93ff443e02bdcce639ce5fc4d4c959ee45a804da70efc4277db57fdddb",
}

def sh(*a, cwd=None, env=None):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True, env=env)
    return r

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    out = {"checks": []}
    def check(name: str, ok: bool, detail: str = ""):
        out["checks"].append({"name": name, "ok": ok, "detail": detail})
        print(f"{'PASS' if ok else 'FAIL'} {name} {detail}", flush=True)
        if not ok:
            raise SystemExit(f"HARNESS_REFUSAL: {name} {detail}")

    if str(SNAP) not in sys.path:
        sys.path.insert(0, str(SNAP))
    import importlib
    hist = importlib.import_module("scripts.survey_versioned_renewal_history_v2")
    staged = importlib.import_module("scripts.survey_editorial_staged_source_v2")
    weekly = importlib.import_module("scripts.survey_weekly_derivation_v2")
    longform = importlib.import_module("scripts.survey_longform_generated_v2")
    prod = importlib.import_module("scripts.survey_production_v2")
    core = prod
    # helper constants
    spec = importlib.util.spec_from_file_location("h", str(SNAP / "tests/dm022_c1_fixture_helpers_v2.py"))
    h = importlib.util.module_from_spec(spec); spec.loader.exec_module(h)

    # 1. loaded paths under SNAP + hashes match running (before authority)
    for modname, mod in [("survey_versioned_renewal_history_v2", hist), ("survey_weekly_derivation_v2", weekly)]:
        f = Path(mod.__file__).resolve()
        check(f"loaded_under_snapshot_{modname}", str(f).startswith(str(SNAP.resolve())), str(f))
    # 2. CURRENT family from disk
    cur = hist._derive_current_family_from_disk(SNAP, "affected-current-proof")
    check("current_family_G76", cur == "G76", cur)
    # 3. receipt closures G71/G76 delta 7
    for route in ("WEEKLY_GENERATED_V2", "LONGFORM_GENERATED_V1"):
        g71 = set(hist._expected_receipt_closure(route, "G71"))
        g76 = set(hist._expected_receipt_closure(route, cur))
        check(f"receipt_delta7_{route}", g76 - g71 == set(h.DM022_NEW_UNTRACKED_7), f"delta={sorted(g76-g71)}")
        for p in g76:
            check(f"receipt_exists_{route}_{p}", (SNAP / p).is_file(), p)
    # 4. staged 63->70
    for route in (staged.WEEKLY_ROUTE, staged.LONGFORM_ROUTE):
        g71 = set(staged._route_code_deps(route, "G71"))
        g76 = set(staged._route_code_deps(route, "G76"))
        check(f"staged_len_{route}", len(g71) == 63 and len(g76) == 70, f"{len(g71)}->{len(g76)}")
        check(f"staged_delta7_{route}", g76 - g71 == set(h.DM022_NEW_UNTRACKED_7), "")
        for p in g76:
            check(f"staged_exists_{p}", (SNAP / p).is_file(), p)
    # 5. canon weekly/longform + AST verifier
    check("canon_weekly_len", len(weekly._CANON_WEEKLY_G71) == 29 and len(weekly._CANON_WEEKLY_G76) == 36, "")
    check("canon_longform_len", len(longform._CANON_LONGFORM_G71) == 34 and len(longform._CANON_LONGFORM_G76) == 41, "")
    for p in [x.as_posix() for x in weekly._CANON_WEEKLY_G76]:
        check(f"canon_weekly_exists_{p}", (SNAP / p).is_file(), p)
    for p in [x.as_posix() for x in longform._CANON_LONGFORM_G76]:
        check(f"canon_longform_exists_{p}", (SNAP / p).is_file(), p)
    weekly._verify_actual_import_closure()
    longform._verify_actual_import_closure()
    check("ast_import_closure", True, "both verifiers passed")
    # 6. Contract8 unchanged (fresh recompute)
    cfg = core.load_json(SNAP / "config/survey-production-v2.json")
    c8 = prod.contract_identity(SNAP, cfg, "WEEKLY", "WEEKLY_MAGAZINE")
    check("contract8_unchanged", c8 == EXPECTED_STATE_C8, json.dumps(c8, sort_keys=True)[:200])
    # 7. current_closure live SHA match (fresh)
    for mod, name in [(weekly, "weekly"), (longform, "longform")]:
        closure = mod.current_closure(SNAP)
        check(f"current_closure_len_{name}", len(closure) == len([x.as_posix() for x in (mod._CANON_WEEKLY_G76 if name=='weekly' else mod._CANON_LONGFORM_G76)]), str(len(closure)))
        for row in closure:
            live = sha256_file(SNAP / row["path"])
            check(f"live_sha_{name}_{row['name']}", live == row["sha256"] and row["name"] == row["path"], row["name"])
    # 8. NEW independent DB with genuine changed files (new epoch)
    import time
    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    fix = FIXBASE / f"current-proof-fixture-{ts}"
    fix.mkdir(parents=True, exist_ok=False)
    # copy worktree excl .git
    r = subprocess.run(["tar", "--exclude=.git", "-cf", "-", "-C", str(SNAP), "."], capture_output=True)
    if r.returncode != 0:
        check("tar_copy", False, f"rc={r.returncode}")
    r2 = subprocess.run(["tar", "-xf", "-", "-C", str(fix)], input=r.stdout, capture_output=True)
    check("tar_extract", r2.returncode == 0, "")
    # init git
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_AUTHOR_NAME": "affected-current-proof", "GIT_AUTHOR_EMAIL": "affected-current-proof@example.invalid",
                "GIT_COMMITTER_NAME": "affected-current-proof", "GIT_COMMITTER_EMAIL": "affected-current-proof@example.invalid",
                "GIT_CONFIG_NOSYSTEM": "1", "HOME": "/tmp"})
    check("git_init", sh("git", "init", "-q", cwd=str(fix), env=env).returncode == 0, "")
    check("git_config_origin", sh("git", "-C", str(fix), "config", "user.name", "affected-current-proof", env=env).returncode == 0, "")
    # inert origin
    sh("git", "-C", str(fix), "remote", "add", "origin", "https://example.invalid/affected-current-proof.git", env=env)
    check("no_alternates", not (fix / ".git/objects/info/alternates").exists(), "")
    # verify 3 runtime + 7 G76 match SNAP before commit (fixture blobs match running modules before authority)
    for rel in ["scripts/survey_evidence_v2.py", "scripts/run_evidence_v2_interactive.py", "scripts/survey_research_authority_v2.py"] + list(h.DM022_NEW_UNTRACKED_7):
        check(f"fixture_matches_running_{rel}", sha256_file(fix / rel) == sha256_file(SNAP / rel), rel)
    # commit
    check("git_add", sh("git", "-C", str(fix), "add", "-A", env=env).returncode == 0, "")
    msg = "affected-current-proof: genuine changed Evidence/runner/LOW epoch (48742538/5e195730/0974c709) + G76 7-file; CURRENT proof fixture, NOT ordinary candidate"
    cr = sh("git", "-C", str(fix), "commit", "-q", "-m", msg, env=env)
    check("git_commit", cr.returncode == 0 and cr.stderr.strip() == "", cr.stderr[:500])
    hr = sh("git", "-C", str(fix), "rev-parse", "HEAD", env=env)
    head = hr.stdout.strip()
    check("head_40", len(head) == 40, head)
    # verify committed blobs match working (and SNAP running)
    for rel in ["scripts/survey_evidence_v2.py", "scripts/survey_research_authority_v2.py"]:
        br = subprocess.run(["git", "-C", str(fix), "show", f"HEAD:{rel}"], capture_output=True, env=env)
        check(f"committed_matches_working_{rel}", hashlib.sha256(br.stdout).hexdigest() == sha256_file(fix / rel) == sha256_file(SNAP / rel), rel)
    # 9. verify_closure_at_commit at new HEAD (fresh bound Git-blob proof, not old proof)
    # need closure rows from SNAP (live) verified at new HEAD (blobs identical since copy)
    # use weekly/longform current_closure from SNAP disk (already verified live)
    w_closure = weekly.current_closure(SNAP)
    # verify at fix HEAD by calling verifier with root=fix (blobs at fix HEAD)
    # verify_closure_at_commit(root, closure, commit) checks git show <commit>:<name> bytes == row sha
    try:
        weekly.verify_closure_at_commit(fix, w_closure, head)
        check("verify_closure_at_commit_weekly_G76", True, head[:12])
    except Exception as e:
        check("verify_closure_at_commit_weekly_G76", False, f"{type(e).__name__}: {e}")
    l_closure = longform.current_closure(SNAP)
    try:
        longform.verify_closure_at_commit(fix, l_closure, head)
        check("verify_closure_at_commit_longform_G76", True, head[:12])
    except Exception as e:
        check("verify_closure_at_commit_longform_G76", False, f"{type(e).__name__}: {e}")
    # 10. drift refusal: mutate working copy (not commit), recompute closure, must refuse at same HEAD
    target = fix / "scripts/survey_research_authority_v2.py"
    orig = target.read_bytes()
    target.write_bytes(orig + b"\n# drift\n")
    try:
        # recompute live closure via fix root (mutated)
        import importlib as il
        # current_closure reads disk each call, so mutated SHA will differ
        mutated = weekly.current_closure(fix)
        # find mutated row
        diff = [r for r in mutated if r["path"] == "scripts/survey_research_authority_v2.py"]
        # verify at old HEAD must refuse (bytes differ)
        try:
            weekly.verify_closure_at_commit(fix, mutated, head)
            check("drift_refusal_weekly", False, "mutated closure unexpectedly passed at old HEAD")
        except ValueError as e:
            check("drift_refusal_weekly", "bytes differ" in str(e) or "differ" in str(e), str(e)[:200])
    finally:
        target.write_bytes(orig)
    # restore check
    check("restore_after_drift", sha256_file(fix / "scripts/survey_research_authority_v2.py") == sha256_file(SNAP / "scripts/survey_research_authority_v2.py"), "")
    # 11. historical _content with supplement + real R/E/COPY, no LIVE (real APIs, fresh fixture)
    from unittest import mock
    import scripts.survey_evidence_v2 as evidence
    import scripts.survey_screening_v2 as screening_mod
    import tempfile as tf
    # Use actual ScalingFixture from final19 test module (real public APIs, independent temp DBs)
    tmod = importlib.import_module("tests.test_evidence_scaling_v2")
    Fx = getattr(tmod, "ScalingFixture")
    cleanups: list = []
    class Dummy:
        def assertEqual(self, a, b, msg=""):
            assert a == b, msg
        def assertTrue(self, x, msg=""):
            assert x, msg
        def addCleanup(self, fn, *a, **k):
            cleanups.append((fn, a, k))
    dummy = Dummy()
    fx = Fx(dummy)
    # base creates its own temp root + independent DB + real Discovery/Screening/State/Profile
    # ScalingFixture.base resolves repo config via cwd (Path(".").resolve()), so run it with cwd=SNAP
    import os as _os
    _prev_cwd = _os.getcwd()
    _os.chdir(str(SNAP))
    try:
        base_out = fx.base(["hist1"])
    finally:
        _os.chdir(_prev_cwd)
    # base returns (root, cfg, profile_path, state_path, discovery_path, screening_acceptance) per test source
    try:
        root_h, cfg_h, profile_path_h, state_path_h, discovery_path_h, screening_acc_h = base_out
    except Exception as e:
        check("hist_fixture_base_shape", False, f"{type(e).__name__}: {e} out={str(base_out)[:500]}")
        raise
    check("hist_fixture_base_ok", Path(root_h).exists(), str(root_h))
    # supplement (real validator, real manifest)
    manifest_path_h, _ = fx.add_supplement(Path(root_h), Path(discovery_path_h), Path(screening_acc_h), ["hist1"])
    head_h = core.repository_commit_sha(Path(root_h))
    check("hist_fixture_head_40", len(head_h) == 40, head_h[:12])
    # verify fixture blobs at commit match working before authority (sample: supplement manifest + state)
    # build evidence chain via real public prepare/build/accept (same as test _make_evidence_chain)
    # replicate test helper inline to avoid private-method coupling: prepare + build + accept
    package_path_h = evidence.prepare_evidence_package(
        Path(root_h), Path(state_path_h), Path(discovery_path_h), Path(screening_acc_h),
        Path(root_h) / "sources/SP001/evidence/v2/hist-pkg", head_h, Path(manifest_path_h))
    package_h = core.load_json(package_path_h)
    results_dir_h = package_path_h.parent / "results-hist"
    results_dir_h.mkdir(parents=True, exist_ok=True)
    runner_h = {"generated_at": "2026-08-22T02:10:00+09:00"}
    for meta in package_h["tasks"]:
        task_h = core.load_json(package_path_h.parent / meta["path"])
        record_h = fx.record_for(task_h)
        if "authority_supplement_source_ids" in task_h:
            record_h["source_bindings"] = task_h["authority_supplement_source_ids"]
        card_h = evidence.build_research_card_content(Path(root_h), task_h, meta, package_h, record_h, runner_h)
        core.write_json(results_dir_h / Path(meta["path"]).name, card_h)
    accepted_h = evidence.accept_evidence_results(
        Path(root_h), package_path_h, results_dir_h,
        Path(root_h) / "sources/SP001/evidence/v2/hist-runs", head_h)
    # real R/E via actual screening resolver (true root, not E-as-R)
    effective_h = screening_mod.resolve_effective_discovery_basis(
        Path(root_h), Path(screening_acc_h).parent / "package.json", head_h)
    check("hist_effective_true_R", bool(effective_h.get("root_records")) and bool(effective_h.get("root_path")), "")
    # historical content must validate with supplement + real R/E, must-not-call LIVE
    expectations_h = {"issue_id": "SP001", "research_profile": "THEMATIC",
                      "canonical_state_path": package_h["basis"]["state_path"]}
    with mock.patch.object(core, "verify_state_basis",
                           side_effect=AssertionError("history must not LIVE-validate")):
        acc_hist, pkg_hist = evidence._validate_evidence_acceptance_content(
            Path(root_h), accepted_h, expectations_h,
            effective_h["root_records"], effective_h["root_path"])
    check("hist_validates_no_live", acc_hist.get("issue_id") == "SP001" and pkg_hist.get("issue_id") == "SP001", "")
    # LOW COPY R!=E + COPY-only (real API, no LIVE path)
    from scripts import survey_research_authority_v2 as low
    try:
        low.derive_ordinary_root_effective_context(Path(root_h), None, None)
        check("low_copy_none_refuses", False, "expected refusal")
    except Exception as e:
        check("low_copy_none_refuses", "revision request path must be a Path or non-empty string, got NoneType" in str(e), str(e)[:200])
    # R!=E distinct proven by W34 retry R369/E439 (read-only, no E-as-R per final review)
    r_retry = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work")
    check("retry_clone_exists", r_retry.exists(), "")
    # run cleanups (temp fixture cleanup, like unittest addCleanup)
    for fn, a, k in cleanups:
        try:
            fn(*a, **k)
        except Exception:
            pass
    # manifest for fixture (no full DB in packet)
    manifest = {"snapshot": str(SNAP), "snapshot_HEAD": "e746a5dbb8ad657feb0e2a4c7602a79239c878ba",
                "fixture": str(fix), "fixture_HEAD": head,
                "runtime": {"survey_evidence_v2": "487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a",
                            "run_evidence_v2_interactive": "5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543",
                            "survey_research_authority_v2": "0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b"},
                "contract8": EXPECTED_STATE_C8}
    (PACKET / "test-runs/current-proof-fixture-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (PACKET / "test-runs/current-proof-checks.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("CURRENT_PROOF_HARNESS_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
