# Independent correction-capability review — DM022 supplement operation scope (read-only, no code)

**Role:** independent scoped source reviewer — NOT implementer, NOT author, NOT Astra/root, NOT Human.
**Date:** 2026-11-06.
**Method:** read-only source inspection + packet DATA join. No execution, imports, tests, fixtures, network, Git/HEAD/status/log readback, State writes, Draft/PDF, Human Gate, ordinary Commit/Push, Production mutation, subagents.
**Instance only:** `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`, epoch `e84a82aca000c990597ea8cf60f548e2ff187bd1` over `48082356`. Shipping final139/771 DIRECT409 unchanged; test-only `d486` vs `7b86` delta preserved as history.

**Read scope (explicit):**

- Current packet `actual-dm022-supplement-operation-map.md` FULL (source-grounded map, authoritative for operation facts).
- Earlier `accepted-evidence-correction-applicability.md` FULL — preserved as historical synthesis; its §4.2 "LOW direct + HIGH coordination" normal-path claim is explicitly superseded by the map header/§7 and is NOT reused as authority here.
- Source `scripts/survey_prearchitecture_acceptance_v2.py`: `prepare_revision` (456), manifest (761-793), `adopt_revision` (1100), CLI (1483-1521).
- Source `scripts/survey_research_authority_v2.py`: `build_revision_package_from_paths` (2128), `build_revision_cards_views_from_paths` (2277), `accept_revision_evidence_views_from_paths` (2457), `prove_revision_from_paths` (3080).
- Source `scripts/survey_evidence_v2.py`: `_resolve_phase_supplement_context` (300), `_discovery_task_sources` (453), `_merge_supplement_task_sources` (469), `validate_evidence_authority_supplement` (523), `prepare_evidence_package` (828), `_build_card_core` (2228), `_validate_card_core` / package/task content cores (989-1141).
- Schemas `dm022-revision-request-v2.schema.json` (37), `dm022-revision-manifest-v2.schema.json` (37,47), `dm022-revision-proof-v2.schema.json` (19), `evidence-v2-run-package.schema.json` (12,99; 77-85), `evidence-v2-task.schema.json` (15).
- Test `tests/test_evidence_scaling_v2.py:1266-1475` (supplemented LOW case).
- Packet lifecycle DATA `route-map-data.json`, `route-map.md` §§1/9, `astra-working-resolution.md` §§1-3 as cited history for State/lifecycle only; no new State verification claimed.

## 1. Verdict

**SOURCEGAP_CONFIRMED.**

No actual supported normal `prepare_revision → adopt_revision` route currently carries an Evidence Authority Supplement. The earlier applicability §4.2 selected-normal-path composition (LOW direct package-path for cards plus HIGH coordination for adoption as a supported whole) is **inaccurate as a normal whole writer** and is superseded by the current map §7. The map's NO/YES split is confirmed on source:

- **NO** — normal HIGH prepare/adopt composition with supplements: not wired, not tested.
- **YES only** — lower direct LOW calls on a manually supplemented package/request: unit-tested, but not HIGH prepare/adopt and not State-adoption composition.

This review does NOT reopen any closed B2/B4 pre-code gate and does NOT require an R4 audit or PDF suite for this read-only selection decision. B2/B4 + §10 map status remains as prior authority states; implementation remains BLOCKED until that map plus Astra plus independent readiness confirm.

## 2. Lifecycle confirmation (packet DATA, valid)

Both editions remain `EVIDENCE_REVIEWED`, `next_action = stage:selection`, `terminal_reason = null`, LEGACY `CANDIDATES_NORMALIZED → EVIDENCE_REVIEWED` checkpoint family (`kind` absent), no Human review/index/gate, no presented immutable request, no Exception, null publication revalidation pointer, guard absent, seven canonical slots absent (`outputs_absent` for both editions in `route-map-data.json`). Four refs live-SHA-checked per `route-map-data.json`:

- W34: Evidence `edf21e4d…` 409, Views `3777133c…` 409, Ledger `f089cc4e…` 439, Completeness `e8c432dd…` 3 LIMITED.
- SP: Evidence `65784e69…` 160 (8 VERIFIED/152 PARTIAL), Views `1557fef7…` 160, Ledger `b7c85b4e…` 165, Completeness `d67f7f83…` 15 LIMITED.

DM022 operating window lifecycle predicates therefore hold on ID/provenance grounds. Content/authority predicates do not (see §§3-4). Seven-absent inventory is currently trivially absent but must still be recorded as exact absent inventory before any adoption; this review records no inventory and performs no adoption.

