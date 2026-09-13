# Phase 5-B r1 independent review

判定: **REPAIR REQUIRED（blocking 1件、nonblocking 3件）**。対象は固定されたlabの候補記録・採否・日本語本文・作業観測であり、production admissionや実験再現の判定ではない。著者出力は変更していない。

## Identity・独立性・範囲

- `r1-freeze.json` の14ファイルをbytesから再hashし、全て記載sha256と一致した。準備履歴のA-MEM v1の同一性確認は行ったが、その本文を性能の根拠として読んではいない。
- `review/expectations-freeze.json` の事前期待内容・protocol・manifestと6つの主source rawも再hash一致。事前期待内容は11:18:47 UTCに固定、r1は11:21:43 UTC固定、reviewの初回clock観測は11:22:11 UTC。非著者reviewerは事前評価の固定までr1やrootの著述/reading aidを読んでいない。root自身の「初稿freezeまで期待内容未読」はfreezeの宣言とsessionの手順に基づく。モデル内の認知状態や学習履歴まで外部計測したわけではない。
- `r1/research.json`、`composition.json`、`manuscript.md`、`work-record-at-freeze.md`を全体読解。事前評価で確認した原HTMLの方法・評価・表・脚注を基準にし、今回はMem0評価集合/J定義、A-MEM著者・評価集合/限界、MemOS future directionsを限定再確認した。新しい外部sourceは追加していない。
- PDF/visual、benchmark実行再現、原コード版の監査、全Weekly Discovery、全canonical受理、Human Gate、CI、historical互換・migrationは範囲外の未実施事項として維持。これらを合格/ゼロ費用にはしない。

## Blocking finding

### R1-B1 — 評価の規模・判定内容を本文に残す

影響先: `r1/manuscript.md` 第2段落〜比較表およびA-MEM比較段落。上流の`research.json`では`C1.c3`が規模を部分的に保持しているが、Jの具体的な採点基準と語彙指標の意味が薄い。`composition.json`の`quality-and-query-cost`/`comparison-boundary`。

本文はJを「別のLLMによる正誤判定の平均値」とし、モデル版不明・adversarial除外・独立再現ではない点は正しく述べている。しかしLOCOMOがどの程度の標本かは示さず、single/multi/temporal/open-domainの意味も英語のまま、F1/BLEU-1も名称だけである。特にAppendix AのJはgold answerと同じ話題や時点を含む回答を寛容にCORRECTとするpromptであり、この条件が抜けると表のJを厳密な事実正誤や広い読者品質へ読み替えやすい。今回の問いは「何が品質として測られ、比較に何が残るか」であり、この不足は単なる詳しさの好みではない。

原文根拠: Mem0 raw `S3.SS1`は10会話・平均約26k tokens・会話当たり平均約200問と4質問種別、`S3.SS2.SSS0.Px1`はF1/BLEUの語彙一致の限界、`A1`はgold/generated answerを用いた寛容なCORRECT/WRONG判定。A-MEM raw `S4.SS1`は5カテゴリ、7,512 QA、平均9k tokens/最大35 sessionsとF1/BLEU-1を説明。両論文の集合説明を同一と認定する根拠にはなっていない。

必要修復: 少なくともMem0評価の規模と対象、Jが参照回答に照らすLLM判定でそのpromptに寛容さがあること、F1/BLEU-1は主に語の重なりの尺度でJとは異なることを、自然な日本語で読者から見える位置に残す。必要な事実はresearchにも根拠付きで保持する。全実験詳細の追加や結果再現を条件にはしない。A-MEMの全件数を記事へ列挙することまでは必須ではないが、同名benchmarkでも同一の評価集合を確認できていないという比較条件は維持する。

## Nonblocking findings

### R1-N1 — A-MEMの著者順を固定metadataに合わせる

影響先: `research.json` C2 `attribution`。

r1は `Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, Yongfeng Zhang`。固定v5のabs metadataとHTML著者欄はいずれも `Wujiang Xu, Kai Mei, Hang Gao, Juntao Tan, Zujie Liang, Yongfeng Zhang`。全著者は含まれているが原順ではない。正式な著者列として保存するなら原順に直す。本文の「Wujiang Xuら」は影響しない。

### R1-N2 — グラフの効用について同一論文内の逆転を一言で明確にできる

影響先: `manuscript.md` グラフ版の集計差の段落、必要ならresearchのcategory metrics/limitations。

