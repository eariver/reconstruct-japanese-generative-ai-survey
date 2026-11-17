# SUPERSEDED by sp-architecture-dossier-ja-r2.md（root §1 修正） — 以下は履歴として保存、現行 binding として使わない。

# SP Architecture Review Dossier（人間向け・未承認・ canonical 前） — SP-efficient-llm-2026

**位置づけ:** Fresh independent SUBSTANTIVE reviewer（not author/operator/root/Human）による packet-local dossier 案。
active 3231 実出力の実質 review に基づく人間向け dossier であり、承認・Draft/PDF・R4・canonical 生成・Human Gate 判断を含まない。
`source 3231a0c280287411513bba359f4d3d2b6703f591` は execution commit であり、genuine Human-reviewed commit ではない。
State は `EVIDENCE_REVIEWED` のまま。approval 要求はしない。stage actions の前に root review が必須。
ガバナンス `docs/survey-production-core-v2-sol-luna-review-governance.md` FULL に準拠（Sol supervisory + 12 項目 dossier）。

## 1. 正確な review identity（edition・revision・repo・lifecycle）

- Edition: `SP-efficient-llm-2026`（research `THEMATIC` / publication `LONGFORM_SPECIAL`）。
- 実 repo: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`、
  source `3231a0c280287411513bba359f4d3d2b6703f591` / parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` /
  tree `ff01b73e6012fd4519fdfb3807186753ff330367`（frozen、DIRECT409 final143/774）。
  manifest `0dc361cb…`/187361B、patch `76ac1318…`/5691014B。
- State: `production-state.json` 4266B `38a63411…`、`EVIDENCE_REVIEWED`、init480/forward4/Human pending、guard なし、7 下流 absent。
- PREARCH: `sp-repaired-20261112-r2/checkpoint/record.json` 6300B `2a528ed5…`、
  kind `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`。old canonical 不使用。
- Typed PREARCH 4 refs（CP artifacts、実在＋一致確認）:
  evidence `7f04e9ad…`/49237・160、views `45d60f9f…`/64222・160、
  ledger `5cf81f8f…`/66850・165、completeness `b4378609…`/34249・LIMITED 15（O01/O07 SAT、13 LIM）。
- Profile: `production-profile.json` 13748B `aff05fd5…`、12 dims＋12 obligations＋named3（Jev mandatory・DSpark or verified equivalent・as-of `2026-09-21T16:10:00Z`）、`OPEN_HISTORY_AS_OF`。
- 7 生成物（全 `READY_FOR_ARCHITECTURE_REVIEW`、`PROPOSED`/`ESTABLISHED`、`human_review null`、Human/stage なし）:
  matrix 239359B `2f62e2a8…`、selection 76603B `4e6884d6…`、architecture 33219B `4af84ab3…`、
  summary 67700B `d0092e13…`、attention 15918B `482f3c21…`（65/50/15）、input 72613B `072f90b6…`（frozen 一致）、audit 1530B `ad5474dafb79276d41a580aa48c394757195b7fe53a60bcd3092498254d15449`（64-hex 修正済、内 6 pin 一致）。
- 本 dossier は canonical authority の前段階の Sol dossier であり、canonical reviewed-commit/branch/Human 権限・Production 権限とは区別する。遠隔 Production write を推認しない。

## 2. 研究 coverage（intake 面・Discovery 規模・独立 completeness・残 gap）

- Source intake: publisher intake＋supplement＋fixed c8/17 文書/3 archive のみ再利用。新規 standing crawl・current-main・Production checkout・code/weights 採用・新 publisher fetch なし（権限なし）。
  保持 authority: fixed774/c8＋17 named SP URLs/version metadata（papers/Jev/vLLM/PR27742/HF/Dynamo、P5 `did-bodies.md`）＋3 archive HTML u1/u2/u3＋S142 summary 3751B。
- Discovery: `discovery-accepted-v2.json` 135693B `2413dbe2…`、Matrix 160 行。Screening: `screening-accepted.json` 69226B `6ff524b0…`。
  Attention 65 件（§5 詳述）は screening-ledger-selection の review DATA（canonical producer ではない）から inventory。
