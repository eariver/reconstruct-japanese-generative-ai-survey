# WEEKLY actual State lifecycle — VALIDATED_DRAFT → RELEASED (public validators only)

2026-10-25. TEST worker WEEKLY ONLY, parallel with Longform and editorial-code author. No shared candidate/INPUT edits, no source patch.

## Fixture

- OLD read-only `.rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly` HEAD `afab1762a90ca568b333abae7f1641ea64bdb5df` (SOURCE G5 `6e82e97` + artifact, State VALIDATED_DRAFT pointer r6 `dbeba4cb`, style `a4bd135a` variant, codes H `6fe86e78` P `825dba1d` PUB `3f4039fd` S `20f63eaf` HIGH `9a04` Reader `098a2c82`).
- NEW byte-independent clone `.rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-20261025T101500Z/renewal-weekly` via `git clone --no-hardlinks`, remote inert `https://example.invalid/versioned-renewal-weekly-state-lifecycle.git`, own absolute gitdir, no `objects/info/alternates`, `nlink_bad=0`, `git_inode_overlap=0`, no `GIT_*`. Exact E copy 225 untracked + 3 ignored by captured manifest (`e-manifest-untracked.txt`/`e-manifest-ignored.txt`, `e-hash-old.txt` vs `e-hash-verify.txt` `E_HASH_UNCHANGED`), including ignored PDF/log and untracked typed fixtures + `scripts/__pycache__` preserved (explicit annotation `exclusion-annotation.txt`: no exclusions, no blind cleanup). No modifications to OLD (OLD HEAD still `afab176`). No new tool source patch; current proof epoch G5 valid artifact-only HEAD allowed.
- Fresh Python per phase (`sys.path.insert(0, FIX)`, origin checks `core.__file__`/`agent.__file__` startswith FIX), sanitized `GIT_*`, `PYTHONDONTWRITEBYTECODE=1`, workspace-local `TMPDIR`, immutable code pre/post guard (all key codes same FIX vs OLD, see phase5 `code_guard`).
- No candidate/reconstruct ordinary commits/network/old-runner exec/cleanup failed fixtures/clone State rewinds. Reconstruct `git status` shows only untracked evidence under `notes/.../weekly-state-lifecycle/` (+ parallel workers), no tracked mods, no staged.

## Config

`config/survey-production-v2.json` `stage_plan`:
- `VALIDATED_DRAFT` (`stage:publication-candidate`, `validate:publication-candidate`, `next_state RELEASE_CANDIDATE`, `checkpoints []`, artifacts `publication-candidate: {source_root}/publication/v2/publication-candidate-v2.json`)
- `RELEASE_CANDIDATE` (`stage:freeze`, `validate:freeze`, `next_state FROZEN`, `checkpoints [freeze]`, artifacts `freeze-record`, `release-manifest`)
- `FROZEN` (`WORKFLOW_DISPATCH stage:release`, `validate:release`, `next_state RELEASED`, `checkpoints [release]`, artifacts `merge-verification`, `release-record`)

Precode binding: ROOT `7d7d5a45` §6 preserved — strict LIVE `agent.validate_agent_state` on exact bytes, canonical path, prePreview window; `production.verify_state_basis` is different globally-pinned API, not a substitute; whole-doc schema pointer `""`; no `Path(".")` repair. Contract `478f0051` §11 whole operation scope respected.

## Public lifecycle (normal validators, no handmade State fields/direct overwrite/monkeypatch)

Synthetic clock monotonic `>=` history/selected (`r6 08:41:00.502366Z`): `09:10:00/01Z`, `09:20:00Z`, `09:30:00/31:00/01Z`, `09:40:00/30/41:00Z`; actual UTC raw separate per phase.

