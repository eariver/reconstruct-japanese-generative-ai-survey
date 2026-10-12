# DM021-P2R independent design review — DESIGN_BOUNDED_PASS

2026-10-13 JST. Fresh author-independent design reviewer, not candidate author/root.

## 1. Role, scope, sources

- **Reviewer:** independent of General analysis/correction author and Astra selector. This is **design-only read-only source review**, not canonical audit, runtime approval, adoption authority, or Human Gate.
- **Reviewed (final authority):** `outputs/rephase-1-dm021-retention-contract-decision.md`
  SHA256 `194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e`.
- **Superseded where final differs:** `notes/rephase-1-dm021-promotion/analysis.md` (initial proposal),
  `notes/rephase-1-dm021-promotion/correction.md` (P2a convergent-retry / 2-arg verifier / `RETENTION_MANIFEST_V1` header),
  per packet README and decision §§5–6.
- **Also read:** `notes/rephase-1-dm021-promotion/task.md`, `README.md`, `source-binding.md`,
  `astra-feedback.md`, `correction.md`, P1 assessment §4 scope.
- **Method:** targeted file reads in
  `/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60`;
  sanitized `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`
  `rev-parse HEAD / HEAD^{tree} / status --porcelain / diff --name-only` (all rc=0, tool-observed only).
  No source/schema/test edits, fixtures, imports, tests, network, restoration, DB/index/ref/commit
  mutations, old scripts. No raw-log claim: observations are tool outputs, not persisted raw transcripts.

## 2. Source basis re-observed (summary, not continuous proof)

- `HEAD` `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`.
- `status --porcelain=v1 -uall`: 3M + 10A = 13 rows, matching P1 freeze shape:
  M `scripts/survey_reader_surface_gate_v2.py`,
  M `schemas/reader-surface-gate-v2.schema.json`,
  M `schemas/reader-surface-semantic-review-v2.schema.json`;
  A `scripts/survey_editorial_correction_proposal_v2.py` (prefix `5d2fde45`, re-hashed),
  A `schemas/editorial-correction-proposal-v2.schema.json`,
  A `tests/test_survey_editorial_correction_proposal_v2.py`,
  plus 7 LF2I-inherited files. `diff --name-only` = the 3M paths.
- P1 increment is 3A1M; the two Gate paths are LF2I-inherited, not P1 modifications
  (correction E-correction accepted; decision does not relabel them).
- Proposed P2R delta `scripts/survey_editorial_retention_v2.py`,
  `schemas/editorial-retention-manifest-v2.schema.json`,
  `tests/test_survey_editorial_retention_v2.py` absent in both reconstruct and
  candidate — no collision, no hidden modification. Budget 3A, no modifications, is structurally available.

## 3. Verdict

**DESIGN_BOUNDED_PASS** — final P2R one-shot retained-root capture + standalone 3-arg verifier
is a coherent, bounded, useful retention-only step. Full promotion/reason/State adoption
remains correctly unselected. No CHANGES_REQUIRED at design level; §7 lists
implementation-interface conditions (must close before code), not blockers.

## 4. Findings — coherence checks (all pass)

### 4.1 Unchanged P1 refusal preserved; no post-write P1 call

- P1 `_retention_plan` refuses existing COPY destinations:
  `scripts/survey_editorial_correction_proposal_v2.py:1278-1282`
  (`is_symlink() or exists()` → `RETENTION_DEST_CONFLICT`). Verified by read.
- Decision §§5–6 explicitly: unchanged P1 **will refuse after capture**; neither automatic
  partial retry nor “fresh P1 validation after retention” is part of P2R; post-write proof
  belongs to `verify_retention`, not re-running P1. Capture’s P1 call is pre-write only
  (§5 step 1), finalization rechecks pinned input hashes without recalling P1 (§5 step 4).
- Supersession explicit: “General correction.md's contrary retry/future-validation claims are
  superseded by this section.” Coherent and fail-closed.

### 4.2 No retry / adopt / cleanup of existing partials

