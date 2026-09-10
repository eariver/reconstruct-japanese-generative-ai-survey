# Phase 3 — canonical authoring境界と実行経路の判断

日付: 2026-09-10 JST  
状態: **DESIGN DECISION / BOUNDED ANALYSIS COMPLETE / NO PRODUCTION ADOPTION**

## 1. 次のdecision surface

**Phase 2のBを縮小する。既存canonical形式を直接authoringするA+を標準候補とし、basis解決・入力完全性・stage別実行・差分表示だけを既存runtimeへ共通化する。独立したsemantic payload DSL、第二のState engine、全stage共通の新materializer frameworkは作らない。**

これはauthority Coreとcanonical artifactsを維持する方向の具体化であり、現runnerの変換規則をそのまま承認する判断ではない。source本文から意味を作る処理には別途改善が必要で、入力形式の改善だけではpaper defectを直せない。

Humanが次に判断できる投資単位は、**reconstruct内の隔離実装で、canonical Evidence authoringの安全な一往復とsource-backedな生成品質を比較し、production接続案を実行可能な差分として示すこと**。実装対象を全stageへ広げる前に、現在の直接Card経路＋既存補助に対する追加価値を判定する。Selectionは今回の実物差分を回帰例・次の実行補助候補として使い、同時に全面実装しない。

今回、schema／抽出functionの局所probeと保存済みSelectionの差分再構成まで行った。sourceからの新しいCard生成、独立semantic review、full Core/stage検証、production integrationは行っていない。したがって、**境界選定と次の検証契約は成立したが、品質非劣化・lifecycle費用削減・production導入可能性は未実証**である。

## 2. 調査選択と新Evidence

起点は[Phase 2 direction](astra-architecture-direction-decision.md)と[closeout](../handoff/astra-phase-2-decision-context-closeout.md)。旧bootstrapやPhase Aを再実行しなかった。最初に「activeな実行が既に別解を持つか」「新しい入力形式は必要か」「旧runnerから失う検査はないか」を選んだ。全failure史・全件paper・外部framework探索は、この境界判断への追加価値が低いため実施しなかった。

### 固定したsnapshot

- reconstruct開始HEAD: `472d7a212cfc11e9c79cc88104abe52207c742d4`、開始時clean。
- `git ls-remote`で確認したproduction main: `6d748a962d57beff89da7c1b20cb5a9a86c8e261`、変更なし。
- W34: `2b49ad77eafc4128f5d7dbf7004f767d8e29c078`。Phase 2の`030eb723...`から10 commits追加。GitHub compareで変更pathとcommitを確認し、Selection実行・修正・reviewを選択readした。
- SP001: `1b19a98511f9717d04b3b8f95207599fcdb7f48d`、変更なし。以前のThematic標本Evidenceを再利用。
- production checkoutの開始時statusはclean。fetch/pull/push、checkout変更、production module import、production writeはしていない。remote snapshotは取得時点の固定Evidenceであり、その後もlatestであるとは主張しない。

