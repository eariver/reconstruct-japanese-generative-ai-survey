# Versioned same-reader renewal — integrated pre-code R6 (author-side delta, FINAL B.1–B.4)

2026-10-23 JST. Fresh AUTHOR-side integration worker, NOT independent review.
Governing: `outputs/rephase-1-versioned-renewal-contract-decision.md` SHA256
`478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf` INCLUDING §11;
mandatory `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md`;
BOTH independent design reviews WITH final-binding addenda; R2 returns;
`independent-readiness-review.md` §§0–12 + R3 addendum §§134–205 (CHANGES_REQUIRED) +
FINAL R5 assessment §B (NOT READY, residuals B.1–B.4, §A credited, hash note §213–218);
R3 822 lines, R4 492 lines, R5 314 lines (all preserved, not edited).
Read-only source: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce + intended57). No source edits/runtime code/imports/tests/build/fixture/
restore/network/Git writes. This file `integrated-precode-r6.md` (+ twin `.json`) is the ONLY write
in this unit. Method: `Read` + read-only `bash` (`grep -rn`, `python3 -c` stdlib reads, NO project
imports, NO repo-code execution). All `PC` citations verified 2026-10-23 in this unit.

## 0. Scope, erratum, verdict (read first — no self-acceptance)

**Status: R6 DELTA-MAP for FINAL B.1–B.4 as specified below; NO MAP-COMPLETE label claimed as
acceptance. Implementation remains BLOCKED until Astra confirms R3+R4+R5+R6 jointly per decision
§§9/11.3. No conditional GO.** This R6 fixes ONLY B.1–B.4 + R3-json hash pin. All other R3/R4/R5 maps
retained by reference (epoch bindings R5 §1, U lineage R5 §2, 71-table R4 §3, build container R4 §4,
digests/snapshot/readback credited per FINAL §A). Silence is not supersession.

**Erratum (explicit, old records NOT edited):** R4 header line claiming R3 `.json` SHA256
`1f758b0a2e65081830b60b12473b7593522ecf068773bb2595a6d245df581f` is a transcription defect.
Observed read-only `sha256sum` of the preserved file is:

- `integrated-precode-r3.md`: `d080c182b1e627467c2c6c001408233db0e77669e1fbb8f74814c28a518d6402`
- `integrated-precode-r3.json`: `1f758b0a2e65081838b60b12473b7593522ecf068773bb059315b6a245df581f`
  (correct pin; `81838b60/059315b6`, NOT R4-header `81830b60/2595a6d`).
- `integrated-precode-r4.md`: `b8e422bb214448113cc64b33272efe8be4a05c42aae4fc88139c87426f3479a5`
- `integrated-precode-r4.json`: `c6852da07d082c0cd4044ad193690b3185bf8328bb50e36fefd8fe0213e9c008`
- `integrated-precode-r5.md`: `57b6b02300d7e5789aa0fd68344915bf3e1ef335b052445c302a7318b78c940a`
- `integrated-precode-r5.json`: `34010eb346207cd29d02bdaca32c51d26e46de340d7c24331a8816c6c9c9c9`

Astra must re-pin the computed R3-json hash above; author files are NOT edited here (FINAL §213–218
hash note). The MAP defect was header transcription only, not a closure/epoch defect.

If any §1–§4 row proves unimplementable without weakening → precise NO-GO with `file:line`.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Production semantic NO-GO.

## 1. B.1 — Bootstrap HIGH call-list completeness (ACTUAL pre-code tables, not AST-later)

Prose bans ("HIGH-AVOIDED") are REPLACED by per-new-function ALLOW/BAN rows below (MAP rows, not code).
Reviewer checks `grep -rn` bricking hits against the BAN lists; no implementation `ast` needed to close
the MAP (implementation `ast` remains verification, R3 §9 discipline). Narrow extractions/branches are
named with host file + preserved behavior; existing nonrenewal public behavior is intact (wrappers keep
signatures, R5 §1 owner registry O1–O16 unchanged).

