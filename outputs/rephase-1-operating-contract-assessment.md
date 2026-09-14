# Re:Phase 1 — 運用規則と現在状態の分離案

日付: 2026-09-15 JST  
状態: **限定設計・offline検証完了 / 5-file候補 / 独立review・production接続・採用は未実施**

## 1. 判断

**現在状態の手書き二重管理を外す案は、限定した設計として成立する。必読規範全体の統合・廃止には広げない。** 固定baselineに対する[5-file候補差分](../notes/rephase-1-contract/candidate.patch)を作り、文書側の記録義務と初期化helperの両方を変更する案を揃えた。

外すのは、規範文書内のcurrent main/保守candidate状態と、execution index内のlive lifecycle・State hash・Gate status・Candidate/PDF・next action・final dispositionのコピー。正式なState、approval、review history、sessionの時点付き記録は残す。表示を一枚追加して全ての手書き更新を残す案ではない。

一方、authority/overlay/governance等の必読義務は保持する。今回、そこにある固有の規則まで安全に別の唯一の文書へ集約できたとは実証していない。「資料が短くなった＝review/read費が下がった」とも扱わない。最初の全体案より狭いが、消せる更新義務とその発生源まで具体化したため、ここを一単位の終了面とする。

production baselineはHuman指定の`774dd39a951c9ac3818e83dfffd4c7666efb0a20`から変更していない。以後も明示rebaselineまで固定し、mainの追跡は不要。今回Git操作・production checkoutの参照/変更・remote ref照会は行っていない。

## 2. 調査で追加した範囲と短い契約

前回の四資料に加え、固定版の`execution-record-policy.md`と`survey_execution_record_v2.py`を読んだ。policy §4はindexにcurrent lifecycle/Gate/Candidate等を記録し、状態変更ごとに更新することを要求していた。helperの`initialize()`もcurrent State hash/lifecycle/next actionとGate statusを文字列へ埋め込む。一方、`validate()`は見出し、Profile identity、Stateへの参照等を確認するだけで、コピーしたcurrent値の一致を検証しない。

そのため、indexの表示だけを変えると記録義務が残り、文書だけを変えると新規indexに同じコピーが生じる。**policyとproducerを一組で変える**ことが必要と判断した。上流のこれらの処理を修正/実行したという意味ではない。

候補が提案する契約は次のとおり。これは本評価の説明であり、新しいproduction必読manualではない。

1. **規則は規範へ、変動する事実はその正式記録へ置く。** 文書のStatus欄でbranch/PR/editionの現在状態や承認を宣言しない。
2. **indexはrun contextとnavigationを持つ。** 開始時baseline、目的、transport/defect/session参照は必要。Stateだけの変化ではindexのlive値を更新しない。
3. **active approvalと過去reviewを別に読む。** activeはState provenance。review indexにある最大rNのAPPROVEDを採用しない。REQUEST_CHANGES時に旧承認を復活させない。
4. **snapshotの読解は実行可否の認定ではない。** 入力bytes、型/直接参照の確認、未確認の依存閉包・reviewed commit・品質を区別する。
5. **既存のreview・Human Gate・実行検証・監査は残す。** session終了時のState/next action記録は時点付き履歴として残し、今後ずっとcurrentだと読ませない。

## 3. 義務・情報の移動先

| 固定baseline内の記述・義務 | 候補での処遇・唯一の事実の参照先 | 残る仕事 |
|---|---|---|
| authority冒頭/§1のmain SHA、保守branch/PRとpre-audit状態 | 規範から削除。選択snapshotと名前付き保守PR/review record。旧状態は固定版URLで参照 | 保守candidate自体の記録・審査は必要。状態が不明ならunknown |
| authority §4の「修復実装済み」「active findings」等の分類 | document roleへ変更。規範の優先順位/リンクは保持 | role/indexの構造が変わる時の更新は残る |
| authority §11のFIXED/DEFERRED一覧とcurrent修復状態 | 名前付きFinding/Repair Setとreviewへ。旧dispositionは固定版に保持 | 保留を再開する指示でも修復認定でもない。Series/網羅matrixを新設しない旨を保持 |
| authority §13の特定PR・edition状態/対象branch | 時点依存説明を履歴へ。shared Coreとeditionの分離、scope明示、immutable releaseを保持 | 現candidateごとのscopeと許可の確認 |
| overlay冒頭/§14のmaintenance候補・過去PASS列挙 | 固定版への歴史参照。全候補変更後の七観点auditとpost-integration validationは残す | 独立audit/CI/実運用validationは削減していない |
| bootstrap §2/§13の再開・記録 | Stateとtyped参照を読み、indexはnavigationとして読む。既存の必読リストは維持 | 同じ規範・source・独立reviewを読む義務 |
| record policy §4のlive lifecycle/stop/Gate/Candidate/finalコピー | State、Stateが指すcheckpoint/active approval、machine review index、最終sessionへ | session追加・defect/transportの発生などnavigation変更時はindex更新 |
| record policy §9のlatest review/終了時記録 | latest rNは履歴。activeはState。終了時の状態はsessionに一度記す | 過去reviewの参照・rN整合・記録の構造検査 |
| initializerのindex f-string | live値を生成せずState/機械記録への参照を出す。initial dispositionはsession側へ移す | Profile identity、必要見出し、実行記録ディレクトリ/validatorは維持 |
| W34の既存index | production差分に含めない。固定版の誤誘導例として使用 | W34を再生成しない。古いindexの主張からStateを推測しない |

