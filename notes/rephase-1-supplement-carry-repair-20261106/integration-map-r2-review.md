# Supplement-carry integration-map r2 independent review addendum (scoped pre-implementation re-confirmation)

Role: NEW independent scoped pre-implementation reviewer (r2 re-confirmation), not map author, not Astra/root, not implementer, not prior reviewer, not Human.
Date: 2026-11-06.
Method: read-only source inspection + packet DATA join. No source edits, import, test, runtime, Git/HEAD/status/log readback, network, Production checkout/mutation, reconstruct readback, or subagents.

Read scope (explicit):

- `notes/rephase-1-supplement-carry-repair-20261106/integration-map-r2.md` FULL (§§1-7).
- `notes/rephase-1-supplement-carry-repair-20261106/integration-map-r2-machine.json` FULL (pretty-printed, 160 lines, fully read — not truncated).
- Prior `integration-map-independent-review.md` FULL (§§1-5, 10 corrections) + `integration-map.md` r1 (superseded details, preserved gap/boundary).
- `README.md`, `test-oracle-inventory.md` FULL, `astra-working-resolution.md` FULL §§4-6, `actual-dm022-supplement-operation-map.md` FULL, `independent-correction-capability-review.md` FULL, assessment §§3/5.
- Actual source final139 proof-copy (reuse prior line-verified pins; no re-execution): LOW builder 2128-2274, cards 2277-2454, HIGH prepare 456-814 (636/638-641/651/786/796), adopt 1100-1329 (prove 1210), tools 437-453, evidence supplement 300-451/523-635/828-986/989-1141/1144-1200/453-520/2228-2356, history kernel 1510-1684/1735-1858/1861-1910/1959-2115 (2066-2076), helpers 263/297-307/1231, prove 3080-3479 (3204-3206/3298/3325/3362-3376/3383-3388/3395-3407/3415-3428/3431-3440), schemas (request 7,37; manifest 37,47 + 7 slots; proof 19; package 12,99 + 77-85).

## 1. Verdict

**PRE_IMPLEMENTATION_READY (scoped to r2; concrete, bounded).**

R2 addresses all 10 prior corrections concretely, surfaces LOW package + prove + HIGH binding seams (no LOW-only claim), and stays within the existing-fields/module/callback/guard/retention boundary with contradiction-returns-to-root. No broad recycle. One inline clarification (§2.8, within the already-selected prove seam, no schema/module change) should be included during implementation; it is not a redesign and needs no new review cycle.

Scoped READY recorded here; code proceeds only after root also confirms r2 per the README gate. Unit ongoing — no author Commit Point until implementation complete or an actual new blocker.

## 2. Checklist against source + prior corrections

### 2.1 Three seams surfaced, no LOW-only claim — PASS

R2 §5 lists LOW `build_revision_package_from_paths` internals + LOW `prove_revision_from_paths` cross-check + small HIGH `prepare_revision` seam (verify + equality + recheck before writes/manifest), signatures unchanged, CLI unchanged. This matches source: sole whole-R writer is HIGH prepare 636; prove 3080 binds manifest/decision/COPY + FULL content cores; adopt 1210 has no supplement refusal. R1's LOW-only gap is closed.

### 2.2 COPY true R/E effective + sourceRoot — PASS

R2 §2 requires `ds_context = derive_ordinary_root_effective_context` (COPY-only, never LIVE), `screening_acceptance=ds.screening_acceptance` + `discoveries=ds.effective_records` (NOT root; tasks derive from effective 2183-2184; kernel binds request.discovery_ref to effective 1630-1644), `expected_source_root`=COPY-bound profile source_root (same predicate as 879-881, COPY-bound), `expected_discovery/screening` paths = request SizedRef paths, `implementation_sha=None` with both values non-None (never None+None fallback). Refusals enumerated (unknown/DROP/identity/class/duplicate/Raw-drift/symlink). Matches validator 497-635 and kernel. Using root would reject valid DERIVED bindings — r2 fixes this.

### 2.3 Before-pins + all-Raw return checks, no future-path pins — PASS

R2 §3 requires pins BEFORE validation (request/COPY/OLD prompt+non-supplement contracts/OLD authority/selected manifest/basis + ALL manifest raw_refs, never task-subset per 311-313/369-376), `_capture` + `_recheck_supplement_context` + `_recheck_phase_pins` + `_finish_authority_phase` (389-451, cards 2444-2446, no reseal, MappingProxyType discarded, no cache), and explicitly forbids future-object pins (`_planned_ref` outputs are return values, not pre-validation inputs). Matches `_capture` 232/`_recheck` 249/`_finish` 427 discipline.

### 2.4 Decoy cross-check + SizedRef bytes — PASS (with §2.8 clarification)

R2 §5 names the hole (passthrough 786 unverified; prove 3204-3206 never verifies request.supplement_manifest; proof proposed has no supplement row), then requires `_sized_ref_shape` (263) + `_verify_sized_ref_bytes` (297: SHA + byte_count>=1, repo-local, no symlink/traversal) before any package/task write, `package.authority_supplement == validated request {path,sha256}`, `candidate_outputs.supplement_manifest == verified request value` (HIGH seam), and prove verifies request manifest + enforces equals NEW package authority (null ⇒ no authority). Correct triangle request↔package; see §2.8 for the manifest↔request leg in prove.

