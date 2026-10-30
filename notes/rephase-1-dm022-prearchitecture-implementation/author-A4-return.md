# Owner-A4 implementation return — DM022 pre-Architecture research operation (CORRECTION)

2026-10-28. Owner A4 (correction implementer; A2 rejected, A3 partially reviewed).
Binding: contract a345bb95 INCLUDING §11, pre-code assessment §5, precode packet
README, mandatory astra-precode-gate-resolution INCLUDING §5 (FULL 0425c530/13788B),
independent readiness §§8–9, R3 (overridden by) R4 + literal 5 schemas, R5 families,
R6 roles, ROOT, R2 independent review §§B1–B8, R2 integration diagnostics, A3
independent review (B1–B8 findings), and **astra-a3-integration-resolution.md
(BINDING)**. R2 snapshot preserves A2; R1 preserved. Human continuation authorized
ACTUAL CODE in independent candidate-work ONLY. No ordinary candidate/reconstruct
Commit/Push; no fixtures in reconstruct; no git config/global writes; no
network/Production/reset/clean/old-log overwrites. Python 3.14.4 + unittest +
jsonschema 4.23.0/pypdf 6.16.2. Whole unit continues — NO Commit Point claimed here.

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all paths below relative to it). Started from R2 (actual409/tree8ce +93);
candidate-work was idle except A edits during this unit (B/C had returned; B's
SizedRef correction + C work present as idle current source). No ordinary source
commit. Prior returns (`author-A/B/C-return.md`, corrections, `author-A2-return.md`,
`author-A3-return.md`) preserved and unchanged.

## 1. Exact written paths (Owner A ONLY, disjoint from B/C1/C2)

CHANGED (A4 correction; schemas untouched, byte-identical R2 == candidate):

- `scripts/survey_research_authority_v2.py` (LOW) — 148801B
- `scripts/survey_prearchitecture_acceptance_v2.py` (HIGH) — 87249B (A3) + B7 slot-proof + idempotence + resume ordering (this unit; re-measured in §4)
- `scripts/survey_evidence_v2.py` (A-owned leaf) — ADDITIVE ONLY: detached
  record/card/view pure builders; zero behavior change to existing validators,
  producers, writers, schemas
- `tests/test_dm022_prearchitecture_acceptance_v2.py` (Owner-A unittest, no
  pytest) — 19 tests (5 carried positives + 14 fault/negative/later-seam tests)
- `tests/dm022_prearchitecture_fixtures_v2.py` — UNCHANGED

NOT touched: B (incl `run_evidence_v2_interactive.py`, agent/consumers), C1
(closures/families/config), C2 (publication/editorial/retention), all five
`schemas/dm022-*.schema.json`, shared fixture helpers. No new runtime modules,
no new schema files, no closure broadening. No B-file edits (B's SizedRef fix
was already landed by B; A only exercises it read-only).

## 2. What A4 closed vs astra-a3-integration-resolution BINDING (§§1–3)

**§1 — SizedRef is selected: repeat now succeeds; malformed ref refused.**
B corrected both PREARCH branches to exact 3-field SizedRef in current source
(A verified, did not edit B). A removed the A3 known-repeat-blocker pin and
replaced it with a REAL positive repeat on BOTH routes plus a genuine
malformed-SizedRef negative: `test_repeat_correction_preserves_original_anchor_both_routes`
adopts rev1 then rev2 and asserts parent ref == rev1 checkpoint FILE bytes,
`original_anchor` carried, rev1 appended to `supersedes`, resolver + checker
pass on the second-generation record; `test_malformed_review_result_refuses`
proves a tampered review result is refused by SELF digest. A never writes
schema-violating records to satisfy any checker.

