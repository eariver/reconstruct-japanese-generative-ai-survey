# Independent scoped R2 map review — Selection scaling repair

Status: Fresh independent scoped reviewer, not author/root. MAP-ONLY. Read `astra-repair-resolution.md` FULL, `integration-map-r2.md` + `integration-map-r2-machine.json` (machine line truncated at 2000 chars in read — remainder explicitly UNVERIFIED, see V1), prior `independent-map-review.md`, active source `.../repaired-correction-rehearsal-20261112T125743Z/candidate-work` (HEAD `ae0dd1ee…`, parent `cc1c7fd…`, tree `ec11cf6c…`). No code/runtime/tests/Git/network/reconstruct readback/subagents. Write only this review + machine.

Verdict: **CHANGES_REQUIRED** — R2 is the correct unified mechanism (bounded 6AG initial retained per root §2, multiplicative 45AG/90AG removed, LOW `1073` retained, full own-epoch batch retained, new HEAD via facade, no new module/family/global/ContextVar/caller-dict/public-flag/third-validator, no 3-file cap). Remaining gaps are literal substitutions + one ordering move + oracle fixes below. Once applied verbatim, map is READY (no new mechanism, root confirms before code).

Root-rejected demands NOT reiterated: no obligation to optimise initial 6AG/within-AG or run more timed-out writers; no new-HEAD contradiction; private cross-module allowed with owner/lifetime/B1; no lightweight own-epoch proof; no arbitrary file budget.

## V1 — Unverified (explicitly not guessed)

- `integration-map-r2-machine.json` full line truncated by read tool (`... (line truncated to 2000 chars`). Prefix verifies mechanism/delivery/forbidden/lifetime fields; remainder (exact counts, helper bindings, estimates) UNVERIFIED. Author must ensure machine contains NO 250–400 estimate, NO initial-affordability claim, and mirrors literal fixes below. Reviewer does not assert machine remainder.
- LOW kernel tail `low:1590-1684` (effective derivation return keys) and `_derive_root_effective_kernel` return `effective_records/effective_path` names partially observed at `low:1670-1684` (`root_records/root_path/root_sha256/effective_records/effective_path/effective_sha256/effective_mode/screening_decisions/provenance`) — sufficient to confirm R2 bundle field names exist, but full kernel predicate list not re-audited. R2 use of `derive_ordinary_root_effective_context(repo_root,request_abs,before_copy_abs)` (`low:1861-1909`, COPY-bound, refuses LIVE path `low:1890-1896`, HIGH-only current loader `low:1912-1956` refuses foreign LIVE `low:1937-1945`) verified for boundary; inner DCP/SCP legacy validation (`_validate_legacy_dcp_scp`) and discovery `validate_acceptance` (`low:1834-1838`) not re-audited line-by-line — flagged, not assumed.

## R1 — R2 line 163: State-SHA → triplet insufficient (BLOCKING, literal fix)

Actual wrapper `agent_tool:53-118` (`_historical_state_basis_wrapper` + `_historical_screening/evidence_basis_wrapper`): tolerates ONLY `state_sha256` drift, and ONLY after (a) sibling acceptance exists (`package_path.parent/acceptance_name`, `screening-accepted.json`/`evidence-accepted.json`, not symlink, is_file, else original `state_error`), (b) `sha256_file(package_path)==acceptance.package_sha256` else `changed_text`, (c) `basis.state_path` non-empty + within repo + file exists, (d) adjusted `basis.state_sha256=sha256_file(state_path)` then `original(...)` rerun. Original `validate_package_basis` (`screening:1322-1338`, `evidence:1203-1251`): `_check_*_files_content` + `sha256_file(state)==basis.state_sha256` (`screening:1333-1334`, `evidence:1219`) + `core.verify_state_basis` (`screening:1336`, `evidence:1223`, strict LIVE: profile bytes/contract/impl-SHA/legacy/semantics `production:959-995`) + issue/research binds. Content `_validate_*_package_basis_content` (`screening:1281-1319`, `evidence:1144-1200`): `basis.state_path==canonical_state_path` path identity, never SHA, never `verify_state_basis`. NOT equivalent.

