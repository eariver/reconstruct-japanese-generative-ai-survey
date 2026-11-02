# P6 — W34 r2 supplement manifest + 425 distinct Raw closure (same fixed 774, no publishers)

Owner: General, material/network-data only (Git read-only `gh` API). No runtime/import/build/fixture/code adopt/old-script rerun/source edits/Git readback, no local checkout/general main/other ref/external publisher network, no subagents. No overwrite of P1–P5 originals; P3 zeros + P4 fixes preserved.
Refs: W34 ONLY `774dd39a951c9ac3818e83dfffd4c7666efb0a20` (SP external permission separate; no SP fetch here, no publishers). Frozen 138 authority; `.py` DATA none in P6.
Dir: `intake-20261101T023147Z-p6-20261101T115240Z` (prefix lineage, suffix actual 115240Z honest; `*.time.txt` governs).

## Why (operator exact gap)

Execution `w34-narrow-check-35.py` + P2b18 (409 records, `3ffc6e31...`, 8 unbound `c035/c038/c051/c054/c057/c058/c065/c103`) require 428 distinct `supplement-src` IDs; old P2d01 r1 manifest (61 entries, 50490B) is WRONG basis (needed−old = 428, 0 overlap; stale discovery `9bfc0fc9...`/screening `5692a79a...` vs fresh `0a23be47...`/`e193ad05...`). Runtime W34 still `CANDIDATES_NORMALIZED`, no Evidence products. Exact missing manifest `sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-authority-supplement.json` @774 blob `88f5f3379f5dc8435ab16a21126ab7550b2c06fd` size 389423 (tree.json 774 confirms) fetched first, then exact referenced Raw closure.

Prior 61→428 correction by append here (old r1 files preserved, NOT amended; new r2 manifest as DATA comparison remains old accepted proof, NEVER new active basis — current rehearsal Supplement builder will create NEW basis later).

## What was fetched (genuine HTTP/raw, failclosed, bounded parallel)

- `p6a01` r2 manifest 389423B `88f5f337...` (contents base64, `len==size`, `sha1(blob)==blob`, `sha256 0fada5df...`). 428 entries.
- 425 distinct Raw (dedupe `fullpath+sha256`: 428 entries → 425 distinct paths+SHAs; 3 exact dupes) — 190385403B all → 188897330B distinct. No 800 shards/all-versions dump. All under `sources/2026-W34/` (0 outside → no STOP needed).
  - `p6b01–425` contents API (394 small <1MiB with base64 DATA verified `len+blob+sha256==manifest`; 31 large >1MiB `encoding:none` metadata-only, 0-byte NO DATA — failclosed, distinct count, NO fake empty).
  - `p6cXXX` exact-blob API for those 31 (blob SHA from fixed path metadata, `len+blob+sha256` verified). Total P6 GETs 1+425+31=457, all `exit 0` `HTTP 200` (transport).
- Bounded parallel `max_workers=4` (dedupe 425, hard limit 4, no duplicate rates); genuine `command/url/ref/time/PID/stdout.raw/stderr/exit/headers/body` per GET, NO hand-constructed logs.
- Reuse P1–P4: 0 bytes (evidence-bodies paths are new; discovery 55 + supplement r1 + 13 raw + X already verified, not recopied). Duplicate reuse 0/425.
- Transport vs content: transport 457/457; content-verified 426 DATA (1 manifest +394 small +31 blob) 189286753B; metadata-only 31 (transport-only, supplemented). Zero-byte DATA: none in P6 (failclosed). P3 6 zeros preserved as fault (P4 superseded, NOT reused). No `transport200==content`.

## Verification (no historical authority certification)

- P2b18 bindings (428 IDs) == P6a01 source_ids (428 IDs), 0 diff; 8 unbound records have no bindings (listed, not forced). DID mapping: `discovery_id`/`evidence_task_id` match P2b18 (e.g. `w34-event-arxiv-2608-14927` → `supplement-src-aae133...`), NO arbitrary new labels. `source_type`/`source_class`/`relation`/`title`/`locator` preserved from manifest (e.g. `arxiv_primary`/`PRIMARY_PAPER`/“primary paper body inspected…”, `official_publisher_page`/`PRIMARY_OFFICIAL`, etc.); Disclosure/body-kind/class unchanged.
- Raw kind honest: P6 bodies are publisher full HTML (411) / PDF (12, e.g. `2608_17605.pdf` 3860219B) / JSON (2, e.g. CISA feed) — primary bodies, NOT obs summaries (`discovery-observations-*.md` 55, P3) NOR arXiv abstracts. Having bytes ≠ VERIFIED (needs independent Evidence semantic review per governance §4.2).
- Counts: 428 entries, 425 distinct path+SHA (3 dupes), 425 files, 188897330B distinct (190385403B with dupes). NOT 61, NOT count-only (full bytes verified).
- W34 packages 7 (actual `architecture-v2.json` array, P2; SP 9 separate, not conflated — P4 correction preserved).

## Output for operator (no reread 599 files)

- `manifest.json` (multiline, 457 results, full HTTP/ref/blob/size/hash/body records).
- `supplement-mapping.json` (425 rows: `repo_path` @774 → verified `local DATA` + `git_blob_sha` (full) + `content_sha256` (full, == manifest `raw_sha256`) + `bytes` + `supplement_ids` + `locator`/`source_class/type` + disclosure kind). Full hex, no truncation. Use directly; no manual reread.
- `DATA.p6a01...` (r2 manifest) + `DATA.p6b*/p6c*` (425 bodies). Old r1 (`DATA.p2d01...`) preserved, NOT active basis.
- Remaining: semantic Evidence review (11 VERIFIED + loadbearing PARTIAL body-consumption per SP hold is separate target; W34 Evidence run awaits Supplement re-basis + independent review). No new publisher fetch needed for referenced repo Raw (complete here); external publisher bodies beyond repo (if any) need separate Human URL-by-URL permission (none attempted). No runtime/tests/fixtures.
