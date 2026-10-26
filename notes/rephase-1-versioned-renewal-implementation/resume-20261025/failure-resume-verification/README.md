# Failure/resume verification — TEST-only (no product source edits)

2026-10-25. Co-Worker parallel fault/resume matrix. RootHuman `f84fcf5` full unit NOT done.
Contract `478f0051` §9/11, root `7d7d5a45` §6, `astra-integration-corrections.md`,
`operation-oracles.md` govern. Candidate CURRENT CODE FROZEN.

Source:
- FIXED 739 `versioned-renewal-repair-input-20261025T082826Z/snapshot-work` (H `6fe86e78…`, P1 `825dba1d…`, PUB `3f4039fd…`, S `20f63eaf…`, HIGH `9a0469ef…`, Reader `098a2c82…`)
- Overlay `edpub 85814124…` + `test_editorial_renewal_archive_correction_20261025.py 5e5a…` => OWN 740.
- Freeze worker parallel 740 `versioned-renewal-archive-input-20261025T133248Z/snapshot-work` (`4e2783fb…` 740 lines) — cross-checked, not run.
- OWN SOURCE snapshot `versioned-renewal-faultresume-src-20261025T150000Z/snapshot-work` (byte-independent `cp -a`, no `-l`, pre/post pins, DST 740 SHA == `4e2783fb…`).
- Bootstrap READONLY `versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly` (721 `721a04d`, old E uncommitted).
- New fixture DB `versioned-renewal-faultresume-20261025T150000Z/renewal-weekly` (721 ancestry, 740 source-only commit before NEW authority, old E uncommitted, no hardlinks/alternates/env override, inert origin).

Method:
- No product source edits. Injection harness outside, OS-level only (`os.open/write/fsync/close/replace/stat/lstat`), exact target FD/path/seam, declarative scopes. No validator/proof mocks, no dummy SHA, no Stub HIGH. Original module bytes unchanged (pre/post SHA pinned).
- First healthy NEW U `fr-u1-weekly` SEALED_INERT via public `prepare_renewal`/`finalize_renewal` current740 (short chain, real existing PDF `0684697f…`/reviews reuse from `wk-boot-1`). State before pinned, new set valid.
- Fork byte-independent copies (`cp -a`, no `-l`, `nlink==1`, `dev:ino` disjoint verified) each case before activation.
- Each case: distinct raw UTC dir, PID, terminal exit, fresh Python child after Core commit. Capture immediate owned FS delta BEFORE repair, explicit operator next step + same public API healthy control. No automatic rollback/adopt unreferenced record. Do NOT delete failed partial/foreign files. NEW id/copy retry. Wrapper timeout != PASS; wait/poll owned child guard before retry.
- Cases: exclusive record collision (incl same bytes); record write/short-write/fsync/close + combined; orphan after complete record before State replace -> ordinary collision + explicit resume RESUMED; STATE temp write/close/fsync/replace; after-replace readback NEW/unknown; foreign inode + no unowned delete; neither-before-nor-after INDETERMINATE; already-active readonly + alias refuse; drift tool/basis/COPY/targets/reviews late guard; 32/33/cycle/sequence/anchor (typed fixture histories, NOT 32 genuine ops, labeled honestly); R1 after versioned pre-write optional.
- Counts: distinct methods/subcases, no false aggregation. All fails/skip/unexecuted listed. No whole-unit/independent PASS/CommitPoint.

Layout:
- `harness/` — `make_own_src_20261025T150000Z.py`, `make_fixture_20261025T150000Z.py`, `healthy_u1_20261025T150000Z.py`, `fault_harness_20261025.py` (OS injection + public API), `chain33_20261025.py`
- `manifest.json` — source IDs, pins, counts
- `raw/` — per-phase UTC dirs (`own-src-…`, `fixture-…`, `healthy-u1-…`, `case-…`), each with `commands.log`, `*-stdout.txt`, `*-stderr.txt`, `*-exit.txt`, `pid.txt`
- `testmatrix.md` — per-case intended seam, observed delta, repair, healthy control, counts