| 今回のEvidence | 観測 | 判断への効果と限界 |
|---|---|---|
| W34 Selection [r1 worklog][w-r1-log] | Core functionをedition-local driverから呼び、Selectionだけで停止。driverは`/tmp/opencode/derive_w34_matrix.py`でrepoに未保存と記録 | stage分離は既に実行済み。新層の発明より、この運用に必要な補助を正式な入口へ移す余地。driverそのものは未取得、時間計測なし |
| [r1 review][w-r1-review] | c045のclusterが誤り。executorはdirectiveどおり、誤りはdirective側と記録 | 機械的再構成でsemantic correctionを防いだことにはならない。独立reviewは残す |
| r1→r2のcanonical objects | 409件中1 assignment、`architecture_role`と`rationale`だけ変更。top-levelは`selection_version`変更。Matrix bytes不変。全rowのProfile extensions等値 | 前版＋明示deltaで新objectを完全再構成できた。汎用semantic DSLを要求しない、実物に基づくrepair例。bytes serializer／stage再実行は検証していない |
| [r2 worklog][w-r2-log] / [review][w-r2-review] | current-Core検証とfresh reviewのPASSを記録。Architecture pending、後続directive/requestあり | Phase 2の「Selection未実行」は更新。PASSはupstream記録の読解で、今回の再検証結果ではない |
| [Evidence prompt][prompt] | もともとfull canonical Cardを返す契約 | A+は新しいontologyではない。既存経路を基準に使える |
| [Card schema][card-schema] / [validator][card-validator] | entity・claim別source・metric/comparatorを表現できる | synthetic multi-source Cardがschemaと抽出validatorを通過。実Rawから正しく生成できる保証ではない |
| [interactive builder][card-builder] | 単一entity、metrics空配列、共通source付与。一方exact target集合照合がある | narrowingを廃止する際、保護まで捨てない。canonical validatorを呼ぶだけでは代替不十分 |
| [agent helper][helper] | current-stage basisの例外はcontent-addressed acceptance照合を伴う。CLI allowlistはScreening/Evidenceのみ | W34のMatrix用driverを不要にするには、単なるCLI名置換以上の接続設計が必要。任意helperの解禁は不可 |

mainのdocs/.github/configを対象に三runner名を検索した結果、得られた参照は主に過去のrepair/audit文書だった。これは利用率でも未使用証明でもない。W34 Evidenceは前Phaseでactual callerを追跡済み、Selectionは今回actual executionを確認した。Draft runnerについては依然「静的な縮約の存在」であり、廃止backlogへ自動登録しない。

## 3. A+ / Bの比較を具体化した結果

比較条件は両案とも同じexact task/package/source resolver、schema検査、stage機構、authorとreviewerを使うこと。A+にhash手入力を負わせてBを有利にしない。

### Evidenceの一往復

| 境界 | A+を基準にする案 | 独立payloadを置くB |
|---|---|---|
| prepare | task/packageからcanonical Cardのidentity/basisを準備。source選択肢と完全なtargetsを提示 | 同じ準備が必要 |
| author | canonical `status/entities/artifact/temporal/sources/claims/metrics/limitations/verification`を編集 | 同じsemantic fieldsを別payloadへ記入 |
| complete/check | 準備したidentity/basisが変更されていないことを照合し、schema＋関係検査＋入力完全性検査 | payloadをcanonicalへ合成し、同じ検査 |
| review | exact Card/View/Task/Rawと差分から表示。省略箇所は参照で展開 | canonical生成後はA+と同じ |
| 維持する契約 | 現canonical schemaとfield ownership | 左に加えpayload許可fields、version、変換、旧input互換 |

[probe results](../notes/phase3-contract-probe-results.json)には、具体的な準備済みCard、Bのmachine fields、Bのsemantic payloadを全文保存した。2 entities・異なるsourceを持つ2 claims・1 metric・UNRESOLVED targetのsynthetic例。架空の72という値はschema実験専用であり、Surveyの事実ではない。Bは4つのtop-level machine fieldsを分離して再結合するとA+と同じobjectになる。**この例の同等性は単純なfield保持の確認に限る。Bの全設計の不要性やモデルの入力容易性を実験で証明したわけではない。**

canonical入力をUI上でsemantic fieldsだけ見せることは可能であり、それだけで別schemaを設ける必要はない。先にこの安い選択肢を試す。source-local metadataの重複が実測で負担になるなら、同じcanonical objectを補完するfunctionを追加する。source別support・comparator・target findingを縮める変換は入れない。

### 保存済みSelectionの一往復

- before: `558d29b...`のcanonical Selection。
- author delta: c045の`architecture_role`を`WEEKLY:model-economics-distribution`へ変更し、対応rationaleを明示。これはreview/directiveによる意味判断である。
- machine: exact prior objectを読み、対象candidateを一意照合、変更field集合を検査。revision metadataは`w34-sol-selection-r2`。全409件の候補集合・Profile extensionsとMatrix hashを保持。
- after: `2b49ad77...`のSelectionとobject等値。件数だけの一致でなく全objectを比較した。差分・hashはprobe resultsへ保存。
- review view: 変わったcandidateのbefore/after＋Card/View参照＋全候補集合の照合結果を示せる。非選択368件は保存・展開可能なnegative spaceとして残す。

