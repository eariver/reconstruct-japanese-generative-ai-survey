# Independent identity resolution — findings-blob typo + authoritative binding

Date: 2026-10-03 (after `m3-20261003T0445Z/corrections2-identity-20261003T0944Z`).
Role: same fresh author-independent reviewer, recovery unit ONLY. No agents, no
worker/root edits, no tests/runtime/network/fixture mutations. Read-only
confirmation only (`Read` + read-only `git ls-tree/rev-parse/log`,
`sha256sum`/`ls`, read-only JSON parsing; worker `compare_identities.py` was
read, not executed). Candidate/archive unchanged. Prior
`independent-recovery-review.md` (CHANGES_REQUIRED) and
`independent-recovery-resolution.md` (BOUNDED_PASS) remain preserved.

## 1. Prior overclaim qualified

My initial review (§5, lines ~72–73) stated the full 32 raw matched the manifest.
That was overbroad and wrong for one entry. What I actually verified then: live
`diff --name-status` path set (32), sample R1 postimage blobs, and manifest
structure — not a machine all-blob cross-check. I missed the single-hex typo:

- `tests/test_survey_findings_v2.py`, mode `100644`
- correct (m2 `raw/20-identities.stdout.txt:24`, live fixture, live restore,
  new binding): `6e179887284026d1fb6fc33522b5fb28afc4788e`
- wrong (m2 `manifest.json:final_32_identities`, copied to m3
  `manifest.pretty.json`): `6e178887284026d1fb6fc33522b5fb28afc4788e`
  (3rd hex char `9`→`8`).

The path-level `TREEDIFF_MATCH` and sample blob checks masked a single-value
transcription error. The underlying artifact/test/closure/restore proof was not
invalidated (live Git always held the correct blob), but the identity-table
claim was. This resolution corrects the record by machine verification, not by
editing originals (typo'd entries preserved with pointer).

## 2. Independent machine confirmation (all 41, read-only)

Recomputed without running worker script, under
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`:

- raw20 parsed: 32 + 9; m2 manifest: 32 + 9; new `final-identity-binding.json`:
  32 + 9; union 41 paths, 32/9 disjoint.
- Live `git ls-tree HEAD -- <41 paths>` at fixture: 41 rows; at restore: 41 rows.
- Pins live: head `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`,
  tree `657032438c6ed8b1c055d5a120b67b4b261a5092`,
  parent `774dd39a951c9ac3818e83dfffd4c7666efb0a20` — unchanged.
- Findings row: m2 `6e1788...` vs raw/final/live/restore `6e1798...` (exactly the
  reported single mismatch; live fixture and live restore agree on `6e1798...`,
  verified directly).
- All other 31 final + all 9 Freeze: new binding == raw20 == live fixture ==
  live restore, 0 extra mismatches. M2 manifest == raw20 except the one known
  typo. `final-identity-binding.json` findings entry is the correct `6e1798...`.
- `final-identity-binding.json` SHA256 live `559512d3e48e0101af543fe1b36c0cfded0a1b6304837b1b5bac253c1eaed75e`
  matches `correction.md` claim. Archive live SHA `faf6792f...2ade9f3c` ==
  `.sha256` file (bytes 5,152,199 per prior verified + worker numeric checks) —
  unchanged.
- Worker `raw/compare-run.stdout.txt` (exit 0) is byte-identical to
  `comparison-report.txt` (20 lines, `TOTAL_MISMATCHES=1` with the single
  `VALUE-DIFF` line); `live-lstree-fixture.stdout.txt` holds 41 rows;
  attempt1 (`KeyError 'raw'`) / attempt2 (`KeyError 'id'`) + final-pass raw
  preserved. Script history disclosed, fixture never written per sources.

## 3. Revised binding/report verified exactly

- `correction.md`: typo description, affected originals (preserved, not fixed in
  place), full-41 comparison scope, authoritative-binding provenance (parsed live
  output, membership/order from raw20, no retyping), script history, and
  unchanged-artifact check all match independent recompute above.
- `comparison-report.txt`: counts, pins, 5 exit-file + argv-name + closure
  (row1 sha, 8 rows) + archive numerics, and the single `MISMATCH` line all
  verified. No hidden second diff.
- `final-identity-binding.json`: head/tree/parent + 32+9 records with correct
  findings blob; supersedes only the two typo'd entries, confirms every other
  entry unchanged. Verified as the durable blob/mode source going forward.
- `master-binding-supplement.md`: two-file rule (manifest for recovery scope,
  binding for blobs) and supersession list are correct — with ONE path error
  (see §4).

## 4. Exact need: one pointer path fix (minimal, non-blocking for binding truth)

`master-binding-supplement.md:6` cites `../recovery-manifest.json`. That path does
not exist (verified `ls`: `m3-20261003T0445Z/recovery-manifest.json` absent).
The actual final recovery manifest is
`../corrections-20261003T0456Z/recovery-manifest.json` (verified present, 9345
bytes). Exact fix: change line 6 to
`` `../corrections-20261003T0456Z/recovery-manifest.json` ``. No content change,
no re-compare needed; binding truth is unaffected.

## Verdict: BOUNDED_PASS for identity binding (recovery only)

The revised final binding/report are exactly verified; only the one mismatch
exists and archives/candidate are unchanged. No hidden PASS transfer: no new
tests, ancestry, approvals, or runnable claims introduced; prior partial-DB,
synthetic-fixture, and evidence-only-harness limits stand. Cite
`corrections2-identity-20261003T0944Z/final-identity-binding.json` for blob/mode
bindings going forward, originals only with this pointer attached, after the
one-line pointer fix above. No further tests/recovery. No Freeze approval,
audit, or publication claims.
