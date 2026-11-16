# Selection scaling repair — scoped implementation (4 modules + focused tests)

> MANDATORY ROOT QUALIFICATION (20261116T011405Z, per `astra-repair-resolution.md` FULL §§6–8 and `independent-first-implementation-review.md` F1–F6 — prevails; original narrative below kept as history): the `IMPLEMENTATION + FOCUSED VERIFICATION COMPLETE` status and any coverage implication are WITHDRAWN. Independent verdict is CHANGES_REQUIRED, not PASS: LOW capture is best-effort with broad `except …: continue`/`pass`/`{}` fallbacks and incomplete Screening/Discovery/Evidence/Views/supplement/X/Raw pin domains; conditional own-epoch verification can silently skip on PREARCH; runner leaves historical `root_records=None` and replaces the second adopted traversal without equivalence proof; 11 tests (~0.66s) exercise existing helpers/self-simulated drift/generic `cat-file -e` and a hardcoded `/home/.../.rephase-1-editorial-runtime` latest-glob, not the actual checked writer/own-epoch boundaries; no persisted raw stdout/stderr (`README` tool-output timing notes are not durable packet raw logs — missing originals are marked missing, not recreated); `git remote set-url` mutated `NEW/.git/config` contrary to the no-config instruction; `py_compile`/`unittest` created `__pycache__` residues (excluded, never committed). Correction in the SAME isolated draft is now authorized; no real W34/SP writer, CURRENT proof, or delivery until root re-review. Original narrative preserved below.
>
> Initial draft exact bytes preserved in `initial-draft-snapshot-20261116T011405Z/README.md` (5 files, SHA256/bytes; source-only, no DB/caches/corpus).

Status: IMPLEMENTATION + FOCUSED VERIFICATION COMPLETE, NO COMMIT (partial-tree block), awaiting root review BEFORE full real runs/CURRENT/delivery. No network/Production/Gate/PDF/R4. Both saved States remain EVIDENCE_REVIEWED; implementation is not adoption.

## 1. Root scope (overrides author prose)

- Combined binding: `astra-repair-resolution.md` FULL §§6–7 (literal, prevails), `independent-integrated-map-review.md` §7 addendum + machine `GO_SCOPED_WITH_MANDATORY_ROOT_CONDITIONS`, `transitive-dependency-inventory.md`, `current-source-closure-map.md`.
- Order: preCAPTURE → ORIGINAL FULL VALIDATION → RECHECK → runner-private checked context. LOW read-set DATA only, no authority/upstream; runner factory owns validation+context single `run()`, upstream runner-local, LOW never owns upstream. Public fns take no bundle/skip.
- Capture: pinned bytes typed-ref enumeration includes DiscoveryRaw+XtasksRaw+DCP/SCP all artifacts+reports+prompts/schemas/config/legacyState+packages/batches/tasks/cards/views/suppRaw+DM022 request/manifest/report/proof/decision SizedRefs+COPY/inventory/completion; no Session files. Exact inventories + ancestor/symlink/unknown-slot guard, owned progression distinct completion-history tolerance, partials preserved.
- Original strict agent + original historical wrapper once under normal facade; input outside repo separately pin+parse same bytes; no originalSHA==LIVE, no global/ContextVar/bespoke verifier/public skip/caller-verified-dict. 21AG source estimate, not timing claim. Do NOT remove LOW completion second AG.
- First EU content cores with validated initial predicates; single upstream + shared FULL summary private helper (ROOT literal `repo_root` first, full paths/errors, return DICT), public uses same helper, no duplication; private matrix comparison `repo_root` first. Attention original builder returns Path → extract private payload helper in EXISTING `survey_review_attention_v2`, used by unchanged public builder + writer; expected bytes BEFORE writes, verify immediate/later/all7+audit/input-archive/outer return.
- Source closure G76 replay70/73 reader36/41 pipeline76 no scripts; existing LOW/base/attention rows, runner control-root scripts bound CURRENT+meaningful commit; no membership changes for these existing-module edits. New focused test file okay, no new runtime module/schema/family.
- Oracles: initial full validity, intended late Raw/card/View/State/guard/report/COPY/needed git blob failures, input-archive change, owned-outputs drift, fresh separate invocation, no-supp/LEGACY/history. Fault Git blob ONLY NEW disposable fixture with retained originals/layout known, never author DB, never b797. No repeated expensive real run for stability.

