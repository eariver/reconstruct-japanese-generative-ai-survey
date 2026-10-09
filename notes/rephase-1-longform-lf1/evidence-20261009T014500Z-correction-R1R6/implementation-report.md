# LF-1 correction implementation report (R1–R6 + additional, SAME 3 paths)

2026-10-09. New correction Co-Worker (not independent reviewer). Source overlay
remains uncommitted on fixed HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, in
`/tmp/opencode/jgas-lf1-design-20261009T001653Z`. No candidate commit/branch,
no reconstruct/source/restore edits except this new packet
`notes/rephase-1-longform-lf1/evidence-20261009T014500Z-correction-R1R6/`.
Source original `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` unchanged at
409, clean. Earlier `evidence-20261009T003443Z/overlay.patch`, `run-focused.sh`
and logs are preserved untouched (MUST NOT overwrite). STOP for Astra and
separate implementation review. Whole candidate NOT_READY, step4/B3 OPEN,
canonical audit unstarted. No shipping/committed-head PASS.

## 1. Final overlay (SAME 3 new paths only)

- `scripts/survey_longform_derivation_v2.py`
  `abd50864e5065d7d69a6c3ccc13d01915be4654aee4aedeac1eb60f9aa33987f`
- `schemas/longform-reader-input-v2.schema.json` (unchanged bytes)
  `71156a53b776a82928519b0a3f821cf40bd4279550e0bc4973c7ed27394e588b`
- `tests/test_survey_longform_derivation_v2.py`
  `d4ab5361c7741d10dbe5986bf1f62b85a21646a8e220641469e6395389ba2ca6`
- Patch `overlay.patch` (standard `a/<path>` `b/<path>`, new-file, vs 409),
  `overlay-sha256.txt`, `overlay-head.txt`, `overlay-tree.txt` in this packet.
- `git status` in DST is exactly the three `??` lines above;
  `git diff --name-only HEAD` is empty. No shared-helper/schema/config/Weekly,
  CLI, renderer/Gate/writer, contract changes. New dependency is read-only
  `survey_reader_surface_gate_v2` (no writer import/invocation).

## 2. R1 — fail-closed runner (new, old script not reused)

