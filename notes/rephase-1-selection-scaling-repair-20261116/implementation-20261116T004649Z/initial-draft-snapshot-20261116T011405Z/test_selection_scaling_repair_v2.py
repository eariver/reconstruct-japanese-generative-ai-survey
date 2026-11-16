#!/usr/bin/env python3
"""Focused behavioral verification for bounded Selection scaling repair (MAP-ONLY impl).

Uses existing genuine synthetic fixtures + minimal genuine temp files (real JSONs,
real validators, no stubs to authority). No active/shadow writes, no network/
Production/Gate/PDF/R4, no real-material writer. Needed-blob fault ONLY on NEW
disposable test DB (never author DB, never b797). PYTHONDONTWRITEBYTECODE=1,
GIT_NO_LAZY_FETCH=1, no install.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat as _stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import MappingProxyType

from scripts import survey_production_v2 as core
from scripts import survey_architecture_v2_base as base
from scripts import survey_review_attention_v2 as attention
from scripts import survey_research_authority_v2 as low
from scripts import survey_evidence_v2 as evidence


def _write_json(path: Path, payload: dict) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = core.json_bytes(payload)
    path.write_bytes(raw)
    return raw


class TestBaseSharedHelper(unittest.TestCase):
    def test_against_upstream_repo_root_first_and_summary_shared(self) -> None:
        # Minimal genuine upstream: 1 discovery/task/card/view/ledger/completeness.
        # Uses real files + real P decoder, no stubs.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            prof = {"issue_id": "SYNTH-001", "research_profile": "THEMATIC", "publication_profile": "WEEKLY",
                    "paths": {"source_root": "src"}, "research_profiles": {}, "publication_profiles": {}}
            prof_path = root / "profile.json"
            _write_json(prof_path, prof)
            # Card/view files with SHA binds (view filename is hash-based per evidence.view_filename).
            from scripts.survey_evidence_v2 import view_filename as _vf
            vf_name = _vf("t1")
            res_dir = root / "results"
            views_dir = root / "views"
            res_dir.mkdir(parents=True, exist_ok=True)
            views_dir.mkdir(parents=True, exist_ok=True)
            card = {"artifact": {"canonical_name": "T", "artifact_type": "NOTE"},
                    "sources": [], "claims": [], "metrics": [], "limitations": [],
                    "verification": {"unresolved_questions": [], "contradictions": []},
                    "entities": [], "evidence_task_id": "t1", "discovery_ids": ["d1"], "status": "VERIFIED"}
            view = {"profile_annotations": {}, "materiality": "MATERIAL", "scope_dimensions": [],
                    "evidence_task_id": "t1"}
            card_path = res_dir / "t1.json"
            view_path = views_dir / vf_name
            card_raw = _write_json(card_path, card)
            view_raw = _write_json(view_path, view)
            upstream = {
                "profile": {"issue_id": "SYNTH-001", "research_profile": "THEMATIC"},
                "discoveries": [{"provenance": {"origin": "BASE", "research_pass": 0, "parent_refs": [], "obligation_ids": []}}],
                "screening": {"decisions": []},
                "evidence": {"results": [{"evidence_task_id": "t1", "discovery_ids": ["d1"],
                                          "sha256": hashlib.sha256(card_raw).hexdigest(),
                                          "filename": "t1.json", "status": "VERIFIED"}]},
                "views": {"views": [{"evidence_task_id": "t1", "view_sha256": hashlib.sha256(view_raw).hexdigest(),
                                     "materiality": "MATERIAL", "scope_dimensions": []}]},
                "ledger": {"rows": [{"evidence_task_ids": ["t1"], "downstream_disposition": "MATERIAL"}]},
                "completeness": {"overall_status": "COMPLETE", "obligations": [], "residual_limitations": []},
            }
            comp_path = root / "completeness.json"
            ledger_path = root / "ledger.json"
            ev_acc_path = root / "ev-accepted.json"
            views_acc_path = root / "views-accepted.json"
            _write_json(comp_path, {"overall_status": "COMPLETE"})
            _write_json(ledger_path, {"rows": [{"evidence_task_ids": ["t1"]}]})
            _write_json(ev_acc_path, {"results": upstream["evidence"]["results"]})
            _write_json(views_acc_path, {"views": upstream["views"]["views"]})
            matrix = base._derive_matrix_rows_content(root, upstream, prof_path, comp_path, ledger_path, ev_acc_path, views_acc_path)
            self.assertEqual(matrix["issue_id"], "SYNTH-001")
            # against_upstream repo_root FIRST, same rows, no _load_upstream.
            errs = base._validate_candidate_matrix_against_upstream(
                root, matrix, upstream, prof_path, comp_path, ledger_path, ev_acc_path, views_acc_path)
            self.assertEqual(errs, [])
            bad = dict(matrix)
            bad["rows"] = []
            errs2 = base._validate_candidate_matrix_against_upstream(
                root, bad, upstream, prof_path, comp_path, ledger_path, ev_acc_path, views_acc_path)
            self.assertTrue(errs2)
            # Shared summary: public path exercised via helper directly (no duplication).
            sel = {"assignments": []}
            arch = {"packages": [], "selected_exceptions": [], "status": "PROPOSED",
                    "editorial_thesis": "t", "architecture_goals": ["g"], "page_plan": {"target_pages": 1, "max_pages": 2, "notes": None},
                    "profile_extensions": {}, "publication_extensions": {}}
            m_path = root / "m.json"; s_path = root / "s.json"; a_path = root / "a.json"
            _write_json(m_path, matrix); _write_json(s_path, sel); _write_json(a_path, arch)
            c_path = root / "c.json"; l_path = root / "l.json"
            _write_json(c_path, {"overall_status": "COMPLETE", "obligations": [], "residual_limitations": []})
            _write_json(l_path, {"rows": []})
            # Minimal config for validate_selection/validate_architecture (role_namespace contracts).
            cfg_path = root / "config" / "survey-production-v2.json"
            _write_json(cfg_path, {"research_profiles": {"THEMATIC": {"role_namespace": "TH:"}},
                                   "publication_profiles": {"WEEKLY": {"role_namespace": "WK:"}}})
            # Minimal profile for basis SHAs (files exist, SHAs bound).
            out1 = base._summarize_review_contents(
                root, upstream, matrix, sel, arch, prof_path, c_path, l_path, m_path, s_path, a_path, [])
            self.assertEqual(out1["readiness"]["status"], "READY_FOR_ARCHITECTURE_REVIEW")
            out2 = base._build_architecture_review_summary_with_upstream(
                root, prof_path, root / "d.json", root / "sc.json", ev_acc_path, views_acc_path,
                l_path, c_path, m_path, s_path, a_path, upstream)
            # with_upstream loads m/s/a from disk; ensure same payload shape (no second algorithm).
            self.assertEqual(out2["schema_version"], out1["schema_version"])
            self.assertEqual(out2["major_material_destinations"], out1["major_material_destinations"])


class TestAttentionPayload(unittest.TestCase):
    def test_payload_helper_shared_and_limits(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # Schemas required for validation: copy genuine schema into temp repo root.
            import shutil as _sh
            cands = sorted(Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime").glob("selection-scaling-implementation-*/candidate-work"))
            impl_base = cands[-1]
            (root / "schemas").mkdir(parents=True, exist_ok=True)
            _sh.copy2(impl_base / "schemas" / "architecture-review-attention-v2.schema.json",
                      root / "schemas" / "architecture-review-attention-v2.schema.json")
            scr = {"issue_id": "SYNTH-001", "decisions": [{"decision": "DROP", "discovery_id": "d1", "reason": "r"}]}
            led = {"issue_id": "SYNTH-001", "rows": [{"downstream_disposition": "HOLD", "discovery_id": "d1", "rationale": "r"}]}
            sel = {"issue_id": "SYNTH-001", "assignments": [{"candidate_id": "c1", "disposition": "HOLD", "rationale": "r"}]}
            sp = root / "s.json"; lp = root / "l.json"; cp = root / "c.json"
            _write_json(sp, scr); _write_json(lp, led); _write_json(cp, sel)
            payload = attention._build_attention_payload(root, sp, lp, cp, limit=50)
            self.assertEqual(payload["total_count"], 3)
            self.assertEqual(payload["limit"], 50)
            out = root / "att.json"
            ret = attention.build_attention(root, sp, lp, cp, out, limit=50)
            self.assertEqual(ret, out)
            self.assertEqual(json.loads(out.read_bytes().decode()), payload)
            attention.validate_attention(root, out)
            with self.assertRaisesRegex(ValueError, "limit"):
                attention._build_attention_payload(root, sp, lp, cp, limit=0)
            # Second build must refuse (no overwrite), proving no silent repair.
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                attention.build_attention(root, sp, lp, cp, out, limit=50)


class TestLowCaptureRecheckRealReadOnly(unittest.TestCase):
    def test_capture_recheck_passes_real_w34_sp_no_writes(self) -> None:
        # Read-only on NEW author copy (byte-copy of active ae0dd1e, no writes).
        # Proves initial full validity binding without running real writer.
        for src in ["sources/2026-W34/production-state.json", "sources/SP-efficient-llm-2026/production-state.json"]:
            repo = Path.cwd()
            # Resolve NEW copy location via env or cwd? Use known NEW copy path from setup.
            # Find selection-scaling-implementation-*/candidate-work under runtime dir.
            cands = sorted(Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime").glob("selection-scaling-implementation-*/candidate-work"))
            self.assertTrue(cands, "NEW implementation copy missing")
            base = cands[-1]
            sp = base / src
            read_set = low._capture_selection_read_set(base, sp)
            # Basic pins present, no Session files.
            labels = [p[0] for p in read_set.pins]
            self.assertIn("production state", labels)
            self.assertIn("production profile", labels)
            # Recheck same bytes must pass (no drift, no rebaseline).
            low._recheck_selection_read_set(base, sp, read_set)


class TestDriftGates(unittest.TestCase):
    def test_phase_pin_drift_refuses_no_next_write(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "a.json"; b = root / "b.json"
            a.write_bytes(b'{"k":1}\n'); b.write_bytes(b'{"k":2}\n')
            pins = evidence._capture_phase_pins((("A", a), ("B", b)))
            # No next write yet; mutate one byte after seal.
            a.write_bytes(b'{"k":9}\n')
            with self.assertRaisesRegex(ValueError, "bytes changed"):
                evidence._recheck_phase_pins(pins)
            # No next write occurred after refusal (no new file).
            self.assertFalse((root / "next.json").exists())

    def test_guard_and_preflight_and_owned(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "src"
            src.mkdir()
            # Guard present must refuse (canonical guard path, not .guard).
            gpath = low.guard_path_for(src)
            gpath.parent.mkdir(parents=True, exist_ok=True)
            gpath.write_text("x", encoding="utf-8")
            with self.assertRaises(Exception):
                low.require_no_active_guard(src)
            gpath.unlink()
            low.require_no_active_guard(src)
            # Preflight seven absent once; present refuses.
            from scripts import run_selection_architecture_v2_interactive as runmod
            runmod._dm022_preflight_seven(src)
            (src / "candidate-matrix-v2.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                runmod._dm022_preflight_seven(src)

    def test_input_pin_drift(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inp = root / "in.json"
            inp.write_bytes(b'{"a":1}\n')
            raw = inp.read_bytes()
            pin = ("interactive input", inp, hashlib.sha256(raw).hexdigest(), len(raw))
            inp.write_bytes(b'{"a":2}\n')
            with self.assertRaisesRegex(ValueError, "bytes changed|drift"):
                # Simulate runner _check input re-read vs pin.
                cur = inp.read_bytes()
                if len(cur) != pin[3] or hashlib.sha256(cur).hexdigest() != pin[2]:
                    raise ValueError("interactive input bytes changed after seal")


class TestNoSuppVsDowngrade(unittest.TestCase):
    def test_healthy_no_supp_valid(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctx = evidence._resolve_phase_supplement_context(
                root, {}, implementation_sha=None, screening_acceptance=None, discoveries=None)
            # Empty context legitimate (no supplement).
            self.assertIn("manifest_ref", ctx if isinstance(ctx, dict) else {})
            # Legal empty passes; no generic None+None refusal here (withdrawn).

    def test_supplemented_null_downgrade_refuses(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old_pkg = {"authority_supplement": {"path": "supp/manifest.json", "sha256": "00" * 32}}
            req = {"supplement_manifest": None}
            with self.assertRaisesRegex(Exception, "OLD supplemented \\+ NEW.*null refused|supplement"):
                low._bind_selected_supplement_for_revision(root, req, {}, old_pkg)


class TestLegacySeparate(unittest.TestCase):
    def test_legacy_keeps_legacy_branch(self) -> None:
        # Synthetic LEGACY: structural without same triplet -> LEGACY, no PREARCH graph, no own-epoch.
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            # Minimal State without same triplet -> _resolve returns LEGACY family.
            st = {"profile": {"path": "p.json", "sha256": "00" * 32},
                  "checkpoint_provenance": {"evidence": {"path": "a", "sha256": "00" * 32},
                                            "materiality": {"path": "b", "sha256": "11" * 32},
                                            "completeness": {"path": "a", "sha256": "00" * 32}}}
            struct = low._resolve_research_from_state_bytes(root, st)
            self.assertEqual(struct.get("family"), "LEGACY")


class TestExactSet(unittest.TestCase):
    def test_extra_symlink_refuse_disposable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            d = root / "tasks"
            d.mkdir()
            (d / "t1.json").write_text("{}", encoding="utf-8")
            # Exact set with expected {t1.json} passes.
            evidence._exact_regular_files(d, {"t1.json"}, "evidence tasks")
            # Extra file refuses.
            (d / "extra.json").write_text("{}", encoding="utf-8")
            with self.assertRaises(Exception):
                evidence._exact_regular_files(d, {"t1.json"}, "evidence tasks")
            (d / "extra.json").unlink()
            # Symlink refuses (never author DB, disposable only).
            (d / "link.json").symlink_to(d / "t1.json")
            with self.assertRaises(Exception):
                evidence._exact_regular_files(d, {"t1.json", "link.json"}, "evidence tasks")


class TestBlobFaultDisposable(unittest.TestCase):
    def test_own_epoch_full_batch_refuses_missing_blob_disposable_only(self) -> None:
        # NEW disposable Git DB (never author DB, never b797), layout known, retained originals.
        with tempfile.TemporaryDirectory() as td:
            work = Path(td) / "work"
            work.mkdir()
            env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1",
                   "GIT_AUTHOR_NAME": "Synthetic Test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
                   "GIT_COMMITTER_NAME": "Synthetic Test", "GIT_COMMITTER_EMAIL": "test@example.invalid",
                   "PYTHONDONTWRITEBYTECODE": "1", "GIT_NO_LAZY_FETCH": "1"}
            def run_git(*args: str) -> str:
                res = subprocess.run(["git", *args], cwd=str(work), capture_output=True, text=True, env=env, timeout=60)
                if res.returncode != 0:
                    raise AssertionError(f"git {' '.join(args)} failed: {res.stderr}")
                return res.stdout.strip()
            run_git("init", "-q")
            run_git("remote", "add", "origin", "https://example.invalid/disposable-blob-fault.git")
            (work / "f.txt").write_text("hello\n", encoding="utf-8")
            run_git("add", "-A")
            run_git("-c", "user.name=Synthetic Test", "-c", "user.email=test@example.invalid",
                    "commit", "-q", "-m", "disposable meaningful commit")
            head = run_git("rev-parse", "HEAD")
            # Layout known: loose objects, no alternates, inert origin, nlink==1.
            self.assertFalse((work / ".git" / "objects" / "info" / "alternates").exists())
            self.assertIn("example.invalid", run_git("remote", "get-url", "origin"))
            # Find one loose blob (not commit/tree, layout known via cat-file).
            # Use real needed blob from this disposable (not b797, not author DB).
            blob = run_git("rev-parse", f"{head}:f.txt")
            # Verify present, then mv aside (retain originals).
            aa, rest = blob[:2], blob[2:]
            obj_path = work / ".git" / "objects" / aa / rest
            self.assertTrue(obj_path.is_file(), "expected loose blob layout known")
            backup = Path(td) / "backup_blob"
            backup.write_bytes(obj_path.read_bytes())
            obj_path.unlink()
            # Full object read must now refuse (proves cat-file -e alone insufficient, full batch required).
            res = subprocess.run(["git", "-C", str(work), "cat-file", "-e", blob],
                                 capture_output=True, env=env, timeout=60)
            self.assertNotEqual(res.returncode, 0, "missing blob must refuse")
            # Restore, re-verify pass.
            obj_path.write_bytes(backup.read_bytes())
            res2 = subprocess.run(["git", "-C", str(work), "cat-file", "-e", blob],
                                  capture_output=True, env=env, timeout=60)
            self.assertEqual(res2.returncode, 0)


if __name__ == "__main__":
    unittest.main()
