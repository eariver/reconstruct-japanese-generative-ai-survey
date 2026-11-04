# Evidence scaling implementation — return (no author approval/whole READY)

Author: General (implementer). Root + independent review BEFORE code already closed
(PRE_CODE_READY); this is implementation + bounded targeted checks, not adoption.
apply_patch TOOL unavailable in this harness; used `default.edit`/`default.write`
(specialized edit fallback) — disclosed.

## 1. Preparation (actual, limits disclosed)

- New dir `.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/`
  via `mkdir -p` (parent verified) + `cp -a proof-copy/. → candidate-work/` (new inodes).
- Verify 770/770 bytes+SHA vs `complete-profile-support-manifest.json` (hashlib, no project import):
  `ok=770/770 fail=0`. Physical modes 770/770 match manifest (`0o664` etc.).
- Independent DB: `.git/HEAD` preserved `409b292756dd1277b9dfae87679934c0d2ce251c`;
  `origin` inert `https://example.invalid/rephase-candidate-recovery.git`;
  no `objects/info/alternates` (dir absent); `.git/info` has only exclude/sparse-checkout;
  no `GIT_*` env; shallow preserved; sample inode old≠new
  (`24119523` vs `21534977` for `survey_evidence_v2.py`) — sample only, NOT full
  inode certification. No `__pycache__` created (PYTHONDONTWRITEBYTECODE=1).
- No restore scripts/old runners/cleanup; old rehearsal + real DATA untouched;
  old maps/reviews intact. Full 770 re-verification was pre-implementation;
  post-implementation only 3 runtime + 1 test files re-hashed (tests use temp DBs,
  do not mutate source — pins before/after identical for 3 runtime files).

## 2. Changed files (full hashes, post-implementation, pre/post-test identical)

- `scripts/survey_evidence_v2.py` 148492B `f8324e194394ed9683b21dedfc4a2776c5f2f7c94f28542ce8dfba774ffc0456`
- `scripts/run_evidence_v2_interactive.py` 42150B `e0b54245abf98cbd780a7d0fe6f815240d54caadbc976d7c1caaab5bca98bd62`
- `scripts/survey_research_authority_v2.py` 214105B `99441ba8519157712361f688d9cd4ba06bfed016941809d34e3cc8aaaaf98d8b`
- `tests/test_evidence_scaling_v2.py` (new, test-only) 33543B `8d3bec576f9e6cd29afc5b5aef34079356ace70100d7a0d802ea10b57781086d`
  (pre-fix `32917 a651…`; edit fixed drift-regex + manifest-file mutation, then green).

## 3. Helper mechanics (actual diff summary, Root §6 exact)

`survey_evidence_v2.py` (imports only `Callable`, `MappingProxyType` added; no new project module):
- `_capture_phase_pins`, `_recheck_phase_pins`, `_load_pinned_json` (same-buffer strict
  `core._strict_object_pairs`, private binder only).
- `_resolve_phase_supplement_context` (package FILE ref + pinned manifest bytes match
  vs `validate_evidence_authority_supplement` return; `manifest_ref` from package authority;
  `raw_refs` ALL manifest declared `raw_sha256/byte_count` (428 refs/425 paths for W34);
  `basis_refs` manifest-declared Discovery/Screening hashes + pinned lengths; empty package →
  legitimate empty ctx). `_recheck_supplement_context` (manifest/basis pins + ALL Raw via
  existing `_supplement_source_file` containment/no-follow/size/hash; never reseals).
- `_finish_authority_phase(ctx,pins,*,revalidate_owner)` (recheck→owner→recheck; owner
  non-recursive: package-basis/current or content/history, never whole acceptance wrapper).
- `_discovery_task_sources` (FIRST, no IO) + `_merge_supplement_task_sources` (pure slice,
  copy-on-return, unbound → exact old error). `task_authority_sources` preserves
  Discovery-first then supplement load only when task has IDs, always new local reload.
- `_build_card_core` ONE body; `build_research_card_content` reload-then-delegate.
  `_validate_card_core(card,task,task_sha,package,get_sources)` ONE body: early
  CARD_KEYS/identity/basis/entities, source-array/id 1057–1063, `get_sources()` ONLY at
  original 1070 branch before fallback loop, supplement+None → requires-context error,
  non-supplement structural no-IO, `OSError/ValueError/JSONDecodeError → errors.append`.
  Public `validate_evidence_card(...,repo_root=None)` reload-then-delegate (lazy).
- `accept_evidence_results`: resolve once via `validate_screening_acceptance` + `_resolve`
  (package-linear), pins package+tasks+results, per-task `_validate_card_core` batch,
  `_finish` BEFORE first copy + BEFORE final record (non-recursive owner
  `validate_evidence_package_basis`), idempotent path unchanged, preflight unchanged,
  partial run-dir preserved, no CAS.
