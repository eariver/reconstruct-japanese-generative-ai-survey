# Independent real-output/source review — Selection scaling real writer rehearsal

Status: AUTHOR/OPERATOR/ROOT-INDEPENDENT ACTUAL-OUTPUT CHECK. No implementation, no writer rerun.
Verdict: **GO** — bounded input-to-actual-output binding verified for new real copy only. No new editorial verdict, no stage/Human/R4/adoption.

## 1. Method and bounds (deviation-mandatory)

- Read ONLY:
  - `notes/rephase-1-selection-scaling-repair-20261116/astra-repair-resolution.md` FULL §§10–11 (prevails; §11 deviation + two-workstream dispatch).
  - `notes/rephase-1-selection-scaling-repair-20261116/real-rehearsal-20261116T022222Z/README.md` + `machine.json` + raw (`w34-run*`, `sp-run*`, `source-commit*`, `realcopy-rsync*`, `*-utc.txt`, `*-epoch.txt`, `*-pid.txt`, `*-exit.txt`).
  - Actual new real `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work` via Read + stdlib `json`/`hashlib`/`pathlib` parsing/hashing only.
  - Frozen prior inputs `notes/rephase-1-repaired-correction-rehearsal-20261112/w34-selection-architecture-input.json` + `sp-selection-architecture-input.json`.
  - Prior delivery manifest `notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/complete-supplement-carry-manifest.json` (773 files, `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`/202833B) + recorded 5 pins in real `machine.json`.
- Input semantic reviews reused as PROPOSAL_READY scope only (honest reuse for input-to-output binding). No whole-corpus re-review, no new editorial verdict beyond binding, not stage/Human/R4/adoption.
- Allowed: stdlib read/parsing/hash. Prohibited and NOT used: project imports, runtime/tests/writer, Git (no `git` invocation, no status/log/head/readback), network, source active writes, subagents, reconstruct HEAD readback.
- Commit identity from data + recorded `source-commit-stdout/stderr/exit.txt` + `machine.json` only. No fresh Git certification is claimed; distinguish recorded identity from fresh certification.
- No continuous-immutability or full-history claim. Old active / shadow checks are actual-read-scope observations only.

## 2. Source 774 binding

- Base: final773 manifest `a7e40c47…`/202833B, BASE `409b292`, final141 DIRECT409 patch `171812f6…` unchanged per packet README. Manifest `files` count 773 verified by parse.
- Real copy:
  - 769 unchanged vs manifest: 0 missing, 0 mismatch (all bytes+SHA256 match manifest entries).
  - 4 mods + 1 new test match recorded `machine.json` pins (bytes+SHA256, `0o664`):
    - `scripts/survey_review_attention_v2.py` 7796B `10126da7482ff5203aa47663c5795ff96c14a452b67ed60b74d690a86d0e5718`
    - `scripts/survey_architecture_v2_base.py` 51050B `b3cd4a95f5123fbf34150bcd09921f035d12480cdaa69382fc58f4b55b8133c0`
    - `scripts/survey_research_authority_v2.py` 309483B `fd788b7444e5c38988d9946eec2542e35c5b9671e1bfaf9cddac5420120e5bf1`
    - `scripts/run_selection_architecture_v2_interactive.py` 50865B `b16c47599856919a38367aa412889baef8df02aeaf3325048e3796c5921869c7`
    - `tests/test_selection_scaling_repair_v2.py` 49973B `a21f5949434a3a7b787df13556d9ff4cf559d41529c6ef27bf46258dc952ba18`
  - Total intended 774 (769+4+1), 0 missing. No caches/material/DBs counted as source. Excluded `.git/__pycache__/*.pyc` per manifest.
- Recorded source commit: HEAD `3231a0c280287411513bba359f4d3d2b6703f591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367`, 5 files 2538+/99-, normal commit (no missing-ok, no amend/empty/bypass/config/HOME), inert `https://invalid.invalid/inert.git`, exit 0. Source: `source-commit-stdout.txt` `[detached HEAD 3231a0c] … 5 files changed` + `machine.json`. No fresh `git` run here; no fresh Git cert claimed. Missing-ok path was pre-authorized but NOT used.

