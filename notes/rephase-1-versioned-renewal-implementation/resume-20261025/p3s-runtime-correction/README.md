# P3S runtime-correction — AUTHOR P3S compatibility + test-harness repair (no CommitPoint)

2026-10-25/26. Whole unit `f84fcf5` ongoing, no CommitPoint. Candidate
`.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`
source 740 (H `6fe86e`, P1 `825dba`, PUB `3f4039`, S `20f63e`, HIGH `9a0469`,
Reader `098a2c`, edpub `85814124`, archive test `5e5a`, `.latexmkrc` `18199fd`).
OWN `scripts/survey_editorial_staged_source_v2.py` + narrow testcase helper
ONLY if necessary + new dedicated tests. Other authors runtime P2R none yet,
no shared source changes elsewhere.

## 1. Root cause (actual import-graph inspection, no blind preload)

- P3S top imports 8 modules; top-level transitive runtime closure = 30 modules.
- Missing at runtime (top-level only, not function-local): 6 =
  `survey_discovery_v2`, `survey_x_intake_v2`,
  `survey_editorial_current_authority_v2` (P2V, already conditional-skip),
  `survey_versioned_renewal_history_v2`, `survey_versioned_renewal_source_v2`,
  `survey_versioned_renewal_v2`.
- New5 = discovery/X/3 renewal modules, lazy for legacy/current canonical
  routes. Old `_check_runtime_binding` demands all 35 loaded before body,
  so fresh Python without test preloading 35 fails all 26 with
  `RUNTIME_BINDING_MISSING: S2 module not loaded: scripts/survey_discovery_v2.py`
  (affected-regressions 26/26, durable `/tmp/opencode` fallback preserved).
- Longform functional worker manually preloaded 35 before P3S — NOT acceptable
  as normal caller requirement.
- Top-level side effects inspected: all 5 are top-safe (pure constants/functions,
  no State/history at import; discovery top pulls x_intake safely, x_intake top
  pulls no discovery, history/source/renewal top pull no scripts; no `sys.modules`
  manipulation, no reload, no State validation/history recursion at import).
  Renewal `survey_versioned_renewal_v2` function-local imports `staged` (lazy,
  no top cycle). No top cycle if imported function-local.

## 2. Fix (OWN product ONLY, no shared changes elsewhere)

File: `scripts/survey_editorial_staged_source_v2.py`
- `131847B ad60e082…` → `133866B 9e2a0ad6…` (+2019B, +26 lines, no new paths).
- `materialize_staged_source`: after Session/root init + dep file pins, before
  existing strict `_check_runtime_binding`, explicit function-local CURRENT
  imports of New5 (5 lines + 11-line comment). Preserves existing P2V lazy import
  at function start. No top cycle, no reload/rebind, no new State/history.
- `verify_staged_source`: same 5 CURRENT imports before binding (5 lines + 4-line
  comment). P2V stays UNimported by discipline (file-pin-only; checker skips P2V
  when not in `sys.modules`). No reload/rebind.
- APIs unchanged: same 2 PUBLIC entry points/signatures/RESULT codes, same
  `StagedSourceError` codes/phases/dispositions. No new public API.
- Format counts unchanged: `_SHARED_PY` 35, `_SHARED_SCHEMAS` 22, per-route
  `code_deps` 63 sorted-unique, union 66. No closure expansion, no pin removal,
  no missing/wrongroot ignoring. Wrongroot/stale keeps `sys.modules` entry and
  refuses via strict path+bytes (`RUNTIME_BINDING_PATH`/`TOOL_DRIFT`).
- Test file `tests/test_survey_editorial_staged_source_v2.py` UNCHANGED
  (no sourcecopy/runtimehelper edit needed: from complete 740 SOURCE, `ls-files`
  already sees renewal as tracked; EDQUOT avoided via env `P3S_DURABLE_OUTDIR`
  + `TMPDIR` workspace-local, not code change).

## 3. NEW isolated complete SOURCE db (SOURCE fixture commits ONLY)

- Provision script (Write-before-`bash -n`): `make_p3s_source_20261025T160000Z.sh`
  (`bash -n` OK, `DONE OK 20261025T160000Z`).
- `PACKROOT .rephase-1-editorial-runtime/versioned-renewal-p3s-runtime-20261025T160000Z/`
  `test-source` HEAD `9a2f55d9b91f6aea2cb22f8b4695a861eeffd8da`
  (parent `409b292`), message `TEST-ONLY: complete 740 SOURCE WITH P3S runtime
  correction before authority`. Status clean, `ls-files` 32206 total
  (32155+51), intended 740 all tracked missing 0. `.git` 83 files, no
  `objects/info`/`alternates`, inert `example.invalid`, `dev:ino` disjoint,
  `nlink==1`. SRC==DST 740/740 SHA. No reconstruct/candidate commits, no
  network/pip/old runners, no cleanup.
