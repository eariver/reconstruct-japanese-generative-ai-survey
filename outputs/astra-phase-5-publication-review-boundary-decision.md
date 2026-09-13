# Phase 5 — Publication review境界の判断

日付: 2026-09-14 JST
状態: **ONE REPAIR CASE TRACED / EXISTING REVIEW APPLICATION GAP IDENTIFIED / NO ARCHITECTURE ADOPTION OR NET SAVING CLAIM / CONDITIONAL 5-C NOT STARTED**

## 1. 判断

**次の改善対象は、既存の編集reviewを、本文だけでなくclaim boundary・書誌等を含む実際の読者向け出力へ適用し、問題をHuman Previewまで持ち越して生じる追加周回を減らせるかである。** 新しい研究Task単位、reviewer追加、意味store、full rendererを先に作る根拠は得ていない。

5-Bの次入口を、W34 Human Preview r2の一件で確認した。結果は「review項目が無かった」ではない。問題の出力はhashで正しくbindされ、同じ版のsemantic reviewは内部用語なし、visual reviewはclaim boundariesを含むPDF確認を宣言していた。その後Humanが内部編集文言と誤った書誌アクセス日を指摘した。**対象版へのbindingとcheckのPASSだけでは、宣言した範囲への判断が有効だったとは限らない**ことが、この実例で具体化した。

これは5-Bの「候補別研究と後段編集の除ける意味再構成」が実証されたという話ではない。その仮説は非支持/一部識別不能のまま、条件付き5-CのA/B試験は非開始。Phase 4もclosedのまま。

本単位は原因・既存責務・修復波及・次の投資条件を判断できる所まで進めて閉じる。以下の改善方向はreconstruct上の設計判断であり、production手順変更の指示や採用ではない。

## 2. 基準とproduction realityの更新

開始reconstructはPush済み`4504d4c1c52d9fcda75e20803b72d470c67a74be`。local/remote main一致・clean。通常Pull/Push/commitは行っていない。

GETでmain `74708eb26a357ec11a839a59de62ab62cd246eef`、W34 `6be0f462d8f02284f8513d7165c778c3797dcaf4`を確認。mainのPR #492はbibliography access provenanceのShared Core修復。W34はHuman r2 REQUEST_CHANGES→Core統合/edition修復→fresh publication→**canonical Human Preview APPROVE r3**。現在`RELEASE_CANDIDATE`、次は`stage:freeze`、Freeze/Releaseはpending。

現Candidate raw SHAは`df376f47…`、payload digestは`52c8d0bc…`、PDFは`e93db71a…`。r3がbindしたCandidate/PDFと現在bytes、State→approvalとimmutable approval、reviewed pre-approval Stateの局所bindingを確認した。5-Bの「Preview pending / null provenance」はこの観測へ更新する。承認が存在する現在に、古いpending表現を残さない。

rootは全State validator、依存閉包、PDF目視/全号品質審査を再実施していない。Human承認を尊重し、過去の問題からcurrent承認を取り消す判断はしない。PR #488/#489/#490/#492はproduction baseline保守でreconstruct成果ではない。

[Evidence](../notes/phase-5-review-boundary/evidence.md)、[観測](../notes/phase-5-review-boundary/observation.json)、[局所確認結果](../notes/phase-5-review-boundary/check.json)に詳細と確認限界を残した。

## 3. 一件で判明したこと