Bricking edges (load-bearing, FINAL §B.1): `production.verify_state_basis:959-996` (`:978` live-live SAFE,
`:980-981` current-vs-old BRICK `expected_contract(current disk 71) != state.contract(old 67)`, `:982`
new HEAD vs old `state.implementation`) bricks ANY call on old/before State under new tools — including
`handoff.build_handoff:97` (`pinned=state.implementation`, still executes `:980-981`) and
`orchestrator.verify_runtime_implementation` (`pinned`, still bricks). Renewal HIGH therefore NEVER reaches
`verify_state_basis` on before/retained State (see tables). `_validate_core_stage_report:266-343`
(`:325-329` `report.contract != contract` where `contract = expected_contract or
contract_identity(current disk)`, `:333` impl SHA) is DUAL: SAFE for live reports with current
`expected_contract`, HISTORICAL for old reports (`:479` record-owned `record.contract`/
`record.implementation.repository_commit_sha`); renewal HIGH never forwards an arbitrary
`expected_contract` (no such param, no public skip). `_profile_and_source:208-236` (`:230`
`profile.contract == state.contract`) is live-live SAFE (both live same generation); renewal HIGH calls
it on LIVE State/Profile only, never old-vs-new.

### 1.1 `_observe_renewal_entry(root,state_path)` — HIGH private, before capture, no basis

ALLOWS (exact, with call conditions):

- `core.load_json` (State file + `core.DEFAULT_CONFIG`) — data-structure load only; no semantics.
- `agent._profile_and_source:208-236` on LIVE `state_path` ONLY (never retained COPY): checks
  `state.profile{path,sha256}` shape, `sha256_file(profile)==ref`, `core.validate_profile`,
  `profile.issue_id == state.issue_id`, `profile.research/publication_profile == state.*`,
  live-live `profile.contract == state.contract` (`:230`, both live same generation — old Profile
  contract REMAINS ORIGINAL, never rewritten). Predicate class: CURRENT live-live (not HIST, not old).
- `core.contract_identity:210-228` + `core.repository_commit_sha` — INFO/pins only (current disk
  recompute for `current_tool_predicates` pins); result MUST NOT be compared to `state.contract`
  (no `expected_contract != state.contract` check here; that check lives in FORBIDDEN
  `production.verify_state_basis:980-981`).
- `core.aggregate_file_hash:168-178` (via `contract_identity` only) — data-structure hash, no State.
- `verify_versioned_history(root,record_path)` (HIST, record-only, new-kind aware per §1.4) for prior
  history: reloads seal/receipt/proof/basis/retention + O17 scope (B.2) + §1 bindings; returns
  `HISTORICAL_IDENTITY_VERIFIED` + observed refs, never a permit.
- Pure `_safe`/`_safe_file`/`_read_bytes_bounded` + strict JSON + `sha256_file/sha256_object` recompute —
  data-structure checks only.

BANS (with `file:line`, transitive included — forbid `production.verify_state_basis` EVEN via helper):

- `production.verify_state_basis:959-996` (BRICK `:980-981`), `agent.validate_agent_state:498` /
  `_validate_agent_state:503-560` (even on LIVE — HIGH uses `_profile_and_source` + HIST directly,
  avoiding checkpoint/human-gate coupling at entry), `agent.resolve_checkpoint_artifact:652`/
  `_resolve:662`, `agent.resolve_active_screening_acceptance` (via `screening:442-489`),
  `agent_tool.current_stage_basis_override:122-143`, `screening._canonical_root_acceptance:325-350`
  (State-profile branch), `screening.resolve_effective_discovery_basis` State branch,
  `observe_current/renewal_authority` (HIGH itself), Reader/Gate/Candidate/seal/full receipt/P1/P2R/P3S,
  `core.repository_commit_sha` AS AUTHORITY (allowed ONLY as INFO pin above),
  `pending_basis`/`already_verified`/caller-dict/`seal_path`/ambient/cache, any `expected_contract`
  caller param or synthetic State. Each BAN is a MAP refusal: reaching it → precise NO-GO, never a
  weakened checker. `grep -rn verify_state_basis` hits (`agent_tool:7,123,127,131`, `evidence:550,765`,
  `handoff:97`, `orchestrator:82`, `production:959,1008,1112`, `screening:503,647`) are therefore all
  excluded from this function by construction.

