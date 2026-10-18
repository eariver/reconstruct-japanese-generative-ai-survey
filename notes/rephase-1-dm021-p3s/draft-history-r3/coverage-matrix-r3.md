# P3S R3 coverage matrix (authored, NOT yet executed)

26 behavioral methods. Every P3S writer/verifier/fault call runs via the common
durable launcher (`_launch_durable_child` with `xb` stdout/stderr BEFORE Popen,
direct child fds, exclusive pre-meta with pid/running, process-group
TERM→KILL + bounded reap, script bytes+sha + actual argv/cwd/env saved). Real
P1/P2R/P2V seams run in-process exactly as P1/P2R/P2V tests do. Fault scripts
wrap ACTUAL `os.*`/`Path.read_bytes`/staged-helper calls (never mock-replacement)
and return fired counts + structured code/phase/disposition + owned details.
Snapshots are raw lstat maps; every refusal asserts immediate equality or exact
owned delta WITH the fault present. Timeouts are selected conservative
operational bounds only (1800/600/1800/60), not measured sufficiency.

| # | Test method | Real seams | Expected (phase/disposition asserted) |
|---|---|---|---|
| O1 | `test_o1_longform_materialize_and_replay` | LF chain + P1/P2R/scope + subprocess `materialize` (1800s) + `verify` (600s) | `MATERIALIZED`+`VERIFIED`; 37 deps; prose delta; owned-delta-only |
| O2 | `test_o2_weekly_materialize_and_replay` | Weekly chain, same | `WEEKLY_GENERATED_V2`; envelope delta; `VERIFIED` |
| O3 | `test_o3_coexistence_p1_refuse_p2r_p2v` | P1 `validate_proposal`; P2R `verify`; P2V `observe` | P1 raises; P2R `VERIFIED`; P2V `SCOPE_BOUND` |
| O4 | `test_o4_live_state_mutation_replay_ok_materializer_refuses` | live-State probe; `verify`; `materialize` | replay `VERIFIED`; writer `OBSERVER_REFUSED` |
| O5 | `test_o5_artifact_only_head_independence` | artifact-only commit; `verify` | `VERIFIED` across HEAD |
| O6a | `test_o6a_tool_drift_reaches_check` | healthy set → tamper import-only dep → `verify` (600s) | `TOOL_DRIFT` `PIN/INVALID`; no-write; restore re-verifies |
| O6b | `test_o6b_keep_drift_preempts_honestly` | KEEP-byte tamper; `materialize` | earlier KEEP `OBSERVE/REFUSED_PRE_WRITE`, not `TOOL_DRIFT` |
| O7 | `test_o7_scope_refusals` | missing/ordinary/malformed/stale; `materialize` | `SCOPE_*` (+ `SCOPE_STALE_UPSTREAM` `OBSERVE/REFUSED_PRE_WRITE`); phase/disposition present |
| O8 | `test_o8_path_ref_schema_inventory_tamper` | extra-aux/duplicate/wrong-path/unknown-field/swapped-deps + `verify` (600s) | `STAGED_SET_MISMATCH`/`SCHEMA_INVALID`/`OUTPUT_PATH_MISMATCH`/`CODE_DEPS_MISMATCH`; phase/disposition present |
| O9 | `test_o9_alias_fifo_no_read` | alias reader; FIFO reader (60s); ancestor alias; `materialize` | `PATH_ALIAS`/`PATH_NOT_REGULAR…` without hang; phase/disposition present |
| O10 | `test_o10_same_inode_vs_new_inode` | in-place `%` edit; same-byte replace; `verify` | edit `REPLAY_MISMATCH`; swap `VERIFIED` |
| O11 | `test_o11_root_preexisting_and_postreadback_drift` | pre-created dir; post-readback swap; `materialize`/`verify` | `STAGED_ROOT_EXISTS`; `REPLAY_MISMATCH` |
| O11b | `test_o11b_midcall_reader_drift` | `drift-reader` exact-rel | `STABILITY_VIOLATION` `PRE_WRITE/REFUSED_PRE_WRITE` fired==1 |
| O11c | `test_o11c_late_control_retained` | `late-control-add`/`late-retained-add` | `ORIGINAL_*` `PRE_CLAIM/REFUSED_PRE_WRITE` fired==1 |
| O11d | `test_o11d_drift_before_claim_manifest` | `drift-before-claim`/`drift-before-manifest` | `STABILITY` `PRE_CLAIM/REFUSED_PRE_WRITE` / `PIN_DRIFT` `MANIFEST/INDETERMINATE` fired==1 |
| O11e | `test_o11e_post_readback_replay` | `post-readback-edit` / `post-replay-samebyte-replace` | edit `REPLAY*` `REPLAY/INDETERMINATE`; replace `FILE_REPLACED` `FINAL/INDETERMINATE` fired==1 |
| O11f | `test_o11f_root_ancestor_replace` | `root-replace`/`ancestor-replace` | `STAGED_ROOT*` `CLAIM/OWNED_PARTIAL` fired==1 |
| O12a | `test_o12a_preexisting_tamper_verify` | truncated/empty-subdir/zeroed | `PIN_UNREADABLE`/`STAGED_SET_MISMATCH`/`REPLAY_MISMATCH` |
| O12b | `test_o12b_during_write_faults_incomplete` | `zero-write`/`write-fail`/`fstat-fail`/`mkdir-fail` leaf-targeted | exact per-fault delta; `bytes_written==0`; `CLAIM/OWNED_PARTIAL` fired==1 |
| O12c | `test_o12c_fsync_close_indeterminate` | `fsync-fail`/`close-fail` | `FSYNC/​CLOSE_FAILED` `CLAIM/INDETERMINATE`; exact root+main.tex fired==1 |
| O12d | `test_o12d_manifest_failure_indeterminate` | `manifest-write-fail`/`manifest-close-fail` | `MANIFEST/INDETERMINATE`; exact partials; close bytes still `VERIFIED` fired==1 |
| O12e | `test_o12e_fstat_identity_mismatch` | `fstat-fake` | `STAGED_FILE_REPLACED` `CLAIM/OWNED_PARTIAL` exact root+empty-file fired==1 |
| O12f | `test_o12f_short_partial_combined_close` | `short-once`/`partial-then-fail`/`write-then-close-fail` | short `MATERIALIZED` fired==1; partial `WRITE_FAILED` `CLAIM/OWNED_PARTIAL` `bytes_written==1` fired==2; combined primary preserved + secondary fired==2 |
| O13 | `test_o13_immediate_no_write_before_repair` | verifier `TOOL_DRIFT` `PIN/INVALID` + writer missing-scope | no-write with fault present; restored re-verify |
| O14 | `test_o14_byte_equal_existing_root_refuses` | re-`materialize` over complete set | `STAGED_ROOT_EXISTS` + no-write; verifier `VERIFIED` |
| R1 | `test_r1_genuine_owner_binds_materialization` | pure comment + fixture-subprocess refresh (1800s) → prepare/capture/scope/`materialize`/`verify` | `observed_head==R1`; receipt binding; non-emission |

Static inventory: module 114460 B `be133819…`, test 112080 B `ebc82355…`,
schema 5627 B `4fa61723…` (unchanged); `static21.json` 21 exact pins;
inherited18 18/18, 84 caches 84/84 verified read-only.
Deferred: root-selected smoke/affected/full runs; B's runner/proof drafts.
