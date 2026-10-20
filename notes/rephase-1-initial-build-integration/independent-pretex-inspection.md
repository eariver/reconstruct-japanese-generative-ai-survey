# Independent pre-TeX semantic inspection — initial real-build integration (R2)

Reviewer role: AUTHOR-INDEPENDENT semantic reviewer. Not the fixture/code/build
author, not Astra/root, not seven-point auditor, not Human Gate. No code, tests,
network, Git mutation, TeX build, or approval JSON produced here.

Task entry: `notes/rephase-1-initial-build-integration/astra-execution-selection.md`
(items 4–5, 8) + `notes/rephase-1-initial-build-integration/fixtures-20261019T133259Z/README.md`.
This inspection is the required author-independent pre-TeX check before any
pass2 TeX/Bib/style materialization. It does NOT authorize pass2, Gate, QA,
Candidate/State promotion, or any synthetic PASS converted to production PASS.

Tool disclosure: `apply_patch` absent in this environment; this file created with
dedicated `Write` only (mkdir not needed — parent dir exists). No other writes.

Date of inspection (UTC): 2026-10-19. Standalone surface read; no rendered
PDF/log/digest examined (builds not yet run at inspection time per STOP §7).

## 1. Read scope (exact)

All reads read-only. No fixture DB, source, or reconstruct mutation.

- Selection: `notes/rephase-1-initial-build-integration/astra-execution-selection.md` (24 lines)
- Fixture report: `notes/rephase-1-initial-build-integration/fixtures-20261019T133259Z/README.md` (184 lines)
- Weekly surface: `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture/sources/2026-W37/publication/v2/reader-surface-input-v2.json`
  SHA256 `136c0dd8a2bf4c5b4323993ff3882524c760d902f2a463b93bcd6fe95a948635`, 2648 B, `issue_id 2026-W37`
- Weekly authored: `…/weekly-fixture/sources/2026-W37/semantic-publication-input.json`
  SHA256 `3a15b12ae61dda0f7dc17dd115fa012bb10de85d0b2b3215cd90c93dffc0c0cf`, 617 B
- Weekly State: `…/weekly-fixture/sources/2026-W37/production-state.json`
  SHA256 `de45bc659cbddc603c4dfb58f05a47123adb7ebf3c0c19f5fb4e11d16b5aceb1`, 5392 B,
  `DRAFT_COMPLETE`, `next_action stage:reader-publication-validation`
- Special surface: `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/special-fixture/sources/SP001/publication/v2/reader-surface-input-v2.json`
  SHA256 `f40db7f6f88f099e13162f51296d0b24874922d80a7ef31fd85329b85a957cd5`, 7071 B, `issue_id SP001`
- Special authored: `…/special-fixture/sources/SP001/semantic-publication-input.json`
  SHA256 `92434aad3817e072605f806fffb6d5163a6bc9eba76e0790bdbf730d490f7a81`, 5297 B
- Special State: `…/special-fixture/sources/SP001/production-state.json`
  SHA256 `907bffd0eda7d5a9980c4aa2755ca46e36bd7fb5c02753a844a8a2f9b19e70d7`, 5359 B,
  `DRAFT_COMPLETE`, same `next_action`
- Accepted-chain spot reads (fidelity basis, same fixtures, content quoted below):
  `discovery/discovery-accepted-v2.json` (both), `draft/v2/packages/pkg-001/draft-package.json` (both),
  `draft/v2/packages/pkg-001/draft-result.json` (both), `gates/architecture-approval.json` (both)
- Pin cross-check: `fixtures-20261019T133259Z/weekly-surface-pin.json`,
  `special-surface-pin.json`, `weekly-authored.json`, `special-authored.json`
  (surface/State/authored SHAs above match pins; verified by re-hash this inspection)

NOT read: full screening/evidence task JSONs beyond draft-package-embedded
evidence cards, full checkpoint JSONs beyond State provenance pointers, TeX
toolchain, schemas/scripts, workflow PDFs. That is an explicit coverage limit —
see §5.

