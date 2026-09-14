# Re:Phase 1 — operating contract split Evidence

固定production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`。Humanの明示rebaselineまで変更しない。本単位ではGit操作禁止、production read-only。

判断: [限定設計assessment](../../outputs/rephase-1-operating-contract-assessment.md)。

## 保存物

- `inputs.json` / `inputs.py`: 固定版32ファイルの捕捉manifestと補助。前回の保存treeを使用し、cacheのrawをblob hashで照合。足りない既知pathだけ固定commitのraw HTTP GETで取得。Git/GitHub refs/mainにはアクセスしない。新しい観測で旧`notes/rephase-1/evidence.json`を上書きしない。
- `candidate.patch` / `candidate-files.json` / `build_candidate.py`: 5-file差分、前後hash/行数、再生成器。Python difflibを使用。候補全ファイルはignored `.rephase-1-inputs/contract-candidate/`。固定baseline cacheとproduction checkoutには書かない。
- `state_view.py`: offlineの限定表示probe。State/Profile、selected release/Preview checkpoint、active approvals、review indexのGateごとの最新**履歴**recordを直接照合する。全checkpoint/依存閉包、Git reachability、Candidate/PDF/品質は検証しない。表示probeをproduction validatorとして採用する案ではない。
- `verify.py` / `checks.json`: 13群の表示・negative・テンプレート/規範保持check。production import、Git、遷移なし。
- `examples.json`: 固定W34/SP001と2つの明示fixtureの表示。REQUEST_CHANGES後fixtureはCore出力でも当時のexact Stateでもない。
- `navigation-template-example.md`: 改訂initializerのf-stringだけをASTから評価した例。実W34の新しい実行記録ではない。`EXAMPLE_ONLY`のsession参照は実ファイルではない。

## 再現と隔離

`python -B -X utf8 notes/rephase-1-contract/verify.py`

このcommandは候補差分を再生成し、captured filesから必要なsourcesだけをtemp directoryにコピーして、表示関数/JSON Schema/抽出f-stringを確認する。Git repositoryを作らず、Gitを呼ぶproduction `initialize`/`validate`は実行しない。baseline rawは前後hash一致を確認。Python/jsonschemaは既存runtimeを使用。

入力cacheが不足する時だけ `python -B notes/rephase-1-contract/inputs.py <inputs.json内のpath> ...`。保存treeがない場合は勝手にmainから再取得せず、この固定refの取得方法を用意する。既存`notes/rephase-1/capture.py observe`はGit/ref確認と旧記録更新を含むため、現在の制約下では使わない。

## Setupと限界

取得時に一度、実在確認前の`schemas/production-profile-v2.schema.json`を指定してmembership assertionで停止。保存treeで`schemas/survey-production-profile.schema.json`を確認して続行した。不存在pathのHTTP取得は行っていない。

最初の候補生成では、終端文字列が先行する見出し定数に一致してhelperの内容を余分に連結した。検索開始位置を制限して修正した。次の構文確認は明示UTF-8なしのreadがWindows cp932で停止したため、UTF-8で確認した。最初の表示fixtureはschema-required checkpoint keysを削除して型拒否となり、pending pointerをnullで保持するようfixtureを修正した。Profile表示のtemporal_policyは正しい`research_scope`内を参照するよう修正し、Weekly/Thematicのmodeをcheckに追加した。いずれもprobe/candidate準備の修正で、production defectやproduction repairではない。

最終checkは13群完了、42節の保持確認、固定入力の前後不変。構造保持は編集節のsemantic reviewの代替ではない。候補全体のCore integration/CLI/caller/歴史互換・独立review・全publication品質・費用削減は未検証。既存文書に残る他のstatus/precedence不一致を網羅的に修復していない。

Git禁止のためHEAD/index/status/diff等も照会していない。今回の差分は捕捉rawとのファイル比較で作成・確認し、Git working treeがcleanかどうかは主張しない。
