# LF-2I independent final resolution — BOUNDED_PASS

2026-10-10. Same fresh author-independent reviewer as
`evidence-20261010T000000Z-correction/independent-implementation-review.md`
(C1 author). Read-only review of correction2; no broad rerun, no code edits,
no network/commits/subagents, no candidate/reconstruct fixture writes. No
disposable probe was required: all findings are decided from saved source,
packet manifests, and raw logs (bytecopy existence independently re-observed
read-only).

## 1. Basis (exact)

- Source `/tmp/opencode/jgas-lf2-design-20261009T113013Z`, HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c` (unchanged, no commits),
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`; status exactly 2M+7A
  plus `__pycache__` side effects listed separately.
- Final 9 pins (per `hash-manifest.json`, re-verified by direct read for the
  two changed paths): gate runtime `e73058841cfa1a841030b96d5cd2fb756c6ba99d1b99522ddbf0131d1f06bbe4`,
  gate schema `fe4a96f4aa87f2a527096c4d3040f92e0217ef972ddae1d7140498184a13322c`,
  receipt schema `4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca`,
  reader schema `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643`,
  derivation `c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149`,
  helper `d480e11d1c398f79f3e894e2e1e1f56ceec507dfde376a163a58b0ebed97d3c2`,
  publisher **`71ef7b976684e0f88407c24ba3ed8d6f51135be2b7a048b2655dd5b777ef5b40`**,
  LF-1 test `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913`,
  integration test **`61a3491a572f113e6b2c94b897e5dde2ac234290c4925ceb1c1f0e52ebdd6ad9`**
  (all modes 664). Only publisher + integration test changed this round;
  path budget unchanged.
- Governing: selected contract `4795a586…` + F1–F3, DM-021 disposition
  (initial + healthy readback only), root `astra-review-r2.md`
  (C1/S1–S4/E1–E3/R4). Prior 44-method result is superseded history; new
  claim is 42 methods only — no 42+44 transfer.

## 2. Source corrections verified (actual on-disk code)

- **C1 PASS.** Drafting archive is now a first-class snapshot dependency:
  `_snapshot_inputs` records `archive_rel` via `_rel` + `archive_sha256`
  under strict `_safe` containment (publisher:187-196); `_recheck_snapshot`
  re-reads it from disk at every window (228-230). Both timing windows are
  seam-proved: (c) archive drift after snapshot → `before-writes` refusal;
  (e) archive drift during `build_receipt` → prospective-divergence refusal.
- **S1 PASS.** Tautological buffer-vs-buffer checks are gone. Raw State/input
  bytes are captured lexically BEFORE validation (`_capture_lexical_bytes`,
  288-291) and verified stable AFTER derivation (302-305); review bytes are
  captured BEFORE semantic validation and verified afterward (484-505);
  snapshot is built from those verified captures (508-510); every recheck
  re-reads actual on-disk State/input/archive/reader/review/accepted/closure
  files (210-242). Seams (a) input-drift-inside-derivation, (b)
  valid-but-swapped review, (c) snapshot seam, (d) pre-write seam prove real
  file mutations refuse; only the deliberately injected file is excluded
  from no-write expectations, explicitly, before repair.
- **S2 PASS.** Publication directory is built from the profile's RAW
  `source_root` string (`pub_rel_raw`, 313-320) through `_strict_dir_preflight`
  with no `_rel`-resolve-before-check on this path, plus existing-path kind
  validation (323-326). E2E proof replaces the old helper-only unit: pass1
  with `publication/` → outside sentinel and pass2 with `v2/` → alternate
  sentinel both refuse through the real caller with full-snapshot equality
  and sentinel targets verified untouched (only `sentinel.txt` present).
- **S3 PASS.** All predictable `lexists` output checks (559-561) AND the
  `before-writes` recheck (562-565) run BEFORE any `mkdir` (567-568); only a
  narrow post-mkdir revalidation follows (569-581). Pass1 same-byte reuse is
  classified: no source set → healthy reuse; complete set → full
  receipt-replay gate (reuse iff valid); partial/inconsistent → refuse
  (444-463). Seam (c) asserts no survey-dir side effect on pre-mkdir refusal.
- **S4 PASS.** `_assert_receipt_matches_prospective` (245-271) compares every
  binding (`schema_version/issue_id/route/status/basis/accepted/authored/
  reviewed/review/outputs` + closure/contract/commit + digest) after
  construction (663-666); a final on-disk `_recheck_snapshot`
  (`final-before-install`) runs AFTER construction immediately BEFORE install
  (667-673). Builder-drift seam (e) refuses with retained partials and no
  receipt. Receipt write/close failure reports the partial receipt path in
  the retained list (678-680); pass1 surface failure reports the surface path
  when created (433) — the old `retained[]`/omitted-receipt misreports are
  fixed.
- **R4 PASS.** Controlled close fault (full `references.bib` bytes installed,
  then close raises) and receipt-install fault (partial receipt bytes, then
  failure; partial file verified present but unparseable) assert retained
  bytes/owned paths, unrelated sibling preservation, and retry refusal BEFORE
  cleanup (seams f, g). Mid-write fault from the prior round is retained.

## 3. Evidence corrections verified (actual packet, not claims)

