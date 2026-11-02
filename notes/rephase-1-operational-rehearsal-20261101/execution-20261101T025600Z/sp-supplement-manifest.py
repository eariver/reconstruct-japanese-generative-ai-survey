"""Build NEW SP supplement manifest via existing builder (fresh basis, verbatim sources)."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
P2 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_evidence_v2 as evidence

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
old = json.loads((P2 / "DATA.p2f02.evidence-authority-supplement-r1.json").read_bytes())
print(f"old manifest: {old['supplement_id']} sources={len(old['sources'])} (archived, untouched)")
assert len(old["sources"]) == 13

# Reuse 13 source rows verbatim (same locators/titles/timestamps/raw refs; staged bytes verified in log 25)
sources = [dict(e) for e in old["sources"]]
impl = core.repository_commit_sha(WORK)
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl
outp = WORK / "sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json"
assert not outp.exists()
# Strict facade: accepted screening package legitimately retains the State SHA from
# the earlier DISCOVERY_COLLECTED boundary (wrapper re-checks everything else strictly).
with agent_tool.current_stage_basis_override():
    built = evidence.build_evidence_authority_supplement(
        WORK,
        "SP-efficient-llm-2026",
        WORK / "sources/SP-efficient-llm-2026",
        WORK / "sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl",
        WORK / "sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json",
        sources,
        outp,
        supplement_id="evidence-supplement-sp-efficient-llm-2026-r1-fresh-basis",
        implementation_sha=impl,
    )
print(f"NEW manifest: {Path(built).relative_to(WORK)}")
new = core.load_json(built)
print(f"basis discovery: {new['basis']['discovery_sha256'][:12]}... screening: {new['basis']['screening_acceptance_sha256'][:12]}... (fresh acceptance, NOT old 24bac6aa)")
print(f"sources: {len(new['sources'])} (verbatim reuse, no rewording)")
print("DONE-MANIFEST (builder-internal validation passed; old manifest untouched)")
