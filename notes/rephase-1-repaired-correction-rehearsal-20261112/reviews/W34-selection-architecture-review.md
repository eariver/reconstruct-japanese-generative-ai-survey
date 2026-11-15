# W34 Selection/Architecture independent editorial review — NEW (PROPOSAL_READY_FOR_PREFLIGHT)

Reviewer: NEW independent editorial Selection/Architecture reviewer. Not current author/operator/earlier content reviewer, not Root, not Human. No prior W34/SP authorship in this packet.
Recorded_at: 2026-11-14T12:00:00Z (packet DATA authoring date reused as review bound; actual review execution 2026-11-14, no active State/source write).
Scope: `notes/rephase-1-repaired-correction-rehearsal-20261112/` packet README + `astra-operation-resolution.md` §§12–18 FULL, adopted W34 PREARCH `73ab28ea` R2 under artifact epoch `ae0dd1e` (parent cc1c, source 773 final). Reviewed NEW `w34-selection-architecture-input.json` + `w34-selection-per-did-map.json` + `w34-selection-read-scope-and-pins.json` + `w34-selection-human-dossier-draft-ja-r4.md` vs actual 45M/354C/10H, 409 Matrix, 439 Ledger, 3 obligations LIMITED.
Method: source/data read-only. `read` + stdlib `hashlib/json/pathlib` counts/pins only. No project imports, no tests/build/runtime, no active writes/Git/network/Production, no reconstruct readback, no subagents. Own NEW review files only exception (this file + machine companion).

## 1. Authority and four-ref binding — PASS

- Runtime `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` epoch `ae0dd1e`, parent cc1c verified via read-scope pins. State `a8586351…` EVIDENCE_REVIEWED, PREARCH record `73ab28ea…`/6054B. Four active refs only (Evidence `eef77479` 409/Views `3727485a` 409/Ledger `066230f4` 439/Completeness `d869027a` LIMITED). Old canonical `f089cc4e` 41M noted inactive, not used. Hash prefixes rechecked match live files for State/Profile/record/Ledger/Completeness and for packet input/per-did/dossier (input `15375476…`/378396B, per-did `0b6808fc…`/443315B both exact match).
- Counts effective: Matrix 409 = 399 eligible +10 ineligible HOLD (c033/c035/c038/c051/c053/c054/c057/c065/c097/c103; 8 NEEDS_MORE +2 PARTIAL/HOLD). Evidence PARTIAL 363/VERIFIED 38/NEEDS_MORE 8. Views MATERIAL 45/CONTEXT 354/HOLD 10. Ledger = 409 Matrix +30 nonMatrix (26 EXCLUDED +4 DUPLICATE, 0 tasks, not assignable). Completeness 3 obligations LIMITED. No status upgrade claimed; 38V/363P/8N preserved as historical labels.

## 2. Assignment completeness — PASS (machine-verified)

- Input `assignments` 409 unique Discovery IDs, exactly once. Per-did `rows` 439 = 409 Matrix +30 nonMatrix. Cross-check input vs per-did: 0 disposition/usage mismatches. Runner dispositions: HOLD/NONE 364, SELECTED/PRIMARY 24, SELECTED/SUPPORTING 21, nonMatrix null/null 30.
- 10 ineligible all HOLD/NONE, none selected, none in packages. 30 nonMatrix separate packages (`non-selected-drop-*` + `non-selected-duplicate-*`), 0 tasks, carry-over C076/C077 disposal external to assignments (not assignment IDs). 26 EXCL +4 DUP accounting exact.
- 45 selected = 24 PRIMARY +21 SUPPORTING across 5 packages (P1 12/P2 13/P3 8/P4 8/P5 4). Primary set == package primary sets, supporting set == package supporting sets, no overlap, no duplicates across packages, no HOLD in packages. Each SUPPORTING exactly one destination (stricter than ≥1 minimum; audit-clear). Each PRIMARY exactly one destination.
- Memory `gap-aws-agentcore-memory-json` PRIMARY single P2 (r2 P1 double-listing fix preserved). `c102` Antigravity SUPPORTING single P3, no dual-role/split. No duplication.
- Paper 4 (15127/16096/21100/18389) SELECTED SUPPORTING single placements (P1 16096, P2 15127+18389, P4 21100). Per-did ledger CONTEXT→MATERIAL, evidence PARTIAL, views MATERIAL after accepted R2 (405 byte-identical +4 bounded claims). Now actual accepted, not packet DATA bypass. Vendor 41 +4 =45. 21095 explicit HOLD as counterfactual (box space), not silent drop.

