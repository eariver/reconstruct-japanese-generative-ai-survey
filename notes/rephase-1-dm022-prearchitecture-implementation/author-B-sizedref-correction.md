# Owner-B SizedRef correction — PREARCH review result is SizedRef (A3 cross-owner)

2026-10-28. Corrects B-01 follow-on from `author-A3-return.md` §3 (A3 19/19
scoped private tests, repeat blocked on B). R2 snapshot + R1 immutable;
candidate-work is the unit-ongoing writable tree. No Human readback, no
ordinary commits/cleanup, no network. AST static only in this turn (source fix
before test snapshot); no broader edits, no A-test edits. A3
`test_repeat_correction_blocked_on_result_authority_shape` is a known blocker
control, not positive acceptance — B returns the fix here, A author promotes
the requirement positive afterwards.

## 1. Selected schema justification (no inference)

File: `notes/rephase-1-dm022-prearchitecture-precode/schema-proposals-r4/dm022-supersession-checkpoint-v2.schema.json`
`§§90-106` (`reviews` array, sole `DM022_SUPERSESSION_PROOF`):
`reviews[].result` is `{ "$ref": "#/$defs/SizedRef" }`.
`$defs.SizedRef` (`§§142-151`): `type object`, `additionalProperties: false`,
`required: [path, sha256, byte_count]`, `byte_count: integer minimum 1`.
This is distinct from `$defs.ArtifactRef` (`§§133-141`):
`required: [path, sha256]`, no `byte_count`; and from `NamedRef`
(`§§152-161`): `required: [name, path, sha256]`.

Actual new-CP bindings determined from the same selected file (not inferred
field names):
- SIZED (`{path,sha256,byte_count}`): `before_state`, `request`,
  `retention_plan`, `proof`, `decision`, `report` (all `SizedRef`), plus
  `reviews[].result` (SizedRef).
- ArtifactRef (`{path,sha256}`): `before_checkpoint.{evidence,materiality,
  completeness}`, `parent_checkpoint`, `original_anchor`, `profile`.
- NamedRef (`{name,path,sha256}`): `artifacts[4]` (evidence-acceptance,
  edition-views-acceptance, materiality-ledger, profile-completeness).
- Distinct `{path,sha256,revision_id}`: `supersedes[]` rows.
Legacy `schemas/stage-checkpoint-v2.schema.json` `reviews[].result` stays
2-key `artifactAuthority {path,sha256}` (or null); B keeps that branch
unchanged.

## 2. Exact B paths/lines fixed (B-owned only)

File: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work/scripts/survey_agent_control_v2.py`

- Branch 1 — pure shape: `def _validate_prearchitecture_record_content`
  (`:166ff`), reviews block `:213-261`. Was:
  `set(result) != {"path","sha256"}` (exact 2-key, rejects valid adopted CP).
  Now: exact `{"path","sha256","byte_count"}` with strict `path` non-empty,
  `sha256` hex64, `byte_count` int `>= 1` (bool excluded), exact keys (no
  foreign keys, no generic subset). File rehash/size lives path-side and in
  the A3 4-path checker before any authority consumer; this pure branch is
  shape-only by design. Also added exact SIZED vs ArtifactRef checks for
  `before_state/request/retention_plan/proof/decision/report` (SizedRef),
  `before_checkpoint.{3}` + `parent_checkpoint/original_anchor/profile`
  (ArtifactRef), reusing the same exact-key + `byte_count >= 1` discipline.
- Branch 2 — path proof: `def _validate_core_stage_report` PREARCH branch
  (`:585ff`), review block `:599-631`. Was: same 2-key check + sha-only
  rehash. Now (`:611-626`): exact 3-key SizedRef + `byte_count int >= 1` +
  `resolve_raw_path` + `sha256_repo_file == sha256` + `stat().st_size ==
  byte_count` (`byte_count mismatch` on drift), then proof-doc load. Legacy
  `CORE_STAGE_CONTRACT` branch (`:632ff`, `set(result_ref) !=
  {"path","sha256"}`) and release branch untouched.

No other B file changed in this turn. New A3 checker full proof already acts
before authority consumers; B does not downgrade it (B calls
`low.check_supersession_record_from_paths(repo_root, checkpoint_path,
report_path, before_copy_path)` with derived SizedRef/retention paths).

## 3. B tests (B-owned only, run later)

- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py`: helper
  `_schema_shaped_prearch_record` reviews result → 3-key SizedRef
  (`byte_count: 2`); `test_10` good/mixed results → 3-key with live
  `byte_count = len(raw)` (mixed still refused as sole-proof wrong review +
  no new files). `test_13/14/15` (added in R2 diagnostic correction) use A2
  real chain helpers (`test_survey_evidence_v2.make_chain` + HIGH
  prepare/adopt) and therefore validate the current A3 same-CP expected
  SizedRef end-to-end (`validate_agent_state` + `resolve_active_research_four_refs`
  with `artifact_refs` + later forward readback + guard-held split). No A-test
  edits; A3 blocker control stays as-is until A promotes it.
- Status: `ast.parse` OK for the 1 runtime file + 1 test file in this turn;
  no `unittest`/`pytest` executed (source fix before test snapshot, while
  A3/C1/C2 edit). Existing R2 11/11 + corrected `test_10` + new `test_13/14/15`
  run in the next frozen integrated snapshot.

Author: Owner B. Scope is the two PREARCH review-result branches + B-test
SizedRef alignment only; no legacy shape change, no broader edits, no
completion claimed.
