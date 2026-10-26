# Independent reader/PDF sanity review — versioned renewal (scoped, not whole-unit acceptance)

Fresh INDEPENDENT reader, not author of implementation or fixtures. No Production / genuine approval. Whole unit: versioned renewal, Human `f84fcf5`. This is a scoped fidelity/visual sanity inspection of actual rendered PDFs + source reading for both routes final C and renewal→editorial sample, not schema-PASS-only. No new Human Gate, no genuine PASS producer, no whole-unit acceptance.

Read first:

- `outputs/rephase-1-versioned-renewal-contract-decision.md` (contract `478f0051` incl §11, unchanged) + `notes/rephase-1-versioned-renewal-contract/astra-review-resolution.md` + both independent design reviews with final-binding addenda.
- `outputs/rephase-1-versioned-renewal-precode-assessment.md` + `notes/rephase-1-versioned-renewal-precode/astra-precode-gate-resolution.md` incl §6 (strict LIVE `agent.validate_agent_state`, schema pointer `""`) + `independent-readiness-review.md` with Final-binding ROOT resolution + pointer-erratum confirmation.
- Implementation notes: `resume-20261025/weekly-integration/result-matrix.md` + `continuation-result-matrix.md`, `resume-20261025/longform-integration/README.md`, `resume-20261025/weekly-final-editorial/manifest.json` + `ed-final-20261025T235500Z/`, `resume-20261025/editorial-archive-correction/README.md` + `worklog-append-20261025T133000Z.md` + `run-lf4-closure-20261025T120000Z/` (LF clean closure `exit.txt 0`, supersedes timeout-qualified FULL; Weekly pending separate).

## 1. Selected samples — why these cover new operation vs old baseline

- **Weekly C (new rendered targets):** `high-c1-weekly` proves C under genuine changed-tool epoch G2 (style+Core comment) with real TL2026 build, `NEW_TARGETS`/`EXECUTED_BUILD`, trio SHA-changed vs old R3 baseline. Old baseline per `weekly-integration/setup/.../e-hash-boot.txt`: `.../wk-boot-1/publication/build/main.pdf` `0684697f7043...` (real 5-page PDF, r1 `65246288...`). C PDF is different SHA, same 5p/61239B coincidence, changed style `a4bd...` vs old `035645...`, primary `1e3b22...` same, bib same — actual changed trio, not same-trio metadata.
- **Longform C:** `high-c1-longform` same argument vs old R3 baseline `.../lf-boot-1/publication/build/main.pdf` `12e2bdfb0aab...` 79530B 5p (`longform-integration/README.md` §1). C PDF `4ce0495c...` 79530B 5p, new R path, `NEW_TARGETS`, style `b1cbbdd...`.
- **Weekly renewal→editorial sample:** `wk-ed-final-1` (`weekly-final-editorial`) proves renewal→editorial after U with changed reader (new headline + 3 paras incl preserved synthesis), real TL2026 build, P1/P2R/scope/P2V/P3S63, `EDITORIAL_PUBLICATION_SOURCE_V1/WEEKLY_GENERATED_V2`, finalize seal + activate r3. Covers editorial delta vs both old baseline and C.
- **Longform renewal→editorial sample:** `lf-ed-4` (`editorial-archive-correction`) proves renewal→editorial after U5 archive-correction with new reader (G7 changed deck + narrative + synthesis), OWN `survey_editorial_publication_v2.py` fix, P1/P2R/P2V/P3S63, real build/postrender QA+reviews, finalize seal + activate r9 + clean `ALREADY_ACTIVE` closure rc0. Covers editorial delta vs C and vs old baseline.

U reuse is NOT visually re-proven here: U sets write no duplicate trio/manuscript/PDF/log/reviews by contract; implementation evidence records byte-identical reuse (e.g. Weekly U3 `old C targets unchanged True`, 6 files SHA equal; Longform U2/U3b lineage). Taken as observed manifest checks, not true Human reuse approval, not a visual PASS.

