# Mechanical-only receipt/Gate refresh — operational contract analysis

- Actual clock: **2026-09-28T01:36:16.3738037+09:00** (`Get-Date -Format o`, reconstruct workdir, pwsh).
- Role: **General author-side SOURCE ANALYSIS Co-Worker.** Not implementer/test runner/independent auditor. No delegation, no benchmark/provider investigation. Root Astra owns design selection. No implementation authorization follows from this recommendation.
- Reconstruct (writable workspace): HEAD `d17560028bd5db459636ca957888b7369b5d5cda`, tree `df4b1324d35126c0a76b8c5d4166316d46f18fa7`, `git status --porcelain=v1` empty at analysis. Human commit; ordinary commit/Push Human-owned.
- Fixed source (read-only): `/tmp/jgas-rephase-gate-cli`, branch `codex/rephase-1-gate-cli`, HEAD **`e4c82692abee6acedbba07815b0d74ccefb80a7e`**, tree **`bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`**, parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`, origin inert `https://example.invalid/rephase-increment-b.git`, status only `?? scripts/__pycache__/`, `?? tests/__pycache__/`. Read-only `rev-parse/log/show/branch/remote/status` + UNC `\\wsl.localhost\Ubuntu\tmp\jgas-rephase-gate-cli\...` reads at this head only. No checkout/reset/clean/apply/index/refs/commits/config edits/candidate writes/runtime imports/tests/network/production/main/Actions.
- Baseline referenced not inspected: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.
- Inputs: `outputs/rephase-1-weekly-regeneration-assessment.md` §Next task, `notes/rephase-1-weekly-regeneration/README.md`, `logs/20260927T160625Z/evidence-closeout.md`, corrected `contract-analysis.md` (use only corrected §§C0/1/4/6, not withdrawn draft claims), `witness-report-supplement.md`, `outputs/rephase-1-weekly-regeneration-decision.md` W0–W6. First/repeat same-byte witness complete within limits; **no scripts/tests rerun, no broad inventory repeated**.
- Legend: **[SOURCE]** exact bytes at `e4c8269` with path:line; **[INFERENCE]** combining cited guards, no execution; **[PROPOSAL]** not in source, needs root decision + later witness.

## 0. Minimal runtime/helper/test/doc inventory + caller flow

**[SOURCE]** Owners:

| Owner | Exact paths at `e4c8269` | Calls in refresh order |
|---|---|---|
| Weekly derivation | `scripts/survey_weekly_derivation_v2.py`: `load_derivation:448-543`, `build_receipt:607-639`, `validate_receipt:642-702`, `_verify_head_bytes:550-604`, `current_closure:546-547`, `build_reader_input:259-353`, `validate_reader_input:356-366`, `render_main:373-415`, `render_bibliography:418-434`, `validate_generated_closure:437-445`, `validate_survey_build_directory:73-96`, consts `READER_INPUT_SCHEMA:22`/`RECEIPT_SCHEMA:23`/`STYLE_PATH:24`/`CURRENT_CLOSURE:28-37`/`WEEKLY_BUILD_INPUTS/OUTPUTS:26-27` | strict derivation → old-receipt negative → new receipt build+replay |
| Weekly publisher (NOT refresh entry) | `scripts/survey_weekly_semantic_publication_v2.py:main:54-181`: `DRAFT_COMPLETE` guard `:67-68` pre-write, surface create-or-compare `:74-82`, review required `:99-114`, `_verify_head_bytes:118`, build-dir `:121-125`, six-output no-overwrite `:135-137`, render/copy/receipt `:139-153` | Shows why publisher rerun at `VALIDATED_DRAFT` is unsupported; do not add flag here (§5) |
| Gate | `scripts/survey_reader_surface_gate_v2.py`: `evaluate_reader_surface_gate:1121-1471` (overwrite `:1468-1469`), `validate_reader_surface_gate:1474-1674`, `_derivation_for_manuscript:1071-1118`, `load_and_validate_reader_surface_semantic_review:884-1045`, CLI `main:1796-1928` (`scan-manuscript:1866-1925`, `validate-gate:1829-1842`) | CLI-equivalent renew + independent validate |
| Agent control | `scripts/survey_agent_control_v2.py`: `_publication_revalidation_roles:680-688`, `_pending_conditions:691-703`, `_collect_pending_rows:706-738`, `_verify_pending_binding:741-776`, `built_checked_pending_publication_basis:779-803`, `revalidate_publication_surface:1554-1808` (pre-write recheck `:1777-1782`, bounded rollback `:1800-1807`), `_validate_checkpoint_record:263-344`, `_validate_agent_state:352-494`/`validate_agent_state:347-349`, `_resolve_publication_revalidation:1085-1182`/`resolve_active:1079-`, `_check_immutable_rows:842-944`, `_check_chain:947-1012`, `_check_agreement:1015-1076`, `_verify_preserved_provenance:1495-1552`, `_revalidation_record_path:652-654`, `_revalidation_surface_roots:674-677`, `_PendingPublicationBasis:56-68`, `_revalidation_row_path:806-813`, consts `REVALIDATION_BASENAME:43`/`REASON_CLASSES:44`/`CHAIN_LIMIT:45`, CLI `main:1830-1932` (`revalidate-publication-surface:1856-1862`) | pending basis + existing revalidation only |
| Core/tool | `scripts/survey_production_v2.py`: `repository_commit_sha:129-147`, `contract_identity:150-168`, `sha256_bytes/file/object:95-105`, `repo_local_path:222-`, `write_json:90-92` (single-file, `mkdir -p` + `write_bytes`, NOT atomic), `load_json:78-83`, `DEFAULT_CONFIG:26`; `scripts/survey_agent_tool_v2.py`: `verify_current_stage_basis:42-50`, `current_stage_basis_override:122-143`, `run_helper:146-179` (allowlist screening/evidence only) | HEAD/contract/hash/path primitives |
| Review criteria | `scripts/survey_reader_publication_v2.py`: `_extra_review_checks:397-418`, `_expected_review_checks:421-439`, `validate_review_record:544-635` (`:620-623` family equality + `fidelity.validate_review_depth`), `build_review_record:458-541`; `scripts/survey_quality_v2.py:expected_checks:80-105`; `config/publication-review-v2.json` (core/semantic `PUBLICATION_BOUNDARY,ARCHITECTURE_CONTENT_FIDELITY,FINAL_SYNTHESIS_QUALITY` + `WEEKLY/WEEKLY_MAGAZINE` lanes); `scripts/survey_stage_validation_v2.py:DRAFT_COMPLETE:464-521`/`VALIDATED_DRAFT:523-573` | criteria closure (§2) |
| Config/schemas | `config/survey-production-v2.json`: `contract_files.pipeline:6-70` + `quality:71-75`, `implementation_control_roots:87` (`config,schemas,scripts,.github/workflows`), `stage_plan.DRAFT_COMPLETE.artifacts:338-345` (6 names), `state_authority:389-401` (`production-state.json:390`, arch approval `:397`); schemas `reader-surface-input-v2`/`weekly-publication-source-manifest-v2`/`reader-surface-gate-v2`/`reader-manuscript-v2`/`publication-review-record-v2`/`reader-surface-semantic-review-v2`/`stage-checkpoint-v2`/`publication-surface-revalidation`/`survey-production-state` | control/criteria bytes |
| Tests (existing, not rerun) | `tests/test_survey_gate_cli_persisted_review_v2.py` (32-method e4c8269 PASS), `test_survey_publication_revalidation_v2.py`, `test_survey_increment_b_weekly_derivation_v2.py`, `test_survey_increment_b_boundary_matrix_v2.py`, `test_survey_weekly_evidence_authority_v2.py`, `test_survey_semantic_publication_v2.py`, `test_survey_stage_validation_v2.py`, `test_survey_reader_surface_gate_v2.py`, `test_survey_agent_control_v2.py`, `test_survey_agent_tool_v2.py` | future refresh tests extend these, not saved harnesses |
| Docs | `docs/survey-production-core-v2-*.md` are pipeline/quality contract bytes (via `aggregate_file_hash:108-118`), not runbook authority | do not treat reference hashes as preflight proof |

