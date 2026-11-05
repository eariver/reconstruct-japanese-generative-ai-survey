# Current observation — e84 repaired runtime (preparation/data+source-read only)

2026-11-04. General preparation owner. **No writes to active State/products/source yet. No subagents/network/Production checkout/reconstruct Git/status/log/HEAD/readback/source edits/runtime/tests/build/fixture.** Data-only hash/JSON/refs/code reading only. No `git -C .`. Machine snapshot in `current-observation.json` (full hashes; this MD is human-readable summary, JSON is authority for bytes).

Selected instance: `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`
- Recorded isolated source epoch `e84a82aca000c990597ea8cf60f548e2ff187bd1` parent `480823560c0c26ed2e5baa18e0e79a22b2839a27` tree `fb8e536ed2860acef8feb2eac7992a69e3ae` (from `notes/rephase-1-evidence-scaling-repair/real-w34-retry-20261103T172327Z/artifact-manifest.json` + README §§2-3; recorded DATA, not new `git` read, no reconstruct readback).
- Old480 rehearsal `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work` and failed `bd80` verification copy preserved untouched; NOT active. Do NOT use old480 or failed bd80 as active.
- Runtime/content matches final139 delivery except test-only diff (see §4). Test-only difference is known, not a new runtime repair epoch.

Read roots: `outputs/rephase-1-evidence-scaling-implementation-assessment.md` §5, mandatory `notes/rephase-1-evidence-scaling-repair/astra-closeout-resolution.md` FULL, original rehearsal ROOT §§5/7 + SP correction draft (`notes/rephase-1-operational-rehearsal-20261101/astra-rehearsal-resolution.md` §§5/7, `closeout-state-observation.md` + `.json` + `closeout-check.md`, `execution-20261101T025600Z/correction-draft-SP-20261101T174517Z/README.md` + JSONs, reviews `primary-consumption-efficient-llm-20261101T174126Z.md/.json` + `evidence-efficient-llm-review-20261101T113240Z.md`, publisher supplement `publisher-intake-supplement-20261101T172535Z/README.md` + `manifest.json`).

## 1. Active e84 State/Profile/DCP/SCP (exact paths from State, not latest-guess)

Both editions `CANDIDATES_NORMALIZED`, `target ARCHITECTURE_REVIEW`, `next stage:evidence-materiality-completeness`, impl `480823560c0c26ed2e5baa18e0e79a22b2839a27` (old init retained, no hand-repin).

- W34 State `sources/2026-W34/production-state.json` 3386B `7e6a50c2b84cdc7e526f1560f02efd95184685770edb95ab35bb9a40c633ea58` mode 664.
- SP State `sources/SP-efficient-llm-2026/production-state.json` 3454B `4865998b99ab2902954619b2a7761c4ae0de77695b6d25d49dff4eb89` mode 664.
- W34 Profile `sources/2026-W34/production-profile.json` 2371B `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`.
- SP Profile `sources/SP-efficient-llm-2026/production-profile.json` 13748B `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`.
- Contract8 (from State `contract`): pipeline `3adfbda22131eac4017ef867aef2ebb2f346f884731c4ea8343e9062392eabd5`, quality `b5b955d524fb438c0f1b2c9490bea1da2083e79028d67a55ca424bbfc20f2958`, research W34 `666f8a064b190ffd35216e26d6fdf2dd0fa932cac7b1b0d6448e262ded77b9a8` vs SP `0f575e6d97caec72b2bf8b7f6b78a562d97ca67b2071193417b968ba3d73e6e8`, publication W34 `99adff93ff443e02bdcce639ce5fc4d4c959ee45a804da70efc4277db57fdddb` vs SP `a6859559dd1b9d42ab8fb4402b74b7bdd8611dbe65c8e02a7b022b545c20f4eb`. Implementation `repository_commit_sha 48082356` both.
- DCP (discovery acceptance chain): W34 `discovery/discovery-accepted-v2.json` 377589B `255fb12d71cf463e78b9be74fbb57d35d3beea2dbb47fa27cbd36b442133f22b` + raw `discovery-v2.jsonl` 963155B `e176326f853ed42b69bad8a1998513d8dba8d3838af7cdea0ca9bc8261df46b0`; SP `discovery/discovery-accepted-v2.json` 135693B `2413dbe2f188ca2cde5d07ac07a749932b6536d41db2263b43cd3cd86924a856` + raw `discovery-v2.jsonl` 173299B `7074cef2bfc3b2dd034addbd778055bc2fed962e9845c756f32f9b3c848199d3`.
- SCP (screening acceptance chain): W34 `screening/v2/accepted/e193ad05.../screening-accepted.json` 543880B `b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841` + `screening/input/event-discovery-v2.jsonl` 1335444B `0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e`; SP `screening/v2/accepted/9b979629...a9/screening-accepted.json` 69226B `6ff524b0a2c2c8f79603348acb86d18d39b180498a72ca92dc12f852dc786bf4`.
- Checkpoints: each `orchestration/v2/checkpoints/` exactly 2 files `ISSUE_INITIALIZED.json` + `DISCOVERY_COLLECTED.json` (W34 `3c64e40b...` 3101B + `4d3221d3...` 3206B; SP `5b9910c9...` 3144B + `481d965f...` 3223B). `CANDIDATES_NORMALIZED.json` absent both, `EVIDENCE_REVIEWED.json` absent both. `stage-reviews/` exactly 2 each, `stage-validation/` exactly 2 reports each. No `candidate-matrix/selection/architecture/selection-architecture-input/pipeline-state.json` either edition. `gates/` absent both. `human_gates pending/null`, `checkpoint_provenance evidence/materiality/completeness null` both. `machine evidence/materiality/completeness pending` both.

