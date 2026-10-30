# A2 original evidence — raw preservation + source binding

Date: 2026-10-28 UTC. Preserves author-A2 test evidence (`/tmp/dm022-a2-test-raw-20261028.txt`,
`/tmp/dm022-a2-private`) WITHOUT re-running tests and WITHOUT copying fixture DBs
into the packet. R1 snapshot untouched. No ordinary commits. Machine binding in
`a2-binding.json`; private intended-source manifest in `private-source-manifest.json`.

## 1. Raw byte preservation (author raw, NOT preparer transcription)

- Source: `/tmp/dm022-a2-test-raw-20261028.txt` (author-saved raw, 835B, 11 lines)
- Preserved copy: `evidence/A2-original-20261028T124706Z/dm022-a2-test-raw-20261028.txt`
- SHA256 src == dst: `1ac355419351eea43fc751db7ed6abdb95350b4b474d4cb3d43c095e2a9b78fe`
  (byte-equal True; `cp` exit 0)
- Content: 5 unittest oks (WEEKLY/THEMATIC prepare→adopt→resume→readback, LOW
  typed-loader dispatch, LOW guard/slots, HIGH CLI prepare) + `Ran 5 tests` + `OK`
  + `EXIT:0`. Matches `author-A2-return.md` §4 claim (5/5, exit 0, same SHA).
- Provenance: this txt IS the author raw run output. Preparation commands that
  copied/hashed it are transcribed tool-observed (see `copy-commands.log` in
  source-r2 evidence) and are explicitly NOT raw. Post-hoc hashing here is
  observation AFTER the run, NOT retroactive per-run proof; no lost raw is
  recreated.

## 2. Private source binding (R1 + only A2, scoped)

Private: `/tmp/dm022-a2-private` (no top-level `.git`; 27 `*.pyc` caches present
but excluded from inventory; independent fixture DBs were temp dirs per A2 return
and are NOT in this path; large fixture trees NOT copied).

Intended counts (excl `.git`/`__pycache__`/`*.pyc`): PRIV 756 / CAND 756 / R1 756.

A-owned 4 (all priv == candidate, all priv != R1):

- `scripts/survey_research_authority_v2.py` — `c67e0afb…`/109192B (A2 pin match)
- `scripts/survey_prearchitecture_acceptance_v2.py` — `0407b1aa…`/76295B
- `tests/dm022_prearchitecture_fixtures_v2.py` — `7fdc692c…`/3330B
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — `749c708e…`/36770B

Other-files-differ (scoped R1+onlyA2 verification):

- PRIV vs R1 diff: exactly 4 paths (the A-owned 4 above). No other private file
  differs from R1. Claim VERIFIED SCOPED.
- CAND vs R1 diff: 41 paths (A2 4 + B/C corrections across agent/handlers/stage/
  orchestrator/bridge/gate, renewal/history/source, derivation, staged-source,
  publication/editorial/retention/reader/release, config-adjacent tests). Expected:
  candidate integrated A2/B/C while private froze at R1+onlyA2.

## 3. Packet contents / limits

- `dm022-a2-test-raw-20261028.txt` (raw byte-preserved, 835B)
- `private-source-manifest.json` (756 intended files; SHA256
  `ad67931f…`/150048B; fixture DBs/caches excluded, NOT copied into packet)
- `a2-binding.json` (hashes, comparisons, counts)
- This file. No Git DB in packet (`find -name .git` empty). No overwrite of
  prior artifacts. No test execution, no installs, no network, no Human commit
  readback.
