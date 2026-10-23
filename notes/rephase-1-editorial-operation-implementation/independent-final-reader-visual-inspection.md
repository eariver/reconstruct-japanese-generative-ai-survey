# Independent final reader/visual inspection — R3 actual revised 2-route R6 second-correction PDFs

Inspector: AUTHOR-INDEPENDENT semantic/visual inspector. Not code/test/fixture
author, not Human. No code/test/build/import/Git/network executed in this unit.
Only read-only `sha256sum` / `cat` / `grep` / `ls` / `wc` hash and content reads
plus image-capability PNG reads and PDF-text reads were used.

Scope is ONLY the current R3 actual revised 2-route PDFs in
`notes/rephase-1-editorial-operation-implementation/final-r6-positives/`.
Later R7 changes only CLI/depth/test, NOT renderer/reader/style. R7 acceptance
built a different PDF (61239 B, see `correction-r7/README.md` §Final operator
acceptance). Those R7 builds are NOT claimed or inspected here.

Source epoch: `ce90246b907c86e9bdeb930dec0e83a5637f2805`,
tree `53349a4efbdd5e3b4153a8e5975101fdd59f132b` (per
`final-epoch-weekly-manifest.json`, `final-epoch-longform-manifest.json`,
`r6-handoff.json`, export `BINDING_OK ... count=720`).

## 1. Exact artifacts inspected

### 1.1 Manifests / handoff (read)

- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/final-epoch-weekly-manifest.json`
- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/final-epoch-longform-manifest.json`
- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/r6-handoff.json`
- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/inert-manifest-weekly.json`
- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/inert-manifest-longform.json`
- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/export-weekly-manual-active-stdout.txt`:
  `MANUAL_ACTIVE_PASS issue=2026-W37 ... pages=5`
- `notes/rephase-1-editorial-operation-implementation/final-r6-positives/export-longform-manual-active-stdout.txt`:
  `MANUAL_ACTIVE_PASS issue=SP001 ... pages=5`
- `notes/rephase-1-editorial-operation-implementation/correction-r7/README.md`
- `notes/rephase-1-editorial-operation-implementation/correction-r7/r7b-closeout-note.md`

### 1.2 Active fixture targets (read + rehashed, scope-honest)

Weekly active fixture root (workspace-ignored):
`.rephase-1-editorial-runtime/final-r6/weekly/`

- `sources/2026-W37/publication/v2/editorial-corrections/wk-r6-2/reader-surface-input-v2.json`
  rehashed `b13d9202d1f57a4da396eb3888ad5361099956233cc09783c5c5dca468927ad0`
  == manifest `roles_15.reader-input`. Byte count 2703 per manifest.
- `sources/2026-W37/publication/v2/editorial-corrections/wk-r6-2/staged-source/main.tex`
  rehashed `85851bc8e5300a27bddb274cdc2360db9b9a29557e70d930c5537946ecc4debe`
  == manifest `validated-source`. 1717 B per manifest.
- `sources/2026-W37/publication/v2/editorial-corrections/wk-r6-2/staged-source/references.bib`
  rehashed `faeae610e3f20e97d0c2c5e95cf25445c50e95f5020d9b2aa4efb30a96eab29b`
  == manifest `bibliography`.
- `sources/2026-W37/publication/v2/editorial-corrections/wk-r6-2/staged-source/jgaisurvey.sty`
  rehashed `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`
  == manifest `style`, == existing R2-postfix contrast-repair pin. 6569 B.
  `grep` confirms `coltitle=SurveyInk` (line ~183) and
  `\definecolor{SurveyInk}{HTML}{17202A}` (line ~29). Repair remains.
- `sources/2026-W37/publication/v2/editorial-corrections/wk-r6-2/publication/build/main.pdf`
  rehashed `308602d1b8b173d552814d604fd1dcd585b26a4521e572f30c80a32674aa4988`
  == manifest `publication-pdf`, 63397 B (`wc -c` agrees).
  `.sha256` sidecar file content is exactly that hash + newline; sidecar-file
  hash `5fe83f755bd01c8bdbdfe882fb8c382fa64826a119137c7185b7e91801c0f790`
  == manifest `pdf-digest`.