- Decision §5: no rollback, recursive cleanup, truncation, overwrite, deletion-to-rerun,
  automatic repair or partial-resume. Failure after root claim leaves owned partials +
  actionable report, live originals untouched. Any existing retained root refuses —
  including empty directory, dangling alias, same-byte foreign files. Caller with prior
  success may only call read-only `verify_retention`; that is verification, not idempotent
  adoption. Stale/incomplete tree needs separately authorized recovery; P2R never directs
  deletion to make P1 pass.
- This deliberately supersedes correction.md §4–§5 “convergent retry (adopt equal bytes)”.
  The one-shot choice is simpler, avoids equality-based takeover, and its manual-intervention
  cost is explicit (§1: “not zero”). Bounded and useful: every destructive-promotion
  alternative needs old-byte persistence first (§1). No hidden idempotence claim.

### 4.3 COPY vs KEEP dependency semantics

- COPY destinations exactly P1 `retained_dest` (`proposal_v2.py:1247` verified);
  KEEP rows stay exact `retained_ref`, not copied, must verify hash+size (§3).
- Decision §3: “dependency-bearing retained set, **not** a self-contained backup.
  COPY can remain valid after live source replaced; KEEP still depends on immutable
  original bytes. Captured State/checkpoint/receipt refs are historical identifiers only.”
- Matches P1 graph policy (`:597-599`, mutable set `:574-595`: effective rows, receipt
  outputs, receipt, reviewed reader, bundle results, State, pre-TeX review,
  publication-authored inputs → COPY; else KEEP). KEEP drift fails even when all COPY
  match (§4). Correct fail-closed dependency treatment.

### 4.4 Explicit proposal / basis binding

- Manifest must carry `proposal_ref` (exact path/SHA256, proposal_id, issue_id, Profile labels),
  exact complete P1 `proposal.basis` object, exact `proposed` refs/canonical digest,
  rows one-to-one with P1 canonical `retention_plan` (same ordered roles, path/hash/
  byte_count/policy, KEEP ref or COPY dest + read-back SHA/count equal to source row),
  `capture_inputs` from P1 `input_hashes` + enumerated P2R dependencies (§4).
- P1 basis shape verified at `proposal_v2.py:1462-1476` (state_ref, validation_checkpoint_ref,
  active_revalidation_ref|null, active_reader_input_ref, before_graph_digest,
  preserved_upstream_digest, generated_receipt_ref, renderer_commit, contract_identity);
  P1 `validate_proposal` returns `input_hashes` + `proposal` unchanged + measured digests
  (`:1823-1830`). Decision’s binding fields exist in source. No omitted/extra/duplicate
  path or role, conflicting policy or identity permitted. Adequate.

### 4.5 Safe canonical layout resolution after mutable State changes

- Proposal dir derived from validated Profile `source_root` + `proposal_id`:
  `proposal_v2.py:1323-1330` and `:1730-1741` (canonical `publication/v2/editorial-corrections/<id>`,
  layout mismatch refuses). Verified.
- Verifier must derive layout from exact bound retained Profile/source-root relation, not
  basename guess or trusted manifest prefix; must check required KEEP Profile bytes before
  using paths (§4). Profile is KEEP under observed graph (bundle Profile node at `:774-776`,
  upstream Profile at `:1164-1165`; Profile path not in mutable set `:574-595`), so a live
  State replacement (State is COPY) does not break layout resolution, while Profile drift
  fails closed. Verifier needs no current live COPY originals or State eligibility (§4).
  Coherent; exact KEEP-Profile row selection is an interface condition (§7), not a design gap.

### 4.6 Exact owned inventory

- Owned set: exactly COPY destinations + final `<proposal_dir>/retained/retention-manifest.json`;
  directories exactly ancestor closure including owned root; only regular files allowed;
  unexpected entries (even empty dirs, aliases, special files) refuse completion/readback (§3).
  Retained root exclusively claimed when previously absent; creation failure confers no
  ownership; before/after writes recheck root/ancestor ownership, unexpected replacement
  stops with no foreign cleanup (§5). Temp entries must be in reviewed ownership protocol
  or avoided; no undeclared temp writes. Closed inventory, no takeover. Coherent.

