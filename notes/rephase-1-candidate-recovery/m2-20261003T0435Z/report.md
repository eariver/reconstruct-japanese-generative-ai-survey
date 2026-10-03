# Candidate recovery — Milestone 2 + runtime/import readiness report

Date: 2026-10-03 (work 13:35–13:45 JST; commit `b40de60` dated Sat Oct 3 13:36:48 2026 +0900, real clock).
Role: General Co-Worker. Authority: `task.md` + Astra `method-decision.md` (8 decisions).
Scope: source recovery, one review commit, equivalence binding, task-local runtime
provisioning, import readiness. **Zero unit tests executed. No archive created yet.
No feature code or test files edited. No reconstruct commits. No subagents.**

Evidence: `m2-20261003T0435Z/raw/` (per-command argv/cwd/stdout/stderr/exit),
`m2-20261003T0435Z/manifest.json` (machine bindings). Reconstruct HEAD at work:
`fe17541` (Human `.gitattributes` byte-protection edit observed, left untouched).

## 1. Executed method (all exits 0; any non-zero would have stopped the unit)

Target (verified absent first): `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`
(`00-*`). `git init -b codex/rephase-candidate-recovery` (`01`). Isolation:
own `.git`, no symlinks/alternates/commondir, empty remotes (`02`).

Acquisition (NO explicit `git config` commands issued): `remote add fixed-input
https://github.com/eariver/japanese-generative-ai-survey.git` (`03`),
`fetch --no-tags --depth=1 --filter=blob:none fixed-input
774dd39a951c9ac3818e83dfffd4c7666efb0a20` (`04`, genuine baseline fetch feasible —
no blocker). `FETCH_HEAD == 774dd39a...` (`05`); fetch configured its own
`[remote fixed-input] promisor=true partialclonefilter=blob:none` (read-only
inspected, removed with the remote). `sparse-checkout init --cone` +
`set .github config docs schemas scripts tests templates specials` (`06`),
`reset --hard 774dd39a...` (675 files, `07`). Verified `HEAD == 774dd39a...`,
`HEAD^{tree} == cd46a6f7a6dcc4031e76220cea4c52c7dd1fc481`, shallow log shows
baseline only (parents unavailable locally, `08`). Nine Freeze blobs verified
against SOURCE-BINDING (`09`). Removed acquisition remote, added inert
`origin https://example.invalid/rephase-candidate-recovery.git` (`10`).
All post-materialization ops ran under `GIT_NO_LAZY_FETCH=1`; inherited
`GIT_*` verified absent at start.

Patches (sequential `--check` then `apply`, each exit 0 with empty streams):
A full patch (`11`: 9 tracked M + 2 untracked), A→B (`12`: cumulative 21 M + 7 untracked),
B→e4 CLI (`13`: +1 untracked test; worktree gate file reached `ea1eb652...`,
the e4 state), R1 seven-path (`14`): preimages checked against **intermediate
worktree bytes** — all 4 matched e4-state blobs
(`2940abe3/ea1eb652/477de21e/01f9ce6b`), 3 added paths absent from worktree
AND index — then `--check`/`apply` exit 0; all 7 postimages match patch
postimage blobs (`d11febc/89b5b85/6d14009/41b289f/6c468de/0c76bb0/10d03d9`).

Delta gate: 21 tracked modifications + 11 untracked additions = 32 paths,
programmatically matched against the approved union (`15`, MATCH; `diff
--name-only` alone was NOT used — tracked `diff --name-status` plus
`ls-files --others --exclude-standard`). Staged exactly that set (`16`:
cached A11+M21, no residual unstaged/untracked). Read status/diff/log, then
one review commit with process-local `GIT_AUTHOR/COMMITTER_*` only, real date,
normal hooks, no `--no-verify`, no config writes (`17`).

## 2. New identity and equivalence (mandatory gates passed)

- HEAD **`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`**, branch
  `codex/rephase-candidate-recovery`, direct parent **`774dd39a...`**,
  tree **`657032438c6ed8b1c055d5a120b67b4b261a5092`** — **equals the expected
  historical assembled tree exactly** (`18`). Status clean after commit.
- `diff 774dd39a b40de60 --name-status` is exactly A11+M21 = approved 32
  (`19`, TREEDIFF_MATCH); `ls-tree -r HEAD` counts **32,152 entries**
  (historical e4 32,149 + 3 added — independent corroboration).
- 32 final mode/blob identities recorded (`20`, embedded in `manifest.json`).
- 9 untouched Freeze bindings at HEAD equal baseline blobs exactly (`09`, `20`).
- Isolation final: no alternates/commondir/symlinks, inert origin only,
  shallow boundary `[774dd39a...]`, sparse cone retained, global config
  untouched (`21`). No objects/commits created in reconstruct's DB.

## 3. Runtime provisioning and import readiness (no unit tests)

Task-local tooling `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z`
(measured 163M — venv/Python NOT part of any future candidate archive):
saved `pip.pyz` → `uv==0.12.15` exact (`31`, exit 0) → `uv python install
3.12.14` (`32`, exit 0) → `uv venv --python 3.12.14` (`33`, exit 0) →
`uv pip install -r <recovered fixture>/config/survey-production-v2-requirements.txt`
(`33`, exit 0). `importlib.metadata` inventory (`34`, exit 0): **Python 3.12.14**,
jsonschema 4.23.0, pypdf 6.16.2, attrs 26.1.0, jsonschema-specifications
2025.9.1, referencing 0.37.0, rpds-py 2026.6.3, typing-extensions 4.16.0 —
every recorded pin available, **no substitution**.