以下の規則群は元の節をそのまま保持した。差分の削除箇所に意味上の漏れがないかはrootで確認したが、非著者の判断ではない。

| 規則群 | 元の規定位置・候補での保持 |
|---|---|
| role責任、継続進行、独立source/negative-space/compression review | authority §2/5/6/9/10、bootstrap §1/7/8、governance（差分対象外） |
| Humanの二Gate、exact reviewed commit、immutable approval、REQUEST_CHANGES | overlay §7/8/11、bootstrap §6/8/10/11、record policy §3/6/7 |
| Source/Raw、active Screening/Evidence、Supplement、reader boundary、quality | authority §7/8、overlay §5/10、bootstrap §7/9/12。型付き表示で代替しない |
| Weekly/Period/Thematic/Foundations・Publication Profileの直交性 | authority §6、overlay §3/4/12、bootstrap §4。Period/Foundationsの実行は今回未検証 |
| direct CLI/bridge trust、分離した実行identity、production/Core境界 | overlay §6/9/13、bootstrap §3/5、record policy §3/5/8。transport詳細の別文書も存続 |
| final audit・歴史・既存caller互換 | authority §12/13末尾、overlay §14末尾、bootstrap §14、record policy §10 |

機械照合では4文書の**42節が変更前後で全文一致**。これは保護した範囲の確認であって、編集した節の意味的正当性や全repositoryの規範整合を証明しない。authorityとoverlayの優先関係、別文書に残る古いStatus、bridge説明の歴史的差異まで解消したとは主張しない。

## 4. 表示実験と確認結果

[表示実験コード](../notes/rephase-1-contract/state_view.py)はreconstruct-onlyのoffline probeで、production向け新validatorではない。JSON Schemaは固定版を使い、Stateのraw hashを外部から指定したanchorへ照合する。Stateを選ぶためのdirectory scan、mtime/latest推測、Git、network、production module importは使わない。artifactを保存・承認・advanceする機能はない。

| 例 | 観測した表示・拒否 | 証明しないこと |
|---|---|---|
| 実W34 snapshot | RELEASED / next null。古いindexを変える/無くしても表示不変。Preview pointerは専用approval型で読める | 現行全stage完走、公開assetやPDFの再確認 |
| 実SP001 snapshot | RELEASED、THEMATIC/LONGFORM、OPEN_HISTORY_AS_OFを保持。WeeklyのROLLING_WINDOWへ潰さない | 全Special/Period/Foundationsの運用一般性 |
| State anchor不一致 | 保存事実の表示を止める | origin/commitの外部信頼性。anchorの正当性は入力捕捉が担う |
| active approval欠落/bytes drift/Stage型への差替え | MISSING/HASH_MISMATCH/TYPE_OR_SCHEMA_MISMATCH。過去承認へのfallbackなし | Candidate/PDFとの全推移的結合 |
| 別edition Profile、path traversal | ISSUE_MISMATCH/UNSAFE_PATH | あらゆるファイルシステム競合・脅威への耐性 |
| publication-local REQUEST_CHANGES fixture | Previewはpending/NOT_ACTIVE、Architecture approvalは別に保持。履歴r2の要求を表示 | 実Coreのrevision操作や当時のStateを再現したこと |
| cross-gate fixture | Architecture pendingと歴史APPROVEDを別表示。最新承認からactiveへ復帰しない | 新Human decisionや正しいfull transitionの成立 |
| review indexの重複rN | 不整合を表示し、そのGateのlatestを黙って選ばない | review chain全依存のvalidation |
| initializerテンプレート | live値のコピーが消え、必要見出しとProfile identityが残る。initial dispositionはsessionへ | initialize()/validate()全体の実行、CLI接続、Git-aware tests |

