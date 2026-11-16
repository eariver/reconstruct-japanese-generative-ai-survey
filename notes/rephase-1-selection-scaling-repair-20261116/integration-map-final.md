# Selection scaling repair — integrated executable map FINAL (MAP-ONLY, no code)

Status: MAP-ONLY source-read design. No Git/imports/runtime/tests/fixtures/network/active/source/shadow writes/subagents in this action. Dedicated reads only (Read/Grep). Awaiting root + fresh independent scoped confirmation BEFORE any code. No implementation-ready self-claim.
Source: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` recorded HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` parent `cc1c7fd1…` tree `ec11cf6c…` (head not re-verified with Git here). Final773 manifest `a7e40c47…`/202833B BASE `409b292` final141 patch `171812f6…` unchanged. Line numbers are worktree observations; re-bind before code.

## 0. Retractions (root §§4–5 bind)

- Empty supplement ⇒ no Raw is WRONG. `discovery._normalize_record` 121–127 reads/hashes every `source.raw_paths` via `_safe_repo_file`. X `raw_path`, supplement Raw, Discovery Raw are independent closures (inventory §§1/3.5).
- `basis.state_sha256==LIVE` is WRONG. `agent_tool._historical_state_basis_wrapper` 53–98 tolerates ONLY `state_sha256` drift, ONLY after sibling `screening-accepted.json`/`evidence-accepted.json` is_file/no-symlink (71–73) AND `sha256_file(package)==acceptance.package_sha256` (75–76), then in-memory `adjusted.basis.state_sha256=sha256_file(state_path)` 92–95 + `original(...,adjusted,...)` 96. Preserve exactly; no second hand wrapper; never demand stored old SHA==LIVE.
- Proof/decision bytes are NOT opened by existing readback (`resolve` 1181–1201, checker 3891–3920 SHA-only cross-bind). New domain explicitly rehashes their SizedRefs as bounded integrity binding; do not claim old code verified full bytes.
- No Session files in this path. “Session root” = in-memory `root_records`/`root_path` passed to content cores (inventory §3.5/§8).

## 1. One integrated mechanism (21AG bounded initial, then 0AG)

Bounded full initial (original code, honest counts) → pre-capture full closure → single content EU + single held upstream → cheap freshness for all later writes/returns. No globals/epoch/ContextVar cache, verified-dict, public skip/flag, expanded monkeypatch verifier, new module/schema/family, third validator.

- KEEP full: `run:249` 3AG (`agent.validate_agent_state` 919–1070) + `run:260` first READY 2AG (`low._verify_completion_full` 996–1125 with `low:1018` + `low:1073` both retained, original LOW file unchanged) + `run:264` first `resolve_research_authority` 1AG + `run:283` screening 6AG (checkpoint 3AG via `agent:1210` + package 3AG via override) = **12AG**.
- Package-once (original publics under ORIGINAL `agent_tool.current_stage_basis_override` 121–143, `finally` restore): `screening.validate_package_basis` 1322–1338 once + `evidence.validate_evidence_package_basis` 1203–1251 once = **+3+6AG**. Total bounded initial **21AG** (source estimate only, not affordability proof; actual 7-run decides). Duplicate-removal only if implementation proves same predicates/same bytes/same order with temporal purpose preserved; default keeps 21AG.
- Then: EU/summary use content cores only (0AG). Later READYs use `low._assert_selection_authority_fresh` (FILE/pin/lstat + FULL own-epoch batch, no 6E/3V) + `require_no_active_guard`. Original `_verify_completion_full`/public validators unchanged.

## 2. Actual registry inspection (not “unchanged” assertion)