## 2. Exact identities (read-only verified)

All `sha256sum` + `pdfinfo` + `pypdf` read-only; no PDF/source modification.

| Sample | Exact PDF path (fixture-local, repo-relative under fixture root) | SHA256 | Bytes | Pages | staged `main.tex` SHA / bytes | bib / style SHA |
|---|---|---|---|---|---|---|
| Weekly C | `.rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/build/main.pdf` | `8fb8aca78a28fb2dc12c54b0cb2609a0d3d4575d09fb5e3a2d064cfc3133dc43` | 61239 | 5 (A4, LuaLaTeX/LuaTeX-1.24.0, Creation Sun Oct 25 14:28:45 2026 JST) | `1e3b22a5d1613...` 1679B | bib `faeae610...` 160B / style `a4bd135a...` 6654B (G2 variant) |
| LF C | `.rephase-1-editorial-runtime/versioned-renewal-longform-20261025T060000Z/renewal-longform/sources/SP001/publication/v2/editorial-corrections/lf-boot-1/renewals/high-c1-longform/build/main.pdf` | `4ce0495c96c995cef4d637d189addddb287bc9898d9518c3fe7403eef21ae39a` | 79530 | 5 (A4, LuaLaTeX/LuaTeX-1.24.0, Creation Sun Oct 25 14:28:58 2026 JST) | `c1da86fc22c7...` 4917B | bib `cbeefa2d...` 169B / style `b1cbbdd9...` 6652B |
| Weekly ED final | `.rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z/renewal-weekly-final/sources/2026-W37/publication/v2/editorial-corrections/wk-ed-final-1/publication/build/main.pdf` | `1c396fac340487c01c69a4fdec9b749be06e34d32ca073a571bc05e1ae325d5f` | 63204 | 5 (A4, LuaLaTeX/LuaTeX-1.24.0, Creation Mon Oct 26 03:18:19 2026 JST) | `e2ed372969ae...` 1836B | bib `faeae610...` 160B / style `035645ca...` 6569B (shipping) |
| LF ED4 | `.rephase-1-editorial-runtime/versioned-renewal-editorial-archive-longform-20261025T100000Z/renewal-longform/sources/SP001/publication/v2/editorial-corrections/lf-ed-4/publication/build/main.pdf` | `c3b6992b2b320e4c52bd04c47919e286a2dae2a740c41afa9ff18004912407bf` | 82921 | 5 (A4, LuaLaTeX/LuaTeX-1.24.0, Creation Sun Oct 25 20:16:36 2026 JST) | `dad9c3b76878...` 5221B | bib `cbeefa2d...` 169B / style `b1cbbdd9...` 6652B |

Tool/source epoch (recorded, not re-derived):

- Weekly C: fixture `versioned-renewal-weekly-20261025T052132Z`, G2 `cec67e5` (style+Core comment), HIGH `9a0469ef...` unchanged, TeX Live 2026 `/tmp/opencode/jgas-texlive-20261019T133205Z`, recipe `.latexmkrc` `18199fd8...`, `EXECUTED_BUILD` disposable `mkdtemp`, 4 cmds, build-record `VERSIONED_RENEWAL_BUILD_V1`.
- LF C: fixture `versioned-renewal-longform-20261025T060000Z`, G2 `5740d67` (style+Core comment), HIGH stable, same TeX Live/recipe, `EXECUTED_BUILD`.
- Weekly ED: fixture `versioned-renewal-weekly-final-20261025T235500Z`, G1 `a8652fda...` (base `721a04d`, overlay 741 files, pins H `74275d22...`/P1 `825dba1d...`/PUB `3f4039fd...`/Reader `098a2c82...`/style `035645ca...`), build-record `EDITORIAL_PUBLICATION_BUILD_V1`, log 92973B, receipt `EDITORIAL_PUBLICATION_SOURCE_V1/WEEKLY_GENERATED_V2`.
- LF ED4: fixture `versioned-renewal-editorial-archive-longform-20261025T100000Z`, FIXED739 + OWN patch `survey_editorial_publication_v2.py` `85814124...` + new test `5e5a0bdc...` (5/5 OK), pins H `6fe86e78...`/P1 `825dba1d...`/PUB `3f4039fd...`/HIGH `9a0469ef...`/Reader `098a2c82...`, closure 63, build-record `EDITORIAL_PUBLICATION_BUILD_V1`, log 94158B, receipt `EDITORIAL_PUBLICATION_SOURCE_V1/LONGFORM_GENERATED_V1`.

