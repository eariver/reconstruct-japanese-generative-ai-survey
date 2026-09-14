# Phase 5 current upstream reconciliation Evidence

2026-09-15 JST。reconstruct開始HEAD `b8bdf9821a48d22b2db840458b1b385f1c744bdb`。productionはGET-only、実行は固定sourceのローカルfixtureだけ。

判断は[assessment](../../outputs/astra-phase-5-upstream-reconciliation-assessment.md)。旧[candidate Evidence](../phase-5-runtime-repair/README.md)は歴史として不変。

## 保存物

- `observation.json`: main refs、clean開始、3e3eebe0→774dd39aの8 commits / 16 changed files。通常Pullはしていない。
- `inputs.json`: current固定refからGETした17ファイルのpath / Git blob SHA-1 / raw SHA-256 / byte count / URL。全変更runtime script/schemaと上流fixture二つ、実W34のState/Release checkpoint/manuscript/approval。rawはignored `.phase-5-inputs/<ref>/`。
- `selected-diff.json`: stage validator / Release helper / controller / Stage schemaの変更箇所。全repository監査ではない。
- `open-issue-index.json`: open Issue検索のタイトルindex。5/5、incomplete_results false。本文/コメント/closed Issueは今回読んでおらず、関連事項が他の記録にない証明ではない。
- `probe.py` / `probe-results.json`: current実関数/schemaを使う限定witness。上流test helperのfixtureのみ再利用し、既存test suiteを起動しない。
- `check.json`: 17取得ファイルのraw/Git blob hash、JSON/構文、22ローカルリンク、HEAD/indexと歴史候補の不変を確認。

## 実行と範囲

reconstructで `python notes/phase-5-upstream-reconciliation/probe.py`。Python/jsonschema等の既存runtimeを使用。`inputs.json`に対応するrawと前回support snapshotが必要。キャッシュ欠落時は[既存GET capture helper](../phase-5b/capture.py)で固定ref/pathを取得し、今回inputsのhashと照合できる。全archiveの再取得は既定にしない。

probeは前回support manifestに照合したscripts/schemas/config 307ファイルをignored `.phase-5-inputs/upstream-reconciliation/`へコピーし、current捕捉ファイルをoverlayする。8-commit compare内の変更script/schemaが全てcapturedであることもassertする。未変更supportの流用は今回のcompareに基づき、旧candidateのpatch bytesを混入させない。import時のpycache出力は止め、fixtureはtemp directoryに作成してcleanupする。Gitコマンド/Git-aware test/外部workflowを呼ばず、親Gitへのfixture object/ref生成は今回行わない。

| witness | 観測 | 証明の限界 |
|---|---|---|
| reader binding | 合成review/JSONを固定してprimary TeXとmanifest hashを変更してもgate生成・再検証PASS | 全stage advance/最終review/Human Gateの突破ではない |
| drift対照 | review済みJSON自体のbytes変更は拒否 | 実reviewの内容品質を判定しない |
| pre-TeX coverage | frontmatter.lede変更でrender TeXが変わり、review input hashは同じ | projection/render関数。空packageのfixture、全publisher CLI未実行 |
| audit scope | TeX/Bib不変、architecture_coverage.detailだけでblocking | 実W34を再生成/再lintしたものではない |
| Freeze artifact set | schema-required visualをextraとして拒否 | current `_current_artifacts`関数。前回は実Stateからの全接続fixtureで再現済み |
| approval type | 実W34 pointer hash一致のHuman approvalはStage schemaで拒否 | current `_prior_artifacts`が使う型の反例。全current State実行ではない |
| historical W34 | 実Release checkpoint pointer hash一致、新Stage schemaで受容 | report/State依存閉包、全旧号互換、PDF/public asset未検証 |

最初の二回はprobeが`semantic_review_path`にPath objectを渡して`repo_local_path`のstring契約で停止した。実関数を変更せず、上流test helperとreader builderと同じpersisted `semantic_authority`経路を使うようprobeを修正した。その後の一回で全witness/assertを完了。このsetup修正をproduction修復や不整合解消として数えない。Path入力/CLI経路全般を検証したとも言わない。

review PASS、profile/architecture/Human approval等の合成入力はtest fixtureであり、実Human/非著者reviewではない。レビュー内容を自動生成してproductionへ渡すツールではない。probe結果中のPASSEDは一部は問題となる受容の観測で、「全品質test成功」を意味しない。

## 終了時の境界

今回のrootによるcurrent-source限定reviewは完了。旧patchの独立review、修復差分の新実装、production adoption、全workflow retry、全profile/歴史実行、純費用測定は未実施。現時点で追加の全test再実行/Issue履歴探索の判断価値は低いため止める。次はassessment §4の二つの保守単位を順に扱う。新agentは別途明示許可、production投稿/変更も別権限。通常Pull/Push/最終commitはHuman。
