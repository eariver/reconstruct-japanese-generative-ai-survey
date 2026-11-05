# SP r4 operation note — single use, SP only (review only, no execution yet)

Replaces rejected r3 execution authority. R3 preserved untouched, never run.
No shipping source changes. All active paths are the saved repaired-runtime
e84 tree; packet DATA are the authorized captures. No network, no Production
checkout, no reconstruct Git (never `git -C .`), no subagents.

## Files (this packet only)

- `sp-operator-harness-r4-20261104.py` — single-use prepare/dispose harness
  (source review only; one bounded Root auth required before `--stage=prepare`;
  separate explicit READY confirmation + auth required before `--stage=dispose`).
- `sp-staging-expected-manifest-r4-20261104.json` — machine staging/expected-pin
  manifest: 17 capture→dest rows with original manifests, exact2 canonical pins,
  original expected authority, intended-source binding vs delivery, blockers.
- This note. R2 DATA (`sp-corrected-input/supplement/delta-r2`) are DATA
  references only, not staged authority. R3 plan/harness/observation stay
  preserved as superseded evidence.

## Authority actually read (no pseudocode)

`run_evidence_v2_interactive.run(repo_root, state_path, input_path,
supplement_manifest_path=None)`; `_validate_record(row, profile)`;
`_validate_completeness_input(value, profile, *, discovery_records,
root_discovery_records)`; `validate_interactive_input(value, profile,
expected_ids, task_source_ids, *, discovery_records, root_discovery_records)`;
`_build_view(profile, task_id, evidence_sha, record)`;
`survey_evidence_v2.build_evidence_authority_supplement(repo_root, issue_id,
source_root, discovery_path, screening_acceptance_path, sources, output_path,
*, supplement_id, implementation_sha)`;
`validate_evidence_authority_supplement(repo_root, supplement_path,
implementation_sha, *, expected_issue_id, expected_source_root,
expected_discovery_path, expected_screening_acceptance_path,
screening_acceptance, discoveries)`; `prepare_evidence_package(...)`;
`stable_task_id / _source_class / _capture|_recheck_phase_pins /
_assert_pin_repo_ancestors / _resolve_phase_supplement_context /
_finish_authority_phase / _build_card_core / _validate_card_core /
validate_edition_view / accept_* / validate_* / build_materiality_ledger /
write_materiality_ledger`; `survey_agent_tool_v2.current_stage_basis_override(
pending_basis=None)` (strict facade, no caller dict, no extra bypass);
`survey_research_authority_v2.require_research_operation_ready(repo_root,
state_path)` (DM022); `survey_agent_control_v2.validate_agent_state(repo_root,
cfg, state) -> []`; `survey_production_v2.write_json/sha256_file/load_json/
repo_local_path/repository_commit_sha`; `survey_schema_v2.validate_instance`;
`survey_screening_v2.resolve_active_screening_acceptance /
resolve_effective_discovery_basis`; `survey_completeness_v2.
validate_profile_completeness`. State key is `lifecycle_state` (not
`lifecycle`); CAND requires `CANDIDATES_NORMALIZED` + machine
evidence/materiality/completeness `pending` + checkpoint_provenance null +
human pending/null + impl `48082356…` + profile `aff05fd5…`.

## Blocker (prepare REFUSES until cleared)

- `EFF-D123` r2 supplement row `supplement-src-8ebcb3c969d5baaf` pins a 65-char
  `raw_sha256` (malformed); true packet file + sidecar are 64-char
  `0cfdda19c8e1691b5226dd0d4949e2397051268e8a823c2fb61db94ea20c4ac0`
  1663475B. Harness enforces `hex64` on every row and raises before any active
  write. A corrected 64-char supplement row + independent re-review is required;
  then one bounded Root authorization for prepare. No semantic PASS is claimed
  from auth-file existence or from staging alone.

## Commands (record exact command at authorization; DO NOT RUN NOW)

All runs: `PYTHONDONTWRITEBYTECODE=1` (harness refuses otherwise),
`cwd=<repo_root>`, capture raw numeric exit/stdout/stderr (launcher pattern
below). Loaded modules must be e84 `scripts/...` with SHAs
`48742538…/5e195730…/0974c709…`; `__pycache__` must stay absent.

