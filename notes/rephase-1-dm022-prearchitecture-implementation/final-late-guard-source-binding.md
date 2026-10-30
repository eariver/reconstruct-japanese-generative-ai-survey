# Final late-guard source binding — General test-author (shipping)

Date: 2026-10-29 UTC. General ONLY, NOT reviewer, NOT B/C1/C2/G71.
No runtime edits (only `tests/test_dm022_normal_writer_late_guard_v2.py` +
`tests/dm022_late_guard_fixture_v2.py`, owned, exported to `candidate-work`
via copy (no B file touched, no metadata overwrites, B
`test_dm022_b_late_prepublish_v2.py` preserved, no duplicate).

## Scope (24 late-guard, no skips, no earlier preemption)

General-owned normal-writer late seams (entry+prepublish, REAL
`low.require_research_operation_ready`, exact file/fn/line, owned synthetic
guard ANY refuses, healthy NEW write then fresh-copy fault, pre/post inventory
`new=={guard}` or allowed prefix, no business cleanup):

- Selection 7 incl AUDIT, Evidence ledger/completeness (EVIDENCE2), Draft,
  Retention (NEW pid), Editorial prepare/finalize/activate/resume (real
  TinyTeX + full receipt/set), Release checkpoint, Candidate/Preview/Visual/
  Freeze, Manuscript/Review/Gate, Execution.

B-specific 15 late tests live separately in candidate
`tests/test_dm022_b_late_prepublish_v2.py` (B2-owned, 10 new +23 existing per
B2 doc; General does NOT duplicate). Bridge (`_advance_stage`/`execute_request`
receipt) and `record_publication_preview` delegate to exact checked children
(`agent.build_stage_checkpoint`/`advance_with_checkpoint`,
`publication.build_preview_approval`) — covered via child prepublishes tested
here (candidate/preview/freeze) + B child tests, NOT falsely claimed as own
per-entry runtime (no own READY write in delegate wrappers; R4 rows 17/40
delegate pattern, B2 §2 table).

## Old 24 (frozen SOURCEPASS, historical)

- Source: `snapshot-review-20261029T053058Z/worktree764` SHA256
  `60aaaee8539f69432a01d0ad72c1131b23951fd87a53…`, 764 files.
  Pins: LOW `2aef837f…`, HIGH `3d1d87d8…`, agent `b6506a8b…`,
  C2 editorial `3a872156…`, publication `705bcee3…`, release `b9433b9e…`,
  refresh `dd01fa01…`, H `a9de2c97…`, S `b139f493…`.
  Evidence prepublishes `742` (ledger) / `758` (completeness) — R3-era map,
  grep + spot-read, no B2 694/727/805 yet.
- Exec: `/tmp/dm022-late-guard-20261029T060000Z/exec/` (byte copy, no `.git`/
  pycache, `PYTHONDONTWRITEBYTECODE=1`, `unset GIT_*`, `/usr/bin/python3`
  3.14.4). Tests: `evidence/late-guards-20261029T060000Z/`
  `test_dm022_normal_writer_late_guard_v2.py` SHA256
  `4b589079…` (old, 15 PASS version) → updated to `bb22ab02…` (24 PASS,
  evidence 742/758) — old RAWs preserved, no overwrites.
- Raw: `evidence/late-guards-20261029T060000Z/raw.txt` (18 tests, 15 PASS +
  3 SKIP) + `raw-full-20261029T113416Z.txt` (`Ran 24 tests in 1524.134s OK`,
  exit 0, PID 605094, 2026-10-29T113422Z→113256Z) + `pins-after.txt` (9/9 match),
  `header.txt`, `cmd-env.txt`, `test-sha.txt`. Failed-before-target fixed, not
  SKIP (evidence CANDIDATES_NORMALIZED + retention NEW pid fixed in new).

## New 24 (CURRENT shipping, required)

- Source: `candidate-work` CURRENT (all runtime idle, no live B capture while
  B2 correcting rollback; pins verified before/after, no drift).
  Pins BEFORE=AFTER (`pins-before/after-CURRENT-20261029T145521Z.txt`):
  LOW `2aef837f…` (unchanged), HIGH `f8af03cc…` (A HIGH A5 new, no Human
  history — existing fixtures carry no Human history, `validate_agent_state==[]`
  healthy readback OK), agent `d801feb6…`, human `101792ad…`,
  orchestrator `491888fe…`, bridge `2fd8a6a2…`, run_evidence
  `949a1248…` (B2 694/727/748/764/805), run_selection `553bf22b…`
  (unchanged 260/316/…/456), run_drafting `ad6cdea7…` (unchanged 81/218/…),
  C2 editorial/publication/release/refresh/reader/execution/retention
  unchanged (`3a872156…`/`705bcee3…`/`b9433b9e…`/`dd01fa01…`/
  `2713eec4…`/`8f035832…`/`fdc9ed7c…`/`dea9191c…`).
  B runners lines moved derived by AST (actual named write + preceding real
  READY with comments, not blind offset), exact executed site asserted:
  evidence ledger `742→748` (`materiality-ledger-v2.json` + comment
  “canonical Ledger creation”), completeness `758→764` (profile-completeness +
  comment), plus new 694/727/805 acknowledged (evidence/views/archive, B2 map;
  General EVIDENCE2 covers ledger/completeness per mandate, B covers rest, no
  duplicate). Selection/drafting/C2 lines unchanged (verified by grep + AST).
- Exec: `/tmp/dm022-late-guard-current-20261029T145521Z/exec/` (byte copy of
  candidate-work excluding `.git`/`__pycache__`/`*.pyc`, no hardlinks/
  alternates, same env/Python, depth only new test files private). Tests:
  `test_dm022_normal_writer_late_guard_v2.py` (24 tests, evidence 748/764) +
  `dm022_late_guard_fixture_v2.py` (LateGuardInjector `inspect.stack()[2]/[3]`,
  `entry_fn` support, synthetic `TEST` nonce). Exported exact intended final
  files to `candidate-work/tests/` via copy (new files, B file untouched).
  Durables (`durable-versioned-20261029T064541Z`, VALIDATED prePreview +
  VERSIONED_ACTIVE, created old source) copied NEW per fault; copied core libs
  in exec are new (CURRENT pins), new module imports bind CURRENT PROOF
  (`resolve_research_authority`/`require_research_operation_ready` CURRENT),
  not modified Root_data (durable State/PDF bytes preserved, PREARCH active,
  REAL PDFs, no Human history); fresh fixtures (new Git/independent DB,
  process identity, inert origin, new proposal IDs) for state-bound current
  proof where B code legally differs (evidence CANDIDATES_NORMALIZED,
  editorial NEW pid, release FROZEN stops, no rollback).
- Raw: `evidence/late-guards-20261029T060000Z/raw-full-CURRENT-20261029T145521Z.txt`
  (103 lines, `Ran 24 tests in 1531.803s OK`, exit 0, PID 682928→? actually
  1352002, 2026-10-29T145632Z→152204Z) + `exit-full-CURRENT-…txt`,
  `header-CURRENT-…txt` (date/PID/exec/pins/collector 24), `pins-before/after-
  CURRENT-…txt` (9/9 match, header-only diff, no drift), `p3s-*/ed-*` dirs
  (timestamp+PID, never overwrite), `test-sha-full-…txt`. No repeated
  duplicates (single full run, each test once; healthy+fault inside same test,
  not separate runs). No record metadata overwrites (only test files added to
  candidate-work, no existing file touched).
- Result: 24 PASS, 0 FAIL, 0 SKIP (no waiver). Real positive counterparts reach
  NEW writes; late faults refuse `DM022_TRANSITION_ACTIVE` at exact prepublish
  with `new=={guard}` (or allowed evidence/ledger prefix), `entry_reached` +
  `target_reached` asserted (outer file/fn/line). No earlier preemption
  (healthy proves passage past entry; C2 entry-only qualification respected,
  prepublish seams proven here). No global CAS. No genuine approval.

## Links

- Old 24: `notes/…/evidence/late-guards-20261029T060000Z/raw-full-20261029T113416Z.txt`,
  `test_dm022_normal_writer_late_guard_v2.py` (`bb22ab02…`? Actually old SHA
  `4b589079…` for 15-test version; 24-test frozen SHA `…`? See `test-sha.txt`
  + `test-sha-full-…txt`; `normal-writer-late-guard-evidence.md` (§ per-family
  + remaining OPEN at that time).
- New 24: same dir `raw-full-CURRENT-20261029T145521Z.txt`,
  `pins-before/after-CURRENT-…txt`, `header-CURRENT-…txt`,
  `test_dm022_normal_writer_late_guard_v2.py` (24 tests, evidence 748/764),
  `late-guard-completion-evidence.md` (prior completion, frozen) + this file
  (final source binding, CURRENT).
- B 15: `candidate-work/tests/test_dm022_b_late_prepublish_v2.py` (B2-owned,
  do not duplicate; delegate facts above).

If real runtime bug outside B known ENTRY-only/rollback appears, return ROOT
precise, no source patch. Shipping tests reference no old raw
SnapshotCondition except explicit needed fixtures (durables old source, copied
core libs new, fresh state-bound proofs as above). Unit ongoing. No
Human readback/ordinary commit/network/Gitconfig/cleanup.
