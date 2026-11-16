# Predicate reuse resolution R3 — additive correction (MAP-ONLY, no code)

Prior R1/R2 preserved. This R3 is concise additive correction per `astra-repair-resolution.md` §4 +
user narrow action. No code/runtime/tests/Git/network/subagents. Source-read only.
No `implementation-ready` self-claim; root + fresh review required BEFORE code.

## 0. Retractions (root §4)

- R2/reviewer claim “empty supplement ctx ⇒ no Raw” is WRONG and retracted.
  `survey_discovery_v2._normalize_record(repo_root,record,issue_id)` (`discovery:84-153`)
  reads/hashes EVERY `source.raw_paths[]` via `_safe_repo_file` (`:126-127`)
  `raw_refs.append({path,sha256,byte_count})`. `_normalize_record_content` (`:204-210`)
  shares it exactly (no drift). Discovery Raw (non-supplement) + X `raw_path` bind
  (`_validate_x_integration` `:179-201`) + Session material are transitive closure.
  Full Session/Discovery/X inventory is parallel independent Explore (root §4); R3 does
  NOT duplicate it — §5 lists only what R3 pins, Explorer adds remainder.
- Reviewer R1 literal “require `basis.state_sha256==LIVE State` AND path-identity” is WRONG
  and NOT applied. Existing `agent_tool._historical_state_basis_wrapper(original,*,error_text,
  acceptance_name,changed_text,label)` (`agent_tool:53-98`) tolerates ONLY `state_sha256` drift,
  ONLY after (a) sibling `package_path.parent/acceptance_name` (`screening-accepted.json`/
  `evidence-accepted.json`, no symlink, is_file, else original `state_error` `:71-73`),
  (b) `sha256_file(package_path)==acceptance.package_sha256` else `changed_text` (`:75-76`),
  (c) `basis.state_path` non-empty/in-repo/file (`:78-90`), then in-memory
  `adjusted.basis.state_sha256=sha256_file(state_path)` (`:92-95`) + `original(...,adjusted,...)` rerun
  (`:96`). Do NOT demand stored `basis.state_sha256==LIVE State`; that rejects healthy saved
  packages. Preserve wrapper exactly; no second hand-written wrapper in runner/freshness.

## 1. Chosen design (minimal robust, no 45AG/90AG)

Bounded full initial retained (original publics, honest counts §4) → single package-once →
content cores for all subsequent assembly (0 new AG). No globals/ContextVar/verified-dict/
public-flag/expanded monkeypatch. Ordinary `agent_tool.current_stage_basis_override`
(`agent_tool:121-143`, `finally` restore) remains SOLE facade; no bespoke verifier.
`verify_current_stage_basis(repo_root,cfg,state,implementation_sha,pending_basis=None)`
(`agent_tool:42-50`): `implementation_sha==core.repository_commit_sha(repo_root)` (`production:189-207`
HEAD-only) then `agent.validate_agent_state(repo_root,cfg,state)` (`agent:919-1070`, 3AG PREARCH).
Current HEAD = real new commit; no State repin (State impl `48082…` vs new HEAD handled by facade;
history uses recorded `cc1c…`/`ae0dd…` via `low:610-617`, never HEAD).

- Retain screening 6AG (`:283` both halves original publics under override) as simplest
  (no screening content factoring). Honest budget §4, runtime decides adequacy.
- Package-once: `screening.validate_package_basis(repo_root,package_path,package,implementation_sha)`
  (`screening:1322-1338`: `_check_screening_package_files_content` + `sha256_file(state)==basis.state_sha256`
  `:1333-1334` + `core.verify_state_basis` `:1336` strict `production:959-995` + binds) and
  `evidence.validate_evidence_package_basis(repo_root,package_path,package,implementation_sha)`
  (`evidence:1203-1251`: fields/files + State-SHA `:1219` + `verify_state_basis` `:1223` +
  `validate_screening_acceptance` nested `:1231-1237` + supplement + `_check_evidence_tasks_content`)
  each run ONCE under override (wrapper applies). Subsequent assembly uses content cores
  (`screening._validate_screening_package_basis_content` `:1281-1319` path-identity only,
  `evidence._validate_evidence_package_basis_content` `:1144-1200` path-identity only,
  plus shared pure row helpers below) + pin rechecks proving State/package/sibling unchanged,
  so original predicates still hold without rerunning `verify_state_basis` (rerun would pass
  identically; drift → fail-closed full revalidation, never silent adjust).
