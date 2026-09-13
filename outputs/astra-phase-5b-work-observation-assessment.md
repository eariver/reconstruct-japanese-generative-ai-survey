# Phase 5-B — 一つの問いの作業観測と停止判断

日付: 2026-09-13 JST  
状態: **BOUNDED CHAIN COMPLETE AFTER REPAIR / NO SUPPORTED REMOVABLE RECONSTRUCTION CASE / PARTIAL NON-IDENTIFIABILITY / NO 5-C TRIAL OR ADOPTION**

## 1. 判断

**Phase 5-Bを、独立review→修復→再reviewまでの一往復で閉じる。5-CのA/B比較は開始しない。** 限定された候補記録・採否・読者本文のblocking defectは修復できた。一方、「同じ比較条件を候補別調査と後段編集で組み立て直す仕事を、一度の検証にまとめて除く」という5-Aの仮説を支持する具体例は、このchainでは確認できなかった。

これは反復ゼロの測定でも、全productionにその仕事が存在しないという否定でもない。raw表等への再訪は実在するが、各時点の結論の完成度・再確認の内訳・除去可能量は識別不能だった。役割別active time/token/料金もunknownである。**非支持と識別限界を両方残す**。

5-Aの停止条件は「支持例がなければ今回の比較投資を止める」として適用する。「観測できなかったので一般仮説が棄却された」へ強めない。新しいauthoring標本を次々と追加してBを探したり、欠けた観測を埋めるための恒久telemetryを作ったりはしない。

## 2. 基準と、5-Aから修正した入口

開始時のreconstruct local HEADとremote mainは、Push済み`cc530fea883a66049b8ab4a9ea3f112da34c4fab`で一致し、working treeはclean。5-Aの変更はこの基準に取り込まれている。Pull/checkout/commitで状態を変えず引き継いだ。[5-A判断](astra-phase-5a-work-unit-decision.md)は歴史判断として保持する。

5-Bの前提は次の三点だけ更新した。

1. **current production baselineをPR #490後へ更新。** 研究・編集Taskの単位は変わらず、主仮説を置き換えるEvidenceにはならなかった。実W34の用語修復は、自然な日本語と読者への説明を共通品質条件に含める具体的な根拠とした。
2. **A-MEMの版を出力前にv1→v5へ変更。** metadataでcutoff前v5を発見したため。旧版を弱い対照へ使わない。v1 rawは準備履歴として保ち、主本文の根拠から外した。
3. **非著者reviewer一体を今回のHuman明示許可で起動。** source事前評価、初稿review、root修復後の再reviewだけ。旧4-C許可を流用せず、追加委任/本文代筆/production操作はしていない。一度の再reviewまで完了したので、この許可を将来の一般的委任へ拡張しない。

全体目的は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準以上に保ち、production・supervisory review/reasoning・repair/regeneration・CI/runtime・LLM・complexity・Human handoff/manual burdenを含むtotal lifecycle workを最小化すること。移転は削減にせず、初期/移行/二重保守/歴史利用費も含める。この目的は未達である。

## 3. 実行した単位

[出力前protocol](../notes/phase-5b/protocol.md)に従い、問いは「長期会話LLMエージェントの外部メモリについて、Mem0の報告から品質と処理負担の何が分かり、他方式との比較・導入判断にはどの条件確認が残るか」とした。Weekly窓は2025-04-28 00:00〜05-05 00:00 UTC未満。

| 候補・固定版 | source消費と採否 | 維持した限定 |
|---|---|---|
| Mem0 `2504.19413v1` | 窓内の主題。方法、LOCOMO評価、品質・応答負担、原表/脚注/判定promptを確認 | 著者報告。全contextの方がJが高い。query時のtoken/latencyは総運用費ではない。exact judge版は未確定 |
| A-MEM `2502.12110v5` | cutoff前の背景比較。note/link/evolution、指標/質問集合/検索k、著者固有の限界を確認 | 新規の今週発表ではない。Mem0引用表と原表のmulti-hop/temporal対応が不一致。原報告と再実行を混ぜず直接比較を保留 |
| MemOS `2507.03724v1` | 同じ問題への強い関連候補として方法/評価/latency/KV実験を確認しHOLD | cutoff後。後日結果を当時の本文へ入れない。latency本文/表不一致と事前cache条件も研究側へ保持 |

raw HTMLとabs metadataは[source manifest](../notes/phase-5b/source-manifest.json)にURL・版・取得時点・hashを記録し、Gitに残す候補として保存した。6件が主根拠、2件がA-MEM v1の準備履歴。[Evidence index](../notes/phase-5b/README.md)が各入口をまとめる。

sourceはこのsessionで新たに本文を調べたが、モデルの一般的な事前知識を排除したblind sampleではない。選定は目的抽出であり、当時の全Weekly Discovery/negative spaceや全研究分野coverageではない。MemOSはタイトルだけで時点除外せず、source固有の内容を研究側に残した。別sourceを追加する必要はこの一往復では生じなかった。