本文のoverall J差1.56ポイントと追加latency/context量、Zepのopen-domain優位は正確。グラフを全質問に優位とは断定していないのでblockingにはしない。ただし現文の「質問種別でも一様な勝利ではなく」の具体例は方式間のZep比較であり、Mem0g自体がMem0より低いカテゴリがあることは伝わりにくい。Mem0 Table 1ではsingle-hop Jは65.71対67.13、multi-hopは47.19対51.15。グラフの追加が多段推論を常に改善するという直感への有用な反例である。短く入れる場合は同一表内の報告に限定し、A-MEMの未解決カテゴリ対応と混ぜない。

### R1-N3 — 本文の用語とトレードオフの向きを明瞭にする

影響先: `manuscript.md` 全体、とくに第2段落とA-MEM段落。

「Mem0は回答時の負担との引き換えを示している」は、何を得て何が下がるのかが日本語として曖昧。ここは全履歴よりJが低い一方、応答時の入力量と遅延が小さいという方向が読み取れる説明にする余地がある。また一般的な「コンテキスト」「ノート」「質問種別」「判定用プロンプト」に置き換えられるcontext/note/category/promptが続き、技術日本語として読みづらい。p95は初出で95パーセンタイルと説明できる。意味は全体から理解できるため、これら単独では不合格にしない。用語置換だけでR1-B1を修復したとはしない。

## Source→facts→採否→本文で成立している点と未確定範囲

- C1のMem0/Mem0g機構、主metrics（66.88/68.44/72.90、1.440/2.590/17.117秒、1,764/3,616/26,031 tokens）、OpenAI比較相手と26%の帰属、Zepの反例は原表に沿う。検索latencyと総応答latency、保存量と検索context、総費用を分離している。raw label不一致を勝手に訂正していない。
- C2のA-MEM v5採用、k=40/50、原論文のF1/BLEUとMem0側A-Mem*再実行を分離する判断は適切。カテゴリ対応不一致は原HTML見出し/セルで再現できるので、現状の直接比較HOLDは支持できる。ただし原因、正しいデータカテゴリ対応、実行commitと全設定の同一性は未確定。コード再現を要求せず、この限界を維持する。
- C3は設計だけの弱いDROPにしていない。後日sourceのJ優位、latency本文/表不一致、KV実験の事前cache条件を研究側に保持し、Weekly本文の根拠へ入れないHOLDは支持できる。sourceのtotal P95 7,937対7,016 msの逆転は正確。独立した後日運用比較の結論を得たわけではない。
- MemOSを当時の読者本文から省いたこと自体はomission defectではない。採否・強い対照・時間境界が研究/編集記録に明示され、本文に後日情報を密輸していないからである。
- 局所のhash/locator検査PASSは、このreviewの判断や論文性能の保証の代用にはならない。R1-B1が残るため、この時点のreader prose完成は未成立。

## 作業観測に関する独立点検

`work-record-at-freeze.md`のW04/W05は異なる一次sourceの初回検証、W07は未選択候補の必要検証、W09は既存記録を用いた編集・説明判断として合理的。W06/W08のraw表・caption・prompt確認は、抽出品質とsource内外の疑義に対する検証として理由がある。独立reviewも別roleの必要な仕事であり、rootの読解と内容が重なるだけで削減候補にはならない。

ただしこの記録では、W06時点でどの結論が完全に固定され再利用可能だったか、W08で同じ疑義をどの範囲まで解消し直したかをoperation単位に識別できない。W06とW08を全量「必須だった」とも、全量「除ける再構成だった」とも独立確定できない。W09でresearch→composition→proseへ移る際の認知的再構成量も実測していない。記録された理由は妥当性を支えるが、実際のcognitive workを完全に可視化するものではない。

したがって現時点で言えるのは、**除ける意味再構成として支持できる具体例が記録上まだ確認されない**こと。ゼロ件の実測、全運用での不存在、net saving、仮説の一般的棄却を意味しない。W06/W08の細分および認知的作業量はunknown/識別不能を残すべきである。r1自身の「rootが認定できた事例はない」という限定はこの範囲を逸脱しない。repair/re-review前なので、全chainに関する最終停止判断はここではしない。

## 費用・review補助

reviewの初回clock観測は2026-09-13 11:22:11 UTC。この段階では新source探索なし、保存r1全体読解、identity再hash、必要箇所のraw再確認、findings作成を実施。role別active time、tokens、金額、operation別費用はunknown。tool runtimeはコマンド実行時間でありreview費用へ換算しない。事前評価の枠中断を含むspanと今回のreviewを混ぜてactive timeと呼ばない。今回のsource再訪はreview品質のための新しい役割上の確認であり、rootの削減と相殺しない。

review固定時刻: 2026-09-13T11:24:40.511234+00:00。対象r1-freeze.jsonのsha256: `99ccc1cb4ccbe468222fcbf310ff8ce8dae60431de502b24b3ac1e0bd2685429`。
