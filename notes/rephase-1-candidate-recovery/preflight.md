# Candidate recovery — Milestone 1 preflight (feasibility proposal)

Date: 2026-10-03T04:30:19Z / 13:30:19+09:00 (actual clock).
Role: General Co-Worker. Scope: **Milestone 1 only** — feasibility/preflight proposal.
No bulk recovery, no test execution, no feature edits, no root replacement,
no whole clone/archive/fresh-root substitute, no ordinary reconstruct commits.
Old scripts are evidence only (not executed). No broad inventory or
main/Summary/Issues refresh was performed.

Read: `AGENTS.md`, `notes/rephase-1-candidate-recovery/task.md`,
`outputs/rephase-1-dm001-019-contract-decision.md` §§2,5,
`notes/rephase-1-dm001-contract/recovery-inventory.md`,
`notes/rephase-1-session-transition/restart-context.md` (recovery guidance +
old preparation mechanics), `notes/rephase-1-dm001-contract/fixed-content/SOURCE-BINDING.md`,
`notes/rephase-1-r1-assembly/20260929T143833Z-assembly/report.md` (prior
assembly mechanics, not rerun).

Reconstruct HEAD at preflight: `fe17541` (`main...origin/main`).
`/tmp/jgas*` and `/tmp/*rephase*` both absent (verified this session).
Reconstruct `.git` was never touched for fixtures.

## 1. Fixed identities (verified read-only this session)

Baseline commit (pinned, via `gh api .../git/commits/774dd39a...`, exit 0):

- commit `774dd39a951c9ac3818e83dfffd4c7666efb0a20`
- message `Merge pull request #496 ... fix(core-v2): add pre-publication reader-surface gate (#434)`
- parents `4cbf34191668ccc033560611f103c15bc4ce84d3`,
  `0f6f84fd13803f834da196f7964e1080f00690db`
- tree `cd46a6f7a6dcc4031e76220cea4c52c7dd1fc481`
- author `EaRiver <yuahykw@gmail.com> 2026-09-14T14:28:25Z`,
  committer `GitHub <noreply@github.com>` (same stamp)

Root tree (via `gh api .../git/trees/cd46a6f7a...`, exit 0, `truncated: false`):

- full SHA `cd46a6f7a6dcc4031e76220cea4c52c7dd1fc481` — matches saved intake
  (`notes/rephase-1-deferred-intake-20261003/deferred-maintenance-summary.md:8`,
  `delta-analysis.md:9`). The `cd46a6f7...` prefix in the task brief is this object.
- 14 top-level entries (`.github`, `.gitignore`, `.latexmkrc`, `AGENTS.md`,
  `README.md`, `config`, `docs`, `schemas`, `scripts`, `sources`, `specials`,
  `surveys`, `templates`, `tests`).

Raw evidence (new, unique): `preflight-20261003T0430Z/raw/` —
`fixed-commit-774dd39a.json` (SHA256 `068acac7...`),
`root-tree-cd46a6f7a.json` (SHA256 `92748016...`), empty stderrs, exits `0`.
No re-fetch is needed; reuse these files for Milestone 2.

Expected final content tree after the 4-delta chain:
`657032438c6ed8b1c055d5a120b67b4b261a5092` (historical 481 tree; content
equality target, **not** ancestry restoration).

Durable delta chain (SHA256 re-verified this session, all match inventory):

| # | Transition | File | SHA256 | Bytes | diffs |
|---|---|---|---|---|---|
| 1 | baseline→A (full, incl. a1/f1) | `notes/rephase-1-increment-a/application.patch` | `0f4bee2c...` OK | 83,377 | 11 |
| 2 | A→B | `notes/rephase-1-increment-b/increment-b.patch` | `bdff2c29...` OK | 287,397 | 21 |
| 3 | B→e4 | `notes/rephase-1-gate-cli/increment-gate-cli.patch` | `29b7f187...` OK | 34,507 | 2 |
| 4 | e4-content (R1 seven-path) | `notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch` | `7817fa4f...` OK | 252,014 | 7 |

Total patch bytes 657,295. Union by `diff --git` path: **32 paths** (list in §4).
Explore reported a 31-path union; direct grep here gives 32 (41 entries minus
9 duplicates across 6 overlapping paths). Discrepancy is flagged for Astra
(§7 Q1) — it does not block preflight but must be resolved before the
Milestone 2 `add` allow-list is frozen.

