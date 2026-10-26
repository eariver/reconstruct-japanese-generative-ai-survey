# Boundary verification — 32/33/cycle/alias + failure ledger reconcile (TEST-only)

2026-10-25. Co-Worker TEST-only boundary/recovery evidence. No product edits.
Contract `478f0051` §§9/11, root `7d7d5a45` §6, `operation-oracles.md` govern.
Candidate CURRENT CODE FROZEN (HEAD `409b292`, worktree CURRENT 741). No
candidate/reconstruct commits, no network, no old-runner exec, no cleanup of
failed fixtures. Fresh Python per SOURCE epoch, owned PID/heartbeat/terminal
exit, workspace TMPDIR (no quota). Whole unit no CommitPoint/independent PASS.

## 0. Source pins (FILE-BYTE SHA256, SELF only in named internal fields)

- OWN fixed runtime SOURCE copy (THIS unit, immutable before execution):
  `.rephase-1-editorial-runtime/versioned-renewal-boundary-20261025T000000Z/snapshot-work`
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
- Fixture CURRENT `48515237ddc7e8e124c514c7433bea660138a884` (parent `721a04d`,
  52 files source-only CURRENT 741 before authority, old E `??` preserved,
  inert origin, no hardlinks/alternates, no inherited `GIT_*`) with healthy
  `cu1-weekly` SEALED_INERT (REUSE_TARGETS, real PDF `0684697f…` 5pp/reviews
  reuse from `wk-boot-1`, State before `ca7c0d2e62b6…`). Fresh Python epoch
  `4851523` (NOT `e211e6e` stale 9a).
- H-ACT CURRENT `case-healthy-activate-current-20261026T000500Z`
  (exit 0, ACTIVATED r2, CURRENT pins, no stale) — healthy control for CURRENT
  faults, NOT re-run here (cited to avoid duplicate live writers).
- Anchor-fix fixture (for legacy template, read-only, no new authority):
  `.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-correction-20261025T200000Z/anchor-fix-weekly`
  (HEAD `05e32ec…`, legacy r1 `8974df…`/r2 `27db…`, editorial r3, versioned r5
  `691fcb…`, forged r6/r7/r8 inert, CURRENT product `1dad1ad/H74275d/S2290ddd`,
  same pins as OWN above, NO stale 9a).
- R7 typed legacy 32/33 retained (NOT rerun decoratively):
  `tests/test_survey_editorial_r7_boundary_v2.py::R7BoundaryTests::test_r7_depth_32_valid_33_refuses_api_and_cli`
  (WorkerD typed33 `LEGACY33_SYNTHETIC_README.txt`: 33 schema-valid
  hash-consistent legacy records, NOT actual R1×33; `Ran 1 test OK` in old
  fixture, preserved). High-prepare-33 CURRENT retained
  (`case-high-prepare-33-current-20261026T000400Z`, ENTRY chain-too-deep, no R,
  State unchanged, CURRENT, exit 0 — NOT rerun).

## 1. 32/33 (typed, NOT 32 real ops — honest scope)

ROOT allows finite valid TYPED predecessor history from real R3/renewal artifact
templates + genuine isolated tool commits/private builders, then public HIGH
32nd admission/strict State/current proof succeeds and 33rd refuses before
writes (R_FILES=0). Label fixture-provided prior history ≠ 32 real operator
runs. All refs/digests/epochs/retainedCopies/current closure/source outputs/
review target paths REAL consistent, no dummy.

