# P3S R1 coverage matrix (authored, NOT yet executed)

21 behavioral methods. Every P3S writer/verifier call runs in a fresh
fixture-code subprocess (`_run_p3s_fixture` + `_P3S_MATERIALIZE_SCRIPT` /
`_P3S_VERIFY_SCRIPT` / `_P3S_FAULT_SCRIPT`); real P1/P2R/P2V seams run
in-process exactly as P1/P2R/P2V tests do. Fault scripts wrap ACTUAL
`os.*`/`Path.read_bytes` calls inside the fixture process (never
mock-replacement of authority/P2V/replay). Snapshots are raw lstat maps
(dirs/identities/types/walk-errors); every refusal asserts immediate
equality with the fault present (plus explicit allowed fault artifacts).

| # | Test method | Seams | Expected |
|---|---|---|---|
| O1 | `test_o1_longform_materialize_and_replay` | LF `_complete(_chain())→_state_path→_advance_to_validated_draft→_authored`+narrative delta→P1 prepare/validate→P2R capture→scope→subprocess `materialize`→subprocess `verify` | `MATERIALIZED`+`VERIFIED`; 37 sorted `code_deps`; prose delta in `main.tex`; owned-delta-only; digest binding |
| O2 | `test_o2_weekly_materialize_and_replay` | `_build_weekly_validated`+cover delta, same chain | `WEEKLY_GENERATED_V2`; envelope delta; `VERIFIED` |
| O3 | `test_o3_coexistence_p1_refuse_p2r_p2v` | post-staging P1 `validate_proposal`; P2R `verify_retention`; P2V `observe_current_authority` | `ProposalError RETENTION_DEST_CONFLICT` + no-write; P2R `VERIFIED`; P2V `SCOPE_BOUND` |
| O4 | `test_o4_live_state_mutation_replay_ok_materializer_refuses` | live State `+p3s_artifact_probe`; subprocess `verify`; subprocess `materialize` | replay `VERIFIED` + no-write; writer `OBSERVER_REFUSED` |
| O5 | `test_o5_artifact_only_head_independence` | artifact-only commit; subprocess `verify` | `VERIFIED` across HEAD change; head differs |
| O6a | `test_o6a_tool_drift_reaches_check` | import-only `survey_review_attention_v2.py` append; subprocess `materialize` | `TOOL_DRIFT` + fault-present no-write; restore |
| O6b | `test_o6b_keep_drift_preempts_honestly` | KEEP-byte append; subprocess `materialize` | earlier KEEP/P2V refusal, NOT `TOOL_DRIFT`; no-write |
| O7 | `test_o7_scope_refusals` | missing / `NEEDS_SCOPE_DETAIL` / `{not json` / `upstream_override=0*64`; subprocess `materialize` | `SCOPE_*` refusals incl. `SCOPE_STALE_UPSTREAM`; fault-present no-write each |
| O8 | `test_o8_path_ref_schema_inventory_tamper` | extra aux; `{"a":1,"a":2}`; wrong-path ref; unknown field; swapped `code_deps` (all with recomputed digest+canonical) | `STAGED_SET_MISMATCH`; strict-parse refusal; `OUTPUT_PATH_MISMATCH`; `SCHEMA_INVALID`; `CODE_DEPS_MISMATCH` |
| O9 | `test_o9_alias_fifo_no_read` | symlink reader; FIFO reader (subprocess+120 s saved timeout); symlinked scope parent | `PATH_ALIAS` / `PATH_NOT_REGULAR…` without read/hang; pre/post no-write |
| O10 | `test_o10_same_inode_vs_new_inode` | in-place `%` byte edit; same-byte `os.replace` swap | edit → `REPLAY_MISMATCH`; swap → `VERIFIED` (documented) + no-write |
| O11 | `test_o11_root_preexisting_and_postreadback_drift` | pre-created staged dir; post-readback bib `os.replace` (+bytes) | `STAGED_ROOT_EXISTS`; `REPLAY_MISMATCH`; no-write |
| O11b | `test_o11b_midcall_reader_drift` | `drift-reader` fault (tamper after pin read in fixture subprocess) | `STABILITY_VIOLATION` pre-claim; exact allowed delta = tampered reader only |
| O12a | `test_o12a_preexisting_tamper_verify` | truncated manifest; empty subdir; zeroed `main.tex` | `PIN_UNREADABLE`; `STAGED_SET_MISMATCH`; `REPLAY_MISMATCH` |
| O12b | `test_o12b_during_write_faults_incomplete` | `zero-write`/`write-fail`/`fstat-fail`/`mkdir-fail` (fresh root each) | `STAGED_FILE_WRITE_FAILED`/`STAGED_FILE_FSTAT_FAILED`/`STAGED_ROOT_CREATE_FAILED`; admitted owned delta only |
| O12c | `test_o12c_fsync_close_indeterminate` | `fsync-fail`/`close-fail` (fresh roots) | `FSYNC_FAILED`/`CLOSE_FAILED` + `INDETERMINATE`; close-fail partials exactly root+main.tex |
| O12d | `test_o12d_manifest_failure_indeterminate` | `manifest-write-fail`; `manifest-close-fail` + later `verify` | `INDETERMINATE` both; complete bytes stay `VERIFIED` (no success invented) |
| O12e | `test_o12e_fstat_identity_mismatch` | `fstat-fake` identity swap | `STAGED_FILE_REPLACED` pre-write, no-write |
| O13 | `test_o13_immediate_no_write_before_repair` | TOOL_DRIFT file probe; missing scope (subprocess) | fault-present no-write; restored equality |
| O14 | `test_o14_byte_equal_existing_root_refuses` | re-`materialize` over complete set (subprocess) | `STAGED_ROOT_EXISTS` + no-write; verifier still `VERIFIED` |
| R1 | `test_r1_genuine_owner_binds_materialization` | pure-comment commit (AST-identical) + fixture-subprocess refresh on SAME built State → `_weekly_prepare_from`→capture→scope→subprocess materialize/verify | `observed_head == R1 commit`; basis receipt ref == refreshed receipt bytes; State changed; anchor absent from `main.tex` |

Static inventory (NEW copy): module 97353 B
`90c950d7b1a11829c06cd6579de0222b9016e173ae4c0d5b7c87994438b95d53`,
schema 5627 B `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46`
(unchanged), test 68949 B
`7b6912e2294ff2e46a86e8f81ae7b5102030fcadf6a62698413164c639b1b8df`,
all `0o664`;
inherited18 18/18 unchanged; status 105 rows (3M+18A+84pyc).
Deferred: root-selected smoke/affected/full runs; B's runner/proof drafts.
