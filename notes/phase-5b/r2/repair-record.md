# r1→r2 repair disposition

rootはreview/r1-findings.mdを読み、R1-B1、N1–N3を全て採用した。新外部source/版は追加していない。r1は保存したまま。

| Finding | 原因とroot確認 | 修復/影響先 |
|---|---|---|
| R1-B1 | raw Mem0 §3.1/§3.2/Appendix Aを再確認。標本規模はC1に部分保持したが本文へ落とし、Jの寛容な採点条件は初稿facts/prose双方で不足していた。単なる用語の問題ではない | C1.c3に規模・質問意味・語彙指標とJの採点内容を追加。C2.c2に9k/35sessionsと集合同一性未確定を保持。composition must-coverを補い、本文冒頭に読者から見える評価条件を追加 |
| R1-N1 | v5のabs著者欄を再確認。rootは初期v1 metadataの順をv5にも適用してしまった。全著者は含むが固定版の順と不一致 | C2 attributionをWujiang Xu, Kai Mei, Hang Gao, Juntao Tan, Zujie Liang, Yongfeng Zhangへ修正。本文の先頭著者は同じ |
| R1-N2 | Mem0原Table1の同一実験内の逆転を追加対象にした。source外の新しい性能判断ではない | C1.m7とC1.l1にMem0g/ Mem0のsingle/multi Jを保持、draft_support更新。本文でgraph追加が多段推論を常に良くするわけでないと明記 |
| R1-N3 | 何を得て何が低下するか、p95と一般技術語の説明を明確化 | Jが低い一方で回答時入力量/遅延が小さいという方向を明示。コンテキスト/ノート/質問種別/判定用プロンプト、95パーセンタイルを使用 |

研究→編集→本文で新しい意味を先に保持し、本文だけにsource事実を追加していない。mechanical copy/JSON再保存を研究判断の反復に数えない。修復の原因は読者への説明不足と版別metadataの取り違えであり、同じ正しい結論が利用できず再構成したという仮説の支持ではない。

source不確実性は残る: Mem0のexact judge版、A-MEMとのcategory対応不一致の原因/正しい割当、再実行commit/全設定/評価集合の同一性。これらを解消したと偽らず、該当する比較を保留する。MemOSの後日HOLDとlatency不一致の記録も変更しない。r2の独立再reviewは別記録で確認する。