- Runner 20–28 imports `agent, agent_tool, architecture(wrapper), discovery, core, low, review_attention, schema_gate, screening`; NO `base`. New edge runner→`survey_architecture_v2_base as base` (owner BASE, documented). Runner never imports evidence/completeness/screening privates; those via LOW function-local only.
- LOW 21–35 + 40–49: top-level ONLY `core` shape-only (`repo_local_path, sha256_file/object/bytes, json_bytes, load_json, parse_instant, iso_utc`) + `schema_gate` + stdlib. B1 leaf preserved. Function-local `evidence_mod/completeness_mod` at 459–460 (same pattern at 820–821) is the allowed owner for new privates.
- BASE 15–17 already imports `completeness, evidence, core`. New privates reuse them; no new top import.
- LOW historical7 `low:587–599` = `survey_research_authority_v2.py`, `survey_prearchitecture_acceptance_v2.py` + 5 `dm022-*` schemas; `$id`s 601–607; `tool_pins.tool_shas` must equal exactly this set 664–667. Own-epoch 639–799: `cat-file -e` 671, `show` 673, `ls-tree -r` 696, `cat-file --batch` 716–726, `$id` 755–761, Contract8 recompute 762–798 (mirrors `core.contract_identity`, profile names from COMMIT bytes) must equal checkpoint contract 795 AND manifest pins 797. CURRENT pipeline closure (76+3+control roots from COMMIT config 681–685) is not own-epoch; no digest claimed for repaired runner/LOW/BASE until implementation (record new SHA/bytes then; verify Contract8/STATE/PROFILE/DM022 schemas unchanged via `sha256_file`, any change returns to root).
- Public signatures UNCHANGED: `run, _dm022_require_ready, _dm022_pinned_family, resolve_research_authority, validate_agent_state, check_supersession_record_from_paths, _verify_adopted_graph_full/_verify_completion_full, derive_candidate_matrix/_load_upstream/validate_candidate_matrix/selection/architecture, build_architecture_review_summary, validate_*_acceptance/ledger/completeness, verify_state_basis, current_stage_basis_override`. New privates only (§3).

Changed paths (existing files only): `run_selection_architecture_v2_interactive.py` (holder + 8 call-site swaps + base import); `survey_research_authority_v2.py` (3 LOW privates); `survey_architecture_v2_base.py` (2 privates + 1 shared projection helper; wrapper `survey_architecture_v2.py` delegation intact). No arbitrary file budget; no 4th file unless wrapper explicit method needed (allowed, documented at implementation).

## 3. Internally owned handle (sealed only after full validation)

```python
# owner LOW, lifetime single run(), opaque to runner
class _SelectionAuthorityBundle:  # frozen slots
    state_path: Path; state_sha: str
    checkpoint_path: str; checkpoint_sha: str
    pins: tuple[label,Path,sha,len]  # every §5 file
    raw_refs: tuple[path,sha,len]    # Discovery non-supp + X + supplement
    expectations: MappingProxyType   # {issue_id,research_profile,canonical_state_path}
    root_records: tuple; root_path: Path; effective_records: tuple; effective_path: Path
    upstream: MappingProxyType | None  # held after first content EU, never in run() return
    own_epoch: tuple[commit,contract]  # commit SHA + Contract8
    guard_lstat: tuple; seven_lstat: tuple; implementation_sha: str
def low._get_selection_authority_bundle(repo_root, state_path) -> _SelectionAuthorityBundle
def low._assert_selection_authority_fresh(repo_root, state_path, bundle) -> None
def low._bundle_upstream_paths(bundle) -> tuple[Path,...]  # profile/discovery/screening/evidence/views/ledger/completeness; runner uses Paths, never bundle[...]
def base._validate_candidate_matrix_against_upstream(matrix, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path) -> list[str]
def base._build_architecture_review_summary_with_upstream(repo_root, profile_path, discovery_path, screening_path, evidence_path, views_path, ledger_path, completeness_path, matrix_path, selection_path, architecture_path, implementation_sha, upstream) -> dict
def base._summarize_review_contents(upstream, matrix, selection, architecture) -> tuple[dict,dict]  # ONE helper extracted from base:914–1044, used by BOTH public build_... and private with-upstream
```

