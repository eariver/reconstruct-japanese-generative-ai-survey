# Phase 4-G — 著述方式の比較と、共通して除ける変換

日付: 2026-09-13 JST

状態: **BOUNDED DESIGN COMPARISON COMPLETE / COMPARISON AXIS REVISED / NO ADOPTION**

## 1. 判断

**「compact拡張」と「canonical直接著述」を大きな二つのarchitectureとして競わせる前に、どちらにも必要なcanonicalからpublicationへの接続を共通部分として切り出す。** 現在のEvidenceは直接著述の費用優位を示さない。compactの入力補助が正確なcanonical欄を編集するだけなら、二案の意味表現は同じものへ近づき、独立した比較armとは言いにくい。

除去候補として具体化できたのは、既にCard/Draftが持つ個別参照や境界処理を、record一括source・Discovery ID＋ref_mode・compact archiveから再構成する経路である。ただし、単に自動copyされるファイル数を減らすことは、著者/reviewerの削減実績ではない。二重の表現規則の保守、参照の再解決、archiveとの同期確認をどこまで不要にできるかが設計上の候補である。

次は**既存canonicalを唯一の本文・個別根拠入力とする、1 packageのpublication接続と修復伝播の限定試験**が妥当。入力を手でfull JSONへ書く方式の採用を先に決めない。既存の入力補助・scaffoldを残しても、意味欄を失わずcanonicalへ到達し、その先が同じなら同じ共通経路として扱う。

source読解、研究の問いへの採否、限定表現の編集、独立review/Human判断は消えていない。大きなarchitecture B、new store、owner追加、acceptance/staging/cache投資を開始する根拠は増えていない。

## 2. 入力と確認範囲

[着手観測](../notes/phase-4g/observation.json)でmain `14781409f6fb8d79e3eb4ad6b4c457764a038fde`、W34 `f50d229162b7402c504c0978f72dab4b33052f5e`を再確認し、4-F末尾から不変だった。PR #488のbib修復、PR #489のpublication-only revalidationを比較baselineへ含める。実号の進行や新しいHuman承認を推測しない。

mainの両agent wrapper、Evidence/Drafting interactive runner、Weekly publication、Card/Draft schemaの7ファイルを固定GET。歴史W34 Packageの1ファイルと合わせてGit blob/SHA-256を照合した。[入力](../notes/phase-4g/inputs.json)、[関数位置・反例結果](../notes/phase-4g/comparison-result.json)、[再現方法](../notes/phase-4g/README.md)を参照。

既知校正入力は4-Fの参照だけを修復した未採用Card、4-Eの日本語Draft案、4-CのR1–R4修復記録。新source生成、未知source比較、独立review、production CLI、State/Gate、PDF、full admissionは行っていない。4-E本文と4-Fの歴史VERIFIEDを今回の品質合格へ読み替えない。

## 3. 比較を変えた確認

### G1. agent入口の変更だけでは形式は変わらない

`run_evidence_v2_agent_first.py`はDiscovery authorityとCompletenessの限定補正を行い、既存interactive runnerを呼ぶ。`run_drafting_synthesis_v2_agent.py`もhistorical basis validationのcontextでinteractive generatorを呼ぶ。名前にagent/canonicalがあることは、既存canonicalをそのまま著述する新経路の証明ではない。

一方、現行helperはtask/Packageからidentity・hash・source metadataなどを供給している。これを捨てて著者が手入力する必要もない。新案の機械欄を人に移す前提で直接著述を高く見積もること、逆にそのscaffold実装費を無料と扱うことの両方を避ける。

### G2. 狭い指定から個別参照を復元することはできない

4-Fで確認したEvidenceの一括source指定に加え、現行Draftの`_refs/_ref_rows`を変更せず関数単位で調べた。対象candidateのDiscovery IDを指定すると、`CLAIMS`はそのCardの全claimを返す。`LIMITATIONS`、`CLAIMS_AND_LIMITATIONS`、`NONE`でも、Grokの`claim-2`だけを選ぶことはできなかった。候補を増やす操作はunionなので、不要なclaimを取り除けない。