## 3. Frozen inputs (exact bytes, no repin)

- W34 `w34-selection-architecture-input.json` 378396B `15375476f308fbfeb79c4e8f3f4d53d85d5cf917e36d29d3c3777580301aab3a` — actual real `sources/2026-W34/orchestration/v2/interactive/selection-architecture-input.json` same bytes+SHA.
- SP `sp-selection-architecture-input.json` 72613B `072f90b6795041f79ab42476faf93ad9e39f7c80ce30e16c1804d4fcbd51e9bd` — actual real `sources/SP-efficient-llm-2026/orchestration/v2/interactive/selection-architecture-input.json` same.
- Reused exact bytes for runs per real README. No repin, no approval/stub.

## 4. Actual State/CP/completion/8 four-refs/Profiles (preserved, no advance)

- Lifecycle both `EVIDENCE_REVIEWED`, `target_gate ARCHITECTURE_REVIEW`, `next_action stage:selection`, `machine_checkpoints.selection/architecture pending`, `human_gates.architecture_review/publication_preview pending`, `human_gate_provenance null/null`, `exception_gate inactive`. No Human review, no stage advance, no active installation.
- State pins (actual):
  - W34 `production-state.json` 4162B `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d` (= expected `a8586351…`), history[0] `48082356…`, last `EVIDENCE_REVIEWED@e84`.
  - SP `production-state.json` 4266B `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde` (= expected `38a63411…`), same history shape.
- CP `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` (actual):
  - W34 `research/v2/acceptance-revisions/w34-repaired-20261112-r2/checkpoint/record.json` 6054B `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`
  - SP `…/sp-repaired-20261112-r2/checkpoint/record.json` 6300B `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`
  - `checkpoint_provenance.evidence/materiality/completeness` → same CP SHAs; `selection/architecture/draft/validation/publication_preview/freeze/release null`.
- 8 four-refs = CP `record.json:artifacts` typed `artifact_refs` (not prose prefixes), all exist+match in real copy:
  - W34 evidence `eef77479b8d9c003ee8daae7eb882ea2aa63063ea10aea3e43d1f951c747427d`/126592, views `3727485ac1f791d64c3d951520bfab7694821ad4584140b913f91a1c48f654ae`/159502, ledger `066230f48ff3d29e714be35e86968a4ec834f9dacefb4590f4b64ac1fb73b320`/186214, completeness `d869027aefce95cde4478b875204c7f930755d66cc4d86e330b82b3835d5fdc6`/71532.
  - SP evidence `7f04e9adeddb327b085ede65de70638777a77a99810952bfdd44b6053a9a3327`/49237, views `45d60f9f19371ba9ae55f528cd20f674f0fbf4315bdabbfa4a4bedde6ba90939`/64222, ledger `5cf81f8f2997d6784da12d805f5cfb54b6c9ebd3b94a2424983b5b591275bdc1`/66850, completeness `b43786099456346b2eaf6f6f63f9636b5407aeedb8ba2c77840bac9adc915757`/34249.
  - Basis of each `candidate-matrix-v2.json` equals these 4 SHAs + profile SHA; verified.
- Profiles (actual, unchanged):
  - W34 `production-profile.json` 2371B `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1`
  - SP `production-profile.json` 13748B `aff05fd573ce873afa24c0ede26c2d4591ee28b7048c9ed528e8fc389ed8ee45`
- Completion (active, LIMITED):
  - W34 `profile-completeness-v2.json` 71532B `e8c432dd6275e81df5286cb8c0d55d99e27aa0812c52a114d870dddaf0d2795f`, `overall_status LIMITED` (2 LIMITATION/1 SATISFIED).
  - SP `profile-completeness-v2.json` 33683B `d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805`, `overall_status LIMITED` (13 LIMITATION/2 SATISFIED, closure `open_material_obligations 0`).
  - Active ledger: W34 `materiality-ledger-v2.json` 186202B `f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d`; SP 66850B `b7c85b4eb009249b355445f94a4041d4374990fccb07c38595b61c1e770c8c60`. Distinct from CP ledger bytes by design; not a mismatch.

## 5. Seven outputs per edition (14 total)

