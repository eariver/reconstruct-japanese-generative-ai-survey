# R3c return — versioned receipt/P1 graph adaptation + both second corrections (internal)

## Code delta (DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`, edits via dedicated Edit only)
1. `tests/test_survey_publication_set_v2.py` (`8768275e…`, was `e2f3…` pre-R3c tracked):
   legitimate update of `test_r1_anchor_and_live_effective`: canonical7 is now
   the ANCHORED cumulative effective (== effective7, live v2 bytes), exact 4-key
   rows with live-derived byte_count. Prior buggy expectation output preserved in
   `correction-r3/r3-existing-low-agent-stderr.txt` (FAIL `5c02…` vs `17e6…`).
2. `scripts/survey_editorial_correction_proposal_v2.py` (`23e3a45f…`, 136407B):
   - `_dispatch_generated_receipt`: unknown receipt kind now explicit
     `RECEIPT_KIND_UNKNOWN` (no silent pass-through); H call gets repo-relative
     refs (absolute-pin boundary fix); legacy kind absence stays on strict schema.
   - Versioned branch: generator_route agreement check; early scope via pinned
     exact `scope_review_ref` (no `semantic_review` alias); authored roles
     exactly `{proposed-publication-authoring, accepted-draft-archive}`;
     FULL accepted list compare vs before_context via shared `_frozen_names_check`
     + path equality (no validation-checkpoint fake; original checkpoint identity
     stays State/proposal/activation-bound).
   - Stale editorial `pass` block removed; pre-TeX review for editorial loads the
     exact scope review targeting the active-before reader (same proposed scope
     target equality, no copied review path).
   - `_build_graph`: `FROZEN_REF_PREFIXES += accepted-draft-archive`;
     proposed-publication-authoring mutable COPY; pretex_rel scope-aware;
     versioned KEEP discards all prior-versioned receipt-owned paths (receipt,
     reviewed input, outputs, quality results, pre-TeX/scope, authored inputs)
     with live State COPY preserved; new prior seal/staged/proposal/retention
     nodes + edges (P2R proof enumeration); gate review binding exact vs scope
     target for editorial; authored loop classifies the new names.
   - `_final_full_receipt_recheck`: H recheck call relativized (`col.rel`);
     ordinary paths untouched (no P1 public post-capture bypass introduced).
   - Untouched per instruction: original-rows canonical check (agent roles),
     effective-vs-15-seal (low), P2V receipt flags (none; shared path), retention
     manifest metadata path behavior (no change).
3. P2V/P2R/P3S/low/agent: no further edits needed (R3 low+agent already in).

## Regressions (clones of committed SOURCE, never DST; bytecode contained outside source)
- `reg1` (SNAP2 clone): focused6 + low18 + agent5 + schema-cache6 = **35 pass, exit 0**.
- `reg3` (SNAP3/final clone): same 35 = **pass, exit 0** (validates final bytes).
- P1-9 + retention-25: setup errors in old helper sandbox (temp fixture lacks
  `.latexmkrc`; `aggregate_file_hash` fails before P1 logic). Pre-existing helper
  gap, unrelated to this logic (same failure on unmodified P1 paths). Needs root
  decision: test-helper-only sandbox fix (helpers not in worker edit scope).
  e2e below covers P1/P2R/P2V/P3S/H for real instead.
- `reg2` combined batch hit the 900s tool timeout (P1/retention setup errors +
  slow staged/current-authority suites); superseded by reg1/reg3 + e2e.

## ACTUAL second corrections (fresh independent copies of final SNAP3 `0d9857e6…`)
- Weekly (`verify-weekly-r3c-20261021T150000Z`, script BEFORE execute, unique raw):
  bootstrap canonical → wk-r3c-1 full cycle → ACTIVATED (anchor
  VALIDATION_CHECKPOINT, supersedes null, HISTORICAL_VALID, VERSIONED_ACTIVE) →
  wk-r3c-2 (new headline): P1_PREPARE ok (was VERSIONED_ROW_SHAPE) → P2R →
  refusal-ok → scope → P2V_SCOPE_BOUND → P3S_VERIFIED50 → REAL TL2026 5pp →
  finalize → INERT_HEALTHY → **ACTIVATED r2, supersedes r1, SAME anchor** →
  State healthy, VERSIONED_ACTIVE wk-r3c-2 candidate, OLD_IMMUTABLE_KEEP_OK,
  receipt/Gate(PASSED)/Candidate(READY) active. **exit 0**, stderr empty.
  First active preserved before Preview (no lifecycle ran).
- Longform (`verify-longform-r3c-20261021T152000Z`, fresh copy): same shape,
  lf-r3c-1 → ACTIVATED → lf-r3c-2 → **ACTIVATED r2, supersedes r1, SAME anchor**
  → State healthy, VERSIONED_ACTIVE lf-r3c-2, KEEP_OK, receipt/Gate(PASSED)/
  Candidate active, 5-page REAL PDFs. **exit 0**, stderr empty.
- No fixture commits, no network/clean/reset/purge; pycache contained outside
  source; clones use inert origins; dirty script-debug clones excluded.

## Frozen SOURCE (untouched; no tests ran inside; status 0 clean; 0 pycache)
- Root `/tmp/opencode/jgas-editorial-r3c-20261021T144500Z/candidate-partial-b40de60`
  HEAD `0d9857e6132fb314a2e2ba141da79c54f4ec5e06`
  tree `44cbfc1864d269e338bdbd6060305e5fd558060`, 718 files, inert origin
  `https://example.invalid/workerR3c-r3c-snapshot.git`, no alternates, inode-separated.
- Valid JSON manifest `correction-r3b/source-manifest-r3c.json` (718 entries;
  manifest SHA `8f9b9aaf…77c0063`). Key pins: low `d2909bba…`, agent `05f1ee03…`,
  P1 `23e3a45f…`, old-low-test `8768275e…`, r3-focused-test `ab6c9ca4…`.
- DST HEAD still `409b292…`; prior R3 history + pre-edit archive preserved.

## Open (for root, not claimed)
- Old unit-test helper sandbox missing `.latexmkrc` (P1/retention/staged setup);
  test-only fix or accept e2e coverage.
- Normal Preview/Freeze/Release lifecycle after second activation (preserved).
- No whole-PASS/production-approval claim; placeholder quality NO-GO maintained.