**[INFERENCE]** Caller flow for same-byte refresh (library-equivalent of existing CLIs, no new producer): `load_derivation` strict → old negatives → `build_receipt` (current HEAD) → `validate_receipt` new → `evaluate_reader_surface_gate` (same args as `scan-manuscript` strict persisted-review path) → `validate_reader_surface_gate` new → `built_checked_pending_publication_basis` → `revalidate_publication_surface(REVIEWED_CORE_CHANGE)` → active readback. Publisher `main` is not in this flow.

## 1. Prior authority without bypass [answers Next-task 1]

**[SOURCE]** Full current validators intentionally reject old bytes after committed helper change: `validate_receipt:661` → `_verify_head_bytes:571-576` (control diff) / `:595-604` (closure drift) / `:663-665` (contract); `validate_reader_surface_gate:1660-1665` → `_derivation_for_manuscript:1093-1101` → old `validate_receipt`. This is old-artifact reuse failure, not State invalidation: `_validate_checkpoint_record:322-330` checks recorded contract/implementation, `verify_current_stage_basis:42-50` pins supplied SHA to current HEAD only for new work (corrected analysis §C0.2).

**[PROPOSAL]** Bind old identities without invoking current-tool validators and without new private validator:

| Old identity | Bind to live authority (explicit `==`, no skip/error-string filter) |
|---|---|
| Old Gate hash | If pointer null: `state.checkpoint_provenance.validation{path,sha256}` → `core.sha256_file(checkpoint)==ref.sha` (`_collect_pending_rows:707-712`), load checkpoint via `CHECKPOINT_SCHEMA` (`:713`), identity `issue_id/from DRAFT_COMPLETE/to VALIDATED_DRAFT/checkpoints has validation` (`:714-715`); checkpoint `artifacts` row `reader-surface-gate{path,sha256}` must `== core.sha256_file(old Gate path)` + `byte_count==stat().st_size`. If pointer non-null: resolve predecessor `live=False` (`built_checked:790-792`, `_resolve:1085-1153` checks `prior_checkpoint==validation_ref:1130-1132`, row union `:911-912`, chain `:1151-1153`); effective map `new_sha/preserved sha` (`:913-920`) for `reader-surface-gate` must `== core.sha256_file(old Gate)`. |
| Old receipt hash | Old Gate `derivation.receipt{path,sha256}` (`_derivation:1095,1118`) must `== {rel(receipt_path), core.sha256_file(old receipt)}`; receipt path must be `surface_path.parent/validated-source-manifest.json` (`:1093`). Also `receipt.reviewed_reader_input=={surface path, sha}` (`:1098-1099`) and `receipt.semantic_review=={review path, sha}` (`:1100-1101`). |
| Old digest/schema | Recompute `receipt_sha256==sha256_object(base without digest)` (`validate_receipt:645-648`) and `gate_sha256==sha256_object(14 digest fields)` (`validate_gate:1522-1542`) on raw bytes + `schema_gate.validate_instance` against `RECEIPT_SCHEMA`/`SURFACE_GATE_SCHEMA` (no tool checks). Raw-byte hash only; never parsed-object hash (closeout §3/§4). |
| Ancestry/source | `git cat-file -e old_commit^{commit}` (`_verify:552-557`) + `git merge-base --is-ancestor old_commit HEAD` (`:558-563`) as narrow check; `core.sha256_file` of every `accepted_refs`+`authored_refs` row `==` recorded sha (`validate_receipt:656-659` pattern) for BOTH old and new receipts; `reviewed_reader_input` bytes `==` disk (`:682-684`); scanned surfaces bytes+`byte_count` `==` disk (`validate_gate:1605-1621`); manuscript/primary binding (`:1561-1603`) + issue/profile (`:1583-1592`, `:1504-1511`); semantic authority `require_pass` + `review_sha/surface_sha/path` (`:1643-1658`). |
| Expected manuscript/surfaces/review | `expected_manuscript_path` mandatory (no standalone fallback, `:1496-1498`); exactly one `MANUSCRIPT_MANIFEST` + one `PRIMARY_SOURCE` (`:1548-1559`); semantic review via strict loader `884-1045` (digest `:926-931`, `READER_PIPELINE_INDEPENDENCE:949-958`, detail/locs `:960-967`, PASS gates `:969-980`, surface drift `:992-1011`). |

No extraction of private checked-prior validation is necessary. **[INFERENCE]** Historical validity is inherited: checkpoint `DRAFT_COMPLETE` admission already ran `validate_gate→validate_receipt` (`stage:510-520`), revalidation chain pins predecessor rows byte-identical (`:865-872,:911-912,:977-978`). Re-proving old tools would need a read-only helper pinning `expected_commit/contract/closure` to old values — new surface for old-tool replay, risks `skip` boolean / `except ValueError→pass` anti-patterns. **Do not weaken public `validate_receipt/validate_gate`; do not catch their errors as equality signals.** Every guard above is a direct hash/bytes/set comparison raising on mismatch.

