# Workstream A report — Evidence canonical mapper + Screening prepackage/admission/universe

2026-10-31. Workstream A implementation return. Workcopy ONLY:
`.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`.
No subagents used. No ordinary Git commit/push, no reconstruct Git status/HEAD/log/Human
readback, no network/Production/restore/intake/cleanup/reset. Old proofs/captures/frozen
documents untouched. No behavioral suites run (concurrently mutating source; dedicated worker
tests a fixed integrated snapshot).

Authority (read in full before review): contract
`outputs/rephase-1-profile-support-contract-decision.md` INCLUDING §7 (FULL
`62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`), contract ROOT
`notes/rephase-1-profile-support-contract/astra-review-resolution.md` §5 (FULL
`021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`), precode assessment
`outputs/rephase-1-profile-support-precode-assessment.md`, packet
`notes/rephase-1-profile-support-precode/README.md`, mandatory precode ROOT FULL
`bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa` /20159B INCLUDING §7,
R3 mechanics overridden by R4 then R5 REQUIRED-path hardening. Scope reassessment
`outputs/rephase-1-scope-reassessment-20261031.md` §§1,3,8 removes the generic-reader
follow-on only, not technical safeguards. No precode re-cycle done.

## 1. Edited paths (exclusive ownership kept)

- `scripts/survey_evidence_v2.py` — canonical10 additive rows + Evidence-side preflight
  helper + 3 NEW-branch callsites (prepare/accept/Views-accept). No other edits.
- `scripts/survey_screening_v2.py` — pure universe/loss/bindings helpers + admission gate +
  PATH-only `resolve_prepackage_root_effective` + 2 NEW-branch callsites
  (prepare_package/accept_results). Added stdlib imports `errno, os, stat` only.
- `scripts/survey_discovery_v2.py` — NOT edited. The public Discovery validator
  `validate_acceptance:274-298` is already state-free per R4 RB1; no approved map change
  requires a Discovery edit. Verified byte-identical to the starting snapshot (diff empty).

Tool note: the `apply_patch` CLI is not installed in this environment (`which apply_patch`
not found), so every edit was applied with the file-edit tool as an exact-string
replacement with equivalent scope (one edit per hunk, no other bytes touched). Proof-vs-workcopy
diff below confirms additions-only, zero removals in Screening and map/helper/callsite-only
changes in Evidence.

## 2. Concrete implemented behaviors

### 2.1 DM016 canonical10 (Evidence)

`SOURCE_CLASS_MAP` gains exactly the 10 contract §3 rows; every pre-existing row/value is
byte-unchanged:

- `PRIMARY_DOC` → `PRIMARY_OFFICIAL`
- `PRIMARY_REPO` → `PRIMARY_REPOSITORY`
- `PRIMARY_ANNOUNCEMENT` → `PRIMARY_OFFICIAL`
- `PRIMARY_MODEL_CARD` → `PRIMARY_OFFICIAL`
- `PRIMARY_SPEC` → `PRIMARY_OFFICIAL`
- `SECONDARY_REFERENCE` → `SECONDARY`
- `SECONDARY_TECHNICAL` → `SECONDARY`
- `RUNTIME_RECIPE` → `PRIMARY_OFFICIAL`
- `PACKAGING_DOCS` → `PRIMARY_OFFICIAL`
- `RUNTIME_PR` → `PRIMARY_REPOSITORY`

No aliases, no default SECONDARY, no URL sniffing, no v1-enum edits, no SOCIAL expansion.
`_source_class` signature/semantics unchanged (fail-closed `ValueError` on unknown).
Enforcement flows through the existing leaves (`task_authority_sources`, supplement check
`entry[source_class]==_source_class(entry[source_type])`, card branches) plus the new
preflights below, all calling the single canonical mapper.

### 2.2 Shared pure helpers (Screening, single home — R3 §6.1)

- `compute_obligation_universe(profile_initial_ids: set[str], root_records: list[dict],
  effective_records: list[dict]) -> set[str]` — returns `P ∪ named(R) ∪ named(E)` where
  `named(X)` unions `provenance.obligation_ids` over `X`. Pure: no I/O, no State, no
  authority token. For worker B's 3/5/U coverage.
- `find_declaration_loss(root_records, effective_records) -> list[tuple[str, str]]` —
  for every root `r` and every `o ∈ r.provenance.obligation_ids`, requires an effective
  carrier `e` with `o ∈ e.provenance.obligation_ids` AND (`e.discovery_id == r.discovery_id`
  OR `r.discovery_id ∈ e.provenance.parent_refs` with actual string-array check). Returns
  sorted `(parent_id, OID)` uncovered list; `[]` = pass. Global-set equality is NOT
  sufficient (shared-OID many-to-many preserved). Pure. `validate_discovery_expansion` and
  all `_content` cores are untouched.
