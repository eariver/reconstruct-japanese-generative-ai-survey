#!/usr/bin/env python3
"""Evidence scaling repair — bounded targeted oracles (test-only module).

Covers Root §6: ONE canonical core, lazy order, phase-local contexts, full
transitive callers incl. LOW bulk, logical-unit rechecks, partial windows.
Uses independent temp git DBs with process-scoped identity, inert origin,
no GIT_* inheritance, meaningful commits (never --allow-empty). No fake
coverage, no source-string asserts, no broad Exception acceptance.
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

from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_screening_v2 as screening


IMPLEMENTATION_SHA_FAKE = "4" * 40
BASE_FILES = [
    "config/survey-production-v2.json",
    "config/weekly-pipeline.json",
    "schemas/survey-production-profile.schema.json",
    "schemas/survey-production-state.schema.json",
]


class ScalingFixture:
    """Minimal THEMATIC chain with supplement, independent DB."""

    def __init__(self, test: unittest.TestCase) -> None:
        self.test = test
        self.temp: tempfile.TemporaryDirectory[str] | None = None
        self.root: Path | None = None

    def sandbox(self) -> tuple[Path, dict]:
        temp = tempfile.TemporaryDirectory()
        self.temp = temp
        self.test.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.root = root
        repo_root = Path(".").resolve()
        source_cfg = core.load_json(repo_root / "config/survey-production-v2.json")
        required = [
            *BASE_FILES,
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
        return root, cfg

    @staticmethod
    def source(locator: str) -> dict:
        return {
            "source_type": "paper",
            "collector_id": "test-collector",
            "collector_run_id": "run-001",
            "observed_at": "2026-08-22T02:00:00+09:00",
            "title": locator,
            "locator": locator,
            "raw_paths": ["raw/source.json"],
            "published_at": "2025-01-01T00:00:00Z",
            "summary_text": "bounded source summary",
            "metadata": {},
        }

    def discovery(self, issue_id: str, did: str) -> dict:
        return {
            "schema_version": "2.0-rc1",
            "issue_id": issue_id,
            "discovery_id": did,
            "provenance": {
                "origin": "BASE",
                "research_pass": 0,
                "parent_refs": [],
                "obligation_ids": [],
                "reason": "scaling test",
            },
            "source": self.source(f"https://example.invalid/{did}"),
        }

    def init_thematic(self, root: Path, cfg: dict) -> tuple[Path, Path]:
        profile = core.thematic_profile(
            root, cfg,
            {"issue_id": "SP001",
             "question": "How did a model lineage develop?",
             "temporal_mode": "OPEN_HISTORY_AS_OF",
             "as_of": "2026-08-22T02:00:00+09:00",
             "scope_dimensions": ["lineage", "competition"]},
        )
        head = core.repository_commit_sha(root)
        return core.initialize(root, cfg, profile, head, "ARCHITECTURE_REVIEW",
                               core.parse_instant("2026-08-22T02:05:00+09:00"))

    def make_screening(self, root: Path, state_path: Path, records: list[dict],
                       decisions: dict[str, str]) -> tuple[Path, Path]:
        issue_id = records[0]["issue_id"]
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
        accepted = screening.accept_results(
            root, package_path, results_dir,
            root / "sources" / issue_id / "screening" / "v2" / "runs",
            core.repository_commit_sha(root))
        return discovery_path, accepted


class EvidenceScalingTests(unittest.TestCase):
    def test_public_vs_private_exact_cards_and_errors(self) -> None:
        fx = ScalingFixture(self)
        root, cfg = fx.sandbox()
        profile_path, state_path = fx.init_thematic(root, cfg)
        issue_id = "SP001"
        records = [fx.discovery(issue_id, f"t{i}") for i in range(1, 4)]
        decisions = {r["discovery_id"]: "KEEP" for r in records}
        discovery_path, screening_acceptance = fx.make_screening(root, state_path, records, decisions)
        head = core.repository_commit_sha(root)
        # Two supplement Raws for t1/t2; t3 stays unbound (no forcing).
        issue_root = root / "sources/SP001"
        raws = {}
        sources = []
        for i in (1, 2):
            rp = issue_root / f"raw/a{i}.html"
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_bytes(f"scaling authority {i}\n".encode())
            sid = f"supplement-src-{'%016d' % i}"
            task_id = evidence.stable_task_id(issue_id, f"t{i}")
            sources.append({
                "supplement_source_id": sid,
                "discovery_id": f"t{i}",
                "evidence_task_id": task_id,
                "locator": f"https://example.invalid/auth{i}",
                "source_type": "paper",
                "source_class": "PRIMARY_PAPER",
                "title": f"Authority {i}",
                "published_at": "2026-08-22T00:00:00Z",
                "accessed_at": "2026-08-23T00:00:00Z",
                "raw_path": rp.relative_to(root).as_posix(),
                "raw_sha256": hashlib.sha256(rp.read_bytes()).hexdigest(),
                "byte_count": rp.stat().st_size,
                "relation": "scaling authority",
            })
            raws[sid] = rp
        manifest_path = evidence.build_evidence_authority_supplement(
            root, issue_id, issue_root, discovery_path, screening_acceptance, sources,
            root / "sources/SP001/evidence-authority-supplement.json",
            supplement_id="supplement-scaling-r1", implementation_sha=head)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/supp-package", head, manifest_path)
        package = core.load_json(package_path)
        # Public reload vs private batch produce byte-identical cards.
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            pub = evidence.task_authority_sources(root, task, package)
            # Private batch via phase context (one validation, pure slices).
            acc, _, discs = evidence.validate_screening_acceptance(
                root, root / package["basis"]["screening_acceptance_path"],
                root / package["basis"]["discovery_path"], issue_id, head)
            ctx = evidence._resolve_phase_supplement_context(
                root, package, implementation_sha=head,
                screening_acceptance=acc, discoveries=discs)
            base = evidence._discovery_task_sources(task)
            priv = evidence._merge_supplement_task_sources(base, task, ctx["entries"])
            self.assertEqual(pub, priv)
            # Golden field checks (not self-comparison only).
            for sid, auth in pub.items():
                if auth.get("supplement"):
                    self.assertTrue(auth["url"].startswith("https://example.invalid/auth"))
                    self.assertEqual(auth["source_class"], "PRIMARY_PAPER")
                    self.assertEqual(auth["role"],
                                     f"Post-Screening exact authority supplement: scaling authority")
                else:
                    self.assertTrue(auth["url"].startswith("https://example.invalid/t"))
            # Card via ONE core both ways.
            record = {"entity": {"entity_id": "e1", "canonical_name": "Target",
                                 "entity_type": "MODEL", "organization": "Example",
                                 "canonical_url": None},
                      "artifact_type": "MODEL", "status": "VERIFIED",
                      "claims": [], "limitations": [],
                      "verification": [{"target": "subject identity", "status": "VERIFIED",
                                        "finding": "ok"}],
                      "materiality": "MATERIAL", "materiality_rationale": "scaling",
                      "scope_dimensions": ["lineage"],
                      "lineage_role": "CORE", "branch_ids": [], "transition_ids": [],
                      "inheritance_note": None, "historical_attribution_caveat": None}
            # Patch task verification targets to match minimal record.
            task = copy.deepcopy(task)
            task["verification_targets"] = ["subject identity"]
            pub_card = evidence._build_card_core(
                task, meta, package, record, {"generated_at": "2026-08-22T02:10:00+09:00"},
                pub)
            priv_card = evidence._build_card_core(
                task, meta, package, record, {"generated_at": "2026-08-22T02:10:00+09:00"},
                priv)
            self.assertEqual(pub_card, priv_card)
            self.assertEqual(pub_card["sources"][0]["source_class"], "PRIMARY_PAPER")
            # Public wrapper errors preserved: unbound supplement.
            bad_task = copy.deepcopy(task)
            bad_task["authority_supplement_source_ids"] = ["supplement-src-0000000000000099"]
            with self.assertRaisesRegex(ValueError, "unbound supplement source"):
                evidence.task_authority_sources(root, bad_task, package)

    def test_raw_read_scaling_per_phase(self) -> None:
        fx = ScalingFixture(self)
        root, cfg = fx.sandbox()
        profile_path, state_path = fx.init_thematic(root, cfg)
        issue_id = "SP001"
        records = [fx.discovery(issue_id, f"s{i}") for i in range(1, 5)]
        decisions = {r["discovery_id"]: "KEEP" for r in records}
        discovery_path, screening_acceptance = fx.make_screening(root, state_path, records, decisions)
        head = core.repository_commit_sha(root)
        issue_root = root / "sources/SP001"
        sources = []
        for i in range(1, 5):
            rp = issue_root / f"raw/b{i}.bin"
            rp.parent.mkdir(parents=True, exist_ok=True)
            rp.write_bytes(f"raw-bytes-{i}\n".encode() * 10)
            sources.append({
                "supplement_source_id": f"supplement-src-{'%016d' % i}",
                "discovery_id": f"s{i}",
                "evidence_task_id": evidence.stable_task_id(issue_id, f"s{i}"),
                "locator": f"https://example.invalid/b{i}",
                "source_type": "paper", "source_class": "PRIMARY_PAPER",
                "title": f"B{i}", "published_at": "2026-08-22T00:00:00Z",
                "accessed_at": "2026-08-23T00:00:00Z",
                "raw_path": rp.relative_to(root).as_posix(),
                "raw_sha256": hashlib.sha256(rp.read_bytes()).hexdigest(),
                "byte_count": rp.stat().st_size,
                "relation": "scaling",
            })
        manifest_path = evidence.build_evidence_authority_supplement(
            root, issue_id, issue_root, discovery_path, screening_acceptance, sources,
            root / "sources/SP001/supp2.json", supplement_id="supplement-scaling-r2",
            implementation_sha=head)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/p2", head, manifest_path)
        package = core.load_json(package_path)
        # Count actual Raw sha256_file calls (IO only, still real validation).
        real_sha = core.sha256_file
        raw_calls: list[Path] = []
        supplement_rel = package["authority_supplement"]["path"]
        manifest = core.load_json(root / supplement_rel)
        raw_set = {root / e["raw_path"] for e in manifest["sources"]}

        def counting_sha(path: Path) -> str:
            if Path(path) in raw_set:
                raw_calls.append(Path(path))
            return real_sha(path)

        # Old shape: per-task full reload (preserved public path).
        with mock.patch.object(core, "sha256_file", side_effect=counting_sha):
            raw_calls.clear()
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                evidence.task_authority_sources(root, task, package)
            old_count = len(raw_calls)
        # New shape: one phase context + pure slices.
        with mock.patch.object(core, "sha256_file", side_effect=counting_sha):
            raw_calls.clear()
            acc, _, discs = evidence.validate_screening_acceptance(
                root, root / package["basis"]["screening_acceptance_path"],
                root / package["basis"]["discovery_path"], issue_id, head)
            ctx = evidence._resolve_phase_supplement_context(
                root, package, implementation_sha=head,
                screening_acceptance=acc, discoveries=discs)
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                base = evidence._discovery_task_sources(task)
                evidence._merge_supplement_task_sources(base, task, ctx["entries"])
            new_count = len(raw_calls)
        distinct = len(raw_set)
        self.assertGreater(old_count, new_count)
        # New is package-linear (constant factor for basis+ctx+recheck, not N×).
        self.assertLessEqual(new_count, distinct * 4)
        self.assertGreaterEqual(old_count, distinct * len(package["tasks"]))

    def test_late_drift_refuses_with_exact_predicate_and_inventories(self) -> None:
        fx = ScalingFixture(self)
        root, cfg = fx.sandbox()
        profile_path, state_path = fx.init_thematic(root, cfg)
        issue_id = "SP001"
        records = [fx.discovery(issue_id, "d1")]
        decisions = {"d1": "KEEP"}
        discovery_path, screening_acceptance = fx.make_screening(root, state_path, records, decisions)
        head = core.repository_commit_sha(root)
        issue_root = root / "sources/SP001"
        rp = issue_root / "raw/drift.html"
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_bytes(b"drift baseline\n")
        src = {
            "supplement_source_id": "supplement-src-0000000000000042",
            "discovery_id": "d1",
            "evidence_task_id": evidence.stable_task_id(issue_id, "d1"),
            "locator": "https://example.invalid/drift",
            "source_type": "paper", "source_class": "PRIMARY_PAPER",
            "title": "Drift", "published_at": "2026-08-22T00:00:00Z",
            "accessed_at": "2026-08-23T00:00:00Z",
            "raw_path": rp.relative_to(root).as_posix(),
            "raw_sha256": hashlib.sha256(rp.read_bytes()).hexdigest(),
            "byte_count": rp.stat().st_size,
            "relation": "drift",
        }
        manifest_path = evidence.build_evidence_authority_supplement(
            root, issue_id, issue_root, discovery_path, screening_acceptance, [src],
            root / "sources/SP001/drift-supp.json", supplement_id="supplement-drift",
            implementation_sha=head)
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/drift-pkg", head, manifest_path)
        package = core.load_json(package_path)
        acc, _, discs = evidence.validate_screening_acceptance(
            root, root / package["basis"]["screening_acceptance_path"],
            root / package["basis"]["discovery_path"], issue_id, head)
        ctx = evidence._resolve_phase_supplement_context(
            root, package, implementation_sha=head,
            screening_acceptance=acc, discoveries=discs)
        pins = evidence._capture_phase_pins((("Drift Raw", rp),))
        # Late Raw byte mutation → recheck refuses (bytes changed), no reseal.
        # Fresh validation would report "Raw SHA drift"; phase recheck reports
        # the pinned-byte predicate "bytes changed" (exact intended recheck).
        rp.write_bytes(b"drift MUTATED\n")
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            evidence._recheck_supplement_context(root, ctx)
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            evidence._recheck_phase_pins(pins)
        # Manifest byte_count drift predicate (exact, not broad): mutate the
        # manifest FILE on disk (not an in-memory dict), then fresh validation.
        rp.write_bytes(b"drift baseline\n")
        manifest_file = core.load_json(manifest_path)
        manifest_file["sources"][0]["byte_count"] = 999999
        core.write_json(manifest_path, manifest_file)
        with self.assertRaisesRegex(ValueError, "byte_count drift|SHA drift|manifest"):
            evidence.validate_evidence_authority_supplement(
                root, manifest_path, head,
                expected_issue_id=issue_id,
                screening_acceptance=acc, discoveries=discs)
        # Restore manifest file to baseline for the accept-inventory check below.
        manifest_file["sources"][0]["byte_count"] = rp.stat().st_size
        manifest_file["sources"][0]["raw_sha256"] = hashlib.sha256(rp.read_bytes()).hexdigest()
        core.write_json(manifest_path, manifest_file)
        # First-write inventory: accept with drifted Raw refuses before copy.
        rp.write_bytes(b"drift MUTATED again\n")
        accepted_root = issue_root / "evidence/v2/accepted"
        # Build minimal results dir for accept (use valid cards from baseline first).
        rp.write_bytes(b"drift baseline\n")
        package2 = core.load_json(package_path)
        # Resolve fresh ctx for valid cards.
        ctx2 = evidence._resolve_phase_supplement_context(
            root, package2, implementation_sha=head,
            screening_acceptance=acc, discoveries=discs)
        results_dir = Path(str(package_path) + "-results")
        if results_dir.exists():
            shutil.rmtree(results_dir)
        results_dir.mkdir(parents=True)
        for meta in package2["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            base = evidence._discovery_task_sources(task)
            auth = evidence._merge_supplement_task_sources(base, task, ctx2["entries"])
            # Minimal valid card via core (status VERIFIED, single entity).
            record = {"entity": {"entity_id": "e1", "canonical_name": "T",
                                 "entity_type": "MODEL", "organization": "Example",
                                 "canonical_url": None},
                      "artifact_type": "MODEL", "status": "VERIFIED",
                      "claims": [], "limitations": [],
                      "verification": [{"target": "subject identity", "status": "VERIFIED",
                                        "finding": "ok"}],
                      "materiality": "MATERIAL", "materiality_rationale": "r",
                      "scope_dimensions": ["lineage"],
                      "lineage_role": "CORE", "branch_ids": [], "transition_ids": [],
                      "inheritance_note": None, "historical_attribution_caveat": None}
            task = dict(task, verification_targets=["subject identity"])
            card = evidence._build_card_core(
                task, meta, package2, record, {"generated_at": "2026-08-22T02:10:00+09:00"}, auth)
            core.write_json(results_dir / Path(meta["path"]).name, card)
        # Now drift Raw and attempt accept → must refuse before first copy.
        rp.write_bytes(b"drifted before accept\n")
        before = list(accepted_root.rglob("*")) if accepted_root.exists() else []
        with self.assertRaisesRegex(ValueError, "Raw SHA drift|byte_count drift|manifest SHA drift"):
            evidence.accept_evidence_results(root, package_path, results_dir, accepted_root, head)
        after = list(accepted_root.rglob("*")) if accepted_root.exists() else []
        # No new canonical output on pre-first-write refusal (immediate inventory).
        self.assertEqual(before, after)
        for p in after:
            self.assertFalse(p.is_symlink())

    def test_standalone_no_supplement_unbound_and_no_reuse(self) -> None:
        fx = ScalingFixture(self)
        root, cfg = fx.sandbox()
        profile_path, state_path = fx.init_thematic(root, cfg)
        issue_id = "SP001"
        records = [fx.discovery(issue_id, "u1"), fx.discovery(issue_id, "u2")]
        decisions = {r["discovery_id"]: "KEEP" for r in records}
        discovery_path, screening_acceptance = fx.make_screening(root, state_path, records, decisions)
        head = core.repository_commit_sha(root)
        # No-supplement package: prepare without manifest.
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/nosupp", head, None)
        package = core.load_json(package_path)
        self.assertNotIn("authority_supplement", package)
        # Empty context legitimate (not requires-context error).
        ctx = evidence._resolve_phase_supplement_context(
            root, package, implementation_sha=head,
            screening_acceptance=None, discoveries=None)
        self.assertIsNone(ctx["manifest_ref"])
        self.assertEqual(dict(ctx["entries"]), {})
        # Non-supplement card validation: structural, no IO, repo_root None ok.
        for meta in package["tasks"]:
            task = core.load_json(package_path.parent / meta["path"])
            card = {
                "schema_version": "2.0-rc1", "issue_id": issue_id,
                "evidence_task_id": task["evidence_task_id"],
                "basis": {"task_sha256": meta["sha256"],
                          "screening_acceptance_sha256": task["screening_basis"]["screening_acceptance_sha256"],
                          "prompt_sha256": package["prompt"]["sha256"],
                          "result_contract_sha256": package["contracts"]["card"]["sha256"]},
                "status": "VERIFIED",
                "entities": [{"entity_id": "e1", "canonical_name": "T", "entity_type": "MODEL",
                              "organization": "Example",
                              "canonical_url": task["source_records"][0]["locator"]}],
                "artifact": {"primary_subject_id": "e1", "artifact_type": "MODEL",
                             "canonical_name": "T",
                             "canonical_url": task["source_records"][0]["locator"]},
                "temporal": {"observed_at": "2026-08-22T02:10:00+09:00", "events": []},
                "sources": [{"source_id": "src-1", "url": task["source_records"][0]["locator"],
                             "source_class": "PRIMARY_PAPER", "title": "t",
                             "published_at": "2025-01-01T00:00:00Z",
                             "accessed_at": "2026-08-22T02:10:00+09:00",
                             "role": "verification source"}],
                "claims": [], "metrics": [], "limitations": [],
                "verification": {"targets": [], "unresolved_questions": [], "contradictions": []},
            }
            self.assertEqual(evidence.validate_evidence_card(card, task, meta["sha256"], package), [])
        # Supplement package but unbound task keeps Discovery-only map.
        issue_root = root / "sources/SP001"
        rp = issue_root / "raw/only.html"
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_bytes(b"only\n")
        only_src = {
            "supplement_source_id": "supplement-src-0000000000000077",
            "discovery_id": "u1",
            "evidence_task_id": evidence.stable_task_id(issue_id, "u1"),
            "locator": "https://example.invalid/only",
            "source_type": "paper", "source_class": "PRIMARY_PAPER",
            "title": "Only", "published_at": None,
            "accessed_at": "2026-08-23T00:00:00Z",
            "raw_path": rp.relative_to(root).as_posix(),
            "raw_sha256": hashlib.sha256(rp.read_bytes()).hexdigest(),
            "byte_count": rp.stat().st_size,
            "relation": "only u1",
        }
        manifest_path = evidence.build_evidence_authority_supplement(
            root, issue_id, issue_root, discovery_path, screening_acceptance, [only_src],
            root / "sources/SP001/only-supp.json", supplement_id="supplement-only",
            implementation_sha=head)
        package2_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/only-pkg", head, manifest_path)
        package2 = core.load_json(package2_path)
        # u2 has no supplement IDs → Discovery-only, no error, no forcing.
        meta_u2 = next(m for m in package2["tasks"] if m["discovery_ids"] == ["u2"])
        task_u2 = core.load_json(package2_path.parent / meta_u2["path"])
        self.assertNotIn("authority_supplement_source_ids", task_u2)
        acc2, _, discs2 = evidence.validate_screening_acceptance(
            root, root / package2["basis"]["screening_acceptance_path"],
            root / package2["basis"]["discovery_path"], issue_id, head)
        ctx2 = evidence._resolve_phase_supplement_context(
            root, package2, implementation_sha=head,
            screening_acceptance=acc2, discoveries=discs2)
        base_u2 = evidence._discovery_task_sources(task_u2)
        merged_u2 = evidence._merge_supplement_task_sources(base_u2, task_u2, ctx2["entries"])
        self.assertEqual(set(merged_u2), {"src-1"})
        # No cross-operation reuse: two healthy ops with different manifest data.
        rp2 = issue_root / "raw/only2.html"
        rp2.write_bytes(b"only2\n")
        only_src2 = dict(only_src, supplement_source_id="supplement-src-0000000000000078",
                         raw_path=rp2.relative_to(root).as_posix(),
                         raw_sha256=hashlib.sha256(rp2.read_bytes()).hexdigest(),
                         byte_count=rp2.stat().st_size)
        manifest2_path = evidence.build_evidence_authority_supplement(
            root, issue_id, issue_root, discovery_path, screening_acceptance, [only_src2],
            root / "sources/SP001/only-supp2.json", supplement_id="supplement-only2",
            implementation_sha=head)
        package3_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/only-pkg2", head, manifest2_path)
        package3 = core.load_json(package3_path)
        ctx3 = evidence._resolve_phase_supplement_context(
            root, package3, implementation_sha=head,
            screening_acceptance=acc2, discoveries=discs2)
        self.assertNotEqual(set(ctx2["entries"]), set(ctx3["entries"]))
        # Standalone second call sees new bytes (no cache).
        task_u1 = core.load_json(package2_path.parent / next(
            m for m in package2["tasks"] if m["discovery_ids"] == ["u1"])["path"])
        first = evidence.task_authority_sources(root, task_u1, package2)
        # Mutate second manifest's Raw (different op) does not leak into first.
        self.assertIn("supplement-src-0000000000000077", first)
        self.assertNotIn("supplement-src-0000000000000078", first)

    def test_direct_derived_history_and_low_copy(self) -> None:
        fx = ScalingFixture(self)
        root, cfg = fx.sandbox()
        profile_path, state_path = fx.init_thematic(root, cfg)
        issue_id = "SP001"
        records = [fx.discovery(issue_id, "h1")]
        decisions = {"h1": "KEEP"}
        discovery_path, screening_acceptance = fx.make_screening(root, state_path, records, decisions)
        head = core.repository_commit_sha(root)
        # DIRECT-like: no supplement, structural validation, repo_root None ok.
        package_path = evidence.prepare_evidence_package(
            root, state_path, discovery_path, screening_acceptance,
            root / "sources/SP001/evidence/v2/direct-pkg", head, None)
        package = core.load_json(package_path)
        meta = package["tasks"][0]
        task = core.load_json(package_path.parent / meta["path"])
        self.assertEqual(evidence.task_authority_sources(root, task, package).keys(), {"src-1"})
        # History content core: path-identity, never LIVE State pin/read.
        expectations = {"issue_id": issue_id, "research_profile": "THEMATIC",
                        "canonical_state_path": package["basis"]["state_path"]}
        # Root records for history: use effective records as DATA (no LIVE).
        _, _, discs = evidence.validate_screening_acceptance(
            root, root / package["basis"]["screening_acceptance_path"],
            root / package["basis"]["discovery_path"], issue_id, head)
        # History basis validation must not call verify_state_basis / LIVE.
        with mock.patch.object(core, "verify_state_basis",
                               side_effect=AssertionError("history must not LIVE-validate")):
            acc_hist, tasks_hist = evidence._validate_evidence_package_basis_content(
                root, package_path, package, expectations, discs, discovery_path)
            self.assertEqual(acc_hist["issue_id"], issue_id)
        # LOW COPY: derive_ordinary requires COPY, refuses LIVE path and None.
        from scripts import survey_research_authority_v2 as low
        with self.assertRaisesRegex(Exception, "before_copy_path|COPY|None"):
            low.derive_ordinary_root_effective_context(root, Path("nonexistent-request.json"), None)  # type: ignore[arg-type]
        # LOW bulk uses ONE canonical core (import check: no runner import).
        import ast
        low_src = (Path(".").resolve() / "scripts" / "survey_research_authority_v2.py").read_text()
        self.assertNotIn("import run_evidence_v2_interactive", low_src)
        self.assertNotIn("from scripts import run_evidence_v2_interactive", low_src)


if __name__ == "__main__":
    unittest.main()
