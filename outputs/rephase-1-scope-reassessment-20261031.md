# 総編纂工数からの残作業再評価 — 2026-10-31

Astra author-side decision。**再評価完了・独立BOUNDED SCOPE-DECISION PASS（§8の限定）。今回は再評価・文書化だけで、実装を開始しない。** HumanのCommit/Push申告を続行前提とし、Commit readbackは行わない。

## 1. 結論と優先順位

**追加実装を、既に具体化した共有upstream修復に絞る。その後は汎用機能を追加する順序から、実用・品質・費用を確認してR4固定候補／監査へ進む順序に変える。**

1. DM016/017＋それを一貫して支えるDM022 root/effective修復は、**最後の予定済み機能実装unit**として維持する。現在のPRE_CODE_READY mapを使い、同内容の新しいpre-code周回は設けない。「最後」は未発見の重大欠陥を放置する約束ではなく、後続機能を自動追加しない投資境界である。
2. **非四系列Thematic／Retrospectiveの汎用complete-reader・normal-correction機構をR4前に必ず設計／実装する条件を撤回する。** R4後に無条件で行う宿題へ移すのでもない。具体的な利用要求、既存経路の不足、費用比較が揃った場合だけ再選択する。
3. Weeklyと必要なSpecialの品質・十分性・provenance・実用性は維持する。形式ごとに同じ生成／reuse機構を持つことを完成条件にしない。必要経路が実際に使えない場合は、その採用／全体完了を保留する。
4. 修復後は**具体的対象のrehearsal → 一つの候補固定とfresh独立七観点audit（R4）→ Human限定採用（R5）→ 実測効果と旧作業の除去（R6）**へ進む。R4準備はsupport表・費用表等の作成を指し、audit開始／採用／全体完了とは別である。

本書は[mission](../brief/00-mission-and-success-criteria.md)／[direction §§6–7](rephase-1-direction-assessment.md)に基づく**投資順序・適用範囲のresolution**。次を明示的に上書きする：

- [Profile契約](rephase-1-profile-support-contract-decision.md) §§2/5/7、[契約ROOT](../notes/rephase-1-profile-support-contract/astra-review-resolution.md) §§4–5の「broader-reader/correction必須後続gate」。
- [pre-code assessment](rephase-1-profile-support-precode-assessment.md) §5、[pre-code ROOT](../notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md) §7.2、および旧roadmap／入口にある同じ順序条件。
- それらを前提とする過去独立reviewの**今後の工程条件だけ**。過去reviewを本判断への賛成と読み替えない。

上記の保存bytesと技術契約は変更しない。canonical10、普通3/5→7、全parent/OID、真のR/E、HIGH/LOW境界、歴史／新規受付分離、guard、CURRENT proofは引き続き必須。PRE_CODE_READYは実装可能性の判定であり、経済的優位やruntime成功ではない。

## 2. 判断根拠と不確実性

### 2.1 実需と実装方式を区別する

- Human missionは高品質なWeeklyとSpecialの実用性を要求するが、全形式の同一generated readerや全mode自動化の実装一覧を要求していない。
- 保存されたhistorical pattern matrixはRetrospective15件（monthly7／half-year4／annual4）を報告する。保存Summaryは複数Thematicの制作・repairを報告する。これはSpecialの需要を無視できない根拠だが、将来の頻度や特定の新rendererへの需要、現candidateの正常運用を証明しない。
- 特にTS-003は**exceptional releaseでnormal StateはVALIDATED_DRAFT**との報告。単純な「3件とも通常RELEASED/COMPLETE」と扱わない。Specialが過去に出版された事実だけで現在の訂正経路を十分とはしない。
- 4文書intakeは67/160 tasksのtype gapとnamed rowsのedition-local対処を報告する。actual Raw／個別publisher proofは未取得。数字はrecurring costや本candidateによる67件受入れの実行証明ではない。

根拠の位置と作者案の訂正は[packet](../notes/rephase-1-scope-reassessment-20261031/README.md)を参照。追加networkや既存edition再実行はしていない。

### 2.2 なぜ共有upstream修復を残すか

