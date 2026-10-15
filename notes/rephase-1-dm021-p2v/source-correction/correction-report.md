# DM021-P2V Co-Worker A source-correction report (R2 fixes, no long run)

2026-10-15 JST. Co-Worker A (shipping source/test). Scope strictly per task:
only selected shipping 2A1M (`scripts/survey_editorial_correction_proposal_v2.py`
private factoring if actual bug, new `survey_editorial_current_authority_v2.py` /
`tests/test_survey_editorial_current_authority_v2.py`) + NEW
`notes/rephase-1-dm021-p2v/source-correction/` docs/evidence. Co-Worker B
tooling under `verification-tools` untouched (dir does not exist; no
edits/runs of old drafts `run_p2v_*.DRAFT` / `proof_apply18_*.DRAFT`).
NO long tests / runtime fixture execution yet (cheap AST parse only).
No candidate branches/commits/network/intake/subagents. No test-pass claim
without run. Generic setup attr probes are type checks only, not behavior.

## 1. Preservation (BEFORE edits)

`preserved-before/` holds byte-identical copies BEFORE this correction:

| File | SHA256 | Bytes | Status |
|---|---|---|---|
| `P1-cdd69fe7.py` (candidate `scripts/survey_editorial_correction_proposal_v2.py`) | `cdd69fe7c24de6dda9ee503cfcfbc791a9d7e421141dbb23586f1e4431c27eab` | 113535 | PRESERVED |
| `observer-79a3396c.py` (candidate `scripts/survey_editorial_current_authority_v2.py`) | `79a3396cf07d85cfeb11df9f85910ba8aed2ed63f965713edab5b076d580d3f4` | 37896 | PRESERVED |
| `test-c7ba6d4a.py` (candidate `tests/test_survey_editorial_current_authority_v2.py`) | `c7ba6d4a4cdde985129b5b5096110a4d839b09f80f15c0d5c68fad2a450be71b` | 32749 | PRESERVED |
| `preserved-expected18-draft.json` (copy of `notes/rephase-1-dm021-p2v/expected18-draft.json`) | `c6bb1fad2ad98048ac5783a381cfe342dbb89ec766118d792d5af6244a227f48` | 3142 | PRESERVED |
| `preserved-implementation-report.md` + `preserved-evidence-corrections.md` | (see `preservation-manifest.json`) | — | Original overclaims preserved as HISTORY, not overwritten |

Candidate at correction time: detached `409b292756dd1277b9dfae87679934c0d2ce251c` /
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status 102 rows
(18 source 3M15A +84 caches). P1 `cdd69`, observer `79a339`, test `c7ba`
match `expected18-draft.json`.

## 2. AFTER pins (this correction)

| Path | Before | After | Change |
|---|---|---|---|
| `scripts/survey_editorial_correction_proposal_v2.py` | `cdd69fe7` 113535B | `cdd69fe7` 113535B | UNCHANGED — no actual bug found; private factoring preserved (see §3) |
| `scripts/survey_editorial_current_authority_v2.py` | `79a3396c` 37896B | `79a3396c` 37896B | UNCHANGED — V1–V5 inspection passes; R2 root fixes already done (see §4) |
| `tests/test_survey_editorial_current_authority_v2.py` | `c7ba6d4a` 32749B | `e00ccddf5c4053cf2a10846cccbaa812d10ff4537849d7fde11a04677a37b5eb` 65422B | CORRECTED per R2 (full diff `test-c7ba-to-e00ccd.diff`, 1105 lines) |

New static18 manifest: `expected18-source-correction.json` in this packet
(17 entries byte-identical to `expected18-draft.json`, only test entry updated
to `e00ccd`/65422). Old manifests (`expected18-draft.json`,
`evidence-20261015T010000Z-r1preservation/preserved-expected18-draft.json`,
P2R `expected16-correction2c.json`) NOT overwritten. Inherited15 (+ P1 +
observer =17) unchanged; 0 schema/P2R/config changes.

Complete diff: `test-c7ba-to-e00ccd.diff` (unified, 1105 lines). No P1/observer
diff (byte-identical).

## 3. P1 inspection (cdd69 preserved, no actual bug)

Read actual `survey_editorial_correction_proposal_v2.py` (1896 lines, AST OK):
- `_retention_rows_for_graph` builds data-only rows+safety with COPY
  `retained_dest` only (no `retained_sha256`/`retained_byte_count`); corrects
  PhaseA125 per selection §3. `_require_retention_dests_absent` is absent-only;
  `_retention_plan` wrapper preserves P1 behavior.