- **E1 PASS.** `GIT_NO_LAZY_FETCH=1`, `GIT_OPTIONAL_LOCKS=0`,
  `GIT_ALLOW_PROTOCOL=file` are forced for BOTH runner-owned git calls
  (`git_env`) and children (`child_env`), plus `PYTHONDONTWRITEBYTECODE=1` /
  `GIT_TERMINAL_PROMPT=0`. `GIT_*` / `PYTHONPATH/HOME/STARTUP/OPTIMIZE`
  overrides and `sys.flags.optimize != 0` are rejected BEFORE EVERY
  candidate git operation (`assert_clean_env`, per-phase `env_checks` all
  empty/0 in `manifest.json`). Child argv, interpreter
  (`3.14.4`, `optimize 0`), git version (`2.53.0`), cwd/env recorded.
  No installs, no network.
- **E2 PASS (real driver, not logic toy).** `proof_suite` builds three NEW
  independent full disposable composites (9 files + own Git DB + own HEAD in
  the exact 2M+7A worktree shape) and invokes the SAME `guard_overlay` code:
  A drifted source → pre-guard rc 1, child never launched (sentinel absent);
  B correct source + exit-7 child → child exit observed, driver nonzero path
  recorded; C child0 (sentinel proves launch) + post-child drift → post-guard
  rc 1. `proofs.log` holds all three lines with numeric codes; `manifest.json`
  `disposable_proofs` matches. No candidate canary, no full-suite repeat.
  The old hash-inequality toy is superseded (preserved only in the old packet).
- **E3 PASS (saved patch replay, not construction).** `save_patch` writes the
  TRUE complete patch (M diff + clean `git diff --no-index` new-file diffs
  with `new file mode` headers, no `---NEW-FILE---` markers;
  `newfile_diff_exits` all 1 as expected). `apply_proof` `cp -a` byte-copies
  ORIGINAL clean 409 (`/tmp/opencode/jgas-dm004-impl-20261004T234416Z`) to a
  NEW isolated DB (re-observed: `/tmp/opencode/jgas-lf2i-409bytecopy-20261009T203526Z`,
  HEAD still 409, status exactly 2M+7A), checks pre-HEAD clean / inert origin
  / no alternates / 109 objects with 0 shared inodes, then applies the EXACT
  SAVED patch (`--check` exit 0, apply exit 0, per-file `Applied patch ...
  cleanly`), and compares all-9 bytes + physical modes + `ls-files -s`
  logical modes. The old 2-file-tmpdir + live-copy construction is superseded.
- **42-source/runner identity PASS as exact-run evidence.** `run.log`: 42
  tests OK in 1698.663s (12-method LF-2I module incl. new
  `test_dependency_snapshot_seams_and_receipt_faults` + Gate module + 3 LF-1
  loader controls); full-repo syntax/compile sweeps were dropped as
  unaffected (no schema/config change — justified, not transferred). Pre/post
  identity (all-9 hash+mode, HEAD/tree/parent, exact 2M+7A set), child exit 0
  no-timeout, exclusive-write files (refuse-overwrite), `__pycache__` listed
  separately. This runner is exact-run evidence, NOT a certified general safe
  rerunner — no such certification is granted here.
- **Preservation/qualification PASS.** `preserved-9/` + manifest pin pre-edit
  bytes/modes/hashes; old packet (prior patch, dev logs, attempt1 env
  failure) intact; `attempt1-proofsetup-failure/` preserves this round's
  proof-harness setup failure (single-commit repo lacks `HEAD~1`; fixed with
  a root commit, rerun green). Earlier reviewer overclaims are explicitly
  corrected: my prior R1/R2/R8 bounded-PASS notes overstated caller safety
  (`_rel`-resolved pub path), snapshot guarantees (frozen-buffer/memory
  comparisons), runner guarantees (logic-only proofs), and apply guarantees
  (2-file construction). Those notes are superseded by C1/S1–S4/E1–E3 above;
  no independent acceptance is inferred from the omissions.

## 4. Scope preserved

Normal healthy FROZEN/RELEASED readback and both same-issue manuscript
stage-Gate backstops remain green in `run.log`; grep confirms no
`EXCEPTION_*` / `REVIEWED_EDITORIAL_CORRECTION` / `REVIEWED_CORE_CHANGE`
paths in publisher or integration test — no DM021 shortcut, no fake
prior-State, no false reason. `config/*.json` untouched; the config-note
mechanism (existing control-roots + closure pinning, no invented
registration) stands as previously endorsed. No new authority/role,
dispatcher, fidelity-schema, or Production change. Closure list correctly
unchanged (no newly imported helper this round; `survey_reader_fidelity_v2`
remains a call-time import bound by the existing control-roots check per the
closure comment).

## Verdict

**BOUNDED_PASS** for the LF-2I correction2 scope (C1 + S1–S4 + E1–E3 + R4
fault proofs) at the exact hashes in §1. This is bounded implementation/
evidence acceptance of the selected initial route only — not full
publication, canonical audit, all-profile, build-transfer, semantic/visual,
or lifecycle-savings approval.

## Limitations

- Read-only packet/source review plus re-observation of on-disk identity;
  the 42-test PASS belongs to the author's runner evidence, not an
  independent rerun.
- Synthetic accepted-chain + type/identity review/PDF/Human fixtures prove
  only the contract's type/identity route.
- Whole candidate NOT_READY; step4/B3 OPEN; canonical audit unstarted.
  No Commit/Push (ordinary reconstruct commit remains Human-owned).

*Corrections vs source vs evidence:* C1/S1–S4 are source + oracle fixes
(publisher `71ef7b…` + test `61a3491a…`); E1–E3 are evidence-harness fixes
(new runner `run_lf2i_correction2.py` + `proofs.log`/`apply.log`/saved
complete patch); prior-packet bytes and my earlier overclaims are preserved
and qualified, not rewritten.
