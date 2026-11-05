# SP independent Evidence re-review — NEW e84 df671195/2ad42d4d sets (BOUNDED_PROCEED to EVIDENCE_REVIEWED)

**Role:** NEW independent substantive Evidence reviewer. NOT operator/source/plan author, NOT Astra/root, NOT prior r1/r2 reviewer, NOT Human. No false attribution.

**File:** `notes/rephase-1-operational-rehearsal-resume-20261104/reviews/sp-evidence-rereview-20261105T003000Z.md`
**Machine:** `sp-evidence-rereview-20261105T003000Z-machine.json` (full SHA256, no truncation)
**Wall-clock:** 2026-11-05T00:30Z (read scope after dispose-run `20261105T000554Z`).
**Bounds:** source-read/data-only, no project imports/run/tests/network/Production/reconstruct Git/readback. Only active e84 `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work` + permitted packets `notes/rephase-1-operational-rehearsal-20261101` + `notes/rephase-1-operational-rehearsal-resume-20261104`. Stdlib `hashlib/os.lstat/json` only. No subagents. SP ONLY. No State advance by reviewer.

**Actual State (read-only):** SP `CANDIDATES_NORMALIZED` (`production-state.json` 3454B `4865998b99ab2902954619b2a7761c4ae0de77695b06ddd5b5e25d49dff4eb89`), machine `evidence/materiality/completeness pending`, `checkpoint_provenance` null, 2 checkpoints only, gates absent, no `EVIDENCE_REVIEWED` checkpoint. `EVIDENCE_REVIEWED` advance pending this review. No advance attempted.

**Workdir base:** e84, impl `480823560c0c26ed2e5baa18e0e79a22b2839a27` retained, e84 `e84a82aca000c990597ea8cf60f548e2ff187bd1` parent48082356. Runtime + other770 match final139; test-only d486 vs 7b862305 known, not a repair epoch.

## 1. Exact new pins + read scope (current bytes, rehashed locally, full hashes)

| artifact | bytes | SHA256 | notes |
|---|---|---|---|
| `evidence/v2/accepted/df6711954d6ee37f0489c6f87e8d072511af26168adb033b0f327d1165faf0ac/evidence-accepted.json` | 49237 | `d64264268eefaf73ae83ba81e175b57badf8ad609c65893636dd4da9ba4115c1` | 160 results (152 PARTIAL / 8 VERIFIED) |
| `…/package.json` | 50279 | `4f6b9bdad089d88e12cbe96b1a80020d1dedb82da9afc33c752f6713c02789b5` | 160 tasks, copy via `copy2` |
| `…/interactive-evidence.json` (archived) | 355386 | `0ee3187eb3850fd79060556bc03cfbe4634365efbf33f47cdacd119d0b7c2a89` | == staged `proposed-input/interactive-evidence-r6-sp17-20261104T162747Z.json` same bytes/SHA |
| `…/interactive-audit.json` | 1145 | `be6c07cc028a1bc2a74877f14f2183c95600ecb01113a27764a68d157a4e065b` | binds NEW archived path + staged bytes `0ee3187e…` |
| `evidence/v2/views/accepted/2ad42d4dd6e9873782410246b9bdde83f0ea04c8aa3d6dfe5d8456855c4b686b/edition-views-accepted.json` | 64222 | `e439db857e9e2f2547f98dfc12c9b956f220b83375d3523290f8c9937f90e9db` | 160 views MATERIAL132/CONTEXT28 |
| `materiality-ledger-v2.json` | 66850 | `253cb2ea7429d0455a3c82df44b809552a67bbb63a03e3638b43aa7827e203a3` | 165 rows MATERIAL132/CONTEXT28/EXCLUDED5 |
| `profile-completeness-v2.json` | 33683 | `18a05292857242ddf4b5339a9b7c8a48ce9a1f154f63d4e58f2cef9fc5695f27` | 15 obligs 2 SATISFIED/13 LIMITATION, overall LIMITED |
| staged supplement `external/evidence-supplement/evidence-authority-supplement-r6-sp17-20261104T162747Z.json` | 30922 | `ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3` | 30 sources, SHAs == r4 proposal (ID wrapper only differs) |
| staged input `evidence/proposed-input/interactive-evidence-r6-sp17-20261104T162747Z.json` | 355386 | `0ee3187eb3850fd79060556bc03cfbe4634365efbf33f47cdacd119d0b7c2a89` | == archived, == r4 proposal |
| r4 proposal supplement `sp-corrected-supplement-r4-20261104.json` | 31278 | `1221d293b121977d8fe4ce086e9fb09a2c4b296c1d50bcbcda3705ec997b5db7` | 30 sources, D123+vLLM corrected |
| r4 proposal input `sp-corrected-input-r4-20261104.json` | 355386 | `0ee3187eb3850fd79060556bc03cfbe4634365efbf33f47cdacd119d0b7c2a89` | 160 rec, O05 LIMITATION |
| old accepted `09f487ab…/evidence-accepted.json` | 49241 | `9c2543191e78a1b8e005e46f0ead9c5a10470a28406f0fd10b58fb8829c46e18` | preserved, unchanged |
| old views `50c919b9…/edition-views-accepted.json` | 64227 | `7a205de1010da647fd8d9af9a8b029da461faae68be4501d0406b3b116ee2a4f` | preserved |
| backups `retention-SP-dispose-20261105T000554Z/materiality-ledger-v2.json` | 66865 | `ee13b8ee5626ea0e7198d85aa0fddf6bcadb42679d11621834f6c97ee8ab796d` | O_EXCL 0o664 nlink1, State `4865998b…` |
| backups `…/profile-completeness-v2.json` | 32511 | `c60a96242a5157ebd7c3509cf1500f45deb277c4c9854343cf2a5f790a106c86` | same |
| 17 staged Raw `external/evidence-supplement/raw/sp17-*` | see §3 | 17/17 match r4 + packet + sidecar (full pins in machine JSON) | 13 old `supp-*` untouched |

