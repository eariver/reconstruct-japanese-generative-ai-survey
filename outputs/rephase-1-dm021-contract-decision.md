# DM-021 — correction authority/retention boundary and first component

2026-10-10. Astra selection after Human continuation at reconstruct **c50be33a0f1508c0ce306827d10a7c7746001384**. Source is exact409 + LF-2I9file overlay (publisher4d235a38/test4a03b564/helperd480e11d/derivationc09c5558/Gatee7305884), unchanged. This unit is source/design analysis: **no code/schema/test changes, fixtures, runtime tests, builds, commits or new intake**. DM-021 remains OPEN; whole NOT_READY, step4/B3 OPEN, canonical audit unstarted.

Read [General original](../notes/rephase-1-dm021-contract/analysis.md) with [Astra feedback](../notes/rephase-1-dm021-contract/astra-feedback.md) and [General correction](../notes/rephase-1-dm021-contract/correction-and-boundary.md). The choices below supersede conflicting proposals. Reuse [captured DM-021 evidence](../notes/rephase-1-dm021-intake/README.md); no TS-003 exception, primary-record acquisition or Production policy adoption is implied.

## 1. Decision

Select **DM021-P1: read-only editorial proposal/before-set/proposed-reader validation**, as a bounded preparatory implementation unit. It establishes the exact data and reviewer-scope relationship needed before designing destructive promotion. It does **not** add a revalidation reason, write live source/State, create an approval/PASS, retain bytes by itself or repair the normal post-validation continuation yet.

Initial proposal capability covers:

- Generated **THEMATIC/LONGFORM_SPECIAL four-family-lineage-v1**: its existing publication-authored cover/frontmatter/final summary and `longform_revision` content, still constrained to current accepted package sources. This is the primary correction fixture because it has an actual publication-authored body surface.
- Generated **WEEKLY_MAGAZINE**: only the existing publication-authored cover/frontmatter/final-summary envelope, preserving the accepted closing-synthesis requirement. No accepted Draft headline/deck/body override, bibliography-entity rewrite or new reader patch language.

Current accepted upstream/Architecture/Draft/Synthesis and code/contract epoch must remain valid and unchanged for the proposed operation. DIRECT_PRIMARY/manual, directive-bearing Longform, new upstream/story/Architecture decisions, decided Preview, FROZEN/RELEASED corrections, mixed Core+editorial changes and old-epoch receipt migration are not selected. Normal healthy later readback from LF-2I remains preserved.

This replaces the unsupported four-path Weekly-only “restores Special” claim. It is justified investment in independently verifiable proposal/closure semantics, not an enum-only pseudo-fix or an unverifiable writer. Runtime feasibility and net savings are not established by this design; independent review and later implementation evidence remain necessary.

## 2. Current facts that constrain the design

1. Actual controller API is `revalidate_publication_surface:1773`, which adopts already regenerated/QA-validated live bytes. The reason constant/schema admit only `REVIEWED_CORE_CHANGE`; that label alone does not mechanically prove an actual reviewed Core delta. Do not claim an operational changed-reader producer merely from its docstring.
2. R1 admits a reviewed change to `survey_weekly_derivation_v2.py` only, unchanged reader/output/criteria, post-install receipts and a real non-no-op. Its receipt/Gate/State retention and guarded failure handling are useful patterns, not a changed-reader owner.
3. `_publication_revalidation_roles:685–693` maps **seven** checkpoint roles: manuscript, primary source, PDF, quality bundle, later semantic review, visual review and Gate. It does not directly include reader JSON, authoring archive, receipt, bib/style, deterministic result files or Candidate.
4. Revalidation rows' `prior_sha256` refer to the **original validation checkpoint**, even on repeat. The active-before values come from the State-bound current record's effective rows. Historical `live=False` checks preserve record-chain integrity, not proof that replaced old artifact bytes were retained.
5. Weekly body text/headline/deck are derived from accepted Draft and closing interpretation from accepted Synthesis. Longform revision prose is publication-authored within accepted-source constraints. A general body correction cannot be silently implemented by changing Weekly authoring metadata.
6. Existing independent semantic/visual review is ChatGPT-owned; formal Human Architecture and Publication Preview are distinct. Config77–85 and existing role contracts do not establish a new “Human editorial/QA gate.” `reviewed_by` text is not proof of genuine Human approval.

