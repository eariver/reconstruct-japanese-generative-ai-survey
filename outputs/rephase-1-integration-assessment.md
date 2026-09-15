# Re:Phase 1 — r2の限定統合検証と判断

日付: 2026-09-16 JST

状態: **限定Git-aware統合検証完了 / r2維持 / production採用・七観点audit・純削減は未認定**

## 1. 判断

**r2の運用規則/live status分離案を維持する。今回確認した統合範囲で、修正を要する候補由来の問題は見つからなかった。** 前回までのmock単体testから、実Profile/State loader、CLI、bridge、実在するGit commitに束縛されたHuman Gate検証へ進んだ。

固定production baselineは`774dd39a951c9ac3818e83dfffd4c7666efb0a20`。Humanの最新指示でGit操作禁止は解除された。必要なGit-aware検証だけを独立repositoryで行い、新しいproduction mainへの追従、production変更・投稿・適用・採用は行っていない。reconstructの通常の最終commit/Pull/Pushも行っていない。

現在の[5-file r2候補](../notes/rephase-1-connection/candidate.patch)は不変。[独立限定レビュー](../notes/rephase-1-connection/independent-review.md)の対象bytes、当時のassessment/checksもそのまま。今回の実行結果はrootによる追加Evidenceであり、新しい独立integration reviewや七観点auditではない。

## 2. 統合で確認したこと

| 範囲 | 結果 | 認定しないこと |
|---|---|---|
| 固定版のbridge/Human Gate上流test 3クラス | **27個の異なるtestが通過**。Linux初回の18件と、試験側guard修正後の残り9件。初期化→Discovery、Architecture/Publicationのrevision→approval、publicationからArchitecture再開、履歴保持、commitの不存在/到達不能/対象bytes不一致の拒否を含む | 全upstream suite、GitHub Actionsの実dispatch、実Humanの判断品質 |
| 3 Profile形態の実CLI | Weekly、Thematic/LONGFORM、設定済monthly Retrospectiveで、実Core初期化→State検証→execution-record初期化/validateが通過。ROLLING_WINDOW / OPEN_HISTORY_AS_OF / BOUNDED_PERIODを保持 | 全Special/Foundations、研究・執筆・公開までの一般性 |
| CLIの負例 | Profileのschemaを保ったbytes driftはindex生成前に拒否。既存indexの再初期化を拒否してbytes保持。State/Profile issue不一致を拒否 | あらゆる破損・競合・移行の網羅 |
| State遷移とnavigation | 実fixtureのINITIALIZED→pending r1→REQUEST_CHANGES r1→pending r2→APPROVED r2の各点で、同じindex bytesのまま実loader/構造validatorが通過 | session/review proseが実運用の全記録義務を満たすこと |
| active approvalと履歴 | APPROVED後にactive approvalファイルを欠落させると検証が失敗。過去APPROVEDからのauthority復活なし。元bytesを戻すと再び通過 | すべてのpublication authority閉包、PDF/公開asset品質 |

実行結果の集約は[results.json](../notes/rephase-1-integration/results.json)。CLIは21回のコマンド呼出しで上記3形態の正負例を確認した。これは21個の独立品質testという意味ではない。navigationは6確認点で同じindex hashを保持した（最後は欠落負例後の復元確認）。

今回のpositive/negativeはProfile/State loaderやレビュー済commit照合をmockしていない。上流fixtureが生成する研究・semantic/visual review・Human decisionは引き続き**合成記録**であり、実研究・独立review・Human approvalの代わりにはならない。

## 3. Gitと固定baselineの扱い

保存済みの固定treeとblob hashを使い、Core実装・config・schema・規範・workflow・template・Special定義・対象testの**485ファイル**を取得した。463ファイルはhash一致するlocal cacheを再利用し、22ファイルだけ固定commitのraw URLから取得。productionの約2.3 GBのsources履歴やsurveys成果物を複製して全履歴を再検証することはしていない。