- `_check_..._with_context` + standalone wrapper (once-load DATA for standalone only);
  `validate_evidence_acceptance` LIVE pins current State bytes (not old package State SHA)
  + recheck BEFORE RETURN; history `_content` DATA-only ctx (impl None, no LIVE State pin,
  path-identity via content core) + pins + recheck BEFORE RETURN.
- `accept_edition_views`: pins profile/evidence/views + recheck BEFORE first copy/final record
  (owner re-validates evidence, non-recursive). Readbacks recheck BEFORE RETURN.
  `build_materiality_ledger` pins profile/discovery/screening/evidence/views + recheck.
  Bare `write_materiality_ledger` unchanged (no authority guess; owner rechecks).

`run_evidence_v2_interactive.py` (no new imports; already imports evidence):
- `_build_card` now reload-then-`_build_card_core` (ONE core, no third mirror).
- `run()`: resolve `_run_ctx` once (screening + `_resolve`), task_source_ids pure slices,
  card build `_build_card_core` + inline `_validate_card_core` batch, discard ctx before
  canonical accept (no cross-phase reuse). Archive NEW phase after temp closed, bound to
  actual accepted package copy (`_capture`/`_recheck` acceptance+package-copy+input).

`survey_research_authority_v2.py` (no runner import, no LIVE; local `evidence_mod` only):
- LOW build: basis content vs true root (COPY-only, required PATHs) + `_resolve` DATA once,
  per-task `_build_card_core` + `_validate_card_core` batch (no per-task reload).
- LOW accept: basis content true-root + `_resolve` once, per-task `_validate_card_core` batch.
  Other LOW validators benefit via shared readback (source-own Epoch intact).
- `derive_ordinary_root_effective_context` COPY-only preserved; `None`/LIVE-path refused.

Preserved: `_source_class`/DM016 10 + old rows, 3/5/U/loss, DM022 7, true R/E,
new-admission/history separation, DM022 READY guards, no-overwrite/idempotent,
`repo_root=None` structural honesty, no public kwarg/verified-dict/bypass/global/ContextVar/
epoch-cache, no new module/schema/family.

## 4. Caller closure/modes (precise, not grep-only)

In-scope changed: runner `task_source_ids/build/inline`, `accept_evidence_results` loop,
`_check_..._with_context` used by current/history wrappers, Views accept/readbacks,
Ledger/Completeness owner writes + read-only RETURN rechecks, archive AFTER temp,
LOW build/accept loops + versioned wrappers. Behavior-via-shared-core (same predicates,
package-linear IO): `survey_architecture_v2_base`, `survey_drafting_v2_base`,
`survey_handlers_v2`, `survey_stage_validation_v2`, `survey_longform_derivation_v2`,
`survey_weekly_derivation_v2`, `survey_versioned_renewal_source_v2`,
`survey_prearchitecture_acceptance_v2`, `survey_completeness_v2`.
Per-public-phase reload constant allowed, no ContextVar. Logical-unit rechecks BEFORE
first copy/final record/RETURN, NOT per-file Raw sweep. Partial: pre-first-write zero
outputs; post-Evidence-accept earlier present/later absent. Generic writers gain no authority.

## 5. Tests (meaningful, no fake coverage)

New `tests/test_evidence_scaling_v2.py` (temp independent DBs, process-scoped identity,
inert origin, no GIT_* inheritance, meaningful commits):
- public-vs-private exact cards/errors + golden field checks (supplement URLs/class/role),
  unbound error preserved.
- Raw read-scaling per phase (instrument `core.sha256_file` IO only, real validation):
  old per-task reload vs new once-context; assert new ≤ distinct×4, old ≥ distinct×tasks.
- Late drift exact predicates + inventories: Raw recheck `bytes changed`, fresh `Raw SHA drift`,
  manifest `byte_count drift`, accept pre-first-write zero new outputs (rglob before/after equal,
  no symlinks), no reseal.
- Standalone/no-supplement/unbound/no-reuse: empty ctx legitimate, structural no-IO,
  supplement-but-unbound Discovery-only, two healthy ops different manifests, second sees new bytes.
- DIRECT/DERIVED/history/COPY + LOW: structural `src-1`, history content no LIVE
  (`verify_state_basis` must-not-call), LOW COPY `None`/LIVE-path refusal, no runner import.

