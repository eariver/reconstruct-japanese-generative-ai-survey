# Phase 4-H — 接続反例とPhase 4 closeout

[判断書](../../outputs/astra-phase-4h-connection-and-closeout.md)が現行decision。Phase 4はclosed、接続probeは反例で停止、修復/再生成は未実行。production採用・全品質・純費用削減の完了ではない。

- [observation.json](observation.json): main/W34のGET、f50d229→8480f4dの6 commits/14 paths。mainは14781409。
- [inputs.json](inputs.json): 今回の固定8 rawのGit blob/SHA-256/bytes。cacheはignored `.phase-4-inputs/<ref>/<path>`。
- [refresh-result.json](refresh-result.json) / [check_refresh.py](check_refresh.py): 実State、revalidation、checkpoint、Candidate/stage recordの4 binding。Candidate payload digestとfile hashを区別する。前4つのpublication metadataは旧rawと差分から照合。PDF本体/全State validatorは未実行。
- [probe-result.json](probe-result.json) / [probe.py](probe.py): 歴史Packageと4-E Draftの接続を試し、同じURLに異なるtitle/date/access metadataが対応する反例で停止。
- [closeout-check.json](closeout-check.json): 入力/出力identity、localリンク、JSON/whitespace検査と実行範囲。反例の再現をpublication成功へ読み替えない。

再現:

```
python -X utf8 notes/phase-4h/check_refresh.py
python -X utf8 notes/phase-4h/probe.py
```

probeのPASS表示は「期待された反例を再現できた」という意味。初回section出力、bibliography出力、修復往復、独立review、PDF、Specialは成功/完了していない。現mainのpure rendering関数だけをASTから取り出し、v2個別source/subjectの一時mappingを作った。URL集約時のmetadata guardは今回のlab判断であり、production Coreの新しい規則ではない。入力を変更していない。

初回probeは`conflicting citation metadata`で停止した。所在を絞るread-only走査で2 Cardsのmetadataを確認し、曖昧性を結果へ残す再現entryにした。未実行だった成功/repair assertionsを取り除き、成功したと読める成果物は出力していない。この準備/失敗/再評価・引継ぎもrootの仕事で、production障害や費用削減には計上しない。active time/token/料金はunknown。

旧4-F lab Cardをaccepted Packageへ混ぜていない。source再取得や意味修復へ範囲を広げず、Phase 3-Gの全体目的と停止原則へ戻ってPhase 4を閉じた。raw復元ではmanifestの固定ref/pathをGETしてhashを照合する。4-F capture moduleを再利用する場合は`module.DEST`を本directoryへ設定し、過去manifestを更新しない。