## 3. HIGH prepare loses task/package supplementation (confirmed on source)

`build_revision_package_from_paths` (2128-2274):

- Loads OLD package only at 2172-2177, copies only `old_pkg_pkg.get("prompt")` / `.get("contracts")` at 2257-2258. It never reads `old_pkg_pkg.get("authority_supplement")`.
- Task derivation at 2211-2228 sets `source_records`, `verification_targets`, `screening_basis` only. No `authority_supplement_source_ids`.
- Package dict at 2243-2265 has no `authority_supplement` key and no supplement contract extension.
- `request.supplement_manifest` is never referenced in this function. Only HIGH manifest records `request.get("supplement_manifest")` at `survey_prearchitecture_acceptance_v2.py:786` as passthrough.

`prepare_revision` (636, 651, 671-676):

- Calls `low.build_revision_package_from_paths` (636), writes package/tasks (638-641), calls `low.build_revision_cards_views_from_paths` (651), then ledger/completeness/manifest. No package/supplement override exists.
- CLI (1487-1504) exposes only `prepare --repo-root --state-path --request-path --revision-id` and `adopt --repo-root --state-path --revision-path --decision-path`. No `--package`, `--supplement`, `--supplement-manifest`, or package override.

`build_revision_cards_views_from_paths` (2350-2355) resolves supplement context from the **package** `authority_supplement` via `_resolve_phase_supplement_context`. With the HIGH-generated package that context is legitimately empty (`survey_evidence_v2.py:322-330`). `_build_card_core` (2243-2247) then requires `record.source_bindings` to name task-bound sources; a request binding to `supplement-src-*` fails against an unsupplemented package, and without `source_bindings` the card defaults to `src-1` Discovery-only.

Full HIGH prepare/adopt tests use unsupplemented requests (`test_dm022_prearchitecture_acceptance_v2.py:615`, `test_dm022_full_lifecycle_v2.py:486`, both `"supplement_manifest": None`). The gap is therefore a producer wiring gap, not a test-selection accident.

Current authority consequence (packet DATA, consistent with source predicates): W34 accepted package carries `authority_supplement` (389414B `ce6f977a…`) with **401** task records bearing `authority_supplement_source_ids` and 8 without; 4 affected arxiv bodies are supplement-only in card `sources`. SP accepted package carries `authority_supplement` (30922B `ffcd0a7e…`) with **28** supplement-bound tasks of 160 (`EFF-D141` supplement-only, `EFF-D142` Discovery-only with no body). HIGH prepare builds a package with zero supplement refs; cards become Discovery-only or prepare fails if request `source_bindings` still names supplement IDs.

## 4. Unaffected 401 W34 / 28 SP cannot be preserved by existing HIGH (confirmed)

`prove_revision_from_paths` (3354-3388, 3391-3407) refuses semantic drift:

- Cards: `old_doc != new_doc` for any unaffected Discovery refuses (3383-3388). Only actually-differing digest SHAs are emitted as mechanical projections (3426-3428); directory-prefix exclusion is forbidden.
- Ledger rows: unaffected rows must be identical OLD vs NEW (3405-3407); affected rows may change only downstream disposition/view/rationale.
- Task identity sets must be identical OLD vs NEW (3298); Discovery→task binding must be identical (3325).

With a HIGH-unsupplemented NEW graph, the 397 unaffected supplement-bound W34 cards plus 8 Discovery-only cards, and the 27-28 unaffected supplement-bound SP cards, would differ from Discovery-only NEW cards. Proof would refuse. The existing HIGH route therefore cannot produce a valid full409/full160 revision with current package/card authority, even though the 4 W34 affected bodies already exist in the W34 supplement manifest (no new archive needed for those bodies). `EFF-D142` additionally needs a new supplement source (currently no task supplement ID, no body) and is blocked on source/producer capability regardless.

## 5. LOW manual unit != HIGH prepare/adopt witness (confirmed)

`test_evidence_scaling_v2.py:1266-1475` explicitly states the boundary:

- Docstring 1266-1277: HIGH prepare threads the unsupplemented revision package; LOW card supplement binding is covered via shared core/unit probe, "not claimed as HIGH-threaded here."
- 1374-1384: pre-existing HIGH producer limitation recorded; `_build_request_and_decision` sets `supplement_manifest: None` and no `source_bindings`; HIGH prepare/adopt threads the unsupplemented package.
- 1385-1423: test manually copies HIGH package, adds `authority_supplement`, supplement contract/rule, task `authority_supplement_source_ids`, and request `source_bindings`.
- 1428-1454: direct LOW `build_revision_cards_views_from_paths` + `accept_revision_evidence_views_from_paths` on that manually supplemented package.
- 1467-1475: `high.adopt_revision` is called on the **original unsupplemented** revision, not the supplemented `supp-candidate`, then readback/check.

