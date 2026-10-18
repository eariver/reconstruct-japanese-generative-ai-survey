# Batch-D R9 diagnosis — O9/O10/O11b/O11c/O11e/O11f (scoped, read-only)

2026-10-18. Fresh read-only diagnosis of saved
`smoke-r9-batch-d-20261018T100340Z/` (9 ran / 4449.573s, no `-f`).
No source edits, no test/runtime, no imports/tests/network/DB/index,
no delegate. Candidate frozen R9 during parallel remaining-9 batch per
`notes/rephase-1-dm021-p3s/astra-write-fault-batch-selection.md:1-9`.
This doc is the only new file.

## 1. Identity scope

- Candidate: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
  detached `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, `index_empty=yes`,
  `remote=inert`, `status_rows=105` per
  `smoke-r9-batch-d-20261018T100340Z/batch-d.record.txt:17`.
- R9 pins: module `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65`
  126181B, schema `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46`
  5627B, test `b9f413234dcc4230be1dcc7865d649efcbadca284dde37e6d9284aa3f43c5604`
  144928B per `draft-history-r9/static21.json:52-95` and
  `draft-history-r9/correction-report-r9.md:24-28`. Only O8 body changed
  R8→R9; all O9/O10/O11b/c/e/f bodies identical R8→R9 per
  `correction-report-r9.md:39-47`. Runtime Python 3.14.4, runner `dc695ace…`,
  launcher `9a943c4a…`, manifest `draft-history-r9/static21.json` `fc33a030…`.
- Selectors (exact, no guesses) per `batch-d.record.txt:2-12`:
  O8 `test_o8_path_ref_schema_inventory_tamper`,
  O9 `test_o9_alias_fifo_no_read`, O10 `test_o10_same_inode_vs_new_inode`,
  O11 `test_o11_root_preexisting_and_postreadback_drift`,
  O11b `test_o11b_midcall_reader_drift`, O11c `test_o11c_late_control_retained`,
  O11d `test_o11d_drift_before_claim_manifest`,
  O11e `test_o11e_post_readback_replay`, O11f `test_o11f_root_ancestor_replace`.
- Saved outcome per `run-b3-batch-d-20261018T100340Z/run_p3s_b3.stderr.txt:1-97`:
  O8 ok, O9 FAIL, O10 FAIL, O11 ok, O11b FAIL, O11c FAIL, O11d ok,
  O11e FAIL, O11f FAIL; `Ran 9 tests`, `FAILED (failures=6)`.
  `launch.stdout:1-4` `child_rc=1 wrapper_rc=1 post_errors=[]`.
  `run_p3s_b3.stdout.txt` only fixture-produce lines + wrapper `timed_out=False`.

## 2. FULL durable raw (read via `cat`; `Read` refuses `.bin`)

Child stdout bins under
`run-b3-batch-d-20261018T100340Z/fixture-raw/` (all stderr 0B unless noted):

- O9 alias `p3s-p3s-0be8i37e`: `LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE`
  `PATH_ALIAS .../fixture-lf-p3s-9/reader-surface-input-v2.json`, `owned_files=0`.
  Field evidence: alias seam correct (test lines `1653-1658` pass).
- O9 FIFO `p3s-p3s-_772u924`: `LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE`
  `PATH_NOT_REGULAR .../fixture-lf-p3s-9/reader-surface-input-v2.json`,
  `owned_files=0`. Code/phase/disposition/regex all match test `1686-1690`;
  only `1684 assertNotIn("timeout", json.dumps(outcome))` fails (see §3).
  O9 ancestor subcase never ran (method aborted at FIFO assert).
- O10 `p3s-p3s-4rmhou44` materialize ok (`fixture-lf-p3s-10` digest `d8ae0c32…`);
  `p3s-p3s-6zh3b33t` verify: `{"ok":true,"result":"STAGED_SOURCE_REPLAY_VERIFIED",
  "reader":"e5105b31..."}` for `jgas-p3s-o10-haw62ogg`.
  Test `1754 assertFalse(outcome.get("ok"))` fails (`True is not false`).
  Second (same-byte replace) subcase never ran.
- O11b `p3s-p3s-zoxbxmyd` (`drift-reader`, `jgas-p3s-o11b`):
  `{"ok":false,"error":"StagedSourceError: LAYOUT_REFUSED: [PIN/REFUSED_PRE_WRITE] canonical proposal layout refused: STABILITY_VIOLATION: staged proposed reader changed mid-inspection: .../fixture-lf-p3s-11b/reader-surface-input-v2.json","code":"LAYOUT_REFUSED","phase":"PIN","disposition":"REFUSED_PRE_WRITE","fired":1,"owned_files":0}`.
  Expected `STABILITY_VIOLATION/PRE_WRITE/REFUSED_PRE_WRITE` at test `2136-2138`.
- O11c `p3s-p3s-pqur_6p_` (`late-control-add`):
  `{"ok":false,"error":"StagedSourceError: OBSERVER_REFUSED: [OBSERVE/REFUSED_PRE_WRITE] fresh current-authority observation refused: RECEIPT_INVALID: [DERIVE] P1: RECEIPT_INVALID: generated receipt validation failed: Longform current implementation or contract contains uncommitted source","code":"OBSERVER_REFUSED","phase":"OBSERVE","disposition":"REFUSED_PRE_WRITE","fired":1,"owned_files":0}`.
  Expected `ORIGINAL_DRIFT/PRE_CLAIM/REFUSED_PRE_WRITE` at test `2244-2246`.
  `late-retained-add` subcase never ran (loop aborted on first fault).
- O11e post-readback `p3s-p3s-wrt4m15c` (`post-readback-edit`):
  `REPLAY_UNVERIFIED/REPLAY/INDETERMINATE_INVOCATION`
  `standalone staged replay refused: REPLAY_MISMATCH ... staged main ...`,
  `fired=1`, `owned_files=4`. Matches test `2358-2360` — field success.
- O11e samebyte `p3s-p3s-a2vmymbt` (`post-replay-samebyte-replace`):
  `{"ok":false,"error":"StagedSourceError: SNAPSHOT_FAILED: [FINAL/INDETERMINATE_INVOCATION] snapshot failed: FILE_REPLACED: [FINAL/INDETERMINATE_INVOCATION] edition file file identity changed: .../fixture-lf-p3s-replace/staged-source/staged-source-manifest.json","code":"SNAPSHOT_FAILED","phase":"FINAL","disposition":"INDETERMINATE_INVOCATION","fired":1,"owned_files":0}`.
  Expected `FILE_REPLACED/FINAL/INDETERMINATE_INVOCATION` at test `2386-2388`.
  Phase/disp match; only outer code differs, nested `FILE_REPLACED` present.
- O11f root `p3s-p3s-z3hv5lvv` (`root-replace`):
  `STAGED_ROOT_REPLACED/CLAIM/OWNED_PARTIAL`
  `canonical staged entry != earliest mkdir identity before writing main.tex`,
  `fired=1`, `owned_files=1`. Matches test `2422-2424` — field success.
- O11f ancestor `p3s-p3s-ikxe49h3` (`ancestor-replace`):
  `{"ok":false,"error":"StagedSourceError: STAGED_ROOT_ENTRY_FAILED: [CLAIM/OWNED_PARTIAL] canonical staged entry unreadable before writing main.tex: canonical ancestor is symlink: .../fixture-lf-p3s-ancestor-replace/staged-source","code":"STAGED_ROOT_ENTRY_FAILED","phase":"CLAIM","disposition":"OWNED_PARTIAL","fired":1,"owned_files":1,...}`.
  Expected `STAGED_ROOT_REPLACED/CLAIM/OWNED_PARTIAL` at test `2422-2424`.
  Phase/disp match; only code differs.
- O8/O11/O11d raws confirm method success (not subcase-partial):
  O8 materialize `08vqckuz` + 13 verifier raws (`SCHEMA_INVALID`, `PROPOSED_MISMATCH`,
  `STAGED_SET_MISMATCH`, `BASIS_MISMATCH`×2, `PROPOSAL_REF_MISMATCH`,
  `CODE_DEPS_MISMATCH`, `REPLAY_MISMATCH` style/bib, `PIN_UNREADABLE` dup-key,
  `LABEL_MISMATCH`, `STYLE_REF_MISMATCH`, `OUTPUT_PATH_MISMATCH`);
  O11 `51a_33k7 STAGED_ROOT_EXISTS` + `_zcozwnc MATERIALIZED` + `moc3wf0o REPLAY_MISMATCH`;
  O11d `y1mhn3dr REVERIFY_FAILED/PRE_CLAIM` + `cks_g27s REVERIFY_FAILED/MANIFEST`.

## 3. Per-failure root cause (vs wrong oracle vs timing)

### O9 — wrong oracle (field presence vs true). No module defect.
- Test `1683-1685`:
  `self.assertFalse(outcome.get("ok"))` passes (raw `ok:false`, fast refusal, no hang),
  then `self.assertNotIn("timeout", json.dumps(outcome), ...)`.
- But `_run_p3s_fixture` (`tests/...:938-977`) always sets `outcome["timeout"]=False`
  on the non-timeout path (`975-976`) and returns `{"timeout":True,...}` only on
  real timeout/interrupt (`952-959`). Hence `json.dumps(outcome)` always contains
  the substring `"timeout"` (the key name, plus `durable_dir/meta/script/timeout_s`
  fields). The assertion can never pass regardless of behavior.
- Durable evidence shows true no-timeout/no-hang: child `rc=0` (script printed JSON),
  `timeout_s=60`, FIFO refused at `col.safe` lstat (`PATH_NOT_REGULAR`) before any
  open/read, `owned_files=0`. Method success must be judged by
  `outcome.get("timeout")==False` / `outcome.get("timed_out")` fields, not substring.
- Minimal test-only fix: replace `1684-1685` with
  `self.assertFalse(outcome.get("timeout"))` (and optionally
  `self.assertFalse(outcome.get("timed_out", False))` if present),
  keep `LAYOUT_REFUSED/PIN/REFUSED_PRE_WRITE` + regex + fault-present no-write.
  Do not infer ancestor no-write passed — ancestor subcase never ran.

### O10 — no-op mutation (missing change/inode asserts). No module defect.
- Test `1745-1748` opens `main.tex` `r+b`, `seek(0)`, `write(b"%")`.
  O10 uses `_lf_prepare` (Longform) whose `render_main`
  (`scripts/survey_longform_generated_v2.py:293-310`) starts with
  `"% Generated from the reviewed LONGFORM_GENERATED_V1 ..."`.
  First byte is already `%` (0x25), so the write is a byte-identical no-op;
  verifier correctly returns `VERIFIED` (raw `6zh3b33t`). `True is not false`
  at `1754` is honest.
- Test never asserts the mutation is present, nor same-inode identity
  (`_snapshot` records `(file, bytes, size, dev, ino)` per `tests/...:172-174`).
  A no-op cannot reach `REPLAY_MISMATCH`.
- Minimal test-only fix: choose a truly differing first byte and prove it:
  ```python
  first = original[0:1]
  new_first = b"X" if first == b"%" else b"%"
  with main_tex.open("r+b") as handle:
      handle.seek(0); handle.write(new_first); handle.flush()
  snap = _snapshot(root)
  rel = main_tex.relative_to(root).as_posix()
  self.assertNotEqual(snap[rel][1], original, "o10 mutation must change bytes")
  self.assertEqual(snap[rel][3:5], _snapshot_before[rel][3:5], "o10 must keep same inode")
  ```
  (take `_snapshot_before` before the write). Keep expected
  `REPLAY_MISMATCH/REPLAY/INVALID` + fault-present no-write.
  Do not claim the second (same-byte/new-inode) subcase — it never ran.

### O11b — early guard preemption (timing, not intended boundary). No module defect.
- Fault `drift-reader` (`tests/...:684-696`) patches `Path.read_bytes` and fires
  on the FIRST exact proposed-reader read (`fired==0`), appending
  `b"\n% injected mid-call drift\n"` and returning pre-append bytes.
- First exact read occurs during PIN layout (`p1mod._pin_proposal_layout`,
  staged `692-696`), long before intended PRE_WRITE use-check
  (`survey_editorial_staged_source_v2.py:894-904`
  `pinned_staged vs live_staged_now → STABILITY_VIOLATION/PRE_WRITE`).
  Actual `LAYOUT_REFUSED/PIN` with cause `STABILITY_VIOLATION: staged proposed
  reader ...` (P1 `_Collector.safe:177`, label `staged proposed reader` at
  `survey_editorial_correction_proposal_v2.py:1688`, wrapped by staged `695`)
  is an honest early refusal; the later seam is untested.
- Broadening expected code to `LAYOUT_REFUSED` would pretend the final guard
  covered the seam — prohibited by the selection boundary.
- Minimal test-only fix (move injection point, keep seam): defer the drift until
  after layout/prepin/first-P2V pins complete, e.g. wrap the first observation
  return (or fire on a later exact read) so layout + `_prepin_known_live_refs`
  (`342-415`) + PRE_WRITE `_recheck/_compare` (`772-777`) + first P2V (`794`)
  all pass with original bytes, then the `894-904` use-check sees drift:
  keep expected `STABILITY_VIOLATION/PRE_WRITE/REFUSED_PRE_WRITE`,
  add mutation-present assert (`cur[reader_rel][1]` contains drift bytes) and
  fault-present `_assert_no_write_except(base, cur, set(), {reader_rel})`
  as currently written (`2140-2143`). Deterministic alternative to fragile
  read-counting: wrap `observer.observe_current_authority` to append drift
  after the real first observation returns (before `894`), restoring the wrapper
  in `finally` like other fault wrappers.

### O11c — early injection before P2V (timing). No module defect.
- Faults `late-control-add/late-retained-add` wrap `staged._compare_original_boundary`
  and fire on `_compare_calls==1` (`tests/...:723-734`), i.e. the PRE_WRITE compare
  (`survey_editorial_staged_source_v2.py:775-777`, zero admitted delta, before first P2V).
  `late-control-add` creates `scripts/late-control-probe-p3s.txt` (untracked under a
  control path). First P2V (`794-798`) then runs receipt validation which checks
  untracked control sources (`survey_longform_generated_v2.py:561-569`
  `ls-files --others ... → "contains uncommitted source"`, via P1 `1420`
  `RECEIPT_INVALID`) and refuses `OBSERVER_REFUSED/OBSERVE` (raw `pqur_6p_`).
  Intended `ORIGINAL_DRIFT/PRE_CLAIM` (`994-996`, after render) is never reached.
- Accepting `OBSERVER_REFUSED` would pretend P2V dirtiness covers the late
  original-baseline guard — prohibited. Required control/retained additions must
  still test the late guard after later real helpers.
- Minimal test-only fix (move injection after helpers, keep late guard): fire the
  probe creation in `_canonical_wrap` (after first P2V + render, before PRE_CLAIM),
  not in `_compare_wrap` call 1 — mirroring the passing `drift-before-claim` pattern
  (`735-742`). Then PRE_CLAIM `_recheck (991) + _compare (994-996)` sees the probe
  with zero admitted delta and refuses `ORIGINAL_DRIFT/PRE_CLAIM/REFUSED_PRE_WRITE`
  as currently expected (`2244-2246`), with fault-present delta exactly
  `{scripts/late-control-probe-p3s.txt}` / `{.../retained/late-retained-probe-dir}`
  and no staged outputs yet (`2247-2265` unchanged). P2V already passed, so no
  `RECEIPT_INVALID` preemption. Do not claim `late-retained-add` — it never ran.

### O11e samebyte — nested-code mapping (wrong oracle code, right phase). No module defect.
- Wrapper `_verify_wrap` (`tests/...:793-817`) runs real `verify_staged_source`
  then swaps all 4 staged files to new inodes, same bytes.
- Writer FINAL first re-inventories via `_snapshot_originals` → retention snapshot
  helper raises `FILE_REPLACED ... edition file file identity changed:
  .../staged-source-manifest.json`, which staged wraps as outer
  `SNAPSHOT_FAILED` (`survey_editorial_staged_source_v2.py:286-288`;
  also `_compare_original_boundary:319-338` `ORIGINAL_*` family).
  Actual `SNAPSHOT_FAILED/FINAL/INDETERMINATE_INVOCATION` with `FILE_REPLACED`
  in `error` (raw `a2vmymbt`) is the honest nested mapping; the later owned-identity
  check (`1324-1326` `FILE_REPLACED`) is simply not reached because the earlier
  FINAL inventory already refused. Phase/disp match expected; only outer code differs.
- Minimal test-only fix: expect `SNAPSHOT_FAILED/FINAL/INDETERMINATE_INVOCATION`
  plus `assertIn("FILE_REPLACED", error)` for the `post-replay-samebyte-replace`
  subcase only (`2384-2388`), keeping owned-4 + complete-bytes + no-leftover asserts
  (`2390-2398`). Keep first subcase (`post-readback-edit`
  `REPLAY_UNVERIFIED/REPLAY/INDETERMINATE`, raw `wrt4m15c`) unchanged — it is field
  evidence of success, but the method as a whole still fails until the second
  subcase oracle is corrected. Do not infer second-subcase no-write beyond the
  fault-present snapshot actually asserted after the failing line.

### O11f ancestor — entry-type mapping (wrong oracle code, right phase). No module defect.
- `_write_owned_file` canonical-entry check
  (`survey_editorial_staged_source_v2.py:1527-1539`): `lstat` failure →
  `STAGED_ROOT_ENTRY_FAILED` (`1530`); symlink-or-not-dir →
  `STAGED_ROOT_REPLACED` (`1534`); dev/ino mismatch →
  `STAGED_ROOT_REPLACED` (`1538`). Wrapper `_emit_wrap` (`tests/...:743-763`)
  renames the claimed dir after mkdir+earliest pin, then installs either a real
  replacement dir (`root-replace`) or a symlink to `/tmp` (`ancestor-replace`).
- `root-replace` (real dir, different ino) → `STAGED_ROOT_REPLACED` (raw `z3hv5lvv`,
  matches expected — field success). `ancestor-replace` (symlink) fails at the
  `lstat`-reopen path as `STAGED_ROOT_ENTRY_FAILED ... canonical ancestor is
  symlink` (raw `ikxe49h3`), because the canonical entry cannot even be reopened
  as a directory before identity comparison. Both are `CLAIM/OWNED_PARTIAL` with
  `fired=1`, `owned_files=1`, exact deltas as asserted.
- Minimal test-only fix: branch expected code by fault (`2422`):
  `root-replace → STAGED_ROOT_REPLACED`, `ancestor-replace → STAGED_ROOT_ENTRY_FAILED`,
  both `CLAIM/OWNED_PARTIAL`, plus `assertIn("symlink", error)` for ancestor.
  Keep exact-delta + injection-bytes + unchanged-originals asserts (`2426-2440`).
  Do not treat the passing root-replace subcase as method success.

## 4. Helpers read (P1/P2V/P2R)

- P1 `_Collector.safe/pinned` (`survey_editorial_correction_proposal_v2.py:87-189`,
  `STABILITY_VIOLATION:177`, `REF_DRIFT:188`, no `.code` attr: `79-84`),
  `_pin_proposal_layout` (`1641-1707`, staged-reader label `1688`),
  `_validated_state_profile_for_tree` (`1576-1609`).
- Staged PIN order: Session pins (`568-677`) → live Collector+HEAD (`680-691`) →
  layout (`692-696` → `LAYOUT_REFUSED`) → live/retained cross-check → prepin
  (`719-725` → `PIN_FAILED`) → snapshots → PRE_WRITE `_recheck/_compare`
  (`772-777`) → first P2V OBSERVE (`791-798` → `OBSERVER_REFUSED`) →
  reader use-check (`894-909` → `STABILITY_VIOLATION/PRE_WRITE`) →
  PRE_CLAIM `_recheck/_compare` (`991-996` → `ORIGINAL_DRIFT/PRE_CLAIM`) →
  CLAIM (`1009-1096`) → MANIFEST (`1102-1117`) → REPLAY (`1119-1130`) →
  OBSERVE2 (`1131-1140`) → FINAL (`1211-1378`, snapshot nesting `286-288`,
  owned identity `1324-1326`, entry `1527-1539`).
- P2V receipt dirtiness: `survey_longform_generated_v2.py:549-569`
  (`diff --quiet HEAD` + `ls-files --others` over control paths →
  `RECEIPT_INVALID` via P1 `1420`), which is what preempts early O11c.
- `_run_p3s_fixture` timeout contract (`tests/...:938-977`):
  real timeout returns `timeout:True`; non-timeout always sets `timeout:False`
  (`975`) — the O9 substring check contradicts this contract.

## 5. Minimal test-only fixes (exact, no module change)

1. O9 `1684-1685`: `assertNotIn("timeout", json.dumps(outcome))` →
   `assertFalse(outcome.get("timeout"))`. Keep all refusal + no-write asserts.
2. O10 `1744-1758`: pick differing byte (`X` if `original[0:1]==b"%"`), assert
   `snap[rel][1] != original` + same `(dev,ino)` before `assertFalse(ok)`; keep
   `REPLAY_MISMATCH/REPLAY/INVALID`.
3. O11b `fault drift-reader`: defer fire until after layout/prepin/first-P2V
   (wrap first observation return or later exact read); keep
   `STABILITY_VIOLATION/PRE_WRITE/REFUSED_PRE_WRITE` + mutation-present +
   `allowed_changed={reader_rel}`. Never broaden to `LAYOUT_REFUSED`.
4. O11c `late-*-add`: move injection from `_compare_wrap` call-1 to
   `_canonical_wrap` (post-P2V/render, pre-PRE_CLAIM); keep
   `ORIGINAL_DRIFT/PRE_CLAIM/REFUSED_PRE_WRITE` + exact probe deltas.
   Never accept `OBSERVER_REFUSED` as late coverage.
5. O11e `2386`: samebyte-replace expected code `FILE_REPLACED` →
   `SNAPSHOT_FAILED` + `assertIn("FILE_REPLACED", error)`; keep
   `FINAL/INDETERMINATE_INVOCATION` + owned-4/complete-bytes/no-leftover asserts.
6. O11f `2422`: branch by fault — `root-replace: STAGED_ROOT_REPLACED`,
   `ancestor-replace: STAGED_ROOT_ENTRY_FAILED` (+ `assertIn("symlink", error)`);
   keep `CLAIM/OWNED_PARTIAL` + exact deltas for both.

## 6. Blocker classification

- **Actual module defect: none found.** All six actual codes are honest mappings
  at the reached boundary (fast FIFO `PATH_NOT_REGULAR`, byte-identical O10
  `VERIFIED`, early layout `STABILITY_VIOLATION`, dirty-receipt `OBSERVER_REFUSED`,
  nested `SNAPSHOT_FAILED(FILE_REPLACED)`, symlink `STAGED_ROOT_ENTRY_FAILED`).
  No staged/schema change is justified by this batch.
- **Test defects (definite): six oracle/timing gaps above.** Four are pure oracle
  (`O9`, `O10` missing asserts, `O11e` outer code, `O11f` branch); two are injection
  timing that never reaches the selected seam (`O11b`, `O11c`) and need moved
  injection points, not broadened acceptance.
- **Field evidence vs method success:** O8/O11/O11d methods succeeded.
  O9 alias refusal, O11e post-readback refusal, O11f root-replace refusal are
  passing *fields* inside failing methods — never count them as method success.
  No-write asserts after a failed line did not execute and must not be inferred.
  O10-second, O9-ancestor, O11c-retained subcases never ran (no evidence).
