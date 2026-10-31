# Profile/support integrated readiness R2 — pre-code map (docs/source-read ONLY)

2026-10-31. **WORKING NOT_READY. No author PASS. No implementation.**
Integrates A (admission/callsites), B (obligation/derivation),
C (family/closure) per gate FULL + decision `62b14add` §§6-7
+ ROOT `021a0d7c` §5. Preserves all original A/B/C unchanged.
Source READONLY `proof-candidate` actual409/tree8ce +133paths/768files
(patch `25b48878`/4931836B, manifest `31fa4a72`/185422B).
No imports/runtime/tests/build/fixtures/network/restore/Git/readback.
New files ONLY: this md + `integrated-readiness-r2.json`.
No source or old-report edits.

Authority: decision §§3-4 normative; ROOT §§1-5 normative;
independent authority §8 + operation §§12-13 FINAL-BINDING selection-only.
JSON carries machine-readable rows.
Closure-C member-wise re-proof is **PENDING** (§9);
nothing here claims unchanged-closure.

## 1. Ownership fixed by ROOT (no new module/schema/family)

1. Canonical DM016 owner: `survey_evidence_v2._source_class`
   (`survey_evidence_v2.py:177-183`, fail-closed `ValueError`,
   no default/classifier). Table `SOURCE_CLASS_MAP:44-109`
   gains exactly 10 rows (§2); old rows UNCHANGED.
   Dead runner table `run_evidence_v2_interactive.py:49-56`
   + leaf `:110-114` delegated-or-removed only after §7 census;
   never a second maintained table.
2. DM017 loss owner: NEW pure
   `find_declaration_loss(root_records, effective_records)`
   + `compute_obligation_universe(...)` in `survey_screening_v2.py`
   (owns `parent_refs`, `PROVENANCE_KEYS:47-48`,
   `validate_discovery:113-183`).
   Separate from unchanged `validate_discovery_expansion:243-322`.
   Input = validated root/effective `list[dict]`;
   output = `list[(parent_id,OID)]`, no authority token.
   `U=P∪named(R)∪named(E)` helper split vs single-home:
   Astra confirms before code. No caller flags, no State recursion.
3. Pre-package helper: NEW
   `resolve_prepackage_root_effective(repo_root,state,profile,`
   `discovery_path,accepted_discovery_path|None)`
   in `survey_screening_v2.py`.
   No dummy package; no resolver call on future path.
   Initial DIRECT/no-marker ONLY when State has no
   accepted-Discovery provenance AND initial window
   (`ISSUE_INITIALIZED` + no `discovery-accepted-v2.json`);
   then supplied Discovery is both R and E.
   If State claims accepted Discovery, missing/mismatch FAILS.
   Never DIRECT fallback. Fixture tolerance is not a bypass flag.
4. Ordinary threading: REQUIRED keyword-only
   `validate_interactive_input(...,*,discovery_records,`
   `root_discovery_records)`
   + `_validate_completeness_input(...,*,discovery_records,`
   `root_discovery_records)` (both `list[dict]`, `None` refuses).
   `_build_completeness(...)` tuple KEEPS.
   Normal builder owns residual union; agent-first `main:79-99`
   becomes thin delegation, keeping pure helpers
   `acceptance_with_canonical_discovery_records:33-52`
   + `completeness_with_preserved_residual_limitations:55-76`.
   No monkey-patching in normal route.
5. HIGH/LOW true R/E: HIGH reloads current canonical State /
   DiscoveryCP / acceptance + Screening package before COPY;
   LOW derives same R/E from pinned before-State COPY +
   accepted refs, never LIVE State. No new request field.
   Typed root CP proof carries role/hash/schema/content;
   no `agent`/`currentState` in LOW.

## 2. Exact current signatures (source-read)

Screening (`survey_screening_v2.py`, top-level ONLY `core:20`):

- `read_jsonl(path:Path)->list[dict]:76`
- `validate_discovery(record:dict,expected_issue_id|None)->list:113`
- `validate_discovery_set(records,issue_id)->None:186`
- `validate_discovery_expansion(repo_root,root_records,`
  `derived_records,issue_id)->dict:243`
- `_canonical_root_acceptance(repo_root,package)->(Path,Path|None):325`
- `resolve_effective_discovery_basis(repo_root,package_path,`
  `implementation_sha|None=None,accepted_root_path|None=None)->dict:353`
