# Semantic handoff feasibility — Astra

実行: 2026-09-09–10 JST  
状態: **PHASE COMPLETE / CONDITIONAL FEASIBILITY / NARROW PRODUCER REPAIR FIRST**  
範囲: read-only investigationとworkspace内の分析。production implementation/adoptionは未実施。

## 1. 判定

**既存chainは、保存済みの意味とedition内authorityを受け渡す基盤として条件付きで利用可能。ただし、意味成果の生成品質まで十分とは言えず、paper producerの狭い修復設計・局所検証を先行させる。**

4 sliceで確認した結果はmixedである。

- Task / Card / Viewのexact bytesとidentityは追跡できた。W34のSupplementは選んだ3例ともRawのhash・sizeまで一致した。別のcanonical truthを追加しなければ参照できない構造ではない。
- C019のclaimsとlimitations、C033の未解決理由、Specialのprofile annotations・比較上の境界は既存artifactに残る。Matrix等で省略されても、元Card/Viewへのjoinで回収できる情報が多い。
- **W34 paper一件のaccepted Cardに、HTMLの非本文UI文言がmethod claimとして入っている。** これはInput→Cardで意味が消えた例ではない。前段の抽出・claim生成で壊れた内容を、Coreがそのまま保存した例である。
- 消費ledgerの `AUTHORITY_CONSUMED` は独立した読解証拠ではなく、producerがstatusとsource binding等から生成するラベルだった。既存ledgerをそのまま再利用の合格証にする案は成立しない。
- source-local span、実際に読んだ範囲、targetごとの判定根拠は均一には残っていない。Rawを再取得せず読むことはできても、過去の読解行為や未記録の意味判断をdeterministicに復元できるわけではない。

したがって、新Consumption Record、全体adapter、常駐critic、resume実装を直ちに追加する根拠はない。一方、「既存構造だけでsemantic workを安全に省略できる」という結論にもならない。

次の投資は **paperの本文範囲・claim生成・target判定の境界を対象にした、狭いproducer修復の設計と局所較正** を推奨する。既存Cardで表現可能な内容はそこへ出し、追加の独立正本を先置きしない。本Phaseではその修復も実行していない。

## 2. 実行契約・remote reality・方法

starting contractは[次Phase決定](astra-next-phase-decision.md)。Humanの同一セッション継続指示により本検証を実行した。Phase Aは再実行していない。

| 対象 | 開始時確認したremote SHA | 前回からの差分 |
|---|---|---|
| workspace | `b328892e5c4a55673a8bff9cdd2d81814ec5d416` | local HEADと一致。前回baselineからの差分は決定文書の追加のみ。開始時clean |
| production main | `6d748a962d57beff89da7c1b20cb5a9a86c8e261` | 変更なし |
| W34 | `030eb723c12282f0cfd09aaada05d14f0c0906c7` | 変更なし。`EVIDENCE_REVIEWED`、Selection未実行という前回の固定点を利用 |
| Special/SP001 | `1b19a98511f9717d04b3b8f95207599fcdb7f48d` | 今回新たにremote確認。THEMATICの固定例として利用 |

2026-09-10 00:00 JST頃の再確認でも、この4 refsは変わっていなかった。SP001のStateは `FROZEN` / `stage:release`。これは当該branchの機械状態であり、外部Releaseの有無や現在の公開障害を示す証拠には使わない。

**境界を明示した方法:** 固定SHAのGit object / GitHub Contents APIを読む。mainの関連functionを静的に追い、4例のpersisted bytesに対してhash・identity・field対応を独立したPython probeで確認した。production moduleのimport、Core validatorの実行、stage acceptance、Matrix/Selection生成は行っていない。以下の「一致」はこの分析の結果であり、current-Core upstream revalidation PASSではない。

