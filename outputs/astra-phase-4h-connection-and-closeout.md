# Phase 4-H — 接続試験の停止とPhase 4終了判断

日付: 2026-09-13 JST

状態: **PHASE 4 CLOSED / CONNECTION PROBE STOPPED ON COUNTEREXAMPLE / NO ADOPTION**

## 1. 判断

**Phase 4をここで閉じる。** 既存canonicalの意味表現、実入力が情報を落とす地点、読者出力との不一致は具体化できた。一方、その周囲のadapter・引用規則を一つずつ完成させる経路は、品質を満たすまでの全role仕事が減るという中心仮説に戻れていない。次の小修正が可能なことを、研究・設計投資を続ける理由にしない。

4-Gで候補とした1 packageの接続を試したが、同じURLに異なるsource metadataが対応する箇所で、今回置いた保守的なURL集約checkが停止した。これはproductionの新しい受理不良や、canonicalからの生成が不可能という結論ではない。URLだけで文献を一つにする案では、既存source identityをどう保存/表示するかの追加判断が要るという具体例である。

この試験は**初回section出力前に停止し、予定した修復→再生成は未実行**。完了したのは事前の停止条件に沿う限定反証であり、接続成功やfull canonical baselineではない。既知例で局所条件を増やし続けず、未実証事項と再開条件を持ってPhaseを閉じる。

再構築全体の目的は継続する。次の主作業は、production実装やfull rendererの完成を前提にせず、研究上の問いから本文・独立review・repairまでの**具体的に異なる仕事の単位**を比較できる条件を作ること。まだ有効な対案を選定済みとは言わない。Phase番号を進めるだけの新実験も開始しない。

## 2. Current production realityの更新

[観測](../notes/phase-4h/observation.json)でmain `14781409f6fb8d79e3eb4ad6b4c457764a038fde`、W34 `8480f4dfffb57b456d1147fcc5360f7864bb19df`を確認した。旧f50d229からの6 commits / 14 pathsはPR #489の統合、revalidation record、State、stage validation/checkpoint、worklogを含む。

[限定binding検査](../notes/phase-4h/refresh-result.json)で確認したこと:

- **実W34のStateはRELEASE_CANDIDATE、next_actionはPUBLICATION_PREVIEW、Preview pending・Human provenance null、Freeze/Release pending。** 4-F/Gの「disposable copyだけ」という観測から更新する。Previewの承認やreleaseは成立したと扱わない。
- State→active revalidationはSHA `2398c332…`で一致し、同recordが旧DRAFT_COMPLETEを名指しする。旧checkpointは比較差分で不変。新VALIDATED_DRAFT checkpoint→Candidate raw bytes、同checkpoint→stage validation resultのbindingも照合した。
- Candidateはf50d229から変更されていない。`candidate_sha256` fieldは`dbd4c783947fbe6c4f3bc1fab151071f2cd8ed5cb8100fdfceaa7195a10a6fb8`、**ファイル全体のSHA**は`c45adaf79edad782db7bb21ee1f62fd7794773a4cdeddc6a9697fdd046592f00`。後者をcheckpointが指す。二つを取り違えない。
- revalidationとCandidateが指すreader/quality/semantic/visual/PDFのmetadataは対応し、前4件の保存済みraw SHA/byte countも一致する。対象pathsは比較差分で不変。PDF本体の取得/目視、rootによるfull State validator、独立品質認定は行っていない。
- Evidence・Selection・Architecture・Draft・reader filesは今回の比較差分で変更されていない。section20の内部配置注記やsource対応の反例が、このadvanceで修復されたというEvidenceはない。

production worklogは既存Candidateを再buildせずvalidateして進めたと報告する。持ち越しのSol/sidecar dispositionは当該framing residualの報告であり、rootの内部配置注記findingと同一の問題が解決したとは扱わない。revalidationは実号で一度使用されたというEvidenceになったが、複数round運用、品質十分性、純費用削減の証明にはならない。PR #488/#489の修復をreconstructの成果として計上せず、修復済みbaselineとして維持する。