Executed (FIXED temp snapshots, `PYTHONDONTWRITEBYTECODE=1`, py3.14.4, no installs):
- `tests.test_evidence_scaling_v2` 5/5 OK (0.8s) — `test-runs/scaling-20261103T114312Z/` (exit 0).
- old Evidence positive `...binds_exact_raw_source_and_card` 1/1 OK.
- old Evidence negative `...rejects_drop_unknown_path_sha_and_symlink` 1/1 OK.
- runner `tests.test_run_evidence_v2_interactive` 8/8 OK.
- Profile `DM016CanonicalTenTests.test_03` (positive) + `test_04` (negative) 2/2 OK.
- DM022 `Dm022A2OperationTests.test_low_typed_loader_dispatch` + `test_raw_binding_refuses_unbound_claim` 2/2 OK.
Raw files: `test-runs/{scaling-*,old-evidence-*,runner-contract,profile-upstream,dm022-low}/`
with UNIQUE stdout/stderr/PID/argv/env/exit (+ drift sub-run). Skips: none. Limits:
small fixtures only (3–4 tasks, 2–4 Raws); no real409 (root reviews diff first);
no wall-clock/IO performance claim (syntax + targeted checks only); no full-suite rerun.

## 6. Blockers / next

No missing-dependency contradiction found; no public-contract widening needed.
Remaining: root diff review → independent implementation review → fresh CURRENT proof +
complete delivery → Human Commit Point. SP Ledger/Completeness disposal still NOT
authorized (W34 proceeds). Dirty-code ≠ auto-refused (external committed/loaded source
check required at test epoch). No automatic R4/Production.

## 7. Correction after Astra source review CHANGES_REQUIRED (2026-11-03, runtime only)

Withdraw: initial "implementation complete" and "5 green = coverage" claims.
Initial 5-green proved helpers only, not full phase wiring; source author 5-green is
not proof. Initial snapshots + raw failures preserved in
`initial-snapshot-archive-20261103T121216Z/` (3 runtime + test with hashes, exact copy,
no overwrite). Tester now owns `tests/test_evidence_scaling_v2.py` (current file
differs from archive — parallel tester writes); runtime owner did NOT edit/run tests
after archive (only `ast.parse` static + hash reads, no unittest execution).

Runtime fixes (3 files only, no new module/schema/family, no public kwarg/cache/token):
- Pins BEFORE validation/parse everywhere: package/acceptance via `_capture` then
  `_load_pinned_json` same buffer; bind authoritative FileRefs/meta SHAs (meta SHA vs
  pinned task SHA, acceptance package SHA vs pinned copy) not post-validation bad bytes;
  explicit revalidate checked bytes immediately after validation before first use.
  Callbacks using cached dicts are guarded by pin rechecks before/after (detect file
  change); package dict comes from pinned buffer, not second read.
- `accept_evidence_results`: pin package → load pinned → pin tasks/results → bind meta
  SHAs → `validate_package_basis` → recheck → ctx → per-task `_validate_card_core`
  batch → `_finish` BEFORE first copy + BEFORE final record (owner
  `validate_evidence_package_basis`, non-recursive) + destination copy SHA checks
  (package/tasks/results vs authoritative) — no source-only final check.
- Historical acceptance: pre-pins acceptance+package copy, `_load_pinned_json`,
  bind package SHA, basis content true-root, recheck, DATA ctx (impl None, no LIVE
  State pin, path-identity only), with_context, recheck pre-pins before return.
- LIVE readback: pre-pins acceptance+package copy + current State actual bytes
  (not old package State SHA), load pinned, basis validation, recheck, ctx (impl sha),
  with_context, recheck pins+ctx BEFORE RETURN.
- Removed dummy ctx in `_check_...` (manifest_ref None + empty raw/basis disabled
  recheck despite real entries). Standalone now uses real DATA-mode constructor
  `_resolve_phase_supplement_context(impl None)` with full declared closure.
- Runner `_run_ctx`: screening + ctx inside `current_stage_basis_override` (real CAND
  facade); pins package+tasks (temp allowed); `_finish` with owner
  `validate_evidence_package_basis` BEFORE discard (was bare `None`).
- Ledger/Completeness before writer + archive after temp: full Raw/owner validation,
  not pins-only. Ledger pins + recheck + owner acceptances (with Raw); Completeness pins
  profile/discovery/screening/evidence/views/ledger/State + recheck before writer.
  Archive NEW phase: `validate_evidence_acceptance` + screening + `_resolve` (full Raw)
  + pins acceptance+package copy+input + `_finish` (owner `validate_evidence_acceptance`)
  before/after `_archive_input`.
- LOW bulk: pins COPY/profile/request/package/tasks (+results/views for accept),
  basis content true-root + DATA ctx, per-task `_build/_validate_card_core` batch,
  `_finish` with owner basis-content revalidation (nonrecursive DS/content, no LIVE)
  at logical return/publication.
