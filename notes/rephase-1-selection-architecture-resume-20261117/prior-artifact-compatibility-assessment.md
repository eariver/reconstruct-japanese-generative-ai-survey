# Prior-artifact compatibility — bounded read-only assessment (no implementation)

Role: fresh bounded compatibility source reviewer, read-only, not implementation.
Scope: concrete existing `_prior_artifacts` integration gap for typed PREARCH
same-record triplet at `EVIDENCE_REVIEWED`. No code, no Git/import/runtime/tests/
network, no source/State artifact writes, no subagents, no whole-corpus scan.
Actual related source only. Source 774 unchanged.

Selected source (recorded, not re-verified here):
`.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`
(`3231a0c…/ff01b73…`, parent `ae0dd1ee…`). Identity discrepancy `d591` (actual
`.git/HEAD` in execution records) vs `f591` (prior prose/dispatch) is a separate
investigator handle per `astra-operation-resolution.md` §5. DO NOT duplicate Git
work, rebaseline, typo-fix raw, or conflate CURRENT synthetic proof epoch with
exact commit certificate.

Maps read: `astra-operation-resolution.md` §5 + `normal-stage-operation-map.md` +
machine. Execution evidence read: `execution-20261117T005500Z-SP|W34`
(`machine.json`, `stderr.txt`).

## 1. Defect source proof (EXIT2 before semantics, not scaling measurement)

Both normal `survey_stage_validation_v2.validate_stage` invocations refused
before `_validate_stage_semantics`:

- SP: `exit=2` after `35.004s`, `stdout_bytes=0`, `stderr_bytes=253`,
  `report absent`, State/checkpoint/guard unchanged.
- W34: `exit=2` after `180.013s`, same stderr, report absent.

`stderr` (both):

```text
prior Stage Checkpoint fails .../schemas/stage-checkpoint-v2.schema.json: $: 'from_state' is a required property
```

This is normal-stage compatibility refusal. The 35s/180s are time-to-refusal
through prior-artifact loading (including supplement-adjacent IO observed in
`/proc` windows), not a measurement of the later `45AG` upstream path or of
`_validate_stage_semantics` cost. Do not attribute these walls to scaling.

Exact gap in
`scripts/survey_stage_validation_v2.py`:

- ` _prior_artifacts` lines 328–423. Lines 333–337 correctly detect PREARCH
  family via strict pinned record (`_dm022_pinned_family`) and enforce the
  same-record shape (3 entries → 1 file). This guard passes for the adopted
  PREARCH triplet.
- Loop lines 351–375 then unconditionally validates **every** distinct prior
  checkpoint path at line 362 with:

  ```python
  record = schema_gate.load_and_validate_json(path, repo_root / agent.CHECKPOINT_SCHEMA, label="prior Stage Checkpoint")
  ```

  `agent.CHECKPOINT_SCHEMA` is `schemas/stage-checkpoint-v2.schema.json`
  (`survey_agent_control_v2.py:43`). That schema `required` includes
  `from_state,to_state,…` (schema lines 7–19) and forbids foreign keys.

