"""W34 final verify 42 + pending semantic inventory (no Evidence accept, no advance).

Checks canonical State/Profile/impl/artifacts, supplement/rawd staged, SP untouched,
evidence/v2 absent, HEAD unchanged. Writes pendingSemanticReview inventory (packet only).
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
P6 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p6-20261101T115240Z")
PACKET = Path("notes/rephase-1-operational-rehearsal-20261101/execution-20261101T025600Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}", flush=True)
impl = core.repository_commit_sha(WORK)
print(f"HEAD={impl}", flush=True)
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl

# W34 canonical
sp = WORK / "sources/2026-W34/production-state.json"
st = core.load_json(sp)
print(f"W34 lifecycle={st['lifecycle_state']} next={st.get('next_action')}", flush=True)
assert st["lifecycle_state"] == "CANDIDATES_NORMALIZED"
assert not agent.validate_agent_state(WORK, core.load_json(WORK / core.DEFAULT_CONFIG), st)
print(f"W34 state sha={core.sha256_file(sp)}", flush=True)
print(f"W34 profile sha={core.sha256_file(WORK / 'sources/2026-W34/production-profile.json')}", flush=True)
print(f"W34 screening FILE sha={core.sha256_file(WORK / 'sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json')}", flush=True)
print(f"W34 discovery E439 sha={core.sha256_file(WORK / 'sources/2026-W34/screening/input/event-discovery-v2.jsonl')}", flush=True)
print(f"W34 checkpoint DISCOVERY_COLLECTED sha={core.sha256_file(WORK / 'sources/2026-W34/orchestration/v2/checkpoints/DISCOVERY_COLLECTED.json')}", flush=True)
print(f"W34 stage report sha={core.sha256_file(WORK / 'sources/2026-W34/orchestration/v2/stage-validation/DISCOVERY_COLLECTED-report.json')}", flush=True)

# Supplement NEW + raws staged
supp = WORK / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"
print(f"NEW supplement exists={supp.exists()} sha={core.sha256_file(supp) if supp.exists() else None} bytes={supp.stat().st_size if supp.exists() else 0}", flush=True)
assert supp.exists()
# Count staged raws under evidence-bodies + official-fallback (425 distinct)
import os
roots = [
    WORK / "sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-bodies",
    WORK / "sources/2026-W34/execution/luna/w34-discovery-gapfill-after-sol-review-r1",
]
cnt = 0
for r in roots:
    if r.exists():
        cnt += sum(1 for _, _, fs in os.walk(r) for f in fs if not f.endswith((".headers", ".curl-stderr")))
print(f"staged raw files (approx, excl sidecars)={cnt}", flush=True)

# Evidence/v2 must still be absent (38 hung, killed, no overwrite)
ev2 = WORK / "sources/2026-W34/evidence/v2"
print(f"evidence/v2 exists={ev2.exists()} (must be False)", flush=True)
assert not ev2.exists()

# SP untouched
sp_state = core.load_json(WORK / "sources/SP-efficient-llm-2026/production-state.json")
print(f"SP lifecycle={sp_state['lifecycle_state']} (must be CANDIDATES_NORMALIZED, CHANGES_REQUIRED hold)", flush=True)
assert sp_state["lifecycle_state"] == "CANDIDATES_NORMALIZED"

# Input 409 + 49 VERIFIED inventory for pending review (historical statuses, NOT new judgment)
inp = core.load_json(WORK / "sources/2026-W34/evidence/proposed-input/interactive-evidence.json")
from collections import Counter
print(f"input records={len(inp['records'])} statuses={dict(Counter(r['status'] for r in inp['records']))}", flush=True)
ver = [r for r in inp["records"] if r["status"] == "VERIFIED"]
print(f"VERIFIED input records={len(ver)} (historical, NOT new authority)", flush=True)
# Build pending file (packet only, no shipping write)
pend = PACKET / "w34-pending-semantic-review-42.md"
lines = []
lines.append("# W34 pending semantic review — Evidence structural accept BLOCKED by capability gap (no accepted products yet)")
lines.append("")
lines.append(f"- Workdir HEAD `{impl}` (unchanged), W34 `{st['lifecycle_state']}`, no `EVIDENCE_REVIEWED` advance, no `evidence/v2` (38 hung/killed, 41 diag confirms).")
lines.append(f"- Input `interactive-evidence.json` 1573186B `3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27` 409 records (352 PARTIAL/49 VERIFIED/8 NEEDS_MORE historical).")
lines.append(f"- NEW supplement `evidence-authority-supplement-r2-fresh-basis.json` `{core.sha256_file(supp)}` 389414B, 428 rows verbatim from r2, basis E439 `0a23be47...` + screening FILE `b9d963d8...` (NOT run-dir digest). Old r1 61 NEVER used, old r2 389423B immutable.")
lines.append(f"- Staged 425 distinct Raws (189286753B distinct, 426 DATA incl manifest) at original `sources/2026-W34/...` paths, verified size+sha+blob+manifest+r2 (log 36). Extension HTML≠full-body semantic; bytes≠VERIFIED.")
lines.append("- NO auto-VERIFIED: historical VERIFIED (49) are input statuses, NOT independent research approval. Core validation class≠claim truth. Full independent Evidence approval later, requires root dispatch.")
lines.append("")
lines.append("## 49 VERIFIED input records — body-coverage inventory (exact DID/claim/source/Raw/limit)")
lines.append("")
# Map supplement IDs to Raw paths via NEW supplement
new_man = core.load_json(supp)
sid_to_entry = {e["supplement_source_id"]: e for e in new_man["sources"]}
for r in sorted(ver, key=lambda x: x["discovery_id"]):
    did = r["discovery_id"]
    sids = r.get("source_bindings", [])
    # First claim text truncated, entity, materiality
    ent = r.get("entity", {})
    claims = r.get("claims", [])
    first_claim = claims[0]["text"][:160].replace("\n", " ") if claims else "(no claims)"
    for sid in sids:
        e = sid_to_entry.get(sid, {})
        lines.append(f"- `{did}` status=VERIFIED (historical) binds `{sid}`")
        lines.append(f"  - entity `{ent.get('entity_id')}` type={ent.get('entity_type')} url={ent.get('canonical_url')}")
        lines.append(f"  - claim: \"{first_claim}...\" class={claims[0].get('evidence_class') if claims else '?'}")
        lines.append(f"  - primary source: locator={e.get('locator')} class={e.get('source_class')}/{e.get('source_type')} title={e.get('title')}")
        lines.append(f"  - Raw: `{e.get('raw_path')}` bytes={e.get('byte_count')} sha256={e.get('raw_sha256')}")
        lines.append(f"  - verification limit: bytes staged ≠ publisher truth; needs independent body-consumption with AUTHORITY_* per governance §4.2; window/identity/chronology/vendor-vs-independent/carryover/X-as-lead still pending per Screening residuals.")
        lines.append("")
lines.append("## Load-bearing PARTIAL (sample, NOT exhaustive — full review needs accepted Evidence)")
lines.append("")
part = [r for r in inp["records"] if r["status"] == "PARTIAL"][:5]
for r in part:
    lines.append(f"- `{r['discovery_id']}` PARTIAL, materiality={r.get('materiality')}, window={r.get('window_relation')}, bindings={len(r.get('source_bindings', []))} (sample; full 352 need same body-consumption check).")
lines.append("")
lines.append("## Capability gap blocking structural accept (exact, no bypass)")
lines.append("")
lines.append("- `run_evidence_v2_interactive.run` hangs in `task_authority_sources` → `_supplement_entries_for_package` re-validating 425-file/189MB supplement per task (409x ≈77GB+ per phase, 228GB observed in 14min, 99.9% CPU, linear 280MB/s, no progress). Logs 38 (killed 143, PRE-only, no evidence/v2) + 41 diag (17GB in 1min in same function, killed 143).")
lines.append("- Existing impl, no source change allowed, no test-stub/validator patch. Requires Root/Astra decision: cache validation, or narrower scope, or documented performance limit. Do NOT retry same path (duplicates blowup).")
lines.append("- Preserved: blocked 34/35, provider-failure partial (6 pre-existing Raws), 36 staged 425 verified, 37 NEW manifest built, 38 hung/killed with no overwrite, 39 state-drift proof (override required), 40 package OK 5.6s, 41 blowup proof.")
pend.write_text("\n".join(lines) + "\n")
print(f"pending review written {pend} bytes={pend.stat().st_size}", flush=True)
print("DONE-FINAL-VERIFY-42 (still CANDIDATES_NORMALIZED, no advance, no whole PASS)", flush=True)
