# Publication review境界 — Evidenceと識別限界

2026-09-14 JST。[scope](scope.md)に従うW34 Human Preview r2の一件調査。[判断文書](../../outputs/astra-phase-5-publication-review-boundary-decision.md)が現在の結論。

## 1. 入力と確認方法

[observation.json](observation.json)はread-onlyで取得したref、5-B基準からのcommit/file差分、現在State。[inputs.json](inputs.json)は26個の固定Git入力についてref/path/Git blob SHA-1/raw SHA-256/bytes/URLを記録する。原ファイルはignored `.phase-5-inputs/<ref>/<path>`。必要なものだけ、既存`notes/phase-5b/capture.py`をimportして`DEST`を本directoryへ指定し`get(ref,path)`で復元できる。既存5-B manifest/freezeは変更していない。

[check.py](check.py) / [結果](check.json)はその26 inputsのbytes/Git blob、旧review→manuscript→問題のTeX/bib、現在State→approval→Candidate/PDF等の局所binding、実際の修復差分を照合する。production moduleを実行しない。旧PDFは取得せずHuman記録とreviewの対象hashを照合。新PDFはbytesのhashだけで目視/ページ判定はしていない。

## 2. 同じ対象版にあるPASSとHuman finding

旧対象は`c7faf207515e7429dd74abd5adaf2962725587ef`。canonical Human r2 transcriptionはCandidate payload `d0af4c9c…`、PDF `1818e866…`（12 pages）を明示し、次の二点だけを要求している。

- reader-facing claim boundaryに出た`Selection r2` / `Package 4`等の内部編集経緯を、節の範囲という意味を保って読者向けにする。
- bibliographyの`visited on`をedition cutoffではなくcanonical source access provenanceへ合わせる。

