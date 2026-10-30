# Independent early blocking source review — DM022 R2 (A-scope: LOW/HIGH + 5 schemas + A helpers)

Fresh independent source reviewer, NOT author, NOT final audit. Early blocking review only.

Date: 2026-10-28. Binding order: contract `a345bb95` INCLUDING §11, pre-code assessment §5,
precode ROOT FULL `0425c530` /13788B INCLUDING §5, independent readiness §§8–9 FINAL-BINDING,
then R3 (overridden by) R4 + literal 5 schemas, R5 families, R6 roles, then ROOT.
R1 rejection `astra-r1-source-review.md` §§A1–A7 + cross-owner B/C1/C2 preserved, not overwritten.
Author claims read: `author-A2-return.md`, `author-B-return.md`, `author-C1-return.md`,
`author-C2-return.md` + `author-C2-correction.md`, coordination disjoint ownership.

Fixed scope reviewed (READ-ONLY, no execution, no fixtures, no network, no Git mutation,
no Human commit readback, no candidate edits):

- `.../.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/snapshot-r2-20261028T124706Z/worktree`
  (756 intended files, manifest `notes/rephase-1-dm022-prearchitecture-implementation/evidence/source-r2-20261028T124706Z/snapshot-r2-manifest.json`
  SHA256 `53fde56bea8b69adeb2cdfbbd716bbe9534bfb0bc49739619f909ae6ca1f3935` /149982B).
- A-scope ONLY in this review:
  `scripts/survey_research_authority_v2.py` (LOW, 1945 lines),
  `scripts/survey_prearchitecture_acceptance_v2.py` (HIGH, 1284 lines),
  `schemas/dm022-*.schema.json` (5 installed),
  `tests/dm022_prearchitecture_fixtures_v2.py` (78 lines),
  `tests/test_dm022_prearchitecture_acceptance_v2.py` (573 lines).
- Candidate may C2-edit `candidate-work` after this freeze; this review binds ONLY the R2 worktree above.
  A2 private raw `evidence/A2-original-20261028T124706Z/` is R1 worktree + only-A2 overlay, NOT R2 proof
  (see §7). B/C1/C2 files NOT re-reviewed here except for closure/API boundary cited below.

Method: static read of R2 worktree bytes + line refs. No `python -m unittest/pytest`, no imports,
no fixture builds, no `git status/log/show/rev-parse` in workspace root. `grep`/`python3 -c` used
only to list line numbers and print file headers already read via Read — no semantic execution.

Verdict: **NOT_READY — blocking. Do NOT claim completion, do NOT proceed to closeout.
Return to Astra before broadening. Minimum coherent fixes in §8 required, then frozen
re-snapshot + full both-route/negative/later-lifecycle witnesses + affected regressions
+ independent implementation review.**

Root's preserved R2 observations confirmed and made precise below (B1–B4). Additional
material blockers B5–B8 found from actual code vs map (not keyword-only).

---

## 1. B1 [BLOCKING] HIGH `_exclusive_write_bytes` still check-then-replace races final target

Location (R2 worktree):

- `scripts/survey_prearchitecture_acceptance_v2.py:66-157` (`_exclusive_write_bytes`),
  esp. `:76` pre-check `if _lstat_single(path) is not None: refuse`,
  `:133-140` second `lstat` then `os.replace(tmp, path)`.
- Same pattern via `scripts/survey_prearchitecture_acceptance_v2.py:193-217`
  (`_copy_regular_exclusive` → `_exclusive_write_bytes` for dst).

What code does:

1. `lstat` final; refuse if present.
2. `os.open(tmp, O_CREAT|O_EXCL|O_WRONLY)` exclusive temp + short-write loop + `fsync` + checked close + re-read + `lstat` temp.
3. Re-`lstat` final; if present unlink tmp and refuse; else `os.replace(tmp, path)` + dir `fsync` + postread.

Why blocking vs map:

- Contract §6 + §11.3 + ROOT §2: immutable R/guard/checkpoint/completion artifacts must never be
  overwritten; State triplet switch is the ONLY replace-over-existing path (single-writer/held-descriptor,
  known-byte, inode-pinned). `os.replace` over an existing final is an overwrite, not an exclusive claim.
- Step 3 is TOCTOU: exclusive temp creation does NOT make the final destination exclusive. Between `:133`
  `lstat` and `:139` `os.replace`, a concurrent writer can create the final; `replace` then silently
  overwrites it. The second check narrows but does not close the race. For crash/ownership faults
  (§7 table: write/short-write/fsync/close/replace/postread/guard failure) the required oracle is
  atomic exclusive final creation (e.g. `link(tmp, final)` which fails with `EEXIST`, or
  `open(final, O_CREAT|O_EXCL)` + copy, never `replace` onto a possibly-present final).
