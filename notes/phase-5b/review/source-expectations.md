# Phase 5-B source-first expectations — 非著者事前評価

状態: 初稿を読む前の期待内容。本文の代筆でも採用承認でもない。対象は protocol r1 の一つの問いと三つの固定版。rootの著述物・旧labの回答・rootのreading.txtは読んでいない。保存raw HTMLからsection、表見出し、セル、脚注を確認した。独立した論文読解であり、実験の独立再現ではない。

## 1. 問い・時点・最低限の読者coverage

Mem0の報告から、長期会話における品質と質問応答時の処理負担のトレードオフを説明し、他方式との比較・導入に必要な条件を残す。方式の紹介だけ、最高値だけ、コスト削減の宣伝だけでは不足。日本語読者が「何を保持し、何を検索し、何を測り、どこまで言えるか」を追えることが必要。

- Mem0 2504.19413v1: 2025-04-28 01:46:35 UTC公開。仮Weekly窓内の主題候補。著者はPrateek Chhikaraほか。研究チームによる報告と帰属させる。
- A-MEM 2502.12110v5: v1は2025-02-17、v5は2025-04-18 17:26:57 UTC。cutoff以前の背景比較として有効。今週の新発表にはしない。著者はWujiang Xuほか。v1を弱い代用対照に使わない。
- MemOS 2507.03724v1: 2025-07-04 17:21:46 UTC。著者はZhiyu Liほか。後日の強い候補として検査したが、当時のWeekly本文の根拠にはできない。除外理由は時点であり、性能が低い・実験がない・無関係だからではない。後日の観測注記を置く場合も当時の記事とは明確に切り分ける。

この三候補はbounded slice。全Weekly Discoveryのcoverageや、未選定方式すべてへの優位を証明しない。Mem0採用とA-MEM背景利用、MemOS時点除外は支持できる編集案だが、数値の比較条件に疑義が残る部分をHOLDにする余地は残す。論文全体のDROPと個別主張の保留を混同しない。

## 2. Mem0 v1に必要な内容と強い反例

根拠: raw `mem0-2504.19413v1-html.html` §2–5、Table 1 (`S3.T1`)、Table 2 (`S4.T2`)、Appendix A/C。数値はこの論文内の報告である。

**機構。** メッセージ対と、会話要約・直近メッセージから重要な事実を抽出。既存の類似記憶と比較してADD/UPDATE/DELETE/NOOPを選ぶ。実験の直近メッセージ数と比較対象記憶数は各10、LLM処理にGPT-4o-mini。Mem0の自然言語記憶と、実体・関係を加えるMem0gを区別する。後者はNeo4jを利用し、関係の競合時には無効化を用いて履歴を残すと説明する。構造化を施せば正確性やprovenanceが保証されるとはしない。

**評価条件。** LOCOMOの10会話、平均約26,000 tokens、会話当たり平均約200問と論文は説明。single-hop、multi-hop、temporal、open-domainの4種。回答不能を問うadversarialを除外しているので、回答を控える能力やfail-closeの実証にしない。F1/BLEU-1は語の重なりを中心とする指標。Jは別のより強いLLMによる判定として説明され、Appendix Aではgold answerと同じ話題・時点を含めば寛容にCORRECTとする二値promptを掲載している。Jを人による品質保証、厳密な事実検証、全体publication品質としない。§3.2は10回の実行と平均±1標準偏差を報告するが、これは独立機関の10再現ではない。確認したv1本文ではjudgeの具体的モデルIDを確定できない。GPT-4o-miniを推論に用いた記述だけからjudgeも同一・またはGPT-4oだと補わない。

**Table 2で外せない比較。** Mem0 J=66.88±0.15、Mem0g=68.44±0.17、Full-context=72.90±0.19、OpenAI=52.90±0.14。全履歴入力の方がJは高い。Mem0の約26%相対改善はこのOpenAI行との比較で、26 percentage pointsではない。OpenAI行はChatGPTから抽出した記憶を全て応答用contextに渡す著者の評価方法であり、汎用のOpenAIモデル性能やChatGPT実製品全体への優位ではない。§3.3のChatGPTと§4.4のplaygroundという説明差も、独立再現済みの厳密実装と見なさない理由になる。