- `_pipeline_data` returns data+`profile` (no acceptance/tree/input_hashes);
  `_pipeline` wrapper adds absent+`reverify`+tree, strips `profile` to preserve
  public shape. Public `prepare_proposal` still structurally calls `_pipeline`.
- `_pin_proposal_layout(col,root,state_path_value,proposal_path_value)` has NO
  caller `profile_validated` arg; inside runs config/proposal pins + schema/id,
  actual `_validated_state_profile_for_tree`, canonical dir/layout/staged/
  description, then tree snapshot; returns bundle (state/cfg/profile/staged/
  tree). Fixes PhaseA96–100.
- `_compare_supplied_to_rederived` compares ALL fields: 7 header keys, basis
  exact, authoring/reader/canonical/description exact, ref-digest consistency,
  P1 retention exact, staged bytes. Public `validate_proposal` is
  layout→`_pipeline`→shared comparison→scope→final receipt→stability; returns
  supplied UNCHANGED + input_hashes/measured intact.
No enum/skip/`verified_set`/caller assertion. No schema change. No actual bug
requiring private-factoring change; P1 left byte-identical.

## 4. Observer inspection (79a339 preserved, V1–V5 pass)

Read actual `survey_editorial_current_authority_v2.py` (614 lines, AST OK).
Cheap grep/AST checks (no execution):

- Signature: `observe_current_authority(root,state_path,proposal_path,
  manifest_path,scope_review_path=None)` — 5 params, no `mode`/`verified_set`/
  `token`/`context`/`dest_policy`/`pending`. `CurrentAuthorityError(code,phase,
  detail,cause)` only; no `owned`, no single-string ctor (test asserts
  TypeError). Docstring `owned` is prose, not attribute.
- V1 fixed completion: `_pin_proposal_layout` without trusted profile arg;
  `_pipeline_data` (data-only) + `_pipeline` wrapper; `_compare_supplied_to_
  rederived` shared; `_validate_scope` + `_final_full_receipt_recheck` retained.
  No `profile_validated` string, no `sorted(` into agreement (0 hits), no
  `int()` coercion (0 hits), no `resolve()` after close (0 hits).
- V2 two stores: live `p1mod._Collector(root_path)` on `session.root_resolved`
  (Session FIRST, symlink root refused); retained/control/edition in
  `retention._Session`; full-tree scans never populate `col.files`
  (snapshots via `retention._snapshot_expanded` in session only). Early narrow
  pins (proposal/manifest/State/config/State-bound Profile/both schemas/scope)
  BEFORE validators; live vs retained ORIGINAL cross-compare; `orig_live_map`/
  `orig_ret_map` preserved; ordered `zip(live_plan,rows)` binding.
- V3 order: sanitized GIT refusal → Session → Collector → sanitized HEAD equality
  → early pins → config cross-check → `_control_paths` → layout (strict authority
  before broad walks) → snapshots → `verify_retention` (#1, SHA vs ORIGINAL pins,
  row/measured checks, COPY/KEEP/staged re-pins, retained inventory vs expected)
  → `_pipeline_data` + supplied comparison + live/retained cross-binding →
  scope (early ORIGINAL vs later loader, live re-pin check) → `_final_full_
  receipt_recheck` AFTER scope → `verify_retention` #2 (SHA stability) →
  `live.reverify` + `session.reverify` → later snapshot/inventory/dep/HEAD reads
  → FINAL ORIGINAL-pin checks + `reverify` again → checked closes
  (`session._close_all`, primary-preserving `_attach_close`) → refs from bound
  rels (`prop_rel`/`man_rel`/`_st_rel`/scope `s_rel`, no resolve). `verify_
  retention` count 2, `reverify` count 5. No resnapshot laundering.
- V4 types: P2R SHAs must be str, `checked.copy_files`/`keep_refs` non-neg ints,
  graph nodes/edges lists, plan list, ref `{path,64-hex}`, basis digests non-empty
  str, `proposed_canonical` bytes, `INPUT_HASH_CONFLICT` on merge, no producer-
  extras blanket check (§4.7). `RESULT_NEEDS_SCOPE` vs `RESULT_SCOPE_BOUND` only;
  invalid scope refuses. HEAD 40-hex via sanitized equality.
- V5 fixture binding: tests (not observer) commit changed P1+new2 BEFORE authority
  with `.github` included and execute fixture code where R1 modifies basis.
No folded path aliases (all reads via `safe_read`/`safe` with no-follow,
O_NONBLOCK, lstat type checks). No token/pending/bearer/creator/anti-rollback.
Conclusion: observer 79a339 already implements R1 §2 + selection V1–V5;
no logic change in this correction. Remaining R2 work is tests-only.

