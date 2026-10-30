# Full-lifecycle witness Attempt 7 — evidence note (General)

Date: 2026-10-28 UTC. Frozen fixed3 (C1 H/S epoch-presence correction: H
`a9de2c97…`, S `b139f493…` unchanged Layer-B, presence tests `a8ce8794…`,
phase_s G76 `71d67aa9…`) + B/C2 fixes intact + own 2 tests (`0daa7ef9…`/
`dc76b2e7…`). New 4th fixed copy (never mutated old ones; live candidate never
executed while C1 edits). Runtime pins unchanged. No whole PASS for
editorial/renewal/G71-G76; no Commit Point.

## Frozen source

`.rephase-1-editorial-runtime/dm022-full-lifecycle-fixed3-20261028T213853Z`
(759 files: fixed2 758 + new C1 presence test). Pre-manifest SHA256
`e28f31f10a173ea49992ac8ec70f81cba2aef7a565d0dc0cf069062d035dd00f65`
/156553B-equivalent. Post-manifest SHA256
`de991a8c0b14d04033a16790ab25a1c969a1dddca4286f0f7aae03052d2fe20e1`
(759 entries): only own test file changed during the attempt
(`8c7901db…` → `0daa7ef9…`); all runtime files byte-identical to freeze
(no hot-edit of admitted fixture tools; no C2/B/A edits).

## Contents (this dir)

- `dm022-edfull-raw-20261028T214720Z.txt` (`8275118c…`): P1→P2R setup failure
  (P2R session needs fixture-local runtime modules; harness fixed by copying
  scripts/ + .github + dotfiles — setup, not target).
- `dm022-edfull-raw-20261028T214920Z.txt` (`4a343d25…`): same setup class
  (control path `.github/workflows` missing; harness fixed).
- `dm022-edfull-raw-20261028T215138Z.txt` (`2bc0bd79…`): P2R capture SUCCEED
  (`RETAINED_SET_CAPTURED` + manifest); my assertion literal was wrong
  (`CAPTURED`), fixed — setup, not target.
- `dm022-edpub-raw-20261028T221123Z.txt` (`6b9c4810…`): FIRST real foreign
  blocker on the editorial path — P3S materialize subprocess passes fixture
  binding, then editorial `prepare_publication` refuses:
  `EditorialError: CLOSURE_SHAPE: [PREPARE/REFUSED_PRE_WRITE] editorial closure
  expected 63, got 70` (`survey_editorial_publication_v2.py:2163`,
  `_editorial_closure_rows`). C2-owned hardcoded G71 closure count vs G76
  exact 70 from C1's `_route_code_deps` (63+2 modules+5 schemas). Verbatim
  traceback + pid + full stdout/stderr preserved (fresh subprocess raw, unique
  dirs under `../full-lifecycle-v2-retained/weekly-full-ed-pub-v2-*/`).
- `dm022-p1-probe-*.txt` + `dm022-p1-probe.py`, `dm022-renewal-probe-*.txt` +
  `dm022-renewal-probe.py` (Attempt-6 probes, first packet preservation here):
  revalidate-on-adopted (B walker PREARCH-shape refusal; R1≠P1, no park) and
  renewal-U entry gate (correct VERSIONED_ACTIVE requirement, not a bug).
- `dm022-debug-surface2.py` (Attempt-6 THEMATIC locator probe, preserved).
- `private-source-manifest-20261028T222347Z.json` (post-run pins).

No transcript overwritten or discarded; P2R staged-4 run raw lives in the
retained dir (`../full-lifecycle-v2-retained/weekly-full-edstaged-v2-*/`).

## Reached this attempt

- Editorial P1 proposal on adopted VALIDATED_DRAFT (real revised reader scope,
  `REVIEW_REQUIRED`), P2R retention capture (17 copy + 72 keep refs + manifest),
  P2V `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`, P3S staged4 materialized via fresh
  fixture-code subprocess (fixture-bound modules, pid/exit/raw recorded).
- Manifest exposure test green (prePreview both routes, packet manifest dir).

## Blocked (foreign, NOT patched, returned to root)

1. **C2 editorial closure hardcoded G71 (63) vs G76 exact 70** —
   `survey_editorial_publication_v2.py:2163 _editorial_closure_rows`
   (`len(rows) != 63`). Route deps are generation-aware (C1 P3S 63/70); the
   count predicate is stale. C2-owned fix (derive expected count from route
   family like C1's generation derive, or drop count for exact membership).
   Blocks editorial prepare/finalize/activate/readback → VERSIONED_ACTIVE →
   renewal U/C + normal release, G71→G76 control.
2. Renewal U entry correctly requires prior VERSIONED_ACTIVE (not a bug; first-
   activation bootstrap is C1's pending dual-epoch work + my VERSIONED_ACTIVE
   fixture, blocked behind (1)).
3. R1 revalidation on adopted state is NOT P1's prerequisite (misclassification
   corrected per instruction; B fixes its PREARCH walker independently).

Whole NOT_READY preserved; no live-candidate execution; no Human readback,
ordinary commits, Git config, network, cleanup, or old runners.
