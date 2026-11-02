"""Post-advance verification, both editions (read-only; canonical record)."""
import hashlib
import json
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core

print(f"HEAD={core.repository_commit_sha(WORK)} (expect 48082356...)")
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
for issue in ["2026-W34", "SP-efficient-llm-2026"]:
    sp = WORK / f"sources/{issue}/production-state.json"
    st = core.load_json(sp)
    errs = agent.validate_agent_state(WORK, cfg, st)
    print(f"{issue}: lifecycle={st['lifecycle_state']} agent_errors={errs}")
    print(f"  state sha256={hashlib.sha256(sp.read_bytes()).hexdigest()}")
    print(f"  checkpoints passed={[k for k, v in st['machine_checkpoints'].items() if v == 'passed']}")
    print(f"  history last: {st['history'][-1]}")
    for cn in ("ISSUE_INITIALIZED", "DISCOVERY_COLLECTED"):
        cp = WORK / f"sources/{issue}/orchestration/v2/checkpoints/{cn}.json"
        print(f"  checkpoint {cn}: exists={cp.exists()}" + (f" sha={hashlib.sha256(cp.read_bytes()).hexdigest()}" if cp.exists() else ""))
print("DONE (read-only; no writes)")