総応答時間p95はFull-context 17.117秒、Mem0 1.440秒、Mem0g 2.590秒。検索だけのp95はMem0 0.200秒で、1.440秒と混同しない。Table 2の比からMem0は約91.6%低減。abstractの91%、§4.3の92%は丸めで説明できる。平均retrieved memory tokensはMem0 1,764、Mem0g 3,616、Full-context 26,031。Mem0対全履歴は約93.2%少ないが、これは回答contextのtoken量。料金、生成token、構築・更新、非同期要約、運用保守を含む総費用を90%以上削減したとしない。§4.5の保存記憶約7k/14k tokensとも分ける。構築時間とZepの待機に関する記述は著者観測であり、各方式の一般的運用性を確定しない。

**全面優位への反例。** Table 1のopen-domain JはZep 76.60、Mem0g 75.71、Mem0 72.93。Mem0gはMem0よりsingle-hopとmulti-hopのJが低い（65.71対67.13、47.19対51.15）。グラフが多段推論を必ず改善するとは言えない。Table 2ではOpenAI行の応答p95 0.889秒もMem0より短く、LangMemの127 tokensはMem0より小さい。よって「全方法より高品質・最速・最小」は不適切。RAG比較はchunk 128–8192、top-k=1/2の固定chunk検索に限る。best RAG J=60.97をもってRAG一般を否定しない。本文の会話長に依らない性能や指数的負担の主張を、10会話の表から独立に証明したとは扱わない。

## 3. A-MEM v5から得る比較条件とHOLD条件

根拠: raw `a-mem-2502.12110v5-html.html` §3、§4.1–4.3、§6、Appendix B.1/B.4、Table 1 (`S4.T1`)、Table 5 (`A2.T5`)。

方式はZettelkastenに着想を得た記憶ノート。原文、時刻、キーワード、タグ、文脈説明、embedding、他記憶へのlinkを持つ。新記憶と類似記憶の関係をLLMで作り、既存ノートの文脈・属性を更新する。両方式とも抽出と検索をするから同じ、と潰さず、Mem0の記憶操作とA-MEMのlink/evolutionの違いを説明する。LLMに依存する組織化品質とテキスト中心の実装は§6自身の限界。

A-MEMはLOCOMOを平均9k tokens・最大35 sessions・7,512 QAと説明し、adversarialを含む5カテゴリを用いる。Mem0の説明と件数・会話長が違うので、同じ名前だけで完全な同一評価集合としない。主指標はF1/BLEU-1、補助はROUGE、METEOR、SBERT等であり、Mem0のJとの単純順位付けは不可。6 backbones（GPT-4o-mini/4o、Qwen2.5 1.5B/3B、Llama3.2 1B/3B）とall-minilm-l6-v2 embedding。本文の「主にk=10」だけを採用せず、Appendix B.4/Table 5ではGPT-4o-mini/4oはsingle/multi/adversarial=40、temporal/open-domain=50であることを反映する。カテゴリやbackboneごとの調整は比較条件である。

**固定資料間の重大な照合点。** A-MEM Table 1 raw見出しはSingle Hop / Multi Hop / Temporal / Open Domain / Adversial。GPT-4o-mini A-MEM行ではMulti Hop F1/BLEU-1=45.85/36.67、Temporal=12.14/12.00。一方Mem0 Table 1の引用A-Mem行ではMulti-Hop=12.14/12.00、Temporal=45.85/36.67。LoCoMo等の引用行にも同様にカテゴリ対応の違いがある。どちらが正しいカテゴリ割当かをこの読解で勝手に修正せず、原表間の不一致として記録する。カテゴリ別の横断優位や引用baselineに依存した推論は確認まで保留。Mem0著者のA-Mem*再実行行（temperature=0、Jを追加）とA-MEM原報告行は別の結果であり、混ぜない。Table 2のA-Mem J=48.38をA-MEM v5著者自身のJ報告や独立再現としない。

## 4. MemOS v1は強い時点除外候補

根拠: raw `memos-2507.03724v1-html.html` §4、§6.1–6.3、Tables 3–5 (`S6.T3`–`S6.T5`)。

単なる構想だけではない。plaintext・activation・parameter memoryをMemCubeのpayloadとmetadataで管理するOS設計と、LOCOMO、検索、KV再利用の評価を含む。origin/version/アクセス権/lifecycle等の設計を記述するが、全governance制御の実証やreconstructへの適合証明にはしない。

