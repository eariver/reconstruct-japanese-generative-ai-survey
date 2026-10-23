# R3 editorial operation — implementation assessment

2026-10-23 JST. **契約d880f53eの選択した統合操作をBOUNDED IMPLEMENTATION COMPLETE。** Weekly envelopeとTHEMATIC/LONGFORM_SPECIAL authored revisionについて、版付き準備→外部review入力→finalize→State参照activation→通常のPreview/Freeze/Releaseを接続した。

必須: [Astra closeout](../notes/rephase-1-editorial-operation-implementation/astra-closeout-resolution.md)、[独立final operation review](../notes/rephase-1-editorial-operation-implementation/independent-final-operation-resolution.md)＋[packaging supplement](../notes/rephase-1-editorial-operation-implementation/independent-final-packaging-resolution.md)、[実reader/visual inspection](../notes/rephase-1-editorial-operation-implementation/independent-final-reader-visual-inspection.md)。複数source/runの限定付き合成であり、単一の全suite PASSではない。

## 1. 実装した利用可能な操作

| 境界 | 成果 |
|---|---|
| prepare | 既存P1/P2R/P2V/P3Sを束縛し、disposable buildから実PDF/log/digest・manuscript・新receiptを準備。reviewのPASSは生成しない |
| external review / finalize | 供給されたsemantic/visual/QAを厳格再検証。exact reviewed target、Candidateと15role sealのpath＋SHAを照合し、Candidate完成後にsealを書く |
| activate / resume | 旧版を保持し、既存Stateのrevalidation pointerだけを切替。孤立したcomplete recordは通常activateで拒否し、明示resumeで全再検証。unknown Stateは保全 |
| normal consumers | active CandidateをState/stage/Preview/profiled Freeze/export等へ接続。固定Profile・canonical approval/Freeze/Manifest出力は維持 |
| repeat / history | 両routeの2回目prePreview訂正、prior version KEEP／State COPY、R1×2後の正しいcumulative canonical anchor、currentとhistorical readbackの区別 |
| failure / boundary | 書込み・close・fsync・replace/readback・foreign inode・stale refs等を検証。duplicate JSON／同SHA別target・role不整合・非canonical current State・32/33 chain境界・CLIを修復 |

Schema compilationの繰返しが実測で遅かったため、fresh schema bytesとfresh instance検証を維持するbounded content-keyed cacheも追加した。authority/State/検証結果のcacheはない。

## 2. 実証範囲

- R6 `ce90246`でWeekly／Longform各2訂正と実PDF各5ページ、strict receipt/Gate/Candidate/State、合成承認付き通常direct stage→RELEASEDを確認。旧canonical成果物と旧版は保持された。真正Human承認・Production公開は実行していない。
- R1×2→訂正の実operation、after-versioned R1／canonical revalidationのpre-write refusalを確認。型付き33-record fixtureはactual R1×33ではない。
- 同じSHAでもsealだけreview pathを変更すると通った不備を修復。現在はCandidate↔sealおよびreviewed targetのpath＋SHAが必要。外部review記録の保存先を勝手に固定する修復にはしていない。
- R7 `00397c3`で公開validate-stateとinclusive depth32の修復を、boundary3・affected57・fresh Weekly実PDF/CLIで確認。R7b `721a04d`はDM004 test-only、同じ7methodsの2clone実行。R6全面runをR7bで再実行したとはしない。
- Fault/negative証拠はcase別にpublic entry、意図したseam、先行拒否、write window、repairを記録。まとめて「全負例同じno-write/repair」とは認定しない。
- 現configはdirect stage/Human-Gate経路。handoff-requiredの別modeでの`build_handoff`成功は未実証。Full export PRはR5b、後続workflow同byte＋R6 current controlsとして限定採用。実Actionsは未実行。

## 3. 内容・visualと費用

作者別に最終の両PDF全10ページとreader/staged sourceを点検し、2回目訂正のheadline／本文が正しく表示され、引用・日本語・表・TOC・総括・Technical Note contrastを保持することを確認した。

**Production semantic品質は両方NO-GOのまま。** 合成の単一DID・placeholder本文・`example.invalid`等は実研究の十分性を示さない。型付きreview/approvalを実判断へ付替えていない。代表的な資料・長さでの評価は残る。

実際に除去できた操作上の問題は、review待ち中のcanonical上書き、切替後のstale Candidate差替え、同じreader/sourceの無意味な別pathコピー。追加費はconsumer/closure維持、不変版保存、再検証、explicit resumeである。多数の実装/fixture/harness修正と検証時間も投資費に含まれる。schema microbenchmarkの改善を総work削減率に読み替えず、純削減は未測定とする。

## 4. Source・保存・残る制約

- 基点actual **409b292756dd1277b9dfae87679934c0d2ce251c** / tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**。これは候補基点で、Production固定baselineは774dd39aのまま。
- Intended **57paths=25M+32A**（旧22を内包し、必要な旧componentも変更）。Raw60entryにはnotes/cache/tmp residueが混在するためcode数にしない。
- 完全patch [complete-r3-operation-409.patch](../notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch): **659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b**, **2018112B**。4parent inputs→actual409へDIRECT適用、旧patch先重ねなし。
- 独立GEN/保存patch check/apply各0、57delta/721 intended bytes一致。適用proofはavailable-source限定（689base＋32new）、full hydrated/history/全tree clean証明ではない。Whitespace/EOF diagnostics、missing26309、unbundled Python/TeXを保持。
- SOURCE fixture HEAD721a04dはsyntheticで、新candidate commitではない。実候補は409＋uncommitted overlay。Workspace `.rephase-1-editorial-runtime/` はEDQUOT後に選択したignored scratch、各DBはreconstructと独立。
- cache混入、snapshot再使用、誤tree転記、途中のshell編集／cache purge／未選択external scratch／provider error／timeout／EDQUOT／上書きで失われたpre-GEN rawをcloseoutに保存。6個のinactive smoke copyは検証済みarchiveで保全後に明示削除した。古いraw喪失を再創作していない。

## 5. 次の単位と全体roadmap

**次はversioned same-reader mechanical renewalの契約選択。** Generalへactual57と実source/record graphを使って委任し、Astraが選択する。

1. current code/tool変更後の旧versioned setを、歴史identity／現在eligibility／新導出として区別して検証できるかを具体化する。旧P3Sのcurrent-file pinを無条件無効化しない。
2. 同一reader＋同一source/PDFの場合のexact-path review再利用と、同一readerでもsource/PDFが変わる場合の新build/postrender review義務を分ける。新しいreview対象へ同SHAで付け替えない。
3. truthful Core-change reason・既存pointer/chain・canonical anchor・Candidate/normal consumer・失敗復旧を同じ契約にし、既存R1を黙って旧canonicalへ走らせない。P1のNO_EDITORIAL_CHANGEを偽編集理由で迂回しない。
4. 実装差分、同じ研究入力からの新replay、必要review/保持/出力集合、public positive/negative oracle、追加維持費を示す。未接続helper追加を終了物にしない。

全体の残り: versioned renewal、DM022 preArchitecture accepted-upstream訂正、必要Profile/Retrospective/manual/direct-primary、代表的品質、固定候補・独立七観点audit、Human採用/実運用、実測削減/旧通常経路廃止。今回のlocal operation completionをupstream CORE_FIXEDや全体READYにしない。

**Human Commit Pointで停止。** WholeNOT_READY / step4B3 OPEN / audit未開始 / DM021+022 OPEN。開始HumanHEADdf63555、今回packet/assessment/入口変更未commit、通常Commit/PushはHuman-owned。
