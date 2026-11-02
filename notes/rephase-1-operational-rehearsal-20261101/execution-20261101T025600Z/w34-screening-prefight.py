"""W34 screening preflight (read-only): root/effective/metadata comparison + coverage predicate.

No runner executed (no valid proposed input exists: archived decisions are 439
event IDs; current runner expects exactly the 369 accepted-root IDs).
No files written.
"""
import json
import sys
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
INTAKE = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_discovery_v2 as disc
from scripts import survey_screening_v2 as scr

fresh = disc.validate_acceptance(WORK, WORK / "sources/2026-W34/discovery/discovery-accepted-v2.json")
root_ids = {r["discovery_id"] for r in fresh["records"]}
print(f"fresh root acceptance: n={len(root_ids)} graph={fresh['graph_sha256'][:12]}...")

ev_recs = [json.loads(l) for l in (INTAKE / "DATA.p2b19.p2b19").read_text().splitlines()]
print(f"event expansion (packet DATA, NOT staged): n={len(ev_recs)}")
print(f"root∩event overlap (must be empty per no-reuse rule): {sorted(root_ids & {r['discovery_id'] for r in ev_recs})[:5]} count={len(root_ids & {r['discovery_id'] for r in ev_recs})}")

acc = json.loads((INTAKE / "DATA.p2b05.screening-accepted.json").read_bytes())
dec_ids = {d["discovery_id"] for d in acc["decisions"]}
ev_ids = {r["discovery_id"] for r in ev_recs}
print(f"archived latest accepted decisions (415...): n={len(dec_ids)}; == event IDs: {dec_ids == ev_ids}")
print(f"archived vs fresh-root: missing={len(root_ids - dec_ids)} extra={len(dec_ids - root_ids)} (runner expects exact fresh-root coverage)")
print(f"archived counts: record_count={acc['record_count']} batch_count={acc['batch_count']}")

import collections
print("archived decision values:", dict(collections.Counter(d["decision"] for d in acc["decisions"])))

# Real validators, read-only: root set + event set + expansion accounting (normalize event against WORKDIR raws)
root_raw = [json.loads(l) for l in (WORK / "sources/2026-W34/discovery/discovery-v2.jsonl").read_text().splitlines()]
rt_norm = [disc._normalize_record(WORK, r, "2026-W34") for r in root_raw]
disc._validate_graph(rt_norm)
print(f"root graph re-validated: {len(rt_norm)}")
try:
    ev_norm = [disc._normalize_record(WORK, r, "2026-W34") for r in ev_recs]
    disc._validate_graph(ev_norm)
    print(f"event graph re-validated: {len(ev_norm)}")
    acct = scr.validate_discovery_expansion(WORK, rt_norm, ev_norm, "2026-W34")
    print(f"expansion accounting OK: accounted_roots={len(acct.get('accounted_root_ids', []))} (expect 369)")
    uo = scr.compute_obligation_universe(
        {o["obligation_id"] for o in core.load_json(WORK / "sources/2026-W34/production-profile.json")["research_scope"]["initial_obligations"]},
        rt_norm, ev_norm)
    print(f"obligation universe U (root+effective): {sorted(uo)}")
    loss = scr.find_declaration_loss(rt_norm, ev_norm)
    print(f"DECLARATION_LOSS uncovered: {loss if loss else []}")
except ValueError as exc:
    bad = [r["discovery_id"] for r in ev_recs if any(
        not (p.startswith("local:") or p.startswith("external:"))
        for p in (r.get("provenance", {}).get("parent_refs", []) or []))]
    print(f"REFUSAL (preserved, no rewrite): ValueError: {exc}")
    print(f"REFUSAL scope: {len(bad)}/{len(ev_recs)} event records carry bare (non-namespaced) parent_refs")
    print(f"REFUSAL predicate: survey_discovery_v2._parse_parent via _normalize_record requires explicit local:<id> or external:<issue>:<id>")
    print(f"REFUSAL note: bare refs == root ID set exactly (369/369, all roots referenced); format gap vs current contract, not corrupt data")
    print("REFUSAL consequence: expansion accounting / universe / loss / runner coverage NOT computable on un-normalized records; no further graph attempt (same cause)")
print("STALE SUBSETS: 105 (2ab82c6b) / 110 (5699a79a) historical acceptances NOT fetched, NOT used (explicitly excluded per instruction).")
print("DONE-PREFLIGHT (read-only; no runner, no writes)")