Narrow extraction (proposed, host file, behavior intact): NO new shared core needed here; HIGH calls
existing `_profile_and_source` + `contract_identity` + HIST directly (thin call, no wrapper change).
Existing `validate_agent_state` public behavior UNCHANGED for nonrenewal callers.

### 1.2 `observe_renewal_authority(root,state_path,basis_path)` — HIGH basis-bound

ALLOWS: §1.1 ALLOWS on LIVE inputs + `validate_renewal_basis` retained-COPY checks (below) +
demands (exact, no `expected_contract` param): LIVE State == fresh `before_state_ref` (live-live,
`sha256_file` equality); retained COPY == `basis.retained_copy_ref` binding
(`_expected_retained_dest:831`, full inventory, R3 §10); selected predecessor == State-selected seal
prior-relative (R3 §3 + R5 §2 lineage-reachable); `basis.current_tool_epoch` == CURRENT disk
closure/contract recompute member-wise (current-current, Layer-B-2 discipline
`weekly:587-588`, `editorial:1958-2000` as 63 per R3 §6.5, `contract_identity` vs
`proof.supported_contract` apart from R3 §6 steady-state bytes). Per-predicate: live-before =
CURRENT live-live; retained = HIST COPY mapping + detached bytes; current tools = CURRENT recompute;
prior selection = HIST lineage + CURRENT State-selected equality. Old Profile contract REMAINS ORIGINAL
(pinned `profile_ref`, never rewritten); new proof/new live `CORE_STAGE_CONTRACT` report uses
currentContract (minted under current disk per §1.3).

BANS: §1.1 BANS + `expected_contract` param + public skip + `verify_state_basis` transitively (even via
`handoff:97`/`orchestrator:82` helpers — renewal path never calls those helpers) +
`validate_agent_state` on before State + checkpoint/human-gate coupling. No pending flags/synthetic
State.

### 1.3 `validate_renewal_basis(root,basis_path)` + `verify_renewal_source_proof(root,basis_path,proof_path)`
— SOURCE detached, every proof readback (startup + finalize + activate + resume + after-activation
readback, decision §11.1)

ALLOWS (Layer-B, still NO State): `core.load_json/sha256_file/sha256_object/sha256_bytes/
repo_local_path/parse_instant/iso_utc/aggregate_file_hash/contract_identity(pure file read ONLY)` +
`schema_gate.*` + `citation_refs.refs` + `drafting.validate_synthesis_result/validate_draft_result` +
`provenance.resolve_source_access_provenance` + pure token/URL/archive helpers +
bounded `O_NOFOLLOW` `_safe` reads (R3 §9 list retained) + §1 `supported==observed` check (B.3) +
HIST verdict consumption (`verify_versioned_history` matching observed epochs per R5 §1). CURRENT
closure/contract/schemas recomputed from CURRENT disk; `proof.supported_source_bindings ==
basis.observed_source_bindings` (B.3 row); old `CORE_STAGE_REPORT` own-record `core` fields for
HISTORICAL reports validated history-only (`:479` record-owned, no live compare); LIVE reports use
exact new current (`:1601-1610` discipline).

BANS: `agent.validate_agent_state:498`/`_validate:503`, `resolve_checkpoint_artifact:652`,
`current_stage_basis_override:122-143`, `_canonical_root_acceptance` State branch `:325-350`,
`resolve_active_screening_acceptance:442-489`, `observe_current/renewal_authority`,
Reader/Gate/Candidate/seal/full receipt/P1/P2R/P3S, `repository_commit_sha` AS AUTHORITY,
`pending_basis`/`already_verified`/caller dicts, `verify_state_basis:959-996` transitively (even via
`evidence:550,765`/`screening:503,647` shared cores — Layer-B calls NARROW shared CONTENT cores in
existing family files with State block REMOVED per R3 §8/R4 §5, thin wrappers keep public behavior;
any State-coupled helper path → NO-GO). No `expected_contract` caller authority.

