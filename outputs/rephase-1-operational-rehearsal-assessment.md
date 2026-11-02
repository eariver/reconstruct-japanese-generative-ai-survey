# W34＋efficient-LLM 実資料rehearsal — 中間評価と次の修復

2026-11-02、Astra author-side。**RehearsalはPARTIAL、R4はNOT_READY。** 実データでpre-Architecture工程を試し、次の投資判断に必要な運用・品質・費用の問題を特定した。今回のbounded評価をcloseoutし、Human Commit Pointで停止する。全rehearsal完了とはしない。

## 1. 入口

- [Packet／許可・現在状態](../notes/rephase-1-operational-rehearsal-20261101/README.md)
- **[Mandatory Astra resolution全文](../notes/rephase-1-operational-rehearsal-20261101/astra-rehearsal-resolution.md)**：実測と推定、取得・review・実行の限定、次修復の条件。
- [独立scaling review](../notes/rephase-1-operational-rehearsal-20261101/reviews/evidence-scaling-independent-review.md)、[独立closeout review（FINAL-BINDINGを含む判定は同書）](../notes/rephase-1-operational-rehearsal-20261101/reviews/independent-rehearsal-closeout-review.md)、[closeout check](../notes/rephase-1-operational-rehearsal-20261101/closeout-check.md)。独立確認・文書checkは別artifactのcloseout条件であり、初稿のforward linkだけを完了証拠とはしない。

HumanはW34とSP-efficient-llm-2026を選択し、固定774／c8の対象資料、続いて指定17レコードの原文・版metadataの限定取得を許可した。Commit readbackは行わなかった。Codeはfinal138のまま、Productionは変更していない。

## 2. 実際に進んだ範囲

| | W34 | efficient-LLM |
|---|---|---|
| 実資料 | 固定774の修復済み最終版、Root369／effective439、409入力、正しいr2補助根拠428bindings／425 Raw | 固定c8のoriginal165 Discovery／160入力、15義務、広い12領域のThematic。compat projectionは比較資料のみ |
| 通常工程 | 新Profile/State、X再取込み、Discovery受理、実DERIVED Screening、独立review、typed advance | 同様の独立reviewと通常advance、canonical分類・普通3/5入力からEvidence/Views/Ledger/Completenessを生成 |
| 現在State | `CANDIDATES_NORMALIZED` | `CANDIDATES_NORMALIZED` |
| 残る阻害要因 | 実規模のEvidence生成が重複検証で完了せず終了 | 現accepted productsは根拠消費review CHANGES_REQUIRED。原文取得後の修正案はDATA draftで、再受理・新review未了 |

W34のroot-only interactive wrapperでは439入力を扱えなかったが、既存prepare/accept経路は正常なDERIVEDとして処理できた。粒度を369へ減らしたりCoreを増設したりはしていない。修復済み歴史baselineはW34 **41selected／7packages／12頁**、SP **112selected／9packages／66頁**。旧indexの1件選択やpackage数の混同は採用しない。

隔離workdirは `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work`、意味ある独立source commit `480823560c0c26ed2e5baa18e0e79a22b2839a27`。旧State/Gateのrollbackや新承認への読替えはない。まだSelection/Architecture dossier、Draft、新PDF、Human Gateへは到達していない。

## 3. R4前に必要と判明したこと

### W34：根拠検証の重複を除く修復

189MB級の補助根拠をtaskごとに繰り返し読む。実runは約14分で終了させた。**operatorの保存noteに転記された観測**は経過14分38秒時点で`rchar=228011353736B`であり、元のraw `/proc` dumpは残っていない。論理read量のtool-observed/transcribed evidenceで、実disk traffic・完走時間・独立perf traceではない。個別diagnostic時間も保存記録の範囲に限る。CPU処理が続いていたとの観測であり、deadlockとは判断していない。Canonical Evidence出力は停止時点で未作成だった。

