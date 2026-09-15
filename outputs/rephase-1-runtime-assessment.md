# Re:Phase 1 — r2実行記録helperの単体回帰

日付: 2026-09-15 JST  
状態: **既存単体test 5件PASS / r2不変 / full Core統合・採用は未認定**

## 判断と今回の前進

独立レビュー後に残った実行確認のうち、**既存execution-record単体testをr2の実helperで実行し、5件すべて通過した**。前回までのAST・テンプレート確認から、初期化による実ファイル生成と構造validatorの実行へ進んだ。今回初めて実行したtestであり、成功済みcheckの反復ではない。

ただし元testは`_load_profile`と`_load_state`をmockしている。今回も元testを変更せず、その境界のまま実行した。これはhelper本体の単体回帰であり、**実Profile/State/contract/reviewed-commitを通した統合検証ではない**。production検証を通すために新しいmockやGitの成功応答を追加してはいない。

新たな不具合は見つからず、[r2候補](../notes/rephase-1-connection/candidate.patch)を変更せず維持する。[独立限定レビュー](../notes/rephase-1-connection/independent-review.md)の対象bytesも不変。独立レビュー許可を追加消費・拡張せず、今回はrootのみで実施した。

## 実行結果

| 元testの対象 | 結果 |
|---|---|
| canonical execution treeとProfile/State等のnavigation生成 | PASS |
| 既存indexがある場合の非破壊性 | PASS |
| indexに未掲載のsession検出と掲載後の解消 | PASS |
| review/defect記録の必須見出し欠落検出 | PASS |
| unsafe session IDと不正commit文字列の拒否 | PASS |

[実行ログ](../notes/rephase-1-runtime/unit-tests.txt)、[機械結果と入力hash](../notes/rephase-1-runtime/unit-results.json)。5 tests / 0 failures / 0 errors / 0 skipped。commit文字列testは形式の確認であり、commitの実在・到達可能性の確認ではない。

## Git-freeの実行方法

固定baseline `774dd39a951c9ac3818e83dfffd4c7666efb0a20`の保存tree/blob hashに照合した、専用testとimport依存19ファイルを使用した。実際にimportする依存コードを事前に静的確認し、実helperだけをr2 bytesへ差し替えたcopyをreconstructのignored領域内に作成。production checkoutを参照・変更していない。

Pythonを`-I -B`で起動し、一時directoryをcwd/import root/fixture出力先とした。production由来の固定コードはこのcopyから実際にimportした。これまでの「production moduleをimportしていない」という記録は過去の各調査範囲の説明であり、今回については該当しない。

import/test開始前にaudit hookを設け、外部process起動、通信、`.git` pathの読取り要求を処理前に拒否する。拒否は成功の代替ではなくtest/setup失敗にし、要求も記録する。今回この種の要求は0件だった。test対象のvalidation関数に新たなstubは入れていない。

一時directoryは終了時に削除し、固定source/r2候補のhash不変を確認した。Git操作、remote ref/main照会、production実行・変更、外部投稿、追加agentは行っていない。ここでの「production実行なし」は実editionの運用を行わない意味であり、固定コードcopyの単体実行を隠すものではない。

## 残る条件と終了面

今回までの到達点は、設計候補、root静的接続確認、独立限定レビュー、既存helper単体回帰。元のr1表示実験や文書testとまとめて「Core統合PASS」と数えない。

CLIの実入力経路、実State/contract/approvalの全検証、bridge/Actions、実publicationは未実行。既存bridge E2Eは固定版`tests/test_survey_core_execution_bridge_v2.py:247`で`core.repository_commit_sha(self.root)`を呼び、同`survey_production_v2.py:129–143`のGit subprocessへ至るため、現在の禁止下では起動しない。全てのCore関数が常にGitを要するという主張ではない。既存単体mockを外した完全な初期化/承認chainを今回作り直してはいない。

次にこの候補を採用へ進める場合は、実際のrepository/commitを扱える明示許可のある環境で既存integrationを確認し、別途production採用判断を行う。Git禁止を解除したとは解釈しない。候補変更がないため、現時点で追加独立レビューや同じ単体testの再実行は不要。

この単体回帰を完了して停止する。全体reconstructionは未完了、production採用・七観点audit・品質保証・純lifecycle savingは未認定。必要以上のshadow productionや新validatorを作ってこの境界を埋めない。
