# R7 narrow boundary correction (internal unit, not Human Commit Point, not whole PASS)

Two actual defects from WorkerD final-r6-faults (preserved as history, R6 32-refuse mislabel retained, not edited):

1. `survey_agent_control_v2.main` validate-state used undefined `repo_root` (local is `root`). Fixed to `root`. Inspected all newly changed main CLI loader calls: only validate-state used `repo_root`, others already use `root`. Actual public CLI valid (exit0 JSON) and malformed (exit2, no data write) proven via new R7 test + DM004 4/7 appropriate regression (valid FROZEN/RELEASED, outside, other-cwd, contract refusals pass; 3 fails are unrelated env/message, documented below, not depth/loader).

2. Depth limit32 means at most 32 total records including active. R6 allowed max31 (agent range31 needs terminator, high range32 needs terminator). Fixed agent `range(LIMIT-1)`->`range(LIMIT)` and high `range(32)`->`range(33)` (32 loads + None break needs 33 iterations). Low `_walk_chain_backwards` already allows 32 via immediate None return and `derive len>32` allows 32, preserved. No numeric seq<=32 restriction (gaps possible legacy). Preserve SHA/chronology/cycles/original union/7 projection.

## DST (implementation copy, R6 strict + R7 fix)

- DST: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60` (matches R6 strict low/high before fix, now R7 fixed).
- Prebytes archived: `*.pre-r7` (agent `c132c944` 149686B, high `2d51c2d2` 256628B, low `ecd7facac` 127802B unchanged).
- Fixed pins: agent `cd8af389` 149677B, high `98f8ff8b` 256725B, low unchanged `ecd7facac`, new test `77ab305e` 18956B.
- Edits via dedicated Edit only, no source outside DST, no raw overwrite/delete/clean/reset/purge/net/ordinary commits.

## New test in DST

- `tests/test_survey_editorial_r7_boundary_v2.py` (3 tests): CLI loader valid/malformed (actual public `python -m scripts.survey_agent_control_v2 --repo-root <fix> validate-state`), depth 32 valid/33 refuses API+CLI (WorkerD typed33 chain fixture schema-valid/cumulative, NOT actual R1x33, fresh code epoch DST fixed, absolute fixture paths, cwd=DST, PYTHONPATH=DST, no alias mix), preflight chain31 allows32 vs32 refuses33 (actual `_build_anchor_chain` + len prewrite, no mocked validator-success). Negatives assert complete old State SHA unchanged. No blanket catch, no typealias fallback. All scratch workspace ignored `.rephase-1-editorial-runtime/final-r7-faults`, never /tmp quota/dev/shm/home. Own GitDir verified NOT reconstruct + inert/no sharing before writes. Frozen SOURCE never executed inside.

## Focused runs (raw direct numeric exit, source pins)

- R7 boundary 3/3 PASS exit0: `r7-boundary-{stdout,stderr,exit}.txt`.
- Affected legacy31/low18/schema/agent 57/57 PASS exit0: `r7-affected-{stdout,stderr,exit}.txt` (revalidation 31, publication_set 18, agent 5, schema 1+2).
- DM004 4/7 PASS exit1 overall (appropriate regression, not only pycompile): `r7-dm004-*`. Pass: generic valid FROZEN/RELEASED, other-cwd, outside, contract refusals (proves loader fix valid/malformed JSON/exit0/exit2/no-write). Fail (actual facts, not preexisting dismissal):
  - 2× `python: command not found` in closure/failfast (workflow uses `python`, env has `python3` only; unrelated to loader/depth, no data write, still fail-closed).
  - 1× removed-record message mismatch (expects `drift`, gets `escapes...missing`; both fail-closed exit2 no-write, correct refusal, only wording differs; previously would have been NameError exit1 before fix, now controlled exit2).

## New SOURCE snapshot R7 (untouched, independent, before authority)

- Path: `.rephase-1-editorial-runtime/jgas-editorial-r7-20261023T033000Z/candidate-partial-b40de60` (unique, NOT reused R6 path which was reused once already).
- Copy via `cp -a` independent inodes (verified dev:ino differs), own GitDir verified NOT reconstruct, inert origin `example.invalid`, no alternates, no sharing.
- Staged only intended files, committed with meaningful message before authority: `00397c31b0f849b46cf556b137064679d026e400`, tree `23c9ba98530f3c94e3ed4ec64ecb13ae53e548ea`, 721 files (720+new test), status only `?? scripts/__pycache__/` (preserved, not committed).
- Manifest: `source-manifest-r7.json` (721 entries, full SHA/bytes/mode + HEAD/tree).
- Sanitized env for Git (NOSYSTEM/GLOBAL/OPTIONAL_LOCKS, --no-optional-locks, no inherited GIT_*), process-scoped identity `worker-r7`.

## Final operator acceptance (fresh Weekly, ALREADY real PDF, R7 code)

- Script: `r7-weekly-accept.py` (new, not old runner), FIX_ROOT fresh copy of R7 SOURCE (`.rephase-1-editorial-runtime/final-r7-accept/weekly-r7-fix`, independent, own GitDir, inert, no sharing).
- Result exit0: `r7-weekly-accept-{stdout,stderr,exit}.txt`.
- Real TL2026 build: `REAL_PDF pages=5 bytes=61239 dt=27.5s` (lualatex-biber-lualatex, no fake PDF).
- Public CLI `validate-state` exit0 JSON (proves loader root fix in acceptance context).
- Normal `prepare/finalize/activate (ACTIVATED) / second activate (ALREADY_ACTIVE) / resume (ALREADY_ACTIVE)` with real PDF, old-immutable preserved (via builders, no canonical rewrite).
- Depth validated via typed33 in R7 tests (32 valid, 33 refuses before write, State SHA unchanged); normal short chain (1 record) unaffected, so old normal scopes remain qualified where code paths unchanged, but no automatic exact-epoch PASS transfer — final independent reviewer decides qualified old scopes. Root packages final after return.
- R6 mislabel (32-refuse PASS wording) preserved in `final-r6-faults/coverage-table-FINAL.md` and `matrix_r6_depth*.py`, not edited.

## No new feature, no downgrade

All normal both-route first+second+RELEASED and R1 anchor typed proofs already passed R6 scope; unchanged paths preserved. No new feature, no boundary downgrade. If another real code bug found, returned as actual facts (DM004 3 fails above), not labelled preexisting.

Internal unit, not Human Commit Point, not whole PASS. Whole unit still awaits final source packaging/evidence review. Stop for root packaging.