- 独立 completeness: Matrix 160＝132 MATERIAL＋28 CONTEXT、Ledger 165＝132＋28＋5 EXCLUDED（D140/D158–D161）。
  SELECTED 130＝126 MATERIAL＋4 CONTEXT（D070/D071/D119/D141）。HOLD 30＝6 MATERIAL（D040/D049/D063/D142/D153/D162）＋24 CONTEXT。DROP 5＝nonmatrix。
  prior 156 unchanged byte-eq＋3 supp-ID rotations＋Ledger 165 parsed-identical＋O10 archive-aware LIMITATION は bounded 再利用（再カウントせず）。
- 残 coverage gap: Discovery locators D005/D061/D062/D093/D094/D098/D112/D117/D139 wrong-identity bytes（frozen-validated supplement で引用、amendment は Sol へ deferred）、full-body section/ablation outstanding（abstract-scope は scope 通り保持）、Jev thin、AIPerf unconsumed、MiniMax/gpt-oss unconfirmed、per-figure/version pins outstanding。候補数だけでは completeness 根拠にしない。

## 3. Evidence quality（status 数＋authority-consumption：何 primary body を実際に消費したか）

- Evidence 160（PARTIAL 152/VERIFIED 8）、Views 160、Ledger 165、Completeness LIMITED（2 SAT/13 LIM、closure FULL 8-field）。
  `PRIMARY_OFFICIAL` bind だけでは `AUTHORITY_CONSUMED` を証明しない。
- 消費区分（Sol §4.2）:
  - `AUTHORITY_CONSUMED`: D070 u1 served/CDX/decoded bound＋vendor quarantine、D071 u2 同＋255 不在 honored、D141 u3 served-row bound＋rate-limit qualifier、D143 Engram paper allocation law＋delta table＋U-law/LogitLens（§2 範囲）、D030 `dba1be0` README-scope CONFIRMED、D165 PR27742 existence PR-reported-only、V41 §2.4.3/§3.2 section scope、Kimi fair-comparison section scope、EAGLE/Snell/s1/TTC headline section/table scope、FrugalGPT Table3 matched-accuracy（prices stale）。
  - `AUTHORITY_CAPTURED_BUT_UNCONSUMED` として残すのは測定核ではない: abstract-scope SUPPORTING は background/conditions としてのみ配置し、未消費の equations/per-figure を引用しない（boundaries で強制、Draft で再検査）。
  - `AUTHORITY_NOT_FOUND`: D142 API body（INFERENCE HOLD、summary-scope のみ）、RLCD 内部/benchmark/calibration/independent repro、unserved u3 `21091419`/pre-09-20、vLLM/Dynamo pinned-09-20、AIPerf standalone、MiniMax/gpt-oss mechanisms。
  - `AUTHORITY_RETRIEVAL_FAILED`: 該当は HOLD 理由に明示（例：D153 card/interface not fetched、D163 version UNRESOLVED）。
- 重要 primary 17 bodies は retained captured DATA として where helpful に参照（再 fetch なし）。inventory ≠ full semantic read。116 SUPPORTING の全 semantic read を主張しない（machine `read_scope` 参照）。

## 4. 主要候補 map（theme・disposition・簡潔理由）

- SELECTED 130＝PRIMARY 14＋SUPPORTING 116。PRIMARY は正確に 1 package（p4×5、p5×5、p6×1、p7×1、p9×2）:
  Qwen3.8-Next D008・Kimi Linear D027・V41 report D123・V3.2 report D125・Engram D143（p4）、EAGLE D036・Snell D148・s1 D149・ThinkPrune D150・Overthinking D151（p5）、llama.cpp PR27742 D165（p6）、FrugalGPT D154（p7）、V4.1 card D030・V3.2-Exp D032（p9）。
  各 PRIMARY は model/version/benchmark/date/harness/authority/vendor-vs-independent＋conditions 付き measured-effect。
