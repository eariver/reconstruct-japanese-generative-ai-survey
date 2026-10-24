# Phase-H history-derivation fix worklog — NONEMPTY editorial bindings + lineage (append-only)

2026-10-24. Fresh AUTHOR replacement for failed provider ses_e95f4071effeJNj8uuqqERlI6w
(response.failed server_error sequence44 on last binding task). Root `ps -eo` rechecked
20261024T040536Z: NO related live test/build child (only own grep); do NOT duplicate any run
without checking. Scope ONLY history derivation integration; no candidate/reconstruct
commits/network/old runner/clean/reset/source outside owned H file. Writable candidate
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
actual409+57+partial H/S. Read AGENTS latest contract/root 7d7d5a45 INCLUDING §6. Whole unit
ongoing implementation not ready; no HumanCommitPoint from partial return. Rejected M1 preserved
`.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work` NOT source.
Current H file 1895 lines after fix (was 1602 after real-bootstrap-20261024T120000Z correction).
Real baseline public activated old R3 fixtures READONLY
`.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly`
& `bootstrap-longform` HEAD 721a04d old721source real 5page PDF/P1P2RP2VP3S/finalize+activate;
fresh independent copies only for tests (this run historyfix-20261024T041000Z).

## 1. BLOCKER fixed (H-owned, preserve legacy/schema)

Prior H `verify_versioned_history` returned `observed_source_bindings==[]` for real editorial old
format; source S therefore cannot build valid T epoch/O17 proof. This is NOT correct selected
contract despite author claim. Fixed by deriving NONEMPTY complete observed bindings from ACTUAL
strict owner docs/record/staged/receipt including each schema owner O1-O7+O17 (editorial subset;
renewal O10-O16/O7/O4-renewal/O5-renewal pending high lifecycle).

Format exact root precode R5: `{source_ref:{path,sha256}, binding:
RECEIPT_CURRENT_TOOLS|STAGED_PRODUCER|SCHEMA, repository_commit_sha:40hex, SCHEMAONLY
schema_path/schema_pointer/schema_sha256}`. E docs live/COPY (never require tool commit), tool rows
& schemas at DERIVED own commit mandatory. Compute expectations from actual
`receipt.current_tools.commit`, `staged.producer_head` and typed owner registry; never from
serialized observed rows/caller epochs. Return canonical sorted dedup by full owner/path/epoch;
same path different generations allowed iff distinct source owners. Preserve all original scope
before/after/upstream/required checks; O17 whole schema `""` not `"/"`.

Changes in `scripts/survey_versioned_renewal_history_v2.py` (dedicated editor, no apply_patch tool;
`Edit` exact replacements, `Read` before each):

- `_check_observed_binding_row` tool rows now enforce actual doc epoch field equality
  (RECEIPT `current_tools.commit`, STAGED `producer_head` == row epoch, else `HISTORY_TOOL_EPOCH_DRIFT`),
  not just commit-exists. Prevents caller epoch authority; preserves E live/COPY (no tool-commit
  requirement for E bytes) and T/schema blob+mode at derived epoch via `git show`/`ls-tree`.
- New `_derive_editorial_observed_bindings` (called after `_verify_editorial_ancestor` passes,
  rereads with same history loader, never dict permit): 2 tool rows (RECEIPT/STAGED at derived own
  commit) + 7 SCHEMA rows (O1 proposal, O2 retention, O3 staged, O4 receipt-editorial, O5 seal-editorial,
  O6 build-old, O17 scope `""`) + optional P specs (`manuscript-spec.json`, `toolchain-spec.json` at
  conventional P dir iff present live; real R3 has both → 11 rows total, synthetic unit without specs
  still NONEMPTY 9 rows). Each validated via strict checker (epoch/owner/pointer/blob/mode, O17 `""`
  enforced, `/` refused). Canonical sorted dedup with conflicting-sha refusal; required O17+RECEIPT+STAGED
  coverage (no subset/empty shortcut). Scope equality staged==receipt enforced (R6 B.2); proposal
  staged==seal re-checked; retention staged==receipt where present.
