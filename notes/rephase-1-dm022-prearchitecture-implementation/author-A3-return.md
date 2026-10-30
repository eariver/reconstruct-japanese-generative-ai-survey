# Owner-A3 implementation return — DM022 pre-Architecture research operation (CORRECTION)

2026-10-28. Owner A3 (correction implementer replacing rejected A2 R1; R2 snapshot
preserves A2). Human continuation authorized ACTUAL CODE in independent
candidate-work ONLY. Binding order: contract a345bb95 INCLUDING §11, pre-code
assessment §5, precode packet README, mandatory astra-precode-gate-resolution
INCLUDING §5 (FULL 0425c530/13788B), independent readiness §§8–9 FINAL-BINDING,
then R3 (overridden by) R4 + literal 5 schemas, R5 families, R6 roles, then ROOT.
Independent review `independent-research-r2-review.md` §§B1–B8 is the correction
authority for this return; R2 snapshot (`snapshot-r2-20261028T124706Z`, manifest
`53fde56…`) is the frozen base and is untouched. No ordinary candidate/reconstruct
Commit/Push; no fixtures in reconstruct; no git config/global writes; no
network/Production/reset/clean/old-log overwrites. Python 3.14.4 + unittest +
jsonschema 4.23.0/pypdf 6.16.2. A3 unit ongoing — NO Commit Point claimed here.

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all paths below relative to it). Started from R2 (actual409/tree8ce +93);
no ordinary source commit. Prior returns preserved (`author-A-return.md`,
`author-A2-return.md` unchanged); R1/R2 snapshots immutable.

## 1. Exact written paths (Owner A ONLY, disjoint from B/C1/C2)

CHANGED (A3 correction; schemas untouched, byte-identical to R2):

- `scripts/survey_research_authority_v2.py` (LOW) — 132244B,
  `aee60132…` (R2 A2 was `c67e0afb…`/109192B)
- `scripts/survey_prearchitecture_acceptance_v2.py` (HIGH) — 87249B,
  `2fe12b9e…` (R2 A2 was `0407b1aa…`/76295B)
- `scripts/survey_evidence_v2.py` (A-owned leaf) — 125817B,
  `8b55dc6c…` (ADDITIVE ONLY: three detached pure helpers appended after
  `validate_edition_view`; zero behavior change to existing validators,
  producers, writers, or schemas)
- `tests/test_dm022_prearchitecture_acceptance_v2.py` (Owner-A unittest,
  no pytest) — 62293B, `9755279f…` (19 tests: 5 carried A2 positives + 14
  new fault/negative/later-seam tests)
- `tests/dm022_prearchitecture_fixtures_v2.py` — UNCHANGED (`7fdc692c…`/3330B)

NOT touched (other owners, concurrent edits respected):

- B (incl. `run_evidence_v2_interactive.py`, agent/consumers), C1
  (closures/families/config), C2 (publication/editorial/retention), all five
  `schemas/dm022-*.schema.json`, shared fixture helpers. No new runtime
  modules, no new schema files, no closure broadening.

## 2. What A3 closed vs independent R2 review §§B1–B8

B1 — atomic exclusive final claim (HIGH `:69–175`). Replaced lstat+`os.replace`
with single-syscall atomic claim: direct `O_CREAT|O_EXCL` write to the FINAL
path (short-write loop, fsync, checked close, re-read verify, dir fsync,
postread equality) — no temp, no second lstat, no replace. EEXIST (racy or
planted final) refuses with no overwrite; partial finals are PRESERVED with
their path in the error (no hidden unlink). `os.replace` remains ONLY in
`replace_state_triplet` (the allowed known-byte State switch with held-descriptor,
before/recheck/postread, inode-pinned). `_TRY_TMP_COUNTER` removed (no temps).
Covered by `test_late_final_plant_blocks_and_resume_recovers` (planted final →
refuse, planted bytes intact, guard held, LIVE==before) and
`test_replace_tmp_exists_refuses` (planted State tmp → switch refuses).

