# Supplement-carry final implementation review — frozen source + focused/scale/C evidence

Role: NEW independent implementation reviewer (final, not author/map reviewer, not Astra/root, not implementer, not Human).
Date: 2026-11-07.
Method: read-only file/text reads + Python hashlib/pathlib hash/parse only. No `git` binary, no reconstruct readback, no repo-script imports, no test/runtime execution, no network/Production/subagents, no source/State writes except this NEW pair. Preserves `initial-…`, `corrected-…`, `corrected-v2-…` reviews/machines.

Read scope (FULL unless noted):
- `astra-implementation-resolution.md` FULL incl §7 (C oracle update + 409/160 scale witnesses + rerun scope + CURRENT/packaging gating)
- `affected-verification-20261107T031826Z/SUMMARY.md` FULL + `pre-sha256-pins.txt`, `pre-loaded-module-paths.txt`, `pre-status-porcelain.txt`, `batch-01…06-raw.txt` headers/tails + failure section (via Python parse, no rerun)
- `implementation-20261106T131722Z/corrected-return-v2.md` FULL, `corrected-implementation-v2.diff` §§577-609 (views seam) + §§158-164 (canonical empty ctx), `corrected-batch-v2-raw.txt` FULL (14 OK), `baseline-control-original-final139-raw.txt` FULL (bound original refusal)
- `changed-c-n7-raw.txt` FULL (single N7 OK after oracle update), `scale-w34-raw.txt` + `scale-sp-raw.txt` FULL, actual workcopy `tests/test_dm022_supplement_carry_scale_v2.py` FULL (402 lines, `7118092f80b1…`), `tests/test_dm022_c_direct_operation_v2.py::test_c_binding_integrity_drift` N7 block (615-687), actual workcopy `tests/test_dm022_supplement_carry_v2.py` v2 prior-records + `_assert_full_unaffected` + view-only negative (as bound in v2 review)
- Identity only: workcopy `.git/HEAD`, `refs/heads/main`, `config`, file counts vs final139 manifest via Python (no git)

## 1. Verdict

**SCOPED_IMPLEMENTATION_READY (bounded selected repair only, conditional until delivery bind).**

Frozen runtime LOW `d50282…` / HIGH `f312f0…` is the v2-reviewed code with narrow unaffected-views seam + canonical empty ctx + C1/C2/HIGH-late closures. Focused 14, scale 409/160, and corrected single-C N7 demonstrate the selected triangle/carry/retention semantics on real HIGH paths with no stubs/manual packages. This is not full-suite PASS, not R4 audit, not semantic/Human approval.

Fresh CURRENT proof + exact complete packaging are running as independent tasks — not claimed passed here. This review is conditional until those delivery bindings pass on the exact frozen hashes. Do not sum 7+2+19+14+6+4+14+1+1 runs or claim real W34/SP 409/160 accepted-correction semantics; real corrections remain unperformed with separate semantic review.

## 2. Frozen source — runtime unchanged, tests added

- Workcopy HEAD `5eef790bd8d492c557cc4db9c29425e3e410d47d` (isolated root, NOT 409 ancestry), inert origin, no alternates. Python SHA256: LOW `d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd`, HIGH `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90`, focused `5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00`, scale `7118092f80b1a7a2…`, C-existing `1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31`. Match `pre-sha256-pins.txt` (LOW/HIGH/focused) + v2 raw header + `changed-c-n7-raw` + scale file parse. Proof `0974c709…`/`388c899…` untouched.
- File set now 773 = 771 manifest + 2 new tests (focused + scale). Affected-verification packet records 772 (771 + focused) because scale file was added after those 6 batches; runtime LOW/HIGH identical pre/post in every batch raw (`POST_SHA` = `d50282/f312/5d5d3a`), so scale addition does not invalidate frozen-runtime evidence. No ordinary candidate/reconstruct commit.

## 3. Scale witnesses — structural, not semantic; counts truthful with one shape caveat

