# W34 baseline reader assessment — historical working final (not a Gate/pass)

Role: independent historical reader/quality baseline assessor, not candidate author or rehearsal edition author. No approval, no Gate, no audit.
Authorization: Human 2026-11-01 — W34 + efficient-LLM target, fixed-ref limited intake. This task covers ONLY W34 baseline read on already-authorized archived bytes.
Bounds: no network, no Production/current checkout, no Git/readback, no source-code import/runtime/tests/fixtures, no new approval. PDF inspected via local read/render utilities only (text layer + render metadata); no project build. No subagents. Inspection evidence saved in ignored runtime `.rephase-1-editorial-runtime/w34-baseline-20261101/` (text + `pdf-inspection.json`), not a build artifact.

## 1. Actual inputs (full hashes, pages read)

- Reader manuscript (authorized archived copy): `.phase-5-inputs/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/publication/v2/reader-manuscript-v2.json` — **19652 B, SHA256 `c453bea798f6d7693d2e92d1dbae3fc7838b24d90df382c2547f3ad033b7c10e`** (actual rehash matches intake get01 expectation `c453bea7…`). Read in full (385 lines: status `READER_FACING_AUTHORED`, 7 architecture packages → 30+ requirement rows all `FULFILLED`, 2 reader-requirements `FULFILLED`, 10 supporting files + bib/style with SHA/byte counts; `authored_by Gemini 3.8 Flash (W34 Human preview r2 Issue #491 repair)`, `recorded_at 2026-09-13T14:30:00Z`).
- Final PDF (authorized archived copy, verified reusable by exact SHA at 774): `.phase-5-inputs/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/surveys/weekly/2026-W34/main.pdf` — **338722 B, SHA256 `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`** (matches get01/get02 + tree blob `a9d0b661…`). **All 12 pages read** via text-layer extraction (total ~27191 chars) + render metadata (A4 595×842 pt, 0 embedded images, 0 blank pages, blocks 10–85/page). Normalized counts (de-hyphenated): `visited on 09/08/2026` ×41, `url:` ×41, normalized repair sentence ×1, `Selection r2` ×0, `Package 4` ×0, `08/21/2026` ×0.
- Fixed profile/state (reused archived bytes, not re-fetched): `.rephase-1-inputs/774…/sources/2026-W34/production-profile.json` (WEEKLY/WEEKLY_MAGAZINE, ROLLING_WINDOW 2026-08-14–21 America/New_York, 3 obligations) and `production-state.json` (`RELEASED/COMPLETE`, 11 transitions 2026-09-02→09-13, all machine checkpoints passed, both Human gates approved, `publication_revalidation_provenance null`). Historical linkage only — old approvals are NOT rebound to any new bytes.
- New intake DATA (reference, not re-verified here): `intake-20261101T023147Z/DATA.publication-candidate-v2.json` (`candidate_sha256 52c8d0bc…`, pdf/manuscript SHAs as above, 12 pp) and `DATA.release-record-v2.json` (`released_at 2026-09-13T16:48:08Z`, tag `weekly/2026-W34`).
- Repair worklogs actually read (already-captured): `execution/luna/w34-human-preview-r2-issue491-repair/session-worklog.md`, `execution/luna/w34-freeze/session-worklog.md`, `execution/reviews/w34-human-publication-preview-decision-20260913-r2.md`, plus stale `execution/index.md` (ARCHITECTURE_ESTABLISHED snapshot — historical, superseded by RELEASED state; do NOT cite as current).
- This is the **final WORKING repaired baseline** (post-r2 PDF `e93db71a…` supersedes pre-repair `1818e866…` 338707 B). The deliberately-bad pre-repair state is NOT the baseline. Old index stale counts (e.g. Selection SELECTED 1 / MATERIAL 1) are historical and NOT current coverage proof.

## 2. Direct observations — what the reader actually gets (with locators)

Mission lens: weekly question "what materially changed + why it matters now" is answered through visible selection → compressed sections → explicit limits, not through asserted completeness.

Observed good (directly verified in bytes above):

