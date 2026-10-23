# FINAL R5b matrix — coverage table (Worker D, no source edits)

Final SOURCE: `.rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60`
HEAD `10e8662e21fd0aa3c2d71c0bb8d6bf6ae3271ae9`, tree `e434978d0d2034f1a6ec51813be92434234bd3b7`, 720 files, clean, inert origin, no alternates.
Bases (originals readonly, never tested inside SOURCE):
- INERT weekly `.rephase-1-editorial-runtime/final-r5b/weekly-inert` State r1 `88394f...`, r2 ABSENT, set2 sealed `3713cd...` (file SHA), set_sha `e4b384...`
- PRELC weekly `.../weekly-prelc` State r2 `1f2211...`, VALIDATED_DRAFT Preview pending
- INERT/PRELC longform same shape SP001 (`lf-r5b-2`, r1 `25062c...`)
Manifests `notes/.../final-r5b-positives/inert-manifest-*.json`, `final-epoch-*.json` same HEAD.

Scratch ONLY `.rephase-1-editorial-runtime/final-r5b-faults/` (ROOT approved, workspace-ignored, 993M preserved).
Every fixture own `.git`/toplevel verified NOT reconstruct before Git write, `cp -a` no hardlinks/alternates/inert.
ENV no-bytecode BEFORE Python (`PYTHONDONTWRITEBYTECODE=1 -B`), `PYTHONPYCACHEPREFIX`+`TMPDIR` under approved scratch.
Per-case subprocess bound (`PYTHONPATH=<fixture>`, `cwd=<fixture>`), never mixed globals.
Scripts BEFORE run via dedicated editor: `matrix_common.py`, `matrix_a.py`, `matrix_a2.py`, `matrix_a3.py`, `matrix_a4.py`, `matrix_b.py`, `matrix_c.py`, `matrix_c2.py`, `matrix_c3.py`, `matrix_c4.py`, `matrix_c5.py` (+ this table).
No clean/reset/purge/rawdelete/network/ordinary commits, no `/home/tmp` or `/dev/shm`. Workspace root ample (no /tmp EDQUOT revert).
Synthetic datatype fixtures only; production NO_GO unchanged.

## Group A full-inputs (INERT base keeps State set1 healthy while target set2 tampered; PRELC for active)

