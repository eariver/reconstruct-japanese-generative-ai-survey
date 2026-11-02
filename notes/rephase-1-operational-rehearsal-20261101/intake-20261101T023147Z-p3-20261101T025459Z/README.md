# P3 intake — REQUIRED primary Raw closure (fixed refs, no overwrite)

Owner: General, material/network-data only. No source/runtime/test/build/fixture, no current checkout/Git readback/code adoption, no subagents.
Refs: W34 `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, SP `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`. Frozen 138 code authority; `.py` DATA never executed.
Dir: `intake-20261101T023147Z-p3-20261101T025459Z` (prefix lineage, suffix actual UTC 025459Z honest; per-GET UTC in `*.time.txt` governs, no invented ordering). Old scripts NOT rerun.

## Why P3 (Root-selected pre-Architecture, not metadata)

P2 `README/ready-sufficiency` proved transport (hashes/counts) for the State-selected dossier, NOT raw validity/semantic assessment — corrected to **transport-partial** (P2 README correction appendix, preserved). P3 examines actual selected Root/E JSONL Raw/source paths + supplement refs, fetches ONLY required primary Raw bytes in those records:
- W34: 55 discovery `raw_paths` (all under `sources/2026-W34/`, no W33/other-edition ref → no broad W33 read; exact need if external: none) + bibliography audit + `official-provenance.jsonl` + working-set inventory + sol decision + `jgaisurvey.sty` for render/biblio/provenance checks. Carryover ledger already in P2 (reused, not recopied).
- SP: discovery 25 refs = 24 `raw/` obs +1 `external/x/.../x-reception-result-r3.md`; 25 obs already in P2, x-reception fetched here. Interactive 160 `source_bindings` refer to arXiv IDs/external publisher bodies (not repo files) + supplement 13 raw (already in P2, 1,275,978B verified) + 25 obs; full publisher bodies are external web (new publisher URL network = new permission, NOT fetched). If fixed tree lacks full-body record → record UNAVAILABLE, no completeness claim from metadata.
- No 800-card shards (aggregated evidence/views already full 409/160 coverage), no 3351 dump, no 450 worklogs. Fresh reaccept uses full aggregates + original input; Raw + root/effective/script INPUT exact closure prioritized.
- Worklogs: small rationale set only (bib audit + official-provenance + sol decision + P2 validations/sessions/index); cost remains UNKNOWN.
- W34 article identities provenance-checked by fixed tree/api blob + acceptance refs (12/12 match, §2), no stale index paths.

## What was fetched (63 GETs, all `exit 0` `HTTP 200`)

- `acquire-p3-raw.sh` (59: W34 54 new Raw +5 provenance/sty/bib + SP x-reception). All under selected roots.
- 4 large (>1MB) via exact-blob API from fixed tree SHAs (contents API metadata-only): `p3b31/34/36/37` (`2fd387fe...`/2479649B, `4e19a711...`/1612070B, `d3b5ea7e...`/1996383B, `0f83d2c2...`/2532040B). `DATA.p3a31/34/36/37.*` now hold blob bytes; `p3b` duplicates removed to avoid double count (see `manifest.json` note).
- Per-GET `command/url/ref/time/PID/stdout.raw/headers/body/exit/stderr` + decoded `DATA.*` (hash/blob/size verified). No tokens. No 404/fallback/rate-limit. No W33 read. No new publisher network.

## Verification + timing correction

- Every file: `len==reported size` + `sha1(blob len\\0+bytes)==reported blob` (+ `sha256`). Listings preserved. `manifest.json` (multiline) details all 63 + cumulative matrix (P1/P2 reused, no recopy) + root mapping + missing parts.
- P2 ready → transport-partial until raw validity + semantic assessment complete (execution owner + baseline assessor judge on captured bytes; no quality-ready/adoption claim from hashes).
- Naming: `023147Z` prefix = lineage to P1; P2 suffix `024051Z`, P3 suffix `025459Z` = actual invocation starts. Per-GET `*.time.txt` is authoritative; directory names do NOT order requests.

## Return

- `manifest.json` (all GETs/full responses/ref/blobSHA/bytes/hash results) + `cumulative-matrix.md` (prior captures, no recopy) + `data-root-mapping.md` (execution-owner paths) + `remaining-requirements.md` (missing parts, not quality-ready).
- Stop at bounded completion/blocker; no broader intake. SP PDF/tex/bib already permit baseline read; W34 PDF/manuscript reused by exact SHA.
