# J-GAS — Phase 5 continuation

日付: 2026-09-13 JST  
状態: **PHASE 5 ACTIVE / 5-B BOUNDED CHAIN COMPLETE AFTER REPAIR / NO 5-C TRIAL / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [5-B判断](../outputs/astra-phase-5b-work-observation-assessment.md) §1・§5–8。
3. 必要時のみ[5-B Evidence index](../notes/phase-5b/README.md)。5-Aの経緯は[5-A判断](../outputs/astra-phase-5a-work-unit-decision.md)、Phase 4の復元はその§2で足りる。全chat/旧lab再読・再実行は不要。

5-B開始時のPush済みreconstruct local/remote mainは`cc530fea883a66049b8ab4a9ea3f112da34c4fab`で一致・clean。今回の5-B変更はHumanのcommit/Push対象であり、commit済みとは扱わない。次sessionではその時のPush済み状態を確認する。

全体目的: publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準以上に保ち、production・supervision/review/reasoning・repair/regeneration・CI/runtime・LLM・complexity・Human handoff/manual burdenを含むtotal lifecycle workを最小化する。移転は削減ではない。初期投資/移行/歴史互換/二重保守込みで判断する。

## 2. 5-Bで判断可能になったこと

**一つの問いの研究→本文→source-first非著者review→root修復→一度の再reviewを完了。除ける意味再構成の具体的支持例は得られず、5-CのA/B比較は開始しない。** 新architecture B、Task統合、新意味層は選定していない。

2025-04-28〜05-05未満UTCのWeekly窓で、Mem0 v1を主題、A-MEM v5をcutoff前の背景、MemOS v1をcutoff後の強い関連HOLDに固定。出力前protocol、取得raw/版/hash、r1/r2、独立期待内容とreview、作業観測を保存した。A-MEM v1は準備履歴のみ。full Weekly Discoveryやblind sampleではない。

初稿はblocking一件（評価規模・Jの判定条件等の読者説明不足）、補足三件（版別著者順、graph版の逆転、日本語/負担比較の向き）。facts→composition→本文を修復し、独立再reviewで全件解消・追加findingなし。[r2本文](../notes/phase-5b/r2/manuscript.md)はこのsliceの結果であり、全号publication quality認定ではない。judgeのexact版、A-MEM引用表と原表のカテゴリ対応、再実行設定/集合の同一性等は未解決として直接順位付けを保留した。

新しい意味層なしで必要な横断比較と根拠の引継ぎができた限定例だが、それでも独立review/repairが必要だった。source固有の初回検証、事実から採否/読者説明への変換、独立review、誤り修復、自動コピーを「同一作業の削減」に数えない。current Coreの1 Discovery/Taskと保存数は認知仕事数ではなく、既存runnerのbatch著述入力とgovernanceのgrouping/適応研究をBの新機能にしない。

**非支持と識別不能を分ける。** W06/W08のraw再訪理由は合理的だが、各時点の既存結論の完成度・再確認の内訳・除去可能量は識別不能。role別active time/token/料金もunknown。反復ゼロの実測でも全productionでの不存在証明でもない。5-Aの「仮説棄却」は今回の比較投資停止として適用し、一般仮説の否定へ強めない。単一rootが研究/編集/本文を続ける観測であり、実運用の別session/roleへのhandoff損失を十分に励起したかも不明。

## 3. 次の具体的入口と停止条件

**同じ小記事自己観測を増やして5-Cを探さない。** この仮説を再開する条件は、実運用で正しく固定された比較結論がhandoff先で利用できず同じsubject/source版/条件を再調査したと名指せる例、または準備/保持/独立review費込みの差を識別できる実行環境。複数ファイル/別role/再訪だけでは足りない。恒久telemetryを埋め合わせに作らない。

全体再構築はこの仮説待ちに固定しない。**次の優先順位判断の入口は、読者原稿の完了判定と実際のreview範囲がHuman修復負担をどこで防げていないかの限定確認。** 今回B1/N3とW34用語修復が候補信号。既存editorial reviewがあるため、reviewer/意味欄/renderer追加を既定解にしない。一つの実publication修復について、誰がどの版/公開要素を既に読んだか、欠けた判断、追加確認費を特定し、除去/前倒し/共通化可能な実仕事差があるかで止める。全W34再監査や小記事との擬似費用比較へ広げない。新trial/実装は未選定。[5-B判断§8](../outputs/astra-phase-5b-work-observation-assessment.md#8-次の入口と権限)が詳細。

5-Bは外部blockedや新Human Gate待ちではなく、支持する判断面で完了。今回許可された一体の非著者reviewerは事前評価・初稿review・一度の再reviewまで完了。旧4-Cと今回の許可は将来の一般的委任に使わない。

## 4. Last observed production realityと保留

[5-B GET観測](../notes/phase-5b/observation.json): main `79a0ddea948af18ef02ec63184e67f99ad7f8e09`、W34 `c7faf207515e7429dd74abd5adaf2962725587ef`。mainのPR #490はHuman revisionによるvalidation無効化時にactive revalidation pointerを解除する修復で、研究/編集Task単位は不変。

W34は旧`5561e232…`へのHuman Preview REQUEST_CHANGES、修復Core統合、正式なDRAFT_COMPLETEでの用語修正、fresh publication生成を経た。**新RELEASE_CANDIDATE / PUBLICATION_PREVIEW pending**、Human Preview provenance null、Freeze/Release pending、active revalidation pointer null。旧Human判断は新exact bytesの承認ではない。

現Candidate payload digest `d0af4c9ca917ce3a51d58fcd213846c4d49cb8d3a9334501484ec798970de429`とraw SHA `6d18b4962ad51bfa974fd4d814a61a070dcab36a0bff8499d11d5821c28dff7a`は別。rawを取得・再hashした。旧`dbd4c783…`/`c45adaf7…`は歴史値。[差分Evidence](../notes/phase-5b/production-change.json)参照。

reader/品質bundle/review/PDF/checkpoints等は更新。Evidence/Selection/Architecture/canonical Draft pathsは今回diffで不変。用語修復を既知source意味/引用反例の解消としない。full State validation・全binding閉包・PDF/全号品質reviewは再実施していない。残Issueはこの判断に不要で未読。PR #488/#489/#490は既存baseline保守でreconstruct成果ではない。Card/Draft修復をpublication-only rebindへ押し込まない。観測refが今後も最新とは仮定しない。

Phase 4はclosed。4-Hはsection出力前にlab URL集約guardで停止しrepair未実行。production schema違反/source矛盾/publication成功ではない。historical Packageとlab修正Cardは別。renderer/citation/source-identity、acceptance/staging/cache、新store/恒久telemetryは保留。正規採用接続や実反復負担の新Evidenceが出た時に再評価する。

## 5. 未実証と権限

実仕事差/純削減、full canonical baseline、全号品質、未知source omission、Weekly/Special全体一般性、歴史/caller互換、PDF/visual、全role費用とROIは未実証。labで省いたproduction必須工程をゼロ費用にしない。Humanを無償reviewer/計測係にしない。今回の記録/取得/独立review/repair/引継ぎと委任確認・usage中断後の再開も観測費から外さない。

productionは明示Human authorizationなしにread-only。State/Gates/承認/Freeze/Release/adoption/migration/PR/Issueを変更しない。外部送信/追加委任なし。通常Git Pull/Push/最終commitはHuman。歴史判断を上書きせず、この入口から必要な範囲だけ継続する。