- A2-return §2 claim “refuses if the final target already exists (no `os.replace` overwrite)” is not
  matched: `os.replace` IS used on the final (`:139`), and the refuse is advisory (two `lstat`s), not atomic.

Minimum fix:

- For all immutable R/guard/checkpoint/completion/slot-COPY finals: replace `os.replace(tmp, path)` with
  an atomic exclusive final claim — e.g. `os.link(tmp, path)` (fails `EEXIST` if present) then `unlink(tmp)`,
  or `os.open(path, O_CREAT|O_EXCL|O_WRONLY)` + copy + `fsync` + checked close + dir `fsync` + postread.
  Never `replace` onto a possibly-present immutable final. Keep `replace` ONLY in
  `replace_state_triplet:739-783` (already inode-pinned known-byte switch with before/recheck/postread).
- Apply same to `_copy_regular_exclusive:193-217` dst path. Preserve short-write/`fsync`/checked-close/dir-`fsync`/postread.
- Add explicit late-seam test: final appears between temp-write and final-claim must refuse with no overwrite
  (requires frozen-snapshot execution, not this static review).

## 2. B2 [BLOCKING] LOW function-local `run_evidence_v2_interactive` import broadens required closure + pulls agent + circular

Locations (R2 worktree LOW):

- `scripts/survey_research_authority_v2.py:577` (`derive_before_context`: `from scripts import run_evidence_v2_interactive as interactive`),
- `:706-708` (`build_revision_package_from_paths`: interactive + evidence + screening),
- `:847-848` (`build_revision_cards_views_from_paths`: interactive + evidence),
- calls at `:624` (`interactive._validate_record`), `:759` (same), `:882` (`interactive._build_card`),
  `:904` (`interactive._build_view`).

Widened closure root (R2 worktree, read for boundary only):

- `scripts/run_evidence_v2_interactive.py:26-32` top-level imports `survey_agent_control_v2 as agent`,
  `survey_agent_tool_v2 as agent_tool`, `survey_completeness_v2`, `survey_discovery_v2`,
  `survey_evidence_v2`, `survey_research_authority_v2 as low` (circular), `survey_schema_v2`, `survey_screening_v2`.

Why blocking vs map:

- LOW docstring `:21-29` claims “Top-level imports (exact, B1 leaf rule): ONLY core shape-only symbols
  … Every evidence/screening/completeness/discovery/interactive access is function-local and calls ONLY
  the real pure content cores with exact signatures. No agent … at top level or inside LOW bodies.
  LOW never validates State.” Function-local `import run_evidence_v2_interactive` violates the second
  sentence: at import time Python executes the runner’s top-level imports, pulling `agent`,
  `agent_tool`, `discovery`, and `low` itself (circular LOW→interactive→LOW). This is the exact
  “runner-level imports widen the detached closure beyond the mapped pure cores” noted in the R2
  preservation record.
- Pre-code map (ROOT §3 + R4/R6 + dependency-closure): G76 delta is ONLY 2 modules + 5 schemas;
  receipt closure G76 70 (63+2+5), staged 70, canon 36/41. Runner `run_evidence_v2_interactive` is NOT
  in the mapped LOW closure; C1 explicitly keeps lazy P2V function-local in materialize and never in
  verifier closure. LOW must call S1.1 leaf `_content` cores (`survey_evidence_v2`, `survey_screening_v2`,
  `survey_completeness_v2`) with exact signatures, extracting pure portions narrowly if needed, preserving
  old wrappers — not the interactive runner’s `_validate_record/_build_card/_build_view` which carry
  runner/State/agent authority.
- A2-return §2 “function-local calls to their exact `_content` cores” is not matched for these three
  functions: they call the runner, not the leaf `_content` cores.

Minimum fix:

- Remove all `from scripts import run_evidence_v2_interactive` from LOW. Replace:
  `_validate_record` → real `survey_evidence_v2`/`survey_screening_v2` record/content validators with exact
  signatures (or narrowly extracted pure helper moved to leaf, old runner wrapper preserved);
  `_build_card/_build_view` → pure leaf builders or narrowly extracted pure portions (no runner State/agent).
  Keep `survey_completeness_v2/survey_evidence_v2/survey_screening_v2` function-local leaf imports
  (`:365-366`, `:939`, `:1052-1053`, `:1169-1170`, `:1350-1352` are the allowed pattern).
