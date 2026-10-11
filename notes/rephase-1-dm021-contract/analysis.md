# DM-021 post-validation editorial-correction contract analysis

2026-10-10. General read-only Co-Worker. Scope: eight questions in
`notes/rephase-1-dm021-contract/task.md`. No code/schema/test edits, no
fixtures/builds/commits/network/old scripts. Source §0. Whole NOT_READY,
step4/B3 OPEN, audit unstarted. STOP for Astra; no code authorized.

## 0. Actual source binding (summary; full record in `source-binding.md`)

- Base: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- Worktree delta vs HEAD: 2M tracked
  (`scripts/survey_reader_surface_gate_v2.py`,
  `schemas/reader-surface-gate-v2.schema.json`) + 7 untracked LF-2I paths =
  exact 9-file overlay. All 9 SHA256 match final correction3
  `hash-manifest.json`: Gate `e7305884…`, gate-schema `fe4a96f4…`,
  LF manifest `4dadf873…`, LF input `7bae9d2a…`, derivation `c09c5558…`,
  generated `d480e11d…`, publisher `4d235a38…`, tests `ce687447…/4a03b564…`.
- Reconstruct HEAD `c50be33a0f1508c0ce306827d10a7c7746001384` observed clean
  except this new untracked packet. DM-021 evidence reused only:
  Summary `afdb3df3…`/blob `62ee6a6b…`/SHA `7c84b6d8…`, lines 690–727.
  Main/Issues/records/corpora not acquired; TS-003/560/561/37955511006 stay
  reported-secondary. Fixed reason-only restriction statically re-corroborated.

## 1. Change taxonomy / present refusal

- Only reason: `scripts/survey_agent_control_v2.py:45`
  `REVALIDATION_REASON_CLASSES={"REVIEWED_CORE_CHANGE"}`; schema
  `schemas/publication-surface-revalidation.schema.json:26` const same.
  Producer `establish_revalidation()` (`survey_agent_control_v2.py:1777ff`)
  refuses anything else at `:1789-1790`; requires non-empty `reason` +
  `executor` string at `:1791-1794`. Free text + identity string is not a
  typed decision (see §2).
- Supported NOW: (a) unchanged-reader mechanical renewal via R1
  (`scripts/survey_weekly_mechanical_refresh_v2.py:36` same reason;
  `docs/weekly-mechanical-refresh.md:33-36`; §4). (b) Shared-Core changes
  that regenerate publication-surface bytes with complete fresh QA:
  `establish_revalidation` docstring `:1783-1787`, upstream-drift refusal
  `:1871-1874`, canonical-role mapping
  `_publication_revalidation_roles()` `:685-693`, pending-row collection
  `_collect_pending_rows()` `:711-743` (exact checkpoint ref, `require_change`,
  noncanonical/upstream refusal `:740`), pre-decision gates
  `_pending_conditions()` `:696-708` (VALIDATED_DRAFT, arch approved, Preview
  pending/no provenance, Freeze/Release pending, Exception inactive).
- Unsupported NOW (refused, not skippable): post-VALIDATED_DRAFT
  editorial/source-fidelity correction within unchanged approved research.
  It is not a shared-Core change; labelling it `REVIEWED_CORE_CHANGE`
  misstates authority; rewriting `DRAFT_COMPLETE.json` or publishing its old
  PDF violates exact-byte provenance (Summary 698). No
  `REVIEWED_EDITORIAL_CORRECTION` exists in code/schema/tests.
- Must stay unsupported: new upstream Architecture/Evidence/Selection/Draft
  changes (refused by `:1871-1874`, `_check_immutable_revalidation_rows()`
  `:847-949`, `survey_stage_validation_v2.py:_merge_artifacts:224-230`),
  already RELEASED editions (§6), directive-bearing/pending-regeneration
  Longform routes (§5), `EXCEPTION_*` as normal authority (§6).

## 2. Correction authority: gap, not prose approval

- Existing: Architecture approval
  (`schemas/architecture-approval-record-v2.schema.json:7-17`: `APPROVED`,
  arch/summary/attention SHAs, `reviewed_by`, `review_reference`) preserves
  upstream. Semantic review
  (`schemas/reader-surface-semantic-review-v2.schema.json:14-15,58-59`:
  `PASS/FAIL`, `reviewed_by`, `reviewed_surface{path,sha256}`,
  `review_sha256` object digest) and Gate semantic authority
  (`schemas/reader-surface-gate-v2.schema.json:134-149`) judge corrected
  bytes only; R1 notes raw-file SHA vs object digest are distinct by design
  (`survey_weekly_mechanical_refresh_v2.py:1006-1012`). Preview approval
  (`schemas/publication-preview-approval-v2.schema.json:7-21`: `APPROVED`,
  candidate path/sha, pdf path/sha, `reviewed_by`, `review_reference`;
  producer `survey_human_gate_v2.py:660-712`) judges the NEW Candidate/PDF
  after revalidation; revalidation `establishment` block (schema `:47-71`)
  snapshots pre-decision pending state separately.
