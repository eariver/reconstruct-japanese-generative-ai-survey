# DM021-P1 independent implementation/evidence review (author-independent)

2026-10-12. Fresh reviewer, no prior P1 authorship. Read AGENTS, selected
contract `outputs/rephase-1-dm021-contract-decision.md` (SHA07e89990),
mandatory `notes/rephase-1-dm021-contract/independent-source-supplement.md` +
`astra-review-resolution.md`, P1 `task.md`, `astra-phaseA-feedback.md`,
`astra-implementation-selection.md` (overrides correction),
`interface-correction.md`, final Phase-B packet
`notes/rephase-1-dm021-p1/evidence-20261011T201412Z-phaseB/` (report, runner,
freezes, patch, raw logs). Inspected actual candidate source at
`/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`
read-only (source reads, `git rev-parse/status/config/remote`, no edits, no
network, no Production, no commits, no subagents, no test execution, no fixture
creation, no candidate writes). Did NOT assume implementation-report truth;
every claim below is source/log-cited. Narrow probes were not executed because
all load-bearing findings are static source facts; no OWN-copy execution was
needed and none was performed.

## 1. Identity pins (actually observed)

- Candidate base: HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, parent chain via shallow
  `774dd39a...` (shallow file present). `git status --porcelain` exactly 3M10A:
  `M schemas/reader-surface-gate-v2.schema.json`,
  `M schemas/reader-surface-semantic-review-v2.schema.json`,
  `M scripts/survey_reader_surface_gate_v2.py`,
  plus 10 `??` (see freeze). No branch, detached HEAD, no candidate commit.
- LF2I 9 pins preserved (match source-supplement/correction3 manifest):
  gate script `e7305884...`, gate schema `fe4a96f4...`, LF manifest
  `4dadf873...`, LF input `7bae9d2a...`, LF derivation `c09c5558...`,
  LF generated `d480e11d...`, LF publisher `4d235a38...`,
  LF derivation test `ce687447...`, LF integration test `4a03b564...`.
  All modes `0o664`, bytes as in `freeze-pre.json`/`freeze-post.json`
  (identical pre/post).
- P1 4 pins (new relative restored LF2I):
  `scripts/survey_editorial_correction_proposal_v2.py`
  `118d49e54335d46c9abedfbcd95b4fe4ea2f67ca9a2d54a908ba041358b264ea`
  (45132 B, 801 lines);
  `schemas/editorial-correction-proposal-v2.schema.json`
  `54b17f0543cc063c4c5d4e53f3cc82d22ea077643b17292fea20ebf8b5cb6aee`
  (3465 B);
  `schemas/reader-surface-semantic-review-v2.schema.json` (M)
  `e8598239d3ca00441f61110fd77a7b7edf063ac15a7a6a1c2efdb38e73d6699b`
  (4219 B);
  `tests/test_survey_editorial_correction_proposal_v2.py`
  `1b62b2d7756d15785564e33ea12393ae75a4d1881af22c1c55642cbcb8eb2c2b`
  (49968 B, 867 lines, 5 test methods).
- Final packet: `complete-p1-overlay-13path.patch` 474268 B,
  SHA256 `5f087f1373d8e532b33ec58530f8567e81f23ded6c01391bcf37a6c38df8f459`;
  13 `diff --git` headers (3M via `git diff HEAD`, 10A via difflib vs /dev/null
  with synthetic `100644` header). `run.exit` = `exit=0`, `run.stderr.txt` tail
  `Ran 32 tests in 1456.586s / OK` (5 P1 + 27 Gate). `deps.txt`:
  Python 3.14.4, jsonschema 4.23.0, pypdf 6.16.2, yaml 6.0.3, git 2.53.0.
  `freeze-pre.json` == `freeze-post.json` (HEAD/tree/status/files identical).

## 2. Git isolation / read-only routing (actually observed)

