"""Deterministic CORE_STAGE_CONTRACT preflight/report builds (no state advance).

Public API: survey_stage_validation_v2.validate_stage (same as CLI
--state --artifact discovery-acceptance=PATH --output PATH --recorded-at).
Supplied: canonical fresh discovery-acceptance per edition.
Output: NEW report files (refuse-overwrite); no checkpoint/state writes.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core, survey_stage_validation_v2 as stageval

RECORDED = datetime.now(timezone.utc)
print(f"REAL-CLOCK recorded_at={core.iso_utc(RECORDED)} (preflight only; state advance needs review decision)")

for issue in ["2026-W34", "SP-efficient-llm-2026"]:
    print(f"===== {issue} =====")
    cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
    spath = WORK / f"sources/{issue}/production-state.json"
    acc = WORK / f"sources/{issue}/discovery/discovery-accepted-v2.json"
    outp = WORK / f"sources/{issue}/orchestration/v2/stage-validation/ISSUE_INITIALIZED-report.json"
    assert acc.is_file(), f"missing acceptance {acc}"
    print(f"exists acceptance: True  output exists (must be False): {outp.exists()}")
    assert not outp.exists()
    outp.parent.mkdir(parents=True, exist_ok=True)
    built = stageval.validate_stage(WORK, cfg, spath, {"discovery-acceptance": acc}, outp, RECORDED)
    rep = core.load_json(built)
    print(f"report: {built.relative_to(WORK)} status={rep['status']} check={rep['check_id']}")
    print(f"  from={rep['from_state']} to={rep['to_state']} artifacts={[a['name'] for a in rep['artifacts']]}")
    print(f"  state_ref={rep['production_state']} profile_ref={rep['production_profile']}")
    print(f"  impl={rep['implementation_commit_sha'][:12]}... recorded_at={rep['recorded_at']}")
print("DONE-ALL (reports only; NO checkpoint write, NO state advance)")
