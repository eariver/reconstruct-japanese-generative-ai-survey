# W34 resume r3 — source review note (DO NOT EXECUTE)

r3 preserves r2 (`w34-operator-resume-r2-20261105.py` 30896B `77b26d79...`)
untouched. Fixes full-branch NameErrors + adaptation bugs found by Root +
independent review (source-only, no execution yet).

## Fixes vs r2

- Bare names fixed: `LEDGER_REL`/`COMP_REL` module globals added;
  `_derive_old_accepted_dirs_resume` defined (ORIGINAL pinned w34-prepare
  manifest `cede7e46...` hash-verified, frozen `w34_tree_full` + accepted
  pin parents, returns DIR NAMES per D3 convention — never calls D3's
  version which requires `w34_tree_full` the resume manifest lacks, never
  fakes `accepted_evidence_dirs` defaults).
- Post-layout adaptation: resume baseline 1780 excludes old2 (CONTINUE
  ABSENT), so D3 unadapted fails `exp_old None` (proven by oracle). r3
  supplies explicit observation-only expected old2 from PINNED backups
  (no claim originals exist live); D3's preserved loop already skips old2;
  regen verified vs backup pins. Old dirs asserted pre-READY and re-verified
  pre-run (P1 vs full-branch consistency gate).
- Terminal post pins ADDED after final validators (source771 + State +
  whole current baseline inputs/supp + manifest SAME hash + new
  Ledger/Completeness expected post pins); before only pre-run existed.
- Umask single read/restore kept (as r2); distinct journals
  (`preflight-journal.json` vs `journal.json`) kept; failure logger
  absolutizes packet path best-effort without masking original.
- Full branch reuses proven dispo-r3 post-layout/actual validators via
  explicit pin `48be5879...` (stdlib-only import verified; its disposal
  never executed), EFFECTIVE 439 paths, archive/umask bindings.

## Files (packet only, no active writes)

- Wrapper r3 `w34-operator-resume-r3-20261105.py` 44856B
  `9072acff864a718ba24f1c31dd29176686f25fc73ec428107b18a53fdcf42f43`
- Launcher r3 `w34-resume-launcher-r3-20261105.sh` 1074B
  `c25008bb736aeb00aeac73c53b572c7c0e88c5f66e0d6410b2e94c282ea18398`
- Oracle `w34-resume-r3-oracle-checks-20261105.py` 10885B `15bceeda...`
  + raw 321B `a7c198c2...` — **6/6 PASS**
- Manifest unchanged `w34-resume-expected-manifest-20261105.json` 807341B
  `13a38710...`; r3 input `15e87eef...` unchanged; baseline 1780/80 intact.

## Oracle (stdlib only, no project runtime/Git)

Unadapted D3 on resume-shaped fixture MUST fail (documents reported bug
class); adapted path with observation-only old2 + DIR NAMES MUST pass
(439 rows/2 tasks bindings verified); r2 fail-closed-before-import +
schema10 structural; real R369/E439 + r3 packet bytes source-read.
Truthful exit 0; raw preserved. No fake views (card bytes retained,
no view-shape claims).

## Unresolved defects / limits

- Full branch (post-READY through `rn.run` + post-verify) is source-reviewed
  only; NEVER executed here. Real-run risks (runner-internal, timing,
  environment) remain for Root-authorized execution with fresh re-review.
- New outputs/modes are predictions from helper contracts + umask, not
  measured artifacts.
- SP anchors checked stable-only; whole SP NOT frozen (preflight may
  complete soon) — explicit pre/post SP snapshot at execution time.