- Verify closure member-wise (not counts): G76 70 + staged/canonical sets contain ONLY mapped files;
  `run_evidence_v2_interactive`, `agent`, `agent_tool`, `discovery` must not be reachable from LOW.
  Circular `low` import from runner must not be loadable via LOW.

## 3. B3 [BLOCKING] `require_completion_consistent` checks booleans/keys only — no schema/COPY/expected-after/slot verification despite docstring

Location: `scripts/survey_research_authority_v2.py:1788-1842`.

What code does (`:1817-1842`):

- Shape-checks `checkpoint_ref` ArtifactRef, discovers repo root, reloads checkpoint FILE + SHA + `is_prearchitecture_record`,
  derives `completion_rel`, loads completion JSON.
- Requires exact keys (`schema_version,issue_id,revision_id,attempt_nonce,checkpoint,expected_after_state,seven_plan,postread,recorded_at,executor`),
  `schema_version=="1.0"`, `checkpoint.sha==checkpoint_ref.sha`, `postread.triplet_match is True`,
  `postread.artifacts_rehashed is True`, `seven_plan` 7 rows with known slots + `cleared/absent_legitimate`.
- STOPS. No `schema_gate.validate_instance` against completion receipt schema, no COPY-derived
  `expected_after` recomputation, no `seven_plan` vs slot `lstat`/retention-inventory inode check,
  no LIVE postread triplet + 4 live re-hashes.

Docstring claim (`:1788-1798`): “Completion validates the FULL receipt schema/inventory/COPY-derived
expected_after cross-binding (no trusted booleans, no same-byte new-slot confusion …)” — not implemented.
`triplet_match/artifacts_rehashed is True` ARE trusted booleans here.

Why blocking:

- Contract §6–§7 + ROOT §2: completion receipt must bind checkpoint + COPY-derived expected State;
  guard loss cannot grant permission; `postread.triplet_match/artifacts_rehashed` must be recomputed
  (re-resolve State triplet same-record + reload 4 refs with live re-hash + FULL content checks), not trusted.
- HIGH `write_cleanup_completion:834-883` DOES recompute COPY-derived expected (`:849-854`), LIVE postread
  (`:856-864`), `require_same_triplet` + `_load_typed_four_refs` (`:861-865`) before writing receipt.
  LOW’s passive verifier must mirror that verification on read; otherwise `resume_bound_attempt:1186`
  (`low.require_completion_consistent` for E + guard-absent → `ALREADY_ACTIVE`) grants `ALREADY_ACTIVE`
  on boolean-only receipt, and B/C2 ordinary `READY` entries calling this R4-signature API pass without
  real verification.
- `require_research_operation_ready:1844-1945` DOES do fuller checks (checkpoint SHA, completion SHA,
  postread booleans + per-slot `lstat` + retention-inventory inode for same-byte regeneration `:1927-1944`).
  The two APIs diverge: R4-signature `require_completion_consistent(source_root, checkpoint_ref)` (no repo_root)
  is the weak one actually wired to B/C callers per coordination.

Minimum fix:

- Make `require_completion_consistent` perform the same FULL verification as `require_research_operation_ready`
  + `write_cleanup_completion`: `validate_instance` completion receipt (report schema `$defs/completionReceipt`
  or standalone receipt schema), recompute `expected_after` from retained COPY + checkpoint ref and compare
  to `completion.expected_after_state.sha`, reload LIVE State (discovered repo root + canonical State path),
  enforce `require_same_triplet` + `_load_typed_four_refs` FULL (or at least digest + obligation shapes —
  see B6), enforce `seven_plan` 7 rows vs `retention/inventory.json` inodes + current slot `lstat`
  (same stale-vs-regenerated rule as B4, fail-closed when inventory missing).
- Do NOT trust `postread.triplet_match/artifacts_rehashed`; recompute. Document `R4 signature (no repo_root)`
  discovery (`_discover_repo_root_from_source_root:1770-1785`) as location-only, never content authority.

## 4. B4 [BLOCKING] `require_research_operation_ready` rejects legitimate regeneration when old slot was absent

Location: `scripts/survey_research_authority_v2.py:1844-1945`, esp. `:1909-1918`:

```python
for row in seven_plan:
    ...
    obs = lstat_slot(source_root, slot)
    if not obs["present"]:
        continue
    copy_sha = row.get("copy_sha")
    if copy_sha is None:
        raise ResearchAuthorityError(f"DM022_TRANSITION_ACTIVE: foreign file at never-present slot: {slot}")
```