Non-row gap **[SOURCE]**: `_collect_pending_rows:721` iterates `record["artifacts"]` only; receipt (`publication/v2/validated-source-manifest.json`), `--input` envelope, drafting archive, `reader-surface-input-v2.json` are absent from `DRAFT_COMPLETE.artifacts:338-345` + gate role `:687`, so pending map neither authorizes nor rejects them (corrected §C0.1). **[PROPOSAL]** Their old/new equality must be actual checks: `accepted_refs` list-`==`, `authored_refs` (exactly 2, `publication-semantic-input`+`drafting-authored-archive`, `:650-651`) list-`==`, `reviewed_reader_input{path,sha}` `==`, `semantic_review{path,sha}` `==`, `outputs.{primary,bibliography,style}.{path,sha}` `==` (same deterministic bytes `:688-701`), each row's disk sha `==` both receipts. `current_tools{commit,contract,closure}` + `receipt_sha256` + `production_state_basis.historical_sha256` (if State unchanged) are the only allowed differences; `lifecycle_state: VALIDATED_DRAFT` provenance needs root call (blocker B6).

## 2. Criterion/control closure [answers Next-task 2]

**[SOURCE]**

| Set | Exact bytes |
|---|---|
| `_verify_head_bytes` control_paths `:564-568` | `DEFAULT_CONFIG` + `cfg.implementation_control_roots` (`config,schemas,scripts,.github/workflows`) + `STYLE_PATH` + all `cfg.contract_files.pipeline+quality` values, sorted uniq; `git diff --quiet commit HEAD -- controls` (`:571-576`), dirty (`:577-582`), untracked non-pyc (`:583-591`) |
| `CURRENT_CLOSURE:28-37` | 5 helpers + `READER_INPUT_SCHEMA` + `RECEIPT_SCHEMA` + `STYLE_PATH`; completeness (`:592-594`), disk (`:596-598`), `git show {commit,head}:name` (`:599-604`) |
| `contract_identity:150-168` | `pipeline_contract_sha` over pipeline files+config+profile+state schemas, `quality_contract_sha` over 3 historical docs, profile version/sha; checked `:663-665` |
| Review criteria | `_expected:421-439` = `quality.expected_checks:80-105` (AGENT_SEMANTIC/VISUAL slice) ∪ `_extra:397-418` over `config/publication-review-v2.json` lanes; enforced `validate_review_record:620-623` (`check family differs`) + `fidelity.validate_review_depth`; semantic loader `884-1045`; Gate semantic authority `1624-1658`; bundle `PASS` + PDF binding in revalidation `:1722-1726,:1726` |

**[INFERENCE]** Comment-only witness (`survey_weekly_derivation_v2.py` one blob, same surface/outputs) does NOT license broad code changes. Same complete reader object is semantic equality only within trusted existing renderer contract (`build_reader_input:259-353` pure projection + `validate_reader_input:356-366` + `render_main/bib` deterministic). Same sample output with changed renderer does not prove same function.

**[PROPOSAL]** Bounded file-level allowlist (no AST/semantic classifier/framework):

- Criteria/control bytes that must be `git show old:show HEAD` byte-identical (`sha256_bytes` equal): `config/publication-review-v2.json`, `config/survey-production-v2.json` (whole file — strict but simple; any config change exits mechanical path), all `schemas/*`, `templates/survey/jgaisurvey.sty`, `scripts/survey_reader_publication_v2.py`, `scripts/survey_reader_surface_gate_v2.py`, `scripts/survey_quality_v2.py`, fidelity/review-attention helpers, `scripts/survey_stage_validation_v2.py`, `scripts/survey_agent_control_v2.py` (except the new refresh subcommand itself — new HEAD only).
- Allowed diff: only within `CURRENT_CLOSURE` helper `.py` files (practically `survey_weekly_derivation_v2.py` as witnessed; extend to other 4 helpers only by root exception), verified by `git diff --quiet old HEAD -- <criteria paths>` == 0 AND `git diff old HEAD -- <control_paths>` non-empty only inside allowed helpers.
- Plus semantic sample proof: recomputed `context[surface]==reviewed` (`:686-687`) AND `render_main/bib` bytes `==` receipt `outputs` (`:688-701`) AND existing reviews still `validate_review_record` (catches added/removed check, supplement N3 `check family differs`).
- Retain current-source `clean+ancestor` (`:552-563,:577-604`) for new receipt; old commit ancestry via narrow check (§1).

Cost/limit: file-level allowlist is coarse — allows behavior-changing edits inside one helper that preserve one sample's output while breaking other inputs; full semantic proof would need full input-space reasoning (rejected as generic framework). This bound trades completeness for auditability: any criteria touch or multi-file control drift stops the mechanical path and requires full re-derivation/review. `VISIBLE_TEXT:38-50` lives inside allowed helper yet feeds reader input (`:348`) — output-equality check covers it per-sample only; root must accept this residual (blocker B3).

## 3. Owned outputs + retention [answers Next-task 3]

**[SOURCE]** Live writes only:

| Write | Canonical path | Existing API/behavior |
|---|---|---|
| Receipt | `<source_root>/publication/v2/validated-source-manifest.json` (publisher `:132`; Gate derivation `:1093`) | `weekly.build_receipt:607-639` + `schema_gate.validate_instance` (publisher `:152` pattern); publisher refuses existing `:135-137` — refresh overwrite needs explicit root authority (blocker B1). Receipt is non-row (absent §0 config+roles) so pre-Gate write causes no checkpoint drift |
| Gate | `<source_root>/publication/v2/reader-surface-gate-v2.json` (roles `:687`) | `evaluate_reader_surface_gate:1121-1471`, overwrite existing `:1468-1469`; Gate IS row → intended drift → pending basis `replacements=[reader-surface-gate]` |
| Revalidation record | `<source_root>/publication/v2/publication-surface-revalidation-rN.json` (`_revalidation_record_path:652-654`, sequences `:657-671`, collision `:1737-1738`) | `revalidate_publication_surface:1554-1808` only; `reason_class REVIEWED_CORE_CHANGE:44`, `supersedes` null (first, `:1728-1735`) or prior pointer |
| State pointer | `<source_root>/production-state.json` (`state_authority:389-390`, canonical `:784-785`) | `core.write_json(state_path, updated{publication_revalidation_provenance:{path,sha256}}):1789-1794` + post `validate_agent_state:1797-1799`; rollback `:1800-1807` covers only record+State |

