"""W34 Evidence diag 41 (full interactive validation + card build timing, temp only).

Finds 38 hang after package (200GB rchar). No canonical writes.
"""
import faulthandler
import sys
import time
import tempfile
from datetime import datetime, timezone
from pathlib import Path

faulthandler.enable()
faulthandler.dump_traceback_later(180, exit=True)

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_discovery_v2 as discovery
from scripts import survey_screening_v2 as screening
from scripts import survey_evidence_v2 as evidence
from scripts import run_evidence_v2_interactive as evmod

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}", flush=True)
impl = core.repository_commit_sha(WORK)
state_path = WORK / "sources/2026-W34/production-state.json"
state = core.load_json(state_path)
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
assert not agent.validate_agent_state(WORK, cfg, state)
profile = core.load_json(WORK / state["profile"]["path"])
source_root = core.repo_local_path(WORK, profile["paths"]["source_root"], "paths.source_root")
da_path = source_root / "discovery/discovery-accepted-v2.json"
acc_discovery = discovery.validate_acceptance(WORK, da_path)
active = screening.resolve_active_screening_acceptance(WORK, state_path, impl)
eff = screening.resolve_effective_discovery_basis(WORK, active["path"].parent / "package.json", impl, accepted_root_path=core.repo_local_path(WORK, acc_discovery["discovery_path"], "accepted Discovery"))
supp_p = WORK / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"
inp_p = WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json"
inp_doc = core.load_json(inp_p)
print(f"input records={len(inp_doc['records'])}", flush=True)

with tempfile.TemporaryDirectory() as td:
    td_p = Path(td) / "evidence-package"
    with agent_tool.current_stage_basis_override():
        pkg_p = evidence.prepare_evidence_package(WORK, state_path, eff["path"], active["path"], td_p, impl, supp_p)
    pkg = core.load_json(pkg_p)
    print(f"package tasks={len(pkg['tasks'])}", flush=True)
    task_meta = {meta["discovery_ids"][0]: meta for meta in pkg["tasks"]}
    # task_source_ids like run() does
    t0 = time.time()
    print("computing task_source_ids for all 409...", flush=True)
    task_source_ids = {}
    for did, meta in sorted(task_meta.items()):
        task = core.load_json(pkg_p.parent / meta["path"])
        task_source_ids[did] = set(evidence.task_authority_sources(WORK, task, pkg))
    print(f"[{time.time()-t0:.1f}s] task_source_ids done", flush=True)
    # validate_interactive_input (this is where run() validates 409 records)
    t0 = time.time()
    print("validate_interactive_input full 409...", flush=True)
    from scripts.run_evidence_v2_interactive import validate_interactive_input
    discoveries = eff["records"]
    root_recs = eff["root_records"]
    records_by_id, runner, comp_in = validate_interactive_input(inp_doc, profile, set(task_meta), task_source_ids, discoveries=discoveries, root_discovery_records=root_recs)
    print(f"[{time.time()-t0:.1f}s] validate_interactive_input OK runner={runner.get('model') if isinstance(runner, dict) else runner}", flush=True)
    # Build all 409 cards (like run does) with timing per 50
    t0 = time.time()
    print("building 409 cards...", flush=True)
    for idx, did in enumerate(sorted(task_meta)):
        meta = task_meta[did]
        task = core.load_json(pkg_p.parent / meta["path"])
        card = evmod._build_card(WORK, task, meta, pkg, records_by_id[did], runner)
        errs = evidence.validate_evidence_card(card, task, meta["sha256"], pkg, repo_root=WORK)
        if errs:
            print(f"CARD INVALID {did}: {errs[:2]}", flush=True)
            break
        if (idx+1) % 50 == 0:
            print(f"  {idx+1}/409 cards [{time.time()-t0:.1f}s]", flush=True)
    print(f"[{time.time()-t0:.1f}s] all cards built+validated", flush=True)

print("DONE-DIAG-41", flush=True)