R2 line 163 says State-SHA gap covered by `require_same_triplet` + State FILE rehash + triplet equality. Per root §2 this is insufficient. R2 lines 165-168 mention sibling+archived+rerun but line 163 contradicts it.

Literal substitution for §4 Gap coverage bullet (replace State-SHA line):
```
Gap coverage: State-SHA → for EACH package (screening package, evidence package) enforce ALL of:
(i) sibling acceptance exists (`package_path.parent/screening-accepted.json` /
`evidence-accepted.json`, O_NOFOLLOW, regular file) + `sha256_file(package_path)==acceptance.package_sha256`
(`agent_tool:71-76`, `screening:1513-1514`, `evidence:1765/1925`);
(ii) `basis.state_path==canonical_state_path` path identity (`screening:1304-1305`,
`evidence:1168-1169`) AND `sha256_file(State FILE)==basis.state_sha256` equality
(`screening:1333-1334`, `evidence:1219`) — both, not either;
(iii) `core.verify_state_basis` strict LIVE predicates via facade where HEAD applies
(`agent_tool:42-50` requested==HEAD then `agent.validate_agent_state`; initial `:249`
already provides strict State validation, no extra AG);
(iv) `require_same_triplet` + State FILE rehash + triplet equality (necessary, not sufficient).
Content-only + triplet alone is never a substitute.
```
No new validator; existing shared cores already cover files/batches/digest/tasks
(`_check_screening_package_files_content`, `_check_screening_batches_and_digest`
`screening:1394-1433` called from BOTH LIVE `:1541` and content `:1519`,
`_check_evidence_package_fields/files_content`, `_check_ledger_rows_content`,
`_check_completeness_result_content` + `_validate_obligation_shape`
`completeness:50-78` + `_check_profile_completeness_extra_content`).
R2 must list these shared call sites explicitly (done above) and state: sibling bind does
NOT imply rerun — rerun is (i)-(iii) in `_assert_selection_authority_fresh` per package,
with `implementation_sha`=bundle HEAD under no override for FILE/SHA/path/sibling checks;
`verify_state_basis` rerun only where facade applies (EU under override, initial `:249`).
If a class cannot be pinned, retain full check for that class (per prompt).

## R2 — Shared-core extraction claim (BLOCKING, literal fix)

R2 §4 line 169: “No predicate duplicated/relaxed; private factoring with internally
constructed context only.” No named factored function given — likely false as a new
extraction (no actual shared-core definition).

Literal substitution: replace with:
```
Shared cores are EXISTING functions only (no new extraction):
`screening._check_screening_package_files_content`,
`screening._check_screening_batches_and_digest`,
`evidence._check_evidence_package_fields_content/_check_evidence_package_files_content`,
`evidence._check_ledger_rows_content`, `evidence._check_completeness_result_content`,
`completeness._validate_obligation_shape/_check_profile_completeness_extra_content`.
LIVE and content paths already call these same helpers (cites above); differing
predicates (State-SHA+verify_state_basis vs path-identity) are BOTH enforced in
freshness per R1, not factored into one predicate.
```
If author wants new factoring beyond listing, define exact function name/signature/file/lifetime in LOW/BASE existing files only (no LOW→architecture move) and return for re-review; otherwise listing suffices.

## R3 — Holder `dict` vs private internally-owned type (BLOCKING, literal fix)

R2 §4 line 107-108: `low._get_selection_authority_bundle(...) -> dict`,
§6 line 196: `low._assert_selection_authority_fresh(..., bundle: dict)`.
Passing `dict` as authority violates root §2 (reuse built from internally reloaded bytes,
isolated to owner, never caller assertions, never escapes invocation). `dict` is mutable,
caller-constructible.

