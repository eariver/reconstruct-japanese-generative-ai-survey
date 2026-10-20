# Independent postbuild semantic + visual inspection — initial real-build integration

Role: AUTHOR-INDEPENDENT postbuild semantic/visual reviewer. Not the
fixture/code/build author, not Astra/root, not seven-point auditor, not Human
Gate. No code, fixture, build, network, Git mutation, review JSON, or Human
blessing produced here. Dedicated `Write` used once for this file only (parent
`ls` already shown by task context; no other writes).

Date (UTC): 2026-10-19. Inspection of real LuaLaTeX PDFs after build; pre-TeX
report is preserved, not superseded on semantics.

## 1. Read scope (exact, read-only)

Pins from packet (accepted as build claims, hashes re-verified here where stated):

- `notes/rephase-1-initial-build-integration/builds-20261019T134223Z/README.md` (146 lines) — full mechanical witness context.
- `builds-20261019T134223Z/final-report-attempt5.json` — Weekly `88813a01…`, Special `d4078d1b…`; both BUILT exit 0 (31.4 s / 24.5 s), LuaHBTeX 1.24.0 / latexmk 4.88 / biber 2.22 (TL2026), epochs 1792416843 / 1792416844; log_gate PASS 0 blocking, 5 pp each; receipt PASS 8.6 s / 8.9 s; blockers [].
- `notes/rephase-1-initial-build-integration/independent-pretex-inspection.md` (pre-TeX fidelity-OK / production NO-GO both routes) and `notes/rephase-1-initial-build-integration/astra-pretex-build-selection.md` (18 lines, proceed on synthetic inputs, synthetic type-only PASS only, production NO-GO retained).
- Reader surfaces re-read this inspection (same bytes as pre-TeX pins `136c0dd8…8635` Weekly 2648 B, `f40db7f6…95cd5` Special 7071 B):
  `/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture/sources/2026-W37/publication/v2/reader-surface-input-v2.json` (86 lines),
  `…/special-fixture/sources/SP001/publication/v2/reader-surface-input-v2.json` (244 lines).
- Generated trio re-read:
  `…/weekly-fixture/surveys/weekly/2026-W37/main.tex` (41 lines),
  `…/special-fixture/surveys/special/SP001/main.tex` (109 lines),
  both `references.bib` (6 lines each). Style `jgaisurvey.sty` not re-read (toolchain resolution already evidenced by successful build; visual output is the check here).
- Build outputs inspected:
  `weekly-main-attempt5.pdf` / `special-main-attempt5.pdf`,
  `weekly/special-extracted-attempt5.txt` (pdftotext `-layout` packet outputs),
  `weekly/special-pdfinfo-stdout-attempt5.txt`, `logcheck-results-attempt4.json`
  (both `PASS`, `blocking_n 0`), attempt5 `main.log` files (grep for blocking patterns only, no execution).

Visual method (actual image inspection, NOT text-only):
all 10 PNGs viewed via image-read capability —
`weekly-page-1..5.png`, `special-page-1..5.png` (packet 150 dpi `pdftoppm`
raster). No visual claim is made from extracted text alone.

Hash verification by execution of read-only `sha256sum` (no build/test run):
- weekly PDF `7230540ec22a3dac1cdb48fd0f28b0925af4207609d3848a236ffaaf937774c4` 61151 B — matches `final-report-attempt5.json` and `weekly-main-attempt5.pdf.sha256` (`7230540e…  main.pdf`).
- special PDF `e181c19ab2ee09a4d6a4e3241f30aa4b83e3b3ae03283526dcbb3a477a1e388d` 79128 B — matches report + digest file.
- logs: weekly `5fe33a8f…`, special `d3710b68…` (recorded; not gate inputs).
- `pdfinfo`: both 5 pages, A4 (595.276×841.89 pt), LuaLaTeX/LuaTeX-1.24.0, PDF 1.7, unencrypted.
- Log grep (`Missing character|Overfull|Underfull|undefined|There were undefined`) on both attempt5 logs: only 2 `Font Info: Kanji font shape … undefined` lines per file (italic/small-caps fallback info, not a workflow blocking pattern); zero `Missing character`, zero over/underfull, zero undefined citations. Consistent with packet log-gate PASS; this grep is inspection only.