- `resolve_active_screening_acceptance(repo_root,state_path,`
  `implementation_sha|None=None)->dict:442`
- `prepare_package(repo_root,state_path,discovery_path,output_dir,`
  `implementation_sha,max_records=50,max_json_chars=120000)->Path:492`
- `_check_screening_package_files_content:629` (State-free)
- `_validate_screening_package_basis_content:654` (State-free)
- `validate_package_basis(...,implementation_sha)->None:695`
- `_resolve_effective_discovery_basis_content(...,root_records|None,`
  `root_path|None)->dict:809`
- `_validate_screening_acceptance_content(...,expectations,`
  `root_records|None=None,root_path|None=None)->dict:859`
- `validate_acceptance(repo_root,acceptance_path,implementation_sha):897`
- `accept_results(repo_root,package_path,results_dir,`
  `accepted_root,implementation_sha)->Path:919`

Evidence (`survey_evidence_v2.py`, top-level `core,schema_gate,screening`):

- `_source_class(source_type:Any)->str:177`
- `task_authority_sources(repo_root,task,package)->dict:413`
- `validate_screening_acceptance(...discovery_path,issue_id,`
  `implementation_sha)->(acceptance,package,discoveries):490`
- `prepare_evidence_package(repo_root,state_path,discovery_path,`
  `screening_acceptance_path,output_dir,implementation_sha,`
  `supplement_manifest_path|None=None)->Path:539`
- `validate_evidence_package_basis:898`
- `_validate_evidence_package_basis_content(...,expectations,`
  `root_records|None=None,root_path|None=None):839`
- `_validate_evidence_acceptance_content(...,expectations,`
  `root_records|None=None,root_path|None=None):1255`
- `_validate_edition_views_acceptance_content(...,expectations,`
  `root_records|None=None,root_path|None=None):1322`
- `_validate_screening_acceptance_content(...,expectations,`
  `root_records|None=None,root_path|None=None):1352`
- `accept_evidence_results(...,implementation_sha)->Path:1159`
- `accept_edition_views(...,implementation_sha)->Path:1829`
- `build_materiality_ledger(...,implementation_sha)->dict:1910`
- `write_materiality_ledger(path,ledger)->Path:2128`

Runner normal (`run_evidence_v2_interactive.py`):

- `_dm022_require_ready(repo_root,state_path)->None:46`
- dead `SOURCE_CLASS_MAP:49-56` + `_source_class:110`
- `_validate_completeness_input(value,profile)->dict:228` CURRENT
- PROPOSED `+ *,discovery_records,root_discovery_records` REQUIRED
- `validate_interactive_input(value,profile,expected_ids,`
  `task_source_ids|None=None)->tuple:272` CURRENT
- PROPOSED `+ *,discovery_records,root_discovery_records` REQUIRED
- `_build_completeness(repo_root,profile,profile_path,`
  `discovery_records,ledger_path,ledger,input_value)->dict:482` KEEP
- `run(repo_root,state_path,input_path,`
  `supplement_manifest_path|None=None)->dict:597`
- Screening runner `validate_interactive_input:42`,
  `run:129` in `run_screening_v2_interactive.py`

Agent-first (`run_evidence_v2_agent_first.py`):

- `acceptance_with_canonical_discovery_records(original,repo_root,`
  `acceptance_path)->dict:33`
- `completeness_with_preserved_residual_limitations(`
  `original,*args,**kwargs)->dict:55`
- `main()->int:79` (patch `:83-91`, restore `:96-99`)

HIGH (`survey_prearchitecture_acceptance_v2.py`):

- `verify_live_eligibility(repo_root,cfg,state)->list:299`
  HIGH-ONLY strict LIVE + exact S3 window
- `_contract_and_tools->(dict,list):437` exact 7-path set
- `prepare_revision(repo_root,state_path,request_path,`
  `revision_id)->dict:456`
- `_exclusive_write_bytes:83` (`O_CREAT|O_EXCL`+`link`+`fsync`)
- `claim_guard:781`, `replace_state_triplet:848`,
  `clear_remaining_exact_slots:896`, `write_cleanup_completion:953`,
  `release_guard:1022`
- `adopt_revision(...,revision_path,decision_path):1064`
- `resume_bound_attempt:1278`, `resume_revision:1374`
- `readback_revision(...,revision_path|None=None):1379` read-only

LOW (`survey_research_authority_v2.py`, top-level ONLY `core+schema_gate`):

