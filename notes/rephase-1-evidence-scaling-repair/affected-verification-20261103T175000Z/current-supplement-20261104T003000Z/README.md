# NEW CURRENT supplement — actual source-proof validator witness (weekly, final139)

Supplement: `notes/rephase-1-evidence-scaling-repair/affected-verification-20261103T175000Z/current-supplement-20261104T003000Z/`
Status: **Genuine positive + SAME-proof drift refusal via real `verify_renewal_source_proof`, `CURRENT_PROOF_VALID True`. No implementation/audit/adoption/semantic PASS. Root + independent reviewer decide.**

## 1. Why this supplement (old 478 qualified)

Prior harness `../current_proof_harness.py` (478 PASS, `../test-runs/batch-09-current-proof/`, fixtures `.../current-proof-fixture-20261104T*/`) is **preserved, not erased**. Per Root, those 478 are **closure/file assertions only** (`current_closure` live-SHA, `verify_closure_at_commit` Git-blob equality, Contract8 recompute, hist no-LIVE guard, etc.), **NOT yet the actual CURRENT source-proof validator witness** (`survey_versioned_renewal_source_v2.verify_renewal_source_proof` returning `CURRENT_PROOF_VALID True` + SAME-proof freshness refusal). Qualify old claims accordingly: useful literal checks, labelled correctly, 478 checks not 478 tests, no proof-PASS inferred.

No unchanged batches repeated (01–08 + 00 loader + 19 final + W34 409 already green, preserved).

## 2. Final139 binding (read-only, no shipping changes)

- SNAP worktree (`.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed`, HEAD `e746a5db…`, 771 files, clean, inert) **== proof-copy worktree** (`.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60`, HEAD `409b292…` + dirty 139) for all 771 intended files: **0 diff** (verified file-by-file SHA256, see `raw/stdout.txt` header + `data/pins-snap-771.txt`).
- Final delivery pins (verified in-harness, read-only):
  - patch `complete-evidence-scaling-409.patch` SHA256 `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49`, 5408065B
  - manifest `complete-evidence-scaling-manifest.json` SHA256 `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143`, 202204B
  - intended 771 = 689 tracked +82 new, delta 57M+82A =139 changed vs actual409.
- No shipping source/test edits; SNAP pins-before==pins-after 771 YES (`raw/pins-same.txt`).

## 3. Actual validator + fixture (no swallowing, no mocks)

