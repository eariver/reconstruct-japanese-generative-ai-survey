# Phase 5-B work observation

記録単位は意思決定に必要な作業の所在とsource再訪理由。実働時間/tokenの復元や思考過程の記録ではない。下表はtool/作業順に基づく初稿前の記録であり、個々の開始終了時刻を後付け推定していない。rootはsource reader/editor/author/補助準備を兼務し、費用を役割へ按分しない。

| ID | 対象/role | 入力・新情報と作業 | 分類/既存結論の使用 | 影響先 |
|---|---|---|---|---|
| W01 | 引継ぎ/root | Push済みcc530feaとproduction差分・State・用語修復worklogを確認 | 準備/新情報。PR490は既存baseline修復。全source調査へ広げない | protocolの日本語品質とcurrent reality |
| W02 | source選定/root | locator検索、v1 metadata/rawを取得。A-MEMにcutoff前v5があると判明 | 新情報による版選定修正。旧v1の答えを本文へ使っていない | source集合v5へ修正 |
| W03 | 読解補助/root | bs4が通常/同梱Python双方に無く一時導入。HTMLをparagraph/table ID付きに抽出 | 準備費。新しい意味正本/rendererではない。依存不足とstdout encoding失敗の修正も含む | reading aids |
| W04 | C1/root | Mem0の方法、評価、表、future workを読む。full-contextとのquality/query負担の違い、A-Mem既報と再実行を区別 | 初回source検証。Table2とmetric定義をC1へ保持 | C1と本文のtradeoff表 |
| W05 | C2/root | A-MEM v5の方法、評価、limitationと表を読む。C1の既報category対応と異なる数字配置を発見 | 新sourceとの横断照合。別sourceの初回検証であり同一結論の再構成ではない | C2、比較保留境界 |
| W06 | C1/C2/root | 抽出で落ちたcaption/Appendix prompt/最終k表をrawで確認。再実行の意味、judge不明、k=40/50を確定 | 初回の未消費部分を補完。疑義ある表のheader/行も再確認。表読解/抽出品質確認は残る必要仕事 | C1.c5/l3、C2.c3、category不一致 |
| W07 | C3/root | MemOS v1の三memory/MemCube設計、LOCOMOとKV別実験、表/latency説明とfuture workを読む | 強いHOLD候補のsource固有検証。全本文網羅ではない。cutoffを当時の根拠へ混ぜない | C3とHOLD理由 |
| W08 | C1/C2/root | raw表のheader/行とjudge関連文字列を限定確認 | source対応の最終確認。単なる抽出表の誤配列でないことを点検し、不一致原因とjudge版は未解決として保持 | 初稿の数値/限定 |
| W09 | 全候補/root | 既存意味欄のlab部分構造→採否/package→日本語本文を著述 | 事実から編集判断・読者説明への変換。既に保持したmetric/境界を利用。読解を全部やり直す禁止/強制はない | r1 research/composition/manuscript |

初稿時点で、除ける同一条件の意味再構成だとrootが認定できた事例はない。ただしW06/W08のraw照合には再訪があり、分類はreviewで点検する。この暫定観測は「反復が全運用に存在しない」ことや費用優位を示さない。publication出力やreview結果を見て後から成功だけを選ばない。

## 費用と中断

- root active time/token/料金: unknown。commandの短いruntimeを意味生成費に使わない。
- sourcesは約1.6MBのHTML/metadata（準備履歴A-MEM v1も含む）。bytesは保管量でありLLM入力tokenや実働費ではない。
- reviewerはHumanが今回明示許可した一体のみ。最初のturnはusage limitで終了した。Humanの枠復活指示後に同一agentを再開。中断前進捗/再開context/待機を無料としない。rootはsource期待内容を未読。
- 非著者source読解・期待内容・初稿review・再reviewは必要仕事として加算する。独立reviewを著者の重複読解削減へ含めない。
- permission質問とHuman回答は一回発生。通常運用の恒久Gateとして追加したものではないが、この観測のHuman handoffから除外しない。
- Core/admission/State操作、full issue synthesis、Human publication判断、PDF/visual、CI、歴史互換/移行は未実行。対応費と品質はunknown/未検証でありゼロとしない。

## r1 freeze後の作業

| ID | 対象/role | 作業と既存結論 | 分類/影響 |
|---|---|---|---|
| W10 | review/非著者 | source期待内容→r1の全facts/採否/本文/作業分類と原文を照合。B1一件とN1–N3を返した | 必要な独立review。rootとの読解重複を削減に数えない。W06/W08の内訳は識別不能と指摘 |
| W11 | repair/root | findingsを読み、Mem0規模/J promptとA-MEM v5著者順をrawで再確認。初稿で欠けた限定/原順を補う | 誤り修復。新sourceなし。C1/C2・composition・日本語本文を改版 |
| W12 | repair/root | 同一論文内のgraph逆転と用語をr2へ反映。source固有の未解決はそのまま保持 | 編集品質の修復。正しい既存結論の紛失による再構成とは認定しない |

reviewの判断を受け、初稿時の「認定できる具体例なし」は維持する一方、W06/W08を全量必須だったとも断定しない。raw再訪の理由は合理的だが、既存結論の完成度と再確認量の細分はこの観測では識別不能。全chainの最終判断はr2再review後に行う。

## 再review後

W13: 同じ非著者がr2の全記録/本文を読み、必要なrawとr1/r2のidentityを照合。B1/N1–N3解消、新findingなし。この再reviewも必要仕事であり削減ではない。W06/W08の識別不能を維持し、除ける意味再構成の支持例なし/ゼロ実測ではないとの判断を返した。source期待内容→review→一度の再reviewの許可範囲は完了。

W14: rootが再reviewを読み、5-Bの非支持/識別限界/費用unknownを評価文書とhandoffへ反映し、最終の局所整合検査を行う。これはreconstructの判断/文書化/保守費。5-C/追加試験/実装は開始しない。
