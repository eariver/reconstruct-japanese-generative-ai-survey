# Profile/support integrated readiness R4 — delta closing RB1–RB7 (docs/source-read ONLY)

2026-10-31. **WORKING DELTA FOR REVIEW. No author PASS. No implementation. No code authorization.**
Delta to R3 `integrated-readiness-r3.md/json` + focused kernel `detached-root-context-map.md/json`
(both preserved unchanged as history). Binds ROOT working gate FULL including §6
`notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md`
SHA256 `da37cb8dcf931377075ef01219539206c4fa5f447589f6cb2d7bd74150dbb544` /13968B
(§§1–6; §§1–5 unchanged, §6 new). No runtime/import/tests/build/fixtures/network/Git/readback.
Source READONLY `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
actual409/tree8ce +133paths54M79A/768 files. No source or old-report edits. New files ONLY:
this md + `integrated-readiness-r4.json` (multiline readable, data-only; stdlib hash only, no project imports).

Normative FULL pins (copy byte-exact from ROOT §6; C2 headers wrong, never authority):

- Decision FULL `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d` /20472B INCLUDING §7.
- ROOT contract FULL `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a` /7225B INCLUDING §5.
- Patch FULL `25b488784d02a156db693459dce6c1d369e7144f1c49461c9b3a846b1b7260` /4931836B (ROOT §6; do not drop `714f`; prior truncated forms not authority).
- Baseline `774dd39a951c9ac3818e83dfffd4f7666efb0a20` (ROOT §6; 40-hex commit, not SHA256).
- Manifest FULL `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` /185422B.
- Focused kernel `detached-root-context-map.md` SHA256 `6d80ffeb72e15637573b50e0421b12853ab8bbd33995f981ff518bef516e3df5` /18627B,
  `.json` SHA256 `fac3e0e33be61bac49f447687a5f1bfee6521176f86ec97300cbad7df2ace199` /10130B
  (byte-preserved move from contract dir; supporting work, not yet approved).
- R3 `integrated-readiness-r3.md` 69124B + `.json` 32572B preserved; this R4 corrects RB1–RB7 without editing them.

ROOT §6 binds corrections to the focused kernel as well. R3 claim “all closed” is WITHDRAWN;
R3 remains NOT_READY per RB1–RB7. This R4 supplies the exact delta; independent readiness must still
close it. No Commit Point declared by author.

## RB1 — Ordinary DCP/SCP proof (no LIVE Screening validators in LOW)

R3 §4 + kernel §2 shared the error: R3 pure chain still cited public
`survey_screening_v2.validate_acceptance:897-916` / `resolve_effective_discovery_basis:353-439`
(and kernel §4 propagated `(*,root_records,root_path)` caller kwargs into public LOW).
ROOT §6: public `validate_acceptance`, `resolve_effective_discovery_basis`,
`resolve_active_screening_acceptance:442-489` are LIVE-bound and FORBIDDEN in LOW.
LOW uses only explicit `_content` siblings; ordinary Discovery acceptance validator is separately
verified state-free.

Actual source predicates (text-read):

- `survey_discovery_v2.validate_acceptance:274-298` is state-free and MAY be used:
  `load_and_validate_json` vs `DISCOVERY_ACCEPTANCE_SCHEMA`; `x_ref` SHA drift `:279-281`;
  `cfg=load_json(DEFAULT_CONFIG)` from disk (policy/drive only); `x_intake.validate_manifest:283`
  (itself state-free `:344-398`, never `verify_state_basis`/checkpoint/pending); issue match `:284-285`;
  `discovery_path` SHA `:286-288`; `read_jsonl+_normalize_record:84-153`; `_validate_graph:156-172`;
  `_validate_x_integration:179-201`; `record_count/records/graph_sha` equality `:294-297`.
  No State load, no `verify_state_basis`, no `agent.*`, no HEAD.
- `survey_screening_v2.validate_acceptance:897-916` is NOT state-free: calls
  `validate_package_basis:695-711` (loads State, `sha256(state)==basis.state_sha256`,
  `verify_state_basis`, identity divergence) + `resolve_effective_discovery_basis:353-439`
  (via `_canonical_root_acceptance:325-350` which `load_json(basis.state_path)` LIVE + derives
  `source_root` from live Profile). Same for `resolve_active_screening_acceptance:442-489`
  (`agent.resolve_checkpoint_artifact` + `verify_state_basis` + override). MUST NOT be used in LOW.
- LOW content-only reuse (explicit `expectations`, no State):
  `_validate_screening_package_basis_content:654-693` (§11.3 path-identity
  `basis.state_path==canonical_state_path`, file SHA drift, profile-identity via file never live
  State, never `verify_state_basis`, never SHA-compare live/retained);
  `_check_screening_package_files_content:629-651`;
  `_check_screening_batches_and_digest:767-806` (pure batch/count/digest, `run_dir.name==digest`);
  `_resolve_effective_discovery_basis_content:809-856`
  (pure `validate_discovery_set` + `validate_discovery_expansion:243-322` only,
  never `_canonical_root_acceptance`, never checkpoint/override);
  `_validate_screening_acceptance_content:859-894`
  (`expectations={issue_id,research_profile,canonical_state_path}`, package copy
  `==package_sha256`, basis content, identity, batches/digest, pure effective basis);
  `evidence._validate_evidence_acceptance_content:1255-1283`,
  `evidence._validate_edition_views_acceptance_content:1322-1349`,
  `evidence._validate_materiality_ledger_content:2056-2099`,
  `completeness._validate_profile_completeness_content:241-262`.
- Ordinary DCP/SCP carry record-owned Contract8 (recomputed `core.contract_identity:210-228`
  equality `:713-717`, never PREARCH 7-file Git proof `:620-780` which is PREARCH-only
  `_MAPPED_DM022_CODESET:568-580` + `_verify_own_epoch_commit` + `_verify_adopted_graph_full:783-911`
  + `check_supersession:2401-2513` + agent PREARCH branch). Preserve existing record-owned report
  equality `_artifact_map(report.artifacts)==_artifact_map(record.artifacts):727-731` and historical
  canonical-State-path-only predicates (`production_state` canonical path only when
  `state_path is None:710-712`, no live SHA), rather than imposing the PREARCH seven-file Git proof.
- Historic 12 keys exact (not 13): `schema_version,check_id,status,issue_id,from_state,to_state,
  production_state,production_profile,implementation_commit_sha,contract,artifacts,recorded_at`
  (`:680-686`); `2.0-rc1/CORE_STAGE_CONTRACT/PASS:687-688`; lifecycle/issue/from/to vs
  `historical_state.lifecycle_state=from_state:689-697`; `production_profile=={path,sha256}:698-701`;
  `production_state` live `{path,sha256}` equality if `state_path is not None:705-708` else
  canonical-path-only `:710-712`; `contract:713-717`; `implementation_commit_sha:718-722`;
  `recorded_at:723-726`.

R4 rule: LOW root loader (§4) calls ONLY Discovery state-free validator + Screening/Evidence
`_content` cores with explicit `expectations={issue_id,research_profile,canonical_state_path}`
derived from COPY/request (not caller flags). Never calls public Screening validators.

## RB2 — DCP/SCP/ECP + Profile binding + exactly-1 CORE review + file-vs-digest

- DCP = `COPY.checkpoint_provenance.discovery` `{path,sha256}`; SCP = `COPY.provenance.screening`
  same shape. Both must exist as FULL CP (DM022 strict `EVIDENCE_REVIEWED` before-State always
  passed D/S, so no initial fallback, no schema fallback, no caller Scan marker/prov reinterpretation).
  Family LEGACY only at DCP/SCP; `load_typed_checkpoint_record:310-355` PREARCH at DCP/SCP refuses
  `DM022_WRONG_FAMILY`. Unknown kind refuses (no `.get(kind,legacy)` coercion).
- ECP = previous evidence checkpoint (`request.before_checkpoint.evidence` ArtifactRef +
  COPY `checkpoint_provenance.evidence`). ECP `prior EVIDENCE != DCP`: removing a redundant supplied
  ECP path is allowed ONLY if the same ECP is derived from `before_checkpoint.evidence`/COPY evidence
  provenance, never from Discovery provenance. DCP artifact is `discovery-acceptance` NamedRef;
  ECP artifact set is `evidence-acceptance/edition-views-acceptance/materiality-ledger/profile-completeness`
  (LOW `derive_before_context:1273-1297`, HIGH `prev_record` 4-artifact check). Never conflate.
- Full Profile binding: `request.profile_ref{path,sha256,byte_count}` SizedRef must equal
  before-State Profile (`_load_json_from_sized:1165-1169` + `_verify_sized_ref_bytes:278-288` +
  `profile.issue_id==COPY.issue_id`, `research_profile==COPY.research_profile`, contract shape;
  `profile_ref` rehash + `request.work.expected_head/tree` returned opaque, never re-observed here;
  HEAD observation is HIGH-only `_current_head_tree`).
- Exactly one CORE review means one matching row, not a ban on additional schema-valid review rows:
  `matches=[row where check_id==CORE_STAGE_CONTRACT]; require len(matches)==1:665-667`
  (`kind==DETERMINISTIC + status==PASS:669-670`); other `kind==DETERMINISTIC` rows retain their
  result `{path,sha256}` rehash checks `:878-890`. PREARCH branch (`:619-664`) distinct:
  exactly one `DM022_SUPERSESSION_PROOF` SizedRef `{path,sha256,byte_count}:631-644`, never mixed
  `CORE+PREARCH:662-663`. All deterministic result refs retain file rehash + drift checks.
- FILE SHA vs result-set digest (never equate): Screening acceptance FILE SHA
  (`sha256(acceptance_path)`) equals its selected NamedRef/request SizedRef SHA
  (`SCP artifact{path,sha256}` / `request.screening_ref.sha256` + `_verify_sized_ref_bytes` +
  `S_accept.result_set_sha256` basis check); `result_set_sha256` is a separate recomputed
  result-set digest (`_screening_acceptance_digest` / `_result_set_digest:757-764`) and run-directory
  identity (`run_dir.name==digest`). Same for Evidence/Views (`_evidence_result_set_digest`,
  `_view_set_digest`, digest-named run dirs HIGH `:645-671`). Never equate file bytes hash with
  recomputed set digest.

## RB3 — (folded into RB1/RB2/file-vs-digest; no separate HIGH 3/5 gate)

Covered by RB1 content-core allowlist + RB2 profile/ECP/file-vs-digest predicates. No separate change.

## RB4 — Public LOW PATHS-only (REJECT kernel optional dict kwargs; no None-DIRECT)

Kernel §4 wrongly adds `(*,root_records,root_path)` / `(*,effective_records,effective_path)`
optional kwargs to public `*_from_paths`. ROOT §6 REJECTS: public LOW `*_from_paths` remain
path-reloading. Do not add caller `root_records/root_path` as permission-bearing optional context.
They may derive an internal full context once and pass it only through private pure helpers.
Complete path signatures + private helper inputs + all forwarding sites must be explicit.
Optional root context must not silently revive E-as-R. No `root None` means DIRECT fallback;
ALL per-site expressions pass actual R/`root_path` vs E separately.

Contract extension (precise, ROOT decision required before code — not implementer choice):

NEW public (PATHS-only, no dict kwargs, no permission token):

- `derive_ordinary_root_effective_context(repo_root: Path, request_path: Path, before_copy_path: Path) -> dict`
  LOW history COPY-only. Algorithm kernel §3.1 steps 1–10 (request pin → COPY sha/byte_count →
  COPY parse + State/Profile shape only → before_checkpoint==COPY provenance →
  DCP/SCP ArtifactRef existence → file rehash + `load_typed_checkpoint_record` LEGACY-only →
  DCP/SCP LEGACY validation per RB1/RB2 (producer `ISSUE_INITIALIZED→DISCOVERY_COLLECTED` /
  `DISCOVERY_COLLECTED→CANDIDATES_NORMALIZED` from disk cfg stage_plan, `issue_id`, checkpoint
  membership, one `discovery-acceptance`/`screening-acceptance` NamedRef, one CORE PASS + historic
  core-report with `state_path=None` canonical-path-only, `contract==record.contract`,
  `impl==record.implementation.repository_commit_sha`) → DCP `discovery.validate_acceptance`
  (state-free) → `root_path/root_sha/root_records(read_jsonl+validate_discovery_set)` →
  SCP `_validate_screening_acceptance_content(expectations,root_records,root_path)` (CONTENT only) →
  `effective_*` + bind `request.discovery_ref==E` + `request.screening_ref==SCP artifact` →
  `profile_ref` SizedRef load + cross-check → return data-only context (list in R4 JSON
  `context_returns`; no writes/guard/State/agent/PREARCH-proof/completion/future-COPY).
- `derive_current_root_effective_context(repo_root: Path, request_path: Path, live_state_path: Path) -> dict`
  HIGH-only, called AFTER `verify_live_eligibility:299-357` and BEFORE first COPY `:538`.
  Reads LIVE `live_state_path` (=`request.before_state.path`, `sha==request.before_state.sha256`,
  `len==byte_count` verified by HIGH strict State, not LOW) as DATA; loads COPY-equivalent provenance
  from that LIVE dict + DCP/SCP files; calls shared private kernel with internally loaded State/prior-CP.
  LOW history never uses this. Shared kernel accepts data; permission comes from HIGH eligibility
  vs LOW COPY pin — kernel itself confers none.
- `resolve_prepackage_root_effective(repo_root: Path, state_path: Path, discovery_path: Path, accepted_discovery_path: Path | None) -> dict`
  Ordinary S-prepare loader (R3 §6.2 corrected per RB6 below). PATHS-only; derives canonical
  marker + State provenance on its own; optional path is expected binding only, never caller selector.

Private (internally derived Context, no authority token):

- `_derive_root_effective_kernel(*, repo_root: Path, before_state: dict, canonical_state_path: str, dcp_record: dict, scp_record: dict, request: dict, profile_doc: dict, root_records: list, root_path: Path) -> dict`
  Pure computation on already-loaded dicts/bytes (CONTENT validation, expansion accounting,
  request binding, map building per kernel §3.2 steps 7b–10). Both public loaders call this kernel
  (no logic fork). Accepts own-loaded data; callers must already hold validated LIVE (HIGH) or
  COPY (LOW) authority.

Existing public `*_from_paths` KEEP original positional PATHS signatures; add keyword-only
`*, before_copy_path: Path | None = None` ONLY where missing (derive from request/manifest refs
if possible, else refuse — never DIRECT fallback, never E-as-R):

- `derive_before_context(repo_root, request_path, before_copy_path, previous_checkpoint_path)` KEEP
  4-positional (compat); `previous_checkpoint_path` derived from `COPY.provenance.discovery` evidence
  ref when caller passes `None`/omits? No — preserve exact 4-arg; new public loader above is the
  preferred path. Old function internally delegates to kernel (no caller dicts).
- `build_revision_package_from_paths(repo_root, request_path, before_copy_path, output_dir)` KEEP
  (already has before_copy; no new kwarg).
- `build_revision_cards_views_from_paths(repo_root, package_path, request_path, results_dir, views_dir, *, before_copy_path: Path|None=None)` ADD keyword-only; when `None`, derive
  `before_copy = repo_root / manifest?request.before_state?` No — cards stage has no manifest;
  derive from `request.before_state.path`? Cannot (logical path, not COPY). So when `None`,
  require caller (HIGH prepare) to pass retained `state-before.json` COPY path explicitly
  (`rev_root/retention/state-before.json`); else refuse. Internally calls
  `derive_ordinary_root_effective_context(repo_root,request_path,before_copy)` once, then private
  `_build_cards_from_context(*, package, request, profile_doc, effective_records, effective_path)`.
- `accept_revision_evidence_views_from_paths(repo_root, package_path, results_dir, views_dir, profile_path, evidence_accepted_root, views_accepted_root, *, request_path: Path|None=None, before_copy_path: Path|None=None)` ADD two keyword-only PATHS;
  when `None`, derive `request_path` from HIGH manifest `request` SizedRef? No — accept stage runs
  under HIGH prepare with `request_abs` in scope; HIGH passes both explicitly. Refuse if absent.
  Forwards true `root_records/root_path` to `evidence._validate_evidence_acceptance_content` /
  `_validate_edition_views_acceptance_content` `root_records/root_path` params (`:1255-1283,:1322-1349`);
  never `None,None` in new-operation path; historical `_content` revalidation keeps `None,None`
  only in detached history branches (provenance: idempotent re-reads `S2:953-954/E2:1191-1192`).
- `build_versioned_ledger_from_paths(repo_root, profile_path, discovery_path, screening_acceptance_path, evidence_acceptance_path, views_acceptance_path, *, request_path: Path|None=None, before_copy_path: Path|None=None)` ADD keyword-only PATHS;
  HIGH passes both; internal `derive_ordinary...` once → private `_build_ledger_from_context` →
  `_validate_materiality_ledger_content:2056-2099(...,root_records,root_path)`.
- `build_versioned_completeness_from_paths(repo_root, profile_path, discovery_path, screening_acceptance_path, evidence_acceptance_path, views_acceptance_path, ledger_path, request_path, old_completeness_path, *, before_copy_path: Path|None=None)` ADD keyword-only;
  `request_path` already positional; HIGH passes retained COPY; internal derive once →
  `_validate_profile_completeness_content:241-262(...,root_records,root_path)`.
- `prove_revision_from_paths(repo_root, revision_manifest_path, decision_path, before_copy_path)` KEEP
  (already has before_copy). Internally derives OLD context via public loader on
  `manifest.request` + retained COPY (OLD before-graph) and validates NEW graph via FULL content cores
  with that R/E (NEW proposed-graph); separate contexts, no new DM016/DM017 policy in either
  historic pass (classification/loss are HIGH new-admission gates, not retrofitted validators).
- `check_supersession_record_from_paths(repo_root, checkpoint_path, report_path, before_copy_path)` KEEP
  4-positional (already path-only). When `before_copy_path` is a placeholder/derived?
  Derive rule: if caller holds checkpoint with `retention_plan{path,sha256,byte_count}` +
  `revision_root`, `before_copy = repo_root / revision_root/retention/state-before.json`
  (immutable path bound `before_state`: `copy_target==retention/state-before.json` +
  `sha==manifest.before_state.sha256` + `_verify_sized_ref_bytes` on `checkpoint.retention_plan`).
  Allows `check_*` to load before-derived context with no recursive old-4-graph (below).
- `_verify_adopted_graph_full(repo_root, checkpoint_path, checkpoint_sha, *, before_copy_path: Path|None=None)` ADD keyword-only PATH (not `root_records` dicts);
  when `None` in LOW adopted path, derive `before_copy` from `checkpoint.retention_plan/revision_root`
  immutable path bound `before_state` (same rule as `check_*`); when called from HIGH postread
  (`:974-994` triplet + FULL recompute) keep existing 2-arg behavior (no new context).
  Returns existing dict shape.

No `root None` means DIRECT fallback: in ALL new-operation expressions, `root_records is None`
refuses; DIRECT is an explicit `mode==DIRECT` with `derived_path.resolve()==root_path.resolve()` +
`sha equal` (per `:413-426` / content `:851-854`), never a `None` default. Historical
`_resolve_effective_discovery_basis_content(root_records=None,root_path=None)→DIRECT` branch
(`:837-843`) stays history-only for legacy direct-basis unit fixtures, never used by new loaders
(which always pass explicit R).

Adopted-full before-COPY derivation + cycle avoidance (no recursive old-4-graph):

- `check_supersession` / `_verify_adopted_graph_full` derive `before_copy` ONLY from
  `checkpoint.retention_plan{path,sha256,byte_count}` (SizedRef verified via
  `_verify_sized_ref_bytes`) + `record.revision_root` immutable path
  (`f"{revision_root}/retention/state-before.json"` bound `before_state.sha256/byte_count`).
  Then call `derive_ordinary_root_effective_context(repo_root, manifest.request_path?, before_copy)`
  where `request_path` is `record.request.path` (manifest `request` SizedRef, verified bytes).
- Context root loader loads ONLY D/S (DCP/SCP LEGACY + Discovery/Screening acceptances + profile
  binding). ECP (previous `evidence-acceptance` etc.) metadata is file existence + SHA only
  (`_artifact_ref_shape` + `_safe_read_bytes` + `sha==ref.sha256`); it does NOT call full
  adopted-graph/completion verification. Finite previous-PREARCH lineage allowed with existing
  bounded cap (exactly the stored `parent_checkpoint/original_anchor/supersedes` chain already
  enforced by `check_supersession:2401-2513`; no new recursion). Forbidden cycle:
  context loader → `adoptedFull` → context loader. R4 forbids: context loader never calls
  `_verify_adopted_graph_full` / `check_supersession` / `prove_revision_from_paths`;
  adopted-full/completion call context loader (one direction only).

Per-site R vs E expressions (all pass actual R/`root_path` vs E separately, never E-as-R, never None):

- Package/tasks: `_resolve_effective_discovery_basis_content(repo_root,package_path,package,root_records,root_path)` +
  `validate_discovery_set(root_records)` + tasks from `effective_records` non-DROP allowlist.
- Cards/views: `build_research_card_content(...,task,meta,package,record,runner)` with
  `record` from `request.records` bound to `effective_records` DIDs + `task_authority_sources`
  leaf per `source_records`; `validate_evidence_card(card,task,meta_sha,package)` +
  `validate_edition_view(view,profile,evidence_sha,status)`.
- Acceptances: `_validate_evidence_acceptance_content(repo_root,ev_path,expectations,root_records,root_path)` +
  `_validate_edition_views_acceptance_content(...,root_records,root_path)` with
  `expectations={issue_id,research_profile,canonical_state_path=request.before_state.path}`.
- Ledger: `_validate_materiality_ledger_content(...,root_records,root_path)` (basis SHAs + row linkage).
- Completeness: `_validate_profile_completeness_content(...,root_records,root_path)` (obligation/closure recomputed, not hash-only).
- Prove/check: OLD context (manifest.request + retained COPY) vs NEW graph (same R/E via FULL cores);
  `retention_plan` bound to stored manifest; `contract/implementation/profile/lineage` cross-checked.

## RB5 — HIGH seven-field only, never ordinary 3/5

HIGH preflight uses DM022 existing seven-field request (`dm022-revision-request-v2.schema.json`
`fullObligation:232-244` `minLength:1` + LOW fallback `:1886-1897` dead under schema-first
`load_revision_request`), never the ordinary 3/5 gate (`validate_interactive_input` /
`_validate_completeness_input` 3 vs 5 + `U` in normal runner N1 only). HIGH checks before first
COPY: canonical `_source_class` per R `source_records` incl DROP + per-parent preservation
`find_declaration_loss(root_records,effective_records)` on R effective basis (decision §§3–4).
Ordinary 3/5 stays in normal runner; DM022 7-shape unchanged (`request/manifest/proof/report/
checkpoint/guard/completion` SizedRef/ArtifactRef sets unchanged).

R3 §6.4 wording “3/5/U shape” for HIGH is WITHDRAWN; R4 corrects to 7-field eligibility.

## RB6 — Ordinary prepackage Paths-only + marker truth table + mode split

NEW helper (contract extension, PATHS-only):

`resolve_prepackage_root_effective(repo_root: Path, state_path: Path, discovery_path: Path, accepted_discovery_path: Path | None) -> dict`

- Takes Paths and derives canonical marker + State provenance on its own (loads State/Profile,
  `verify_state_basis` via caller-checked facade same as `prepare_package:501-503`, marker file
  `source_root/discovery/discovery-accepted-v2.json` via `_repo_file`-equivalent no-follow checks).
  Optional `accepted_discovery_path` is expected binding only (must equal canonical marker when
  marker present: `resolve(expected)==resolve(canonical)` + `sha==canonical_sha` + `validate_acceptance`
  bytes equality), never a caller selector that suppresses a present canonical marker or overrides
  State provenance. If marker present and optional path differs/missing → refuse.
- Returns FULL dict (R3 §6.2 keys) with `mode` SPLIT (ROOT §6): `authorityKind: "NO_MARKER" | "STAGE_CLAIMED" | "CANONICAL_MARKER"` + `basisMode: "DIRECT" | "DERIVED_EXPANSION"` (not ambiguous `ACCEPTED_BOUND`).
  `authorityKind` = marker provenance; `basisMode` = `derived_path.resolve()==root_path.resolve()+sha equal→DIRECT` else `DERIVED_EXPANSION` via `validate_discovery_expansion` (same predicates `:413-439` but without future package).
- Truth table (actual `lstat`/State/DCP predicates; no stronger Stage gate invented):

  | Row | State lifecycle | Marker `source_root/discovery/discovery-accepted-v2.json` | Supplied Discovery | Result |
  |---|---|---|---|---|
  | R1 noMarker initial | `ISSUE_INITIALIZED` | `lstat` ENOENT (absent; `is_file()==False`, no symlink) | `read_jsonl+validate_discovery_set` passes, `issue_id` matches | `authorityKind=NO_MARKER`, `basisMode=DIRECT`, `root_records==records==supplied`. Preserves existing initial preparation. |
  | R2 marker exists initial pending (supported) | `ISSUE_INITIALIZED` | present regular file + `discovery.validate_acceptance` passes + SHA/ID/count binds | supplied validated (may equal root or DERIVED with valid expansion) | `authorityKind=CANONICAL_MARKER`, `basisMode=DIRECT or DERIVED_EXPANSION` per bytes; run unknown+loss+U. Keeps marker-exists-initial-pending support: actual src fixture `test_screening_expansion_authority_v2:156-169` writes appropriate bound marker file (fixture authority, not State-passed claim). No new lifecycle requirement beyond existing `ISSUE_INITIALIZED\|DISCOVERY_COLLECTED:504-505`. |
  | R3 malformed/symlink/unreadable | any | symlink / nonregular / unreadable / strict-parse fail / schema fail | any | NEVER fallback to DIRECT; refuse (`symlink→refuse`, `nonregular→refuse`, `unreadable→refuse`). Distinguish absence (ENOENT) from malformed/unreadable. |
  | R4 Stage-claimed DCP missing | `DISCOVERY_COLLECTED` or State `checkpoint_provenance.discovery` present (Stage claims DCP) but marker file absent | ENOENT while Stage claims DCP | any | REFUSE (`Stage claimed DCP missing fails`); never DIRECT fallback. DCP claim comes from State provenance / `resolve_active` authority, not caller dict. |
  | R5 claimed-but-different | any | present but `supplied` bytes ≠ bound root when DIRECT expected, or DERIVED without valid expansion; or optional expected path ≠ canonical marker | any | REFUSE; caller `allow_unbound` FORBIDDEN. |

  State/Profile/marker/checkpoint-reference provenance are different facts; map states exactly which
  original predicates authorize each row (lifecycle + `verify_state_basis` + Profile identity +
  marker `validate_acceptance` + JSONL SHA/ID/count/schema). Marker existence alone never authorizes;
  lifecycle alone never authorizes; State-passed claim never substitutes for bound marker file.

## RB7 — Closure 4+1+3 + C-R2 arrays + lazy imports + control binding

R3 §5.2 heading “4 operator fields” is WITHDRAWN. ROOT §5 formulae control. Correct heading:
four provenance/status-derived counters, one row-status count, three operator-fed fields
(including the limitations union):

- Provenance/status-derived 4: `expansion_passes=max(1,max_pass)`, `final_pass_new_sources=len(final_records)`,
  `final_pass_new_material_obligations=len(material_ids)`, `final_pass_new_material_obligations_open=len(open_ids)`
  (`survey_completeness_v2:101-141` + `_build_completeness:527-546`; `material_ids` filtered by
  `MATERIAL_OBLIGATION_STATUS`, `open_ids` by `NEEDS_RESEARCH`).
- Row-status count 1: `open_material_obligations=needs_research` (total NEEDS_RESEARCH rows).
- Operator-fed 3: `targeted_gap_fill_completed:bool`, `status∈{COMPLETE,LIMITED,NEEDS_RESEARCH}`,
  `limitations` (closure-input order first, then missing residual in residual order per adapter
  `:66-69`; R3 §5.1 order retained). Judgment cross-checked `:2184-2243` (overall + expected_closure +
  finish/zero-open/COMPLETE-empty/LIMITED-nonempty/residual-subset). No autostatus.
- HIGH only 7 input (RB5) + 8 closure heading above (not R3 incorrect heading).

C-R2 exact arrays tied to R4 full-hash correct refs (metadata, not new code):
`source-family-closure-map-r2.md/json` member-wise arrays (`_SHARED_PY_G71` 35 entries `:103-139` +
`_DM022_PY_2` `:92-95`, `_OLD_PY_30/_OLD_SCHEMAS_14/_NEW_PY_3/_NEW_SCHEMAS_4/_NEW_DM022_MODULES_2/
_NEW_DM022_SCHEMAS_5/_FAMILY_PY_2/_FAMILY_SCHEMAS_4`, `_KNOWN_*`, `_OLD_PIPELINE_67`,
`_DM022_SCHEMA_IDS`, `_route_code_deps:217-249`, staged 37py+27sch, union 70, pipeline 76,
canonical 36/41, DM022 mapped 7) are referenced with R4 FULL patch/manifest/baseline/decision/ROOT
hashes in R4 JSON `closure_arrays_ref` (correct source refs; arrays themselves unchanged from C-R2).
Helper new lazy imports within existing sets/current-proof code changes retained:
Evidence/Screening/Completeness function-local only (precedent `:397`, HIGH `:465,:616,:673`,
LOW `:1887,:1322`), top-level unchanged (`screening:core` only, `evidence:core,schema_gate,screening`,
LOW `core+schema_gate` only). Outside-driver control binding exact paths:
`implementation_control_roots=[config,schemas,scripts,.github/workflows]` +
`_verify_head_bytes`/`verify_tool_basis` ancestor + commit..HEAD quiet + HEAD clean + untracked
refusal + per-row byte equality; staged AST audit; renewal generation/Contract8 gates.
Drivers stay outside replay-blob closures (outside but not replay deps, NO auto-add to P3S).
Code-bytes change still requires fresh CURRENT proof + member-wise closure equality.

No source counts unsupported: counts never authority (G76 exact-76 + member-wise equality + fresh
CURRENT proof required; R2/R3 count claims withdrawn where unproven).

## Operation branches — idempotent / refusal / guard / current-vs-history (source facts, not generic)

- S1: entry `ISSUE_INITIALIZED|DISCOVERY_COLLECTED:504-505` + `verify_state_basis:503`;
  `output_dir` non-empty refuse `:517-518`; `batch_dir.mkdir(parents=True,exist_ok=True):520` +
  `write_jsonl:525` + `core.write_json(package):566` (mkdir-p+write_bytes, check-then-write NOT O_EXCL).
  No idempotent re-prepare; TOCTOU preserved. NEW preflight (RB6 loader + unknown + loss + U)
  MUST precede `:517`. History: `_check_screening_package_files_content:629-651` State-free stays unchanged.
- S2: `validate_package_basis:927` before any copy; `run_dir.exists` branch: if
  `acceptance_path.is_file()` → `validate_acceptance:953-954` return existing (idempotent);
  else `raise incomplete:956`. Copies `package.json` + input batches + results via `shutil.copy2:960-965`
  then `core.write_json(acceptance):977`; digest `_result_set_digest:757-764`, `run_dir.name==digest`.
  NEW preflight before first `copy2`. Historical re-read `validate_acceptance:897-916` stays
  LIVE-bound for current S2 only; LOW never calls it (RB1).
- E1: temp `tasks/task-*.json:631` + `package.json:680`; non-empty refuse `:595-596`.
  NEW unknown-check before temp authority (N1 preflight + HIGH eligibility).
- E2/Views: digest-dir `exists` check (not O_EXCL); incomplete raises `:1190-1194/:1863-1869`;
  prepublish `_dm022_require_ready:694,727` immediately before write; idempotent re-reads
  `:1191-1192/:1864-1865` preserve original validity, MUST NOT apply new policy.
- E3: `exists-or-symlink→refuse:749-750,765-766` (NOT O_EXCL); archive `exists→sha-compare→raise:573-594`
  (identical idempotent, divergent refuse); entry+prepublish `_dm022_require_ready:748,764,805`.
- N1: `CANDIDATES_NORMALIZED+validate_agent_state:610-614`, `_dm022_require_ready:623`,
  PREARCH refuse `:624-631`, accepted+effective resolution `:637-648`, NEW preflight AFTER `:641-648`
  BEFORE `:653`; no writes. `task_source_ids:665-672` after package (record/task-dependent only).
- H1 prepare: eligibility `:478-499` + `_prove_before_graph_unbound:499` + HEAD/tree `:500` +
  request parse/schema `:502-508` + LIVE pins `:515-522` + `before_state` SHA/count `:524-535` +
  `derive_current_root_effective_context` + DM016/DM017 7-field eligibility BEFORE first COPY `:538`
  (`_copy_regular_exclusive`), 7-slot COPYs `:563-600`, candidate writes ONLY from `:605`
  (`_exclusive_write_bytes:83` O_CREAT|O_EXCL+link+fsync+postread; partial PRESERVED;
  State switch ONLY `replace_state_triplet`). `state_path` must be canonical `production-state.json`.
- H1 adopt: LIVE re-parse + eligibility + HEAD/tree + contract/tools + `before_state` SHA +
  retention equality + slot drift + `_prove_before_graph_unbound:1127` BEFORE any guard/checkpoint/
  State mutation, then `prove_revision_from_paths:1140` BEFORE proof write `:1142`
  (`_exclusive_write_bytes proof/proposed-graph-proof.json`) + report `:1176` + guard claim `:1241` +
  checkpoint `:1242-1243` + switch/clear/complete/release `:1249-1254`. Unknown LIVE never rewritten;
  stale pins refuse (NEW bounded attempt, no silent overwrite).
- Resume: `B→switch+clear+complete+release`, `E→clear+complete+release`,
  `E`+completion+guard-absent→`ALREADY_ACTIVE` (no writes), else `INDETERMINATE` preserve
  (no auto-rollback/takeover). Nonce-bound guard intent verified.
- Readback `:1379-1410` detached read-only via `resolve_research_authority` (no LIVE window re-imposed);
  old readback NOT re-gated; artifact-producer boundary reported separately.
- Current-vs-history: old accepted graphs WITH loss remain VALID history; new S1/S2/N1/E1/E2/H1
  refuse `DECLARATION_LOSS` before writes. New policy ONLY at current-operation owners; never in
  historical `_content`/renewal/LOW passive checks (`require_no_active_guard`, `require_completion_consistent`,
  `require_research_operation_ready` stay entry-only).

## Oracles (planning ONLY — NOT executed; no test-count sums)

- Positive: all 10 new types via actual v2 task/card; unchanged old types; many-to-many per-`(parent,OID)`
  incl shared-OID pass variant; initial-only `U==P` 3-field all 3 Profiles (WEEKLY `2026-W35` null,
  THEMATIC `SP001` 3→8, RETRO `SP-2025-H2` null); GAP_FILL `O13` + valid `REFERENCE_EXPANSION` carrier
  with 5-field passes and derives DIDs/taskIDs; direct==agent-first byte-equal + residual order;
  `LIMITED` residual-subset passes full validators; HIGH prepare+adopt re-verified with true R/E.
- Negative pre-write: unknown `source_type` incl DROP; `(R2,O1)` loss despite global equality
  (synthetic D1/D2 labelled); dup/missing/extra/undeclared-dim/empty-desc/5-on-initial/7-field/auto-status;
  `NOT_APPLICABLE` explicit; late drift caught; `SOURCE-passes` false-completeness refused
  (provenance `research_pass` mismatch); E-as-R refused; `None`-as-DIRECT refused; Stage-claimed-DCP-missing
  refused; malformed/symlink/unreadable marker never DIRECT fallback; file-vs-digest conflation refused.
- Limits: non-four-family/Retro complete-reader REQUIRED follow-on, not solved; manual
  `DIRECT_PRIMARY/PRIMARY_ONLY` byte-hash only, post-VALIDATED republication `UNSUPPORTED_ROUTE`;
  custom-period `--spec` sufficient; DM022 `research_profile` WEEKLY/THEMATIC only; RETRO excluded;
  multi-DID/multi-source ambiguous-primary refused; old history valid, new loss refused;
  epoch drift `INDETERMINATE` preserve; no full-suite/test-count sum. Tests reuse EXISTING fixtures/methods
  only; no invented names; EFF-O13/O14/O15 secondary reference only.

## Contract extension requiring ROOT decision (not implementer choice)

New public PATHS-only loaders are non-equivalent Source API (new importable entry points in existing
modules, no new module/schema/family). R4 gives precise contracts for ROOT decision BEFORE code:

1. `derive_ordinary_root_effective_context(repo_root: Path, request_path: Path, before_copy_path: Path) -> dict`
   in `survey_research_authority_v2.py` (LOW history COPY-only; returns §4 context keys; no writes/guard/State/agent).
2. `derive_current_root_effective_context(repo_root: Path, request_path: Path, live_state_path: Path) -> dict`
   in `survey_research_authority_v2.py` (HIGH-only; after eligibility, before first COPY).
3. `resolve_prepackage_root_effective(repo_root: Path, state_path: Path, discovery_path: Path, accepted_discovery_path: Path | None) -> dict`
   in `survey_screening_v2.py` (ordinary S-prepare; PATHS-only; optional path expected-binding only;
   returns `authorityKind/basisMode` + R/E + SHAs/counts).
4. Private `_derive_root_effective_kernel(*, ...)` shared pure kernel (no permission token).
5. Keyword-only `*, before_copy_path: Path|None=None` (+ `*, request_path` where missing) on the five
   LOW `*_from_paths` listed in §RB4 (derive from request/manifest retention refs if possible, else refuse).

If ROOT rejects any new public path, return exact gap before code; no silent fallback to caller dict
kwargs, no E-as-R, no `None`-DIRECT, no schema change, no support reduction. Any essential contradiction
returns ROOT NOT_READY.

## Return + stop point

R4 actual complete function args + record field predicates (12 keys, Contract8, producer, profile
binding, 1-CORE, deterministic refs, file-vs-digest) + low-high root map (COPY vs LIVE loaders +
per-site forwarding + adopted-full before-COPY derivation + cycle rule) + source compat
(lazy imports within existing sets, drivers outside replay, G76 exact-76 + member-wise + fresh proof)
+ oracles (above, planning only) are COMPLETE FOR REVIEW. No author PASS. Independent readiness must
close RB1–RB7; final Astra confirmation required before code. Author declares no Commit Point.
Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; Profile/quality/adoption/savings OPEN.

(End — R4 delta; R3/kernel preserved; review + Astra confirmation required before code.)
