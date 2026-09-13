# Phase 5-B protocol — 一つの問いの作業観測

2026-09-13 JST。状態: SOURCE FREEZE / NO AUTHOR OUTPUT / ONE REVIEWER AUTHORIZED。

基準reconstruct: `cc530fea883a66049b8ab4a9ea3f112da34c4fab`。開始時local/remote main一致・cleanを確認。5-Aの単一chain観測を継承し、A/Bや費用優位を測ったとはしない。

## 問い・標本と選定前提

問い: **長期会話を扱うLLMエージェントの外部メモリについて、Mem0の報告から品質と処理負担の何が分かり、他方式との比較・導入判断にはどの条件確認が残るか。**

読者は日本語の技術読者。方式の機構、評価集合、質問種別、backbone/judge、baseline、metric定義、測定範囲、source固有の制約を区別する。論文のmaker-reported結果を独立再現やJ-GASの実運用費へ変換しない。

候補はMem0 (`2504.19413`)、A-MEM (`2502.12110`)、MemOS (`2507.03724`)の各arXiv v1。既存W34/CAS/P-EAGLE/DFlash/旧lab以外から、同じ外部メモリ問題と比較軸を持つ3候補として選んだ。一般的な名前/分野の事前知識はあるが、このsessionで本文・表の解答はまだ作成していない。2026-09-13のlocator検索ではタイトル/短い検索snippetに接触した。完全な未学習authorやランダム標本とは主張しない。

仮のWeekly観測窓は2025-04-28 00:00 UTC〜2025-05-05 00:00 UTC未満。v1公開metadataを確認し、主候補が窓と合わなければ本文作成前に理由付きで修正する。背景研究の利用は可能だが「今週の新発表」と混ぜない。後日sourceを当時のpublication根拠に用いない。採用/HOLD/除外の正答は未固定。第三候補もmetadata/本文からsource固有の範囲を確認し、単なる未読DROPにはしない。

これは指定source集合のbounded sliceであり、当時の完全なWeekly Discoveryや全research laneの再現ではない。source外の強い対照をreviewerが発見した場合、omissionとして記録し、必要ならsource集合/出力を改版する。全号coverageへの外挿をしない。

## source固定・著述・review

- 一次sourceは明示v1のraw HTML/PDFとarXiv metadataを保存し、URL/取得時刻/byte hashをmanifestへ記録。読むための抽出は補助であり、表/脚注/限界の確認にはrawを参照する。
- 本文の別version/二次解説/後日のbenchmark論争を無意識に混ぜない。版の追加やsource拡張は具体的な未解決が判断を変える時に限り、rawと理由を別保存する。網羅的検索を行わない。
- 非著者reviewer一体が先にprotocolとsourceから期待内容・強い反例・omissionを固定。その後初稿をreviewする。rootは初稿固定まで期待内容を読まない。reviewerは本文を著述しない。rootがrepairし、同reviewerが再reviewする。
- Humanは本sessionで5-B専用の非著者reviewer一体を明示許可した。範囲はsource事前評価、初稿review、root修復後の再reviewのみ。本文著述・production操作・追加委任は禁止。外部production reviewerへのメッセージは送らない。
- 完了物は候補別の事実/subject/source/比較条件、全候補の採否、packageの問い/coverage/境界、自然な日本語本文と根拠参照、初稿freeze、finding、repairと再review。既存canonicalの意味分離を使うlab部分構造とし、full production schema/admissionを模造しない。
- 日本語品質は自然な標準的技術用語、source帰属、意味を変えない説明を含む。productionの今回の用語修復を踏まえ、機械PASS/直訳の逐語保存を読者品質と同一視しない。

## 観測と停止

意味判断を変更した時/sourceへ戻った時だけ、問い・比較軸/subject/source版/role/再訪理由/利用した既存結論/新たな判断/影響先/計測値またはunknownを簡潔に記録する。思考過程の全文は記録しない。

初回読解、新source/新要件、独立review、誤り修復、既存結論を利用できず行う再構成、機械再生成を区別する。同じ問い/subject/source版/条件について既に使える結論があり、新しいEvidenceや品質要求がないのに実質的研究をやり直した時だけ、除ける再構成候補とする。必要な再読・別の編集判断・自動コピーを削減に数えない。

全roleの探索/読解/authoring/review/repair/再生成/補助/観測/handoffを含める。rootのactive time/token/料金はoperation別の実測が得られない限りunknown。tool command runtimeやreview wall spanはその単位のまま保持する。Human Gate、Core受理、全号synthesis、PDF/visual、CI、移行/歴史互換をlabで省略し、費用ゼロ・合格としない。

初稿→独立review→最初のrepair→一度の再reviewを一区切りとする。blocking残件は不合格/未実証。質を満たす範囲で除ける再構成が観測されなければ、この単位では仮説を支持せず共通authoringで閉じる。独立性・観測性の不足が中心なら識別不能。5-C/新B/renderer/acceptance/cacheを埋め合わせで開始しない。

production変更/PR/Issue送信/State/Gates/承認/Freeze/Release/採用/移行、Git Pull/Push/最終commitは行わない。

## 出力前のmetadata確認による修正（r1固定条件）

arXiv metadataを2026-09-13 10:18 UTC頃に確認。Mem0 v1は2025-04-28公開なので窓は維持する。A-MEMはcutoff以前にv5（2025-04-18）が存在したため、主比較をv1から**v5**へ変更する。古い版を便宜的に弱い対照へ使わない。取得済みv1は準備履歴として保持するが、本文/性能比較の根拠集合から外す。MemOS v1は2025-07-04公開。後日の強い候補を時点の対照として検査する。source集合はMem0 v1 / A-MEM v5 / MemOS v1、metadataとraw hashはsource-manifest.json。version metadataには後日の履歴も含まれるが、当時の根拠へ昇格させない。

初期の「各v1」はこのmetadata確認で上書きされた選定案であり、初稿へ適用する条件ではない。検索snippetへの接触とこの変更は準備費/新情報であって、除ける同一結論の再構成には分類しない。