固定根拠: [Human r2 transcription](https://github.com/eariver/japanese-generative-ai-survey/blob/6be0f462d8f02284f8513d7165c778c3797dcaf4/sources/2026-W34/execution/reviews/w34-human-publication-preview-decision-20260913-r2.md#L6)。これは実行側のHuman判断転記である。Issue #491の本文/コメントを追加取得していない。要求・対象・承認はcanonical記録で今回の問いに足り、他Issueは探索していない。

| 対象・記録 | 記録が述べた範囲 | rootが照合したこと / 分からないこと |
|---|---|---|
| 旧reader manifest | `READER_FACING_AUTHORED`。main.texとsupporting section/bibliographyをhashで指定 | raw manifest `6a60e95c…`、section20 `8f8c0488…`、bib `1d3fecf3…`は実bytes一致。manifest自身のpayload digest `6e9b3de6…`とrawは別 |
| 旧semantic review | `PUBLICATION_BOUNDARY=PASS`、内部pipeline用語なし。evidence_locationsにsection20を含む。`BIBLIOGRAPHY_METADATA=PASS`は41 citation解決/再生成一致/内部注記なしを説明 | 問題のclaimboundaryはそのsection20内に一回あり、reviewがbindするmanuscriptと一致。access日のsource照合を示すdetailはない。key解決/再生成一致は正しい日付の証明ではない |
| 旧visual review | exact12-page PDFのcover/目次/7節/claim boundaries/41参考文献を確認、reader-facing entriesのみと記す | semanticと同じPDF hash。Humanの対象とも一致。実際の目の動き/読解単位は記録から復元できない。旧PDFをrootが再目視したわけではない |
| r1修復worklog | 日本語技術用語のcontext-sensitive置換。claim boundaries/bibliographyは変更せず。text-layerで残存訳語を確認 | 狭い修復作業の記録と、上の広い全体PASS宣言との隔たりを確認できる。「記録にないので読まなかった」とは断定しない |

固定根拠: [旧semantic](https://github.com/eariver/japanese-generative-ai-survey/blob/c7faf207515e7429dd74abd5adaf2962725587ef/sources/2026-W34/publication/v2/semantic-editorial-review-v2.json)、[旧visual](https://github.com/eariver/japanese-generative-ai-survey/blob/c7faf207515e7429dd74abd5adaf2962725587ef/sources/2026-W34/publication/v2/visual-review-v2.json)、[旧manifest](https://github.com/eariver/japanese-generative-ai-survey/blob/c7faf207515e7429dd74abd5adaf2962725587ef/sources/2026-W34/publication/v2/reader-manuscript-v2.json)、[r1 worklog](https://github.com/eariver/japanese-generative-ai-survey/blob/c7faf207515e7429dd74abd5adaf2962725587ef/sources/2026-W34/execution/luna/w34-human-preview-r1-terminology-correction/session-worklog.md)。

旧manifest著者、semantic/visual reviewer、r1実行agentは全て`Muse Spark 1.3 (W34 Human preview r1 terminology correction)`相当の名義。[レビューdirectoryの限定一覧](review-directory.json)にはこのexact版の独立publication reviewファイルは見当たらなかった。これは独立supervisory消費を実証しないが、他の会話/場所で一切reviewしなかったという証明でもない。モデル名から能力や独立性を推定しない。

## 3. 修復箇所と責務

[旧section20 L18](https://github.com/eariver/japanese-generative-ai-survey/blob/c7faf207515e7429dd74abd5adaf2962725587ef/surveys/weekly/2026-W34/sections/20-agent-workflows.tex#L18)のclaim boundaryは、[Draft Result](https://github.com/eariver/japanese-generative-ai-survey/blob/c7faf207515e7429dd74abd5adaf2962725587ef/sources/2026-W34/draft/v2/packages/w34-collaborative-agent-workflows-retrieval/draft-result.json)の`blocks[CLAIM_BOUNDARY].text`全体と一致する。末尾は`regional processing is NOT part of this package after Selection r2; it belongs to Package 4`。Human記録はArchitecture/Packageでは正しい内部auditの文言で、公開TeXでは正規化が必要と分類している。rootはArchitecture全文の独立再審査まで行っていない。

[修復section20 L18](https://github.com/eariver/japanese-generative-ai-survey/blob/6be0f462d8f02284f8513d7165c778c3797dcaf4/surveys/weekly/2026-W34/sections/20-agent-workflows.tex#L18)は末尾を`Regional processing is outside the scope of this section and is discussed with deployment and model-distribution conditions`へ置換。旧TeXにこの一置換を適用すると新TeX全体と一致する。境界全体/実質的限界を削った修復ではない。

bibは41 entries全ての`urldate`が`2026-08-21`→`2026-09-08`。dateフィールドを除く旧/新textは完全一致。41 accepted sources全件の独立再検証はせず、canonical accessへの41/41一致はCore/edition側auditの報告として扱う。[Core checkpoint](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/docs/checkpoints/core-v2-bibliography-access-provenance-repair-20260913.md)と[main diff](main-diff.json)では、Weekly cutoff / Special as_ofを日付に流用する経路を除き、accepted sourceのaccessed_atを解決する共通helperへ変更。空/不正timestamp、未解決の異なるcapture timestampはfail-close、明示offsetの暦日を保持する。source URL/同一timestamp等に関する実装分岐もあり、普遍的source identity完成とはしない。

[current Weekly generator L329](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/scripts/survey_weekly_semantic_publication_v2.py#L329)はCLAIM_BOUNDARYのtextをescapeして出力する。一般的な内部audit→読者説明の書き換えを#492が実装したわけではない。ただし、現W34は修復済みTeXを正式にmanifestへbindしている。通常PDF rebuildで旧Draftの文言が必ず復活するとは言わない。将来Draftから再著述する場合とTeXからのbuildを分ける。

## 4. 既存contractと機械確認の限界

- [governance L15–52](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/docs/survey-production-core-v2-sol-luna-review-governance.md#L15)は実行とsupervisionの独立性、draft/publicationのeditorial/semantic/visual責務を既に規定。§9は内部reviewを追加Human確認へ変えない。新reviewerを増やすことをこの実例から正当化しない。
- [publication review contract](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/config/publication-review-v2.json)は`PUBLICATION_BOUNDARY`と`EXACT_PDF_VISUAL_REVIEW`を既に要求。
- [review validator L519](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/scripts/survey_reader_publication_v2.py#L519)はhash/同一source/PDFページ数/要求check集合等を確認し、fidelityへ委譲。[schema](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/schemas/publication-review-record-v2.schema.json)はdetail/evidence_locations/reviewed_byを文字列として要求する。
- [fidelity L419](https://github.com/eariver/japanese-generative-ai-survey/blob/74708eb26a357ec11a839a59de62ab62cd246eef/scripts/survey_reader_fidelity_v2.py#L419)の追加review-depth規則はLONGFORM_SPECIAL用。Weeklyではreturn。Specialの明示block条件も意味品質の保証ではなく、そのままWeeklyへ移せば今回の見逃しが防げるとはしない。

rootはこの限定code読解を行った。Coreの全validator/tests/CIを再実行したとはしない。機械側が人の読解を証明しないことは設計上の責務分離であり、hash検査を緩める理由ではない。

## 5. 発生した仕事と現在の終端

[r2 repair worklog](https://github.com/eariver/japanese-generative-ai-survey/blob/6be0f462d8f02284f8513d7165c778c3797dcaf4/sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/session-worklog.md)は正式rollback、Core統合、reader一置換、41日付再生成、CI build `34762344518`、PDF text確認、manuscript/bundle/semantic/visual/2 checkpoints/Candidateの再記録・検査を記録する。CI durationの3m45sはこのworklogの報告値であり、rootがActions APIで再計測していない。r1にも別build/review/Candidate生成がある。一連の費用をファイル数やcheck数から認知費へ換算しない。

全roleのactive time/token/金額、Humanが各指摘にかけた時間、generic PASSの実際の読解量、早期確認なら何件防げたかはunknown。修復そのものと品質reviewは必要仕事。回避候補は、同じ修復をpublication readiness前に終えられる場合の追加周回だけ。Core開発/試験/保守費も無償ではない。

現在は[canonical r3](https://github.com/eariver/japanese-generative-ai-survey/blob/6be0f462d8f02284f8513d7165c778c3797dcaf4/sources/2026-W34/gates/reviews/publication-r3.json)で`APPROVED`。reviewed commitは`f9f3e040…`、Stateの履歴pre-approval raw `691fb12f…`をbindする。現Stateは承認記録後なので別bytesで正常。

- 現Candidate raw `df376f474acf5fafa14f9af5196727858b1dd76f5c7d17664fa52ba784e32061`、payload `52c8d0bcc85140a2727d1867a908d7077d40c7088a7c1e83f10b66044c50f3ba`。
- 現PDF raw `e93db71a5be8249d65d66c5f3b0284875447d953eeadf3b66ca23a9318bd06de`、338722 bytes。
- approval raw `80e90446…`はState・checkpointのpointer、r3 immutable approvalと一致。r3がreviewしたCandidate/PDFのhashは現在bytesと一致。
- `RELEASE_CANDIDATE` / Human Preview approved / `stage:freeze`、Freeze/Release pending。rootによるfreeze実行や新たな品質承認はない。

PR #492は既存production保守。5-B終了後のadvanceとして反映するが、reconstruct成果/純削減とはしない。
