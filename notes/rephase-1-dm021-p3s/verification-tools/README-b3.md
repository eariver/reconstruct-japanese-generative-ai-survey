# P3S verification-tools B3 — DRAFT docs (NOT EXECUTED as suite, root readback)

2026-10-18. CoWorkerB tooling author B3, single worker, no delegation.
B1/B2 bytes/reports/raw preserved untouched (B2 shas verified unchanged:
run `4a8e2ac0…`, gen `759f69f2…`, proof `1b2b9622…`; B3 bases copied
byte-identical via `cp -a` then corrected with exact replacements).
NEW files only: 3× b3 scripts + launcher + this README-b3. No
candidate/source/test/schema edits; source author otherwise waits.
No network/commit/push. No PASS claims; root re-readback required.

## 0. Author error correction (explicit, required)

- B2 smoke-r5 `run_p3s_b2.py` crashed at line 356 with
  `AttributeError: module 'os' has no attribute 'lexists'` — `os.lexists`
  does not exist; the correct API is `os.path.lexists` (verified:
  `hasattr(os,'lexists')==False`, `hasattr(os.path,'lexists')==True`).
  I authored and the independent B2 reviewer repeated the same wrong call
  on every existence gate (runner 7, gen 6, proof 8 sites); both missed it
  because neither executed even `--help`-adjacent paths. Corrected in B3.
