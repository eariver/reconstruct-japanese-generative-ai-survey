"""Pre-advance strict snapshot (read-only): agent validation, pins, reviews-file shape, absence checks."""
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

print(f"HEAD={core.repository_commit_sha(WORK)}")
for issue in ["2026-W34", "SP-efficient-llm-2026"]:
    print(f"===== {issue} =====")
    cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
    spath = WORK / f"sources/{issue}/production-state.json"
    state = core.load_json(spath)
    errs = agent.validate_agent_state(WORK, cfg, state)
    print(f"agent.validate_agent_state errors: {errs}")
    print(f"lifecycle={state['lifecycle_state']} impl={state['implementation']['repository_commit_sha'][:12]}... checkpoints_passed={[k for k,v in state['machine_checkpoints'].items() if v=='passed']}")
    print(f"state_sha={core.sha256_file(spath)}")
    ppath = WORK / state["profile"]["path"]
    print(f"profile_sha={core.sha256_file(ppath)} contract_pipe={core.contract_identity(WORK, cfg, state['research_profile'], state['publication_profile'])['pipeline_contract_sha256'][:12]}...")
    rpath = WORK / f"sources/{issue}/orchestration/v2/stage-reviews/ISSUE_INITIALIZED-reviews.json"
    rows = agent._load_reviews(WORK, rpath)
    print(f"reviews rows={[(r['check_id'], r['kind'], r['status'], r['executor'][:60]) for r in rows]}")
    for r in rows:
        if r["kind"] == "DETERMINISTIC":
            print(f"  deterministic result ref: {r['result']}")
    cpath = WORK / f"sources/{issue}/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json"
    print(f"canonical checkpoint exists (must be False): {cpath.exists()}")
    rep = WORK / f"sources/{issue}/orchestration/v2/stage-validation/ISSUE_INITIALIZED-report.json"
    print(f"report exists: {rep.exists()} sha={core.sha256_file(rep) if rep.exists() else None}")
print("DONE-PRE-SNAPSHOT (no writes)")
