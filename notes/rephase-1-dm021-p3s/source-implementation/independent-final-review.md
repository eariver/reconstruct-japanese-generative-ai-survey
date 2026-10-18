# DM021-P3S independent final review — author-independent, actual-source (fresh)

2026-10-18 UTC. Fresh reviewer, not candidate/test/tool author, not root reviewer.
No delegation. Read-only except this new file. No runtime imports/tests/fixtures/
DB/index/network writes. Only readonly `Read` + `sha256sum`/`stat`/`git rev-parse`/
`git status` (sanitized env) used for identity. All `file:line` below are
observations at frozen R11 bytes, not standing references.

Prior `independent-preexecution-resolution-r1.md` wrongly said blockers resolved
in shape; root R2 (`astra-code-draft-review-r2.md`) concrete defects supersede it.
This review re-verifies each R2 item at frozen R11 source + runtime raw, and does
not revive the superseded conclusion.

## 0. Inputs read

- Fixed contract `outputs/rephase-1-dm021-staged-source-contract-decision.md`
  SHA256 `42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472`
  (104 lines, re-checked header; hash not recomputed here, root-pinned).
- Mandatory `notes/rephase-1-dm021-materialization/astra-review-resolution.md`
  S1–S5 + `independent-design-review.md` §§0–7 incl. §7 closeout qualification.
- `notes/rephase-1-dm021-p3s/task.md`, `astra-implementation-selection.md`,
  `interface-correction.md` §§2–7, `source-binding.md`,
  `astra-code-draft-review-r1.md` (R1–R5), `astra-code-draft-review-r2.md` (R2-1..10),
  `astra-smoke-selection-r5.md`, `astra-smoke-retry-b3.md`,
  `astra-batch-a-selection-r6.md`, `astra-batch-a-resolution-selection.md`,
  `astra-batch-b-resolution-selection.md`, `astra-replay-fault-batch-selection.md`,
  `astra-write-fault-batch-selection.md`, `astra-seven-correction-selection.md`,
  `astra-r1-fixture-resolution-selection.md`, `astra-postsmoke-oracle-review.md`,
  `astra-presmoke-disposition-r3.md`, `astra-final-evidence-selection.md`.
- Full actual frozen new3 (module 2095 lines, schema 157 lines, test method
  census via `ast.parse` + targeted reads; embedded scripts via literal-eval +
  `ast.parse`, no execution). Needed inherited helpers spot-read at pinned
  bytes only for callsite shape (P1 `_validate_scope`/`_Collector`/`_pin_proposal_layout`,
  P2R `_Session`/`verify_retention`, P2V `observe_current_authority`, route
  renderers/closures, `surface_gate` review loader, `core` digest/bytes).
- All batch raw: `smoke-r5b3`, `smoke-r6-batch-a`, `smoke-r7-batch-b`,
  `smoke-r8-batch-c`, `smoke-r9-batch-d`, `smoke-r9-batch-e`,
  `smoke-r10-batch-f`, `smoke-r11-batch-g` (`batch-*.record.txt`,
  `launch.*`, `run_p3s_b3.{stdout,stderr,stage-done,pre,post}.json`,
  durable `fixture-raw/child.*` script/error refs sampled for oracle binding).
  `smoke-r5-20261018T074631Z` first B2 failure preserved.
- Static binding: `draft-history-r5..r11/static21.json` + `correction-report-r6..r11.md`
  + `prior-bytes-r*/` + `static21-r*-preserved.json` + batch diagnosis docs.
- Packaging: `evidence-20261018T154812Z-final-packaging/gen-complete21/`
  GEN only read (patch + sha + stage-done + console). No PROOF packet found at
  review time — **packaging PROOF pending, not reviewed; may supplement later**.
  No finding depends on it.

## 1. Frozen candidate identity (readonly, measured)

- Copy: `/tmp/opencode/jgas-dm021p3s-impl-20261017T092635Z/candidate-partial-b40de60`
- `HEAD 409b292756dd1277b9dfae87679934c0d2ce251c` (detached),
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  status 105 rows (3M+18A+84pyc; index empty, remote inert
  `example.invalid`, no alternates) — matches every batch `PRE/POST` record.
