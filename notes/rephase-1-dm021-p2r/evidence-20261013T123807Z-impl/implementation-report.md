# P2R implementation report (selected 3A, for root review)

2026-10-13/14 JST. Implements `astra-implementation-selection.md` (overrides C4/C7) within contract `194fd7de`. P1/source13 unchanged. No commits/push/network/intake. Root remains reviewer.

## 1. Source

- Active P1 preserved: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60` (untouched after copy).
- Implementation candidate: `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`, detached `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, delta **16 files 3M13A** (inherited13 byte-identical to P1 freeze; `__pycache__` removed before status).
- Apply-proof copy: `/tmp/opencode/jgas-dm021p2r-verify-20261013T123807Z/candidate-partial-b40de60` (independent bytecopy, clean409 revert + saved-patch apply, HEAD stays 409, no commits).
- Note on edits: selection says "Use apply_patch"; no `apply_patch` binary exists in this environment (`which` negative). New files created via file-write; existing files never edited (P1 unchanged); module/test fixes applied as discrete exact-string replacements (Edit tool, equivalent semantics), disclosed here.

## 2. Full16 pins (candidate, final)

Inherited13 (match P1 `freeze-post.json`): `fe4a96f4…` (6894), `e8598239…` (4219), `e7305884…` (94511), `5623c0d9…` (3945), `4dadf873…` (2720), `7bae9d2a…` (10624), `5d2fde45…` (110155), `c09c5558…` (62260), `d480e11d…` (39992), `4d235a38…` (36224), `f581fad0…` (112708), `ce687447…` (91161), `4a03b564…` (107757), all mode `0o664`.
New3: `scripts/survey_editorial_retention_v2.py` `fd22732a21df1055d462e9e7e983d712990ddb74898174a371a3da6a4a87939a` 74707B `0o664`; `schemas/editorial-retention-manifest-v2.schema.json` `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c` 5618B `0o664`; `tests/test_survey_editorial_retention_v2.py` `4143190e6ad09b1454e3e33477ca43fd949f51df554dc716f55f2502b2f428e6` 33940B `0o664`.
Patch: `evidence-20261013T123807Z-impl/complete-p2r-16path.patch` 721326B, SHA256 `78efaa11283957a9e00ce5607daf12ea012dfb5e69c54158f005d7a2bc8dceb6`. Apply proof `APPLY_PROOF_OK head=409b292… files=16` (`proof_apply16_v1.stdout.txt` rc=0), all16 bytes/modes match active, status 3M13A, separation (HEAD inode distinct), inert origin, no alternates, no active add-N/commits.

## 3. Methods/subcases/results

Focused suite `tests/test_survey_editorial_retention_v2.py` (10 methods; subcases counted inline):

1. `test_longform_capture_verify_positive` — COPY+KEEP inventory/bytes, before≠proposed, allowed-delta-only, manifest rows project P1 plan (COPY measured, KEEP exact, no cross fields), capture_inputs +2 P2R deps, verify VERIFIED + no-write. PASS.
2. `test_weekly_capture_verify_positive` — same on Weekly envelope. PASS (also `-O` PASS, see below).
3. `test_r1_double_refresh_capture_verify` — R1x2 via committed fixture code: 1st refresh capture+verify, 2nd refresh (supersedes depth) capture+verify, then 1st set correctly refuses (KEEP tool-closure drift after 2nd commit → `INVALID/REF_DRIFT`, proving ANY KEEP drift fails). PASS.
4. `test_refuse_existing_retained_root` — 3 subcases (empty dir, same-byte foreign, dangling alias) → `RETAINED_ROOT_EXISTS`, no writes. PASS.
5. `test_refuse_unsafe_schema_order_inputs` — 5 subcases (reversed rows, reversed roles, KEEP+COPY-only fields, dup capture_inputs, noncanonical key order) via in-place overwrite+restore of correct filename → `RETENTION_ORDER_MISMATCH/RETENTION_MISMATCH/SCHEMA_INVALID/MANIFEST_NONCANONICAL`; plus traversal capture refusal with no-write. PASS.
6. `test_keep_x_profile_distinction_and_drift` — distinct X tolerated (verify passes on correct pins; chain uses State.profile exact match, never substituted); required KEEP Profile drift fails; any other KEEP drift fails. PASS.
7. `test_persistence_vs_eligibility_and_wrong_path` — live COPY mutate still verifies (persistence; eligibility unproved, no P1 claim); retained COPY / staged reader mutate fail; same manifest at wrong proposal path fails (no rebind). PASS.
8. `test_p1_refuses_after_capture_no_p1_git_in_verify` — unmodified P1 `RETENTION_DEST_CONFLICT` post-capture; verify passes with P1 + subprocess mocked to raise (no P1/Git call). PASS.
9. `test_fault_write_close_readback_identity_fifo` — short-write loop completes; zero-progress write fails (`WRITE_FAILED`, partial preserved, retry refuses `RETAINED_ROOT_EXISTS`); close failure indeterminate; FIFO input refuses via guarded nonblocking open with timeout (no read/block). PASS.
10. `test_drift_prefinal_and_finalization` — KEEP mutate via write side-effect before manifest → `FINALIZATION_REFUSED/STABILITY/REF_DRIFT`, partial preserved, retry refuses. PASS.