Nine Freeze-boundary files are chain-untouched (five-patch `diff --git` grep 0
per SOURCE-BINDING): both Freeze scripts, both Freeze tests, release workflow,
four schemas. Baseline bytes = chain-latest bytes for exactly those paths
(static evidence, not live-HEAD proof).

## 2. Available tooling / assets (inspected, not executed)

- `git 2.53.0`, `gh 2.46.0`. `gh` read-only fixed-object fetch works (2 calls,
  both exit 0 above).
- `python3` is **3.14.4 only**. No `python3.12`, no `pip`/`pip3`, no `uv`,
  no `/tmp/jgas-rephase-python`, no `/tmp/jgas-rephase-application-venv`.
  `.rephase-1-inputs/integration-venv` is Python 3.14.4 without
  `jsonschema`/`pypdf`. `.rephase-1-inputs/pip.pyz` (1.7M) survives.
- Direct pins available in fixed cache:
  `.rephase-1-inputs/774dd39a.../config/survey-production-v2-requirements.txt`
  contains `jsonschema==4.23.0`, `pypdf==6.16.2` (matches restart-context pins).
  Transitive pins (attrs 26.1.0, jsonschema-specifications 2025.9.1,
  referencing 0.37.0, rpds-py 2026.6.3, typing-extensions 4.16.0, uv 0.12.15,
  CPython 3.12.14) are historical observations only.
- Fixed cache `.rephase-1-inputs/774dd39a.../` is present (44M total for
  `.rephase-1-inputs/`). Sparse-cone-relevant sizes: `scripts/` 3.1M (212
  files = full script set per `tree.json`), `schemas/` 372K, `tests/` 112K
  (only 5 files — sparse cache, not content gap), `docs/` 1.6M, `.github/` 72K,
  `config/` 216K, `templates/` 28K, `specials/` 124K, `sources/` 448K.
  `tree.json` 13,698,921 bytes, SHA256 `80e788f5...` OK, `truncated: False`,
  34,155 entries (trees + blobs; blob-only sparse-cone subset below).
- `tree.json` sparse-cone estimate (prefixes `.github config docs schemas
  scripts tests templates specials`, blob entries only): **704 blobs,
  5,897,694 bytes**. Full sparse worktree + `.git` (commit + trees + sparse
  blobs) is therefore on the order of ~10–30M, well within `/tmp` (7.4G avail).
- Old preparation mechanics (reference only, **not run**):
  `notes/rephase-1-application/prepare_candidate.py` (init → remote
  `fixed-input` → `promisor true` + `partialclonefilter blob:none` →
  `fetch --no-tags --depth=1 --filter=blob:none fixed-input BASE` →
  `sparse-checkout init --cone` + `set .github config docs schemas scripts
  tests templates specials` → `reset --hard BASE` → remove acquisition remote
  → inert `origin https://example.invalid/...`), `hydrate_test_assets.py`
  (fixed-SHA blob verification, <5M cap, cache-or-`raw.githubusercontent`
  fallback), `test-assets.json`, `runtime-setup.md` (uv 0.12.15 + CPython
  3.12.14 + pins above). These mechanics are sound for reuse with a NEW target
  path; their fixed `/tmp` targets and overwriting logs must not be reused.
- Reconstruct `.git/hooks/` holds samples only; no custom hooks observed.
  Global/user git config holds only Human identity + `gh` credential helpers;
  no fixture overrides.

## 3. Proposed exact method (Milestones 2–4, for Astra selection — NOT executed)

Target (new, unique at execution time):
`/tmp/jgas-rephase-candidate-recovery-<UTC timestamp>Z`
(e.g. `20261003T04XXXXZ`). Pre-create guards: verify `/tmp` is `drwxrwxrwt`,
target absent, no `GIT_*` env (`env | grep ^GIT_` empty), reconstruct HEAD
still `fe17541` clean, patch SHA256 re-check (table §1).

Independent DB creation (outside reconstruct `.git`):

1. `git init -b codex/rephase-candidate-recovery <TARGET>` (fresh branch name;
   do not reuse `codex/rephase-1-*`).
2. Verify `rev-parse --absolute-git-dir == <TARGET>/.git`, `.git` is a real
   directory, no symlinks in `.git`, no `objects/info/alternates`, no
   `.git/commondir` file, `git remote -v` empty.

Safe sparse/partial acquisition (same cone as proven mechanics):

3. `git -C <TARGET> remote add fixed-input https://github.com/eariver/japanese-generative-ai-survey.git`
4. `git -C <TARGET> config remote.fixed-input.promisor true` and
   `remote.fixed-input.partialclonefilter blob:none` (repo-local only; never
   touch user/global config).