§6.1はGPT-4o-miniを共通backbone、validation performanceで設定選択と説明。Table 3/4ではMemOS-0630のJ=73.31、同表のMem0=64.57、Full-context=71.58。後日の強い結果であり、単にMem0以下だから除外するのではない。ただしMem0原論文のJ=66.88と横断して増分を算出しない。retrieval token量、設定、評価実装の違いがあり、同表内の結果だけが一応の同条件比較である。captionはfive major tasksと述べるが表は4カテゴリとoverallで、5番目の独立taskやadversarialを足して読まない。

**内的反例。** §6.2本文はfull-contextより大幅に低いlatencyと述べるが、Table 4 rawのtotal duration(ms)はMemOS P50/P95=4,942/7,937、Full-context=2,339/7,016である。表に従えば両percentileでMemOSの方が長い。同表のMem0=4,906/5,962に対しても長い。この版から「MemOSが高品質かつ全履歴より高速」と転記するのは不可。

KV注入の§6.3/Table 5は別実験。H800 80GB、HuggingFace transformers、Qwen3-8B/32BとQwen2.5-72B、memoryを事前変換しGPUにcacheした条件でTTFTを測定。Build時間も別記。これをGPT-4o-miniのLOCOMO総応答時間の短縮、cold startを含む総費用削減、一般的な意味同一保証へ変換しない。

## 5. 初稿reviewでの判定基準

少なくとも次が見えることを要求する。表・注記と本文で役割を分けてよいが、重要な留保を読者から見えない研究メモにだけ置かない。

1. Weekly cutoffと三候補の採否・背景/後日役割、固定版とsourceへの追跡可能な参照。
2. Mem0の機構と、J・質問種別・latency・tokenの意味、品質と負担のトレードオフ。
3. Full-context、Zep、Mem0gのカテゴリ差など強い反例。abstractの全面優位をそのまま結論にしない。
4. A-MEMの評価集合・metric・設定の差と、カテゴリ対応不一致への処理。未確定な比較を断定しない。
5. MemOSを読んだ上での時点除外と、後日性能を当時の結論に混ぜない処理。
6. 導入判断では対象会話、回答不能、backbone/judge、設定、構築/更新を含む測定範囲の確認を残す。論文報告をJ-GASのnet savingやadoptionへ飛躍させない。
7. 自然な日本語。「外部メモリ」「記憶の抽出・更新」「質問応答」「検索と応答生成」「95パーセンタイル」等を意味が伝わるよう用い、graph/agentic/LLM judgeの英単語の羅列や逐語訳を完成品質としない。相対%とポイント、保存tokensと検索tokens、初回応答までと総応答時間を区別する。

sourceにない詳細を網羅することや、論文実験を再実行することはこのreviewの合格条件に増設しない。未確定な主張を適切に限定することで読者品質を満たせる。根拠と留保が崩れる主張はblocking、些末な言い換えの好みはblockingにしない。

## 6. 範囲・観測・費用

追加の外部source取得は実施していない。指定集合内に強い性能対照（全履歴、Zep、Mem0gの逆転）と、後日強い候補MemOSがある。未選定全方式を探索したとはしない。Zepの原論文/実装の独立監査は未実施で、Mem0の表内の対照としてのみ評価する。

意味のある再訪: (a) Mem0 Jのモデル同定のため§3.2とAppendix A、およびモデル記述を再確認し、具体IDは未確定に保持。(b) A-MEMのカテゴリ対応をMem0引用表とraw見出し・セルで照合し、不一致による比較HOLD条件を追加。(c) MemOS latencyの本文とraw Table 4を照合し、全面高速化主張を許容しない条件を追加。いずれも独立reviewに必要な検証であり、著者の重複仕事削減に算入しない。

初回tool読解は2026-09-13 10:20 UTC頃から。途中に使用枠復帰を待つ中断があり、freezeまでのwall spanはactive作業時間ではない。抽出のstdout encoding失敗1回と出力切れに対する対象絞り込みを含む補助費も存在する。role別active time、token、金額、operation別費用はunknown。tool runtimeもLLM費用の代理にしない。原HTMLとmetadata照合以外のPDF/visual、コード実行再現、production品質、Human review/approvalは未実施。機械hash一致はsource bindingの確認だけで、論文内容やpublication品質のPASSではない。
