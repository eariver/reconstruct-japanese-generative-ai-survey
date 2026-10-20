# Targeted VALIDATED_DRAFT Gate refusal — terminal summary — 20261019T145007Z

Scope: root-required correction — NEG-S2 (`Publication Candidate does not bind exact…`,
line 555) is a Candidate backstop, NOT Gate-site evidence. This unit demonstrates the
actual Gate check (line ~572) at the VALIDATED_DRAFT stage on both routes, with a
late-fault injection into the real public `validate_stage`, then stops. No source
changes, no rebuilds, no commits, no Production actions. STOP for fresh author-independent
resolution (no full-suite rerun, no rebuild of passed builds).

## Fixtures (NEW, independent, no reuse of positives)

`jgas-supplement-fixtures-20261019T145007Z/{weekly,special}-supp7`:
`git archive HEAD` tracked707 + byte-copied `.git` from final22 SOURCE fixtures
(HEADs `51b0e42b…` / `9917a6ff…`, unchanged); 22/22 pins verified (21 static
`1c0e339c…` + style `035645ca…` 6569 B); `.git` dev:ino overlap 0 vs all other DBs;
no alternates/hardlinks; safe local config; no inherited `GIT_*`. No new commits
(same SOURCE HEADs). Prior supp/supp2/supp5/supp6 fixtures preserved untouched
(failure history + superseded attempts, never cleaned or reset).

## Method (per route; 41 exact operations each)

Accepted chain → DRAFT_COMPLETE → pass1 (surface byte-identical to original21 pins)
→ synthetic type-only pretex review → pass2 → trio hash-equal to recorded positive
pins (no rebuild) → REAL positive-run PDF/log/digest staged (hash-verified against
recorded transfer pins; basis recorded) → SAME exclusive helper transfer → exact
manuscript → Gate build+validate → receipt replays → deterministic QA bundle →
synthetic postrender reviews → NEG-S1 (DRAFT_COMPLETE advance with decoy manuscript +
decoy reviews + exact gate: refused, `expected …-decoy … got …reader-manuscript…`,
no-write verified) → healthy DRAFT_COMPLETE advance (checkpoint saved) →
decoy GATE via actual builder (bound to decoy manuscript; pretex review is
surface-bound so no review forgery needed) → NEG-G (below) → repair + healthy rerun
+ readbacks. Final state VALIDATED_DRAFT (no further advancement; positives already
cover RC→RELEASED).

NEG-G late fault: wrapper around actual `_merge_artifacts` calls the original first
(prior-artifact checks + merge complete, refs recorded), then overwrites ONLY the
validated gate file with decoy gate bytes (seam asserted == 1), then the real
`_validate_stage_semantics` runs. Result, both routes:
`StageValidationError: Reader-Surface Gate validation failed: Reader-Surface Gate
MANUSCRIPT_MANIFEST does not bind the exact expected Reader Manuscript`
(expected = active manuscript from merged refs, got = injected decoy gate).
Fault-present snapshot: EXACTLY ONE file changed (the gate), HEAD/status/diff
unchanged, no report written. Repair restored only the injected bytes
(sha-verified); same actual stage call then PASSED (report written as expected
diagnostic). Helper-level probe (`expected==decoy` on restored gate) recorded
separately as agreement evidence, NOT stage coverage.

## Transfer helper — exact behavioral delta (evidence-only, not shipping)

Old witness code (`shutil.copyfile` after `exists()`/`lexists()` preflight) was
NEVER exclusive: preflight-then-copy with a TOCTOU gap; the old
"absent-exclusive" wording is hereby retracted for all old copy paths.
`transfer_exclusive.py`: `os.open(dst, O_CREAT|O_EXCL|O_WRONLY|O_NOFOLLOW)` creates
atomically or raises `FileExistsError` (no takeover); source opened first (an
unreadable source leaves no destination trace); 64 KiB short-write detection;
fsync + close-error propagation; digest convention enforced BEFORE any write;
postread sha equality + digest-line check; `on_error(exc, written, dir)` callback
before re-raise; partials never cleaned. Same function drives positives,
conflict (`FileExistsError`, shas unchanged), failed build (`no built main.pdf`,
no writes), partial after-first-write (`PermissionError`; 3trio+1pdf inventory;
State/QA/bundle/candidate unchanged), and NEW-target restore (OK + postread;
partial preserved untouched). Raw in `transfer-controls.json` + per-control logs.
No validator stubs; faults are environmental I/O only.

## Counts and paths

- Targeted: 41 + 41 ops; NEG-G refused as intended ×2; seam == 1 ×2; no-write
  verified ×2; repair + healthy rerun PASS ×2; final states VALIDATED_DRAFT.
- Evidence: `weekly/special-neg-g-targeted2.txt` (exact error),
  `weekly/special-neg-g-snapshot-targeted2.json` (single-file delta + seam + refs),
  `weekly/special-decoy-gate-pin-targeted2.json`, `weekly/special-helper-probe-targeted2.txt`,
  `weekly/special-neg-g-healthy-targeted2.json`, `weekly/special-targeted-report-targeted2.json`
  (41 ops each), `special/weekly-validated-draft-checkpoint.json`,
  packet copies + 5+5 PNGs + `pdfinfo` (real-compiler bytes, no rebuild).
- Fixtures: `/tmp/opencode/jgas-supplement-fixtures-20261019T145007Z/{weekly,special}-supp7`
  (untouched except by their own run; no `.git` writes beyond the copied DB).
- Candidate source unchanged: HEAD `409b292…`, `4M18A22`, style sha `035645ca…`.
- Real post-fix visual inspection still not done (rasters are inputs for the
  independent visual inspector). No Human approval, no adoption, no audit claims.