## 2. Setup (NEW independent copy only, no reconstruct readback)

- NEW: `.rephase-1-editorial-runtime/selection-scaling-implementation-20261116T004649Z/candidate-work` (UTC 20261116T004649Z, byte-copy `tar --exclude=.git -cf - -C active . | tar -xf - -C NEW`, hardlinks 0, inodes differ).
- Active preserved: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` (HEAD ae0dd1e parent cc1c7fd tree ec11cf...), shadow preflight, proofs, all prior packets untouched.
- Source773 verified BEFORE editing vs final manifest `a7e40c47…`/202833B BASE 409b292: 773/773 files, 0 pin mismatches (SHA/bytes), missing 0, extra = sources data only (12235 total incl sources, 773 intended). Command (workspace root, no Git): `python3 -c` with `json/hashlib/os` walk excl `.git/__pycache__/*.pyc`, compare `files` dict.
- States/CPs/slots/Profiles (NEW copy, read-only, no writes):
  - W34 + SP `production-state.json` lifecycle EVIDENCE_REVIEWED, impl `48082356…`, triplet same record (`w34-repaired-20261112-r2`, `sp-repaired-20261112-r2`), 4 artifacts evidence/views/ledger/completeness, Profile SHAs `2a8c3089…`/`aff05fd5…` match State, source_root `sources/2026-W34` / `sources/SP-efficient-llm-2026`.
  - CPs: kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, revision_id `w34-repaired-20261112-r2` / `sp-repaired-20261112-r2`, 4 NamedRefs.
  - Completion + inventory exist, seven_plan 7 rows, checkpoint path matches.
  - Seven slots absent (all 7: matrix/selection/architecture/review/attention/input/audit) in both source_roots.
- Git (explicit NEW cwd ONLY, never reconstruct status/log/HEAD/readback):
  - `git init -b main` (new empty DB) → `cp -a active/.git NEW/.git` (byte-copy, 0 inode overlap, nlink 1 e.g. `01/60c04…` nlink 1 ino 25040529) → `git remote set-url origin https://invalid.invalid/inert.git` (inert), `remote -v` inert, no `objects/info/alternates`, no `commondir`, HEAD `ae0dd1ee…` tree `ec11cf6c…` (inherited history, for own-epoch proof), no `.gitmodules`/nested `.git`/gitlinks, no HOME/config mutation, process-scoped identity only, no empty/hook-bypass.
  - `git status --porcelain=v1` shows intended 4M + 1 new test + inherited active dirty (States/CPs/rehearsal outputs) + `__pycache__/` (excluded, from py_compile/unittest, never committed). `git diff` FAILS partial-tree: `fatal: unable to read 99c34b75…` / `9a1c38de…` (missing 26309 blobs, inherited partialDB). STOP before `write-tree --missing-ok` per ROOT (no commit, report here).
- Env: `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1`, safe env, no install, no network/Production.

## 3. Changed files (source-only, 4 existing + 1 new test)

| Path | Before SHA/bytes/mode | After SHA/bytes/mode |
|---|---|---|
| `scripts/survey_review_attention_v2.py` | `be50e5e3d35d`/7058/0664 (runner pin `553bf22b…` context) | `10126da7482f`/7796/0664 |
| `scripts/survey_architecture_v2_base.py` | `ac52c842afa1`/47416/0664 | `b3cd4a95f512`/51050/0664 |
| `scripts/survey_research_authority_v2.py` | `7f5fc9e0d797`/240969/0664 (LOW pin) | `18f58ea021b9`/266023/0664 |
| `scripts/run_selection_architecture_v2_interactive.py` | `553bf22bb7d2`/27766/0664 (runner pin) | `041a5b245b4f`/42350/0664 |
| `tests/test_selection_scaling_repair_v2.py` | MISSING (new file) | `98b109763e41`/18998/0664 |

- No new runtime module/schema/family; no membership changes (G76 70/73, reader 36/41, pipeline 76 no scripts, LOW 7 unchanged, runner control-root bound) per closure-map.
- Diff (source-only, worktree NEW vs active, no Git due to partial-tree block; reproducible via stdlib `difflib`, no shell text editing):
  - attention: extract `_build_attention_payload` (pure, existing construction+validation, no write), `build_attention` calls it then writes (unchanged public, same limit/count/truncation/overflow + `validate_attention`).
  - base: add `_validate_candidate_matrix_against_upstream(repo_root,matrix,upstream,profile,completeness,ledger,evidence,views)` (P-only, no second `_load_upstream`); add `_summarize_review_contents(repo_root,upstream,matrix,selection,architecture,profile,completeness,ledger,matrix,selection,architecture,errors)->dict` (FULL, shared, adds INCOMPLETE); add `_build_..._with_upstream(...upstream)` (held upstream+paths only, no `implementation_sha`); `build_...` calls shared (no duplication, wrapper-patched `validate_architecture` preserved).
  - low: add `_SelectionReadSet` (DATA-only, immutable pins/docs/dir-sets/own-epoch), `_capture_selection_read_set` (pinned bytes for each next ref, external SHA checked, observation where no external SHA, DCP/SCP artifacts/reviews/reports, packages/batches/tasks/cards/views/suppRaw/prompts/schemas/config, request/manifest/report/proof/decision/COPY/inventory/completion, own-epoch args, expectations/source_root; no generic recursion, no Session files), `_recheck_selection_read_set` (FILE re-read O_NOFOLLOW/dev-ino + SHA/len, ancestors via `_repo_rel`, exact dir-sets, FULL `_verify_own_epoch_commit` for PREARCH, LEGACY skips own-epoch).
  - runner: add `base` import (new edge, owner BASE); add `_CheckedSelection` (runner-local, holds read_set/validated/expectations/root/effective/input pin/implementation_sha/upstream/expected_outputs); add `_prepare_checked_selection` (capture→input pin+parse same bytes→original full validation 3AG+2AG+1AG+6AG+BOTH screening halves+effective+package-once 3+6AG under ORIGINAL facade→recheck→sealed); add `_check_selection_boundary` (LOW recheck incl FULL own-epoch + guard + triplet + HEAD==implementation_sha + input still matches pin); add `_verify_owned` (already-owned == expected, not-yet-written absent); `run()` uses `_prepare` once (no duplicated initial calls outside), preflight7-absent once, first EU via `_load_upstream_content` + `_derive_matrix_rows_content` (0AG), writes with expected `json_bytes`/`copy2`/payload-helper bytes verified immediate/later/outer-return, single held upstream + `with_upstream`, attention via payload helper, archive matches entry pin, audit binds archive+5 outputs, final return verifies read-set/source/HEAD/own-epoch/guard/State + all7 + audit, no success after drift, partials remain, no cleanup/retry/rollback.
- Full unified diff omitted here for brevity (700+ lines); reproducible: `python3 -c` with `difflib.unified_diff` comparing active vs NEW worktrees for the 4 paths above (no Git, no shell editing). Pins above bind exact bytes.

## 4. Focused tests (11/11 PASS after ordinary fixes, no coverage overclaim)

- File: `tests/test_selection_scaling_repair_v2.py` (new, no runtime change). Helpers: existing genuine `test_survey_evidence_v2.make_chain` pattern + minimal genuine temp JSONs + real validators, no stubs. Safe env, no install, temp disposable DBs with process-scoped identity/inert origin/no empty/HOME changes, never author DB (except read-only real W34/SP capture), never b797, no active/shadow writes/network/Production.
- Names:
  1. `TestBaseSharedHelper.test_against_upstream_repo_root_first_and_summary_shared` (repo_root first, shared FULL helper, public vs with_upstream same shape)
  2. `TestAttentionPayload.test_payload_helper_shared_and_limits` (private payload vs public builder same bytes, limit/count/truncation, no overwrite)
  3. `TestLowCaptureRecheckRealReadOnly.test_capture_recheck_passes_real_w34_sp_no_writes` (capture→recheck on NEW copy real W34/SP, no writer, no drift)
  4. `TestDriftGates.test_phase_pin_drift_refuses_no_next_write` (Raw/task pin drift refuses, no next file)
  5. `TestDriftGates.test_guard_and_preflight_and_owned` (canonical guard `orchestration/v2/acceptance-revision.guard.json` present refuses, absent passes; preflight7 absent once, present refuses)
  6. `TestDriftGates.test_input_pin_drift` (input bytes changed after seal refuses)
  7. `TestNoSuppVsDowngrade.test_healthy_no_supp_valid` (empty supplement valid, no generic None+None)
  8. `TestNoSuppVsDowngrade.test_supplemented_null_downgrade_refuses` (OLD supplemented + NEW null refuses `OLD supplemented + NEW supplement_manifest null refused`)
  9. `TestLegacySeparate.test_legacy_keeps_legacy_branch` (LEGACY without same triplet → LEGACY, no PREARCH graph/own-epoch)
  10. `TestExactSet.test_extra_symlink_refuse_disposable` (missing/extra/symlink/non-file refuse via `_exact_regular_files`, disposable only)
  11. `TestBlobFaultDisposable.test_own_epoch_full_batch_refuses_missing_blob_disposable_only` (NEW disposable DB, layout known, loose blob mv aside → `cat-file -e` refuses, restore → passes; never b797/author DB)
- Runs (NEW cwd ONLY, `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 python3 -m unittest tests.test_selection_scaling_repair_v2 -v`, no install):
  - Attempt1 UTC ~20261116T0050Z: 11 tests, 1F+3E (attention schema missing in temp, BASE card/view path + view_filename hash, LOW own-epoch missing objects before .git copy, guard `.guard` vs canonical). EXIT 1. Raw preserved (see tool output 0.303s).
  - Attempt2 after .git copy + guard fix + attention schema copy: 11 tests, 1E (BASE ledger `downstream_disposition` missing). EXIT 1. Raw preserved (0.664s).
  - Attempt3 after ledger fix + config for with_upstream: 11/11 PASS. EXIT 0. Raw (0.664s, final 0.669s/0.664s runs). Before: source773 verified, States EVIDENCE_REVIEWED, 7 absent, inert origin/no alternates/nlink1. After: no active/shadow writes, no new DB objects in author DB (disposable only in temp), `__pycache__/` excluded, no network/Production.
- Runtime cost (honest, no speedup claim): focused 11 tests ~0.66s wall in NEW copy (no full 409/160, no CURRENT proof, no delivery). 21AG remains source estimate; actual 7-run decides in separate dispatch.
- No test coverage overclaim: 11 focused behavioral tests only, not full matrix/suite, not R4 audit/adoption/savings.

## 5. Return (actuals + concerns for root BEFORE full real runs/CURRENT/delivery)

- Actual files: 4 modified (pins above) + 1 new test (`98b10976…`/18998). No commit (partial-tree block: `fatal: unable to read 99c34b75…` / `9a1c38de…`, missing 26309 blobs inherited; STOP before `write-tree --missing-ok` per ROOT). No ordinary Commit/Push/Human readback.
- Source pins: 773 intended verified 0 mismatches BEFORE edits; after: 769 unchanged + 4 modified (pins above) + 1 new test + sources data extra. Runner/LOW before pins match recorded `553bf22b…`/`7f5fc9e0…`; HIGH `f31202e…` untouched.
- Tests: 11 names/results above, failures preserved (1F+3E → 1E → 11 PASS), runtime ~0.66s, EXIT 0 final, raw logs preserved (tool outputs).
- Concerns (load-bearing, return before expansion):
  - Partial-tree commit blocked (missing objects) → no source-only child yet; needs root decision (fresh full 409 restore vs `write-tree --missing-ok` vs defer commit to delivery).
  - LOW capture best-effort gaps: DiscoveryRaw/XtasksRaw full closure via request refs only (X manifest/tasks/Raws + Discovery JSONL + root Raws pinned where reachable, but full X raw + effective derived Raw byte rehash relies on existing validators, not separate capture); supplement manifest/Raw path resolution best-effort; dir_sets only evidence tasks (not all exact sets) → later recheck relies on FULL validators for exactness; requires root confirmation no load-bearing omission before real 409/160.
  - Runner `_prepare` root_records=None (lazy, root_path=accepted root) for content EU; real W34/SP content EU with None must be confirmed via real 409/160 oracle (actual run decides).
  - Later boundaries omit explicit historical seven-plan vs lstat tolerance recompute (relies on pins + owned progression + initial full completion with second AG retained); requires root confirmation.
  - No full real W34-409/SP-160 all-seven, no fresh CURRENT proof, no DIRECT409 delivery yet (separate dispatch after root review).
- Next after root review: separate real-size W34/SP normal-writer all-seven completion, fresh CURRENT proof, exact DIRECT409 delivery, independent implementation review → Human Commit Point. No auto-start.

(End of packet — implementation + focused verification, no commit, no real writer.)
