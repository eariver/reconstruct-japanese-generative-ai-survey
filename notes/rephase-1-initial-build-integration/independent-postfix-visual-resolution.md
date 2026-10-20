# Post-fix visual resolution — selected technicalnote contrast only

Role: AUTHOR-INDEPENDENT post-fix visual reviewer (same inspector as
`independent-postbuild-inspection.md`; did not write the fix, did not run
builds/tests, no code/test/Git writes, no network). Original postbuild report
is RETAINED unedited; this file resolves ONLY the disposition-selected
contrast finding. Dedicated `Write` used once for this file only.

Date (UTC): 2026-10-19. Disposition read: `astra-postbuild-disposition.md`
(items 1–5): SELECT FIX was ONLY `coltitle=SurveyInk` on the shared
`technicalnote` style; pagination rewrite DEFERRED pending representative
content; citation/locale RETAINED; production NO-GO both routes UNCHANGED;
synthetic lifecycle wiring is type/authority only, never genuine approval.

## 1. Actual viewed scope (read-only, no execution)

- Disposition: `astra-postbuild-disposition.md` (21 lines).
- Fix record (read, style bytes NOT rehashed — recorded pins accepted as scope):
  `style-correction/README.md` (before sha `3b6d1562…`, 6547 B; after
  `035645ca…6569`, 6569 B), `style-correction/style-coltitle-fix.patch`
  (one line `coltitle=SurveyInk`, background/frame/layout untouched),
  `style-correction/final22-manifest.json` (not re-opened).
- Final22 packet: `final22-integration-20261019T135318Z/README.md` (positive
  74 ops, 5 pp both routes, QA genuine / synthetic reviews labelled,
  negatives 25 + preemptions, surface bytes identical both routes).
- Harness-level pins read (not re-derived): weekly PDF `899f0f2a…` 61151 B,
  special PDF `71a2c98a…` 79156 B; pdfinfo both 5 pp A4 LuaTeX-1.24.0.
- PDFs REHASHED this inspection via read-only `sha256sum`:
  `weekly-main.pdf` = `899f0f2a405bfeedd057debaec55e76a084940a9a1eaa92b8de84bf3cbd97563`,
  `special-main-attempt6.pdf` = `71a2c98ac3ff3542a820bd535940e9e71b56491536348bf159ae8acfbdb90c3b` —
  both match recorded digest files / positive reports.
- Images VIEWED via image-read capability (10/10, not text-only):
  `weekly-page-1..5.png`, `special-page-attempt6-1..5.png` (150 dpi packet rasters).
- Baseline comparator (previously inspected): `builds-20261019T134223Z/special-page-3.png`
  (white-on-light-gray technicalnote title, barely readable).
- Text completeness cross-check: `special-extracted-attempt6.txt` /
  `weekly-extracted.txt` (all paragraphs/boundaries/citations/URLs present;
  no line relied on for the contrast judgment alone).

## 2. Selected finding — RESOLVED

- **Contrast (Special p3 `technicalnote` title): FIXED.**
  New `special-page-attempt6-3.png`: header `Fixture note for pkg-001`
  renders in DARK ink on the SAME light-gray background — fully legible at
  150 dpi. Baseline p3 showed near-invisible white-on-light-gray for the
  identical string. No other box altered: blue `Theme at a glance` header
  stays white-on-blue, purple `Claim boundary` / scope boxes stay
  white-on-purple, body text/frames identical. No text lost:
  Chronology / Technical points / Limitation / Primary URL rows all present
  with identical wording and `[1]` placement; extracted text matches baseline
  ordering. No layout shift: surrounding `Claim boundary` box, section
  heading, timeline table, and page break positions visually unchanged;
  page count stays 5 (weekly) / 5 (special) per pdfinfo and raster count;
  headers/footers/page numbers, TOC p2 (2/3/4/4), Japanese glyphs
  (`目次`, `この号の総括`, `観点`, straplines) all render with no tofu.
  Weekly pages 1–5 show no style side effects (shared style affects only the
  technicalnote title path, which Weekly does not use).
- Scope of this PASS: the single `coltitle` contrast defect is closed.
  Nothing else in the original report is closed by this file.

## 3. Explicit non-resolutions (remain OPEN per disposition)

- Production semantic NO-GO both routes UNCHANGED (placeholder prose,
  single-DID chains, `example.invalid` URLs, `Unknown`/`Example` authors,
  zero metrics). New renders reproduce the same synthetic content
  byte-identically per packet surface-compare — correctly, as fixtures.
- Pagination/real-length limits UNCHANGED: sparse-fixture 5 pp observation
  stands, but disposition defers any general layout rewrite until
  representative long-form content is measured.
- Correction to my original report: the phrase implying Longform breaks
  "after every section" was TOO BROAD. Root actual source read (accepted):
  Longform `main.tex` has explicit breaks at cover/frontmatter/references,
  not after every section; synthesis-inside-multicols awkwardness is
  recorded flow behavior, not an established faulty-authority contract.
- Citation placement (row-cite in last cell) and bibliography locale
  (US `MM/DD/YYYY`) are RETAINED open items per disposition; no judgment
  made here beyond confirming they render exactly as before.
- Lifecycle records in final22 (synthetic Preview approval, Candidate/
  Freeze/RELEASED via actual APIs on synthetic fixtures) are
  TYPE/AUTHORITY-wiring evidence only. This resolution does NOT convert any
  synthetic PASS into real semantic review, Human approval, or publication
  readiness. No QA/Candidate/State/production adoption is granted.

## 4. Verdict

Selected contrast blocker RESOLVED and visually verified on the real
final22 PDFs (10/10 pages viewed, both PDFs rehashed matching). All other
postbuild findings, production NO-GO judgments, and real-length layout
validation remain OPEN and are NOT closed by this fix.
