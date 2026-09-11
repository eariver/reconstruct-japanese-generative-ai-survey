# 検証bytesの所有権と共有案の判断

日付: 2026-09-12 JST  
状態: **CONTROLLED INTERLEAVINGS TESTED / SHARING NARROWED / NO PRODUCTION ADOPTION**

継続更新: [staging試作の採否判断](astra-staged-acceptance-tradeoff-decision.md)でpackage/task固定・公開失敗・historical再入を検証。外側wrapperは互換性退行と費用増のため採らず、次の範囲と停止条件を同文書§6へ更新した。

## 1. 結論と前回からの修正

**Supplement検証結果の単純な操作内cacheは採らない。先に検査・hash・保存が同じbytesを使う受理境界を整える。** 前回の「単一操作へ共有を閉じる」は必要な制約だが、それだけで安全にはならなかった。

固定main `005e59841272464307386abfc11f5b09228f0814`の隔離Coreで、最初のCard検査後にSupplement Rawを同じ長さの別bytesへ変更した。現行処理と前回の構造補強版は2件目のCardで拒否した。一方、操作の終了時に破棄するprivate cacheでも、Supplement検査を1回へ減らした比較版は受理を返した。次の独立再検証ではRaw SHA driftになった。**永続cacheを避けても、live pathを検証済み不変basisとして使えば、既存の拒否を失う。**

併せて、Cardの検査後からhash/copyまでの間にbytesが変わる問題を実行で確認した。前回のstructural hardeningは不正Cardの検出を補強するが、検査したCardと保存したCardが同じであることは保証しない。

今回の最小試作は、前回のhardeningに**Card bytesの単一読込・そのbytesのdecode/検査/hash/保存**だけを加えたもの。正常時のacceptance hashはbaselineと同じ。2つのCard差し替え条件で検査済みの元bytesを保存し、その後の独立再検証も通った。4つの構造反例の受理前拒否は保った。ただしpackage/task/Raw全体のsnapshot化やatomic publicationは解決していない。

よって方針は、A+ canonical直接authoring＋既存Coreの狭い境界補強を維持し、**性能共有は条件付きの後続へ縮小**する。新しい永続authority registryやsemantic DSLを導入する根拠はない。今回、production性能改善や採用準備完了を宣言しない。

## 2. 所有権をどこまで確認したか

対象は前回exportの固定main。今回はproduction refの再観測やPullをせず、前回の[reality記録](../notes/phase6-production-reality.json)と[Git blob検証済manifest](../notes/phase6-lab-manifest.json)を使用した。以下はそのrefでのcode読解である。

| 経路 | 確認した性質 | 保証として使えないもの |
|---|---|---|
| `run_evidence_v2_interactive.py` 約626–681行 | `TemporaryDirectory`でpackage/resultsを作り、Core accept直後にacceptedを再検証する | repository配下のSupplement manifest/Rawまでimmutableになったという保証 |
| `survey_agent_tool_v2.current_stage_basis_override` 約122行 | State/Screening/Evidence verifierをcontext中だけ置換し、終了時に戻す | filesystem lockやRaw所有権の取得ではない |
| `survey_evidence_v2.accept_evidence_results` 約1059行 | Card load→validate→file hash→後のcopy2。package/taskもpathから複数回読込。最終run dirへ順次書込 | 検査bytesと保存bytesの同一性、失敗時のatomic publication |
| `validate_evidence_acceptance` 約1116行 | acceptedのbinding/result setを再検査 | 過去に返したacceptの正当化や既に書いたdirectoryの自動撤去 |
| stage validator 約224行 | 下流でもEvidence acceptanceを再検査する | 最初の受理関数が不正bytesを保存しないことの代替 |
| operator bridge workflow 21–24行 | event/comment/PR/head等でconcurrency groupを作る | local helper内の全reader/writerを拘束するedition-wide Raw lockとは認定できない |

指定経路の読解で、Supplement closureの排他的所有権を証明できなかった。これは全runtimeのlock不存在の証明でも、実運用で並行writerが存在するとの主張でもない。trusted transport/権限の正当性と、関数が読むbytesの不変性は別の確認項目である。

