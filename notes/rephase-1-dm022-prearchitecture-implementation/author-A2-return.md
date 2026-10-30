# Owner-A2 implementation return — DM022 pre-Architecture research operation (CORRECTION)

2026-10-28. Owner A2 (correction implementer replacing rejected ownerA R1).
Human continuation authorized ACTUAL CODE in independent candidate ONLY;
docs-only explicitly NOT the task. Binding order: contract a345bb95 INCLUDING
S11, pre-code assessment S5, precode packet README, mandatory
astra-precode-gate-resolution INCLUDING S5 (FULL 0425c530/13788B), independent
readiness SS8-9 FINAL-BINDING, then R3 (overridden by) R4 + literal 5 schemas,
R5 families, R6 roles, then ROOT. No ordinary candidate/reconstruct Commit/Push;
no fixtures in reconstruct; no git config/global writes; no
network/Production/reset/clean/old-log overwrites. Python 3.14.4 +
unittest/jsonschema 4.23.0/pypdf 6.16.2; TinyTeX path per coordination
(availability only, no build executed here).

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all paths below relative to it). Started from prepared full742+inodes
source actual409/tree8ce + inherited93; no ordinary source commit.
Rejected R1 snapshot preserved immutable at
`snapshot-r1-20261028T121631Z/worktree` (756 files, manifest
f67ad9b6/149981B) + `evidence/source-r1-20261028T121631Z/`; old
`author-A-return.md` preserved (this file is `author-A2-return.md`, not a
replacement). No deletion of old packet/snapshot.

## 1. Exact written paths (Owner A ONLY, disjoint from B/C1/C2)

CHANGED (A2 correction, this unit; schemas unchanged except preserved R1 fix):

- `scripts/survey_research_authority_v2.py` (LOW, detached, PATHS-only) — 109192B
- `scripts/survey_prearchitecture_acceptance_v2.py` (HIGH, sole mutator) — 76295B
- `tests/dm022_prearchitecture_fixtures_v2.py` (Owner-A test-only helper; NEVER
  runtime authority, never enters source closures) — 3330B
- `tests/test_dm022_prearchitecture_acceptance_v2.py` (Owner-A unittest, no
  pytest) — 36770B

OWNED BUT UNCHANGED (verified, not edited this unit):

- `schemas/dm022-*.schema.json` (5 installed): request a99f0dc1/18648B,
  manifest e7534d01/8773B, proof a79c0920/7403B, checkpoint fd39c246/7259B all
  match R4 proposal SHAs; report 10238a1a/14629B differs from R4 proposal
  21369608 ONLY by the preserved intentional B2 registry fix (first two
  `roleSchemaRegistry` entries retarget `notes/.../schema-proposals-r4/...` →
  `schemas/...`; closed/local registry, no dangling proposal path). Old
  `author-A-return.md` §2 documents this; A2 preserves it.
- `scripts/survey_evidence_v2.py`, `survey_screening_v2.py`,
  `survey_completeness_v2.py` — existing A-owned S1.1 leaf cores; A2 made NO
  edits (all real validation is via function-local calls to their exact
  `_content` cores with correct signatures, never via wrapper mutation or
  global monkeypatch). If root's integration snapshot finds a wrapper predicate
  gap, A2 will patch narrowly on request.

NOT touched (other owners, concurrent edits respected):

- B: agent/selection/architecture/drafting/handlers/stage/bridge/orchestrator/
  human-gate, four-ref/7-slot writers, B tests.
- C1: versioned-renewal/derivation/staged-source + `config/survey-production-v2.json`,
  C1 fixture helpers/tests.
- C2: publication/editorial/retention/current-authority/reader/execution/
  release, C2 fixture helpers/tests. Shared C1/C2 fixture helpers untouched.

## 2. What A2 corrected vs rejected R1 (root astra-r1-source-review §A1–A7)

