# Independent implementation review — DM021-P2R (fresh, author-independent)

2026-10-13/14 JST. Fresh author-independent reviewer: not the implementing General,
not root. Read-only review of actual new code, actual test oracles and saved raw
evidence. No tests/scripts rerun, no imports, no source/DB/index/refs/network
writes, no cleanup, no source fixes (per review task). No subagents. Only this NEW
review file is written, in the existing evidence directory.

## Scope read

- Task/selection: `notes/rephase-1-dm021-p2r/task.md`,
  `astra-implementation-selection.md` (overrides C4/C7), `interface-correction.md`
  (C1–C8, overridden where selection differs).
- Fixed contract: `outputs/rephase-1-dm021-retention-contract-decision.md`
  (SHA256 `194fd7de…`); mandatory design resolution
  `notes/rephase-1-dm021-promotion/astra-review-resolution.md` (I1–I4).
- Implementation source (read-only):
  `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`,
  new files `scripts/survey_editorial_retention_v2.py` (`fd22732a…`, 74707 B),
  `schemas/editorial-retention-manifest-v2.schema.json` (`347e5499…`, 5618 B),
  `tests/test_survey_editorial_retention_v2.py` (`4143190e…`, 33940 B).
  Full module (1284 lines) and full test (636 lines) read end-to-end.
- Evidence: `evidence-20261013T123807Z-impl/` — `implementation-report.md`,
  `run_p2r_v{1,2,3,4,5}.sh/.stdout/.stderr/.exit` (v5 `.exit` absent),
  `run_opt_v1.*`, `gen_16patch_v1.*`, `complete-p2r-16path.patch/.sha256`
  (`78efaa11…`), `proof_apply16_v1.*`, `proof-freeze-clean/applied.json`,
  `make_candidate_v1.*`.

## What verifies correctly by read (pass, no rerun)

- **Budget/scope**: exactly 3A added; P1 unchanged (inherited13 hashes in
  `proof-freeze-applied.json` match the P1 freeze pins on spot check, e.g.
  `fe4a96f4…`, `e8598239…`, `e7305884…`; reviewer did not rehash — hashes cited
  from saved evidence, not independently recomputed).
- **No verifier authority**: module imports are `json/os/stat/pathlib/typing` +
  `core` + `schema_gate` only (module `:25-32`); no `subprocess`, no top-level P1
  import. P1 is lazy-imported inside `capture_retention` only (module `:528`).
  `verify_retention` (module `:1046-1284`) contains no P1 call, no Git/HEAD/config
  authority read. Test proves it by mocking `p1mod.validate_proposal` and
  `subprocess.run` to raise during verify (test `:509-512`, PASS in raw).
- **P1-before-writes-only**: capture pins narrow inputs (`:535-594`), refuses on
  existing retained root before any P1 call (`:579-584`), calls unmodified P1 once
  (`:597-602`, wrapped as `P1_REFUSED` with `cause`), compares every P1
  `input_hashes` entry immediately (`:613-619`), snapshots before any write
  (`:621-648`), claims/writes only after (`:717+`). No post-write P1 call; the
  post-close check is P2R self-`verify_retention` (`:1019`), not P1 readback.
- **I1 chain**: verifier enforces unique `state:authority` COPY row equal to
  `basis.state_ref` → retained-State bytes → exact `State.profile{path,sha256}` →
  unique matching KEEP row → verified Profile bytes → source_root/proposal_id →
  canonical proposal/retained/manifest paths (module `:1132-1194`). `basis.state_ref`
  is exact `{path,sha256}`, no `byte_count` (schema `:139-147`); `proposal_id`
  from proposal, `source_root` from retained Profile — not basename/current-State.
- **KEEP row shape per selection override**: schema forbids `retained_dest` /
  `retained_sha256` / `retained_byte_count` on KEEP and the reverse on COPY
  (schema `:119-128`); module enforces both directions (`:667-688` capture,
  `:1110-1127` verify); test asserts absence on KEEP / presence-measured on COPY
  (test `:175-183`). Selection's rejection of C4's "measured pair on both" is
  correctly implemented.
- **X-Profile distinction**: verifier uses State.profile exact match and rechecks
  EVERY KEEP row, so any required KEEP drift (including X rows) fails
  (module `:1206-1216` + comment). Test proves distinct-X presence tolerated with
  exact pins, required KEEP Profile drift fails, and any other KEEP drift fails
  (test `:392-439`). Matches selection (C7's "X drift tolerated" correctly NOT
  implemented as drift tolerance).
- **Ordering/canonical/history scope**: exact ordered plan projection, sorted-unique
  roles, sorted-unique `capture_inputs`, lexical paths, duplicate-key rejection
  (`_loads_strict`), canonical `json_bytes` projector used only for comparison
  (module `:116-150`, `:334-385`, `:1094-1131`, `:1223-1259`). Verifier never reads
  live mutable COPY originals (required row paths need only be *present* in
  `capture_inputs`, bytes bound against retained/KEEP/staged/proposal —
  module `:1238-1257`). Historical-observation scope (not complete-history
  attestation) is stated in code comments and report; no approval/eligibility
  inferred.