Sizes match `machine.json:seven_sizes`; all SHA bindings below verified by stdlib hash.

W34 (all `READY_FOR_ARCHITECTURE_REVIEW`, `selected_count 45/package_count 5` per `w34-run2-stdout.txt` 504B):
- `candidate-matrix-v2.json` 683098B `f4469c85b819d8436d37eecbaac68e07551e4942f0d86f124e6b6469480261af`
- `candidate-selection-v2.json` 375063B `f3a5000fe3c5370ae0768dc993f28fc3c64d9086ead566427728a1a6ff39a030`
- `architecture-v2.json` 24447B `9a76294ef05688c11fa6e114e96c98723e47c418522998ce835385c12a595615`
- `architecture-review-summary-v2.json` 314350B `1b7f6076b11c5b47f41ab838ce70da7e5b2f4d856a3d309f6e8859828040eff7`
- `architecture-review-attention-v2.json` 18437B `d68b5f319e996a73076338b939f6661e46648ef9fd5b3033346e17ccfe6f5b92` (`total 770/shown 50/overflow 720/limit 50/truncated true`)
- `orchestration/v2/interactive/selection-architecture-input.json` 378396B `15375476…` (== frozen)
- `orchestration/v2/interactive/selection-architecture-audit.json` 1436B `61d6a0bc5d427ecfb2bf5a4a3f47cdda2f9c01bf55b6ff3906f41bc01e6fd982`

SP (all `READY_FOR_ARCHITECTURE_REVIEW`, `selected 130/packages 9` per `sp-run-stdout.txt` 570B):
- `candidate-matrix-v2.json` 239359B `2f62e2a82af38ce0d8d9eaa405399a1b24df5b70d62a9872f3d5aa8549d81a8b`
- `candidate-selection-v2.json` 76603B `4e6884d6bb8e8f5ca92b3344501687b686cd6355a65de69dfc98a9ab2e262a1f`
- `architecture-v2.json` 33219B `4af84ab37d60145407adf393a519077aeb5debaea33f0f8305fda636a858396c`
- `architecture-review-summary-v2.json` 67700B `d0092e132ecb9d094cf04a8ee97b1603bfaa777a18508f834a7a5a55c022a341`
- `architecture-review-attention-v2.json` 15918B `482f3c215597e1d91726506149356f3dbd5190ac173233f1f6ee84acd362dd9f` (`total 65/shown 50/overflow 15/limit 50/truncated true`)
- `orchestration/v2/interactive/selection-architecture-input.json` 72613B `072f90b6…` (== frozen)
- `orchestration/v2/interactive/selection-architecture-audit.json` 1530B `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3098254d15449`

Audit binding: each `selection-architecture-audit.json` pins `interactive_input {path,sha256}` + 5 outputs `{path,sha256}`; all 6 pins per edition match actual file hashes above. Archive is exact input bytes; audit is binding only, no new content adjudication.

## 6. Content bindings (stdlib parse, no new verdict)

- Exact assignments every Matrix once: W34 Matrix 409 rows / Selection 409 assignments, sets of `candidate_id` equal, assignments unique (409 unique); SP 160/160 equal, unique. No missing, no duplicate, no extra.
- Selected count/roles/package-membership primary-once/support/no-HOLD-smuggling:
  - W34 `disposition SELECTED 45 / HOLD 364`; `architecture_usage PRIMARY 24 / SUPPORTING 21 / NONE 364`; `architecture_role WEEKLY:*` only on SELECTED (13+12+8+8+4), `publication_role WEEKLY_MAGAZINE:primary-story-anchor 24 / supporting-evidence 21`; HOLD all `NONE/null/null`. Packages 5: primary 24 + supp 21 =45 unique, `set(selected)==set(primary+supp)`, `primary∩supp ∅`, `pkg∩HOLD ∅`. Bad-selected 0, bad-hold 0.
  - SP `SELECTED 130 / HOLD 30`; `PRIMARY 14 / SUPPORTING 116 / NONE 30`; `THEMATIC:core-measured-effect 14 / supporting-conditions 116`, `LONGFORM_SPECIAL:reader-facing-technical 130`; HOLD all `NONE/null/null`. Packages 9: primary 14 + supp 116 =130 unique, equality holds, no overlap, no HOLD in packages. Bad counts 0.
