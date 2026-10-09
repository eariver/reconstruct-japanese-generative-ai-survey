# LF-1 design correction (bounded; original preserved)

2026-10-09. Corrects `design-proposal.md` (sha256 `4860669aad6b4135cd252050a873aebe8e3628ba0707c3a567ebfae98437a289`, 733 lines, UNCHANGED).
No source/test edits, fixture/test execution, commits/ref writes, network, or LF-2 work.
Corrections are design text; feasibility stays proposed, not demonstrated.

## 1. Directive authority: bound route vs unbound sidecar (BLOCKED for integration)

- Bound carriage exists but creates no placement semantics. `derive_draft_package`
  copies Architecture `profile/publication_extensions` verbatim into the Draft Package
  (`survey_drafting_v2_base.py:365-366`); preservation into Results is validated
  (`survey_draft_profile_v2.py:22-43`, `survey_handlers_v2.py:334-350`,
  `survey_stage_validation_v2.py:448-450`). Schema free-object permits carriage;
  it does not authorize a new placement obligation. `docs/special-human-gates.md:13-23,41-54`
  preserves substantive Architecture/exception authority; extension allowance alone is not authority.
- The NEW synthetic initial shape (`THEMATIC_FOUR_FAMILY_LINEAGE_V1`) takes its
  final-summary obligation from the selected format (decision §4) as encoded in the
  existing consumer constant (`run_..._base.py:114-116`: heading `この号の総括`, ≥3 paras)
  and serializer order (`:101-103` summary before bibliography). The LF-1 projector
  therefore takes NO directive-file input: nothing invented, and for its own shape
  nothing applicable ignored. This distinguishes the constructible new route from legacy reuse.
- The legacy file `editorial/post-architecture-directives-v2.json` is an unbound sidecar:
  one unvalidated consumer (`:133-135` via `core.load_json`, exact-one-row placement check),
  after-the-fact manifest recording (`:202`), no producer/schema/validator/checkpoint artifact,
  absent from Human-gate inputs (`config/survey-production-v2.json:218-226`) and from approval
  binding (`survey_drafting_v2_base.py:105-134` binds architecture/summary/attention only).
  Search bound: AVAILABLE partial 409 worktree only (shallow; inherited unmaterialized history
  unsearched). Absence is bounded, not universal. No UNPROVED-as-accepted flag: that would invent
  a route (forbidden). No D1/D2/D3 selected: all three exceed this unit (new authority / publisher
  change / deferred acceptance claim).
- Precise unresolved relationship: the existing publisher still hard-requires the sidecar file
  at materialization (`:133-135` SystemExit). LF-1 reader output cannot satisfy that publisher
  without a demonstrated bound producer (none in available content) or a Human-authorized
  publisher change (LF-2 scope). Source-only projection design (as corrected) is NOT blocked;
  publisher/receipt/Gate integration IS blocked. Next: scoped blocker/design review + Human
  Commit Point, no workaround, no new schema authority.

## 2. Reader object: reader content only; one byte algorithm

- DELETE top-level `provenance` from the proposed schema/file entirely (also §1.1 key 15,
  §5.2). Mechanical context (State/Profile/Architecture/approval/Draft/Evidence/Card/Matrix/
  Materiality/Discovery refs, tool closure, `review_reference`/runner/recorded-at) returns as a
  SEPARATE in-memory `load_derivation` value, never written into the reader file. An excluded-hash
  field inside the exact reviewed file contradicts same-complete-reader-bytes admission.
- Move `as_of_source` (raw Profile `as_of`) out of the file: audit/mechanical context only.
  File keeps display values (`title` const, `display_as_of` + fixed prefixes) that are rendered.
- ONE canonical file-byte algorithm: `core.write_json` bytes
  (`survey_production_v2.py:86-92`: `json.dumps(ensure_ascii=False, indent=2)+"\n"`, utf-8);
  byte digest = sha256 OF THOSE BYTES (`sha256_file:99-100`). `sha256_object` (`:103-105`,
  sort_keys compact) is an in-memory comparator, NOT file identity. Proposal §5.2 conflation withdrawn.

## 3. Constants: enumerate actuals; single edition descriptor

- Technical-note labels, exact (`survey_longform_publication_v2.py:106-116`):
  `Chronology:`, `Technical points:`, `Limitation / attribution:`, `Primary URL:` (+ `Primary URL:`
  emitted via `\url{}` WITHOUT `tex_escape`, `:116`).
- Style defaults OBSERVED (`jgaisurvey.sty:60-73`): `SurveyTitle` lacks `Special`,
  `SurveyEditionDescriptor` defaults to Weekly (`週刊Technical Survey`); Longform emitted values
  (`Japanese Generative AI Technical Survey Special`, `Thematic Longform Special`, base `:87-88`)
  are explicit overrides, not defaults. Weekly `VISIBLE_TEXT`
  (`survey_weekly_derivation_v2.py:38-50`) MUST NOT be reused where it differs
  (edition descriptor, `WEEKLY SYNTHESIS` vs `ISSUE SYNTHESIS` kicker, cover labels/values).