- R11 new3 (readonly `sha256sum`/`stat`, matches `draft-history-r11/static21.json`
  `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5`):
  - `scripts/survey_editorial_staged_source_v2.py` 126181 B 0o664
    `7059166e075d1a10aacdd375bb8193881f0bfb2ca3e67dd142e175a349031c65`
  - `schemas/editorial-staged-source-manifest-v2.schema.json` 5627 B 0o664
    `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46`
  - `tests/test_survey_editorial_staged_source_v2.py` 147845 B 0o664
    `a3bb0f2369ffc131e8ad645759105d165a62fa114e9b4088a2497e4a13dfa036`
    (2622 lines, 26 `test_*` methods + 23 helpers + 4 script constants via AST).
- Inherited18 18/18 + 84 caches 84/84 per R11 `static21.json` (path census +
  recorded hashes; cache bytes not re-executed here; authority is P2V TB1 proof).
- Module AST-OK (22 top defs incl. 2 APIs), test outer AST-OK (49 funcs),
  schema `Draft202012Validator.check_schema` shape per correction reports;
  all 4 embedded child programs `ast.parse` OK via literal-eval
  (`_P3S_MATERIALIZE_SCRIPT` 1120, `_P3S_VERIFY_SCRIPT` 729,
  `_P3S_FAULT_SCRIPT` 13343, `_R1_FIXTURE_PREPARE_SCRIPT` 3388).

## 2. S1 — historical State COPY→KEEP Profile / narrow scope adapter / no liveState/Git verifier

PASS in shape + runtime-bound where exercised.

- Verifier never imports/calls P2V, never validates current State, never compares
  `HEAD==producer_HEAD` (producer_head provenance only, writer 966/1402, never
  compared in verifier). No live `_Collector` in verifier; no dummy HEAD/config,
  no fabricated former-State. Verified by grep: `observer` import only inside
  `materialize_staged_source` 574 (lazy, comment 8–10); verifier 1699–2096 has
  zero `observer`/`_Collector`/HEAD-compare.
- Narrow adapter `_SessionScopeReader.safe(value,label)` 168–188: exact 2-arg
  arity, backed by `session.safe_read(value,label,"VERIFY","INVALID")`, returns
  `root/rel`, records `rels` for post-loader `reverify`. Verifier calls actual
  `p1mod._validate_scope(shim,root_path,scope_ref[path],proposal,rstate,rprofile)`
  1927 with actual retained bytes, requires `RESULT_BOUND` 1931, then
  `session.reverify` 1934. Matches S1 “`col.safe` + passed metadata” contract.
- Historical chain: verifier V2 1811–1902 does actual `verify_retention` 1832,
  SHA-compare 1838–1840, then independent typed hops from original pinned bytes:
  `state:authority COPY_BEFORE_REPLACEMENT` 1861 → basis `state_ref` match 1863 →
  recomputed provisional dest 1866 → retained State read/hash 1869–1871 →
  `State.profile` exact shape 1873 → unique matching `KEEP_IMMUTABLE` 1876 →
  KEEP re-read/hash 1881–1883. Labels/issue/profile bound 1886–1892. Canonical
  `expected_dir` derived from retained Profile only 1903–1909, staged namespace
  checked 1910–1912. No current-mutable COPY originals, no basename-only trust.
- Writer current side correctly uses live `_Collector` 680 + sanitized HEAD pin
  686–691 with triple equality, plus `_prepin_known_live_refs` 719 (hash-bound,
  no fabricated authority; checkpoint artifact map evidence-only 427–449, never
  live-pinned — R1-supersede safe). S1 adapter feasibility blocker from design §4
  is closed: shim preserves after-binding/substantive-PASS/raw-equality via real
  P1 call + bracketed reverify.

## 3. S2 — actual deps incl. transitives/style/runtime path

PASS. Fixed set is implementation-derived, not manifest-chosen.

