# P4 — integrity fix (6 github Raw via exact blob) + X-manifests + X tasks (same fixed refs)

Owner: General, material/network-data only. No source/runtime/test/build/fixture, no local checkout/Git readback/code adoption, no subagents. No overwrite of P1/P2/P3 originals; P3 zero DATA preserved as fault evidence.
Refs: W34 `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, SP `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`. Frozen 138 code authority; `.py` DATA never executed.
Dir: `intake-20261101T023147Z-p4-20261101T031826Z` (prefix lineage, suffix actual UTC 031826Z honest; per-GET `*.time.txt` governs, no invented ordering).

## Hold reason (packet README Current integrity hold)

P3 `data-root-mapping.md` rows `p3a02`–`p3a07` listed 0-byte DATA (`sha256 e3b0...` empty) while recorded Git blob IDs are non-empty (empty blob would be `e69de29...`). Blanket “required Raw closure verified” NOT accepted. Pause consumption of those 6 files.

## Actual reason (investigated, not guessed)

P3 `p3a02`–`p3a07` contents-API bodies are **metadata-only**: `encoding:"none"`, `content:""` (len 0), `size` = 1805968/5257525/1323799/1854867/1839084/3340585, `sha` = non-empty blob IDs. GitHub contents API omits `content` for files >1MiB (returns metadata + `encoding:none`). P3 procedure base64-decoded `""` → 0 bytes and wrote fake empty DATA (protocol fault: HTTP200 ≠ content acquisition; empty payload ≠ valid Raw, ≠ repo quality issue). Same pattern for `p3a31/34/36/37` (>1MiB) — already supplemented in P3 via exact-blob `p3b31/34/36/37` (now verified, preserved).

## Fix (NEW unique P4 files, genuine HTTP/raw exit, no overwrite)

- 6 exact-blob GETs from fixed P3 path metadata (774 selected Raw, no new ref): `p4a02` (`90462213...`/1805968B), `p4a03` (`62edff35...`/5257525B), `p4a04` (`daa04d86...`/1323799B), `p4a05` (`6b093886...`/1854867B), `p4a06` (`f16c5ec6...`/1839084B), `p4a07` (`94aaa506...`/3340585B). All `exit 0` `HTTP 200`, `len==reported size`, `sha1(blob len\\0+bytes)==reported blob`, full `sha256` in `manifest.json`.
- 2 X-manifests (same authorized refs, no new permission): `p4x01` W34 `x-source-intake-v2.json` 3913B `113d62e7...`, `p4x02` SP `x-source-intake-v2.json` 5359B `638ea4af...`. Both `exit 0`.
- 2 X tasks (manifest-referenced data refs, same refs): `p4x03` W34 `grok-task.md` 11686B `2d6c607b...` (== manifest `e97bbd06...`), `p4x04` SP `grok-task.md` 20555B `c9a04eb6...` (== manifest `c1150730...`). Both `exit 0`.
- X result raws already present: W34 `grok-x-result.corrected.md` 23612B `43b0923b...` (P3 `DATA.p3a51...`, == `p4x01` manifest), SP `x-reception-result-r3.md` 30213B `b3a8a040...` (P3 `DATA.p3a59...`, == `p4x02` manifest). Validated, no refetch (avoid recopy).
- Transport vs content: **transport 10/10 HTTP200 exit 0**; **content-verified 10/10** (`len+blob+sha256`). Zero-byte payloads (P3 6) are NOT counted as content-verified.

## Cumulative mapping (original → NEW verified payload)

See `supersede-mapping.md` (full hex hashes, readable): each P3 failed `repoPath@774` → P4 `DATA.p4a0*` verified bytes; P3 zero DATA explicitly **SUPERSEDED UNAVAILABLE** (preserved, not consumed). P3 `p3a31/34/36/37` already blob-fixed in P3 (preserved, verified). No fake empty fallback.

## Corrections

- P2 “dossier ready” = transport-partial until raw validity + semantic assessment (P2 README correction preserved). P3 blanket “full shards need new permission” line is WRONG and superseded here: **task/batch/result shards at the same fixed refs share the same user authorization** (no new Human question); only new publisher URLs / new ref / separate asset not in fixed tree need new permission.
- Package counts from actual artifact arrays (not manual transcription): W34 `architecture-v2.json` 7 packages (`w34-agent-control-plane`, `...-workflows-retrieval`, `...-safety-security-governance`, `...-model-economics-distribution`, `...-creative-multimodal-production`, `...-ecosystem-infrastructure-economics`, `...-week-in-review`); SP `architecture-v2.json` 9 packages (`p1-bottleneck` … `p9-measure`). Packet README hold (§ baseline graph count correction) is authoritative.
- Timing: `023147Z` prefix = P1 lineage only; P2 suffix `024051Z`, P3 suffix `025459Z`, P4 suffix `031826Z` = actual invocation starts. Per-GET `*.time.txt` (actual UTC) governs.

## Coverage (partial/complete, not blanket)

- Complete (verified bytes): W34 55/55 discovery Raw (49 via contents +6 via P4 blob; carryover already P2) + bib audit + official-provenance + working-set + sol decision + sty (12/12 article identities match manuscript/tree); SP 25 obs + supplement 13/13 (1,275,978B) + supplement manifest + interactive orig/r2 + screening/evidence/views/ledger/completeness/matrix/selection/arch + publication 10 + reader tex/bib/PDF + X manifests/tasks/results (see `manifest.json` + P2/P3 manifests).
- Partial (inventoried, bytes NOT fetched): W34 per-task shards (409+409, aggregated covers), screening batches/results intermediates, collector run metadata beyond referenced raws, execution 450 worklogs (small rationale set only); SP per-task shards (160+160, aggregated covers), screening input/results subdirs, execution 20+ dirs (small set only); full publisher bodies (arXiv PDFs/web, external — new permission, not fetched); TeX log, eyed visual proof, wall/LLM cost (UNKNOWN).
- No W33/other-edition ref found in selected records (all W34 under `sources/2026-W34`, all SP under `sources/SP-efficient-llm-2026`); no broad W33 read performed. If execution needs sharded bytes at same fixed refs, same authorization applies (no new question).

## No further primary fetch needed for referenced repo Raw (path coverage demonstrated in `cumulative-matrix` P3 + `manifest.json` here). Stop bounded completion here; no broader intake, no runtime/tests/fixtures/shipping changes. Second checker audits P1/P2/P3 data separately (not duplicated here).