### 2.5 Null policy + new-only non-DROP IDs — PASS

R2 §4 matrix is explicit and NEW-revision-only (never retroactive): null+null unsupplemented compat (keeps 615/486); null+non-null novel addition (fixture; D142 blocked without body authority); supp+same unchanged (W34 401); supp+different replaced (SP 27+3); supp+null builder fail-fast in `build_revision_package_from_paths` (not eventual proof). Record coverage reuses `derive_before_context:2066-2076` (records exact non-DROP, affected nonempty unique subset of non-DROP + known DIDs). Matches task predicate 927-931 + `_check` 1124-1140 + validator DROP/unknown/identity guards.

### 2.6 Normalize only allowed mechanical projections — PASS

R2 §4 forbids preserving OLD SHAs without recompute or dropping IDs, requires deterministic task recreate (`stable_task_id`/`task_filename`/`core.json_bytes`/sorted IDs) with byte-identical unchanged tasks, and limits exclusions to actually-emitted-when-differing mechanical projections 3415-3428 (9 listed SHAs). Cards unaffected `old_doc != new_doc` refuses (3383-3388); ledger unaffected identical (3405-3407). No card-semantic normalization allowed. Matches prove.

### 2.7 Existing fields/module/family/callback/guard/retention unchanged — PASS

R2 §5: signatures unchanged, no new flags (supplement in versioned request/manifest), one narrow shared private helper in existing `survey_research_authority_v2.py` only (no new module/staticmethod/cache/public verified-dict; re-derive ds/request bytes each time, never old self-passed metadata), records verbatim via 796 copy (no stripping), write-window noted (638-641 before 651; fresh revision root; never claim zero-all-write), retention 7 slots + guard/checkpoint/State-switch order unchanged, contradiction returns to root before broadening. Contract8 UNCHANGED (scripts/tests absent from identity; 5 DM022 schemas in pipeline+pins so no schema change); tool SHAs WILL change (edited module + small HIGH seam) with fresh pins + expected_head/tree. No public bypass, no mirrored producer — repair stays in the existing producer.

### 2.8 One inline clarification (non-blocking, within selected prove seam)

Prove re-verifies tasks/cards/views per-file refs (3237-3243) as tamper-evidence. For the same defense-in-depth, the prove seam should also enforce `manifest.candidate_outputs.supplement_manifest == request.supplement_manifest` (both null, or equal SizedRef with byte-verified file) alongside the required request↔package check. HIGH prepare already enforces manifest==request at prepare; this adds the prove-time re-enforcement for a crafted manifest+decision pair. Two-line check, no schema/module change, consistent with the selected seam. Include during implementation; no new design or re-review needed.

### 2.9 No-supp history preserved; add/replace without bypass — PASS

Null+null compat + A2/C regressions kept; novel addition and replaced carry via existing producer + FULL cores (no bypass flag, no operator mirror). Correct per ROOT §5.

### 2.10 Workcopy: already-applied 139, no reapply — PASS

R2 §7: do NOT apply 139 patch on the already-applied copy; independent copy of all 771 files + object separation (inert origin, no alternates/hardlinks/shared objects, process-scoped identity, no empty commits, no HOME/git-config mutation); apply-check only NEW clean409 proof when packaging final DIRECT. Minimal raw listed; network/Production/reconstruct-Git/old-runner/e84-mutation forbidden. Matches delivery discipline.

### 2.11 Tests: ≥3 non-DROP, DERIVED + Special both HIGH, fresh CURRENT API — PASS

R2 §6: each supplemented HIGH positive ≥1 affected + ≥1 unaffected supplement-bound + ≥1 Discovery-only (≥3 tasks/DIDs, ≥2 non-DROP), asserts package authority/contract/task IDs/card sources/byte-identical unchanged/ledger identity/Discovery→task identity/`rows_checked` covering non-DROP + ledger rows; versions unchanged + replaced + novel-addition + no-supp compat; routes BOTH WEEKLY DERIVED (304 pattern) AND THEMATIC/Special whole HIGH prepare→adopt/resume/readback + repeat anchor (946-968) with recorded Thematic limitation if not extended (ordinary-path 828/927b); negatives include decoy mismatch + unaffected reject + all late/readback oracles (807/888/950/1124/1327/1603/1662); forbids token echo (786), patched validators, manual supp-candidate as HIGH witness, fake/stub proofs; targeted subset §9 only. Fresh `verify_renewal_source_proof` CURRENT via actual API required (old proofs stale when 2 modules change G76 + pins). Full 409/160 correction needs separate semantic review, not test count. Concrete and scoped.

## 3. Bounds + stop

- Scoped pre-implementation re-confirmation only. No source edits, imports, tests, runtime, Git, network, Production, readback, or subagents performed or selected.
- Reuses only final139 proof-copy + authorized packet DATA (fixed774/c8 + 17 SP URLs/version metadata + P1-P6/publisher intake/supplement captures as DATA, never refetched). Three-archive-URL permission used/completed, not standing.
- Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN.
- Unit ongoing — no author Commit Point until implementation complete or an actual new blocker. Ordinary Commit/Push Human-owned. Implementation may proceed on an isolated workcopy per r2 only after root also confirms r2.