- Recheck ancestor NoFollow: new `_assert_pin_repo_ancestors` (repo-local via
  `_repo_file` re-derivation + equality; temp outside repo allowed). Enforced in
  `_recheck_supplement_context` (manifest/basis) and `_finish` (phase pins) before hash.
  Raw loop linear (zip manifest order, no `by_id`/nested scan, duplicates rechecked,
  full sequence, no task subset). `MappingProxy`/copy-owned, no public token.
  Whole transitive callbacks non-recursive (basis/current or content/history, never
  whole acceptance); current readbacks pin actual CurrentState, history canonical
  path-only/COPY.
- Public standalone signatures/errors unchanged, structural no-IO branch preserved.
  No repeated full Raw per copy/task (package-linear: basis 1× + ctx 1× + rechecks).

Static check only after fix (no unittest execution while tester writes):
`ast.parse` OK 3 runtime files. Quiet runtime pins for fixed snapshot:
- `survey_evidence_v2.py` 153491B `49bcd9e9601e9a657afa6c8d416972a5ad3182be7fcc715a98936cf1e2c34b6e`
- `run_evidence_v2_interactive.py` 45501B `c9b7c70bd58055b105c6dce8b9e75072fa83e8396acd929d13b676185b4c225b`
- `survey_research_authority_v2.py` 217397B `31ab2c732de55065d44836bdefd81522d60867f6783c5912c1ed356f751ff3ce`

Remaining gaps: full transitive readback pins (Views history, Ledger history,
Completeness history) reuse LIVE-tested cores with DATA ctx — behavior preserved via
shared core, not separately re-pinned beyond phase pins; destination-copy SHA checks
cover Evidence/Views accepts, Ledger/Completeness writers verify via owner validators
+ pins (no direct destination SHA, as outputs are newly written JSON, not copies);
real409 still gated (no run before Root+independent source review).

## 8. Private phase table (exact wire sites)

- `accept_evidence_results` (`survey_evidence_v2.py`): pins `package → tasks+results`
  (pre-validation, `_capture` + `_load_pinned_json` + meta-SHA bind) →
  `validate_evidence_package_basis` (owner, current, non-recursive) → recheck →
  `validate_screening_acceptance` + `_resolve_phase_supplement_context` (impl sha,
  package-linear) → per-task `_validate_card_core` batch (lazy, no IO) →
  `_finish(ctx,pins,owner=validate_package_basis)` BEFORE first copy →
  copies + destination SHA checks (package/tasks/results vs authoritative) →
  `_finish` BEFORE final record → `core.write_json`.
- `_validate_evidence_acceptance_content` (history): pre-pins acceptance+package copy →
  `_load_pinned_json` → bind package SHA → `_validate_package_basis_content`
  (true root, no LIVE) → recheck → DATA ctx (impl None) → `with_context` →
  recheck pre-pins BEFORE RETURN (no State pin, path-identity only).
- `validate_evidence_acceptance` (LIVE): pre-pins acceptance+package+current State →
  `_load_pinned_json` → basis validation → recheck → ctx (impl sha) →
  `with_context` → recheck BEFORE RETURN (current State bytes, not old package SHA).
- `accept_edition_views`: pins profile/evidence/views BEFORE per-view validation →
  loop → preflight → `_finish(owner=validate_evidence_acceptance)` BEFORE first copy →
  copies + destination view SHA checks vs rows → `_finish` BEFORE final record.
- `validate_edition_views_acceptance` (LIVE readback): pins profile/evidence/views →
  with row checks → recheck BEFORE RETURN.
- `build_materiality_ledger` (+ `validate_*`): pins profile/discovery/screening/
  evidence/views (+ State for LIVE wrapper) → acceptances (with Raw via ctx) →
  `_check_ledger_rows_content` → recheck BEFORE RETURN; writer (`write_materiality_ledger`)
  generic, owner rechecks BEFORE writer in runner.
- Runner `run()`: temp package pins → `validate_screening_acceptance` + `_resolve`
  inside `current_stage_basis_override` → pins tasks → task_source_ids/build/inline batch →
  `_finish(owner=validate_package_basis)` BEFORE discard; accept/Views/Ledger/Completeness
  via owners above; archive NEW phase: `validate_evidence_acceptance` + screening +
  `_resolve` (full Raw) + pins acceptance+package copy+input + `_finish`
  (owner=`validate_evidence_acceptance`) before/after `_archive_input` (temp closed).
- LOW `build_revision_cards_views_from_paths`: `derive_ordinary_root_effective_context`
  (COPY-only, required PATHs) → `_validate_package_basis_content` (true root) →
  `_resolve` DATA → pins COPY/profile/request/package/tasks → per-task
  `_build/_validate_card_core` batch → `_finish(owner=basis_content)` at return (no LIVE).
