# Correction: findings-blob typo + authoritative identity binding

Date: 2026-10-03T09:44Z. Worker: General Co-Worker. Trigger: root final
comparison (missed by worker m3 report and independent review).
**No originals edited, no tests/diagnostics rerun, no network, no fixture
writes, no source edits.** Machine comparison only (read-only file reads +
read-only live `git ls-tree/rev-parse/log`).

## The typo (single hex char, 3rd position 9→8)

- File: `tests/test_survey_findings_v2.py`, mode `100644`.
- Correct blob (live fixture `ls-tree`, live restore `ls-tree`, m2
  `raw/20-identities.stdout.txt:24`): `6e179887284026d1fb6fc33522b5fb28afc4788e`.
- Wrong value transcribed into `m2/.../manifest.json:final_32_identities` and
  copied into `m3/.../manifest.pretty.json`: `6e178887284026d1fb6fc33522b5fb28afc4788e`.
- Affected originals (preserved, NOT fixed in place): the m2 manifest entry
  and the m3 pretty copy. No other blob/mode/path in either file is affected.

## Full machine comparison (not just the flagged file)

`compare_identities.py` (saved here, literal run in `raw/compare-run.*`)
parsed raw20 (32+9 sections) as the path set, then compared all 41
(mode, blob) tuples across raw20 / m2 manifest / m3 pretty / live fixture /
live restore, plus numeric cross-checks (five exit files + argv-name coverage,
closure row1/source + 8-row count, archive bytes/sha live vs pinned vs
manifest). Result: **TOTAL_MISMATCHES=1** — exactly the findings typo above.
The other 31 final identities and all 9 Freeze bindings are byte-identical in
all five sources; both live trees agree on all 41 rows. Full per-source values
for the one diff are in `comparison-report.txt` (also `raw/compare-run.stdout.txt`).

## Authoritative binding (new, parsed — not retyped)

`final-identity-binding.json` (SHA256
`559512d3e48e0101af543fe1b36c0cfded0a1b6304837b1b5bac253c1eaed75e`)
was generated **solely from parsed live-Git output** (`ls-tree` rows,
`rev-parse`/`log` pins) with membership/order derived from raw20 sections —
no manual transcription. It carries full head/tree/parent plus the complete
32+9 records with the correct findings blob. It **supersedes** the two typo'd
manifest entries; every other entry it confirms unchanged.

## Script history (preserved, not hidden)

- Attempt 1: `KeyError 'raw'` (assumed a manifest key that does not exist) —
  raw saved as `compare-run-attempt1.*`.
- Attempt 2: `KeyError 'id'` (m3 manifest entries lack ids) — saved as
  `compare-run-attempt2.*`.
- Final pass: exit 0, glob-enumerated exit files + argv-name coverage instead
  of assumed keys. Two interim script edits are the current file; attempts are
  retained. Read-only inspection; fixture never written.

## Unchanged-artifact check

Archive live recompute: 5,152,199 bytes, SHA256
`faf6792f...2ade9f3c` — equal to `.sha256` file and both manifests.
Candidate/restore HEAD/tree/parent re-read live, unchanged
(`b40de60/6570324/774dd39a`). No test, network, or write operations occurred
in this unit.