- `git config --list --show-origin`: repo `.git/config` has only
  `core.repositoryformatversion/filemode/bare/logallrefupdates`,
  `extensions.worktreeconfig`, `remote.origin.url=https://example.invalid/...`
  (inert fetch+push same URL), worktree `core.sparsecheckout(cone)`;
  no `core.hooksPath`, no `user.name/email` in local (process identity only via
  `-c` in fixtures). No `objects/info/alternates` file. Shallow single line
  `774dd39a...`. `GIT_COMMON_DIR` not set in environment; test `setUp` refuses
  inherited `GIT_DIR/WORK_TREE/INDEX_FILE/OBJECT_DIRECTORY/ALTERNATE.../COMMON_DIR`.
- Hooks dir holds only 14 `*.sample` (executable samples, 0 active).
- Runner (`run_phaseB.py:1-115`) strips inherited `GIT_*`/`PYTHONPATH`, forces
  `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`,
  asserts exact 3M10A pre AND finally-post (HEAD/tree/status/files), removes
  `__pycache__` byproducts, preserves partial timeout output, refuses on
  existing logs (exclusive). Test helpers `_run_git`/`_run_fixture_code`
  (`test:63-72,456-471`) use same sanitized env + process-scoped
  `Synthetic DM021-P1 Fixture` identity, inert origin
  `https://example.invalid/dm021-p1-fixture.git`, no `fetch/clone`, only
  `init/remote add/add/commit/rev-parse/status/config --local --list`.
  Fixture source commit pins all 10 `UNTRACKED_SOURCES` (`test:46-57,91-99`)
  with sha equality; asserts clean status and no local `user.name/email`
  (`test:110-114`). No empty commits (basis commit has full source;
  derivation-only commit changes one TeX-comment literal, `test:316-330`).
- No lazy-fetch, no `file`-protocol fixture use, no inherited routing. PASS.

## 3. Truly read-only, no roles/reason/adoption/PASS — PASS with one note

- `survey_editorial_correction_proposal_v2.py` contains no `write_bytes/
  write_text/core.write_json/open(*w/mkdir/unlink/rename/commit/subprocess/
  shutil` writes; only `read_bytes` via `_Collector.safe` + validator re-reads.
  No call to `agent.revalidate_publication_surface`, no `REVIEWED_CORE_CHANGE`
  construction, no `reason` enum, no State write, no CLI, no Gate/receipt/
  Candidate creation. Returns only in-memory `proposal/proposed_canonical/
  graph` (`prepare`) and `{result: REVIEW_REQUIRED|REVIEW_BOUND_PROPOSAL,
  input_hashes, proposal}` (`validate`). Entry `_Collector` pins HEAD/config/
  file bytes, `reverify()` + `_tree_map` comparison enforce no-write before
  return; tests assert file/HEAD/status equality before/after every P1 call
  (`test:118-134`, used in all 5 methods). PASS.
- Note: `_pipeline:548` reads `agent._publication_revalidation_roles` only as a
  canonical-path allowlist (`ROW_NOT_CANONICAL`); it does not create roles.
  Allowed read-only use.

## 4. Before-graph 7-effective vs original + typed deps — PASS (structure), FAIL (digest membership, see §10)

- `_original_checkpoint:190-212` enforces exact `{path,sha256}` State pin,
  checkpoint identity (`DRAFT_COMPLETE→VALIDATED_DRAFT` + `validation` in
  checkpoints), duplicate-role refusal, row-shape check. Good.
- `_active_effective:215-246` uses real
  `agent.resolve_active_publication_revalidation`; `None` → binds original bytes
  with `ORIGIN=ORIGINAL`; valid record → requires superseded∪preserved ==
  original names exactly once, forbids path rebind (`ACTIVE_PATH_REBIND`),
  checks superseded `new_sha256` / preserved `sha256` against live bytes.
  Distinguishes original-metadata vs effective-current correctly; no filename
  latest-selection, no pending-basis constructor, no fabricated DRAFT_COMPLETE.
  Good.
