# A4 correction evidence — raw preservation + source binding

Date: 2026-10-28 UTC. Preserves author-A4 test evidence (`/tmp/dm022-a4-raw-20261028.txt`,
`/tmp/dm022-a4-private` = CURRENT idle candidate-work incl B SizedRef fix, minus
`.git`) WITHOUT re-running tests and WITHOUT copying fixture DBs into the packet.
R1/R2 snapshots untouched. No ordinary commits. Machine binding in `a-binding.json`;
private intended-source manifest in `private-source-manifest.json`.

## 1. Raw byte preservation (author raw, NOT preparer transcription)

- Source: `/tmp/dm022-a4-raw-20261028.txt` (author-saved raw, 3984B, 37 lines)
- Preserved copy: `evidence/A4-correction-20261028T140520Z/dm022-a4-test-raw-20261028.txt`
- SHA256 src == dst: `61939974f5d5c524bdc131ef757c6fc942d2dd960db10a7a9470c970578e18ce`
  (byte-equal; `cp` exit 0)
- Content: 19 unittest oks + `Ran 19 tests` + `OK` + `EXIT:0`. Scope: WEEKLY +
  THEMATIC full prepare→adopt→resume→readback (incl per-file manifest refs,
  FULL adopted-graph validation incl recorded-commit own-epoch proof,
  checker, resolver, CLI prepare), LOW loader dispatch, LOW guard/slots, plus
  14 fault tests: Raw claim binding, late final plant + bounded resume, 3×
  completion tamper + resume INDETERMINATE, absent-slot regeneration + READY +
  readback, positive repeat both routes + malformed-SizedRef refusal,
  stale HEAD/decision/unsupported profile/named gap(+positive), interrupted
  clear + resume, unknown-state resume, slot ownership ×2, State-tmp plant,
  completion idempotence, unreadable-path fail-closed.
- Provenance: this txt IS the author raw run output. Preparation commands that
  copied/hashed it are transcribed tool-observed and are explicitly NOT raw.
  Post-hoc hashing here is observation AFTER the run, NOT retroactive per-run
  proof; no lost raw is recreated. Known repeat-blocker pin from A3 is GONE:
  replaced by the real positive repeat (B corrected both PREARCH branches to
  exact 3-field SizedRef in current source; A did not edit B).

## 2. Private source binding (CURRENT candidate incl B fix + only-A4 delta)

Private: `/tmp/dm022-a4-private` (no top-level `.git`; no `__pycache__`/`*.pyc`;
independent fixture DBs were temp dirs per test and are NOT in this path).

Intended counts (excl `.git`/`__pycache__`/`*.pyc`): PRIV 756.

A-owned 5 (all priv == candidate-work):

- `scripts/survey_research_authority_v2.py` — `2df25c5d…`/148801B
- `scripts/survey_prearchitecture_acceptance_v2.py` — `2fe12b9e…`/87249B
- `scripts/survey_evidence_v2.py` — `8b55dc6c…`/125817B (A3 pure helpers)
- `tests/dm022_prearchitecture_fixtures_v2.py` — `7fdc692c…`/3330B (unchanged)
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — `a2e48ba1…`/63453B

priv vs candidate: 0 diffs (private IS current candidate minus `.git`).
Schemas unchanged (all 5 byte-identical R2 == candidate == private).
B's SizedRef correction and C work are included as idle current source;
A tests do not execute B/C suites (shared candidate tests not run).

## 3. Packet contents / limits

- `dm022-a4-test-raw-20261028.txt` (raw byte-preserved, 3984B)
- `private-source-manifest.json` (756 intended files; SHA256
  `14ef836dfc9ae7ce8e30b1f27bb51ab45062cc8b9218cf44ff250704a35fcc4a`;
  fixture DBs/caches excluded, NOT copied into packet)
- `a-binding.json` (hashes, comparisons, runtime pins)
- This file. No Git DB in packet (`find -name .git` empty). No overwrite of
  prior artifacts (R1/R2/A2/A3 evidence intact). No test execution, no installs,
  no network, no Human commit readback. A4 unit ongoing (no Commit Point claimed).
