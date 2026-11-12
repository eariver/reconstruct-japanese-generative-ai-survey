# Applied-source verification — supplement-carry packaging proof-copy (independent runner, read-only)

Packet: `notes/rephase-1-supplement-carry-repair-20261106/applied-verification-20261107T035441Z/`
Proof: `.rephase-1-editorial-runtime/supplement-carry-packaging-20261107T034506Z/proof-copy/candidate-partial-b40de60` (actual409 + complete141/773). No modify/commit. No subagents.

## Source bounds (pre/post identical, read-only)

- Proof-copy 773 files excl .git, 0 pyc/__pycache__; manifest `complete-supplement-carry-manifest.json` f88f6d088381beb7cb975b068ef308ddb8d794c8daffc92639d6f11e62e470cf / 202750B, files 773 = 689+84, delta 57M+84A=141, patch 3032752c.../5526524B
- 5 hashes pre==post: LOW d50282bf.../239978B, HIGH f312f02e.../97844B, focused 5d5d3aade.../60569B (14), scale 7118092f.../27736B, Ctest 1fa905bf.../43626B — match manifest table + pins-workcopy-773
- Loaded modules resolve to proof-copy/scripts/... (see pre-loaded-module-paths.txt)
- Process-scoped identity only (GIT_AUTHOR/COMMITTER + GIT_CONFIG_NOSYSTEM + GIT_OPTIONAL_LOCKS), no HOME/config-root/gitconfig writes, no --allow-empty, no ordinary commit/push, no network/Production/reconstruct Git/readback; synthetic example.invalid only; PYTHONDONTWRITEBYTECODE=1; fresh temp-DB fixtures normally; no cleanup beyond test-owned lifecycle
- Fixture policy inspection COMPLIANT, no relaxed-policy needed

## Batches (unique PIDs, unmasked exits, fresh fixtures from applied source)

- Batch 01 C-direct FULL (7): `tests.test_dm022_c_direct_operation_v2` all 7 — 7 run / 7 pass / 0 fail / 0 skip, 18.760s, exit 0. Raw `batch-01-c-direct-full-raw.txt` (PID 784227, 035456Z-035515Z, pre/post SHA identical). Methods: test_c_direct_weekly_prepare_adopt_readback, test_c_thematic_direct_prepare_adopt_readback, test_c_derived_weekly_true_r_not_equal_e, test_c_negatives_profile_copy_retention_refuse_no_write, test_c_binding_ref_mismatch, test_c_binding_integrity_drift (corrected N7 expects exact non-DROP coverage, now passes), test_c_report_positive_control_extra_rows_pass.
- Batch 02 replaced focused (2): `SupplementCarryFocusedTests.test_weekly_derived_replaced_manifest` + `test_thematic_replaced_manifest` — 2 run / 2 pass / 0 fail / 0 skip, 8.267s, exit 0. Raw `batch-02-replaced-focused-raw.txt` (PID 785939, 035522Z-035531Z). Proves replaced supp on Weekly DERIVED (27+3 same+replaced Raw) and Thematic/Special (same+replaced Raw, unaffected preserved).

Totals in this packet: 9 run, 9 pass, 0 fail, 0 skip. No fail-first trigger (no unexpected failure, no fix/rerun).

## Not repeated

- 19 scaling whole, A2 14, other scale tests — just counts referenced from prior affected-verification-20261107T031826Z, not re-run per authorization. No full suite, no CURRENT-proof re-run, no semantic/adoption claim.

## Files

- pre-sha256-pins.txt, pre-manifest-hash.txt, pre-loaded-module-paths.txt, pre-env.txt, pre-inspection.txt, manifest-binding-table.txt, batch-01-*, batch-02-*, post-snapshot.txt, SUMMARY.md
