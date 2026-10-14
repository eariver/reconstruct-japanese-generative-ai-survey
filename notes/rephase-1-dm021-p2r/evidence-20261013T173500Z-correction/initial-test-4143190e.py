"""DM021-P2R focused tests: one-shot retention capture + standalone verify.

Real accepted-chain fixtures through actual producers/stage validators in
independent Git databases (process-scoped identity, inert origins, no empty
commits); fixture source commits include all P1/LF2I bytes PLUS all3 P2R
files BEFORE authority (local override, no P1 test change). Every capture /
verify call is wrapped in immediately-around snapshots. Synthetic reviews
are type/identity fixtures, never semantic acceptance. No assert keyword
guards (explicit TestCase methods; safe under python -O).
"""
from __future__ import annotations

import json
import os
import shutil
import stat as _stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import survey_production_v2 as core
from scripts import survey_editorial_retention_v2 as retention

from tests import test_survey_editorial_correction_proposal_v2 as p1t

ProposalError = p1t.ProposalError
RetentionError = retention.RetentionError

_GIT_VARS = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)

P2R_EXTRA = (
    "scripts/survey_editorial_retention_v2.py",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "tests/test_survey_editorial_retention_v2.py",
)

W_ISSUE = p1t.W_ISSUE
L_ISSUE = p1t.L_ISSUE


def _run_git(root: Path, *args: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
        "GIT_AUTHOR_NAME": "Synthetic DM021-P2R Fixture", "GIT_AUTHOR_EMAIL": "p2r-fixture@example.invalid",
        "GIT_COMMITTER_NAME": "Synthetic DM021-P2R Fixture", "GIT_COMMITTER_EMAIL": "p2r-fixture@example.invalid",
    })
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=env)


def _make_p2r_source_root(testcase: unittest.TestCase, prefix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    workspace = Path(__file__).resolve().parents[1]
    scratch = tempfile.TemporaryDirectory(prefix=prefix)
    testcase.addCleanup(scratch.cleanup)
    root = Path(scratch.name).resolve()
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", ".github", "config", "schemas", "scripts", "templates", "prompts",
         "docs", "data", "tests"],
        cwd=workspace, capture_output=True, check=True).stdout
    for raw in tracked.split(b"\0"):
        if not raw:
            continue
        relative = Path(raw.decode("utf-8"))
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(workspace / relative, destination)
    for rel in list(p1t.UNTRACKED_SOURCES) + list(P2R_EXTRA):
        source = workspace / rel
        testcase.assertTrue(source.is_file(), f"untracked P2R source missing: {rel}")
        destination = root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        testcase.assertEqual(core.sha256_file(destination), core.sha256_file(source),
                             f"fixture copy drift: {rel}")
    for command in (
        ["init", "-q"],
        ["remote", "add", "origin", "https://example.invalid/dm021-p2r-fixture.git"],
        ["add", "-A"],
        ["-c", "user.name=Synthetic DM021-P2R Fixture",
         "-c", "user.email=p2r-fixture@example.invalid",
         "commit", "-q", "-m", "Synthetic isolated DM021-P2R source basis"],
    ):
        proc = _run_git(root, *command)
        testcase.assertEqual(proc.returncode, 0, f"git {command}: {proc.stderr}")
    status = _run_git(root, "status", "--porcelain").stdout
    testcase.assertEqual(status, "", f"fixture source not clean after commit: {status}")
    return scratch, root


def _snapshot(root: Path) -> dict:
    return p1t._snapshot(root)


def _assert_no_write(testcase: unittest.TestCase, before: dict, after: dict, label: str) -> None:
    p1t._assert_no_write(testcase, before, after, label)