**Method (governance §§4.2–4.4, not shape/count):** for each of 17 patched records parsed exact `verification.targets/finding`, `claims/evidence_class`, `source_bindings`, `materiality/materiality_rationale`, `limitations`; compared claimed body/version vs (a) active e84 staged Raw 17 bytes/SHAs, (b) task `source_bindings` vs r4 supplement `supplement_source_id`, (c) discovery locator immutability. Old CHANGES_REQUIRED `evidence-efficient-llm-review-20261101T113240Z.md` §§3–5/§7 + primary-consumption `172752Z` + narrow update `174126Z` read FULL as baseline, not re-litigated where retained (D032 + 9 wrong-locator supplement positives).

**Explicit read scope (no full160 semantic PASS from 17-sample):** substantive read = 17 patched input records (full verification/claims/limitations/materiality) + 9 wrong-locator supplement cards (retained PARTIAL, spot-checked bindings) + D032 launch (retained) + 15 completeness rows (full rationale) + ledger 165 downstream dispositions (counts + 5 CONTEXT + 5 EXCLUDED spot + rationale) + views 160 materiality counts + supplement 30 rows (SHAs/bytes/locators) + 17 staged Raw existence/SHA/bytes (not full-paper re-read; paper bodies already consumed in `172752Z/174126Z` as DATA, this review binds pins/scopes, does not re-extract all sections) + dispose-run report/manifest/READY/DISPOSE_RUN/retention-manifest/run-bundle + r4 delta/true-binding + disposition plans. Remaining ~143 non-patched records NOT re-semantic-reviewed; prior PARTIAL/abstract-scope retained only where claims scoped accordingly. No blind 160 PASS.

## 2. Old CHANGES_REQUIRED disposition (11/12 + loadbearing + O05/O04/O11)

Old `113240Z`: 1/12 VERIFIED bounded-legitimate (D032); 11/12 VERIFIED unsupported (D036/D070/D071/D141/D148/D149/D150/D151/D154/D163/D165) + loadbearing PARTIAL body-VERIFIED overclaims (D027/D008/D123/D125/D030/D004+D163-dependent) + O05/O04/O11 `body-consumed` rationale overstatements. Verdict CHANGES_REQUIRED, no `EVIDENCE_REVIEWED`.

