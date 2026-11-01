# Workstream D report — Test/fixture preparation (source edits + static parse only)

2026-10-31. Dedicated General TEST/FIXTURE owner D. Workcopy ONLY:
`.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`.
Runtime A/B/C are concurrently being corrected; NO behavioral tests run on
moving shared source in this invocation. Exclusive edit ownership kept:
ALL `tests/*.py` plus existing `tests/dm022_*_fixture_v2.py` family ONLY
where actual fixture migration needed; no shipping runtime/schema/config
edits. No subagents used. No commits/fixtures instantiated yet; source/test
edits allowed, later fixed snapshots instantiate meaningful independent
fixtures. No network/Production/intake/restore/reconstruct Git status/HEAD/
log/Human Commit readback/ordinary commit/push/cleanup/reset.

Authority (read in full before editing): contract
`outputs/rephase-1-profile-support-contract-decision.md` INCLUDING §7 (FULL
`62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`),
contract ROOT §5
(`notes/rephase-1-profile-support-contract/astra-review-resolution.md` FULL
`021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`),
precode assessment `outputs/rephase-1-profile-support-precode-assessment.md`,
packet `notes/rephase-1-profile-support-precode/README.md`, mandatory precode
ROOT FULL `bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa`
/20159B INCLUDING §7, R4 (`integrated-readiness-r4.md`) / R5 REQUIRED-path
hardening (`integrated-readiness-r5-path-hardening.md`) technical corrections,
workstream reports `workstream-{a,b,c}.md`, and
`astra-implementation-review.md` (working, changes-required 1–6).

Tool note: the `apply_patch` CLI is not installed in this environment
(`which apply_patch` not found), so every edit was applied with the
file-edit tool as an exact-string replacement (one edit per hunk, no other
bytes touched) and direct file creation for the one NEW test module owned
by this workstream. Same discipline as A/B/C reports; do not recast as
`apply_patch` execution.

## 1. Edited paths (exclusive ownership kept)

Workcopy only (workspace-side report is this file):

- `tests/test_run_evidence_v2_interactive.py` — MIGRATED existing direct
  caller to required keyword-only `discovery_records`/`root_discovery_records`.
  Added `_discovery_basis()` (canonical `paper`, empty `obligation_ids`,
  `U==P=={"obligation-1"}`) and forwarded both keywords in `validate()`.
  All 8 old test bodies preserved verbatim except the signature/fixture
  authority migration. No expectation change: old U==P 3-field inputs still
  pass; new-unknown/loss gates are covered in the new module, not by
  weakening these tests.
- `tests/test_dm022_prearchitecture_acceptance_v2.py` — REPAIRED simplified
  DCP fixture. Added `_materialize_production_discovery_acceptance()` (real
  Raw `root/raw/source.json` + real X spec/manifest per profile: WEEKLY
  REQUIRED run binding `target-source`, THEMATIC NOT_REQUIRED + real
  `build_acceptance`/`validate_acceptance`) and changed
  `_make_evidence_reviewed_state` to bind DCP `discovery-acceptance` to the
  real acceptance file (never raw JSONL). SCP unchanged (already the real
  Screening acceptance with sibling `package.json`). Old test bodies
  preserved; DCP bytes now satisfy the new LEGACY kernel
  (`validate_acceptance` + root-path/SHA + effective + request binding).
  Previous `disc.jsonl-as-acceptance` comment removed as superseded history.
- `tests/test_profile_support_upstream_repair_v2.py` — NEW test module
  (allowed: no new shipping runtime module/schema/family). 25 tests in 8
  classes, proportionate (not a duplicate of all old suites, no count-sum
  claim). Covers the dispatch oracle matrix explicitly (see §2). Uses REAL
  validators/helpers/loaders, real SHAs, exact error substrings, before/after
  file-inventory no-write checks, and independent temp trees. Git-backed
  cases use independent DBs with meaningful synthetic commits,
  process-scoped identity, inert `example.invalid` origin, no alternates/
  sharing, no `--allow-empty`, no reconstruct objects. All reviewer/executor
  labels are explicit `SYNTHETIC_FIXTURE_*`; no genuine Human approval.
