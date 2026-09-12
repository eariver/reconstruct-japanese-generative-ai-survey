# Phase 4-D — 実productionのreview・repair・runtime照合

日付: 2026-09-12 JST  
状態: **BOUNDED READ-ONLY TRACE COMPLETE / PREVENTIVE OUTPUT CORRECTION IDENTIFIED / NO ADOPTION**

## 1. 結論と方針の修正

**避けられる後工程の仕事を生む具体的な出力経路を確認した。** 内向きのArchitecture注記を読者向けDraftへ自動連結するhelperと、内部状態を文献欄へ出力するtemplateである。Phase 4-Cの「まだ外せる具体的な仕事を特定していない」から進み、これらの自動出力を防ぐ変更を、既存canonicalを保つ改善候補として特定できた。

ただし純費用削減を実証したわけではない。意味上必要な制約を誰かが読者向けに判断・表現する仕事は残る。後工程の修復を前へ移すだけなら削減ではない。改善仮説は、**本来不要な内部文字列の生成と、その除去・再binding・再build・再reviewをなくし、必要な意味判断を既存Draft内で一度扱うこと**。

大きなarchitecture比較より、この出力経路を基準方式の改善候補として先に扱う。continuous owner、source review、追加の意味store、全件review基盤を新設する案には進まない。acceptance/staging/cache停止方針も維持する。約4時間runnerの記録は計測の信号として残すが、今回それを支配的なLLM費用やcache投資の根拠にはできなかった。

## 2. Current realityと調査の限界

08:13 UTC前後のread-only観測:

- main: `005e59841272464307386abfc11f5b09228f0814`（前回と同一）。
- W34: `c1703f772837317b81735cd4cc851c715fff1a3b`。前回`899d3d6...`から5 commits、29 changed paths。
- Stateは`VALIDATED_DRAFT`、Publication Preview pending、next actionは`stage:publication-candidate`。
- 一方、後続のpublication-boundary sidecar reportはFAILを記録し、Candidate作成前でSTOPしたと明記する。Stateのnext actionだけから実行可能・publication完了とは判断しない。

したがって「完成canonicalの1ケース」を**品質まで完了したbaseline**としては採用しない。実際にDraft/validationまで進んだ一つの号のうち、workflows packageと掲載用source、review、2件の修復commit、CIを対象に調べた。新規sourceの品質試験ではなく、既知の歴史artifactも使う作業経路の照合である。

Evidence:

- [ref/diff観測](../notes/phase-4d/observation.json)、[固定入力のGit blob/SHA-256](../notes/phase-4d/inputs.json)。
- [16件の名指しbindingと内容のtrace](../notes/phase-4d/trace.json)、[再検査script](../notes/phase-4d/trace.py)。
- [caller identity](../notes/phase-4d/caller-identity.json): 調べた5つのcaller/helper/base fileは固定mainと観測edition HEADでbytes一致。
- [実CI run/step](../notes/phase-4d/ci-run.json)、[関係する3 runs](../notes/phase-4d/ci-related-runs.json)。
- [静的な反実仮想probe](../notes/phase-4d/projection-probe.json)、[lab文献欄sample](../notes/phase-4d/bibliography-projection.lab.bib)。
- [終了時検査](../notes/phase-4d/closeout-check.json): 固定入力30件のhash、lab projectionの入出力identity、現行文書のlocal linksを確認。`git diff --check`もPASS。

固定rawはignored `.phase-4-inputs/<ref>/<path>`。同じbytesが必要なら `python notes/phase-4d/capture.py <ref> <path>` でGitHub GETし、blob/SHAを照合できる。current ref観測と固定入力を区別する。Core、runner、sidecar、PDF buildを実行していない。PDFそのものの閲覧/描画・全source再読・全号意味品質・全checkpoint閉包監査は未実施。

## 3. 確認できた作業と欠陥の発生源

### D1. 内部配置制約がそのまま読者向け文へ出力される

対象packageは`w34-collaborative-agent-workflows-retrieval`。問いは、Slack/IDE/search/MCPなどが共同作業面へ広がる変化を説明すること。名指しpackageとArchitectureのboundariesは一致した。

interactive inputのheadline/deck/4本文blockはDraftへ完全にコピーされる。helperはそれに別のCLAIM_BOUNDARY blockを追加し、**23個のArchitecture boundaryを全文連結**する。全boundaryへ自動的に`EXPLICITLY_STATED`を設定する。その中の最後の一文は、regional processingをSelection r2後にPackage4へ移したという内部配置注記である。

