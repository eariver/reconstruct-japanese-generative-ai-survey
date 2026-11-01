# Workstream C — DM022 HIGH/LOW coupled runtime (largest coupled part, whole P1–P4)

2026-10-31. Owner C exclusive runtime edit ownership: `scripts/survey_research_authority_v2.py` (LOW)
and `scripts/survey_prearchitecture_acceptance_v2.py` (HIGH), in workcopy ONLY
`.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`
(768-file final133 snapshot; no restore, no old overlay layering).
Raw check transcript: `workstream-c-checks-20261031T154321Z.txt` (same directory).

Authority (read in full, existing map READY, no new pre-code cycle):
contract `outputs/rephase-1-profile-support-contract-decision.md` INCLUDING §7 (FULL
`62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`)
+ contract ROOT §5 (`notes/rephase-1-profile-support-contract/astra-review-resolution.md`,
FULL `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`);
pre-code assessment + packet README; mandatory `astra-precode-gate-resolution.md` FULL
`bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa` /20159B INCLUDING §7;
R3 + C-R2 + detached-root-context-map overridden by R4, with FULL R5
(`integrated-readiness-r5-path-hardening.md`) overriding; scope decision
`outputs/rephase-1-scope-reassessment-20261031.md` INCLUDING §8 (whole P1–P4 retained,
no automatic generic reader later). No new schema/module/family; no DIRECT-only reduction.

Tool note: the dispatch required `apply_patch` for code/doc edits, but no `apply_patch`
binary exists in this environment (`which apply_patch` → not found). Used the file-editor
exact-replacement path for existing files (same discipline: exact `oldString`→`newString`,
no `sed`/`awk`/shell redirection) and direct file creation for the two NEW files owned by
this workstream (this note + the raw transcript above). No other files touched.

## 1. Edited paths / source hashes (implementation, not stubs)

- `scripts/survey_research_authority_v2.py` — SHA256
  `881de0f66d6f375445fd139d236f4be10bdbce4e5c3479acea6b0aae0517b49f`, 3500 lines
  (was 2677; +823 net: loaders/kernel/LEGACY validators/kwarg threading).
- `scripts/survey_prearchitecture_acceptance_v2.py` — SHA256
  `6c2b4d0364fec9030aa36ad71854bd0295124093b4945d878b473af0d17f64d0`, 1540 lines
  (was 1456; +84 net: HIGH preflight + adopt recheck + caller forwarding).
- No tests/fixtures/schema/config/other-file edits (owners D/B/A respectively).

## 2. Full mechanics covered (requirement → implementation site)

- PATH-only public loaders (exact R4/R5 names, LOW file): 
  `derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)`
  (LOW history, pinned COPY, never LIVE State) and
  `derive_current_root_effective_context(repo_root, request_path, live_state_path)`
  (HIGH-only, after strict LIVE eligibility, before first COPY; LIVE bytes re-checked
  against `request.before_state`). Shared private kernel `_derive_root_effective_kernel(*,
  repo_root, before_state, canonical_state_path, dcp_record, scp_record, request,
  profile_doc, root_records, root_path)` (exact R4 signature, keyword-only); kernel data
  is not external permission — authority comes from the caller's COPY pin vs HIGH
  eligibility. Common tail `_context_from_before_state` (steps 3–10).
- Ordinary LEGACY DCP/SCP (`_validate_legacy_dcp_scp`, `_validate_legacy_stage_report`,
  `_rehash_deterministic_reviews`, `_legacy_producer_check`, `_local_artifact_map` — all
  local to LOW, no agent import per LOW header): LEGACY-only (`DM022_WRONG_FAMILY` on
  PREARCH, unknown kinds refused by typed loader), issue==COPY issue, producer from
  on-disk config `stage_plan` only (discovery→ISSUE_INITIALIZED/DISCOVERY_COLLECTED,
  screening→DISCOVERY_COLLECTED/CANDIDATES_NORMALIZED), checkpoint membership, exactly
  one `discovery-acceptance` / `screening-acceptance` NamedRef, exactly one matching
  CORE_STAGE_CONTRACT DETERMINISTIC PASS (additional schema-valid rows allowed; every
  deterministic result ref file-rehashed incl. byte_count), original 12-key report with
  record-owned Contract8/implementation equality (`record.contract`, never a current
  `contract_identity` fallback), canonical logical historical State path ONLY
  (`<source_root>/production-state.json`, no live SHA), artifact-map equality,
  `recorded_at` parse. DCP → state-free `discovery.validate_acceptance`; SCP →
  Screening `_validate_screening_acceptance_content` + `_resolve_effective_discovery_basis_content`
  (CONTENT siblings only; never public LIVE-bound `validate_acceptance` /
  `resolve_effective_discovery_basis` / `resolve_active_screening_acceptance` /
  `_canonical_root_acceptance`, never agent validation, never PREARCH seven-file
  proof/completion on DCP/SCP). Request Discovery binds E (resolve+SHA+SizedRef);
  request Screening binds the SCP artifact; profile SizedRef bound (issue/research match).
  FILE SHA vs `result_set_sha256` never equated.
