# Profile/support upstream repair — pre-code readiness assessment

2026-10-31、Astra author-side判定。**PRE_CODE_READY（具体設計・interface map限定）**。独立readiness reviewとAstra確認を完了した。**このpre-code unitのHuman Commit Pointで停止し、実装は次のHuman continuation後に開始する。**

## 1. 正本・優先順位

1. [選択済み契約 INCLUDING §7](rephase-1-profile-support-contract-decision.md)：FULL SHA256 `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`、20472B。
2. [契約ROOT INCLUDING §5](../notes/rephase-1-profile-support-contract/astra-review-resolution.md)：FULL SHA256 `021a0d7ce696a1d386ff2accd803e97033a297872ea65a0d7646a9953ded217a`、7225B。両design reviewの選択限定判定と共に不変。
3. **[今回mandatory ROOT INCLUDING §7](../notes/rephase-1-profile-support-precode/astra-precode-gate-resolution.md)**：FULL SHA256 **`bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa`**、**20159B**。
4. **[独立readiness reviewのFINAL R5判定と§8 FINAL-BINDING ROOT確認](../notes/rephase-1-profile-support-precode/independent-readiness-review.md)**：FULL SHA256 `8ab81a2b158d3a9f35b5efcb5198ab18f9d94bdbac58bee2b6e5a967926bbdf0`、50891B。

具体mapは[packet](../notes/rephase-1-profile-support-precode/README.md)に整理した。R3の詳細inventory／mechanics、C-R2のliteral closure arrays、focused root-context mapを、**R4→R5→今回ROOT全文**で上書きして読む。初稿、NOT_READY、誤ったsource pinや未修正のfallback文は履歴として保存する。旧working ROOT `da37cb8d…`/13968Bは§§1–6だけであり、現全文hashではない。

## 2. 今回閉じた具体map

| 面 | 確定した境界 |
|---|---|
| DM016 | 既存canonical Evidence mapperへ選択済み10行を追加、旧行と元typeを保持。未知typeを新規Screening/Evidenceのwrite前に拒否。DROP予定も除外しない。v1 enums／補助SOCIAL／URL推測／default SECONDARYは変更しない |
| DM017 | 普通のinputはinitial3項目／named-only5項目、結果7項目は内部導出。U=initial∪named(root)∪named(effective)、全parent/OIDのcarrierを実parent_refsで確認。欠落はDECLARATION_LOSS。旧Completeness依存や自動充足なし |
| package前の根拠 | まだ存在しないpackageをresolverへ渡さない。State/Profile・marker・checkpoint provenanceを区別し、実Pathからroot/effectiveを導く。初期DIRECTとinitial valid-markerケースを保持し、claimed-root欠落はfallbackしない。ENOENTのみ不在 |
| 受付／再読込 | 新規runの直前に新規policy、既存content-addressed runは元の妥当性で再読込。共有historical expansion/content validatorへ新しい受付規則を混ぜない |
| DM022 HIGH | strict LIVE eligibility後、**最初のState COPYより前**に真のR/Eと新規policyを確認。adoptでもwrite前に再検証。DM022は既存7-field inputであり普通の3/5 gateを流用しない |
| DM022 LOW | before-State COPY→通常DCP/SCP→受理artifact→root JSONLとScreening effective basisを再読込。通常Stage CheckpointにPREARCH専用proofやLIVE State/completion validatorを適用しない |
| 通常checkpoint | schema/issue/producer/artifact/result/hash、exactly-one matching CORE_STAGE_CONTRACT、12-field reportを維持。record-owned Contract8/implementation、historical Stateはcanonical logical pathのみ。FILE SHAとresult-set digestは別 |
| パス引数 | LOWの4 builder APIsへ必要なrequest/COPY **keyword-only PATHを必須追加**。Optional NoneからLIVE Stateやbasenameを推測しない。前ECPはevidence provenanceでありDCPではない。adopted-fullは既存3引数でbound checkpointからCOPYを導く |
| parity／closure | direct/agent-firstは同じ普通builderへ。既存pure adapter helpersは互換維持、normal routeのmonkey-patchは廃止。limitationsはclosure-first＋不足residualを元順序で追加。closureは4 provenance/status counters＋1 status count＋3 operator-fed fields |
| source family | 既存G76 member集合を維持するmapを確認。HIGH/LOWはcanonical＋staged＋mapped7、Evidence/Screeningはstaged、interactive driversはcontrol-root束縛。コードbytes変更にはfresh CURRENT proofが必要。旧PASS自動転用なし |