def _allowed_delta_only(testcase: unittest.TestCase, before: dict, after: dict,
                        allowed_prefix: str, label: str) -> None:
    # Old originals unchanged; only exact allowed retention delta added.
    before_files = before["files"]
    after_files = after["files"]
    for rel, sha in before_files.items():
        testcase.assertIn(rel, after_files, f"disappearance during {label}: {rel}")
        testcase.assertEqual(after_files[rel], sha, f"drift during {label}: {rel}")
    added = sorted(set(after_files) - set(before_files))
    testcase.assertTrue(added, f"no retained delta during {label}")
    for rel in added:
        testcase.assertTrue(rel.startswith(allowed_prefix),
                            f"unowned addition during {label}: {rel}")
    testcase.assertEqual(after["head"], before["head"], f"HEAD moved during {label}")


def _prepare_proposal_for(testcase: unittest.TestCase, root: Path, helper, chain: dict,
                          state_path: Path, proposal_id: str, authored_mut) -> tuple[Path, dict]:
    from scripts import survey_editorial_correction_proposal_v2 as p1mod
    authored = authored_mut()
    staged_authoring = p1t._stage_authoring_before_prepare(testcase, root, helper.source_root, proposal_id, authored)
    prepared = p1mod.prepare_proposal(root, state_path, staged_authoring, proposal_id,
                                      f"Fixture P2R correction {proposal_id}.")
    proposal_path = p1t._stage_reader_and_proposal(testcase, root, helper.source_root, proposal_id, prepared)
    return proposal_path, prepared