New disposition:
- 7 papers + PR now bounded VERIFIED with version-pinned bodies (§3): D036 v3, D148 v1, D149 v3, D150 v1, D151 v1 (corrected date), D154 v1, D165 merged+full conversation. **Resolved as SUPPORTS at cited scope, NOT automatic; required NEW bound run now satisfied.**
- 1 retained SUPPORTS (D032 launch 84605B `bf027425…`). No repair.
- 4 living-doc/docs correctly HELD as PARTIAL/UNRESOLVED/CONTEXT current-only (§4): D070/D071/D141/D163/D004. **Resolved as honest HOLD, NOT false VERIFIED.**
- Loadbearing PARTIAL (§5): D027/D008/D123/D125/D030 remain PARTIAL with VERIFIED section-scope sub-targets + UNCONSUMED outstanding quarantined; D004/D163 UNRESOLVED/CONTEXT; old `sibling D163 fully consumed` WITHDRAWN. **Resolved.**
- O05/O04/O11 (§6): all LIMITATION with per-body vN + scope + outstanding, no SATISFIED, no blanket `body-consumed`. **Resolved.** Draft `O05 SATISFIED` overstatement corrected to LIMITATION before staging (see `sp-draft-correction-20261104.json` + r4 input).

No remaining VERIFIED without body. No numeric-threshold/blanket downgrade (MATERIAL132 retained where authority supports bounded claims).

## 3. Seventeen new body consumption (10 papers CONFIRMED + PR COMPLETE + HF CONFIRMED + 5 current-only)

Staged Raw 17 verified live vs READY vs r4 vs packet (17/17 SAME, 0o664, nlink1, no symlinks). Full pins in machine JSON.