B2 — runner import removed from LOW (zero `run_evidence_v2_interactive`
imports; docstring updated). Pure record/card/view logic now lives in A-owned
`survey_evidence_v2.py` as exact narrow extractions:
`validate_research_record_content` (`:1549`), `build_research_card_content`
(`:1647`), `build_research_view_content` (`:1782`) — pure dict in/out, only
leaf `task_authority_sources` + local constant sets mirroring the interactive
contract (B keeps its runner copies for the normal path; coordination point
documented in-module). LOW calls the evidence-module helpers at all four
former runner call sites. Test file no longer imports the runner either.
Closure verified: LOW top-level = core+schema_gate+stdlib only; function-local
leaf imports only (evidence/screening/completeness + jsonschema, see below).

B3 — FULL completion verification (LOW `_verify_completion_full`, `:675ff`).
`require_completion_consistent(source_root, checkpoint_ref)` (R4 signature,
repo discovered by location-only walk-up) now runs the FULL chain: checkpoint
FILE/sha + PREARCH family, completion receipt against the EXACT report
`$defs/completionReceipt` schema (`_validate_against_report_def`, `:189ff`;
function-local `import jsonschema` — required runtime dep already wrapped by
schema_gate, no repo-file closure, no agent, no circularity), issue/revision/
checkpoint cross-bindings, retention inventory 7 rows exactly bound to the
stored manifest snapshots (dict equality per slot), COPY-derived
expected_after recompute (byte-compared, never trusted), LIVE canonical State
reload with same-record triplet bound to THIS checkpoint, FULL adopted-graph
validation (recomputes triplet_match/artifacts_rehashed), and seven_plan vs
inventory vs current slots. No trusted booleans anywhere on this path.

B4 — regeneration-tolerant readiness (`_verify_completion_full` slot rule
`:753ff`, shared by `require_research_operation_ready`). After FULL-verified
completion with guard absent: old-absent slots with present files are ALLOWED
(legitimate normal regeneration; stage validators enforce content); present-plan
slots allow new-content bytes and same-byte new-inode outputs; only same-inode
stale bytes refuse (fail-closed when inventory identity unavailable). The old
absence/inode window is not reapplied post-completion. Covered by
`test_absent_slot_regeneration_ready_and_readback` (absent-plan regeneration →
READY passes + readback PREARCH).

B5 — prove FULL NEW validators + Raw binding + per-file refs (LOW
`prove_revision_from_paths`, HIGH prepare manifest).
(a) NEW graph: request loaded+schema-validated from stored manifest ref;
per-file tasks/cards/views refs verified non-empty with live re-hash;
`_validate_evidence_acceptance_content`, `_validate_edition_views_acceptance_content`,
`_validate_materiality_ledger_content`, `_validate_profile_completeness_content`
with exact signatures and root_records/root_path bound to the request
Discovery file (DIRECT session basis); digest recomputes kept.
(b) Raw/event binding: every affected DID must route to ≥1 supplied Raw file
whose basename contains the DID, AND the NEW card's first claim text must occur
in that Raw file's bytes (content binding, not SHA-only); decision assessment
fields verified non-empty strings; `manifest_ref`/`before_state`/`allowlist`
exact bindings kept; raw_refs required non-empty with live re-hash.
(c) Manifest `candidate_outputs.tasks/cards/views` populated by HIGH with a
SizedRef per written accepted-run file (code-enforced non-empty; schema
unchanged per no-broadening rule) and mirrored into proof.proposed with
verification; mechanical projections extended to package/result_set/view_set/
ledger-basis/completeness-basis SHAs, emitted only on actual differ (derived
set, never count-only). Unaffected comparison keeps the total>0 guard (empty
package already refused upstream) while allowing zero unaffected rows.