## 3. 接続試験と停止した反例

対象は4-Eの日本語Draftと、そのbasisが指す歴史W34の1 Package。現mainの既存rendererからescaping・citation key・block rendering等のpure関数だけを抽出した。full旧rendererの再利用ではない。v2のstatement/subject/sourceを解決する一時mappingは機械で作り、compact archiveや手書きcitation mapを入力にしない試作だった。

試作の表示範囲はsection/deck/blocksと限定bibliography。NOTEを引用付きplain paragraphにするlab上のstyle、heading citation拒否なども試作内で明示したが、それらの成功検査へ到達していない。profile外観、full publication manifest、PDF、Special、独立reviewを実施したとは扱わない。

[反例結果](../notes/phase-4h/probe-result.json): block `p2-ide-enterprise`が参照する2 Cardsに、同じ `https://help.openai.com/en/articles/6825453-chatgpt-release-notes` がある。

| Cardのtask末尾 / source ID | title | published_at | accessed_at |
|---|---|---|---|
| ac31c38a016aad80 / supplement-src-40875f5b03808f54 | OpenAI ChatGPT release notes (shared body) | 2026-08-20T00:00:00Z | 2026-09-08T23:00:00Z |
| 70016a4d5eb2908e / supplement-src-4adb47d7859f6b51 | First-party/official body: 同URL | null | 2026-09-08T14:50:59Z |

両方のsource_classはPRIMARY_OFFICIAL。同一URLは同一保存snapshot・同一日付意味を証明しない。今回のcheckは、URL由来の一つのcitation keyに異なる表示metadataが来た時、先着のrowを無言で採用するのを防ぐためrootが置いたもの。**現Core schemaの要求でも、2 Cardsが互いに矛盾/不正という認定でもない。** underlying sourceの2 raw本文まで追跡していないため、実bytesが異なるとも断定しない。

選択肢にはsource occurrence/versionを保持する文献識別、明示的な集約規則、読者向け代表表示とprovenance traceの分離がある。しかしどれも無条件に正解ではなく、重複した文献表示、保守、review/再生成への影響がある。この段階で新しいcitation storeや一律の再取得要件を増やさない。

8件の今回入力と2件の既存入力のidentity、Draft→Package hash、Draft schema、入力不変、反例の再現を確認した。**これはcounterexample検査のPASSであり、publication経路のPASSではない。** 最初の停止後に修復fixtureを走らせて成功だけを追加することもしていない。4-F Cardを歴史accepted Packageへ挿入していない。

## 4. Phase 4で判断可能になったこと

| Evidence | 支持する判断 | 支持しない判断 |
|---|---|---|
| 4-A/B: 実governanceと比較条件 | 継続owner/上流reviewは既にあり、新Bとして追加できない | 現行運用のreview量が最適、全ての運用単位が固定 |
| 4-C: 3候補のsource→本文→独立review→repair→再review | 既存意味欄で具体的な研究/帰属/比較条件の欠陥を修復できる。機械PASSは意味品質を代替しない | full canonical production baseline、費用優位、未知source全般の十分性 |
| 4-D/E: 実W34と境界Draft | 内部制約の単純連結と読者文は別。canonicalに記せても既存helper/rendererが同じ意味を使うとは限らない | 新schema/storeの必要性、全号品質合格 |
| 4-F/G: 日時sourceと個別参照 | authorityに既にある情報を狭い入力/変換で落とす具体的経路。忠実なcompactと補助付きcanonicalは同じ意味欄へ収束し得る | 直接JSON著述の費用勝利、source読解/review不要 |
| 4-H: source metadataの集約 | source identityをURLだけで代表させる場合にも判断/保守が残る | canonical出力不能、全repositoryのmetadata品質不良 |
| PR #488/#489と実W34 advance | 修復済みbaselineを更新し、重複開発を避けられる | reconstructionの純削減達成、Preview承認、意味品質完成 |

