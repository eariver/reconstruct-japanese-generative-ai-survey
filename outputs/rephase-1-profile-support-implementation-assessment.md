# Profile/support shared upstream repair — implementation assessment

2026-11-01、Astra author-side判定。**BOUNDED IMPLEMENTATION COMPLETE（qualified source/run composite）**。既存mapのwhole P1–P4を実装・影響検証し、独立implementation reviewと完全配送の適用確認を得た。このunitの**Human Commit Pointで停止**する。

## 1. 正本・判定範囲

- [Packet／証拠入口](../notes/rephase-1-profile-support-implementation/README.md)
- **[Mandatory Astra closeout全文](../notes/rephase-1-profile-support-implementation/astra-closeout-resolution.md)**：実装・run・配送・誤記・原失敗の限定と次task。
- **[独立implementation review WITH FINAL-BINDING＋closeout確認](../notes/rephase-1-profile-support-implementation/independent-final-implementation-review.md)**：作者ではないreviewerの判定。R4七観点auditではない。
- [総工数scope再評価INCLUDING§8](rephase-1-scope-reassessment-20261031.md)：投資順序を維持。技術契約62b14add／契約ROOT021a0d7c／precodeROOTbfb72bf2はbyte-preserved。

Generalが実装と実行、Astraがsource/oracle/scope/evidence reviewを担当した。無条件の汎用Thematic/Retrospective reader必須gateは再開していない。今回の限定完了を品質・全形式対応・採用・実測削減へ拡張しない。

## 2. 実装結果

| 面 | 接続した内容 |
|---|---|
| DM016 | canonical10追加、旧mapping/元label維持、未知typeとDROP予定を新規受付write前に拒否 |
| DM017 ordinary | exact initial3／named-only5→内部導出7、U=initial+root+effective、各(parent,OID)保持、欠落拒否、明示status／意味、closure-first残余制限 |
| Entry parity | 普通runnerが正本、agent-firstはthin delegation。pure互換helpers保持、normal routeのmonkey-patch不要 |
| Screening | package以前のPATH-based root/effective取得、marker/State-DCP/expected pathを別々に束縛。初期DIRECT・初期marker pending・健康なSTAGE_CLAIMED、ENOENT-only不在を保持 |
| DM022 HIGH | full strict LIVE後、最初のCOPY前にactual R/Eとnew-admission判定。adopt write前も再確認 |
| DM022 LOW | pinned COPY→通常DCP/SCP→accepted R/E、Profile/canonical path／record-owned report／retention束縛。required keyword-only PATHs、adopted-full既存3args、EとRの役割分離 |
| 履歴・失敗 | 新規policyをhistorical/idempotent validatorへ混入しない。DM0227はordinary3/5と別。own-epoch/CURRENT、guard/no-overwrite、許容owned-partial failureを維持 |

Shipping変更は6既存runtime files。新runtime module/schema/familyはない。tests/fixtures既存9変更＋新2test modulesを含め、final133比15M+2A。Actual409に対する全継承込み配送は次節の138paths。

## 3. 完全配送と利用可能source

**Actual409/tree8ce＋138paths57M81A／770 intended files（689 available base+81new）。**

Final directory: `notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/`

- `complete-profile-support-409.patch`：SHA256 **`efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e`**、**5247647B**。
- `complete-profile-support-manifest.json`：SHA256 **`634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc`**、**186847B**。
- Applied proof：`.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60`。

完全DIRECT409、旧133/93等を内包。旧patch先重ねは禁止。独立check/apply各0、全138delta＋全770のbytes/size/modesをCAND/GEN/PROOFで照合。GEN whitespace check2／apply5diagnosticsは保存。旧first-package `e0ca796f…` はC-test oracle修正前であり、消さず保存した。

partialDB26309／bulk31466／非同梱runtime・TeXは残る。full hydration/tree-clean／全履歴復元／safe-rerunner認証ではない。普通candidate commitは作っていない。ReportのHIGH/Evidence/patch hash転記誤りはROOT§2が訂正し、実manifestと実file hashが正本。