- SUPPORTING 116 は各 ≥1 package（p1 3、p2 19、p3 15、p4 22、p5 6、p6 14、p7 15、p8 3、p9 19）。dense/scaling/MoE/attention/decoding/precision/serving の genealogy/background を担い、abstract-scope は equations/per-figure を引用しない。
- HOLD 30 は配置なし（§5 全件）。6 MATERIAL HOLD（D040 DSpark bundle、D049 MXFP4、D063 Dynamo lens、D142 API unfetched、D153 effort-control、D162 X social）は living-docs/current-only/unfetched/social ceiling。
  4 CONTEXT SELECTED（D070/D071/D141 Jev vendor case、D119 GenAI-Perf docs distinct）は quarantine/docs-only で配置。
- EXCLUDED 5（D140/D158–D161）は Matrix 外、park-leaning/boundary probes。

## 5. Negative-space / omission review（選ばれなかった重要候補となぜ publication にないか）

- Attention 65 全件 inventory（review DATA、canonical producer ではない）:
  MATERIALITY:EXCLUDED 5＋SCREENING:DROP 5（同 5、park-leaning）、SCREENING:INSPECT 5（D032 homepage-only、D077 AI-drafted、D093 Which-Pro normalization、D119 AIPerf identity、D150 body-unread）、SCREENING:MAYBE 20（secondary/pricing/watches/harness/boundary/survey）、SELECTION:HOLD 30（shown 15＋overflow 15）。
  Shown 50＝5＋5＋5＋20＋15。Overflow 15 は隠蔽ではなく negative-space として本 dossier＋machine に全件記載:
  D004/D040/D063/D073/D075/D076/D080/D085/D086/D087/D097/D099/D147/D152/D162。
  高 signal MATERIAL 6 HOLD は shown 3（D049/D142/D153）＋overflow 3（D040/D063/D162）で全件 HOLD ceiling 保持、appendix smuggle なし。
- 重要 HOLD の不採用理由: D040 paper ablations 不在・workload-only・as-of not proved、D049 dispatch not audited、D063 body not line-level、D142 body unfetched INFERENCE、D153 card/interface not fetched summary-only、D162 social-only no technical fact、D004/D163 current-only、D075/D076 pricing snapshot、D086/D087 watches mechanism unconfirmed、D097/D099/D100 harness/authority-only、D146/D147 boundary precedents、D152/D156 secondary surveys。
- Silent exclusion なし。MiniMax/gpt-oss watches、AIME/DeepSWE/BrowseComp methodology-only holds も明示。

## 6. Editorial thesis（issue 全体として何を言い、何が period/profile に合うか）

dense 巨大化から必要な計算・メモリ・生成・waste 削減・生成回避への architecture/systems co-design 転換を、as-of 2026-09-21 scope の一次資料で測定可能な効果と trade-off として確立する。
vendor 報告は vendor として隔離し、独立再現・RLCD 内部・calibration を NOT FOUND のまま O10 LIMITATION とし、current-only・secondary・watch は配置せず dossier に留める。
全数値に model/version・benchmark version・date・harness・authority・vendor/independent を bind し横断比較を暗示しない。
14 PRIMARY を正確に 1 配置し 116 SUPPORTING を 1 以上配置し継承 boundaries を保持する。

## 7. Architecture packages（順序・role・primary/supporting・claim 境界・rationale）