これは今後のrepairでも全rowを別入力へ書き直す必要がない実例である。**生成できる差分説明とsemantic approvalは別**。r1の誤clusterをdeterministicに正解へ直す一般則は得ていない。

## 4. 境界契約 — 共通化するものを限定する

新サービスではなく、既存runtime内で再利用するfunction／CLIの責任として定義する。以下はproposalで、実装・採用済みAPI名ではない。

### 4.1 prepare / author / check / review / acceptを分ける

1. **prepare:** 現行Stateとaccepted refsからtask/package/Profile/effective Discoveryを解決する。raw URLへの再取得で古いbytesを置換しない。exact basisと使用runtime identityを記録した未受理candidateを作る。
2. **author:** canonical objectの意味を編集する。意味的に未決の必須値を機械のdefaultで埋めず、未完成candidateとして止める。候補がschema未成立でもauthoring途中と明示し、受理へ渡さない。
3. **check:** 形式、関係、全件対応、basis、許可差分を検査。authorがmachine-owned fieldsを変えた場合は上書き修正せずreject。全検査成功まで通常canonical output pathへ書かない。
4. **review:** checked candidateのexact bytesに対するsource-backedな意味review。別途Human Gateが必要なstageでは現行Gateへ渡す。schema PASSを意味PASSとして表示しない。
5. **accept/advance:** 現行Coreの独立operation。materializationだけではState・approvalを作らない。write直前にbasis/lease/requestを再照合し、既存trust・stage契約で処理する。

既存writerが検査前に途中artifactを書く場合も、最初の統合では隔離stagingで完了させてから既存write経路へ渡す案を優先する。全repoのtransaction engine新設はしない。並行中にbasisが変われば再prepare／必要な再reviewへ戻す。暗黙rebaseやlast-writer-winsはしない。

### 4.2 Field ownership

| Artifact | 機械が扱う範囲 | author／editorが決める範囲 |
|---|---|---|
| Card | schema/issue/task/basis、確認済みsource metadataの照合・転記、ID重複検査 | entitiesの同一性、artifact、各statementのsource subset/subject/class/context、metricsと比較条件、event意味、verification/findings、status |
| View | exact Card bytes hash、issue/Profile/task binding | materiality/rationale、scope dimensions、Profile別annotations |
| Selection | exact Matrix/basis、candidate join、counts、明示された継承fieldsの等値照合 | 全候補の採否・usage・role・rationale。bulk HOLDはeditorが対象集合と理由を明示した場合のみ |
| Architecture | exact Selection refs/basis、既存構造検査 | thesis、packages、requirements、omissions、allocation、boundariesへの応答 |
| Draft | approved package内のref lookupとsubject照合、basis | prose、blockごとの特定ref、coverageの実際の対応、boundary disposition |

`accessed_at`や`observed_at`を単なる実行時刻へ置換しない。capture、observation、source publication、実際のeventを区別する。authoring時刻とsource取得時刻が同じとは限らない。source `role`やcanonical entity URLも意味を含むため、既定のDiscovery locatorが常に答えとは扱わない。

statement/entityのIDは候補作成時の補助で発行できるが、既存IDをarray順変更で振り直さない。同じIDの内容が変わればCard bytes／下流basisの変更として扱う。IDが安定したことを旧approval再利用の根拠にしない。

### 4.3 旧runnerから移す検査と、新しく明示する制約

[局所probe](../notes/phase3_contract_probe.py)はfixed mainから3 functionsと必要constantsだけをAST抽出して実行した。production modulesやstageは実行していない。date parserはoffset-awareの小さい代替、Supplement経路は未実行。schemaは実物をjsonschemaで検査した。