## 3. Three identities, one verified before graph

Keep distinct throughout:

| Identity | Meaning |
|---|---|
| Original baseline | exact immutable validation checkpoint path/hash and its original7 rows |
| Active before | current exact State + optional State-bound revalidation predecessor/chain + effective current7 rows and their validated dependencies |
| Proposed after | newly authored, unadopted reader input at an immutable proposal path; no State authority |

P1 must start from **healthy VALIDATED_DRAFT**, approved Architecture, Preview pending with no provenance, downstream checkpoints pending, inactive exception. Validate the real State and current active revalidation pointer; never infer the active version from directory recency or a schema-valid unreferenced file. A referenced-invalid record is a stop, not fallback to original bytes. Do not manufacture a DRAFT_COMPLETE dictionary or invoke a pending-basis bypass.

Resolve the seven effective rows using existing State-bound revalidation semantics. Then independently validate and enumerate their **finite typed dependency graph**:

- manuscript→Profile/Architecture/approval/primary/BIBLIOGRAPHY/STYLE;
- Gate→selected manuscript, reviewed reader input, pre-TeX review and generated receipt;
- receipt→accepted refs, publication authoring archive, Draft archive, reader/review/output refs and current tool/contract basis;
- quality bundle→source/PDF/check-result files; later reviews→exact manuscript/source/PDF;
- original checkpoint, State-bound predecessor record chain and relevant upstream authority remain exact immutable references.

Use actual existing validators and their verified refs, not a generic recursive “follow every path-looking string” resolver. Shared physical files may have multiple logical edges; conflicting hashes for one path, unknown executable inputs, duplicate roles or unresolvable required refs stop. Source-only helper functions may assist, but raw path presence never supplies acceptance.

An existing canonical Candidate is optional **observed/unadopted data** at this lifecycle. If present, require the actual candidate validator and exact agreement with the active-before publication; otherwise stop. Include its bytes in the proposed retention set without claiming State adoption or permission to overwrite it. Do not discover arbitrary alternative Candidates or bless an unknown canonical file.

## 4. Proposed artifact and read-only APIs

Names in this section are **new proposed interfaces**, not present fields in the current candidate.

Use a narrow `schemas/editorial-correction-proposal-v2.schema.json`, with strict top-level keys:

- `schema_version`, `proposal_id` (safe fixed token), `issue_id`, `research_profile`, `publication_profile`, `route=EDITORIAL_CORRECTION_PROPOSAL_V1`, `status=PROPOSED`;
- `basis`: exact State ref, original validation checkpoint ref, optional active-revalidation ref, current reader-input ref, canonical digest of the independently enumerated before graph, preserved-upstream digest and current validated generated-receipt ref;
- `proposed`: exact publication-authored input ref, exact proposed-reader ref and nonempty change description;
- `retention_plan`: closed typed rows described in §6. No review/PASS/receipt/Gate/Candidate AFTER references in this proposal.

Proposed files use `<source_root>/publication/v2/editorial-corrections/<proposal_id>/` for `authoring-input.json`, `reader-surface-input-v2.json`, `proposal.json`, and an explicitly supplied review record. P1 creates no directory or file: an author/test fixture supplies named files, or consumes the preparation API's in-memory values with explicit separate persistence. Reject aliases/traversal/noncanonical proposal layout before reads. These versioned paths are unadopted and must not replace the live canonical reader/source files.

Proposed new `scripts/survey_editorial_correction_proposal_v2.py` APIs:

1. `prepare_proposal(root,state_path,authoring_path,proposal_id)`: read-only current-before validation and real proposed derivation; returns prospective proposal, canonical reader bytes and mechanical binding data in memory, **not approval**. It may calculate refs for the not-yet-persisted proposed reader from those bytes; no successful persisted-file claim follows.
2. `validate_proposal(root,state_path,proposal_path,scope_review_path=None)`: rederive before graph and proposal from actual named input bytes, compare exact canonical proposed-reader bytes and all bindings/plan rows; optionally verify the scope review (§5). Return a clearly typed deterministic result (`REVIEW_REQUIRED` or `REVIEW_BOUND_PROPOSAL`) and input hashes, not a Reader-Surface PASS, Gate or revalidation record.