- LOW `accept_revision_evidence_views_from_paths`: same + results/views pins →
  per-task `_validate_card_core` batch → `_finish(owner=basis_content)` at publication.

## 9. Second correction (independent review + Root #5/#3 accepted, #4/#1/#2 rejected)

Withdraw (reaffirmed): initial "implementation complete" and 5-green coverage claims.
5-green proved helpers only, not phase wiring; source author 5-green is not proof.
Initial snapshots + raw failures preserved in `initial-snapshot-archive-20261103T121216Z/`
(3 runtime `f8324e19/e0b54245/99441ba8` + test `8d3bec57`, exact copy, no overwrite);
quiescent pre-second-fix snapshots in `second-snapshot-archive-20261103T123055Z/`
(3 runtime `49bcd9e9/c9b7c70b/31ab2c73`). Tester owns `tests/test_evidence_scaling_v2.py`
(current file differs from archives — parallel tester writes); runtime owner did NOT
edit/run tests after `initial-snapshot-archive` (only `ast.parse` static + hash reads,
no `unittest` execution). Old rehearsal/proof never mutated; no network/Git readback/
ordinary commit; no real409.

Accepted #5 (readback pins ALL task/result files): `_check_..._with_context` now pins
ALL declared task/result files BEFORE checks, binds to authoritative meta/acceptance SHAs
(task pin == meta SHA, result pin == acceptance result SHA), uses `_load_pinned_json`
same-buffer parsed dicts (no read-after-hash different buffer), rechecks (with ancestor)
BEFORE RETURN. Wrappers (`validate_evidence_acceptance` LIVE with current State bytes,
`_validate_..._content` history with path-identity only, no LIVE State) pin
acceptance+package (+State LIVE only) BEFORE parse via `_load_pinned_json`, bind package
SHA, recheck before/after owner validation and before RETURN. Views readback pins ALL
views files BEFORE row checks (bind row view_sha), same-buffer parses, recheck BEFORE
RETURN; Views LIVE/history wrappers pin profile+views acceptance BEFORE parse.
Accept per-task loop uses pinned task/card buffers + pin SHAs for entries (no re-read
`sha256_file`/`core.load_json` different buffer); `package_sha` from pinned package pin.

Accepted #3 (ancestor + temp + pins-before + callbacks): new
`_assert_pin_repo_ancestors(repo_root,pin)` (repo-local via `_repo_file` re-derivation +
equality; temp outside repo allowed, no unconditional `_repo_file` feed) enforced in
`_recheck_supplement_context` (manifest/basis) and `_finish` (phase pins) + manual
pre/post validation rechecks. `manifest/basis/task/results` rechecks preserve existing
`_repo_file`/`_supplement_source_file` ancestor NoFollow + containment/size/hash;
owned temp package/task/results staging allowed. All material phases pin BEFORE
load/validate (`accept`, historical, LIVE, Views, Ledger, runner pre-accept/archive/
Ledger/Completeness, LOW build/accept pre-pins + post-load recheck) and callbacks
validate current pinned data (`_load_pinned_json` dicts, not old cached aliases);
`_finish` rechecks pins+ctx before/after non-recursive owner
(basis/current or content/history, never whole acceptance). No reseal (pins pre-date
validation, immediate recheck after). Raw loop linear (zip manifest order, no `by_id`/
nested scan, duplicates rechecked, full sequence, no task subset). `MappingProxy`/
copy-owned, no public token. Destination copy SHA checks (Evidence package/tasks/results,
Views) — source-only final check rejected.

Rejected #4 (LOW digest domain): kept `hashlib.sha256(core.json_bytes(ev_acceptance))`
as planned FILE hash. HIGH writes exact `core.json_bytes` at
`survey_prearchitecture_acceptance_v2.py:699` then validates at 716 — same serializer,
NOT `sha256_object`; pure builder cannot read future file. No serializer change;
control to be shown via actual write/readback witness (tester), not changed here.

Rejected #1/#2 (dead block / LOW lookups): left `validate_completeness:2780-2865`
dead block and LOW view-derivation quadratic + dead `rec=next(...)` untouched (not
measured Raw bottleneck, no new gate). Canonical factor preserves first-match behavior;
no duplicate-refusal change, no unrelated cleanup, no new feature.