- `sources/2026-W37/publication/v2/editorial-corrections/wk-r6-2/publication/publication-candidate-v2.json`
  rehashed `1fcbfdab8c75702169b6916c19193bb982613e1ae21cb5e0077eab633fca422d`
  == manifest `candidate` == manifest `publication-candidate` ==
  `inert.sealed_candidate`. Candidate-internal `pdf.sha256` is the same
  `308602...` with `byte_count` 63397 and `page_count` 5. No stale old PDF:
  weekly inert record is `publication-surface-revalidation-r1.json`
  (`8c2d0f90...`), `r2` record absent by design (note in both manifests).

Longform active fixture root (workspace-ignored):
`.rephase-1-editorial-runtime/final-r6/longform/`

- `sources/SP001/publication/v2/editorial-corrections/lf-r6-2/reader-surface-input-v2.json`
  rehashed `50733c97c436172b5d634242ce20997602667d7d56273d202bd0a133dfe0c0c6`
  == manifest `reader-input`. 7172 B per manifest.
- `sources/SP001/publication/v2/editorial-corrections/lf-r6-2/staged-source/main.tex`
  rehashed `b7eec4baf8d7b562520442c5952c00d7ea27873d82c43a13019616de1fcd8200`
  == manifest `validated-source`. 4967 B.
- `sources/SP001/publication/v2/editorial-corrections/lf-r6-2/staged-source/references.bib`
  rehashed `cbeefa2d996b1bb2a473cd51cfad1fc9bca21f2b28a66f087405e06001831be0`
  == manifest `bibliography`.
- `sources/SP001/publication/v2/editorial-corrections/lf-r6-2/staged-source/jgaisurvey.sty`
  rehashed `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`
  == manifest `style`, identical to weekly pin. Same `coltitle=SurveyInk` repair.
- `sources/SP001/publication/v2/editorial-corrections/lf-r6-2/publication/build/main.pdf`
  rehashed `5233a47d5178efb4f3073bc2030bb5822989200a0d6c5ad3041194cbb86874d0`
  == manifest `publication-pdf`, 79757 B (`wc -c` agrees).
  `.sha256` sidecar content is exactly that hash; sidecar-file hash
  `7b0ccd7b2c8bbab5ac759b8d9d0fa158fd7a812349febdc855f95e5d9f4ba765`
  == manifest `pdf-digest`.
- `sources/SP001/publication/v2/editorial-corrections/lf-r6-2/publication/publication-candidate-v2.json`
  rehashed `a6d86e4ad7e4270266477dfd43fa3206d1856699517d49d3ea52c59cae00efe1`
  == manifest `candidate` == `publication-candidate` == `sealed_candidate`.
  Candidate-internal `pdf.sha256` is the same `5233a4...` with 79757 B, 5 pp.
  Old canonical `sources/SP001/publication/v2/publication-candidate-v2.json`
  rehashed `6e214bdcf7c09cf2d84349af7b7a293f4186ff6c3f3a981921a48bce6ed7bc93`
  == `inert.old_canonical_candidate`, distinct from sealed R6-2 candidate,
  recorded as `healthy+byte-identical+not-adopted` in `r6-handoff.json`.
  No stale-old-PDF substitution: current Candidate binds only the R6-2 PDF.

Original canonical reader/source compared (read):

- `.rephase-1-editorial-runtime/final-r6/weekly/sources/2026-W37/publication/v2/reader-surface-input-v2.json`
  `136c0dd8a2bf4c5b4323993ff3882524c760d902f2a463b93bcd6fe95a948635`
  (canonical headline `Weekly tested method`, summary `... one source.`)
- `.rephase-1-editorial-runtime/final-r6/longform/sources/SP001/publication/v2/reader-surface-input-v2.json`
  `f40db7f6f88f099e13162f51296d0b24874922d80a7ef31fd85329b85a957cd5`
  (canonical narrative-one-p1 `Fixture narrative-one paragraph one for pkg-001.`)
- `.rephase-1-editorial-runtime/final-r6/longform/sources/SP001/publication/v2/publication-candidate-v2.json`
  `6e214bdc...` (same old-canonical pin above).

Rehash scope honesty: only the PDF, reader-input, staged main/bib/style,
candidate, sidecar, and the three canonical comparison files above were
rehashed by this inspector. Manifest `sha256` values for State pointer, set,
gate, manuscript, receipt, log, regression bundle, and reviews were read but
NOT independently rehashed. No whole-history, no-cache, no-DB continuity claim.

### 1.3 PDF text (read as additional, not primary)

- `final-r6-positives/final-weekly-second-correction.txt` (74 lines)
  hash `42baa5b7678bacf939848baa16df6ed81314e29644c7f2dfb8e819b44a1518dd`
