# P3S R3 correction report (fresh author, pre-execution)

2026-10-18. Implements all six root R3 readback items in the same independent
copy `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`). Only new3 changed; inherited18
18/18 and 84 caches verified read-only (0 mismatches, no baseline rewrite).
Prior R2 bytes preserved in `draft-history-r3/prior-bytes/`; R2 reports in
`draft-history-r2/` untouched. No imports, no test/fixture runs,
no network/commit/push; no `verification-tools/` or root-doc edits. Cheap
checks only (`PYTHONDONTWRITEBYTECODE=1`, stdlib + `jsonschema`, no
candidate-module imports).

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 | Lines |
|---|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 114460 | 0o664 | `be133819b00a9f7c635d67466d309563e735441fa17992ba6e8619b869c37dfd` | 1896 |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) | 157 |
| `tests/test_survey_editorial_staged_source_v2.py` | 112080 | 0o664 | `ebc8235524177956238e464006e22a5199ed84701b1f7cc2e415c3ba29030af8` | 2024 |

Module AST-OK (24 defs), test outer AST-OK (49 defs, 26 methods), schema
`Draft202012Validator.check_schema` OK. Every embedded child program AST-OK via
literal-eval + `ast.parse` (no fixture execution): `_P3S_MATERIALIZE_SCRIPT`
1120 chars, `_P3S_VERIFY_SCRIPT` 729 chars, `_P3S_FAULT_SCRIPT` 11997 chars.
No `...[truncated` markers; single `__main__` only. Status 105 rows
(3M + 18A + 84 pyc; non-pyc 21 = 3M+18A).

## R3-1 — durable helper (xb before Popen, pgid, timeouts, no cleanup)

Prior helpers launched with `PIPE` then `write_bytes` after `communicate`,
contradicting the direct durable/exclusive requirement. Replaced with a common
`_launch_durable_child` used by both `_run_fixture_code` and `_run_p3s_fixture`:

- Exclusive `xb` stdout/stderr opened BEFORE `Popen`; open fds passed directly
  to the child (`stdout=fb_out`, `stderr=fb_err`), never `PIPE`-then-write.
- Exclusive per-call durable dir under `_durable_base()`; exclusive pre-launch
  meta (`open(..., "x")`) with pid/pgid/running record written immediately
  after `Popen` (pid = pgid leader via `start_new_session=True`).
- Process-group timeout/interrupt kill (`SIGTERM` then `SIGKILL` via `os.killpg`)
  with bounded reap (`wait(10s)`); `KeyboardInterrupt` also kills the group.
  Finally block preserves any primary timeout/interrupt error and attaches
  secondary close/readback failures instead of masking it.
- Saves exact script bytes (`child.script.py`), sha256, actual argv/cwd/
  sanitized env/timeout/pid/pgid/elapsed for evidence; final meta written
  exclusively (`"x"`). Full stdout/stderr preserved as files and returned
  (not truncated, not success-discarded). No automatic cleanup; durable dirs
  persist for the packet/runner.
- `P3S_DURABLE_OUTDIR` must point to the runner's new `outdir/fixture-raw`
  when provided; fallback is explicitly `/tmp/opencode` (created if missing).
- Selected conservative operational bounds (not measured sufficiency, no margin
  proof): materialize/fault 1800s (default in `_run_p3s_fixture`), standalone
  verify 600s (explicit callers), R1 refresh 1800s (default in
  `_run_fixture_code`), FIFO no-read 60s (explicit). The 1800/600s values cover
  slow filesystems/runners; they do not prove any run will complete within the
  bound. Prior 240/180/120s justifications invoking older 425s averages are
  withdrawn.

Seams: test `_durable_base` ~220, `_launch_durable_child` ~239–390,
`_run_fixture_code` default 1800, `_run_p3s_fixture` default 1800, `_verify`
600, FIFO 60.

## R3-2 — ancestor identity vs original (no extra closure masks)

Prior `_write_owned_file` ancestor loop checked only type/alias, not original
identities. Corrected to compare every canonical ancestor to the ORIGINAL
pinned identities before EACH create:

- Root `"."` compared to `session.root_id` (dev, ino, mode).
- Each proposal-parent prefix compared to `session.dir_ids[rel]` when pinned
  at CLAIM-time `_open_dir_chain`; alias/type still refused when unpinned, but
  absence is never treated as equality. Pins are read, never mutated.
- Staged dir itself compared to earliest owned `dir_identity` (mkdir identity).
- Uses `lstat` only (no extra opens, no closure masks).

Final staged root entry must equal the owned ID: after reopen, `fstat(check_staged)`
and parent entry via `session._entry_identity(check_parent, STAGED_DIRNAME)`
are both compared to `owned["staged_identity"]`; mismatch refuses
`STAGED_ROOT_REPLACED` before any file-identity loop. Repo-root entry is also
rechecked at FINAL (`fstat(root_fd)` vs `lstat(root_resolved)`).

Seams: module `_write_owned_file` ancestor block ~1249–1295, FINAL root check
~1015–1025, FINAL staged-dir owned check ~1095–1115.

## R3-3 — canonical static21 artifact (no baselining)

Prior report claimed final21 static but saved no artifact. New artifact
`draft-history-r3/static21.json` (107 lines, 3670 B, sha256
`30ae3abcff42b0e26cba669aa0c5150d824efe47d6e65ef2bfdf2411ca927ef1`):
canonical flat JSON, outer keys sorted, inner order `sha256/bytes/mode`,
exact 21 entries (inherited18 + new3).

- Inherited18 rehashed read-only vs
  `notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json`:
  18/18 match (sha256+bytes+mode `0o664`), 0 mismatches.
- All84 rehashed read-only vs
  `notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/cache-inventory-static.json`:
  84/84 match, 0 mismatches.
- Never baselined changed inherited/cache values; mismatches would have been
  exact blockers (none occurred). The artifact records actual corrected new3
  hashes (`be133819…`, `ebc82355…`) plus unchanged inherited pins.

## R3-4 — FIRST observed_head equality before writes

Later FINAL compared both observations to the pin, but no explicit FIRST
equality existed before CLAIM. Added immediately after the first P2V
`RESULT_SCOPE_BOUND` check, before any stable-ref compare:

- `observed["observed_head"]` must be a 40-hex string equal to `head_pinned`;
  otherwise `HEAD_MOVED` at phase `OBSERVE` before writes. This is the first
  write-gating HEAD equality; later FINAL still checks both observations plus
  live/collector HEADs.

Seam: module ~660–668.

## R3-5 — disposition semantics (per-file vs SET, no contradiction)

Prior docstring said fsync/close failure “reports INDETERMINATE because complete
bytes may already exist” without distinguishing SET incompleteness. Corrected
`_write_owned_file` docstring (selected semantics, no contradiction with this
report):

- Write failure: caller phase/disposition (`CLAIM/OWNED_PARTIAL` for sources):
  file bytes definitely incomplete, staged SET incomplete.
- Fsync/close failure: `INDETERMINATE_INVOCATION` even for the first file — the
  per-file bytes/close state are uncertain (complete valid file bytes may
  exist) while the staged SET is separately incomplete (manifest/other files
  missing, proven by FINAL inventory, not by the disposition string). Per-file
  uncertainty and SET completeness are distinct fields (`owned["owned_files"]`
  vs FINAL inventory); the disposition string never claims SET completeness.
- Primary preservation unchanged (write/fsync primary survives secondary
  close). No crash-atomicity/power-loss/replica claim.

## R3-6 — fault-test phase/disposition asserted, AST all embedded

All fault-script outcomes now assert `phase`/`disposition` (not merely return
them); direct tamper/verify outcomes assert presence or exact values where
deterministic:

- O12b: `CLAIM/OWNED_PARTIAL` exact per-fault deltas + `bytes_written==0`.
- O12c: `CLAIM/INDETERMINATE` exact root+main.tex + live-unchanged.
- O12d: `MANIFEST/INDETERMINATE` exact root+3+manifest / root+4 + live-unchanged.
- O12e: `CLAIM/OWNED_PARTIAL` exact root+empty-file.
- O11b drift-reader: `PRE_WRITE/REFUSED_PRE_WRITE` + exact reader-rel delta.
- O11c late-control/retained: `PRE_CLAIM/REFUSED_PRE_WRITE`.
- O11d drift-before-claim `PRE_CLAIM/REFUSED_PRE_WRITE`, drift-before-manifest
  `MANIFEST/INDETERMINATE_INVOCATION`.