**[PROPOSAL]** Retain BOTH superseded bytes before any live replacement. Inert dir OUTSIDE `survey_root` (else `validate_survey_build_directory:73-96` 6-name allowlist breaks): `<source_root>/publication/v2/.refresh-retention/<UTC-run-id>_<old8>_<new8>/` (never under `survey_root`, never consulted by validators — provenance only, not approval ledger).

- Before P2: `cp` raw `validated-source-manifest.json` → `receipt-superseded-<old8>.json`, raw `reader-surface-gate-v2.json` → `gate-superseded-<old8>.json`; path safety via `core.repo_local_path` + `is_symlink→refuse` + `is_file→require` (`_revalidation_row_path:806-813` pattern) + destination `exists/is_symlink→refuse` (no-overwrite, cf. `_write_json:34-37`, `build_review_record:537-538`).
- Manifest `retention.json` (plain JSON, NO new schema — blocker if schema demanded): `{run_id, recorded_at, old_commit, new_head, old_receipt:{path,sha256(raw bytes),byte_count}, old_gate:{...}, state:{path,sha256}, checkpoint_ref, predecessor_ref, reason_class}`. Minimum hashes are raw-byte `sha256_file`, not parsed-object hash (closeout lesson). Validators never read this dir (state this invariant in code comment + review).
- History integrity **[SOURCE]**: `r1.prior_checkpoint==validation_ref` (`:1126-1140`), `superseded.prior_sha==checkpoint sha` (`:865-866`), `preserved.sha==checkpoint sha` (`:901-902`), row union `==` prior rows (`:911-912`); `r2.prior_checkpoint` still original checkpoint, `r2.supersedes==r1 pointer` (`:1728-1734`), chain `prior_checkpoint` equal (`:977-978`) + chronology (`:981-988`) + linked rows `live=False` (`:1005-1007`); live checks disk vs `new_sha` (`:889-893,:909-910`) + agreement (`:1015-1076`). Never rewrite checkpoint/revalidation records; supersession via pointer only.

## 4. Failure protocol [answers Next-task 4]

Existing rollback (`:1783-1807`) covers record+State only, not receipt/Gate. **[PROPOSAL]** Minimal narrow wrapper (caught exceptions only; crash → manual):

- P0 pre-write (no retention yet): `_pending_conditions:691-703` + strict State + old-authority binding (§1) + equality/criteria (§2) + `HEAD==snapshot` + clean (`:577-592`). **No-op refused here**: if `built_checked_pending` would show no replacements (`:736-737`) or `resolve_active` already validates (`:1577-1579`), refuse before retention writes. Idempotent success is NOT selected (preserve guard).
- P1 retention (first write, inert only): snapshot old receipt/Gate/State bytes+hases+HEAD; write retention copies (no-overwrite). Retention failure → abort, no live writes.
- Commit point: successful `revalidate_publication_surface` return (`:1808`) + post State valid (`:1797-1799`). After this, snapshots are evidence only; no restore.
- Ordinary (caught `Exception`, process alive) restoration — ONLY IF `State sha==pre-write snapshot` AND `HEAD==snapshot` AND written bytes `==` just-written new hashes (re-`sha256_file`): P2 failure (new receipt invalid) → restore receipt from retention, verify `==old sha`; P3 failure (Gate CLI non-zero) → if Gate `==old` restore receipt only, elif Gate changed restore both; P4 failure (revalidation `AgentControlError`, incl. pre-write recheck `:1777-1782`/State-bytes `:1780-1782`) → revalidation's own rollback already restored State/deleted record (`:1801-1806`); wrapper additionally restores receipt+Gate to old snapshots. Any external drift (`State/HEAD/Gate/receipt != expected`) → NO blind restore; fail-closed, keep retention+live bytes, require manual recovery. Never `except→pass`, never error-string matching: recheck via hash `==`, restore via `write_bytes(retention_bytes)` + verify.
- Crash/interruption (kill, power, `SystemExit` outside `try`): no auto-restore promised (single-file `write_json:90-92` is non-atomic; multi-file receipt+Gate+record+State cannot be atomic — state this). Retained evidence + manifest + `fail-closed manual recovery` (inspect `retention.json` vs live `sha256_file`, either complete manually with same inputs or copy retention bytes back, then re-validate) is acceptable if explicit. Document as such; do not add transaction manager/resolver/history framework.
- Concurrency: check-then-write (`snapshot→recheck→write`) races remain. No lock exists; `pending HEAD changed` (`:760-761`), `row snapshot changed` (`:765-767`), `State bytes changed` (`:756-757,:1781-1782`), `sequence collision` (`:1737-1738`) catch some interleavings but receipt/Gate clobber is still possible. Require external single-writer serialization (Human commit discipline); cooperative lock NOT proposed (would be new framework). State this limit.
- Read-only classifier CLI is NOT selected (corrected §C0.4; assessment Next-task).

## 5. Entry selection [answers Next-task 5]

**[PROPOSAL]** New explicit subcommand in existing agent owner: `survey_agent_control_v2.py: main:1830-1932` add `refresh-mechanical-evidence` (name root-final):

```
agent-control --repo-root . --config config/survey-production-v2.json refresh-mechanical-evidence
  --state <source_root>/production-state.json --manuscript <.../reader-manuscript-v2.json>
  --reason <non-empty> --executor <identity> [--recorded-at <iso>] [--retention-dir <default .refresh-retention>]
  [--implementation-sha <must == HEAD if given, cf. :1620-1621>]
```

- Why here: agent control already owns `VALIDATED_DRAFT` gates (`:691-703,:1580-1593`), pending basis (`:779-803`), revalidation (`:1554-1808`) and imports `weekly/surface_gate` (`:31-36`); Weekly publisher is `DRAFT_COMPLETE`-only (`:67-68`) — adding a `VALIDATED_DRAFT` flag there would perturb initial semantics (forbidden). Gate CLI stays callee (library-equivalent args: `manuscript, semantic_review_path=persisted review, output=gate path, state_path`, preserving strict loader `1880-1885`).
- Size: ~4 small helpers (bind-old-authority, check-equality-criteria, retain, recheck-restore) + subcommand glue, reuse `build_receipt/validate_receipt/evaluate/validate/built_checked/revalidate/active-readback`; <250 runtime lines, no new schema/producer, no Weekly/Gate CLI semantic change, no giant wrapper extraction. Handwritten artifacts/ad-hoc witness scripts are NOT the operational route.
- Deferred (unchanged dispositions): build transfer/compile-exact-source/canonical-root admission/PDF changed-output (`validate_survey_build_directory:73-96`, Explore boundary), Special/support, DM-001/003/004, optional findings transport, Candidate-stage/TeX/visual/Human Gates, Windows/Actions, lifecycle savings.

