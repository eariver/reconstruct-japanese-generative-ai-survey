# Normal HIGH prepare plan — SOURCE REVIEW only (no execution)

Selected runtime (read-only, no prepare yet):
- NEW_WORK `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
- HEAD `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, parent `e84a82aca000c990597ea8cf60f548e2ff187bd1`, tree `ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`, init480 `480823560c0c26ed2e5baa18e0e79a22b2839a27`, both `EVIDENCE_REVIEWED`.
- Tool pins (7, live file SHA256, `survey_prearchitecture_acceptance_v2.py:437-453` `_contract_and_tools`):
  - `scripts/survey_research_authority_v2.py` `7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f`/240969
  - `scripts/survey_prearchitecture_acceptance_v2.py` `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90`/97844
  - `schemas/dm022-revision-request-v2.schema.json` `a99f0dc1f6e10ae5736063a051ef3b147eb85bccf20e435db87054a2bac1a31f`/18648
  - `schemas/dm022-revision-manifest-v2.schema.json` `e7534d019ec1b58672ff306ac901d65669e2c64251fe41964df2e81e356fbaf4`/8773
  - `schemas/dm022-revision-proof-v2.schema.json` `a79c09209c145d485ec39e1c1c277f0d706cf3ccfb0972c5bd9f6d6fe7cec5c3`/7403
  - `schemas/dm022-preadoption-report-v2.schema.json` `10238a1af7330e5352cbbad709e6360797fade789f184126f296fbeb3e82e4db`/14629
  - `schemas/dm022-supersession-checkpoint-v2.schema.json` `fd39c246617293ecb6760906534512e2b5a14a484916c3d1f3ba055b33d3bec0`/7259
- Contract8 (live `contract_identity`, State-embedded, unchanged):
  - pipeline `3adfbda22131eac4017ef867aef2ebb2f346f884731c4ea8343e9062392eabd5`, quality `b5b955d524fb438c0f1b2c9490bea1da2083e79028d67a55ca424bbfc20f2958`
  - W34 research `666f8a064b190ffd35216e26d6fdf2dd0fa932cac7b1b0d6448e262ded77b9a8`, publication `99adff93ff443e02bdcce639ce5fc4d4c959ee45a804da70efc4277db57fdddb`
  - SP research `0f575e6d97caec72b2bf8b7f6b78a562d97ca67b2073417b968ba3d73e6e8`, publication `a6859559dd1b9d42ab8fb4402b74b7bdd8611dbe65c8e02a7b022b545c20f4eb`
  - orchestrator `survey-production-core-v2/0.15-postintegration-transport-thematic`
- DM022 request schema (`schemas/dm022-revision-request-v2.schema.json`): required 18 `schema_version/issue_id/revision_id/research_profile/before_state/before_checkpoint/profile_ref/discovery_ref/screening_ref/work/affected_ids/supplement_manifest/records/completeness/runner/tool_pins/recorded_at/executor`; `revision_id` pattern `^[a-z0-9][a-z0-9-]{0,63}$` (lowercase hyphen ≤64). Planned `w34-repaired-20261112-r1` / `sp-repaired-20261112-r1` (no uppercase `T`/`Z`, no `U` score suffix).

Records assembly (DATA only, no write):
- W34: base `sources/2026-W34/evidence/v2/accepted/5ca6f310…/interactive-evidence.json` `15e87eef…`/1576279 + `w34-repaired-patch4.json` 4 (`15127/16096/21100/18389` PARTIAL MATERIAL AUTHOR_CLAIM) = full 409 (405 unaffected `20a5313741d54bf89afd856b3e56950b62954a6d317f14c6ae7ce7783852433d`/1358779 +4). Duplicate `discovery_id` unique check; unaffected canonical doc hashes preserved; verification targets = package task `verification_targets` exact (per `survey_evidence_v2.py:2291-2296` `_build_card_core`); runner `provider/model/invocation/generated_at` preserved from base for `accessed_at` fallback + `observed_at` (`survey_evidence_v2.py:2265,2344`).
- SP: base `…/73f4bc1e…/interactive-evidence.json` `697a4ed0…`/355643 + `sp-repaired-records-4-r4.json` 4 (`EFF-D070/D071/D141` PARTIAL vendor + `EFF-D142` PARTIAL INFERENCE narrow) = full 160 (156 unaffected `d455f7221a0addd93dd2a3c07c874fe4dfb815d3e795933882eb839e868a1ef9` +4, D165 `16f046f5…` preserved). Same duplicate/task-target/runner rules.