- No other `tests/*.py`, no `scripts/*`, no `schemas/*`, no `config/*`
  touched. `tests/dm022_*_fixture_v2.py` helpers needed no separate edit:
  the DCP repair lives in the A2 test's own builder (which already owns its
  EVIDENCE_REVIEWED fixture); shared helper files are reused as-is.
  `test_dm022_full_lifecycle_v2.py` already binds DCP to the real
  production acceptance and was NOT edited.

## 2. Oracle coverage (new module test IDs)

- DM016: `test_01` all10 leaf exact; `test_02` unchanged old sample;
  `test_03` all10 through ACTUAL task/card authority
  (`task_authority_sources` + `validate_evidence_card` on a real chain
  package/task/card template, correct passes / mismatched refuses per type);
  `test_04` unknown leaf fail-closed.
- Unknown incl DROP pre-write: `test_05` pure preflight refuses unknown in
  KEEP and in prospective DROP (no shortcut); `test_06` Screening
  `prepare_package` with unknown refuses with EXACT unchanged inventory
  (immediate no-write, not post-repair equality).
- DM017 universe/loss: `test_07` U=P∪named(R)∪named(E); `test_08`
  shared-OID global-equality-insufficient (`(R-2,O-1)` loss refuses) vs
  healthy many-to-many passes; `test_09` DIRECT + derived carriers pass,
  non-array `parent_refs` does not; `test_10` `derive_bindings` DROP-safe
  (DIDs incl DROP, no invented tasks) and profile-only `([],[])`.
- Ordinary 3/5→7: `test_11` initial-only 3-field passes when U==P;
  `test_12` named-only 5-field with Profile dimension + non-empty
  description; `test_13` refuses 5-on-initial, 3-on-named, undeclared
  dimension, empty description, missing/extra/duplicate/invented/7-field;
  `test_14` `_build_completeness` derives `discovery_ids`/`evidence_task_ids`
  from effective/Ledger (DROP yields no tasks) and the derived final7
  passes the FULL `validate_completeness` + Selection-consumable shape.
- Profiles + parity: `test_15` all3 research Profiles upstream semantics;
  `test_16` direct/agent-first PUBLIC parity (normal builder owns
  closure-first residual union `["residual-A","residual-B"]`, adapter helper
  idempotent, `adapter.main` is thin `return runner.main()` with no
  monkey-patch assignments — helpers alone are NOT claimed as parity).
- History vs new: `test_17` healthy history readback predicate untouched
  (`validate_discovery_expansion` gains no `DECLARATION_LOSS`) vs new
  admission refuses loss.
- Prepackage: `test_18` genuine initial DIRECT (`NO_MARKER`/`DIRECT`,
  root==records==supplied); `test_19` Stage-claimed-but-marker-missing
  refuses (no DIRECT fallback) with unchanged inventory; `test_20` healthy
  claimed-DCP marker passes (`CANONICAL_MARKER`) vs mismatched supplied
  expected path refuses — explicit Astra finding #1 case (fails until A
  binds the State claim in the marker-present branch; no weakening);
  `test_21` symlink marker refuses with unchanged inventory.
- DM022 HIGH/LOW: `test_22` HIGH corrupted `discovery_ref` refuses BEFORE
  first State COPY (only the setup bad-request file is new, no COPY/revision
  dir); adopt re-verification is exercised via the A2 adopt path in
  `test_23`/`test_25`. `test_23` LOW adopted record passes detached checker,
  retention substitution refuses (full layout/byte binding, not plan-hash
  only), four builders expose REQUIRED keyword-only `request_path`/
  `before_copy_path` (missing keywords raise `TypeError`, never LIVE/basename
  guess). `test_24` ordinary report record-owned Contract8/implementation +
  canonical-path + digest predicates enforced (tampered contract refuses).