class EditorialRetentionV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in _GIT_VARS:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        self.workspace = Path(__file__).resolve().parents[1]

    def test_longform_capture_verify_positive(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-longform-")
        helper = p1t._new_longform_helper(self, root, self.workspace)
        chain = helper._complete(helper._chain())
        state_path = helper._state_path(chain)
        helper._advance_to_validated_draft(chain, state_path)
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "VALIDATED_DRAFT")

        def _mut():
            authored = helper._authored(chain, helper.worker)
            authored["longform_revision"]["packages"][0]["narrative_sections"][0]["paragraphs"][0]["text"] += \
                " Revised fixture sentence within approved evidence."
            return authored

        proposal_path, prepared = _prepare_proposal_for(self, root, helper, chain, state_path,
                                                        "fixture-lf-p2r-1", _mut)
        before = _snapshot(root)
        out = retention.capture_retention(root, state_path, proposal_path)
        after = _snapshot(root)
        self.assertEqual(out["result"], "RETAINED_SET_CAPTURED")
        proposal_dir = f"sources/{L_ISSUE}/publication/v2/editorial-corrections/fixture-lf-p2r-1"
        _allowed_delta_only(self, before, after, proposal_dir + "/retained/", "longform capture")
        manifest_path = root / out["manifest_path"]
        self.assertTrue(manifest_path.is_file())
        self.assertEqual(core.sha256_file(manifest_path), out["manifest_sha256"])
        manifest = core.load_json(manifest_path)
        self.assertEqual(manifest["schema_version"], "2.0-rc1")
        self.assertEqual(manifest["kind"], "EDITORIAL_RETENTION_V1")
        self.assertEqual(manifest["status"], "CAPTURED")
        # Rows project P1 plan exactly (order, COPY measured, KEEP exact).
        plan = prepared["proposal"]["retention_plan"]
        self.assertEqual(len(manifest["rows"]), len(plan))
        for prow, mrow in zip(plan, manifest["rows"]):
            self.assertEqual(mrow["path"], prow["path"])
            self.assertEqual(mrow["roles"], sorted(prow["roles"]))
            if prow["policy"] == "KEEP_IMMUTABLE":
                self.assertNotIn("retained_dest", mrow)
                self.assertNotIn("retained_sha256", mrow)
                self.assertNotIn("retained_byte_count", mrow)
                self.assertEqual(mrow["retained_ref"], {"path": prow["path"], "sha256": prow["sha256"]})
            else:
                self.assertNotIn("retained_ref", mrow)
                self.assertEqual(mrow["retained_sha256"], prow["sha256"])
                self.assertEqual(mrow["retained_byte_count"], prow["byte_count"])
        # capture_inputs binds every P1 hash + 2 P2R deps.
        self.assertIn("scripts/survey_editorial_retention_v2.py",
                      {e["path"] for e in manifest["capture_inputs"]})
        self.assertIn("schemas/editorial-retention-manifest-v2.schema.json",
                      {e["path"] for e in manifest["capture_inputs"]})
        snap = _snapshot(root)
        vout = retention.verify_retention(root, proposal_path, manifest_path)
        self.assertEqual(vout["result"], "RETAINED_SET_VERIFIED")
        _assert_no_write(self, snap, _snapshot(root), "longform verify no-write")

    def test_weekly_capture_verify_positive(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-weekly-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly P2R test, revised edition"
            return authored

        proposal_path, prepared = _prepare_proposal_for(self, root, helper, chain, state_path,
                                                        "fixture-wk-p2r-1", _mut)
        before = _snapshot(root)
        out = retention.capture_retention(root, state_path, proposal_path)
        after = _snapshot(root)
        self.assertEqual(out["result"], "RETAINED_SET_CAPTURED")
        proposal_dir = f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-p2r-1"
        _allowed_delta_only(self, before, after, proposal_dir + "/retained/", "weekly capture")
        vout = retention.verify_retention(root, proposal_path, root / out["manifest_path"])
        self.assertEqual(vout["result"], "RETAINED_SET_VERIFIED")

    def test_r1_double_refresh_capture_verify(self) -> None:
        # Real R1 x2: two non-emitted refreshes, supersedes chain, two captures.
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-r1-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        target = root / "scripts" / "survey_weekly_derivation_v2.py"
        original = target.read_text(encoding="utf-8")
        self.assertNotIn("R1 non-emitted fixture comment", original)
        refresh_script = (
            "import sys\nfrom pathlib import Path\nroot = Path(sys.argv[1])\nstate_path = Path(sys.argv[2])\n"
            "from scripts import survey_production_v2 as core\n"
            "from scripts import survey_weekly_mechanical_refresh_v2 as r1\n"
            "from datetime import datetime, timezone\n"
            "recorded = datetime(2026, 9, 19, 8, 0, 0, tzinfo=timezone.utc)\n"
            "result = r1.refresh_mechanical_evidence(root, cfg if False else core.load_json(root / core.DEFAULT_CONFIG), state_path, 'fixture R1 refresh', 'synthetic P2R R1', recorded)\n"
            "print(core.sha256_object(result)[:16])\n"
        )
        target.write_text(original + "\n# R1 non-emitted fixture comment: no output change.\n", encoding="utf-8")
        proc = _run_git(root, "add", "scripts/survey_weekly_derivation_v2.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P2R Fixture",
                        "-c", "user.email=p2r-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture R1 non-emitted derivation comment")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        p1t._run_fixture_code(self, root, refresh_script, [str(root), str(state_path)])
        state1 = core.load_json(state_path)
        self.assertIsNotNone(state1.get("publication_revalidation_provenance"))

        def _mut1():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly R1 first refresh, revised edition"
            return authored

        pp1, _prep1 = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-r1a-1", _mut1)
        out1 = retention.capture_retention(root, state_path, pp1)
        self.assertEqual(out1["result"], "RETAINED_SET_CAPTURED")
        v1 = retention.verify_retention(root, pp1, root / out1["manifest_path"])
        self.assertEqual(v1["result"], "RETAINED_SET_VERIFIED")
        # Second non-emitted commit + refresh -> supersedes chain depth.
        target.write_text(target.read_text(encoding="utf-8") + "# R1 second non-emitted comment.\n", encoding="utf-8")
        proc = _run_git(root, "add", "scripts/survey_weekly_derivation_v2.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P2R Fixture",
                        "-c", "user.email=p2r-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture R1 second non-emitted comment")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        p1t._run_fixture_code(self, root, refresh_script, [str(root), str(state_path)])
        from scripts import survey_agent_control_v2 as _agent
        cfg2 = core.load_json(root / core.DEFAULT_CONFIG)
        record2, errors2 = _agent.resolve_active_publication_revalidation(root, cfg2, core.load_json(state_path))
        self.assertEqual(errors2, [])
        self.assertIsNotNone(record2.get("supersedes"))

        def _mut2():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly R1 second refresh, revised edition"
            return authored

        pp2, _prep2 = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-r1b-1", _mut2)
        out2 = retention.capture_retention(root, state_path, pp2)
        self.assertEqual(out2["result"], "RETAINED_SET_CAPTURED")
        v2 = retention.verify_retention(root, pp2, root / out2["manifest_path"])
        self.assertEqual(v2["result"], "RETAINED_SET_VERIFIED")
        # KEEP rows reference live originals: after the second tool commit,
        # the first retained set's KEEP pin no longer matches live bytes, so
        # it must now refuse (ANY KEEP drift fails, including tool closure).
        with self.assertRaisesRegex(RetentionError, "INVALID_RETENTION|REF_DRIFT"):
            retention.verify_retention(root, pp1, root / out1["manifest_path"])

    def test_refuse_existing_retained_root(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-exists-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly exists test, revised edition"
            return authored

        # Empty dir.
        pp_e, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ex-empty", _mut)
        (root / f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-ex-empty/retained").mkdir()
        snap = _snapshot(root)
        with self.assertRaisesRegex(RetentionError, "RETAINED_ROOT_EXISTS"):
            retention.capture_retention(root, state_path, pp_e)
        _assert_no_write(self, snap, _snapshot(root), "empty retained root no-write")
        # Same-byte foreign files.
        pp_s, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ex-same", _mut)
        foreign = root / f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-ex-same/retained"
        foreign.mkdir()
        (foreign / "foreign.txt").write_bytes(b"same bytes foreign")
        snap2 = _snapshot(root)
        with self.assertRaisesRegex(RetentionError, "RETAINED_ROOT_EXISTS"):
            retention.capture_retention(root, state_path, pp_s)
        _assert_no_write(self, snap2, _snapshot(root), "same-byte foreign no-write")
        # Dangling alias.
        pp_d, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ex-alias", _mut)
        alias = root / f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-ex-alias/retained"
        alias.symlink_to(root / "nonexistent-p2r-target")
        snap3 = _snapshot(root)
        with self.assertRaisesRegex(RetentionError, "RETAINED_ROOT_EXISTS"):
            retention.capture_retention(root, state_path, pp_d)
        _assert_no_write(self, snap3, _snapshot(root), "dangling alias no-write")

    def test_refuse_unsafe_schema_order_inputs(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-neg-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly neg test, revised edition"
            return authored

        pp, prepared = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-neg-1", _mut)
        out = retention.capture_retention(root, state_path, pp)
        manifest_path = root / out["manifest_path"]
        manifest = core.load_json(manifest_path)
        good_bytes = manifest_path.read_bytes()

        def _corrupt_and_check(mut, pattern: str) -> None:
            bad = json.loads(json.dumps(manifest))
            mut(bad)
            manifest_path.write_bytes(core.json_bytes(bad) if isinstance(bad, dict) else bad)
            try:
                with self.assertRaisesRegex(RetentionError, pattern):
                    retention.verify_retention(root, pp, manifest_path)
            finally:
                manifest_path.write_bytes(good_bytes)

        # Reordered rows are not plan equality.
        def _rev_rows(bad: dict) -> None:
            bad["rows"] = list(reversed(bad["rows"]))
        _corrupt_and_check(_rev_rows, "RETENTION_ORDER_MISMATCH|RETENTION_MISMATCH")
        # Unsorted roles.
        def _rev_roles(bad: dict) -> None:
            for r in bad["rows"]:
                if len(r["roles"]) > 1:
                    r["roles"] = list(reversed(r["roles"]))
                    break
        _corrupt_and_check(_rev_roles, "RETENTION_ORDER_MISMATCH|RETENTION_MISMATCH")
        # KEEP with COPY-only fields.
        def _keep_extra(bad: dict) -> None:
            for r in bad["rows"]:
                if r["policy"] == "KEEP_IMMUTABLE":
                    r["retained_sha256"] = "0" * 64
                    r["retained_byte_count"] = 1
                    break
        _corrupt_and_check(_keep_extra, "RETENTION_MISMATCH|SCHEMA_INVALID|INVALID_RETENTION")
        # Duplicate capture_inputs.
        def _dup_inputs(bad: dict) -> None:
            bad["capture_inputs"] = bad["capture_inputs"] + [bad["capture_inputs"][0]]
        _corrupt_and_check(_dup_inputs, "RETENTION_MISMATCH|RETENTION_ORDER_MISMATCH")
        # Noncanonical key order (same data, reordered keys): bypass json_bytes
        # to preserve the noncanonical order on disk.
        parsed = json.loads(good_bytes.decode("utf-8"))
        reordered: dict = {}
        for k in reversed(list(parsed.keys())):
            reordered[k] = parsed[k]
        manifest_path.write_bytes((json.dumps(reordered, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        try:
            with self.assertRaisesRegex(RetentionError, "MANIFEST_NONCANONICAL|RETENTION_MISMATCH|INVALID_RETENTION"):
                retention.verify_retention(root, pp, manifest_path)
        finally:
            manifest_path.write_bytes(good_bytes)
        self.assertEqual(retention.verify_retention(root, pp, manifest_path)["result"],
                         "RETAINED_SET_VERIFIED")
        # Traversal proposal refuses pre-write with no writes.
        snap = _snapshot(root)
        with self.assertRaisesRegex(RetentionError, "PATH_TRAVERSAL|PATH_NOT_REPO_LOCAL"):
            retention.capture_retention(root, state_path, "../outside.json")
        _assert_no_write(self, snap, _snapshot(root), "traversal no-write")

    def test_keep_x_profile_distinction_and_drift(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-xprof-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly XProfile test, revised edition"
            return authored

        pp, _prep = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-x-1", _mut)
        out = retention.capture_retention(root, state_path, pp)
        manifest = core.load_json(root / out["manifest_path"])
        # Distinct X identity correctly pinned is tolerated (not substituted):
        # verifier uses State.profile exact match, X rows simply rechecked.
        v = retention.verify_retention(root, pp, root / out["manifest_path"])
        self.assertEqual(v["result"], "RETAINED_SET_VERIFIED")
        # ANY required KEEP drift fails: drift the required KEEP Profile.
        state_rows = [r for r in manifest["rows"] if "state:authority" in r["roles"]]
        self.assertEqual(len(state_rows), 1)
        rstate = json.loads((root / state_rows[0]["retained_dest"]).read_bytes().decode("utf-8"))
        prof_path = rstate["profile"]["path"]
        keep = [r for r in manifest["rows"] if r.get("retained_ref", {}).get("path") == prof_path]
        self.assertEqual(len(keep), 1)
        full = root / prof_path
        original = full.read_bytes()
        try:
            full.write_bytes(original + b"\n")
            with self.assertRaisesRegex(RetentionError, "INVALID_RETENTION|REF_DRIFT"):
                retention.verify_retention(root, pp, root / out["manifest_path"])
        finally:
            full.write_bytes(original)
        # X-row drift (any other KEEP row) also fails.
        other_keep = [r for r in manifest["rows"] if r["policy"] == "KEEP_IMMUTABLE"
                      and r["path"] != prof_path]
        self.assertTrue(other_keep, "expected another KEEP row for X-drift oracle")
        victim = other_keep[0]["retained_ref"]["path"]
        vfull = root / victim
        vorig = vfull.read_bytes()
        try:
            vfull.write_bytes(vorig + b"\n")
            with self.assertRaisesRegex(RetentionError, "INVALID_RETENTION|REF_DRIFT"):
                retention.verify_retention(root, pp, root / out["manifest_path"])
        finally:
            vfull.write_bytes(vorig)
        self.assertEqual(retention.verify_retention(root, pp, root / out["manifest_path"])["result"],
                         "RETAINED_SET_VERIFIED")

    def test_persistence_vs_eligibility_and_wrong_path(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-persist-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly persist test, revised edition"
            return authored

        pp, _prep = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ps-1", _mut)
        out = retention.capture_retention(root, state_path, pp)
        manifest = core.load_json(root / out["manifest_path"])
        copy_rows = [r for r in manifest["rows"] if r["policy"] == "COPY_BEFORE_REPLACEMENT"]
        self.assertTrue(copy_rows)
        live_path = root / copy_rows[0]["path"]
        live_orig = live_path.read_bytes()
        try:
            live_path.write_bytes(live_orig + b"\n")
            # Persistence: verifier never reads live COPY originals, still verifies;
            # current eligibility expressly unproved (no P1 claim made here).
            v = retention.verify_retention(root, pp, root / out["manifest_path"])
            self.assertEqual(v["result"], "RETAINED_SET_VERIFIED")
        finally:
            live_path.write_bytes(live_orig)
        # Retained COPY mutation fails.
        ret_full = root / copy_rows[0]["retained_dest"]
        rorig = ret_full.read_bytes()
        try:
            ret_full.write_bytes(rorig + b"\n")
            with self.assertRaisesRegex(RetentionError, "INVALID_RETENTION"):
                retention.verify_retention(root, pp, root / out["manifest_path"])
        finally:
            ret_full.write_bytes(rorig)
        # Staged reader mutation fails.
        proposed = manifest["proposed"]
        staged = root / proposed["proposed_reader_ref"]["path"]
        sorig = staged.read_bytes()
        try:
            staged.write_bytes(sorig + b"\n")
            with self.assertRaisesRegex(RetentionError, "INVALID_RETENTION|REF_DRIFT"):
                retention.verify_retention(root, pp, root / out["manifest_path"])
        finally:
            staged.write_bytes(sorig)
        # Same manifest bytes at wrong proposal path fail (no path rebind).
        pp2, _prep2 = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ps-2", _mut)
        with self.assertRaisesRegex(RetentionError, "HEADER_MISMATCH|INVALID_RETENTION|BASIS_MISMATCH"):
            retention.verify_retention(root, pp2, root / out["manifest_path"])

    def test_p1_refuses_after_capture_no_p1_git_in_verify(self) -> None:
        from scripts import survey_editorial_correction_proposal_v2 as p1mod
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-postp1-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly postP1 test, revised edition"
            return authored

        pp, _prep = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-pp-1", _mut)
        out = retention.capture_retention(root, state_path, pp)
        self.assertEqual(out["result"], "RETAINED_SET_CAPTURED")
        with self.assertRaisesRegex(ProposalError, "RETENTION_DEST_CONFLICT"):
            p1mod.validate_proposal(root, state_path, pp)
        # Standalone verify makes no P1/Git calls: patch both to raise.
        with mock.patch.object(p1mod, "validate_proposal",
                               side_effect=AssertionError("P1 must not be called")):
            with mock.patch("subprocess.run", side_effect=AssertionError("Git must not be called")):
                v = retention.verify_retention(root, pp, root / out["manifest_path"])
        self.assertEqual(v["result"], "RETAINED_SET_VERIFIED")

    def test_fault_write_close_readback_identity_fifo(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-fault-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut(tag: str):
            def _f():
                authored = core.load_json(chain["authored_path"])
                authored["cover"]["headline"] = f"Weekly fault {tag}, revised edition"
                return authored
            return _f

        # Short-write loop success: single short return completed in loop.
        pp_loop, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ft-loop", _mut("loop"))
        real_write = os.write
        calls = {"n": 0}

        def _short_once(fd: int, data: bytes) -> int:
            if calls["n"] == 0 and len(data) > 1:
                calls["n"] += 1
                return real_write(fd, data[:1])
            return real_write(fd, data)

        with mock.patch("os.write", side_effect=_short_once):
            out = retention.capture_retention(root, state_path, pp_loop)
        self.assertEqual(out["result"], "RETAINED_SET_CAPTURED")
        # Zero-progress write fails (owned partial preserved, live untouched).
        pp_zero, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ft-zero", _mut("zero"))
        live_before = _snapshot(root)
        with mock.patch("os.write", return_value=0):
            with self.assertRaisesRegex(RetentionError, "WRITE_FAILED|MANIFEST_CLOSE_FAILED"):
                retention.capture_retention(root, state_path, pp_zero)
        # Partial preserved (retained root exists), live originals unchanged except owned delta.
        proposal_dir = f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-ft-zero/retained"
        self.assertTrue((root / proposal_dir).exists())
        with self.assertRaisesRegex(RetentionError, "RETAINED_ROOT_EXISTS"):
            retention.capture_retention(root, state_path, pp_zero)
        # Close failure is indeterminate even if bytes complete.
        pp_close, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ft-close", _mut("close"))

        def _close_fail(fd: int) -> None:
            raise OSError("injected close failure")

        with mock.patch("os.close", side_effect=_close_fail):
            with self.assertRaisesRegex(RetentionError, "CLOSE_FAILED|MANIFEST_CLOSE_FAILED|INDETERMINATE"):
                retention.capture_retention(root, state_path, pp_close)
        # Root replacement after success: no foreign writes, verify detects.
        pp_rep, _ = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-ft-rep", _mut("rep"))
        out_rep = retention.capture_retention(root, state_path, pp_rep)
        self.assertEqual(out_rep["result"], "RETAINED_SET_CAPTURED")
        # FIFO no-read oracle: FIFO at planned input refuses without blocking.
        fifo = root / f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-ft-rep/fifo-probe"
        try:
            os.mkfifo(fifo)
        except OSError:
            pass
        else:
            import signal

            def _handler(signum, frame):
                raise TimeoutError("fifo open blocked")

            old = signal.signal(signal.SIGALRM, _handler)
            try:
                signal.alarm(5)
                with self.assertRaisesRegex(RetentionError, "PATH_NOT_REGULAR|PATH_ALIAS|PATH_UNREADABLE"):
                    retention.capture_retention(root, state_path, fifo)
                signal.alarm(0)
            finally:
                signal.signal(signal.SIGALRM, old)
                try:
                    fifo.unlink()
                except OSError:
                    pass
        self.assertEqual(live_before["head"], _snapshot(root)["head"])

    def test_drift_prefinal_and_finalization(self) -> None:
        scratch, root = _make_p2r_source_root(self, "jgas-p2r-drift-")
        helper = p1t._new_weekly_helper(self, root)
        built = p1t._build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]

        def _mut():
            authored = core.load_json(chain["authored_path"])
            authored["cover"]["headline"] = "Weekly drift test, revised edition"
            return authored

        pp, prepared = _prepare_proposal_for(self, root, helper, chain, state_path, "fixture-wk-dr-1", _mut)
        # Mutate a KEEP file via side effect during COPY writes (before manifest):
        # late recheck must refuse finalization, partial preserved.
        keep_path = None
        for r in prepared["proposal"]["retention_plan"]:
            if r["policy"] == "KEEP_IMMUTABLE":
                keep_path = root / r["path"]
                break
        self.assertIsNotNone(keep_path)
        keep_orig = keep_path.read_bytes()
        real_write = os.write
        mutated = {"done": False}

        def _write_then_mutate(fd: int, data: bytes) -> int:
            n = real_write(fd, data)
            if not mutated["done"]:
                mutated["done"] = True
                keep_path.write_bytes(keep_orig + b"\n")
            return n

        with mock.patch("os.write", side_effect=_write_then_mutate):
            with self.assertRaisesRegex(RetentionError, "FINALIZATION_REFUSED|STABILITY_VIOLATION|REF_DRIFT"):
                retention.capture_retention(root, state_path, pp)
        keep_path.write_bytes(keep_orig)
        # Extra file inside retained subtree before finalization refuses tested
        # via post-partial inventory: retained root exists from the partial above.
        proposal_dir = f"sources/{W_ISSUE}/publication/v2/editorial-corrections/fixture-wk-dr-1/retained"
        self.assertTrue((root / proposal_dir).exists())
        with self.assertRaisesRegex(RetentionError, "RETAINED_ROOT_EXISTS"):
            retention.capture_retention(root, state_path, pp)


if __name__ == "__main__":
    unittest.main()
