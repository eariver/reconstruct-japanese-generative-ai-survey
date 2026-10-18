# P3S R2 correction report (fresh author, pre-execution)

2026-10-18. Implements ALL ten Astra R2 blockers
(`astra-code-draft-review-r2.md`) plus outstanding R1 shape gaps, in the same
independent copy `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
(detached `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`). Only new3 changed; inherited18
18/18 byte-identical vs `expected18-source-correction-v5.json`; 84 caches frozen
(105 status rows = 3M + 18A + 84 pyc before and after). No imports, no
test/fixture runs, no network/commit/push; no `verification-tools/` or root-doc
edits. Prior R1 bytes preserved in `draft-history-r2/prior-bytes/` with pins
(`README.md`). Cheap checks only (`PYTHONDONTWRITEBYTECODE=1`, stdlib +
`jsonschema` only, no candidate-module imports).

## Corrected new3 identity (measured, read-only sha256sum/stat)

| File | Bytes | Mode | SHA256 | Lines |
|---|---|---|---|---|
| `scripts/survey_editorial_staged_source_v2.py` | 110461 | 0o664 | `821c57ba910d1ea8e8e8df44783f298b5a6bd0a318bdfa0c50519076ae1d7849` | 1836 |
| `schemas/editorial-staged-source-manifest-v2.schema.json` | 5627 | 0o664 | `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (unchanged) | 157 |
| `tests/test_survey_editorial_staged_source_v2.py` | 104179 | 0o664 | `fa172fd3a97a7059960f970886f3ac918a0423a1bb67155e71e475392bfaeb90` | 1908 |

Module AST-OK (24 defs), test outer AST-OK (49 defs, 26 test methods), schema
`Draft202012Validator.check_schema` OK. Every embedded child program AST-OK via
literal-eval + `ast.parse` (no fixture execution): `_P3S_MATERIALIZE_SCRIPT`
1120 chars, `_P3S_VERIFY_SCRIPT` 729 chars, `_P3S_FAULT_SCRIPT` 11997 chars.
No `...[truncated` markers; single `__main__` only. Static21 = inherited18 +
new3 (3M+18A tracked overlay unchanged); 105 rows = 3M + 18A + 84 pyc.

## Explicit correction of former overclaims

Author `draft-history-r1/correction-report.md` + independent
`independent-preexecution-resolution-r1.md` claimed B1–B4 and root R1–R5
“resolved in shape.” Root R2 proves those conclusions do not authorize
execution. This correction explicitly retracts and repairs:

- **Guaranteed positive rejection (R2-1):** prior FINAL compared the full
  edition `_tree_map` to pre-claim `init_tree` without the owned 4-file delta,
  guaranteeing rejection of every correct materialization; `_capture`/`_materialize`
  passed FILE-only allowed sets to DIR+FILE `_snapshot`. Corrected to
  original+owned-4-file expected-tree compare with diff diagnostics, plus
  explicit allowed ancestor/owned-dir sets derived from code (not observed
  output).
- **Embedded fault syntax (R2-2):** prior outer `"""` embedded `b"\n...\n"`
  as literal newlines (child SyntaxError) plus 4-space `outcome` indent and
  duplicate `__main__`. Outer-file AST-OK never validated embedded programs.
  Corrected to `r"""` outers, column-0 outcome, single `__main__`; every
  literal child program now `ast.parse`d via literal-eval (cheap, no fixture).
- **Structured/fired oracle (R2-3):** prior fault script returned only error
  text + owned count, dropped phase/disposition/attempt/byte-progress/secondary,
  tracked fds by number (reusable) with `created[3]` manifest index, and module
  `bytes_written` updated only after ALL writes (partial falsely 0). Corrected
  to leaf+generation active map with removal on close, fired count + full
  owned/code/phase/disposition in every outcome, progressive `bytes_written`,
  plus true short-once completion, partial-then-fail (bytes_written==1), and
  write-then-close combined primary+secondary.
- **Missing injections (R2-4):** prior generic early `drift-reader` + successful
  writer (which never exercises its identity-refusal branch) proved no late
  boundary. Added real-helper-then-inject wrappers (never fake success) with
  exact target paths for late-control/retained, drift-after-render/before-claim,
  drift-after-source/before-manifest, post-readback edit, post-replay same-byte
  replace, root/ancestor replace, plus 5 new test methods asserting exact
  deltas/behaviour.
- **Preclaim placement (R2-5):** prior helpers ran before first P2V/render with
  no boundary at 780–792, and dynamic-pin check silently ignored new paths.
  Added post-render/preflight PRE_CLAIM `_recheck`+`_compare` (zero delta, HEAD
  before writes) and strict new-path refusal for both P2V observations (second
  allows exactly the 4 owned outputs by original bytes).
- **Ownership (R2-6):** prior held-fd-only checks miss rename-away (fd
  unchanged). Added canonical lstat + ancestor alias walk before EACH file,
  earliest post-mkdir entry stat with three-way bind (earliest/fstat/current),
  honest blind-window qualification, and FINAL repo-root entry check.
