# J-GAS再構築全体の再評価と重点変更

日付: 2026-09-12 JST  
状態: **SYSTEM DIRECTION REASSESSED / PRIORITIES REPLACED / NO PRODUCTION ADOPTION**

## 1. 結論

**現時点では受理境界の実装検討を主経路として続けない。前回予定した「内部staging案をもう1つ試す」も保留し、研究上の問いからpublication・review・repairまでを通した仕事の比較へ重点を移す。**

これまでの検証は無駄ではない。既存canonical artifactsの表現力、Coreの具体的な検査不足、検査bytesと保存bytesの時間差、単純cacheの拒否能力低下、外側stagingの歴史互換性退行を実行で明らかにした。これらは今後の採用候補が満たす制約として残す。

しかし、ここ数単位は次々に見つかる局所的な安全条件を追い、**publication quality・全roleの実働負担・LLM利用・修復回数が改善するという中心仮説を未検証のままにした。** synthetic testsの追加成功は、その不足を埋めない。さらに、保存処理を1案改善しても、元のpaper読解不良、曖昧な問い、過度の編集圧縮、directive自身の誤り、意味を複数の役割が再構成する仕事は残る。

したがって、前回の停止条件を「もう1案の後」まで待たずに適用する。これは安全要件の引下げでも、既知の問題を放置してproductionへ新経路を入れる判断でもない。**reconstruct内で安全に行える品質・仕事量比較を、production受理コードの完成に依存させない**という投資順の変更である。

当面のarchitecture仮説は次とする。

> 既存authorityとcanonical artifactsを基準に、研究・編集判断の継続責任を明確にし、問い・source support・採否理由・本文での使用を意味を失わず引き継ぐ。機械はidentity/binding/転記/差分を担い、独立reviewは誤りとomissionを検出する。これが全役割の仕事を下げるかを、実際の読者向け出力と修復まで比較する。

「一つの編集責任」は全調査・全文生成・全reviewを一人へ集めることではない。「canonical直接authoring」はhashやboilerplateをLLM/Humanへ手入力させることでもない。追加役割、短い新payload、詳細な記録自体を改善とは数えない。

## 2. 何が証明され、何がまだ分からないか

今回の再評価は既存durable Evidenceの統合であり、新しいproduction観測、独立semantic review、費用実測ではない。main `005e598...`等は各記録時点の固定refとして扱う。

| Evidence | 判断に使えること | 使えない推論 |
|---|---|---|
| W34の過度の編集圧縮と#485の品質回復策：[mission](../brief/00-mission-and-success-criteria.md)、[Phase A refinement](astra-phase-a-architecture-refinement.md) | 元の問題には遅い品質発見とsupervisory負担増がある | 現時点でも同じ頻度で起きる、#485のreviewが不要、という断定 |
| paperのpersisted semantic defect、問いが切れたDiscovery要約だったこと：[Phase 2](astra-architecture-direction-decision.md)、[canonical ingress](astra-canonical-ingress-validation-decision.md) | 正しいstorageや構造PASSだけでは問い・意味・研究の十分性を作れない | 新candidateは独立review済み、全文を読めば必ず安くなる、という主張 |
| 3 Profilesで豊かなcanonical Card/Viewが受理された：[canonical ingress](astra-canonical-ingress-validation-decision.md) | 新semantic DSLなしでも表現・接続できる | Weekly/Specialのpublication品質、temporal sufficiency、運用経済性の証明 |
| W34 Selection 409 objectsを前版＋2 fieldsのdeltaで再構成：[Phase 3](astra-phase-3-boundary-and-execution-decision.md) | 転記・再組立てを減らす実物上の余地。directive側の誤りと機械実行は別 | review不要、全auditを局所化できる、409件の実働費を削減済み、という換算 |
| 4構造反例と共通境界補強、旧bytes保持：[stage/compatibility](astra-stage-boundary-and-compatibility-decision.md) | safety maintenanceの具体的な必要性と候補境界 | production全体の発生率、独立品質の改善、移行準備完了 |
| PR #487、W34の再導出費、N(N+1)のRaw hash：[validation work](astra-validation-work-and-pr487-decision.md) | 既存resolver再利用の実例と、機械的重複の確かな削減候補 | runtimeがtotal workの最大部分、cacheで安全に削減できる、という断定 |
| bytesとcacheの反例：[ownership](astra-byte-ownership-and-sharing-decision.md) | 操作内cacheでも不変basisの保証が要る。Card bytes束縛は局所改善 | OS並行性・全closure・production writeの安全性達成 |
| 外側stagingの互換性退行と検証費増：[staging tradeoff](astra-staged-acceptance-tradeoff-decision.md) | 外付けwrapperによる解決は費用とauthority互換に限界がある | staging一般が無価値、Core全置換が安い、という結論 |