- `verify_versioned_history` now accumulates editorial derived (was `[]` skip) + lineage
  (`materialization_lineage` per ancestor: original proposal/staged/scope/retention/receipt/seal/build
  refs + `staged_producer_head`/`receipt_epoch`; versioned: `prior_selected`/`basis`/`proof` +
  `basis_current_epoch`; LEGACY: path/sha/kind). Versioned collection remains narrow (submitted basis
  observed already verified exact, plus lineage for S C→U→U reachability); full expected==submitted
  completeness pending high lifecycle — explicitly narrow unit, NOT endtoend. Dedup now groups by
  (path,binding,schema,pointer,epoch) without sha, refusing conflicting sha (`HISTORY_DIGEST_MISMATCH`);
  same path different owners/epochs allowed. Empty for active chain refuses (must be NONEMPTY).
- Preserved: E-staged NOT required at tool commit (style trio explicitly NOT checked at epoch),
  live before-State NOT validated (retained COPY only), skipped scope/proposal now required,
  len15 exact (missing/extra lists), closure exact membership (name==path, set/order/blob/mode),
  no swallowed errors, pass order. Low `_is_versioned_record`/`_is_versioned_seal` + legacy/schema shapes
  unchanged from real-bootstrap blocker fix.

Interface for S/high in `../integration-interface.md` (exact return fields/semantics, descriptive not
permit, S rereads via loader, C→U→U stored-producer-older-ancestor rule, S scope-row incompatibility
noted for S worker, no S/high edits here).

## 2. NEW independent DBs (fixture commits only, no candidate/reconstruct commits)

- Parent: `.rephase-1-editorial-runtime/versioned-renewal-historyfix-20261024T041000Z/`
- Weekly-new + Longform-new via `cp -a` (no `-l/--link`, no hardlinks): dev:ino disjoint
  (orig 21628504 vs new 21645933 weekly worktree; inodes 21630317 vs 21653318, nlink==1 both),
  no `objects/info/alternates`, inert origins
  `https://example.invalid/versioned-renewal-historyfix-weekly-new.git`
  (and longform-new), no `GIT_*` env, `git status` clean except ?? old E (10 weekly/12 longform untracked),
  HEAD same 721a04d, `ls-files` 721 pre-overlay.
- Overlay ONLY coherent current intended source (9 H/S + low files, byte-identical from candidate-work):
  `scripts/survey_publication_set_v2.py`, `scripts/survey_agent_control_v2.py`,
  `scripts/survey_versioned_renewal_history_v2.py` (fixed, 1895 lines, sha f14cf9e…),
  `scripts/survey_versioned_renewal_source_v2.py`, `schemas/versioned-renewal-*.json` (4),
  `schemas/publication-surface-revalidation.schema.json`. No config/staged/consumer edits (high worker
  owns), no content/route edits (S worker owns). Snapshot `source-manifest.json` (explicit path/SHA/bytes).
- Commit meaningful NEW tool source BEFORE history validation (no `--allow-empty`, code before authorities,
  fixture identity `fixture@example.invalid`, `commit.gpgsign false`):
  weekly `296a9cc`, longform `404c7d8`, each 9 files (3 M + 6 A), old E remains ?? untracked,
  `ls-files` 727 (721+6 new), trees equal `5e38950…` (coherent). No `git clean/reset`, no network,
  no old runner exec. `PYTHONDONTWRITEBYTECODE=1`, fixture paths verified import origin
  (`sys.path.insert NEW DB first, assert __file__ starts with NEW DB`).

## 3. Public proofs on BOTH real fixtures (authority positive = real R3, not synthetic)

Script `verify_history_fix.py` (dedicated editor, `PYTHONDONTWRITEBYTECODE=1`, fixture import origin verified):

- HIST `verify_versioned_history` PASS both (chain 1, anchor VALIDATION_CHECKPOINT, refs 1,
  `observed_source_bindings` NONEMPTY 11 rows (7 required + 2 optional specs + 2 tool), O17 `""`,
  RECEIPT+STAGED+SCHEMA, each verified git blob via H (schema `git show` + mode + live SHA),
  `materialization_lineage` with original proposal/staged/scope producer + receipt/seal/build/retention).
- E absent at old tool commit positive both (`git show 721a04d:E_path` exit 128, HIST still passes).
- beforeState COPY not live + old State mutated: live vs before_ref SHA differs
  (weekly live `ca7c0d2e…` vs before `ad2d207c…`; longform live `17c20a1e…` vs before `40107355…`),
  retained COPY matches before_ref, HIST passes despite live mutation (proving COPY not live).
