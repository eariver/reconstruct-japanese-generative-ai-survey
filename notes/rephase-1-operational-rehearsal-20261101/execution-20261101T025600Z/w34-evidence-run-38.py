"""W34 Evidence run 38 via normal public runner (structural accept only, no semantic PASS).

Input 409-record 3ffc6e31 (352 PARTIAL/49 VERIFIED/8 NEEDS_MORE historical) + NEW r2-fresh-basis supplement.
No state advance, no EVIDENCE_REVIEWED checkpoint.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import run_evidence_v2_interactive as evrun  # noqa: F401 (import via scripts)
import scripts.run_evidence_v2_interactive as evmod

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
print(f"CWD={Path.cwd()}")
impl = core.repository_commit_sha(WORK)
print(f"HEAD={impl}")
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl

state_path = WORK / "sources/2026-W34/production-state.json"
state = core.load_json(state_path)
print(f"PRE lifecycle={state['lifecycle_state']}")
assert state["lifecycle_state"] == "CANDIDATES_NORMALIZED", state["lifecycle_state"]
errs = agent.validate_agent_state(WORK, core.load_json(WORK / core.DEFAULT_CONFIG), state)
print(f"PRE agent errors={errs}")
assert not errs

inp = WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json"
b = inp.read_bytes()
print(f"input {len(b)}B sha256={hashlib.sha256(b).hexdigest()}")
assert len(b) == 1573186
assert hashlib.sha256(b).hexdigest() == "3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27"

supp = WORK / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"
assert supp.is_file(), f"fresh supplement missing {supp}"
print(f"supplement {supp.relative_to(WORK)} sha256={core.sha256_file(supp)} bytes={supp.stat().st_size}")

# No overwrite: evidence/v2 must be absent
ev_root = WORK / "sources/2026-W34/evidence/v2"
assert not ev_root.exists(), f"refusing overwrite {ev_root}"
print("PRE evidence/v2 absent OK")

out = evmod.run(WORK, state_path, inp, supp)
print(json.dumps(out, indent=2))
print("DONE-EVIDENCE-38 (accepted products only; NO checkpoint, NO state advance, NO semantic PASS)")