| DID | body file | bytes | SHA256 | version/published (API governs) | historical | finding |
|---|---|---|---|---|---|---|
| D036 EAGLE | `sp17-eagle-v3.pdf` | 1865998 | `3484aad4d255ac8ff3ebbb0df9f3b2fdb222145923f59ad25727812f4748a0f4` | v3 pub 2024-01-26 upd 2025-03-04 | CONFIRMED <cutoff | VERIFIED Fig.1 2.90x/3.07x/2.95x, 1.7–2.1x/1.5–1.6x, ~0.8 vs 0.6, lossless/composable; ablations outstanding |
| D148 Snell | `sp17-snell-v1.pdf` | 3870997 | `ded7b20b51493258c5ce2a1a024cd33dd752de1fa3373d1207620da4cfe24545` | v1 2024-08-06 | CONFIRMED | VERIFIED §7 + 4x+/14x with non-trivial-success condition; appendices outstanding |
| D149 s1 | `sp17-s1-v3.pdf` | 1480533 | `598932c9f96849cd52495d8b3e12ba4d224e41d5588d2278a78f76c744d8a3bc` | v3 pub 2025-01-31 upd 2025-03-01 | CONFIRMED | VERIFIED §§2–3 s1K + budget-forcing Wait + 27%/50→57% Qwen2.5-32B-bound; ablations outstanding |
| D150 ThinkPrune | `sp17-thinkprune-v1.pdf` | 1035542 | `63d4ee6f96ce18bf0a65b925fc3cbe433784d7c30c685d4e38190d4c3d84437c` | v1 2025-04-02 | CONFIRMED | VERIFIED §§3.3/5 + Table1 exact (82.9/29.4/70.3/44.7/56.8 → 83.8/73.6/46.5/58.2, len 10355→5232) + temp0.6/top-p0.95/N64; RL-cost outstanding |
| D151 overthinking | `sp17-overthinking-v1.pdf` | 531162 | `c4254e531f3ab61bc5979357f6d8f0988f5c413f8d96f8d906ababb2c7e7ad3d` | v1 **2026-04-12** (API/abs/PDF agree, single version, no v2) | CONFIRMED <cutoff with corrected date | VERIFIED flip + Table3 CIs + Uλ 16k 32x; **CORRECTS Discovery `published_at 2026-08-24` to 2026-04-12, P5 08-24 UNVERIFIED record date, Discovery immutable** |
| D154 FrugalGPT | `sp17-frugalgpt-v1.pdf` | 1171365 | `035ae8b90333dad8b7817fc8f55e7c4cbca435368c5c1a4dbf7bba9e5db87473` | v1 API 2023-05-09 (P5 05-10 1-day immaterial) | CONFIRMED | VERIFIED §4 Table3 50–98% + OVERULLING + heterogeneous pricing; formulation/prices-stale outstanding |
| D027 Kimi | `sp17-kimi-v2.pdf` | 1354769 | `e2e23a449fc9bb27e34e783d20b2e6cd0f1ac67d58efdc0479c03c54db956a17` | v2 pub 2025-10-30 upd 2025-11-01 (P5 now pinned v2) | CONFIRMED | PARTIAL record + VERIFIED section-scope (KDA/DPLR/identical-recipe/−75%/6×); per-task tables + license (CC BY-NC-ND repo-side, not PDF) outstanding |
| D008 Qwen | `sp17-qwen-v1.pdf` | 2363790 | `17db868acaa0b86caaf89cd9516e0a92f79d7e161431e5e274b70a3123d60ef7` | v1 2026-08-31 | CONFIRMED | PARTIAL + VERIFIED Tab.11 + 1/3–1/9 ratios as vendor self-comparison quarantine; ablations outstanding |
| D123 V4.1 | `sp17-v41-v1.pdf` | 1663475 | `0cfdda19c8e1691b5226dd0d4949e2397051268e8a823c2fb61db94ea20c4ac0` | v1 2026-09-17 (P5 09-18 1-day, API governs, 4d<cutoff) | CONFIRMED | PARTIAL + VERIFIED section/arch/appendix-map scope; Appendix B/C per-figure UNCONSUMED quarantined |
| D125 V3.2 | `sp17-v32-v1.pdf` | 980616 | `2bec0671778769c159ec389412727d1f3d4889fe1c71564b61edaa24705bd17b` | v1 2025-12-02 | CONFIRMED | PARTIAL + VERIFIED DSA §2 prototype + parity; ablations outstanding |
| D070 launch | `sp17-launch-current.html` | 270966 | `278478f09f3df3c2987dba4c7620ef7b842fed1c1e13f362e3a11d3713c21de9` | living, Last-Modified 2026-10-28, P5 09-15 field PRESENT but mod proves nothing | UNCONFIRMED current-only | PARTIAL + UNRESOLVED, vendor-quarantined only (§4) |
| D071 concepts | `sp17-concepts-current.html` | 165512 | `b58d91ae23784860dd4083c04ca51b1a382b9c045c54af053085c0e0bfe3540d` | living, dateModified 2026-10-14, no version | UNCONFIRMED | PARTIAL + UNRESOLVED (§4) |
| D141 models | `sp17-models-current.html` | 219035 | `59b6c17b12d3cb8ac781abdf5f9b52888ce336d840d35c49cc9c1f9ec9286e60` | living, dateModified 2026-11-01, 1.13+1.14 table (1.14 drift) | UNCONFIRMED | PARTIAL + UNRESOLVED, 1.13.0+drift current-only (§4) |
| D163 vLLM | `sp17-vllm-recipe-current.html` | 2705796 | `fa61427e75ee14b172bc56ce79e46179e1a6c906fad4142625c4a0eea7d908c2` | living, no version header, pinned 09-20 NOT verified, gap 0/13 ≤cutoff proven | UNCONFIRMED highest drift | PARTIAL + UNRESOLVED, topology-conditional current-only (§4) |
| D165 PR27742 | `sp17-pr27742.json` | 26122 | `3728e08d0731a5faab852f32d0aee0fdd6011bf0873c7c697cb4280b0a338561` | merged `2026-08-27T19:32:31Z` head `eaf93765` base `732707df`, 65 commits + 144 comments (packet `4143b4ad…` 256128B + `c1b1f7d5…` 271317B + `541bd239…` 134958B, all ≤cutoff) | CONFIRMED merge ≤cutoff, full conversation CONFIRMED | VERIFIED merged existence + PR-scope validation-report (ppl 4.0068/4.0126, QSA/PLE/gaps); **existence NOT correctness, no rebuild** |
| D030 HF | `sp17-hf-readme-dba1be0.md` | 13110 | `347c9db4e5506acb531cbc3b724407ab88e9af8781679152f0823d7bac16d251` | README @`dba1be0` `2026-09-10T08:18:10Z` (11 Sep10+6 Oct in `b32414f9…` 267351B, matches P5 09-10) | CONFIRMED ≤cutoff | PARTIAL + VERIFIED spec-identity scope (CED/CSA/Engram/DSpark/552B/8B/16B/890B/45T/effort/harness+MIT); MXFP/B200 UNRESOLVED (§5) |
| D004 Dynamo | `sp17-dynamo-dev.md` | 16535 | `5b9ddeb7a047130d5811926d40d14237142562ccd291a7e88c9cd77fc8f9ff66` | living dev branch, `for version dev`, no direct Edit link | UNCONFIRMED | PARTIAL + UNRESOLVED, role+disaggregation current-only, topology matrix UNCONSUMED (§4) |