- **30 legacy clones PASS (NEW, CURRENT, read-only, no authority):**
  `case-depth32-legacy-20261025T010000Z` (exit 0). Fork byte-independent from
  anchor-fix fixture; synthetic `synth-depth32-attempt/r1..r30` as untracked E
  (NOT committed, read-only test, no State write, no new R). Template = real
  legacy r1 (`8974df…`, REVIEWED_CORE_CHANGE, no kind) with same
  issue `2026-W37`/prior_checkpoint/rows, strictly increasing sequence
  (r1..r30 basename), nondecreasing time (+1s per clone), REAL file SHAs
  (no dummy), recomputed per clone. `hist.verify_versioned_history` on r30 →
  `HISTORICAL_IDENTITY_VERIFIED` (CURRENT H `74275d…`, fresh Python epoch,
  workspace TMPDIR, owned PID/exit). Proves old/new legacy allowed history
  branch can supply counts (30) with fully valid models, but counts NOT R1×32
  (fixture-provided typed history, labeled, NOT 32 real operator runs).
- **30 editorial clones FAIL at exact predicate (NEW, CURRENT, read-only):**
  `case-depth32-attempt-20261025T000000Z` (exit 2, honest failure, preserved).
  Same method but template = editorial r1 (CURRENT base, EDITORIAL kind) →
  `HISTORY_DIGEST_MISMATCH: repeated activation before_candidate must equal
  predecessor seal Candidate` (State unchanged, read-only, no new R). Exact
  blocker for naive editorial cloning without re-deriving every before State
  COPY/selected seal/record with REAL consistent bindings. NOT just
  'needs 32 real renewals'.
- **Remaining for full 32nd/33rd (OPEN, NOT executed, exact predicate):**
  31st editorial (sequence 31, anchor = latest legacy r30, staged OLD50/NEW63
  generation must match owned epoch, before_active_digest chain recompute must
  pass) + HIGH 32nd public activate (1 real op: genuine eligible Core change
  with old/new tool commits + changed paths, artifact-only never qualifies per
  contract §2; fresh basis/COPY; full proof/receipt/build/QA/Gate/Candidate/
  seal with REAL consistent refs, no dummy; strict State/current proof) +
  33rd prepare refuse `BASIS_ENTRY_INELIGIBLE chain too deep`, R_FILES=0, State
  unchanged. If editorial anchor ≠ r30, exact code is `HISTORY_ANCESTOR` anchor
  identity (same as N1-N4). HIGH 32-valid with renewal is NOT proven via legacy
  alone (wrong kind: legacy-only vs versioned active set, OLD vs NEW closure;
  do NOT use wrong-kind rowcount dummy SchemaFake). Cap33 prewrite no newR
  already proven (cited `high-prepare-33-current-000400Z`, CURRENT, typed legacy
  33, ENTRY depth, no R, State `9b5c…` unchanged, exit 0). No 32-renewal fixture
  exists; do NOT infer 32 valid from 32-legacy editorial alone.

## 2. Cycle (public malformed fails closed + defensive walker cap)

True public SHA-consistent loop impossible without cryptographic fixedpoint;
do NOT fake 'public valid cycle'.

- **Public malformed cycle fails closed (CITED, NOT rerun):**
  `case-cycle-proper-rehash-20261026T000200Z` (exit 0, CURRENT H `74275d…`,
  read-only verify, State unchanged, no new R) → `HISTORY_DIGEST_MISMATCH:
  superseded revalidation record SHA drift` (qualified preemption digest, NOT
  cycle). Best-effort 2-cycle rehash (`r2↔r3`, write r2 supersedes r3 placeholder,
  compute r2 SHA, write r3 supersedes r2, compute r3 SHA, update r2 supersedes
  to r3 SHA, recompute r2 SHA → r3 supersedes outdated) leaves one outdated →
  digest fails before cycle detection (chicken-egg cross SHAs cannot both be
  correct). Honest, NOT claimed as cycle HIT. True cycle HIT OPEN (needs
  simultaneously correct cross SHAs, infeasible with pure file edits, needs
  legitimate generator with simultaneously correct SHAs, NOT dummy SchemaFake,
  NOT constructed here).
