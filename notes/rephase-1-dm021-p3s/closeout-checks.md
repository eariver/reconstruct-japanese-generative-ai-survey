# DM021-P3S closeout checks — final readonly consistency (2026-10-19 UTC)

**Astra annotation:** the original header's `2026-10-19 UTC` is a timezone-label error; use **2026-10-19 JST** for this closeout. Root subsequently observed UTC `2026-10-18T16:02:14Z` (=2026-10-19 01:02:14 JST). This later clock observation does not reconstruct an exact earlier check timestamp. Original header and machine summary are preserved. The two doc-only findings in §5 were subsequently corrected in assessment/README; the checks remain the recorded pre-correction observations.

Co-Worker readonly verification. No tests, no candidate imports, no runtime execution,
no Git writes, no network, no production inspection. Method: `Read` + `sha256sum`/`stat`
(no pyc execution) + `git --no-pager` rev-parse/symbolic-ref/status/diff/check-attr +
`find` walk of `notes/rephase-1-dm021-p3s`. Only `closeout-checks.json` + this file created.
Companion machine record: [closeout-checks.json](closeout-checks.json).

**Hash-suffix note:** static21 file SHA256 is `1c0e339c…ef1a5` (full
`1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5`);
`…9df3472` is the contract42eb suffix
(`42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472`), not static21.

## 1. File rehash (exact)

| File | SHA256 | Size | Verdict |
|---|---|---:|---|
| `outputs/rephase-1-dm021-staged-source-contract-decision.md` | `42eb8dbb…9df3472` | 19547 B | MATCH |
| `notes/rephase-1-dm021-p3s/draft-history-r11/static21.json` | `1c0e339c…ef1a5` | 3670 B, 21 entries | MATCH |
| `gen-complete21/complete-p3s-21path.patch` | `e449d029…3012fa` | 1233670 B | MATCH (`.sha256` + proof stdout) |

## 2. Live source identity (sanitized checked Git, read-only)

- Active `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`:
  detached HEAD `409b292…`, tree `8ce36998…`, index empty,
  full status **105 rows** (`3 M` + `102 ??` = 18 new source + 84 caches).
  Collapsed porcelain shows 23 lines (3 M + 20 ??); 105 needs `--untracked-files=all`.
- Apply `/tmp/opencode/jgas-p3s-final-20261018T154812Z/proof-apply21-clean409-copy`:
  detached HEAD `409b292…`, tree `8ce36998…`, index empty,
  status **21 rows** (`3 M` + `18 ??`, no caches) — confirms supplement §5
  (applied-21, not 105; 105 is the active-tree census).

## 3. Live byte rehash (my current observations — see scope)

- ACTIVE21 vs static21: **21/21** sha256+bytes+mode(0o664) match.
- APPLY21 vs static21: **21/21** match — my own live rehash of the apply copy,
  distinct from the independent reviewer's recorded-freeze comparison (§5).
- Active84 caches vs P2R `cache-inventory-static.json`: **84/84** match, 0 missing
  (readonly byte hash; no pyc executed).
- Recorded applied-freeze `files` vs static21: **0 mismatches** (recorded-guard
  comparison); freeze status 21 rows; clean freeze `new_absent` 18 /
  `modified_match_head` 3 / `caches_removed` 84 / head+tree 409/8ce / empty status+index.

## 4. Packet / docs / workspace

- `notes/rephase-1-dm021-p3s` walk: 0 nested `.git`, 0 symlinks, 0 FIFO/socket/device,
  0 other non-regular entries; walk errors none.
- `git check-attr text`: `unset` (-text) for packet README, closeout, new assessment,
  staged-source contract. New docs: no trailing-whitespace lines.
- Current-entry links: **232/232** local markdown targets resolve across the 9 new/updated
  docs; AGENTS current-entry paths **8/8** exist. Assessment new3 table identical to
  static21; no applied-105 claim in new docs.
- Workspace HEAD `6dcbb89` (`6dcbb89bb08…a722`), no index staging,
  `git diff --check` clean; diff touches only the 8 allowed tracked files + 2 new files.

## 5. Doc-only defects for root correction (no edits made)

1. Assessment §3 (~line 55) “checked applied21 vs static21 with 0 mismatches” does not
   name the recorded-freeze basis — suggest §5 wording (“recorded applied21 freeze
   0 mismatches”).
2. Packet README correction list (line 8) does not name §5’s applied-freeze-21-rows or
   live-rehash-scope corrections — root decides whether to extend.

## 6. Scope

Current-hash proof only. Historical per-run assurance (scoped26 batches, oracles,
failures, provider/tooling records) stays with the root closeout + independent
review/supplement, whose failing/raw/historical text is preserved. Counts (26 distinct,
SIX double-pass O11d+O12b–f, R1 only at R11, 8 batches) are cited per that census, not
recounted from headers here. Not a runtime suite or full audit.
