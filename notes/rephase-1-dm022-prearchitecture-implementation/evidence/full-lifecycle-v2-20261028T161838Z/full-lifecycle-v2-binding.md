# Full-lifecycle witness v2 evidence — raw preservation + source binding (General)

Date: 2026-10-28 UTC. General whole-operation witness, NOT independent review.
No Human Commit/Push readback, no ordinary commits, no edits to any existing
code/tests/helpers (only NEW tests/test_dm022_full_lifecycle_v2.py +
NEW tests/dm022_lifecycle_fixture_v2.py owned by General). No old runner
execution, no network/install/cleanup/Production.

## 1. Raw byte preservation (witness raw, NOT transcription)

- Source: `/tmp/dm022-full-v2-raw-20261028.txt` (witness-saved raw, 602B, 8 lines)
- Preserved copy: `evidence/full-lifecycle-v2-20261028T161838Z/dm022-full-v2-test-raw-20261028.txt`
- SHA256 src == dst: `de5b3e5dc09ad4e55b581fd43a8729a1f7f89020dd1df9f537e791e9df4e0996`
  (byte-equal; `cp` exit 0)
- Content: 3 unittest oks + `Ran 3 tests` + `OK` + `EXIT:0`. Scope: WEEKLY +
  THEMATIC full DM022 prepare→external synthetic decision→adopt→strict LIVE
  State validation/readback→7-slot exact inventory→ordinary
  run_selection_architecture regeneration (new independent Selection input,
  audit no-overwrite)→public stage advance EVIDENCE_REVIEWED→SELECTION_COMPLETE,
  plus repeat correction (second generation, anchor preserved) + wrong-role
  PREARCH publication pointer refusal (mode + activation). Synthetic reviewer/
  executor identities are explicit nongenuine (SYNTHETIC_FIXTURE_PROVIDER/
  DM022_FULL_V2); no genuine PASS generated.
- Provenance: this txt IS the witness raw run output from the private copy.
  Preparation commands that copied/hashed it are transcribed tool-observed and
  are explicitly NOT raw. Post-hoc hashing is observation AFTER the run, NOT
  retroactive per-run proof.

## 2. Private source binding (CURRENT idle candidate + only-General new tests)

- Private: `/tmp/dm022-full-lifecycle-private-20261028T120000Z` (no `.git`;
  no `__pycache__`; independent fixture DBs were per-test temp dirs, NOT in path).
- Base: actual409/tree8ce + 93 intended overlay (idle candidate-work, all runtime
  authors returned idle; HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`).
- Intended counts (excl `.git`/`__pycache__`): PRIV 758 (742 + 5 DM022 schemas?
  actually 756 A4 baseline + 2 General new files = 758).
- General-owned 2 (priv == candidate-work):
  - `tests/test_dm022_full_lifecycle_v2.py` — `a6998aa0…`/47837B
  - `tests/dm022_lifecycle_fixture_v2.py` — `dc76b2e7…`/3892B
- priv vs candidate-work: 0 diffs on intended files (private IS current
  candidate-work minus `.git`, plus overlay already in candidate-work).
- Runtime: `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
  TinyTeX `lualatex` (LuaHBTeX 1.24.0) + `biber 2.22` available (not yet
  exercised; publication PDF is later scope, see progress doc).
- Manifest: `private-source-manifest.json` (758 files; SHA256
  `17358b2f08136865e87f24c9132bbc4ab76832451ebde98011c16308536c702c`).

## 3. Packet contents / limits

- `dm022-full-v2-test-raw-20261028.txt` (Attempt 1 raw, 3 tests OK)
- `dm022-full-v2-test-raw-20261028-attempt2.txt` (Attempt 2 raw, 4 tests OK,
  SHA256 `ef3a36db10f19713ea631e36a65b8d29e0cc6d375070f75e9be80f1bc1674507`)
- `private-source-manifest.json` (Attempt 1, 758 files `17358b2f…`)
- `private-source-manifest-attempt2.json` (Attempt 2, 758 files `2e684ea9…`;
  own test file `49392600…`/50436B with new Architecture test)
- This file. No Git DB in packet. No overwrite of prior artifacts
  (R1/R2/A2/A3/A4/integration evidence intact). No test re-execution here,
  no installs, no network, no Human commit readback. Whole-lifecycle unit
  continues (no Commit Point claimed; later lifecycle NOT passed).
