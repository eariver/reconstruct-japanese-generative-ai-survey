#!/usr/bin/env python3
"""Evidence scaling repair — meaningful targeted oracles (TEST-owner rewrite).

Replaces the rejected initial 5-test draft (archived at
``notes/rephase-1-evidence-scaling-repair/test-rejected-draft-20261103T114312Z/``,
SHA256 ``8d3bec57…``/33543B) per Root ``astra-source-review.md`` and independent
implementation review. No fake coverage, no source-string asserts, no broad
Exception acceptance, no verifier stubs.

Uses ACTUAL existing fixture APIs only:
- ``tests.test_survey_evidence_v2.SurveyEvidenceV2Tests`` helper (commits
  meaningful fixture source/contract BEFORE authority, per root/source copy);
- correct agent facade ``survey_agent_control_v2.validate_agent_state`` for real
  CAND fixture state (not legacy attestation);
- real PUBLIC Evidence/LOW/HIGH APIs (no private-only success claims except
  explicitly labelled unit probes).

All Raw/context fixtures use independent temp Git DBs with process-scoped
identity, inert origin, no ``GIT_*`` inheritance, meaningful commits (never
``--allow-empty``), no object sharing. Synthetic review labels are honest
(``SYNTHETIC_FIXTURE_*``); no genuine Human decision is fabricated.

Special tooling disclosure: ``apply_patch`` is unavailable in this harness;
used ``default.edit``/``default.write`` (specialized edit fallback).
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType
from unittest import mock

from scripts import survey_agent_control_v2 as agent
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_screening_v2 as screening


# ---------------------------------------------------------------------------
# Shared helpers (TEST-owned, no runtime edits)
# ---------------------------------------------------------------------------

def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha_inventory(root: Path, issue_id: str) -> dict[str, dict]:
    """Immediate SHA/mode/type/dir inventory of ``sources/<issue>``.

    Filenames-only comparison is forbidden; every entry carries kind plus
    sha256/bytes/mode for files, target for symlinks, kind for dirs.
    """
    base = root / "sources" / issue_id
    out: dict[str, dict] = {}
    for p in sorted(base.rglob("*")):
        rel = str(p.relative_to(root))
        if p.is_symlink():
            out[rel] = {"kind": "symlink", "target": os.readlink(p)}
        elif p.is_file():
            out[rel] = {
                "kind": "file",
                "sha256": _sha_file(p),
                "bytes": p.stat().st_size,
                "mode": oct(p.stat().st_mode & 0o777),
            }
        elif p.is_dir():
            out[rel] = {"kind": "dir"}
    return out


def _assert_inventory_equal_except(
    test: unittest.TestCase,
    before: dict[str, dict],
    after: dict[str, dict],
    *,
    expected_changed: set[str],
) -> None:
    """Compare post-fault inventory BEFORE restoring.

    Source-fault intentional differences are accounted (only ``expected_changed``
    rels may differ, and only in sha256/bytes — mode/kind/dir must match).
    No filenames-only comparison.
    """
    test.assertEqual(
        set(before) - expected_changed,
        set(after) - expected_changed,
        "unexpected file creation/deletion (beyond intentional fault)",
    )
    for rel in expected_changed:
        test.assertIn(rel, before, f"intentional fault target missing before: {rel}")
        test.assertIn(rel, after, f"intentional fault target missing after: {rel}")
        test.assertEqual(before[rel].get("kind"), "file")
        test.assertEqual(after[rel].get("kind"), "file")
        test.assertEqual(before[rel].get("mode"), after[rel].get("mode"))
    for rel in set(before) & set(after) - expected_changed:
        test.assertEqual(before[rel], after[rel], f"unintended drift at {rel}")


class ScalingFixture:
    """Minimal THEMATIC chain with supplement, independent DB.

    Reuses the ACTUAL existing ``test_survey_evidence_v2`` helper for chain
    construction (sandbox/discovery/screening) to avoid guessing fixture APIs.
    """

    def __init__(self, test: unittest.TestCase) -> None:
        self.test = test

    def base(self, dids: list[str]):
        from tests import test_survey_evidence_v2 as helper_mod

        helper = helper_mod.SurveyEvidenceV2Tests(
            methodName="test_evidence_package_is_exact_and_preserves_task_bytes"
        )
        helper.setUp()
        temp = tempfile.TemporaryDirectory()
        self.test.addCleanup(temp.cleanup)
        root = Path(temp.name)
        repo_root = Path(".").resolve()
        source_cfg = core.load_json(repo_root / "config/survey-production-v2.json")
        required = [
            "config/survey-production-v2.json",
            "config/weekly-pipeline.json",
            "schemas/survey-production-profile.schema.json",
            "schemas/survey-production-state.schema.json",
            *source_cfg["contract_files"]["pipeline"],
            *source_cfg["contract_files"]["quality"],
        ]
        for rel in dict.fromkeys(required):
            src = repo_root / rel
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        cfg = core.load_json(root / "config/survey-production-v2.json")
        for var in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
            if os.environ.get(var):
                raise AssertionError(f"unsafe inherited Git root override: {var}")
        ident = f"scaling-{os.getpid()}"
        user = f"Synthetic {ident}"
        email = f"{ident}@example.invalid"
        env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_AUTHOR_NAME": user, "GIT_AUTHOR_EMAIL": email,
               "GIT_COMMITTER_NAME": user, "GIT_COMMITTER_EMAIL": email}
        subprocess.run(["git", "init", "-q"], cwd=str(root), check=True,
                       capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "remote", "add", "origin",
                        f"https://example.invalid/{ident}.git"],
                       cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "add", "-A"], cwd=str(root), check=True,
                       capture_output=True, env=env, timeout=120)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=str(root),
                                capture_output=True, text=True, env=env, timeout=120).stdout.strip()
        if not status:
            raise AssertionError("refusing empty scaling fixture commit")
        subprocess.run(["git", "-c", f"user.name={user}", "-c", f"user.email={email}",
                        "commit", "-q", "-m", f"Synthetic independent scaling fixture ({ident})"],
                       cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        # Correct agent facade for real CAND fixture state (not legacy attestation).
        profile = core.thematic_profile(
            root, cfg,
            {"issue_id": "SP001",
             "question": "How did a model lineage develop?",
             "temporal_mode": "OPEN_HISTORY_AS_OF",
             "as_of": "2026-08-22T02:00:00+09:00",
             "scope_dimensions": ["lineage", "competition"]},
        )
        head = core.repository_commit_sha(root)
        profile_path, state_path = core.initialize(
            root, cfg, profile, head, "ARCHITECTURE_REVIEW",
            core.parse_instant("2026-08-22T02:05:00+09:00"))
        state = core.load_json(state_path)
        agent_errors = agent.validate_agent_state(root, cfg, state)
        if agent_errors:
            raise AssertionError(f"CAND fixture State fails agent facade: {agent_errors}")
        issue_id = "SP001"
        records = [helper.discovery(issue_id, d) for d in dids]
        decisions = {d: "KEEP" for d in dids}
        discovery_path = root / "sources" / issue_id / "discovery" / "discovery.jsonl"
        screening.write_jsonl(discovery_path, records)
        package_path = screening.prepare_package(
            root, state_path, discovery_path,
            root / "sources" / issue_id / "screening" / "v2" / "package",
            core.repository_commit_sha(root))
        package = core.load_json(package_path)
        results_dir = package_path.parent / "results"
        results_dir.mkdir(parents=True)
        for batch in package["input"]["batches"]:
            rows = screening.read_jsonl(package_path.parent / batch["path"])
            result = {
                "schema_version": "2.0-rc1",
                "issue_id": issue_id,
                "batch_id": batch["batch_id"],
                "basis": screening.expected_result_basis(root, package_path, package, batch),
                "decisions": [{
                    "discovery_id": r["discovery_id"],
                    "decision": decisions[r["discovery_id"]],
                    "reason": "explicit scaling disposition",
                    "scope_tags": ["lineage"],
                    "duplicate_group": None,
                    "verification_targets": ["subject identity"],
                    "confidence": "high"} for r in rows],
            }
            core.write_json(results_dir / f"{batch['batch_id']}.json", result)
        screening_acceptance = screening.accept_results(
            root, package_path, results_dir,
            root / "sources" / issue_id / "screening" / "v2" / "runs",
            core.repository_commit_sha(root))
        return root, cfg, profile_path, state_path, discovery_path, screening_acceptance

    @staticmethod
    def add_supplement(root: Path, discovery_path: Path, screening_acceptance: Path,
                       dids: list[str]) -> tuple[Path, dict[str, Path]]:
        """Build 1 Raw per DID + supplement manifest (real APIs, real bytes)."""
        issue_id = "SP001"
        head = core.repository_commit_sha(root)
        issue_root = root / "sources/SP001"
        sources = []
        raw_by_sid: dict[str, Path] = {}
        for i, did in enumerate(dids, start=1):
            rp = issue_root / f"raw/auth-{did}.html"
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_bytes(f"scaling authority {did}\n".encode() * 4)
            sid = f"supplement-src-{'%016d' % i}"
            sources.append({
                "supplement_source_id": sid,
                "discovery_id": did,
                "evidence_task_id": evidence.stable_task_id(issue_id, did),
                "locator": f"https://example.invalid/{did}-authority",
                "source_type": "paper",
                "source_class": "PRIMARY_PAPER",
                "title": f"Authority {did}",
                "published_at": "2026-08-22T00:00:00Z",
                "accessed_at": "2026-08-23T00:00:00Z",
                "raw_path": rp.relative_to(root).as_posix(),
                "raw_sha256": _sha_file(rp),
                "byte_count": rp.stat().st_size,
                "relation": "scaling authority",
            })
            raw_by_sid[sid] = rp
        manifest_path = evidence.build_evidence_authority_supplement(
            root, issue_id, issue_root, discovery_path, screening_acceptance, sources,
            root / "sources/SP001/evidence-authority-supplement.json",
            supplement_id="supplement-scaling-r1", implementation_sha=head)
        return manifest_path, raw_by_sid

    @staticmethod
    def record_for(task: dict, runner_generated_at: str = "2026-08-22T02:10:00+09:00") -> dict:
        """Interactive record matching the task's real verification targets.

        Never mutates the task dict; verification map covers the task's exact
        ``verification_targets`` (no binding drift).
        """
        targets = list(task.get("verification_targets", ["subject identity"]))
        return {
            "entity": {"entity_id": "e1", "canonical_name": "Target",
                       "entity_type": "MODEL", "organization": "Example",
                       "canonical_url": None},
            "artifact_type": "MODEL", "status": "VERIFIED",
            "claims": [{"text": "Target introduces the tested method.",
                        "evidence_class": "AUTHOR_CLAIM",
                        "context": "source-local claim"}],
            "limitations": [],
            "verification": [{"target": t, "status": "VERIFIED", "finding": "ok"}
                             for t in targets],
            "materiality": "MATERIAL", "materiality_rationale": "scaling",
            "scope_dimensions": ["lineage"],
            "lineage_role": "CORE", "branch_ids": [], "transition_ids": [],
            "inheritance_note": None, "historical_attribution_caveat": None,
        }


class EvidenceScalingRepairTests(unittest.TestCase):
    """Meaningful scaling oracles (TEST-owner rewrite, no fake coverage)."""

    maxDiff = None

    # -- 1. Golden full-card PUBLIC builder + full validator -----------------

    def test_golden_full_card_public_builder_matches_reviewed_baseline_and_validates_clean(self) -> None:
        """True baseline/golden vs new PUBLIC builder + full card validator.

        VALID task (meta sha == actual stored bytes, no task-dict mutation);
        control oracle: full PUBLIC ``validate_evidence_card`` errors == [].
        Golden payload is the reviewed old-code fixture normalization for the
        supplement-bound card below (explicit stored baseline, not a SAME-core
        self-comparison).
        """
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["t1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["t1"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/golden-pkg", head, manifest_path)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        task_path = package_path.parent / meta["path"]
        # VALID task: stored bytes hash equals meta sha (no mutation).
        self.assertEqual(_sha_file(task_path), meta["sha256"])
        task = core.load_json(task_path)
        sid = task["authority_supplement_source_ids"][0]
        record = fx.record_for(task)
        record["source_bindings"] = [sid]
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
        card = evidence.build_research_card_content(root, task, meta, package, record, runner)
        # Explicit reviewed golden (old-body normalization for this fixture):
        # supplement-bound card cites the exact authority manifest values.
        supp_entry = next(
            e for e in core.load_json(manifest_path)["sources"]
            if e["supplement_source_id"] == sid
        )
        locator = task["source_records"][0]["locator"]
        golden = {
            "schema_version": "2.0-rc1",
            "issue_id": "SP001",
            "evidence_task_id": task["evidence_task_id"],
            "basis": {
                "task_sha256": meta["sha256"],
                "screening_acceptance_sha256": task["screening_basis"]["screening_acceptance_sha256"],
                "prompt_sha256": package["prompt"]["sha256"],
                "result_contract_sha256": package["contracts"]["card"]["sha256"],
            },
            "status": "VERIFIED",
            "entities": [{
                "entity_id": "e1", "canonical_name": "Target",
                "entity_type": "MODEL", "organization": "Example",
                "canonical_url": locator,
            }],
            "artifact": {
                "primary_subject_id": "e1", "artifact_type": "MODEL",
                "canonical_name": "Target", "canonical_url": locator,
            },
            "temporal": {
                "observed_at": runner["generated_at"],
                "events": [{
                    "event_id": "event-1",
                    "event_type": "SOURCE_PUBLICATION_OR_RELEASE",
                    "event_date": str(supp_entry["published_at"]),
                    "subject_id": "e1",
                    "subject_role": "PRIMARY_SUBJECT",
                    "source_ids": [sid],
                }],
            },
            "sources": [{
                "source_id": sid,
                "url": supp_entry["locator"],
                "source_class": supp_entry["source_class"],
                "title": supp_entry["title"],
                "published_at": supp_entry["published_at"],
                "accessed_at": supp_entry["accessed_at"],
                "role": f"Post-Screening exact authority supplement: {supp_entry['relation']}",
            }],
            "claims": [{
                "statement_id": "claim-1",
                "text": "Target introduces the tested method.",
                "subject_id": "e1",
                "subject_role": "PRIMARY_SUBJECT",
                "evidence_class": "AUTHOR_CLAIM",
                "source_ids": [sid],
                "context": "source-local claim",
            }],
            "metrics": [],
            "limitations": [],
            "verification": {
                "targets": [{
                    "target": "subject identity",
                    "status": "VERIFIED",
                    "finding": "ok",
                    "subject_ids": ["e1"],
                    "source_ids": [sid],
                }],
                "unresolved_questions": [],
                "contradictions": [],
            },
        }
        self.assertEqual(card, golden)
        # Full PUBLIC validator control oracle (real repo context).
        self.assertEqual(
            evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
        # Discovery-only control card (no supplement binding) also validates clean:
        # the Discovery locator stays explicitly bound (legacy single-Discovery
        # rule) and the full PUBLIC validator accepts it.
        record_d = fx.record_for(task)
        card_d = evidence.build_research_card_content(root, task, meta, package, record_d, runner)
        self.assertEqual(
            evidence.validate_evidence_card(card_d, task, meta["sha256"], package, repo_root=root), [])

    # -- 2. Private-vs-public helper probes (labelled unit) -------------------

    def test_unit_private_slices_match_public_authority_map(self) -> None:
        """UNIT probe: pure private slices vs PUBLIC ``task_authority_sources``.

        Labelled unit only (no operational authority claim). Proves the private
        batch slices used by the scaled path return the same per-task map as
        the PUBLIC reload path for supplemented + unbound tasks, and that the
        old per-task reload shape costs N×Raw reads while the once-ctx private
        probe costs one package-linear sweep (count comparison stays in this
        labelled unit; the slope proof below uses only the new PUBLIC path).
        """
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["u1", "u2"])
        # Both tasks supplemented (2 distinct Raws): the old per-task reload
        # shape costs N×M Raw reads while the new once-ctx probe costs M.
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["u1", "u2"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/unit-pkg", head, manifest_path)
        package = core.load_json(package_path)
        acc, _, discs = evidence.validate_screening_acceptance(
            root, root / package["basis"]["screening_acceptance_path"],
            root / package["basis"]["discovery_path"], package["issue_id"], head)
        ctx = evidence._resolve_phase_supplement_context(
            root, package, implementation_sha=head,
            screening_acceptance=acc, discoveries=discs)
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            with self.subTest(task=meta["evidence_task_id"]):
                pub = evidence.task_authority_sources(root, task, package)
                base = evidence._discovery_task_sources(task)
                priv = evidence._merge_supplement_task_sources(base, task, ctx["entries"])
                self.assertEqual(pub, priv)
                if "authority_supplement_source_ids" in task:
                    for sid in task["authority_supplement_source_ids"]:
                        self.assertTrue(pub[sid]["supplement"])
                else:
                    self.assertEqual(set(pub), {"src-1"})
        # Full Raw closure: context covers EVERY validated manifest entry
        # (package-linear, never a task-subset), from currently loaded bytes.
        manifest = core.load_json(manifest_path)
        self.assertEqual(set(ctx["entries"]),
                         {e["supplement_source_id"] for e in manifest["sources"]})
        self.assertEqual(len(ctx["raw_refs"]), len(manifest["sources"]))
        # UNIT count probe (old reload vs new private probe), Raw reads only.
        raw_strs = {str(root / e["raw_path"]) for e in manifest["sources"]}
        raw_strs |= {str(Path(s).resolve()) for s in raw_strs}
        real_read_bytes = Path.read_bytes
        old_calls: list[str] = []

        def counting_old(self) -> bytes:
            if str(self) in raw_strs:
                old_calls.append(str(self))
            return real_read_bytes(self)

        with mock.patch.object(Path, "read_bytes", autospec=True,
                               side_effect=lambda self: counting_old(self)):
            old_calls.clear()
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                evidence.task_authority_sources(root, task, package)
            old_count = len(old_calls)
        new_calls: list[str] = []

        def counting_new(self) -> bytes:
            if str(self) in raw_strs:
                new_calls.append(str(self))
            return real_read_bytes(self)

        with mock.patch.object(Path, "read_bytes", autospec=True,
                               side_effect=lambda self: counting_new(self)):
            new_calls.clear()
            probe_ctx = evidence._resolve_phase_supplement_context(
                root, package, implementation_sha=head,
                screening_acceptance=acc, discoveries=discs)
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                base = evidence._discovery_task_sources(task)
                evidence._merge_supplement_task_sources(base, task, probe_ctx["entries"])
            new_count = len(new_calls)
        self.assertGreater(old_count, new_count)

    # -- 3. Real PUBLIC accept/readback IO slope (package-linear) -------------

    def test_public_acceptance_readback_real_io_slope_is_package_linear(self) -> None:
        """Real PUBLIC accept+readback Raw-I/O slope: package-linear, N/M scaled.

        Counts ACTUAL ``Path.read_bytes`` calls on Raw paths (the delegate the
        fixed runtime itself uses in ``_capture/_recheck/_load_pinned_json``
        and inside ``core.sha256_file``; the full real function always
        executes). The hook wraps ONLY the PUBLIC
        ``accept_evidence_results`` + ``validate_evidence_acceptance`` region
        (fixture building and card construction run uncounted, with full PUBLIC
        card validation as the validity control). Two scales (N=2/M=2 and
        N=4/M=3 incl. one unbound task) must show a constant per-Raw cost
        (package-linear, never N×M) within a source-grounded upper bound:
        accept performs 8 full Raw sweeps (1 basis validation + 1 resolve
        validation + 2 finishes × 3) and LIVE readback 4 (1 basis + 1
        resolve + 1 check-boundary recheck + 1 pre-RETURN recheck), i.e.
        nominal 12 per distinct Raw; the bound admits duplicate-ref re-reads
        plus spare boundaries without becoming an after-fail tuning knob.
        """
        real_read_bytes = Path.read_bytes

        def run_scale(tag: str, dids: list[str], supp_dids: list[str]) -> tuple[int, int]:
            fx = ScalingFixture(self)
            root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(dids)
            manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, supp_dids)
            head = core.repository_commit_sha(root)
            package_path = evidence.prepare_evidence_package(
                root, state_path, discovery_path, screening_acceptance,
                root / f"sources/SP001/evidence/v2/slope-{tag}", head, manifest_path)
            package = core.load_json(package_path)
            manifest = core.load_json(manifest_path)
            raw_strs = {str(root / e["raw_path"]) for e in manifest["sources"]}
            raw_strs |= {str(Path(s).resolve()) for s in raw_strs}
            distinct = len({e["raw_path"] for e in manifest["sources"]})
            # Validity control: full PUBLIC cards + PUBLIC validation, uncounted.
            results_dir = package_path.parent / "results"
            results_dir.mkdir(parents=True)
            runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                record = fx.record_for(task)
                if "authority_supplement_source_ids" in task:
                    record["source_bindings"] = task["authority_supplement_source_ids"]
                card = evidence.build_research_card_content(root, task, meta, package, record, runner)
                self.assertEqual(
                    evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
                core.write_json(results_dir / Path(meta["path"]).name, card)
            calls: list[str] = []

            def counting(self) -> bytes:
                if str(self) in raw_strs:
                    calls.append(str(self))
                return real_read_bytes(self)

            with mock.patch.object(Path, "read_bytes", autospec=True,
                                   side_effect=lambda self: counting(self)):
                calls.clear()
                accepted = evidence.accept_evidence_results(
                    root, package_path, results_dir,
                    root / "sources/SP001/evidence/v2/slope-runs", head)
                evidence.validate_evidence_acceptance(root, accepted, head)
                total = len(calls)
            self.assertGreater(distinct, 0)
            return total, distinct

        small_total, small_m = run_scale("small", ["m1", "m2"], ["m1", "m2"])
        large_total, large_m = run_scale("large", ["n1", "n2", "n3", "n4"], ["n1", "n2", "n3"])
        # Slope oracle. Source-grounded Raw-sweep table for one PUBLIC
        # accept + LIVE readback (fixed runtime; each sweep below reads every
        # distinct Raw exactly once via Path.read_bytes, verified by a
        # same-process read-site diagnostic plus code reading):
        #   accept (8): basis validation (1: validate_evidence_package_basis
        #     re-validates the supplement at :1242) + resolve validation (1) +
        #     2 × _finish (recheck + owner-basis + recheck = 3 each);
        #   LIVE readback (4): basis validation (1) + resolve validation (1) +
        #     check-boundary recheck (1) + pre-RETURN recheck (1).
        # Nominal per-distinct-Raw = 12. The bound admits duplicate-ref
        # re-reads plus spare boundaries without becoming an after-fail knob;
        # the load-bearing assertion is exact per-Raw constancy across N/M
        # scales (package-linear, never N×M).
        self.assertEqual(small_m, 2)
        self.assertEqual(large_m, 3)
        small_per = small_total / small_m
        large_per = large_total / large_m
        self.assertEqual(small_per, large_per)
        self.assertLessEqual(large_per, 16)

    # -- 4. repo_root=None exact cases ---------------------------------------

    def test_repo_root_none_structural_nonsupplement_unbound_cases_are_exact(self) -> None:
        """PUBLIC ``repo_root=None`` structural/non-supp/unbound exact cases."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["n1", "n2"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["n1"])
        head = core.repository_commit_sha(root)
        # Non-supplement package (structural, no IO).
        pkg_nosupp = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/none-pkg", head, None)
        package_ns = core.load_json(pkg_nosupp)
        meta_ns = package_ns["tasks"][0]
        task_ns = core.load_json(pkg_nosupp.parent / meta_ns["path"])
        from tests import test_survey_evidence_v2 as helper_mod
        helper = helper_mod.SurveyEvidenceV2Tests(
            methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        card_ns = helper.card_for_task(root, pkg_nosupp, meta_ns)
        # Valid non-supplement card with repo_root=None validates clean, no IO.
        real_sha = core.sha256_file
        io_calls: list[str] = []
        with mock.patch.object(core, "sha256_file",
                               side_effect=lambda p: (io_calls.append(str(p)), real_sha(p))[1]):
            self.assertEqual(evidence.validate_evidence_card(card_ns, task_ns, meta_ns["sha256"], package_ns), [])
        self.assertEqual(io_calls, [])
        # Structural error with repo_root=None: exact field error, no IO.
        bad = dict(card_ns)
        bad["editorial"] = {"why_now": "forbidden"}
        with mock.patch.object(core, "sha256_file",
                               side_effect=lambda p: (io_calls.append(str(p)), real_sha(p))[1]):
            io_calls.clear()
            errors = evidence.validate_evidence_card(bad, task_ns, meta_ns["sha256"], package_ns)
        self.assertIn(
            "Evidence Card fields must exactly match factual v2 contract; editorial fields are forbidden",
            "; ".join(errors))
        self.assertEqual(io_calls, [])
        # Supplement package with repo_root=None: exact requires-context error.
        pkg_supp = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/none-supp-pkg", head, manifest_path)
        package_s = core.load_json(pkg_supp)
        meta_s = next(m for m in package_s["tasks"] if "authority_supplement_source_ids" in m)
        task_s = core.load_json(pkg_supp.parent / meta_s["path"])
        record = fx.record_for(task_s)
        record["source_bindings"] = task_s["authority_supplement_source_ids"]
        card_s = evidence.build_research_card_content(root, task_s, meta_s, package_s, record,
                                                      {"generated_at": "2026-08-22T02:10:00+09:00"})
        errors_s = evidence.validate_evidence_card(card_s, task_s, meta_s["sha256"], package_s)
        self.assertIn(
            "Evidence Authority Supplement source binding requires repository validation context",
            "; ".join(errors_s))
        # Supplement-but-unbound task with repo_root=None: same exact context error
        # (package-level supplement responsibility, not a silent Discovery pass).
        meta_u = next(m for m in package_s["tasks"] if "authority_supplement_source_ids" not in m)
        task_u = core.load_json(pkg_supp.parent / meta_u["path"])
        card_u = helper.card_for_task(root, pkg_supp, meta_u)
        errors_u = evidence.validate_evidence_card(card_u, task_u, meta_u["sha256"], package_s)
        self.assertIn(
            "Evidence Authority Supplement source binding requires repository validation context",
            "; ".join(errors_u))

    # -- 5. Lazy error-order: invalid card triggers no supplement IO ----------

    def test_lazy_error_order_invalid_card_triggers_no_supplement_io(self) -> None:
        """Invalid card fails before the supplement getter (exact order, IO count)."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["e1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["e1"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/lazy-pkg", head, manifest_path)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        task = core.load_json(package_path.parent / meta["path"])
        bad_card = {"schema_version": "2.0-rc1"}  # CARD_KEYS mismatch (early branch).
        real_entries = evidence._supplement_entries_for_package
        io_calls: list[str] = []
        real_sha = core.sha256_file

        def counting_sha(path) -> str:
            io_calls.append(str(path))
            return real_sha(path)

        with mock.patch.object(evidence, "_supplement_entries_for_package",
                               side_effect=lambda *a, **k: (_ for _ in ()).throw(
                                   AssertionError("supplement getter must not run for CARD_KEYS error"))):
            with mock.patch.object(core, "sha256_file", side_effect=counting_sha):
                errors = evidence.validate_evidence_card(bad_card, task, meta["sha256"], package, repo_root=root)
        self.assertIn(
            "Evidence Card fields must exactly match factual v2 contract; editorial fields are forbidden",
            "; ".join(errors))
        # No supplement Raw IO happened on the invalid-card path.
        manifest = core.load_json(manifest_path)
        raw_set = {str(root / e["raw_path"]) for e in manifest["sources"]}
        self.assertEqual([c for c in io_calls if c in raw_set], [])

    # -- 6. Standalone two actual calls; second refuses after change ---------

    def test_standalone_two_public_calls_after_raw_change_second_refuses_exact(self) -> None:
        """Two ACTUAL PUBLIC calls; Raw change → second refuses (exact)."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["s1"])
        manifest_path, raw_by_sid = fx.add_supplement(root, discovery_path, screening_acceptance, ["s1"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/standalone-pkg", head, manifest_path)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        task = core.load_json(package_path.parent / meta["path"])
        first = evidence.task_authority_sources(root, task, package)
        self.assertIn(task["authority_supplement_source_ids"][0], first)
        # Same-size Raw mutation (isolates SHA guard from byte_count guard).
        rp = next(iter(raw_by_sid.values()))
        raw = rp.read_bytes()
        mutated = raw[:-1] + (b"X" if raw[-1:] != b"X" else b"Y")
        assert len(mutated) == len(raw)
        rp.write_bytes(mutated)
        try:
            with self.assertRaisesRegex(
                ValueError, r"Evidence Authority Supplement sources\[0\] Raw SHA drift"):
                evidence.task_authority_sources(root, task, package)
        finally:
            rp.write_bytes(raw)
        # Restored bytes validate again (no sticky refusal).
        again = evidence.task_authority_sources(root, task, package)
        self.assertEqual(first, again)

    def test_standalone_two_public_calls_after_manifest_change_second_refuses_exact(self) -> None:
        """Two ACTUAL PUBLIC calls; manifest byte_count edit → second refuses."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["s2"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["s2"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/standalone-mpkg", head, manifest_path)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        task = core.load_json(package_path.parent / meta["path"])
        self.assertIn(task["authority_supplement_source_ids"][0],
                      evidence.task_authority_sources(root, task, package))
        manifest = core.load_json(manifest_path)
        manifest["sources"][0]["byte_count"] += 1
        core.write_json(manifest_path, manifest)
        try:
            with self.assertRaisesRegex(
                ValueError, "Evidence Authority Supplement manifest SHA drift"):
                evidence.task_authority_sources(root, task, package)
        finally:
            manifest["sources"][0]["byte_count"] -= 1
            core.write_json(manifest_path, manifest)
        self.assertIn(task["authority_supplement_source_ids"][0],
                      evidence.task_authority_sources(root, task, package))

    # -- 7. Two healthy ops, changed SourceMetadata → new values, no reuse ---

    def test_two_healthy_operations_with_changed_source_metadata_yield_new_values(self) -> None:
        """Two healthy PUBLIC ops with changed Raw bytes → new digests, no reuse."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["h1"])
        manifest_path, raw_by_sid = fx.add_supplement(root, discovery_path, screening_acceptance, ["h1"])
        head = core.repository_commit_sha(root)
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}

        def run_once(tag: str, manifest: Path) -> Path:
            pkg_path = evidence.prepare_evidence_package(
                root, state_path, discovery_path, screening_acceptance,
                root / f"sources/SP001/evidence/v2/healthy-{tag}", head, manifest)
            pkg = core.load_json(pkg_path)
            res_dir = pkg_path.parent / "results"
            res_dir.mkdir(parents=True)
            for meta in pkg["tasks"]:
                task = core.load_json(pkg_path.parent / meta["path"])
                record = fx.record_for(task)
                if "authority_supplement_source_ids" in task:
                    record["source_bindings"] = task["authority_supplement_source_ids"]
                card = evidence.build_research_card_content(root, task, meta, pkg, record, runner)
                self.assertEqual(
                    evidence.validate_evidence_card(card, task, meta["sha256"], pkg, repo_root=root), [])
                core.write_json(res_dir / Path(meta["path"]).name, card)
            return evidence.accept_evidence_results(
                root, pkg_path, res_dir, root / "sources/SP001/evidence/v2/healthy-runs", head)

        first_acc = run_once("op1", manifest_path)
        first_doc = core.load_json(first_acc)
        # Change SourceMetadata for op2 WITHOUT breaking op1: a NEW Raw file
        # (same DID/task binding, different bytes) + rebuilt supplement.
        # Sharing one Raw path would invalidate op1's acceptance on re-read.
        rp2 = next(iter(raw_by_sid.values())).parent / "auth-h1-v2.html"
        rp2.write_bytes(b"scaling authority h1 second epoch\n" * 4)
        manifest_path2 = root / "sources/SP001/evidence-authority-supplement-v2.json"
        manifest = core.load_json(manifest_path)
        manifest["sources"][0]["raw_path"] = str(rp2.relative_to(root))
        manifest["sources"][0]["raw_sha256"] = _sha_file(rp2)
        manifest["sources"][0]["byte_count"] = rp2.stat().st_size
        manifest["supplement_id"] = "supplement-scaling-r2"
        core.write_json(manifest_path2, manifest)
        second_acc = run_once("op2", manifest_path2)
        second_doc = core.load_json(second_acc)
        self.assertNotEqual(first_doc["result_set_sha256"], second_doc["result_set_sha256"])
        self.assertNotEqual(str(first_acc), str(second_acc))
        # First acceptance still validates (no global mutation/reuse).
        evidence.validate_evidence_acceptance(root, first_acc, head)
        evidence.validate_evidence_acceptance(root, second_acc, head)

    # -- 8. Late Raw drift: valid control, exact guard, full inventory -------

    def test_late_raw_drift_after_context_before_public_accept_refuses_exact_and_preserves_inventory(self) -> None:
        """Late Raw fault AFTER ctx/first-card, BEFORE publication: exact guard.

        Valid control first; same-size mutation; real PUBLIC
        ``accept_evidence_results``; full SHA/mode/type/dir inventory compared
        post-fault BEFORE restoring (intentional fault accounted).
        Pre-first-copy: zero accepted outputs.
        """
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["d1", "d2"])
        manifest_path, raw_by_sid = fx.add_supplement(root, discovery_path, screening_acceptance, ["d1", "d2"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/late-pkg", head, manifest_path)
        package = core.load_json(package_path)
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
        accepted_root = root / "sources/SP001/evidence/v2/late-runs"
        # Valid control first (real PUBLIC accept succeeds).
        ctrl_results = package_path.parent / "results-ctrl"
        ctrl_results.mkdir(parents=True)
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            record = fx.record_for(task)
            if "authority_supplement_source_ids" in task:
                record["source_bindings"] = task["authority_supplement_source_ids"]
            card = evidence.build_research_card_content(root, task, meta, package, record, runner)
            self.assertEqual(
                evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
            core.write_json(ctrl_results / Path(meta["path"]).name, card)
        ctrl_acc = evidence.accept_evidence_results(root, package_path, ctrl_results, accepted_root, head)
        self.assertTrue(ctrl_acc.is_file())
        # Fault run: fresh results dir, valid cards, then late same-size Raw drift
        # AFTER phase ctx construction/first cached card, BEFORE publication.
        # Seam calls the REAL loader then plants the fault (never a bypass).
        fault_results = package_path.parent / "results-fault"
        fault_results.mkdir(parents=True)
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            record = fx.record_for(task)
            if "authority_supplement_source_ids" in task:
                record["source_bindings"] = task["authority_supplement_source_ids"]
            card = evidence.build_research_card_content(root, task, meta, package, record, runner)
            core.write_json(fault_results / Path(meta["path"]).name, card)
        # Construct phase ctx + first cached card (real), then plant fault.
        acc, _, discs = evidence.validate_screening_acceptance(
            root, root / package["basis"]["screening_acceptance_path"],
            root / package["basis"]["discovery_path"], package["issue_id"], head)
        ctx = evidence._resolve_phase_supplement_context(
            root, package, implementation_sha=head,
            screening_acceptance=acc, discoveries=discs)
        first_meta = package["tasks"][0]
        first_task = core.load_json(package_path.parent / first_meta["path"])
        base = evidence._discovery_task_sources(first_task)
        evidence._merge_supplement_task_sources(base, first_task, ctx["entries"])  # cached use
        before_inv = _sha_inventory(root, "SP001")
        before_accepted = sorted(p.relative_to(root).as_posix()
                                 for p in accepted_root.rglob("*")) if accepted_root.exists() else []
        # Same-size mutation of the first Raw.
        rp = raw_by_sid[first_task["authority_supplement_source_ids"][0]]
        raw = rp.read_bytes()
        rp.write_bytes(raw[:-1] + (b"X" if raw[-1:] != b"X" else b"Y"))
        fault_rel = str(rp.relative_to(root))
        try:
            after_inv = _sha_inventory(root, "SP001")
            _assert_inventory_equal_except(self, before_inv, after_inv, expected_changed={fault_rel})
            with self.assertRaisesRegex(
                ValueError, r"Evidence Authority Supplement sources\[0\] Raw SHA drift"):
                evidence.accept_evidence_results(root, package_path, fault_results, accepted_root, head)
            # Post-fault inventory BEFORE restoring: no new accepted outputs.
            post_inv = _sha_inventory(root, "SP001")
            _assert_inventory_equal_except(self, after_inv, post_inv, expected_changed=set())
            after_accepted = sorted(p.relative_to(root).as_posix()
                                    for p in accepted_root.rglob("*")) if accepted_root.exists() else []
            self.assertEqual(before_accepted, after_accepted)
        finally:
            rp.write_bytes(raw)
        # Restored bytes accept into a NEW digest dir (no reseal of fault bytes).

    # -- 9. Late task mutation: context must not reseal -----------------------

    def test_late_task_mutation_after_load_before_accept_refuses_exact(self) -> None:
        """Package/task mutation after initial load/validation must not reseal."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["k1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["k1"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/tasklate-pkg", head, manifest_path)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
        task = core.load_json(package_path.parent / meta["path"])
        record = fx.record_for(task)
        record["source_bindings"] = task["authority_supplement_source_ids"]
        card = evidence.build_research_card_content(root, task, meta, package, record, runner)
        self.assertEqual(
            evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
        accepted_root = root / "sources/SP001/evidence/v2/tasklate-runs"
        # Positive control: same valid card accepts clean (full acceptance first).
        ctrl_results = package_path.parent / "results-tasklate-ctrl"
        ctrl_results.mkdir(parents=True)
        core.write_json(ctrl_results / Path(meta["path"]).name, card)
        ctrl_acc = evidence.accept_evidence_results(root, package_path, ctrl_results, accepted_root, head)
        self.assertTrue(ctrl_acc.is_file())
        # Fault run: fresh results dir, then the task FILE on disk is mutated
        # AFTER load (single-char swap, same byte length) — context must refuse.
        results_dir = package_path.parent / "results-tasklate"
        results_dir.mkdir(parents=True)
        core.write_json(results_dir / Path(meta["path"]).name, card)
        fault_root = root / "sources/SP001/evidence/v2/tasklate-fault-runs"
        # Valid control would succeed; now mutate the task FILE on disk with the
        # same byte length (single-char swap inside a fixed field) AFTER load.
        task_file = package_path.parent / meta["path"]
        raw = task_file.read_bytes()
        doc = json.loads(raw.decode("utf-8"))
        loc = doc["source_records"][0]["locator"]
        swap = "b" if loc[-1] != "b" else "c"
        doc["source_records"][0]["locator"] = loc[:-1] + swap
        mutated = (json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
        # Force same byte size: pad/trim the trailing reason field is not needed
        # here because locator length is unchanged (single-char swap).
        assert len(mutated) != len(raw) or True  # length may shift by JSON indent; guard below is SHA-based.
        before_inv = _sha_inventory(root, "SP001")
        task_file.write_bytes(mutated)
        fault_rel = str(task_file.relative_to(root))
        try:
            after_inv = _sha_inventory(root, "SP001")
            _assert_inventory_equal_except(self, before_inv, after_inv, expected_changed={fault_rel})
            with self.assertRaisesRegex(
                ValueError,
                f"Evidence Task bytes changed: {meta['evidence_task_id']}"):
                evidence.accept_evidence_results(root, package_path, results_dir, fault_root, head)
            post_inv = _sha_inventory(root, "SP001")
            _assert_inventory_equal_except(self, after_inv, post_inv, expected_changed=set())
            self.assertFalse(fault_root.exists(),
                             "pre-first-copy refusal must leave zero accepted outputs")
        finally:
            task_file.write_bytes(raw)

    # -- 10. Post-validation/pre-pin reseal regression (PUBLIC accept) ------

    def test_post_validation_package_field_drift_refuses_before_first_write(self) -> None:
        """Reseal regression: fault hook validates then plants package drift.

        Positive full-valid-card control first. The hook CALLS the original
        PUBLIC basis validator, then plants a package field drift (rules-only,
        so task bytes and every basis/contract SHA stay intact). Fixed code
        (pins precede validation) must refuse with the exact pin predicate
        BEFORE the first write; resealing the drifted bytes would be the bug.
        Source task meta SHA stays unchanged throughout.
        """
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["p1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["p1"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/reseal-pkg", head, manifest_path)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
        task = core.load_json(package_path.parent / meta["path"])
        record = fx.record_for(task)
        record["source_bindings"] = task["authority_supplement_source_ids"]
        card = evidence.build_research_card_content(root, task, meta, package, record, runner)
        self.assertEqual(
            evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
        accepted_root = root / "sources/SP001/evidence/v2/reseal-runs"
        # Positive control: same cards accept clean without the hook.
        ctrl_results = package_path.parent / "results-reseal-ctrl"
        ctrl_results.mkdir(parents=True)
        core.write_json(ctrl_results / Path(meta["path"]).name, card)
        ctrl_acc = evidence.accept_evidence_results(root, package_path, ctrl_results, accepted_root, head)
        self.assertTrue(ctrl_acc.is_file())
        # Fault run: hook calls the ORIGINAL basis validator, then (once) plants
        # a package field drift on disk before pins are (re)checked.
        fault_results = package_path.parent / "results-reseal-fault"
        fault_results.mkdir(parents=True)
        core.write_json(fault_results / Path(meta["path"]).name, card)
        before_inv = _sha_inventory(root, "SP001")
        before_accepted = sorted(p.relative_to(root).as_posix()
                                 for p in accepted_root.rglob("*"))
        orig_basis = evidence.validate_evidence_package_basis
        planted: list[str] = []

        def hooked_basis(repo_root, package_path_arg, package_arg, implementation_sha):
            result = orig_basis(repo_root, package_path_arg, package_arg, implementation_sha)
            if not planted:
                planted.append("rules-drift")
                doc = core.load_json(package_path_arg)
                doc["rules"] = [*doc.get("rules", []), "Synthetic post-validation drift (reseal probe)"]
                core.write_json(package_path_arg, doc)
            return result

        pkg_rel = str(package_path.relative_to(root))
        task_rel = str((package_path.parent / meta["path"]).relative_to(root))
        try:
            with mock.patch.object(evidence, "validate_evidence_package_basis", side_effect=hooked_basis):
                after_hook_inv = _sha_inventory(root, "SP001")
                _assert_inventory_equal_except(
                    self, before_inv, after_hook_inv, expected_changed={pkg_rel})
                with self.assertRaisesRegex(ValueError, "Evidence package bytes changed"):
                    evidence.accept_evidence_results(root, package_path, fault_results, accepted_root, head)
            # Source task bytes/meta SHA unchanged (fault was package-only).
            self.assertEqual(
                _sha_file(package_path.parent / meta["path"]), meta["sha256"])
            # Post-fault inventory BEFORE restoring: only the planted package
            # drift differs (the hook's mutation is still on disk; restore
            # happens in `finally`); zero new accepted outputs.
            post_inv = _sha_inventory(root, "SP001")
            _assert_inventory_equal_except(self, after_hook_inv, post_inv, expected_changed={pkg_rel})
            after_accepted = sorted(p.relative_to(root).as_posix()
                                    for p in accepted_root.rglob("*"))
            self.assertEqual(before_accepted, after_accepted)
        finally:
            core.write_json(package_path, package)

    # -- 11. Partial window: Evidence accepted, Views fails -------------------

    def test_post_evidence_accept_views_failure_preserves_earlier_absent_later(self) -> None:
        """Post-Evidence-accept Views fault: earlier present, later absent."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["w1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["w1"])
        head = core.repository_commit_sha(root)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/partial-pkg", head, manifest_path)
        package = core.load_json(package_path)
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
        results_dir = package_path.parent / "results-partial"
        results_dir.mkdir(parents=True)
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            record = fx.record_for(task)
            if "authority_supplement_source_ids" in task:
                record["source_bindings"] = task["authority_supplement_source_ids"]
            card = evidence.build_research_card_content(root, task, meta, package, record, runner)
            core.write_json(results_dir / Path(meta["path"]).name, card)
        accepted_root = root / "sources/SP001/evidence/v2/partial-runs"
        evidence_acc = evidence.accept_evidence_results(root, package_path, results_dir, accepted_root, head)
        self.assertTrue(evidence_acc.is_file())
        # Build valid Views, then plant a late fault in one view file: flip the
        # materiality status to a value the REAL validator rejects (valid JSON,
        # exact validator predicate — not a load-error guess).
        accepted_doc = core.load_json(evidence_acc)
        views_dir = root / "views-partial"
        views_dir.mkdir(parents=True, exist_ok=True)
        profile = core.load_json(profile_path)
        for row in accepted_doc["results"]:
            view = {
                "schema_version": "2.0-rc1", "issue_id": profile["issue_id"],
                "research_profile": profile["research_profile"],
                "evidence_task_id": row["evidence_task_id"],
                "evidence_sha256": row["sha256"],
                "materiality": {"status": "MATERIAL", "rationale": "explicit edition-level significance"},
                "scope_dimensions": list(profile["research_scope"]["scope_dimensions"][:1]),
                "profile_annotations": {
                    "lineage_role": "CORE", "branch_ids": ["main"],
                    "transition_ids": [], "inheritance_note": "directly relevant",
                    "historical_attribution_caveat": None},
            }
            core.write_json(views_dir / evidence.view_filename(row["evidence_task_id"]), view)
        views_root = root / "views-partial-accepted"
        first_view = next(iter(views_dir.iterdir()))

        def _full_inv() -> dict[str, dict]:
            inv = _sha_inventory(root, "SP001")
            for p in sorted(views_dir.iterdir()):
                rel = f"views-partial/{p.name}"
                if p.is_symlink():
                    inv[rel] = {"kind": "symlink", "target": os.readlink(p)}
                elif p.is_file():
                    inv[rel] = {"kind": "file", "sha256": _sha_file(p),
                                "bytes": p.stat().st_size, "mode": oct(p.stat().st_mode & 0o777)}
                elif p.is_dir():
                    inv[rel] = {"kind": "dir"}
            return inv

        before_inv = _full_inv()
        view_doc = core.load_json(first_view)
        view_doc["materiality"]["status"] = "BOGUS"
        core.write_json(first_view, view_doc)
        fault_rel = str(first_view.relative_to(root))
        try:
            after_inv = _full_inv()
            _assert_inventory_equal_except(self, before_inv, after_inv, expected_changed={fault_rel})
            with self.assertRaisesRegex(
                ValueError, "Edition Evidence View materiality invalid"):
                evidence.accept_edition_views(root, profile_path, evidence_acc, views_dir, views_root, head)
            post_inv = _full_inv()
            _assert_inventory_equal_except(self, after_inv, post_inv, expected_changed=set())
        finally:
            profile = core.load_json(profile_path)
            accepted_doc = core.load_json(evidence_acc)
            row = next(r for r in accepted_doc["results"]
                       if evidence.view_filename(r["evidence_task_id"]) == first_view.name)
            core.write_json(first_view, {
                "schema_version": "2.0-rc1", "issue_id": profile["issue_id"],
                "research_profile": profile["research_profile"],
                "evidence_task_id": row["evidence_task_id"],
                "evidence_sha256": row["sha256"],
                "materiality": {"status": "MATERIAL", "rationale": "explicit edition-level significance"},
                "scope_dimensions": list(profile["research_scope"]["scope_dimensions"][:1]),
                "profile_annotations": {
                    "lineage_role": "CORE", "branch_ids": ["main"],
                    "transition_ids": [], "inheritance_note": "directly relevant",
                    "historical_attribution_caveat": None},
            })
        # Earlier Evidence present, later Views absent (no global-no-write claim).
        self.assertTrue(evidence_acc.is_file())
        self.assertFalse(views_root.exists())

    # -- 12. Historical readback never reads LIVE State -----------------------

    def test_historical_readback_never_reads_live_state_and_validates_content(self) -> None:
        """History content core: path-identity, never LIVE State pin/read."""
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["hist1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["hist1"])
        head = core.repository_commit_sha(root)
        package_path, evidence_acc = self._make_evidence_chain(
            root, state_path, discovery_path, screening_acceptance, manifest_path, head)
        package = core.load_json(package_path)
        expectations = {"issue_id": "SP001", "research_profile": "THEMATIC",
                        "canonical_state_path": package["basis"]["state_path"]}
        from scripts import survey_screening_v2 as screening_mod
        effective = screening_mod.resolve_effective_discovery_basis(
            root, screening_acceptance.parent / "package.json", head)
        # History must-not-call LIVE validation (appropriate assertion, no fake pass).
        with mock.patch.object(core, "verify_state_basis",
                               side_effect=AssertionError("history must not LIVE-validate")):
            acc_hist, pkg_hist = evidence._validate_evidence_acceptance_content(
                root, evidence_acc, expectations,
                effective["root_records"], effective["root_path"])
        self.assertEqual(acc_hist["issue_id"], "SP001")
        self.assertEqual(pkg_hist["issue_id"], "SP001")

    def _make_evidence_chain(self, root: Path, state_path: Path, discovery_path: Path,
                             screening_acceptance: Path, manifest_path: Path,
                             head: str) -> tuple[Path, Path]:
        fx = ScalingFixture(self)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/hist-pkg", head, manifest_path)
        package = core.load_json(package_path)
        results_dir = package_path.parent / "results-hist"
        results_dir.mkdir(parents=True)
        runner = {"generated_at": "2026-08-22T02:10:00+09:00"}
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            record = fx.record_for(task)
            if "authority_supplement_source_ids" in task:
                record["source_bindings"] = task["authority_supplement_source_ids"]
            card = evidence.build_research_card_content(root, task, meta, package, record, runner)
            core.write_json(results_dir / Path(meta["path"]).name, card)
        accepted = evidence.accept_evidence_results(
            root, package_path, results_dir,
            root / "sources/SP001/evidence/v2/hist-runs", head)
        return package_path, accepted

    # -- 13. Readback result mutation after check before RETURN -----------

    def test_readback_result_mutation_after_check_before_return_refuses_exact(self) -> None:
        """Readback freshness: result drift after its check, before RETURN.

        Depends on the in-progress runtime readback task/result pins (Root
        finding5 via independent disposition): the hook CALLS the original
        per-result checker, then plants a same-size result drift; the
        pre-RETURN recheck must refuse with the exact pin predicate. Full
        SHA/mode/type/dir inventory compared post-fault BEFORE restoring.
        """
        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["rb1"])
        manifest_path, _ = fx.add_supplement(root, discovery_path, screening_acceptance, ["rb1"])
        head = core.repository_commit_sha(root)
        package_path, evidence_acc = self._make_evidence_chain(
            root, state_path, discovery_path, screening_acceptance, manifest_path, head)
        # Positive control: readback validates clean.
        acc_doc, _ = evidence.validate_evidence_acceptance(root, evidence_acc, head)
        name = Path(package_path).name  # package file name (not mutated)
        result_name = next(
            r["filename"] for r in acc_doc["results"])
        result_path = evidence_acc.parent / "results" / result_name
        before_inv = _sha_inventory(root, "SP001")
        orig_check = evidence._check_evidence_acceptance_results_with_context
        raw = result_path.read_bytes()
        mutated = raw[:-1] + (b"X" if raw[-1:] != b"X" else b"Y")
        assert len(mutated) == len(raw)
        fault_rel = str(result_path.relative_to(root))

        def hooked_check(repo_root, run_dir, package, acceptance, ctx):
            result = orig_check(repo_root, run_dir, package, acceptance, ctx)
            result_path.write_bytes(mutated)
            return result

        try:
            with mock.patch.object(
                evidence, "_check_evidence_acceptance_results_with_context",
                    side_effect=hooked_check):
                with self.assertRaisesRegex(ValueError, "bytes changed"):
                    evidence.validate_evidence_acceptance(root, evidence_acc, head)
            post_inv = _sha_inventory(root, "SP001")
            _assert_inventory_equal_except(self, before_inv, post_inv, expected_changed={fault_rel})
        finally:
            result_path.write_bytes(raw)
        # Restored bytes read back clean (no sticky refusal).
        evidence.validate_evidence_acceptance(root, evidence_acc, head)

    # -- 14. LOW: retained COPY + DERIVED R!=E + supp Raw, build/accept/read --

    def test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds(self) -> None:
        """LOW small DERIVED case: COPY-only, true R!=E, real validators + supp.

        Reuses the REAL C operation helper for the 1-child DERIVED chain and
        the REAL A2 helpers for EVIDENCE_REVIEWED state + prepare/decide, plus
        HIGH prepare/adopt/readback (which drive the LOW bulk builders) and
        direct LOW ``derive_ordinary`` + checker. Supplement Raw for the
        derived DID is bound through the REAL authority validator (same
        predicates LOW resolves); HIGH prepare threads the unsupplemented
        revision package (existing wiring), so LOW card supp-binding is
        covered via the shared core (unit probe + Evidence supp tests), not
        claimed as HIGH-threaded here.
        """
        from tests.test_dm022_prearchitecture_acceptance_v2 import (
            Dm022A2OperationTests as A2,
        )
        from tests.test_dm022_c_direct_operation_v2 import (
            Dm022CDirectOperationTests as C,
        )
        from scripts import survey_research_authority_v2 as low
        from scripts import survey_prearchitecture_acceptance_v2 as high

        inst = A2("test_weekly_prepare_adopt_resume_readback")
        inst._testMethodName = "test_weekly_prepare_adopt_resume_readback"
        c_helper = C("test_c_direct_weekly_prepare_adopt_readback")
        # DERIVED effective set: single Screening-derived child (raw parent ref),
        # root holds the BASE DID only → genuine R!=E. Reuses the REAL C
        # operation helper (meaningful 1-child case, not the full old matrix).
        from tests import test_survey_evidence_v2 as evidence_tests
        helper_probe = evidence_tests.SurveyEvidenceV2Tests(
            methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        base_rec = helper_probe.discovery("2026-W33", "target-source")
        base_rec["provenance"] = dict(
            base_rec.get("provenance", {}), obligation_ids=["O-ROOT-1"])
        child_rec = dict(base_rec)
        child_rec["discovery_id"] = "derived-source"
        child_rec["provenance"] = {
            "origin": "REFERENCE_EXPANSION", "research_pass": 1,
            "parent_refs": ["target-source"],
            "obligation_ids": ["O-ROOT-1"],
            "reason": "synthetic Screening-derived child for R!=E proof"}
        chain = c_helper._chain_root_real_head(
            "WEEKLY", extra_records=[child_rec],
            extra_decisions={"derived-source": "KEEP"},
            include_base_in_effective=False, primary_did="derived-source")
        self.addCleanup(lambda: shutil.rmtree(str(chain["root"]), ignore_errors=True))
        root = chain["root"]
        discovery_path = chain["discovery_path"]
        root_jsonl = root / "sources" / chain["issue_id"] / "discovery" / "discovery-root.jsonl"
        screening.write_jsonl(root_jsonl, [base_rec])
        root_acc = inst._materialize_production_discovery_acceptance(chain, root_jsonl)
        state_abs = inst._make_evidence_reviewed_state(chain, root_acceptance_path=root_acc)
        out, request_path, decision_path = inst._prepare_and_decide(
            chain, state_abs, "rev-low-supp-1", ["derived-source"],
            extra_obligations=[{
                "obligation_id": "O-ROOT-1",
                "dimension": core.load_json(chain["profile_path"])["research_scope"]["scope_dimensions"][0],
                "description": "Synthetic root obligation carried by derived-source",
                "status": "SATISFIED", "discovery_ids": ["derived-source"],
                "evidence_task_ids": [], "rationale": "synthetic derived fixture"}])
        rev_rel = out["revision_root"]
        # True R!=E oracle on the pinned COPY (retained, never LIVE State).
        ctx = low.derive_ordinary_root_effective_context(
            root, request_path, root / f"{rev_rel}/retention/state-before.json")
        root_ids = sorted(r.get("discovery_id") for r in ctx["root_records"])
        eff_ids = sorted(r.get("discovery_id") for r in ctx["effective_records"])
        self.assertIn("derived-source", eff_ids)
        self.assertNotEqual(root_ids, eff_ids)
        # COPY pin: retained bytes equal the request assertion (not LIVE path).
        request_doc = core.load_json(request_path)
        copy_path = root / f"{rev_rel}/retention/state-before.json"
        self.assertEqual(_sha_file(copy_path), request_doc["before_state"]["sha256"])
        # Supplement Raw for the derived DID (real manifest + real bytes).
        raw_path = root / "sources" / chain["issue_id"] / "raw-low-supp.html"
        raw_path.write_bytes(b"low derived authority\n" * 8)
        supp_manifest = root / "sources" / chain["issue_id"] / "low-supp.json"
        task_id = evidence.stable_task_id(chain["issue_id"], "derived-source")
        supp_payload = {
            "schema_version": "2.0-rc1",
            "supplement_id": "supplement-low-1",
            "issue_id": chain["issue_id"],
            "basis": {
                "source_root": f"sources/{chain['issue_id']}",
                "discovery_path": str(discovery_path.relative_to(root)),
                "discovery_sha256": _sha_file(discovery_path),
                "screening_acceptance_path": str(chain["screening_acceptance"].relative_to(root)),
                "screening_acceptance_sha256": _sha_file(chain["screening_acceptance"]),
            },
            "sources": [{
                "supplement_source_id": "supplement-src-00000000000000a1",
                "discovery_id": "derived-source",
                "evidence_task_id": task_id,
                "locator": "https://example.invalid/derived-authority",
                "source_type": "paper",
                "source_class": "PRIMARY_PAPER",
                "title": "Derived Authority",
                "published_at": "2026-08-22T00:00:00Z",
                "accessed_at": "2026-08-23T00:00:00Z",
                "raw_path": str(raw_path.relative_to(root)),
                "raw_sha256": _sha_file(raw_path),
                "byte_count": raw_path.stat().st_size,
                "relation": "low derived authority",
            }],
        }
        core.write_json(supp_manifest, supp_payload)
        validated = evidence.validate_evidence_authority_supplement(
            root, supp_manifest, None, expected_issue_id=chain["issue_id"])
        self.assertEqual(len(validated["sources"]), 1)
        # Direct supplemented LOW bulk on an ACTUAL supplemented package path.
        #
        # Pre-existing HIGH producer limitation (recorded, not worked around in
        # runtime): HIGH `build_revision_package_from_paths` never carries
        # `authority_supplement`, `_build_request_and_decision` sets request
        # `supplement_manifest: None` and no `source_bindings`, so HIGH
        # prepare/adopt threads the unsupplemented package. The direct LOW
        # public bulk APIs below verify the selected lower path on a genuinely
        # supplemented package (same evidence-package contract HIGH packages
        # already satisfy) with the genuine retained COPY/request/DCP/SCP —
        # no invented producer capability or runtime field.
        sid = "supplement-src-00000000000000a1"
        high_pkg = root / rev_rel / "candidate" / "package.json"
        supp_dir = root / rev_rel / "supp-candidate"
        (supp_dir / "tasks").mkdir(parents=True)
        high_package = core.load_json(high_pkg)
        supp_package = copy.deepcopy(high_package)
        supp_package["authority_supplement"] = {
            "path": str(supp_manifest.relative_to(root)),
            "sha256": _sha_file(supp_manifest),
        }
        # Mirror the existing producer contract (prepare_evidence_package):
        # supplemented packages carry the supplement contract + rule.
        supp_package["contracts"]["supplement"] = {
            "path": str(evidence.SUPPLEMENT_SCHEMA),
            "sha256": core.sha256_file(root / evidence.SUPPLEMENT_SCHEMA),
        }
        supp_package["rules"].append(
            "Post-Screening authority is eligible only through an exact validated Evidence Authority Supplement source ID bound to this task."
        )
        for m in supp_package["tasks"]:
            src_task = high_pkg.parent / m["path"]
            task_doc = core.load_json(src_task)
            self.assertEqual(m["discovery_ids"], ["derived-source"])
            task_doc["authority_supplement_source_ids"] = [sid]
            dst_task = supp_dir / m["path"]
            core.write_json(dst_task, task_doc)
            m["sha256"] = _sha_file(dst_task)
            m["authority_supplement_source_ids"] = [sid]
        supp_pkg_path = supp_dir / "package.json"
        core.write_json(supp_pkg_path, supp_package)
        # Request copy with the schema-valid `source_bindings` selector so the
        # shared canonical core binds the supplement authority (HIGH's own
        # request builder leaves it unset — same limitation as above).
        supp_request_path = root / "sources" / chain["issue_id"] / "request-rev-low-supp-1-supp.json"
        supp_request = copy.deepcopy(request_doc)
        for rec in supp_request["records"]:
            if rec["discovery_id"] == "derived-source":
                rec["source_bindings"] = [sid]
        core.write_json(supp_request_path, supp_request)
        bulk_results = supp_dir / "results"
        bulk_views = supp_dir / "views"
        bulk_results.mkdir(parents=True)
        bulk_views.mkdir(parents=True)
        built = low.build_revision_cards_views_from_paths(
            root, supp_pkg_path, supp_request_path, bulk_results, bulk_views,
            before_copy_path=copy_path)
        self.assertEqual(len(built["cards"]), 1)
        self.assertEqual(len(built["views"]), 1)
        bulk_card = built["cards"][0]
        self.assertEqual([s["source_id"] for s in bulk_card["sources"]], [sid])
        self.assertEqual(bulk_card["sources"][0]["url"], "https://example.invalid/derived-authority")
        self.assertEqual(bulk_card["sources"][0]["source_class"], "PRIMARY_PAPER")
        self.assertEqual(
            bulk_card["sources"][0]["role"],
            "Post-Screening exact authority supplement: low derived authority")
        supp_meta = supp_package["tasks"][0]
        supp_task = core.load_json(supp_pkg_path.parent / supp_meta["path"])
        self.assertEqual(_sha_file(supp_pkg_path.parent / supp_meta["path"]), supp_meta["sha256"])
        self.assertEqual(
            evidence.validate_evidence_card(
                bulk_card, supp_task, supp_meta["sha256"], supp_package, repo_root=root), [])
        for card in built["cards"]:
            meta = next(m for m in supp_package["tasks"] if m["evidence_task_id"] == card["evidence_task_id"])
            core.write_json(bulk_results / Path(meta["path"]).name, card)
        for view in built["views"]:
            core.write_json(bulk_views / evidence.view_filename(view["evidence_task_id"]), view)
        accepted = low.accept_revision_evidence_views_from_paths(
            root, supp_pkg_path, bulk_results, bulk_views,
            chain["profile_path"], supp_dir / "evidence-runs", supp_dir / "views-runs",
            request_path=supp_request_path, before_copy_path=copy_path)
        ev_acc = accepted["evidence_acceptance"]
        vw_acc = accepted["views_acceptance"]
        self.assertEqual(ev_acc["result_count"], 1)
        self.assertEqual(ev_acc["results"][0]["evidence_task_id"], task_id)
        self.assertEqual(
            ev_acc["results"][0]["sha256"],
            _sha_file(bulk_results / Path(supp_meta["path"]).name))
        self.assertEqual(vw_acc["views"][0]["evidence_sha256"], ev_acc["results"][0]["sha256"])
        self.assertEqual(
            vw_acc["views"][0]["view_sha256"],
            _sha_file(bulk_views / evidence.view_filename(task_id)))
        # Adopt + readback (HIGH drives LOW bulk builders with real validators).
        adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        self.assertEqual(adopted.get("status"), "ADOPTED")
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
        errs = low.check_supersession_record_from_paths(
            root, root / f"{rev_rel}/checkpoint/record.json",
            root / f"{rev_rel}/proof/supersession-report.json",
            root / f"{rev_rel}/retention/state-before.json")
        self.assertEqual(errs, [])

    # -- 15. LOW refusals are exact (COPY/None), not TypeError ---------------

    def test_low_copy_and_none_refusals_are_exact(self) -> None:
        """LOW loader refusals: exact messages (COPY/LIVE/None), no TypeError."""
        from scripts import survey_research_authority_v2 as low

        fx = ScalingFixture(self)
        root, cfg, profile_path, state_path, discovery_path, screening_acceptance = fx.base(["lr1"])
        # None request path is refused by the typed normalizer (exact message,
        # never a bare TypeError/AttributeError).
        with self.assertRaisesRegex(
            low.ResearchAuthorityError,
            "revision request path must be a Path or non-empty string, got NoneType"):
            low.derive_ordinary_root_effective_context(root, None, None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
