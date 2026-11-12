# Supplement-carry integration-map independent review (scoped pre-implementation)

Role: NEW independent scoped pre-implementation reviewer, not map author, not Astra/root, not implementer, not prior reviewer, not Human.
Date: 2026-11-06.
Method: read-only source inspection + packet DATA join. No execution, import, test, restore, Git/HEAD/status/log readback, network, Production checkout/mutation, reconstruct readback, or source edits. No subagents.

Read scope (explicit):

- `notes/rephase-1-supplement-carry-repair-20261106/README.md` FULL.
- `notes/rephase-1-supplement-carry-repair-20261106/integration-map.md` FULL (review target).
- `notes/rephase-1-supplement-carry-repair-20261106/integration-map-machine.json` PARTIAL (single-line file truncated by 2000-char read limit; base/carry_gap/change_surface/oracles prefix observed, remainder not used as authority beyond md).
- `notes/rephase-1-supplement-carry-repair-20261106/test-oracle-inventory.md` FULL (§§1-11).
- `notes/rephase-1-selection-architecture-20261105/astra-working-resolution.md` FULL (§§1-6; §5 selected repair + §4 supersession + §6 qualifications binding).
- `notes/rephase-1-selection-architecture-20261105/actual-dm022-supplement-operation-map.md` FULL.
- `notes/rephase-1-selection-architecture-20261105/independent-correction-capability-review.md` FULL (§§1-10).
- `outputs/rephase-1-selection-architecture-assessment.md` §§3/5 (operation gap + selected task).
- Actual source: final139 applied proof `.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60` (preferred; final test 7b). e84 instance not re-read; prior e84 observations reused as DATA only.

Source pins checked (SRC = proof-copy above):

- LOW builder `scripts/survey_research_authority_v2.py:2128-2274` (OLD copy 2257-2258, tasks 2211-2228, package dict 2243-2265, checks 2267-2270).
- LOW cards `survey_research_authority_v2.py:2277-2454` (pins 2305-2330, basis 2342-2348, supplement ctx 2350-2355 with None/None, task→record 2383-2385, card build 2399-2411, `_finish_authority_phase` 2444-2446).
- HIGH prepare `scripts/survey_prearchitecture_acceptance_v2.py:456-814` (sole package call 636, writes 638-641, cards call 651, manifest 761-793 with passthrough 786, request verbatim copy 796).
- HIGH adopt `survey_prearchitecture_acceptance_v2.py:1100-1329` (prove call 1210, no supplement-shape refusal).
- Contract/tools `survey_prearchitecture_acceptance_v2.py:437-453` (7 pinned paths).
- Evidence supplement `scripts/survey_evidence_v2.py:300-451` (`_resolve_phase_supplement_context` 300, empty-context 322-330, `_recheck` 389, `_finish` 427), validator 523-635 (unknown 607-608, DROP 611-612, task identity 613-614, Raw SHA/bytes 627-634), builder 638-687, `prepare_evidence_package` 828-986 (IDs 927-931, authority 975-983), task validator 989-1021, package files 1036-1072 (supplement contract 1061-1067), tasks content 1074-1141 (exact-once 1124-1136, IDs-require-manifest 1137-1138, contract-requires-manifest 1139-1140), basis content 1144-1200 (supplement via `_supplement_entries_for_package` 1194-1198), `_discovery_task_sources` 453, `_merge` 469-494, `_supplement_source_file` 497-520, `_build_card_core` 2228-2356 (bindings gate 2243-2247), `_validate_card_core` 1270+.
- LOW history `survey_research_authority_v2.py:1861-1910` (ordinary COPY loader), kernel 1510-1684 (E binding 1630-1651, effective vs root), `_context_from_before_state` 1735-1858, `derive_before_context` 1959-2115 (records exact non-DROP 2073-2076), helpers `_sized_ref_shape` 263, `_verify_sized_ref_bytes` 297-307 (SHA+byte_count), `load_revision_request` 1231.
- Prove `survey_research_authority_v2.py:3080-3479` (request profile/discovery/screening byte verify 3204-3206, no supplement_manifest verify; task identity 3298, Discovery→task 3325, affected-must-differ + Raw routing 3362-3376, unaffected refuse 3383-3388, ledger 3394-3407, mechanical 3415-3428, tool pins 3431-3440; proposed schema has no supplement row).
- Schemas: request `dm022-revision-request-v2.schema.json:7,37` (supplement_manifest null|SizedRef), manifest `dm022-revision-manifest-v2.schema.json:37,47` (candidate_outputs.supplement_manifest null|SizedRef, 7 slots), proof `dm022-revision-proof-v2.schema.json:19` (proposed has no supplement_manifest), package `evidence-v2-run-package.schema.json:12,99` (optional authority_supplement), `77-85` (optional supplement contract), task `15`/`99` (optional IDs).

