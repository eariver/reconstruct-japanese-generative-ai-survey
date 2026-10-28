# DM022 pre-Architecture — Task C guard / IO / HEAD-tree / public oracles (DESIGN ONLY)

2026-10-27 author-side pre-code C. **DESIGN ONLY. No runtime/import/tests/build/fixtures/restore/network/Git/source edits.**
Human `ab84b4f` assumed; 55 bare gitlinks preserved untouched (carryover `notes/rephase-1-dm022-prearchitecture-contract/source-and-carryover-observation.md`).

Read (read-only, no execution):

- `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351 B **INCLUDING §11**.
- `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` **INCLUDING §5**.
- BOTH independent reviews WITH FINAL-BINDING addenda (`independent-authority-design-review.md`, `independent-operation-design-review.md`).
- ACTUAL final93 proof-copy READONLY at `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60` (= actual `409b292` / tree `8ce36998` +93 paths 40M53A / 742 files; patch `f898d33b…` / manifest `d488c6ee…`; 5/5 spot pins matched in carryover §8; full93/742 NOT recertified here).

This file is the Task C return: exact seven-slot coordination map + failure/resume/write-set/HEAD-tree oracles + public oracle matrix. It defines predicates to be closed in pre-code readiness (§10–§11/root §5). It is **not** code, not approval, not a CommitPoint.

Selected order (binding, decision §§6–7/root R5):

```text
pin current basis
→ generate / review / prove immutable candidate (detached, pre-State)
→ retain COPYs + present/absent inventory
→ claim + revalidate guard
→ complete typed checkpoint
→ prevalidate exact expected State
→ ONE known-byte State triplet switch (ONLY evidence/materiality/completeness → SAME new record)
→ checked clearing of old unaccepted 7 slots
→ postread + inventory verification
→ release OWN guard
→ normal regeneration
```

No `clear-while-State-old then block-on-missing` window. No restore-on-swap-failure. No automatic rollback. No multi-file/CAS/crash atomicity.

---

## 1. Exact seven-slot boundary (decision §11.1, binding)

All seven paths are **relative to the validated Profile `source_root`** (`core.repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")`; `survey_agent_control_v2._profile_and_source:307`; `survey_production_v2.repo_local_path:282`). No invented `R`, no invented QA path, no invented absolute `source_root`, no `sources/<issue>` fabrication, no broad glob, no deletion of reviewer notes/raw/accepted dirs/history.

| # | Role | Relative slot | Config owner (`survey-production-v2.json:266-275`) | Current runner preflight |
|---|---|---|---|---|
| 1 | Matrix | `candidate-matrix-v2.json` | `EVIDENCE_REVIEWED` (`candidate-matrix`) | `run_selection_architecture_v2_interactive:193,199-201` guarded |
| 2 | Selection | `candidate-selection-v2.json` | `EVIDENCE_REVIEWED` (`candidate-selection`) | `run:194,199-201` guarded |
| 3 | Architecture | `architecture-v2.json` | `SELECTION_COMPLETE` (`issue-architecture`) | `run:195,199-201` guarded |
| 4 | Architecture summary | `architecture-review-summary-v2.json` | `SELECTION_COMPLETE` (`architecture-review-summary`) | `run:196,199-201` guarded |
| 5 | Architecture attention | `architecture-review-attention-v2.json` | `SELECTION_COMPLETE` (`architecture-review-attention`) | `run:197,199-201` guarded |
| 6 | Interactive input archive | `orchestration/v2/interactive/selection-architecture-input.json` | `EVIDENCE_REVIEWED` (`selection-architecture-input`) | `run:198-201` guarded; `run:328-329` `mkdir(parents)+shutil.copy2(input_path, archive_path)` producer |
| 7 | Interactive audit | `orchestration/v2/interactive/selection-architecture-audit.json` | **no `canonical_regeneration_artifacts` row** — execution provenance, not a regeneration artifact | **NOT guarded today**: `run:330-343` `core.write_json(audit_path, {...})` with `mkdir+copy2+write_json`, no existence/divergence check; binds `interactive_input={archive path,SHA}`, `runner`, five `outputs` refs (matrix/selection/architecture/summary/attention) — not itself |

Current preflight is **6, must become 7**. Successor normal runner no-overwrite/guard preflight MUST cover all seven including the audit; no divergent audit overwrite after adoption. Pre-code must exhibit the corrected writer/ownership/fault oracles for all seven (§§3–4, §7).

Retain-present / record-absent rule: preparation records which of the seven are present and copies exact bytes to owned retention; absent stays absent (not a deletion permission). Partial failed-run outputs are inventoried as partial, never fabricated into a complete reviewed result. The audit's `interactive_input` + five `outputs` refs must bind the captured old files if claimed as a complete old producer result. Unknown/foreign/changed files refuse; absent entries do not authorize deletion. Caller `input_path` (outside `source_root`, argv `--input`) vs generated `archive_path` (inside `source_root`) provenance MUST stay distinguished; copying equal bytes does not rebind a reviewed target.

Slots 3–5 are owned by `SELECTION_COMPLETE` per config yet written by the same pre-advance `EVIDENCE_REVIEWED` invocation (`run:158-168` requires `EVIDENCE_REVIEWED`; `193-343` writes all seven). Unaccepted bytes in all seven can therefore coexist with a pure `EVIDENCE_REVIEWED` State. That is the A1 blast radius — not three files.

---

## 2. B4 producer slot output paths / reference list + normal no-overwrite (pre-code OPEN)

B4 stays OPEN until pre-code binds actual producer output arguments, filenames, schema fields and current content-validator entrypoints, showing old canonical Ledger/Completeness are neither overwritten nor accidentally consumed, with no fabricated `CANDIDATES_NORMALIZED` runner invocation.

### 2.1 Versioned R outputs (new authority, NOT canonical overwrite)

Template only (decision §4): `R=<source_root>/research/v2/acceptance-revisions/<revision_id>` (safe single-segment id, exact Profile-derived root, no latest-scan selection). **No concrete `<revision_id>` invented here.** Pre-code must bind:

- New Evidence accepts: content-addressed new runs under owned revision namespace; unchanged complete runs reused ONLY at exact validated immutable refs. Entry validators: `survey_evidence_v2.validate_evidence_acceptance:1412`, `validate_evidence_card:965`, `validate_evidence_package_basis:898`.
- New Edition Views accepts: always a newly validated complete acceptance when cards/Views change; no partial overlay treated as accepted. Entry: `validate_edition_view:1437`, `validate_edition_views_acceptance:1555`.
- New versioned Ledger: newly generated versioned file under R. Pure builder: `survey_evidence_v2.build_materiality_ledger:1579` (+ `validate_materiality_ledger`, `_check_ledger_rows_content`). Writer for canonical path is `write_materiality_ledger:1797` (refuse-if-exists) — **NOT** to be called on the canonical path for R; pre-code must define the versioned write path that does NOT hit `source_root/materiality-ledger-v2.json`.
- New versioned Completeness: newly generated versioned file under R. Builder `run_evidence_v2_interactive._build_completeness:471` iterates ONLY `profile["research_scope"]["initial_obligations"]` (`486`); full validator `survey_completeness_v2:190-238` ALSO requires every Discovery-named `obligation_ids` (`213-223` `silently dropped named Discovery obligations`). Pre-code MUST preserve/validate the union of Profile-initial + existing Discovery-named obligations with exact provenance and consume explicitly provided complete rows through the unchanged full validator; it MUST NOT silently call the incomplete builder and claim completeness (DM017, decision §8).
- New package/task/result inputs bound to the actual pre-revision State + existing Discovery/Screening. Same-State production MUST NOT pretend the issue temporarily was `CANDIDATES_NORMALIZED`.

Old canonical `materiality-ledger-v2.json` / `profile-completeness-v2.json` stay byte-identical until State adoption; they become inactive ONLY via State provenance switch, never by overwrite or rebind-by-hash.

### 2.2 Normal no-overwrite that must be extended to seven

Existing refuses (all must remain, audit added):

- `run_selection_architecture_v2_interactive:199-201` — six-path `if path.exists(): raise … refusing to overwrite …` (matrix/selection/architecture/summary/attention/archive).
- `run:328-343` — archive `mkdir+copy2`, then **unguarded** audit `core.write_json`. Successor MUST add audit to the `199-201` set (or an equivalent exact seven-path preflight executed BEFORE any of the seven is written) AND gate both archive+audit creation on held guard (§4).
- `run_evidence_v2_interactive:715-717` Ledger `if exists: raise refusing to overwrite Materiality Ledger`; `:730-732` Completeness same; `survey_evidence_v2.write_materiality_ledger:1797-1799` same.
- `run_drafting_synthesis_v2_interactive:173-174` `if package/result exists: raise refusing existing Draft artifacts`; `:193-194` `if synthesis input/result or archive exists: raise`.
- `survey_architecture_v2_base:396,1176` writer no-overwrite guards (per authority review; pre-code must cite exact lines for the bound final93).
- `core.write_json:150-152` itself is `mkdir(parents, exist_ok=True)+write_bytes` — NO fsync, NO atomic rename, NO existence check. All atomicity/existence guarantees must come from caller preflight + guard + postread, not from `write_json`.

Pre-code must list for each of the seven: exact producer function, exact output argument/filename, exact schema file (`schemas/candidate-matrix-v2`, `candidate-selection-v2`, `issue-architecture-v2`, `architecture-review-summary-v2`, `architecture-review-attention-v2`, plus archive/audit envelope `schema_version 2.0-rc1` shape at `run:331-343`), and the current content-validator entrypoint (`schema_gate.validate_instance`, `architecture.validate_selection:249`, `architecture.validate_architecture:309`, `architecture.build_architecture_review_summary:317`, `review_attention.build_attention/validate_attention:325-326`).

