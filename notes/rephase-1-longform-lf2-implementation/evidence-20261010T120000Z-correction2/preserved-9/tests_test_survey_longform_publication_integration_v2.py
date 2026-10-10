"""LF-2I focused integration: initial LONGFORM_GENERATED_V1 route.

All research/editorial/visual/Human records here are synthetic TYPE/IDENTITY
fixtures built through the real current producers and stage validators; they
never assert genuine semantic sufficiency, a TeX/PDF build transfer, or real
editorial/visual acceptance. Fixture Git databases are independent temp dirs
with process-scoped synthetic identity (no persistent user.* config); the
candidate source and reconstruct databases are never written. The candidate
under test stays an uncommitted exact-hash overlay.
"""
from __future__ import annotations

import copy
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from pypdf import PdfReader, PdfWriter

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_longform_derivation_v2 as derivation
from scripts import survey_longform_generated_v2 as generated
from scripts import survey_longform_semantic_publication_v2 as longform_publication
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_fidelity_v2 as fidelity
from scripts import survey_reader_publication_v2 as reader_publication
from scripts import survey_reader_surface_gate_v2 as reader_gate
from scripts import survey_stage_validation_v2 as stage_validation
from scripts import survey_release_checkpoint_v2 as release_checkpoint
from scripts.render_article_draft_tex import tex_escape
from tests import test_survey_longform_derivation_v2 as lf1_tests


ISSUE = "SP001"
DID1 = "fixture-paper-D001"
URL1 = "https://example.invalid/papers/lineage-note-one"
URL_BY_DID = {DID1: URL1}

# New overlay paths absent from `git ls-files` (tracked M paths are copied via
# ls-files with working-tree bytes; these must be pinned and included too).
OVERLAY_NEW = (
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "schemas/longform-publication-source-manifest-v2.schema.json",
)
OVERLAY_LF1 = (
    "scripts/survey_longform_derivation_v2.py",
    "schemas/longform-reader-input-v2.schema.json",
)

_GIT_VARS = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)


def _snapshot(root: Path) -> dict:
    files: dict[str, str] = {}
    dirs: list[str] = []
    symlinks: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        rel = str(path.relative_to(root))
        if path.is_symlink():
            try:
                symlinks[rel] = os.readlink(path)
            except OSError:
                symlinks[rel] = "<unreadable-symlink>"
        elif path.is_dir():
            dirs.append(rel)
        elif path.is_file():
            files[rel] = core.sha256_file(path)
    git: dict[str, str] = {}
    for args, key in (
        (["git", "rev-parse", "HEAD"], "head"),
        (["git", "status", "--porcelain=v1", "--untracked-files=all"], "status"),
        (["git", "diff", "--name-only", "HEAD"], "diff"),
    ):
        proc = subprocess.run(args, cwd=root, capture_output=True, text=True)
        git[key] = proc.stdout
        git[key + ":exit"] = str(proc.returncode)
    return {"files": files, "dirs": sorted(dirs), "symlinks": symlinks, "git": git}