Thus LOW direct supplemented package plus direct LOW card/view/acceptance is unit-supported, but HIGH prepare plus HIGH adopt with supplements has no test and no producer wiring. The later HIGH adopt does not adopt the supplemented products.

## 6. Nuance — lack of prepare override does not prove every manual LOW + complete R manifest + HIGH adopt composition forbidden

Inspected HIGH adopt predicates do not contain an explicit "package must lack `authority_supplement`" refusal:

- `adopt_revision` (1210) calls `low.prove_revision_from_paths` over manifest + decision + retained COPY. Proof validates the NEW graph via real content cores (`_validate_evidence_acceptance_content`, `_validate_edition_views_acceptance_content`, ledger/completeness cores), binds manifest FILE SHA, decision `manifest_ref`/`before_state`, affected==allowlist, `raw_refs` existence plus claim-bytes-in-Raw routing, OLD vs NEW identity/binding checks, affected-must-differ plus Raw binding, unaffected-must-match, mechanical projections, tool-pin drift refusal, and proof-schema validation. It does not check which function built the package. The content cores already handle supplemented packages: `_check_evidence_tasks_content` (1124-1141) enforces exact supplement binding (every supplement source bound exactly once by its task; task supplement IDs require manifest; supplement contract requires manifest), and `_validate_evidence_package_basis_content` / LOW builders thread `_resolve_phase_supplement_context` with `implementation_sha=None` as DATA loading, not LIVE validation.
- Manifest `candidate_outputs.supplement_manifest` is `request.get("supplement_manifest")` passthrough (786); if request carries a SizedRef it is recorded. Proof `proposed` (proof schema 19) has no `supplement_manifest` row — supplement authority is carried only if the NEW package itself carries `authority_supplement`. Retention is exactly seven canonical slots (manifest schema 28); supplement Raw files are not retained in HIGH inventory — direct LOW validation reads the manifest-declared `raw_path` at its existing path.
- Adopt additionally checks HEAD/tree/contract/tool drift, LIVE==before, retention inventory == manifest snapshots, guard absent, no-prior-Human-review window, DM016/DM017 P1-P4 gates, and decision binding. None of these is a supplement-shape refusal in itself.

Therefore a manually supplemented HIGH package (OLD `authority_supplement` path/sha carried, supplement contract entry added, supplement rule appended, per-task `authority_supplement_source_ids` restored from supplement manifest entries filtered by `evidence_task_id` with recomputed task SHAs, OLD prompt/contracts preserved, Discovery/Screening basis unchanged) plus schema-valid `source_bindings` plus SizedRef `supplement_manifest` in request/manifest **is not proven forbidden by prepare-override absence alone**. It is untested: no complete supplemented R (ledger/completeness/manifest/proof/retention/guard/checkpoint) has been built or proven, and proof/retention/supplement-Raw interactions for a supplemented HIGH graph (mechanical projections with changed package SHA, ledger/completeness basis propagation, Raw-at-existing-path vs retention inventory) have no passing observation.

Critically, **no normal existing public whole writer covers that construction**:

- The sole public whole-R writer is HIGH `prepare_revision` (plus `adopt`/`resume`/`readback`). It has no supplement carry.
- `prepare_evidence_package` (828-986) DOES carry supplements (`supplement_manifest_path` → `validate_evidence_authority_supplement` → `supplement_entries` → per-task IDs 927-943 → `package["authority_supplement"]` + `contracts["supplement"]` + rule 975-983, with field/content checks 1061-1141). But it is a different lifecycle (CANDIDATES_NORMALIZED-time Evidence package requiring `verify_state_basis` on LIVE State, not same-State revision with before-COPY/retention/guard/supersession/checkpoint/State-switch). It cannot be substituted for `build_revision_package_from_paths` without bespoke mirrored operator construction replicating HIGH's exclusive-write, pin, FULL validation, manifest SizedRefs, retention inventory, proof mechanical projections, guard/checkpoint/State-switch/clear/verify ordering for all 401/28 unaffected plus affected IDs.

The test's `supp-candidate` pattern (1385-1423) demonstrates only the package/task/request supplement shape for one derived DID, not a complete R. So the forbidden-composition claim is unproven, but the supported-whole-path claim is also unproven — and the only way to realize it today is bespoke mirrored production outside the versioned producer.

## 7. Narrow missing production capability and minimum field/schema boundary