NOT read: full screening/evidence chains beyond draft-embedded cards, profile ledgers, TeX style internals, QA/Candidate/State (not built per STOP). No network, no source writes, no test execution.

## 2. Verdict (scoped)

- **Render fidelity for disposable mechanics witness: PASS (with layout defects noted).** Every reader-surface string checked renders with no loss, no tofu, no `[?]` undefined citation, correct single-entry bibliography order, correct headers/footers/page numbers, accurate Special TOC page numbers. Japanese headings/strapline/table header all glyph-complete (HaranoAji/Japanese stack works).
- **Production semantic: NO-GO for BOTH routes (retained from pre-TeX, confirmed visually).** Placeholders (`Target Model`, `tested method`, `Fixture … for pkg-001`), single-DID chains, `example.invalid` URLs, `Unknown`/`Example` authors, zero metrics/limitations. Render success does not promote any of this to research quality. No synthetic type PASS or Human approval is blessed here.
- **Layout/pagination: NOT production-ready.** Both editions are 5 pages by forced breaks, not by content volume. Weekly pp 2–5 each carry <10 lines with >70% whitespace; Special pp 2/4/5 similarly sparse with one dense p 3. Plus one contrast defect and two column/table placement awkwardnesses below. These are real rendering/template defects exposed by this task — not an assumed PASS.

## 3. Page-specific visual findings

Severity: `Sev-R` = renderer/mechanics severity; `Sev-P` = production-research severity. All pages A4, running header from p 2 onward, centered footer page number (cover p 1 has neither — expected cover treatment).

### Weekly 2026-W37 (surface `136c0dd8…`, trio + bib as above)

- **W-p1 (cover).** Title/issue `2026-W37`/date `2026-09-11`/headline `Weekly tested method`/deck/anchor `Target Model`/cutoff `Window: 2026-09-04 18:00 - 2026-09-11 18:00 America/New_York`/repo/build rows/JP strapline all present and ordered as surface + `main.tex` `\surveysetup/coverstory`. JP strapline renders fully, no tofu. Blue top rule renders. Middle ~60% of page is empty whitespace. Cutoff underscore renders literally (`New_York`) — matches escaped TeX source, correct. Sev-R: Low (correct) + inflation note (see W-p2–p5). Sev-P: High-NO-GO (placeholder headline/deck).
- **W-p2 (frontmatter `This week`).** Header `Japanese Generative AI Technical Survey — 2026-W37` + footer `2` correct. Lede `A bounded technical survey.` + purple `Evidence / scope boundary` box with `One accepted primary source.` — matches surface `frontmatter` + `visible_text.frontmatter_boundary`. Box renders with filled header, rounded body. Remainder ~75% empty (forced `\clearpage` before and after). Sev-R: Low fidelity, Medium inflation (template forces a near-empty page per section). Sev-P: n/a (scaffold ok, substance absent per pre-TeX F-W5).
- **W-p3 (§1 `Evidence-bound headline`).** Kicker `PRIMARY SOURCE` blue, deck bold + blue `[1]`, block paragraph with hyphenated `intro-duces` (hyphenation active) + blue `[1]`. Matches surface package + deck/block citations `w2026-W37target-source`. `\twocolumn` in effect: text occupies left column only, right column entirely empty; page ~80% empty. No table to check on this route. Sev-R: Low fidelity (citations resolve, order kept), Medium layout (unbalanced two-column + clearpage inflates; with real multi-paragraph content this fills, but single-package short content exposes the waste). Sev-P: High-NO-GO (single vacuous claim, pre-Tex F-W5).
- **W-p4 (§2 `今週の総括`).** JP section heading renders (no tofu), kicker `WEEKLY SYNTHESIS` blue, 3 paragraphs exactly as surface `final_summary.paragraphs`. Page ~85% empty. Sev-R: Low (JP heading proves font path), Medium inflation. Sev-P: Medium-High (redundant closing line noted pre-TeX F-W4; filler prose).
- **W-p5 (`References / Source Notes`).** Single `[1] Unknown. Target Model. URL: https://example.invalid/target-source (visited on 08/22/2026).` URL blue monospace, wraps without overflow. No `[?]`. Order trivially correct. Bib date renders US `08/22/2026` from ISO `urldate 2026-08-22` — bib-style localization, note for JP production (Sev-R Low). Author `Unknown` matches surface (fidelity OK, authority zero — pre-TeX F-W3). Page ~85% empty. Sev-R: Low. Sev-P: High-NO-GO (invalid URL, no authorship).