再現用補助は[probe](../notes/semantic_handoff_probe.py)と[結果JSON](../notes/semantic-handoff-probe-results.json)。`python -B -X utf8 notes/semantic_handoff_probe.py` は固定refからreadし、選択した分析結果をstdoutへ出す。cacheはOS temporary directoryで、production refsやcheckoutを変更しない。

### Samplingと実行中の変更

当初の4 slice内で完了した。選定は統計標本ではなく、異なるfailure modeを判定するためのpurposeful samplingである。

| Slice | identity | 選定理由 |
|---|---|---|
| W34 product | `w34-event-c019` / task `fb85a056f96e113a` | 旧症状が改善した例。既存意味成果の保持を確認 |
| W34 paper | `w34-event-arxiv-2608-14927` / task `10f1492c33d25e64` | ledger順で最初のarXiv例。handread overrideと異なるproducerを確認 |
| W34 captured/unresolved | `w34-event-c033` / task `b25c912f0774b778` | sourceがあってもtarget未解決の境界 |
| SP001 thematic | `SP001-D008` / task `afc0e0cae360c851` | Qwen3.8の時点・license・比較境界とThematic annotationsがある例 |

paperで実際の欠陥を得たため、予定の均等なmappingから、`body_extract.py` / `generate_evidence_input.py`と固定Rawの照合へ時間を移した。理由は、projection追加では解けない問題かを識別する情報価値が高かったためである。SP001は全Specialの代表ではなく、共通v2 CardとThematic consumerの成立例として扱った。

補助probeの初回でMatrix配列名を `candidates` と仮定してKeyErrorになったが、実物の `rows` へ修正した。大きな出力はそのまま結論にせず、必要な4例・fieldを抽出し直した。保存済み結果は修正後のもの。

追加paperを読めば欠陥頻度は多少分かるが、今回の「既存情報の保持と、意味生成の欠落は別」という主判定は変わらない。頻度推計や409件のquality auditへ拡張せず停止した。

## 3. Producer / validator / consumer mapping

下記コード参照は特記なき限りmain固定SHA。SP001については当時のbytesを分析し、現在mainとの再受理互換性は主張しない。

| 境界 | Producer・正本候補 | Validator / consumer | 保持できること・限界 |
|---|---|---|---|
| Discovery / Screening→Task | `prepare_evidence_package`。accepted package内のTask copy | `validate_evidence_package_basis` / `_validate_task` | discovery ID、source records、Raw paths、verification targets、Screening basis。Task IDはedition内のjoin用で、edition非依存のsource identityではない |
| Supplement→task-bound sources | `build_evidence_authority_supplement`とTaskのsource IDs | `validate_evidence_authority_supplement`、`task_authority_sources` | locator、Raw path/hash/size、取得時刻、task/discovery binding。sourceの実在・同一性は読解やentailmentの証明ではない |
| W34 Raw→interactive record | edition側 `generate_evidence_input.py`。paper / overrideの二経路 | `_validate_record`、`validate_interactive_input` | 生成されたclaims・limitations・targets・materialityを保持。ただしpaperの選文・target判定に問題。入力の形の検査は意味の検査ではない |
| interactive record→Card | runner `_build_card`、`accept_evidence_results`。accepted Cardがfactual payload | `validate_evidence_card` / `validate_evidence_acceptance` | 3 W34例でtext/class/contextが完全一致。task/package/Screening/contract hashes、subject/source参照を検査。metrics/comparator等の表現力はrunnerがcanonical schemaより狭い |
| input→Edition View | `_build_view`、`accept_edition_views`。accepted Viewがedition annotation | `validate_edition_view` / `validate_edition_views_acceptance` | Card hash、materialityとrationale、Profile固有情報。NEEDS_MORE→HOLD等を検査 |
| Card/View→Materiality/Matrix | `build_materiality_ledger` / `derive_candidate_matrix`。機械projection | `validate_materiality_ledger` / `validate_candidate_matrix` | task全体の対応、status、counts、boundaries、View annotations。Matrixの`comparison`は件数であり性能比較データではない |
| Matrix→Selection | 編集担当の意味決定、executorによるmaterialization | `validate_selection` / stage `_selection_basis` | exact basis、全candidateの一回ずつのassignment、disposition、role namespace、未解決のSELECTED禁止。意味判断はstatusから自動導出できない |
| Selection→Architecture / review summary | editorial package決定、`build_architecture_review_summary` | `validate_architecture`等 | summaryは後段のprojection。本文claimsやsource-local条件を再発見するためにはCard/View/Rawへ戻る参照が必要 |