No CONTRADICTS: no new body contradicts its old headline metric (ThinkPrune Table1 exact, EAGLE Fig.1 exact, Snell 4x/14x, s1 27%/50→57%, FrugalGPT Table3 exact). Only date correction E151 (flattened first-posted vs P5, handled as lineage correction, not silent fix).

## 4. Historical5 CONTEXT-current-only (no asof overclaim)

All 5: record PARTIAL, verification UNRESOLVED (both targets where 2), materiality CONTEXT, `published_at null`, `accessed_at 2026-11-01`, `CURRENT-ONLY UNCONFIRMED` + vendor/project quarantine + explicit Last-Modified/dateModified/gap flags + `historical VERIFIED requires 09-21/pinned revision` (D163: exact recipes-repo path STOP; D004: no new repo guess; TypeSafe: 09-15 field + Oct mod MIXED, 1.13 presence + 1.14 drift does NOT prove 09-21). Ledger downstream CONTEXT (not MATERIAL proof) until historical version bound. Views CONTEXT28 (was 23, +5). **No asof elevation; current bytes retained for archival comparison only.** O10/O04/O08/O11 relevance preserved in rationale text; MATERIAL status alone is not relevance proof (explicit).

## 5. O05 actual scope + D123/vLLM corrected digests

- O05 LIMITATION (not SATISFIED): EAGLE v3 + Qwen v1 section/table SUPPORTS + DSpark via vLLM current-only PARTIAL-current ONLY + Medusa/MTP outstanding + Snell/s1/ThinkPrune/overthinking explicitly scoped to O14, not O05. `No structural SATISFIED; overall LIMITED preserved; historical DSpark VERIFIED requires exact recipes-repo path.` Draft SATISFIED corrected before staging. Complies with `174126Z` §8.
- D123 65-char `…0fd4949…` → 64-char `0cfdda19c8e1691b5226dd0d4949e2397051268e8a823c2fb61db94ea20c4ac0` (1663475B, sidecar + manifest + durable DATA agreement, not reseal). Embedded in record finding + supplement relation corrected; other 29 rows unchanged.
- vLLM 63-char `…5c4aeea…` → 64-char `fa61427e75ee14b172bc56ce79e46179e1a6c906fad4142625c4a0eea7d908c2` (2705796B) restored in O05 rationale. `new_embedded_malformed_count 0` (40-char `dba1be0a…` in D030 relation is valid Git commit, allowed).
- Remaining r4-manifest 5 wrong pins (61/65/60-char, 2-vs-1 byte) REPORT ONLY, never fixed by reseal; harness bound real files (see §8). Correct quarantine.

## 6. Load-bearing MATERIAL + prior VERIFIED labels

- New VERIFIED records 8/160: D032/D036/D148/D149/D150/D151/D154/D165. Each binds cited body at scope with limitations preserved; no VERIFIED without body remains.
- PARTIAL records with VERIFIED sub-targets (D027/D008/D123/D125/D030): VERIFIED is section/spec-identity scope ONLY, record stays PARTIAL, per-figure/ablation/license/MXFP outstanding quarantined. No full-body inference.
- MATERIAL132/CONTEXT28/EXCLUDED5 coherent: 165 = 160 + 5 DROPs (D140/D158/D159/D160/D161 preserved, not reintroduced); +5 CONTEXT shift = historical5. No silent narrow/drop; parent-OID/extra15 preserved (from prior §2, unchanged by this delta).
- Source-class≠truth: EAGLE/s1/etc `PRIMARY_PAPER` + `AUTHOR_CLAIM` quarantine; launch/recipe/card `PRIMARY_OFFICIAL/REPOSITORY` + `VENDOR/PROJECT_CLAIM` quarantine; PR merged = existence only; SOCIAL stays reception-lead. `1 OFFICIAL quirk` per-source-id mapping legitimate.
- D030 MAY close spec-identity on README alone; MUST NOT cite unsupported historical vLLM; D004 sibling corroboration WITHDRAWN (both legs PENDING).