- SAFE IO: LOW `_safe_read_bytes` + HIGH `_safe_read_bytes` now compare opened-FD
  `fstat` identity with pre-open `lstat` (`dev/ino` must match; symlink/
  nonregular/unreadable refuse, `O_NOFOLLOW`, checked close, no TOCTOU grant).
  HIGH `_exclusive_write_bytes` now refuses if the final target already exists
  (no `os.replace` overwrite of immutable revision/guard/checkpoint/completion
  artifacts); only the State triplet switch uses a separate inode-pinned
  replace-over-existing path (`_replace_state_known_byte` logic inside
  `replace_state_triplet`: LIVE must still be `B` with SAME `dev/ino`, temp is a
  new inode, `os.replace` + dir fsync + immediate postread). `_copy_regular_exclusive`
  re-reads source, verifies `dev/ino` differ, refuses inode sharing. Checked
  slot clearing (`clear_remaining_exact_slots`) captures `source_dev/source_ino`
  equality, refuses `present-with-unexpected-ino` even on equal bytes, and
  refuses `present-while-retention-planned-absent` (no unowned unlink of a newly
  planted file where the retained slot was absent).
- REAL acceptance graph (no fabricated digests, no automatic SATISFIED/COMPLETE,
  no default MATERIAL, no task placeholder, no ignored exceptions, no hash-only
  acceptance):
  - Package tasks derive from REAL Discovery (`read_jsonl`) + REAL Screening
    decisions + `stable_task_id`/`task_filename` + REAL `source_records`/
    `verification_targets`/`screening_basis`; prompt/contracts are copied from
    the REAL OLD package (no `"0"*64` placeholders); tasks validated via real
    `_validate_task`; package validated via real
    `_check_evidence_package_fields_content` (no `revision_id` in package).
  - Cards/views via REAL `run_evidence_v2_interactive._build_card`/`_build_view`
    with real task authority, validated via real `validate_evidence_card`/
    `validate_edition_view`; digests via REAL `_evidence_result_set_digest`/
    `_view_set_digest` (keys `package_sha256`/`results sorted`, `rows sorted`;
    run-dir name == digest enforced at HIGH materialization). No
    `hashlib.sha256(b"screening")`/`b"profile"`/`b"result-set"` constants; no
    `if False` ledger code; no invented ledger shape.
  - Ledger via REAL row construction (same logic as production
    `build_materiality_ledger`: one row per Discovery, `KEEP/MAYBE/INSPECT` →
    exactly one task, `DROP` → `DUPLICATE`/`EXCLUDED`, View disposition,
    rationale) with REAL 7-field basis (all file SHAs + `evidence_set_sha256`/
    `edition_view_set_sha256` from real acceptances), validated via real
    `_check_ledger_rows_content`.
  - Completeness via REAL Profile-initial ∪ Discovery-named union (same
    enumeration as `_check_profile_completeness_extra_content`), explicit full
    7-field request rows for the entire union (no new IDs, no silent drops),
    dimension/description from OLD valid completeness where Profile lacks them
    (no invented defaults), `discovery_ids`/`evidence_task_ids` re-derived from
    ledger/Discovery (not trusted), `overall_status` via REAL logic
    (`READY`/`LIMITED`/`INCOMPLETE`, never `COMPLETE`), THEMATIC closure via
    REAL Discovery-provenance counters, validated via real
    `_check_completeness_result_content` (in `survey_evidence_v2`) +
    `_thematic_closure_errors` + `_validate_obligation_shape` (no swallowed
    Discovery errors, no `{"task-placeholder"}`).
  - Proof via REAL full affected/unaffected comparison (every affected ID old/new
    full card bytes + ledger-row immutable-field checks; every unaffected row
    full semantic equality; mechanical `field_path`/`old_sha256`/`new_sha256`/
    `reason` for basis-SHA propagation only, no directory-prefix exclusion;
    `rows_checked` must be >0, zero-row PASS refused) + REAL tool-pin binding
    (every `tool_shas` path re-hashed, stale pins refuse) + REAL Raw refs
    (every `raw_refs` SizedRef re-hashed) + manifest/decision/before-COPY
    bindings + retention/lineage + SELF digest via `sha256_object`
    (not `sha256(json_bytes)`). No zero-unaffected PASS, no placeholder
    `result_set`/`view_set` digests after SELF.
  - Four-ref loads via FULL validators (not rehash-only): per-card/view digest
    recompute + ledger basis/row checks + completeness obligation shapes +
    `overall_status` enum + profile/issue identity, plus `artifact_refs` mapping.
