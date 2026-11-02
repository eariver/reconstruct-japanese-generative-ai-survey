"""W34 Evidence diag 39b (with override, stepwise timing, faulthandler).

Mimics run() with override to find hang after supplement validation.
No canonical writes (temp only), no state advance.
"""
import faulthandler
import sys
import time
import tempfile
from datetime import datetime, timezone
from pathlib import Path

faulthandler.enable()
faulthandler.dump_traceback_later(120, exit=True)

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_discovery_v2 as discovery
from scripts import survey_screening_v2 as screening
from scripts import survey_evidence_v2 as evidence

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}", flush=True)
impl = core.repository_commit_sha(WORK)
print(f"HEAD={impl}", flush=True)
state_path = WORK / "sources/2026-W34/production-state.json"
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
state = core.load_json(state_path)
print(f"lifecycle={state['lifecycle_state']} agent={agent.validate_agent_state(WORK, cfg, state)}", flush=True)
profile = core.load_json(WORK / state["profile"]["path"])
source_root = core.repo_local_path(WORK, profile["paths"]["source_root"], "paths.source_root")

# Resolve like run() does
da_path = source_root / "discovery/discovery-accepted-v2.json"
acc_discovery = discovery.validate_acceptance(WORK, da_path)
print(f"discovery OK {len(acc_discovery.get('records', [])) if isinstance(acc_discovery, dict) else '?'}", flush=True)
active = screening.resolve_active_screening_acceptance(WORK, state_path, impl)
print(f"active screening {active['path']}", flush=True)
eff = screening.resolve_effective_discovery_basis(WORK, active["path"].parent / "package.json", impl, accepted_root_path=core.repo_local_path(WORK, acc_discovery["discovery_path"], "accepted Discovery"))
print(f"effective records={len(eff['records'])} root={len(eff.get('root_records', []))}", flush=True)

supp_p = WORK / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"
print(f"supplement {core.sha256_file(supp_p)[:12]}...", flush=True)

t0 = time.time()
print("validate_supplement WITH override (like builder)...", flush=True)
with agent_tool.current_stage_basis_override():
    man = evidence.validate_evidence_authority_supplement(WORK, supp_p, impl, expected_issue_id="2026-W34", expected_source_root=source_root, expected_discovery_path=WORK / "sources/2026-W34/screening/input/event-discovery-v2.jsonl", expected_screening_acceptance_path=active["path"])
print(f"[{time.time()-t0:.1f}s] validate_supplement WITH override OK {len(man['sources'])}", flush=True)

t0 = time.time()
print("prepare_evidence_package WITH override to temp...", flush=True)
with tempfile.TemporaryDirectory() as td:
    td_p = Path(td) / "evidence-package"
    with agent_tool.current_stage_basis_override():
        pkg_p = evidence.prepare_evidence_package(WORK, state_path, eff["path"], active["path"], td_p, impl, supp_p)
    print(f"[{time.time()-t0:.1f}s] prepare OK", flush=True)
    import json as _json
    pkg = core.load_json(pkg_p)
    print(f"tasks={len(pkg['tasks'])}", flush=True)
    # Now validate_interactive_input (like run does) – time it
    inp_p = WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json"
    inp_doc = core.load_json(inp_p)
    from scripts import run_evidence_v2_interactive as evmod
    # Replicate run()'s preflight + validate_interactive_input without building cards
    t1 = time.time()
    print("validate_interactive_input...", flush=True)
    # Use internal function via run module? Call directly with same args as run()
    # run() does: _validate_completeness_input, then validate_interactive_input(doc, profile, expected_ids, task_source_ids, ...)
    # First need task_source_ids (reads tasks) – time that
    task_meta = {meta["discovery_ids"][0]: meta for meta in pkg["tasks"]}
    print(f"task_meta {len(task_meta)}", flush=True)
    # task_authority_sources per task – this may be the 200GB loop
    t2 = time.time()
    print("task_authority_sources per task (count only, first 5)...", flush=True)
    for i, did in enumerate(sorted(task_meta)):
        meta = task_meta[did]
        task = core.load_json(pkg_p.parent / meta["path"])
        srcs = evidence.task_authority_sources(WORK, task, pkg)
        if i < 5:
            print(f"  {did} -> {len(srcs)} sources", flush=True)
        if i >= 4:
            break
    print(f"[{time.time()-t2:.1f}s] first-5 task_authority_sources done", flush=True)

print("DONE-DIAG-39b (no accept, no state write)", flush=True)
