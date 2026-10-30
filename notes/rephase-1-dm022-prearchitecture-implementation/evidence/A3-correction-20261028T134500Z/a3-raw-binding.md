# A3 correction evidence — raw preservation + source binding

Date: 2026-10-28 UTC. Preserves author-A3 test evidence (`/tmp/dm022-a3-raw-20261028.txt`,
`/tmp/dm022-a3-fresh` = R2 snapshot + ONLY-A3 overlay) WITHOUT re-running tests and
WITHOUT copying fixture DBs into the packet. R1/R2 snapshots untouched. No ordinary
commits. Machine binding in `a3-binding.json`; private intended-source manifest in
`private-source-manifest.json`.

## 1. Raw byte preservation (author raw, NOT preparer transcription)

- Source: `/tmp/dm022-a3-raw-20261028.txt` (author-saved raw, 3997B, 37 lines)
- Preserved copy: `evidence/A3-correction-20261028T134500Z/dm022-a3-test-raw-20261028.txt`
- SHA256 src == dst: `abb66f3ded3c03113928db57dc1cbb7090dc80731ed49a1b1d5c28347da037d3`
  (byte-equal True; `cp` exit 0)
- Content: 19 unittest oks + `Ran 19 tests` + `OK` + `EXIT:0`. Scope: WEEKLY +
  THEMATIC full prepare→adopt→resume→readback×2 (incl. per-file manifest refs,
  FULL adopted-graph validation, checker, resolver, CLI prepare), LOW
  typed-loader dispatch, LOW guard/slots, plus 14 fault tests (Raw binding
  refusal, late final plant + bounded resume, completion tamper ×3 +
  resume-INDETERMINATE, absent-slot regeneration + READY + readback, blocked
  repeat pin, stale HEAD/decision/unsupported profile/named gap(+positive),
  interrupted-clear resume, unknown-state resume, slot ownership ×2, State-tmp
  plant refusal, completion idempotence, unreadable-path fail-closed).
- Provenance: this txt IS the author raw run output. Preparation commands that
  copied/hashed it are transcribed tool-observed and are explicitly NOT raw.
  Post-hoc hashing here is observation AFTER the run, NOT retroactive per-run
  proof; no lost raw is recreated.

## 2. Private source binding (R2 + only A3, scoped)

Private: `/tmp/dm022-a3-fresh` (no top-level `.git`; no `__pycache__`/`*.pyc`;
independent fixture DBs were temp dirs per test and are NOT in this path).

Intended counts (excl `.git`/`__pycache__`/`*.pyc`): PRIV 756 / R2 756.

A-owned 5 (all priv == candidate-work):

- `scripts/survey_research_authority_v2.py` — `aee60132…`/132244B (priv==cand, priv!=r2)
- `scripts/survey_prearchitecture_acceptance_v2.py` — `2fe12b9e…`/87249B (priv==cand, priv!=r2)
- `scripts/survey_evidence_v2.py` — `8b55dc6c…`/125817B (priv==cand, priv!=r2; A3 pure helpers added)
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — `9755279f…`/62293B (priv==cand, priv!=r2)
- `tests/dm022_prearchitecture_fixtures_v2.py` — `7fdc692c…`/3330B (priv==cand, priv==r2; unchanged in A3)

Other-files-differ (scoped R2+onlyA3 verification):

- PRIV vs R2 diff: exactly the 4 A3-modified paths above. No other private file
  differs from R2. Claim VERIFIED SCOPED. Schemas unchanged (all 5 byte-identical
  R2 == candidate == private).

## 3. Packet contents / limits

- `dm022-a3-test-raw-20261028.txt` (raw byte-preserved, 3997B)
- `private-source-manifest.json` (756 intended files; SHA256
  `b73c4d9352d22745671077d6368ae28384a298ad06461fc31b68d929f963d1bc`;
  fixture DBs/caches excluded, NOT copied into packet)
- `a3-binding.json` (hashes, comparisons, counts, runtime pins)
- This file. No Git DB in packet (`find -name .git` empty). No overwrite of
  prior artifacts (R1/R2/A2 evidence intact). No test execution, no installs, no
  network, no Human commit readback. A3 unit ongoing (no Commit Point claimed).