## 6. Minimal acceptance matrix (fresh fixture + fresh log target per case; separate OS processes post-commit with `helper_sha+HEAD` logged — supplement §A)

| ID | Setup | Pre-write oracle | Ordinary-failure oracle (caught) |
|---|---|---|---|
| T1 first | null pointer, comment-only helper commit, all §1/§2 equal | old receipt/Gate reject with specific messages (`implementation or contract changed`, `reviewed target mismatch`/`derivation mismatch`); new receipt+Gate `validate_*` pass; `replacements==[reader-surface-gate]`; r1 `supersedes null`, active readback pass; retention raw hashes `==` pre-refresh live | n/a (success) |
| T2 repeat | intact r1 + second comment-only commit | same as T1 + `r1 sha` unchanged, checkpoint unchanged, r2 `supersedes r1`, chain pass | n/a |
| T3 output-change | same surface, edited `render_main` so `main.tex` differs | refuse P0 (`deterministic primary replay mismatch:700-701`); no retention/live/State/record change | — |
| T4 accepted-drift | Evidence card / matrix / ledger byte change | refuse P0 (`accepted authority differs:671-672` / `card SHA drift:165-166`); no writes | — |
| T5 authored-drift | cover/`final_summary`/closing change | refuse P0 (`recomputed reader input differs:686-687` / authored envelope `:119-153`); no writes | — |
| T6 criteria-change | add check to `publication-review-v2.json`, same review bytes (supplement SN-n3) | refuse P0 (`check family differs:622-623` + criteria `git diff` non-zero); strict State `[]` noted but NOT used as guard; no writes | — |
| T7 malformed authority | bad pointer/checkpoint/digest/duplicate | refuse P0 (`SHA mismatch`/`prior SHA mismatch:865-866`/`digest mismatch`/`duplicate:724-725,851-857`); no writes | — |
| T8 dirty/HEAD drift | untracked control file / dirty control / HEAD moved after snapshot | refuse P0/P1 (`uncommitted source:587-591` / `HEAD changed:760-761` / `State bytes changed:756-757`); no live writes (retention for P1 race kept as aborted evidence) | — |
| T9 write race | concurrent Gate overwrite between snapshot and P2 | recheck `sha!=snapshot` → abort before live write; State/record listing unchanged | if race after P2/P3 but State intact → restore owned bytes to snapshots, verify, no new State/record; if State drifted → manual |
| T10 post-write QA fail | Gate CLI fail after receipt replaced; revalidation fail after both replaced | — | restore receipt (+Gate) iff State/HEAD/written bytes intact; else manual; assert `State sha` + record listing unchanged, live `==old` (restored) |
| T11 no-op | no control change, active validates | refuse P0 (`nothing to supersede:1578-1579`) BEFORE retention; no writes | — |

Harness rules for all: assert specific message substrings (never bare-`Exception` sentinel — closeout §1 N1/N2 lesson); assert `State sha` + `revalidation -r*.json` listing invariance + live file shas per window (receipt-only / gate-only / record+State, supplement §C); fresh imports per process; never `reset --hard`/`clean`/saved-harness rerun; harness policy refusals separated from runtime rejections (decision W6). Independent fixed-head review later; green here is not audit/adoption.

## 7. Preferred protocol (proposed, root decision required)

```
P0 refuse-before-retention: lifecycle VALIDATED_DRAFT+approved/arch+pending preview/freeze/release+inactive exception (:691-703,:1580-1593)
  + checkpoint/active predecessor intact (§1) + old Gate/receipt binding (§1) + accepted/authored/surface/render/review/QA+criteria equal (§1-§2)
  + HEAD==repo HEAD + clean controls (:577-592) + no-op check (:736-737,:1577-1579). Any fail → exit 2, no writes.
P1 retain: snapshot {old receipt, old gate, state, HEAD, checkpoint_ref, predecessor_ref}; mkdir retention (no-overwrite);
  cp raw bytes + retention.json (raw shas). Fail → exit 3, no live writes.
P2 receipt: recheck snapshots==disk; receipt=build_receipt(current HEAD/contract/closure, same accepted/authored/surface/review/outputs);
  write receipt (overwrite with explicit authority B1); validate_receipt(new) incl. _verify_head_bytes+contract+replay. Caught fail → restore iff §4 else manual.
P3 gate: recheck; evaluate_reader_surface_gate(manuscript, persisted semantic_review_path, output=gate path, state_path) [CLI-equivalent];
  validate_reader_surface_gate(new, expected_manuscript_path, state_path). Caught fail → §4 restore/manual.
P4 revalidate: recheck; basis=built_checked_pending (must be exactly replacements=[reader-surface-gate]); revalidate_publication_surface(REVIEWED_CORE_CHANGE,reason,executor,recorded_at,implementation_sha==HEAD);
  active readback (hashes+chain+agreement). Caught fail → wrapper restore iff §4 else manual. Success = commit point.
```

## 8. Exact blockers requiring root decision

- B1 receipt-overwrite writer authority (publisher `:135-137` refuses existing; Gate overwrite `:1468-1469` exists). Grant narrowly to `refresh-mechanical-evidence` for exact `publication/v2/validated-source-manifest.json` at pre-decision `VALIDATED_DRAFT` only, or deny.
- B2 retention dir + manifest (proposed `<source_root>/publication/v2/.refresh-retention/<run-id>_<old8>_<new8>/` + raw `receipt/gate-superseded` + `retention.json` with raw shas/byte_counts/commits) + `validators never read it` invariant. Confirm no new schema.
- B3 criterion allowlist: whole-config+schemas+review/quality/fidelity/stage/agent files identical `old vs HEAD`, diff allowed only in `CURRENT_CLOSURE` helpers; accept comment-only witness does not prove semantic preservation + `VISIBLE_TEXT` residual. Loosen/tighten per root.
- B4 failure semantics: narrow caught-only restore iff snapshots intact else fail-closed manual; no atomic multi-file promise; single-writer serialization with no lock. Accept crash-manual classification.
- B5 entry: `agent-control refresh-mechanical-evidence` with above args (no Weekly `DRAFT_COMPLETE` change, no new file, Gate CLI stays callee). Approve name/args/owner.
- B6 `production_state_basis.lifecycle_state=VALIDATED_DRAFT` on new receipt (not reconstructed `DRAFT_COMPLETE`) — acceptable provenance?
- B7 `REVALIDATION_CHAIN_LIMIT=32` bound for repeated refreshes — acceptable or need rotation?
- B8 review-reuse check: byte binding + `_expected_review_checks` set equality + semantic-loader `require_pass` sufficient, or explicit extra assertion?