**Missing capability (producer/contract, not reader/B2/B4/new module):** HIGH revision-package supplement carry plus task IDs plus package/authority contract threading through genuine HIGH whole path — i.e. `build_revision_package_from_paths` must carry OLD `authority_supplement` (path/sha), add the supplement contract entry and rule, set per-task `authority_supplement_source_ids` from the validated supplement manifest, recompute task SHAs/metas, while preserving Discovery/Screening basis, OLD prompt/contracts, and all HIGH prepare invariants (COPY SHA bind, previous-checkpoint OLD fallback, DS context true R/E, package/tasks adjacency, FULL validators after each write, manifest SizedRefs, retention inventory, proof/retention/guard/checkpoint/State-switch/clear/verify sequence).

**Minimum existing field/schema boundary (no new schema/family required):**

- Request already has `supplement_manifest` nullable SizedRef (request schema 7,37) and `source_bindings` optional on records (149,184,214).
- Manifest already has `candidate_outputs.supplement_manifest` nullable SizedRef (manifest schema 37,47).
- Package already has optional `authority_supplement` `{path,sha256}` (package schema 12,99) and optional supplement contract `{path,sha256}` (77-85); task metas already allow optional `authority_supplement_source_ids` (99).
- Task already has optional `authority_supplement_source_ids` (task schema 15); content cores already validate the supplemented shape (1061-1141).
- Proof already binds supplement authority via the NEW package itself plus `result_set_sha256`/`view_set_sha256` digests and explicit mechanical projections (proof schema 19; `prove_revision_from_paths` 3341-3479). No separate proof supplement row or new proof family is needed for minimal repair.
- Retention remains seven slots; supplement Raw stays at its existing manifest-declared path (same as direct LOW validation). No retention-schema change is part of the minimum.

Do NOT infer a new proof schema, new supplement family, new module, global/epoch cache, caller verified-dict, public bypass flag, or third mirrored validator. None is required for the minimum and none is selected.

## 8. Total-work / current-reuse tradeoff (concrete, no line budget, no future full reader)

- **Option R (recommended): bounded repair of the existing producer carrying supplements across the genuine HIGH whole path.** Reuses: existing `validate_evidence_authority_supplement` DATA path (`implementation_sha=None` already used in LOW), existing `_resolve_phase_supplement_context` / `_merge_supplement_task_sources` / `_build_card_core` / `_validate_card_core`, existing package/task/request/manifest schemas (no migration), existing HIGH whole-R sequence (prepare → ledger/completeness → manifest → prove → report → checkpoint → guard → State switch → clear → verify → resume/readback) with only package/task derivation changed. Must still preserve: 401/28 unaffected supplement bindings exactly (else proof refuses), OLD prompt/contracts, Discovery/Screening basis, `COPY bytes == request SHA`, `COPY != LIVE`, keyword-only `request_path`/`before_copy_path`, true root R/E, no caller dict/bypass, DM016 taxonomy refusal, DM017 union with unchanged full validator, declaration-loss gate, seven-slot retention inventory (currently absent), guard coordination, mechanical-projection explicitness. Cost is a scoped producer change plus genuinely needed affected tests plus fresh CURRENT proof plus independent implementation review — not a generic reader, not a full-tree rerun, not an R4/PDF suite.
- **Option W (bespoke ~1000-line operator workaround): higher cost, lower authority.** Would duplicate HIGH's whole-R assembly outside the versioned producer (exclusive writes, pins, FULL content validations, manifest SizedRefs, retention inventory, proof, report, checkpoint, guard, State switch, clearing, verification, resume, HEAD/tree/contract/tool predicates, DM016/DM017 gates) for every revision, without contract authority. Must still make the same supplement-shape decisions as Option R, then additionally re-prove the mirror's equivalence to HIGH on every path including all unaffected rows, retention/guard/resume failure seams, and downstream Selection→Architecture→Draft/Reader consumers. No reuse of HIGH whole-path assurance; creates a second unreviewed writer and retention/proof divergence risk. Rejected as production capability.
- **Option M (metadata-only / narrow scope): false economy.** Saves implementation work but forfeits the very Selection substance that necessitates correction: W34 paper box cannot cite body snippets (abstract-triage only, `technical_claims_accepted:false`), SP D141/D142 as-of claims and O10 as-of VERIFIED remain impossible, page/budget/tiering corrections stay ungrounded. The honest ceiling (W34 no-paper scope with corrected arithmetic; SP HOLD+LIMITATION with D143 PRIMARY promotion and lineage quarantine) is already available without any State mutation and should be selected explicitly if correction is not pursued — but it must not be labeled as completion of the correction.

