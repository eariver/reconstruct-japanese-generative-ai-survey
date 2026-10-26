# R1×2→editorial→renewal anchor — TEST Co-Worker blocker (NOT proven)

2026-10-25. Root Human `f84fcf5`. Required: real Weekly initial canonical inputs under old 721 source, actual R1 refresh TWICE (meaningful tool-source comment commits, canonical R1 only weekly derivation), latest legacy anchor=r2 cumulative original checkpoint; then real R3 editorial activate (full tool source at actual R3 old 721, code control R1-only changes); then overlay new 740 SOURCE commit → renewal U typed history anchor unchanged. Real C build R3 once TL2026 local tools, explicit synthetic reviews, old R1 runs PUBLIC not fabricated. Need 2 only, not 32.

## 1. Attempted identification (read-only, no authority)

- Old 721 base available: `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly` HEAD `721a04d`, tree `ac7cb0bd`, 850 worktree files (721 + old E untracked `??` 127+2 Weekly, 136+2 Longform), status tracked clean. Real ancestry `721a04d←00397c3←ce90246…`, inert origin, no alternates. Old E live/COPY, NOT required at tool commit per root map.
- New 740 TEST SOURCE ready: `…/affected-regress-20261025T143000Z/test-source` HEAD `debd16c9` (parent `409b292`), 740/740, hashes H6fe/P1825d/PUB3f/S20f/HIGH9a/Reader098/edpub85814124/archive5e5a (see affected-regressions).
- Current test library: `test_survey_weekly_mechanical_refresh_v2.py` (R1, 34 methods), `test_survey_editorial_*` (P1/P2R/P2V/P3S), `test_versioned_renewal_*` (H/S/HIGH). No old-runner exec.

## 2. Actual step blocker (anchor NOT executed, NOT proven from shape)

R1 helper blocks fresh R1×2 at first step; P3S/history also block editorial/renewal. No authority generated, no fixture commits for anchor, no GIT sharing, no cleanup.

- **R1 blocker (load-bearing)**: `tests/test_survey_weekly_mechanical_refresh_v2.py:71-76` prefix `config schemas scripts templates prompts docs data` omits `.latexmkrc/.github/tests` with NO explicit `.latexmkrc` copy. Affected-regressions at 740: Ran 34 FAILED errors=29, all `ValueError: .latexmkrc missing …/jgas-weekly-mechanical-r1-…/.latexmkrc` via `weekly.current_closure:684`. Fixture cannot build real Weekly VALIDATED_DRAFT baseline, so genuine R1 comment-commit TWICE impossible. Required TEST-ONLY patch (explicit `.latexmkrc` copy like P1:103-109) needs root approval; NOT applied (no silent weakening). File: `tests/test_survey_weekly_mechanical_refresh_v2.py`, code: add `recipe_src=workspace/“.latexmkrc”` copy + SHA check before `git add -A`.
- **P3S blocker**: `tests/test_survey_editorial_staged_source_v2.py:237-243` fallback `Path(“/tmp/opencode”)` ignores workspace TMPDIR (EDQUOT risk). Affected-regressions: Ran 26 FAILED failures=26 `RUNTIME_BINDING_MISSING: S2 survey_discovery_v2.py` + `durable_dir /tmp/opencode/…`. Editorial R3 materialization cannot proceed without `P3S_DURABLE_OUTDIR=workspace-tmp` + S2 binding triage. File: same test + `scripts/survey_editorial_staged_source_v2.py` S2 binding.
- **History blocker**: `test_versioned_renewal_history_phase_h` Ran 2 errors=2 `HISTORY_DIGEST_MISMATCH scope review_sha256 dummy a*64` (new H6fe strict canonical vs test dummy). Renewal U history cannot be proven until fixture scope uses real digest. File: `tests/test_versioned_renewal_history_phase_h.py:289`.
- **Source/Reader blockers**: `test_versioned_renewal_source_phase_s` 4 failures (`receipt` vs `receipt_path`, `SCOPE_WRONG_BEFORE` vs `HISTORY_DIGEST_MISMATCH`); `test_versioned_renewal_reader_f4` `BASIS_CURRENT_TOOL_DRIFT` cross-root high24 (`1620b92`) vs TESTSRC (`9a04`). Renewal U finalize/readback needs root code/test alignment + isolated TESTSRC-epoch fixture.
- **Build**: Real C build R3 once TL2026 local tools at `/tmp/opencode/jgas-texlive-…` (pdfTeX 3.14, latexmk 4.88) NOT on PATH, NOT run here (no PDF per freeze discipline). Using `/tmp` risks EDQUOT; workspace-local TeX not set up. No synthetic reviews generated for anchor.

## 3. Anchor fields (NOT proven, for root ordering)

- `old_source`: `721a04d85532d7855f3e54cc411f5847c787726e` (R7b 721, bootstrap-weekly/longform)
- `new_source`: `debd16c9da0e8e533968c2926048b336eadb7070` (TEST-ONLY 740, parent `409b292`)
- `r1_commits`: NONE (blocked before first R1; need 2 meaningful `survey_weekly_derivation_v2.py` comment commits)
- `latest_legacy_anchor`: NOT established (need r2 cumulative original checkpoint from R1×2)
- `editorial_r3`: NOT activated (need P1/P2R/P2V/P3S50 at old 721 + real 5-page PDF + finalize/activate prePreview)
- `renewal_u`: NOT activated (need overlay 740 SOURCE commit → U typed history, anchor unchanged)
- `c_build`: NOT done (need real TL2026 PDF + postrender reviews)
- `reviews`: synthetic only (no genuine approval); production semantic NO-GO retained.

## 4. Test-owned temp/process status

- No anchor fixture DB created, no anchor commits, no authority, no `/tmp` writes for anchor. Affected-regressions tmp `…/affected-regress-…/tmp` clean, TESTSRC HEAD `debd16c9` unchanged, SRC `409b292` unchanged, reconstruct `f84fcf5` unchanged. Raw: affected-regressions `run-*-stdout/stderr/exit + pin-before/after`; first wrongcwd preserved.
- If too heavy, this IS the blocker return — do NOT declare anchor proven from shape unit. Root to order TEST-ONLY `.latexmkrc` patch + `P3S_DURABLE_OUTDIR` + history/scope alignment before R1×2 retry.

No whole-unit/independent PASS, no CommitPoint.