### Special SP001 (surface `f40db7f6…`, trio + bib as above)

- **S-p1 (cover).** Title wraps `… Survey / Special`, `SP001`, `Thematic history / as of 2026-08-21 17:00:00 UTC`, headline `Fixture lineage cover`, same repo/build rows, JP strapline with `Thematic Longform Special` descriptor — all match surface cover + `\surveysetup`. JP renders, no tofu. Same large mid-page whitespace as Weekly. Sev-R: Low. Sev-P: High-NO-GO (fixture cover).
- **S-p2 (frontmatter + `目次`).** Heading `Fixture frontmatter`, lede, purple `Scope / attribution boundary` box — correct. TOC `目次` with dot leaders and blue entries: frontmatter ..2, §1 ..3, §2 ..4, §3 ..4. Verified against actual pagination (frontmatter here p 2, §1 p 3, §2+§3 both start p 4) — ACCURATE. JP TOC title and §3 entry `この号の総括` render. Header `… Special — SP001` + footer `2`. Lower ~55% empty. Sev-R: Low (TOC engine + JP both work). Sev-P: n/a scaffold.
- **S-p3 (§1 dense package).** Kicker `THEMATIC LINEAGE 1/1 — 001`, deck + `[1]`; blue `Theme at a glance` box with `Focus/Signal` tabular rows + `[1]` each; two-column `multicols` narratives left/right correctly paired; `Transition timeline` table (`Early/Late`); synthesis `multicols` — heading `Fixture synthesis for pkg-001` sits in LEFT column only while `paragraph two` starts at top of RIGHT column (heading confinement artifact — visually awkward, see §4 blocker 3); purple `Claim boundary` box; `Source-backed Technical Notes` gray-header box: header text `Fixture note for pkg-001` is WHITE on LIGHT GRAY, barely readable in raster (contrast defect, see §4 blocker 2). Chronology/points/limitation labels bold; bullets render; `Primary URL: https://example.invalid/papers/lineage-note-one` blue mono, fits line. Every prose unit carries blue `[1]` matching single-DID surface; citation mechanics correct. Tables have `booktabs` rules, no overflow/clipping at 150 dpi. Sev-R: Low fidelity, Medium layout (contrast + heading-column artifacts). Sev-P: High-NO-GO (single-DID filler in every cell, pre-TeX F-S2).
- **S-p4 (§2 cross-family + §3 summary).** `CROSS-FAMILY SYNTHESIS` + 2 paragraphs + blue `Cross-family comparison` box: 5-col table (`観点/GLM/Qwen/DeepSeek/Kimi` header JP renders), `Fixture aspect 1/2/3` rows, `\scriptsize` fits width, `\toprule/\midrule/\bottomrule` present, no cell overflow. Citation `[1]` appears ONLY in `Kimi` column per row — faithful to `main.tex` (single `\cite` after last cell), but visually implies only Kimi is sourced (see §4 blocker 4). §3 `この号の総括` + `ISSUE SYNTHESIS`, 3 paragraphs in `multicols{2}` split 2-left/1-right, lower ~60% empty. Sev-R: Low fidelity (table engine works), Low-Medium placement (row-cite). Sev-P: High-NO-GO (identical filler per family on same DID would mislead if published — pre-TeX F-S2).
- **S-p5 (References).** Single `[1] Example. Target Model. URL: https://example.invalid/papers/lineage-note-one (visited on 08/22/2026).` — matches bib (`Example` here vs Weekly `Unknown` for same `Target Model` title — inconsistency preserved from surfaces, pre-TeX F-S3/F-W3). Resolves, no overflow. Page ~85% empty. Sev-R: Low. Sev-P: High-NO-GO (invalid URL, round `2025-01-01` source date per pre-TeX chain).