## 7. Per-obligation disposition (15 rows, actual NEW completeness)

| oblig | status | disposition |
|---|---|---|
| O01 bottleneck | SATISFIED | KEEP: Kaplan/Chinchilla + Orca prefill/decode + Dynamo 2026; tables outstanding, no structural gap. No repair. |
| O02 precision-quant | LIMITATION | KEEP: D005/D139 supplement-bound true identities (abstract-scope); D140 DROP. Carry abstract-only + body-outstanding to Selection. |
| O03 MoE | LIMITATION | KEEP: DeepSeekMoE/Mixtral/MoD/LayerSkip/Expert-Choice/MegaBlocks; D117 supplement-bound (body outstanding). |
| O04 attention/KV | LIMITATION | KEEP: V4.1 v1 + V3.2 v1 + Qwen v1 + Kimi v2 section/arch/appendix-map; D032 launch; D077 lead-only; D061/D062/D112 abstract-scope. **Per-figure B/C + ablation + license outstanding.** |
| O05 decoding | LIMITATION | Section/table scope per §5; DSpark current-only + gap proven + STOP; Medusa/MTP outstanding; TTC in O14. **No SATISFIED.** |
| O06 quant-serving | LIMITATION | KEEP int8/GPTQ/AWQ/QLoRA/SparseGPT/BitNet/MX/MXFP4/GGUF; D005 supplement-bound (body outstanding). |
| O07 local/GGUF | SATISFIED | GGUF/llama.cpp/KTransformers/Ascend/X/Unsloth/Qwen-port bound where load-bearing. No repair. |
| O08 disaggregation | LIMITATION | KEEP Mooncake + SARATHI/Sarathi-Serve supplement-bound true identities (abstract-scope). |
| O09 PEFT/sparse | LIMITATION | Hinton/LoRA/QLoRA/SparseGPT/R1 intact; D159–D161 DROPs. |
| O10 Jev | LIMITATION | Current-only launch/concepts/models + vendor quarantine; reproduction thin (community leads, F4 unresolved, no calibration). Historical VERIFIED requires 09-21 revision or narrower PARTIAL scope. |
| O11 capstone | LIMITATION | 32KEEP+9MAYBE+2INSPECT zero DROP; 4 capstones section-level + D032; D077 lead-only; MiniMax/gpt-oss watches; GLM abstract-only + per-figure quarantined. |
| O12 bench/method | LIMITATION | SWE-Pro identity supplement-bound (section outstanding); RULER+TBench family; GenAI-Perf consumed; AIPerf open; harness pins outstanding. |
| O13 Engram | LIMITATION | Body-level allocation law + delta table; repo release-level; Qwen-PLE parallel/unresolved; static-fusion/allocation-curve outstanding. |
| O14 TTC | LIMITATION | Snell/s1/ThinkPrune/overthinking (2026-04-12 corr.) section/table-consumed; effort-control via vLLM current-only; D152/D156 deferred; ablations outstanding. |
| O15 routing | LIMITATION | FrugalGPT Table3 + RouteLLM pipeline section-scope; unifier secondary-by-design; D158 DROP; formulation/pricing-stale outstanding. |

Overall LIMITED, `open_material_obligations 0` + `targeted_gap_fill_completed true` does NOT auto-complete (LIMITED preserved, explicit residuals). Closure residuals (5) match per-record limits: wrong-identity locators (Sol amendment deferred), full-body/ablation outstanding, Jev thin, AIPerf open + MiniMax/gpt-oss watches, per-figure/version pins outstanding. **Selection must still explain 5 EXCLUDED + carry all LIMITATION scopes; no Selection PASS inferred.**

## 8. Mechanical operation/backups (independent inspection, not PASS transfer)

