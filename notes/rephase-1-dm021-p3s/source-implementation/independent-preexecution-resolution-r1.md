# DM021-P3S independent pre-execution resolution R1 (fresh, source-only)

2026-10-18 UTC. Fresh reviewer, not authors/root. Follow-up to
`source-implementation/independent-preexecution-review.md` (preserved, not
overwritten). Read-only source review, NO runtime: no candidate imports,
no fixture/test execution, no DB/index/network writes. Read
`astra-code-draft-review-r1.md` (R1–R5), `draft-history-r1/correction-report.md`,
`draft-history-r1/coverage-matrix-r1.md`, `draft-history-r1/README.md`, then
full actual corrected new3. Read-only `sha256sum`/`stat`/`git rev-parse`/
`git status --porcelain` only. No subagents. Only this new file created.
Root separately reviews writer and tools; no acceptance inferred.

## 1. Corrected identity (readonly, summary not raw proof)

Copy `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`,
detached `409b292756dd1277b9dfae87679934c0d2ce251c`,
tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status 105 rows:

- `scripts/survey_editorial_staged_source_v2.py` 97353 B 0o664
  `90c950d7b1a11829c06cd6579de0222b9016e173ae4c0d5b7c87994438b95d53`
- `schemas/editorial-staged-source-manifest-v2.schema.json` 5627 B 0o664
  `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46`
  (unchanged)
- `tests/test_survey_editorial_staged_source_v2.py` 68949 B 0o664
  `7b6912e2294ff2e46a86e8f81ae7b5102030fcadf6a62698413164c639b1b8df`

Match author `correction-report.md:16–18` and `coverage-matrix-r1.md:36–40`.
Module 1645 lines, test 1248 lines, schema 157 lines all read. Inherited18 /
84 caches not rehashed here (author `18/18`, `105 rows` is summary).

## 2. B1–B4 verification (independent blockers)

### B1 — during-write faults + fsync — RESOLVED IN SHAPE

- `os.fsync` seam added module 1171–1183 (`FSYNC_FAILED` →
  `INDETERMINATE_INVOCATION`, no atomicity/power-loss claim 1171–1173).
  Short/zero 1156–1170, close-preserving-primary 1184–1201
  (`_attach_close` on write-error path 1192–1193), fstat/entry
  1118–1154, readback 1202–1214, manifest LAST 855–873 all present.
- Faults are scoped wrappers around ACTUAL calls inside the fixture
  subprocess, never mock-replacement of authority/P2V/replay: test
  263–350 (`real_write/real_fsync/real_close/real_fstat/real_mkdir/`
  `real_open` saved 276–277, restored 345–348; `_track_open` 280–284;
  `_write_once` 285–293; `_fsync_once` 294–298; `_close_once` 299–307;
  `_fstat_once` 308–318; `_mkdir_once` 319–323; `drift-reader`
  324–333). O12b 1032–1057 (zero/write/fstat/mkdir → `INCOMPLETE`-class
  codes + admitted-delta + live-unchanged), O12c 1059–1087 (fsync/close
  → `FSYNC_FAILED`/`CLOSE_FAILED` + `INDETERMINATE`; close partials
  exactly root+main.tex 1086), O12d 1089–1112 (manifest-write/close →
  `INDETERMINATE`; complete bytes stay `VERIFIED` 1109–1112), O12e
  1114–1125 (`fstat-fake` → `STAGED_FILE_REPLACED`, no-write), O11b
  1127–1146 (`drift-reader` → `STABILITY_VIOLATION` with exact allowed
  delta 1145). O12a 986–1030 is now explicitly labelled verify-level
  tamper (`PIN_UNREADABLE`/`STAGED_SET_MISMATCH`/`REPLAY_MISMATCH`),
  not fault injection. Comment-vs-injection distinction fixed.
- Reachability limitation (not a shape blocker, requires runtime
  proof): `manifest-write-fail`/`manifest-close-fail` target
  `created[3]` test 291/304–305, assuming manifest is the 4th `O_CREAT`
  fd (3 outputs 855–856 then manifest 872–873). Any unrelated `O_CREAT`
  in the fixture process would shift the index. `drift-reader` fires
  only when `Path.name == "reader-surface-input-v2.json"` test 327
  while O11b runs an LF chain 1135–1139; whether the LF staged-reader
  basename matches is not proven source-only. Both need the
  root-selected run to prove the fault actually fired (outcome
  `ok:False` + expected code alone does not prove fire-count; the
  script tracks `fired` but never prints it).

### B2 — O10 same-inode vs new-inode — RESOLVED IN SHAPE

- Test 882–928 now documents byte-consistency semantics 883–888:
  in-place `%` edit → `REPLAY_MISMATCH` 907–911; same-byte `os.replace`
  swap → `VERIFIED` 920–925 (not refusal). Matches verifier shape
  (replay bytes 1531–1534, closed set 1555, digest 1557, canonical 1559 —
  no owned-identity oracle in replay). Writer FINAL retains the
  identity oracle for all 4 files 977–983 (old manifest skip removed).
  The prior overclaim is gone.

