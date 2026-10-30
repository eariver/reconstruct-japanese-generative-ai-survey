# Owner-B preserved-provenance correction — R1 PREARCH research trio (Attempt6 Blocker 1)

2026-10-28. Fixes Attempt6 Blocker 1 (`whole-lifecycle-witness-progress.md`
§Attempt6.1; raw `evidence/full-lifecycle-v2-20261028T213412Z/dm022-p1-probe-20261028T213310Z.txt`
SHA `4c9c3ec5…`, probe `dm022-p1-probe.py` SHA `67efd4e6…`):
`agent.revalidate_publication_surface` REVIEWED_CORE_CHANGE on adopted
VALIDATED_DRAFT with PREARCH upstream failed in `_verify_preserved_provenance`
(`survey_agent_control_v2.py:2517`) with `revalidation basis checkpoint
completeness … '$' : 'from_state' is a required property` — the legacy
StageCheckpoint schema was applied to the new PREARCH record. This is a
legitimate pre-versioned R1 affected consumer (canonical R1 before any
versioned set; NOT a required prereq for editorial P1, whose long-worker probe
label conflated the two). No ordinary commits, no Human readback, no network,
no Gitconfig, no cleanup. Unit ongoing — root must review; no milestone claimed.

## 1. Exact B-owned source change (no foreign source patched)

