# Publisher intake supplement — necessary version metadata only (preserve original 40)

Supplement of `publisher-intake-20261101T163426Z` (40 req/40 DATA preserved, no overwrite, no modified original files). New dir `publisher-intake-supplement-20261101T172535Z`. Cutoff `2026-09-21T16:10:00Z`. No subagents, no Production/state/test/code exec, no weights, no broad search/crawl/clone.

## Correction: Last-Modified ≠ disproof

Later modification alone DOES NOT disprove earlier publication. API `published` (first version) vs `updated` (latest version) vs `observation` (retrieved 11-01) vs commit/dateModified/lastModified are separate. P5 `published_at`/record dates are UNVERIFIED (may refer to revision/record, not first publication), NOT marked false solely because current Last-Modified is later. Current bytes do NOT prove old revision.

- sp11: `date 2026-09-15` field present in current body + Published Oct 28 + SSR Oct 27 + Last-Modified Oct 28 — both true, UNCONFIRMED historical.
- sp16: Sep 10 commits + Oct 16 lastModified — both true; Sep 10 now CONFIRMED via exact README.
- vLLM Oct commits vs Sep claim — gap proven, not false.
- PR merged Aug 27 + updated Sep 05 — both ≤ cutoff, CONFIRMED.

## Per-DID version decisions (machine pointers in manifest.json did_decisions)

- 10 arxiv: KEEP (verified local API/abs histories, latest≤cutoff = selected). No new bodies:
  EAGLE v3 2025-03-04, Snell v1, s1 v3 2025-03-01, ThinkPrune v1, overthinking v1 2026-04-12 (only version, NO v2 exists — P5 08-24 unverified, no v2 to capture), FrugalGPT v1, Kimi v2 2025-11-01, Qwen v1 08-31, V4.1 v1 09-17, V3.2 v1. All CONFIRMED.
- TypeSafe 3: NO new fetch (local parse suffices). UNCONFIRMED current-only: launch (09-15 field + Oct 28 mod), concepts dateModified Oct 14, models dateModified Nov 01 (1.13 + 1.14 drift). Use with quarantine or narrower PARTIAL.
- vLLM: CURRENT ONLY + gap proven. Correct repo is `vllm-project/vllm` (Edit/blob hrefs, not recipes). File @main sha 29a4c64 + blob commit e0d 2026-11-01 (> cutoff). File history 13 commits Oct 17-31, 0/13 ≤ cutoff (created Oct 17 Host recipes + sync recipes#1136,#1137). Historical source likely in `vllm-project/recipes` — exact path unknown, STOP exact need, no broad clone. Pinned 09-20 unverified.
- PR27742: COMPLETE (NEW, no overwrite). `s15-commits-all100` 65/65 (all 08-25–08-27 ≤ cutoff) + `s15-comments-p1-100` 100 + `s15-comments-p2-100` 44 =144/144 (all 08-26–09-05 ≤ cutoff). CONFIRMED. Existence≠correctness retained.
- HF: MIXED. API `/commits` 404 preserved + wrong-repo attempts preserved (404/422/empty). Same-document `commits/main` HTML 267KB gives 17 commits (11 Sep 10 ≤ cutoff +6 Oct > cutoff). Latest≤cutoff `dba1be0 2026-09-10T08:18:10Z` (matches P5 09-10, corroborated). NEW `DATA.s16-README-dba1be0.md` 13110B 347c9db4… (NO weights, CED/CSA/Engram/DSpark) CONFIRMED. Current card/API (Oct 16) UNCONFIRMED.
- Dynamo: UNCONFIRMED (dev current only, kustomization links are not doc source, no direct Edit link — STOP, no new repo guess).

## New requests (12, all within 17 + direct version links)

- PR 3: commits-all100 per_page100, comments p1/p2 per_page100 (complete 65+144).
- HF 2+1: commits API 404 (preserved) + commits/main HTML + README@dba1be0 (historical body).
- vLLM 5+1: recipes-path empty [] (wrong repo preserved) + file-main 404 + commit 422 (wrong repo preserved) + file-main-correct + commit-e0d-correct + file-history-correct (gap proof).
- No arxiv/TypeSafe/Dynamo new bodies (local parse suffices, avoid repeat 40).

Files: `DATA.*` (12 NEW, distinct gids `s15-* s14-* s16-*`, no overwrite) + `*.headers.txt`/`*.stderr.txt` (redirect chain)/`*.command.txt`/`*.url.txt`/`*.time.txt`/`*.exit.txt`/`*.bytes.txt`/`*.sha256.txt` + `manifest.json` (per-DID decisions + evidence pointers + gaps) + `fetch-supplement-phase*.sh`. No token logs. DATA never executed.

Return: 1 NEW historical body (HF README Sep 10) + PR complete (65+144 CONFIRMED) + 10 arxiv KEEP (no new) + 6 UNCONFIRMED current-only (3 TypeSafe + vLLM + Dynamo + HF current) with exact gaps. No semantic VERIFIED, no State change. Needs independent SP Evidence re-review.
