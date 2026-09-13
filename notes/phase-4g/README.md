# Phase 4-G — 著述方式の限定設計比較

[判断書](../../outputs/astra-phase-4g-authoring-design-assessment.md)が現行decision。既知入力の表現力・依存関係を比較し、直接canonical著述の費用優位は主張しない。

- [observation.json](observation.json): main/W34は4-F末尾と同じ。reconstructのHuman commit名にあるPhase番号とは独立に、durable判断書の次を4-Gと呼ぶ。
- [inputs.json](inputs.json): mainの7固定入力。rawはignored `.phase-4-inputs/<ref>/<path>`。GitHub GETのみ。
- [comparison-result.json](comparison-result.json): 上記7件＋4-Dの歴史Package1件のidentity、2 lab入力のSHA、現行function位置と参照選択の反例。
- [compare.py](compare.py): `_refs/_ref_rows`だけをASTから抽出して実行。main/State/Gate/writerは実行しない。
- [closeout-check.json](closeout-check.json): localリンク、文書/試験script/outputのidentity、diff whitespace検査。品質認定ではない。

再現:

```
python -X utf8 notes/phase-4g/compare.py
```

rawの再取得が必要なら、4-F capture moduleの`module.DEST`を本directoryへ設定して`get(ref,path)`を使うか、固定GitHub blobを取得しmanifestのhashへ照合する。4-F CLIの既定保存先は4-Fなので、4-G記録を復元する際に過去manifestを不用意に更新しない。

4-E Draftと4-F Cardは既存schemaを検査した。2つの参照variantは同じ本文のsource sufficiencyを認定するためのものではなく、canonicalが区別する参照をcompact modeで選べないことを示すfixtureである。4-F修復Cardをaccepted Packageへ挿入していない。new renderer/PDF/独立review/品質試験は未実行。

今回の仕事はmainの関係code取得・読解、欄/責務の比較、関数反例、判断/引継ぎ。初回に存在しない`run_evidence_v2_agent.py`を仮定したGETが404となり、directory listingで`run_evidence_v2_agent_first.py`を確認した。これはrootの調査費である。role別active time、token、料金、純削減値はunknown。新store、telemetryや大規模shadow executionは作っていない。