この部分snapshotから、独立Git rootに合成baseline commitと合成r2 commitを作った。r2との差分は候補5ファイルだけ。これらはproductionの実commitそのものではなく、実Gitの実在性/到達可能性/対象bytes検証を動かすための**fixture commit**である。

- 合成baseline: `270050797c3a28861f05cffae1c142fc9b9271bc`
- 合成r2: `502b3781c58a1b453f5d9389caef32f3a7866524`

最初はignored `.rephase-1-inputs/integration-r2/`、最終Gate/CLI/navigation試験はUbuntu `/tmp/jgas-rephase-r2-502b3781`で実行。後者は前者を`--no-local`で複製した独立databaseで、alternatesを持たず、originは`https://example.invalid/rephase-fixture.git`に変更した。remote network fetch/pushは行っていない。testのreview snapshot objects/refsはこの独立fixture内だけに作られた。

fixtureのHEAD/通常indexは試験前後で維持し、testのremote-tracking refsはcleanup済み。全485入力の実行後bytesが期待値（5ファイルのみr2）と一致すること、元r2とreview packetが不変であることを確認した。reconstruct HEADは開始時/終了時とも`388d827922459c2130512513148613657d0deede`。最終commitは作成していない。

## 4. 初期失敗の切り分け

初回から全件PASSだったとは記録しない。試行ログを[Evidence](../notes/rephase-1-integration/README.md)へ保存した。

- Windowsでaudit hookの`subprocess.Popen`引数表現を誤って扱い、試験側で失敗。Windowsのcommand-line形式に対応させた。
- その後のWindows実行は27件中11 errors。固定Coreの`str(relative_path)`がbackslashを生成する一方でvalidatorがbackslashを拒否することと、環境のAsia/Tokyoデータ不足によるもの。r2が変更していない初期State生成段階の問題であり、候補をWindows対応へ拡張せずUbuntuへ移した。Windows実行互換は未成立のまま。
- Linux初回は18 PASS / 9 errors。試験用allowlistが実際に必要な`check-ref-format`を拒否していた。次の9件は`ls-tree`拒否で止まった。ローカルGit照合コマンドだけを許可し直し、未完了9件のみ再実行して全通過。Coreのfail-close照合を外したわけではない。
- CLI初期fixtureのWeekly日時が対象号のcutoff前だったため正しく拒否された。fixture日時をcutoff後へ修正した。元の拒否規則・候補コードは不変。

UbuntuのPython環境にはpip/ensurepipがなかったため、workspace内の専用環境へbootstrapし、固定Coreが要求する`jsonschema==4.23.0`・`pypdf==6.16.2`を導入した。解決済み依存versionも保存。システム全体へpackageを導入したりproduction環境を変更したりしていない。

## 5. 今後の進め方

この候補についての著者側作業は、**設計・静的接続・許可された独立限定レビュー・単体回帰・今回の限定統合**まで終了する。成功testの反復や、今回の範囲で必要のないFreeze/reader全面修復・全manual統合・新resolverには進まない。

次は、**r2をproductionへの適用審査に進めるかというHuman判断**が妥当である。ただし今回の結果だけで適用可能と宣言せず、進める場合は実際のcandidate treeに対する既存Core review/CI/fixed-head七観点audit・contract変更の扱いを満たす必要がある。新しい独立agent作業の許可とproduction変更/採用の許可は別で、今回どちらも追加取得していない。

残る未確認はfull upstream CI、実Actions輸送、実際のadoption/既存editionとの契約互換、全Profileの公開完走とpublication品質、全roleの純lifecycle work差。今回「Stateの変化だけならindexのlive値同期を要求しなくても限定機械検証は成立する」と確認できたが、必読規範や必要な原記録探索・reviewは残る。実運用で仕事が別roleへ移っただけなら削減とは数えない。全体reconstructionは引き続き未完了。