- **Selection visible as structure, not hidden.** p2 Contents + pp3–9 six feature sections (control-plane / workflows / safety-security / model-economics / creative-multimodal / ecosystem-infrastructure) + p9 Week-in-Review synthesis that explicitly reuses only prior sections ("横断…新しい事実の典拠を起こさない", p9). Manuscript `architecture_coverage` binds each package to 1 section file (e.g. 4 control-plane requirements → `sections/10-agent-control-plane.tex`). Reader can see what was chosen and where it lands.
- **Lead / why-this-week.** p1 cover lede (JA: 支払い・操作・共同作業・検索が実装の姿で並び…何がどこでいくらでどの条件のもと動くか) + p2 "This Week in AI" three-axis framing (実行 / 統制 / 配備) + p9 synthesis (中心/制約/配備の三軸 + next-watch list). Cutoff explicit on p1 (`Editorial cutoff 2026-08-14 18:00 – 2026-08-21 18:00 America/New_York`) and repeated p2/p10.
- **Technical explanation with claim boundaries, not hype.** Each content section ends with a bilingual 読解上の境界 box (12 occurrences of the heading across pp3–9): vendor framing quarantined (e.g. p3 "'Agents transact safely at scale' is vendor framing", "Performance/latency … vendor-stated without benchmarks"; p4 FinanceBench/OfficeQA "Mistral-reported … no independent reproduction"; p6 Astra "cannot be ruled out … no evaluation scores"; p7 cross-region "architectural claims without workload measurements"; p8 "'Commercially safe' is Adobe framing"); date-precision limits stated per item (date-only vs 22:00Z boundary unresolved, Aug 26 re-date distinguished, Sep 8 capture dating).
- **Date/source roles separated.** p10 "Sources & limitations" + "Temporal and claim boundary" explicitly assign roles: official/project docs → conditions/routes; changelogs/Model Studio → date-bounded; researcher reports → not substituted for vendor assertions; uncaptured bytes stay uncaptured (MSRC JS-shell, Ray advisory/NVD, retention scope). References pp10–12 list 41 entries, each with `visited on 09/08/2026` (41/41 normalized) — matches r2 biblio repair.
- **Historical defects verifiably repaired in final bytes.** Normalized repair sentence present ×1 (p5 tail → "Regional processing is outside the scope of this section and is discussed with deployment and model-distribution conditions"); `Selection r2` / `Package 4` leakage ×0; blanket `08/21/2026` urldate ×0. This is a text-layer fact about the final PDF, not a semantic PASS.
- **Visual baseline (bounded).** 12 pp, uniform A4, no blank pages, no embedded figures (images 0/page — text-only layout, so no figure-rendering risk to carry). Mixed JA/EN body with section headers, boundary boxes, and reference list renders as rasterizable pages (60 dpi probe 497×702 px/page, non-blank). No print-proof claim beyond this (see §4).

Observed problems / readability costs (reader-visible, with locators — not Gate defects):

- **Boundary boxes are dense and bilingually fragmented.** pp3–9 boxes carry many short EN limit sentences with hyphenation splits (e.g. p5 "Regional pro-/cessing"; p6 "MSRC advisory bytes were / not captured"). Extraction needs de-hyphenation to recover sentences. Reader cost: high information density, small-type feel; rehearsal should preserve the guard content but review line-break/typographic calmness in proof, not by deleting limits.
- **Chronology precision is repeatedly deferred, not resolved.** Multiple "date-only … unresolved vs 22:00Z/W34-start" caveats (pp5–8: Qwen Aug 14, Claude watermark Aug 14, Imagen Aug 17 UTC moment, Vertex Jun 30 vs Gemini Aug 17). Honest as limits, but a new Weekly must decide whether this level of date-fuzz is acceptable or needs capture-time discipline — a rehearsal review question, not a W34 failure.
- **Comparability guard is asserted, not demonstrated.** p2/p10 promise no cross-condition ranking; spot-check confirms vendor numbers are attributed (e.g. Pika multiples flagged "non-normalized", DeepSeek tariffs marked secondary-reported p7). Whether any sentence implicitly ranks remains a line-level semantic question requiring Raw — not decidable from reader text alone.
- **Synthesis adds no new evidence by design** (p9). A reader wanting "so what" beyond the six sections gets framing + next-watch only. Whether that suffices for the Weekly mission is an editorial judgment for Human review, not a byte defect.

