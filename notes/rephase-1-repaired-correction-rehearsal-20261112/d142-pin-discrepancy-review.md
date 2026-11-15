# D142 pin discrepancy — independent DATA review (NEW, no author edits)

Scope: actual SP dispatch `cli-prepare-SP-20261113T140724Z` failed before ANY writes with
`REFUSE: SP D142 pinned drift` at `prepare-normal-high-r3.py:648`.
This is a NEW independent DATA pin investigation only.
No project runtime/imports/Git/network/Production/active writes/subagents.
Only stdlib `hashlib`/`json` reads + these two new packet files.
No edits to author files. No fix/retry/cleanup.

## 1. Failure point (actual operator conditional, not fabricated cause)

- Outer: `prepare-normal-high-r3-SP-20261113T140724Z-outer.exit = 2`,
  `stderr = REFUSE: SP D142 pinned drift`,
  `traceback.txt` → `prepare-normal-high-r3.py line 648 in main → fail("SP D142 pinned drift")`.
- `stdout.txt` stops after `routing keys [...]`; u1/u2/u3 passed, D142 check is next.
- `cwd.txt = /home/eariver/git/reconstruct-japanese-generative-ai-survey`.
- `argv`: `--repo-root .../.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
  (absolute), `--config notes/.../prepare-normal-high-config-r3.json`,
  `--outdir .../prepare-normal-high-r3-SP-20261113T140724Z-outer`.
- Wrapper code (read-only, lines 635–649):
  `d142 = rout_doc["d142_summary_routing"]`,
  required keys `existing_file, existing_sha256, existing_bytes, future_raw_path, first_claim_literal`
  all present (types: string, string-64hex, int, string-safe-rel, string).
  `src142 = Path(d142["existing_file"])` (workspace-relative with leading `.rephase-...`).
  Containment `src142.resolve().relative_to(repo.resolve())` passes because CWD is workspace root,
  so `src142.resolve() = <repo>/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`,
  same physical file as entry-inventory `repo/sources/...`.
  Then:
  `if sha256_file(src142) != d142["existing_sha256"] or src142.stat().st_size != d142["existing_bytes"]: fail("SP D142 pinned drift")`.
- Size matches (3751 == 3751). SHA is the sole discriminator.
  No source mutation occurred; zero SP Raw/request/supplement/R created (outer report §10 + machine `writes_stopped_after`).

## 2. FULL 64-char hashes + sizes (programmatic, not prefix-only)

Routed expected (`sp-repaired-raw-routing-map-r4.json`):
- `existing_file = .rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`
- `existing_sha256 = f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718662662` (64 hex)
- `existing_bytes = 3751`
- `future_raw_path = sources/SP-efficient-llm-2026/external/evidence-supplement/raw/sp17-EFF-D142-summary-captured-20260921.md`
- Routing file itself: 4061B `d8e10ea0d97a88e55f7b5f4f997242e4ed133c1d2b5dbdae25757f17804e31a8` matches config-r3 pin (packet file intact; error is inside its `existing_sha256` value).

Actual bytes (stdlib `hashlib.sha256(read_bytes()).hexdigest()` + `st_size`):
- NEW cc1c: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`
  `3751B f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662 mode 0o664`
- OLD e84: `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`
  `3751B f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662 mode 0o664`
- P2 captured DATA: `notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c33.discovery-observations-r2-g19-g20-data-jev.md`
  `3751B f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662 mode 0o664`
- Entry-inventory extra: `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`
  `["f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662", 3751, "0o664"]`

Diff (full-string compare):
- `actual (...18672662)` vs `routed (...18662662)`: single-char diff at index 59 (0-based): `7` vs `6`.
  Prefix `f7eeec68` identical, which is why outer `execution-report.md:11` ("matching routing pin")
  and machine `precise_exception` ("match f7eeec68/3751") are prefix-only and hide the typo.
  Full 64-char comparison fails, triggering the wrapper refusal.

