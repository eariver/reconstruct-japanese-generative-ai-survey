# Evidence受理のstaging試作と採否判断

日付: 2026-09-12 JST  
状態: **BOUNDED PUBLICATION EXPERIMENT COMPLETE / OUTER WRAPPER NOT RECOMMENDED / NO ADOPTION**

全体再評価による更新: [J-GAS全体方針再評価](astra-system-direction-reassessment.md)が次の優先順位を置き換える。本書§6の「内部案を次に1つ試す」は保留し、研究・編集・review・repairを通した品質/総仕事量比較を主経路とする。下記の試験結果は固定Evidenceとして保持する。

## 1. 結論

**package/task/Cardをprivateな作業領域へ固定し、完成後に公開する性質は有効だった。ただし、今回の「既存accept関数の外側を包むwrapper」は採用候補から外す。** 理由は、既存のhistorical accepted再入を壊し、同じEvidenceの全再検証を追加して費用を増やすためである。これらを隠して「安全なstagingが完成した」とは扱わない。

前回のCard bytes試作に対し、今回次を具体化できた。

- package/taskが検査後に差し替わっても、固定した元bytesから正常なacceptedを作れる。
- result書込み、acceptance manifest書込み、公開処理の例外では、新しいcanonical runを残さず終了できる。
- 既存の完全runを再利用し、壊れたrunや空directoryとの衝突は上書きせず拒否できる。
- しかし、accepted packageをprivate input directoryへ移すと、既存historical basis wrapperが必要とする隣接acceptanceを失う。従来通る再入が`state_sha256` driftで拒否される。
- 全検査を最後にもう一度行っても、検査後・公開直前のRaw変更は防げない。増えた検証費を全closureの不変性保証とは交換できていない。

**architecture上の修正は「外付けwrapperを増やさず、既存Core内部の保存処理に境界を置く」へ絞ること。** 入力元のauthority identityやhistorical admissionを保持したまま、検査に使用したpackage/task/Card bytesと出力物を結び付ける必要がある。単純なvalidator cache、永続PASS registry、新しいsemantic DSLは引き続き採らない。

## 2. 試作の範囲と固定根拠

対象sourceは前回と同じ`005e59841272464307386abfc11f5b09228f0814`の[phase6 export](../notes/phase6-lab-manifest.json)。今回upstreamを再観測していないので、新しいcurrent mainの確認結果とは呼ばない。production repositoryへはアクセス・書込みせず、既存exportをLinux temporary directoryへcopyして使用した。

[実装変換script](../notes/phase8_staged_acceptance.py) / [実験用差分](../notes/phase8-staged-acceptance-proposal.patch)

差分のbaseは**phase7のCard bytes補強済module**。baseline mainへ直接適用するpatchではない。構成は以下。

1. package bytesとtask metadataを取得し、taskのexact filename setと各task bytesのSHAを確認する。
2. destinationと同一filesystem上のprivate temporary directoryへpackage/task/Cardをcopyする。
3. 元のaccept処理をprivate inputとprivate accepted rootで呼ぶ。
4. 完成したprivate acceptedを既存validatorで再検証する。
5. digest名のdirectoryをLinux `renameat2(RENAME_NOREPLACE)`で公開する。既存targetは置換せず、完全な同一runなら再検証して再利用する。

Raw、manifest、contracts、Profile、Stateの全closureはsnapshot化しない。Linux以外や`renameat2`を利用できない環境ではfail-closeする試作用実装であり、portableなproduction実装ではない。Pythonの通常renameで既存空directoryを置換する挙動を避けるためにnative primitiveを使用したが、これ自体も追加の保守費である。

## 3. 実行結果

[probe](../notes/phase8_publication_probe.py) / [結果JSON](../notes/phase8-publication-results.json)