## 1. Verdict

**CHANGES_REQUIRED — not PRE_IMPLEMENTATION_READY.**

The map correctly identifies the one-sentence gap, the existing LOW-function-only change surface, Contract8-same boundary, COPY true R/E order, and full HIGH prepare→adopt/resume/readback scope, and correctly supersedes the old B2/B4 whole-cycle claim per ROOT §4. Those parts are adequate and must be kept.

It is not ready for implementation because 10 minimal corrections below are missing or ambiguous. Each is a concrete map-text fix, not a new generic feature, not a reopened B2/B4 cycle, not a new schema/module/family. Implementation stays BLOCKED until the map author revises these points and root + a scoped reviewer re-confirm.

## 2. What the map gets right (keep)

- Gap sentence (§1): HIGH `prepare_revision:636` always calls LOW `build_revision_package_from_paths:2128` which copies only OLD prompt/contracts (2257-2258), never authority_supplement, never task IDs (2211-2228), ignores `request.supplement_manifest`; cards resolve empty context (322-330) and fail or go Discovery-only (2243-2247). Confirmed on source.
- Explicit nullable SizedRef, no OLD-carry fallback, no inference (§2 first line + schema refs). Correct; matches request schema 7,37 and manifest 37,47.
- LOW-function-only change, Contract8 same (§4): `build_revision_package_from_paths` internal supplement load/copy/task-SHA path only; callers `prepare:636` sole writer, cards/accept/prove/adopt/resume/readback/CLI unchanged unless contradiction returns to root. Adequate — no signature change is needed (request already carries SizedRef; package/task optional fields already exist; supplement travels in versioned request/manifest, no new CLI flags). Contract8 unchanged is correct (scripts/tests absent from `contract_identity`; schemas are in pipeline + tool pins so schema edits would change Contract8 — therefore no schema change in minimum).
- Tool-SHA consequence (§4): edited `survey_research_authority_v2.py` changes 7 pinned tool SHAs; requests must pin new SHAs + new expected_head/tree. Correct.
- HIGH flow pins→writes→rechecks (§3): COPY/validators unchanged order, `derive_ordinary_root_effective_context` true historical R/E (never E-as-R, never LIVE), caller writes exclusively (638-641), FULL validators after each write, 7-slot inventory, prove/report/checkpoint/guard/State-switch/clear/verify order. Correct structure.
- Existing supplements reused (§4): `_resolve_phase_supplement_context:300`, `_merge:469`, `_build_card_core:2228`, `_validate_card_core`, `_check_*_content:1024-1141`, `_validate_*_basis_content`, `validate_evidence_authority_supplement:523`, `derive_ordinary_root_effective_context`, `load_revision_request`, `stable_task_id/task_filename`. Correct — no public verified-dict, no global/epoch cache, no new validator.
- No new proof family/retention slot as initial boundary (§4) with contradiction-returns-to-root clause. Correct as boundary, not forced assumption (see §3.10).
- Test direction (§5): real HIGH prepare→adopt/resume/readback on isolated fixtures, WEEKLY DERIVED + THEMATIC/Special, affected+unaffected, negatives, no-supp compat, unchanged vs replaced, no stub proof. Correct direction; needs strengthening below.