これは個別指定を失う具体例であり、全compact表現の数学的な最小性証明ではない。4-F lab Cardではclaim-1がprimary page、claim-2がDailyX reportへ対応するため、どのclaimを参照するかは実際のsource選択へ影響する。4-F Cardは歴史Packageへ差し替えていない。二つを同一のaccepted chainとして試してはいない。

現行Draft schemaは個別`deck_evidence_refs`を許し、同じ本文/identityで参照だけが異なる2 variantを受け入れた。ただしこのvariantは参照識別のfixtureであり、本文に対するsource sufficiencyやattributionのfull validator合格を主張しない。

また静的読解ではEvidence helperが単一entityをPRIMARY_SUBJECTへ付け、metricsを空配列にする。Draft helperは全LIMITATIONを一つの自動境界blockへ寄せ、全must-coverに同じcontent block集合を付ける。4-Cで意味上の修復が必要だった比較対象・metric条件を、このcompact経路が一般に網羅できるとは扱えない。これら全機構の新しい実行試験はしていない。

### G3. publicationのcompact依存は両案に共通する問題

現行Weekly publicationはcanonical Draftをvalidateした後、compact archiveからheadline/deck/block textとの一致を調べ、引用はarchiveのDiscovery IDとDiscovery locatorから生成する。CLAIM_BOUNDARYのcitation欠落とsection_label要件は4-Eで確認済みで、現在のcodeでも残る。

canonicalの個別参照を著者が正しく埋めても、この出力経路を維持すれば参照の精密化がそのまま読者へ届かない。逆にcompact拡張案でも、生成後のcanonicalだけをpublicationに渡すことは設計できる。**この依存の除去を直接著述だけの便益へ計上してはいけない。** archiveを履歴として保存することと、現在の本文/引用を決めるために読み戻すことは分けられる。履歴削除は提案しない。

## 4. 公平な二案と、欄ごとの仕事

比較対象を次のように補正する。未修復の現行helperを安価な対照として置かない。

| 面 | E: 意味を保持するcompact拡張 | C: 既存canonical欄の著述＋機械補助 |
|---|---|---|
| Card個別source/subject/metric | statement別指定、複数subject、必要なmetric等を入力・変換・validatorへ追加 | 同じ意味判断を既存Card欄へ記す。source metadata/ID候補はtaskから補助 |
| Draft個別根拠 | Discovery IDの全件展開だけに依存せず、既存ref tuple相当を選択できるようにする | Package内の既存ref tupleを選択。長いIDの手入力を必須にしない |
| reader境界/omission/coverage | 自動連結を外し、本文と対応/rationaleを著述可能にする | 既存blocks、boundary_dispositions、must_cover_coverageへ著述 |
| 機械欄 | task/Packageからbasis、identity、run provenance等を供給 | 同じscaffoldを維持/抽出。人がhashを捏造・転記する方式にしない |
| publication | canonicalを読む共通consumerが必要。compactへ戻らない | 同じconsumerが必要。方式固有の便益にしない |
| 統合/保守 | compact契約とcanonical契約の意味対応、互換callerを保守 | canonical編集経路、未完成欄の検出、既存callerとの接続を保守 |
| review/repair | sourceとcanonical/読者出力をreview。意味変換が残ればその忠実性も確認 | sourceとcanonical/読者出力をreview。詳細欄の誤選択/欠落も確認 |

Eがcanonicalと同じ意味欄をそのまま通す設計になるなら、Cの入力補助として扱える。これを異なるarchitectureとして大きなA/B試験にしない。field数、JSON bytes、ファイル数だけでLLM費用・思考量・Human負担を代理評価しない。

意味の所有と機械処理を分ける:

| 内容 | 一度だけ判断する場所／残る仕事 |
|---|---|
| sourceの支持範囲、時点、entity/metric条件 | Cardの既存意味欄。原source読解とreviewは残る。metadataからevent時点や因果を自動推測しない |
| 採否・役割・package範囲 | 既存View/Selection/Architecture。Cardがあれば編集判断が不要になるわけではない |
| 日本語の説明・比較・限定 | Draftの本文と個別参照。内部制約の単純連結ではなく読者文を著述する仕事が残る |
| must-cover、omission、attribution | 既存対応欄へ編集判断を保存。参照先を機械で検査できても、十分性や本文の言い方を自動認定しない |
| identity、許可source候補、basis hashes | 正規入力から機械で供給/検証する。statusやHuman decisionを無条件に生成する項目ではない |
| citation、表示用構造、manifest | 検証済みcanonicalの参照から派生させる。表示JSON等を編集可能な第二の意味storeにしない |

## 5. 削減候補、投資費、未実証

具体的に不要にできる可能性があるのは、record-wide sourceやDiscovery単位の指定から意味を再推測する変換、現在の読者出力のためのcompact text同期、citationの手製対応の維持である。ただしproductionで毎回これらを人が二重著述していたという観測はない。現行generatorの自動copyも含まれるため、削減人数・分数は算出しない。

共通consumerにも費用がある。v2 Packageのexact bindingとsubject/statementの解決、sourceの表示metadata選択、bibliography、block種別、profileごとの外観、歴史互換caller、QAを扱う必要がある。旧rendererの関数再利用は可能でも全体drop-inは4-Eで棄却済み。読者向け帰属や観測reportの性質を、内部note禁止を理由に消してはいけない。

修復後に残る費用も両案へ等しく置く。Cardのsource対応を変えればEA/View/Matrix以降のbindingに影響する。Draft意味欄変更もpublication-only修復ではない。PR #489で正規化された表示側再生成と混ぜず、意味の影響review・新bytesに対応する正規authority処理を保持する。過去承認の再利用や全sourceの無条件再調査のどちらも前提にしない。

同等品質が成立した後にのみ、同じ寿命/利用回数について、除去できた著述・照合・repairの仕事が、新consumer/入力補助の開発・review・互換保守と残る操作費を上回るかを比較する。現時点でその各値はunknown。調査scriptや本判断書の作成もrootの追加仕事で、productionの削減実績ではない。

## 6. 次の一単位と停止条件

次は1 packageの**canonical本文・引用の接続と、1回の修復による派生物更新**を同時に扱う。helper入口ごとの速度競争や全号生成を始める必要はない。

最小入力は4-E Draft/Packageの既知境界例と4-F source対応例。両者を無断で同じaccepted chainへ混ぜない。歴史Packageの試験と、参照修復を表すlab fixtureを区別する。PR #488/#489を含む現在のcodeと、使用する関数/契約の固定identityを用いる。

この単位で判断すること:

1. compact archiveを意味入力にせず、本文・deck・NOTE/CLAIM_BOUNDARYの個別refから、source種別/locatorを取り違えず読者出力を生成できるか。意味を新しい中間手書きmappingへ退避しない。
2. 一つのcanonical参照/境界修復から派生出力を再生成したとき、別の本文・citation入力への手直しが不要か。これは機械的な保存/依存試験であり、source sufficiencyを既知fixtureから認定しない。
3. section_label等のprofile表示条件、frontmatter/synthesis、table/list、bibliography・review manifestのうち、共通化できる責務と未対応の責務はどれか。元Architectureへ無言でfieldや承認を追加しない。

本文・citation・必要な限定の保存ができなければ、その最小反例で止める。core接続やPDFまで拡張しない。成立した場合も、全号品質/費用比較を始める前に、残るcaller/authority閉包、Weekly/Special差、独立review→repair→再reviewを完結できる試験範囲を定める。既知W34をunknown-source比較へ再利用しない。

今回は設計比較と反例で判断面が閉じたため、同じsessionで新consumerの実装を惰性で開始しない。これはHumanへの新たな判断要求や外部blockedではない。次のsessionはこの設計を固定仕様とせず、source/production修復の新Evidenceで順序・範囲を変更してよい。

全号のpublication quality、full canonical baseline、Special実行、未知source omission品質、独立review、PDF/visual QA、長期total lifecycle純減は未実証。追加subagentは使っていない。productionはread-only、Git Pull/Push/最終commitはHuman。
