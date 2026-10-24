# Bootstrap fixtures — evidence summary (references, DBs not in notes)

2026-10-23. Both fixtures child exit 0, ACTIVATED prePreview, no Preview/freeze/adoption.

## Weekly (2026-W37, wk-boot-1)

- FIX_ROOT: `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly`
  HEAD `721a04d85532d7855f3e54cc411f5847c787726e`, tree `ac7cb0bd2e977b46e957450816eddd779799e144`, ls-files 721.
  Post-run HEAD same, `git status` 10 untracked (`sources/`, `surveys/`, etc.), no HEAD move.

- State: `sources/2026-W37/production-state.json` SHA `ca7c0d2e62b69125a5365593eecb797b1b0f4449e2d888edb4b71dacf68fda03`
  lifecycle `VALIDATED_DRAFT`, Preview pending, strict `agent.validate_agent_state` == [].

- Proposal: `sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/proposal.json` SHA `99c59ecf60f494e94fa121cf3c1fdc353047d74c411164d4d71abc874b774c6f`
  P1 `REVIEW_REQUIRED`, after-capture `ProposalError` refusal OK.

- P2R manifest: `.../wk-boot-1/retained/retention-manifest.json` SHA `b36ec8859f9503c9fdf6d39be3dab0d1bbfdb66bff65d5b191b05342780e223d` (`CAPTURED`/`VERIFIED`).

- Scope: `.../wk-boot-1/scope-review-v2.json` SHA `4ad453f4f6a83119b10ab20ae05f9ff576d6604ccf03fb635aeda5af3526641b` (synthetic, `WITHIN_APPROVED_AUTHORITY`).

- P2V: `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`.

- P3S staged manifest: `.../wk-boot-1/staged-source/staged-source-manifest.json` SHA `0b17f44d00ecdfee054e4ff5810d530d6dafd5b118185bf782466be1ce5ed79c`, code_deps 50, `STAGED_SOURCE_REPLAY_VERIFIED`.

- Specs: `manuscript-spec.json` SHA `9d1bbc3b7e16e4b60a96231c0e31f4d358da1aece8648e6e56aacdb908e0dccb`, `toolchain-spec.json` SHA `1992e8c9c7c9bbe750aead85e1d870a76c225a7a8eb9376d587dc22353213795`, recipe `lualatex-biber-lualatex`, argv ×4 == `EXPECTED_ARGV_LUALATEX_BIBER`.

- Prepare REAL TL2026 dt 27.5s:
  PDF `.../wk-boot-1/publication/build/main.pdf` SHA `0684697f7043f5dc7c4464e90ceec162ac1553b284ce09ba88c01f9dd450b9d3`, 61239B, 5 pages (pypdf).
  Log `.../build/main.log` SHA `431a92823eec4133ae65d792b66633510e66d01acd7808f207d3d2cee3c0b5c1`, 92972B.
  Manuscript `.../publication/reader-manuscript-v2.json` SHA `cff7253d0dedd3d22e69ec98ef7b7f27a30763d88065b32f7d44f8fe94f19a17`.

- QA: `deterministic-checks.json` SHA `c23cd49b7f89aecdce2d3e9a54c2a72606e7aa0e8d8342e9bbcaf027a220ff7c` (3 DETERMINISTIC, actual file assertions).
  Synthetic reviews via actual builders: semantic SHA `77d758e1...`, visual SHA `f81a3cbd...` (clearly synthetic, no genuine approval).

- Seal: `.../wk-boot-1/publication/publication-set.json` SHA `782c02bb13481384f13511ea1d08fab6dc9f25342d9cc6e5a02b60f0e7da06ff`, `validate_prepared_set` OK (15 roles).

- Record: `sources/2026-W37/publication/v2/publication-surface-revalidation-r1.json` SHA `652462887f6a7ce5835f7db83e8d702110209c9ca7ed408d7133baf007145ea6`, supersedes None, anchor `VALIDATION_CHECKPOINT` (`DRAFT_COMPLETE.json` SHA `ffbde649...`).
  Selection `VERSIONED_ACTIVE`, candidate `.../wk-boot-1/publication/publication-candidate-v2.json`, receipt issue `2026-W37`, Gate `PASSED`, Candidate `READY_FOR_PUBLICATION_PREVIEW`, history `HISTORICAL_VALID`.

- Raw log: `evidence-weekly-20261023T194449Z/run-combined-20261023T194449Z.txt` (transcribed tool-observed, child exit 0).
  Machine: `evidence-weekly-20261023T194449Z/bootstrap-weekly-evidence.json`.

## Longform (SP001, lf-boot-1)

