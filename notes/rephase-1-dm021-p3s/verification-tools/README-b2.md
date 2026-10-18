# P3S verification-tools B2 — DRAFT docs (NOT EXECUTED, root readback)

2026-10-18. CoWorkerB tooling author B2, in parallel with CoWorkerA code.
B1 files/reports preserved byte-for-byte; this unit writes ONLY NEW b2
filenames + this README-b2.md. No candidate/source/test/schema edits, no
tests/sourcecopy/fixture/GEN/PROOF execution, no network/commit/push.
No PASS claims; root re-readback required before any execution. Root source
author concurrently corrects new3 — static21 was NOT read here (no
half-written static21 treated as finalized).

## 1. New files (ONLY these, all DRAFT)

- `notes/rephase-1-dm021-p3s/verification-tools/run_p3s_b2.py` (672 lines)
- `notes/rephase-1-dm021-p3s/verification-tools/gen_complete21_b2.py` (737 lines)
- `notes/rephase-1-dm021-p3s/verification-tools/proof_apply21_b2.py` (882 lines)
- `notes/rephase-1-dm021-p3s/verification-tools/README-b2.md` (this file)

Preserved (untouched): `run_p3s_b1.py`, `gen_complete21_b1.py`,
`proof_apply21_b1.py`, `README.md`,
`independent-tooling-preexecution-review.md` (B1–B8).

