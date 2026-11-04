# Real W34 409 retry — ACTUAL COMPLETION (facade fix, no repin)

Packet: `notes/rephase-1-evidence-scaling-repair/real-w34-retry-20261103T172327Z/`
Runtime: `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`
Status: **Exit 0, 409 completion via normal strict facades. No EVIDENCE_REVIEWED/Gate/Production. Returned to Root for closeout.**

## 1. Disposition (why retry, what was wrong)

- Prior `real-w34-verification-20261103T170921Z` (epoch `bd80d60` over `48082356`) failed exit2 in 17.56s at runner pre-accept `_finish` → bare `core.verify_state_basis` comparing init `480…` vs current `bd80…`. Preserved untouched with all metrics/source/raw (`raw/machine.json` 21K, `stderr.txt` 2.3K, rchar delta 4.8G).
- Correction per `astra-source-review.md` §“Actual409 attempt — escaped current-stage facade” + source owner `implementation-return.md` §11: failure was NEW runner callback EXECUTION outside `current_stage_basis_override`, NOT proof epoch continuation unsupported. Existing agent-first support still valid; new wiring bug, not existing API gap. Fix is runner-only: `_finish` EXECUTION inside facade at `run:~707` (pre-accept) + `~890,894` (archive ×2); definition alone inside `with` was insufficient. No State/Profile/CP repin/reinit/legacy validator change. Failed packet preserved; this note limits Explore-trace withdrawal to the escaped-facade scope.

## 2. SOURCE (NEW quiet pins, 771, external dirty guard)

Author workcopy `evidence-scaling-implementation-20261103T114312Z/candidate-work` (HEAD `409b292…`):

- `survey_evidence_v2.py` 158943B `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a` (unchanged F5)
- `run_evidence_v2_interactive.py` 45833B `5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543` (facade fix; verified `~707 with override(): _finish`, `~890,894` archive ×2 wrapped)
- `survey_research_authority_v2.py` 218692B `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b` (unchanged)
- Test `d486809c4ae88c0e78784ade8e456cd9227b25a29c12cde9700664a1eec3edad`/91561B from `evidence-scaling-fixed-20261103T170831Z` (= `1c95f675` + additive Views-RETURN 2 tests, TEST-ONLY). Author copy still `1c95…`; actual full pin observed and composited here per `TEST-ONLY-DIFF.md`. Runtime frozen.

Baseline manifest `634d41f9…`/770 + new test = 771 intended. Modes `0o664`/`100644`.

## 3. NEW clone (ORIGINAL 480, not bd80)

- From PRESERVED ORIGINAL `rehearsal-20261101T025600Z/candidate-work` HEAD `480823560c…` (failed `bd80` clone untouched, HEAD still `bd80d60…`). Parent verified, 326G avail >> 249M. `cp -a` no hardlinks, `__pycache__` removed NEW only; 231 `.git` files 0 shared inodes/0 content diff, inert origin, 0 symlinks, no `GIT_*`.
- Old pins verified before install (3 OLD_OK, test absent). Installed ONLY 4 files (3 runtime author + test fixed-snapshot), NEW_OK above. No config/docs/schema/Profile/State/checkpoint edits; 7 pre-existing `M sources/…` + 7 `??` real-DATA identical to original.
- Staged ONLY 4 (`git add` 4, never `add -A`). Commit `e84a82aca000c990597ea8cf60f548e2ff187bd1` parent `48082356…`, tree `fb8e536e…`, author `w34-retry-isolated`, no config change, no `allow-empty`. Blobs `6a1b6886…/01cf1198…/e6c56ba3…/322d6caf…` match working. Contract8 unchanged (pipeline `3adfbda2…` etc. identical). State impl still `48082356`, `CANDIDATES_NORMALIZED`. Source HEAD change alone, not State repin.

## 4. Inputs (every SHA, Raw425, absent, SP read-only)

- State 3386B `7e6a50c2…`, Profile 2371B `2a8c3089…`, R369 `e176326f…`/963155B (369 lines), E439 `0a23be47…`/1335444B, Screening `b9d963d8…`/543880B, 409-input `3ffc6e31…`/1573186B (409 records: 352 PARTIAL/49 VERIFIED/8 NEEDS_MORE kept structural, no publisher-truth claim), supp-r2 `ce6f977a…`/389414B (428 entries/425 distinct Raw, 0 missing/0 mismatch verified file-by-file). No r1.
- Canonical `evidence/v2` absent, ledger/completeness absent at entry (fail-closed guards). SP state/profile byte-equal orig vs new, untouched/read-only. 770 baseline files present + newtest = 771.

## 5. Run (correct facades, fresh fail-closed harness, durable raw)

