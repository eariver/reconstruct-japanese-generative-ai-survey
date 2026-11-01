# Workstream B report — Ordinary runner 3/5→7 + agent-first parity

2026-10-31. Workstream B implementation return. Workcopy ONLY:
`.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`.
Parallel workers own other files; B touched only its exclusive runner files below.
No subagents used. No ordinary commit/push, no reconstruct Git status/HEAD/log/Human
readback, no network/Production/restore/intake/cleanup/reset. Old docs/proofs untouched.
No behavioral suites run on shared moving source. `survey_completeness_v2.py` was
READ-ONLY (shared historical validator semantics unchanged).

Authority (read in full): contract
`outputs/rephase-1-profile-support-contract-decision.md` INCLUDING §7 (FULL
`62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`), contract ROOT
`notes/rephase-1-profile-support-contract/astra-review-resolution.md` §5 (FULL
`021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`), precode
assessment `outputs/rephase-1-profile-support-precode-assessment.md`, packet
`notes/rephase-1-profile-support-precode/README.md`, mandatory precode ROOT FULL
`bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa` /20159B
INCLUDING §7 (R3 mechanics/C-R2 arrays/kernel overridden by R4 then R5
REQUIRED-path hardening, then FULL ROOT). Scope reassessment
`outputs/rephase-1-scope-reassessment-20261031.md` §§1,3,8 removes automatic
generic-reader follow-on only; technical map binding, no new precode cycle.
Implement now; no new contract/authority/dependency gap found to return.

Tool note: `apply_patch` CLI is not installed in this environment, so edits were
applied with the file-edit tool as exact-string replacements with equivalent
scope (one edit per hunk, no other bytes touched). This report is the
`workstream-b.md` delivery.

## 1. Edited paths (exclusive ownership kept)

- `scripts/run_evidence_v2_interactive.py` — ordinary 3/5→7, keyword-only R/E,
  early preflight, closure-first residual union, dead-mapper removal.
- `scripts/run_evidence_v2_agent_first.py` — thin delegation, compatible pure
  helpers kept, monkey-patch removed.
- `scripts/run_screening_v2_interactive.py` — NOT edited (Screening decisions
  cover accepted Discovery IDs exactly; no DM017 U change per R3 §7).
- `scripts/run_weekly_interactive_*.py`, `scripts/run_special_interactive_*.py`
  — NOT edited. They are legacy v1 compact paths (`prepare_screening_run` /
  `prepare_evidence_run`); they do not call `validate_interactive_input` and
  need no caller forwarding for this map.
- `scripts/survey_completeness_v2.py` — NOT edited (READ-ONLY per assignment).
- `scripts/survey_evidence_v2.py`, `scripts/survey_screening_v2.py`,
  DM022 HIGH/LOW, tests/fixtures/schema/config — NOT edited (A/C/D ownership).

## 2. Concrete implemented behaviors

### 2.1 Dead runner mapper removed (census proved)

Deleted `run_evidence_v2_interactive.SOURCE_CLASS_MAP` (six-key) and
`_source_class` leaf. Census in workcopy: zero in-file callers, zero
`tests/*` importers of the runner leaf; live card `:321` and task inventory
`:666` paths already call `evidence.task_authority_sources`. Canonical10 /
`_source_class` belongs to A in `survey_evidence_v2.py` (A landed:
`PRIMARY_DOC` present). B only consumes `evidence._source_class`.

### 2.2 Required keyword-only R/E threading (R3 §6.3 exact)

```python
def _validate_completeness_input(value, profile, *, discovery_records, root_discovery_records)
def validate_interactive_input(value, profile, expected_ids, task_source_ids=None, *, discovery_records, root_discovery_records)
```

Both new kwargs are REQUIRED (no default; `None` refuses). They are
validation inputs inside the checked operation, not authority tokens.
`_build_completeness(repo_root, profile, profile_path, discovery_records,
ledger_path, ledger, input_value)` tuple KEPT (7 positional, no kwonly).

### 2.3 Exact ordinary 3/5→U contract

- `P` = Profile `initial_obligations` IDs; `U = P ∪ named(R) ∪ named(E)` via
  `screening.compute_obligation_universe(P, root_discovery_records,
  discovery_records)` (exact precode name, no duplicate policy).
- `id ∈ P` → exact 3 `{obligation_id,status,rationale}`; 5-field on initial
  refuses (no redefinition).
- `id ∈ U−P` → exact 5 `+{dimension,description}`; dimension must be
  Profile-declared, description non-empty.
- `id ∉ U` → refuse (no unrelated/invented OIDs); 7-field rows refuse.
- Exact `U` coverage, unique IDs, explicit valid status/rationale every member.
  No auto-SATISFIED/COMPLETE, no OLD fallback. Old 3-only passes exactly when
  `U==P`.
- Unknown `source_type` fail-closed on every validated root+effective record
  including prospective DROP via canonical `evidence._source_class`
  (no type-eligibility shortcut).
