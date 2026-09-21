# Re:Phase 1 — B3 reader responsibility boundary

2026-09-21 JST

**B3の修復範囲を再評価し、限定実験と実装契約を作成した。B3は未解消、f1は不変、全候補はNOT_READY。** productionへの変更や採用は行っていない。

## 分かったこと

B3は`frontmatter.lede`の追加だけでは直らない。現在のWeekly rendererはpublication input・Architecture plan・Draft spec・Draft resultから出力する一方、review用JSONはその一部だけを投影する。rootの[限定実験](../notes/rephase-1-reader/probe-results.json)では、10種類の変更がTeXを変えてもreview対象hashを変えなかった。

- 表紙anchors、前書きheading/lede/scope notes、最終summary heading、section label、生成済Claim Boundaryの7箇所。
- 表示日と期間境界。
- citation key。これは本文の語句とは区別した引用・生成identityの反例。

headlineとsummary paragraphの2対照では両方のhashが変わるため、projection自体が動作していないという結果ではない。単一合成packageで実関数を比較した証拠であり、10件の実号品質不良や全workflow突破を実証したものではない。

さらに、全renderer入力をreview対象へ入れて再生成比較する試作では、異なるTeXや不完全なreader projectionを拒否できた。一方で、本文に関係しないDraft内部注記の変更もreview対象hashを変えた。現rendererがDraft result全体のhashをTeXコメントへ入れるためである。**この試作をそのまま採用すると不要なsemantic再reviewを増やすため、実装候補にはしない。**

## 選んだ修正方針

Weeklyは、全reader内容を持つ一つの入力をreviewし、その同じ入力から出力する構造へ寄せる。Gateの作成時・再検証時に実際の生成対応を確かめる。単に自己申告の`rendered_sha256`を追加したり、毎回二度目のTeX reviewを課したりする案は選ばない。

既存のdirect-primary review経路は別に扱い、review対象がmanifestの実primary sourceと同じpath/bytesであることを求める。LONGFORM_SPECIALにWeekly用の構造を無条件に課さない。この経路が存在することは、Special/manualの全実行が検証済みという意味ではない。

reader内容、生成・来歴情報、bibliography/style/supportの責任を[実装契約](../notes/rephase-1-reader/contract-decision.md)へ具体化した。内部コメントなどは任意TeX注入を許さない制限付き生成情報として扱う。bibliographyやsupporting TeXも意味や表示へ影響し得るため、primary-onlyの実験から全reader coverageを認定しない。既存manifest等を優先し、新しい台帳や万能resolverへ広げない。

WorkerとAuditorのsource確認から、stageが選んだexact Reader ManuscriptとGateの接続も契約へ追加した。同じissue/ProfileのGateであるだけでは足りない。構造化JSONのschema不正を黙って読み飛ばす現在の経路も、derived-input経路ではfail-closeにする。いずれも今回実装したという主張ではない。

## 独立性と限界

rootは元の反例とf1 sourceを読み、実験と契約を作成した。別のfresh-context Sol Workerが[callsite・責任範囲](../notes/rephase-1-reader/worker-analysis.md)を調査し、さらに候補作成に参加していないfresh-context Astra Auditorが[独立design review](../notes/rephase-1-reader/auditor/review.md)を担当した。いずれも実研究・編集・Human判断や最終七観点auditの代わりではない。

Auditorの指摘により、内部注記の初期対照がschema外のtop-level fieldだった点を修正した。初期code/resultsを保存し、schemaが許す`publication_extensions`内の注記で再実行して同じ関数上の費用問題を確認した。fixture全体は完全なpublisher入力ではなく、実CLIで不要な再reviewが起きた実測とは区別する。

初期Auditorはreport/input hashesを保存後に利用上限で停止したため、別のfresh-context Sol Auditorへ対応確認だけを依頼した。[独立した対応確認](../notes/rephase-1-reader/resolution-auditor/review.md)は、証拠の限定とexact Manuscript接続の2指摘をdesign/evidence上で対応済みとした。B3実装の受入や七観点PASSには変換しない。

f1とB1/B2の24件PASSは元のscopeで保持し、再試験していない。今回の証拠はfunction/design experimentであり、新しいproduction候補の実装回帰PASSではない。元r2、a1、f1、過去のreview/失敗記録は保持する。

## 停止地点と継続条件

今回は**B3の境界設計単位**を閉じる。1フィールド修正では不足し、全入力を束縛する近道には再review費用の欠点があると実証できたため、未整理の契約を候補コードへ固定しなかった。これは新たな許可待ちではなく、rootによる範囲判断である。

採用経路を続ける場合、次はbibliography/supporting-sourceと非reader provenanceを既存責任へ割り当てたうえで、canonical reader input・renderer・Gateの一貫した最小修復をf1の隔離後継へ実装する。projectionだけ直してB3完了としない。反例の拒否、direct-primary互換、pre-materialization停止、既存stage/revalidation接続を検証し、fresh独立implementation reviewへ進む。新候補には後続のdiagnostic・同期・fresh七観点auditが必要。

r2の便益のためにCore全体の修復を無条件に引き受けない。支持できる責任境界が大きくなる場合は、この採用経路に必要な投資とreconstruction全体の目標を再比較する。純lifecycle削減は未実測で、移された作業を削減とは数えない。通常のreconstruct最終commit/Pull/Pushとproduction採用はHumanの領域に保持する。
