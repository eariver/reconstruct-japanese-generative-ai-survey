# Re:Phase 1 — current productionからの再baselineと再構築方針

日付: 2026-09-15 JST  
状態: **方針再評価完了 / 次の限定設計を選定 / production未変更・未採用**

## 1. 結論

**同じreconstruct repositoryを継続し、旧Phaseを論理的にArchiveする。production `774dd39a`を新しい比較基準として、通常運用に必要な契約・入口・成果物の責任を整理し、既存の仕事を実際に外せる単位で再構築する。** 旧Phase 5の「Freeze修復、次にreader修復」という順序は、今後のreconstructionの既定工程から外す。

目標は、良いWeekly/Specialを、調査・著述・独立review・修復・実行・保守・Human判断まで含めて少ない仕事で作れること。旧案を完成させることでも、productionの全bugをreconstructで直すことでもない。

選ぶ方向は**current Coreを暫定的に利用する部分再設計**である。既存の意味表現・承認・履歴を利用し、通常入口に重複している現在状態の説明、運用に不要な過去経緯、意味を落とす変換や手作業の再組立てを順に減らす。Core、schema、role配置、review配置、監査方法を永久固定する判断ではない。今すぐ全面置換するだけの便益・移行根拠はまだない。

**次の一単位には「currentな運用契約と現在状態表示の分離・統合案」を選ぶ。** 根拠は、現在も必読のauthority/bootstrapとedition indexに、機械Stateと矛盾するcurrent説明が実在し、その解決を利用者へ要求していること。新しい要約文書を追加するだけでは合格にしない。既存のどのcurrent記述・必読義務・更新作業を外すかを対にした差分を作る。§7で対象と終了条件を固定する。

これは方針の選定であり、効率改善や採用の実証ではない。今回、次単位の実装、production運用、独立agent review、A/B試験は実行していない。

## 2. 基準と確認範囲

| 基準 | 固定値と確認 |
|---|---|
| reconstruct | `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`。開始HEADは一致、working treeはclean。GitHub mainもGETで一致確認 |
| production | `774dd39a951c9ac3818e83dfffd4c7666efb0a20`。GitHub mainをGETで確認し、以後このcommitのtree/blobを使用 |
| 新規の観測 | 2026-09-14 17:05 UTC以降。切れのないtree listingと選択ファイルのGit blob SHA-1/raw SHA-256を保存 |
| local production checkout | HEADは旧`f9f3e040`で、開始時に12 pathの削除表示があった。調査基準に使わず、復旧・更新もしない |

今回の一次資料は、current config、authority/bootstrap/governance/audit規則、関係するhelper/publisher/validator、W34修復記録とindex、W33/W34/SP001のState等である。[取得manifestと観測](../notes/rephase-1/evidence.json)、[方法と範囲](../notes/rephase-1/README.md)を参照。旧入力cacheはcurrent treeのblob hashと一致するものだけ再利用した。

旧reconstructについてはmission、直前handoff/assessment、Phase 3-G/5-A、関係する旧判断を選択読解した。全chat、全失敗史、全source本文、全Coreは再読していない。旧Phaseを捨てて同じ調査をやり直すことには情報価値が低い。

## 3. 現在のproductionをどう評価するか

### 3.1 すでに存在する有用な構造

current configは11 lifecycle states、二つの通常Human Gate、3 research Profilesと2 publication Profilesを持つ。10 stageすべてで`handoff_required=false`、direct local CLIを優先し、connector用bridgeは同じ機械処理の実行手段である。したがって「stageごとに別agentへ渡す工場」を現方式と仮定して比較しない。[config][config]

governanceには継続する監督責任、独立Discovery探索、captured-but-unconsumedの点検、強い未選択候補のreview、適応的gap fill、Selection/Architectureの最終判断、publicationのsemantic/visual reviewが既にある。まとめて調べることやreview責任を置くこと自体は新案の便益ではない。保存Taskの数と認知作業の数も同一ではない。[governance][governance]