Import readiness (`35`/`35b`): an initial probe with the scripts directory on
`sys.path` failed (`ModuleNotFoundError: No module named 'scripts'` — the
modules use `from scripts import ...`, i.e. repo-root packaging; preserved in
`35-imports.*` as probe-path correction, NOT a code defect). Corrected
repo-root probe exits 0: `build_profiled_freeze` and `build_freeze` present,
stage validation and surface gate import clean (IMPORTS_OK).

## 4. Exact proposed test argv (NOT run — awaiting Astra approval)

All four modules use `tempfile` sandboxes and synthetic fixtures; their
`sources/...` strings are sandbox-relative writes, not real-asset reads, and
`sources/` is (by design) absent from the sparse worktree. Any missing-asset
access at execution will fail closed under `GIT_NO_LAZY_FETCH=1` (scoped
acquisition decision, no silent production fetch). No hydration is proposed
up front. Venv: `$TOOL/venv/bin/python` (`$TOOL` above). CWD: fixture root.
Env: `GIT_NO_LAZY_FETCH=1`, no `GIT_*` overrides.

Proposed (6 methods, Freeze-boundary only; no B-132/R1-97/coverage reruns):

1. `tests.test_survey_profiled_freeze_v2.SurveyProfiledFreezeV2Tests.test_release_workflow_rederives_tag_title_and_asset_from_profile_slug`
   — release-workflow consumer predicate (identity tag/title/asset from slug).
2. `tests.test_survey_profiled_freeze_v2.SurveyProfiledFreezeV2Tests.test_thematic_and_weekly_public_identity_remain_natural`
   — Weekly/Special public-identity regression guard.
3. `tests.test_survey_freeze_stage_boundary_v2.FreezeStageBoundaryV2Tests.test_approved_preview_resolves_as_typed_authority`
   — typed-approval authority resolution at the stage gate.
4. `tests.test_survey_freeze_stage_boundary_v2.FreezeStageBoundaryV2Tests.test_weekly_approved_preview_advances_through_real_freeze_boundary`
   — real Freeze-boundary advance (positive control for the forthcoming writer work).
5. `tests.test_survey_gate_cli_persisted_review_v2.GateCliPersistedReviewV2Tests.test_direct_primary_cli_admission_absolute_relative_and_cwd`
   — real CLI admission incl. the recovered `test_survey_reader_surface_gate_v2` fixture import and `REPO`-rooted reads.
6. `tests.test_survey_publication_v2.SurveyPublicationV2Tests.test_exact_reviewed_pdf_chain_reaches_release_without_postapproval_quality_gate`
   — canonical exact-reviewed chain regression (positive control).

Prerequisites: none beyond the pinned venv + recovered fixture + inert origin
(all present). Oracle rationale: 1–2 pin the workflow/identity consumer
contract the joint Freeze change must preserve; 3–4 pin stage-gate authority
the builders rely on; 5 pins the CLI path the writer-preflight will reuse;
6 pins the canonical chain the wrapper must not regress. Negative/mixed-pair
oracles belong to the Freeze implementation unit, not recovery verification.

## 5. Proposed Git-aware current-source closure check (NOT run — awaiting approval)

`closure-freeze-identity` probe (read-only; no state/output writes), to run in
the pinned venv with `GIT_NO_LAZY_FETCH=1` from a neutral CWD:

1. Git half: assert `rev-parse HEAD == b40de60`, `HEAD^{tree} == 6570324...`,
   and `git show HEAD:<path>` bytes equal worktree bytes equal expected blob
   for the 9 Freeze paths + workflow + 4 schemas (fail on first mismatch).
2. Real-helper half (exercises actual validators, not a listing):
   `jsonschema.Draft202012Validator.check_schema()` on each recovered schema
   JSON; execute `scripts.survey_profiled_freeze_v2.public_issue_slug` and the
   profiled `release_identity` on a minimal synthetic profile and assert
   well-formed slug/identity shape. (Deliberately does NOT assert
   profiled-vs-canonical identity agreement — that divergence is the DM-019
   defect under contract, and must remain a pre-repair witness, not a passing
   assertion.)
3. Record stdout/stderr/exit plus the exact helper return values.

## 6. Packaging estimate (measured only — no archive created)

Recovery fixture: **17M total** (`.git` 8.7M, 48 object files; worktree ~8M).
Compressed snapshot estimate ~4–6M — far below the 50MiB packet gate, so the
final partial-DB + materialized-worktree archive (after justified test assets,
per decision §8) is expected to fit in the packet with hashes. Tooling/venv
(163M) is excluded from the candidate archive by design. No `git bundle`
attempted (hydration risk noted in decision §7); the planned artifact is a
verified byte-copy tarball + object/byte inventory + offline second-DB restore
check, executed only after selected tests/assets stabilize.

## 7. Limitations and root decisions needed

Limitations (carried, §manifest): shallow+promisor partial history; new honest
identity (no 481/e4 ancestry, no PASS transfer); tree equality ≠ full
history/asset closure; 41 R1 data blobs unverified; worktree umask modes
(664) vs Git-recorded 100644 (binding uses Git modes).

Decisions needed before further execution:

- D1. Approve the §4 exact 6-method argv (or amend) for the small
  source/runtime verification run.
- D2. Approve the §5 closure-check probe design (or amend) — it executes real
  helpers but is still a new probe requiring authorization.
- D3. Confirm archive-after-assets sequencing (§6): snapshot + offline restore
  only after D1/D2 pass and any justified test assets are materialized.
- D4. Fresh independent reviewer assignment for the recovery boundary
  (task milestone 5), before any Freeze implementation unit begins.

No blockers: genuine fixed-baseline fetch succeeded and final tree matches.
Work stops here for Astra review; reconstruct commit/push remains Human-owned.
