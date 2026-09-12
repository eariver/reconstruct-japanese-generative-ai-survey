# Phase 4 — 比較の基準を実運用とsource読解に合わせる

日付: 2026-09-12 JST  
状態: **PHASE 4 STARTED / FIRST BOUNDED INVESTIGATION COMPLETE / NO PRODUCTION ADOPTION**

## 1. 今回の判断

Phase 3-Gの重点変更を維持する。**次に検証するのは、既存の研究・編集責任の下で、問いに答えられるEvidenceと採否理由を作り、本文・非著者review・修復まで完了するための総作業量である。** acceptance/staging/cache実装は再開しない。

今回のread-only調査により、比較条件を次のように更新する。

1. **「継続責任を新設するB」は独立した処置として採らない。** 現行governanceはすでに監督役に研究の十分性、source消費の確認、materiality、Selection、Architecture、Human向け説明の責任を置く。W34の実artifactにもreader questionとboundaryの引継ぎがある。Phase 3-GのBのうち、責任者を明示するだけの部分はAの共通条件へ吸収する。
2. **Aの経済性・品質は未証明のまま。** canonicalの豊かな表現、sourceを保存したこと、監督役の存在だけでは、sourceの意味を十分に消費したことにならない。未選択paperの固定Rawと受理Cardの照合で具体的な不足を確認した。
3. **比較では「意味を誰が補完したか」を最後まで数える。** 手書きの高品質product overrideと自動抽出paperを、同じauthoring作業の成功例として比較しない。editorが埋めた欠落、補助script、準備と再読を含める。
4. 次はまず**full canonicalを使うAの、品質条件を満たす小さな完了例と全roleの費用記録**を作る。そこで段階間の意味再構成が残る場合に限り、同じowner・表現・reviewで仕事の順序/単位を変える比較を具体化する。Bの追加storeや新しいreview層を先に作らない。
5. 本sessionはこの比較基準の修正と実Evidenceの固定で区切る。新規sourceでの比較出力、独立した試験review、修復後の品質非劣化、費用優位は**未実施・未実証**。Phase 4全体の終了や最終architecture選定ではない。

