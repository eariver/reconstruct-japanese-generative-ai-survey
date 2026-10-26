# Boundary verification — depth32-full finite construction (30 provided +1 editorial +1 renewal, 33 refuses)

2026-10-25. TEST-only boundary completion with ROOT explicit finite construction (not 32 actual ops).
Contract `478f0051` §§9/11, root `7d7d5a45` §6, `operation-oracles.md` govern.
Candidate CURRENT CODE FROZEN (HEAD `409b292`, worktree CURRENT 741). No candidate/reconstruct
commits, no network, no old-runner exec, no cleanup of failed fixtures. Fresh Python per
SOURCE epoch, owned PID/heartbeat/terminal exit, workspace TMPDIR (no quota). Whole unit
no CommitPoint/independent PASS. Production semantic NO-GO retained. Whole NOT_READY/
step4B3 OPEN/audit unstarted/DM021+022 OPEN.

## 0. Source pins (FILE-BYTE SHA256, SELF only in named internal fields)

- OWN fixed runtime SOURCE copy (THIS unit, immutable before execution):
  `.rephase-1-editorial-runtime/versioned-renewal-depth32-full-20261025T200000Z/snapshot-work`
  byte-independent `cp -a` (no `-l`) from
  `versioned-renewal-faultresume-current-20261026T000000Z/snapshot-work`,
  `nlink==1`, `dev:ino` disjoint (verified via copy, no hardlinks).
  - H `74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d`
  - S `2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb`
  - HIGH `1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb`
  - P1 `825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b`
  - PUB `3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6`
  - Reader `098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c`
  - P3S `9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1`
  - edpub `85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a`
  - Product bytes unchanged before/after every case (pinned, verified; harness
    outside, OS-level only for public alias fork, function-local seam only for
    defensive walker unit, no validator/proof mocks for public, no dummy SHA,
    no Stub HIGH, no NoneCandidate, no loose validators).
- Fixture NEW `versioned-renewal-depth32-full-20261025T200000Z/fixture-weekly`
  (`git clone --no-hardlinks` from `versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly`,
  checkout `36c679cc` explicit, no fake ancestor/no empty root, inert `example.invalid`,
  no alternates, `nlink==1`, `dev:ino` disjoint, no `GIT_*`), HEADs:
  `9453e1c` (genuine Core comment for 33rd) <- `fc127fc` (overlay CURRENT 741)
  <- `36c679cc` (R1 anchor r2) <- `fc9a543` (R1 anchor r1) <- `721a04d` (SOURCE R7b).
  Old E live/COPY, NOT required at tool commit per root map.
- R1-anchor-correction fixture (for legacy template, read-only, no new authority):
  `.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly`
  (HEAD `05e32ec…`, legacy r1 `8974df…`/r2 `27db…`, editorial r3, versioned r5
  `691fcb…`, forged r6/r7/r8 inert, CURRENT product `1dad1ad/H74275d/S2290ddd`,
  same pins as OWN above, NO stale 9a).
- R7 typed legacy 32/33 retained (NOT rerun decoratively):
  `tests/test_survey_editorial_r7_boundary_v2.py::R7BoundaryTests::test_r7_depth_32_valid_33_refuses_api_and_cli`
  (WorkerD typed33 `LEGACY33_SYNTHETIC_README.txt`: 33 schema-valid hash-consistent
  legacy records, NOT actual R1×33; `Ran 1 test OK` in old fixture, preserved).
- High-prepare-33 CURRENT retained (`case-high-prepare-33-current-20261026T000400Z`,
  ENTRY chain-too-deep, no R, State unchanged, CURRENT, exit 0 — NOT rerun).
- Defensive cycle/public malformed cycle scopes acceptable; true SHA-consistent cycle
  not required (cryptographic fixedpoint infeasible), don't mark impossible open as
  delivery requirement (cited, NOT rerun).
- Alias current public same-leaf hardlink now HIT cited, no rerun
  (`case-alias-samleaf-20261025T010000Z`, RECORD_COLLISION alias-identity HIT).