Fixture isolation context (from fixture README, not re-verified here):
weekly source-commit `88813a01accb320b5948e368618e4061a4d72e0b`,
special `d4078d1bc851b9977289acf4b9cd6560c080b69e`, inert origin
`https://example.invalid/initial-build-fixture.git`. Accepted as declared
context; isolation not re-audited in this inspection.

## 2. Distinction enforced

- (A) Integration fidelity: does the reader object structurally/semantically
  match the declared synthetic evidence + authored content, and is it useful to
  exercise the renderer (single-package path, citation keys, kicker/table slots)?
- (B) Production quality: would this content satisfy real research sufficiency,
  readability, and citable authority for a Weekly / LONGFORM_SPECIAL edition?
  Answer is NO for both routes (placeholders by declaration). No finding below
  promotes a placeholder to genuine production quality. Schema-valid or
  loader-accepted is not semantic PASS. No findings-free record by schema.

## 3. Findings (exact fields)

Severity is split: `Sev-A` = severity for integration/mechanics witness;
`Sev-B` = severity for production research quality. `Low/Medium/High` only.

### F-W1 — Weekly authored → surface preservation (lossless)

- Route: Weekly 2026-W37. Locations: authored `cover/frontmatter/final_summary`
  vs surface same objects; verified byte-object equality via read (cover==cover,
  frontmatter==frontmatter, final_summary==final_summary True).
- Observation: No authored-field loss, no rewording, no added authored claims.
  Surface adds derived `packages[0]`, `bibliography[0]`, `visible_text`,
  `issue_metadata`, `closing_synthesis` — expected pass1 expansion, not authored
  overwrite.
- Sev-A: Low (positive — renderer receives exactly the authored cover matter).
- Sev-B: n/a (preservation says nothing about research depth).

### F-W2 — Weekly draft → surface package fidelity (exact)

- Route: Weekly. Locations: surface `packages[0].headline/deck/blocks[0].text`
  vs `draft/v2/packages/pkg-001/draft-result.json` headline
  `Evidence-bound headline`, deck `The source authors report the tested method.`,
  block text `The source authors report that Target Model introduces the tested method.`
  All three equal True. `deck_attribution_mode ATTRIBUTED` carried as surface
  `attribution_mode ATTRIBUTED`; evidence ref `claim-1 / PRIMARY_SUBJECT` carried
  as surface `deck_citations` + `citations` with `discovery_id target-source`,
  key `w2026-W37target-source`.
- Chain: draft evidence card claim-1 text `Target Model introduces the tested method.`
  (`AUTHOR_CLAIM`, `source-1`), entity `target / Target Model / MODEL`,
  candidate `candidate:2026-W37:12a1f44ab9a5d18c`, discovery `target-source`
  (`https://example.invalid/target-source`). Surface citation resolves to the
  single accepted DID; bibliography has exactly that one entry.
- Sev-A: Low (internally consistent minimal chain; good for single-source render path).
- Sev-B: High-insufficient if mistaken for production (single generic claim only) —
  see F-W5/F-W6. Not a fidelity defect.

### F-W3 — Weekly bibliography author inconsistency (citation defect)

- Route: Weekly. Location: surface `bibliography[0]` =
  `{title Target Model, author Unknown, url https://example.invalid/target-source, urldate 2026-08-22}`.
- Observation: Evidence card entities declare `organization Example`
  (target) / `Other` (comparator) with `canonical_url` same invalid host, and
  evidence source `title Source`. Surface bibliography author `Unknown` does not
  match `Example`, while Special bibliography for the same `Target Model` title
  uses `author Example` (see F-S3). At least one route's author mapping is
  synthetic-fallback, and the two routes are inconsistent with each other.
  URL is non-resolvable `example.invalid` by design (synthetic), `urldate`
  `2026-08-22` matches evidence `accessed_at 2026-08-22T02:10:00+09:00` — date
  consistent, authorship is not real authority.
- Sev-A: Medium (renderer still gets a well-formed bib entry + key to typeset;
  but author-field provenance is untrustworthy — do not snapshot this mapping as
  a golden bib rule).
- Sev-B: High (no real citable authorship; `Unknown` + invalid URL = zero
  production citation authority).

### F-W4 — Weekly dates/boundary (boundary defect, minor)