W33/W34/SP001の保存Stateは、いずれも`RELEASED / next_action=null / COMPLETE`である。W34はHuman Preview修復とr3承認を経た実績を持つ。一方、これらの成果は旧Coreやedition-local修復を含む履歴であり、**current Coreから新号を通常経路だけで完走できる証明ではない**。今回、State依存閉包・公開asset・PDF・全号品質を再検証していない。[W34 State][w34-state]、[W34 Freeze記録][w34-freeze]

### 3.2 旧問題の一部は上流で解消されている

| 項目 | 今回の扱い |
|---|---|
| 書誌access日をcutoffで作る原因 | #492のprovenance helperをcurrent sourceで確認。旧W34修復一周を、そのまま今後の反復費へ外挿しない |
| Releaseの必須CORE report欠落 | #495はreport生成とdual reviewを実装。旧候補の該当実装を再び作らない |
| pre-TeX reader reviewの入口 | #496はstructured inputとpersisted semantic reviewを実装。「新規gate導入」を再構築の新機能として数えない |
| 全profile通常実行・retry | 上記実装やPRのPASS記述だけで成立認定しない。Releaseの時刻差再呼出し等は旧候補と異なる |

[Release helper][release-helper]、[Weekly publisher][weekly-publisher]、[PR #495](https://github.com/eariver/japanese-generative-ai-survey/pull/495)、[PR #496](https://github.com/eariver/japanese-generative-ai-survey/pull/496)。PR記載の試験結果は上流の報告であり、今回の再実行結果ではない。上流の改善をreconstructの採用・純削減として計上しない。

### 3.3 currentな契約と現在状態の説明が混在している

同じ`774dd39a`内で、次の記述が共存する。

| 場所 | 保存されている記述 | 判断への意味 |
|---|---|---|
| authority index冒頭 | current main=`005e5984`、#488=`draft/open/unmerged` | currentの事実を規範文書に埋め込み、現実照合を毎回必要にする |
| redesign authority / feedback backlog | bridge repair candidate、reaudit pending等の旧状態 | 歴史経緯と有効な規則を読者が分離する必要がある |
| W34 execution index | `ARCHITECTURE_ESTABLISHED / ARCHITECTURE_REVIEW` | current Stateの`RELEASED`と一致しない。index自体はStateがauthorityだと明記している |
| session bootstrap | authority/overlay、bootstrap、governance、checklist等を開始・再開時に読む要求 | 現在状態の矛盾は単なる奥の古文書ではなく、通常入口に接続されている |

[authority][authority]、[overlay][overlay]、[execution index][w34-index]、[bootstrap][bootstrap]。これは今回sourceで確認した不一致であり、誤ったState遷移が実際に起きたという主張ではない。precedence規則は誤採用を避ける助けになるが、照合作業を不要にはしない。全sessionの再読量や費用は不明。

この種の不一致は旧Phase Aでも指摘されていた。今回の判断根拠は新発見であることではなく、上流の機能修復が進んだ現在でも通常入口に残り、具体的な除去対象を示せることである。

さらにconfigの`contract_files.pipeline`にはauthority/overlay/過去audit文書が含まれ、Core final auditは全候補変更後の固定SHAで七観点をゼロから確認し、candidate tree変更で全PASSを失効させる。**正しい対象への承認**と、**あらゆる変更で全監査仕事を作り直すこと**は設計上分けて評価できる。ただし現規則は有効であり、今回緩和していない。文書整理も契約変更・移行・監査費を伴う。[audit rule][audit]

### 3.4 品質と実装適合には別の残差がある

W34 r2では、review対象へのbindingが正しくてもHumanが内部編集語彙と書誌日付の問題を発見し、修復・build・review記録・Candidate・Previewを作り直した。既存reviewの有効な適用が必要であり、hash、check ID、reviewer欄の追加だけで品質を認定できない。[実修復記録][w34-repair]。独立監督がこのexact版を消費したことは旧調査の限定資料では示されなかったが、他所でreviewがなかったとは断定しない。

同じproduction基準の[既存probe](../notes/phase-5-upstream-reconciliation/probe-results.json)は、Freezeのartifact集合/approval型の不整合、reader gateと現在TeXの導出結合不足、frontmatter等のprojection漏れ、audit-only fieldでの停止を示す。今回current treeとその固定入力の一致を確認し、関係sourceを再読した。probeは再実行していない。関数/schema反例であり、全stageや最終Human Gateの突破、全号の品質不良ではない。

この二種類を混ぜない。実装の不整合は修復できるが、それだけで意味品質・通常運用費の改善を説明し終えたことにはならない。

## 4. 旧reconstructionの判断をどう変えるか

| 旧成果・前提 | Re:Phase 1の処遇 |
|---|---|
| missionと全roleのlifecycle評価 | 再採用する。現在の目的に直接合致するためであり、旧Phaseの権威だからではない |
| canonical表現の適合性、旧反例、修復・review記録 | 固定版のEvidenceとして保持。currentへの適用は入力・契約・caller差を確認する |
| A+、継続editor、意味再構成削減仮説 | 候補/仮説へ戻す。既存方式との実質差なしに優位としない |
| Phase 5-Bの非支持・識別不能 | その範囲で保持。認知的重複ゼロ、別設計一般の無価値とはしない |
| Freeze→readerの固定順序 | 撤回。運用で必要になる修復backlogへ移す。全体設計の開始条件にしない |
| 旧runtime patch | 歴史的候補。current-readyではなく、必要な反例/限定差分の再利用元 |
| 特定の再構成例が見つかるまでarchitecture投資を止める条件 | 全体への拘束を解除。運用契約、遅い発見、移行・保守増幅からも投資を選べる |
| cache/staging/新store/外部engine等 | 自動再開もしなければ永久禁止もしない。具体的な除去対象・保証・導入費を示せる時に再評価 |
| 旧Phaseを順番に閉じること | 今後の完了条件から削除。旧未完工程を消化する義務はない |

reconstruction自身にも、局所的な反例→追加条件→次の局所修復という進行が蓄積し、全体便益を示せないままcurrent引き継ぎが長くなる問題があった。安全性検証の価値は残るが、**次の欠陥が見つかったことを、次の投資の十分な理由にしない**。旧成果の総費用もunknownであり、失敗・浪費と一括認定はしない。

## 5. 再baselineとworkspaceの選択

| 選択肢 | 利点 | 主な追加費・問題 | 判断 |
|---|---|---|---|
| 旧Phase 5を続行 | 既知の小さな修復をすぐ進められる | 改善全体の目的が保守backlog消化へ置換される | 既定方針にはしない |
| 同repoで論理Archive＋current再baseline | 履歴リンク/反例を保ち、active入口だけ更新できる | 新旧の位置付けを明示する必要 | **採用する調査方針** |
| 全成果を物理移設し、新workspaceにcurrentを丸ごとcopy | 見た目の分離が強い | 相対参照・probeのpath・再現手順の修復、取得・二重保守、調査のやり直し | 今は選ばない |
| Coreを含む全面置換 | 契約と状態モデルを根本整理できる余地 | 意味品質を自動では改善せず、承認・歴史・Profile・transportの再実装/移行が大きい | 現時点で優先しない |

ここでの再baselineは、**比較の起点と有効な調査方針を更新すること**である。current productionを正解・全品質PASS・費用最適と認定したり、旧accepted artifactをcurrent schemaで書き直したりすることではない。

実施する整理はREADME、root AGENTS、Re:Phase 1 handoffから新判断へ入る形にするだけ。旧outputs/notes/handoff/brief/instructions/候補patchは移動・上書きしない。旧入口に書かれた「current」「next」は、その歴史時点の記述として読む。過去のroot入口は`ec6a502e`でも復元できる。

次の候補を実装する時だけ、必要なcurrent sourceを独立した隔離Git rootに置く。上流checkoutを更新せず、全production archiveを常設shadowとして複製する必要もない。

## 6. 目指す構成と、減らす仕事

暫定構成は次の四つの責任から成る。新serviceや新agentを四つ作る意味ではない。

| 責任 | 保持する内容 | 簡素化する方向 |
|---|---|---|
| 有効な運用契約と現在表示 | 権限、入力/停止条件、Profile差、正式State/approval参照 | 安定した規則と変動する事実を分離。current factsを手書きの複数正本にしない |
| 研究・編集判断 | source/version/比較条件、採否・未選択理由、問いと読者説明 | 既存canonicalの意味を落とさず補助。機械field/参照/転記を毎回著述させない |
| 機械実行とpublication導出 | 検証、binding、render、invalidation、exact Candidate/Freeze/Release | 一つの入力責任から既存成果物へ導出。局所driver/重複writerは実使用を確認して外す |
| 独立reviewとHuman判断 | source/omission/意味/visualの点検、明示Human approval | 同じreviewの有効な適用を明確にし、誤りを早く見つける。PASS記録の増設を成果にしない |

通常の流れは、target/Profile→current authority解決→調査と独立確認→採否・構成→Human Architecture→読者原稿と早期review→renderとexact出力review→Human Preview→Freeze/Releaseとする。現方式と共通する部分が多く、流れ図の違い自体に便益はない。

| 具体的な除去候補 | 残す保証・費用 | 優先の考え方 |
|---|---|---|
| 規範文書/indexのcurrent SHA・statusを手書きで合わせる仕事 | 元のState/commit/approval、時点、未確認表示。規則自体は人が明示しreview | 最初に設計する。currentで不一致が直接確認できる |
| 機械参照の探索・手製driver・意味を落とす中間変換 | exact basis、入力完全性、source固有の意味、既存caller/歴史互換 | actual callerを限定して次点。helperの`metrics=[]`等の静的縮約を、全production利用実績としない |
| 遅いreader defect発見による追加周回 | 実source/semantic review、導出結合、post-transform確認、exact PDF review | current #496を基準に評価。早期reviewを足しただけで後段仕事が消えたとはしない |
| currentを説明するための過去audit経緯の反復読解 | 検証対象への承認、根拠の参照可能性、履歴 | 開始入口からの除去を設計。意味ある規則を単なる古文書と誤分類しない |
| 全変更での再監査/広い再計算 | 変更影響閉包、trust/authority/歴史の拒否能力 | 影響が説明できる変更で別途比較。今はaudit免除やcache実装へ広げない |

二つの通常Human Gate、独立性、exact bytes、historical verificationは当面保持する。11 state、7 workflow、特定model/人数、すべての現在のfile/schemaを目的上の不変条件とはしない。ただしproductionの有効な契約を変える提案には、守っていた保証をどこへ移すかとHumanの明示採用が必要である。

## 7. 次の一単位と、その後の分岐

### 7.1 最初に作るもの

**reconstruct-onlyで、通常開始・再開用の運用契約整理案と現在状態表示の一例を作る。** 完全な新manual、全Core wrapper、恒久telemetryは作らない。

対象はcurrentのauthority index、redesign overlay、session bootstrap、W34 execution indexの重複current記述と読込関係。governance、Profile/Human Gate、transport trust等の義務は、重複していることと不要であることを区別する。

review可能な完成物は、短い契約案に加え次の対応表/差分で足りる。

1. 各現行義務を「維持する唯一の規定位置／必要時だけ参照する詳細／歴史へ移す状態説明」に対応させる。どこにも移らない義務があれば未完。
2. live factsは`commit + Profile + State + typed checkpoint/approval pointers`から表示し、規則や承認を生成しない。欠落・drift・未確認はそのまま示し、`latest`探索や成功推測で埋めない。
3. currentと提案のstart/resumeで読むもの・手で更新するものを比較し、外す記述を具体的に列挙する。新viewだけ足して既存必読/手書きを残す案は不合格。
4. current W34の`RELEASED`、旧indexのArchitecture待ち、Human REQUEST_CHANGES後の再開、SpecialのProfile差を限定例にする。W34は保存事実、修正例は明示したfixtureとして混同しない。文書/表示の検証を全workflow PASSとしない。
5. 文書がcontract hashや監査対象である点を含め、将来の移行差分と残す歴史versionを記す。まだproductionの読み方を切り替えない。

**終了条件:** 現在状態の二重記述と、そのための照合・手書き更新を少なくとも一箇所、必要保証を残して外せる具体案が成立すること。読みやすい要約が一枚増えるだけ、あるいは人が毎回viewを修復するだけならこの案への追加投資を止める。時間/token削減率は、この設計単位だけでは主張しない。

選定理由は低影響だからというだけではない。currentの誤誘導を直接減らし、以降の全設計・運用がどの義務と状態を使うかを明瞭にする共通の入口だからである。支配的コストだと測定したわけではなく、**現在の不確実性の下で、除去対象が明確で撤回しやすい初期投資**として選ぶ。

### 7.2 既知修復とarchitecture検証を混ぜない

Freezeの二残差とreaderのbinding/coverage/audit-scopeは、[既存の限定Evidence](../notes/phase-5-upstream-reconciliation/README.md)を修復backlogとして保持する。修復が必要な通常経路を実行・提案する時は、その経路の前提として直す。既知欠陥を残した悪い対照で新案を勝たせない。

順序は目的依存にする。readerの早期品質・手戻りを検証するならreader側が先、Freeze実行を通すならtyped approval/artifact修復が先でよい。運用契約の整理をするためにFreeze/Release全chainを完成させる必要はない。旧patch一括移植はどちらにも使わない。

次の候補では、その都度 **currentの具体的な仕事→提案で外す仕事→残る保証→増える準備/保守費→必要な検証** を一組にする。source生成品質はsource-backedな非著者review、writer変更は実入力の意味保持とauthority negatives、運用入口は同じ再開条件での誤誘導/欠落/更新作業、audit方式は変更影響と歴史/trust negativesで評価する。全候補に同じ大きなA/Bを課さない。

### 7.3 採用と全体完了への道筋

成立した単位だけをcurrent差分にし、対象・検証・除去する旧経路・切戻し・残る費用を揃えて独立reviewとHumanの採用判断へ進める。実運用はその権限が得られた後に行う。ここでの方針判断は独立review済みではない。

初回導入後は、実際の対象edition/変更で研究、review、修復、CI、Human、保守への仕事移動を確認する。取れる時間/usageは既存記録から取り、取れないものはunknownとする。全role計測環境を作ることやfull canonical baselineを完成させることを、あらゆる設計検討の前提にはしない。一方、未実行工程をゼロにして純削減を認定しない。

実際に旧作業を外せず準備/review/Human負担を増やすなら撤回する。安定した意味経路でもCore変更・再開・全監査の負担が反復して支配的と示されれば、Core分割・置換やOSS再利用へ進む。具体的な置換責任がまだ定まらない今、外部frameworkの網羅比較はしない。

全体の成功は、通常経路でWeeklyと必要なSpecialを作り、同等以上の品質・provenance・Human authorityを保持し、初期投資・移行・二重保守を含む仕事が許容範囲で減り、旧通常経路を実際に廃止できた時に判断する。今回その成功は未達である。

## 8. 今回の終了境界

Re:Phase 1の方針再評価はここで完了する。比較基準、旧成果の処遇、暫定構成、最初の除去対象、検証/採用の道筋を選べたためであり、次の実装まで自動で進めない。

今回行ったのはGETとsource/記録の読解、hash照合、reconstruct文書/入口の更新。production変更・投稿・dispatch、Pull/Push、最終commit、追加agent、試験の再実行は行っていない。full quality、cold-startの全Profile成立、全caller/歴史互換、純費用削減は未実証。旧Human approvalや旧独立review許可を新しい権限として使わない。

次の入口は[Re:Phase 1 handoff](../handoff/rephase-1-continuation.md)。旧Phase番号・旧commit title・古い「next」記述は今後の工程を決めない。

[config]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/config/survey-production-v2.json
[governance]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/docs/survey-production-core-v2-sol-luna-review-governance.md
[authority]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/docs/survey-production-core-v2-authority.md
[overlay]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/docs/survey-production-core-v2-redesign-authority.md
[bootstrap]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/docs/survey-production-core-v2-session-bootstrap.md
[audit]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/docs/survey-production-core-v2-final-audit-rule.md
[w34-index]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/execution/index.md
[w34-state]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/production-state.json
[w34-freeze]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/execution/luna/w34-freeze/session-worklog.md
[w34-repair]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/session-worklog.md
[release-helper]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/scripts/survey_release_checkpoint_v2.py
[weekly-publisher]: https://github.com/eariver/japanese-generative-ai-survey/blob/774dd39a951c9ac3818e83dfffd4c7666efb0a20/scripts/survey_weekly_semantic_publication_v2.py