- `derive_bindings(oid, effective_records, ledger_task_by_discovery) -> tuple[list[str],
  list[str]]` — `(sorted declaring DIDs incl DROP declarers, sorted union task IDs from the
  supplied Ledger map)`. Profile-only yields `([], [])`; DROP declarers yield DIDs with no
  invented task IDs (Ledger binds no tasks to DROP). Pure. For worker B's `_build_completeness`.
- `check_new_operation_admission(root_records, effective_records) -> None` — Screening-side
  combined gate: canonical Evidence `_source_class` over every root+effective record
  (including prospective DROP) via function-local import (precedent `:397`), then
  `find_declaration_loss` refusal. Exact errors in §4.

### 2.3 PATH-only prepackage binding (Screening — R4 RB6, R5 §4)

`resolve_prepackage_root_effective(repo_root: Path, state_path: Path, discovery_path: Path,
accepted_discovery_path: Path | None) -> dict` — PATHS-only; reloads State/cfg/Profile,
runs `verify_state_basis` with in-run `repository_commit_sha`, validates supplied Discovery,
derives canonical marker `source_root/discovery/discovery-accepted-v2.json` itself.

- Only `ENOENT` (`errno.ENOENT` via `os.lstat`) means absent. Symlink/nonregular/unreadable
  (`os.access`)/schema-parse failure refuses; never DIRECT fallback.
- Supplied expected path is an expected binding only: when a marker is present it must
  resolve-equal the canonical marker with equal SHA bytes; foreign/missing/mismatched
  refuses. `None` means no additional expectation and never suppresses a present marker.
- Claimed accepted root never DIRECT fallback: `DISCOVERY_COLLECTED` lifecycle or State
  `checkpoint_provenance.discovery` with absent marker refuses (`Stage claimed accepted
  Discovery but marker is missing`).
- Genuine initial DIRECT (`ISSUE_INITIALIZED`, absent, unclaimed → `root==records==supplied`)
  and valid-marker initial-pending (marker validated → DIRECT or `validate_discovery_expansion`
  DERIVED) preserved. Entry lifecycles stay `ISSUE_INITIALIZED|DISCOVERY_COLLECTED`.
- Returns R4 names (overriding R3 `mode`/`marker_kind`): `authorityKind`
  (`NO_MARKER`|`CANONICAL_MARKER`; see §6 on reserved `STAGE_CLAIMED`) + `basisMode`
  (`DIRECT`|`DERIVED_EXPANSION`) with full R3 context fields otherwise intact: `profile`,
  `profile_path`, `profile_sha256`, `state`, `state_sha256`, `root_records`, `root_path`,
  `root_sha256`, `root_record_count`, `records`, `discovery_path`, `discovery_sha256`,
  `discovery_record_count`, `accepted_path|None`, `accepted_sha256|None`,
  `accepted_record_count|None` (+ `accounted_root_ids` on DERIVED).

### 2.4 NEW-branch preflights before first write (history untouched)

- Screening `prepare_package`: `resolve_prepackage_root_effective(..., None)` +
  `check_new_operation_admission` immediately after `validate_discovery_set`, before
  prompt/contract checks and well before non-empty refuse `:517` / `mkdir` `:520` /
  `write_jsonl` `:525` / `core.write_json` `:566`.
- Screening `accept_results`: resolver `resolve_effective_discovery_basis` (LIVE-bound,
  correct for this current-path owner) + `check_new_operation_admission` AFTER the
  idempotent `run_dir.exists` re-read branch, BEFORE first `copy2` in `:958-977`.
- Evidence `prepare_evidence_package`: resolver on the Screening package +
  `_preflight_new_evidence_admission(root, discoveries-effective-incl-DROP)` after the
  State-identity check, before required-contract checks / non-empty refuse `:595` / temp
  `task-*.json:631` + `package.json:680`.
- Evidence `accept_evidence_results` / `accept_edition_views`: same helper AFTER the
  idempotent digest-dir re-read branches (`:1191-1192`/`:1864-1865`), BEFORE `mkdir`+`copy2`
  canonical writes. Prepublish/entry DM022 guards and existing failure/no-overwrite windows
  unchanged; no new global-atomicity claim.
