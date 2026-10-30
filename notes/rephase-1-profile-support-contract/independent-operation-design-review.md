# Independent OPERATION/SCOPE design review — selected Profile/support contract (selection ONLY)

Status: **DESIGN REVIEW ONLY, operation/scope. No tests/runtime/import/build/fixtures/network/Git Human readback/code edits.**
Independent of authors A/B/C, integrated proposal, and Astra/ROOT. Prior
`independent-obligation-contract-review.md` (DESIGN_NOT_READY §§1–4) and
`independent-authority-design-review.md` (DESIGN_BOUNDED_PASS) preserved unchanged —
this file adds the operation/scope verdict only.

Task: fresh operation/scope review of selected ROOT contract
`outputs/rephase-1-profile-support-contract-decision.md` FULL +
`notes/rephase-1-profile-support-contract/astra-review-resolution.md` (mandatory),
per DM022 assessment §5 FIRST-repair order.

Source boundary: final133 READ-ONLY
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(actual409/tree8ce +133 paths54M79A/768 intended files;
delivery patch `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b9260`/4931836B;
manifest `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa`/185422B;
independent check/apply 0 per DM022 packaging review). Baseline `774dd39a` unchanged.
Contract `a345bb95` §11 + precode ROOT `0425c530` §5 unchanged.
Human Commit-point readback omitted as authority; no Commit/Push.
Acquired compat `.py` is DATA text-read only, never executed/imported.
Fixed intake commit `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`, 4 GETs only.

Reviewed bindings (data-only file bytes, no Git object/commit as authority):

- Decision `outputs/rephase-1-profile-support-contract-decision.md`
  SHA256 `e5aed7a4d3da3f50bf0fd14448690053dbd58fb5e936d8cb51948e6f894bedd8` / 18663B.
- ROOT resolution `notes/rephase-1-profile-support-contract/astra-review-resolution.md`
  SHA256 `34ee4891ec49a1796c155f74a5410c227e3f67d9a5b3f3931ec127d230955858` / 4745B.
- If either file is revised, this review needs final confirmation against the new bytes;
  the verdict below binds only the above bytes.

Verdict: **DESIGN_BOUNDED_PASS — contract SELECTION only.**

Selection is source-grounded, preserves normal operation discipline, and leaves no hidden
extra Gate, obligation retype, or old-Profile rewrite. Code remains **BLOCKED** until the
mandatory concrete pre-code map (decision §6) is returned, independently reviewed, and
Astra confirms. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN unchanged.
Essential mapping/failure authorities below cannot be waived as "pre-code detail";
non-contradicting interface details may stay open.

## 1. Operator work / authorities / sequence — viable, no hidden Gate/retype (PASS)

Selected work is additive and caller-pinned, not a new authority:

- DM016: ten literal appends to canonical `survey_evidence_v2.SOURCE_CLASS_MAP:44-109`
  via leaf `_source_class:177-184`, consumed at `task_authority_sources:413-446`
  (`:422-423` `_source_class(source.get("source_type"))`) and supplement exactness
  `:304-305`. All old mappings unchanged (decision §3). No conditional classifier,
  default SECONDARY, PR-never-primary, URL-sniff, alias/projection ledger, new module,
  legacy-enum edit, or supplement-SOCIAL expansion — all explicitly rejected in
  decision §§3/5 and ROOT §§1–2. Source confirms runner 6-map
  (`run_evidence_v2_interactive.py:49-56,110-114`) is dead (3 grep hits 49/110/111,
  zero in-file calls; live card path `:321` + task inventory `:666` call canonical
  `evidence.task_authority_sources`). Legacy 4-enums
  (`screening-record.schema.json:12`, `evidence-task.schema.json:25`) are v1 path
  (`prepare_screening_run` family, zero v2 imports); correctly not edited.
