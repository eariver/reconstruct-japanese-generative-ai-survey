# Runtime bug — activation POSTREPLACE_FAIL after correct R1x2 anchor (no source edits)

Worker C diagnostic, governing d880 §9 + root selection. Fixed SOURCE717
`/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60`
HEAD `4ff2d8562502db36223332c45c9cc5d01bb93156`, tree `4a0c5343937151af0c0ad4522177441acd0e8fcc`,
tracked 717, clean before fixture (untracked Weekly authority from smoke excluded).
Independent fixture
`/tmp/opencode/jgas-workerC-r1anchor-20261021T093000Z/candidate-partial-b40de60`
same HEAD/tree, tracked 717/717 hashes match, no hardlinks (`1` link, distinct ino),
no alternates, inert origin `https://example.invalid/workerC-r1anchor-fixture.git`,
status clean before run. No DST/snapshot/R2 clean/reset/evidence deletion/network/
ordinary commits. No validator/Git mock. No whole PASS / production approval.

## Source pins (exact, fixture committed bytes)

- `scripts/survey_agent_control_v2.py` SHA256 `12995a8415f8b2ee28fab783b1688f2b3012aadb045f03ad95cf7e5be3d8f78d`
- `scripts/survey_editorial_publication_v2.py` SHA256 `d57542e0e3e54a2bdbcbd957df99d738d1659e9e78f71dbb8bfab9583a87eb1f`
- `scripts/survey_publication_set_v2.py` SHA256 `e897a638d9c113944185a7e7c76c4fd9f14d5a5bfbf06d3741b07b4ca387fa7d`
- Closure 22 (`survey_weekly_derivation_v2.CURRENT_CLOSURE` len 22) unchanged by R1 comments.
- Config `survey-production-v2.json` pipeline len 67 unchanged.
- R1 stimulus: `tests/test_survey_editorial_staged_source_v2._commit_r1_nonemitted_comment`
  anchor `fixture R1 non-emitted Python comment`, AST-equal before `def build_reader_input(`.
  Second line `fixture R1 second non-emitted Python comment C2`, also AST-equal.
  Process-scoped Git identity only (`-c user.name/email`, sanitized `GIT_*`).

## Fixture timeline (isolated R1 commits only, receipts AFTER commit)

- `4ff2d85` SOURCE snapshot (before authority).
- `a71047fce...` Fixture R1 first non-emitted comment (P3S genuine owner).
  `refresh_mechanical_evidence` via fixture-code subprocess (`python -c`, cwd=fixture,
  sanitized env, no ambient stale, `recorded 2026-09-19T08:00Z`) rc 0, dt 7.2s.
  Record `r1.json` SHA `5dadb539868ad037bd6fb1084d16b28d7dd0eef33bd410884e0b7b30a1dce27b`,
  `supersedes null`, rows cumulative vs original (superseded 1 + preserved 6 = 7).
- `744b121cc...` Fixture R1 second comment C2.
  `refresh_mechanical_evidence` via fixture subprocess (`recorded 2026-09-19T08:05Z`) rc 0, dt 8.0s.
  Record `r2.json` SHA `28c4bd0acf9540c903086367b6fd6d62598b60f3ebb141e6919ced76111ffc11`,
  `supersedes == r1 ref` (second.supersedes first OK), cumulative vs original OK.
  `resolve_active_publication_revalidation` errors `[]`, supersedes present.
- P1 `fixture-wk-r1a/b-verify` + retention capture/verify OK each; old retention `pp1`
  correctly refuses after R1b (`REF_DRIFT: KEEP recheck ... bytes differ`).
- Versioned `fixture-wk-corr-verify`: P1 envelope → retention → scope (`scope-review-v2.json`)
  → P2V `CURRENT_BASIS_OBSERVED_SCOPE_BOUND` → P3S materialize/verify OK, `code_deps 50`.
  Prepare REAL TL2026 (`lualatex-biber-lualatex`, `EXPECTED_ARGV_LUALATEX_BIBER`,
  `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex`)
  dt 29.8s, real PDF 5 pages 61239B. External typed reviews via actual
  `build_review_record` (synthetic labels, no genuine Human approval) + bounded QA
  (`validate_checks` pattern, actual file bytes). Finalize dt 20.3s, seal
  `publication-set.json` file SHA `517dd198...` (internal `set_sha256 fb449237...`
  is canonical-without-self, not file SHA — not a mismatch).
  Inert healthy (`validate_agent_state == []`) before activate.
- Activate attempts `activate_publication` with `reason WorkerC weekly editorial correction`.
  Record `r3.json` created:
  `path sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json`,
  SHA `c1edaa53bf93543ffb03c1733ea7d4d5fb7b19e5a81dc873de6951c5511394b5`,
  `supersedes == r2`, `canonical_anchor {kind LEGACY_REVALIDATION, ref r2}` — correct
  per contract (latest second legacy). `before_state_ref` etc. correct.
  State now points to `r3` (observed new), mode `VERSIONED_ACTIVE`.
  `derive_canonical_anchor` returns same anchor; `resolve_publication_selection`
  mode `VERSIONED_ACTIVE`. Old canonical files unchanged except State+record+new
  publication (inventory check: only expected delta).

## Failure callsite + exact error (no new code edits)

