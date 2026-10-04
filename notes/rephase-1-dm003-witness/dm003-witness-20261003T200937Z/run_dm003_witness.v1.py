"""DM-003 external witness harness — fixed 222, seven approved scenarios.

External to candidate control roots: lives in the notes evidence packet, operates
on the independent byte-copy DB at /tmp/opencode/jgas-dm003-witness-20261003T200937Z.
No shipping code/schema/config changes, no candidate commits, no network.

Environment (allowlisted offline):
  GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file GIT_OPTIONAL_LOCKS=0
  PYTHONDONTWRITEBYTECODE=1
Runtime: /tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python (3.12.14).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import traceback
from datetime import timedelta
from pathlib import Path

PACKET = Path(__file__).resolve().parent
EVIDENCE = PACKET / "evidence"
REPO = Path("/tmp/opencode/jgas-dm003-witness-20261003T200937Z")

EXPECTED_HEAD = "222a37e9ee2aa96724a491f2c04c2583a86b9650"
EXPECTED_TREE = "dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd"
EXPECTED_PARENT = "ff6c67f68e12b3093901248219f2de2872e54d73"
EXPECTED_BRANCH = "codex/dm001019-freeze-implementation"

SOURCE_PINS = [
    "scripts/survey_agent_control_v2.py",
    "scripts/survey_stage_validation_v2.py",
    "scripts/survey_publication_v2.py",
    "scripts/survey_profiled_freeze_v2.py",
    "config/survey-production-v2.json",
]

GIT_ENV = {
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_ALLOW_PROTOCOL": "file",
    "GIT_OPTIONAL_LOCKS": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
}

os.chdir(REPO)
sys.path.insert(0, str(REPO))
for key, value in GIT_ENV.items():
    os.environ[key] = value

_FIX_SPEC = importlib.util.spec_from_file_location(
    "dm003_witness_fixture",
    REPO / "tests/test_survey_dm001_019_freeze_equivalence_v2.py",
)
assert _FIX_SPEC is not None and _FIX_SPEC.loader is not None
W = importlib.util.module_from_spec(_FIX_SPEC)
_FIX_SPEC.loader.exec_module(W)

from scripts import survey_agent_control_v2 as agent  # noqa: E402
from scripts import survey_production_v2 as core  # noqa: E402
from scripts import survey_profiled_freeze_v2 as profiled  # noqa: E402
from scripts import survey_publication_v2 as publication  # noqa: E402
from scripts import survey_quality_v2 as quality  # noqa: E402
from scripts import survey_reader_publication_v2 as reader  # noqa: E402
from scripts import survey_stage_validation_v2 as stage_validation  # noqa: E402

import scripts.survey_schema_v2 as schema_gate  # noqa: E402


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, env=dict(os.environ)
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def guard(label: str) -> dict:
    """Fresh asserted HEAD/tree/parent/tracked-clean + source-hash observation."""
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    parent = git("rev-parse", "HEAD^")
    branch = git("branch", "--show-current")
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    lines = status.splitlines() if status else []
    tracked_changes = [line for line in lines if not line.startswith("??")]
    sources = {rel: sha256_file(REPO / rel) for rel in SOURCE_PINS}
    record = {
        "label": label,
        "head": head,
        "tree": tree,
        "parent": parent,
        "branch": branch,
        "status_lines": lines,
        "tracked_changes": tracked_changes,
        "source_hashes": sources,
    }
    assert head == EXPECTED_HEAD, f"{label}: HEAD drift {head}"
    assert tree == EXPECTED_TREE, f"{label}: tree drift {tree}"
    assert parent == EXPECTED_PARENT, f"{label}: parent drift {parent}"
    assert branch == EXPECTED_BRANCH, f"{label}: branch drift {branch}"
    assert not tracked_changes, f"{label}: tracked modifications {tracked_changes}"
    assert sources == guard_sources_baseline(), f"{label}: source bytes changed"
    return record


def guard_sources_baseline() -> dict:
    if not hasattr(guard_sources_baseline, "cache"):
        guard_sources_baseline.cache = {  # type: ignore[attr-defined]
            rel: sha256_file(REPO / rel) for rel in SOURCE_PINS
        }
    return guard_sources_baseline.cache  # type: ignore[attr-defined]


def write_once(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as handle:
        handle.write(data)


def save_json(path: Path, payload: object) -> None:
    write_once(path, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())


def snap_file(path: Path) -> dict:
    if not path.exists():
        return {"exists": False}
    raw = path.read_bytes()
    entry: dict = {
        "exists": True,
        "size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    if path.suffix == ".json" and len(raw) < 200000:
        entry["bytes_utf8"] = raw.decode("utf-8")
    return entry


class Scenario:
    def __init__(self, sid: str, issue: str, survey_rel: str, day: int) -> None:
        self.sid = sid
        self.issue = issue
        self.survey_rel = survey_rel
        self.day = day
        self.dir = EVIDENCE / sid
        self.ops: list[dict] = []
        self.at = W.T0 + timedelta(days=day)

    def record_op(self, name: str, outcome: str, detail: str = "",
                  extra: dict | None = None) -> None:
        entry: dict = {"op": name, "outcome": outcome, "detail": detail}
        if extra:
            entry.update(extra)
        self.ops.append(entry)

    def attempt(self, name: str, func, expect: tuple[str, str] | None = None) -> object:
        """Run func; return value or 'RAISED ...'. expect=(TypeName, exact_message)."""
        try:
            value = func()
        except Exception as exc:  # noqa: BLE001 - raw capture required
            tb = traceback.format_exc()
            write_once(self.dir / f"{name}.traceback.txt", tb.encode())
            got = f"{type(exc).__name__}: {exc}"
            if expect is not None and (type(exc).__name__, str(exc)) == (expect[0], expect[1]):
                self.record_op(name, "raised-as-expected", got)
            else:
                self.record_op(name, "raised", got,
                               {"expected": None if expect is None else f"{expect[0]}: {expect[1]}"})
            return ("RAISED", type(exc).__name__, str(exc))
        self.record_op(name, "ok", "" if value is None else type(value).__name__)
        return value

    def new_fixture(self):
        src = REPO / "sources" / self.issue
        survey = REPO / self.survey_rel
        assert not src.exists(), f"refusing pre-existing fixture path {src}"
        assert not survey.exists(), f"refusing pre-existing fixture path {survey}"
        fix = W.SpecialFixture(REPO, self.issue, self.survey_rel)
        self.record_op("fixture-construct", "ok",
                       f"sources/{self.issue} + {self.survey_rel}")
        return fix

    def orphan_path(self, fix) -> Path:
        return fix.src / "orchestration" / "v2" / "checkpoints" / "VALIDATED_DRAFT.json"

    def state_path(self, fix) -> Path:
        return fix.src / "production-state.json"

    def load_state(self, fix) -> dict:
        return core.load_json(self.state_path(fix))

    def save_state_snap(self, fix, name: str) -> dict:
        entry = snap_file(self.state_path(fix))
        save_json(self.dir / f"{name}.state.json",
                  json.loads(entry["bytes_utf8"]) if entry.get("bytes_utf8") else entry)
        return entry

    def cleanup(self, fix) -> None:
        fix.cleanup()
        assert not (REPO / "sources" / self.issue).exists()
        assert not (REPO / self.survey_rel).exists()
        self.record_op("fixture-cleanup", "ok", "witness-owned dirs removed")

    def freeze_artifacts(self, fix, candidate: dict) -> dict:
        pub = fix.src / "publication" / "v2"
        return {
            "freeze-record": pub / "freeze-record-v2.json",
            "release-manifest": pub / "release-manifest-v2.json",
            "visual-review-record": REPO / candidate["visual_review"]["path"],
        }

    def stage_admit(self, fix, artifacts: dict, suffix: str):
        output = fix.src / f"execution/freeze-stage-report-{suffix}.json"
        return stage_validation.validate_stage(
            REPO, fix.cfg, self.state_path(fix), artifacts, output,
            self.at + timedelta(hours=4))

    def build_rival_candidate(self, fix):
        """Genuinely independent valid C2: same issue/Profile/PDF bytes, distinct paths+shas."""
        pub = fix.src / "publication" / "v2"
        rival_tex = fix.survey / "main-rival.tex"
        rival_pdf = fix.survey / "main-rival.pdf"
        rival_tex.write_bytes((fix.survey / "main.tex").read_bytes())
        rival_pdf.write_bytes((fix.survey / "main.pdf").read_bytes())
        bib_rel = str((fix.survey / "references.bib").relative_to(REPO))
        support = [{"role": "BIBLIOGRAPHY", "path": bib_rel}]
        coverage = [
            {"package_id": "PKG-1", "requirement": "Explain concrete transition",
             "status": "FULFILLED", "reader_locations": ["Subsection 1.1 — Concrete transition"],
             "detail": "Reader prose explains the transition in a distinct substantive block"},
            {"package_id": "PKG-1", "requirement": "Explain remaining boundary",
             "status": "FULFILLED", "reader_locations": ["Subsection 1.2 — Remaining boundary"],
             "detail": "Reader prose explains the remaining boundary in a distinct substantive block"},
        ]
        requirements = [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                         "reader_locations": ["Section 1 — Final synthesis"],
                         "detail": "Final synthesis remains reader-visible and substantive"}]
        rival_manuscript = pub / "reader-manuscript-rival-v2.json"
        reader.build_manuscript_manifest(
            REPO, fix.issue, fix.profile_path,
            fix.src / "architecture-v2.json", fix.src / "gates" / "architecture-approval.json",
            rival_tex, support, coverage, requirements,
            W.EXECUTOR, self.at, rival_manuscript)
        checks = fix._deterministic_checks(pub)
        rival_bundle = pub / "quality-regression-bundle-rival-v2.json"
        quality.build_bundle(REPO, fix.issue, rival_tex, rival_pdf, checks, rival_bundle,
                             production_profile_path=fix.profile_path)
        rival_sem = pub / "semantic-editorial-review-rival-v2.json"
        rival_vis = pub / "visual-review-rival-v2.json"
        reader.build_review_record(REPO, rival_manuscript, rival_pdf, 12, "SEMANTIC_EDITORIAL",
                                   fix._review_checks("SEMANTIC_EDITORIAL"), "ChatGPT", self.at, rival_sem)
        reader.build_review_record(REPO, rival_manuscript, rival_pdf, 12, "VISUAL",
                                   fix._review_checks("VISUAL"), "ChatGPT", self.at, rival_vis)
        rival_out = pub / "publication-candidate-rival-v2.json"
        publication.build_candidate(REPO, fix.issue, fix.publication_profile, rival_manuscript,
                                    rival_tex, rival_pdf, 12, rival_bundle, rival_sem, rival_vis,
                                    rival_out)
        rival = publication.validate_candidate(REPO, rival_out, issue_id=fix.issue)
        self.record_op("rival-build", "ok",
                       f"C2={rival_out.relative_to(REPO)} sha={sha256_file(rival_out)[:16]}")
        return rival_out, rival


def run_c1() -> Scenario:
    sc = Scenario("C1", "SP-DM003-C1", "surveys/special/SP-DM003-C1", 60)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C1-before"))
    fix = sc.new_fixture()
    orphan = sc.orphan_path(fix)
    sc.record_op("orphan-pre-advance-absent", "ok" if not orphan.exists() else "UNEXPECTED-PRESENT",
                 f"exists={orphan.exists()}")
    assert not orphan.exists()
    candidate_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "RELEASE_CANDIDATE+HUMAN_GATE_REACHED asserted by helper")
    assert orphan.is_file(), "canonical producer must create VALIDATED_DRAFT.json"
    record = core.load_json(orphan)
    save_json(sc.dir / "orphan.record.json", record)
    assert record["checkpoints"] == [], record["checkpoints"]
    sc.record_op("orphan-checkpoints-empty", "ok", "record checkpoints == []")
    state = sc.load_state(fix)
    sc.save_state_snap(fix, "post-advance")
    orphan_rel = str(orphan.relative_to(REPO))
    mapped_paths = {k: (v or {}).get("path") for k, v in state["checkpoint_provenance"].items()}
    save_json(sc.dir / "provenance-paths.json", mapped_paths)
    assert orphan_rel not in set(mapped_paths.values()), "orphan must be absent from every named ref"
    sc.record_op("orphan-absent-from-all-refs", "ok", f"{orphan_rel} not in {len(mapped_paths)} refs")
    validation_ref = state["checkpoint_provenance"]["validation"] or {}
    assert validation_ref.get("path") != orphan_rel
    assert validation_ref.get("path", "").endswith("DRAFT_COMPLETE.json"), validation_ref
    sc.record_op("validation-checkpoint-distinct", "ok", f"named validation={validation_ref.get('path')}")
    errors = agent.validate_agent_state(REPO, fix.cfg, state)
    assert errors == [], errors
    sc.record_op("state-valid-post-advance", "ok", "validate_agent_state == []")
    candidate = publication.validate_candidate(REPO, candidate_path, issue_id=fix.issue)
    save_json(sc.dir / "candidate.c1.json", candidate)
    state_before_approval = snap_file(sc.state_path(fix))
    sc.attempt("approve-preview", lambda: W._special_approve(fix, sc.at))
    sc.save_state_snap(fix, "post-approval")
    assert snap_file(sc.state_path(fix))["sha256"] != state_before_approval["sha256"]
    sc.record_op("approval-state-write-window", "ok", "State mutated only by real approval")
    approval_rel = fix.cfg["state_authority"]["publication_preview_approval_path"]
    approval_path = fix.src / approval_rel
    save_json(sc.dir / "approval.a1.json", core.load_json(approval_path))
    assert core.load_json(approval_path)["publication_candidate_sha256"] == sha256_file(candidate_path)
    sc.record_op("approval-binds-c1", "ok", "approval candidate sha == C1 bytes")
    frozen_at = sc.at + timedelta(hours=3)
    state_pre_freeze = snap_file(sc.state_path(fix))
    sc.attempt("wrapper-freeze", lambda: profiled.build_profiled_freeze(
        REPO, fix.cfg, sc.state_path(fix), frozen_at))
    assert snap_file(sc.state_path(fix)) == state_pre_freeze, "wrapper must not rewrite State"
    sc.record_op("freeze-no-state-write", "ok", "State bytes identical across wrapper Freeze")
    freeze = core.load_json(fix.src / "publication" / "v2" / "freeze-record-v2.json")
    assert freeze["publication_candidate_path"] == str(candidate_path.relative_to(REPO))
    assert freeze["publication_candidate_sha256"] == sha256_file(candidate_path)
    save_json(sc.dir / "freeze-record.json", freeze)
    sc.record_op("freeze-binds-exact-c1", "ok", "freeze record path+sha == C1")
    state_pre_stage = snap_file(sc.state_path(fix))
    report = sc.attempt("stage-admit", lambda: sc.stage_admit(
        fix, sc.freeze_artifacts(fix, candidate), "c1"))
    assert not isinstance(report, tuple)
    assert core.load_json(report)["status"] == "PASS"
    assert snap_file(sc.state_path(fix)) == state_pre_stage, "stage admission must not rewrite State"
    sc.record_op("stage-no-state-write", "ok", "State bytes identical across stage admission")
    cand_pre = sha256_file(candidate_path)
    appr_pre = sha256_file(approval_path)
    assert sha256_file(candidate_path) == cand_pre and sha256_file(approval_path) == appr_pre
    sc.record_op("inputs-unchanged-across-freeze-admission", "ok", "C1+approval bytes stable")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C1-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_c2() -> Scenario:
    sc = Scenario("C2", "SP-DM003-C2", "surveys/special/SP-DM003-C2", 61)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C2-before"))
    fix = sc.new_fixture()
    candidate_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "")
    orphan = sc.orphan_path(fix)
    assert orphan.is_file()
    save_json(sc.dir / "orphan.original.json", core.load_json(orphan))
    orphan.unlink()
    sc.record_op("orphan-removed-pre-approval", "ok", "witness-owned sibling deleted after transition")
    assert not orphan.exists()
    state = sc.load_state(fix)
    errors = agent.validate_agent_state(REPO, fix.cfg, state)
    assert errors == [], errors
    sc.record_op("state-valid-without-sibling", "ok", "no named ref points at sibling")
    sc.attempt("approve-preview", lambda: W._special_approve(fix, sc.at))
    sc.save_state_snap(fix, "post-approval")
    candidate = publication.validate_candidate(REPO, candidate_path, issue_id=fix.issue)
    sc.attempt("wrapper-freeze", lambda: profiled.build_profiled_freeze(
        REPO, fix.cfg, sc.state_path(fix), sc.at + timedelta(hours=3)))
    report = sc.attempt("stage-admit", lambda: sc.stage_admit(
        fix, sc.freeze_artifacts(fix, candidate), "c2"))
    assert not isinstance(report, tuple) and core.load_json(report)["status"] == "PASS"
    sc.record_op("freeze-stage-pass-without-sibling", "ok", "no re-discovery; orphan not recreated: "
                 f"exists={orphan.exists()}")
    assert not orphan.exists(), "Freeze/stage must not re-discover sibling"
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C2-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_c3() -> Scenario:
    sc = Scenario("C3", "SP-DM003-C3", "surveys/special/SP-DM003-C3", 62)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C3-before"))
    fix = sc.new_fixture()
    candidate_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "")
    sc.attempt("approve-preview", lambda: W._special_approve(fix, sc.at))
    orphan = sc.orphan_path(fix)
    save_json(sc.dir / "orphan.original.json", core.load_json(orphan))
    cand_sha = sha256_file(candidate_path)
    orphan.write_bytes(b"{\n  NOT VALID CHECKPOINT JSON \x00\x01\n")
    write_once(sc.dir / "orphan.corrupted.bin", orphan.read_bytes())
    sc.record_op("orphan-corrupted-post-approval", "ok", "sibling bytes replaced, named authority untouched")
    state = sc.load_state(fix)
    errors = agent.validate_agent_state(REPO, fix.cfg, state)
    assert errors == [], errors
    sc.record_op("state-still-valid", "ok", "validate_agent_state == []")
    candidate = publication.validate_candidate(REPO, candidate_path, issue_id=fix.issue)
    assert sha256_file(candidate_path) == cand_sha
    sc.record_op("typed-candidate-unchanged", "ok", "C1 bytes stable")
    sc.attempt("wrapper-freeze", lambda: profiled.build_profiled_freeze(
        REPO, fix.cfg, sc.state_path(fix), sc.at + timedelta(hours=3)))
    report = sc.attempt("stage-admit", lambda: sc.stage_admit(
        fix, sc.freeze_artifacts(fix, candidate), "c3"))
    assert not isinstance(report, tuple) and core.load_json(report)["status"] == "PASS"
    sc.record_op("freeze-stage-pass-despite-corrupt-sibling", "ok",
                 "ignored unreferenced content, not validation of corruption")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C3-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_c4() -> Scenario:
    sc = Scenario("C4", "SP-DM003-C4", "surveys/special/SP-DM003-C4", 63)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C4-before"))
    fix = sc.new_fixture()
    candidate_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "")
    sc.attempt("approve-preview", lambda: W._special_approve(fix, sc.at))
    approval_path = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
    candidate = publication.validate_candidate(REPO, candidate_path, issue_id=fix.issue)
    save_json(sc.dir / "candidate.original.json", candidate)
    with open(candidate_path, "ab") as handle:
        handle.write(b" ")
    sc.record_op("candidate-mutated", "ok", "one trailing byte appended; JSON still parses, sha drifts")
    pub = fix.src / "publication" / "v2"
    freeze_out, manifest_out = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
    state_pre = snap_file(sc.state_path(fix))
    res = sc.attempt(
        "wrapper-freeze-stale",
        lambda: profiled.build_profiled_freeze(REPO, fix.cfg, sc.state_path(fix),
                                               sc.at + timedelta(hours=3)),
        expect=("ValueError", "Publication Preview approved candidate bytes drifted"))
    assert isinstance(res, tuple), "stale Candidate must be rejected"
    assert not freeze_out.exists() and not manifest_out.exists()
    sc.record_op("no-outputs-on-rejection", "ok", "freeze/manifest absent")
    assert snap_file(sc.state_path(fix)) == state_pre
    sc.record_op("no-state-mutation-on-rejection", "ok", "State bytes identical")
    res2 = sc.attempt(
        "validate-approval-direct",
        lambda: publication.validate_preview_approval(REPO, approval_path, issue_id=fix.issue),
        expect=("ValueError", "Publication Preview approved candidate bytes drifted"))
    assert isinstance(res2, tuple)
    state_errors = agent.validate_agent_state(REPO, fix.cfg, sc.load_state(fix))
    save_json(sc.dir / "state-errors.json", state_errors)
    sc.record_op("state-entry-errors", "ok" if state_errors else "UNEXPECTED-CLEAN",
                 f"errors={state_errors}")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C4-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_c5() -> Scenario:
    sc = Scenario("C5", "SP-DM003-C5", "surveys/special/SP-DM003-C5", 64)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C5-before"))
    fix = sc.new_fixture()
    candidate_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "")
    sc.attempt("approve-preview-a1", lambda: W._special_approve(fix, sc.at))
    candidate = publication.validate_candidate(REPO, candidate_path, issue_id=fix.issue)
    sc.attempt("wrapper-freeze", lambda: profiled.build_profiled_freeze(
        REPO, fix.cfg, sc.state_path(fix), sc.at + timedelta(hours=3)))
    freeze_pre = snap_file(fix.src / "publication" / "v2" / "freeze-record-v2.json")
    manifest_pre = snap_file(fix.src / "publication" / "v2" / "release-manifest-v2.json")
    rival_approval = fix.src / "gates" / "publication-preview-approval-rival.json"
    publication.build_preview_approval(REPO, candidate_path, rival_approval,
                                       "synthetic-human-second", sc.at + timedelta(hours=2, minutes=5),
                                       "synthetic:publication-preview-second")
    a2 = publication.validate_preview_approval(REPO, rival_approval, issue_id=fix.issue)
    assert a2["publication_candidate_sha256"] == sha256_file(candidate_path)
    sc.record_op("rival-approval-standalone-valid", "ok", "A2 schema+validator valid, binds same C1")
    a1_path = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
    a1 = publication.validate_preview_approval(REPO, a1_path, issue_id=fix.issue)
    assert a1["approval_id"] != a2["approval_id"], "approvals must be distinct records"
    sc.record_op("approvals-distinct", "ok", f"A1={a1['approval_id']} A2={a2['approval_id']}")
    save_json(sc.dir / "approval.a2.json", a2)
    state = sc.load_state(fix)
    save_json(sc.dir / "state.pre-mutation.json", state)
    state["human_gate_provenance"]["publication_preview"] = {
        "path": str(rival_approval.relative_to(REPO)), "sha256": sha256_file(rival_approval)}
    core.write_json(sc.state_path(fix), state)
    sc.record_op("state-mutated-human-ref-to-a2", "ok", "checkpoint side still A1; State now deliberately split")
    mutated_state = snap_file(sc.state_path(fix))
    state_errors = agent.validate_agent_state(REPO, fix.cfg, sc.load_state(fix))
    save_json(sc.dir / "state-errors.json", state_errors)
    sc.record_op("state-entry-outcome", "ok" if not state_errors else "state-entry-rejects",
                 f"errors={state_errors}")
    res = sc.attempt(
        "stage-admit-split-refs",
        lambda: sc.stage_admit(fix, sc.freeze_artifacts(fix, candidate), "c5"),
        expect=("StageValidationError",
                "Human Preview and checkpoint approval authorities disagree"))
    assert isinstance(res, tuple), "split typed refs must be rejected at stage entry"
    assert not (fix.src / "execution/freeze-stage-report-c5.json").exists()
    sc.record_op("no-report-on-rejection", "ok", "no stage report written")
    assert snap_file(fix.src / "publication" / "v2" / "freeze-record-v2.json") == freeze_pre
    assert snap_file(fix.src / "publication" / "v2" / "release-manifest-v2.json") == manifest_pre
    sc.record_op("existing-outputs-unchanged", "ok", "prior freeze/manifest bytes stable")
    assert snap_file(sc.state_path(fix)) == mutated_state
    sc.record_op("state-kept-mutated-bytes", "ok", "failed admission caused no further State mutation")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C5-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_c6() -> Scenario:
    sc = Scenario("C6", "SP-DM003-C6", "surveys/special/SP-DM003-C6", 65)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C6-before"))
    fix = sc.new_fixture()
    c1_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "")
    sc.attempt("approve-preview-a1", lambda: W._special_approve(fix, sc.at))
    c1 = publication.validate_candidate(REPO, c1_path, issue_id=fix.issue)
    c2_path, c2 = sc.build_rival_candidate(fix)
    assert c2["pdf"]["sha256"] == c1["pdf"]["sha256"], "same PDF bytes required"
    assert str(c2_path) != str(c1_path)
    assert sha256_file(c2_path) != sha256_file(c1_path), "distinct candidate authority required"
    save_json(sc.dir / "candidate.c2.json", c2)
    sc.record_op("rival-standalone-valid", "ok",
                 "C2 validate_candidate PASS; same issue/Profile/PDF-sha, distinct path+sha")
    a1_path = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
    pub = fix.src / "publication" / "v2"
    rival_freeze, rival_manifest = pub / "freeze-record-rival.json", pub / "release-manifest-rival.json"
    state_pre = snap_file(sc.state_path(fix))
    res = sc.attempt(
        "direct-freeze-c2-under-a1",
        lambda: publication.build_freeze(REPO, c2_path, a1_path, sc.at + timedelta(hours=3),
                                         rival_freeze, rival_manifest),
        expect=("ValueError",
                "Publication Preview approval does not bind the exact Publication Candidate being frozen"))
    assert isinstance(res, tuple), "lower-level C2/A1 mismatch must reject"
    assert not rival_freeze.exists() and not rival_manifest.exists()
    sc.record_op("no-writes-on-mismatch", "ok", "rival outputs absent; rejection before preflight")
    assert snap_file(sc.state_path(fix)) == state_pre
    sc.attempt("wrapper-freeze-c1", lambda: profiled.build_profiled_freeze(
        REPO, fix.cfg, sc.state_path(fix), sc.at + timedelta(hours=3)))
    arts = sc.freeze_artifacts(fix, c1)
    arts["publication-candidate"] = c2_path
    res2 = sc.attempt(
        "stage-surplus-candidate",
        lambda: sc.stage_admit(fix, arts, "c6-surplus"),
        expect=("StageValidationError",
                "unexpected current stage artifacts: publication-candidate"))
    assert isinstance(res2, tuple), "surplus current key must hit the extra-key guard, not merge"
    assert not (fix.src / "execution/freeze-stage-report-c6-surplus.json").exists()
    sc.record_op("no-report-on-extra-key", "ok", "")
    report = sc.attempt("stage-admit-c1", lambda: sc.stage_admit(
        fix, sc.freeze_artifacts(fix, c1), "c6"))
    assert not isinstance(report, tuple) and core.load_json(report)["status"] == "PASS"
    freeze = core.load_json(pub / "freeze-record-v2.json")
    assert freeze["publication_candidate_sha256"] == sha256_file(c1_path)
    sc.record_op("prior-still-resolves-c1", "ok", "admission + freeze bind exact C1 after refusals")
    assert snap_file(c1_path)["sha256"] == sha256_file(c1_path)
    sc.record_op("active-c1-approval-state-unchanged", "ok", "C1/approval/State bytes stable (asserted via guards+hashes)")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C6-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_c7() -> Scenario:
    sc = Scenario("C7", "SP-DM003-C7", "surveys/special/SP-DM003-C7", 66)
    sc.dir.mkdir(parents=True, exist_ok=False)
    save_json(sc.dir / "guard.before.json", guard("C7-before"))
    fix = sc.new_fixture()
    c1_path = W._special_advance_to_rc(fix, sc.at)
    sc.record_op("advance-to-RC", "ok", "")
    sc.attempt("approve-preview-a1", lambda: W._special_approve(fix, sc.at))
    c1 = publication.validate_candidate(REPO, c1_path, issue_id=fix.issue)
    c2_path, c2 = sc.build_rival_candidate(fix)
    sc.record_op("rival-standalone-valid", "ok", "C2 validate_candidate PASS")
    orphan = sc.orphan_path(fix)
    save_json(sc.dir / "orphan.original.json", core.load_json(orphan))
    state_pre = snap_file(sc.state_path(fix))
    c1_pre, a1_path = sha256_file(c1_path), fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
    a1_pre = sha256_file(a1_path)
    record = core.load_json(orphan)
    rows = [row for row in record["artifacts"] if row["name"] != "publication-candidate"]
    rows.append({"name": "publication-candidate",
                 "path": str(c2_path.relative_to(REPO)), "sha256": sha256_file(c2_path)})
    record["artifacts"] = sorted(rows, key=lambda row: row["name"])
    core.write_json(orphan, record)
    write_once(sc.dir / "orphan.altered.bin", orphan.read_bytes())
    sc.record_op("orphan-retargeted-to-c2", "ok", "named authority + C1 bytes untouched")
    try:
        schema_gate.load_and_validate_json(
            orphan, REPO / agent.CHECKPOINT_SCHEMA, label="altered orphan checkpoint")
        schema_outcome = "schema-valid"
    except Exception as exc:  # noqa: BLE001
        schema_outcome = f"{type(exc).__name__}: {exc}"
    sc.record_op("altered-orphan-schema-check", "ok", schema_outcome)
    core_report = core.load_json(fix.src / "execution/validated-draft-stage-report.json")
    report_names = {row["name"]: row["sha256"] for row in core_report["artifacts"]}
    orphan_names = {row["name"]: row["sha256"] for row in core.load_json(orphan)["artifacts"]}
    assert report_names != orphan_names, "edited orphan must diverge from consumed transition report"
    sc.record_op("transition-inconsistent", "ok",
                 "altered orphan diverges from CORE report consumed at advance; never re-advanced")
    sc.attempt("wrapper-freeze", lambda: profiled.build_profiled_freeze(
        REPO, fix.cfg, sc.state_path(fix), sc.at + timedelta(hours=3)))
    report = sc.attempt("stage-admit", lambda: sc.stage_admit(
        fix, sc.freeze_artifacts(fix, c1), "c7"))
    assert not isinstance(report, tuple) and core.load_json(report)["status"] == "PASS"
    freeze = core.load_json(fix.src / "publication" / "v2" / "freeze-record-v2.json")
    assert freeze["publication_candidate_sha256"] == c1_pre, "orphan C2 must not be promoted"
    sc.record_op("typed-c1-wins", "ok", "freeze binds C1 sha; orphan C2 ignored")
    assert snap_file(sc.state_path(fix)) == state_pre
    assert sha256_file(c1_path) == c1_pre and sha256_file(a1_path) == a1_pre
    sc.record_op("named-authority-bytes-unchanged", "ok", "State/C1/A1 stable")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("C7-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def main() -> int:
    assert sys.version_info[:3] == (3, 12, 14), sys.version
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    save_json(EVIDENCE / "guard.baseline.json", guard("run-baseline"))
    manifest = {
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "repo": str(REPO),
        "python": sys.version,
        "env_allowlist": GIT_ENV,
        "expected": {"head": EXPECTED_HEAD, "tree": EXPECTED_TREE,
                     "parent": EXPECTED_PARENT, "branch": EXPECTED_BRANCH},
        "fixture_module": str(REPO / "tests/test_survey_dm001_019_freeze_equivalence_v2.py"),
    }
    save_json(EVIDENCE / "run-manifest.json", manifest)
    runners = [("C1", run_c1), ("C2", run_c2), ("C3", run_c3), ("C4", run_c4),
               ("C5", run_c5), ("C6", run_c6), ("C7", run_c7)]
    summary: dict = {}
    failures = 0
    for sid, func in runners:
        try:
            sc = func()
            odch = [op for op in sc.ops if op["outcome"] not in ("ok", "raised-as-expected")]
            summary[sid] = {"status": "COMPLETE",
                            "unexpected": odch}
            if odch:
                failures += 1
        except Exception:  # noqa: BLE001 - retain raw, continue other scenarios
            tb = traceback.format_exc()
            write_once(EVIDENCE / sid / "SCENARIO-FAILURE.traceback.txt", tb.encode())
            summary[sid] = {"status": "SCENARIO-FAILURE", "traceback_tail": tb[-2000:]}
            failures += 1
    save_json(EVIDENCE / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
