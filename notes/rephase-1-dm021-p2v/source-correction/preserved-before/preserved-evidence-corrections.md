# R1 correction record (implementation-in-progress, NOT a completed unit)

2026-10-15 JST. General corrections per `astra-code-draft-review-r1.md` (NOT READY).
Preserved pre-correction versions kept intact in this directory; original
`implementation-report.md` inaccurate claims stay visible there with corrections
below. No long run/proof executed. No P2R/schema/config/network/commit/subagents.

## 1. Preparation/report corrections (path-specific readonly)

- Both-100 claim corrected: path-specific `status --porcelain=v1 -uall` counts
  (sanitized Git, checked rc, saved exclusive `status-{active,apply,p2vnew}.raw.txt`):
  active `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/...` 100 rows
  (16 source 3M+13A +84 caches); apply-copy
  `/tmp/opencode/jgas-dm021p2r-verify-20261014T000007Z/...` 16 rows
  (source only; 84 caches removed during P2R proof preparation); new P2V
  `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/...` 102 rows
  (18 source 3M+15A +84 caches). All share HEAD `409b292…`/tree `8ce36998…`.
- Sample-inode claim corrected: pack-only sample insufficient. Finished
  read-only all-entry `.git` check in EXISTING new copy (no recopy):
  new 134 files / 96 dirs / 0 symlinks / 0 errors; active same counts;
  0 shared dev/ino across copies; 0 nlink>1 in new; no alternates file.
  Saved `allentry-isolation.raw.txt` (includes py_compile + status corrections).
- py_compile disclosure: `PYTHONDONTWRITEBYTECODE=1` does NOT prevent pyc
  writes; `PYTHONPYCACHEPREFIX` only redirects. Prefix
  `/tmp/opencode/p2v-cache-absent-20261014T224000Z` holds 3 pyc
  (P1 139762B, observer 34839B, test 18249B); candidate tree unchanged (102).
  One unprefixed check additionally wrote
  `scripts/__pycache__/survey_editorial_current_authority_v2.cpython-314.pyc`
  into the candidate tree (103 rows); only that own artifact was removed to
  restore pre-check 102 (84 original caches untouched, missing=[]). Prefix pyc
  files left in place without deletion. Draft compiles similarly redirected
  2 pyc to `/tmp/opencode/p2v-draft-check-20261015T010000Z` (disclosed, kept).
- PhaseA/current summaries are not durable raw capture; this directory holds
  the saved exclusive preparation raw (status raws + preservation manifest +
  all-entry raw). Collection output summarized in return (transient), not a
  raw packet.

## 2. Observer d52f154b → corrected version (fixes R1 §2)

- Sanitized BEFORE Collector + throughout: refuse inherited `GIT_*` route
  (`GIT_ENV_REFUSED`) at entry, then `retention._sanitized_git_env_ctx()`
  scope for all Git-aware P1/receipt/HEAD work (restores process state on exit).
- Session FIRST: `_Session(str(root))` before any caller-root resolve; live
  `_Collector` built on `session.root_resolved` (symlink root refused by Session).
- Early pins BEFORE validators: proposal/manifest/State/config/State-bound
  Profile (parsed from pinned State bytes)/both schemas/supplied scope all
  pinned in retained session before layout/pipeline/scope/verify; live re-pins
  stability-checked; shared-path ORIGINALs cross-compared (live vs retained).
- Final ORIGINAL boundary AFTER later reads: `orig_live_map`/`orig_ret_map`
  preserved at entry; after later snapshot/inventory/dep/HEAD reads, every
  consumed file compared to entry ORIGINAL (no laundering) + `reverify` again.
- Returned refs from bound rels (`prop_rel`/`man_rel`/`_st_rel`/scope `s_rel`
  recorded before close; no `resolve()` after close). Ordered row
  cross-binding (`zip(live_plan, rows)`, no sorting into agreement).
- Close handling: `except CurrentAuthorityError as primary` + `_close_all`
  secondary attach via `_attach_close` (primary preserved, no `owned`).
  Removed single-string compatibility constructor; structured
  `(code, phase, detail, cause)` only. Strict type checks on helper returns
  (P2R SHAs/checked ints, graph nodes/edges lists, plan list, ref shapes;
  no `int()`/silent coercion).

## 3. P1/test/runner/proof status

- P1 unchanged `cdd69fe7` 113535B (333-line factoring diff preserved);
  inherited15 ALL_MATCH; 0 schema/P2R/config changes. Public shape/absence/
  final checks preserved via fixed `_pipeline`/`_retention_plan` wrappers +
  shared comparator.
- Tests: placeholder file (13 placeholders, 0 observe calls) replaced by
  behavioral file (13 methods; 11 call `observe_current_authority`, 2 are
  signature/error-shape probes). Longform helper fixed with `workspace` arg;
  fixture tracked list includes `.github`; R1 via real owner + fixture-code
  cascade; every behavioral method asserts result/error AND immediate
  pre/post no-write (mutated-pre/post BEFORE repair); close test asserts
  observer `CLOSE_FAILED` mapping + fd-leak check (not mock behavior).
- Runner/proof v1 scaffolding (comment-only, `assert`, return-0) preserved
  here, superseded by executable `run_p2v_v2.py.DRAFT` /
  `proof_apply18_v2.py.DRAFT` in `notes/rephase-1-dm021-p2v/` (explicit
  `GuardFailed`/`ProofFailed`, exact 102/static18/inherited15/cache84 PRE+
  finally-POST, durable O_EXCL streams, child spawn + timeout + process-group,
  TMPDIR/absent-cache-prefix, no secrets; proof via independent byte-copy +
  declared overlay revert + disposable index, no archive/fake-root/borrowed-DB).
- Current source pins: P1 `cdd69fe7` 113535B; observer `79a3396c` 37896B;
  test `c7ba6d4a` 32749B; expected18 draft hash `c6bb1fad2ad9` (in packet).

## 4. Blocker

No real >budget/fixture blocker: corrected code fits 2A1M (P1 M +2A paths,
no new paths beyond selected 2); fixture recipes use actual accepted-chain
helpers + independent committed source; drafts executable pending root
readback. Long run/proof NOT started (awaiting root selection). This is
implementation-in-progress, NOT a completed-unit Human Commit Point.