LOW supplement wire (no new producer/schema/request feature): inspected
`build_revision_package_from_paths` — carries NO `authority_supplement` (grep: no match).
HIGH producer limitation documented (not added). Lower API validates provided actual
supplemented package + real request/COPY even if HIGH does not generate it:
`build_revision_cards_views_from_paths(repo_root, package_path, request_path,
results_dir, views_dir, *, before_copy_path)` and
`accept_revision_evidence_views_from_paths(repo_root, package_path, results_dir,
views_dir, profile_path, evidence_accepted_root, views_accepted_root, *,
request_path, before_copy_path)` accept a revision `package.json` containing
`authority_supplement:{path,sha256}` + tasks with `authority_supplement_source_ids`,
plus supplement manifest file (repo-relative, `*_supplement*.json`) with
`sources[{supplement_source_id, discovery_id, evidence_task_id, locator, source_type,
source_class, title, published_at, accessed_at, raw_path (repo-relative under
profile source_root, no traversal/symlink), raw_sha256, byte_count, relation}]`
+ Raw files (repo-local, non-empty, hash-pinned) + request with records bound to
effective DIDs + `before_copy_path` retained COPY + profile. Tester fixture interface:
provide above files via temp independent DB (process-scoped identity, inert origin),
call LOW bulk paths directly (no HIGH producer), expect `ResearchAuthorityError` with
exact predicate on drift/unbound/DROP/E-as-R/stale-basis, and `_finish` revalidation
at return/publication. Still finish LOW bulk cache/lateness where ctx nonempty
(pins + `_finish` + rechecks, no LIVE); no claim of no-future-source-gap if actual
public paths cannot construct valid context — document capability limit here.

Quiet runtime pins for fixed snapshot (post-second-fix, pre-test-dispatch, static only):
- `scripts/survey_evidence_v2.py` 156966B `dfc5e27f2f8c874c1a7ebc56f5b586c368e21b9a97ed7e7151798fc3e8ec6e17`
- `scripts/run_evidence_v2_interactive.py` 45501B `c9b7c70bd58055b105c6dce8b9e75072fa83e8396acd929d13b676185b4c225b`
  (unchanged from quiescent — facade/pins/_finish/archive/Ledger/Completeness already correct)
- `scripts/survey_research_authority_v2.py` 218692B `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`

Remaining limitations (no clean/whole PASS): Views/Ledger/Completeness history content
paths reuse LIVE-tested shared cores with DATA ctx (behavior preserved, pins cover
profile/acceptances + views/tasks/results where declared; full 770-file re-verification
not rerun post-fix — only 3 runtime hashes + pre-fix 770 manifest proof); destination
newly-written JSON (Ledger/Completeness/audit) verified via owner validators + pins,
not direct destination SHA (outputs, not copies); no real409 (Root+independent source
review required before fixed test dispatch, then real W34 409). Next: fixed test
dispatch after this return, then real409. No ordinary commit/Production/network/readback.

## 10. Third correction — readback RETURN freshness F5 (genuine runtime bug, not fixture)

Tester `batch-02c` (`1c95f675`, 15/16, PID 3415160) found genuine bug, preserved as durable
raw (`test-runs/batch-02c-full16-reattempt3/`, exit 1):
`test_readback_result_mutation_after_check_before_return_refuses_exact` — `ValueError not raised`.
Fault hook calls real `_check_..._with_context` (which rechecks its local `_cr_pins` then
returns), plants SAME-SIZE result drift, then outer `validate_evidence_acceptance` performs
more Raw/context work and returns WITHOUT rechecking task/result files. Pre-RETURN rechecks
covered only acceptance/package/State + supp ctx, not the declared result set. Not a fixture
error; independent SOURCE condition was test-green (subject), not permission to ignore failure.

Fix (3 runtime files only, no test edits/runs, no public kwargs/new module/schema/global cache):
- `_check_evidence_acceptance_results_with_context` now RETURNS `_cr_pins`
  (private helper return refinable, public API unchanged). Pins ALL declared task/result files
  BEFORE checks (bind meta/acceptance SHAs), same-buffer `_load_pinned_json` (no
  read-after-hash), per-task `_validate_card_core` batch, recheck (ancestor + pins + supp)
  BEFORE helper return.
- LIVE `validate_evidence_acceptance` + history `_validate_..._content`: capture returned
  `_cr_pins`, recheck COMPLETE declared set at actual public RETURN after other
  owner/context validation (no recursive whole-acceptance callback, no per-task Raw rehash):
  `for pin in (*pre_pins, *cr_pins): _assert + _recheck; _recheck_supp; _recheck_pins(all)`.
  Current State actual bytes (LIVE) vs path-identity + COPY (history, no LIVE) preserved.
- Standalone private wrapper `_check_evidence_acceptance_results_content`: resolves real
  DATA ctx (full closure; empty only when actual package has no supplement), calls with_context,
  rechecks returned pins + ctx BEFORE return (final freshness, no task subset, authoritative
  meta/result SHA + same-buffer parse).
