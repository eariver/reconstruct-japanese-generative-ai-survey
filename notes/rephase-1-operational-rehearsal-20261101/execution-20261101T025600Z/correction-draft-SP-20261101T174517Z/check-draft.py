#!/usr/bin/env python3
"""Read-only draft checks for SP correction (no canonical writes, no State advance).
Harness outside control roots (packet dir). Uses verified workdir inputs as DATA.
Checks: record fields (no new keys), coverage 160, old13 verbatim, new17 task/class/pattern,
bindings match, completeness universe (keyword-only 3 vs 5), status enums.
Supplement full Raw validation intentionally NOT run (Raw not staged by design).
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(WORK))
from scripts import survey_evidence_v2 as evidence
from scripts.run_evidence_v2_interactive import _validate_record, _validate_completeness_input, COMMON_RECORD_FIELDS, THEMATIC_RECORD_FIELDS, CARD_STATUS, VERIFY_STATUS
def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
profile = json.loads((WORK/"sources/SP-efficient-llm-2026/production-profile.json").read_text())
disc = [json.loads(l) for l in (WORK/"sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl").read_text().splitlines() if l.strip()]
new = json.loads((OUT/"new-input.json").read_text())
assert set(new)=={"schema_version","issue_id","runner","records","completeness"}
allowed = COMMON_RECORD_FIELDS|THEMATIC_RECORD_FIELDS|{"source_bindings"}
for r in new["records"]:
    assert set(r)-allowed==set(), r["discovery_id"]
    _validate_record(r, profile)
print("records 160 PASS")
acc = json.loads((WORK/"sources/SP-efficient-llm-2026/screening/v2/accepted/9b9796295c2ddf28b087fc725b78b7d089d6e946a5a5ba65ab51601d58f558a9/screening-accepted.json").read_text())
non_drop=set(d["discovery_id"] for d in acc["decisions"] if d["decision"]!="DROP")
assert set(r["discovery_id"] for r in new["records"])==non_drop
print("coverage PASS")
prop = json.loads((OUT/"new-supplement-proposal.json").read_text())
old = json.loads((WORK/"sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json").read_text())
assert prop["sources"][:13]==old["sources"]
print("old13 verbatim PASS")
pat=re.compile(r"^supplement-src-[0-9a-f]{16}$")
for s in prop["sources"][13:]:
    assert pat.match(s["supplement_source_id"])
    assert s["evidence_task_id"]==evidence.stable_task_id("SP-efficient-llm-2026", s["discovery_id"])
    assert s["source_class"]==evidence._source_class(s["source_type"])
print("new17 PASS")
ids=json.loads((OUT/"new-supplement-ids.json").read_text())
for did,m in ids.items():
    rec=next(r for r in new["records"] if r["discovery_id"]==did)
    assert rec["source_bindings"]==[m["supp"]]
print("bindings PASS")
_validate_completeness_input(new["completeness"], profile, discovery_records=disc, root_discovery_records=disc)
print("completeness PASS")
for r in new["records"]:
    assert r["status"] in CARD_STATUS
    for v in r["verification"]:
        assert v["status"] in VERIFY_STATUS
print("enums PASS")
for fn in ["current-outputs-machine.json","new-supplement-proposal.json","new-supplement-ids.json","new-input.json","new-input-delta.json"]:
    p=OUT/fn
    print(fn, p.stat().st_size, sha(p))
print("DONE-CHECK-DRAFT (read-only, no canonical mutation, no State advance)")
