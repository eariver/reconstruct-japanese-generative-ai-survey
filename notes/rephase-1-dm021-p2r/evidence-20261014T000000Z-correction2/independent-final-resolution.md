# Independent final resolution — DM021-P2R correction2 (S1–S3 + E1/E2)

2026-10-14. Fresh AUTHOR-INDEPENDENT final scoped implementation/evidence reviewer,
not authors/root/previous reviewer. No tests/application imports/script reruns/source/DB/index/ref/network writes.
Only NEW file written is this resolution. Previous
`evidence-20261013T173500Z-correction/independent-correction-resolution.md`
(blanket R1–R6 resolution) is preserved as historical; per `astra-review-r2.md:3`
it overstated closure. No PASS is transferred from it, from v6/v8 partials,
or from any prior unit.

## 1. Sources read (all read-only)

- Task: `notes/rephase-1-dm021-p2r/task.md` (3A budget, one-shot capture + standalone verifier, no adoption).
- Fixed contract: `outputs/rephase-1-dm021-retention-contract-decision.md`
  SHA256 `194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e` (rehash verified, summary scope).
- `notes/rephase-1-dm021-p2r/astra-implementation-selection.md` (KEEP row shape, X distinction,
  ownership entry+fd chain, canonical inputs, guard completeness, close distinction, fixture fidelity).
- `notes/rephase-1-dm021-p2r/astra-review-r1.md` (R1–R6 CHANGES_REQUIRED, preserved).
- `notes/rephase-1-dm021-p2r/astra-review-r2.md` S1–S3 + E1–E2 (controlling gaps for this review).
- `notes/rephase-1-dm021-p2r/correction2-execution-selection.md`
  (selects final verification on module `3833b14a` / test `36814fe5` pins with static
  `expected16-correction2b.json` + inherited13 + 84-cache inventory; exact-run approval only).
- Promotion basis: `notes/rephase-1-dm021-promotion/astra-review-resolution.md` I1–I4 and
  `notes/rephase-1-dm021-promotion/independent-design-review.md` §§1–8
  (DESIGN_BOUNDED_PASS, I1 profile chain / I2 raw/snapshot/ownership / I3 schema-results / I4 budget-stop;
  design-only, no runtime/adoption authority).
- Correction2 packet `notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/`:
  `correction2-final-report.md`, `correction2-notes.md`, `ready-revision-notes.md`,
  `ready2-notes.md`, `expected16-correction2b.json`, `expected16-correction2c.json`,
  `inherited13-static-freeze.json`, `cache-inventory-static.json`,
  `run_p2r_correction_v9.py.READY` + `.pre/.post/.meta/.exit/.stderr/.stdout/.launch.log/.stage-*.json`,
  `run_p2r_correction_v8.stderr.txt/.stage-done.json` (23/25 + 2 failures),
  `run_affected_c2c_v1.stderr.txt/.stdout.txt`, `run_opt_correction_v3.stderr.txt/.stdout.txt`,
  `gen_16patch_v3.stdout.txt`, `complete-p2r-16path-v3.patch` + `.sha256`,
  `proof_apply16_v7.py.READY` + `.stdout/.stderr/.exit`,
  `proof-freeze-clean-v7.json`, `proof-freeze-applied-v7.json`,
  `proof-copy-000002Z-anomaly-record.md`.
- Final actual candidate `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`:
  full module `scripts/survey_editorial_retention_v2.py` (targeted S1/S2/S3 sections),
  full test `tests/test_survey_editorial_retention_v2.py` (targeted oracle sections).
  No imports, no execution, no Git mutations. Full evidence review is not rerun;
  counts/timings below are cited from persisted raw, except the allowed readonly rehashes.

## 2. Allowed readonly rehash (summary scope, no raw-proof misclaim)

Via `sha256sum`/`wc`/`stat` only:

- `scripts/survey_editorial_retention_v2.py`:
  `3833b14a281ab82999410d91361d5aace3c77015484e621c62077e480b73f5b2`,
  122231 bytes, mode `664`, 2080 lines — matches final-report §1 and `expected16-correction2c.json`.
