"""SP evidence run via normal public runner (structural validation only, no semantic PASS)."""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import run_evidence_v2_interactive as evrun

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
src = Path("notes/rephase-1-operational-rehearsal-20261101/execution-20261101T025600Z/input-archive/SP/interactive-evidence-r2-adapted-O13-15.json")
b = src.read_bytes()
print(f"adapted input: {len(b)}B sha256={hashlib.sha256(b).hexdigest()}")
assert len(b) == 345202, "r2-adapted size drift"
dst = WORK / "sources/SP-efficient-llm-2026/evidence/proposed-input/interactive-evidence.json"
if dst.exists():
    assert dst.read_bytes() == b, "proposed input exists with different bytes"
    print("proposed input already staged identical")
else:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"staged proposed input: {dst.relative_to(WORK)}")
supp = WORK / "sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json"
assert supp.is_file(), "fresh supplement manifest must exist"
print(f"supplement manifest: {supp.relative_to(WORK)}")

state_path = WORK / "sources/SP-efficient-llm-2026/production-state.json"
state = core.load_json(state_path)
assert state["lifecycle_state"] == "CANDIDATES_NORMALIZED", state["lifecycle_state"]
out = evrun.run(WORK, state_path, dst, supp)
print(json.dumps(out, indent=2))
print("DONE-EVIDENCE (accepted product only; NO checkpoint, NO state advance, NO semantic PASS)")