Literal substitution (all occurrences §4-§6/§8/§11/machine):
- Define in LOW (existing file, no new module):
```
class _SelectionAuthorityBundle:  # frozen, slots, no public constructor
  # fields exactly §4 line 134-137: state_path,state_sha,checkpoint_path,checkpoint_sha,
  # four_paths_shas_bytes, request/manifest/report/proof/decision/retention/COPY/completion_pins_bytes,
  # profile_bytes, root_records,root_path,effective_records,effective_path,screening_acceptance,
  # expectations,supplement{manifest_ref,entries:MappingProxyType,raw_refs:tuple,basis_refs,source_root},
  # own_epoch{commit,blobs,contract},guard_lstat,seven_lstat,implementation_sha
  # entries MappingProxyType, raw_refs tuple, all pins tuple[label,Path,sha,len]; no setter.
```
- `low._get_selection_authority_bundle(repo_root: Path, state_path: Path) -> _SelectionAuthorityBundle`
- `low._assert_selection_authority_fresh(repo_root: Path, state_path: Path, bundle: _SelectionAuthorityBundle) -> None`
- Runner holds opaque handle only: never constructs, never `bundle[...]` indexes, never mutates.
  Needed paths for first EU (`profile_path,discovery_path,...`) obtained via LOW getters,
  e.g. `low._bundle_upstream_paths(bundle) -> tuple[Path,...]` (exact signature to be stated),
  or passed as explicit separate args from bundle creation (no dict indexing in runner).
Update §8: runner→LOW edge carries opaque type, not dict; no `verified_dict`.

## R4 — Full closure enumeration gaps (BLOCKING, literal additions)

R2 §4 enumeration is close but misses/underspecifies (checked against actual helpers):

(a) DCP/SCP checkpoint records + CORE reports missing. Bundle pins DCP/SCP acceptance
+ root/effective JSONL (`low:1833-1847` loads `dcp_artifacts[...]` + `discovery.validate_acceptance`
+ `read_jsonl(root_abs)` + `validate_discovery_set`), but NOT the DCP/SCP checkpoint record
FILEs themselves (`before_state.checkpoint_provenance.discovery/screening` refs loaded via
`_load_cp` `low:1775-1789` + `_validate_legacy_dcp_scp` `low:1820-1827`) + their
`CORE_STAGE_CONTRACT` review result FILEs (via `_rehash_deterministic_reviews` `low:1325-1379`).
Add to §4 bundle file list (with `_verify_sized_ref/_safe_read_bytes` + `_artifact_ref_shape`):
`before_state.checkpoint_provenance.discovery` record FILE, `...screening` record FILE,
each record's `reviews[CORE_STAGE_CONTRACT].result.{path,sha256}` FILEs, each record's
`artifacts[discovery-acceptance/screening-acceptance]` FILEs (already), plus
`_local_artifact_map` uniqueness (`low:1270-1286`).

(b) Screening batch/result pinning. R2 says “via `_check_screening_batches_and_digest`”.
That helper (`screening:1394-1433`) validates via `_validate_result_batch`
(`screening:1341-1381`, reads batch JSONL + result JSON, checks digests) but does NOT
`_capture_phase_pins`. Bundle MUST separately `_capture_phase_pins` BEFORE validation:
batch input FILEs (`package.input.batches[].path` basenames under `package_path.parent/input/batches/`)
+ result FILEs (`run_dir/results/<batch_id>.json`), exact set via `screening._exact_regular_files`
(`screening:99-...`, same semantics as `evidence:738-753`: no symlink, files only, exact
missing/extra refusal). List exact dirs in §4; do not claim helper pins.

(c) Tasks/results/views/supplement pre-capture chain. R2 lists `tasks/*.json` via
`_exact_regular_files(run_dir/tasks, expected_names)` (`evidence:1635-1636`, names from
`package.tasks[].path` basenames, `meta_by_id` bind `evidence:1634-1661`), views via
`_exact_regular_files(views_dir, {view_filename(task_id)})` (`evidence:1819-1826`),
supplement all-entry loop (`evidence:369-376`, `_supplement_source_file` `evidence:497-520`)
+ basis pins (`evidence:359-368`). Correct, but R2 must state capture-then-parse chain:
capture package FILE pin BEFORE parsing `package.tasks` to enumerate tasks; capture
acceptance FILE pin BEFORE parsing `results` to bind `meta_by_id`; capture manifest FILE
pin BEFORE parsing `validated.sources[]` to enumerate Raw. Never parse unpinned file to
discover next file. Add one sentence + ordered steps to §4.