- `tests/test_survey_editorial_retention_v2.py`:
  `4155baab733e8bddc0b7cbc34b83fe801def2927a716d43132321f8f083d614e`,
  93733 bytes, mode `664`, **1818 lines actual** (`wc -l`), 25 methods per persisted
  `run_p2r_correction_v9.stderr.txt:1-25` (`Ran 25 tests in 7936.817s OK`).
  Report §1 says “1802 lines” — see §7 mandatory errata. Hash/bytes/mode/method-count match.
- `schemas/editorial-retention-manifest-v2.schema.json`:
  `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c`,
  5618 bytes, mode `664` — unchanged since initial, matches.
- `complete-p2r-16path-v3.patch`: `5b79218e3c90fc8bcb11e39571e2ab1e8dfc52e04f5e98843937e4e876515208`,
  830622 bytes — matches saved `.sha256` and `gen_16patch_v3.stdout.txt`.
- Contract `outputs/rephase-1-dm021-retention-contract-decision.md`: `194fd7de…9370e` — matches.
- P1 source-13 unchanged: persisted `run_p2r_correction_v9.pre.json:files` and
  `.post.json:files` both equal static `expected16-correction2c.json` 16 entries
  (verified by `json.load` comparison, not by re-execution); the 13 non-P2R entries
  equal `inherited13-static-freeze.json` pins by inspection
  (`5623c0d9`, `4dadf873`, `7bae9d2a`, `fe4a96f4`, `e8598239`, `5d2fde45`,
  `c09c5558`, `d480e11d`, `4d235a38`, `e7305884`, `f581fad0`, `ce687447`, `4a03b564`).
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`
  in both pre and post. No new HEAD/commit.

## 3. S1 — final inventory boundary + post-verify byte/HEAD/deps binding: CLOSED

Module (final `3833b14a`, 2080 lines):

- `_retained_expected_sets:829-848` — exact COPY-dest + manifest file set and retained-root
  dir closure; used at both final boundaries (comment `:833-835` states late file/empty-dir refusal).
- Verifier final boundary `verify_retention:2043-2056` — full retained re-inventory AFTER
  canonical-bytes check, before `reverify`/close; `expected_files2/expected_dirs2` via
  `_retained_expected_sets`, `INVALID_RETENTION` with `final retained inventory mismatch`
  (`:2049-2051`) and `final retained dir mismatch` (`:2052-2055`).
- Capture post-verify `capture_retention:1561-1687` — fresh `post = _Session` after standalone
  `verify_retention:1562`; rechecks P1 input hashes (`:1571-1576`), HEAD (`:1577-1580`),
  P2R dep bytes (`:1581-1588`), full control inventory (`:1589-1613`), edition owned-delta
  with manifest as exact owned addition (`:1614-1641`, no prefix exemption),
  retained exact sets (`:1642-1657`), **capture-original byte binding** (`:1658-1671`:
  every COPY `inv_files3/size` vs original plan row hash/size; manifest vs `manifest_sha/len`),
  owned dev/ino recheck (`:1672-1681`), then `reverify` + close-all before success.
  This is the ready2 post-verify same-inode fix; comment `:1658-1663` states the threat.
- Pre-manifest finalization `:1347-1422` — P1 hashes, HEAD, retained rehash, KEEP repin,
  control exact equality, edition exact owned delta (manifest not yet in expected).
  Manifest-last exclusive create/fsync/close-checked/readback `:1478-1553`,
  pre-close `reverify:1555` + close-all `:1556-1560`.

Oracles (final `4155baab`, 1818 lines):

- `test_verifier_late_retained_additions_refuse:829-912` — hooks staged-reader read
  (after first inventory + all rehashes), plants retained file / empty dir mid-verify,
  asserts `INVALID_RETENTION` with `"final retained"` in error (`:894-895`),
  mutated-pre/post compared before repair (`:885-892` pre/post, `:899-907` plant removal
  then `_assert_no_write` proving verifier wrote nothing else), restore-to-VERIFIED (`:908-909`).
- `test_capture_readback_control_edition_injection_refuses:1659-1748` — injects
  control file / edition empty dir exactly at manifest open (inside standalone-readback window),
  asserts `FINALIZATION_REFUSED`/`INDETERMINATE_INVOCATION`, partials preserved, retry refuses,
  only injected + owned deltas (`:1707-1726`, `:1736-1748`).
- `test_capture_postverify_inplace_edit_refuses:1750-1814` — wraps REAL `verify_retention`
  (call-through, assert VERIFIED, then same-inode truncating rewrite with flipped middle byte,
  same size `:1788-1792`), asserts capture refuses `FINALIZATION_REFUSED`/`INDETERMINATE`
  (`:1797-1800`), live originals unchanged / owned-prefix-only additions (`:1804-1811`),
  partial + retry (`:1802-1804`, `:1813-1814`).
- Bind-matrix extras in `test_verifier_capture_inputs_deps_dest_dirs_sizes:523-681`
  (extra empty dir refuses `:672-681`; wrong COPY hash / missing dep covered in S3).

No S1 gap remains at the selected boundaries. Claim/open races remain bounded
(no global CAS — preserved limit, not a defect).

## 4. S2 — fstat fail-closed / ownership / primary+secondary close: CLOSED

Module:

- COPY creation fstat `:1262-1280` — on `os.fstat` failure closes new fd, removes from
  `_open_fds`, records `owned["creation_attempts"]=[{path, identity-failed}]`, refuses
  `WRITE_IDENTITY_FAILED`/`OWNED_PARTIAL` BEFORE any write; comment `:1265-1268`
  states no stale-entry reuse. Manifest creation likewise `:1488-1503`
  (`MANIFEST_IDENTITY_FAILED`/`INDETERMINATE_INVOCATION`, `manifest_attempt` identity;
  closed manifest entry carries dev/ino `:1542-1549`).
- `_close_all:243-277` — attaches EVERY secondary close failure to prior structured error
  (`owned.secondary_close_errors` + detail), never `pass`-discards; only raises
  `CLOSE_FAILED` when no primary in flight; never reports closed on failure.
- `safe_read:440-461` + `reverify:501-519` — intermediate-dir close failures preserve
  structured primary (secondaries attached) and only raise `CLOSE_FAILED` when no primary
  in flight; unexpected non-structured primaries chained. `safe_read` close-after-read
  `:418-421` fails the read path (no silent success).
- COPY/manifest write+close `:1306-1319` / `:1527-1539` — primary write error preserved,
  secondary close appended (`secondary_close_errors`), not overwritten. Owned entries carry
  dev/ino/bytes/status (`:1281-1283`, `:1542-1549`); entry+fd identity chain
  (`_open_dir_chain:285-...`, ancestor/entry-vs-fd checks, `FILE_REPLACED` on same-byte replacement
  `:400-407`, `:1327-1335`).

Oracles:

- `test_fault_create_identity_and_close_preservation:1228-1285` — scoped creation-fstat failure
  refuses `WRITE_IDENTITY_FAILED`/`OWNED_PARTIAL`, `written==set()` (zero bytes through fd,
  `:1278`), attempt recorded (`:1279-1281`), partial preserved + retry `RETAINED_ROOT_EXISTS`
  (`:1282-1285`).
- `test_fault_primary_read_close_secondary_preserved:1287-1360` — arms close-failures only at
  proposal-leaf open (`:1308-1314` comment states why), injects primary read error + dir-close
  failures, asserts primary `PATH_UNREADABLE` preserved (`:1355-1357`) with non-empty
  `owned.secondary_close_errors` (`:1358-1359`) and pre-write no-write (`:1360`).
  This is the fixed v8-failing oracle (see §6); v9 green with same expectation codes.
- `test_fault_manifest_write_fsync_close_indeterminate:1088-...` + 
  `test_fault_combined_write_close_primary_preserved:1168-...` — distinct
  `MANIFEST_WRITE/ ZERO/F SYNC/CLOSE_FAILED` all `INDETERMINATE_INVOCATION` per report;
  implementation `:1506-1536` matches (read, not re-executed).

No S2 gap remains at the selected helper/close boundaries.

## 5. S3 — historical verifier precision: CLOSED

Module (`verify_retention`, final):

- Mandatory State labels `:1889-1900` — `rstate.issue_id` must equal proposal;
  `research_profile`/`publication_profile` REQUIRED in retained State (`LABEL_MISMATCH`
  when absent `:1892-1893`, when disagreeing `:1894-1895`); KEEP Profile labels likewise
  (`:1896-1900`). The `if k in rstate` silent accept is removed.
- Provisional COPY-dest mapping BEFORE retained-State read `:1844-1860` — every COPY dest
  vs `<supplied-proposal-dir>/retained/before/<original_path>` (`RETENTION_DEST_MISMATCH`
  `:1857-1859`); retained State read follows at `:1860`. Canonical recomputation vs
  State/Profile-derived `expected_dir` follows `:1916-1925`. No basename/current-State shortcut.
- P2R dep fingerprints as historical observations `:2009-2019` with scope comment
  `:2010-2016` — requires presence + well-formed shape only (`MISSING_P2R_DEP` `:2018-2019`);
  blanket live-producer byte equality removed. Exact hashes still enforced where the same paths
  are independently required (plan rows `:2020-2027`, staged/proposal `:2028-2039`,
  COPY rehash `:1953-1959`, EVERY KEEP repin+size `:1960-1963`, staged canonical names/digests
  `:1964-1988`). Historical extras without retained bytes correctly unprovable (documented).

Oracles:

- `test_verifier_state_labels_required:747-828` — coordinated retained-State + plan-row +
  manifest-row + `proposal_ref` rebind reaching label check; missing/disagreeing labels refuse
  `LABEL_MISMATCH` with immediate no-write and restore-to-VERIFIED (mutated-pre/post before repair).
- Bind matrix `test_verifier_capture_inputs_deps_dest_dirs_sizes:523-681` —
  wrong COPY hash refuses (`:558-566`), missing P2R dep refuses (`:567-570`),
  dep-hash distinction succeeds (`:571-588`, wrong P2R dep hash still VERIFIES with comment
  stating historical-observation scope), unplanted moved-dest refuses `RETENTION_DEST_MISMATCH`
  with v4-history comment (`:589-598`), planted moved-dest records fd-chain reads and asserts
  moved path never read (`:599-665`, esp. `:660-663`) plus no-write (`:660`), bad size refuses
  (`:666-671`). `test583`’s old “read succeeds first” shape is superseded by the planted
  no-read proof; v4 `PATH_MISSING` raw preserved as history only (comment `:595-597`).
- Typed-hop `_check_both` and staged `_corrupt`/noncanonical paths compare immediate
  mutated-pre/post before restoration (`_assert_no_write`, e.g. `:539-556`, `:638-660`,
  `:710`, `:742`); X-vs-required KEEP distinction asserts distinct identity
  (`test_keep_profile_distinction_and_all_drift:916-968`, esp. `:943-945`) with honest
  generic-KEEP labelling (no synthetic X authority).

No S3 gap remains at the selected precision points.

## 6. Evidence guards + raw outcomes (cited, not re-executed)

- Final v9 (`run_p2r_correction_v9.py.READY`, hash `e890cbab…` per report):
  `Ran 25 tests in 7936.817s OK` (`run_p2r_correction_v9.stderr.txt:1-30`),
  `child_rc=0 wrapper_rc=0` (`.launch.log:1-2`, `.stage-done.json:14-16`),
  exit `0` (`.exit`), Python `3.14.4` + forced 5 keys + 28 redacted
  (`.meta.json`, `.stage-running.json:14-21`, child `python -u -m unittest`
  in candidate, own process group per READY header `:2-32`).
  Pre/post (`run_p2r_correction_v9.pre/post.json`): HEAD/tree identical fixed pins,
  `files` both equal static `expected16-correction2c.json` (verified), 84 caches both sides
  equal with full sha/size/mode detail (verified `len 84`, `pre==post`, `cache_detail` equal),
  status `3M13A` source rows + 84 cache rows, index empty. No cleanup (residue preserved).
  Stale in-tree `.pyc` neither executed nor rewritten via absent `PYTHONPYCACHEPREFIX`
  + `PYTHONDONTWRITEBYTECODE=1` per READY guard and `ready2-notes.md:55-58`;
  this review cites the guard + pre/post cache equality, not a live absence re-observation.
- Affected (`run_affected_c2c_v1.py`): `Ran 2 tests in 440.248s OK` (`.stderr.txt:1-7`),
  exit 0 per report; covers the two v8-fixed oracles.
- Optimized (`run_opt_correction_v3.py`, isolated guarded): `Ran 1 test in 250.016s OK`
  (`.stderr.txt:1-6`). Full-suite `-O` unproved (explicit bounded limit; new code uses
  explicit raises only).
- Proof v7 (`proof_apply16_v7.py.READY`): exit `0` (`.exit`), stderr empty,
  `APPLY_PROOF_OK head=409b292… files=16 patch=5b79218e…` (`.stdout.txt:15`);
  active 16 match static manifest, HEAD/tree/index pinned; copy completeness all16 byte-equal;
  active+copy `.git` 134 regular + 96 dirs each, zero problems incl. nlink==1 enforced,
  zero shared (dev,ino) pairs; exact inert remote pair + exact inert config URLs with whole
  outputs persisted (active once, copy pre/post); 84 copy caches inventoried before declared
  removal; clean409 verified (13 NEW absent + 3 MODIFIED byte-equal `git show HEAD:` + empty
  status/index); `apply --check` + `apply` rc 0; applied 16 match static; applied status
  exactly `3M13A` (`proof-freeze-applied-v7.json:4`, `proof-freeze-clean-v7.json:4-5`).
  Outputs exclusively held (`xb`/`x`, no overwrites) per READY docstring `:31-34`.
  Declared disposable-copy-only cache removals separated from run no-write claims.
- Complete16 patch generated via `gen_16patch_v3.py` after final pins
  (`gen_16patch_v3.stdout.txt`: active pins match correction2c, 830622B, sha compared,
  active index empty = no add-N).

Preserved history (not erased, oracles never loosened):

- v8 `run_p2r_correction_v8` 23/25 in 7786.576s with 2 test-mechanics failures
  (`.stderr.txt` tails: `test_fault_primary_read_close_secondary_preserved` got `CLOSE_FAILED`
  at first read because global close-mock armed too early; `test_verifier_late_retained_additions_refuse`
  counted own mid-call plant as verifier output). Fixed (arm at proposal-leaf open;
  plant removed before strict compare), affected-proven 2/2, full-green v9 same codes.
- Proof v3b/v4/v5 exit 40 root-caused (E2 rewrite `freeze(COPYREPO)` read 16 paths AFTER
  unlink loop deleted 13 NEW; `FileNotFoundError` from generic handler, never unlink path’s
  own message) with v6 `strace -f -e trace=%file` decisive (`proof_apply16_v6.strace.log`);
  ghost sparse/timer/stray-process/cp-loop/symlink investigation hereby retracted
  (`proof_apply16_v7.py.READY:1-19`); anomaly record + probe scratch dirs stand as history.
- v5 interruption, v6 runner buffering/overclaim notes preserved; v8/v9 use `-u` direct redirect.
- Accidentally deleted/restored UNEXECUTED `proof_apply16_v3.py.DRAFT` (transcript-restored,
  parses, NOT byte-certified; READY files operative; DRAFT reference-only).
- Mechanical file versioning for v9/proof-READY2 via python file-write instead of specialized
  Write tool (functionally verified by AST+grep+execution; disclosed).

## 7. Mandatory root errata (documentation, not source blocker)

- **E-1 (required):** `correction2-final-report.md:18-19` states test file “1802 lines”.
  Actual final `4155baab` file is **1818 lines** (`wc -l`; ends with `if __name__` at `:1817-1818`).
  Bytes/mode/hash/methods remain correct (93733B, `0o664`, 25 methods). The “1802” value
  matches the intermediate `36814fe5` pins in `ready2-notes.md:40-41` and was carried over.
  Root must errata the final line count to 1818. No source/test change required for this item.
- No other source-blocking documentation overclaim found in the sampled guards.
  Report claims of “scripts executed each once / never edited after execution / never re-executed”,
  “no duplicate processes”, and “secrets audit (5 forced keys, grep-verified)” are cited as
  author evidence with bounded scope (stage/meta/launch/patch/proof files listed above);
  this review does not independently re-observe processes or re-grep secrets.

## 8. Remaining limitations (explicit, no expansion)

- Snapshot equality is not continuous no-drift/global-CAS/crash-atomicity; claim/open races
  bounded, not excluded. `fsync` checked but no replica/power-loss/multi-file durability claim.
- Synthetic accepted-chain Longform/Weekly + real R1×2 fixtures are mechanical oracles,
  not genuine approvals, publication acceptance, or current-eligibility proof.
- `capture_inputs` are historical observations; same-byte identity continuity without a baseline
  is beyond a fresh standalone verifier (capture-time oracles prove it instead).
- Full-suite `-O`, all-profile publication, Windows/Actions, net savings, canonical audit,
  full promotion/reason/State adoption remain open per standing scope. DM021 OPEN,
  Whole NOT_READY, step4/B3 OPEN, audit unstarted.
- This verdict covers only the 3A component (`survey_editorial_retention_v2.py` +
  `editorial-retention-manifest-v2.schema.json` + `test_survey_editorial_retention_v2.py`)
  on actual409 + P1-13 unchanged, with the evidence listed above. No P1 edit, no contract edit,
  no branch/commit/push, no production/network/intake/adoption, no CLI/config/Gate/receipt/publisher change.

## 9. Verdict

**BOUNDED_PASS (limited component)** — final 3A implementation + focused evidence close the
R2 S1/S2/S3 + E1/E2 gaps within their selected scope:

- Final pins: module `3833b14a…` / test `4155baab…` / schema `347e5499…` (P1-13 unchanged),
  HEAD `409b292…`, tree `8ce36998…`, Python 3.14.4.
- `Ran 25 tests in 7936.817s OK` (v9, exit 0) + `Ran 2 tests in 440.248s OK` (affected) +
  `Ran 1 test in 250.016s OK` (optimized smoke) + `APPLY_PROOF_OK` (proof v7, exit 0,
  complete16 patch `5b79218e…` 830622B).
- Concrete S1 final-inventory + post-verify byte binding, S2 fail-closed ownership/close
  preservation, and S3 label/provisional/historical-fingerprint precision are present in code
  and exercised by real typed-hop/late-write/fault oracles with mutations-before-repair and
  exact final-source/test-guard + proof all-entry/static-pin/exact-status/no-overwrite behavior
  as cited above.

Subject to mandatory root errata E-1 and the preserved limitations in §6/§8. No source rework
required by this review. No full adoption, canonical audit, or global-CAS claim inferred.
Stop at Human Commit Point; ordinary reconstruct Commit/Push remains Human-owned.

Report path: `notes/rephase-1-dm021-p2r/evidence-20261014T000000Z-correction2/independent-final-resolution.md`

## 10. Scoped qualification after `astra-closeout-resolution.md` (appended, §§1–9 preserved)

2026-10-14. Focused documentary scope check only on root
`evidence-20261014T000000Z-correction2/astra-closeout-resolution.md`; no source/test/rerun.
Prior sections stand with these exact narrowed limits:

- **Late-plant oracle scope:** `test_verifier_late_retained_additions_refuse:885–907` captures
  immediate `post` but does not compare it; it removes the injected path before `_assert_no_write`.
  My §3/§5 blanket “mutations-before-repair / immediate post equality” wording is therefore too broad
  for this one oracle. What this case proves is late final-inventory refusal plus equality after
  injected-path removal; a verifier change confined to the injected path could be masked here.
  The component still stands because the read-only verifier implementation plus the other immediate
  mutated-pre/post oracles (bind-matrix, staged/canonical, typed-hop, X/persistence, fault,
  replacement, drift, readback, inplace) support the no-write property. Do not extend this
  particular oracle beyond its proven scope.
- **Proof logging scope:** proof v7 `_emit:306–327` can suppress stdout flush/close errors and
  return the prior code; it is not a generally certified transactional logger. Actual complete
  readable v7 raw/JSON/hash/application outputs support this successful run
  (exit 0, empty stderr, `APPLY_PROOF_OK`); no generic logging-failure-path certification follows.
- **Erratum adopted:** final test `4155baab` line count is 1818 (E-1); root closeout §2.1 so records.
- **Attribution:** worker-report “root-caused” means diagnosed root cause in worker proof work,
  not Astra execution attribution (root closeout §3).

With these two qualifications, the §9 **BOUNDED_PASS (limited component)** stands within its exact
limits. No new blocker, no source change, no further check required.