Card相当の事実・subject/source/metrics/limitations、採否とpackage、本文は既存canonicalの意味分離を使う**lab部分構造**。full schema/Core admissionを通したとせず、架空のHuman approvalやproduction checkpointを作っていない。source集合を読みながら横断比較すること、既存結論を利用することを禁止して対照を遅くする実験でもない。

## 4. 独立reviewと修復の結果

非著者はrootの初稿やreading aidを読まずに[source期待内容](../notes/phase-5b/review/source-expectations.md)を固定。rootは[r1 freeze](../notes/phase-5b/r1-freeze.json)までその内容を読んでいない。rootが研究/編集/本文著述を兼ね、非著者がsource-first評価と独立reviewを担当した。これは現productionの全role配置を再現する比較ではない。

[r1 review](../notes/phase-5b/review/r1-findings.md)はblocking一件、nonblocking三件を出した。rootが原文の必要箇所を再確認し、全て採用して[r2](../notes/phase-5b/r2-freeze.json)を固定した。

| finding | 初稿の不足・原因 | 修復 |
|---|---|---|
| B1 / blocking | 評価規模はfactsに一部あったが本文で不足。Jの寛容な正誤判定条件はfacts/prose双方で薄く、F1/BLEU-1との差も読者に不明瞭 | 10会話・平均規模・質問種別、Jの参照回答/寛容な採点、語彙指標との違いをfacts→must-cover→本文へ反映 |
| N1 | A-MEM v5に初期v1の著者順を適用していた | 固定v5の原著者順へ修正。全著者は元から含まれ、先頭著者は不変 |
| N2 | graph版のoverall差とZep反例は正確だが、graph版自身の不得意な質問種別を明示していなかった | 同一Mem0論文内のsingle/multi-hop Jの逆転をfactsと本文へ追加 |
| N3 | tradeoffの向きが曖昧で、一般技術語の英語が続いた | 品質スコアが低い一方で回答時負担が小さいことを明示。日本語化とp95の説明 |

[独立r2再review](../notes/phase-5b/review/r2-rereview.md)はB1とN1–N3の解消、追加findingなしを確認した。r2の15 files、保持したr1の14 filesのhashも照合した。読者向けの結果は[r2本文](../notes/phase-5b/r2/manuscript.md)。

**source内外の未解決を解消したというPASSではない。** exact judge版、A-MEM表のcategory不一致の原因/正しい割当、再実行commit/全設定/評価集合の同一性は残す。これらを使う順位付けを保留し、その判断を必要としない本文にした。MemOSの後日HOLDも維持。未解決を隠すためにquality scopeを後から縮めたわけではない。

## 5. 仕事の差について分かったこと

[作業記録](../notes/phase-5b/work-record.md)と各freeze時の写しは、意味判断の変更とsource再訪の理由を記録する。完全な操作別時間/認知ログではない。

| 観測された仕事 | 5-Bでの解釈 |
|---|---|
| 別sourceで同名benchmark・異なるcategory/設定を確認 | 異なる入力の初回検証。横断で関係を判断すること自体を重複扱いしない |
| W06/W08のcaption・表見出し・promptへの再訪 | 抽出の未消費部分・疑義の確認として理由は合理的。ただし既存結論の完成度/内訳/除去可能量は識別不能 |
| factsから採否/package/本文へ移る仕事 | source事実を読者目的へ変換する別の編集判断。記録利用はできたが、認知的再構成量は測れていない |
| 独立reviewの原文再読 | 異なるroleの誤り検出責務。rootの読解と重なることだけでは削減候補にならない |
| B1/N1–N3のrepairと再review | 読者説明/版別metadata/表現の修復。正しい既存結論が利用できず再研究したという単一原因にまとめられない |
| JSON/参照/保存版の生成とhash検査 | 機械作業とその準備費。ファイル数を意味判断回数へ換算しない |

今回、**新しい意味層やTask統合なしでも、必要な横断比較を行い、根拠を既存の意味分離で引き継げる限定例**は得た。しかしその同じchainでも読者への説明不足が残り、独立reviewとrepairが必要だった。良い共通authoringの便益を新Bだけへ付け替える根拠はない。

一つのactorが事実/編集/本文を続けて扱い、必要な内容を記録するこの観測では、現productionの別session/別roleのhandoff喪失を十分に励起していない可能性がある。観測を意識したauthoringの影響も排除できない。対照armもない。したがって「rootの一往復が終わった」ことから、productionでどのroleやstageを外せるかは決まらない。

5-Aが期待した情報の一部は得たが、処置の有効性を識別する根拠には足りなかった。この不足を、自己報告による重複件数・短いcommand runtime・大量の引用数で埋めない。

## 6. 全role費用・未実証