(d) Non-supplement Raw. Confirm: no Raw files exist outside supplement (`_resolve_phase_supplement_context`
`evidence:300-330` returns empty ctx `{manifest_ref:None,entries:{},raw_refs:(),basis_refs:(),source_root:None}`
when `authority_supplement` absent; `_recheck_supplement_context` `evidence:389-424` no-ops).
State this explicitly so “full closure” is not read as missing non-supp Raw. Supplement Raw
= every `validated.sources[]` entry (never task-subset, `evidence:369-376` + `len(raw_refs)==len(entries)`
`evidence:412-413`).

(e) Consumed parse before capture. Fix by (c) chain + R5 ordering (bundle BEFORE initial).

## R5 — Bundle timing: before initial 6AG + bind without repeat-full (BLOCKING, ordering move)

R2 §4: bundle AFTER `:264`. Then bundle pins are post-initial baseline; drift `:249→bundle`
would be rebaselined (violates root §2: pins BEFORE validation bytes consumed).
And initial not bound to bundle unless repeats full after capture.

Literal ordering fix (replace §4 “After `:264`” + §1/§6 flow):
```
(i) NEW bundle capture BEFORE `:249` (stepwise capture-then-parse chain from
`state_path` arg only: State FILE pin→parse→checkpoint refs→checkpoint FILE pin→parse→
four refs/request ref→request/manifest/... pins→DCP/SCP/root/effective→screening/evidence
acceptance/package pins→tasks/results/views/supplement enumeration pins; any
captured!=expected-ref at capture time → fail-closed, no bundle, never `expected=observed`).
(ii) `:249` 3AG + `:260` 2AG (incl `low:1018+1073` retained) + `:264` 1AG full (unchanged code).
(iii) Immediately `low._assert_selection_authority_fresh` (cheap + full own-epoch batch)
to prove bundle still current (binds initial to bundle without repeating 6AG).
(iv) First content-EU with bundle `expectations/root_records/root_path` + pre-captured pins.
```
No extra full validation; one cheap freshness after initial (negligible vs AG).
Update §1 flow sentence + §4 call site + §11 checklist accordingly.

Expected-refs vs new capture (user spot): add to §4 bundle spec verbatim:
```
At capture, for every file, verify `_safe_read_bytes` sha/byte_count == expected ref
(from checkpoint/manifest/request/SizedRef) BEFORE storing pin; mismatch → fail-closed
`ResearchAuthorityError`/drift, no bundle. Bundle stores newly captured (path,sha,len,bytes-hash),
never copies ref strings as pins. Freshness compares current FILE vs bundle pins, never vs
provisional originals.
```

## R6 — 9 vs 6 counting (BLOCKING, literal fix)

R2 says “6 AG bounded initial” (§1 line 29, §1 line 36 net, §4, §6, §11, machine).
Actual retained: `:249` 3AG + `:260` 2AG + `:264` 1AG =6AG PLUS screening `:283`
first-half 3AG kept (`resolve_checkpoint_artifact` path, §6 line 210) =9AG pre-first-EU
(`:286` 0AG, preflight 0AG). Second-half 3AG removed via content.

Literal substitution everywhere (including machine `blocking_addressed`/initial):
Replace `6 AG bounded initial` / `6AG initial` / `6AG initial + 0AG EU` with
`9 AG bounded initial (6AG `:249+:260+:264` + screening first-half 3AG, second-half 0AG via content)`.
Net becomes `162AG → 9AG initial + 0AG EU + cheap freshness`.
No affordability claim added (see R9); 7-run oracle proves practicality.

## R7 — Mapped codeset filenames (VERIFIED, no fix)