Harness `run_w34_retry.py` (fresh, not blind reuse; fail-closed guards bound to NEW HEAD `e84a82a`/parent `480…`/7 input SHAs/4 runtime SHAs + canonical-absent; exit 3 on guard fail). Normal `run_mod.run(repo_root, state_path, input_path, supp_path)` only, no bypass/monkeypatch/preloaded context/subset/projection/public flag. Private batch slices preserved. `PYTHONDONTWRITEBYTECODE=1`, one run.

- PID `3515131` recorded/polled same PID, no duplicate jobs. Outer start `2026-11-03T17:24:52Z`, inner start `2026-11-03T17:24:52…`, end `+175.26s`, outer end `2026-11-03T…`. Exit 0.
- Modules same-process `__file__` hashes match committed source (Evidence `48742538…`, runner `5e195730…`, LOW `0974c709…`). Committed `e84a82a/480…` in machine. Before/after 4 runtime + 6 State/SP + 7 inputs + full 771 identical except new canonical outputs; `source_mutated_during_run=false`.
- `/proc/self/io` same-process: before `rchar:1629111 read_bytes:0`, after `rchar:45240615956 wchar:11701213 syscr:320657 read_bytes:0 write_bytes:10125312` (delta rchar 45238986845 ≈45GB logical, physical `read_bytes` 0). `rusage` utime delta 160.18s. Raw preserved: `raw/stdout.txt` 601B, `stderr.txt` 0B, `machine.json` 20K, `pid/outer_*` + `run_w34_retry.py`. Scope clear: measures only.

## 6. Outputs (full validators, no silent fix)

- Evidence `…/bf208f96…/evidence-accepted.json`: `result_count=409`, results 409, status 352 PARTIAL/49 VERIFIED/8 NEEDS_MORE (matches input; old 49 VERIFIED kept structural pending semantic review, no independent research PASS).
- Views `…/f744e46b…/edition-views-accepted.json`: 409 views. Files: tasks 409, results 409, views 409.
- Ledger `materiality-ledger-v2.json`: rows 439. Completeness `profile-completeness-v2.json`: 3 obligations, `overall_status=LIMITED`.
- Stable IDs: package tasks 409, authority_supplement path/SHA `ce6f977a…` (428/425), no hand-append (409==input 409). R≠E: basis `discovery_path=screening/input/event-discovery-v2.jsonl` (`0a23be47…`) vs evidence results derived, distinct; resolvers carry validated `root_records`, no E-as-R fallback.
- Accepted/public readback valid using NEW code/new HEAD inside facade (runner context): `validate_evidence_acceptance` 409 OK, `validate_edition_views_acceptance` OK. Bare standalone without facade correctly refuses on old-State/new-HEAD (expected, not a defect).
- State still `CANDIDATES_NORMALIZED` (no `EVIDENCE_REVIEWED`), checkpoints `DISCOVERY_COLLECTED`/`ISSUE_INITIALIZED` preserved, Contract8 identical, SP unchanged, old rehearsal `480…` unchanged, failed `bd80` untouched, NEW source 771 unchanged. No code edits on success. Products retained in NEW ignored clone (not Temp auto-clean only) + machine manifest here.

## 7. Metrics scope (bounded)

New measured 45GB rchar / 175s wall / 160s utime to 409 completion. Old transcribed failed bounds 228GB rchar ~14min to 143-task termination (no raw dump). Compare ONLY these logical/time numbers; **no full speedup/disk/deadlock/savings claim, no old-full-runtime extrapolation**. Physical `read_bytes` 0 in this run (page-cache logical), not disk proof.

## 8. Pointers

- Harness: `run_w34_retry.py`; Machine: `raw/machine.json`; Raw: `raw/stdout.txt/stderr.txt/pid.txt/outer_* /repo_root.txt`; Manifest: `artifact-manifest.json`
- Runtime: `…/evidence-scaling-w34-retry-20261103T172327Z/candidate-work` HEAD `e84a82a` parent `480…`
- Failed preserved: `../real-w34-verification-20261103T170921Z/` + `…/evidence-scaling-w34-verification-20261103T170921Z/`
- No Human Commit Point; unit Root closes.

## 9. Record qualification — workspace HEAD note (no new authority)

- Prior tool return stated `Workspace HEAD dddbdfe… unchanged`. Provenance from already-saved tool history: that value came from a NEW reconstruct-side `git -C . rev-parse HEAD` read issued during packet verification, not from `run_w34_retry.py` (which rev-parses ONLY the NEW isolated clone `e84a82a`/`480…`) and not from this README (which makes no workspace-HEAD claim).
- Per explicit no-Human-Commit-readback / no-current-checkout authority, quarantine that reconstruct HEAD read as NOT authority for unit-boundary statements. Withdraw the fresh `unchanged` inference; do not use it to assert workspace state. Old tool-return facts otherwise preserved as recorded.
- Genuine code-epoch `e84a82a` / workdir guard / 409-completion claims above stay independent of the quarantined workspace-HEAD note.