Reader IR / manuscript refs (exact, read-only `reader-manuscript-v2.json`):

- Weekly C: manuscript binds staged `main.tex` `1e3b22a5...`, bib/style above, `renewal_source.proof  bd2e39a4...`, `authored_by bootstrap weekly manuscript author`.
- LF C: manuscript binds staged `main.tex` `c1da86fc...`, `renewal_source.proof 4b39f628...`, `authored_by bootstrap longform manuscript author`.
- Weekly ED: manuscript `primary_source .../wk-ed-final-1/staged-source/main.tex e2ed3729...`, `editorial_source.proposal .../wk-ed-final-1/proposal.json 8bd69e2b...` + staged-manifest `5f52fcd2...`, `authored_by weekly-final wk-ed-final-1 (changed reader, synthetic)`.
- LF ED4: manuscript `primary_source .../lf-ed-4/staged-source/main.tex dad9c3b7...`, `editorial_source.proposal .../lf-ed-4/proposal.json f6789141...` + staged-manifest `6ab75bce...`, `authored_by longform G7 editorial author lf-ed-4`.

Raw tool records: `build-record.json`, `validated-source-manifest.json`, `publication-candidate-v2.json`, `publication-set.json`, `quality/*` (incl `pdf_preflight.json` 5 pages + pdf SHA), `reviews/semantic-review-v2.json` + `visual-review-v2.json` at each sample path above; lifecycle/closure raw (`run-lf4-closure-.../stdout.txt`, `exit.txt 0`, `heartbeat.txt`; `weekly-final-editorial/ed-final-.../ed-prepare-stdout.txt`, `qa-build-weekly-stdout.txt` `pages 5`, `driver-stdout.log`).

## 3. Inspection method (independent, read-only)

- `pdfinfo` (poppler 26.01.0) + `pdftotext -layout` + `pypdf 6.16.2` `PdfReader` page-count + per-page `extract_text` length — read-only, no source/PDF writes. `pypdf` lengths: wk-c `[367,143,222,194,170]`, wk-ed `[454,143,222,266,170]`, lf-c `[388,649,1211,640,185]`, lf-ed `[550,649,1240,755,185]` — delta only on changed pages, consistent with text diff.
- Visual: `pdftoppm -png/-jpeg` to `/tmp/opencode/jgas-renewal-visual-20261025T000000Z` FAILED (`libpng Write Error`, `FzErrorSystem: cannot fwrite: Disk quota exceeded` on `/tmp` tmpfs 81% — recorded, not a source defect). Fallback: read-only `pymupdf 1.28.2` rasterization to owned evidence dir in workspace (different filesystem, ample space), DPI 130, all 5 pages × 4 PDFs = 20 PNGs, then `Read` of every PNG image. No PDF/source mutation; failed `/tmp` 0-byte artifacts removed.
- Compared complete Reader/proposed authored scope (manuscript `primary_source` + staged `main.tex` bytes via recorded SHA + `proposal.json` changed-reader deltas) to actual PDF text/layout. No project imports, no old runners, no tests, no Git mutation, no network, no source edits, no ordinary commit.

Display/citation extraction limits (explicit):