- `_SHARED_PY` 27 entries 87–115 + `_SHARED_SCHEMAS` 5 (incl. self) 117–123 +
  route extras 3 (reader DIRECT-USE, receipt/semantic-pub FILE-PIN) 129–133 +
  `STAGED_MODULE` + `STYLE_PATH` = 37; `_route_code_deps` sorts unique and
  asserts `27+5+3+1+1==37` 140–142. `code_deps` manifest order is construction
  sorted order; writer 964–965 and verifier 1788–1790 enforce exact sorted-name
  equality with `CODE_DEPS_MISMATCH` before replay.
- Pins are measured `dep_pins/dep_sizes` via `session.safe_read` (writer 668–671,
  verifier 1793–1796) with byte+size equality 1799–1802; schemas pinned before
  validator reread (writer 625–629/650–651, verifier 1730–1732/1777–1778) and
  rechecked after. Route schemas loaded as schemas (writer 659–666), never
  validated as reader instances against themselves (R1-1 fixed).
- Runtime binding `_check_runtime_binding` 501–545: loaded `__file__` must resolve
  to pinned repo-rel path with matching bytes; semantic-pub FILE-PINs skipped
  516–518 (never imported/executed); arbitrary same-basename `.pyc` refused
  526–530 (R2-10 fixed — no tolerant path bypass). Tripwire limit honestly
  documented 502–511, not hotpatch proof.
- Lazy P2V import keeps writer-only dep out of verifier closure (S2 “no silent
  leak”); file-pin-only producer CLIs never executed (`_check_runtime_binding`
  skips them, verifier never imports them). KEEP config/tool rows enforced
  through called P2R + typed re-reads, never live config substitution.

## 4. S3 — manifest complete basis/proposed/style/refs + strict schema/hash/error + close

PASS with one standing disposition-label qualification (not a blocker).

- Schema 157 lines: `schema_version 2.0-rc1`, `kind EDITORIAL_STAGED_SOURCE_V1`,
  `status STAGED_ONLY`, 17 top-level required, strict `additionalProperties:false`
  throughout, 8-key `contract_identity`, sized `outputs`/`style_input_ref`
  (`path/sha256/byte_count`, `byte_count>=1`), `code_deps` array of sized refs,
  `producer_head` 40-hex, `manifest_digest` 64-hex. Route enum only the two
  supported routes; `active_revalidation_ref` nullable; no aux/temp/unknown.
  Sorted/unique/exact-37 enforced in code (S2), not schema alone — acceptable per
  selection (verifier refuses before replay).
- Writer manifest 941–968 carries exact `proposal_ref` (path/sha + 4 IDs),
  `retention_manifest_ref`, `scope_review_ref`, labels + route (derived via
  `_route_of` 548–565 from valid profiles, never caller enum), complete `basis`/
  `proposed` lossless (equality rechecked 974–977), 3 output refs + sized style
  input + sorted `code_deps` + producer HEAD. Digest `_manifest_digest` 209–212
  (`sha256_object` minus digest) + canonical `_canonical_json_bytes` 191–206
  (recursive key sort, semantic array order preserved, `core.json_bytes`);
  equality/contract-identity checked before canonical projection 970–980. No full
  P2V `input_hashes` persistence, no self-hash cycle (maps stay in memory).
- Manifest LAST: 3 outputs emitted 1095, pre-manifest boundary 1104–1111, manifest
  write 1113, readback 1117, then replay/second-P2V/final before return 1119–1378.
  Pre-write refusal leaves nothing (exclusive claim only after PRE_CLAIM);
  post-claim preserves owned partials + structured phase/per-file/primary+secondary
  disposition; no truncation/rewrite/rollback/resume. Failed close/final with
  complete valid bytes reports `INDETERMINATE_INVOCATION` (writer 1384, fsync
  1623, close 1646, replay/observe2/final 1121/1131/1212), never success; later
  verifier attests byte-consistency only. Primary survives secondaries via
  `_attach_close` 244 + `_close_session` never passing `StagedSourceError` as
  P2R `prior` 251–266 + write/fsync/close/readback paths 1597–1665.