Plus `:1919-1945` same-byte path consults retention inventory inodes, but absent-plan path above has no
regeneration allowance.

Why blocking:

- Contract §6: “Missing output files do not themselves block the normal generator: they are usual precondition.”
  ROOT §2: “The later completion receipt … does not require regenerated slots to remain absent.”
  ROOT §5.2 + §11.1: all seven old slots retained/cleared, then ordinary seven-slot regeneration without
  audit overwrite; normal forward Architecture/Draft/publication consumers must work after valid upstream correction.
- After completion + guard release, the normal Selection runner regenerates all seven slots (including ones
  legitimately absent before). At next `READY` entry (entry+prepublish per B/C wiring), guard is absent but
  completion verifies; the loop above sees a present file at a `copy_sha is None` (planned-absent) slot and
  refuses `DM022_TRANSITION_ACTIVE: foreign file`. Legitimate post-completion regeneration is thus refused
  as stale/foreign. The code’s own comment `:1927-1930` acknowledges inventory inodes distinguish stale
  (same inode) vs regenerated (new inode) for present-plan rows, but the absent-plan branch unconditionally refuses.
- This is the exact “readiness rejects normal regenerated slot when old was absent (lines 1917)” preserved
  in the R2 snapshot record. A2-return §2 claim “regenerated same-byte new-inode files allowed via
  retention-inventory inode comparison” holds ONLY for present-plan rows (`:1939-1944`), NOT for absent-plan rows.

Minimum fix:

- Distinguish guard-held vs guard-absent+completion-verified contexts. When guard absent AND completion
  receipt FULL-verifies (B3-fixed) AND retention inventory shows the slot as `present: false` (planned absent),
  a present file must NOT auto-refuse: allow if it is a legitimate normal-producer output under the NEW
  authority (new inode vs absent, or content valid under new research refs), or at minimum do NOT block
  `READY` on this slot alone — record `regenerated_legitimate` and let stage validators enforce content.
  Only refuse when guard is held (transition window) or inventory shows planned-present with same-inode stale
  bytes (`:1939-1945` rule) or present file is nonregular/unreadable.
- Add frozen-snapshot witness: absent-plan slot → adopt → release → normal regeneration → `READY` must pass;
  guard-held foreign plant must still refuse. Neither is proved by current A 5/5 (see §7).

## 5. B5 [BLOCKING] Deterministic proof + manifest do not bind full new graph, Raw semantics, or per-file outputs

Locations:

- LOW `prove_revision_from_paths:1335-1611`.
- HIGH `prepare_revision:614-670` manifest construction, esp. `:636-644` `candidate_outputs: {package, tasks: [], cards: [], views: [], ...}`.
- Schemas: `dm022-revision-proof-v2.schema.json:39` (`rows_checked minimum 0`), `:20-31` (proposed tasks/cards/views no `minItems`);
  `dm022-revision-manifest-v2.schema.json:39-42` (tasks/cards/views no `minItems`).

What code does / omits:

- (a) NEW graph FULL validation missing: `:1435-1447` recomputes evidence/views digests only; ledger check
  `:1533-1559` enforces Discovery identity + affected-row immutable fields + unaffected-row equality + 4 ledger-basis
  SHA mechanical projections, but NEVER calls real `_check_ledger_rows_content` or
  `_check_completeness_result_content`/`_validate_obligation_shape`/`_thematic_closure_errors` on the NEW
  ledger/completeness. Comment `:1448` admits “needs profile/discovery/screening paths … Use request refs”
  but code does not. Build-time validation (`build_versioned_ledger/completeness`) is trusted; proof (the
  deterministic binding before adoption) does not re-validate proposed bytes.
- (b) Raw/event semantics not bound: `:1379-1382` verifies each `decision.raw_refs[]` SizedRef SHA/bytes only.
  `decision.assessment.{interpretation,event_semantics,provenance_check}` (request schema `$defs/suppliedDecision:346-354`)
  are free text never checked against Raw bytes or card `source_records/verification_targets/claims`. Contract §4
  requires “newly retained Raw and source/event/clock semantics” + “new official article must have actual
  preserved bytes/provenance, not a Summary quotation.” Current proof would PASS a fabricated new card with
  same Raw SHA but invented event semantics.
