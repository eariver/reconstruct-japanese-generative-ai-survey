# Re:Phase 1 — r2 production application review

開始: 2026-09-16 JST / closeout: 2026-09-21 JST

状態: **適用準備審査はNOT_READY / r2本体維持 / 最終七観点audit未開始 / production未変更**

## 判断

**r2の設計は保持するが、production採用には進めない。** 必要だった既存testの修正まで行い、独立Auditorによる適用準備審査を完了した。6ファイル差分の範囲では新たなactionable defectは見つからなかった。一方、固定baselineに残るFreezeとreaderの問題が全候補の受入条件に関係するため、七観点PASSや採用可能とは認定しない。

これは「r2が既存問題を起こした」「既存のRELEASED版が無効」という判断ではない。限定差分の妥当性と、全候補の通常経路を認定できることを分けた。[独立報告](../notes/rephase-1-application/auditor/review.md)をrootも採用する。

## 用意した適用候補

Human固定production baseline `774dd39a951c9ac3818e83dfffd4c7666efb0a20`を直接の親とする、独立Git repository内の候補を作成した。今回のcommitはproductionの完全なtreeを継承する。ただしworktreeはsparseであり、全archiveや歴史依存閉包を検証したわけではない。

- 元の5-file r2: `46472e41e353de56685e737fc91e85fcc2005312`。以前のr2候補ファイルとhash一致、別refに保持。
- 適用候補 **a1**: `d38f023ce200619f7f49ce17a348755f05e0e021`、tree `960585ef29b55567efdf08901de489e4f3bb8fe5`。
- a1は**r2本体5ファイル＋既存test 1ファイル**。[適用差分](../notes/rephase-1-application/application.patch)、[候補manifest](../notes/rephase-1-application/application-candidate.json)。

広い回帰検証で、既存WU-011 testがauthority文書内の`PRE-AUDIT CANDIDATE`やW34の現在status記述を要求していると判明した。testを規則・状態の分離に合わせ、歴史Finding/Repair Set、genericなreleased版不変性、production scope、七観点audit、Human Gateのassertionを保持した。loader、schema、Git照合、Gateの検証は緩めていない。

## 独立性と結果

Workerはfresh-context Sol、高reasoningでCI前提調査とtest修正を担当。rootが修正を確認して候補化した。Workerはその後利用上限で停止したため、後半の実行はrootが引き継いだ。

Auditorは別のfresh-context Astra、高reasoningとし、候補・test・検証harnessの作成に参加させなかった。実差分、規範、source/schema、反例の原記録を独自に確認し、候補に書き込まず別reportへ記録した。旧r2限定reviewのPASSを転用していない。

| 独立確認した既存問題 | 受入条件への影響 |
|---|---|
| **B1:** Freezeのschemaは`visual-review-record`を要求し、stage validatorはextraとして拒否。report/checkpoint集合一致も必要 | 通常のvalidated Freeze transitionで両契約を同時に満たせない |
| **B2:** Publication approvalをcheckpoint provenanceへ保存するproducerと、全参照をStage Checkpoint型で読むconsumerの不整合 | approvalのtyped authorityを保持したまま次stageを検証する経路が失敗する |
| **B3:** reader projectionの`frontmatter.lede`漏れと、review済JSON/現在primary manuscriptの対応検証不足 | exact reader source全体のsemantic reviewを認定できない |

B1/B2はsource/schemaの接続をAuditorが再確認した。B3は現source確認と、同じ固定版の保存済み関数/projection反例を併用した。関係13入力のhash不変も確認。**新しい全workflow突破・全号品質不良の実証ではない。** 行番号、因果関係、Evidenceの限界は独立報告に記載した。

最終auditの前提を調べる準備審査であり、七観点auditは開始していない。どの観点にも最終PASSを付けず、後日のrootによる残件検証をAuditor自身の実行・署名とも扱わない。

## 検証と未完了

- Python 3.10初期診断で、上記test不整合と、固定CoreのPython 3.12構文に由来するimport errorを確認。初回からgreenだったとしない。
- 隔離Python **3.12.14**と固定版の直接依存を用意。**405 Pythonファイルのcompile、79 config/schema JSON、16固定Release manifestのJSON parseが通過**。
- a1の広い`test_*.py`診断では、修正したtestや多数の上流testが通過したが、再開時にprocessも完了recordもなく、logがtest途中で終わっていた。停止原因は未確定。**全件試験は未完了であり、全CI PASSではない。**
- sparse不足によるRelease manifest 2件のfailure/errorとSP001 fixtureのskipは、固定treeに照合した41ファイル、92,553 bytesを補って、対象**3 testsのみ再実行し全通過**。データ書換え・test弱体化ではない。
- 古いW34 commit fixtureのskip、上流明示legacy handoff skips、広い試験の未完了部分は残る。実Actions、全CI系列、全Profile公開完走を認定しない。

[Diagnostic disposition](../notes/rephase-1-application/diagnostic-disposition.md)と[Evidence一覧](../notes/rephase-1-application/README.md)に原記録を整理した。具体的blockerが確認済みのため、今回の否定的準備判断を変えない残りの広い試験は止めた。後の採用時に必要な検証を免除したわけではない。

## 契約・既存版・費用

68個の固定入力と実`contract_identity()`で比較した。3文書がpipeline契約対象なので、そのhashは変わる。quality/Profile hashとversion文字列は変わらない。a1のtestはaggregate外である。**文書中心の変更でも契約同一性は維持されない。**

将来採用する場合の基本は新規実行への適用とする。既存State/Profileの初期契約、旧承認、index/session、Candidate/PDF/Freeze/Releaseを付け替えず、released版を移行実績のために再生成しない。in-flight版には既存のreview済Core統合・影響境界再検証・current tool/contractを束縛する新checkpoint規則を適用する。今回edition移行は実行していない。[適用scope案](../notes/rephase-1-application/application-scope.md)に整理した。

除去対象はlive statusコピーの更新義務である。原記録探索、規範読解、独立review、CI、Human、migration等への費用移動を含む純削減は未実測。r2の便益のために既存Core全体の修復を無条件に引き受ける判断はしない。

## 停止地点と次の入口

**今回のapplication readiness reviewを閉じ、a1を保留する。** 既存blockerを別のCore保守判断へ分離し、旧runtime patch移植、reader全面再設計、既存版再生成、audit規則の緩和には進まない。

採用経路を再開する次の保守単位は、B1/B2のFreeze契約・typed authority接続の最小修復が妥当。reader B3のcoverage/derivationは別責任として残し、Freeze修復だけでreadyとはしない。修復・同期・必要diagnostic後の新candidateに対し、最初からの七観点auditが必要。これは旧Phase順序の復活ではなく、今回選んだ採用経路で確認した依存関係である。

production採用/投稿/dispatch/State変更、最新main照会・rebaseline、通常のreconstruct最終commit/Pull/Pushは行っていない。固定SHAのread-only取得、独立fixtureのGit操作、reconstruct分析成果更新だけを行った。全体reconstructionは継続中。
