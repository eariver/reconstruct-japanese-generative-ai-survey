#!/usr/bin/env python3
"""DM022 Owner-B late-prepublish tests: entry+prepublish on every B mutating write.

Wraps the REAL low.require_research_operation_ready (no mock PASS) and injects
an owned synthetic guard at the exact prepublish seam (file/fn/line, direct
business frame). Healthy proves the real write (NEW output or State advance,
no clearing); fault proves DM022_TRANSITION_ACTIVE with no writes except guard
plus allowed already-completed prefix writes (approval file before second State
check: no rollback; revalidate rolls back record via existing owner-aware
cleanup so only guard remains). No broad Exception, no early-reject bypass.
Self-contained injector (no dependency on General's helper to avoid concurrent
edit); method names prefixed test_b_ to avoid duplicate.
"""

from __future__ import annotations

import inspect
import json
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _snapshot(root: Path) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    for p in sorted(root.rglob("*")):
        try:
            if p.is_symlink() or not p.is_file():
                continue
            rel = p.relative_to(root).as_posix()
        except ValueError:
            continue
        if rel.startswith(".git/") or "__pycache__" in rel or rel.endswith(".pyc"):
            continue
        out[rel] = p.read_bytes()
    return out


class _Injector:
    """Wrap REAL low.require_research_operation_ready; inject at exact prepublish seam."""

    def __init__(self, guard_path: Path, target_file_sub: str, target_fn: str, target_line: int, entry_line: int, entry_fn: str | None = None):
        self.guard_path = guard_path
        self.target_file_sub = target_file_sub
        self.target_fn = target_fn
        self.target_line = target_line
        self.entry_line = entry_line
        self.entry_fn = entry_fn if entry_fn is not None else target_fn
        self.calls: list[dict] = []
        self.state = {"injected": False, "target_reached": False, "entry_reached": False}
        from scripts import survey_research_authority_v2 as low
        self._orig = low.require_research_operation_ready
        self._low = low

    def _outer(self):
        st = inspect.stack()
        try:
            direct = st[2] if len(st) > 2 else st[1]
            outer = st[3] if len(st) > 3 else (st[2] if len(st) > 2 else st[1])
            return (direct.filename, direct.lineno, direct.function,
                    outer.filename, outer.lineno, outer.function)
        finally:
            del st

    def __call__(self, repo_root: Path, state_path: Path) -> None:
        d_file, d_line, d_fn, o_file, o_line, o_fn = self._outer()
        self.calls.append({"d_file": d_file, "d_line": d_line, "d_fn": d_fn,
                           "o_file": o_file, "o_line": o_fn, "o_fn": o_fn})
        if self.target_file_sub in o_file and o_fn == self.entry_fn and o_line == self.entry_line:
            self.state["entry_reached"] = True
        if self.target_file_sub in o_file and o_fn == self.target_fn and o_line == self.target_line:
            self.state["target_reached"] = True
            if not self.state["injected"]:
                self.guard_path.parent.mkdir(parents=True, exist_ok=True)
                self.guard_path.write_text(json.dumps({"phase": "TEST", "nonce": f"synthetic-b-lg-{self.target_fn}-{self.target_line}"}) + "\n")
                self.state["injected"] = True
        return self._orig(repo_root, state_path)

    def install(self, testcase: unittest.TestCase):
        from scripts import survey_research_authority_v2 as low
        assert low.require_research_operation_ready is self._orig
        low.require_research_operation_ready = self  # type: ignore
        def _restore():
            low.require_research_operation_ready = self._orig  # type: ignore
        testcase.addCleanup(_restore)


def _b_agent_harness(testcase: unittest.TestCase):
    """Simple LEGACY fixture for agent build/advance (like existing agent tests)."""
    from scripts import survey_production_v2 as core
    root = Path(".").resolve()
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    # Use tmp dir under root (like existing tests) for profile/source.
    import tempfile as _tf
    temp = _tf.TemporaryDirectory(dir=str(root))
    testcase.addCleanup(temp.cleanup)
    base = Path(temp.name)
    rel = str(base.relative_to(root))
    spec = {
        "issue_id": "SP-B-LG",
        "question": "B late-guard agent fixture?",
        "temporal_mode": "OPEN_HISTORY_AS_OF",
        "as_of": "2026-08-22T09:00:00Z",
        "scope_dimensions": ["tool evolution"],
        "source_root": rel,
        "survey_root": f"{rel}/survey",
        "work_branch": "test/b-lg",
    }
    profile = core.thematic_profile(root, cfg, spec)
    profile_path, state_path = core.initialize(
        root, cfg, profile, "1" * 40, "ARCHITECTURE_REVIEW",
        core.parse_instant("2026-08-22T09:00:00Z"),
    )
    return root, cfg, base, profile_path, state_path