5. `git -C <TARGET> fetch --no-tags --depth=1 --filter=blob:none fixed-input 774dd39a951c9ac3818e83dfffd4c7666efb0a20`
6. Verify `rev-parse FETCH_HEAD == 774dd39a...`.
7. `git -C <TARGET> sparse-checkout init --cone` then
   `sparse-checkout set .github config docs schemas scripts tests templates specials`
   (covers all 32 union paths + Freeze boundary + workflow/schemas; excludes
   bulk `sources/`/`surveys/` except later justified test-asset hydration).
8. `git -C <TARGET> reset --hard 774dd39a951c9ac3818e83dfffd4c7666efb0a20`
9. Verify `rev-parse HEAD == 774dd39a...` and
   `rev-parse HEAD^{tree} == cd46a6f7a6dcc4031e76220cea4c52c7dd1fc481`.
   Spot-check the 9 Freeze blobs via `git hash-object` vs SOURCE-BINDING table
   (e.g. `survey_profiled_freeze_v2.py → 27e5bcb1...`, already confirmed in
   cache this session).
10. `git -C <TARGET> remote remove fixed-input`; then
    `git -C <TARGET> remote add origin https://example.invalid/rephase-candidate-recovery.git`;
    verify `remote -v` shows only the inert URL (2 lines), `shallow` and
    `info/sparse-checkout` preserved as evidence, no `alternates`.

Four sequential patch checks/applications (stop on first mismatch, no code edits):

11. For patches 1–3 in order: verify SHA256 (§1 table), then
    `git -C <TARGET> apply --check <patch>` (expect exit 0, empty stdout/stderr),
    then `git -C <TARGET> apply <patch>` (expect exit 0, empty streams).
    After each, record `status --porcelain`, `diff --stat`, and `ls-tree HEAD`
    vs worktree `hash-object` for touched paths.
12. For patch 4 (R1 seven-path, basis `a1a4242..b74` but preimages coincide with
    e4 per historical assembly §3): before `apply --check`, verify 4 preimages
    via `ls-tree HEAD` + `ls-files` (`survey_agent_control_v2.py 2940abe...`,
    `survey_reader_surface_gate_v2.py ea1eb65...`,
    `survey_weekly_derivation_v2.py 477de21...`,
    `test_survey_publication_revalidation_v2.py 01f9ce6...`) and 3 absents
    (`survey_weekly_mechanical_refresh_v2.py`,
    `test_survey_weekly_mechanical_refresh_v2.py`,
    `weekly-mechanical-refresh.md` empty in both `ls-tree` and `ls-files`).
    Then same `--check` → `apply` pair. Post-apply, verify all 7 worktree
    mode/blob/SHA256 equal the committed R1 `changed-files/` copies and
    `ls-tree b74`-equivalent blobs cited in the assembly packet (modes `644`).
13. Post-chain worktree check: `diff --name-only HEAD` (HEAD still baseline)
    must equal the frozen 32-path union (§4); no extra changed/untracked paths
    except the intended 32 (+ pre-existing `__pycache__` if any, recorded not
    deleted). `diff --cached` must be empty before staging.

Review commit (own DB only, normal hooks, process-local identity):

14. Inspect `status`, `diff`, `log --oneline -10` (expect baseline ancestry:
    `774dd39a` on top of `4cbf341...`/`0f6f84f...` merge parents).
15. `git -C <TARGET> checkout -b codex/rephase-candidate-recovery` only if not
    already on it from init (no import of b74/a1 history).
16. `git -C <TARGET> add -- <32 union paths>` (exact allow-list from §4 after
    Astra resolves Q1; no pycache). Verify cached `diff --cached --name-status`
    is exactly A+M for those paths.
17. Commit with process-local env only, real date, no bypass:
    `GIT_AUTHOR_NAME='Candidate Recovery General Co-Worker'`
    `GIT_AUTHOR_EMAIL='candidate-recovery@example.invalid'`
    `GIT_COMMITTER_NAME=...` / `GIT_COMMITTER_EMAIL=...` (same values),
    no `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` overrides, no `git config`
    writes, no `--no-verify`/`-n`, no `amend`/`reset`/`clean`, no
    `core.hooksPath` override, no inherited `GIT_DIR/WORK_TREE/INDEX_FILE/
    OBJECT_DIRECTORY/ALTERNATE_OBJECT_DIRECTORIES/COMMON_DIR`.
    Record stdout/stderr/exit (expect `7 files changed`-style summary for the
    final commit only if staged per-delta; preferred is ONE review commit over
    the full 32-path delta — see Q2).