Smallest coherent increment (if root grants B1–B8): **R1** — new `refresh-mechanical-evidence` subcommand (~4 helpers, <250 lines, no schema/producer/semantic change) + focused tests (T1/T2 + T3–T8/T10–T11 representative, explicit-message + no-write/restore oracles, fresh fixture/processes, no saved-harness reuse) + this contract disposition. Stop on first fail-closed rejection; return exact call/bytes. Changed-output/build/PDF/Special/DM/findings/candidate-stage excluded. Requires fresh exact-head review + seven-point audit before any adoption; this analysis alone authorizes nothing.

## 9. Honest limits

Same-byte only; one-sample output equality ≠ function equivalence (§2); no atomic publication, no concurrent-writer safety, no Windows/Actions/CI, no Candidate-stage/TeX/real review/PDF preflight, no all-profile/support, no lifecycle savings, no history rewrite, no new approval ledger. Missing-initial-Gate-bytes lesson (closeout §3) is why §3 retains both bytes. Broad-exception/stale-import/reset-clean flaws (closeout §§1/6, supplement §§A/D/F) are excluded from R1 by §6 rules.

## 10. Files/verification

- New file only: `notes/rephase-1-mechanical-refresh/operational-contract-analysis.md` (this doc). No handoff/assessment/AGENTS/candidate/test/doc edits; no candidate objects/commits; no runtime/tests/imports executed for this analysis.
- Identity re-verified read-only at analysis clock (see header). Prior B/CLI/witness conclusions and limitations retained; no PASS transfer to new HEAD.

## 11. Correction — root provisional decisions (2026-09-28T01:46:05.7559302+09:00)

Role unchanged (source analysis only, no code/tests). Source re-verified at correction clock; identities in header unchanged. **[CORRECTION]** marks where §§1/4/7/T11 and related claims were wrong; root text prevails unless source evidence below shows infeasibility (none found blocking, two honest deferrals noted).

### C1. No-op / pending timing [CORRECTION of §§4/7/T11]

- **[CORRECTION]** Prior P0 `built_checked_pending` + `resolve_active succeeds → no-op` is infeasible. **[SOURCE]** `built_checked_pending:779-803` calls `_collect_pending_rows:789` with default `require_change=True`; `706-738:736-737` raises `requires changed publication bytes` when nothing changed. It cannot classify no-op before Gate replacement. Prior T11 oracle (`nothing to supersede:1577-1579` before retention) conflated revalidation-time refusal with pre-retention classification.
- **[SOURCE]** Repeat pre-refresh healthy state is strict-pass + intact active: supplement S2 `helper_sha=18a88161… HEAD=b41c58f2… strict State passes with intact r1` (supplement §A); `load_derivation:454-460` stays strict when checkpoint rows untouched (no pending basis built). Witness proves intact active BEFORE renewed Gate is expected for repeat.
- **[PROPOSAL revised]** P0: require `validate_agent_state==[]` strict + `resolve_active_publication_revalidation live=True` returns `(None,[])` (first) or `(record,[])` (repeat, current bytes valid) — never `live=False` for healthy preflight (§C2). No `built_checked_pending` in P0. No-op refusal is explicit old→current control/closure difference: if `git diff --quiet old_commit HEAD -- <control_paths>` (`weekly:571-576` pattern) == 0 AND old closure rows == current closure rows (names/cardinality+shas, `:592-604`), then artifact-only head change still satisfies old receipt (`_verify_head_bytes` passes) → no mechanical need → refuse `MECHANICAL_REFRESH_NO_OP` before retention. Do not call `resolve_active succeeds` a no-op.

### C2. Checkpoint rows / Gate digest / LIVE preflight [CORRECTION of §1 table]

- **[CORRECTION]** Checkpoint `artifacts` rows are `namedAuthority{name,path,sha256}` only, no `byte_count`. **[SOURCE]** `schemas/stage-checkpoint-v2.schema.json:$defs/namedAuthority required [name,path,sha256], additionalProperties false`. Prior §1 `+ byte_count==stat()` for checkpoint Gate row is withdrawn. `byte_count` belongs to Gate `scanned_surfaces{path,sha256,kind,byte_count}` (`reader-surface-gate-v2.schema:33,47`), revalidation `superseded{prior,new,byte_count}` + `validation.pdf{path,sha,byte_count,page_count}` (`publication-surface-revalidation.schema:86,125`).
- **[CORRECTION]** Gate digest is 13 fields, not 14. **[SOURCE]** `survey_reader_surface_gate_v2.py:1522-1536` lists `schema_version,issue_id,publication_profile,status,scanned_surfaces,rules_checked,suppressions,findings,summary,evaluated_by,recorded_at,semantic_authority,derivation` (13). Prior `14` withdrawn.
- **[SOURCE]** `resolve_active:1079-1082` = `_resolve(...,live=True)`; `live=True` checks live manuscript/bundle/reviews/PDF (`:1154-1177`) + chain (`:1178`) + agreement (`:1179`), while `live=False` skips live disk-vs-`new_sha` (`_check_immutable:889-893,909-910` guarded by `if live`). Healthy preflight MUST use `resolve_active LIVE` (current bytes verified). Existing pending code uses predecessor `live=False` only after owned Gate change (`built_checked:790-792`, `_resolve:1151-1153`). Prior §1 `live=False` for repeat pre-refresh is withdrawn.
- First/repeat effective Gate row **[SOURCE/PROPOSAL]**: first = checkpoint `artifacts` unique `(name=reader-surface-gate,path=canonical:687)` row sha; repeat = active record effective map (`:913-920` superseded `new_sha` ∪ preserved `sha`) entry for same unique key, with `seen==prior_rows (:911-912)` guaranteeing uniqueness. Old Gate raw `sha256_file==` that effective sha (explicit `==`).

### C3. Private non-authoritative inspection (no duplication) [CORRECTION of §1 “no new private validator”]

