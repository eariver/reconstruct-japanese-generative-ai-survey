"""W34 evidence prep (read-only verify + input staging; NO runner: supplement blocked)."""
import collections
import hashlib
import json
import shutil
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
P2 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))

inp = P2 / "DATA.p2b18.p2b18"
b = inp.read_bytes()
print(f"input DATA: {len(b)}B sha256={hashlib.sha256(b).hexdigest()}")
assert len(b) == 1573186
doc = json.loads(b)
assert doc["issue_id"] == "2026-W34" and doc["schema_version"] == "2.0-rc1"
print(f"records={len(doc['records'])} statuses={dict(collections.Counter(r['status'] for r in doc['records']))}")
comp = doc["completeness"]
print(f"completeness obligs={[(o['obligation_id'], o['status'], sorted(o.keys())) for o in comp['obligations']]} closure={comp.get('closure')}")
assert {o["obligation_id"] for o in comp["obligations"]} == {"weekly:current-relevance", "weekly:technical-significance", "weekly:carry-over"}
assert all(set(o) == {"obligation_id", "status", "rationale"} for o in comp["obligations"])
nb = sum(1 for r in doc["records"] if "source_bindings" in r)
print(f"records with source_bindings: {nb}/409")
need = {sb for r in doc["records"] for sb in (r.get("source_bindings") or [])}
print(f"distinct needed supplement IDs: {len(need)}")

old = json.loads((P2 / "DATA.p2d01.evidence-authority-supplement.json").read_bytes())
print(f"old r1 manifest: {old['supplement_id']} sources={len(old['sources'])}")
print(f"old basis discovery: {old['basis']['discovery_path']} {old['basis']['discovery_sha256'][:12]}... (fresh event: 0a23be47...)")
print(f"old basis screening: {old['basis']['screening_acceptance_path'].split('/')[-2][:12]}... {old['basis']['screening_acceptance_sha256'][:12]}... (fresh: e193ad05...)")
man = {e["supplement_source_id"] for e in old["sources"]}
print(f"needed - r1manifest: {len(need - man)} (r1 rows CANNOT bind this input)")
print(f"unbound records (no bindings): {sum(1 for r in doc['records'] if 'source_bindings' not in r)}")
dst = WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json"
if dst.exists():
    assert dst.read_bytes() == b, "proposed input exists with different bytes"
    print("proposed input already staged identical")
else:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(inp, dst)
    print(f"staged proposed input: {dst.relative_to(WORK)}")
print("BLOCKED: r2 supplement manifest (tree: .../w34-screening-evidence-after-sol-discovery-r2/evidence-authority-supplement.json 389423B blob 88f5f337...) + its raws not captured; intake fetch required (same ref, no new permission). Old r1 manifest basis stale on 3 axes; no rebind, no runner.")
print("DONE-PREP (no runner executed)")