18. Post-commit binding: record `rev-parse HEAD` (new honest identity — NOT
    `481dec0`), `rev-parse HEAD^{tree}` (must equal
    `657032438c6ed8b1c055d5a120b67b4b261a5092`), `log --format=%P -1` (must be
    `774dd39a...`), `branch --show-current`, `status` (clean except pycache).

Full tree reference equality (content, not history closure):

19. `git -C <TARGET> ls-tree -r HEAD | wc -l` vs baseline blob count from
    `tree.json` (note: `tree.json` 34,155 includes trees; compare blob-only
    counts, not raw totals). `diff <(git ls-tree -r 774dd39a) <(git ls-tree -r HEAD)`
    must show exactly the 32 union paths differing with expected modes/blobs;
    all other references byte-identical (promisor references compared as tree
    metadata without hydration, as in historical assembly §3).
20. Final `HEAD^{tree} == 657032438c6ed8b1c055d5a120b67b4b261a5092` is the
    content gate. Tree equality alone is not history/asset closure (§5 limits).

## 4. Union path list (proposal for the Milestone 2 allow-list)

32 paths (pending Astra Q1 resolution of the 31-vs-32 count):

- docs (5): `docs/survey-production-core-v2-authority.md`,
  `docs/survey-production-core-v2-execution-record-policy.md`,
  `docs/survey-production-core-v2-redesign-authority.md`,
  `docs/survey-production-core-v2-session-bootstrap.md`,
  `docs/weekly-mechanical-refresh.md`
- schemas (3): `schemas/reader-surface-gate-v2.schema.json`,
  `schemas/reader-surface-input-v2.schema.json`,
  `schemas/weekly-publication-source-manifest-v2.schema.json`
- scripts (11): `scripts/run_drafting_synthesis_v2_interactive.py`,
  `scripts/survey_agent_control_v2.py`, `scripts/survey_agent_tool_v2.py`,
  `scripts/survey_drafting_citation_refs_v2.py`,
  `scripts/survey_execution_record_v2.py`,
  `scripts/survey_reader_publication_v2.py`,
  `scripts/survey_reader_surface_gate_v2.py`,
  `scripts/survey_stage_validation_v2.py`,
  `scripts/survey_weekly_derivation_v2.py`,
  `scripts/survey_weekly_semantic_publication_v2.py`,
  `scripts/survey_weekly_mechanical_refresh_v2.py`
- templates (1): `templates/survey/jgaisurvey.sty`
- tests (12): `tests/test_survey_bibliography_access_provenance_v2.py`,
  `tests/test_survey_exact_manuscript_admission_v2.py`,
  `tests/test_survey_findings_v2.py`,
  `tests/test_survey_freeze_stage_boundary_v2.py`,
  `tests/test_survey_gate_cli_persisted_review_v2.py`,
  `tests/test_survey_increment_b_boundary_matrix_v2.py`,
  `tests/test_survey_increment_b_weekly_derivation_v2.py`,
  `tests/test_survey_publication_revalidation_v2.py`,
  `tests/test_survey_reader_surface_gate_v2.py`,
  `tests/test_survey_semantic_publication_v2.py`,
  `tests/test_survey_weekly_evidence_authority_v2.py`,
  `tests/test_survey_weekly_mechanical_refresh_v2.py`

Docs 5 + schemas 3 + scripts 11 + templates 1 + tests 12 = 32.

Overlaps: `survey_agent_control_v2.py` ×3, `survey_reader_surface_gate_v2.py`
×4, `survey_stage_validation_v2.py` ×2, `test_survey_exact_manuscript_admission_v2.py`
×2, `survey_weekly_derivation_v2.py` ×2, `test_survey_publication_revalidation_v2.py` ×2.

## 5. Scale / risk

- Network (Milestone 2): one depth-1 `blob:none` fetch of `774dd39a` + sparse
  checkout of 704 blobs (~5.9M). Trivial; no whole clone/archive.
  Fallback if fetch fails: reuse ignored fixed cache blobs with per-file
  `hash-object` verification + `git hash-object -w` construction — NOT
  preferred (risks synthetic history); return blocker to Astra instead of
  silently substituting cache bytes for fetched objects.
- Disk: `/tmp` 7.4G avail; expected new DB + worktree ~10–30M; patch chain
  0.7M; `tree.json` already on disk (14M). Bundle (§6) expected single-digit MB
  (historical e4 DB had 6,235 objects; new shallow DB will have far fewer).
  No giant archive goes to reconstruct without Astra size-gate approval.