- **Close masking (R2-7):** prior silently discarded secondary closes,
  fsync failure not assigned to primary (masked by close), FINAL caught only
  `StagedSourceError` though `_entry_identity` raises `RetentionError`.
  Corrected to single-close-once with secondary recording (no blind retry on
  reused numbers), fsync assigned to primary, FINAL catches any primary
  (wrapping identity-unknown as `StagedSourceError`) with secondary attach,
  per-file INCOMPLETE-class vs complete-manifest INDETERMINATE kept distinct.
- **Timeout/raw (R2-8):** prior `capture_output` + no pgid + truncated timeout +
  JSON-only success is false. Replaced with exclusive durable child raw/meta
  OUTSIDE fixture cleanup (`P3S_DURABLE_OUTDIR` or `/tmp/opencode`), Popen with
  own process group, TERM→KILL reap, full stdout/stderr preserved and returned,
  justified bounds 240s materialize / 120s verify / 60s FIFO (not guessed 300s).
- **Oracles/no-write (R2-9):** prior O12e whole-tree equality (ignores real
  root+empty-file partials), O12b subset allowance, O12c/d missing
  unchanged-originals/exact partials, O13/O6a writer TOOL_DRIFT forced on
  unreachable paths. Corrected to exact per-fault deltas with fired/code/phase,
  unchanged-originals with fault present before repair, and standalone artifact
  verifier TOOL_DRIFT (healthy set → tamper S2 dep → verifier TOOL_DRIFT) with
  earlier refusals labelled separately.
- **Pyc bypass (R2-10):** prior arbitrary same-basename `.pyc` tolerance kept.
  Corrected to outright `RUNTIME_BINDING_PYC` refusal; normal source imports
  under isolated cache prefix still bind via `.py` `__file__`.

No new paths beyond the selected 3A; no existing-source/schema/loader change.
No scope reduction: all contract cases are implemented, not descoped. No
runtime PASS is claimed (no execution in this unit).

## Exact method/seam map (new3 line numbers in corrected bytes)

Module `survey_editorial_staged_source_v2.py` (1836 lines):

- `_check_runtime_binding` 375–421: R2-10 pyc refusal + tripwire (file-pin
  producers skipped, no hotpatch proof claimed).
- `_snapshot_originals` 269–293, `_compare_original_boundary` 295–341 (zero
  vs owned-4-file deltas, deletions+additions, modes/sizes), 
  `_recheck_consumed_pins` 342–373 (HEAD + live/retained pins + reverify).
- Writer PIN/W0 456–623 (strict root first, narrow pins, config cross-check,
  S2 37/route sorted, route schemas as schemas, dep pins+sizes).
- First P2V + strict new-path refusal 649–683 (R2-5: overlaps byte-identical,
  new paths `OBSERVER_NEW_PIN`).
- W3 render + preflight 684–784, PRE_CLAIM boundary 799–803 (R2-5: after
  render, zero delta, HEAD before writes).
- CLAIM earliest entry + three-way bind 817–891 (R2-6) with blind-window qual.
- `_write_owned_file` 1205–1407: R2-6 canonical entry+ancestor walk per file,
  single-close-once with secondary recording, progressive `bytes_written`
  1354, fsync assigned to primary (R2-7), no silent discard.
- Pre-manifest 900–910 (3 outputs only), manifest LAST, `_verify_outputs`
  1422–1438, replay + second P2V 893–1010 with `OBSERVER2_NEW_PIN` allowing
  exactly original 4 outputs (R2-5).
- FINAL 1011–1190: R2-1 owned-delta tree 1048–1065, exact 4-file closure,
  per-file bytes/sizes, FILE_REPLACED for all 4 (no manifest exemption),
  root entry check, `FILE_IDENTITY_UNKNOWN` wrapping (R2-7), primary-preserving
  staged-dir close, HEAD/pins/reverify, INDETERMINATE close with diagnostics.

Test `test_survey_editorial_staged_source_v2.py` (1908 lines, 26 methods):

- Helpers: `_durable_base` + `_run_fixture_code` 220–300 (180s, pgid, durable),
  `_P3S_MATERIALIZE_SCRIPT` r-string, `_P3S_VERIFY_SCRIPT` r-string,
  `_P3S_FAULT_SCRIPT` r-string 277–562 (R2-2 syntax, R2-3 fd leaf+gen
  360–370, write/short/partial/combined 384–402, fsync/close 411–433,
  fstat/mkdir 440–451, exact-reader drift 452–469, R2-4 wrappers 470–593,
  fired+structured outcome + staged-helper restore 594–610).
- `_run_p3s_fixture` 636–710 (R2-8: exclusive durable dir outside cleanup,
  `start_new_session`, TERM→KILL reap, 240/120/60s justified bounds, full
  raw preserved + returned).
- `_materialize` 865–888 (R2-1: allowed = staged dir + 4 files), `_verify`
  890–900 (120s), `_capture` 810–849 (R2-1: files + explicit retained ancestor
  dirs), `_retamper_manifest` (digest+canonical recomputed per R4).
