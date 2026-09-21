# J-GAS reconstruction — Re:Phase 1 continuation

更新: 2026-09-21 JST

状態: **B3境界設計・限定実験完了 / B3実装未着手 / f1不変 / 全候補NOT_READY / production未変更**

## 最新の継続点 — B3設計後

[B3評価](../outputs/rephase-1-reader-boundary-assessment.md)、[実装契約](../notes/rephase-1-reader/contract-decision.md)、必要時[Evidence](../notes/rephase-1-reader/README.md)を起点にする。以下のB1/B2節とa1記録は以前の判断として保持。

Weeklyのreview projectionにはlede以外の漏れもある。固定f1実関数の限定実験で、10変更（本文7箇所・日付/期間・citation identity）がTeXを変えてもprojectionを変えず、既存covered項目の2対照は両方を変えた。全renderer入力をreviewへ束縛する試作は不一致を拒否するが、内部注記だけで再review identityを変えるため不採用。prototypeをCoreへ移植しない。

採った設計方向はcomplete reader inputからの単一生成とGateでの独立derivation検証。stageが選んだexact Manuscriptにも接続する。direct-primaryは別経路として証明し、同じ本文を二度reviewする義務を安易に追加しない。bibliography/style/supporting sourceと制限付き非reader provenanceの分担、LONGFORM/Retrospective callerは未確定。ここを既存責任へ割り当ててから、f1隔離後継でinput/renderer/Gateを一貫して修復する。単一field修正をB3完了としない。

fresh Sol Workerはsource/callsiteを調査。fresh Astra Auditorは初期design reportを保存後、利用上限で停止したため、root修正後の承認とは扱わない。初期指摘はschema外注記とexact manuscript接続の不足で、rootが両方対応。別のfresh Sol Auditorによる[独立対応確認](../notes/rephase-1-reader/resolution-auditor/review.md)で2点ともdesign/evidence上の対応済みを確認した。各reportの入力hash/scopeを保持し、B3実装受入にはしない。実研究・semantic/Human review、全Profile完走、七観点PASSはいずれも未証明。

B3 candidateは作成しておらずf1と旧Evidenceは不変。通常のreconstruct最終commit/Pull/Push、production変更/投稿/採用、新main照会は行っていない。次は上記のsupport/provenance/caller契約と限定後継実装。投資が広がるならr2の便益と全体目標から採用経路を再比較し、Core全体修復へ自動拡張しない。

## 前回の継続点 — B1/B2修復後

最初に[Freeze修復判断](../outputs/rephase-1-freeze-assessment.md)、[独立報告](../notes/rephase-1-freeze/auditor/review.md)、必要時[Evidence](../notes/rephase-1-freeze/README.md)を読む。以下のa1 application review記録は前回の判断経緯として保持する。現在の候補/次作業はこの節を優先する。

