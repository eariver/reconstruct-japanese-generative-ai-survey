# Evidence restoration and loss report — A4 overwrite / A5 preservation

Date: 2026-10-29 UTC. Evidence-preservation correction ONLY. No source edits, no
tests, no ordinary commits, no Human commit readback (no git commands in
workspace reconstruct root). Candidate/proofs unchanged by this task. 55 child
Gitlinks untouched. No Git DB in packet. Copy commands below are TRANSCRIBED
tool-observed, explicitly NOT raw. No deep debug; source work continues
independently.

## 1. What happened (violation)

The A5 human-history task wrote its NEW data under OLD paths: all 5 files in
`evidence/A4-path-normalization-20261028T164439Z/` (same filenames) plus a full
rewrite of `author-A-path-normalization.md` (now 7508B/119 lines of A5 text),
calling the new data "A4". This violated the no-overwrite rule and mislabeled
the A5 revision as the A4 task (root: no close-out of the wrong A4 task).

## 2. Scopes (exact)

RECOVERED (byte-verified originals restored to old paths — AFTER §3 preserved):

- `evidence/A4-path-normalization-20261028T164439Z/dm022-a4-full-20261028.txt` —
  4433B/41 lines, SHA256
  `632d41f73f0865484ac67ea5ee6ae28631684a2a60540a65a7a6abc4420d848a`
  (matches recorded `632d41f7…`, 21/21 exit 0). Source:
  `/tmp/dm022-a4-full-20261028.txt` (byte-equal, `cp` exit 0).
- `evidence/A4-path-normalization-20261028T164439Z/dm022-a4-path-targeted-raw-20261028.txt` —
  5412B/100 lines, SHA256
  `5102c874afda09b33ef8e9ac569170ae69877ba47ce95a6045e207d0beb6ac74`
  (matches recorded `5102c874…`, old targeted exit 1). Source:
  `/tmp/dm022-a4-path-raw-20261028.txt` (byte-equal, `cp` exit 0; note the /tmp
  basename differs from the evidence basename — recorded transparently here).

NEW REWRITTEN (overwritten A5 version, preserved BEFORE restoration):

- `evidence/A-human-history-20261029T095202Z/` (NEW unique dir, exactly 5 files):
  `a-binding.json` `75933375…`/4195B, `a4-path-raw-binding.md`
  `c65bdee6…`/3957B, `dm022-a5-full-20261028.txt` `d77d5776…`/5357B (25/25),
  `dm022-a5-path-targeted-raw.txt` `7213b03d…`/3381B (4/4),
  `private-source-manifest.json` `f5fa1269…`/151883B (765 files). All 5 `cp`
  exits 0, byte-equal to pre-restoration state. These exact bytes are the new
  A5 actual observation (returned in this report; see also
  `author-A-human-history-window-correction.md`).

LOST (no byte backup found; NOT manufactured, NOT reconstructed from chat/text):

- Original `a-binding.json`, `a4-path-raw-binding.md`,
  `private-source-manifest.json` (`4f14a15f…`/756 files) and original
  `author-A-path-normalization.md` (105-line A4 text). Narrow search of
  `/tmp/dm022-a4p-path` + `/tmp/dm022-a5p-priv` (maxdepth-2 filename sweep for
  `*binding*`/`*manifest*`/`dm022-a4-*`/`dm022-a5-*`) found only source-tree
  files (entity-binding scripts/tests, source-manifest schemas) — no evidence
  byte backups. Earlier tool-Read transcripts of the A4 return remain HISTORY,
  not byte archive.

## 3. Current state + qualification (no fully-clean claim)

`evidence/A4-path-normalization-20261028T164439Z/` now holds 7 files: 2 restored
A4 original raws + 2 A5 raws + 3 A5-overwritten metadata files. QUALIFICATION:
the 3 metadata files (`a-binding.json`, `a4-path-raw-binding.md`,
`private-source-manifest.json`) and the `author-A-path-normalization.md` text
are the NEW A5 revision, NOT the A4 originals — old claims citing them now read
as new-revision claims. Bounded limited evidence survives via stored hashes and
prior reads: original full-raw `632d41f7…` and targeted-raw `5102c874…` are
byte-restored above; original manifest hash `4f14a15f…`/756 and the A4 return's
21-test/exit-1 targeted scope stand as recorded (unrestorable bytes noted).
Historical fully-clean / no-loss is NOT claimed.

## 4. Footnotes (available old metadata, preserved)

- Original A4 scope per prior read: targeted 100 lines `5102c874…` (4 tests:
  3 PASS + 1 C2-fixture-owned ERROR, exit 1); full 41 lines `632d41f7…`
  (21/21 PASS, exit 0); manifest 756 files `4f14a15f…`; private
  `/tmp/dm022-a4p-path`.
- A5 scope per new return: targeted 77 lines `7213b03d…` (4/4, exit 0); full 49
  lines `d77d5776…` (25/25, exit 0); manifest 765 files `f5fa1269…`; private
  `/tmp/dm022-a5p-priv`; HIGH `f8af03cc`/88603B, LOW `2aef837f`/155892B, test
  `a0826517`/80610B (25 methods), helper `8b55dc6c`/125817B, fixtures
  `7fdc692c`/3330B.
- New A5 return lives at `author-A-human-history-window-correction.md` (does not
  overwrite other authors). No semantic approval of HIGH `f8af03cc` policy or
  tests is given here; pins captured read-only (HIGH REQUEST_CHANGES refs at
  `:371,428,497` observed, not judged).
