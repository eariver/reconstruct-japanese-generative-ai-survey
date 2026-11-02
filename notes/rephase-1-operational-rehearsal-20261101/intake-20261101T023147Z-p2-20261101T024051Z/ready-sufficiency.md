# Ready sufficiency — pre-Architecture dossier + Raw + reader/PDF + repair worklogs

Code authority: final 138 only. Intake DATA never adopted as code. Compat `.py`/projection only comparison, never executed/adopted. Old approvals never rebound. Broad SP 12-dim NOT claimed as four-family generated compatibility.

## 1. Actual bytes verified (aggregated full coverage, not sampled counts)

### W34 @774 — checkpoint-selected 369/439/409 graph (stale 110/80 index superseded)
- Discovery: `discovery-v2.jsonl` 963155B `e176326f...` 369 rec; `discovery-accepted-v2.json` 377589B `c1dc53f8...`; crosswalks v0.1 186672B + v0.2 195834B; event-discovery 1335444B `0a23be47...` via blob (439 event rec).
- Screening: Sol authority 6160B + supplement 3560B; accepted `415.../screening-accepted.json` 543880B `d18c8ce3...` 439 rec/decisions (135 KEEP-family scale per checkpoint review: 409 non-DROP basis for Evidence).
- Evidence/Views (full 409 in aggregated files, per-task sharded files NOT fetched to avoid 800-file dump): `647.../evidence-accepted.json` 126603B `8437905d...` 409 results; `interactive-evidence.json` 1573186B via blob (409 inputs); `package.json` 157446B; `e2e6.../edition-views-accepted.json` 159498B `5991cd9e...` 409 views.
- Ledger/Completeness: `materiality-ledger-v2.json` 186202B 439 rows; `profile-completeness-v2.json` 71532B 3 obligations LIMITED.
- Selection/Architecture: `candidate-matrix-v2.json` 676213B 409 rows (MATERIAL41/CONTEXT358/HOLD10; VERIFIED49/PARTIAL352/NEEDS_MORE8); `candidate-selection-v2.json` 289679B SELECTED41/HOLD368 (PRIMARY10/SUPPORTING31); `architecture-v2.json` 27528B `7f30d273...` (== reader-manuscript architecture SHA); summary 202555B + attention 18372B (41 placed P1-P6, P7 synthesis empty, c045 SUPPORTING in P4).
- Supplement/Raw: `evidence-authority-supplement.json` 50490B 61 bodies/60 SHA/50 bindings; collectors top listings (arxiv/github-releases/official-pages/gapfill) + carryover ledger 2407B (1 RECHECKED_UNRESOLVED) + `tree.json` 3351-path inventory (blob SHAs). Collector raw bytes (73 paths) inventory only (see missing).
- Reader/PDF (historical, exact-SHA reused, no new W34 PDF fetch): manuscript 19652B `c453bea7...` (arch coverage 7 pkgs + synthesis reqs, Gemini 3.8 Flash r2); `main.tex` 1262B `9d320a62...` + 8 sections + `references.bib` 8630B + `99-source-notes`; PDF 338722B `e93db71a...`/blob `a9d0b661...` (== 774 tree + candidate/release expectation, 12pp). Checks DRAFT→VALIDATED→CANDIDATE→FROZEN→RELEASED chain verified.
- Checkpoints: 10 JSONs (2019–6109B) binding above SHAs; contract `704eacb9...` (pre-09-11) → `7e37522c...` (post-09-11) preserved.