- Repeat/consumers/epoch: `test_25` same-`revision_id` repeat refuses
  (guard/no-overwrite), later `resolve_active_research_four_refs`/
  `resolve_research_authority`/`readback_revision` still PREARCH, adopted
  State passes strict LIVE `validate_agent_state` (own-epoch history vs
  CURRENT HEAD proof, no timestamp inference).

Changed expectations caused by correctly earlier refusal (honest): none in
the preserved old bodies. The A2 DCP repair CHANGES fixture authority
(raw-JSONL artifact → real acceptance artifact); its previously passing
LEGACY DCP path now exercises strictly MORE validation (acceptance schema/
X/SHA/graph + kernel request binding). Any A2 test that relied on the
simplified DCP shape would now refuse by design — that is the intended
fixture correction, not a runtime weakening. New-module `test_20`
(healthy-claim vs mismatched-claim) is EXPECTED to fail until workstream A
lands the marker-present claim binding per Astra finding #1; `test_22`–`test_25`
require the integrated A+B+C snapshot (A helpers + B runner + C HIGH/LOW).

## 3. Verification in THIS invocation (static only)

Checks run with `PYTHONDONTWRITEBYTECODE=1` (no `.pyc`, no project
imports, no fixtures, no suite execution on the mutating shared source):

1. `AST parse` the 3 touched files → `[5, 25, 36]` top-level bodies,
   `AST_PARSE_OK`, exit 0. Raw is the tool transcript (unique to this
   invocation, not saved as a separate raw file because the parse emits no
   project bytes).
2. `find tests -name __pycache__ -o -name *.pyc` → empty (no bytecode).
3. No `git status/HEAD/log`, no Human Commit readback, no network, no
   restore, no cleanup/reset performed.

Oracles READY (code complete, parse-clean, awaiting fixed-snapshot run):
all §2 IDs `test_01`–`test_25` plus the migrated 8 old interactive tests
and the repaired A2 DCP fixture chain.

Still PENDING (cannot be claimed until the next fixed-snapshot
invocation): ALL behavioral execution — imports, sandbox/X/acceptance
materialization, Screening/Evidence prepare/accept, runner
`validate`/`_build`, prepackage resolver, HIGH prepare/adopt/resume/
readback, LOW loaders/builders/checkers, Selection/Architecture consumers,
guard/no-write/idempotence inventories, CURRENT HEAD proof, and the
independent implementation review. No PASS, no coverage sum, no
adoption/savings claim is made here.

## 4. Expected runtime source dependencies (for the next invocation)

Fixed integrated snapshot must contain A+B+C landed together (do NOT run
against a partial tree):

- A: `survey_evidence_v2.SOURCE_CLASS_MAP` canonical10 +
  `_preflight_new_evidence_admission` + `survey_screening_v2`
  (`compute_obligation_universe`, `find_declaration_loss`,
  `derive_bindings`, `check_new_operation_admission`,
  `resolve_prepackage_root_effective`) incl. Astra finding #1 fix (bind
  State claimed DCP in the marker-present branch).
- B: `run_evidence_v2_interactive` (`_validate_completeness_input`,
  `validate_interactive_input` with REQUIRED kwonly R/E,
  `_build_completeness` 7-tuple kept, closure-first residual union, dead
  mapper removed) + thin `run_evidence_v2_agent_first.main`, incl. Astra
  finding #2 fix (require actual `root_records`, no E-as-R default).