- `survey_editorial_publication_v2.activate_publication:3064`
  `POSTREPLACE_FAIL: [ACTIVATE/EXPLICIT_RECOVERY] primary activation wrote record+State
  but postreplace failed; observed new; record at
  sources/2026-W37/publication/v2/publication-surface-revalidation-r3.json preserved
  (never delete); secondary: post set invalid: STATE_INVALID:
  [VALIDATE/REFUSED_PRE_WRITE] strict Production State invalid:
  Stage Checkpoint artifact drift: reader-surface-gate;
  post State agent invalid: Stage Checkpoint artifact drift: reader-surface-gate`
- Secondary paths:
  `survey_editorial_publication_v2:3052 validate_prepared_set` → strict State invalid,
  `:3058 validate_agent_state` → same drift.
- Root:
  `survey_agent_control_v2._validate_checkpoint_record:405-410`
  editorial branch sets `superseded = {}` (no allowance even when
  `authority.path == prior_checkpoint.path`), then `:424-427`
  `expected = superseded.get(..., artifact.sha256)` vs live file →
  `Stage Checkpoint artifact drift: reader-surface-gate`.
- Concrete drift:
  validation checkpoint `DRAFT_COMPLETE.json` Gate `7342717d8ebbab57`,
  live `sources/2026-W37/publication/v2/reader-surface-gate-v2.json`
  `35c3aa6a7a9b5c0e` (= R1b `new_sha256`, cumulative prior `7342717d...`).
  R1a/b both correctly cumulative (`prior_sha256 == original`), union == original 7.
  Editorial postreplace expects original, not anchor effective rows, so R1-updated
  Gate fails. Contract §5 requires historical via anchor + active7 separately;
  implementation checks live Stage Checkpoint against original when revalidation
  is editorial. Not a fixture misuse: R1x2→correction with cumulative anchor is
  required §9 oracle; old canonical files remain byte-exact second legacy output
  (verified). No fake editorial reason bypass involved (fake path correctly refuses
  separately). No blanket pre-existing label: exact pins/callsite/error above,
  no code edits made to fix.

## Negative scopes AFTER versioned (complete, before-write, inventory-compared)

State already `VERSIONED_ACTIVE r3` (observed new despite POSTREPLACE_FAIL), so
revised-mode refusals tested in `verify-refusals-after-v3.py` (fresh subprocess,
immediate `_snapshot` before/after, `HEAD/status/files/special` equal):

- R1 `refresh_mechanical_evidence` rc 3:
  `REFUSED:MechanicalRefreshError:R1 mechanical refresh refused in
  VERSIONED_ACTIVE/invalid mode before any write: canonical operation refused
  in revised mode (use versioned editorial operation) (versioned renewal unselected
  §10; no editorial-reason bypass)` — nowrite OK.
- Canonical `revalidate_publication_surface REVIEWED_CORE_CHANGE` rc 3:
  `REFUSED:AgentControlError:canonical revalidation refused in revised mode:
  canonical operation refused in revised mode (use versioned editorial operation)`
  — nowrite OK.
- Fake `REVIEWED_EDITORIAL_CORRECTION` via legacy writer rc 3:
  `REFUSED:AgentControlError:publication revalidation writer refuses
  REVIEWED_EDITORIAL_CORRECTION (must use new versioned activation via
  survey_editorial_publication_v2)` — nowrite OK, no fake bypass.

Raw: `refusal-*-after.txt`, `run-stdout-v3.txt` (exit 0), `run-exit-v3.txt`.

## Remaining INCOMPLETE (truthfully, no PASS)

- Activation did NOT return `ACTIVATED`; post-State `validate_agent_state`
  = `['Stage Checkpoint artifact drift: reader-surface-gate']`,
  `validate_editorial_receipt` → same `STATE_INVALID` (saved `receipt-incomplete.txt`).
  Healthy `RECEIPT_ACTIVE_OK / GATE_ACTIVE_OK / CANDIDATE_ACTIVE_OK / ALREADY_ACTIVE`
  not achieved due to bug — not claimed.
- Second pre-Preview correction, `verify_activation_history` historical vs active
  separation beyond anchor derivation, artifact-only HEAD full closure (attempted
  cheap, saved separately as `artifact-only-incomplete.txt` if present, no old PASS
  transfer), normal synthetic Preview/Freeze/Release lifecycle, measured savings/
  old-path retirement — all OPEN, not duplicated here.
- No full Release executed (others own), no production approval.

## Artifacts

- Notes dir `verify-r1-anchor-20261021T093000Z/`:
  `verify-r1-anchor.py` (first, pycache failure raw preserved),
  `verify-r1-anchor-v2.py` (harness fix: `dont_write_bytecode` + purge, same logic),
  `verify-refusals-after-v3.py`, `run-*.txt` (cmd/cwd/env/stdout/stderr/exit/timing),
  `fixture-*.txt` (clone/remote/inode/hash/tree), `base-*.json`,
  `state-after-r1a/b.json`, `record-r1a/b.json`, `retention-r1a/b-manifest.json`,
  `publication-set.json`, `activation-record-r3.json`, `state-after-activate-r3.json`,
  `post-state-validate.txt`, `refusal-*.txt`, `summary.json` (partial) + this bug file.
- Fixture `/tmp/opencode/jgas-workerC-r1anchor-20261021T093000Z/candidate-partial-b40de60`
  HEAD `744b121...` (+ untracked versioned outputs + `r3`), no hardlinks/alternates,
  inert origin. Original DST/snapshot/R2 untouched.

No whole PASS. Bug returned for root/scope choice; no code edits made.