## 3. Minimal map corrections required

### 3.1 SizedRef + sourceRoot/discovery/SCP bound to COPY true R/E (no LIVE)

Map §2 line 18 currently:

`validate_evidence_authority_supplement(repo_root, manifest_path, None, expected_issue_id, expected_discovery_path=request.discovery, expected_screening_path=request.screening, screening_acceptance=DS.s screening, discoveries=DS.root)`

Correct to:

- `Supplement SizedRef` itself must be verified first via `_verify_sized_ref_bytes` (SHA + `byte_count`, repo-local via `_repo_rel`/`_repo_file`, no symlink/traversal, `byte_count>=1`). Map says "path/sha/byte_count bind file bytes" but must name the helper and byte_count enforcement.
- `implementation_sha=None` (DATA loading, not LIVE validation) AND `screening_acceptance` + `discoveries` both non-None from `ds_context` (never None+None fallback which reloads manifest-declared paths via raw `load_json`/`read_jsonl` without Screening content validation).
- `expected_issue_id` = request `issue_id` (== COPY issue).
- Add missing `expected_source_root` = COPY-bound profile `source_root` (same as `prepare_evidence_package:879-881`). Without it sourceRoot escape is unbound.
- `expected_discovery_path` = request `discovery_ref.path` (== kernel-bound effective path), `expected_screening_acceptance_path` = request `screening_ref.path` (== SCP artifact). Keep as map says, but state they are request SizedRef paths already bound to E/SCP by the kernel (1630-1651).
- `screening_acceptance` = `ds_context["screening_acceptance"]` (COPY-bound SCP content, not LIVE).
- `discoveries` = `ds_context["effective_records"]`, NOT `DS.root`. Tasks derive from effective (2183-2184); supplement `discovery_id`/`evidence_task_id` must bind effective DIDs. Using root rejects valid DERIVED bindings (Weekly genuine DERIVED true R!=E) or accepts wrong set. Fix the `DS.root` wording.

### 3.2 All-Raw closure pin before validation + recheck before return

Map §2 line 29 says capture pins BEFORE validation (request SHA, COPY SHA, OLD prompt/contracts SHAs, OLD authority path/sha, selected manifest SHA/bytes, all Raw path/sha/bytes, basis Discovery/Screening SHAs). Keep, and add:

- Repaired LOW builder must obtain full `validated.entries` + `raw_refs` covering EVERY manifest source (never task-subset, never newly observed — same invariant as `_resolve_phase_supplement_context:311-313,369-376`), pin via `_capture_phase_pins`, and recheck before return via `_recheck_phase_pins`/`_recheck_supplement_context`/`_finish_authority_phase` pattern (no reseal). Map §3 line 30 says checks before return but does not name Raw recheck. Add it.
- Card/views path already does `_finish_authority_phase` (2444-2446) — map correctly keeps it unchanged; state explicitly that the new package path must use the same no-reseal discipline.

### 3.3 Task IDs exact-one binding + DROP/unknown/extra + request-records coverage

Map §2 line 20 cites the `sorted(... evidence_task_id == task_id)` predicate (same as 927-931) and `_check_evidence_tasks_content:1124-1138`. Keep, and enumerate explicitly so the implementer cannot miss cases:

- Supplement validator refusals: unknown Discovery ID (607-608), DROP-targeting (611-612), task-identity mismatch vs `stable_task_id` (613-614), source_class mismatch (615-616), duplicate source IDs / ambiguous bindings (602-604,617-620), Raw `byte_count`/SHA drift + empty Raw (627-634), symlink/traversal/cross-source_root (497-520).
- Task/package content refusals: every supplement source bound exactly once by its task (1135-1136), task IDs require manifest (1137-1138), supplement contract requires manifest (1139-1140), meta IDs must equal task IDs (1111-1114), task filename deterministic (1105-1106), tasks cover every non-DROP exactly once (1118-1119).
- Add missing request-records coverage: `request.records` must cover exact non-DROP Discovery IDs (no new/omitted IDs, no DROP records, no extra unused records) — same predicate as `derive_before_context:2073-2076`. Current `build_revision_package_from_paths` only validates each record shape (2197-2201); cards builder only checks task→record (2383-2385), not record→task, so extra unused records would be silently ignored. Require the exact-coverage check before package derivation, plus `affected_ids` nonempty unique subset of non-DROP (2067-2072).

### 3.4 OLD prompt/contracts + supplement contract/rule + task/meta digests; novel addition + null-refusal matrix

Map §2 line 21 covers W34-unchanged (request manifest == OLD authority) and SP-replaced (NEW file, OLD prompt/contracts verbatim + supplement contract/rule to NEW schema SHA). Clarify and complete:

- Prompt verbatim from OLD; non-supplement contracts (`run_package`/`task`/`card`) verbatim from OLD (must still pass `_check_evidence_package_files_content` drift check against live files; drift refuses, never silently updated).
- Supplement contract set to live supplement-schema SHA (via `_repo_file` + rehash) + rule appended with the exact `prepare_evidence_package:981-983` string. When OLD null + NEW null: no supplement contract/rule. State that "verbatim + updated" means verbatim except the supplement entry.
- Task/meta digests: tasks deterministically reconstructed (sorted discovery order, `stable_task_id`, `task_filename`, same `source_records`/`verification_targets`/`screening_basis` + sorted supplement IDs), `task_raw` via `core.json_bytes`, SHA recomputed, meta path deterministic. Forbid preserving OLD task SHAs without recompute or dropping supplement IDs. Unchanged tasks must yield byte-identical files (required for proof unaffected equality).
- Add the full OLD/NEW matrix the map omits:
  - OLD null + NEW null → unsupplemented package (compat; current tests `:615`,`:486` preserved).
  - OLD null + NEW non-null → novel addition: add authority/contract/rule/IDs (needs a fixture test; real D142-new-source stays blocked on body unless root grants archive authority).
  - OLD supplemented + NEW same manifest → unchanged carry (W34).
  - OLD supplemented + NEW different manifest → replaced carry (SP 27+3).
  - OLD supplemented + NEW null → builder must refuse in `build_revision_package_from_paths` (would lose 401/28 bindings). Map says "null must refuse" but leaves the enforcement point ambiguous (builder vs eventual proof). Require fail-fast builder refusal. State explicitly this is NEW-revision-only and does not retroactively invalidate OLD accepted history.

### 3.5 Request/manifest/proof decoy fix (not merely schemas)

This is the largest gap. Current source: HIGH manifest `supplement_manifest = request.get(...)` passthrough (786) with no byte verify; prove verifies profile/discovery/screening SizedRef bytes (3204-3206) but never `request.supplement_manifest`; proof `proposed` has no supplement row (schema 19). A decoy request manifest (schema-valid SizedRef to an unrelated file) would pass schema + passthrough + proof while the package carries different/OLD/no authority.

Map §3 step 6 repeats "supplement_manifest passthrough" without verification/equality. Correct to (no new schema/family needed if these cross-checks are added; else return to root per §4):

- HIGH prepare: when request `supplement_manifest` non-null, `_verify_sized_ref_bytes` it before any package/task write; `package.authority_supplement` MUST equal validated request manifest `{path,sha256}` exactly (not OLD path when replaced); manifest `candidate_outputs.supplement_manifest` MUST equal the verified request value (not an unverified passthrough copy).
- Prove: when request `supplement_manifest` non-null, `_verify_sized_ref_bytes` it; enforce it equals NEW `package.authority_supplement` `{path,sha256}`; when null, enforce NEW package has no `authority_supplement`. Without this, proof binds supplement authority only via NEW package content cores but never binds the request/manifest decoy field.
- If prove/retention cannot bind the supplemented graph without a schema change (e.g., a new proof row or retention slot proves necessary), the implementer must return to root before broadening — do not silently add it.