## 3. Pending primary verification — what forthcoming Raw intake must corroborate

Reader text alone does NOT prove research sufficiency. Do not treat selection counts, viewer labels, or old approvals as primary proof. For each item below, the rehearsal must fetch the exact fixed-ref bytes (W34 @774) and check the binding; this assessment does not duplicate that fetch or pretend it verified.

1. **Discovery→Screening→Evidence chain behind the 6 sections.** `discovery-v2.jsonl` (40 rec) → event expansion 110 rec → Screening KEEP45/MAYBE19/INSPECT16/DROP30 → active Evidence `377134b6…` (VERIFIED32/PARTIAL27/NEEDS_MORE14/REJECTED7) + Views `bcaa69b0…` → Ledger/Completeness (`LIMITED` with explicit limitations) → matrix 80 → Selection → Architecture 7 packages. Needed: exact accepted JSONL/JSON bytes + checkpoint SHAs (`CANDIDATES_NORMALIZED`, `EVIDENCE_REVIEWED`, `SELECTION_COMPLETE`) to confirm the reader's 7-package mapping is the true accepted closure, not the stale index snapshot.
2. **Per-claim capture bytes for high-risk attributions.** Grok Bot Aug 21 X observation vs Aug 26 re-date (manuscript `WEEKLY_COMMUNITY_MOVEMENT`); Transformers v5.15.1 release response (the one bounded in-window repo verification); Mistral FinanceBench/OfficeQA default-stack provenance; Pika cost multiples; DeepSeek tariff secondary-reporting boundary; Stripe/OpenRouter $7–8B exclusion; PORTS-Pike 8GW/financing plan-vs-fact split. Needed: collector/raw responses + `official-provenance.jsonl` capture timestamps (esp. Sep 8) + evidence `sources[].accessed_at`.
3. **Bibliography provenance.** 41/41 `visited on 09/08/2026` in reader PDF is consistent with worklog claim (Evidence `accessed_at 2026-09-08` superseding cutoff), but the 41 `references.bib` bodies + `bibliography-provenance-audit-r2.md` were not re-read here. Needed: bib bytes + audit table for exact capture-date binding (esp. c066 event/page/capture triple).
4. **Carry-over disposal.** Profile obligation `weekly:carry-over` + index note "one RECHECKED_UNRESOLVED; no promotion" + Completeness "carry-over explicitly disposed". Needed: carry-over ledger bytes to confirm nothing material was silently dropped.
5. **Render determinism.** `main.tex` (1262 B manifest entry) + 7 section bodies + `references.bib` + `jgaisurvey.sty` bytes + CI TeX log (run `34762344518`) were not re-read here. Needed: exact section/bib/style bytes + build log if rehearsal must reproduce byte-identical PDF; otherwise treat PDF as reference only.

## 4. Existing reader/visual guarantees to preserve / review in rehearsal

Preserve (do not regress without Human decision):

- 12-page repaired PDF identity (`e93db71a…`, 338722 B) as the working-quality reference; pre-repair `1818e866…` must not reappear.
- Per-section boundary boxes + p10 Sources/limitations + no-ranking rule as the editorial contract.
- 41-entry bibliography with uniform capture-date (`09/08/2026`) + per-item URL attribution.
- Bilingual JA body / EN boundary-sentence convention and section→package mapping.

Review (not automatic carry-over):

- Typographic calmness of boundary boxes (density, hyphenation, EN/JA mixing) in fresh proof — visual read required.
- Date-precision discipline: whether new capture pipeline can reduce "date-only unresolved" caveats or must retain them.
- Synthesis depth: whether next-watch + three-axis framing suffices for the new issue.

Visual note: inspection here is **text-layer + render-metadata only** (page size, non-blank, block/drawing/image counts, normalized string counts). No human-eyed typographic proof, no color/contrast/font-embedding check, no print check was performed. Missing visual cells stay missing — not faked.

## 5. Bounded quality-comparison criteria + concrete work removed/retained cost questions

