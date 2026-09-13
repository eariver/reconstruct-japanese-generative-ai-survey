# J-GAS — Phase 4 closeout / current continuation

日付: 2026-09-13 JST

状態: **PHASE 4 CLOSED / OVERALL RECONSTRUCTION OBJECTIVE CONTINUES / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [Phase 4終了判断](../outputs/astra-phase-4h-connection-and-closeout.md) §1・§4–6。W34の現実は§2、接続反例は§3。
3. 必要なEvidenceだけ読む。旧session/chat、全source、過去labの再実行は不要。

全体目的は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを少なくとも意図した水準で保ち、production・supervisory reasoning/review・repair/regeneration・CI/runtime・LLM・operational complexity・Human handoffを含むtotal lifecycle workを最小化すること。仕事の役割移転は削減ではなく、根拠ある長期投資は許容する。

## 2. なぜPhase 4を閉じたか

4-Cの研究・編集sliceは独立review→repair→再reviewまで完了し、canonical意味欄の利用可能性と意味品質の重要性を示した。ただしfull canonical baselineや費用優位は未実証。4-D以降の既知W34追跡は、情報を落とすhelper/source/citation接続を具体化した一方、中心の全role仕事比較へ戻れていない。

4-Hは1 packageのcanonical出力を試し、同じrelease-notes URLに異なるtitle/published_at/accessed_atが対応する箇所で停止した。URL集約時の先着metadata採用を防ぐためrootが置いたlab guardであり、production schema違反やcanonical生成不能ではない。section生成も予定したrepair/regenerationも未完了。反例を再現したことをpublication PASSにしない。

追加のsource-identity/citation規則は設計できるが、局所adapter完成を主比較の前提にし続けない。[Phase 3-G再評価](../outputs/astra-system-direction-reassessment.md) §1・§5・§7の停止原則を適用し、この調査経路を閉じた。全体目標達成、quality合格、production採用を宣言したのではない。

## 3. 次の入口と進める条件

**4-H probe修正、renderer完成、全W34 source追跡を既定にしない。** 次の一単位は、問い→source→採否→本文→独立review→repairで、実際に異なる仕事の単位を比較できるかを決める設計判断。

- 同じ読者価値・coverage/品質義務で、どの仕事を除く/まとめるかを一文で示す。継続owner/事前review追加は現governanceに既にあり、新Bではない。
- taskの完了単位や研究・編集の往復順序は再検討可能だが、現運用が既にその方式でないかを対象範囲だけ確認する。役割/model/欄への移転やrepair前倒しだけなら棄却する。
- canonicalに詳細を書くだけ、または両案へ同じ便益を適用できる場合は共通化し、無理に対案を作らない。4-Gの「lossless compact対assisted canonical」も独立architectureとして未成立。
- 意味のある差がある時だけ、未回答source・HOLD/除外対照・共通品質基準・非著者source-first review→repair→再review・全role費用観測を固定して一往復を始める。旧W34/P-EAGLE等を未知source比較にしない。
- full Core/renderer実装を準備の前提にしない。labで省くproduction必須工程は両案とも明記し、ゼロ費用の勝利を作らない。Humanを無償reviewer/計測係にしない。active time/token不明はunknownのままにする。

現時点で有効な新B、主比較、Phase 5開始を決定/実行済みとは扱わない。次のAstraが新Evidenceで順序・範囲を判断する。外部blockedや追加Human Gateではない。

## 4. 保持する設計Evidence

- [4-C](../outputs/astra-phase-4c-trial-assessment.md): source/metric/帰属/限定の4欠陥を修復。機械PASSと意味品質を区別する校正例。
- [4-E](../outputs/astra-phase-4e-canonical-rendering-assessment.md): 22境界＋内部omissionを既存欄で表現。helperのsection_label/CLAIM_BOUNDARY/compact引用制約、旧renderer全体drop-inの不適合。
- [4-F](../outputs/astra-phase-4f-source-join-assessment.md): DailyX report bytesはtaskにあり、compact一括sourceで対応を落とす。reportは元X HTTPではない。原X403で既存bounded chronology reviewを自動的に覆さない。参照修復は未採用で全Card意味品質は未完了。
- [4-G](../outputs/astra-phase-4g-authoring-design-assessment.md): 個別claimはDiscovery ID＋ref_modeから選べない。忠実な入力補助はcanonical意味欄へ近づき、共通consumerの便益を直接著述だけへ計上できない。
- [4-H反例](../notes/phase-4h/probe-result.json): URL identityとsource occurrence/display metadataの扱いを暗黙に決めない。

source/citation/rendererは保守候補として保持し、採用候補への接続や実運用の反復負担が投資を裏付ける時だけ再開する。Phase 3のacceptance/staging/cache、新store、恒久telemetry保留も維持。既存architecture自体を永久固定するものではない。

## 5. Current production reality

[4-H観測](../notes/phase-4h/observation.json)、[限定binding検査](../notes/phase-4h/refresh-result.json):

- main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`。
- W34 `8480f4dfffb57b456d1147fcc5360f7864bb19df`。**実State RELEASE_CANDIDATE / PUBLICATION_PREVIEW pending、Human provenance null、Freeze/Release pending**。
- State-bound publication revalidation `2398c332…`と歴史checkpoint、新checkpoint→Candidate/stage recordの4 bindingを照合。PR #489は実号で一度使われた。旧「disposable copyのみ」を現在状態へ流用しない。
- Candidateは旧f50d229と同じ。payloadのcandidate_sha256は`dbd4c783947fbe6c4f3bc1fab151071f2cd8ed5cb8100fdfceaa7195a10a6fb8`、raw file SHAは`c45adaf79edad782db7bb21ee1f62fd7794773a4cdeddc6a9697fdd046592f00`。
- Evidence/Selection/Architecture/Draft/reader pathsは今回の差分で不変。内部配置注記/source反例はadvanceで修復されていない。PDFはmetadata対応と差分だけ確認、目視/full State検証/独立quality認定なし。
- PR #488 bibliography修復、PR #489 publication-only revalidationをbaselineへ含め、重複実装しない。Card/Draft上流変更をpublication-only例外へ押し込まない。Preview承認/Releaseや純費用削減は未認定。

current realityは判断に関係する差分だけ更新し、毎回全号監査しない。

## 6. 未実証と権限

full canonical baseline、全号品質、未知source omission、Special実行、全歴史/caller互換、PDF/visual QA、今回の接続成功・repair往復、total lifecycle純減、role別active time/token/料金は未実証。4-Cの独立review完了を他probeへ拡張しない。

productionは明示Human authorizationなしにread-only。State/Gates/承認/Freeze/Release/adoption/migration/PR/Issueを変更しない。4-Cの1体のreview/re-review許可は完了済みで、将来の比較へ流用しない。今回追加委任・外部送信なし。通常Git Pull/Pushと最終commitはHuman。