- Qualification (standing, not blocking): CLAIM phase uses disposition
  `OWNED_PARTIAL` (1011) where contract text names `INCOMPLETE`. Tests assert
  typed `code/phase` (e.g. `STAGED_FILE_WRITE_FAILED`) not the disposition string
  for O12b, so runtime passes regardless; SET-completeness is proven by FINAL
  inventory, not the disposition label. Record as label variance, not semantic
  failure. No `STAGED_INCOMPLETE` rewrite, no always-invalid failed-manifest claim.

## 5. S4 — actual fresh P2V ×2 + original/supplemental domain + exact delta + late final checks + owned identities + no cleanup

PASS.

- Strict current root before broad inventory: `_Session(root)` 589 + HEAD pin 594
  before narrow pins 597–629, broad snapshots only after canonical roots 735–758.
  No unvalidated Profile/manifest-prefix trust; sanitized Git env enforced.
- In-call P2V #1 794 + ref/path+SHA match 808–816 + before/upstream/proposed
  digest match 822–832 + `observed_head==head_pinned` 805 before any write.
  P2V #2 1134 + stable-fact compare to original AND first observation 1144–1173
  (refs, digests, both HEADs); never whole-map equality. New outputs legitimately
  appear in second map but must equal original expected bytes 1181–1193, never
  rebaselined.
- Dynamic pins (R2-B1/R3-B1): prepin known plan rows 719, supplemental
  hash-bound pins from first observation 839–878 (overlap must be byte-identical;
  new paths safe-pinned vs returned expected hash, immutable, conflict with
  recorded retention plan refuses). Supplemental rechecked at pre-claim 991,
  pre-manifest 1104, final 1361–1368; never replaces original values
  (conflict refuses 483/1363). Second-observation unexpected new path refuses
  1207. Contract §5.2 dynamic-pin requirement closed without historical
  whole-tree/self-hash equality.
- Reader: independently pinned staged reader + P2V digest + canonicalizer +
  actual renderers 879–934 (Longform `canonical_reader_bytes` equality 921,
  Weekly byte path 929–932, heading/closure checks, exact style-template bytes);
  no private `_pipeline_data`, no public P1 after retention.
- Ownership: exclusive dirfd `mkdir` 1032 + earliest entry stat 1043 + open 1052 +
  fstat 1059 + entry-vs-fd + earliest triple bind 1077–1080 before any file write,
  with explicitly qualified blind mkdir→earliest window 1015–1023 (no race-free
  claim). Files `O_CREAT|O_EXCL|O_NOFOLLOW` 1541 + fstat 1567 + entry bind 1581
  before bytes; held-fd + canonical entry + original pinned ancestor identities
  rechecked before EACH write 1472–1539. Attempt→identity→progress/bytes/fsync/
  close/readback state recorded 1467–1470/1613/1628/1650/1665; unknown identity
  explicit 1061/1570.
- Fault seams real: short/zero loop 1601–1613 with progressive `bytes_written`,
  `fsync` 1619 with `FSYNC_FAILED→INDETERMINATE`, close 1635 with primary-preserved
  secondary attach, readback mismatch 1660. Pre-manifest 3-output-only boundary
  1099–1111 + FINAL 4-file + zero control/retained + tree-equals-original+owned-4
  1239–1262 + staged closure/bytes/sizes 1263–1271 + same-inode identity for all 4
  (manifest exemption removed) 1314–1326 + root/entry rebind 1221–1306 + original/
  supplemental pin recheck after helpers 1349–1370. No takeover/retry/cleanup/
  rewrite; no global CAS/crash-atomicity claim (durability comment 1614–1617).

## 6. S5 — actual faults / primary+secondary / partial vs complete/failed manifest / no-write before repair / R1 same-chain / ordinary review distinction

PASS (qualified scoped evidence, §8).

- 26 methods present (AST census §1); oracles call real APIs with real fixtures,
  assert exact codes/phases/dispositions + bytes/sizes/identities + immediate
  fault-present no-write/owned-delta before repair. No `mock` as oracle, no
  comment-only coverage, no placeholder seams.
