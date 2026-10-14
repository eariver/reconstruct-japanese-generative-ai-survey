# Independent correction resolution — DM021-P2R (B1–B3 + R1–R6)

2026-10-14. Fresh author-independent reviewer (not implementing General, not root).
Resumes the initial independent review (preserved intact at
`evidence-20261013T123807Z-impl/independent-implementation-review.md`;
B1–B3 blockers). Read ALL of root `notes/rephase-1-dm021-p2r/astra-review-r1.md`
(R1–R6), the correction packet
`evidence-20261013T173500Z-correction/correction-report.md`, the resumption record
`notes/rephase-1-dm021-p2r/resume-after-interruption.md`, the full final module
(1842 lines) and full final test (1305 lines), v6/opt/proof/gen raw, pins and
pre/post guards. Read-only rehash of the new3 plus sanitized Git observations
(allowed scope; no imports, executions, test/script reruns, or DB writes). No
subagents. This NEW file is the only write. Initial review is not edited.

## Independently rehashed / observed (this review, read-only)

- `scripts/survey_editorial_retention_v2.py`:
  `77ee2a3e690c23f64b7dfa4c6c5ef0ec55920644c34a247f8e4e3fc469a0e964`,
  mode 664, 1842 lines — matches correction-report §2.
- `schemas/editorial-retention-manifest-v2.schema.json`:
  `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c`
  (unchanged from initial) — matches.
- `tests/test_survey_editorial_retention_v2.py`:
  `22f5604165f837ae631feabb26859cdc2e2e443e3e6dc4875ec85071bd94e741`,
  mode 664, 1305 lines — matches.
- Candidate live Git (sanitized `GIT_*`, forced
  `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`):
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree
  `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status `3M13A` (P1 `3M10A` + 3 new),
  origin `https://example.invalid/rephase-candidate-recovery.git` (inert, fetch+push).
- All other hashes/counts/timings below are cited from persisted evidence files,
  not re-measured. No raw-hash claim is made except the rehashes above.

## Resolution per finding (actual-source basis, file:line in final code)

**B1 — replacement oracles: RESOLVED.** Genuine injections now exist, replacing the
old comment-only claim:
- Retained-root entry swap mid-write (`os.rename` of the claimed root + planted
  foreign file) → exact `ROOT_IDENTITY_CHANGED|ANCESTOR_REPLACED`, live-original
  stability, retry `RETAINED_ROOT_EXISTS` (test `:1008-1057`).
- Proposal-ancestor dir swap mid-write → refusal at a real boundary
  (test `:1059-1093`; regex is a 4-way alternation — see Q2).
- Owned COPY file same-byte inode swap at manifest-open → exact `FILE_REPLACED`
  with `OWNED_PARTIAL` asserted on the exception object, partial preserved, retry
  refuses, owned-prefix-only delta (test `:1127-1193`); implementation compares
  post-write entry dev/ino against creation identity (module `:1245-1254`), closing
  the exact R4 gap the report discloses.

**B2 — typed-hop/row negatives: RESOLVED.** Coordinated untrusted-artifact fixtures
with proposal_ref rebinding reach the typed checks: missing/duplicate
`state:authority`, disagreeing `state_ref`, ambiguous dual KEEP, omitted/extra
manifest rows (test `:437-523`), each with restore + re-verify success. Exact-code
families asserted (`MISSING/AMBIGUOUS_STATE_AUTHORITY`, `STATE_REF_MISMATCH`,
`AMBIGUOUS_PROFILE_MATCH`, `RETENTION_MISMATCH`).

**B3 — manifest close disposition: RESOLVED.** Manifest write/zero/fsync/close use
distinct `MANIFEST_WRITE_FAILED / MANIFEST_ZERO_PROGRESS / MANIFEST_FSYNC_FAILED /
MANIFEST_CLOSE_FAILED`, all `INDETERMINATE_INVOCATION` (module `:1419-1442`), with
exact-code oracles plus disposition asserted (`INDETERMINATE_INVOCATION`,
test `:866-944`); COPY-side codes stay distinct (`WRITE_ZERO_PROGRESS`,
`FSYNC_FAILED`, module `:1213-1221`). Old masking alternation is gone for these paths.

**R1 — raw paths: RESOLVED.** Raw `/`-split segments, no `Path.parts`, no
`resolve()` before NOFOLLOW checks (module `:90-145`); lstat-first symlink root
refusal + entry-vs-fd root binding (`:189-233`); per-ancestor entry-vs-fd match +
pinned `dir_ids` comparison (`:314-350`); file entry-vs-fd + pinned identity
(`:395-402`); checked intermediate closes (`:427-436`); filename checks on raw
segments (`:845`, `:1536`, `:1542`); all snapshot bases lexically checked
(`:633`); lexical walk without resolve + fail-closed `onerror` + per-entry lstat
modes (`:642-712`, `:730-773`); strict duplicate-key JSON at State/Profile and
retained-State/Profile hops (`:819`, `:838`, `:1645`, `:1664`). Oracles: lexical
dot/`//`/trailing/absolute forms, same-byte contained leaf alias, FIFO with
explicit skip-on-creation-failure (test `:361-433`).