### 4.7 Preflight / final input and drift guards

- Step 1: safe-read canonical proposal/State/Profile, reject existing retained root, run
  unmodified P1 validation, pin HEAD/P2R deps/config/control/source-survey snapshot, capture
  raw inputs before any rereading validator, recheck afterwards.
- Step 2: full-plan preflight (paths, aliases/nonregular, namespace overlaps, COPY bytes,
  KEEP refs), snapshot consumed inputs + required inventories, FIFO/device never opened
  before type check, no writes on predictable preflight failure.
- Step 4: before manifest publish, recheck all P1 input hashes, retained bytes/KEEP refs,
  HEAD/P2R deps, input inventories except precisely owned new retained entries; extra/changed
  input, disappearance, mode/type change, or unowned output refuses; source/survey snapshot
  must allow only exact owned retention delta (§5). Mirrors P1 `_Collector` raw-safe discipline
  (`proposal_v2.py:87-135,191-234`). Detectable drift at checked boundaries fails closed;
  no global CAS/crash-atomicity claimed (§5). Adequate.

### 4.8 Final manifest partial / close errors and result classifications

- Manifest serialized last from measured bytes, exclusive create, full write/close + readback,
  standalone verification + final no-drift checks before `RETAINED_SET_CAPTURED`; merely
  existing manifest insufficient; partial/malformed/close-failed artifact preserved as
  incomplete/indeterminate, never rewritten into success (§5). Crash may leave physically
  valid manifest with no delivered success; readback establishes consistency, not historical
  success event; no success count from file presence. `RETAINED_SET_VERIFIED` only for
  complete matching manifest + exact inventory + all required refs; missing/malformed/partial
  never success; valid-manifest readback distinguished from delivered success (§§4–5, §7).
  Exact enum/error-shape text is an interface condition (§7). No semantic/PASS conflation.

### 4.9 No semantic / adoption / PASS producer

- `validate_proposal` unchanged and strict; capture calls it **without scope review**;
  valid `REVIEW_REQUIRED` (`proposal_v2.py:50`, returned at `:1809-1810` when
  `scope_review_path is None`) suffices to copy old bytes, not promote them. No new review
  producer or semantic-PASS requirement; already-reviewed proposal reused without regenerating,
  rebinding or adopting review (§2). P1 docstring “No writes, no approval, no reason enum,
  no State adoption” (`:1-23`) preserved. Correct: retention ≠ promotion.

### 4.10 Future retained-aware CURRENT authority debt explicit

- §6 is an explicit stop: retained-aware freshness/adoption check unsolved, must bind fresh
  State/receipt/control/accepted upstream + proposal before-identity while validating exact
  retained set; may refactor P1 with narrow retained-context path or another reviewed verifier;
  no permissive flag, trusted assertion, deletion, or manufactured former State; P2R readback
  alone cannot supply that check. If pre-implementation schema cannot preserve needed identities
  without selecting full adoption, return exact blocker. This is stated as known boundary, not
  hidden composability promise. Satisfies task Q6 “select useful next contract or exact blocker”.

### 4.11 Fixtures adequate; no new Human Gate; no same-SHA rebind

- §7: real accepted-chain **synthetic** Longform + Weekly fixtures at exact source (as P1),
  Longform prose primary, Weekly envelope-only, accepted Draft/upstream unchanged; no
  production-owned edition or new Human Gate to test mechanics; genuine semantic/visual/
  Preview acceptance separate. Positive COPY+KEEP inventory with before≠proposed inequality,
  R1-predecessor fixture distinguishing checkpoint from active-before; refusal/controls for
  alias/nonregular/out-of-root/overlap/empty-preexisting/same-byte-foreign/malformed/
  omitted-extra-duplicate/unexpected entries; drift injection at pre-finalization seams;
  short/write/close/readback/final-manifest faults with preserved partials and accurate
  classification; live-COPY mutation persistence vs retained/KEEP/proposal/staged mutation
  failure; wrong-path manifest failure (“same SHA is not a path rebind”); unmodified P1
  rejection after capture; verifier without P1/State-authority bypass. Mechanical oracles,
  refusal-based except positive chain; no synthetic PASS as real review. Matches Astra
  feedback §5 (no production fixture / no new Gate required). Manifest must not infer new
  review target (§3). Adequate.