| Case | Fixture (new copy) | Public API/CLI | Expected oracle / fired seam | Terminal (observed/preserved) | Exit | Status |
|---|---|---|---|---|すすめ|---|
| A_unknown_branch | `a-unknown-branch` (INERT_W) | `validate_activation_record` + CLI `verify-activation-history` | unknown `kind` refuses branch/schema | preserved, no delete | API 0 (refused), CLI 2 | PASS |
| A_seal_missing/extra | `a-seal-missing`, `a-seal-extra` | `validate_prepared_set` | `SEAL_SCHEMA` missing/extra | preserved | 0 | PASS |
| A_seal_duplicate_JSON | `a-seal-duplicate-json` | `validate_prepared_set` | `duplicate JSON key refused` strict before digest | preserved | 0 | PASS |
| A_malformed_JSON | `a-malformed-json` (truncated semantic-review) | `validate_prepared_set` | strict parse refuses before digest | preserved | 0 | PASS |
| A_state_clone_retained | `a-state-canonical` (INERT) | `validate_prepared_set` (canonical ok) + `validate_editorial_receipt` with retained COPY (refuses `STATE_NOT_CANONICAL`) + `verify_activation_history` (historical valid) + CLI `validate-prepared-set --state retained` exit2 | canonical accepted, retained/cloned refused, history separate | preserved | API 0, CLI 2 | PASS |
| A_deep_research | `a-deep-research` (INERT, accepted research tampered + fresh receipt/seal digests) | `validate_prepared_set` | got `STATE_INVALID ... accepted_refs SHA drift` (retention pin) – digest preemption, NOT deep replay | preserved | 0 | PREEMPTED (INCOMPLETE true deep; needs retention-excluded target or retention update) |
| A_deep_reader | `a-deep-reader` (INERT, reader forged inconsistent + fresh digests) | `validate_prepared_set` | reader/author rederive mismatch (deep, not digest) | preserved | 0 | PASS |
| A_equal_SHA_wrong_path | `a-equal-sha-wrong-path` (INERT, same bytes new path + fresh set_sha) | `validate_prepared_set` | UNEXPECTED_PASS – seal allows same-SHA different filename inside `<P>/publication` (only `inside` check, not exact) | State unchanged, file preserved | 10 (unexpected) | BLOCKER – missing exact path binding for reviews; needs root disposition |
| A_reviews | `a-review-missing/nonpass/stale` | `validate_prepared_set` + CLI `validate-prepared-set` exit2 | missing/nonPASS/stale refuses | preserved, before writes | API 0, CLI 2 | PASS |
| A_tamper | `a-tamper-source/pdf/log/digest` | `validate_prepared_set` | `SEAL_DRIFT` digest | preserved | 0 | PASS |
| A_wrong_binding | `a-wrong-binding` | `validate_prepared_set` (wrong Candidate) + public `validate_reader_surface_gate` with wrong manuscript | cross-binding refuses | preserved | 0 | PASS |
| A_adopted | `a-adopted-check` (INERT set2 inert valid, active set1) + `a-old-canonical-check` (PRELC) | `validate_prepared_set` + `resolve_publication_selection` + `validate_candidate` standalone | inert valid but NOT adopted (active set1), old canonical standalone fine but NOT selected | preserved | 0 | PASS |
| A_build_failure | `a-build-component` (INERT) | explicit ` _run_disposable_build` with invalid toolchain (scope-bound) | toolchain/executable/build refuses, no fake PDF, positive Tool build exists (no repeat success) | no PDF forged, incomplete preserved | 0 | PASS (component); PUBLIC NEW-proposal full P1/P2R/scope/P2V/P3S+prepare INCOMPLETE (heavy, needs NEW ID cycle) |
| A_2route | `a-2route-weekly/longform` (PRELC_W/L) + `a-before-kinds` (INERT) | `validate_prepared_set` + `validate_agent_state` + `resolve_publication_selection` | both routes VALIDATED_DRAFT VERSIONED_ACTIVE, retention has COPY+KEEP, LF reader canonical exists | preserved | 0 | PASS (shared predicate once + 2route controls, no double R1) |

## Group B chain/current (PRELC for active chain, INERT for drift/approved/foreign)

| Case | Fixture | Public API/CLI | Fired seam | Terminal | Exit | Status |
|---|---|---|---|---|すすめ|---|
| B_anchor_ref | `b-anchor-ref` (PRELC_W) | `validate_activation_record` on bad-anchor/bad-ref + CLI `verify-activation-history` | anchor/ref SHA drift refuses | preserved | API 0, CLI 2 | PASS |
| B_cycle_seq_depth | `b-cycle-seq` | `_next_record_seq` predecessor+1 (R5b fix, no max+1 fork, next 3 on prelc) | SEQ OK | preserved | 0 | PASS (seq); depth32 (33-record) + full cycle chain INCOMPLETE (heavy, cycle files preserved as evidence) |
| B_drift | `b-drift` (INERT, contract SHA drifted) | `activate_publication` | `STATE_DRIFT`/`BEFORE_STATE`/contract before writes, no r2 created | preserved old, no writes | 0 | PASS |
| B_approved_foreign | `b-approved` (INERT, Preview approved) + `b-foreign` (weekly State + longform set) | `activate_publication` + CLI `activate-publication` | `PREDECISION` (approved), foreign issue mismatch | preserved | API 0, CLI 2 | PASS |
| B_writers | `b-writers` (PRELC_W) | `revalidate_publication_surface` editorial reason + core on revised | editorial refuses (use versioned), revised refuses (use versioned) | preserved, no destructive action | 0 | PASS (R1 separate full healthy; interactive/semantic wrappers INCOMPLETE if needed) |

## Group C activation write/fault/resume (INERT State r1, no r2, set2 sealed; orphan via PRELC r2 copy)

