# DM021-P1 Phase B implementation report (General worker → Astra review)

Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(detached HEAD409b292/tree8ce36998, no branch/commit/network/Production ops).
Final overlay exactly 13 paths (3M10A relative 409), no extra path decision needed.

## Delivered paths (exactly 3A+1M on the restored LF2I baseline)

- A `scripts/survey_editorial_correction_proposal_v2.py` (~700 lines):
  `prepare_proposal` / `validate_proposal`, read-only, zero writes/approval/
  reason/State-adoption/CLI/PASS. Layered pipeline: safe paths → strict State +
  eligibility → original checkpoint → State-bound active record (or verified
  absence) → manuscript → receipt routing parse → independent before/proposed
  derivation with canonical checks → full receipt validation → full Gate
  validation → pre-TeX scope loader → bundle → finite graph/retention/digests →
  entry/exit snapshots (consumed bytes, full edition trees, HEAD, config).
- A `schemas/editorial-correction-proposal-v2.schema.json` (`schema_version`
  `2.0-rc1`, `route` EDITORIAL_CORRECTION_PROPOSAL_V1, `renderer_commit` 40-hex
  commit, full `basis`/`proposed`/retention keys).
- M `schemas/reader-surface-semantic-review-v2.schema.json`: optional strict
  `editorial_correction_scope` block only; ordinary records unaffected.
- A `tests/test_survey_editorial_correction_proposal_v2.py` (5 tests, ~800 lines).

## Selection resolutions implemented

- Frozen digest is ONLY immutable authority refs (profile/architecture/approval/
  summary/attention/accepted Draft/Synthesis/Evidence/Discovery/Selection/
  Matrix/Materiality/authored archives); before-graph/before-reader/State/QA/
  tools excluded. One deterministic path-based KEEP/COPY policy (no first-wins);
  HASH/POLICY conflict guards retained; original rows are metadata, never live
  old-SHA nodes; active rows bind effective bytes.
- Scope: pre-TeX loader with expected AFTER only; raw bytes captured BEFORE the
  loader, disk re-compared after, object digest bound to captured JSON; block
  read from captured bytes. `reader.validate_review_record` used only for later
  reviews. NoScope/OrdinaryWithoutScope → REVIEW_REQUIRED; malformed/non-PASS/
  wrong/stale/REJECT/needs-Owner → typed refusal, never bound.
- Canonical: proposed FILE vs independently rederived bytes; NO_EDITORIAL_CHANGE
  on canonical equality (runner-only/format-only excluded); noncanonical before
  explicitly refused. `proposal_id` grammar + layout/overlap/retention-dest
  rules enforced.
- Predecessor: real derivation-only fixture commit (TeX-comment literal) +
  regeneration with REAL producers + honest QA cascade + genuine
  REVIEWED_CORE_CHANGE record. Epoch honesty finding preserved: post-commit
  replay executes the fixture's COMMITTED code in a sanitized subprocess
  (ambient code cannot replay a committed revision); fixture source commits
  include all untracked P1/LF2I bytes with process identity, no empty commits.

## Test evidence (no old PASS transfer)

Strict runner per attempt (deps → 3M10A freeze → sanitized env → unittest →
finally-post freeze): 13 attempts preserved, all failures analyzed in
`attempt-*-analysis.md` files. Final attempt-13 (`evidence-20261011T201412Z-phaseB`,
1456.586s): **32/32 OK** (5 new P1 + 27 affected gate-control tests),
pre/post HEAD/tree/status/files identical. Runtime Python 3.14.4, jsonschema
4.23.0, pypdf 6.16.2, no installs/network.

## Final patch

`complete-p1-overlay-13path.patch` (474,268 bytes, SHA256
`5f087f1373d8e532b33ec58530f8567e81f23ded6c01391bcf37a6c38df8f459`),
base HEAD409/tree8ce, 13 diffs; all 10 new files verified byte-identical by
reconstruction from the patch. Saved with generator + freeze files in the
passing evidence dir. No candidate commit; ordinary reconstruct Commit/Push
remains Human-owned.

STOP for Astra code/oracle review, then fresh author-independent implementation
review. DM021 remains OPEN (P1 preparatory, not repair).