From-state naming: missing Evidence producer is `CANDIDATES_NORMALIZED.json` (needed for future `EVIDENCE_REVIEWED` advance). This is observation, not a new runtime validator PASS. No live `HumanGate` files, no `ResearchECP` file where absent recorded as absent.

## 2. W34 new 409 products (e84 run, State still CAND)

- Proposed `evidence/proposed-input/interactive-evidence.json` 1573186B `3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27`.
- Supplement `external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json` 389414B `ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b6b6b8f0fbc704e` (428 bindings/425 distinct Raw, per artifact-manifest).
- Accepted `evidence/v2/accepted/bf208f96.../evidence-accepted.json` 126603B `450b508ca5078703d99aad46d5aedf466222aa3889e8753862696f7588cf000e`, `result_count 409` (352 PARTIAL/49 VERIFIED/8 NEEDS_MORE, historical input status kept, no new publisher-truth claim), `result_set bf208f96...`, package `package.json` 157429B `0ec312b4b66435ee09c34f982b39bf126710edb2c853d6b2915733a7fe25652c`, audit `interactive-audit.json` 1041B `0a41ec9dce66337d6cf3cfb5431a7defa0408f7ccab0b5253e3c78a77b8de7fe5` (input `3ffc6e31...`, outputs path-only).
- Views `evidence/v2/views/accepted/f744e46b.../edition-views-accepted.json` 159498B `5ad0a6acdb27e3e5c1415297a6c03838107b8785ec2d4c5025050f1d0aaacf0e`, 409 views.
- Ledger `materiality-ledger-v2.json` 186202B `76ac53f90f3c731c5819ab73ae3fcfd4451f7d5030795232e80e02ebac2aca4b` rows 439, basis pins profile `2a8c3089...`, discovery `0a23be47...`, screening `b9d963d8...`, evidence `450b508c...`, views `5ad0a6ac...`, sets `bf208f96.../f744e46b...`.
- Completeness `profile-completeness-v2.json` 71532B `93dbefae96ee0acddf5a13125dac6d28a25c3ef3e1d4decaf61d766356c57bfb` obligations 3, `LIMITED`, basis ledger `76ac53f9...`.

State remains `CANDIDATES_NORMALIZED`; W34 ledger/completeness are new but still unaccepted (no `EVIDENCE_REVIEWED` checkpoint). Preserved for review, not as acceptance.

## 3. SP old products (held CHANGES_REQUIRED, State CAND)