目的関数・品質制約は[Phase 3-G §3](astra-system-direction-reassessment.md#3-目的関数と品質条件を整理し直す)を継承する。仕事の役割間移転は削減に数えず、同等保証と移行/保守費込みで優位が示されればCoreやrole構成の再検討を妨げない。

## 2. 観測範囲と基準の確定

### 固定refと実施内容

- mainの観測/分析ref: `005e59841272464307386abfc11f5b09228f0814`
- 調査開始時のremote `weekly/2026-W34-v2-work`および4件の固定分析ref: `601481acd9b82ee8fa0c2eb28a2ca28636165d60`
- 開始時はPhase 3最終観測と同一。固定分析refのStateは`ARCHITECTURE_ESTABLISHED`、Architecture approved、Publication Preview pending、next action `stage:drafting-synthesis`、Draft checkpoint pending。
- **終了時の追加観測:** W34が`899d3d6ab96c14bb82ea24b0ae12700e798a781f`へ1 commit進んだ。[late-observation.json](../notes/phase-4/late-observation.json)で差分とStateを別保存。Draft/Synthesis・検証record・Draft checkpointの追加とState変更であり、今回のEvidence/Selection/Architectureは変更されていない。新Stateは`DRAFT_COMPLETE`、next action `stage:reader-publication-validation`、Publication Preview pending。以降の進行は追跡していない。
- 選択基準: continuityが働くselected例、既知のdirective修復例、明示的な未解決HOLD例、未選択paper例。4件の**目的抽出による歴史標本**であり無作為標本ではない。paperはMatrixで見つけたCASを使用。出力確認前のpreregistered sampleでも、未知sourceに対するA/B試験でもない。

[basis.json](../notes/phase-4/basis.json)に取得対象の固定ref・Git blob SHA-1・SHA-256・URLを保存した。[trace.json](../notes/phase-4/trace.json)は4件のTask→Card→View→Selection→Architectureの抽出。Task/Card/ViewはStateのEvidence checkpointが名指すacceptanceから辿り、対象bytesのbindingを照合した。Matrix/Selection/Architecture間の名指しhashも確認した。

**これはCore全検証ではない。** Raw closure全件、全stage依存、全歴史、並行性、Human Gate admissionを再実行したわけではない。CASのRawだけはSupplementのhashとも照合して、方法・実験・Limitationsの該当部分を読んだ。他3件の外部source本文の意味的再検証はしていない。

### 実使用経路と、混同しないもの

| Evidence | 今回確認したこと | 比較上の意味 |
|---|---|---|
| [現行governance §2–4・8][governance] | 監督役の継続した意味判断、未選択sourceのrisk-based inspectionがすでに必要 | Aからこの責任を引き去ってBだけへ与えない |
| W34 `generate_evidence_input.py` と `session-worklog-evidence-resume.md` | productは手読解override、paperは抽出script。worklogは409件のinteractive inputとconsumption ledgerを記録しCoreのinteractive Evidence経路を指す。受理Cardに対応内容が存在 | source tree上の旧runnerだけをbaselineとしない。記録は実行由来の資料であり、今回そのgeneratorを再実行したわけではない |
| W34 Selection r2とArchitecture directive | supervisor-owned意味判断のmaterialization、修正の限定、reader question・must-cover・boundaryを具体化済み | 意味の継続は全面的に欠落しているわけではない |
| [post-#487 Drafting request][draft-request]と終了時のworklog | canonical Drafting/Synthesis、既存Architectureの保持、semantic/visual review、sidecarの要求。新worklogは`run_drafting_synthesis_v2_agent.py`の実行と7 packagesのPASSを報告 | 開始時はDraft pending、終了時はDRAFT_COMPLETE。reader/publication validationは新Stateでもpending。今回、新Draftの意味品質やPDFをreviewしたわけではない |
| W34 `execution/index.md` | 旧80件・SELECTED 1・Architecture pendingの案内が残るが、現行Selectionは409件・41 selectedでStateはapproved | 手動handoffの不一致を観測。ただし頻度/負担は未測定で、generated indexの実装へは転進しない |

script/worklog/Task等のexact pathはmanifestとtraceにある。運用役の記録上のbindingはこのW34標本ではMuse Spark 1.3の実験的Luna-role substitutionであり、役割名からモデル性能を推定しない。

## 3. 4件の追跡結果とsource反例

| 対象 | 追跡で確認したこと | 支持しない結論 |
|---|---|---|
| `w34-event-c019` Mistral Agentic Search | Taskはmulti-step retrievalとmaker benchmark境界を問う。Cardに機構/帰属、Viewにwhy-this-issue、Selectionにprimary anchor理由、Architecture Package 2に検索・読解・refineとbenchmark境界がある | 新しい継続ownerが必要、source読解が完全、本文品質が合格、という結論ではない |
| `w34-event-c045` regional processing | Taskの問いはcapture不足という準備課題。Cardはその解決を記録。誤ったclusterはSol directive r2でdeployability側へ修正され、SelectionとPackage 4がその判断を保持 | identity/hash補助が意味判断の誤りを予防する証拠ではない。今回修復時間は測っていない |
| `w34-event-c033` OpenRouter rankings | Taskの39-model benchmarkという問いをCardがUNRESOLVEDとし、View/HOLD理由が未確認内容を保持。Architecture placementなし | 落とす候補は一律にsourceを読んでいない、という主張への反例。追加探索の十分性は今回未判定 |
| `w34-event-arxiv-2608-20771` CAS | Taskは切れたDiscovery abstractを引き継ぐ。Cardの方法説明にUI由来の文言、genericな解析上のlimitation、Viewはprovisional CONTEXT。SelectionはMATERIAL非成立を理由にHOLD、placementなし | 論文を必ず選ぶべき、全paperが不良、既存reviewすべてが無効、とは結論しない |

### CASの反例を再確認できる根拠

対象RawはW34のSupplementに含まれるHTML `2608_20771.html`、SHA-256 `81703068b769326d461a92974341333c81946a7c8f2b632e933925a288844ed2`。取得時刻は記録上`2026-09-08T14:40:19Z`。今回の外部live pageの状態とは混ぜない。exact pathとHTML sectionのbyte offsetはtraceの`paper_source_check`に保存した。

**P4-F1 — 方法説明がsourceの方法を伝えていない。** 受理Cardのclaim-1は `proposes Aptive Retrieval and Policy Weighting Title: Content selection saved.` を含む。RawのUIには`Title: Content selection saved.`があり、方法の節は別に存在する。§3.2は検索結果集合のAPSによる適応的切詰め、§3.4はACIによるconfidenceに応じた学習時の重み付けを説明する。この2点の差を問う材料は保存されているが、claim-1からは得られない。

**P4-F2 — 実在するsource-specific limitationsが未消費。** Cardは専用Limitationsをsection parserで捕捉しなかったという観測を記録する。Rawには`id="S7"`の「7 Limitations」があり、著者は一般的なopen-domain QA以外への適用が未検証であること、calibration set作成に強い外部teacherを使うこと、中間推論過程まで保証を拡張していないことを明示する。Cardの文言は「論文にlimitationsがない」と断定してはいないが、解析失敗の記録はこの実質的内容の代わりにならない。

**P4-F3 — 読解済みラベルを十分性の代理にできない。** CAS ledgerは`AUTHORITY_CONSUMED`、CardはPARTIALだが当該verification targetはVERIFIED。`generate_evidence_input.py`のpaper経路は、targetごとの意味評価とは別に同型のVERIFIED findingを作り、provisional materialityをCONTEXTにする。さらにbound bodyがありstatusがVERIFIED/PARTIALならconsumptionをCONSUMEDにする。`body_extract.py`はHTMLを空白1行へ平坦化し、section parserは短い行数ならfull bucketへ戻すため、source固有の節を落とし得る。

これらは保存Raw・受理出力・source code間で確認した**局所的な意味情報の不足**である。script全件再実行や欠陥率推計はしていない。コード上の経路と記録の一致は、全履歴の完全な実行provenance検証とは区別する。

**編集上の未解決:** CASは選択済みのretrieval packageと近い研究上の問いを持つが、類似topicだけでは週の重要度や採用を決められない。著者報告だからCONTEXT、CONTEXTだからHOLDという経路に対し、source固有の方法・比較条件・限界を踏まえてもHOLDかを確認する余地がある。既存HOLDを変更したり、production reviewへREQUEST_CHANGESを記録したりはしていない。

このcaseは今後**校正用**。今回見た答えを使ってA/Bの未知source性能や費用差を測らない。新たな手書きCardをここで一つ作っても、独立reviewと仕事量の比較がなければ中心判断は変わらないため、その追加生成は行わなかった。

## 4. 比較する構成を整理し直す

| 構成 | 定義 | 現在の扱い |
|---|---|---|
| 現行観測例 | W34のmixed authoring、canonical materialization、既存supervisory reviewとdirective | failure/品質要求/実経路を知る歴史標本。記録のない費用は新実行と比較しない |
| A：意味を十分に記したfull canonical＋共通機械補助 | sourceに対する問い/回答/不確実性、Viewのedition上の理由、Selection、Architecture、本文の責務を既存roleとcanonicalで遂行 | 次に小さな完了例を作って評価する基準案。完成済みprototypeでも最終解でもない |
| 旧Bの「継続ownerを明示」 | 既存governanceの責任を改めて宣言 | **Aへ吸収。単独の比較armにはしない** |
| 残る対案 | 同じrole/入力/表現/reviewで、source読解時の問いと後段利用をまとめる作業順序・単位の変更 | Aで反復する意味再構成が実測された場合に具体化。今は追加契約/storeなし |

これはBのすべての利益がAで実証されたという判断ではない。**責任分担の差が観測できない部分を対照実験から除く**だけである。Aで意味の補完やHumanの追加説明が膨らめばAも不利になる。source/cardの良い例だけを採ってAが完成したとはしない。

再利用できる置き場所はすでにある: Profileの`research_scope.question`、Taskの`verification_targets`、Cardの`verification.targets`/claims/metrics/limitations、Viewのmateriality rationale、Selectionのrationale、Architectureのpurpose/must-cover/boundaries、DraftのEvidence refs/coverage/boundary handling。編集上の採否はfactual Cardへ混ぜない。Taskを変える場合もreconstructの新しい候補として準備し、accepted Taskへの後書きはしない。

## 5. 次の小さな実行を具体化する

次の入口は**Aの品質を満たす完了過程を観測する小試験**。大きなshadow editionや計測基盤を作らず、以下の条件を出力作成前に固定する。source群の選定と実行は未着手であり、本書は実行済みの結果を先取りしない。

1. **source選定:** Weeklyの一つのreader questionに関係する3–4候補。機構/評価を持つpaper、product/実装の一次source、同じ話題でも期間外・別subject・source未解決等で落とす可能性のある対照を含める。今回の4件とPhase 3の既知paperは除く。採用/HOLDの正答を先に固定しない。読者目的、cutoff、調査lane、許されるsource拡張、Profile義務を先に記す。
2. **source選定後・出力前の固定:** exact URL/version/取得bytes、取得時点、問い、重要な比較条件、強い反例、品質条件を記録。source拡張で出力条件が変わったら版を上げ、変更分の仕事を数える。reviewerの別探索は妨げない。小slice外のDiscovery/全候補coverage/Grok/carry-over等を実施したとは扱わない。
3. **生成から本文まで:** source本文を読む作業を含め、canonical Card/View、全slice候補の採否、短いpackageのpurpose/must-cover/boundaryと日本語本文まで作る。hash/identity/参照は共通機械補助で扱う。補助にない仕事を追加実装するなら初期費として記録する。別の意味正本は作らない。
4. **review:** 非著者がまずsourceとProfileから必要内容と反例を確認し、その後候補を照合する。採用候補だけでなく強い未選択例を含める。本文からRawへ自由に調べるのはreview側であり、Draft authorがaccepted Evidenceを外部知識で補修する経路にしない。
5. **修復:** findingの原因がTask、Card、View/Selection、本文のどこかを分け、変更bytes、依存する再生成/再review、残る不確実性まで記録。production Gateを通ったと仮定しない。新しいcandidate本文に対する同じauthorの再読を独立reviewに数えない。

合否は次の独立条件で扱う。平均点で相殺しない。

| 条件 | 最低限確認する内容 / 不合格の例 |
|---|---|
| source consumption | reader questionに答える機構・比較条件・source固有の限界を特定。UI文字列、抽出成功、CONSUMEDラベル、汎用の「未再現」注記だけでは不十分 |
| materiality / omission | timingだけで採用しない。author-reportedだけで自動不採用にしない。強い未選択例を本文と同じ読者目的から説明できる。妥当なHOLDも成功状態 |
| reader value | 読者が何が変わり、どの条件で意味があり、どこまで不明かを理解できる。claim数や文章量は合否の代理にしない |
| provenance / safety | subject/comparator、source/version/時点、claimと根拠を対応させる。不明をVERIFIEDへ昇格させない。機械検査PASSから意味PASSを導かない |
| authority / history | 全出力はreconstructの未採用候補。既存Gate/State/旧bytesを上書きしない。reviewは対象版と依存先を明示する |

数値差を書く場合は同じbackbone/評価集合/条件と比較subjectを明示する。CAS校正なら、本文§4.1–4.2/Table 1–2の条件を確認し、論文の統計的保証を任意領域・推論過程全体の保証へ広げないことが検査項目になる。この既知答えを次の試験sourceの代用にはしない。

**拡張条件:** Aが品質条件に到達し、実際の重複読解・handoff補完・修復の所在が分かったら、外せる仕事を名指せる対案を一つ選ぶ。A/B双方を同じsource/補助/reviewで比較する際は答えの漏洩を防ぎ、準備費とrepeated measuresによる学習を区別する。Aが不合格なら先に問い・sourceアクセス・表現・reviewの共通不足を見直す。有望な純削減が出た後にSpecialの系譜/時点/歴史という異なるfailureで反証する。

## 6. 全roleの費用と、このsessionの未計測

| 軸 | 次の小試験での記録 | 今回の証拠の強さ |
|---|---|---|
| production operations | 取得、本文読解、canonical記入、準備script、参照探索・再開 | W34はproduct overrideとpaper抽出の異なる仕事を確認。実働分数はunknown |
| supervisory review/reasoning | sourceの再読、未選択調査、意味補完、directive作成と照合 | responsibilityと実recordは存在。必要十分なreview量・改善量はunknown |
| repair/regeneration | 発見点、原因層、修正・下流生成・再review、解決まで | c045の限定修正は歴史証拠。CASを本sessionで修復/再reviewしてはいない |
| CI/runtime | 必要なadmission/audit/build、再試行、待ちとactive work | 今回Core/CI/PDF実行なし。終了時のproduction worklogには7 packages＋synthesis実行が約4時間との報告。今回の計測でも全工程の支配性証明でもなく、初期の全工程費用記録で照合すべき信号。省略分を削減に算入しない |
| LLM利用 | preparation/author/editor/reviewer/operatorと再開contextの実測usage | W34と今回調査のrole別token/料金はunknown。文字数・API読込bytesから換算しない |
| operational complexity | 増える契約/補助/route、廃止できた旧作業、二重保守 | 新しいproduction routeなし。調査scriptは準備費であり削減実績ではない |
| Human | 必要な裁定、説明再要求、参照探索、active work | Gate権限維持。追加reviewer・計測係をHumanへ割り当てていない。将来負担はunknown |

この調査にもAstraの読解/判断、GitHub取得、4件抽出、source照合、文書化の費用がある。費用差が取れない状態でROIは計算しない。途中の大きなtree応答や取得/表示のやり直しも準備側の仕事であり除外しない。APIの取得時刻はagent active timeではない。

同じ費用単位で初期増分Iと、全roleを含む反復純削減sが測れた場合のみ回収I/sを使う。削減の裏で未選択review・source読解・admission・Human説明が増えていれば合算する。sourceごとの1件当たり費用を全Weekly/Specialへそのまま外挿しない。

## 7. 停止理由・再開条件・権限

今回、旧A/Bの一部が現行governanceと重なり、別の品質差を無意識に混ぜる危険が確認できた。また、保存済みsourceを増やすことも継続ownerの宣言も解かない意味情報不足を1件固定した。**比較の識別可能性と品質条件を変えるEvidenceが得られたため、ここを最初の支持された判断面とする。** 追加の全号crawl、同じsourceの手書き比較、parser修理を続ける情報価値は低い。

次sessionは[Phase 4 handoff](../handoff/astra-phase-4-continuation.md)から入り、§5のsource選定・条件固定・小さな完了例へ進む。非著者reviewとrole別usageの取得方法は実行前に確認する。未準備ならsource/入力/候補準備は可能だが、品質非劣化・経済性・採用は未判定のままにする。委任や外部送信は本書によって実行済み・許可済みにはならない。

production `eariver/japanese-generative-ai-survey`はread-onlyのまま。P4-F1–F3はreconstructの調査findingであり、productionのReview/Gate/State判断ではない。productionの修正・採用・migration、PR/Issue投稿はしていない。通常Pull/Pushと最終commitはHumanが行う。

runtimeが全工程費用を支配する実測、新しいproduction blocker、canonical内部で同等保証を維持できない具体的な不適合が出れば保留領域を再評価してよい。今回のCAS反例だけでCore置換、新DSL、review全件化、恒久telemetry、特定parser patchを新しい主経路にはしない。

[governance]: https://github.com/eariver/japanese-generative-ai-survey/blob/005e59841272464307386abfc11f5b09228f0814/docs/survey-production-core-v2-sol-luna-review-governance.md
[draft-request]: https://github.com/eariver/japanese-generative-ai-survey/blob/601481acd9b82ee8fa0c2eb28a2ca28636165d60/sources/2026-W34/execution/requests/sol-post-core487-drafting-resume-20260912-r1.md