- None expresses the necessary old→new editorial decision before pending
  Preview: who reviewed the correction as a correction, what old bytes were
  judged wrong, what new bytes replace them, under what unchanged-research
  scope and evidence reference. `reason` free text + `executor` string +
  corrected PASS + file/hash alone do not supply that relation.
- Missing relation (minimum, no new Gate/role): narrowly typed
  `editorial_correction_decision` record/field, owned by the existing Human
  editorial/QA reviewer role (same humans who sign semantic PASS and Preview
  approval): correction_id/issue_id; old set (prior checkpoint path/sha +
  superseded prior SHAs); new set (new SHAs/byte_counts); scope attestation
  (Architecture/Evidence/Selection/Draft unchanged, editorial/source-fidelity
  nature); `reviewed_by/review_reference/recorded_at`; exact binding to the
  fresh QA inputs. `establish_revalidation` must require and validate it when
  reason is editorial; Preview approval still follows for the new Candidate.
  If Astra rejects even this record, the alternative is explicit: editorial
  corrections stay unsupported (no silent enum-only fix).

## 3. Identity / supersession

- Old immutable: `checkpoint_provenance.validation{path,sha256}` → staged
  `DRAFT_COMPLETE→VALIDATED_DRAFT` record (`:719`, `:1823-1837`); never
  rewritten (`:1785`). Active predecessor:
  `publication_revalidation_provenance{path,sha256}` → `…-rN.json`, chained
  via `supersedes{path,sha256}|null` (schema `:43-46`; chain walk
  `_check_revalidation_chain()` `:952ff`; R1 predecessor handling `:949-963`).
- Prior/current reader input, archive, manuscript/bib/style/PDF/quality/
  reviews/Gate/Candidate bound per-row: `superseded_artifacts{name,path,
  prior_sha256,new_sha256,byte_count}` + `preserved_artifacts{name,path,
  sha256}` (schema `:30-38`); row-union must equal prior checkpoint
  (`:916-917`); validation block rebinds manuscript/bundle/semantic/visual/
  pdf to rows (`:926-949`); live drift refused (`:894-915`).
  `_prior_artifacts()` in `survey_stage_validation_v2.py:159-198` already
  substitutes `new_sha256` for superseded rows — schema consumers handle
  supersession there. Other readers of raw checkpoint artifacts do not; they
  must go through active-revalidation resolution, not raw checkpoint bytes.
- Object digests vs file SHAs vs State provenance are distinct: review
  `review_sha256` (object digest), receipt/Gate file SHAs, checkpoint/State
  SHAs, `core.implementation_commit_sha`/HEAD. Repeated corrections must
  select the single live `publication_revalidation_provenance` pointer plus
  full `supersedes` chain, never an arbitrary latest file; sequence
  collision refused (`:1954-1957`, `:2022-2023`).

## 4. Retention / ownership / write order; why R1 does not extend

- Canonical-file replacement problem is real: correction replaces live
  files that existing records point at. R1 solves only its own scope:
  old receipt + old Gate + old State bytes retained under
  `publication/v2/.mechanical-refresh-retention/<run-id>/` with hashes
  (`docs/weekly-mechanical-refresh.md:40-46`; implementation
  `:1270-1318`), same-directory temp + atomic replace from known bytes,
  pre-write old-hash rechecks, exclusive record create (`xb`), bounded State
  temp+replace, owner-aware restore preserving unknown bytes (`:2024-2130`
  pattern; R1 `:73-80,1130-1600`). It retains receipt/Gate/State only, for
  same-byte-output mechanical renewal (`WEEKLY_MAIN_BIB_STYLE` `:974-975`,
  no-change refused `:35-36`), not changed-reader source/review/manuscript/
  PDF/quality/bundle retention.
- Minimum for editorial correction: same operation-owned pattern extended to
  the full changed set (old reader source/input, old manuscript/outputs,
  old PDF/quality/reviews/Gate/Candidate inputs as touched): canonical-path
  derivation, alias/traversal refusal, full snapshot + guard, per-write
  old-hash recheck, exclusive new-record create, temp+replace State, truthful
  partial-failure preservation; no global CAS/crash framework, no universal
  resolver, no stored success before real validation/review/adoption. Refusal
  must leave old valid publication state intact.

## 5. Regeneration path (both initial publishers refuse correction)

- Weekly initial: `survey_weekly_semantic_publication_v2.py:67-68` requires
  `DRAFT_COMPLETE`; existing-input mismatch refused (`:77-80`); no-write
  overwrite guard (`:35-37`); legacy base adds only pending
  RELEASE_CANDIDATE Preview revision
  (`run_semantic_publication_v2_interactive_base.py:122-124`), not
  post-VALIDATED_DRAFT changed-source renewal. Weekly derivation in
  VALIDATED_DRAFT without pending basis enforces strict State and builds a
  pending basis only if rows changed (`survey_weekly_derivation_v2.py:481-500`).