未測定の中心は、実際のsource再読、production/supervisory reasoningのactive work、LLM利用、修復往復、Humanの質問・確認負担、実使用callerの頻度、各変更のfull audit費、今後のedition/変更頻度である。局所秒数やJSON bytesを、これらの代用にしてはいけない。

既知paperのcandidateは旧Cardより大きく、記録量が増えた。必要な比較条件を表せたことは前進だが、author負担増がreview/repair減で回収されるかは不明。詳細化を全候補へ一律適用する根拠はない。

## 3. 目的関数と品質条件を整理し直す

目的は**品質条件を満たす構成の中でtotal lifecycle workを最小化すること**。現行実装の既知bugや偶然の受理挙動を保存することではなく、現在意図している保証水準を維持することを基準にする。個別機構や配置は、その保証と歴史を保てるなら変更可能である。

比較は少なくとも次の仕事を含む。

| 軸 | 数えるもの | 見落としやすい仕事の移動 |
|---|---|---|
| production operations | source取得・準備・読解、authoring、入力/参照探索、実行・再開 | 短いworker出力の不足をsupervisorが補完する |
| supervisory reasoning/review | 独立な問い/omission確認、意味判断、反例探索、findings処理 | workerが減った分をeditorの全件再読で埋める |
| repair/regeneration | 原因診断、意味差分の修復、下流再生成、再review | deltaだけ直したように見せ、監査・判断のやり直しを除外する |
| CI/runtime | validation、audit、hash、I/O、失敗再実行、待ち時間 | fast pathのためのsnapshot/cache/CI保守を数えない |
| LLM利用 | author/editor/reviewer/operator各roleの実測usageと再開context | 別agent/session、裏のpreparation、review回答生成のusageを除外する |
| operational complexity | active routes、契約、adapter、設定、例外、runtime依存の維持 | 既存処理を外さず便利な層を積む |
| Human handoff/manual burden | 必要な裁定、説明再要求、参照探索、手作業、確認のactive time | agent間の不一致をHumanに毎回統合させる |

初期architecture investment、migration、二重保守、歴史互換の費用も別建てで含める。長期削減が十分なら大きい投資も排除しない。一方、将来の回数・削減量が不明なのに「長期なら回収できる」とは置かない。

異なる単位を恣意的な点数へ足さない。同じ品質で各軸が改善するなら選びやすい。trade-offがある場合は、実測差・頻度・初期費からどの運用条件で有利になるかを示す。例えば同じ費用単位で初期増分I、1反復当たり純削減sが裏付けられた場合だけI/sを回収反復数として計算する。sが未知、負、またはHumanへ移しただけなら回収を主張しない。

品質条件は平均scoreで相殺しない。

- publication: 読者に必要な重要事項、比較条件、反対材料、採否・omissionの妥当性。ページ数やclaim数を代理の合格基準にしない。
- provenance: claim/metric/subject/source/時点と保存根拠が対応し、不明なcaptureは不明のまま。
- fail-close: machine-checkableな不正やstale bindingを通さない。semantic uncertaintyをVERIFIEDへ自動昇格しない。
- Human authority: adoption/priority/Gates/Freeze/Releaseの権限とexact対象を維持。比較実験で決定を上書きしない。
- generality: Weeklyの広さ・期間とSpecialの系譜・比較・歴史を同一の単純な基準で潰さない。
- history: 当時のbytes/contract/判断の検証と、現在の利用可否を区別。新生成の同じ文章への収束を歴史再現性の代用にしない。

## 4. Architecture directionの維持・変更

| 項目 | 今回の判断 |
|---|---|
| 既存authority Core/canonical artifacts | **基準として維持。永久固定ではない。** 既に防ぐfailureと歴史資産を捨てる費用があり、同等保証をより安くする代替の実証がない |
| A+＋薄い機械補助 | **比較基準として維持し、最終推奨との区別を強める。** 表現適合性は成立、lifecycle優位は未実証 |
| authoringとmaterializationの責任分離 | 維持。ただし新service/DSLではなく、意味を失う転記をなくすための責任境界として使う |
| 一つの継続した編集責任 | **実験対象へ戻す。** 問い・採否・記事への利用を毎stage別の役割が作り直す仕事を減らせるかを問う。固定model/常駐人数は決めない |
| independent review | 現行責任・停止点を維持して比較。自分の再読や別promptを独立reviewと称さない。削減・統合は別の十分性Evidenceが必要 |
| Core maintenance | 既知の不足と実験結果を保守backlogへ固定し、主経路から外す。採用時に必要な安全補強は免除しない |
| 内部staging、cache、全stage共有 | **今は実装しない。** 前回の「次に1案」の約束を撤回。重複の存在だけでは総費用改善の投資順を決めない |
| canonical全件の最大詳細化 | 採らない。問いを答え、重要な不確実性を保存する最小十分な内容を比較する |
| Core全置換・外部workflow/CAS導入 | 現時点では選ばないが閉じない。安定した意味経路でも保守/authority仕事が支配的と測れた時、同じ保証・歴史・移行費込みで比較する |

