"""W34: stage event JSONL at canonical input path + prepare expansion package (existing API, strict facade)."""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
INTAKE = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_screening_v2 as screening

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
print(f"HEAD={core.repository_commit_sha(WORK)}")

src = INTAKE / "DATA.p2b19.p2b19"
b = src.read_bytes()
assert len(b) == 1335444
assert hashlib.sha256(b).hexdigest() == "0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e"
assert hashlib.sha1(b"blob " + str(len(b)).encode() + b"\x00" + b).hexdigest() == "06eb26bbaafd08782a5158102e9a67885809b434"
print("event bytes self-verified: size+sha256+git-blob == tree/API (06eb26bb/1335444)")

dst = WORK / "sources/2026-W34/screening/input/event-discovery-v2.jsonl"
assert str(dst.relative_to(WORK)) == "sources/2026-W34/screening/input/event-discovery-v2.jsonl", "canonical input path from tree@774"
if dst.exists():
    assert dst.read_bytes() == b, "canonical event path already staged with different bytes"
    print("event already staged identical")
else:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"staged canonical E path: {dst.relative_to(WORK)}")

state_path = WORK / "sources/2026-W34/production-state.json"
out_dir = WORK / "sources/2026-W34/screening/proposed-input/expansion-package"
assert not out_dir.exists(), "owned output dir must be fresh"
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
state = core.load_json(state_path)
assert state["lifecycle_state"] == "DISCOVERY_COLLECTED", state["lifecycle_state"]

impl = core.repository_commit_sha(WORK)
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl
print(f"implementation_sha (actual current work-branch head): {impl}")
with agent_tool.current_stage_basis_override():
    pkg = screening.prepare_package(WORK, state_path, dst, out_dir, impl)
print(f"package: {Path(pkg).relative_to(WORK)}")
package = core.load_json(pkg)
print(f"package basis discovery: {package['basis']['discovery_path']} sha={package['basis']['discovery_sha256'][:12]}...")
print(f"package input: record_count={package['input']['record_count']} batches={len(package['input']['batches'])}")
print("DONE-STAGE-PREPARE (package draft only; no decisions, no accept, no state write)")