Fixed identities (all three B2): FIXED_HEAD
`409b292756dd1277b9dfae87679934c0d2ce251c`, FIXED_TREE
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`, canonical21 = MODIFIED3 (3,
`" M "`) + NEW18 (18, `"?? "`; includes NEW_P3S3:
`scripts/survey_editorial_staged_source_v2.py`,
`schemas/editorial-staged-source-manifest-v2.schema.json`,
`tests/test_survey_editorial_staged_source_v2.py`) + 84 caches = 105 rows.
Inherited18 must equal P2V `expected18-source-correction-v5.json`
(supplied at execution); caches from P2R static inventory (84 ×
`{sha256,bytes,mode}`). Static21 + candidate are REQUIRED CLI at execution
after CoWorkerA return.

## 2. B1–B8 repairs (code-reviewed, ast.parse only)

AST: `run_p3s_b2.py` 6198 nodes / 10 funcs; `gen_complete21_b2.py` 6594
nodes / 11 funcs; `proof_apply21_b2.py` 7513 nodes / 14 funcs — all
`ast.parse` OK (`PYTHONDONTWRITEBYTECODE=1`,
`PYTHONPYCACHEPREFIX=/tmp/opencode/p3s-b2-nocache-absent`, absent verified).
No imports, no runner/generator/proof execution, no `py_compile`.

- **B6 raw-once (all three):** `_pin_file_bytes` + `_load_json_once`
  (runner ≈L150–165; gen ≈L145–160; proof ≈L138–153). Static inputs pinned
  to bytes once; `sha256(raw)` + `json.loads(raw.decode())` share the same
  buffer; `input_ids` reuse those hashes — never a second `read_bytes()`.
  Patch (proof) pinned as bytes once, hashed once, compared to pinned hash
  text once.
- **B7 pin immutability (all three):** every pin file passes
  `os.lstat` refusal (symlink/FIFO/socket/non-regular/`nlink!=1`) in
  `_require_regular`/`_pin_file_bytes` BEFORE first read; existence gates
  use `os.lexists` + `is_file` (broken-symlink safe). Cache wrapper key
  `"files"` explicitly required — `{"files": …}` missing/ non-dict fails
  40 (no silent `.get("files", {})`). Runner gates ≈L348–370; gen
  ≈L330–360; proof ≈L312–344.
- **B1 concrete cache enforcement (gen):** `_check_source` ≈L244–298 now
  compares all 84 cache entries per-file (`sha256`/`bytes`/`mode`, alias
  errors fail) with entry-shape validation, and source-post re-compares
  cache bytes (≈L545–560), not only 21 files.
- **B2 binary patch capture (gen):** new `_run_git_bytes` ≈L114–126
  (`capture_output` bytes, no text decode; stderr decoded replace-only);
  `diff --cached --binary` bytes written directly to `xb` patch file
  (≈L470–500). Text `_run_git` retained for `read-tree`/`add`.
- **B3 absolute saved-patch (proof):** `patch_abs`/`patch_hash_abs` =
  `Path(args…).resolve()` immediately after parse (≈L310–320); `git
  apply --check`/`apply` receive `str(patch_abs)` (≈L620–635), never a
  `cwd=copyrepo`-relative path. Pinned `patch_raw` (original path) supplies
  the sha; absolute path supplies the filesystem location.
- **B4 full cache removal, disposable only (proof):** inventory
  `__pycache__/*` + top-level `*.pyc` (≈L560–575); each inventoried file
  `lstat`-checked (symlink/special/`nlink!=1` refuse) and `unlink`ed
  individually; `__pycache__` dirs `rmtree`d only after file removal;
  every target prefix-checked under `copyrepo` (escape refuses);
  survivors enumerated and fail (≈L575–610). Removal never touches source.
- **B5 interrupt path (proof):** `except KeyboardInterrupt` records
  primary `interrupted` + `interrupted=True` (≈L690–697), still runs checked
  source-POST, single `_emit(130)` at end (≈L745–760); handles always
  closed via `_emit`; no print-and-return before POST.
- **B8 accurate meta/commands (gen):** durable `meta` holds inputs/forced
  env only; raw git sequence + `stdout_bytes` + `patch_sha256`/`patch_bytes`
  + absolute index live in `stage-done.json` (≈L565–590); docstring + this
  README state that split accurately (code and doc agree).
- **QUALs (runner):** `_observe` reuses `_require_regular` lstat
  mode/size (≈L167–202, no second `f.stat()` for mode); `pip freeze` runs
  with sanitized `git_env` (≈L445–455); `cache_prefix`/`tmpdir`/`outdir`
  gates use `os.lexists` (≈L348–357, post ≈L545–555); `outdir.mkdir
  (parents=False)` (≈L395–402, same in gen/proof).
- **POST-on-failure (gen + proof):** work section records `primary_error`
  (never `return` after handles reserved); checked source-POST always
  attempted when `pre`/`active` exists — gen `_observe_source` +
  `_check_source` (21 + 84) + pre/post equality + per-file/cache sha +
  input re-hash (≈L525–580); proof `_freeze_full(source)` vs `active` +
  input re-hash incl. patch/hash (≈L700–745). `primary_error` +
  `secondary_errors` both preserved in logs + `stage-done.json` /
  `terminal-note.json`; wrapper codes: interrupt 130 > primary 40/1 >
  secondary-only 3 > flush/exit/stage 5/6. Refusals before outdir
  reservation (bad args, missing pins, scratch violations) still return
  40 console-only — no durable location exists for POST (documented limit).
  No `return` inside any `finally`; single return after `finally`/`_emit`.
- **Silent-manifest guard (all three):** POST re-pins every static input
  and compares sha to the pre-guard pin; drift reports
  `static input changed post guard (…)` as secondary error (runner
  ≈L583–597; gen ≈L560–575; proof ≈L730–745).

## 3. Line-based guard map (B2)

### run_p3s_b2.py (672 lines)

- L56–62 fixed HEAD/tree/timeout; L64–94 canonical sets (MODIFIED3/NEW15/
  NEW_P3S3/NEW18/CANONICAL21); L105–119 env (`_git_env` strips `GIT_*`;
  `_child_env` strips `GIT_*`+`PYTHONPATH`/`PYTHONHOME`, forces 6 keys).
- L121–130 `_run_git` (text, 60 s, GuardFailed on timeout); L132–148
  `_require_regular` → `(mode,size)`; L150–165 pin-once helpers.
- L167–202 `_observe`: 5 git cmds rc==0, lstat-regular candidate files +
  caches, `read_bytes` sha, mode from lstat (QUAL fix).
- L224–281 `_check_pins`: HEAD/tree/index-empty/keyset/shape/live-match/
  inherited18-manifest+live/NEW_P3S3/cache-len+per-file/105-len+dup+rowset.
- L305–334 `_kill_reap` (own pgid TERM→KILL + reap, orphan limit noted).
- L337–402 `main` args + `os.lexists` gates + raw-once load + wrapper
  validation + `parents=False` outdir.
- L403–460 reserved/meta (input_ids from raw sha/size, pip with `git_env`).
- L461–500 pre observe + `_check_pins`; child `python -u -m unittest`
  (`start_new_session`, held `xb`, sanitized env, 18000 s) or pre-errors.
- L501–530 excepts (interrupt/guard/runtime/fatal, reap, no return).
- L531–613 `finally`: checked POST (observe + `_check_pins` + pre/post
  diff + `lexists(cache_prefix)` + input re-hash), wrapper ladder
  (130/124/launch/2/child/0→3), trailer/flush/`x`-exit/`x`-stage-done
  (5/6 forcing), single return L614.

### gen_complete21_b2.py (737 lines)

- L52–88 identities; L96–126 git helpers (`_run_git` text,
  `_run_git_bytes` binary); L128–160 pin helpers.
- L162–207 all-entry `.git` walk; L209–242 `_observe_source` (21 + 84);
  L244–298 `_check_source` (B1 cache per-file + entry-shape parity).
- L300–395 `main` validation (scratch under `/tmp/opencode`, `lexists`
  gates, raw-once + wrapper check, absolute disp/index, `parents=False`).
- L396–430 reserved/meta (inputs only — B8 accurate).
- L431–520 work with `primary_error` (pre → copy → completeness →
  isolation → inert remote/config → `read-tree`/`add`/binary `diff` →
  `xb` patch + `x` hash); no early return.
- L521–580 checked POST-on-failure (post observe/write + `_check_source`
  + pre/post equality + 21-file + cache sha + input re-hash;
  `primary`/`secondary` preserved).
- L581–640 `finally` (no return inside): trailer/flush/`x`-exit/
  `x`-stage-done incl. `raw_git_sequence` + patch sha (B8), single return.

### proof_apply21_b2.py (882 lines)

- L54–86 identities; L95–120 git env/run; L121–153 pin helpers;
  L155–200 all-entry walk; L202–229 remote/config (inert + no alternates);
  L230–241 `git show` bytes; L242–271 freezes (`_freeze_full` 21-file;
  `_freeze_clean` absence-only, no NEW reads).
- L293–344 args (scratch under `/tmp/opencode`, absolute `patch_abs`,
  `lexists` gates, raw-once pins incl. patch/hash, wrapper check,
  64-hex + sha match before outdir).
- L345–408 outdir `parents=False` + handle reservation + `_emit`
  (flush/close→5, `PROOF_LIMIT` note, no generic certification).
- L409–690 work with `primary_error` (meta → keyset/NEW_P3S3 → active
  freeze → HEAD/tree/index → 21-file → inherited18 → 105 rowset → 84
  caches → remote → byte-copy → completeness → isolation → copy remote →
  B4 cache removal (disposable only) → checkout 3M → unlink NEW18 →
  clean freeze + `x` clean json → absolute `--check`/`apply` → applied
  freeze + `x` applied json → byte/mode vs source → EXACT21 + len 21).
- L690–745 interrupt/exception capture + checked source-POST
  (`_freeze_full(source)` vs `active` + 5-input re-hash); `primary` +
  `secondary` preserved; terminal-note `x`-persisted; single
  `return _emit(130/40/3/0)`.

## 4. Self code-review (revisions only, no execution)

- Reviewed each B2 diff-region against its B1 parent by re-reading the new
  files in full (Read, no imports, no subprocess). No candidate modules
  imported; no `cp`/DB/index operations performed; `ast.parse` was the
  only code operation (read + parse, `PYTHONDONTWRITEBYTECODE=1`, absent
  prefix verified absent afterwards).
- Verified: no `return` inside any `finally` (runner L531–613, gen
  L581–640 use wrapper variable + post-`finally` return; proof uses
  single `_emit` return after post). Verified `os.lexists` on all
  existence gates; `parents=False` on all `mkdir`s; absolute
  `GIT_INDEX_FILE`/`patch_abs`/`disp`/`copyrepo` with `/tmp/opencode`
  prefix enforcement; `removed`/`caches_before`/`applied`/`removed`
  scoping guarded by `primary_error is None` chains.
- Known residual risk (not a blocker, carried as limits §5): `Path.resolve()`
  on the cache-removal prefix check follows symlinks before `lstat` — a
  symlink is still refused by the subsequent `lstat`, but the check order
  is belt-and-suspenders rather than a single atomic operation (local
  single-user scope; no concurrent writer assumed beyond the documented
  root new3 correction, which these tools never read).

## 5. Unresolved limits (no execution, no PASS)

- Not executed: no smoke/full/API/oracle verdicts; no timing/byte claims
  beyond static review. Root re-readback + explicit run authorization
  still required; smoke vs full require different exclusive outdirs at
  execution.
- Pre-outdir refusals (bad args, missing/non-regular pins, scratch-root
  violations, unresolvable paths) return 40 console-only without POST —
  no durable location exists yet; all post-reservation failures do POST.
- TOCTOU: pin-then-read is not atomic against a concurrent writer; tools
  detect post-guard drift via re-hash but assume no adversary during the
  run (local single-user scope). Static21 concurrently corrected by root
  was deliberately never read here.
- `_freeze_full` (proof) records mode via `p.stat()` after `_require_regular`
  lstat (parity with B1); runner `_observe` was fixed to lstat mode, proof
  freeze retains the two-call pattern — noted, not a run blocker in local
  scope.
- `pip freeze` output truncated to 6000 chars; full env never persisted
  (redaction count only). Orphan limit: pgid kill cannot claim
  double-forked escapees. `parents=False` fails if the evidence parent
  does not exist (operator creates it). `scratch-root` must pre-exist
  under `/tmp/opencode`. Tools are one-off exact-run evidence, not
  universal rerunners and not candidate/Production authority.
