# P3S verification-tools B1 — independent pre-execution review (read-only, no run)

2026-10-18. Scope: `run_p3s_b1.py` (619 lines), `gen_complete21_b1.py` (519 lines), `proof_apply21_b1.py` (611 lines) + `verification-tools/README.md` + `astra-implementation-selection.md` + AGENTS.md role/boundaries. Method: full static read only. No tests, no imports, no fixture/proof executions, no candidate/DB/index writes, no network, no `__pycache__` claims. This is a tooling review, not source authorship and not a run authorization. No generic certification; blockers below must be repaired and re-read before any execution.

Role: reviewer only per AGENTS.md (Astra/root reviews; Co-Worker implements/runs). Did not delegate. Did not create or modify any other file.

## Claims checked

README §2–§3 + selection §24–§26 require: exact fixed HEAD/tree/index/Git-rc PRE + finally-POST, full-105 rowset+len+dup check, static21 `{sha256,bytes,mode}` per-file live match, inherited18 vs P2V-v5 equality, 84-cache per-file match, immutable input pinning, direct held exclusive `xb`/`x` outputs, actual argv/cwd/python/PID/timing + allowlisted env, cache-prefix absent + no cleanup, TERM→KILL on own pgid + reap with orphan limit, no `return` in `finally`, scratch under `/tmp/opencode` resolved absolute with escape refusal, no notes-nested DBs, all-entry `.git` lstat + inode-set disjointness, no absent-NEW reads, saved-patch-only proof, inert remote/config on both DBs.

## Per-tool verdicts

### 1. `run_p3s_b1.py` — largely conformant, 2 pinning gaps + 2 qualifications

