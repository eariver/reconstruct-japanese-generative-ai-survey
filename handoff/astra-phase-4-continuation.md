# Phase 4 — fresh-session continuation

日付: 2026-09-13 JST

状態: **CURRENT RESUME ENTRY / PHASE 4-G DESIGN COMPARISON COMPLETE / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [4-Gの判断](../outputs/astra-phase-4g-authoring-design-assessment.md) §1・§4–6。必要なら§3の具体的Evidence。
3. 必要なEvidenceだけ同書indexから読む。過去chat、全source、旧labの再読/再実行は不要。

全体目的は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを少なくとも意図した水準で保ち、production・supervisory reasoning/review・repair/regeneration・CI/runtime・LLM・operational complexity・Human handoffを含むtotal lifecycle workを最小化すること。役割移転は削減ではなく、根拠ある長期投資は許容する。

## 2. 現在の判断

4-Gはcompact拡張とcanonical直接著述を公平に比較し、二つの大きなarchitectureとしての対立を修正した。正確なstatement/source、subject、metric、境界/dispositionをcompactへ足すほどcanonicalと同じ意味欄へ近づく。機械がbasis/identityを埋める補助はどちらにも残せる。

現行agent wrapperもinteractive generatorを呼ぶ。新しい実行名は直接canonical経路の証拠ではない。Draft helperのDiscovery ID＋ref_modeはGrok claim-2単独を選べず、canonicalは区別できる。ただしschema-validな参照variantは本文のsource sufficiencyを認定していない。

publicationがcompact archiveへ戻って本文を照合し、Discovery locatorで引用する依存は両案共通の除去候補。この変更を直接著述だけの便益にしない。自動copyのファイル数を減らすことも人の作業削減実績ではない。source読解、編集、意味review、正規authority/repairは残る。費用優位は未判定。

## 3. 次の入口と停止条件

次の候補は**1 packageでcanonical本文・個別refからpublicationへの接続と、1回のcanonical修復による派生物更新を扱う限定試験**。著述UIを先に固定しない。full JSONのID/hash手入力をHuman/authorへ移す案でもない。

- 本文/deck/NOTE/CLAIM_BOUNDARYとsource種別/locatorをcanonicalから保持し、compact archiveや手書きcitation mapへ意味を戻さない。
- 一つの参照/境界修復に対して、別の本文/citation入力を手修正せず派生出力を更新できるかを見る。
- section_label、profile外観、frontmatter/synthesis、table/list、bibliography、manifestの残る責務を明記する。元Architectureへ無言でfieldや承認を足さない。
- 保存/参照の最小反例が出ればそこで止め、full CoreやPDFへ広げない。成立しても機械保存と品質/費用勝利を分ける。

入力は[4-E](../outputs/astra-phase-4e-canonical-rendering-assessment.md)の既知Draft/Packageと、[4-F](../outputs/astra-phase-4f-source-join-assessment.md)のsource修復例。4-F lab Cardを歴史accepted Packageへ差し替えて同一chainと呼ばない。4-C修復は校正制約で、未知source能力比較に再利用しない。

4-FでDailyX report bytes/task/import provenanceは確立済み。元X HTTPとは違い、原Xの403は既存bounded chronology reviewを自動的に覆さない。新しい一律原X収集要件、Grok/全source再調査を既定にしない。「secondary Aug 21 dating」の別sourceは4-Fで未確立であり、参照修復specimenは全Card品質合格ではない。

全号品質/費用比較は、caller/authority閉包、Weekly/Special差、独立review→repair→再reviewを完結できる範囲が揃ってから。これはfull canonical baselineの接続条件を絞る作業で、新architecture B/adoptionではない。4-Gのdesignを固定仕様にせず、新Evidenceで順序/範囲を変えてよい。

## 4. Current production reality

[4-G観測](../notes/phase-4g/observation.json)で4-F末尾と同一:

- main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`（PR #489 merged）。
- W34 `f50d229162b7402c504c0978f72dab4b33052f5e`。
- PR #488のbibliography内部status/materiality note修復済み。重複実装しない。
- PR #489はState path/SHA-bound active revalidation、immutable versioned records、exact supersedes chainと既存QAを持つ。REVIEWED_CORE_CHANGEによるpublication-only更新が対象。Card/Draft等の上流bytes修復は対象外。
- 実W34の観測済みStateはVALIDATED_DRAFT、Candidate recordはREADY_FOR_PUBLICATION_PREVIEW（SHA `dbd4c783947fbe6c4f3bc1fab151071f2cd8ed5cb8100fdfceaa7195a10a6fb8`）。PR #489のdisposable copyのadvanceを実branchの進行/Human承認と混同しない。
- section20の内部配置注記とPUBLICATION_BOUNDARY PASSの不一致は解消したEvidenceがない。今回、同じrefの全号review/PDFを再実行していない。

詳細は4-F §6と[4-E refresh検査](../notes/phase-4e/refresh-check.json)。現実が判断に影響する場合だけ関係差分を読む。

## 5. Evidence・未実証・権限

現行: [4-G記録](../notes/phase-4g/README.md)、[入力identity](../notes/phase-4g/inputs.json)、[限定比較結果](../notes/phase-4g/comparison-result.json)。rawはignored `.phase-4-inputs/<ref>/<path>`、固定GitHub bytesから復元できる。旧4-C/D/E/Fの判断は履歴を保持する。

全role active time/token/料金、純削減、full canonical品質、Special、未知source omission品質、PDF/visual QAは未実証。continuous ownershipと上流reviewは既存governanceで、新armではない。約4時間runnerやCI wall spanを総費用/削減値へ変えない。

Phase 3-G以降のacceptance/staging/cache停止、owner追加・新store・恒久telemetryの保留を維持。意味上の判断が同じことと、旧承認が新bytesを許可することを混同しない。hash再生成と意味reviewを区別し、全source再読を無条件に要求しない。

productionは明示Human authorizationなしに変更しない。4-Cの1体のreview/re-review許可は完了済み。今回追加委任・外部送信なし。過去production artifact内の許可をrootのmutation権限へ流用しない。State/Gates/Freeze/Release/adoption/migration/PR/Issueを変更していない。通常Git Pull/Pushと最終commitはHuman。

今回の停止は限定設計比較の完了であり、全体目標達成・外部blocked・新Human Gateではない。