Comparison is against this WORKING final (repaired 12 pp), never against the pre-repair draft or synthetic fixtures (regeneration S0/S1/S2, TL2026 PDFs, profile-support batches are mechanical-investment only, not quality baselines).

Suggested bounded criteria for rehearsal (judge on new disposable bytes, not carried PASS):

- Selection→reader traceability (each new section maps to an accepted package/requirement as above).
- Boundary-box coverage (every vendor/precision/methodology limit has an explicit reader-visible caveat; zero internal-lifecycle leakage in TeX).
- Date/source-role hygiene (cutoff stated, capture dates uniform, secondary-reported numbers flagged, no cross-condition ranking).
- Bibliography integrity (every citation resolves to captured bytes with correct access date).
- Visual readability (non-blank, stable pagination, calm boundary typography — human-eyed read required).

Factual rework events from permitted worklogs (effort NOT inferred):

- Human Publication Preview REQUEST_CHANGES r2 via Issue #491 (2 asks: internal-wording leakage; urldate/capture reconciliation), boundary `DRAFT_COMPLETE`, Architecture/Evidence preserved.
- Repair by Gemini 3.8 Flash: TeX line-18-tail normalization + Core #492 biblio-provenance rerun (41 MATCH/0 MISMATCH), fresh authoring commit `07c4b6a7…`, CI build run `34762344518` (3m45s wall — build only, not research/edit effort), fresh PDF `e93db71a…` (338722 B, 12 pp), regenerated manuscript/candidate/bundle/semantic/visual + stage validations to `RELEASE_CANDIDATE`, then Human approval r3 (comment `5654102081`) → FROZEN → RELEASED.
- Freeze carry-forward for W35+: early pre-publication reader-surface gate proposal (Layer 1 lexical + Layer 2 semantic, fail-fast before TeX/PDF) — explicitly outside W34 closure.
- All numeric LLM usage, per-role wall-clock, handoff counts, regeneration loops, QA/visual read time, Human discovery latency: **UNKNOWN** (durations from state-history timestamps 2026-09-02→09-13 are calendar spans, not effort). No synthetic timing may fill these cells.

Concrete cost questions rehearsal must answer with real worklog rows (`date | edition | stage/op | input bytes ref | role | wall_clock | llm | outcome | rework_reason | blocker`):

- How much research/read time does per-claim capture + boundary authoring cost vs. reusing this W34 boundary pattern?
- How much repair/rework does early reader-surface lint (the W35+ carry-forward) actually remove, measured in refused-vs-passed publication attempts?
- What stays manual regardless (date-precision judgment, vendor-vs-independent attribution, synthesis framing) — i.e. retained cost floor?

## 6. Explicit non-claims

This assessment is NOT a full semantic PASS, NOT a new Gate decision, NOT an audit, NOT a whole-quality-ready verdict. It does not approve any old release, rebind any old review/approval to new bytes, or certify full corpus completeness, render determinism, or adoption readiness. All semantic-source truth (publisher claims, benchmark figures, advisory scope, pricing/availability specifics) remains pending primary Raw corroboration per §3.

Evidence path: this file + ignored-runtime inspection bundle `.rephase-1-editorial-runtime/w34-baseline-20261101/` (12-page text + `pdf-inspection.json` with per-page rect/blocks/drawings/images + normalized counts). Assessment inputs: manuscript + PDF hashes in §1, profile/state paths, worklog paths, intake `material-sufficiency.md` §§2–3/5–6, packet `README.md` authorization/bounds, `operation-readiness.md` + CORR appendix (route predicates, no synthetic-as-baseline rule).

## 7. Addendum 2026-11-01 — actual page-appearance qualification + P2 coverage correction (this task only)

Scope: solely final-W34 baseline appearance qualification and updated evidence paths. No new Raw download, no broader semantic review, no approval/Gate/audit. Prior §§1–6 preserved; where this addendum conflicts on visual method or selection counts, this addendum governs as correction.

### 7.1 Method correction — text/metadata vs actually-seen appearance