- `pdftotext -layout` linearizes LF cross-family comparison table and two-column narrative/synthesis; cell order is readable but not a table-fidelity proof. Hyphenation splits (`intro-duces`, `ap-proval`, `re-newal`) require visual join; URL extraction is correct but line-wrapped in layout text.
- `pypdf.extract_text` returns short per-page strings (headers/footers/page numbers included, Japanese preserved) — sufficient for presence checks, not for glyph/contrast/overflow.
- Visual PNGs at 130 dpi prove layout/overflow/contrast/bib presence at sanity resolution, not print-resolution glyph hinting or WCAG color-contrast certification. Citation `[1]`→References mapping verified manually per page, not via automated citation parser.
- TOC dots/page numbers (`lf-c/lf-ed p2`) render correctly; `pdftotext` preserves them as dot leaders — page-number correctness checked visually (2/3/4/4), not via TOC hyperlinks.

## 4. Findings — ALL pages inspected

### Weekly C (`8fb8aca...`, 5p) — BOUNDED FIDELITY/VISUAL PASS

- p1 cover: `Japanese Generative AI Technical Survey / 2026-W37 / 2026-09-11 / Weekly tested method, revised edition / Source-based survey / Target Model (SurveyInk blue)` + cutoff/repository/build + Japanese tagline `一次情報・論文・OSS・X上の技術反応を分離し…週刊 Technical Survey。` No overflow, rule + headline + deck spacing clean, Japanese glyphs rendered (no tofu) at 130 dpi.
- p2 `This week / A bounded technical survey / Evidence/scope boundary: One accepted primary source.` Purple header white text, light body — contrast readable, box fully inside margins.
- p3 `1 Evidence-bound headline / PRIMARY SOURCE / The source authors report the tested method. [1] / The source authors report that Target Model introduces the tested method. [1]` Hyphenation `intro-duces` is TeX-legal, no overflow, `[1]` blue, matches bib.
- p4 `2 今週の総括 / WEEKLY SYNTHESIS` 3 paras: `The edition surveys one source. / The claims remain attributed. / The accepted source authors describe the tested method.` Japanese heading renders, no overflow.
- p5 `References/Source Notes [1] Unknown. Target Model. url: https://example.invalid/target-source (visited on 08/22/2026).` URL blue mono, single entry, matches in-text `[1]`×3. No orphan/extra refs.
- Manuscript match: staged `1e3b22a5...` + bib/style SHAs in manuscript = build-record declared inputs; PDF text equals staged reader scope (complete reader bytes per implementation proof, headline/prose equality alone not relied on).

### Weekly ED final (`1c396fac...`, 5p, new headline+3 paras) — BOUNDED FIDELITY/VISUAL PASS

- p1 delta vs C: headline `Weekly tested method, revised final edition`, deck `Source-based survey with weekly-final renewal-editorial amendment; synthetic, no genuine approval.` Wraps to 2 lines with `ap-proval.` hyphen — inside margins, no overflow. All else identical to C (cutoff/repo/build/Japanese tagline unchanged). PNG hash differs only on p1/p4, p2/p3/p5 hashes identical to C (`wk-ed-p2==wk-c-p2`, etc.) — proves selective change.
- p4 delta vs C: `The edition surveys one source with weekly-final changed reader. / The claims remain attributed; renewal proof fresh, tool epoch final. / The accepted source authors describe the tested method.` Third para (exact synthesis) preserved. No overflow, 3 paras clean.
- p2/p3/p5 byte-identical visually to C (SHA-identical PNGs + identical `pdftotext`), bib unchanged `faeae610...`.
- Manuscript match: staged `e2ed3729...` (1836B vs C 1679B) + proposal `8bd69e2b...` changed-reader authoring; PDF reflects new headline/deck + 2 changed synthesis paras, synthesis sentence preserved per Weekly envelope rule.

### Longform C (`4ce0495c...`, 5p) — BOUNDED FIDELITY/VISUAL PASS