Owner constructs/reloads/fully validates internally and binds to invocation; arbitrary caller dict never promoted. Capture-then-parse: State pin→parse SAME bytes→checkpoint refs→checkpoint pin→parse SAME bytes→four/request/manifest pins→DCP/SCP/root/effective→acceptance/package/tasks/results/views/supplement enumeration; each `sha/byte_count==expected ref` BEFORE storing, mismatch fail-closed, never `expected=observed`. Construction order: pre-capture enumeration (§5) → run full 21AG initial (§1) → seal (store pins + own-epoch + lstats + implementation_sha). Freshness never reseals.

## 4. Capture origin per field (expected pin → traversal → inventory → containment)

| Class | Expected pin origin | Traversal / inventory / containment |
|---|---|---|
| LIVE State FILE | itself (no external SHA); bound by first full strictState+completion | `_safe_read_bytes` low:147–187 (O_NOFOLLOW/dev-ino) + `_repo_rel` 127–135; parse SAME buffer |
| Profile FILE | `state.profile.{path,sha256}` + `request.profile_ref` + checkpoint `profile` | read via pinned paths; multi-ref equality NOT universally enforced — pin each ref separately, freshness requires each FILE == its own pin |
| Checkpoint FILE | State triplet SHA (`require_same_triplet` 387–400) | `_load_typed_checkpoint_record` 329; shape/self-digest/family |
| 4 artifacts | checkpoint `artifacts[4 NamedRefs]` path/sha | `_load_typed_four_refs` 437–565; each FILE rehashed |
| request/retention_plan/report SizedRefs | checkpoint `{request,retention_plan,report}.{path,sha256,byte_count}` | `_verify_sized_ref_bytes` 297–307 + `_safe_read_bytes`; report→manifest SHA bound in `resolve` 1194–1197 (completion-only binds via request/before/retention rows, no whole-manifest SHA) |
| proof/decision/reviews[0].result SizedRefs | checkpoint refs (old code SHA-only) | **new**: rehash bytes same helpers; selected integrity binding, not old-behavior claim |
| COPY `state-before.json` | `record.before_state` + `request.before_state` SHA/len (same COPY checked against both) | `_repo_rel revision_root/retention/state-before.json`; `derive_ordinary_root_effective_context` 1861–1909 COPY-bound, refuses LIVE 1890–1896 |
| manifest/completion/inventory | `report.manifest` SHA; `retention_snapshots[7]` exact rows; `seven_plan[7]`; `expected_after` COPY-recompute 1059–1063 | manifest 871–885; inventory 7 rows 1033–1053 exact vs manifest; completion 1022–1031; `lstat_slot` 3984 + tolerance 1102–1124 |
| DCP/SCP + deterministic reviews + CORE reports | State `checkpoint_provenance.{discovery,screening}` SHA; LEGACY family 1775–1789 | `_context_from_before_state` 1765–1789; `_validate_legacy_dcp_scp` 1459–1507; `_rehash_deterministic_reviews` 1325–1379; `_validate_legacy_stage_report` 1382–1456 (exact 12 keys, record-owned contract/impl) |
| Discovery acceptance/X manifest/tasks/Raws/JSONL/root Raw | acceptance `x_source_intake.sha256`, `discovery_sha256`; X `production_profile.path`, `runs[].task.path`, `runs[].result.raw.{path,sha256,byte_count}` | `discovery.validate_acceptance` 274–298; X 344–396; `_normalize_record` 121–127 EVERY `raw_paths` + `_safe_repo_file`; expansion child path existence/containment only 297–298 (bytes via root Raw hash) |
| Screening pkg/batches/results/prompt/schema/basis | acceptance `package_sha256`; `package.input.batches[].sha256`; acceptance `batches[].result_sha256`; `basis.*_path` file SHAs; prompt/contract SHAs | `_exact_regular_files` (screening 99–113, evidence 738–753) exact set/no-missing/no-extra/no-symlink; `_check_screening_package_files_content` 1256–1278; batch/digest 1394–1433; content 1281–1319 path-identity 1304–1305 vs live SHA+`verify_state_basis` 1332–1338 |
| Evidence pkg/tasks/cards/Views/supplement | acceptance `package_sha256`, `screening_acceptance_sha256`; package `tasks[].{path,sha256}`, results `filename/sha`, views `view_sha256`; supplement manifest SHA + EVERY `validated.sources[].raw_path` SHA/len | `_check_evidence_package_fields/files` 1036–1071; tasks 1635–1652 capture BEFORE `meta_by_id` bind; `_load_pinned_json` same-buffer 259–277; `_supplement_source_file` 497–520 containment/no-follow; `_resolve_phase_supplement_context` 300–386 + `_recheck_supplement_context` 389–424 + `_recheck_phase_pins` 249–256 + `_assert_pin_repo_ancestors` 280–297 |
| Ledger/Completeness | PREARCH NamedRef SHAs; ledger basis recomputes Profile/Discovery/Screening/Evidence/Views/digests; completeness basis recomputes Profile+Ledger | `_check_ledger_rows_content` 2657–2722; `_validate_profile_completeness_content` 241–262 + `_validate_obligation_shape` 50–78; extra rereads Discovery/Profile/Ledger |
| Schemas/config/prompts/legacy State | current files if actually read (no declared SHA in selection path); own-epoch pins via `tool_shas` | `_require_contracts` base:79–82; agent/LOW `_legacy_producer_check` 1289–1322; never substitute LIVE tools for history |

