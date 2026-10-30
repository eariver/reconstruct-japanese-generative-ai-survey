# Full-lifecycle witness Attempt 3 — evidence note (General)

Date: 2026-10-28 UTC. First real blocker reached; foreign scope NOT patched.
Private frozen source `/tmp/dm022-full-lifecycle-private-20261028T120000Z`
(same as Attempts 1–2: base HEAD `409b292…`/tree `8ce36998…`, 758 files,
manifest SHA256 `58fc324e…`). Runtime 3.14.4 / jsonschema 4.23.0 / pypdf 6.16.2.

## Contents

- `dm022-full-v2-test-raw-20261028T163336Z.txt` (SHA256
  `6a1d896394a8906ba358a9e165b4cbb6cb032dc713db14c8c6199573c03a59bd`):
  full 7-test witness transcript, exit 1, 97.441s — 5 ok, 1 error
  (present-old-slots, Blocker 1), 1 failure (draft, Blocker 2). Preserves both
  tracebacks verbatim (runner line 252/78; drafting base line 461/389/244;
  screening line 707).
- `dm022-dual-repro-20261028T163326Z.txt` (SHA256
  `4c9c3ec5319a0e3367b938958d385be870834ee95d4b8eb3fb895d8a289897d4`):
  minimal-repro probe transcript, probe exit 0 — Part A and Part B both
  reproduced with exact signatures, incl. triplet refs, resolver family,
  strict-State errors, legacy-branch health, canonical SHAs, and the one real
  advance DISCOVERY_COLLECTED.
- `dm022-dual-repro-probe.py` (SHA256
  `67efd4e6b6371d851a7457f0679d115003d1cd95d452a2742e1d4b440de5092b`):
  exact probe source (imports only General's own new test helpers from the
  frozen private copy; builds fresh independent fixture DBs with process-scoped
  identity, inert origin, meaningful commits; no fixture objects in
  reconstruct, no ordinary commits, no old runners).
- `private-source-manifest-20261028T163527Z.json` (SHA256
  `58fc324e94bb970743ea81a5a5a9713b052169417cbc8587f7f0c5507ede6027`):
  758 intended files (own test file `899ff146…`/63094B with 3 new tests;
  fixture helper unchanged `dc76b2e7…`; rest frozen).

## Owner-code failures returned to ROOT (summaries; full detail in progress doc Attempt 3)

1. B-owned `scripts/run_selection_architecture_v2_interactive.py`
   `_dm022_resolve_ledger_completeness:78`: triplet-shape heuristic says
   PREARCH on LEGACY same-triplet states; kind dispatch says LEGACY; runner
   raises instead of using the healthy legacy branch. Blocks disposition §4
   present-old-slots case.
2. `scripts/survey_screening_v2.py:704-707` (`validate_package_basis`,
   called by `scripts/survey_drafting_v2_base.py:244`): preparation-era State
   SHA pin vs any later faithful State advance (proven with one real advance,
   no DM022). Blocks all drafting and everything downstream.

No foreign file was modified; no live-candidate execution; no Human
commit readback; no ordinary commits. Whole unit remains in progress; no
Commit Point claimed.