- p1 cover: `... Special / SP001 / Thematic history / as of 2026-08-21 17:00:00 UTC / Fixture lineage cover / Source-based lineage survey / Target Model` + cutoff/repo/build + Japanese tagline `... Thematic Longform Special。` Clean, no overflow.
- p2 frontmatter + TOC: `Fixture frontmatter / A bounded lineage survey / Scope/attribution boundary: One accepted primary source per package.` + `目次` with 4 entries + dot leaders + pages 2/3/4/4. Japanese `目次`/`この号の総括` render, no tofu. Blue TOC links, purple boundary box contrast readable.
- p3 dense two-column + boxes: `1 Evidence-bound headline / THEMATIC LINEAGE 1/1 — 001 / The source authors... [1] / Theme at a glance (Focus/Signal) / Fixture narrative one/two / Transition timeline (Early/Late) / Fixture synthesis / Claim boundary / Source-backed Technical Notes (Fixture note, Chronology, Technical points •×2, Limitation/attribution, Primary URL https://example.invalid/papers/lineage-note-one)`. Checked: no column overlap, no text outside blue/purple/gray boxes, `Technical Notes` gray header (`Fixture note for pkg-001`) black-on-light-gray readable at 130 dpi (bounded sanity, not colorimeter). All `[1]` present, URL blue mono single line.
- p4 `2 Fixture cross-family synthesis / CROSS-FAMILY SYNTHESIS / 2 paras [1] / Cross-family comparison` table (`観点 / GLM/Qwen/DeepSeek/Kimi`, 3 aspect rows, all `[1]`) + `3 この号の総括 / ISSUE SYNTHESIS` 3 paras (`The edition surveys accepted lineage sources. / The claims remain attributed to their origins. / The synthesis stays inside authorized evidence.` two-column). Table grid fully inside blue box, Japanese `観点` renders, no overflow.
- p5 `References/Source Notes [1] Example. Target Model. url: https://example.invalid/papers/lineage-note-one (visited on 08/22/2026).` Matches in-text `[1]` count scope.
- Manuscript match: staged `c1da86fc...` 4917B + bib/style SHAs = build-record inputs; PDF equals staged reader scope.

### Longform ED4 (`c3b6992b...`, 82921B, 5p, new reader) — BOUNDED FIDELITY/VISUAL PASS

- p1 delta vs C: title `LONGFORM renewal-editorial G7: changed reader after U5 archive-correction; no genuine approval.` (3 lines, inside margins) + deck `Changed deck for U5-active prior: same accepted research/Draft/Architecture, changed reader bytes (G7 fix witness).` No overflow, Japanese tagline unchanged.
- p2 identical to C (`lf-ed-p2==lf-c-p2` PNG SHA), TOC/pages unchanged — correct (frontmatter not part of G7 delta).
- p3 delta vs C: `Fixture narrative-one paragraph one ... Revised G7 sentence within approved evidence with LONGFORM editorial amendment. [1]` (vs `Revised fixture sentence within approved evidence.`). Two-column flow rebalanced (right column `narrative-one para two` moves up) but no overlap, boxes intact, `Technical Notes` contrast unchanged. PNG hash differs as expected.
- p4 delta vs C: `3 この号の総括` now `The edition surveys accepted lineage sources with a fixture-local editorial amendment after versioned renewal (G7). / The claims remain attributed to their origins under the same accepted research and Draft. / The synthesis stays inside authorized evidence.` (reordered + amended, `re-newal` hyphen legal). Table unchanged. No overflow.
- p5 identical to C (`lf-ed-p5==lf-c-p5` PNG SHA), bib unchanged.
- Manuscript match: staged `dad9c3b7...` 5221B (vs C 4917B) + proposal `f6789141...` + staged-manifest `6ab75bce...`; PDF reflects G7 deck + narrative + synthesis deltas, accepted research/Draft/Architecture unchanged per proposal basis.

## 5. Fixtures/reviews — explicit nongenuine, semantic NO-GO

