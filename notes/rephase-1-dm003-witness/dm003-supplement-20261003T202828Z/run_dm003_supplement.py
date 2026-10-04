"""DM-003 supplemental witness S1/S2/S3 — fixed 222, correction-decision follow-up.

Exactly one scenario per invocation: `supplement.py S1| S2 | S3`.
No default: empty/unknown argv refuses without executing anything.

External to candidate control roots; operates on the independent byte-copy DB
/tmp/opencode/jgas-dm003-witness-20261003T200937Z (222a37e, tree dbabeed).
No shipping changes, commits, network, or generic repair.

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

SCRUB = ("GIT_DIR", "GIT_WORK_TREE", "GIT_CEILING_DIRECTORIES", "GIT_COMMON_DIR",
         "GIT_PREFIX", "GIT_INDEX_FILE")
BASE_ENV = {k: v for k, v in os.environ.items() if k not in SCRUB}
BASE_ENV.update({
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_ALLOW_PROTOCOL": "file",
    "GIT_OPTIONAL_LOCKS": "0",
    "PYTHONDONTWRITEBYTECODE": "1",
})

os.chdir(REPO)
sys.path.insert(0, str(REPO))
sys.dont_write_bytecode = True  # enforce in-process (env may be set too late by callers)
FIXTURE_MOD = REPO / "tests/test_survey_dm001_019_freeze_equivalence_v2.py"
_FIX_SPEC = importlib.util.spec_from_file_location("dm003_supp_fixture", FIXTURE_MOD)
assert _FIX_SPEC is not None and _FIX_SPEC.loader is not None
W = importlib.util.module_from_spec(_FIX_SPEC)
_FIX_SPEC.loader.exec_module(W)

from scripts import survey_agent_control_v2 as agent  # noqa: E402
from scripts import survey_production_v2 as core  # noqa: E402
from scripts import survey_profiled_freeze_v2 as profiled  # noqa: E402
from scripts import survey_publication_v2 as publication  # noqa: E402
from scripts import survey_stage_validation_v2 as stage_validation  # noqa: E402

import scripts.survey_schema_v2 as schema_gate  # noqa: E402


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                            text=True, env=dict(BASE_ENV))
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


BASELINE_SOURCES: dict | None = None


def guard(label: str) -> dict:
    global BASELINE_SOURCES
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    parent = git("rev-parse", "HEAD^")
    branch = git("branch", "--show-current")
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    lines = status.splitlines() if status else []
    tracked = [line for line in lines if not line.startswith("??")]
    sources = {rel: sha256_file(REPO / rel) for rel in SOURCE_PINS}
    if BASELINE_SOURCES is None:
        BASELINE_SOURCES = dict(sources)
    record = {"label": label, "head": head, "tree": tree, "parent": parent,
              "branch": branch, "status_lines": lines, "tracked_changes": tracked,
              "source_hashes": sources}
    assert head == EXPECTED_HEAD, f"{label}: HEAD {head}"
    assert tree == EXPECTED_TREE, f"{label}: tree {tree}"
    assert parent == EXPECTED_PARENT, f"{label}: parent {parent}"
    assert branch == EXPECTED_BRANCH, f"{label}: branch {branch}"
    assert not tracked, f"{label}: tracked changes {tracked}"
    assert sources == BASELINE_SOURCES, f"{label}: source drift"
    return record


def write_once(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "xb") as handle:
        handle.write(data)


def versioned(path: Path) -> Path:
    if not path.exists():
        return path
    n = 2
    while path.with_name(f"{path.stem}-R{n}{path.suffix}").exists():
        n += 1
    return path.with_name(f"{path.stem}-R{n}{path.suffix}")


def save_json(path: Path, payload: object) -> None:
    write_once(path, (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode())


class Supp:
    def __init__(self, sid: str, issue: str, survey_rel: str, day: int) -> None:
        self.sid = sid
        self.issue = issue
        self.survey_rel = survey_rel
        self.day = day
        self.dir = EVIDENCE / sid
        if self.dir.exists():
            n = 2
            while (EVIDENCE / f"{sid}-R{n}").exists():
                n += 1
            self.dir = EVIDENCE / f"{sid}-R{n}"
        self.dir.mkdir(parents=True, exist_ok=False)
        self.ops: list[dict] = []
        self.at = W.T0 + timedelta(days=day)

    def op(self, name: str, outcome: str, detail: str = "") -> None:
        self.ops.append({"op": name, "outcome": outcome, "detail": detail})

    def roots(self) -> list[Path]:
        return [REPO / "sources" / self.issue, REPO / self.survey_rel]

    def inventory(self) -> dict[str, str]:
        inv: dict[str, str] = {}
        for root in self.roots():
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if path.is_file() and not path.is_symlink():
                    inv[str(path.relative_to(REPO))] = sha256_file(path)
        return inv

    def save_inventory(self, name: str) -> dict[str, str]:
        inv = self.inventory()
        save_json(self.dir / f"{name}.inventory.json", inv)
        return inv

    @staticmethod
    def diff(before: dict[str, str], after: dict[str, str]) -> dict:
        added = sorted(set(after) - set(before))
        removed = sorted(set(before) - set(after))
        modified = sorted(p for p in set(before) & set(after) if before[p] != after[p])
        return {"added": added, "removed": removed, "modified": modified}

    def assert_diff(self, name: str, before: dict, after: dict,
                    allowed_added: set[str], allowed_modified: set[str],
                    allowed_removed: set[str] = frozenset()) -> dict:
        got = self.diff(before, after)
        save_json(self.dir / f"{name}.diff.json", got)
        assert set(got["added"]) == set(allowed_added), f"{name} added: {got['added']}"
        assert set(got["modified"]) == set(allowed_modified), f"{name} modified: {got['modified']}"
        assert set(got["removed"]) == set(allowed_removed), f"{name} removed: {got['removed']}"
        self.op(name, "ok", f"added={len(allowed_added)} modified={len(allowed_modified)} "
                f"removed={len(allowed_removed)}")
        return got

    def save_bytes(self, name: str, path: Path) -> dict:
        raw = path.read_bytes()
        entry = {"path": str(path.relative_to(REPO)), "size": len(raw),
                 "sha256": sha256_bytes(raw)}
        write_once(self.dir / f"{name}.bin", raw)
        save_json(self.dir / f"{name}.meta.json", entry)
        return entry

    def new_fixture(self):
        for root in self.roots():
            assert not root.exists(), f"refusing pre-existing fixture path {root}"
        fix = W.SpecialFixture(REPO, self.issue, self.survey_rel)
        self.op("fixture-construct", "ok", f"sources/{self.issue} + {self.survey_rel}")
        return fix

    def orphan(self, fix) -> Path:
        return fix.src / "orchestration" / "v2" / "checkpoints" / "VALIDATED_DRAFT.json"

    def state_file(self, fix) -> Path:
        return fix.src / "production-state.json"

    def cleanup(self, fix) -> None:
        fix.cleanup()
        for root in self.roots():
            assert not root.exists(), f"cleanup left {root}"
        self.op("fixture-cleanup", "ok", "witness-owned dirs removed")

    def freeze_arts(self, fix, candidate: dict) -> dict:
        pub = fix.src / "publication" / "v2"
        return {"freeze-record": pub / "freeze-record-v2.json",
                "release-manifest": pub / "release-manifest-v2.json",
                "visual-review-record": REPO / candidate["visual_review"]["path"]}


def run_s1() -> Supp:
    sc = Supp("S1", "SP-DM003-S1", "surveys/special/SP-DM003-S1", 70)
    save_json(sc.dir / "guard.before.json", guard("S1-before"))
    fix = sc.new_fixture()
    orphan = sc.orphan(fix)
    assert not orphan.exists()
    sc.op("orphan-absent-pre-advance", "ok", "")
    inv0 = sc.save_inventory("s1-00-post-fixture")
    c1_path = W._special_advance_to_rc(fix, sc.at)
    sc.op("advance-to-RC", "ok", "helper asserts RELEASE_CANDIDATE+HUMAN_GATE_REACHED")
    assert orphan.is_file()
    assert core.load_json(orphan)["checkpoints"] == []
    inv1 = sc.save_inventory("s1-01-post-advance")
    sc.save_bytes("s1-state-post-advance", sc.state_file(fix))
    sc.save_bytes("s1-orphan-post-advance", orphan)
    state = core.load_json(sc.state_file(fix))
    assert all((v or {}).get("path") != str(orphan.relative_to(REPO))
               for v in state["checkpoint_provenance"].values())
    sc.op("orphan-unmapped", "ok", "absent from every named provenance ref")
    c1_pre_bytes = c1_path.read_bytes()
    sc.save_bytes("s1-candidate-c1", c1_path)
    W._special_approve(fix, sc.at)
    sc.op("approve-a1", "ok", "real Preview approval")
    named_pre = {k: (dict(v) if v else None)
                 for k, v in core.load_json(sc.state_file(fix))["checkpoint_provenance"].items()}
    inv2 = sc.save_inventory("s1-02-post-approval")
    rel_state = str(sc.state_file(fix).relative_to(REPO))
    rel_appr = str((fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]).relative_to(REPO))
    sc.assert_diff("s1-approval-window", inv1, inv2, {rel_appr}, {rel_state})
    sc.save_bytes("s1-state-post-approval", sc.state_file(fix))
    a1_path = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
    sc.save_bytes("s1-approval-a1", a1_path)
    assert core.load_json(a1_path)["publication_candidate_sha256"] == sha256_bytes(c1_pre_bytes)
    c1 = publication.validate_candidate(REPO, c1_path, issue_id=fix.issue)
    # Genuine byte-distinct second chain over SAME canonical inputs.
    second = W._build_special_second_chain(fix)
    c2_path = second["candidate2"]
    c2 = publication.validate_candidate(REPO, c2_path, issue_id=fix.issue)
    c2_sha, c1_sha = sha256_file(c2_path), sha256_file(c1_path)
    assert c2_sha != c1_sha, "C2 must be byte-distinct"
    assert c2["pdf"]["sha256"] == c1["pdf"]["sha256"], "same PDF bytes required"
    assert str(c2_path) != str(c1_path)
    sc.op("rival-byte-distinct-valid", "ok",
          f"C2 sha={c2_sha[:16]} != C1 sha={c1_sha[:16]}; pdf-sha equal; paths distinct")
    sc.save_bytes("s1-candidate-c2", c2_path)
    state2 = core.load_json(sc.state_file(fix))
    assert {k: (dict(v) if v else None) for k, v in state2["checkpoint_provenance"].items()} == named_pre
    assert c1_path.read_bytes() == c1_pre_bytes, "C1 inputs untouched by second-chain build"
    sc.op("named-pins-untouched", "ok", "checkpoint_provenance + C1 bytes identical")
    inv3 = sc.save_inventory("s1-03-post-second-chain")
    new_files = set(inv3) - set(inv2)
    assert new_files == {
        "sources/SP-DM003-S1/publication/v2/quality-regression-bundle-2-v2.json",
        "sources/SP-DM003-S1/publication/v2/semantic-editorial-review-2-v2.json",
        "sources/SP-DM003-S1/publication/v2/visual-review-2-v2.json",
        "sources/SP-DM003-S1/publication/v2/publication-candidate-2-v2.json",
    }, sorted(new_files)
    sc.op("second-chain-adds-only-4", "ok", "no recognized input rewritten with new bytes")
    # Direct lower-level mismatch, rival outputs.
    pub = fix.src / "publication" / "v2"
    rival_freeze, rival_manifest = pub / "freeze-record-rival.json", pub / "release-manifest-rival.json"
    state_pre = sc.state_file(fix).read_bytes()
    try:
        publication.build_freeze(REPO, c2_path, a1_path, sc.at + timedelta(hours=3),
                                 rival_freeze, rival_manifest)
    except ValueError as exc:
        assert str(exc) == ("Publication Preview approval does not bind the exact "
                            "Publication Candidate being frozen"), str(exc)
        sc.op("direct-freeze-c2-under-a1", "raised-as-expected", f"ValueError: {exc}")
        write_once(sc.dir / "s1-direct-mismatch.traceback.txt",
                   traceback.format_exc().encode())
    else:
        raise AssertionError("direct Freeze(C2,A1) must reject")
    assert not rival_freeze.exists() and not rival_manifest.exists()
    assert sc.state_file(fix).read_bytes() == state_pre
    sc.op("no-writes-on-mismatch", "ok", "rival outputs absent; State identical")
    # Retarget ONLY the unmapped sibling to byte-distinct C2.
    sc.save_bytes("s1-orphan-pre-retarget", orphan)
    record = core.load_json(orphan)
    rows = [r for r in record["artifacts"] if r["name"] != "publication-candidate"]
    rows.append({"name": "publication-candidate", "path": str(c2_path.relative_to(REPO)),
                 "sha256": c2_sha})
    record["artifacts"] = sorted(rows, key=lambda r: r["name"])
    core.write_json(orphan, record)
    sc.save_bytes("s1-orphan-retargeted-c2", orphan)
    try:
        schema_gate.load_and_validate_json(orphan, REPO / agent.CHECKPOINT_SCHEMA,
                                           label="retargeted orphan")
        sc.op("orphan-schema-check", "ok", "schema-valid")
    except Exception as exc:  # noqa: BLE001
        sc.op("orphan-schema-check", "recorded", f"{type(exc).__name__}: {exc}")
    core_report = core.load_json(fix.src / "execution/validated-draft-stage-report.json")
    report_rows = {(r["name"], r["path"], r["sha256"]) for r in core_report["artifacts"]}
    orphan_rows = {(r["name"], r["path"], r["sha256"]) for r in core.load_json(orphan)["artifacts"]}
    save_json(sc.dir / "s1-orphan-vs-report-rows.json",
              {"report": sorted(report_rows), "orphan": sorted(orphan_rows)})
    assert report_rows != orphan_rows
    assert any(n == "publication-candidate" and c2_sha in (p, s)
               for n, p, s in orphan_rows - report_rows)
    sc.op("orphan-transition-inconsistent", "ok", "path AND sha diverge from consumed report")
    # Wrapper for C1, then exact selected-path assertions.
    inv_pre_freeze = sc.save_inventory("s1-04-pre-freeze")
    profiled.build_profiled_freeze(REPO, fix.cfg, sc.state_file(fix), sc.at + timedelta(hours=3))
    sc.op("wrapper-freeze", "ok", "built")
    inv_post_freeze = sc.save_inventory("s1-05-post-freeze")
    sc.assert_diff("s1-freeze-window", inv_pre_freeze, inv_post_freeze,
                   {"sources/SP-DM003-S1/publication/v2/freeze-record-v2.json",
                    "sources/SP-DM003-S1/publication/v2/release-manifest-v2.json"}, set())
    freeze = core.load_json(pub / "freeze-record-v2.json")
    sc.save_bytes("s1-freeze-record", pub / "freeze-record-v2.json")
    sc.save_bytes("s1-manifest", pub / "release-manifest-v2.json")
    assert freeze["publication_candidate_path"] == str(c1_path.relative_to(REPO)), freeze
    assert freeze["publication_candidate_sha256"] == c1_sha, freeze
    sc.op("freeze-winner-path-and-sha", "ok", "record binds exact C1 path+sha, not C2")
    prior = stage_validation._prior_artifacts(REPO, fix.cfg, core.load_json(sc.state_file(fix)))
    sel = prior["publication-candidate"]
    assert sel == c1_path, sel
    assert sha256_file(sel) == c1_sha
    sc.op("prior-selects-c1-path-hash", "ok", f"_prior_artifacts resolves {sel.relative_to(REPO)}")
    # Surplus-key refusal (extra-key guard, not merge).
    arts = sc.freeze_arts(fix, c1)
    arts["publication-candidate"] = c2_path
    try:
        stage_validation.validate_stage(REPO, fix.cfg, sc.state_file(fix), arts,
                                        fix.src / "execution/freeze-stage-report-s1-surplus.json",
                                        sc.at + timedelta(hours=4))
    except stage_validation.StageValidationError as exc:
        assert str(exc) == "unexpected current stage artifacts: publication-candidate", str(exc)
        sc.op("stage-surplus-extra-key", "raised-as-expected", f"StageValidationError: {exc}")
        write_once(sc.dir / "s1-surplus.traceback.txt", traceback.format_exc().encode())
    else:
        raise AssertionError("surplus key must hit the extra-key guard")
    assert not (fix.src / "execution/freeze-stage-report-s1-surplus.json").exists()
    # Correct admission.
    inv_pre_stage = sc.save_inventory("s1-06-pre-stage")
    report = stage_validation.validate_stage(REPO, fix.cfg, sc.state_file(fix),
                                             sc.freeze_arts(fix, c1),
                                             fix.src / "execution/freeze-stage-report-s1.json",
                                             sc.at + timedelta(hours=4))
    assert core.load_json(report)["status"] == "PASS"
    sc.op("stage-admit-c1", "ok", "PASS")
    inv_post_stage = sc.save_inventory("s1-07-post-stage")
    sc.assert_diff("s1-stage-window", inv_pre_stage, inv_post_stage,
                   {"sources/SP-DM003-S1/execution/freeze-stage-report-s1.json"}, set())
    sc.save_bytes("s1-stage-report", report)
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("S1-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_s2() -> Supp:
    sc = Supp("S2", "SP-DM003-S2", "surveys/special/SP-DM003-S2", 71)
    save_json(sc.dir / "guard.before.json", guard("S2-before"))
    fix = sc.new_fixture()
    c1_path = W._special_advance_to_rc(fix, sc.at)
    sc.op("advance-to-RC", "ok", "")
    orphan = sc.orphan(fix)
    assert orphan.is_file()
    sc.save_bytes("s2-orphan-consumed", orphan)
    inv0 = sc.save_inventory("s2-00-post-advance")
    orphan.unlink()
    sc.op("orphan-removed-pre-approval", "ok", "only the consumed unmapped sibling removed")
    inv0b = sc.save_inventory("s2-00b-post-removal")
    sc.assert_diff("s2-removal-window", inv0, inv0b, set(), set(),
                   {"sources/SP-DM003-S2/orchestration/v2/checkpoints/VALIDATED_DRAFT.json"})
    assert agent.validate_agent_state(REPO, fix.cfg, core.load_json(sc.state_file(fix))) == []
    sc.op("state-valid-without-sibling", "ok", "")
    c1 = publication.validate_candidate(REPO, c1_path, issue_id=fix.issue)
    sc.save_bytes("s2-candidate-c1", c1_path)
    W._special_approve(fix, sc.at)
    sc.op("approve-a1", "ok", "")
    inv1 = sc.save_inventory("s2-01-post-approval")
    rel_state = str(sc.state_file(fix).relative_to(REPO))
    rel_appr = str((fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]).relative_to(REPO))
    sc.assert_diff("s2-approval-window", inv0b, inv1, {rel_appr}, {rel_state})
    sc.save_bytes("s2-state-post-approval", sc.state_file(fix))
    sc.save_bytes("s2-approval-a1", fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"])
    profiled.build_profiled_freeze(REPO, fix.cfg, sc.state_file(fix), sc.at + timedelta(hours=3))
    sc.op("wrapper-freeze", "ok", "")
    inv2 = sc.save_inventory("s2-02-post-freeze")
    sc.assert_diff("s2-freeze-window", inv1, inv2,
                   {"sources/SP-DM003-S2/publication/v2/freeze-record-v2.json",
                    "sources/SP-DM003-S2/publication/v2/release-manifest-v2.json"}, set())
    sc.save_bytes("s2-state-post-freeze", sc.state_file(fix))
    sc.save_bytes("s2-freeze-record", fix.src / "publication" / "v2" / "freeze-record-v2.json")
    sc.save_bytes("s2-manifest", fix.src / "publication" / "v2" / "release-manifest-v2.json")
    report = stage_validation.validate_stage(REPO, fix.cfg, sc.state_file(fix),
                                             sc.freeze_arts(fix, c1),
                                             fix.src / "execution/freeze-stage-report-s2.json",
                                             sc.at + timedelta(hours=4))
    assert core.load_json(report)["status"] == "PASS"
    sc.op("stage-admit", "ok", "PASS")
    inv3 = sc.save_inventory("s2-03-post-stage")
    sc.assert_diff("s2-stage-window", inv2, inv3,
                   {"sources/SP-DM003-S2/execution/freeze-stage-report-s2.json"}, set())
    sc.save_bytes("s2-state-post-stage", sc.state_file(fix))
    sc.save_bytes("s2-stage-report", report)
    assert not orphan.exists(), "sibling must not be re-discovered"
    sc.op("orphan-still-absent", "ok", "")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("S2-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


def run_s3() -> Supp:
    sc = Supp("S3", "SP-DM003-S3", "surveys/special/SP-DM003-S3", 72)
    save_json(sc.dir / "guard.before.json", guard("S3-before"))
    fix = sc.new_fixture()
    c1_path = W._special_advance_to_rc(fix, sc.at)
    sc.op("advance-to-RC", "ok", "")
    W._special_approve(fix, sc.at)
    sc.op("approve-a1", "ok", "")
    c1 = publication.validate_candidate(REPO, c1_path, issue_id=fix.issue)
    sc.save_bytes("s3-candidate-c1", c1_path)
    pub = fix.src / "publication" / "v2"
    freeze_out, manifest_out = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
    assert not freeze_out.exists() and not manifest_out.exists()
    sc.op("outputs-initially-absent", "ok", "post-split wrapper tested before any write")
    a1_path = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
    a1 = publication.validate_preview_approval(REPO, a1_path, issue_id=fix.issue)
    rival_approval = fix.src / "gates" / "publication-preview-approval-rival.json"
    publication.build_preview_approval(REPO, c1_path, rival_approval,
                                       "synthetic-human-second", sc.at + timedelta(hours=2, minutes=5),
                                       "synthetic:publication-preview-second")
    a2 = publication.validate_preview_approval(REPO, rival_approval, issue_id=fix.issue)
    assert a2["publication_candidate_sha256"] == sha256_file(c1_path)
    assert a1["approval_id"] != a2["approval_id"]
    sc.op("a1-a2-standalone-valid-distinct", "ok",
          f"A1={a1['approval_id']} A2={a2['approval_id']}; both bind same C1")
    sc.save_bytes("s3-approval-a1", a1_path)
    sc.save_bytes("s3-approval-a2", rival_approval)
    state = core.load_json(sc.state_file(fix))
    sc.save_bytes("s3-state-pre-split", sc.state_file(fix))
    state["human_gate_provenance"]["publication_preview"] = {
        "path": str(rival_approval.relative_to(REPO)), "sha256": sha256_file(rival_approval)}
    core.write_json(sc.state_file(fix), state)
    sc.op("state-split-human-to-a2", "ok", "checkpoint side stays canonical A1")
    sc.save_bytes("s3-state-split", sc.state_file(fix))
    state_errors = agent.validate_agent_state(REPO, fix.cfg, core.load_json(sc.state_file(fix)))
    save_json(sc.dir / "s3-state-errors.json", state_errors)
    assert state_errors == [], state_errors
    sc.op("state-entry-empty", "ok", "validate_agent_state == [] on split refs (current-code behavior)")
    inv_pre_wrapper = sc.save_inventory("s3-00-pre-wrapper")
    wrapper_outcome: dict = {}
    try:
        result = profiled.build_profiled_freeze(REPO, fix.cfg, sc.state_file(fix),
                                                sc.at + timedelta(hours=3))
        wrapper_outcome = {"outcome": "BUILT",
                           "freeze": str(result[0].relative_to(REPO)),
                           "manifest": str(result[1].relative_to(REPO))}
        freeze_rec = core.load_json(result[0])
        wrapper_outcome["frozen_approval_path"] = freeze_rec["publication_preview_approval_path"]
        wrapper_outcome["frozen_approval_sha256"] = freeze_rec["publication_preview_approval_sha256"]
        wrapper_outcome["frozen_candidate_path"] = freeze_rec["publication_candidate_path"]
        wrapper_outcome["frozen_candidate_sha256"] = freeze_rec["publication_candidate_sha256"]
        sc.op("wrapper-after-split", "CHARACTERIZED-BUILT",
              f"built via {wrapper_outcome['frozen_approval_path']}")
    except Exception as exc:  # noqa: BLE001
        wrapper_outcome = {"outcome": "REJECTED", "exc_type": type(exc).__name__,
                           "exc_message": str(exc)}
        sc.op("wrapper-after-split", "CHARACTERIZED-REJECTED",
              f"{type(exc).__name__}: {exc}")
        write_once(sc.dir / "s3-wrapper.traceback.txt", traceback.format_exc().encode())
    save_json(sc.dir / "s3-wrapper-outcome.json", wrapper_outcome)
    inv_post_wrapper = sc.save_inventory("s3-01-post-wrapper")
    wrapper_diff = sc.diff(inv_pre_wrapper, inv_post_wrapper)
    save_json(sc.dir / "s3-wrapper-window.diff.json", wrapper_diff)
    sc.save_bytes("s3-state-post-wrapper", sc.state_file(fix))
    if freeze_out.exists():
        sc.save_bytes("s3-freeze-record", freeze_out)
    if manifest_out.exists():
        sc.save_bytes("s3-manifest", manifest_out)
    sc.op("wrapper-window-recorded", "ok",
          f"added={wrapper_diff['added']} modified={wrapper_diff['modified']} "
          f"removed={wrapper_diff['removed']}")
    # Stage leg on whatever outputs exist.
    if freeze_out.exists() and manifest_out.exists():
        arts = sc.freeze_arts(fix, c1)
        try:
            stage_validation.validate_stage(REPO, fix.cfg, sc.state_file(fix), arts,
                                            fix.src / "execution/freeze-stage-report-s3.json",
                                            sc.at + timedelta(hours=4))
        except stage_validation.StageValidationError as exc:
            assert str(exc) == ("Human Preview and checkpoint approval authorities disagree"), str(exc)
            sc.op("stage-split-rejection", "raised-as-expected", f"StageValidationError: {exc}")
            write_once(sc.dir / "s3-stage.traceback.txt", traceback.format_exc().encode())
        else:
            raise AssertionError("split refs must be rejected at stage entry")
        assert not (fix.src / "execution/freeze-stage-report-s3.json").exists()
        sc.op("no-report-on-rejection", "ok", "")
    else:
        try:
            stage_validation.validate_stage(REPO, fix.cfg, sc.state_file(fix),
                                            sc.freeze_arts(fix, c1),
                                            fix.src / "execution/freeze-stage-report-s3.json",
                                            sc.at + timedelta(hours=4))
        except (stage_validation.StageValidationError, ValueError) as exc:
            sc.op("stage-without-outputs", "characterized",
                  f"{type(exc).__name__}: {exc}")
            write_once(sc.dir / "s3-stage.traceback.txt", traceback.format_exc().encode())
        else:
            raise AssertionError("stage without freeze outputs must not pass")
    sc.cleanup(fix)
    save_json(sc.dir / "guard.after.json", guard("S3-after"))
    save_json(sc.dir / "ops.json", sc.ops)
    return sc


RUNNERS = {"S1": run_s1, "S2": run_s2, "S3": run_s3}


def main() -> int:
    assert sys.version_info[:3] == (3, 12, 14), sys.version
    if len(sys.argv) != 2 or sys.argv[1] not in RUNNERS:
        print("usage: run_dm003_supplement.py S1|S2|S3  (exactly one; no default run)",
              file=sys.stderr)
        return 2
    sid = sys.argv[1]
    save_json(EVIDENCE / "guard.baseline.json", guard("supp-baseline")) \
        if not (EVIDENCE / "guard.baseline.json").exists() else None
    if (EVIDENCE / "guard.baseline.json").exists():
        stored = json.loads((EVIDENCE / "guard.baseline.json").read_bytes())
        fresh = guard("supp-baseline-recheck")
        for key in ("head", "tree", "parent", "branch", "tracked_changes", "source_hashes"):
            assert fresh[key] == stored[key], f"baseline drift: {key}"
    manifest = {"argv": sys.argv, "cwd": os.getcwd(), "repo": str(REPO),
                "python": sys.version,
                "env": {"GIT_NO_LAZY_FETCH": "1", "GIT_ALLOW_PROTOCOL": "file",
                        "GIT_OPTIONAL_LOCKS": "0", "PYTHONDONTWRITEBYTECODE": "1",
                        "scrubbed": list(SCRUB)},
                "expected": {"head": EXPECTED_HEAD, "tree": EXPECTED_TREE,
                             "parent": EXPECTED_PARENT, "branch": EXPECTED_BRANCH},
                "harness_sha256": sha256_file(Path(__file__).resolve()),
                "fixture_module": str(FIXTURE_MOD),
                "fixture_module_sha256": sha256_file(FIXTURE_MOD)}
    save_json(versioned(EVIDENCE / f"run-manifest-{sid}.json"), manifest)
    try:
        sc = RUNNERS[sid]()
        bad = [o for o in sc.ops if o["outcome"] not in
               ("ok", "raised-as-expected", "recorded",
                "CHARACTERIZED-BUILT", "CHARACTERIZED-REJECTED", "characterized")]
        summary = {"status": "COMPLETE", "unexpected": bad}
        rc = 1 if bad else 0
    except Exception:  # noqa: BLE001
        tb = traceback.format_exc()
        tdir = EVIDENCE / f"{sid}-FAILURE"
        tdir.mkdir(parents=True, exist_ok=False)
        write_once(tdir / "SCENARIO-FAILURE.traceback.txt", tb.encode())
        summary = {"status": "SCENARIO-FAILURE", "traceback_tail": tb[-2000:]}
        rc = 1
    save_json(versioned(EVIDENCE / f"summary-{sid}.json"), summary)
    print(json.dumps({sid: summary}, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