Phase Aで提案した編集責任の継続は、今までに実証された優位ではない。これを再び提案書だけで推奨するのではなく、A+と同じ機械補助・品質条件で比較する。Bを縮めた経緯も、追加architecture investmentの一般的な否定には使わない。

## 5. 次の主作業：研究・編集の一往復を比較する

次の最優先は、**同じsource/対象範囲から、問い→Evidence→editionでの意味・採否→読者向け本文→review→修復を通す、小さい比較の準備と実行**である。Cardだけ、writerだけ、秒数だけの比較を追加しない。

### 比較する仮説

まず、実際に使われる入口・directive・reviewの責任を対象sliceに限って確認する。source treeにある旧runnerを「現行baseline」と決めつけない。過去出力はfailureと必要品質を理解する資料とし、過去に記録されていない時間/usageを推計して新実行の費用と比較しない。

| 比較相手 | 内容 | 問えること |
|---|---|---|
| A：canonical表現改善を主とする経路 | 現行の意味判断・review責任を保ち、full canonical表現と既存の機械補助を使う | 情報を狭める入口を外すだけで十分か |
| B：問いと編集判断の継続を加える経路 | Aと同じ表現・source access・機械補助・review責任で、sourceに何を問うか、回答/不確実性をどう採否・本文へ使うかの継続責任を明示する | 意味を後段で再構成する往復を、全role合計で減らせるか |

Bで元の問いが変わることは隠さず、両案に共通のProfile/読者目的/品質基準に対して評価する。canonical形式の変更、モデル変更、review削減、Gate変更を同時に行って勝因を不明にしない。これはBのsemantic DSL復活ではなく、仕事の単位・責任の比較である。

### 最小の開始範囲

既知paperはsource supportや比較条件の評価項目を校正する資料に使う。既に答えを知っているので、これだけで新手法の品質優位は主張しない。

最初の比較対象は、まだ両案の答えを作っていない小さいsource群とし、採用候補だけでなく落とす/保留する対照候補も含める。sourceを選んだ後、出力を見る前に必要な読者価値・時点・重要な反例・未確認条件を固定する。Source選定はknown answerの作りやすさではなく、判断を変えるfailureを問えるかで決める。

Weeklyでは期間内の重要事項と過少選択を、Specialでは比較/系譜/時点と欠けた歴史を問う。最初の一往復で優位がなければ機械的に全Profileへ広げない。有望な差が出た場合に、異なるfailureを持つ他方のProfileで反証を試す。小sliceの成功をedition全体やWeekly/Special generalityの達成とは数えない。

reconstructではunadopted candidateとread-only評価資料を作れる。accepted TaskやStateを書き換えて新しい問いを試すことはしない。current policyが要求する全候補disposition、review、admission、Human Gateを省いた実験は、その省略分を費用削減として算入しない。将来の研究深度配分の変更を比較する場合も、現行のcoverage義務を消した結果と区別する。

### 評価の順序と独立性

1. 同じ入力条件、適用policy、品質要求、失敗条件、計測可能な費用を先に固定する。
2. 両案で意味生成から短い本文と理由・未選択/保留・残余不確実性まで作る。既存canonical artifactsを使い、別のConsumption正本や判断storeを追加しない。
3. reviewerはsource・Profileから必要な内容/強い反例をまず確認し、その後候補と照合する。案名や期待される勝者を評価根拠にしない。必要なsourceへのアクセスは削らない。
4. findingを修復し、再review、canonical差分、必要な再生成範囲、Humanへ残す判断まで追う。既知の正答を渡した無損失変換だけで終了しない。
5. 品質未達・重大なomission・unsupported claimがあれば、その案は費用が低くても不合格とする。両案不合格なら共通の問い/source/役割設計を見直す。