- Route: Weekly. Locations: `issue_metadata {title Japanese Generative AI
  Technical Survey, display_date 2026-09-11, window_boundary "Window:
  2026-09-04 18:00 - 2026-09-11 18:00 America/New_York"}`; State history
  `DRAFT_COMPLETE recorded_at 2026-09-18T19:06:00Z` (fixture source head
  `88813a01…`); bibliography `urldate 2026-08-22`; evidence
  `observed_at 2026-08-22T02:10:00+09:00`.
- Observation: Display date (09-11) precedes DRAFT_COMPLETE (09-18) by 7 days;
  research observation (08-22) precedes window (09-04–09-11). Ordering is
  explicable for a synthetic fixture (old observation carried into later window,
  draft after window close) and State `next_action` correctly remains
  pre-validation, but a production Weekly reader would expect the window to
  contain the observation/recency justification and the display date to not
  predate completion without note. Timezone mix (NY window vs +09:00 evidence vs
  UTC history vs date-only display) is disclosed but not normalized for readers.
  `closing_synthesis` (`The accepted source authors describe the tested method.`)
  exactly repeats `final_summary.paragraphs[2]` — redundant, not contradictory.
- Sev-A: Low (no blocker to renderer witness; note for future date-line template).
- Sev-B: Medium (weak recency/boundary story; repetition reads as filler).

### F-W5 — Weekly substantive thinness (declared placeholder — judge, not invent)

- Route: Weekly. Locations: whole surface (86 lines): one package, one block,
  one claim, zero metrics, zero limitations, zero unresolved/contradictions
  (matches draft `comparison {metric 0, limitation 0, unresolved 0,
  contradiction 0}`); strapline/cover/frontmatter boilerplate
  (`Weekly tested method`, `A bounded technical survey.`, `One accepted primary
  source.`, JP strapline shared with Special).
- Observation: Content is the known generic `Target Model / tested method /
  example.invalid` placeholder. Attribution discipline is syntactically correct
  (`ATTRIBUTED`, claim-bound citations) but semantically vacuous — no method
  name, no result, no number, no limitation a reader could verify or act on.
  This is useful ONLY as a renderer shape (headline/deck/block/citation/bib
  slots, single-entry bibliography), not as survey research.
- Sev-A: Low (fit for purpose as disposable mechanics input; exercises the
  single-package Weekly path but NOT multi-source, collision, or pending-scope paths).
- Sev-B: High (fails production sufficiency/readability; MUST NOT be labelled
  Weekly quality PASS).

### F-S1 — Special authored → surface preservation (lossless, structural)

- Route: Special SP001. Locations: surface `cover/frontmatter` == authored same
  objects True; `final_summary.heading/paragraphs` == authored True (surface adds
  `placement END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER`).
  Package inner objects `theme_at_a_glance/narrative_sections/timeline/synthesis/
  reader_claim_boundary/technical_notes` each == authored `longform_revision.
  packages[0]` same key True; `cross_family_synthesis.heading/paragraphs/
  comparison_rows` == authored cross synthesis True.
- Observation: No authored longform content dropped or reworded in surface.
  Surface adds expected wrappers: `package_id/drafting_order/headline/deck/
  deck_discovery_ids/kicker` (`THEMATIC LINEAGE 1/1 — 001`), `format
  THEMATIC_FOUR_FAMILY_LINEAGE_V1`, `visible_text`, `issue_metadata`,
  `bibliography`. Headline/deck equal draft-result (`Evidence-bound headline` /
  `The source authors report the tested method.`), consistent with Weekly draft
  text but with Special `deck_discovery_ids [fixture-paper-D001]`.
- Sev-A: Low (positive — full longform shape survives to renderer).
- Sev-B: n/a.

### F-S2 — Special single-DID four-family comparison is placeholder (unbound content)

- Route: Special. Locations: surface `packages[0]` + `cross_family_synthesis.
  comparison_rows[3]` × `{dimension Fixture aspect N, glm/qwen/deepseek/kimi
  "Fixture {FAMILY}.", discovery_ids [fixture-paper-D001]}`; `packages` length 1;
  evidence basis single DID `fixture-paper-D001`
  (`https://example.invalid/papers/lineage-note-one`), single claim-1
  (`Target Model introduces the tested method.`), `metric_count 0,
  limitation_count 0`.