- FIX_ROOT: `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-longform`
  Same HEAD/tree/count. Post-run HEAD same, `git status` 12 untracked, no HEAD move.

- State: `sources/SP001/production-state.json` SHA `17c20a1e4a83f3758ee5679eacfa4bca41e9c3dfadc8928b6d7d06229ab13bc0`, VALIDATED_DRAFT prePreview, strict State [].

- Old canonical candidate (preserved, not adopted): `sources/SP001/publication/v2/publication-candidate-v2.json` SHA `9a6c4c63fb247194d5015d897851b7581bd05ff48f3ec8f3e27df69a7a107724`, `READY_FOR_PUBLICATION_PREVIEW` before correction, byte-identical after.

- Proposal: `sources/SP001/publication/v2/editorial-corrections/lf-boot-1/proposal.json` SHA `26a2baa02eef595f457640fad28f1532097bf7f0681f4863dd0504e2a59b0653`, `REVIEW_REQUIRED`, after-capture refusal OK.

- P2R manifest SHA `8bcff592a3f3ba32512c244c5bb2012148ee84fa3fe131216b2cbd21c55d9acc`.

- Scope SHA `847a9b0ea85d2730c9bff7fb866b3a86c23de2133f377e646438137dc4b8db08`.

- P2V `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`.

- P3S staged manifest SHA `d1bdbb927b6b3c2cba1ab36602ee93fa1428d31996671cebec4a3884aef9ab83`, code_deps 50.

- Specs: manuscript SHA `b101512800f78cbaa8c445a4f7e137717154ce028cda18150bfa27b5636e23d2`, toolchain SHA `6f3f9098cee64763e59270d466e1c4c25634c57336cc476ef03239649250abe5`, same fixed recipe.

- Prepare REAL TL2026 dt 29.8s:
  PDF `.../lf-boot-1/publication/build/main.pdf` SHA `12e2bdfb0aabe4d3d7ca9df3600e565a26de067e8b8e7104a1fd9ff26d8e7a48`, 79530B, 5 pages.
  Log `.../build/main.log` SHA `f3a80a9c111f2e33bef885b8e9b6649246b08b2fe888a04902aa0dba74affb61`, 94029B.
  (Longform real multi-page asserted >=2, observed 5.)

- QA 4-checks (actual `expected_checks_by_kind`): deterministic-checks 4, synthetic reviews via actual builders (section-locations, page-plan, layout bindings, clearly synthetic).
  Semantic SHA `d2349563...`, visual SHA `231a0ed0...`.

- Seal: `.../lf-boot-1/publication/publication-set.json` SHA `b890d1b8c0b998cf6983f2a45974ea0ee1cc3789a43b87f51b78995ae8a59940`, validate OK.

- Record: `sources/SP001/publication/v2/publication-surface-revalidation-r1.json` SHA `2bd14fc72491efb30bd0b137960c9b72058f86eb3e1c1bd0b17e068736f38c7e`, supersedes None, same VALIDATION_CHECKPOINT anchor pattern.
  Selection `VERSIONED_ACTIVE` → `.../lf-boot-1/publication/publication-candidate-v2.json` (NOT old canonical), receipt SP001, Gate PASSED, history HISTORICAL_VALID.

- Raw log: `evidence-longform-20261023T194449Z/run-combined-20261023T194449Z.txt` (tee-preserved, PIPE_EXIT 0).
  Machine: `evidence-longform-20261023T194449Z/bootstrap-longform-evidence.json`.

## Toolchain / provenance (both)

- lualatex LuaHBTeX 1.24.0 TL2026, biber 2.22, python 3.14.4, jsonschema 4.23.0, pypdf 6.16.2.
- Source commit `721a04d` message `SOURCE R7b TEST-ONLY...`, tree `ac7cb0...`, manifest `source-manifest-r7b.json` count 721.
- M1 HEAD `a8890d4` clean, proof-copy 57 unchanged, reconstruct HEAD `c5b0d7c` (plus untracked packet).
- No lifecycle/provider timeout errors (both prepares ~27-30s, no assumed PASS). No freeze/adoption/Human approval.

## Handoff (read-only copy)

- Use FIX_ROOT worktrees as renewal immediate predecessors (ACTIVE prePreview, exact record/set/state paths + SHAs above).
- Do NOT edit M1 candidate-work or proof-copy. DBs are isolated (no alternates, inert origin, inode-disjoint).
- This packet is milestone (both fixtures), NOT whole-operation complete. Remaining: typed renewal U/C (incl. C→U→U), renewal→editorial, normal direct lifecycle, failure/resume, affected regressions, independent final review.
