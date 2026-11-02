# SP correction draft — NEW proposed input + supplement proposal (DATA only, no canonical mutation)

Role: General SP correction operator/planner, NOT independent reviewer. No subagents/network/Git readback/Production/shipping code edits/ordinary commits.
Workdir: `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work` final138 `48082356` (read-only this unit).
State held: SP `CANDIDATES_NORMALIZED`, `machine evidence/materiality/completeness pending`, NO `EVIDENCE_REVIEWED`/`CANDIDATES_NORMALIZED` checkpoint files, Human gates `pending/null`, `target ARCHITECTURE_REVIEW`. W34 untouched (same State, large Evidence perf blocked; DO NOT run W34 or edit its files).

## Read scope (packet README/current status + independent findings + actual bodies)

- Packet `notes/rephase-1-operational-rehearsal-20261101/README.md` §§ Current Evidence-quality hold + Human publisher-bodies authorization + W34 correction + Current state.
- Execution `execution-20261101T025600Z/README.md` §§7–10 + `worklog.md` + logs `23-29` (SP advance + Evidence accept `09f487ab` + ledger/completeness).
- Independent SP Evidence review `reviews/evidence-efficient-llm-review-20261101T113240Z.md` §§3–5/§7 `CHANGES_REQUIRED` (11/12 VERIFIED unsupported + loadbearing PARTIAL body-VERIFIED overclaims + O05/O04/O11 rationale overstatements).
- Primary-consumption review `reviews/primary-consumption-efficient-llm-20261101T172752Z.md` §§2A–2C + machine `.json` (10 papers CONFIRMED SUPPORTS at cited scope, 7 nonpapers PARTIAL-current NEEDS_VERSION; E151 Apr12 vs Aug24 ghost-date; TypeSafe3/vLLM/Dynamo hist UNC; PR/HF version pins).
- Publisher intake `publisher-intake-20261101T163426Z/README.md` + `manifest.json` (40/40 DATA 21054963B) + supplement `publisher-intake-supplement-20261101T172535Z/README.md` + `manifest.json` (1 NEW historical README dba1be0 + PR complete 65+144 CONFIRMED + vLLM gap proven + 10 arxiv KEEP).
- Main semantic review context: 10 papers body confirmed + PR65/144 + HF historical README, TypeSafe3/vLLM/Dynamo hist v5 UNC (preserved, not re-fetched).

## Current outputs (full hashes in `current-outputs-machine.json`, generated via hashlib, not truncated)

- Proposed input `evidence/proposed-input/interactive-evidence.json` 345202B `f46dcf2f…` (r2-adapted O13-15, 160 rec PARTIAL148/VERIFIED12).
- Accepted `evidence/v2/accepted/09f487ab…/evidence-accepted.json` 49241B `9c254319…` + `package.json` 48671B `34f81e56…` + views `50c919b9…/edition-views-accepted.json` 64227B `7a205de1…`.
- Canonical `materiality-ledger-v2.json` 66865B `ee13b8ee…` + `profile-completeness-v2.json` 32511B `c60a9624…` (written while State CAND, Evidence pending).
- Fresh basis Discovery `7074cef2…` + Screening `6ff524b0…` + Supplement r1-fresh `6e1ae0cb…` (13 sources verbatim).
- State `4865998b…` CAND, checkpoints ISSUE_INITIALIZED `5b9910c9…` + DISCOVERY_COLLECTED `481d965f…` only; NO evidence/materiality/completeness checkpoints; NO Human checkpoint refs.

Preserved: original r2 + accepted `09f487ab` immutable; original 13 supp sources + Discovery immutable (no relabel/drop/child rewrite).

## Crucial retry boundary (actual runner/write APIs + governance)

