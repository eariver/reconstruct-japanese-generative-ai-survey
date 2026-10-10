# LF-2I R3 correction evidence qualification

2026-10-10. Correction implementation Co-Worker closeout for root R3
 findings (P1–P3). Not independent review. Correction2 packet and its
 independent BOUNDED_PASS are preserved untouched; prior 44- and 42-method
 results are historical evidence only — no PASS transfer claimed.

## Source identity (fixed final hashes)
- Design copy `/tmp/opencode/jgas-lf2-design-20261009T113013Z`, HEAD
  `409b292756dd1277b9dfae87679934c0d2ce251c` (unchanged, no commits),
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- Changed this round (2 files, same publisher+test budget):
  - `scripts/survey_longform_semantic_publication_v2.py`
    `4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195`
    (was correction2 `71ef7b…`)
  - `tests/test_survey_longform_publication_integration_v2.py`
    `4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4`
    (was correction2 `61a3491a…`)
- Unchanged (7 files, all modes 664): derivation `c09c55…41149`, helper
  `d480e1…97d3c2`, gate runtime `e73058…bbe4`, gate schema `fe4a96…13322c`,
  receipt schema `4dadf8…3e8ca`, reader schema `7bae9d…d0643`, LF-1 test
  `ce6874…f913`.
- Actual code uses the context ref for P2: `_snapshot_inputs` selects the exact
  named `drafting-archive` row from `context["authored_refs"]`, runs it through
  strict `_safe` directly (no `_rel`-resolve-first), and compares file SHA to
  the recorded ref hash. No such claim is made beyond this code.
- No candidate/reconstruct commits, branches, refs, or fixture-DB writes; no
  original/LF1/verify-copy/409-DB mutation; no network, Production actions,
  subagents, DM021 repair, or `EXCEPTION_*` path. `config/*.json` untouched;
  no global CAS, no new paths/roles/framework.

## What changed per finding
- **P1**: `_capture_lexical_bytes` deleted. Raw-first `_safe(root,raw,label)`
  now runs BEFORE ANY content read; captures are taken from the validated
  paths, with the post-derivation/post-validation stability checks retained.
  Proven by new `test_alias_outside_sentinel_never_opened`: State leaf and
  input parent aliases pointing at outside FIFO sentinels refuse via
  containment with threaded read observation (any open would block; both
  refused promptly, sentinels never opened, no-write).
- **P2**: snapshot archive path/hash come from the exact named
  `drafting-archive` context ref (compared, not freshly adopted). New seam
  (h): archive drifted immediately after real `load_derivation` returns but
  before `_snapshot_inputs` refuses pre-mkdir/pre-write with an
  injected-archive-only delta. Existing later archive drift tests (c)/(e)
  preserved.
- **P3**: every `_recheck_snapshot` re-runs the ACTUAL
  all-control-root/committed-source predicate (`verify_tool_basis` with the
  validated recorded commit/closure), replacing the 14-file equality. New
  seams with an unlisted tracked helper under the `scripts` control root
  (`survey_stage_validation_v2.py`, outside CURRENT_CLOSURE): (i) drift after
  initial verification refuses pre-write with no outputs; (j) drift during
  the final write refuses pre-receipt with the retained set and no receipt.
  No Core-change renewal or hash absorption.

## Verification (new runner `run_lf2i_correction3.py`, new logs/pins)
- Proofs PASS (same-guard A/B/C on new full disposable composites);
  pre/post identity PASS (all-9 hash+mode pins, HEAD/tree/parent, exact
  2M+7A set); child exit 0, no timeout; forced no-network Git env for runner
  git + children; routing/optimization overrides rejected per git op.
- Suite: **43 tests OK in 1822.421s** — full focused LF-2I integration module
  (13 methods incl. new sentinel test and extended seam suite) + Gate module +
  3 LF-1 loader controls at the fixed final hashes above. `run.log` holds raw
  per-test outcomes; manifest holds runtime/exits/modes metadata.
- E3: exact SAVED `complete-overlay.patch` applied as saved (`--check` then
  apply, both exit 0) to a NEW `cp -a` byte-copy of ORIGINAL clean 409 at
  `/tmp/opencode/jgas-lf2i-409bytecopy-20261010T033640Z` (correction2's copy
  preserved): pre HEAD-409 clean/inert/no-alternates with 0 shared object
  inodes; post HEAD-409, status exactly 2M+7A, all-9 bytes + physical modes
  match, logical `ls-files -s` modes recorded.
- Normal healthy FROZEN/RELEASED readback and both same-issue manuscript
  stage-Gate backstops retained green; DM021 remains explicit non-goal.

## Preservation / limits
- `preserved-9/` holds exact pre-edit bytes (correction2 finals) of all 9
  files; correction2 packet, both byte-copies, and all prior logs/reports
  intact. New unique dir, exclusive-write evidence only, no overwrites.
- `__pycache__` side effects never blindly deleted; TMPDIR stayed under
  `/tmp/opencode` for all temporary work.
- Whole candidate NOT_READY; step4/B3 OPEN; canonical audit unstarted.
  Stop for root code/oracle/evidence review + independent scoped resolution
  of P1–P3 (and correction2 claims). No automatic next unit; no Commit/Push
  (ordinary reconstruct commit remains Human-owned).
