# SP 人間向け Architecture ドラフト（案・未承認） — efficient-llm-2026

**位置づけ:** AUTHOR DATA案のみ。独立research/selection review・Architecture承認・Human Gate・Draft/PDF・R4は未了。Stateは`EVIDENCE_REVIEWED`のまま。数値・日付の限定を隠さない。詳細machineは`sp-candidate-map.json`、仮説訂正は`sp-initial-author-hypotheses.md`。

## 対象と読み方

- as_of `2026-09-21T16:10:00Z` (`OPEN_HISTORY_AS_OF`)。Evidence 160（8 VERIFIED/152 PARTIAL）、Ledger 165（132 MATERIAL/28 CONTEXT/5 EXCLUDED）、義務15（2 SATISFIED O01/O07、13 LIMITATION）LIMITED。
- VERIFIED/PARTIAL・MATERIAL/CONTEXTは既存ラベルであり新規PASSではない。ベンダー数値は未再現、前提は本文限定どおり。
- 現行only 5（D004/D070/D071/D141/D163）はas-of歴史証明ではない。付録Aに隔離し、as-of coreと混同しない。O10はLIMITATIONのまま閉じない。
- PR数値はbound `pr.json 26122B 3728e08d…` のみ。packet `4143b4ad/c1b1f7d5/541bd239` はchronology review-contextでありstaged権威ではない（D165 2-field fix維持）。

## 今号の主張（案）

**dense巨大化から「必要計算・保持memory・生成高速化・serving waste削減・生成回避」のarchitecture/systems co-designへ。測定可能効果は条件付き数値でのみ示し、横断ランキングをしない。**

1. ボトルネック言語（P1）で一語化高速化を禁止する。
2. スケーリング・適応（P2）はChinchilla起点とdistillation/LoRAを分離する。
3. MoE（P3）は系譜とtotal/active・通信・residencyで追跡する。
4. 注意機構（P4）はexact-IOとcompute/storage変更を区別し、Kimi/Qwen/V41/V32のsection-level効果で示す。per-figureは引用しない。
5. デコーディング・テスト時（P5）はEAGLEとSnell/s1/ThinkPrune/overthinkingを分離する。Snell系はO14でありO05に含めない。
6. 精度・ローカル（P6）はGGUFはformat、D165 port存在を correctness/rebuildなしで束縛する。
7. サービング・ルーティング（P7）はFrugalGPT Table3とRouteLLM pipelineをfragility bound付きで示す。
8. Jev特化（P8）は契約中心・現行限定明示。vendor claimはquarantine、再現thin・calibrationなしを明示する。
9. Capstones・計測（P9）は4機ランクなし＋methodology。GLMはabstract-only、MiniMax/gpt-ossはwatch、AIPerfはopenだがGenAI-Perf docsは別claimとして利用する。

## 目次案（70pp target / 92 max、付録A 6pp別、計76）

- P1 ボトルネック 6pp: Kaplan/Chinchilla/Orca。係数表・isoFLOP・scheduling詳細は扱わない。
- P2 スケーリング・適応 8pp: Megatron/GPipe/ZeRO/FSDP/Ulysses/Ring + Hinton/LoRA/R1等。D159-161 EXCLUDE。
- P3 MoE 8pp: Shazeer/GShard/Switch/Mixtral/DeepSeekMoE/Qwen/GLM系＋MoD/LayerSkip/ExpertChoice/MegaBlocks。
- P4 注意・Engram 10pp: PRIMARY Kimi/Qwen/V41/V32 section-level＋Engram body-level。Appx B/C per-figure・ablations・licenseはquarantine。
- P5 デコード・テスト時 10pp: PRIMARY EAGLE Fig1＋Snell 4x/14x＋s1 27%/50→57%＋ThinkPrune Table1＋overthinking CI/cost。DSparkはV41 §2.4.3＋READMEで充足、vLLM歴史は配置gapのみ。
- P6 精度・ローカル 7pp: PRIMARY D165 existence＋validation-report scope。GGUF境界、MXFP/B200条件付き。
- P7 サービング・ routing 8pp: PRIMARY FrugalGPT Table3。D061/062 abstract-scope、D158 EXCLUDE、survey二次はdeferred明記。
- P8 Jev特化 5pp: SUPPORTING D142契約＋現行HOLDs付録参照。09-21 VERIFIED主張なし、再現・calibration outstanding。
- P9 Capstones・計測 8pp: PRIMARY D030 README@dba1be0＋D032 launch。Qwen/Kimi/V41/V32配置はP4 PRIMARYを再掲せず、ここではspec/価格/throughput/評価条件とmethodology（MMLU-Pro/GPQA/HLE/LiveCode/SWE/RULER/lm-eval/HELM＋GenAI-Perf docs）をbind。GLM abstract-only、AIPerf open。
- 付録A 現行context 6pp: D004/D070/D071/D141/D163＋D162 lead-only＋watches（D075/076/077/086/087等）。as-of外明記。

## 選ばなかったもの

- HOLD 28: 現行only 5＋X受容 lead-only＋watches＋precedents/boundary（kNN-LM/RETRO、survey follow-ups deferred、caveated harness等）。いずれも主章非引用、付録Aまたは言及のみ。
- EXCLUDE 5 taskless DROP lawful: D140 park-leaning、D158 collaboration boundary、D159 encoder-era、D160 TinyBERT重複回避、D161 training-free metric。
- CONTEXT内 D119のみ SELECTED: GenAI-Perf docs VERIFIEDはAIPerf missingと別claimであり利用可能。AIPerf openはlimitationとして残す。
- D162はSELECTEDにしない: ledger受容 VERIFIEDだが技術・経済・license事実の根拠にできない per limitations。

## 残る限定（Humanが躊躇すべき点）

- O10 JevはLIMITATIONのまま。09-21 revision取得時のみ upgrade可能。現状HOLD＋quarantineが誠実な上限。
- O05 DSpark ORはV41 body＋READMEで充足。vLLM pinned-09-20は配置gapでありarchitecture blockではない。
- per-figure/harness/licenseはfigure番号引用時のみ REQUIRED。現提案は引用しないため新規fetch不要。
- 追加fetchは特定gapのみ。broad crawlなし。

## 次に必要なもの

独立research/selection reviewを経て正式 dossierとし、`ARCHITECTURE_REVIEW` の APPROVED/REQUEST_CHANGESを受ける。Draft/PDFは承認前作らない。Typed API JSONは本map後。

*出典pin・読解範囲は`sp-candidate-map.json` source_pins/read_scope、countsは同counts、gapsは同essential_gaps。*