| 部分 | 今残す理由 | 追加費用／限定 |
|---|---|---|
| P1 canonical10 | 実在するsource-class入口gapを一つの正本で直し、元labelを保つ。editionごとのprojection修復を除去する対象が明確 | task/card実入力・claim限界の検証が必要。全recordのpublisher認定にはならない |
| P2 普通3/5→7＋parity | named obligationを手で追記／機械参照列を再入力する作業とadapter分岐を減らす | U=initial+root+effective、全(parent,OID)、closure残余の意味を守る検証・保守費 |
| P3 新規受付preflight | P1/P2で入口を広げる際に未知type／宣言脱落をwrite前に拒否するため | 将来すべての入力問題を解く汎用validatorではない |
| P4 DM022 true-R/E／COPY kernel | 既存操作のrequest自己申告をaccepted chainへ束縛する。DIRECTだと確認するためにも根拠が必要 | 最大のcoupled実装・歴史/現行・repeat/readback・closure回帰費。実利用頻度は未知 |

Rootはfinal133の`survey_research_authority_v2.py:783–799,1172–1297`を再読し、request DiscoveryをDIRECT rootとして扱う記述とCOPY／triplet／request refsの現状を確認した。[削減可否分析](../notes/rephase-1-scope-reassessment-20261031/reduced-repair-feasibility.md)ではDIRECT-onlyでもCOPY-bound DCP/SCPとroot証明の大半が必要とされた。単にDERIVEDを使わない前提では、その前提自体を検証できない。

従ってP4を外した小修復は選ばない。ただし「wholeの方が安い」と実測したわけではない。**共有修復の具体的除去対象と既存authority欠落を根拠に、未知の費用を伴う限定投資として選択する**。過去の設計費・test費・PRE_CODE_READYを正当化理由にしない。

### 2.3 比較した選択肢

| 選択肢 | 判定 |
|---|---|
| whole修復→汎用reader必須→R4 | 不採用。reader投資が必要と分かる前に出口を後退させる |
| P1–P3＋DIRECT-only縮小→R4 | 不採用。kernelの大半が残り、unsupported分岐／review／維持費が増える。より安い一貫した切断は未成立 |
| final133を今固定してaudit | 不採用。既知の受付・authority修復前に全audit費を払い、その後候補変更で再監査する見込みが高い |
| final133の限定品質／費用調査を先にする | 可能な情報収集だが、未修復入口のworkaround込みのrehearsalを重複させないため、今回は次実装を上記共有修復に選択。利用対象の明確化／既存記録の整理はR4準備として可能 |
| **whole共有修復→具体的rehearsal→固定/audit** | **選択**。汎用機能への自動投資を止め、既知の共有gapを閉じた一つの経路で実用・費用を判定 |

M≈M等の作者の相対式は工数見積りではなく、kernelを削れない構造の説明に限る。「機械cost negligible」「実需はDIRECTのみ」「TS-001 DERIVED shapeを実証済み」も採用しない。頻度・個別graph・総費用は未確認である。

## 3. 実装・検証の境界

次のHuman continuation後、Generalは[pre-code ROOT全文INCLUDING §7](../notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md)に従いwhole P1–P4を実装する。契約62b14add／ROOT021a0d7c／precode bfb72bf2、R3＋C-R2＋kernelをR4→R5→ROOTで訂正する既存優先順位を使う。新しい仕様選択の再提出を通常工程にしない。

- 新runtime module／schema／family／generic resolver／cadence engine／telemetryは選択していない。
- 三research Profilesの**共有upstream**意味、10types、many-to-many/shared-OID、実DIRECT/DERIVED、ordinaryとDM022 input差、history/new-admission、guard/no-overwrite、repeatと影響consumerを検証する。これは三Profile全publicationの生成・訂正実装要求ではない。
- 既存成功suiteを件数装飾のため全面反復しない。変更predicate→oracle→影響consumerの対応から実行を選び、独立implementation reviewを保持する。新codeのCURRENT proofや意味のあるaffected regressionは削らない。
- 原失敗／skip／partial／raw欠落とsource/run束縛を保存。synthetic承認を真正reviewへ転用しない。
- 欠落authority／新dependency／契約矛盾を発見した時は、具体箇所・影響・最小修復／制限／延期の選択肢をAstraへ返す。**「最後の修復」を口実に無制限に直し続けない。** 単なる必要caller配線は同unit内だが、新capabilityや契約変更は別の投資判断である。
- 終了時は独立implementation review・exact delivery・未解決事項を揃えCommit Point。引渡し品質未達ならNOT_READYとし、R4 auditで穴を隠さない。

