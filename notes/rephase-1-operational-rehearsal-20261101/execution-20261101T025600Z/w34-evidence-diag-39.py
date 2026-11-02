"""W34 Evidence diag 39 (read-only preflight timing, no evidence/v2 write, faulthandler).

Goal: pinpoint 38 hang (200GB+ rchar, 99% CPU, no output) without duplicating accepted outputs.
No state write, no package write to canonical paths (uses temp), no evidence accept.
"""
import faulthandler
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

faulthandler.enable()
# Dump traceback to stderr after 90s if still running (proves hang location)
faulthandler.dump_traceback_later(90, exit=True)

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_discovery_v2 as discovery
from scripts import survey_screening_v2 as screening
from scripts import survey_evidence_v2 as evidence
import tempfile

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}", flush=True)
impl = core.repository_commit_sha(WORK)
print(f"HEAD={impl}", flush=True)
state_path = WORK / "sources/2026-W34/production-state.json"
state = core.load_json(state_path)
print(f"lifecycle={state['lifecycle_state']}", flush=True)
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
print(f"agent errors={agent.validate_agent_state(WORK, cfg, state)}", flush=True)
profile = core.load_json(WORK / state["profile"]["path"])
print(f"profile={profile['research_profile']}", flush=True)
source_root = core.repo_local_path(WORK, profile["paths"]["source_root"], "paths.source_root")
print(f"source_root={source_root.relative_to(WORK)}", flush=True)

t0 = time.time()
da_path = source_root / "discovery/discovery-accepted-v2.json"
acc_discovery = discovery.validate_acceptance(WORK, da_path)
print(f"[{time.time()-t0:.1f}s] discovery.validate_acceptance OK records={len(acc_discovery.get('records', [])) if isinstance(acc_discovery, dict) else '?'}", flush=True)

t0 = time.time()
active = screening.resolve_active_screening_acceptance(WORK, state_path, impl)
print(f"[{time.time()-t0:.1f}s] resolve_active_screening_acceptance OK path={active['path']}", flush=True)

t0 = time.time()
eff = screening.resolve_effective_discovery_basis(WORK, active["path"].parent / "package.json", impl, accepted_root_path=core.repo_local_path(WORK, acc_discovery["discovery_path"], "accepted Discovery JSONL"))
print(f"[{time.time()-t0:.1f}s] resolve_effective OK records={len(eff['records'])} root={len(eff.get('root_records', []))}", flush=True)

# Supplement validate (like 37, should be fast with preloaded acceptance/discoveries?)
supp_p = WORK / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"
print(f"supplement exists={supp_p.exists()} sha={core.sha256_file(supp_p) if supp_p.exists() else None}", flush=True)
t0 = time.time()
# Use same call as prepare_evidence_package does (with preloaded acceptance/discoveries to avoid re-resolve?)
# First, direct validate without preloads (like builder does) – times file reads
man = evidence.validate_evidence_authority_supplement(WORK, supp_p, impl, expected_issue_id="2026-W34")
print(f"[{time.time()-t0:.1f}s] validate_supplement (no preload) OK sources={len(man['sources'])}", flush=True)

# Now prepare_evidence_package to temp (no canonical write) – this is where 38 likely hangs
t0 = time.time()
print("starting prepare_evidence_package to temp (may hang – faulthandler will dump at 90s)...", flush=True)
with tempfile.TemporaryDirectory() as td:
    td_p = Path(td) / "evidence-package"
    with agent_tool.current_stage_basis_override():
        pkg_p = evidence.prepare_evidence_package(WORK, state_path, eff["path"], active["path"], td_p, impl, supp_p)
    print(f"[{time.time()-t0:.1f}s] prepare_evidence_package OK pkg={pkg_p}", flush=True)
    pkg = core.load_json(pkg_p)
    print(f"tasks={len(pkg['tasks'])}", flush=True)

print("DONE-DIAG-39 (no evidence accept, no state write)", flush=True)