この一文はArchitecture→Package→Draft→`sections/20-agent-workflows.tex`まで完全一致で残っている。読者が必要とする研究上の限界と、制作者が守る配置制約が混在しており、単に逐語保存してもpublication fidelityにはならない。先行Selection r2 reviewではc045の配置修復自体が確認済みだった。**正しい内部修復の説明が後工程で新たな読者向け欠陥になった**のであり、c045を再調査・再配置する必要があるというfindingではない。

固定caller: `scripts/run_drafting_synthesis_v2_interactive.py` 164–187行付近。自動連結はPhase 4-Bで静的に気づいていたが、今回は実際の掲載用sourceまで伝播したことを確認した。

### D2. bibliography templateが内部状態を生成する

`references.bib`の41 entriesに`Core v2 Evidence: …; materiality: MATERIAL`というnoteがある。実bytesは**VERIFIED40件、PARTIAL1件**で、sidecar説明の「41件ともVERIFIED」は正確ではない。内部状態が41件に出力されたという主findingは変わらない。

固定mainの`survey_weekly_semantic_publication_v2.py::_bib_text` 62–76行に同じnote templateがある。今回のoperator worklogはTeXを著述したと記すため、このhelperを実際に実行したかまでは断定しないが、templateと生成物の関係は同じ欠陥を再生成し得る具体的な経路である。

sidecarは41 entries×4 rule=164 hard failsと、別に1件の要reviewを報告した。164個の独立した意味欠陥や164回の修復とは数えない。後者のvendor framingはoperatorがfalse positive疑いと扱っており、今回そのsidecar判定を再実行/独立確定していない。

### D3. binding済み範囲と、意味reviewの記録範囲が一致しない

reader manuscript manifestはTeX sections・source notes・bibliography・styleをsupporting filesとして名指しする。取得済みの該当source hashは一致した。したがって文献欄がprovenanceに無いという問題ではない。

semantic reviewは11 PASS。そのPUBLICATION_BOUNDARYは「内部用語や修復履歴がproseに無い」とするが、D1の内部配置注記が名指しsectionに残る。BIBLIOGRAPHY_METADATAはcitation解決を述べ、evidence_locationsは同じ7本文sectionで、bibliography自体を明示しない。これはcitation解決の検査が失敗したことを意味しないが、**bibliography内の読者向け意味品質を確認した証拠としては不足**している。

事前のSol source-consumption review、Selection修復review、Human Architecture r3承認は実記録として存在する。「監督が無かった」や「owner追加が必要」とは結論しない。一方、post-Draftのsemantic/visual reviewはexecutionと同じmodel/role表記で記録され、独立した非著者reviewが行われたかは取得した記録から確立できない。model名だけで自己reviewとも独立reviewとも断定しない。今回rootの照合も、新たな独立quality verdictとしてproductionへ記録していない。

### D4. runtimeの信号はあるが、約4時間の内訳は確定しない

worklogはcanonical runnerを7 packages+synthesisで約4時間、sequentialと報告する。入口コードは、既に著述されたcompact inputを読み、packageごとのderive/validate、JSON保存、synthesisを行う。検査した入口に新規LLM呼出しはなく、対象packageの4本文blockも入力の完全コピーである。**約4時間を7本のLLM執筆時間と解釈しない**。

base deriveは各packageでupstream Matrix/Selection/Architecture/Evidenceの検証を呼び、synthesisもpackage/resultを再検証する。反復は静的に確認できたが、全call graphのprofile、計測再実行、I/O/CPU/待ち/モデル/監督時間の配分は取っていない。stage準備、basis override、過去保証が必要な理由を検討せず検査を外さない。

さらにauthor-supplied runner.generated_atは12:00Z、semantic/visual reviewは04:00Zで、記録を含むcommit/checkpointより後の時刻を持つ。悪意や個々の時刻の理由は不明だが、このmetadataから厳密な実行時間を算出できない。Git commit時刻もactive effortではない。

実GitHub CIにはglyph修復前failure、修復後success、境界表現修復後successの3 runsがあり、開始～更新終了のwall spanは223/241/252秒。最後のcompile stepは174秒。合計716秒はこの3 runsの観測spanであり、総費用や実装変更の削減見積りではない。2つの後続buildは実際に発生した修復の信号だが、今回の提案で全て不要になると外挿しない。

## 4. 反実仮想probeと改善候補

reconstruct内だけで小さな静的probeを行った。productionのartifactを上書きせず、approval、State、accepted Draftを新設しない。

