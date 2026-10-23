# Correction R1 history (Group L)

Root `CHANGES_REQUIRED` (`independent-draft-lc-review.md` + `astra-draft-review-r1.md`).
This directory preserves the R1 draft before correction edits.

- `initial-bytes/`: exact R1 working-tree bytes of all 5 L-owned paths
  (hashes verified equal to `group-l-sha-diff-20261021T120000Z.md` pins).
- `group-l-sha-diff-20261021T120000Z.md`, `group-l-test-20261021T120000Z.md`:
  copied R1 hash/diff report and pure-test log (10/10 pass after fixing the
  initial `derive_anchor_empty_chain` fixture ERROR: checkpoint schema required
  `contract` 8 keys + `CORE_STAGE_CONTRACT` review + 3 validation artifacts;
  fixture fixed, source not weakened).

No reset/clean/raw-delete/commit/network. DST source copy unchanged
(`409b292`, same HEAD/tree). Corrections below edit L-owned paths only.