- Fault taxonomy covered at runtime (per batch stderr/raw): O12b zero/write/fstat/
  mkdir→`INCOMPLETE`-class; O12c fsync/close with complete bytes→`INDETERMINATE`
  + exact root+main partials; O12d manifest write/close→`INDETERMINATE` with valid
  bytes still `VERIFIED`; O12e fstat-vs-entry mismatch + exact owned partials;
  O12f short/partial/combined primary+secondary; O11b mid-call drift→
  `STABILITY_VIOLATION/PRE_WRITE`; O11c late control/retained after second P2V→
  `ORIGINAL_DRIFT/FINAL`; O11d pre-claim/pre-manifest; O11e post-readback vs
  samebyte (`SNAPSHOT_FAILED`+nested `FILE_REPLACED` correctly distinguished);
  O11f root vs ancestor branch codes; O10 same-inode refuse vs same-byte/new-inode
  `VERIFIED`; O9 alias/FIFO no-read without hang; O8 path/ref/schema/inventory
  incl. basis/proposed/style/contract-identity; O7 missing/ordinary/malformed/
  stale-upstream with `REQUIRES_OWNER_DECISION` non-binding + ordinary-without-block
  removal cases; O6a `TOOL_DRIFT` reaching check vs O6b honest earlier KEEP
  preemption; O4 live-State mutation replay-positive/materializer-refuses;
  O5 artifact-only HEAD independence; O3 P1-refuse/P2R-VERIFIED/P2V-SCOPE_BOUND
  coexistence; O13 immediate no-write; O14 existing-root refusal; R1 genuine
  non-emitted comment + committed fixture refresh on SAME chain binding head/
  receipt/non-emission/reader digest.
- Shared `_P3S_FAULT_SCRIPT` observer wrapper change (R10) and R1 helper/script
  changes correctly scoped: R10→R11 `ast.dump` shows exactly 1 changed constant
  (`_R1_FIXTURE_PREPARE_SCRIPT`) + all 49 funcs otherwise identical; R9→R10
  exactly 9 nodes (6 methods + R1 helper + fault script + class aggregate).
  Affected6 (O11d/O12b–f) rerun at R11; other fault-using successes stay bound
  to old pins — no silent transfer claimed here.

## 7. 26 distinct successes — qualified scoped evidence, NOT a full26 run

Each method passed once at its recorded pin; no single invocation ran all 26.
Do not cite this as a full26 PASS or transfer acceptance to R11.

| Method | Pin (test SHA8) | Batch raw (ran/pass) |
|---|---|---|
| O1 Longform + replay | `6b35a3e5` (R5) | `smoke-r5b3/run-b3-o1o2` 2 ran/2 ok 855.750s; child/runner/launcher 0, `post_errors[]` |
| O2 Weekly + replay | `6b35a3e5` (R5) | same packet as O1 |
| O3 coexistence | `0e1cc20f` (R6) | `smoke-r6-batch-a` 2 ran (O3 ok, O4 fail) 951.172s; fail-fast stops, 6 unrun |
| O4 live-State | `cf2bddd6` (R7) | `smoke-r7-batch-b` 5 ran (O4/O5/O6a/O6b ok, O7 fail) 1975.991s |
| O5 artifact HEAD | `cf2bddd6` (R7) | same R7 packet |
| O6a TOOL_DRIFT | `cf2bddd6` (R7) | same R7 packet |
| O6b KEEP preempt | `cf2bddd6` (R7) | same R7 packet |
| O7 scope | `955f6fb5` (R8) | `smoke-r8-batch-c` 2 ran (O7 ok, O8 fail) 953.654s |
| O8 tamper | `b9f41323` (R9) | `smoke-r9-batch-d` 9 ran, O8/O11/O11d ok, 6 fail 4449.573s |
| O11 preexisting+postreadback | `b9f41323` (R9) | same R9-D packet |
| O11d preclaim | `b9f41323` (R9) | same R9-D packet |
| O12a verify-tamper | `b9f41323` (R9) | `smoke-r9-batch-e` 9 ran, 8 ok (O12a–f/O13/O14), R1 fail 5810.125s |
| O12b during-write | `b9f41323` (R9) | same R9-E packet |
| O12c fsync/close | `b9f41323` (R9) | same R9-E packet |
| O12d manifest-fault | `b9f41323` (R9) | same R9-E packet |
| O12e fstat | `b9f41323` (R9) | same R9-E packet |
| O12f short/partial | `b9f41323` (R9) | same R9-E packet |
| O13 no-write | `b9f41323` (R9) | same R9-E packet |
| O14 existing-root | `b9f41323` (R9) | same R9-E packet |
| O9 alias/FIFO | `6b6bd1f0` (R10) | `smoke-r10-batch-f` 7 ran, 6 ok, R1 fail 3664.477s |
| O10 same/new inode | `6b6bd1f0` (R10) | same R10-F packet |
| O11b midcall | `6b6bd1f0` (R10) | same R10-F packet |
| O11c late control | `6b6bd1f0` (R10) | same R10-F packet |
| O11e post-readback | `6b6bd1f0` (R10) | same R10-F packet |
| O11f root/ancestor | `6b6bd1f0` (R10) | same R10-F packet |
| R1 same-chain | `a3bb0f23` (R11) | `smoke-r11-batch-g` 7 ran/7 ok 5634.188s; child/runner/launcher 0, `post_errors[]` |
| O11d rerun | `a3bb0f23` (R11) | same R11-G packet |
| O12b–f rerun (6) | `a3bb0f23` (R11) | same R11-G packet (affected checks for R10 wrapper change) |

