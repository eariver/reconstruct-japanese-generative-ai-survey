# P3S R6 correction report — post-smoke test-only oracles (pre-execution)

2026-10-18. Implements all seven root post-smoke items on the R5 candidate.
Module (`7059166e…`) and schema (`4fa61723…`) UNCHANGED — no implementation
defect found requiring selection (one generic-code observation below, not
changed). Only `tests/test_survey_editorial_staged_source_v2.py` changed:
114642 B `6b35a3e5…` → 141792 B `0e1cc20f…`, 2277 → 2521 lines, still 26 test
methods (no method added/removed; +1 embedded constant
`_R1_FIXTURE_PREPARE_SCRIPT`). No imports, no test/fixture runs, no
network/commit/push; no `verification-tools/` or root-doc edits. Prior R5 bytes
preserved in `draft-history-r6/prior-bytes-r6/`; R5 reports untouched.

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 |
|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 126181 | 0o664 | `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65` (unchanged) |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) |
| `tests/test_survey_editorial_staged_source_v2.py` | 141792 | 0o664 | `0e1cc20fa0d34f6d4096bd1f99865513d4c4f1e07e6fdf20a2c36dfff6c52d9d` |

Module AST-OK (25 defs), test outer AST-OK (26 test methods + helpers), schema
Draft202012Validator.check_schema OK. Every embedded child program AST-OK via
literal-eval + `ast.parse` (no fixture execution): `_P3S_MATERIALIZE_SCRIPT`
1120, `_P3S_VERIFY_SCRIPT` 729, `_P3S_FAULT_SCRIPT` 11997,
`_R1_FIXTURE_PREPARE_SCRIPT` 3473 (new). No `...[truncated` markers; single
`__main__` only. Status 105 rows (3M + 18A + 84 pyc).

## Evidence-transfer body hashes (qualified scoped2 + later24)

O1 `9da4a76dab317364` and O2 `e730fc8ff6146e4b` AST-body hashes IDENTICAL
R5→R6. All 24 shared helper bodies IDENTICAL R5→R6 (`_lf_prepare`, `_weekly_prepare`,
`_weekly_prepare_from`, `_capture`, `_scope_for`, `_materialize`, `_verify`,
`_retamper_manifest`, `_snapshot`, `_assert_no_write`, `_assert_no_write_except`,
`_assert_owned_delta_only`, `_run_p3s_fixture`, `_launch_durable_child`,
`_durable_base`, `_make_p3s_source_root`, `_copy_base`, `_run_fixture_code`,
`_commit_r1_nonemitted_comment`, `_run_git`, `_fresh_lf_root`, `_fault_run`;
full list verified equal). New code is only the `_R1_FIXTURE_PREPARE_SCRIPT`
constant and test-body edits in non-protected tests
(o4/o6b/o7/o8/o9/o11e/o11f/o12a/o12b/o12c/o12d/o12e/o12f/o13/o14/r1). Runtime
`/usr/bin/python3` 3.14.4 and schema unchanged. R5 O1/O2 smoke evidence stays
bound to R5; transfer qualification (scoped2 + later24) is for root selection,
not claimed here — no new full26 run performed.

## Item 1 — O7 exact wrapped codes + injection-present snapshots + cleanup

- Missing scope file: session pin fails at writer PIN before any scope logic.
  Assert exact `WRITER_FAILED/PIN/REFUSED_PRE_WRITE` (+ absent-path assert).
  Prior `SCOPE_` expectation was wrong (invented late reachability).
- Ordinary (`NEEDS_SCOPE_DETAIL`), malformed (`{not json`), stale
  (`upstream_override=0*64`): all reach the in-call observer and refuse there.
  Assert exact `OBSERVER_REFUSED/OBSERVE/REFUSED_PRE_WRITE` plus the
  distinguishing detail substring (`SCOPE_NOT_WITHIN_AUTHORITY`,
  `SCOPE_UNREADABLE`, `SCOPE_STALE_UPSTREAM` respectively) and a mutation
  assert (ordinary decision field, malformed raw bytes, stale upstream field).
- Snapshot WITH each injection present; compare immediately (fault-present).
  Ordinary + stale review records are deleted before the final restored
  comparison (malformed already was); final `base` equality now accounts for
  every deliberately created record instead of falsely comparing against a
  baseline that lacks them.

## Item 2 — O8 pristine-per-case + canonical dup-key + semantic coverage