**R2 — verifier exactness: RESOLVED.** Exact directory closure vs recomputed
ancestor sets (`:1716-1731`) over a fresh re-inventory (`:1707`); COPY dest
recomputed independently on both sides (`:989-993`, `:1697-1704`); staged refs
pinned to exact canonical names + canonical-digest consistency (`:1743-1767`);
EVERY KEEP row rehashed with size (`repinned(..., expected_size)`, `:1740-1742`,
`:1024-1026`); `capture_inputs` requires every plan path with the row hash
(`CAPTURE_INPUT_MISMATCH`, `:1795-1802`), staged+proposal presence/hash
(`:1803-1814`), mandatory P2R deps present and byte-bound (`MISSING_P2R_DEP` /
`P2R_DEP_DRIFT`, `:1788-1794`); sorted-unique plan paths both sides
(`:953-957`, `:1580-1585`); nested refs rebuilt in fixed order by the projector
(`:487-545`); dead header loop removed (confirmed absent); retained-State/Profile
label agreement enforced (State labels conditional on presence, Profile strict —
`:1669-1679`, see Q6). Oracles: wrong COPY hash, missing P2R dep, moved dest to
absent path (exact `PATH_MISSING`) AND moved dest with planted same bytes (exact
`RETENTION_DEST_MISMATCH` before reading the moved path), byte_count, extra empty
dir (test `:525-633`); order/canonical/shape matrix (test `:635-690`).

**R3 — capture snapshot: RESOLVED.** HEAD pinned before anything and rechecked
pre-P1, post-P1, pre-final, pre-manifest and post-verify (`:814`, `:890`, `:918`,
`:1273`, `:1395`, `:1475-1478`); P1 runs under a sanitized-Git context manager
(`:581-600`, `:895`); verifier contains no Git/HEAD path (read-verified: only
capture calls `_git_head`); missing/alias/irregular control entries refuse
(`CONTROL_MISSING/CONTROL_ALIAS/CONTROL_NOT_REGULAR`, `:925-942`); control
file+dir maps recomputed with exact equality (`:1283-1308`); edition finalization
uses exact expected sets (snapshot ∪ owned, no `startswith` exemption —
`:1309-1341`); post-verify session rechecks live inputs + HEAD + reverify before
success (`:1464-1491`). Seams oracled: control-file injection, empty edition dir,
HEAD move via real mid-capture commit, pre-final KEEP drift (test `:1197-1301`).

**R4 — ownership/close: RESOLVED.** Full ancestor-chain lstat pins + per-write
`_verify_ancestors` (`:1033-1057`, wired into `_check_root_live` `:1100-1117`);
owned-subdir entry/fd match (`:1162-1172`); owned files carry dev/ino/status from
creation (`:1196-1202`) plus post-write entry check (`:1245-1254`);
`owned_dirs` tracked (`:1149`); primary failures preserved with secondaries
attached at both fault sites (`:1226-1243`, `:1430-1445`) and `_close_all`
aggregates secondary closes (`:245-274`); post-claim errors without ownership get
it attached (`:1497-1502`); combined write+close oracle asserts the primary code
survives (test `:946-1004`); manifest-fault mocks target only the manifest fd,
not global close (test `:885-944`), answering the old global-mock criticism.

**R5 — oracle precision: RESOLVED with noted limits (Q2–Q6).** X test honestly
labels the second row generic KEEP (no synthetic X authority) and asserts distinct
identity positively (test `:716-723`); live-State replacement mutates the resolved
canonical State and still verifies, while retained/staged/cross-proposal drift
refuse (test `:748-795`); no-P1/Git proven by raise-mocks (test `:814-817`);
verifier-corruption cases in the bind matrix compare pre/post inventories before
repair (test `:545-556`); fault cases assert owned-prefix deltas, live stability,
partials and retry refusal. Limits: typed-hop/staged matrices restore without a
pre/post diff (Q3); ancestor regex breadth (Q2); nested-ref reorder without a
dedicated oracle (Q4); missing-file/mode-change seams without oracles (Q5).

**R6 — guards/proof: RESOLVED with noted limits (Q1, Q8–Q9).** v6 runner:
preselected expected16, pre HEAD/tree/status/index/caches with rc, exclusive
streamed child files, `child_rc=0`, `timed_out=false`, finally-post identical to
pre (HEAD/tree/status/index/all16 pins), wrapper exit 0
(`run_p2r_correction_v6.{pre,post,state.json,exit}`, stderr `Ran 19 tests in
6391.813s OK`). No trailing `-O` inside the long run; cheap single-method `-O`
separately `OK in 251.675s`, exit 0. v4 failed suite (17/18, moved-dest
`PATH_MISSING` outside old regex) preserved and explained; v5 (meta+pre only)
explicitly unproven — not a result. Hardened v2 proof: whole-`.git` regular-entry
comparison (134/134, `odd=[]`), shared-inode refusal, alternates check, exact
inert remote/config with checked rc, pre-removal cache log, output-existence
refusal, clean409 revert confined to the disposable copy, `apply --check` +
`apply` rc 0, all16 bytes/modes equal active, `APPLY_PROOF_OK`, exit 0, empty
stderr (`proof_apply16_v2.{py,stdout,stderr,exit}`). Patch v2
`f42af778da95e025fb09d21fc0aca1ed19e6ff62b2256d613c70cc5df69555d7`
(787863 B) matches `.sha256` and generator stdout. Initial3/v1–v5 artifacts
intact; pycache residue and buffering limitation disclosed in the report.