- **Phase0** (`phase0-.../phase0-result.json`): initial VALIDATED_DRAFT, `agent.validate_agent_state==[]`, `VERSIONED_ACTIVE`, active Candidate `.../high-u4-weekly/publication-candidate-v2.json` `2a1374...`, proof `395cc0...` matches seal, PDF `8fb8aca...` 5 pages, stage_plan captured.
- **Phase1** (`phase1-.../before.json`/`after.json`/`transition.json`, `phase1-...-stdout/stderr/exit.txt` exit 0 after repair): `stage.validate_stage` + `agent.build_stage_checkpoint` + `agent.advance_with_checkpoint` with exact State-selected Candidate. Before `520a9b74...` VALIDATED_DRAFT → After `b1c52628...` RELEASE_CANDIDATE, `HUMAN_GATE_REACHED`, `PUBLICATION_PREVIEW` pending, pointer unchanged `r6 dbeba4cb`, history 8→9 `VALIDATED_DRAFT→RELEASE_CANDIDATE 09:10:01Z afab176`. New: `VALIDATED_DRAFT-core-contract.json 08eb3cb5...`, `VALIDATED_DRAFT-reviews.json fc6876...`, `VALIDATED_DRAFT.json c71129...`. Empty checkpoints `[]` so no `checkpoint_provenance` entry (corrected vs initial harness assertion, see `phase1-repair-...py`).
- **Phase2** (`phase2-.../` exit 0): synthetic `agent.approve_publication_preview` (`synthetic-human-fixture`, `09:20:00Z`, `synthetic:weekly-u4-preview; NO genuine Human/Production approval`) bounded to exact Candidate/PDF. `aabc47c0...` RELEASE_CANDIDATE, human/machine preview `approved`/`passed`, Human/checkpoint agreement on `gates/publication-preview-approval.json 732aca...` binding exact Candidate `2a1374...`/PDF `8fb8aca...`, history unchanged (9), sole pointer exact.
- **Phase3** (`phase3-.../` exit 0): `profiled.build_profiled_freeze` (`09:30:00Z`) → canonical `freeze-record-v2.json 3f2330a4...` + `release-manifest-v2.json 9ae8be16...` (fresh, no delete/overwrite divergent; noncanonical `lifecycle-high-u4-weekly-continuation/*` preserved). Then `stage.validate_stage` + `build/advance` with `freeze-record`+`release-manifest`+`visual-review-record` (exact Candidate Visual `.../high-c1-weekly/reviews/visual-review-v2.json 9b41df...`). `95ba3d7c...` FROZEN, `stage:release`, freeze `passed`/release `pending`, history 9→10 `RELEASE_CANDIDATE→FROZEN 09:31:01Z`, provenance `RELEASE_CANDIDATE.json b96baf...`.
- **Phase4** (`phase4-.../` exit 0): offline synthetic `pubmod.build_merge_verification` (`09:40:00Z`, HEAD `afab176`) + `pubmod.build_release_record` (`09:40:30Z`, `weekly-u4-synthetic-release; NO real GitHub/network/tags`) via same test contract, then `release_checkpoint.build_release_checkpoint` (`09:41:00Z`) + `agent.advance_with_checkpoint`. `a06e16c3...` RELEASED, `COMPLETE`, `next None`, release `passed`, history 10→11 `FROZEN→RELEASED 09:41:00Z`, provenance `FROZEN.json 413615...`. New: `merge-verification-v2.json 47d39a3...`, `release-record-v2.json 68c19c29...`, `core-stage-contract-v2.json ede9c6e7...`.
- **Phase5** (`phase5-.../phase5-result.json`, `phase5-...-stdout/stderr/exit.txt` exit 0): after RELEASED `agent.validate_agent_state API==[]` + CLI `validate-state --state sources/2026-W37/production-state.json` exit 0 `{"valid":true,"lifecycle_state":"RELEASED","terminal_reason":"COMPLETE"}`. Current Candidate/proof/history/readback: `VERSIONED_ACTIVE`, Candidate `2a1374...` proof `395cc0...` == seal, history 11 with exact tail `09:10:01/09:31:01/09:41:00 afab176`, effective7 7 roles, Release Manifest `9ae8be16...` (`weekly/2026-W37`, pdf `8fb8aca...`, source `1e3b22a5...`), source PDF `61239B 5 pages`, source tex `1e3b22...`, merge/record validated. Expected write inventory = 13 new files listed in `phase5-result.json` (+ State updates), no source patch (`code_guard` all same), no tracked mods, OLD unchanged, noncanonical preserved.

Per-phase bound 1200s (all exits 0, no timeouts; PID/heartbeat via driver `START/DONE` logs + `commands.log` where applicable). No blocked fallback: at no point returned low-level-only success; every transition used normal public validators. Existing low-level Preview/Freeze at noncanonical paths not used as canonical, not deleted, no divergent overwrites; canonical collisions checked fresh before each write (all fresh, no `refusing divergent`).

## No whole-unit claim

WEEKLY State lifecycle to RELEASED is BOUNDED COMPLETE as a TEST-worker route. No operational adoption claim; synthetic reviews/Preview/merge/release are explicit fixture decisions, never genuine Human/Production approval; Production semantic NO-GO retained. Root whole unit not done, no Commit Point. Ordinary Commit/Push Human-owned.

## Evidence index

- `setup-20261025T101500Z/` (clone-0/remote/cfg/head/log/gitdir/noalternates/config-show, `e-manifest-*.txt`, `e-hash-*.txt`, `status-postE`, `isolation-nlink/inode.txt`, `head-postE`, `exclusion-annotation.txt`, `commands.log`)
- `phase0-20261025T101500Z/phase0-result.json`
- `phase1-20261025T101500Z/{before,after,transition}.json` + `phase1-...-stdout/stderr/exit.txt` (exit 1 initial harness assertion) + `phase1-repair-...py` (PASS, explains empty-checkpoint provenance)
- `phase2-20261025T101500Z/{before,after,transition}.json` + stdout/stderr/exit (0)
- `phase3-20261025T101500Z/{before,after,transition}.json` + stdout/stderr/exit (0)
- `phase4-20261025T101500Z/{before,after,transition}.json` + stdout/stderr/exit (0)
- `phase5-20261025T101500Z/phase5-result.json` + stdout/stderr/exit (0)
- Drivers `phase{0..5}-*.py` (`py_compile` OK, no saved-runner reuse, no old-runner exec)