- Time: fetch + sparse checkout + 4 apply pairs + one commit + tree diffs is
  minutes (excluding test execution, which belongs to Milestone 3).
-Python/runtime (Milestone 3 prerequisite, not run now): no 3.12 runtime
  exists. Provisioning requires network (`uv python install 3.12` or
  equivalent + `uv pip install -r <fixed requirements>` with exact pins) and a
  new isolated venv outside `/tmp/jgas-rephase-application-venv` (absent).
  Fallback: system 3.14 import check only — INSUFFICIENT for acceptance
  (3.10 incompatibility precedent; 3.14 is untested for this Core). Do not
  claim runtime closure on 3.14.
- Honest limits (carried, not healed by preflight): shallow `depth=1` +
  `blob:none` promisor means incomplete history and missing blobs; the new HEAD
  is an honest new identity directly descended from real `774dd39a`, NOT
  restored `481dec0`/e4 ancestry; 41 R1 historical data blobs remain
  unverified; test assets under `sources/...` need justified hydration at
  fixed SHA (cap <5M per old mechanics) before any test that touches them;
  `tree.json` 34,155-entry count includes trees (compare blob-only counts);
  saved runners remain evidence only.

## 6. Physical storage / durable artifact + offline restore (design, not built)

- Portable artifact (Milestone 4 proposal): `git bundle create
  candidate-recovery-<HEAD7>.bundle --all` from the recovery DB + sidecar
  manifest (new HEAD/tree/parent, 32 mode/blob/SHA256 rows, 4 patch SHAs,
  baseline commit/tree pins, `shallow` + `sparse-checkout` copies, `remote -v`
  inert proof, `ls-tree` diff summary, venv pin record). Bundle stays OUTSIDE
  reconstruct until Astra clears the size gate; reconstruct stores only the
  manifest + restoration recipe if the bundle is large. No credentials in any
  artifact.
- Completeness statement: bundle covers the shallow single-commit history +
  sparse blobs only; it is NOT a full-history backup and cannot rehydrate
  promisor-missing `sources/...` blobs offline. Thin/partial status will be
  explicitly labeled; a thin bundle is not claimed as complete backup.
- Offline restore verification (second independent DB, no sharing):
  `git init -b verify <SECOND>` (absent-guard) → `git -C <SECOND> fetch
  <bundle> --all` or `git clone --no-hardlinks <bundle> <SECOND>` with network
  disabled (no remotes pointing at production; inert origin only) → verify
  `HEAD`/`HEAD^{tree}`/parent equal the recovery commit, `ls-tree -r` identical,
  all 32 materialized runtime bytes identical (`sha256sum` row match), inode
  comparison shows no hardlinks to the first DB, no `alternates`. Record
  sizes/closure before any reconstruct packaging.

## 7. Verification matrix (Milestone 2–4 gates; this preflight ran only P0–P1)

| ID | Gate | Method | Expected | Evidence (new unique paths) |
|---|---|---|---|---|
| P0 | Patch bytes | `sha256sum` 4 patches | §1 table SHAs | Milestone 2 manifest |
| P1 | Fixed identity | `gh api` commit + root tree (DONE) | `774dd39a...` / `cd46a6f7a...` | `preflight-20261003T0430Z/raw/` |
| P2 | Isolation | `absolute-gitdir`, no symlinks/alternates, `remote -v`, `env \| grep GIT_` | Own `.git`, inert origin, no overrides | Milestone 2 manifest |
| P3 | Baseline presence | `rev-parse HEAD`, `HEAD^{tree}` | `774dd39a...` / `cd46a6f7a...` | Milestone 2 manifest |
| P4 | Sequential apply | 4× `apply --check` (exit 0, empty streams) then `apply` | All exit 0; R1 preimages 4+3 verified first | Per-patch stdout/stderr/exit files |
| P5 | Worktree delta | `diff --name-only HEAD` (pre-commit) | Exactly frozen 32-path union | Manifest + `status`/`diff` raws |
| P6 | Review commit | Process-local `GIT_*`, real date, hooks normal | New HEAD, parent `774dd39a...`, no `--no-verify` | Commit stdout/stderr/exit + `log -2` |
| P7 | Tree equality | `rev-parse HEAD^{tree}`, `ls-tree -r` diff | `657032438c...`, only 32 refs differ | `ls-tree` raws + tree diff |
| P8 | Imports (M3) | `python -c "import survey_profiled_freeze_v2, ..."` + `jsonschema/pypdf` versions | Import exit 0 on 3.12.14 + pins | M3 logs (not run now) |
| P9 | Small affected tests (M3) | §8 selection only | Real validators, no mocks | M3 logs (not run now) |
| P10 | Bundle + offline restore (M4) | `git bundle` + second-DB clone/fetch | Identity/tree/bytes equal, no sharing | Bundle manifest + restore log |