- `scripts/run_evidence_v2_interactive.py:852-873`: if `materiality-ledger-v2.json` exists/symlink → `refusing to overwrite Materiality Ledger`; same for `profile-completeness-v2.json:872-873`. Only `O_EXCL`-style refuse, no `--force`, no cleanup flag.
- `scripts/survey_evidence_v2.py:650` package dir `refusing to overwrite non-empty Evidence package directory`; `:381` supplement `refusing to overwrite`; `:2203` ledger `refusing to overwrite`; `accept_evidence_results:1244-1248` content-addressed idempotent re-read only if same `result_set_sha`, else new dir or `incomplete pre-existing` error; views `:1926-1932` same.
- Order in `run()`: Evidence accept (new content-addressed dir) → Views accept (new dir) → Ledger write (refuse, existing file) → Completeness (refuse). A public normal rerun with divergent NEW Evidence/Views would create orphan NEW accepted dirs then fail at Ledger, leaving canonical Ledger/Completeness unchanged + no State change. DO NOT run expensive full160 merely to discover this collision (already mapped from code, no execution).
- `survey_agent_control_v2.py:build_stage_checkpoint` refuses divergent overwrite, allows idempotent same-bytes re-read; `advance_with_checkpoint` requires canonical checkpoint + reviews + contract/impl identity; no delete/move/overwrite API. Human Gate invalidation (`survey_human_gate_v2.py`) only for pending Gates, not for Ledger/Completeness. `revise_weekly_interactive_evidence.py:48` requires `EVIDENCE_REVIEWED` (SP is CAND, not eligible). No synthetic Human REQUEST_CHANGES, no old-State rollback, no unselected generic pending bypass.
- Verdict on canonical files: Ledger/Completeness are UNACCEPTED owned outputs (State CAND, evidence/materiality/completeness `pending`, no checkpoint provenance, no Human refs), NOT immutable accepted authority (accepted Evidence/Views dirs are content-addressed + validated, still immutable). But runner still treats them as no-overwrite, so same-stage correction has NO legitimate existing manual repair path while they exist. Precise capability gap (see Blocker).

No file deletion/move/overwrite performed this unit (checked: Ledger/Completeness hashes unchanged vs `current-outputs-machine.json`).

## NEW draft artifacts (this dir only, packet permitted, no workdir/canonical mutation, no State advance)

