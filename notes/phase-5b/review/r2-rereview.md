# Phase 5-B r2 independent re-review

判定: **今回のbounded sliceではblocking解消。追加のblocking/nonblocking findingなし。** R1-B1とN1–N3の修復を確認した。指定された一度の再reviewをここで区切る。これは保存sourceに基づく候補事実・採否・短い日本語本文の局所品質判断であり、全号publication completion、canonical受理、production adoption、実験再現またはnet lifecycle savingの認定ではない。

## 対象・identity

対象は `r2-freeze.json` と `r2/research.json`、`composition.json`、`manuscript.md`、`repair-record.md`、`work-record-at-freeze.md`。全体を読み、`review/r1-findings.md`の修復要求と事前source評価に照らして再reviewした。著者本文・研究・編集記録をreviewerは変更していない。追加委任・production操作・追加の外部source取得は行っていない。

r2 freezeの15ファイルを再hashして全て一致。r1 freezeの14ファイルも全て一致し、r1が保持されていることを確認。protocol、manifest、rawに新source/版の変更はない。A-MEM v1は準備履歴に留まり、主根拠はMem0 v1 / A-MEM v5 / MemOS v1のまま。対象 `r2-freeze.json` 自体のsha256は `9b5d473c274efdbd4a3546609275f9cc1c8c1b29070f07309afc27c38e0cde02`。

今回の限定raw再訪ではMem0 Appendix Aの実際の判定promptと、Table 1のMem0/Mem0g行を確認した。評価規模・質問種別、A-MEM v5著者順/評価集合の原文根拠は、前回までに同一hashのrawで確認済みの内容を利用した。全sourceを最初から読み直すことや、不要な新資料の追加を条件にしていない。

## 修復判定

| Finding | 結果 | source→facts→本文の確認 |
|---|---|---|
| R1-B1 | 解消 | C1.c3が10会話・平均26k tokens/200問、4質問種別、F1/BLEU-1の語彙一致、Jの参照回答と寛容な二値判定を保持。C2.c2には9k/35sessionsと集合同一性未確定が追加され、composition must-coverへ反映。本文第2–3段落に規模・質問意味・Jの採点条件と限界が現れた。 |
| R1-N1 | 解消 | C2 attributionが固定v5の原著者順に一致。本文の先頭著者との整合も維持。 |
| R1-N2 | 解消 | C1.m7はMem0g/Mem0を区別してsingle-hop J=65.71/67.13、multi-hop J=47.19/51.15を保持し、C1.l1とdraft_supportへ接続。本文もこの同一論文内の逆転を述べ、グラフの必然的改善を否定する範囲に留めた。A-MEM側の未解決値から推論していない。 |
| R1-N3 | 解消 | 全履歴よりJが低い一方、回答時の入力量と遅延が小さいという向きが明確。コンテキスト/ノート/質問種別/判定用プロンプトの日本語化とp95の説明を確認。残る英語のモデル名・指標名は説明と対応しており、新たな修復要求はない。 |

Appendix Aは同じ話題や時点を含めば寛容に正解とする指示を実際に含む。r2はこのpromptを実際の人間評価や厳密な事実確認と同一視していない。J判定モデル版を推測で埋めず、評価反復を独立再現とも呼んでいない。新しい日本語説明はsourceの意味を変えていない。

## 修復後も維持された境界・残るsource不確実性

- 主要表のsubject・数値・単位、overall Jの比較、OpenAI独自baselineと全履歴baselineの区別、Zepの反例、検索contextと総費用の分離は維持されている。表のp95を検索だけのlatencyやKVのTTFTと取り違える変更はない。
- Mem0のjudge具体版、A-MEM原表とMem0引用表のカテゴリ対応不一致の原因/正しい割当、再実行commit・設定・評価集合の完全同一性は未解決のまま。r2はその事実を保留条件として示しているため、これらの未解決自体は今回の記事をblockingにしない。原因を解決済みとする主張や、その部分を使った直接順位付けが復活すれば別の欠陥になる。
- MemOSは研究側で強い関連候補と実験結果、latency記述/表の不一致、KV試験の事前cache条件を保持し、cutoff後のHOLDを維持。後日の性能を当時の記事の根拠へ持ち込んでいない。本文からの省略はこの時点条件に整合する。
- 修復は研究記録・編集要件・本文へ届いており、必要な追加事実を本文にだけ孤立して置く変更は確認されなかった。参考リンクは固定版を指す。

sourceの範囲外まで網羅したか、全号のページ配分・PDF表示・production provenance/Stateが正しいかはこの判断から導けない。今回そのquality scopeを合格扱いへ縮小・置換していない。

## 作業観測の再review

W10は非著者review、W11は欠けた評価条件と版別著者順の修復、W12は本文の説明・反例追加として記録されている。これらを正しい既存結論が利用できず行った「除ける意味再構成」の支持例にしていない点は妥当。B1には研究記録に既に一部あった規模を本文に落とした編集上の不足と、J条件の保持不足の両方があり、全てを単一の重複研究原因へまとめる根拠はない。repair-recordのより細かな原因説明はrootによる自己報告であり、reviewerが内部認知を直接測ったものではない。

W06/W08のraw再訪理由の合理性は維持されるが、各時点の既存結論の完成度、再確認の内訳、除去可能量は識別不能。r2の末尾追記がこれを明示し、「0重複を測定した」としていないことを確認した。

このchainでは、**除ける意味再構成として支持できる具体例は確認されなかった**。同時に、認知的反復が一切なかったという実測も得られていない。したがってこの観測だけから仮説の支持、A/B差、全運用での不存在、費用優位またはnet savingを主張することはできない。独立review/repairが有用だったことは、別のarchitectureの優位を意味しない。最終のPhase 5判断では、この非支持と識別限界を両方残す必要がある。

## 時刻・費用・未実施

今回の初回clock観測は2026-09-13 11:28:01 UTC。再reviewの作業はr2全体読解、修復への照合、r1/r2 bytes確認、追加内容に関する限定raw照合と本記録作成。active time、tokens、金額、operation別費用はunknown。コマンドruntimeをLLM読解/判断費へ換算しない。事前評価時の中断spanも今回のactive作業時間へ混ぜない。必要な独立再review費を著者の再読削減と相殺しない。

新しいbenchmark/code実行、PDF/visual、full Weekly Discovery、canonical admission、production State/Gates/Freeze/Release、CI、historical caller/repair互換、移行/Human承認は未実施であり、費用ゼロ・品質合格ではない。許可された一度の再reviewを完了し、追加roundは開始しない。

再review固定時刻: 2026-09-13T11:29:45.331052+00:00。
