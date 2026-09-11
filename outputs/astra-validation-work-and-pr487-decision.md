# PR #487後のbasis共有・検証workの判断

日付: 2026-09-12 JST  
状態: **CURRENT MAIN VERIFIED / WORK AMPLIFICATION MEASURED / NO PRODUCTION ADOPTION**

## 1. 今回の判断

**authority Coreとcanonical artifactsを維持する方針は継続する。ただし、次の実装検討を「Evidence境界補強＋schema compile再利用」だけに限定せず、同じ操作内の検証済みbasisの共有へ広げる。最初の対象はEvidence Authority Supplementの重複検査とする。**

PR #487はDraftingでroot Discoveryとeffective Discoveryを取り違える問題を、既存Screening resolverを共通loaderから再利用して修復した。別engineや新canonical modelを導入せず境界を整える方向と整合する。一方、修復記録にあるW34の大きな再導出費は、前回のschema単体測定より投資順に影響する。

今回current mainの無改変Coreで、N個のSupplement sourceを持ち全N個のCardがSupplementを利用するfixtureを測った。**1回のEvidence acceptance再検証で、Supplement全体の検査はN+1回、Supplement RawのhashはN(N+1)回**だった。これは安全検査そのものの削除を要する結果ではない。同じoperationの中で、検査済みの同一basisを捨て、Cardごとに再構成していることが削減候補になる。

今ここで決められるのは、次に試す境界と採否基準である。安全な共有の成立、W34全体の短縮率、operator/Human workの削減までは未実証。production採用候補が完成したとは扱わない。Phase番号による固定工程は設けず、以下の証拠依存で継続する。

## 2. Current production realityと差分の範囲

[観測記録](../notes/phase6-production-reality.json)はGitHubのPR/ref/固定refのStateをread-onlyで取得したもの。観測時刻はJSONのUTC、本文の日付はJST。