- Checker: `check_supersession_record_from_paths(repo_root, checkpoint_path,
  report_path, before_copy_path) -> list[str]` (REQUIRED signature) validates
  the FULL graph (checkpoint schema/kind/reason/operation/boundary/checkpoints/
  artifacts/SELF, report schema with NO checkpoint/afterState/guard-hash refs,
  report↔checkpoint proof/decision/request/manifest/before cross-bindings,
  before-COPY equality, sole `DM022_SUPERSESSION_PROOF` review, four artifacts
  via FULL `_load_typed_four_refs`, retention plan 7-row SizedRefs, lineage
  shapes). No hash-only acceptance, no trusted booleans.
- Eligibility: HIGH `verify_live_eligibility` now uses ACTUAL State shapes
  (`human_gates` strings `pending`, `human_gate_provenance` nulls,
  `exception_gate.status == "inactive"`, `publication_revalidation_provenance`
  null, downstream provenances `None`, lifecycle `EVIDENCE_REVIEWED`,
  canonical LIVE path check, approval-file absence) after full public
  `agent.validate_agent_state` on the same bytes. No dict-valued Human Gate /
  empty-Exception confusion.
- Resume/CLI/anchor/completion (no noop stubs, no `if False`, no advice-only
  resume): five narrow step oracles (`claim_guard`,
  `write_checkpoint_as_planned`, `replace_state_triplet`,
  `clear_remaining_exact_slots`, `write_cleanup_completion`, `release_guard`)
  are REAL bound-context steps (each verifies guard intent + executes exactly
  one IO-verified step; outside adopt context they raise explicit
  "requires HIGH adopt context", not silent success). `resume_bound_attempt`/
  `resume_revision` EXECUTE bounded remaining state/slot/completion steps with
  known old/new/unknown/nonce-bound context (`B` → switch+clear+complete+
  release; `E` + guard → clear-remaining+complete+release; `E` + no guard +
  completion → `ALREADY_ACTIVE` no writes; else `INDETERMINATE` preserve, no
  automatic restoration). Repeated correction preserves the REAL original
  anchor/predecessor lineage (previous PREARCH `original_anchor` carried,
  `supersedes` appends previous ref; first correction anchors to before
  evidence). Completion validates FULL receipt schema/inventory/COPY-derived
  expected-after cross-binding (`expected_after` recomputed from COPY +
  checkpoint, not trusted), `postread.triplet_match/artifacts_rehashed` true
  via recomputed four-ref loads, seven_plan cleared/absent_legitimate with
  inode-aware slot checks (regenerated same-byte new-inode files allowed via
  retention-inventory inode comparison; stale same-inode files refuse; guard
  loss never grants permission). Actual CLI with four operations
  (`prepare`/`adopt`/`resume`/`readback`, `argparse`, JSON stdout, exit
  0/1, `if __name__ == "__main__"`).
- Report/checkpoint/review cycles: none (report has NO checkpoint/afterState/
  guard refs; checkpoint has NO guardRef/afterState/completion refs; reviews
  sole `DM022_SUPERSESSION_PROOF` with result → proof file). Contracts: no new
  authorities (uses `core.contract_identity`, no new contract files).