## 5. Initial-analysis corrections adequate

- **Changed-byte revalidation:** correction E1 + decision §1 correctly state
  `survey_agent_control_v2.py:1844-1876` admits changed surface rows (verified
  `:1860-1876`: under-surface changed → `superseded`; outside-surface drift refuses
  `:1871-1872`; empty superseded refuses `:1875-1876`) under restricted
  `REVIEWED_CORE_CHANGE` (`:45` verified). Real gaps are editorial authority, full
  closure, path/State/pending integration — not “old-byte-only checker.” Fixed.
- **Longform strict cycle:** DRAFT_COMPLETE-only initial (`longform_derivation_v2.py:1101-1139`
  verified) vs healthy-readback allowlist `:1142-1182` (verified, excludes pending/editorial
  renewal `:1149-1151`); receipt demands canonical surface/archive/receipt paths
  (`longform_generated_v2.py:721-730` verified) + strict healthy-State reload `:698-730`.
  Decision cites all three ranges correctly. Fixed.
- **Weekly pending ≠ editorial authority:** `survey_weekly_derivation_v2.py:481-487`
  verified (checked pending-basis branch); decision states it without proof of editorial
  scope/retention authority, no blanket bypass. Correct, no reuse claim.
- **Candidate ≠ publisher:** `survey_publication_v2.py:668-746` verified (validates
  manuscript/bundle/reviews, `_write_immutable`; no publisher re-entry). Decision states
  exactly this. Fixed (Candidate-as-publisher conflation rejected).
- **No tiny budget / no linear scheduler:** correction E4 withdraws `1A1A2M`; decision §1
  withdraws tiny full-writer budget + unchanged-validator bridge, offers cost drivers only,
  net savings unmeasured, manual cost explicit. Correct order lists pre-TeX scope/semantic
  PASS before generation (publisher requires PASS before TeX at
  `survey_longform_semantic_publication_v2.py:480-486` verified; receipt consumes review at
  `longform_generated_v2.py:686-693`) but decision explicitly disclaims certified topological
  scheduler. Second live-review default withdrawn (E3); neither versioned-target nor second
  review selected, same-SHA retargeting forbidden. Fixed.
- **Source-binding errata:** Gate paths relabeled LF2I-inherited (accepted); transcripts
  declared summaries, not raw logs (preserved); alias legend + full filenames used.
  Decision uses `schema_version: "2.0-rc1"` + `kind: "EDITORIAL_RETENTION_V1"` (consistent
  with P1 `proposal.schema_version 2.0-rc1` at `:1455` and Candidate `:732`), improving
  correction’s `RETENTION_MANIFEST_V1` version misuse; 3-arg
  `verify_retention(root, proposal_path, manifest_path)` improves correction’s 2-arg form
  by binding explicit proposal against path rebind. Both changes are intentional and coherent.

## 6. Blockers vs implementation-interface conditions

- **Concrete blockers to DESIGN acceptance: none.** No design change required before
  Human Commit Point.
- **Next-unit gates (not invented approvals, per task + decision §§2,8):**
  1. This independent review + Astra resolution (closeout of this unit).
  2. General’s P2R interface/fixture return to Astra **before code**: actual module
     imports/helper feasibility, complete schema/return/error shapes, safe filesystem
     algorithm (retained-root identity/ownership, ancestor checks, exclusive-create +
     close/readback, no-temp or declared-temp protocol), canonical serialization/digest
     without self-hash recursion, enumerated P2R module/schema `capture_inputs`,
     exact KEEP-Profile resolution path, concrete test commands/counts after diff
     (not borrowed from P1’s 36). Any necessary change beyond 3A is a scope decision.
  3. Exact-blocker return if concrete schema cannot preserve future retained-aware-check
     identities without selecting full adoption (§6). No reason/pointer/second-review
     policy smuggled.
