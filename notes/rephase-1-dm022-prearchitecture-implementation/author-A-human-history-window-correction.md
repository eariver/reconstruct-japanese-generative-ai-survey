# Author-A human-history-window correction — DM022 pre-Architecture (A5, NEW task)

2026-10-29. Owner A (research operation). NEW human-history-window task, assembled
from actual source + actual NEW-run evidence. This file is NEW
(`author-A-human-history-window-correction.md`); it does NOT overwrite
`author-A-path-normalization.md` (which currently holds the same A5 text under
the wrong A4 label — see evidence-restoration-and-loss.md) or any other author's
return. Binding: contract a345bb95 INCLUDING §11, pre-code ROOT FULL `0425c530…`
INCLUDING §5, R4 + literal schemas / R5 / R6, R2 + A4 independent reviews. No
ordinary candidate/reconstruct Commit/Push; no fixtures in reconstruct; no git
config/global writes; no network/Production/reset/clean/old-log overwrites.
Python 3.14.4 + unittest + jsonschema 4.23.0/pypdf 6.16.2. No implementation
acceptance claimed; root review required. The A4 task is NOT closed out by this
file (root asked: no close-out of the wrong A4 task).

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(765 intended files excl `.git`/caches; HEAD `409b292…`, no ordinary commit).

## 1. A-owned files (this task; verified read-only from candidate)

- `scripts/survey_research_authority_v2.py` — 155892B, SHA256
  `2aef837faaa549b9eab3f1a03696b5a44ef63ff63316cad817842c2110554fb3`
  (private `_norm_path`, 106 use sites; Path-or-non-empty-string coercion at
  every public path entry; FD-vs-lstat identity + O_NOFOLLOW unchanged)
- `scripts/survey_prearchitecture_acceptance_v2.py` — 88603B, SHA256
  `f8af03cc5d58af1057ea26d9cef0eb87b1fd71118ddf63a2186e24da9bc1e751`
  (file-local `_norm_path`, 27 use sites; sole-mutator discipline unchanged)
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — 80610B, SHA256
  `a08265175a1ea697cdf2fa8716cc2b53708ddf586de1a721505b76bc63b3f5e4`
  (25 `def test_` methods: 23 carried positives + 2 new str-path loader tests;
  4 human-window tests `:1104`–`:1168` intact)
- `scripts/survey_evidence_v2.py` — 125817B, `8b55dc6c…` (A-owned leaf, unchanged
  this task; consumed function-locally)
- `tests/dm022_prearchitecture_fixtures_v2.py` — 3330B, `7fdc692c…` (test-only
  helper, unchanged; never runtime authority)

HIGH `f8af03cc` policy note (observed, NOT semantic approval): eligibility and
review-presentation checks explicitly account for Human decisions PRIOR to new
REQUEST_CHANGES (`survey_prearchitecture_acceptance_v2.py:371,428,497` reference
recorded presentation/review/decision including REQUEST_CHANGES; the 4
human-window tests exercise the pre-REQUEST_CHANGES window). Characterized from
read-only source inspection; no behavior proof claimed here.

## 2. NEW-run evidence (A5 human-history run; actual recorded raws)

Private copy `/tmp/dm022-a5p-priv` = current idle candidate worktree (765
intended files; rebuilt AFTER all A edits; pycache purged) + independent `.git`
byte-copy (83 files, 0 inode overlap, inert origin, HEAD `409b292…`). Fixture
Git DBs independent temp dirs per test; no fixture objects in reconstruct; no
saved runners; no shared-candidate tests.

- Targeted raw `dm022-a5-path-targeted-raw.txt` — 3381B, 77 lines, SHA256
  `7213b03deb2cacf460b90c1a5a4f5f255eb6216578b31c33dd57811823a74de6`,
  exit 0: **4/4 PASS** (2 new loader str-vs-Path tests; release CLI
  `main == 0` + already-RELEASED refusal, REG-03 gone; C2 refresh healthy-legacy
  end-to-end PASS via B `Path()` wrap + C2 schema-fixture fix + A
  normalization — three-part attribution, no single-component over-claim).
- Full raw `dm022-a5-full-20261028.txt` — 5357B, 49 lines, SHA256
  `d77d5776a5e942ab8b74509c4e7611461cfeadbe9b8cbbeb696ae1fa43578e0d`,
  exit 0: **25/25 PASS in ~26s**.
- `private-source-manifest.json` — 765 files, SHA256
  `f5fa1269e932598aa2899bdfaff35146ada5066ca98b49f172f00e3ec82a99cb`.
- Byte-preserved copies: `evidence/A-human-history-20261029T095202Z/` (all 5
  A5 files above plus `a-binding.json` `75933375…`/4195B and
  `a4-path-raw-binding.md` `c65bdee6…`/3957B).

Supersession note: the stale `/tmp/dm022-a4p-path` run (exit 1, 3 PASS + 1
C2-fixture ERROR, 21 tests) is superseded by the two final A5 raws; its draft
numbers are withdrawn, not alternate evidence. No old test-count/PASS transfer;
no Production/W40/adoption claim. Whole NOT_READY/step4B3 OPEN/audit
unstarted/DM021+022 OPEN preserved. Ordinary Commit/Push Human-owned.