- `_build_graph:337-507` builds: checkpoint-record node + `CHECKPOINT_ROW`
  edges (effective shas, not old-hash live nodes — correct per selection);
  active-record node + `PREDECESSOR_CHAIN` when present; manuscript
  profile/architecture/approval/primary + `supporting_files` via
  `MANUSCRIPT_SUPPORT`; approval review-summary/attention via
  `APPROVAL_DEPENDENCY`; Gate→receipt + Gate→pre-TeX-review bindings with
  `GATE_RECEIPT_BINDING`/`GATE_REVIEW_BINDING` equality; receipt
  `accepted_refs/authored_refs` with duplicate + `UNCLASSIFIED_DEPENDENCY`
  stops; tool-closure/outputs; quality `QUALITY_OUTPUT`; later
  `SEMANTIC_EDITORIAL`/`VISUAL` via real `reader.validate_review_record` +
  manuscript/source/pdf drift checks; optional observed/unadopted Candidate via
  real `publication.validate_candidate` + divergence refusal, never owned by
  filename. Roles union via `_Graph.node` with `HASH_CONFLICT`/`POLICY_CONFLICT`
  stops; nodes/edges canonically sorted; `before_graph_digest =
  core.sha256_object({nodes,edges})` (`_pipeline:616`). Matches selection
  wire/dedup/conflict rules. PASS for structure.
- Count not enforced to exactly 7 names (relies on allowlist + coverage);
  fixtures always have 7, so no false accept observed, but explicit 7-name
  assertion is absent. Minor robustness note, not a correctness failure.

## 5. Lossless roles union / policy / canonicalization — PASS

- `_Graph:280-307` one node per normalized path, `sha256+byte_count` equality,
  `policy` equality, `roles` union (append if absent), canonical sorts roles.
  Retention (`509-532`) emits one row per node with both `role=roles[0]`
  (deterministic first-sorted) and full sorted `roles`; `KEEP` → `retained_ref`
  equal identity, `COPY` → deterministic
  `<proposal_dir>/retained/before/<rel>` with overlap/dup/present (incl.
  dangling alias via `is_symlink`) refusals. Exact `retention_plan` equality
  check in `validate_proposal:781` catches missing/extra/conflicting rows.
  No first-wins loss. PASS.
- Extra singular `role` key is not in selection's canonical
  `{path,sha256,byte_count,roles,policy}` description and is not declared in
  the implementation report (selection requires declaring any extra wire key).
  Lossless but undocumented. See §11.

## 6. Preserved-upstream digest — CHANGES_REQUIRED (see §10, load-bearing)

- Structure (`500-506`): `preserved_digest = sha256_object(sorted
  {kind,path,sha256})`, sorted by `(kind,path)`, excludes State/checkpoint/
  revalidation/tool/outputs/QA/review/PDF/Candidate/publication nodes by
  construction. Exclusion direction PASS.
- Inclusion direction FAIL: `_frozen_member_kind:317-334` never matches receipt
  accepted/authored roles (static bug). Details in §10.

## 7. Typed approval / transitive validation — PASS (qualified)

- Manuscript via real `reader.validate_manuscript_manifest:553`; receipt via
  full `longform_generated.validate_receipt` / `weekly.validate_receipt:587-590`
  (not `verify_tool_basis` alone) + `contract_identity` equality (`592-594`) +
  reader-binding stability (`595-596`); Gate via real
  `surface_gate.validate_reader_surface_gate:598-604` + `GATE_NOT_PASSED`;
  pre-TeX authority via real loader with expected before path/sha (`606-610`);
  bundle via real `quality.validate_bundle:611`; later reviews via real
  `reader.validate_review_record:469`; Candidate via real
  `publication.validate_candidate:490`. Approval review-summary/attention
  pinned via `_add_file` against approval-recorded shas (`397-405`); drift
  fails closed (`REF_DRIFT`). No generic string-following resolver; provenance
  literals (URLs/reviewer/executor) never followed. PASS.
