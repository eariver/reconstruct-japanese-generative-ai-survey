# Detached ROOT/EFFECTIVE context map — hardest missing piece (LOW rootloader, no code)

2026-10-31. Pre-code author ONLY. No runtime/import/test/build/fixture/network/Git/readback.
Text-read final133 `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(actual409/tree8ce +133paths54M79A/768). Decision FULL `62b14add…/20472B` §§6–7,
ROOT `021a0d7c…/7225B` §5 control. Prior R3 claimed pure chain still calls public
`Screening.validate_acceptance` / `resolve_effective_discovery_basis` and lacks
ordinary Discovery-CP actual proof → NOT_READY B1/B9 preserved. This file maps ONLY
the true R/E LOW rootloader. No new module/schema/family, no DM022 7-shape change,
no ordinary 3/5 applied HIGH.

## 1. Authority predicates reused (no invention)

- State/Profile bindings: `schemas/survey-production-state.schema.json`,
  `schemas/survey-production-profile.schema.json`,
  `config/survey-production-v2.json:281-302` stage_plan:
  `ISSUE_INITIALIZED{checkpoints:[discovery],next:DISCOVERY_COLLECTED}`,
  `DISCOVERY_COLLECTED{checkpoints:[screening],next:CANDIDATES_NORMALIZED}`.
  Producer lookup `survey_agent_control_v2.py:588-592` `_producer_for_checkpoint`.
- Checkpoint envelope: `schemas/stage-checkpoint-v2.schema.json:7-18,94-107`
  (11 top keys, `from_state/to_state/checkpoints/artifacts/reviews`,
  per-`from_state` artifact gates `192-199` discovery-acceptance,
  `196-198` screening-acceptance, `136-171` CORE_STAGE_CONTRACT contains).
- Agent historic predicates (read-only, no call):
  `_validate_checkpoint_record:770-904`: ArtifactRef `{path,sha256}` shape+live rehash
  `:772-776`; typed dispatch PREARCH vs LEGACY `:777-814` (PREARCH refused at legacy path
  `:811-812`); producer `:815-818`; `issue_id` `:819-820`; `from/to` `:821-822`;
  `checkpoint in record.checkpoints` `:823-824`; per-artifact rehash `:865-877`
  (superseded map only for versioned/prior `:825-864`); deterministic review rehash
  `:878-890`; historic `_validate_core_stage_report` `:891-904` with
  `expected_contract=record.contract`, `expected_implementation_sha=record.implementation.repository_commit_sha`;
  FROZEN reconciliation `:905-916`.
- `_validate_core_stage_report:605-731`: PREARCH branch `:619-664` distinct;
  legacy requires exactly one `CORE_STAGE_CONTRACT` DETERMINISTIC PASS `:665-670`;
  result ref `{path,sha256}` 2-key `:671-673` + drift `:674-679`; report exact
  **12 keys** (not 13 — actual count `:680-686`:
  `schema_version,check_id,status,issue_id,from_state,to_state,production_state,`
  `production_profile,implementation_commit_sha,contract,artifacts,recorded_at`);
  `2.0-rc1/CORE_STAGE_CONTRACT/PASS` `:687-688`; lifecycle/issue/from/to vs
  `historical_state.lifecycle_state=from_state` `:689-697`; `production_profile`
  `=={path:_rel(profile_path),sha256:sha256_file}` `:698-701`;
  `production_state`: if `state_path is not None` live `{path,sha256}` equality
  `:705-708`, else historical canonical-path-only `:710-712`
  (`profile.parent/authoritative_filename`, **no live SHA** — preserve exactly);
  `contract==expected_contract` `:713-717`
  (`core.contract_identity:210-228`); `implementation_commit_sha` `:718-722`;
  `recorded_at` parse `:723-726`; artifact map equality
  `_artifact_map(report.artifacts)==_artifact_map(record.artifacts)` `:727-731`.
- Ordinary historic validator does NOT recompute Git tool blobs. Own-epoch
  recorded-commit proof (`survey_research_authority_v2.py:620-780`
  `_verify_own_epoch_commit`, 7-file `_MAPPED_DM022_CODESET:568-580`) is
  PREARCH-only (`_verify_adopted_graph_full:783-911`, `check_supersession:2401-2513`,
  agent PREARCH branch `:784-805,:290-321`). Do not retrofit onto ordinary DCP/SCP.
  No new historical requirement, no source-schema invention.

## 2. State-free status (verified, no hidden Current checks)

- `survey_discovery_v2.validate_acceptance:274-298` is state-free and MAY be used:
  `load_and_validate_json` vs `DISCOVERY_ACCEPTANCE_SCHEMA`; `x_ref` SHA drift
  `:279-281`; `cfg=load_json(DEFAULT_CONFIG)` from disk (policy/drive only);
  `x_intake.validate_manifest(repo_root,cfg,…require_complete=True)` `:283`
  (itself state-free `:344-398`, never `verify_state_basis`/checkpoint/pending);
  issue match `:284-285`; `discovery_path` SHA `:286-288`;
  `read_jsonl+_normalize_record:84-153` per record (origin/research_pass/parent_refs/
  obligations/raw_paths/collector/locator, `raw_refs{path,sha256,byte_count}` via
  `_safe_repo_file:43-55`); `_validate_graph:156-172` (dup + dangling + pass order);
  `_validate_x_integration:179-201`; `record_count/records/graph_sha` equality
  `:294-297`. No State load, no `verify_state_basis`, no `agent.*`, no HEAD.
- `survey_screening_v2.validate_acceptance:897-916` is NOT state-free and MUST NOT
  be used in claimed pure chain: calls `validate_package_basis:695-711`
  (loads State, `sha256(state)==basis.state_sha256`, `verify_state_basis:959-995`,
  identity divergence) + `resolve_effective_discovery_basis:353-439`
  (via `_canonical_root_acceptance:325-350` which `load_json(basis.state_path)` LIVE
  + derives `source_root` from live Profile). Same for `resolve_active_screening_acceptance:442-489`
  (`agent.resolve_checkpoint_artifact` + `verify_state_basis` + override).
- Use CONTENT siblings only (explicit `expectations`, no State):
  `_validate_screening_package_basis_content:654-693` (§11.3 path-identity
  `basis.state_path==canonical_state_path`, file SHA drift, profile-identity via file
  never live State, never `verify_state_basis`, never SHA-compare live/retained);
  `_check_screening_package_files_content:629-651`;
  `_check_screening_batches_and_digest:767-806` (pure batch/count/digest,
  `run_dir.name==digest`); `_resolve_effective_discovery_basis_content:809-856`
  (pure `validate_discovery_set` + `validate_discovery_expansion:243-322` only,
  never `_canonical_root_acceptance`, never checkpoint/override);
  `_validate_screening_acceptance_content:859-894`
  (`expectations={issue_id,research_profile,canonical_state_path}`, package copy
  `==package_sha256`, basis content, identity, batches/digest, pure effective basis).
  Full archived batch digest + `source_root` strict proof preserved via
  `_exact_regular_files:96-110` + `_validate_result_batch:714-754` + digest
  `_result_set_digest:757-764`.
- S1 prepackage-before-COPY separate loader stays in Screening (`prepare_package:492-567`
  uses LIVE `state_path` + `verify_state_basis` caller-checked facade). LOW history
  public path MUST NOT use `_canonical_root_acceptance` because it reads LIVE.

## 3. New helpers — PATHS-only, no LIVE/agent/PREARCH-validator/future-COPY

### 3.1 Public LOW (history, COPY-only)

```python
def derive_ordinary_root_effective_context(
    repo_root: Path, request_path: Path, before_copy_path: Path
) -> dict[str, Any]
```

Top-level imports unchanged (`survey_research_authority_v2.py:21-35`: only
`core` shape-only + `schema_gate` + stdlib; all evidence/screening/completeness
function-local, exact signatures, no `run_evidence_v2_interactive` (top pulls
agent/tool + circular LOW), no `agent/survey_agent_control_v2/survey_agent_tool_v2/
verify_state_basis/human_gate/bridge/renewal/editorial/publication_set/guard-coordinator`).
No new module; factor pure primitive into existing LOW/Screening if needed
(e.g. reuse `_check_screening_batches_and_digest`,
`_resolve_effective_discovery_basis_content` as-is, no copy drift).

Algorithm (all path reloads via `_safe_read_bytes:128-168` O_NOFOLLOW+lstat/fstat/inode
+ `_strict_parse_object:171-178` + `schema_gate.validate_instance`, `_repo_rel:108-116`,
`_sized_ref_shape:244-254`, `_artifact_ref_shape:256-264`, `_verify_sized_ref_bytes:278-288`):

1. `request=load_revision_request(repo_root,request_path)` (`1149-1162`,
   `DM022_REQUEST_SCHEMA`). `before_ref=_sized_ref_shape(request.before_state)`.
2. `copy_raw=_safe_read_bytes(before_copy)`, require
   `sha256==before_ref.sha256` + `len==byte_count` (cf. `derive_before_context:1197-1203`).
   `before_state=_strict_parse_object(copy_raw)`; validate State/Profile shapes via
   `STATE_SCHEMA`/`survey-production-profile.schema.json` bindings (shape only,
   no `verify_state_basis`, no `agent.validate_agent_state`).
3. `before_checkpoint=request.before_checkpoint{evidence,materiality,completeness}`
   must equal `COPY.checkpoint_provenance{evidence,materiality,completeness}`
   ArtifactRef-wise (cf. `:1207-1215`). `canonical_state_path=request.before_state.path`
   (pinned logical path, preserved; no caller cfg/dict flag).
4. `DCP_ref=COPY.checkpoint_provenance.discovery`,
   `SCP_ref=COPY.checkpoint_provenance.screening`; both must be `{path,sha256}`
   (else refuse — DM022 strict `EVIDENCE_REVIEWED` before-State always passed D/S,
   so FULL CP must exist; **no initial fallback**, no schema fallback, no caller Scan
   marker/prov reinterpretation).
5. Load DCP/SCP record files + `sha256==provenance.sha`. Dispatch via
   `load_typed_checkpoint_record:310-355`. If `family==PREARCH` refuse
   `DM022_WRONG_FAMILY` (root DCP/SCP may be LEGACY only; PREARCH roles are
   `evidence/materiality/completeness` only). Unknown kind refuses.
6. Validate DCP record LEGACY: schema `OLD_CHECKPOINT_SCHEMA`,
   `issue_id==COPY.issue_id`, producer `==_producer_for_checkpoint(cfg,disc)=
   (ISSUE_INITIALIZED,DISCOVERY_COLLECTED)` (cfg read from disk for stage_plan only,
   not authority), `"discovery" in checkpoints`, artifacts contain exactly one
   `discovery-acceptance` NamedRef, reviews exactly one `CORE_STAGE_CONTRACT`
   DETERMINISTIC PASS with result `{path,sha256}` rehashed, then historic
   `_validate_core_stage_report` predicates with `state_path=None`
   (canonical-path-only `:710-712`), `expected_contract=record.contract`,
   `expected_implementation_sha=record.implementation.repository_commit_sha`.
   Same for SCP with producer `(DISCOVERY_COLLECTED,CANDIDATES_NORMALIZED)`,
   artifact `screening-acceptance`. No `verify_state_basis`, no Git blobs.
7. DCP artifact `discovery-acceptance{path,sha256}` → `D_accept_path`; rehash file;
   `D_accept=discovery.validate_acceptance(repo_root,D_accept_path)` (state-free §2).
   `root_path=D_accept.discovery_path` (repo-local, `_safe_repo_file`), `root_sha=…`,
   `root_records=screening.read_jsonl(root_path)` + `validate_discovery_set`.
   SCP artifact `screening-acceptance{path,sha256}` → `S_accept_path`; rehash;
   `expectations={issue_id:COPY.issue_id, research_profile:COPY.research_profile
   (+profile file cross-check), canonical_state_path}` (derived, not caller flag);
   `S_accept=_validate_screening_acceptance_content(repo_root,S_accept_path,
   expectations,root_records,root_path)` (CONTENT only); `effective=…_content.return`
   (`mode/path/records/accounting`); `effective_records/effective_path/effective_sha/mode`.
8. Bind request: `request.discovery_ref{path,sha256,byte_count}` must equal E actual
   (`resolve(effective_path)==resolve(request.discovery_ref.path)` +
   `sha256==effective_sha` + `_verify_sized_ref_bytes` + byte_count; else refuse.
   `request.screening_ref` must equal SCP artifact
   (`path==SCP screening-acceptance.path` + `sha256==SCP sha` + file rehash +
   `==S_accept.result_set_sha256` basis); else refuse.
9. `profile_doc,profile_raw=_load_json_from_sized(request.profile_ref)` (`1165-1169`);
   require `profile.issue_id==COPY.issue_id`, `research_profile==COPY.research_profile`,
   `profile.contract` shape; `before Profile/head captured unchanged`
   (`profile_ref` rehash + `request.work.expected_head/tree` returned opaque, never
   re-observed here; HEAD observation is HIGH-only `_current_head_tree`).
10. Return (data only, consumers reload bytes themselves):
    `request, before_state, before_state_sha256, canonical_state_path,
    profile, profile_path, profile_sha256,
    dcp_record, scp_record, dcp_path, scp_path,
    discovery_acceptance, screening_acceptance,
    root_records, root_path, root_sha256,
    effective_records, effective_path, effective_sha256, effective_mode,
    accounted_root_ids, discovery_map, screening_decisions,
    provenance:{dcp_ref,scp_ref,before_checkpoint,copy_sha}`.
    No writes, no guard, no State mutation, no `agent.*`, no PREARCH proof
    (`check_supersession/_verify_own_epoch_commit` untouched, PREARCH-only remains),
    no operational completion (`require_completion_consistent/_verify_completion_full`
    not called), no future COPY.

### 3.2 Shared private kernel (no permission)

```python
def _derive_root_effective_kernel(
    *, repo_root: Path, before_state: dict[str, Any], canonical_state_path: str,
    dcp_record: dict[str, Any], scp_record: dict[str, Any],
    request: dict[str, Any], profile_doc: dict[str, Any],
    root_records: list[dict[str, Any]], root_path: Path,
) -> dict[str, Any]
```

Pure computation on already-loaded dicts/bytes (steps 7b–10 above: CONTENT validation,
expansion accounting, request binding, map building). Accepts own-loaded data;
acceptance does not grant permission — callers must already hold validated
LIVE (HIGH) or COPY (LOW) authority. Both public loaders call this kernel
(no logic fork).

### 3.3 HIGH current loader (before first COPY, no pretend COPY)

```python
def derive_current_root_effective_context(
    repo_root: Path, request_path: Path, live_state_path: Path
) -> dict[str, Any]
```

HIGH-only, called after `verify_live_eligibility:299-357`
(`agent.validate_agent_state` + `EVIDENCE_REVIEWED` + no downstream + gates pending/
null + no approval files + empty review index + `exception inactive` + null revalidation).
Reads LIVE `live_state_path` (=`request.before_state.path`, hash/bytes checked
`hash==request.before_state.sha256`, `len==byte_count`) **as DATA**
(currently HIGH-validated, not LOW authority); loads `COPY-equivalent` provenance
from that LIVE dict + DCP/SCP files; calls `_derive_root_effective_kernel`
with internally loaded State/prior-CP. LOW history public entry never uses this;
LOW uses §3.1 COPY path only. Precise split: shared kernel accepts data,
permission comes from HIGH eligibility vs LOW COPY pin — kernel itself confers none.

## 4. Propagation sites (exact new kwargs / returned keys)

- `derive_before_context:1172` → superseded by §3.1 (keep name if ROOT prefers,
  else new name; either way path-only `(repo_root,request_path,before_copy_path)`
  — `previous_checkpoint_path` arg removed because predecessor is derived from
  `COPY.provenance.discovery` evidence ref, not caller path; returns §3.1 keys
  incl. `root_* / effective_*`; old `discoveries/screening_acceptance/old_checkpoint_refs`
  keys retained for compat, now bound to validated R/E).
- `build_revision_package_from_paths:1310(repo_root,request_path,before_copy_path,output_dir)`
  → `(*, root_records, root_path)` keyword-only (from §3.1); uses them for
  `validate_discovery_set` + task derivation; returns `{"package","tasks","planned_files"}`
  unchanged shape (no new policy in historic pass).
- `build_revision_cards_views_from_paths:1458(repo_root,package_path,request_path,results_dir,views_dir)`
  → `(*, effective_records, effective_path)` for record binding; returns
  `{"cards","views","planned_files"}` unchanged.
- `accept_revision_evidence_views_from_paths:1550(...)` → `(*, root_records, root_path)`
  passed through to `_validate_evidence_acceptance_content` /
  `_validate_edition_views_acceptance_content` `root_records/root_path` params
  (`evidence:1255-1283,1322-1349`); returns `{"evidence_acceptance","views_acceptance",…}`.
- `build_versioned_ledger_from_paths:1675(...)` → `(*, root_records, root_path)`;
  forwards to `_validate_materiality_ledger_content:2056-2099`
  `(…,root_records,root_path)`; returns `{"ledger","planned_files"}`.
- `build_versioned_completeness_from_paths:1795(...)` → `(*, root_records, root_path)`;
  forwards to `_validate_profile_completeness_content:241-262`
  `(…,root_records,root_path)`; returns `{"completeness","planned_files"}`.
- `prove_revision_from_paths:2002(repo_root,revision_manifest_path,decision_path,before_copy_path)`
  → internally derives OLD context via §3.1 on `manifest.request` + retained COPY
  (OLD before-graph) and validates NEW graph via FULL content cores with
  `discoveries=root_records/effective` from that context (NEW proposed-graph);
  separate contexts, no new DM016/DM017 policy in either historic pass
  (classification/loss are HIGH new-admission gates, not retrofitted validators);
  returns `{"proof","planned_files",…}` unchanged.
- `_verify_adopted_graph_full:783(repo_root,checkpoint_path,checkpoint_sha)`
  → `(*, root_records, root_path)` optional (when called from LOW adopted path,
  pass session R from §3.1 instead of re-deriving from `request.discovery_ref`
  alone); returns existing `{"record","artifacts","artifact_refs","request",
  "manifest","profile_abs","discovery_abs","screening_abs",…}`.
- `check_supersession_record_from_paths:2401(repo_root,checkpoint_path,report_path,before_copy_path)`
  signature unchanged (already path-only); internally uses §3.1-derived R/E for the
  4-artifact FULL validators (no new kwarg, internal reuse).
- HIGH `prepare_revision:456(repo_root,state_path,request_path,revision_id)`:
  after eligibility `:478-499` + `_prove_before_graph_unbound:364-434` and BEFORE
  first COPY `:538 state-before COPY`, call §3.3 current loader + DM016
  `task_authority_sources` classification + DM017 `(parent,OID)` loss check
  (decision §§3–4); refuse before any `*_exclusive_write_bytes`/`_copy_regular_exclusive`.
  `adopt_revision:1064(...)`: re-verifies window `:1127`, then `prove…:1140` BEFORE
  `proof/report` writes `:1142,1176` (existing `_exclusive_write_bytes` no-overwrite
  preserved); postwrite `write_checkpoint_as_planned/replace_state_triplet/
  clear_remaining_exact_slots/write_cleanup_completion/release_guard` need no R/E
  (`None,None` — postread uses triplet + `_verify_adopted_graph_full` recompute,
  `:974-994`, not a new context).
- No DM022 7-shape change (`request/manifest/proof/report/checkpoint/guard/completion`
  SizedRef/ArtifactRef sets unchanged); ordinary 3/5 input validation stays in
  normal Evidence runner, never applied HIGH.

Missing-root authority refuses (`_artifact_ref_shape` fail-closed, no schema fallback,
no `get(kind,legacy)` coercion, no `SECONDARY` fallback). Unresolvable field: none —
map is complete and source-grounded; any future interface contradiction returns to
Astra before code (decision §6/§7, ROOT §5). No helper-only completion.

*Stop at Human Commit Point; no implementation.*