- `new-supplement-proposal.json` 30 sources (13 old verbatim + 17 NEW per-source-id). IDs `supplement-src-[0-9a-f]{16}` derived `sha256(sp17:DID:locator)[:16]`, distinct from old 13, no aliases. `evidence_task_id` = `stable_task_id` via actual API (`sha256(DID)[:16]`), not alias. `source_class` = `_source_class(source_type)` (DM016 canonical, no new keys). Basis binds fresh Discovery `7074cef2…` + Screening `6ff524b0…`. Raw `raw_path` future-intended under `source_root`, `raw_sha256`/`byte_count` from intake manifests (full hashes). Old locators/Discovery unchanged. E151 locator version-pinned PDF, Discovery `published_at 2026-08-24` preserved with annotation corrected to API `2026-04-12` in relation/finding (no hidden root rewrite, no new DIDs).
  - 10 arxiv: version-pinned PDF locators, `published_at` API, `accessed_at` intake time, CONFIRMED<=cutoff, binds cited sections/tables, appendices outstanding, quarantine preserved.
  - 5 living docs (TypeSafe3 + vLLM + Dynamo): `published_at null`, `accessed_at` current, CURRENT-ONLY UNCONFIRMED, vendor/project quarantine, no full appendix/license proof, explicit bounded status. vLLM gap proven (0/13 <=cutoff in vllm path, historical likely recipes#1136/#1137 unknown STOP).
  - PR27742: single row binds `pr.json` merge (head `eaf93765` base `732707df` merged `2026-08-27T19:32:31Z`), full 65+144 CONFIRMED in packet noted as supporting (256128B `4143b4ad` +271317B `c1b1f7d5` +134958B `541bd239`), existence≠correctness, no rebuild.
  - HF: historical README `@dba1be0` 13110B `347c9db4…` `2026-09-10T08:18:10Z` CONFIRMED + current card 452330B `99c60974…` lastModified `2026-10-16` UNCONFIRMED, B200-conditionality preserved.
- `new-input.json` 353016B full 160 (143 preserved verbatim + 17 patched + completeness O05/O04/O11/O10/O14/O15). No new schema keys (only `COMMON+THEMATIC+source_bindings`). Statuses: 10 papers VERIFIED/PARTIAL kept (findings now cite vN+SHA+sections + E151 date fix), PR VERIFIED kept (full conversation cited), 6 living docs PARTIAL (downgraded D070/D071/D141/D163 from VERIFIED to PARTIAL with `UNRESOLVED` historical, findings cite current hashes + Last-Modified flags). D030/D004 kept PARTIAL with updated README/current-only findings. All alterations carry rationale+body ref; SourceClass resource not truth (OFFICIAL/REPOSITORY as provenance, VENDOR/PROJECT/AUTHOR evidence_class + limitations preserved). Dependent O05 SATISFIED only with per-body vN + DSpark current-only + Sol concurrence note, else LIMITATION; O04/O11 rationales replaced blanket `body-consumed` with per-body vN + outstanding list; overall LIMITED preserved.
- `new-supplement-ids.json` + `new-input-delta.json` (patched 17 + completeness 6, preserved r2 basis note).
- `current-outputs-machine.json` (full hashes via hashlib) + `check-draft.py` (read-only `_validate_record`/`_validate_completeness_input`/class/task/pattern/coverage checks on verified inputs, no canonical writes).

Checks run read-only: 160 `_validate_record` PASS, exact 160 non-DROP coverage PASS, old13 verbatim PASS, new17 IDs/task/class PASS, bindings match PASS, completeness universe (U=initial+root+effective, 3-field initial vs 5-field named, no new keys) PASS, status enums PASS. Supplement full `validate_evidence_authority_supplement` NOT run (Raw not staged by design; would fail until intake bytes staged under `source_root`).

## Minimal safe plan (root choose before any cleanup)

1. Retain exact old bytes: Ledger `ee13b8ee…` + Completeness `c60a9624…` + Proposed `f46dcf2f…` + Accepted `09f487ab/9c254319…` + Views `50c919b9…` + Supplement r1-fresh `6e1ae0cb…` + State CAND `4865998b…` + checkpoints `5b9910c9…`/`481d965f…` (see machine JSON). Verify ownership/current State/guard via strict read (`production-state.json` + `checkpoint_provenance` + `human_gate_provenance` null + DM022 READY `require_research_operation_ready` — guard absent this unit, no PREARCH family).
2. Legitimate existing manual repair if actually allowed: NONE found. No public API cleans up UNACCEPTED canonical Ledger/Completeness at CAND while preserving content-addressed Evidence/Views; `build_stage_checkpoint`/`advance_with_checkpoint` do not delete; Human invalidation does not apply; `revise_weekly_interactive_evidence` requires EVIDENCE_REVIEWED. Any `rm/mv --force` would be outside normal operation (no guessed `--force`).
3. OR precise capability gap: same-stage Evidence correction at `CANDIDATES_NORMALIZED` with existing canonical Ledger/Completeness + new accepted Evidence/Views SHAs needs either (a) root-authorized owned cleanup/recovery/resume operation with exact old-byte backup + guard checks + re-run under current impl `48082356` with strict validators, or (b) new capability (e.g., versioned Ledger/Completeness or owned retry branch) via Astra. No synthetic REQUEST_CHANGES, no old-State rollback, no generic pending bypass.
4. Needed root dispatch: choose (a) vs (b) + authorize staging of 17 intake Raw bytes under `source_root/external/evidence-supplement/raw/sp17-*` (same-ref `c8` for `execution/**/evidence-bodies/*` if present, else already-authorized 17 URLs reused as bytes, no new broad search) + NEW supplement build via `build_evidence_authority_supplement` (fresh basis) + NEW input adapt (this draft `new-input.json` as DATA reference, not direct install) + normal `run_evidence_v2_interactive` retry + fresh independent Evidence re-review. State held CAND until root dispatch + fresh review; no canonical new acceptance/mutations yet; no W34 run.

New private input files kept outside active `evidence/proposed-input` (this packet dir) to avoid overwrite. Data/harness scripts outside control roots only; no project source mods.

## Files in this draft

- `current-outputs-machine.json` 6394B `54acf40c…` (full hashes, predicate anchors, State refs)
- `new-supplement-proposal.json` 30 sources (13+17) — see `new-supplement-ids.json`
- `new-input.json` 353016B `0a6876d4…` (160 rec, 15 obligs, new bindings)
- `new-input-delta.json` + `check-draft.py` (read-only checks, no writes to workdir)