主要コード: [Evidence Core][core-evidence]、[interactive runner][runner]、[Architecture/Matrix Core][arch-core]、[stage validator][stage]。

### 正本とwriterを増やさない扱い

- **source bytes / capture metadata:** 既存RawとDiscovery/Supplement。capture担当が作り、Coreがbindingを検査する。URLだけから別版へ置き換えない。
- **factual extraction:** accepted Card。interactive inputはその生成元とprovenanceであり、consumerが別々に編集する第二の正本にしない。分析時は両者の差分検証に使える。
- **edition meaning:** accepted Viewのannotationと、明示された編集directive / canonical Selectionの段階を区別する。W34のView rationaleはprovisional、Sol directiveは後続の意味決定、Selectionは未materialize。後者が存在しない段階で前者を最終採否にしない。
- **consumption process trace:** 実行領域のdetails / ledgerは参考記録。状態・意味正本・Human approvalを上書きするauthorityにしない。新しい表示に取り込む場合も記録元と限界を見せる。
- **Matrix / compact packet / summary:** 一つのdeterministic writerによるread-only projectionとして扱える。表示上の省略をsource削除や承認省略へ変えない。
- **Human Gate / historical execution:** 従来の正本とidentityのまま。Astraの分析やlogical editorial continuityへ委譲しない。

## 4. Slice別の実証

### 4.1 C019 — 保存済みの意味の再利用は成立する

[accepted Card][w-card-c019]の3 claims、VENDOR_CLAIM分類、context、limitationsはarchived interactive inputと一致した。Viewには「今回のMATERIALである理由」と `MAIN_EVENT` が残る。SupplementのRaw hash/size、Task→Card→Viewのhash対応も一致した。

**deterministicに回収できるもの:** Cardのsource ID→Taskのbinding→Supplementのexact Raw。Cardのsubject/class/context、Viewのwhy-this-issue、Taskのverification target。`temporal.events=[]`でも、選択されたSupplementのpublished_atがnullである理由と、Discoveryの `2026-08-20` が別由来の情報であることはTaskから分かる。

**新しく意味判断が必要なもの:** そのDiscovery日付を一次本文で検証済みのeventとして昇格すること、あるclaimがRawのどのspanに支えられるかの確定、別号の問いへの十分性。これらを既存の文字列から勝手に補完しない。

`consumption-details`のこの行はmethodとbound source IDsのみで、handreadの範囲・claim別locatorはない。本文の同一bytesは取得できるが、過去の読解範囲を復元する記録としては不十分。CoreのCard変換が既存のlocatorを消したとは観測していない。

### 4.2 Paper — authorityはつながるが、意味生成が壊れた実例

[paper Card][w-card-paper]の第一claimには `Content selection saved.` がmethod説明の一部として現れる。固定Rawは556,046 bytes、Supplement SHAとの一致を確認した。この文言はRawのhidden UI modal内にあり、paperのmethodではない。

原因経路をこの例では次まで追えた。