Headers/footers/cutoffs: running headers correct on pp 2–5 both routes (Weekly `… 2026-W37`, Special `… Special SP001`); footers centered page numbers 2–5; cover has none. Cutoff blocks match surfaces verbatim (Weekly window string, Special as-of string). No truncated text, no overprint, no missing glyph boxes observed at 150 dpi on any of the 10 pages.

## 4. Actionable rendering blockers vs fixture-quality limitations

**Blockers (template/generator/style — fix even before real content; do NOT fix by hand-editing generated TeX in a witness):**

1. **Forced-break page inflation (both, High for production, Medium for witness).** `main.tex` issues `\clearpage` after cover, after every section, and toggles `\twocolumn/\onecolumn`; with tiny fixture inputs this yields 5 pages of mostly whitespace (Weekly pp 2–5, Special pp 2/4/5). Build succeeds and log gate passes, so mechanics witness stands — but no production edition can ship one paragraph per page. Root fix: continuous-flow layout with keep-together/`Needspace` only where needed, balanced columns or single-column default for short sections; re-measure pages-per-content on a real-length input.
2. **Technical-note header contrast (S-p3, Medium).** White title on light-gray header fails readability in raster and likely WCAG contrast. Style fix in `jgaisurvey.sty` (`technicalnote` header colors), independent of content.
3. **Multicol heading confinement (S-p3 synthesis, Low-Medium).** `\subsection*` inside `multicols` strands the heading in column 1 while body flows to column 2. Move section headings outside `multicols` or use spanning constructs; will recur with real two-column syntheses.
4. **Row-level citation placed in last cell only (S-p4 table, Low render / Medium generator rule).** Renderer is faithful, but a reader infers only `Kimi` is cited. Generator should emit per-cell cites or a row-note cite when all cells share one DID, and per-cell DIDs when real multi-source binding lands (pre-TeX F-S2 caution: do not infer multi-DID binding works from this run).
5. **Weekly `\twocolumn` single-short-package orphan (W-p3, Low-Medium, same root as 1).** Left-column-only fill with empty right column. Same continuous-flow/balancing fix as 1.
6. **Bibliography date localization (both p 5, Low).** ISO `urldate` renders US `MM/DD/YYYY`; JP production needs an explicit locale decision (and JP `visited on` wording if the edition is JP-facing).

**Fixture-quality limitations (NOT renderer defects; renderer correctly reproduces them — do not bake into golden expectations):**

- Thin/vacuous placeholder prose, single claim/DID per route, identical `Fixture {FAMILY}.` cells, `example.invalid` URLs, `Unknown` vs `Example` author inconsistency, `08/22/2026` vs evidence `+09:00` timezone mix, as-of/observation inversion, redundant closing synthesis — all already judged production NO-GO in `independent-pretex-inspection.md` F-W3–W5/F-S2–S4/F-G2. No layout fix cures them; only real research does.
- Single-entry bibliography order is trivially correct here; multi-entry sorting/collision behavior remains unexercised. TOC accuracy here does not prove long-edition TOC robustness.

## 5. Limitations of this postbuild inspection

- Raster is packet 150 dpi PNG via `pdftoppm`; sub-pixel kerning/microtype and print-color fidelity not judged. PDF text extraction compared for completeness only; visual judgment comes from the 10 PNG views above.
- Log judgment is workflow-gate-scoped (blocking-pattern grep + packet `logcheck-results-attempt4.json`); full `main.log` warning taxonomy not audited.
- No QA/Candidate/State, no multi-source/pending-scope paths, no Windows/real-actions variance, no print proof. Isolation/DB claims accepted from packet context, not re-audited.
- This report grants no semantic PASS, no type PASS, no Human approval, and no reviewer identity to any synthetic record. Production NO-GO findings from the pre-TeX report are retained in full.

## 6. Recommendation to root

Keep both PDFs as disposable renderer evidence only. Route the six blockers (especially 1–2) into the R2 template/generator fix list with a real-length content re-measure before any publication QA; carry all pre-TeX production NO-GO findings unchanged into the R2 disposition. Do not promote either PDF, either digest, or any synthetic review into Candidate/State or Human adoption.