- `_preflight_new_evidence_admission(root_records, effective_records) -> None` (Evidence):
  direct `_source_class` per record source_type (no import needed) + shared
  `screening.find_declaration_loss` (existing top-level import). Historical
  `validate_*`/`_validate_*_content`/renewal cores gain NO new-policy gate.

Top-level imports unchanged (Screening: `core` only + stdlib; Evidence: `core, schema_gate,
screening` as before). Evidence-leaf calls from Screening are function-local only — no
top-level Screening↔Evidence cycle.

## 3. Forwarding to integrator / other owners (same unit wiring, not new capability)

- **Worker B (ordinary runner/adapters):** consume `compute_obligation_universe`,
  `find_declaration_loss` (and `derive_bindings` for `_build_completeness`) with required
  keyword-only `discovery_records`/`root_discovery_records`; implement U coverage, 3/5 shapes,
  closure-first residual union, thin agent-first delegation. Pure-helper signatures/returns
  are frozen as in §2.2/§4. B must pass the already-resolved canonical `root_records`+`records`
  (from `resolve_effective_discovery_basis:641-648`); never compact summaries, second fetch,
  supplement-derived universe, or caller verified flags.
- **Worker C (DM022 HIGH/LOW):** consume the same pure helpers plus canonical `_source_class`
  via YOUR PATH-loaded true R/E (own `derive_ordinary/derive_current` loaders + private
  kernel). Do NOT copy A's Evidence-accept pattern of calling LIVE-bound
  `screening.resolve_effective_discovery_basis` into LOW historical recovery — LOW uses
  `_content` siblings only (R4 RB1). HIGH eligibility (DM022 7-field, never ordinary 3/5)
  runs before first State COPY `:538`; adopt re-verifies in the `:1127` window.
- **Runner dead table (B/integrator):** `run_evidence_v2_interactive.SOURCE_CLASS_MAP:49-56`
  + `_source_class:110-114` (unused six-key local) still exists — A did not touch runner
  files per ownership. Remove it in the runner-owned diff after caller census (or delegate
  to canonical); do not keep two maintained tables. Live card/task paths already call
  `evidence.task_authority_sources`.
- **Tests/fixtures (worker D):** A edited no tests. Oracle intent: all10 types via actual v2
  task/card; unchanged old types; unknown incl DROP refused pre-write; shared-OID
  `(R2,O1)`-style loss refused despite global equality; DIRECT/DERIVED prepackage rows
  R1/R2 pass with exact errors on R3/R4/R5 rows; `U==P` initial-only 3-field passes.
- No schema/module/family/request-field changes made or needed by A.

## 4. Exact integration contract (names + errors)

Public/pure names: `compute_obligation_universe`, `find_declaration_loss`, `derive_bindings`,
`check_new_operation_admission`, `resolve_prepackage_root_effective`,
`_preflight_new_evidence_admission` (Evidence-private by leading underscore; Screening's
`check_new_operation_admission` is the cross-file gate for Screening sites).

Exact error strings raised:

- `unsupported source_type for Evidence authority: {source_type!r}` (canonical leaf)
- `DECLARATION_LOSS uncovered={uncovered!r}` with sorted `(parent,OID)` list
- `Stage claimed accepted Discovery but marker is missing`
- `supplied accepted Discovery path has no canonical marker to bind`
- `supplied accepted Discovery path is missing` / `is not a regular file` /
  `does not match canonical marker` / `does not match canonical marker bytes`
- `accepted Discovery marker is symlinked` / `is not a regular file` / `is unreadable` /
  `accepted Discovery marker invalid: {cause}` / `accepted Discovery marker unreadable: ...`
- `accepted Discovery JSONL SHA drift`, `accepted Discovery graph IDs differ from accepted
  Discovery JSONL`, `direct Screening basis does not bind accepted Discovery bytes`
- `Screening Discovery basis does not match session root/effective basis`
- `Screening preparation requires ISSUE_INITIALIZED or DISCOVERY_COLLECTED state`

## 5. Authority/dependency/contract gaps

**None blocking discovered.** No new capability, schema, module, family, request field, or
support reduction was needed; no missing authority bytes blocked the assigned sites. Two
judgment calls returned for integrator/Astra awareness (not expansions):

1. `authorityKind` reserves the contract enum value `STAGE_CLAIMED` but never returns it as
   success: a Stage-claimed-but-unbound state refuses instead (R4 R4). If Astra wants
   `STAGE_CLAIMED` as a returned success kind (e.g. COLLECTED+marker-present split from
   `CANONICAL_MARKER`), that is a contract clarification, not code broadening — A kept the
   refuse semantic and documented the reservation in the docstring.
