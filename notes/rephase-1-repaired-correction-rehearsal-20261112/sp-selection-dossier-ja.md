# SP Selection/Architecture DATA dossier（案・未承認・条件なし再評価） — efficient-llm-2026

**位置づけ:** NEW SP Selection DATA author（not reviewer/operator/Human）による packet-local DATA 案。active ae0dd1e runtime、SP State `38a63411…`、PREARCH record `2a528ed5…`、R2 active four refs VERSIONED（evidence `7f04e9ad…`/49237・views `45d60f9f…`/64222・ledger `5cf81f8f…`/66850・completeness `b4378609…`/34249 LIMITED）に束縛。old canonical b7c/d67 は使わない。160 cards/views・165 ledger・15 obligations（O01/O07 SAT、13 LIM）・Profile 12 dims＋named3（Jev mandatory・DSparkまたは検証済み等価・as-of 2026-09-21T16:10:00Z）を実読した。`sp-selection-architecture-input.json`（160 assignments、165ではない）が runner 形状の本体で、本書は人間向け実質 dossier、`sp-selection-per-did-map.json` が per-DID 配置、`sp-selection-read-scope.json` が現行 pins/読範囲である。承認・Draft/PDF・R4・Human Gate・canonical 生成は含まない。canonical 生成は後続 root＋独立 review が行う。

## 1. 再評価の結論（条件付き 14/116/30 を鵜呑みにしない）

- prior r3 canonical 14 PRIMARY/113 SUPPORTING/33 HOLD、conditional 14/116/30（D070/D071/D141 HOLD→SELECTED、D142 HOLD維持）は仮説だった。R2 accepted revision（D070/D071/D141 歴史 rebind＋D142 UNRESOLVED 訂正、supplement `ff3ba775…`/31530、records `0a54004e…`、completeness `6929d9ca…` FULL 8-field）が normal HIGH で adopt され、156 unchanged cards/views byte-eq、3 supp-ID rotations のみ、Ledger 165 rows parsed-identical、O10 archive-aware LIMITATION が独立 postprepare review（BOUNDED_RESEARCH_DECISION_READY）で確認された。よって **14 PRIMARY/116 SUPPORTING/30 HOLD/5 nonmatrix＝165（Matrix 160＝14＋116＋30）を再評価の結果として採用**する。ただしこれは quota でも全 MATERIAL 自動選択でもない。
- MATERIAL 132 のうち 6（D040/D049/D063/D142/D153/D162）を HOLD に残す。CONTEXT 28 のうち 4（D070/D071/D141/D119）のみ SELECTED、24 は HOLD。SELECTED 130＝126 MATERIAL＋4 CONTEXT。HOLD 30 は配置なし、dossier に留める。source class は真実ではない。
- 15 obligations は honest に **2 SAT（O01 bottleneck、O07 local）・13 LIM**。O10 を含め自動 SAT なし。O13（Engram）・O14（TTC）・O15（routing）は completeness の追加 3 義務で、Profile 12 dims と一体で扱うが、独立証拠の薄さは LIMITATION のまま。

## 2. Jev mandatory case（D070/D071/D141 vendor 歴史 scope、D142 は INFERENCE lead）