- Approval JSON itself is `core.load_json` without separate schema-validator
  call; binding still fail-closed via manuscript-validator pin + `_add_file`
  sha equality. Acceptable, noted as qualification.

## 8. Independent derivation, no pending/fake State — PASS

- `_derive:257-271` pins authored input via `safe`, then calls real
  `longform_derivation.load_derivation_for_readback` (Longform) or
  `weekly.load_derivation` (Weekly); requires 6 context keys; wraps
  `ValueError` as `DERIVATION_REFUSED`. No pending-basis construction,
  no `_verify_pending_binding` callee, no manufactured former-State.
  Before canonical vs file equality enforces `NONCANONICAL_BEFORE:579-580`;
  proposed canonical vs before canonical enforces `NO_EDITORIAL_CHANGE:584-585`
  on independently rederived bytes (not file re-serialization), so
  key-order/pretty-print alone is not an editorial change. Upstream set/sha
  equality via `_frozen_names_check:664-672` (receipt vs rederived), not a
  self-asserted flag. PASS.

## 9. Honest R1 predecessor — PASS (code + oracle honest)

- Code never handcrafts a pointer: `_active_effective` only accepts
  State-bound valid record or verified absence; stale/invalid → typed refusal.
  No fake reason.
- Test `test_honest_predecessor_original_vs_active:692-754` performs a real
  derivation-only source commit (TeX-comment literal `DERIVATION_COMMENT_ANCHOR
  →REVISED`, `test:310-330`), asserts `new_head != renderer_before`, then
  executes the post-commit cascade in the FIXTURE's committed code via
  sanitized subprocess (`_FIXTURE_CASCADE:474-535`, `_run_fixture_code:456-471`):
  real `weekly.load_derivation` same-byte proof, real pre-TeX loader check,
  real render/receipt/build/validate, real QA rebuild
  (`_rebuild_weekly_qa_after_regeneration:333-396`), genuine
  `agent.revalidate_publication_surface(..., REVIEWED_CORE_CHANGE, ...)` with
  process identity, then in-fixture `prepare`+`validate` with no-write asserts.
  Oracle displays `ORIGINAL` vs `ACTIVE` origins, changed `validated-source`
  sha, non-null `active_ref`, `before != proposed`, `graph_nodes/edges >20`,
  record file existence + State-pointer agreement + checkpoint stability.
  No handcrafted pointer, no fake reason, no empty commit, all untracked
  P1/LF2I bytes committed before fixture commit. PASS. Epoch-honesty comment
  (ambient code cannot replay committed revision) is accurate and preserved.

## 10. LOAD-BEARING DEFECT — frozen membership misses all receipt authority (CHANGES_REQUIRED)

- Location: `scripts/survey_editorial_correction_proposal_v2.py:324-327`:
  ```python
  for role in roles:
      head, _, tail = role.partition(":")
      if head in ("receipt:accepted", "receipt:authored", "upstream"):
          return tail
  ```
  `str.partition(":")` splits on the FIRST colon. Roles constructed at
  `439-451` are `f"{prefix}:{row['name']}"` with `prefix` = `"receipt:accepted"`
  / `"receipt:authored"`, e.g. role `"receipt:accepted:production-profile"` →
  `head="receipt"`, `tail="accepted:production-profile"`. Condition
  `head in ("receipt:accepted", ...)` is therefore NEVER true for any receipt
  role. Only `"upstream:..."` (head `"upstream"`) and exact
  `"manuscript:profile/architecture/approval"` match.
