# Astra next-phase decision

決定日: 2026-09-09 JST  
状態: **NEXT PHASE SELECTED / EXECUTION NOT AUTHORIZED / NO PRODUCTION ADOPTION**

## 1. 選定する single next phase

**既存の意味成果を再利用・受渡しする最小契約の適合性検証**を選ぶ。

主種別は bounded mapping / feasibility validation。現行の source・Evidence・消費記録・edition判断を少数の実例で縦に追い、**どの既存情報を正本として使えば、意味とauthorityを失わず、次の役が研究や編集判断を作り直さずに済むか**を判定する。新しいConsumption Recordを作ることも、過去の五つのlogical productsを物理実装することも、結論に先置きしない。

このPhaseの成果は、最小の変更候補とその適合性を示す一つの検証報告である。productionコード、全面的なschema inventory、shadow用の第二production systemは作らない。次に投資する対象を「既存構造だけのprojection」「狭いproducer/consumer修復」「不足情報の限定的なcontract追加」「変更不要」のいずれかまで絞る。

本書はPhase選定だけを完了する。選定した検証自体は、Humanの同一セッションでの明示的な継続指示を待つ。

## 2. Fresh production reality — 今回確認した固定点

確認時刻: 2026-09-09 23:35–23:40 JST頃。以下は観測時点のsnapshotであり、将来のHEADを保証しない。

| 対象 | 確認したref / SHA | 意味 |
|---|---|---|
| writable workspace | local HEAD = remote HEAD = `d34ce896eb727b733451ba70a29bc92873c63e33` | 作業開始時のtracked/untracked差分なし。最新bootstrapをローカルから読めた |
| production main | `6d748a962d57beff89da7c1b20cb5a9a86c8e261` | Phase A baseline `0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc` より2 commits先 |
| production W34 work branch | `weekly/2026-W34-v2-work` = `030eb723c12282f0cfd09aaada05d14f0c0906c7` | Phase A W34 baseline `993583e871bcbfea7bfe700fe5c6f2648e8887c0` より12 commits先。mainと別に確認した |

確認手段は `git ls-remote`、GitHub APIのcompare/commit/contents/PR read、ローカルに既に存在するproduction Git objectの固定SHA `git show`。Pull/Push/Fetch/checkoutはしていない。W34の最新objectはローカルに無かったため、固定SHAのContents APIを使用した。

### 直接観測した事実