Checked `low:587-599` vs R2 §3 lines 81-85. R2 list matches byte-for-byte:
`scripts/survey_research_authority_v2.py`, `scripts/survey_prearchitecture_acceptance_v2.py`,
`schemas/dm022-revision-request-v2.schema.json`, `schemas/dm022-revision-manifest-v2.schema.json`,
`schemas/dm022-revision-proof-v2.schema.json`, `schemas/dm022-preadoption-report-v2.schema.json`,
`schemas/dm022-supersession-checkpoint-v2.schema.json`; `$id`s `low:601-607` as cited.
User suspicion of invented schema filenames NOT reproduced. No correction needed; retain
R2 §3 + F7 sentence (Contract8 unchanged ≠ repaired-code proof).

## R8 — Base private missing `repo_root` (BLOCKING, literal fix)

R2 §5 line 178:
`base._validate_candidate_matrix_against_upstream(matrix: dict, upstream: dict, profile_path: Path, ...`
lacks `repo_root` but must call `base._derive_matrix_rows_content(repo_root,upstream,...)`
(`base:183-276`, needs `repo_root` for `sha256_file+load_json` at `:213-218`).

Literal substitution:
```
base._validate_candidate_matrix_against_upstream(repo_root: Path, matrix: dict, upstream: dict,
profile_path: Path, completeness_path: Path, ledger_path: Path,
evidence_path: Path, views_path: Path) -> list[str]
```
`_build_..._with_upstream` (§5 line 181) already has `repo_root` first — retain.
Runner call sites pass `repo_root` first in both.

## R9 — Runner→base import contradiction (BLOCKING, literal fix)

R2 §4 says runner calls `base._load_upstream_content` + `base._derive...` directly;
R2 §8 says “no new runner→evidence/base/completeness/screening direct private imports,
single existing runner→low edge”. Both cannot hold. Runner today imports
`agent,agent_tool,architecture,wrapper,discovery,core,low,review_attention,schema_gate,screening`
(`run:20-28`), no direct `base/evidence/completeness`. `architecture` wrapper forwards
everything via `__getattr__` (`survey_architecture_v2.py:144-145`), but relying on
`__getattr__` forwarding for privates is fragile and undocumented.

Literal fix (choose one, R2 must be consistent; minimal is explicit import):
In §8 Changed paths runner bullet, replace `no new runner→evidence/base/...` with:
```
Runner adds `from scripts import survey_architecture_v2_base as base`
(existing modules, new edge runner→base documented; owner BASE, lifetime
invocation-local; B1 preserved: BASE top-level only stdlib+core/completeness/evidence
function-local as today; runner never imports evidence/completeness/screening privates
directly — those via LOW function-local only).
Call sites: `base._load_upstream_content`, `base._derive_matrix_rows_content` (via
`derive_candidate_matrix_content` or directly), `base._validate_candidate_matrix_against_upstream`,
`base._build_..._with_upstream` (or via `architecture` wrapper if wrapper adds explicit
methods — not via `__getattr__`).
```
If author prefers wrapper-only (no runner→base edge), then add explicit methods in
`survey_architecture_v2.py` (4th file change, allowed per root — no 3-file cap) and
state signatures there instead; do not claim both no-import and direct-base calls.

LOW holder NOT architecture-specific (verified): LOW bundle/freshness contain NO
matrix/selection/architecture validation (bundle §4 lines 134-137 has no
matrix/selection/architecture; row derivation stays in BASE `_derive...`,
`validate_selection` `base:407-564`/wrapper, `validate_architecture`
`base:567-...`+wrapper empty-placement `survey_architecture_v2.py:98-141`).
Add one boundary sentence to §8: “LOW holds research authority + D/S + supplement pins
only; upstream object lives in runner, row/Selection/Architecture validation live in BASE.”

## R10 — Missing-blob + stable-rerun oracles (BLOCKING, literal fixes)

(a) R2 §9 lines 277-279 uses `b797…` as missing-blob example. Closeout §2: `b797…`
already missing, unrelated, still missing; own-epoch needed set (`low:685-695`:
contract inputs from COMMIT config + `config+2 schemas` + sorted pinned 7 +
`request.profile_ref`) does NOT include `b797…`, so absent `b797…` would NOT refuse
(oracle would falsely expect refusal).

