# Phase 4-F — 日時claimのsource対応と修復地点

日付: 2026-09-13 JST

状態: **ONE SOURCE-JOIN TRACE COMPLETE / PREVENTIVE AUTHORING CHANGE IDENTIFIED / NO ADOPTION**

## 1. 結論

**Grokの日時を記したDailyX記録は既存authorityの入力に存在した。参照が消えた場所は、canonicalの表現力ではなく、compact入力とCard生成の経路だった。** 必要な記録を探す仕事を繰り返す前に、既存のstatement別source対応を途中で落とさない著述経路を検討すべきである。

accepted taskが持つDailyXのhash/import provenanceは実bytesに一致し、CoreにはそのSOCIAL sourceを`src-1`として扱う既存経路がある。一方、手書きoverrideと実compact recordはprimary supplementだけを選び、共通helperはその一つのsource listを全claim・limitation・verificationへ一律に付ける。actual inputからaccepted Cardを関数単位で再現できた。DailyXを選択に追加するだけでも、全statementに両sourceが付くため、statement別の対応は復元されない。

既存Card欄で参照を分ける未採用specimenを作り、schemaとlocal source bindingを検査した。**新schema、別の意味store、追加ownerは不要**。ただしsource対応の修復が、全Cardの意味品質・日時の独立確認・full canonical admission・lifecycle純減の実証になったわけではない。

既存Sol reviewはこのchronologyを限定付きPASSとして扱っていた。今回の原X取得403を理由に、それを自動的にPARTIALへ下げたり、原X HTTP保存を全件の新要件にしたりしない。既存の保証水準を維持することと、今回rootが独立に確立できた範囲を区別する。

## 2. ScopeとEvidence

[観測](../notes/phase-4f/observation.json): main `658ae823987431e1f1098243dc2f88cfc0d4864a`、W34 `f50d229162b7402c504c0978f72dab4b33052f5e`。4-E更新時から不変。PR #488のbib修復は既にmain/W34にあり、重複改修しない。Candidate/Stateの状況は[4-E §6](astra-phase-4e-canonical-rendering-assessment.md#6-途中push後のcurrent-reality反映--2026-09-13-jst)の固定ref説明を保持する。

対象は`evidence:2026-W34:589f97e8aee10bd1` / `claim-2` / Card SHA `c398b532b7d0c047154176eb579e9931d9c025b313649307f5585cddb47781c1`だけ。

- [入力identity](../notes/phase-4f/inputs.json)、[traceと名指しbinding](../notes/phase-4f/trace-result.json)。
- [raw抜粋](../notes/phase-4f/source-excerpts.md)、[未採用Card specimen](../notes/phase-4f/card-corrective.lab.json)。
- [試験方法・費用・限界・再開方法](../notes/phase-4f/README.md)、[検査script](../notes/phase-4f/trace.py)。

fixed rawはignored cache。必要時はmanifestのref/pathからGETしhashを照合する。全repo/sourceをcrawlせず、taskのraw_paths、accepted packageのsupplement参照、該当operator directoryと既存codeを追った。別sourceの存在否定や全accepted corpusの監査は行わない。

## 3. 何がどこまで確かめられたか

### F1. 日時の記録と、その保証範囲

accepted taskのsource recordはDailyX import `dailyx-w34-exact-import-20260902T173601Z`を名指しする。`2026-08-22_0700.md`は15981 bytes、SHA `644bafbf1ca25423b37c919837f0a25ceff7b12323a9d1c2b544c82f299a908b`。task metadataとimport provenanceの両方が同じrawを指し、実bytesに一致した。import記録は2026-09-02T17:36:01Zである。

topic 11はElon Muskのquote-post locator、`2026-08-21 17:29:36 GMT`、Plus/Pro+/Teamsの利用拡大という要約を含む。ただしGrok Bot公式投稿は引用元として説明されるだけで、その個別locator/HTTP本文はこのtopicにない。import provenanceも`DISCOVERY_AND_COMMUNITY_SIGNAL_ONLY`、`original_http_bytes_claimed=false`を明記する。**exactなのは保存されたreport bytesであり、元投稿本文の直接検証とは別**である。

primary supplementは184728-byte HTML、SHA `793b387e874aa6240b829bc2a686490e719f7c1ceb9a5e8a938915366b70b8c8`へ一致した。可視textにはAug 26, 2026、Aug 11 beta、プランの説明がある。このprimary pageをAug 21本文へ置き換えてはいけないという従来の境界は維持する。

元X locatorへのcurrent web openは1回だけ行い403だった。独立した原投稿確認は得られなかったが、投稿が無い/誤りだという証拠ではない。既存Sol reviewの「Aug 11 baseとAug 21 expansionを区別し、後日のpageでbase launchを書き換えない」というbounded PASSも確認した。観測reportとしてのclaimと、event自体の時点確定を混ぜない。

### F2. 対応が落ちる経路を再現した

以下はすべて固定W34内の実artifact/codeである。

