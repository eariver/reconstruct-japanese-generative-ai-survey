# P3S R1 correction report (author A, pre-execution)

2026-10-18. Implements every concrete item in Astra `astra-code-draft-review-r1.md`
(R1–R5) and the accepted independent blockers B1–B4 plus Q1–Q8 dispositions.
Only new3 changed, in the same independent copy
`/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292`). Inherited18 18/18 unchanged; 84 caches frozen
(105 status rows = 3M + 18 new + 84 pyc before and after). No imports, no
test/fixture runs, no network/commit/push; no `verification-tools/` or root-doc
edits. Initial draft preserved in `initial-new3/` with pins (`README.md`).

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 97353 | 0o664 | `90c950d7b1a11829c06cd6579de0222b9016e173ae4c0d5b7c87994438b95d53` |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 68949 | 0o664 | `7b6912e2294ff2e46a86e8f81ae7b5102030fcadf6a62698413164c639b1b8df` |

Module AST-OK (23 defs), test AST-OK (21 methods), schema
`Draft202012Validator.check_schema` OK. No `...[truncated` harness markers in
any new3 bytes (byte-verified). Cheap checks only (`PYTHONDONTWRITEBYTECODE=1`,
stdlib/third-party imports, no candidate-module imports).

## R1 — positive-path blockers (all fixed)

- **R1-1** Route schemas are now checked AS schemas (`load_schema` for both
  route schemas); the actual pinned staged reader is validated later via the
  route canonicalizer. The old self-`validate_instance` block is gone.
- **R1-2** Config is pinned in the writer Session at PIN phase
  (`orig_config_sha`), cross-checked live-Collector vs Session, and W1 uses
  the pinned bytes (no second read that could move the basis).
- **R1-3 (critical)** The `staged_rel` overwrite is fixed: output directory
  (`staged_rel`) and staged reader file (`staged_reader_rel`) are distinct
  immutable names; manifest/claim/output paths all derive from the directory.
- **R1-4** Runtime binding stays strict (S2 byte+path `__file__` tripwire,
  file-pin producers never imported). Tests now execute public P3S operations
  in fresh fixture-code subprocesses (`_run_p3s_fixture` + `_P3S_MATERIALIZE_
  SCRIPT` / `_P3S_VERIFY_SCRIPT`, sanitized env, `cwd=root`, saved JSON
  outcome or saved timeout); the in-process `_materialize` outer-P2V helper is
  removed (Q7).

## R2 — original boundaries (all fixed)

- New `_snapshot_originals` / `_compare_original_boundary` /
  `_recheck_consumed_pins` helpers: full control+edition+retained inventories
  (incl. empty dirs, deletions AND additions, mode/size equality) compared
  against ORIGINAL snapshots — never a rebaselined capture. `Session.reverify`
  alone never substitutes for planted-file/empty-dir walks.
- Guards wired at: pre-claim (zero admitted delta), pre-manifest (exactly the
  3 outputs + staged dir), FINAL (exact 4-file edition delta; control and
  retained deltas must be zero) — plus tree recompute vs `init_tree`.
- `init_ctrl/init_ret/init_tree` are now consumed (previously captured unused).
- Second P2V compares explicit normalized refs (path AND SHA) vs ORIGINAL pins
  AND vs the first observation; before/upstream digests and both HEADs
  cross-checked; dynamic pins bound (`input_hashes` overlap must be
  byte-identical). No whole-map equality.
- New real cases: late control/retained empty-dir/file must refuse (covered by
  the FINAL zero-delta compares), pre-write drift and before-manifest drift
  via `drift-reader` fault test O11b (exact owned-delta: only the injected
  reader change), stale-upstream scope (O7).

## R3 — ownership / primary-secondary (all fixed)

- Claim records the mkdir attempt immediately and qualifies the unavoidable
  mkdir→open window in a comment (no global exclusion claimed). Held-root
  fstat vs owned `staged_identity` is checked before EACH file write
  (ancestors held open = ancestor binding).
- `_write_owned_file` records attempt → identity → progress/bytes → fsync →
  close → readback states in the owned entry; open/fstat failures preserve
  unknown identity explicitly; fsync seam added (`FSYNC_FAILED` →
  INDETERMINATE, no atomicity/power-loss claim).
- Primary-preserving closes everywhere: write-error primary survives close
  failure via `_attach_close`; FINAL dir close and final `_close_session`
  reclassify to INDETERMINATE with owned diagnostics (never a success label).