## 3. Immutable capture provenance (no fetch, captured scope only)

- P2 `manifest.json` gid `p2c33`, label `SP-raw-obs-r2-g19`:
  `repo_path sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`,
  `ref c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`,
  `reported_blob_sha 0c1d507be945b1cf38d8afbee0be8aaf8b0a623b`,
  `reported_size 3751`,
  `data_files[0] = DATA.p2c33... bytes 3751 sha256 f7eeec68...18672662`.
  Computed P2 DATA bytes match manifest (3751 + full hash).
- P5 `did-bodies.md`: same path `@c8 blob 0c1d507b... 3751B sha256 f7eeec68...18672662 (P2 DATA.p2c33..., reused no recopy)`.
- Explore inventory `sp-jev-authority-inventory.md:97`: `3751B f7eeec68...18672662` — matches provenance.
- Expected manifests `sp-prepare-expected-manifest-r5/r6-20261104.json`, `r7-D165fix-20261105.json`, P2 `DATA.p2b21...`, P2 `manifest.json`: all `...18672662`.
- Jev-archive intake `intake-20261106T001808Z-jev-archive/manifest.json` (4289B) covers only u1/u2/u3 (3 index + 3 body, no API fetch); D142 correctly absent there. No new fetch performed here.
- Git blob `0c1d507b...` cited from manifests only; no `git` invocation per task bounds.

Old e84 == new cc1c == P2 DATA == entry-inventory == provenance (`...18672662`).
No evidence of source drift/mutation.

## 4. Other hash variants (for root triage, not authority)

- `sp-candidate-map-r2/r3.json`, `sp-essential-gap-map.json`: 62-char malformed
  `f7eeec6872fa7dd9ad8f8fb80adfb9e2ff2bab571ffff807c2d34718662662` (len 62, invalid SHA256).
  Explore transcription error, not a pin; do not use as authority.
- Current author r4 chain (`sp-repaired-raw-routing-map-r4.json`, `sp-repaired-records-4-r4/r5/r6.json`,
  `sp-repaired-patch4.json`, `reviews/sp-correction-proposal-review.md` + machine JSONs):
  all carry `...18662662` (64-char, single-digit typo). Includes D142 new-record `claims[0].context`
  provenance string `3751B sha256 f7eeec68...18662662`.

## 5. Verdict

`TYPO_DATA_CORRECTION` (not `UNKNOWN_DRIFT`).

Reason: actual bytes are tied to immutable capture provenance across three independent byte sources
(old e84, new cc1c, P2 DATA) plus manifest/blob/size metadata, all `...18672662`/3751.
Routed `...18662662` is a single-digit transcription error at index 59.
Wrapper correctly refused on full-hash mismatch; prefix-only "match" claims in execution reports are superseded.

## 6. Required next (not done here)

- Hash in D142 new-record context (`sp-repaired-records-4-r4/r5/r6.json` + patch/reviews) is also wrong
  (`...18662662`) and needs NEW r7 DATA + root review. No edits made here to author files.
- Routing `existing_sha256` needs author correction via normal correction path with fresh root/independent review;
  do not blind-repin drift. No R4/generic-reader/Production/commit/readback authorized here.

Files read: `cli-prepare-SP-20261113T140724Z-execution-report.md` + `-machine.json`,
`prepare-normal-high-config-r3.json`, `sp-repaired-raw-routing-map-r4.json`,
`sp-repaired-records-4-r4.json`, `prepare-normal-high-r3.py:635-649`,
outer `argv/cwd/exit/stdout/stderr/traceback/entry-inventory.json`,
`sp-jev-authority-inventory.md`, P2 `DATA.p2c33...` + `manifest.json`, P5 `did-bodies.md`,
jev-archive `manifest.json` + `independent-content-review.md`, `sp-read-scope-and-pins.json`.
Method: stdlib hash/JSON only.