- (c) Per-file outputs unbound: HIGH manifest leaves `tasks/cards/views` empty arrays (`:638-640`) though files
  ARE written (`:493-540`). Proof `proposed.{package,tasks,cards,views,...}` (`:1580-1591`) thus binds only
  package + acceptances + ledger + completeness, not individual task/card/view SHAs. Schema permits empty
  (no `minItems`), so schema PASS hides the gap. Contract §4 + §10 + ROOT §5.2 require exact-target reuse vs
  new-build binding, full affected/unaffected semantics, and complete path set for HEAD/tree predicate —
  every mechanical acceptance/file SHA change must be explicitly mapped, not directory-prefix excluded.
  Proof’s `mechanical` (`:1551-1559`) covers only 4 ledger-basis SHAs.

Minimum fix:

- In `prove_revision_from_paths`: after loading NEW 4, call FULL validators on proposed bytes —
  `evidence_mod._check_ledger_rows_content(...)`, `survey_completeness_v2._check_completeness_result_content(...)`
  + `_thematic_closure_errors` + `_validate_obligation_shape` for every NEW obligation (same strictness as
  `build_versioned_*`), not just digest/identity checks. Bind Raw: for each affected Discovery, require NEW
  card’s `source_records/verification_targets` to reference `decision.raw_refs` SHAs + `assessment.event_semantics`
  consistently (exact field map per R4, no invented linkage). Record explicit `mechanical_projections` for ALL
  propagated SHAs (package/tasks/cards/views/acceptances/ledger/completeness basis), no prefix exclusion.
- In HIGH `prepare_revision`: populate `manifest.candidate_outputs.{tasks,cards,views}` with per-file SizedRefs
  (path+SHA+bytes for every task/card/view written), and mirror them in proof `proposed`. Tighten schemas
  or code-enforce `minItems 1` / non-empty (schema currently allows empty; code must refuse empty when tasks exist).
  Keep `rows_checked>0` code refusal (`:1560-1561` good) but raise schema `minimum` to 1 to prevent schema-only PASS.

## 6. B6 [BLOCKING] `_load_typed_four_refs` partial vs claimed FULL — unsafe as standalone acceptance authority

Location: `scripts/survey_research_authority_v2.py:353-495`, docstring `:353-364` claims
“loads each named artifact … with FULL content checks via real S1.1 leaf cores.”

What code does (`:401-493`):

- Live re-hash + schema `validate_instance` per artifact (good), per-card/view digest recompute (`:452-464`),
  ledger shape + basis-key set + evidence/view digest equality (`:470-479`), completeness shape +
  `overall_status ∈ {READY,LIMITED,INCOMPLETE}` + per-row `_validate_obligation_shape` (`:481-493`).
- Explicitly DEFERS full ledger basis/row validation and full Discovery/Screening/basis validation
  (`:419-431` “without requiring canonical Discovery/Screening reload here. Full … validation is deferred
  to prove/check paths”, `:466-469` “full ledger basis validation is deferred”).

Why blocking:

- B/C ordinary consumers (`agent.resolve_active_research_four_refs`, `resolve_active_evidence_views`,
  publication/editorial/retention walkers per A2 §3 / B §1 / C2 §1) call this resolver as the active
  research authority post-adoption and in later lifecycle readback. If they rely on it alone, shape +
  digest-equality PASS is treated as full acceptance, while decision drift, task linkage, DROP vs non-DROP
  dispositions, rationale, and full completeness content (`_check_*_content`) are unchecked.
- `check_supersession_record_from_paths:1671-1683` calls this loader for “four-artifact FULL validation”
  but inherits the same partialness; error string claims FULL while code is partial.

Minimum fix (one of, no broadening):

- Either (preferred) make `_load_typed_four_refs` FULL: resolve profile/discovery/screening paths from
  checkpoint’s `request/manifest/retention` (available via `record.request/retention_plan` + repo files),
  then call `_check_ledger_rows_content` + `_check_completeness_result_content` + `_thematic_closure_errors`
  on the loaded 4 (same as build/prove), or
- Narrow the contract: document this function as classification + digest/shape only, and require ALL
  acceptance paths (HIGH adopt/resume/completion, B/C `READY`, `check_supersession_*`) to call
  `prove_revision_from_paths` or `check_supersession_record_from_paths` FULL (B5-fixed) — never this loader alone.
  Update A2 §3 “FULL content validators” claim accordingly and fix the `check_supersession` error label.

## 7. B7 [BLOCKING] HIGH slot retention copies without proving unaccepted / Human-unbound (fixed `accepted_bound/gate_bound` false)

Location: `scripts/survey_prearchitecture_acceptance_v2.py:454-488` (slot loop), manifest `:632-635`
+ retention inventory `:656-664`.

