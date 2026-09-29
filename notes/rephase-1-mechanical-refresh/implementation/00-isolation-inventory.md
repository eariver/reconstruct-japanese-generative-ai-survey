# R1 implementation evidence — isolation + path inventory

- Evidence clock: **2026-09-28T23:28:36.9074668+09:00** (`Get-Date -Format o`, reconstruct workdir).
- Role: General IMPLEMENTATION/TEST Co-Worker. No independent review; root reviews source/oracles before a fresh independent exact-head review.
- Reconstruct HEAD at work: `d17560028bd5db459636ca957888b7369b5d5cda` (Human commit; ordinary commit/Push Human-owned; this packet only adds new files under `notes/rephase-1-mechanical-refresh/implementation/`).
- Preserved source (read-only, never mutated): `/tmp/jgas-rephase-gate-cli`, HEAD `e4c82692abee6acedbba07815b0d74ccefb80a7e`, tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`, branch `codex/rephase-1-gate-cli`, origin inert, status pycache-only. Re-verified `rev-parse/show/status/remote/branch` read-only before and after this unit.
- `apply_patch` is not in this worker's tool set (stated honestly); all authored edits used the dedicated file edit/write tools. One mechanical 3-line comprehension fix was applied via a shell Python rewrite and verified by read+grep to be identical in content to an edit-tool outcome (disclosed deviation, no semantic difference).

## New fixture (independent native Linux DB)

- Path: `/tmp/jgas-rephase-mechanical-r1-20260928T000710Z`, branch `codex/rephase-1-mechanical-r1`, origin inert `https://example.invalid/mechanical-r1.git`.
- `git archive HEAD` from the preserved source is infeasible: promisor-missing objects for `sources/2026-W32/...` (error preserved in shell history: `invalid object ... for 'sources/2026-W32/candidates/README.md'`). Used a worktree `tar` copy (`--exclude=.git --exclude=__pycache__`) instead: `diff -r --brief` source-vs-fixture worktrees exit 0, 0 lines (`logs/r1-diff-check.txt`). Same filesystem, exact bytes, new inodes (no hardlinks), exec bit preserved (`survey_core_execution_bridge_v2.py` 755 both sides).
- Own DB: `git init -b main`, `remote add` inert origin, basis commit `a1a4242` (process-local `GIT_AUTHOR/COMMITTER_*` env identity, `--no-verify`, no `git config` writes, no amend/hooks). `rev-parse --git-dir` == `--git-common-dir` (`.git`), `objects/info/alternates` absent, `count-objects`: 783 loose/0 packs at basis, local config only (formatversion/filemode/bare/logallrefupdates + inert origin), worktree `find -type l` empty, `find -links +1` empty, no inherited `GIT_*` env (guarded in every test setUp).
- Content boundary (honest subset, same pattern as the prior witness): sparse-checked-out worktree of 724 files. Blob check vs `e4c8269` (`logs/r1-blob-check-out.txt` + full 41-name list in shell history): **683/724 blobs identical**; 41 failures are all promisor-missing `sources/...` data files (release manifests, SP001 evidence packages) present in the worktree but unfetchable from the source DB. All §6 inventory paths (scripts/config/schemas/tests/docs/templates) are within the 683 verified blobs. R1 tests build synthetic editions and never read those 41 data files.

## §6 inventory verification (before edits)

- Present with e4 line counts: `scripts/survey_agent_control_v2.py` 1935, `scripts/survey_reader_surface_gate_v2.py` 1931, `scripts/survey_weekly_derivation_v2.py` 702, `tests/test_survey_publication_revalidation_v2.py` 1046.
- Absent (created by this unit): `scripts/survey_weekly_mechanical_refresh_v2.py`, `tests/test_survey_weekly_mechanical_refresh_v2.py`, `docs/weekly-mechanical-refresh.md`.
- No extra runtime/schema path was needed: `core.json_bytes`, orchestrator `os.replace` precedent, Gate lazy weekly import, agent CLI structure, existing constructors (`build_manuscript_manifest`, `build_reader_surface_gate`, `build_bundle`, `build_review_record`, `build_stage_checkpoint`) all already in inventory. `docs/weekly-mechanical-refresh.md` is not added to `contract_files` (no maintenance loop).

## Candidate commits (own DB only, after status/diff/log inspection)

| Commit | Subject |
|---|---|
| `a1a4242` | R1 basis: worktree bytes of e4c8269 |
| `65ee720` | R1 runtime: refresh writer, Gate/receipt inspection sharing, ownership-checked revalidation rollback |
| `e79967a` | R1 writer corrections: exact change classification, clean-before-noop, relative review path, exit-2 error wrapping |
| **`afd925d`** | R1 tests and runbook: dedicated refresh suite, revalidation rollback regressions, operator runbook |

- Candidate head **`afd925d4f2413533e62c3ed211c732dd4a4d1539`**, tree **`2ee9cf2a284aca8497e99fb833102b03f2fcf0a2`**, parent `e79967a`. Tracked tree clean (only `scripts/__pycache__/`, `tests/__pycache__/` untracked).
- Full diff `a1a4242..afd925d`: 7 files, +1475/−28 (`logs/r1-candidate.patch`, SHA-256 `eccb85fd1eba8a61cae0839414040fe42ffea1c716eae216be5be747edb0574d`, 1630 lines).
- e4/B/witness fixtures untouched; no reconstruct commits/pushes; no network/production/main/Actions; no reset/clean/checkout of preserved dirs; no saved-harness reruns.
