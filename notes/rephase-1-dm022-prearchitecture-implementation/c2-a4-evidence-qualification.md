# C2 A4-regression evidence qualification — saved-evidence scope check only

2026-10-28 UTC. Fresh checker. Read-only inspection of SAVED C2 work/evidence.
No code edits, no runtime, no duplicate tests, no network, no Git mutation,
no Human commit/readback. Previous resume provider `invalid_parameters`
not deep-debugged per instruction. No active-child probe executed
(premise: authors STOPPED / probably all stopped). Inherited 55 children
not inspected. This is evidence-scope check, not fresh implementation
approval. Author report `author-C2-a4-regression-correction.md` preserved
original; corrections below do not edit it.

## 1. Checked set

- Author: `notes/rephase-1-dm022-prearchitecture-implementation/author-C2-a4-regression-correction.md` (159 lines).
- Pin: `evidence/integration-c2-a4fix-20261028T171309/source-pin.txt` (14 lines).
- Base manifest ref: `evidence/source-a4-20261028T160708Z/snapshot-a4-manifest.json`
  (756 entries) + `source-a4-preservation.md` (31 lines).
- Raws/headers/exits: `evidence/integration-c2-a4fix-20261028T171309/` —
  8× `run-0X-{header,exit-code,stdout-stderr-raw}` + 7× secondary
  `run-survey-*` / `run-run-selection-*` `{stdout-stderr-raw,exit-code}`
  without header (39 entries total incl. `source-pin.txt`).
- Grep over evidence dir for `^(OK|FAILED|Ran \d+ tests)` and for
  `DM022_TRANSITION_ACTIVE|MISSING_ANCESTOR|lstat failed|NO_WRITES|no writes`.

No private-copy re-hash, no candidate-work readback, no test re-execution.

## 2. Green counts — primary 8 match author table; 7 secondaries extra

Author §4 table claims 17+28+9+9+5+5+2+2 (total 77), all exit 0.
Primary `run-0X` raws confirm exactly:

- 01 c2-consumers: `Ran 17 tests in 41.151s` + `OK`, exit `0`.
- 02 reader-gate: `Ran 28 tests in 2.678s` + `OK`, exit `0`.
- 03 pub: `Ran 9 tests in 2.103s` + `OK`, exit `0`.
- 04 release: `Ran 9 tests in 0.341s` + `OK`, exit `0`.
- 05 exec: `Ran 5 tests in 0.036s` + `OK`, exit `0`.
- 06 agent: `Ran 5 tests in 0.928s` + `OK`, exit `0`.
- 07 views: `Ran 2 tests in 0.003s` + `OK`, exit `0`.
- 08 selarch: `Ran 2 tests in 0.000s` + `OK`, exit `0`.

All 8 headers agree: `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest
discover -s tests -p <file> -v`, cwd `.../dm022-prearchitecture-implementation-20261028T113126Z/c2-a4fix-20261028T171309`,
`Python 3.14.4`, `HEAD: 409b292756dd1277b9dfae87679934c0d2ce251c`,
`origin: https://example.invalid/rephase-candidate-recovery.git`,
`NO_GIT_ENV_OVERRIDES`, `PRE_COUNT: 756`, `PRE_PYCACHE: 0`.

Secondary terse raws (dots-only, no per-test names) are also green exit `0`
with same counts but different durations and NO header/binding:

- `run-survey-reader-surface-gate-v2`: 28 in 2.459s OK.
- `run-survey-publication-v2`: 9 in 2.120s OK.
- `run-survey-release-checkpoint-v2`: 9 in 0.311s OK.
- `run-survey-execution-record-v2`: 5 in 0.035s OK.
- `run-survey-agent-control-v2`: 5 in 0.932s OK.
- `run-survey-active-evidence-views-v2`: 2 in 0.002s OK.
- `run-run-selection-architecture-v2-interactive`: 2 in 0.000s OK.

Qualification: secondaries are unbound (no cmd/cwd/HEAD header) and
unmentioned in author table. They do not expand scope; primary 8 are the
bound claim. Run-01 has no terse duplicate. Naming-scheme split
(`run-0X-*` vs `run-survey-*`) is unexplained in author text which cites
only `run-*-stdout-stderr-raw.txt (+ -header.txt, -exit-code.txt)`.

## 3. Six owned files — pin vs base distinct; re-hash not done

`source-pin.txt` pins C2-only overlay (6 files, `candidate-work -> private
copy, byte-identical` claimed):

- `scripts/survey_weekly_mechanical_refresh_v2.py` `5f6f4ac2025dfe2e9659bbee4624a53c08980252ab66090d0ce4f8b367f76653`
- `scripts/survey_release_checkpoint_v2.py` `dccad3a91044df3d31776f80e6a4db17ba279fee48685a65d6d7da9b866b9619`
- `tests/test_survey_dm022_c2_consumers_v2.py` `32b4cd49190302ff7b00dd5f25c82139b9fbdff625169ca7d1438ea9e5379aba`
- `tests/test_survey_reader_surface_gate_v2.py` `3729bcba3bd0fb287e413464bc6170784feea1a21c1d3a57df82fb57ddfaae3c`
- `tests/test_survey_publication_v2.py` `2d3e4204b21bf5d874e503f02bff6f4d3a66be61032fb2b91808290439a4ee7b`
- `tests/test_survey_execution_record_v2.py` `15f85350623e1aea13baaa8bc1d52b05652327261dcaa26fb5eec875b23e0b58`