- `smoke-status.txt:56` ("Caught by main() generic except ... launch_rc=1")
  is FALSE and I do not repeat it: line 356 sits in `main()`'s pre-try
  validation gates (before outdir creation/try), so the AttributeError
  propagated uncaught — full traceback, Python exit 1 implied, NO
  `terminal[]`, NO `run_p3s_b2.exit`, NO PRE/POST observe, NO child.
  The nohup-shell `wait` then reported 127 for *wait itself* ("not a child
  of this shell"), not the runner. No actual runner rc was captured in
  smoke-r5; I record none and fabricate none (packet line 41 states this
  honestly). The B3 launcher below exists precisely so the next smoke
  captures the true rc from the same parent process in all cases.

## 1. NEW files (DRAFT)

- `notes/rephase-1-dm021-p3s/verification-tools/run_p3s_b3.py` (691 lines, 6409 nodes, sha256 `dc695ace…`)
- `notes/rephase-1-dm021-p3s/verification-tools/gen_complete21_b3.py` (756 lines, 6809 nodes, sha256 `82445836…`)
- `notes/rephase-1-dm021-p3s/verification-tools/proof_apply21_b3.py` (921 lines, 7868 nodes, sha256 `9e868a16…`)
- `notes/rephase-1-dm021-p3s/verification-tools/launch_p3s_smoke_b3.py` (264 lines, 1928 nodes, sha256 `a2b5b4c3…`)
- `notes/rephase-1-dm021-p3s/verification-tools/README-b3.md` (this file)
- Diagnostics packet `notes/rephase-1-dm021-p3s/tooling-b3-nsdiag-20261018T075057Z/`
  (`diag.cmds.txt`, `diag.record.json`, `d1.help.*`, `d2.missing.*`, `d3.collide.*`)

AST: all four `ast.parse` OK (`PYTHONDONTWRITEBYTECODE=1`, absent
`PYTHONPYCACHEPREFIX`, verified still absent); no `return` inside any
`finally` (AST-verified); stdlib audit: every other `os.*` call in B3
(`environ/lstat/scandir/killpg/getpid/getcwd/sep`) exists — `os.lexists`
was the only bad attribute.

## 2. B3 deltas vs B2 (line refs, B3 files)

- **Namespace fix (all three):** every `os.lexists` → `os.path.lexists`
  (runner L17–18 doc + L356/359/362/365/370/373 gates + L569 post;
  gen L25 doc + L326/329/332/335 + L441 multi-gate + L533;
  proof L27 doc + L335/340/343/346/349/352/355 + L581). Self-names
  `*_b2` → `*_b3` (usage/outputs/terminal ids). B2 files keep the old
  text deliberately (evidence of the defect).
- **Actual detached-HEAD guard (all three, pre AND post):**
  runner `_observe` runs `git symbolic-ref -q HEAD` separately (rc
  preserved, L183–192) and `_check_pins` fails closed unless rc==1
  (L245–248); gen identical in `_observe_source`/`_check_source`
  (L223–232 / L259–264); proof new `_check_detached` (L124–132, rc 0/1
  accepted, else ProofFailed) enforced on active pre-guard
  (L~560–575, primary) and source-post (L~870–890, secondary).
  Attached worktrees (rc 0) now refuse instead of passing doc-only.
- **Canonical inherited18 keyset (all three):** new `INHERITED18 =
  MODIFIED3 | NEW15_INHERITED` (runner L100; gen L90; proof L93);
  exact set-equality check before per-key drift (runner L272–276;
  gen L275–280; proof L~550–556). Wrapped/partial/extra-key supplied
  maps fail closed instead of being iterated as authority.
- Existing static21/cache guards unchanged (21 keyset + entry shape +
  live match, 84 cache per-file, 105 rowset+len+dup, index-empty,
  HEAD/tree pins).

## 3. Durable launcher (`launch_p3s_smoke_b3.py`)

Same-process wrapper for the root-selected smoke (worker run task uses
it): reserves `launch.cmd/.pid/.stdout/.stderr/.exit/.record.json` +
`record-done.json` exclusively in the packet logdir (refuses 40 if any
exists); writes raw cmd/record BEFORE spawn; spawns
`[sys.executable,-u,runner,...]` with direct held `xb` stdout/stderr,
`start_new_session=True`, sanitized env (allowlist + redaction count,
no full env leak); `wait(timeout)` in the SAME process so early
tracebacks yield a true recorded rc; timeout TERM→KILL + reap (124);
interrupt reap (130); flush/close→5, exit/record→6 upgrades only from 0.
Raw-before-launch + same-process exit close the smoke-r5 wait-127 gap:
no `nohup`, no cross-shell `wait`.

## 4. Cheap no-candidate diagnostics (NEW packet, actual raw)

Fixture `/tmp/opencode/p3s-b3-nsdiag-20261018T075057Z/` (exclusive; holds
only pre-created `collide/`; cache-prefix verified still absent after).
Clean inherited env (no `GIT_*`/`PYTHON*`/`TMPDIR`); forced
`PYTHONDONTWRITEBYTECODE=1`, absent `PYTHONPYCACHEPREFIX`,
`TMPDIR=/tmp/opencode`. Python 3.14.4. No candidate paths exist or were
touched; no GEN/PROOF/test execution; no network.

- D1 `run_p3s_b3.py --help` → exit 0, stdout 940 B, stderr 0 B
  (`d1.help.*`). Proves module import (no top-level namespace error).
- D2 missing `--manifest` → exit 40,
  `RUNNER_REFUSAL: manifest missing/non-regular: .../no-such.json`
  (`d2.missing.*`). Executes the exact fixed line (old B2 L356 crash
  site) and refuses cleanly — no AttributeError.
- D3 pre-created outdir → exit 40,
  `RUNNER_REFUSAL: outdir exists (not overwriting, ...)`, stdout 0 B
  (`d3.collide.*`). Executes the fixed collision gate; candidate arg
  (nonexistent) never reached — candidate untouched.

Claim: namespace-only (fixed lines execute and refuse correctly). NOT
runtime code acceptance, NOT a smoke verdict, NOT a 105-row/21-file
claim — full guards still await execution-time pins after root
readback and CoWorkerA return.

## 5. Precise limitations

- B3 unexecuted as suite: no PRE/POST observe, no child, no GEN/PROOF,
  no timing/byte verdicts; root-selected smoke (via launcher) still
  requires explicit authorization + final static21/pins + different
  exclusive outdirs per run.
- D1–D3 prove only that the repaired early paths import and refuse;
  they do not cover git/observe/child/post paths, binary diff capture,
  or patch application.
- Fixed HEAD/tree/index/detached/105-row predicates are enforced at
  execution only; half-written static21 was deliberately never read here.
- Pre-outdir refusals remain console-only (no durable location); all
  post-reservation failures POST with primary+secondary preserved.
- Tools are one-off exact-run evidence, not universal rerunners and not
  candidate/Production authority.