### B3 — O7/O8/O9/O11 coverage gaps — RESOLVED IN SHAPE

- O7 694–747: missing / `NEEDS_SCOPE_DETAIL` / `{not json` (now without
  `encoding=` — old TypeError gone) / `upstream_override="0"*64` →
  `SCOPE_STALE_UPSTREAM` 746, each with fault-present snapshot
  (714/725/740) and no-write. Stale-upstream added.
- O8 749–803: extra-aux → `STAGED_SET_MISMATCH` 766, duplicate-key
  refusal 776, plus `_retamper_manifest` 523–534 (recompute
  digest+canonical AFTER tamper per R4) for wrong-path →
  `OUTPUT_PATH_MISMATCH` 787, unknown-field → `SCHEMA_INVALID` 794,
  swapped deps → `CODE_DEPS_MISMATCH` 803. All three semantic paths
  present in shape.
- O9 805–880: alias staged-reader 813–837 (unlink + copy + symlink,
  `PATH_ALIAS` 827, fault-present no-write 828, restore 837),
  FIFO staged-reader via killable `_run_p3s_fixture` 120 s 845–854
  (`PATH_NOT_REGULAR|PATH_UNREADABLE|PATH_ALIAS` 852–853, explicit
  no-`timeout` assert 850), symlinked scope-parent ancestor 863–877
  (`PATH_ALIAS` 875). `ThreadPoolExecutor` hang path gone; raw-safe
  `_snapshot` 130–188 (lstat-only, dirs/identities/types, FIFO kind
  without open, walk-error fail-closed) replaces blind `read_bytes`
  + alias-follow + FIFO-block.
- O11 930–969 + O11b 1127–1146: pre-existing root → `STAGED_ROOT_EXISTS`
  947, post-readback changed-byte swap → `REPLAY_MISMATCH` 966, plus
  genuine mid-call `drift-reader` → `STABILITY_VIOLATION` 1144 with
  exact allowed delta (only injected reader change) 1145. Mid-call
  seam present in shape (subject to B1 fire-count limitation above).

### B4 — R1 same-chain binding — RESOLVED IN SHAPE

- Helper `_weekly_prepare_from` test 435–451 reuses the SAME
  `helper/built/chain,state_path` (439) instead of building a fresh
  chain. Test 1202–1238: pure comment commit 1214 (column-0 `#` above
  `def refresh_mechanical_evidence`, AST-identical 392/399–400 —
  old assignment-before-docstring gone), refresh on SAME `state_path`
  1218–1219 with State-changed assert 1221–1222, then
  `_weekly_prepare_from` 1223 → capture/scope/subprocess
  materialize 1224–1228, binding asserts `head == R1 commit` 1229,
  basis receipt bytes 1231–1233, anchor absent from `main.tex` 1235,
  reader digest 1237–1238. The discarded-chain defect is gone in shape.
  Non-emission + receipt linkage still require runtime proof (no
  execution here).

## 3. Root R1–R5 verification (source-only)

- **R1 (positive-path):** R1-1 route schemas as schemas module 528–536
  (`load_schema` both, never instance-against-itself) — fixed. R1-2
  config pinned in Session 494–506 (`orig_config_sha` 506), live-vs-
  Session cross-check 580–583, W1 uses pinned `config_obj` 594 — fixed
  (old `session.files[DEFAULT_CONFIG]`-without-pin gone). R1-3
  `staged_rel` 589 vs `staged_reader_rel` 692 distinct + comment
  687–690; manifest/claim/outputs derive from directory 754/808/1223 —
  fixed (old line-545 overwrite gone). R1-4 runtime binding stays strict
  module 375–414 (file-pin producers skipped 383–385, pyc tolerance
  398–400 kept only with explicit tripwire-limit comment 375–379 per
  Q3 disposition — disclosed, not proof); public ops run in fresh
  fixture subprocesses test 232–261/353–375 (`cwd=root`, sanitized env,
  saved JSON/timeout; no parent-code import for behavior); in-process
  `_materialize` outer-P2V removed 490–512 (kept only in O3 coexistence
  590–594) — fixed in shape.
- **R2 (original boundaries):** helpers `_snapshot_originals` 269–292,
  `_compare_original_boundary` 295–339 (deletions AND additions,
  bytes/sizes/modes, edition-only allowlist), `_recheck_consumed_pins`
  342–372 wired at pre-claim zero-delta 627–631, pre-manifest 3-outputs-
  only 859–870, FINAL 4-file edition + zero control/retained 948–950
  plus tree recompute 951–952. `init_*` consumed 617–623 (old unused
  gone). Second P2V compares normalized path AND SHA vs ORIGINAL and
  vs FIRST 903–916, before/upstream 919–925, proposed 926–929, both
  HEADs 930–932, plus `input_hashes` overlap byte-identity 666–672; no
  whole-map equality — fixed in shape.
