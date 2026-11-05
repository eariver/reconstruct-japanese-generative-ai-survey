# W34 dispose+run r3 — single-invocation execution report (STOP at first failure)

Root §7 authorized ONE invocation of `w34-operator-dispose-run-r3-20261104.py`
`48be5879...`, launcher `46f90f21...`, READY `473bf85b...`, manifest
`cede7e46...`, helper `2c6f...`. Pins verified before execution (ALL_OK).
No network/Production/reconstruct readback; clean GIT env; bytecode disabled.

## Invocation (exactly once; prior 126 was shell exec-bit failure before tool)

- argv: `PYTHONDONTWRITEBYTECODE=1 notes/.../w34-dispose-run-launcher-r3-...sh --retention-dir notes/.../retention-W34-dispose-20261105T003915Z --ready-path notes/.../retention-W34-.../READY.json --manifest .../w34-prepare-expected-manifest-20261104.json --expected-tool-sha 48be... --expected-ready-sha 473bf85b... --expected-manifest-sha cede7e46... --repo-root .rephase-1-editorial-runtime/.../candidate-work` (via `bash` launcher; direct exec bit absent)
- cwd `/home/eariver/git/reconstruct-japanese-generative-ai-survey`, PID 73306/73308, start `2026-11-05T00:39:50Z`, end `2026-11-05T00:40:22Z`, exit **1** (tool `exit 2` path raised as launcher `exit 1`? raw: tool traceback + `PREFLIGHT_REFUSED`? recorded exit 1 from launcher wrapper; numeric exit preserved in raw files)
- env: `HOME=/home/eariver` unchanged, `PYTHONDONTWRITEBYTECODE=1`, no `GIT_*` overrides, no gitconfig change
- stdout `w34-dispose-run-stdout-20261105T003915Z.txt` (launcher argv/cwd/HOME/timestamps), stderr `w34-dispose-run-stderr-...txt` (tool traceback, 27 lines)
- Git: explicit isolated e84 only via `core.repository_commit_sha(repo)`; no `git -C .`

## Outcome: STOP, no retry, partials preserved (no edit/fix/restore/cleanup)

- P1-P5 passed: strict State CAND, tree 1782→1781→1780, all771 (770+test diff), staged `1ea562...` pinned, supplement428 validated, retained 409-task package validated, checkpoints/accepted/preserved pins, SP snapshot OK.
- P2 backups (O_EXCL 0664, readback): `materiality-ledger-v2.json` 186202B `76ac53...` + `profile-completeness-v2.json` 71532B `93dbef...` + `retention-manifest.json` in `retention-W34-dispose-20261105T003915Z/` (3 files; no journal/DISPOSE_RUN/FAILURE — see bug below).
- P3 ledger unlinked (absent verified), P4 completeness unlinked (both absent verified), P5 post-disposal 1780 verified, State unchanged CAND.
- P6 ONE `rn.run` FAILED before any Evidence accept (first failure, STOP):
  `w34-event-c001: verification input must cover exact task targets: missing=['Release confirmed; exact Aug 14 ... regardless.'] extra=['Content: GLM-5.3 ...', 'Week placement: ...']`
  r2 split its verification targets; tasks (from screening decisions) still carry the single old target. Pre-disposal `validate_interactive_input` does not check target strings (only ids/bindings), so P1 passed and the mismatch surfaced in `_build_card_core` during run.
- Secondary wrapper defect: `FAILURE.json` write failed (`dest must be absolute: notes/.../FAILURE.json` — relative path passed to `_stage_bytes_exclusive_under`). No FAILURE.json preserved; partials are the 3 retention files above + active tree state below. No auto-retry/restore/cleanup performed.

## Run completed vs wrapper validation (no semantic PASS)

- Wrapper pre-disposal validation: PASSED (State/tree/source/supplement/package/pins).
- Normal run: DID NOT COMPLETE (failed during card build, before Evidence/Views/Ledger/Completeness accept). No new accepted dirs, no Ledger/Completeness regen.
- No `EVIDENCE_REVIEWED`/Selection/Architecture, no semantic publication PASS.

## Post-observation (stdlib, actual files)

- source771: **770 ok +1 known test diff** (`d486809c/91561` vs `7b862305/106616`), 0 missing
- W34 live: **1780 files / 80 dirs** (1781 baseline +1 staged −2 disposed), 0 unexpected; staged `interactive-evidence-w34-r2-...json` 1580317B `1ea562...` preserved; old accepted `bf208...` + `f744...` unchanged (1+1); exact2 both absent (backed up); State `7e6a50c2...` + Profile `2a8c30...` bytes unchanged CAND
- Staged input actual counts: **409 records (363 PARTIAL / 38 VERIFIED / 8 NEEDS_MORE)**, 3 obligations (LIMITATION/LIMITATION/SATISFIED)
- SP completed outputs unchanged: preflight READY `c7cd05a8...`, dispose `DISPOSE_RUN.json` `cf26a23c...` still present; no SP invoke
- Counts above read from actual files, not summaries.

## Artifacts (NEW packet, full programmatic hashes in manifest)

- `retention-W34-dispose-20261105T003915Z/{materiality-ledger-v2.json,profile-completeness-v2.json,retention-manifest.json}` + stdout/stderr + this report + artifact manifest below.
- Next review needs: (1) contract decision on chronology representation within exact task-target coverage (split input targets break `_build_card_core` exact match for c001 and by same logic c002/c020/c022/c024/c039/c045/c066/c099-102 — tasks carry screening targets, inputs must cover them exactly); (2) fix `FAILURE.json` relative→absolute packet path; (3) new bounded observation/decision for already-removed exact2 (backups preserved, originals absent — no auto-restore); (4) independent re-review before any new dispose/run auth. No State advance, no Selection, no SP mutation.
