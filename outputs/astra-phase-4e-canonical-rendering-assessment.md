# Phase 4-E — canonical Draftから読者出力への互換性反証

初回記録: 2026-09-12 JST / current reality追記: 2026-09-13 JST（§6）

状態: **BOUNDED COMPATIBILITY PROBE COMPLETE / SOURCE JOIN REQUIRES TRACE / NO ADOPTION**

## 1. 結論と方針

**既存canonical欄での境界著述は可能だが、それだけでは根拠を保った掲載経路は成立しない。** Phase 4-Dで特定した不要な内部出力を防ぐ方向は維持する。一方、「reader向けDraftを完成させてrendererへ渡せばよい」から、**canonicalの根拠対応と実際の出力経路を先に確かめる**順序へ修正する。

W34の1 packageを使い、22件の意味境界をsubject別の日本語12 blockへ、内部配置制約1件を既存のomission dispositionへ対応させた。full Draft Result schemaと固定validator関数は通り、元の20 distinct LIMITATION参照・4本文block・Package/prompt bindingを保持できた。新schemaや意味storeは不要だった。

ただし以下の反例が得られたため、PDF・独立quality review・全号実行へ広げず、この単位を完了する。

- 元ArchitectureはWeekly helperの`section_label`要件を満たさず、関数入口で拒否される。
- その要件を明示的なunit fixtureで満たして後段を調べると、12個のCLAIM_BOUNDARYは日本語textを保つがcitationを出さない。canonicalで許される新しいNOTE blockもcompact inputに対応がないとrendererが拒否する。
- Cardのstable IDが解決しても、必要なsourceを指しているとは限らない。Grokの日時claimはDailyX観測を根拠と記すが、source IDは編集後の案内ページしか指していない。

これらは大きなarchitecture Bの必要性も、現行canonicalの放棄も示さない。まず既存source authorityと読者向け引用の接続を1反例で調べるべきである。不完全な基準経路を対照にして新方式の費用優位を作らない。acceptance/staging/cache、owner追加、新store、恒久telemetryの保留は維持する。

## 2. Evidenceと範囲

- [着手時ref](../notes/phase-4e/observation.json): main `005e59841272464307386abfc11f5b09228f0814`、W34 `c1703f772837317b81735cd4cc851c715fff1a3b`。4-Dから不変。
- [使用入力とidentity](../notes/phase-4e/used-inputs.json)、[追加GET](../notes/phase-4e/inputs.json)。rawはignored cacheで固定refから再取得可能。4-Dの入力と新規4件のGit blob/SHA-256を検査。
- [試験範囲・再実行入口](../notes/phase-4e/README.md)、[日本語案](../notes/phase-4e/boundary-wording.lab.md)、[full構造のlab DRAFT](../notes/phase-4e/draft-result.lab.json)。
- [機械検査と反例](../notes/phase-4e/probe-result.json)、[検査script](../notes/phase-4e/probe.py)。
- [Weekly関数の出力抜粋](../notes/phase-4e/weekly-renderer.lab.tex)、[既存render_blockの引用付き抜粋](../notes/phase-4e/existing-block-renderer.lab.tex)。どちらもlab sectionだけでpublication manifestや品質合格ではない。

既知W34の`w34-collaborative-agent-workflows-retrieval`だけを扱う。元の4本文blockを改稿/再検証せず、境界の言語化と対応を著者案として扱う。Package/Architecture/accepted Evidenceは歴史入力であり、承認の新設・流用はない。fixed Core sourceから指定関数と必要なload/hash関数を抽出して実行した。full Core import/CLI、State/Gate、package検証閉包、sidecar、PDF buildは実行していない。

## 3. 判断を変えた詳細

### E1. 構造の表現力は足りるが、意味品質を保証しない

22の境界文をそれぞれ名指しblockへ対応し、重複する制約は同じblockを共有した。12 subjectの20 LIMITATION refsを保存し、regional processingの内部配置はcanonicalに残して読者文へ出さない。must-coverも全blockを一律指定する状態から名指し箇所へ絞った。これに新contractは要らない。

5つの負例は、Package hash不一致、subject誤り、unknown Evidence ID、内部disposition欠落、omissionなのにreader blockを指定、であり、固定validatorはすべて拒否した。一方「すべての数値は独立再現され制約がない」という意図的な意味反転は同じvalidatorを通る。**機械PASSは日本語の意味保存・source sufficiency・review完了を意味しない**。今回の日本語案も著者による照合までである。

### E2. canonicalで有効な出力がWeekly helperと一致しない

固定`survey_weekly_semantic_publication_v2.py::_section_label`は`publication_extensions.section_label`を要求する。対象の実Architectureにはそれがなく、元入力では拒否した。productionでこのhelperが実際に使われたとは4-Dでも確立しておらず、operatorはTeXを著述したと記している。**実productionの12-page PDFがこのエラーで生成不能だった、という主張ではない**。

後段だけを見るため、memory上で`section_label=LAB FUNCTION FIXTURE`を加えた。これは承認済みArchitectureの変更ではなく、単体試験の明示的なfixtureである。元inputへの拒否は結果に残した。