- **[CORRECTION]** Pure hash-anchoring still duplicates ~190-line Gate structural+semantic binding and risks missing post-derivation unresolved findings (`:1667-1672` after derivation `:1660-1665`). Root preference accepted as feasible.
- **[SOURCE]** `validate_reader_surface_gate:1474-1674`: schema/digest `:1500-1542`, scanned uniqueness `:1544-1559`, manuscript binding `:1561-1603`, scanned bytes+counts `:1605-1621`, semantic authority `:1623-1658`, derivation replay `:1660-1665`, unresolved BLOCKING `:1667-1672`.
- **[PROPOSAL]** Smallest extraction in `scripts/survey_reader_surface_gate_v2.py` (existing file, no new authority): new `_inspect_gate_record(repo_root,path,expected_manuscript_path)` = lines `:1500-1658` + `:1667-1672` moved verbatim, returning `{payload,manuscript,validated_sem,scanned}` without calling `_derivation_for_manuscript`. Rewrite `validate_reader_surface_gate` to `inspect=...; expected=_derivation_for_manuscript(...:1660-1663); if payload[derivation]!=expected: raise; return payload` — ordinary callers stay strict, no `skip` param/public bypass. Refresh calls `inspect` ONLY after old Gate raw hash anchored to strict checkpoint/active effective row (§C2), then independently checks receipt link (`derivation.receipt:1095,1118` + `:1098-1101`) + historical closure (§C4). Public readback after install remains full `validate_*`.
- Receipt: same pattern in `scripts/survey_weekly_derivation_v2.py` if concrete reuse shown: extract envelope/input part `validate_receipt:643-659` (schema/digest/state_file/authored names/disk-sha) + surface/output recompute `:682-701` into `_inspect_receipt_inputs(...)` without tool-pinning `:660-665`; public `validate_receipt` calls inspect then pinning+`load_derivation:666-672`. Propose only if implementation shows verbatim reuse; otherwise refresh does explicit `sha256_file==` per row (no logic fork). No promise `<250 lines` — count after extraction.

### C4. Criteria policy (single helper file) [CORRECTION of §2 allowlist]

- **[PROPOSAL revised per root]** Initial allowed executable diff ONLY `scripts/survey_weekly_derivation_v2.py`. All other `implementation_control_roots:config:87` (`config,schemas,scripts,.github/workflows`) + `STYLE_PATH` + all `contract_files.pipeline:6-70/quality:71-75` files must be `git show old:HEAD` byte-equal (`sha256_bytes` `==`). Current clean verified with existing `_verify_head_bytes:577-592` at CURRENT HEAD (dirty/untracked), not a new checker.
- **[SOURCE]** Historical closure: `expected_names==CURRENT_CLOSURE:592-594`, disk `:596-598`, `git show {commit,head}:name sha==row sha:599-604`. Require bytes at recorded `old_commit` (not just `cat-file -e`/`is-ancestor:552-563`), names/cardinality exact. Added/removed/renamed/mode-changed fail via control diff `:571-576` (mode counts as diff) + closure completeness `:592-594`.
- **[SOURCE]** `contract_identity:150-168` aggregates `contract_files.pipeline` + `DEFAULT_CONFIG` + profile/state schemas only — no `scripts/`. Hence helper-only change leaves `contract_identity` equal old==current (witness consistent). Require exact equal; **no self-exemption** for the new refresh subcommand/helper itself.
- Bootstrap honest limit: any new file under `scripts/` (refresh subcommand/helper/lock) is itself a control diff (`git diff old HEAD -- scripts` non-zero). E4-era receipts (generated before interface install) therefore fail old-receipt control check for two reasons (helper change + interface files) and are **unsupported for mechanical refresh** — disposition: establish new baseline receipts from a candidate with the interface installed, then permit helper changes. Do not carve out interface paths in code.
- Same-edition byte equality is scope, not whole-program equivalence. Prospective helper edits still need normal exact-head code review; no approval inherited. Concrete co-location risk (not generic): allowed file contains `_key:234-241` (citation-key regex/normalization), `VISIBLE_TEXT:38-50` (feeds `build_reader_input:348`), `_window:104-116`, `_validate_authored_input:119-153`, `build_reader_input:259-353`, `render_main/bib:373-434` together — e.g. a `_key` edge-char change preserves one edition’s cited IDs/outputs while breaking other IDs. Caught only by same-edition `surface==reviewed:686-687` + deterministic replay `:688-701` + review family `:620-623` for this edition; other editions need their own refresh/re-derivation. State this.

### C5. Entry (approved conceptually) [refines §5]

- Args minimal: `refresh-mechanical-evidence --state --reason --executor [--recorded-at]` only. No `--retention-dir/--manuscript/--config/--implementation-sha`: derive canonical `cfg (DEFAULT_CONFIG:26)`, `state`, `source/survey roots` (`_profile_and_source`, `_revalidation_surface_roots:674-677`), `manuscript/receipt/Gate/record` paths from State/profile/roles (`:680-688,:652-654`), actual `HEAD` via `repository_commit_sha:129-147` (no override).
- **[SOURCE]** Circularity: `survey_weekly_derivation_v2.py:11` imports `agent_control`, while `agent_control:31-38` does not import weekly; Gate file lazily imports weekly inside functions (`:1091,:1302` precedent). Hence agent→weekly must be function-local lazy import in the refresh subcommand, not top-level.
- Optional 1 new helper justified if controller growth >~300 lines: e.g. `scripts/survey_refresh_mechanical_evidence_v2.py` with pure helpers (`bind_old_authority`, `check_mechanical_scope`, `retain_before_write`, `atomic_replace_guarded`) called by the thin `agent-control` subcommand; no new schema/producer/framework, no Weekly/Gate semantic change. Root decides file split at implementation; analysis allows either with same guards.

### C6. Pre-computed bytes + atomic replace [CORRECTION of §§3-4 writes]

- **[CORRECTION]** Do not CLI-write unknown Gate then treat any changed Gate as owned. **[SOURCE]** `evaluate:1468-1469` writes only `if output_path is not None`, returns `report:1471`; `core.json_bytes:86-88` == `write_json:90-92` bytes. Generate new receipt dict (`build_receipt:607-639`) + `core.json_bytes` and new Gate dict (`evaluate(...,output_path=None)`) + `core.json_bytes` pre-retention; compare scope/equality (§§C1/C4) before any live write.
- Replace via same-directory atomic pattern (precedent `survey_orchestrator_v2.py:484,493 `os.replace(state_next,state_path)``; `core.write_json` direct `write_bytes` is non-atomic): write temp in same dir + `fsync` + `os.replace`, rechecking expected snapshots (`State/HEAD/old receipt/Gate shas`, byte counts) before each replace; preserve `byte_count/stat().st_size` + `sha256_file`. Public Gate/receipt readback after install remains actual `validate_*`.

