# W34 preflight r2 — short note (review only, DO NOT EXECUTE)

Root rejects r1 wrapper despite mechanical PASS. r1 preserved untouched
(`w34-operator-preflight-20261104.py` 24479B). r2 is NEW, same
manifest/input unchanged.

## Root defects fixed in r2

- `251-254 _strict_json(root_path)` parsed Discovery JSONL as single JSON
  object => certain failure. r2 uses validated `effective['root_records']`
  (369) / `effective['records']` (439) as authority; never JSONL-as-JSON,
  no dummy defaults.
- Meaningless `pass` guard (223-225) replaced by strict
  `len(root_recs)==369`, `len(disc_recs)==439` + screening decisions 439.
- Fake `if False` supplement context (246) removed.
- Dead fallback walk helpers removed; pinned SP helper called directly.
- Retention was under entire workspace (permits active-repo dir); r2
  enforces exact resume-packet lexical containment before mkdir and before
  every packet write (`_require_under_packet` / `_stage_bytes_exclusive_packet`).
- `EXPECTED_ABSENT` hardcoded gate/CP labels removed; gates/CP absence
  relies on full W34 tree (1781f/80d) + real State CAND, no false labels.

## Files (packet only, no active writes)

- NEW wrapper `w34-operator-preflight-r2-20261104.py` 25129B
  `0898d6bc3b24c8e89dc3286037ac659fe818704cbd6effafea694e5ad617ce68`
  (programmatic sha256, 64-hex, stdlib syntax OK)
- Manifest unchanged `w34-prepare-expected-manifest-20261104.json` 991185B
  `cede7e467406b25763b9090484b31e34dc771a6c85a81e52bd19025a9db02590`
- Input r2 unchanged `w34-corrected-input-r2-20261104.json` 1580317B
  `1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed`
- Supplement reused unchanged `ce6f977a...` 389414B (428/425)
- Stdlib checks `w34-preflight-r2-stdlib-checks-20261104.py` 7857B
  `1aa4ac144dca0d5c0deee296ab78a5d53c9d77a014d7f15f03f9a6e7b47501f6`
  + raw `...raw.txt` 969B `9b39eaafecc663ffe97e1c6812f3b0c3c980d83bb51868f4659ab8671e45ec34`
  (28/28 PASS: JSONL-not-JSON, real 369/439, invalid-count refusal not token
  presence, packet/active-ancestor refusal; no project import/run/git/network)

No active execution yet. Exact2 disposition mapping remains pending
(`w34-owned-output-disposition-candidate-20261104.json` ownership only).