- O11e post-readback `REPLAY/INDETERMINATE`, post-replay-samebyte
  `FINAL/INDETERMINATE` `FILE_REPLACED`.
- O11f root/ancestor: `CLAIM/OWNED_PARTIAL`.
- O12f short-once (positive, fired==1), partial-then-fail
  `CLAIM/OWNED_PARTIAL` `bytes_written==1` fired==2, write-then-close
  `CLAIM/OWNED_PARTIAL` primary preserved + secondary attached fired==2.
- O6a/O13 verifier `TOOL_DRIFT`: `PIN/INVALID`; O6b KEEP: `OBSERVE/REFUSED_PRE_WRITE`;
  O7 stale: `OBSERVE/REFUSED_PRE_WRITE`, others presence-asserted; O8/O9/O10/O11/O14
  presence-asserted (exact where deterministic).

ALL embedded scripts cheap-checked via literal-eval + `ast.parse` (no fixture
execution, no candidate imports): outer + 3 child programs OK (see §pins).
`_P3S_R1_NONEMITTED_COMMENT_ANCHOR` is a string constant, not a child program,
and is excluded from the AST check.

## Guarded execution prerequisites (for root selection)

- Fixed HEAD/tree: `409b292756dd1277b9dfae87679934c0d2ce251c` /
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`; `GIT_NO_LAZY_FETCH=1`,
  `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; sanitized `GIT_*`
  inheritance refusal; `PYTHONDONTWRITEBYTECODE=1`; no `PYTHONPATH` inheritance.
- Static21 artifact above (21 exact pins); inherited18 and 84 caches verified
  read-only (no rerun of old suites, no cache cleanup).
- Durable evidence contract: set `P3S_DURABLE_OUTDIR=<runner-outdir>/fixture-raw`
  before any run; otherwise fallback `/tmp/opencode` is used. Each call creates
  an exclusive durable dir with `xb` stdout/stderr, pre-meta (pid/running),
  script bytes+sha, final meta (rc/timeout/interrupt/elapsed/close-secondaries).
  No notes-nested DBs; temp GEN/PROOF DBs/indexes (when authorized) stay under
  fresh `/tmp/opencode` locations, never in notes. No absent-NEW reads; no
  archive/fake-root/active `add -N`.
- Run only after root selects smoke/affected/full; no old13+1/25/36 transfer.
  Timeouts are operational bounds only (1800/600/1800/60); a timeout is an
  explicit failure with durable raw, never a hang or truncated-only stdout.

## Unresolved limits (no execution PASS claimed)

- No execution in this unit: all 26 methods unaudited at runtime; every
  seam/code/binding string remains a pre-execution claim for root-selected
  runs. This report confers no execution PASS, no adoption/production
  authority, and no tooling acceptance.
- Fire-count/binding claims (leaf-targeted `active` map, exact-rel drift,
  manifest-leaf targeting, `TOOL_DRIFT`-vs-KEEP preemption, short/partial/
  combined byte progress) require runtime proof that each fault fires at the
  intended seam.
- Ancestor-replace *during* a write is covered by pre-write alias + held-fd +
  canonical + FINAL rechecks, not mid-syscall swap injection (honestly
  disclosed; no post-final-injection guarantee).
- Weekly has no `canonical_reader_bytes` equivalent; Weekly replay binds FILE
  bytes to the canonical digest (same as P2V) — disclosed limitation.
- `_check_runtime_binding` remains a tripwire, not hotpatch proof; `OWNED_PARTIAL`
  maps to INCOMPLETE-class (contract string `INCOMPLETE`), tested via codes;
  `sha256_object` vs pretty-bytes distinction retained per Q8.
- No crash-atomicity/power-loss/replica/global-CAS/no-drift claims; no
  candidate/reconstruct commit/push.

No scope exceedance (still 3A/0M, existing18 untouched). No concrete missing
requirement is hidden; the above limits are the only standing qualifications.