- `final-r6-positives/final-longform-second-correction.txt` (187 lines)
  hash `2083114890bbeb3de05a8b520cb742e1865822b719dc6a843409afbccd42a922`

### 1.4 Page PNGs — ALL pages actually viewed via image capability

Weekly (`final-weekly-second-correction-p1..p5.png`), 5/5 viewed:

- p1 `febab1cca3404dc3f809c1017115dc3600da13fea4a9337fd469339d9aa9187c`
- p2 `16bda7ab4f26c22c0cb50834cd01723ff7aebceed1456d1a490c98c622ea9ced`
- p3 `cefcb6da886746485ef7b21428d243e2d4c781988e18d8b782525a2f56f49c23`
- p4 `7a5af517ab62868b42310f0529cf69bee74421b0f544e92babd14f8dc6b47681`
- p5 `334ccc012cb6ac5655694680452b3337b017f0f60f203001451dc4b9172107d8`

Longform (`final-longform-second-correction-p1..p5.png`), 5/5 viewed:

- p1 `74a2167639d93d12016c3aee5db1bd96f204870f3309ac0112031a61af93f055`
- p2 `76d425517f3fe48229ffd138aa1f9e0eeb021661208cf267c6407fecc69c8ae3`
- p3 `f4d7cc03c47794817629a77b385307ed892c164fe24a45a1c8d3155cef88098b`
- p4 `4b25da01751552a38ce07fc667590634edaf28e2635b6c0a0569a5a294b992a4`
- p5 `e771bac7564552de82d5e50dfc7ec4683b8d0c6438626c72b0cfc4b4f270fb41`

No image was skipped. I can see images; this is a real visual PASS basis
(bounded), not a disclosure-of-blindness case.

## 2. Changed-content verification (exact)

### Weekly route — second correction present in reader, staged, PDF

Proposed P2 `reader-surface-input-v2.json` vs original canonical:

- `cover.headline`: `Weekly tested method` →
  `Weekly tested method — Second Editorial Correction` (exact, em-dash).
- `final_summary.paragraphs[0]`: `The edition surveys one source.` →
  `The edition surveys one source with second correction.` (exact).
- All else identical (deck, blocks, single DID `target-source`,
  bib `https://example.invalid/target-source`).

Staged `main.tex` carries both strings verbatim:

- `\surveycoverstory{Weekly tested method — Second Editorial Correction}...`
- `The edition surveys one source with second correction.`

PDF observation:

- p1 cover headline renders `Weekly tested method — Second Editorial Correction`
  across two lines, exact words, with `Source-based survey` deck and blue
  `Target Model` anchor below.
- p4 `2 今週の総括` / blue `WEEKLY SYNTHESIS` section renders all three
  paragraphs, first paragraph exactly
  `The edition surveys one source with second correction.`
- PDF text file lines 5–6 and 59 confirm the same strings. Present, no truncation.

### Longform route — second correction present in reader, staged, PDF

Proposed P2 `reader-surface-input-v2.json` vs original canonical (single delta):

- `packages[0].narrative_sections[0].paragraphs[0].text`:
  `Fixture narrative-one paragraph one for pkg-001.` →
  `Fixture narrative-one paragraph one for pkg-001. Revised fixture sentence within approved evidence. Second fixture sentence within approved evidence.`
  (exact).

Staged `main.tex` line 43 carries the full revised sentence verbatim with its
`\cite{sp001fixturepaperd001}`.

PDF observation:

- p3 left column under `Fixture narrative one for pkg-001` renders
  `Fixture narrative-one paragraph one for pkg-001. Revised fixture sentence
  within approved evidence. Second fixture sentence within approved evidence. [1]`
  (hyphenated `Re-/vised`, `Sec-/ond` only by line-breaking; words exact).
- PDF text file lines 83–87 confirm the same two added sentences. Present.

### Style repair

Both staged `jgaisurvey.sty` equal the R2-postfix pin
`035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`
with `coltitle=SurveyInk`. Visually all purple/blue box titles are white on
saturated color (weekly p2 `Evidence / scope boundary`; longform p2
`Scope / attribution boundary`, p3 `Theme at a glance`, `Claim boundary`,
p4 `Cross-family comparison`; technical-note header dark-on-light-gray).
No low-contrast regression observed.

### Old-canonical byte-immutability — test claim vs own scope (distinct)