- ECP handling: `derive_before_context` keeps 4 required positionals; supplied previous
  path must resolve to `request.before_checkpoint.evidence` == COPY
  `checkpoint_provenance.evidence` with file SHA checked (never Discovery-derived); now
  also merges true-R/E keys (`root_*`, `effective_*`, `canonical_state_path`) from the
  D/S loader alongside legacy return keys (ECP content/lineage checks preserved, not replaced).
- Four builders gain REQUIRED keyword-only PATHs per R5 exact signatures (positions kept;
  explicit `None` refusal, never LIVE/ basename guessing): cards `*, before_copy_path`;
  accept `*, request_path, before_copy_path`; ledger `*, request_path, before_copy_path`;
  completeness `*, before_copy_path`. Each derives the D/S context from the same
  request+COPY and: package uses validated effective set for tasks; cards binds request
  records to effective DIDs; accept re-validates package basis via
  `_validate_evidence_package_basis_content` with true root; ledger verifies supplied
  paths resolve to the bound chain + uses effective rows + FULL `_validate_materiality_ledger_content`
  with true root; completeness union = initial + root-named + effective-named, declaring
  from effective, + FULL `_validate_profile_completeness_content` with true root.
  `prove_revision_from_paths` keeps 4 positionals; OLD ctx from manifest request +
  retained COPY feeds all NEW-graph FULL checks (separate OLD/NEW contexts, no new
  DM016/DM017 policy in historic passes). `_verify_adopted_graph_full` stays 3 args:
  retention/state-before.json derived ONLY after verified checkpoint exact-SHA / request
  SizedRef / revision identity-root / retention-plan SizedRef / manifest binding /
  before-SHA-size checks, then D/S loader; FULL content cores use true root (never
  E-as-R). `check_supersession_record_from_paths` keeps 4 positionals; supplied COPY now
  verified against bound retention layout bytes AND before-State SHA/size.
- HIGH (`survey_prearchitecture_acceptance_v2.py`): full strict LIVE eligibility retained
  (`verify_live_eligibility` untouched); prepare runs current loader + canonical
  `_source_class` over all R/E source rows incl DROP + `find_declaration_loss`
  per-(parent,OID) gate on the DM022 seven-field request (never ordinary 3/5) BEFORE
  first State COPY (`:538`); adopt re-verifies the same triple in the `:1127` window
  before ANY proof (`:1142`)/guard/checkpoint writes. All HIGH callers forward required
  paths (prepare cards/accept/ledger/completeness; adopt prove already had COPY);
  post-write acceptance FULL checks now carry true `root_records`/`root_path` (both
  `None,None` sites `:677/:682` fixed; repo now contains zero `None,None`). Resume/
  readback unchanged (resume completes bound intent under original guard/epoch rules;
  no retrospective eligibility; readback detached). Guard/ready/prepublish/rollback
  boundaries untouched. No historical new-policy gate added anywhere.
- Import discipline: top-level imports unchanged in both files (LOW: core+schema_gate+stdlib;
  HIGH: +LOW). All Evidence/Screening/Discovery/Completeness uses are function-local with
  exact signatures; LOW never imports agent modules or `run_evidence_v2_interactive`;
  pure mapping/universe/loss stays with owner A (`evidence._source_class`,
  `screening.find_declaration_loss` — referenced by precode names only, no second policy
  home, no top-level cycle).

