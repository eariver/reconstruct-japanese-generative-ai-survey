# R4c return — root-directed corrections (central CODE corrector)

## 1. Runtime patch REJECTED, production unchanged

Root review: the R4 `current_stage_basis_override` "patch ALL loaded instances"
is NOT adopted as production fix (broadens shared runtime authority under
mixed-fixture harness contamination; conflicts fixture-code isolation).
Action taken with dedicated editor only, no reset:
- R4 draft preserved: `correction-r4/survey_agent_tool_v2.py.r4-draft` (fb25cf55).
- `scripts/survey_agent_tool_v2.py` in DST restored to EXACT pre-R4 bytes:
  restored/archived/frozen-0d hashes all `0ff3bd9a0b13509554f82bf2a4c5e729fb2d5eea61097816076f3eaa8f84dd64`
  (`diff` identical). Other R4 fixes (export/orphan/fsync/owned recheck) RETAINED.

## 2. Isolated per-fixture Longform receipt: PASSES single-root (harness problem recorded)

New script `correction-r4c/test-r4c-longform-receipt-isolated.py` (saved BEFORE
execution): fresh subprocess per fixture, asserts exactly one jgas root on
sys.path, purges `scripts.*`, verifies every imported `scripts.*.__file__`
under the fixture root + single-root `scripts.__path__`, then calls real
`validate_editorial_receipt` on the RELEASED State (no mocks, no wrapper).
- Longform RELEASED (`jgas-longform-lifecycle-20261021T160000Z`, SP001/lf-r3c-2):
  exit 0, `RECEIPT_PASS issue=SP001 route=LONGFORM_GENERATED_V1`,
  SELECTION VERSIONED_ACTIVE. Raw: `r4c-longform-isolated-{stdout,stderr,exit}.txt`.
- Weekly RELEASED control: exit 0, `RECEIPT_PASS issue=2026-W37`. Same raws.
Conclusion: genuine single-root receipt passes AFTER RELEASED on production
(narrow) runtime. The R4-observed failure came from the lifecycle test harness
loading Weekly+Longform fixtures in ONE process (accumulated `scripts`
namespace path, `rt.evidence is not evidence`), NOT a source bug. Production
runtime stays unchanged (restored above). No ignore flag, no global patch, no
fabricated basis files. Baseline Longform readback contract (supports RELEASED)
holds.

## 3. New SOURCE snapshot (pre-authority, inert origin, untouched after commit)

New repo `/tmp/opencode/jgas-editorial-r4c-20261021T161000Z/candidate-partial-b40de60`:
- Built by `git archive` of 0d HEAD (exact 718 bytes) + 3 intended file replacements
  from DST (export workflow, `survey_agent_control_v2.py`, `survey_editorial_publication_v2.py`)
  + 1 new test file `tests/test_survey_editorial_activation_faults_r4c.py`.
- Verified: fileset = 0d 718 + 1 new (719); content diff vs 0d = exactly those 3 files;
  no `__pycache__`; no stale 39-char tree string; no hardcoded 0d HEAD in source.
- Control-file guard (0d -> DST worktree): `config/survey-production-v2.json` SAME
  (cde4f115...); all `.github/`+`config/` SAME except the intended export workflow
  fix (872f31e... -> c38423be...).
- Commit (repo-local identity only, no global config change):
  `b54a1f21a5b6b58b39777b3c5ae402219ff87715`
  tree `faef73d6e9bea08496be48462e8972d6d59536c2` (40 chars, from git not typed),
  719 files, status clean after commit (untouched).
- Valid JSON manifest `correction-r4c/source-manifest-r4.json`
  (snapshot/root/head/tree/count + 719 file pins incl. new test; tree 40;
  validated: counts match, 6 spot-check hashes OK).
- Origin inert `https://example.invalid/workerR4c-r4c-snapshot.git`, no alternates.

## 4. New fixtures: ONE Weekly + ONE Longform two-revision, REAL PDF, inert checkpoints

Scripts (saved BEFORE execution, parameterized EXPECT_HEAD/EXPECT_COUNT/INERT_ROOT,
no stale hardcodes): `correction-r4c/fixture-weekly-r4c-20261021T161000Z.py`,
`correction-r4c/fixture-longform-r4c-20261021T161000Z.py` (adapted R3c recipe).
Each ran in a FRESH cp -a copy of the snapshot (FIX_ROOT), env
`PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/opencode/r4c-pycache` set
BEFORE python startup, TL2026 lualatex, typed (synthetic, labeled) reviews.
- Weekly `/tmp/opencode/jgas-weekly-r4c-20261021T161000Z/candidate-partial-b40de60`:
  exit 0. r1 ACTIVATED (anchor VALIDATION_CHECKPOINT, supersedes null) -> r2
  ACTIVATED (supersedes r1, SAME anchor), REAL PDF 5pp 63397B, receipt/Gate PASSED,
  Candidate READY, old-immutable KEEP OK. Raw: `fixture-weekly-{stdout,stderr,exit}.txt`.