| 反例 | schema＋抽出Card validatorの結果 | 新入口での扱い |
|---|---|---|
| task targetを全部落とす | 通過 | exact target集合＋重複禁止を独立検査。旧builderの集合照合を最低限保持 |
| 同じtargetを2回返す | 通過 | 重複をreject。dict化で隠さない |
| 未登録source ref | 関係検査で拒否 | 既存検査を維持し、Supplementの実物bindingも統合試験 |
| metricが自己をcomparatorにする | 関係検査で拒否 | comparatorの意味自体は別途review |
| task hashがstale | 関係検査で拒否 | source/package/Profile/runtimeを含む実Coreのbasis検証も必要 |
| claimを`Content selection saved.`に替える | 通過 | source preparationとsemantic reviewで扱う。文字列ブラックリストで完了しない |

空target通過は**Card schema／このfunctionの限定した検査範囲**についての発見。production全経路が無条件で受理することや、既存accepted成果に欠落があることを実証していない。入口設計で失う保証を特定するための反例である。

Viewは既存`validate_edition_view`がProfile別key集合を検査する。Weeklyのwindow/carry-over、Thematicのlineage/branch/transition/caveat、Periodのperiod roleをそのまま編集可能にする。CONTEXTやMAIN_EVENTを自動固定しない。Selectionのextensions保持は型検査だけに任せず、対象routeがMatrix継承を要求する場合に等値を確認する。異なる意味へ変更する必要があれば明示した設計変更・reviewへ戻す。

Draftのrefは現行`(evidence_task_id, kind, evidence_id, subject_id, subject_role)`を使用する。kindはEVENT/CLAIM/METRIC/LIMITATION。特定blockへ選んだrefsだけを付け、requirement→blockの実対応をauthorが記す。全claimを全blockへ付けるfallbackを新入口には設けない。今回Draft出力やcoverageの実行試験はしていない。

## 5. Source品質とhistorical reproducibilityは別に検証する

paperについては、既存Rawの本文構造・未確認target・source-specific limitationsを保持する準備が必要。DOM本文の除去境界、section locator、truncationと未処理範囲を示し、prepared textからexact Rawへ戻せるようにする。本文抽出は意味確認の完了宣言ではない。

最初は既存`context`／`finding`へ必要なsource-local locatorと比較条件を記し、既存実行provenanceにRaw digest・抽出version・範囲を残す方式を評価する。別Consumption正本は追加しない。ただし自由文locatorは自動検証契約ではない。実例で繰り返し構造的照合が必要なら、その時に狭いschema拡張を判断する。

次の品質比較は二つを分離する。

- **変換適合性:** 与えた正しい意味を保つか。今回のprobeはここだけを部分的に確認した。
- **生成の十分性:** 同じ保存Raw/taskから、authorが重要なclaim・比較条件・limitationsを作れるか。既知paperのUI混入除去だけでなく、未確認targetとomissionを非著者が確認する。gold payloadを与えた変換成功で代替しない。

historical reproducibilityも分ける。旧bytes・旧contract・reviewed commit・Gate・PDFを検証できることは必須。新modelで同じ文章を再生成できることは保証できない。新実行の再現性にはinput bytes、prompt/model設定、抽出・producer/runtime version、canonical出力とvalidationを既存archiveへ記録する。現在存在しないSpecialの外部bytesや過去の読解範囲をbackfillで作らない。

Weeklyでの成功をTHEMATICやRETROSPECTIVE_PERIODへ転用承認しない。SP001のobservation-only chainは不足を明示したまま通す表示例にし、当時のexternal repository full captureがあるように表示したら失敗。Periodは今回実物round-trip未検証で、拡大条件に残る。

## 6. Lifecycle全体の仕事とretirement

最適化対象はauthor token数だけではない。新しい常駐役割や独立review削減を先取りしない。

