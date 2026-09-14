# Re:Phase 1 — 記録規則分離候補の接続評価

日付: 2026-09-15 JST  
状態: **root限定評価完了 / 5-file r2 / 独立review・Core実行・採用は未実施**

## 1. 判断

**live statusの二重管理を外す方針を維持し、候補をr2へ修正した。** 今回調べたcaller/testの接続には、削除するlive文字列への依存は見つからなかった。ただし初稿には参照先の設定追従、開始時情報への案内、規範の適用範囲に修正が必要だった。単に「既存testが要求しないから削除可」とは判定しない。

現在の候補は[固定baselineからの5-file差分](../notes/rephase-1-connection/candidate.patch)。[r1からの変更だけ](../notes/rephase-1-connection/r1-to-r2.patch)も保存した。[前回assessment](rephase-1-operating-contract-assessment.md)とr1成果は履歴として不変。r1の13群の表示確認をr2のfull integration結果として転記しない。

production baselineは`774dd39a951c9ac3818e83dfffd4c7666efb0a20`のまま。Git操作、main照会、production実行/変更、外部投稿、追加agentは行っていない。

## 2. 接続の観測

| 対象 | 固定sourceで確認したこと | 判定の限界 |
|---|---|---|
| 実装内の参照探索 | 保存treeとblob hashが一致するscripts配下のPython 212ファイルを文字列検索。execution-record moduleの外部callerはbridge。helper自身にはCLI入口がある | 名前・文字列による探索。動的呼出しや外部repositoryまでの全caller証明ではない |
| bridge初期化 | `execution_record.initialize()`へcfg/Profile/Stateとrun情報を渡し、`validate()`を呼び、二つの返却pathをreceipt対象へ渡す。indexのlive値は解析しない | 実bridge/receipt/Actionsは実行していない |
| execution-record専用test 5件 | 初期化、非破壊性、session掲載、review/defect見出し、session/commit形式を対象にする。indexのassertはProfile identity、X policy、State path。live lifecycle/Gate/hashのassertはない | 元testはProfile/State loaderをmockしている。今回は静的読解のみであり、5件PASSとは数えない |
| bridge test 2ファイル | 初期化E2Eのexecution index存在確認、machine review/receiptの確認を読む。Markdownのlive値依存は見つからない | E2Eは`repository_commit_sha`を呼ぶ。Human Gate testも既存Gate fixtureを使用するため起動しない |
| CI 2ファイル | Core CIの`test_survey_*_v2.py`とpipelineの`test_*.py` discoveryに専用testは含まれる。5-file変更を既存CIへ接続するための新workflowは不要 | 既存CI自体の実行結果ではない |

全testsを取り直していない。初回local scanはscripts 212 / tests 3 / workflows 0であり、その後にbridge tests 2、final-audit test、CI 2等を必要分だけ追加した。未読testや外部callerまで互換性を保証しない。取得範囲とhashは[Evidence](../notes/rephase-1-connection/README.md)に保存した。

## 3. r2で修正した点

| 初稿の問題 | 修正・残す義務 |
|---|---|
| review indexの`gates/review-index.json`を固定文字列で生成 | 既存producerと同じ`cfg.state_authority.human_review_index_path`をProfile source rootからの相対pathとして表示。設定欠落は`NOT_CONFIGURED`、最初のdecision前の履歴不在は承認を意味しない。新resolver/validatorは作らない |
| indexに目的がなく、実行modeへの案内もなかった | 初期sessionのobjectiveへ参照し、requested stopを初期値と表示。各sessionのtransport節へ案内。既存policy §5が要求していたのにbaselineテンプレートが欠いていた`Deterministic execution transport`見出しを生成し、実際のmodeと必要なbridge根拠を記録するplaceholderを設ける。modeを推測しない |
| 「Markdownのcurrent値を更新しない」が広すぎる | authority/execution navigationのlive二重管理に限定。版に結び付いたsession/review・Human提示資料は維持し、誤誘導handoffは使用前に修正する |
| 「Frozen/released editions immutable」がFROZEN後の状態進行まで禁止し得る | released editionの不変性を残し、Frozen Candidate authorityは既存Freeze/Release規則に従う。正当なlifecycle advanceを禁止する新規則にはしない |
| active approvalだけではpending Human review対象への案内が曖昧 | State-bound stage artifactと版付きsession/review presentationから辿る旨を明示。古い承認から対象/許可を推定しない。Human Gate提示を省略しない |

execution mode/transportは各sessionの記録として必須で、Grok/Xの適用時だけ必要と読める曖昧さも外した。sessionの新見出しは既存validatorの必須集合には追加していない。過去のsessionを新レイアウトに合わせて再生成させないためであり、既存policyの記録義務を免除するものではない。

編集した規範のroot読解では、authorityのstatus/履歴を外す変更と、実効規則を保持する変更を区別した。audit invalidation・七観点・post-integration検証・Core/edition分離は保持。Findingの移動は再開/修復認定ではなく、deferred制約は引き続き明示。overlayの実効規則はr1と同一。独立した意味的reviewは未実施である。

## 4. 今回の確認結果

[checks.json](../notes/rephase-1-connection/checks.json)は5群の限定check。内訳:

- 固定版からr1を保存patchで再構成しhash一致を確認。r2 patchをメモリ内で適用し、5候補ファイルと一致。累計41 captured inputsのbytesは不変。
- helperのindex/sessionテンプレート以外は**全ASTが同一**。loader、引数、返却処理、非破壊guard、validator、CLIを変更していない。
- 実W34/SP001 Profileの形と明示した合成session値を使い、テンプレートだけを評価。既存testのnavigation要件、目的/transport参照、custom/missing review-path設定、activeと履歴の区別を確認した。
- 4文書の42非編集節がbaselineと全文一致することをr2でも確認した。
- 内容を読んでGitを使わないことを確認した**上流の文書専用test 4件**を、固定rule/AGENTSとr2 bootstrapだけの一時directoryで実行し、全件通過。mockなし。これは最終audit実施でも七観点PASSでもない。

production module、initialize/validate本体、bridge、CLI、Git-aware testは実行していない。レビュー済commitの検証をstub化して実行互換と見せることもしない。テンプレート例は新しいproduction/session/Human authorityではない。

## 5. ここでの終了面と残る判断

この単位のroot接続評価と既知の候補修正は完了。追加の表示probe、全manual統合、旧Freeze/reader修復へは広げない。新たな具体的反例がないまま同じ著者によるoffline checkを積み増しても、残る独立性/実行の不確かさは解消しない。

次に価値があるのは、**このr2の独立review**と、許可された環境での既存Core/CLI/bridge回帰である。独立reviewの具体scopeは、5-file差分の削除義務と保持義務、初期化/再開/REQUEST_CHANGES時の参照、履歴とactive authorityの分離、既存caller/testとの接続。表示probeの再実装やfull publication試作は対象外。独立agentは新たなHumanの明示許可が必要であり、今回の一般的な続行指示をその許可に拡張しない。Git禁止も継続する。

将来採用する場合は既存のfixed-head review/CI/contract規則を適用し、旧State/approval/hashを付替えない。production posting/適用/adoptionは別の明示許可が必要。現段階では新しいコードをproduction-readyとせず、採用後の総仕事削減も未測定とする。原記録の探索やHuman/reviewerへの仕事移動が増えるなら案の便益を再評価する。
