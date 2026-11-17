# SP Architecture Review Dossier r2（人間向け・未承認・canonical 前・root §1 修正） — SP-efficient-llm-2026

**位置づけ:** Fresh independent SUBSTANTIVE reviewer r2（not author/operator/root/Human）による packet-local dossier。
r1 dossier は SUPERSEDED 履歴として保存（top note のみ追加、本文保存）。本 r2 が現行。
`source 3231a0c280287411513bba359f4d3d2b6703f591` は execution commit であり genuine Human-reviewed commit ではない。
State `EVIDENCE_REVIEWED`。approval 要求なし。stage actions の前に root review が必須。
ガバナンス FULL＋root `astra-operation-resolution.md` §§1–2（prevails）に準拠。

## 1. 正確な review identity（r1 stale 修正）

- Edition `SP-efficient-llm-2026`（THEMATIC/LONGFORM_SPECIAL）。実 repo `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`、
  `3231a0c…`/parent `ae0dd1e…`/tree `ff01b73e…`（frozen、DIRECT409 final143/774 `0dc361cb…`/187361B、`76ac1318…`/5691014B）。
- State `38a63411…` 4266B `EVIDENCE_REVIEWED`、guard なし。**訂正: 現 3231 は 7 生成物あり（下記）。旧 ae0 の `7 slots absent` は現 copy の記述ではない。**
- PREARCH `sp-repaired-20261112-r2` `2a528ed5…` 6300B `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` が active。
  **訂正: 旧 canonical Ledger/Completeness は inactive。** Active authority は PREARCH R2 の 4 refs
  （evidence `7f04e9ad…`/49237、views `45d60f9f…`/64222、ledger `5cf81f8f…`/66850、completeness `b4378609…`/34249 LIMITED 15）。
  `materiality-ledger-v2.json` `b7c85b…`/`profile-completeness-v2.json` `d67f7f…` は inactive lineage であり active と label しない。
- Profile `aff05fd5…` 13748B、12 dims＋named3、as_of `2026-09-21T16:10:00Z`。
- **7 生成物あり（生成 ready 済、writer 再実行不要）:**
  matrix `2f62e2a8…`/239359、selection `4e6884d6…`/76603、architecture `4af84ab3…`/33219、
  summary `d0092e13…`/67700、attention `482f3c21…`/15918（65/50/15）、input `072f90b6…`/72613（frozen 一致）、audit `ad5474dafb…`/1530（内 6 一致）。
  全 `READY_FOR_ARCHITECTURE_REVIEW`、`human_review null`。**訂正: 将来は canonical 再生成ではなく normal stage checkpoint/advance。**
- 本 dossier は canonical 前の Sol dossier。canonical reviewed-commit/branch/Human 権限・Production とは区別。

## 2. 研究 coverage

- 再利用のみ、新規 fetch なし（fixed c8/17 文書/3 archive＋S142 3751B＋supplement pins）。
  Discovery 160 行、Screening `6ff524b0…`、Attention 65（review DATA、canonical producer ではない、bind hash `482f3c21…` 保持）。
- Matrix 132M/28C、SELECTED 126M+4C（D070/D071/D119/D141）、HOLD 6M+24C、DROP 5。Ledger 165。
  prior 156 byte-eq 等は bounded 再利用。
- 残 gap: Discovery locator wrong-identity（supplement 引用、amendment deferred）、full-body outstanding（abstract-scope は scope 通り）、Jev thin、AIPerf open、MiniMax/gpt-oss unconfirmed、per-figure/version outstanding。

## 3. Evidence quality（r1 ラベル訂正＋高 risk 2 件 direct read）

- Evidence 160（PARTIAL 152/VERIFIED 8）、Views 160、Ledger 165、Completeness LIMITED。`PRIMARY_OFFICIAL` bind は `AUTHORITY_CONSUMED` の証明ではない。
- **D142 訂正:** 既知 locator `https://docs.typesafe.ai/api`、body NOT_ACQUIRED/UNINSPECTED、supplement なし、`source_bindings` absent。
  Task＋result direct read: INFERENCE x2 summary-scope（S142 3751B line44）、limitation “page not fetched”、verification UNRESOLVED x2。
  ラベルは UNKNOWN/NOT_ACQUIRED。attempt-failure 証拠なしのため `AUTHORITY_NOT_FOUND` でも `AUTHORITY_RETRIEVAL_FAILED` でもない。
  Summary-scope であり global absence ではない。HOLD ceiling。
