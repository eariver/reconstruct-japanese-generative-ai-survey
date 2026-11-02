"""W34: results from unchanged archived 439 decisions + accept via existing API (strict facade)."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORK = Path(".rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work").resolve()
INTAKE = Path("notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z")
sys.path.insert(0, str(WORK))
from scripts import survey_production_v2 as core
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_screening_v2 as screening

print(f"REAL-CLOCK {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
impl = core.repository_commit_sha(WORK)
assert impl == "480823560c0c26ed2e5baa18e0e79a22b2839a27", impl
print(f"implementation_sha (actual current head): {impl}")

pkg_path = WORK / "sources/2026-W34/screening/proposed-input/expansion-package/package.json"
package = core.load_json(pkg_path)
print(f"package: record_count={package['input']['record_count']} batches={len(package['input']['batches'])} sha={core.sha256_file(pkg_path)[:12]}...")

arch = json.loads((INTAKE / "DATA.p2b05.screening-accepted.json").read_bytes())
print(f"archived decisions source: DATA.p2b05 439 rows sha256={hashlib.sha256((INTAKE / 'DATA.p2b05.screening-accepted.json').read_bytes()).hexdigest()[:12]}...")
by_id = {}
for d in arch["decisions"]:
    errs = screening.validate_decision(d)
    assert not errs, f"archived decision invalid: {d.get('discovery_id')} {errs}"
    assert d["discovery_id"] not in by_id, f"duplicate archived {d['discovery_id']}"
    by_id[d["discovery_id"]] = d
import collections
print(f"archived decisions validate_decision errors: 0/439; counts={dict(collections.Counter(d['decision'] for d in arch['decisions']))}")

res_dir = WORK / "sources/2026-W34/screening/proposed-input/expansion-results"
assert not res_dir.exists(), "owned results dir must be fresh"
res_dir.mkdir(parents=True)
for batch in package["input"]["batches"]:
    inputs = screening.read_jsonl(pkg_path.parent / batch["path"])
    rows = [by_id[r["discovery_id"]] for r in inputs]
    assert len(rows) == len(inputs) and {r["discovery_id"] for r in rows} == {r["discovery_id"] for r in inputs}
    result = {
        "schema_version": "2.0-rc1",
        "issue_id": package["issue_id"],
        "batch_id": batch["batch_id"],
        "basis": screening.expected_result_basis(WORK, pkg_path, package, batch),
        "decisions": rows,
    }
    core.write_json(res_dir / f"{batch['batch_id']}.json", result)
print(f"results written: {len(package['input']['batches'])} files (decisions verbatim archived, basis real per-batch)")

prov = {
    "reuse": "archived W34 screening decisions reused verbatim (no status/wording change)",
    "archived_source": {"packet": str(INTAKE / "DATA.p2b05.screening-accepted.json"), "record_count": 439, "counts": {"KEEP": 73, "MAYBE": 136, "INSPECT": 200, "DROP": 30}},
    "justification": "independent SourceIntake BOUNDED PROCEED (reviews/source-intake-review-20261101T104700Z.md 1d46058e/38557B); event set validated vs R369 (expansion accounting 369/369, DECLARATION_LOSS none)",
    "operator_attribution": "embedded per-decision reason/confidence/scope_tags/verification_targets preserved verbatim; historical runner identity NOT claimed (audit not fetched)",
    "not_rebound": "old package/record/result SHAs not reused; fresh package basis only",
}
core.write_json(WORK / "sources/2026-W34/screening/proposed-input/reuse-provenance.json", prov)
print("reuse provenance recorded (packet-side detail in logs/status, not in results/)")

with agent_tool.current_stage_basis_override():
    accepted = screening.accept_results(WORK, pkg_path, res_dir, WORK / "sources/2026-W34/screening/v2/accepted", impl)
print(f"ACCEPTED: {Path(accepted).relative_to(WORK)}")
acc = core.load_json(accepted)
print(f"record_count={acc['record_count']} batch_count={acc['batch_count']} result_set={acc['result_set_sha256'][:12]}... package={acc['package_sha256'][:12]}...")
print("DONE-ACCEPT (product only; NO checkpoint, NO state advance)")
