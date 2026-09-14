# J-GAS — Phase 5 continuation

日付: 2026-09-15 JST
状態: **PHASE 5 ACTIVE / CURRENT UPSTREAM RECONCILED / RESIDUAL MAINTENANCE / NO 5-C TRIAL / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [current Core照合判断](../outputs/astra-phase-5-upstream-reconciliation-assessment.md) §1–4。限界は§5。
3. 必要時だけ[今回Evidence](../notes/phase-5-upstream-reconciliation/README.md)。[旧runtime候補](../outputs/astra-phase-5-runtime-repair-assessment.md)と[reader計画](../outputs/astra-phase-5-review-plan-and-runtime-priority.md)は再利用用の歴史入力。全chat/旧lab/全source再読・全test再実行は不要。Phase 4の復元は[5-A判断](../outputs/astra-phase-5a-work-unit-decision.md) §2で足りる。

今回の開始reconstruct local/remote mainは`b8bdf9821a48d22b2db840458b1b385f1c744bdb`で一致・clean。productionのHuman指定main `774dd39a951c9ac3818e83dfffd4c7666efb0a20`をGET確認し固定した。通常Pull/Push/最終commitはHuman。旧commit名`Astra work Phase 5-C`はHuman補足によりphase authorityではない。publication review boundary investigationとconditional 5-C A/Bを混同しない。

全体目的: publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを維持し、production・supervision/review/reasoning・repair/regeneration・CI/runtime・LLM・complexity・Human handoff/manual burdenを含むtotal lifecycle workを最小化する。移転は削減ではない。初期投資/移行/歴史互換/二重保守込みで判断する。

## 2. 5-Bで判断可能になったこと

**一つの問いの研究→本文→source-first非著者review→root修復→一度の再reviewを完了。除ける意味再構成の具体的支持例は得られず、5-CのA/B比較は開始しない。** 新architecture B、Task統合、新意味層は選定していない。

2025-04-28〜05-05未満UTCのWeekly窓で、Mem0 v1を主題、A-MEM v5をcutoff前の背景、MemOS v1をcutoff後の強い関連HOLDに固定。出力前protocol、取得raw/版/hash、r1/r2、独立期待内容とreview、作業観測を保存した。A-MEM v1は準備履歴のみ。full Weekly Discoveryやblind sampleではない。

初稿はblocking一件（評価規模・Jの判定条件等の読者説明不足）、補足三件（版別著者順、graph版の逆転、日本語/負担比較の向き）。facts→composition→本文を修復し、独立再reviewで全件解消・追加findingなし。[r2本文](../notes/phase-5b/r2/manuscript.md)はこのsliceの結果であり、全号publication quality認定ではない。judgeのexact版、A-MEM引用表と原表のカテゴリ対応、再実行設定/集合の同一性等は未解決として直接順位付けを保留した。

新しい意味層なしで必要な横断比較と根拠の引継ぎができた限定例だが、それでも独立review/repairが必要だった。source固有の初回検証、事実から採否/読者説明への変換、独立review、誤り修復、自動コピーを「同一作業の削減」に数えない。current Coreの1 Discovery/Taskと保存数は認知仕事数ではなく、既存runnerのbatch著述入力とgovernanceのgrouping/適応研究をBの新機能にしない。

**非支持と識別不能を分ける。** W06/W08のraw再訪理由は合理的だが、各時点の既存結論の完成度・再確認の内訳・除去可能量は識別不能。role別active time/token/料金もunknown。反復ゼロの実測でも全productionでの不存在証明でもない。5-Aの「仮説棄却」は今回の比較投資停止として適用し、一般仮説の否定へ強めない。単一rootが研究/編集/本文を続ける観測であり、実運用の別session/roleへのhandoff損失を十分に励起したかも不明。

## 3. 今回の判断と次の入口

**current upstream照合とrootの限定reviewを完了。旧patch一式のreview/適用を次の入口にしない。** #495がRelease helperのCORE report欠落を修復し、dual reviewとcontroller照合も実装した。旧候補とはFROZEN semanticsやtimestamp再利用の設計が異なる。旧候補の試験成功をcurrentへ移さない。

Freezeは未解消: runtimeがschema-required visual-review-recordをextraとして拒否し、`_prior_artifacts`はHuman approvalをStage Checkpoint型で読む。前者はcurrent関数、後者はcurrent実W34 approvalのpointer/hashと当該schemaで確認。以前の合成全chain試験は[旧Evidence](../notes/phase-5-runtime-repair/README.md)に保持し、今回全chainを再実行したとは言わない。

#496でpre-TeX structured input/persisted semantic review/下流gateが実装されたため、前回の新規入口実装計画は更新が必要。限定probeは次を再現した:

- review済みJSON/reviewを固定し、現在のprimary TeXとmanifest hashを別の読者本文へ変更しても、gate生成・再検証がPASS。review対象ファイル自体のdriftは拒否される。個々のhash検証とrender導出関係は別。
- `frontmatter.lede`変更でTeXは変わるがpre-TeX review input hashは同じ。cover anchors、frontmatter、summary heading等のrender入力がprojectionから落ちる。後段lintは早期reviewの網羅を代替しない。
- TeX/Bib不変でもmanifestのaudit説明`architecture_coverage.detail`だけでlintが停止。読者本文に出ない説明を修復/例外管理する仕事へ移さない。