- An adopted PREARCH record deliberately has nested
  `operation.{from_state,to_state}` + `producer_boundary.{from_state,to_state}`
  rather than legacy top-level `from_state/to_state`, plus `kind:
  PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, `reason`,
  `before_state/before_checkpoint/parent_checkpoint/original_anchor/supersedes/
  revision_id/revision_root/request/retention_plan/proof/decision/report/…/
  supersession_checkpoint_sha256` per
  `schemas/dm022-supersession-checkpoint-v2.schema.json` lines 7–8, 13–30.
  It therefore **correctly** fails the legacy schema with
  `'from_state' is a required property`. The bug is caller selection of the
  wrong loader/schema, not a malformed PREARCH record.

- `validate_stage` lines 852–907 calls `prior = _prior_artifacts(...)` at
  line 880 **before** `with runtime_tool.current_stage_basis_override():
  _validate_stage_semantics(...)` at 884–885 and before report build at
  889–903. Hence failure precedes semantic validation, report, checkpoint
  build, and advance. No `CORE_STAGE_CONTRACT` report was fabricated; no
  advance was attempted. Preserved.

## 2. Existing canonical reuse that the fix must use (no new surface)

The codebase already has the correct typed dispatch. The repair must reuse it,
not add a parallel validator, schema, family, cache, flag, or JSON projection.

- LOW strict typing:
  `scripts/survey_research_authority_v2.py:329–373`
  `load_typed_checkpoint_record` — `kind` absent → `LEGACY` via
  `OLD_CHECKPOINT_SCHEMA`; `kind == DM022_KIND` → `PREARCH` via
  `DM022_CHECKPOINT_SCHEMA` + strict `reason/operation/producer_boundary/
  checkpoints/artifacts/self-digest` checks; unknown `kind` refuses. No
  `kind`-default fallback.
- Agent prior-checkpoint validation:
  `scripts/survey_agent_control_v2.py:770–805` `_validate_checkpoint_record`
  — generic `low.load_typed_checkpoint_record` first; `PREARCH` → content
  (`_validate_prearchitecture_record_content`, lines 186–287) + triplet +
  issue binding + `_validate_prearchitecture_core_proof` (lines 290–321 via
  `low.check_supersession_record_from_paths`); legacy →
  `load_and_validate_json_strict` + producer/artifact/review re-hash +
  `_validate_core_stage_report` with historical State. Lines 811–812 explicitly
  refuse a PREARCH record reaching the legacy path as `DM022_WRONG_FAMILY`.
- Agent resolvers:
  `_resolve_prearchitecture_artifact` (circa 1060–1146),
  `_resolve_checkpoint_artifact` PREARCH dispatch (1202–1208),
  `resolve_active_evidence_views` PREARCH dispatch (1345–1361),
  `resolve_active_research_four_refs` (1389–1462) — same-record, live re-hash of
  all four, lineage + SELF/proof via 4-path checker, View→Evidence binding,
  `artifact_refs` exactly the 4 NamedRefs.
- Pinned family (no triplet heuristic):
  `survey_stage_validation_v2.py:194–209` and
  `survey_agent_control_v2.py:110–128` `_dm022_pinned_family` — reload pinned
  `checkpoint_provenance.evidence` via LOW. Healthy LEGACY same-triplet returns
  `LEGACY`; malformed raises fail-closed. Deprecated
  `_dm022_state_kind` (agent lines 131–149) is test-only heuristic and must not
  be used for routing.
- Stage R4 wiring: `_dm022_verify_current_r4` (stage lines 216–246) already
  uses `agent.resolve_active_research_four_refs` for `CANDIDATES_NORMALIZED`
  PREARCH current values. Same resolver is the canonical prior-lineage source.

## 3. Minimal repair recommendation (one function, existing imports only)

Change **only** `survey_stage_validation_v2._prior_artifacts` loop to dispatch
on the already-available typed family instead of unconditionally applying the
legacy schema. No new module/schema/family/cache/flag/parallel validator.
No PREARCH→legacy JSON projection. No fake `CORE_STAGE_CONTRACT` report.

Existing imports already cover the fix: `agent`, `low`, `_setmod`, `core`,
`schema_gate` (stage lines 22,30,36,39). No new `import`.

Recommended shape (intent, not code):

1. Keep lines 333–337 PREARCH same-record precheck and lines 338–350
   publication-approval / `resolve_active_publication_revalidation` /
   `superseded` / `bound_prior` / `seen_checkpoint_paths` logic unchanged.
2. For each distinct `rel` in `checkpoint_provenance` (excluding
   `publication_preview` as now): `fam =
   low.load_typed_checkpoint_record(repo_root, path)`.
   - If `fam.family == "PREARCH"`:
     `four = agent.resolve_active_research_four_refs(repo_root, cfg, state)`
     once (or per distinct PREARCH path with same-record equality), then merge
     `four.artifact_refs` rows into `result` with the **same** checks the
     legacy branch performs: FILE existence/alias/`sha256` drift via
     `core.sha256_file`, `existing.resolve() != artifact.resolve()` →
     `prior Stage Checkpoints disagree on artifact name`, plus
     `issue_id` binding already enforced by the resolver chain. Do not trust a
     caller proof dict; paths come from the pinned record + revision retention
     mapping via the existing 4-path checker.
   - Else (`LEGACY`): retain current lines 362–375 byte-for-byte, including
     legacy `load_and_validate_json`, `issue_id` check, artifact drift check,
     disagree check, and `seen_checkpoint_paths` dedup.
3. Keep Group C `VERSIONED_ACTIVE` active7 overlay (lines 376–422) unchanged
   and after the above. Keep `_merge_artifacts` (449–455),
   `_evidence_basis`/`_selection_basis`/`_validate_stage_semantics`,
   `validate_stage` entry/prepublish `READY`, and report construction unchanged.

Digest closure groups (no new hashing authority):

- State triplet `path/sha256` → checkpoint FILE bytes `sha256` equality.
- Checkpoint record `artifacts[4].{name,path,sha256}` → live FILE re-hash for
  each of `evidence-acceptance/edition-views-acceptance/materiality-ledger/
  profile-completeness`.
- SizedRef `report/proof/decision/request/retention_plan/before_state` +
  `before_checkpoint/parent_checkpoint/original_anchor` + `revision_root/
  retention/state-before.json` via `low.check_supersession_record_from_paths`
  (detached proof), plus View→Evidence `evidence_acceptance_sha256` binding and
  `supersession_checkpoint_sha256` SELF digest.
- Current `candidate-matrix/candidate-selection` remain `_current_artifacts` +
  `_authority` re-hash; checkpoint `reviews[0]` SizedRef and report/decision
  bindings remain enforced downstream by agent `_validate_checkpoint_record`
  and `_validate_core_stage_report`, not bypassed here.

Preserve explicitly:

- FULL schemas: legacy `stage-checkpoint-v2` and PREARCH `dm022-supersession`
  both enforced via their own schema, never cross-validated.
- Report/decision binding, own-epoch, true R–E: no hand-normalized PREARCH
  record, no caller proof dict, no epoch pin change.
- Artifact conflict: `_merge_artifacts` replace-refusal stays.
- Seen-record path duplicate: `seen_checkpoint_paths` dedup stays; same-record
  PREARCH triplet resolves once.
- LIVE vs HISTORY: historical/diagnostic reads must not require guard absence;
  mutating path keeps entry + prepublish `_dm022_require_ready` (stage lines
  869, 887; agent lines 152–162). No operational guard in the read helper.
- Forward mutator `READY` entry + prepublish stays on `validate_stage`,
  `build_stage_checkpoint`, `advance_with_checkpoint`.

Callers affected: sole edited caller is `_prior_artifacts`. Unchanged consumers:
`_dm022_verify_current_r4`, `_merge_artifacts`, `_evidence_basis`,
`_selection_basis`, `_validate_stage_semantics`, `validate_stage`,
`agent.resolve_active_research_four_refs`,
`low.load_typed_checkpoint_record` /
`low.check_supersession_record_from_paths`,
`agent._validate_prearchitecture_record_content` /
`agent._validate_prearchitecture_core_proof`. No other callers need edits.

## 4. Existing tests that falsely appear to cover this path

Actual method names in
`tests/test_survey_stage_validation_v2.py` (94 lines, only stage-validation
test):

- `test_same_named_but_invalid_discovery_authority_is_rejected` — exercises
  **public** `validate_stage` but at `ISSUE_INITIALIZED` with a fake
  `discovery-acceptance`; never reaches `_prior_artifacts` PREARCH branch.
- `test_current_tool_basis_does_not_reuse_initialization_commit_as_execution_identity`
  — exercises `runtime_tool.verify_current_stage_basis` only; no stage
  validation, no PREARCH.
- `test_draft_stage_validator_requires_paired_package_and_result_authorities`
  — exercises **private** `stage_validation._current_artifacts` with synthetic
  `ARCHITECTURE_ESTABLISHED` draft-package/draft-result mismatch; no public
  `validate_stage`, no prior checkpoints, no PREARCH.

Hence none covers EVIDENCE_REVIEWED PREARCH same-record prior via public
`validate_stage` after adopt.

Related public-`validate_stage` coverage elsewhere is at other lifecycles or
with LEGACY provenances and does not traverse the failing branch, e.g.
`test_dm022_b_late_prepublish_v2.Dm022BLatePrepublishTests.
test_b_stage_validate_prepublish` validates `ISSUE_INITIALIZED` with
`discovery-acceptance` and a guard-injection refusal; it does not supply an
adopted PREARCH `evidence/materiality/completeness` triplet at
`EVIDENCE_REVIEWED`. Any claim that B-side, C-side, supplement-carry, or
lifecycle tests already prove `_prior_artifacts` PREARCH compatibility is
therefore false coverage via private path or wrong lifecycle. Real chain needed:
public `validate_stage` on an adopted PREARCH State, no fake `CORE` report, no
hand-built legacy projection of the PREARCH record.

## 5. Collision and malformed-triplet considerations (must be preserved)

- Repeated correction / stage future publication `active7` overlay: Group C
  `VERSIONED_ACTIVE` overlay (stage 382–422) validates canonical anchor +
  historical rows via L `canonical7`, then overlays `effective7` active paths
  and requires downstream candidate to match active exactly. The PREARCH-prior
  fix must not weaken this: `prior_cand` vs active binding
  (`_require_active_candidate_binding`) and `_merge_artifacts` replace-refusal
  stay. A future publication-stage `validate_stage` with both PREARCH research
  prior and `VERSIONED_ACTIVE` selection must resolve research via the same
  typed four-ref path **and** publication via the seal path, with historical
  bytes pinned and active projection explicit.
- Malformed same-triplet LEGACY positive: healthy LEGACY states may share one
  path/sha across `evidence/materiality/completeness` (same file, legacy
  shape). `_dm022_pinned_family` correctly returns `LEGACY` for them; the fix
  must keep that branch on the legacy loader with full schema + drift checks
  and must not route them through the PREARCH resolver merely because
  `len(paths)==1`. Malformed PREARCH (bad `kind/reason/operation/boundary/
  checkpoints/artifacts/SizedRefs/digest`) must fail closed via LOW/agent
  errors, never fall back to legacy.

## 6. Full public-stage semantics cost remains unmeasured

Even after the compatibility fix, existing public stage full semantics costs
remain: `EVIDENCE_REVIEWED._selection_basis` re-reads Discovery/Screening/
Evidence/Views/Ledger/Completeness plus transitive supplement Raw per task,
then Matrix (409 W34 / 160 SP) + Selection exact-once coverage; `agent.
validate_agent_state` re-validates every passed checkpoint via typed loader +
  FULL PREARCH proof + legacy artifact/review re-hash + core-report + history/
  gates. No caller bundle/skip exists (`_SelectionReadSet` is writer-private).
Prior writer walls (W34 836s, SP 148s) are wall-only (no `rchar`/CPU/call-count
proof). The failed 35s/180s walls are refusal observations with `/proc`
windows, not speedup or total-cost proof. Preserve the remaining cost as
UNKNOWN later potential; do not claim the one-branch fix solves all stage
performance or proves a 1200s bound will hold.

## 7. Planned oracles (no execution now; for root dispatch after repair)

Meaningful specific regression (synthetic, isolated, no network):

- Construct minimal adopted-PREARCH `EVIDENCE_REVIEWED` State (typed
  same-record triplet + 4 R refs + `CANDIDATES_NORMALIZED` history) and invoke
  **public** `stage_validation.validate_stage` with synthetic
  `candidate-matrix/candidate-selection` that satisfy Matrix/Selection
  validators. Oracle: `PASS` report with exact
  `from_state/to_state/production_state/production_profile/
  implementation_commit_sha/contract/artifacts/recorded_at`; no overwrite on
  rerun (`refusing to overwrite…`); malformed PREARCH (e.g. legacy-projected
  PREARCH JSON with top-level `from_state`) refuses fail-closed without report.
- Negative: same PREARCH State through legacy-only loader would still EXIT2
  with the observed `'from_state' is a required property`; after repair this
  negative is quarantined to the legacy branch test, not the public path.

Full real normal `validate → build → advance` oracles (sequential SP then W34,
or W34 then SP per root order, only if source/State/inputs unchanged):

- `validate_stage` → `CORE_STAGE_CONTRACT` PASS report (new unique path,
  re-hash/path/contract/impl pins shown); `build_stage_checkpoint` +
  `advance_with_checkpoint` via existing `advance-stage` CLI with genuine
  deterministic + independent `AGENT_RESEARCH` review rows; checkpoint at
  `sources/<edition>/orchestration/v2/checkpoints/EVIDENCE_REVIEWED.json`;
  State `EVIDENCE_REVIEWED → SELECTION_COMPLETE` with `history/contract/impl`
  pins; no State/checkpoint/report overwrite, no guard injection, no HEAD move.
- Observability without bypass: `timeout 1200s` per edition-stage, sequential,
  absolute `--repo-root`, repo-rel `--state/--artifact/--output/--reviews`,
  unique raw/observation files, actual child PID/wall/exit/`stdout/stderr`/
  report bytes/hash or actual absence, before/after authority/output inventories,
  stdlib-only same-child `/proc` windows labelled observed-vs-total. On any
  `exit 2`/timeout stop that edition immediately, preserve partials, return to
  root; do not auto-retry, extend bound, profile, or swap in a private/bypass
  validator. Then repeat for `SELECTION_COMPLETE → ARCHITECTURE_ESTABLISHED`
  only after the first advance lands.

## 8. Unresolved decisions (for root, not this read-only review)

- Source identity: `d591` vs `f591` full-SHA discrepancy, prefix-only
  `head_expected_prefix` weakening, and whether documentary transcription vs
  ref drift is evidenced. No Git work duplicated here.
- Whether the one-function `_prior_artifacts` reuse above is sufficient or
  whether `survey_agent_control_v2._validate_checkpoint_record` /
  `_resolve_checkpoint_artifact` need a shared helper to avoid drift (preference
  here: reuse existing resolvers as-is, no new helper/surface).
- 1200s bound adequacy for full real `EVIDENCE_REVIEWED` validation on 3231
  given supplement-transitive reloads; missing-blob/retention/COPY drift, guard,
  HEAD, or contract drift handling; retry vs investment choice.
- No retreat from `FULL` schemas, report/decision binding, own-epoch, true
  R–E, conflict/duplicate, LIVE-vs-HISTORY, guard, or forward-mutator `READY`
  predicates to make validation pass.

## 9. Bounded root choice and scope (not a general precode cycle)

- **Choice:** accept this assessment as the scoped `_prior_artifacts`
  integration-gap diagnosis; authorize a **single-function** compatibility
  repair reusing existing `low.load_typed_checkpoint_record` +
  `agent.resolve_active_research_four_refs` (+ existing 4-path proof) with no
  new module/schema/family/cache/flag/parallel validator and no
  PREARCH→legacy projection. Require a fresh scoped regression (public
  `validate_stage` on synthetic PREARCH) plus independent review of the exact
  diff before any real normal `validate → build → advance` dispatch.
- **Scope:** `_prior_artifacts` branch only + named regression + full real
  normal-path oracles above with timeout observation. Explicitly **not** a
  general precode cycle, generic reader, writer rerun, R4/PDF/Production,
  source/State rewrite, or broad test-suite green claim. Whole
  `NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN`
  preserved; substantive R2 reviews remain bounded editorial evidence until a
  mechanical PASS exists.

machine JSON bracket corrected, no substantive changes; identity now resolved by source-identity-resolution + root operation §6; original identity UNKNOWN was at assessment time.