- `derive_before_context(repo_root,request_path,before_copy_path,`
  `previous_checkpoint_path)->dict:1172`
- `build_revision_package_from_paths(repo_root,request_path,`
  `before_copy_path,output_dir)->dict:1310`
- `build_revision_cards_views_from_paths(repo_root,package_path,`
  `request_path,results_dir,views_dir)->dict:1458`
- `build_versioned_ledger_from_paths:1675`
- `build_versioned_completeness_from_paths:1795`
- `prove_revision_from_paths(repo_root,revision_manifest_path,`
  `decision_path,before_copy_path)->dict:2002`
- `check_supersession_record_from_paths:2401`
- `guard_path_for:2516`, `lstat_slot:2521`
- `require_no_active_guard(source_root)->None:2561`
- `require_completion_consistent:2602`
- `require_research_operation_ready(repo_root,state_path)->None:2624`

## 3. DM016 table + unknown refusal

Normative 10 (original literals KEEP, old UNCHANGED):

- `PRIMARY_DOC→PRIMARY_OFFICIAL`
- `PRIMARY_REPO→PRIMARY_REPOSITORY`
- `PRIMARY_ANNOUNCEMENT→PRIMARY_OFFICIAL`
- `PRIMARY_MODEL_CARD→PRIMARY_OFFICIAL`
- `PRIMARY_SPEC→PRIMARY_OFFICIAL`
- `SECONDARY_REFERENCE→SECONDARY`
- `SECONDARY_TECHNICAL→SECONDARY`
- `RUNTIME_RECIPE→PRIMARY_OFFICIAL`
- `PACKAGING_DOCS→PRIMARY_OFFICIAL`
- `RUNTIME_PR→PRIMARY_REPOSITORY`

Rejected: conditional classifier, default SECONDARY,
PR-never-primary, URL-sniff `run_special_interactive_evidence:41-47`,
alias/projection ledger, new module, legacy-enum edit,
supplement-SOCIAL expansion.
Enforcement: supplement `:304`, `task_authority_sources:422-423`,
card `:1016/:1020-1028`, LOW `validate_research_record_content:1549`.
Runner dead map has 0 in-file calls (live `:321/:666` use Evidence leaf).
Unknown fail-closed BEFORE any owned/package write.
Screening `source_type` open (`screening:171-173`) so Screening-site
refusal is via new preflight calling canonical leaf function-local.
DROP excluded from tasks (`prepare:601-604`) but still loss-checked.

## 4. BEFORE-read / first-write / prepublish / current-pin

S1 Screening prepare `prepare_package:492-567`:

- BEFORE: `state+cfg+verify_state_basis:501-503`, `profile:506-508`,
  `read_jsonl+validate_discovery_set:509-510`,
  prompt/result `:512-515`; NEW `resolve_prepackage_root_effective`
  (no future package).
- FIRST WRITE: `output_dir/input/batches/*.jsonl:525` +
  `package.json:566` via `core.write_json`
  (`mkdir-p+write_bytes`, check-then-write, NOT `O_EXCL`).
  Non-empty refuse `:517-518`; NEW preflight MUST precede `:517`.
- PIN: entry `ISSUE_INITIALIZED|DISCOVERY_COLLECTED:504-505`,
  no State mutation.

S2 Screening accept `accept_results:919-979`:

- BEFORE: `validate_package_basis:927`
  (profile/discovery/prompt/contract SHA + `state_sha256` +
  `verify_state_basis:695-711`), `_exact_regular_files:929`,
  `_validate_result_batch:935`, dupe/count/digest `:946-956`.
- FIRST WRITE: `accepted_root/<digest>/...:958-977`
  (`copy2+write_json:977`); idempotent re-accept `:953-954`;
  incomplete raises `:956`. NEW preflight before first `copy2`.
- PIN: `validate_package_basis` before copy; no overwrite of complete run.
  Archive `interactive-decisions/audit:88-126` after accept.

E1 Evidence prepare `prepare_evidence_package:539-681`:

- BEFORE: `verify_state_basis:549-550`, `profile:552-553`,
  `validate_screening_acceptance:554-556`
  (`resolve_effective:518-520` + SHA/ID/count `:532-535`,
  binds `state_path:557-558`), supplement `:563-588`.
- FIRST WRITE: temp `tasks/task-*.json:631` + `package.json:680`;
  non-empty refuse `:595-596`.
- PIN: temp-dir only; still unknown-check before authority.

