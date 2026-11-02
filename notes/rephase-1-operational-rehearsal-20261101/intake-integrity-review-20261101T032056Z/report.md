# Intake-integrity review — P1/P2/P3 DATA vs original API response (independent)

Review dir: `notes/rephase-1-operational-rehearsal-20261101/intake-integrity-review-20261101T032056Z/`
Role: fresh independent DATA-integrity checker, not intake/execution author.
Bounds observed: no network, no Production checkout, no `git` commands/readback,
no project runtime/import/tests/build/fixtures, no source/manifest edits, no subagents.
Only NEW files in this dir; intakes not overwritten; P4 (`...-p4-20261101T031826Z/`)
not read/edited/fetched (race avoidance).

## Evidence (exact)

- `check_intake_integrity.py` SHA256 `80f6e75389a335ddaec67bf0b83878c080aa8477a856cdef204ba27f25153255` / 21593B
  stdlib only: `hashlib/json/base64/pathlib` (+`sys` for fail-closed exit). No `assert`.
  Git blob = `sha1(b'blob '+len+'\\0'+bytes)`. Base64 helper strips GitHub LF then
  `validate=True` (fail-closed, no silent skip).
- `check_file_links.py` SHA256 `148e84580f1fcc1d7e02a19a211312b2353590f7b9d31077c6ad3f0951b1e9c0` / 8406B
  same stdlib discipline. Walks all `DATA.*.json` for `{path,sha256[,byte_count]}`
  under `sources/`/`surveys/`, compares to captured map; `candidate_sha256`-style
  semantic digests (no `path`) are correctly ignored as non-FILE refs.
- `checker.stdout.json` SHA256 `68b0c4325b4ed4813f07498dc8fbc81c1daf3704a208c61ecfc15e3bf05ab7fc` / 2387B,
  `checker.exit.txt` = `1`, `checker.stderr.txt` = 0B.
- `checker.stdout.v1-base64-newline-fault.json` (preserved script fault): first run used
  `base64.b64decode(...,validate=True)` on raw GitHub content with LF every 60 chars,
  flagged 200+ false `Only base64 data is allowed`. Fixed to strip whitespace then validate.
  V1 preserved; V2 above is authoritative.
- `links.stdout.json` SHA256 `2e3a72581a5b7ad9f49520ad6ca7bddcc49e1fd082c87a8629c881eb57d164a5` / 53974B,
  `links.exit.txt` = `1`, `links.stderr.txt` = 0B.
- Exits are fail-closed: `1` = NEEDS_REPAIR/mismatch present, not checker crash.
  No `assert`-disable loophole (no `assert` in scripts).

## Transport vs content (verified, not authored counts)

Authored manifest `successcounts` (`6/6`, `179/179`, `63/63` HTTP200 exit0) are transport
only. This review decoded every body independently:

- P1 (`intake-20261101T023147Z`): 6 GETs, 6× exit0 + `200` + empty stderr.
  4 file bodies (`get01,02,04,05`) base64 → `len==size` + `git-blob==sha` + `DATA==raw`
  + `sha256==manifest` all PASS. 2 listings (`get03` 20 entries, `get06` 3 entries)
  are JSON arrays, correctly with no DATA — metadata-only, expected.
  No `encoding:none`, no 0-byte DATA, no wrong edition/ref.
- P2 (`...-p2-20261101T024051Z`): 179 GETs, 179× exit0 + `200`.
  145 DATA files, all base64 bodies decode PASS after whitespace fix.
  34 zero-DATA GIDs are ALL `listing:*` directory arrays with
  `reported_size/blob=null` — metadata-only, expected, not missing bytes.
  No `encoding:none`, no 0-byte DATA file. 3 blob-API supplements
  (`p2a30` SP PDF 850785B, `p2b18` 1573186B, `p2b19` 1335444B) decode PASS.
- P3 (`...-p3-20261101T025459Z`): 63 GETs (59 contents +4 blob), 63× exit0 + `200`.
  53 contents base64 PASS. 4 large `encoding:none` correctly supplemented via blob
  (`p3a31↔p3b31` 2479649B, `p3a34↔p3b34` 1612070B, `p3a36↔p3b36` 1996383B,
  `p3a37↔p3b37` 2532040B): `DATA==blob-decoded`, `size/blob/sha256` all match.
  6 contents `encoding:none` with NO supplement are NEEDS_REPAIR (below).
  P3 has no directory listings.

HTTP200 + `encoding:none`/empty `content` is metadata-only, NOT byte acquisition.

## NEEDS_REPAIR — missing/truncated/misbound (beyond listings)

Only 6, all already known `p3a02–07`, no other missing/truncated/misbound found
in P1/P2/P3 file bodies. Do not trust `data-root-mapping.md` blanket
“required Raw closure verified” for these rows.