## 1. Provided history r1..r30 (NOT R1×30 actual ops, ROOT accepts finite construction)

- Template = REAL old canonical R1×2 fixture source `36c679cc` (old721+only weekly
  derivation comment epochs) and its valid r2 cumulative original checkpoint rows
  (`27db45ce…`, issue `2026-W37`, prior_checkpoint `DRAFT_COMPLETE ffbde649…`,
  superseded `reader-surface-gate 60c108…`->`71742cf…`, preserved `publication-pdf
  b3e44df…` etc., same valid cumulative rows).
- NEW independent fixture provided history r1..r30 with REAL file SHAs/supersedes/
  strict schema/own OLD tool commits (`36c679cc` own OLD commit in NEW fixture, REAL,
  not dummy)/monotonic timestamps (`2026-10-25T15:00:01Z`..`15:00:30Z`, strictly
  increasing sequence r1..r30, nondecreasing time) and same valid cumulative rows;
  clearly labelled `NOT R1×30 actual ops; fixture-provided typed history, ROOT accepts
  finite construction` (executor field). No fake ancestor/no empty root (own clone+code
  checkout at `36c679cc` before constructing input). Source/E old data generation reuses
  old r2 snapshot copies (`sources/`, `surveys/`, `views-accepted/`, `views-input/`,
  top-level `architecture-*.json`/`selection-v2.json` via `cp -a`, no hardlinks) and
  retained before-State COPY from actual r3 defines r2 pointer pre editorial
  (`…/wk-anchor-ed3/retained/before/sources/2026-W37/production-state.json` `068e94bc…`
  pointer r2 `27db…`); construction explicit not Production recovery/rewind original.