What code does:

- For each `low.SEVEN_SLOTS`: `lstat_slot`, refuse nonregular/refused, `present:false` → row with null SHAs,
  `present:true` → `_safe_read_bytes` + `_copy_regular_exclusive` + row with SHAs + inodes.
- Sets `accepted_bound: False, gate_bound: False` unconditionally (`:472,487`) without verification.

Why blocking vs contract §6 + §11.1 + ROOT §2:

- Preparation must “prove each [slot] is unaccepted, not a Human-reviewed/request-bound input, unchanged
  since capture, in the fixed invalidation plan” before retention/clearing. Unknown/foreign/changed files
  refuse; absent entries do not become deletion permissions. Current code proves only regular + readable +
  copied; it never checks State provenance/history shows Selection/Architecture/Draft/validation pending,
  no Human approval/provenance, no recorded review/index entry, no presented immutable request, no active
  Exception, and that the slot path is exactly the Profile-derived canonical path (it does derive
  `slot_rel` from `profile.paths.source_root` — good — but not the acceptance/binding check).
- `accepted_bound/gate_bound` are thus fabricated constants (same class as R1 `if False`/invented ledger
  rejected in `astra-r1-source-review.md` §A2), not observed predicates. A Human-bound audit file
  (`selection-architecture-audit.json` with `interactive_input` + 5 `outputs` refs per §11.1) present at
  prepare would be retained + later cleared without proving it is not a reviewed/bound result.

Minimum fix:

- Before COPY, for each present slot: load bytes + prove unaccepted (no accepted downstream provenance in
  LIVE State `checkpoint_provenance.selection/architecture/...` + `machine_checkpoints` pending),
  prove no Human binding (both gates pending + both provenances null + no approval files + no review-index
  entry referencing the slot SHA + no presented immutable request superseding), prove unchanged since capture
  (re-read + SHA stable), prove path in fixed 7-slot plan. Set `accepted_bound/gate_bound` from those checks
  (must remain false to proceed; true → refuse, not silent clear). Preserve `source_dev/source_ino` already captured.
- Bind manifest `retention_snapshots` (`:632-635`, 7 rows with inodes) exactly to retention `inventory.json`
  (`:656-664`); currently two representations with different key sets (`byte_count/source_dev/...` vs
  `accepted_bound/gate_bound` only) — make them consistent or document canonical.

## 8. B8 [BLOCKING] A 5/5 observation is R1+only-A2 private, NOT R2 proof; fault/lifecycle coverage absent

Preserved raw (read, not re-executed):

- `notes/rephase-1-dm022-prearchitecture-implementation/evidence/A2-original-20261028T124706Z/`
  (`a2-binding.json`, `a2-raw-binding.md`, `dm022-a2-test-raw-20261028.txt` SHA256
  `1ac355419351...`, exit 0, 11 lines) + `author-A2-return.md` §4.
- Private copy described as `snapshot-R1 worktree (756 files) + ONLY A2 4 files overlaid`, fresh independent
  fixture DBs, `python3 -m unittest tests.test_dm022_prearchitecture_acceptance_v2 -v` 5/5 PASS
  (Weekly full prepare→adopt→resume→readback, Thematic full, LOW loader dispatch, LOW guard/slots, HIGH CLI prepare).

Why NOT R2 proof (no new execution performed here; static scope analysis only):

- R2 worktree is the NEW complete integration snapshot (A2+B+C1+C2 bound, manifest `53fde56...`).
  A2 raw predates B/C1/C2 landing and does NOT contain their files; it cannot prove R2 integration,
  cross-owner API reconciliation (`author-A2-return.md` §3 REQUIRED B/C fixes), or absence of regressions.
  A2-return §4 itself scopes it as “NOT current R2/all fault coverage” + “integration awaits all authors
  after root freezes the snapshot.”
- 5 tests cover only happy-path Weekly/Thematic adopt + loader dispatch + guard/slot lstat + CLI `prepare`
  (`test_...:468-569`). Static read of `test_dm022_prearchitecture_acceptance_v2.py` shows NO:
  wrong-role PREARCH-at-publication refusal, split/mixed authority refusal, unsupported Profile type,
  missing named obligation, stale Raw/HEAD/controls/tool-pin drift, ownership/close/replace faults,
  guard interruption on BOTH sides of State switch, late-seam (slot/State/retention drift between prepare
  and adopt), repeat correction lineage (`original_anchor` carried + `supersedes` append — HIGH `:1031-1039`
  implements but no test asserts second correction), later-lifecycle readback after forward Selection/Architecture/Draft
  progress (HIGH `readback_revision:1209-1238` + LOW resolver must work without EVIDENCE_REVIEWED window per §11.2 —
  no test advances State forward), G71→G76 unchanged-upstream control, G76 correction→initial publication→editorial/renewal,
  affected regressions (`test_run_evidence_v2_interactive`, `test_prepare_evidence_run`, etc. per A2 §6).
  Two `except: pass` in LOW (retention walk-up + temp-unlink cleanup per A2 §4) are claimed “legitimate best-effort”
  but have no fault-injection proof that validation swallows are impossible.