- O1 916 / O2 940 (healthy LF/Weekly + replay, prose deltas, 37 sorted deps).
- O3 955 (P1 `RETENTION_DEST_CONFLICT` + P2R VERIFIED + P2V SCOPE_BOUND).
- O4 976 (live-State drift: replay VERIFIED, writer `OBSERVER_REFUSED`).
- O5 1000 (artifact-only HEAD independence, no HEAD compare).
- O6a 1021 (R2-9: healthy set → tamper import-only dep → verifier TOOL_DRIFT,
  no-write, restore re-verifies) / O6b 1062 (KEEP preempts honestly, not
  TOOL_DRIFT).
- O7 1090 (missing/ordinary/malformed/stale-upstream, fault-present no-write).
- O8 1145 (extra-aux, duplicate-key, wrong-path, unknown-field, swapped deps
  with recomputed digest).
- O9 1201 (alias reader, FIFO reader 60s no-hang, symlinked scope parent).
- O10 1281 (in-place `%` → REPLAY_MISMATCH; same-byte replace → VERIFIED).
- O11 1329 (pre-existing root, post-readback changed-byte swap).
- O11b 1609 (drift-reader, fired==1, exact reader-rel delta) + O11c 1692
  (late-control/retained, exact injection present) + O11d 1726
  (drift-before-claim/manifest at later boundaries) + O11e 1748
  (post-readback edit, post-replay same-byte FILE_REPLACED proving writer
  identity branch) + O11f 1782 (root/ancestor replace before writes).
- O12a 1385 (truncated/empty-subdir/zeroed verify-level tamper).
- O12b 1431 (R2-9: exact per-fault root+main.tex vs {} + fired/code/phase +
  bytes_written==0 + live-unchanged).
- O12c 1475 (R2-9: fsync/close exact partials + fired + INDETERMINATE +
  live-unchanged).
- O12d 1524 (R2-9: manifest-write exact root+3+empty-manifest vs manifest-close
  exact root+4 + fired + INDETERMINATE + live-unchanged + close bytes verify).
- O12e 1582 (R2-9: fstat-fake exact root+empty-file, not whole-tree no-write).
- O12f 1631 (R2-3: short-once MATERIALIZED, partial-then-fail bytes_written==1
  with fired==2, write-then-close primary preserved with secondary).
- O13 1630→1802 (R2-9: standalone verifier TOOL_DRIFT + missing-scope
  no-write, restored re-verify).
- O14 1844 (byte-equal existing root refuses, verifier still VERIFIED).
- R1 1866 (pure comment, same-State refresh, basis receipt + head binding,
  non-emission).

Schema unchanged (17 top-level required, strict 8-key contract_identity,
sized refs, `2.0-rc1`/`EDITORIAL_STAGED_SOURCE_V1`/`STAGED_ONLY`).

## Static21 / inherited18 / caches (measured)

- Candidate detached `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status 105 rows
  (3M inherited P2V overlay + 18A new source + 84 pyc; non-pyc 21 = 3M+18A).
- Inherited18 18/18 match vs `expected18-source-correction-v5.json`
  (sha256+bytes+mode 0o664).
- New3 above; future composite21 = 3M+18A, 84 caches separately pinned (P2R
  correction2 inventory, not rehashed here). No `.pyc` created/cleaned by cheap
  checks (`PYTHONDONTWRITEBYTECODE=1`).

## Unresolved limits (no blockers, require root-selected runtime proof)

- No execution: all 26 methods unaudited at runtime; every seam/code/binding
  string is a pre-execution claim for root-selected smoke/affected/full runs.
- Fire-count gap closed in shape (fired asserted), but runtime must prove each
  fault actually fires at the intended seam (especially `created` vs `active`
  leaf targeting, `drift-reader` exact-rel match on both routes, manifest leaf
  targeting without `created[3]` index, and TOOL_DRIFT-vs-KEEP preemption).
- Ancestor-replace *during* a write is covered by pre-write alias refusal +
  held-fd + canonical recheck + FINAL, not mid-syscall swap injection (honestly
  disclosed; contract promises no post-final-injection guarantee).
- Weekly has no `canonical_reader_bytes` equivalent; Weekly replay binds FILE
  bytes to canonical digest (same as P2V) — disclosed limitation.
- `_check_runtime_binding` remains a tripwire, not hotpatch proof (disclosed).
- `OWNED_PARTIAL` disposition for CLAIM-phase output failures maps to
  INCOMPLETE-class (contract string is `INCOMPLETE`); tests assert codes, not
  the disposition string — standing qualification, not a shape blocker.
- `sha256_object` vs pretty-file-bytes distinction retained per Q8 (writer and
  verifier use the same `_manifest_digest`, so internal consistency holds).
- No crash-atomicity/power-loss/replica/global-CAS/no-drift claims; no
  adoption/Production authority; no candidate/reconstruct commit/push.

## Verdict

Bounded source-only R2 correction: all ten R2 blockers plus outstanding R1
shape gaps are implemented in shape in the corrected new3 (lines cited above).
No concrete source-only blocker remains; no scope exceedance (still 3A/0M,
existing18 untouched). All reachability/exactness/binding claims require
root-selected runtime proof; this review confers no execution PASS, no
adoption/production authority, and no tooling acceptance.
