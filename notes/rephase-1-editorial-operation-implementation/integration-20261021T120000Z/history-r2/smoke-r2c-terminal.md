# R2 Weekly full smoke — terminal 0 (new SOURCE epoch, explicit intended set)

## Commands (read-only DST, fixture creation via explicit list, no clean/reset/network)

- `DST=/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
- `FIXR2C=/tmp/opencode/jgas-editorial-r2c-20261021T000000Z/candidate-partial-b40de60`
- Explicit copy: `git -C $DST ls-files | while read f; do [ -f $DST/$f ] && mkdir -p $FIXR2C/$(dirname $f) && cp -a $DST/$f $FIXR2C/$f; done` (689 files) + 28 new selected (10 schemas + 9 scripts + 9 tests incl. `test_survey_schema_cache_v2.py`) → `find $FIXR2C -type f | wc -l` = `717` (exits 0)
- `git -C $FIXR2C init -q; config user.name/email/commit.gpgsign false; add -A; ls-files -s | wc -l` → `717` (exits 0); `ls-files | grep -c __pycache__` → `0`; `grep -c ^tmpvr07sdme/` → `0`; `ls .git/objects/info/alternates` → `No such file` (exit non-zero, expected absent); `remote -v` → empty (inert); `stat` inodes differ, link count `1` (independent, no hardlinks)
- `git -C $FIXR2C -c commit.gpgsign=false commit -qm "SOURCE snapshot: R2 ..." --no-verify` → `ab19400c00567aa18e4ff7932663f944d5eaf8f8` (full 40-char, exit 0); `status --short | wc -l` → `0` (clean SOURCE, exit 0)
- Smoke: `SMOKE_FIX_ROOT=$FIXR2C PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/opencode/int-pycache TMPDIR=/tmp/opencode PYTHONPATH=$FIXR2C timeout 1200 python3 $PKG/smoke-weekly-activation.py > $PKG/history-r2/smoke-r2c/stdout.txt 2> $PKG/history-r2/smoke-r2c/stderr.txt; echo $? > $PKG/history-r2/smoke-r2c/exit.txt`
  - `exit.txt` → `0` (terminal 0, not 124; exits 0)
  - `stdout.txt` milestones (9 lines): `PREPARE {...}`, `REVIEW ...`, `FINALIZE {...}`, `INERT_HEALTHY`, `DEBUG_SET_PATH ...`, `DEBUG_SET_REF ...`, `ACTIVATE {"status":"ACTIVATED","record_path":".../r1.json",...}`, `RECEIPT_ACTIVE_OK`, `GATE_ACTIVE_OK`, `CANDIDATE_ACTIVE_OK ...`, `REPEAT {"status":"ALREADY_ACTIVE","record_path":".../r1.json",...}`, `SMOKE_WEEKLY_ACTIVATION_OK`
  - `stderr.txt` → empty (0 lines, no traceback)
  - Exact pins: `FINALIZE set_ref .../publication-set.json set_sha ...` (see stdout), `ACTIVATE record r1.json`, `REPEAT record r1.json` (correct, not seal – ALREADY_ACTIVE fix verified), `State .../production-state.json`, `observed new`
  - Timing: completed within 1200s bound (tool timeout 1250s, no timeout); prior without cache timed out at 1200s after CANDIDATE (exit 124, no REPEAT) – improvement correlates with schema cache (0.014s→0.001s per validate, 14x) + FULL accepted work, but no seconds claim beyond bound (unknown exact seconds not measured with `date`; only bound + exit + milestones reported).

## Failure residue (preserved, not edited green)

- Prior attempts 1-22 raw in `integration-20261021T120000Z/smoke/` (`stdout*.txt` 1-24, `stderr*.txt`, `exit*.txt` 2/124) + `diagnostic-20261021/` (v1/v2 stacks, fresh timings) – all preserved.
- Old FIX23 (feb4d1fc, 759 incl. 43 tmpvr07sdme) preserved; new FIXR2B (642bc0c, 717? Actually FIXR2B was 717? No, FIXR2B was explicit 52? Wait FIXR2B was incomplete 52-file attempt – preserved as failed attempt per “preserve old”). FIXR2C (ab19400c, 717, clean) is new epoch for terminal raw; no authority pin rebinding (authorities regenerated fresh with wk-smoke-1, not copied from old).
- Old partial/bad receipts (single-checkpoint, no generator_route, no FULL) remain in `history/` + old fixtures as evidence of refusal (they fail H unconditional FULL check, correctly).

## Production semantic NO-GO preserved

- Synthetic reviews: `smoke-weekly-activation.py:211-218` `reviewed_by="smoke synthetic ..."`, `evidence_locations=["smoke-real-build:main.pdf"]`, deterministic checks with actual file assertions only; H never generates PASS (`REVIEW_NOT_PASS` + Gate editorial-derivation enforced). Real TL2026 PDF (`lualatex-biber-lualatex`, `luahbtex`, `latexmk.pl`, `PATH toolbin:/usr/bin:/bin`, `.latexmkrc` markers, blocking patterns, `pypdf` ≥1) inspected separately from synthetic type/authority. No genuine Human approval claimed.