- Pristine canonical manifest bytes saved once after materialize; EVERY case
  restores pristine first, applies exactly one mutation, recomputes
  digest+canonical, snapshots with the fault present, asserts exact
  code/phase, then proves no-write before repair. Final restore + successful
  `_verify` proves each tamper caused its refusal.
- Duplicate-key uses the CANONICAL manifest path (raw `{"a": 1, "a": 2}`
  written to `staged-source-manifest.json`) → `PIN_UNREADABLE/PIN/INVALID`
  (strict parser refusal), not a foreign-filename refusal.
- New semantic cases (each exact code/phase): basis tamper →
  `BASIS_MISMATCH/PIN/INVALID`; proposed tamper → `PROPOSED_MISMATCH/PIN/INVALID`;
  `style_input_ref` tamper → `STYLE_REF_MISMATCH/REPLAY/INVALID`; extra
  `proposal_ref` ID → `PROPOSAL_REF_MISMATCH/PIN/INVALID`; top-level
  `issue_id` → `LABEL_MISMATCH/PIN/INVALID`; contract-identity value →
  `CONTRACT_IDENTITY_MISMATCH/PIN/INVALID`; outputs.style bytes →
  `REPLAY_MISMATCH/REPLAY/INVALID`. Retained: wrong-path
  (`OUTPUT_PATH_MISMATCH/REPLAY/INVALID`), unknown-field
  (`SCHEMA_INVALID/PIN/INVALID`), swapped-deps
  (`CODE_DEPS_MISMATCH/PIN/INVALID`), extra-aux
  (`STAGED_SET_MISMATCH/VERIFY/INVALID`).

## Item 3 — O9 rename-restore + exact codes, FIFO no-read proof

- Original reader preserved by `rename` to `*.orig-p3s-restore` (inode-preserving
  restore via rename-back); final `base` equality now holds instead of the
  impossible byte-copy restoration claim. Same pattern for the FIFO case.
- Alias reader: exact `LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE` + `PATH_ALIAS`
  detail; injection asserted (`symlink` kind + copy bytes equal original).
- FIFO at the actual reader path: exact `LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE`
  + `PATH_NOT_REGULAR` detail, 60s bound with explicit no-timeout assert and
  no-write; refusal happens at `col.safe` lstat before any open/read.
- Scope-parent symlink: exact `WRITER_FAILED/PIN/REFUSED_PRE_WRITE` +
  `PATH_ALIAS` detail (session pin fails before scope logic); injection
  asserted (`symlink` kind); ancestor copy content asserted equal.

## Item 4 — O6b exact KEEP target, truthful prepin code

- Target is the lexicographically first KEEP `retained_ref` path after excluding
  individually-pinned files (State/Profile/proposal/manifest/scope/config/
  authoring/reader), documented in-test — deterministic, not arbitrary.
- R4 prepin hash-binds every plan row first, so the refusal is the prepin
  itself: exact `PIN_FAILED/PIN/REFUSED_PRE_WRITE` (ProposalError carries no
  `.code`; prepin preserves the typed shape as PIN_FAILED). `TOOL_DRIFT`
  absence still asserted — O6a remains the standalone TOOL_DRIFT test.
- Fault-present delta asserted (`allowed_changed={target}`, unchanged
  originals), injection bytes asserted (`original+b"\n"`), restored equality
  asserted.

## Item 5 — O11c/O11e/O11f/combined exact deltas (no observed-derived allowances)

- O11c: exact `ORIGINAL_DRIFT/PRE_CLAIM/REFUSED_PRE_WRITE`; allowed-new sets are
  now literal expected values (`{probe}` / `{expected_dir}`), not derived from
  the observed diff; injection content/kind asserted; unchanged-originals via
  exact allowed sets.
- O11e post-readback: exact `REPLAY_UNVERIFIED/REPLAY/INDETERMINATE_INVOCATION`;
  allowed-new = owned5 (root+4 incl. manifest), allowed-changed = {main};
  injected marker bytes asserted.
- O11e samebyte: exact `FILE_REPLACED/FINAL/INDETERMINATE_INVOCATION`;
  allowed-new = owned4, no changed; complete bytes asserted (size>0 all files);
  no `*.swap-p3s` leftovers asserted.
- O11f root: exact `STAGED_ROOT_REPLACED/CLAIM/OWNED_PARTIAL`; allowed-new =
  `{backup, staged, staged/replacement.txt}` + injection bytes; no staged file
  bytes; unchanged originals. Ancestor: allowed-new = `{backup, staged-symlink}`
  + symlink-target assert. Both document post-earliest-identity timing (fault
  wraps first `_emit`, i.e. after CLAIM mkdir+earliest+open+fstat+entry bind).
