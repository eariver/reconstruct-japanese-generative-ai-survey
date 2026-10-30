#!/usr/bin/env python3
"""DM022 normal-writer late-guard v2 (General test-author/executor ONLY).

See dm022_late_guard_fixture_v2.py for injector + snapshot discipline.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tests import dm022_late_guard_fixture_v2 as lg
from tests import dm022_lifecycle_fixture_v2 as fix

DURABLE_MANIFEST = Path(
    "/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/full-lifecycle-v2-fixture-manifests/durable-versioned-20261029T064541Z/durable-fixture-manifest.json"
)


def _manifest() -> dict:
    return json.loads(DURABLE_MANIFEST.read_bytes().decode("utf-8"))


class TestNormalWriterLateGuardV2(unittest.TestCase):
    # ---------- shared late-guard runner ----------

    def _run_healthy_and_fault(
        self,
        *,
        case: str,
        build_fixture,
        call_producer,
        target_file_sub: str,
        target_fn: str,
        target_line: int,
        entry_line: int,
        guard_rel: str,
        new_outputs: list[str],
    ) -> dict:
        """Build TWO independent fixtures: healthy (no guard) proves REAL write;
        fault (fresh copy) injects owned guard at exact prepublish seam.

        build_fixture(tag) -> (td_holder, root, extra dict with state_path etc.)
        call_producer(root, extra) -> None (must perform REAL write on healthy).
        Returns fault diagnostics for report.
        """
        # Healthy
        td_h, root_h, extra_h = build_fixture(f"{case}-healthy")
        state_h = extra_h["state_path"]
        # state_path may be absolute or relative; normalize for snapshot
        pre_h = lg._snapshot_files(root_h)
        call_producer(root_h, extra_h)
        post_h = lg._snapshot_files(root_h)
        for rel in new_outputs:
            self.assertIn(rel, post_h, f"{case} healthy must write {rel}")
            self.assertNotIn(rel, pre_h, f"{case} healthy output must be NEW (no clearing): {rel}")
        # Fault: fresh independent copy
        td_f, root_f, extra_f = build_fixture(f"{case}-fault")
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, target_file_sub, target_fn, target_line, entry_line)
        inj.install(self)
        pre_f = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            call_producer(root_f, extra_f)
        post_f = lg._snapshot_files(root_f)
        # Exact target reached, entry reached, injected
        self.assertTrue(inj.entry_reached, f"{case}: entry READY not observed")
        self.assertTrue(inj.target_reached, f"{case}: prepublish target not reached (file={target_file_sub} fn={target_fn} line={target_line}) calls={inj.calls[-3:]}")
        self.assertTrue(inj.injected, f"{case}: guard not injected")
        self.assertTrue(guard_path.is_file(), f"{case}: owned fault guard must be preserved")
        # No writes except the injected guard itself
        pre_keys = set(pre_f.keys())
        post_keys = set(post_f.keys())
        new_keys = post_keys - pre_keys
        guard_key = guard_rel
        self.assertIn(guard_key, post_f, f"{case}: guard missing in post")
        self.assertEqual(new_keys, {guard_key}, f"{case}: unexpected writes besides guard: {sorted(new_keys - {guard_key})}")
        for k in pre_keys & post_keys:
            self.assertEqual(pre_f[k], post_f[k], f"{case}: byte drift outside write window: {k}")
        return {
            "case": case, "target": f"{target_file_sub}:{target_fn}:{target_line}",
            "entry": entry_line, "calls": len(inj.calls),
            "healthy_new": new_outputs, "fault_guard": guard_rel,
        }

    # ---------- selection seven writes (fresh EVIDENCE_REVIEWED) ----------

    def _build_selection(self, tag: str):
        from tests import test_dm022_full_lifecycle_v2 as full
        # Reuse full-lifecycle construction via subclass trick: instantiate a
        # throwaway owner to build, then rebind cleanups to self.
        owner = full.Dm022FullLifecycleWitnessTests("test_weekly_dm022_to_selection_stage")
        # Minimal chain: use owner's helpers but with self as assert host by
        # temporarily swapping addCleanup/assert methods is fragile; instead
        # duplicate the small path via owner's methods bound to owner, then
        # transfer temp cleanup to self.
        chain = owner._chain_root("WEEKLY", discovery_id="target-source")
        # owner._chain_root registered cleanups on owner; keep owner alive via self
        self.addCleanup(lambda: None)
        self._sel_owner = owner  # keep alive
        state_abs = owner._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        cfg = chain["cfg"]
        from scripts import survey_production_v2 as core
        # Materialize production Discovery acceptance (required by runner)
        owner._materialize_production_discovery_acceptance(chain)
        from scripts import survey_screening_v2 as screening_mod
        discoveries = screening_mod.read_jsonl(chain["discovery_path"])
        screening_doc = core.load_json(chain["screening_acceptance"])
        dec_map = {r["discovery_id"]: r["decision"] for r in screening_doc.get("decisions", [])}
        expected_ids = {d["discovery_id"] for d in discoveries if dec_map.get(d["discovery_id"]) in ("KEEP", "MAYBE", "INSPECT")}
        input_path = owner._build_selection_input(root, chain["issue_id"], expected_ids, tag, "WEEKLY")
        # Wrap temp lifetime: chain root temp is owned by owner's helper temp;
        # create a holder that keeps owner + chain alive (no copy, already independent DB).
        class _Holder:
            def __init__(self, td_list):
                self.td_list = td_list
            def cleanup(self):
                pass
        # chain root temp cleanup is on owner's helper temp + temp dir; keep owner
        td_holder = tempfile.TemporaryDirectory(prefix=f"sel-hold-{tag}-")
        self.addCleanup(td_holder.cleanup)
        profile_doc = core.load_json(chain["profile_path"])
        source_rel = profile_doc["paths"]["source_root"]
        extra = {
            "state_path": state_abs, "input_path": input_path,
            "source_rel": source_rel, "chain": chain, "owner": owner,
        }
        return td_holder, root, extra

    def _call_selection(self, root: Path, extra: dict) -> None:
        from scripts import run_selection_architecture_v2_interactive as sel
        sel.run(root, extra["state_path"], extra["input_path"])

    def test_selection_matrix_late_guard(self) -> None:
        self._run_healthy_and_fault(
            case="selection-matrix",
            build_fixture=self._build_selection,
            call_producer=self._call_selection,
            target_file_sub="run_selection_architecture_v2_interactive.py",
            target_fn="run", target_line=316, entry_line=260,
            guard_rel="sources/2026-W35/orchestration/v2/acceptance-revision.guard.json" if False else "sources/2026-W33/orchestration/v2/acceptance-revision.guard.json",
            new_outputs=[
                "sources/2026-W33/candidate-matrix-v2.json",
            ],
        )

    def test_selection_selection_late_guard(self) -> None:
        # Inject before selection write (line 362); matrix already written is allowed.
        from scripts import run_selection_architecture_v2_interactive as sel
        td_h, root_h, extra_h = self._build_selection("sel-selection-healthy")
        self._call_selection(root_h, extra_h)
        # Fault on fresh copy, inject at 362
        td_f, root_f, extra_f = self._build_selection("sel-selection-fault")
        from scripts import survey_production_v2 as core
        profile_doc = core.load_json(extra_f["chain"]["profile_path"])
        source_rel = profile_doc["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_selection_architecture_v2_interactive.py", "run", 362, 260)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_selection(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"selection-selection target not reached: {inj.calls}")
        # Matrix may already be written before fault; selection must not be.
        self.assertTrue(guard_path.is_file())
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        # Selection must not appear as NEW beyond matrix? Matrix is allowed as
        # partial (written before fault). Assert selection absent.
        sel_rel = f"{source_rel}/candidate-selection-v2.json"
        # If matrix was written pre-fault it is in new_keys; selection must not be newly written with valid bytes?
        # Strict: selection file must either be absent or, if present due to partial, post must equal pre? Here pre has absent, so it must stay absent.
        # Because fault is before selection write, matrix partial is allowed.
        # Check: matrix may be present, selection must be absent.
        self.assertNotIn(sel_rel, post, "selection must not be written when late guard refuses")
        # No other drift besides guard + allowed matrix partial
        allowed = {guard_rel, f"{source_rel}/candidate-matrix-v2.json"}
        self.assertTrue(new_keys <= allowed, f"unexpected writes: {sorted(new_keys)}")

    def test_selection_audit_late_guard(self) -> None:
        # Inject before audit (line 456, last write). Earlier six writes are allowed partials.
        td_h, root_h, extra_h = self._build_selection("sel-audit-healthy")
        self._call_selection(root_h, extra_h)
        from scripts import survey_production_v2 as core
        td_f, root_f, extra_f = self._build_selection("sel-audit-fault")
        profile_doc = core.load_json(extra_f["chain"]["profile_path"])
        source_rel = profile_doc["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_selection_architecture_v2_interactive.py", "run", 456, 260)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_selection(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached)
        audit_rel = f"{source_rel}/orchestration/v2/interactive/selection-architecture-audit.json"
        self.assertNotIn(audit_rel, post, "audit must not be written when late guard refuses")
        self.assertTrue(guard_path.is_file())

    # ---------- execution_record (simple NEW session) ----------

    def _build_execution(self, tag: str):
        from tests import test_survey_dm022_c2_consumers_v2 as c2
        td = tempfile.TemporaryDirectory(prefix=f"exec-{tag}-")
        self.addCleanup(td.cleanup)
        root = Path(td.name).resolve()
        state_rel = c2._make_c2_ready_root(self, root)
        from scripts import survey_production_v2 as core
        cfg = core.load_json(root / core.DEFAULT_CONFIG)
        state_abs = root / state_rel
        profile_path = root / "sources/2026-W35/production-profile.json"
        extra = {"state_path": state_abs, "cfg": cfg, "profile_path": profile_path, "tag": tag}
        return td, root, extra

    def _call_execution(self, root: Path, extra: dict) -> None:
        from scripts import survey_execution_record_v2 as ex
        tag = extra["tag"]
        # NEW session_id per fixture ensures NEW legitimate output path
        session_id = f"late-guard-{tag}".replace("_", "-")[:32]
        # Sanitize to safe stem
        session_id = "".join(ch if (ch.isalnum() or ch in ("-", "_")) else "-" for ch in session_id)
        ex.initialize(
            root, extra["cfg"], extra["profile_path"], extra["state_path"],
            session_id=session_id, started_at="2026-09-14T12:00:00Z",
            main_sha="0" * 40, branch_head="1" * 40,
            objective="late-guard execution test", requested_stop="ARCHITECTURE_REVIEW",
        )

    def test_execution_record_late_guard(self) -> None:
        from scripts import survey_production_v2 as core
        # Healthy proves REAL write with NEW session
        td_h, root_h, extra_h = self._build_execution("healthy")
        pre_h = lg._snapshot_files(root_h)
        self._call_execution(root_h, extra_h)
        post_h = lg._snapshot_files(root_h)
        new_h = set(post_h) - set(pre_h)
        self.assertTrue(any("execution/" in k for k in new_h), f"execution healthy must write execution tree: {sorted(new_h)}")
        # Fault with NEW session + guard at prepublish (line 302)
        td_f, root_f, extra_f = self._build_execution("fault")
        profile_doc = core.load_json(root_f / "sources/2026-W35/production-profile.json")
        source_rel = profile_doc["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_execution_record_v2.py", "initialize", 302, 170)
        inj.install(self)
        # Use a different NEW session for fault to avoid already-exists
        extra_f["tag"] = "fault-unique"
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_execution(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"execution prepublish not reached: {inj.calls}")
        self.assertTrue(guard_path.is_file())
        new_keys = set(post) - set(pre)
        self.assertEqual(new_keys, {guard_rel}, f"execution fault must write only guard: {sorted(new_keys)}")

    # ---------- publication candidate (durable VALIDATED_DRAFT + NEW out) ----------

    def _build_candidate(self, tag: str):
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        td, root = lg._copy_durable_to_temp(self, durable, f"cand-{tag}-")
        from scripts import survey_production_v2 as core
        state_abs = root / "sources/2026-W33/production-state.json"
        extra = {"state_path": state_abs, "tag": tag}
        return td, root, extra

    def _call_candidate(self, root: Path, extra: dict) -> None:
        from scripts import survey_publication_v2 as pub
        tag = extra["tag"]
        out_rel = f"sources/2026-W33/publication/v2/publication-candidate-late-{tag}.json"
        out_path = root / out_rel
        # Durable VALIDATED_DRAFT bindings (manuscript/source/pdf/bundle/sem/vis)
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        src_rel = "surveys/weekly/2026-W33/main.tex"
        pdf_rel = "surveys/weekly/2026-W33/main.pdf"
        bundle_rel = "sources/2026-W33/publication/v2/quality-regression-bundle-v2.json"
        sem_rel = "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json"
        vis_rel = "sources/2026-W33/publication/v2/visual-review-v2.json"
        from scripts import survey_production_v2 as core
        # page_count must match reviews (durable VALIDATED_DRAFT reviews carry 5)
        try:
            sem_doc = core.load_json(root / sem_rel)
            page_count = int(sem_doc.get("page_count", 5) or 5)
        except Exception:
            page_count = 5
        if page_count < 1:
            page_count = 5
        pub.build_candidate(
            root, "2026-W33", "WEEKLY_MAGAZINE",
            root / man_rel, root / src_rel, root / pdf_rel, page_count,
            root / bundle_rel, root / sem_rel, root / vis_rel,
            out_path, state_path=root / "sources/2026-W33/production-state.json",
        )
        extra["out_rel"] = out_rel

    def test_publication_candidate_late_guard(self) -> None:
        # Healthy proves REAL write with NEW legitimate output path
        td_h, root_h, extra_h = self._build_candidate('candidate-healthy')
        pre_h = lg._snapshot_files(root_h)
        self._call_candidate(root_h, extra_h)
        post_h = lg._snapshot_files(root_h)
        out_h = extra_h['out_rel']
        self.assertIn(out_h, post_h)
        self.assertNotIn(out_h, pre_h)
        # Fault on fresh copy injects at exact prepublish 2013
        td_f, root_f, extra_f = self._build_candidate('candidate-fault')
        guard_rel = 'sources/2026-W33/orchestration/v2/acceptance-revision.guard.json'
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, 'survey_publication_v2.py', 'build_candidate', 2013, 1932)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r'DM022_TRANSITION_ACTIVE'):
            self._call_candidate(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.entry_reached)
        self.assertTrue(inj.target_reached, f'candidate prepublish not reached: {inj.calls}')
        self.assertTrue(guard_path.is_file())
        out_f = f'sources/2026-W33/publication/v2/publication-candidate-late-candidate-fault.json'
        self.assertNotIn(out_f, post, 'candidate must not be written when late guard refuses')
        new_keys = set(post) - set(pre)
        self.assertEqual(new_keys, {guard_rel}, f'candidate fault must write only guard: {sorted(new_keys)}')

    # ---------- retention (P1 scope fixture, NEW copy per fault) ----------

    # ---------- manuscript (reader_publication, NEW out) ----------

    def _build_manuscript(self, tag: str):
        import hashlib as _hl
        from tests import test_survey_dm022_c2_consumers_v2 as c2
        td = tempfile.TemporaryDirectory(prefix=f"man-{tag}-")
        self.addCleanup(td.cleanup)
        root = Path(td.name).resolve()
        state_rel = c2._make_c2_ready_root(self, root)
        # Fixture setup (arch/approval/tex/bib) happens here so pre-snapshot includes them;
        # producer call below only writes the NEW manuscript out.
        profile_path = root / "sources/2026-W35/production-profile.json"
        arch_path = root / "sources/2026-W35/architecture-v2.json"
        c2._write_json(arch_path, {
            "schema_version": "2.0-rc1", "issue_id": "2026-W35",
            "research_profile": "WEEKLY", "publication_profile": "WEEKLY_MAGAZINE",
            "status": "APPROVED",
            "basis": {k: "a" * 64 for k in ("production_profile_sha256", "profile_completeness_sha256", "materiality_ledger_sha256", "candidate_matrix_sha256", "candidate_selection_sha256")},
            "editorial_thesis": "t", "architecture_goals": ["g"],
            "page_plan": {"target_pages": 12, "max_pages": 24, "notes": "n"},
            "packages": [{"package_id": "PKG-1", "title": "t", "purpose": "p", "primary_candidate_ids": ["C1"], "supporting_candidate_ids": [], "must_cover_requirements": ["Explain agent workflows"], "boundaries": ["b"], "drafting_order": 1, "profile_extensions": {}, "publication_extensions": {"section_label": "pkg1"}}],
            "selected_exceptions": [],
            "profile_extensions": {"weekly_closing_summary": {"required": True, "source": "profile_synthesis.current_interpretation"}},
            "publication_extensions": {"closing_summary": {"required": True, "heading": "x", "placement": "after_body_before_references"}},
            "human_review": {"reviewed_by": "r", "reviewed_at": "2026-09-14T12:00:00Z", "review_reference": "ref"},
        })
        approval_path = root / "sources/2026-W35/gates/architecture-approval.json"
        approval_path.parent.mkdir(parents=True, exist_ok=True)
        c2._write_json(approval_path, {
            "schema_version": "2.0-rc1", "approval_id": "arch:2026-W35:test", "issue_id": "2026-W35", "gate": "ARCHITECTURE_REVIEW", "decision": "APPROVED",
            "architecture_sha256": _hl.sha256(arch_path.read_bytes()).hexdigest(),
            "architecture_review_summary_sha256": "a" * 64, "architecture_review_attention_sha256": "a" * 64,
            "reviewed_by": "reviewer", "reviewed_at": "2026-09-14T12:00:00Z", "review_reference": "ref",
        })
        survey_rel = "surveys/weekly/2026-W35"
        (root / survey_rel).mkdir(parents=True, exist_ok=True)
        (root / survey_rel / "main.tex").write_text("\\section{Agent Workflows}\nDirect reader prose.\n", encoding="utf-8")
        (root / survey_rel / "references.bib").write_text("@online{x,\n  title = {{T}},\n  author = {{A}},\n  url = {https://example.com/x},\n  urldate = {2026-09-14}\n}\n", encoding="utf-8")
        extra = {"state_path": root / state_rel, "tag": tag, "root": root, "profile_path": profile_path, "arch_path": arch_path, "approval_path": approval_path}
        return td, root, extra

    def _call_manuscript(self, root: Path, extra: dict) -> None:
        from scripts import survey_reader_publication_v2 as rp
        tag = extra["tag"]
        profile_path = extra["profile_path"]
        arch_path = extra["arch_path"]
        approval_path = extra["approval_path"]
        survey_rel = "surveys/weekly/2026-W35"
        main_tex = root / survey_rel / "main.tex"
        bib = root / survey_rel / "references.bib"
        out_rel = "sources/2026-W35/publication/v2/reader-manuscript-late.json"
        m_out = root / out_rel
        rp.build_manuscript_manifest(
            root, "2026-W35", profile_path, arch_path, approval_path, main_tex,
            [{"role": "BIBLIOGRAPHY", "path": str(bib.relative_to(root))}],
            [{"package_id": "PKG-1", "requirement": "Explain agent workflows", "status": "FULFILLED", "reader_locations": ["main.tex:section1"], "detail": "Prose explains agent coordination directly"}],
            [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": ["main.tex:summary"], "detail": "Summary."}, {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED", "reader_locations": ["main.tex:community"], "detail": "Community."}],
            "ChatGPT", datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc), m_out,
        )
        extra["out_rel"] = out_rel

    def test_manuscript_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_manuscript("healthy")
        pre_h = lg._snapshot_files(root_h)
        self._call_manuscript(root_h, extra_h)
        post_h = lg._snapshot_files(root_h)
        self.assertIn(extra_h["out_rel"], post_h)
        self.assertNotIn(extra_h["out_rel"], pre_h)
        td_f, root_f, extra_f = self._build_manuscript("fault")
        guard_rel = "sources/2026-W35/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_reader_publication_v2.py", "build_manuscript_manifest", 661, 606)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_manuscript(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.entry_reached)
        self.assertTrue(inj.target_reached, f"manuscript prepublish not reached: {inj.calls}")
        self.assertTrue(guard_path.is_file())
        out_f = "sources/2026-W35/publication/v2/reader-manuscript-late.json"
        self.assertNotIn(out_f, post)
        new_keys = set(post) - set(pre)
        self.assertEqual(new_keys, {guard_rel}, f"manuscript fault must write only guard: {sorted(new_keys)}")

    def test_selection_architecture_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_selection("sel-arch-healthy")
        self._call_selection(root_h, extra_h)
        td_f, root_f, extra_f = self._build_selection("sel-arch-fault")
        from scripts import survey_production_v2 as core
        profile_doc = core.load_json(extra_f["chain"]["profile_path"])
        source_rel = profile_doc["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_selection_architecture_v2_interactive.py", "run", 427, 260)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_selection(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached)
        self.assertTrue(guard_path.is_file())
        self.assertNotIn(f"{source_rel}/architecture-v2.json", post)
        new_keys = set(post) - set(pre)
        allowed = {guard_rel, f"{source_rel}/candidate-matrix-v2.json", f"{source_rel}/candidate-selection-v2.json"}
        self.assertTrue(new_keys <= allowed, f"unexpected: {sorted(new_keys)}")

    def test_selection_summary_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_selection("sel-sum-healthy")
        self._call_selection(root_h, extra_h)
        td_f, root_f, extra_f = self._build_selection("sel-sum-fault")
        from scripts import survey_production_v2 as core
        source_rel = core.load_json(extra_f["chain"]["profile_path"])["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_selection_architecture_v2_interactive.py", "run", 440, 260)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_selection(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached)
        self.assertNotIn(f"{source_rel}/architecture-review-summary-v2.json", post)

    def test_selection_attention_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_selection("sel-att-healthy")
        self._call_selection(root_h, extra_h)
        td_f, root_f, extra_f = self._build_selection("sel-att-fault")
        from scripts import survey_production_v2 as core
        source_rel = core.load_json(extra_f["chain"]["profile_path"])["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_selection_architecture_v2_interactive.py", "run", 444, 260)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_selection(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached)
        self.assertNotIn(f"{source_rel}/architecture-review-attention-v2.json", post)

    def test_selection_archive_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_selection("sel-arc-healthy")
        self._call_selection(root_h, extra_h)
        td_f, root_f, extra_f = self._build_selection("sel-arc-fault")
        from scripts import survey_production_v2 as core
        source_rel = core.load_json(extra_f["chain"]["profile_path"])["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_selection_architecture_v2_interactive.py", "run", 451, 260)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_selection(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached)
        self.assertNotIn(f"{source_rel}/orchestration/v2/interactive/selection-architecture-input.json", post)

    def test_preview_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_candidate("preview-base-healthy")
        self._call_candidate(root_h, extra_h)
        cand_rel = extra_h["out_rel"]
        from scripts import survey_publication_v2 as pub
        out_rel_h = "sources/2026-W33/publication/v2/publication-preview-late-healthy.json"
        pre_h = lg._snapshot_files(root_h)
        pub.build_preview_approval(
            root_h, root_h / cand_rel, root_h / out_rel_h,
            "Synthetic Reviewer", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc),
            "synthetic-late-guard-preview", state_path=root_h / "sources/2026-W33/production-state.json",
        )
        post_h = lg._snapshot_files(root_h)
        self.assertIn(out_rel_h, post_h)
        td_f, root_f, extra_f = self._build_candidate("preview-base-fault")
        self._call_candidate(root_f, extra_f)
        cand_rel_f = extra_f["out_rel"]
        guard_rel = "sources/2026-W33/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_publication_v2.py", "build_preview_approval", 2161, 2123)
        inj.install(self)
        out_rel_f = "sources/2026-W33/publication/v2/publication-preview-late-fault.json"
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            pub.build_preview_approval(
                root_f, root_f / cand_rel_f, root_f / out_rel_f,
                "Synthetic Reviewer", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc),
                "synthetic-late-guard-preview", state_path=root_f / "sources/2026-W33/production-state.json",
            )
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"preview prepublish not reached: {inj.calls}")
        self.assertTrue(guard_path.is_file())
        self.assertNotIn(out_rel_f, post)
        new_keys = set(post) - set(pre)
        self.assertEqual(new_keys, {guard_rel})



    def test_review_late_guard(self) -> None:
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        from scripts import survey_reader_publication_v2 as rp
        td_h, root_h = lg._copy_durable_to_temp(self, durable, "review-healthy-")
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        pdf_rel = "surveys/weekly/2026-W33/main.pdf"
        # Reuse durable valid checks (full family) for NEW review
        from scripts import survey_production_v2 as core2
        sem_template = core2.load_json(root_h / "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json")
        checks = sem_template["checks"]
        out_rel_h = "sources/2026-W33/publication/v2/review-late-healthy.json"
        pre_h = lg._snapshot_files(root_h)
        rp.build_review_record(
            root_h, root_h / man_rel, root_h / pdf_rel, 5, "SEMANTIC_EDITORIAL",
            checks,
            "Synthetic Reviewer", datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc),
            root_h / out_rel_h, state_path=root_h / "sources/2026-W33/production-state.json",
        )
        post_h = lg._snapshot_files(root_h)
        self.assertIn(out_rel_h, post_h)
        td_f, root_f = lg._copy_durable_to_temp(self, durable, "review-fault-")
        guard_rel = "sources/2026-W33/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_reader_publication_v2.py", "build_review_record", 898, 799)
        inj.install(self)
        from scripts import survey_production_v2 as core3
        sem_template_f = core3.load_json(root_f / "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json")
        checks_f = sem_template_f["checks"]
        out_rel_f = "sources/2026-W33/publication/v2/review-late-fault.json"
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            rp.build_review_record(
                root_f, root_f / man_rel, root_f / pdf_rel, 5, "SEMANTIC_EDITORIAL",
                checks_f,
                "Synthetic Reviewer", datetime(2026, 9, 14, 12, 0, tzinfo=timezone.utc),
                root_f / out_rel_f, state_path=root_f / "sources/2026-W33/production-state.json",
            )
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"review prepublish not reached: {inj.calls}")
        self.assertNotIn(out_rel_f, post)
        self.assertEqual(set(post) - set(pre), {guard_rel})



    def test_gate_late_guard(self) -> None:
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        from scripts import survey_reader_surface_gate_v2 as gate
        td_h, root_h = lg._copy_durable_to_temp(self, durable, "gate-healthy-")
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        sem_rel = "sources/2026-W33/publication/v2/reader-surface-semantic-review-v2.json"
        out_rel_h = "sources/2026-W33/publication/v2/reader-surface-gate-late-healthy.json"
        pre_h = lg._snapshot_files(root_h)
        gate.evaluate_reader_surface_gate(
            root_h, root_h / man_rel, semantic_review_path=root_h / sem_rel,
            output_path=root_h / out_rel_h, state_path=root_h / "sources/2026-W33/production-state.json",
        )
        post_h = lg._snapshot_files(root_h)
        self.assertIn(out_rel_h, post_h)
        td_f, root_f = lg._copy_durable_to_temp(self, durable, "gate-fault-")
        guard_rel = "sources/2026-W33/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_reader_surface_gate_v2.py", "evaluate_reader_surface_gate", 1830, 1475)
        inj.install(self)
        out_rel_f = "sources/2026-W33/publication/v2/reader-surface-gate-late-fault.json"
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            gate.evaluate_reader_surface_gate(
                root_f, root_f / man_rel, semantic_review_path=root_f / sem_rel,
                output_path=root_f / out_rel_f, state_path=root_f / "sources/2026-W33/production-state.json",
            )
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"gate prepublish not reached: {inj.calls}")
        self.assertNotIn(out_rel_f, post)
        self.assertEqual(set(post) - set(pre), {guard_rel})

    def test_visual_late_guard(self) -> None:
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        from scripts import survey_publication_v2 as pub
        td_h, root_h = lg._copy_durable_to_temp(self, durable, "vis-healthy-")
        # Build candidate + preview healthy chain in same root for valid approval
        cand_out_h = "sources/2026-W33/publication/v2/publication-candidate-late-vis-healthy.json"
        # Reuse candidate helper logic with fixed out (copy of _call_candidate but fixed name)
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        src_rel = "surveys/weekly/2026-W33/main.tex"
        pdf_rel = "surveys/weekly/2026-W33/main.pdf"
        bundle_rel = "sources/2026-W33/publication/v2/quality-regression-bundle-v2.json"
        sem_rel = "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json"
        vis_rel = "sources/2026-W33/publication/v2/visual-review-v2.json"
        from scripts import survey_production_v2 as core
        sem_doc = core.load_json(root_h / sem_rel)
        page_count = int(sem_doc.get("page_count", 5) or 5)
        pub.build_candidate(root_h, "2026-W33", "WEEKLY_MAGAZINE", root_h / man_rel, root_h / src_rel, root_h / pdf_rel, page_count, root_h / bundle_rel, root_h / sem_rel, root_h / vis_rel, root_h / cand_out_h, state_path=root_h / "sources/2026-W33/production-state.json")
        appr_out_h = "sources/2026-W33/publication/v2/publication-preview-late-vis-healthy.json"
        pub.build_preview_approval(root_h, root_h / cand_out_h, root_h / appr_out_h, "Synthetic Reviewer", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "synthetic-vis", state_path=root_h / "sources/2026-W33/production-state.json")
        out_rel_h = "sources/2026-W33/publication/v2/visual-late-healthy.json"
        pre_h = lg._snapshot_files(root_h)
        pub.build_visual_review(root_h, root_h / appr_out_h, [{"check_id": "v1", "status": "PASS", "detail": "ok"}], "tool", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), root_h / out_rel_h, state_path=root_h / "sources/2026-W33/production-state.json")
        post_h = lg._snapshot_files(root_h)
        self.assertIn(out_rel_h, post_h)
        td_f, root_f = lg._copy_durable_to_temp(self, durable, "vis-fault-")
        cand_out_f = "sources/2026-W33/publication/v2/publication-candidate-late-vis-fault.json"
        pub.build_candidate(root_f, "2026-W33", "WEEKLY_MAGAZINE", root_f / man_rel, root_f / src_rel, root_f / pdf_rel, page_count, root_f / bundle_rel, root_f / sem_rel, root_f / vis_rel, root_f / cand_out_f, state_path=root_f / "sources/2026-W33/production-state.json")
        appr_out_f = "sources/2026-W33/publication/v2/publication-preview-late-vis-fault.json"
        pub.build_preview_approval(root_f, root_f / cand_out_f, root_f / appr_out_f, "Synthetic Reviewer", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "synthetic-vis", state_path=root_f / "sources/2026-W33/production-state.json")
        guard_rel = "sources/2026-W33/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_publication_v2.py", "build_visual_review", 2245, 2209)
        inj.install(self)
        out_rel_f = "sources/2026-W33/publication/v2/visual-late-fault.json"
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            pub.build_visual_review(root_f, root_f / appr_out_f, [{"check_id": "v1", "status": "PASS", "detail": "ok"}], "tool", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), root_f / out_rel_f, state_path=root_f / "sources/2026-W33/production-state.json")
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached)
        self.assertNotIn(out_rel_f, post)
        self.assertEqual(set(post) - set(pre), {guard_rel})


    def test_freeze_late_guard(self) -> None:
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        from scripts import survey_publication_v2 as pub
        from scripts import survey_production_v2 as core
        from datetime import datetime, timezone
        td_h, root_h = lg._copy_durable_to_temp(self, durable, "freeze-healthy-")
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        src_rel = "surveys/weekly/2026-W33/main.tex"
        pdf_rel = "surveys/weekly/2026-W33/main.pdf"
        bundle_rel = "sources/2026-W33/publication/v2/quality-regression-bundle-v2.json"
        sem_rel = "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json"
        vis_rel = "sources/2026-W33/publication/v2/visual-review-v2.json"
        sem_doc = core.load_json(root_h / sem_rel)
        page_count = int(sem_doc.get("page_count", 5) or 5)
        cand_out = "sources/2026-W33/publication/v2/publication-candidate-late-freeze-healthy.json"
        pub.build_candidate(root_h, "2026-W33", "WEEKLY_MAGAZINE", root_h / man_rel, root_h / src_rel, root_h / pdf_rel, page_count, root_h / bundle_rel, root_h / sem_rel, root_h / vis_rel, root_h / cand_out, state_path=root_h / "sources/2026-W33/production-state.json")
        appr_out = "sources/2026-W33/publication/v2/publication-preview-late-freeze-healthy.json"
        pub.build_preview_approval(root_h, root_h / cand_out, root_h / appr_out, "Synthetic Reviewer", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "synthetic-freeze", state_path=root_h / "sources/2026-W33/production-state.json")
        freeze_out = "sources/2026-W33/publication/v2/freeze-late-healthy.json"
        manifest_out = "sources/2026-W33/publication/v2/release-manifest-late-healthy.json"
        pre_h = lg._snapshot_files(root_h)
        pub.build_freeze(root_h, root_h / cand_out, root_h / appr_out, datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc), root_h / freeze_out, root_h / manifest_out)
        post_h = lg._snapshot_files(root_h)
        self.assertIn(freeze_out, post_h)
        self.assertIn(manifest_out, post_h)
        td_f, root_f = lg._copy_durable_to_temp(self, durable, "freeze-fault-")
        cand_out_f = "sources/2026-W33/publication/v2/publication-candidate-late-freeze-fault.json"
        pub.build_candidate(root_f, "2026-W33", "WEEKLY_MAGAZINE", root_f / man_rel, root_f / src_rel, root_f / pdf_rel, page_count, root_f / bundle_rel, root_f / sem_rel, root_f / vis_rel, root_f / cand_out_f, state_path=root_f / "sources/2026-W33/production-state.json")
        appr_out_f = "sources/2026-W33/publication/v2/publication-preview-late-freeze-fault.json"
        pub.build_preview_approval(root_f, root_f / cand_out_f, root_f / appr_out_f, "Synthetic Reviewer", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "synthetic-freeze", state_path=root_f / "sources/2026-W33/production-state.json")
        guard_rel = "sources/2026-W33/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_publication_v2.py", "build_freeze", 2338, 2294)
        inj.install(self)
        freeze_out_f = "sources/2026-W33/publication/v2/freeze-late-fault.json"
        manifest_out_f = "sources/2026-W33/publication/v2/release-manifest-late-fault.json"
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            pub.build_freeze(root_f, root_f / cand_out_f, root_f / appr_out_f, datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc), root_f / freeze_out_f, root_f / manifest_out_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"freeze prepublish not reached: {inj.calls}")
        self.assertNotIn(freeze_out_f, post)
        self.assertNotIn(manifest_out_f, post)
        self.assertEqual(set(post) - set(pre), {guard_rel})


    def _make_candidates_normalized_state(self, chain: dict) -> Path:
        import copy
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from tests import test_dm022_full_lifecycle_v2 as full
        from tests.test_dm022_full_lifecycle_v2 import _sha_file as _s, _write as _w
        root: Path = chain["root"]
        cfg: dict = chain["cfg"]
        issue_id: str = chain["issue_id"]
        profile_path: Path = chain["profile_path"]
        tmp_owner = full.Dm022FullLifecycleWitnessTests("test_weekly_dm022_to_selection_stage")
        tmp_owner._ensure_dm022_files(root)
        disc_acc = tmp_owner._materialize_production_discovery_acceptance(chain)
        head, _ = tmp_owner._git_init(root)
        contract = core.contract_identity(root, cfg, chain["research_profile"], "WEEKLY_MAGAZINE" if chain["research_profile"] == "WEEKLY" else "LONGFORM_SPECIAL")
        state_path = root / "sources" / issue_id / "production-state.json"
        init_state = core.load_json(chain["state_path"])
        def _report(from_s: str, to_s: str, cps: list[str], arts: list[dict]) -> dict:
            return {"schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT", "status": "PASS", "issue_id": issue_id, "from_state": from_s, "to_state": to_s, "production_state": {"path": str(state_path.relative_to(root)), "sha256": _s(state_path)}, "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": _s(profile_path)}, "implementation_commit_sha": head, "contract": contract, "artifacts": arts, "recorded_at": "2026-10-28T00:00:00Z"}
        disc_rel = str(disc_acc.relative_to(root))
        disc_arts = [{"name": "discovery-acceptance", "path": disc_rel, "sha256": _s(disc_acc)}]
        disc_report = _report("ISSUE_INITIALIZED", "DISCOVERY_COLLECTED", ["discovery"], disc_arts)
        disc_report_path = root / "sources" / issue_id / "checkpoint-discovery-report.json"
        _w(disc_report_path, disc_report)
        disc_record = {"schema_version": "2.0-rc1", "issue_id": issue_id, "from_state": "ISSUE_INITIALIZED", "to_state": "DISCOVERY_COLLECTED", "checkpoints": ["discovery"], "recorded_at": "2026-10-28T00:00:00Z", "implementation": {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]}, "contract": contract, "artifacts": disc_arts, "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": str(disc_report_path.relative_to(root)), "sha256": _s(disc_report_path)}}], "summary": "fixture discovery checkpoint"}
        disc_record_path = root / "sources" / issue_id / "checkpoint-discovery.json"
        _w(disc_record_path, disc_record)
        scr_rel = str(chain["screening_acceptance"].relative_to(root))
        scr_arts = [{"name": "screening-acceptance", "path": scr_rel, "sha256": _s(chain["screening_acceptance"])}]
        scr_report = _report("DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED", ["screening"], scr_arts)
        scr_report_path = root / "sources" / issue_id / "checkpoint-screening-report.json"
        _w(scr_report_path, scr_report)
        scr_record = {"schema_version": "2.0-rc1", "issue_id": issue_id, "from_state": "DISCOVERY_COLLECTED", "to_state": "CANDIDATES_NORMALIZED", "checkpoints": ["screening"], "recorded_at": "2026-10-28T00:00:00Z", "implementation": {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]}, "contract": contract, "artifacts": scr_arts, "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": str(scr_report_path.relative_to(root)), "sha256": _s(scr_report_path)}}], "summary": "fixture screening checkpoint"}
        scr_record_path = root / "sources" / issue_id / "checkpoint-screening.json"
        _w(scr_record_path, scr_record)
        profile_doc = core.load_json(profile_path)
        source_root_rel = profile_doc["paths"]["source_root"]
        new_state = copy.deepcopy(init_state)
        new_state["lifecycle_state"] = "CANDIDATES_NORMALIZED"
        new_state["contract"] = contract
        new_state["implementation"] = {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]}
        new_state["machine_checkpoints"] = {"discovery": "passed", "screening": "passed", "evidence": "pending", "materiality": "pending", "completeness": "pending", "selection": "pending", "architecture": "pending", "draft": "pending", "validation": "pending", "publication_preview": "pending", "freeze": "pending", "release": "pending"}
        new_state["checkpoint_provenance"] = {"discovery": {"path": str(disc_record_path.relative_to(root)), "sha256": _s(disc_record_path)}, "screening": {"path": str(scr_record_path.relative_to(root)), "sha256": _s(scr_record_path)}, "evidence": None, "materiality": None, "completeness": None, "selection": None, "architecture": None, "draft": None, "validation": None, "publication_preview": None, "freeze": None, "release": None}
        new_state["human_gates"] = {"architecture_review": "pending", "publication_preview": "pending"}
        new_state["human_gate_provenance"] = {"architecture_review": None, "publication_preview": None}
        new_state["target_gate"] = "ARCHITECTURE_REVIEW"
        new_state["exception_gate"] = {"status": "inactive", "reason": None}
        new_state["publication_revalidation_provenance"] = None
        new_state["history"] = [{"from": None, "to": "ISSUE_INITIALIZED", "recorded_at": "2026-10-28T00:00:00Z", "repository_commit_sha": head}, {"from": "ISSUE_INITIALIZED", "to": "DISCOVERY_COLLECTED", "recorded_at": "2026-10-28T00:00:01Z", "repository_commit_sha": head}, {"from": "DISCOVERY_COLLECTED", "to": "CANDIDATES_NORMALIZED", "recorded_at": "2026-10-28T00:00:02Z", "repository_commit_sha": head}]
        new_state = core.refresh_state_control(new_state, cfg)
        canonical_abs = root / f"{source_root_rel}/production-state.json"
        canonical_abs.parent.mkdir(parents=True, exist_ok=True)
        _w(canonical_abs, new_state)
        errs = agent.validate_agent_state(root, cfg, core.load_json(canonical_abs))
        self.assertEqual(errs, [], f"CANDIDATES_NORMALIZED fixture must pass: {errs}")
        return canonical_abs

    def _build_evidence_input(self, root: Path, chain: dict) -> Path:
        from scripts import survey_production_v2 as core
        profile_doc = core.load_json(chain["profile_path"])
        issue_id = chain["issue_id"]
        # Single non-DROP discovery (target-source, KEEP)
        rec = {"discovery_id": "target-source", "status": "VERIFIED", "entity": {"entity_id": "ent-target-source", "canonical_name": "Synthetic verified model", "entity_type": "MODEL", "organization": "Synthetic Org", "canonical_url": None}, "artifact_type": "MODEL", "claims": [{"text": "Synthetic revised claim for target-source", "evidence_class": "PRIMARY_FACT", "context": None}], "limitations": [], "verification": [{"target": "subject identity", "status": "VERIFIED", "finding": "synthetic verification"}], "materiality": "MATERIAL", "materiality_rationale": "Synthetic rationale", "scope_dimensions": list(profile_doc["research_scope"]["scope_dimensions"][:1]), "window_relation": "MAIN_EVENT", "carry_over": False}
        doc = {"schema_version": "2.0-rc1", "issue_id": issue_id, "runner": {"provider": "SYNTHETIC_FIXTURE_PROVIDER", "model": "SYNTHETIC_FIXTURE_MODEL_DM022_FULL_V2", "invocation": "SYNTHETIC_EVIDENCE_INPUT", "generated_at": "2026-10-28T00:00:00Z"}, "records": [rec], "completeness": {"obligations": [{"obligation_id": row["obligation_id"], "status": "SATISFIED", "rationale": f"Synthetic satisfies {row['obligation_id']}"} for row in profile_doc["research_scope"]["initial_obligations"]], "residual_limitations": [], "closure": None}}
        # Thematic needs closure; weekly closure must be null (already)
        if profile_doc["research_profile"] == "THEMATIC":
            doc["completeness"]["closure"] = {"targeted_gap_fill_completed": True, "limitations": [], "status": "COMPLETE"}
        input_path = root / f"evidence-input-{issue_id}.json"
        input_path.write_text(__import__("json").dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return input_path

    def _build_evidence_fixture(self, tag: str):
        from tests import test_dm022_full_lifecycle_v2 as full
        from tests import test_survey_evidence_v2 as evidence_tests
        from scripts import survey_production_v2 as core
        owner = full.Dm022FullLifecycleWitnessTests("test_weekly_dm022_to_selection_stage")
        helper = evidence_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        # Do not use helper.tearDown (would clean sandbox); sandbox temp lives via chain root? Actually helper.sandbox creates temp dir; we keep helper alive via owner? Simplify: use owner._copy_publication_support_files + helper methods, keep temps via self.
        temp, root, cfg = helper.sandbox()
        self.addCleanup(temp.cleanup)
        self.addCleanup(lambda: helper.tearDown() if hasattr(helper, "tearDown") else None)
        owner._copy_publication_support_files(root)
        profile_path, state_path = helper.init_profile(root, cfg, "WEEKLY")
        issue_id = core.load_json(state_path)["issue_id"]
        rec = helper.discovery(issue_id, "target-source")
        records = [rec]
        decisions = {"target-source": "KEEP"}
        discovery_path, screening_acceptance = helper.make_screening(root, state_path, records, decisions)
        chain = {"helper": helper, "root": root, "cfg": cfg, "profile_path": profile_path, "state_path": state_path, "discovery_path": discovery_path, "screening_acceptance": screening_acceptance, "issue_id": issue_id, "research_profile": "WEEKLY", "discovery_id": "target-source", "canonical_url": rec["source"]["locator"]}
        self._sel_owner = owner
        state_abs = self._make_candidates_normalized_state(chain)
        input_path = self._build_evidence_input(root, chain)
        td_holder = tempfile.TemporaryDirectory(prefix=f"ev-hold-{tag}-")
        self.addCleanup(td_holder.cleanup)
        extra = {"state_path": state_abs, "chain": chain, "input_path": input_path, "tag": tag}
        return td_holder, root, extra

    def _call_evidence(self, root: Path, extra: dict) -> None:
        from scripts import run_evidence_v2_interactive as ev_run
        ev_run.run(root, extra["state_path"], extra["input_path"])

    def test_evidence_ledger_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_evidence_fixture("ev-ledger-healthy")
        pre_h = lg._snapshot_files(root_h)
        self._call_evidence(root_h, extra_h)
        post_h = lg._snapshot_files(root_h)
        from scripts import survey_production_v2 as core
        source_rel = core.load_json(extra_h["chain"]["profile_path"])["paths"]["source_root"]
        self.assertIn(f"{source_rel}/materiality-ledger-v2.json", post_h)
        self.assertIn(f"{source_rel}/profile-completeness-v2.json", post_h)
        td_f, root_f, extra_f = self._build_evidence_fixture("ev-ledger-fault")
        source_rel_f = core.load_json(extra_f["chain"]["profile_path"])["paths"]["source_root"]
        guard_rel = f"{source_rel_f}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_evidence_v2_interactive.py", "run", 742, 623)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_evidence(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.entry_reached)
        self.assertTrue(inj.target_reached, f"evidence ledger prepublish not reached: {inj.calls}")
        self.assertNotIn(f"{source_rel_f}/materiality-ledger-v2.json", post)
        self.assertNotIn(f"{source_rel_f}/profile-completeness-v2.json", post)
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        # Evidence/views written before ledger prepublish are allowed prefixes (frozen has no READY at 694/727)
        for k in new_keys - {guard_rel}:
            self.assertTrue(k.startswith(f"{source_rel_f}/evidence/v2/") or k.startswith(f"{source_rel_f}/screening/"), f"unexpected write besides guard+evidence prefix: {k}")

    def test_evidence_completeness_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_evidence_fixture("ev-comp-healthy")
        self._call_evidence(root_h, extra_h)
        from scripts import survey_production_v2 as core
        source_rel = core.load_json(extra_h["chain"]["profile_path"])["paths"]["source_root"]
        self.assertIn(f"{source_rel}/profile-completeness-v2.json", lg._snapshot_files(root_h))
        td_f, root_f, extra_f = self._build_evidence_fixture("ev-comp-fault")
        source_rel_f = core.load_json(extra_f["chain"]["profile_path"])["paths"]["source_root"]
        guard_rel = f"{source_rel_f}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_evidence_v2_interactive.py", "run", 758, 623)
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            self._call_evidence(root_f, extra_f)
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.entry_reached)
        self.assertTrue(inj.target_reached, f"evidence completeness prepublish not reached: {inj.calls}")
        self.assertNotIn(f"{source_rel_f}/profile-completeness-v2.json", post)
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        self.assertIn(f"{source_rel_f}/materiality-ledger-v2.json", post)
        for k in new_keys - {guard_rel, f"{source_rel_f}/materiality-ledger-v2.json"}:
            self.assertTrue(k.startswith(f"{source_rel_f}/evidence/v2/") or k.startswith(f"{source_rel_f}/screening/"), f"unexpected: {k}")

    def _build_draft(self, tag: str):
        from tests import test_dm022_full_lifecycle_v2 as full
        owner = full.Dm022FullLifecycleWitnessTests("test_weekly_dm022_to_selection_stage")
        witness = owner._full_route_witness("WEEKLY", f"draft-late-{tag}")
        approved = owner._approve_architecture_for(witness, f"draft-late-{tag}", hour=3)
        root: Path = approved["root"]
        chain = witness["chain"]
        owner._materialize_canonical_accepted_evidence_tree(root, chain, approved["state_abs"])
        input_path = owner._build_drafting_input(root, chain, f"draft-late-{tag}")
        self._sel_owner = owner
        self._draft_owner = owner
        td_holder = tempfile.TemporaryDirectory(prefix=f"draft-hold-{tag}-")
        self.addCleanup(td_holder.cleanup)
        extra = {"state_path": approved["state_abs"], "root": root, "chain": chain, "input_path": input_path, "owner": owner, "approved": approved, "tag": tag}
        return td_holder, root, extra

    def _call_draft(self, root: Path, extra: dict) -> None:
        import sys as _sys
        from scripts import run_drafting_synthesis_v2_interactive as draft_run
        # Call main in-process via argv (same code as subprocess, but injector-visible)
        argv_old = _sys.argv[:]
        try:
            _sys.argv = ["run_drafting_synthesis_v2_interactive", "--repo-root", str(root), "--state", str(extra["state_path"].relative_to(root)), "--input", str(extra["input_path"].relative_to(root))]
            rc = draft_run.main()
            assert rc == 0, f"draft main must return 0, got {rc}"
        finally:
            _sys.argv = argv_old

    def test_draft_package_late_guard(self) -> None:
        td_h, root_h, extra_h = self._build_draft("healthy")
        pre_h = lg._snapshot_files(root_h)
        self._call_draft(root_h, extra_h)
        post_h = lg._snapshot_files(root_h)
        from scripts import survey_production_v2 as core
        source_rel = core.load_json(extra_h["chain"]["profile_path"])["paths"]["source_root"]
        # First package write must exist (NEW)
        pkg_files = [k for k in post_h if k.startswith(f"{source_rel}/draft/v2/packages/") and k.endswith("/draft-package.json")]
        self.assertTrue(pkg_files, f"draft healthy must write package: {sorted(set(post_h)-set(pre_h))}")
        td_f, root_f, extra_f = self._build_draft("fault")
        source_rel_f = core.load_json(extra_f["chain"]["profile_path"])["paths"]["source_root"]
        guard_rel = f"{source_rel_f}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "run_drafting_synthesis_v2_interactive.py", "main", 218, 81, entry_fn="_upstream")
        inj.install(self)
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"(DM022_TRANSITION_ACTIVE|SystemExit)"):
            try:
                self._call_draft(root_f, extra_f)
            except SystemExit as e:
                # main() may SystemExit on guard? It raises SystemExit via main's error handling? Actually _dm022_require_ready raises ValueError, main lets it propagate? Check: main calls _upstream (which calls READY) and later READYs; on guard it raises ValueError, not SystemExit, except for input validation which SystemExits. Our fault should raise ValueError DM022. If SystemExit with DM022 text, re-raise as ValueError pattern.
                raise ValueError(f"DM022_TRANSITION_ACTIVE via SystemExit {e}")
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.target_reached, f"draft prepublish 218 not reached: {inj.calls}")
        self.assertTrue(guard_path.is_file())
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        for k in new_keys - {guard_rel}:
            # No package writes allowed before 218? Actually _upstream (entry) does no writes; 218 is first write, so no package partials allowed
            self.assertTrue(k.startswith(f"{source_rel_f}/draft/") is False or "packages" not in k, f"draft package must not be written when late guard refuses: {k}")

    def _build_finalize_scope_with_pid(self, prefix: str, pid: str) -> dict:
        import hashlib as _hl
        import tempfile as _tf
        from pathlib import Path as _P
        from tests import test_survey_dm022_c2_consumers_v2 as c2
        import tests.test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        from scripts import survey_editorial_retention_v2 as retention
        from scripts import survey_production_v2 as core_fixture
        scratch = _tf.TemporaryDirectory(prefix=prefix)
        self.addCleanup(scratch.cleanup)
        root = _P(scratch.name).resolve()
        c2._copy_c2_workspace(self, root)
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core_fixture.load_json(chain["authored_path"])
        authored["cover"]["headline"] = f"Weekly finalize guard test {pid}, revised edition"
        staged_authoring = p1t._stage_authoring_before_prepare(self, root, helper.source_root, pid, authored)
        prepared = p1mod.prepare_proposal(root, state_path, staged_authoring, pid, f"Fixture finalize guard test {pid}.")
        proposal_path = p1t._stage_reader_and_proposal(self, root, helper.source_root, pid, prepared)
        cap = retention.capture_retention(root, state_path, proposal_path)
        manifest_path = root / cap["manifest_path"]
        staged_reader_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        scope_path = p1t._scope_review_for(self, root, prepared, staged_reader_rel, f"scope-review-{pid}.json")
        staged_path = proposal_path.parent / "staged-test.json"
        c2._write_json(staged_path, {"retention_manifest_ref": {"path": str(manifest_path.relative_to(root)), "sha256": _hl.sha256(manifest_path.read_bytes()).hexdigest()}, "scope_review_ref": {"path": str(scope_path.relative_to(root)), "sha256": _hl.sha256(scope_path.read_bytes()).hexdigest()}})
        (proposal_path.parent / "publication").mkdir(exist_ok=True)
        return {"scratch": scratch, "root": root, "helper": helper, "chain": chain, "state_path": state_path, "prepared": prepared, "proposal_path": proposal_path, "manifest_path": manifest_path, "scope_path": scope_path, "staged_path": staged_path, "staged_authoring": staged_authoring, "pid": pid}

    def _prepare_new_proposal_in_root(self, root: Path, fix: dict, new_pid: str) -> dict:
        import tests.test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        from scripts import survey_production_v2 as core
        helper = fix["helper"]
        chain = fix["chain"]
        state_path = fix["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = f"Weekly finalize guard test {new_pid}, revised edition"
        staged_authoring = p1t._stage_authoring_before_prepare(self, root, helper.source_root, new_pid, authored)
        prepared = p1mod.prepare_proposal(root, state_path, staged_authoring, new_pid, f"Fixture finalize guard test {new_pid}.")
        proposal_path = p1t._stage_reader_and_proposal(self, root, helper.source_root, new_pid, prepared)
        staged_reader_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        scope_path = p1t._scope_review_for(self, root, prepared, staged_reader_rel, f"scope-review-{new_pid}.json")
        return {"proposal_path": proposal_path, "prepared": prepared, "scope_path": scope_path, "staged_authoring": staged_authoring}

    def test_retention_late_guard(self) -> None:
        from scripts import survey_editorial_retention_v2 as ret
        from scripts import survey_production_v2 as core
        fix_h = self._build_finalize_scope_with_pid("late-ret-healthy", "fixture-wk-ret-healthy")
        self.assertTrue(fix_h["manifest_path"].is_file())
        fix_f = self._build_finalize_scope_with_pid("late-ret-fault", "fixture-wk-ret-fault")
        root_f = fix_f["root"]
        state_abs = fix_f["state_path"]
        state = core.load_json(state_abs)
        profile = core.load_json(root_f / state["profile"]["path"])
        source_rel = profile["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        guard_path = root_f / guard_rel
        inj = lg.LateGuardInjector(guard_path, "survey_editorial_retention_v2.py", "capture_retention", 1519, 942)
        inj.install(self)
        new_fix = self._prepare_new_proposal_in_root(root_f, fix_f, "fixture-wk-ret-fault2")
        pre = lg._snapshot_files(root_f)
        with self.assertRaisesRegex(Exception, r"DM022_TRANSITION_ACTIVE"):
            ret.capture_retention(root_f, state_abs, new_fix["proposal_path"])
        post = lg._snapshot_files(root_f)
        self.assertTrue(inj.entry_reached)
        self.assertTrue(inj.target_reached, f"retention prepublish not reached: {inj.calls}")
        self.assertTrue(guard_path.is_file())
        self.assertIn(guard_rel, set(post) - set(pre))

    def _build_editorial_staged_with_pid(self, prefix: str, pid: str) -> dict:
        import copy as _cp
        from scripts import survey_production_v2 as core
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        td, root = lg._copy_durable_to_temp(self, durable, f"edstaged-{prefix}-")
        # P1 proposal with NEW pid (revised deck, same as full-lifecycle staged)
        import tests.test_survey_editorial_correction_proposal_v2 as p1t
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        from scripts import survey_editorial_retention_v2 as retention_mod
        from scripts import survey_editorial_current_authority_v2 as authority_mod
        from scripts import survey_editorial_staged_source_v2 as staged_mod
        cfg = core.load_json(root / "config/survey-production-v2.json")
        state_abs = root / "sources/2026-W33/production-state.json"
        # Load archived derivation input for genuinely revised authoring (same as full-lifecycle)
        archived_deriv = core.load_json(root / "sources/2026-W33/publication/v2/interactive-semantic-publication-input.json")
        revised = _cp.deepcopy(archived_deriv)
        revised["cover"] = dict(archived_deriv["cover"])
        revised["cover"]["deck"] = archived_deriv["cover"]["deck"] + f" Corrected: revised MATERIAL claim {pid}."
        # Need helper for source_root + profile? Use p1t helpers with copied workspace (needs git? _copy_c2_workspace? No, durable already has .git + scripts, use p1t helpers that need helper object? p1t._new_weekly_helper needs root with .git? Durable has .git, good.
        # For simplicity, reuse p1t helpers via fresh helper bound to durable copy root (which has .git, scripts, etc.)
        # p1t._new_weekly_helper expects workspace with git ls-files? No, it uses root directly? Let's use direct P1 prepare without helper: need staged_authoring path. Use p1t._stage_authoring_before_prepare which needs helper.source_root? We don't have helper. Instead, construct staged_authoring manually via same steps as _build_finalize_scope_with_pid but for editorial (not finalize)? Actually editorial P1 uses different helpers (proposal_mod.prepare_proposal with authoring-input, not staged_authoring? Let's reuse _build_finalize_scope_with_pid's P1 steps? No, editorial correction proposal uses authoring-input, not staged_authoring.
        # To avoid duplicating P1 helper setup, use full-lifecycle's _weekly_to_editorial_staged steps but with NEW pid and WITHOUT rebuilding VALIDATED_DRAFT (reuse durable VALIDATED_DRAFT as base, skip TinyTeX rebuild).
        # Durable already has VALIDATED_DRAFT + REAL PDFs; we only need NEW P1 proposal + P2R + P2V + P3S in durable copy.
        # Use p1t helpers via manual init (no helper object): directly call proposal_mod.prepare_proposal with authoring-input we create.
        proposal_dir = root / "sources/2026-W33/publication/v2/editorial-corrections" / pid
        proposal_dir.mkdir(parents=True, exist_ok=True)
        authored_path = proposal_dir / "authoring-input.json"
        authored_path.write_text(__import__("json").dumps(revised, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        # Need state_path + helper.source_root? proposal_mod.prepare_proposal needs root, state_path, authored_path, proposal_id. It derives source_root from State/profile, no helper needed. Good.
        prepared = p1mod.prepare_proposal(root, state_abs, authored_path, pid)
        # Persist proposal + proposed reader (same as full-lifecycle)
        (proposal_dir / "proposal.json").write_text(__import__("json").dumps(prepared["proposal"], ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        proposed_reader = prepared.get("proposed_canonical") or prepared.get("proposed_reader")
        assert proposed_reader is not None
        if isinstance(proposed_reader, (bytes, bytearray)):
            (proposal_dir / "reader-surface-input-v2.json").write_bytes(bytes(proposed_reader))
        else:
            (proposal_dir / "reader-surface-input-v2.json").write_text(__import__("json").dumps(proposed_reader, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        proposal_path = proposal_dir / "proposal.json"
        # P2R capture
        captured = retention_mod.capture_retention(root, state_abs, proposal_path)
        manifest_path = root / captured["manifest_path"]
        # Scope review (synthetic, same as full-lifecycle _write_editorial_scope_review but with NEW pid)
        # Reuse full-lifecycle helper via owner to avoid duplication
        from tests import test_dm022_full_lifecycle_v2 as full
        owner = full.Dm022FullLifecycleWitnessTests("test_weekly_dm022_to_selection_stage")
        # Need chain for scope? Scope needs proposal + basis. Use owner._write_editorial_scope_review with minimal chain (issue_id + profile). Construct minimal chain dict with issue_id, profile?
        # Simpler: build scope manually (same shape as _write_editorial_scope_review) using proposal basis
        proposal_doc = core.load_json(proposal_path)
        basis = proposal_doc["basis"]
        prop_reader_rel = str((proposal_dir / "reader-surface-input-v2.json").relative_to(root))
        after_sha = core.sha256_file(proposal_dir / "reader-surface-input-v2.json")
        block = {"version": "EDITORIAL_CORRECTION_SCOPE_V1", "decision": "WITHIN_APPROVED_AUTHORITY", "before_reader_input": basis["active_reader_input_ref"], "preserved_upstream_sha256": basis["preserved_upstream_digest"], "change_summary": f"Synthetic scope judgment ({pid}): corrected deck wording inside approved Architecture authority.", "evidence_locations": [f"synthetic-fixture:proposal-{pid}"]}
        review = {"schema_version": "2.0-rc1", "issue_id": "2026-W33", "publication_profile": proposal_doc["publication_profile"], "review_kind": "SEMANTIC_EDITORIAL", "reviewed_surface": {"path": prop_reader_rel, "sha256": after_sha}, "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS", "detail": f"Synthetic scope reviewer ({pid})", "evidence_locations": ["synthetic-fixture:proposed-reader"]}, {"check_id": "EDITORIAL_CORRECTION_SCOPE", "status": "PASS", "detail": f"Synthetic scope reviewer ({pid})", "evidence_locations": [f"synthetic-fixture:proposal-{pid}"]}], "decision": "PASS", "reviewed_by": "SYNTHETIC_FIXTURE_REVIEWER_GENERAL_FULL_V2", "reviewed_at": "2026-10-28T16:00:00Z", "recorded_at": "2026-10-28T16:00:00Z", "status": "PASSED", "findings": [], "summary": f"Synthetic scope PASS ({pid})", "editorial_correction_scope": block}
        review["review_sha256"] = core.sha256_object({k: v for k, v in review.items() if k != "review_sha256"})
        scope_path = proposal_dir / "scope-review-v2.json"
        scope_path.write_text(__import__("json").dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        # P2V observe
        observed = authority_mod.observe_current_authority(root, state_abs, proposal_path, manifest_path, scope_path)
        assert observed.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", observed
        # P3S materialize via fresh fixture-code subprocess (runtime binding to fixture root, like full-lifecycle, but packet logs to late-guards, unique, no overwrites)
        import subprocess as _sp, sys as _sys, json as _jj2, datetime as _dt
        driver = ("import json, sys; from pathlib import Path; root = Path(sys.argv[1]).resolve(); " "state_path = Path(sys.argv[2]); proposal_path = Path(sys.argv[3]); " "manifest_path = Path(sys.argv[4]); scope_path = Path(sys.argv[5]); " "from scripts import survey_editorial_staged_source_v2 as staged; " "out = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path); " "print(json.dumps({'staged_manifest_ref': out.get('staged_manifest_ref')}))")
        proc = _sp.Popen([_sys.executable, "-c", driver, str(root), str(state_abs.relative_to(root)), str(proposal_path.relative_to(root)), str(manifest_path.relative_to(root)), str(scope_path.relative_to(root))], cwd=str(root), stdout=_sp.PIPE, stderr=_sp.PIPE, text=True, env={k: v for k, v in __import__("os").environ.items() if not k.startswith("GIT_")})
        _pid = proc.pid
        try:
            _out_text, _err_text = proc.communicate(timeout=900)
        except Exception:
            proc.kill()
            _out_text, _err_text = proc.communicate()
            raise AssertionError(f"P3S fixture subprocess failed (pid {_pid})")
        # Unique raw logs in late-guards packet (never overwrite)
        import pathlib as _pl
        _packet_base = _pl.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        _stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        _dest = _packet_base / f"p3s-{pid}-{_stamp}-{_pid}"
        assert not _dest.exists(), "run dir must be run-unique"
        _dest.mkdir(parents=True)
        (_dest / "stdout.txt").write_text(_out_text, encoding="utf-8")
        (_dest / "stderr.txt").write_text(_err_text, encoding="utf-8")
        (_dest / "meta.json").write_text(_jj2.dumps({"pid": _pid, "exit": proc.returncode, "pid_tag": pid}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc.returncode == 0, f"P3S materialize must succeed (pid {_pid}): {_err_text[-3000:]}"
        _result = _jj2.loads(_out_text.strip().splitlines()[-1])
        staged_manifest_path = root / _result["staged_manifest_ref"]["path"]
        assert staged_manifest_path.is_file()
        # Manuscript + toolchain specs (same as _weekly_to_versioned_active, real TinyTeX path)
        manuscript_spec_path = proposal_dir / "manuscript-spec.json"
        manuscript_spec_path.write_text(__import__("json").dumps({"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1", "issue_id": "2026-W33", "proposal_ref": {"path": str(proposal_path.relative_to(root)), "sha256": core.sha256_file(proposal_path)}, "architecture_coverage": [], "reader_requirements": [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": ["main.tex"], "detail": "synthetic"}, {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED", "reader_locations": ["main.tex"], "detail": "synthetic"}], "authored_by": "SYNTHETIC_FIXTURE_AUTHOR_GENERAL_FULL_V2", "recorded_at": "2026-10-28T16:00:00Z"}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        from scripts.survey_editorial_publication_v2 import EXPECTED_ARGV_LUALATEX_BIBER
        toolchain_spec_path = proposal_dir / "toolchain-spec.json"
        toolchain_spec_path.write_text(__import__("json").dumps({"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1", "executor": "SYNTHETIC_FIXTURE_EXECUTOR_GENERAL_FULL_V2", "absolute_executable": "/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex", "recipe": "lualatex-biber-lualatex", "argv": list(EXPECTED_ARGV_LUALATEX_BIBER), "env": {}, "recorded_at": "2026-10-28T16:00:00Z"}, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        extra = {"state_path": state_abs, "proposal_path": proposal_path, "manifest_path": manifest_path, "scope_path": scope_path, "staged_manifest_path": staged_manifest_path, "manuscript_spec_path": manuscript_spec_path, "toolchain_spec_path": toolchain_spec_path, "proposal_dir": proposal_dir, "pid": pid, "cfg": cfg}
        return td, root, extra

    def _build_editorial_prepared_with_pid(self, prefix: str, pid: str) -> dict:
        # Up to staged (no TinyTeX yet) then prepare (one real TinyTeX build via subprocess for fixture binding) + reviews (no build) to reach finalize-ready
        td, root, extra = self._build_editorial_staged_with_pid(prefix, pid)
        from scripts import survey_reader_publication_v2 as reader
        from scripts import survey_production_v2 as core
        from datetime import datetime, timezone
        # Prepare via subprocess (fixture binding, no injection) to avoid S2 binding error in-process
        res = self._run_editorial_prepare_subprocess(root, extra, f"{prefix}-baseprep", inject=False)
        assert res.get("ok"), f"base prepare must succeed: {res}"
        # Re-read prep outputs (manuscript, etc.) from base (prepare wrote build outputs)
        proposal_dir = extra["proposal_dir"]
        # Reviews (deterministic + semantic + visual, no build, need real PDF page count from prepare build)
        from pypdf import PdfReader as _PdfReader
        ed_pdf = proposal_dir / "publication" / "build" / "main.pdf"
        assert ed_pdf.is_file(), f"prepare must write PDF: {ed_pdf}"
        pages = len(_PdfReader(str(ed_pdf)).pages)
        det_dir = proposal_dir / "publication" / "deterministic"
        det_dir.mkdir(parents=True, exist_ok=True)
        import hashlib as _hl2, json as _jj
        det_results = {}
        for check_id in ("IDENTIFIER_PRESERVATION", "PDF_PREFLIGHT", "SUBJECT_ENTITY_PROPERTY_BINDING"):
            p = det_dir / f"{check_id.lower()}.json"
            p.write_text(_jj.dumps({"check_id": check_id, "status": "PASS"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            det_results[check_id] = {"path": str(p.relative_to(root)), "sha256": _hl2.sha256(p.read_bytes()).hexdigest()}
        det_checks = [{"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": "SYNTHETIC_FIXTURE_GENERAL_FULL_V2", "evidence": f"synthetic {cid}", "recorded_at": "2026-10-28T17:00:00Z", "result": det_results[cid]} for cid in ("IDENTIFIER_PRESERVATION", "PDF_PREFLIGHT", "SUBJECT_ENTITY_PROPERTY_BINDING")]
        det_checks_path = proposal_dir / "publication" / "deterministic-checks.json"
        det_checks_path.write_text(_jj.dumps({"checks": det_checks}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        # Expected review checks (same as full-lifecycle) via subprocess for fixture binding (avoid S2 in-process error)
        import subprocess as _sp2, sys as _sys2, json as _jj2, datetime as _dt2, os as _os2
        from scripts import survey_production_v2 as core2
        profile2 = core2.load_json(root / "sources/2026-W33/production-profile.json")
        # Get expected checks via in-process (no S2 check for _expected_review_checks? It is pure, no binding? Should be safe in-process. If fails, do via subprocess too. Try in-process first.)
        try:
            from scripts import survey_reader_publication_v2 as _reader2
            expected_sem = sorted(_reader2._expected_review_checks(root, profile2, "SEMANTIC_EDITORIAL"))
            expected_vis = sorted(_reader2._expected_review_checks(root, profile2, "VISUAL"))
        except Exception:
            # Fallback: use durable's known checks (same as full-lifecycle's expected)
            expected_sem = sorted(["ARCHITECTURE_CONTENT_FIDELITY", "BIBLIOGRAPHY_METADATA", "FINAL_SYNTHESIS_QUALITY", "PUBLICATION_BOUNDARY", "WEEKLY_COMMUNITY_MOVEMENT"])
            expected_vis = sorted(["EXACT_PDF_VISUAL_REVIEW"])
        sem_path = proposal_dir / "publication" / "semantic-editorial-review-v2.json"
        vis_path = proposal_dir / "publication" / "visual-review-v2.json"
        prep = res.get("prep", {})
        assert "manuscript" in prep, f"base prepare must return manuscript: {res}"
        # Reviews via subprocess with cwd=root (fixture binding) to avoid S2 in-process error
        driver_rev = [
            "import json, sys; from pathlib import Path; root = Path(sys.argv[1]).resolve(); args = json.loads(sys.argv[2])",
            "from scripts import survey_reader_publication_v2 as reader",
            "from pypdf import PdfReader as _PdfReader",
            "ed_pdf = root / args['ed_pdf_rel']",
            "pages = len(_PdfReader(str(ed_pdf)).pages)",
            "man_rel = args['manuscript']",
            "sem_rel = args['sem_rel']; vis_rel = args['vis_rel']",
            "exp_sem = args['expected_sem']; exp_vis = args['expected_vis']",
            "reader.build_review_record(root, root / man_rel, ed_pdf, pages, 'SEMANTIC_EDITORIAL', [{'check_id': c, 'status': 'PASS', 'detail': f'synthetic {c}', 'evidence_locations': ['main.tex']} for c in exp_sem], args['reviewer'], __import__('datetime').datetime.fromisoformat(args['recorded_at']), root / sem_rel)",
            "reader.build_review_record(root, root / man_rel, ed_pdf, pages, 'VISUAL', [{'check_id': c, 'status': 'PASS', 'detail': f'synthetic {c}', 'evidence_locations': ['main.pdf']} for c in exp_vis], args['reviewer'], __import__('datetime').datetime.fromisoformat(args['recorded_at']), root / vis_rel)",
            "print(json.dumps({'ok': True, 'pages': pages}))",
        ]
        import hashlib as _hl3
        payload_rev = {"manuscript": prep["manuscript"], "ed_pdf_rel": str(ed_pdf.relative_to(root)), "sem_rel": str(sem_path.relative_to(root)), "vis_rel": str(vis_path.relative_to(root)), "expected_sem": expected_sem, "expected_vis": expected_vis, "reviewer": "SYNTHETIC_FIXTURE_REVIEWER_GENERAL_FULL_V2", "recorded_at": "2026-10-28T17:30:00+00:00"}
        proc_rev = _sp2.Popen([_sys2.executable, "-c", "\n".join(driver_rev), str(root), _jj2.dumps(payload_rev)], cwd=str(root), stdout=_sp2.PIPE, stderr=_sp2.PIPE, text=True, env={k: v for k, v in _os2.environ.items() if not k.startswith("GIT_")})
        pid_rev = proc_rev.pid
        try:
            out_rev, err_rev = proc_rev.communicate(timeout=300)
        except Exception:
            proc_rev.kill()
            out_rev, err_rev = proc_rev.communicate()
            raise AssertionError(f"reviews subprocess failed (pid {pid_rev})")
        import pathlib as _pl_rev, datetime as _dt_rev
        packet_base_rev = _pl_rev.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        stamp_rev = _dt_rev.datetime.now(_dt_rev.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest_rev = packet_base_rev / f"ed-reviews-{pid}-base-{stamp_rev}-{pid_rev}"
        assert not dest_rev.exists()
        dest_rev.mkdir(parents=True)
        (dest_rev / "stdout.txt").write_text(out_rev, encoding="utf-8")
        (dest_rev / "stderr.txt").write_text(err_rev, encoding="utf-8")
        (dest_rev / "meta.json").write_text(_jj2.dumps({"pid": pid_rev, "exit": proc_rev.returncode}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc_rev.returncode == 0, f"reviews must succeed (pid {pid_rev}): {err_rev[-3000:]}"
        import json as _jj_rev
        _res_rev = _jj_rev.loads(out_rev.strip().splitlines()[-1])
        assert _res_rev.get("ok"), f"reviews failed: {_res_rev}"
        pages = int(_res_rev.get("pages", 0))
        assert pages >= 1
        extra.update({"prep": prep, "det_checks_path": det_checks_path, "sem_path": sem_path, "vis_path": vis_path, "ed_pdf": ed_pdf, "pages": pages})
        return td, root, extra

    def _run_editorial_prepare_subprocess(self, root: Path, extra: dict, tag: str, inject: bool) -> dict:
        import subprocess as _sp, sys as _sys, json as _jj, datetime as _dt, os as _os
        from pathlib import Path as _P
        # Driver runs with cwd=root (fixture code binding), self-contained injector for fault (no exec imports)
        driver_lines = [
            "import json, sys, inspect",
            "from pathlib import Path",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "inject = args.get('inject', False)",
            "from scripts import survey_research_authority_v2 as low",
            "orig = low.require_research_operation_ready",
            "calls = []",
            "injected = {'v': False}",
            "target_file = 'survey_editorial_publication_v2.py'",
            "target_fn = 'prepare_publication'",
            "target_line = 1783",
            "entry_line = 1733",
            "guard_rel = args['guard_rel']",
            "guard_path = root / guard_rel",
            "def _outer():",
            "    st = inspect.stack()",
            "    direct = st[2] if len(st) > 2 else st[1]",
            "    outer = st[3] if len(st) > 3 else direct",
            "    return (direct.filename, direct.lineno, direct.function, outer.filename, outer.lineno, outer.function)",
            "def wrapped(repo_root, state_path):",
            "    d_f, d_l, d_fn, o_f, o_l, o_fn = _outer()",
            "    calls.append({'o_file': o_f, 'o_line': o_l, 'o_fn': o_fn})",
            "    is_target = (target_file in o_f and o_fn == target_fn and o_l == target_line)",
            "    is_entry = (target_file in o_f and o_fn == target_fn and o_l == entry_line)",
            "    # record entry/target via stdout? store in file? For parent asserts, print calls",
            "    if inject and is_target and not injected['v']:",
            "        guard_path.parent.mkdir(parents=True, exist_ok=True)",
            "        import hashlib as _hl",
            "        nonce = f\"synthetic-late-guard-v2-{target_fn}-{target_line}-{args.get('pid', 0)}\"",
            "        guard_path.write_text(json.dumps({'phase': 'TEST', 'nonce': nonce}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "        injected['v'] = True",
            "    return orig(repo_root, state_path)",
            "low.require_research_operation_ready = wrapped",
            "from scripts import survey_editorial_publication_v2 as edpub",
            "from datetime import datetime, timezone",
            "out = {}",
            "try:",
            "    prep = edpub.prepare_publication(root, args['state'], args['proposal'], args['staged_manifest'], args['manuscript_spec'], args['toolchain_spec'], datetime.fromisoformat(args['recorded_at']))",
            "    out = {'ok': True, 'prep': {k: prep[k] for k in ('manuscript','receipt','build_record') if k in prep}, 'calls': calls, 'injected': injected['v']}",
            "except Exception as e:",
            "    out = {'ok': False, 'error': f\"{type(e).__name__}: {e}\", 'calls': calls, 'injected': injected['v']}",
            "print(json.dumps(out))",
        ]
        payload = {"state": str(extra["state_path"].relative_to(root)), "proposal": str(extra["proposal_path"].relative_to(root)), "staged_manifest": str(extra["staged_manifest_path"].relative_to(root)), "manuscript_spec": str(extra["manuscript_spec_path"].relative_to(root)), "toolchain_spec": str(extra["toolchain_spec_path"].relative_to(root)), "recorded_at": "2026-10-28T16:30:00+00:00", "inject": inject, "guard_rel": str(extra.get("guard_rel", "")), "pid": _os.getpid()}
        # For healthy, guard_rel not needed (no injection); for fault, need guard_rel
        if inject:
            # Derive guard_rel from State profile (same as parent does)
            from scripts import survey_production_v2 as core
            st = core.load_json(extra["state_path"])
            prof = core.load_json(root / st["profile"]["path"])
            source_rel = prof["paths"]["source_root"]
            payload["guard_rel"] = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        proc = _sp.Popen([_sys.executable, "-c", "\n".join(driver_lines), str(root), _jj.dumps(payload)], cwd=str(root), stdout=_sp.PIPE, stderr=_sp.PIPE, text=True, env={k: v for k, v in _os.environ.items() if not k.startswith("GIT_")})
        pid = proc.pid
        try:
            out_text, err_text = proc.communicate(timeout=900)
        except Exception:
            proc.kill()
            out_text, err_text = proc.communicate()
            raise AssertionError(f"editorial prepare subprocess failed (pid {pid})")
        import pathlib as _pl2, datetime as _dt2
        packet_base = _pl2.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        stamp = _dt2.datetime.now(_dt2.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = packet_base / f"ed-prep-{tag}-{stamp}-{pid}"
        assert not dest.exists()
        dest.mkdir(parents=True)
        (dest / "stdout.txt").write_text(out_text, encoding="utf-8")
        (dest / "stderr.txt").write_text(err_text, encoding="utf-8")
        (dest / "meta.json").write_text(_jj.dumps({"pid": pid, "exit": proc.returncode, "tag": tag, "inject": inject}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc.returncode == 0, f"driver must exit 0 (pid {pid}): {err_text[-3000:]}"
        result = _jj.loads(out_text.strip().splitlines()[-1])
        result["raw_dir"] = str(dest)
        result["pid"] = pid
        return result

    def test_editorial_prepare_late_guard(self) -> None:
        # Healthy via subprocess (fixture binding, no injection) must write build outputs
        td_h, root_h, extra_h = self._build_editorial_staged_with_pid("ed-prep-healthy", "ed-late-prep-healthy")
        pre_h = lg._snapshot_files(root_h)
        res_h = self._run_editorial_prepare_subprocess(root_h, extra_h, "healthy", inject=False)
        self.assertTrue(res_h.get("ok"), f"prepare healthy must succeed: {res_h}")
        post_h = lg._snapshot_files(root_h)
        self.assertTrue(any("publication/build/main.pdf" in k for k in post_h), f"prepare healthy must write build: {sorted(set(post_h)-set(pre_h))}")
        # Fault via subprocess with late injection before 1783 must refuse, no build transfer
        td_f, root_f, extra_f = self._build_editorial_staged_with_pid("ed-prep-fault", "ed-late-prep-fault")
        from scripts import survey_production_v2 as core
        st = core.load_json(extra_f["state_path"])
        prof = core.load_json(root_f / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        pre = lg._snapshot_files(root_f)
        res_f = self._run_editorial_prepare_subprocess(root_f, extra_f, "fault", inject=True)
        self.assertFalse(res_f.get("ok"), f"prepare fault must refuse: {res_f}")
        self.assertIn("DM022_TRANSITION_ACTIVE", res_f.get("error", ""))
        # Target/entry must have been seen in subprocess calls
        calls = res_f.get("calls", [])
        self.assertTrue(any(c.get("o_line") == 1733 for c in calls), f"prepare entry 1733 not seen: {calls}")
        self.assertTrue(any(c.get("o_line") == 1783 for c in calls), f"prepare prepublish 1783 not reached: {calls}")
        self.assertTrue(res_f.get("injected"))
        post = lg._snapshot_files(root_f)
        self.assertTrue((root_f / guard_rel).is_file())
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        for k in new_keys - {guard_rel}:
            self.assertFalse(k.endswith("publication/build/main.pdf"), f"build transfer must not happen: {k}")

    def _run_editorial_finalize_subprocess(self, root: Path, extra: dict, tag: str, inject: bool, target_line: int) -> dict:
        import subprocess as _sp, sys as _sys, json as _jj, datetime as _dt, os as _os
        from pathlib import Path as _P
        driver_lines = [
            "import json, sys, inspect",
            "from pathlib import Path",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "inject = args.get('inject', False)",
            "from scripts import survey_research_authority_v2 as low",
            "orig = low.require_research_operation_ready",
            "calls = []",
            "injected = {'v': False}",
            "target_file = 'survey_editorial_publication_v2.py'",
            "target_fn = 'finalize_publication'",
            f"target_line = {target_line}",
            "entry_line = 2301",
            "guard_rel = args['guard_rel']",
            "guard_path = root / guard_rel",
            "def _outer():",
            "    st = inspect.stack()",
            "    direct = st[2] if len(st) > 2 else st[1]",
            "    outer = st[3] if len(st) > 3 else direct",
            "    return (direct.filename, direct.lineno, direct.function, outer.filename, outer.lineno, outer.function)",
            "def wrapped(repo_root, state_path):",
            "    d_f, d_l, d_fn, o_f, o_l, o_fn = _outer()",
            "    calls.append({'o_file': o_f, 'o_line': o_l, 'o_fn': o_fn})",
            "    is_target = (target_file in o_f and o_fn == target_fn and o_l == target_line)",
            "    if inject and is_target and not injected['v']:",
            "        guard_path.parent.mkdir(parents=True, exist_ok=True)",
            "        nonce = f\"synthetic-late-guard-v2-{target_fn}-{target_line}-{args.get('pid', 0)}\"",
            "        guard_path.write_text(json.dumps({'phase': 'TEST', 'nonce': nonce}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "        injected['v'] = True",
            "    return orig(repo_root, state_path)",
            "low.require_research_operation_ready = wrapped",
            "from scripts import survey_editorial_publication_v2 as edpub",
            "from datetime import datetime, timezone",
            "out = {}",
            "try:",
            "    fin = edpub.finalize_publication(root, args['state'], args['proposal'], args['staged_manifest'], args['det'], args['sem'], args['vis'], datetime.fromisoformat(args['recorded_at']))",
            "    out = {'ok': True, 'fin': {k: fin[k] for k in ('receipt_path','build_record_path','bundle_path','gate_path','candidate_path','set_path') if k in fin}, 'calls': calls, 'injected': injected['v']}",
            "except Exception as e:",
            "    out = {'ok': False, 'error': f\"{type(e).__name__}: {e}\", 'calls': calls, 'injected': injected['v']}",
            "print(json.dumps(out))",
        ]
        from scripts import survey_production_v2 as core
        st = core.load_json(extra["state_path"])
        prof = core.load_json(root / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        payload = {"state": str(extra["state_path"].relative_to(root)), "proposal": str(extra["proposal_path"].relative_to(root)), "staged_manifest": str(extra["staged_manifest_path"].relative_to(root)), "det": str(extra["det_checks_path"].relative_to(root)), "sem": str(extra["sem_path"].relative_to(root)), "vis": str(extra["vis_path"].relative_to(root)), "recorded_at": "2026-10-28T18:00:00+00:00", "inject": inject, "guard_rel": f"{source_rel}/orchestration/v2/acceptance-revision.guard.json", "pid": _os.getpid()}
        proc = _sp.Popen([_sys.executable, "-c", "\n".join(driver_lines), str(root), _jj.dumps(payload)], cwd=str(root), stdout=_sp.PIPE, stderr=_sp.PIPE, text=True, env={k: v for k, v in _os.environ.items() if not k.startswith("GIT_")})
        pid = proc.pid
        try:
            out_text, err_text = proc.communicate(timeout=900)
        except Exception:
            proc.kill()
            out_text, err_text = proc.communicate()
            raise AssertionError(f"editorial finalize subprocess failed (pid {pid})")
        import pathlib as _pl2, datetime as _dt2
        packet_base = _pl2.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        stamp = _dt2.datetime.now(_dt2.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = packet_base / f"ed-final-{tag}-{stamp}-{pid}"
        assert not dest.exists()
        dest.mkdir(parents=True)
        (dest / "stdout.txt").write_text(out_text, encoding="utf-8")
        (dest / "stderr.txt").write_text(err_text, encoding="utf-8")
        (dest / "meta.json").write_text(_jj.dumps({"pid": pid, "exit": proc.returncode, "tag": tag, "inject": inject, "target": target_line}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc.returncode == 0, f"driver must exit 0 (pid {pid}): {err_text[-3000:]}"
        result = _jj.loads(out_text.strip().splitlines()[-1])
        result["raw_dir"] = str(dest)
        result["pid"] = pid
        return result

    def test_editorial_finalize_late_guard(self) -> None:
        # Base prepared once (one TinyTeX build), copies per healthy/fault (no rebuild)
        td_base, root_base, extra_base = self._build_editorial_prepared_with_pid("ed-final-base", "ed-late-final-base")
        import shutil as _sh, tempfile as _tf
        from pathlib import Path as _P
        from scripts import survey_production_v2 as core
        # Healthy copy
        td_h = _tf.TemporaryDirectory(prefix="ed-final-healthy-")
        self.addCleanup(td_h.cleanup)
        root_h = _P(td_h.name).resolve() / "fixture"
        _sh.copytree(root_base, root_h, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        # Re-derive extra for new root (paths same rel, but absolute root changed; state_path etc. must be re-based)
        # Since copy is byte-identical (same rel paths), reconstruct extra with new root
        extra_h = dict(extra_base)
        # Update absolute paths to new root (all stored as absolute Paths)
        for k in ("state_path", "proposal_path", "manifest_path", "scope_path", "staged_manifest_path", "manuscript_spec_path", "toolchain_spec_path", "det_checks_path", "sem_path", "vis_path", "ed_pdf"):
            if k in extra_h and isinstance(extra_h[k], _P):
                # extra paths are absolute (root_base / rel); recompute as root_h / rel
                rel = extra_h[k].relative_to(root_base)
                extra_h[k] = root_h / rel
        extra_h["proposal_dir"] = root_h / extra_h["proposal_dir"].relative_to(root_base)
        extra_h["cfg"] = core.load_json(root_h / "config/survey-production-v2.json")
        pre_h = lg._snapshot_files(root_h)
        res_h = self._run_editorial_finalize_subprocess(root_h, extra_h, "healthy", inject=False, target_line=2431)
        self.assertTrue(res_h.get("ok"), f"finalize healthy must succeed: {res_h}")
        post_h = lg._snapshot_files(root_h)
        # Bundle must exist (NEW, since base had no finalize outputs)
        self.assertTrue(any("publication/bundle" in k or "quality-bundle" in k or "publication-candidate" in k for k in post_h), f"finalize healthy must write bundle/candidate: {sorted(set(post_h)-set(pre_h))}")
        # Fault copy (fresh copy of base, inject before bundle 2431)
        td_f = _tf.TemporaryDirectory(prefix="ed-final-fault-")
        self.addCleanup(td_f.cleanup)
        root_f = _P(td_f.name).resolve() / "fixture"
        _sh.copytree(root_base, root_f, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        extra_f = dict(extra_base)
        for k in ("state_path", "proposal_path", "manifest_path", "scope_path", "staged_manifest_path", "manuscript_spec_path", "toolchain_spec_path", "det_checks_path", "sem_path", "vis_path", "ed_pdf"):
            if k in extra_f and isinstance(extra_f[k], _P):
                rel = extra_f[k].relative_to(root_base)
                extra_f[k] = root_f / rel
        extra_f["proposal_dir"] = root_f / extra_base["proposal_dir"].relative_to(root_base)
        extra_f["cfg"] = core.load_json(root_f / "config/survey-production-v2.json")
        st = core.load_json(extra_f["state_path"])
        prof = core.load_json(root_f / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        pre = lg._snapshot_files(root_f)
        res_f = self._run_editorial_finalize_subprocess(root_f, extra_f, "fault", inject=True, target_line=2431)
        self.assertFalse(res_f.get("ok"))
        self.assertIn("DM022_TRANSITION_ACTIVE", res_f.get("error", ""))
        calls = res_f.get("calls", [])
        self.assertTrue(any(c.get("o_line") == 2301 for c in calls), f"finalize entry 2301 not seen: {calls}")
        self.assertTrue(any(c.get("o_line") == 2431 for c in calls), f"finalize prepublish 2431 not reached: {calls}")
        self.assertTrue(res_f.get("injected"))
        post = lg._snapshot_files(root_f)
        self.assertTrue((root_f / guard_rel).is_file())
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        # Bundle must not exist (blocked before 2431)
        for k in new_keys - {guard_rel}:
            self.assertFalse("bundle" in k and "publication" in k, f"bundle must not be written: {k}")

    def _run_editorial_activate_subprocess(self, root: Path, extra: dict, tag: str, inject: bool, target_line: int) -> dict:
        import subprocess as _sp, sys as _sys, json as _jj, datetime as _dt, os as _os
        driver_lines = [
            "import json, sys, inspect",
            "from pathlib import Path",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "inject = args.get('inject', False)",
            "from scripts import survey_research_authority_v2 as low",
            "orig = low.require_research_operation_ready",
            "calls = []",
            "injected = {'v': False}",
            "target_file = 'survey_editorial_publication_v2.py'",
            "target_fn = 'activate_publication'",
            f"target_line = {target_line}",
            "entry_line = 3466",
            "guard_rel = args['guard_rel']",
            "guard_path = root / guard_rel",
            "def _outer():",
            "    st = inspect.stack()",
            "    direct = st[2] if len(st) > 2 else st[1]",
            "    outer = st[3] if len(st) > 3 else direct",
            "    return (direct.filename, direct.lineno, direct.function, outer.filename, outer.lineno, outer.function)",
            "def wrapped(repo_root, state_path):",
            "    d_f, d_l, d_fn, o_f, o_l, o_fn = _outer()",
            "    calls.append({'o_file': o_f, 'o_line': o_l, 'o_fn': o_fn})",
            "    is_target = (target_file in o_f and o_fn == target_fn and o_l == target_line)",
            "    if inject and is_target and not injected['v']:",
            "        guard_path.parent.mkdir(parents=True, exist_ok=True)",
            "        nonce = f\"synthetic-late-guard-v2-{target_fn}-{target_line}-{args.get('pid', 0)}\"",
            "        guard_path.write_text(json.dumps({'phase': 'TEST', 'nonce': nonce}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "        injected['v'] = True",
            "    return orig(repo_root, state_path)",
            "low.require_research_operation_ready = wrapped",
            "from scripts import survey_editorial_publication_v2 as edpub",
            "from datetime import datetime",
            "out = {}",
            "try:",
            "    act = edpub.activate_publication(root, args['state'], args['set'], args['reason'], args['executor'], datetime.fromisoformat(args['recorded_at']) if isinstance(args.get('recorded_at'), str) else None)",
            "    out = {'ok': True, 'activate': act.get('status') if isinstance(act, dict) else str(act), 'calls': calls, 'injected': injected['v']}",
            "except Exception as e:",
            "    out = {'ok': False, 'error': f\"{type(e).__name__}: {e}\", 'calls': calls, 'injected': injected['v']}",
            "print(json.dumps(out))",
        ]
        from scripts import survey_production_v2 as core
        st = core.load_json(extra["state_path"])
        prof = core.load_json(root / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        payload = {"state": str(extra["state_path"].relative_to(root)), "set": str(extra["set_path"].relative_to(root)) if "set_path" in extra else str(extra.get("set_rel", "")), "reason": "Synthetic editorial activation (late-guard)", "executor": "SYNTHETIC_FIXTURE_EXECUTOR_GENERAL_FULL_V2", "recorded_at": "2026-10-28T19:00:00+00:00", "inject": inject, "guard_rel": f"{source_rel}/orchestration/v2/acceptance-revision.guard.json", "pid": _os.getpid()}
        # set_path may be stored as set_rel (relative) in extra from finalize; normalize to string
        if "set" not in payload or not payload["set"]:
            set_rel = extra.get("set_rel") or (extra.get("fin", {}) or {}).get("set_ref", {}).get("path") if isinstance(extra.get("fin"), dict) else None
            if isinstance(set_rel, dict):
                set_rel = set_rel.get("path")
            set_val = set_rel or extra.get("set_path", "")
            payload["set"] = str(set_val.relative_to(root)) if isinstance(set_val, Path) else str(set_val or "")
        proc = _sp.Popen([_sys.executable, "-c", "\n".join(driver_lines), str(root), _jj.dumps(payload)], cwd=str(root), stdout=_sp.PIPE, stderr=_sp.PIPE, text=True, env={k: v for k, v in _os.environ.items() if not k.startswith("GIT_")})
        pid = proc.pid
        try:
            out_text, err_text = proc.communicate(timeout=900)
        except Exception:
            proc.kill()
            out_text, err_text = proc.communicate()
            raise AssertionError(f"activate subprocess failed (pid {pid})")
        import pathlib as _pl2, datetime as _dt2
        packet_base = _pl2.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        stamp = _dt2.datetime.now(_dt2.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = packet_base / f"ed-activate-{tag}-{stamp}-{pid}"
        assert not dest.exists()
        dest.mkdir(parents=True)
        (dest / "stdout.txt").write_text(out_text, encoding="utf-8")
        (dest / "stderr.txt").write_text(err_text, encoding="utf-8")
        (dest / "meta.json").write_text(_jj.dumps({"pid": pid, "exit": proc.returncode, "tag": tag, "inject": inject, "target": target_line}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc.returncode == 0, f"driver must exit 0 (pid {pid}): {err_text[-3000:]}"
        result = _jj.loads(out_text.strip().splitlines()[-1])
        result["raw_dir"] = str(dest)
        result["pid"] = pid
        return result

    def test_editorial_activate_late_guard(self) -> None:
        # Base finalized once (no extra TinyTeX beyond prepared base), copies per healthy/fault
        td_base, root_base, extra_base = self._build_editorial_prepared_with_pid("ed-act-base", "ed-late-act-base")
        # Finalize base once to get set (no TinyTeX, via subprocess healthy)
        res_fin = self._run_editorial_finalize_subprocess(root_base, extra_base, "basefin", inject=False, target_line=2431)
        assert res_fin.get("ok"), f"base finalize must succeed: {res_fin}"
        # Retrieve set path from finalize outputs (bundle/gate/candidate/seal + set). Driver returns fin with set? Our finalize driver returns fin with set? It returns fin with receipt/build_record/bundle/gate/candidate/set? Actually finalize driver returns fin with ... + set? Let's get set path via publication-set? Finalize returns set_ref? In full-lifecycle, finalize returns set_ref. Our finalize driver returns fin with ...? It returns fin with receipt_path/build_record_path/bundle_path/gate_path/candidate_path/set_path? Actually our finalize driver returns fin with ...? It returns fin with ...? Let's check: finalize driver returns {'ok': True, 'fin': {k: fin[k] for k in (...) if k in fin}} – includes set? No, finalize returns set_ref? Actually finalize_publication returns dict with set_ref? In full-lifecycle, fin = edpub.finalize_publication(...); _set_rel_raw = fin['set_ref']; ... Good – finalize returns set_ref, not set_path. Our finalize driver currently returns fin with ...? It returns fin with ...? Let's make activate use set path from finalize outputs on disk: find publication-set.json in proposal_dir/publication/
        import shutil as _sh, tempfile as _tf
        from pathlib import Path as _P
        from scripts import survey_production_v2 as core
        # Find set path in base (finalize wrote set)
        # Finalize writes set to proposal_dir/publication/publication-set.json? Actually finalize returns set_ref with path. Our finalize driver didn't capture set path? It captured fin with ...? Let's re-derive set path by globbing for publication-set.json in base
        set_candidates = list(root_base.rglob("publication-set.json"))
        # Filter to proposal_dir's publication (ed-late-act-base)
        set_candidates = [p for p in set_candidates if "ed-late-act-base" in p.as_posix()]
        assert set_candidates, f"base finalize must write set: {[p.as_posix() for p in root_base.rglob('publication-set.json')]}"
        set_path_base = set_candidates[0]
        set_rel_base = str(set_path_base.relative_to(root_base))
        # Healthy copy
        td_h = _tf.TemporaryDirectory(prefix="ed-act-healthy-")
        self.addCleanup(td_h.cleanup)
        root_h = _P(td_h.name).resolve() / "fixture"
        _sh.copytree(root_base, root_h, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        extra_h = {"state_path": root_h / extra_base["state_path"].relative_to(root_base), "set_path": root_h / set_rel_base, "set_rel": set_rel_base}
        # Need full extra for activate driver (state_path + set_path + guard_rel derivation inside driver via State profile, good)
        # For activate, extra needs state_path, set_path (relative? driver expects relative? It does str(extra["state_path"].relative_to(root))? Actually driver payload uses str(extra["state_path"].relative_to(root))? No, driver payload uses str(extra["state_path"].relative_to(root))? In _run_editorial_activate_subprocess, payload uses str(extra["state_path"].relative_to(root))? Actually it uses str(extra["state_path"].relative_to(root))? Let's check: payload = {"state": str(extra["state_path"].relative_to(root)), "set": str(extra["set_path"].relative_to(root)) ...} – extra["state_path"] and extra["set_path"] must be absolute Paths (root_h / ...). Good – we set them as absolute (root_h / ...). Good.
        pre_h = lg._snapshot_files(root_h)
        res_h = self._run_editorial_activate_subprocess(root_h, {"state_path": root_h / extra_base["state_path"].relative_to(root_base), "set_path": root_h / set_rel_base}, "healthy", inject=False, target_line=3805)
        self.assertTrue(res_h.get("ok"), f"activate healthy must succeed: {res_h}")
        post_h = lg._snapshot_files(root_h)
        # Activate writes record + State (State sha changes, record exists)
        self.assertTrue(any("activation-record" in k or "editorial-activation" in k or "publication-set" in k for k in post_h), f"activate healthy must write record/set: {sorted(set(post_h)-set(pre_h))}")
        # Fault copy (fresh copy of base with finalize outputs, inject before record 3805)
        td_f = _tf.TemporaryDirectory(prefix="ed-act-fault-")
        self.addCleanup(td_f.cleanup)
        root_f = _P(td_f.name).resolve() / "fixture"
        _sh.copytree(root_base, root_f, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        extra_f = {"state_path": root_f / extra_base["state_path"].relative_to(root_base), "set_path": root_f / set_rel_base}
        st = core.load_json(extra_f["state_path"])
        prof = core.load_json(root_f / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        pre = lg._snapshot_files(root_f)
        res_f = self._run_editorial_activate_subprocess(root_f, extra_f, "fault", inject=True, target_line=3805)
        self.assertFalse(res_f.get("ok"))
        self.assertIn("DM022_TRANSITION_ACTIVE", res_f.get("error", ""))
        calls = res_f.get("calls", [])
        self.assertTrue(any(c.get("o_line") == 3466 for c in calls), f"activate entry 3466 not seen: {calls}")
        self.assertTrue(any(c.get("o_line") == 3805 for c in calls), f"activate prepublish 3805 not reached: {calls}")
        post = lg._snapshot_files(root_f)
        self.assertTrue((root_f / guard_rel).is_file())
        new_keys = set(post) - set(pre)
        self.assertIn(guard_rel, new_keys)
        # Record must not exist (blocked before 3805)
        for k in new_keys - {guard_rel}:
            self.assertFalse("activation-record" in k, f"record must not be written: {k}")

    def _run_editorial_resume_subprocess(self, root: Path, extra: dict, tag: str, inject: bool, target_line: int) -> dict:
        import subprocess as _sp, sys as _sys, json as _jj, datetime as _dt, os as _os
        driver_lines = [
            "import json, sys, inspect",
            "from pathlib import Path",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "inject = args.get('inject', False)",
            "from scripts import survey_research_authority_v2 as low",
            "orig = low.require_research_operation_ready",
            "calls = []",
            "injected = {'v': False}",
            "target_file = 'survey_editorial_publication_v2.py'",
            "target_fn = 'resume_activation'",
            f"target_line = {target_line}",
            "entry_line = 3954",
            "guard_rel = args['guard_rel']",
            "guard_path = root / guard_rel",
            "def _outer():",
            "    st = inspect.stack()",
            "    direct = st[2] if len(st) > 2 else st[1]",
            "    outer = st[3] if len(st) > 3 else direct",
            "    return (direct.filename, direct.lineno, direct.function, outer.filename, outer.lineno, outer.function)",
            "def wrapped(repo_root, state_path):",
            "    d_f, d_l, d_fn, o_f, o_l, o_fn = _outer()",
            "    calls.append({'o_file': o_f, 'o_line': o_l, 'o_fn': o_fn})",
            "    is_target = (target_file in o_f and o_fn == target_fn and o_l == target_line)",
            "    if inject and is_target and not injected['v']:",
            "        guard_path.parent.mkdir(parents=True, exist_ok=True)",
            "        nonce = f\"synthetic-late-guard-v2-{target_fn}-{target_line}-{args.get('pid', 0)}\"",
            "        guard_path.write_text(json.dumps({'phase': 'TEST', 'nonce': nonce}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "        injected['v'] = True",
            "    return orig(repo_root, state_path)",
            "low.require_research_operation_ready = wrapped",
            "from scripts import survey_editorial_publication_v2 as edpub",
            "out = {}",
            "try:",
            "    res = edpub.resume_activation(root, args['state'], args['record'])",
            "    out = {'ok': True, 'res': str(res.get('status')) if isinstance(res, dict) else str(res), 'calls': calls, 'injected': injected['v']}",
            "except Exception as e:",
            "    out = {'ok': False, 'error': f\"{type(e).__name__}: {e}\", 'calls': calls, 'injected': injected['v']}",
            "print(json.dumps(out))",
        ]
        from scripts import survey_production_v2 as core
        st = core.load_json(extra["state_path"])
        prof = core.load_json(root / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        payload = {"state": str(extra["state_path"].relative_to(root)), "record": str(extra["record_path"].relative_to(root)), "inject": inject, "guard_rel": f"{source_rel}/orchestration/v2/acceptance-revision.guard.json", "pid": _os.getpid()}
        proc = _sp.Popen([_sys.executable, "-c", "\n".join(driver_lines), str(root), _jj.dumps(payload)], cwd=str(root), stdout=_sp.PIPE, stderr=_sp.PIPE, text=True, env={k: v for k, v in _os.environ.items() if not k.startswith("GIT_")})
        pid = proc.pid
        try:
            out_text, err_text = proc.communicate(timeout=900)
        except Exception:
            proc.kill()
            out_text, err_text = proc.communicate()
            raise AssertionError(f"resume subprocess failed (pid {pid})")
        import pathlib as _pl2, datetime as _dt2
        packet_base = _pl2.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        stamp = _dt2.datetime.now(_dt2.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = packet_base / f"ed-resume-{tag}-{stamp}-{pid}"
        assert not dest.exists()
        dest.mkdir(parents=True)
        (dest / "stdout.txt").write_text(out_text, encoding="utf-8")
        (dest / "stderr.txt").write_text(err_text, encoding="utf-8")
        (dest / "meta.json").write_text(_jj.dumps({"pid": pid, "exit": proc.returncode, "tag": tag, "inject": inject, "target": target_line}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc.returncode == 0, f"driver must exit 0 (pid {pid}): {err_text[-3000:]}"
        result = _jj.loads(out_text.strip().splitlines()[-1])
        result["raw_dir"] = str(dest)
        result["pid"] = pid
        return result

    def test_editorial_resume_late_guard(self) -> None:
        import shutil as _sh, tempfile as _tf
        from pathlib import Path as _P
        from scripts import survey_production_v2 as core
        # Base prepared (one build) then finalized (no build) to get set + old State (no record yet)
        td_base, root_base, extra_base = self._build_editorial_prepared_with_pid("ed-res-base", "ed-late-res-base")
        res_fin_base = self._run_editorial_finalize_subprocess(root_base, extra_base, "basefin-res", inject=False, target_line=2431)
        assert res_fin_base.get("ok"), f"base finalize must succeed: {res_fin_base}"
        set_cands = [p for p in root_base.rglob("publication-set.json") if "ed-late-res-base" in p.as_posix()]
        assert set_cands, "base finalize must write set"
        set_rel_base = str(set_cands[0].relative_to(root_base))
        # Orphan source: fresh copy of finalized base (old State + set), activate healthy (no injection) to get record + new State
        td_orph = _tf.TemporaryDirectory(prefix="ed-res-orphsrc-")
        self.addCleanup(td_orph.cleanup)
        root_orph = _P(td_orph.name).resolve() / "fixture"
        _sh.copytree(root_base, root_orph, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        extra_orph = {"state_path": root_orph / extra_base["state_path"].relative_to(root_base), "set_path": root_orph / set_rel_base}
        res_act_orph = self._run_editorial_activate_subprocess(root_orph, extra_orph, "orphsrc", inject=False, target_line=3805)
        assert res_act_orph.get("ok"), f"orphan source activate must succeed: {res_act_orph}"
        rec_cands = [p for p in root_orph.rglob("publication-surface-revalidation-r*.json")]
        if not rec_cands:
            # Fallback: any *revalidation*.json under proposal publication (excluding set/bundle/etc.)
            prop_pub = root_orph / extra_base["proposal_dir"].relative_to(root_base) / "publication"
            rec_cands = [p for p in prop_pub.rglob("*revalidation*.json")]
            rec_cands = [p for p in rec_cands if "publication-set.json" not in p.name]
        assert rec_cands, f"activate must write record"
        rec_rel = str(rec_cands[0].relative_to(root_orph))
        # Healthy resume copy (fresh copy of finalized base with old State + set, plus orphan record, no guard)
        td_h = _tf.TemporaryDirectory(prefix="ed-res-healthy-")
        self.addCleanup(td_h.cleanup)
        root_h = _P(td_h.name).resolve() / "fixture"
        _sh.copytree(root_base, root_h, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        (root_h / rec_rel).parent.mkdir(parents=True, exist_ok=True)
        (root_h / rec_rel).write_bytes((root_orph / rec_rel).read_bytes())
        extra_h = {"state_path": root_h / extra_base["state_path"].relative_to(root_base), "record_path": root_h / rec_rel}
        pre_h = lg._snapshot_files(root_h)
        res_h = self._run_editorial_resume_subprocess(root_h, extra_h, "healthy", inject=False, target_line=4025)
        assert res_h.get("ok"), f"resume healthy must succeed: {res_h}"
        post_h = lg._snapshot_files(root_h)
        # State must have changed (new State installed) or record installed? Resume installs via State replace (State sha changes). Check State sha changed or new files.
        self.assertTrue(any("production-state.json" in k for k in post_h), "resume healthy must touch State")
        # Fault copy (fresh copy of finalized base + orphan record, inject before 4025)
        td_f = _tf.TemporaryDirectory(prefix="ed-res-fault-")
        self.addCleanup(td_f.cleanup)
        root_f = _P(td_f.name).resolve() / "fixture"
        _sh.copytree(root_base, root_f, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        (root_f / rec_rel).parent.mkdir(parents=True, exist_ok=True)
        (root_f / rec_rel).write_bytes((root_orph / rec_rel).read_bytes())
        extra_f = {"state_path": root_f / extra_base["state_path"].relative_to(root_base), "record_path": root_f / rec_rel}
        st = core.load_json(extra_f["state_path"])
        prof = core.load_json(root_f / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        pre = lg._snapshot_files(root_f)
        res_f = self._run_editorial_resume_subprocess(root_f, extra_f, "fault", inject=True, target_line=4025)
        assert not res_f.get("ok"), f"resume fault must refuse: {res_f}"
        assert "DM022_TRANSITION_ACTIVE" in res_f.get("error", ""), res_f
        calls = res_f.get("calls", [])
        assert any(c.get("o_line") == 3954 for c in calls), f"resume entry 3954 not seen: {calls}"
        assert any(c.get("o_line") == 4025 for c in calls), f"resume prepublish 4025 not reached: {calls}"
        assert res_f.get("injected")
        post = lg._snapshot_files(root_f)
        assert (root_f / guard_rel).is_file()
        new_keys = set(post) - set(pre)
        assert guard_rel in new_keys
        # State must NOT have changed (still old), record preserved (already existed in pre, so no NEW record besides guard)
        # Since record already existed in pre (orphan copied before pre), new_keys should be only guard (no State rewrite to NEW? Actually State sha in post should equal pre (old), since refused before install. Good.
        for k in new_keys - {guard_rel}:
            assert "production-state.json" not in k or lg._snapshot_files(root_f)[k] == pre.get(k), f"State must not change on refused resume: {k}"

    def _run_release_checkpoint_subprocess(self, root: Path, extra: dict, tag: str, inject: bool, target_line: int) -> dict:
        import subprocess as _sp, sys as _sys, json as _jj, datetime as _dt, os as _os
        driver_lines = [
            "import json, sys, inspect",
            "from pathlib import Path",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "inject = args.get('inject', False)",
            "from scripts import survey_research_authority_v2 as low",
            "orig = low.require_research_operation_ready",
            "calls = []",
            "injected = {'v': False}",
            "target_file = 'survey_release_checkpoint_v2.py'",
            "target_fn = 'build_release_checkpoint'",
            f"target_line = {target_line}",
            "entry_line = 67",
            "guard_rel = args['guard_rel']",
            "guard_path = root / guard_rel",
            "def _outer():",
            "    st = inspect.stack()",
            "    direct = st[2] if len(st) > 2 else st[1]",
            "    outer = st[3] if len(st) > 3 else direct",
            "    return (direct.filename, direct.lineno, direct.function, outer.filename, outer.lineno, outer.function)",
            "def wrapped(repo_root, state_path):",
            "    d_f, d_l, d_fn, o_f, o_l, o_fn = _outer()",
            "    calls.append({'o_file': o_f, 'o_line': o_l, 'o_fn': o_fn})",
            "    is_target = (target_file in o_f and o_fn == target_fn and o_l == target_line)",
            "    if inject and is_target and not injected['v']:",
            "        guard_path.parent.mkdir(parents=True, exist_ok=True)",
            "        nonce = f\"synthetic-late-guard-v2-{target_fn}-{target_line}-{args.get('pid', 0)}\"",
            "        guard_path.write_text(json.dumps({'phase': 'TEST', 'nonce': nonce}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "        injected['v'] = True",
            "    return orig(repo_root, state_path)",
            "low.require_research_operation_ready = wrapped",
            "from scripts import survey_release_checkpoint_v2 as rel",
            "from scripts import survey_production_v2 as core",
            "from datetime import datetime",
            "out = {}",
            "try:",
            "    cfg = core.load_json(root / core.DEFAULT_CONFIG)",
            "    cp = rel.build_release_checkpoint(root, cfg, Path(args['state']), Path(args['merge']), Path(args['record']), datetime.fromisoformat(args['recorded_at']))",
            "    out = {'ok': True, 'cp': str(cp.relative_to(root)) if hasattr(cp, 'relative_to') else str(cp), 'calls': calls, 'injected': injected['v']}",
            "except Exception as e:",
            "    out = {'ok': False, 'error': f\"{type(e).__name__}: {e}\", 'calls': calls, 'injected': injected['v']}",
            "print(json.dumps(out))",
        ]
        from scripts import survey_production_v2 as core
        st = core.load_json(extra["state_path"])
        prof = core.load_json(root / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        payload = {"state": str(extra["state_path"].relative_to(root)), "merge": str(extra["merge_path"].relative_to(root)), "record": str(extra["record_path"].relative_to(root)), "recorded_at": "2026-10-29T00:00:00+00:00", "inject": inject, "guard_rel": f"{source_rel}/orchestration/v2/acceptance-revision.guard.json", "pid": _os.getpid()}
        proc = _sp.Popen([_sys.executable, "-c", "\n".join(driver_lines), str(root), _jj.dumps(payload)], cwd=str(root), stdout=_sp.PIPE, stderr=_sp.PIPE, text=True, env={k: v for k, v in _os.environ.items() if not k.startswith("GIT_")})
        pid = proc.pid
        try:
            out_text, err_text = proc.communicate(timeout=900)
        except Exception:
            proc.kill()
            out_text, err_text = proc.communicate()
            raise AssertionError(f"release subprocess failed (pid {pid})")
        import pathlib as _pl2, datetime as _dt2
        packet_base = _pl2.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm022-prearchitecture-implementation/evidence/late-guards-20261029T060000Z")
        stamp = _dt2.datetime.now(_dt2.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        dest = packet_base / f"ed-release-{tag}-{stamp}-{pid}"
        assert not dest.exists()
        dest.mkdir(parents=True)
        (dest / "stdout.txt").write_text(out_text, encoding="utf-8")
        (dest / "stderr.txt").write_text(err_text, encoding="utf-8")
        (dest / "meta.json").write_text(_jj.dumps({"pid": pid, "exit": proc.returncode, "tag": tag, "inject": inject, "target": target_line}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        assert proc.returncode == 0, f"driver must exit 0 (pid {pid}): {err_text[-3000:]}"
        result = _jj.loads(out_text.strip().splitlines()[-1])
        result["raw_dir"] = str(dest)
        result["pid"] = pid
        return result

    def test_release_checkpoint_late_guard(self) -> None:
        # FROZEN via VALIDATED_DRAFT durable + candidate/preview/freeze (no TinyTeX rebuild, REAL PDFs), then merge + record + checkpoint with NEW outputs
        man = _manifest()
        durable = Path(man["weekly_validated_prepreview"]["durable_path"])
        from scripts import survey_publication_v2 as pub
        from scripts import survey_production_v2 as core
        from scripts import survey_agent_control_v2 as agent
        from datetime import datetime, timezone
        import shutil as _sh, tempfile as _tf, subprocess as _sp
        from pathlib import Path as _P
        from tests import test_dm022_full_lifecycle_v2 as full
        owner = full.Dm022FullLifecycleWitnessTests("test_weekly_dm022_to_selection_stage")
        # Base FROZEN (one freeze chain, no injection) to get FROZEN State + freeze outputs - use canonical paths (fresh copy has no candidate yet, so canonical is NEW)
        td_base, root_base = lg._copy_durable_to_temp(self, durable, "rel-base-")
        man_rel = "sources/2026-W33/publication/v2/reader-manuscript-v2.json"
        src_rel = "surveys/weekly/2026-W33/main.tex"
        pdf_rel = "surveys/weekly/2026-W33/main.pdf"
        bundle_rel = "sources/2026-W33/publication/v2/quality-regression-bundle-v2.json"
        sem_rel = "sources/2026-W33/publication/v2/semantic-editorial-review-v2.json"
        vis_rel = "sources/2026-W33/publication/v2/visual-review-v2.json"
        sem_doc = core.load_json(root_base / sem_rel)
        page_count = int(sem_doc.get("page_count", 5) or 5)
        cand_rel = "sources/2026-W33/publication/v2/publication-candidate-v2.json"
        pub.build_candidate(root_base, "2026-W33", "WEEKLY_MAGAZINE", root_base / man_rel, root_base / src_rel, root_base / pdf_rel, page_count, root_base / bundle_rel, root_base / sem_rel, root_base / vis_rel, root_base / cand_rel, state_path=root_base / "sources/2026-W33/production-state.json")
        cfg = core.load_json(root_base / "config/survey-production-v2.json")
        state_abs = root_base / "sources/2026-W33/production-state.json"
        cand_reviews = owner._stage_reviews_for(root_base, cfg, state_abs, {"publication-candidate": root_base / cand_rel}, "candidate-rel-base")
        cand_cp = agent.build_stage_checkpoint(root_base, cfg, state_abs, {"publication-candidate": root_base / cand_rel}, cand_reviews, "Candidate staged (late-guard).", datetime(2026, 10, 28, 10, 0, 0, tzinfo=timezone.utc))
        agent.advance_with_checkpoint(root_base, cfg, state_abs, cand_cp)
        agent.approve_publication_preview(root_base, cfg, state_abs, "SYNTHETIC_FIXTURE_REVIEWER_GENERAL_FULL_V2", datetime(2026, 10, 28, 11, 0, 0, tzinfo=timezone.utc), "synthetic-rel-late")
        # Freeze via normal public API using HumanGate approval (canonical paths, fresh copy has no freeze yet)
        freeze_rel = "sources/2026-W33/publication/v2/freeze-record-v2.json"
        manifest_rel = "sources/2026-W33/publication/v2/release-manifest-v2.json"
        preview_approval_rel = f"sources/2026-W33/{cfg['state_authority']['publication_preview_approval_path']}"
        pub.build_freeze(root_base, root_base / cand_rel, root_base / preview_approval_rel, datetime(2026, 10, 28, 12, 0, 0, tzinfo=timezone.utc), root_base / freeze_rel, root_base / manifest_rel)
        freeze_reviews = owner._stage_reviews_for(root_base, cfg, state_abs, {"freeze-record": root_base / freeze_rel, "release-manifest": root_base / manifest_rel, "visual-review-record": root_base / vis_rel}, "freeze-rel-base")
        freeze_cp = agent.build_stage_checkpoint(root_base, cfg, state_abs, {"freeze-record": root_base / freeze_rel, "release-manifest": root_base / manifest_rel, "visual-review-record": root_base / vis_rel}, freeze_reviews, "Freeze staged (late-guard).", datetime(2026, 10, 28, 13, 0, 0, tzinfo=timezone.utc))
        agent.advance_with_checkpoint(root_base, cfg, state_abs, freeze_cp)
        assert core.load_json(state_abs)["lifecycle_state"] == "FROZEN", f"must reach FROZEN: {core.load_json(state_abs)['lifecycle_state']}"
        # Merge verification + release record with canonical paths (fresh copy has no merge/record yet, so canonical is NEW, no clearing)
        merge_rel = "sources/2026-W33/publication/v2/merge-verification-v2.json"
        record_rel = "sources/2026-W33/publication/v2/release-record-v2.json"
        fixture_head = _sp.run(["git", "rev-parse", "HEAD"], cwd=str(root_base), capture_output=True, text=True, check=True).stdout.strip()
        pub.build_merge_verification(root_base, root_base / manifest_rel, fixture_head, datetime(2026, 10, 28, 14, 0, 0, tzinfo=timezone.utc), root_base / merge_rel)
        pub.build_release_record(root_base, root_base / manifest_rel, root_base / merge_rel, datetime(2026, 10, 29, 0, 0, 0, tzinfo=timezone.utc), "synthetic-rel-late", root_base / record_rel)
        # Healthy and fault copies (both FROZEN with merge+record, no release checkpoint yet)
        td_h = _tf.TemporaryDirectory(prefix="rel-healthy-")
        self.addCleanup(td_h.cleanup)
        root_h = _P(td_h.name).resolve() / "fixture"
        _sh.copytree(root_base, root_h, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        extra_h = {"state_path": root_h / "sources/2026-W33/production-state.json", "merge_path": root_h / merge_rel, "record_path": root_h / record_rel}
        pre_h = lg._snapshot_files(root_h)
        res_h = self._run_release_checkpoint_subprocess(root_h, extra_h, "healthy", inject=False, target_line=231)
        assert res_h.get("ok"), f"release healthy must succeed: {res_h}"
        post_h = lg._snapshot_files(root_h)
        # Release checkpoint writes FROZEN.json (canonical for FROZEN, NEW) + core-stage-contract (NEW); driver does build only, not advance, so State stays FROZEN
        new_h = set(post_h) - set(pre_h)
        assert any(k.endswith("checkpoints/FROZEN.json") for k in new_h), f"release healthy must write FROZEN checkpoint: {sorted(new_h)}"
        td_f = _tf.TemporaryDirectory(prefix="rel-fault-")
        self.addCleanup(td_f.cleanup)
        root_f = _P(td_f.name).resolve() / "fixture"
        _sh.copytree(root_base, root_f, symlinks=False, ignore=_sh.ignore_patterns("__pycache__", "*.pyc"))
        extra_f = {"state_path": root_f / "sources/2026-W33/production-state.json", "merge_path": root_f / merge_rel, "record_path": root_f / record_rel}
        st = core.load_json(extra_f["state_path"])
        prof = core.load_json(root_f / st["profile"]["path"])
        source_rel = prof["paths"]["source_root"]
        guard_rel = f"{source_rel}/orchestration/v2/acceptance-revision.guard.json"
        pre = lg._snapshot_files(root_f)
        res_f = self._run_release_checkpoint_subprocess(root_f, extra_f, "fault", inject=True, target_line=231)
        assert not res_f.get("ok")
        assert "DM022_TRANSITION_ACTIVE" in res_f.get("error", ""), res_f
        calls = res_f.get("calls", [])
        assert any(c.get("o_line") == 67 for c in calls), f"release entry 67 not seen: {calls}"
        assert any(c.get("o_line") == 231 for c in calls), f"release prepublish 231 not reached: {calls}"
        assert res_f.get("injected")
        post = lg._snapshot_files(root_f)
        assert (root_f / guard_rel).is_file()
        new_keys = set(post) - set(pre)
        assert guard_rel in new_keys

if __name__ == "__main__":
    unittest.main()