- **Defensive walker branch probe (NEW, standalone unit, NOT public):**
  `case-cycle-defensive-20261025T000000Z` (exit 0, OWN CURRENT pins, fresh
  Python, no fixture, no authority, no State, product bytes unchanged).
  Controlled read seam (patches `_load_record_file` in-process ONLY) supplies
  cyclic ref sequence (`rA↔rB`) → `HISTORY_ANCESTOR cycle`, and 33-length linear
  chain (`r0..r32`) → `HISTORY_ANCESTOR too deep (max32)`. Both hit caps
  (`CHAIN_LIMIT==32` asserted). Explicit unit defensive, NOT full cryptographic
  proof. Qualification matches previous R7 precedent (r6-cycle-malformed fails
  closed + walker discipline `1023–1230`), sufficient bounded cycle oracle, NOT
  open impossible cryptography. Root: no duplicate case count — standalone unit
  vs public distinct (this unit counted separately from public citation above).

## 3. Alias (true ALREADY branch same-leaf hardlink)

- **Public same-leaf hardlink with real dir (NEW, CURRENT, HIT):**
  `case-alias-samleaf-20261025T010000Z` (exit 0). Fork byte-independent from
  H-ACT CURRENT (ACTIVATED r2, State new, no new setup writer — reuses existing
  ACTIVATED state). Real dir `alias-r-samleaf` (NOT symlink) + hardlink
  `alias-r-samleaf/publication-set.json` → `cu1-weekly/publication-set.json`
  (same leaf `publication-set.json`, different parent spelling, same
  `(dev,ino)`, same FILE SHA, `nlink==2`, no symlink ancestor). Activate with
  alias path → `RECORD_COLLISION ACTIVATE PRESERVED_INCOMPLETE: ALREADY_ACTIVE
  set alias input refused before writes (spelling differs but same bytes/inode;
  NOT ALREADY_ACTIVE by same SHA)` (BEFORE writes, State unchanged, no new
  record `r3`, alias + parent dir preserved, NOT ALREADY_ACTIVE). Passes
  `SEAL_BIND` set-shape (`ends with /publication-set.json`) and ancestor check
  (real dir, no symlink), then hits alias-identity. True B3 seam.
  Previous different-leaf hardlink (`alias-hardlink-…`, SEAL_BIND set-shape)
  and symlink-parent same-leaf (`alias-R-current` symlink, HIGH_MODE ancestor)
  are legitimate earlier path guards (refusal + preservation + NOT ALREADY
  proven, BUT code NOT alias-identity) — retained as partial, NOT rerun here.
  If registry forbade all alias paths, earlier SEAL_BIND/HIGH_MODE would be
  classified as legitimate public refusal/no writes (per task); here registry
  allows real-dir hardlink same-leaf, so alias-identity reached (no bypass
  invented).
- **Helper exact path+inode mode (defensive standalone, confirmation subcase):**
  Direct `_check_already_active_set` with same alias/canonical (same inode/SHA,
  different spelling) → same `RECORD_COLLISION alias` (NOT ALREADY). Counted as
  confirmation subcase within same raw (NOT separate method) per root no-duplicate
  rule (standalone unit vs public distinct, but here helper confirms public
  within one case to avoid double-count).
- **Harness defect preserved (NOT HIT, NOT deleted):**
  `case-alias-samleaf-20261025T000000Z` (exit 2, `BASIS_CURRENT_TOOL_DRIFT wrong-root`:
  reused HIGH from OWN snapshot on fork different root, correctly refused by
  product `_verify_module_roots`). Fixed by using fork's own code (same CURRENT
  pins, verified SHA before exec) in `010000Z` above. Old defect dir preserved,
  NOT cleaned, NOT counted as HIT.

## 4. Failure ledger reconcile (named IDs, actual source, exits — NO guessing)