- `cross_table_header` is an ordered ARRAY `["観点","GLM","Qwen","DeepSeek","Kimi"]`
  (wrapper `:138`), not a string. `toc_title`: future explicitly selected reviewed format string,
  NOT an observed class default (`\tableofcontents`, base `:95`, has no reviewed source in 409).
- Keep ONE `edition_descriptor`, in `visible_text` only; delete the `issue_metadata` duplicate
  (proposal §§1.2/1.3). No LF-2 serializer work in this unit.

## 4. Fixture chain to DRAFT_COMPLETE (proposed, not demonstrated)

- Concrete chain (existing producers only): per-stage `stage_validation.validate_stage` +
  `agent.build_stage_checkpoint` (`survey_agent_control_v2.py:1267`) +
  `advance_with_checkpoint` (`:1332`) with `approve_architecture` (`:1393`) after
  SELECTION_COMPLETE — the increment-B `_advance`/`_current_state` pattern
  (`test_survey_increment_b_weekly_derivation_v2.py:222-299`): discovery/screening/
  evidence+views/materiality/completeness/matrix/selection/architecture-trio/
  `draft-package:<pid>`+`draft-result:<pid>`/synthesis-input/result, ending in State AT
  DRAFT_COMPLETE (draft checkpoint passed, validation pending). `load_derivation` resolves
  exactly these checkpoint-bound refs; schema-only dicts never count. Original §2.3 omission
  of this chain corrected.
- Hard limit: DRAFT_COMPLETE's own 7 artifacts (`survey_stage_validation_v2.py:66-74`:
  reader-manuscript/validated-source/pdf/bundle/semantic+visual reviews/gate) have NO
  LONGFORM_SPECIAL producer in 409 (Weekly has `survey_weekly_semantic_publication_v2.py`;
  legacy Longform writer emits a different set under the UNCONFIGURED
  `stage:semantic-publication-validation` — base `:122`, `survey_semantic_quality_v2.py:46` —
  while config requires `stage:reader-publication-validation`, `:330-333`, which has NO registry
  entry, `survey_handlers_v2.py:452-479`). One-source four-family body is a structural
  type/identity fixture, never semantic sufficiency. Missing authority blocks; never fabricate State.

## 5. Source policy fixes

- `explicit_source_id=None` ALWAYS in LF-1: different-timestamp ambiguity refuses
  unconditionally (decision §5 first-subset rule). The adjacent-interactive single-binding
  fallback (`survey_bibliography_access_provenance_v2.py:154-167`; base `:175-178`) is
  unaccepted sidecar and MUST NOT supply it. Equal-timestamp rule follows the resolver
  (`:109-111`); no min/max/latest heuristics (`:59-60`).
- Lifecycle rule: `core.LIFECYCLE.index` comparisons (cf. weekly `:490`) + required configured
  `next_action=="stage:reader-publication-validation"` at DRAFT_COMPLETE. No lexical
  `lifecycle < ...` string comparison (proposal §5.3 withdrawn). Later-state readback behavior
  is LF-2 scope (decision §6.4: no blind write-entry restrictions on readback).
- URL safety: refuse `{whitepsace,{,},\,%,#,^,~,",<,>,|}` explicitly (ordinary URL-legal but
  TeX-unsafe in `\url{}`/`.bib` emission); non-ASCII/IRI handling DEFERRED to LF-2 real-serializer
  proof. Acceptance ≠ TeX safety. Drop the cross-package kicker-collision rule (ordinal/total in
  the string already distinguish); keep Architecture charset `^[A-Za-z0-9][A-Za-z0-9._-]*$`,
  empty-suffix refusal, and citation-key collision refusal.

## 6. Verification oracles (for the later implementation phase)

- Mutate AUTHORING/ACCEPTED inputs or trusted constants, then REPROJECT; never edit IR bytes
  directly (that tests only JSON serialization). Assert refusal (ValueError) vs changed canonical
  file bytes as disjoint outcomes. Raw-Draft-body mutation without updating archive/package/result
  hashes is an INVALID test (authority fails first — not reader stability evidence).
- Stability positives retain ALL real accepted bindings (same State/checkpoints/cards/matrix/
  ledger/discovery/synthesis) while varying ONLY mechanical context; assert identical file bytes.
- No-write inventory = full recursive pre/post file inventory + `git status` BEFORE any
  cleanup/repair (not git-only plus three filenames); no hidden finally-repair.

## 7. Preparation record (honest)

- `commands.txt` is an ABBREVIATED reconstruction (placeholder `find <SRC|DST>` line 22,
  aggregated pseudo-command line 23, no per-command exit/env transcript): preserved as-is, NOT
  raw replayable commands. `current-verify.sh` + `current-verification.log` (new, old logs
  untouched) verify CURRENT state only: proposal intact (733 lines), HEAD/tree/parent/status/
  remotes/shallow/no-alternates/no-overrides/refs-identical/device-shared-inodes-zero hold;
  `diff -r -q` finds exactly ONE cache difference (`.git/index`, refreshed by read-only status
  calls — not fixed content). Current checks cannot retroactively certify copy-time guards;
  full-history availability stays limited (shallow at baseline; inherited missing blobs).
