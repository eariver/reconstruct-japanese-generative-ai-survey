# DM021-P1 final resolution — independent source-grounded review (R2+R3)

2026-10-12. Same author-independent reviewer (Phase-B narrow + correction
qualified-PASS author). This is a NEW source-grounded final resolution for
root R2 (`astra-review-r2.md`) + R3 (`astra-review-r3.md`); it does NOT reuse
the previous qualified PASS. Read R2/R3, latest packet
`notes/rephase-1-dm021-p1/evidence-20261012T060946Z-correction3/`
(report/freezes/run/proof/patch), and actual corrected source at
`/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
read-only (no rerun/code edits/network/commits/subagents; no OWN-copy probe —
no concrete ambiguity required one; all findings source/log-cited).

## 0. Explicit correction of the prior overclaim

`evidence-20261011T235631Z-correction/independent-correction-resolution.md`
(SHA `86ddf38d...`) gave a qualified BOUNDED_PASS for module `9f3aea25`.
Root R2 then found that verdict's "R1-complete" language was an overclaim:
the graph stopped at receipt roots (no Evidence/screening/views/completeness/
selection transitives), bundle-profile was a `pass` no-op, final predicate was
contract-only, and tree walked unvalidated preview roots. R3 further found the
correction2 collector added wrappers without artifact refs, lacked
`candidate-selection`/`edition-views-acceptance` bodies, and used a guessed
`profile-completeness.json` presence fallback. That prior PASS is WITHDRAWN to
the extent it claimed C1 completeness; this resolution re-verifies every item
below against actual latest source. No blanket PASS is given.

## 1. FULL pins (actually observed)

- Base: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status exactly 3M10A
  (freeze-pre == freeze-post, `diff` empty; `git diff --cached --name-only`
  empty — no index intent this round).
- M `reader-surface-gate-v2.schema.json` `fe4a96f4` 6894B;
  M `reader-surface-semantic-review-v2.schema.json` `e8598239` 4219B
  (pre-TeX, UNCHANGED across R1–R3); M `survey_reader_surface_gate_v2.py`
  `e7305884` 94511B — all `0o664`, LF2I-preserved.
- A `editorial-correction-proposal-v2.schema.json` `5623c0d9` 3945B
  (UNCHANGED from R1 correction; required nullable pointer + persisted reader
  ref + XOR retention + no singular role retained).
- A `survey_editorial_correction_proposal_v2.py` `69790944` 104046B/1737 lines
  (R3 module); A `test_survey_editorial_correction_proposal_v2.py`
  `84a6e4a11` 106226B/1746 lines/9 P1 methods; other 7 LF2I paths stable
  (`4dadf873/7bae9d2a/c09c5558/d480e11d/4d235a38/ce687447/4a03b564`).
- Patch `complete-p1-correction-13path.patch` 591663B SHA256
  `611cfd75f12f960b606e697b50ea4a50782a214ce06e86a2687b2c9fa7f01fc6`,
  13 `diff --git`, base HEAD409/tree8ce. `run.exit=exit=0`,
  `proof-apply.exit=exit=0` (empty check out/err). `deps.txt`: Python 3.14.4
  `optimize==0`, jsonschema 4.23.0, pypdf 6.16.2, git 2.53.0.
- Run: `Ran 36 tests in 3255.889s OK` (9 P1 + 27 Gate affected control only;
  old 36 no transfer). Proof: byte-copy → revert 13 in COPY to clean409
  (`status=""`, HEAD409/tree8ce, `proof-freeze-clean.json`) → `apply --check`
  + `apply` AS SAVED → applied files/modes/status == freeze-pre
  (`proof-freeze-applied.json`; independently re-verified equal here).
- `preserve-prior/` retains R2 packet (module `8bf87871`, test `00ba3ef1`,
  report, 36 raw). Prior ACTIVE `add -N` deviation (R1/R2 generators)
  preserved/disclosed; R3 `gen_correction_patch.py` is copy-based
  (`R3-gen` temp, `add -N` THERE, patch copied out, temp deleted; ACTIVE
  `diff --cached` verified empty in-script and re-observed empty here).

## 2. C1 — State-bound transitives: FIXED (source-verified)

- `_build_graph` takes `cfg` and resolves EXACT named artifacts via real
  `agent.resolve_checkpoint_artifact(root,cfg,state,checkpoint,name)` with
  per-checkpoint record cache (first row full API validation, rest reuse pinned
  record, `1005-1039`): `discovery/discovery-acceptance`,
  `screening/screening-acceptance`, `evidence/evidence-acceptance` +
  `evidence/edition-views-acceptance` (pair additionally bound by
  `resolve_active_evidence_views` same-checkpoint check `1058-1061`, no
  cross-run join), `materiality/materiality-ledger`,
  `completeness/profile-completeness`, `selection/candidate-matrix` +
  `selection/candidate-selection`, `architecture` all 3
  (issue-architecture/summary/attention), `draft` synthesis-input/result +
  DYNAMIC `draft-package:*`/`draft-result:*` from the pinned draft record
  (`1077-1092`, no pid guessing). Each: `checkpoint-artifact:<cp>:<name>`
  provenance + `upstream:<kind>` frozen (union, same KEEP),
  `CHECKPOINT_ARTIFACT` edge from its wrapper (`1041-1051`).
- Wrappers: EVERY `state.checkpoint_provenance` `{path,sha256}` pinned,
  `checkpoint-wrapper:<name>` KEEP operational, `STATE_CHECKPOINT` edges
  (`864-872`); history/old-SHA stay provenance (no live nodes).
- Views: `views[]` + validator `survey_evidence_v2.view_filename` convention
  (`views/<file>` siblings, `view_sha256` pinned, `1093-1122`):
  `upstream:edition-view:<id>`. Evidence `package.json`+`tasks/*.json`
  (`878-933`), screening `package.json`+`input/batches/*.jsonl`+
  `results/<bid>.json` (`934-992`), discovery raw via explicit basis
  paths+SHAs — all from checkpoint-bound acceptances with source-SHA
  verification and role union; URLs/historical SHAs provenance-only.
- Guessed fallback REMOVED: `grep profile-completeness.json in module → exit 1`
  (no presence/glob lookup); completeness ONLY via `completeness` checkpoint
  ref (`1066`). No `candidate-selection`/`edition-views-acceptance` omission
  (both collected `1064,1069`).
- Honest history: nodes remain effective bytes; edges relabelled `EFFECTIVE
  <name>` (`627-629`, no `CHECKPOINT_ROW` literal); original path/sha kept in
  `original_rows` return, not live nodes. `grep EFFECTIVE` confirms; no
  `CHECKPOINT_ROW` edge remains.
- Frozen: ANY `upstream:*` → frozen kind (incl. selection/views/completeness/
  evidence-tasks/batches/results); wrappers/state/QA/tool/pub/candidate
  excluded by construction. Missing/unclassifiable → explicit
  `CHECKPOINT_*/VIEWS_*/EVIDENCE_*/SCREENING_*` blocker (none hit; fixtures
  include views acceptance+files via checkpoint).
- Oracle (independent, not receipt list): `_assert_transitives_expected_set`
  (`test:652-788`) resolves the SAME exact map via `agent.
  resolve_checkpoint_artifact` IN TEST + container maps via explicit acceptance
  fields (`package.tasks`, `input.batches`, `batches/result_sha256`,
  `views[]`+`view_filename`, draft-record artifacts — independently loaded).
  Asserts EACH in graph/retention KEEP + frozen (research) vs wrappers KEEP
  not frozen; pub/QA/State/receipt/candidate excluded from frozen; NO count
  surrogate. Stale `source_root/stale-profile-completeness.json` (same
  bytes/basis as real, valid-looking, NOT checkpoint-bound, created BEFORE
  prepare) asserted NOT in graph/frozen in BOTH Longform (`810-813`) and Weekly
  (`907-910`) positives — proves no presence/glob inference. Selection/views
  retention+frozen explicitly proved. PASS. Report §R3-C1 accurate.

## 3. C2 — bundle profile: FIXED

- `_check_bundle_profile_exact:491-514` requires bundle profile path+SHA ==
  State-bound profile path+SHA AND manuscript profile == State profile +
  live-bytes check; called in graph build (`773`) before node/edge creation.
  Prior `pass` no-op gone (verified). Tests: same-SHA alternate-path unit
  proves `BUNDLE_PROFILE_DIVERGED` via path mismatch (not broad hash), plus
  file-tamper checkpoint-drift (`STATE_INVALID` first) and manuscript-profile
  divergence cases (`test:1503-1525`). Other source/PDF/Candidate cross-bindings
  preserved. PASS. Report §C2 accurate.

## 4. C3 — full final predicate: FIXED (both APIs)

- `_final_full_receipt_recheck:1479-1505` re-runs the ACTUAL route full
  `validate_receipt` (ancestry/dirty/untracked/closure/contract/replay, no
  bypass) from pinned basis refs + `reverify()`. Called AFTER schema in
  `prepare` (`1531`) + validated-tree recheck (`1533-1538`), and AFTER scope in
  `validate` (`1721`) + `reverify()` + validated-tree recheck (`1723-1728`).
  Not contract-only (prior `1391-1399` comment-only superseded; contract
  equality remains as an additional check, not the predicate). Late-prepare and
  late-scope seams mutate tracked helper `scripts/survey_production_v2.py`
  (outside `CURRENT_CLOSURE`, HEAD/config/closure-bytes unchanged) and MUST
  refuse (`RECEIPT_RECHECK_FAILED` family); artifact-only commit still passes
  (`test_artifact_only_vs_control_drift_and_tree`). PASS. Report §C3 accurate.

## 5. C4 — validated authority before tree walk: FIXED

- `_validated_state_profile_for_tree:1443-1476` (State/Profile via safe-pinned
  bytes, strict validation, eligibility, canonical-State, repo-local roots)
  is called BEFORE ANY `_tree_map` in BOTH `prepare_proposal:1523-1525` and
  `validate_proposal:1635-1638,1677-1678`; `Path(root).resolve()` normalized
  once per entry. Invalid `source_root="/"` spy test proves `_tree_map`
  call_count == 0 (`c4-unvalidated-tree-spy`, mock wraps but never mocks
  authority success). Dead retention no-op loop + duplicate digest check
  removed (verified absent vs prior lines). PASS. Report §C4 accurate.

## 6. Scope/binding/R1/no-extra-authority: RETAINED, PASS

- Headers/path/digest/schema compared ALL; supplied returned UNCHANGED +
  separate `measured` (tests assert `outcome["proposal"] == proposal` for
  noscope/bound); scope framework (capture-before-loader, digest bind,
  before/after/upstream + substantive check) unchanged and correct, incl.
  NeedsOwner/wrong-AFTER/header/digest/layout/retention-completeness/conflict/
  stale-Candidate oracles. Real R1 owner ×2 refreshes (non-emitted,
  same-reader/output, `supersedes` depth) + generic Core-change predecessor
  (relabeled, not conflated) + artifact-only allowed vs control-drift refused +
  root field binding + unread-alias (FIFO/ancestor/shadow without opening) +
  pending refusals all present in 36-method run. No new controller/receipt/
  writer/reason/approval paths; 3A1M budget kept. PASS.

## 7. Evidence completeness: PASS with stated limits

- 36/36 actual methods with per-call before snapshots (after fault mutation,
  before cleanup) + guards/raw preserved; runner pins all13 hashes/modes/
  status/base + sanitized Git + `optimize==0` + exclusive logs + timeouts;
  patch copy-generated (no active index writes) and applied AS SAVED to an
  independent actual409 base with mode/isolation checks. Previous `add -N`
  deviation preserved as history, not repeated. No old36 transfer. PASS.

## 8. Verdict: BOUNDED_PASS (final, source-grounded, not blanket)

R2 C1–C4 and R3 narrow items are implemented in actual code at pins §1 and
exercised by independent checkpoint/container-SET oracles (incl. stale-sibling
non-adoption), exact profile binding, full-receipt late rechecks, and
authority-first tree discipline. Prior qualified-PASS overclaim for C1
explicitly corrected (§0). Limitations: P1 remains read-only preparatory
validation (`REVIEW_REQUIRED/REVIEW_BOUND_PROPOSAL` only); whole NOT_READY,
DM021 OPEN; no genuine publication/proposal adoption, no full-historical
retention proof, no production maintenance. Stop at Human Commit Point;
Commit/Push Human-owned.