`LOW` vs `HIGH` names (where they appear in renewal/history or checkpoint coordination prose) are abstract coordination labels for the schema owner in this design; they introduce NO new module, NO new file, NO new authority. The ONLY new record kind is fixed: `kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, reason `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION` (decision §5). No alternate kind strings.

---

## 3. Retention COPYs — before-copy inventory, accepted/Gate-bound scans, bytes+inode+identity after copy

Owned retention root is a NEW owned directory under the edition (Profile-derived, NOT a fabricated `sources/<issue>` path; exact path/schema pre-code). It holds:

- Mutable before-State COPY (exact bytes of the pinned LIVE `production-state.json`).
- Every PRESENT targeted unaccepted canonical output among the seven (exact bytes).
- Exact present/absent inventory + source refs.

### 3.1 Before-copy inventory (refuse-or-record, never fabricate)

For each of the seven, pre-code oracle MUST record:

1. `present: true/false` (via `Path.is_file()`, NOT via directory prefix scan).
2. If present: `bytes` (length), `sha256` (`core.sha256_file`), plus `st_dev/st_ino` (inode identity) observed read-only; NO hardlink creation, NO sharing claim.
3. Accepted/Human-bound scan: is this byte sequence referenced by ANY accepted checkpoint provenance (`state.checkpoint_provenance.*.{path,sha256}` live re-hash via `pubset.sha256_repo_file`), by `human_gate_provenance.architecture_review` / `publication_preview`, by `gates/review-index.json` rows, or by `gates/reviews/*-rN.json` approvals? If bound → **refuse clearing** (not unaccepted; not in plan). Old reviewed targets are NOT rebound by equal-byte copy.
4. Derivation staleness note: matrix `basis.{production_profile_sha256,candidate_matrix_sha256,profile_completeness_sha256,materiality_ledger_sha256}` (`run:235-240`), architecture `basis.{…candidate_matrix_sha256,candidate_selection_sha256…}` (`run:292-298`), review/attention derivation inputs (`run:316-325`) — record which upstream SHAs they bind, so post-adoption regeneration can prove fresh reasoning (not a same-byte copy).

Absent slots: record `present:false`; absent is NOT a deletion permission and does NOT block the normal generator (missing is its usual precondition — `run:199-201` loops `if exists: refuse`, absent proceeds).

### 3.2 After-copy verification (bytes + inode + identity)

After each COPY (`shutil.copy2`-equivalent preserving bytes; exact copy primitive pre-code):

- `bytes` equal, `sha256` equal (re-hash COPY).
- Record COPY `st_dev/st_ino` AND source `st_dev/st_ino`; they MUST differ as path identities (no same-file alias); NO inode-sharing certification beyond this pair observation.
- Source re-read: source `sha256` unchanged (no mutation during copy).
- Manifest row: `{slot, source_rel, copy_rel, present, bytes, source_sha256, copy_sha256, source_dev_ino, copy_dev_ino, accepted_bound: false, gate_bound: false}`. Any `accepted_bound:true` or `gate_bound:true` → remove from clear plan, preserve manifest, refuse that slot.

### 3.3 Changed / foreign files refuse

- If a present slot's bytes at copy time ≠ bytes at capture time (raced mutation) → refuse that slot, preserve both observations, INDETERMINATE for that slot (no clearing).
- If a NEW file appears at a planned slot path between inventory and unlink (foreign/new bytes) → preserve, refuse unlink, INDETERMINATE.
- If unknown files (not among the seven, not reviewer notes) appear in `orchestration/v2/interactive/` → they are NOT cleared by basename resemblance; only the exact seven relpaths are eligible.

---

## 4. Guard coordination map (transient, NOT a selector, NOT permission)

Guard is scoped exclusive transition coordination, checked by affected operational producers/advance/Gate preparation at entry AND before publishing outputs. It is NOT a second live authority pointer. Unknown/unreadable/mismatched guard fails closed. Strict read-only State/history diagnosis remains permitted while incomplete; it MUST NOT be confused with permission to proceed.

No generic guard-ignore flag. No lease-takeover. No cleanup-unknown. Guard-release failure has its own explicit row (§7).

### 4.1 Guard root / path / schema / owner binding (pre-code must pin)

Constraints (no invention beyond these; exact filename/schema pre-code):

- Root: derived from validated Profile `source_root` (same `repo_local_path` derivation as §1), inside the edition execution tree (e.g. under `orchestration/v2/` or edition `execution/`), NEVER outside `repo_root`, NEVER via traversal (`..`, absolute, backslash rejected by `repo_local_path:282-291`).
- Path: ONE exact file path (not a directory permission, not a glob). Pre-code must name it.
- Schema: minimal JSON object with at least `{schema_version, issue_id, operation:"PREARCHITECTURE_ACCEPTANCE_SUPERSESSION", revision_id, bound_state_sha256, bound_expected_state_sha256, holder:{executor, recorded_at, work_head, work_tree}, phase}` — exact field names pre-code; `issue_id` MUST equal State `issue_id`; `revision_id` MUST equal the owned R single segment.
- Owner binding: `holder` is the claiming attempt's identity (executor + invocation `generated_at`-style instant + work HEAD/tree, cf. `INPUT_NAME` runner metadata `run:56-58`). Guard file records `bound_state_sha256` = pinned before-State SHA and `bound_expected_state_sha256` = prevalidated expected-after SHA. A guard file whose `issue_id/revision_id/bound SHAs` do not match the reloading attempt is FOREIGN — never taken over, never deleted, never cleaned.
- Guard FD / inode / hash identity: claim MUST use exclusive creation (e.g. `O_CREAT|O_EXCL`, or atomic `mkdir` for a guard dir + write inside — exact primitive pre-code) and then HOLD an open FD (or re-stat `st_dev/st_ino` + re-hash on every check). Checks compare BOTH path identity (`st_dev/st_ino` of held/opened file) AND content hash (`sha256_file(guard_path)` vs `bound` record). `stale FD after unlink/replace` → treat as unknown/mismatched → fail closed. No `flock`-only or mtime-only guard.
- No existing counterpart: targeted grep finds NO DM022 guard in final93 (only retained-owned-partial and exclusive-create-fd idioms). Pre-code introduces it as NEW code; it MUST NOT be inferred as already present.

### 4.2 Every affected producer / advance / Gate surface that must check guard (not names-only)

Each row needs file:line citation + resolver-or-refuse disposition + concrete check for callers with NO State arg. Missing any unguarded normal writer blocks code (decision §6 completeness bar: “code cannot begin if an unguarded normal writer can regenerate stale outputs in this window”).

Verified normal surfaces (final93 proof-copy; pre-code must complete the list through Draft/Reader/publication proposal/retention/operator/handoff/Gate prep/checkpoint-history inspection):

| Surface | State arg? | Guard check required (entry + before publish) |
|---|---|---|
| `run_selection_architecture_v2_interactive.run:158` (`repo_root,state_path,input_path`) | YES — `validate_agent_state:164`, `lifecycle==EVIDENCE_REVIEWED:167-168`, six-path preflight `199-201` | MUST add: (a) seven-path preflight (incl. audit), (b) guard-held-by-self check at entry (phase `RETAIN→CHECKPOINT→SWITCH→CLEAR`), (c) guard revalidate before EACH `core.write_json` / `copy2` (`209,252,314,324-326,329,331`), (d) refuse if guard foreign/unknown/mismatched. Post-adoption normal regen runs ONLY with guard released + new State (fresh Matrix package). |
| `agent.advance_with_checkpoint:1768` (`repo_root,cfg,state_path,checkpoint_path`) | YES (State file) — canonical path `1771-1773`, lifecycle match `1778-1781`, same-authority-to-all-stage-checkpoints `1808-1812`, `core.write_json(state_path):1825` | MUST refuse DM022 supersession kind through this path (same-State `EVIDENCE→EVIDENCE` matches no `stage_plan` producer; `_producer_for_checkpoint:348-352` returns NONE; `_validate_checkpoint_record:493-500` lifecycle-producer mismatch). New supersession adoption is a SEPARATE single-writer/held-descriptor State-file replacement (§6), not `advance_with_checkpoint`. Guard must be held by self at adoption and checked at entry. |
| `survey_human_gate_v2._current_pending_gate:440-485` + `invalidate_pending_gate:1179-1348` + Gate presentation (`1019-1032` summary/attention load) | State-derived | MUST check guard before presenting Architecture Gate dossier: if guard held (transition incomplete) → refuse presentation (stale/mixed dossier risk). Read-only Gate-input diagnosis (bytes present?) remains allowed without proceeding. `gate_at_state:223-226` maps ONLY `ARCHITECTURE_ESTABLISHED→ARCHITECTURE_REVIEW`, `RELEASE_CANDIDATE→PUBLICATION_PREVIEW`; at `EVIDENCE_REVIEWED` lookup fails closed (`457-465`). Do NOT manufacture a Gate to use invalidation. |
| `run_drafting_synthesis_v2_interactive.main:150` + `_upstream:43` (requires `ARCHITECTURE_ESTABLISHED`+approved `45-47`, `validate_agent_state:50`, derives `source_root/profile/discovery/matrix/evidence/views/ledger/completeness/selection/architecture/review/approval:53-93`, matrix↔Evidence binding `70-73`) | YES (State file via `_upstream`) | Post-adoption Draft MUST resolve new Ledger/Completeness/Evidence/Views through the State-bound checkpoint interface (new four-ref resolver, §5), never old canonical singleton paths. Guard: refuse Draft while transition guard held (pre-regen or stale-clear window). Read-only Draft-input inspection allowed. |
| `run_evidence_v2_interactive` (Ledger `715-717` + Completeness `730-732` refuse-overwrite) + `survey_evidence_v2.write_materiality_ledger:1797` | State-adjacent (profile/source_root + implementation_sha) | These are the FORBIDDEN reuse paths for DM022 versioned R outputs: pre-code MUST show versioned R producer args/filenames/schema fields that do NOT call these canonical-path writers. If invoked in supersession mode with canonical paths → refuse. No-State-arg library calls (`build_materiality_ledger:1579`, `_build_completeness:471`) may be reused/extracted ONLY with the new operation's actual high-side LIVE eligibility + full proposed-graph checks, never with synthetic old lifecycle State. Guard check: refuse canonical Ledger/Completeness creation while supersession guard held unless it IS the versioned-R write under R. |
| `survey_agent_control.approve_architecture:1829` (reads canonical `architecture/review/attention:1846-1848`, binds approval `1866-1883`) + `survey_drafting_v2:130` / `survey_drafting_v2_base:124` / `run_semantic_publication_v2_interactive_base:139` / `survey_publication_v2:653,679` / `survey_orchestrator_v2:771-775` / `survey_stage_validation_v2:477-585` / `survey_handlers_v2:204-314` / Weekly/Longform derivation (`survey_weekly_derivation_v2:609-610`, `survey_longform_derivation_v2:1033`, `survey_editorial_correction_proposal_v2:1469,1508` per reviews) + operator/handoff/Gate prep + checkpoint/history inspection (`agent._validate_agent_state`, `core.validate_state_semantics:718`, `publication.validate_release_record` family) | MIXED — several take NO State arg (canonical `source_root/...` paths or handoff dicts only) | For EVERY no-State-arg normal mutation/validation reader: pre-code MUST give EITHER (a) concrete derived Profile-root guard check (resolve Profile → `source_root` → guard path → fail-closed if held by another intent / mismatched / unknown), OR (b) explicit `refuse in superseded mode` (detect new-kind checkpoint lineage and raise before reading old canonical Ledger/Completeness/Matrix/Selection). Names-only inventory (“listed but unchecked”) is NOT closure. B2 stays OPEN until this per-caller resolver-or-refuse map with file:line citations + post-acceptance tests is returned. |
| Later R1/editorial/renewal accepted-source/retention walkers (`survey_versioned_renewal_source_v2:653,998-999,1181-1182`, `survey_versioned_renewal_history_v2:124-127`, `survey_publication_set_v2:1213,1627,1981` prior-checkpoint loads, `survey_weekly_mechanical_refresh_v2:931`) | MIXED | MUST recognize new kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` (do NOT treat as unknown-producer reject after adoption, do NOT fall back to old canonical singleton). Exact disposition per walker pre-code. |

Read-only State/history diagnosis (`core.load_json(state_path)` + `validate_agent_state` / `validate_state_semantics` + `history` length/path check `core:760-780` / `agent:678-700`) NEVER requires guard and NEVER authorizes mutation/publication while guard is held.

---

## 5. Active research resolution throughout the later lifecycle (B2 rule, no whole duplication)

New active resolver returns ALL FOUR refs from the SAME selected typed checkpoint (`evidence-acceptance`, `edition-views-acceptance`, `materiality-ledger`, `profile-completeness` with full exact `{path,sha256}` + live re-hash), verifies lineage + same-record triplet, refuses split/mixed authority. Callers MUST NOT reopen old canonical Ledger/Completeness afterward.

- Creation/adoption restricted to §3 `EVIDENCE_REVIEWED` window (exact predicates decision §3: strict LIVE State+Profile validation via public agent validator, passed Discovery/Screening + Evidence/Materiality/Completeness with same-producer four artifacts, Selection/Architecture/Draft/publication-preview/Freeze/Release pending with no accepted provenance, no Human approval/index/request, no Exception, null publication revalidation pointer, same issue/Profile/Discovery/Screening, nonempty unique subset allowlist, no new Discovery/changed Screening).
- **Readback of the adopted checkpoint is NOT restricted to that lifecycle.** Normal forward `SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED→DRAFT_COMPLETE→…` MUST continue to validate/consume it with original operation context verified from retained before-State/lineage. Do NOT demand live State still equal before-State; do NOT pretend correction happened later. Historical/detached proof stays State-nonrecursive; operational eligibility + guard stay high-side. Agent normal public strict State validator keeps FULL existing predicates + precise new-kind branch (NOT a current-pinned `production.verify_state_basis` substitute — `core.verify_state_basis:959` is globally current-pinned, distinct from `agent.validate_agent_state:597` / `verify_agent_state_basis:941` resumable-State path).
- Public generation/validation readers that would otherwise go stale on old canonical Ledger after the switch and are tied to the `canonical_regeneration_artifacts` owner (`CANDIDATES_NORMALIZED` for ledger/completeness) are covered by that owner row: they resolve via the new State-selected graph (exact `{path,sha256}` + live SHA re-hash, no caller dict). This section does NOT duplicate the whole §4 table; it states the resolver invariant those rows implement.

Pre-state: a typed history CAN verify the pre-state record (detached/history validation via `_validate_checkpoint_record` with `historical_state.lifecycle=CANDIDATES_NORMALIZED`-style derivation + `_validate_core_stage_report`) WITHOUT the physical State being new. After-state: source readback MUST NOT require live-before equality; it validates current canonical State against recorded before/expected-after + retained lineage.

---

## 6. Selected order with phase predicates

`A` = owner of this attempt (executor+invocation). `R` = versioned revision dir (template §2.1, no concrete id here). `G` = guard file (§4.1). `S_before` / `S_after` = known-byte State files.

1. **Pin current basis.** `S_before = load(state_path)`; `validate_agent_state(repo_root,cfg,S_before)==[]`; `lifecycle==EVIDENCE_REVIEWED`; §3 window predicates hold; `implementation_sha=repository_commit_sha(repo_root)` (`core:189`: `git rev-parse HEAD`, 40-hex); `contract=contract_identity(...)` (`core:210`); record exact work HEAD/tree (§9) + committed tool/schema/contract files + full live evidence pins (package/task/result/card/View/Ledger/Completeness/criteria/prompt/schema). No current-main refresh, no schema migration.
2. **Generate / review / prove (detached).** Truthful new package/task/result under R bound to pre-revision State + existing Discovery/Screening; new Evidence/View content-addressed under R; Ledger/Completeness versioned under R; NO canonical overwrite. Externally supplied author-independent research/authority-consumption decision binds exact before/after graphs, affected IDs, Raw/event semantics. Complete proposed-graph revalidation (package/task/result sets+digests; card entity/claim/time/access; Views coverage+binding; Ledger dispositions/rationales; Completeness obligations+closure; unchanged Discovery/Screening/X/raw/Profile; allowlist + ALL unaffected semantic content with mechanical SHA-propagation explicitly mapped, never directory-prefix excluded). Proof leaf bound to proposed bytes, NEVER calls current State acceptance recursively; LIVE eligibility checked high-side separately.
3. **Retain COPYs + inventory** (§3). Mutable before-State + every PRESENT seven-slot byte → owned retention; present/absent manifest; accepted/Gate-bound scans (bound → remove from clear plan).
4. **Claim + revalidate guard** (§4). Exclusive-create `G` with `bound_state_sha256=sha256(S_before)` + `bound_expected_state_sha256` (from step 5 prevalidation plan); HOLD FD/inode identity; every affected writer checks `G` at entry.
5. **Complete typed checkpoint.** ONE record `kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`, with `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED` operation + `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED` producer boundary, roles Evidence/Materiality/Completeness + four named refs, before-State/COPY refs, Profile, predecessor+anchor, `supersedes`/lineage, request/affected-ID + retention-plan refs, proposed-graph proof, supplied decision, code/contract/work-ref observations, executor/time, self-digest. STRICT new checkpoint-schema branch + truthful supersession proof/report; NEVER forge old `CORE_STAGE_CONTRACT` lifecycle fields (`agent._validate_core_stage_report:365-443` pins `from==lifecycle,to==next_state:403-408`; schema `evidenceArtifacts` keys ONLY on `from_state==CANDIDATES_NORMALIZED:200-208`). Record complete BEFORE State switch. New field names/digest expressions pre-code.
6. **Prevalidate exact expected State.** Internally construct `S_expected` = `S_before` with ONLY `checkpoint_provenance.{evidence,materiality,completeness}` replaced TOGETHER by the SAME new record ref `{path,sha256}`; lifecycle/passed flags/history/Profile/initialization/other checkpoints/Human gates UNCHANGED. Validate `S_expected` as a plan (schema + `validate_agent_state` with new-kind branch). Still validate actual pinned LIVE State before mutation (no synthetic old State to producers, no hypothetical-State-as-authority).
7. **ONE known-byte State triplet switch.** Single complete State-file replacement (`core.write_json(state_path, S_expected)`-equivalent under single-writer/held-descriptor discipline) containing all three refs + full after-readback (`load+sha256+validate_agent_state+triplet same-record check`). This is ONE-record co-update ONLY — NOT cross-directory/guard/record/slot/filesystem/durability/crash atomicity. Failed after-readback with new/unknown bytes NEVER authorizes restoring before bytes (§7 INDETERMINATE).
8. **Checked clearing of old unaccepted slots.** ONLY remaining EXACT old planned slots (§§1/3/7); per-slot pre-unlink reverify (present + bytes/sha == captured old + still unaccepted/unbound + guard held by self); missing-already-cleared allowed; foreign/replaced bytes preserved+refused.
9. **Postread + inventory verification.** Full readback: active triplet resolves to new record; seven-slot present/absent matches expected (cleared absent unless regeneration already ran under released guard — which MUST NOT have run before release); retained COPYs intact; guard still held by self.
10. **Release OWN guard.** ONLY the holder releases (exact `st_dev/st_ino+hash` identity); release failure → stay blocked, explicit retry, NO auto-delete, NO silent proceed (§7 row).
11. **Normal regeneration.** Fresh Matrix/Selection/Architecture package against the NEW accepted graph with fresh independent reasoning + ordinary Architecture Human Gate later. Missing files ENABLE the generator; guard release is the go-ahead, not file absence.

---

## 7. Failure / resume / write-set oracles (exact old/new/unknown per failure)

Notation: `S` = live State bytes observed; `B` = pinned before (`sha256(S_before)`); `E` = prevalidated expected after (`sha256(S_expected)`); `P` = primary error, `Q` = secondary error (close/fsync/replace/after-read/unlink/guard-release stage).

For EVERY failure the oracle MUST retain: `P+Q`, `observed_old/new/unknown` (which of `B/E/neither-unreadable` was seen at each stage), and partial-preservation proof (never delete referenced or possibly-referenced records; never delete retained COPYs; never clean unknown guard).

| # | Boundary / failure | Required behavior + resume |
|---|---|---|
| F1 | Invalid basis / changed ID/Raw/Profile / failed review/content proof / unsupported stage/mode (BEFORE adoption/cleanup) | REFUSE before adoption/cleanup. Preserve owned inert preparation (R dir + retention + guard-claim attempt if any). No State write, no slot unlink. Resume = NEW bounded attempt with NEW `revision_id` (ordinary same-intent collision MUST NOT allocate/fork inside the old R; no same-byte takeover). |
| F2 | Incomplete candidate / retention (generate/prove/COPY/inventory/guard-claim/checkpoint incomplete) | PRESERVE; no same-byte takeover. New attempt uses NEW id UNLESS a specific immutable completed phase has an explicit validated continuation recorded in the manifest (exact phase + bytes + sha). |
| F3 | `write` fault (State-file `write_bytes` raises; versioned R Ledger/Completeness write raises; retained COPY write raises) | Retain `P` (write errno) + `S` observation (re-read State path: `B` unchanged? `E` partial? unreadable?). If `S==B` → State-Still-Before path (F8). If `S` unreadable/unknown → INDETERMINATE (F11). NEVER retry by overwriting a possibly-referenced record; NEVER delete R/retention. Explicit resume reloads record/graph/review/COPY/guard and MAY switch only if `S==B` + guard held by self. |
| F4 | `short-write` (bytes written < `json_bytes` length; observed via after-write `bytes != expected` or `sha != E/B`) | Same as F3 + record `expected_bytes vs actual_bytes`. Treat live file as UNKNOWN until a clean rewrite under held guard re-establishes `B` or `E`. No unlink of the short file if it MIGHT be referenced (compare path against ALL provenance refs first). |
| F5 | `fsync/close` fault (flush/close raises; `core.write_json` has NO fsync — pre-code MUST surface close errors, not swallow them in a logger) | Retain `P` (close error) as SECONDARY `Q` alongside write `P`. `S` = re-read + `validate_agent_state` result. `B`→F8, `E`→F9/F10, else F11. Proof logger MUST NOT suppress flush/close failures (no “rerunner certification” by log text alone). |
| F6 | `replace` fault (State-file replacement not installed: rename/link/exclusive-create step fails; versioned file appears at wrong path; COPY lands at wrong path) | Primary `P` + `S` = BOTH old path bytes AND new path bytes (old/new/unknown EACH). If old path still `B` and new path absent/partial → F8 posture (State-Still-Before). If EITHER path shows `E` → treat as F9/F10 posture (State-After family), NOT as before. Preserve both paths; delete NEITHER. |
| F7 | `after-read` fault (post-write readback fails, hash mismatch, or `validate_agent_state` fails on after bytes) | This is the ADOPTION gate. `S==E` + readback PASS → proceed to clearing (F9). `S==E` + readback FAIL → DO NOT restore `B`; preserve `S==E` bytes + record + guard; posture = State-After-Cleanup-Pending with a REPORTED after-read defect (explicit resume must re-prove readback before clearing). `S==B` → F8. `S` neither/nor or unreadable → F11. Failed after-readback with new/unknown NEVER authorizes before-bytes restoration. |
| F8 | Complete record, State still EXACTLY before (`S==B`, cleanup not started) | Ordinary adoption REFUSES same intent (“already attempted” is NOT auto-resume). EXPLICIT resume ONLY: reload record/graph/review/COPY/guard (verify `bound_state_sha256==sha256(S)` + guard held by self + R bytes + inventory), revalidate LIVE eligibility + guard, then MAY perform the ONE triplet switch. Same-attempt collision (two claimants, same `revision_id`/guard) CANNOT allocate/fork: second claimant refuses (guard held by another), never creates a sibling R. |
| F9 | State EXACTLY expected after (`S==E`), cleanup incomplete | EXPLICIT resume verifies active triplet (all three refs == SAME new record + live re-hash of four artifacts) then removes ONLY remaining EXACT old planned slots: per-slot pre-unlink reverify (present + `sha==captured_old_sha` + still unaccepted/unbound + guard held by self). Missing-already-cleared slots ALLOWED (record `already_cleared`). Foreign/replaced bytes (present but `sha != captured_old_sha`) → PRESERVE + REFUSE that slot. New file appeared at a cleared path AFTER State-new → PRESERVE (it is NOT old authority; it may be early regeneration — refuse unlink, record, require operator decision, never delete). |
| F10 | State after + cleanup complete | Full readback + readonly `ALREADY_ACTIVE` / complete result. NO new acceptance, NO new approval, NO new checkpoint. Normal regeneration proceeds under released guard. |
| F11 | State NEITHER before NOR expected after, OR unreadable, OR ownership unverifiable (`S ∉ {B,E}` / `EACCES` / guard unknown) | INDETERMINATE. Preserve records/bytes/guard. NO automatic State restoration, NO deletion, NO adoption. Explicit re-diagnosis (read-only State/history/inspection) only. Return exact blocker; if A1 guard/consumer map cannot preserve invariants, return to A1-vs-A2 comparison (decision §9) rather than implement partially guarded A1. |
| F12 | `unlink` fault (per-slot clear: `unlink` raises, or pre-unlink reverify fails) | Retain `P` (unlink errno) + per-slot `observed` (`old-captured` / `changed-foreign` / `missing-cleared` / `new-foreign`). `changed-foreign`/`new-foreign` → preserve + refuse (posture stays F9 with remaining exact slots). `missing-cleared` → record + continue (allowed). Guard stays held; NO release until postread passes. |
| F13 | `guard-release` fault (release raises, guard file changed under holder, `st_dev/st_ino` or hash mismatch at release, or release would delete a FOREIGN guard) | **Explicit row (operator review §3.4).** Guard left HELD MUST block normal writers fail-closed (entry + pre-publish checks fail). Release ONLY on exact holder identity (`st_dev/st_ino` + `sha256` + `bound` fields match claim record); otherwise REFUSE release (no auto-delete, no silent proceed, no takeover). Explicit release-retry only. Read-only diagnosis still allowed. Normal regeneration MUST NOT run while guard held, even if slots are already cleared. |

After-State-NEW resume removes ONLY remaining EXACT old slots or absent-already-cleared; NEVER re-clears a path that now holds NEW/foreign bytes. Pre-state record existence does NOT require physical State to be new: typed history/detached validation (`_validate_checkpoint_record` + `_validate_core_stage_report` on `historical_state`) verifies the record WITHOUT live-before equality. After-state source readback requires NO live-before equality — it verifies CURRENT canonical State against `B/E` + retained lineage.

No automatic rollback on ANY row. No CAS/global-CAS/crash-atomicity/creator-authenticity claim (decision §7 + R5/C6 disclaimer preserved).

---

## 8. HEAD / tree predicate (actual Git calls, fully pinned inputs, no execution here)

Pre-code must supply the phase HEAD/tree predicate + COMPLETE path set. Expected maps below are SELECTION templates (no execution in this unit).

- **Actual calls:** ONLY `git rev-parse HEAD` (via `core.repository_commit_sha:189-207`: `subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, check, capture)` + strict 40-hex check) and `git rev-parse HEAD^{tree}` / `git status --porcelain` / `git diff --raw` / `git ls-files --stage` / `git ls-tree` for tree/dirty observation (as used in carryover §§1–4). NO `submodule update/deinit`, NO `config` writes, NO checkout/reset/clean, NO standing main-refresh, NO self-reference future commit.
- **Mode / dirty roots:** root worktree dirt vs `HEAD` tree; 55 bare gitlinks mode `160000` WITHOUT `.gitmodules` (NOT configured submodules) left intact; child `.git` dirs are path-local with inert `example.invalid` remotes; `alternates`/`commondir` absent (carryover §§4/6). Default `git diff --raw` shows 1 (tracked-dirty child `survey_quality_v2.py` fault fixture); `--ignore-submodules=all` shows 0 — the ignore flag is a SCOPED check ONLY, not a clean-worktree claim. Pre-code predicate MUST state exact mode (`--ignore-submodules` value or none) per check and MUST fail closed on unknown/unreadable/dirty roots that affect the phase (tool/schema/contract/source/proof inputs). Generic dirty allowance or standing main-follow is FORBIDDEN.
- **Default config / source / proof inputs selection fully pinned:** `contract_identity:210` pins `contract_files.pipeline` + `DEFAULT_CONFIG/PROFILE_SCHEMA/STATE_SCHEMA` (`aggregate_file_hash:168` sorted rel + NUL framing) + quality 3 + research/publication profile versions+SHAs. `advance_with_checkpoint:1782-1787` requires `record.contract==current_contract` AND `record.implementation.repository_commit_sha==current_impl (repository_commit_sha(repo_root))` AND `orchestrator_version` match. Artifact-only descendant during review admissible ONLY if ancestry + EXACT changed-path set are explained by the declared attempt's input/output/review records, EVERY prior pin unchanged, current controls/contract identical; otherwise refuse + NEW bounded attempt. No future self-containing SHA; no dirty allowance for tool/schema/contract paths.
- **Code committed BEFORE authorities:** work HEAD/tree observations are pinned at generation/review/proof time; checkpoint/State authorities are recorded AFTER code commit (E = execution/observation identity, NOT “at the code commit”). Pre-code MUST record `E` (observed work HEAD/tree + tool contract SHAs at run time) separately from `C` (code-commit SHA that reviewers bind). Conflating them (demanding a future self-containing SHA) is refused.
- **Expected source / candidate fixture preflight maps (NO execute here):** for Weekly (`ROLLING_WINDOW`+X/Grok) and Thematic (`OPEN_HISTORY_AS_OF`/`CURRENT_STATE_AS_OF`+lineage) witnesses, pre-code MUST exhibit the exact expected `HEAD`, `HEAD^{tree}`, `implementation_control_roots` (`config,schemas,scripts,.github/workflows`), `contract_files` set, Profile bytes/sha, Discovery/Screening/X/raw pins, and candidate fixture State/lifecycle/allowlist predicates that the phase will check — WITHOUT running them. This file states the predicate shape only.

---

## 9. Public oracles — Weekly + Thematic, both directions, both sides of the switch

Each case below is a DESIGN oracle row. Pre-code readiness + implementation witnesses MUST instantiate EACH with: `entry` (exact State/lifecycle/guard/pins at start), `intended seam` (which transition in §6 is exercised), `observed writes` (exact seven-slot + R + retention + State + guard bytes/hashes/inodes changed vs preserved), `healthy repair` (exact explicit-resume/retry that reaches the equivalent of F8–F10 without weakening predicates). Earlier refusals are NOT proof of later seams. Synthetic reviews stay explicitly nongenuine; Production semantic NO-GO unchanged.

### 9.1 Happy-path family (must hold for BOTH Weekly and Thematic)

- **O-W1 Weekly new acceptance → normal Architecture pending.** Entry: valid `EVIDENCE_REVIEWED`, preserved Discovery/Screening/Profile + old accepts immutable, newly captured input proof with correct article-event interpretation (hosted-article bytes + `URL/fetched_at/SHA/bytes` + `datePublished` as hosted-article event, NOT model/code/dataset availability or reproducibility; AstaBrief-predates + AutoSynthData-no-standalone caveats as fields). Seam: §§6.2–6.11 full order. Observed: new Evidence/Views/Ledger/Completeness under R, same-record triplet `S_before→S_expected`, seven old slots retained then checked-cleared, fresh Matrix/Selection/Architecture regenerated, Guard released. Repair: N/A (baseline).
- **O-T1 Thematic new acceptance → normal Architecture pending.** Same as O-W1 with `OPEN_HISTORY_AS_OF`/`CURRENT_STATE_AS_OF` temporal policy (`config:248-249`), lineage/parallel-competing/unresolved-lineage boundaries, genuinely supported source types ONLY (DM016: refuse unsupported; no alias relabelling; 10 absent canonical Thematic types stay OPEN; report non-closure).
- **O-W2 / O-T2 Full post-acceptance Draft/reader closure.** Entry: adopted checkpoint + regenerated Architecture + later `ARCHITECTURE_ESTABLISHED`+approved → Draft/Reader. Seam: §5 readback through forward lifecycle (original context from retained lineage, NOT live-before equality). Observed: Draft/Synthesis/Reader/publication-proposal/retention consumers resolve new four refs; NO old canonical fallback; Reader closure predicates hold. Repair: any stale-canonical read → refuse + rewire (B2), not silent fallback.
- **O-R1 Repeated revision.** Entry: post-O-W1/O-T1 `EVIDENCE_REVIEWED` (new accepted authority now active). Seam: second same-State revision with NEW `revision_id` + NEW guard claim (F1 collision rule: no fork inside old R). Observed: second R dir, second retention, second checkpoint lineage (`supersedes` chain), second triplet switch. Repair: second attempt MUST NOT reuse first R/guard.

### 9.2 Guard-interruption family (both sides of the State switch)

- **O-G1 Guard interruption BEFORE switch** (crash/kill between §§6.4–6.6). Entry: guard held by self, checkpoint complete or not, `S==B`. Seam: F8 explicit resume (reload record/graph/review/COPY/guard, revalidate LIVE + guard, then switch). Observed: NO slot cleared before switch; NO State change until resume. Repair: explicit resume MAY switch; ordinary same-intent adoption refuses.
- **O-G2 Guard interruption AFTER switch, BEFORE/AFTER partial clear** (between §§6.7–6.9). Entry: `S==E`, some old slots cleared, some remaining. Seam: F9 explicit resume (verify triplet, clear ONLY remaining EXACT old slots; `already_cleared` allowed; foreign/new preserved). Observed: NO re-clear of new/foreign bytes; NO State restore. Repair: explicit resume completes clearing → postread → release → regen.
- **O-G3 Guard-release failure.** Entry: postread PASS but `unlink`/release raises or identity mismatch. Seam: F13 (stay blocked fail-closed, explicit release-retry only). Observed: normal writers STILL refuse (guard held); NO silent proceed to regen. Repair: holder-identity release retry; NEVER auto-delete/foreign-takeover.

### 9.3 Negative family (must REFUSE; refusal ≠ seam proof)

- **N1 Accepted old / stale-canonical reuse.** Entry: caller attempts old canonical Ledger/Completeness/Matrix/Selection AFTER adoption. Expected: refuse (B2 resolver) — record refusal, NO bytes changed.
- **N2 No-Human / fake-Gate flags.** Entry: `human_gates.*==pending`, `human_gate_provenance.*==null`, NO review-index rows, NO presented immutable request; OR fabricated `REQUEST_CHANGES`/pending-Gate invalidation at bare `EVIDENCE_REVIEWED`. Expected: refuse; pending-Gate path (`_current_pending_gate:440-485` + `invalidate_pending_gate:1179-1348` requiring passed `architecture` checkpoint `:1208-1209`) unreachable at bare `EVIDENCE_REVIEWED`. No fake Sol/Human Gate, no generated genuine PASS.
- **N3 Malformed / split refs.** Entry: triplet refs NOT same record; View→Evidence SHA mismatch (`resolve_active_evidence_views:920-932`); exact-one-artifact violation (`_resolve_checkpoint_artifact`); `CORE_STAGE_CONTRACT` lifecycle forgery (`_validate_core_stage_report:403-408`). Expected: refuse.
- **N4 Wrong stage / prior Human review.** Entry: lifecycle ≠ `EVIDENCE_REVIEWED`; OR State returned after genuine `REQUEST_CHANGES` / pending-reviewed Architecture Gate / approved Architecture / later stage. Expected: refuse this window (legitimate Gate revision stays under its own conditions; do NOT erase review history to gain eligibility).
- **N5 Missing obligations.** Entry: Completeness drops a Profile-initial OR Discovery-named obligation (`survey_completeness_v2:208-223`). Expected: refuse; DM017 builder (`_build_completeness:471-507`) MUST NOT be called alone.
- **N6 Unknown source types.** Entry: witness uses unsupported Weekly/Thematic source type (DM016 inconsistent maps `run_evidence:38-45` vs `survey_evidence:44-109`; 10 Thematic types absent). Expected: refuse; no alias relabelling.
- **N7 INSPECT misuse.** Entry: `INSPECT` ID without valid non-DROP task association + evidence status + View/Ledger pass (`build_evidence_tasks:19 PROMOTED`; `survey_evidence:1602-1635`; `validate_edition_view:1437-1491`). Expected: refuse promotion to KEEP/MATERIAL; HOLD→MATERIAL/SELECTED auto-promotion refused.
- **N8 Source/clock data.** Entry: Summary quotation as evidence; missing original HTML bytes/provenance; `datePublished` misread as first-availability/reproducibility; missing `INSPECT`/event-meaning fields. Expected: refuse; require preserved bytes + retrieval provenance.
- **N9 Stale HEAD / controls / Raw.** Entry: work HEAD/tree ≠ expected; `contract_identity` / `implementation_sha` drift (`advance:1782-1787`); Raw bytes drift vs acceptance (`package_sha256` basis). Expected: refuse + NEW bounded attempt; no standing main-follow/dirty allowance.
- **N10 Metadata-only “promotion”.** Entry: no new article bytes, only directory-SHA propagation claimed as new acceptance. Expected: refuse; mechanical SHA propagation explicitly mapped per unaffected row, never directory-prefix excluded; full semantic revalidation required.
- **N11 Ownership / close / replace faults.** Entry: inject each F3–F6/F12 fault class on State, R, retention, seven slots. Expected: F3–F6/F12 rows (preserve + INDETERMINATE-or-explicit-resume, never delete possibly-referenced records).
- **N12 Ordinary collision.** Entry: second claimant same `revision_id`/guard while first guard held. Expected: refuse (no fork allocation).

Each N-row MUST be witnessed as a REFUSAL with `entry + intended seam (none taken) + observed writes (none except owned inert prep if allowed)`. An N-refusal MUST NOT be cited as proof of the corresponding O-seam.

### 9.4 Cost

Qualitative added work ONLY (typed checkpoint/report/lineage, retained storage, guard/resume coordination, affected consumer integration, independent re-review). Unknown is NOT zero. NO numeric saving/cost/finish-date claim. No guarantee.

---

## 10. Precise complete OPEN list → root decision requests (no code approval)

Pre-code readiness return (General, after Human continuation) MUST close ALL of the following with source-cited predicates; Astra + author-independent readiness reviewer MUST confirm BEFORE code. Implementation BLOCKED until then (decision §10–§11/root §5).

1. **Checkpoint/report/schema/digest map:** exact new branch field names, `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` schema additions (`stage-checkpoint-v2.schema.json` `evidenceArtifacts:200-208` extension for `from_state==EVIDENCE_REVIEWED` same-State operation), `CORE_STAGE_CONTRACT`-distinct supersession proof/report shape, self-digest expression, same-record triplet validation predicate, historical (`historical_state`) vs CURRENT proof boundaries (detached proof NEVER calls current State acceptance; LIVE eligibility + guard high-side).
2. **B2 caller closure:** EVERY direct canonical Ledger/Completeness/Matrix/Selection reader + EVERY post-acceptance consumer Selection→Architecture→Draft/Reader/publication proposal/retention/operator/handoff/Gate prep/checkpoint-history inspection + EVERY later R1/editorial/renewal walker — each with file:line + `resolver-or-explicit-refuse` disposition + post-acceptance tests. No unchanged-consumer claim, no canonical-filename fallback, no fake old report.
3. **B4 path/call map:** exact versioned R output args/filenames/schema fields + current content-validator entrypoints (§2.1); proof canonical Ledger/Completeness stay byte-identical + inactive via provenance switch; present/absent inventory + source refs; no fabricated `CANDIDATES_NORMALIZED` runner.
4. **Seven-slot writer/ownership map:** exact producer per slot (§2.2 seven-path preflight incl. audit) + caller-input vs generated-archive provenance + partial-run non-fabrication rule + per-slot fault oracles (§7 F12).
5. **Guard machine:** exact root/path/schema/owner binding (§4.1) + claim/revalidate/release protocol + FD/inode/hash identity + EVERY check call site (§4.2 table completed) + unknown/unreadable/mismatched fail-closed + degraded postures (F8/F9/F11/F13) + explicit guard-release-failure row. Proof that NO unguarded normal writer can regenerate stale outputs in the window.
6. **HEAD/tree + work-ref map:** phase predicate + COMPLETE path set (§8); expected source/candidate fixture preflight maps for Weekly + Thematic (no execution); code-before-authorities (E) separation; artifact-only descendant admissibility rule.
7. **Owned IO/resume oracles:** retain/copy/inventory verification (§3) + pre-unlink reverify + State snapshot/restore discipline (cleared-slots-staying-cleared degraded posture) + postread/inventory + explicit-resume-per-§7-row; no caller flags/verified-dict bypass, no skipped predicates, no path budgets, no unselected migrations.
8. **Profile-specific predicates:** per-witness (Weekly + Thematic) supported source-type allowlists (DM016), exact Discovery-named obligation rows (DM017 union rule), archived-HTML + retrieval-provenance shape, timestamp-parser + event-meaning fields, INSPECT binding rule, full unaffected-content comparison rule.
9. **Public oracle instantiation:** §§9.1–9.3 instantiated per witness with `entry/seam/observed/repair` + negative matrix + repeat-revision + both-sides guard interruption. Each case meaningful (not earlier-refusal reuse).
10. **A1-vs-A2 fallback readiness:** if ANY required predicate/writer cannot be included without weakening, return the EXACT blocker + revise A1 vs A2 (decision §§9/11.4) — NEVER implement a partially guarded A1.
11. **Audit-slot obligation:** successor runner MUST NOT reuse the six-path preflight verbatim; audit writer/ownership/fault oracles for slot 7 explicit.

Root is asked to confirm this Task C oracle set as the binding pre-code C surface (alongside the pending interface/schema/digest/import/closure map), OR to return exact corrections before any code. No implementation authorization is requested or granted by this file.

---

## Appendix — pins, scope, stop

- Decision hash `a345bb95…f223` / 31351 B; root resolution §§1–5 (closeout §5 binds); authority B1–B4 + operation §3 (7 obligations) dispositions per §§11.1–11.4.
- Final93 proof-copy available in place; NO restore/network/fixture/test/build/import performed or claimed here.
- Whole NOT_READY / step4 B3 OPEN / audit unstarted / DM021+022 OPEN; DM016 inconsistent maps + DM017 incomplete builder remain separate requirements; Profile/quality/adoption/savings OPEN.
- This unit wrote ONLY `notes/rephase-1-dm022-prearchitecture-precode/guard-resume-oracles.md` (+ optional `.json` same base). No ordinary Commit/Push. **Stop; no code approval; no CommitPoint claim.**

(End of file)