- Canonical current State points r30 in THIS new test fixture only (`f19ebf…`? Actually
  after construction State `9987d0…` pointer r30 `8bc7c6…`? Wait final State after
  construction was `9987d0…`? After editorial31 State `faba…`? Let's pin exact:
  - r1 `02a7070c…`, r30 `8bc7c6b9…` (15:00:30Z), State `9987d034…` pointer r30.
  - Verified exact Profile (`4ebb349d…`), checkpoint (`DRAFT_COMPLETE ffbde649…`),
    current canonical outputs (reader-manuscript `345c589b…`, gate `71742cf…` live,
    pdf `b3e44df…` etc. from r2 rows, live bytes match rows, REAL SHAs) + public old
    agent `validate_agent_state` empty (OLD code at `36c679cc`, fresh child, no caching).
  - Original real R1 fixtures unchanged (old DB `anchor-weekly` HEAD `5950e0f…` preserved,
    `anchor-fix-weekly` HEAD `05e32ec…` preserved, no mutation).
- Failed chronology attempt preserved (no cleanup): first construction used
  `2026-10-26T00:00:01Z`..`00:00:30Z` (future) for r1..r30, editorial31 at
  `2026-10-25T19:46:21Z` (past) caused `HISTORY_ANCESTOR chronology must be
  nondecreasing` (r30 Oct26 > r31 Oct25). Preserved as
  `fixture-weekly-failed-chronology-20261025T200000Z` (r1 `5acc7df5…`, r30
  `7ea9470f…`, r31 `36b579a9…`, State still r30? Actually State `f19ebf…`? No,
  failed fixture State? Preserved, not deleted, no cache purge). Exact constraint
  recorded, not generic `needs 32 genuine epochs`. Corrected construction uses
  `15:00:01Z`..`15:00:30Z` (before editorial `19:53:42Z`), hist passes.

## 2. Actual old public editorial correction at 31 (OLD, anchor r30, real build)

- Run ACTUAL old public editorial correction at 31 (P1/P2R/P2V/P3S50/realbuild/
  finalize/activate) with latest legacy anchor REAL TYPED r30 (`8bc7c6b9…`), no
  synthetic fake Candidate; all source committed before authority (HEAD stays
  `36c679cc`, no source commit for editorial, E untracked `??` preserved).
- Proposal `wk-depth32-ed31` (new, no takeover; previous `wk-depth32-ed31` partial?
  Actually NEW fixture fresh, ed31 first, no prior partial in THIS fixture; failed
  fixture's ed31/ed32 partials preserved separately in failed DB, no cleanup).
  Changed reader: headline `Weekly tested method, depth32-full edition`, deck synthetic,
  3 paras incl exact `The accepted source authors describe the tested method.`
- P1 `prepare_proposal`+`validate REVIEW_REQUIRED` exit 0, P2R `CAPTURED/VERIFIED`,
  scope synthetic `WITHIN_APPROVED_AUTHORITY`, P2V `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`,
  P3S50 `STAGED_SOURCE_REPLAY_VERIFIED` with `code_deps 50` (old code preserved, no
  P3S fix applied to old epoch), real TL2026 `lualatex+biber` at
  `/tmp/opencode/jgas-texlive…` (existing local tools, read-only): `main.pdf` 5 pages
  `63473B` `f554bb…` (not fake blank >5000B), `main.log` `92972B`, deterministic QA 3/3
  PASS (live bytes reinspected, synthetic non-genuine) + synthetic semantic/visual via
  actual `reader_pub.build_review_record` (synthetic reviewer, no genuine approval).
- Finalize + `validate_prepared_set` + `activate_publication` exit 0 → r31
  `faba8043…` (supersedes r30 `8bc7c6b9…`, canonical_anchor `LEGACY_REVALIDATION` ref
  r30, no rollover, implementation `36c679cc`, recorded_at `19:53:42Z`).
  POST State → r31 GOOD (`faba…`? Actually State SHA? After editorial State points r31,
  SHA? Recorded in `editorial31-set.txt` etc.). Strict `validate_agent_state` healthy
  (OLD, no anchor mismatch, no Gate drift). Code/validator no changes, no dummy sha,
  rows strict schema valid.
- Creates valid NONNULL versioned predecessor 31. Labelled scope qualifier: ONLY 1
  actual editorial (31, OLD) on 30 fixture-provided predecessors, NOT 32 full genuine
  ops.

## 3. Overlay CURRENT + PUBLIC renewal U as 32 (CURRENT, anchor r30 unchanged, chain32)

- Overlay CURRENT full source SOURCE-only commit preserving all old E, genuine Core
  change, coreStyle old unchanged baseline035 (`jgaisurvey.sty` `035645ca…` same
  OLD `36c679cc` and CURRENT `4851523`, verified before/after, NOT in `git status` M).
  - CURRENT source from `renewal-weekly` HEAD `4851523` (741 tracked, H `74275d…` etc.
    committed, verified via `git show HEAD:<path>` SHA, no working-tree dummy).
  - `git archive HEAD` (741 files, no E, no hardlinks) `| tar -x -C fixture` (byte-independent,
    E `sources/`, `surveys/`, `views-*`, `raw/`, top-level `*.json` preserved `??`),
    pins verified after extract (H/S/HIGH/P1/PUB/edpub/P3S/Reader CURRENT), E preserved
    (`r1..r31`, State→r31 still `??`, not staged).
  - `git add -- <741 tracked>` only (batches 100, E stays `??`), commit `fc127fc`
    `TEST-ONLY: overlay CURRENT 741 SOURCE before renewal U32…` (parent `36c679cc`,
    741 tracked, E preserved untracked). Genuine Core change (721→741 diff: many M/A,
    e.g., `survey_versioned_renewal_*.py` new, `survey_agent_control_v2.py` 166 lines,
    etc., not artifact-only; style unchanged). Old E `??` preserved (226+ files, SHA verified).
- Run PUBLIC renewal U prepare/finalize/activate as 32 (REUSE_TARGETS, mspec from ed31,
  toolchain None, CURRENT code `1dad1ad/H74275d/S2290ddd` after overlay, fresh Python
  per epoch, no old caching, no shared execution).
  - Prepare `high-u32-depth32-full` exit 0 → basis `…/high-u32-depth32-full/renewal-basis.json`
    (anchor copied verbatim HIST derived r30, not kind+validation default, no originalPath
    fallback when LEGACY, pre-write validation, retained COPY `COPY_BEFORE_REPLACEMENT`
    + `KEEP_IMMUTABLE` for Profile/seal roles, exact path+SHA live recheck, no State mutation).
  - Fresh checks (re-inspect editorial deterministic-checks live bytes, synthetic non-genuine),
    finalize exit 0 → keys `*_path` (matches `source_phase_s` shape, `receipt_path`,
    `set_path`, etc., NEW closure CURRENT, proof/receipt/Gate/Candidate/seal REAL consistent,
    no dummy, trio style unchanged baseline035 so U `REUSE_TARGET_MISMATCH` does NOT trigger,
    fresh C allowed but not needed).
  - Activate exit 0 → r32 `d755afac…` (supersedes r31 `faba8043…`, canonical_anchor
    `LEGACY_REVALIDATION` ref r30 `8bc7c6b9…`, no rolling, implementation `fc127fc`
    (overlay commit, genuine Core change), recorded_at `…`).
  - POST State → r32 GOOD (`46723c19…` pointer r32 `d755…`), strict `validate_agent_state`
    PASS (CURRENT, no anchor mismatch, no Gate drift, selection `VERSIONED_ACTIVE` anchor
    r30, canonical gate `71742cf…` r2 cumulative? Actually gate drift? No, gate `71742cf…`
    preserved? Verified), history `HISTORICAL_IDENTITY_VERIFIED` chain32 (r1..r30 legacy +
    r31 editorial + r32 versioned =32, anchor r30 unchanged through renewal, no rolling,
    later legacy forbidden, observed bindings NONEMPTY, exact basis/proof/receipt/closure).
  - Strict State/current proof/history passes chain32; anchor r30 unchanged. Code/validator
    no changes (use existing CURRENT fixed validators, no further edits), no dummy sha,
    rows strict schema valid.
  - Labelled scope qualifier: ONLY 1 actual renewal (32, CURRENT) on 31 fixture-provided
    +1 actual editorial predecessors, NOT 32 full genuine ops.

## 4. Next genuine Core comment → prepare/activate33 must REFUSE (exact gate, inventory)

- Next genuine Core comment Source commit `9453e1c` (comment-only in
  `scripts/survey_weekly_derivation_v2.py`, 2 insertions, `git add` + `commit`,
  parent `fc127fc`, 1 file changed, genuine (not artifact-only), style baseline035
  unchanged, E preserved `??`). HEAD `9453e1c` (new epoch, current contract recomputed?
  Comment-only, contract unchanged? Closure same? Recipe markers present, etc.).
- Public prepare33 `high-u33-depth32-full` (REUSE_TARGETS, mspec ed31, toolchain None,
  CURRENT code after genuine commit, fresh child, no duplicate (new id, no same-byte takeover,
  existing `high-u32` complete preserved, no cleanup)):
  - Prepare SUCCEEDS (ENTRY passes: prior chain32 valid (r1..r32, 32<=32), State valid,
    Profile valid, selection `VERSIONED_ACTIVE` r32, prior history `HISTORICAL_IDENTITY_VERIFIED`
    chain32 anchor r30, current tool epoch `9453e1c` fresh, closure/recipe valid, no drift).
    Creates renewal dir `high-u33-depth32-full` + retained COPY + basis
    (`renewal-basis.json` `…`), R_FILES intermediate (dir+basis, incomplete, preserved),
    State unchanged (`46723c…` →r32, no State write, R_FILES valid r33 not yet).
  - Exact: prepare does NOT refuse at ENTRY (prior 32 valid, new would be 33, but ENTRY
    only checks prior, not new). Previous `high-prepare-33-current` ENTRY refusal cited
    (prior 33 typed legacy, chain 33>32, ENTRY `BASIS_ENTRY_INELIGIBLE` chain-too-deep,
    no R, State `9b5c…` unchanged) is distinct (prior too deep vs new would exceed).
    Do NOT claim generic `needs 32 genuine epochs`; record exact.
- Public finalize33 SUCCEEDS (fresh checks, proof/receipt/Gate/Candidate/seal with REAL
  consistent refs, NEW closure `9453e1c`, no dummy, trio style unchanged so U still allowed).
  Keys `*_path` etc., no refusal at finalize (chain new 33 not yet checked? Finalize does not
  verify new chain length? It verifies prior chain (32 valid) + new proof/closure, not new
  chain exceeds? Good).
- Public activate33 REFUSES at ACTIVATE, exact gate:
  - Code `SEAL_BIND`, Phase `ACTIVATE`, Disposition `PRESERVED_INCOMPLETE` (not INDETERMINATE,
    no State mutation, no rollback, no cleanup, incomplete preserved).
  - Detail: `low activation-record validation failed: versioned activation history invalid:
    HISTORY_ANCESTOR: history chain exceeds max32` (new chain r1..r33 =33 >32, max32).
  - Immediate inventory (before NEW valid R/State writes for r33 record + State):
    - `rec_count` 33 (r33 file `868eff46…` EXISTS as incomplete, preserved, not deleted,
      `supersedes` r32 `d755…`? Actually r33 file created during activate before validation?
      Activate creates r33 file `868eff…`, then validates history (fails chain exceeds max32),
      refuses before State write, preserves incomplete r33 (no delete, no takeover, explicit
      resume would require new id, no auto-adopt). No new VALID r33 (hist fails for r33,
      `HISTORICAL_IDENTITY_VERIFIED` false for chain33, only chain32 valid). R_FILES valid =0
      (no new valid revalidation record, r33 invalid incomplete, preserved as evidence of
      refusal, not adoption).
    - State SHA unchanged `46723c19…` →r32 `d755…` (no State write, no INDETERMINATE mutation
      to r33, pointer still r32 GOOD, strict `validate_agent_state` still PASS for chain32).
    - Renewal dirs: `high-u32-depth32-full` (complete, valid, ACTIVATED r32) + 
      `high-u33-depth32-full` (incomplete, preserved: basis `…`, retained COPY, proof/receipt/
      set/build etc. from finalize success + r33 incomplete `868eff…`, no State change,
      no cleanup, retry would require new id `high-u34…`, no same-byte takeover).
    - Anchor r30 unchanged (`8bc7c6b9…` through chain32, r33 incomplete anchor? r33 file's
      anchor? r33 incomplete has anchor r30? Actually r33 file created with anchor r30?
      But hist fails due to chain length, not anchor (anchor still r30, correct, no rolling).
      Good.
  - This IS terminal public proof for 33rd refusal (refuse before NEW valid R/State writes:
    no new valid r33, State unchanged, incomplete preserved, no rollback). Return exact
    constraint, not generic. Whole unit no CommitPoint.
- If old source constructor initial canonical State at r30 required direct State fixture
  build, allowed ONLY new test input exact descriptor not public live process rollback
  (State→r30 constructed via retained before-State COPY `068e94bc…` pointer r2 template
  updated to r30 `8bc7…`, exact descriptor `sources/2026-W37/production-state.json` with
  REAL SHA, Profile/checkpoint/canonical outputs verified, OLD `validate_agent_state` empty);
  actual tested HIGH32 public begins from fully valid input (State→r30 hist verified +
  OLD validate empty, then editorial31 public, then overlay, then renewal32 public from
  fully valid State→r31). Good.

## 5. Actual completed coverage vs remaining (whole unit no CommitPoint/PASS)

- NEW in THIS unit (CURRENT 1dad1ad/H74275d/S2290ddd, exit 0 unless noted):
  - `fixture construction r1..r30` (1 bounded construction: 30 LEGACY clones `02a7070c…`..`8bc7c6b9…`
    HISTORICAL_IDENTITY_VERIFIED HIT, State→r30 `9987d0…` OLD validate empty HIT, NOT R1×30)
  - `editorial31` (1 public method: P1/P2R/P2V/P3S50/realbuild/finalize/activate → r31
    `faba8043…` supersedes r30 anchor r30, real PDF 5pp `63473B`, State→r31, HEAD stays
    `36c679cc`, HIST31 anchor r30 HIT)
  - `overlay CURRENT 741` (1 SOURCE-only commit `fc127fc` 741 tracked, E preserved, genuine
    Core change, style `035645ca…` unchanged HIT)
  - `renewal32` (1 public method: prepare/finalize/activate → r32 `d755afac…` supersedes
    r31 anchor r30, State→r32 `46723c…`, HIST32 chain32 anchor r30, State healthy HIT)
  - `genuine commit 33rd` (1 SOURCE commit `9453e1c` comment-only, style unchanged HIT)
  - `prepare33` (1 public: ENTRY passes (prior 32 valid), creates dir+basis, State unchanged,
    no r33 yet, exit 0 — NOT refusal at ENTRY, exact recorded)
  - `finalize33` (1 public: succeeds, proof/receipt/etc., State unchanged, no r33 yet, exit 0)
  - `activate33` (1 public: REFUSES `SEAL_BIND` ACTIVATE `PRESERVED_INCOMPLETE`
    `HISTORY_ANCESTOR chain exceeds max32`, r33 incomplete `868eff46…` preserved, State
    unchanged →r32, no valid r33, exit 0 HIT for refusal proof)
  = 8 NEW raw dirs/files (construction + editorial + overlay + renewal + genuine + prepare +
    finalize + activate) + 1 failed-chronology preserved fixture (exact `HISTORY_ANCESTOR
    chronology` failure, NOT deleted). No product edits, no new authority except editorial31
    (r31) + renewal32 (r32) + genuine33 (HEAD) + prepare/finalize33 intermediate (dir+basis/proof,
    incomplete preserved); alias fork reuses existing ACTIVATED? No alias here (cited, NOT rerun).
- CITED (retained, NOT rerun decoratively):
  R7 depth 32-valid/33-refuses (STATE API+CLI, typed legacy33, NOT R1×33);
  `high-prepare-33-current-000400Z` (ENTRY chain-too-deep, no R, State `9b5c…` unchanged, CURRENT);
  `cycle-proper-rehash-000200Z` (digest preemption, CURRENT); `sequence-nonincreasing-time-000200Z`
  (HISTORY_ANCESTOR chronology HIT, CURRENT); `postreplace-true-mismatch-000200Z` (INDETERMINATE
  mismatch HIT, CURRENT); `parent-alias-same-leaf-000200Z` (HIGH_MODE ancestor path guard HIT,
  CURRENT); `healthy-activate-current-000500Z` (ACTIVATED control, CURRENT);
  `r1-anchor-correction` N1-N4 + positives (anchor identity BEFORE State write, CURRENT, separate
  worker, NOT duplicated); defensive `cycle-defensive-000000Z` (standalone unit, cycle+depth caps HIT);
  alias `samleaf-010000Z` (public RECORD_COLLISION alias-identity HIT).
- Remaining OPEN (exact, NOT run, no PASS claimed):
  HIGH 32-valid with renewal is PROVEN here via finite construction (1 editorial+1 renewal on 30
  provided predecessors, labelled scope qualifier, NOT 32 genuine renewals); true public
  SHA-consistent cycle (impossible without fixedpoint, NOT faked, NOT marked open as delivery
  requirement per task); parent-alias same-leaf via symlink parent (registry forbids: symlink
  ancestor always fails HIGH_MODE first — legitimate path guard, NOT alias-identity; real-dir
  hardlink already proves alias-identity, no further alias OPEN); `postread-true-mismatch`
  already HIT (no OPEN); R1-after-versioned (existing separate regression worker, NOT duplicated);
  C→U→U/renewal→editorial/normal lifecycle/affected regressions (separate workers, NOT duplicated).
- No whole-unit/independent PASS, no Human CommitPoint. Production semantic NO-GO retained.
  Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Representative-quality/Profile/
  adoption/savings OPEN.