Fail policy: any P2–P7 mismatch stops before code alteration; return raw
evidence + concrete blocker. No validator weakening, no unrelated hydration,
no repair broadening to force green. Distinct labels for setup failure vs
missing asset vs skip vs expected parent defect vs success (Milestone 3).

## 8. Imports + small affected-test proposal (Milestone 3 — proposed, NOT run)

Provision first: isolated Python **3.12.14** + `requirements.txt` pins
(`jsonschema==4.23.0`, `pypdf==6.16.2`) in a NEW venv (not the absent
`/tmp/jgas-rephase-application-venv`); record `pip show`-equivalent inventory
(the historical final-run inventory failed on missing pip — do not repeat that
gap; capture versions from import + metadata).

Boundary checks (minimal, Freeze-interface only):

1. `python -c` imports (no fixtures): `survey_profiled_freeze_v2`,
   `survey_publication_v2`, `survey_stage_validation_v2`,
   `survey_reader_surface_gate_v2`; plus `jsonschema.__version__`,
   `pypdf.__version__` assertions.
2. Git-aware source closure: `ls-tree -r HEAD` for the 32 paths + release
   workflow + schemas vs §1/P7 bindings (no filesystem scan).
3. Small real-test selection (4–6 methods, exact names for Astra to confirm;
   no full B-132 / R1-97 / 24-test rerun for coverage):
   - `tests/test_survey_profiled_freeze_v2.py` — existing slug/identity/workflow
     regression (never calls `build_profiled_freeze`; regression only).
   - `tests/test_survey_publication_v2.py` — canonical chain subset (1–2 methods).
   - `tests/test_survey_freeze_stage_boundary_v2.py` — A boundary subset (1 method).
   - `tests/test_survey_gate_cli_persisted_review_v2.py` — e4 CLI subset (1 method).
   Synthetic approvals/PDFs prove type/identity only. If any selected test
   needs missing `sources/...` assets, hydrate ONLY those blobs at fixed SHA
   (verify `hash-object` vs `tree.json` row) before the run; record cache-hit
   vs network rows. Unrelated suites stay unrunned.

## 9. Root decisions needed (no recovery bulk work until answered)

- Q1. Freeze the 32-path union vs Explore's 31: accept the direct-grep 32
  (proposed §4) or direct which single path to exclude and why?
- Q2. One review commit over the full 32-path delta (recommended: single honest
  new identity, simplest bundle) vs 4 sequential review commits (A/B/e4/R1
  checkpoints, more faithful staging but 4 new identities)? Preflight assumes
  ONE commit; confirm.
- Q3. Sparse cone: keep proven `.github config docs schemas scripts tests
  templates specials` (recommended) or add minimal `sources/` hydration up
  front? Preflight proposes cone-as-is + justified per-test hydration later.
- Q4. Python 3.12.14 provisioning authority: allow networked `uv` install +
  pinned `pip install` in Milestone 3, and record exact venv path?
- Q5. Durable bundle size gate: threshold (e.g. 50M) above which reconstruct
  stores manifest + recipe only, bundle held outside? And new
  `notes/rephase-1-candidate-recovery/** -text` byte-protection rule (Human/root
  edit; General does not edit `.gitattributes`)?
- Q6. Small-test selection (§8): confirm/adjust the 4–6 method list, or direct
  a different Freeze-boundary subset before Milestone 3 runs anything?

## 10. Preservation / scope compliance

- New files this unit: `notes/rephase-1-candidate-recovery/preflight.md`
  (this file) + `preflight-20261003T0430Z/raw/` (2 JSON + 2 stderr + 2 exit).
  `task.md` and all older packets untouched. No existing-file edits, no
  reconstruct commits, no pushes.
- No subagents used. No feature code. No test execution (only read-only `gh`
  metadata + local `ls`/`sha256sum`/`grep`/`git -C ... check-attr/log/status`
  reads).
- Next: await Astra method decision (Q1–Q6); then Milestone 2 recovery in a new
  location with normal hooks + process-local identity + real date.
