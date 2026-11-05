# SP r5 prepare-only — short commands note (review only, no execution yet)

R4 rejected for active use (preserved untouched). R5 is PREPARE-ONLY: no
disposition/removal, no retry, no auth-file framework. All pins generated
programmatically from live bytes (generator below); zero hand transcription.
Corrected source: r4 input `0ee3187e…` + supplement `1221d293…` (D123 64-char
fix verified; still requires independent semantic re-review before Root auth).

## Files (this packet only)

- `sp-prepare-generator-r5-20261104.py` — stdlib-only pin generator (no project
  imports, no git, no network). Run once → reviewed manifest.
- `sp-prepare-expected-manifest-r5-20261104.json` — 394754B `592b0bef…`,
  generated, clean, `unresolved: []`. Binds: 771 intended files, full 552-file
  SP tree + 32 dirs, original authority, all30 Raw/packet pins + sidecar
  cross-check, corrected DATA SHAs, gates-absent/checkpoint/stage-scan evidence.
- `sp-operator-prepare-r5-20261104.py` — prepare-only tool. Phases: source
  precheck before imports → full pre-validation (zero active writes) → exclusive
  17 Raw + verbatim input + NEW supplement (stage + schema gate + FULL existing
  validator; builder NOT used — it unlinks owned output on failure) →
  package to RETAINED scratch + `validate_interactive_input` (no card/view
  mirror) → recheck → READY. LIVE sha via `repository_commit_sha(repo_root)`
  (isolated; mirrors `run():599`); State480 historical only.
- `sp-prepare-launcher-r5-20261104.sh` — unique raw bundle (no git): argv/cwd/
  env-subset/timestamps + tool stdout/stderr/exit.

## Commands (DO NOT RUN until Root authorizes AFTER independent review)

Generate (already run once; recorded):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-generator-r5-20261104.py \
  --repo-root .rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work \
  --resume notes/rephase-1-operational-rehearsal-resume-20261104 \
  --intake notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z \
  --supp-intake notes/rephase-1-operational-rehearsal-20261101/publisher-intake-supplement-20261101T172535Z \
  --delivery-manifest notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json \
  --out notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-expected-manifest-r5-20261104.json
# exit 0, clean true. Re-run refuses nothing (read-only); review the manifest first.
```

Prepare (AFTER review + one bounded Root authorization; STOPS at READY):

```sh
notes/rephase-1-operational-rehearsal-resume-20261104/sp-prepare-launcher-r5-20261104.sh \
  --new-supplement-id r5-sp17-YYYYMMDDTHHMMSSZ \
  --retention-dir notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-YYYYMMDDTHHMMSSZ
# exit 0 → READY.json in retention; exit 2 → PREPARE_REFUSED + FAILURE.json, partials preserved, no retry loop.
```

## Failure handling / bounds

Any refusal: preserve staged/retained partials + journal, report exact partials,
require a new bounded observation/decision. No auto-restore/retry, no State/CP/
Human/config/schema/source/test writes, no old-output overwrite, no glob/force.
Disposal + retry are SEPARATE future decisions (distinct checked operation +
normal `run()`), never implied by READY. Helper green ≠ project runtime proof;
semantic re-review of corrected DATA is still required. WholeNOT_READY/
step4B3OPEN/auditunstarted/DM021+022OPEN. Human Commit Point — stop.
