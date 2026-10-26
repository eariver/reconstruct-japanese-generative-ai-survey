# Affected regressions — TEST Co-Worker parallel (no product runtime changes)

2026-10-25. Root Human `f84fcf5`. Code FROZEN actual candidate 740 = fixed739 + edpub `85814124` + new archive test `5e5a`. H `6fe86e`, P1 `825dba`, PUB `3f4039`, S `20f63e`, HIGH `9a0469`, Reader `098a2c`.

## 1. Authority and source

- Read `AGENTS.md` Re:Phase-1, contract `478f0051` §§9/11, precode `7d7d5a45` §6, `final-integration-input.md`, `integration-repair-input.md`, `integrated-source-freeze.md`, `archive-compatible-input.md`, `evidence-reconciliation.md`, `astra-integration-corrections.md`.
- INPUT (Freeze worker, read-only): `.rephase-1-editorial-runtime/versioned-renewal-archive-input-20261025T133248Z/snapshot-work` HEAD `409b292`, tree `8ce36998`, 740 files, `dst-hash-intended` `4e2783fb…` (740 lines). Reconstruct HEAD `f84fcf5` clean pre/post, candidate HEAD `409b292` unchanged.
- NEW independent TEST SOURCE (owned, before authority): `.rephase-1-editorial-runtime/versioned-renewal-affected-regress-20261025T143000Z/test-source` HEAD `debd16c9da0e8e533968c2926048b336eadb7070` (parent `409b292`), message `TEST-ONLY: complete 740 SOURCE before authority`. Status clean, `ls-files` 32206 total (full index 32155+51), intended 740 all tracked missing 0. `.git` 83 files, no `objects/info`/`alternates`, inert `example.invalid`, `dev:ino` disjoint, `nlink==1`. SRC==DST SHA 740/740. No reconstruct/candidate commits, no network/pip, no old-runner exec, no cleanup (140000Z mkdir-order FAIL, 141000Z hash-format FAIL, 142000Z total-ls-files FAIL preserved).
- Pins (TESTSRC, `hashlib`): H 288349B `6fe86e…`, P1 158652B `825dba…`, PUB 125977B `3f4039…`, S 127981B `20f63e…`, HIGH 202862B `9a0469…`, Reader 46395B `098a2c…`, edpub 264756B `85814124…`, archive test 4521B `5e5a0b…`, `.latexmkrc` 218B `18199fd8…`.
- TMPDIR workspace-local `…/affected-regress-…/tmp`, fresh child per module, exact SOURCE pin raw before/after (HEAD `debd16c9` both). No `/tmp` EDQUOT for own children; P3S helper itself uses `/tmp/opencode` fallback (see §3).

## 2. Copy-helper inspection (actual source)

- P1 `test_survey_editorial_correction_proposal_v2.py:81-109`: `ls-files -- config schemas scripts templates prompts docs data tests` + explicit `UNTRACKED_SOURCES` 10 old + explicit `.latexmkrc` copy. From TESTSRC (740 tracked) sees renewal (under `schemas/scripts/tests`) as tracked; `.github` still missed (not needed for P1). Complete for P1.
- P2R `test_survey_editorial_retention_v2.py:67-94`: prefix includes `.github`, + `UNTRACKED_SOURCES`+`P2R_EXTRA` + explicit `.latexmkrc`. Complete for P2R when run from TESTSRC.
- P3S `test_survey_editorial_staged_source_v2.py:88-110`: prefix includes `.github`, `UNTRACKED_P3S_SOURCES` includes `.latexmkrc` + old/new P1/P2V/P3S but NOT renewal 10. From TESTSRC renewal tracked via `ls-files`, so complete. Uses `P3S_DURABLE_OUTDIR` else `/tmp/opencode` (EDQUOT risk, not workspace TMPDIR).
- R1 `test_survey_weekly_mechanical_refresh_v2.py:71-76`: prefix `config schemas scripts templates prompts docs data` (omits `.github/tests/.latexmkrc`), NO explicit `.latexmkrc` copy. Fixture always misses `.latexmkrc` → `current_closure` fails `.latexmkrc missing`. Requires TEST-ONLY patch (add `.latexmkrc` explicit copy like P1) with root approval; NOT applied here (no silent runtime weakening).
- Longform/weekly derivation helpers use same omit-prefix without `.latexmkrc` (e.g. `test_survey_longform_derivation_v2.py:105`, `test_survey_increment_b_weekly_derivation_v2.py:53`). Same patch class needed if used for anchor.
- New renewal tests: `test_versioned_renewal_history_phase_h.py:100-116` walks worktree (complete, excludes `.git/__pycache__/*.pyc`), commits BEFORE authority — correct. `test_versioned_renewal_source_phase_s.py:6-7` same. `test_versioned_renewal_history_author_h_20261025.py:328-331` includes `.latexmkrc` explicitly in `_src_paths`. Good.
- Signature check (actual APIs): `weekly.load_derivation(root,state_path,authored_path,pending_basis=None)` vs `longform.load_derivation(root,state_path,authored_path)` + `load_derivation_for_readback` same 3-arg. No `old_lf` 4-arg call found in current helpers; all call sites match current signatures (checked via `ast`). No silent signature change.