### 3.6 Request-records semantic preservation (no normalization)

HIGH prepare already copies `request.json` verbatim (796). Require explicitly:

- `request.records` (including `source_bindings`, claims, verification, materiality, window/lineage fields) preserved verbatim; no stripping/normalizing of `source_bindings` or envelope/digest fields to hide authority.
- Cards built from exact records; `record.source_bindings` must explicitly select task-bound sources else `_build_card_core:2243-2247` refuses; unbound `supplement-src-*` refused; without bindings cards default to `src-1` Discovery-only (must be asserted in tests, not normalized away).

### 3.7 Caller signatures (confirm no change)

Map §4 is correct: no signature changes. `build_revision_package_from_paths(repo_root, request_path, before_copy_path, output_dir)` can load `request.supplement_manifest` internally + resolve the supplement file from the repo; no new param/flag/schema needed. Downstream `build_revision_cards_views_from_paths(..., *, before_copy_path)`, `accept_...`, `prove_...`, `adopt/resume/readback/CLI` unchanged. CLI unchanged (no new flags). Keep.

### 3.8 Tests: nonempty unaffected + no token/stub traps + full HIGH operation

Map §5 direction is right; make these mandatory and explicit (existing HIGH positives have no nonempty unaffected set; LOW manual `supp-candidate` is not a HIGH witness per test-oracle §§8-9 and operation-map §4):

- Each new supplemented HIGH positive must have ≥1 affected + ≥1 unaffected supplement-bound + ≥1 Discovery-only task (covers 401/28 patterns), with at least two non-DROP DIDs. Assert: package `authority_supplement` + supplement contract, per-task `authority_supplement_source_ids`, card `sources` naming task-bound `supplement-src-*` vs `src-1`, unchanged cards byte-identical, ledger rows identical for unaffected, task-identity + Discovery→task binding identical, `unaffected_comparison.rows_checked` covers all non-DROP + ledger rows (not just mechanical projections), `test_repeat_correction...:946-968` pattern extended.
- Forbid token trap: asserting only `revision-manifest.json candidate_outputs.supplement_manifest` echo (786) does not prove carry; must assert `candidate/package.json`, `candidate/tasks/*`, `candidate/results/*` bytes + `validate_evidence_card` + adopt/readback + `check_supersession_record_from_paths`.
- Forbid stub traps: no patched `_resolve_phase_supplement_context`/`_merge_supplement_task_sources`/`_build_card_core`/`validate_evidence_card`/`build_revision_package_from_paths`; no manual `supp-candidate` assembly as HIGH witness; no fake repo/empty root/stub proof. Must use real `high.prepare_revision` path + real validators (per test-oracle §8.257-265, including write-window note: card-build refusal may leave partial inert R files; use fresh revision root and assert actual R inventory/refusal).
- Require BOTH WEEKLY genuine DERIVED (true R!=E via `_chain_root_real_head` + derived-source pattern, `test_c_derived_weekly_true_r_not_equal_e:304`) AND THEMATIC/Special whole HIGH prepare→adopt/resume/readback. Note the known limitation from test-oracle §5: Thematic HIGH positive covers only Profile-initial obligations + COMPLETE closure; full 7-field/named/KEEP+DROP is covered on the ordinary path (`test_14:828`, `test_14b:927`). If the repair needs it on DM022 HIGH, add it; else record as limitation, never silently exclude Special.
- Negatives (each with exact refusal + no-write/inventory preservation): missing supplement file, `supplement_manifest` SHA/`byte_count` drift, Raw missing/SHA/`byte_count` drift + symlink/traversal/cross-source_root, wrong-DID binding, supplement targeting DROP, unknown DID, extra unused supplement source, `source_bindings` naming unbound `supplement-src-*`, task IDs without manifest, supplement contract without manifest, OLD-supplemented + NEW null refusal, late HEADER/tree/contract/tool drift (prepare vs adopt), guard present, retention mismatch.
- Add the late/readback oracles the map omits: late Raw drift after context before accept (807 pattern), late task mutation after load before accept (888), post-validation package field drift before first write (950), historical readback never reads LIVE (1124), readback mutation after check before return (1327), live/history views mutation (1603/1662).
- No-supp compat: OLD-unsupplemented history still passes with `supplement_manifest:null` (keep current A2/C tests as regressions, not decoration sweeps).
- Unchanged (W34 same) vs replaced (SP 27+3) both covered;SP D142-new-source stays blocked (no body) unless root grants archive authority.
- Targeted regression subset is test-oracle §9; do not run whole-suite sweeps or count-decoration tests. Heavy full-lifecycle/G71-G76/depth witnesses only if the repair changes publication/renewal behavior (they need TinyTeX/old proof copy).