## 4. 検証と限定

最終証拠は**合算しないsource-bound composite**：ordinary28/28、ordinary affected26/26、DM022 A2 25/25、family/history/consumer affected37/37、Selection／7slot再生成／draft consumer各1/1の独立batch。初期8batch中のC6はoracle修正前で、FINAL complete patchを適用したsource上の**7/7**へ置換した。変更はそのtest1fileだけ、他769一致、runtime不変。全770 pre/post一致、final7は同processのmodule path/hashとrunを束縛。

正当な三research Profilesのupstream、ordinary直接／agent-first実public parity、実R≠Eとshared-OID保持／脱落拒否、ordinaryから実Selection API、DM022両route DIRECT＋Weekly DERIVED・新ID反復訂正・later consumersを検証。真正Human承認ではなくsynthetic fixture。語彙・source-classはclaim truth/publisher/mergednessを自動認定しない。

Ambiguous-primaryは保存された追加[valid-task補足](../notes/rephase-1-profile-support-implementation/primary-binding-verification.md)で正確な拒否を確認した。最初の2DID単一taskはinvalidなleaf probeとして退け、補足は正当な2個のsingle-DID task/packageとprimary mismatchだけを用いる。既存multi-source bindingと実multi-DID graphの別証拠を組み合わせるが、一つの全組合せ実運用とは呼ばない。

初稿code/test誤り、setup失敗、timeout、summary-only raw欠落、loader-probe失敗、hardcoded retention上書き、誤hash／TeX不在誤記をROOTに保存・限定。新env-gated exclusive retentionの実7artifact＋manifestは選択出力だけで、Temp fixture DB／graph全体backupではない。

今回PDF build／heavy全旧matrixは再実行していない。変更上流からSelection／7slot／Draft生成への接続を確認した範囲であり、旧PDF/semantic結果を新sourceへ移していない。品質rehearsal・全必要Specialの正常訂正・実運用総工数は未証明。

## 5. 次のHuman continuation — 具体的rehearsal／R4準備

次の一単位は**既存機能で具体的Weekly＋実需Specialを制作・修正するcapability/品質/費用rehearsal**。汎用reader機構を追加設計するunitではない。

1. 採用対象と必要操作を表にする：topic/period/Profile、初回・通常訂正・機械更新・upstream訂正・失敗再開、実経路/受理窓、制限、不足、外せる仕事と追加費用。四系列Thematicで非四系列／Retrospectiveを代表済みにしない。
2. 利用可能な許可済み資料を使い、具体対象／Rawが不足する場合だけHumanへ必要選択・限定取得を求める。既存capturesの追加network権限を推測しない。対象editionを勝手に決めてfixtureを実需要にしない。
3. 実内容の十分性・選択/欠落・claim-source/date・読者説明・実PDF visualを作者別に確認し、必要Human Gateは真正判断までpending。manual PRIMARY_ONLYの正常訂正は実stage条件で確認し、架空REQUEST_CHANGESやaccepted overwriteで通さない。
4. 既存worklogで各roleの準備・再読・LLM・review・build・repair・Human・移行/二重保守を記録。欠けた費用はUNKNOWN。改善が見えないなら追加機能ではなく投資/責任範囲を再判断する。
5. その対象のblockerを解消してから一つのexact候補へ固定し、fresh独立七観点audit R4→Human限定採用R5→実測効果/旧作業除去R6。今回のcomponent PASSでauditを代用しない。

新しいcapability/authority/契約gapが判明したらAstraへ具体箇所・最小代替・費用を返し、scopeを自動拡張しない。これは最後の予定済み機能実装のcloseoutであり、重大欠陥への対応放棄ではない。

**WholeNOT_READY / step4B3OPEN / audit未開始 / DM021+022OPEN / quality-adoption-savings OPEN。通常Commit/Push・Production採用はHuman-owned。Commit readbackなし。Human Commit Point、次unitを自動開始しない。**