Old 16 sum confused (testmatrix §6 counted 12 fault HIT with depth double-count
ambiguity + 3 partial + 3 seam-miss; §9 revised to 16 HIT (11+5) + 5 partial +
3 seam-miss + 5 defects + 11 OPEN, mixing stale vs CURRENT and counting H-ACT
setups inside already-active/alias/orphan as separate methods). Reconciled by
named ID with actual source/exit (read-only scan of `raw/case-*`, NO new counts
from guessing). See `reconciled-ledger.md` for per-case table (39 raw case
dirs: 37 exit 0, 1 exit 1, 1 missing; plus 4 non-case dirs: fixture-current,
healthy-current, healthy-u1, own-current). Methods/subcases/harness errors/
earlier-guard controls split (distinct, no false aggregation). No whole-unit/
independent PASS.

## 5. Actual completed coverage vs remaining (whole unit no CommitPoint/PASS)

- **NEW in THIS unit (CURRENT 1dad1ad/H74275d/S2290ddd, exit 0 unless noted):**
  - `cycle-defensive` (1 standalone defensive unit: cycle + depth caps HIT)
  - `alias-samleaf-010000Z` (1 public method: RECORD_COLLISION alias-identity HIT + helper confirmation subcase)
  - `alias-samleaf-000000Z` (1 harness defect, exit 2, wrong-root, preserved, NOT HIT)
  - `depth32-legacy-010000Z` (1 bounded read-only: 30 legacy clones HISTORICAL_IDENTITY_VERIFIED HIT, NOT 32 real ops)
  - `depth32-attempt-000000Z` (1 bounded read-only: 30 editorial clones exact predicate HISTORY_DIGEST_MISMATCH before_candidate, exit 2, honest failure, NOT HIT for 32-valid)
  - `ledger-reconcile-000000Z` (1 read-only reconcile, exit 0, 39 dirs)
  = **6 NEW raw dirs (4 HIT/verified (cycle-defensive, alias-public, legacy-30, ledger) + 1 exact-predicate failure (editorial-30) + 1 defect (alias wrong-root))**. No product edits, no new authority (except alias fork reuses existing ACTIVATED r2, no new r3; depth forks read-only, no State write, synthetic untracked E only).
- **CITED (retained, NOT rerun decoratively):**
  R7 depth 32-valid/33-refuses (STATE API+CLI, typed legacy33, NOT R1×33);
  `high-prepare-33-current-000400Z` (ENTRY chain-too-deep, no R, State unchanged,
  CURRENT); `cycle-proper-rehash-000200Z` (digest preemption, CURRENT);
  `sequence-nonincreasing-time-000200Z` (HISTORY_ANCESTOR chronology HIT, CURRENT);
  `postreplace-true-mismatch-000200Z` (INDETERMINATE mismatch HIT, CURRENT);
  `parent-alias-same-leaf-000200Z` (HIGH_MODE ancestor path guard HIT, CURRENT);
  `healthy-activate-current-000500Z` (ACTIVATED control, CURRENT);
  `r1-anchor-correction` N1-N4 + positives (anchor identity BEFORE State write,
  CURRENT, separate worker, NOT duplicated).
- **Remaining OPEN (exact, NOT run, no PASS claimed):**
  HIGH 32-valid with renewal (prior 31 versioned with 31 genuine Core epochs +
  NEW 63 closure + pipeline 71; NOT constructible without 31 genuine renewals;
  do NOT weaken via legacy alone or dummy SchemaFake); true public SHA-consistent
  cycle (impossible without fixedpoint, NOT faked); parent-alias same-leaf that
  passes ancestor but hits alias-identity via symlink parent (registry forbids:
  symlink ancestor always fails HIGH_MODE first — legitimate path guard, NOT
  alias-identity; real-dir hardlink already proves alias-identity above, so no
  further alias OPEN for B3); `postread-true-mismatch` already HIT (INDETERMINATE,
  CURRENT) — no OPEN; R1-after-versioned (existing, separate regression worker,
  NOT duplicated); C→U→U/renewal→editorial/normal lifecycle/affected regressions
  (separate workers, NOT duplicated here).
- **No whole-unit/independent PASS, no Human CommitPoint.** Production semantic
  NO-GO retained. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
  Representative-quality/Profile/adoption/savings OPEN.