### C7. Retention + existing rollback hazard [CORRECTION of §§3-4]

- Fixed dir outside `survey_root` (else `validate_survey_build_directory:73-96` breaks), e.g. `<source_root>/publication/v2/.refresh-retention/<UTC-run-id>/` (no CLI override): exclusive no-overwrite `receipt-superseded.json` + `gate-superseded.json` + inert `retention.json` (run_id, old/new commits, raw shas/byte_counts, checkpoint/predecessor refs, reason). Verify `sha256_file(retained)==live pre-write sha` BEFORE live writes.
- Restore only known own files with expected-hash guards; never `Gate changed → restore both` on unknown bytes: if post-failure live bytes `!=` (old snapshot XOR just-computed new bytes) or State/HEAD/source-bound drift, fail-closed manual (keep retention+live, no clobber).
- **[SOURCE hazard]** `revalidate:1800-1807`: on `except`, if `wrote_state` and State still `==written_state_sha` restores `original_state_bytes`, then `if created and record_path.is_file(): unlink()` — **no byte check** on record, and State write itself truncates. A narrow owner-check correction in this unit is justified and bounded: record `just_written_record_sha` after `core.write_json(record_path:1787)`; before `unlink`, refuse removal if `sha256_file(record)!=just_written` (unexpected tamper → keep + fail-closed, do not delete). State already has `written_state_sha` guard `:1802-1803` — keep. If root defers even this, then honest supported cases are only `record untouched + State intact`; all tamper cases are manual-reconciliation (state explicitly; do not promise safe removal).

### C8. Cooperative lock + commit point [CORRECTION of §4 “no lock”]

- Bounded hygiene allowed (not framework): derived exclusive guard e.g. `<source_root>/publication/v2/.refresh-lock.json` (`{run_id,head,state_sha,recorded_at}`), created no-overwrite (`O_EXCL`-equivalent: refuse if exists/is-symlink) before P1, removed only by owning run after commit/abort-restore. Occupied → refuse before writes (no clobber). Stale after crash → manual reconciliation only, no automatic steal. Noncooperating writers remain externally serialized; check-then-replace is observed-drift refusal, not global CAS.
- Guarantee: at most one cooperating refresh owns receipt/Gate writes at a time; all other drifts (State/HEAD/source-bound/retention mismatch) refuse/restore-per-§C7 without clobber. Catch (`Exception`, process alive) vs crash (kill/power, no handler) distinct; retention+lock+live hashes are the manual-recovery evidence.
- Commit point is `revalidate_publication_surface` successful return (`:1808`) with post State valid (`:1797-1799`). Do not roll back after establishment on later read/print error.

### Revised concise protocol (first/repeat viable)

```
P0 healthy preflight (no pending, no retention, no lock-held-write):
  strict validate_agent_state==[] + resolve_active LIVE (None→first; record→repeat, §C2)
  + old Gate==effective row (§C2) + inspect-old-Gate (C3) + receipt link + historical closure bytes@old (§C4)
  + new receipt/Gate bytes pre-computed (C6) + scope equal: accepted/authored/surface/render/review/QA+criteria (§§1-2/C4)
  + contract_identity old==current + control diff non-empty ONLY in survey_weekly_derivation_v2.py + current clean@HEAD
  + mechanical-need check (C1): control/closure identical → refuse NO_OP. Any fail → exit 2, no writes.
P1 lock+retain: acquire derived lock (C8, refuse occupied); snapshot; write fixed retention copies+manifest; verify retained==live.
  Fail → release own lock if held, exit 3, no live writes.
P2/P3 install (recheck snapshots+lock ownership before each atomic replace, C6-C8):
  receipt = atomic_replace(receipt_path, new_receipt_bytes); validate_receipt(new);
  gate = atomic_replace(gate_path, new_gate_bytes); validate_gate(new, expected_manuscript_path, state_path).
  Caught fail → restore ONLY known own files iff guards pass (§C7), release lock, exit 4; else keep + manual.
P4 revalidate: recheck; basis=built_checked_pending (must be exactly replacements=[reader-surface-gate]);
  revalidate(REVIEWED_CORE_CHANGE,reason,executor,recorded_at, HEAD) [existing rollback + C7 record owner-check];
  active LIVE readback. Success = commit (C8); release lock; no post-commit rollback.
  Caught fail → §C7 restore/manual; crash → retention+lock+live evidence, manual (no steal).
```

First path: null pointer, checkpoint Gate row, `supersedes null`. Repeat path: intact active r(n) LIVE, effective Gate row = r(n) `new_sha`, `supersedes=r(n)`, r(n)/checkpoint unchanged, chain+chronology (`:947-1012`) pass. Both use same P0–P4; pending context exists only P4 after owned Gate change.

Runtime files (2–4, root choice): (1) `scripts/survey_agent_control_v2.py` thin `refresh-mechanical-evidence` subcommand (lazy weekly import); optionally (2) `scripts/survey_refresh_mechanical_evidence_v2.py` focused helpers; (3) small diffs in `scripts/survey_reader_surface_gate_v2.py` (`_inspect_gate_record` split) and if justified `scripts/survey_weekly_derivation_v2.py` (`_inspect_receipt_inputs`); no new schemas/producers. Tests: extend `test_survey_publication_revalidation_v2.py` / `test_survey_increment_b_weekly_derivation_v2.py` / `test_survey_gate_cli_persisted_review_v2.py` family with T1/T2 + prioritized negatives (no saved-harness reuse). Runbook/doc: ≤1 short operator note only if lock/manual-recovery steps need prose; no contract-doc churn.

Prioritized T1–T11 (expected boundaries): T1 first + T2 repeat (retained raw bytes, r1→r2 chain, checkpoint immutable) highest; then T6 criteria-change (`check family differs`), T3 output-change (`deterministic replay mismatch`), T4/T5 accepted/authored drift (`accepted differs`/`surface differs`), T7 malformed authority/duplicate (`SHA/prior-SHA/digest/duplicate`), T8 dirty/HEAD drift (`uncommitted/HEAD-changed/State-changed`), T10 post-write QA fail (owner-guarded restore vs manual), T9 race/lock-occupied (refuse without clobber), T11 no-op via control/closure equality (C1, before retention). Each asserts specific message + State/record-listing + live-sha oracles per window; separate harness policy from runtime rejection; fresh fixture/process; no broad-`Exception` sentinel, no stale imports, no reset/clean.

(End of correction — §§1/2/4/7/T11 allowlist/write/no-op/lock claims above superseded where marked [CORRECTION]; rest of analysis retained.)

