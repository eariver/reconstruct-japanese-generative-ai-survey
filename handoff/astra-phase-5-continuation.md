# J-GAS — Phase 5 continuation

日付: 2026-09-14 JST
状態: **PHASE 5 ACTIVE / PUBLICATION REVIEW CASE TRACED / 5-B COMPLETE / NO 5-C TRIAL / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [publication review境界の判断](../outputs/astra-phase-5-publication-review-boundary-decision.md) §1・§4–6。
3. 必要時のみ[今回Evidence](../notes/phase-5-review-boundary/evidence.md)。5-Bの判断は[5-B評価](../outputs/astra-phase-5b-work-observation-assessment.md)に保持。Phase 4の復元は[5-A判断](../outputs/astra-phase-5a-work-unit-decision.md) §2で足りる。全chat/旧lab再読・再実行は不要。

今回の開始時Push済みreconstruct local/remote mainは`4504d4c1c52d9fcda75e20803b72d470c67a74be`で一致・clean。5-Bはこの基準へ取り込まれた。今回のpublication review境界調査はHumanのcommit/Push対象であり、commit済みとは扱わない。次sessionではその時のPush済み状態を確認する。

全体目的: publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準以上に保ち、production・supervision/review/reasoning・repair/regeneration・CI/runtime・LLM・complexity・Human handoff/manual burdenを含むtotal lifecycle workを最小化する。移転は削減ではない。初期投資/移行/歴史互換/二重保守込みで判断する。

## 2. 5-Bで判断可能になったこと

**一つの問いの研究→本文→source-first非著者review→root修復→一度の再reviewを完了。除ける意味再構成の具体的支持例は得られず、5-CのA/B比較は開始しない。** 新architecture B、Task統合、新意味層は選定していない。

2025-04-28〜05-05未満UTCのWeekly窓で、Mem0 v1を主題、A-MEM v5をcutoff前の背景、MemOS v1をcutoff後の強い関連HOLDに固定。出力前protocol、取得raw/版/hash、r1/r2、独立期待内容とreview、作業観測を保存した。A-MEM v1は準備履歴のみ。full Weekly Discoveryやblind sampleではない。

初稿はblocking一件（評価規模・Jの判定条件等の読者説明不足）、補足三件（版別著者順、graph版の逆転、日本語/負担比較の向き）。facts→composition→本文を修復し、独立再reviewで全件解消・追加findingなし。[r2本文](../notes/phase-5b/r2/manuscript.md)はこのsliceの結果であり、全号publication quality認定ではない。judgeのexact版、A-MEM引用表と原表のカテゴリ対応、再実行設定/集合の同一性等は未解決として直接順位付けを保留した。

新しい意味層なしで必要な横断比較と根拠の引継ぎができた限定例だが、それでも独立review/repairが必要だった。source固有の初回検証、事実から採否/読者説明への変換、独立review、誤り修復、自動コピーを「同一作業の削減」に数えない。current Coreの1 Discovery/Taskと保存数は認知仕事数ではなく、既存runnerのbatch著述入力とgovernanceのgrouping/適応研究をBの新機能にしない。

**非支持と識別不能を分ける。** W06/W08のraw再訪理由は合理的だが、各時点の既存結論の完成度・再確認の内訳・除去可能量は識別不能。role別active time/token/料金もunknown。反復ゼロの実測でも全productionでの不存在証明でもない。5-Aの「仮説棄却」は今回の比較投資停止として適用し、一般仮説の否定へ強めない。単一rootが研究/編集/本文を続ける観測であり、実運用の別session/roleへのhandoff損失を十分に励起したかも不明。

## 3. 今回の判断と次の入口

5-Bの次入口を、W34 Human Preview r2の一件で確認した。**問題のTeX/bibはreview対象manuscriptに正しくbindされ、semanticは内部用語なし、visualはclaim boundariesを含むexact PDF確認を宣言していたが、Humanが同じ版から問題を発見した。** 新しいcheck IDや対象ファイルを足すだけでは解けない実例である。

二原因を分離した。claim boundary末尾の内部編集理由は読者向け節範囲へ正規化する編集判断が必要だった。41件のaccess日はgeneratorがcutoffを流用した機械処理の誤りで、PR #492により修復済み。現W34のTeXは一置換で修復され他の限界は保持、bibは41日付以外不変。通常PDF rebuildと旧Draftからの再著述を混同しない。

governanceは独立したsupervisory editorial/semantic/visual責務を既に持つ。旧manifest/semantic/visualと実行worklogは同じ実行側名義で、調べた記録ではexact版の独立supervisory消費を実証できなかった。他の場所/会話にreviewが無かったとまでは言わない。reviewの実読解量、見逃しの内部認知原因、全role費用はunknown。