- First EU (`run:310`) and summary (`run:432`) use EXISTING
  `base._load_upstream_content(...,expectations,root_records,root_path)` (`base:85-152`)
  (NO `effective_*`, NO `implementation_sha`) + `base._derive_matrix_rows_content` (`base:183-276`, P
  `sha256_file+load_json` `:213-218`). No LIVE `_load_upstream` (`base:279-353`) after package-once.
  Summary single-upstream via §3 privates sharing ONE public projection helper (no huge duplicate).
- Remaining AG explicitly: `:249` 3AG + `:260` 2AG (`low:1018+1073` retained) + `:264` 1AG +
  `:283` 6AG + package-once nested already counted in `:283`/EU-once (no extra) + `:271` 0AG cheap +
  later READYs 0AG cheap (FILE/pin/lstat + FULL own-epoch batch `low:639-799` retained, §2) +
  EU/summary 0AG. Total bounded initial 12AG pre-first-content (3+2+1+6), NOT 6AG/9AG; no zero-assumption.
  No affordability/250-400 claim; 7-run oracle decides.

## 2. Factoring (existing originals, one new private pathway, no mirror)

Public standalone UNCHANGED (exact signatures retained):
`screening.validate_package_basis`, `evidence.validate_evidence_package_basis`,
`screening.validate_acceptance` (`screening:1524-1543`), `evidence.validate_evidence_acceptance`
(`evidence:1956-2015`), `evidence.validate_materiality_ledger` (`evidence:2770-2793`),
`completeness.validate_profile_completeness` (`completeness:265-290`),
`agent.validate_agent_state`, `core.verify_state_basis`, `current_stage_basis_override`.

NEW private pathway (owner LOW, lifetime single `run()`, opaque to runner):
- `low._get_selection_authority_bundle(repo_root: Path, state_path: Path) -> _SelectionAuthorityBundle`
  (frozen slots, no public constructor; `entries:MappingProxyType`, `raw_refs:tuple`,
  `pins:tuple[label,Path,sha,len]`; runner never constructs/indexes/mutates).
  Capture BEFORE `:249` from `state_path` arg only (capture-then-parse: State pin→parse→checkpoint
  refs→checkpoint pin→parse→four/request/manifest pins→DCP/SCP/root/effective→acceptance/package pins→
  tasks/results/views/supplement enumeration pins; each `sha/byte_count==expected ref` BEFORE storing,
  mismatch → fail-closed, never `expected=observed`). Owner reloads + fully validates internally;
  arbitrary caller dict never promoted to authority.
- `low._assert_selection_authority_fresh(repo_root: Path, state_path: Path, bundle: _SelectionAuthorityBundle) -> None`
  (re-read LIVE State + `require_same_triplet` `low:387-400` + checkpoint/four FILE rehash +
  `evidence._recheck_phase_pins/_recheck_supplement_context/_assert_pin_repo_ancestors` +
  COPY/`expected_after` (`low:568-584`) + seven-plan vs inventory vs `lstat_slot` `low:1102-1124` +
  FULL `_verify_own_epoch_commit` batch; drift → fail-closed).
- `low._bundle_upstream_paths(bundle: _SelectionAuthorityBundle) -> tuple[Path,...]`
  (opaque getter for `profile/discovery/screening/evidence/views/ledger/completeness` paths; runner
  uses returned Paths, never `bundle[...]`).
- Shared pure row helpers (EXISTING only, both LIVE+content already call them — no new extraction):
  `screening._check_screening_package_files_content`, `screening._check_screening_batches_and_digest`
  (`screening:1394-1433` via `_validate_result_batch` `:1341-1381`), `evidence._check_evidence_package_fields_content`,
  `evidence._check_evidence_package_files_content`, `evidence._check_ledger_rows_content`,
  `evidence._check_completeness_result_content` + `completeness._validate_obligation_shape` (`:50-78`).
  Differing predicates (State-SHA+`verify_state_basis` vs path-identity) BOTH enforced: originals once,
  then pin-rechecks + sibling/archived binds (R1 line-163 triplet-only insufficient — corrected here).

## 3. Runner/base imports + summary projection (no duplication, no LOW move)

