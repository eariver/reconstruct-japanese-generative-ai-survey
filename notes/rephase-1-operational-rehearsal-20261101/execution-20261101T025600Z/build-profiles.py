import json, sys
from pathlib import Path
from datetime import datetime
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
cfg = core.load_json(WORK / core.DEFAULT_CONFIG)
print("cfg schema", cfg.get("schema_version"), "orchestrator", cfg.get("orchestrator_version"))
print("HEAD", core.repository_commit_sha(WORK))
# W34 authorized for comparison
w34auth = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z/../intake-20261101T023147Z/../../rephase-1-operational-rehearsal-20261101/../../.rephase-1-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-profile.json").read_text()) if False else None
# Build W34 via normal factory
now_w34 = core.parse_instant("2026-08-25T00:00:00Z")
prof_w34 = core.weekly_profile(WORK, cfg, now_w34, "2026-W34")
print("W34 profile", prof_w34["issue_id"], prof_w34["research_profile"], prof_w34["publication_profile"])
print("W34 question", prof_w34["research_scope"]["question"][:120])
print("W34 temporal", prof_w34["research_scope"]["temporal_policy"])
print("W34 dims", prof_w34["research_scope"]["scope_dimensions"])
print("W34 obligs", [o["obligation_id"] for o in prof_w34["research_scope"]["initial_obligations"]])
print("W34 paths", prof_w34["paths"])
# SP authorized bytes
spauth = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z/DATA.production-profile.json").read_text())
spec = {
  "issue_id": spauth["issue_id"],
  "question": spauth["research_scope"]["question"],
  "temporal_mode": spauth["research_scope"]["temporal_policy"]["mode"],
  "as_of": spauth["research_scope"]["temporal_policy"]["as_of"],
  "scope_dimensions": list(spauth["research_scope"]["scope_dimensions"]),
  "inclusion": list(spauth["research_scope"].get("inclusion", [])),
  "exclusion": list(spauth["research_scope"].get("exclusion", [])),
  "initial_obligations": [dict(o) for o in spauth["research_scope"]["initial_obligations"]],
  "source_root": spauth["paths"]["source_root"],
  "survey_root": spauth["paths"]["survey_root"],
  "work_branch": spauth["paths"]["work_branch"],
}
prof_sp = core.thematic_profile(WORK, cfg, spec)
print("SP profile", prof_sp["issue_id"], prof_sp["research_profile"], prof_sp["publication_profile"])
print("SP temporal", prof_sp["research_scope"]["temporal_policy"])
print("SP dims n", len(prof_sp["research_scope"]["scope_dimensions"]))
# Compare question/dims/asof preserved
assert prof_sp["research_scope"]["question"] == spauth["research_scope"]["question"], "SP question drift"
assert prof_sp["research_scope"]["scope_dimensions"] == spauth["research_scope"]["scope_dimensions"], "SP dims drift"
assert prof_sp["research_scope"]["temporal_policy"] == spauth["research_scope"]["temporal_policy"], "SP temporal drift"
assert prof_sp["paths"] == spauth["paths"], "SP paths drift"
print("SP preserved question/window/dims/paths OK; contract fresh from current implementation")
# Initialize both (ISSUE_INITIALIZED) with true HEAD
head = core.repository_commit_sha(WORK)
from pathlib import Path as P
pw34, sw34 = core.initialize(WORK, cfg, prof_w34, head, "ARCHITECTURE_REVIEW", core.parse_instant("2026-08-25T00:00:00Z"))
print("W34 initialized", pw34.relative_to(WORK), sw34.relative_to(WORK))
psp, ssp = core.initialize(WORK, cfg, prof_sp, head, "ARCHITECTURE_REVIEW", core.parse_instant("2026-09-21T16:10:00Z"))
print("SP initialized", psp.relative_to(WORK), ssp.relative_to(WORK))