入口だけでなく、accepted Evidenceの再検証を通してViews／Ledger／Completeness／履歴readerへ繰り返しが波及する。小さいfixtureの成功を実規模の費用・実用性へ移せなかった。Dataset間引きや検証省略は選ばない。

**必要修復conceptを選択：操作内で検証済みの情報を用いるprivate batch処理＋共通のcanonical実装。** 公開API・単独呼出し・Raw/manifest/task/State/Profileの境界検証・履歴/current分離・no-overwriteを維持する。Global cache、caller verified-dict、第三のvalidatorコピー、新schema/module/familyは選択していない。

ただし**implementation-readyではない**。短い具体interface/caller/境界mapをAstra＋独立reviewerが確認してからcodeへ進む。作者案の下流非反復・全taskでLIVE検証・code変更で必ずContract8変更という前提はROOTが訂正した。全影響closureを扱い、source epochの合法な継続可否も確認する。

### SP：現在の原文へ根拠を束縛し直す入力修正

現在の12 VERIFIEDのうち11件は、初回の部分captureだけではbody-consumptionを確認できなかった。追加取得と独立読解により、10論文の固定版、PRの完全な日付付きmetadata、HFの歴史READMEを確認した。残る5文書の歴史版は未確定。取得しただけではVERIFIEDにならず、publisher claim／scope／時点の限界を保った新inputとRaw bindingが必要である。

さらに、未受理のcanonical Ledger／Completenessが既に存在するため、普通runnerの単純再実行は上書き拒否となる。旧content-addressed runsは保持する。所有・参照・State/guard・退避を確認した限定manual recoveryが可能かを具体的に決める必要があり、cleanup APIがないことだけで新Core機能を必須化しない。まだ削除・移動・上書きは実行していない。

## 4. 費用・品質の結論と証拠境界

SPでは旧67件のsource-type projectionと最終7項目の手追記を用いず、通常経路で160件／15義務を生成できた。一方、資料移行、根拠の実読、独立review、wrong-epoch manifestの修正、取得不備・実行失敗・再引継ぎは実費である。**総工数削減・break-even・完成edition品質非劣化は未測定／未証明。**

固定資料の不足と、元の出版物が誤っていたという判断は別である。新しいコードの機械的成功も、現在の研究判断の妥当性とは別に確認した。W34は全12頁を後続の実画像点検、SPは66頁text＋明示14頁を視覚点検した範囲に限る。

探索担当の範囲外local checkout読取、P3の6空payload過大申告（P4で修復）、誤ったE normalizer／r1 manifest、hash種別・時刻・package数の混同、review control誤記、retry stdio喪失、provider失敗時の部分進行を保存した。新しい全面clean／全履歴復元／safe-rerunner証明にはしない。

## 5. 次のHuman continuation

**Generalのbounded Evidence scaling repair**を次単位にする。最初にROOT§4の短いprivate-interface／全caller／current-history／return-write境界／epoch／oracle mapを返し、Astraと独立reviewが確認後、選択修復を実装・影響検証する。実W34409完了と意味保持・late drift・standalone・affected LOW/history/readbackを証明し、完全配送・独立implementation reviewでそのunitのCommit Pointに止める。新しい汎用readerや広いpre-code周回は開始しない。

保存したSP修正案・原文・reviewを再利用し、必要なsame-stage owned-output recoveryを別の実運用条件として確認する。新sourceでのfresh startを通常訂正の証明にしない。Rehearsal再開後に必要な品質・正常訂正・費用を閉じ、それから一候補固定／fresh七観点audit R4→Human限定採用R5→実測効果と旧作業除去R6へ進む。

**Source final138不変、repair未実装。WholeNOT_READY / step4B3OPEN / audit未開始 / DM021+022OPEN / quality-adoption-savings OPEN。Human Commit Point。通常Commit/PushはHuman-owned、次単位を自動開始しない。**