| 作業 | 減らせる候補 | 維持／増える仕事 | Evidenceの強さ |
|---|---|---|---|
| production | canonicalの転記、共通sourceの一律展開、edition-specific basis探索 | source読解と明示support、入力検査 | narrowingはコード確認、削減時間未計測 |
| review | exact refs探索、全row手動比較、counterexample資料の組立て | semantic correctness、omission、非選択、Human判断 | W34 r1 defectはreviewの必要性を支持 |
| repair | 前版＋bounded deltaで変更範囲を生成・照合 | 新candidateへのfresh validation/review、現行invalidation | 409件の実物object replayで成立 |
| maintenance | writer間に散ったbasis/default/target対応 | 共通入口のregressionと文書・移行保守 | Matrix driverの実行記録あり。全caller集合は未確定 |
| regeneration | 不変Raw/既存accepted basis再利用、必要箇所の準備再実行 | contractが要求する全候補検証・fixed-head audit | audit時間削減は算入しない |
| Human handoff | current refs・未解決・必要判断を正本から表示 | adoption/priority/Gatesの裁定、exact candidate確認 | 生成viewの運用費は未測定 |

紙面上で別payloadを短くしても、reviewerの再読・operatorの補完・Humanの質問が増えれば採用しない。人のactive time、author/reviewer/operatorのLLM usage、CI elapsed/cost、再実行回数、入力／修復箇所、維持すべき契約数を別軸で計測する。今回のprobe実行秒数はproduction workの代用にしない。

### 増やすものと外せるものを対にする

| 導入候補 | future routeから外す対象 | 実際のretirement条件 |
|---|---|---|
| canonical Evidence入力補助 | 適用routeの`_build_card`によるnarrowingと、paperのkeyword→claim／target一律VERIFIED | source-backed生成と完全性検査が合格し、対象callerが新経路を使う。旧入力archiveは保存 |
| Selectionだけの既存Core呼出入口 | W34 worklogにあるようなMatrix derivation用の使い捨てdriverを今後作る仕事 | historical basis例外を正確に継承、stage停止、全候補/extension照合。W34の過去成果は書換えない |
| exact delta/review表示 | 同じcounts/hash/変更一覧の手作業による再構成 | 正本参照と欠落/stale表示が十分。review verdictや固有の読解根拠まで削除しない |
| Draft直接refs入力（後続候補） | 適用callerのcandidate単位all-refs/all-coverage展開 | actual callerと生成物で価値が示された時だけ。現時点で全runner削除を約束しない |

新入口を足して旧新を恒久的に通常運用するなら採用を見直す。ただし適用未検証Profileの旧routeと歴史再現用versionは残す。retirementは旧artifact削除とは違う。

## 7. 実行経路と停止条件

Phase番号を全layer完成の工程表にしない。次は以下の順で、結果が判断を変える範囲だけ進める。

### 次の隔離検証単位（推奨する追加投資）

最初にEvidenceのcanonical authoring補助をreconstruct内で実装し、full upstreamコードの固定snapshotを隔離環境で使って、既存schema/validator/acceptance接続の互換性を確認する。production refs/Stateは接続しない。抽出function probeのPASSをfull Core PASSに昇格しない。

検証面は、既知paper failure、異なるsource/subjectとmetric、captured-but-unresolved、Profileと時点差、stale/missing/duplicate binding。全件shadowは不要だが、known failureだけに合わせた成功にも留めない。新経路が正しく意味を生成できるかを見るsource/taskを追加し、費用・omissionが判断を変えなくなるところまで選択する。

比較対照は「full canonicalを既存補助と直接生成する経路」。両armへ同じRaw/taskと同じreview基準を与える。known bad keyword producerだけを対照にして勝利を宣言しない。model名は実行設定として記録し、role ontologyにはしない。今回独立agent reviewは実施していない。

成功条件は、(a)必要意味の保持、(b)missing/stale/無許可writeでfail-close、(c)fresh semantic品質が低下しない、(d)少なくとも一つの旧作業を通常routeから外せる、(e)全roleの仕事増が許容可能、(f)既存historical検証を壊さない、を同じcandidateで説明できること。小標本の成功は全production ROIの証明としない。

### その結果に応じた分岐

