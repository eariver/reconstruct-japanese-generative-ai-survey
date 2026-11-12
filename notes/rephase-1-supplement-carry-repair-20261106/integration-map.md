# Supplement-carry integration map — existing HIGH producer (source-grounded, no code yet)

Binding: `notes/rephase-1-selection-architecture-20261105/astra-working-resolution.md` FULL (§§5–6, §4 supersession).
Facts: `actual-dm022-supplement-operation-map.md` + `independent-correction-capability-review.md`.
Source: final139 applied proof `.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60` (preferred final test7b). e84 instance read-only comparison only.
Scope: repair `LOW.build_revision_package_from_paths` missing carry; full normal HIGH `prepare→adopt/resume/readback`, not test manual `supp-candidate` assembly.

## 1. Gap (one sentence)

HIGH `prepare_revision` (`survey_prearchitecture_acceptance_v2.py:636`) always calls `LOW.build_revision_package_from_paths` (`survey_research_authority_v2.py:2128`), which copies only OLD `prompt`/`contracts` (`2257-2258`), never `authority_supplement`, never sets `authority_supplement_source_ids` (`2211-2228`), ignores `request.supplement_manifest`; cards then resolve empty supplement context (`survey_evidence_v2.py:322-330`) and fail or go Discovery-only (`_build_card_core:2243-2247`).

## 2. `request.supplement_manifest` semantics (decision)

Explicit nullable `SizedRef`, no OLD-carry fallback, no inference:

- Schema already `null|SizedRef` (request schema 7,37; manifest 37,47). HIGH manifest records `request.get("supplement_manifest")` passthrough (`:786`).
- `null` → unsupplemented package: no `authority_supplement`, no `contracts.supplement`, no task supplement IDs. Preserves current no-supp history (tests `:615`, `:486`). For W34/SP OLD-supplemented editions, `null` must refuse (would lose 401/28 bindings, proof `unaffected !=` would refuse).
- non-`null` → selected manifest MUST be validated before any package/task write: `SizedRef` path/sha/`byte_count` bind file bytes; `validate_evidence_authority_supplement(repo_root, manifest_path, None, expected_issue_id, expected_discovery_path=request.discovery, expected_screening_path=request.screening, screening_acceptance=DS.s screening, discoveries=DS.root)`; every `raw_ref` exists, `raw_sha256`+`byte_count` match, `raw_path` inside `source_root`, no symlink/traversal, Discovery/Screening SHA drift refused (`survey_evidence_v2.py:560-634`).
- `package.authority_supplement` MUST equal validated request manifest `{path,sha256}` (not OLD path when replaced). `contracts.supplement` + trailing rule required iff supplemented (`_check_evidence_package_files_content:1061-1067`, `prepare_evidence_package:975-983` pattern).
- Task IDs: `sorted(id for id, e in validated.entries.items() if e.evidence_task_id == task_id)` (same predicate as `prepare_evidence_package:927-931`). Enforce `_check_evidence_tasks_content:1124-1138` — every supplement source bound exactly once by its task; task supplement IDs require manifest; supplement contract requires manifest.
- Unchanged (W34): request manifest path/sha MUST equal OLD `authority_supplement` (401 bindings preserved, bodies already in manifest, no new archive). Replaced (SP 30 = 27 same + 3 replaced): request manifest is NEW file; OLD `prompt`/`contracts` preserved verbatim, supplement contract/rule updated to NEW supplement schema SHA.

## 3. HIGH flow with carry (pins → writes → rechecks)

Initial COPY/validators (existing, unchanged order): LIVE strict parse → `verify_live_eligibility` → profile/source → `_prove_before_graph_unbound` → HEAD/tree bind → request parse/schema → `expected_head/tree` + Contract8 + tool SHAs bind → `before_state` SHA/`byte_count` bind → DM016 classification + DM017 loss gate → 7-slot COPY (`prepare_revision:467-633`).
Then:

1. `ds_context = derive_ordinary_root_effective_context(repo_root, request_abs, state_copy)` — true historical R/E from pinned COPY + accepted D/S chain (never E-as-R, never LIVE). Reuse for package + cards + proof.
2. Validate request `supplement_manifest` SizedRef bytes + full supplement content (above) using `ds_context` screening/discoveries. Capture expected pins BEFORE validation: request SHA, COPY SHA, OLD package `prompt`/`contracts` SHAs, OLD `authority_supplement` path/sha (if any), selected supplement manifest SHA/bytes, all Raw path/sha/bytes, basis Discovery/Screening SHAs.
3. `built_pkg = low.build_revision_package_from_paths(...)` [TO BE REPAIRED]: keep Discovery/Screening derivation, OLD `prompt`/`contracts`, screening digest recompute, task `stable_task_id`/filename/deterministic order; ADD: authority copy, supplement contract+rule, per-task IDs, recomputed task SHAs/metas, `_check_evidence_package_fields_content` + `_check_evidence_tasks_content` before return. Caller writes package/tasks exclusively (`:638-641`).
4. `low.build_revision_cards_views_from_paths(..., before_copy_path=state_copy)` (unchanged code): pins request+COPY+package, `_validate_evidence_package_basis_content` vs true root, `_resolve_phase_supplement_context(package, implementation_sha=None)` now non-empty, `_merge_supplement_task_sources` + `_build_card_core` with `record.source_bindings` (must name task-bound `supplement-src-*` for supplemented tasks, else `src-1` Discovery-only), `_validate_card_core` per card. Private context reuse only — no public verified-dict, no global/epoch cache, no new validator.
5. `low.accept_revision_evidence_views_from_paths(..., request_path, before_copy_path)` + FULL `_validate_evidence_acceptance_content` / `_validate_edition_views_acceptance_content` (`:707-718`).
6. Ledger/completeness via existing builders + manifest `_sized()` per-file refs (tasks/cards/views/acceptances/ledger/completeness + `supplement_manifest` passthrough) + retention 7-slot inventory + schema validate + exclusive writes (`:719-808`).
7. `prove_revision_from_paths` (no change needed unless contradiction found): manifest/decision/COPY bind, OLD 4 via `before_checkpoint.evidence` triplet, NEW 4 via `candidate_outputs`, FULL content cores, task-identity + Discovery→task identity, affected-must-differ + Raw claim-bytes routing (basename contains DID), unaffected `old_doc != new_doc` refuse (`:3383-3388`), ledger row identity, mechanical projections explicit, digests recomputed. Package-only fix insufficient if request/manifest/proof inconsistent — proof + `_validate_*_content` + `_check_evidence_tasks_content` are the changing-path oracles, not just builder output.
8. `adopt_revision`: LIVE==before, HEAD/tree + Contract8 + tool SHAs + retention==manifest + no-prior-Human-review + DM016/DM017 re-verify → `prove` → report → `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` checkpoint (same-State `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`, atomic triplet switch, original_anchor/supersedes) → guarded 7-slot clear → completion → guard release (`:1100-1332`). `resume_bound_attempt`/`resume_revision` bounded remaining-steps only; `readback_revision` reports triplet/lineage/completion, never claims publication activation. CLI unchanged (no new flags; supplement travels in versioned request/manifest).

## 4. Signatures / callers / closure / Contract8

- Change surface (existing fields/module/family only): `survey_research_authority_v2.build_revision_package_from_paths(2128)` + its internal supplement load/copy/task-SHA path. Callers: `survey_prearchitecture_acceptance_v2.prepare_revision(636)` sole whole-R writer; downstream `build_revision_cards_views_from_paths(2277)` / `accept_...(2457)` / `prove_...(3080)` / `adopt(1100)` / `resume/readback/CLI(1483-1521)` unchanged unless contradiction returns to root.
- Reused (no change): `_resolve_phase_supplement_context(300)`, `_merge_supplement_task_sources(469)`, `_build_card_core(2228)`, `_validate_card_core`, `_check_evidence_package_fields/files/tasks_content(1024-1141)`, `_validate_evidence_package_basis_content`, `validate_evidence_authority_supplement(523)`, `derive_ordinary_root_effective_context`, `load_revision_request`, `stable_task_id/task_filename`.
- SOURCE closure/digests: `ds_context` root+effective + `result_set_sha256`/`view_set_sha256` recompute + per-file `SizedRef` manifest/proof binds + manifest FILE SHA bound by decision `manifest_ref`. No new proof family/retention slot (proof schema 19 has no supplement row; retention 7 slots only; supplement Raw stays at manifest-declared `raw_path`).
- Contract8: NO change (pipeline/quality/research/publication versions/SHAs via `core.contract_identity`). Tool SHAs (`_contract_and_tools:437-453`, 7 paths) WILL change for edited `survey_research_authority_v2.py`; requests must pin new SHAs + new `expected_head/tree`. No new schema/module/family, no public bypass flag, no cache. Any contradiction (e.g. proof/retention cannot bind supplemented graph without schema change) returns to root before broadening.

## 5. Tests (meaningful, no stubs)

Real HIGH `prepare→adopt/resume/readback` on isolated fixtures with legitimate content (reuse captured W34/SP DATA shapes, no fake repo/empty root/stub proof):

- BOTH `WEEKLY` (DERIVED, 401-supplement pattern) and `THEMATIC/Special` (28-supplement pattern) full prepare + supplemented cards + independent-fixture decision + adopt + resume + readback.
- Full affected + unaffected: unchanged cards byte-identical else proof refuses; ledger rows identical except allowed affected disposition; task-identity + Discovery→task binding identical.
- Negative: missing supplement file, `supplement_manifest` SHA/`byte_count` drift, Raw missing/SHA/`byte_count` drift, wrong-DID binding, supplement targeting DROP, `source_bindings` naming unbound `supplement-src-*`, late HEADER/tree/contract/tool drift, guard present, retention mismatch.
- No-supp compat: OLD-unsupplemented history still passes with `supplement_manifest:null` (current tests preserved).
- Unchanged (W34 manifest same) vs replaced (SP 27 same + 3 replaced) both covered; SP D142-new-source case stays blocked (no body) unless root grants archive authority.

## 6. Workcopy + evidence plan (not executed yet)

From available final proof `candidate-partial-b40de60` (final139/771: DIRECT409 `de0af9cbd...`, manifest `c5a6b230...`, 771-file guard): new isolated workcopy + independent Git DB (inert origin, no alternates/hardlinks/shared objects, process-scoped identity, no empty commits, no `HOME`/git-config mutation). Verify 771 files + patch apply `check0` before edits. Minimal raw: exclusive-write logs, pin tables (request/COPY/package/tasks/supplement/Raw/basis/tools/HEAD-tree), FULL validator outputs, proof/report/checkpoint bytes, adopt/resume/readback outputs, failure INDETERMINATE preservation. No network/Production/reconstruct-Git/readback, no old-runner rerun, no saved e84 mutation.

---
Code BLOCKED until root + independent scoped review confirm this map. Implementation after confirmation only.
