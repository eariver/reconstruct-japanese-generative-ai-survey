# W34 resume r2 — source review note (DO NOT EXECUTE)

r2 preserves r1 (`w34-operator-resume-20261105.py` 30896B `77b26d79...`)
untouched. Minimal fixes per Root + independent findings; no broad features.
No active writes, no project execution/network/Git/Production while authoring
(stdlib-only checks). Awaiting independent review + Root auth.

## Fixes vs r1

- Pre-import fail-closed already present in r1; r2 keeps it verbatim.
- After-import 10-module match (`rn.schema_gate` 10th + no `__pycache__`).
- Single umask read/restore (`os.umask` ×2: read + restore, mode
  `0o666 & ~prev`); r1 double-call left mask 0 with wrong mode.
- Supplement 428 rows derived from validated supp FILE `ce6f...` (verify
  file hash first, then exact manifest Raw pins, 428/425); no empty-default
  skip (r1 `manifest.get(...,[])` silently passed on missing key).
- No fictitious view validation: preflight retains actual canonical card
  bytes (`core.json_bytes`) outside active + honest card-only claim (real
  view proof left to full branch via accepted path).
- Full shared guards (baseline+1/source771/State/absent2/backups/supp/
  input/self-manifest SAME hash) run BEFORE READY even with --prepare-only;
  READY manifest field binds externally recorded hash (no fresh-read reseal).
- Distinct journals: `preflight-journal.json` (preflight) vs `journal.json`
  (final); second O_EXCL write can no longer collide.
- Full branch reuses proven W34 dispo-r3 post-layout/actual validators via
  explicit pin `48be5879...` (stdlib-only import verified; its disposal never
  executed), with current+old2 inventory, exact old accepted sets,
  EFFECTIVE 439 paths, card/archive/umask bindings.
- Failure logger absolutizes packet path before best-effort write without
  masking the original error; launcher always captures stdout/stderr/exit.

## Files (packet only)

- Wrapper r2 `w34-operator-resume-r2-20261105.py` 37213B
  `9f27a6c39533888f1e70e22ee28d7c448ffef5d0e7b4c892141a84a66a6546fe`
- Launcher r2 `w34-resume-launcher-r2-20261105.sh` 1095B
  `ea7c0427fd34af7050c4aa204eb79723e955d53a79ef1a1c0db6c7eb639847af`
- Expected manifest (unchanged v1) `w34-resume-expected-manifest-20261105.json`
  807341B `13a38710...` (machine current 1780/80 derived/crosschecked)
- Oracle `w34-resume-r2-oracle-checks-20261105.py` 4301B `559e07f4...`
  + raw 343B `b8059e88...` — **9/9 PASS**
- r3 input `15e87eef...` / preflight READY `473bf85b...` unchanged.

## Oracle (stdlib source-read, no project runtime)

r3 covers ALL 409 exact task targets (0 mismatches); tampered c001 target
detected pre-run with no active writes; O_EXCL journal collision refused;
tampered manifest refused (SAME hash); guards-before-READY, card-bytes (no
view fiction), distinct journals, single umask restore verified by AST +
behavior. Truthful exit 0; raw preserved. No fake views.