**13群のoffline checkを完了。** [検証結果](../notes/rephase-1-contract/checks.json)、[実例/fixtureの区別付きJSON](../notes/rephase-1-contract/examples.json)、[navigationのテンプレート例](../notes/rephase-1-contract/navigation-template-example.md)。JSONには全例で`execution_admission=NOT_EVALUATED`を付け、Stateに保存されているimplementation/contractと調査snapshotを分けた。W34の保存target_gateがArchitectureでもnext_action=nullを勝手にArchitecture再開へ変換しない。

fixtureは実記録を参考にした表示用変更で、当時のStateの復元でもCore遷移の出力でもない。cross-gate REQUEST_CHANGESは明示した合成記録。実Human/独立reviewの権限として使わない。

## 5. 何が減り、何はまだ分からないか

| 場面 | baselineの要求/生成 | 候補の要求/生成 |
|---|---|---|
| Stateだけが進み、参照path/navigationは不変 | indexのcurrent値を合わせる要求がある | 既存session/machine記録に残す。indexのlive値更新を要求しない |
| 新session、Grok result、defectが追加 | 記録とindex更新 | 必要な記録/新しい参照のindex追加は維持 |
| main/maintenance candidate状態が変わる | 規範文書のcurrent SHA/候補状態も同期する形 | 名前付きsnapshot/PR/review recordで読む。規範本文にコピーしない |
| session再開 | 複数のcurrent説明を読み、Stateとの不一致を解消 | Stateとtyped参照から事実を読む。必読規範そのものは同じ |

削除対象は明確だが、baselineで要求された全更新が実際に毎回行われていたわけではない。W34の古いindexは未更新の例でもある。したがって「全遷移回数×更新時間」を削減量にしてはいけない。減らせるのは不要な更新義務・古い説明の誤誘導と照合の一部で、実際の作業差は未計測。

増える費用は、今回の調査/差分/表示probe、編集節の独立review、既存helper接続/回帰、規範変更によるcontract identity/監査/移行の評価である。実運用で毎回もう一つの全validatorや生成済みsummary正本を維持するなら、この案の便益を損なう。

**probeはそのままproductionへ入れない。** 実運用の表示が必要なら既存Coreのread-only resolver/診断へ寄せ、同じauthority解決を二重実装しない。この候補は、人/agentが既存の正式記録を直接読む場合でも成立する記録規則の変更であり、新表示サービスの完成を採用の絶対前提にしない。ただし原記録への探索負担が増えるなら、総仕事が減るという主張は撤回する。

## 6. 移行・採用と、今回の停止

候補は5ファイルに限定し、config/schema/State/approval/Candidate/PDFやW34/SP001の実indexを変更しない。helperの変更はindex/sessionテンプレートだけで、`_load_state`、`_load_profile`、`validate`のASTは同一。これをfull execution互換PASSに読み替えない。

authority/overlay/record policyはbaseline configのcontract対象であり、helperは共有実装である。productionへ採用する場合は、必要な審査/CIと既存のcontract再検証規則が適用される。過去Stateのcontract hashや承認を新しい値へ書き替えない。旧bytes/旧契約での歴史検証を残し、既存released editionを「移行実績」のために再生成しない。

切戻しは未採用候補の破棄なら容易。採用後は通常のCore変更として扱い、変更後の記録を消したり古い承認を付け直したりしない。旧index見出しを残したのは既存の構造validatorとの不要な互換変更を避けるためで、「Current authority」の下にlive値があるという意味ではない。

**次の投資候補は、この差分の接続可能性を限定して確認すること。** 既存execution-record tests/callersがlive値のコピーに依存していないか、初期化と再開でnavigationが不足しないか、編集節が規範を落としていないかを対象にする。独立reviewはこの具体差分に対する新しい明示許可が必要で、今回実行していない。現時点のGit操作禁止下ではGitを要求する実行試験を起動しない。

今回はその手前で、保護した規則・除去対象・prototypeでの表示/拒否・残る接続条件を揃えて止める。全manual統合、status dashboard、常設cache、新stage/新Gate、旧Freeze修復へ自動拡張しない。ここまでの限定成立は全体reconstructionの完了、独立品質認定、production採用、純lifecycle savingsではない。

取得・生成・試験は全て固定版とreconstruct内の一時/候補ファイルに限定した。Gitコマンド、GitHub Git/ref API、main追跡、production実行/変更、外部投稿、追加agentは行っていない。手順・初期setup修正は[Evidence](../notes/rephase-1-contract/README.md)に記録する。