- DM017: one existing `completeness.obligations` array, 3-field for `P` /
  5-field for `U−P` / refuse `∉U`, exact cover, internal derive (decision §4.2).
  No second definition/decision catalog (no sync work), no Profile versioning/migration,
  no caller-verified dict, no `production.verify_state_basis` substitution, no canonical
  overwrite/rebind-by-hash. `_build_completeness` tuple
  `(repo_root,profile,profile_path,discovery_records,ledger_path,ledger,input_value)`
  retained (`run_evidence_v2_interactive.py:767-775`); only 3-vs-5 branch + internal
  derive change. Keyword-only
  `validate_interactive_input(...,task_source_ids=None,*,discovery_records,root_discovery_records)`
  + keyword-only `_validate_completeness_input` (decision §4.2, proposal §2) fixes the
  prior required-after-optional SyntaxError. Concrete caller/test/adapter pin is
  pre-code §6.1 business — permitted open, not a waiver (decision §6 "not a path
  budget", "any additional necessity returns to Astra").
- Callers verified in final133 (read-only, no run): `validate_interactive_input` prod 1
  (`:674-676`), test 1 (`tests/test_run_evidence_v2_interactive.py:99-106` positional
  4-arg today, must be updated to keyword), frozen edition driver
  (`DATA.run_frozen_evidence_chain.py:166-167`, edition-local NOT Core);
  `_build_completeness` prod 1 (`:767-775`), adapter wrapper 1
  (`run_evidence_v2_agent_first.py:88-91` `*args/**kwargs` forward), frozen driver 1
  (`:222-223`); `_validate_completeness_input` internal 1 (`:309`). No hidden Gate:
  ENTRY `:610-623` + prepublish `_dm022_require_ready` at `:694,727,748,764,805`
  preserved; no new Gate added.

## 2. Source-schema vs claim-strength separation (PASS)

Decision §3 ¶2 + intake §§3–4 keep `source_class` (resource provenance for the
resource's own statement/proposal) distinct from `evidence_class`
(`PRIMARY_FACT/VENDOR_CLAIM/...`), `verification.targets`, materiality, completeness.
Source confirms: `EVIDENCE_CLASSES:37-40` distinct from `SOURCE_CLASS_MAP:44-109`;
`task_authority_sources:413-446` emits `source_class` only; card builder
(`run_evidence_v2_interactive.py:321-361`) binds `evidence_class` per claim separately.
No model-vendor endorsement, merge status, architecture fact, benchmark performance,
or available-weights proof is conferred by the ten mappings. Per-record publisher bytes
were NOT fetched in 4-doc scope (intake-summary §§3/5: vLLM-recipe / PR-27742
associations UNVERIFIED, PACKAGING counterpart unidentified) and are explicitly NOT
claimed — no existing edition source/assertion approved, no CORE_FIXED. Genuine-type
witnesses with full source API (collector + `raw_refs` + published/accessed instants +
publisher identity + claim binding per literal) are deferred to mandatory oracles
(§6.4), not assumed. The three single-task `PRIMARY_*` rows stay under the §8 oracle
gate: no PRIMARY authority may be asserted until that oracle closes; selection does
not waive it.

## 3. 3/5 exact cover + mechanical derive + residual union (PASS)

- Exactness: `oid∈P` → exactly `{obligation_id,status,rationale}` (dimension/description
  from Profile only); `oid∈U−P` → exactly
  `{obligation_id,status,rationale,dimension,description}` (dimension already
  Profile-declared per `_validate_obligation_shape:62-63`, description non-empty);
  `oid∉U` → refuse. Exact `U` coverage, unique IDs, explicit valid status/rationale,
  no autostatus. Five fields on a Profile-initial ID refuse (preserves Profile
  authorship and existing `survey_completeness_v2.py:211-212` dimension-change error).
  Final 7-field rows, result/Profile/DM022-request/consumer schemas unchanged;
  DM022 `fullObligation` (`dm022-revision-request-v2.schema.json:232-244`,
  `minLength:1`) separate; ordinary path has no OLD (refuse-overwrite `:763-766`).
  Old 3-only inputs valid exactly when `U==P`. This closes prior §2/§4 at selection.
- Derive: `discovery_ids` from all effective declarations
  (`sorted(declaring.get(oid,[]))`, profile-only `[]` legitimate per
  `_unique_string_list` + LOW `:1900-1909` pattern); `evidence_task_ids` from exact
  ledger map (LOW `:1898-1908` pattern), never retyped by operator. Existing full
  content/basis/traceability/closure validators run after derivation; Thematic counters
  recomputed from canonical provenance; residual limitations preserved by stable union,
  not another operator copy task (decision §4.2, ROOT §3, adapter `:55-76` + validator
  `survey_evidence_v2.py:2239-2240` LIMITED-must-preserve-residual).
- Judgment stays explicit: operator supplies new semantics (dimension already declared,
  description non-empty) + status/rationale; Discovery/ledger supply DIDs/task IDs;
  validators enforce. No invented `dimension/description`, silent drop, alias, or
  allowlist relax.

## 4. Unknown source — early Screening refusal, not coerce/DROP/alias (PASS)

Decision §3 requires classification before new v2 Screening preparation/acceptance
writes and before Evidence package/accepted-output writes; Discovery archival vocabulary
stays open; unsupported captured material does not become eligible by type-eligibility
shortcut. Source makes this feasible: Discovery `source_type` open
(`survey-discovery-record.schema.json:51` `{type:string,minLength:1}`,
`survey_screening_v2.py:171-173` no enum); canonical `_source_class:177-184` raises
`unsupported source_type` fail-closed; `prepare_evidence_package:601-621` passes through
open `source_records` but `task_authority_sources:422-423` fails before any owned write
on unknown. Exact admission callsites + lazy import closure must be confirmed pre-code
(no top-level Screening↔Evidence cycle: `survey_evidence_v2.py:21` top-level imports
screening; `survey_screening_v2.py:397` uses function-local discovery import — any
Screening→Evidence preflight MUST be function-local). Alias relabel to satisfy the
validator is prohibited (exact `source_type→source_class` equality at
`survey_evidence_v2.py:304-305,1053-1055` would then verify the projection, not the
original — ledger auditability lost). No coerced DROP, no URL-sniff
(`run_special_interactive_evidence.py:41-47` rejected), no projection ledger.

## 5. Per-parent declaration loss — current operation vs own history (PASS)

Decision §4.1 + ROOT §3 scope the new loss rule to new Screening preparation/acceptance,
ordinary Evidence input preflight, and DM022 HIGH new-operation eligibility before
writes. They forbid blindly tightening shared historical `validate_discovery_expansion`
or detached validators: old records stay interpretable under their accepted contract;
historic validity ≠ new-operation eligibility. Source-grounded because that shared
function is called by current (`resolve_effective_discovery_basis:428`), renewal content
(`_resolve_effective:855`), and acceptance validation (`validate_acceptance:915`) —
global tightening would rewrite history. Pre-code must prove the separation without
caller-verified flags or State recursion.

Source facts restated correctly in selection: expansion enforces per-child
`child_obligations ⊆ union(declared parents)` (`survey_screening_v2.py:303-311`) +
DID closure (`:313-318`); `EXPANSION_REQUIRING_PARENT:37-43` excludes
`GAP_FILL/BASE/CARRY_OVER` (`:272-275`), so derived cannot invent GAP_FILL IDs —
genuinely new named IDs enter as root, not derived additions. R2 "expansion-added IDs"
wording is recorded as erratum. Selected `U = P ∪ named(R) ∪ named(E)` from the SAME
already-resolved `resolve_effective_discovery_basis:353-439` dict
(`root_records` + `records`, `run():641-648` already holds both; no second fetch, no
compact acceptance as `U` source per `discovery-acceptance-v2.schema.json:85-98`
normalized `parent_edges` vs canonical JSONL `provenance`, no supplement-DID universe
per `prepare_evidence_package:563-591`). Per-parent rule cites the actual source field:
string-array `provenance.parent_refs` (`survey_screening_v2.py:144-159`,
`survey_discovery_v2.py:96-115`). Every `(parent,OID)` needs an effective carrier
(identical DIRECT record or valid derived child with that parent in `parent_refs`);
global-set equality insufficient when two parents share one OID. `lost` (global +
per-parent uncovered) → `DECLARATION_LOSS` refuse before writes; no auto-add, no
accepted-child rewrite (acceptance immutability `validate_acceptance:897-916`,
`accept_results:919-979` digest). On pass `U` collapses to `initial ∪ named(effective)`;
final-row traceability uses effective DIDs + validated parent graph, never invalid root
IDs in an effective-only result.

## 6. Retry / guard / no-overwrite + no code before operator input validation (PASS)

Normal discipline preserved: `_dm022_require_ready` at ENTRY `:623` and prepublish
`:694,727,748,764,805`; ordinary Ledger/Completeness refuse-overwrite
(`run():749-750,765-766` exists-or-symlink check — selection does NOT claim invented
`O_NOFOLLOW/O_EXCL` for this path; exclusive discipline lives in other modules);
Evidence package non-empty refusal (`survey_evidence_v2.py:595-596`); Screening
`prepare_package` / `accept_results` digest path. Decision §4.3 requires completeness
shape/`U`/declaration-preservation validation **before** ordinary owned/package writes,
using root/effective already available at `run():641-648` before
`prepare_evidence_package:653-661`, while record/task-dependent validation still uses
the generated actual task universe. No "invalid input is pre-write because the final
schema eventually rejects it" inference. Failure/resume windows, late guards, and
refusal-before-write ordering are pre-code §6.5 proof items, not assumed.

## 7. Manual alternatives — actually legal, not 'just rewrite' (PASS)

`DIRECT_PRIMARY`/`PRIMARY_ONLY` preserved with honest scope: Gate returns it only on
exact primary path+bytes (`survey_reader_surface_gate_v2.py:1352-1356` early return),
vs generated branches requiring canonical `reader-surface-input-v2.json` + receipt +
exact trio closure (`:1357-1428`) and editorial trio binding (`:1335-1349`).
Supporting BIBLIOGRAPHY/STYLE path+sha binding is a byte hash, not complete-reader
semantic projection or reuse proof. Post-render reviews (core `PDF_PREFLIGHT`,
publication-profile `AGENT_VISUAL` per `config/survey-production-v2.json:170-206`,
plus semantic/editorial/visual/Human Preview) are distinct from pre-TeX Reader-Surface
judgment over every emitted value/order/citation.

Legality windows (decision §2, route disposition §8, source-confirmed):

- Pre-acceptance authoring (up to EVIDENCE_REVIEWED): new manuscript/support bytes with
  no accepted authority to violate — legitimate, no Gate faking.
- Post-VALIDATED with changed reader: direct P1 on Retro/manual is `UNSUPPORTED_ROUTE`
  (`survey_editorial_correction_proposal_v2.py:566-573`); renewal admits only
  WEEKLY+THEMATIC (`survey_versioned_renewal_source_v2.py:637-639`); PREARCH refuses
  wrong family. Changed-reader republication without a proper gate is arbitrary
  correction, not legal. Legitimate only via genuine Human `REQUEST_CHANGES`
  reopening to an allowed regeneration boundary (`survey_human_gate_v2.py:5-15,180,344`,
  never agent-synthesized PASS), or a new edition / other proper gate (new
  Profile/State, new DRAFT_COMPLETE, or a future selected correction contract). Never
  fake Gate bytes, never reuse old-State hash as current authority, never direct
  changed-reader P1 on Retro/manual. "Just republication" as a blanket path is not
  selected.

## 8. No unnecessary schema/legacy/collector expansion; no unverifiable publisher claim (PASS)

Footprint (estimate, pre-code must confirm): `survey_evidence_v2.py` (map +
`_source_class` + `task_authority_sources`), `survey_screening_v2.py` (preflight +
loss gate + effective basis), `run_evidence_v2_interactive.py` (validators +
`_build_completeness` + residual fold), `run_evidence_v2_agent_first.py` (thin),
tests/docs only. No new schema/module/family ID presumed; no 3-schema budget; no
legacy-enum edit; no supplement-SOCIAL add (optional post-Screening exact-manifest
path, possibly deliberate policy — correctly left alone); no collector rewrite; no
new cadence engine or bridge expansion (custom Retro `--spec` CLI at
`survey_period_v2.py:193-216` is sufficient transport if Human-authorized; Foundations
is planning-only overlay on THEMATIC per `survey_x_intake_v2.py:86,152-154`, not a new
Profile/series machine). The ten mappings append only; old mappings unchanged; new
admission applies to new sources only; accepted historic Evidence/Views/Ledger bytes
never rewritten. The three `PRIMARY_*` singletons do NOT assert per-record publisher
authority until the §8 oracle (collector + `raw_refs` + instants + publisher identity +
claim binding per literal) closes; until then they stay fail-closed `SECONDARY`-or-refuse
rather than admitted `PRIMARY_*`. This condition is part of selection, not a later
embellishment.

## 9. Cost unknown, no numeric promise (PASS)

Decision §5 states implementation, historical-policy separation, cross-profile tests,
and independent review have real costs; amounts and net savings are unknown and must
be measured later; necessary review is not duplication. No date, percentage, or
numerical saving asserted. Order (shared upstream → necessary non-four-family/Retro
reader/correction → quality → candidate/diagnostics/audit → adoption → measured
improvement) matches assessment §5. No silent Special narrowing, alias relabel,
obligation drop, or batch-all-maintenance repair.

## 10. Route citations — necessary scope, no silent narrowing (PASS)

Decision §2 + ROOT §4 preserve every necessary route with completion conditions;
route disposition §§1–11 is source-cited and provisional-policy-safe:

- Weekly generated (`WEEKLY_GENERATED_V2`) + Thematic four-family
  (`LONGFORM_GENERATED_V1`, `FORMAT="THEMATIC_FOUR_FAMILY_LINEAGE_V1"` at
  `survey_longform_derivation_v2.py:109`, fixed display
  `FIXED_TITLE/EDITION/FINAL_HEADING/TOC_TITLE` + 4-model cross-table at `:118-136`,
  not generic IR) — required existing cases, not all-Thematic acceptance.
- Other-Thematic subjects: generic upstream Profile exists but four-family serializer
  does not express arbitrary topics — **required remaining complete-reader/correction
  contract**, not silently excluded or claimed solved by source-class fixes.
- Monthly/half-year/annual/custom bounded Retrospective: generic period/Profile +
  upstream semantics exist (`survey_period_v2.py:5-134`, `BOUNDED_PERIOD`),
  no selected generated Retrospective reader or versioned editorial/renewal/PREARCH
  route — **required remaining applicability/reader/correction gate**; keep bounded
  period semantics, never relabel as Thematic. Editorial P1 refuses Retro/manual,
  renewal admits WEEKLY+THEMATIC only, mechanical refresh requires WEEKLY,
  PREARCH refuses wrong family — all preserved, not bypassed.
- Manual/direct-primary: capability + PRIMARY_ONLY limits + post-render/Human reviews
  preserved; main-source identity + declared bib/style hashes are not complete-reader
  projection or semantic-reuse proof; post-VALIDATED arbitrary replacement is not made
  legal by calling it manual.
- Custom-period transport: local `--spec` CLI exists; bridge only configured slug —
  no extra engine selected. Foundations: planning/series convention on Thematic, no
  new Profile/series machine, but still requires meeting Thematic semantics/quality.

No independent-source all-Profile acceptance claimed; DM016/017 are shared
prerequisites. No publication semantic PASS, no all-maintenance batch.

## 11. Source contradictions checked (no prose-only reliance)

Independently read in final133 (no execution): `survey_evidence_v2.py:44-109,177-184,
304-305,413-446,518-681,965-1055,1387-,1663-1910,2090-,2135-2383`;
`run_evidence_v2_interactive.py:49-56,110-114,228-310,321,482-570,600-811`;
`run_evidence_v2_agent_first.py:33-99`; `survey_screening_v2.py:30-60,144-159,243-322,
353-439,809-939`; `survey_completeness_v2.py:25-33,50-238,241-290`;
`survey_reader_surface_gate_v2.py:1330-1428`;
`survey_editorial_correction_proposal_v2.py:548-573`;
`survey_versioned_renewal_source_v2.py:637-639`;
`survey_longform_derivation_v2.py:109,118-136`;
`survey_period_v2.py:5-134,193-216`; `survey_x_intake_v2.py:86,152-154`;
`survey_human_gate_v2.py:5-15,180,344,457-504`;
schemas `evidence-v2-card:85`, `evidence-authority-supplement-v2:60-61`,
`profile-completeness-result:27`, `dm022-revision-request-v2:232-244`;
`config/survey-production-v2.json:129-133,138-169,170-206`.
`grep` confirms zero hits for all 10 Thematic literals in `scripts/` (gap is
source-factual, not report-only). No contradiction to selection found; §8 oracle
remains the only PRIMARY-admission blocker.

## 12. Next-unit readiness limits (binding)

- This PASS covers **contract selection only**. No implementation, no representative
  quality, no fixed candidate/diagnostics/audit, no adoption/operation, no measured
  saving.
- Code blocked until Human continuation returns the concrete pre-code readiness map
  per decision §6.1–6.5 (actual new-operation preparation/acceptance sites for
  classification + per-parent preservation; full root/effective canonical loading;
  exact early-input validation ordering; all direct/agent-first/CLI/handler callers +
  DM022 HIGH eligibility; test/adapter signatures; ten mappings with unchanged olds;
  source/claim distinction; strict 3/5 alternatives; final-7 equality; file/import/
  digest/closure/epoch map; behavioral witnesses incl. all-10-type acceptance,
  unknown-refuse, multi-source/multi-DID, two-parents-share-OID loss exposure,
  DROP/HOLD/CONTEXT retention, parity, history-vs-new rejection, downstream
  Selection/Architecture consumption without PASS-count transfer), then independent
  readiness review + Astra confirmation.
- Essential authorities that cannot be waived as detail: ten-literal exact mapping
  with `RUNTIME_*`/PACKAGING/`RUNTIME_PR` PRIMARY oracle; `U` + per-parent
  `DECLARATION_LOSS` gate on actual `parent_refs` before owned writes with history
  separation; keyword-only signatures + caller/adapter pin; pre-write validation order
  with guard/no-overwrite preservation; manual-legality windows (genuine Human
  REQUEST_CHANGES/new edition only); no schema/collector/Gate expansion beyond selection.
- After this review, update current entry and **stop at Human Commit Point; do not
  auto-start the next unit**. Ordinary Commit/Push Human-owned.

No runtime, fixtures, Human-commit readback, or source edits used. Source reads only.

## 13. FINAL-BINDING selected-contract confirmation (decision §7 + ROOT §5)

FINAL-BINDING confirmation on the corrected contract. This section only is new;
§§1–12 preserved unchanged as operation/scope evidence, except where explicitly
superseded below. Prior adverse/design reviews preserved (initial DM017
DESIGN_NOT_READY, author errors, workaround-vs-canonical limits).

New bindings (data-only file bytes, no Git object/commit as authority):

- Decision FULL INCLUDING §7 `outputs/rephase-1-profile-support-contract-decision.md`
  SHA256 `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` / 20472B / 123 lines.
- ROOT FULL INCLUDING §5
  `notes/rephase-1-profile-support-contract/astra-review-resolution.md`
  SHA256 `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a` / 7225B / 39 lines.
- Prior bindings `e5aed7a4d3da3f50bf0fd14448690053dbd58fb5e936d8cb51948e6f894bedd8`/18663B
  and `34ee4891ec49a1796c155f74a5410c227e3f67d9a5b3f3931ec127d230955858`/4745B remain
  history; verdict below binds only the new bytes. If either file is revised again,
  fresh confirmation is required.
- Source final133 unchanged: `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
  (actual409/tree8ce +133/768, patch `25b48878`/4931836B, manifest `31fa4a72`/185422B).
  Baseline `774dd39a` unchanged. Intake `c8d0ecc1`, 4 GETs DATA-only, no execution.

Acknowledged correction: the `SECONDARY-or-refuse` phrase in §§2/8/11 above and the
integrated proposal §6 fallback question were overbroad and are **superseded** per
decision §7 + ROOT §5. They are not retained as a conditional/downgraded map.
What was coherent in §§1–12 (exact callers, U + per-parent loss, 3/5 exactness,
guard/no-overwrite order, manual windows, route scope, cost-unknown, citation checks)
stands; only the fallback-class wording is corrected.

Confirmed selection (coherent, no blocker):

- Fixed 10-class table in decision §3 is normative NEW contract for correctly
  represented new inputs. `RUNTIME_RECIPE`→`PRIMARY_OFFICIAL`,
  `PACKAGING_DOCS`→`PRIMARY_OFFICIAL`, `RUNTIME_PR`→`PRIMARY_REPOSITORY` are resource
  categories (maintainer docs first-party to that runtime/package subject; repo-native
  PR primary evidence of its own proposal), not claim proof. No runtime conditional
  map, no default SECONDARY, no PR-never-primary rule is authorized.
- Genuine-type oracles + claim limits are required pre-code: accurately represented
  maintainer documentation and repository-native proposals with explicit limitations
  and independent research/claim assessment (§6.4 witnesses across all three research
  Profiles, bounded to route matrix). No genuine Production/publisher proof is inferred
  from synthetic fixtures or from the 4 docs; synthetic fixtures must be labelled as
  such. No new capture/Gate permission, no extra network access, no unapproved new
  Production capture is demanded or authorized.
- Unfit claim/provenance is handled by existing refusal/limited status
  (unknown-type refuse, class-drift refuse, `silently dropped`/traceback refuse,
  `DECLARATION_LOSS` refuse, `UNSUPPORTED_ROUTE`/wrong-family refuse, NEEDS_RESEARCH/
  LIMITATION judgment), not by silent class relabel of accepted inputs. Accepted inputs
  are never relabelled to make them pass; `PRIMARY_REPOSITORY` for a PR does not prove
  merge status or target-model claims. This does not certify the actual uncaptured 67
  TS-001 tasks or promote the edition workaround to CORE_FIXED.

Not waived: new-operation vs own-history separation (new gates only, shared historical
validators untouched, old bytes/mappings immutable); current-operation preflight
(root/effective canonical loading, early classification + per-parent preservation
before owned/package writes, unknown-source refusal placement); private input
semantics (keyword-only discovery/root records, exact 3/5 cover, internal mechanical
DID/task derive, residual-union in normal builder, direct/agent-first parity with
caller proof, guard/no-overwrite/failure windows, file/import/digest/closure/epoch
handling). Pre-code gate remains OPEN; any interface contradiction returns to Astra
before code.

Verdict: **DESIGN_BOUNDED_PASS (selection only)** on the corrected contract.
Coherent as selection; no exact blocker. Code/tests/runtime remain blocked until the
mandatory pre-code map (§6.1–6.5, now under §7) is returned, independently reviewed,
and Astra confirms. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN;
Profile/quality/adoption/savings and non-four-family/Retrospective requirements open.
Stop at Human Commit Point.
