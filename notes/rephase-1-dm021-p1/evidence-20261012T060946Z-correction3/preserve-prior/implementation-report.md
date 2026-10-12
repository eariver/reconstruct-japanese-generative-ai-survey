# DM021-P1 R2 correction implementation report (worker → Astra + same independent review)

Source: `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
(detached HEAD409b292/tree8ce, no branch/commit/network/Production). Final overlay
13 paths (3M10A), same 3A1M budget; LF2I 9 pins preserved, pre-TeX schema P1 M
unchanged (`e8598239`). Prior 36-test packet + qualified PASS preserved untouched
in `preserve-prior/` (4 files `9f3aea25/5623c0d9/e8598239/a7b04dc1`, 36 raw,
old report/patch `147014b4`); R2 edits only module+test (schema unchanged).

## Final pins (freeze-pre==post)

HEAD `409b292`, tree `8ce36998`, status 3M10A. M gate-schema `fe4a96f4` 6894B,
M semantic-review `e8598239` 4219B, M gate-script `e7305884` 94511B; A proposal
schema `5623c0d9` 3945B, A LF-manifest `4dadf873` 2720B, A LF-input `7bae9d2a`
10624B, A proposal module `8bf87871` 97334B, A LF-derivation `c09c5558` 62260B,
A LF-generated `d480e11d` 39992B, A LF-publisher `4d235a38` 36224B, A P1 test
`00ba3ef1` 101176B, A LF-derivation-test `ce687447` 91161B, A LF-integration
`4a03b564` 107757B (all 0o664). No other runtime touched.

## C1 — finite typed transitives (not receipt-prefix iteration)

`_build_graph` now walks State/checkpoint + accepted-record schemas with explicit
known fields/implicit siblings, source-SHA verification, role union; no generic
string recursion, no URLs, no fake State; history SHAs stay provenance.

- Checkpoint wrappers: every `state.checkpoint_provenance` `{path,sha256}` (nulls
  skipped) pinned, `checkpoint-wrapper:<name>` KEEP operational (never frozen),
  `STATE_CHECKPOINT <name>` edges. Shared-file wrappers union (same SHA/policy).
- Evidence: for each `evidence-acceptance` row, sibling `package.json` verified
  against `package_sha256`, `upstream:evidence-package` KEEP frozen; basis
  `screening_acceptance_path/sha` → `upstream:screening-acceptance`,
  `discovery_path/sha` → `upstream:discovery-raw`; `package.tasks[]`
  (`tasks/*.json` under run_dir) → `upstream:evidence-task:<id>`.
- Screening: for each pinned screening acceptance, sibling `package.json`
  verified, `upstream:screening-package`; `package.input.batches[]`
  (`input/batches/*.jsonl`) → `upstream:screening-batch:<id>`; acceptance
  `batches[]` (`results/<batch_id>.json` known pattern, verified `result_sha256`)
  → `upstream:screening-result:<id>`.
- Completeness: known implicits `source_root/profile-completeness.json` (+`-v2`
  variant) if regular non-symlink; basis `production_profile_sha256`/
  `materiality_ledger_sha256` verified against pinned Profile/Ledger live SHAs;
  `upstream:profile-completeness` KEEP frozen. Missing both → `COMPLETENESS_MISSING`
  (fail-closed, not omit). Views files absent in Weekly/Longform minimal fixtures
  and unreferenced by path (only SHAs in ledger basis); validators pass without
  files, so no fake nodes (not omitted necessary relation; would STOP if a required
  path relation proved necessary without authority).
- `_frozen_member_kinds` already maps any `upstream:*` → frozen kind; wrappers/
  State/QA/tool/pub/candidate stay operational (excluded). Historical State SHA /
  old superseded SHAs never become live nodes.

Oracle `_assert_transitives_expected_set` (independent, not receipt list): enumerates
REAL fixture filesystem via known parent dirs (`orchestration/.../checkpoints/*.json`,
`evidence/.../runs/*/package.json`+`tasks/*.json`, `screening/.../runs/*/...`,
`discovery/discovery.jsonl`, `profile-completeness.json`) + State wrappers; asserts
each in graph/retention with KEEP + frozen inclusion (research) vs exclusion
(wrappers/State/QA/receipt/candidate). Called in Longform + Weekly positives
(filesystem, no receipt-list derivation).

## C2 — bundle profile exact (no-op pass removed)

`_check_bundle_profile_exact` requires bundle `production_profile` == State
`profile` (path+SHA) and manuscript `production_profile` == State (coherent),
plus pinned live bytes == State SHA; mismatch → `BUNDLE_PROFILE_DIVERGED`/
`MANUSCRIPT_PROFILE_DIVERGED` (not `pass`). File-tamper necessarily triggers
checkpoint drift (`STATE_INVALID`) first (bundle file is a checkpoint row; any
byte change alters its SHA) — both fail-closed; exact logic unit-proved via
same-SHA different-path (valid alt, no file tamper, no drift) → `BUNDLE_PROFILE_DIVERGED`
by PATH (not broad hash). Alt-path file-tamper subTest accepts
`STATE_INVALID|BUNDLE_PROFILE_DIVERGED` (injected delta recorded, no P1 write).

## C3 — full predicate after scope/schema in BOTH APIs

`_final_full_receipt_recheck` re-runs ACTUAL route `validate_receipt`
(ancestry/dirty/untracked/closure/contract/replay, no pending bypass) from pinned
basis refs, then `reverify`. `prepare_proposal` calls it AFTER schema validation
+ final tree (validated roots); `validate_proposal` calls it AFTER scope + final
tree (replacing contract-only equality). `contract_identity` alone never suffices
(unlisted helper outside closure leaves HEAD/config/closure unchanged but dirties
`scripts/` control). Seams (real calls, no reason bypass): late-prepare helper
`scripts/survey_production_v2.py` (outside Weekly 8/Longform 14 closures, tracked
control) dirty → `RECEIPT_RECHECK_FAILED`; late-scope same helper drifted after
scope creation → validate with scope refuses via final recheck. Artifact-only
commit (non-control `sources/.../artifact-only-note.txt`) still passes (receipt
ancestry/control clean). Each seam snapshots AFTER mutation, proves no P1 write.

## C4 — validated roots before walk, normalized root, dead code

`_validated_state_profile_for_tree` loads State/Profile ONLY via safe-pinned bytes,
enforces strict `validate_agent_state`, eligibility, Profile SHA/issue, canonical
State, repo-local roots — BEFORE any `_tree_map`. Public entries normalize
`Path(root).resolve()` once, derive `tree_entry` from VALIDATED roots (never preview),
then `_pipeline` (re-validates). Invalid/unbound Profile (`source_root="/"`)
spy test patches `_tree_map` (wraps, never mocks success), asserts `call_count==0`
and refusal. Removed dead `for ...: pass` in retention + duplicate
`REVIEW_DIGEST_UNBOUND` while touching those sections only.

## Tests (fresh, no old36 transfer)

Strict `run_correction.py`: **36/36 OK (9 P1 incl. C1 oracles/R1×2 + 27 gate) in
3030.572s, `exit=0`, pre/post identical**. Python 3.14.4/jsonschema 4.23.0/pypdf
6.16.2/git 2.53.0, `optimize==0`, sanitized no-network Git, exclusive logs.
Gate controls affected by shared-schema M all pass; ordinary semantic-record
compat (`test_ordinary`) + real R1 two-refresh chain preserved. One R2 attempt
failed (C2 expects specific code, got STATE_INVALID drift-first) preserved in
`attempt-1-failed-c2/` with analysis; active fixed (accept drift-first +
exact-unit).

## Patch/proof (no active index mutation — prior add-N disclosed)

Prior generator's transient `git add -N` + `reset` in ACTIVE index disclosed as
avoidable mutation (worktree untouched, no commit, but index touched). R2
`gen_correction_patch.py` byte-copies ACTIVE to `/tmp/.../R2-gen-...`, does
`add -N`+`diff HEAD` THERE (disposable index), copies patch out, deletes copy —
ACTIVE index never touched (`git diff --cached --name-only` empty, verified).
Patch `complete-p1-correction-13path.patch` 579733B SHA256
`2046d3ba243a81113e01e568ed6affdde3113a9acd6f2ec96719713373e1c3c5`, 13 `diff --git`,
base HEAD409/tree8ce. `proof_apply.py` byte-copies ACTIVE to
`/tmp/.../R2-verify-...` (inert origin, no alternates, inode separation checked),
reverts ONLY 13 overlays in COPY to clean409 (`checkout HEAD -- 3M` + `rm 10A`,
verified clean HEAD409/tree8ce), `apply --check`+`apply` AS SAVED (`exit=0`),
verified all13 hashes/modes/status/base equal freeze-pre. Active/protected copies
unedited, no commits/branches/network/subagents.

STOP for root + same independent re-review (graph-complete/profile-no-op/
control-recheck PASS against actual code + expected-set oracles). Whole NOT_READY,
DM021 OPEN. Commit/Push Human-owned. If any transitive relation proves missing
without authority, this report claims no false completeness — return blocker, not
PASS (none found; views absent-but-unrequired as above).