## 3. Independent editorial judgments — PASS

Positive (independently sampled, not author repetition):
- 24 PRIMARY all VERIFIED first-party deltas (distribution/pricing/GA/safety/infra anchors with date-level/vendor qualifiers). No PARTIAL PRIMARY. Roles `WEEKLY_MAGAZINE:primary-story-anchor` + `WEEKLY:<package>` namespace-correct.
- 21 SUPPORTING = 15 PARTIAL (11 vendor boundary-date +4 papers) +6 VERIFIED background boxes (c087/c104/c105 +3 refresh). PARTIAL SUPPORTING all carry explicit `timing-UNRESOLVED vs 22Z` / `Sep8 capture UNRESOLVED` / `AUTHOR_CLAIM, no reproduction/deployment` qualifiers, restricted role, no status upgrade, no confirmed-W34 headline. Papers as bounded Research-Notes mechanism background (§§ bounds, maker-reported numbers), not core-event replacement. No blanket “maker-reported without deployment = unselectable” exclusion repeated; prior CHANGES_REQUIRED corrected.
- 6 VERIFIED SUPPORTING correctly not promoted to PRIMARY (control-plane/docs/essay framing, not weekly events). Chronology honesty preserved: all selected `window_relation MAIN_EVENT`; all OUT_OF_WINDOW (e.g. 15224/15389/15402/refresh K-bench etc.) HOLD.

Negative (independently sampled):
- HOLD 364 = 10 ineligible +354 CONTEXT. Sampled HOLD rationales carry lane/score/date/screening/cluster/title + distinct body bytes/SHA where read (e.g. 14927 556046B, 14967 112296B, 15008 1201745B) + maker-reported/no-reproduction + overlap reason + “no shallow year-group exclusion”. Not mechanical HOLD.
- 319 arxiv triage +26 body-read reused as history; remaining ~293 hash-only, explicitly NOT full semantic PASS. Prior r2 reviews reused as history, not re-read wholesale — appropriate limited scope. 39 non-arxiv each explicit reason. Counterfactuals retained: 6th technical package possible as supplement box but not core replacement; sparse 1-package rejected for ignoring VERIFIED deltas.
- Evidence 3 obligations LIMITED preserved (carry-over SATISFIED, current-relevance/technical-significance LIMITATION, closure null). Scope-appropriate, no auto-SAT.

## 4. Page arithmetic, inherited boundaries, Research-Notes box — PASS

- Page plan `target 15 max 16 notes: P1 3+P2 4+P3 2+P4 3+P5 2=14 base (P3 trio-merge) +1 Research-Notes box (P1 0.5 sidebar +P2/P4 0.5 notes, single box last) =15 target, max 16 allows 0.5 overflow`. Arithmetic 3+4+2+3+2=14 correct. Provisional, not measured Draft — appropriate as proposal DATA.
- Input package `boundaries []` is correct runner ergonomics: runner `run_selection_architecture_v2_interactive.py` inherits `remaining_boundaries` from Matrix (`[*src boundaries, *inherited]`). Final architecture will carry inherited Evidence boundaries; input empty does not waive them. `must_cover_requirements` unique string arrays (free-text with `weekly:*` prefix); validator requires uniqueness only — passes preflight shape.
- Research-Notes box is presentation within 5 packages, NOT 6th package object (packages 5 only, drafting_order 1–5, no empty-placement package). 4 papers each single SUPPORTING placement, no duplication, no unplaced extra. Wrapper empty-placement rule (at most one last empty package) not triggered — compliant.

## 5. Downstream required shapes — PASS (inspected, not trusted)

