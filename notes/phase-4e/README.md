# Phase 4-E — canonical境界表現と出力関数の限定検証

2026-09-12 JST。**LAB / FUNCTION-UNIT PROBE COMPLETE / NOT ADMITTED / NOT QUALITY-COMPLETE**。

問いは「既存のcanonical制約・根拠を保った日本語Draftを、内部注記を足さずに出力できるか」。既知W34の1 packageを用いる互換性反証であり、未知sourceの比較、production実行、全号の品質試験ではない。着手時の[ref観測](observation.json)はPhase 4-Dと同一だった。

## 入力と著述範囲

- [使用した固定入力](used-inputs.json)。rawは`.phase-4-inputs/<ref>/<path>`。追加GETは[inputs.json](inputs.json)の4件で、他は4-Dから再利用。各rawのGit blob SHA-1 / SHA-256を検査。
- [author.py](author.py)は歴史Draftの4本文block・headline/deck・根拠・Package/prompt bindingを保持し、連結された境界blockを12個のsubject別日本語案へ置き換える。一律stripではない。
- 22件の境界は名指しblockへ、内部配置制約1件は`RESPECTED_BY_OMISSION`へ対応付ける。元Architecture/Packageは不変。既存must-cover対応も名指し箇所に限定するが、本文の網羅性を独立認定していない。
- [draft-result.lab.json](draft-result.lab.json)はfull Draft Result構造の**DRAFT**。元operatorのrunner情報を流用せずlab著述と明記する。historical Packageのhashは入力の識別であり、Humanの新しい採用許可を意味しない。State、承認、accepted結果を作成していない。
- [日本語案](boundary-wording.lab.md)は同Draftからの閲覧用抜粋。既存4本文blockの品質・現在の事実・元sourceの真偽は再検証していない。

## 実行したもの

```
python -X utf8 notes/phase-4e/author.py
python -X utf8 notes/phase-4e/probe.py
```

[probe.py](probe.py)は固定sourceの指定した関数・定数だけをASTから取り出す。`validate_draft_result`本体と使用するCoreのload/hash関数は改変しない。CLI、State/Gate検証、package admissionの呼出し元、production writerは実行しない。従って「関数単位のvalidator PASS」と「full canonical admission」は別である。

Weekly rendererは**元Architectureのままではsection_label不足で拒否**した。その記録を残し、後段block分岐を見るためだけにmemory上のfixtureへ`section_label=LAB FUNCTION FIXTURE`を補った。placeholder cover/frontmatter/summary、元compact spec、既存bib keyを使う。fixtureは変更済みArchitectureや承認ファイルとして保存しない。この実行を元Architecture対応PASSに数えない。

[weekly-renderer.lab.tex](weekly-renderer.lab.tex)はその関数単位のsection抜粋で、12境界blockにcitationが付かない。[existing-block-renderer.lab.tex](existing-block-renderer.lab.tex)は、既存の別rendererにある`render_block`を、canonical Cardから解決した一時的なmappingで呼んだ12境界block。引用が付くという機構の確認だけで、full rendererの移植ではない。mappingや表示用抜粋を新しいcanonical意味storeにしない。

機械検査: schema/関数validator、22+1 dispositions、20 distinct LIMITATION refs、4本文blockの保存、5つの拒否control、意図的に誤った意味文が機械validatorを通る限界control、12/12 blockのcitation挙動、既存41件のbibliography生成で既知内部noteだけを除く操作。他の意味あるnoteを一般に削除してよいとは検証していない。

## 結果と停止境界

[probe-result.json](probe-result.json)と[判断](../../outputs/astra-phase-4e-canonical-rendering-assessment.md)を参照。既存構造で著述は可能だが、Weekly rendererの入力要件・引用経路、Card内のsource対応に未解決点がある。旧renderer全体もv2のdrop-inではなく内部role noteを出すため、無変更の置換を提案しない。

今回rootが日本語案を自己照合した範囲は**著者検査**。独立review・再reviewではない。Phase 4-Cの1体のreview許可は完了済みなので追加委任していない。既に互換性/根拠対応の停止理由が得られたため、この状態で独立quality試験やPDF compile/visual QAへ進めない。追加のHuman Gateを新設したものでもない。

費用にはrootのcode読解、22境界の照合・日本語著述、試験用scriptとfixture、結果整理を含む。機能単位の処理時間を全production費へ外挿しない。active time/token/料金はunknown。PowerShellのrg wildcard誤用、広いJSON表示のtruncation、section_label不足による初回停止も調査費である。最後の停止は実入力に対する互換性findingとして保持し、fixtureで無かったことにしない。

productionはGET/read-only、Pull/Push/commitなし。全号完成、Special一般性、historical全閉包、独立source品質、純費用削減は未実証。