Base `snapshot-a4-manifest.json` entries for the same paths differ in
every case (bytes+SHA), consistent with an overlay change:

- weekly-refresh base `609dad4a91b694e3ad327df556922690b50b550edd52c961930b617abb9486da` (95545B)
- release base `9dac1ed104bd46b4457d3f10939aeed4d317e86ac07563ca356469c498cebe83` (10849B)
- c2-consumers base `63f5ced8e326f97bffc573f4a90f5e40edd9f93f1e203c3efde5081aa5b36882` (20930B)
- execution base `2fab6de40c6e06c7012d97c84794f6fa5d3f3edeec4ce64ce217f816687b864a` (6809B)
- publication base `48188a74dd5da1f3dc9f5516ba0d89902323aad5b8f7e4875a06241fc9acc941` (25208B)
- reader-gate base `2157c7fb55c21f469161480ce4942ab28fff8730571d8b086eca625efbffa21b` (54322B)

Qualifications: (a) overlay SHAs are author-asserted in `source-pin.txt`;
independent re-hash of private copy not performed per no-runtime scope.
(b) No full private manifest for `c2-a4fix` copy in packet — only the 6
pins + base-manifest reference + `worktree files: 756` line. (c) Claimed
`candidate-work copies verified byte-identical post-sync` and `final
diffs limited to intended C2 files (verified byte-identical
candidate-work ↔ private copy at run time)` have no saved diff artifact.
(d) Current main `candidate-work` may since carry B/A changes; C2 six
expected unchanged but not re-verified here.

## 4. Corrections to author §4 lines 82–85

(a) Base-manifest hash typo. Author line 83 gives
`2eb615b41307e86cc86770c9f4ba259e2626f88c4e898f3672a2cdc86621`.
Correct per `source-pin.txt:3` and `source-a4-preservation.md:15` is
`2eb615b41307e86cc86770c9798bf4ba559e2626f6884e898f3672a2cdc86621`
(149855B, 756 entries). Use the latter; author string is a transcription
typo.

(b) `83 .git files ≠ 83 objects`. Author line 84 says byte-copied `.git`
`(83 objects, ...)`. `source-a4-preservation.md:9` and `:22` say 83
**files**, 0 `(dev,ino)` overlap, no alternates/commondir, inert
`example.invalid` origin, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`.
Headers corroborate HEAD/origin. `83 objects` is wrong; read as 83 files.

## 5. Entry/late-seam assertions — entry-pass only, not full-positive/prepublish proof

Author §4 lines 112–118: positive phase fails strictly later
(finalize→editorial-receipt missing-file; activate→prepared-set schema;
resume→activation-record schema; candidate→manuscript-schema;
gate→missing semantic-review), each with NO `DM022_TRANSITION_ACTIVE` and
no writes, proving entry READY passed; guard phase then refuses with exact
`DM022_TRANSITION_ACTIVE: [FINALIZE|ACTIVATE|RESUME/REFUSED_PRE_WRITE]` or
`guard present` and no canonical writes.

Checked: all saved raws contain only unittest test-names + `ok` +
`Ran N tests` + `OK` (plus trailing JSON dumps in 01/04). Grep for
`DM022_TRANSITION_ACTIVE|MISSING_ANCESTOR|lstat failed|NO_WRITES|no writes`
over the evidence dir returns nil. So seam location, exact-error text, and
no-writes are **test-oracle claims** (`ok` means the in-test asserts
passed), not independently visible in raw logs.

Qualification per instruction: a positive that fails LATER at a
missing-receipt/set-schema check proves only that the entry READY seam was
passed **within that test's oracle**; it does not prove full positive
publication success, and source-code guard wiring (`READY entry+prepublish`
in author §5) cited as unchanged code paths is a code claim not evidenced
by these raws alone. Likewise guard-phase exact-typed refusal is
oracle-only here. Do not claim full-positive or prepublish-fault coverage
beyond entry-pass + planted-guard refusal as oracled. No such exercise was
run in this check.

## 6. Intermediate failures — disclosed but not preserved (overwritten in place)

Author lines 106–110 disclose intermediate iteration failures (missing
schemas copy, relative-path resolution against CWD, guard file counted in
snapshot) fixed in-place and superseded by final greens.

Checked: evidence dir holds only final green raws (8 primary + 7 terse).
No intermediate failure raw/header preserved. Determination: intermediate
failures were overwritten in place, not preserved. Accept author disclosure
as history; do not reconstruct missing logs. Final-green-only packet cannot
independently prove the stated intermediate failure modes or the in-place
fix sequence.

## 7. Actual scope

Proved by saved evidence as checked: 8 bound primary runs green with
matching counts/exit-0/consistent headers on a 756-file pre-count copy at
HEAD `409b292` with inert origin; 6-pin overlay distinct from base
manifest; base hash and 83-files corrections above; secondary 7 greens
exist but unbound. Not proved by this packet alone: independent overlay
re-hash, `candidate-work ↔ private` byte-identity, exact-error/no-write
strings outside test oracles, full-positive publication, prepublish guard
wiring beyond entry-pass, intermediate failure modes, or any
B/A-current-tree state. No implementation approval granted.