E2 Evidence accept + Views `:1159-1213` / `:1829-1883`:

- BEFORE: reload package + `validate_evidence_package_basis:1167` /
  `validate_evidence_acceptance:1838`
  (screening+evidence+views+SHA `:1412-1434/:1886-1907`);
  `validate_evidence_card:1176` / `validate_edition_view:1850`.
- FIRST WRITE: `evidence/v2/accepted/<digest>:1195-1212`,
  `views/accepted/<digest>:1861-1882`
  (`copy2+write_json`, digest-dir `exists` check, NOT `O_EXCL`).
  Incomplete raises `:1190-1194/:1863-1869`.
- PIN: prepublish `_dm022_require_ready` before each write
  (`run:694,727`). NEW preflight before E1 temp AND E2.

E3 Ledger/Completeness/archive:

- BEFORE: ledger reloads profile+screening+evidence+views
  `:1920-1926`, rows from effective `:1933-1966`;
  `_build_completeness` effective + ledger `run:641-648/771-774`;
  archive byte-compare `:573-594`.
- FIRST WRITE: `materiality-ledger-v2.json:749-761`,
  `profile-completeness-v2.json:764-795`
  (`exists-or-symlink→refuse:749-750`),
  `INPUT/AUDIT:573-594` (`exists→sha-compare→raise`).
- PIN: entry `:748,764` + prepublish `:805`;
  `validate_profile_completeness` override `:781-792` before `:795`.

N1 Normal early preflight (NEW) `run:597-811`:

- BEFORE: `CANDIDATES_NORMALIZED+validate_agent_state:610-614`,
  `_dm022_require_ready:623`, PREARCH refuse `:624-631`,
  `discovery.validate_acceptance` +
  `resolve_active_screening_acceptance:637-640` +
  `resolve_effective(...accepted_root_path=root_discovery_path):641-646`
  holds BOTH `root_records+records`; `profile:616-618`;
  `input_doc:673` in-memory; `task_source_ids:665-672` AFTER package.
- FIRST WRITE: none; gate refuses before E1 temp.
- PIN: canonical `_source_class` per `source_records` incl DROP +
  `find_declaration_loss` per `(parent,OID)` +
  3/5+`U` AFTER `:641-648` BEFORE `:653`.

H1 HIGH `prepare_revision:456-781` / adopt / resume / readback:

- BEFORE: LIVE strict parse `:470-476`,
  `verify_live_eligibility` SAME bytes `:478-480`,
  canonical-State check `:484-489`,
  `require_no_active_guard:495`,
  `_prove_before_graph_unbound` BEFORE first R write `:499`,
  HEAD/tree `:500`, request parse+schema `:502-508`,
  pins LIVE `:515-522`, `before_state` SHA/count `:524-535`,
  COPY `:536-538`, 7-slot COPYs `:563-600`,
  OLD via `before_checkpoint.evidence:541-559`.
- FIRST WRITE: R-owned `revision_root/candidate/**` ONLY via
  `_exclusive_write_bytes:83` (`O_CREAT|O_EXCL`, partial PRESERVED;
  State switch ONLY `replace_state_triplet`).
  NEW DM016+DM017 before R candidate writes.
  Adopt re-verifies before ANY guard/checkpoint/State mutation.
- PIN: `state_path` must be canonical `production-state.json`.
  Resume reuses bound guard/retention/planned bytes
  (`B→switch+clear+complete+release`,
  `E→clear+complete+release`, `ALREADY_ACTIVE`, `INDETERMINATE`).
  `readback:1379` read-only; old readback NOT re-gated.

No blanket all-stage/IO claims: only HIGH uses `O_EXCL`.
Idempotent re-reads (`S2:953-954`, `E2:1191-1192/1864-1865`)
preserve original validity, MUST NOT apply new policy to history.

## 5. Exact 3/5 shapes, no new JSON schema

