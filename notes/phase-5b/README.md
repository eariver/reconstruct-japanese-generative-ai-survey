# Phase 5-B Evidence index

本単位は一つの問いの研究→読者本文→非著者review→修復→再reviewの観測。A/B費用試験、full canonical production run、全号Discovery、実験再現ではない。

## 入力と独立性

- [protocol](protocol.md): 出力前の問い、Weekly窓、source候補、品質/coverage、停止条件、全role費用、Humanが許可した一体reviewの境界。
- [source manifest](source-manifest.json): 8 raw filesのURL/明示版/取得時刻/SHA-256/bytes。主根拠はMem0 v1、A-MEM v5、MemOS v1のHTMLとabs metadataの6件。A-MEM v1の2件は出力前の版選定修正履歴であり、主性能比較には使用しない。
- [metadata index](sources/metadata.json)は読むための索引。[fetch_sources.py](fetch_sources.py)は固定版を取得する補助であり、再取得bytesが初回と同じとは仮定しない。今回のexact bytesは`sources/raw/`に保存済み。[read_sources.py](read_sources.py)の抽出は補助であり、caption/表のrowspan/数式/promptの完全消費を保証しない。判定時にはrawを確認した。
- [非著者のsource事前評価](review/source-expectations.md)、[そのfreeze](review/expectations-freeze.json)。reviewerはrootの初稿/reading aidを読まずに事前評価。rootはr1固定まで期待内容を未読。source一般の事前知識やモデル内の認知状態まで隔離/計測した試験ではない。

## 出力・review・repair

- [r1 freeze](r1-freeze.json): source/protocolと初稿の14 filesを固定。30個の意味IDと参照/locatorをlocal検査。[初稿本文](r1/manuscript.md)、[初稿facts](r1/research.json)、[採否/package](r1/composition.json)。
- [独立r1 findings](review/r1-findings.md): blocking一件（評価規模・Jの採点条件等の読者説明不足）、nonblocking三件（版別著者順、graph逆転、日本語）。機械的identity検査と意味品質の判定は別。
- [r2 repair](r2/repair-record.md)、[r2 freeze](r2-freeze.json): r1を保存し、既存sourceの必要部分を再確認してfacts→composition→本文を修復。15 files、31意味IDを固定。[r2本文](r2/manuscript.md)、[r2 facts](r2/research.json)、[r2採否/package](r2/composition.json)。
- [独立r2再review](review/r2-rereview.md): blocking解消、新findingなし。source未解決、後日HOLD、作業量の識別不能を維持。[5-B評価](../../outputs/astra-phase-5b-work-observation-assessment.md)が最終判断。
- [作業観測](work-record.md)。freeze時点の写しは各revision内。rootとreviewerの必要な独立再読を「削減」とせず、W06/W08等の内訳は識別不能を保持する。
- [check_and_freeze.py](check_and_freeze.py)はローカルのbytes/参照/HTML locatorチェックのみ。Coreや独立semantic reviewerの代替ではない。既存freezeの上書きを拒否する。
- [最終local確認](check.json): 保存したr1/r2と非著者事前評価のhash、8 source raw、4 production取得入力のSHA/Git blob、文書リンク、補助Python構文とGit差分を確認。production validationや意味品質の追加認定ではない。

raw、protocol、revision、reviewのhashをGit改行変換から守るため、repository `.gitattributes`は`/notes/phase-5b/** -text`だけを指定した。他の歴史Evidenceやproductionは変更していない。

補助依存は一時領域`.phase-5-inputs/python-deps`のBeautifulSoup 4.15.0。再実行が必要なら同版を同pathへ導入する。raw/r1/r2/reviewを読むだけなら補助実行は不要で、source再取得やrenderer完成を継続条件にしない。

## Current production realityと5-Aからの差分

- [ref/State/diff観測](observation.json): 開始local/remote reconstructはPush済み`cc530fea883a66049b8ab4a9ea3f112da34c4fab`。production main `79a0ddea948af18ef02ec63184e67f99ad7f8e09`、W34 `c7faf207515e7429dd74abd5adaf2962725587ef`。
- [限定repair確認](production-change.json): PR #490はHuman revisionがvalidationを無効化する場合のactive revalidation pointer解除。mainの差分はHuman Gate scriptの6行と新test。事実/編集Taskの単位は変わらない。テストをrootが再実行したとはしない。
- [取得入力manifest](inputs.json): State、Human提供decisionのtranscription、用語修復worklog、CandidateをGit blob/raw SHAで確認。rawはignored `.phase-5-inputs/<ref>/<path>`。必要時は[capture.py](capture.py)に固定ref/pathを渡して再取得できる。`observe`は新しいcurrent観測となるため今回のfreezeの再生ではない。
- W34はHuman `REQUEST_CHANGES`の正式記録→DRAFT_COMPLETEの読者向け用語修正→fresh publication regenerationを経て、**新しいRELEASE_CANDIDATE / PUBLICATION_PREVIEW pending**。Human Preview provenance null、Freeze/Release pending、active revalidation pointer null。Human recordの技術/構造についての受容と、修正後exact bytesのPreview承認は別。
- 新Candidate **raw SHA** `6d18b4962ad51bfa974fd4d814a61a070dcab36a0bff8499d11d5821c28dff7a`、**payload candidate_sha256** `d0af4c9ca917ce3a51d58fcd213846c4d49cb8d3a9334501484ec798970de429`。旧`dbd4c783…`/`c45adaf7…`は歴史値。worklogの`6d18b496…`は今回取得したraw SHAと一致し、payload digestと混同しない。
- reader/品質bundle/review/PDF/checkpoints等は更新。Evidence/Selection/Architecture/canonical Draft pathsは今回diffで不変。用語修復をsourceの意味/引用反例の修復としない。full State validation、全binding閉包、PDF目視、独立全号品質判定をrootが繰り返したわけではない。

残Issueは読んでいない。この限定差分から5-Bの仮説・受理条件に影響しないと判断し、issue crawlを避けた。PR #488/#489/#490はproduction baseline修復でありreconstructの純削減ではない。用語修復の実例は自然な日本語の品質条件へ反映したが、renderer/acceptance/cache実装再開の根拠にはしていない。

production操作、外部メッセージ、PR/Issue送信、Git Pull/Push/commitなし。Humanが許可した一体以外のagentなし。費用/品質の最終判断は5-B評価文書に集約する。
