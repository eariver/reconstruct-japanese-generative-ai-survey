import json, sys
from pathlib import Path
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core, survey_discovery_v2 as disc, survey_screening_v2 as scr, survey_evidence_v2 as ev, survey_completeness_v2 as comp, survey_schema_v2 as sg
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
for issue, rel in [("2026-W34","sources/2026-W34"),("SP-efficient-llm-2026","sources/SP-efficient-llm-2026")]:
  pp = WORK / rel / "production-profile.json"
  sp = WORK / rel / "production-state.json"
  prof = core.load_json(pp)
  st = core.load_json(sp)
  print(f"== {issue} ==")
  print(" profile", prof["issue_id"], prof["research_profile"], prof["publication_profile"], "contract", prof["contract"]["pipeline_contract_version"])
  print(" state", st["lifecycle_state"], "impl", st["implementation"]["repository_commit_sha"][:8], "target", st.get("target_gate"))
  errs = core.validate_profile(prof, cfg)
  print(" validate_profile errors:", errs)
  from scripts import survey_agent_control_v2 as agent
  aerr = agent.validate_agent_state(WORK, cfg, st)
  print(" agent_state errors:", aerr)
  # discovery JSONL data-read
  dpath = WORK / rel / "discovery/discovery-v2.jsonl"
  recs = disc.read_jsonl(dpath)
  print(f" discovery JSONL n={len(recs)} first_id={recs[0].get('discovery_id') if recs else None}")
  try:
    norm = [disc._normalize_record(WORK, r, issue) for r in recs]
    disc._validate_graph(norm)
    print(f" discovery graph OK n={len(norm)}")
    # root/effective split? compute obligation universe inputs need screening? just report parent_refs presence
    import collections
    pr = sum(1 for r in norm if r.get("parent_refs"))
    print(f" records with parent_refs: {pr}")
  except Exception as e:
    print(f" discovery graph FAIL: {e}")