- Longform initial (LF-2I): two-pass only —
  `survey_longform_semantic_publication_v2.py:1-9` (pass1 reader only; pass2
  needs materialized reader + validated persisted PASS; no legacy writer,
  no pending-regeneration/changed-output renewal); derivation requires exact
  `DRAFT_COMPLETE` + action (`survey_longform_derivation_v2.py:1122-1131`);
  readback allowlist explicitly rejects pending/revalidation bypass
  (`:1142-1153`). Do not call LF-2I route or R1 writer a correction owner.
- Required concrete changes: a real correction owner writer (new bounded
  module, modeled on R1 ownership semantics but for changed bytes) that
  prepares a changed-reader source set, persists fresh pre-TeX review, fresh
  exact outputs/PDF/quality/later reviews/Gate, while normal State/readback
  stays valid; plus §2 authority + §4 retention + §7 budget. Fidelity/depth/
  layout and independent review responsibilities preserved; no auto
  semantic/visual PASS, no mutable old checkpoint.

## 6. Normal continuation; stale-approval invalidation (static, not witnessed)

- Statically: establishment requires Preview pending + no provenance +
  Freeze/Release pending (`:1803-1809`, `:696-708`), so no old approval
  survives into the correction record. Afterwards the normal chain is
  unchanged: new Candidate → new typed Preview approval
  (`survey_human_gate_v2.py:660-712`) → Freeze binds exact candidate +
  approval + pre-preview visual (`survey_publication_v2.py:185-197`;
  `survey_stage_validation_v2.py:588-595`: candidate/pdf/approval SHA
  equality, `…PDF authority diverged` refusal) → Release verifies frozen
  bytes. Stale same-issue Candidate/PDF/approval are rejected by SHA
  mismatch, not by version recency.
- This is conceptual feasibility from static paths above. No executed
  correction→Candidate→Preview→Freeze→Release witness exists here; LF-2I
  normal FROZEN/RELEASED readback is healthy-authority replay, not a
  correction witness. No caller in read scope contradicts the design, but a
  future implementation must produce the witness; if one appears, return its
  exact blocker and minimum decision. `EXCEPTION_FROZEN/RELEASED` are not
  substitutes; no permission to correct an already RELEASED edition is
  inferred (TS-003 exception stays edition-local secondary evidence).

## 7. Smallest coherent increment / budget / cost

- Recommend bounded operation C1: one Weekly editorial-correction renewal
  (changed reader source within unchanged approved research) with §2 typed
  decision, §3 supersession, §4 retention, §5 Weekly owner, §6 normal
  continuation. Longform correction owner explicitly deferred; LF-2I initial
  route untouched. Enum-only (`REVIEWED_EDITORIAL_CORRECTION` string alone)
  rejected as insufficient; universal resolver/crash framework rejected.
- Path budget (exact): M `schemas/publication-surface-revalidation.schema.json`
  (new reason + required decision authority block); A
  `schemas/editorial-correction-decision-v2.schema.json` (narrow record); M
  `scripts/survey_agent_control_v2.py` (reason set, establish/validate/chain/
  pending-basis, CLI `--reason-class` at `:2322`); A new bounded Weekly
  correction writer (retention/inventory/preflight/snapshot/exclusive
  writer/failure semantics); read-only `survey_weekly_derivation_v2.py`,
  `survey_weekly_semantic_publication_v2.py`, `survey_stage_validation_v2.py`,
  `survey_human_gate_v2.py`, `survey_publication_v2.py`,
  `survey_weekly_mechanical_refresh_v2.py` (non-regression). Reuse vs cost:
  reuses pending-basis/supersession/stale-rejection/retention patterns, but
  new decision schema + writer + review/QA + independent review are real
  costs; unknown cost is not zero; independent review is not duplication.
- Unsupported afterwards (and why useful anyway): RELEASED editions, new
  upstream/Architecture authority, Longform changed-output renewal,
  general Thematic/Retrospective/manual, crash-atomicity. C1 still restores
  truthful Weekly/Special viability for the TS-003-shaped gap without
  legitimizing the one-off exception.

## 8. Future acceptance oracles (do not execute now)

- Real accepted Git-aware Weekly fixtures (committed synthetic DBs, exact
  HEAD pins); true vs false reason classes (editorial within unchanged
  research vs shared-Core change vs upstream change vs released edition);
  missing/forged/stale decision provenance; unchanged vs changed upstream;
  old checkpoint immutability + retention-byte presence; exact new-byte
  review/admission (fresh semantic/visual PASS bound to new SHAs, Gate +
  receipt replay); stale same-issue Candidate/approval rejection;
  first/repeat corrections via `supersedes` chain + sequence-collision;
  idempotence/drift/partial-failure/retention controls; Core-change and R1
  same-byte non-regressions. Separate type/identity fixtures from genuine
  research/rendered/semantic acceptance (synthetic blank-PDF PASS is not
  publication acceptance); no `EXCEPTION_*` fixtures as normal authority.

## Open authority questions for Astra

1. Is the §2 narrowly typed old→new decision record (Human editorial/QA
   owner, no new Gate) the selected authority, or do corrections stay
   unsupported? 2. Is Weekly-only C1 the selected first boundary, or a
   source-only schema/controller preparatory boundary first? 3. Any needed
   primary intake beyond saved `afdb3df3` before contract selection?