- Fixture helper `tests/dm022_prearchitecture_fixtures_v2.py:53-78` is only `init_independent_git` + SHA helpers;
  real chain comes from `test_survey_evidence_v2.make_chain` + synthetic decisions in the test file itself.
  Thematic closure, Discovery-provenance counters, and single-Discovery (`target-source` only) fixtures do not
  exercise multi-ID affected/unaffected semantics, DROP handling, or INSPECT preservation required by §4/§8.

Minimum fix (execution, after B1–B7 code fixes + frozen re-snapshot):

- Bind ONE immutable complete integration snapshot (all owners, manifest SHA/bytes/modes, git independence,
  no `candidate-work` mutation during runs). Execute on it, with separately source-committed meaningful
  synthetic fixtures in independent Git DBs (no reconstruct objects, no old-runner reuse):
  Weekly + Thematic full prepare→adopt→resume→readback; complete 4-artifact acceptance; affected/unaffected
  semantic comparison + full obligations; 7-slot retain/clear + audit no-overwrite + regeneration;
  repeat correction (lineage assert); wrong-role publication refusal; forward Architecture/Draft/publication
  readback + history separation; G71→G76 control; G76→initial→editorial/renewal; old/new/unknown State +
  guard/completion loss + stale Raw/HEAD + ownership/close/replace faults + late seams + explicit resume
  (both sides of switch); synthetic reviews remain nongenuine. Preserve unique raw logs + exit codes + source pins.
- Run affected regressions named in A2 §6 + B/C suites on the same snapshot. No old test-count/PASS transfer.

---

## Claims NOT matched (author A2 vs R2 code)

1. “SAFE IO … no `os.replace` overwrite” (`author-A2-return.md` §2): NOT matched — HIGH `:139` `os.replace(tmp, path)`
   overwrites a concurrently created final; second `lstat` (`:133`) is not atomic (B1).
2. “REAL acceptance graph (no fabricated … no ignored exceptions …)” (§2): NOT matched for slots —
   `accepted_bound/gate_bound: False` constants without proof (B7); for ledger/completeness — proof trusts
   builder without re-validation (B5a); for Raw — SHA-only without event semantics (B5b).
3. “Ledger via REAL row construction … validated via real `_check_ledger_rows_content`” (§2): matched at BUILD
   (`LOW:1131-1140`) but NOT at PROVE (`prove_revision_from_paths` never calls it — B5a).
4. “Completeness via REAL … validated via real `_check_completeness_result_content` + `_thematic_closure_errors`
   + `_validate_obligation_shape`” (§2): matched at BUILD (`LOW:1314-1331`) but NOT at PROVE or
   `_load_typed_four_refs` FULL (B5a/B6).
5. “Checker … validates the FULL graph … No hash-only acceptance” (§2): NOT matched — checker delegates to
   partial `_load_typed_four_refs` (B6) + report/checkpoint cross-bindings only, no NEW ledger/completeness FULL.
6. “Completion validates FULL receipt schema/inventory/COPY-derived expected-after … (no trusted booleans …
   regenerated same-byte files … allowed)” (§2): NOT matched for `require_completion_consistent` (B3);
   partially matched for `require_research_operation_ready` except absent-plan regeneration (B4).
7. “Five narrow step oracles … are REAL bound-context steps (each verifies guard intent + executes exactly one
   IO-verified step …)” (§2): matched as bound-context dispatch (`HIGH:716-915`), BUT `write_cleanup_completion`
   idempotent path (`:877-881` compare `existing != core.json_bytes(completion)` with fresh `recorded_at`)
   can never be idempotent (new timestamp each call) — minor vs map, note for fix (use deterministic compare
   excluding `recorded_at` or refuse re-completion explicitly).
