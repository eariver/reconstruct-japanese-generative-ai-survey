"""Post-advance strict verification (read-only): agent validation, lifecycle, checkpoint provenance + hashes."""
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
    print(f"agent errors: {errs}")
    print(f"lifecycle={state['lifecycle_state']} next={state.get('next_action')} terminal={state.get('terminal_reason')}")
    print(f"history last: {state['history'][-1]}")
    print(f"machine discovery/screening: {state['machine_checkpoints']['discovery']}/{state['machine_checkpoints']['screening']}")
    print(f"checkpoint_provenance.discovery={state['checkpoint_provenance']['discovery']}")
    cpath = WORK / f"sources/{issue}/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json"
    print(f"canonical checkpoint exists: {cpath.exists()} sha={core.sha256_file(cpath) if cpath.exists() else None}")
    print(f"state sha={core.sha256_file(spath)}")
print("DONE-POST-VERIFY (no writes)")