- Views nested readback analogous: `_check_views_acceptance_rows_content` returns `_v_pins`
  (ALL views files pinned BEFORE checks, bind row view_sha, same-buffer parse, recheck BEFORE
  helper return); LIVE `validate_edition_views_acceptance` + history
  `_validate_..._content` capture + recheck views pins at actual public RETURN after other
  validation. Other analogous outer gaps censused: accept per-task loops already use pinned
  buffers + `_finish` (tasks/results) BEFORE first copy/final record + destination copy SHA
  checks; Views accept per-view loop uses pinned buffers + pin SHAs; Ledger/Completeness
  owner validators + pins BEFORE writer; runner pre-accept/archive/LOW bulk already
  `_finish` with role-correct non-recursive owners (basis/current or content/history).
  No recursive acceptance-validation loops, no per-task full Raw sweep, no source policy/
  public kwarg/new module/schema/global cache changes.

Quiet runtime pins for fixed F5 snapshot (static `ast.parse` OK, no test execution):
- `scripts/survey_evidence_v2.py` 158943B `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a`
- `scripts/run_evidence_v2_interactive.py` 45501B `c9b7c70bd58055b105c6dce8b9e75072fa83e8396acd929d13b676185b4c225b`
  (unchanged — facade/pins/_finish/archive/Ledger/Completeness already correct)
- `scripts/survey_research_authority_v2.py` 218692B `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`
  (unchanged — LOW pre-pins/_finish already correct; no producer feature added)

Exact private callback/pins sites (wire map delta for F5):
- `survey_evidence_v2._check_..._with_context(...) -> _cr_pins` (was `-> None`);
  callers `validate_evidence_acceptance:~1988` (`_live_cr_pins = _check...`),
  `_validate_..._content:~1774` (`_hist_cr_pins = _check...`),
  standalone wrapper `...:1726` (captures + final recheck, returns `None` preserved).
- RETURN rechecks: LIVE `...:1995` (`(*_live_pins, *_live_cr_pins)` + supp),
  history `...:1782` (`(*_hist_pre_pins, *_hist_cr_pins)` + supp),
  Views `_check_views... -> _v_pins`; LIVE `validate_edition_views_acceptance` +
  history `_validate_..._content` capture + recheck at RETURN.
- Potential callers unchanged (public signatures identical): `accept_evidence_results`,
  `validate_evidence_acceptance`, `_validate_..._content`, `accept_edition_views`,
  `validate_edition_views_acceptance`, `_validate_..._content`, LOW bulk paths (use
  shared cores, no new callers).

Remaining limitations (no clean/whole PASS, no independent approval): full 770-file
re-verification not rerun post-F5 (only 3 runtime hashes + pre-fix 770 manifest proof +
`ast.parse`); destination newly-written JSON (Ledger/Completeness/audit) verified via
owner validators + pins, not direct destination SHA; LOW HIGH-producer supplement gap
documented in §9 (no new producer); no real409 until green test rerun + Root + independent
source confirmation. Old rehearsal/proof untouched; no ordinary commit/network/readback.
Test case `test_readback_...` will rerun fixed snapshot next (tester-owned).

## 11. Fourth correction — escaped current-stage facade (genuine NEW wiring bug, not repin)

Real W34 run `real-w34-verification-20261103T170921Z` (new independent clone, genuine
epoch `bd80d603…` over `48082356`, Contract8 unchanged, old State/Profile/checkpoints
unchanged) stopped exit2 after 17.56s at runner pre-accept `_finish` (raw
`raw/stderr.txt` 2.3K traceback, `raw/machine.json` 21K, rchar delta ≈4.84GB logical):
`run:712 _finish → _revalidate_run_owner:710 validate_package_basis:1223 →
verify_state_basis:984`: bare legacy `core.verify_state_basis` compared historical
init `48082356` vs current `bd80d60` → `implementation commit differs...rebase required`.
No canonical outputs; old rehearsal preserved. This is NOT reason-handrepin or discard
agent-first epoch plan; existing strict `verify_current_stage_basis` requires actual
head + agent state (not failure stub). Do NOT fix bare `core.verify_state_basis`,
state-init hash, Profile, or old CP. SourceEpochScriptContract8 unchanged DATA.

Root cause: newly added `_finish` OWNER callback EXECUTION outside
`current_stage_basis_override`, not just definition inside `with`.
`current_stage_basis_override` monkey-patches `core.verify_state_basis` →
`verify_current_stage_basis` (actual head + agent state) + historical basis wrappers;
bare legacy path requires State impl == implementation_sha and rejects script-only
epoch. Runner pre-accept `_finish` (owner `validate_evidence_package_basis`) and
archive `_finish` ×2 (owner `validate_evidence_acceptance`) ran outside the facade,
so new epoch `bd80` vs old State `480` failed before first copy. No State/Profile/
contract edits; no validator weakening; no silent restart.