Fixture scripts (`fixture-weekly-r6-*.py`, `fixture-longform-r6-*.py`)
assert old-immutable (`after2[rel] == sha ... drift after second activate`)
and `r6-handoff.json` records longform old-canonical as
`healthy+byte-identical+not-adopted`. That is the implementation's test claim.

My scope is distinct and narrower: I verified the old-canonical candidate hash
(`6e214bdc...`) is still the recorded pin and differs from the sealed R6-2
candidate (`a6d86e4...`), and that the current Candidate binds only the R6-2
PDF. I did NOT re-execute the immutability tests, did not snapshot
before/after trees, and make no continuous no-drift / whole-history
immutability claim.

## 3. Per-route rendered/fidelity observation

### Weekly (5 pp, 63397 B)

- p1 (cover): title, `2026-W37`, `2026-09-11`, corrected headline, deck,
  anchor, cutoff/repository/build rows, Japanese strapline
  `一次情報・論文・OSS・X上の技術反応を分離し、検証可能なEvidence chainとして編成する`
  plus `週刊Technical Survey` — all glyphs legible, no tofu, no overlap.
  Blue top rule renders.
- p2: `This week` + lede + purple `Evidence / scope boundary` box
  (`One accepted primary source.`). White-on-purple contrast good. Page number
  `2` bottom-center. Large trailing whitespace is short-fixture sparsity, not a
  defect.
- p3: `1 Evidence-bound headline`, blue `PRIMARY SOURCE` kicker, bold deck
  + `[1]`, body paragraph + `[1]`. Citations blue, on same baseline family.
  Page number `3`. Two-column source (`\twocolumn`) renders single narrow
  column because content is short — expected, not overflow.
- p4: `2 今週の総括`, blue `WEEKLY SYNTHESIS`, three synthesis paragraphs.
  Japanese heading glyphs legible. Page number `4`.
- p5: `References / Source Notes`, `[1]Unknown. Target Model. URL:
  https://example.invalid/target-source (visited on 08/22/2026).` URL blue
  mono, wraps without clipping. Page number `5`.
- Running heads `Japanese Generative AI Technical Survey / 2026-W37` on
  pp2–5, black rule, muted blue-gray text, consistent.
- Citations: every claim carries `[1]`; bib key `w2026-W37target-source`
  matches staged bib; reference entry matches reader bib fields.
- Tables/TOC: none by Weekly design. Absence is not a defect.
- Contrast/layout defects: none observed. No overfull lines spilling into
  margins, no box-text escape, no missing page numbers.

### Longform (5 pp, 79757 B)

- p1 (cover): `... Special`, `SP001`, `Thematic history / as of 2026-08-21
  17:00:00 UTC`, `Fixture lineage cover`, deck, anchor, as-of/repository/build
  rows, Japanese strapline + `Thematic Longform Special` — legible, no overlap.
- p2: `Fixture frontmatter`, lede, purple scope box, `目次` TOC with four
  entries, blue text, dot leaders, page numbers `2 / 3 / 4 / 4` which match
  actual pagination (frontmatter p2, headline p3, cross-family + synthesis p4).
  Japanese `目次` and `この号の総括` entries legible. Page number `2`.
- p3: `1 Evidence-bound headline`, blue `THEMATIC LINEAGE 1/1 — 001` kicker,
  deck + `[1]`, blue `Theme at a glance` table (Focus/Signal rows, `[1]` blue),
  two-column narrative (both narrative sections with all `[1]`), timeline
  table (Early/Late), synthesis (two paragraphs, second paragraph wraps to
  right column — balanced-columns artifact, not loss), purple `Claim boundary`
  box, `Source-backed Technical Notes` gray-header box with Chronology /
  Technical points bullets / Limitation / blue Primary URL
  `https://example.invalid/papers/lineage-note-one`. All observed legible;
  no cell overflow, no text outside boxes. Page number `3`.
- p4: `2 Fixture cross-family synthesis`, blue kicker, two cross paragraphs
  + `[1]`, blue `Cross-family comparison` table with header
  `観点 | GLM | Qwen | DeepSeek | Kimi` (Japanese `観点` legible), three aspect
  rows each with `Fixture ...` + `[1]` in Kimi column, rules top/mid/bottom
  intact, `scriptsize` fits linewidth without clipping. Then
  `3 この号の総括` / blue `ISSUE SYNTHESIS` with three paragraphs in balanced
  two columns. PDF-text linearisation order (surveys, synthesis-stays, claims)
  differs from source order (surveys, claims, synthesis-stays) only because of
  `multicols` column-major extraction; visually each sentence is present in
  its column. Not a content defect. Page number `4`.