- **D153/D163 訂正（fabricated failure なし）:** D153 PARTIAL VERIFIED（D163 で corroborated、card bodies outstanding、SUMMARY_CAPTURED）。
  D163 PARTIAL UNRESOLVED x2（current-only 2705796B `fa61427e…`、pinned-09-20 NOT verified、highest drift risk、SUMMARY_CAPTURED）。
  取得失敗ではなく capture 履歴通りの current-only。HOLD。
- **D119 direct read（prior 再利用不足分）:** task LOCATOR_CAPTURED＋result PARTIAL。
  Source `supplement-src-6fe51b459a274631` PRIMARY_OFFICIAL（NVIDIA docs URL）。
  Claims PROJECT_CLAIM x2（throughput/TTFT/ITL/request throughput＋genai-perf/ path 一致、Docs bytes consumed／phased out in favor of AIPerf、standalone AIPerf not located）。
  Limitations INFERENCE x2（repo not cloned、AIPerf identity open）。Verification VERIFIED（Docs consumed）＋UNRESOLVED（Successor named only、not closed by assertion）。
  SELECTED SUPPORTING docs-only、AIPerf distinct open。taxonomy 利用には loadbearing ではない（§8）。
- **D141 訂正:** alias 1.13 fix は r2 で adopted 済（result VERIFIED: served-scope 1.13-only、1.14 drift post-cutoff not conflicting）。pending contradiction として carry しない。
- D143/D030/D165/D032 等は §4 narrow roles 参照。重要 17 bodies は retained captured DATA として参照。inventory ≠ full semantic read。

## 4. 主要候補 map（PRIMARY は editorial role、万能 measured-effect 証明ではない）

- SELECTED 130＝PRIMARY 14＋SUPPORTING 116。PRIMARY は正確に 1 package（p4×5、p5×5、p6×1、p7×1、p9×2）。
- **Narrow 訂正:**
  - D165 PRIMARY p6: VERIFIED existence（PR27742、65 commits、merged 2026-08-27）＋PR-reported numbers（ppl 4.0068/4.0126、98% agreement 等）。Category “existence authority NOT correctness/rebuild”。 existence のみ。
  - D032 PRIMARY p9: VERIFIED launch announcement narrow（DSA debut、50%+ price cut、artifact identities）。launch authority であり mechanism 証明ではない。
- 他 PRIMARY も section/table/headline scope＋quarantine＋ablations outstanding。SUPPORTING 116 は background/conditions のみで equations/per-figure を引用しない。

## 5. Negative-space（65 全件保持、30 HOLD/5 DROP exact、overflow 15＋高 signal 3）

- Attention 65: EXCLUDED 5＋DROP 5（同 5）＋INSPECT 5（D032/D077/D093/D119/D150）＋MAYBE 20＋HOLD 30（shown 15＋overflow 15）。
  Shown 15: D117/D082/D120/D077/D049/D142/D153/D079/D163/D146/D156/D084/D072/D100/D074。
  Overflow 15: D004/D040/D063/D073/D075/D076/D080/D085/D086/D087/D097/D099/D147/D152/D162。
  高 signal MATERIAL 6: shown D049/D142/D153＋overflow D040/D063/D162。全件 HOLD ceiling、smuggle なし。
  Bind hash `482f3c21…` 保持。詳細は r2 machine。
- Silent exclusion なし。

## 6. Editorial thesis

dense 巨大化→必要計算・メモリ・生成・waste 削減・生成回避の co-design 転換を as-of 2026-09-21 一次資料で測定効果と trade-off として確立。
vendor は vendor 隔離、RLCD/benchmark/calibration/独立再現は NOT FOUND のまま O10 LIMITATION、current-only/secondary/watch は dossier に留める。
全数値に model/version/benchmark/date/harness/authority bind、横断比較を暗示しない。14 PRIMARY 1 配置＋116 SUPPORTING 1 以上＋boundaries 保持。

## 7. Architecture packages

- p1 0+3、p2 0+19、p3 0+15、p4 5+22、p5 5+6、p6 1+14、p7 1+15、p8 0+3、p9 2+19。must_cover O01–O15 過不足なし。`selected_exceptions []`。
  Boundaries total 199 は review DATA の descriptive limits であり、将来 Draft を enforce する proved state constraint ではない。
  Draft 引用境界 check は将来独立 work。