**Report-overclaim check (no silence accepted).** Correction-report claims
verified against raw: v6 `19 tests / 6391.813s / child_rc=0` ✓ (stderr+state.json);
opt `251.675s` ✓; patch bytes/sha ✓; v4 17/18 with stated cause ✓ (stderr);
v5 meta+pre-only ✓ (directory listing); `+4 lines 1838→1842` consistent with the
read `FILE_REPLACED` block; coverage matrix rows all map to read methods,
including the honestly rescoped ancestor/file row. One stale comment found: test
`:409-411` announces a "contained ancestor alias" injection that the method does
not perform (it proceeds to the FIFO probe); the real ancestor injection lives in
`test_replacement_ancestor_and_file`. Cosmetic only — see Q7. No other overclaim
found; failures, limits and residue are disclosed, not laundered.

**Worker-continuity note.** Interruption → resumption chain is documented
(`resume-after-interruption.md`: no running process found/killed; v4 failed not
passed; v5 unproven; moved-dest must be proven with planted bytes — done, test
`:583-617`) and the correction report preserves pre-edit pins/snapshot
(`initial3-*`, `expected16-pinned-v5.json`, resume snapshot path). No author
independence conflict for this review: the implementer/test-runner is General,
root reviewed, and this reviewer executed nothing and changed no source.

## Verdict

**BOUNDED_PASS** — correction resolves initial B1–B3 and root R1–R6 as
implemented, oracled (19/19 PASS in `run_p2r_correction_v6`, exit 0, pre/post
guards identical) and proven for patch application (hardened v2 proof, exit 0).
P1/source13 untouched (inherited13 all match; rehashed new3 match report).
Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN — unchanged.
No adoption, reason/State promotion, global-CAS/durability, or canonical-audit
claim is made or inferred.

## Required qualifications (carried, not rerun triggers)

- **Q1.** Full-suite `-O` unproved (single weekly-positive `-O` only). New
  module/test use explicit raises (read-verified; test uses `TestCase` methods +
  `raise AssertionError`, no `assert`-statement guards), so `-O` safety holds by
  construction for the changed files; full-suite `-O` remains open.
- **Q2.** Ancestor-swap oracle asserts a 4-way refusal alternation
  (`ROOT_IDENTITY_CHANGED|ANCESTOR_REPLACED|PATH_MISSING|PATH_UNREADABLE`); the
  exact trip point is unpinned (root-swap is a tighter 2-way). Any member is a
  real fail-closed boundary for that mechanism.
- **Q3.** `test_verifier_typed_hop_negatives._check_both` and
  `test_verifier_staged_canonical_order._corrupt` restore without a pre/post
  inventory diff (the bind matrix `_corrupt` does diff). Verifier is write-free
  by construction (read-verified: no `O_CREAT`/`O_WRONLY` path in
  `verify_retention`), so this is evidence-completeness, not a safety hole.
- **Q4.** No dedicated nested-ref-key-reorder oracle; top-level reorder refusal is
  proven and nested refs pass through the same canonical comparison.
- **Q5.** Deleted-control-file and mode/identity-change seams lack dedicated
  injection oracles (new-file/empty-dir/HEAD-move/KEEP-drift proven; the final
  equality comparisons are shared code paths).
- **Q6.** Retained-State research/publication labels are checked only when present
  (module `:1673`); KEEP Profile labels are strict. Narrow, documented tolerance.
- **Q7.** Stale comment at test `:409-411` (ancestor-alias injection announced but
  not performed in that method). Recommend comment cleanup; no pin impact, no
  rerun needed for the comment alone — correct it with the next touched version.
- **Q8.** This reviewer rehashed only the new3 + Git observations above; all other
  pins/counts are cited from persisted evidence (spot-read, not re-measured).
- **Q9.** v5 remains explicitly unproven; v4 remains a failed suite (17/18); the
  initial 10-suite result is superseded, not transferred — v6's fresh 19 on final
  code is the binding result.
- **Q10.** Non-certifications preserved: runner/proof scripts are exact-run
  evidence, not generic rerun tools; snapshot equality is not continuous
  no-drift/crash-atomicity/replica-durability/global-CAS proof; synthetic
  accepted-chain fixtures are not semantic/visual/Human approvals, publication
  acceptance, or current-eligibility proof; `CAPTURED`/`VERIFIED` attest only this
  invocation's checks / currently observed bound bytes; `capture_inputs` are
  historical observations, not complete-history attestation.