Verified in actual `test_dm022_supplement_carry_scale_v2.py`:
- W34-scale WEEKLY: 409 tasks, 401 supp-bound, 428 entries (374×1 + 27×2 multi-source), 428 unique Raw files. Affected 4 + unaffected 397 supp-bound + 8 Discovery-only (401−4=397, 409−401=8). File header explicitly states selected shape has no duplicates; real 428/425 duplicate shape documented as not replicated — use 428 unique Raw (NOT real 425), not a semantic replica.
- SP-scale THEMATIC: 160 tasks, 28 supp-bound, 30 entries (26×1 + 2×2), 30 unique Raw. Affected 4 + unaffected 24 supp-bound + 132 Discovery-only (28−4=24, 160−28=132).
- Flow is initially-all-affected novel bootstrap (rev1 `affected=dids`, no prior) vs unchanged/replaced with nonempty unaffected separate (rev2 `affected4` + `prior1`, rev3 replaced `supp_b` + `prior2`, `sid_a == sid_b`, distinct `raw/auth-<did>-r2.html` built BEFORE State on same screening basis HEAD). Each stage real `high.prepare_revision → adopt_revision` (+ `readback_revision` on rev3), no manual `supp-candidate` assembly, no patched `_resolve/_merge/_build_card/validate/build_revision_package`, no stub proof, synthetic `example.invalid`/`SYNTHETIC_FIXTURE_*` only, ALL unaffected fields deepcopied via `prior_records_by_did` (same pattern as focused v2).
- Unaffected asserts mirror focused v2: task identity + Discovery→task identical, cards + views byte-identical, ledger rows identical, `rows_checked == len(tasks)+len(rows)` (W34 409+409=818, SP 160+160=320), mechanical allowlist exactly 9 fields. Raws: `scale-w34-raw.txt` 313.961s OK, `scale-sp-raw.txt` 96.578s OK (ARGV/ENV/PID/START/EXIT/END bound, no source-hash header — bounded by frozen-runtime pins + v2 raw, see §6 limits). These are structural full-size witnesses, not WEEKLY DERIVED/Special route proofs (those remain in focused `test_dm022_supplement_carry_v2`) and not publisher semantic acceptance.

## 4. Corrected C testcase — earlier exact coverage + honest write window, no full-C green claim

Verified in actual `test_c_binding_integrity_drift` N7 block (615-687):
- New expectation is the earlier exact error `request.records must cover exact non-DROP Discovery IDs (no new/omitted/DROP/extra unused …)` from repaired `build_revision_package_from_paths` exact-coverage preflight (r2 §4), not the older later `request.records[1] … not a bound effective …`. Root §7 authorizes this oracle update; preserved failed `batch-05` raw + no rerun/cleanup is the superseded evidence.
- Write-window assertions are exact: owned State COPY may exist (`retention/state-before.json` + slot COPYs), but `candidate/package.json|tasks|results` must NOT exist, canonical State bytes unchanged, no `checkpoint/proof` new files (excluding the bad request file itself), no guard (`guard_path_for` absent). Covers StateCOPY-exists/candidate-absent, no checkpoint/guard/proof writes — no universal zero-write overclaim.
- `changed-c-n7-raw.txt` (single N7, 4.553s OK, source `d50282/f312` bound) proves the updated N7 in isolation. Full C batch green is NOT claimed: `batch-05` remains 5 pass + N7 fail (exit 1, STOPPED, no fix/rerun), and only the single N7 was rerun after correction. Follow-up full C6 rerun is still required before any C-green statement.

## 5. Other regressions — separate batches, no aggregate source claims

`affected-verification-…/SUMMARY.md` + raws: batch-01 LOW 7 OK, 02 interactive 2 OK, 03 scaling whole19 OK, 04 HIGH A2 14 OK, 05 C direct 5+fail (exit 1, preserved), 06 Profile selected 4 OK (14/14b + 23/24 covering ledger/DERIVED/lossy per §9). Each batch is a unique per-module process with argv/cwd/env/PID/START/END + pre/post `d50282/f312/5d5d3a` binding; totals (52 run, 51 pass, 1 fail) are listed without sum-as-source claim. Unexecuted lists (§9 targeted exclusions, heavy PDF/TinyTeX/CURRENT) are explicit. `mock.patch` only for fault-injection negatives + private-slice probes, never to hide parent failure. No TinyTeX/OLD_ROOT/Production/network/CURRENT in target files.

## 6. Limits + needed final bindings (pending, not passed)

- Scale raws lack source-hash/loaded-module headers (only ARGV/ENV/PID); binding relies on frozen `d50282/f312` + focused/changed raws + file-parse hashes. No per-test source header; no proof/report/checkpoint bytes in raws (only asserts). Fixture Git commits are test DATA.
- Needed before Human Commit Point: (a) full C6 rerun after N7 oracle update, (b) targeted no-supp compat + any remaining §9 regressions selected by root, (c) fresh `verify_renewal_source_proof` CURRENT via API with new pins/`expected_head/tree` on exact `d50282/f312`, (d) exact complete DIRECT409 delivery with apply-check on actual409 (not isolated 5eef ancestry). Real e84 material unchanged; real W34/SP corrections retain separate independent semantic review. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality/adoption/savings OPEN. Ordinary Commit/Push Human-owned.