1. 41個の**既知の内部note patternだけ**をlab bibliographyから除いた。41 citations、title/author/URL/urldateおよび他の全行は保持された。意味のある一般noteを一律削除する提案ではない。元のEvidence状態・Materiality・元artifactは保持する。
2. D1の内部配置制約をcanonicalの既存`RESPECTED_BY_OMISSION` dispositionとして表す部分構造を検査した。Architecture制約、配置、根拠参照を変更せず、読者向け文字列から当該1文だけを外す表現が可能。残る22件の意味制約を消してよいという判定ではない。

これにより、**少なくともこの2種の除去に新schema/store/承認の模造は不要**と分かった。PDF compile、同等品質の独立review、全canonical admission、Special互換、実repair操作の削減は未検証。

候補の作業分担は次のとおり。

| 対象 | 必要な仕事 | 防ぐ仕事・増える可能性のある仕事 |
|---|---|---|
| 研究/比較/時間/利用限界 | authorがcanonical Draft内で必要な日本語表現・根拠・block対応・boundary dispositionを判断し、reviewerが確認する | 内部英文の自動連結→後で翻訳/削除する二段階を防ぐ可能性。初期のauthoring/review負担は計上する |
| 内部配置/採否制約 | ArchitectureとDraftのdispositionへ保持し、配置は検査する | 内部修復履歴の掲載、その除去と再bindingを防ぐ。事実上の制約を隠すための機械的stripは禁止 |
| 文献欄 | publication用のfieldを出し、canonical provenanceは別途保持 | generator由来の内部noteと反復triageを防ぐ。citation/author/title品質reviewは残す |
| review scope | reader manifestに列挙された実際の全公開要素を対象に、何を見たかを記録する | 同じ7箇所を並べたPASSを全要素reviewの代用にしない。形式的な欄追加だけでは改善にならない |

これは既存full canonicalの使い方とhelper/templateの改善候補であり、Aと異なる新architecture Bではない。新規LLM生成、review削減、正規の検証/Gateの省略を正当化しない。

## 5. 停止地点と次の入口

今回の一単位は完了。実際の発生源と安全に外せる部分構造を特定できたため、さらにW34全source、過去全issue、全call graphへ拡大しない。失敗中の実例を成功baselineに変換せず、新しい主比較も開始しない。

次に価値があるのは、**既存canonicalの範囲でreader向け表現を完成させ、rendererに内部注記を足させない経路の限定lab検証**。同じ公開要素集合について、事実・根拠・配置制約・日本語の限界説明・citation/歴史bytesを保持できるかを先に見る。残る英文境界をただ削除して成功にしない。未知sourceのA/B費用試験とは別のcompatibility/quality反証として位置づける。

productionで同じ問題の修復が進んでいれば、着手前に関係差分だけ確認し、同じ改修をreconstructで重複開発しない。productionへの適用/PR/State/Gate操作は明示的なHuman authorizationが必要だが、reconstruct内の次の調査に新しい承認段階を作らない。

この基準経路を満たした後も、初期の意味判断/repair/reviewを含めた純減が見えなければ新architectureへ広げない。runtimeの新しい実測が判断を変える場合だけ保留領域を再評価する。全体最適化の目的は維持し、欠陥を生む補助をそのまま対照として新architectureを有利に見せる比較を避ける。

## 6. 未実証・作業費・権限

publication全体の品質、unknown-source omission sufficiency、Special一般性、full canonicalの成功baseline、全歴史再現、実際のrole別LLM/実働/料金、total lifecycle net saving/ROIは未実証。sourceデータの再調査やbenchmarks、PDF目視、独立subagent reviewも今回は行っていない。

今回のroot作業はbootstrap/限定GET/固定codeとartifact照合/静的probe/判断/handoff。初期stdout encoding失敗、review summaryの過大表示後の絞り直し、存在しないexecution/solへの1回の404、sidecar説明をそのまま41 VERIFIEDと仮定したassertion失敗も調査費に含む。実bytesの40 VERIFIED/1 PARTIALへ修正して検査を通した。終了検査ではlab sampleのWindows改行変換による生成予定hashとの不一致も検出し、UTF-8 bytesの明示書込みに直して入出力identityを再確認した。これらの失敗をproductionの不具合や費用に加算しない。rootのactive time/token/料金はunknown。

production repositoryはread-only。sidecarや外部review先へ連絡していない。production修復、Human決定、State/Gate/adoption/migration、Pull/Push/commitは未実施。