- **Explicitly not required:** new Human Gate/role, production-owned fixture, full old-suite
  rerun, canonical audit, runtime acceptance, reason/State/Candidate adoption, CLI/config/
  Gate/receipt/publisher changes. Do not impose them.

## 7. Boundaries preserved

- Design-only; no behavior implemented. Whole NOT_READY, step4/B3 OPEN, canonical audit
  unstarted, DM021 OPEN. P1 contract `07e899901f488b256ca846c62b1a1fab3edadc880f34593a38078412aeb3c661`
  and patch `85e9d9ab3c972a786afb1cf2f941bf4dbcfd4980f2e63d0ad9cf6df3cb55963c` unchanged.
- P1 evidence qualifications (filtered statuses, HEAD-inode apply proof, transient `add -N`,
  snapshot≠continuous-proof, local-only predicates, lost pre-fix bytes, exact-run-only scripts,
  synthetic fixtures ≠ genuine approvals, retention plan ≠ retained bytes, no SHA-rebinding)
  remain in force. No new HEAD/commit; ordinary Commit/Push Human-owned.

(End of review.)

## 8. Scoped resolution on `astra-review-resolution.md` (appended, earlier §§1–7 preserved)

2026-10-13 JST. Focused compatibility check only; no re-audit, no source/test/hash rerun.

- **Resolution accepted:** `astra-review-resolution.md` accepts `DESIGN_BOUNDED_PASS` for fixed
  contract SHA256 `194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e`
  with no contract edit. P1 contract/patchpins and actual409+13file source basis unchanged.
  No new approval, Gate, or runtime claim inferred. Compatible with this review's verdict.
- **I1 (Profile binding):** coherent refinement of §4.5's interface condition. Chain
  supplied-proposal SHA → manifest/basis equality → unique `state:authority` COPY row
  matching `basis.state_ref` → verified retained State bytes → exact State `profile`
  path/hash → unique matching KEEP Profile row + verified bytes → source_root/proposal_id
  → canonical paths uses retained history, not an arbitrary Profile-labelled row, basename
  guess, or mutable current State. Cited P1 sites check out by targeted read:
  State node `survey_editorial_correction_proposal_v2.py:608-614`,
  State-bound Profile validation `:414-428`, exact bundle/manuscript Profile equality
  `:493-514`, X `upstream:x-production-profile` `:1159-1165` correctly excluded as
  non-authority. Reject-missing/ambiguous/disagreeing + raw-containment-before-typed-hop
  is fail-closed. No blocker.
- **I2 (raw-read/snapshot/ownership):** coherent refinement of §§4.6–4.7 conditions.
  Not importing P1 `_Collector` wholesale avoids pulling current config/HEAD assumptions
  into the historical verifier; minimal local safe-read + `input_hashes` binding + explicit
  mode/type/ancestor/inventory protocol + exclusive-claim identity + manifest-last
  exclusive-create/write/close/readback (not global atomicity) stays inside the selected
  contract. No generic framework or silent P1 expansion. No blocker.
- **I3/I4 (schema/results/budget/stop):** restate decision §§4–5,7 proof scopes
  (`RETAINED_SET_CAPTURED` = this invocation finished; `RETAINED_SET_VERIFIED` = bound set
  complete now; neither = current/semantic/historical authority; KEEP drift refuses, live
  COPY-original drift after capture is not persistence failure) and affected-regression-only
  budget with exact-blocker return beyond 3A. Consistent; concrete interface approval stays
  Astra engineering decision, not a new Human Gate. No blocker.
- **Attribution:** resolution §3's evidence bounds (summarized tool observations, no raw
  transcripts; review is actual-source design review that did not independently rehash
  all13; P1 freezes remain exact basis) are precise and match this report's §1–§2
  qualifications. No overclaim.
- **Final:** verdict remains **DESIGN_BOUNDED_PASS**; no design blocker. Next is General's
  I1–I4 interface/fixture return, then Astra-selected implementation only.