- Shapes: `reason` (not `reason_class`), `from_state`/`to_state` (not
  `from`/`to`), `operation`/`producer_boundary` exact consts, `NamedRef`
  `{name,path,sha256}`, `SizedRef` `{path,sha256,byte_count}`, `ArtifactRef`
  `{path,sha256}` throughout.

## 3. APIs reconciled with B/C (B/C must adapt before frozen snapshot)

- LOW public path APIs (unchanged names, exact shapes):
  `load_typed_checkpoint_record(repo_root, path) -> {family, record}`;
  `resolve_research_authority(repo_root, state_path) -> {family, checkpoint,
  artifacts, artifact_refs, lineage}` (ADDS `artifact_refs` mapping by the
  four role names to `NamedRef`s alongside parsed `artifacts`; output data
  only, consumers reload bytes themselves via the same path+hash);
  `check_supersession_record_from_paths(repo_root, checkpoint_path,
  report_path, before_copy_path) -> list[str]` (REQUIRED 4-arg path signature;
  B's `checker(record)` dict-caller form is REJECTED — keep path reloading, no
  caller-verified dicts, no exception-swallowing fallbacks, no duck-typed
  substitutes);
  `require_research_operation_ready(repo_root, state_path)`,
  `require_no_active_guard(source_root)`,
  `require_completion_consistent(source_root, checkpoint_ref)`,
  `guard_path_for(source_root)`, `lstat_slot(source_root, rel)`.
  Private ` _resolve_research_from_state_bytes(repo_root, state: dict)` is
  structural-only (selected refs only: evidence/materiality/completeness, no
  current-State recursion); `_load_typed_four_refs(repo_root, structural)` then
  fully loads the 4 refs with live re-hash + FULL content validators.
- HIGH sole mutator: `prepare_revision`, `adopt_revision`, `resume_revision`
  (= `resume_bound_attempt`), `readback_revision`, `verify_live_eligibility`,
  `claim_guard`, `write_checkpoint_as_planned`, `replace_state_triplet`,
  `clear_remaining_exact_slots`, `write_cleanup_completion`, `release_guard`.
  `operation`/`producer_boundary` use `from_state`/`to_state`; `reason` is
  `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION` (not `reason_class`).
- REQUIRED B/C fixes (return to Astra before broadening if any cannot be met):
  B `agent._is_prearchitecture_record` + C1 history `_is_prearch_record` must
  use `reason` (not `reason_class`); B `_validate_prearchitecture_core_proof`
  must call LOW checker with 4 PATHS (not `checker(record)`); B operation
  checks must use exact `from_state`/`to_state` (not invented
  `operation.from/to`, list aliases, or weak boundary checks); C2 must remove
  import/attribute/guard catch-all fallbacks (LOW is a required installed
  dependency of G76, not optional) and must allow normal publication/editorial/
  renewal paths after a valid upstream correction (a blanket superseded-mode
  refusal cannot satisfy the required positive witness). C1 must pin
  implementation SHAs for the 5 schemas after A lands (R4 SHAs pinned as
  history; A2 installed report SHA is `10238a1a…` due to the preserved B2
  registry fix, others match R4).

## 4. Actual checks performed (static + REAL private-copy execution)

Per execution discipline (no tests against files another worker is changing;
integration tests await all authors after root freezes the snapshot):

- Static: `ast.parse` OK for LOW (109192B), HIGH (76295B), fixtures (3330B),
  tests (36770B). JSON parse OK for all five installed `schemas/dm022-*`
  (strict duplicate-key refusal at runtime via `schema_gate`). No `if False`
  (0/0), no `task-placeholder` (0/0), no `hashlib.sha256(b"` fabricated
  constants except two deterministic `b"dm022-nonce:"` nonce derivations
  (allowed, per-spec deterministic nonce, not content digests), no
  `reason_class` (0/0), no invented `overall_status COMPLETE` (0/0). Two
  `except: pass` are legitimate best-effort cleanups (retention-inventory
  walk-up continue + temp-unlink cleanup before raising), not validation
  swallows. Every public positive codepath calls a FULL validator (audit:
  all LOW builders/proof/checker + all HIGH prepare/adopt/steps/resume call
  `validate_instance`/`_validate_*`/`_check_*`/`validate_evidence_card`/
  `validate_edition_view`/`_evidence_result_set_digest`/`_view_set_digest`/
  `agent.validate_agent_state`; `require_no_active_guard` is a passive lstat
  oracle (no content to validate); `resume_revision` dispatches to audited
  `resume_bound_attempt`; `readback_revision` runs FULL validation via
  `low.resolve_research_authority`).