New `run-corrected.sh` (not old `run-focused.sh`): absent-log-only, pinned
HEAD/tree/three hashes/three-path exact predicate, zero tracked mods, all six
`GIT_DIR/WORK_TREE/INDEX_FILE/OBJECT_DIRECTORY/ALTERNATE_OBJECT_DIRECTORIES/
COMMON_DIR` checked, interpreter/version/caller-cwd/child-cwd/argv/filtered
env/inert origin/file-protocol recorded, child runs from pinned copy
(`cd "$DST"`), numeric child exit retained, finally postguard runs without
masking (`exit $CHILD_EXIT`), exclusive log, `PYTHONDONTWRITEBYTECODE=1`,
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`.

Proofs in this packet:

- `proof-wrong-head-shell.log`: `PIN_OVERRIDE_FOR_PROOF=deadbeef…` causes
  `REFUSE: HEAD mismatch … (child not executed)`, shell exit 2, inner child
  log absent (no sentinel). Proves wrong expected source/HEAD refuses before
  child execution.
- `proof-failing-child.log` (final hash): nonexistent unittest causes
  `FAILED (errors=1)`, `unittest_exit:1`, postguard still runs,
  `CHILD_FAILED exit=1 (propagated, not masked)`, shell exit 1. Proves failing
  child returns nonzero with postguard. Superseded proofs with older hashes are
  preserved as `proof-failing-child-superseded-*.log`.

## 3. R2 — archive authorization (module + tests)

`_validate_archive_authorization` added and called after per-package drift
checks: archive packages exactly once each vs Architecture (no
extra/duplicate/missing, length + set equality), spec blocks exactly once each
vs Result non-`CLAIM_BOUNDARY` blocks (unique + set equality with
archive-only/result-only diagnostics), and EVERY assigned DID validated via
accepted `citation_refs.refs(package, ids, mode)` exact-one semantics for deck
+ each spec block (archive-only cross-package DID refuses). `spec_by_id`
duplicate package and per-package duplicate block checks added in loader.

Tests `test_archive_exact_coverage_and_selected_only` on ONE reusable
two-package chain: healthy control passes, then five file mutations (each
written BEFORE before-snapshot, snapshot immediately around derive before
archive repair, repair disclosed via `addCleanup`+explicit restore):
extra/duplicate archive package, extra/duplicate block, cross-package
archive-only DID (`pkg-001` gains `DID2`). Each refuses with
`coverage differs|duplicates|exactly once inside package`. Post-repair healthy
control passes again. `run-archive-superseded-3983.log` is stale (old hash);
final proof is `run-final-batch.log` (archive case inside batch) on final hash.

## 4. R3 — full category/controls (table-driven, reusable chain)

`test_table_every_category_mutation_reuses_single_chain` builds ONE single-DID
accepted chain, baselines via real loader, then 21 authored variants (each file
written BEFORE before-snapshot, snapshot immediately around derive):
cover/headline/deck, frontmatter lede, final-summary para, glance text,
narrative heading, timeline label, synthesis heading, boundary text,
note chronology/point/limitation, cross heading/dimension/GLM all prove
`changes` (reader bytes differ); scanner/forbidden/DID-leak, missing note,
unknown DID, bad final heading prove `refuses` with intended patterns.
No chain rebuild per field. `run-table-superseded-*-fail.log` preserve two
pattern fixes (DID scanner message, missing-note empty-list message).

Additional R3 negatives in `test_unsupported_inputs_refuse_reusing_single_chain`
(ONE chain, spy-captured `ordered` in a single derive, then pure builds):
unsupported research/publication profile, altered synthesis issue, tampered
synthesis shape, DID/kicker token refusals, dotted-key preservation.
`test_held_back_cite_refuses_at_projection` proves direct loader-level
held-back refusal (mutated `records` HOLD refuses with `held-back`); the older
`NEEDS_MORE` fixture `AssertionError BLOCKED` is explicitly labelled upstream
readiness evidence only, not a loader negative.
`test_citation_collision_refuses_end_to_end` builds colliding DIDs
(`fixture-paper-D001` vs `fixturepaper-D001`, same `_bib_key`) and proves
`citation key collision` end-to-end. Superseded bibkey expectation preserved.

## 5. R4 — runner metadata nonreader

Module: `REQUIRED_RUNNER` removed; authored `runner` requires only non-empty
string (modest envelope/type policy). Profile defines THEMATIC/LONGFORM_SPECIAL;
any non-empty runner projects identically. Reader schema already carries no
runner/provenance (unchanged). `visible_text` uses `copy.deepcopy`.

Tests `test_runner_and_review_reference_are_nonreader` (ONE chain):
runner-only change retains reader bytes with differing `authored_refs`;
empty runner refuses as type policy; review-reference-only change retains bytes;
surface contains no `runner`/`review_reference`/`provenance`/`recorded_at`.
This explicitly corrects the first `test_runner_mismatch_refuses` claim
(`runner must be LONGFORM_SPECIAL`); that refusal was a false authority
assumption and is retracted. Old 25-test transfer is NOT claimed.

## 6. R5 — scoped full no-write oracles

`_snapshot` replaces file-only `_inventory` (legacy `_inventory` retained as
file-view): regular-file SHA, directory identity, symlink targets, plus Git
`HEAD`/`status`/`diff` with exits. `.git` file walk is explicitly scoped out;
Git state is observed via plumbing. Helper `_derive_checked` /
`_derive_checked_refuses` snapshot immediately around derivation; mutations are
always on disk BEFORE before-snapshot; comparison precedes any repair/cleanup.
No absent-filenames-only substitute: `test_no_writer_artifacts_or_gate_created`
compares full snapshots plus edition-root writer-name sets before/after.
All new table/archive/held-back/tamper/collision paths assert snapshots around
both passing and refusing derivations. `.git/index` cause speculation is NOT
retained as fact; same-device inode claims are bounded file/symlink/dir/Git
observations, not full-filesystem proof. Superseded narrow-oracle code is
preserved in the old packet.

## 7. R6 — scanner + selected-only eligibility

Scanner: `_reader_text` now calls read-only
`surface_gate.scan_reader_text_lines([text], label, "longform-revision")` and
refuses `BLOCKING/UNRESOLVED` before preserved forbidden/Verify/DID/TeX checks.
No writer import. `test_pure_policy_boundaries_without_chain` (no chain, fast)
proves scanner blocks `approved architecture` (absent from local list) plus
preserved local refusals, exact URL reject set, primary missing/duplicate,
constants isolation, dotted-key grammar, card-filename traversal,
`validate_*` escape. Table scanner row proves end-to-end loader refusal.

Selected-only: `_longform_records(..., selected_ids)` validates container/card
integrity globally (duplicate DID, card SHA with pre-read `_safe_card_path`,
single-DID, Matrix/Materiality/Discovery mismatch, card presence) for EVERY
Matrix row, then resolves primary/URL/provenance + VERIFIED/PARTIAL/non-HOLD
only for `selected_ids` (union of Draft-assigned DIDs). Unselected
HOLD/ambiguous rows are absent from `records` (preserved without promotion,
never block); citing them later refuses via `missing from accepted`
/`held-back`. `missing = selected - records` fails closed if an assigned DID
has no eligible record. Archive test proves `selected={DID1}` yields only DID1
and `selected={DID1,DID2}` yields both on real files. No success mocks; real
loaders/producers/checkpoint typed approval throughout. If producers cannot
yield an unselected-HOLD chain, the narrower reachable scope (unselected
VERIFIED skip) is disclosed here; no invented eligibility.

## 8. Additional corrections (same 3-file budget)

- Exact URL before trim: `_resolve_primary_entity` calls `_check_url(raw_url)`
  on the untrimmed accepted URL; surrounding whitespace refuses, never
  normalizes. Pure tests prove `" https://…"` refuses and missing/duplicate
  primary refuses.
- Mutable constants: `copy.deepcopy(VISIBLE_TEXT)`; pure test mutates one
  surface header and proves `VISIBLE_TEXT` unchanged. Unused
  `survey_draft_profile_v2` import removed; stray `URL616-style` wording
  removed (now `exact unsupported-URL issue`); `_CITATION_KEY` aligned to
  `^[A-Za-z][A-Za-z0-9:._-]*$` (dots preserved per DID subset).
- Pre-read path safety: `_safe_card_path` validates plain-basename filename
  under `results/` BEFORE SHA/read, plus `_safe` containment/symlink/file
  checks and `results/`-relative enforcement; `_artifact` re-checks.
  `validate_longform_reader_input(Path)` calls `_safe` before read. Pure tests
  prove `../evil`, `a/b`, empty, absolute, backslash refuse and outside
  `validate_*` path refuses.
- Process-scoped fixture identity: `setUp` uses `-c user.name/email` +
  `GIT_AUTHOR/COMMITTER_*` env, no persistent `git config user.*`; asserts
  `git config --local --list` lacks `user.*` (global operator identity is out
  of scope; first global-config failure preserved as
  `run-pure-superseded-globalconfig-fail.log`).
- A3/metadata driver: `_complete_authorities`/`_chain` preserve acceptance
  (real producers, stage checks, typed Architecture approval, historical-basis
  override); no fabricated passing states, no helper-success mocks, no
  invisible repair (archive restore disclosed, snapshots precede repair).

## 9. Test evidence (appropriate only, no old transfer)

Final composite identity is module `abd5086…`, schema `71156a5…`, test
`d4ab536…`, HEAD `409b292…`, tree `8ce3699…`. All final logs in this packet
record pinned identity, interpreter/version/cwd/argv/env, file-protocol
runtime, pre/post guards, numeric exits.

- `run-final-batch.log`: 6 tests OK in 562.904s (pure, valid-single,
  table-21, archive+selected-only, runner-nonreader, collision) via new
  runner, exit 0, postguard clean.
- `run-unsupported.log`, `run-heldback.log`, `run-tamper.log`: each 1 test OK
  (~64–73s), exit 0, postguard clean.
- `proof-failing-child.log` + `proof-wrong-head-shell.log`: guard proofs
  above, exits 1 and 2.
- Superseded development failures preserved untouched:
  `run-pure-superseded-*-fail.log` (globalconfig, verify-pattern,
  did-scanner, entities-msg), `run-valid-superseded-archive-keyerror-fail.log`,
  `run-table-superseded-*-fail.log`, `run-unsupported-superseded-bibkey-fail.log`,
  plus stale-hash passes (`*-superseded-3983.log`, `*-superseded-77c47.log`,
  `*-superseded-60188e.log`, `*-superseded-ca2fe.log`). Do NOT claim old 25
  (old 20 + 5 regression) transfer; final claim is 6-batch + 3 singles = 9
  meaningful methods on final identity plus 2 guard proofs. Existing full
  first code bytes remain in `evidence-20261009T003443Z/overlay.patch`.

## 10. Corrected first claims (explicit retraction)

Preserve original evidence; correct honestly:

- `implementation-report.md:8–9,65,91` and return claims of strict/asserting
  guards in `run-focused.sh` are FALSE. Old runner printed identities/hashes
  but never compared expected values, never asserted three-path/HEAD/tree/clean
  baseline, checked only a subset of overrides, omitted runtime/cwd/argv,
  masked unittest failures with later echo, overwrote LOG paths. Retracted;
  replaced by `run-corrected.sh` proofs above.
- `test_runner_mismatch_refuses` (`runner must be LONGFORM_SPECIAL`) was a
  false authority assumption; runner is nonreader envelope. Retracted and
  replaced by nonreader stability proof.
- `_inventory`-only no-write and central-positive-only assertions were narrower
  than claimed; replaced by scoped `_snapshot` around each selected
  positive/negative before repair.
- `NEEDS_MORE` fixture `AssertionError BLOCKED` was mislabelled as a direct
  loader negative; it is upstream readiness evidence only. Direct held-back
  refusal is proved separately.
- Archive extra/duplicate/cross-package coverage, scanner obligation,
  selected-only eligibility, exact untrimmed URL, constants isolation,
  pre-read card safety and `validate_*` containment were missing/weakened;
  corrected above. No silent weakening: where producers block an unselected-HOLD
  chain, the narrower scope is disclosed, not invented.

## 11. Packaging and independent apply verification

`overlay-sha256.txt/head/tree/patch` in this packet are final bytes.
Independent offline verification without refs/commit: fresh byte-copy
`/tmp/opencode/jgas-lf1-verify-20261009T120000Z` from original 409 via `cp -a`
(HEAD/tree verified, inert origin, no `alternates`, zero multi-link objects),
`git apply --check` exit 0, `git apply` exit 0, post-apply status exactly three
`??` lines, zero tracked mods, three SHA256 match final overlay (path prefix
differs only by directory). No test repeat for packaging. See
`verify-apply.log`. Verify copy is disposable; durable content is this packet
plus DST overlay.

## 12. Limits and STOP

No LF-2/renderer/Gate/writer/CLI/contract/config changes. No
candidate/reconstruct commit/branch. Tests create only independent synthetic
Git DBs/commits with process-scoped identity. If any root requirement conflicts
with actual source, exact issue is returned above; no silent weakening.
Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted. STOP for
Astra and separate author-independent implementation review.