- p1-bottleneck（O01）: primary 0＋supp 3（Kaplan/Chinchilla/Orca）。boundaries 5。dense anchor＋isoFLOP outstanding、scheduling detail なし、cross-ranking なし。
- p2-scaling-adaptation（O02＋O09）: 0＋19（FP8/Muon/MTP/Megatron/ZeRO/FSDP 等）。boundaries 23。prices/formulation outstanding。
- p3-moe（O03）: 0＋15（Shazeer/GShard/Switch/Mixtral/DeepSeekMoE/V2/KTransformers 等）。boundaries 20。per-expert micro-benchmarks 除外。
- p4-attention-engram（O04＋O13）: 5＋22（Qwen3.8-Next/Kimi/V41/V3.2/Engram 核＋MQA/GQA/FlashAttention/Mamba/H2O/SnapKV 等）。boundaries 37。V41 Appx per-figure＋Qwen ablations＋Kimi tables not cited＋PLE parallel unresolved。
- p5-decoding-testtime（O05＋O14）: 5＋6（EAGLE/Snell/s1/ThinkPrune/Overthinking 核＋speculative/Medusa/MTP 等）。boundaries 16。DSpark/Medusa per-body＋HW/batching/quality outstanding。
- p6-precision-local（O06＋O07）: 1＋14（PR27742 核＋LLM.int8/GPTQ/SmoothQuant/AWQ/QLoRA/SparseGPT/BitNet/GGUF/llama.cpp 等）。boundaries 25。GGUF-not-algorithm、correctness/rebuild 除外。
- p7-serving-routing（O08＋O15）: 1＋15（FrugalGPT 核＋PagedAttention/SGLang/FlashMLA/TensorRT/Splitwise/RouteLLM 等）。boundaries 23。D061/D062 abstract、survey unifier deferred。
- p8-specialization-jev（O10）: 0＋3（D070/D071/D141 vendor historical）。boundaries 15。vendor-as-vendor、RLCD 推論なし、255-as-of なし、D142 schema/math なし、独立 bench/calibration なし。
- p9-capstones-measurement（O11＋O12）: 2＋19（V4.1 card/V3.2-Exp 核＋Qwen blog/GLM/MMLU-Pro/GPQA/HLE/LiveCodeBench/SWE/HELM/RULER/lm-eval 等）。boundaries 35。GLM abstract-only、vendor ratios conditional、harness/scaffold outstanding、AIPerf distinct。
- `selected_exceptions []`（全 SELECTED 配置済）。IDs は token-safe（`p1-bottleneck` 等）。空 package なし。empty-last-synthesis 充足。

## 8. Page/section 配分（intended length・structural balance・Paper Watch 等の省略含む）

- target 60pp / max 75pp: 14 PRIMARY 約1pp（14pp）＋116 SUPPORTING 約0.3pp（約35pp）＋thesis/intro/methodology overhead 約11pp＝60pp target、layout/figures slack で max 75pp。内訳 p1 3＋p2 5＋p3 4＋p4 10＋p5 9＋p6 6＋p7 5＋p8 4＋p9 9＝55pp 実質＋overhead 5pp。
  HOLD 30 は 0pp。履歴 63/85 や 66 は使わない。HOLD を配置に入れず、out-of-cutoff を appendix で smuggle しない。
- 130 in 60pp はそれ自体で quality を証明しない（§9 counterfactual 参照）。116 SUPPORTING の ~0.3pp は background/conditions のみで、equations/per-figure over-citation は boundaries＋Draft citation-boundary check で防ぐ。本 DATA は Draft を authorize しない。

## 9. Counterfactual alternatives（materially plausible な代替と棄却理由）

- (a) all-MATERIAL autopick（132 全選択）: 棄却。relevance と measured-effect を混同し HOLD ceilings を無視する。
- (b) Jev appendix waiver（D070/D071/D141 除外）: 棄却。mandatory O10 は quarantined vendor case として出現させねばならず、消去できない。
- (c) vLLM/Dynamo as-of deployment 証明化: 棄却。current-only で pinned-09-20 proof なし、as-of smuggle になる。
- (d) AIPerf＝GenAI-Perf 混同: 棄却。別 identity、AIPerf surface unconsumed。
- (e) X の SUPPORTING 昇格: 棄却。social-only で technical fact なし。
- 9 package 構造は 15 obligations の最小 coherent 分割。Jev を serving に統合、capstones を methodology に統合すれば mandatory quarantine と measurement taxonomy が隠れる。Special viability（THEMATIC/LONGFORM_SPECIAL reader-facing technical、9 packages、60/75pp、thesis＋lineage＋conditions）は明示的に要求し、2–3 lanes への silent narrowing はしない。

## 10. 既知 limitations と risks（completeness・chronology・publisher-only・unresolved・carry-over・躊躇理由）