## 4. R4へ進むための最小条件

### 4.1 準備：採用対象と正常操作を具体化

共有修復のcloseout後、最初のtaskは**採用対象／capability表と代表的品質・費用rehearsal**。別の汎用reader設計unitを自動開始しない。準備の記録は次の一枚の表で足りる：

`対象edition/用途・Profile | 必要操作 | 実際の経路と受理窓 | 品質/通常修正の証拠 | 制限/不足 | 外す仕事/追加費 | 採用可否`

最低限、一つのWeeklyと一つの**実需要を説明できるSpecial**を代表に選ぶ。二例はcoverage上限でも全形式代表の自動認定でもない。Thematic四系列の成功を非四系列／Retrospectiveへ横展開しない。全形式・全期間の重複production replayを前提にもせず、未代表の必要経路は表で制限と検証の要否を判断する。

具体的topic／period／Rawが利用許可内に定まらなければ、そこで不足する選択・取得許可だけをHumanへ求める。存在しない実需要をfixtureで作らない。この再評価では新しい対象editionも取得権限も発明しない。

Manual/direct-primaryは正当な既存経路として候補に含められる。ただしPRIMARY_ONLYはcomplete-reader/reuse証明ではない。**受理前のmanual編集、真正Human REQUEST_CHANGESに基づくre-entry、別途合法な操作／新edition**等の実条件と費用を示す。通常必要なpost-VALIDATED変更がexceptionや架空Gateなしにできないなら、その対象のblocker。単に「manualで対応」と表を閉じない。

### 4.2 Rehearsal：qualityとworkを確認

- 実資料に基づく研究の十分性、選択/欠落、claimとsource/date/比較条件、読者向け説明、実PDFのvisualを作者から独立して確認する。placeholder版のsynthetic semantic NO-GOは未解決のまま引き継ぐ。
- 採用対象に必要な初回制作と通常訂正を確認。機械更新・accepted-upstream訂正・failure/resumeは、既存mechanical evidenceの有効範囲と変更影響を使い、再実行が必要な箇所を選ぶ。全履歴matrixをもう一度制作しない。
- 機械的fixture GateとHumanの意思決定は別。Human受理を必要とする段階は真正の判断を得るまでpendingとし、rehearsalの成功からProduction採用／公開権限を推測しない。
- 費用は§5の既存記録で比較する。品質不合格や通常修正不能は修復／scopeの明示再選択へ、費用不明はunknown。rehearsalだけで純削減達成としない。

### 4.3 固定候補・audit開始とR4出口

**Audit開始条件:** 選択修復が閉じ、採用対象のsupport表とrehearsal dispositionが揃い、その対象に未解決の品質／authority／正常運用blockerがないこと。未代表・延期経路をaudit対象から黙って消さず、維持経路と不足を明記する。必要経路全体が閉じる前の限定candidate auditは可能だが、対象外への採用／whole完了は許可しない。

固定するものは一つの**exact source identity**（実HEAD/treeに加えて未commit overlayの全patch／manifest／modes、採用時commitはHuman）、必要runtime／asset／dependency閉包、復元・診断・必須CI/環境checkと未実行項目、既存historyの扱い、移行・切戻し・旧作業除去表。将来の変更後も133paths/768と固定して呼ばない。partialDBを全history backupと表示しない。

**R4出口:** そのexact bytesとsupport envelopeに対するfresh作者別七観点auditを完了し、採用blockerを解消、残費用・責任・rollback・Human向け採用手順を束縛する。旧component PASSの合計で代用しない。audit中の変更は影響説明と必要な再確認を行うが、通過数のための反復はしない。非blockerの便利機能はbacklogとし、際限なくcandidateを動かさない。

Current Productionとの移行base比較、ordinary commit、実CI/Actions／Releaseは必要な時点で明示Human権限を得る。今回のbaseline774／4GET captureの権限を拡大しない。

## 5. 総費用の判定とR5／R6

既存worklogに、Weekly／必要Special／機械更新／editorial訂正／accepted-upstream訂正／failure-resumeごとに次を短く記す：**現行の具体作業→除去する作業→保持する保証→新しい準備・保守・review・Human費→観測とunknown**。取得可能なwall-clock・LLM usage・再読・handoff・build/repair周回を使う。欠けたtoken/timeを再構成しない。

