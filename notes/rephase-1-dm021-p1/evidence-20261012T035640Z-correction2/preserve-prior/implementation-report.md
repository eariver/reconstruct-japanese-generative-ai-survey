# DM021-P1 correction implementation report (worker → Astra + independent review)

Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(detached HEAD409b292756dd1277b9dfae87679934c0d2ce251c/tree8ce3699861505f32d1d60bdc185d4d4f635aedb2,
no branch/commit/network/Production ops). Final overlay exactly 13 paths
(3M10A relative actual409), only selected 3A1M changed; LF2I 9 pins preserved
except additive pre-TeX schema (P1 M, unchanged bytes).

## Final pins (freeze-pre, pre==post)

- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  status exactly 3M10A (see `freeze-pre.json`==`freeze-post.json`).
- M `schemas/reader-surface-gate-v2.schema.json` `fe4a96f4...` 6894B 0o664 (LF2I preserved)
- M `schemas/reader-surface-semantic-review-v2.schema.json` `e8598239...` 4219B 0o664 (P1 M, unchanged)
- M `scripts/survey_reader_surface_gate_v2.py` `e7305884...` 94511B 0o664 (LF2I preserved)
- A `schemas/editorial-correction-proposal-v2.schema.json` `5623c0d9...` 3945B 0o664 (corrected)
- A `schemas/longform-publication-source-manifest-v2.schema.json` `4dadf873...` 2720B (LF2I preserved)
- A `schemas/longform-reader-input-v2.schema.json` `7bae9d2a...` 10624B (LF2I preserved)
- A `scripts/survey_editorial_correction_proposal_v2.py` `9f3aea25...` 82601B 0o664 (corrected)
- A `scripts/survey_longform_derivation_v2.py` `c09c5558...` 62260B (LF2I preserved)
- A `scripts/survey_longform_generated_v2.py` `d480e11d...` 39992B (LF2I preserved)
- A `scripts/survey_longform_semantic_publication_v2.py` `4d235a38...` 36224B (LF2I preserved)
- A `tests/test_survey_editorial_correction_proposal_v2.py` `a7b04dc1...` 87348B 0o664 (corrected)
- A `tests/test_survey_longform_derivation_v2.py` `ce687447...` 91161B (LF2I preserved)
- A `tests/test_survey_longform_publication_integration_v2.py` `4a03b564...` 107757B (LF2I preserved)

Initial P1 bytes/logs preserved untouched in `initial-preserve/` (4 files at
118d49e5/54b17f05/e8598239/1b62b2d7 + `complete-p1-overlay-13path.patch`
5f087f13/474268B). No edit to old packets, no reconstruct commit/branch.

## R1 — frozen/graph/retention (full, not partition-only)

- `_frozen_member_kind` partition bug fixed via `startswith("receipt:accepted:")/
  "receipt:authored:"/"upstream:"` + `_frozen_kind()` gate; deterministic sorted
  scan; new `_frozen_member_kinds()` preserves ALL union roles (one frozen entry
  per `(kind,path)`). `FROZEN_REF_PREFIXES` drops mutable
  `publication-semantic-input`/`publication-authored-input` (now `None`, COPY);
  keeps `drafting-authored-archive`/`drafting-archive` (frozen, KEEP) plus all
  accepted authority (`production-profile`, `issue-architecture`, `synthesis-*`,
  `draft-package/result`, `evidence-acceptance`/`evidence-card:*`,
  `candidate-matrix`, `materiality-ledger`, `discovery-acceptance`, etc.).
- Graph adds live `state:authority` node (COPY), full `supersedes` predecessor
  chain walk (limit 32, cycle/issue/prior/chronology checks, `PREDECESSOR_CHAIN`
  edges), `STATE_CHECKPOINT`/`STATE_ACTIVE_RECORD` edges, bundle
  `production-profile`/`source`/`pdf` nodes + `BUNDLE_SOURCE/PDF_DIVERGED`
  equality, later-review manuscript/source/pdf NODES (not edge-only) + exact
  `LATER_REVIEW_DIVERGED` equality to effective, canonical Candidate from
  validated `profile.paths.source_root` (not `parent.parent`) + all 6 bindings
  (`reader_manuscript/source/pdf/quality_bundle/semantic_review/visual_review`)
  + `CANDIDATE_INVALID` wrapping, mutable now includes ALL effective (later
  reviews included), State, pre-TeX review, candidate, publication-authored
  COPY; tools/checkpoint/prior records/frozen KEEP. `HASH_CONFLICT`/
  `POLICY_CONFLICT` preserved; `UNCLASSIFIED_DEPENDENCY` allows mutable
  publication-authored operational, otherwise stops (no generic resolver).