Proposed reader content must come through existing real accepted-source derivation: Longform healthy readback loader with the new authored input, or Weekly healthy current-state loader without a pending bypass. Exact accepted refs/Draft archive/Architecture approval remain equal. Require proposed reader FILE bytes differ from active-before reader bytes; same-byte metadata-only change is not an editorial correction and gets an explicit no-editorial-change refusal, not automatic routing to R1.

Reject changes to frozen fields through actual rederivation/schema checks, not only a claimed `upstream_unchanged=true`. Require source/authority/code snapshots stable throughout the inspection; report observed drift without writes. Same-Core means validated control/contract equality/ancestry, not necessarily identical Git HEAD after harmless artifact-only commits. Pre-feature/mixed-epoch cases stop; current generated receipt replay remains strict. First witness can be a new synthetic edition generated under the new component's committed fixture code; it does not migrate TS-003.

## 5. Correction-scope relation uses the existing independent review

Select **a narrow optional `editorial_correction_scope` block in the existing Reader-Surface semantic-review schema**, not a new normal Human Gate or a separate parallel review role. Existing ordinary review records remain valid without it. P1 requires the block when a caller asks for `REVIEW_BOUND_PROPOSAL`; bare corrected PASS/free reason/reviewer name is insufficient.

Proposed strict block fields: version `EDITORIAL_CORRECTION_SCOPE_V1`, decision (`WITHIN_APPROVED_AUTHORITY`, `REQUIRES_OWNER_DECISION`, `REJECT`), exact `before_reader_input{path,sha256}`, `preserved_upstream_sha256`, nonempty `change_summary` and `evidence_locations`. The existing `reviewed_surface{path,sha256}` identifies the **after** reader artifact, and existing reviewer/timestamps/digest identify the reviewer statement. Require an explicit `EDITORIAL_CORRECTION_SCOPE` check with substantive old/new/approved-authority evidence, as well as all existing semantic checks; positive eligibility requires PASS and WITHIN_APPROVED_AUTHORITY, with exact before/after/upstream bindings.

The assessor is the existing independent ChatGPT semantic/editorial reviewer. It judges whether the proposed delta remains within the approved Architecture/source constraints while reviewing the proposed reader surface. Material new editorial/Architecture choices are routed to existing Owner/exception/upstream authority; P1 only refuses/records that need and does not open or resolve a Human Gate. Later post-PDF semantic/visual review and exact Human Preview remain mandatory.

Do not bind this semantic-scope relation to every runner/debug/State timestamp or the whole mutable plan. Its exact before reader + after reader + frozen-upstream relationship is separate from the proposal's stricter operational State/predecessor/code/retention snapshot. Operation staleness still fails; it is not automatically a change in reader semantics. Machine type/hash validation cannot prove genuine reviewer independence or semantic truth, and P1 must not generate the review's PASS/block itself.

`repair-set-v2` and `review-finding-v2` lack this exact replacement relationship and State consumer; they may describe the finding but cannot substitute for the block. Its first consumer is ONLY the new proposal validator. Merely adding a block to a review never authorizes existing revalidation or publication adoption.

## 6. Retention plan, immutable review paths and later adoption limit

P1's plan distinguishes `KEEP_IMMUTABLE` for upstream/checkpoint/prior revalidation records and `COPY_BEFORE_REPLACEMENT` for old mutable publication artifacts in the verified graph. Each row has role, exact source path/hash/byte-count and either the unchanged retained reference or a deterministic safe future destination under `<proposal_dir>/retained/before/<original_repo_relative_path>`. Deduplicate physical destinations while preserving logical edges. No omitted reader/archive/receipt/bib/style/QA/review/PDF/Gate/Candidate dependency, no unknown input, no self-referential retention of the plan/review being created.