- Proposed `evidence/proposed-input/interactive-evidence.json` 345202B `f46dcf2f43ebed472d309d40a70ddba8f402193eeca99787791636442ba29958`.
- Supplement r1-fresh `external/evidence-supplement/evidence-authority-supplement-r1-fresh-basis.json` 12871B `6e1ae0cb2d5671655dddd46d0826901b590f48a0b2fd027fe874f7385971608a`.
- Accepted `evidence/v2/accepted/09f487ab.../evidence-accepted.json` 49241B `9c2543191e78a1b8e005e46f0ead9c5a10470a28406f0fd10b58fb8829c46e18`, `result_count 160` (148 PARTIAL/12 VERIFIED), `result_set 09f487ab...`, package 48671B `34f81e563b2f8c3d43dde42bf58a4be0152955237466dc0add7c6025059aefd0`, audit 1145B `890a43239dacd50f867f43a672798c40e735a42dc1830a5427036f5f3dcaad`.
- Views `evidence/v2/views/accepted/50c919b9.../edition-views-accepted.json` 64227B `7a205de1010da647fd8d9af9a8b029da461faae68be4501d0406d3b116ee2a4f`, 160 views.
- Ledger `materiality-ledger-v2.json` 66865B `ee13b8ee5626ea0e7198d85aa0fddf6bcadb42679d11621834f6c97ee8ab796d` rows 165, basis pins profile `aff05fd5...`, discovery `7074cef2...`, screening `6ff524b0...`, evidence `9c254319...`, views `7a205de1...`, sets `09f487ab.../50c919b9...`.
- Completeness `profile-completeness-v2.json` 32511B `c60a96242a5157ebd7c3509cf1500f45deb277c4c9854343cf2a5f790a106c86` obligations 15, `LIMITED`, basis ledger `ee13b8ee...`.

Old accepted Evidence/Views dirs (`09f487ab...`, `50c919b9...`) are content-addressed + validated, immutable. Ledger/Completeness are owned **unaccepted** (State CAND, no evidence/materiality/completeness checkpoints, no Human refs). See disposition plan for exact 2-file recovery; no disposition executed here.

Old accepted audit pathrefs vs SHArefs: `interactive-audit.json` outputs are path strings only (no SHA for outputs); input carries path+SHA `f46dcf2f...`. Ledger basis pins accepted Evidence/Views by full SHA (path+SHA in basis). Completeness basis pins ledger SHA `ee13b8ee...`. No accepted checkpoint/Human/downstream pins ledger/completeness themselves (stage reviews/reports contain no ledger refs; no candidate-matrix/selection/architecture files). Completeness→ledger pin is unaccepted-downstream, not accepted authority.

## 4. Source comparison intended 771 vs final manifest

Final delivery: actual `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` +139paths57M82A/771 files. Patch `complete-evidence-scaling-409.patch` `de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49` 5408065B, manifest `complete-evidence-scaling-manifest.json` `c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143` 202204B (recorded in `source-packaging/final-20261103T174718Z/*-sha256.txt`, `gen-revparse-stdout.txt`/`candidate-head-after-stdout.txt` both `409b292...`).

E84 vs manifest (stdlib `hashlib` compare of all 771 intended paths in e84):
- ok 770, missing 0, mismatch 1.
- Only diff: `tests/test_evidence_scaling_v2.py` e84 `d486809c4ae88c0e78784ade8e456cd9227b25a29c12cde9700664a1eec3edad` 91561B vs final `7b862305db39afde93c4ca0f1ce2d4b5faf512729e6956a8166f09c0e12e` 106616B (TEST-ONLY, 18→19 methods). Other 770 including all 3 runtime (`survey_evidence_v2.py 48742538...` 158943B, `run_evidence_v2_interactive.py 5e195730...` 45833B, `survey_research_authority_v2.py 0974c709...` 218692B) exact. No source/test change needed; do NOT mutate source to normalize counts.

Config `survey-production-v2.json` in e84 `95fe3c283f54b356c02ebcb4964eea02282c239c93d7c7e748f28001fb4d8dc8` 19097B (part of 770 match).

## 5. Validity / open questions / ready review inputs

- Validity: this is data/source observation, not a new runtime validator run, whole-history/inode certification, or semantic PASS. 49 VERIFIED (W34) /12 VERIFIED (SP) are historical input statuses preserved, not new publisher-truth PASS. Old228GB failed observation stays transcribed incomplete, not a baseline for speedup/disk/savings.
- Open: substantive W34 Evidence/authority-consumption review on actual current outputs + corresponding Raw (historical vs new distinction) still needed; SP independent re-review of NEW bound artifacts still needed (see disposition plan). No Selection/Architecture preparation, no R4, no Human adoption.
- Ready inputs for Root/independent reviewer: `current-observation.json` (all full hashes above), e84 State/Profile/checkpoints/audit/ledger/completeness files as listed, final patch/manifest + `independent-packaging-report.md`, real-run packet `real-w34-retry-20261103T172327Z/README.md` + `artifact-manifest.json` + `raw/machine.json`, SP draft + 174126Z review + supplement manifest (hashes in JSON §sp_draft_refs to be added in disposition plan), and this MD.
- Next: Root reviews observation + disposition plan BEFORE any copy/rename/unlink/disposition or re-execution. Do NOT auto-start rehearsal/audit. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality/adoption/savings OPEN. Human Commit Point — stop.