### SP @c8 — 165/160/112/9-pkg graph (original labels preserved; accepted points to compat-projected)
- Discovery (original unprojected): `discovery-v2.jsonl` 173299B `7074cef2...` 165 rec; `discovery-accepted-v2.json` 135693B `b57fb044...`; r2 44352B (history, not current). Original `PRIMARY_DOC/REPO/ANNOUNCE/MODEL_CARD/SPEC/SEC_REF/SEC_TECH/RUNTIME_RECIPE/PACKAGING/RUNTIME_PR` labels preserved in these inputs.
- Screening (DIRECT basis, original): accepted `24bac6aa.../screening-accepted.json` 69226B `65330476...` 165 rec (135 KEEP/20 MAYBE/5 INSPECT/5 DROP; non-DROP 160); `interactive-decisions.json` 68226B (full decisions).
- Evidence (accepted IS compat-projected `dba89409...`, comparison only): `evidence-accepted.json` 49241B `72ba3407...` 160 results (PARTIAL148/VERIFIED12 per validation-report); `edition-views-accepted.json` 64227B `364d484a...` 160 views; `package.json` 48659B `60860c88...` (== validation-report); `interactive-evidence.json` (accepted) 311908B == r2 (compat input). Original unprojected semantics fetched: `evidence-interactive-input/interactive-evidence.json` 313083B `6cac92b1...` (== ts001 r1) 160 rec + `task-targets.json` 12011B + r2 311908B `8cff1a0e...` (note: validation-report quoted r2 `5f8395d0...` ≠ fetched `8cff1a0e...`; record discrepancy, use fetched bytes).
- Compat (comparison only, never adopt): `projection-ledger.json` 87223B `b99a3068...` + README 4431B + `compat-package` dir listing; prior 4-doc `.py` DATA remains unexecuted. Do NOT treat projected counts as canonical map authority.
- Ledger/Completeness/Selection/Architecture: `materiality-ledger-v2.json` 66865B `ad750936...` (see counts: MATERIAL137/CONTEXT23/EXCLUDED5 per validation-report); `profile-completeness-v2.json` 32511B `aeeadd19...` 15 obs (3 SATISFIED/12 LIMITATION incl O13-O15 `attention_sequence_kv_cache/decoding_acceleration/inference_kernels_serving` gap-fill lanes); `candidate-matrix-v2.json` 236220B `1dcc2902...` 160; `candidate-selection-v2.json` 83877B `f91af7cf...` SELECTED112 (PRIMARY53/SUPPORTING59)/HOLD12/REJECT33/INSPECT3; `architecture-v2.json` 32767B + summary 72043B + attention 17230B (9-pkg PROPOSED 76/96pp, READY_FOR_REVIEW, D128 visible in P8, Jev in P7).
- Supplement/Raw (required primary): `evidence-authority-supplement-r1.json` 12859B `62031208...` (== validation-report) + raw 13 files 1,275,978B total (each verified: 43673/84605/41955/44150/45145/45614/597003/53747/43155/43732/41417/149239/42543) + `raw/` 25 discovery observations (1680–8503B each, D01-D10 + R2-G12-G19 + R3-D09-G21-G23 + R4-X + negative-space/methodology/capstone) + `research-scope-v2.json` 12302B.
- Reader/PDF (present at c8, now fetched — not unapproved separate asset): `main.tex` 293777B `87bcb707...` + `references.bib` 39266B `9c0edead...` + `main.pdf` 850785B `8a9a721a...`/blob `a5974701...` 66pp; manuscript 9657B `cf7aca20...` (arch EFF-O01-O12 → Sections 1-9, deterministic fidelity only); candidate `adf22516...` binds manuscript/tex/PDF/quality/semantic/visual; surface-gate 4315B + semantic 7521B (9 checks, below-target 66/76) + visual 4065B (5 checks) + quality 3056B + freeze 1071B + manifest 655B + merge 573B + release 797B + revalidation 5938B (`380cedca...` == state provenance). DRAFT manuscript `f99c3b93...`/PDF `bc6e280c...` superseded by final (record gap closed).
- Checkpoints: 10 JSONs (2210–6491B) binding above SHAs; publication revalidation `380cedca...` in state.

## 2. Missing boundaries (no completeness claim)