- **D070 launch（u1 served 2026-09-21T03:30:22Z、wire gzip 42836B `10bf6607…` CDX `6XH5…` MATCH、decoded 253542B `14ae3118…`）**: new architecture＋parallel sampler＋RLCD 名のみ＋typed probabilistic outputs＋70–500ms/40–200x/$0.042/MTok in＋free out＋193.6x/444.6x（laptop/West-Coast・subsidy未証明・authorship/OpenRouter nuance 付き）を vendor 報告として SELECTED SUPPORTING。RLCD 内部・独立再現なしを明記。as-of source binding は memento served、publication ではない。
- **D071 concepts（u2 served 2026-09-21T04:13:55Z、wire gzip 49007B CDX `TUIO…` MATCH、decoded 307198B `35770834…`）**: Choice/Score/Noul＋probabilities/confidence＋parallel via state＋typed map、`POST /v1/systemone`、`model: jev-latest` default、**group-level calibration、per-answer 保証なし（verbatim first-party caveat）**、text-only、decomposition＋confidence-gated escalation を vendor 報告として SELECTED SUPPORTING。**255-cardinality/score-then-choose は archive 可視 text に不在のため as-of に使わない（current-only）**。API 詳細は D142 に属し本頁で主張しない。
- **D141 models（u3 served 2026-09-20T20:50:53Z via 302 from requested `21091419`、plain 350662B、CDX served `ABQR…` MATCH/requested `E2BR…` NO-MATCH）**: jev-1.13.0-only（8 hits）、$42/BTok input-only＋free outputs、250k tok/s＋1200 req/min、64k（32k state＋longest）、text-only、**both aliases→1.13.0（“no preview build right now”）**、alias-drift 警告＋response `model` field、no per-account tuning（shared RLCD weights）、English-primary/CJK weaker、enterprise ZDR を vendor 報告として SELECTED SUPPORTING。**1.13.0 歴史 valid、Nov 1.14 drift は post-cutoff で衝突なし（back-project しない）**。table 値は platform rate limits であり measured throughput ではない。
- **D142 API（unfetched）**: `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` token＋summary-scope `API body uninspected, not global proof` の **INFERENCE lead**に留める。schema fields・confidence-derivation math・version/date/body 消費は主張しない。PARTIAL MATERIAL＋HOLD ceiling＋UNRESOLVED×2 が honest 上限。u2 concepts は schema を含まず D142 を close しない。
- vLLM＋Dynamo（D004/D163）＋継承 D040/D049/D063/D153 は **current-only deployment**として HOLD。as-of proof にならない。DSpark は **V41 §2.4.3＋HF README dba1be0 の architecture  Bounds**からのみ主張し、deployment で裏打ちしない。D040/D049/D063/D153 の recipe/docs は living documentation であり、per-topology precision matrix・dispatch code audit・version pin は outstanding。

## 3. 個別 lane の honest 扱い

- **D143 Engram PRIMARY（p4）**: Cheng et al. 2026 body-consumed allocation law＋delta table（MMLU＋3.4/CMMLU＋4.0/MMLU-Pro＋1.8/BBH＋5.0/ARC-C＋3.7/DROP＋3.3/HumanEval＋3.0/MATH＋2.4/GSM8K＋2.2＋U-law/LogitLens）＋official repo release-level を根拠に PRIMARY。O13（sparsity-axis、MoE 補完）を測定核として担う。static-lookup fusion・allocation-curve 詳細 outstanding、Qwen-PLE 並列未解決、kNN-LM/RETRO は HOLD 境界 precedent のまま。O01/O03/O08/O09/O12 は cross-mapped measured anchors（V41/Qwen/Kimi/FrugalGPT/GenAI-Perf）で正当化し、PRIMARY-every-obligation はしない。
- **D119 GenAI-Perf docs SELECTED SUPPORTING（p9）**: Triton tooling docs を `perf_analyzer` semantics として利用可。AIPerf standalone open とは別 claim。repo 未 clone、metric semantics は docs 止まり、AIPerf product identity は open のまま LIMITATION。O12 background 内で taxonomy/methodology を担い、新 benchmark 数値は主張しない。
- **D162 HOLD**: Accepted X reception ledger r3（27 observations/24 accounts/20 independent）は **social lead**であり technical fact ではない。per-observation verification なし、technical/economic/license fact を sourced しない。HOLD ceiling、配置なし。
- **D165 PRIMARY（p6）**: llama.cpp Qwen port PR27742 existence＋PR-reported numbers のみ。correctness/rebuild は主張しない。O06/O07 を担うが、host PLE memory（97.7GiB table等）は implementation-described のまま。
- **D030 README dba1be0・D032 launch PRIMARY（p9）**: README は dba1be0 pin でのみ CONFIRMED、current drift は UNCONFIRMED。per-figure/version pins outstanding。GLM は abstract-only、MiniMax/gpt-oss は watch、harness/scaffold pins outstanding。

