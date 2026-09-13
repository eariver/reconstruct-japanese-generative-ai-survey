# J-GAS — Phase 5 continuation

日付: 2026-09-14 JST
状態: **PHASE 5 ACTIVE / ISOLATED RUNTIME REPAIR CANDIDATE / REGRESSION CLOSEOUT / NO 5-C TRIAL / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [runtime修復候補評価](../outputs/astra-phase-5-runtime-repair-assessment.md) §1・§3–5。patch内容は§2。
3. 必要時のみ[今回Evidence](../notes/phase-5-runtime-repair/README.md)。reader計画は[前回判断§3](../outputs/astra-phase-5-review-plan-and-runtime-priority.md)に完成済み。[前回publication review境界調査](../outputs/astra-phase-5-publication-review-boundary-decision.md)と[5-B評価](../outputs/astra-phase-5b-work-observation-assessment.md)は歴史判断として保持。Phase 4の復元は[5-A判断](../outputs/astra-phase-5a-work-unit-decision.md) §2で足りる。全chat/旧lab再読・再実行は不要。

今回の開始reconstruct local/remote mainは`f5dffe5c3c748a545437b21f1e43a145a041ba4d`で一致・clean。commit title `Astra work Phase 5-C (human commit)`はHumanの明示補足によりphase authorityではない。前回はpublication review boundary investigation、conditional 5-C A/Bは未開始。commit改名/履歴書換はしない。今回変更の通常commit/PushはHumanが行う。

全体目的: publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準以上に保ち、production・supervision/review/reasoning・repair/regeneration・CI/runtime・LLM・complexity・Human handoff/manual burdenを含むtotal lifecycle workを最小化する。移転は削減ではない。初期投資/移行/歴史互換/二重保守込みで判断する。

## 2. 5-Bで判断可能になったこと

**一つの問いの研究→本文→source-first非著者review→root修復→一度の再reviewを完了。除ける意味再構成の具体的支持例は得られず、5-CのA/B比較は開始しない。** 新architecture B、Task統合、新意味層は選定していない。

2025-04-28〜05-05未満UTCのWeekly窓で、Mem0 v1を主題、A-MEM v5をcutoff前の背景、MemOS v1をcutoff後の強い関連HOLDに固定。出力前protocol、取得raw/版/hash、r1/r2、独立期待内容とreview、作業観測を保存した。A-MEM v1は準備履歴のみ。full Weekly Discoveryやblind sampleではない。

初稿はblocking一件（評価規模・Jの判定条件等の読者説明不足）、補足三件（版別著者順、graph版の逆転、日本語/負担比較の向き）。facts→composition→本文を修復し、独立再reviewで全件解消・追加findingなし。[r2本文](../notes/phase-5b/r2/manuscript.md)はこのsliceの結果であり、全号publication quality認定ではない。judgeのexact版、A-MEM引用表と原表のカテゴリ対応、再実行設定/集合の同一性等は未解決として直接順位付けを保留した。

新しい意味層なしで必要な横断比較と根拠の引継ぎができた限定例だが、それでも独立review/repairが必要だった。source固有の初回検証、事実から採否/読者説明への変換、独立review、誤り修復、自動コピーを「同一作業の削減」に数えない。current Coreの1 Discovery/Taskと保存数は認知仕事数ではなく、既存runnerのbatch著述入力とgovernanceのgrouping/適応研究をBの新機能にしない。

**非支持と識別不能を分ける。** W06/W08のraw再訪理由は合理的だが、各時点の既存結論の完成度・再確認の内訳・除去可能量は識別不能。role別active time/token/料金もunknown。反復ゼロの実測でも全productionでの不存在証明でもない。5-Aの「仮説棄却」は今回の比較投資停止として適用し、一般仮説の否定へ強めない。単一rootが研究/編集/本文を続ける観測であり、実運用の別session/roleへのhandoff損失を十分に励起したかも不明。

## 3. 今回の判断と次の入口

**Freeze/Releaseの限定修復候補をreconstruct内で実装した。** Human approvalを専用の型で解決してexact Candidateへ進む、Freeze runtimeのartifact集合をschemaと揃える、FROZENのlocal adoption検証結果をrelease producerから既存CORE_STAGE_CONTRACTとして出す、同一basisのlocal再試行でreport/checkpoint bytesを保持する変更。guard削除/偽PASS/新Human Gate/承認後の新VISUAL/最新Candidate推測/公開Release再作成はしない。

実State/schema/publication/approval/stage/controllerを使う合成Weekly/Thematic/Retrospective fixtureで、未修復baselineの三条件はunexpected visual-review-recordで失敗し、候補は承認→Freeze→Releaseへ進む。drift/別号/別profile/曖昧なpointer/別path・manifest/report basis改変を拒否。active revalidation履歴を保持して承認→Freezeへ進むケースも通過した。上流研究本文・review判断はfixtureであり、実研究・独立QA・全号品質の実証ではない。