`P`=Profile initial IDs; `R`=root JSONL `root_records`;
`E`=effective `records`; `U=P∪named(R)∪named(E)`.
Resolver reloads full JSONL (`:375-379/:403-406`,
`accepted_ids==root_ids:408-411`, DIRECT or `:428`).
Compact `parent_edges` NEVER `U`; supplement additive only.
Per-parent rule on actual `parent_refs:list[str]`
(`screening:144-159`): every root `r` + OID `o` needs carrier
as identical DIRECT record OR derived child with
`r.discovery_id∈child.parent_refs` AND `_raw_paths` subset
(`:287-301`) + `_source_identity` rooted + child-subset
(`:303-311`) + DID closure (`:313-318`).
Global OID equality insufficient.
Missing `(parent,OID)` = `DECLARATION_LOSS`: refuse new
preparation/acceptance before writes.
Shared `validate_discovery_expansion:243-322` + detached
`_content` cores + renewal/LOW passive checks stay UNCHANGED;
new policy ONLY at S1/S2/N1/E1/E2/H1.
One `completeness.obligations` array (final 7-field UNCHANGED
`OBLIGATION_KEYS:25-33`):

- `id∈P` → exact 3 `{obligation_id,status,rationale}`
- `id∈U−P` → exact 5 `+{dimension,description}`
  (dimension Profile-declared `_validate_obligation_shape:62-63`,
  description non-empty)
- `id∉U` → refuse

Exact `U` coverage, unique IDs, explicit
`status∈{SATISFIED,LIMITATION,NEEDS_RESEARCH,NOT_APPLICABLE}`
+ non-empty `rationale`. 5 fields on `P` refuses.
No auto-status, no OLD fallback. Old 3-only valid iff `U==P`.
DM022 7-field `fullObligation` stays SEPARATE.
Builder: `discovery_ids` from effective declarations +
`evidence_task_ids` from Ledger rows (profile-only `[]`);
DROP no invented tasks.
Thematic `closure` 8 fields ALL from provenance
(`completeness:81-142`, `_build_completeness:527-556`):

- `expansion_passes=max(1,max_pass)`
- `final_pass_new_sources=len(final_records)`
- `final_pass_new_material_obligations(_open)`
- `targeted_gap_fill_completed/limitations/status`
  (`COMPLETE/LIMITED/NEEDS_RESEARCH`)

Residual union STABLE: `list(input.residual)` then append missing
`closure.limitations` in order (adapter `:66-69`);
folded into normal builder so direct==agent-first.
`SOURCE passes` fixtures never satisfy counters.

## 6. DM022 true R/E repair (all LOW+HIGH, no new field)

Gap: request Discovery treated as DIRECT; HIGH postwrite
`None,None` at `prepare:677,682`.
Repair: HIGH prepare/adopt/resume/readback + LOW
`derive_before:1172`, `package:1310`, `cards:1458`,
`accept:1550`, `ledger:1675`, `completeness:1795`,
`prove:2002` (FULL checks `:2172-2196` pass
`discoveries,disc_abs` as `root_records,root_path`),
`check:2401` must receive TRUE validated root context.
Chain WITHOUT new schema: pinned COPY bytes==
`request.before_state.sha256/byte_count:1197-1203` →
COPY triplet==`request.before_checkpoint:1207-1215` →
`load_typed_checkpoint_record:1205-1206` →
`profile/discovery/screening` live re-hash `:1227-1236` +
`prove:2126-2138` → `read_jsonl+validate_discovery_set:1247-1255` →
`screening_doc` + non-DROP allowlist + `records` cover `:1256-1272` →
OLD 4-artifact graph `:1273-1297`.
LOW historical true R/E: `beforeState COPY→DiscoveryCP→`
`accepted artifact→canonical RootJSONL` + `Screening package E`
via existing paths.
Crossbind: `request.discovery_ref==E`,
`request.screening_ref==selected old Screening`;
no `inputRoot` dict/alias/old-State fake; logical State paths
stay canonical, COPY supplies bytes.
Typed root CP proof (role/hash/schema/content,
no `agent`/`currentState` in LOW):
`load_typed_checkpoint_record:310` +
`_verify_own_epoch_commit:620` (own-epoch Contract8,
never LIVE/HEAD==epoch) + `_verify_adopted_graph_full:783` +
`_verify_completion_full:914`.
Retain old DIRECT valid; DERIVED positive MUST full
content proof (`:851-856` + `:428`), not current-policy history.
Resume = already-admitted bound intent only; readback detached.
Missing R authority → exact gap to Astra, no schema change.

## 7. Caller census (shipping only; DATA excluded)