## 3. External forwarding needed to root/integrator (report, not silent)

- **Owner A MUST land before HIGH gates can pass** (exact blocker, fail-closed at runtime,
  not a silent pass): `find_declaration_loss(root_records, effective_records)` in
  `scripts/survey_screening_v2.py` under its precode name (sorted `list[(parent_id,OID)]`,
  `[]`=pass), canonical10 rows in `survey_evidence_v2._source_class` (current table lacks
  the 10 literals, so new-type rows fail closed until A lands), and (for ordinary paths,
  owner B) `resolve_prepackage_root_effective`. Until A lands, HIGH prepare/adopt refuse
  with `BLOCKER(workstream-A): screening.find_declaration_loss is not yet present…`.
  No C-side fallback was added (a second policy home is forbidden).
- **Owner D (tests) MUST update callers/fixtures**: the four builders' new REQUIRED
  keyword-only PATHs break all existing direct test calls (pass explicit fixture COPY/
  request keywords; no test-only fallback); DM022 fixtures whose DCP `discovery-acceptance`
  artifact points at a raw JSONL (e.g. lifecycle-fixture simplifications) cannot satisfy
  the new LEGACY DCP chain (artifact must be a real Discovery acceptance; SCP artifact a
  real Screening acceptance with sibling `package.json`); adopted-full/prove/check tests
  need retention-layout COPYs and manifest bindings per R5 §3. Existing PASS counts do not
  transfer (fresh CURRENT proof required).
- **Owner B**: no action needed from C beyond the boundary — ordinary 3/5→7, residual
  parity, and agent-first thinning stay in B's files; C never applies the ordinary 3/5
  gate to DM022 (HIGH uses seven-field only) and never edits runner files.
- No new capability/contract/dependency gap beyond the above was found; no schema change
  was presumed; support was not reduced (DERIVED kept with full COPY-bound proof).

## 4. Actual checks / failures / limits

- Syntax/static (no-cache, zero-write): `ast.parse` over both edited files → `SYNTAX_OK`,
  exit 0, empty stderr (raw transcript pinned above with source SHAs). No `*.pyc` /
  `__pycache__` residue in the workcopy after checks.
- No behavioral suite executed on the shared moving source (per dispatch: integration
  testing follows after A/B/D land; running HIGH/LOW flows now would test a half-landed
  tree). No imports, fixtures, builds, network, commits, or reconstruct-Git inspection.
- Signature audit by read-only search: R5 keyword-only lists exact; `_verify_adopted_graph_full`
  3-arg; `derive_before_context`/`build_revision_package_from_paths`/`prove_revision_from_paths`/
  `check_supersession_record_from_paths` positional sets preserved; zero `None,None`
  remaining in owned files; all content-core calls carry true-root variables.
- Known limits carried forward (unchanged): partialDB missing26309/bulk31466, runtime/TeX
  unbundled, 55 Gitlinks/child dirt preserved, no full133/768/inode recertification, no
  old-PASS transfer. Old source/evidence untouched outside the two owned files.

## 5. Map gaps

None beyond §3's A-dependency blocker. The pre-code map proved sufficient for every C
site: every old `None,None`/E-as-R site is threaded, every required PATH is exact, the
D/S recovery is acyclic (loader/kernel never call adopted-full/completion/prove; the
reverse direction only), and ECP lineage stays outer file+SHA. Any further contradiction
found during integration returns to Astra before broadening.

No stubs, no hash-only proof, no forced positivity, no helper-only completion: every new
function performs its documented validation chain and refuses fail-closed with the exact
gap. No author independent approval claimed. Stopping here; no next unit auto-started.

---

## 6. Appendix — root review corrections #3–6 (2026-10-31, supersedes only the listed defects)

Review: `notes/rephase-1-profile-support-implementation/astra-implementation-review.md` §§3–6
(working review, not acceptance). Earlier §§1–5 claims above are preserved except where this
appendix explicitly corrects them. New source hashes (replacing §1):
`scripts/survey_research_authority_v2.py` SHA256
`546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737` (3644 lines);
`scripts/survey_prearchitecture_acceptance_v2.py` SHA256
`388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4` (1526 lines).
Raw transcript: `workstream-c-checks-20261031T155034Z.txt`. Only the two C-owned files
edited; A/B/D files untouched.