class LongformPublicationIntegrationV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in _GIT_VARS:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        self.workspace = Path(__file__).resolve().parents[1]
        scratch = tempfile.TemporaryDirectory(prefix="jgas-lf2i-")
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "config", "schemas", "scripts", "templates", "prompts", "docs", "data"],
            cwd=self.workspace, capture_output=True, check=True,
        ).stdout
        copied: set[str] = set()
        for raw in tracked.split(b"\0"):
            if not raw:
                continue
            relative = Path(raw.decode("utf-8"))
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.workspace / relative, destination)
            copied.add(relative.as_posix())
        overlay_hashes: dict[str, str] = {}
        for rel in (*OVERLAY_LF1, *OVERLAY_NEW):
            source = self.workspace / rel
            self.assertTrue(source.is_file(), f"overlay source missing: {rel}")
            overlay_hashes[rel] = core.sha256_file(source)
            destination = self.root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        self.overlay_hashes = overlay_hashes
        fixture_env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Synthetic LF-2I Fixture",
            "GIT_AUTHOR_EMAIL": "synthetic-lf2i@example.invalid",
            "GIT_COMMITTER_NAME": "Synthetic LF-2I Fixture",
            "GIT_COMMITTER_EMAIL": "synthetic-lf2i@example.invalid",
        }
        for command in (
            ["git", "init", "-q"],
            ["git", "remote", "add", "origin", "https://example.invalid/lf2i-fixture.git"],
            ["git", "add", "-A"],
            ["git", "-c", "user.name=Synthetic LF-2I Fixture",
             "-c", "user.email=synthetic-lf2i@example.invalid",
             "commit", "-q", "-m", "Synthetic isolated LF-2I source basis"],
        ):
            subprocess.run(command, cwd=self.root, check=True, capture_output=True, env=fixture_env)
        listed = subprocess.run(
            ["git", "config", "--local", "--list"], cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout
        self.assertNotIn("user.name=", listed)
        self.assertNotIn("user.email=", listed)
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)
        self.head = core.repository_commit_sha(self.root)
        self.source_root = self.root / "sources" / ISSUE
        self.survey_root = self.root / "surveys" / "special" / ISSUE
        self.publication_root = self.source_root / "publication" / "v2"
        worker = lf1_tests.LongformDerivationV2Tests(
            methodName="test_valid_single_did_projects_every_category"
        )
        worker.root = self.root
        worker.cfg = self.cfg
        worker.head = self.head
        worker.workspace = self.workspace
        test_self = self

        def _bound_authored(chain: dict, review_reference: str = "fixture longform review") -> dict:
            return test_self._authored(chain, worker, review_reference)

        worker._authored = _bound_authored
        base_helper_factory = worker._evidence_helper

        def _clean_evidence_helper():
            # DID-free accepted locators end to end: the Gate lexical scanner
            # flags repository Discovery IDs even inside bibliography URLs, so
            # the synthetic chain carries clean canonical locators from the
            # Discovery record itself (task/card/provenance stay consistent).
            helper = base_helper_factory()
            original_discovery = helper.discovery

            def _clean_discovery(issue_id: str, discovery_id: str, origin: str = "BASE") -> dict:
                record = original_discovery(issue_id, discovery_id, origin)
                record["source"] = helper.source(URL_BY_DID[discovery_id])
                return record

            helper.discovery = _clean_discovery
            return helper

        worker._evidence_helper = _clean_evidence_helper
        self.worker = worker

    # ---- accepted-chain helpers (real producers/validators only) ----

    def _chain(self) -> dict:
        return self.worker._chain(dids=(DID1,))

    def _authored(self, chain: dict, worker, review_reference: str = "fixture longform review") -> dict:
        rows = []
        for pid in chain["draft_paths"]:
            row = worker._revision_row(pid, worker._did_for_package(chain, pid))
            for note in row["technical_notes"]:
                note["primary_url"] = URL1
            rows.append(row)
        dids = [did for pid in chain["draft_paths"] for did in worker._did_for_package(chain, pid)]
        return {
            "schema_version": "2.0-rc1",
            "issue_id": ISSUE,
            "runner": "LONGFORM_SPECIAL",
            "cover": {"headline": "Fixture lineage cover", "deck": "Source-based lineage survey",
                      "anchors": ["Target Model"]},
            "frontmatter": {"heading": "Fixture frontmatter", "lede": "A bounded lineage survey.",
                            "scope_notes": ["One accepted primary source per package."]},
            "final_summary": {"heading": "この号の総括", "paragraphs": [
                "The edition surveys accepted lineage sources.",
                "The claims remain attributed to their origins.",
                "The synthesis stays inside authorized evidence.",
            ]},
            "longform_revision": {
                "review_reference": review_reference,
                "new_external_evidence": False,
                "packages": rows,
                "cross_family_synthesis": {
                    "heading": "Fixture cross-family synthesis",
                    "paragraphs": [
                        {"text": "Fixture cross paragraph one.", "discovery_ids": list(dids)},
                        {"text": "Fixture cross paragraph two.", "discovery_ids": list(dids)},
                    ],
                    "comparison_rows": [
                        {"dimension": f"Fixture aspect {number}", "glm": "Fixture GLM.",
                         "qwen": "Fixture Qwen.", "deepseek": "Fixture DeepSeek.",
                         "kimi": "Fixture Kimi.", "discovery_ids": list(dids)}
                        for number in (1, 2, 3)
                    ],
                },
            },
        }

    def _complete(self, chain: dict) -> dict:
        return self.worker._complete_authorities(chain)

    def _advance(self, chain: dict, stage: str, artifacts: dict[str, Path], minute: int) -> None:
        state_path = chain["source_root"] / "production-state.json"
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], stage)
        stamp = core.parse_instant(f"2026-08-22T{4 + minute // 60:02d}:{minute % 60:02d}:00+09:00")
        report = chain["source_root"] / "orchestration/v2/reviews" / f"{stage}-core-contract.json"
        stage_validation.validate_stage(self.root, self.cfg, state_path, artifacts, report, stamp)
        review_path = report.with_name(f"{stage}-reviews.json")
        core.write_json(review_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "synthetic LF-2I fixture using actual stage validator",
            "evidence": "actual stage validator PASS for exact synthetic edition authorities",
            "result_path": str(review_path.parent.joinpath(report.name).relative_to(self.root)),
        }]})
        checkpoint = agent.build_stage_checkpoint(
            self.root, self.cfg, state_path, artifacts, review_path,
            f"Synthetic LF-2I {stage} fixture stage was validated.", stamp,
        )
        updated = agent.advance_with_checkpoint(self.root, self.cfg, state_path, checkpoint)
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])

    def _state_path(self, chain: dict) -> Path:
        return self.worker._current_state(chain)

    def _pass1(self, chain: dict, state_path: Path) -> Path:
        argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                "--state", str(state_path), "--input", str(chain["authored_path"]),
                "--materialize-surface-only"]
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(longform_publication.main(), 0)
        surface_path = self.publication_root / "reader-surface-input-v2.json"
        self.assertTrue(surface_path.is_file())
        return surface_path

    def _pass_review(self, surface_path: Path, reviewed_by: str = "synthetic LF-2I reviewer") -> Path:
        review_path = self.publication_root / "reader-surface-semantic-review-v2.json"
        review = {
            "schema_version": "2.0-rc1", "issue_id": ISSUE,
            "publication_profile": "LONGFORM_SPECIAL", "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {"path": str(surface_path.relative_to(self.root)),
                                 "sha256": core.sha256_file(surface_path)},
            "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                        "detail": "Synthetic reviewer judged the complete fixture prose independently understandable.",
                        "evidence_locations": ["reader-surface-input-v2.json:packages",
                                               "reader-surface-input-v2.json:bibliography"]}],
            "decision": "PASS", "reviewed_by": reviewed_by,
            "reviewed_at": "2026-08-22T05:00:00+09:00", "recorded_at": "2026-08-22T05:00:00+09:00",
            "status": "PASSED", "findings": [],
            "summary": "Synthetic PASS after inspection of the complete fixture reader input.",
        }
        review["review_sha256"] = core.sha256_object(review)
        core.write_json(review_path, review)
        return review_path

    def _pass2(self, chain: dict, state_path: Path) -> dict[str, Path]:
        argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                "--state", str(state_path), "--input", str(chain["authored_path"])]
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(longform_publication.main(), 0)
        paths = {
            role: path for role, path in (
                ("surface", self.publication_root / "reader-surface-input-v2.json"),
                ("review", self.publication_root / "reader-surface-semantic-review-v2.json"),
                ("primary", self.survey_root / "main.tex"),
                ("bibliography", self.survey_root / "references.bib"),
                ("style", self.survey_root / "jgaisurvey.sty"),
                ("archive", self.publication_root / "interactive-semantic-publication-input.json"),
                ("receipt", self.publication_root / "validated-source-manifest.json"),
            )
        }
        for role, path in paths.items():
            self.assertTrue(path.is_file(), f"pass2 missing {role}")
        return paths

    def _section_locations(self, chain: dict, surface: dict[str, Any], main_text: str) -> tuple[list[str], str]:
        blocks, _ = fidelity.parse_longform_blocks(main_text)
        packages = surface["packages"]
        self.assertEqual(len(blocks), len(packages) + 2)
        for position, package in enumerate(packages):
            self.assertEqual(blocks[position].title, tex_escape(package["headline"]))
        self.assertEqual(blocks[len(packages)].title, tex_escape(surface["cross_family_synthesis"]["heading"]))
        self.assertEqual(blocks[len(packages) + 1].title, tex_escape(surface["final_summary"]["heading"]))
        locations = [block.canonical_location for block in blocks]
        return locations[:len(packages)], locations[-1]

    def _manuscript_inputs(self, chain: dict, surface: dict[str, Any], main_text: str) -> tuple[list[dict], list[dict]]:
        architecture = core.load_json(chain["source_root"] / "architecture-v2.json")
        package_locations, final_location = self._section_locations(chain, surface, main_text)
        coverage = [
            {"package_id": package["package_id"], "requirement": requirement,
             "status": "FULFILLED", "reader_locations": [location],
             "detail": "Synthetic fixture author maps the accepted package requirement to its source section."}
            for package, location in zip(architecture["packages"], package_locations)
            for requirement in package["must_cover_requirements"]
        ]
        requirements = [
            {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
             "reader_locations": [final_location],
             "detail": "Synthetic fixture author asserts this visible requirement is present."}
        ]
        return coverage, requirements

    def _build_pdf(self) -> Path:
        pdf_path = self.survey_root / "main.pdf"
        pdf = PdfWriter()
        pdf.add_blank_page(width=595, height=842)
        with pdf_path.open("wb") as output:
            pdf.write(output)
        self.assertEqual(len(PdfReader(pdf_path).pages), 1)
        log_path = self.survey_root / "main.log"
        checksum_path = self.survey_root / "main.pdf.sha256"
        log_path.write_text("synthetic build log\n", encoding="utf-8")
        checksum_path.write_text(core.sha256_file(pdf_path) + "  main.pdf\n", encoding="utf-8")
        return pdf_path

    def _quality_bundle(self, chain: dict, pdf_path: Path) -> Path:
        bundle_path = self.publication_root / "quality-regression-bundle-v2.json"
        result_paths = {}
        payloads = {
            "SUBJECT_ENTITY_PROPERTY_BINDING": {
                "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS", "issue_id": ISSUE,
                "cited_discovery_count": 1,
                "bindings": [{"discovery_id": DID1, "canonical_name": "Target Model",
                              "canonical_url": URL1, "materiality": "MATERIAL",
                              "status": "VERIFIED", "source_accessed_at": "2026-08-22T02:10:00+09:00"}],
            },
            "IDENTIFIER_PRESERVATION": {
                "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                "source_sha256": core.sha256_file(self.survey_root / "main.tex"),
                "inspected_identifiers": [ISSUE, "Target Model"],
                "scope": "synthetic generated fixture",
            },
            "PDF_PREFLIGHT": {
                "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": 1,
                "pdf_sha256": core.sha256_file(pdf_path), "byte_count": pdf_path.stat().st_size,
                "scope": "synthetic parseable one-page PDF; not a TeX rendering",
            },
            "EMPTY_WRAPPER_SUPPRESSION": {
                "check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
                "scope": "synthetic generated fixture carries no empty wrapper",
                "inspected_paths": ["surveys/special/SP001/main.tex"],
            },
        }
        kinds = quality.expected_checks_by_kind(self.cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})
        self.assertEqual(set(payloads), set(kinds))
        quality_checks = []
        for check_id, payload in payloads.items():
            path = self.publication_root / "quality" / f"{check_id.lower()}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            core.write_json(path, payload)
            result_paths[check_id] = path
            quality_checks.append({
                "check_id": check_id, "kind": kinds[check_id], "status": "PASS",
                "executor": "synthetic LF-2I fixture with actual file assertions",
                "evidence": "Exact fixture bytes and result file inspected by test.",
                "recorded_at": "2026-08-22T05:20:00+09:00",
                "result": {"path": str(path.relative_to(self.root)), "sha256": core.sha256_file(path)},
            })
        quality.build_bundle(
            self.root, ISSUE, self.survey_root / "main.tex", pdf_path, quality_checks,
            bundle_path, production_profile_path=chain["profile_path"],
        )
        return bundle_path

    def _publication_reviews(self, chain: dict, manuscript_path: Path, pdf_path: Path,
                             coverage_locations: list[str], final_locations: list[str],
                             reviewed_by: str = "synthetic LF-2I review author",
                             prefix: str = "") -> dict[str, Path]:
        profile = core.load_json(chain["profile_path"])
        architecture = core.load_json(chain["source_root"] / "architecture-v2.json")
        package_ids = [row["package_id"] for row in architecture["packages"]]
        final_package = max(architecture["packages"], key=lambda row: row["drafting_order"])["package_id"]
        paths: dict[str, Path] = {}
        for kind, name in (("SEMANTIC_EDITORIAL", f"{prefix}semantic-editorial-review-v2.json"),
                           ("VISUAL", f"{prefix}visual-review-v2.json")):
            expected = reader_publication._expected_review_checks(self.root, profile, kind)
            checks = []
            for check_id in sorted(expected):
                evidence = ["synthetic-fixture:main.tex"]
                if check_id in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                    evidence = sorted(
                        {f"package:{pid}" for pid in package_ids} | set(coverage_locations)
                    )
                    if check_id == "LONGFORM_TECHNICAL_DEPTH":
                        evidence = sorted(set(evidence) | {
                            "page-plan:1/12", "density-review:below-target-substantive"})
                elif check_id == "FINAL_SYNTHESIS_QUALITY":
                    evidence = sorted(
                        set(final_locations) | {"reader-role:final-synthesis", f"package:{final_package}"}
                    )
                elif check_id == "LONGFORM_MIXED_LAYOUT":
                    evidence = ["reader-layout:wide-surfaces-full-width",
                                "reader-layout:references-one-column",
                                "reader-layout:balanced-two-column-narrative"]
                checks.append({
                    "check_id": check_id, "status": "PASS",
                    "detail": "Synthetic fixture review; no real editorial or visual acceptance asserted.",
                    "evidence_locations": evidence,
                })
            path = self.publication_root / name
            reader_publication.build_review_record(
                self.root, manuscript_path, pdf_path, 1, kind, checks, reviewed_by,
                core.parse_instant("2026-08-22T05:30:00+09:00"), path,
            )
            paths[kind] = path
        return paths

    def _build_manuscript(self, chain: dict, surface: dict[str, Any], main_text: str,
                          name: str = "reader-manuscript-v2.json",
                          authored_by: str = "synthetic LF-2I manuscript author") -> Path:
        coverage, requirements = self._manuscript_inputs(chain, surface, main_text)
        if name != "reader-manuscript-v2.json":
            for row in coverage:
                row["detail"] = "Decoy manuscript detail for the same issue; locations unchanged."
        manuscript_path = self.publication_root / name
        reader_publication.build_manuscript_manifest(
            self.root, ISSUE, chain["profile_path"], chain["source_root"] / "architecture-v2.json",
            chain["approval_path"], self.survey_root / "main.tex",
            [{"role": "BIBLIOGRAPHY", "path": str((self.survey_root / "references.bib").relative_to(self.root))},
             {"role": "STYLE", "path": str((self.survey_root / "jgaisurvey.sty").relative_to(self.root))}],
            coverage, requirements, authored_by,
            core.parse_instant("2026-08-22T05:10:00+09:00"), manuscript_path,
        )
        return manuscript_path

    def _build_gate(self, manuscript_path: Path, review_path: Path, name: str = "reader-surface-gate-v2.json") -> Path:
        gate_path = self.publication_root / name
        reader_publication.build_reader_surface_gate(
            self.root, manuscript_path, review_path, output_path=gate_path,
            state_path=self.source_root / "production-state.json",
        )
        gate = reader_gate.validate_reader_surface_gate(
            self.root, gate_path, issue_id=ISSUE, publication_profile="LONGFORM_SPECIAL",
            expected_manuscript_path=manuscript_path,
            state_path=self.source_root / "production-state.json",
        )
        self.assertEqual(gate["status"], "PASSED")
        self.assertEqual(gate["derivation"]["route"], generated.ROUTE)
        self.assertEqual(gate["derivation"]["scope"], generated.SCOPE)
        return gate_path

    def _advance_to_validated_draft(self, chain: dict, state_path: Path) -> dict[str, Path]:
        surface_path = self._pass1(chain, state_path)
        review_path = self._pass_review(surface_path)
        paths = self._pass2(chain, state_path)
        surface = core.load_json(surface_path)
        main_text = (self.survey_root / "main.tex").read_text(encoding="utf-8")
        manuscript_path = self._build_manuscript(chain, surface, main_text)
        pdf_path = self._build_pdf()
        bundle_path = self._quality_bundle(chain, pdf_path)
        coverage, _ = self._manuscript_inputs(chain, surface, main_text)
        coverage_locations = sorted({location for row in coverage for location in row["reader_locations"]})
        _, requirements = self._manuscript_inputs(chain, surface, main_text)
        final_locations = [location for row in requirements for location in row["reader_locations"]]
        review_paths = self._publication_reviews(
            chain, manuscript_path, pdf_path, coverage_locations, final_locations)
        gate_path = self._build_gate(manuscript_path, review_path)
        generated.validate_receipt(
            self.root, paths["receipt"], self.source_root / "production-state.json")
        self._advance(chain, "DRAFT_COMPLETE", {
            "reader-manuscript": manuscript_path,
            "validated-source": self.survey_root / "main.tex",
            "publication-pdf": pdf_path,
            "quality-regression-bundle": bundle_path,
            "semantic-review": review_paths["SEMANTIC_EDITORIAL"],
            "visual-review": review_paths["VISUAL"],
            "reader-surface-gate": gate_path,
        }, 130)
        self.assertEqual(
            core.load_json(self.source_root / "production-state.json")["lifecycle_state"], "VALIDATED_DRAFT")
        generated.validate_receipt(
            self.root, paths["receipt"], self.source_root / "production-state.json")
        reader_gate.validate_reader_surface_gate(
            self.root, gate_path, expected_manuscript_path=manuscript_path,
            state_path=self.source_root / "production-state.json",
        )
        return {**paths, "manuscript": manuscript_path, "pdf": pdf_path,
                "bundle": bundle_path, "gate": gate_path, **review_paths}

    # ---- selected boundary: two-pass gating ----

    def test_two_pass_initial_reviewer_gating(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        for absent in ("main.tex", "references.bib", "jgaisurvey.sty",
                       "validated-source-manifest.json"):
            holder = (self.survey_root / absent) if absent != "validated-source-manifest.json" else (
                self.publication_root / absent)
            self.assertFalse(holder.exists(), f"pass1 must not materialize {absent}")
        argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                "--state", str(state_path), "--input", str(chain["authored_path"])]
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "semantic review artifact missing"):
                longform_publication.main()
        before = _snapshot(self.root)
        self.assertFalse((self.survey_root / "main.tex").exists())
        self.assertFalse((self.publication_root / "validated-source-manifest.json").exists())
        review_path = self.publication_root / "reader-surface-semantic-review-v2.json"
        good_review = {
            "schema_version": "2.0-rc1", "issue_id": ISSUE,
            "publication_profile": "LONGFORM_SPECIAL", "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {"path": str(surface_path.relative_to(self.root)),
                                 "sha256": core.sha256_file(surface_path)},
            "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                        "detail": "Synthetic reviewer judged the complete fixture prose independently understandable.",
                        "evidence_locations": ["reader-surface-input-v2.json:packages"]}],
            "decision": "PASS", "reviewed_by": "synthetic LF-2I reviewer",
            "reviewed_at": "2026-08-22T05:00:00+09:00", "recorded_at": "2026-08-22T05:00:00+09:00",
            "status": "PASSED", "findings": [],
            "summary": "Synthetic PASS after inspection of the complete fixture reader input.",
        }
        good_review["review_sha256"] = core.sha256_object(good_review)
        for failure, message in (
            ("wrong-target", "Reviewed surface bytes drifted"),
            ("non-pass", "did not yield PASS decision"),
            ("legacy-shape", "must be reader-surface-semantic-review-v2"),
        ):
            bad_review = copy.deepcopy(good_review)
            if failure == "wrong-target":
                bad_review["reviewed_surface"]["sha256"] = "0" * 64
            elif failure == "non-pass":
                bad_review["decision"] = "FAIL"
                bad_review["status"] = "FAILED"
            else:
                bad_review.pop("reviewed_surface")
                bad_review["review_kind"] = "SEMANTIC_EDITORIAL"
            bad_review["review_sha256"] = core.sha256_object({
                key: value for key, value in bad_review.items() if key != "review_sha256"
            })
            core.write_json(review_path, bad_review)
            with self.subTest(review_failure=failure), mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, message):
                    longform_publication.main()
            self.assertFalse((self.survey_root / "main.tex").exists())
            self.assertFalse((self.publication_root / "validated-source-manifest.json").exists())
        core.write_json(review_path, good_review)
        extra = self.survey_root / "hyperref.sty"
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("% inert local package shadow\n", encoding="utf-8")
        try:
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "build directory invalid.*undeclared entry"):
                    longform_publication.main()
            self.assertFalse((self.survey_root / "main.tex").exists())
            self.assertFalse((self.publication_root / "validated-source-manifest.json").exists())
        finally:
            extra.unlink()
        paths = self._pass2(chain, state_path)
        generated.validate_receipt(self.root, paths["receipt"], state_path)
        # Pass1 byte-equality reuse: a second materialize-only run reuses the
        # exact same bytes instead of overwriting.
        with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
            self.assertEqual(longform_publication.main(), 0)
        self.assertEqual(_snapshot(self.root)["git"]["head"], before["git"]["head"])

    def test_receipt_replay_tamper_matrix_and_tool_guards(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        self._pass_review(surface_path)
        paths = self._pass2(chain, state_path)
        receipt_path = paths["receipt"]
        receipt_original = receipt_path.read_bytes()
        generated.validate_receipt(self.root, receipt_path, state_path)
        for role, file_path in (
            ("primary", self.survey_root / "main.tex"),
            ("bibliography", self.survey_root / "references.bib"),
            ("style", self.survey_root / "jgaisurvey.sty"),
        ):
            with self.subTest(rehashed_output=role):
                original = file_path.read_bytes()
                file_path.write_bytes(original + b"\n% synthetic changed output\n")
                changed_receipt = core.load_json(receipt_path)
                changed_receipt["outputs"][role]["sha256"] = core.sha256_file(file_path)
                changed_receipt["receipt_sha256"] = core.sha256_object({
                    key: value for key, value in changed_receipt.items() if key != "receipt_sha256"
                })
                core.write_json(receipt_path, changed_receipt)
                with self.assertRaisesRegex(ValueError, f"deterministic {role} replay mismatch"):
                    generated.validate_receipt(self.root, receipt_path, state_path)
                file_path.write_bytes(original)
                receipt_path.write_bytes(receipt_original)
        reviewed_original = surface_path.read_bytes()
        changed_surface = core.load_json(surface_path)
        changed_surface["cover"]["headline"] = "Unreviewed replacement headline"
        core.write_json(surface_path, changed_surface)
        changed_receipt = core.load_json(receipt_path)
        changed_receipt["reviewed_reader_input"]["sha256"] = core.sha256_file(surface_path)
        changed_receipt["receipt_sha256"] = core.sha256_object({
            key: value for key, value in changed_receipt.items() if key != "receipt_sha256"
        })
        core.write_json(receipt_path, changed_receipt)
        with self.assertRaisesRegex(ValueError, "reviewed reader input drift|surface bytes drifted|recomputed reader input differs"):
            generated.validate_receipt(self.root, receipt_path, state_path)
        surface_path.write_bytes(reviewed_original)
        receipt_path.write_bytes(receipt_original)
        review_path = paths["review"]
        review_original = review_path.read_bytes()
        review_path.write_bytes(review_original + b" ")
        with self.assertRaisesRegex(ValueError, "semantic review mismatch"):
            generated.validate_receipt(self.root, receipt_path, state_path)
        review_path.write_bytes(review_original)
        closure_path = self.root / "scripts/survey_longform_generated_v2.py"
        closure_original = closure_path.read_bytes()
        closure_path.write_bytes(closure_original + b"\n# synthetic uncommitted control change\n")
        try:
            with self.assertRaisesRegex(ValueError, "differs from committed HEAD"):
                generated.validate_receipt(self.root, receipt_path, state_path)
        finally:
            closure_path.write_bytes(closure_original)
        stray = self.root / "scripts/synthetic-uncommitted-helper.py"
        stray.write_text("# synthetic untracked control source\n", encoding="utf-8")
        try:
            with self.assertRaisesRegex(ValueError, "uncommitted source"):
                generated.validate_receipt(self.root, receipt_path, state_path)
        finally:
            stray.unlink()
        generated.validate_receipt(self.root, receipt_path, state_path)

    def test_gate_and_both_admission_backstops(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        review_path = self._pass_review(surface_path)
        paths = self._pass2(chain, state_path)
        surface = core.load_json(surface_path)
        main_text = (self.survey_root / "main.tex").read_text(encoding="utf-8")
        manuscript_path = self._build_manuscript(chain, surface, main_text)
        pdf_path = self._build_pdf()
        bundle_path = self._quality_bundle(chain, pdf_path)
        coverage, _ = self._manuscript_inputs(chain, surface, main_text)
        coverage_locations = sorted({location for row in coverage for location in row["reader_locations"]})
        _, requirements = self._manuscript_inputs(chain, surface, main_text)
        final_locations = [location for row in requirements for location in row["reader_locations"]]
        review_paths = self._publication_reviews(
            chain, manuscript_path, pdf_path, coverage_locations, final_locations)
        gate_path = self._build_gate(manuscript_path, review_path)
        decoy_path = self._build_manuscript(
            chain, surface, main_text, name="decoy-manuscript-v2.json",
            authored_by="synthetic LF-2I decoy manuscript author")
        with self.assertRaisesRegex(ValueError, "does not bind the exact expected Reader Manuscript"):
            reader_gate.validate_reader_surface_gate(
                self.root, gate_path, issue_id=ISSUE, publication_profile="LONGFORM_SPECIAL",
                expected_manuscript_path=decoy_path,
                state_path=self.source_root / "production-state.json",
            )
        decoy_pub_reviews = self._publication_reviews(
            chain, decoy_path, pdf_path, coverage_locations, final_locations,
            reviewed_by="synthetic LF-2I decoy review author", prefix="decoy-pub-")
        renamed = dict(decoy_pub_reviews)
        # Stage-site negative at DRAFT_COMPLETE uses decoy manuscript + decoy
        # reviews against the exact-manuscript Gate: Gate-layer refusal.
        before = _snapshot(self.root)
        with self.assertRaisesRegex(stage_validation.StageValidationError, "Reader-Surface Gate validation failed"):
            self._advance(chain, "DRAFT_COMPLETE", {
                "reader-manuscript": decoy_path,
                "validated-source": self.survey_root / "main.tex",
                "publication-pdf": pdf_path,
                "quality-regression-bundle": bundle_path,
                "semantic-review": renamed["SEMANTIC_EDITORIAL"],
                "visual-review": renamed["VISUAL"],
                "reader-surface-gate": gate_path,
            }, 131)
        self.assertEqual(_snapshot(self.root), before)
        self._advance(chain, "DRAFT_COMPLETE", {
            "reader-manuscript": manuscript_path,
            "validated-source": self.survey_root / "main.tex",
            "publication-pdf": pdf_path,
            "quality-regression-bundle": bundle_path,
            "semantic-review": review_paths["SEMANTIC_EDITORIAL"],
            "visual-review": review_paths["VISUAL"],
            "reader-surface-gate": gate_path,
        }, 130)
        self.assertEqual(
            core.load_json(self.source_root / "production-state.json")["lifecycle_state"], "VALIDATED_DRAFT")
        candidate_path = self.publication_root / "publication-candidate-v2.json"
        publication.build_candidate(
            self.root, ISSUE, "LONGFORM_SPECIAL", manuscript_path, self.survey_root / "main.tex",
            pdf_path, 1, bundle_path, review_paths["SEMANTIC_EDITORIAL"], review_paths["VISUAL"],
            candidate_path,
        )
        decoy_candidate = self.publication_root / "decoy-publication-candidate-v2.json"
        publication.build_candidate(
            self.root, ISSUE, "LONGFORM_SPECIAL", decoy_path, self.survey_root / "main.tex",
            pdf_path, 1, bundle_path, renamed["SEMANTIC_EDITORIAL"], renamed["VISUAL"],
            decoy_candidate,
        )
        before = _snapshot(self.root)
        with self.assertRaisesRegex(stage_validation.StageValidationError, "does not bind exact"):
            self._advance(chain, "VALIDATED_DRAFT", {"publication-candidate": decoy_candidate}, 132)
        self.assertEqual(_snapshot(self.root), before)
        self._advance(chain, "VALIDATED_DRAFT", {"publication-candidate": candidate_path}, 133)
        self.assertEqual(
            core.load_json(self.source_root / "production-state.json")["lifecycle_state"], "RELEASE_CANDIDATE")
        for extra in (decoy_path, decoy_candidate, *renamed.values(), *decoy_pub_reviews.values()):
            if extra.exists():
                extra.unlink()

    def test_healthy_frozen_released_readback(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        paths = self._advance_to_validated_draft(chain, state_path)
        state_file = self.source_root / "production-state.json"
        candidate_path = self.publication_root / "publication-candidate-v2.json"
        review_paths = {"SEMANTIC_EDITORIAL": paths["SEMANTIC_EDITORIAL"], "VISUAL": paths["VISUAL"]}
        publication.build_candidate(
            self.root, ISSUE, "LONGFORM_SPECIAL", paths["manuscript"], self.survey_root / "main.tex",
            paths["pdf"], 1, paths["bundle"], review_paths["SEMANTIC_EDITORIAL"],
            review_paths["VISUAL"], candidate_path,
        )
        self._advance(chain, "VALIDATED_DRAFT", {"publication-candidate": candidate_path}, 140)
        self.assertEqual(core.load_json(state_file)["lifecycle_state"], "RELEASE_CANDIDATE")
        agent.approve_publication_preview(
            self.root, self.cfg, state_file, "synthetic-human-fixture",
            core.parse_instant("2026-08-22T07:00:00+09:00"), "synthetic:publication-preview",
        )
        approval_rel = self.cfg["state_authority"]["publication_preview_approval_path"]
        approval_path = self.source_root / approval_rel
        self.assertTrue(approval_path.is_file())
        freeze_path = self.publication_root / "freeze-record-v2.json"
        manifest_path = self.publication_root / "release-manifest-v2.json"
        publication.build_freeze(
            self.root, candidate_path, approval_path,
            core.parse_instant("2026-08-22T08:00:00+09:00"), freeze_path, manifest_path,
        )
        candidate_payload = publication.validate_candidate(self.root, candidate_path, issue_id=ISSUE)
        visual_path = self.root / candidate_payload["visual_review"]["path"]
        self._advance(chain, "RELEASE_CANDIDATE", {
            "freeze-record": freeze_path,
            "release-manifest": manifest_path,
            "visual-review-record": visual_path,
        }, 141)
        self.assertEqual(core.load_json(state_file)["lifecycle_state"], "FROZEN")
        frozen_context = derivation.load_derivation_for_readback(
            self.root, state_file, paths["archive"])
        self.assertEqual(frozen_context["surface"], core.load_json(paths["surface"]))
        generated.validate_receipt(self.root, paths["receipt"], state_file)
        with self.assertRaisesRegex(ValueError, "exact DRAFT_COMPLETE"):
            derivation.load_derivation(self.root, state_file, paths["archive"])
        merge_path = self.publication_root / "merge-verification-v2.json"
        record_path = self.publication_root / "release-record-v2.json"
        publication.build_merge_verification(
            self.root, manifest_path, core.repository_commit_sha(self.root),
            core.parse_instant("2026-08-22T09:00:00+09:00"), merge_path,
        )
        publication.build_release_record(
            self.root, manifest_path, merge_path,
            core.parse_instant("2026-08-22T09:30:00+09:00"), "synthetic-lf2i-release", record_path,
        )
        checkpoint = release_checkpoint.build_release_checkpoint(
            self.root, self.cfg, state_file, merge_path, record_path,
            core.parse_instant("2026-08-22T10:00:00+09:00"),
        )
        updated = agent.advance_with_checkpoint(self.root, self.cfg, state_file, checkpoint)
        self.assertEqual(updated["lifecycle_state"], "RELEASED")
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])
        released_context = derivation.load_derivation_for_readback(
            self.root, state_file, paths["archive"])
        self.assertEqual(released_context["surface"], core.load_json(paths["surface"]))
        generated.validate_receipt(self.root, paths["receipt"], state_file)
        reader_gate.validate_reader_surface_gate(
            self.root, paths["gate"], expected_manuscript_path=paths["manuscript"], state_path=state_file,
        )
        ghost = self.source_root / "synthetic-ghost-state.json"
        altered = core.load_json(state_file)
        altered["lifecycle_state"] = "COMPLETE"
        core.write_json(ghost, altered)
        try:
            with self.assertRaisesRegex(ValueError, "Production State invalid for Longform readback"):
                derivation.load_derivation_for_readback(self.root, ghost, paths["archive"])
        finally:
            ghost.unlink()

    def test_mechanical_only_change_rebinds_without_reader_drift(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        first = derivation.load_derivation(self.root, state_path, chain["authored_path"])
        first_bytes = derivation.canonical_reader_bytes(first["surface"])
        authored = copy.deepcopy(core.load_json(chain["authored_path"]))
        authored["runner"] = "LONGFORM_SPECIAL-RENEWED"
        authored["longform_revision"]["review_reference"] = "fixture longform review renewed"
        variant_path = chain["source_root"] / "semantic-publication-input-renewed.json"
        core.write_json(variant_path, authored)
        try:
            second = derivation.load_derivation(self.root, state_path, variant_path)
            self.assertEqual(derivation.canonical_reader_bytes(second["surface"]), first_bytes)
            self.assertNotEqual(
                core.sha256_file(variant_path), core.sha256_file(chain["authored_path"]))
        finally:
            variant_path.unlink()

    def test_pure_serializer_scanner_and_review_probes(self) -> None:
        # Labelled pure/schema/helper probes: no lifecycle/stage/CLI evidence.
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        context = derivation.load_derivation(self.root, state_path, chain["authored_path"])
        surface = context["surface"]
        derivation.validate_longform_reader_input(self.root, surface)
        first = generated.render_main(surface)
        self.assertEqual(generated.render_main(copy.deepcopy(surface)), first)
        self.assertIn("\\renewcommand{\\contentsname}{目次}", first)
        self.assertIn("Target Model", first)
        self.assertIn(URL1, first)
        bib_keys = [row["key"] for row in surface["bibliography"]]
        for key in bib_keys:
            self.assertIn(f"\\cite{{{key}}}", first)
        with self.assertRaisesRegex(ValueError, "no reviewed bibliography key"):
            generated._cite(["missing-did"], {row["discovery_id"]: row["key"] for row in surface["bibliography"]})
        with self.assertRaisesRegex(ValueError, "at least one source"):
            generated.render_bibliography({"bibliography": []})
        with self.assertRaisesRegex(ValueError, "bibliography declaration"):
            generated.validate_generated_closure(first.replace("\\addbibresource{references.bib}", ""), "")
        findings = reader_gate.scan_structured_reader_surface(surface, "probe-surface")
        self.assertIsInstance(findings, list)
        leaked = copy.deepcopy(surface)
        leaked["cover"]["headline"] = "Probe headline with an internal Verify obligation."
        leaked_findings = reader_gate.scan_structured_reader_surface(leaked, "probe-surface")
        blocking = [row for row in leaked_findings if row.severity == "BLOCKING" and row.disposition == "UNRESOLVED"]
        self.assertTrue(blocking, "nested Longform scanner must flag leaked prose")
        # Full serializer/scanner category matrix (table-driven, pure probes).
        pid = surface["packages"][0]["package_id"]
        categories = [
            ("cover.headline", ("cover", "headline")),
            ("frontmatter.heading", ("frontmatter", "heading")),
            ("package.headline", ("packages", 0, "headline")),
            ("package.kicker", ("packages", 0, "kicker")),
            ("narrative.heading", ("packages", 0, "narrative_sections", 0, "heading")),
            ("synthesis.heading", ("packages", 0, "synthesis", "heading")),
            ("note.title", ("packages", 0, "technical_notes", 0, "title")),
            ("cross.heading", ("cross_family_synthesis", "heading")),
            ("final.heading", ("final_summary", "heading")),
            ("bibliography.title", ("bibliography", 0, "title")),
        ]
        for label, locator in categories:
            with self.subTest(scanner_category=label):
                mutated = copy.deepcopy(surface)
                node: object = mutated
                for step in locator[:-1]:
                    node = node[step]  # type: ignore[index]
                assert isinstance(node, dict) or isinstance(node, list)
                if isinstance(node, list):
                    node[locator[-1]] = "Probe Verify leakage"  # type: ignore[index]
                else:
                    node[locator[-1]] = "Probe Verify leakage"  # type: ignore[index]
                found = reader_gate.scan_structured_reader_surface(mutated, "probe-surface")
                self.assertTrue(
                    any(r.severity == "BLOCKING" and r.disposition == "UNRESOLVED" for r in found),
                    f"scanner must flag {label}",
                )

    def test_pass2_missing_surface_refuses_without_silent_pass1(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        self.assertTrue(surface_path.is_file())
        # Remove surface to simulate missing pass1 output; pass2 must refuse
        # without silently recreating it (no-write).
        surface_path.unlink()
        self.assertFalse(surface_path.exists())
        before = _snapshot(self.root)
        argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                "--state", str(state_path), "--input", str(chain["authored_path"])]
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "already materialized exact reader input|without silently doing pass1"):
                longform_publication.main()
        after = _snapshot(self.root)
        self.assertEqual(after, before)
        self.assertFalse(surface_path.exists())
        self.assertFalse((self.publication_root / "validated-source-manifest.json").exists())
        # Pass1 recreates the exact same bytes; pass2 still needs review.
        with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
            self.assertEqual(longform_publication.main(), 0)
        self.assertTrue(surface_path.is_file())
        # Pass1 pre-mkdir eligibility: undeclared survey entry refuses before surface write.
        surface_path.unlink()
        extra = self.survey_root / "undeclared-shadow.tex"
        extra.parent.mkdir(parents=True, exist_ok=True)
        extra.write_text("% undeclared\n", encoding="utf-8")
        try:
            before = _snapshot(self.root)
            with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
                with self.assertRaisesRegex(SystemExit, "build directory invalid.*undeclared entry"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
            self.assertFalse(surface_path.exists())
        finally:
            extra.unlink()
        # Pass1 with pre-existing partial outputs refuses fresh surface write.
        surface_path.unlink(missing_ok=True)
        self.survey_root.mkdir(parents=True, exist_ok=True)
        partial = self.survey_root / "main.tex"
        partial.write_text("% partial\n", encoding="utf-8")
        try:
            before = _snapshot(self.root)
            with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
                with self.assertRaisesRegex(SystemExit, "pre-existing partial output"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
            self.assertFalse(surface_path.exists())
        finally:
            partial.unlink()
        # Healthy pass1 still succeeds after cleanup.
        with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
            self.assertEqual(longform_publication.main(), 0)

    def test_alias_directive_and_lifecycle_containment(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        review_path = self._pass_review(surface_path)
        argv2 = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                 "--state", str(state_path), "--input", str(chain["authored_path"])]
        # State leaf symlink refuses with no-write.
        real_state = state_path.read_bytes()
        alias_state = chain["source_root"] / "alias-state.json"
        if alias_state.exists() or os.path.lexists(alias_state):
            alias_state.unlink() if not alias_state.is_symlink() else os.unlink(alias_state)
        os.symlink(state_path.name, alias_state)
        try:
            before = _snapshot(self.root)
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(alias_state.relative_to(self.root)), "--input",
                    str(chain["authored_path"].relative_to(self.root)), "--materialize-surface-only"]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "leaf alias is unsafe|containment invalid"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            os.unlink(alias_state)
        # Input parent symlink refuses.
        parent_alias = self.root / "sources" / "alias-parent"
        try:
            if os.path.lexists(parent_alias):
                os.unlink(parent_alias)
            os.symlink(ISSUE, parent_alias)
            before = _snapshot(self.root)
            aliased_input = parent_alias / "semantic-publication-input.json"
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(state_path.relative_to(self.root)), "--input",
                    str(aliased_input.relative_to(self.root)) if not aliased_input.is_absolute() else str(aliased_input),
                    "--materialize-surface-only"]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "symlinked ancestor|leaf alias|containment invalid|derivation invalid"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            if os.path.lexists(parent_alias):
                os.unlink(parent_alias)
        # Review leaf alias (explicit path) refuses before any source write.
        alias_review = self.publication_root / "alias-review.json"
        if os.path.lexists(alias_review):
            os.unlink(alias_review)
        os.symlink(review_path.name, alias_review)
        try:
            before = _snapshot(self.root)
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(state_path), "--input", str(chain["authored_path"]),
                    "--semantic-review", str(alias_review)]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "leaf alias is unsafe|semantic review path invalid"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
            self.assertFalse((self.survey_root / "main.tex").exists())
        finally:
            os.unlink(alias_review)
        # Dangling review destination refuses.
        dangling = self.publication_root / "dangling-review.json"
        if os.path.lexists(dangling):
            os.unlink(dangling)
        os.symlink("nonexistent-target.json", dangling)
        try:
            before = _snapshot(self.root)
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(state_path), "--input", str(chain["authored_path"]),
                    "--semantic-review", str(dangling)]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "leaf alias is unsafe|semantic review path invalid|missing on disk"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            os.unlink(dangling)
        # Publication output directory alias refuses before mkdir/write.
        # Use a fresh chain location would be expensive; simulate by aliasing a
        # new source_root sibling? Instead verify _strict_dir_preflight directly
        # plus a no-write pass1 when publication parent is aliased is covered by
        # ancestor check: create aliased publication parent.
        pub_parent_alias = chain["source_root"] / "publication-alias"
        if os.path.lexists(pub_parent_alias):
            os.unlink(pub_parent_alias)
        os.symlink("publication", pub_parent_alias)
        try:
            before = _snapshot(self.root)
            # Direct preflight must refuse the aliased directory itself.
            with self.assertRaisesRegex(ValueError, "leaf alias is unsafe|symlinked ancestor"):
                longform_publication._strict_dir_preflight(
                    self.root, os.path.relpath(pub_parent_alias / "v2", self.root),
                    "Longform publication output directory")
            self.assertEqual(_snapshot(self.root), before)
        finally:
            os.unlink(pub_parent_alias)
        # Directive file presence refuses (regular file).
        directive = chain["source_root"] / "editorial" / "post-architecture-directives-v2.json"
        directive.parent.mkdir(parents=True, exist_ok=True)
        directive.write_text('{"directive": true}\n', encoding="utf-8")
        try:
            # Surface already exists so reuse path still loads derivation which must refuse directive.
            # Remove surface to force derivation through directive check on fresh write path.
            surface_path.unlink()
            before = _snapshot(self.root)
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(state_path), "--input", str(chain["authored_path"]),
                    "--materialize-surface-only"]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "unsupported directive authority|derivation invalid"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            directive.unlink()
            # Restore surface for later tests in this fixture (no cross-test sharing).
            with mock.patch.object(sys, "argv", argv2 + ["--materialize-surface-only"]):
                longform_publication.main()
        # Directive symlink (including dangling) refuses.
        os.symlink("nonexistent-directive.json", directive)
        try:
            surface_path.unlink(missing_ok=True)
            before = _snapshot(self.root)
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(state_path), "--input", str(chain["authored_path"]),
                    "--materialize-surface-only"]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "unsupported directive authority|derivation invalid"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            os.unlink(directive)
        # Wrong-path same-byte review, VISUAL review, and pending/later CLI refusal.
        surface_path = self.publication_root / "reader-surface-input-v2.json"
        if not surface_path.exists():
            with mock.patch.object(sys, "argv", argv2 + ["--materialize-surface-only"]):
                longform_publication.main()
        good = core.load_json(review_path) if review_path.exists() else None
        # Wrong-path same bytes: copy review bytes to alternate contained path; pass2 with
        # explicit alternate path must still succeed (override permitted) but default-path
        # replay binds exact file SHA, so alternate receipt path is distinct. Here we only
        # assert the loader binds the alternate path strictly (no silent default fallback).
        alt_review = self.publication_root / "alt-review.json"
        if good is not None:
            core.write_json(alt_review, good)
            try:
                validated = reader_gate.load_and_validate_reader_surface_semantic_review(
                    self.root, alt_review, expected_issue_id=ISSUE,
                    expected_publication_profile="LONGFORM_SPECIAL", require_pass=True)
                self.assertEqual(validated["review_path"], str(alt_review.relative_to(self.root)))
            finally:
                alt_review.unlink()
        # VISUAL review refuses in pass2.
        visual = copy.deepcopy(core.load_json(review_path))
        visual["review_kind"] = "VISUAL"
        visual.pop("review_sha256", None)
        visual["review_sha256"] = core.sha256_object(visual)
        core.write_json(review_path, visual)
        try:
            before = _snapshot(self.root)
            with mock.patch.object(sys, "argv", argv2):
                with self.assertRaisesRegex(SystemExit, "semantic review validation FAILED"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            assert good is not None
            core.write_json(review_path, good)

    def test_snapshot_drift_partial_retention_and_canonical_replay(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        review_path = self._pass_review(surface_path)
        input_raw_before = (chain["authored_path"]).read_bytes()
        paths = self._pass2(chain, state_path)
        receipt_path = paths["receipt"]
        receipt_original = receipt_path.read_bytes()
        # Exact raw input bytes archived (not re-canonicalized parsed JSON).
        archived = (self.publication_root / "interactive-semantic-publication-input.json").read_bytes()
        self.assertEqual(archived, input_raw_before)
        # Accepted/State drift before writes refuses tested via direct recheck helper:
        # mutate State file after snapshot, then pass2 on fresh outputs must refuse.
        # Use a second issue-less mutation inside this fixture: tamper review then restore.
        before = _snapshot(self.root)
        review_bytes = review_path.read_bytes()
        review_path.write_bytes(review_bytes + b" ")
        try:
            with self.assertRaisesRegex(ValueError, "semantic review mismatch|digest mismatch|missing"):
                generated.validate_receipt(self.root, receipt_path, state_path)
            self.assertEqual(_snapshot(self.root)["git"]["head"], before["git"]["head"])
        finally:
            review_path.write_bytes(review_bytes)
        generated.validate_receipt(self.root, receipt_path, state_path)
        # Alternate serialization (same object, noncanonical bytes) fails FILE-byte replay.
        surface_bytes = surface_path.read_bytes()
        noncanonical = surface_bytes.replace(b": ", b":").replace(b",\n", b",")
        if noncanonical != surface_bytes:
            surface_path.write_bytes(noncanonical)
            try:
                with self.assertRaisesRegex(ValueError, "FILE bytes differ|drift|recomputed"):
                    generated.validate_receipt(self.root, receipt_path, state_path)
            finally:
                surface_path.write_bytes(surface_bytes)
            generated.validate_receipt(self.root, receipt_path, state_path)
        # Alternate canonical-looking directory fails path authority: tampered receipt
        # pointing at a sibling v2-alt surface (same bytes, fresh hash) must refuse
        # on canonical edition path, not merely hash equality.
        alt_dir = chain["source_root"] / "publication" / "v2-alt"
        alt_dir.mkdir(parents=True, exist_ok=True)
        try:
            alt_surface = alt_dir / "reader-surface-input-v2.json"
            alt_surface.write_bytes(surface_bytes)
            tampered = core.load_json(receipt_path)
            tampered["reviewed_reader_input"] = {
                "path": str(alt_surface.relative_to(self.root)),
                "sha256": core.sha256_file(alt_surface),
            }
            tampered["receipt_sha256"] = core.sha256_object(
                {k: v for k, v in tampered.items() if k != "receipt_sha256"})
            core.write_json(receipt_path, tampered)
            with self.assertRaisesRegex(ValueError, "canonical|reviewed target|drift"):
                generated.validate_receipt(self.root, receipt_path, state_path)
        finally:
            import shutil as _shutil
            _shutil.rmtree(alt_dir, ignore_errors=True)
            receipt_path.write_bytes(receipt_original)
        # Fresh rehash alone is not the sole oracle: tampered output + fresh hash still fails replay.
        main_path = self.survey_root / "main.tex"
        main_original = main_path.read_bytes()
        main_path.write_bytes(main_original + b"\n% synthetic changed output\n")
        try:
            tampered = core.load_json(receipt_path)
            tampered["outputs"]["primary"]["sha256"] = core.sha256_file(main_path)
            tampered["receipt_sha256"] = core.sha256_object(
                {k: v for k, v in tampered.items() if k != "receipt_sha256"})
            core.write_json(receipt_path, tampered)
            with self.assertRaisesRegex(ValueError, "deterministic primary replay mismatch"):
                generated.validate_receipt(self.root, receipt_path, state_path)
        finally:
            main_path.write_bytes(main_original)
            receipt_path.write_bytes(receipt_original)
        generated.validate_receipt(self.root, receipt_path, state_path)
        # Injected write failure retains partial with no unlink and refuses retry.
        # Write-seam fault (not a success-validator mock): second exclusive write
        # raises after the first output was installed.
        (self.survey_root / "main.tex").unlink()
        (self.survey_root / "references.bib").unlink()
        (self.survey_root / "jgaisurvey.sty").unlink()
        (self.publication_root / "interactive-semantic-publication-input.json").unlink()
        (self.publication_root / "validated-source-manifest.json").unlink()
        before = _snapshot(self.root)
        argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                "--state", str(state_path), "--input", str(chain["authored_path"])]
        real_write = longform_publication._write_bytes_exclusive
        calls: list[str] = []

        def _faulting_write(path: Path, data: bytes, label: str) -> None:
            calls.append(str(path))
            if len(calls) == 2:
                path.write_bytes(data[: len(data) // 2])
                raise OSError("synthetic mid-write fault for LF-2I retention proof")
            return real_write(path, data, label)

        with mock.patch.object(longform_publication, "_write_bytes_exclusive", side_effect=_faulting_write):
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(SystemExit, "materialization failed|retained owned partial"):
                    longform_publication.main()
        after = _snapshot(self.root)
        self.assertTrue((self.survey_root / "main.tex").is_file())
        self.assertTrue((self.survey_root / "references.bib").is_file())
        self.assertFalse((self.publication_root / "validated-source-manifest.json").exists())
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "refusing existing Longform publication artifact"):
                longform_publication.main()
        key = str((self.survey_root / "main.tex").relative_to(self.root))
        self.assertEqual(_snapshot(self.root)["files"].get(key), after["files"].get(key))
        for p in (self.survey_root / "main.tex", self.survey_root / "references.bib"):
            if p.exists():
                p.unlink()

    def test_heading_delimiter_subprocess_and_gate_cli(self) -> None:
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        context = derivation.load_derivation(self.root, state_path, chain["authored_path"])
        surface = context["surface"]
        # Positive punctuation/escaping controls (must pass pre-write validation).
        positive = copy.deepcopy(surface)
        positive["packages"][0]["narrative_sections"][0]["heading"] = "Fixture heading: scope, range — 1/2 (flat)."
        generated.validate_heading_syntax(positive)
        main_ok = generated.render_main(positive)
        generated.validate_generated_closure(main_ok, (self.root / generated.STYLE_PATH).read_text(encoding="utf-8"))
        blocks, _ = fidelity.parse_longform_blocks(main_ok)
        self.assertTrue(len(blocks) >= len(surface["packages"]) + 2)
        # Precise unsupported-character no-write cases (each refuses before writes).
        for bad, label in [
            ("Bad {brace} heading", "braces"),
            ("Bad \\ backslash heading", "backslash"),
            ("Bad ~ tilde heading", "tilde"),
            ("Bad ^ circumflex heading", "circumflex"),
        ]:
            with self.subTest(unsupported=label):
                mutated = copy.deepcopy(surface)
                mutated["packages"][0]["headline"] = bad
                with self.assertRaisesRegex(ValueError, "unsupported TeX heading character"):
                    generated.validate_heading_syntax(mutated)
        with self.subTest(unsupported="optional-delimiter"):
            mutated = copy.deepcopy(surface)
            mutated["packages"][0]["technical_notes"][0]["title"] = "Note with ] delimiter"
            with self.assertRaisesRegex(ValueError, "optional-argument delimiter"):
                generated.validate_heading_syntax(mutated)
        # End-to-end no-write: unsupported heading in authored input refuses before surface write.
        authored = copy.deepcopy(core.load_json(chain["authored_path"]))
        # Authored revision heading flows into surface headline? Use narrative heading via revision row.
        authored["longform_revision"]["packages"][0]["narrative_sections"][0]["heading"] = "Bad {brace} authored"
        bad_authored = chain["source_root"] / "bad-authored.json"
        core.write_json(bad_authored, authored)
        try:
            before = _snapshot(self.root)
            argv = ["survey_longform_semantic_publication_v2.py", "--repo-root", str(self.root),
                    "--state", str(state_path), "--input", str(bad_authored),
                    "--materialize-surface-only"]
            with mock.patch.object(sys, "argv", argv):
                # Derivation itself may refuse lexical leakage or heading syntax refuses at publisher preflight.
                with self.assertRaisesRegex(SystemExit, "heading syntax invalid|derivation invalid|leaks production metadata"):
                    longform_publication.main()
            self.assertEqual(_snapshot(self.root), before)
        finally:
            bad_authored.unlink()
        # Actual subprocess CLI pass1/pass2 (not in-process argv monkeypatch).
        surface_path = self._pass1(chain, state_path)
        review_path = self._pass_review(surface_path)
        env = {k: v for k, v in os.environ.items() if k not in _GIT_VARS}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        cmd1 = [sys.executable, "-m", "scripts.survey_longform_semantic_publication_v2",
                "--repo-root", str(self.root), "--state", str(state_path.relative_to(self.root)),
                "--input", str(chain["authored_path"].relative_to(self.root)), "--materialize-surface-only"]
        proc = subprocess.run(cmd1, cwd=str(self.workspace), capture_output=True, text=True, env=env, timeout=300)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        cmd2 = [sys.executable, "-m", "scripts.survey_longform_semantic_publication_v2",
                "--repo-root", str(self.root), "--state", str(state_path.relative_to(self.root)),
                "--input", str(chain["authored_path"].relative_to(self.root))]
        proc = subprocess.run(cmd2, cwd=str(self.workspace), capture_output=True, text=True, env=env, timeout=300)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        # Actual Gate CLI persisted-review path (validate-gate) on the built gate.
        paths = {"surface": surface_path, "review": review_path}
        # Build gate via in-process helper then validate via CLI.
        surf = core.load_json(surface_path)
        main_text = (self.survey_root / "main.tex").read_text(encoding="utf-8") if (self.survey_root / "main.tex").exists() else generated.render_main(surf)
        if not (self.survey_root / "main.tex").exists():
            # Materialize already done by subprocess pass2 above; reload.
            pass
        manuscript_path = self._build_manuscript(chain, surf, (self.survey_root / "main.tex").read_text(encoding="utf-8"))
        gate_path = self._build_gate(manuscript_path, review_path)
        gate_cli = [sys.executable, "-m", "scripts.survey_reader_surface_gate_v2",
                    "--repo-root", str(self.root), "validate-gate", "--gate",
                    str(gate_path.relative_to(self.root)), "--issue-id", ISSUE, "--profile", "LONGFORM_SPECIAL",
                    "--state", str((self.source_root / "production-state.json").relative_to(self.root))]
        proc = subprocess.run(gate_cli, cwd=str(self.workspace), capture_output=True, text=True, env=env, timeout=300)
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("PASSED", proc.stdout)
        # Both exact same-issue manuscript Gate-site backstops with valid authority:
        # VALIDATED_DRAFT site already covered; here prove Gate-layer exact-manuscript
        # backstop at VALIDATED_DRAFT with an otherwise coherent same-issue chain
        # (decoy manuscript binds different bytes but same issue).
        decoy = self._build_manuscript(chain, surf, (self.survey_root / "main.tex").read_text(encoding="utf-8"),
                                       name="cli-decoy-manuscript-v2.json")
        before = _snapshot(self.root)
        with self.assertRaisesRegex(ValueError, "does not bind the exact expected Reader Manuscript"):
            reader_gate.validate_reader_surface_gate(
                self.root, gate_path, issue_id=ISSUE, publication_profile="LONGFORM_SPECIAL",
                expected_manuscript_path=decoy, state_path=self.source_root / "production-state.json")
        self.assertEqual(_snapshot(self.root), before)
        for extra in (decoy,):
            if extra.exists():
                extra.unlink()

    def test_valid_initial_operation_same_reader_with_mechanical_rebind(self) -> None:
        # Valid initial-operation same-reader/review with changed mechanical authoring
        # binding (not a regeneration owner): runner + review_reference change only.
        chain = self._complete(self._chain())
        state_path = self._state_path(chain)
        surface_path = self._pass1(chain, state_path)
        review_path = self._pass_review(surface_path)
        first_surface_bytes = surface_path.read_bytes()
        first_review = core.load_json(review_path)
        # Changed mechanical binding, same reader bytes, same review file SHA.
        authored = copy.deepcopy(core.load_json(chain["authored_path"]))
        authored["runner"] = "LONGFORM_SPECIAL-REBOUND"
        authored["longform_revision"]["review_reference"] = "fixture longform review rebound"
        rebound_path = chain["source_root"] / "rebound-authored.json"
        core.write_json(rebound_path, authored)
        try:
            second = derivation.load_derivation(self.root, state_path, rebound_path)
            self.assertEqual(derivation.canonical_reader_bytes(second["surface"]), first_surface_bytes)
            # Same persisted review still validates the same reader bytes.
            validated = reader_gate.load_and_validate_reader_surface_semantic_review(
                self.root, review_path, expected_issue_id=ISSUE,
                expected_publication_profile="LONGFORM_SPECIAL",
                expected_surface_path=surface_path,
                expected_surface_sha256=core.sha256_file(surface_path), require_pass=True)
            self.assertEqual(validated["surface_sha256"], core.sha256_file(surface_path))
            self.assertEqual(first_review["review_sha256"], core.load_json(review_path)["review_sha256"])
        finally:
            rebound_path.unlink()


if __name__ == "__main__":
    unittest.main()