- Prior reports (§1 line 10, §2 "Visual baseline (bounded)", §4 "Visual note") correctly stated **text-layer + render-metadata only** (page size, block/drawing/image counts, normalized string counts). That was NOT visual inspection, despite the shorthand "12 pages read." No visual PASS was or is claimed from 0-images/0-blank metadata.
- This addendum performs the actual appearance check: source PDF SHA re-verified (`e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`, 338722 B) with no new fetch, rendered locally via installed PyMuPDF to **NEW ignored-runtime dir `.rephase-1-editorial-runtime/w34-visual-20261101/`** (`w34-p01.png` … `w34-p12.png`, 100 dpi, 827×1170 px, 65–328 KB each), and **all 12 page images actually visually seen** via image-capable Read (p01–p04, p05–p08, p09–p12 in sequence). No network/project build/source edits/Git/current-checkout.
- Text-layer facts (§2) remain text-layer facts. Appearance facts below are image-observed only.

### 7.2 Page-appearance findings (image-observed, bounded legibility only)

- **p1 (cover):** blue rule, EN title, `2026-W34` / `2026-08-21`, large JA headline + 2-line JA lede, blue feature tags, bottom block (Editorial cutoff / Repository / Build) + gray JA method line. Generous whitespace, no overlap, no missing glyphs at render resolution.
- **p2 (contents + framing):** Contents 1–7, three light-gray boxed JA paragraphs (実行/統制/配備), purple この号の読み方 box, single-line reading-axis note. Running head (title left, 2026-W34 right), footer `2`. Clean stacking, boxes fully contained.
- **p3 (§1 control-plane, first half):** two-column JA body with citations `[1]` `[2]` visible; right-column body; purple-bordered 読解上の境界 box (EN) bottom-right, fully on-page. Header/footer consistent. No column overflow.
- **p4 (§1 tail → §2 head):** light-gray EN boundary box top-left (continuation of §1 limits, incl. Dogwood/W34-delta lines), then `2 仕事場…` heading + FEATURE: AGENT WORKFLOWS + JA lede + two-column JA body with `[9,10,11]` `[12,13,14]`. Small EN type legible at 100 dpi; hyphenation present but recoverable.
- **p5 (§2 tail → §3 head):** left JA body + purple §2 boundary box (FinanceBench/Mistral-reported, capture-dated Sep 8, Grok Aug 21/26 lines); right EN boundary box whose visible lines include the repaired sentence **"Regional pro-cessing is outside the scope of this section and is discussed with deployment and model-distribution conditions"** — repair confirmed by eye, not only by text-layer search. `3 安全と守りを一語に潰さない` heading + SECURITY GOVERNANCE + JA lede + body with `[21]` visible. Footer `5`.
- **p6 (§3 continued):** left JA body (KEV/Ray, Astra pacing, ZDR/monitoring, watermark, Defender essay) with `[22,23]` `[24,25,26]` `[27]`; right full-height EN boundary box (age-estimation, MSRC JS-shell, KEV-catalog-only, Astra "cannot be ruled out", ~20% overhead estimate, preview-status, ZDR carve-out). No overlap into body column; box border intact top-to-bottom.
- **p7 (§4 model-economics):** `4 モデルより配備の週` + MARKET TECHNICAL + JA lede + two-column JA body (`[28]`–`[32]` left, Bedrock/cross-region `[33,34]` right); right EN boundary box (post-promo scope, Sep-3 mirror, Aug-14 time unresolved, DeepSeek secondary-reported, Grok pre-window). Layout holds; citations break across columns without loss.
- **p8 (§5 multimodal + §6 head):** §5 JA body (`[35]`–`[39]`, Firefly/Imagen/Pika/wan3.0/Vision-Exp) + right EN boundary box (Commercially-safe framing, Vertex Jun-30 vs Gemini Aug-17, UTC-cutoff unspecified); `6 結節点と電力を押さえる動き` + ECOSYSTEM heading at page foot. No stranded heading (heading + lede start together on p9).
- **p9 (§6 tail + synthesis §7 head):** left OpenRouter/PORTS-Pike JA body with `[40]` `[41]` + purple §6 boundary box (price/terms unstated, scale company-reported, timelines planned); right `今週何が変わり、何が残ったか` synthesis + three-axis paragraphs with `[1,9,12]` `[3,21,22]` `[28,33,40]` + next-watch + purple この総括の読み方 box; `7 Week in Review / WEEKLY SYNTHESIS` heading at foot. Both columns end cleanly; footer `9`.
- **p10 (sources + refs start):** Sources & limitations gray box (4 sub-blocks) + purple Temporal and claim boundary box + References `[1]`–`[6]` with blue URLs wrapping across lines and `(visited on 09/08/2026)` per entry. No URL truncation beyond line-wrap; footer `10`.
- **p11 (refs continued):** `[7]`–`[30]`, blue URLs wrap mid-path across lines but remain complete across the wrap (spot-checked `[8]` antgroup, `[12]` mistral, `[14]` kimi-code). Footer `11`.
- **p12 (refs end):** `[31]`–`[41]`, closing with PORTS-Pike entry, then clean whitespace to footer `12`. No orphan header, no missing page number, no trailing overflow page.