B6 — four-ref contract narrowed + FULL where authority is taken.
`_load_typed_four_refs` docstring now states the narrow contract explicitly
(classification + file/sha + schema + digest equality + ledger shape/basis-key
+ completeness shape/obligation shapes; NOT ledger-vs-discovery linkage, basis
vs live files, or closure/provenance). New shared `_verify_adopted_graph_full`
(`:545ff`) runs the FULL graph: four-ref load + request load/validate +
root_records Discovery + FULL evidence/views/ledger/completeness validators +
ownEpoch pins (checkpoint contract/implementation vs STORED manifest
tool_pins — never current source, so checks stay valid after LIVE advances).
Wired into `check_supersession_record_from_paths` (replacing the partial
"FULL" label), HIGH `write_cleanup_completion` postread, and
`_verify_completion_full` (hence `require_completion_consistent`,
`require_research_operation_ready`, resume ALREADY_ACTIVE). `resolve_research_authority`
stays classification-grade for detached diagnosis (readback); mutating
producers and READY entries go through the FULL paths.

B7 — slot proof, no False constants (HIGH `_prove_before_graph_unbound`
`:346ff`, `_prove_slot_not_human_presented` `:401ff`, wired into prepare
before any COPY). For every retained slot: downstream machine_checkpoints
pending + provenance None (unaccepted), both Human gates pending + provenances
null, no approval files under source_root gates paths, review-index absent or
schema-valid with no APPROVED decision and no record referencing the slot path
or slot SHA (presented-request check). `accepted_bound`/`gate_bound` False is
now the PROVEN outcome of these checks — any bound evidence refuses before
the COPY. Manifest `retention_snapshots` and `retention/inventory.json` carry
the identical 13-key rows (inodes/byte_count added to inventory); adopt/resume/
completion paths enforce exact per-slot equality between them.

B7b — idempotent completion timestamp. `write_cleanup_completion` compares
semantic intent excluding `recorded_at`: identical intent reuses the existing
receipt WITHOUT rewrite (returns idempotent True, bytes verified unchanged);
differing intent refuses (no overwrite). Covered by
`test_completion_idempotent_reuse` (bytes identical pre/post, idempotent True).

## 3. Public API stability (B/C coordination)

No public signature changed. LOW: `load_typed_checkpoint_record`,
`resolve_research_authority` (+`artifact_refs`), `check_supersession_record_from_paths`
(REQUIRED 4-path form), `require_research_operation_ready`,
`require_no_active_guard`, `require_completion_consistent`,
`guard_path_for`, `lstat_slot`, builders/provers — all same shapes; added
`artifact_refs` already in A2. HIGH: `prepare/adopt/resume/readback_revision`,
`verify_live_eligibility`, `claim_guard`, `write_checkpoint_as_planned`,
`replace_state_triplet`, `clear_remaining_exact_slots`,
`write_cleanup_completion`, `release_guard`, `resume_bound_attempt` — same
shapes; `reason`/`from_state`/`to_state` (never `reason_class`/`from`/`to`).
New A-owned leaf helpers in `survey_evidence_v2` are additive only.
C2 removing READY from its diagnostic Gate needs no A change (LOW readiness
entry unchanged). B's 3 new tests using real A helpers run against these
stable signatures.

PRECISE CROSS-OWNER NEED (blocks repeat correction; A does not work around
it): B's agent PREARCH branch (`_validate_checkpoint_record` PREARCH dispatch
and `_validate_core_stage_report` PREARCH branch in
`scripts/survey_agent_control_v2.py`) demands review `result` to be exactly
`{path, sha256}`, but the SELECTED checkpoint schema requires
reviews[].result to be a SizedRef `{path, sha256, byte_count}`. A writes
schema-conformant records, so `agent.validate_agent_state` on an adopted
PREARCH state fails with "requires deterministic result authority" (pinned by
new `test_repeat_correction_blocked_on_result_authority_shape`: rev2 prepare
on adopted EVIDENCE_REVIEWED+PREARCH state refuses there, guard absent, zero
writes). Request to Astra/B: accept SizedRef review results in both PREARCH
branches (subset check on path+sha256, mirroring the report-ref discipline),
which unblocks the required repeated-correction witness. A-lineage logic for
repeat (parent = previous record, original_anchor carried, supersedes appends)
is implemented in adopt (`:1131ff` HIGH) and executes once B accepts the shape.

