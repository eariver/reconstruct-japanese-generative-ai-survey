# SP r6 prepare-only — short commands note (review only, no execution yet)

Narrow r6 successor of r5 (r5 preserved untouched). Still prepare-only: no
disposal/removal, no retry, no auth-file framework. Root re-review required
before prepare; this note + tool + generated manifest are the review surface.

## Files (this packet only)

- `sp-prepare-generator-r6-20261104.py` — stdlib-only pin generator (no project
  imports, no git, no network). R5 generator + one structured addition:
  triangulated test pins (delivered/intended vs live e84 vs r3-recorded).
- `sp-prepare-expected-manifest-r6-20261104.json` — 395713B
  `6507804dd4b16ff93f6513773a1adb6a47d7cc3db628b6f1a1c1f9efb97d6bb7`,
  generated exit 0, `clean:true`, `unresolved:[]`. Old authority pinned
  unchanged (same intended set, SP tree, supplement30 as r5).
- `sp-operator-prepare-r6-20261104.py` — prepare-only tool. Fixes: recorded
  physical modes for all771 (0o775 executable honored), test d486 triangulated
  (never skipped); 771 preflight before imports + terminal prepost recheck;
  terminal FULL tree/gates/refcheck; lexical writer callsites + retention
  ancestor validation (snapshot checks, no race claim); manifest self-pin at
  invocation + same-hash recheck before READY; `_finish_authority_phase` close
  with initial pins/context + real owner inside facade; scratch absent-required
  (API creates it). Builder unused (deletes owned output on failure).
- `sp-prepare-launcher-r6-20261104.sh` — unique EXCLUSIVE bundle dir
  (`mkdir`, no `-p`), no git. Captures argv/cwd/env-subset/timestamps +
  tool stdout/stderr/exit.
- r4/r5 preserved untouched, never executed.

## Commands (DO NOT RUN until Root authorizes AFTER independent re-review)

Generate (already run once; recorded output above):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-generator-r6-20261104.py \
  --repo-root .rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work \
  --resume notes/rephase-1-operational-rehearsal-resume-20261104 \
  --intake notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z \
  --supp-intake notes/rephase-1-operational-rehearsal-20261101/publisher-intake-supplement-20261101T172535Z \
  --delivery-manifest notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json \
  --out notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-expected-manifest-r6-20261104.json
# exit 0, clean true. Re-run is read-only; review the manifest before use.
```

Prepare (AFTER review + one bounded Root authorization; STOPS at READY):

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-launcher-r6-20261104.sh \
  --new-supplement-id r6-sp17-YYYYMMDDTHHMMSSZ \
  --retention-dir notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-YYYYMMDDTHHMMSSZ \
  --expected-manifest-sha 6507804dd4b16ff93f6513773a1adb6a47d7cc3db628b6f1a1c1f9efb97d6bb7
# exit 0 → READY.json in retention; exit 2 → PREPARE_REFUSED + FAILURE.json, partials preserved, no retry loop.
```

The `--expected-manifest-sha` above is the externally recorded command hash;
the tool refuses when the manifest file differs at startup or before READY.

## Failure handling / bounds

Any mismatch vs original intended files refuses (never quietly accepts newly
observed source). Any refusal: preserve staged/retained partials + journal,
report exact partials, require a new bounded observation/decision. No
auto-restore/retry, no State/CP/Human/config/schema/source/test writes, no
old-output overwrite, no glob/force. Disposal + retry are SEPARATE future
decisions. Helper green ≠ project runtime proof; semantic re-review of
corrected DATA still required. WholeNOT_READY/step4B3OPEN/auditunstarted/
DM021+022OPEN. Human Commit Point — stop.