**§2 — public resolve runs FULL validation at the SAME selected checkpoint.**
`resolve_research_authority(repo_root, state_path)` (`survey_research_authority_v2.py:1021`)
now: structural peek → classification → FULL adopted-graph validation at the
selected path+sha (`_verify_adopted_graph_full`, `:760`) → report/proof/
decision/retention actual reloads with crossbinds → retained-COPY binding →
final pin recheck (State file + checkpoint FILE re-read; refuse on any drift —
never a different selection observed after an earlier READY call). Returns data
only after the FULL phase passes. Private `_load_typed_four_refs` (`:396`) stays
a NARROW internal classification phase with the narrowed contract stated in its
docstring; every public authority result (resolve, check, completion, cleanup
postread, resume ALREADY_ACTIVE) passes the FULL phase first. Acyclic call graph
(check → FULL, never check → resolve → check). No caller verified dicts, no
current State validation, no operational guard in detached validation.

**§3 — own-epoch proof against recorded-commit git objects (not stored-claim
equality).** New `_verify_own_epoch_commit` (`:597`, called from
`_verify_adopted_graph_full`): verifies the recorded commit exists; the manifest
tool_pins path set equals EXACTLY the mapped DM022 finite code set (2 modules +
5 schemas, `:546`; no caller-arbitrary list, no silent broadening — a future map
change returns to Astra); every pinned path is a 100644 blob in that commit whose
bytes hash to the pinned SHA (single batched `git cat-file --batch` read);
schemas carry the selected `$id`s; Contract8 recomputed byte-for-byte from the
COMMIT's config/files (mirrors `core.contract_identity`/`aggregate_file_hash`
exactly, profile names from the COMMIT's profile bytes) and required to equal
BOTH the checkpoint contract and the stored manifest pins. Historical reads never
substitute LIVE tools, never demand HEAD equal the recorded epoch, never recurse
into current State. Read-only `git -C` subprocess calls with scrubbed
GIT_* env (`_git_read`, `:569`); no network fetch ever; missing objects refuse.
Uses only stdlib + already-closed core/schema_gate — no unmapped dependency, so
no return-to-Astra needed for imports. Stored cross-claim equality is kept as
well (binds record↔manifest), with the git-object proof on top.

(§4 ordinary writers/Gate wiring is C-owned; no A action. C2 removed READY from
its diagnostic Gate and kept writers; B added 3 tests using real A helpers —
stable A signatures below; C1 11 pass scoped. A confirms its public signatures
are unchanged: LOW `load_typed_checkpoint_record`,
`resolve_research_authority`, `check_supersession_record_from_paths` (REQUIRED
4-path form), `require_research_operation_ready`, `require_no_active_guard`,
`require_completion_consistent`, `guard_path_for`, `lstat_slot`, builders/provers;
HIGH `prepare/adopt/resume/readback_revision`, `verify_live_eligibility`,
`claim_guard`, `write_checkpoint_as_planned`, `replace_state_triplet`,
`clear_remaining_exact_slots`, `write_cleanup_completion`, `release_guard`;
`reason`/`from_state`/`to_state` throughout, never `reason_class`.)

R2-review leftovers closed in A scope along the way: B1 atomic link-claim finals
with preserved partials (`HIGH:_exclusive_write_bytes`, `:69`; State switch stays
the sole inode-pinned replace path); B2 runner import removed from LOW and tests
(pure `validate_research_record_content` / `build_research_card_content` /
`build_research_view_content` in A-owned evidence module); B3 FULL completion
(EXACT `report.$defs/completionReceipt` schema via `_validate_against_report_def`,
`:190`; COPY-recomputed expected_after; triplet+FULL revalidation, not trusted
booleans) in `require_completion_consistent`, `require_research_operation_ready`,
resume and cleanup postread via `_verify_completion_full` (`:675`); B4
regeneration tolerance (old-absent slots and regenerated new-content/same-byte
new-inode outputs never block; only same-inode stale refuses); B5 FULL NEW-graph
validators + Raw claim-content binding + per-file manifest/proof refs +
full mechanical set in `prove_revision_from_paths` (`:1916`) and HIGH manifest
(`candidate_outputs.tasks/cards/views` now bound, non-empty enforced); B6 narrow
four-ref contract + FULL in check/cleanup/require paths + ownEpoch pins; B7 slot
unaccepted/Human-unbound proof (`HIGH:_prove_before_graph_unbound`, `:346`,
`_prove_slot_not_human_presented`, `:401`; no False constants) with manifest↔
inventory exact 7-row bind in adopt/resume/completion/check; B7b idempotent
completion (semantic compare excluding `recorded_at`, never rewrite).

