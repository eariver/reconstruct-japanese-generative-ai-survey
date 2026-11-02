"""W34 narrow takeover check 35 (read-only; no advance duplication, no Evidence runner).

Owner: NEW General execution owner (takeover after provider server_error, not source/test failure).
Bounds: workdir read-only + packet tree.json (local authorized input); no network, no reconstruct Git readback,
no Production checkout, no new intake, no source/schema/module edits, no candidate commit, SP untouched.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
PACKET = Path("notes/rephase-1-operational-rehearsal-20261101/execution-20261101T025600Z")
INTAKE_P2 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
print(f"CWD={Path.cwd()}")
impl = core.repository_commit_sha(WORK)
print(f"HEAD={impl}")
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl

# 1. Canonical W34 State (no root Git readback; workdir State only)
spath = WORK / "sources/2026-W34/production-state.json"
state = core.load_json(spath)
print(f"W34 lifecycle={state['lifecycle_state']} next={state.get('next_action')}")
print(f"W34 state file sha256={core.sha256_file(spath)} bytes={spath.stat().st_size}")
errs = agent.validate_agent_state(WORK, core.load_json(WORK / core.DEFAULT_CONFIG), state)
print(f"W34 agent errors={errs}")
assert state["lifecycle_state"] == "CANDIDATES_NORMALIZED", "expected already-advanced (logs 31-33)"
print(f"W34 history last={state['history'][-1]}")
print(f"W34 discovery/screening={state['machine_checkpoints']['discovery']}/{state['machine_checkpoints']['screening']} evidence={state['machine_checkpoints']['evidence']}")
# Checkpoints
for name in ["ISSUE_INITIALIZED", "DISCOVERY_COLLECTED"]:
    cp = WORK / f"sources/2026-W34/orchestration/v2/checkpoints/{name}.json"
    print(f"checkpoint {name} exists={cp.exists()} sha={core.sha256_file(cp) if cp.exists() else None}")
# Screening acceptance still bound
acc = WORK / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json"
print(f"screening-accepted exists={acc.exists()} sha={core.sha256_file(acc) if acc.exists() else None} bytes={acc.stat().st_size if acc.exists() else 0}")
pkg = WORK / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/package.json"
print(f"package exists={pkg.exists()} sha={core.sha256_file(pkg) if pkg.exists() else None}")
# Stage-validation report for DISCOVERY_COLLECTED->CANDIDATES_NORMALIZED (current stage, not old ISSUE_INITIALIZED report)
rep = WORK / "sources/2026-W34/orchestration/v2/stage-validation/DISCOVERY_COLLECTED-report.json"
print(f"stage report DISCOVERY_COLLECTED exists={rep.exists()} sha={core.sha256_file(rep) if rep.exists() else None}")
if rep.exists():
    rj = core.load_json(rep)
    print(f"report from={rj.get('from_state')} to={rj.get('to_state')} status={rj.get('status')} recorded_at={rj.get('recorded_at')}")
# Profile
prof = WORK / "sources/2026-W34/production-profile.json"
print(f"profile sha={core.sha256_file(prof)}")
# Evidence proposed input already staged (p2b18)
evp = WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json"
print(f"evidence proposed-input exists={evp.exists()} sha={core.sha256_file(evp) if evp.exists() else None} bytes={evp.stat().st_size if evp.exists() else 0}")
# Evidence v2 must NOT exist yet (no runner)
ev2 = WORK / "sources/2026-W34/evidence/v2"
print(f"evidence/v2 exists={ev2.exists()} (must be False; no Evidence run yet)")
assert not ev2.exists(), "evidence/v2 already exists - would be overwrite collision"

# 2. Intake binding: current input + old supplement (immutable), missing r2
p2b18 = INTAKE_P2 / "DATA.p2b18.p2b18"
print(f"P2 p2b18 exists={p2b18.exists()} sha={hashlib.sha256(p2b18.read_bytes()).hexdigest() if p2b18.exists() else None}")
p2d01 = INTAKE_P2 / "DATA.p2d01.evidence-authority-supplement.json"
old = json.loads(p2d01.read_bytes())
print(f"P2 p2d01 {old['supplement_id']} sources={len(old['sources'])} sha={hashlib.sha256(p2d01.read_bytes()).hexdigest()}")
doc = json.loads(evp.read_bytes())
import collections
print(f"interactive records={len(doc['records'])} statuses={dict(collections.Counter(r['status'] for r in doc['records']))}")
need = {sb for r in doc["records"] for sb in (r.get("source_bindings") or [])}
print(f"distinct needed supplement IDs={len(need)}")
man = {e["supplement_source_id"] for e in old["sources"]}
print(f"needed - old_manifest={len(need - man)} (old rows CANNOT bind current input)")
print(f"unbound records (no bindings)={sum(1 for r in doc['records'] if 'source_bindings' not in r)}")
# r2 manifest exact fixed-ref identity from local tree.json (no network, no intake fetch)
tree_p = Path(".rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/tree.json")
import re
data = tree_p.read_text()
m = re.search(r'"path": "sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-authority-supplement.json".*?"sha": "([0-9a-f]+)".*?"size": ([0-9]+)', data, re.DOTALL)
print(f"r2 manifest fixed-ref path=sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-authority-supplement.json blob={m.group(1) if m else None} size={m.group(2) if m else None}")
print("BLOCKED: r2 manifest + its raws not in P2-P4 captures; intake fetch required (same ref 774, no new Human permission per README). Old r1 manifest basis stale (discovery 9bfc0fc9 vs fresh 0a23be47; screening 5692a79a vs fresh e193ad05); no rebind, no runner.")
# 3. SP untouched
sp_state = core.load_json(WORK / "sources/SP-efficient-llm-2026/production-state.json")
print(f"SP lifecycle={sp_state['lifecycle_state']} (held immutable, CHANGES_REQUIRED; no SP advance/edit)")
print("DONE-NARROW-CHECK-35 (read-only; advance already performed, Evidence blocked, no overwrite)")