- Consequence: `preserved_upstream_digest` (`500-506`) covers only manuscript
  profile/architecture/approval + approval `upstream:*` summary/attention
  (≈5 nodes). It OMITS every receipt-accepted/authored authority the selection
  mandates: `synthesis-input/result`, `draft-package:{pid}/draft-result:{pid}`,
  `evidence-acceptance`, `candidate-matrix`, `materiality-ledger`,
  `discovery-acceptance`, card refs, `publication-semantic-input`,
  `drafting-authored-archive` (Weekly `survey_weekly_derivation_v2.py:519-559`;
  Longform authored refs `survey_longform_generated_v2.py:612-623` same shape).
  Nodes that share a physical file with manuscript (profile/architecture) are
  still frozen via the manuscript role, masking the bug for those two paths;
  all other authority files are silently excluded.
- Security impact: scope `preserved_upstream_sha256` binding and proposal
  `preserved_upstream_digest` do not actually bind Draft/Synthesis/Evidence/
  Discovery/Selection/Matrix/Materiality/authored-archive bytes. A Draft drift
  after `prepare` would still fail closed in `validate_proposal` via
  `_frozen_names_check` (`UPSTREAM_SET_DRIFT/UPSTREAM_REF_DRIFT`) during
  re-derivation, so this is not an open false-accept in the current pipeline
  order — but the digest's stated guarantee is false, `SCOPE_STALE_UPSTREAM`
  cannot fire for those files, error codes misattribute, and any future
  consumer trusting the digest alone would be unprotected. Selection §20
  membership ("MUST include Profile, approved Architecture/its typed approval
  and review-summary/attention dependencies, exact accepted Draft
  packages/results + Draft authored archive, Synthesis, Evidence
  acceptance/required package/task/card dependencies,
  Discovery/Selection/Matrix/Materiality/completeness authority") is violated.
- Oracle gap proving the miss: `test_longform_prose_correction_end_to_end:
  621-623` asserts only `production-profile` and `issue-architecture` in
  `frozen_kinds`; no test asserts Draft/Synthesis/Evidence/Discovery/Matrix/
  Materiality/authored-archive presence, nor fails if they are absent. Hence
  32/32 passes despite the omission. No mask-success, but insufficient
  frozen-completeness oracle.
- Required fix: correct the prefix test (e.g. `role.startswith
  ("receipt:accepted:")/"receipt:authored:"/"upstream:"` with appropriate kind
  extraction, or split on last colon / check full prefix), re-derive expected
  digests, extend focused tests to assert the full mandated membership
  (including at least one Draft package/result, Synthesis input/result,
  Evidence acceptance, Matrix/Ledger/Discovery, both authored refs) and assert
  absence of State/QA/tool/publication nodes. Do not broaden to a generic
  allowlist; keep `UNCLASSIFIED_DEPENDENCY` stop and known-record-only walk.

## 11. Secondary wire deviations (fix with §10 or obtain Astra waiver)

- (a) Persisted `proposed` omits `proposed_reader_ref`. Correction §6 (+ selection
  adoption) specifies `proposed: {authoring_input_ref, proposed_reader_ref,
  proposed_reader_canonical_sha256, change_description}`. Schema (`editorial-
  correction-proposal-v2.schema.json:54-67`) and `_pipeline:648-653` persist
  only `authoring_input_ref/proposed_reader_canonical_sha256/change_description`.
  `validate_proposal:785-789` augments in-memory with `proposed_reader_ref` +
  duplicate `proposed_reader_sha256` for scope binding, but persisted
  `proposal.json` never carries the path. Functionally bound via fixed layout
  (`proposal_dir/reader-surface-input-v2.json`) + canonical-sha equality, so no
  false accept — but spec-noncompliant and the duplicate bare-sha key is
  redundant with `proposed_reader_canonical_sha256`. Either persist the exact
  §6 key or return to Astra for a wire amendment; do not keep an undocumented
  deviation.
- (b) `basis.active_revalidation_ref` defined as nullable in properties but
  absent from `required` (`schema:30-39` vs `43-45`). Pipeline always emits the
  key (null when absent), and `BASIS_MISMATCH` enforces equality, so omission in
  a supplied file fails closed — but schema permits an absent key the contract
  says must be present-as-null. Make it required (nullable) to match §6.
- (c) Retention rows carry extra singular `role` alongside required sorted
  `roles` (`schema:74`, `module:514`). Lossless (full `roles` preserved) and
  deterministic (`roles[0]`), but selection's canonical row is
  `{path,sha256,byte_count,roles,policy}` and requires declaring any extra wire
  key. Report does not declare it. Either remove `role` or declare and justify
  it.
- (d) Config read bypasses `safe`: `_Collector.__init__:91` + `_pipeline:540`
  + `prepare/validate:680,754` do `core.sha256_file/load_json(root /
  DEFAULT_CONFIG)` without `col.safe` alias/regular checks, contrary to "raw
  path safety must precede content reads." Later `reverify` detects drift but
  not a symlinked config at entry. Low exploitability (fixed repo-local path),
  but fix by routing config through `safe` or documenting the exception.
- (e) Later-review referenced files (`manuscript/source/pdf` from
  `reader.validate_review_record:469-481`) are validated by the external loader
  before `col.safe` pinning; review file itself was already pinned via
  effective, and drift is caught by subsequent `safe` + `reverify`, so
  fail-closed — but order is validator-before-pin for those three refs by
  necessity (refs discovered by validator). Noted as qualification, not a
  defect.

## 12. Scope loader timing / block semantics — PASS (qualified)

- `_validate_scope:691-746` captures raw bytes BEFORE the loader (`694-695`),
  calls `surface_gate.load_and_validate_reader_surface_semantic_review` with
  expected AFTER path/sha + `require_pass=True` (`706-710`), re-compares disk
  bytes after (`713`), binds `review_sha256` recomputed over captured JSON
  (`715`) and loader digest (`717-718`), reads the optional block from captured
  bytes (`719`), never rereads. Matches selection §30; no second-read switch.
  (`captured_sha:696` is computed but unused — dead variable, harmless.)
- Outcomes: no arg → `REVIEW_REQUIRED`; valid ordinary PASS without block →
  `REVIEW_REQUIRED` (record stays ordinarily valid, never correction approval);
  malformed/non-PASS/wrong-target/stale/reject/needs-Owner → typed refusal
  (`SCOPE_ORDINARY_INVALID/BLOCK_SHAPE/NOT_WITHIN_AUTHORITY/WRONG_BEFORE/
  WRONG_AFTER/STALE_UPSTREAM/CHECK_NOT_PASS`), never bound. Positive requires
  strict block + exact before/after/upstream + substantive `EDITORIAL_CORRECTION
  _SCOPE` PASS check with detail/evidence. Schema strictness for the block is
  enforced by the loader's `validate_instance` against the modified schema
  (additionalProperties false throughout); P1 adds binding checks on top.
  `reader.validate_review_record` used only for later-review graph edges, never
  as scope carrier. PASS.
- Oracle qualification: matrix (`test_refusal_and_scope_matrix:756-852`)
  covers bad-id, alias (`PATH_ALIAS`), traversal, noncanonical-before,
  ineligible-State, retention-dest conflict, noscope→required,
  ordinary-without-scope→required, wrong-before, REJECT, stale-upstream, and
  bound positive with no-write asserts. `REQUIRES_OWNER_DECISION` shares the
  `SCOPE_NOT_WITHIN_AUTHORITY` branch but has no explicit subtest (only
  `REJECT`); add one with the fix. `SCOPE_BYTES_SWITCHED` concurrency path is
  code-inspected only (not raced in tests) — acceptable.

## 13. Test/scenario completeness — PASS on counts/isolation, QUALIFIED on oracles

- Counts: 32 = 5 new P1 (`longform_prose`, `weekly_envelope`, `honest_predecessor`,
  `refusal_matrix`, `ordinary_compat`) + 27 existing Gate controls
  (`test_survey_reader_surface_gate_v2`, the affected control for the shared-
  schema M). No old 43/31 transfer claimed; report explicitly disclaims it.
  No full-suite decoration. PASS.
- Meaningful oracles present: Longform authored-prose positive + noscope/bound;
  Weekly envelope positive + Draft-result/Synthesis/archive tampers (correctly
  expecting `STATE_INVALID` for checkpoint-bound tamper, `DERIVATION_REFUSED`
  for archive tamper) + same-byte `NO_EDITORIAL_CHANGE`; honest predecessor
  original-vs-active distinction; refusal/scope matrix; ordinary-review
  compatibility (loader PASS without scope, then `NO_EDITORIAL_CHANGE` for
  same-byte prepare). Fixture adapters (`incb/lf1/lf2i` imports,
  `_clean_discovery` local-source override, `sys.argv` mock for real publisher
  CLI) are in-file and reported, not hidden stubs; synthetic reviews are
  type/identity fixtures with substantive detail/evidence via the real loader,
  never semantic acceptance. PASS.
- Gaps requiring new oracles with the §10 fix: (i) frozen-membership
  completeness (see §10); (ii) explicit `REQUIRES_OWNER_DECISION` refusal;
  (iii) artifact-only HEAD descendant allowed (commit unrelated non-canonical
  file, no revalidation, `prepare` still succeeds when receipt/graph still
  verify) vs control/contract drift refused (change contract/tool without
  revalidation → `RECEIPT_CONTRACT_DRIFT`/graph refusal); currently only
  control-with-revalidation positive exists; (iv) explicit `HASH_CONFLICT`/
  `POLICY_CONFLICT` contradiction stops (currently only retention-dest
  conflict is exercised). These are CHANGES_REQUIRED companions to §10, not
  standalone passes.

## 14. Restoration qualification / patch — QUALIFIED PASS (no re-assertion of bad predicate)

- Do not restore again. Phase-A restoration is accepted with its separate
  qualification packet `evidence-20261011T161549Z-qualification/` (v2
  `st_dev/st_ino` separation, per-path mode `0o664` + exact status rows,
  stdlib archive audit, config/hooks/route review), which explicitly supersedes
  the legacy `find -printf '%d %i'` depth-as-device error and the hash-only
  overlay verifier. Phase-B evidence correctly does NOT repeat the bad
  predicate; runner freezes record per-path sha/mode/bytes + HEAD/tree/status
  pre/post equality. No new device claim is made in Phase B — correctly
  qualified as preservation, not a new pre-extraction proof.
- Patch includes ALL 13 paths with the M semantic-review schema (verified
  `diff --git` headers §1); modified hunks are `git diff HEAD` bytes; new-file
  hunks reconstruct byte-identical via the generator's custom difflib reparse.
  Qualification: this is content-recovery proof, NOT a `git apply --check`
  against a clean 409 worktree (synthetic `100644` headers, difflib formatting).
  Do not cite it as clean-base application proof. No candidate commit; ordinary
  reconstruct Commit/Push remains Human-owned.

## 15. Verdict: CHANGES_REQUIRED (narrow, implementable)

- Primary: fix §10 frozen-membership predicate + frozen-completeness oracles.
- With it: resolve §11(a)-(d) (persist or waive `proposed_reader_ref`, require
  nullable `active_revalidation_ref`, declare/remove singular `role`, route
  config through `safe`/document, add `REQUIRES_OWNER_DECISION` + artifact-only
  vs control-drift + contradiction oracles), then return for Astra code review
  and a fresh independent re-review. No other runtime paths, no CLI/writer/
  State/reason/PASS, no promotion/adoption.
- Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted; DM-021 remains
  OPEN (P1 preparatory, not repair). No 43/31-test transfer. Stop at Human
  Commit Point; no automatic next unit.

## 16. Method limits

- No test execution, no fixture/Git mutation, no network, no Production reads
  beyond the candidate worktree, no empty-commit or branch operations. All
  `/tmp` availability statements are read-observed at review time; closeout
  absence override for other environments stands. Source lines cited are
  candidate bytes at the §1 pins; any later candidate movement invalidates
  this review.
