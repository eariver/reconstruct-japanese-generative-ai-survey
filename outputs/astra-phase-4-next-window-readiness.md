# Phase 4-A後 — 次の5時間枠の開始条件

日付: 2026-09-12 JST  
状態: **PREPARATION COMPLETE / MAIN TRIAL NOT STARTED / NO PRODUCTION ADOPTION**

## 1. 残り枠での判断

**主比較のsource選定・意味生成は次の枠へ残す。** Phase 4-Aの[比較基準](astra-phase-4-comparison-basis.md)を継承し、この残り枠では試験の成立条件と結論の範囲を整理した。新しいsource、candidate、本文、独立review、repairは作っていない。単なる開始を進捗として数えない。

次に必要なのは、source読解から採否・短い本文・非著者review・修復/再reviewまでがつながった観測である。今、既知CASの修正版だけを作っても未知source品質や総作業量の判断は増えない。一方、以下の3点を曖昧にしたまま次枠を始めると、完走しても判定できない。

1. **A単独の完了は費用優位を示さない。** 最初の試験はAの成立性と仕事の所在を知る観測。対案と同条件の実測を得るまでは削減量・ROIを計算しない。旧Bのowner明示だけの部分は引き続きAへ吸収する。
2. **小sliceの研究・編集完了とproduction全工程完了を分ける。** 全号Discovery、admission、Human Gates、PDF/visual QA、Freeze/Release、歴史互換を省くことは、同等保証や総費用削減の証明にならない。
3. **canonicalに出せる機械補助でも意味評価の代用にはならない。** 次の試験では本文の根拠対応・coverageを誰が判断するかを明示し、補助が埋めた欄をreview済みと数えない。

この判断に新しいremote状況は必要なかったため、productionの再crawlはしていない。Phase 4-A末尾のW34 `DRAFT_COMPLETE`観測はその時点のEvidenceのまま。残りusageや次枠の処理能力を実測したわけではなく、5時間枠を300分の連続実行保証とは解釈しない。

## 2. 共通機械補助について確認できた具体的な注意点

Phase 4-Aが取得済みのmain `005e59841272464307386abfc11f5b09228f0814`に限って、[interactive Drafting runner][runner]の§相当の関数を静的に確認した。今回、runnerの実行・変更はしていない。取得bytesのidentityは[既存manifest](../notes/phase-4/basis.json)で確認できる。

| 固定コードの箇所 | 観測 | 次の試験での扱い |
|---|---|---|
| `_ref_rows`、95–106行 | CLAIMS/CLAIMS_AND_LIMITATIONSでclaims全件、claimsがなければeventsを列挙。LIMITATIONS系でlimitationsを列挙。metricsの列挙経路はない | full canonicalのMETRIC表現能力と、このcompact helperの入力能力を同一視しない。数値を書くなら必要なsubject/contextを持つ正確なcanonical参照を扱える経路を選ぶ |
| `_draft_result`、186行 | 各must-coverに全content block IDを対応させる | 対応欄の存在を意味的coverage PASSに換算しない。authorが内容との対応を判断し、非著者が検証する仕事を計上する |
| 同、172–187行 | package boundariesの結合文とboundary blockを作り、各boundaryをEXPLICITLY_STATEDとする | 読者に必要な制約の説明、帰属、自然な本文への統合を達成したとはみなさない |

一方、[canonical Drafting prompt][prompt]はEVENT/CLAIM/METRIC/LIMITATIONのstable IDとsubjectを保持し、must-coverのblock対応とboundary handlingを求める。**Core全体が表現できないという発見ではなく、次の比較で便利な入力経路を無検討に選ばないための確認**である。これだけを理由にwrapper改修や新しいauthoring engineは開始しない。

最小の方針は、既存canonical表現を使い、identity/hash/参照の機械処理と意味判断を区別すること。小試験に足りない機械補助が分かった場合は、新規source出力を作る前に校正用入力で接続を確認する。必要な小修正の準備費も数え、補助実装だけで枠を消費しそうなら意味生成は始めない。Phase 3の古い受理実験を再開条件として丸ごと再実行しない。

## 3. 次枠の作業単位