投資判断では今後の限界費用を比較する。Reconstruction全体の効果を報告する時は過去投資も含め、準備・audit・移行・並行保守を除外しない。旧経路は正常に完了する品質相当の比較にする。必要独立reviewやsemantic judgmentを「削れる重複」と決めつけない。

概念上の収支は `対象期間の反復作業削減 − 追加実装/検証/監査/移行/並行保守/例外対応費`。未知の頻度・horizon・単位費用があるのでbreak-even回数や削減率は現在**UNKNOWN**。P1/P2の除去対象は具体的だが、実際にprojection／手追記／二重driverの仕事が消えたかは運用で確認する。

- **R5:** auditされた範囲でHumanが限定採用を判断し、通常運用・品質非劣化・失敗/rollbackを確認。未確認Specialを採用済みにしない。旧RELEASEDの再承認でもない。
- **R6:** 置換対象の旧作業を実際に廃止し、品質と総費用を評価。既存manual経路が適切なら維持可能だが、その保守・二重運用を計上する。全旧routeの機械的削除を完了条件にしない。
- 作業が単に移った、Human発見負担／repair loopが増えた、旧仕事を外せない場合は、範囲調整・撤回・責任単位の置換を判断する。追加汎用化を自動的な解決策にしない。

## 6. 追加投資を再開する条件

新機能は、(a)必要な具体的edition/操作が現経路では品質・権限を維持して完了できない、または(b)同種の手作業/repairが反復し費用が実際に支配的、と判明した時に比較する。対象caller、外せる仕事、代替の実条件、追加保守/audit費、最小検証を示してAstraが選択し、契約変更には必要な独立reviewとHuman境界を守る。

**延期・非選択:** 汎用非四系列／Retrospective reader、全cadence bridge、Foundations engine、generic IR/resolver、全deferred maintenance修復、新telemetry、full hydration／main refresh。延期はcapability完成を意味しない。重大quality/provenance欠陥には頻度を待たず対応し、別用途の便利機能は採用候補を妨げない。

## 7. 今回の成果・境界・次の一手

Sourceはfinal133（actual409/tree8ce、133paths54M79A/768）のまま。完全DIRECT409 patch `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260` /4931836B、manifest `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` /185422B。今回full133/768/inodeを再認証していない。過去qualified composite、欠落raw／partialDB／非同梱runtime／55Gitlinks・child dirtの限定を維持する。

今回の成果は投資順序とR4条件の再選択。source編集/import/runtime/test/build/fixture/restore/network/Commit/Push/Human Commit readbackは実施しない。**Whole NOT_READY、step4B3 OPEN、audit未開始、DM021+022 OPEN、quality/adoption/savings OPEN。**

独立scope review後に入口を同期し、この再評価unitの**Human Commit Pointで停止**。次のHuman continuationでGeneralが§3の共有修復を実装・検証する。そのcloseout後の次unitは§4の具体的rehearsal/R4準備であり、旧broader-reader必須gateは再開しない。

## 8. 独立reviewへの最終resolution

[独立scope review](../notes/rephase-1-scope-reassessment-20261031/independent-scope-review.md)は§§1–7の投資順序・scopeへ**BOUNDED SCOPE-DECISION PASS**、packet READMEに二つの明確化を要求した。General-Bのmandatory-reader案の該当箇所を明示して上書きし、reduced案末尾のfeature lossが不採用DIRECT-only案だけを指し、DERIVED拒否分岐を許可しない旨を追記した。技術mapの再review／実装／runtime成功／七観点audit／採用／実測削減の承認ではない。

Rootはreviewをこの範囲で受入れる。review §3の「evidence-first」説明は**audit-nowと品質/費用の先行調査を同一視しない**条件で読む。本書§2.3は両者を分け、限定先行調査は可能だが次の予定unitには共有修復を選択した。reader機構を必須化した旧条件の撤回は維持し、必要Specialの実用性を判定する義務は維持する。

Final-binding確認と[文書check](../notes/rephase-1-scope-reassessment-20261031/closeout-document-check.md)をpacketで参照する。現在sourceは不変、次unit未開始。**Human Commit Point。**
