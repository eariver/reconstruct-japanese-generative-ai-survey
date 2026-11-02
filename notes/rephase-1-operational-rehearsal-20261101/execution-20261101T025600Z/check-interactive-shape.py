import json, sys
from pathlib import Path
WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core, survey_screening_v2 as scr
from scripts.run_evidence_v2_interactive import _validate_record as ev_validate_record
# SP screening decisions (original, 165)
sp_dec = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2g14.interactive-decisions.json").read_bytes())
print("SP decisions file", sp_dec.get("issue_id"), sp_dec.get("schema_version"), "n=", len(sp_dec.get("decisions",[])))
errs=0
for row in sp_dec["decisions"]:
    e = scr.validate_decision(row)
    if e:
        errs+=1
        print(" decision invalid", row.get("discovery_id"), e[:2])
print("SP screening decisions validate_decision errors:", errs, "of", len(sp_dec["decisions"]))
# SP discovery accepted IDs (historical reference for expected coverage, not installed)
sp_acc = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b21.discovery-accepted-v2.json").read_bytes())
print("SP discovery-accepted records", sp_acc.get("record_count"), "ids sample", [r["discovery_id"] for r in sp_acc["records"][:3]])
dec_ids=set(r["discovery_id"] for r in sp_dec["decisions"])
acc_ids=set(r["discovery_id"] for r in sp_acc["records"])
print("SP decisions cover accepted exactly:", dec_ids==acc_ids, "missing", sorted(acc_ids-dec_ids)[:5], "extra", sorted(dec_ids-acc_ids)[:5])
# SP evidence interactive r1 records profile-bound check (fresh SP profile)
sp_prof = core.load_json(WORK/"sources/SP-efficient-llm-2026/production-profile.json")
sp_ev = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c01.interactive-evidence.json").read_bytes())
print("SP evidence r1", sp_ev.get("issue_id"), "records", len(sp_ev.get("records",[])))
errs=0
for row in sp_ev["records"][:5]:
    try:
        ev_validate_record(row, sp_prof)
    except Exception as e:
        errs+=1
        print(" record invalid", row.get("discovery_id"), e)
print("SP evidence r1 first-5 record errors:", errs)
# check all 160 quickly (count only)
err_all=0
for row in sp_ev["records"]:
    try:
        ev_validate_record(row, sp_prof)
    except Exception:
        err_all+=1
print("SP evidence r1 all-record errors:", err_all, "of", len(sp_ev["records"]))
# W34 evidence interactive (409) profile-bound check
w34_prof = core.load_json(WORK/"sources/2026-W34/production-profile.json")
w34_ev = json.loads(Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b18.p2b18").read_bytes())
print("W34 evidence", w34_ev.get("issue_id"), "records", len(w34_ev.get("records",[])))
err_all=0
for row in w34_ev["records"]:
    try:
        ev_validate_record(row, w34_prof)
    except Exception as e:
        err_all+=1
        if err_all<=3:
            print(" record invalid", row.get("discovery_id"), e)
print("W34 evidence all-record errors:", err_all, "of", len(w34_ev["records"]))