- p5: `References / Source Notes`,
  `[1]Example. Target Model. URL: https://example.invalid/papers/lineage-note-one
  (visited on 08/22/2026).` Blue URL, no clipping. Page number `5`.
- Running heads `... Special / SP001` on pp2–5, consistent.
- Citations: `[1]` on deck, every glance/narrative/timeline/synthesis/boundary/
  note/cross/table cell; bib key `sp001fixturepaperd001` matches staged bib.
- Final summary (`この号の総括`, three paragraphs) present on p4 before
  references, per `placement: END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER`.
- Contrast/layout defects: none observed. No missing glyphs, no table overflow,
  no TOC mismatch, no orphaned header without body.

### Concrete renderer finding

No actual renderer defect found in the inspected R6 second-correction PDFs.
Sparse whitespace (weekly pp2–5, longform p5) and the 5-page length for a
single-package fixture are consequences of the short representative fixture
(single DID, minimal prose), already flagged as below-target density in the
synthetic longform review (`density-review:below-target-substantive`,
`page-plan:5/12`). I do NOT mandate any global pagination rewrite, page-count
target, or layout rebalancing on that basis alone. Any future full-length
edition needs its own visual proof.

## 4. Production-research verdict vs rendered/fidelity verdict (kept distinct)

- Production research: NO-GO (both routes, unchanged by correction). Reasons
  actually observed in reader + staged + PDF: single accepted primary source
  per edition/route (`target-source` / `fixture-paper-D001`); placeholder
  prose (`tested method`, `Target Model`, `Fixture ... for pkg-001`);
  authors `Unknown` / `Example`; URLs under `example.invalid`
  (`https://example.invalid/target-source`,
  `https://example.invalid/papers/lineage-note-one`) which are non-resolvable
  by TLD; visited date `08/22/2026` on synthetic fixture. The correction adds
  only the approved headline/summary/narrative sentences above — no new source,
  no real evidence chain. Not publishable as real research.
- Rendered/fidelity: bounded PASS (both routes). The exact P2 correction
  strings propagate losslessly reader-surface-input → staged main.tex →
  built PDF text + PNG pixels; bib keys/fields match citations; style pin
  unchanged with contrast repair intact; Candidate binds exactly the hashed
  current PDF with matching page counts; no stale old PDF.
- The fidelity PASS does not cure the research NO-GO, and the research NO-GO
  does not refute the fidelity PASS.

## 5. Synthetic/external reviews — not converted

Existing post-review fixtures use `review_kind: SEMANTIC_EDITORIAL` and
`VISUAL` with synthetic type-actors:

- weekly `external-reviews/semantic-review-v2.json` (`reviewed_by: r6 synthetic
  SEMANTIC_EDITORIAL reviewer`), `external-reviews/visual-review-v2.json`
  (`reviewed_by: r6 synthetic VISUAL reviewer`);
- longform `publication/semantic-review-v2.json`
  (`reviewed_by: r6 synthetic LF SEMANTIC_EDITORIAL reviewer`),
  `publication/visual-review-v2.json`
  (`reviewed_by: r6 synthetic LF VISUAL reviewer`);
- every check `detail` states `no genuine Human approval` / `no genuine approval`.

Those synthetic PASSES are fixture mechanics, not real semantic, visual, or
Human approval. This document is the separate real author-independent
inspection judgment described above, and it converts nothing into Human
approval, production acceptance, audit PASS, or adoption authority.

## 6. Limits

- Representative length: single-package, single-DID fixture (weekly reader
  2703 B, longform 7172 B; staged 1717 / 4967 B). Findings do not generalise to
  full-length multi-source editions, real pagination balance, or print proofing.
- Screens only: PNGs viewed at supplied resolution; qualitative contrast
  judgment only (no colorimeter, no WCAG ratio measurement); Japanese legibility
  means no tofu/mojibake/overlap at screen scale, not font-shaping certification.
- Text aid: PDF-text files used only to confirm strings; visual truth is the PNGs.
- No TeX-log audit, no build reproduction, no registry/Profile/DID resolution,
  no URL fetching (`.invalid` judged by TLD, not dialed), no R7 PDFs inspected.
- Read-only hashes cover only §1.2 targets; all other manifest pins taken as
  read. No continuous-drift, no-CAS, no-crash, no-migration claim.
- No overall R3 implementation PASS, no audit PASS, no adoption/operation PASS.
  This is a bounded reader/visual inspection only.