Prepare (after blocker cleared + Root auth; STOPS at READY, no removal):

```sh
E84=.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work
RET=notes/rephase-1-operational-rehearsal-resume-20261104/retention-SP-YYYYMMDDTHHMMSSZ
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 notes/rephase-1-operational-rehearsal-resume-20261104/sp-operator-harness-r4-20261104.py \
  --stage=prepare --retention-dir "$RET" --new-supplement-id r4-sp17-YYYYMMDDTHHMMSSZ \
  --staging-map-file notes/rephase-1-operational-rehearsal-resume-20261104/sp-staging-expected-manifest-r4-20261104.json \
  >"$RET/raw/prepare.stdout.txt" 2>"$RET/raw/prepare.stderr.txt"; echo $? >"$RET/raw/prepare.exit.txt"
```

Expected prepare outputs (packet-local + active NEW only; State/CP/Human/
config/schema/source/test untouched): retention dir + `raw/` +
`historical-context.json` + 17 staged `raw/sp17-*` (exclusive O_EXCL, 0o664,
SHA/bytes/mode verified) + NEW supplement + NEW proposed input +
FULL validation (supplement Raw-present; `validate_interactive_input` with true
non-DROP universe + real task_source_ids + real R/E lists; per-task
`_build_card_core/_validate_card_core`; `_build_view/validate_edition_view`;
`stable_task_id/_source_class` per supplement row) + `READY.json` with exact
pins/inventory. Any failure: STOP, preserve staged/NEW products + retention,
report exact partials, no retry loop. Do NOT proceed to dispose without fresh
independent re-review of READY + explicit READY confirmation.

Dispose (only after READY + separate explicit Root auth file):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 notes/rephase-1-operational-rehearsal-resume-20261104/sp-operator-harness-r4-20261104.py \
  --stage=dispose --retention-dir "$RET" --root-auth-file "$RET/../ROOT-AUTH-dispose-<id>.txt" \
  >"$RET/raw/dispose.stdout.txt" 2>"$RET/raw/dispose.stderr.txt"; echo $? >"$RET/raw/dispose.exit.txt"
```

Guards re-checked before EACH removal: READY pins + unchanged original
authority (State `4865998b…`, exact2 `ee13b8ee…/c60a9624…`, profile/DCP/SCP/
accepted SHAs) + `validate_agent_state==[]` + `require_research_operation_ready`
passes + phase inventory (pre-2a both present; pre-2b ledger absent EXPECTED +
completeness pinned; post-both absent; no reseal). Backup is exclusive
`O_CREAT|O_EXCL|O_NOFOLLOW` 0o664 + SHA/size/mode verify + manifest; then
exact `os.unlink` of the ONE canonical file. No glob/force/State reset/fake
`REQUEST_CHANGES`/weakening. No automatic restore/retry on any failure.

Retry (SEPARATE Root decision AFTER dispose; NOT in harness):

```sh
E84=.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work
ID=r4-sp17-YYYYMMDDTHHMMSSZ
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 "$E84/scripts/run_evidence_v2_interactive.py" \
  --repo-root "$E84" --state sources/SP-efficient-llm-2026/production-state.json \
  --input "sources/SP-efficient-llm-2026/evidence/proposed-input/interactive-evidence-$ID.json" \
  --supplement "sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-$ID.json" \
  >"$RET/raw/retry.stdout.txt" 2>"$RET/raw/retry.stderr.txt"; echo $? >"$RET/raw/retry.exit.txt"
```

Canonical outputs (under `sources/SP-efficient-llm-2026`, State stays CAND):
`evidence/v2/accepted/<new_result_set_sha>/evidence-accepted.json` +
`package.json` + archived `interactive-evidence.json` + `interactive-audit.json`
+ `evidence/v2/views/accepted/<new_view_set_sha>/edition-views-accepted.json` +
`materiality-ledger-v2.json` + `profile-completeness-v2.json`. On `refusing to
overwrite` / `incomplete pre-existing` / State drift: STOP, preserve orphans +
backups + survivors + new products, report exact partials, require a new
bounded observation/decision. No test run substitutes for this authority run;
no fabricated approval.

Stop at Human Commit Point after results + independent review. Whole NOT_READY /
step4B3 OPEN / audit unstarted / DM021+022 OPEN; quality/adoption/savings OPEN.
