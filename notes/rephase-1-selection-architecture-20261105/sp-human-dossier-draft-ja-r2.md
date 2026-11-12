# SP 人間向け Architecture ドラフト r2（案・未承認） — efficient-llm-2026

**位置づけ:** AUTHOR r2 DATA案。v1 (`sp-candidate-map.json` + dossier) に対する独立review `CHANGES_REQUIRED` と `sp-jev-authority-inventory.md` 新知見を受けた訂正。独立review承認・Architecture承認・Human Gate・Draft/PDF・R4は未了。Stateは`EVIDENCE_REVIEWED`のまま。受容済Evidenceの編集はしない。訂正はRootへの正確な scope 提示に留める。

## r2で直したこと（fetchなし）

- D142はSELECTEDからHOLDへ。unfetched APIはtyped mechanismにできない。summary-level契約＋NOT FOUNDのみ。P8 as-of章は削除し、O10はLIMITATIONのまま付録A＋scope返上で閉じない。
- D141はHOLD維持。cardの `aliases ->1.13.0` は現行body `aliases ->1.14.0` と矛盾（dated summary vs new body distinct）。受容済み修正 scope をRootへ提示し、ここでは編集しない。
- D040/D049/D063/D153はSELECTEDからHOLDへ。現行vLLM/Dynamo条件を継承する as-of serving proofにできない。V41 §2.4.3＋README dba1be0のarchitectureは既存束縛で足り、vLLM/Dynamoは配置gapとして付録Aへ。paperに独立根拠がある場合のみ制限引用（今回は移動）。
- D143 EngramをPRIMARYへ。body-consumed deltas (MMLU +3.4/CMMLU +4.0/MMLU-Pro +1.8/BBH +5.0/ARC-C +3.7/DROP +3.3/HumanEval +3.0/MATH +2.4/GSM8K +2.2 + U-law + LogitLens) でO13 measured core。allocation-curve/training-costはoutstanding。
- O01/O03/O08/O09/O12/O13はPRIMARY全義務化ではなく evidence-bearing baseを明示: O01はKaplan/Chinchilla/Orca語彙 4pp、O03は系譜＋V41/Qwen/Kimi cross-mapped measured、O08はOrca/Paged/SGLang等＋V41 §3.2/DSpark cross-mapped、O09はHinton/LoRA等 history、O12はseed benchmarks＋GenAI-Perf docs (D119はAIPerf openと別claimで利用可)、O13はD143 PRIMARY。all MATERIAL autopick 131ではない。
- 70ppはclaim utilityで unpack/削減: measured p4/p5/p6/p9は10/10/7/10pp維持、lineage-only p1/p2/p3/p7は4/6/5/6ppへ削減、p8削除。target 58/max 80＋付録A 6pp独立で計64。prior 66pp copyでも任意shrinkでもない。

## 対象と読み方（r2維持）

- as_of `2026-09-21T16:10:00Z`。Evidence 160 (8 VERIFIED/152 PARTIAL)、Ledger 165、義務15 LIMITATION (O01/O07 SATISFIED)。VERIFIED/PARTIAL等は既存ラベル。
- 現行onlyは付録Aに隔離しas-of coreと混同しない。PR数値は `pr.json 26122B 3728e08d…` のみ、packetはchronology context。
- D119はSELECTED SUPPORTING (GenAI-Perf docs VERIFIED、AIPerf openは別)。D162はHOLD lead-only (技術・経済・license根拠にしない)。

## 今号の主張 r2（方向維持、O10は閉じない）

dense巨大化から co-designへ。条件付き数値のみで横断ランキングなし。O10はLIMITATIONのまま: 契約存在＋NOT FOUND＋現行quarantine＋再現thinを明示し、09-21 VERIFIEDは主張しない。

## 目次案 r2（58pp target / 80 max＋付録A 6pp独立、計64）

- P1 ボトルネック 4pp: Kaplan/Chinchilla/Orca語彙のみ。係数表等扱わず。
- P2 スケーリング・適応 6pp: Megatron/GPipe/ZeRO/FSDP/Ulysses/Ring＋Hinton/LoRA等 history。D159-161 EXCLUDE。
- P3 MoE 5pp: Shazeer/GShard/Switch/Mixtral/DeepSeekMoE/Qwen3/MoD/LayerSkip/ExpertChoice/MegaBlocks系譜。MiniMax/gpt-ossはwatch言及のみ。
- P4 注意・Engram 10pp: PRIMARY Kimi/Qwen/V41/V32 section-level＋D143 deltas。per-figure/ablations/licenseはquarantine。PLE並列未解決。
- P5 デコード・テスト時 10pp: PRIMARY EAGLE Fig1＋Snell 4x/14x＋s1 27%/50→57%＋ThinkPrune Table1＋overthinking CI/cost。Snell系はO14。DSparkはV41＋READMEで充足。
- P6 精度・ローカル 7pp: PRIMARY D165 existence＋PR-reported numbersのみ。GGUFはformat。MXFP/B200条件付き。
- P7 サービング・routing 6pp: PRIMARY FrugalGPT Table3。D061/062 abstract-scope、D158 EXCLUDE。D040/D049/D063はHOLDへ移動済み。
- P9 Capstones・計測 10pp: PRIMARY D030 README@dba1be0＋D032 launch。Qwen/Kimi/V41/V32配置はP4 PRIMARY再掲せず、ここではspec/価格/throughput/評価条件とmethodology (MMLU-Pro/GPQA/HLE/LiveCode/SWE/RULER/lm-eval/HELM＋GenAI-Perf)。GLM abstract-only、AIPerf open。D153はHOLDへ移動済み。
- 付録A 現行context 6pp独立: D004/D070/D071/D141/D163＋D040/D049/D063/D153/D142/D162＋watches/precedents。O10/O04/O08/O11 LIMITATION retained。

## 選ばなかったもの r2

- HOLD 33: 上記＋D142 summary-only。主章非引用、付録Aまたは言及のみ。
- EXCLUDED 5 taskless DROP lawful維持。
- P8削除: D142 unfetchedではtyped mechanism章は成立しない。O10はscope返上。

## 残る限定・Rootへの正確な修正依頼（受容済み編集なし）

- D141: claims alias `->1.13.0` vs 現行 `->1.14.0`、verification UNRESOLVED維持。修正はRootへ。
- D142: claims契約はsummary-only、verification VERIFIEDラベルとPARTIAL/UNRESOLVEDの不整合はbody検証としない。修正はRootへ。
- D040/D049/D063/D153: 現行継承ではas-of proof不可。HOLDが上限。as-of配置主張にはG1/G2 historical pinが必要（現提案は主張しない）。
- O10 historical VERIFIEDにはG3 archive snapshotsが必要。現 captures ではHOLD＋LIMITATIONが上限でwaive不可。

## 次に必要なもの

独立re-reviewを経て正式 dossierとし、ARCHITECTURE_REVIEWへ。Draft/PDFは承認前作らない。Typed APIは本r2 map後。Rootは3 TypeSafe URLsのlimited archive accessを別途問う。Human Q1Q2Q3は不要。

*出典pin・counts・gapsは`sp-candidate-map-r2.json`、gap詳細は`sp-essential-gap-map.json`。165 join/160 Matrix＋5 nonmatrix維持。*
