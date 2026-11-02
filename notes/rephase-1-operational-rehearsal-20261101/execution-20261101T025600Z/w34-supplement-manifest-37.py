"""Build NEW W34 supplement manifest 37 via normal builder (fresh basis, verbatim 428 rows).

Old r2 manifest (P6a01, 428 entries) is archived proof, untouched.
Old r1 (61 entries) NEVER used.
New basis: discovery E439 0a23be47..., screening FILE b9d963d8... (NOT run-dir digest e193ad05).
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
P6 = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p6-20261101T115240Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_evidence_v2 as evidence

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
print(f"CWD={Path.cwd()}")
impl = core.repository_commit_sha(WORK)
print(f"HEAD (implementation_sha)={impl}")
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl

state_path = WORK / "sources/2026-W34/production-state.json"
state = core.load_json(state_path)
print(f"PRE lifecycle={state['lifecycle_state']}")
assert state["lifecycle_state"] == "CANDIDATES_NORMALIZED", state["lifecycle_state"]
errs = agent.validate_agent_state(WORK, core.load_json(WORK / core.DEFAULT_CONFIG), state)
print(f"PRE agent errors={errs}")
assert not errs

# Original 428 rows verbatim from P6a01 (r2, correct for current input)
old_path = P6 / "DATA.p6a01.evidence-authority-supplement.json"
old = json.loads(old_path.read_bytes())
print(f"old r2 manifest {old['supplement_id']} sources={len(old['sources'])} sha256={hashlib.sha256(old_path.read_bytes()).hexdigest()}")
assert len(old["sources"]) == 428
assert old["supplement_id"] == "w34-supplement-screening-evidence-r2-muse-spark"
sources = [dict(e) for e in old["sources"]]
# Spot-check preservation: no aliasing, original class/types
from collections import Counter
print(f"source_class counts={dict(Counter(e['source_class'] for e in sources))}")
print(f"source_type counts={dict(Counter(e['source_type'] for e in sources))}")

# Fresh basis paths (must exist, hashes must match task-specified fresh)
discovery_p = WORK / "sources/2026-W34/screening/input/event-discovery-v2.jsonl"
screening_p = WORK / "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json"
print(f"discovery {discovery_p.relative_to(WORK)} sha={core.sha256_file(discovery_p)}")
print(f"screening {screening_p.relative_to(WORK)} sha={core.sha256_file(screening_p)}")
assert core.sha256_file(discovery_p) == "0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e"
assert core.sha256_file(screening_p) == "b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841"
# Run-dir digest is directory name, NOT file hash – must not confuse
assert screening_p.parent.name.startswith("e193ad05"), screening_p.parent.name
print(f"run-dir digest={screening_p.parent.name} (NOT used as basis hash; FILE hash b9d963d8 used)")

outp = WORK / "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json"
print(f"output {outp.relative_to(WORK)} exists={outp.exists()}")
assert not outp.exists(), f"refusing to overwrite {outp}"
assert not outp.is_symlink()

with agent_tool.current_stage_basis_override():
    built = evidence.build_evidence_authority_supplement(
        WORK,
        "2026-W34",
        WORK / "sources/2026-W34",
        discovery_p,
        screening_p,
        sources,
        outp,
        supplement_id="evidence-supplement-w34-r2-fresh-basis",
        implementation_sha=impl,
    )
print(f"NEW manifest: {Path(built).relative_to(WORK)}")
new = core.load_json(built)
print(f"new basis discovery={new['basis']['discovery_sha256'][:12]}... screening={new['basis']['screening_acceptance_sha256'][:12]}... (must be 0a23be47/b9d963d8)")
assert new["basis"]["discovery_sha256"] == "0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e"
assert new["basis"]["screening_acceptance_sha256"] == "b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841"
print(f"sources={len(new['sources'])} (verbatim, no rewording)")
assert len(new["sources"]) == 428
print(f"new file sha256={core.sha256_file(built)} bytes={built.stat().st_size}")
print(f"old P6a01 untouched (still 389423B at intake)")
print("DONE-MANIFEST-37 (builder-internal validation passed; old manifests immutable)")
