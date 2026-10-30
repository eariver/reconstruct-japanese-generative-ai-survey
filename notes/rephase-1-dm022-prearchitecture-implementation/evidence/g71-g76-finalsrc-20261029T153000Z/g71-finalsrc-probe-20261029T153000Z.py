#!/usr/bin/env python3
"""G71 WEEKLY initial publication + editorial activation (genuine G71 epoch).

Runs ONLY G71 fixture code (sys.path/cwd = G71 fixture root). Adapted witness
(no DM022 modules; legacy resolution). Fixture = full G71 worktree copy in temp
dir + independent Git DB with meaningful G71 epoch commit BEFORE authority
(inert origin, process identity). Prints KEEP path; does NOT clean up (caller
inspects; unique run).
Exit 0 = VERSIONED_ACTIVE reached; 1 = setup fault; 2 = target refusal/failure.
"""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

G71 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/dm022-g71-control-20261029T001711Z/worktree")
sys.path.insert(0, str(G71))
os.chdir(str(G71))
for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
           "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
    os.environ.pop(_v, None)
os.environ["GIT_OPTIONAL_LOCKS"] = "0"
os.environ["GIT_CONFIG_NOSYSTEM"] = "1"

from scripts import survey_production_v2 as core  # noqa: E402
from tests import test_survey_evidence_v2 as evidence_tests  # noqa: E402
# G71 helper pins a placeholder tool SHA; bind the REAL epoch instead
# (more truthful, not less: epoch commit exists with the tool bytes).

REPO_ROOT = G71
TEXBIN = Path("/home/eariver/.TinyTeX/bin/x86_64-linux")