Bounded legibility verdict (appearance only, not a visual PASS): all 12 pages paginate cleanly; two-column body + right/left boundary boxes co-exist without overlap on any page; JA body and small EN limit type are eye-legible at 100 dpi; running heads/footers/page numbers consistent pp2–12; no blank pages, no figures to misrender, no tofu/missing-glyph blocks observed. NOT claimed: font-embedding, color-contrast, print fidelity, or typographic perfection — those cells stay uninspected.

### 7.3 P2 coverage correction — stale-index inference superseded

Prior §§1/3 cited stale `execution/index.md` snapshot counts (Discovery 40 / event 110 / Screening KEEP45 / Evidence VERIFIED32+… / matrix 80 / SELECTED 1 / MATERIAL 1). That index is an ARCHITECTURE_ESTABLISHED snapshot and is **superseded for coverage by P2 actual State-selected graph at 774** (`intake-20261101T023147Z-p2-20261101T024051Z/`), which this addendum cites without re-downloading:

- Root discovery: **369 records** (`DATA.p2b01.discovery-v2.jsonl`, 369 lines).
- Screening acceptance: **439 records / 12 batches** (`DATA.p2b05.screening-accepted.json`: KEEP73/MAYBE136/INSPECT200/DROP30 of 439 decisions).
- Evidence acceptance: **409 results** (`DATA.p2b06.evidence-accepted.json`: PARTIAL352/VERIFIED49/NEEDS_MORE8).
- Edition views: **409 views** (`DATA.p2b08.edition-views-accepted.json`: MATERIAL41/CONTEXT358/HOLD10).
- Candidate matrix: **409 rows** (`DATA.p2b11.candidate-matrix-v2.json`); candidate selection: **SELECTED41/HOLD368 of 409** (`DATA.p2b12.candidate-selection-v2.json`, `selection_version w34-sol-selection-r2`, summary `selected_count 41`) — NOT "80 candidates / SELECTED 1".
- Architecture: **7 packages** (`DATA.p2b13.architecture-v2.json`: the 7 w34-* packages mapping to the 6 sections + synthesis). The "9 packages" figure in the task note belongs to the **SP** architecture (`DATA.p2b29.architecture-v2.json`: p1-bottleneck … p9-measure, 9 packages) and must not be cited as W34 coverage.
- W34 reader manuscript maps these 7 packages to sections (text observed in §2); the selection→architecture→reader chain to verify in rehearsal is therefore **369 → 439 → 409 → 41 SELECTED → 7 packages**, per P2 files above, not the stale 110/80/1 chain.

Pending-Raw list in §3 remains valid with updated denominators (replace "110 rec / 80 candidates / SELECTED 1" with the P2 chain above when fetching exact bytes).

### 7.4 Updated evidence paths

- Prior bundle preserved: `.rephase-1-editorial-runtime/w34-baseline-20261101/` (text + `pdf-inspection.json` = metadata only, explicitly not appearance proof).
- New appearance bundle (this task): `.rephase-1-editorial-runtime/w34-visual-20261101/w34-p01.png` … `w34-p12.png` (all 12 actually seen) rendered from SHA-verified `e93db71a…` PDF; no build, no approval, no corpus change.
- Coverage authority updated: P2 dir above supersedes `execution/index.md` for selection counts; W34 vs SP package counts kept separate (7 vs 9).