Source binding: module `7059166e` + schema `4fa61723` unchanged since R5
positives (all batch `PRE` static21 checks); test bodies for unchanged methods
verified identical via `ast.dump` across R5→R11 reports (O1/O2 helper bodies
identical R5→R6; 48/49 identical R8→R9; 41/49 identical R9→R10 with only the 6
corrected methods + R1 helper + fault script changed; 48/49 identical R10→R11
with only `_R1_FIXTURE_PREPARE_SCRIPT` changed). Earlier successes stay bound to
their pins; R11 reran only R1 + 6 affected + O11d. This is explicitly qualified
scoped evidence, not a full26 run and not an acceptance transfer.

Failure packet preserved, no retroactive clean run:

- First attempt `smoke-r5-20261018T074631Z/` executed 0 tests: runner B2 called
  nonexistent `os.lexists` before guarded try/outdir/PRE; its own exit was never
  captured (`wait127` was later shell artifact). Packet line56 generic-handler
  claim is wrong; retry `smoke-r5b3` is the only valid O1/O2 evidence.
- Subsequent failures preserve erroneous oracles / missed reviewer claims and
  honest early-guard preemption, not runtime defects: R6 O4 `LAYOUT_REFUSED` vs
  `PIN_FAILED` (extra `p3s_artifact_probe` key forbidden by State
  `additionalProperties:false`); R7 O7 `SCOPE_ORDINARY_INVALID` vs invented late
  reachability (unsupported `NEEDS_SCOPE_DETAIL`); R8 O8 `BASIS_MISMATCH` vs
  `CONTRACT_IDENTITY_MISMATCH` (complete-basis equality correctly fires first);
  R9-D six (O9 substring-timeout, O10 byte-identical `%` no-op, O11b early-layout
  preemption, O11c dirty-receipt preemption, O11e outer `SNAPSHOT_FAILED`, O11f
  symlink `ENTRY_FAILED`) with exact durable child JSON/script/error refs in
  `batch-d-diagnosis-r9.md`; R9-E/R10-F R1 fixture-oracle defects (snap0 before
  staging + P1 file-only snapshot vs directory delta; then R1 refresh-target
  allowlist). Each was corrected test-only with preserved raw; no failure was
  relabeled green or deleted.

## 8. Limitations (travel with any verdict)

- Initial mkdir observation window explicitly qualified (1015–1023): swap between
  exclusive `mkdir` and earliest entry stat is a blind window, not a detected
  case; detection covers every replacement after earliest stat via fd/entry bind.