- Test/API source: `tests/test_versioned_renewal_source_phase_s.py` in fixture work (final139). Read `_full_valid_proof` (~699, real `src.verify_renewal_source_proof`, asserts `CURRENT_PROOF_VALID`), `TestPhaseSHighU` actual proof paths. **NOT reused:** `test_layerb_full_reused_positive_weekly` allows `REUSE_TARGET_MISMATCH` as success — simply passing that method is NOT positive proof. This supplement does NOT use that swallowing logic; it requires explicit `CURRENT_PROOF_VALID is True`.
- HIGH U finalize path (`TestPhaseSHighU._run_u` weekly) **blocked in this environment, preserved as setup failure** (see `../current-supplement-20261104T000000Z-HIGH-toolchain-blocked/raw/`): `BASIS_ENTRY_INELIGIBLE: public State validation refuses LIVE bytes: ... build-record toolchain executable must be an existing file` (TeX toolchain absent, no PDF build, no fake). No manufacture; LayerB full-valid path used instead (legitimate, genuine, no HIGH stub).
- NEW evidence-only harness (packet, not shipping): `../current_supplement_proof.py` + wrapper `../run_current_supplement.py` (copied here as `harness/` for self-containment; authoritative versions in parent packet). Proper independent fixture:
  - bootstrap-weekly (existing legitimate `versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly`, read-only) + candidate source (SNAP 771, `_copy_tree_no_git` logic, no `.git/__pycache__/*.pyc/.rephase-...`, no hardlinks `nlink==1`, no alternates).
  - new independent DB, **process-scoped identity only** (`GIT_AUTHOR_*`/`GIT_COMMITTER_*` env `current-supplement-proof`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`), **no `git config`, no HOME rewrite, no remote (inert by absence), no `--allow-empty`**, no rootDB sharing. Executor identity (name/email/pid/ppid) persisted in `data/manifest.json`; executor label `phase-S-test (synthetic, non-genuine)` disclosed, NOT Human approval, no PDF/RELEASED claim.
  - strict loader roots: `sys.path.insert(0, work)`, pop all `scripts.*`, import `src/high/hist/core/test-helpers` from fixture work, assert `__file__.startswith(work)` **before authority**, verify fixture `git show HEAD:<rel>` SHA == live == SNAP for src/hist/high/LOW/Evidence before authority.
  - real full validator called, true flag checked explicitly (`is True`), plus `basis_file_sha256` == live basis bytes, `basis_self_sha256` == basis field.
- Scope: **weekly only** (`2026-W37/wk-boot-1`, `WEEKLY_GENERATED_V2`, closure 70). Longform via existing 7/8/3 consumers + family 6/graph 8 (labelled, not re-proven here).

## 4. Positive + SAME-proof drift (controlled separate, no coercion)

- Positive: `_basis_for(sc, "current-supplement-w1")` (real HIST verdict, real contract, real observed bindings) + `_full_valid_proof(sc, basis_rel, basis)` (real trio/old refs/Layer-A digests/CURRENT G76 closure 70/contract/HIST) → `src.verify_renewal_source_proof(work, basis_rel, proof_rel)` returns `CURRENT_PROOF_VALID is True`. Live State unchanged. Persisted: `data/renewal-basis.json`, `data/renewal-source-proof.json` (basis `4ab89395…`, proof `d6e7ff65…`, file `e3c21041…`), `data/current-code-closure.json` (70 rows), `data/manifest.json` (final patch/manifest, SNAP/fixture HEADs `e746a…/9359efd…`, issue/prop/route, executor, scope), `data/pins-snap-771.txt` (771), `data/pins-work-source.txt`, `raw/*` (argv/env/cwd/pid 3665050/UTC/exit 0/pins 771 YES/direct stdout/stderr).
- Drift: mutate CURRENT relevant tool byte `scripts/survey_research_authority_v2.py` (G76 7-file, Evidence-scaling LOW, in CURRENT closure 70) by appending one comment line, invoke **SAME stored proof files** (same `basis_rel`/`proof_rel` bytes, not rewritten) → **exact intended freshness refusal**: `RenewalSourceError: BASIS_CURRENT_TOOL_DRIFT: proof closure drift: scripts/survey_research_authority_v2.py` (`data/drift-refusal.txt`). SAME proof/basis bytes verified unchanged during refusal. Historical basis/proof data unchanged.
- Repair controlled separate: restore byte, re-verify SAME files → `CURRENT_PROOF_VALID True` (`data/repair-positive.txt`). No code coercion (restore, not validator weakening).
- No full old lifecycle/PDF (trio refs from seal, no PDF build), no synthetic Human approval counted real.

## 5. Pointers + gaps

- Harness (authoritative in parent packet, copied here): `harness/current_supplement_proof.py`, `harness/run_current_supplement.py`
- Data: `data/{renewal-basis.json,renewal-source-proof.json,current-code-closure.json,manifest.json,pins-snap-771.txt,pins-work-source.txt,drift-refusal.txt,repair-positive.txt}`
- Raw: `raw/{stdout,stderr,exit,argv,env,cwd,pid,wall-start/end,meta,pins-snap-before/after-771,pins-same}.txt` (exit 0, pins YES, PID 3665050, 2026-11-04T00:23–00:24Z)
- Fixture (ignored runtime, manifest only in packet, no full DB): `.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/current-supplement-fixture-20261104T002400Z/work` HEAD `9359efd01ac1655debf906e74bc43bb57d2f6405`
- Preserved failures: `../current-supplement-20261104T000000Z-HIGH-toolchain-blocked/` (HIGH toolchain executable gap, TeX absent); old 478 harness/raw preserved with qualified claims above.
- Gaps: weekly only (longform not re-proven here); HIGH finalize blocked by toolchain (see preserved failure); no R4/audit/adoption/savings; no test19/Raw409 repeat (already green).