Completeness (7 fields `obligation_id/dimension/description/status/discovery_ids/evidence_task_ids/rationale`, scoped updates only):
- W34 3 rows (from `profile-completeness-v2.json` `e8c432dd…`/71532 LIMITED): `weekly:current-relevance` LIMITATION, `weekly:technical-significance` LIMITATION, `weekly:carry-over` SATISFIED. No promotion.
- SP 15 rows (`sp-repaired-obligations-15-r4.json` `1d80d994…`/31838 LIMITED): `EFF-O01/O07` SATISFIED, rest LIMITATION incl `EFF-O10`. No fake SAT, `closure:null` preserved.

Raw/supplement staging (proposed only, no write now):
- W34 4 future `sources/2026-W34/external/evidence-supplement/raw/w34-event-arxiv-2608-{15127,16096,21100,18389}.html` byte-identical to `…/execution/luna/…/evidence-bodies/arxiv/2608_*.html` (`85c70376…`/314048, `a4c2aafe…`/414077, `da737a85…`/711224, `56b48291…`/388712), FULL DID basename, no traversal. Supplement existing `evidence-authority-supplement-r2-fresh-basis.json` `ce6f977a…`/389414 retained (428 sources, no new entry).
- SP 4 future `sources/SP-efficient-llm-2026/external/evidence-supplement/raw/sp17-EFF-D070-archive-launch-20260921T033022Z.html` (`14ae3118…`/253542 exact decoded copy), `sp17-EFF-D071-…041355Z.html` (`35770834…`/307198), `sp17-EFF-D141-…205053Z.html` (`97a5dd74…`/350662), `sp17-EFF-D142-summary-captured-20260921.md` (exact copy `f7eeec68…`/3751 SUMMARY_CAPTURED, no new content). Full30 `sp-repaired-supplement-full30-r4.json` `e2bfb30a…`/31522 = 27 preserved `c75389e8…` +3 new (`ea9b086e…`, `793903f4…`, `228b8166…` hex16, `PRIMARY_ANNOUNCEMENT/DOC`, `PRIMARY_OFFICIAL`, `published_at:null`, `raw_sha/bytes` above, `SourceRoot` safe paths, no `../`). Validated via normal builder validator / schema + normal full validator, never caller `verified_dict`.
- Request `SizedRef` (`path/sha256/byte_count`, `safePath` `^(?![/\\])(?!.*\\.\\.)[^\\\\]+$`): actual source/data bytes + expected `work.expected_head=cc1c…` / `expected_tree=ed2dc4…` + current 7 tools + Contract8 from actual public/private producer helper (allowed, no new engine). `supplement_manifest` null (W34, existing supplement carried) or SizedRef to staged full30 (SP, after authorized staging).

HIGH operation (later dispatch only):
- Use ONLY `survey_prearchitecture_acceptance_v2.py:456` `prepare_revision(repo_root,state_path,request_path,revision_id)` / CLI `prepare --repo-root --state-path --request-path --revision-id` (`:1557-1582`). Call order: `verify_live_eligibility` → `_profile_and_source` → `_prove_before_graph_unbound` → `_current_head_tree` → request parse+`dm022-revision-request` validate → `revision_id` equality → `work` HEAD/tree match → `tool_pins.contract/tool_shas` live match → `before_state` bytes/count match → current root/effective + source-class + `find_declaration_loss` → exclusive `state-before COPY` + 7-slot retention (`SEVEN_SLOTS` `survey_research_authority_v2.py:66-74`) → LOW pure builders + supplement closure → exclusive R writes + FULL validators → manifest (no self digest). New owned `R` = `source_root/research/v2/acceptance-revisions/<revision_id>/` (`:261-265`); writes manifest/retention only, no State/guard/adoption.
- Guard: entry/post all773 + State/Profile/CP/Human/old-accepted/canonical4 unchanged; only unique Raw/request/supp/R writes allowed; failure preserve first temp/final, stop, no auto retry/cleanup (`_exclusive_write_bytes:83-96`).
- Capture unique `raw/stdout/stderr/exit/PID/UTC/env/argv` per attempt; no project tests needed.
- Preflight (this dispatch script): cheap real validators — file SHA/size/mode, JSON strict parse, schema required/regex/counts, task-target coverage, duplicate/unaffected hashes, safePath/traversal, SizedRef bytes — before `prepare` can be authorized. No public CAND writer / old stage helper / adopt now.
- External `Decision` (`suppliedDecision` schema `:315-368`) generated by independent reviewer after exact manifest, never operator `SYNTHETIC` reviewer fields for real data.

Bounds: no commits/code/State/network/Production/reconstruct Git/readback/subagents. Whole NOT_READY/DM021+022OPEN. Stop at Commit Point.