- No global CAS, all-writer exclusion, crash-atomic multi-file transaction,
  power-loss/replica guarantee, or continuous no-drift. Test checked boundaries
  only; no promise about injection after every final observation.
- Runtime tripwire (`_check_runtime_binding`) is not hotpatch proof; pyc-only
  provenance now refuses (R2-10) but in-process substitution beyond file bytes
  is out of scope.
- Runner/launcher/GEN/PROOF scripts are exact-run tools, not certified rerunners;
  namespace diagnostics for B3 did not execute GEN/PROOF.
- Synthetic reviews/fixtures are not genuine approvals; staged `VERIFIED` is
  byte-consistency + deterministic replay only, never publication admission,
  Gate/Candidate/Preview, rendered QA, migration, or live-adoption authority.
- Weekly has no `canonical_reader_bytes` equivalent (FILE-bytes-to-digest bind,
  same as P2V) — disclosed.
- Ancestor-replace *during* a write is covered by pre-write alias + held-fd +
  canonical recheck + FINAL, not mid-syscall swap injection.

## 9. Blocking defects

**None found at frozen R11 that invalidates the 3A/0M boundary, closed 4-file
namespace, freshness/ownership rules, historical-namespace verifier, replay/
TOOL_DRIFT policy, or expressly OPEN promotion debt.**

All root R2-1..10 items verified closed in source + runtime where applicable:
whole-map equality replaced by original+owned-4 delta (1246–1262); embedded
fault scripts all `ast.parse` OK (no top-level indent fault, no duplicate
`__main__`); structured `fired`/`observer_calls`/phase/disposition asserted
(68 `fired`, 11 `observer_calls` refs; R11-G 7/7 ok proves firing, not merely
refusal codes); required late injections present (O11c after second P2V,
O11b after first P2V, both with `observer_calls` asserts); preclaim boundary
after render/preflight (991–996); ownership earliest-entry + held/entry/ancestor
checks before each write + FINAL rebind (no manifest skip); primary-preserved
closes throughout (no silent secondary discard, no blind retry); timeout via
killable reaped subprocess with real `timeout` bool assert (not substring);
immediate fault-present no-write + exact owned deltas (no post-repair equality
masquerading, no observed-derived allowances); runtime binding pyc-bypass
refused.

Standing qualifications in §4/`§8` (disposition label, schema-vs-code sortedness,
tripwire, blind window, Weekly canonicalizer) are disclosed bounds, not blockers.
Any future change to inherited18, larger S2 closure, or new authority would be
an exact blocker with new scope decision — none is needed for this verdict.

## 10. Verdict

**BOUNDED PASS — actual-source, qualified scoped evidence.**

- Source: frozen R11 module `7059166e`/schema `4fa61723`/test `a3bb0f23`
  satisfies S1–S5 in shape at cited lines; no concrete code blocker remains.
- Evidence: 26 distinct methods each passed once at its recorded pin (§7 table)
  with saved stdout/stderr/stage-done/pre/post + durable child JSON/script/error
  refs; R11-G proves R1 + O11d + O12b–f at final pins. This is **not** a single
  full26 run and **not** a transfer of old passes to R11. Full26, complete21
  patch apply proof, candidate commit/adoption, Production/State/Gate/Candidate/
  PDF authority, and full promotion remain unselected/OPEN.
- Packaging: GEN `complete-p3s-21path.patch` (`e449d029…`, 1233670 B) read;
  **PROOF (independent clean409 apply) pending — not reviewed here.**
  Supplement after PROOF is read; do not infer it from GEN.
- Stop at Human Commit Point. No candidate/reconstruct commit/push, no live
  replacement, no adoption/authority inference.

*Method: `Read` of contract/S1–S5/§7/selections/reviews + full frozen new3 +
targeted inherited helper reads + readonly `sha256sum`/`stat`/`git rev-parse`/
`status`; `ast.parse` (outer + literal-eval embedded scripts); batch raw +
static21/body-hash comparison R5..R11. No candidate imports, no test/fixture
execution, no DB/index/network writes. Only this file created.*