## 4. 15 obligations mapping（2 SAT/13 LIM、自動 SAT なし）

- O01 SATISFIED（bottleneck 共通言語、Kaplan/Chinchilla/Orca＋Dynamo 2026 instance、body-level tables outstanding でも構造 gap なし）、O07 SATISFIED（GGUF format 明示、llama.cpp/KTransformers/offload、D165 existence）。他 13 は LIMITATION。
- O02（scaling）・O03（MoE）・O04（attention）・O05（decoding）・O06（precision）・O08（serving）・O09（distill）・O10（Jev vendor quarantine）・O11（capstones）・O12（methodology）・O13（Engram）・O14（TTC）・O15（routing）は、それぞれ p1–p9 に must_cover として割付け、measured-effect は PRIMARY が担い、genealogy/background は SUPPORTING が担う。source-backed の境界 rationale のみ改善し、source class を真実化しない。

## 5. Reader budget（履歴 66＋arbitrary ではなく claim utility/pages 算術）

- prior 63 target/85 max＋付録A 6 は selected policy ではない。HOLD 30 を配置に入れず、out-of-cutoff mechanisms を appendix で smuggle しない。current-only inventory は review dossier に留め publication にしない。
- **target 60pp / max 75pp**：14 PRIMARY measured-effect に quarantine＋figures で約1pp each（14pp）、116 SUPPORTING background/conditions に平均約0.3pp each（約35pp）、thesis/intro/methodology overhead（約11pp）の合計 60pp を target とし、layout/figures slack で max 75pp。内訳は p1 3pp＋p2 5pp＋p3 4pp＋p4 10pp＋p5 9pp＋p6 6pp＋p7 5pp＋p8 4pp＋p9 9pp＝55pp 実質＋overhead 5pp＝60pp。HOLD は 0pp。66 などの履歴数字は使わない。
- 9 packages は quota ではなく coherent 選択：major lane（bottleneck/scaling/MoE/attention/decoding/precision/serving）＋mandatory Jev＋capstones/measurement の 9 が、15 obligations（O01–O15 を O02+O09、O04+O13、O05+O14、O06+O07、O08+O15、O11+O12 の 6 組＋残り 3 単独で束ねる）に過不足なく対応する最小 coherent 分割である。empty-synthesis は 0（at most 1・last・factual prior の条件を空振りさせない）。package IDs は token-safe（`p1-bottleneck` 等、英小文字＋hyphen）。
- PRIMARY は正確に1配置、SUPPORTING は1以上配置、継承 boundaries を保持する（runner が union する）。HOLD は配置も exception もなし（全 SELECTED を配置するため selected_exceptions は空）。

## 6. 不足・gap（PASS ではなく返却）

- D142 API body 未取得、RLCD 内部・benchmark/calibration methodology・独立再現なし、unserved u3 `21091419` revision・pre-09-20 revisions 未取得、D141 card-vs-current alias contradiction の accepted 側訂正は root/normal-producer 業務（本 DATA は訂正 scope 提示のみ）、vLLM/Dynamo の pinned-09-20 historical proof なし、per-figure pins（V41 Appx B/C、Qwen ablations、Kimi tables、routing/TTC、harness/scaffold）outstanding、AIPerf standalone surface 未消費、MiniMax/gpt-oss mechanism 未確認。これらは indispensable unsupported claims/gaps として残し、PASS とはしない。
- 本 DATA は durable packet-local DATA であり、accepted research の編集・State/guard/Selection 遷移・承認・Draft/PDF を含まない。actual canonical 生成は後続 root＋独立 review が `run_selection_architecture_v2_interactive` で行う。

*counts：160 assignments（SELECTED 130＝PRIMARY 14＋SUPPORTING 116、HOLD 30）＋5 nonmatrix EXCLUDED＝165 ledger；pins・gaps は `sp-selection-per-did-map.json`、`sp-selection-read-scope.json` を参照。*