1. [body_extract.py][extract]はHTMLタグ等を落として空白を一行へ潰し、60,000文字に切る。独立probeで当該Rawの正規化後は79,363文字、一行になった。
2. 同ファイルの`parse_sections`は20行未満を `full` bucketへ入れる。このHTML経路ではmethod/evaluation/limitationsのsection bucketsが成立せず、全体や先頭のfallbackに依存する。
3. [paper_record][generator]はkeywordで順位付けした先頭sentenceをclaimにし、title先頭40文字の除去・claimへのprefix付加・280文字切り詰めを行う。detailsの第一method spanもUI混入済みだった。第三method spanには実際の四protocol比較の記述が残っているが、method claimには選ばれていない。
4. 同functionは各targetに一律 `VERIFIED` を付与する。Card最上位はPARTIALで、edition materialityはCONTEXT固定。**PARTIALという安全側の全体ラベルと、根拠を伴わないtarget VERIFIEDが同居する。**
5. interactive record→Cardではtext/class/contextが一致する。今回の欠陥はCardへのprojectionによる脱落ではない。

Rawには `section#S7` のLimitations本文もある。内容にはsolver/benchmarkの範囲などが書かれている。一方Cardは「section parsingで専用limitationsを捕捉できなかった」という一般的な注記に留まる。この注記はparsing observationと限定されているため、単純な「limitations節が存在しない」という虚偽断定とは区別する。しかしconsumerが必要なsource-specific制約を使うにはRawを読み直す必要がある。

**判定:** UI混入は実際のsemantic defect。形式・hash・authority bindingの成功では検出されなかった。paper全件の欠陥率、当該paperのMATERIAL相当性、公開物への流出は未検証。現在directiveではこのCONTEXT例はHOLD側であり、公開済み事故やcritical authority breachとは判定しない。

また、ledgerのtargetは934文字から220文字へ切られている。全文はTaskに残るので、これはchain全体の不可逆損失ではない。ledgerだけをresume packetの唯一入力にすると欠落になる。

### 4.3 C033 — 未解決の表現は既存構造で保持できる

[C033 Card][w-card-c033]には、取得したrankings surfaceと未取得のbenchmark methodologyを区別したclaim、二つのlimitations、UNRESOLVED targetがある。ViewはHOLDで理由も保持し、3者のhash chainとSupplement Rawのhash/sizeは一致した。

ここで `AUTHORITY_CAPTURED_BUT_UNCONSUMED` は「一文字も読んでいない」の意味ではない。Cardにはrankings pageを読んだbounded observationが存在する。**targetに必要なbenchmark情報を解決できていない状態**として読む必要がある。単一のconsumed boolへ畳むと、読めた部分と未解決の問いが失われる。

既存Card/Viewをjoinすれば、この違いは新schemaなしに提示できる。CoreのView validationはNEEDS_MORE→HOLD、Selection validationはNEEDS_MORE/HOLDのSELECTEDを拒否する。今回は静的確認であり、この例を変更してstageを再実行したわけではない。

### 4.4 SP001-D008 — Thematic contextの保持とsource snapshotの限界

[SP001 Card][sp-card]はPROJECT_CLAIM、checkpoint/license/performance比較の未解決境界を持つ。View→Matrix→Selectionで `lineage_role`、`branch_ids`、`transition_ids`、`historical_attribution_caveat` が完全一致した。Profileは `OPEN_HISTORY_AS_OF` / `2026-08-24T17:24:00Z`。Matrix hash refsからCard/Viewへ戻れ、Selection rationaleとQwen packageのboundariesにも未解決事項が残る。[SP001 Matrix][sp-matrix] [Selection][sp-selection] [Architecture][sp-arch]

ただしTaskのRaw参照は[primary-source observation Markdown][sp-raw]である。当該Cardのclaim textはDiscovery source summaryと同一だった。このchainから再現できるのは保存されたsource-local observationとそのedition解釈であり、外部repositoryの当時の全bytes、exact checkpoint license、比較実験の条件ではない。別の保管場所に元bytesがある可能性は排除していないが、今回の参照chainには接続されていない。

このCardを作った人が本文を読まなかった、あるいは特定transformが意味を削った、とは断定しない。元のsemantic authoringの原因行は未追跡。当時の[Evidence execution request][sp-request]はCard/Viewの成立を報告するが、missing source bytesを補う証拠ではない。

