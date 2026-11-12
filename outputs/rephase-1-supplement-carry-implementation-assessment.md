# Re:Phase 1 — DM022 supplement carry修復評価

2026-11-07。**既存producerの補足資料引継ぎを限定実装完了（source/run composite）。** 正常HIGH prepare→adopt/resume/readback経路で補足資料を束縛し、変更対象外の研究内容を保持する修復を実装・検証・配送した。実W34/SPの保存Stateへの適用・内容訂正・Selection再開は次の作業であり、まだ実行していない。

読むもの: [packet](../notes/rephase-1-supplement-carry-repair-20261106/README.md)、**[Astra closeout全文](../notes/rephase-1-supplement-carry-repair-20261106/astra-closeout-resolution.md)**、[最終source確認](../notes/rephase-1-supplement-carry-repair-20261106/implementation-20261106T131722Z/final-binding-review.md)、同packetの独立closeout確認。

## 1. 修復内容

- requestの明示的なsupplement SizedRefを、COPYに束縛された実root/effective DiscoveryとScreening、Profile source_root、全Raw bytesに対して検証する。
- 既存package/taskに補足authority、contract/rule、task別source IDsを引き継ぐ。既存の補足を保持・置換する経路と、新規追加／補足なしの経路を区別する。補足を黙ってDiscovery-onlyへ落とさない。
- request／新package／manifestの参照一致をproofでも確認し、SHA・byte_count・元の期待pinを使って遅い境界のdriftを拒否する。
- 変更しないカード・Ledgerに加え、Edition Viewの理由文・注釈も保持する。受理集合のdigest変更を、未変更候補の意味変更の許可にしない。
- request recordsは非DROPの全DIDに**一度ずつ**対応させる。集合比較だけでは見逃す重複DIDも拒否する。

変更したruntimeは既存LOW/HIGHの2ファイル。既存schema・module family・CLIを維持し、公開bypass／verified-dict／global cacheや別のoperator producerは追加していない。Contract8は不変、実tool/sourceのSHAは変更される。

## 2. 最終配送

**actual409/tree8ceに直接適用する完全patch。141paths=57M84A／773 intended files。旧final139を内包し、旧patchを先に重ねない。**

`notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/`

| 成果物 | SHA256 | bytes |
|---|---|---:|
| `complete-supplement-carry-409.patch` | `171812f686c05d8494de8bd32a6c00e043dc5ff1aa7452204a8e35f16848600d` | 5532921 |
| `complete-supplement-carry-manifest.json` | `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c` | 202833 |

適用済みproof: `.rephase-1-editorial-runtime/supplement-carry-packaging-20261107T040903Z/proof-copy/candidate-partial-b40de60`。clean check0／apply0、全773のbytes・size・modesを作者／GEN／PROOFで照合。既存whitespace警告、partialDB missing26309／bulk31466、runtime/TeX非同梱の限定は保持。全履歴・全treeのhydrationやclean認証ではない。

作者workcopyの`5eef790b…`は、既存771 sourceの意味ある隔離root snapshotでありactual409 ancestryではない。配送の基準は別に保持した本物のactual409。通常shipping候補HEADやreconstruct Commit/Pushは作成していない。

## 3. 検証の実範囲

- 最終runtimeでfocused17、C-direct全7、A2選択3が別batchで成功。
- 正常HIGH経路のWeekly DERIVED／Special、補足の追加・保持・置換、未変更card/View/Ledger保持、誤束縛・遅いdrift・重複record拒否を確認。
- full-size構造fixture:409tasks/401 supplement-bound/428 sources、160tasks/28 bound/30 sourcesで、正常HIGH生成・adopt/readbackとaffected/unaffectedを確認。ただしこれは重複DID guard追加前のruntimeで実行した証拠。最後の差分はrecord cardinality拒否で、最終17件にはその正常系と追加negativeが含まれる。単一のfull-final-suiteとは呼ばない。
- 実`verify_renewal_source_proof`のWeekly CURRENT positive、**同じ保存proof**でのLOW byte drift拒否、復旧positiveを最終runtimeで確認。closure件数だけのassertionではない。Longform全経路や新PDFの証明ではない。

当初Cテストの古い遅いerror期待値、phase-pin不足、未変更View drift、重複DIDの抜けは原失敗と共に保存・訂正した。旧CURRENT／prefinal配送は保持し、最終sourceのPASSとして流用しない。原source red-controlのため保存済み旧proofへ一時test fileを追加・削除した逸脱も記録し、「旧proofに一切書かなかった」とは主張しない。

## 4. 現在の研究状態

実資料instance `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work` は**旧e84 runtimeのまま保持**した。W34/SPはともに`EVIDENCE_REVIEWED`、最新CP四refと受理済み成果物は変更していない。保存済み4-paper／SP4-record訂正DATA、Jev archive captureも未adopt。新Selection/Architecture、Human Gate、Draft/PDF、Production操作はない。

構造fixtureの409/160を、実資料の訂正・独立内容review・Human承認と混同しない。総role/token/実運用コストとnet savingsはUNKNOWN。

## 5. 次Human continuation後

1. 保存e84から新たな独立rehearsal copyを選び、最終773 sourceを正確に移して意味ある隔離実行epochを確立する。旧e84・Profile・State初期化480・既存CP／materialは保持し、手動repinやCANDへのrollbackはしない。必要な現在source/contract適合を実際に確認する。
2. W344-paper、SP4-record＋archive補足案を、現schema・元のtask targets・根拠scope・Raw/claim bindingに照らして再確認する。特に本文のliteral引用／Raw routingを実際のproof契約で検証し、架空Rawや本文にないclaimを補わない。
3. 修復済みの正常HIGH prepareでimmutable候補を生成し、外部の独立内容review、proof、adopt/resume/readbackで同じEVIDENCE_REVIEWED Stateの研究authorityを正当に更新する。その後Selection/Architecture準備へ戻る。canonical受理物の手編集、fake Human REQUEST_CHANGES、下位関数だけの迂回はしない。

**Human Commit Point。ここで停止し、通常Commit/PushはHumanに委ねる。** WholeNOT_READY／step4B3OPEN／auditunstarted／DM021+022OPEN／quality-adoption-savings OPEN。今回の独立確認は限定修復でありR4七観点auditではない。
