# P3S R2 coverage matrix (authored, NOT yet executed)

26 behavioral methods. Every P3S writer/verifier call runs in a fresh
fixture-code subprocess with durable raw/meta outside cleanup
(`_run_p3s_fixture` + `_P3S_MATERIALIZE/VERIFY/FAULT_SCRIPT`); real P1/P2R/P2V
seams run in-process exactly as P1/P2R/P2V tests do. Fault scripts wrap ACTUAL
`os.*`/`Path.read_bytes`/staged-helper calls inside the fixture process (never
mock-replacement of authority/P2V/replay) and return fired counts + structured
code/phase/disposition + owned details. Snapshots are raw lstat maps
(dirs/identities/types/walk-errors); every refusal asserts immediate equality
or exact owned delta WITH the fault present (before repair). No mocks-as-oracles,
no decorative reruns, no old13+1/25/36 transfer.

Conventions: `_snapshot` skips `__pycache__`; fixture roots are independent
temp dirs committed BEFORE authority (UNTRACKED_P3S_SOURCES 18 entries =
inherited 15 + new3) with `.github` copied and inert `example.invalid` origin.

| # | Test method | Real seams (all verified signatures) | Expected |
|---|---|---|---|
| O1 | `test_o1_longform_materialize_and_replay` | LF `_complete(_chain())→_state_path→_advance_to_validated_draft→_authored`+narrative delta→P1 prepare/validate→P2R capture→scope→subprocess `materialize`→subprocess `verify` | `MATERIALIZED`+`VERIFIED`; 37 sorted `code_deps`; prose delta in `main.tex`; owned-delta-only; digest binding |
| O2 | `test_o2_weekly_materialize_and_replay` | `_build_weekly_validated`+cover delta, same chain | `WEEKLY_GENERATED_V2`; envelope delta; `VERIFIED` |
| O3 | `test_o3_coexistence_p1_refuse_p2r_p2v` | post-staging P1 `validate_proposal`; P2R `verify_retention`; P2V `observe_current_authority` | P1 raises; P2R `VERIFIED`; P2V `SCOPE_BOUND`; no-write |
| O4 | `test_o4_live_state_mutation_replay_ok_materializer_refuses` | live State `+p3s_artifact_probe`; subprocess `verify`; subprocess `materialize` | replay `VERIFIED` + no-write; writer `OBSERVER_REFUSED` |
| O5 | `test_o5_artifact_only_head_independence` | artifact-only file commit; subprocess `verify` | `VERIFIED` across HEAD change; head differs |
| O6a | `test_o6a_tool_drift_reaches_check` | healthy `materialize`+`verify`, then tamper import-only `survey_review_attention_v2.py`, subprocess `verify` | `TOOL_DRIFT` (verifier, no earlier KEEP preemption); fault-present no-write; restore re-verifies |
| O6b | `test_o6b_keep_drift_preempts_honestly` | KEEP-byte append; subprocess `materialize` | earlier KEEP/P2R refusal, NOT `TOOL_DRIFT`; no-write |
| O7 | `test_o7_scope_refusals` | missing / `NEEDS_SCOPE_DETAIL` / `{not json` / `upstream_override=0*64`; subprocess `materialize` | `SCOPE_*` incl. `SCOPE_STALE_UPSTREAM`; fault-present no-write each |
| O8 | `test_o8_path_ref_schema_inventory_tamper` | extra aux; `{"a":1,"a":2}`; wrong-path ref; unknown field; swapped `code_deps` (all with recomputed digest+canonical) | `STAGED_SET_MISMATCH`; strict-parse refusal; `OUTPUT_PATH_MISMATCH`; `SCHEMA_INVALID`; `CODE_DEPS_MISMATCH` |
| O9 | `test_o9_alias_fifo_no_read` | symlink reader; FIFO reader (durable subprocess + 60s saved timeout); symlinked scope parent | `PATH_ALIAS` / `PATH_NOT_REGULAR…` without read/hang; pre/post no-write |
| O10 | `test_o10_same_inode_vs_new_inode` | in-place `%` byte edit; same-byte `os.replace` swap | edit → `REPLAY_MISMATCH`; swap → `VERIFIED` (documented) + no-write |
| O11 | `test_o11_root_preexisting_and_postreadback_drift` | pre-created staged dir; post-readback bib `os.replace` (+bytes) | `STAGED_ROOT_EXISTS`; `REPLAY_MISMATCH`; no-write |
| O11b | `test_o11b_midcall_reader_drift` | `drift-reader` fault (exact reader rel, real-helper read then append) | `STABILITY_VIOLATION` pre-claim; exact allowed delta = tampered reader only; fired==1 |
| O11c | `test_o11c_late_control_retained` | `late-control-add` / `late-retained-add` (real `_compare` then inject) | `ORIGINAL_*` at later boundary; exact injection present; fired==1 |
| O11d | `test_o11d_drift_before_claim_manifest` | `drift-before-claim` (real `_canonical` then tamper exact reader) / `drift-before-manifest` (real `_emit` then tamper COPY dest) | later-boundary refusal (`STABILITY` / `PIN_DRIFT`); fired==1 |
| O11e | `test_o11e_post_readback_replay` | `post-readback-edit` (real `_verify_outputs` then in-place edit) / `post-replay-samebyte-replace` (real `verify` then same-byte `os.replace` all 4) | edit → `REPLAY*`; same-byte → writer `FILE_REPLACED` (proves writer identity branch); fired==1 |
| O11f | `test_o11f_root_ancestor_replace` | `root-replace` / `ancestor-replace` (rename after mkdir before files) | `STAGED_ROOT*`/`ANCESTOR*`/`PATH_ALIAS` before writes; fired==1 |
| O12a | `test_o12a_preexisting_tamper_verify` | truncated manifest; empty subdir; zeroed `main.tex` | `PIN_UNREADABLE`; `STAGED_SET_MISMATCH`; `REPLAY_MISMATCH` |
| O12b | `test_o12b_during_write_faults_incomplete` | `zero-write`/`write-fail`/`fstat-fail`/`mkdir-fail` (fresh root each, leaf-targeted, fired==1) | exact per-fault delta (root+main.tex vs {}); `bytes_written==0`; live-unchanged |
| O12c | `test_o12c_fsync_close_indeterminate` | `fsync-fail`/`close-fail` (fresh roots, leaf-targeted, fired==1) | `FSYNC_FAILED`/`CLOSE_FAILED` + `INDETERMINATE`; exact root+main.tex; live-unchanged |
| O12d | `test_o12d_manifest_failure_indeterminate` | `manifest-write-fail` (root+3+empty-manifest) / `manifest-close-fail` (root+4 complete, still `VERIFIED`) | `INDETERMINATE` both; exact partials; live-unchanged; fired==1 |
| O12e | `test_o12e_fstat_identity_mismatch` | `fstat-fake` identity swap (leaf-targeted, fired==1) | `STAGED_FILE_REPLACED`; exact root+empty-file (not whole-tree no-write) |
| O12f | `test_o12f_short_partial_combined_close` | `short-once` (positive completion) / `partial-then-fail` (1 byte then fail) / `write-then-close-fail` (primary+secondary) | short → `MATERIALIZED` fired==1; partial → `WRITE_FAILED` fired==2 `bytes_written==1`; combined → primary `WRITE_FAILED` with secondary attached fired==2 |
| O13 | `test_o13_immediate_no_write_before_repair` | standalone verifier `TOOL_DRIFT` (healthy set → tamper `survey_completeness_v2.py` → verifier) + missing scope (writer) | verifier `TOOL_DRIFT` no-write + restored re-verify; writer missing-scope no-write |
| O14 | `test_o14_byte_equal_existing_root_refuses` | re-`materialize` over complete set (subprocess) | `STAGED_ROOT_EXISTS` + no-write; verifier still `VERIFIED` |
| R1 | `test_r1_genuine_owner_binds_materialization` | pure-comment commit (AST-identical) + fixture-subprocess refresh on SAME built State → `_weekly_prepare_from`→capture→scope→subprocess materialize/verify | `observed_head == R1 commit`; basis receipt ref == refreshed receipt bytes; State changed; anchor absent from `main.tex` |

Static inventory (NEW copy): module 110461 B `821c57ba…`, schema 5627 B
`4fa61723…` (unchanged), test 104179 B `fa172fd3…`, all `0o664`;
inherited18 18/18 unchanged; status 105 rows (3M+18A+84pyc).
Deferred: root-selected smoke/affected/full runs; B's runner/proof drafts.