- Observation: Surface faithfully reproduces the authored placeholder rows
  (exact equality, so (A) passes), but semantically every family cell cites the
  SAME single DID and every cell text is identical filler differing only by
  family label. There is no per-family evidence, no lineage transition, no
  branch/transition IDs populated beyond `branch_ids [main]`, no dates in
  timeline beyond `Early/Late` labels. The `FOUR_FAMILY` format slot is
  structurally exercised yet substantively empty — a reader comparing GLM vs
  Qwen vs DeepSeek vs Kimi learns nothing. `technical_notes.primary_url` is the
  same invalid URL; chronology/points/limitation are `Fixture … for pkg-001`
  filler.
- Sev-A: Low-Medium (Low for shape witness — table renders; Medium caution —
  do NOT treat successful table render as proof that real four-family binding
  works; a real multi-DID binding path remains unexercised).
- Sev-B: High (fails production lineage sufficiency; MUST NOT be labelled
  Thematic quality PASS; cross-family synthesis as written would mislead if
  published).

### F-S3 — Special bibliography vs Weekly + chain (citation defect, shared root)

- Route: Special (contrast Weekly F-W3). Location: surface `bibliography[0]` =
  `{discovery_id fixture-paper-D001, key sp001fixturepaperd001, title Target
  Model, author Example, url https://example.invalid/papers/lineage-note-one,
  urldate 2026-08-22}`.
- Observation: Author `Example` matches evidence `organization Example` here
  (better than Weekly `Unknown`), but URL remains non-resolvable invalid host,
  title generic `Target Model`, source `published_at 2025-01-01T00:00:00Z`
  (implausible round date, synthetic), key convention differs from Weekly
  (`sp001fixturepaperd001` lower-concatenated vs `w2026-W37target-source`
  prefixed). Either key rule is fine for a disposable fixture, but the
  inconsistency means no shared bib-key invariant can be inferred. No real
  citation authority in either route.
- Sev-A: Medium (same as F-W3 — typesettable but not a golden bib rule).
- Sev-B: High (zero real authority).

### F-S4 — Special dates/boundary (consistent, still synthetic)

- Route: Special. Locations: `issue_metadata.title … Special`,
  `display_as_of 2026-08-21 17:00:00 UTC`; State history `DRAFT_COMPLETE
  2026-08-21T19:06:00Z` (2 h after as-of — coherent); evidence `observed_at /
  accessed_at 2026-08-22T02:10:00+09:00` — i.e. evidence timestamp AFTER the
  issue as-of date. Discovery `test-collector / run-001`, draft runner
  `provider fixture / model fixture-model / invocation unit-test`,
  architecture approval `reviewed_by synthetic human reviewer`,
  `review_reference synthetic LF-1 fixture architecture review`.
- Observation: As-of vs DRAFT ordering is tighter than Weekly, but evidence
  observation postdates as-of, and all upstream authorities are explicitly
  synthetic (`fixture-model`, `synthetic human reviewer`). State correctly shows
  `publication_preview pending`, `validation/freeze/release pending` — no false
  approval. For renderer witness this labelling is correct and must be preserved
  into any synthetic typed PASS; for production the as-of/evidence inversion
  and synthetic approvals are disqualifying.
- Sev-A: Low (correctly labelled synthetic; no mechanics blocker).
- Sev-B: High if misread as real (synthetic chain, inverted observation date).

### F-G1 — No unintended loss; one intended-stop confirmation

- Routes: both. Surface deltas per fixture README contain only research outputs
  (`sources/2026-W37/` or `sources/SP001/` + 9 root chain intermediates); no
  `main.tex/references.bib/jgaisurvey.sty`, no `validated-source-manifest.json`.
  This inspection confirms surfaces are pass1 reader inputs only
  (`DRAFT_COMPLETE`, no receipt). No authored paragraph missing in either
  surface (all equalities above True). Redundancy (F-W4 closing == summary para)
  and filler repetition (`Fixture … for pkg-001` × N) are verbosity, not loss.