1. `product_overrides.py`のc066はprimary page由来claimとDailyX由来claimを別に記し、後者をSOCIAL_OBSERVATIONと分類する。ただし各claimのtupleはclass/text/contextだけ。
2. `generate_evidence_input.py::build_override_record`は`supp_ids(did)`をrecord全体の`source_bindings`にする。実`interactive-evidence.json`のc066もprimary supplement IDだけを指定する。
3. `run_evidence_v2_interactive.py::_build_card`は選択されたsource IDsを全claim・limitation・verificationへ同じlistとして付ける。compact claimの許可fieldにもstatement別source指定がない。
4. consumption ledgerはAUTHORITY_CONSUMED、methodはoverride_handread、bound_sourcesはprimary1件。これは各statementの根拠対応を確認した証拠にはならない。

pre-resolved authorityを渡す明示的なunit fixtureで、改変していない`_build_card`関数がactual compact record/runner/metaからaccepted Cardと同じparsed objectを作ることを確認した。次にrecordの選択をprimary＋DailyXへ変えると、全5 statement rowsが両方を参照した。これも正しいstatement別source選択の代わりにはならない。

この試験はfull Coreのsource authority validatorやadmissionではない。input hashと単体関数の挙動を確認したものである。それでも、**rendererへ到達する前に意図した根拠対応が表現されなくなる具体的な経路**を特定できた。LLMがsourceを全く読んでいなかった、という推測は要らない。

### F3. 修復できる最小範囲と残る判断

既存taskはDailyXをDiscovery-bounded SOCIAL sourceとして持つ。Cardへ`src-1`を追加し、claim-2をそのsourceへ、chronology limitation/verificationをprimary＋DailyXへ対応させることは既存schemaで表せる。taskやsupplementの新設はこの**reportへの参照修復**には要らない。直接XのURLをCardのsource URLへ単純に差し替えるのは、今のtaskが名指しするsource authorityと異なる。

lab specimenはsource rowと3つのsource_idsだけを変え、それ以外のtext、class、status、basis、日時を保持した。`accessed_at`には既存import記録を用い、今回Driveへアクセスしたとは記さない。VERIFIEDという値も既存の履歴をcopyしただけで、新しい認定ではない。schema/local source checkはPASS。直接X URLの未登録差替えとSOCIAL→PRIMARY_OFFICIAL格上げの負例はlocal checkで拒否した。

元の「secondary Aug 21 dating」という文の別sourceは、このbounded traceでは確立していない。そのためspecimenを全Cardの意味修復完了やproduction差替え可能と扱わない。必要な確認は、既存の限定付き判断をどの根拠で維持するか、読者向けの日時/引用表現がその範囲を超えないかである。全件への追加原投稿収集を要求する根拠はない。

## 4. 修復・予防をtotal lifecycle workで見る

readerのURLだけを直してもcanonicalの誤対応は残る。逆にCardだけを差し替えて現在のaccepted chainを使い続けても、exact-byte provenanceを満たさない。

| 地点 | 必要な仕事・確認 |
|---|---|
| sourceとCard | existing sourceの許可範囲、statement別の対応、限定表現を確認する。参照だけの修復なら元のtask/supplement bytesを利用できる |
| Evidence acceptance・View・Matrix等 | Card SHAが変わる。旧accepted Cardを上書きせず、名指しする結果集合/派生artifactのbindingを更新する。sourceの意味を変える場合はView/採否への影響も判断する |
| Selection/ArchitectureとHuman authority | 後段はMatrix/Selection等のexact hashを名指しする。意味上の配置が同じかと、旧承認が新bytesを許可するかは別問題。正規の再生成/review/承認処理を確認し、旧承認を新bytesへ流用しない |
| Draft/Synthesis/reader/Candidate | 各DraftPackageはMatrix/Evidence acceptanceのhashを持つ。影響はCard内部だけでは終わらない。参照/manifest/PDFの必要な更新とreview範囲を整理する |

これは静的な依存関係に基づく作業分類で、全stageの再実行・時間測定ではない。全sourceの意味調査やLLM再執筆を毎回行うと決めたわけでもない。hashの再生成と、変わった意味のreviewを分けて費用を把握する必要がある。Phase 3のacceptance/cache投資をこの1例から再開しない。

予防候補は、意味判断を新しい補助資料へ重ねず、**既存canonicalのstatement別source欄に最初から記し、publication用の表現をそこから生成する経路**。4-EのDraft境界/compact archive問題と同じく、既存full構造が持つ情報を狭い補助形式へ落とし、後で手で復元する仕事を減らせる可能性がある。

ただしfull Card/Draftの直接著述が費用面で優位だとは未実証。詳細欄の記入、ID/hashの扱い、reviewerが読む量、誤記修復、既存callerとの互換性は負担になる。compactに個別source等を追加する案にも、二つの形式の保守と整合確認がある。役割を変えたり仕事を前へ移したりした分を削減と数えない。

## 5. 停止地点と次の入口

この1例について、記録の所在、元taskとのbinding、source対応が落ちる経路、既存欄での最小修復表現と後段への影響が判断可能になった。従ってGrok周辺や全source corpusの追跡をここで止める。原X再取得403を外部blockedや新Human Gateにしない。