Future full-reader investment, R4 audit, PDF/production, adoption/savings measurement, and SP archive fetch (D142 body, ≤09-21 snapshots, G1/G2 as-of pins) are separate decisions with separate authorities and are not part of this tradeoff.

## 9. Selected next-unit recommendation

**Select next bounded repair of the existing producer (Option R) before any same-stage retry, subject to prior Root scope confirmation and the mandatory §10/B4 map plus Astra plus independent readiness BEFORE code.**

Concretely, the next unit is a **bounded producer-repair pre-code map + scoped implementation** limited to:

1. HIGH `build_revision_package_from_paths` supplement carry (OLD `authority_supplement` + supplement contract/rule + per-task `authority_supplement_source_ids` + recomputed SHAs/metas) with unchanged Discovery/Screening/OLD prompt/contracts basis.
2. Request builder `supplement_manifest` SizedRef plus schema-valid `source_bindings` threading (currently `None`/unset in HIGH test helper).
3. HIGH `prepare_revision` / `adopt_revision` / `prove_revision_from_paths` / retention/guard/checkpoint/State-switch threading validation that the supplemented NEW graph passes FULL content cores, unaffected comparison, ledger/completeness validation, and mechanical-projection explicitness for full409 (W34) and full160 (SP) sets — not a single-DID probe.

**Exact functions/invariants the repair must bind (pre-code deliverables, no code in this review):**

- `survey_research_authority_v2.build_revision_package_from_paths` (2128): OLD supplement load path, `authority_supplement` copy predicate, task-ID derivation from validated supplement entries keyed by `evidence_task_id`, supplement contract/rule insertion, task SHA recompute, package field/content checks (`_check_evidence_package_fields_content`, `_check_evidence_tasks_content`).
- `survey_research_authority_v2.build_revision_cards_views_from_paths` (2277) + `accept_revision_evidence_views_from_paths` (2457): unchanged LOW supplement resolution (`_resolve_phase_supplement_context` 300, `_merge_supplement_task_sources` 469, `_build_card_core` 2228, `_validate_card_core`) with HIGH-supplied supplemented package; `before_copy_path` required keyword-only, `COPY bytes == request SHA`, true R/E via `derive_ordinary_root_effective_context`.
- `survey_prearchitecture_acceptance_v2.prepare_revision` (456, 636, 651, 671-676, 761-793): package/task write exclusivity, FULL validators after each write, manifest `candidate_outputs.supplement_manifest` binding to request SizedRef, seven-slot retention inventory (absent recorded as absent), HEAD/tree/contract/tool pins.
- `survey_research_authority_v2.prove_revision_from_paths` (3080): affected-must-differ plus Raw claim-bytes routing, unaffected-must-match (cards + ledger rows), task-identity/Discovery-binding identity, mechanical projections explicit, tool-pin drift refusal, proof-schema conformance without new family.
- `survey_prearchitecture_acceptance_v2.adopt_revision` (1100): LIVE==before, retention==manifest, guard claim/revalidate/release, no-prior-Human-review window, DM016/DM017 gates, decision binds manifest FILE SHA, checkpoint `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` truthful lifecycle/producer boundary, known-byte State triplet switch, checked seven-slot clearing, postread/verification.
- CLI (1483-1521): no new flags implied; supplement selection travels in the versioned request/manifest, not CLI options.

SP correction additionally requires Root limited archive-access decision (D142 body, 3 TypeSafe ≤09-21 snapshots; G1/G2 only if as-of deployment claimed) BEFORE any SP pre-code map. W34 4-ID correction is window-eligible on ID/provenance grounds (captured bodies/SHAs/sections already in ledger/raw) but content sufficiency (bounded AUTHOR_CLAIM PARTIAL claim sets, independent research decision, complete-graph revalidation) remains to be authored/reviewed, not assumed. Neither proceeds to author code in this unit.

## 10. Bounds + stop

- This is a read-only selection-dependency decision. No source edits, imports, runtime, tests, builds, fixtures, restores, network, Git/HEAD/status/log readback, ordinary Commit/Push, Human readback, or Production mutation was performed or is selected.
- Uses only selected `e84` plus authorized packet DATA (fixed774/c8 + 17 SP URLs/version metadata + P1-P6/publisher intake/supplement captures as DATA, never refetched). No new standing crawl, current-main following, local Production checkout, code/weights adoption, or standing main-follow authority.
- Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN.
- **Human Commit Point — stop; do NOT auto-start pre-code, implementation, rehearsal, R4, or new feature unit.** Ordinary Commit/Push Human-owned.
