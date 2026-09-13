# J-GAS — Phase 5 continuation

日付: 2026-09-13 JST  
状態: **PHASE 5 ACTIVE / 5-A COMPLETE / NEXT 5-B WORK-UNIT OBSERVATION / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [5-A判断](../outputs/astra-phase-5a-work-unit-decision.md) §1・§3–6。
3. 必要時のみ[5-A Evidence](../notes/phase-5a/evidence.md)。Phase 4の復元は5-A §2と[4-H closeout](../outputs/astra-phase-4h-connection-and-closeout.md) §4で足りる。全chat/旧lab再実行は不要。

基準はHuman指定のPush済みreconstruct main `64b78ec6aa94c5c1a81b3a1dd14f6a958b99f962`。5-A開始時local/remote一致・cleanを確認。これ以後の5-A変更はHumanのcommit/Push対象であり、commit済みとは扱わない。

全体目的: publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準以上に保ち、production・supervision/review/reasoning・repair/regeneration・CI/runtime・LLM・complexity・Human handoff/manual burdenを含むtotal lifecycle workを最小化する。移転は削減ではない。初期投資/移行/歴史互換/二重保守込みで判断する。

## 2. 5-Aで決めたこと

**新architecture BやA/B費用試験は未選定。5-Bは一つの問いの研究→本文→独立review→repairで、除ける意味再構成があるかを観測する。** full Core/renderer/canonical production baseline完成を前提にしない。

仮説は、同じsubject/source版/比較条件について、候補別調査の完了時と後段の横断編集時に同じ比較可能性を組み立て直しているなら、一度のsource横断検証と既存欄への引継ぎで後者を除ける、というもの。**その反復はまだ実証されていない。** sourceごとの読解、事実と採否の別判断、独立review、誤り修復、自動コピーは除ける同一作業に数えない。

確認した境界:

- current v2 Coreは1 Discovery/Taskを実装・検証する。schemaの複数ID許容だけを見てjoint Taskを受理可能としない。
- interactive runnerは複数著述済みrecordsを一括消費できる。保存Task数はLLM仕事数ではない。
- governanceは継続監督、source review、候補横断grouping、適応的gap fill、未選択risk reviewを既に含む。これらの追加をBにしない。
- W34の409 task-local records/後段clusterはartifact上のEvidence。認知作業の反復やその費用は不明。
- compact対canonical、問い共有、良いauthoring等の共通便益で差が消えれば共通化して止める。現方式に不自然な禁止を課して対照を作らない。

## 3. 次の具体的入口と停止条件

5-A §5に従い、未回答の一つの問い、3–4候補、採用し得る候補と強いHOLD/除外対照、cutoff/lane/探索範囲、同等の品質/coverage、raw/version/hash、source-first非著者review、実際に取得可能な費用観測を**出力前**に固定する。source群は未選定。W34/CAS/P-EAGLE/DFlash等を未知source標本へ再利用しない。

作業記録は意味判断の変更/sourceへの再訪時だけ、問い/比較軸、subject/source版、role、再訪理由、既存結論、新しい判断、影響先、計測値/unknownを記す。一時観測であり新しい意味正本や恒久telemetryにしない。authoringと分類/reviewの費用も加算する。

非著者review→最初のrepair→再reviewを一区切りとする。残件は不合格/未実証。実質的な再構成が無ければ仮説棄却、記録が識別できなければ識別不能で止める。無理にBを追加しない。実質的な差と代替費がある時だけ5-Cのfresh source比較を設計する。同じauthorの同じsource二周を独立費用試験にしない。

独立reviewerを今回は起動していない。4-Cの一体許可は終了済みで、新委任に流用できない。独立性を確保できない実行は自己点検の範囲に留める。5-Aの完了は追加Human Gate待ちではない。

## 4. Current production realityと保留

[5-A GET観測](../notes/phase-5a/observation.json): main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`、W34 `5561e2328a09061a3e0c8e881d24ddcb03e1e975`。4-Hの`8480f4df`からはworklogのmerge ancestry修正1 commit/1 pathのみ。

実StateはRELEASE_CANDIDATE / PUBLICATION_PREVIEW pending、Human Preview provenance null、Freeze/Release pending。State/Candidate/Evidence/Selection/Architecture/Draft/reader pathsはこの差分で不変。full State validation・binding全閉包・PDF/quality reviewは繰り返していない。4-HのCandidate payload digest `dbd4c783…`とraw hash `c45adaf7…`は別。今回Candidate再hash済みとは言わない。

PR #488/#489は既存baseline修復。reconstruct成果やPreview承認/Releaseに数えない。内部注記/source反例は今回のadvanceで修復されていない。Card/Draft修復をpublication-only rebindへ押し込まない。

Phase 4はclosed。4-Hはsection出力前にlab URL集約guardで停止しrepair未実行。production schema違反/source矛盾/publication成功ではない。historical Packageとlab修正Cardは別。renderer/citation/source-identity、acceptance/staging/cache、新store/恒久telemetryは保留。正規採用接続や実反復負担の新Evidenceが出た時に再評価する。

## 5. 未実証と権限

作業差/純削減、full canonical baseline、全号品質、未知source omission、Weekly/Special全体一般性、歴史/caller互換、PDF/visual、全role active time/token/料金とROIは未実証。labで省くproduction必須工程をゼロ費用にしない。Humanを無償reviewer/計測係にしない。

productionは明示Human authorizationなしにread-only。State/Gates/承認/Freeze/Release/adoption/migration/PR/Issueを変更しない。外部送信/追加委任なし。通常Git Pull/Push/最終commitはHuman。次sessionではcurrent reconstructのPush済み状態を確認し、本handoffから必要な範囲だけ進む。