- **#3 Profile + canonical binding (LOW).** New `_bind_profile_and_canonical`: request
  Profile SizedRef loaded with SHA/byte_count verification + profile-shape validation;
  canonical logical State path derived from the BOUND profile (profile-file parent dir)
  and on-disk config `state_authority.authoritative_filename` — the exact original agent
  predicate — never the request assertion, never LIVE bytes, never current Contract8.
  `_context_from_before_state` (signature now `(repo_root, request, before_state)`) enforces:
  request Profile path **and** SHA exactly equal `before_state.profile` (not just
  issue/research), and `request.before_state.path` equals the derived canonical path
  (foreign assertions refused). HIGH current loader additionally requires the supplied
  LIVE path to resolve-equal the canonical request path; LOW ordinary loader refuses a
  COPY that resolves to the canonical LIVE path (LOW never reads LIVE). Both loaders bind
  Profile/canonical BEFORE any COPY/LIVE read. Adopted-full/prove/builder `expectations`
  now carry the loader-derived canonical value throughout.
- **#4 E-vs-R census (positional discovery vs trailing root).** Audited every C content-core
  call (not merely `None` absence): `_validate_*_acceptance_content` trailing
  `(root_records, root_path)` was already true-R; the defect was the *positional*
  `discovery_path` in ledger/completeness cores. Adopted-full and prove now pass
  `ctx["effective_path"]` (E) positionally with ctx root trailing — legitimate DERIVED
  chains (R≠E) validate the right graph instead of false-refusing on basis/row mismatch.
  Ledger/completeness builders already passed effective positionally; HIGH post-write
  checks and kernel paths re-verified correct.
- **#5 Retention/layout cross-binding (adopted-full, still 3 args).** Beyond the
  retention-plan SizedRef rehash: typed retention-inventory payload parsed (exactly 7 rows,
  slots in `SEVEN_SLOTS`, every row exactly equal to the stored manifest
  `retention_snapshots` slot row — the existing supersession/completion predicate, no
  second weaker parser) plus `manifest.before_checkpoint == request.before_checkpoint`
  exact triplet equality, before the fixed `revision_root/retention/state-before.json`
  derivation. No current State/Contract8 computation, no ECP-lineage recursion (outer
  ECP checks unchanged, one-direction acyclicity kept).
- **#6a Artifact predicate (inspected, no gap to return).** Stage-checkpoint schema allows
  `artifacts` minItems 1 (no total cap); the agent validator drift-checks *every* row with
  no count cap and the CORE report enforces full map equality. The earlier
  exactly-one-*total* rule was stronger than the original contract, so it is relaxed to:
  all rows valid NamedRefs (real `namedAuthority` shape, unique names) + exactly one row
  with the expected role name + every row's file rehashed (original per-row drift, now
  covering non-acceptance rows too). Deterministic non-CORE review rows tolerate extra
  result keys (original reads path/sha only); CORE stays exact 2-key per the agent core
  predicate. Record-owned implementation equality kept per the READY map (R4), which the
  review did not dispute.
- **#6b Direct A-helper calls.** `find_declaration_loss` has landed in Screening with the
  exact precode signature; both HIGH gates now call it directly. `BLOCKER(workstream-A)` /
  `getattr` compatibility text removed (probe: 0 occurrences in both files). Canonical10
  rows verified present in Evidence; `_source_class` calls unchanged.
- **#6c Docstrings.** Adopted-full stale `(DIRECT session basis)` wording and kernel
  `pure computation` wording corrected (`state-free path-reloading`, which does file I/O
  without State/agent). Required-4 builder PATHs, adopted-full 3 args, and all
  guard/ready/prepublish/rollback scopes kept unchanged.

Unresolved obligations (precise): meaningful behavioral tests with true DERIVED R≠E
through public HIGH and adopted readback, COPY Profile/path mismatch negatives, and
retention-binding substitution negatives belong to owner D + integrator runs on the
fully-landed tree (no suite run here per dispatch while others mutate shared source);
independent implementation review and CURRENT proof remain open. No contract authority
was missing beyond the inspected-and-resolved artifact question above — no broadening
requested, no mismatch accepted, no hash-only proof shipped.