8. “Actual CLI with four operations (`prepare/adopt/resume/readback`, `argparse`, JSON stdout, exit 0/1 …)” (§2):
   MATCHED (`HIGH:1241-1284`). CLI exists; resume executes (not advice) — R1 §A5 closed on this point.
   Remaining CLI gap is B3-dependence (`resume … ALREADY_ACTIVE` via weak check).
9. “Shapes: `reason` (not `reason_class`), `from_state/to_state` (not `from/to`) …” (§2): MATCHED in A-scope
   (`LOW:45-56`, `HIGH:41-44`, `load_typed:274-281`). B/C `reason_class` fixes are out of A-scope for this review.
10. “No `if False` (0/0), no `task-placeholder` (0/0), no `hashlib.sha256(b` constants except 2 deterministic nonces,
    no `reason_class` (0/0), no invented `overall_status COMPLETE` (0/0)” (§4): static keyword scan MATCHED as far
    as keywords go, but B2/B5/B7 show keyword absence ≠ semantic proof (runner import, empty manifest arrays,
    constant `accepted_bound/gate_bound`, trusted booleans).
11. “Tests are new-only + existing A-owned (untouched). No old test-count/PASS transferred” (§4 + §5): MATCHED as
    statement, but 5/5 private scope is misreadable as R2 proof — explicitly NOT R2/all-fault coverage (B8).

Schemas (R2 worktree, read-only):

- 5 schemas parse as strict JSON (additionalProperties false, required, consts, safePath/sha256/gitsha,
  exact 7-slot enums, exact `EVIDENCE_REVIEWED`/`CANDIDATES_NORMALIZED` consts, single `DM022_SUPERSESSION_PROOF`
  review, `supersession_checkpoint_sha256` self-digest). B2 registry fix (report `10238a1a…` retarget
  `schemas/` vs R4 proposal `21369608…` `notes/...schema-proposals-r4/...`) preserved per A-return §2 — not re-hashed here.
- Schema gaps enabling B5: proof `rows_checked minimum 0` + proposed/manifest `tasks/cards/views` no `minItems`
  permit zero-row / empty-binding schema PASS; code MUST enforce non-empty (proof does for rows `:1560-1561`,
  but not for per-file arrays). Report `$defs/completionReceipt` + `retentionManifest` + `guardIntentCoord`
  are `$defs`-only (never top-level `$ref`); completion receipt validation relies on code (B3) — schema alone
  does not enforce receipt shape on read.

## Readiness: NOT_READY (blocking, no waiver)

Required pre-code predicates CLOSED for map purposes (ROOT §5), but R2 implementation predicates below are OPEN:

- Owned IO/resume exactness (B1), detached closure purity (B2), completion FULL verification (B3),
  normal-regeneration READY (B4), full proof/Raw/obligation/per-file binding (B5), active-resolver FULL (B6),
  unaccepted/Human-unbound retention proof (B7), frozen-snapshot both-route/negative/later-lifecycle + affected
  witnesses (B8).

No automatic rollback/global atomicity claimed (HIGH preserves INDETERMINATE, no restoration — correct per §7).
Unknown State preserved (HIGH `_classify_live:1113-1123` + resume INDETERMINATE — correct). No new family/schema
introduced in A-scope (correct). These do NOT offset the blockers above.

Next: implement B1–B7 minimum fixes in `candidate-work` ONLY (never edit R1/R2 snapshots), respecting disjoint
ownership (B: agent/ordinary consumers, C1: families/closures, C2: publication/editorial — return exact
interface mismatches to Astra rather than broadening). Then root binds a NEW immutable complete integration
snapshot, executes B8 witnesses + affected regressions with saved raw + pins, and seeks independent
implementation review before any closeout. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN
remain; Profile/quality/adoption/savings OPEN. Stop at Human Commit Point; ordinary Commit/Push Human-owned.

## Independence

- This reviewer is NOT Owner A/A2/B/C1/C2, NOT Astra author-side, and has NOT edited any source, schema,
  test, fixture, or config in `candidate-work` or snapshots. No runtime/tests/builds/fixtures/restores/network/
  Git mutations/Human commit readback were performed. Only the R2 worktree bytes + packet/output docs above were read.
- Findings are from actual file:line semantics vs selected contract + ROOT, not keyword-count alone.
  Line refs are to the R2 worktree (`snapshot-r2-20261028T124706Z/worktree/...`); `candidate-work` may have drifted
  via concurrent C2 edits — re-verify line numbers at the next freeze.
- This is an early blocking review, NOT a final audit and NOT implementation acceptance. The reviewer may later
  serve as final reviewer only with a fresh fixed snapshot + full raw evidence; no code editing by this reviewer.