**初期単位:** 一つのWeekly reader question、原則3候補、短い一つの日本語本文と全候補の採否。4候補目は、独立した反例を含めないと判断できない場合だけ出力前に追加する。件数は実行範囲の上限目安であり、品質や採用数の目標ではない。

Phase 4-A §5のpaper・product/実装の一次source・未選択/未解決になり得る対照という選び方を維持する。比較可能なsource群がなければ、同じ週の無関係な材料を強引に束ねずreader questionを見直す。採用/HOLDの正答を事前に決めない。Phase 3/4-Aで既に読んだpaperと4件の標本は未知source試験から除く。

この単位の完了に必要なもの:

- version/取得bytes/時点が追跡できるsourceとProfile上の問い。
- Taskの問い、canonical Card/View、全slice候補の採否理由、packageのpurpose/must-cover/boundaries。
- 上記に依拠する短い読者本文。数値/比較・帰属・不確実性・読者価値が必要十分に表れること。長さは品質点数にしない。
- sourceとProfileから始めた非著者のfinding、対応する修復または根拠付き不採用、修正対象版の再review。
- 役割別の作業記録、未解決finding、実行していない工程と費用、次の判断。

これは**研究・編集sliceの完了**であり、publication全体の品質非劣化やproduction接続を証明する完了ではない。新しい試験ID/候補領域をreconstructに作り、schema等の機械検査とproduction admissionを区別して記録する。production State、Human approval、accepted Taskを複製して新しい意味出力が承認済みであるかのように見せない。入力に正式なbindingが必要なら新しいlab候補として生成し、旧approvalの借用やhashの手入力で通さない。

## 4. 意味生成の前に揃えるもの

以下は実験の成立条件であって、新たなHuman Gateではない。次枠のAstraが条件を確認して進める。今回、許可や入力をHumanへ追加要求してはいない。

| 条件 | 次枠で確定する内容 | 現状 |
|---|---|---|
| 研究範囲 | reader question、読者目的、Weekly window/cutoff、対象lane、carry-over等の関連性、slice外の未評価範囲 | 選定ルールあり。具体source/期間は未選定 |
| source固定 | URL/version、Raw bytes/hash、取得時刻、原文/抽出の別、読めない部分、必要な比較条件・反例 | 未取得。今は答えの先行生成をしていない |
| 出力経路 | Card/View等の既存contract、正確な参照を扱う機械補助、どの機械検査を走らせるか | 表現能力の歴史Evidenceあり。次試験の最小接続は未確認。§2のcompact helper上の注意あり |
| 非著者review | evaluator、アクセス可能なsource、対象版、source-firstの順序、review記録と再review方法 | 未配置・未実施。自己再読では代替不可 |
| 費用記録 | 役割/行動/入出力/実行理由、使えるusageログと計測粒度、unknownの範囲 | 項目は定義済み。実環境のログ取得方法は未確認 |
| 完了の余力 | source調査/生成だけでなくreview、少なくとも修復と再reviewに対応する余力を残せる範囲 | 次枠開始時に判断。一定時間で成功すると仮定しない |

非著者は、検査対象の意味判断・本文・修正版のauthorと区別する。productionの監督役がexecutorから独立していることと、その監督役自身の編集判断に対して非著者reviewが行われることは別である。モデル名や新しいsession名だけで独立性を判定しない。reviewerが修正文を直接書けば、その部分の再reviewを自己評価と数えない。これは試験結果の独立性の条件であり、productionへ恒久的な第三review roleを追加する提案ではない。

必要な委任・別taskへの送信は、その時点の実行権限と利用可能な経路に従う。本書はsubagent起動や外部送信の許可を新設しない。非著者の経路がまだ成立しない場合、入力準備までは可能だが、この一往復が同枠で完結できると見込まず、主試験の意味生成は保留する。Humanへreview作業を自動的に割り当てない。

source-first reviewはcandidateの自己申告に評価項目を限定しない。reviewerはsourceと読者目的から必要内容/強い反例を記録してからcandidateを見る。本文にないsource固有の制約や、強い未選択候補も確認対象にする。全sourceを別途再読した費用を共通費として隠さない。

## 5. 最小の費用記録と判定点

