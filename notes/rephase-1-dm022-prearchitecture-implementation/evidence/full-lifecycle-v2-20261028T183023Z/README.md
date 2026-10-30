# Full-lifecycle witness Attempt 4 — evidence note (General)

Date: 2026-10-28 UTC. BOTH Attempt-3 blockers fixed by B; C2 fixture correction
landed; runtime idle. Fresh FIXED private snapshot (never modified the old one):
`.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed-20261028T175919Z`
(758 files, base HEAD `409b292…`/tree `8ce36998…` + B lifecycle correction +
General own 2 test files). Runtime pins: `Python 3.14.4`, `PYTHONDONTWRITEBYTECODE=1`,
TinyTeX `lualatex` (LuaHBTeX 1.24.0) + `biber 2.22`, no `GIT_*` overrides,
process-scoped fixture identity, inert `example.invalid` origin, no alternates,
no fixture objects in reconstruct, no ordinary commits, no Human readback,
no network/install/old runners.

## Contents (this dir)

- `dm022-full-v2-test-raw-20261028T182623Z.txt` (SHA256
  `7793b699d91dc6542c825078d97065bd1bd44b430b0aa5689700a6ecff4b9ad0`):
  full 9-test witness transcript, exit 1, 226.610s — 8 ok, 1 failure
  (`test_weekly_candidate_to_released` at the release-checkpoint CLI;
  traceback + pid preserved verbatim). All Attempt-3 failures are preserved in
  `../full-lifecycle-v2-20261028T163527Z/` + `../full-lifecycle-v2-20261028T161838Z/`
  (no discarded transcript).
- `private-source-manifest-20261028T183023Z.json` (SHA256
  `b65f78e4fdbf27063d748b9615860eaf7359d25722f0812f2fea04b0cb79e2db`):
  758 intended files, post-run pins. Own test file
  `2c665f94e2c158f475283fac685bf6bcfb4d3c4ec66cfafcc8e3d61ae34f5e8e`;
  fixture helper unchanged `dc76b2e7…`; rest frozen B-corrected source.

## Own-harness fixes this attempt (setup, not target faults; all green after)

- seven_plan row key is `captured_sha`/`disposition` (not `source_sha256`).
- Draft input: `block_type` PARAGRAPH (SECTION invalid), runner `run_reference: null`.
- Fixture discovery artifact is the acceptance (records with locators), not JSONL.
- Fixture support files: whole schemas/config/templates + exact weekly/longform
  G76 closure members imported from the runtime modules (covers `.latexmkrc`).
- Canonical accepted-Evidence tree mirrored from revised R4 bytes.
- Draft stage checkpoint carries synthesis-input/result + paired
  draft-package/draft-result artifacts; freeze checkpoint adds
  visual-review-record (candidate pre-preview VISUAL review).

## New blocker (C2 scope, foreign — NOT patched, returned to ROOT)

- `scripts/survey_release_checkpoint_v2.py:68-81`
  (`build_release_checkpoint`, same in CLI `main`): iterates ALL
  `checkpoint_provenance` entries and raises `DM022_WRONG_FAMILY ... refused at
  completeness` for any PREARCH-family node. R6 site 15 (role map) selects
  refusal only for a PREARCH record *supplied as the release payload*
  (FROZEN->RELEASED + freeze/manifest/record); research roles
  evidence/materiality/completeness with a valid PREARCH record must be ADMITTED
  (R6 site 2; contract §11.2 forward consumption; ROOT §3 detached history).
  The adopted same-record triplet is permanent, so no DM022-adopted issue can
  ever reach RELEASED through this CLI. Exact function + traceback + pid in
  the raw transcript; minimal context in progress doc Attempt 4.

No foreign file modified; frozen snapshot never re-modified after pre-manifest
(pre-manifest `392776b1…` at 175919Z; post-manifest above). Whole unit remains
in progress; no Commit Point claimed.