2. Evidence NEW-branch preflights resolve the Screening package through LIVE-bound
   `resolve_effective_discovery_basis` (correct for current-path E1/E2/Views owners). This
   pattern must not be reused in LOW detached recovery (worker C boundary).

## 6. Verification (narrow, static-only) and limits

Checks run (all with `PYTHONDONTWRITEBYTECODE=1`, no `.pyc`, no project imports):

1. `AST parse both files` → `AST_PARSE_OK [...evidence, ...screening]`, exit 0.
2. `AST symbol census` → all of `compute_obligation_universe, find_declaration_loss,
   derive_bindings, check_new_operation_admission, resolve_prepackage_root_effective,
   prepare_package, accept_results` present in Screening; `_source_class,
   _preflight_new_evidence_admission, prepare_evidence_package, accept_evidence_results,
   accept_edition_views` present in Evidence; exit 0.
3. `Top-level import audit` → Screening top-level imports are stdlib + `core` only (no
   top-level Evidence import; Evidence-leaf import is function-local line ~450); exit 0.
4. `Proof-snapshot diff` (workcopy vs `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`):
   Evidence 68 changed lines = exactly the 5 A hunks (§2.1 + helper + 3 callsites);
   Screening 333 added / 0 removed = exactly the A additions; Discovery 0 (untouched).
   (Raw `git diff` vs HEAD is larger because it includes the final133 overlay itself;
   the proof-snapshot diff isolates the A runtime diff.)
5. `find *.pyc/__pycache__ under candidate-work/scripts` → empty (no bytecode emitted).
6. Source pins (workcopy, post-edit): `survey_evidence_v2.py` 129758B sha256
   `174c04cf37ca77f4394c9c7e2bcca9bc05c4c68aeccf0788df964249187fdc88`;
   `survey_screening_v2.py` 66344B sha256
   `8155dea36979bf92d9da405b4f32d8896064cc2526e2106c288f277564ce5386`;
   `survey_discovery_v2.py` 14044B sha256
   `dc1897bec4029507b596f5160216f1f79020c83489e76ad076b4aa01e55dbfe7` (unedited).