## R2 — persisted binding (no silent repair)

- Schema: `basis.active_revalidation_ref` required nullable; `proposed`
  requires `proposed_reader_ref` + `proposed_reader_canonical_sha256` (ref sha
  must equal canonical sha); retention removes singular `role`, keeps sorted
  `roles`, enforces `retained_ref XOR retained_dest` via `allOf/if/then`.
- `_pipeline` derives `expected_proposal_dir` from validated `source_root` +
  `proposal_id`, requires authoring ALREADY at
  `<proposal_dir>/authoring-input.json` BEFORE prepare (`AUTHORING_NOT_STAGED`
  otherwise; fixtures stage outside P1, P1 writes nothing), planned reader ref
  prospective (`<proposal_dir>/reader-surface-input-v2.json` + canonical sha,
  file need not exist at prepare). Author-supplied `change_description`
  (nonempty, new optional `prepare_proposal(..., change_description)`) preserved,
  not forced to placeholder. `_proposed_upstream_check` (proposed vs before
  accepted/archive/profile) + `_frozen_names_check` (receipt vs before) after
  validated receipt.
- `validate_proposal` compares ALL (`schema_version/proposal_id/issue_id/
  research/publication/route/status`, `basis`, authoring PATH+sha, reader
  PATH+sha/canonical sha, retention exact), allows any nonempty description,
  requires exact canonical dir (not final2 names), safe/alias/regular checks for
  all three `PROPOSAL_FILES`, exact staged FILE bytes, returns supplied proposal
  UNCHANGED + separate `measured` binding (no inserted `proposed_reader_sha256`).

## R3 — raw-first safety / canonical State / token