## 4. Actual checks performed (static + REAL private-copy execution)

- Static: `ast.parse` OK for LOW (2300+ lines), HIGH (1400+ lines),
  evidence additions, tests. No `run_evidence_v2_interactive` import in LOW
  or A tests (docstring mention only). No `if False`, no `task-placeholder`,
  no `hashlib.sha256(b"…")` fabricated constants (only the `b"dm022-nonce:"`
  deterministic guard-nonce derivation, per map). No `reason_class` in A scope.
  Every public positive codepath calls a FULL validator (audit: LOW builders/
  prove/check/completion/readiness + HIGH prepare/adopt/steps/resume all call
  `validate_instance`/`_validate_*`/`_check_*`/`validate_evidence_card`/
  `validate_edition_view`/digest recomputes; `require_no_active_guard` is a
  passive lstat oracle; `resume_revision` dispatches to audited
  `resume_bound_attempt`; readback resolves via `low.resolve_research_authority`
  and never calls READY).
- REAL execution (fresh private copy `/tmp/dm022-a3-fresh` = R2 snapshot 756
  files + ONLY the 4 A3-modified files overlaid; schemas byte-identical;
  Python 3.14.4, jsonschema==4.23.0, pypdf==6.16.2; fixture Git DBs are
  independent temp dirs, inert example.invalid origin, process-scoped identity;
  no reconstruct objects, no old-runner reuse, no shared-candidate tests):
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
  tests.test_dm022_prearchitecture_acceptance_v2 -v` → **19/19 PASS, exit 0,
  17.7s**. Scope: WEEKLY + THEMATIC full prepare→adopt→resume→readback (incl.
  per-file manifest refs, FULL adopted-graph validation, checker, resolver
  with artifact_refs, CLI prepare), LOW loader dispatch, LOW guard/slots, plus
  14 fault tests: Raw-binding refusal; late final plant + bounded resume to
  RESUME_ADOPTED; completion tamper ×3 (checkpoint sha, seven-plan, expected_after)
  + resume INDETERMINATE; absent-slot regeneration + READY + readback; blocked
  repeat pin; stale HEAD/decision/unsupported profile/named-obligation gap (+
  named-obligation positive); interrupted-clear resume to RESUME_CLEARED;
  unknown-state resume INDETERMINATE; slot ownership (unreadable fail-closed,
  same-byte new-inode refusal + honest resume); State-tmp plant refusal +
  recovery; completion idempotent reuse; unreadable-path fail-closed.
  Raw: `evidence/A3-correction-20261028T134500Z/dm022-a3-test-raw-20261028.txt`
  (37 lines, 3997B, SHA256 `abb66f3d…`, exit 0). Manifest:
  `private-source-manifest.json` (756 files, SHA256 `b73c4d93…`). Binding:
  `a3-binding.json` + `a3-raw-binding.md` in the same packet dir.

## 5. Precise map notes / residual (HONEST, no broadening)

- A3 closes B1–B8 code findings in A scope as far as A-owned files reach. The
  B result-authority shape need above is the one public-positive path A cannot
  close without B (repeat prepare on adopted PREARCH state). Everything else
  A-claimed here executed green on the frozen R2+A3 private copy.
- Integration witnesses on the frozen all-owner snapshot (both-route
  positive/negative/later-lifecycle incl. G71→G76 control, G76→initial→
  editorial/renewal, genuine forwarded-State readback via B/C forward writers,
  affected regressions, B/C suites) remain for root after all authors return,
  plus independent implementation review. Whole NOT_READY/step4B3 OPEN/audit
  unstarted/DM021+022 OPEN preserved except pre-code gate; Profile/quality/
  adoption/savings OPEN. No implementation acceptance claimed; no Production
  semantic claim. Stop at Human Commit Point; ordinary Commit/Push Human-owned.
