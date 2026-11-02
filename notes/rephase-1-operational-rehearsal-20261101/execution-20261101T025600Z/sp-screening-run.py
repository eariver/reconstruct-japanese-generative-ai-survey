"""SP screening: verify archived decisions, stage exact bytes, check coverage vs FRESH acceptance (no writes yet)."""
import hashlib
import json
import shutil
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
INTAKE = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core

src = INTAKE / "DATA.p2g14.interactive-decisions.json"
b = src.read_bytes()
print(f"archived decisions: {len(b)}B sha256={hashlib.sha256(b).hexdigest()}")
assert len(b) == 68226, "p2g14 size drift"
doc = json.loads(b)
assert doc["issue_id"] == "SP-efficient-llm-2026" and doc["schema_version"] == "2.0-rc1"

fresh = core.load_json(WORK / "sources/SP-efficient-llm-2026/discovery/discovery-accepted-v2.json")
fresh_ids = {r["discovery_id"] for r in fresh["records"]}
dec_ids = {d["discovery_id"] for d in doc["decisions"]}
print(f"fresh accepted IDs: {len(fresh_ids)}; decision IDs: {len(dec_ids)}")
print(f"missing={sorted(fresh_ids - dec_ids)[:5]} (count {len(fresh_ids - dec_ids)})")
print(f"extra={sorted(dec_ids - fresh_ids)[:5]} (count {len(dec_ids - fresh_ids)})")
assert fresh_ids == dec_ids, "coverage mismatch vs FRESH acceptance"

dst = WORK / "sources/SP-efficient-llm-2026/screening/proposed-input/interactive-decisions.json"
if dst.exists():
    assert dst.read_bytes() == b, "proposed input already staged but bytes differ"
    print("proposed input already staged identical")
else:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"staged proposed input: {dst.relative_to(WORK)} sha={hashlib.sha256(b).hexdigest()[:12]}...")
print("READY-FOR-RUNNER (no runner executed in this script)")