Record (FD-tracked `os.open/write/fsync/close`, delegate until fault; no validation/Git stubs):
- `c-record-zero/short/fsync/close/combined` (separate `c-record-*` INERT) – `RECORD_*`/`WRITE`/`FSYNC`/`CLOSE`/`WRITE_CLOSE_COMBINED` with primary+secondary, observed old, partial preserved, State old – PASS
- `c-record-pre/partial/post` (`c-record-pre/partial/post-v2`) – open collision / partial after half / readback mismatch, observed old – PASS
- CLI `validate-prepared-set` tampered exit2 – PASS

State (temp `...tmp-reval-*` FD-tracked):
- `c-state-temp_create/write/fsync/close/pre_replace/replace` (separate `c-state-*`) – `STATE_REPLACE`/`TEMP_*`/`EXPLICIT_RECOVERY`, observed old, record inert preserved – PASS (6/6)
- `c-state-postread-v2` (`c-state-postread-v2`, `os.read` fails after replace) – `POSTREAD_FAIL` observed unknown, State new preserved, record preserved – PASS
- `c-observed-new` (`c-observed-new`, corrupt seal after replace) – `POSTREPLACE_FAIL` observed new, State new r2, record preserved – PASS

Foreign/orphan/active/unknown:
- `c-foreign-v2` – create replacement WHILE original exists (assert different dev/ino), `os.replace`, ordinary `activate` refuses `RECORD_OWNERSHIP` before State write, observed old, State old r1, no deletion – PASS
- `c-orphan-v2` – INERT + PRELC r2 copy (State old r1 + record r2, same set `3713cd...`, before_state `5f9764...` matches): ordinary `activate` refuses `RECORD_COLLISION`/`INTENT_COLLISION` (no r3 fork, R5b predecessor+1 fix), explicit `resume` → `RESUMED` exact r2 (pointer SHA matches), strict readback VERSIONED_ACTIVE – PASS; CLI ordinary exit2 – PASS
- `c-already-v2` (PRELC_W State r2) – ordinary `activate` same set → `ALREADY_ACTIVE` readonly (hashes unchanged) – PASS
- `c-unknown` (INERT + r2, State→null, neither old r1 nor new r2) – `resume` refuses `INDETERMINATE` (readable null, not missing precondition), preserved – PASS; CLI `resume` unknown exit2 – PASS
- `c-incomplete-orphan` (truncated r2) – `resume` refuses gracefully (`RECORD_INVALID`), preserved, no auto-overwrite – PASS

I/O notes: close faults target write FD only (FD map from `os.open`), never fail read-close first; wrappers delegate actual func until exact fault; immediate fault inventory = only owned record/temp allowed delta (new inert record on State faults, partial record on record faults), State old/new/unknown as above, primary+secondary preserved, no referenced foreign deletion (foreign replacement file retained via `os.replace`, never unlinked; unknown/incomplete records retained).

## CLI exit2 coverage (actual-root `python -m scripts.survey_editorial_publication_v2`)
- `verify-activation-history` unknown branch 2 – PASS
- `validate-prepared-set --state retained` 2 – PASS
- `validate-prepared-set` review missing 2 – PASS
- `activate-publication` approved 2, orphan ordinary 2 – PASS
- `resume-activation` unknown (null State) 2 (`INDETERMINATE`) – PASS
- `validate-prepared-set` tampered 2 – PASS

## INCOMPLETE (not claimed, concrete next)
- A_deep_research true replay (got retention drift preemption; needs retention-excluded target or declared retention update + fresh digests to reach replay)
- A_equal_SHA_wrong_path BLOCKER (allows same-SHA different filename for reviews; seal only `inside`, not exact – needs exact binding or root disposition that inside+SHA is sufficient)
- A_build PUBLIC NEW-proposal full cycle (component executor done; needs NEW ID P1/P2R/scope/P2V/P3S+prepare, heavy, no success decoration)
- B_depth32 (33-record chain) + B_cycle full chain via public API (seq predecessor+1 done, cycle files preserved)
- B_writers interactive/semantic wrappers if needed (R1 separate done)
- LF deep forgery separate (shared predicate once + 2route positives done, no double count)
- R1 both routes double count explicitly NOT claimed.

No Human Commit Point until root closes whole unit. Production NO_GO unchanged. Synthetic datatypes only.