- Longform `/tmp/opencode/jgas-longform-r4c-20261021T161000Z/candidate-partial-b40de60`:
  exit 0. r1 -> r2 ACTIVATED, SAME anchor, REAL PDF 5pp 79757B, receipt/Gate PASSED,
  Candidate READY, old-immutable KEEP OK. Raw: `fixture-longform-*`.
- Inert checkpoints (captured AFTER second finalize INERT_HEALTHY, BEFORE second
  activate; cp -a, no State rewrite): `jgas-weekly-r4c-inert-...` (State->r1,
  sealed wk-r4c-2 set+candidate, NO r2) + `NOTES/inert-manifest-weekly.json`;
  same for longform (lf-r4c-2). Manifests record inert HEAD (= snapshot HEAD),
  state pointer (r1), sealed set/candidate path+sha256 (match bytes in BOTH inert
  and active copies), `record_absent` r2 path (verified absent in inert).
- No fixture commits (single snapshot commit each, HEAD still b54a1f2 everywhere);
  no network/clean/reset; HEAD pins verified post-run.

## 5. Fault regressions, real APIs, no success mocks

(a) Snapshot suite addition `tests/test_survey_editorial_activation_faults_r4c.py`
(4 tests, real writers/helpers, OS fault seam only for fsync, no validator mocks):
record-fsync classified+preserved, State-fsync classified+live-preserved,
same-byte foreign inode refused + record kept, predecessor+1 + intent refusal.
Ran in separate snapshot clone: exit 0, 4/4 OK.
Raw: `reg-editorial_activation_faults_r4c-{stdout,stderr,exit}.txt`.

(b) Orphan refusal -> explicit resume end-to-end, script
`correction-r4c/fault-orphan-resume-r4c.py` (saved BEFORE): temp cp -a of INERT
checkpoint + r2 record copied from ACTIVE fixture (State file NEVER rewritten),
real `activate_publication` must refuse, real `resume_activation` must install.
Single-fixture process with binding check.
- Weekly: exit 0. Ordinary refused `RECORD_COLLISION ... use resume` (no fork,
  State still r1); resume -> RESUMED, State->r2, VERSIONED_ACTIVE, wk-r4c-2 candidate.
- Longform: exit 0. Same refusal -> RESUMED, State->r2, lf-r4c-2 candidate.
Raw: `fault-weekly-*`, `fault-longform-*`.

## 6. Small source regressions (separate clone, not decorative full 26)

Clone `/tmp/opencode/jgas-r4c-regress-20261021T161000Z` @ b54a1f2 (untouched after):
- legacy revalidation (31): 28 pass, 3 errors in `_anchored_canonical7`
  (n10/n4/t11). IDENTICAL 3 errors on unmodified 0d code (separate 0d check clone,
  exit 1, same traces; raw `reg-legacy-reval-0dcheck-*`). Pre-existing, NOT R4
  regressions; no code path touched by R4 in that stack (low selection read path).
- agent control (5): OK. state publication authority (2): OK. low set (18): OK.
  schema cache (6): OK. Raw `reg-*-{stdout,stderr,exit}.txt` (all exit 0).
- P1/P2R helper `.latexmkrc` gap: NOT hit (no P1/P2R unittest suites in scope);
  no helper modification made; original error record preserved from R3c.

## 7. Storage / hygiene

First-6 inactive archives already reclaimed by storage worker (12k inodes/68MB).
This unit added: snapshot 14M + 2 fixtures (16M each) + 2 inert (16M each) +
1 regress clone 14M + temps (removed after use: my r4c-orphan temps, mkmanifest
script, 0d check clone). Avail ~1.6G. All current needed copies/raw kept; other
workers' copies untouched. No source pycache (external prefix always pre-set);
DST pycache unchanged; snapshot has none.

## 8. Pins for root parallel lifecycle/fault rerun

- SOURCE: `/tmp/opencode/jgas-editorial-r4c-20261021T161000Z/candidate-partial-b40de60`
  HEAD `b54a1f21a5b6b58b39777b3c5ae402219ff87715`
  tree `faef73d6e9bea08496be48462e8972d6d59536c2`, 719 files, manifest
  `correction-r4c/source-manifest-r4.json`.
- Healthy pre-Preview fixtures (VALIDATED_DRAFT, pointer r2, REAL PDFs):
  weekly + longform roots above (HEAD b54a1f2, no new commits).
- Inert checkpoint copies + manifests: `jgas-weekly-r4c-inert-...` /
  `jgas-longform-r4c-inert-...` + `correction-r4c/inert-manifest-{weekly,longform}.json`
  (State->r1, sealed set2/candidate2 with sha256, r2 absent).
- Blockers: none new. The 3 legacy-reval errors are pre-existing on 0d (evidence
  attached). No Human Commit Point taken; ordinary commits/push Human-owned.
  Independent review/packaging left to root.