Narrow extractions/branches (proposed, host files, wrappers intact): `_validate_evidence_package_basis_content`
(`survey_evidence_v2.py` minus `:764-770` State block minus `implementation_sha`), `_validate_screening_package_basis_content`
(minus `:647`), `_validate_result_batch_content` (`:653-693` with `expected_result_basis` State-free per
R2-A §7 `Path(".")` fix retained), `_validate_discovery_set/expansion_content`, `_normalize_record_content`+
`_validate_graph_content`+`_validate_x_integration_content`, `_validate_ledger/completeness/view/supplement/selection/
architecture/draft_content` (R3 §8 list retained); original publics keep UNCHANGED signatures via thin
wrappers (State block + delegation). Equivalence oracle per R3 §8 retained (both paths over identical
accepted graphs, identical accept/refuse, else NO-GO).

### 1.4 Historical low selection + new-kind resolver (before agent new-state validation)

New typed history resolver `verify_versioned_history` MUST understand the new kind BEFORE any agent
new-state validation runs (don't just `old_is_editorial`):

- Branches (exact functions + branch): `agent._is_editorial_record:64-69` /
  `_is_legacy_record:72-77` + `_resolve_publication_revalidation:1361-1443` (`:1386-1392` kind dispatch,
  else `reason class unrecognized`) + `publication_set.validate_activation_record:1239-1314` +
  `_walk_chain_backwards:1023-1051` + `resolve_publication_selection` /
  `require_active_or_canonical:2118-...`/`resolve_publication_mode:2090-...` — ADD
  `VERSIONED_RENEWAL_ACTIVATION_V1`/`REVIEWED_VERSIONED_CORE_RENEWAL` branch (legacy/editorial verbatim,
  chain/anchor/sequence/time/cycle per `:109,:1023-1230`, later-legacy unsupported `:1189`,
  R1/canonical pre-write refusal kept) with old-vs-new pin rule (pre-renewal records validate against
  record-epoch SHA; renewal validates against current disk, R3 §1). Without this delta P-N1 (normal
  active Candidate→direct stage) refuses post-activation — concrete consumer MAP gap closed here as MAP
  rows (code pending, correctly classified as implementation).
- Order: HIST structural load + new-kind branch runs BEFORE `agent.validate_agent_state:498`/
  `_validate_agent_state:503` on the NEW State (which calls `_resolve_publication_revalidation`
  + `_validate_checkpoint_record:382-...` + `validate_state_semantics:718-...`); HIST never calls agent
  State validation (no recursion, decision §4/§11.1; low structural selection MAY call history, history
  MUST NOT call selection back). Existing nonrenewal public behavior intact (legacy/editorial/canonical
  branches verbatim).

### 1.5 Stage VALIDATED/Release wrappers (current-only, no fake State)

- `stage.validate_stage:721-766` (calls `agent.validate_agent_state:732`, mints `current_contract:749`
  + `current_impl:744` for the NEW report, NO `verify_state_basis`; wrapped in
  `current_stage_basis_override:746` ONLY for stage semantics, not for renewal HIGH): renewal P-N1 calls
  it on the LIVE post-activation State (current-current SAFE); HIGH tables above never route old State
  through it. `_profile:740` is the stage-local Profile loader (live-live, same as
  `agent._profile_and_source:208-236`); NO Profile rebind (path/bytes identical).
- Freeze `_prepare_freeze_inputs:171-245` (derives proof from VALIDATED Candidate, passes to direct
  review loader, requires bundle equality) + `_preflight_freeze_pair:323-390` (authority/overlap +
  `st_dev,st_ino` alias checks) + `_recheck_snapshot:248-256` + Release
  `validate_release_manifest`/`validate_release_reconciliation_review` (agent `:486` FROZEN branch):
  all derive proof from validated Candidate (R3 §§9–10 retained), snapshot members per R3 §10 (externals
  ARE members, exact-file inventories). No `verify_state_basis` on old State; no `expected_contract`
  caller param.
- Per-predicate summary for §1.1–1.5: live State/Profile/binding = CURRENT live-live
  (`_profile_and_source:208-236`, `:230` kept live-live); retained COPY = HIST mapping + detached bytes
  (`validate_renewal_basis`); current tools = CURRENT recompute (Layer-B-2); prior selection = HIST
  lineage + CURRENT State-selected equality; old report `core` = HISTORICAL record-owned (`:479`);
  new report `core` = CURRENT minted (`:1601-1610`). `production.verify_state_basis:959-996` appears
  NOWHERE transitively on any renewal HIGH/Layer-B path above (even via `handoff:97`/`orchestrator:82`/
  `evidence:550,765`/`screening:503,647` — those helpers are never called from the ALLOW lists; where a
  shared core is needed the State-free narrow extraction is called instead). The ONLY justified current
  initialization is LIVE minting (`stage:749-760`, `agent:1601-1623`, `editorial_pub:1886/3403`) on LIVE
  State under current disk — never old State under new tools. No public pending flags/synthetic State/
  `expected_contract` caller authority exists on any new entry (signatures per R3 §11 retained:
  `basis_path`-only + persisted paths, reloaded every use).

## 2. B.2 — O17 scope evidence row (narrow, finite)

R5 §1.2 O1–O16 omits original scope evidence (decision §11.1 history leaf reloads "original scope
evidence"; R3 §2 bootstrap recognizes P1 scope shape; Gate early-scope reload). ADD O17:

| # | Validated doc (`source_ref`) | Schema (`schema_path`) | Pointer | Digest | Epoch owner |
|---|---|---|---|---|---|
| O17 | scope review file from receipt `scope_review_ref{path,sha256}` (editorial `P/...` or prior-`R` lineage; `staged.scope_review_ref == receipt.scope_review_ref` checked `:795-796`) | `schemas/reader-surface-semantic-review-v2.schema.json` | `/editorial_correction_scope` (whole-doc `review_sha256` binds captured JSON `:2154-2157`) | `review_sha256 == core.sha256_object({all except review_sha256})` + loader digest `load_and_validate_reader_surface_semantic_review` binding (`proposal:2145-2149`, staged `:1990-2002`, receipt `:866-899`) | staged producer_head (editorial scope fixed at staged time; `staged.scope_review_ref` pinned at dispatch `:1683-1688,:1738`; Gate `_derivation_for_manuscript:1195-1224` reloads early scope via staged proof context, never postrender) |

- HIST semantic target: HIST loads scope file by persisted `scope_review_ref` path+SHA, checks
  `reviewed_surface == receipt.reviewed_reader_input` (exact early review `:866-899`), `scope block
  {version:EDITORIAL_CORRECTION_SCOPE_V1, decision:WITHIN_APPROVED_AUTHORITY}` (`:886-887`,
  `proposal:2161-2165`), `before_reader_input == proposal.basis.active_reader_input_ref`,
  `preserved_upstream_sha256 == proposal.basis.preserved_upstream_digest`, `change_summary`/
  `evidence_locations` non-empty, scope `check_id` PASS with detail/evidence (`proposal:2125-2185`),
  via record-epoch blobs + `schema_gate` at derived epoch. CURRENT semantic target (Layer-B/HIGH):
  same predicates on session-pinned bytes + proof-bound trio/reader (R5 §2); Gate uses early scope
  ONLY (postrender semantic reviews are separate C inputs, never waived). Epoch source is actual
  staged `scope_review_ref` + `producer_head:1039` (not caller choice); unknown source/schema/pointer/
  epoch → refuse (`REVIEW_TARGET_MISMATCH` for binding, `HISTORY_*` for epoch/blob).

## 3. B.3 — `supported==observed` comparison (exact callee/runtime/position)

R5 §1 states the rule but not the check site. ADD one Layer-B row (MAP, code pending):

- Exact callee: `verify_renewal_source_proof(root,basis_path,proof_path)` (SOURCE detached, R3 §9)
  step 4 (after R3 §9 steps 1–3 + R5 §1 HIST verdict): load `basis.observed_source_bindings` +
  `proof.supported_source_bindings`, verify sorted-set equality on full row tuples
  (`source_ref.path,source_ref.sha256,binding,schema_path|"",schema_pointer|"",
  repository_commit_sha,schema_sha256|""`) AND byte-order equality to sorted-key order; mismatch →
  `HISTORY_TOOL_EPOCH_DRIFT` (NOT `BASIS_*`; basis/proof binding mismatch is a history-epoch fault).
- Runtime/position: runs at startup AND on EVERY proof readback INCLUDING after activation (same
  Layer-B entry as CURRENT closure/contract/schemas + HIST verdict: `validate_candidate:749-814` →
  `validate_manuscript_manifest:413-451` (reloaded `renewal_source_proof_ref`) →
  `verify_renewal_source_proof` steps 1–4; also `validate_renewal_receipt`/
  `validate_prepared_renewal_set` pre-write + `resume_renewal_activation` full-intent reload per R3 §11).
  HIGH NEVER runs it on readback; detached NEVER calls `observe_renewal_authority` (R3 §9 retained).
  `proof.supported` without matching `basis.observed` (subset/superset/invented epoch) refuses pre-write;
  old evidence absent from tool commit remains positive control (decision §3).

## 4. B.4 — Finalize REQUIRED rule for U (enforcement, no silent fallback)

R5 §2.1 marks the keyword REQUIRED for U but leaves the operation boundary implicit. ADD (MAP, code
pending): `finalize_renewal`/`validate_prepared_renewal_set` MUST refuse a renewed set whose NEW
Candidate/QA/Gate files lack the NEW `renewal_source_proof_ref` (+ `renewal_receipt_ref` on Gate)
with full-set SAME-proof equality to the NEW proof (R5 §2.2 rule 3). Absence → `REVIEW_TARGET_MISMATCH`
(refuse pre-write, exit 2), never silent fallback to the embedded PRIOR proof. Validator fallback
remains READ-ONLY (R5 §2.1: C manuscript without keyword → own embedded CURRENT, may stale-refuse;
editorial without keyword → old P3S path). API `renewal_source_proof_ref=None` default does NOT permit
a missing proof in renewal HIGH finalization: `finalize_renewal` treats `None` for a renewed set as
refusal (the default exists for standalone old validators only). This covers BOTH the supplied old
review loader nested manuscript (`validate_review_record:643-647` threads SAME reloaded NEW ref
explicitly, never ambient) AND Candidate/QA/Gate builders/validators (derive from own payload, outer
expected must be identical). Context `→` stored-prior (HIST) vs `→` current-NEW (CURRENT) never cycles
per R5 §2 (HIST ancestor-only, CURRENT immediate-bind, seal-selected NEW).

## 5. Per-B status (proof-map closed vs precise unclosed — no unproven all-closed)

- [x] B.1 MAP-CLOSED as pre-code tables above (§1.1–1.5: per-function ALLOW/BAN with `file:line`,
  narrow extractions with host files + wrappers intact, per-predicate CURRENT/HIST/data-structure +
  call conditions, old Profile ORIGINAL vs new proof/report currentContract, `verify_state_basis`
  forbidden transitively with helper coverage, no pending/synthetic/`expected_contract` authority,
  new-kind resolver before agent validation with branch rows, nonrenewal behavior intact).
  Remaining CODE (not MAP): implementation of the three HIGH functions + low new-kind branches per the
  rows (correctly classified as implementation; MAP tables above ARE the completeness proof the gate
  demanded instead of "AST-later").
- [x] B.2 MAP-CLOSED (O17 row with exact schema path/pointer/digest/epoch source from actual
  staged `:1039,:1990-2002,:2140` + receipt `:795-796,:866-899` + proposal scope validator
  `:2125-2185` + Gate early-scope `:1195-1224`; current vs HIST targets distinguished).
- [x] B.3 MAP-CLOSED (exact callee `verify_renewal_source_proof` step 4 + runtime all-readback position +
  `HISTORY_TOOL_EPOCH_DRIFT` code; HIGH/readback separation retained).
- [x] B.4 MAP-CLOSED (finalize/validate-set REQUIRED rule with `REVIEW_TARGET_MISMATCH`, nested-manuscript
  + Candidate/QA/Gate coverage, `None`-default ≠ permission, no-cycle restatement).
- [x] R3-json hash pin ERRATUM delivered (§0; computed hashes govern; no old file edited).

**No MAP-COMPLETE label is claimed as acceptance; no conditional GO.** Implementation stays BLOCKED
until Astra confirms R3+R4+R5+R6 jointly. Any unimplementable row → precise NO-GO with `file:line`.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Stop at internal return; no code, no
ordinary Commit/Push (Human-owned).

(End — R6 fixes B.1–B.4 + hash pin ONLY; R3/R4/R5 preserved; all other maps referenced, not duplicated;
no independence claim; no runtime evidence.)
