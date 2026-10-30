# Full-lifecycle witness Attempt 5 — evidence note (General)

Date: 2026-10-28 UTC. C2 release blanket-ban fix verified; overlay copy; both
routes REAL initial publication → RELEASED; PDFs + full build logs retained.
No whole PASS claimed for renewal/G71-G76 (awaiting C1); no Commit Point.

## Frozen source

- New private copy (old fixed snapshot preserved, never modified):
  `.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed2-20261028T192129Z`
  (758 files; pre-manifest SHA256
  `258331f10a173ea49992ac8ec70f89dc221e56de1fbfe6a8dc6d6e`).
- Base = prior fixed witness (`.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed-20261028T175919Z`,
  HEAD `409b292…`/tree `8ce36998…`) + KNOWN exact C2 4-file overlay from current
  candidate-work (verified byte-identical to correction pins):
  - `scripts/survey_release_checkpoint_v2.py` `a5e84668…` (was `dccad3a9…`)
  - `tests/test_survey_editorial_correction_proposal_v2.py` `36ca8afe…` (was `035d5aba…`)
  - `tests/test_survey_editorial_retention_v2.py` `403beeed…` (was `1994f16d…`)
  - `tests/test_survey_editorial_current_authority_v2.py` `cf7a5bd5…` (was `fde4c9a2…`)
  File list identical to prior copy (only those 4 contents differ). Candidate
  whole NOT captured (C1 history wiring editing in live tree, per instruction).
- Runtime pins: `Python 3.14.4`, `jsonschema 4.23.0`, `pypdf 6.16.2`,
  TinyTeX `lualatex` (LuaHBTeX 1.24.0) + `biber 2.22`, `PYTHONDONTWRITEBYTECODE=1`,
  no `GIT_*` overrides, process-scoped fixture identity, inert `example.invalid`
  origin, no alternates, no fixture objects in reconstruct, no ordinary commits,
  no Human readback, no network/install/old-runners/cleanup/Gitconfig.
- Own files only (candidate-work otherwise untouched):
  `tests/test_dm022_full_lifecycle_v2.py` `e26eaa6b…`,
  `tests/dm022_lifecycle_fixture_v2.py` `dc76b2e7…` (identical in snapshot).

## Contents (this dir)

- `dm022-full-v2-test-raw-20261028T201654Z.txt` (SHA256
  `d4c9c422e0eecdd3643cccd34ef36df348ae50745ef8e3bc2b37a5334554829b`):
  definitive full 12-test transcript, exit 0, 372.629s — 12 ok, 0 fail/error.
  Own-test pins recorded in-transcript header (`e26eaa6b…`/`dc76b2e7…`).
- `private-source-manifest-20261028T202317Z.json` (SHA256
  `c5a9d2ed1028a6996d0cc082c426459c8d4fd22ec6669be33cdf23d7aed38aa9`):
  758 intended files, post-run pins.
- This README. Intermediate attempt transcripts preserved in Attempt-4 dir
  (`full-lifecycle-v2-20261028T183023Z/`); Attempt-3 dual-repro intact;
  retained PDFs/full TeX logs/author inspections accumulate under
  `../full-lifecycle-v2-retained/<tag>-<UTC>/` (never overwritten; 14+ run dirs).
  No prior log edited or discarded.

## Scope achieved (actual public APIs, both routes)

- DM022 prepare→external decision→adopt→repeat, 7-slot retain/clear/regenerate
  (absent AND present-old cases), ordinary regeneration (audit no-overwrite),
  stage advances through SELECTION_COMPLETE, both-route Architecture approval
  (genuine-type synthetic Gates, explicit nongenuine reviewers, clear labels).
- Both-route Draft (accepted-state facade) → DRAFT_COMPLETE.
- Both-route Reader → REAL lualatex+biber PDF (isolated disposable builds, every
  step pid/exit/full-log recorded; `%PDF` magic + pypdf page counts asserted;
  exact byte transfer to canonical survey roots) → author inspect loop
  (explicitly NOT independent visual) → manuscript → QA → synthetic reviews →
  gate → VALIDATED_DRAFT with strict State validation + PREARCH readback.
- Both-route VALIDATED_DRAFT → Candidate → Preview approval →
  Freeze → merge-verification + release-record → release-checkpoint CLI →
  RELEASED (terminal COMPLETE), wrong-role publication pointers still refuse.
- Retained per route+run: real PDF + main.tex/bib/sty + full TeX logs +
  manifest/QA/reviews/gate + author inspection + retained-manifest with PDF digest.

## NOT reached (reported, waiting — no foreign patch, no downgrade)

- Later editorial + versioned renewal Preview/Freeze/Release: needs C1's pending
  H-positive + P3S/affected batch (`author-C1-historian-wiring-correction.md`
  §§4–5: H verifier + S source proof + renewal graph on tool-commit-predates-CP
  fixture; full P3S 26 needs ~2210s; G71/G76 copy lists + genuine epoch work).
  Current C1-old would block renewal; per instruction, report then wait — no
  renewal witness attempted against uncorrected C1, no C1 files touched.
- G71→G76 unchanged-upstream compatibility control with genuine historical G71
  epoch (read-only final93 proof copy) + new G76 committed tool epoch: needs
  C1's corrected renewal machinery; membership counts are not the control.
- THEMATIC/WEEKLY HELPERS: other workers' regression exec frozen elsewhere;
  General touched ONLY the 2 own files.

No foreign file modified in any copy; old snapshots preserved; no live-candidate
execution (all runs in frozen ignored-runtime copies); no Human Commit Point.