- `_Collector` root normalized once; `safe()` lexical `..`/`\` checks + leaf
  `is_symlink` + ancestor symlink walk BEFORE `resolve()`, post-resolve
  containment + `lstat` `S_ISREG` (no FIFO/device/dir/symlink open) + pinned
  bytes + stability; `reverify()` rechecks ancestor alias + `S_ISREG` + bytes +
  HEAD + config (config via `safe`, not direct read). Config loads from pinned
  bytes. Canonical State enforced (`source_root/authoritative_filename` via
  `repo_local_path`; clone `STATE_NOT_CANONICAL`). `PROPOSAL_ID_RE` uses
  `fullmatch("[a-z0-9][a-z0-9-]{0,63}")` (trailing newline refused). Retention
  dests get raw ancestor alias checks even when absent (prospective, incl.
  dangling alias), namespace overlap (exact + ancestor/descendant) vs live
  inputs, absent-required (no overwrite). Public-API controls covered in matrix
  (traversal/alias/ancestor/FIFO/shadow/newline).

## R4 — root-anchored snapshot + late rechecks

- `_tree_map` resolves edition bases against `root` (never CWD), rejects symlink
  dirs/files, FIFO/device (`TREE_NOT_REGULAR`), never silently skips symlink
  dirs; CWD-independence proven in drift test (`chdir("/tmp")` still equal).
  Pins before consumption (State/Profile/checkpoint/effective/manuscript/Gate/
  receipt/archive/reader before validators reuse); `col.reverify()` + `_tree_map`
  recheck after scope in `validate_proposal` (tree check no longer ends inside
  `_pipeline` before scope); all-control/current-receipt predicates rechecked
  after scope (`contract_identity` equality); proposed vs before upstream
  equality (`_proposed_upstream_check`); late mutation seams exercised (upstream/
  container/record/control/scope bytes at late phases with injected-delta vs
  forbidden-write separation in drift/candidate/binding tests).

## R5 — tests (honest R1, each-call no-write, full sets)

- Existing emitted-TeX-comment cascade relabeled as generic Core-change
  (`test_honest_predecessor_original_vs_active` docstring, staged flow, no-write
  each). New `test_r1_mechanical_refresh_owner`: non-emitted Python
  comment-only commits (2×) with unchanged reader/output bytes + two successive
  `survey_weekly_mechanical_refresh_v2.refresh_mechanical_evidence` via
  fixture-committed code (sanitized subprocess, process identity, inert origin),
  supersedes chain depth (`record.supersedes` non-null), `ORIGIN=ACTIVE`,
  P1 prepare/validate via fixture code with no-write asserts. If R1
  unconstructible, test would fail with exact gap (no fake pointer/reason).
- `_snapshot` now records regular hashes + symlink/dir/FIFO inventory (never
  opens FIFO) + HEAD/status; EVERY negative/scope/drift takes snapshot AFTER
  fault mutation (injected delta recorded), immediately before the P1 call,
  before cleanup (alias/traversal/ancestor/FIFO/shadow/noncanonical/ineligible/
  retention/scope/binding/drift/candidate). Full frozen/retention expected-SET
  oracles (not counts): frozen must include profile/arch/approval/synthesis/
  draft-package/result/evidence/matrix/ledger/discovery/cards/drafting-archive
  and exclude publication-authored/State/QA/tool/outputs; retention ONE row per
  node, sorted unique roles, `retained_ref` exact vs `retained_dest` under
  `retained/before/`, XOR. `REQUIRES_OWNER_DECISION` + wrong-AFTER added;
  artifact-only commit allowed vs control-drift (`closure` dirty) refused
  (`RECEIPT_INVALID` wrapping); candidate proper (real `build_candidate` exact
  6-field agreement, COPY) vs stale (`CANDIDATE_INVALID`) + absent allowed;
  forged-header/wrong-PATH/wrong-digest/missing-nullable/wrong-dir/
  extra-omitted-conflicting retention + `HASH/POLICY` + union-roles unit;
  ordinary-review compat preserved (no semantic acceptance).

## Test evidence (no old transfer)

Strict runner `run_correction.py` (deps → 3M10A freeze → sanitized no-network
Git + `optimize==0` refuse → unittest → finally-post freeze, exclusive logs,
timeout partial): **36/36 OK (9 new P1 + 27 gate) in 2736.162s**,
`run.exit=exit=0`, pre/post HEAD/tree/status/files identical. Runtime
Python 3.14.4, jsonschema 4.23.0, pypdf 6.16.2, git 2.53.0, no installs/network.
Old 32 historical superseded (no PASS transfer); only focused + affected gate
control. Three failed attempts preserved (`attempt-1-failed-unboundlocal/`,
`attempt-2-failed-snapshot/`, `attempt-3-failed-1plus1/` with analyses).

## Patch + independent apply proof (AS SAVED)

- `complete-p1-correction-13path.patch` 550730B, SHA256
  `147014b4307b8dd56860491c51c06502962692c100804086aa7277210e3f52d7`,
  13 `diff --git` via `git add -N` + `git diff HEAD` (proper new-file headers),
  base HEAD409/tree8ce. `gen_correction_patch.py` saved (transient `add -N`
  reset, no commit).
- `proof_apply.py` byte-copied active DB to
  `/tmp/opencode/jgas-dm021p1-correction-verify-20261011T235631Z/` (inert origin,
  no alternates, verified 3M10A + all13 bytes), reverted ONLY 13 overlays in
  the COPY to clean409 (`checkout HEAD -- 3M` + `rm 10A`, verified clean status
  + HEAD409/tree8ce), `git apply --check` + `git apply` AS SAVED (exit 0),
  verified all13 hashes/modes/status equal freeze-pre
  (`proof-freeze-applied.json`). Active source/archive inputs untouched. No
  candidate commits/branches, network, or protected-DB writes.

STOP for Astra code/oracle review + same author-independent re-review. No extra
Source/State/reason/approval runtime; DM021 still OPEN, whole NOT_READY,
step4/B3 OPEN, canonical audit unstarted. Ordinary reconstruct Commit/Push
remains Human-owned.