比較相手はphase7 Card bytes試作。2 Cards / 2 Supplement sourcesのThematic fixtureで、関数間に変更・例外・directory衝突を注入した。追加比較20ケースとphase7から引き継いだ9ケース、計29ケースを実行した。これは実OS並行writer試験、trusted workflow、stage/checkpoint試験ではない。

| 条件 | phase7 Card bytes試作 | 外側staging wrapper |
|---|---|---|
| 正常入力 | 受理・再検証成功 | 同左。acceptance SHA一致 |
| 1件目のCard検査後にpackage変更 | 変更後packageを保存し、後続再検証で拒否 | 元package bytesを保存・再検証成功 |
| 同時点でtask変更 | 変更後taskを保存し、後続再検証で拒否 | 元task bytesを保存・再検証成功 |
| result書込み例外 | 不完全なcanonical digest directoryが残る | 新しいcanonical runなし |
| acceptance manifest書込み例外 | 同上 | 同上 |
| 同一入力で再実行 | 既存runを再利用 | 同左、既存bytes不変 |
| 壊れた既存accepted | 拒否し、既存bytes不変 | 同左 |
| historical acceptedからの再入 | 通過・同じrunを再利用 | **拒否。互換性退行** |

staging固有の4ケースも確認した。

- publish関数の例外: 新しいcanonical runなし。
- publish直前に空targetが出現: 拒否し、その空directoryを置換しない。
- 同一の完全runがtargetへ先に出現: 再検証して再利用する。
- publish直前に同じ長さの別Raw bytesへ変更: **受理を返し、その後の独立再検証でRaw SHA drift**。

全追加ケースでStateは操作前後不変、既存runを持つケースではその全file bytesが不変。失敗時に空のaccepted rootが残る場合はあるが、新しいdigest runを公開したとは数えない。衝突ケースのtargetは試験が外部writer役として作ったものなので「runなし」とは報告しない。private working directoriesは通常終了・注入例外からのunwindでcleanupされた。process kill、電源断、disk durability、cleanup自体の失敗は試験していない。

引継ぎ9ケースでは、4つの構造反例の受理前拒否、2つのCard差し替えで元bytes保持が継続した。最後のCard検査直後のRaw変更は、追加された完成物再検証が公開前に検出した。ただし上記の「その再検証後の変更」では依然受理を返す。検査時点が後ろへ移っただけで、closure全体がimmutableになったのではない。

新staging実装で既存Evidence unit testsの12試験も成功した。**unit testsが成功しても、追加のhistorical再入試験は失敗した。** 全Core regression、実Weekly/過去409 Cards、独立semantic品質の証明はない。

## 4. Historical再入の退行が示すもの

既存`survey_agent_tool_v2._historical_state_basis_wrapper`は、accepted packageに隣接するacceptanceを読み、そのpackage SHAとのbindingを確認してから現在のState basisを検査する。これは単なるpath解決の都合ではなく、旧acceptedを新しいStateの下で使うことを認める条件である。

試験は、syntheticなacceptedを作り、State JSONへ改行を追加して**意味を変えずbytes SHAだけを変更**し、そのaccepted package/resultsから同じrunへの再入を行った。既存EvidenceとScreeningのhistorical wrappersを両方適用した場合、phase7版は通り、再検証も通った。staging版ではprivate `input/package.json`の隣に元のacceptanceがないため失敗した。

これはactual stage進行やHuman Gate変更の試験ではない。fixture implementation identityのまま、既存のhistorical basis経路を狙った互換性試験である。current-stage runtime全体のidentity admissionを代替していない。

private inputへacceptanceもcopyすれば当該エラーだけを消せる可能性はある。しかし、どの元accepted identityを検証・保持するのか、コピーした場所のresult setやdirname identityをどう扱うのかという責任が増える。**staging wrapperを成立させるためだけにauthorityの見せかけを再現する方向へ進めない。** 既存の入口でauthorityを解決し、内部の保存処理だけを分離する方が、小さい保守候補として比較する価値がある。

## 5. Total lifecycle費用の判断