Literal substitution:
```
Source-epoch/missing-blob: on implementation copy ONLY (never active/shadow),
`mv .git/objects/<aa>/<rest> /tmp/backup` for ONE proof-required blob
(e.g. `scripts/survey_research_authority_v2.py` blob from `low:592`,
or `schemas/dm022-supersession-checkpoint-v2.schema.json` blob from `low:598`,
or `config/survey-production-v2.json` blob from needed set `low:689-691`),
then run full `_verify_own_epoch_commit` → MUST refuse `ResearchAuthorityError`
(missing/corrupt object, proves SHA-only insufficient); restore `mv` back, re-verify pass.
`b797…` MUST NOT be used (already missing, unrelated, not in needed set).
Verify needed blobs present in copy first (`git cat-file -e <commit>^{commit}` etc.;
231/231 objects expected); if needed blob absent in copy, copy procedure failed, abort.
```

(b) R2 §9 lines 284-286 “stable across clean rerun (same bytes, new inode allowed)”.
`audit` (`run:459-471`) binds `interactive_input{path,sha256}` + `runner` (from input file,
fixed if same input bytes) + 5 outputs SHAs; no `generated_at`. Stable ONLY if same
input bytes reused. Second run over SAME `source_root` would refuse overwrite
(`_dm022_preflight_seven` `:304` + per-file `exists/is_symlink` refuses `:317,363,428,441,445,452,457`).

Literal substitution:
```
Archive/audit stability: TWO independent clean copies from same `ae0dd1e`
(same procedure §2), SAME input file bytes (copy once, reuse same bytes for both runs),
run normal `run()` on each, compare seven outputs + `audit.json` `sha256_file` equal
(bytes equal; `lstat` inode may differ per `low:1102-1124` same-byte-new-inode tolerance;
modes `100644` preserved). Never re-run over same `source_root` (would refuse, not a failure).
Different input bytes (new `generated_at`/invocation) differing audit is NOT a failure.
```

## R11 — Initial-affordability + 250-400 estimate (COMPLIANCE, no new claim)

R2 visible text makes NO affordability claim and contains NO 250-400 numbers
(§1: “Cost is one-time and honestly recorded; real W34/SP 7-run oracle proves
practicality (no speedup claim, no extrapolation from READY probes…)”). Retain verbatim.
Machine remainder UNVERIFIED (V1) — author must ensure machine contains no 250-400
estimate and no “initial fits” claim. Any such estimate if present must be deleted;
oracle wall/CPU/`rchar` honestly recorded only (no uninstrumented ranking/speedup,
no full-run extrapolation from READY 85.01s-partial-8E / 27.98s-12E observations).

## Checklist (literal substitutions that close the map)

- [ ] R1 line-163 replacement (State-SHA four-part, wrapper cites, no triplet-only).
- [ ] R2 shared-core listing (existing helpers only, no new extraction or define it).
- [ ] R3 `dict` → `_SelectionAuthorityBundle` + getters, opaque runner handle.
- [ ] R4 (a) DCP/SCP records + CORE reports added; (b) batch/result explicit pins (not helper);
  (c) capture-then-parse chain; (d) non-supp Raw empty-ctx sentence; (e) never-parse-unpinned.
- [ ] R5 bundle BEFORE `:249` + `_assert...fresh` after initial + captured==expected-ref check.
- [ ] R6 6AG → 9AG everywhere including machine.
- [ ] R7 no fix (verified).
- [ ] R8 add `repo_root` to `_validate...against_upstream`.
- [ ] R9 runner→base import stated (or wrapper explicit methods, 4th file allowed) + LOW/BASE boundary sentence.
- [ ] R10 (a) proof-required blob (not `b797`) with `mv`-aside/restore on copy only;
  (b) two-copy same-input stability, no overwrite.
- [ ] R11 no affordability/250-400 in text+machine.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.
Ordinary Commit/Push Human-owned. No code until root confirms true map closed.