- Pins (WITH fix): H 288349B `6fe86e…`, P1 158652B `825dba…`, PUB 125977B
  `3f4039…`, S 127981B `20f63e…`, HIGH 202862B `9a0469…`, Reader 46395B
  `098a2c…`, staged `133866B 9e2a0ad…`, `.latexmkrc` 218B `18199fd…`.
- Candidate ordinary commit FORBIDDEN preserved: candidate-work HEAD still
  `409b292`, working tree dirty with fix uncommitted. Reconstruct HEAD still
  `f84fcf5`. No product root relaxation, no all-objects DB change, existing
  proof context preserved.

## 4. Dedicated PUBLIC tests (fresh Python, no preloading, workspace TMPDIR)

All on NEW SOURCE db, `TMPDIR` + `P3S_DURABLE_OUTDIR` workspace-local
(`…/p3s-runtime-20261025T160000Z/tmp`), fresh child per call, genuine PIDs,
no filtered PASS. No `/tmp/opencode` EDQUOT for own runs (durable via env).

- `p3s_fresh_public_20261025.py` → `p3s-fresh-public-exit.txt` 0:
  LAZY OK (5 NOT top-loaded after `import staged` alone),
  CLOSURE OK (LONGFORM 63, WEEKLY 63, UNION 66, SHARED 35+22),
  WEEKLY FRESH OK + LONGFORM FRESH OK (REAL initial old-canonical accepted
  fixtures under FULL 740 commit before authority, materialize+verify fresh
  without preloading, manifests 63, union 66). After-renewal context: no owned
  fixture available (other authors pending) — initial canonical only.
- `p3s_negatives_20261025.py` → `p3s-negatives-exit.txt` 0:
  WRONGROOT OK (foreign discovery from old `affected-regress-143000Z` preload
  refuses `RUNTIME_BINDING_PATH [PIN/REFUSED_PRE_WRITE]`, `cur_file` still
  foreign — NO auto-reload/rebind), repair fresh PASS;
  DIRTY OK (discovery tamper refuses `TOOL_DRIFT [PIN/INVALID]` no-write),
  repair restored verifies again. Targets New5 to prove expanded-35 strict.

## 5. Original 26 on NEW SOURCE (parent controls, not product claims)

- `run_p3s_26_20261025T160000Z.sh` full module, bound 1200s, guard PID:
  `p3s-26-exit.txt` 15 (TERM after 1200s, genuine timeout, NOT filtered PASS).
  Reached 18/26: 17 PASS (o10,o11,o11b-f,o12a-f,o13,o14,o2,o3) + 1 FAIL
  (o1 ONLY `63 != 50` outdated test expectation; binding/materialize+verify
  themselves SUCCEEDED fresh). 8 pending (o4,o5,o6a,o6b,o7,o8,o9,r1) due to bound.
  Pins before/after HEAD `9a2f55d` same, status clean.
- `run_p3s_remaining8_20261025T160000Z.sh` remaining 8, bound 1200s:
  `p3s-remaining8-exit.txt` 0, `Ran 8 tests … OK (369.762s)` — all 8 PASS.
- Combined 26: 25 PASS + 1 FAIL (o1 count only). o1 failure is TEST expectation
  bug (`assertEqual(len(code_deps),50)` vs correct renewal-map 63; comment says
  `37→50`, predates `63/66` selection). NOT edited (out of narrow
  sourcecopy/runtimehelper scope); preserved as parent control. Product 63/66
  correct per `Actual AST closure counts remain 63/66 exact`.
- P2V discipline preserved (verifier never loads P2V; writer loads P2V fresh
  twice). Current tool/live/schema closure unchanged (dep pins == manifest,
  route schemas load as schemas, style/recipe file-pin-only).

## 6. Remaining / next (source will freeze after all authors)

- o1 `50 vs 63` needs TEST owner update (50→63) OR root confirmation that 63 is
  selected (map says 63/66 exact). Product MUST stay 63/66; do NOT relax to 50
  or remove pins.
- After-renewal P3S context (C→U→U, renewal→editorial, etc.) pending other
  authors + freeze; initial canonical proven here.
- No whole-unit PASS, no CommitPoint. Human Commit Point preserved. Ordinary
  Commit/Push Human-owned.