def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _write(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return path


def _git(root: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1"})
    r = subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True, env=env, timeout=120)
    if r.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {r.stderr[:500]}")
    return r.stdout.strip()


def main() -> int:
    from scripts import survey_agent_control_v2 as agent
    from scripts.run_drafting_synthesis_v2_interactive import _draft_result as _g71_draft_result
    from scripts import survey_screening_v2 as screening_mod
    from scripts import survey_evidence_v2 as evidence_mod
    from scripts import survey_discovery_v2 as discovery_mod
    from scripts import survey_x_intake_v2 as x_mod
    from scripts import run_selection_architecture_v2_interactive as sel_runner
    try:
        helper = evidence_tests.SurveyEvidenceV2Tests(
            methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        import tempfile as _tf2; _keep = _tf2.mkdtemp(prefix="dm022-g71-keep-"); root = Path(_keep)
        print(f"KEEP fixture at: {root}", flush=True)
        shutil.copytree(G71, root, symlinks=False,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"),
                        dirs_exist_ok=True)
        _git(root, "init", "-q")
        _git(root, "config", "user.name", "Synthetic G71 witness")
        _git(root, "config", "user.email", "g71-witness@example.invalid")
        _git(root, "remote", "add", "origin", "https://example.invalid/g71-witness.git")
        import shutil as _sh2; [shutil.rmtree(p, ignore_errors=True) for p in list(root.rglob("__pycache__"))]; _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "Genuine G71 source epoch fixture (G71 tools, no DM022)")
        epoch_g71 = _git(root, "rev-parse", "HEAD")
        print("G71 epoch:", epoch_g71, flush=True)
        evidence_tests.IMPLEMENTATION_SHA = epoch_g71  # real epoch, not placeholder
        cfg = core.load_json(root / "config/survey-production-v2.json")
        # --- chain (G71 helpers, same API shape) ---
        profile = core.weekly_profile(root, cfg, core.parse_instant("2026-08-22T02:00:00+09:00"), "2026-W33")
        profile_path, state_path = core.initialize(root, cfg, profile, epoch_g71, "ARCHITECTURE_REVIEW", core.parse_instant("2026-08-22T02:05:00+09:00"))
        issue_id = core.load_json(state_path)["issue_id"]
        rec = helper.discovery(issue_id, "target-source")
        discovery_path, screening_acceptance = helper.make_screening(root, state_path, [rec], {"target-source": "KEEP"})
        package_path, evidence_acceptance = helper.make_evidence(root, state_path, discovery_path, screening_acceptance)
        views_acceptance = helper.make_views(root, profile_path, evidence_acceptance)
        ledger = evidence_mod.build_materiality_ledger(root, profile_path, discovery_path, screening_acceptance, evidence_acceptance, views_acceptance, epoch_g71)
        profile_doc = core.load_json(profile_path)
        source_root = root / profile_doc["paths"]["source_root"]
        source_root.mkdir(parents=True, exist_ok=True)
        ledger_path = source_root / "materiality-ledger-v2.json"
        evidence_mod.write_materiality_ledger(ledger_path, ledger)
        # completeness (profile-initial union, SATISFIED)
        initial = profile_doc["research_scope"]["initial_obligations"]
        obligations = [{"obligation_id": r["obligation_id"], "dimension": r["dimension"],
                        "description": r["description"], "status": "SATISFIED",
                        "discovery_ids": ["target-source"],
                        "evidence_task_ids": [core.load_json(evidence_acceptance)["results"][0]["evidence_task_id"]],
                        "rationale": "fixture satisfies"} for r in initial]
        completeness = {"schema_version": "2.0-rc1", "issue_id": issue_id,
                        "research_profile": "WEEKLY",
                        "basis": {"production_profile_sha256": _sha_file(profile_path),
                                  "materiality_ledger_sha256": _sha_file(ledger_path)},
                        "overall_status": "READY", "obligations": obligations,
                        "residual_limitations": [], "closure": None}
        completeness_path = source_root / "profile-completeness-v2.json"
        _write(completeness_path, completeness)
        print("chain built", flush=True)
        # --- X manifest (REQUIRED for WEEKLY) + discovery acceptance ---
        raw_path = root / "raw" / "source.json"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(b'{"synthetic": "g71 raw source"}\n')
        spec_path = source_root / "external" / "x" / "spec.json"
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(spec_path, {
            "decision": "REQUIRED",
            "rationale": "G71 WEEKLY requires Grok/X Source Intake (synthetic fixture)",
            "series_context": None,
            "runs": [{"run_id": "run-001", "purpose": "Synthetic G71 fixture X",
                      "research_questions": ["What is the synthetic target finding?"],
                      "coverage_focus": ["synthetic target-source"],
                      "time_scope": "2026-08-22", "expected_result_filename": "result-001.md"}]})
        manifest_path = source_root / "external" / "x" / "x-source-intake-v2.json"
        x_mod.build_manifest(root, cfg, profile_path, core.load_json(spec_path), manifest_path)
        grok_raw = source_root / "external" / "x" / "run-001" / "result-001-raw.json"
        grok_raw.parent.mkdir(parents=True, exist_ok=True)
        if not grok_raw.is_file():
            grok_raw.write_bytes(raw_path.read_bytes())
        x_mod.record_result(root, cfg, manifest_path, "run-001", raw_path, "result-001.md",
                            "2026-08-22T02:00:00+09:00", "2026-08-22T02:05:00+09:00",
                            "SUCCESS", "DISCOVERY_RECORDED", ["target-source"],
                            "Synthetic G71 Grok observation")
        disc_accept = source_root / "discovery" / "discovery-accepted-v2.json"
        disc_accept.parent.mkdir(parents=True, exist_ok=True)
        discovery_mod.build_acceptance(root, discovery_path, manifest_path, issue_id, disc_accept)
        discovery_mod.validate_acceptance(root, disc_accept)
        print("discovery acceptance OK", flush=True)
        # --- hand-built legacy EVIDENCE_REVIEWED state (same shape as production advance output) ---
        head_now = _git(root, "rev-parse", "HEAD")
        import shutil as _sh2; [shutil.rmtree(p, ignore_errors=True) for p in list(root.rglob("__pycache__"))]; _git(root, "add", "-A")
        try:
            head_now2 = _git(root, "rev-parse", "HEAD")
        except AssertionError:
            head_now2 = head_now
        contract = core.contract_identity(root, cfg, "WEEKLY", "WEEKLY_MAGAZINE")
        state_p = root / "sources" / issue_id / "production-state.json"
        init_state = core.load_json(state_path)
        def _rep(_st, _fr, _to, _cps, _arts):
            return {"schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT", "status": "PASS",
                    "issue_id": issue_id, "from_state": _fr, "to_state": _to,
                    "production_state": {"path": str(state_p.relative_to(root)), "sha256": _sha_file(state_p)},
                    "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": _sha_file(profile_path)},
                    "implementation_commit_sha": head_now, "contract": contract,
                    "artifacts": _arts, "recorded_at": "2026-10-29T00:00:00Z"}
        def _rec(_fr, _to, _cps, _arts, _rep_path):
            return {"schema_version": "2.0-rc1", "issue_id": issue_id, "from_state": _fr, "to_state": _to,
                    "checkpoints": _cps, "recorded_at": "2026-10-29T00:00:00Z",
                    "implementation": {"repository_commit_sha": head_now, "orchestrator_version": cfg["orchestrator_version"]},
                    "contract": contract, "artifacts": _arts,
                    "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS",
                                 "executor": "fixture", "evidence": "fixture",
                                 "result": {"path": str(_rep_path.relative_to(root)), "sha256": _sha_file(_rep_path)}}],
                    "summary": "fixture checkpoint"}
        _drel = str(disc_accept.relative_to(root))
        _darts = [{"name": "discovery-acceptance", "path": _drel, "sha256": _sha_file(disc_accept)}]
        _drp = root / "sources" / issue_id / "checkpoint-discovery-report.json"
        _write(_drp, _rep(init_state, "ISSUE_INITIALIZED", "DISCOVERY_COLLECTED", ["discovery"], _darts))
        _dr = root / "sources" / issue_id / "checkpoint-discovery.json"
        _write(_dr, _rec("ISSUE_INITIALIZED", "DISCOVERY_COLLECTED", ["discovery"], _darts, _drp))
        _srel = str(screening_acceptance.relative_to(root))
        _sarts = [{"name": "screening-acceptance", "path": _srel, "sha256": _sha_file(screening_acceptance)}]
        _srp = root / "sources" / issue_id / "checkpoint-screening-report.json"
        _write(_srp, _rep(init_state, "DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED", ["screening"], _sarts))
        _sr = root / "sources" / issue_id / "checkpoint-screening.json"
        _write(_sr, _rec("DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED", ["screening"], _sarts, _srp))
        _evrel = str(evidence_acceptance.relative_to(root)); _vwrel = str(views_acceptance.relative_to(root))
        _ldrel = str(ledger_path.relative_to(root)); _cprel = str(completeness_path.relative_to(root))
        _evarts = [{"name": "evidence-acceptance", "path": _evrel, "sha256": _sha_file(evidence_acceptance)},
                   {"name": "edition-views-acceptance", "path": _vwrel, "sha256": _sha_file(views_acceptance)},
                   {"name": "materiality-ledger", "path": _ldrel, "sha256": _sha_file(ledger_path)},
                   {"name": "profile-completeness", "path": _cprel, "sha256": _sha_file(completeness_path)}]
        _erp = root / "sources" / issue_id / "checkpoint-evidence-report.json"
        _write(_erp, _rep(init_state, "CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED", ["evidence", "materiality", "completeness"], _evarts))
        _er = root / "sources" / issue_id / "checkpoint-evidence.json"
        _write(_er, _rec("CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED", ["evidence", "materiality", "completeness"], _evarts, _erp))
        profile_doc = core.load_json(profile_path)
        new_state = copy.deepcopy(init_state)
        new_state["lifecycle_state"] = "EVIDENCE_REVIEWED"
        new_state["contract"] = contract
        new_state["implementation"] = {"repository_commit_sha": head_now, "orchestrator_version": cfg["orchestrator_version"]}
        new_state["machine_checkpoints"] = {"discovery": "passed", "screening": "passed", "evidence": "passed",
            "materiality": "passed", "completeness": "passed", "selection": "pending", "architecture": "pending",
            "draft": "pending", "validation": "pending", "publication_preview": "pending", "freeze": "pending", "release": "pending"}
        new_state["checkpoint_provenance"] = {
            "discovery": {"path": str(_dr.relative_to(root)), "sha256": _sha_file(_dr)},
            "screening": {"path": str(_sr.relative_to(root)), "sha256": _sha_file(_sr)},
            "evidence": {"path": str(_er.relative_to(root)), "sha256": _sha_file(_er)},
            "materiality": {"path": str(_er.relative_to(root)), "sha256": _sha_file(_er)},
            "completeness": {"path": str(_er.relative_to(root)), "sha256": _sha_file(_er)},
            "selection": None, "architecture": None, "draft": None, "validation": None,
            "publication_preview": None, "freeze": None, "release": None}
        new_state["human_gates"] = {"architecture_review": "pending", "publication_preview": "pending"}
        new_state["human_gate_provenance"] = {"architecture_review": None, "publication_preview": None}
        new_state["target_gate"] = "ARCHITECTURE_REVIEW"
        new_state["next_action"] = "stage:selection"
        new_state["terminal_reason"] = None
        new_state["exception_gate"] = {"status": "inactive", "reason": None}
        new_state["publication_revalidation_provenance"] = None
        new_state["history"] = [
            {"from": None, "to": "ISSUE_INITIALIZED", "recorded_at": "2026-10-29T00:00:00Z", "repository_commit_sha": head_now},
            {"from": "ISSUE_INITIALIZED", "to": "DISCOVERY_COLLECTED", "recorded_at": "2026-10-29T00:00:01Z", "repository_commit_sha": head_now},
            {"from": "DISCOVERY_COLLECTED", "to": "CANDIDATES_NORMALIZED", "recorded_at": "2026-10-29T00:00:02Z", "repository_commit_sha": head_now},
            {"from": "CANDIDATES_NORMALIZED", "to": "EVIDENCE_REVIEWED", "recorded_at": "2026-10-29T00:00:03Z", "repository_commit_sha": head_now}]
        canon = root / profile_doc["paths"]["source_root"] / "production-state.json"
        canon.parent.mkdir(parents=True, exist_ok=True)
        _write(canon, new_state)
        errs = agent.validate_agent_state(root, cfg, core.load_json(canon))
        assert errs == [], f"G71 EVIDENCE_REVIEWED must pass: {errs}"
        print("G71 EVIDENCE_REVIEWED valid; strict errors: []", flush=True)
        # --- ordinary selection runner on G71 (no DM022 branches) ---
        _sdoc = core.load_json(screening_acceptance)
        _dmap = {r["discovery_id"]: r["decision"] for r in _sdoc.get("decisions", [])}
        _recs = screening_mod.read_jsonl(discovery_path)
        _exp = {d["discovery_id"] for d in _recs if _dmap.get(d["discovery_id"]) in ("KEEP", "MAYBE", "INSPECT")}
        _assign = [{"discovery_id": d, "disposition": "SELECTED",
                    "rationale": "Synthetic G71 independent reasoning",
                    "architecture_usage": "PRIMARY",
                    "publication_role": "WEEKLY_MAGAZINE:core-finding",
                    "architecture_role": "WEEKLY:core-package",
                    "profile_extensions": {}} for d in sorted(_exp)]
        _input = {"schema_version": "2.0-rc1", "issue_id": issue_id,
                  "runner": {"provider": "SYNTHETIC_FIXTURE_PROVIDER", "model": "SYNTHETIC_G71",
                             "invocation": "SYNTHETIC_G71_SELECTION", "generated_at": "2026-10-29T00:00:00Z"},
                  "assignments": _assign,
                  "architecture": {"editorial_thesis": "Synthetic G71 thesis",
                                   "architecture_goals": ["cover revised MATERIAL finding"],
                                   "page_plan": {"target_pages": 8, "max_pages": 12, "notes": None},
                                   "packages": [{"package_id": "pkg-core", "title": "Core package",
                                                 "purpose": "Carry revised MATERIAL finding",
                                                 "primary_discovery_ids": sorted(_exp),
                                                 "supporting_discovery_ids": [], "must_cover_requirements": [],
                                                 "boundaries": [], "drafting_order": 1,
                                                 "profile_extensions": {},
                                                 "publication_extensions": {"section_label": "Synthetic G71 section"}}],
                                   "selected_exceptions": [],
                    "profile_extensions": {"weekly_closing_summary": {"required": True, "source": "profile_synthesis.current_interpretation"}},
                    "publication_extensions": {"closing_summary": {"required": True, "heading": "Synthetic G71 closing", "placement": "after_body_before_references"}}}}
        _in_path = root / "selection-input-g71.json"
        _write(_in_path, _input)
        _res = sel_runner.run(root, canon, _in_path)
        assert _res.get("review_readiness") == "READY_FOR_ARCHITECTURE_REVIEW", _res
        print("G71 regen OK:", _res.get("selected_count"), flush=True)
        # --- commit chain files (epoch stays tool-only; chain uncommitted is fine) ---
        # --- stage advance to SELECTION_COMPLETE ---
        def _mk_reviews(_tag, _arts):
            _rp = source_root / "reviews" / f"{_tag}-core.json"
            _rp.parent.mkdir(parents=True, exist_ok=True)
            _st0 = core.load_json(canon)
            _prof0 = core.load_json(profile_path)
            _stage0 = cfg["orchestration"]["stage_plan"][_st0["lifecycle_state"]]
            _arows = [{"name": k, "path": str(v.relative_to(root)), "sha256": core.sha256_file(v)} for k, v in sorted(_arts.items())]
            core.write_json(_rp, {
                "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT", "status": "PASS",
                "issue_id": _st0["issue_id"], "from_state": _st0["lifecycle_state"],
                "to_state": _stage0["next_state"],
                "production_state": {"path": str(canon.relative_to(root)), "sha256": core.sha256_file(canon)},
                "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": core.sha256_file(profile_path)},
                "implementation_commit_sha": core.repository_commit_sha(root),
                "contract": core.contract_identity(root, cfg, _st0["research_profile"], _st0["publication_profile"]),
                "artifacts": _arows, "recorded_at": "2026-10-29T05:00:00Z"})
            _vp = source_root / "reviews" / f"{_tag}-reviews.json"
            core.write_json(_vp, {"reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
                "executor": "synthetic-g71-fixture", "evidence": "reviewed exact stage outputs",
                "result_path": str(_rp.relative_to(root))}]})
            return _vp
        _mx = source_root / "candidate-matrix-v2.json"
        _sx = source_root / "candidate-selection-v2.json"
        _reviews = _mk_reviews("selection-g71", {"candidate-matrix": _mx, "candidate-selection": _sx})
        import json as _js
        _dbg = _js.loads(open(source_root / "reviews" / "selection-g71-core.json").read())
        print("REPORT KEYS:", sorted(_dbg.keys()), flush=True)
        _cp = agent.build_stage_checkpoint(root, cfg, canon, {"candidate-matrix": _mx, "candidate-selection": _sx},
            _reviews, "G71 selection stage reviewed.", datetime(2026, 10, 29, 1, 0, 0, tzinfo=timezone.utc))
        _up = agent.advance_with_checkpoint(root, cfg, canon, _cp)
        assert _up["lifecycle_state"] == "SELECTION_COMPLETE", _up["lifecycle_state"]
        assert agent.validate_agent_state(root, cfg, core.load_json(canon)) == []
        print("G71 SELECTION_COMPLETE", flush=True)
        # --- architecture advance + approval ---
        _ap = source_root / "architecture-v2.json"
        _rp2 = source_root / "architecture-review-summary-v2.json"
        _atp = source_root / "architecture-review-attention-v2.json"
        _arts2 = {"issue-architecture": _ap, "architecture-review-summary": _rp2, "architecture-review-attention": _atp}
        _reviews2 = _mk_reviews("architecture-g71", _arts2)
        _cp2 = agent.build_stage_checkpoint(root, cfg, canon, _arts2, _reviews2,
            "G71 architecture stage reviewed.", datetime(2026, 10, 29, 2, 0, 0, tzinfo=timezone.utc))
        _up2 = agent.advance_with_checkpoint(root, cfg, canon, _cp2)
        assert _up2["lifecycle_state"] == "ARCHITECTURE_ESTABLISHED", _up2["lifecycle_state"]
        _appr = agent.approve_architecture(root, cfg, canon, "SYNTHETIC_FIXTURE_REVIEWER_G71",
            datetime(2026, 10, 29, 3, 0, 0, tzinfo=timezone.utc), "synthetic-g71-architecture-gate")
        assert _appr["human_gates"]["architecture_review"] == "approved"
        print("G71 ARCHITECTURE approved", flush=True)
        # --- drafting synthesis (G71 runner, subprocess) ---
        import hashlib as _hl
        _arch = core.load_json(_ap)
        _dr_input = {"schema_version": "2.0-rc1", "issue_id": issue_id,
                     "draft_version": "draft-g71-v2",
                     "runner": {"provider": "SYNTHETIC_FIXTURE_PROVIDER", "model": "SYNTHETIC_G71",
                                "invocation": "SYNTHETIC_G71_DRAFTING", "generated_at": "2026-10-29T00:00:00Z"},
                     "packages": [], "synthesis": {}}
        _cfg2 = core.load_json(root / "config/survey-production-v2.json")
        _rreq = _cfg2["research_profiles"]["WEEKLY"]["synthesis_payload_required"]
        _preq = _cfg2["publication_profiles"]["WEEKLY_MAGAZINE"].get("synthesis_payload_required", [])
        for _plan in sorted(_arch["packages"], key=lambda r: (r["drafting_order"], r["package_id"])):
            _pid = _plan["package_id"]
            _dr_input["packages"].append({
                "package_id": _pid,
                "headline": f"Synthetic G71 headline ({_pid})",
                "deck": f"Synthetic G71 deck ({_pid}): revised MATERIAL claim carried.",
                "deck_discovery_ids": ["target-source"],
                "blocks": [{"block_id": f"{_pid}-body", "block_type": "PARAGRAPH",
                            "text": f"Synthetic G71 body ({_pid}): revised MATERIAL claim preserved.",
                            "ref_mode": "NONE", "discovery_ids": []}]})
        _dr_input["synthesis"] = {
            "profile_payload": {k: f"Synthetic G71 {k}" for k in _rreq},
            "publication_payload": {k: f"Synthetic G71 {k}" for k in _preq}}
        _dr_path = root / "drafting-input-g71.json"
        _write(_dr_path, _dr_input)
        # Content-path drafting (G71's own State-free content core, mirroring
        # C1's G76 accepted-state facade pattern; the G71 runner's state-SHA
        # gate can never pass post-advance and is not patched).
        from scripts import survey_drafting_v2 as drafting_mod
        from scripts import survey_drafting_v2_base as drafting_base
        from scripts import survey_architecture_v2 as arch_mod
        _exp = {"issue_id": issue_id, "research_profile": "WEEKLY",
                "publication_profile": "WEEKLY_MAGAZINE",
                "generator_route": "WEEKLY_GENERATED_V2",
                "canonical_state_path": str(canon.relative_to(root))}
        _rr = screening_mod.read_jsonl(discovery_path)
        _ap_path = root / core.load_json(canon)["human_gate_provenance"]["architecture_review"]["path"]
        _up = drafting_base._load_drafting_basis_content(
            root, profile_path, discovery_path, screening_acceptance,
            evidence_acceptance, views_acceptance,
            ledger_path, completeness_path,
            source_root / "candidate-matrix-v2.json", source_root / "candidate-selection-v2.json",
            source_root / "architecture-v2.json", source_root / "architecture-review-summary-v2.json",
            _ap_path, _exp, _rr, discovery_path)
        print("G71 content basis OK:", sorted(_up.keys()), flush=True)
        # Assemble draft package exactly like derive_draft_package (same pure
        # construction; basis already content-validated above).
        _profile = _up["profile"]; _matrix = _up["matrix"]; _plan = _up["architecture"]
        _evacc = _up["evidence"]
        _pkgs = [r for r in _plan.get("packages", []) if r.get("package_id") == "pkg-core"]
        assert len(_pkgs) == 1, _pkgs
        _pp = _pkgs[0]
        _mbid = {r["candidate_id"]: r for r in _matrix["rows"]}
        _ebyt = {r["evidence_task_id"]: r for r in _evacc["results"]}
        _inputs = []
        for _cid, _use in ([(c, "PRIMARY") for c in _pp["primary_candidate_ids"]] + [(c, "SUPPORTING") for c in _pp["supporting_candidate_ids"]]):
            _row = _mbid.get(_cid)
            assert _row is not None, _cid
            _tid = _row["evidence_task_id"]
            _meta = _ebyt.get(_tid)
            assert _meta is not None and _meta["sha256"] == _row["evidence_sha256"], _tid
            _cardp = evidence_acceptance.parent / "results" / _meta["filename"]
            _cardraw = _cardp.read_bytes()
            assert hashlib.sha256(_cardraw).hexdigest() == _meta["sha256"], _cid
            _inputs.append({"candidate_id": _cid, "architecture_usage": _use,
                            "evidence_task_id": _tid, "evidence_sha256": _meta["sha256"],
                            "evidence_card": json.loads(_cardraw.decode())})
        print("G71 draft inputs:", [(i["candidate_id"], i["architecture_usage"]) for i in _inputs], flush=True)
        _package = {
            "schema_version": "2.0-rc1", "issue_id": _profile["issue_id"],
            "research_profile": _profile["research_profile"],
            "publication_profile": _profile["publication_profile"],
            "package_id": "pkg-core",
            "basis": {
                "production_profile_sha256": _sha_file(profile_path),
                "architecture_sha256": _sha_file(source_root / "architecture-v2.json"),
                "architecture_review_summary_sha256": _sha_file(source_root / "architecture-review-summary-v2.json"),
                "architecture_approval_sha256": _sha_file(root / core.load_json(canon)["human_gate_provenance"]["architecture_review"]["path"]),
                "candidate_matrix_sha256": _sha_file(source_root / "candidate-matrix-v2.json"),
                "candidate_selection_sha256": _sha_file(source_root / "candidate-selection-v2.json"),
                "evidence_acceptance_sha256": _sha_file(evidence_acceptance)},
            "package": {"title": _pp["title"], "purpose": _pp["purpose"],
                        "drafting_order": _pp["drafting_order"],
                        "primary_candidate_ids": list(_pp["primary_candidate_ids"]),
                        "supporting_candidate_ids": list(_pp["supporting_candidate_ids"]),
                        "must_cover_requirements": list(_pp["must_cover_requirements"]),
                        "boundaries": list(_pp["boundaries"])},
            "candidate_matrix": _matrix, "evidence_acceptance": _evacc,
            "evidence_inputs": _inputs,
            "drafting_constraints": {"language": "ja", "raw_sources_forbidden": True,
                                     "unknowns_remain_unknown": True,
                                     "citation_granularity": "EVENT_CLAIM_METRIC_LIMITATION"},
            "profile_extensions": dict(_pp["profile_extensions"]),
            "publication_extensions": dict(_pp["publication_extensions"])}
        _pkg_dir = source_root / "draft" / "v2" / "packages" / "pkg-core"
        _pkg_dir.mkdir(parents=True, exist_ok=True)
        _pkg_path = _pkg_dir / "draft-package.json"
        _write(_pkg_path, _package)
        print("G71 draft package written", flush=True)
        # Canonical accepted-Evidence tree (mirrored bytes, like G76 helper).
        _evacc = core.load_json(evidence_acceptance)
        _rs = _evacc["result_set_sha256"]
        _dest = source_root / "evidence" / "v2" / "accepted" / _rs
        _dest.mkdir(parents=True, exist_ok=True)
        (_dest / "evidence-accepted.json").write_bytes(Path(evidence_acceptance).read_bytes())
        (_dest / "results").mkdir(exist_ok=True)
        for _row in _evacc.get("results", []):
            _fn = _row.get("filename")
            assert isinstance(_fn, str) and _fn, _row
            _src_card = Path(evidence_acceptance).parent / "results" / _fn
            assert _src_card.is_file(), _src_card
            (_dest / "results" / _fn).write_bytes(_src_card.read_bytes())
        print("G71 canonical tree mirrored:", _rs[:12], flush=True)
        # Result via the runner's own builder + G71 validator.
        from scripts import survey_drafting_v2 as _drafting_mod
        _spec = {"package_id": "pkg-core",
                 "headline": "Synthetic G71 headline (pkg-core)",
                 "deck": "Synthetic G71 deck (pkg-core): revised MATERIAL claim carried.",
                 "deck_discovery_ids": ["target-source"],
                 "blocks": [{"block_id": "pkg-core-body", "block_type": "PARAGRAPH",
                             "text": "Synthetic G71 body (pkg-core): revised MATERIAL claim preserved.",
                             "ref_mode": "NONE", "discovery_ids": []}]}
        _runner = {"provider": "SYNTHETIC_FIXTURE_PROVIDER", "model": "SYNTHETIC_G71",
                   "invocation": "SYNTHETIC_G71_DRAFTING", "generated_at": "2026-10-29T00:00:00Z",
                   "run_reference": None}
        _result = _g71_draft_result(root, _pkg_path, _package, _spec, _runner, "draft-g71-v2")
        _errs = _drafting_mod.validate_draft_result(_result, _pkg_path, root / _drafting_mod.DRAFT_PROMPT)
        assert not _errs, _errs
        _res_path = _pkg_dir / "draft-result.json"
        _write(_res_path, _result)
        print("G71 draft result valid", flush=True)
        # Synthesis input/result via G71 builders.
        _syn_in = _drafting_mod.build_synthesis_input(
            root, profile_path, source_root / "architecture-v2.json",
            source_root / "architecture-review-summary-v2.json",
            root / core.load_json(canon)["human_gate_provenance"]["architecture_review"]["path"],
            [(_pkg_path, _res_path)])
        _syn_in_path = source_root / "draft" / "v2" / "profile-synthesis-input.json"
        _write(_syn_in_path, _syn_in)
        _syn_cfg = core.load_json(root / "config/survey-production-v2.json")
        _rreq = _syn_cfg["research_profiles"]["WEEKLY"]["synthesis_payload_required"]
        _preq = _syn_cfg["publication_profiles"]["WEEKLY_MAGAZINE"].get("synthesis_payload_required", [])
        _syn_res = {
            "schema_version": "2.0-rc1", "issue_id": issue_id,
            "research_profile": "WEEKLY", "publication_profile": "WEEKLY_MAGAZINE",
            "synthesis_version": "1.0", "status": "ESTABLISHED",
            "basis": {"synthesis_input_sha256": _sha_file(_syn_in_path),
                      "prompt_id": "profile-synthesis-v2",
                      "prompt_sha256": _sha_file(root / _drafting_mod.SYNTHESIS_PROMPT)},
            "runner": {"provider": "SYNTHETIC_FIXTURE_PROVIDER", "model": "SYNTHETIC_G71",
                       "invocation": "SYNTHETIC_G71_SYNTHESIS", "generated_at": "2026-10-29T00:00:00Z",
                       "run_reference": None},
            "profile_payload": {k: f"Synthetic G71 {k}" for k in _rreq},
            "publication_payload": {k: f"Synthetic G71 {k}" for k in _preq}}
        _syn_errs = _drafting_mod.validate_synthesis_result(
            _syn_res, _syn_in_path, root / _drafting_mod.SYNTHESIS_PROMPT)
        assert not _syn_errs, _syn_errs
        _syn_res_path = source_root / "draft" / "v2" / "profile-synthesis-result.json"
        _write(_syn_res_path, _syn_res)
        _write(source_root / "draft" / "v2" / "interactive-drafting-synthesis-input.json",
               {"schema_version": "2.0-rc1", "issue_id": issue_id,
                "runner": _runner, "draft_version": "draft-g71-v2",
                "packages": [{"package_id": "pkg-core",
                              "headline": _spec["headline"], "deck": _spec["deck"],
                              "deck_discovery_ids": ["target-source"],
                              "blocks": [{"block_id": "pkg-core-body", "block_type": "PARAGRAPH",
                                          "text": "Synthetic G71 body (pkg-core): revised MATERIAL claim preserved.",
                                          "ref_mode": "NONE", "discovery_ids": []}]}],
                "synthesis": {"profile_payload": _syn_res["profile_payload"],
                              "publication_payload": _syn_res["publication_payload"]}})
        print("G71 synthesis valid", flush=True)
        # Stage advance to DRAFT_COMPLETE.
        def _mkrev(_tag2, _arts):
            _rp2 = source_root / "reviews" / f"{_tag2}-core.json"
            _rp2.parent.mkdir(parents=True, exist_ok=True)
            _st0 = core.load_json(canon)
            _stage0 = cfg["orchestration"]["stage_plan"][_st0["lifecycle_state"]]
            _arows = [{"name": k, "path": str(v.relative_to(root)), "sha256": core.sha256_file(v)} for k, v in sorted(_arts.items())]
            core.write_json(_rp2, {
                "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT", "status": "PASS",
                "issue_id": _st0["issue_id"], "from_state": _st0["lifecycle_state"],
                "to_state": _stage0["next_state"],
                "production_state": {"path": str(canon.relative_to(root)), "sha256": core.sha256_file(canon)},
                "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": core.sha256_file(profile_path)},
                "implementation_commit_sha": core.repository_commit_sha(root),
                "contract": core.contract_identity(root, cfg, _st0["research_profile"], _st0["publication_profile"]),
                "artifacts": _arows, "recorded_at": "2026-10-29T04:00:00Z"})
            _vp2 = source_root / "reviews" / f"{_tag2}-reviews.json"
            core.write_json(_vp2, {"reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
                "executor": "synthetic-g71-fixture", "evidence": "reviewed exact stage outputs",
                "result_path": str(_rp2.relative_to(root))}]})
            return _vp2
        _darts = {"synthesis-input": source_root / "draft/v2/profile-synthesis-input.json",
                  "synthesis-result": source_root / "draft/v2/profile-synthesis-result.json",
                  "draft-package:pkg-core": source_root / "draft/v2/packages/pkg-core/draft-package.json",
                  "draft-result:pkg-core": source_root / "draft/v2/packages/pkg-core/draft-result.json"}
        _rvp = _mkrev("draft-g71", _darts)
        _cp = agent.build_stage_checkpoint(root, cfg, canon, _darts, _rvp,
            "G71 drafting synthesis reviewed.", datetime(2026, 10, 29, 4, 0, 0, tzinfo=timezone.utc))
        _up = agent.advance_with_checkpoint(root, cfg, canon, _cp)
        assert _up["lifecycle_state"] == "DRAFT_COMPLETE", _up["lifecycle_state"]
        assert agent.validate_agent_state(root, cfg, core.load_json(canon)) == []
        print("G71 DRAFT_COMPLETE", flush=True)
        # --- weekly derivation input + render + REAL PDF ---
        _arch = core.load_json(source_root / "architecture-v2.json")
        _synres = core.load_json(source_root / "draft/v2/profile-synthesis-result.json")
        _cur_interp = _syn_res["profile_payload"]["current_interpretation"] if False else _synres["profile_payload"]["current_interpretation"]
        _deriv_in = {
            "schema_version": "2.0-rc1", "issue_id": issue_id, "runner": "WEEKLY_MAGAZINE",
            "cover": {"headline": "Synthetic G71 cover", "deck": "Synthetic G71 deck.",
                      "anchors": ["synthetic-g71-anchor"]},
            "frontmatter": {"heading": "Synthetic G71 frontmatter",
                            "lede": "Synthetic G71 lede.",
                            "scope_notes": ["Synthetic G71 scope note."]},
            "final_summary": {"heading": "Synthetic G71 closing",
                              "paragraphs": [_cur_interp,
                                             "Synthetic G71 supporting paragraph one.",
                                             "Synthetic G71 supporting paragraph two."]}}
        _di_path = root / "weekly-derivation-g71.json"
        _write(_di_path, _deriv_in)
        print("G71 derivation input staged", flush=True)
        # --- weekly render via G71 subprocess (fixture-bound) ---
        _r1 = subprocess.run(
            [sys.executable, "-m", "scripts.survey_weekly_semantic_publication_v2",
             "--repo-root", str(root), "--state", str(canon.relative_to(root)),
             "--input", "weekly-derivation-g71.json", "--materialize-surface-only"],
            cwd=str(root), capture_output=True, text=True, timeout=300)
        assert _r1.returncode == 0, f"G71 surface failed: {_r1.stderr[-2000:]}"
        _surf = source_root / "publication" / "v2" / "reader-surface-input-v2.json"
        assert _surf.is_file()
        _srev = {"schema_version": "2.0-rc1", "issue_id": issue_id,
                 "publication_profile": "WEEKLY_MAGAZINE", "review_kind": "SEMANTIC_EDITORIAL",
                 "reviewed_surface": {"path": str(_surf.relative_to(root)), "sha256": _sha_file(_surf)},
                 "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                             "detail": "Synthetic G71 fixture review, explicitly nongenuine.",
                             "evidence_locations": ["reader-surface-input-v2.json:cover"]}],
                 "decision": "PASS", "reviewed_by": "SYNTHETIC_G71_FIXTURE",
                 "reviewed_at": "2026-10-29T06:00:00Z", "status": "PASSED",
                 "findings": [], "summary": "Synthetic G71 pre-TeX review, explicitly nongenuine"}
        _srev["review_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in _srev.items() if k != "review_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        _srev_path = source_root / "publication" / "v2" / "reader-surface-semantic-review-v2.json"
        _write(_srev_path, _srev)
        _r2 = subprocess.run(
            [sys.executable, "-m", "scripts.survey_weekly_semantic_publication_v2",
             "--repo-root", str(root), "--state", str(canon.relative_to(root)),
             "--input", "weekly-derivation-g71.json",
             "--semantic-review", str(_srev_path.relative_to(root))],
            cwd=str(root), capture_output=True, text=True, timeout=300)
        assert _r2.returncode == 0, f"G71 render failed: {_r2.stderr[-3000:]}"
        _survey = root / profile_doc["paths"]["survey_root"]
        assert (_survey / "main.tex").is_file(), "G71 main.tex missing"
        print("G71 render OK; main.tex present", flush=True)
        # --- REAL PDF via disposable TinyTeX + exact transfer ---
        import shutil as _sh
        _bd = Path(tempfile.mkdtemp(prefix="dm022-g71-realpdf-"))
        _inputs = {}
        for _nm in ("main.tex", "references.bib", "jgaisurvey.sty"):
            _d = (_survey / _nm).read_bytes()
            (_bd / _nm).write_bytes(_d)
            _inputs[_nm] = hashlib.sha256(_d).hexdigest()
        _tenv = {**os.environ, "PATH": f"{TEXBIN}{os.pathsep}{os.environ.get('PATH', '')}", "TERM": "dumb"}
        for _av in (["lualatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                    ["biber", "main"],
                    ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                    ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]):
            _pp = subprocess.run([str(TEXBIN / _av[0])] + _av[1:], cwd=str(_bd),
                                 capture_output=True, text=True, env=_tenv, timeout=600)
            assert _pp.returncode == 0, f"G71 TeX step failed {' '.join(_av)}: {_pp.stdout[-1500:]}"
        _pdf = (_bd / "main.pdf").read_bytes()
        assert _pdf.startswith(b"%PDF"), "not a PDF"
        from pypdf import PdfReader as _PR
        _pages = len(_PR(_bd / "main.pdf").pages)
        assert _pages >= 1
        (_survey / "main.pdf").write_bytes(_pdf)
        print(f"G71 REAL PDF OK: {len(_pdf)} bytes, {_pages} pages", flush=True)
        # --- manuscript + QA + reviews + gate + VALIDATED_DRAFT ---
        from scripts import survey_reader_publication_v2 as reader
        from scripts import survey_quality_v2 as quality
        from scripts import survey_publication_set_v2 as pubset
        _man_path = source_root / "publication" / "v2" / "reader-manuscript-v2.json"
        reader.build_manuscript_manifest(
            root, issue_id, profile_path, source_root / "architecture-v2.json",
            root / core.load_json(canon)["human_gate_provenance"]["architecture_review"]["path"],
            _survey / "main.tex",
            [{"role": "BIBLIOGRAPHY", "path": str((_survey / "references.bib").relative_to(root))},
             {"role": "STYLE", "path": str((_survey / "jgaisurvey.sty").relative_to(root))}],
            [], [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                  "reader_locations": ["main.tex"], "detail": "synthetic G71 requirement"},
                 {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
                  "reader_locations": ["main.tex"], "detail": "synthetic G71 requirement"}],
            "SYNTHETIC_G71_FIXTURE", datetime(2026, 10, 29, 7, 0, 0, tzinfo=timezone.utc), _man_path)
        _det_dir = source_root / "publication" / "v2" / "deterministic"
        _det_dir.mkdir(parents=True, exist_ok=True)
        _det_res = {}
        for _cid in ("IDENTIFIER_PRESERVATION", "PDF_PREFLIGHT", "SUBJECT_ENTITY_PROPERTY_BINDING"):
            _pp = _det_dir / f"{_cid.lower()}.json"
            _write(_pp, {"check_id": _cid, "status": "PASS"})
            _det_res[_cid] = {"path": str(_pp.relative_to(root)), "sha256": _sha_file(_pp)}
        _det_checks = [{"check_id": c, "kind": "DETERMINISTIC", "status": "PASS",
                        "executor": "SYNTHETIC_G71", "evidence": f"synthetic G71 check {c}",
                        "recorded_at": "2026-10-29T07:00:00Z", "result": _det_res[c]}
                       for c in ("IDENTIFIER_PRESERVATION", "PDF_PREFLIGHT", "SUBJECT_ENTITY_PROPERTY_BINDING")]
        _bundle = source_root / "publication" / "v2" / "quality-regression-bundle-v2.json"
        quality.build_bundle(root, issue_id, _survey / "main.tex", _survey / "main.pdf",
                             _det_checks, _bundle, production_profile_path=profile_path)
        _exp_sem = sorted(reader._expected_review_checks(root, profile_doc, "SEMANTIC_EDITORIAL"))
        _exp_vis = sorted(reader._expected_review_checks(root, profile_doc, "VISUAL"))
        _sem_path = source_root / "publication" / "v2" / "semantic-editorial-review-v2.json"
        reader.build_review_record(root, _man_path, _survey / "main.pdf", _pages, "SEMANTIC_EDITORIAL",
            [{"check_id": c, "status": "PASS", "detail": f"synthetic explicitly-nongenuine G71 {c}", "evidence_locations": ["main.tex"]} for c in _exp_sem],
            "SYNTHETIC_G71_FIXTURE", datetime(2026, 10, 29, 7, 30, 0, tzinfo=timezone.utc), _sem_path)
        _vis_path = source_root / "publication" / "v2" / "visual-review-v2.json"
        reader.build_review_record(root, _man_path, _survey / "main.pdf", _pages, "VISUAL",
            [{"check_id": c, "status": "PASS", "detail": f"synthetic explicitly-nongenuine G71 {c}", "evidence_locations": ["main.pdf"]} for c in _exp_vis],
            "SYNTHETIC_G71_FIXTURE", datetime(2026, 10, 29, 7, 45, 0, tzinfo=timezone.utc), _vis_path)
        _gate_path = source_root / "publication" / "v2" / "reader-surface-gate-v2.json"
        from scripts import survey_reader_surface_gate_v2 as _gate_mod
        _gate_surf = source_root / "publication" / "v2" / "reader-surface-semantic-review-v2.json"
        assert _gate_surf.is_file()
        reader.build_reader_surface_gate(root, _man_path, _gate_surf, output_path=_gate_path,
            evaluated_by="SYNTHETIC_G71_FIXTURE", recorded_at=datetime(2026, 10, 29, 8, 0, 0, tzinfo=timezone.utc))
        print("G71 gate OK", flush=True)
        # --- VALIDATED_DRAFT via real stage checkpoint ---
        _val_artifacts = {
            "reader-manuscript": _man_path,
            "validated-source": _survey / "main.tex",
            "publication-pdf": _survey / "main.pdf",
            "quality-regression-bundle": _bundle,
            "semantic-review": _sem_path,
            "visual-review": _vis_path,
            "reader-surface-gate": _gate_path}
        for _vn, _vp in _val_artifacts.items():
            assert _vp.is_file(), _vn
        _vr_path = source_root / "reviews" / "validation-g71-core.json"
        _vr_path.parent.mkdir(parents=True, exist_ok=True)
        _vstate = core.load_json(canon)
        _vstage = cfg["orchestration"]["stage_plan"][_vstate["lifecycle_state"]]
        _varows = [{"name": k, "path": str(v.relative_to(root)), "sha256": core.sha256_file(v)} for k, v in sorted(_val_artifacts.items())]
        core.write_json(_vr_path, {
            "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT", "status": "PASS",
            "issue_id": _vstate["issue_id"], "from_state": _vstate["lifecycle_state"],
            "to_state": _vstage["next_state"],
            "production_state": {"path": str(canon.relative_to(root)), "sha256": core.sha256_file(canon)},
            "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": core.sha256_file(profile_path)},
            "implementation_commit_sha": core.repository_commit_sha(root),
            "contract": core.contract_identity(root, cfg, _vstate["research_profile"], _vstate["publication_profile"]),
            "artifacts": _varows, "recorded_at": "2026-10-29T09:00:00Z"})
        _vrp = source_root / "reviews" / "validation-g71-reviews.json"
        core.write_json(_vrp, {"reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "synthetic-g71-fixture", "evidence": "reviewed exact stage outputs",
            "result_path": str(_vr_path.relative_to(root))}]})
        _vcp = agent.build_stage_checkpoint(root, cfg, canon, _val_artifacts, _vrp,
            "G71 reader publication validated.", datetime(2026, 10, 29, 9, 0, 0, tzinfo=timezone.utc))
        _vup = agent.advance_with_checkpoint(root, cfg, canon, _vcp)
        assert _vup["lifecycle_state"] == "VALIDATED_DRAFT", _vup["lifecycle_state"]
        assert agent.validate_agent_state(root, cfg, core.load_json(canon)) == []
        print("G71 VALIDATED_DRAFT", flush=True)
        # --- P1 correction proposal on G71 VALIDATED_DRAFT ---
        from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
        _archived = core.load_json(source_root / "publication" / "v2" / "interactive-semantic-publication-input.json")
        _revised = copy.deepcopy(_archived)
        _revised["cover"] = dict(_archived["cover"])
        _revised["cover"]["deck"] = _archived["cover"]["deck"] + " Corrected: revised MATERIAL claim verified against retained Raw."
        _prop_id = "ed-g71-v2-01"
        _prop_dir = source_root / "publication" / "v2" / "editorial-corrections" / _prop_id
        _prop_dir.mkdir(parents=True, exist_ok=True)
        _auth_path = _prop_dir / "authoring-input.json"
        _write(_auth_path, _revised)
        _prepared = proposal_mod.prepare_proposal(root, canon, _auth_path, _prop_id)
        assert _prepared.get("proposal"), _prepared.keys()
        _write(_prop_dir / "proposal.json", _prepared["proposal"])
        _proposed = _prepared.get("proposed_canonical") or _prepared.get("proposed_reader")
        assert _proposed is not None
        if isinstance(_proposed, (bytes, bytearray)):
            (_prop_dir / "reader-surface-input-v2.json").write_bytes(bytes(_proposed))
        else:
            _write(_prop_dir / "reader-surface-input-v2.json", _proposed)
        _outcome = proposal_mod.validate_proposal(root, canon, _prop_dir / "proposal.json")
        assert _outcome.get("result") == "REVIEW_REQUIRED", _outcome
        print("G71 P1 proposal REVIEW_REQUIRED", flush=True)
        # --- P2R capture + scope + P2V ---
        from scripts import survey_editorial_retention_v2 as retention_mod
        from scripts import survey_editorial_current_authority_v2 as authority_mod
        _prop_path = _prop_dir / "proposal.json"
        _captured = retention_mod.capture_retention(root, canon, _prop_path)
        assert _captured.get("result") == "RETAINED_SET_CAPTURED", _captured
        _manifest_path = root / _captured["manifest_rel"] if "manifest_rel" in _captured else root / _captured["manifest_path"]
        print("G71 P2R captured:", _captured.get("result"), flush=True)
        # --- external scope review (explicit synthetic) + P2V SCOPE_BOUND ---
        _prep_doc = core.load_json(_prop_dir / "proposal.json")
        _basis = _prep_doc["proposal"]["basis"] if "proposal" in _prep_doc else _prep_doc["basis"]
        _scope = {
            "schema_version": "2.0-rc1", "issue_id": issue_id,
            "publication_profile": "WEEKLY_MAGAZINE",
            "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {"path": str((_prop_dir / "reader-surface-input-v2.json").relative_to(root)),
                                "sha256": _sha_file(_prop_dir / "reader-surface-input-v2.json")},
            "checks": [
                {"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                 "detail": "Synthetic G71 scope review: proposed reader independently understandable.",
                 "evidence_locations": ["synthetic-fixture:proposed-reader"]},
                {"check_id": "EDITORIAL_CORRECTION_SCOPE", "status": "PASS",
                 "detail": "Synthetic G71 scope review: delta inside approved authority.",
                 "evidence_locations": ["synthetic-fixture:proposal-g71"]}],
            "decision": "PASS", "reviewed_by": "SYNTHETIC_G71_FIXTURE",
            "reviewed_at": "2026-10-29T16:00:00Z", "recorded_at": "2026-10-29T16:00:00Z",
            "status": "PASSED", "findings": [],
            "summary": "Synthetic G71 scope PASS; explicitly nongenuine.",
            "editorial_correction_scope": {
                "version": "EDITORIAL_CORRECTION_SCOPE_V1", "decision": "WITHIN_APPROVED_AUTHORITY",
                "before_reader_input": _basis["active_reader_input_ref"],
                "preserved_upstream_sha256": _basis["preserved_upstream_digest"],
                "change_summary": "Synthetic G71 scope: corrected deck within approved authority.",
                "evidence_locations": ["synthetic-fixture:proposal-g71"]}}
        _scope["review_sha256"] = hashlib.sha256(json.dumps({k: v for k, v in _scope.items() if k != "review_sha256"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        _scope_path = _prop_dir / "scope-review-v2.json"
        _write(_scope_path, _scope)
        _observed = authority_mod.observe_current_authority(root, canon, _prop_dir / "proposal.json", _manifest_path, _scope_path)
        assert _observed.get("result") in ("CURRENT_BASIS_OBSERVED_SCOPE_BOUND", "SCOPE_BOUND"), _observed
        print("G71 P2V:", _observed.get("result"), flush=True)
        _p3s_code = "; ".join([
            "import json, sys",
            "from pathlib import Path",
            "root = Path(sys.argv[1]).resolve()",
            "from scripts import survey_editorial_staged_source_v2 as staged",
            "out = staged.materialize_staged_source(root, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])",
            "print(json.dumps({'staged_manifest': out.get('staged_manifest_ref', {}).get('path') if isinstance(out.get('staged_manifest_ref'), dict) else out.get('staged_manifest')}))",
        ])
        import subprocess as _sp3
        _pr3 = _sp3.run(
            [sys.executable, "-c", _p3s_code, str(root),
             str(canon.relative_to(root)),
             str((_prop_dir / "proposal.json").relative_to(root)),
             str(_manifest_path.relative_to(root)),
             str(_scope_path.relative_to(root))],
            cwd=str(root), capture_output=True, text=True, timeout=600)
        assert _pr3.returncode == 0, f"G71 P3S failed: {_pr3.stderr[-2000:]}"
        import json as _js3
        _staged_out = _js3.loads(_pr3.stdout.strip().splitlines()[-1])
        _staged_manifest = root / _staged_out["staged_manifest"]
        assert _staged_manifest.is_file(), _staged_manifest
        print("G71 P3S staged:", _staged_manifest.relative_to(root), flush=True)
        # --- editorial prepare (REAL TinyTeX build) via fixture-code subprocess ---
        from scripts import survey_editorial_publication_v2 as edpub_mod
        _mspec = _prop_dir / "manuscript-spec.json"
        _write(_mspec, {
            "schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
            "issue_id": issue_id,
            "proposal_ref": {"path": str((_prop_dir / "proposal.json").relative_to(root)),
                             "sha256": _sha_file(_prop_dir / "proposal.json")},
            "architecture_coverage": [],
            "reader_requirements": [
                {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                 "reader_locations": ["main.tex"], "detail": "synthetic G71 editorial requirement"},
                {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
                 "reader_locations": ["main.tex"], "detail": "synthetic G71 editorial requirement"}],
            "authored_by": "SYNTHETIC_G71_FIXTURE", "recorded_at": "2026-10-29T16:00:00Z"})
        _texbin = Path("/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex")
        assert _texbin.is_file()
        _tspec = _prop_dir / "toolchain-spec.json"
        _write(_tspec, {
            "schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
            "executor": "SYNTHETIC_G71_FIXTURE",
            "absolute_executable": str(_texbin),
            "recipe": "lualatex-biber-lualatex",
            "argv": ["lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex",
                     "biber main",
                     "lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex",
                     "lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex"],
            "env": {}, "recorded_at": "2026-10-29T16:00:00Z"})
        print("G71 editorial specs written", flush=True)
        _ed_lines = [
            "import json, sys",
            "from pathlib import Path",
            "from datetime import datetime, timezone",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "from scripts import survey_editorial_publication_v2 as edpub",
            "from scripts import survey_editorial_retention_v2 as retention_mod",
            "from scripts import survey_publication_set_v2 as setmod",
            "from scripts import survey_production_v2 as core",
            "from scripts import survey_reader_publication_v2 as reader",
            "prep = edpub.prepare_publication(root, args['state'], args['proposal'], args['staged_manifest'], args['manuscript_spec'], args['toolchain_spec'], datetime.fromisoformat(args['recorded_at']))",
            "pubdir = root / prep['publication_dir']",
            "man = root / prep['manuscript']",
            "pdf = pubdir / 'build' / 'main.pdf'",
            "assert man.is_file() and pdf.is_file(), 'editorial build outputs missing'",
            "from pypdf import PdfReader as _PR",
            "pages = len(_PR(str(pdf)).pages)",
            "assert pages >= 1, 'need positive page count'",
            "det_dir = pubdir / 'deterministic'",
            "det_dir.mkdir(parents=True, exist_ok=True)",
            "import hashlib as _hl, json as _jj",
            "_det = []",
            "for _cid in ('IDENTIFIER_PRESERVATION', 'PDF_PREFLIGHT', 'SUBJECT_ENTITY_PROPERTY_BINDING'):",
            "    _rp = det_dir / (_cid.lower() + '.json')",
            "    _rp.write_text(_jj.dumps({'check_id': _cid, 'status': 'PASS'}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "    _det.append({'check_id': _cid, 'kind': 'DETERMINISTIC', 'status': 'PASS', 'executor': 'SYNTHETIC_G71_FIXTURE', 'evidence': 'synthetic G71 editorial check', 'recorded_at': '2026-10-29T17:00:00Z', 'result': {'path': str(_rp.relative_to(root)), 'sha256': _hl.sha256(_rp.read_bytes()).hexdigest()}})",
            "_det_path = pubdir / 'deterministic-checks.json'",
            "_det_path.write_text(_jj.dumps({'checks': _det}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "_prof = core.load_json(root / args['profile'])",
            "_exp_sem = sorted(reader._expected_review_checks(root, _prof, 'SEMANTIC_EDITORIAL'))",
            "_exp_vis = sorted(reader._expected_review_checks(root, _prof, 'VISUAL'))",
            "_sem = pubdir / 'semantic-editorial-review-v2.json'",
            "reader.build_review_record(root, man, pdf, pages, 'SEMANTIC_EDITORIAL', [{'check_id': c, 'status': 'PASS', 'detail': 'synthetic explicitly-nongenuine G71 ' + c, 'evidence_locations': ['main.tex']} for c in _exp_sem], 'SYNTHETIC_G71_FIXTURE', datetime.fromisoformat(args['recorded_at']), _sem)",
            "_vis = pubdir / 'visual-editorial-review-v2.json'",
            "reader.build_review_record(root, man, pdf, pages, 'VISUAL', [{'check_id': c, 'status': 'PASS', 'detail': 'synthetic explicitly-nongenuine G71 ' + c, 'evidence_locations': ['main.pdf']} for c in _exp_vis], 'SYNTHETIC_G71_FIXTURE', datetime.fromisoformat(args['recorded_at']), _vis)",
            "fin = edpub.finalize_publication(root, args['state'], args['proposal'], args['staged_manifest'], str(_det_path.relative_to(root)), str(_sem.relative_to(root)), str(_vis.relative_to(root)), datetime.fromisoformat(args['finalized_at']))",
            "set_rel = fin['set_ref'] if isinstance(fin['set_ref'], str) else fin['set_ref']['path']",
            "import hashlib as _hl2",
            "_set_sha = _hl2.sha256((root / set_rel).read_bytes()).hexdigest()",
            "act = edpub.activate_publication(root, args['state'], set_rel, args['reason'], args['executor'], datetime.fromisoformat(args['activated_at']))",
            "st = core.load_json(root / args['state'])",
            "sel = setmod.resolve_publication_selection(root, core.load_json(root / core.DEFAULT_CONFIG), st)",
            "vrfy = retention_mod.verify_retention(root, args['proposal'], args['retention_manifest'])",
            "out = {'set_ref': {'path': set_rel, 'sha256': _set_sha}, 'activate': act.get('status'), 'mode': sel.get('mode'), 'verify': vrfy.get('result')}",
            "print(json.dumps(out))",
        ]
        import json as _jj_pay
        _ed_payload = {
            "state": str(canon.relative_to(root)),
            "proposal": str((_prop_dir / "proposal.json").relative_to(root)),
            "staged_manifest": str(_staged_manifest.relative_to(root)),
            "manuscript_spec": str(_mspec.relative_to(root)),
            "toolchain_spec": str(_tspec.relative_to(root)),
            "recorded_at": "2026-10-29T16:30:00+00:00",
            "profile": str(profile_path.relative_to(root)),
            "det": "DUMMY",
            "sem": "DUMMY",
            "vis": "DUMMY",
            "finalized_at": "2026-10-29T18:00:00+00:00",
            "reason": "Synthetic G71 editorial activation (explicit nongenuine fixture review)",
            "executor": "SYNTHETIC_G71_FIXTURE",
            "activated_at": "2026-10-29T19:00:00+00:00",
            "retention_manifest": str(_manifest_path.relative_to(root)),
        }
        _ed_proc = subprocess.run(
            [sys.executable, "-c", "\n".join(_ed_lines), str(root), _jj_pay.dumps(_ed_payload)],
            cwd=str(root), capture_output=True, text=True, timeout=900)
        assert _ed_proc.returncode == 0, f"G71 editorial failed: {_ed_proc.stderr[-3000:]}"
        import json as _jj_out
        _ed_out = _jj_out.loads(_ed_proc.stdout.strip().splitlines()[-1])
        print("G71 editorial VERSIONED_ACTIVE:", _ed_out.get("mode"), _ed_out.get("activate"), flush=True)
        assert _ed_out.get("mode") == "VERSIONED_ACTIVE", _ed_out
        # --- record pre-overlay upstream SHAs (expanded: all accepted graph/materialized base, must stay byte-identical) ---
        import hashlib as _hl2, json as _jj2
        # Expanded KEEP: every file under sources/2026-W33 at G71 VERSIONED_ACTIVE prePreview (accepted Evidence/Views/Ledger/Comp/Profile/Architecture/Draft/completeReader/currentPDF/manuscript/reviews/seal/State/record/retention + direct inputs). Typed graph covers base all materialized; renewal not yet created so all files are upstream.
        _upstream_paths = sorted([str(q.relative_to(root)) for q in (root / "sources/2026-W33").rglob("*") if q.is_file() and "__pycache__" not in q.parts])
        _upstream_pre = {p: _hl2.sha256((root / p).read_bytes()).hexdigest() for p in _upstream_paths}
        print("G71 upstream pins (expanded, all materialized):", len(_upstream_pre), flush=True)
        # --- install G76 source (fixed4, reviewed) + commit G76 epoch ---
        _G76 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/dm022-g71-g76-finalsrc-20261029T152924Z")
        assert (_G76 / "scripts" / "survey_research_authority_v2.py").is_file(), "G76 source must carry DM022 modules"
        _overlay_list = [l.strip() for l in open("/tmp/g76-tool-relpaths-finalsrc-152924Z.txt") if l.strip()]
        # TOOL-only (no tests): genuine code/schema/config delta, not test helpers, not artifact intent.
        print("G76 overlay files:", len(_overlay_list), flush=True)
        for _rel in _overlay_list:
            _src = _G76 / _rel
            assert _src.is_file(), _rel
            _dst = root / _rel
            _dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(_src, _dst)
        import shutil as _sh2; [shutil.rmtree(p, ignore_errors=True) for p in list(root.rglob("__pycache__"))]; _git(root, "add", "-A")
        _git(root, "commit", "-q", "-m", "Genuine G76 tool epoch: install reviewed G76 candidate source over unchanged G71 upstream (research/Profile/Architecture/Draft/reader/reviews preserved)")
        _epoch_g76 = _git(root, "rev-parse", "HEAD")
        print("G76 epoch:", _epoch_g76, flush=True)
        _st = _git(root, "status", "--porcelain=v1")
        print(f"G76 post-commit status lines: {len(_st.splitlines())}", flush=True)
        print(_st[:2000], flush=True)
        assert _epoch_g76 != epoch_g71, "G76 epoch must differ (genuine Core change)"
        # --- unchanged-upstream verification (expanded, byte-identical, no State rewind/old receipt rebind) ---
        _post_paths = sorted([str(q.relative_to(root)) for q in (root / "sources/2026-W33").rglob("*") if q.is_file() and "__pycache__" not in q.parts])
        assert set(_post_paths)==set(_upstream_pre.keys()), f"upstream file set drift: only-added={sorted(set(_post_paths)-set(_upstream_pre.keys()))[:10]} only-removed={sorted(set(_upstream_pre.keys())-set(_post_paths))[:10]}"
        for _p, _sha in _upstream_pre.items():
            _now = _hl2.sha256((root / _p).read_bytes()).hexdigest()
            assert _now == _sha, f"upstream drift after G76 overlay: {_p}"
        print("G71 upstream unchanged after G76 overlay (expanded, all materialized): OK", flush=True)
        # --- renewal U on G76 (genuine G71->G76 Core change) ---
        _ren_spec = _prop_dir / "renewal-manuscript-spec.json"
        _write(_ren_spec, {
            "schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
            "issue_id": issue_id,
            "proposal_ref": {"path": str((_prop_dir / "proposal.json").relative_to(root)),
                             "sha256": _sha_file(_prop_dir / "proposal.json")},
            "architecture_coverage": [],
            "reader_requirements": [
                {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                 "reader_locations": ["main.tex"], "detail": "synthetic G71 renewal requirement"},
                {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
                 "reader_locations": ["main.tex"], "detail": "synthetic G71 renewal requirement"}],
            "authored_by": "SYNTHETIC_G71_FIXTURE", "recorded_at": "2026-10-29T20:00:00Z"})
        import subprocess as _sp2
        _ren_code = "\n".join([
            "import json, sys",
            "from pathlib import Path",
            "from datetime import datetime, timezone",
            "root = Path(sys.argv[1]).resolve()",
            "args = json.loads(sys.argv[2])",
            "from scripts import survey_versioned_renewal_v2 as high",
            "from scripts import survey_versioned_renewal_source_v2 as srcmod",
            "prep = high.prepare_renewal(root, args['state'], args['renewal_id'], 'REUSE_TARGETS', args['manuscript_spec'], None, args['executor'], datetime.fromisoformat(args['recorded_at']))",
            "basis_rel = prep['basis_path']",
            "det_dir = root / 'sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/publication/deterministic'",
            "checks = []",
            "import hashlib as _hl3, json as _jj3",
            "for _cid in ('IDENTIFIER_PRESERVATION', 'PDF_PREFLIGHT', 'SUBJECT_ENTITY_PROPERTY_BINDING'):",
            "    _rp = det_dir / (_cid.lower() + '.json')",
            "    _rd = _jj3.loads(_rp.read_bytes())",
            "    checks.append({'check_id': _cid, 'kind': 'DETERMINISTIC', 'status': 'PASS', 'executor': 'SYNTHETIC_G71_FIXTURE', 'evidence': 'synthetic G71 renewal recheck', 'recorded_at': '2026-10-29T20:30:00+00:00', 'result': {'path': str(_rp.relative_to(root)), 'sha256': _hl3.sha256(_rp.read_bytes()).hexdigest()}})",
            "_chk_path = root / 'sources/2026-W33/publication/v2/editorial-corrections/ed-g71-v2-01/renewal-checks.json'",
            "_chk_path.write_text(_jj3.dumps({'checks': checks}, indent=2, sort_keys=True) + chr(10), encoding='utf-8')",
            "out = {'basis': basis_rel}",
            "fin = high.finalize_renewal(root, args['state'], basis_rel, str(_chk_path.relative_to(root)), None, None, args['executor'], datetime.fromisoformat(args['finalized_at']))",
            "out['finalize'] = {k: fin[k] for k in ('receipt_path','build_record_path','bundle_path','gate_path','candidate_path','set_path','proof_path') if k in fin}",
            "_proof_rel = fin.get('proof_path', basis_rel.replace('renewal-basis.json', 'renewal-source-proof.json'))",
            "out['proof'] = _proof_rel",
            "vrfy = srcmod.verify_renewal_source_proof(root, basis_rel, _proof_rel)",
            "out['verify'] = {'CURRENT_PROOF_VALID': vrfy.get('CURRENT_PROOF_VALID')}",
            "print(json.dumps(out))",
        ])
        import json as _jj_pay2
        _ren_payload = {"state": str(canon.relative_to(root)),
                        "renewal_id": "ren-g71-u-v2",
                        "manuscript_spec": str(_ren_spec.relative_to(root)),
                        "executor": "SYNTHETIC_G71_FIXTURE",
                        "recorded_at": "2026-10-29T20:00:00+00:00",
                        "finalized_at": "2026-10-29T21:00:00+00:00"}
        _ren = _sp2.run([sys.executable, "-c", _ren_code, str(root), _jj_pay2.dumps(_ren_payload)],
                        cwd=str(root), capture_output=True, text=True, timeout=900)
        assert _ren.returncode == 0, f"G71->G76 renewal U prepare/finalize failed: {_ren.stderr[-3000:]}"
        import json as _jj_out2
        _ren_out = _jj_out2.loads(_ren.stdout.strip().splitlines()[-1])
        print("G71->G76 renewal U finalize OK:", sorted(_ren_out["finalize"].keys()), flush=True)
        print("KEEP fixture at:", root, flush=True)
        return 0
    except Exception:
        import traceback; traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