Cycles: AG never calls completion/resolve/ready; completion calls AG twice (1018+1073); resolve calls AG once; `_load_upstream`→validators→`verify_state_basis`→`check_supersession`→AG leaf finite DAG. Discovery parent graph `_validate_graph` duplicate/edge checks; no Session-file cycle (no Session files).

## 5. Package-once + content cores (no 45AG/90AG)

- Package-once under ORIGINAL override: `screening.validate_package_basis` + `evidence.validate_evidence_package_basis` originals once (historical wrapper 53–98 applies; sibling+archived binds + adjusted rerun). Later assembly uses content cores `screening._validate_screening_package_basis_content` 1281–1319 + `evidence._validate_evidence_package_basis_content` 1144–1200 (path-identity 1304–1305/1168–1169) + shared pure row helpers (`_check_screening_package_files_content`, `_check_screening_batches_and_digest` 1394–1433 via `_validate_result_batch` 1341–1381, `_check_evidence_package_fields/files`, `_check_ledger_rows_content`, `_check_completeness_result_content`+`_validate_obligation_shape`), plus pin rechecks + sibling/archived binds proving original predicates still hold. State-SHA+`verify_state_basis` vs path-identity BOTH enforced (originals once, then rechecks; R1 line-163 triplet-only corrected).
- First EU (`run:310`) + summary (`run:432`): existing `base._load_upstream_content` 85–152 (`expectations/root_records/root_path`, NO `effective_*`/NO `implementation_sha`) + `base._derive_matrix_rows_content` 183–276 (P retained: `sha256_file+load_json` per card/view 213–218). No LIVE `_load_upstream` 279–353 after package-once.
- Summary: extract ONE `base._summarize_review_contents` from 914–1044 (counts + `major_material_destinations`); public `build_...` 852–1044 and private `with_upstream` share it. Private `with_upstream` loads matrix/selection/architecture JSONs, calls `_validate_candidate_matrix_against_upstream` (P-only re-derive, byte-equality vs `derive` shape 388–397, no second `_load_upstream`), `validate_selection` 407–564 + `validate_architecture` 567+ small, then shared projection. No 45AG at 866, no 45AG at 880/373.