関連回帰は[初回結果](../notes/phase-5-runtime-repair/test-results.json)と[Git-aware再確認](../notes/phase-5-runtime-repair/git-aware-results.json)を合わせて読む。初回58件中52件PASS、6件のGit root不足errorsを成功へ上書きしない。Git隔離の不備・対処・fixture objectsの生成も[Evidence](../notes/phase-5-runtime-repair/README.md)に記録。成果のHEAD/index/mainは維持し、通常Pull/Push/最終commitはしていない。

**次は具体的patchの限定reviewとShared Core保守への還元判断。** [現判断§5](../outputs/astra-phase-5-runtime-repair-assessment.md)に従い、current Shared Coreに同修復が入っていれば重複実装せず差分評価する。独立非著者reviewは未実施で、新agentを使う場合はこの具体物について新しい明示許可が必要。4-C/5-B許可を再利用しない。productionへの提案投稿/適用/採用は別の明示Human authorizationが必要。

local retryの実証は「外部成功の固定Release Recordから、State advance前に残ったreport/checkpointを再検証して継続」の範囲。Actions全体の再dispatch、builderの時刻付きimmutable record再利用、main更新後のtarget、RELEASED後の再実行、legacy Action/Handoff経路は未実証/対象外。正当な最終quality/Human工程を省略せず、追加検証/実装/保守費も含む純削減はunknown。

前回のreader review計画はHumanのW35+ pre-TeX carry-forwardに沿って完成済み。計画を作り直さず、W34の受容済みdebtを再修復しない。reader trial・conditional 5-Cは未実行。旧renderer/citation/source-identity、acceptance/staging/cache、新meaning store/telemetryは保留。今回追加agentなし。次turnでpatchや成功済みテスト一式を最初から作り直さない。

## 4. Last observed production realityと保留

前回の[GET観測](../notes/phase-5-review-plan/observation.json): main `3e3eebe0cda3a32ac88ae764d279b37768f6bfca`、W34 branch `3bad8a57cf2b246c7f71cb749ba3105fa318b073`。branchはFROZEN / stage:release、mainはPR #493でfrozen authority統合後、**RELEASED / next null / terminal COMPLETE**。mainをfreeze待ち/Release待ちとしない。今回main refだけfreshに確認して同じSHAだった。W34 branch/State/PDF/公開assetの再取得や全検証はしていない。

Candidate raw SHA `df376f474acf5fafa14f9af5196727858b1dd76f5c7d17664fa52ba784e32061`、payload digest `52c8d0bcc85140a2727d1867a908d7077d40c7088a7c1e83f10b66044c50f3ba`、PDF `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`。Human r3 approved bytesを保持。Freeze record raw `ba5d76d3…`、Release manifest `921803d4…`、Release record `6808dbb0…`。

[局所check](../notes/phase-5-review-plan/check.json)はState/Freeze/Manifest/Release/checkpointとCandidate/approval/PDFを照合。公開Release weekly/2026-W34はnon-draft/non-prerelease、asset338722 bytes、server digestも同じ。公開assetの独立download、全State/依存閉包、source TeX/visual実bytes、PDF目視/全号品質reviewは再実施していない。既存承認/Releaseの取消や再生成はしない。

mainへのmerge compareは112 commits/返却300 files上限のため全差分監査には使わない。必要なreader publication、Weekly publisher、review contract、governanceは旧main74708eb2とbyte-identicalを確認した。旧作業指示を新authorityとして再実行しない。#492の書誌修復と#493のfrozen authority統合/Releaseは既存production成果でreconstructの純削減ではない。既知source意味/引用反例全般の解消は認定しない。

Phase 4はclosed。4-Hはsection出力前のlab URL集約guardで停止しrepair未実行。historical Packageとlab修正Cardは別。renderer/citation/source-identity、acceptance/staging/cache、新meaning store/恒久telemetryは保留。このruntime契約調査はそれらの再開ではない。

## 5. 未実証と権限

実仕事差/純削減、full canonical baseline、全号品質、未知source omission、Weekly/Special全体一般性、歴史/caller互換、PDF/visual、全role費用とROIは未実証。labで省いたproduction必須工程をゼロ費用にしない。Humanを無償reviewer/計測係にしない。今回の記録/取得/独立review/repair/引継ぎと委任確認・usage中断後の再開も観測費から外さない。

productionは明示Human authorizationなしにread-only。State/Gates/承認/Freeze/Release/adoption/migration/PR/Issueを変更しない。外部送信/追加委任なし。通常Git Pull/Push/最終commitはHuman。歴史判断を上書きせず、この入口から必要な範囲だけ継続する。
