# Prior-artifact reader修復 実装評価 — 2026-11-22 技術PASS／実運用PARTIAL

技術修復は完了、実W34はBLOCKED。判定は `BOUNDED_READER_REPAIR_PASS / REAL_OPERATION_PARTIAL_BLOCKED`。
文書bindingは未了であり、本書で最終binding済みと主張しない。
後続は最終reviewerが文書bindingを追加する。

必読は root `notes/rephase-1-prior-artifact-reader-repair-20261117/astra-closeout-resolution.md` FULL、
`astra-repair-resolution.md` §§3–6、
独立最終 `final-implementation-review.md`（§10親対照含む）＋machine、
独立実検証 `independent-real-validation-review.md`＋machine、
`source-packaging/final-20261122T114000Z/` 報告・raw、
`closeout-evidence-index.md`。
root §§6–7の限定・逸脱・nextが本評価に優先する。

## 1. 結果

既存 `_prior_artifacts` の型付きPREARCH分岐不具合を1関数で修復した。
厳密family先読み→重複前判定、非研究roleのPREARCH別名を拒否、
個別PREARCHは既存 `agent._validate_checkpoint_record` のPREARCH枝で証明し、
publication superseded上書きは使わない。LEGACY・active7・入口/prepublishは不変。
新module・schema・family・cache・bypass・第三validatorはない。

Focusedは合成Weekly/Thematicの公開 `validate→build/advance→Architecture` を含む8件（228.541s）と、
late/prepublish拒否・直接PREARCH衝突の2件（46.406s）の別batchである。
旧8本体は不変で、単一10件runに合算しない。最終testは522行（作者520表記はcount誤りのみ）。
影響回帰は harness選択TypeErrorの無権限retry後に8成功2FAIL（exit1）であり、
`corrected-10pass` は予定名であって10PASS結果ではない。
親d591/774での同一2件再現によりpre-existing fixture不一致と確定し、
writer注入不発・freeze早期strict State拒否は修復前の位置で一致する。
旧FAILは保持し、件数合算や全体PASS化はしない。
独立最終reviewが、この限定修復のblocking findingsを解消した。コード全体の無欠陥証明ではない。

実運用は新real copyでSPのみreport PASS（約840s・exit0・1704B `e424…`・State不変）、
W34は約1250s tool killでreportなし・exit124（wrapper慣行であってvalidator正常exitではない）。
stackは修復済みreaderを越えた全体semanticsにあり、deadlock・正確costの主張はしない。

R2 dossiersは従来のbounded入力として再利用するのみで、
新規body semantic review・Human承認・Gate/Draft/PDF/R4/Productionではない。

## 2. Sourceと配送

新source child `e59fa9bc5f323a640fd922412de7757e60eb5944`、
parent `3231a0c280287411513bba359f4d3d2b6703d591`（d591）、
tree `e5e888cbb285dc32c60b422a41b24acc044378e6`。
390B commit body再計算が一致。旧f591は誤記metadataであり不使用・旧pack書換なし。
corrigendumが従来表記に優先する。

変更は stage `scripts/survey_stage_validation_v2.py`
`1e4c818b144ebeed7a4365cb00b5e43ed93e9bff4d1396691432ba77a515787e`/51927B と、
新test `tests/test_prior_artifact_reader_repair_v2.py`
`1fb831673b8291813ab0480720f84467e334374619a87fe072ff00c63438d4db`/30019B のみ。
patch差分47行は追加のみ（runtime +36行を含む）である。

完全DIRECT409は actual409/tree8ce＋144paths58M86A/775（689＋86）。
旧143を完全内包し、layer重ね・cache/material/DB同梱はない。
`source-packaging/final-20261122T114000Z/` の
patch `f032097389ad39f92cd5f1753b176cc3d89278d67fbc096b040091804f51ea39`/5724474B、
manifest `aa54944ff032450fc4cb5701668c6b5ad01a53b3000c73b078292ac27bcbdb15`/187642B。
proof `.rephase-1-editorial-runtime/prior-artifact-reader-packaging-20261122T114000Z/proof-copy/candidate-partial-b40de60`
でauthor/real/GEN/PROOFの全775を独立確認（check0/apply0、whitespace保持、partialDB限定）。

CURRENTはWeeklyのみでfixture `066c11c672a82e7ccaecb2c4e8eb23c0df1bfe4c`、
route WEEKLY_GENERATED_V2/70。stageはclosure行ではなくcontrol-rootのみ。
SAME proofのpositive→stage drift拒否 `BASIS_CURRENT_TOOL_DRIFT`→復元positiveを確認し、resealなし。
明示7pin＋loaded pathsの範囲であり、fresh全775 fixture certやLongform/PDFではない。

## 3. 実検証と逸脱

Real copy `.rephase-1-editorial-runtime/prior-artifact-reader-real-20261122T065145Z/candidate-work`
は両State EVIDENCE_REVIEWED（W34 `a858…`・SP `38a634…`）、CP `73ab…`/`2a528…`、
生成14・8 four-refs・guard不在を現認し、checkpoint/advanceなし。
SP report `prior-reader-selection-r1.json` 1704B `e424…` はe59と現State/Profileにbindし、
将来epochへrepinしない。将来source変更時は新規unique pathでfresh reportを作る。

W34 report不在、約1250s killは要請1200s child期限の未実装による超過であり、
124はtool kill慣行である。両State・14出力は現時点一致のみで、
W34 post完全raw欠落など全期間pre/post certではない。
独立実検証が両PID不在・raw・stack位相をfresh確認した。

逸脱は追認しない。launcher v1 import失敗後の無権限v2 retry（v1 bytes欠落のまま）、
1200s未実装・1250s kill、affected TypeError後のretryはいずれも preserved である。
performance codeは本unitではなく、現sourceの性能改善も主張しない。

## 4. Next

Human Commit Point後は bounded既存normal-stage validation scaling修復のみ。
Generalが実 `_evidence_basis`・`_selection_basis`・`_validate_stage_semantics` 等の
短い実transitive/interface・全pin・own-epoch・current/history・report write-return・oracle mapを返し、
root＋独立scoped確認をcode前に行う。
期限の記録だけを直すための無変更W34再実行やgeneric precode・新module/schema/family・global authority cache・bypass、
公開skip・timeout延長のworkaroundは選ばない。
public validatorは内部で完全権威を自立し、writerのalready-verified tokenを受けない。

Whole NOT_READY/DM021+022OPEN/audit未開始/quality-adoption-savings OPEN、正味削減UNKNOWN。
本unitはcode/test・2版の正常validation試行（別にlauncher初回失敗）・proof packingを含み、現docs phaseのみDOCS-ONLYである。
**Human Commit Point — stop。Ordinary Commit/Push Human-owned。**
文書bindingは最終reviewerが後続で付す。