- Authority: `astra-resume-resolution.md` §6 one invocation only. Tool `2044257f…` 46350B, launcher `b60d2cad…` 3020B, READY `c7cd05a8…` 12270B, manifest `6507804d…` 395713B, helper `2c6f1aeb…` 42142B — all verified programmatic before launch. `RET=retention-SP-dispose-20261105T000554Z` new exclusive, no prior `retention-SP-dispose-*/dispose-run-r2-*`. UTC 2026-11-05T00:05:54Z→00:06:21Z, parent 4151751, no `GIT_*`, `HOME=/home/eariver`, `PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0`, no network/Production/reconstruct Git; e84 isolated Git only.
- Result: normal run `evidence_result_count 160`, `completeness_status LIMITED`; wrapper `post-run-verify pass` exit 0 (mechanical, not semantic PASS). New Evidence `df671195…` 49237B `d6426426…`, package 50279B `4f6b9bda…`, archived `0ee3187e…` == staged, audit binds NEW archived path + staged bytes, 160 tasks/results; new Views `2ad42d4d…` 64222B `e439db85…` 160 views; discovery 165 nonempty; ledger 66850B `253cb2ea…` 165 rows; completeness 33683B `18a05292…` 15 obligs LIMITED.
- Tree: SP 1056 files/37 dirs (571 pre + 485 new + 5 dirs); umask `0o2` → `0o664`, no chmod of products.
- Preservation: backups exact O_EXCL 0o664 nlink1 (ledger `ee13b8ee…`, completeness `c60a9624…`, State `4865998b…`, manifest `490ce0aa…`); State `4865998b…` CAND unchanged, Profile `aff05fd5…` unchanged, old accepted `9c254319…/34f81e56…/890a4323…/7a205de1…` unchanged, W34 preflight `1ea56297…` + W34 State/ledger/completeness unchanged; no W34 run; no State/CP/Human/source change.
- Deviations preserved, no false claim: old v1 wrapper altered (44098B `546f7174…`, not `d591e5d4…`) as-altered, never executed; old helper 20/20 stale exit1 ≠ exit0; single invocation, no restore/cleanup; r4-manifest 5 mismatches REPORT ONLY.

## 9. Verdict + allowed next (narrow, no audit/adoption PASS)

**Verdict: `BOUNDED_PROCEED to EVIDENCE_REVIEWED` — NEW 160/165/15 LIMITED fit for `EVIDENCE_REVIEWED` checkpoint on authority-consumption/research-quality grounds ONLY.**

Structural/contract PASS (normal run exit 0, 160/160/165/15 shape, hashes bound, State CAND, no overwrite/force) + substantive PASS on patched scope: original 11/12 unsupported resolved per §2–§5, O05/O04/O11 rewrites per §6, historical5 honestly held per §4, D123/vLLM digests corrected per §5, mechanical preservation per §8. This is NOT a full-corpus semantic PASS, NOT publication/Selection/Architecture/Draft/Candidate/Preview/Freeze/Release PASS, NOT Human Gate, NOT adoption/savings/quality verdict.

**Selection/Architecture residuals (must be carried, not closed here):** 5 EXCLUDED DROPs need Selection explanation; per-figure B/C + Qwen ablations + Kimi tables + routing/TTC results + version pins (kernels/repos/harnesses) outstanding; Jev reproduction/evaluation thin + vendor quarantine; AIPerf open; MiniMax/gpt-oss watches; GLM abstract-only; MXFP/B200 with V41 section-scope + vLLM current-only quarantined; Dynamo topology matrix UNCONSUMED; vLLM historical path STOP (recipes#1136/#1137 exact-path Human need, no broad clone); TypeSafe 09-21 revisions (or accept PARTIAL-current per §4).

**Explicit allowed next:** Root may record this review + advance SP to `EVIDENCE_REVIEWED` via normal checkpoint path (existing State/Profile/Contract8, no source change) when ready. Then Selection/Architecture preparation only when gates actually hold. **NOT allowed:** Selection/Architecture PASS, Draft/Candidate/Preview/Freeze/Release, Human Gate decisions, old approval rebinding, source edits, synthetic PASS/savings, new Core feature/schema/checkID/Gate, W34 Ledger/Completeness clearing (separately unselected), asof elevation of current-only Raw.

**Attribution:** NEW independent substantive Evidence reviewer. Binds §1 full hashes + §§3–8 read scopes above. Prior CHANGES_REQUIRED stands as history until checkpoint; this re-review is its bounded successor for the NEW bound artifacts, not its deletion.

(End of independent SP Evidence re-review — 2026-11-05.)
