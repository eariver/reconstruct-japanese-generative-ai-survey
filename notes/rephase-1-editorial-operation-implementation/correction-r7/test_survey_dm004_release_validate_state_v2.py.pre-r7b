"""DM-004 Release workflow/CLI/State-validation bounded acceptance.

Uses the existing real-validator DM001/019 SpecialFixture (imported, not
copied) to reach FROZEN, then real merge-verification/release-record builders
and the real release-checkpoint CLI to reach RELEASED. No authority/Git
success mocks in any new case; the synthetic release reference never claims a
real remote Release. Research/editorial/visual/Human content is synthetic.

The new `validate-state` CLI normalizes/contain the State path through
existing helpers before any byte load; the closure oracle executes the actual
extracted workflow run block under bash (not a hand-rebuilt argv).
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from datetime import timedelta
from pathlib import Path

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_profiled_freeze_v2 as profiled
from scripts import survey_publication_v2 as publication

ROOT = Path(".").resolve()
_DM001019_SPEC = importlib.util.spec_from_file_location(
    "dm004_dm001019_fixture",
    ROOT / "tests/test_survey_dm001_019_freeze_equivalence_v2.py",
)
assert _DM001019_SPEC is not None and _DM001019_SPEC.loader is not None
_DM = importlib.util.module_from_spec(_DM001019_SPEC)
_DM001019_SPEC.loader.exec_module(_DM)

ISSUE_PREFIX = "SP-DM004"
SURVEY_PREFIX = "surveys/special/SP-DM004"
ESCAPE_BASE = Path("/tmp/opencode")
AT = _DM.T0 + timedelta(hours=5)
RELEASE_REF = "synthetic:dm004-offline-no-remote"
CONTAINMENT_ERROR = "must be repository-local"


def offline_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = {
        "PATH": f"{Path(sys.executable).parent}:/usr/bin:/bin",
        "PYTHONPATH": ".",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_ALLOW_PROTOCOL": "file",
    }
    if "HOME" in os.environ:
        env["HOME"] = os.environ["HOME"]
    if extra:
        env.update(extra)
    return env


def run_cli(*argv: str, cwd: Path = ROOT,
            extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *argv], cwd=str(cwd),
        env=offline_env(extra_env), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def inventory(roots: list[Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for base in roots:
        for p in sorted(base.rglob("*")):
            key = str(p.relative_to(ROOT))
            if p.is_symlink():
                out[key] = "link:" + os.readlink(p)
            elif p.is_file():
                out[key] = core.sha256_file(p)
    return out


def drop_sibling(test: unittest.TestCase, sib: Path) -> None:
    """Register cleanup removing sibling temp dir contents, then the dir."""
    def _drop() -> None:
        for p in sorted(sib.glob("*")):
            if p.is_symlink() or p.is_file():
                p.unlink()
        sib.rmdir()
    test.addCleanup(_drop)


def state_paths(fix) -> tuple[Path, str, str]:
    state = fix.src / "production-state.json"
    rel = str(state.relative_to(ROOT))
    return state, rel, str(state)


def build_to_frozen(test: unittest.TestCase, tag: str):
    issue = f"{ISSUE_PREFIX}-{tag}"
    survey_rel = f"{SURVEY_PREFIX}-{tag}"
    for p in (ROOT / "sources" / issue, ROOT / survey_rel):
        test.assertFalse(p.exists(), f"fixture path not absent: {p}")
    fix = _DM.SpecialFixture(ROOT, issue, survey_rel)
    test.addCleanup(fix.cleanup)
    candidate = _DM._special_advance_to_rc(fix, AT)
    _DM._special_approve(fix, AT)
    profiled.build_profiled_freeze(ROOT, fix.cfg, fix.src / "production-state.json",
                                   AT + timedelta(hours=3))
    validated = publication.validate_candidate(
        ROOT, fix.src / "publication" / "v2" / "publication-candidate-v2.json",
        issue_id=issue)
    artifacts = {
        "visual-review-record": ROOT / validated["visual_review"]["path"],
        "freeze-record": fix.src / "publication" / "v2" / "freeze-record-v2.json",
        "release-manifest": fix.src / "publication" / "v2" / "release-manifest-v2.json",
    }
    _DM._special_advance_to_frozen(fix, artifacts, AT, "dm004")
    state = core.load_json(fix.src / "production-state.json")
    test.assertEqual(state["lifecycle_state"], "FROZEN")
    test.assertEqual(agent.validate_agent_state(ROOT, fix.cfg, state), [])
    return fix


def build_to_released(test: unittest.TestCase, tag: str):
    fix = build_to_frozen(test, tag)
    frozen_state = core.load_json(fix.src / "production-state.json")
    release_cp = agent.canonical_checkpoint_path(ROOT, fix.cfg, frozen_state)
    pub = fix.src / "publication" / "v2"
    manifest = pub / "release-manifest-v2.json"
    verification = pub / "merge-verification-v2.json"
    record = pub / "release-record-v2.json"
    impl = core.repository_commit_sha(ROOT)
    publication.build_merge_verification(
        ROOT, manifest, impl, AT + timedelta(hours=5), verification)
    publication.build_release_record(
        ROOT, manifest, verification, AT + timedelta(hours=6),
        RELEASE_REF, record)
    proc = run_cli("scripts/survey_release_checkpoint_v2.py",
                   "--repo-root", str(ROOT),
                   "--state", str(fix.src / "production-state.json"),
                   "--merge-verification", str(verification),
                   "--release-record", str(record))
    test.assertEqual(proc.returncode, 0, proc.stderr.decode())
    state = core.load_json(fix.src / "production-state.json")
    test.assertEqual(state["lifecycle_state"], "RELEASED")
    test.assertIsNone(state["next_action"])
    test.assertEqual(state["terminal_reason"], "COMPLETE")
    test.assertEqual(agent.validate_agent_state(ROOT, fix.cfg, state), [])
    test.assertTrue(release_cp.is_file())
    return fix, release_cp


def locate_closure_block() -> tuple[str, str]:
    """Fail-closed extraction of the single named closure step run block."""
    text = (ROOT / ".github/workflows/survey-production-v2-release.yml").read_text(
        encoding="utf-8")
    name = "- name: Build immutable Release Record and compact Release Stage Checkpoint"
    assert text.count(name) == 1, "closure step must occur exactly once"
    start = text.find(name)
    following = text.find("- name:", start + len(name))
    assert following != -1, "closure step must be followed by another step"
    step_text = text[start:following]
    run_marker = "run: |"
    assert step_text.count(run_marker) == 1, "closure step needs one run block"
    lines = step_text.split("run: |", 1)[1].splitlines()
    body: list[str] = []
    for line in lines[1:]:
        if line.strip() == "":
            body.append("")
            continue
        if not line.startswith("          ") and line.strip():
            break
        body.append(line[10:] if line.startswith("          ") else line)
    block = "\n".join(body).strip("\n") + "\n"
    assert block.startswith("set -euo pipefail"), "block must be fail-closed"
    assert block.count("python - <<'PY'") == 1, "exactly one heredoc"
    assert "publication.build_release_record" in block
    assert "scripts/survey_release_checkpoint_v2.py" in block
    assert block.count("validate-state") == 1, "exactly one validation call"
    for token in ('--state "$STATE"',
                  '--merge-verification "${SOURCE_ROOT}/publication/v2/merge-verification-v2.json"',
                  '--release-record "${SOURCE_ROOT}/publication/v2/release-record-v2.json"'):
        assert token in block, f"closure block lost exact argv token: {token}"
    for forbidden in ("gh release", "gh pr create", "gh api", "git push",
                      "git switch", "git config user", "actions/checkout",
                      "setup-python", "GITHUB_OUTPUT",
                      "Create or reconcile exact-byte issue-only GitHub Release",
                      "Commit post-release provenance through a normal PR"):
        assert forbidden not in block, f"non-local content in closure block: {forbidden}"
    validation_lines = [ln for ln in block.splitlines() if "validate-state" in ln]
    assert len(validation_lines) == 1, "exactly one validation line"
    return block, validation_lines[0]


class DM004ReleaseValidateStateTests(unittest.TestCase):
    def test_generic_cli_accepts_valid_frozen_and_released(self) -> None:
        # FROZEN control first on a dedicated fixture, then RELEASED.
        frozen_fix = build_to_frozen(self, "POSF")
        state_path, rel, absolute = state_paths(frozen_fix)
        frozen_roots = [frozen_fix.src, frozen_fix.survey]
        with self.subTest(stage="FROZEN-relative"):
            pre = inventory(frozen_roots)
            proc = run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", ".", "validate-state", "--state", rel)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode())
            payload = json.loads(proc.stdout.decode())
            self.assertEqual(
                (payload["valid"], payload["lifecycle_state"],
                 payload["state"]), (True, "FROZEN", rel))
            self.assertEqual(inventory(frozen_roots), pre)
        with self.subTest(stage="FROZEN-absolute"):
            pre = inventory(frozen_roots)
            proc = run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", str(ROOT),
                           "validate-state", "--state", absolute)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode())
            payload = json.loads(proc.stdout.decode())
            self.assertEqual(payload["state"], rel)
            self.assertEqual(inventory(frozen_roots), pre)
        released_fix, _ = build_to_released(self, "POSR")
        rpath, rrel, _ = state_paths(released_fix)
        released_roots = [released_fix.src, released_fix.survey]
        pre = inventory(released_roots)
        proc = run_cli("scripts/survey_agent_control_v2.py",
                       "--repo-root", ".", "validate-state", "--state", rrel)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode())
        payload = json.loads(proc.stdout.decode())
        self.assertEqual(
            (payload["valid"], payload["lifecycle_state"],
             payload["terminal_reason"], payload["state"]),
            (True, "RELEASED", "COMPLETE", rrel))
        self.assertEqual(inventory(released_roots), pre)

    def test_validate_state_rejects_outside_paths(self) -> None:
        fix, _ = build_to_released(self, "ESC")
        state_path, _, _ = state_paths(fix)
        valid_bytes = state_path.read_bytes()
        sib = ESCAPE_BASE / "dm004-escape-ESC"
        self.assertFalse(sib.exists(), f"sibling path not absent: {sib}")
        sib.mkdir()
        drop_sibling(self, sib)
        (sib / "state.json").write_bytes(valid_bytes)
        (sib / "bad.json").write_text("{not json", encoding="utf-8")
        link = fix.src / "escape-link.json"
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(sib / "state.json")
        self.addCleanup(lambda: link.unlink(missing_ok=True))

        def cli(state_arg: str) -> subprocess.CompletedProcess:
            return run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", ".", "validate-state",
                           "--state", state_arg)

        with self.subTest(case="absolute-outside"):
            proc = cli(str(sib / "state.json"))
            self.assertEqual(proc.returncode, 2, proc.stderr.decode())
            self.assertIn(CONTAINMENT_ERROR, proc.stderr.decode())
            self.assertNotIn("Production State invalid", proc.stderr.decode())
            self.assertNotIn(b'"valid": true', proc.stdout)
        with self.subTest(case="repo-relative-escape"):
            proc = cli(f"../dm004-escape-ESC/state.json")
            self.assertEqual(proc.returncode, 2, proc.stderr.decode())
            self.assertIn(CONTAINMENT_ERROR, proc.stderr.decode())
            self.assertNotIn("Production State invalid", proc.stderr.decode())
            self.assertNotIn(b'"valid": true', proc.stdout)
        with self.subTest(case="outside-invalid-json-early"):
            proc = cli("../dm004-escape-ESC/bad.json")
            self.assertEqual(proc.returncode, 2, proc.stderr.decode())
            self.assertIn(CONTAINMENT_ERROR, proc.stderr.decode())
            self.assertNotIn("Production State invalid", proc.stderr.decode())
            self.assertNotIn(b'"valid": true', proc.stdout)
        with self.subTest(case="symlink-escape"):
            proc = cli(str((fix.src / "escape-link.json").relative_to(ROOT)))
            self.assertEqual(proc.returncode, 2, proc.stderr.decode())
            self.assertIn(CONTAINMENT_ERROR, proc.stderr.decode())
            self.assertNotIn(b'"valid": true', proc.stdout)
        self.assertEqual(state_path.read_bytes(), valid_bytes)

    def test_validate_state_accepts_from_other_cwd(self) -> None:
        fix = build_to_frozen(self, "CWD")
        state_path, rel, absolute = state_paths(fix)
        before = state_path.read_bytes()
        sib = ESCAPE_BASE / "dm004-escape-CWD"
        self.assertFalse(sib.exists(), f"sibling path not absent: {sib}")
        sib.mkdir()
        drop_sibling(self, sib)
        pythonpath = {"PYTHONPATH": str(ROOT)}
        controller = str(ROOT / "scripts/survey_agent_control_v2.py")
        with self.subTest(case="repo-relative"):
            proc = run_cli(controller,
                           "--repo-root", str(ROOT),
                           "validate-state", "--state", rel,
                           cwd=sib, extra_env=pythonpath)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode())
            self.assertEqual(json.loads(proc.stdout.decode())["state"], rel)
        with self.subTest(case="absolute-in-repo"):
            proc = run_cli(controller,
                           "--repo-root", str(ROOT),
                           "validate-state", "--state", absolute,
                           cwd=sib, extra_env=pythonpath)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode())
            self.assertEqual(json.loads(proc.stdout.decode())["state"], rel)
        with self.subTest(case="normalized-dotdot-inside"):
            normalized = f"sources/{fix.issue}/../{fix.issue}/production-state.json"
            proc = run_cli(controller,
                           "--repo-root", str(ROOT),
                           "validate-state", "--state", normalized,
                           cwd=sib, extra_env=pythonpath)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode())
            self.assertEqual(json.loads(proc.stdout.decode())["state"], rel)
        self.assertEqual(state_path.read_bytes(), before)

    def test_invalid_states_rejected_with_discriminative_errors(self) -> None:
        fix, checkpoint = build_to_released(self, "NEG")
        state_path, rel, _ = state_paths(fix)
        valid_state = state_path.read_bytes()
        pub = fix.src / "publication" / "v2"
        valid_checkpoint = checkpoint.read_bytes()
        valid_record = (pub / "release-record-v2.json").read_bytes()
        roots = [fix.src, fix.survey]

        def cli() -> subprocess.CompletedProcess:
            return run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", ".", "validate-state", "--state", rel)

        def restore() -> None:
            state_path.write_bytes(valid_state)
            checkpoint.write_bytes(valid_checkpoint)
            (pub / "release-record-v2.json").write_bytes(valid_record)

        cases = [
            ("drifted-release-provenance-sha",
             "checkpoint release provenance SHA drift", True),
            ("removed-release-record",
             "Stage Checkpoint artifact drift: release-record", True),
            ("release-checkpoint-pending", "expected 'passed'", True),
            ("schema-invalid-parseable", "Production State fails", True),
            ("malformed-state-json", None, False),
            ("missing-state-file", None, False),
        ]
        for case, expected_error, semantic_prefix in cases:
            with self.subTest(case=case):
                try:
                    if case == "drifted-release-provenance-sha":
                        doc = json.loads(valid_state.decode())
                        doc["checkpoint_provenance"]["release"]["sha256"] = "0" * 64
                        state_path.write_text(json.dumps(doc), encoding="utf-8")
                    elif case == "removed-release-record":
                        (pub / "release-record-v2.json").rename(
                            pub / "release-record-v2.json.hold")
                    elif case == "release-checkpoint-pending":
                        doc = json.loads(valid_state.decode())
                        doc["machine_checkpoints"]["release"] = "pending"
                        doc["checkpoint_provenance"]["release"] = None
                        doc["lifecycle_state"] = "RELEASED"
                        state_path.write_text(json.dumps(doc), encoding="utf-8")
                    elif case == "schema-invalid-parseable":
                        state_path.write_text(json.dumps(
                            {"schema_version": "2.0-rc1"}), encoding="utf-8")
                    elif case == "malformed-state-json":
                        state_path.write_text("{not json", encoding="utf-8")
                    elif case == "missing-state-file":
                        state_path.rename(fix.src / "production-state.json.bak")
                    pre_inv = inventory(roots)
                    pre_state = (state_path.read_bytes()
                                 if state_path.is_file() else None)
                    proc = cli()
                    err = proc.stderr.decode()
                    self.assertEqual(proc.returncode, 2,
                                     f"{case}: {proc.stdout!r} {err!r}")
                    self.assertNotIn(b'"valid": true', proc.stdout, case)
                    if expected_error is not None:
                        self.assertIn("Production State invalid", err, case)
                        self.assertIn(expected_error, err, case)
                    else:
                        self.assertNotIn("Production State invalid", err, case)
                    # No-write proven BEFORE fixture repair.
                    self.assertEqual(inventory(roots), pre_inv, case)
                    post_state = (state_path.read_bytes()
                                  if state_path.is_file() else None)
                    self.assertEqual(post_state, pre_state, case)
                finally:
                    hold = pub / "release-record-v2.json.hold"
                    if hold.exists():
                        hold.rename(pub / "release-record-v2.json")
                    moved = fix.src / "production-state.json.bak"
                    if moved.exists():
                        moved.rename(state_path)
                    restore()
        self.assertEqual(state_path.read_bytes(), valid_state)
        self.assertEqual(checkpoint.read_bytes(), valid_checkpoint)
        self.assertEqual(
            agent.validate_agent_state(
                ROOT, fix.cfg, core.load_json(state_path)), [])

    def test_cli_contract_refusals_have_no_effects(self) -> None:
        fix, _ = build_to_released(self, "CON")
        state_path, rel, _ = state_paths(fix)
        roots = [fix.src, fix.survey]
        before = inventory(roots)
        with self.subTest(case="unknown-command"):
            proc = run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", ".", "validate-states",
                           "--state", rel)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("invalid choice", proc.stderr.decode())
        with self.subTest(case="missing-required-state"):
            proc = run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", ".", "validate-state")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("--state", proc.stderr.decode())
        with self.subTest(case="rejected-implementation-sha-flag"):
            proc = run_cli("scripts/survey_agent_control_v2.py",
                           "--repo-root", ".", "validate-state",
                           "--state", rel, "--implementation-sha", "0" * 40)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("unrecognized arguments", proc.stderr.decode())
        self.assertEqual(inventory(roots), before)

    def test_extracted_workflow_closure_block_offline(self) -> None:
        block, _ = locate_closure_block()
        fix = build_to_frozen(self, "CLO")
        frozen_state = core.load_json(fix.src / "production-state.json")
        expected_cp = agent.canonical_checkpoint_path(ROOT, fix.cfg, frozen_state)
        self.assertEqual(expected_cp.name, "FROZEN.json")
        pub = fix.src / "publication" / "v2"
        manifest = pub / "release-manifest-v2.json"
        verification = pub / "merge-verification-v2.json"
        record = pub / "release-record-v2.json"
        core_report = pub / "core-stage-contract-v2.json"
        publication.build_merge_verification(
            ROOT, manifest, core.repository_commit_sha(ROOT),
            AT + timedelta(hours=5), verification)
        source_root = str(fix.src.relative_to(ROOT))
        step_env = offline_env({
            "STATE": str((fix.src / "production-state.json").relative_to(ROOT)),
            "SOURCE_ROOT": source_root,
            "MANIFEST": str(manifest.relative_to(ROOT)),
            "RELEASE_URL": RELEASE_REF,
        })
        pre_inv = inventory([fix.src, fix.survey])
        script = ESCAPE_BASE / f"dm004-closure-CLO-{os.getpid()}.sh"
        self.assertFalse(script.exists() or script.is_symlink(),
                         f"closure script path not absent: {script}")
        script.write_text(block, encoding="utf-8")
        self.addCleanup(lambda: script.unlink(missing_ok=True))
        proc = subprocess.run(
            ["bash", str(script)], cwd=str(ROOT), env=step_env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode())
        post_inv = inventory([fix.src, fix.survey])
        added = {k for k in post_inv if k not in pre_inv}
        modified = {k for k in pre_inv
                    if k in post_inv and post_inv[k] != pre_inv[k]}
        removed = {k for k in pre_inv if k not in post_inv}
        state_rel = str((fix.src / "production-state.json").relative_to(ROOT))
        self.assertEqual(added, {
            str(record.relative_to(ROOT)),
            str(core_report.relative_to(ROOT)),
            str(expected_cp.relative_to(ROOT)),
        })
        self.assertEqual(modified, {state_rel})
        self.assertEqual(removed, set())
        final = core.load_json(fix.src / "production-state.json")
        self.assertEqual(final["lifecycle_state"], "RELEASED")
        self.assertIsNone(final["next_action"])
        self.assertEqual(final["terminal_reason"], "COMPLETE")
        self.assertEqual(final["machine_checkpoints"]["release"], "passed")
        authority = final["checkpoint_provenance"]["release"]
        self.assertTrue(expected_cp.is_file())
        self.assertEqual(authority["path"],
                         str(expected_cp.relative_to(ROOT)))
        self.assertEqual(authority["sha256"],
                         core.sha256_file(expected_cp))
        self.assertEqual(agent.validate_agent_state(ROOT, fix.cfg, final), [])

    def test_failfast_uses_extracted_line_on_semantic_invalid(self) -> None:
        _, validation_line = locate_closure_block()
        self.assertIn("validate-state", validation_line)
        self.assertNotIn("gh ", validation_line)
        fix, _ = build_to_released(self, "FF")
        state_path, _, _ = state_paths(fix)
        valid_bytes = state_path.read_bytes()
        drifted = fix.src / "production-state-drifted.json"
        self.assertFalse(drifted.exists())
        doc = json.loads(state_path.read_bytes().decode())
        doc["checkpoint_provenance"]["release"]["sha256"] = "0" * 64
        drifted.write_text(json.dumps(doc), encoding="utf-8")
        self.addCleanup(lambda: drifted.unlink(missing_ok=True))
        roots = [fix.src, fix.survey]
        pre_inv = inventory(roots)
        sentinel = fix.src / "sentinel"
        script = (
            "set -euo pipefail\n"
            f"{validation_line}\n"
            f"touch {sentinel}\n"
        )
        proc = subprocess.run(
            ["bash", "-c", script], cwd=str(ROOT),
            env=offline_env({"PYTHONPATH": ".",
                             "STATE": str(drifted.relative_to(ROOT))}),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = proc.stderr.decode()
        self.assertEqual(proc.returncode, 2, err)
        self.assertIn("checkpoint release provenance SHA drift", err)
        self.assertFalse(sentinel.exists())
        self.assertEqual(inventory(roots), pre_inv)
        self.assertEqual(state_path.read_bytes(), valid_bytes)


if __name__ == "__main__":
    unittest.main()