- `agent.validate_agent_state` on canonical LIVE old R3 after NEW tool commit PASS (0 errors,
  STATE structure, absolute root, no fake/pending/skip).
- Old full receipt REFUSE via public `edpub.validate_editorial_receipt` (TOOL_DRIFT on H-owned
  revalidation schema, Core-change proof; weekly/longform both `STAGED_REFUSED … TOOL_DRIFT …
  schemas/publication-surface-revalidation.schema.json`).
- Mutations each hit intended seam + repair (real graph/role arrays, not minimal synthetic):
  seal 15-name, staged code_deps 50 subset, receipt file SHA drift (authority), receipt closure TOOL_DRIFT
  direct (real OLD 50, no file mutation), scope SHA drift, retained-COPY tamper, digest recompute mismatch.
  Each HIST preempts with exact HISTORY_* code, repair restores bytes + re-PASS.
- Row-level observed-binding mutations via strict checker (derived proposal SCHEMA + RECEIPT tool rows):
  epoch `f*40` → `HISTORY_TOOL_EPOCH_DRIFT`; owner unregistered → `UNSUPPORTED_MIGRATION`;
  extra key → `HISTORY_DIGEST_MISMATCH`; omit required key → `HISTORY_DIGEST_MISMATCH`;
  O17 pointer `/` → `HISTORY_DIGEST_MISMATCH` (must be `""`); tool epoch `0*40` → fail-closed
  `HISTORY_BLOB_MISSING`/`HISTORY_TOOL_EPOCH_DRIFT` (no caller authority; distinct-epoch tool test
  deferred to narrow renewal unit since real R3 both epochs coincide at 721a04d).
- Raw layer: duplicate JSON → duplicate refusal; traversal `../escape` → `HISTORY_MODE`;
  symlink → `HISTORY_MODE` symlink refusal (repair by unlink).
- Raw output `run-raw.txt` exit 0. No high stubs for claimed whole proof (no `survey_versioned_renewal_v2.py`
  created; high lifecycle pending high worker).

## 4. Narrow renewal-graph unit — explicitly NOT ENDTOEND (high not ready)

Synthetic versioned fixture (complete-source DB, 63 NEW closure, minimal valid receipt with
`current_tools.commit`) exercising row-level seams (epoch/owner/extra-key/omit-key/O17 `/`/dup-JSON)
via H strict checker + documenting array-order (`file_order != sorted` → `HISTORY_TOOL_EPOCH_DRIFT`
in `_verify_versioned_ancestor`) without executing full high lifecycle (prepare/finalize/activate/resume,
C→U→U, renewal→editorial, normal direct Candidate/Preview/Freeze/Release). Labelled
`NARROW RENEWAL GRAPH UNIT — NOT ENDTOEND` in script output. NOT whole completion, NOT independent PASS,
production semantic NO-GO. No high stubs.

## 5. No-regression checks + remaining

- Existing phase-h editorial synthetic (`test_complete_editorial_passes_and_mutations`) still PASS
  (no fake R receipt involved). Existing phase-h versioned synthetic now correctly REFUSES fake
  `R/validated-source-manifest.json` (`b'{"receipt":1}'` lacks `current_tools`) with
  `HISTORY_DIGEST_MISMATCH: receipt tool doc lacks current_tools` — stricter (correct) H, fixture
  invalid (real R receipts have `current_tools`), preserved as gap, not H weakening. Narrow unit with
  valid minimal receipt PASS. Low `test_survey_publication_set_v2` + `test_repository_contract_syntax`
  20/20 OK. No `__pycache__` in new DBs. No candidate/reconstruct commits.
- S worker must fix `_validate_scope_o17` blanket scope-row refusal (currently refuses ANY
  `schema_path == reader-surface-semantic-review` in `basis.observed` as caller row; correct
  history-derived O17 `""` rows from H must be accepted when equal to H rederived expected).
  High worker owns U/C + consumers + CLI/write/failure oracles + repeat/C→U→U/renewal→editorial/normal
  lifecycle + affected regressions + independent final review. Any map contradiction returns to Astra
  before broadening. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Production semantic
  NO-GO. Stop here. Ordinary Commit/Push Human-owned.