- REAL execution (NEW private fixed copy from rejected R1 snapshot with ONLY
  A2 files overlaid + fresh independent fixture DBs, saved raw + source pins;
  NOT live candidate; integration awaits all authors):
  - Private copy: `/tmp/dm022-a2-private` = snapshot R1 worktree (756 files)
    + ONLY `scripts/survey_research_authority_v2.py`,
    `scripts/survey_prearchitecture_acceptance_v2.py`,
    `tests/dm022_prearchitecture_fixtures_v2.py`,
    `tests/test_dm022_prearchitecture_acceptance_v2.py` overlaid. No B/C files
    touched. Python 3.14.4, `jsonschema==4.23.0`, `pypdf==6.16.2` (exact).
    Fixture Git DBs are independent temp dirs (inert `example.invalid` origin,
    process-scoped `dm022-a2-<pid>` identity, no alternates, no hardlinks, no
    `GIT_DIR` overrides, no hook bypass, no root objects, no network). Source
    commits are meaningful (`Synthetic independent DM022 A2 fixture`), not
    empty-root.
  - Command (saved raw): `python3 -m unittest
    tests.test_dm022_prearchitecture_acceptance_v2 -v` in the private copy.
    Raw: `/tmp/dm022-a2-test-raw-20261028.txt` (11 lines,
    SHA256 `1ac355419351eea43fc751db7ed6abdb95350b4b474d4cb3d43c095e2a9b78fe`,
    exit 0). Scope: 5/5 PASS — WEEKLY full prepare→adopt→resume→readback,
    THEMATIC full prepare→adopt→resume→readback, LOW typed-loader dispatch
    (LEGACY vs unknown-kind refusal), LOW guard/slots (absent pass, present
    refuses, nonregular observed, unknown slot refuses), HIGH CLI prepare
    (real `argparse` four-operation CLI, `prepare` via
    `python -m scripts.survey_prearchitecture_acceptance_v2`). No pytest, no
    test-raised expected errors (all `assertRaises` assert REAL code refusals
    on real fixtures: unknown kind, present guard, unreadable slot).
    Fixtures use REAL chain helpers (`test_survey_evidence_v2.make_chain` for
    genuine Discovery/Screening/Evidence/Views/Ledger/Completeness bytes) +
    external synthetic decisions (affected allowlist, Raw files with
    URL/fetched_at/SHA/bytes, interpretation/event/provenance), real Git
    HEAD/tree pins, real contract/tool SHAs, real EVIDENCE_REVIEWED States
    that pass REAL `agent.validate_agent_state` (verified in-test; fixture
    construction fails honestly if validation fails). No fake passed State.
  - Source pins (private copy, A2 files): LOW `c67e0afb…` (109192B), HIGH
    `0407b1aa…` (76295B), fixtures `7fdc692c…` (3330B), tests `749c708e…`
    (36770B). Candidate-work HEAD `409b292…`/tree `8ce36998…` (unchanged, no
    ordinary commit). Installed schemas (candidate-work, unchanged this unit):
    request `a99f0dc1…`, manifest `e7534d01…`, proof `a79c0920…`, checkpoint
    `fd39c246…` (all match R4), report `10238a1a…` (preserved B2 registry fix;
    R4 proposal `21369608…` superseded by installed fix, documented in
    `author-A-return.md` §2).