`validate_interactive_input`: prod 1 (`run:674-676` positional today
→ keyword+2 REQUIRED); test 1
(`tests/test_run_evidence_v2_interactive.py:101-106` same migration);
DATA 1 (edition-local, DO NOT UPDATE).
Internal `_validate_completeness_input` caller 1 (`:309`).
`_build_completeness`: prod 1 (`:767-775` KEEP),
adapter wrapper 1 (`agent_first:88-91`), DATA 1 (DO NOT UPDATE).
Adapter also patches 2 helpers (`:80-99`);
`ALLOWED_HELPERS` lists only screening+evidence
(`survey_agent_tool_v2.py:36-39`, agent-first via `runpy`).
Agent-first pure helpers directly tested:
`tests/test_run_evidence_v2_agent_first.py:54,82`
(`acceptance_with_canonical...`) + `:96,111`
(`completeness_with_preserved...`).
Screening `prepare_package`: `cmd_prepare:1005`,
`run_screening:164`, tests `test_survey_screening_v2:150,209,235,287`,
`test_survey_screening_archive_v2:25`,
`test_survey_evidence_v2:117`,
`test_survey_drafting_basis_v2:159,641`,
`test_screening_expansion_authority_v2:169`,
`test_dm022_g71_g76_compatibility_v2:208`.
Evidence `prepare_evidence_package`: `run:653`,
tests `test_survey_evidence_v2:245,354,671`,
`test_screening_expansion_authority_v2:214`,
`test_dm022_g71_g76_compatibility_v2:219`,
`test_survey_longform_derivation_v2:213`,
`test_survey_screening_archive_v2:56`.
`accept_evidence_results/accept_edition_views`: `run:696,729`,
tests `test_survey_evidence_v2:259,308,366,368`,
`test_dm022_g71_g76_compatibility_v2:228`,
`test_survey_longform_derivation_v2:225`.
LOW/HIGH: HIGH `prepare:603,618,686,695` calls LOW builders;
`adopt:1140` calls `prove_revision_from_paths`;
DM022 fixtures `dm022_*_v2.py` are HIGH/LOW scope.
Any extra driver found in diff returns to Astra.

## 8. Import/digest/closure/current-vs-history (summary)

Surface is existing Evidence, Screening, normal interactive,
agent-first, HIGH + LOW pure helpers, tests/docs only.
No new module/schema/family ID.
`survey_evidence_v2:21` top-level `screening` already closed;
Screening→Evidence preflight MUST be function-local
(`screening:397` precedent), never top-level cycle.
LOW keeps ONLY `core+schema_gate:48-49`; HIGH keeps
`core+schema_gate+low` + function-local `agent:312,466`.
Staged/canonical closure correction (gate §1) needs parallel C
member-wise proof; **PENDING — not claimed closed**.
G76 needs own-epoch + CURRENT re-derivation + exact76 +
member-wise equality + fresh CURRENT proof;
unchanged-closure NEVER presumed; counts not authority.
History readback stays under accepted contract;
new eligibility never leaks into historical validators.

## 9. Oracles + route limits (planning only, NOT executed)

Positive: all 10 types via actual v2 task/card; unchanged old;
many-to-many per-`(parent,OID)`; initial-only `U==P` 3-field
all 3 Profiles (WEEKLY `2026-W35` null, THEMATIC `SP001` 3→8,
RETRO `SP-2025-H2` null); GAP_FILL + `REFERENCE_EXPANSION` +
5-field derived DIDs/taskIDs; direct==agent-first byte-equal +
residual order; LIMITED residual-subset full validators;
HIGH prepare+adopt re-verified.
Negative pre-write: unknown incl DROP; `(R2,O1)` loss despite
global equality; dup/missing/extra/undeclared-dim/empty-desc/
5-on-initial/7-field/auto-status; `NOT_APPLICABLE` explicit;
late drift caught; `SOURCE passes` refused.
Limits: non-four-family/Retro reader REQUIRED follow-on;
manual `DIRECT_PRIMARY/PRIMARY_ONLY` byte-hash only,
post-VALIDATED republication `UNSUPPORTED_ROUTE`;
custom-period `--spec` sufficient; DM022 `research_profile`
`WEEKLY/THEMATIC` only this unit; multi-DID/multi-source
ambiguous-primary refused; old history valid, new loss refused;
epoch drift `INDETERMINATE` preserve, no auto-rollback;
no full-suite/test-count sum.
Any essential contradiction (missing R authority, required
schema/interface, unmapped driver) returns to Astra NOT_READY.
Independent readiness + final Astra confirmation required.
Stop at Human Commit Point; quality/audit/adoption/savings OPEN.

(End — R2 integrated map; C re-proof PENDING; no author PASS.)