### 3.9 CURRENT proof + delivery binding

Map §6 (771-file guard + patch `check0` before edits, exclusive-write logs, pin tables, FULL validator outputs, proof/report/checkpoint bytes, adopt/resume/readback outputs) is adequate; add explicitly: source edits to the 2 DM022 modules change G76 closure + HIGH tool pins (per test-oracle §10), so the delivery must bind fresh request/tool pins + new `expected_head/tree` and a fresh `verify_renewal_source_proof` CURRENT proof for the new workcopy (old recorded CURRENT proofs go stale). Test-only edits do not change closure/Contract8/pins. No network/Production/reconstruct-Git/readback, no old-runner rerun, no saved e84 mutation.

### 3.10 Minimum boundary is initial, not forced

Keep map §4's "Any contradiction returns to root before broadening" as binding. If during implementation the supplemented graph cannot pass FULL content cores / unaffected comparison / ledger/completeness / mechanical explicitness / retention-guard-checkpoint-State-switch for full409/160 without a schema/module/family change, the owner must return that concrete contradiction to root rather than silently broadening. This preserves ROOT §5 ("do not assume a new schema/module/family or public bypass is needed") as an initial boundary, not proof none is needed.

## 4. Test-oracle inventory assessment

The inventory is accurate and must be reused as DATA (not re-executed): LOW supplement oracles (§2), HIGH A2/C suites with `supplement_manifest:None` (615/486) (§3), DERIVED true R!=E witnesses (§4), Thematic obligation gap (§5), unaffected/CURRENT/digest gaps (§6), fixture helpers without public approval (§7), discriminating-positive design + token/patched-validator/write-window traps (§8), targeted regression subset + heavy exclusions (§9), closure memberships (§10: tests absent from Contract8/closure/pins; 2 DM022 modules + 5 schemas in G76/tool pins; `survey_evidence_v2.py` in staged/renewal closures but not HIGH pins). No test was executed for this review; all statements are inspection at the stated proof-copy path.

## 5. Bounds + stop

- This is a scoped pre-implementation review only. No source edits, imports, runtime, tests, builds, fixtures, restores, network, Git/HEAD/status/log readback, ordinary Commit/Push, Human readback, Draft/PDF, or Production mutation was performed or is selected.
- Uses only selected final139 proof-copy + authorized packet DATA (fixed774/c8 + 17 SP URLs/version metadata + P1-P6/publisher intake/supplement captures as DATA, never refetched). No new standing crawl, current-main following, local Production checkout, code/weights adoption, or standing main-follow authority. Three-archive-URL permission was used/completed, not standing.
- Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN.
- Human Commit Point — stop; do NOT auto-start implementation. Ordinary Commit/Push Human-owned. Code BLOCKED until this map is revised per §3 and root + a scoped reviewer re-confirm. This is not reopening the old general B2/B4 pre-code cycle and not authorizing new reader features.
