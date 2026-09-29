# Independent scoped review — fixed candidate 8a544f9 (R1 mechanical refresh)

- Clock: **2026-09-29T09:30:28+09:00** (`Get-Date -Format o`, reconstruct workdir).
- Role: **FRESH independent scoped implementation/evidence reviewer**, not author, not root/Astra. No model identity/benchmark claim. No delegation, no tests/probes/runtime imports/commits/network/production/main/Actions, no checkout/switch/reset/clean/apply/index/ref/config writes. Saved scripts not run.
- Source identity (fixed, immutable): candidate **`8a544f916b943b2ed03a3e46222016ef1d41faf5`**, tree `68a447913c0aff8397ed93c4aebff1dbaf0d94df`, parent `269c2a0a15a0db346cab09603f28f1465740d8a4`, branch `codex/rephase-1-mechanical-r1-correction`, fixture `/tmp/jgas-rephase-mechanical-r1-20260928T000710Z`. Fresh-root basis `a1a4242adaddc42427b68c18ae367c04d6cd63b4` (NOT e4c8269 ancestry). Last accepted shipping `e4c82692abee6acedbba07815b0d74ccefb80a7e` unaffected.
- Method: reviewed immutable copies via `notes/rephase-1-mechanical-refresh/correction/round2/changed-files/` (7 paths) plus `patch-269c-to-successor.patch`, `patch-afd-to-successor.patch`, `manifest-round2.json`, `results.md`, `commit-evidence.txt`, `run-suite.sh`, all 5 raw logs. NEVER read mutable worktree or fixture worktree as frozen. Fixture git objects not queried beyond preserved log headers (read-only pins accepted as evidence).

## Reviewed evidence

- Contract: `outputs/rephase-1-mechanical-refresh-contract-decision.md` (§1-§7).
- Prior root findings: `outputs/rephase-1-mechanical-refresh-review-findings.md` (R1-A01..A06 at afd925d).
- Basis/pins/gaps: `notes/rephase-1-mechanical-refresh/implementation/03-return-evidence-clarification.md` (fresh root, 41 unverified `sources/...` blobs, 4× `--no-verify` at afd-era, no in-log HEAD pins at afd).
- Round2 manifest/results/commit-evidence/runner + 5 logs with exact pins:
  - `weekly-refresh.log`: 25 ran OK exit 0 1246s, HEAD 8a544f9/TREE 68a4479/PARENT 269c2a0, SOURCE-SHA256 matches manifest.
  - `revalidation.log`: 29 OK 54s, same pins/hashes.
  - `gate.log`: 27 OK 1.2s, same pins.
  - `cli.log`: 5 OK 40s, same pins.
  - `increment-b.log`: 8 OK 266s, same pins. Total **94 ran, 0 failed/errors/skipped**.
  - Manifest `hook_bypass:false`, `procedure.no_verify:false`, scope 7 paths only, 4 changed vs 269c (writer, agent, 2 tests), 3 unchanged with notes. Patch stat `4 files, 839 insertions, 194 deletions` — no schema/config/authority expansion.
- Runtime source (all 1442-line writer + agent diff + gate/derivation):
  - `scripts/survey_weekly_mechanical_refresh_v2.py` (81116 B, blob `c85f0c7d…`, sha `fc4c9545…`).
  - `scripts/survey_agent_control_v2.py` (119151 B, blob `9527127…`, sha `ce6c0b88…`) lines 1600-2122 (exclusive record, State temp+replace, revalidation owner, refresh CLI).
  - `scripts/survey_reader_surface_gate_v2.py` (unchanged, blob `89b5b859…`) `_inspect_gate_record` 1474-1667 + public replay 1670-1715 + evaluate 1121-.
  - `scripts/survey_weekly_derivation_v2.py` (unchanged, blob `6d14009c…`) `_inspect_receipt_envelope` 669-696, closure/history 699-773.
- Tests/runbook: `tests/test_survey_weekly_mechanical_refresh_v2.py` (25 methods, 1208 lines), `tests/test_survey_publication_revalidation_v2.py` (29), `docs/weekly-mechanical-refresh.md` (118 lines, informational, not contract file).

## Verdict