- `DECLARATION_LOSS` via `screening.find_declaration_loss(root, effective)`
  (exact name); `uncovered=[(parent,OID)] sorted` refuses before writes.
  Global-set equality insufficient.

### 2.4 Complete preflight AFTER R/E, BEFORE owned writes

In `run()`: after `resolve_active_screening_acceptance` +
`resolve_effective_discovery_basis` (`effective["records"]` +
`effective.get("root_records")`), load in-memory `interactive_doc` and call
`_validate_completeness_input(... discovery_records, root_discovery_records)`
BEFORE `tempfile.TemporaryDirectory` / `prepare_evidence_package` temp writes.
Later full `validate_interactive_input(..., expected_ids, task_source_ids,
discovery_records, root_discovery_records)` runs AFTER package with the real
generated task universe (record `source_bindings` task-authority checks).
No dummy task universe. Entry `_dm022_require_ready` + PREARCH-refusal +
prepublish guards retained.

### 2.5 Final7 internally derived, DROP-safe

`_build_completeness` derives for each `oid ∈ U` (Profile order then sorted
named-only): `screening.derive_bindings(oid, effective_records,
ledger_task_by_discovery)` → `(sorted declaring DIDs incl DROP, sorted union
task IDs via Ledger)`. Profile-only `([],[])` legitimate; DROP yields DIDs
with no invented tasks (Ledger binds none). Dimensions/descriptions from
Profile for initial, from validated input for named-only. No OLD completeness,
no child rewrite/autofill/status promotion. Full
content/basis/traceability/closure validators run downstream unchanged. No
DM0227 conflation (ordinary 3/5 gate never reused for DM022).

### 2.6 Closure-first residual union + 4+1+3 formulas

Normal builder owns parity: `normalized=list(closure_input["limitations"])`
then append each missing `residual` in residual order (byte-exactly as
`run_evidence_v2_agent_first:66-69`). Direct==agent-first byte-equal depends
on this order. 4 provenance/status-derived counters
(`expansion_passes/final_pass_new_sources/final_pass_new_material_obligations(_open)`
bound to `research_pass` + `MATERIAL_OBLIGATION_STATUS`) + 1 row-status count
(`open_material_obligations=needs_research`) + 3 operator-fed
(`targeted_gap_fill_completed/status/limitations` with union). No judgment
automation; statuses copied then cross-checked downstream.

### 2.7 Thin direct/agent-first parity

`run_evidence_v2_agent_first.main()` is now `return runner.main()` with no
mutable monkey-patching in either route. Both pure helpers kept byte-identical
for compat and remain directly tested:
`acceptance_with_canonical_discovery_records` and
`completeness_with_preserved_residual_limitations` (tests
`test_run_evidence_v2_agent_first.py:54,82,96,111` still bind).

Historical/idempotent branch semantics and entry+prepublish readiness/guard
preserved; ordinary paths only.

## 3. Required unowned caller changes (for integrator/D)