mainとSP001の間でCard schemaとArchitecture baseは同じ、Evidence Coreとinteractive runnerには差分がある。過去acceptanceのfieldsがjoinできることを、現在mainでの再受理可否や全Special互換性と混同しない。

## 5. 欠落・lossy projection・再判断を区別する

| 必要情報 | 判定 | 最小の扱い |
|---|---|---|
| edition/task/Card/View identity、exact Supplement Raw | 観測例では保持 | 既存acceptance/packageからjoin。新しい独立ID台帳は不要 |
| claims、evidence class、subject、limitations | 保存済み部分は保持 | Cardを読み、Matrixの件数から内容を推定しない |
| materiality rationale | Viewには残る。Materiality ledgerはstatus由来の一般文、Matrixはrationaleを直接持たない | Viewへjoin。特にThematicではWeeklyのwhy-this-issue代替がないためrationaleを明示取得 |
| full verification target | Task/Cardに残る。consumption ledgerでは切り詰める | Task/Cardを参照し、省略表示と実体を区別 |
| claimごとのsource support / span | C019は未記録、paperはsentence候補のみでsource/spanの厳密対応なし | locator候補の検索は可能だが、support判定と過去の消費範囲を自動で認定しない |
| paperのsource-specific method/limitations | Raw/detailsに材料が残るが、Cardへの意味化が不十分 | sourceを使う狭い生成・review修復が必要。新projectionだけでは直らない |
| metrics、comparators、claimごとの異なるsource選択 | canonical schemaは表現可能。interactive runnerは単一entity、全claim共通source集合、metrics空配列へ制限 | schema不足と扱わずproducer経路の表現力を先に評価。4例では非空metricsが消えた事故を実証していない |
| event date / applicability | Profile/Task/Viewで由来別に保持。選択sourceのpublished_at=nullからeventは作れない | snapshot date、Discovery chronology、verified eventを分けて表示。推定でeventを作らない |
| Specialのexternal source当時bytes | selected chainではobservationしか辿れない | 既存observationの再利用範囲を限定。強い新claimにはexact capture / 読解が別途必要 |
| selection role / editorial cluster | directiveまたはSelectionに存在。Evidence statusからは復元不可 | 明示した意味決定をmaterializeする。採否を再推論するprojectionを作らない |

**重要な契約上の留保:** mainの`validate_selection`は `profile_extensions` がobjectかを検査するが、Matrix annotationsとの等値をこのfunction内では強制しない。schemaもobjectとしている。stageはこのvalidatorへ委譲する。W34の実行依頼はexact preservationを別途要求し、SP001標本では実際に保存されていた。したがってこれは今回観測した消失事故ではなく、将来の一般adapterで自動的に保証されると思ってはいけない境界である。

## 6. 最小変更候補と仕事の増減

総workの改善は未計測。以下は観測した構造から説明できる作業仮説で、時間・credits削減率は付けない。

| 候補 | 減らせる可能性のある仕事 | 新たに増える仕事・制約 | 今回の判断 |
|---|---|---|---|
| Paper producerの狭い修復 | UI/title汚染、根拠なしtarget PASS、失った条件を後段が再抽出する修復 | 本文範囲の抽出、targetごとの意味判断、限定回帰例の保守。必要な読解自体は減らない | **先行投資**。型や全stageを作り直す根拠はない |
| 既存chainからのread-only handoff projection | task/path/hash、rationale、unresolved、profile、directiveを人が探し直す仕事。ledgerだけを読む誤解 | exact/current basis解決、stale/missing表示、join検証、表示量の管理 | 条件付きで成立。品質の悪いCardを見やすくするだけで十分とはしない |
| 既存Cardのcontext等を使うsource-local supportの記録 | 後段のsupport箇所の再探索、何を読んだかの再質問 | source抽出時のlocating、抽出version・切断範囲の記録、意味的supportの確認 | 新canonical objectの前に試す候補。free textではmachine検証が足りないなら、その不足だけschema拡張を検討 |
| canonical Cardの表現力を保つ入力経路 | metric/comparator/別source帰属を文章から再構成する仕事 | producer入力とvalidationの対応拡張、既存inputとの互換性 | 複数source/比較を必要とする次の局所caseで必要性を確認。今回の4例だけで全面拡張しない |
| Selection materializationのexact照合 | directiveのID転記、profile_extensionsの手動比較、role取り違え修復 | directiveとMatrixの一意照合、機械生成不能な編集判断の明示 | W34の依頼にすでに方向性あり。未実行を成功実績に数えない |
| 新しい独立Consumption Record正本 | 現時点では既存の何を廃止できるか未実証 | 同じsource/claim/statusの二重保守・migration・review | **今は採らない** |

