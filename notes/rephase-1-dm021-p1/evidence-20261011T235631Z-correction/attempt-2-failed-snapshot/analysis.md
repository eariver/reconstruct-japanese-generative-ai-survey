# Attempt-2 analysis (failed, preserved)

Run exit=1, 36 tests, 2567s, 8 failures + 2 errors (gate 27/27 OK).

## Snapshot-timing systemic (6 subfailures + 1 weekly)

All scope/retention/weekly negatives took `snap = _snapshot` BEFORE setup
mutation (scope file creation, occupant creation, upstream tamper), so the
injected file itself caused `files` diff. Fix: snapshot AFTER mutation,
immediately before the P1 call (records deliberate delta, proves P1 adds no
further write). Fixed for weekly draft/synthesis/archive (snap after
write_json), retention occupant (snap after write), wrong-before/after,
reject, needs-owner, stale-upstream (snap after `_scope_review_for`).

## Binding rmtree over-deletion

`_shutil.rmtree(wrong_dir.parent.parent)` deleted the entire
`editorial-corrections/` dir (including the valid `fixture-wk-bind-1` proposal
with authoring/reader/proposal), causing later wrong-digest tests to fail with
`PROPOSAL_LAYOUT ... authoring-input.json missing`. Fixed to
`rmtree(wrong_dir.parent)` (only `wrong-dir`).

## Artifact-only vs control-drift (ERROR, needs debug)

`prepare` after artifact-only commit (`sources/.../artifact-only-note.txt`
committed, HEAD moved) fails in `weekly.validate_receipt:_verify_head_bytes`
with `Weekly current implementation or contract differs from committed HEAD`
(dirty control check). Artifact file is under `sources/` (not control roots
`config/schemas/scripts/.github`), so `git diff HEAD -- control` should be
clean. Requires single-fixture debug (`git diff --name-only HEAD -- control`
after artifact commit) before next full run.

## Candidate absent/proper (ERROR, needs debug)

Absent-case `prepare` (asserted `not (root/cand_rel).exists()`) still entered
`validate_candidate` and failed with `'candidate_sha256' is a required
property`. Either `candidate_full.is_file()` true due to wrong `cand_rel`
(e.g., points to an existing file) or fixture creates a candidate implicitly.
Requires single-fixture debug (list `publication/v2/` before prepare).

## Next

Fix snapshot timing + rmtree (done, active hashes updated). Debug artifact +
candidate with single-fixture runs before attempt-3 full suite.
