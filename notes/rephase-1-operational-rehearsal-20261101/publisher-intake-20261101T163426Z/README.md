# SP bounded publisher intake — 17 exact URLs + version/body endpoints (no broad crawl)

Owner: General, external-material DATA only. No subagents. No Production checkout/Git readback/Production writes/code adoption/runtime/project tests/fixture/new Gate. No saved old scripts rerun (new `fetch-phase1.sh`/`fetch-phase2.sh` only).

Refs: packet `README.md` §§62-65 Human authorization (限定取得を許可 for EXACT17 in `intake-20261101T023147Z-p5-20261101T114236Z/did-bodies.md`), Current Evidence-quality hold, independent `reviews/evidence-efficient-llm-review-20261101T113240Z.md` §§3-5/§7 CHANGES_REQUIRED. Source138 unchanged. `.py`/downloaded code never executed. No weights (HF modelcard ONLY + API metadata).

Dir: `notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z` (NEW unique actualUTC). Per-GET `*.time.txt` governs. Cutoff historical scope `as_of 2026-09-21T16:10:00Z`; retrieval `2026-11-01T16:35:36Z to 2026-11-01T16:36:42Z`.

## What was fetched (40 requests, 40 exit0, 40 HTTP200, 40 DATA, 21054963B)

- arXiv 10: export API metadata + abs version history + version-pinned PDF primary (immutable vN < cutoff, verified API+abs):
  sp01 EAGLE v3 2025-03-04, sp02 Snell v1, sp03 s1 v3 2025-03-01, sp04 ThinkPrune v1, sp05 overthinking v1 2026-04-12, sp06 FrugalGPT v1, sp07 Kimi v2 2025-11-01, sp08 Qwen v1 2026-08-31, sp09 V4.1 v1 2026-09-17, sp10 V3.2 v1 2025-12-02. All PDF %PDF + application/pdf + title match.
- Living docs 7 current observations (historical UNCONFIRMED, NOT retroactive proof):
  sp11 Jev launch 270966B (Last-Modified Oct 28 2026 AFTER cutoff, P5 09-15 flagged), sp12 concepts 165512B, sp13 models 219035B, sp14 vLLM recipe 2705796B (pinned 09-20 unverified), sp16 HF modelcard 452330B + API 24520B (lastModified Oct 16 2026 AFTER cutoff, P5 09-10 flagged, captcha string is config not block), sp17 Dynamo dev MD 16535B (dev branch only).
- GitHub PR27742 via `gh` only (no raw HTTP): pr 26122B (merged True 2026-08-27, 65 commits/28 files, head eaf93765 base 732707df), commits 129618B (30/65 page1 partial), comments 66029B (30/144 page1 partial). Title actual `model: add Qwen3.8-Flash-Next (qwen4exp)` vs P5 descriptive - flagged as description, not mismatch.

Transport vs content: 40/40 HTTP200 exit0; content-verified 40/40 bytes+SHA (%PDF magic, <title>/keywords, JSON keys, MD). Transport200 != VERIFIED. Zero-byte: none. Single attempt per URL, no overwrite, no unbounded retry. All 17 unblocked retrieved, 0 unavailable.

## Identity / version-boundary flags (preserve, don't rewrite)

- P5 date mismatches: sp05 API 2026-04-12 vs P5 2026-08-24; sp06 2023-05-09 vs 2023-05-10; sp07 2025-10-30 vs 2025-10-29; sp09 2026-09-17 vs 2026-09-18; sp11 Oct 28 2026 vs 2026-09-15; sp16 Oct 16 2026 vs 2026-09-10. Actual API/headers govern, P5 preserved as claim.
- Historical CONFIRMED: 10/10 arXiv vN < cutoff. UNCONFIRMED: 7/7 living docs (current 2026-11-01 only). PR merge CONFIRMED (< cutoff) but commits/comments paginated PARTIAL (30/65, 30/144) - needs ?page=2.. if reviewer demands full.
- No 404/wrong-title/robot deny. All identity-match YES at intake level (title/URL/version/content-type/size/magic/keywords). Semantic coverage PENDING for all - needs independent Evidence re-review before any VERIFIED change. O05/O04/O11 rationale overstatements still open.

## Per-DID → body → review task (see manifest.json did_map FULL)

- D036 EAGLE v3 PDF → §5 results/guarantee/composability; D148 Snell v1 → §7 synthesis/comparison; D149 s1 v3 → §2-3 method/results/scope; D150 ThinkPrune v1 → §3.3/§5 schedule/table/eval; D151 overthinking v1 → §3.3/§5 flip/CI/cost; D154 FrugalGPT v1 → §4 Table3/pricing; D027 Kimi v2 → KDA/hybrid/NoPE/KV/license; D008 Qwen v1 → Tab.11/ratios/placement; D123 V4.1 v1 → arch/appendix/pins; D125 V3.2 v1 → DSA/parity; D070 launch current → arch/price/latency/eval quarantine; D071 concepts current → primitives/calibration; D141 models current → jev-1.13.0/alias; D163 vLLM current → floor/CED/Engram/layout/AMD; D165 PR partial → merged/QSA/PLE/validation/gaps; D030 card+API current → spec/MXFP/FP4/B200; D004 Dynamo dev → topology matrix.

No new Gate/schema/role, no State edit, no downgrade by file edit, no auto-VERIFIED.

## Files

- `DATA.*` (40) unchanged bytes + `*.headers.txt` (redirect final) + `*.stderr.txt` (curl -v redirect chain) + `*.command.txt`/`*.url.txt`/`*.time.txt` (start/end UTC)/`*.exit.txt`/`*.bytes.txt`/`*.sha256.txt`/`*.argv-extra.txt`/`*.pid.txt` + `*.stdout.raw` for gh (split to headers/body). No token logs.
- `manifest.json` readable per-DID + per-gid results + counts + gaps + worklog. SHA all payloads, PR head/base + HF sha, arXiv version IDs.
- `fetch-phase1.sh` (30 metadata/living/PR) + `fetch-phase2.sh` (10 version-pinned PDFs).

Worklog: 40 requests, 21054963B, ~66s network 16:35:36-16:36:42Z 2026-11-01 + verification/manifest. Recurring research cost UNKNOWN (no synthetic baseline per CORR C3).

Return: actual success 17/17 bodies (10 CONFIRMED historical + 7 current UNCONFIRMED), 0 unavailable, 0 failed transport. Exact raw locations in this dir. Version gaps above. Additional permission only if reviewer demands PR pages 2+ or pinned living-doc revisions outside 17 (none fetched, exact need to be stated).