## 3. Results (cwd=TESTSRC FIXED; first wrongcwd preserved in `first-run-wrongcwd/`)

Previous 120 green at older code NOT transferred. All below at 740 TESTSRC HEAD `debd16c9`, fresh `python3 -m unittest`, timeout 1200s, `PYTHONDONTWRITEBYTECODE=1`, no pip/network.

PASS 18 modules (168 methods + skips noted):
- `test_editorial_renewal_archive_correction_20261025`: Ran 5 OK (0.2s)
- `test_editorial_renewal_p1_dispatch_20261025`: Ran 4 OK (0.7s)
- `test_versioned_renewal_high_phase`: Ran 12 OK skipped=3 (0.4s)
- `test_versioned_renewal_history_author_h_20261025`: Ran 5 OK (8.2s)
- `test_versioned_renewal_source_author_s_f1f2f3_20261025`: Ran 11 OK (130s)
- `test_versioned_renewal_operation_correction_b1b2b3`: Ran 19 OK (0.02s)
- `test_versioned_renewal_history_perf_batched_20261025`: Ran 3 OK (9.5s)
- `test_versioned_renewal_history_traversal_opt_20261025`: Ran 4 OK (20.5s)
- `test_survey_dm004_release_validate_state_v2`: Ran 7 OK (38.9s) — DM004 current
- `test_survey_agent_control_v2`: Ran 5 OK (0.7s) — public State
- `test_survey_publication_set_v2`: Ran 18 OK (1.6s) — Candidate/set
- `test_survey_reader_surface_gate_v2`: Ran 27 OK (2.5s) — Reader/Gate
- `test_survey_quality_v2`: Ran 10 OK (0.18s) — quality
- `test_survey_publication_v2`: Ran 8 OK (2.2s) — Gate/Candidate
- `test_survey_stage_validation_v2`: Ran 3 OK (0.08s) — Preview/stage
- `test_survey_profiled_freeze_v2`: Ran 4 OK (0.04s) — profiled Freeze
- `test_survey_editorial_correction_proposal_v2`: Ran 9 OK (288s) — P1 current
- `test_survey_editorial_current_authority_v2`: Ran 14 OK (533s) — P2V current