- **R3 (ownership/diagnostics):** mkdir attempt recorded 803 + window
  qualified 798–802 (no race-free claim); held-root fstat vs
  `staged_identity` before EACH write 1093–1106 via `dir_identity`
  1221–1224 (`staged_identity` stored 844 and consumed 1221 — old
  unused gone); `_write_owned_file` records attempt→identity→progress
  1088–1092/1128/1170/1183/1199/1214, open/fstat unknown-identity
  explicit 1100/1121; write-error primary preserved 1155–1168/1192–1193,
  FINAL dir-close attach 991–992, final `_close_session` reclassified
  to `INDETERMINATE` 1023–1028 (old `MATERIALIZED` label gone);
  manifest-phase `MANIFEST`/`INDETERMINATE` 862–873, replay/observe/
  final `INDETERMINATE` 880/890/936 — fixed in shape. Disposition
  naming qualification: outputs use `OWNED_PARTIAL` (CLAIM 793–794)
  where correction-report maps it to `INCOMPLETE`-class; contract
  string is `INCOMPLETE`. Tests assert codes (`STAGED_FILE_WRITE_FAILED`
  etc.) not the disposition string for O12b, so runtime will pass
  regardless, but record the string mapping as a standing qualification.
- **R4 (verifier claims + final retained closure):** staged
  basis/proposed vs proposal 1308–1311, proposal_ref 6 IDs 1298–1302,
  top labels 1304–1307, contract identity both sides 1312–1318,
  `style_input_ref` fixed path/hash/size 1540–1545 + style output
  1546–1548 (old self-compare gone) — fixed. V6 repeats retained
  inventory 1571–1580 + COPY byte re-pin 1581–1587 + KEEP `repinned`
  1588–1590 + `lock_map` 1591–1597 (old staged-only final gone); no
  current-State/HEAD authority, no blanket `capture_inputs` equality —
  fixed in shape. `_retamper_manifest` ordering (digest+canonical
  recomputed first) lets targeted codes fire — fixed in shape.
- **R5 (helpers/coverage honesty):** `write_bytes(..., encoding=)` gone
  (723/771 plain bytes); O7/O9 fault-present snapshots (714/725/740/
  821/844/869) replace post-cleanup-only compares; `_snapshot` raw-safe
  130–188; subprocess-with-timeout 353–375 replaces executor-wait;
  `ls-files` entries asserted present 89–91 with `check=True` 80–83
  (no sparse assumption); R1 pure comment + AST check 392/399–400;
  asserts tightened throughout (O3 `ProposalError RETENTION_DEST_CONFLICT`
  587, O4 `OBSERVER_REFUSED` 618, O6a `TOOL_DRIFT` 660, O6b not-TOOL_DRIFT
  688, O10–O14/R1 exact codes above); 21 methods, no O-label-only claim —
  fixed in shape.

## 4. Remaining qualifications (no shape blocker; runtime must prove)

- No execution: all 21 methods unaudited at runtime; every seam/code/
  binding string is a pre-execution claim for root-selected runs.
- Fire-count gap: fault scripts never print `fired["n"]`; a passing
  refusal with expected code does not by itself prove the injected
  fault fired (vs an earlier guard preempting). Runtime should assert
  or log fire-count, especially for `drift-reader` (LF basename match),
  `created[3]` manifest targeting, and `TOOL_DRIFT`-vs-KEEP preemption
  (O6b already asserts not-TOOL_DRIFT 688 — keep that discipline).
- O12b asserts admitted-subset 1054–1055, not exact per-fault partials
  (only O12c close-fail asserts exact root+main.tex 1086). Accept as
  bounded (live-unchanged + admitted-delta) unless root requires exact.
- Ancestor-replace *during* a write is covered by pre-write alias
  refusal + held-fd checks + FINAL rechecks, not mid-syscall swap
  injection (author honestly discloses). Accept as bounded; contract
  promises no post-final-injection guarantee.
- Weekly has no `canonical_reader_bytes` equivalent; Weekly replay binds
  FILE bytes to canonical digest (same as P2V) — disclosed limitation.
- `_check_runtime_binding` remains a tripwire, not hotpatch proof
  (disclosed 375–379). `sha256_object` vs pretty-file-bytes distinction
  retained per Q8 (disclosed). Duplicate `if __name__ == "__main__":`
  test 1241–1247 is a harmless editing duplicate; remove opportunistically.
- Schema unchanged (correctly — R4 code-enforces sorted/exact-37;
  schema stays shape-only).

## 5. Verdict

Bounded source-only resolution: B1–B4 and root R1–R5 are **resolved in
shape** in the corrected new3 (lines cited above). No concrete source-only
blocker remains. All reachability/exactness/binding claims (fire-counts,
LF drift basename, `created[3]` stability, R1 non-emission/receipt linkage,
exact partials, retained closure) require root-selected runtime proof;
this review confers no execution PASS, no adoption/production authority,
and no tooling acceptance.