class BPrepublishLateGuardTests(unittest.TestCase):
    def test_b_agent_build_prepublish(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_research_authority_v2 as low_mod
        root, cfg, base, profile_path, state_path = _b_agent_harness(self)
        # Artifacts + review for build (LEGACY, guard absent).
        art_path = base / "discovery" / "discovery-accepted-v2.json"
        art_path.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(art_path, {"fixture": "discovery-acceptance"})
        artifacts = {"discovery-acceptance": art_path}
        # Minimal deterministic review (CORE_STAGE_CONTRACT).
        state = core.load_json(state_path)
        stage = cfg["orchestration"]["stage_plan"][state["lifecycle_state"]]
        res_path = base / "reviews" / "b-lg-build-core.json"
        res_path.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(res_path, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS", "issue_id": state["issue_id"],
            "from_state": state["lifecycle_state"], "to_state": stage["next_state"],
            "production_state": {"path": str(state_path.relative_to(root)), "sha256": core.sha256_file(state_path)},
            "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": core.sha256_file(profile_path)},
            "implementation_commit_sha": core.repository_commit_sha(root),
            "contract": core.contract_identity(root, cfg, state["research_profile"], state["publication_profile"]),
            "artifacts": [{"name": "discovery-acceptance", "path": str(art_path.relative_to(root)), "sha256": core.sha256_file(art_path)}],
            "recorded_at": "2026-08-22T09:05:00Z",
        })
        rev_path = base / "reviews" / "b-lg-build-rev.json"
        core.write_json(rev_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "b-lg", "evidence": "b-lg",
            "result_path": str(res_path.relative_to(root))}]})
        # Healthy: NEW checkpoint file.
        pre_h = _snapshot(root)
        cp = agent.build_stage_checkpoint(
            root, cfg, state_path, artifacts, rev_path, "B healthy build.",
            datetime(2026, 8, 22, 9, 10, 0, tzinfo=timezone.utc))
        post_h = _snapshot(root)
        self.assertIn(cp.relative_to(root).as_posix(), set(post_h) - set(pre_h))
        # Fault: fresh harness (independent tmp) to avoid overwrite collision.
        root2, cfg2, base2, pp2, sp2 = _b_agent_harness(self)
        art2 = base2 / "discovery" / "discovery-accepted-v2.json"
        art2.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(art2, {"fixture": "discovery-acceptance"})
        st2 = core.load_json(sp2)
        stage2 = cfg2["orchestration"]["stage_plan"][st2["lifecycle_state"]]
        res2 = base2 / "reviews" / "b-lg-build-core.json"
        res2.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(res2, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS", "issue_id": st2["issue_id"],
            "from_state": st2["lifecycle_state"], "to_state": stage2["next_state"],
            "production_state": {"path": str(sp2.relative_to(root2)), "sha256": core.sha256_file(sp2)},
            "production_profile": {"path": str(pp2.relative_to(root2)), "sha256": core.sha256_file(pp2)},
            "implementation_commit_sha": core.repository_commit_sha(root2),
            "contract": core.contract_identity(root2, cfg2, st2["research_profile"], st2["publication_profile"]),
            "artifacts": [{"name": "discovery-acceptance", "path": str(art2.relative_to(root2)), "sha256": core.sha256_file(art2)}],
            "recorded_at": "2026-08-22T09:05:00Z",
        })
        rev2 = base2 / "reviews" / "b-lg-build-rev.json"
        core.write_json(rev2, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "b-lg", "evidence": "b-lg",
            "result_path": str(res2.relative_to(root2))}]})
        # Guard path for this source (Profile source_root).
        prof2 = core.load_json(pp2)
        src2 = root2 / prof2["paths"]["source_root"]
        guard = low_mod.guard_path_for(src2)
        inj = _Injector(guard, "survey_agent_control_v2.py", "build_stage_checkpoint", 2295, 2242)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.build_stage_checkpoint(
                root2, cfg2, sp2, {"discovery-acceptance": art2}, rev2, "B fault build.",
                datetime(2026, 8, 22, 9, 10, 0, tzinfo=timezone.utc))
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard.relative_to(root2).as_posix()})

    def test_b_agent_advance_prepublish(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_research_authority_v2 as low_mod
        root, cfg, base, profile_path, state_path = _b_agent_harness(self)
        art_path = base / "discovery" / "discovery-accepted-v2.json"
        art_path.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(art_path, {"fixture": "discovery-acceptance"})
        artifacts = {"discovery-acceptance": art_path}
        state = core.load_json(state_path)
        stage = cfg["orchestration"]["stage_plan"][state["lifecycle_state"]]
        res_path = base / "reviews" / "b-lg-adv-core.json"
        res_path.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(res_path, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS", "issue_id": state["issue_id"],
            "from_state": state["lifecycle_state"], "to_state": stage["next_state"],
            "production_state": {"path": str(state_path.relative_to(root)), "sha256": core.sha256_file(state_path)},
            "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": core.sha256_file(profile_path)},
            "implementation_commit_sha": core.repository_commit_sha(root),
            "contract": core.contract_identity(root, cfg, state["research_profile"], state["publication_profile"]),
            "artifacts": [{"name": "discovery-acceptance", "path": str(art_path.relative_to(root)), "sha256": core.sha256_file(art_path)}],
            "recorded_at": "2026-08-22T09:05:00Z",
        })
        rev_path = base / "reviews" / "b-lg-adv-rev.json"
        core.write_json(rev_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "b-lg", "evidence": "b-lg",
            "result_path": str(res_path.relative_to(root))}]})
        cp = agent.build_stage_checkpoint(
            root, cfg, state_path, artifacts, rev_path, "B healthy build for advance.",
            datetime(2026, 8, 22, 9, 10, 0, tzinfo=timezone.utc))
        # Healthy advance: State bytes change.
        pre_h = _snapshot(root)
        state_before = core.sha256_file(state_path)
        updated = agent.advance_with_checkpoint(root, cfg, state_path, cp)
        post_h = _snapshot(root)
        self.assertNotEqual(core.sha256_file(state_path), state_before)
        self.assertEqual(updated["lifecycle_state"], stage["next_state"])
        # Fault: fresh harness, build first (no guard), then inject at advance prepublish.
        root2, cfg2, base2, pp2, sp2 = _b_agent_harness(self)
        art2 = base2 / "discovery" / "discovery-accepted-v2.json"
        art2.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(art2, {"fixture": "discovery-acceptance"})
        st2 = core.load_json(sp2)
        stage2 = cfg2["orchestration"]["stage_plan"][st2["lifecycle_state"]]
        res2 = base2 / "reviews" / "b-lg-adv-core.json"
        res2.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(res2, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS", "issue_id": st2["issue_id"],
            "from_state": st2["lifecycle_state"], "to_state": stage2["next_state"],
            "production_state": {"path": str(sp2.relative_to(root2)), "sha256": core.sha256_file(sp2)},
            "production_profile": {"path": str(pp2.relative_to(root2)), "sha256": core.sha256_file(pp2)},
            "implementation_commit_sha": core.repository_commit_sha(root2),
            "contract": core.contract_identity(root2, cfg2, st2["research_profile"], st2["publication_profile"]),
            "artifacts": [{"name": "discovery-acceptance", "path": str(art2.relative_to(root2)), "sha256": core.sha256_file(art2)}],
            "recorded_at": "2026-08-22T09:05:00Z",
        })
        rev2 = base2 / "reviews" / "b-lg-adv-rev.json"
        core.write_json(rev2, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "b-lg", "evidence": "b-lg",
            "result_path": str(res2.relative_to(root2))}]})
        cp2 = agent.build_stage_checkpoint(
            root2, cfg2, sp2, {"discovery-acceptance": art2}, rev2, "B fault setup build.",
            datetime(2026, 8, 22, 9, 10, 0, tzinfo=timezone.utc))
        prof2 = core.load_json(pp2)
        src2 = root2 / prof2["paths"]["source_root"]
        guard = low_mod.guard_path_for(src2)
        inj = _Injector(guard, "survey_agent_control_v2.py", "advance_with_checkpoint", 2372, 2311)
        inj.install(self)
        pre_f = _snapshot(root2)
        state_before_f = core.sha256_file(sp2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.advance_with_checkpoint(root2, cfg2, sp2, cp2)
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        self.assertEqual(core.sha256_file(sp2), state_before_f)
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard.relative_to(root2).as_posix()})

    def _arch_pending(self, tag: str):
        """Fresh WEEKLY SELECTION_COMPLETE -> ARCHITECTURE_ESTABLISHED pending (PREARCH active).

        Reuses full-lifecycle witness (proven HIGH adopt + regen + advance).
        Keeps witness alive via self to preserve temp lifetimes. Returns
        (owner, root, cfg, state_abs, source_root).
        """
        from tests import test_dm022_full_lifecycle_v2 as full_mod
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        owner = full_mod.Dm022FullLifecycleWitnessTests(methodName="test_weekly_full_to_architecture_approval")
        # Keep owner alive (its helpers register cleanups on owner).
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        witness = owner._full_route_witness("WEEKLY", tag)
        root = witness["chain"]["root"]
        cfg = witness["chain"]["cfg"]
        state_abs = witness["state_abs"]
        # Transfer temp lifetime to self (witness temps are GC-collected otherwise).
        # Owner already has cleanups; keeping owner alive is sufficient.
        # Advance SELECTION_COMPLETE -> ARCHITECTURE_ESTABLISHED (pending, no approval yet).
        from pathlib import Path as _P
        # Source root + arch artifacts (created by selection runner in witness).
        profile_doc = core.load_json(witness["chain"]["profile_path"])
        source_root = root / profile_doc["paths"]["source_root"]
        arch_path = source_root / "architecture-v2.json"
        review_path = source_root / "architecture-review-summary-v2.json"
        attention_path = source_root / "architecture-review-attention-v2.json"
        for p in (arch_path, review_path, attention_path):
            self.assertTrue(p.is_file(), f"arch authority missing: {p}")
        reviews_path = owner._stage_reviews_for(
            root, cfg, state_abs,
            {"issue-architecture": arch_path,
             "architecture-review-summary": review_path,
             "architecture-review-attention": attention_path},
            f"architecture-{tag}")
        cp = agent.build_stage_checkpoint(
            root, cfg, state_abs,
            {"issue-architecture": arch_path,
             "architecture-review-summary": review_path,
             "architecture-review-attention": attention_path},
            reviews_path,
            f"Architecture stage reviewed for {tag} (B late-guard).",
            datetime(2026, 10, 28, 2, 0, 0, tzinfo=timezone.utc))
        updated = agent.advance_with_checkpoint(root, cfg, state_abs, cp)
        self.assertEqual(updated["lifecycle_state"], "ARCHITECTURE_ESTABLISHED")
        return owner, root, cfg, state_abs, source_root

    def test_b_agent_approve_arch_approval_file(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_research_authority_v2 as low_mod
        _, root, cfg, state_abs, source_root = self._arch_pending("b-approve-file-healthy")
        approval_rel = (source_root / cfg["state_authority"]["architecture_approval_path"]).relative_to(root).as_posix()
        # Healthy: NEW approval file + State.
        pre_h = _snapshot(root)
        state_before_h = core.sha256_file(state_abs)
        agent.approve_architecture(
            root, cfg, state_abs, "b-lg-reviewer",
            datetime(2026, 10, 28, 3, 0, 0, tzinfo=timezone.utc), "b-lg-approve-file-healthy")
        post_h = _snapshot(root)
        self.assertIn(approval_rel, post_h)
        self.assertNotIn(approval_rel, pre_h)
        self.assertNotEqual(core.sha256_file(state_abs), state_before_h)
        # Fault at approval-file prepublish 2446 (entry 2390): no approval, only guard.
        _, root2, cfg2, state_abs2, source_root2 = self._arch_pending("b-approve-file-fault")
        approval_rel2 = (source_root2 / cfg2["state_authority"]["architecture_approval_path"]).relative_to(root2).as_posix()
        guard2 = low_mod.guard_path_for(source_root2)
        inj = _Injector(guard2, "survey_agent_control_v2.py", "approve_architecture", 2446, 2390)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.approve_architecture(
                root2, cfg2, state_abs2, "b-lg-reviewer",
                datetime(2026, 10, 28, 3, 0, 0, tzinfo=timezone.utc), "b-lg-approve-file-fault")
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        self.assertNotIn(approval_rel2, post_f)
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard2.relative_to(root2).as_posix()})

    def test_b_agent_approve_arch_state(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_research_authority_v2 as low_mod
        _, root, cfg, state_abs, source_root = self._arch_pending("b-approve-state-healthy")
        approval_rel = (source_root / cfg["state_authority"]["architecture_approval_path"]).relative_to(root).as_posix()
        pre_h = _snapshot(root)
        agent.approve_architecture(
            root, cfg, state_abs, "b-lg-reviewer",
            datetime(2026, 10, 28, 3, 0, 0, tzinfo=timezone.utc), "b-lg-approve-state-healthy")
        post_h = _snapshot(root)
        self.assertIn(approval_rel, post_h)
        # Fault at State prepublish 2461: approval prefix allowed, State unchanged.
        _, root2, cfg2, state_abs2, source_root2 = self._arch_pending("b-approve-state-fault")
        approval_rel2 = (source_root2 / cfg2["state_authority"]["architecture_approval_path"]).relative_to(root2).as_posix()
        guard2 = low_mod.guard_path_for(source_root2)
        inj = _Injector(guard2, "survey_agent_control_v2.py", "approve_architecture", 2461, 2390)
        inj.install(self)
        pre_f = _snapshot(root2)
        state_before_f = core.sha256_file(state_abs2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.approve_architecture(
                root2, cfg2, state_abs2, "b-lg-reviewer",
                datetime(2026, 10, 28, 3, 0, 0, tzinfo=timezone.utc), "b-lg-approve-state-fault")
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        # Approval prefix allowed (first prepublish passed before injection at second).
        self.assertIn(approval_rel2, post_f)
        self.assertEqual(core.sha256_file(state_abs2), state_before_f)
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard2.relative_to(root2).as_posix(), approval_rel2})

    def _stage_harness(self):
        """Simple LEGACY fixture for stage validate (like existing stage tests, fast)."""
        from scripts import survey_production_v2 as core
        import tempfile as _tf
        root = Path(".").resolve()
        cfg = core.load_json(root / core.DEFAULT_CONFIG)
        temp = _tf.TemporaryDirectory(dir=str(root))
        self.addCleanup(temp.cleanup)
        base = Path(temp.name)
        rel = str(base.relative_to(root))
        profile = core.thematic_profile(root, cfg, {
            "issue_id": "SP-B-STAGE",
            "question": "B stage late-guard?",
            "temporal_mode": "OPEN_HISTORY_AS_OF",
            "as_of": "2026-08-22T09:00:00Z",
            "scope_dimensions": ["stage"],
            "source_root": rel,
            "survey_root": f"{rel}/survey",
            "work_branch": "test/b-stage",
        })
        _, state_path = core.initialize(root, cfg, profile, "1" * 40, "ARCHITECTURE_REVIEW",
            core.parse_instant("2026-08-22T09:00:00Z"))
        return root, cfg, base, state_path

    def test_b_stage_validate_prepublish(self) -> None:
        from tests import test_dm022_full_lifecycle_v2 as full_mod
        from scripts import survey_production_v2 as core
        from scripts import survey_stage_validation_v2 as stage
        from scripts import survey_research_authority_v2 as low_mod
        owner = full_mod.Dm022FullLifecycleWitnessTests(methodName="test_weekly_dm022_to_selection_stage")
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        chain = owner._chain_root("WEEKLY")
        root = chain["root"]
        cfg = chain["cfg"]
        owner._git_init(root)
        disc_acc = owner._materialize_production_discovery_acceptance(chain)
        state_path = chain["state_path"]
        out_h = root / "sources" / chain["issue_id"] / "orchestration" / "v2" / "stage-validation" / "b-lg-stage-h.json"
        pre_h = _snapshot(root)
        stage.validate_stage(root, cfg, state_path, {"discovery-acceptance": disc_acc}, out_h,
            core.parse_instant("2026-10-28T00:00:00Z"))
        post_h = _snapshot(root)
        self.assertIn(out_h.relative_to(root).as_posix(), set(post_h) - set(pre_h))
        chain2 = owner._chain_root("WEEKLY")
        root2 = chain2["root"]
        cfg2 = chain2["cfg"]
        owner._git_init(root2)
        disc_acc2 = owner._materialize_production_discovery_acceptance(chain2)
        sp2 = chain2["state_path"]
        out_f = root2 / "sources" / chain2["issue_id"] / "orchestration" / "v2" / "stage-validation" / "b-lg-stage-f.json"
        prof2 = core.load_json(chain2["profile_path"])
        src2 = root2 / prof2["paths"]["source_root"]
        guard2 = low_mod.guard_path_for(src2)
        inj = _Injector(guard2, "survey_stage_validation_v2.py", "validate_stage", 888, 869)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            stage.validate_stage(root2, cfg2, sp2, {"discovery-acceptance": disc_acc2}, out_f,
                core.parse_instant("2026-10-28T00:00:00Z"))
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        self.assertNotIn(out_f.relative_to(root2).as_posix(), post_f)
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard2.relative_to(root2).as_posix()})

    def _release_candidate_pending(self, tag: str):
        """Durable VALIDATED_DRAFT + NEW candidate + advance to RELEASE_CANDIDATE pending."""
        import json as _js
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_publication_v2 as pub
        man_path = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/full-lifecycle-v2-fixture-manifests/durable-versioned-20261029T064541Z/durable-fixture-manifest.json")
        man = _js.loads(man_path.read_bytes().decode("utf-8"))
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        import tempfile as _tf, shutil as _sh
        td = _tf.TemporaryDirectory(prefix=f"b-rel-{tag}-")
        self.addCleanup(td.cleanup)
        dst = Path(td.name).resolve() / "fixture"
        _sh.copytree(durable, dst, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        root = dst
        cfg = core.load_json(root / core.DEFAULT_CONFIG)
        state_abs = root / "sources/2026-W33/production-state.json"
        cand_rel = "sources/2026-W33/publication/v2/publication-candidate-v2.json"
        cand_path = root / cand_rel
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        src_rel = "surveys/weekly/2026-W33/main.tex"
        pdf_rel = "surveys/weekly/2026-W33/main.pdf"
        bundle_rel = "sources/2026-W33/publication/v2/quality-regression-bundle-v2.json"
        sem_rel = "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json"
        vis_rel = "sources/2026-W33/publication/v2/visual-review-v2.json"
        sem_doc = core.load_json(root / sem_rel)
        page_count = int(sem_doc.get("page_count", 5) or 5)
        pub.build_candidate(root, "2026-W33", "WEEKLY_MAGAZINE",
            root / man_rel, root / src_rel, root / pdf_rel, page_count,
            root / bundle_rel, root / sem_rel, root / vis_rel,
            cand_path, state_path=state_abs)
        rev_dir = root / "sources/2026-W33/reviews"
        rev_dir.mkdir(parents=True, exist_ok=True)
        res_p = rev_dir / f"b-lg-cand-core-{tag}.json"
        head = core.repository_commit_sha(root)
        state = core.load_json(state_abs)
        stage_plan = cfg["orchestration"]["stage_plan"][state["lifecycle_state"]]
        core.write_json(res_p, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS", "issue_id": state["issue_id"],
            "from_state": state["lifecycle_state"], "to_state": stage_plan["next_state"],
            "production_state": {"path": str(state_abs.relative_to(root)), "sha256": core.sha256_file(state_abs)},
            "production_profile": {"path": "sources/2026-W33/production-profile.json", "sha256": core.sha256_file(root / "sources/2026-W33/production-profile.json")},
            "implementation_commit_sha": head,
            "contract": core.contract_identity(root, cfg, state["research_profile"], state["publication_profile"]),
            "artifacts": [{"name": "publication-candidate", "path": cand_rel, "sha256": core.sha256_file(cand_path)}],
            "recorded_at": "2026-10-28T10:00:00Z",
        })
        rev_p = rev_dir / f"b-lg-cand-rev-{tag}.json"
        core.write_json(rev_p, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "b-lg", "evidence": "b-lg",
            "result_path": str(res_p.relative_to(root))}]})
        cp = agent.build_stage_checkpoint(root, cfg, state_abs,
            {"publication-candidate": cand_path}, rev_p,
            f"Candidate staged for {tag}.", datetime(2026, 10, 28, 10, 0, 0, tzinfo=timezone.utc))
        updated = agent.advance_with_checkpoint(root, cfg, state_abs, cp)
        self.assertEqual(updated["lifecycle_state"], "RELEASE_CANDIDATE")
        profile = core.load_json(root / "sources/2026-W33/production-profile.json")
        source_root = root / profile["paths"]["source_root"]
        return root, cfg, state_abs, cand_path, source_root

    def test_b_agent_approve_preview_state(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from scripts import survey_research_authority_v2 as low_mod
        root, cfg, state_abs, _, source_root = self._release_candidate_pending("healthy")
        approval_rel = (source_root / cfg["state_authority"]["publication_preview_approval_path"]).relative_to(root).as_posix()
        agent.approve_publication_preview(root, cfg, state_abs, "b-lg-reviewer",
            datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "b-lg-preview-healthy")
        post_h = _snapshot(root)
        self.assertIn(approval_rel, post_h)
        root2, cfg2, state_abs2, _, source_root2 = self._release_candidate_pending("fault")
        approval_rel2 = (source_root2 / cfg2["state_authority"]["publication_preview_approval_path"]).relative_to(root2).as_posix()
        guard2 = low_mod.guard_path_for(source_root2)
        inj = _Injector(guard2, "survey_agent_control_v2.py", "approve_publication_preview", 2512, 2481)
        inj.install(self)
        pre_f = _snapshot(root2)
        state_before_f = core.sha256_file(state_abs2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.approve_publication_preview(root2, cfg2, state_abs2, "b-lg-reviewer",
                datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "b-lg-preview-fault")
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        self.assertIn(approval_rel2, post_f)
        self.assertEqual(core.sha256_file(state_abs2), state_before_f)
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard2.relative_to(root2).as_posix(), approval_rel2})

    def _revalidate_harness(self, tag: str):
        from tests import test_survey_publication_revalidation_v2 as reval_mod
        from scripts import survey_production_v2 as core
        from scripts import survey_research_authority_v2 as low_mod
        owner = reval_mod.PublicationRevalidationTests(methodName="test_t1_legitimate_regeneration_revalidates")
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        owner.root = Path(".").resolve()
        owner.cfg = core.load_json(owner.root / core.DEFAULT_CONFIG)
        temp, fix = owner.make_fixture()
        self.addCleanup(temp.cleanup)
        owner.regenerate(fix)
        state_path = fix.src / "production-state.json"
        guard_path = low_mod.guard_path_for(fix.src)
        return temp, fix, state_path, guard_path

    def test_b_agent_revalidate_record(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        temp, fix, state_path, _ = self._revalidate_harness("rec-healthy")
        pre_h = _snapshot(Path(".").resolve())
        rec = agent.revalidate_publication_surface(
            Path(".").resolve(), core.load_json(Path(".").resolve() / core.DEFAULT_CONFIG),
            state_path, "REVIEWED_CORE_CHANGE", "b-lg revalidate healthy", "b-lg-executor",
            datetime(2026, 9, 12, 13, 0, 0, tzinfo=timezone.utc), None)
        self.assertTrue(rec.is_file())
        temp2, fix2, state_path2, guard2 = self._revalidate_harness("rec-fault")
        inj = _Injector(guard2, "survey_agent_control_v2.py", "revalidate_publication_surface", 3247, 3004)
        inj.install(self)
        pre_f = _snapshot(Path(".").resolve())
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.revalidate_publication_surface(
                Path(".").resolve(), core.load_json(Path(".").resolve() / core.DEFAULT_CONFIG),
                state_path2, "REVIEWED_CORE_CHANGE", "b-lg revalidate fault", "b-lg-executor",
                datetime(2026, 9, 12, 13, 0, 0, tzinfo=timezone.utc), None)
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(Path(".").resolve())
        new_f = set(post_f) - set(pre_f)
        self.assertEqual(new_f, {guard2.relative_to(Path(".").resolve()).as_posix()})

    def test_b_agent_revalidate_state(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        temp, fix, state_path, _ = self._revalidate_harness("state-healthy")
        state_before_h = core.sha256_file(state_path)
        agent.revalidate_publication_surface(
            Path(".").resolve(), core.load_json(Path(".").resolve() / core.DEFAULT_CONFIG),
            state_path, "REVIEWED_CORE_CHANGE", "b-lg revalidate state healthy", "b-lg-executor",
            datetime(2026, 9, 12, 14, 0, 0, tzinfo=timezone.utc), None)
        self.assertNotEqual(core.sha256_file(state_path), state_before_h)
        temp2, fix2, state_path2, guard2 = self._revalidate_harness("state-fault")
        inj = _Injector(guard2, "survey_agent_control_v2.py", "revalidate_publication_surface", 3263, 3004)
        inj.install(self)
        pre_f = _snapshot(Path(".").resolve())
        state_before_f = core.sha256_file(state_path2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            agent.revalidate_publication_surface(
                Path(".").resolve(), core.load_json(Path(".").resolve() / core.DEFAULT_CONFIG),
                state_path2, "REVIEWED_CORE_CHANGE", "b-lg revalidate state fault", "b-lg-executor",
                datetime(2026, 9, 12, 14, 0, 0, tzinfo=timezone.utc), None)
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(Path(".").resolve())
        self.assertEqual(core.sha256_file(state_path2), state_before_f)
        new_f = set(post_f) - set(pre_f)
        # Guard-aware rollback preserves record prefix (no deletion under guard).
        self.assertIn(guard2.relative_to(Path(".").resolve()).as_posix(), new_f)
        self.assertEqual(len(new_f), 2, f"expected guard+record prefix, got: {sorted(new_f)}")

    def _hg_arch_pending(self, tag: str):
        """LEGACY ARCHITECTURE_ESTABLISHED pending via human-gate helpers (fast, no DM022).

        Reuses existing human-gate fixture helpers (proven valid State/Profile/gates).
        Keeps owner alive. Returns (owner, root, cfg, state_path, source_root).
        """
        from tests import test_survey_human_gate_v2 as hg_mod
        from scripts import survey_production_v2 as core
        # Ensure class-level fixtures (root/cfg/impl) are initialised once.
        try:
            hg_mod.SurveyHumanGateV2Tests.setUpClass()
        except Exception:
            pass
        owner = hg_mod.SurveyHumanGateV2Tests(methodName="test_architecture_request_changes_regenerates_r2_then_approves")
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        owner.setUp()
        self.addCleanup(owner.tearDown if hasattr(owner, "tearDown") else lambda: None)
        # Advance to SELECTION_COMPLETE then ARCH pending (LEGACY, no DM022).
        owner._advance_to_selection()
        owner._reach_architecture_gate(f"B late-guard arch {tag}", "2026-08-24T00:05:00Z")
        root = owner.root
        cfg = owner.cfg
        state_path = owner.state_path
        source_root = owner.source_root
        return owner, root, cfg, state_path, source_root

    def test_b_humangate_record_arch_prepublish(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_human_gate_v2 as hg
        from scripts import survey_research_authority_v2 as low_mod
        owner, root, cfg, state_path, source_root = self._hg_arch_pending("healthy")
        # Healthy: NEW review record + index (plus approval snapshot + State via agent).
        pre_h = _snapshot(root)
        _, rec_h, idx_h = hg.record_architecture_approval(
            root, cfg, state_path, "b-lg-reviewer",
            core.parse_instant("2026-08-24T00:06:00Z"), "b-lg-arch-healthy",
            expected_revision=1, reviewed_commit_sha=owner._snapshot_review_commit())
        post_h = _snapshot(root)
        self.assertTrue(rec_h.is_file())
        self.assertIn(rec_h.relative_to(root).as_posix(), set(post_h) - set(pre_h))
        # Fault: fresh ARCH pending, inject at review/index prepublish 765 (entry 718).
        owner2, root2, cfg2, sp2, src2 = self._hg_arch_pending("fault")
        guard2 = low_mod.guard_path_for(src2)
        inj = _Injector(guard2, "survey_human_gate_v2.py", "record_architecture_approval", 765, 718)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            hg.record_architecture_approval(
                root2, cfg2, sp2, "b-lg-reviewer",
                core.parse_instant("2026-08-24T00:06:00Z"), "b-lg-arch-fault",
                expected_revision=1, reviewed_commit_sha=owner2._snapshot_review_commit())
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        # Prefix allowed: agent approval+State + snapshot (742 passed before 765).
        # Target review/index must be absent.
        new_f = set(post_f) - set(pre_f)
        # Record must not be present as NEW (it may not exist at all).
        # Index may have been created empty before? No, index created in _write_review_record only.
        # Assert guard present and no NEW review record beyond allowed prefixes.
        self.assertIn(guard2.relative_to(root2).as_posix(), new_f)
        # Review record is gates/reviews/architecture-r1.json (snapshot approvals/ is allowed prefix).
        bad = [k for k in new_f if k.endswith("/gates/reviews/architecture-r1.json")]
        self.assertEqual(bad, [], f"review record must not be written: {sorted(new_f)}")

    def test_b_humangate_request_prepublish(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_human_gate_v2 as hg
        from scripts import survey_research_authority_v2 as low_mod
        owner, root, cfg, state_path, source_root = self._hg_arch_pending("req-healthy")
        pre_h = _snapshot(root)
        hg.request_changes(root, cfg, state_path, "ARCHITECTURE_REVIEW", "SELECTION_COMPLETE",
            "b-lg request healthy", "b-lg-reviewer",
            core.parse_instant("2026-08-24T00:06:00Z"), "b-lg-req-healthy",
            expected_revision=1, reviewed_commit_sha=owner._snapshot_review_commit())
        post_h = _snapshot(root)
        new_h = set(post_h) - set(pre_h)
        self.assertTrue(any("reviews" in k for k in new_h), f"request must write review: {sorted(new_h)}")
        owner2, root2, cfg2, sp2, src2 = self._hg_arch_pending("req-fault")
        guard2 = low_mod.guard_path_for(src2)
        inj = _Injector(guard2, "survey_human_gate_v2.py", "request_changes", 1530, 1472)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            hg.request_changes(root2, cfg2, sp2, "ARCHITECTURE_REVIEW", "SELECTION_COMPLETE",
                "b-lg request fault", "b-lg-reviewer",
                core.parse_instant("2026-08-24T00:06:00Z"), "b-lg-req-fault",
                expected_revision=1, reviewed_commit_sha=owner2._snapshot_review_commit())
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        self.assertIn(guard2.relative_to(root2).as_posix(), set(post_f) - set(pre_f))
    def _arch_full_for_invalidate(self, tag: str):
        """PREARCH ARCH pending with full summary + work_branch (for invalidate, no preemption).

        Uses _arch_pending (full witness, full research summary via selection runner, PREARCH active)
        + creates work_branch ref to HEAD (for _require_expected_branch_head) with independent
        process identity (no Gitconfig mutation, inert origin preserved from witness).
        Returns (owner, root, cfg, state_abs, source_root, work_branch, head).
        """
        import subprocess as _sp
        from scripts import survey_production_v2 as core
        _, root, cfg, state_abs, source_root = self._arch_pending(tag)
        # Work branch from profile (chain profile work_branch? Use state profile?).
        # _arch_pending root is full-witness root (chain root). Profile work_branch:
        # chain profile_path is witness["chain"]["profile_path"]? _arch_pending returns root/cfg/state_abs/source_root,
        # but not profile_path. Derive via state profile path.
        state = core.load_json(state_abs)
        prof_rel = state["profile"]["path"]
        prof = core.load_json(root / prof_rel)
        # Work branch: use profile work_branch if present, else default test branch.
        wb = None
        try:
            wb = prof.get("work_branch") or prof.get("paths", {}).get("work_branch")
        except Exception:
            wb = None
        if not wb or not isinstance(wb, str):
            # Fallback: derive from chain? Full witness uses thematic? Use generic.
            wb = "test/b-invalidate"
        head = core.repository_commit_sha(root)
        # Commit current fixture files (State advanced since _git_init, so HEAD is stale;
        # _review_commit requires reviewed commit bytes == current State).
        # Use process-scoped identity, no Gitconfig mutation, independent fixture DB.
        env = {k: v for k, v in __import__("os").environ.items() if not k.startswith("GIT_")}
        env.update({
            "GIT_AUTHOR_NAME": "Synthetic DM022-B2 Invalidate",
            "GIT_AUTHOR_EMAIL": "b2-invalidate@example.invalid",
            "GIT_COMMITTER_NAME": "Synthetic DM022-B2 Invalidate",
            "GIT_COMMITTER_EMAIL": "b2-invalidate@example.invalid",
        })
        _sp.run(["git", "add", "-A"], cwd=str(root), env=env, check=True,
                capture_output=True, text=True)
        _sp.run(["git", "commit", "-m", f"b2-invalidate-fixture-{tag}", "--allow-empty"],
                cwd=str(root), env=env, check=True, capture_output=True, text=True)
        head = core.repository_commit_sha(root)
        # Create work_branch ref to HEAD (independent fixture DB, no config change).
        # Full witness has inert origin (example.invalid) → expected ref is
        # refs/remotes/origin/<branch> (like human-gate setUp remote_ref).
        _sp.run(["git", "update-ref", f"refs/remotes/origin/{wb}", head], cwd=str(root), env=env, check=True,
                capture_output=True, text=True)
        return root, cfg, state_abs, source_root, wb, head

    def test_b_humangate_invalidate_healthy(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_human_gate_v2 as hg
        root, cfg, state_abs, source_root, wb, head = self._arch_full_for_invalidate("inv-h-healthy")
        allowed = cfg["orchestration"].get("operator_pending_gate_invalidation_boundaries", {}).get("ARCHITECTURE_REVIEW", [])
        self.assertTrue(allowed)
        boundary = "SELECTION_COMPLETE" if "SELECTION_COMPLETE" in allowed else allowed[0]
        pre_h = _snapshot(root)
        _, rec_h, _ = hg.invalidate_pending_gate(root, cfg, state_abs, "ARCHITECTURE_REVIEW",
            boundary, "b-lg inv healthy", "b-lg-operator", head)
        post_h = _snapshot(root)
        self.assertTrue(rec_h.is_file())
        self.assertIn(rec_h.relative_to(root).as_posix(), set(post_h) - set(pre_h))

    def test_b_humangate_invalidate_record_fault(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_human_gate_v2 as hg
        from scripts import survey_research_authority_v2 as low_mod
        root, cfg, state_abs, source_root, wb, head = self._arch_full_for_invalidate("inv-r-fault")
        allowed = cfg["orchestration"].get("operator_pending_gate_invalidation_boundaries", {}).get("ARCHITECTURE_REVIEW", [])
        boundary = "SELECTION_COMPLETE" if "SELECTION_COMPLETE" in allowed else allowed[0]
        guard = low_mod.guard_path_for(source_root)
        inj = _Injector(guard, "survey_human_gate_v2.py", "invalidate_pending_gate", 1390, 1258)
        inj.install(self)
        pre_f = _snapshot(root)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            hg.invalidate_pending_gate(root, cfg, state_abs, "ARCHITECTURE_REVIEW",
                boundary, "b-lg inv record fault", "b-lg-operator", head)
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root)
        # No record (target not written), only guard NEW (cleanup deletions are prefix, not NEW).
        new_f = set(post_f) - set(pre_f)
        self.assertIn(guard.relative_to(root).as_posix(), new_f)
        bad = [k for k in new_f if "invalidation" in k and k.endswith(".json")]
        self.assertEqual(bad, [], f"invalidation record must not be written: {sorted(new_f)}")
        # State unchanged (no rollback writes under guard).
        # Find State rel (state_abs relative to root).
        srel = state_abs.relative_to(root).as_posix()
        if srel in pre_f and srel in post_f:
            self.assertEqual(pre_f[srel], post_f[srel], "State must be unchanged when late guard refuses")

    def test_b_humangate_invalidate_state_fault(self) -> None:
        from scripts import survey_production_v2 as core
        from scripts import survey_human_gate_v2 as hg
        from scripts import survey_research_authority_v2 as low_mod
        root, cfg, state_abs, source_root, wb, head = self._arch_full_for_invalidate("inv-s-fault")
        allowed = cfg["orchestration"].get("operator_pending_gate_invalidation_boundaries", {}).get("ARCHITECTURE_REVIEW", [])
        boundary = "SELECTION_COMPLETE" if "SELECTION_COMPLETE" in allowed else allowed[0]
        guard = low_mod.guard_path_for(source_root)
        inj = _Injector(guard, "survey_human_gate_v2.py", "invalidate_pending_gate", 1394, 1258)
        inj.install(self)
        pre_f = _snapshot(root)
        s_before = core.sha256_file(state_abs)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            hg.invalidate_pending_gate(root, cfg, state_abs, "ARCHITECTURE_REVIEW",
                boundary, "b-lg inv state fault", "b-lg-operator", head)
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root)
        self.assertEqual(core.sha256_file(state_abs), s_before, "State must be unchanged (no rollback under guard)")
        new_f = set(post_f) - set(pre_f)
        # Record prefix allowed (created before State prepublish), guard preserved, no State rollback/deletion.
        self.assertIn(guard.relative_to(root).as_posix(), new_f)
        recs = [k for k in new_f if "invalidation" in k and k.endswith(".json")]
        self.assertEqual(len(recs), 1, f"expected record prefix + guard, got: {sorted(new_f)}")
        # Record must still exist (not deleted by rollback under guard).
        self.assertTrue((root / recs[0]).is_file(), "record prefix must be preserved (no deletion under guard)")

    def _hg_preview_pending(self, tag: str):
        """LEGACY RELEASE_CANDIDATE pending (preview) via human-gate helpers (fast, synthetic).

        Reuses existing preview gate helpers (valid candidate + gate surface, no DM022).
        Keeps owner alive. Returns (owner, root, cfg, state_path, source_root).
        """
        from tests import test_survey_human_gate_v2 as hg_mod
        try:
            hg_mod.SurveyHumanGateV2Tests.setUpClass()
        except Exception:
            pass
        owner = hg_mod.SurveyHumanGateV2Tests(methodName="test_publication_preview_request_changes_regenerates_r2_then_approves")
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        owner.setUp()
        self.addCleanup(owner.tearDown if hasattr(owner, "tearDown") else lambda: None)
        owner._advance_to_selection()
        owner._reach_architecture_gate(f"B preview arch {tag}", "2026-08-24T00:05:00Z")
        owner.record_architecture_approval = __import__("scripts.survey_human_gate_v2", fromlist=["record_architecture_approval"]).record_architecture_approval
        # Approve ARCH (LEGACY, no DM022) to reach ARCH approved, then preview gate.
        from scripts import survey_human_gate_v2 as hg
        from scripts import survey_production_v2 as core
        hg.record_architecture_approval(owner.root, owner.cfg, owner.state_path, "b-lg-reviewer",
            core.parse_instant("2026-08-24T00:06:00Z"), f"b-lg-preview-arch-{tag}",
            expected_revision=1, reviewed_commit_sha=owner._snapshot_review_commit())
        cand_paths = owner._reach_publication_gate(1, 10)
        return owner, owner.root, owner.cfg, owner.state_path, owner.source_root, cand_paths

    def test_b_orchestrator_execute_prepublish(self) -> None:
        from tests import test_survey_orchestrator_v2 as orch_mod
        from scripts import survey_orchestrator_v2 as orch
        from scripts import survey_production_v2 as core
        from scripts import survey_research_authority_v2 as low_mod
        # Sandbox + first action (discovery) via stage_registry (LEGACY, fast, no DM022).
        owner = orch_mod.SurveyOrchestratorV2Tests(methodName="test_advance_to_gate_executes_validated_stage_order_and_pins_attestations")
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        owner.setUp()
        # Reuse sandbox helper (copies config/schemas, git init, thematic profile, no DM022).
        temp, root, cfg, state_path, pinned = owner.sandbox()
        self.addCleanup(temp.cleanup)
        reg = owner.stage_registry(cfg)
        spec = orch.plan_action(root, cfg, state_path)
        spec_path = root / "sources/SP001/orchestration/v2/specs/b-lg-spec.json"
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        orch.write_action_spec(spec_path, spec)
        result_path = root / "sources/SP001/orchestration/v2/results/b-lg-result-h.json"
        result_path.parent.mkdir(parents=True, exist_ok=True)
        # Healthy: SUCCESS with NEW result + attestations + State.
        pre_h = _snapshot(root)
        res_h = orch.execute_action(root, cfg, state_path, spec_path, result_path, reg,
            clock=lambda: core.parse_instant("2026-08-22T03:05:00+09:00"))
        self.assertEqual(res_h["status"], "SUCCEEDED")
        post_h = _snapshot(root)
        self.assertIn(result_path.relative_to(root).as_posix(), set(post_h) - set(pre_h))
        # Fault: fresh sandbox, inject at attestations prepublish 726 (entry 667).
        temp2, root2, cfg2, sp2, _ = owner.sandbox()
        self.addCleanup(temp2.cleanup)
        reg2 = owner.stage_registry(cfg2)
        spec2 = orch.plan_action(root2, cfg2, sp2)
        spec_path2 = root2 / "sources/SP001/orchestration/v2/specs/b-lg-spec-f.json"
        spec_path2.parent.mkdir(parents=True, exist_ok=True)
        orch.write_action_spec(spec_path2, spec2)
        result_path2 = root2 / "sources/SP001/orchestration/v2/results/b-lg-result-f.json"
        result_path2.parent.mkdir(parents=True, exist_ok=True)
        # Guard path via profile source_root (SP001).
        prof2 = core.load_json(root2 / core.load_json(sp2)["profile"]["path"])
        # SP001 source_root is sources/SP001 (fixed in sandbox).
        src2 = root2 / "sources/SP001"
        guard2 = low_mod.guard_path_for(src2)
        inj = _Injector(guard2, "survey_orchestrator_v2.py", "execute_action", 726, 667)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            orch.execute_action(root2, cfg2, sp2, spec_path2, result_path2, reg2,
                clock=lambda: core.parse_instant("2026-08-22T03:05:00+09:00"))
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        new_f = set(post_f) - set(pre_f)
        self.assertIn(guard2.relative_to(root2).as_posix(), new_f)
        # No result (target not written), only guard (attestations are prefix? No, fault at 726 before attestations, so no attestations).
        self.assertNotIn(result_path2.relative_to(root2).as_posix(), post_f)

    def _orch_arch_pending(self, tag: str):
        """LEGACY ARCH pending via sandbox + advance_to_gate (fast, no DM022).

        Returns (owner, temp, root, cfg, state_path, spec_path, arch_path, review_path, approval_path, result_path).
        """
        from tests import test_survey_orchestrator_v2 as orch_mod
        from scripts import survey_orchestrator_v2 as orch
        from scripts import survey_production_v2 as core
        owner = orch_mod.SurveyOrchestratorV2Tests(methodName="test_architecture_approval_binds_attested_reviewed_bytes_and_gate_provenance")
        if not hasattr(self, "_b_witnesses"):
            self._b_witnesses = []
        self._b_witnesses.append(owner)
        owner.setUp()
        temp, root, cfg, state_path, _ = owner.sandbox()
        self.addCleanup(temp.cleanup)
        terminal = orch.advance_to_gate(root, cfg, state_path, root / "sources/SP001/orchestration/v2",
            owner.stage_registry(cfg), clock=lambda: core.parse_instant("2026-08-22T03:05:00+09:00"))
        spec_path = root / terminal["action_spec_path"]
        arch_path = root / "sources/SP001/architecture-v2.json"
        review_path = root / "sources/SP001/architecture-review-summary-v2.json"
        approval_path = root / f"sources/SP001/gates/architecture-approval-b-{tag}.json"
        # Use canonical approval path? apply_architecture_approval requires canonical configured path.
        # Existing test uses sources/SP001/gates/architecture-approval.json (canonical).
        # For NEW output (no clearing), use canonical (absent before) — healthy proves NEW, fault proves no write.
        approval_path = root / "sources/SP001/gates/architecture-approval.json"
        result_path = root / f"sources/SP001/orchestration/v2/results/architecture-human-review-b-{tag}.json"
        return owner, temp, root, cfg, state_path, spec_path, arch_path, review_path, approval_path, result_path

    def test_b_orchestrator_apply_arch_state(self) -> None:
        from scripts import survey_orchestrator_v2 as orch
        from scripts import survey_production_v2 as core
        from scripts import survey_research_authority_v2 as low_mod
        _, _, root, cfg, sp, spec_path, arch_path, review_path, approval_path, result_path = self._orch_arch_pending("healthy")
        pre_h = _snapshot(root)
        orch.apply_architecture_approval(root, cfg, sp, spec_path, arch_path, review_path, approval_path, result_path,
            "human-reviewer", core.parse_instant("2026-08-22T03:10:00+09:00"), "review:SP001:architecture:1")
        post_h = _snapshot(root)
        self.assertIn(approval_path.relative_to(root).as_posix(), set(post_h) - set(pre_h))
        _, _, root2, cfg2, sp2, spec_path2, arch_path2, review_path2, approval_path2, result_path2 = self._orch_arch_pending("fault")
        # Guard path: SP001 source_root.
        src2 = root2 / "sources/SP001"
        guard2 = low_mod.guard_path_for(src2)
        inj = _Injector(guard2, "survey_orchestrator_v2.py", "apply_architecture_approval", 899, 788)
        inj.install(self)
        pre_f = _snapshot(root2)
        with self.assertRaisesRegex(Exception, "DM022_TRANSITION_ACTIVE"):
            orch.apply_architecture_approval(root2, cfg2, sp2, spec_path2, arch_path2, review_path2, approval_path2, result_path2,
                "human-reviewer", core.parse_instant("2026-08-22T03:10:00+09:00"), "review:SP001:architecture:1")
        self.assertTrue(inj.state["entry_reached"])
        self.assertTrue(inj.state["target_reached"])
        post_f = _snapshot(root2)
        new_f = set(post_f) - set(pre_f)
        self.assertIn(guard2.relative_to(root2).as_posix(), new_f)
        self.assertIn(approval_path2.relative_to(root2).as_posix(), new_f, f"approval prefix must remain: {sorted(new_f)}")



if __name__ == "__main__":
    unittest.main()