実際に発生したのは、引継ぎ/production差分確認、source選定と版修正、取得/抽出補助、原文/表/脚注の読解、facts/編集/本文著述、非著者のsource事前評価/初稿review/再review、repair、freeze/identityチェック、handoffである。bs4不在の二環境確認と一時導入、stdout encoding失敗/出力範囲の修正も準備費へ含む。Humanへの一回の委任確認と回答、usage limit後の再開指示もこの観測のhandoffから外さない。

role別active time/token/料金はunknown。非著者の事前評価には枠中断を含む約3,526秒のwall spanが記録されたが、active timeではない。初稿review/再reviewの時刻や短いtool runtimeも、その単位の記録であってtotal costではない。別roleの仕事を無償としたり、観測費を除いて優位を算出したりしていない。

full Discovery/coverage、full canonical admission/State閉包、Human Gates、全号synthesis/ページ配分、PDF/visual QA、CI、Freeze/Release、Special、歴史caller/repair互換、移行/二重保守は未実行。費用ゼロや同等品質認定に置き換えない。長期の発生頻度Nと一回あたり差も不明で、初期投資の回収時期は出せない。

未実証: 除ける実仕事の差、費用優位/net lifecycle純減、full canonical baseline、全号publication quality、未知source omission全般、Weekly/Special一般性、historical reproducibility全体。今回の非著者reviewはこのbounded sliceにだけ適用する。

## 7. Current production reality

[GET観測](../notes/phase-5b/observation.json)と[限定repair/Candidate確認](../notes/phase-5b/production-change.json)は次を記録する。

- main `79a0ddea948af18ef02ec63184e67f99ad7f8e09`。5-A基準からの差分はPR #490のHuman Gate scriptとtestで、validation無効化時のactive revalidation pointerを解除する修復。
- W34 `c7faf207515e7429dd74abd5adaf2962725587ef`。旧`5561e232…`へのHuman Preview REQUEST_CHANGES、修復Core統合、DRAFT_COMPLETEでの読者向け用語修正、fresh publication生成が記録される。
- **新しいRELEASE_CANDIDATE / PUBLICATION_PREVIEW pending**。Human Preview provenance null、Freeze/Release pending、active revalidation pointer null。旧Human判断は修正後exact bytesの承認ではない。
- Candidate payload digestは`d0af4c9ca917ce3a51d58fcd213846c4d49cb8d3a9334501484ec798970de429`、raw file SHAは`6d18b4962ad51bfa974fd4d814a61a070dcab36a0bff8499d11d5821c28dff7a`。旧`dbd4c783…`/`c45adaf7…`を現Candidateへ流用しない。
- reader、品質bundle/review、PDF、checkpoint等は更新。Evidence/Selection/Architecture/canonical Draft pathsは今回diffで不変。用語修復は、既知のsource意味/引用反例の解消を示さない。

rootはfull State validation、全binding閉包、PDF目視、全号独立quality reviewを再実施していない。Human提供decisionのtranscriptionは技術/構造が受容可能で用語修正を求めたと記す。その権限を尊重しつつ、局所的なrootの以前のfindingが全て修復/再審査済みという認定には置き換えない。

残Issueはこの判断に必要でないため読まなかった。PR #488/#489/#490は既存production baselineの保守であり、reconstruct成果や純削減に数えない。source/citation/renderer・acceptance/staging/cacheは保留のまま。研究標本のMemOSにcacheが登場したことも、J-GASのcache調査を再開する理由ではない。

## 8. 次の入口と権限

**この仮説を使う5-Cは非開始。別のfresh小記事を続けて同じ自己観測を繰り返さない。** 再開に値するのは、実運用で正しく固定された比較結論がhandoff先で利用できず、同じsubject/source版/条件を再調査したと名指せる例、または準備/保持/独立review費込みの差を観測できる実行環境が得られた場合である。単なる複数ファイル/別role/再訪ログは再開条件ではない。

全体再構築はこの仮説の実証待ちへ固定しない。**次の全体優先順位判断の入口は、読者向け原稿の完了判定とreview範囲が、Human修復負担をどこで防げていないかの限定確認とする。** 今回のB1/N3とW34の用語修復は候補信号になる。ただし既存governanceにもeditorial reviewはあるので、reviewer追加や意味欄増設を既定解にしない。実行するなら一つの実publication修復について、既にどの版/公開要素を誰が読んでいたか、欠けた判断と追加確認費を特定する。現在の小記事の成功を対照にした費用比較や、全W34再監査へ広げない。新しいtrial/実装はまだ選定していない。

これは外部blockedや新しいHuman Gateではなく、この単位が支持する判断面での停止である。Phase 4はclosed、Phase 5の全体目標はopen。history/旧accepted chainは変更していない。production操作、PR/Issue/外部メッセージ、State/Gates/承認/Freeze/Release/adoption/migration、通常Git Pull/Push/最終commitは行っていない。継続入口は[Phase 5 handoff](../handoff/astra-phase-5-continuation.md)。