- Runner adds `from scripts import survey_architecture_v2_base as base` (existing modules, new edge
  runner→base documented; owner BASE; runner never imports evidence/completeness/screening privates —
  those via LOW function-local only, `low:459-460,820-821`; B1 leaf preserved).
  Call sites: `base._load_upstream_content`, `base._validate_candidate_matrix_against_upstream(repo_root: Path,
  matrix: dict, upstream: dict, profile_path: Path, completeness_path: Path, ledger_path: Path,
  evidence_path: Path, views_path: Path) -> list[str]` (repo_root FIRST for `_derive...` `:213-218`),
  `base._build_architecture_review_summary_with_upstream(repo_root,...,upstream: dict) -> dict`.
  Alternatively explicit methods in `survey_architecture_v2.py` wrapper (4th file allowed); NOT via
  `__getattr__` (`wrapper:144-145` fragile). LOW holds research+D/S+supplement pins only; `upstream`
  lives in runner; row/Selection/Architecture validation live in BASE (boundary sentence).
- Summary huge projection (`base:914-1044`) NOT duplicated: extract ONCE public same helper, e.g.
  `base._summarize_review_contents(upstream: dict, matrix: dict, selection: dict, architecture: dict) -> tuple[dict,dict]`
  (counts + `major_material_destinations`), called by BOTH public `build_architecture_review_summary`
  (`base:852-1044`) and private `_with_upstream` overload. Public signature unchanged.

## 4. What to pin (R3 scope; Explorer adds Session/Discovery/X remainder)

Bundle pins (all `_safe_read_bytes` `low:147-187` O_NOFOLLOW/dev-ino + `_repo_rel` `low:127-135` +
`_verify_sized_ref_bytes` `low:297-306`): State+profile FILEs; checkpoint+4 artifact FILEs;
request/manifest/report/proof/decision/retention-inventory/COPY/completion FILEs;
DCP/SCP checkpoint records + `CORE_STAGE_CONTRACT` result FILEs + `artifacts[discovery/screening-acceptance]`
+ `_local_artifact_map` uniqueness (`low:1270-1286`); screening package/batch-input/result FILEs
(exact set via `screening._exact_regular_files`, same semantics `evidence:738-753`; capture BEFORE
`_check_batches_and_digest`); evidence acceptance/package + `tasks/*.json`+`results/*.json`
(`evidence:1635-1652` capture BEFORE `meta_by_id` bind, `_load_pinned_json` same-buffer `:1670-1673`);
views acceptance+`views/*.json` (`evidence:1819-1832`); supplement manifest + EVERY
`validated.sources[]` Raw (`evidence:369-376`, `_supplement_source_file` `:497-520`, `len(raw_refs)==len(entries)`
`:412-413`) + `basis_refs`; Discovery root/effective JSONLs (from `derive_ordinary_root_effective_context`
`low:1861-1909`, COPY-bound, refuses LIVE `low:1890-1896`); ledger/completeness via loaded dicts +
pure row checks. Discovery non-supplement Raw via `_normalize_record` `raw_paths` enumerated from
pinned root JSONL (capture root pin BEFORE parsing to discover raws; never parse unpinned to find next file).
Never `expected=observed`; freshness compares current FILE vs bundle pins.

## 5. Oracles (corrected, no active-DB mutation)

- Missing-blob: on implementation COPY ONLY, `mv .git/objects/<aa>/<rest> /tmp/backup` for ONE
  proof-required blob (e.g. `scripts/survey_research_authority_v2.py` from `low:592`,
  `schemas/dm022-supersession-checkpoint-v2.schema.json` from `low:598`, or
  `config/survey-production-v2.json` from needed `low:689-691`), then full `_verify_own_epoch_commit`
  MUST refuse; `restore mv` back, re-verify pass. NEVER `b797…` (already missing, unrelated, not in
  needed set `low:685-695`). Verify 231/231 present first (`cat-file -e <commit>^{commit}`); else abort copy.
- Stability: TWO independent clean copies from `ae0dd1e` (same §2 procedure), SAME input bytes reused,
  run `run()` each, compare 7 outputs + `audit.json` SHAs equal (bytes equal; inode may differ per
  `low:1102-1124`; modes `100644`). Never second run over same `source_root` (preflight+per-file refuses).
  Different input `generated_at` differing audit is NOT failure.
- New failures must be intended oracle failures, not earlier bad-fixture refusal.

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. No code until root confirms.