- Manifest-phase disposition: output-write failures → INCOMPLETE
  (OWNED_PARTIAL); manifest write/close/final failures with possibly complete
  bytes → INDETERMINATE_INVOCATION. Close failure on outputs also reports
  INDETERMINATE (bytes complete, close unproven). No retry/rewrite/cleanup.

## R4 — verifier claims (all fixed)

- Staged `basis`/`proposed` compared for equality to the proposal (not only
  retention-vs-proposal); staged `proposal_ref` all 6 ID fields compared;
  top-level labels + strict 8-key contract identity must agree both sides.
- `style_input_ref` validated as fixed template path/hash/size; staged
  `style` output byte-equality enforced (the old self-comparison removed).
- V6 repeats retained exact inventory + COPY/KEEP byte re-pins + original
  consumed pins after scope/rendering (no current-State/HEAD authority, no
  blanket `capture_inputs` equality).
- Verifier now recomputes/validates in an order where semantic tamper tests
  recompute digest+canonical bytes first (`_retamper_manifest`), so targeted
  checks (`OUTPUT_PATH_MISMATCH`, `SCHEMA_INVALID`, `CODE_DEPS_MISMATCH`)
  fire instead of an earlier digest failure.

## Q dispositions

- Q1 dead byte-check removed (`if not manifest_bytes`). Q2 duplicate
  `_verify_outputs_and_manifest` call removed. Q3 pyc tolerance kept with an
  explicit tripwire-limit comment (no hotpatch-proof claim). Q4 proposal_ref
  IDs + contract identity compared under R4. Q5 sorted/exact-37 enforced in
  code (`_route_code_deps` size assert + order equality); schema cited only
  for shape. Q6 generics tightened (ProposalError/RETENTION_DEST_CONFLICT,
  STABILITY/REPLAY/TOOL_DRIFT/STAGED_ROOT_EXISTS/PATH codes; remaining
  refusal-presence asserts are typed `StagedSourceError` + no-write proofs).
  Q7 outer P2V removed from helpers (kept only in O3 coexistence). Q8 digest
  representation retained (`sha256_object` body vs indent2 canonical file
  bytes — intentionally different, documented).

## B1–B4 (accepted blockers, all addressed)

- **B1** `os.fsync` seam added; during-write faults via scoped wrappers around
  actual `os.*` calls inside the fixture subprocess: zero/short-fail writes,
  fsync-fail, close-fail (incl. manifest variants), fstat-fail/fake-identity,
  mkdir-fail, mid-call reader drift. O12 relabelled: O12a verify-level tamper,
  O12b–O12e genuine during-write faults with phase-appropriate
  INCOMPLETE/INDETERMINATE classification + exact owned-partial assertions
  (e.g. close-fail leaves exactly root+main.tex).
- **B2** O10 corrected: same-inode content change → verifier refuses
  (`REPLAY_MISMATCH`); same-byte/new-inode → verifier VERIFIES (documented
  byte-consistency semantics); the FILE_REPLACED identity oracle stays in
  writer FINAL, which every successful materialization exercises.
- **B3** Added: stale-upstream scope (O7), wrong-path same-SHA
  `OUTPUT_PATH_MISMATCH`, unknown-field `SCHEMA_INVALID`, unsorted-deps
  `CODE_DEPS_MISMATCH` (O8, all with recomputed digest/canonical per R4);
  alias staged-reader, FIFO staged-reader (killable subprocess, saved
  timeout outcome, never hangs), symlinked scope-parent ancestor (O9);
  mid-call drift with exact owned delta (O11b); fstat identity (O12e).
- **B4** R1 rewired to the SAME chain: `_weekly_prepare_from` reuses the
  refreshed helper/built State; assertions bind materialization to the R1
  basis (`observed_head == R1 commit`, basis receipt ref == refreshed receipt
  bytes, pre/post State change, non-emission of the anchor in `main.tex`).
  The comment insertion is pure (AST dumps identical) at column 0 above the
  owner `def`.

## Remaining limitations (no blockers, recorded honestly)

- No execution yet: all 21 methods unauthored at runtime; every seam, code,
  and binding string is a pre-execution claim for root-selected runs.
- `_check_runtime_binding` remains a tripwire, not a hotpatch proof.
- Ancestor-replace *during* a write is covered by pre-write alias refusal +
  FINAL identity/inventory rechecks, not by a mid-syscall swap injection.
- `reader-surface-input` Weekly path has no `canonical_reader_bytes`
  equivalent; Weekly replay binds FILE bytes to the canonical digest
  (same as P2V), not a second canonicalization.