- PASS: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` (L56–57); 5 git cmds with rc==0 enforcement (L149–160); canonical21/MODIFIED3/NEW18/NEW_P3S3 sets (L64–92); full `_check_pins` covers HEAD/tree/index-empty/manifest-keyset/static21-shape/live-match/inherited18-manifest+live/cache-len+per-file/105-len+dup+rowset (L203–281); child `python -u -m unittest`, `cwd=candidate`, held `xb` handles, `start_new_session=True`, sanitized `_child_env` stripping `GIT_*`+`PYTHONPATH`/`PYTHONHOME` and forcing 6 keys (L108–114, L452–456); TERM→KILL+reap on own pgid with double-fork limit noted (L284–313, L464); finally-POST observe+`_check_pins`+pre/post rowset diff+`cache_prefix.exists()` (L503–532); wrapper_rc ladder (130/124/launch/2/child/0→3 on post-errors) + trailer/flush/exit/stage `5`/`6` forcing with no `return` in `finally`, single return L614–615 (L533–613).
- GAP (pinning, blocker B6/B7 below): inputs accepted via `is_file()` only (L335–343); manifest/cache/p2v loaded L363–365 then re-read for `input_ids` hashing L420–423 — two reads, TOCTOU; no `lstat` alias/`nlink` refusal on the pin files themselves.
- QUAL: mode recorded via second `f.stat()` (L181, L196) after `_require_regular` `lstat` — claim says `lstat`; reuse `lstat` result or `O_NOFOLLOW`+`fstat`. Not a run blocker in single-user local scope but diverges from claim.
- QUAL: `pip freeze` (L430–431) inherits unsanitized parent env (no `GIT_*` strip); pass `git_env`. `cache_prefix.exists()` (L529) misses broken-symlink creation; use `os.lexists`/`lstat`.

### 2. `gen_complete21_b1.py` — 3 blockers

- PASS: scratch-root must pre-exist under `/tmp/opencode` (L270–275); `disp`/`disp_index` resolved absolute + escape refused (L296–303); disposable-index-only `read-tree→add→diff --cached --binary` with `GIT_INDEX_FILE` absolute (L411–427); all-entry walk + inode-disjointness (L372–386); inert remote/config + no-alternates on source AND copy (L387–409); exclusive `xb`/`x` outputs, no commits/network/cleanup, source-post rowset+sha check (L442–450), no `return` in `finally` (L461–515).
- See B1/B2/B8.

### 3. `proof_apply21_b1.py` — 3 blockers

- PASS: saved-patch-only (hash 64-hex L438–439 + `sha256(patch)` match L441–446, never generates); `copyrepo` resolved under `/tmp/opencode` (L341–344); active freeze HEAD/tree/index + per-file static21 + inherited18-manifest + 105-rowset/len + 84-cache per-file (L448–487); all-entry + inode-disjoint + remote inert on both DBs (L503–517); `checkout HEAD -- 3M` + `unlink` NEW18 with absence-only (no NEW-byte reads, comment L259) + `HEAD`-bytes match (L523–271); `--check` then `apply` (L558–563); applied freeze + byte+mode source-vs-copy + EXACT21 rowset/len21 + source-post sha (L564–599); `_emit` flush/close→5 with `PROOF_LIMIT` note if exit already recorded (L366–407).
- See B3/B4/B5.

### Cross-cutting checks

- Default paths/env: `DEFAULT_CACHE_STATIC` / `DEFAULT_P2V_EXPECTED18` absolute workspace paths in all three (runner L58–59; gen L52–53; proof L54–55). Manifest/candidate/source/outdir/scratch-root correctly REQUIRED (no masking defaults). `cache_static` assumes `{"files": …}` wrapper while `p2v_expected18` assumes flat dict (runner L363–365; gen L286–288; proof L331–333) — silent `{}` fallback on wrapper mismatch would surface only as len error; validate wrapper explicitly (part of B7 repair).
- No notes nested DBs: PASS — durable outdir separate from disposable `copy/index` under `/tmp/opencode` in gen/proof; runner `tmpdir`/`cache_prefix` forced under `/tmp/opencode` (runner L347–354).
- All-entry isolation: PASS for gen/proof; runner does not claim it (correct — runner creates no DB).
- No absent-NEW reads: PASS — proof `_freeze_clean` uses `exists()`/`is_symlink()` only (L247–259); gen/runner read only expected-present 21 after pre-guard.
- Saved patch use: PASS — proof never runs `diff`; gen never touches active index/objects.
- Remote effective config: PASS (bounded) for gen/proof; runner N/A by design.

## Concrete blockers (repair required, re-read before any run)

**B1 — gen omits 84-cache content check.** `gen_complete21_b1.py` L212–247 `_check_source` observes `cache_detail` (L197–203) but never compares it to `cache_static`; only `len==84` (L236) + status rowset (L238). README §3 claims “same 21+84 source guards.” Runner L259–266 does per-file compare; gen must add identical loop (`sha256`/`bytes`/`mode` vs live, alias errors fail). Also add source-post cache compare (currently only 21-file sha L447–449).

**B2 — gen binary-unsafe patch capture.** `gen_complete21_b1.py` L102–110 `_run_git(..., text=True)` + L430 `r3.stdout.encode("utf-8")`. `git diff --cached --binary` must be captured as bytes (`text=False`) and written directly; current path mangles any non-UTF-8 byte and re-encodes rather than preserving exact diff bytes. Repair: separate binary run for `diff` (bytes, no decode) or set `text=False` throughout raw sequence; keep `stderr` text-only.

**B3 — proof relative `--patch` resolves against copyrepo.** `proof_apply21_b1.py` L558/L561 `_git(copyrepo, env, "apply", …, str(patch))` with `cwd=copyrepo` (L100–108). A relative `--patch` is then resolved inside the clean copy, not the invocation cwd — wrong file or spurious failure. Repair: `patch = Path(args.patch).resolve()` (and `patch_hash_p`) immediately after arg parse, refuse escape if desired, pass absolute to `git apply`.

**B4 — proof inventories `*.pyc` but removes only `__pycache__` dirs.** Inventory L518–522 globs `__pycache__/*` + `*.pyc`; removal L533–539 `rmtree`s only the three `__pycache__` dirs. Top-level `*.pyc` (if any) would survive yet be recorded as “removed,” or cause clean-status failure. Repair: also unlink inventoried `*.pyc` (with `lstat` alias check) or narrow inventory/claim to dirs only and assert no `*.pyc` remain.

**B5 — proof missing `KeyboardInterrupt` path.** Runner L476 / gen L455 handle interrupt (130) with reap/cleanup; proof L602 catches only `(ProofFailed, RuntimeError, OSError)`. Interrupt before `_emit` leaves `stdout/stderr/exit` handles open with no exit record. Repair: add `except KeyboardInterrupt as exc: _log(...); return _emit(130)` mirroring gen, ensuring handles always closed via `_emit`.

**B6 — double-read static inputs (all three).** Runner L363 vs L420–423; gen L286 vs L340–342; proof L331 vs L421–423: JSON loaded once, then files re-read to hash `input_ids`. Bytes checked by guards may differ from bytes hashed. Repair: read raw bytes once into variables, `hashlib.sha256(raw).hexdigest()` + `json.loads(raw)`, reuse for both guards and `input_ids`.

**B7 — pin files lack alias immutability.** All `is_file()`/`exists()` gates (runner L335–343; gen L279; proof L318–329) follow symlinks; `_require_regular` is applied only to candidate files, never to `--manifest`/`--cache-inventory`/`--p2v-expected18`/`--patch`/`--patch-hash`. Repair: `lstat`-refuse symlink/FIFO/socket + `nlink==1` on each input pin before first read (reuse `_require_regular`), and explicitly require `cache_static` wrapper key `"files"` (fail 40 if absent rather than `.get("files", {})`).

**B8 — gen `meta.json` missing raw sequence.** `gen_complete21_b1.py` L348–349 writes `meta_p` before `raw_git_sequence`/`patch_sha` exist (populated L428–440 only in memory → `stage-done.json`). README §3 “raw cmds/rc/stderr persisted in `meta.json`” is false as written. Repair: defer `meta_p` write until after L440, or append/update via exclusive second file; alternatively correct README to state raw sequence lives in `stage-done.json` — code and doc must agree before run.

## Minors (not execution blockers, fix opportunistically)

- Proof L1+L7 duplicate `shebang`; L610 redundant `import sys as _sys` (already L44). Remove one.
- Proof L482 `import hashlib as _hl` inside loop; hoist (hashlib already imported L37).
- Gen L225–229 lacks manifest-entry keyset check that runner L227–229 has (`set=={"sha256","bytes","mode"}`); add for parity.
- Proof records `pid`/argv (L313, L413) but no `started_utc`/`ended_utc`/`elapsed_s` unlike runner/gen; add for timing parity.
- All `outdir.mkdir(parents=True)` (runner L388; gen L322; proof L352) auto-creates parents; consider `parents=False` to avoid unintended notes-tree creation.
- `disp.exists()` / `copyrepo.exists()` miss broken symlinks; prefer `os.lexists`.

## Finding

Tools are well-structured drafts with correct fixed identities (HEAD/tree), exclusive outputs, sanitized git env, and proper no-cleanup/no-commit discipline — but **NOT READY to execute**: B1–B8 violate the selection’s exact-105/static21/cache84, immutable-pinning, binary-exactness, patch-path, and fault-semantics predicates. Repair minimally as above, re-read diffs only, then return for a second pre-execution readback. No run, smoke/full selection, or affected-suite decision is authorized by this review.