**CHANGES_REQUIRED** at 8a544f9. Four known root residuals plus healthy-prior coverage remain OPEN (verified below, not fixed). Two new ownership/robustness blockers (N1 High, N2 Medium) plus two Low hardening notes require successor correction. No unconditional PASS. No approval inferred. Later explicit successor delta resolution must bind final verdict. Scope is bounded R1 only — not full B/step4/application/all-profiles/seven-point/Human adoption.

## Known residuals — verified OPEN at 8a (do not duplicate as new)

### K1 — Validation checkpoint deterministic review-result refs skipped (High, snapshot completeness)
- Path: `scripts/survey_weekly_mechanical_refresh_v2.py:498-505`.
- `for cp_name, cp_ref …: … if cp_ref["path"] == validation_path: continue` skips the validation checkpoint's own `record.reviews[].result.path/sha256` pinning. Earlier `checkpoint.get("artifacts")` with effective rows (449-453) covers artifacts only, not `reviews`. Non-validation checkpoints pin both artifacts (510-512) and results (513-516).
- Bundle `checks[].result` + pdf (475-483) partially overlaps but does not prove all checkpoint review-result refs. Action: pin validation record `reviews[].result` with effective-row logic (or prove bundle covers all and document), add targeted drift test.

### K2 — Temp-file cleanup/mid-write ownership needs fd identity AND known bytes (High)
- Writer `scripts/survey_weekly_mechanical_refresh_v2.py:203-263` (`_atomic_replace`): no `fstat` identity capture; `tmp.unlink(missing_ok=True)` unconditional on bytes-mismatch (229-231), pre-replace drift (242-244), recheck failure (253-255). Foreign tmp with same `run_id` (timestamp-only, 717-718, 217) would be deleted. Writer temp helper identity absent entirely.
- Agent `scripts/survey_agent_control_v2.py:1632-1714` (`_atomic_replace_state_bytes`): captures `tmp_id` (1660-1663), `_drop_own_temp` checks identity (1676-1678) but not bytes — same-inode changed data deleted on mismatch (1684-1686). Action: both sides require identity match AND bytes in {expected} before unlink; retain otherwise. Writer needs same `fstat` pattern as agent plus byte check.

### K3 — Canonical filenames checked parent/unique only (Medium)
- Writer `1058-1064`: `reviewed_path.resolve().parent != publication_dir`, `old_receipt_path/gate_path parent != publication_dir` — no leaf check. `RECEIPT_FILENAME="validated-source-manifest.json"` (32) never enforced. `GATE_FILENAME` only via lexical `gate_rel` (802,805-809). Manuscript `reader-manuscript` uniqueness (814-816) without filename; reviewed-input/manuscript leaf names unconstrained beyond parent. Action: require `old_receipt_path.name==RECEIPT_FILENAME`, `gate_path.name==GATE_FILENAME`, reviewed-input/manuscript leaves equal canonical Profile-derived filenames (or prove checkpoint/role already constrains and document).

### K4 — `_record_inventory` sentinel equality instead of fail-closed (Medium)
- Writer `613-646`: `"<unreadable-file>"`, `"symlink:…"`, `"<other>"`, `"<unknown>"` stored on OSError. Failure path `1336: if cur_state_bytes != pre_state_bytes or post_records != pre_records` treats two identical sentinels (e.g., persistently unreadable file) as clean and proceeds to guarded restoration + guard release. Action: track readability flag; any sentinel pre or post fails closed with guard retained.

### K5 — Healthy prior metadata revalidation coverage OPEN (coverage)
- Code handles effective rows for repeat (`440-447`, `826-834`) so a healthy prior revalidation with renewed manuscript/reviews/bundle vs original checkpoint does not false-fail. No dedicated test at 8a mutates manuscript/review/bundle, revalidates via API, then refreshes and asserts effective-row acceptance. Assigned to author successor; verify explicitly, do not infer from `test_first_and_repeat_success` (helper-only change).

## New findings (independent)