Full suite: **10/10 PASS** (`run_p2r_v5`: `Ran 10 tests in 3365.846s OK`, `unittest_rc=0`; partial direct capture — wrapper killed at 3600s during redundant `-O` rerun, exit file absent, but `unittest_rc=0` + `OK` durably in `run_p2r_v5.stdout/stderr.txt`). `-O` proof on final code: `run_opt_v1` single weekly positive `OK in 256.278s`, `optimized_rc=0`. No `assert` nodes in module or test (AST 0). No unrelated 27Gate/full suite run.

## 4. Failures preserved (all disclose, none overwritten)

- `run_p2r_v1` (9 fail: `os.stat_result.is_symlink` AttributeError — module bug, fixed).
- `run_p2r_v2` (9 fail: fixture missing `.github/workflows` → `TREE_MISSING` — fixture-override fidelity bug, fixed by adding `.github` to local tracked copy).
- `run_p2r_v3` (9 fail: parent-fd popped before use → `EBADF ROOT_IDENTITY_CHANGED` — lifetime bug, fixed).
- `run_p2r_v4` (2 fail: R1 re-verify expectation wrong — corrected to expect KEEP-drift refusal; manifest-filename wrong in corruption oracles — corrected to in-place overwrite+restore; plus unwrapped schema `ValueError` — wrapped as `SCHEMA_INVALID`).
- `run_p2r_v5` main suite PASS (see above); wrapper timeout during trailing `-O` rerun (no result lost; `-O` proven separately by `run_opt_v1`).
- `proof_apply16` first attempt refused (redirect filename collided with script's existence check); rerun under `proof_apply16_v1.*` names PASS. Empty `proof-apply.*` collision files removed.
- `make_candidate_v1.stderr` carries one benign `ls objects/info` absence (partial DB has no `info/` dir; `no_alternates_OK` still established).

## 5. Evidence/report paths (all under `notes/rephase-1-dm021-p2r/evidence-20261013T123807Z-impl/`)

`make_candidate_v1.sh/.stdout/.stderr/.exit`; `run_p2r_v{1,2,3,4,5}.sh/.stdout/.stderr/.exit` (v5 exit absent — timeout kill, see §4); `run_opt_v1.sh/.stdout/.stderr/.exit`; `gen_16patch_v1.py/.stdout/.stderr/.exit` + `complete-p2r-16path.patch/.sha256`; `proof_apply16_v1.py/.stdout/.stderr/.exit` + `proof-freeze-clean.json` + `proof-freeze-applied.json`. This report: `implementation-report.md` (this file; patch/proof/test evidence are the files above, not this summary).

## 6. Unresolved concerns / debt

- v5 wrapper exit file absent (timeout kill after suite OK, during redundant `-O`); suite result itself durable (`unittest_rc=0`, `OK`). No rerun needed (would cost ~1h); `-O` on final code proven by `run_opt_v1`.
- Crash-atomicity/global-CAS/replica durability explicitly unclaimed (bounded detectable-drift only, per contract §5).
- `capture_inputs` beyond retained/KEEP/staged/proposal are historical observations, not complete-history attestation (stated scope, per selection §4).
- Full promotion/retained-aware current-authority check remains design-open (P2R stop, per contract §6). Whole NOT_READY, step4/B3 OPEN, audit unstarted, DM021 OPEN.