Phase 4のresearch/editorial sliceと局所probeは役に立ったが、4-D以降は既知W34の補助形式や表示規則へ次々と対象が移った。新しいfixtureが示すのは主に互換性/保存条件であり、source・編集・review・repair全体の実働/LLM費用を下げる比較Evidenceは増えていない。[Phase 3-G再評価](astra-system-direction-reassessment.md) §1・§5・§7の停止原則をここでも適用する。

**「full canonical baselineを完成させるため」として局所実装の完了を次の研究・仕事量比較の前提にし続ける方針を終了する。** 不足する品質/authority保証を達成済みにするという意味ではない。production採用を伴わない比較で省略した工程は、費用削減に含めず未実証として明示する。

## 5. 今後の入口・再開条件

次回は本判断とhandoffから始め、4-H probeの修正やrenderer完成を既定にしない。最初の一単位は**比較すべき実際の仕事の差を、一つだけ成立させる設計判断**。既存4-Cの修復/4-Dの運用Evidenceを選択的に使い、追加の全文再調査や全repo crawlを条件にしない。

必要な判断は次の順序:

1. 同じ読者の問い・品質/coverage義務で、どの実仕事を除く/まとめるかを一文で特定する。継続owner追加、別modelへの移転、canonicalへの詳細記入、repairの前倒しだけを差にしない。taskの完了単位や研究・編集の往復順序を再検討する余地はあるが、現productionが既にそうしていないかを先に確認する。
2. 対案が意味を別role/補助記録へ移すだけ、またはAへ同じ便益を適用できるなら、対案を棄却/共通化して止める。無理にBを発明しない。full Core・rendererの完成はこの設計判断の前提にしない。
3. 実行に値する差がある場合だけ、未回答のsource群、採用以外のHOLD/除外、共通品質条件、非著者source-first review→repair→再review、全roleの計測可能な仕事を出力前に固定する。W34やP-EAGLE等の既知解答を未知source比較にしない。
4. productionで必須の工程をlabで省く場合、その仕事を両案で明示し、ゼロ費用として優位を作らない。Humanを無償reviewer/計測係にしない。計測不能なtoken/active timeはunknownを保持し、記録量やwall spanで代替しない。

source/citation/rendererの保守候補は、本書の反例に加え4-E/F/Gを保持する。再開するのは、採用候補への正規接続に必要になった場合、または実運用の頻度/負担がその投資を裏付けた場合。安全条件を弱めたり既知反例を消したりはしない。Phase 3のacceptance/staging/cache・新store・恒久telemetryの保留も維持する。既存architectureを永久固定するという結論ではない。

次の主比較、独立review、Phase 5の開始を今回実行したとは扱わない。全体目標は未達で、閉じるのはPhase 4のこの調査経路である。新Human判断を要求して止めたのでも、外部blockedでもない。

## 6. 未実証・権限・durable記録

未実証: full canonical baseline、全号publication quality、未知source omission品質、Weekly/Special全体一般性、全caller/歴史再現、PDF/visual QA、今回の接続成功と修復往復、長期total lifecycle純減、役割別active time/token/料金。4-C以外の試験に独立quality review済みのラベルを付けない。

[4-H実験記録](../notes/phase-4h/README.md)、[現実更新](../notes/phase-4h/refresh-result.json)、[反例](../notes/phase-4h/probe-result.json)、[現在handoff](../handoff/astra-phase-4-continuation.md)が継続入口。以前の判断は履歴を保持する。

productionはread-only。PR/Issue、State、承認、Gates、Freeze/Release、adoption/migrationを変更していない。追加subagent/外部送信なし。4-Cの一体review許可は完了済みで、新比較の委任権限に流用しない。通常Git Pull/Push/最終commitはHuman。