## 5. Test R2 fixes (c7ba → e00ccd, 545 → 1096 lines, 13 methods preserved)

All positive fixtures use `_make_p2v_source_root` (tracked incl. `.github` +
15 untracked P1/new2, byte-hash verified, committed BEFORE authority with
meaningful message, clean status, no user identity). All behavioral methods call
actual `observe_current_authority`/`prepare_proposal`/`validate_proposal`/
`capture_retention`/`verify_retention`/scope review and assert expected semantic
result/error + immediate no-write/injected-only delta BEFORE repair. Real P1/P2R
recipes only; no invented helper attributes in code (`_build_validated`,
`frontmatter.lede`, `_commit_derivation_only_change` for R1, `_FIXTURE_CASCADE`
for R1: 0 code hits; `_build_validated` appears only in this report's prose).

| Method / subcase | Actual helper / injection point | Fix vs c7ba |
|---|---|---|
| `test_public_api_has_no_caller_token` (probe) | `inspect.signature(observe_current_authority)` | Unchanged (type probe, not behavior) |
| `test_error_shape_no_owned` (probe) | `CurrentAuthorityError(code,phase,detail)` | + single-string ctor TypeError regression guard; `owned` attr absent |
| `_build_weekly_pair` (shared) | `p1t._new_weekly_helper`, `p1t._build_weekly_validated`, `p1t._stage_authoring_before_prepare`, `p1mod.prepare_proposal`, `p1t._stage_reader_and_proposal`, `p1mod.validate_proposal` (REVIEW_REQUIRED), `retention.capture_retention` (RETAINED_SET_CAPTURED) + `p1t._snapshot`/`_assert_no_write` each step | + capture no-extra-writes check; manifest via `cap["manifest_path"]` |
| `test_longform_observe_needs_scope` | `p1t._new_longform_helper` → `helper._complete(helper._chain())` → `helper._state_path(chain)` → `helper._advance_to_validated_draft` → `helper._authored(chain,helper.worker)` + `longform_revision.packages[0].narrative_sections[0].paragraphs[0].text` delta → stage/prepare/validate/capture/observe | REPLACED invented `helper._build_validated()` + `frontmatter.lede` with actual recipe; asserts proposal/manifest/State SHAs + `proposed_reader_sha256` + full no-write |
| `test_weekly_observe_scope_bound_after_capture` | `p1t._scope_review_for` ordinary (block popped + `EDITORIAL_CORRECTION_SCOPE` check removed + sha recomputed) → NEEDS_SCOPE; valid after-capture outside `retained/` → SCOPE_BOUND; REJECT → `SCOPE_NOT_WITHIN_AUTHORITY` | FIXED ordinary check removal (was leaving scope check); exact REJECT code; full no-write each |
| `test_p1_baseline_and_postcapture_refusal` | `p1mod.prepare_proposal` + `validate_proposal` after capture | Now asserts exact `RETENTION_DEST_CONFLICT` (was generic `ProposalError`) + full no-write each; observer NEEDS_SCOPE still |
| `test_mutable_persistence_positive_current_negative` | `proposal.basis.generated_receipt_ref` asserted COPY policy; `retention.verify_retention` (VERIFIED) vs `observe` (refuse) | + COPY-policy meaningfulness assert; full files+special+head+status no-write (was files+head only) |
| `test_keep_drift_refuses_both` | KEEP row `retained_ref` mutation; `verify_retention` (RetentionError) + `observe` (CurrentAuthorityError) | Full `_assert_no_write` BEFORE repair (was files-only); positive again after repair |
| `test_r1_active_owner_and_stale_refuses` | Non-emitted `# R1 non-emitted fixture comment` in `survey_weekly_derivation_v2.py` + commit; `_R1_SAMEBYTE_SCRIPT` (fixture-code `weekly.load_derivation` sha vs `before_surface`); `_R1_REFRESH_SCRIPT` (fixture-code `r1.refresh_mechanical_evidence`); `_R1_PREPARE_CASCADE` (fixture-code prepare+stage+validate, ACTIVE origin); `capture_retention`; `_P2V_OBSERVE_CASCADE` (fixture-code observe NEEDS_SCOPE); second comment+refresh → `agent.resolve_active_publication_revalidation` supersedes; stale observe via cascade → `BASIS_MISMATCH` | REPLACED emitted-TeX `_commit_derivation_only_change` + generic `_FIXTURE_CASCADE` with genuine R1 owner + fixture-code execution (avoids import mismatch); ADDED named stale-active negative (was absent); deleted unused `_prepare_via_fixture` |
| `test_real_control_change_and_artifact_head` | Real `cfg["contract_files"]["pipeline"][0]` bytes +`\n` → observe refuses; `docs/p2v-artifact-note.md` commit → conditional artifact-HEAD accept | Full no-write (was files-only); real control file (not synthetic string) preserved |
| `test_retained_missing_extra_empty_dir` | Missing COPY unlink → RetentionError + `CurrentAuthorityError`; extra `retained/late-file.json` → `INVALID_RETENTION`; `retained/before/empty-dir` → `INVALID_RETENTION` | All three now full snapshots BEFORE restoration (extra/empty-dir had none) + exact `INVALID_RETENTION` + repair restores |
| `test_alias_fifo_no_read_and_late_addition` | (a) `proposal/alias-leaf.json` symlink → `PATH_ALIAS\|TREE_ALIAS\|PROPOSAL_LAYOUT` via `_observe_with_timeout`; (b) `proposal/fifo-probe` mkfifo → explicit `os.open` leaf tracking (FIFO never opened) + 30s timeout + special-inventory assert + full no-write; (c) mid-call seams via `mock.patch.object(p1mod._final_full_receipt_recheck)` wrapper (fires once after real call, before second verify/final): control `config/late-control-midcall.json` → `CONTROL_DRIFT`; edition `src/empty-midcall-dir` → `EDITION_DRIFT` (files + special checks); retained `midcall-retained-extra.json` → `INVALID_RETENTION`; KEEP bytes +`\n` → `PIN_DRIFT\|STABILITY_VIOLATION\|REF_DRIFT\|COPY_DRIFT`; scope mutation via `mock.patch.object(p1mod._pin_proposal_layout)` wrapper → `SCOPE_DRIFT\|SCOPE_BYTES_SWITCHED\|SCOPE_DIGEST` | REPLACED pre-observe-only late file (which tested existing refusal) with actual mid-call injections before known final checks; exact codes + injected-only deltas BEFORE repair (files diff exactly injected, head unchanged); FIFO now timeout + no-read proof + explicit setup fail; alias now timeout + full no-write |
| `test_scope_invalid_matrix` | Observer with scope files: malformed → `SCOPE_UNREADABLE`; non-PASS (decision FAIL, rehashed) → `SCOPE_ORDINARY_INVALID`; wrong-before → `SCOPE_WRONG_BEFORE`; wrong-after (before-reader rel) → `SCOPE_ORDINARY_INVALID\|SCOPE_WRONG_AFTER\|SCOPE_DIGEST`; stale-upstream (`f`*64) → `SCOPE_STALE_UPSTREAM`; REJECT/REQUIRES_OWNER → `SCOPE_NOT_WITHIN_AUTHORITY`; empty `change_summary`/`evidence_locations` (rehashed) → `SCOPE_BLOCK_SHAPE`; scope check FAIL (rehashed) → `SCOPE_CHECK_NOT_PASS\|SCOPE_ORDINARY_INVALID`; tamper without rehash → `SCOPE_DIGEST_MISMATCH`; shared `p1mod._compare_supplied_to_rederived` on real `prepared` (header/basis/retention/bytes) → `HEADER_MISMATCH`/`BASIS_MISMATCH`/`RETENTION_MISMATCH`/`PROPOSED_BYTES_MISMATCH` with full no-write | COMPLETED non-PASS/wrong-after/upstream/substance + comparator refusals (were missing); exact codes + full no-write each (was partial matrix, generic codes) |
| `test_close_fault_and_no_write` | Success + `/proc/self/fd` leak check; (a) success-path CLOSE_FAILED via armed `mock.patch.object(p1mod._final_full_receipt_recheck)` (sets flag after real call) + `mock.patch.object(retention.os,"close",side_effect=real_close-then-raise)` (only when armed) → `CLOSE_FAILED`, fd sets equal (no leak), success again; (b) primary+secondary via KEEP mid-call inject (PIN_DRIFT primary) + armed close fail → primary `PIN_DRIFT` preserved, `err.code != CLOSE_FAILED`, `secondary closes` in detail, fd sets equal; final success | REPLACED global early `os.close` mock (which failed every close from entry, leaked fds) with precise final/session-boundary faults; real fd closed before simulated error (no leaks); proves primary preserved; DELETED no-op `real_close(...).__class__` + `os.close(999999)` lines; no test-only production switch |

Method counts: 13 test methods (2 probes + 11 behavioral, all behavioral call
`observe_current_authority`; R1 positive + stale via fixture-code cascade
`_P2V_OBSERVE_CASCADE` to bind to committed R1 basis). Subcase counts follow
actual matrix above, not target13.

## 6. Readable extraction invariants (P1 private factoring + observer)

P1 data-only factoring (cdd69, preserved):
- `_retention_rows_for_graph(graph,proposal_dir)` → rows with `roles/path/sha256/
  byte_count/policy` + `retained_dest` (COPY) or `retained_ref={path,sha256}`
  (KEEP); common alias/namespace safety; NO absence verdict, NO measured
  `retained_sha256`/`retained_byte_count`, NO readiness.
- `_require_retention_dests_absent(col,rows)` → absent-only (`RETENTION_DEST_
  CONFLICT` if COPY dest exists/symlink).
- `_retention_plan = rows + absent` (fixed P1 wrapper; public success still
  requires absence).
- `_pipeline_data(col,root,state_path,authored,pid,desc)` → `{proposal,
  before_canonical, proposed_canonical, graph, frozen, effective, ...}` + `profile`;
  NO acceptance/tree/input_hashes/readiness.
- `_pipeline = data + absent + reverify + tree` (fixed wrapper; strips `profile`).
- `_pin_proposal_layout(col,root,state_path,proposal_path)` → `{proposal,
  proposal_id, expected_dir, observed_dir_rel, staged_authored, staged_reader,
  tree_entry, state, cfg, profile}`; strict State/Profile/canonical guard BEFORE
  broad walks; no caller profile arg.
- `_compare_supplied_to_rederived(supplied,rederived,staged_bytes,canon)` →
  void or `HEADER/BASIS/PROPOSED_*/RETENTION_MISMATCH`; ordered list equality
  (no sorting into agreement).
- Public `prepare_proposal` calls `_pipeline` structurally; public
  `validate_proposal` is layout→`_pipeline`→shared comparison→scope→final FULL
  receipt→stability; returns supplied UNCHANGED. Moving code need not preserve
  diagnostic order for simultaneous invalids; all success/refusal invariants +
  normal result fields preserved.

Observer separation (79a339, preserved):
- Live `_Collector` (planner inputs incl. staged proposal) vs retained/control/
  edition `_Session` (+ final hash union with conflict refusal). Full-tree scans
  never populate `col.files`. Shared-path ORIGINALs cross-compared; later reopens
  compared to ORIGINAL pins; no laundering; no `verified_set`/token/pending/
  State forge/cleanup/creator/bearer claims.
- Order: narrow pins → strict live authority before broad walks → control/edition/
  retained snapshots → same-invocation P2R + row re-pins + inventory → live
  derivation/comparison/cross-binding (ordered) → optional scope → FULL receipt
  AFTER scope → second P2R → final ORIGINAL + control/edition/retained/HEAD/
  schema/module checks + checked closes. Late additions detected by full
  inventories, not known-file rehash alone. `input_hashes` union rejects conflicts.

## 7. Cheap checks only (no long run, no fixture execution)

- `ast.parse` candidate P1 (1896 lines), observer (614 lines), new test (1096
  lines, 13 tests): OK. P1/observer AST unchanged; test AST OK with 0 invented
  code hits (`_build_validated` 0 excl. prose, `frontmatter.lede` 0,
  `_commit_derivation_only_change` 0, `_FIXTURE_CASCADE` 0).
- No `py_compile`/collection/test/proof execution in this correction (avoids
  bytecode writes; candidate status remains 102 rows). New pins are static
  file hashes (above), not runtime PASS.
- No historical scripts rerun, no old25/36 transfer, no subagents, no
  `verification-tools` edits, no candidate commit/push/network/intake.

## 8. STOP — await root + runner approval before long run

No long fixture/test/proof started. Next requires root readback/selection of
this source-correction (actual diff `test-c7ba-to-e00ccd.diff`, pins
`preservation-manifest.json` + `expected18-source-correction.json`, method table
§5, invariants §6) AND Co-Worker B runner/proof approval. Whole NOT_READY,
step4/B3 OPEN, audit unstarted, DM021 OPEN. Ordinary Commit/Push Human-owned.

Original report overclaims (runner/proof v1 print-only, both-100, sample-inode,
`py_compile` no-write, transient collection as packet) remain visible in
`preserved-before/preserved-implementation-report.md` +
`preserved-evidence-corrections.md` as history; this correction annotates by
preservation + exact R2 fixes, does not overwrite or claim green runs.