File: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work/scripts/survey_agent_control_v2.py`,
function `def _verify_preserved_provenance` (`:2489`; PREARCH branch `:2519-2572`,
legacy path unchanged below).

Per R6 expected roles (research trio ADMIT with same 3 roles + 4-name set +
SELF/proof + lineage + G76 window; validation/freeze/release + selection +
all other checkpoints REFUSE PREARCH) and existing precode (all preserved
provenance readers through later mechanical required; no new contract):

- For each `checkpoint_provenance` entry: reload bytes + SHA drift check
  (unchanged), then classify by real record via required
  `low.load_typed_checkpoint_record(repo_root, path)` (generic parse, no role
  decision, no caller-dict trust). No triplet-shape heuristic anywhere on this
  path; malformed records raise fail-closed (never fall back to the other branch).
- If family `PREARCH`: admit ONLY when `name in {evidence, materiality,
  completeness}` (R6 site 2); otherwise raise
  `DM022_WRONG_FAMILY for <name>` (covers validation/freeze/release/selection
  and any other expected-legacy role). Then: strict content branch
  (`_validate_prearchitecture_record_content`: kind/reason/operation
  `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`/producer_boundary
  `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`/3 checkpoints/4 NamedRefs/SizedRef
  review result + SIZED vs ArtifactRef bindings below); same-record original
  refs (all three State refs same path+sha, else triplet mismatch); lineage
  presence (`parent_checkpoint`/`original_anchor`/`supersedes`); full path
  proof via required A3 `low.check_supersession_record_from_paths(repo_root,
  checkpoint_path, report_path, before_copy_path)` with paths derived from the
  pinned record (`report.path`, `revision_root + /retention/state-before.json`,
  no caller proof dict); live re-hash of all 4 NamedRefs + SizedRef review
  result (`path/sha/byte_count` exact keys, `byte_count int >= 1`, file re-read
  SHA equality + `st_size == byte_count`). Own-epoch lineage is enforced inside
  the A3 checker (contract/implementation vs stored manifest pins, never
  current source). No `agent.validate_agent_state` call (no recursion into
  State validation); no `require_research_operation_ready` (LOW detached proof
  has no operational READY); no State triplet switch (R1 never adopts research).
- Else (LEGACY family, including legacy research trio with legacy kind and all
  validation/freeze/release/discovery/screening/selection/architecture/draft
  checkpoints): byte-identical legacy path (old `CHECKPOINT_SCHEMA` load +
  issue check + artifact/review live re-hash with `sup` superseded allowance
  on the bound validation record only). Source graph strict Evidence checks
  unchanged; validation-projection untouched; `sup` semantics unchanged.
- Publication R1 after versioned still prewrite-refuses via the unchanged
  `assert_canonical_publication_mode` gate at `revalidate_publication_surface`
  entry (no change here); no research adoption via R1 (this function never
  writes State triplet, only validates preserved bytes + creates the new
  revalidation record downstream).

SizedRef vs ArtifactRef bindings enforced per selected schema (no inferred
field names): `before_state/request/retention_plan/proof/decision/report` +
`reviews[].result` are SizedRef `{path,sha256,byte_count}`;
`before_checkpoint.{evidence,materiality,completeness}` +
`parent_checkpoint`/`original_anchor`/`profile` are ArtifactRef `{path,sha256}`;
`artifacts[4]` are NamedRef `{name,path,sha256}`;
`supersedes[]` are `{path,sha256,revision_id}`. Legacy
`CORE_STAGE_CONTRACT`/`release` review results stay 2-key (untouched).

## 2. Exact B-owned tests (no authority mock; existing obligations unchanged)

File: `candidate-work/tests/test_dm022_prearch_b_ordinary_consumers_v2.py`
(SHA `b56ad21e7d6e90afcbf7e35c3df709e1360f399fa667d0d7db18c1748ee98868`; 23 tests).

- Retained: `test_01-19` (strict `reason`, exact operation/boundary, SizedRef
  proof, wrong-family, triplet, 7-slot + audit, guard split, legacy
  discriminators, drafting R4, full PREARCH validate + resolve4 + later
  forward, guard no-recursion, LEGACY same-triplet routing, PREARCH R refs,
  stale-StateSHA vs content facade, stale-refuse-no-write). Existing
  `test_23` pins `PUBLICATION_ROLES_7` (7 roles) + 7-slot audit (before/after
  obligations unchanged by construction).
- New for this blocker:
  - `test_20_r1_healthy_prearch_before_versioned`: real public R1 on WEEKLY
    VALIDATED_DRAFT with PREARCH (built via General real chain: DM022 adopt +
    regen + advance + Architecture approval + accepted-facade Drafting + REAL
    PDF publication, canonical mode, no versioned set). Re-runs deterministic
    QA with a new legitimate executor label (byte-distinct bundle, same
    source/pdf binding, explicit nongenuine re-QA) then calls public
    `agent.revalidate_publication_surface` REVIEWED_CORE_CHANGE. Must create
    the r1 record with PREARCH upstream preserved (no `from_state` error, no
    fallback, writes only the new record + rebuilt QA bundle).
  - `test_21_r1_wrong_role_prearch_as_validation_refuses`: real HIGH-adopted
    PREARCH record file (not a mocked dict). `_validate_checkpoint_record`
    returns (not raises) `DM022_WRONG_FAMILY` for checkpoint=validation with
    PREARCH authority; `_verify_preserved_provenance` raises WRONG_FAMILY when
    the validation provenance itself is a PREARCH node. No writes. Proves
    classification by real record and that R1 never adopts research.
  - `test_22_r1_split_and_stale_refuse_no_writes`: split State triplet (one
    ref retargeted to a different real checkpoint with real path+sha) refuses
    triplet mismatch; drifted R artifact bytes refuse SHA drift; file set
    identical before/after (no writes). Real files only, no authority-mock dicts.
- Not mocked: every authority is a real file path+live SHA (HIGH-adopted
  records, A2 chain files, General VALIDATED_DRAFT fixture); refusals come
  from real code paths (loader/schema/checker/live re-hash), never
  self-raised strings. `test_10` oracle asserts the required wrong-review
  property + no new files (not a brittle string).

## 3. Pins, private copy, raw (no shared-candidate execution)

- Private copy (B-safe only; other workers' file edits untouched):
  `/tmp/dm022-b-lifecycle-private-20261028T180000Z` — `tar
  --exclude=.git --exclude=__pycache__` from current candidate-work after own
  edit + `.git` byte-copied from `snapshot-a4-20261028T160708Z/git-independent/.git`
  (83 files, HEAD `409b292…`, inert example.invalid, no alternates) for legacy
  tests needing `repository_commit_sha`; 758 worktree files, 0 `__pycache__`.
- Changed-file SHAs (candidate-work): `survey_agent_control_v2.py`
  `b6506a8b…` (this fix + prior R1/SizedRef/lifecycle fixes);
  `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` `c634fa32…`.
  A3 LOW/HIGH/evidence unchanged by B (A-owned); C1/C2 untouched by B.
- Raw unique: `/tmp/dm022-b-preserved-r1-raw-20261028T183000Z.txt` (63 lines,
  SHA256 `7b939bde…`, exit 0): `Ran 23 tests in 74.083s OK` (B 23/23).
  Legacy controls in the same copy: `tests.test_survey_agent_control_v2` (5),
  `test_survey_active_evidence_views_v2` (2),
  `test_run_selection_architecture_v2_interactive` (2) → 9/9 OK
  (raw `/tmp/dm022-b-legacy-raw-20261028T180000Z.txt`, SHA `cb861b44…`, exit 0).
  No ordinary commit/push, no Human readback, no network, no Gitconfig mutation,
  no cleanup/reset of shared trees.

## 4. Caller impact + what remains (honest, no milestone)

- C1/C2 caller changes required by this fix: none. C1 already calls content
  helpers with session expectations/roots (no State SHA); C2 release gate was
  narrowed in Attempt5 (research trio admitted, wrong-role publication
  pointers still refuse). The remaining C2 diagnostic-vs-writer split
  (`validate_reader_surface_gate` READY inside diagnostic) is unchanged and
  still returned separately; it does not block R1 (guard absent + completion
  present in the R1 fixture, so READY passes; diagnostic still works).
- Editorial P1 (`prepare_proposal` on the revalidated state) is NOT executed
  here; per instruction the actual editorial test witness proceeds P1 direct
  separately on top of a healthy R1. This return stops at healthy R1 + wrong
  role/split/stale refusals; whole NOT_READY/step4B3 OPEN/audit unstarted/
  DM021+022 OPEN preserved except pre-code gate. Root must review before any
  test-snapshot claim.

Author: Owner B. Scope is `_verify_preserved_provenance` PREARCH branch + B R1
tests above only; legacy paths, Evidence validators, R1 prewrite refusal, and
State triplet discipline unchanged.