その条件下では、元4本文blockのcompact archive一致と12日本語blockのtext保存を確認できたが、CLAIM_BOUNDARY分岐にはcitation処理がない。通常blockはDraftの`evidence_refs`からではなく、compact archiveの`discovery_ids`から引用する。新しい境界blockをcanonicalで許されるNOTEへ変える負例では、Draft validatorを通っても`non-boundary Draft block missing semantic source`で拒否した。

これは追加adapterやcompact欄が無条件に必要だという結論ではない。**既存full Draftを使う案を、現在のWeekly helperのままで完成経路と数えられない**という互換性の反証である。本文の二重著述や手作業の引用修復を増やす経路はtotal workへ計上する必要がある。

### E3. 既存rendererの部分再利用は可能だが、置換は未成立

既存`render_article_draft_tex.py`にはEvidence ref→source ID→URLの引用とCLAIM_BOUNDARYへのcitationを行う機構がある。canonical Cardsから解決した一時mappingを既存`render_block`へ渡すと、12/12 blockにcitationが付き、13 distinct URLへ対応した。新しい意味storeを作らず機構を再利用できる可能性はある。

ただし旧`evidence_maps`は`primary_evidence/supporting_evidence`、`claim_id/limitation_id`を想定する。v2 Packageを直接渡すと空mappingとなり、v2の`evidence_inputs`、`statement_id`とは一致しない。さらに旧bibliographyはsourceの`role`をnoteへ出すため、今回のCard metadataを入れると`Post-Screening exact authority supplement`等を読者向けに再出力する。**旧renderer全体をそのまま使う解決策は棄却する**。再利用するなら関数と責務を限定する。

4-Dの41件の内部status note除去は引き続き可能で、固定`_bib_text`を41件の既存field値で呼び、既知noteだけを除いた他の生成fieldの保存を検査した。ただし既存文献欄41件には、今回の20 LIMITATION refsが指す13 URLのうち、Antigravityの発表記事とSlackのblogの2 URLがない。source ID由来の引用へ変える場合、既存41 keyを単純に保存するだけでは出典集合の同等性を判定できない。全sourceを全て掲載すべきという判断でもなく、claimごとの出典選択を確認する必要がある。

### E4. 表示関数では補えない日時根拠の対応

対象: `evidence:2026-W34:589f97e8aee10bd1`、Card SHA `c398b532b7d0c047154176eb579e9931d9c025b313649307f5585cddb47781c1`、`claim-2`。

claim textは2026-08-21T17:29:36Zの公式X観測を、contextはLocal DailyX raw bytesを日時のexact authorityとして述べる。しかし`source_ids`は`supplement-src-6b3ce48a6c75d42b`だけで、そのsource rowは`https://x.ai/news/grok-bot-more-plans`を指す。CardのLIMITATION自体が、同ページは8月26日に編集され、8月21本文の根拠にしてはいけないと述べている。Cardには他のsource rowもtemporal eventもない。

したがってCardのIDを正しく解決しても、日時claimが記述する根拠へ読者を導けない。**元のDailyX rawがrepository全体に無いとは結論しない**。今回はその外側のsource/task/supplementを調べていない。rendererが本文やcontextからXのURLを推測したり、編集後ページを日時根拠へ格上げしたりするのは解決策にならない。source-firstの意味確認が必要な場所を具体化できた。

## 4. 次の一単位と停止条件

次は**上記Grokの1件だけを、固定accepted Cardからtask/source supplement/DailyX観測までread-onlyで追う**のが最も判断価値が高い。入口はE4のtask ID、Card SHA、claim-2と、Package内Evidence acceptanceのfilename `task-3ebd2dfa1c0a39c4f92a.json`。artifactの所在は正規のmanifest/参照から解決し、全repo/source再crawlに広げない。

判定すること:

1. 元の日時根拠のexact bytesとlocatorが既存authorityにあり、Cardへの対応だけが抜けているのか。あるなら既存canonical fieldsでどこを修復し、何を再生成/rebind/reviewする必要があるか。
2. 根拠が十分に確立していないなら、その日時claimの保留/限定が必要か。labで根拠や承認を創作しない。
3. 実際のpublication経路は手著述/Weekly helper/別の既存経路のどれを基準にするのが総仕事を減らせるか。reader向けcitationの対応、metadata fieldの選択、使用した全公開要素のreviewを含めて判断する。

1件で既存authorityからの修復可能性と必要な再作業が分かれば、同型の全件監査へ広げず停止・再評価する。解決がrendererだけの変更で済まない場合、全号PDFや新architecture Bを先に実装しない。補助関数の適用より、根拠が揃ったcanonicalから一度だけ読者文を著述し引用を生成する基準経路の条件を先に確定する。

同一refなら今回の日本語案やknown W34を未知source費用比較に使わない。productionで修復が進んでいれば関係差分を先に確認し、重複開発を避ける。次のAstraは新Evidenceによりこの順序を変えてよい。

## 5. 全体目的・費用・未実証・権限

