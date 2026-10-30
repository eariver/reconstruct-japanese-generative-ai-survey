# Full-lifecycle witness Attempt 6 — evidence note (General)

Date: 2026-10-28 UTC. PrePreview exposure + editorial/renewal probes under the
KNOWN snapshot (fixed2, old H/C1-pending); new fixed copy with latest H/S
awaits C1 change message + root coordination (NOT created here; live candidate
never captured while C1 edits history wiring). No whole PASS claimed for
editorial/renewal/G71-G76; no Commit Point.

Frozen execution base (unchanged from Attempt 5):
`.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed2-20261028T192129Z`
(758 files; pre-manifest `258331f1…`; own tests now `e26eaa6b…` + helper
`dc76b2e7…`; B lifecycle fix + C2 4-file overlay in place; base HEAD
`409b292…`/tree `8ce36998…`). Runtime pins unchanged (3.14.4 / jsonschema
4.23.0 / pypdf 6.16.2 / TinyTeX lualatex+biber; no GIT_* overrides;
process-scoped identity; inert origin; no network/install/old-runners).

## Contents (this dir)

- `dm022-full-v2-raw-20261028T200830Z.txt` (SHA256
  `84831435370ee1bbbdfa596e2ea3e763d8e0027ae8b9c11d963b03da3c1b8702`):
  definitive 12-test transcript on current test sources, exit 0, 372.629s —
  12 ok (both routes DM022→7-slot→regen→stage→Architecture approval→Draft→
  REAL PDF→admission→Candidate→Preview→Freeze→RELEASED, present-old-7slots,
  repeat, wrong-role; per-step pids/exits retained in-test).
- `dm022-manifest-raw-20261028T212643Z.txt` (SHA256 `44b4bc1f…`, exit 0):
  prePreview fixture-manifest test (both routes rebuilt to VALIDATED_DRAFT with
  corrected PREARCH; manifest packet dir
  `../full-lifecycle-v2-fixture-manifests/prepreview-both-routes-<UTC>/`).
- `dm022-renewal-probe-20261028T213125Z.txt` + `dm022-renewal-probe.py`
  (SHA256 `68c43312…` / `8e6c6d19…`, probe exit 2 = target refusal, not setup):
  renewal U `prepare_renewal` on fresh VALIDATED_DRAFT → `BASIS_ENTRY_INELIGIBLE:
  State pointer must select a nonnull versioned active set` (needs prior
  VERSIONED_ACTIVE set; first-activation bootstrap is C1's pending dual-epoch
  work, not a wrong-runtime adaptation).
- `dm022-p1-probe-20261028T213256Z.txt` + `dm022-p1-probe-20261028T213310Z.txt`
  + `dm022-p1-probe.py` (probe exits 2): P1 editorial-correction entry on kept
  VALIDATED_DRAFT fixture → (a) `pending publication requires changed
  publication bytes` (probe-setup gap, fixed by genuine marker change), then
  (b) B-owned `_verify_preserved_provenance` refuses the PREARCH research node:
  `revalidation basis checkpoint completeness invalid: ... 'from_state' is a
  required property` (exact traceback preserved; ROOT §3 detached
  research-history dispatch vs legacy-shape demand — for root disposition,
  B-owned `survey_agent_control_v2.py`, NOT patched).
- `dm022-debug-surface2.py` (SHA256 `c3ae87ad…`): THEMATIC surface locator
  probe (setup scaffolding; the -D### finding it chased was resolved in-test
  via clean canonical URL + entity name, no code change).
- `private-source-manifest-20261028T213412Z.json` (SHA256 `e8fa9f65…`):
  758 intended files, post-run pins.
- Prior attempt dirs + retained PDFs/full TeX logs/author inspections
  (`../full-lifecycle-v2-retained/`, run-unique, now 15+ runs) preserved;
  nothing overwritten or discarded.

## G71 base verified (read-only, no action)

- `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  exists, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (actual409/tree8ce per
  AGENTS pin) — genuine historical G71 source epoch for the future control. No
  fixture DB created from it here; the G71→G76 dual-epoch renewal run awaits
  C1's renewal construction + root disposition (C1: H-positive dual-epoch
  pending, affected batch incl. P3S-26 re-run and source_phase_s 3 faults).

No foreign file modified; no live-candidate execution; no Human readback,
ordinary commits, Git config, network, or cleanup. Whole NOT_READY preserved.
