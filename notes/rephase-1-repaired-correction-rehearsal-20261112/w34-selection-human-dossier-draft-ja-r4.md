# W34 人間向け Selection/Architecture ドラフト r4（案・未承認） — 2026-W34 週次誌

**位置づけ:** 著者 DATA r4。v1/r2/r3 を保存し、上書きしない。独立指摘 F1–F5 と r2 CHANGES_REQUIRED・counterfactual 4 紙を反映し、R2 accepted 訂正後の 45（41 vendor＋4 research）を provisional で用意した。**独立 semantic review を経る前の正準 writer 実行はしない。** Architecture 承認・Human Gate・Draft/PDF・R4 は未了。38V/363P/8N・45M/354C/10H 等は既存ラベルであり新規 PASS ではない。著者のみ、Human 承認なし。

## 現状（active PREARCH のみ）

- Runtime: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` HEAD `ae0dd1e`（parent cc1c）。State `EVIDENCE_REVIEWED`、active PREARCH `73ab28ea` R2 の 4 refs のみ（Evidence `eef77479` 409・Views `3727485a` 409・Ledger `066230f4` 439・Completeness `d869027a` LIMITED）。旧 canonical Ledger `f089cc4e` 41M は inactive、現 versioned 45M が active。旧 refs を使わない。
- Matrix 409（Evidence/View 結合で 1 Discovery＝1 row、409 exact once）。Ledger 439＝Matrix 409＋nonMatrix 30（26 EXCLUDED＋4 DUPLICATE、0 tasks、割当不可）。Completeness 3 obligations LIMITED。
- Root/effective: 399 eligible、10 HOLD ineligible（8 NEEDS_MORE/HOLD＋2 PARTIAL/HOLD: c033/c035/c038/c051/c053/c054/c057/c065/c097/c103）。SELECTED は MATERIAL＋VERIFIED/PARTIAL のみ。
- 405 unchanged は `15e87eef` と byte-identical、4 枚のみ CONTEXT→MATERIAL＋bounded claims 差し替え。task_target names/set exact。手で全 source 再構築しない。

## r4 で選ぶ 45（41 vendor＋4 research、15 target/16 max）

**Thesis:** W34 は配布と統治の週。新奇モデルより、使える場所・値段・支払い・協働・安全条件が動いた。41 の VERIFIED 一次デルタを 5 package の PRIMARY として据え、4 紙を bounded Research-Notes 1 箱の SUPPORTING に留める。VERIFIED core を置き換えない、表題化しない、再現・配備を主張しない。

- P1 配布・価格 3pp（計12: PRIMARY 7＋SUPPORTING 5）: c017 Sol promo / c023 Grok Bedrock / c030 GPT-5.6 / c040 DeepSeek 改定＋c018 Imagen移行＋kimi-k3/wan-prime＋c022/c039/c045/c066 日付限定囲み＋**16096 Commercial-tax SUPPORTING 買い手注意**（NV-Embed-v2 CC-BY-NC、13 embedder/8 maker、floor・費用・checklist §§3-4/§§4-5、AUTHOR_CLAIM、配備なし）。P1 の値段・SOTA・throughput を修飾する欄外。
- P2 エージェント基盤GA 4pp（計13: PRIMARY 8＋SUPPORTING 5）: c010 Payments / c011 Computer Use / c012 Slack Code / c007 Alipay＋c019 Agentic Search / c031 Dogwood / c047 Runway / memory JSON（P2 単一、P1 重複なし）＋c087/c104/c105 1囲み＋**15127 Agentic workload SUPPORTING 機構**（10 apps＋計測、tool/state/I-O、非LLMボトルネック、pay-go内訳、AUTHOR_CLAIM）＋**18389 Jagged frontier SUPPORTING 堅牢注意**（SPT変換で最大6.7pp低下、6/16有意、単一P2配置、ベンダーGAへのcounterweight）。P2 pay-and-collaborate を裏付ける機構欄。
- P3 企業面 2pp（計8: PRIMARY 2＋SUPPORTING 6）: c052 History拡大＋c096 Messages（範囲限定）＋c099-101 Copilot 3点 Sep8限定1囲み＋c102 Antigravity 単一SUPPORTING（束と追加を分離せず、dual-roleなし）＋Kimi CLI/Replit。変更なし。
- P4 安全・統治 3pp（計8: PRIMARY 4＋SUPPORTING 4）: c005 Astra / c008 ZDR / c004 Teens / c006 KEV＋c002 watermark / c055 CoSnitch研究者限定 / Defenders随想＋**21100 ReFrame SUPPORTING 安全機構**（Evidence生成＋Rewrite-Routing＋Safe Inference、37.28→45.95、AUTHOR_CLAIM、closed-source適用は記述のみ）。P4 条件部の機構メモ。
- P5 infra・経済・創作 2pp（計4: PRIMARY 3＋SUPPORTING 1）: c026 PORTS-Pike / c003 Stripe / c091 Firefly＋c020 Pika日付限定。変更なし。
- 合計 P1 3＋P2 4＋P3 2＋P4 3＋P5 2＝14 base（P3 trio統合で締め）＋Research-Notes 1箱（P1 0.5＋P2/P4 0.5、単一箱・最終順）＝15 target、overflow見込みで max 16。自動17ppではない。限定11＋新規4はいずれも表題化しない。
- CORE roles: PRIMARY は `WEEKLY_MAGAZINE:primary-story-anchor`＋`WEEKLY:<package>`、SUPPORTING は `WEEKLY_MAGAZINE:supporting-evidence`＋`WEEKLY:<package>`。PRIMARY は exactly 1 package、SUPPORTING は ≥1（本案では監査明確化のため各1）。Memory二重・c102二重なし。Weekly downstream `section_label`（各package）＋`closing_summary required/heading/after_body_before_references`＋`weekly_closing_summary required/source profile_synthesis.current_interpretation` は実導出 func の exact shape、invent なし。Manuscript/Draft 著述なし。

## 負の空間（364 HOLD＋30 nonMatrix、機械的 HOLD ではない）

- HOLD 364: 10 ineligible HOLD（NEEDS_MORE 8＋PARTIAL/HOLD 2、上記リスト、HOLD/NONE、昇格には upstream Evidence 改訂が要る）＋354 CONTEXT HOLD。319 arxiv は全点 triage（lane・score・日付・抄録・cluster CL-A/B/C/D/E/F/G/H）＋26 体本文読み（14927/14967/15004/15127/16096 他 KEEP 21＋refresh、112KB–1.5MB、節・text_len・SHA 確認）の上で、手法知見としては確認したが週イベント昇格なしと落とす。残り ~293 は hash-only、PASS 主張なし。39 非arxiv も各点理由（GLM旗艦日付、Mythos両用、DSpark速度、UI-Mate出所、Build対応、AutoDesign分割等）。一律「未読ゆえ除外」に戻さない。先行 review の negatives を再利用。
- 21095 Trustworthy RAG は P4 適性あるが箱余白なしで明示 HOLD（14927 routing否定・14967 WAN解析は背景として考慮済み HOLD）。
- nonMatrix 30 separate: カバレッジAPI 5 routine noise、重複4（c042→c023/c024、c067→c025背景＋c066限定、c069→c031、c070→c029、いずれも no-loss 継承）、carry-over C076/C077（8/13・8/03 週外をここで明示処分、RECHECKED_UNRESOLVED、promotion/backfill なし）、他19 週外・重複・定常ノイズ。いずれも task なし、割当不可。carry-over 処分は dossier 外部、assignment IDs ではない。
- 圧縮 counterfactual: 319 全消費でも 6th 技術 package（retrieval/agents/eval）は補足箱にはなり得るが現 core を置き換えない。Sparse 1-package は VERIFIED デルタ（c017/c023/c030/c040/c005/c008 等）を無視するため棄却。

## 残る問い（Human が躊躇すべき点）

- 限定 SUPPORTING（日付・Sep8・研究者限定）＋新規4 AUTHOR_CLAIM を囲みに留める判断は妥当か、落とすべきか。
- Copilot 3点・Antigravity を snapshot として載せる範囲は妥当か。
- CoSnitch を研究者報告として載せるか。
- 21095 を次に足すか、HOLD のままか。
- 15/16pp（P3 2締め＋1箱）は妥当か、さらに締めるか。

## 次に必要なもの・残る essential gaps

- 独立 semantic review（本 input＋per-DID map＋pins＋dossier）を経てから正準 writer。writer は Discovery→`candidate:<issue>:sha256(task)[:16]` を解決し、Matrix→Selection→Architecture→Summary→Attention＋input/audit の順に no-overwrite で書く。失敗時は全残しで止め、retry/cleanup なし。Draft/PDF なし。
- 不足一次（MSRC/NVD、Aug14/21 時刻、Copilot 当日 bytes、一覧 bytes）は現限定表示には不要。確定見出し化を求める場合のみ Root に具体 scope で返す。現 cost は proof/prepare の public preflight 等の実測のみで、lifecycle 全削減は UNKNOWN、zero-cost 主張なし。
- 旧 canonical f089・LEGACY refs・旧 overlay を重ねない。新規 fetch・source 修理・State rollback・REQUEST_CHANGES 捏造・LOW/手動迂回なし。

*ピン・範囲は `w34-selection-read-scope-and-pins.json`、全 DID は `w34-selection-per-did-map.json`、入力は `w34-selection-architecture-input.json`。型は現 ae0dd1e・73ab R2 のみ。*
