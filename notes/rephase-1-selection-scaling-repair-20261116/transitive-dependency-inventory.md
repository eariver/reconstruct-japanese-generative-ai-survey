# Transitive dependency inventory — existing Selection PREARCH validation

Status: SOURCE-READ-ONLY ANALYSIS. Not implementation authorization, not a new authority,
not a runtime proof, and not a global audit verdict.

Source: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
(recorded HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, parent
`cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, tree
`ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`, as recorded in the packet README).
The commit/tree was not re-verified with Git in this source-read action.

Method: source files in the active worktree only; no project source import, no execution,
no tests, no fixtures, no Git command, no network, no active/shadow/proof writes, no
subagents, no DB/corpus scan. One static config read as DATA was used to identify the
configured `orchestration.stage_plan`; no project module was imported. All counts below
are static source/call-graph estimates, not measured runtime counts or timing claims.

This file records consumed-file dependencies and field relationships. It does not select a
repair design and does not duplicate the author's separate LIVE/content factoring.

---

## 1. Root §4.1 confirmation: Discovery Raw exists without supplement

`scripts/survey_discovery_v2.py` `_normalize_record` lines 121-127 unconditionally reads and
hashes every `source.raw_paths` entry for every Discovery record:

- `raw_paths = source.get("raw_paths")` (121)
- non-empty string-list validation (122-123)
- for each `rel`: `_safe_repo_file(repo_root, rel)` and
  `raw_refs.append({"path": rel, "sha256": core.sha256_file(raw),
  "byte_count": raw.stat().st_size})` (125-127)

`survey_evidence_v2._resolve_phase_supplement_context` returns a legitimate empty supplement
context only when `package.authority_supplement` is absent (lines 322-330). That empty
supplement context says nothing about Discovery, X-intake, or in-memory session-root Raw
material. The R2 review's inference that an empty supplement means no non-supplement Raw is
incorrect and is retracted here.

---

## 2. Entry sequence in the existing runner

`scripts/run_selection_architecture_v2_interactive.py`

| Line | Existing call | Consumed-material class |
|---|---|---|
| 247-249 | `core.load_json(config)`, `core.load_json(state)`, `agent.validate_agent_state` | current config, LIVE State, Profile, State schema, legacy artifact, DCP/SCP, 3x PREARCH full proof |
| 260 | `_dm022_require_ready` -> `low.require_research_operation_ready` | guard, State, Profile, checkpoint, FULL completion (2 adopted-graph traversals) |
| 262 | `discovery.validate_acceptance` | Discovery acceptance, X manifest, config/Profile, X task/Raw, Discovery JSONL/Raw |
| 264 | `_dm022_resolve_ledger_completeness` -> `low.resolve_research_authority` (PREARCH) | full adopted graph, report, State/checkpoint recheck |
| 270-278 | `_dm022_pinned_family` + second `low.resolve_research_authority` | typed checkpoint reload; second full adopted graph |
| 283-285 | `screening.resolve_active_screening_acceptance` | State-bound SCP, package/batches/results/effective Discovery; internal strictState and overridden package-basis verifier |
| 286-291 | `screening.resolve_effective_discovery_basis` | Screening package, derived/root Discovery, acceptance |
| 304 | `_dm022_preflight_seven` | seven output-slot lstat checks |
| 309-313 | `architecture.derive_candidate_matrix` under `current_stage_basis_override` | LIVE `_load_upstream` E/V/L/C nesting |
| 316-319 | READY + matrix write | full completion again |
| 359 | `architecture.validate_selection` | config, Profile, matrix, completeness, ledger |
| 362-365 | READY + selection write | full completion |
| 422-430 | `architecture.validate_architecture` + READY + write | reads selection, Profile, matrix, completeness, ledger |
| 432-436 | `build_architecture_review_summary` under override | `_load_upstream` plus `validate_candidate_matrix` -> second `_load_upstream` |
| 440-448 | READY + review write + READY + attention | full completion twice; attention reads SCP acceptance, ledger, selection |
| 451-459 | READY + archive copy + READY + audit | full completion; audit hashes five outputs plus archive |
| 472-481 | return | relative paths/counts/readiness only; no output SHA re-hash |

---

## 3. Exact typed field -> file -> expected-pin relationships

### 3.1 LIVE State, Profile, config, schemas

| Typed field/ref | Path | Existing expected pin | Actual bytes consumed by | Notes |
|---|---|---|---|---|
| runner `state_path` | CLI path | no external SHA; the file itself is the authority input | runner 248; LOW readiness 4104; completion 1066-1068 | State content validated, not compared to a separately declared State hash |
| `state.profile.{path,sha256}` | repo-relative Profile | SHA from State | runner 255; agent `_profile_and_source` 547-575; LOW `_bind_profile_and_canonical` 1687-1732; Screening `_canonical_root_acceptance` 953-961 | Profile bytes are actually read/hashed |
| `profile.paths.source_root` | directory | no hash; path only | output root; supplement containment | Not a byte pin |
| `state.legacy_compatibility.legacy_state_path` + present/sha | file | present + SHA from State | agent strictState 947-956 | Current compatibility artifact |
| `state.checkpoint_provenance.{evidence,materiality,completeness}` | ArtifactRef `{path,sha256}` | SHA from State | agent/LOW typed loader; `require_same_triplet` 387-400 | Same PREARCH record path/SHA |
| `state.checkpoint_provenance.discovery/screening` | ArtifactRef `{path,sha256}` | SHA from State | `_context_from_before_state` 1765-1789 | Legacy DCP/SCP records |
| `config/survey-production-v2.json` | static repo path | no declared hash in selection path | runner 247; agent producer/control; LOW `_legacy_producer_check` 1289-1322 and `_bind_profile_and_canonical` 1709-1717; Screening live basis | Own epoch reads the COMMIT config 673-685, not current source |
| `schemas/survey-production-state.schema.json` | static | no declared hash | agent 937; LOW 1906 | Current tool schema |
| `schemas/survey-production-profile.schema.json` | static | no declared hash | LOW 1705 | Current tool schema |
| `schemas/stage-checkpoint-v2.schema.json` | static | no declared hash | legacy DCP/SCP typed load 346-350 | Current tool schema |
| `schemas/dm022-supersession-checkpoint-v2.schema.json` | static | `$id` checked in own epoch | typed load 352-357 | DM022 checkpoint |
| `schemas/dm022-revision-request-v2.schema.json` | static | no declared hash; object contract used in own epoch | request validators 842, 1238 | Request |
| `schemas/dm022-revision-manifest-v2.schema.json` | static | no declared hash; object contract used in own epoch | manifest validators 875, 3402 | Manifest |
| `schemas/dm022-preadoption-report-v2.schema.json` | static | no declared hash; object contract used in own epoch | report validators 242, 1186, 3897 | Report |
| `schemas/dm022-revision-proof-v2.schema.json` | static | no declared hash in selection readback | only proof build path 3842; selection readback does not validate proof bytes | Proof schema is not opened by the readback inventory shown here |

`state.history`, `state.contract`, and `state.implementation` are DATA-only for content
validation: strictState checks history shape/monotonicity and `profile.contract ==
state.contract`, but PREARCH selection content does not recompute Contract8 from current
config and does not demand HEAD == State implementation. HEAD is checked only through the
`agent_tool.verify_current_stage_basis` facade (42-50).

### 3.2 PREARCH DM022 record and its refs

The same checkpoint file is referenced by all three State provenance roles. Its expected SHA
comes from the State triplet. `load_typed_checkpoint_record` reads it and validates the DM022
schema, kind/reason/operation/producer boundary/checkpoint set/four artifact names/self
digest (`survey_research_authority_v2.py:329-373`).

| Record field | Typed shape | Path relationship | Actual bytes consumed? |
|---|---|---|---|
| `artifacts[].{name,path,sha256}` | NamedRef x4 | names exactly `evidence-acceptance`, `edition-views-acceptance`, `materiality-ledger`, `profile-completeness` | yes; each file read/hashed in `_load_typed_four_refs` 476-494 |
| `profile.{path,sha256}` | ArtifactRef | checkpoint profile file | yes; read/hashed 514-520 |
| `request.{path,sha256,byte_count}` | SizedRef | revision request file | yes; 837-846; reread by `derive_ordinary_root_effective_context` via `load_revision_request` |
| `retention_plan.{path,sha256,byte_count}` | SizedRef | retention/plan JSON | yes; read/hash 868-870 and reread 901-903. The path may be the same file as `revision_root/retention/inventory.json`; when it is, this SizedRef can externally bind that inventory path/SHA. Equality of the two paths is not enforced by the readback, so do not claim the inventory is universally unpinned |
| `report.{path,sha256,byte_count}` | SizedRef | pre-adoption report | yes; report read by `resolve_research_authority` 1181-1187 and `check_supersession_record_from_paths` 3891-3899 |
| `proof.{path,sha256,byte_count}` | SizedRef | proof file | no in the existing selection readback; SHA only cross-bound to report fields 1189-1191 and 3906-3908 |
| `decision.{path,sha256,byte_count}` | SizedRef | decision file | no in the existing selection readback; SHA-only cross-binding |
| `reviews[0].result.{path,sha256,byte_count}` | SizedRef | proof result | no bytes read by these selection readback paths; shape checked 630-644 and 248-259; the detached supersession checker does not open it |
| `before_state.{path,sha256,byte_count}` | SizedRef | logical canonical State path | path/length/SHA used; actual bytes read at `revision_root/retention/state-before.json` (918-925, 1054-1063) |
| `before_checkpoint.{evidence,materiality,completeness}` | ArtifactRef x3 | identity only | no direct file read; request.before_checkpoint is compared to COPY-State provenance in `_context_from_before_state` 1753-1764 |
| `parent_checkpoint`, `original_anchor` | ArtifactRef | lineage only | no file read |
| `supersedes[]` | `{path,sha256,revision_id}` | lineage only | no file read |
| `revision_root` | safe path prefix | manifest/copy/inventory/completion location | no own bytes |
| `contract` / `implementation.repository_commit_sha` | Contract8 / SHA | own epoch | used by `_verify_own_epoch_commit` 655-799 |
| `reviews[0]` review id/kind/status | DATA | proof semantics | no proof file read |

Field relationships actually enforced in this path:

- checkpoint.request == manifest.request;
- manifest.before_state.sha == checkpoint.before_state.sha;
- manifest.before_checkpoint == request.before_checkpoint;
- manifest.revision_root == checkpoint.revision_root;
- retained COPY bytes == checkpoint.before_state.sha/len AND request.before_state.sha/len
  (the same copy is checked against both, so those two declared hashes must agree in bytes);
- request.before_state.path equals the Profile/config-derived canonical logical State path;
- request.profile_ref, request.discovery_ref, request.screening_ref are file-read/hash-bound.

Relationships not enforced by this path:

- `record.profile` vs `request.profile_ref`;
- `manifest.profile_ref/discovery_ref/screening_ref` vs request refs;
- `manifest.candidate_outputs` vs actual files;
- `report.proposed_artifacts` vs checkpoint artifacts;
- `record.before_checkpoint` vs request/manifest (request <-> manifest <-> COPY-State
  provenance are tied, but the record field itself is not separately compared);
- `record.retention_plan.path` vs `revision_root/retention/inventory.json` (may coincide, but
  the code does not demand equality).

### 3.3 DM022 request, manifest, report

- Request required shape is in `schemas/dm022-revision-request-v2.schema.json`: `before_state`
  SizedRef, `before_checkpoint` three ArtifactRefs, `profile_ref`/`discovery_ref`/
  `screening_ref` SizedRefs, `supplement_manifest` null/SizedRef, `records`, `completeness`,
  `work`, `tool_pins`, `runner`, `executor`.
- `request.profile_ref` is bytes-consumed (`_bind_profile_and_canonical` 1703-1732; request
  schema 2258).
- `request.discovery_ref` must resolve to the effective Discovery path and SHA
  (`_derive_root_effective_kernel` 1632-1644).
- `request.screening_ref` must equal the SCP `screening-acceptance` path plus SHA
  (1645-1651).
- `request.before_state` bytes come from the retained COPY; the request path must equal the
  derived canonical State path, and LOW refuses supplying the LIVE canonical path as the COPY
  (`derive_ordinary_root_effective_context` 1884-1908).
- `request.supplement_manifest`, `request.records`, `request.completeness`, `request.work`,
  `request.tool_pins`, `request.runner`, `request.executor`, `request.affected_ids`:
  DATA-only for this Selection readback; no file is enumerated from them here.
- Manifest path is `revision_root/revision-manifest.json`. There is no direct declared SHA
  for it in the checkpoint. `_verify_adopted_graph_full` reads/parses it (871-885), then
  binds request/before and compares retention rows. `resolve_research_authority` later binds
  `report.manifest` SHA to the actual manifest bytes (1194-1197); the detached supersession
  checker does the same (3911-3920). `candidate_outputs` is not read by either path.
- Report is read/hashed and schema-checked. Only `report.proof/decision/request/
  before_state/manifest` are cross-bound. `proposed_artifacts`, `operation`,
  `producer_boundary`, `affected_ids`, `mechanical_projections`, and `work_ref` are not
  independently re-derived by these selection reads.

### 3.4 Legacy DCP / SCP

`_context_from_before_state` reads both typed checkpoint files (SHA from State provenance),
requires LEGACY family (1775-1789), then:

- `_validate_legacy_dcp_scp` 1459-1507:
  - issue_id, producer pair from current config `stage_plan`, checkpoint membership;
  - all `artifacts[]` NamedRefs file-rehashed; exactly one expected role artifact;
  - `_rehash_deterministic_reviews` 1325-1379 reads/hashes every deterministic review result;
  - `_validate_legacy_stage_report` 1382-1456 reads the CORE report: exact 12 keys,
    issue/from/to, Profile `{path,sha256}`, `production_state.path` only (no live SHA),
    record-owned contract, record-owned implementation, exact artifact map equality.
- DCP `discovery-acceptance` artifact path -> Discovery acceptance; SCP
  `screening-acceptance` artifact path -> Screening acceptance.
- These legacy paths do not perform Git own-epoch object proof; that is PREARCH-only via
  `_verify_own_epoch_commit`.

### 3.5 Discovery / X / root / effective / collector / session-root

`discovery.validate_acceptance` 274-298:

- reads Discovery acceptance through schema `schemas/discovery-acceptance-v2.schema.json`;
- `x_source_intake.path` file read/hash against `x_source_intake.sha256`;
- current config load;
- `x_intake.validate_manifest` 344-396:
  - X manifest schema `schemas/x-source-intake-v2.schema.json`;
  - X `production_profile.path` file read/hash;
  - Profile read/parse again through `_profile` 56-62;
  - every `runs[].task.path` file read/hash;
  - every `runs[].result.raw.path` file read/hash/size (`_validate_raw_ref` 305-312);
  - current config `external_source_intake.x_grok` policy/category checks;
- Discovery JSONL path read/hash; `read_jsonl`; `_normalize_record` re-reads/hashes every
  `source.raw_paths` raw;
- graph/X integration over DATA fields; accepted payload compared to recomputed records.

`collector_id`, `collector_run_id`, `locator`, and `source_type` are DATA-only. No collector
config or collector-run file is consumed.

Effective Discovery:

- derived `basis.discovery_path` read/hash plus `read_jsonl` plus `validate_discovery_set`
  (1436-1463);
- root accepted JSONL read through DCP acceptance; root records passed from
  `_context_from_before_state`;
- derived != root -> `validate_discovery_expansion` 246-325: parent closure, source identity,
  obligation union, and child Raw path existence via `_repo_file` (297-298). It does not
  re-hash child Raw bytes; expansion constrains child Raw paths to the parent Raw union, which
  is why root Raw hashing is the byte authority.

Session-root terminology: the in-memory `root_records`/`root_path` passed to the `_content`
validators is the "session root" context. No `sessions/*.md`, execution index, collector
session, or P3S `_Session` material is read by this Selection path. Explicitly: "session-root"
here does NOT mean session files.

### 3.6 Screening closure

| Object | Existing expected pin / relationship | Consumer |
|---|---|---|
| `screening-acceptance` | path from SCP artifact; SHA from SCP NamedRef; parent dir name equals `result_set_sha256` | `validate_acceptance` / `_validate_screening_acceptance_content` |
| `package.json` | SHA must equal acceptance `package_sha256` | 1512-1515, 1924-1927 |
| `input/batches/*.jsonl` | exact directory set; each SHA from `package.input.batches[].sha256`; content read/parsed | `_check_screening_batches_and_digest` 1394-1433 |
| `results/*.json` | exact directory set; each SHA from acceptance `batches[].result_sha256`; basis hashes checked | same |
| `basis.profile_path` | file SHA from package; Profile read for identity | `_validate_screening_package_basis_content` 1281-1319 |
| `basis.discovery_path` | file SHA from package | same |
| `prompt.path` | `config/prompts/source-screening-v2.md`; SHA from package | `_check_screening_package_files_content` 1256-1278 |
| `result_contract.path` | `schemas/screening-v2-batch-result.schema.json`; SHA from package | same |
| archived `screening-accepted.json` | if present, package/batch/result SHAs rechecked | `_validate_archived_screening_files` 1233-1253 |
| `basis.state_path` | content: path identity only; LIVE: file SHA and State validation | content 1304-1305; live 1322-1338 |
| effective Discovery | derived JSONL read/hash; expansion check; no derived-Raw byte rehash | `_resolve_effective_discovery_basis_content` 1436-1483 |
| LIVE State-bound root | `_canonical_root_acceptance` loads `package.basis.state_path` -> State -> Profile -> `source_root/discovery/discovery-accepted-v2.json`; if absent returns `source_root/discovery/discovery-v2.jsonl` with `acceptance_marker=None` (DIRECT fallback) | 945-970; `resolve_effective_discovery_basis` 973-1059 |

### 3.7 Evidence / Views / Supplement / Ledger / Completeness

Evidence acceptance package closure:

- `evidence-accepted.json`: read/pin; exact field set; parent dir name equals
  `result_set_sha256`; `package_sha256` binds package copy; `screening_acceptance_sha256`
  binds package basis (1738-1793, 1621-1695).
- `package.json`: read/pin/SHA equal to acceptance package SHA; `basis.profile_path`,
  `basis.discovery_path`, `basis.screening_acceptance_path` each read/hashed
  (`_check_evidence_package_files_content` 1036-1071).
- `prompt.path` = `config/prompts/evidence-verification-v2.md`; read/hashed.
- `contracts.run_package/task/card` are Evidence package/task/card schemas; read/hashed;
  `contracts.supplement` when present is the supplement schema; read/hashed.
- `tasks[]`: `{evidence_task_id,path,sha256,discovery_ids[,authority_supplement_source_ids]}`;
  exact `tasks/` set via `_exact_regular_files`; each file read/hash/parse; filename equals
  `task_filename`; `_validate_task` 989-1021.
- `results/*` (Evidence cards): exact `results/` set using task basenames; acceptance
  `results[].sha256`/`filename` and task metadata SHA bind; each file read/hash/parse;
  `_validate_card_core` 1270-1461.
- `views/*` (Edition Views): exact `views/` set using `view_filename(task_id)`; each row
  `view_sha256` from views acceptance; each file read/hash/parse; `validate_edition_view`
  2018-2072.
- Supplement (if `package.authority_supplement`): manifest path/SHA from package field;
  schema `schemas/evidence-authority-supplement-v2.schema.json`; manifest
  `basis.source_root` directory, `basis.discovery_path`, `basis.screening_acceptance_path`
  read/hash; every `sources[].raw_path` read/hash/byte_count and containment under
  `source_root`; source IDs/task bindings/source_class/timestamps checked
  (`_resolve_phase_supplement_context` 300-386; `validate_evidence_authority_supplement`
  523-635; `_supplement_source_file` 497-520).
- Supplement context rechecks all declared Raw refs on every phase/readback
  (`_recheck_supplement_context` 389-424), not a task subset.
- Evidence card source validation uses Task `source_records` (DATA) and supplement entries;
  it does not re-read Discovery Raw bodies.

Ledger / Completeness:

- Paths come from PREARCH `artifacts` NamedRefs; SHA from each NamedRef.
  `_load_typed_four_refs` and `_verify_adopted_graph_full` read/hash them.
- Ledger `basis` recomputes SHA256 of Profile, Discovery effective, Screening acceptance,
  Evidence acceptance, Views acceptance, plus Evidence/View result-set digests; rows link
  exactly one per Discovery/task (`_check_ledger_rows_content` 2657-2722).
- Completeness `basis` recomputes Profile plus Ledger SHA; obligations/closure checked;
  `_check_profile_completeness_extra_content` rereads the Discovery JSONL, Profile, and
  Ledger (50-78, 145-238, 241-262).
- The Profile file is read multiple times through separate refs (checkpoint artifact profile,
  request profile, State profile, content validators); equality among all three refs is not
  universally enforced (see section 7).

### 3.8 Outputs / seven owned slots / return

Seven slots (`run_selection...:294-300`, `DM022_SEVEN_SLOTS`):

```
candidate-matrix-v2.json
candidate-selection-v2.json
architecture-v2.json
architecture-review-summary-v2.json
architecture-review-attention-v2.json
orchestration/v2/interactive/selection-architecture-input.json
orchestration/v2/interactive/selection-architecture-audit.json
```

- Before any write: `_dm022_preflight_seven` lstat all seven and refuses any present or
  nonregular slot (101-114, 304).
- Each write is preceded by `_dm022_require_ready` and per-path `exists()/is_symlink()`
  refusal; writes at 319, 365, 430, 443, 447-448, 454, 459-471.
- `review_attention.build_attention` reads Screening acceptance, Ledger, Selection; writes
  attention; basis stores their SHAs (32-143). `validate_attention` re-hashes those three
  paths from its basis (146-159).
- Audit binds archive input plus five output SHAs (462-469), not its own SHA.
- Outer return 472-481 returns only relative paths/counts/readiness. It does not re-hash the
  seven outputs. The last `_dm022_require_ready` is before the audit write (456); there is no
  post-audit freshness check or output-SHA return binding.

---

## 4. Actual bytes vs DATA-only vs proposed freshness pins

This section separates three different things. Nothing here is a new authority or an
implementation decision.

### 4.1 Actual bytes consumed by existing code

- LIVE State file; Profile file; State/Profile schemas; config; legacy compatibility file.
- State-referenced PREARCH checkpoint; its four artifact files; checkpoint Profile; request;
  retention payload (and inventory if same path); report; revision manifest; retained
  `state-before.json`; cleanup completion; owner-epoch Git objects.
- Legacy DCP/SCP checkpoint records; their artifacts and deterministic review results; their
  CORE reports.
- Discovery acceptance; X manifest; X task files; X result Raw files; Discovery JSONL; every
  normalized Discovery `source.raw_paths` Raw; accepted root JSONL.
- Screening acceptance; package copy; exact input batches; exact result batches; prompt;
  result schema; basis Profile/Discovery; effective derived Discovery JSONL; accepted root
  Discovery.
- Evidence acceptance; package copy; basis Profile/Discovery/Screening acceptance; prompt;
  package/task/card/supplement schemas; every task file; every result/card file; every View
  file; supplement manifest; supplement basis Discovery/Screening acceptance; every declared
  supplement Raw.
- Ledger; completeness; Profile again; Discovery JSONL again; completion receipt; retention
  inventory.
- Reference-attention inputs: Screening acceptance, ledger, selection, attention schema.

### 4.2 DATA-only fields / paths in existing code

- `state.history`, `state.contract`, `state.implementation` (content checks only; no current
  Contract8 recompute and no HEAD equality in the content path).
- Checkpoint `parent_checkpoint`, `original_anchor`, `supersedes`, `summary`, `executor`,
  review id/kind/status (no external file read).
- Checkpoint `proof` and `decision`, and `reviews[0].result` in the selection readback:
  shape and SHA-only cross-binding; their bytes are not opened by the selection readback
  paths. This is a material source observation, not an audited global defect claim.
- Request `records`, `completeness`, `work`, `tool_pins`, `runner`, `executor`,
  `affected_ids`, `supplement_manifest` (DATA-only in this readback path).
- Manifest `profile_ref`, `discovery_ref`, `screening_ref`, `candidate_outputs`, `work`
  (DATA-only or schema-only; manifest profile/discovery/screening refs are not compared to
  request refs).
- Report `proposed_artifacts`, `operation`, `producer_boundary`, `affected_ids`,
  `mechanical_projections`, `work_ref` (DATA-only; not re-derived by the selection readback
  shown here).
- Collector identity/locator fields; Task `source_records`; card/View textual fields; ledger
  row rationale; completeness obligation text; retention row `accepted_bound`/`gate_bound`
  fields.
- Derived/effective Discovery child Raw paths: path existence/containment only during
  expansion; bytes are not re-hashed by Screening content.
- Execution/session files: not read. The "session root" is only the in-memory
  `root_records`/`root_path` for the content cores.

### 4.3 Proposed freshness-pin candidates (NOT existing code, NOT authorization)

These are candidate expected pins for a future pre-capture/freshness design. They are
analysis only and do not imply a new module, schema, family, global cache, context variable,
public flag, or verified dict.

- LIVE State file; State-bound Profile file; current config; current tool schema files.
- State-referenced PREARCH checkpoint; four artifacts; checkpoint Profile; request; retention
  payload; report; manifest; retained COPY; inventory; completion receipt.
- DCP/SCP checkpoint files; their artifacts; deterministic review results; CORE reports.
- Discovery acceptance; X manifest; X tasks/Raws; Discovery JSONL; root Raw closure;
  accepted root JSONL.
- Screening acceptance; package; input batches; result batches; prompt; result schema; basis
  Profile/Discovery; effective derived Discovery JSONL; accepted root Discovery.
- Evidence acceptance; package; basis files; prompt; contract schemas; tasks; results/cards;
  Views; supplement manifest/basis/Raws.
- Ledger; completeness; seven output slots after each write and at outer return.
- The existing external refs that already bind these are preferred over invented pins:
  State artifact SHAs, DCP/SCP NamedRefs, Discovery acceptance `x_source_intake.sha256` and
  `discovery_sha256`, Screening acceptance/package/batch/result SHAs, Evidence
  acceptance/package/task/result/view SHAs, checkpoint `request`/`retention_plan`/`report`
  SizedRefs, manifest `report.manifest`/retention rows, and the own-epoch Git object pins.
- `record.retention_plan` is a SizedRef and may bind the same file as
  `revision_root/retention/inventory.json`. If the paths coincide, that record ref can be an
  external SHA for the inventory. If they do not coincide, the current code compares content
  only. A proposed pin set must not assert a universal "inventory has no external SHA"
  statement without checking this path relationship.

---

## 5. Static multiplicity estimates (source/call-graph only)

`_verify_adopted_graph_full` (802-993) does entry typed loading, four artifact loads, Profile
read, request read/schema, request Profile/Discovery/Screening checks, manifest read/schema,
COPY read, retention read, `derive_ordinary_root_effective_context`, full Evidence/Views/
Ledger/Completeness content, and `_verify_own_epoch_commit`.

`derive_ordinary_root_effective_context` calls `discovery.validate_acceptance` twice (context
1836 and kernel 1575), loads DCP/SCP records, DCP/SCP reports, all DCP/SCP artifact files,
deterministic review results, config twice through producer checks, and Screening content.

Within one adopted-graph traversal, static nesting estimates are approximately:

- `_validate_evidence_acceptance_content`: 6 calls (direct, Views top, Ledger top, Views via
  Ledger, Completeness via Ledger, Views via Completeness via Ledger).
- `_validate_edition_views_acceptance_content`: 3 calls (direct, Ledger top, Completeness via
  Ledger).
- `_validate_materiality_ledger_content`: 2 calls (direct, Completeness).
- `screening._validate_screening_acceptance_content`: about 9 calls (one explicit kernel,
  one Ledger direct, one Completeness-Ledger, six from Evidence acceptance).
- `_resolve_effective_discovery_basis_content`: about 10 calls (one per Screening content
  plus the explicit kernel).
- supplement context and full Raw recheck: once per Evidence acceptance (about 6).
- Discovery acceptance/Raw normalization: 2 per `derive_ordinary`, each re-reading X
  manifest/config/Profile/task/Raw and all root Raw.
- Git own-epoch batch: once per adopted graph.

Runner-level static estimates:

- `agent.validate_agent_state` on the PREARCH State calls the PREARCH content and proof path
  for three checkpoints; each proof call enters `check_supersession_record_from_paths` ->
  `_verify_adopted_graph_full` once. This is about 3 full adopted traversals per strictState,
  plus legacy DCP/SCP validation.
- `_verify_completion_full` calls `_verify_adopted_graph_full` twice (1018 and 1073), plus
  LIVE State and slot checks.
- `_dm022_require_ready` is called 8 times at 260, 316, 362, 427, 440, 444, 451, 456; each
  invokes one completion -> two adopted traversals.
- Initial flow calls `resolve_research_authority` twice (264/271), each with an adopted
  traversal, plus strictState at 249 and `resolve_active_screening_acceptance` (which enters
  strictState through checkpoint resolution and again through the overridden package-basis
  verifier).
- `derive_candidate_matrix` at 310 and `build_architecture_review_summary` at 433 use LIVE
  `_load_upstream`; summary does `_load_upstream` at 866 plus `validate_candidate_matrix` ->
  `derive_candidate_matrix` -> `_load_upstream` at 373, i.e. two more full upstream
  closures. Each `validate_package_basis`/`validate_evidence_package_basis` under the override
  re-enters `verify_current_stage_basis` -> strictState.

These are source/call-graph estimates only. No measured count, wall time, CPU, `rchar`, or
speedup is claimed.

---

## 6. Existing builders and retained full classes available for reuse

Pin/freshness helpers:

- `survey_evidence_v2._capture_phase_pins(paths)` 232-246
- `_recheck_phase_pins(pins)` 249-256
- `_load_pinned_json(pin)` 259-277
- `_assert_pin_repo_ancestors(repo_root, pin)` 280-297
- `_finish_authority_phase(repo_root, ctx, pins, *, revalidate_owner)` 427-450
- `_resolve_phase_supplement_context(...)` 300-386 and
  `_recheck_supplement_context(...)` 389-424
- `_exact_regular_files(directory, expected, label)` in Evidence 738-753; semantically
  identical Screening private helper 99-113
- LOW `_sized_ref_shape` / `_artifact_ref_shape` / `_named_ref_shape` 263-294,
  `_verify_sized_ref_bytes` 297-307, `_repo_rel` 127-135, `_safe_read_bytes` 147-187,
  `_lstat_one` 138-144

Full validation classes:

- `low._verify_adopted_graph_full` 802-993
- `low._verify_completion_full` 996-1125
- `low.resolve_research_authority` 1128-1228
- `low._verify_own_epoch_commit` 639-799
- `low.require_research_operation_ready` 4087-4140
- `agent.validate_agent_state` 919-921 -> 924-1070
- `agent._validate_prearchitecture_core_proof` 290-321
- `agent._resolve_prearchitecture_artifact` 1073-1146
- `agent.resolve_checkpoint_artifact` 1149-1326
- `agent_tool.verify_current_stage_basis` 42-50
- `agent_tool._historical_state_basis_wrapper` 53-98
- `agent_tool.current_stage_basis_override` 121-143

Content cores already shared:

- `discovery.validate_acceptance` 274-298; `_normalize_record` 84-153
- `screening.resolve_effective_discovery_basis` 973-1059;
  `_validate_screening_acceptance_content` 1486-1521;
  `_resolve_effective_discovery_basis_content` 1436-1483
- `evidence._validate_evidence_acceptance_content` 1738-1793;
  `_validate_edition_views_acceptance_content` 1856-1893;
  `_validate_materiality_ledger_content` 2724-2767;
  `_check_evidence_acceptance_results_with_context` 1621-1695
- `completeness._validate_profile_completeness_content` 241-262
- `architecture_v2_base._load_upstream_content` 85-152;
  `_derive_matrix_rows_content` 183-276

Enumeration status: no single existing function enumerates the entire transitive closure
(DCP/SCP artifacts/reports -> Discovery/X/root Raw -> Screening batches/results/effective ->
Evidence package/tasks/cards/Views/supplement -> Ledger/Completeness -> request/manifest/
report/COPY/retention/completion). Enumeration is distributed across the content validators
and exact-directory helpers. If enumeration is expensive, retain the existing full classes
rather than adding a mirrored validator or a global/epoch cache. The proposed pin candidates
in section 4.3 are not existing behavior.

---

## 7. Observations, uncertainties, and phrase corrections

1. Discovery Raw exists independently of Evidence supplement. The R2 review inference is
   retracted; root §4.1 is confirmed.
2. Proof and decision bytes are not opened by the existing Selection readback paths, despite
   comments at `resolve_research_authority` 1179-1201 and
   `check_supersession_record_from_paths` 3856-3864 referring to report/proof/decision
   reloads. Only SHA fields are cross-bound. This is a material source observation about the
   existing readback, not an audited global defect claim and not a claim that the broader
   DM022 lifecycle lacks proof validation.
3. `record.profile`, `request.profile_ref`, and manifest profile/discovery/screening refs are
   not all cross-equal. Four-ref loading uses `record.profile`; content uses
   `request.profile_ref`; manifest refs are schema-only. `_verify_own_epoch_commit` uses
   `request.profile_ref` for the committed Profile. This relationship is not enforced by the
   selection readback.
4. Manifest `candidate_outputs`, report `proposed_artifacts`, and report
   `operation`/`producer_boundary`/`affected_ids`/`mechanical_projections` are DATA-only in
   this readback; they are not file-enumerated or re-derived here.
5. There is no direct declared SHA for the revision manifest in the checkpoint. Binding is
   through `report.manifest` in `resolve_research_authority` and the detached supersession
   checker; completion-only readiness does not read the report, so it binds manifest through
   request/before/retention-row comparisons rather than a whole-file SHA.
6. There is no direct external SHA for the LIVE State file, `retention/inventory.json`, or
   `cleanup-completion.json` in these readback paths; they are content-validated. Exception:
   `record.retention_plan` is a SizedRef and may point to the same file as
   `revision_root/retention/inventory.json`; if the paths coincide, that SizedRef can
   externally bind the inventory path/SHA. The code does not enforce path equality, so do not
   assert a universal "inventory is unpinned" statement.
7. Derived/effective Discovery Raw bytes are not re-hashed by Screening content; root Raw is
   hashed through Discovery normalization, while expansion checks derived Raw path
   existence/containment. Supplement Raw and X Raw are separately hashed.
8. Outer return has no output SHA binding (472-481). The audit hashes five outputs plus the
   archive before return, but not itself, and there is no post-audit `_dm022_require_ready`.
9. No execution/session file is consumed by Selection. The "session-root" is the in-memory
   `root_records`/`root_path` passed to the content cores. This is explicit, not a session
   file path.
10. Legacy DCP/SCP implementation identity is record-owned only; no Git own-epoch object check
    occurs on that branch. PREARCH is the only branch with `_verify_own_epoch_commit`.
11. `_verify_adopted_graph_full` has no final whole-closure pin recheck. Its nested content
    helpers recheck their own subclosures, and `resolve_research_authority` rechecks State and
    the checkpoint file after the full traversal. `_verify_completion_full` re-runs the
    adopted graph twice but does not bind every material byte to one pre-captured set.
12. `_dm022_require_ready` is called before each write but not after the final audit write;
    no end-to-end output freshness window exists in the runner.

---

## 8. Explicit no-runtime-proof statement

This inventory is source-grounded analysis only. No project source was imported or executed,
no tests or fixtures ran, no Git history/HEAD/status was inspected, no network was used, and
no active, shadow, proof, State, Profile, output, or source file was written. The only writes
from this action are these two NEW files in the packet. Any future implementation, pin
capture, or freshness behavior requires separate root/independent confirmation and real
runtime evidence; nothing here constitutes such evidence or authority.
