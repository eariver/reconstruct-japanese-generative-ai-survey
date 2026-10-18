
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2])
authored_path = Path(sys.argv[3])
source_root = Path(sys.argv[4])
proposal_id = sys.argv[5]
scope_name = sys.argv[6]
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
from scripts import survey_editorial_retention_v2 as retention
from tests import test_survey_editorial_correction_proposal_v2 as p1t
class _Asserts:
    def assertEqual(self, a, b, msg=""):
        assert a == b, f"{msg}: {a!r} != {b!r}"
    def assertTrue(self, v, msg=""):
        assert bool(v), msg
    def assertFalse(self, v, msg=""):
        assert not v, f"{msg}: {v!r}"
    def assertIn(self, m, c, msg=""):
        assert m in c, f"{msg}: {m!r} not in container"
    def assertNotIn(self, m, c, msg=""):
        assert m not in c, f"{msg}: {m!r} unexpectedly present"
tc = _Asserts()
authored = core.load_json(authored_path)
authored["cover"]["headline"] = "Weekly tested method, revised edition"
snap0 = p1t._snapshot(root)
staged = p1t._stage_authoring_before_prepare(tc, root, source_root, proposal_id, authored)
prepared = proposal_mod.prepare_proposal(root, state_path, staged, proposal_id,
                                         "Fixture weekly envelope correction.")
p1t._assert_no_write(tc, snap0, p1t._snapshot(root), "R1 prepare (fixture code)")
proposal_path = p1t._stage_reader_and_proposal(tc, root, source_root, proposal_id, prepared)
outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
assert outcome["result"] == "REVIEW_REQUIRED", outcome["result"]
snap1 = p1t._snapshot(root)
out = retention.capture_retention(root, state_path, proposal_path)
assert out["result"] == retention.RESULT_CAPTURED, out["result"]
manifest_path = root / out["manifest_path"]
assert manifest_path.is_file()
assert core.sha256_file(manifest_path) == out["manifest_sha256"]
vout = retention.verify_retention(root, proposal_path, manifest_path)
assert vout["result"] == retention.RESULT_VERIFIED, vout["result"]
manifest = core.load_json(manifest_path)
new_files = {out["manifest_path"]} | {r["retained_dest"] for r in manifest["rows"]
                                      if r["policy"] == "COPY_BEFORE_REPLACEMENT"}
retained_rel = Path(out["manifest_path"]).parent.as_posix()
new_dirs = {retained_rel}
for frel in new_files:
    parts = Path(frel).parts
    cur = list(parts[:-1])
    while len(cur) >= len(Path(retained_rel).parts):
        cand = Path(*cur).as_posix()
        if cand == retained_rel or cand.startswith(retained_rel + "/"):
            new_dirs.add(cand)
        if cand == retained_rel:
            break
        cur = cur[:-1]
before = dict(snap1)
after = p1t._snapshot(root)
assert set(after) - set(before) == new_files | new_dirs, sorted(set(after) - set(before))
for rel, data in before.items():
    assert after.get(rel) == data, f"R1 capture changed live entry: {rel}"
staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
scope_path = p1t._scope_review_for(tc, root, prepared, staged_reader_rel, scope_name)
print(json.dumps({"state_rel": str(state_path.relative_to(root)),
                  "proposal_rel": str(proposal_path.relative_to(root)),
                  "manifest_rel": str(manifest_path.relative_to(root)),
                  "scope_rel": str(scope_path.relative_to(root)),
                  "headline": authored["cover"]["headline"]}))