次に価値があるのは、**compact helperを個別拡張する案と、既存canonicalを直接著述して表示用データを生成する案の、必要な書込み・変換・review・repair面の比較**。Phase 4-C/D/E/Fで分かった制約を入力に、同じ保証をどこで一度だけ扱えるかを見る。これは既存canonical baselineの整備候補で、まだ独立architecture Bやadoptionではない。

比較の最小入口:

- statement別source: 今回のtask/Card/source mapと`_build_card`。既知例でありunknown-sourceの能力比較にしない。
- reader境界/引用: 4-Eのcanonical DraftとWeekly/legacy renderer制約。PR #488のbib修復を既に含む現実を基準にする。
- source/entity/metric/limitの忠実性: 4-Cの修復済みcanonical sliceは制約の校正用に使い、未知source再試験とは呼ばない。
- closure: schemeを選ぶ前に、正規のbinding、Human authority、Weekly/Specialの差を保てるか、もう一つの意味store/手製publication truthを作らないかを確認する。

まず具体的に消せる重複変換/著述があるかを設計上で絞る。作業が別の欄や役割へ移るだけなら候補を止める。実装・独立review・repair込みの試験が必要になった時点で一まとまりの範囲を定め、途中のschema PASSを費用/品質勝利にしない。既存sourceの再読やhelperへの継ぎ足しを進捗の代用にしない。

rootのactive time/token/料金、全roleの純費用、full canonical品質、Special実行、PDF/visual QA、未知sourceのomission sufficiencyは未実証。4-Cの1体のreview許可は完了済みで、今回追加委任はない。productionはread-only、State/Gates/承認/PR/Issue/adoption/migrationに変更なし。Pull/Push/最終commitはHumanが行う。

## 6. PR #489 merge後の判断更新 — 2026-09-13 JST

途中Push後の[read-only観測](../notes/phase-4f/production-refresh-489.json)でmain `14781409f6fb8d79e3eb4ad6b4c457764a038fde`、W34 `f50d229162b7402c504c0978f72dab4b33052f5e`を確認した。§2の658ae823は調査開始時の固定Evidenceとして保持する。PR #489はpublication-surface revalidation / authority rebindを追加し、Evidence入力/helperやW34 artifactsは変更していない。

### 変わった費用前提

productionには、review済みCore変更によるpublication側だけの再生成を、歴史DRAFT_COMPLETEを書き換えずに再検証する正規経路ができた。`REVIEWED_CORE_CHANGE`のみ、VALIDATED_DRAFT・Architecture承認済み・Preview未決定・freeze/release pending・Exception inactiveが入口。Stateの`publication_revalidation_provenance`がpath/SHAでactive recordを指定し、版付きのimmutable recordと`supersedes`リンクを保持する。後のHuman承認/Freeze/ReleaseとのPDF一致も検査する。

固定mainの`survey_agent_control_v2.py`を選択読解した。`revalidate_publication_surface`（1224行以降）はpublication/survey surfaceの変更だけを候補にし、`_verify_preserved_provenance`（1168行付近）は全checkpoint provenanceの非superseded bytesを照合する。manuscript・quality bundle・semantic/visual review等の既存validatorを再実行する。`survey_stage_validation_v2.py`も同じactive basisを利用する。これはreview文章の意味品質を自動的に証明する変更ではない。

したがって§4の費用分類は二つに分ける:

| 修復対象 | 現在の前提 |
|---|---|
| review済みCore変更によるpublication-only再生成 | PR #489の正規revalidationを比較baselineへ含める。旧checkpoint driftを未修復と数えず、同じrebindを再実装しない。ただし新publication bytes・review records・QA・Candidate更新等の仕事は残る |
| 今回のCard source参照、canonical Draft境界など上流bytesの修復 | publication-only例外の対象外。Evidence/Architecture/Draft等のbinding・影響review・正規authority処理が必要という§4の分類は維持する。単なる表示修復としてこのoperationへ押し込まない |

### 確認範囲と残る条件

mainの5ファイルを固定refで保存し、Git blob/SHA-256を照合した。PR metadata/8変更path、最終schema、関係control flowを読んだ限定調査であり、独立した全PR監査ではない。23件focused/342件全体（6 legacy skips）のPASSとW34 disposable copyでのRELEASE_CANDIDATE到達はproduction側の報告で、rootは再実行していない。実W34はf50d229のままであり、その到達や新Human承認を実号の事実にしない。

checkpoint文書の§4–7には旧singleton/State無変更の設計が履歴として残る。最終仕様の判断には§8・merge済みcode/schemaを使う。repository/account/authorized operatorを信頼し、偶発drift/stale authority/不適切な進行を対象とするproductionの明示threat modelを確認した。新たな攻撃者モデルを追加したり、過去Human承認をrootのproduction操作許可へ転用したりしない。

**方針は維持し、比較baselineだけを更新する。** source対応を取り落とす著述経路、4-Eのrenderer互換、W34の内部配置注記はこのPRで解消していない。次は§5の限定設計比較で、既存canonicalへ一度記す案が実際に消せる変換/著述を特定する。新revalidationの存在だけでacceptance/staging投資を再開しない。全品質・全role純費用・実号の複数round運用は引き続き未実証である。