恒久telemetryや空の台帳群を今は作らない。次試験で既存ログから取れる値を、一つの作業記録へ次の列で対応付ければよい。

`役割 / 行動・理由 / 入力版→出力版 / source参照・再読・handoff / finding・修復先 / 実測active time / wall time・待ち / 実測usageと取得元 / 未計測・省略工程`

時間が区切れるときだけactive timeを記録する。tool待ちをactive workと混ぜず、重なったwall timeを足さない。usageは利用可能なログの範囲・集計単位を記す。各turnが複数役割を兼ねる場合、厳密に分離できないtokenを便宜的に按分しない。全体usageだけ取れるなら全体値と役割別unknownを併記する。本文文字数、ファイルbytes、5時間枠の消費率をtoken/料金/実働時間へ換算しない。

scope設定、source選定、補助の準備、独立review、修復、再開・説明も仕事である。今回の設計整理は準備費に属するが、役割別usage/active timeを取得したとは扱わない。小sliceで未実行の全号coverage、admission、CI/audit、PDF/visual QA、Gates、運用保守は「0」ではなく未評価とする。W34の約4時間というworklog値は照合対象であり、新試験の実測値や比例外挿の係数には使わない。

| 観測された終了状態 | 判断できること / 次の扱い |
|---|---|
| 全sliceのsource→本文→review→修復が完了し、重大なunsupported claim/omission等が解消 | この範囲でAを遂行できた。誰に何の仕事が残るかを特定。単独実行なので費用優位は未判定 |
| 問い/読解/採否/本文に重大な欠陥が残る | Aのこの実行は品質条件未達。安さで相殺しない。共通の問い/source/表現/reviewの不足を先に見直す |
| 品質は満たすが仕事の削減候補を特定できない | 新しい層や比較armを惰性で作らない。このsource範囲ではarchitecture投資の信号不足 |
| 意味再構成が反復し、具体的に外せる作業が見つかる | 同じrole/表現/補助/reviewで仕事の順序・単位を変える対案を一つ定義。未知sourceで同条件比較し、双方の準備/修復/再reviewも含める |
| runtime/機械補助の準備が支配して一往復を始められない | 準備障害そのものを記録。安全検査を省略して速い成功を作らず、限定的な接続設計を再評価 |
| 時間/usageが尽き、reviewまたは修復が未完 | 不合格確定とも成功ともせず、未完・既消費費用・対象版・次の一手を保存。弱い出力へscopeを後付け縮小して完了扱いにしない |

A単独で有望でも、paired比較なしに「減った仕事」と呼ばない。比較はsource、Profile、品質条件、補助、review条件を揃え、Aの答えを見た後に同じauthorがBを作る順序効果を避ける。異なるsourceだけの差をarchitectureの効果にしない。全roleの純削減が確認できた後に、Specialの系譜・時点・歴史という異なるfailureへ進む。

## 6. 今枠の終点と次の入口

今枠で判断可能になったのは、**次にA単独の小試験を行う目的は成立性/仕事の所在の確認であり、全体の費用優位判定ではないこと、その試験の前に正確なcanonical接続と非著者reviewを準備する必要があること**。compact Drafting helperの既存挙動をそのまま意味品質の評価に使わないことも固定した。

次枠は本書§4の未確定項目を必要範囲だけ確認し、§3の一単位を完了できる構成にしてからsource/条件を固定する。これは旧decision-only承認手順の再演ではない。準備のために残り枠で新規sourceを先に読んで答えを持ち越すこともしていない。

Phase 4-Aの主判断と安全/権限境界は変更しない。production mutation、adoption/migration、State/Gates/Freeze/Releaseの変更、PR/Issue送信、Pull/Push/commitは未実施。次のHuman継続指示で再開するためにdurableを整え、この枠の作業を停止する。

[runner]: https://github.com/eariver/japanese-generative-ai-survey/blob/005e59841272464307386abfc11f5b09228f0814/scripts/run_drafting_synthesis_v2_interactive.py#L95
[prompt]: https://github.com/eariver/japanese-generative-ai-survey/blob/005e59841272464307386abfc11f5b09228f0814/config/prompts/article-drafting-v2.md