## 8. Page 配分（formal trigger なし、voluntary dense 評価）

- 60pp/75pp: 14×~1pp＋116×~0.3pp＋overhead ~11pp。HOLD 0pp。
- **訂正:  governance extreme test `SELECTED <=1` の formal trigger は 130 には適用されない。** Formal compression-PASS を主張しない。
  Voluntary dense 評価: 130 in 60 は quality を証明しない。116×~0.3pp は background-only で over-citation risk あり。mitigation は将来 Draft check（not proved）。
- Special viability: LONGFORM_SPECIAL 必要 Special は 9 packages で確保。116 abstract-only は background であり 2–3 lanes への silent narrowing ではない。
  Actual missing primary reading critical? AIPerf open は D119 taxonomy 利用に loadbearing ではない（LIMITATION 保持）。
  D142 missing は HOLD（publication 外）。Scoped review で concrete loadbearing gap なし。将来 Draft で AIPerf facts/per-figure が要れば Draft-stage gap。

## 9. Counterfactual alternatives（scoped、universal 主張なし）

- (a) all-MATERIAL、(b) Jev waiver、(c) vLLM/Dynamo as-of、(d) AIPerf 混同、(e) X 昇格はいずれも棄却（HOLD ceilings/別 identity/social-only）。
  9 package 最小 coherent。
- Scoped counterfactual: reviewed 65＋7 direct reads＋bounded reuse の範囲では HOLD ceilings 内で concrete な代替 multi-item Architecture は支持されない。
  Full-corpus の universal “captured body は決して別 core を支持しない” は主張しない。

## 10. 既知 limitations/risks

- D142 UNKNOWN（summary-scope）、RLCD/benchmark/repro outstanding、unserved u3/pre-09-20 未取得（D141 fix 済、pending なし）、vLLM/Dynamo pinned-09-20 NOT verified、per-figure/version＋AIPerf open＋MiniMax/gpt-oss unconfirmed、abstract-scope over-citation risk（Draft check 要、not proved）、locator wrong-identity（supplement 引用、deferred）。
- Human 躊躇理由: 上記 LIMITATIONS が normal stage＋Draft まで保持されることが条件。3231 は Human-reviewed ではない。

## 11. Sol finding

- Blocking なし（scoped）。CHANGES_REQUIRED なし。65＋30＋5 inventory、高 signal 6 HOLD ceilings、Jev/D142/deployment/Engram/GenAI-Perf/X narrow roles、mechanical shapes/placement/IDs 充足。
  60pp gap 隠蔽なし、代替検討、Special narrowing なし。
- Non-blocking LIMITATIONS §10 を保持。Abstract over-citation は Draft check 必須。
- Recommendation: **EDITORIAL_READY_FOR_NORMAL_STAGE (scoped r2)** — root normal checkpoint/advance へ。Selection/Architecture PASS・R4・quality/adoption/savings・Human 承認ではない。

## 12. Human decision options（canonical 後にのみ、現時点要求なし）

- 現時点 `APPROVED`/`REQUEST_CHANGES` を求めない。State EVIDENCE_REVIEWED、canonical reviewed-commit/branch/Human 権限とは別。
- 将来 canonical 後の参考: `ARCHITECTURE_REVIEW` で `APPROVED`（exact Human-reviewed commit＋exact bytes＋immutable snapshot＋reachability＋本 12 項目提示後）／`REQUEST_CHANGES`（上流 defect は正しい path で repair、edition-local vs shared 分類、governance 更新、crisp な場合のみ deterministic 保護、semantic 責任保持）。
  `PUBLICATION_PREVIEW` は exact-byte Candidate-bound PDF のみ。
- Next: root が inspect し precise normal-stage dispatch。writer rerun/regeneration/manual State、auto reader/R4/PDF/Production なし。
  Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN。Commit Point 停止。Ordinary Commit/Push Human-owned。

*counts: 160（130＝14＋116、30 HOLD）＋5 EXCLUDED＝165；132M/28C SELECTED 126M/4C；65/50/15；9 pkgs；60/75pp；pins・gaps は r2 review＋r2 machine 参照。*