- Sev-A: Low. Sev-B: n/a.

### F-G2 — Standalone readability (pre-TeX, JP/EN mix)

- Routes: both. `visible_text` boundaries (`Evidence / scope boundary`, `Claim
  boundary`, `Scope / attribution boundary`), kickers (`WEEKLY SYNTHESIS`,
  `CROSS-FAMILY SYNTHESIS`, `ISSUE SYNTHESIS`), section labels
  (`References / Source Notes`, `目次`, `この号の総括`/`今週の総括`,
  `週刊Technical Survey`/`Thematic Longform Special`) are present and correctly
  routed per profile. JP strapline identical in both routes; JP headings paired
  with EN body paragraphs. At surface level this is a coherent bilingual
  scaffold, but body prose is EN-only filler with no JP technical substance —
  fine for layout inspection, inadequate as a JP survey edition.
- Sev-A: Low. Sev-B: Medium-High (scaffold ok, substance absent).

## 4. Scoped verdicts (pre-TeX only — NOT production PASS, NOT build PASS)

- Weekly 2026-W37 surface `136c0dd8…48635`: (A) FIDELITY-OK for disposable
  renderer witness — authored cover matter preserved exactly, single-claim
  evidence chain internally consistent (1 DID → 1 claim → 1 bib entry, citations
  resolve). Safe to feed to pass2 mechanics AFTER this report, with F-W3/F-W4
  noted for template attention. (B) PRODUCTION NO-GO — generic placeholder,
  `Unknown` author + invalid URL, single vacuous claim, no metrics/limitations;
  explicitly NOT Weekly research quality. No semantic PASS granted.
- Special SP001 surface `f40db7f6…95cd5`: (A) FIDELITY-OK for disposable
  renderer witness — full longform shape (glance/narrative/timeline/synthesis/
  boundary/notes + cross-family table + final summary placement) preserved
  exactly from authored revision; single-DID filler consistently applied so the
  table/kicker code paths can be exercised. Safe to feed to pass2 mechanics
  AFTER this report, with F-S2/F-S3/F-S4 cautions (do not infer multi-DID
  binding from this run). (B) PRODUCTION NO-GO — one-DID placeholder masquerading
  in a four-family comparison slot; all family cells identical filler on the same
  DID; invalid URL; synthetic approvals only. Explicitly NOT Thematic/Longform
  quality. No semantic PASS granted.
- Root may use a separately labelled synthetic typed PASS only for mechanics
  witness after these findings (per selection item 5/8); this report must not be
  converted to such a PASS, and no `publication_preview` approval is supplied.

## 5. Limitations of this inspection

- Surface-only: no TeX/Bib/style mapping, PDF layout, JP typesetting,
  citation-key rendering, pagination, or visual check performed. Renderer output
  may still fail or misrender despite (A) fidelity.
- Chain sampled, not exhaustive: full screening/evidence task payloads beyond
  draft-embedded cards, checkpoint JSON bytes beyond State pointers, and
  profile/completeness ledgers were not re-read. Hash-graph continuity relies on
  fixture README pins + State provenance, not independent re-hash here except
  the six SHAs above.
- No isolation re-audit: fixture DB separation/inert-origin claims accepted as
  declared context.
- No Human, synthetic-reviewer, or QA authority granted or inferred. Both States
  correctly show `publication_preview pending`; architecture `APPROVED` entries
  are explicitly `synthetic human reviewer` test authority, not genuine review.

## 6. What root should do next (no new authority claimed)

1. Proceed to pass2 isolated disposable builds with the generated trio +
   declared recipe, keeping survey-root transfer to exactly
   `main.pdf/main.log/main.pdf.sha256` (+ packet-side Special audit JSON, not in
   survey_root) per selection items 6–7.
2. Carry F-W3/F-S3 (bib author/key inconsistency), F-W4/F-S4 (date/tz/as-of
   notes), and F-S2 (single-DID four-family placeholder) into build-review
   attention; do not bake placeholder bib/date/table behaviour into golden
   expectations.
3. Keep any schema-valid synthetic PASS explicitly labelled synthetic/test-type
   and separate from this inspection and from Human preview.
