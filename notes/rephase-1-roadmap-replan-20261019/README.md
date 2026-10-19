# 2026-10-19 ロードマップ再計画と最初のtask

Human依頼: 目標/目的を再確認し、完了までを再計画、大規模探索はCo-Workerへ委任、再計画後は選択した最初のtaskを完了してCommit Pointを提示する。

- 現在の全体計画: [completion roadmap](../../outputs/rephase-1-completion-roadmap-20261019.md)
- Production入力: [DM022限定intake](dm022-intake/README.md)（必須Astra-requested correction込み）
- 開始HEAD: `eb6b79be1dc6fcd704194c46de1c2f53c7c26e58`、clean。今回intake packetは委任Worker作成であり、既存Human作業ではない。

## Closeout / current result

- [Astra R1可否判断・次task§5](../../outputs/rephase-1-integrated-admission-feasibility-decision.md): **両提出案NO-GO**。first taskは不採用/次投資判断として完了、implementation-ready契約は未成立。
- [fresh作者別review](independent-roadmap-decision-review.md) **必須§9**: replan/rejection/次taskに限るBOUNDED_PASS。原§3の「訂正で全解消/coherent」、§2全premise確認、§4費用最適の強い表現は§9で撤回/限定。両設計案にPASSはない。
- 次はinitial Weekly＋Thematic/Longformの実build→明示transfer→公開admission/実内容・visual点検。今回のCommit Point後にHuman continuationで開始する。
- [restoration qualification](admission/restoration-evidence-correction.md)と[current observation raw](admission/current-source-verification-20261019T000525Z/README.md)を併読。復元当時rawと後発観測を混同しない。runtime実装/test/build/Production mutationなし。
- 下記R1 taskは開始時の定義として保持する。出口「採用不能ならblocker＋代案/採否決定」を適用した。元Worker提案のAPI/小path予算/fixture手順は実装指示ではない。

## 調査の採否（Astra）

Explore二担当が目的/完成線と現在技術依存を広く探索し、GeneralがSummary＋Issue562を3 GETで取得した。探索返却は一次証拠や独立auditではなく、Astraの判断入力である。

採用: 総費用最適化と実運用/旧経路廃止がfinish line、統合未了、便益未測定、entryの重複、/tmp source不在、保存4inputs＋full21patchの可用性、DM021の相互依存した述語。

採らない/訂正する返却:

- 「409をそのままWeekly-first adoption候補にする」: readiness未証明。Specialを暗黙に後回しにして全体完成を宣言しない。
- 「LF2I10＋DM02111」: 分類誤り。LF2I時点は9file、現21はその累積。正確なpath集合はR11 static21を用いる。
- 「新intakeはHuman新規packet」: 並行Generalが本依頼で作成したpacket。
- 「DM022はreconstructに無関係/別cycleのため分析禁止」: 誤り。intakeの末尾訂正が優先する。既存role/Production権限は維持し、Humanが委任した計画選択に不要な承認待ちを追加しない。
- 「3modifiedを読まずpin/patchだけで十分」: 統合設計には実base callerとfinal21全体が必要。復元後のactual-sourceを使う。
- 「Human判断まで停止」: 本依頼は再計画後の最初のtask完了まで続行を明示。

## R1 task契約 — 再計画後の最初のtask

Generalが実sourceを準備・分析し、Astraが契約選択、fresh作者別Generalが設計を検証する。実装/通常test実行はこのtaskの成果としない。

1. 新fail-closed手順で4parent inputsからactual409独立DBを復元し、保存full21patchをDIRECT適用。固定hash/actualHEAD/tree/清浄base/最終21bytesとstatus、inert origin/no alternates/独立DB、保存inputs不変を確認。旧runner・fake root・network refreshなし。失敗rawを保存し再実行は別名、cache84は以前の実体を再創作しない。
2. actual final21＋既存controller/State/revalidation/receipt/Gate/Candidate/Review/build callersを読む。DM022との共通保持原則とstage固有の差をsourceで示す。
3. versioned reviewed targetとlive出力、reasonとrecord、State旧新参照、current authorityとhistorical readback、receipt/Gate/manuscript、install窓/所有書込み/失敗復旧、existing Candidate衝突、通常QA/Candidate/Preview/Freeze/Releaseを**同じ操作の契約**にする。既存reviewのpathを同一SHAで付替えず、accepted Draftの上書きや偽reason、generic pending bypassを使わない。
4. 現状維持/一貫した最小拡張/より大きなauthority置換を、実caller・除去作業・追加保守・failure costで比較。code path数に恣意的上限を課さず、未接続helperの追加で終了しない。route別適用域、明示拒否、移行制約を記す。
5. 次のvertical implementation taskの具体API/schema/path変更面、実fixtureのauthority生成順、成功/負例/失敗時のoracle、必要回帰とsource-committed fixture条件を返す。実装不可能なら、残る決定を次の分析へ丸投げせず根本blockerと代案/採否を決定する。
6. Astra実sourceレビューと修正後、fresh独立設計reviewで出口と費用/権限を検証。設計PASSはimplementation/application acceptanceではない。完了後entryを本ロードマップ/R1結果へ接続しCommit Pointで停止。