FAIL 6 modules (preserve first fail, no blind pre-existing claim):
- `test_versioned_renewal_history_phase_h`: Ran 2 FAILED errors=2. Both `HISTORY_DIGEST_MISMATCH: editorial ancestor scope review_sha256 mismatch (not canonical excluding itself)` at `history_v2.py:1959 _verify_self_digest` via `2052 _verify_editorial_ancestor`. Test builds scope `{"review_sha256":"a"*64}` dummy, new H requires canonical self-digest. Product stricter than test fixture. Proposed: update TEST-ONLY fixture scope to compute real `review_sha256` via canonical (no runtime weakening), or root confirms H strictness. File: `tests/test_versioned_renewal_history_phase_h.py:289,500`, code: recompute `scope-review.json` digest.
- `test_versioned_renewal_source_phase_s`: Ran 18 FAILED failures=4. 2× `finalize must return receipt` — code returns `receipt_path` not `receipt` (`_run_u:904`, fin keys show `receipt_path/build_record_path/...` + `disposition REUSED_TARGETS`). Test expects `receipt` key. Proposed TEST-ONLY fix or HIGH contract clarification: `scripts/survey_versioned_renewal_v2.py` finalize return keys vs test `tests/test_versioned_renewal_source_phase_s.py:904`. 2× scope mutation expects `SCOPE_WRONG_BEFORE` but gets `HISTORY_DIGEST_MISMATCH … before-reader must equal proposal basis` (`:365`). Product maps to digest mismatch, test expects specific code. Needs root code decision, not silent edit.
- `test_versioned_renewal_reader_f4_20261025`: Ran 7 FAILED failures=1 errors=1 skipped=2. `BASIS_CURRENT_TOOL_DRIFT: loaded history module wrong root: …/test-source/scripts/…` vs fixture `high24 …/renewal-weekly` (G2+ HIGH `1620b92` vs TESTSRC HIGH `9a04`). Detached CURRENT-tool check correctly refuses cross-root. Test expects PASS using high24 fixture with TESTSRC tools. Needs isolated fixture at TESTSRC epoch, not high24 reuse. No runtime weakening.
- `test_survey_editorial_retention_v2` (P2R): Ran 25 FAILED failures=1. `test_replacement_owned_file_midcapture_refuses` — `RetentionError FILE_REPLACED not raised` (`:1544`). Single midcapture replacement oracle not hit at 740. Parent controls (24 pass) preserved. Needs root triage (timing vs product).
- `test_survey_editorial_staged_source_v2` (P3S): Ran 26 FAILED failures=26. All `RUNTIME_BINDING_MISSING: S2 module not loaded: scripts/survey_discovery_v2.py` with `durable_dir /tmp/opencode/…`. Fixture uses `/tmp/opencode` fallback (ignores workspace TMPDIR), plus possible incomplete S2 binding at 740. First fail `test_o10_same_inode_vs_new_inode:1774` via `_materialize:1158`. Needs TEST-ONLY `P3S_DURABLE_OUTDIR=workspace-tmp` + S2 binding check; no runtime weakening without root.
- `test_survey_weekly_mechanical_refresh_v2` (R1): Ran 34 FAILED errors=29 (5 pass implied). All errors `ValueError: .latexmkrc missing …/tmp/…/jgas-weekly-mechanical-r1-…/.latexmkrc` via `weekly.current_closure:684` ← `survey_weekly_semantic_publication_v2.py:118`. Helper prefix omits `.latexmkrc` with no explicit copy. Requires TEST-ONLY patch adding `.latexmkrc` explicit copy (like P1:68-109) with root approval; NOT applied. Preserve first fail.

SKIPPED 2 modules (honest, no certify):
- `test_versioned_renewal_freeze_transitive_correction_20261025` (6 methods) + `test_group_c_editorial_consumers_v2` (9 methods): pytest-style bare functions, `unittest` 0 tests exit 5. `pytest` absent, `pip` NOT used, no network. Not product PASS/FAIL. First wrongcwd exit 5 preserved.

No global/continuous guard certified. All pins HEAD `debd16c9` before/after per module. Test-owned tmp under workspace `…/tmp`, processes reaped (timeout 1200s, no hangs; P1 288s, P2V 533s, P2R 685s, P3S 796s within bound). No candidate/reconstruct mutation, no GIT sharing.

## 4. TEST-ONLY repair proposal (for root approval, not applied)

- R1 helper `tests/test_survey_weekly_mechanical_refresh_v2.py:71-76`: add explicit `.latexmkrc` copy after `ls-files` loop (mirror P1 `recipe_src/dst` + SHA check), include in `git add -A` before commit. No runtime validator change.
- P3S runner: export `P3S_DURABLE_OUTDIR=$TMPBASE/p3s-durable` in NEW external runner (no code change) to avoid `/tmp` EDQUOT; plus verify S2 binding at 740.
- History PhaseH fixture scope: compute real `review_sha256` canonical instead of `"a"*64`.
- Source PhaseS finalize key: align test `receipt` vs code `receipt_path` (root decides contract).
- Reader F4: use TESTSRC-epoch isolated fixture, not high24 cross-root.
- If test-source edits on candidate required, will return exact files/code; none done here.

No whole-unit/independent PASS, no CommitPoint.
