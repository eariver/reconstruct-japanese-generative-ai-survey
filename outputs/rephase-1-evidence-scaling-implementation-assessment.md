# Evidence scaling repair — implementation assessment

2026-11-04、Astra author-side。**BOUNDED IMPLEMENTATION COMPLETE（delivery-bound source/run composite）。実W34の409件処理を完了した。** 独立implementation review、完全patchの別DB適用確認、必要な実行証拠が揃ったため、このunitのHuman Commit Pointで停止する。

## 1. 正本

- [Packet入口](../notes/rephase-1-evidence-scaling-repair/README.md)
- **[Mandatory Astra closeout全文](../notes/rephase-1-evidence-scaling-repair/astra-closeout-resolution.md)**：source・runの範囲、失敗／逸脱、次task。
- **[独立final implementation review WITH FINAL-BINDING＋closeout確認](../notes/rephase-1-evidence-scaling-repair/final-implementation-review.md)**。
- [完全配送report](../notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/independent-packaging-report.md)、[closeout check](../notes/rephase-1-evidence-scaling-repair/closeout-check.md)。

短いinterface mapとROOT§6、独立確認後にGeneralが実装・検証し、Astraがsource/oracle/evidenceをreviewした。新しい汎用readerやcache基盤を作るunitではない。

## 2. 修復したこと

Evidence、ordinary runner、LOW research authorityの3既存runtimeを変更した。操作phase内のprivate contextと純粋なtask単位の参照で、taskごとの全補助Raw再検証を除去。カード生成／検査は一つのcanonical coreを共有する。

公開signature・単独呼出しの再読込・error順序、全manifest Raw closure、書込みとreadback returnのfreshness、guard/no-overwrite、current Stateとhistory/COPYの区別を保持。公開verified-dict／bypass flag／global・epoch cache／第三のvalidatorコピー／新runtime module/schema/familyは追加していない。検証を省略した結果ではない。

## 3. 実W34の結果

保存rehearsal48082356の**新しい独立copy**で、修復コードを意味あるsource commit **`e84a82aca000c990597ea8cf60f548e2ff187bd1`** として記録した。旧State初期化SHA、Profile、Contract8、DCP/SCPは変更せず、既存agent-first経路で継続した。

| 項目 | 実結果 |
|---|---|
| 入力 | Root369／effective439、409 records、428 bindings／425 Raw |
| 出力 | Evidence409、Views409、Ledger439行、Weekly3義務／LIMITED |
| State | `CANDIDATES_NORMALIZED`のまま。研究受理・Human Gateへのadvanceなし |
| 実行 | exit0、wall175.26秒、logical rchar増分45238986845B、user CPU約160秒 |
| 不変性 | 実行source771、旧State/Profile/checkpoints、SP状態、元rehearsalを保持 |

[実run packet](../notes/rephase-1-evidence-scaling-repair/real-w34-retry-20261103T172327Z/README.md)に同processのmodule/commit/byte binding、raw `/proc`・time、出力manifestを保存した。測定窓にはguardやin-run検証を含む。旧約228GB／14分38秒は転記観測かつ未完走なので、厳密なspeedup・disk削減・総工数削減率は主張しない。

49 VERIFIED等は入力の構造上のstatusを保持したもので、新しい原文確認／独立研究PASSではない。SPの根拠消費とsame-stage retryもこの完了では閉じていない。

## 4. 検証・完全配送

最終module **19/19**、別batchでProfile28／Evidence関連26／DM022 C7／A2選択5（全25ではない）／family6／graph・presence8／consumer3を確認。合算や全旧suite成功とはしない。Weeklyの実 `verify_renewal_source_proof` はCURRENT_PROOF_VALID、同じ保存proofでCURRENT code driftを拒否し、修復後に再成功した。初稿478チェックはclosure/file検査に限られ、この実proofと区別する。

完全DIRECT409配送は **139paths57M82A／771 intended files**（689 available base＋82new）。旧138を全て内包し、先に旧patchを重ねない。

- Patch：[complete-evidence-scaling-409.patch](../notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-409.patch)
  - SHA256 **`de0af9cbd58665dc632a53cee5a0605da30ba9cdd3dc63202268565ba9887d49`**、**5408065B**。
- Manifest：[complete-evidence-scaling-manifest.json](../notes/rephase-1-evidence-scaling-repair/source-packaging/final-20261103T174718Z/complete-evidence-scaling-manifest.json)
  - SHA256 **`c5a6b230c975dc94a45e651f48cd42687f84d060c65b37f49d9917ff1bf0f143`**、**202204B**。
- Available applied proof：`.rephase-1-editorial-runtime/evidence-scaling-packaging-20261103T174718Z/proof-copy/candidate-partial-b40de60`。

全139delta＋771のbytes/size/modesをCAND/GEN/PROOFで照合。Mode修正前のcheck warning、修正後check0、apply0、whitespace diagnosticsを保存。実W34はtest d486、配送は最終19の7b862305で、差はそのtest1fileだけ・他770一致。実行と配送はこの明示的compositeで束縛する。

初稿の検査配置／不十分test、実F5失敗、Views/HEAD testsの一時的配送漏れ、最初の実409のfacade外実行、CURRENT harness過大表現／fixture-local git config、toolchain setup失敗、委任先の不要なreconstruct HEAD読取をROOTで保存・訂正した。通常Commit/Push・Production変更はないが、全workerがreadbackしなかったとは記述しない。部分DB・非同梱runtime・旧55Gitlinksの限定も継承する。

## 5. 次のHuman continuation

**修復済みruntimeで保存した実資料rehearsalを再開する。** W34の成功409を件数のために再実行せず、現在出力の実質的なEvidence／authority-consumption reviewへ。SPは原文・修正案を保持し、未受理Ledger/Completenessの所有・参照・退避・guard条件を具体化してから通常の同stage訂正／再受理・独立reviewを進める。旧accepted runsを破壊しない。新instanceでのやり直しを通常retryの証明にしない。

必要Weekly/Specialの品質・正常訂正・費用を確認し、その後に一候補固定／fresh七観点audit R4→Human限定採用R5→実測削減と旧作業除去R6。Generic readerを自動で追加せず、必要Specialを暗黙に除外しない。

**WholeNOT_READY / step4B3OPEN / audit未開始 / DM021+022OPEN / quality-adoption-savings OPEN。Human Commit Point。通常Commit/PushはHuman-owned、次unitを自動開始しない。**
