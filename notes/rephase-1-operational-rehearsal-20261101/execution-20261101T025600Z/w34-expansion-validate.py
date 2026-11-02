"""W34 E439 read-only validation (no writes): schema, expansion vs R369, universe, loss."""
import hashlib
import json
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
INTAKE = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_screening_v2 as scr
from scripts import survey_discovery_v2 as disc

ev_bytes = (INTAKE / "DATA.p2b19.p2b19").read_bytes()
print(f"event DATA: {len(ev_bytes)}B sha256={hashlib.sha256(ev_bytes).hexdigest()} blob-sha1={hashlib.sha1(b'blob '+str(len(ev_bytes)).encode()+b'\\x00'+ev_bytes).hexdigest()}")
assert len(ev_bytes) == 1335444, "event blob size must equal tree size 1335444"
ev = [json.loads(l) for l in ev_bytes.decode().splitlines()]
print(f"event records: {len(ev)}")

rt_raw = [json.loads(l) for l in (WORK / "sources/2026-W34/discovery/discovery-v2.jsonl").read_text().splitlines()]
print(f"root records (workdir): {len(rt_raw)}")
scr.validate_discovery_set(rt_raw, "2026-W34")
print("root validate_discovery_set: PASS")
scr.validate_discovery_set(ev, "2026-W34")
print("event validate_discovery_set: PASS")

acct = scr.validate_discovery_expansion(WORK, rt_raw, ev, "2026-W34")
print(f"expansion accounting: accounted_roots={len(acct.get('accounted_root_ids', []))} mode=DERIVED_EXPANSION")

prof = core.load_json(WORK / "sources/2026-W34/production-profile.json")
initial = {o["obligation_id"] for o in prof["research_scope"]["initial_obligations"]}
uo = scr.compute_obligation_universe(initial, rt_raw, ev)
print(f"universe U: {sorted(uo)}")
loss = scr.find_declaration_loss(rt_raw, ev)
print(f"DECLARATION_LOSS uncovered: {loss if loss else []}")

import collections
print("archived decisions (packet ref): KEEP73/MAYBE136/INSPECT200/DROP30 n=439 (p2b05, verified earlier: exact event-ID match)")
print("DONE-EXPANSION-VALIDATE (read-only; no staging, no package, no writes)")