| ID | ref | repo-relative path | blob (expected git SHA) | expected size | actual size | actual SHA256 | captured failure indicator |
|---|---|---|---|---|---|---|---|
| p3a02 | `774dd39a...` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json` | `90462213d9825c9224a0b169d753f023dcf18537` | 1805968 | 0 | `e3b0c44298fc...` (empty) | `p3a02.body.json`: `encoding:none`, `content:""`, `size:1805968`; `DATA.p3a02...` 0B empty-SHA; manifest correctly records `bytes:0`; no `p3b*` supplement |
| p3a03 | `774dd39a...` | `.../raw/ggml-org__llama.cpp.json` | `62edff35562c0eaa4d175546364b1c2838a11a3a` | 5257525 | 0 | `e3b0c44298fc...` | same pattern |
| p3a04 | `774dd39a...` | `.../raw/huggingface__transformers.json` | `daa04d862800fc51c3066a2b3e2f53ff96394992` | 1323799 | 0 | `e3b0c44298fc...` | same pattern |
| p3a05 | `774dd39a...` | `.../raw/nvidia__tensorrt-llm.json` | `6b093886cc5cf29de0c3ebe55bb907de9c64bad3` | 1854867 | 0 | `e3b0c44298fc...` | same pattern |
| p3a06 | `774dd39a...` | `.../raw/sgl-project__sglang.json` | `f16c5ec6b2a24a09e7f76dd5fd7ca8e555d30587` | 1839084 | 0 | `e3b0c44298fc...` | same pattern |
| p3a07 | `774dd39a...` | `.../raw/vllm-project__vllm.json` | `94aaa50674ab67014d4b0a0030c00af752df7c87` | 3340585 | 0 | `e3b0c44298fc...` | same pattern |

`Content-encoding:none`/empty API content for large files is NOT zero-byte Raw.
Valid zero blobs would require `blob==e69de2...` (empty blob); here blobs are
non-empty, so 0 bytes is confirmed missing. Intake owner now repairs 6 in NEW P4;
this review does not race edit/fetch P4. P4 must validate BOTH `blob SHA`
(above) AND content `sha256` from discovery (next section).

No other P1/P2/P3 file has `encoding:none`, 0-byte DATA, `len!=size`,
`git-blob!=sha`, `DATA!=raw`, cross-edition ref, or `url`-without-`ref`.
`checked_files:208, listings:36, blob_apis:7, errors:[]` in `checker.stdout.json`.

## Metadata-only rows vs valid zero blobs

- All 2 (P1) + 34 (P2) listings are `list` bodies with `listing:N entries`,
  each entry has `path/sha/size`; manifests correctly use `reported_size/blob=null`
  and zero `data_files`. These are availability metadata, not byte closure —
  must not be counted as Raw proof.
- No valid zero-byte Raw file exists in P1/P2/P3 (no `blob e69de2...`).
  Every 0-byte DATA in P3 is one of the 6 above with non-empty blob → NEEDS_REPAIR.

## FILE sha refs vs captured bytes (760 links)

`links.stdout.json`: `links_checked:760, matched:628, unacquired:119, archived:2`.
119 UNACQUIRED = path has no captured DATA in P1/P2/P3 (e.g. W34
`reader-manuscript-v2.json`/`main.pdf`/`quality/semantic/visual`, sharded
evidence/views, `main.log`, publisher bodies). Per instruction these are
NOT called invalid — bytes remain at fixed refs if needed, separate permission
only for new ref/asset/publisher web.

13 MISMATCH (exact):

1. 6× `DATA.p2b02.discovery-accepted-v2.json` raw_refs to the same 6
   github-releases paths above want content-sha256
   `f75febae.../80345df9.../2a843332.../d711b2eb.../acab64f7.../75f34b03...`
   (byte_counts 1805968/5257525/1323799/1854867/1839084/3340585 match P3 sizes)
   but captured DATA are the 0-byte placeholders. Same root cause as NEEDS_REPAIR,
   with independent expected content hashes for P4 validation. P4 bytes must satisfy
   BOTH `sha256==discovery-want` AND `git-blob==body-sha` (`9046...` etc.;
   verified pattern on `p3a01`: want `257bbf...` == DATA `257bbf...` with blob
   `ea11...`).
2. 6× `DATA.p2a17.DRAFT_COMPLETE.json` (SP, `recorded_at 2026-09-22T19:10:00Z`,
   DRAFT-stage) artifacts want `08c0e358.../f99c3b93.../417e49ac.../c60513eb.../b09ab351.../c4ae1c38...`
   (+ `bc6e280c...` PDF in same file) but current files at `c8` are final
   (`a3f1b649.../cf7aca20.../d5c95b52.../6f5e7ff1.../87bcb707.../fae79e67...`,
   PDF `8a9a721a...` 850785B). This is documented supersession
   (P2 README §16: DRAFT manuscript/PDF superseded by candidate/freeze), not intake
   byte corruption. Checkpoint pins are historical, not live pointers — do not
   consume DRAFT SHAs as current bytes.
3. 1× `DATA.p2e11.publication-r1.json` reviewed candidate `76191e9b...` vs captured
   current candidate `DATA.p2c04... adf22516...` (REQUEST_CHANGES `r1` → final,
   `reviewed_commit 1266a5f...`, expected supersession).

FILE (`path`+`sha256`+`byte_count`) vs semantic digest: `candidate_sha256`
(`52c8d0bc...` W34, `6b9fd905...` SP) and checkpoint `implementation.contract`
hashes have no `path` and were correctly excluded from FILE matching.

Spot MATCHES (independent): SP candidate PDF `8a9a721a...` 850785B ==
`DATA.p2a30.p2a30` bytes; W34 `main.tex` `9d320a62...` 1262B ==
`DATA.p2c39.main.tex`; SP `main.tex` `87bcb707...` 293777B ==
`DATA.p2a28.main.tex` (final, distinct from DRAFT `b09ab351...`).

## Crosspath / basenames / .py

- No wrong-edition/ref mapping: every `sources/2026-W34`/`surveys/weekly/2026-W34`
  body has ref `774...`; every `sources/SP-efficient-llm-2026`/`surveys/special/...`
  has ref `c8...`; blob supplements use `blob-sha-pinned` with blob-SHA URL.
  `url`-contains-`ref` holds for all contents-API files.
- Duplicate basenames are properly namespaced: 30 basenames duplicate across
  editions (e.g. 10 checkpoints, `architecture-v2.json`, `discovery-v2.jsonl`,
  `main.tex`, `references.bib`, `session-worklog.md`); manifests distinguish by
  full `repo_path` + `DATA.<gid>.<basename>` local (`DATA.p2a01...` vs
  `DATA.p2a11...`, `DATA.p2b43...` vs `DATA.p2b44...` for the two W34 worklogs
  at different luna paths). Checker enforces `local startswith DATA.<gid>.`;
  no collision. Consumers must look up by `gid`+`repo_path`, never bare basename.
- No `DATA.py` execution: zero `DATA*.py` / `*.py` in P1/P2/P3; acquired `.py`
  DATA referenced in READMEs belongs to the older profile-support intake, not here.

## Old fixed archives (limited, no sweep)

Only exact paths cited in intake docs were read:

- `.rephase-1-inputs/774.../sources/2026-W34/production-profile.json` PRESENT 2371B
  (profile intake secondary, not corpus proof).
- `.phase-5-inputs/774.../sources/2026-W34/publication/v2/reader-manuscript-v2.json`
  19652B `c453bea7...` MATCHES P1 candidate `reader_manuscript.sha256` (W34 link
  verified via archive, explaining `UNACQUIRED` in P1/P2/P3-only map).
- `.phase-5-inputs/3e3e.../surveys/weekly/2026-W34/main.pdf` 338722B
  `e93db71a...` MATCHES P1 candidate/release `pdf_sha256` (same).
- SP PDF verified via captured blob, not archive: `DATA.p2a30` 850785B
  `8a9a721a...` MATCHES `DATA.p2c04` candidate `pdf.sha256`.

No Production checkout (`/home/eariver/git/japanese-generative-ai-survey`) inspected.
No root sweep, no Gitlinks traversal. `tree.json` 3351-blob inventory reused as
provenance only, not re-hashed here.

## Snapshot of current P3 claims (unsupported until P4)

- `data-root-mapping.md` “required Raw closure verified” blanket: UNSUPPORTED for
  `p3a02–07` (0 bytes vs non-empty blobs). Pause consumption of those 6; preserve
  original wording as fault, do not overwrite.
- `cumulative-matrix.md` “W34 55/55, SP 26/26 … coverage demonstrated … No further
  primary fetch needed for referenced repo Raw paths”: TRANSPORT inventory only
  (paths from `discovery-v2.jsonl`), NOT byte closure for the 6. Valid for the
  other 53+4+25 once P4 lands.
- `remaining-requirements.md` correctly scopes publisher bodies/shards/intermediates/
  worklogs/render/bibliography as separate-permission or at-ref-but-unfetched;
  no new authority claim made there.
- P2 `transport-partial` correction is accurate; same applies to P3 until P4.
- No quality/corpus-completeness/vulnerability claim is made by hashes here.
  Hashes prove transport + per-file integrity where bytes exist, not editorial
  sufficiency, provenance authority, security, or cost.

## Final routing

- NEEDS_REPAIR: 6 rows above (P3 `p3a02–07`). P4 must fetch exact-blob bytes at
  `774...` for those 6 blob SHAs and validate `len==size`,
  `git-blob==body-sha`, `sha256==discovery-want` (`f75f...` etc.), then rewire
  `DATA` + manifest. Root routes findings; intake owner repairs.
- Material consumption of those 6 + dependent discovery/evidence chains must wait
  for fixed mapping; other 57 P3 + 145 P2 + 4 P1 DATA are byte-verified and
  consumable per stage need.
- This is intake-integrity only, not a new audit gate/system framework.
  No new Human auth needed for P4 repair of already-authorized fixed-ref files;
  ask only for another ref/separate asset/publisher acquisition as packet README directs.