1. **mainの追加修正はsource taxonomyの接続修復。** [#486][pr486] のdiffはEvidenceのsource-class対応5件とunknown type rejectionの回帰testに限られる。PR説明では329 fresh tasksを阻んだ問題として報告されている。これは消費contract全体の再設計でも、research品質の実証でもない。
2. **W34の現在Stateは `EVIDENCE_REVIEWED`、next actionは `stage:selection`。** Evidence/Materiality/Completenessはpassed、Selection/Architectureと両Human Gatesはpending。[State][state] 旧handoffの `CANDIDATES_NORMALIZED` を現在値として使わない。
3. **旧C019の症状は新カードにそのまま残っていない。** 新accepted set `647cde46…` の[C019 card][card]には、multi-step retrieval、五つの操作、maker-reported evaluationなど候補固有のclaims、source-specific limitations、verification findingがある。これはカード内容の直接確認であり、今回Raw本文を再監査して全claimの正しさを認定したという意味ではない。
4. **consumption情報は既にeditionの実行領域に存在する。** [authority-consumption-ledger][ledger]のC019行はtask/discovery identity、body path、target、状態、理由等を持つ。[consumption-details][details]の同例は `method=override_handread` とbound source IDsを持つ。この二つの行だけからclaimごとのsource span再現性や全件の十分性は言えない。新しい同名の正本を追加する前に、これらとSupplement/Cardの関係を調べる必要がある。
5. **既存schemaは意味情報の相当部分を既に表せる。** 現行[Evidence Card schema][schema]はsubject、evidence class、source IDs、context、metricのunit/comparison、limitationsを持つ。一方、明示的なclaim単位のRaw span/digest fieldはこのschema内にはない。Raw bindingがシステム全体で欠けると結論せず、Supplement等とのjoinを未確定事項とする。Cardの `issue_id` とtask/Screening/prompt/contract hashesも維持されており、別号への受理のコピーを正当化しない。
6. **編集責任とmaterializationの分離は現在運用にも現れている。** [Sol Selection directive][directive]は41 MATERIALを10 PRIMARY / 31 SUPPORTINGに分け、残る368をHOLDとし、clusterとexact identityを指定する。[materialization request][request]は既存CoreからMatrixを導出し、この決定を転記・検証するよう求めている。ただしState上、これは未実行の依頼であり成功したadapterの証拠ではない。これらはproductionの文書を観察したもので、本セッションへの実行指示ではない。

### 他者のreviewとして確認した証拠

[Sol Evidence review r1][review]は409件についてVERIFIED 49 / PARTIAL 352 / NEEDS_MORE 8、AUTHORITY_CONSUMED 401、未消費・未取得等8件、profile completeness LIMITEDと報告する。必須high-signal事例で旧来のsystematic defectは再現せず、Selection実行へPASSとしている。

これは重要な新Evidenceだが、Astraによる409件の独立再監査、読者品質の比較、総費用削減の計測ではない。また同reviewはhistorical checkpointの実行SHAを遡及修正せず、次のSelection stageでcurrent reviewed implementationによるupstream再検証を要求する。その再検証結果は今回のsnapshotでは未確認である。

### Durable stateから引き継ぐが再実証していないこと

[closeout](../handoff/astra-phase-a-session-closeout.md)、[refinement](astra-phase-a-architecture-refinement.md) §1・§6・§9・§10、[Human–Sol discussion](../context/2026-09-09_post-refinement-human-sol-discussion.md)を読んだ。

- 過去のsemantic defectの原因を一つのコード行へ確定してはいない。今回も確定しない。
- 外部criticのexact source/PDFアクセスとtransport費は未検証。subscriptionやmodel名をcapabilityの証拠にしない。
- release producer/consumer mismatchは[過去のevidence ledger](../notes/phase-a-evidence.md)にある独立maintenance候補。main差分に修復は見当たらないが、今回releaseを実行・再検証していない。
- current Specialのartifact chainは今回再読していない。Weeklyで見た実行領域の記録を共通Core contractとして一般化しない。

## 3. なぜこのPhaseを今優先するか

**判断を変えたのは、production側が既に意味消費を改善し、意味判断と生成を分離し始めていた点である。** 「不足しているsemantic productをまず新設する」という進め方では、現在の消費ledger、details、Card、directiveと重複する危険が高い。過去のarchitectureを固定した実装仕様として扱わない。

次に解く不確実性は、構造化された情報が無いかどうかより、**現在の複数表現から次の判断に必要な意味を再現できるか、どこで再抽出・再判断・手動転記を要求してしまうか**である。これを解かずにresume、context packet、critic packetを別々に設計すると、同じjoinとauthority境界の調査を繰り返す。

今回の選択は「ここが最大の実測cost center」という主張ではない。role別時間、usage、repair費の比較はない。少数例で既存投資を使えるかを判定する方が、全面shadowや新contract実装より先行費用を限定でき、後続設計の誤投資を防ぐという情報価値の判断である。

作業仮説は次の二点に限定する。

- **H1:** 既存のSource/Supplement/Card/View/edition判断の大半を再利用し、独立保守する意味正本を増やさずに受渡しを改善できる。
- **H2:** 再読の一部は、必要な独立verificationではなく、locator・current basis・判断理由の受渡し不足に起因する。安全なprojectionによってその一部を除ける。

H1/H2は未検証であり、必須reviewの削減を許可しない。仮説が否定された場合にも、不要な新設を止められることがこのPhaseの価値となる。

## 4. 比較した選択肢

| 選択肢 | 今回の扱いと理由 |
|---|---|
| 新Consumption Recordのcontract/実装 | defer。既存ledger/details/Supplement/Cardで足りる範囲が未確定。情報欠落を実例で示してから追加を判断する |
| Generated resumeのみ先行 | defer。state表示の価値は残るが、意味判断への受渡しまで改善する根拠はまだない。全stage status UIを本Phaseへ混ぜない |
| 広いarchitecture再設計 | defer。current運用が既に一部の責任分離を具体化している。全体topologyをもう一度論じるより、既存構造への適合性の方が判断を動かす |
| 外部criticのtransport feasibility | defer。重要な独立した不確実性だが、今回の受渡し問題はcross-family criticを採らなくても存在する。model/provider比較を前提条件にしない |
| Fresh Weekly/Specialの全面shadow、またはその全準備 | defer。比較armの物理変更量が未確定で、不要なartifactやwrapperを用意する恐れがある。少数例の適合性結果を先に得る |
| Release helperの独立maintenance | 有効な候補としてdefer。反復修復の既知Evidenceは強いが、今回確認した進行W34の次工程はSelection。本依頼はproduction修復実行の委任でもない。直近release阻害が判明したら優先度を再考する |
| W34の新Evidenceを全件再監査／修復 | 選ばない。Solが新reviewを行いC019の表現も変わった。全件再監査の追加価値を示す新しいsystemic異常は今回得ていない |
| Gate reuse、semantic acceptance cache、外部workflow engine置換 | defer。現在のauthority equivalenceや実測bottleneckを根拠にできず、変更・検証費が大きい |

## 5. 選定Phaseの bounded scope

### 解く問いと標本

**上限4つのsource/task slice**を使う。各sliceはsourceから受渡し先までの一経路であり、号全体ではない。

1. current W34 C019：既知症状から表現が改善した例。
2. current W34のpaper一件：製品のhandread overrideだけに通用する設計を避ける。
3. current W34のcaptured-but-unconsumed一件：source presenceをconsumption/acceptanceへ誤昇格しないことを確かめる。
4. 固定したSpecialの一件：問い/as-of、比較対象または期間の違いを含む例。current remoteで適切なrefを確認して選ぶ。W34が同じSpecialで採用されると仮定しない。

Specialの該当例が取得不能、または異なるlegacy contractしかない場合は、その差分を未検証として止める。標本数を増やして無制限に探索しない。historical/既知例はcontract較正専用で、fresh品質・採用の証明には使わない。

### 行うこと

- 各例で、source snapshot / 消費した問いと範囲 / bounded claimとlimitations / edition判断 / consumerが必要とする情報を、現存artifact・field・identityへ対応付ける。
- 関連する実際のproducer、validator、consumerだけを追う。中心はSource/Supplement→Evidence→View/Materiality→Selectionへの一経路。Architecture以降は意味が渡せるかの必要情報境界までとし、rendererやrelease実装まで広げない。
- 各情報を「既存fieldで保持」「既存情報から決定的に導出」「未記録で新しい意味作業が必要」「未検証」に分ける。field名が似ているだけで同義としない。
- 少数の紙上例またはread-only解析probeで、source/claim identity、publisher claimとfact、未消費範囲、時点/比較条件、HOLD理由、profile固有情報が受渡し後も残るか確認する。見つからないlocatorを補完・創作しない。
- 各論理情報について、意味を決める役とそれを保存する既存正本、projectionのwriter、consumerを一つずつ明示する。review dispositionとHuman approvalは別にする。
- 最小変更候補に、置換・削除できる手動転記／再構成、追加される保守・review・transportの仕事を対応させる。artifact数やbytesは参考値で、実働時間・LLM creditsの代替測定とは呼ばない。削減対象を具体的に示せない候補は費用優位未証明とする。

### 非目標

新schemaやadapterのproduction実装、409件の再実行、研究内容の再承認、W34 Selectionのmaterialization、全field/全Core監査、モデルの実行比較、外部サービスへのpacket転送、PDF生成、full shadow runは行わない。再利用によるcurrent-edition acceptanceの省略、正式なstage/Gate invalidationの細粒度化も行わない。

独立verificationに必要な再読は削減対象として数えない。新しいclaimの抽出が必要な箇所はmappingの都合で埋めず、実際に必要な仕事として残す。

## 6. 成果物・終了判定・stop boundary

継続時のprimary artifactは `outputs/astra-semantic-handoff-feasibility.md` 一つとし、固定refs、標本、狭い対応表、欠落・競合、最小変更候補、費用仮説、判定をまとめる。補助probe/fixtureは判定に不可欠な場合だけworkspaceに置き、production authorityと誤認できない分析用出力に限定する。

以下を揃えたら検証を終える。

1. 4例以内で、意味を失う箇所／既存情報で足りる箇所を具体的な参照で示した。
2. 最小候補について、正本の二重保守を避ける方法と、消せる仕事・増える仕事を示した。
3. Weekly/Special差分、旧checkpoint/current implementation、sourceがあるが未消費の状態を黙って同一化しないことを点検した。
4. 結論を **適合性あり／狭い修復が先／証拠不足** のいずれかとし、その先の投資対象を一つ提案した。

「適合性あり」は設計の成立可能性だけを意味する。品質同等性や総work削減、production adoptionのPASSにはしない。sourceへの到達不能、必須identityの未解決、未知のauthority contractに遭遇して標本内で解けない場合は「証拠不足」で終了できる。残りを推測して埋めず、調査範囲も自動拡大しない。

**その報告を完成したら再び停止する。** prototype実装、shadow実行、production修復・採用・移行は次の明示指示の範囲として扱う。Human Gates、Freeze、Release、historical bytesの変更権限は一切含まれない。

## 7. 主要未確定事項と方向転換条件

| 未確定事項／得られた場合のEvidence | 判断への作用 |
|---|---|
| 既存consumerが必要情報を既に無損失で消費しており、余計な再構成が観測できない | 新contract案を撤回。変更不要、または限定的な表示改善の提案で閉じる |
| 正しい意味を持つ入力が特定producer/transformで失われている | 広いsemantic product追加を止め、その狭い修復を次候補にする |
| source span/範囲/問いの情報が既存chainに無く、projectionだけでは復元不能 | 既存structureへの限定拡張または抽出contract修正を提案。正本新設を自動決定しない |
| Specialでidentity、比較軸、期間やconsumer契約が異なり共通化がlossy | 共通部分とprofile差分を分けて提案し、Weekly成功をSpecial対応の証拠にしない |
| 手動transport・再判定・保守追加が除去できる仕事を上回る／内訳不明 | 費用優位を主張せず候補を縮小または保留。まず追加計測が必要と報告する |
| W34 Selectionのcurrent-Core再検証に重大なauthority問題、または直近release阻害が新たに判明 | 進行運用との接続条件を再評価し、独立maintenance優先への変更をHumanへ提案。本Phaseの権限で修復しない |
| remote更新が本書の標本・契約を実質的に置換 | 当該差分だけ再確認。Phase A全体を再実行しない。選定理由が崩れたら改訂判断で停止する |

criticの経済性、fresh Weekly/Specialでのreader品質とwork差、最適bindingはこのPhase後にも残る。最小契約の適合性からそれらの成功を推論しない。

## 8. Humanが同一セッションで継続を許可した場合

例えば「本書のbounded scopeで、選定した適合性検証Phaseを実行してください」という指示を受けたら、次を行う。

1. workspace/main/W34と選ぶSpecial refのremote realityをread-onlyで確認し、本書からの関連差分だけ読む。
2. 上記4例以内を固定し、source→消費記録→Card/View→edition判断のidentityとproducer/consumer対応を追う。
3. 最小変更候補を既存構造だけの場合から評価し、限定的な欠落・衝突チェックと仕事の増減を報告する。
4. `outputs/astra-semantic-handoff-feasibility.md` を完成し、実装前に停止する。

役割はモデル名から切り離す。Astraはこの設計・適合性判断を担当し、Solの独立reviewはHumanが依頼する後続の確認として扱う。productionの意味決定権限やHuman採用権限を本分析へ移さない。今回は他agentへの実行依頼もしていない。

## 9. 今回の調査の終了理由

current main差分、W34のState、新しい代表Card、消費記録の実例、Sol review、編集directiveと実行依頼が揃い、古い診断をそのまま実装へ転用すべきでないこと、既存構造との適合性が次の小さな判断単位になることを確認できた。

これ以上のfield-by-field mapping、全件集計、追加Raw監査は選定したPhaseそのものに入るため、今回行わない。API compareの広いfile一覧は大量出力になったため完全な変更inventoryとして使用せず、以後は固定pathの直接readに絞った。OSS/model/価格の追加調査も、この選定を変える見込みが小さいため行わなかった。

本書のみを新規保存し、production repository・refs・State・decisions・Gates・Freeze・Releaseは変更していない。通常のGit transportはHumanに委ねる。**選定Phaseは未実行のまま、ここで停止する。**

[pr486]: https://github.com/eariver/japanese-generative-ai-survey/pull/486
[state]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/production-state.json
[schema]: https://github.com/eariver/japanese-generative-ai-survey/blob/6d748a962d57beff89da7c1b20cb5a9a86c8e261/schemas/evidence-v2-card.schema.json
[card]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/results/task-089aea0f0b318bee50b2.json
[ledger]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/authority-consumption-ledger.jsonl
[details]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-consumption-details.jsonl
[review]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/reviews/sol-evidence-authority-consumption-review-20260909-r1.md
[directive]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/reviews/sol-selection-directive-20260909-r1.md
[request]: https://github.com/eariver/japanese-generative-ai-survey/blob/030eb723c12282f0cfd09aaada05d14f0c0906c7/sources/2026-W34/execution/requests/sol-selection-materialization-request-20260909-r1.md