- All 8 review records inspected (JSON, read-only): `reviewed_by` = `renewal-c-fixture synthetic ...; no genuine approval`, `renewal-c1-fixture synthetic ...; no genuine approval`, `synthetic Weekly semantic/visual reviewer weekly-final (no genuine, Production NO-GO)`, `synthetic LONGFORM semantic/visual reviewer G7 (no genuine approval)`; `status PASSED` is a typed-fixture PASS, NOT genuine Human approval, NOT Production release. Placeholder fixture prose (`Target Model`, `Fixture ... for pkg-001`, `https://example.invalid/...`) remains Production semantic NO-GO by design. No transfer from previous R3 old tests; fidelity/visual here are bounded to these 4 PDFs only.
- QA `PDF_PREFLIGHT` (5 pages + pdf SHA) + `IDENTIFIER_PRESERVATION` + `SUBJECT_ENTITY_PROPERTY_BINDING` (Weekly) / `+EMPTY_WRAPPER_SUPPRESSION` (Longform) are deterministic byte checks, not semantic approval.

## 6. Scoped verdict (not whole-unit acceptance)

- **Weekly C FIDELITY/VISUAL BOUNDED PASS** — 5/5 pages inspected, text/ref/bib/style/glyph/overflow/technicalnote(n/a — no tech-note box on Weekly; purple boundary contrast OK) clean, manuscript→PDF scope matches, real `EXECUTED_BUILD` materialization recorded.
- **Longform C FIDELITY/VISUAL BOUNDED PASS** — 5/5 pages inspected, two-column/table/tech-note contrast (bounded visual) clean, no overflow, manuscript→PDF scope matches, real `EXECUTED_BUILD` recorded.
- **Weekly renewal→editorial (`1c396fac...`) FIDELITY/VISUAL BOUNDED PASS** — 5/5 pages inspected, new headline + 3 paras (2 changed + synthesis preserved) render with no overflow, selective-change PNG hashes confirm scope, real editorial build + P1→activate chain recorded (`ed-prepare` `PDF 5p 63204B 1c396fac`, seal `c4647bbe`, r3 `ef2b8f93`).
- **Longform renewal→editorial (`c3b6992b...`) FIDELITY/VISUAL BOUNDED PASS** — 5/5 pages inspected, new G7 reader (deck + narrative + synthesis) renders with no overflow/overlap, selective-change hashes confirm scope, real editorial build + clean closure `exit.txt 0` (`PDF 5p 82921B c3b6992b`, seal `737b78...`, r9 `7dfc73...`, LIVE `[]`, semantic `PASSED/9` + visual `PASSED/5` synthetic) recorded.
- **Semantic / representative-quality: NO-GO (remains)** — placeholder synthetic content, no genuine approval, no Production quality claim. **Whole-unit acceptance: NOT claimed** — U reuse taken as manifest observation only, normal direct Candidate/Preview/Freeze/Release + failure/resume + affected regressions + independent final implementation review remain for other workers per `remaining-route-failures.md` / `independent-operation-review.md`. No fabricated genuine PASS / new Human Gate.

## 7. Method limits + provenance

- Independent: no implementation/fixture authorship; only read (`Read`, `Glob`/`Grep`), read-only `sha256sum`/`pdfinfo`/`pdftotext`/`python3 -c (pypdf/pymupdf/stdlib json/pathlib)`, new owned rasterization. No network, no old runners, no project imports, no tests, no Git mutation, no ordinary commit, no source edits. Started from Human `f84fcf5` context; fixture DBs untouched.
- `/tmp` rasterization failed with disk-quota (`Disk quota exceeded`) — documented above; workspace rasterization succeeded. `Read` rendered all 20 PNGs successfully; no `cannot-visual` disclaimer needed for these samples, but PNGs are 130 dpi sanity renders, not print certification.
- Evidence (NEW only, no Git DB in notes): `resume-20261025/independent-reader-visual-evidence-20261025T203744Z/` — 20 PNGs (`wk-c-p{1..5}`, `lf-c-p{1..5}`, `wk-ed-p{1..5}`, `lf-ed-p{1..5}`), 4 `*-pdftotext-layout.txt`, 4 `*.pdfinfo.txt`, `SHA256SUMS.txt`. This review is `resume-20261025/independent-reader-visual-review.md`. No other files written.

