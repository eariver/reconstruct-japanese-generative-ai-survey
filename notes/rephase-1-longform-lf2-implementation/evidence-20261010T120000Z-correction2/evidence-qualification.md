# LF-2I R2 correction evidence qualification

2026-10-10. Correction implementation Co-Worker closeout for root R2
 findings (C1 + S1–S4 + E1–E3). Not independent review. Old 44-method result
 is historical evidence only — no PASS transfer claimed.

## Source identity (fixed final hashes)
- Design copy `/tmp/opencode/jgas-lf2-design-20261009T113013Z`, HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c` (unchanged, no commits),
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- Changed this round (2 files, same path budget — publisher + integration test):
  - `scripts/survey_longform_semantic_publication_v2.py`
    `71ef7b976684e0f88407c24ba3ed8d6f51135be2b7a048b2655dd5b777ef5b40` (was `1020e4…`)
  - `tests/test_survey_longform_publication_integration_v2.py`
    `61a3491a572f113e6b2c94b897e5dde2ac234290c4925ceb1c1f0e52ebdd6ad9` (was `16864f…`)
- Unchanged (7 files, all modes 664): gate runtime `e73058…bbe4`, gate schema
  `fe4a96…13322c`, receipt schema `4dadf8…3e8ca`, reader schema `7bae9d…d0643`,
  derivation `c09c55…41149`, helper `d480e1…97d3c2`, LF-1 test `ce6874…f913`.
- Status at close: exactly 2M + 7A source entries plus `__pycache__` side
  effects (listed separately in manifest, never claimed untouched).
- No candidate/reconstruct commits, branches, refs, or fixture-DB writes; no
  original/LF1/verify-copy/409-DB mutation; no network, Production actions,
  subagents, DM021 reason, or `EXCEPTION_*` path. `config/*.json` untouched.

## What changed per finding
- **C1**: drafting archive (`context["archive_path"]`, receipt
  `authored_refs[1]`) added to `_snapshot_inputs` (strict lexical containment)
  and every `_recheck_snapshot` window. Both timing windows proved by
  seam tests (c) before-writes and (e) builder/before-receipt.
- **S1**: pre-validation raw capture (`_capture_lexical_bytes`) for State and
  publication input, capture-verify after derivation; review raw capture before
  semantic validation with verify-after; all rechecks re-read actual on-disk
  files (State, input, archive, reader file, review, accepted refs, closure) —
  no frozen-buffer or memory-vs-memory comparisons remain. Proven by seam
  tests (a) input validation seam, (b) review validation seam (valid-but-
  drifted review), (c) snapshot seam, (d) pre-write seam.
- **S2**: publication directory comes from the profile's raw `source_root`
  string via `_strict_dir_preflight` (no `_rel` resolve-before-check anywhere
  on this path); existing-path kind validated before mkdir. Proven by E2E
  pass1 (`publication/` → outside sentinel, no target writes) and E2E pass2
  (`v2/` → alternate sentinel) plus the retained direct-helper unit.
- **S3**: existing-output `lexists` checks and the before-writes recheck run
  BEFORE any mkdir; narrow post-mkdir revalidation only. Pass1 same-byte
  reuse classifies: no source set → healthy reuse; complete set → full
  receipt-replay gate (reuse iff valid); partial/inconsistent → refuse.
  Seams (c) asserts no survey-dir side effect on pre-mkdir refusal.
- **S4**: installed receipt must equal the prevalidated prospective record
  (`_assert_receipt_matches_prospective`, all bindings + closure/contract/
  commit + digest); final on-disk dependency recheck runs AFTER construction
  immediately BEFORE install; builder-drift refuses with retained partials and
  no receipt. Receipt write/close failure reports the partial receipt path in
  the retained list; pass1 surface failure reports the surface path when created.
- **R4**: controlled close fault (full bytes installed, close raises) and
  receipt-install fault (partial receipt bytes, then failure) with retained
  bytes/paths, sibling preservation, and retry-refusal BEFORE cleanup.
- **E1**: `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`,
  `GIT_ALLOW_PROTOCOL=file` forced for runner git AND children (plus
  `PYTHONDONTWRITEBYTECODE=1`, `GIT_TERMINAL_PROMPT=0`); routing/optimization
  overrides (`GIT_*`, `PYTHONPATH/HOME/STARTUP/OPTIMIZE`) rejected before
  every candidate git operation; `sys.flags.optimize==0` enforced; child argv,
  interpreter, git version, and env recorded. No installs, no network.
- **E2**: prior toy replaced (preserved only in old packet). Real proofs on
  three NEW independent full disposable composites (9 files + own Git DB +
  own HEAD, exact 2M+7A overlay shape) with the SAME guard code: A wrong
  source → nonzero, child never launched (sentinel absent); B correct source,
  exit-7 child → child exit observed, driver nonzero, postguard recorded;
  C child0 (sentinel proves launch) + drift → postguard nonzero. Exclusive
  `proofs.log`, numeric codes, no candidate canary, no full-suite repeat.
- **E3**: exact SAVED `complete-overlay.patch` (clean M diff + clean new-file
  diffs, no markers) applied as saved (`--check` then apply, both exit 0) to a
  NEW `cp -a` byte-copy (no archive/clone) of ORIGINAL clean 409
  `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` at
  `/tmp/opencode/jgas-lf2i-409bytecopy-20261009T203526Z`: pre HEAD 409 clean,
  inert origin, no alternates, 109 objects with 0 shared inodes; post HEAD
  still 409, status exactly 2M+7A, all-9 bytes and physical modes match,
  `ls-files -s` logical modes recorded.

## Verification (new runner `run_lf2i_correction2.py`)
- Proofs PASS (A/B/C as above); pre/post identity PASS (all-9 hash+mode pins,
  HEAD/tree/parent, exact 2M+7A set); child exit 0, no timeout.
- Suite: **42 tests OK in 1698.663s** — full focused LF-2I integration module
  (12 methods incl. new `test_dependency_snapshot_seams_and_receipt_faults`)
  + Gate module + 3 LF-1 loader controls at the fixed final hashes above.
  Full-repo syntax/compile sweeps dropped as unaffected (no schema/config
  change); old 44 not transferred. `run.log` holds raw per-test outcomes.
- Normal healthy FROZEN/RELEASED readback and both same-issue manuscript
  stage-Gate backstops retained green; DM021 remains explicit non-goal
  (no `EXCEPTION_*`/`REVIEWED_EDITORIAL_CORRECTION` paths added).
- Earlier reviewer source/evidence PASS overclaims corrected here: prior
  bounded-PASS notes on R3/R7/R8 are superseded by the C1/S1–S4/E1–E3 defects
  above and their new proofs. No independent acceptance is inferred.

## Preservation / limits
- `preserved-9/` + manifest: exact pre-edit bytes/modes/hashes of all 9 files.
  Old packet (incl. prior complete patch, dev logs, attempt1 env failure)
  intact; `attempt1-proofsetup-failure/` preserves this round's proof-harness
  setup failure (single-commit disposable repo lacks `HEAD~1`; fixed with a
  root commit, rerun green). `__pycache__` side effects never blindly deleted.
- New unique dir, exclusive-write evidence only, no overwrites.
- Whole candidate NOT_READY; step4/B3 OPEN; canonical audit unstarted.
  Stop for root code/oracle/evidence review + same independent reviewer final
  resolution. No automatic next unit; no Commit/Push (ordinary reconstruct
  commit remains Human-owned).
