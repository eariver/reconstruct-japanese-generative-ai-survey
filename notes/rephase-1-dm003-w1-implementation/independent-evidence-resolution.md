# DM003-W1 independent evidence resolution (read-only)

Scope: DM003-W1 ONLY. No tests/probes/runtime/network/restore/code/ref edits,
no agents. Read-only file + hash/Git inventory only. Original
`independent-implementation-review.md` left intact. No full audit/adoption.

## 1. New worker files reviewed

- `evidence-20261004T072423Z/evidence-qualification.md`
- `evidence-20261004T072423Z/final-binding-supplement.json`
- `evidence-20261004T072423Z/final-binding-observation.raw`

Original README/manifest/logs/scripts/pack/patch untouched; evidence dir now
holds 20 entries (17 prior + 3 new).

## 2. Limitations confirmed truthful

- `run-02..run-08` persist unittest stdout only. Grep over the evidence dir
  finds `GUARD`/argv/env headers only in `run-01` (commented command),
  `guard*.sh`, `gen_manifest.py` and the new qualification itself — none in
  `run-02..run-08`. Claim of no persisted literal argv/cwd/runtime/env/exit
  headers and no guard before/after transcripts is accurate.
- `run-01` is a transcribed subset (notes header + 6 test lines + full
  traceback + `Ran`/`FAILED`/`EXIT=1`), not a byte-exact redirect capture.
  Stated exactly; content unaltered.
- `run-09` `verify-pack` (no `-v`) sections are empty. Explanation (nonverbose
  silent on success; only tool-observed `EXIT=0`) is plausible and consistent
  with the saved log. `verify-pack -v` 7-object detail was and remains in
  `implementation-manifest.json:new_pack`, now re-observed in the supplement.
- No actual restore-script capture exists. Evidence dir contains only
  `gen_manifest.py`, guard sources and read-only re-verification logs. Claim
  that restore acquisition steps were tool-observed without raw script capture
  is accepted as a disclosed gap, not a proof.

## 3. New NOW bindings align (not retroactive)

`final-binding-supplement.json` + `final-binding-observation.raw` (labelled
command+output+exit transcript, offline git/stat/sha only) align with the
real candidate and prior raw/source:

- Impl and restore both actual HEAD `e1705b7fed01369767ab9d827c0360117d54aa1f`,
  tree `3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557`,
  parent `222a37e9ee2aa96724a491f2c04c2583a86b9650`, clean, branches
  `codex/dm003w1-preview-agreement` / `dm003w1-final`.
- Changed-3 index modes+blobs identical both DBs
  (`d58db79`/`25a7881`/`0eb328b`, all `100644`); worktree SHAs identical
  both DBs and equal to prior manifest
  (`7974551f…`/`7d4d0004…`/`ae42b94a…`); wrapper/stage unchanged
  (`092f1a2d…`/`0f2393da…`). Re-checked read-only here: all five SHAs match.
- All 7 pack objects typed (1 commit/3 trees/3 blobs) and `cat-file -e`
  present in restore; `verify-pack -v` output matches prior manifest.
- Artifacts: b40 tar 5,152,199 B `faf6792f…`, 20-pack 46,164 B `2c2a8e6f…`,
  W1 pack 57,856 B `97d384fe…`. Object-file inode intersection 0, alternates
  absent both DBs, remotes inert, full chain `e1705b7→222a37e→ff6c67f→
  490414c→b40de60→774dd39a`.
- Both 222 inputs still HEAD `222a37e`, clean.

These are NOW identity/successor observations only. They do NOT create
retroactive per-run guard proof, and the qualification explicitly disclaims
that ("durable per-run raw guard binding cannot be claimed; missing raw is
not reconstructed"). That disclaimer is correct and must be retained.

## 4. Source and test count unchanged

Source at `e1705b7` unchanged (SHAs above). 24 successful methods are the
same original evidence (`run-06` 6 + `run-07` 16 + `run-08` 2); no reruns,
no new test claims.

## 5. Doc wording: a375eb9

Qualification §1 ("Production is unchanged: reconstruct stays at Human
`a375eb9`, baseline `774dd39a` untouched") does NOT equate `a375eb9` with the
Production baseline; it distinguishes reconstruct Human HEAD from baseline
`774`. No mistaken identity. Optional cosmetic precisification (not a
blocker, no rerun): "Reconstruct workspace unchanged except new evidence at
Human `a375eb9`; Production baseline `774dd39a` untouched." No candidate
impact.

## 6. Disposition

- Blockers: none. Code/test findings stand per the intact original review.
- Nonblocking qualifications carried forward: per-run guard raw absent
  (NOW binding only, no backfill); `run-01` transcribed subset; `run-09`
  nonverbose verify-pack + no restore-script capture; module-level (not
  per-test) guards; owned-root inventories only; inherited 26,309 missing
  blobs; no full-56/R1 rerun or PASS transfer.
- **Final: BOUNDED_PASS for DM003-W1 only, with the above guard-raw/
  successor-proof qualifications.** No cosmetic reruns. Original review
  intact. Whole candidate remains NOT_READY; no adoption.

## 7. Clarification to my review (documentary only, disposition unchanged)

- Non-dict checkpoint takes the existing lacks-provenance branch; the new
  equality gate inside the authority-dict `else` does not execute — my "both
  errors" wording overstated.
- "Pending forbids any Preview provenance" was too broad; only existing
  pending rules are unchanged (`_pending_conditions` narrower than public
  State), normal null-pending/inert-file case valid.
- Special healthy asserts added+removed+modified; Weekly healthy asserts
  only added-2+manifest. S3 full-inventory no-diff proof remains genuine.