Fix (runtime author copy only, likely runner; 3-file ownership, no test edits):
- Runner pre-accept: `with agent_tool.current_stage_basis_override():
  evidence._finish_authority_phase(..., revalidate_owner=_revalidate_run_owner)`
  (was bare call). Definition of `_revalidate_run_owner` unchanged (still
  `validate_evidence_package_basis`); EXECUTION now inside facade.
- Runner archive: both `_finish(... owner=_revalidate_archive_owner)` wrapped in
  `with agent_tool.current_stage_basis_override():` (pins capture + `_archive_input`
  stay outside — file hashes/copies, no State validation; owner `validate_evidence_acceptance`
  needs facade). No change to `_archive_input` itself.
- Census (all new current-owner finish/entry checks, same escaped-facade mistake):
  preaccept ✅ fixed above; archive ✅ fixed above (×2);
  ledger (`_ledger_pins` capture + `_recheck`, no owner callback — hashes only, safe
  outside facade; owner `build_materiality_ledger` runs inside facade via runner
  `with override():`); completeness (`_comp_pins` capture + recheck outside, owner
  `validate_profile_completeness` runs inside facade via runner `with override():`);
  accept internal `_finish` runs inside facade because `accept_evidence_results` itself
  is invoked inside runner `with override():` (real epoch) and standalone tests use
  matching epoch (no facade needed); Views accept internal rechecks + owner
  (`_revalidate_views_owner` → `validate_evidence_acceptance`) runs inside facade
  because Views accept is invoked inside runner `with override():`.
  Accepted (`validate_evidence_acceptance` LIVE readback, no `_finish`, only rechecks —
  rechecks are hashes, safe; owner validation is the function itself, called inside
  facade by runner pre-accept/archive/Ledger paths, standalone tests use matching epoch),
  history (`_validate_..._content`, no facade — State-free content, never LIVE),
  LOW bulk/standalone (`_finish` owner = basis content, no LIVE — never wrapped in LIVE
  facade; `derive_ordinary_root_effective_context` COPY-only) remain unchanged.
  No module-global cache/new bypass; no historical_content wrapped in LIVE; no public
  standalone semantic change.

Public standalone `repo_root=None` structural branch, no-IO, preserved; no new
module/schema/family. Contract8 unchanged (pipeline/quality/research/publication SHAs
identical orig vs new per real-run packet §3). If other real contradiction appears,
return before broadening (no validator/state/profile/CP fix).

Quiet runtime pins for fixed facade snapshot (static `ast.parse` OK, no test execution,
no new 409 run, failed clone untouched):
- `scripts/survey_evidence_v2.py` 158943B `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a`
  (unchanged — F5 return pins already correct; facade fix is runner-only)
- `scripts/run_evidence_v2_interactive.py` 45833B `5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543`
  (changed: pre-accept + archive `_finish` EXECUTION inside `current_stage_basis_override`)
- `scripts/survey_research_authority_v2.py` 218692B `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`
  (unchanged — LOW historical, no LIVE facade)

Exact changed scopes (wire sites):
- `run_evidence_v2_interactive.run:~707` (`with override(): _finish(... _revalidate_run_owner)`,
  was bare `_finish`); `_revalidate_run_owner:709` definition unchanged
  (`validate_evidence_package_basis`).
- `run_evidence_v2_interactive.run:~890,894` (archive `_finish` ×2 wrapped in
  `with override():`; `_revalidate_archive_owner` definition unchanged
  (`validate_evidence_acceptance`)).
- No changes to `survey_evidence_v2._finish_authority_phase` (already rechecks +
  non-recursive owner; execution context fixed at call sites), no changes to
  `survey_research_authority_v2` (LOW/history, no LIVE facade), no changes to
  accepted/history/standalone wrappers.

Potential callers affected (same public signatures): runner `run()` pre-accept +
archive phases only (real epoch needs facade; matching-epoch tests unaffected —
bare `verify_state_basis` still passes when impl == State). No new callers.

Remaining limitations (no clean/whole PASS, no independent approval): full 770-file
re-verification not rerun post-facade (only 3 runtime hashes + `ast.parse` + pre-fix
770 manifest proof); failed real clone
`.rephase-1-editorial-runtime/evidence-scaling-w34-verification-20261103T170921Z`
untouched (raw stderr/machine/pins preserved in packet); no new 409 launch by owner;
needed tests assigned separately after fix (tester owns `d486...` additive Views;
source old report `1c95...` preserved). Real-run exits/source PIDs honored, no
Human Commit Point for failure — owned unit still active. Root reviews actual code;
prior facts kept. Do NOT run new 409 (tester/root dispatch), no ordinary commit/
network/Git readback/production.
