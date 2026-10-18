# P3S coverage matrix (authored, NOT yet executed)

16 behavioral methods in
`tests/test_survey_editorial_staged_source_v2.py` (module A3). Every row calls
real APIs and asserts exact result/error + immediate no-write or exact owned
delta BEFORE any repair. No mocks-as-oracles (`mock` is not even imported),
no decorative reruns, no old13+1/25/36 transfer.

Conventions: `_snapshot` skips `__pycache__`; fixture roots are independent
temp dirs committed BEFORE authority (UNTRACKED_P3S_SOURCES 18 entries =
inherited 15 + new3) with `.github` copied and inert `example.invalid` origin.

| # | Test method | Real seams (all verified signatures) | Expected |
|---|---|---|---|
| O1 | `test_o1_longform_materialize_and_replay` | LF `_complete(_chain())`→`_state_path`→`_advance_to_validated_draft`→`_authored`+narrative delta→P1 prepare/validate→P2R capture→scope→`materialize`→`verify` | `MATERIALIZED`+`REPLAY_VERIFIED`; 37 sorted `code_deps`; prose delta in `main.tex`; owned-delta-only; digest equality |
| O2 | `test_o2_weekly_materialize_and_replay` | `_build_weekly_validated`+cover delta→prepare/validate/capture/scope→`materialize`→`verify` | `WEEKLY_GENERATED_V2` route; envelope delta in `main.tex`; `VERIFIED` |
| O3 | `test_o3_coexistence_p1_refuse_p2r_p2v` | post-staging P1 `validate_proposal`, P2R `verify_retention`, P2V `observe_current_authority` | P1 raises; P2R `VERIFIED`; P2V `SCOPE_BOUND`; no-write |
| O4 | `test_o4_live_state_mutation_replay_ok_materializer_refuses` | live State `+p3s_artifact_probe` key; `verify`; fresh `materialize` | replay `VERIFIED` + no-write; writer raises |
| O5 | `test_o5_artifact_only_head_independence` | artifact-only file commit; `verify` | `VERIFIED` across HEAD change; no HEAD comparison |
| O6a | `test_o6a_tool_drift_reaches_check` | import-only `survey_review_attention_v2.py` comment append; `materialize` | `TOOL_DRIFT`; fault-present no-write; restore |
| O6b | `test_o6b_keep_drift_preempts_honestly` | KEEP-byte append; `materialize` | earlier KEEP/P2R refusal (NOT `TOOL_DRIFT`); no-write |
| O7 | `test_o7_scope_refusals` | missing path; `NEEDS_SCOPE_DETAIL` ordinary; `{not json` malformed | `SCOPE_*`/pin refusals; pre-write no-write each |
| O8 | `test_o8_path_ref_schema_inventory_tamper` | extra aux file; `{"a":1,"a":2}` manifest | `STAGED_SET_MISMATCH`; strict-parse refusal |
| O9 | `test_o9_alias_fifo_no_read` | symlink reader; `os.mkfifo` scope + 60 s timeout guard | `PATH_ALIAS`; FIFO refuses without hang; no-write |
| O10 | `test_o10_same_inode_vs_new_inode` | in-place `%` byte edit; `os.replace` same-byte swap | both refuse with distinct codes; no-write |
| O11 | `test_o11_root_file_replacement_and_midcall_drift` | pre-created staged dir; post-readback bib `os.replace` | `STAGED_ROOT_EXISTS`; drift refusal; no-write |
| O12 | `test_o12_partial_manifest_and_zeroed_output` | truncated manifest; empty subdir; zeroed `main.tex` | digest/set/replay refusals |
| O13 | `test_o13_immediate_no_write_before_repair` | TOOL_DRIFT fault; missing scope | fault-present snapshots equal before repair |
| O14 | `test_o14_byte_equal_existing_root_refuses` | re-`materialize` over complete set; `verify` | `STAGED_ROOT_EXISTS` + no-write; verifier still `VERIFIED` |
| R1 | `test_r1_genuine_owner_binds_materialization` | `_commit_r1_nonemitted_comment` (Python-only comment, committed) + `_R1_REFRESH_SCRIPT` in fresh subprocess → Weekly prepare/capture/scope/`materialize`/`verify` | refresh output nonempty; `MATERIALIZED` + `VERIFIED` bound to R1 basis |

Static file inventory (measured, NEW copy): module 77172 B `49a55643…`,
schema 5627 B `4fa61723…`, test 40738 B `92fcc964…`, all `0o664`;
inherited18 18/18 unchanged; status 105 rows (3M+18A+84pyc).

Deferred (B scope, non-overlapping `verification-tools/`): functioning
runner/proof drafts enforcing exact full105/static21/inherited18/preknown84
bytes+mode+size, HEAD/tree/index/Git rc PRE+POST, exclusive outputs,
runtime/argv/cwd/PIDs/allowlist, cache isolation, child/timeout/failure
accounting; complete21 saved patch + independent clean-409 apply proof. Root
selects smoke/affected/full after source + draft review.