- A+だけで十分なら、追加payloadを中止したまま、必要な入力検査と薄いCLI整備の採用案へ進む。
- 意味生成が依然悪ければ、source preparation／author指示／review方式を修正する。共通materializerを拡張して隠さない。
- basis復旧やstage接続が支配的なら、Selectionの正式入口とrepair lifecycle診断へ優先を移す。W34の一時的State再提示を一般的rollbackレシピとしてコピーしない。現Coreのrevision/invalidation契約を精査してから接続する。
- canonicalで必要意味を表せない反例が出たら、そのfieldだけの拡張を比較する。現時点でCore全体置換やCへ進む根拠はない。
- total workが減らない／通常旧routeを外せないなら局所repair中心へ戻し、framework投資を止める。

### productionへの境界

隔離結果から、対象future edition/Profile/stage、実装差分、検証結果、外すcaller、rollback/invalidation手順、残るcostを具体化してHumanへ採用判断を提示する。その明示承認の後だけproduction変更へ進む。初回はone writerと現行review/Gatesを維持し、W34やfrozen SP001を移行実績のために書換えない。

受理前ならcandidateを破棄して旧routeへ戻せる。受理後／Gate後は現行revisionと再検証が必要で、旧approvalを新bytesへ付替えない。exact PDF、Freeze、Release照合、trust root、lease、broad contract hashとfixed-head auditは現行どおり。release接続maintenanceやaudit粒度変更は独立の優先判断とし、この案のROIへ未実施の緩和効果を入れない。

## 8. 終了判断と継続用メモ

ここで停止する理由は、次の主要不確実性がさらに文書やschemaを読むことでは解けず、**source-backedな実生成、full Core統合、全roleの実働比較**へ移ったためである。今回のEvidenceでA+を基準とする境界、移すべき入力検査、actual repairの再構成、retirement条件まで具体化できた。独立semantic DSLの詳細設計や全stage prototypeへ進む情報価値は現時点で低い。

継続時は本書§1・§4・§7とprobe結果から始める。remote currentnessが必要な時だけmain/W34/SP001を再確認し、差分を選択readする。過去のSelection未実行snapshotをcurrent状態と誤読しない。未検証の主要項目はSupplementつきfull Core round-trip、fresh semantic品質、Period実例、runtime integration、実使用caller全体、費用内訳である。

再現: `python -B -X utf8 notes/phase3_contract_probe.py`。結果JSONは実行stdoutを保存したもの。必要runtimeはPythonとjsonschema、source取得は既存fixed-ref helperを利用する。最初にschema名を`evidence-card-v2.schema.json`と仮定して404となり、tree listingで実名`evidence-v2-card.schema.json`を確認して修正した。最終probeは成功。

新規durable artifactsは本書・probe・結果JSONの3点。Git commit/Pull/Push、production mutation、Human decisions/Gates/Freeze/Release/adoption/migrationの変更は行っていない。

[w-r1-log]: https://github.com/eariver/japanese-generative-ai-survey/blob/2b49ad77eafc4128f5d7dbf7004f767d8e29c078/sources/2026-W34/execution/luna/w34-selection-after-sol-evidence-r1/session-worklog.md
[w-r1-review]: https://github.com/eariver/japanese-generative-ai-survey/blob/2b49ad77eafc4128f5d7dbf7004f767d8e29c078/sources/2026-W34/execution/reviews/sol-selection-review-20260910-r1.md
[w-r2-log]: https://github.com/eariver/japanese-generative-ai-survey/blob/2b49ad77eafc4128f5d7dbf7004f767d8e29c078/sources/2026-W34/execution/luna/w34-selection-c045-cluster-correction-r2/session-worklog.md
[w-r2-review]: https://github.com/eariver/japanese-generative-ai-survey/blob/2b49ad77eafc4128f5d7dbf7004f767d8e29c078/sources/2026-W34/execution/reviews/sol-selection-review-20260910-r2.md
[prompt]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/config/prompts/evidence-verification-v2.md
[card-schema]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/schemas/evidence-v2-card.schema.json
[card-validator]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/survey_evidence_v2.py#L865
[card-builder]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/run_evidence_v2_interactive.py#L302
[helper]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/survey_agent_tool_v2.py#L122