## 6. Freshness (cheap + FULL own-epoch batch)

`low._assert_selection_authority_fresh` calls only existing primitives: re-read LIVE State (`_safe_read_bytes`) + `require_same_triplet` 387–400 + checkpoint/four FILE rehash vs pins; SizedRef re-verify 297–307; `evidence._recheck_phase_pins/_recheck_supplement_context/_assert_pin_repo_ancestors` function-local; COPY sha/len vs `before_state`; retention 7-row exact vs manifest; `expected_after` recompute 568–584; `require_no_active_guard` 4024 + `seven_plan` vs inventory vs `lstat_slot` 1102–1124 (old-absent/new-content/same-byte-new-inode allowed, same-inode stale/nonregular/unreadable refuse); PLUS FULL `low._verify_own_epoch_commit` 639–799 every gate (commit+blobs+config+Contract8, per root F6; cost is implementation oracle, not SHA-only skip). Drift → fail-closed `ResearchAuthorityError`/`DM022_TRANSITION_ACTIVE`, never silent adjust. Later READY sites (`:316,:362,:427,:440,:444,:451,:456`), `:271` (reuse `:264` four dict), `:283`-second-half, matrix/summary second EU use this; initial `:260` keeps full 2AG; LEGACY keeps guard-only branch (no content cache).

## 7. Writes + return (original pins, no drift into new baseline)

Each write keeps gate + no-overwrite + binding (sites unchanged, gate cost changed): matrix `:316→:319`, selection `:362→:365`, architecture `:427→:430`, review `:440→:443`, attention `:444→:447–448` (`build_attention`+`validate_attention` small, basis SHAs), archive `copy2` `:451→:454`, audit `:456→:459–471` (binds archive input + 5 outputs, not itself). Preceded by freshness + `_dm022_preflight_seven` 101–114/304 + `exists()/is_symlink()` refuse + `lstat_slot` tolerance. Outer `return` 472–481 re-binds 7 rels + SHAs AFTER final freshness; drift between last write and return refuses (no partial PASS). No auto-overwrite/rollback/cleanup-retry over partials; unknown State/guard refuses; global atomicity not claimed. LEGACY healthy same-triplet keeps canonical `materiality-ledger-v2.json`/`profile-completeness-v2.json`, guard-only READY, no PREARCH cores.

Epoch: historical reads use RECORDED commit (`low:610–617` never HEAD==recorded); CURRENT proof via `verify_current_stage_basis` 42–50 (`implementation_sha==repository_commit_sha` HEAD-only 189–207 + `validate_agent_state`) under override at 309–313/432–436. New HEAD (meaningful source-only commit in NEW independent DB, after root authorization; dirty oracles labelled dirty, clean re-run binds committed bytes) permits old initState `48082…`; no State/Profile repin, no old-implementation override, no fresh-init fixture standing in for saved-State continuation.

## 8. Oracles (exact fixture/method bindings, no active-DB mutation)