- Inherited boundaries: output `architecture-v2.json:packages[].boundaries` non-empty both editions (W34 total 97: 29/24/16/18/10; SP total 199: 5/23/20/37/16/25/23/15/35). Input `architecture.packages[].boundaries` empty by design (proposal omits boundaries; writer binds inherited material boundaries). No empty package. Page plan preserved: W34 `target 15/max 16` with Research-Notes-box note; SP `target 60/max 75` with 14×1pp+116×0.3pp+overhead note. Thesis/goals/`selected_exceptions []` preserved.
- Ordinary summary major destinations/residual obligations:
  - W34 `major_material_destinations 399`, `selection {total 409 HOLD 364 SELECTED 45}`, `completeness LIMITED (2 LIMITATION/1 SATISFIED)`, `architecture PROPOSED package_count 5`, `readiness READY_FOR_ARCHITECTURE_REVIEW errors []`, `residual_limitations 5` (arXiv HTML, SOCIAL-only, Grok re-date, AWS mirror post-cutoff, provisional materiality).
  - SP `major_material_destinations 160`, `selection {total 160 HOLD 30 SELECTED 130}`, `completeness LIMITED (13/2)`, `architecture PROPOSED package_count 9`, `readiness READY errors []`, `residual 5` (Discovery locators, full-body gaps, Jev thin, AIPerf unconsumed, per-figure pins).
- Attention total/shown/overflow distinct stages:
  - W34 `total 770/shown 50/overflow 720/limit 50/truncated true`, `counts {MATERIALITY:DUPLICATE 4, EXCLUDED 26, HOLD 10, SCREENING:DROP 30, INSPECT 200, MAYBE 136, SELECTION:HOLD 364}`, shown items 50 = MATERIALITY 40 + SCREENING 10.
  - SP `total 65/shown 50/overflow 15/limit 50/truncated true`, `counts {MATERIALITY:EXCLUDED 5, SCREENING:DROP 5, INSPECT 5, MAYBE 20, SELECTION:HOLD 30}`, shown 50 = SCREENING 30 + SELECTION 15 + MATERIALITY 5.
  - Basis pins rehash screening-accepted + materiality-ledger + candidate-selection; verified present.
- No Human review/stage advance: `architecture-v2.json:human_review {reviewed_by null, reviewed_at null, review_reference null}`, `status PROPOSED`, `selection status ESTABLISHED` (not approved), State still `EVIDENCE_REVIEWED` with `selection/architecture pending` (see §4). No Gate activation, no install, no CURRENT/delivery in this scope.

## 7. Old active vs new vs shadow (actual-read-scope only)

- Old active `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`: 0/14 outputs present (all 7 per edition absent). Consistent with recorded `seven slots absent, guard absent`.
- New real `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`: 14/14 present (7+7) with sizes/pins above.
- Shadow `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work`: W34 0/7, SP 3/7 only (`candidate-matrix`, `candidate-selection`, `architecture` present with same sizes 239359/76603/33219; review/attention/input/audit absent). Matches prior `W34 0/7 SP 3/7 only` within actually read scope.
- No claim of continuous immutability or full history; only that actually read slots match above at review time.

## 8. Operation deviation and raw limits (ROOT §11 explicit)