## 3. Actual checks performed (static + REAL private-copy execution)

- Static: `ast.parse` OK for LOW/HIGH/evidence/tests. No `run_evidence_v2_interactive`
  imports in LOW or A tests (docstring mentions only). No `if False`, no
  `task-placeholder`, no fabricated digests (`sha256(b"…")` only in the
  deterministic guard-nonce derivation), no `reason_class`, no invented
  `overall_status COMPLETE`. Every public positive codepath calls a FULL
  validator; `require_no_active_guard` is a passive lstat oracle;
  `resume_revision` dispatches to audited `resume_bound_attempt`; readback never
  calls READY.
- REAL execution (fresh private copy `/tmp/dm022-a4-private` = FULL current
  idle candidate-work incl B fix, minus `.git`; 756 intended files; Python 3.14.4,
  jsonschema==4.23.0, pypdf==6.16.2; fixture Git DBs independent temp dirs, inert
  example.invalid origin, process-scoped identity; no reconstruct objects, no
  saved runners, no shared-candidate tests):
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
  tests.test_dm022_prearchitecture_acceptance_v2 -v` → **19/19 PASS, exit 0,
  ~21s**. Scope: WEEKLY + THEMATIC full prepare→adopt→resume→readback (incl
  per-file refs, FULL adopted-graph incl recorded-commit own-epoch proof,
  checker, resolver, CLI prepare), LOW loader dispatch, LOW guard/slots, plus
  14 fault tests: Raw claim binding refusal; late final plant + bounded resume
  to RESUME_ADOPTED; 3× completion tamper + resume INDETERMINATE; absent-slot
  regeneration + READY + readback; positive repeat both routes + malformed-result
  refusal; stale HEAD/decision/unsupported profile/named gap(+positive);
  interrupted clear + RESUME_CLEARED; unknown-state resume INDETERMINATE; slot
  ownership ×2 (unreadable fail-closed, same-byte new-inode refusal + honest
  resume); State-tmp plant refusal + recovery; completion idempotent reuse;
  unreadable-path fail-closed. Raw: `evidence/A4-correction-20261028T140520Z/
  dm022-a4-test-raw-20261028.txt` (37 lines, 3984B, SHA256 `61939974…`, exit 0).
  Manifest: `private-source-manifest.json` (756 files, SHA256 `14ef836d…`).
  Binding: `a-binding.json` + `a4-raw-binding.md` in the same packet dir.
  This is real full scope for A, not an A1/A2 closure-readiness claim.

## 4. Precise residual / honest non-scope (no broadening)

- A3's audit items are closed in A scope as far as A-owned files reach. The one
  A3-flagged cross-owner need (B SizedRef result shape) is RESOLVED by B in
  current source; the previously pinned blocker test is replaced by the real
  positive repeat above.
- Remaining for root after ALL authors: frozen all-owner integration snapshot,
  full Weekly/Thematic correction + repeat + normal regeneration/Architecture/
  Draft/publication + later editorial/renewal, exact G71→G76 unchanged-upstream
  compatibility control, failure/resume seams, affected regressions, B/C suites,
  and independent implementation review. Whole NOT_READY/step4B3 OPEN/audit
  unstarted/DM021+022 OPEN preserved except pre-code gate; Profile/quality/
  adoption/savings OPEN. No implementation acceptance claimed; no Production
  semantic claim. Ordinary Commit/Push Human-owned. Unit continues (no Commit
  Point).