**改善候補は既存publication reviewの主たる意味判断を完成した読者向けsource一式へ揃え、最初の高コストbuild/Candidateより前に置けるか。** 最終exact PDF/全体review責務とHuman Gateは残す。既存manifest/detail/evidence_locationsを使い、新store/追加reviewer/恒久coverage ledger/full rendererを既定解にしない。前倒しだけは仕事の移転であり、回避できる追加build/再記録/Human再確認より追加確認・同期・保守費が小さいかを判断する。旧r2は二原因を同時修復したため、片方の早期検出だけで全周回が消えたとは言えない。#492後のbaselineに過去と同じ発生率も仮定しない。

今回の一件調査はこの判断面で完了。**次に進めるなら、既存の誰が・何を入力に・いつ独立消費するかを示す一回分の実行計画を具体化する。** 既に同じ適切なreviewがあるなら追加案を捨て、見逃し/残存頻度を再評価。共通Core、同等品質、exact binding、全role費を観測できる条件が揃った時だけ新たな比較実行を選ぶ。既知r2を見つけ直す自己試験は不可。条件がなければ保守候補に留め全体優先順位を再評価する。[現在判断§4–6](../outputs/astra-phase-5-publication-review-boundary-decision.md)参照。

5-Bの旧仮説/条件付き5-Cは引き続き非開始。同じ小記事を増やしてBを探さない。再開条件は、固定比較結論がhandoff先で利用できず同じsubject/source版/条件を再研究した名指せる実例、または全role差を識別できる環境。今回のpublication repairはその支持例ではない。4-C/5-Bの一体review許可は完了。今回追加agentなし。

## 4. Last observed production realityと保留

[今回GET観測](../notes/phase-5-review-boundary/observation.json): main `74708eb26a357ec11a839a59de62ab62cd246eef`、W34 `6be0f462d8f02284f8513d7165c778c3797dcaf4`。Human r2 REQUEST_CHANGES→PR #492統合/edition修復→fresh publication→**canonical Human Preview APPROVE r3**。現在`RELEASE_CANDIDATE`、`next_action: stage:freeze`、Freeze/Release pending。5-B時のPreview pending/nullを現在へ流用しない。

現Candidate raw SHA `df376f474acf5fafa14f9af5196727858b1dd76f5c7d17664fa52ba784e32061`とpayload digest `52c8d0bcc85140a2727d1867a908d7077d40c7088a7c1e83f10b66044c50f3ba`は別。PDF raw `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`。旧値は歴史値。

r3はreviewed commit `f9f3e040…`、そのpre-approval Stateをbindし、現在のCandidate/PDF bytesにも一致。State→approval/checkpoint、immutable approvalとr3の局所bindingを[check](../notes/phase-5-review-boundary/check.json)で確認。全State validation・依存閉包・PDF目視/全号品質reviewは再実施していない。Human承認を尊重し、追加承認要求/取消/freezeはしない。

#492はWeekly cutoff/Special as_ofの一律urldateをcanonical accessへ変更。sourceの未確定/曖昧性を推測で埋めない。main diffはbibliography修復でeditorial review責務/Task単位は不変。W34のEvidence/Selection/Architecture/canonical Draft pathsは今回diffで不変。修復を全source意味/引用反例の解消へ広げない。PR #488/#489/#490/#492は既存baseline保守でreconstruct成果ではない。Issue本文/コメントは今回不要で未取得。観測refが今後も最新とは仮定しない。

Phase 4はclosed。4-Hはsection出力前にlab URL集約guardで停止しrepair未実行。production schema違反/source矛盾/publication成功ではない。historical Packageとlab修正Cardは別。renderer/citation/source-identity、acceptance/staging/cache、新store/恒久telemetryは保留。#492の存在だけでそれらの再開や普遍的source identity完成を意味しない。

## 5. 未実証と権限

実仕事差/純削減、full canonical baseline、全号品質、未知source omission、Weekly/Special全体一般性、歴史/caller互換、PDF/visual、全role費用とROIは未実証。labで省いたproduction必須工程をゼロ費用にしない。Humanを無償reviewer/計測係にしない。今回の記録/取得/独立review/repair/引継ぎと委任確認・usage中断後の再開も観測費から外さない。

productionは明示Human authorizationなしにread-only。State/Gates/承認/Freeze/Release/adoption/migration/PR/Issueを変更しない。外部送信/追加委任なし。通常Git Pull/Push/最終commitはHuman。歴史判断を上書きせず、この入口から必要な範囲だけ継続する。