正常2件で、accept呼出内のCard validationは2回から4回、Supplement全体検査は3回から6回に増えた。既存Coreを包み、完成物のfull revalidationを追加したことによる確定的なwork増である。

| synthetic受理 | phase7版 | staging wrapper |
|---|---:|---:|
| 2 Cards | 0.061秒 | 0.121秒 |
| 16 Cards | 0.432秒 | 0.899秒 |

各1回の小規模計測で、fixture生成費は除外。順序やcacheを制御したbenchmarkではなく、W34の実行時間へ外挿しない。それでも、前回見つけた重複検査をさらに増やす実装だというcode/countのEvidenceとは整合する。

機械時間だけでなく、Linux native publication primitive、private inputの新しいpath制約、historical bindingの再表現、cleanup、memory/diskコピー、診断箇所が追加される。得られる部分書込み防止は価値があるが、**この実装構成のままtotal lifecycle workを下げる根拠は得られなかった**。よって外側wrapperの採用・拡張、historical wrapperへの特例追加は進めない。

維持するのは性質と反例である。

- 検査に使用したpackage/task/Cardのbytesからのみ出力を作る。
- 公開する前に、完成した出力と検査対象のbindingが一致している。
- 同一digestの既存runを破壊しない。不完全runの残骸を通常の失敗で増やさない。
- 旧acceptedの再入条件を保存場所の変更で失わない。
- 追加のfull validationが何を保証し、何を保証しないかを明示する。

## 6. 次の判断単位と停止条件

**次回の機械的保守は1つの内部案に限定する。** 既存入口で元package/acceptedのauthorityを検証し、そのidentityを保ったままpackage/task/Cardをbytesへ束縛し、既存acceptの最終保存部分だけをprivate staging→公開へ分ける案を比較する。外側へ別のaccept loopやfull revalidation loopを追加しない。Raw共有は同梱しない。

採否を変える最小試験集合は今回のpackage/task変更、3種の書込み・公開失敗、完全/不完全runへの再入、historical再入、phase7の4反例とCard差し替えである。正常出力の同値性と元artifact不変、呼出回数・保持bytes・必要な回帰を併記する。authorityを省略するflag、任意callerが渡すvalidated dict、既存acceptedへの無言backfillは解決策にしない。

この内部案でも大きなauthority再設計や追加の全再検証が必要になるなら、機械的staging実装をここで保留する。前回の構造補強とCard bytes補強を限界付きの小さい保守案として整理し、次の主作業をsourceの問いの具体化とomission評価の設計・比較へ移す。これにより、性能・安全実装だけを際限なく掘り続けない。

独立semantic review、fresh source authoringの品質、operator/Human修復負担の実測は今回も未実証。今回の29ケースやunit PASSからそれらを改善済みにしない。Phase番号ではなく、上記の採否・停止条件を次の範囲として使う。

## 7. 再現・継続

```text
PYTHONPATH=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/.phase4-linux-deps python3 -B notes/phase8_publication_probe.py
```

phase6 fixed export、phase7 fixture/変換script、前回Linux依存を使用する。各armは独立temporary snapshot・別processで実行し、source module SHAをJSONへ記録する。試験用patchと結果はreconstructに生成する。結果JSONのhistorical退行は期待した観測値としてassertしてあり、全採用条件がPASSしたという意味ではない。

**decision surface:** privateな保存と公開の分離が何を改善するか、単純wrapperが既存authority経路をどう壊すか、費用がどこで増えるかまで実行で確認できた。外側wrapperを採らず、内部保存境界の1案だけを比較する／成立しなければ別の品質作業へ移る判断を残して、この単位を終了する。

次回は本書§1・§4・§6から。前回の[bytes所有権判断](astra-byte-ownership-and-sharing-decision.md)は履歴として保持する。production adoption/migration、State、Human decisions、Gates、Freeze、Release、production repositoryの書込み、通常Git Pull/Push、reconstructのcommitは行っていない。