## 3. 実行した比較と結果

[probe](../notes/phase7_ownership_probe.py) / [fixture](../notes/phase7_fixture.py) / [結果JSON](../notes/phase7-ownership-results.json)

既存test helper由来のThematic fixtureで、2 Cards / 2 Supplement sourcesを使用。各caseは別のtemporary repository。validatorのreturn直後、またはresult-set digest計算後・copy前へ変更を注入した。validatorは実際に呼ぶ。OS thread、外部writer、GitHub workflow、stage/checkpointの実行試験ではなく、**読込順の意味を確認する決定的なinterleaving試験**である。

比較は4 arms × 9 cases = 36ケース。

- baseline: current固定main無改変。
- hardened: 前回のstrict JSON/schema/exact targets補強。
- unsafe_memoized: hardenedのSupplement loaderを、操作内のroot＋package内容をkeyとするprivate cacheに置換。これは意図的な比較対照で、proposalではない。返却dictもdeep copyしており、callerによるdict変更を防ぐだけでは足りないことを問う。
- card_byte_bound: hardened＋今回のCard bytes試作。Supplement検査の回数は削減しない。

| 条件 | baseline | hardened | unsafe memoized | Card bytes試作 |
|---|---|---|---|---|
| 正常入力 | 受理・再検証成功 | 同左 | 同左 | 同左、全armのacceptance SHA一致 |
| 1件目の検査後Raw変更 | 受理前拒否 | 受理前拒否 | **受理を返す。後続再検証で拒否** | 受理前拒否 |
| 最後のCard検査後Raw変更 | 受理を返す。後続再検証で拒否 | 同左 | 同左 | 同左 |
| Card検査後にclaim.textを削除 | 変更後Cardを受理。後続再検証も通る | 変更後Cardを保存。後続再検証で拒否 | hardenedと同じ | **検査済み元bytesを保存・再検証成功** |
| digest計算後・copy前に同じCard変更 | 変更後bytesをcopy。後続再検証で拒否 | 同左 | 同左 | **検査済み元bytesを保存・再検証成功** |
| 事前missing target / duplicate target / missing text / duplicate JSON key | 4件とも受理 | 4件とも受理前拒否 | 同左 | 同左 |

受理前拒否の4構造反例ではaccepted root自体が未作成であることを確認した。全ケースでState bytesは不変。正常2件時のSupplement全体検査はbaseline/hardened/Card試作が3回、unsafe cacheだけ1回。この削減は**採用できる改善値には数えない**。

各armの環境で既存Evidenceの12 unit testsも成功した。計48回のunit-test実行だが、48種類の独立試験ではない。unsafe cacheはprobe中だけのwrapperであり、このarmの通常unit testsはhardened実装を試したもの。全Core regressionやcurrent productionの全409 Cards互換、Weeklyの差し替え試験はしていない。

## 4. Card bytes試作の責任範囲

[変換script](../notes/phase7_byte_binding.py) / [差分](../notes/phase7-card-byte-binding-proposal.patch)

**差分のbaseはcurrent main単体ではなく、前回phase5 structural hardeningを適用したmodule。** probeはその順序で構築し、結果にmodule SHAを記録する。productionへ直接適用する完成patchとは扱わない。

変更はCard専用decoderをbytes入力にし、accept中にCard bytesを保持して、そのdecode結果を検査し、同じbytesからhashを作り、そのbytesを保存する。accepted再検証でもCardを一度読み、そのbytesをhash/検査に使う。新schemaやcanonical fieldは追加しない。

差し替え時の意味は「呼出終了時点のcandidate pathが元通りである」ではない。**当該操作が取得して検査したCard snapshotを受理する**というもの。外部pathが後で変更されても、無検査の新bytesに置き換わらない。最新のcandidate pathとの一致まで要件にするなら別のadmission条件が必要になる。

未解決事項を明示する。