独立reviewを実施するには非著者の評価が必要で、現sessionの自己再読だけでは満たせない。今回それを実施したとは扱わない。比較資料の準備・source照合・検査設計は進められるが、実際の独立評価が得られるまでquality non-inferiorityの結論は保留する。Humanを無償の追加reviewerや費用計測係へ割り当てない。別agent/外部への委任・送信もこの文書で実行済みとはしない。

## 6. 比較を仕事の移動で終わらせない記録

恒久telemetry systemを先に作らない。比較中の各作業を、役割・対象・行動・理由・結果に対応付け、既存ログから取れるusage/時間/実行回数を使う。

| 記録 | 判断への用途 |
|---|---|
| roleごとのactive work、source再読/参照探索、handoff、質問・補完 | editorやHumanへの仕事移動を検出する。wall timeとactive timeを分ける |
| LLM実測usage/費用、context再ロード、再試行 | 取得不能はunknown。文字数からtoken/金額へ換算しない |
| findingの発見位置・重大性、修復回数、修復後の残余 | 早い発見で何のやり直しを避けたか。見つけた欠陥数が多いだけで悪化としない |
| runtime/CIの必要処理、実測と未実行の区別 | production admissionを省いた速さを比較から除く。共通費用も総額に含む |
| 追加する処理・外せる現行処理・未廃止の二重経路 | retirementなしの層追加を検出する |
| Humanに残る具体的な判断と、その根拠への到達 | 短いhandoff文書に情報を隠しただけかを検出する |

最初に問うのは精密な年間ROIではなく、「品質を維持した完了状態へ到達するまで、誰の何の仕事が実際に消えたか」。信号がなければ大規模な計測投資を止める。信号があれば、source/Profile変更、修復、再開、歴史参照という異なる条件で持続するか調べ、そこで初期投資の回収可能性を評価する。

## 7. 改訂roadmapと再開条件

**旧roadmapの内部staging試作を次回のdefaultにしない。本書が今後の優先順位を置き換える。**

| 領域 | 今の扱い | 再開・拡大するEvidence |
|---|---|---|
| 研究・編集の一往復比較 | **主経路。次に準備・実行する** | Bの利益がAで既に得られるならAへ縮小。Bだけに全roleでの純削減が出れば境界設計を具体化 |
| 4構造反例・Card bytes補強 | 保守候補として保持。追加fixture作成をdefaultにしない | 新経路のproduction採用候補化、またはactual incident/active routeの阻害により必要性が確定した時 |
| 内部/外側staging・Raw cache・basis共有 | 実装保留。外側wrapperは不採用 | 実際のworkflow所有権/失敗頻度/全工程費用が投資を正当化し、保証を低下させない小さい設計が提示できる時 |
| CI/audit粒度、repair automation、generated handoff view | 主比較で仕事を記録し、必要なら対象を1つ選ぶ | 意味の改善後もその費用が支配的/反復的と分かった時。Gate/audit緩和の先取りはしない |
| role数・review回数・model family変更 | 固定せず、現行条件でまず比較 | 品質escape/omissionと全role費用を比較できる時。別modelへ移すだけでは採らない |
| Core置換・外部OSS/framework評価 | 保留 | 既存Core内部の小修正では反復する維持費を減らせない根拠と、代替を同じ保証で比較する具体的な問いがある時 |

新しいproduction変更の連絡があれば、該当する仮説と固定Evidenceだけを更新する。毎回main/全歴史を再crawlしない。観測した1つのruntime hotspotや新しいfailureがあるだけで全体の主経路を再び局所修復へ移さず、緊急の保守とarchitecture投資の価値を分ける。

安全補強を保留してよいのは、現在の作業がreconstruct内の分析・候補比較でありproduction adoptionではないためである。採用時には不足する保証を解決する必要がある。今回の保留を既存productionに対する安全認定・運用継続承認として使わない。

## 8. 今回の完了範囲と継続入口

今回完了したのは、全体目標に対するEvidenceの強度の再分類、局所実装を主経路にする判断の撤回、architecture仮説の更新、公平な次比較と費用・品質・停止条件の具体化である。新prototype、production試験、独立review、費用削減実績は追加していない。

今後は**本書§1・§5・§7**を起点にする。過去のphase文書や実験scriptを順に再実行しない。必要な資料は本書のリンクから選択readする。過去のpatchは採用済みではなく、失敗例を含む固定Evidenceとして保存する。成果物を増やすこと自体を進捗にせず、次の比較で何を選べるようになったかを終了基準にする。

production repository、State、Human decisions、Gates、Freeze、Release、adoption/migrationは変更していない。Git Pull/Push、reconstructのcommitも行っていない。