Limits (honest, not waived): static parse + symbol/import/diff audits only — NOT runtime
proof. No imports, no behavioral suites (concurrent mutation), no fixtures, no DM022
HIGH/LOW or runner paths executed. Cross-file APIs (B's runner preflight, C's HIGH/LOW
eligibility, D's tests) cannot be assumed executed until integrated. One static-check
invocation initially failed on a wrong relative path (workdir `scripts/` + `scripts/` prefix,
`FileNotFoundError`) — rerun with corrected paths passed; no source impact. Shared-workcopy
concurrency noted: ownership respected (only the two A files plus this report written), but
integrator must re-verify the fixed snapshot before behavioral testing.

## 7. Files written

- Exclusive runtime edits: `scripts/survey_evidence_v2.py`, `scripts/survey_screening_v2.py`
  (workcopy only).
- This report: `notes/rephase-1-profile-support-implementation/workstream-a.md` (only
  workspace-side write). No tests/fixtures/schema/config/docs touched.

## 8. Correction — astra review #1 (STAGE_CLAIMED binding + path hardening)

2026-10-31, second return. Root's `astra-implementation-review.md` #1 is a blocking
within-map defect in the first return above: `resolve_prepackage_root_effective` validated
the State discovery claim ONLY in the marker-absent branch, returning `CANONICAL_MARKER`
for any present valid marker without binding the State-named DCP. §§1–7 above are preserved
as the first return's claims; this section corrects them (no new contract gate — ROOT§7.1
and R5§4 already require this, and the misleading `STAGE_CLAIMED`-reservation wording was
removed from the shipping docstring per review #6).

Corrected behavior (Screening only; Evidence/Discovery untouched this round):

- Marker-present branch now binds the State-named DCP claim through new private
  `_validate_prepackage_dcp_claim` (ordinary LEGACY DCP predicates mirrored from the
  in-map reference, with LIVE-prepackage bindings): claim shape exactly `{path,sha256}` →
  record file bytes == claim SHA → `stage-checkpoint-v2` schema (PREARCH-shaped records
  fail it) → issue/producer (`stage_plan` discovery producer)/`checkpoints` membership →
  exactly-one `discovery-acceptance` NamedRef → exactly-one CORE_STAGE_CONTRACT
  DETERMINISTIC PASS with every deterministic result ref file-rehashed (incl byte_count) →
  historical 12-key report with record-owned profile/contract/implementation equality and
  canonical State path-only (no live SHA comparison) → DCP artifact path+SHA equality with
  the canonical marker. Success yields `authorityKind="STAGE_CLAIMED"`; a valid but
  unrelated marker refuses (`... does not bind the canonical marker`). `DISCOVERY_COLLECTED`
  with missing/malformed named claim refuses; `ISSUE_INITIALIZED` with no claim keeps the
  genuine initial valid-marker pending case (`CANONICAL_MARKER`); no-marker `DIRECT`
  (`NO_MARKER`) unchanged. No public resolver on the future package, no screening
  acceptance (not yet prepared), no agent publication/machine-checkpoint machinery (which
  binds a different lifecycle moment), no new schema/module/family.
- Path hardening: State/supplied-Discovery/marker/expected inputs all resolve
  repository-locally with no-follow ancestor rules via `_resolve_repo_local_input`
  (CWD-relative semantics preserved, containment + per-part lstat + resolved recheck +
  regular-file leaf through existing `_repo_file`); marker readability proved with a
  no-follow open probe (`_probe_readable_no_follow`) instead of `os.access`; issue/profile/
  ref hashes checked at every link. Prior leaf-only messages
  (`... is symlinked`/`is not a regular file`/`is missing`) are superseded by
  `... must be repository-local: ...` / `... missing or unsafe: ...` / `... is unreadable:
  ...` refusals.
- B/C interfaces unchanged: `compute_obligation_universe`, `find_declaration_loss`,
  `derive_bindings`, `check_new_operation_admission`, `resolve_prepackage_root_effective`
  keep names/signatures/return fields; new privates are `_resolve_repo_local_input`,
  `_probe_readable_no_follow`, `_dcp_named_ref_map`, `_validate_prepackage_dcp_claim`,
  constants `_CORE_STAGE_CONTRACT_ID`, `_DCP_CHECKPOINT_SCHEMA`, `_DCP_ARTIFACT_NAME`,
  `_HISTORICAL_DCP_REPORT_KEYS`, helper `_is_hex`. New exact errors: `prepackage Discovery
  checkpoint named claim must be exactly {path,sha256}`, `... record bytes drift from named
  claim`, `... record invalid: ...`, `... producer mismatch: ...`,
  `... must list discovery in checkpoints`, `... must carry exactly one discovery-acceptance
  artifact ...`, `... requires exactly one CORE_STAGE_CONTRACT review ...`,
  `... CORE report {12-keys/identity/issue/from-to/profile/state-path/contract/
  implementation/recorded_at/artifacts} ...`, `... discovery-acceptance does not bind the
  canonical marker ...`, `Stage-claimed lifecycle DISCOVERY_COLLECTED requires a named
  Discovery checkpoint claim`. §4's list is extended by these; §5 item 1 (STAGE_CLAIMED
  clarification request) is withdrawn as implemented.
- Verification this round (static-only, `PYTHONDONTWRITEBYTECODE=1`, no project imports, no
  behavioral suites on moving source): AST parse both A files ok; symbol census adds the 5
  new privates/constants path ok; top-level import audit ok (Screening top-level still
  stdlib+`core` only; `schema_gate`/`evidence`/`discovery` leaves function-local at lines
  ~449/~561/~785/~998); proof-snapshot diff: Evidence +68/−0 (untouched this round, hash
  unchanged), Screening +615/−0 vs proof (entire A diff purely additive; raw `git diff` vs
  HEAD is larger only because it includes the final133 overlay), Discovery identical;
  `*.pyc`/`__pycache__` scan empty.
- Corrected source pins (workcopy): `survey_screening_v2.py` 81195B sha256
  `45e93e76a481b620cc4989efb1fb575d7278d2ad7ae5996320b240a1b6c2c665`;
  `survey_evidence_v2.py` 129758B sha256
  `174c04cf37ca77f4394c9c7e2bcca9bc05c4c68aeccf0788df964249187fdc88` (unchanged);
  `survey_discovery_v2.py` 14044B sha256
  `dc1897bec4029507b596f5160216f1f79020c83489e76ad076b4aa01e55dbfe7` (unedited).
- Limits carried forward: NOT runtime proof; cross-file execution (B preflight, C HIGH/LOW,
  D tests incl. healthy-claimed-DCP and mismatched-claim-vs-marker oracles) awaits the fixed
  integrated snapshot. No new gap found; machine-checkpoint `passed` flags and publication
  revalidation remain orchestrator/transition machinery outside this prepackage gate by map
  boundary (stated, not waived). Tool note: the harness provides no `apply_patch` tool or
  binary; all edits used the specialized file-edit tool as exact-string replacements —
  documented here per dispatch instead of re-probing the shell.