- D142 API body 未取得、RLCD 内部・benchmark/calibration・独立再現なし、unserved u3 `21091419`・pre-09-20 未取得、D141 card-vs-current alias contradiction の accepted 側訂正は root/normal-producer 業務、vLLM/Dynamo pinned-09-20 なし、per-figure pins（V41 Appx B/C、Qwen ablations、Kimi tables、routing/TTC、harness/scaffold/version）outstanding、AIPerf standalone unconsumed、MiniMax/gpt-oss unconfirmed。
- Discovery locator wrong-identity（D005 等）は frozen-validated supplement で引用、amendment deferred。
- Abstract-scope SUPPORTING の unconsumed equations/per-figure 引用 risk は boundaries＋Draft check で mitigation。
- Human が躊躇すべき理由: 上記 LIMITATIONS が canonical 生成・Draft 引用境界まで保持されることが条件。60pp 配分は quality 証明ではない。source 3231 は execution commit で Human-reviewed ではない。

## 11. Sol review finding（explicit blocking/non-blocking＋recommendation）

- Blocking findings: なし。具体的な CHANGES_REQUIRED（matrix/selection/architecture/summary/attention/audit の修正）はない。
  counts/dispositions/packages/obligations/numerics/Jev/D142/deployment/Engram/GenAI-Perf/X/mechanical shapes/placement/IDs/boundaries/empty-exception は全て充足。
  65 attention 全件＋30 HOLD＋5 DROP を inventory し、高 signal MATERIAL 6 HOLD の HOLD ceiling を確認、silent exclusion なし。
  60pp は gap を隠さず、代替案を検討し、Special viability を narrowing せず要求する。
- Non-blocking preserved LIMITATIONS: §10 の 7 項目を LIMITATION のまま canonical 生成・Draft 引用境界まで保持すること。
  Abstract-scope の over-citation risk は Draft check が必須。
- Recommendation: **EDITORIAL_READY_FOR_NORMAL_STAGE** — root normal `build_stage_checkpoint` / `advance_with_checkpoint` へ進む準備ができた。
  Selection PASS・Architecture PASS・R4・quality/adoption/savings・Human 承認ではない。

## 12. Human decision options（canonical authority の後にのみ提示、現時点では要求なし）

- 現時点では `APPROVED` / `REQUEST_CHANGES` を求めない。State `EVIDENCE_REVIEWED`、canonical reviewed-commit/branch/Human 権限・Production 権限は別であり、本 dossier はその前提を満たさない。
- 将来 canonical authority の後、Human が判断できる options（参考、現時点では選択を求めない）:
  - `ARCHITECTURE_REVIEW` で `APPROVED`: exact Human-reviewed commit＋exact review bytes＋immutable approval snapshot が canonical work branch に存在し、reachability が確認され、本 dossier 12 項目＋Sol findings が提示された後。
  - `ARCHITECTURE_REVIEW` で `REQUEST_CHANGES`: 上流 defect（research depth・role separation・presentation）が露見した場合、正しい `REQUEST_CHANGES` path で edition を repair し、edition-local vs shared を分類し、本 governance/checklist を shared の場合に更新し、crisp machine-testable の場合のみ deterministic protection を追加し、semantic review 責任を保持する（governance §10）。
  - `PUBLICATION_PREVIEW` は exact-byte Candidate-bound PDF のみが対象。rebuilt/different PDF は reviewed Candidate ではない。
- Next: root が本 findings/dossier を inspect し、別途 precise normal-stage dispatch を出す。old writer rerun/regeneration/manual State、auto generic reader/R4/PDF/Production なし。
  Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN。Human Commit Point で停止。Ordinary Commit/Push は Human-owned。

*counts: 160 assignments（SELECTED 130＝PRIMARY 14＋SUPPORTING 116、HOLD 30）＋5 nonmatrix EXCLUDED＝165 ledger；Matrix 132M/28C SELECTED 126M/4C；attention 65/50/15；packages 9；60 target/75 max；pins・gaps は `sp-substantive-review.md`・`sp-substantive-review-machine.json` を参照。*