This validates a **retention plan**, not retained-byte existence or authorization to delete/replace. It writes/copies nothing. The later owner must actually preserve and verify old bytes before replacement, preserve original checkpoint rows and active-predecessor identity separately, and enforce guarded owned-file rollback/manual-stop semantics.

The dependency DAG is acyclic: before snapshot + new authored input → proposed reader/proposal → independent scope review (old reader/upstream and new reader bindings only) → future source/receipt/Gate/QA → future revalidation adoption. No proposal↔review or receipt↔adoption-record hash cycle.

**No “path rebind + same SHA” shortcut is adopted.** An immutable review over a staged path does not become a review of another canonical path merely because file contents match. Preserve the versioned reviewed reader artifact and exact review bytes. A future correction-specific receipt/admission contract must explicitly connect that reviewed artifact to live generated outputs, or obtain a genuine new review for a different target. Current initial receipt/Gate canonical-path restrictions remain intact in P1. General correction§5's ambiguous path-rebind language is superseded.

Full promotion is intentionally not selected yet: old live authority stays healthy during preparation/review; later multi-file promotion may temporarily fail closed rather than stay continuously valid. Its owner must serialize cooperating writers, preflight the full new set, retain old bytes, verify actual new replay/QA, install an immutable supersession record and adopt the State pointer, then use the normal new Candidate→Preview→Freeze→Release chain. No fake former State, unbound staged-path fallback, global CAS/crash recovery or stale approval reuse. These are requirements for the later design, not runtime claims from P1.

## 7. First implementation budget / acceptance / stop

Expected DM021-P1 paths: **A** proposal module above, **A** proposal schema, **M** `reader-surface-semantic-review-v2.schema.json` (optional strict scope block only), **A** focused `tests/test_survey_editorial_correction_proposal_v2.py`. Existing controller/revalidation schema, publishers, receipt/Gate runtime, stage/fidelity/Freeze/Release code remain read-only in this component. Necessary extra runtime path or lack of safe real-loader reuse returns to Astra before editing; no four-file promise overrides a demonstrated blocker.

Before implementation, General returns exact before-graph role enumeration/dedup rules, schema/API shape, and a real accepted-fixture plan (not success mocks). Then implement only the read-only component under the selected budget. Required future evidence:

- healthy generated Longform VALIDATED_DRAFT with a meaningful publication-authored prose correction; Weekly's narrower authored-field positive plus immutable-body/upstream negatives;
- original-checkpoint vs active-before distinction with a real valid predecessor pointer when constructible (never a filename-selected or forged active record); stale/invalid pointer stops;
- exact proposed derivation/FILE bytes, missing/extra/conflicting retention rows, aliases, stale State/accepted refs/code epoch and absent current dependencies refuse; all calls leave owned trees/State/refs unchanged;
- absent scope block yields review-required (not adoption); invalid/missing/wrong-before/wrong-after/stale-upstream/reject/needs-Owner decisions cannot become review-bound; genuine schema-valid synthetic scope PASS binds exact targets through existing review loader;
- ordinary pre-TeX reviews remain compatible with the optional schema extension; current LF-2I/Weekly/direct-primary and Core-change/R1 source behavior is unchanged, with only affected checks selected;
- scope/data fixtures are synthetic type/identity tests, not semantic acceptance, real corrected PDF, retained-history bytes or normal correction continuation.

If healthy active-before authority or proposed derivation cannot be constructed without new authority, live mutation or a false reason, return the precise blocker; do not add pending or lifecycle exceptions. No candidate commit is authorized; source remains an exact-hash overlay, testing uses existing independent synthetic Git-fixture discipline and no empty commits. Preserve all failed evidence and true pre/post guards, no old-script/old-suite rerun by default.

Obtain scoped author-independent design review and resolve findings, then stop at this **design Human Commit Point**. Next unit is DM021-P1's concrete interface/fixture return followed by bounded implementation, not live correction adoption. DM-021 remains OPEN_CORE/EDITION_WORKAROUND (reported Production status), fixed baseline774 and Production read-only boundaries remain.