- [PR #487](https://github.com/eariver/japanese-generative-ai-survey/pull/487)はmerged。merge commitと観測mainはともに`005e59841272464307386abfc11f5b09228f0814`。
- 前回main `6d748a962d57beff89da7c1b20cb5a9a86c8e261`との差分は6 commits・3 filesのみ。`survey_drafting_v2_base.py`、新規8試験、修復checkpoint文書。Evidence、Screening resolver、schema、workflowの変更はない。
- `weekly/2026-W34-v2-work`の観測refは`601481acd9b82ee8fa0c2eb28a2ca28636165d60`。Stateは`ARCHITECTURE_ESTABLISHED`、architecture reviewはapproved、publication previewはpending、next actionは`stage:drafting-synthesis`。これはStateの観測であり、全Draft packageの実行成功やreleaseを示すものではない。

PR修復は、accepted Screeningのsibling packageをacceptanceのSHAへ結び、既存`validate_package_basis`と`resolve_effective_discovery_basis`を使ってeffective pathを取得する。callerがresolver認定のroot/effective以外を指定した場合は拒否し、Candidate Matrix再導出へeffective pathを渡す。ordinary Draftingとcross-package synthesisは共通loaderを通る。DIRECTのroot=effectiveも維持する。

PR本文・checkpointに残るmerge前の停止指示は履歴として読む。今回のHuman連絡と実際のmerged状態を上書きする現行指示にはしない。

## 3. Evidenceの更新

| これまでの判断／未実証事項 | #487後の扱い |
|---|---|
| root/effective不一致によるDrafting failure | この修復の対象。一般的な未解決backlogとして残さない。全production Draft成功へは拡張しない |
| Evidenceのmissing target・duplicate target・missing claim.text・duplicate JSON keyの4反例 | 対象実装が無変更なので前回の反例は反駁されない。今回4反例のstage実行を全件再試験したとは主張しない |
| Evidence共通境界補強patch | current exportへの`git apply --check`成功。前回の試験結果は前回refに属する。current mainの全統合互換性や採用の証明ではない |
| shared resolver/shared mechanical checks | #487は既存resolverを再利用する具体例を追加。全basisを新registryへ移す必要性は示さない |
| historical reproductionとactive eligibilityの区別 | 維持。過去bytes/当時のcontractを保持し、現在の継続可否は現在の検査で判断する |
| fresh sourceの品質・独立omission review・問いの具体化の効用 | 未実証のまま。Drafting修復やmachine PASSでは解消しない |
| schema処理系再利用の費用効果 | 局所Evidenceは維持。ただし次の性能検討をこれだけに限定しない |
| lease/staging、trusted runtime、並行性、検査bytesと受理bytesの一致 | 依然未実証。basis共有の設計で先に確認すべき条件になった |

前回の[stage・互換判断](astra-stage-boundary-and-compatibility-decision.md)は履歴として残す。A+ canonical直接authoring＋薄い共通補助という方向も維持するが、その実装順を本書§6へ更新する。Bのsemantic DSL、global semantic cache、独立した永続PASS registryを再導入する根拠は得ていない。

## 4. 費用について新しく分かったこと

### Upstreamで報告されたW34の費用

[固定mainの修復記録](https://github.com/eariver/japanese-generative-ai-survey/blob/005e59841272464307386abfc11f5b09228f0814/docs/checkpoints/core-v2-drafting-derived-discovery-basis-repair-20260911.md) §13–§18には、Screening 2.7秒、Evidence acceptance 325.2秒、Edition Views 336.0秒、Materiality 691.6秒、Completeness 651.7秒、Candidate Matrix再導出1915.0秒・409 rowsで一致、とある。**これはupstreamの実測報告で、今回独立にW34で再計測していない。** 呼出が入れ子なので、各秒数を独立費用として足し合わせない。

記録はこの大きな費用を修復前からのCore cost profileとしている。#487が30分規模の再導出を新しく生んだとは判断しない。また文書にはDraft derivationが1/7と2/7の記述が併存する。2件のPASS記載はあるが、今回の根拠を7件完走へ拡張しない。786 tests / skipped 6のfull-suite成功もupstream報告であり、今回のローカル試験数には含めない。

### 今回独立に測った機械的work

[実行script](../notes/phase6_validation_work_probe.py) / [結果JSON](../notes/phase6-validation-work-results.json)

current mainのunmodified Coreに既存Thematic test helperで隔離fixtureを作った。全Cardに1つずつ異なるSupplement sourceを結び、受理後の`validate_evidence_acceptance`だけを計測した。count wrapperは元関数を必ず呼び、検査のreturn valueを置換しない。fixture生成費は計測外。

| Cards / Supplement sources | Supplement全体検査 | Supplement Raw hash | synthetic elapsed |
|---:|---:|---:|---:|
| 2 / 2 | 3 | 6 | 0.026秒 |
| 4 / 4 | 5 | 20 | 0.042秒 |
| 8 / 8 | 9 | 72 | 0.074秒 |
| 16 / 16 | 17 | 272 | 0.161秒 |

呼出元も確認した。`validate_evidence_package_basis`がSupplement全体を検査し、taskへのexact bindingを確認する。しかし返却値はScreening acceptanceとtasksだけ。後続のCard loopが`task_authority_sources`→`_supplement_entries_for_package`を通って全Supplementを再検査する。source数とSupplementを使うCard数の両方に依存する重複であり、上表のN(N+1)はこの全件利用fixtureについての式である。

さらにcode上、Architecture basis loaderはEvidence/Views/Materiality/Completenessの各validatorを呼び、Drafting loaderはMatrix検査後にEvidenceを再検証する。これはstage間の重複がある根拠だが、今回その全呼出回数や割合は測っていない。**W34の325秒のうち何秒がRaw hashか、今回の1箇所の改善だけで何倍速くなるかは不明。** tiny Raw・小規模fixtureの秒数から409件の性能やproduction filesystemの費用を外挿しない。

各fixtureでState bytesは不変。終了前に1つのRawを同じbyte countの別bytesへ変更すると、次の独立再検証は`Raw SHA drift`で拒否した。これは現行検査のbaselineであり、未実装のcacheの安全性試験ではない。

PR追加8試験＋既存Evidence12試験、計20試験がLinuxで成功。source exportはcurrent Git treeに対して629 filesのGit blob SHAを検証し、旧snapshotと同一bytesの626 filesを再利用、差分3 filesを取得した。[manifest](../notes/phase6-lab-manifest.json)。旧snapshotをcurrentと名付け替えて試験していない。

## 5. 次に成立させる設計境界

最小の比較対象は**単一Evidence受理／再検証操作の中で、既に検査したSupplement basisをCard loopへ渡す内部経路**である。public acceptance API・canonical JSON・Gate・Stateを増やす必然性はまだない。compile済schemaの再利用は補助候補に下げ、stage横断や複数Draft package間の共有はこの境界の成立後に検討する。

設計で満たす条件は以下。

1. **入口で検証する責任を維持する。** acceptance/package/implementation/contract/Discovery/Screening/manifest/Raw/task bindingの検査結果を内部で一体として扱う。外部callerが`validated=True`や任意dictを渡して省略できる入口は作らない。単独Card APIが必要なら従来の検証を実行する。
2. **同じbytesを使う。** pathやmtime、package SHAだけではRaw closure全体の不変性を保証できない。immutableに保持した検証対象bytes/metadata、または実証した既存所有権・snapshot境界が必要。関数開始時と終了時のhash一致だけで、途中の差し替えまで排除したとは主張しない。
3. **共有範囲を1操作に閉じる。** privateなcontextを操作終了時に破棄する。次の独立操作では再検証する。永続PASS、cross-process cache、editionをまたぐ共有を前提にしない。Human decisionやsemantic sufficiencyを共有対象にしない。
4. **失敗時に受理を残さない。** task/card/Supplementの変更、missing/extra files、symlink、別package混入、schema/implementation変更、検証途中の差し替えを試す。検査に使ったbytesとhash/copy/acceptedに使ったbytesを追跡する。前回4反例を含むfail-closeを保つ。
5. **削減を検査省略と混同しない。** 同一closureは1回検査して再利用し、各Card固有のschema・exact targets・source/subject関係・result setは全件検査する。N=16でRaw hashを272回から16回程度へ減らせるかは試作の目標であり、現時点の達成値ではない。snapshot構築／再確認費も数える。

この条件が小さい変更で成立しない場合は、性能案を縮小する。schema処理系の再利用と安全境界の補強だけを独立した保守案として残せる。共有contextのために新しいauthority artifactや永続管理サービスを増やし、maintenance/Human handoffを重くする案は優先しない。

## 6. 改訂した実行順と採否基準

**次の1単位は、Evidence Supplementの内部basis共有が現行所有権の下で安全に成立するかを判定する仕事とする。** runner→stage→acceptanceの該当lease/staging/読み書き箇所だけを追い、必要ならreconstructの隔離snapshotで最小prototypeを作る。全Coreの再設計調査やW34の全Draft再実行を先行させない。

| 順序 | 決めること | 先へ進む条件／縮小条件 |
|---|---|---|
| 1 | 単一Evidence操作の所有権・bytes寿命と内部共有 | 同一検査対象の保証と4反例拒否が説明・試験できる。できなければ性能案を縮小 |
| 2 | 境界補強＋局所共有の採用候補 | baselineとの正常出力同値、tamper拒否、後継validator/過去bytes保持、fixture総費用と必要な回帰。安全patchと性能patchは比較・切戻し可能にする |
| 3 | Architecture/Draftingのbasis共有・package batching | 局所改善後も残る入れ子費用を測ってから選ぶ。state/Gate admissionは共有結果で代用しない |
| 別の品質判断 | sourceの問いの具体化・独立omission評価 | 前回paperと異なるfailureを持つsourceでauthor/reviewer/operator workを比較。独立評価の成立なしに品質改善を認定しない |

これは品質仕事を無期限に性能改善の後へ送る宣言ではない。1単位目の終了時に、残る機械的負荷と品質の未実証のどちらが次のdecision valueを持つか見直す。安全補強が性能試作の長期化を待つ必要もない。数値が改善しても、新しいcontext伝播・fixture維持・障害診断が費用を上回るなら導入しない。

Humanへ採用を求める段階では、具体差分、future edition/Profile/stageの適用範囲、旧acceptedへの影響、検査とbytesの関係、外す旧処理、rollback/invalidation、未解決の品質・費用を提示する。今回その承認は求めず、productionへの適用も行わない。

## 7. 再現と継続

Windowsの`python -B notes/phase6_prepare_lab.py`は固定GitHub treeから必要な6 directoriesだけをexportする。既存`.phase4-lab-snapshot`の一致bytesを再利用するが、それが無くても必要blobを取得できる。出力先が存在する場合は上書きしない。`python -B notes/phase6_capture_reality.py`は再実行時点のrefを新たに観測するため、保存済JSONが今回の観測根拠である。

Linux試験:

```text
PYTHONPATH=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/.phase4-linux-deps python3 -B notes/phase6_validation_work_probe.py
```

固定依存は前回と同じLinux環境。fixture implementation SHAはupstream test用の`4444...`であり、trusted production admissionではない。準備はproductionをread-onlyで読むだけ。snapshotと依存はignored、結果とscriptsはdurable。既存labの削除再試行はしていない。

**今回の停止理由:** #487の影響範囲、前回Evidenceの継承範囲、実際に重複する検査単位、次の安全設計と採否基準が揃った。同じtiny fixtureを増やしても所有権やsemantic qualityは解決しない。次回は本書§1・§5・§6と結果JSONから継続し、履歴全体を再読しない。

production adoption/migration、State、Human decisions、Gates、Freeze、Release、production repositoryの書込み、通常Git Pull/Push、reconstructのcommitは行っていない。