- **Ownership mechanics by read**: dirfd-relative exclusive claim (`os.mkdir` +
  `O_EXCL` opens bound to pinned parent fds), no-follow/nonblock opens with
  pre-open `lstat` type refusal, per-write `_check_root_live` entry+fd identity
  comparison (module `:717-770`, `:813-870`), manifest-last exclusive-create +
  fsync + readback + standalone re-verify (module `:919-1027`), closed retained
  inventory with exact expected-set equality (module `:474-517`, `:1195-1205`),
  no cleanup/overwrite/retry (existing root refuses at `:579-584` and `:724-726`).
- **Fixtures**: local override commits all3 P2R files BEFORE authority
  (test `:59-95` — tracked copy + `UNTRACKED_SOURCES` + `P2R_EXTRA`, then commit,
  then helpers build authority). No P1 test file change. Longform prose primary,
  Weekly envelope, real R1×2 predecessor commits with supersedes depth
  (test `:140-193`, `:194-215`, `:216-284`). Destructive faults use distinct
  proposal ids; refusals prove no-write via snapshots.
- **Patch/proof**: complete 16-path patch `78efaa11…` (721326 B); apply proof
  `APPLY_PROOF_OK head=409b292… files=16`, exit 0; applied freeze shows all16
  bytes/modes with new3 prefixes `fd22732a/347e5499/4143190e`; candidate shows
  expected `3M13A` (P1's `3M10A` + 3 new); byte-copy with no hardlinks, inode
  separation, inert `example.invalid` origin, no alternates, no active add-N
  (`make_candidate_v1.stdout.txt :20-21,:54-56,:80-106`). First proof-attempt
  refusal (redirect collision) and rerun under versioned names are disclosed.
- **Failure history honest**: v1 (`os.stat_result.is_symlink` AttributeError),
  v2 (fixture missing `.github/workflows` → `TREE_MISSING`), v3 (parent-fd
  lifetime → `EBADF ROOT_IDENTITY_CHANGED`), v4 (R1 re-verify expectation +
  manifest-filename oracle + unwrapped schema `ValueError`) are all preserved in
  raw stderr with fixes disclosed in `implementation-report.md §4`. No
  overwriting of executed versions/failed outputs observed.

## Blockers — CHANGES_REQUIRED

**B1. Claimed root/ancestor replacement oracle does not exist.**
`implementation-report.md §3 item 9` claims `test_fault_write_close_readback_identity_fifo`
covers "root identity replacement (fd-identity mismatch, no foreign writes)", and the
test carries the comment "Root replacement after success: no foreign writes, verify
detects" (test `:562`). The method body (test `:515-590`) performs: short-write-loop
(mock), zero-progress-write refusal, close-failure refusal, a plain second capture
(`pp_rep`), and a FIFO-as-proposal-path probe. There is **no** rename/symlink-swap/
entry-replacement injection against the claimed retained root or any ancestor, no
`ROOT_IDENTITY_CHANGED`/`ANCESTOR_REPLACED` assertion anywhere in the file (the full
636-line test was read; those codes never appear in oracles), and no fd-identity
mismatch is ever triggered deliberately. Contract §7 explicitly requires injecting
root identity replacement. The implementation's `_check_root_live`
(module `:754-770`) is therefore unproven by any designed oracle (v3's accidental
`EBADF` trip during a lifetime bug is not a replacement-injection proof). Required:
add a genuine entry-replacement injection oracle (e.g. swap the claimed retained-root
entry or a pinned ancestor entry mid-invocation via fault hook, assert the exact
`ROOT_IDENTITY_CHANGED` refusal, partial preservation, retry refusal and no foreign
writes), or remove the claim — but removal still leaves the explicit contract oracle
unsatisfied, so the oracle must be added. Report §3 item 9 wording must be corrected
to match what actually ran.

**B2. Missing typed-hop and row-shape negative oracles required by I1/§7.**
No test constructs: missing `state:authority` row, duplicate `state:authority` rows,
`basis.state_ref` disagreeing with the COPY row, State-profile ref pointing at a
non-matching/absent KEEP row, ambiguous dual KEEP match, omitted/extra/duplicate
manifest rows, or duplicate retention paths. The keep/X test only asserts the
positive-path uniqueness (`len(state_rows)==1`, `len(keep)==1` on valid manifests —
test `:411-416`); the order test reverses rows but keeps count identical
(test `:350-352`). The verifier code paths exist (module `:1097-1131`,
`:1137-1163`) but have no failure oracles. Required: add compact negatives for at
least missing/duplicate/disagreeing `state:authority`, ambiguous KEEP match, and
omitted/extra/duplicate rows, asserting exact refusal codes.

**B3. Manifest-publish close-fail disposition deviates from mandatory C5 and the
oracle masks it.** C5 (via `interface-correction.md`, retained by selection except
as overridden) requires a close-failed manifest publish to report
`INDETERMINATE_INVOCATION`. The module raises `MANIFEST_CLOSE_FAILED` with
`OWNED_PARTIAL` for manifest write/fsync/close failures (module `:986-1002`);
only the final directory-close path uses `INDETERMINATE_INVOCATION` (`:1016`). The
test oracle accepts `CLOSE_FAILED|MANIFEST_CLOSE_FAILED|INDETERMINATE`
(test `:560`), so it passes under either disposition and does not pin the required
one. No false success results (failure is raised either way; partials preserved;
retry refuses), so this is label-precision, but it is a deviation from a mandatory
correction item. Required: either emit `INDETERMINATE_INVOCATION` for manifest-publish
close failures per C5, or obtain an explicit Astra variance; and tighten the oracle
to assert the exact required code/disposition instead of the three-way alternation.

## Qualifications (accepted as bounded limits, not rerun triggers)

- **Q1 — v5 wrapper exit absent; -O evidence is single-method.** `run_p2r_v5.sh`
  runs the full 10-method suite then a redundant `-O` rerun; the wrapper was killed
  at 3600 s during the trailing `-O` (`run_p2r_v5.stdout.txt :224-225` shows
  `unittest_rc=0` then `=== -O smoke ===` with no further lines; no `.exit` file).
  The 10/10 PASS (`Ran 10 tests in 3365.846s OK`, `unittest_rc=0` durably in both
  stdout and stderr) stands, and `-O` on final code is proven only for the single
  weekly positive (`run_opt_v1`: `OK in 256.278s`, `optimized_rc=0`, exit 0).
  Full-suite `-O` was not run. `-O` safety for the new files holds by read
  (explicit raises only; no `assert`-statement guards observed in the new module or
  test — test uses `self.assert*` methods and `raise AssertionError`, which survive
  `-O`), but full-suite `-O` remains unproved. No rerun demanded now (would cost
  ~1 h); any post-correction rerun should include full-suite `-O` if cheap, else
  repeat the single-method `-O` on changed code.
- **Q2 — Control-snapshot strictness gaps.** Absent control-list files are silently
  skipped (module `:623-634`, comment at `:629` relies on P1 having validated
  authority); final recheck covers P1 `input_hashes` + edition trees + P2R deps
  (module `:879-922`) but not every control file outside P1's input set; intermediate
  ancestor dir fds opened in `safe_read` are closed quietly, swallowing close errors
  (module `:297-300`), while only file-read closes and final `_close_all` propagate
  them; `dir_ids`/`file_ids` are recorded (module `:178`,`:233`,`:290`) but never
  compared — dead bookkeeping. Ancestor replacement above the retained root's parent
  is prevented from causing foreign writes (all writes are fd-bound) but is not
  explicitly detected. Fail-closed outcome is preserved by readback + exact-inventory
  backstops; these are defense-in-depth gaps, to be hardened or explicitly accepted
  by root.
- **Q3 — Corruption oracles mutate the retained manifest in place.** Reordered/
  extra-field/dup-input/noncanonical cases overwrite the captured manifest file then
  restore `good_bytes` and re-verify (test `:339-385`). Restoration + re-verify is
  asserted, and snapshots are not taken around these verifier-only mutations; acceptable
  bounded practice, but the technique (mutating retained bytes outside the writer)
  must not be cited as a writer-fault proof.
- **Q4 — Dead code.** `verify_retention` contains a no-op loop over header keys whose
  `schema_version` branch is `pass` (module `:1078-1080`, "checked separately below"
  but no such check follows). Harmless (schema `const` checks both files' versions),
  but it should be deleted to avoid review noise.
- **Q5 — Reviewer did not re-execute or rehash.** All hashes, counts, timings and
  pass/fail states are cited from saved evidence files, spot-read for consistency
  (e.g. v1/v4 raw failures match the report's §4 attributions; v5 stdout `pre` status
  `3M13A` matches the expected delta). No independent byte/mode re-verification was
  performed (execution forbidden by the review task). The saved apply proof and
  freezes are the binding evidence, not this review.

## Explicit non-certifications

- Runner/proof scripts are exact-run evidence, not certified generic rerun tools.
- Snapshot equality at checked boundaries is not continuous no-drift, crash-atomicity,
  replica-durability or global-CAS proof (contract §5; implementation claims none).
- Synthetic accepted-chain fixtures and type/identity oracles are not genuine
  semantic/visual/Human publication approvals or current-eligibility proof; `CAPTURED`/
  `VERIFIED` attest only this invocation's checks / currently observed bound bytes.
- `capture_inputs` are historical observations bound to this capture's P1 return, not
  complete-history attestation.

## Verdict

**CHANGES_REQUIRED** — narrowly scoped to B1 (replacement-injection oracle + report
correction), B2 (typed-hop/row-shape negatives), B3 (manifest-publish close
disposition + exact oracle). No design rework, no scope expansion, no P1 change.
After correction: bump test/runner to NEW versioned names, preserve all raw (including
v1–v5), rerun at minimum the changed methods plus both positive captures and the
no-P1/Git verifier case (full 10-method rerun preferred; retain the single-method
`-O` at minimum), refresh the saved patch + apply proof if bytes change, and return
for root's author-side binding/oracle review. Whole NOT_READY, step4/B3 OPEN,
canonical audit unstarted, DM021 OPEN remain unchanged.