「recordがあるからreviewを省ける」「locatorがあるからentailmentは保証される」は認めない。増えたproducer作業が後段のreview/repairより安いかは将来の局所比較で測る。単にSolの仕事をworkerへ移しただけなら改善と呼ばない。

## 7. 安全性・一般化・未確定事項

### Observed facts

- 4例のpersisted hash/identity/field対応は補助結果のとおり。全件のCore検証ではない。
- paperのUI混入と、現在producerのunconditional target VERIFIED、入力→Cardの保存、RawのLimitations節の存在は直接確認した。
- 3 W34例の消費記録の形と生成ロジックは読んだ。main scripts/schemasにはledger/details filenamesのliteral参照が無く、追跡したacceptance chainもこれらの内容をsemantic validatorとして消費していない。外部の人間reviewまで存在しないとは言わない。
- SP001例のThematic contextは保持され、強い比較に必要なcheckpoint条件は未解決のまま残る。

### Working hypotheses

- source-local locatorとscopeを生成時に残す方が、後段が同じsupportを毎回探すより総仕事が少ない。
- paperの同じ生成方式は同種のfailureを別paperにも起こし得る。ただし件数・重大度は未計測。
- 小さいjoined packetで必要な意味に到達できれば、resumeやreview準備の手動再構成を減らせる。

### Unresolved evidence dependencies

- W34のcurrent-Core upstream再検証とSelection materializationは未実行のsnapshot。historical checkpointの古い実行SHAを、新しいreviewed SHAへ書き換えて解消しない。
- paperのsource-specificな内容をどこまで抽出すれば当該editionのCONTEXT判定に十分か、また他のpaperの重要omissionがあるかは未裁定。
- C019のhandread範囲・claim別support、SP001の外部source当時bytes／original semantic authoring経路は今回のchainだけでは証明できない。
- interactive runnerの単一entity/metrics制約が実運用でどれだけ追加作業を生んだかは未計測。
- fresh Weekly/Specialのreader品質、必要なindependent review強度、critic/transportの経済性、総work差は未検証。

**一般化できる範囲:** 共通v2 Card/View/Matrixを使うWEEKLYとTHEMATICについて、保存情報をlossy summaryから元artifactへ戻って取り出す設計は成立する。Profile差分を残す必要性を実例で示せた。

**一般化しない範囲:** RETROSPECTIVE_PERIODや全Special type、別号へのacceptance再利用、旧Specialのcurrent-main再検証、比較metricsや複数sourceへの全経路、全source kind、最終原稿/PDF品質。コードにprofile分岐が存在することは、そのprofileの検証済み実績ではない。

## 8. 次の投資と最小decision sequence

**推奨する次手は一つ: paper producerの狭い修復設計・局所較正。**

理由は、実際のaccepted artifactに至ったfailure chainを得ており、source/identity基盤を増やす前に解ける具体的問題だからである。副次的なmetadataの整理だけを先に行っても、この欠陥を再利用しやすくするだけになり得る。