- `tests/test_run_evidence_v2_interactive.py:101-106` positional
  `validate_interactive_input(document, profile, {"D-1"}, task_sources)` →
  add `discovery_records=..., root_discovery_records=...` keywords from actual
  validated JSONL fixtures. Same for internal `_validate_completeness_input`
  caller (now only B's two sites migrated; test helper needs same).
- No prod caller outside `run()` uses these validators; `main()`/CLI unchanged.
- Agent-first helpers need no migration (signatures unchanged; `*args/**kwargs`
  forward still valid; normal builder tuple kept).
- Weekly/Special wrappers need no migration (no forwarding).
- A dependency now satisfied in shared workcopy: `survey_screening_v2`
  provides `compute_obligation_universe`, `find_declaration_loss`,
  `derive_bindings`; `survey_evidence_v2` provides canonical10. B calls them
  directly; integrator must keep A+B in same snapshot before behavioral testing.
- No schema/module/family/request-field change needed.

## 4. Verification (static-only, no cache) and limits

Checks run with `PYTHONDONTWRITEBYTECODE=1` equivalent (AST parse, no imports,
no `.pyc` emitted; no behavioral suites on shared moving source):

1. `AST parse run_evidence_v2_interactive.py / run_evidence_v2_agent_first.py /
   run_screening_v2_interactive.py` → all `AST-PARSE OK`, exit 0. Lines/bytes:
   interactive 945 lines (post-edit), agent-first 89 lines.
2. `AST signature audit` → `_validate_completeness_input (value,profile, *,
   discovery_records REQUIRED, root_discovery_records REQUIRED)`;
   `validate_interactive_input (value,profile,expected_ids,task_source_ids=None,
   *, discovery_records REQUIRED, root_discovery_records REQUIRED)`;
   `_build_completeness` 7-tuple kept, exit 0.
3. `Symbol census` → `evidence._source_class`, `compute_obligation_universe`,
   `find_declaration_loss`, `screening.derive_bindings`,
   `_normalized = list(closure_input` present; runner-local
   `def _source_class` / `SOURCE_CLASS_MAP = {` absent (only comment + canonical
   leaf mentions remain), exit 0.
4. `Agent audit` → no `runner.discovery.validate_acceptance =` /
   `runner._build_completeness =` assignment; `return runner.main()` present;
   both pure helpers present, exit 0.
5. `find *.pyc/__pycache__` not run as write; `PYTHONDONTWRITEBYTECODE` set for
   checks; no cache files created by B.

Source pins (workcopy post-edit, data-only `hashlib.sha256`, no Git):

- `scripts/run_evidence_v2_interactive.py` 44560B sha256
  `f92d26e5d3f43f0aa512b97ecfa5ff2e53449a2a9b953dfb3aeaf1a41cc82b90`
- `scripts/run_evidence_v2_agent_first.py` 3684B sha256
  `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910`
- `scripts/run_screening_v2_interactive.py` 9939B sha256
  `693df7484527ebcdd053e0368389247b9f618bdff7acbef759a266ac24b87f2f`
  (unedited)
- `scripts/survey_completeness_v2.py` 11843B sha256
  `ba551ba44bc37276f6949569a43f339ec84da67da5953d31547b63690be9c7e1`
  (READ-ONLY, unedited)
- Weekly/Special wrappers unchanged (hashes in check log; no edits).

Limits (honest): syntax/signature/symbol audits only, NOT runtime proof. No
imports, no behavioral suites, no fixtures, no DM022 HIGH/LOW or runner paths
executed (shared workcopy concurrently mutating; Owner D tests fixed integrated
snapshot). Cross-file runtime (A helpers + B preflight + C HIGH/LOW + D tests)
cannot be assumed executed until integrated. No author PASS, no whole
completion. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN;
quality/adoption/savings OPEN. Stop at Human Commit Point.

## 5. Files written

- Exclusive runtime edits (workcopy only):
  `scripts/run_evidence_v2_interactive.py`,
  `scripts/run_evidence_v2_agent_first.py`.
- This report: `notes/rephase-1-profile-support-implementation/workstream-b.md`
  (only workspace-side write). No tests/fixtures/schema/config/docs touched.

## 6. Correction per Astra review #2 — explicit root_records, no E-as-R (appended, first version preserved)

2026-10-31. Root `astra-implementation-review.md` #2 requires the ordinary
runner to require the resolver's actual `root_records` field and reject an
invalid resolver result instead of `effective.get("root_records",
discovery_records)`. Corrected within owned runner only; §§1–5 above are
preserved as the first-version return, not rewritten.

- Change (workcopy `scripts/run_evidence_v2_interactive.py` around `run:728`):
  replaced `root_records = effective.get("root_records", discovery_records)`
  with explicit `if "root_records" not in effective: raise ValueError("effective
  Discovery basis missing validated root_records")`, then `root_records =
  effective["root_records"]` plus `if not isinstance(root_records, list) or not
  root_records: raise` and same non-empty list check for `discovery_records`.
  No E-as-R fallback remains (`grep .get("root_records"` in owned
  `run_evidence_v2_*` now zero). Legitimate DIRECT is already explicit identical
  root bytes from the resolver contract; no new DIRECT behavior added.
- Analogous fallback audit (owned files only): no other `.get("root_records",
  ...)` / E-as-R default introduced. `_validate_completeness_input` and
  `validate_interactive_input` still REQUIRE keyword-only non-`None` lists and
  refuse otherwise; `_build_completeness` tuple kept and uses
  `screening.derive_bindings`; agent-first thin delegation unchanged.
- Early/late separation preserved: early pre-write path calls only
  `_validate_completeness_input` (U/loss/unknown/shape, no task universe);
  task-dependent `records` vs `expected_ids` + `task_source_ids` bindings stay
  in late `validate_interactive_input` after `prepare_evidence_package` with the
  real generated task universe. No dummy universe, no early task check moved.
- Tool disclosure: no `apply_patch` binary/CLI exists in this harness. All B
  edits (first version + this correction) were applied with the specialized
  file-editing tool (`default.edit` exact-string replacement, one hunk at a
  time). Prior §-header wording about a missing CLI is retained above; this
  correction does not recast prior edits as `apply_patch` execution, per review
  preparation §19.
- No unowned edits. No behavioral tests run (shared moving source; D owns tests
  on the fixed integrated snapshot).

Checks (static-only, `PYTHONDONTWRITEBYTECODE`, no imports, no cache):

- `ast.parse run_evidence_v2_interactive.py` → OK, exit 0.
- `grep .get("root_records"` in owned `run_evidence_v2_*` → 0 matches.
- Explicit-require strings present (`missing validated root_records`).

Corrected source pin (workcopy, data-only `hashlib.sha256`, no Git):

- `scripts/run_evidence_v2_interactive.py` 45084B sha256
  `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812`
- `scripts/run_evidence_v2_agent_first.py` 3684B sha256
  `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910`
  (unchanged by this correction)
- First-version interactive pin `f92d26e5d3f43f0aa512b97ecfa5ff2e53449a2a9b953dfb3aeaf1a41cc82b90`
  superseded by the corrected pin above for the same path; prior §4 pin retained
  as history.
