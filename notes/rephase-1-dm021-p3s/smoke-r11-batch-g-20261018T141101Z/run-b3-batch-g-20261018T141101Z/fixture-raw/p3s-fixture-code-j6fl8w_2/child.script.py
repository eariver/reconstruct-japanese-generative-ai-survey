
import json, sys, unittest
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
from tests.test_survey_editorial_staged_source_v2 import _snapshot as _p3s_snapshot
from tests.test_survey_editorial_staged_source_v2 import _assert_no_write as _p3s_assert_no_write
from tests.test_survey_editorial_staged_source_v2 import _assert_no_write_except as _p3s_assert_no_write_except
class _TC(unittest.TestCase):
    def runTest(self):
        pass
tc = _TC()
authored = core.load_json(authored_path)
authored["cover"]["headline"] = "Weekly tested method, revised edition"
staged = p1t._stage_authoring_before_prepare(tc, root, source_root, proposal_id, authored)
snap0 = _p3s_snapshot(root)
prepared = proposal_mod.prepare_proposal(root, state_path, staged, proposal_id,
                                         "Fixture weekly envelope correction.")
_p3s_assert_no_write(tc, snap0, _p3s_snapshot(root), "R1 prepare (fixture code)")
proposal_path = p1t._stage_reader_and_proposal(tc, root, source_root, proposal_id, prepared)
outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
tc.assertEqual(outcome["result"], "REVIEW_REQUIRED")
snap1 = _p3s_snapshot(root)
out = retention.capture_retention(root, state_path, proposal_path)
tc.assertEqual(out["result"], retention.RESULT_CAPTURED)
manifest_path = root / out["manifest_path"]
tc.assertTrue(manifest_path.is_file())
tc.assertEqual(core.sha256_file(manifest_path), out["manifest_sha256"])
vout = retention.verify_retention(root, proposal_path, manifest_path)
tc.assertEqual(vout["result"], retention.RESULT_VERIFIED)
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
after = _p3s_snapshot(root)
tc.assertEqual(set(after) - set(before), new_files | new_dirs, sorted(set(after) - set(before)))
_p3s_assert_no_write_except(tc, before, after, new_files | new_dirs, set(), "R1 capture unchanged-originals")
staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
scope_path = p1t._scope_review_for(tc, root, prepared, staged_reader_rel, scope_name)
print(json.dumps({"state_rel": str(state_path.relative_to(root)),
                  "proposal_rel": str(proposal_path.relative_to(root)),
                  "manifest_rel": str(manifest_path.relative_to(root)),
                  "scope_rel": str(scope_path.relative_to(root)),
                  "headline": authored["cover"]["headline"]}))