新runtime module、schema、source-family IDは選択していない。必要な追加surfaceが実装時に判明したら正確な欠落箇所をAstraへ返す。単なる同じmembership件数、private dictionary、保存済みPASSはauthorityの代わりにならない。

## 3. Reviewで訂正した事項

- 初期A/B inventoryはhelper/API・最初のwrite・HIGH rootsが未確定、Cはclosure membershipとhashを誤記。独立reviewはNOT_READYを維持した。
- R2/R3は通常Discovery checkpointにPREARCH用検証を当てたり、LIVE-bound Screening関数をState-freeと呼んだりしていた。実sourceの通常checkpoint/report predicatesへ訂正した。
- root/effective、COPY、前ECP、FILE SHAとresult-set digestを区別し、全LOW/HIGHへの伝播を具体化した。LOWのpublic APIへcaller supplied record collectionsを足す案は不採用。
- residualの順序、closure8フィールドの由来、HIGH7と普通3/5の混同、absence判定、optional path fallbackを訂正した。
- R5で正しいfull source pinsと必須PATHを固定。独立FINAL R5はbounded PRE_CODE_READY、§8はROOT§7を含む全文へ最終確認を付した。

これは設計／interfaceの確認であり、実装の成功、runtime correctness、全Profile受入れ、独立七観点auditを意味しない。

[最終文書check](../notes/rephase-1-profile-support-precode/closeout-document-check.md)では現正本のfull hash・link・whitespaceを確認した。初期C JSONだけはextra dataでparse不能のまま、拒否済み履歴として保持する。現行のC-R2/R4/R5を含む他8 JSONはparseでき、初期Cを実装用machine inputにしない。以前の一括JSON-valid表現を引き継がない。

## 4. Sourceと作業境界

Read-only final133は `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate` を使用。actual409/tree8ce＋133paths54M79A/768、完全DIRECT409 patch `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260` /4931836B、manifest `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` /185422Bは不変。

今回はsource-readと文書／JSON・hashのdata処理だけ。source編集、project import、runtime/test/build、fixture、復元、network、普通のCommit/Push、Human Commit readbackは実施していない。前unitの4固定GETは完了済みcaptureを再利用し、DATA Pythonは非実行。取得権限は常設refresh権限ではない。

既存55 Gitlinks/child dirt、partialDB/missing26309/bulk31466、runtime/TeX非同梱、過去のqualified compositeと証拠欠落の限定を引き継ぐ。今回full133/768/inode再認証をしたとはしない。必要な資料の追加読取でsource可用性を確認した範囲に限る。

## 5. 次のHuman continuation — whole upstream implementation

GeneralがROOT§7.2に従い、独立final133由来workcopyで **canonical10／全新規受付preflight／普通3/5→7／root-effectiveのcurrent・historical束縛／adapter parity／DM022真のR/E対応** を一体として実装・検証する。役割別の並行担当と固定実行snapshotを使い、Astraは差分・raw・scopeをreviewする。

必須検証は全10typeと既存type、unknown/DROP早期拒否、三research Profiles、many-to-many/shared-OID、正当なDIRECT/DERIVED、missing/extra/duplicate/dimension/status/ref不整合、direct/agent-first同一出力、old-history-valid対new-admission-refusal、guard/no-overwrite/idempotence/partial-failure、DM022 repeatと後続consumer・own-epoch/CURRENT proofを含む。単独helperや件数だけの完了を認めない。必要追加dependencyや契約矛盾はcodeを広げる前にAstraへ返す。

その後の非四系列Thematic／Retrospective complete-reader＋normal correction契約は**必須後続gate**。Manual DIRECT_PRIMARY/PRIMARY_ONLY維持はその代替ではない。代表的品質、固定candidate/audit、Human採用・実運用、実測削減は未完了。

**WholeNOT_READY / step4B3OPEN / audit未開始 / DM021+022OPEN。Human Commit Pointで停止し、次unitを自動開始しない。**