- Full validity: new independent byte-copy of `ae0dd1e` (hardlinks 0, inodes differ, 231/231, inert origin, no commondir/alternates; verify source773, runner/LOW/HIGH SHAs, both States `EVIDENCE_REVIEWED` init480 forward-history4 Human-pending, PREARCH CPs/completions/8 four-ref FILEs, active 7-absent vs shadow 0/3, guard absent, `GIT_OPTIONAL_LOCKS=0`/`PYTHONDONTWRITEBYTECODE=1`); unmutated W34-409/SP-160 `run()` must emit 7/7 exact schemas + basis binds + `READY_FOR_ARCHITECTURE_REVIEW` + audit input/output binds. Helpers: `test_run_selection_architecture_v2_interactive` (contract/no-overwrite), `test_survey_architecture_v2` + `test_survey_architecture_review_expansion_v2`, `test_dm022_full_lifecycle_v2` + `test_dm022_prearchitecture_acceptance_v2`.
- Late drift (each AFTER authority sealed, BEFORE next cheap gate): mutate one byte each (Raw/task/result/card/View/supplement manifest/COPY/State/checkpoint/one four-ref/guard/one slot stale same-inode) → gate refuses, no write. Missing-object (unlink one Raw/task) → pin-recheck refuses. Helpers: `test_dm022_b_late_prepublish_v2` + `test_dm022_normal_writer_late_guard_v2`, `test_survey_evidence_v2`/`test_survey_completeness_v2`/`test_survey_active_*` (content), `test_dm022_prearch_b_ordinary_consumers_v2` (B-side).
- Outer-return/archive: mutate State/checkpoint/artifact between last write and 472–481 → return refused. Mutate `input_path` archive source vs `archive_path` → audit bind refuses. Owned-outputs drift: second `run()` in FRESH invocation must NOT reuse prior bundle (local-only, no module-global/ContextVar — prove by code); W34 bundle must not validate SP (`issue_id`/triplet mismatch in `_load_upstream_content` 108 + `require_same_triplet`). Helpers: runner test + `test_dm022_c_*`/`test_dm022_c_direct_operation_v2` (completion/resolve/proof), `test_survey_agent_control_v2` + `test_survey_agent_tool_v2` (state/override/facade).
- No-supp/LEGACY/history-current: synthetic fixtures only — no-supplement `None+None` refusal (`evidence:300–330,1194–1198`), LEGACY same-triplet canonical branch (no AG), COPY-bound `derive_ordinary_root_effective_context` refuses LIVE path as COPY and vice versa (1884–1908/1937–1945). Fixtures: `dm022_prearchitecture_fixtures_v2` + `dm022_lifecycle_fixture_v2` + `dm022_g71_g76_fixture_v2`.
- Needed-blob fault: ONLY on NEW disposable fixture copy (`mv .git/objects/<aa>/<rest> /tmp/backup` for ONE needed blob e.g. `survey_research_authority_v2.py` from `low:592`, `dm022-supersession-checkpoint` schema 598, or `config/survey-production-v2.json` 689–691; verify 231/231 present via `cat-file -e <commit>^{commit}` else abort copy); full own-epoch batch MUST refuse; `restore mv` back, re-verify pass. NEVER `b797…` (already absent, unrelated, not in needed set 685–695), NEVER remove from author/implementation/delivery DB. No repeated expensive real run for byte-stability; two independent clean copies same-input 7-output `audit.json` SHA equality (bytes equal, inodes may differ per 1102–1124) uses SAME procedure, never second run over same `source_root`.

## 9. Proof/delivery/stop

After repair on new copy: actual W34-409/SP-160 all-seven normal-writer completion, independent output/content binding, fresh CURRENT proof (`verify_renewal_source_proof` CURRENT_PROOF_VALID + SAME-proof drift refusal/restore), exact DIRECT409 `409b292`→new-HEAD patch (inherited overlays included, never layer old patches) + manifest (per-path SHA/bytes/modes) + proof-copy `candidate-partial-b40de60` check0/apply0 all-paths×3, scoped689+new, missing26309/bulk31466/runtimeTeX nonbundled + whitespace diagnostics retained. Record wall/CPU/rchar honestly. Genuine gaps returning to root (no auto-broaden): un-pinnable class, new schema/module/family/global-flag need, supplement shape change, Profile P1–P4, DM022-HIGH/LOW residual, Thematic/Retrospective scope per 2026-10-31. No generic B2/B4 cycle/reader/timeout-only enlargement.

## 10. Final disposition

No load-bearing gap found in this source-read map; all required signatures/origins/traversals/closures/writes/oracles are bound above to actual registries. MAP status: **READY for root + independent scoped confirmation; NOT implementation PASS, no code authorized**. Implementation dispatch requires both confirmations recorded.

(End of map — MAP-ONLY, no code.)