不要な内部noteを生成しないことは、既知の欠陥を発生させない改善候補として維持する。ただし4-Eは12日本語案の著述・対応付け・script・単体fixture・照合という追加のroot仕事を使った。意味判断やcitation repairを前工程へ移すだけでは純減にならない。約4時間runnerやCI時間から今回の修正の削減額を算出できない。

publication全体の品質、独立source-first review/repair/re-review、PDF/visual QA、full canonical admission、Special一般性、歴史全閉包、all-role active time/token/料金、lifecycle純減は未実証。4-Cのreview許可はその試験で完了しており、4-Eでは追加subagentや外部reviewを使っていない。既に得た停止理由を埋めずに品質合格を取りに進む必要はない。

productionはread-only。Human承認、State、Gates、Freeze/Release、adoption/migration、PR/Issueを変更していない。通常Git Pull/Pushと最終commitはHumanが行う。これは完了した限定調査であり、全体目標の達成や外部blockedの宣言ではない。

## 6. 途中Push後のcurrent reality反映 — 2026-09-13 JST

Humanによる途中commit `97a28af`後、PR #488 mergeの連絡を受けて関係差分をread-onlyで確認した。§2の「ref不変」は初回probe着手時の観測として保持し、**現在の入口はこちらとhandoffを使う**。

[更新観測](../notes/phase-4e/production-refresh.json)（2026-09-12 15:47 UTC / 09-13 00:47 JST）:

- [PR #488](https://github.com/eariver/japanese-generative-ai-survey/pull/488)はmerged。mainは`658ae823987431e1f1098243dc2f88cfc0d4864a`。
- W34は`f50d229162b7402c504c0978f72dab4b33052f5e`。旧c170から12 commits / 19 changed paths。Core統合、bib再生成、新PDF、sidecar再実行、reader/quality/review更新、Candidate作成を含む。
- Candidate recordのstatusは`READY_FOR_PUBLICATION_PREVIEW`、candidate SHAは`dbd4c783947fbe6c4f3bc1fab151071f2cd8ed5cb8100fdfceaa7195a10a6fb8`。PDF metadataはSHA `f7403b0a...`、340480 bytes、12 pages。Human Previewの承認やRelease完了とは解釈しない。Production Stateはこの差分で変更されず、旧`VALIDATED_DRAFT`のままである。これらrecord間のfull admission整合は今回検証していない。

[関係差分の検査](../notes/phase-4e/refresh-check.json)、[script](../notes/phase-4e/check_refresh.py)、追加rawのidentityは[inputs.json](../notes/phase-4e/inputs.json)。確認したこと:

1. Weekly rendererの関数AST差分は`_bib_text`だけ。内部status/materialityのnoteを出さなくなった。W34の41 citation keys/order、title/author/URL/urldateの値はすべて保持され、内部noteは0。書式差分にはurldate末尾commaの除去がある。**この生成欠陥はcurrent mainとW34掲載sourceで修復済みなので、重複実装対象から外す。** 旧probeは歴史Evidenceに留める。
2. 最新Candidateが名指しするreader manuscript、quality bundle、semantic review、visual reviewの4ファイルはSHA/byte_count一致。新manuscriptは実bibを正しいhashで指す。PDFはmetadataの照合のみで、download/目視やrootのquality認定はしていない。
3. sidecar再実行reportはhard fail 164→0、既知Mistral framingのREVIEW_REQUIRED 1件、aggregate NEEDS_REVIEWと報告する。このreportのSTOPはCandidate作成より前の段階の記録であり、現在もCandidateが無いとは述べない。こちらでsidecarを再実行したわけではない。
4. 対象Architecture/Package/Draft、section20、main.texは比較差分で不変。新manuscriptのsection20 hashも旧実bytesに一致し、内部のregional processing配置注記は残る。最新semantic PUBLICATION_BOUNDARYは本文/新bibに内部用語・修復履歴が無いとしてPASSする。**bibliography修復の成立と、本文の意味reviewの十分性は別**であり、新Candidateが全体品質の反例を解消したとは判断しない。
5. `_section_label`、`_render_tex`等は関数ASTで不変。従ってE2のcompatibility制約は今回のmergeでは解決されない。Grokを含む上流Packageも不変なのでE4のsource対応の反例も残る。

全体判断は、**修復済みのbib serializer案は閉じ、未解決のcanonical source対応を先に追う**。§4のGrok1件の入口を維持する。今回の修復では実際に再生成/build/sidecar/rebinding/review更新が生じたが、PR #488の将来の純削減額をこれらの件数やwall timeから算出しない。authority文書の再同期commitもあり、意味判断だけでなく運用/保守作業を含めた費用評価が必要という目的も維持する。

current reality更新もreconstruct内のEvidence整理だけで、productionへの指示・書込み、commit/Pushはしていない。現時点で関係差分以上の全号監査やPDF試験へ広げる必要はない。

[終了検査](../notes/phase-4e/closeout-check.json): 初回probeとrefresh検査を再実行し、固定入力identity、lab output、文書のlocal linksと`git diff --check`を確認した。機械的な整合の確認であり、残るsource対応や意味品質を合格へ変えない。