- Schemas: `candidate-selection-v2.schema.json` `9f7859d9…`/2618B requires `candidate_id/disposition/rationale/architecture_usage/publication_role/architecture_role/profile_extensions`; `issue-architecture-v2.schema.json` `215b73fb…`/4216B requires `package_id/title/purpose/primary_candidate_ids/supporting_candidate_ids/must_cover/boundaries/drafting_order/profile+publication_extensions`, `page_plan target/max/notes`, `human_review` nulls for PROPOSED. Config `95fe3c28…` namespaces `WEEKLY:` / `WEEKLY_MAGAZINE:`.
- Interactive runner `_validate_input` requires top-level exactly `{schema_version,issue_id,runner,assignments,architecture}`, assignments cover every Matrix Discovery exactly once with `WEEKLY_MAGAZINE:`/`WEEKLY:` prefix checks, packages reference known DIDs, no primary/supporting overlap. Input matches exactly (5 packages, selected_exceptions [] valid since all selected placed).
- Weekly derivation `survey_weekly_derivation_v2.py` `3bf9c2a4…`: `section_label` = `plan.publication_extensions.section_label` non-empty (input provides 5 Japanese labels); `closing_summary` = `publication_extensions.closing_summary {required true, heading non-empty, placement after_body_before_references}` + `profile_extensions.weekly_closing_summary {required true, source profile_synthesis.current_interpretation}`. Input provides exactly `closing_summary {required true, heading 今週の総括 — 分布と統治の週, placement after_body_before_references}` + `weekly_closing_summary {required true, source profile_synthesis.current_interpretation}`. Exact shape, no invent. No manuscript/Draft authored.
- Selection validator: SELECTED requires PRIMARY/SUPPORTING + ≥1 namespaced role, forbids HOLD/NEEDS_MORE selection, forbids roles on non-selected; architecture validator: PRIMARY exactly one destination, SUPPORTING ≥1, placements must cover `remaining_boundaries` via inherited merge. Input satisfies all checkable pre-conditions; full boundary cover will be enforced by runner inheritance.

## 6. Human-facing dossier completeness — PASS

- Dossier r4 `c22d3ad8…`/8122B explicitly: author DATA r4, prior versions preserved, independent semantic review required before canonical writer, no writer/Architecture approval/Human Gate/Draft/PDF/R4, 38V/363P/8N etc. existing labels not new PASS, author-only no Human approval. No `APPROVED` request, no completed `human_review` metadata, no genuine approval implied. Open questions (limited SUPPORTING scope, Copilot/Antigravity snapshot range, CoSnitch researcher-only, 21095 next, 15/16 tightness) honestly listed as Human hesitation points. Next steps: independent review → canonical writer (Discovery→candidate ID resolve, Matrix→Selection→Architecture→Summary→Attention no-overwrite, fail-closed preserve partials), missing primaries only if headline demanded, cost UNKNOWN lifecycle, no old canonical overlay/new fetch/State rollback/REQUEST_CHANGES/LOW bypass. Complete for preflight decision.

## Verdict

**PROPOSAL_READY_FOR_PREFLIGHT** (bounded proposal DATA only). NOT Selection PASS, NOT Architecture PASS/APPROVED, NOT Human Gate approval, NOT Draft/PDF/R4.

## Required next (bounded, no new generic features)

1. Canonical writer preflight only after this review: seven-slot no-overwrite preflight, basis pins (Profile/Matrix/Ledger/Completeness/Selection), role namespaces, inherited boundaries, `section_label`/`closing_summary` shapes. Single normal `run_selection_architecture_v2_interactive` invocation with exact reviewed input bytes; stop on first refusal, preserve partials, no retry/cleanup.
2. Normal Selection→Architecture transitions + `READY_FOR_ARCHITECTURE_REVIEW` summary/attention, then Human Architecture Gate. No Draft/PDF before genuine approval. `ARCHITECTURE_ESTABLISHED` remains pending Human Gate, not approved state.
3. No FullBodyReread of 293 hash-only, no new fetch, no source repair, no generic warnings. Future gaps (MSRC/NVD, Aug14/21 clock, Sep8/Copilot bytes) only if Human/root demands confirmed headlines.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