- C: `survey_research_authority_v2` (PATH-only loaders, LEGACY DCP/SCP with
  record-owned Contract8/canonical-path/FILE-vs-result-set distinction,
  4 builders with REQUIRED kwonly PATHs, adopted-full 3-arg + full
  retention/layout binding per findings #3–#5) + `survey_prearchitecture_`
  `acceptance_v2` (HIGH preflight before first COPY `:538`, adopt
  re-verification `:1127`, zero `None,None`, no `BLOCKER(workstream-A)`
  shipping mode per finding #6) with real config/schema shapes.
- TeX for later real-build verification only (if affected): explicit
  `/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex` and `biber` per
  dispatch; NOT needed for this test-preparation unit.

## 5. Commands for the NEXT fixed-snapshot invocation (do NOT run now)

On a FRESH fixed snapshot (A+B+C integrated, workcopy quiesced), with
`PYTHONDONTWRITEBYTECODE=1` and unique raw capture per command (do not
overwrite old raws; distinguish setup failure vs intended negative by the
asserted error regex + before/after inventory diff):

```bash
# Positive controls first (must all pass):
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_profile_support_upstream_repair_v2.DM016CanonicalTenTests.test_01_all_ten_leaf_mappings_exact \
  tests.test_profile_support_upstream_repair_v2.DM016CanonicalTenTests.test_02_unchanged_old_mappings_preserved \
  tests.test_profile_support_upstream_repair_v2.DM017UniverseLossTests \
  tests.test_run_evidence_v2_interactive -v
# Full new oracle module (includes intended negatives; each negative asserts
# its exact error + immediate no-write inventory, not post-repair equality):
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_profile_support_upstream_repair_v2 -v
# Affected existing suites (no PASS transfer; rerun, do not sum counts):
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  tests.test_run_evidence_v2_interactive \
  tests.test_run_evidence_v2_agent_first \
  tests.test_survey_evidence_v2 \
  tests.test_survey_evidence_source_class_regression \
  tests.test_dm022_prearchitecture_acceptance_v2 -v
```

Intended failure sites (must refuse with the documented regex + zero new
files beyond setup): `test_04`/`test_05`/`test_06` (unsupported
source_type), `test_08`/`test_09-loss`/`test_13`/`test_17-new`
(DECLARATION_LOSS / shape gates), `test_19`/`test_20-mismatch`/
`test_21` (marker/claim/symlink), `test_22` (before-COPY refusal, no
`rev-d22-bad` dir), `test_23-retention`/`test_24` (binding/contract),
`test_25-repeat` (guard/no-overwrite). Setup failures (missing sandbox
files, Git init failure, X/acceptance materialization error) are distinct
from these intended negatives: they raise BEFORE the asserted gate
(usually `FileNotFoundError`/SHA drift/contract-identity error) and must
be fixed as harness faults, not counted as oracle passes.

## 6. Blockers / gaps honestly returned

- Astra findings #1–#6 are NOT fixed by D (runtime owners A/B/C): `test_20`
  healthy-vs-mismatched claim, B E-as-R default, C profile/canonical-path,
  adopted-full E-vs-R forwarding, retention cross-binding, and
  `BLOCKER(workstream-A)` shipping mode all require runtime corrections
  before the corresponding oracles can pass. D added the explicit failing
  cases; D did NOT weaken predicates or add test-only fallbacks to make
  them pass.
- Four LOW builders' new REQUIRED kwonly PATHs break any remaining direct
  test caller that still omits them: D migrated the ordinary-validator
  caller and asserted the new signatures in `test_23`, but a full
  caller census rerun on the fixed snapshot is still required (R3/R4 census
  predates C's final signatures).
- `tests/dm022_*_fixture_v2.py` shared helpers were NOT forked; if the
  integrator finds a second simplified DCP/SCP beyond the repaired A2
  builder (e.g. `test_dm022_b_late_prepublish_v2.py` synthetic
  `{"fixture": "discovery-acceptance"}` fault fixtures — intentionally
  invalid fault inputs, NOT healthy fixtures), D will migrate on exact
  instruction rather than silently rewriting fault-oracle semantics.
- No new capability/contract/dependency gap beyond the above; no schema/
  module/family/request-field change made or needed by D. Any further
  contradiction found during fixed-snapshot execution returns to Astra
  before broadening.

## 7. Files written

- Workcopy test edits (D-exclusive): `tests/test_run_evidence_v2_interactive.py`,
  `tests/test_dm022_prearchitecture_acceptance_v2.py`,
  `tests/test_profile_support_upstream_repair_v2.py` (NEW).
- This report (only workspace-side write):
  `notes/rephase-1-profile-support-implementation/workstream-d-test-preparation.md`.
  No runtime/schema/config/docs, no fixtures instantiated, no commits.

WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN retained; no
Commit Point claimed by D. Stopping here; no next unit auto-started.