- Combined write-then-close: exact `STAGED_FILE_WRITE_FAILED/CLAIM/OWNED_PARTIAL`
  + attached secondary; allowed-new = {root, main}; bytes_written==0; unchanged
  originals. (O12b/c/d/e already exact with deltas; O12b fstat extended with
  empty-file asserts; O12c fsync/close extended with full-bytes/fsync-state
  asserts; O12d manifest-write/close extended with codes
  `STAGED_FILE_WRITE_FAILED`/`CLOSE_FAILED` + empty/full-bytes asserts; O12e
  extended with empty-file size assert.)

## Item 6 — root/ancestor injection timing

Covered under item 5: injection occurs in `_emit_wrap` before the first real
`_emit`, i.e. strictly after the CLAIM earliest-identity pin
(mkdir→earliest-entry→open→fstat→entry bind). The blind mkdir-to-earliest
window is not tested and not claimed. The canonical-entry-vs-owned-ID check
(`STAGED_ROOT_REPLACED`) before the first file write is the tested seam, with
exact allowed partials proving no file bytes were written.

## Item 7 — audit + R1 fixture-side prepare + O4 prepin code

- All negative code/phase assertions re-mapped to the actual call graph
  (details above; O4 below). No generic `Exception` asserts; broad regexes
  kept only as distinction supplements alongside exact code+phase (O9 FIFO
  alternation, O11b already exact). Missing-scope and scope-ancestor WRITER_FAILED
  is the actual wrapped code for pre-scope PIN pin failures — recorded as
  actual behavior, not a scope-code invention; if root wants SCOPE_-specific
  codes there, that is a module change for selection (not implemented).
- O4 stale live-State now refuses at R5 prepin: exact
  `PIN_FAILED/PIN/REFUSED_PRE_WRITE` (+`REF_DRIFT` detail + mutation-present
  assert + writer no-write). Prior `OBSERVER_REFUSED` expectation predates
  prepin and is preserved in earlier drafts.
- R1: added `_R1_FIXTURE_PREPARE_SCRIPT` (fixture-cwd, fixture imports, stub
  asserts) performing stage→prepare→validate→capture→verify→scope on the
  SAME refreshed chain; test now passes only string paths + proposal id (no
  parent-imported modules touch the fixture after the source commit). Binding
  asserts unchanged (head==R1 commit, receipt bytes, non-emission, reader
  digest). `_weekly_prepare_from` helper left untouched for O2.

## Static21 / caches (NEW, read-only)

`draft-history-r6/static21.json` 3670 B `f37cf825…`: canonical flat JSON
(outer sorted, inner `sha256/bytes/mode`), exact
21 entries (18 inherited + 3 new). New3: module `7059166e…` 126181 B,
test `0e1cc20f…` 141792 B, schema `4fa61723…` 5627 B, all `0o664`.
Inherited18 18/18 match `expected18-source-correction-v5.json`; 84 caches 84/84
match `cache-inventory-static.json`; 0 mismatches, no baselining.

## Remaining concerns (no execution in this unit; for root selection)

- Missing-scope and scope-ancestor WRITER_FAILED generality (above): actual
  behavior, asserted exactly; SCOPE_-specific codes would be a module change.
- Prepin `PIN_FAILED` masking of the underlying P1 `REF_DRIFT` code (no `.code`
  on ProposalError): actual behavior, asserted exactly; propagating P1 codes
  through prepin would be a module change.
- O6b target depends on fixture KEEP inventory (lexicographically first
  non-individually-pinned KEEP path); deterministic for the recorded fixture
  recipe but re-verify the selected path if the recipe changes.
- Ancestor-replace *during* a write remains covered by pre-write alias +
  held-fd + canonical recheck + FINAL, not mid-syscall swap injection (honestly
  disclosed; no post-final-injection guarantee).
- Weekly has no `canonical_reader_bytes` equivalent (disclosed); R1 refresh
  script itself unchanged (`p2vt._R1_REFRESH_SCRIPT`).
- No execution PASS claimed: all 26 methods unaudited at runtime post-edit;
  O1/O2 evidence stays bound to R5 (bodies unchanged). A qualified scoped2 +
  later24 may be considered by root; no full26 claim here. Root will select a
  fail-fast batch first.