次の明示指示がある場合に取り組むべき内容は、今回の失敗例を既知の較正例とし、本文領域・抽出上限・section対応・claimのsupport・target別判定をどう残すかを最小限設計すること。UI除去だけでPASSとせず、source-specific conditionsがCardに渡ること、未確認targetを未確認として残すことを終了条件にする。既存Cardのtext/context/verificationで足りるならschemaを増やさない。既知例への過適合を避ける必要が出た時だけ、同方式の別paperを限定的に追加する。

その後の分岐は二つだけ残す。

1. **意味を十分に表現できる場合:** 既存authority chainからのread-only packet/projectionへ進む候補を評価する。消える手動探索と、追加のprojection保守・review費を比べる。
2. **実例で表現力が不足する場合:** 既存producer/inputの拡張を先に検討する。canonical schemaにも不足があると具体的に示せた場合のみ、最小field/contract変更へ進む。

本書はW34のproduction判断を覆すreview、修復依頼、Gate decisionではない。今回のpaper findingを現在運用でどう扱うか、production優先度や再確認範囲はHumanおよび担当review roleの判断に残す。Sol reviewのhigh-signal改善を否定する全件結論にはせず、そのreviewだけではcoveredと扱えないpaper経路の新Evidenceとして提示する。

release maintenance、外部critic、全面shadow、全体role topologyの変更は今回の依存前提ではない。次の投資でもcritical authority保証や独立verificationを作業削減と交換しない。

## 9. 終了判断

成立するjoin、summaryから回収できる情報、未記録の情報、実際に壊れたproducer出力を区別できた。追加sliceは主に欠陥の頻度や外的妥当性を増す段階であり、次に小さなproducer修復を評価すべきという主判断を変える見込みは低い。

本Phaseをここで完了する。primary artifactは本書、補助は固定refのread-only probeとその結果のみ。production repository・refs・State・Selection・Human decisions・Gates・Publication Preview・Freeze・Releaseは変更していない。Pull/Push、external critic、prototype、shadow、production修復・採用・移行は行っていない。

[core-evidence]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/survey_evidence_v2.py
[runner]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/run_evidence_v2_interactive.py
[arch-core]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/survey_architecture_v2_base.py
[stage]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/scripts/survey_stage_validation_v2.py
[extract]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/body_extract.py
[generator]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/generate_evidence_input.py#L55
[w-card-c019]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/results/task-089aea0f0b318bee50b2.json
[w-card-paper]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/results/task-3cc4e37f782b5aba0ce7.json
[w-card-c033]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/results/task-c776ff2ef6ed21175ba8.json
[sp-card]: https://github.com/eariver/japanese-generative-ai-survey/blob/1b19a98511f9717d04b3b8f95207599fcdb7f48d/sources/SP001/evidence/v2/accepted/3785dc9ee87378b6682cc6d45a064cba1c9325bba4339dc04e460d441dcfb430/results/task-daa40564c14ee29d4dd3.json
[sp-matrix]: https://github.com/eariver/japanese-generative-ai-survey/blob/1b19a98511f9717d04b3b8f95207599fcdb7f48d/sources/SP001/candidate-matrix-v2.json
[sp-selection]: https://github.com/eariver/japanese-generative-ai-survey/blob/1b19a98511f9717d04b3b8f95207599fcdb7f48d/sources/SP001/candidate-selection-v2.json
[sp-arch]: https://github.com/eariver/japanese-generative-ai-survey/blob/1b19a98511f9717d04b3b8f95207599fcdb7f48d/sources/SP001/architecture-v2.json
[sp-raw]: https://github.com/eariver/japanese-generative-ai-survey/blob/1b19a98511f9717d04b3b8f95207599fcdb7f48d/sources/SP001/raw/postintegration-primary-source-observations-2026-08-25.md
[sp-request]: https://github.com/eariver/japanese-generative-ai-survey/blob/1b19a98511f9717d04b3b8f95207599fcdb7f48d/sources/SP001/execution/requests/postintegration-sp001-evidence-r3.json