- W34 first invocation `w34-run-*` PID 1107379 `20261116T022256Z` wall 0s exit 1, `ModuleNotFoundError: No module named 'scripts'` (`python3 <file>` vs `-m`), stderr 4 lines, stdout 0B, no partials, source/authority unchanged. Preserved as operational invocation failure, not writer PASS/refusal.
- W34 retry `w34-run2-*` PID 1108798 `20261116T022342Z–20261116T023738Z` wall 836s exit 0 stdout 504B stderr 0B. SP `sp-run-*` PID 1110053 `20261116T023802Z–20261116T024030Z` wall 148s exit 0 stdout 570B stderr 0B. Tool cap 1200s respected.
- Deviation: operator locally changed invocation to `-m` and retried without returning to root, contrary to §10 stop-at-first-failure. Calling it “still first genuine writer” does not make retry authorized. First failure + success preserved separately; no retroactive permission or no-autoretry claim. This deviation neither certifies nor invalidates generated bytes; this independent output check was required and is now recorded.
- Raw durability: saved `stdout/stderr/exit/PID/start/end UTC/epoch/wall` are durable; `argv/cwd/env whitelist/CPU/IO/actual Python PID` claims vs wrapper PIDs are NOT durable in saved raw (no `argv/env` files, no `cProfile`, no child `rchar`). Do NOT manufacture missing raw later; mark tool-observed vs durable explicitly. CPU/rchar were NOT separately measured.
- Wall 836s + 148s are bounded operability observations vs prior 1200s timeouts only. No exact speedup, physical-read, disk/net-savings, or net-benefit claim.

## 9. Findings and verdict

- F1–F8 all PASS on actual bytes: source 774, frozen inputs, State/CP/completion/8 refs/Profiles, 7+7 outputs, assignments/packages/roles, boundaries/page-plan, summary/attention/archive-audit, no Human/stage advance, preservation scope, recorded commit identity, deviation/raw honesty.
- No mismatch found. No fix is proposed or required in this review. Any future source change requires root review/rebinding before further real/proof execution per ROOT §11.
- Scope: this GO covers ONLY bounded input-to-actual-output binding on reviewed `3231a0c` real copy. It is NOT Selection PASS, NOT Human approval, NOT R4 audit, NOT CURRENT proof, NOT delivery/packaging, NOT quality/adoption/savings. Second workstream (affected regressions, fresh CURRENT, complete DIRECT409 packaging + independent final implementation/delivery review) remains separate.

**Verdict: GO_TO_SEPARATE_VERIFICATION_PACKAGING (bounded output binding only).**

Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Ordinary Commit/Push Human-owned.

## 10. Correction addendum — own-review SP audit SHA typo (ROOT §12 authorized, actual-file-bytes only)

- Authority: `astra-repair-resolution.md §12` explicit authorization for this reviewer to correct own documentary pin from actual file bytes only. No artifact edit/rebuild. No forged attribution.
- Method for this addendum only: re-read + stdlib `hashlib.sha256`/`json` of actual `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/sources/SP-efficient-llm-2026/orchestration/v2/interactive/selection-architecture-audit.json` + inner refs. No Git/runtime/imports/tests/network/source active writes/subagents. Code unchanged.
- Preserved history (superseded, 61 hex, DO NOT USE): `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3098254d15449` (recorded in §5 line 81 and machine `seven_outputs_per_edition.sp.audit.sha256` before this correction; missing `249` segment).
- Corrected current pin (64 hex, actual 1530B file bytes): `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3092498254d15449`, bytes 1530.
- Inner 6 refs re-verified unchanged from actual audit bytes (all 64 hex, match §5 + machine):
  - `interactive_input 072f90b6795041f79ab42476faf93ad9e39f7c80ce30e16c1804d4fcbd51e9bd`
  - `candidate_matrix 2f62e2a82af38ce0d8d9eaa405399a1b24df5b70d62a9872f3d5aa8549d81a8b`
  - `candidate_selection 4e6884d6bb8e8f5ca92b3344501687b686cd6355a65de69dfc98a9ab2e262a1f`
  - `issue_architecture 4af84ab37d60145407adf393a519077aeb5debaea33f0f8305fda636a858396c`
  - `architecture_review_summary d0092e132ecb9d094cf04a8ee97b1603bfaa777a18508f834a7a5a55c022a341`
  - `architecture_review_attention 482f3c215597e1d91726506149356f3dbd5190ac173233f1f6ee84acd362dd9f`
- Other 13/14 full output SHAs checked length 64 vs actual all-14; no other truncation found (40-hex commit/tree IDs are expected 40, not errors). See machine `correction` block.
- Narrow effect: actual output bytes, inner 6 pins, all other findings F1–F11, and bounded `GO_TO_SEPARATE_VERIFICATION_PACKAGING` verdict are unchanged. This corrects documentary pin transcription only.
- No claim of future final-implementation PASS. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN remains.