| 修復要素 | 原因と既存reviewとの関係 | 今回の判断 |
|---|---|---|
| section20のclaim boundary末尾 | 内部で正しい配属理由がDraft CLAIM_BOUNDARYからTeXへそのまま現れた。旧reviewはそのsectionを指して内部用語なしとPASS。r1の用語修復はclaim boundariesを変更せず | 読者向け範囲説明への編集判断が必要。制約の保持と内部文言の逐語コピーは別。review対象のファイル追加や新しいcheck IDだけでは解けない |
| 41件の書誌access日 | generatorがWeekly cutoff / Special as_ofを一律に使用。旧書誌reviewのkey解決/byte-identical再生成はこの誤りを検出できなかった | source accessを明示的に消費する機械処理の問題。PR #492で修復済み。LLM/Humanに毎号41日付を作り直させる案を採らない |
| 完了/品質記録 | manuscript/semantic/visualは同じ実行側名義。generic detailは全体PASSを述べ、限定した修復記録を超える。機械検査はbytes/check集合等を保証 | 既存の独立supervisory責務がこのexact版をどう消費したかは、調べた記録では実証されない。独立reviewがどこにも無かったとは断定しない。review名義欄追加は解決とみなさない |

旧manuscriptと問題のsection/bibの実hashはreviewと一致した。ファイル取り違えや古いhashのreviewという原因は、この二要素について除ける。逆に「claim boundaryを一切読まなかった」「contextが足りなかった」「モデルが弱かった」は認知記録がなく識別できない。

既存governanceはpublicationのeditorial/semantic/visual責務と実行側からの独立性を既に置き、review contractも`PUBLICATION_BOUNDARY`と`EXACT_PDF_VISUAL_REVIEW`を要求する。Specialにはさらにexact blockの位置確認がある。それらを新architectureの機能として再提案しないし、位置確認を増やせば意味品質が上がるとも推定しない。

## 4. 進める方向と棄却する代案

**最小の候補は、既存のpublication編集reviewの仕事を「完成した読者向けsource一式」に揃え、その主たる意味判断を最初の高コストbuild/Candidate生成より前に置けるかを確認すること。** 既存manifestがbindするTeX・書誌等と既存reviewのdetail/evidence_locationsを使えるため、当面新schema/storeは要らない。本文、限界説明、脚注、cover/synthesis、書誌のうち、実際に公開される要素をpublicationの仕事として扱う。source事実の確認と内部auditの保管は引き続き必要である。

この候補を具体化するときの条件:

1. **独立した既存review責務の消費を確認する。** execution側の「整えた」と独立判断を混同しない。すでに外部で同じ版を十分reviewしているなら、その作業との重複を先に解消する。現在の可視記録不足を新agent追加で埋めない。
2. **全体PASSの根拠を実際の公開箇所で述べる。** 例えば既存`PUBLICATION_BOUNDARY`のdetailで「section20 claimboundaryの節範囲説明とsource限界を確認」と具体化できる。別の恒久coverage ledgerや全項目の逐語転記を必須にしない。文字列を埋めたこと自体も品質証明ではない。
3. **source段階の意味reviewと、生成後のexact PDF確認を役割に応じて接続する。** review記録/Candidateは最終PDF・manuscriptへ正式にbindする。PDFでしか見えない欠落・改変・可読性や最終全体の責務は残す。古いPASSをhashだけ付け替えて使わず、変化/変換の影響を再判断する。既存validation/Human Gateの省略を前提にしない。
4. **書誌は修復済みCoreを共通baselineへ含める。** event日、page dateline、access日は別。今後も未知/曖昧なprovenanceはfail-closeで扱う。local値の帳尻合わせやcutoffへのfallbackはしない。

| 代案 | 採らない理由 / 再評価条件 |
|---|---|
| reviewerやPASS項目を追加 | 責務/項目は既にあり、消費が改善する証拠なし。実行・supervision・Humanの総仕事を増やし得る |
| 全公開文章の内部語ブラックリストを新Gate化 | この既知例は見つかっても、技術用語としてのpackage/selection等は正当な場合がある。意味品質と限界保持は保証できず誤検知修復を生む |
| claim boundaryを削る/短くすれば良いとする | source固有の限界を失う。今回の正当な修復は節範囲の説明へ一置換し、他の限界を残した |
| 新reader意味正本/full rendererへ即投資 | 現manifestと正式なTeX authoringで修復可能。再生成時の長期保守損失や実反復量が未測定 |
| Specialの位置証明をWeeklyへ移植 | 位置を知っても旧reviewは同じsectionとclaimboundaryを宣言済み。意味見逃しを防ぐ証拠にならない |
| Humanに追加precheckを依頼 | Human手作業への移転。既存の二つのHuman Gateとadoption権限を保つ |