## 5. Precise map contradictions / TODO / blockers (HONEST, no broadening)

- NONE that blocks A-scope compilation: no new direct reader/closure/contract
  contradiction discovered in A-owned surface. No missing A reader; no omitted
  import closure in A files; no incompatible predicate introduced by A2. Any
  genuine omission found by root/B/C1/C2 returns to Astra rather than
  broadening (per coordination).
- Open interface-consistency items (NOT contradictions, owned elsewhere):
  C1 owns source-family pins/registry/config (`pipeline71→76`, replay
  70/union73, canon 36/41, schema SHAs at code); A validates via installed
  file SHAs at runtime and does not pin family labels. B owns the 17-site
  loader migration + 8 branches + 40-row guard/readiness wiring; A exposes the
  exact `load_typed_checkpoint_record` / `resolve_research_authority` (+
  `artifact_refs`) / `_resolve_research_from_state_bytes` /
  `_load_typed_four_refs` / `check_supersession_record_from_paths` (+ REQUIRED
  4-arg shape) / `require_research_operation_ready` interfaces B needs (see §3
  for REQUIRED B fixes). C2 owns downstream role refusal/readiness + P1/P2R
  explicit copy lists. Cross-owner reconciliation happens at root's frozen
  snapshot, not by A changing trust boundaries here.
- `require_completion_consistent(source_root, checkpoint_ref)` (R4 signature,
  no repo_root) is implemented via deterministic repo-root discovery (walk up
  to `config/survey-production-v2.json`). Documented here so B/C callers do
  not misread it as source_root-relative resolution. If root prefers a
  repo_root-explicit variant, A2 will add it WITHOUT changing the R4 signature.
- Mechanical `result_set_sha256`/`view_set_sha256` in proof `proposed` are
  carried as explicit content digests (R4); full acceptance-run-dir-name ==
  digest binding is enforced at HIGH materialization (prepare writes
  `evidence-runs/<digest>/evidence-accepted.json` +
  `views-runs/<digest>/edition-views-accepted.json`), not inside LOW pure
  proof. No directory-prefix exclusion; every mechanical projection is
  explicitly mappable via manifest/retention SHAs.
- Tests are new-only + existing A-owned (untouched). No old test-count/PASS
  transferred; no implementation acceptance claimed; no Production semantic
  claim. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN remain
  until independent implementation review + affected regressions + Human
  adoption decide otherwise. Integration (both-route positive/negative/
  later-lifecycle witnesses + affected regressions on the frozen snapshot with
  all authors bound) remains for root after A2/B/C1/C2 return. Root must review
  before any completion label; A2 does NOT label scope complete.

## 6. Files for root freeze / next steps

Root binds one immutable complete integration snapshot (all authors bound),
then executes meaningful both-route positive/negative/later-lifecycle witnesses
+ affected regressions (per ROOT §5.2 + decision §10): Weekly+Thematic
genuine-type synthetic fixtures; independent supplied research decisions;
complete four-artifact acceptance; affected/unaffected comparison + full
obligations; 7-slot retain/clear + audit no-overwrite + regen; repeat;
wrong-role publication refusal; forward Architecture/Draft/publication +
history separation; G71→G76 unchanged-upstream compat control; G76 correction→
initial publication→editorial/renewal; old/new/unknown State + guard/completion
loss + stale Raw/HEAD + ownership/close/replace faults + late-seam explicit
resume; synthetic reviews stay nongenuine. After freeze, run at minimum:
`python -m unittest tests.test_dm022_prearchitecture_acceptance_v2 -v` (A2)
plus B/C1/C2 suites + affected `test_run_evidence_v2_interactive`,
`test_prepare_evidence_run`, `test_prepare_screening_run`,
`test_accept_evidence_results`, `test_accept_screening_results` (existing
A-owned; A2 did not modify them).

Author: Owner A2. Scope implemented (A-owned only); no implementation acceptance
claimed. Root review required before any completion.