1. package/task、Supplement manifest/Raw、contracts/Profile/Stateの全closureは依然live path。最後のRaw検査後の変更は全armで受理を返した。現在の反復検査も完全なsnapshot保証ではない。
2. 受理directoryは依然順次書込。途中例外やdisk failureでの部分生成、既存directoryとの競合、atomic publish/rollbackは未解決。
3. Card pathのsymlink差し替え、read中の変更、package/taskの差し替え、巨大Cardによる保持memory、accepted再検証中の競合は未試験。単一readは全入力closureのatomic snapshotを意味しない。
4. Card全件bytesの保持は追加memoryを使う。streaming spoolや上限の要否はproductionの実サイズに合わせて選ぶ。Raw全件まで同じ方法でmemoryへ載せることは推奨していない。
5. 本試作はCard固有の保存整合を改善する実験で、sourceの意味・omission・Human承認の妥当性を改善した証拠ではない。

この切分けにより、phase5の「構造不正を受理前拒否する」と、今回の「検査済みbytesを保存する」を混同せずreviewできる。どちらかだけのPASSを完全な受理安全性へ換算しない。

## 5. 次の実行経路を縮小する

前回はSupplement共有の安全成立を最初に試すとした。今回はその最小のlive-path共有案が反例で不成立となったため、性能contextを拡張して埋め合わせる作業は止める。次の保守候補を**Evidence受理で検査した入力と公開するbytesを揃える境界**へ絞る。

次回の最初の問いは、既存runnerのprivate temp領域を利用し、package/task/Cardを固定したworking setから検証・保存し、失敗時にはacceptedを公開しない経路を、小さい変更で作れるかである。検証済みRawまで共有するには別途closureの不変性が必要なので、その未解決を隠してcacheを同梱しない。必要なstaging案はreconstruct内だけで試せる。

採否を変える試験は、package/task/Card差し替え、accepted既存runへの再入、途中書込失敗、正常時のbyte identity、phase5の4反例、変更した境界に必要な回帰と歴史互換である。full repository snapshot serviceや永続CAS、global validator registryを先に作らない。小さな保守候補の範囲に収まらないなら、限界を明示して別の高価値作業へ移る。

性能投資は次の条件で再開する。

- 使い回す対象が同じimmutable bytes/検査結果であることと、操作終了後の再検証責任を示せる。
- Raw/manifest/package/task/contract変更を含む負例で既存拒否を失わない。
- staging/読込/保持/診断/保守を含む費用が、反復検証削減に見合う。

schema compile再利用は引き続き独立した低scope候補だが、今回の受理bytes問題の解決にはならない。Architecture/Drafting間の共有やbatchingは後続のままにする。

品質側の未実証も残る。現時点では独立semantic reviewを実施しておらず、自分の再読をそれとして数えていない。受理境界を際限なく掘り続けないため、次の小さなstaging判断が終わった時点で、機械的保守の残課題とsourceの問い・omission評価のdecision valueを再比較する。現在のPhase構成を固定仕様にはしない。

## 6. 再現と継続

phase6固定snapshotと前回Linux依存を使用する。

```text
PYTHONPATH=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/.phase4-linux-deps python3 -B notes/phase7_ownership_probe.py
```

scriptはLinux temporary directoriesへsnapshotをcopyし、armごとに新processでmoduleをloadする。productionへ書かず、既存ignored snapshotも変更しない。結果JSON・Card差分を生成する。fixtureのimplementation identityはupstream test用であり、trusted runtime admissionではない。

**今回のdecision surface:** private操作内cacheでも拒否を失う具体的条件、前回hardeningに不足するbytes binding、狭い改善の実行結果と残る限界が揃った。これで性能案を縮小し、次の受理境界試作を定義できる。同じ2件fixtureのcaseを無目的に増やす段階ではない。

次回は本書§1・§4・§5から。前回の[共有判断](astra-validation-work-and-pr487-decision.md)の重複計測は有効な履歴として残し、「共有すれば安全に減る」という結論には進めない。production adoption/migration、production State/Human decisions/Gates/Freeze/Release、production repositoryの書込み、Git Pull/Push、reconstructのcommitは行っていない。