これらはcurrent実関数/schemaと合成reviewのwitnessで、実editorial判断や全stage/Human Gate突破の証明ではない。全Specialのrender網羅、全CLI/歴史互換は未検証。今回agent起動なし、独立reviewなし。

**次は現判断§4に沿ったreconstruct-onlyの限定修復。** 最初はFreezeのartifact集合とtyped approval解決を、current reader gateと上流Release producerを保持して修復。旧候補の該当部分/negativeを再利用する。その後、別差分でreaderの完全なprojection・現在のmanuscript/出力への結合・audit除外を扱う。既知不整合が残る旧patchの独立reviewやreader実運用trialを先行させず、前回計画そのものを再執筆しない。上流が進んでいれば当該残差だけ再照合する。

各単位は失敗再現、修復後正常系/authority negatives、関連回帰、未実証の記録をreview可能にして止める。新agentは具体物について新しい明示許可が必要。4-C/5-B許可を再利用しない。production posting/application/adoptionは別権限。今回の停止は許可待ちではなく、upstream照合と残差処遇を揃えた判断面による。

[旧runtime候補](../notes/phase-5-runtime-repair/candidate.patch)は未変更。初回58 testsの52 PASS / 6 Git-root errorsと隔離後8 PASSを合成して初回全成功にしない。最初のfixture objects/test ref生成とcleanup履歴を消さず、後続Git-aware testは独立Git rootでのみ実行する。今回はhash確認したsupport 307filesとcurrent変更をignored labへコピーし、Git非使用の関数/schema probeだけを実行した。最初のPath引数によるprobe二回停止と修正もEvidenceに記録。

local retryの旧実証は固定済み外部成功Release RecordからState advance前に再開する範囲。current producerのtimestamp equality、Actions全dispatch、record builder再利用、main変化、RELEASED後、legacy caller互換は未実証。必要なsource/独立review/PDF/Human工程を省略せず、追加の検証/保守/引継ぎ費を含む純削減はunknown。

## 4. Last observed production reality

今回mainは`774dd39a951c9ac3818e83dfffd4c7666efb0a20`。3e3eebe0から8 commits / 16 changed filesで返却capなし。変更script/schemaを取得したが全Core監査ではない。旧112-commit/300-file打切り比較とは区別する。[current観測](../notes/phase-5-upstream-reconciliation/observation.json)。open Issueタイトル5件のindexは取得したが、全本文/closed Issue/PR reviewのinventoryではない。

実W34 main Stateは**RELEASED / next null**。Release checkpoint raw SHAはState pointerと一致し、新schemaでも受容。既にCORE_STAGE_CONTRACTとRELEASE_EXACT_BYTE_RECONCILIATIONを持っていたので、schema強化だけからW34 historical breakageを推定しない。全State/report依存閉包の再検証ではない。

前回観測ではW34 branch `3bad8a57cf2b246c7f71cb749ba3105fa318b073`がFROZEN / stage:release、main 3e3eebe0がRELEASED / COMPLETE。今回branch/公開asset/PDFはfresh確認していない。旧観測のCandidate raw SHA `df376f474acf5fafa14f9af5196727858b1dd76f5c7d17664fa52ba784e32061`とpayload `52c8d0bcc85140a2727d1867a908d7077d40c7088a7c1e83f10b66044c50f3ba`を区別。PDF `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`、public server digest/338722bytes等の[旧局所check](../notes/phase-5-review-plan/check.json)は歴史Evidenceである。

#492書誌access provenance、#493 frozen authority/Release recovery、#495/#496のCore改修はproduction成果で、reconstruct採用/純削減ではない。全source/citation問題の解消認定でもない。Human #491/5654102081のW35+早期reader gate方向を保持し、Humanが受容したW34残余audit語彙を再生成しない。

Phase 4はclosed。4-Hはsection出力前のlab URL集約guardで停止しrepair未実行。historical Packageとlab修正Cardを分ける。renderer/citation/source-identity、acceptance/staging/cache、新meaning store/恒久telemetryは保留。この限定保守はconditional 5-Cではない。

## 5. 未実証と権限

実仕事差/純削減、full canonical baseline、全号品質、未知source omission、Weekly/Special全体一般性、歴史/caller互換、PDF/visual、全role費用とROIは未実証。labで省いたproduction必須工程をゼロ費用にしない。Humanを無償reviewer/計測係にしない。今回の記録/取得/独立review/repair/引継ぎと委任確認・usage中断後の再開も観測費から外さない。

productionは明示Human authorizationなしにread-only。State/Gates/承認/Freeze/Release/adoption/migration/PR/Issueを変更しない。外部送信/追加委任なし。通常Git Pull/Push/最終commitはHuman。歴史判断を上書きせず、この入口から必要な範囲だけ継続する。
