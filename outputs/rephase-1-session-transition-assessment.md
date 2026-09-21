# Re:Phase — next-session preparation

2026-09-21 JST. **切替準備完了。実装・test executionは開始していない。B3 OPEN、f1不変、全候補NOT_READY。**

## 今回の判断

Human指定のDeferred Maintenance Summaryを後発read-only Evidenceとして取得した。取得時mainは`f85539c31a079ab7a7fa86185f3cbb0fcad0485a`、Summaryが記すlast-reviewed mainは`0a0b0747...`。Re:Phaseのproduction baselineは引き続き **`774dd39a951c9ac3818e83dfffd4c7666efb0a20`**。取得元・blob/hash・時刻と原文は[保存packet](../notes/rephase-1-session-transition/README.md)にある。リンク先の一次defect/Issue/PRや後発codeを取得したものではない。

全15項目を[採否・再確認時点の表](../notes/rephase-1-session-transition/deferred-intake.md)へ整理した。取り込む時期は**今は計画/acceptance制約、実装修復は必要な単位ごと、全体audit前には関連未解決項目のdisposition確認**とする。全backlog実装や定期main追従は選ばない。

特に次の区別を維持する。

- DM-002はB2を補強する後発報告だが、f1の隔離修復をproductionのCORE_FIXEDに変えない。
- DM-001はprofile-aware Freeze helperの別問題でB1と同一ではない。DM-003のprovenance completeness、DM-004のRelease workflowもf1の24件PASSで閉じない。全application path認定前に個別判断が必要。
- DM-014のindex staleはr2の責任分離に関連するEvidence。production側のrefresh義務案をそのままreconstructへ移植せず、コピー義務を外すr2案を維持する。既存production policy・履歴を今回変更しない。
- Reader/意味/引用/時間/表示の項目はB3のinterfaceとacceptanceを補う。source intake、reviewer認証、chronology validator等のgeneric修復を自動的に現在scopeへ入れない。

## 次に実装する単位

[Implementation plan](rephase-1-implementation-plan.md)で、まず **Increment A: exact stage-selected Reader Manuscript admission**を独立した部分修復にする。これはB3の既知接続欠陥であり、全IRや全Profile設計が固まるまで着手不能にする必要はない。一方で、これだけをB3完了とは呼ばない。

その後、complete reader inputと単一生成、Gate作成/再検証のderivation、bibliography/style/supportと制限付きprovenanceの責任を一貫して実装する。Direct-primaryの実行証拠とSpecial/Retrospectiveの未証明範囲を混同しない。段階的な候補、negative witness、影響のある既存tests、scope停止条件、Astra reviewと独立review、全体auditとの分離をplanへ定義した。

Human指定の新役割分担をAGENTSへ反映。**Astraはarchitecture/計画/task definition/diff・Evidence review/修正判断、コードとtest executionはCo-Worker。** 単純な定型作業で十分ならLuna、B3のCore authorityや複雑なnegativeはSol。WorkerのPASSだけでは採用しない。利用上限時もAstraが実装・testを通常業務として代行する運用には戻さない。独立Auditor/七観点auditはこのroot reviewと別である。

## Durable contextの整理

現在のhandoffを短く書き直し、最初のtask、候補identity、baseline/権限、Summaryの位置付け、未完了の範囲を一つの入口にした。旧AGENTS/handoffは移行packetへ原文保存し、過去の判断を消していない。原則として次セッションはhandoff＋planだけでdispatch判断でき、必要箇所のEvidenceへ降りる。

[Restart context](../notes/rephase-1-session-transition/restart-context.md)には、実path/runtime、`/tmp`消失時の固定SHA＋durable patch復元、既存scriptを無条件再実行しない理由、GitDB分離、既知環境失敗、初期B3 witnessの限定、review停止/修正確認の範囲を記録した。旧root実行実績を今後のrole permissionと誤読しないことも明示した。

前回までの重要contextは、現時点の復帰判断に必要な形でdurable化できた。巨大な会話履歴や生きたsubagentを前提にしない。fresh readerによる入口確認は文書の再開性確認で、implementation auditや七観点PASSではない。

## 停止地点

本セッションは文書・Evidence取得・計画・引継ぎのみで終了。新candidate、実装patch、test実行、production変更/採用/投稿、通常の最終commit/Pull/Pushは行っていない。

次セッションは新Human指示とworkspace status確認後、plan末尾のtaskをfresh Solへ渡す。成功済みf1 testsの再実行、全旧chat/notes再読、current main再取得からは始めない。全体のNOT_READY、B3未修復、最終七観点audit未開始は維持する。