mainのCLAIM_BOUNDARY出力は依然textをescapeして出す。ただし修復後W34の通常PDF buildは修復TeXから行う。旧Draftから再著述する際の再発可能性と、通常buildでの実再発を区別する。この一件をPhase 4-H renderer再開の自動理由にはしない。

## 5. Total lifecycle workとしての判断

意味を正す仕事、access provenanceを解決する仕事、独立review、最初のbuild、Humanの最終判断は必要仕事であり、前へ移すだけでは削減にならない。回避候補は、同じ問題を遅く発見したために増える**追加周回**である。

今回のr2にはHuman要求のcanonical記録/rollback、Core統合とedition修復、CI build、PDF確認、manuscript/bundle/review/checkpoints/Candidate再生成、再びHuman Previewという実仕事があった。worklogはCIを3m45sと報告するが、root実測でも全費用でもない。r1にも別の周回がある。二原因が一緒に修復されており、claimboundaryだけ直せばr2周回全体が消えたとは言えない。

長期比較で残す式は、**早期に防げる周回の期待費用 − 追加のsource準備/独立消費/変換確認/同期/記録費 − 初期実装/移行/歴史互換/二重保守費**。変更前後で共通の修復/意味判断費は相殺しても、省略工程をゼロにしない。Shared Core修復によってaccess日原因の今後の発生率は変わるため、旧r2全体をそのまま将来baselineの反復費へ使わない。

全role active time/token/金額、Human負担、再発率、早期検出率、現reviewの実消費量はunknown。したがって現時点では「改善投資の対象を絞れた」であり、純削減/ROI/新architectureの優位は認定しない。今回のread-only取得・code読解・hash/差分確認・文書化自体もreconstruct費である。

## 6. 停止面と次の入口

本単位は、**正しいbindingと既存checkがある場所でもHuman修復を防げなかった実例**を特定し、機械処理の原因（既修復）と残る編集判断/消費の問題を分離した所で完了。追加Issue crawl、全W34監査、旧lab再実行はこの判断を変えにくいため行わない。現在の承認済みW34に追加review要求を出さず、freezeも実行しない。

次に進めるなら、**current方式の既存publication reviewを誰が・何の入力で・いつ消費するかを明示した、一回分の実行計画**を先に具体化する。新たな意味正本やstageは作らず、前節の追加周回を省ける条件と増える仕事を同時に示す。既存reviewが既にsource一式を適切な時点で独立消費していると分かれば、その仕事を追加する案は捨て、見逃し原因/残存頻度が投資を支持するか再判断する。

比較実行を選ぶ条件は、修復済みCoreを両側のbaselineに置き、独立性・同等の全公開要素の品質・exact PDF/Human authorityを維持し、前倒しの追加仕事と後段の省略可能仕事を実際に観測できること。既知r2をもう一度見つけるだけの自己試験では足りない。条件が揃わなければ新trialを始めず、この限定提案を保守候補として残して全体の優先順位を再評価する。5-Cの旧仮説を自動復活させない。

全体目標はopen。publication quality、provenance correctness、fail-close、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準で維持し、production/review/repair/CI/LLM/complexity/Human burdenを含む総仕事を下げる責務は変わらない。full canonical baseline・全号品質・一般性・歴史再現・純削減は未実証。

権限: production read-only。PR/Issue/comment/State/Gate/Freeze/Release/adoption/migrationに変更なし。追加agentなし。旧review許可は使わない。通常Pull/Push/最終commitはHuman。[current handoff](../handoff/astra-phase-5-continuation.md)から継続する。