### N1 — Agent record rollback can delete foreign record (High, exclusive-record ownership)
- Paths: `scripts/survey_agent_control_v2.py:2038-2063` (State-is-new orphan path) and `2079-2104` (State-is-original path). Both do `is_symlink/is_file` + `read_bytes()==record_bytes` then `record_path.unlink()` with no fd/dev-ino identity.
- Why blocking: violates "Never delete an unknown record" and "removal only while current record still matches own written bytes **and** pre-write basis". TOCTOU between read and unlink allows swap-delete. Same-bytes foreign record (same reason/executor/recorded_at/head/Gate — all caller-controlled, no nonce in record payload 1903-1938) would be deleted as "own". Guard has nonce+identity (`_release_guard_if_owned` 320-333 does bytes+identity); record does not.
- Actionable: capture record identity at exclusive create (`os.stat` after `xb`, like State `tmp_id`), require `(dev,ino)` match AND `read_bytes()==record_bytes` immediately before unlink; retain + fail-closed otherwise. Add test: pre-create foreign record with identical bytes but different inode, force API failure requiring rollback, assert foreign preserved + guard retained.

### N2 — `run_id`/tmp/retention names predictable, collision over-strict + unsafe interaction (Medium)
- Paths: writer `717-719` (`run_id` from `iso_utc(recorded_at)` only), `217` (`.tmp-{run_id}`), `1152` (`retention_base/run_id`), plus agent State tmp `1648` uses content-hash (unique) — writer does not.
- Why: two cooperating operations with same `--recorded-at` (second-precision, operator retry or clock skew) share retention dir + tmp names. Current behavior is fail-closed (`retention collision`, raw `FileExistsError` from `open(xb)` unmapped in writer `_atomic_replace` vs agent's mapped collision), but legitimate retry with same instant is falsely refused (availability), and K2 unconditional unlink can delete other's tmp. `test_two_cooperating_calls_controlled_overlap` uses distinct R1/R2 times, so same-instant case untested.
- Actionable: include unique nonce (`secrets.token_hex`, like guard 1094-1097) in `run_id` or tmp/retention suffixes; map writer `FileExistsError` to `MechanicalRefreshError … collision`; document that `--recorded-at` reuse is refused. Add same-instant overlap test asserting second refuses on guard (not corrupting first's tmp/retention).

### N3 — Staged-index-only control drift missed (Low)
- Path: writer `606-610` (`_git … diff --quiet HEAD`). `git diff HEAD` compares HEAD→worktree, misses index-only staged change with clean worktree. `_control_tracked/untracked` + worktree hashing also miss it. No safety impact this run (operation reads worktree, allowed-change gate uses committed `old..head` diff), but violates "Reject dirty control code".
- Actionable: also run `git diff --cached --quiet HEAD -- controls` (or `git status --porcelain`) at capture/recheck. Add staged-only test.

### N4 — Control-membership join/split fragile + chain-depth off-by-one (Low)
- Paths: writer `536` (`"\n".join(tracked)`) / `597` (`split("\n")`) breaks on newline in filename; `522-523` (`>33`) vs agent `REVALIDATION_CHAIN_LIMIT=32` (`957`). No exploit in synthetic fixture, but fix cheaply: use `"\0".join` or list compare; align writer limit to 32 with comment.

## What was checked and found adequate (do not re-verify without head change)

- Prior authority binding: State canonical Profile-derived (744-760), strict State + `resolve_active…` (762-772), validation checkpoint identity (774-789), Gate role alias cross-check (792-809), checkpoint→effective Gate row (820-834), live Gate hash (836-839), `_inspect_gate_record` (schema/PASSED/13-field digest/manuscript+primary cardinality/scanned bytes+counts/semantic binding/unresolved 1474-1667) + receipt anchoring (849-858), `_inspect_receipt_envelope` + full linkage (route/issue/reviewed-input↔`surface_sha256/path`, review path, outputs↔manuscript 862-905, authored by NAME 907-909, receipt-next-to-surface, `verify_closure_at_commit` + ancestor 914-920). Public `validate_reader_surface_gate` always replays (1697-1714); no `skip` param.
- Allowed-helper + equality: `diff --name-status -z` classification + mode check (926-951), `_verify_head_bytes` before no-op (957-960), `MECHANICAL_REFRESH_NO_OP` excludes healthy active (961-962, tested), contract identity (963-965), independent re-derivation + render equality (967-1021), prospective receipt equality + HEAD/VALIDATED_DRAFT/State-sha (1039-1048), Gate `_compare_gate_reports` full preservation except `recorded_at/gate_sha256/derivation` + `evaluated_by` stable + receipt swap + full `semantic_authority` (649-698, 1235-1242).
- Snapshot/recheck/safe-paths: `_capture_bound_snapshot` covers receipt inputs/outputs, Gate surfaces, bundle results+pdf, manuscript/profile/arch, all checkpoint files+artifacts+results (except K1), predecessor chain, controls+membership (397-548); `_recheck_bound_snapshot` rechecks HEAD/hashes/membership/untracked/`diff HEAD` before guard/retention/each live write/commit (557-610); raw-first lexical `lstat` walks (`_check_raw_rel/abs_ancestors` 92-149, `_safe_existing_file` 152-174, `_reject_symlink_ancestors` 58-89) used for State/config/Profile/publication/reviewed/receipt/Gate/retention/guard/temp/live; real-entry alias + inside-root symlink tests pass.
- Retention/guard/rollback: nonce+pid+`fstat` guard (1094-1126), `_verify/_release_guard_if_owned` bytes+identity (276-333), retention exclusive + verified copies + metadata (1136-1184), `_atomic_replace` old-hash + temp-verify + post-readback (203-263, except K2), pre-revalidation `pre_records/pre_state` (1267-1271), commit point = API success (1276-1278), post-commit never rolls back (1296-1308, tested), pre-commit guard-first + disposition + HEAD/State/known-bytes/dependency recheck + owned-only restore (1309-1428, tested: gate-failure restore, revalidation-failure restore, record-collision preserve, torn-write retain, post-commit no-rollback, foreign-guard retain, overlap guard-occupied).
- Owner record/State: `_exclusive_create_record_bytes` xb+readback (1600-1629), `_atomic_replace_state_bytes` known-bytes + temp identity + `_drop_own_temp` (1632-1714, except K2/N1), pre-mutation basis/HEAD/State rechecks (1956-1967), post-rename disposition (1994-2025) with orphan-only deletion (except N1), alias recheck at rollback (1986-1993).
- Oracles: 25+29+27+5+8 methods use real accepted Weekly VALIDATED_DRAFT at installed R1, fresh processes/CLI, independent Git DBs, exact `returncode 2` + intended regex + before/after snapshots + record lists; `test_accepted_and_authored_mutation_refused` now restores in `finally` and asserts opposite-branch absence (fixes R1-A06); `test_first_and_repeat_success` asserts old-receipt rejection, new receipt/Gate strict validation, superseded bytes, r1 immutability, only-selected-writes + no temps. Synthetic reviews/one-page PDF remain synthetic by disclosure — not publisher-valid, no whole-program equivalence, no self-exemption for pre-install receipts.
- Procedure/identity: round2 fixes prior `--no-verify`/pin gaps — `commit-evidence.txt` shows NO `--no-verify`, hooks ran, status/diff/log inspected; all 5 logs pin HEAD/TREE/PARENT/argv/cwd/python/deps + per-file SOURCE-SHA256 matching `manifest-round2.json` worktree hashes; 41 historical `sources/...` blobs still unverified but no test reads them (copies only `config/schemas/scripts/templates/prompts/docs/data` + synthetic `2026-W37`).

## Limits

- No tests/candidate mutation by reviewer; fixed source identity above even if worktree moves.
- No multi-file atomicity, crash/power-loss automation, or global CAS against noncooperators claimed (contract §5); cooperating-refresh only.
- Synthetic publication/reviews/PDFs, narrow snapshot windows, process-local synthetic Git envs; real PDF build, all-profile/application, Windows/Actions, full diagnostics/canonical seven-point audit, Human adoption all out of scope.
- Basis divergence (a1a4242 vs e4c8269) and 41 unverified data blobs preserved from clarification; no PASS transfer.
- Successor branch is mutating; this report binds only 8a544f9 bytes reviewed.

## Required successor delta

Fix K1-K4 + N1-N2 (N3-N4 opportunistic), add healthy-prior-metadata revalidation test + same-instant/identical-record-rollback tests, rerun justified 94-method matrix once at new HEAD with same pinning, then request explicit successor delta resolution. No final acceptance until then.
