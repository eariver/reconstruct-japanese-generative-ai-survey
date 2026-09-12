# Phase 4-F — Grokの1 claimのsource対応を追う

2026-09-13 JST。**READ-ONLY TRACE COMPLETE / LAB SPECIMEN NOT ACCEPTED / NO ADOPTION**。

[判断書](../../outputs/astra-phase-4f-source-join-assessment.md)が決定記録。[observation.json](observation.json)のmain/W34は4-E更新時と同一。

## Evidence

- [inputs.json](inputs.json): 取得した固定ref/path、Git blob SHA-1、SHA-256、byte count。rawはignored `.phase-4-inputs/<ref>/<path>`。
- [trace-result.json](trace-result.json): accepted Card→task、Acceptance→Card/Package、Package→supplement、supplement→HTML、task/import provenance→DailyX等の名指しhash照合。該当import/source metadata、既存Sol reviewのbounded PASS、helper再現と限界も収録。
- [source-excerpts.md](source-excerpts.md): hashを照合したDailyX topic 11とprimary HTMLの可視text抜粋。DailyXはDriveから返ったMarkdownのexact bytesであり、元XのHTTP本文ではない。
- [card-corrective.lab.json](card-corrective.lab.json): 参照だけを変える未採用specimen。`src-1`を追加し、claim-2をそこへ、chronology limitation/verificationをprimaryとDailyXの両方へ対応。その他の本文・status・日時・basisは歴史Cardから保持する。**VERIFIEDは既存値のcopyで、新しいroot/独立reviewの合格ではない。** 原本は固定cacheへ保持し変更しない。

既存Sol reviewはbounded chronology PASS。今回のX URLのweb openは403で、投稿削除や日時誤りを示さない。一律の原X再取得要件や自動PARTIAL化を追加しない。元の「secondary Aug 21 dating」という文の別sourceは今回確立しておらず、specimenを全Cardの意味修復完了と扱わない。

## 再実行

```
python -X utf8 notes/phase-4f/trace.py
```

rawが無い場合は`inputs.json`の各固定pathを次で再取得し、同manifestのhashを照合する。

```
python -X utf8 notes/phase-4f/capture.py <repository-relative-path>
```

capture.pyは4-DのGit blob/hash検証を再利用し、出力先を4-Fへ限定する。JSONは明示UTF-8/LFで保存。ネットワーク操作はGitHub GETのみ。

trace.pyは入力identityとschema/local source bindingを検査し、固定`_build_card`関数だけを呼ぶ。その単体fixtureではtask/supplementから読んだ二つのsource authorityを供給する。full `task_authority_sources`/supplement validatorを実行したという意味ではない。

- actual compact record＋actual runner/metaからaccepted Cardのparsed objectを完全再現。
- source_bindingsへDailyXを加えると、全5 statement rowsに両方のsourceが付くことを再現。
- full Card構造で個別source対応が表せることをschema/local checksで確認。
- taskへ未登録の直接X URLへの置換、SOCIALをPRIMARY_OFFICIALへ格上げする負例をlocal source checkで拒否。元の問題Cardもsourceの許可集合検査は通るので、このcheckを意味品質保証にしない。

Core CLI、accepted artifact生成、State/Gate、publication、PDF、独立subagent reviewは未実行。役割別active time/token/料金、純費用削減はunknown。

調査費には既存文書/code読解、targeted directory metadata/GET、hash照合、単体fixture/specimen、current X取得1回、判断/引継ぎを含む。checkpoint keyの探り読み、広いGrok文字列検索の過大表示、Windowsのrg wildcard誤用、supplement keyをsource_idと仮定した失敗も今回の調査費。最初に保守的なPARTIAL案を検討したが、既存Sol reviewのbounded PASS確認後、参照だけの案へ狭めた。productionの失敗/費用には加算しない。
