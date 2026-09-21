# Re:Phase 1 — B1/B2 Freeze maintenance

2026-09-21 JST

**B1/B2の限定修復を完了。全候補の適用判断は引き続きNOT_READY。production未変更。**

前回の[適用準備審査](rephase-1-application-assessment.md)が指摘したFreezeのartifact集合矛盾と承認参照の型不一致を、隔離候補で修復した。旧Phaseの順序を復活させたものではなく、選択した採用経路に必要な接続だけを扱った。B3のreader責任は別に残す。

## 修復候補

限定候補 **f1** は `bf32edf98ba8f605169d7188bbc764de74ee4f6e`、tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`。親はa1 `d38f023ce200619f7f49ce17a348755f05e0e021`、その親はHuman固定production `774dd39a951c9ac3818e83dfffd4c7666efb0a20`。

a1からの変更はruntime 1ファイルと新規test 1ファイル。r2の5ファイルとa1の既存test修正は不変。[修復差分](../notes/rephase-1-freeze/repair.patch)と[全適用差分](../notes/rephase-1-freeze/application.patch)を保存した。独立sparse repository内のreview用commitであり、production branchやreconstruct最終commitではない。

- **B1:** stage validatorを既存schemaの3-artifact集合へ合わせた。`visual-review-record`はCandidateが既に参照するpre-preview VISUALの同じpath/hashに限定する。新しい承認後reviewやGateは追加しない。
- **B2:** `publication_preview`という既知のslotをPublication approvalとして検証する。Human/checkpoint両参照の一致、approved/passed状態、canonical path、実bytes、Candidate/Profile identityを確認し、そのCandidateをartifact集合へ束縛する。他slotは従来のStage Checkpoint型検証を維持する。

schema、承認producer、reviewed-commit照合、Release実装は変更していない。#495/#496のactive revalidation/supersession処理を保持。旧runtime patch全体の移植はしていない。

## Evidenceと独立性

未修正版a1を別Git databaseへコピーし、同じ新規testでB1/B2を個別再現した。B1は余分なvisual artifactとして拒否、B2は承認記録にStage Checkpointの`artifacts`がないとして拒否された。初期設定の失敗ではない。

固定f1に対する**24 testsが通過**した。新規8件、既存stage 3件、agent-control 5件、publication 8件。Weeklyでは実Candidate→stage report→checkpoint→承認→Freeze report/checkpoint→FROZENを接続した。active publication revalidation後のFreeze stage検証、bytes改変、参照不一致、未承認状態、誤った型/visualの拒否も確認した。[原logとidentity](../notes/rephase-1-freeze/README.md)を参照。

fresh-context Sol Workerが新規testの初稿7件を作成したが、継続時に完了reportはなく、rootが確認・第8test追加・実行・候補固定を引き継いだ。runtime authorもrootである。別のfresh-context Astra Auditorが候補作成側から独立して固定差分・source/schema接続・tests/evidenceを確認した。[独立報告](../notes/rephase-1-freeze/auditor/review.md)は限定修復のreviewであり、最終七観点auditではない。

独立reviewの結論は**2ファイル差分にactionable findingなし、B1/B2はこの固定候補と限定Evidenceの範囲で解消**。rootもこの判断を採用した。[Closeout](../notes/rephase-1-freeze/closeout.json)では旧41入力とa1の6ファイルの保持、候補・test・reviewの対応を再確認した。

上流履歴・研究・意味/visual review・Human判断は合成fixture。実validatorを通したことは、実際の出版品質やHuman承認を意味しない。承認は既存low-level producerで生成しており、canonical durable-reviewed-commit Human Gateの新たな全往復実証ではない。新接続試験はWeeklyのみ。Special/Retrospectiveの全Freeze経路、Windows、実Actions、全歴史依存閉包は未検証。FROZEN到達を公開完走とは呼ばない。

## 停止地点と次の判断

B1/B2について修復候補・前後反例・限定回帰・独立reviewを揃えたため、この保守単位を閉じる。前回の広いtest未完了をPASSへ変更せず、今回の24件を全CIとしない。実行時間は記録したが、Human/LLM/review/移行を含む純lifecycle削減は未実測。

採用経路を続ける次の責任は**B3のreader coverage/derivation**。まずemitted proseとreview対象の対応、review済JSONと現在manuscriptの関係を固定baseline上で限定する。全reader再設計、旧patch移植、既存RELEASED版の再生成は既定にしない。修復後も必要diagnostic・同期と新candidateのfresh七観点auditが必要であり、production採用には別のHuman判断が必要。

今回はB3実装へ広げず、次の判断入口をhandoffへ記録した。固定baselineは維持し、新しいmainの照会・追従、production変更/投稿/適用、通常のreconstruct最終commit/Pull/Pushは行っていない。