f1 `bf32edf98ba8f605169d7188bbc764de74ee4f6e`、tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`、親a1 `d38f023ce200619f7f49ce17a348755f05e0e021`。Human固定production祖先`774dd39a951c9ac3818e83dfffd4c7666efb0a20`を維持。a1からstage validatorと新規testだけ変更し、元6ファイル不変。隔離fixture `/tmp/jgas-rephase-freeze-b1b2` は専用Git database/inert origin/alternatesなし。保存したpatch/manifestを正とし、消失し得る`/tmp`へ依存しない。

B1は既存schemaの3-artifactとCandidate pre-preview visualのexact path/hashへ接続。B2は既知approval slotだけをtyped approvalとして完全検証し、承認されたCandidateを束縛。schema/Gate/承認producer/Release/reviewed-commit規則の変更なし。#495/#496 revalidationを保持。

未修正版a1で同じtestがB1/B2の意図した理由で個別失敗し、固定f1では24 tests通過（新規8、stage 3、agent-control 5、publication 8）。Weeklyで実stage/report/checkpoint経由FROZENを確認。active revalidationはFreeze stage検証まで。研究/review/Humanは合成fixture、low-level承認producer使用、canonical durable Human Gate全往復やSpecial/Retrospective完走・実公開の実証ではない。fresh-context独立Auditorの限定reviewは七観点auditではない。

この保守単位を閉じる。次に採用経路を進めるならB3 reader coverage/derivationの最小責任境界を扱う。B3実装は今回未着手。全CI未完了/Windows/実Actions/全Profile/歴史閉包/純削減は未解消。修復・同期・必要diagnostic後の新candidateにはfresh七観点auditが必要。production採用は別Human判断。通常のreconstruct最終commit/Pull/PushはHuman担当。

## 前回a1 application reviewの記録（以下の旧「次」は上記で更新済み）

## 再開入力

1. 本handoff。
2. [最新の適用審査判断](../outputs/rephase-1-application-assessment.md)。
3. [独立Auditor報告](../notes/rephase-1-application/auditor/review.md)、必要時のみ[Evidence一覧](../notes/rephase-1-application/README.md)と[diagnostic disposition](../notes/rephase-1-application/diagnostic-disposition.md)。

固定production baselineは`774dd39a951c9ac3818e83dfffd4c7666efb0a20`。明示rebaselineまで新しいmainへ追従/照会しない。旧reconstruct開始`ec6a502e`は歴史値。今回観測reconstruct HEADは`098b05a2af44734549b305ba0ccf4dd31472398f`で、通常の最終commit/Pull/PushはHuman担当。

必要なGit/Git-aware検証は許可済み。Humanはr2 application reviewとWorker/独立Auditorを許可した。production変更・投稿・適用・採用の権限とは別であり、今回それらを行っていない。fixtureはinert origin、専用Git database、alternatesなし。追加agent作業も現在の具体的scope内で扱う。

## 候補

以前の[5-file r2](../notes/rephase-1-connection/candidate.patch)は不変。限定設計/root接続/独立review/単体/限定Git-aware統合の結果は元のscopeで保持する。

今回はproduction実固定commitを親とする独立sparse repositoryを作成。完全treeは維持するが、全sources/surveys/historyを検証したものではない。

- 元r2 review commit: `46472e41e353de56685e737fc91e85fcc2005312`。
- 適用候補 **a1**: `d38f023ce200619f7f49ce17a348755f05e0e021`、tree `960585ef29b55567efdf08901de489e4f3bb8fe5`。
- a1はr2本体5ファイル＋`tests/test_survey_findings_v2.py`だけ。[差分](../notes/rephase-1-application/application.patch)、[manifest](../notes/rephase-1-application/application-candidate.json)。

旧testが外すべきlive候補/edition statusを要求していたため、Workerが責任分離へ合わせる変更を提案しrootが採用した。歴史Finding/Repair Set、released版不変性、production scope、七観点/Human Gateの検証は保持。Gate/schema/loader/Git照合の弱体化はない。

## 独立審査

fresh-context Sol Workerは前提調査とtest修正後、利用上限で停止。rootが後半実行を担当。fresh-context Astra Auditorは候補作成に参加せず、規範・差分・source/schema接続・原反例を独立に読んだ。旧限定reviewの再利用ではない。

**六ファイル差分にactionable defectなし。ただし全候補はNOT_READY。**

1. **B1 Freeze集合矛盾:** schema-required `visual-review-record`をstage validatorがextraとして拒否。report/checkpoint集合一致も必要。
2. **B2 型不整合:** Publication approvalをcheckpoint provenanceへ置くproducerと、全参照をStage Checkpoint型で読むconsumerが衝突。
3. **B3 reader対応関係:** `frontmatter.lede`のprojection漏れと、review済JSON/現在primary manuscriptの対応検証不足。

すべて固定baselineに残る問題で、a1は関係実装を変更していない。関連13入力のhash不変を独立確認。B1/B2は接続したsource/schema矛盾、B3は現source＋保存済み関数/projection反例。全workflow/Human Gate突破やRELEASED版の無効を証明したものではない。

最終七観点auditの前提が満たせないと判断した**準備審査**であり、七観点auditは始めていない。後日のroot試験・closeoutをAuditorの実行/署名としない。

## 実行結果と残件

- Python 3.12.14で405 Python compile、79 config/schema JSON、16固定Release manifest parseが通過。
- corrected WU-011 testはa1の広い上流診断logで通過。
- 全件診断は再開時process/完了recordなし、logがtest途中で終わる。停止原因不明。**全CI PASSとはしない。**
- sparse不足のRelease manifest 2件とSP001 skipを、固定treeに照合した41 files / 92,553 bytesで補完し、対象3 testsだけ再実行して全通過。
- W34旧commit fixture skip、上流明示legacy skips、広い試験の未完了、実Actions/全Profile公開品質/全歴史依存閉包は残る。

実行fixtureはUbuntu `/tmp/jgas-rephase-application-r2`、Pythonは `/tmp/jgas-rephase-application-venv`。root input seal/Auditor copyはEvidence参照。`/tmp`は消失し得るのでmanifest/patch/scriptsを起点にする。pycacheと中断testのtemp directoryはfixture debrisでありcandidate差分ではない。reconstruct Gitへfixture objectsを生成していない。

pipeline契約hashは3文書の変更で変わる。quality/Profile hashやversionラベルが同じでもidentity-preservingとは言わない。新規実行へ適用する案を基本とし、既存State/Profile/承認/Released historyを付け替えない。実migration・純lifecycle削減は未実証。

## 次の判断面

**今回の準備審査は完了し、a1を保留。** 同じ成功testや独立レビューを再実行しない。全件診断の残りを完走しても今回のblockerは消えないため、否定的判断に必要のない追加検証は止めた。後の採用検証を免除しない。

採用経路を再開する次の保守単位は、B1/B2のFreeze契約・typed approval接続の最小修復が妥当。B3のreader coverage/derivationは別責任とし、Freeze修復だけでreadyとはしない。旧patch一括移植や全reader再設計は既定にしない。新candidateには必要diagnostic・authority同期後のfresh fixed-head七観点auditが必要。production採用はさらに別Human判断。

旧Phase順序を復活させず、現在選んだ経路に必要な欠陥だけを扱う。全manual、dashboard、新resolver、常設telemetryへ広げない。reconstruction全体は未完了。