- Per-task sharded files NOT fetched (by design, aggregated IS full coverage): W34 80+80 historical + 409+409 current tasks/results/views (tree counts 2461 evidence +661 views paths); SP 160+160 tasks/results/views (accepted dirs list 6 +2 entries; views subdir counts unverified beyond aggregated 160). If execution later needs sharded bytes, they remain at fixed refs (no new permission) — ask only if actually needed.
- W34 collector raw bytes (73 paths: arxiv/github-releases/official-pages/gapfill raws) — top listings only (4 dirs), bytes NOT fetched. Discovery/event-discovery + supplement + cards contain excerpts; full publisher-byte re-verification would need these (available at 774, no new permission).
- W34 screening batches/results intermediates (12 batches +12 results in `415...`) + historical acceptances (`2ab82c6b...` 105, `5692a79a...` 110) — only current `415.../screening-accepted.json` fetched (correct for selected graph; history preserved in tree, not fetched).
- SP screening input/results subdirs + evidence tasks/results/views subdirs contents — listings only (accepted dirs 6 entries each), bytes via aggregated files (full 165/160/160). Sharded bytes remain at c8 if needed.
- W34 execution 450 worklogs — only 4 stage validations +2 session worklogs +3 gates + index (stale) + tree inventory fetched. SP execution 20+ dirs — only index +3 validations +2 sessions +1 Sol review + listings fetched. Wall-clock/LLM/role/cost rows remain UNKNOWN (see below).
- No missing-ref 404; no rate/storage limit hit (179/179 success). If later fetch hits limit, return exact gap with completed raw.

## 3. Exact captured full-graph vs unverified record counts

- Captured + SHA-verified: all checkpoint→artifact SHAs above (W34 10 + SP 10 checkpoints match fetched bytes); aggregated counts verified in bytes (W34 369/439/409/409/439/3/409/41; SP 165/165/160/160/165/15/160/112). Supplement raw 13/13 bytes sum 1,275,978B matches validation-report. SP PDF/tex/bib SHAs match candidate/manuscript bindings. W34 PDF/manuscript SHAs match candidate/release/tree.
- Unverified (existence from listings/tree, bytes NOT verified here): per-task sharded contents (counts from tree/listings, not byte-checked); W34 collector raw contents; SP screening input/results sharded contents; historical acceptances beyond current (counts from tree/listings). Do NOT claim these from transport/inventory alone.
- Discrepancies preserved (not smoothed): W34 index (110/80) vs checkpoint graph (369/439/409); SP validation-report r2 `5f8395d0...` vs fetched r2 `8cff1a0e...`; SP DRAFT manuscript/PDF vs final candidate/freeze (supersession recorded).

## 4. Calls/exits/total bytes

- **179 GETs, 179 `exit 0`, 179 `HTTP 200`**, stderr empty (2 manual `p2f` same). Times in `p2*.time.txt` (actual UTC 2026-11-01T02:40–02:55Z), PIDs in `p2*.pid.txt`. Full argv/url/ref/headers/body/stdout/stderr preserved; `DATA.*` hashes after saving in `manifest.json`.
- **145 DATA files, 12,194,416B** total (10.5MB Phase A-C +1.7MB supplement/raw/package). Raw transport 15MB+ with base64 overhead. No fake download proof.
- Reused (no new fetch): prior 6 GETs + tree + 15-file W34 snapshot + 774 manuscript + 3e3e PDF + 4-doc intake.

## 5. Reusable historical semantic products (provenance, not approvals)

- W34 RELEASED (774 + 3e3e PDF): candidate `df376f47...`/release `6808dbb0...`/manuscript `c453bea7...`/tex `9d320a62...`/PDF `e93db71a...`/quality/semantic/visual + gates `0fef8e29.../80e90446...` + checkpoints — usable as Weekly reference + exact-byte reuse (PDF/manuscript verified). Old Human approvals MUST NOT be rebound to new bytes/paths.
- SP RELEASED (c8): candidate `adf22516...`/manuscript `cf7aca20...`/tex `87bcb707...`/PDF `8a9a721a...`/quality/semantic/visual + gates `5289b68e.../15b88fb22...` + revalidation `380cedca...` — usable as broad-Thematic reference (12-dim, NOT four-family proof). Old approvals MUST NOT be rebound.
- Compat workaround (`WORKAROUND_VALIDATED`, ledger `b99a3068...`, package `60860c88...`) — mechanical-investment evidence + comparison only; NEVER `CORE_FIXED`/canonical map authority.
- Synthetic fixtures (regeneration S0/S1/S2, TL2026 PDFs, profile-support batches) — mechanical investment only per CORR C3, NOT recurring baseline.
- Worklogs captured (W34 4 validations +2 worklogs +3 gates; SP index +3 validations +2 sessions +1 Sol pass + reviews/sessions listings) document operation/repair disposition only. Missing cost (wall-clock/LLM/role/handoff/loops/QA/Human/frequency/horizon) stays UNKNOWN; no reconstructed timings.
