# Phase 4 — fresh-session continuation

日付: 2026-09-12 JST  
状態: **CURRENT RESUME ENTRY / PHASE 4 STARTED / FIRST BOUNDED INVESTIGATION COMPLETE**

## 1. 最小の再開入力

1. 本handoff。
2. [Phase 4判断](../outputs/astra-phase-4-comparison-basis.md) §1・§3・§5・§7。費用条件が必要なら§6。

Phase 3-Gの全体目標・安全制約は継承済み。過去chat、Human-Sol logs、Phase A、旧labの再実行を開始条件にしない。`notes/phase4-*`等はPhase 3中の歴史probeであり、新Phase 4の資料は`notes/phase-4/`にある。

## 2. 今回変わった判断

- 継続したresearch/editorial ownerは現行governanceにすでにある。W34の実Selection/Architectureにも問いとboundaryの引継ぎがある。旧Bの「ownerを明示するだけ」の部分をAの共通条件へ吸収し、独立した比較armにはしない。
- これはAの優位やBの全利益の否定ではない。次はfull canonicalと既存責任で、source読解→採否→短い本文→非著者review→修復まで品質条件を満たす小さな完了例を作り、全roleの仕事を記録する。そこで反復する意味再構成が残るなら、仕事の順序/単位を変える対案を一つ比較する。
- acceptance/staging/cache、Core置換、review削減・全件化、新しい意味store、恒久telemetryは開始しない。実測で情報価値が変われば再評価可能。

目標はpublication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを少なくとも意図した水準で維持し、production/supervisory/repair/CI-runtime/LLM/複雑性/Humanを含むtotal lifecycle workを最小化すること。役割間の仕事移転は削減に数えない。長期純削減を裏付けられる初期投資は許容する。

## 3. 実施済みのEvidenceと限界

[manifest](../notes/phase-4/basis.json)と[4件trace](../notes/phase-4/trace.json)を固定。GitHub GETによるread-only観測、Git blobと名指しSHA-256照合、targeted source読解を行った。Core/CI/PDFや旧labは実行していない。

| 標本 | 引き継ぐ知見 |
|---|---|
| c019 Mistral Agentic Search | Task→Card→View→Selection→Architectureに機構/帰属/利用目的がすでにある。本文完成の証拠ではない |
| c045 regional processing | directive由来のcluster誤りがr2で修正され、canonicalへ保持。修復費用削減は未測定 |
| c033 OpenRouter rankings | 未確認benchmarkをHOLDへ保持する具体例。追加探索の十分性は未評価 |
| arxiv-2608-20771 CAS | Cardの方法文にUI文字列、保存本文にある§7 Limitationsが未消費、記録はCONSUMED。source固有の読解不足を確認。採用すべきという判定ではない |

CASのRawはhash確認済み。本文§3.2、§3.4、§4.1–4.2、§7を対象に照合した。詳細と反例P4-F1–F3は判断書§3。4件は**結果を見ながら選んだ歴史校正例**であり、未知sourceの比較材料に再利用しない。新しいcanonical candidate、読者本文、修復後reviewは作っていない。

調査script [capture_basis.py](../notes/phase-4/capture_basis.py) は`python notes/phase-4/capture_basis.py`で固定refを再取得できる。入力cacheはignored `.phase-4-inputs/`。upstream checkoutやCoreを実行/変更しない。manifestは最新observed refsと固定analysis refsを区別する。原則、再開時に再実行は不要。出力を再生成すると観測時刻が変わるため、新しい調査Evidenceを混ぜる際は旧scopeを保持する。

## 4. Remote reality

開始時はPhase 3最終観測と同一。終了時にedition branchの進行を検出し、関係差分だけ確認した。

- main `005e59841272464307386abfc11f5b09228f0814`
- 4件の固定分析ref: `weekly/2026-W34-v2-work@601481acd9b82ee8fa0c2eb28a2ca28636165d60`。この時点のStateは`ARCHITECTURE_ESTABLISHED`、Architecture approved、Publication Preview pending、Draft pending。
- 終了時の観測ref: `899d3d6ab96c14bb82ea24b0ae12700e798a781f`。1 commit追加、Stateは`DRAFT_COMPLETE`、next action `stage:reader-publication-validation`、Architecture approved、Publication Preview pending。Draft/Synthesisと検証recordが追加され、今回のEvidence/Selection/Architectureは不変。[追加観測](../notes/phase-4/late-observation.json)に保存した。新Draftの意味品質/reader manuscript/PDFは未検査。
- 新worklogは`run_drafting_synthesis_v2_agent.py`で7 packages＋synthesis PASS、約4時間と報告する。実使用callerの補強Evidenceと費用上の信号だが、全role総費用の支配性やcache優位を証明しない。次の費用記録でruntimeも確認する。

`execution/index.md`の80件/SELECTED 1/Architecture pendingという古い案内をcurrent stateとしない。現行Selectionは409件/SELECTED 41/HOLD 368。Stateやcheckpointの名指し先を辿る。indexの修正/自動生成を新主経路にするだけの費用Evidenceはない。

今後current detailが判断を変える場合だけ、対象refと関係差分をread-onlyで確認する。固定snapshotを最新とみなさない。

## 5. 次の入口・未実証・停止条件

次の最小作業は判断書§5。まだ答えを作っていない3–4候補を一つのWeekly reader questionで選び、source/時点/品質条件/費用記録を**出力前**に固定する。paperとproductの異なる主張、強い未選択/未解決の対照を含める。全号/全Profileに広げない。採用/HOLDを事前の正答として割り当てない。

非著者reviewとrole別usageの取得方法は実行前に確認する。自分の再読を新candidateの独立reviewに数えず、取得できない値はunknown。Humanを追加reviewerや計測係へ無償で割り当てない。本sessionでは別agentへの委任・外部送信は行っていない。本handoffはそれらの包括的な実行許可でもない。

未実証: Aのpublication品質、omission reviewの十分性、all-role費用、未知sourceでの再現、repair完了、Specialの一般性、全歴史互換、ROI。今回の反例の存在から率や総額を推計しない。

品質条件を満たせないなら問い/source/表現/reviewを見直す。完了できても消えた仕事がなければ対案の拡張/計測基盤投資を止める。純削減が見えれば他Profile/失敗条件で反証する。runtime支配等の実測が出れば保留領域を再評価してよい。

このsessionは比較の前提を変えるEvidenceが得られた判断面で区切った。Phase 4全体の完了、外部要因によるblocked、Humanの追加採用判断待ちではない。続行指示では旧decision-only承認手順を再演しない。

## 6. 権限

production `eariver/japanese-generative-ai-survey`はread-only。上記findingはreconstructの調査資料のみで、productionのreview/State/Gate/adoption/migrationを変更していない。新たなproduction mutationは明示的なHuman authorizationが必要。通常Git Pull/Pushと最終commitはHumanが行う。
