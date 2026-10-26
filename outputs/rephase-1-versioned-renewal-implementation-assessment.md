# Versioned same-reader renewal — implementation assessment

2026-10-26. **選択契約478f0051のbootstrap＋U/C renewal操作をBOUNDED IMPLEMENTATION COMPLETE（qualified composite）とする。** WeeklyとTHEMATIC/LONGFORM_SPECIALについて、旧版の歴史検証、新しいcurrent proof、版付きCandidate/seal、既存State参照の切替、通常direct工程と失敗再開を接続した。単一の全final-source matrix PASSではない。

必須: [Astra closeout](../notes/rephase-1-versioned-renewal-implementation/astra-closeout-resolution.md)、[独立authority reviewの§§14–15](../notes/rephase-1-versioned-renewal-implementation/resume-20261025/independent-authority-review.md)、[独立operation reviewのFINAL-BINDING条件解消](../notes/rephase-1-versioned-renewal-implementation/resume-20261025/independent-operation-review.md)、[独立evidence ledgerのFINAL-BINDING addendum](../notes/rephase-1-versioned-renewal-implementation/resume-20261025/independent-final-evidence-ledger.md)、[独立final packaging review](../notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-20261025T205432Z/independent-final-packaging-review.md)、[実PDF点検](../notes/rephase-1-versioned-renewal-implementation/resume-20261025/independent-reader-visual-review.md)。以前のNOT READYや誤った完了主張は履歴として保存した。

## 1. 実装した利用可能な操作

| 境界 | 実装・限定実証 |
|---|---|
| Bootstrap / history | actual R3-formatの両routeからrenewalへ。E証拠は元path／記録されたCOPY、T工具はowner別のrecorded commitで検証。証拠をtool commitに要求しない |
| Current source proof | accepted researchの内容検証と再導出をState再帰から分離。毎回のreadbackでlive/loaded/committed工具、epoch、contract、closureを再検証。artifact-only descendant HEADは条件付きで維持 |
| U reuse | 同一complete readerとcurrent trioの一致を要求。直前に選択された元target/review pathを保持し、旧PDFを新環境で再buildしたとは記録しない |
| C render | 新しいtrio/proof/manuscriptと実PDFを作成。build record→receipt→供給された新postrender review/QA→Gate/Candidate→seal。`prepare-targets`はC準備の公開分割入口 |
| Selection / activation | 完成したCandidate/sealの後に、既存Stateのrevalidation pointerのみを変更。strict LIVE State、canonical path、prePreview/Exception windowを保持。canonical Candidate install/Profile rebindなし |
| Repeat / next editorial | 両routeのC→U→U、古い到達可能なmaterialization proofの再利用、renewal後の編集訂正を実証。旧P1のNO_EDITORIAL_CHANGEを迂回しない |
| Normal consumers | State選択のCandidate/proofを通常stage、Preview、profiled Freeze、Releaseへ伝搬。両routeでpublic APIによるState `RELEASED / COMPLETE`、API/CLI validate-stateを確認 |
| Failure / resume | same-set孤立recordのordinary再activationを拒否し、明示resumeで再検証。ALREADY_ACTIVEはreadonly。alias/IO/close/fsync/replace/postread/foreign file、unknown Stateを分類・保全 |

歴史identity、現在eligibility、実際の旧code実行は別である。新しいreasonは`REVIEWED_VERSIONED_CORE_RENEWAL`、record kindは`VERSIONED_RENEWAL_ACTIVATION_V1`。既存R1/canonical revalidationはversioned activation後もpre-write拒否を維持する。

## 2. 実行証拠の採用範囲

* **U/Cとrepeat:** 固定736-source系列で両routeの新工具epoch、style変更、実5-page C PDF、新review targets、C→U→Uを確認。その後の修正sourceでU refreshを追加した。Longformの一度目U3はG3/G4を先に両方commitしていたため同じepochとなり拒否した。新G5→U3bが成功点で、失敗r5は保持した。
* **renewal→editorial:** 最終Weekly741系列はP1/P2R/P2V/P3S63（手動preloadなし）→実PDF→finalize→activate→history/receipt/current Stateまで各exit0。Longformは実build/新editorial setを作成後、finalize/activateのTIMEOUTを記録し、別の明示resumeで`ALREADY_ACTIVE`＋set/history/receipt/State readbackの**clean exit0**を得た。元の失敗を成功へ付け替えない。
* **実State lifecycle:** 739系列の独立コピーで、両routeともstage report→Stage Checkpoint→advance、合成のpublic Preview承認、profiled Freeze、offline合成merge/release記録→advanceを実行し`RELEASED / COMPLETE`へ到達した。先行したlow-level成果物作成だけのrunとは区別する。
* **R1×2 anchor:** 実public R1を2回→実R3 editorial→renewalでlatest LEGACY r2を保持。誤ってDRAFT checkpointをanchorにした初回はpost-State失敗となったため保存し、修正後はchain-derived anchorの完全一致とpre-write拒否を確認した。別fixtureへの既知before-COPYからの再構成は、Production rollbackの実証ではない。
* **depth:** 30件の提供済みtyped legacy履歴＋1件の実editorialから、実public HIGHで32件目renewalが成功。次の33件目は新R/record/State/temp作成前に拒否する。**32回の実renewal/R1操作ではない。** Public不正cycleのSHA拒否と、walkerのdefensive cycle probeを分け、SHA固定点を持つ実在cycleを作ったとはしない。
* **回帰:** R1は先行33＋修正pointer method/healthy control、P2Rは24＋inode交換hook修正1、P3Sは25＋current63に合わせたO1とfresh public両route、Reader F4は正しいrecorded epoch/import rootで7/7・skip0。H2/S18、bare-function15の実assertion実行、その他影響moduleの結果はledgerに個別束縛する。0-test exitやstatic source文字列checkを機能証明にしない。重複methodや異なるsourceの成功を合算した全suite件数は出さない。

最終HIGHはorphan→anchor→depthの修正を含む`3dbdedb8…`。変更の影響箇所を実public controlsで検証し、独立reviewがqualified compositeとして受入れた。旧120-greenや全742-source一括suiteの自動転用ではない。

## 3. 内容・visualと費用

作者別reviewerがWeekly/LFのCとrenewal後editorialの計4 PDF・**全20ページ**を実読し、reader/manuscript/sourceとの対応、変更箇所、引用/References、日本語glyph、余白、Technical Note contrastを限定確認した。Fidelity/visualはbounded PASS。

**代表的なProduction semantic品質はNO-GOのまま。** `example.invalid`等を含むsynthetic資料と型付きレビュー/承認は、実研究の十分性や真正Human判断ではない。Uの再利用は実targetのpath/byte一致を示し、真正レビューの存在を自動生成しない。

実測で深い履歴の反復検証が支配的だったため、1公開invocation内のimmutable Git object batchingと、独立に導出したtyped schema nodeの一度の完全検証＋各edgeのfresh pin/equality検査へ整理した。Global authority cacheやcaller permitは追加していない。これは局所的な検証時間改善であり、実装・修正・review・保存費を含む総work削減率は未測定。

## 4. Final source・配送・限界

* actual base **409b292756dd1277b9dfae87679934c0d2ce251c / tree8ce3699861505f32d1d60bdc185d4d4f635aedb2**＋**93 intended paths=40M+53A**。旧57を内包し、必要な既存componentも変更した。
* 完全DIRECT409 patch: [final-depth/complete-versioned-renewal-409.patch](../notes/rephase-1-versioned-renewal-implementation/source-packaging/final-depth-20261025T205432Z/complete-versioned-renewal-409.patch)、SHA256 **f898d33bfe6904fd29063d5a1ff462588d11f227f5aab6a3a2d505614941da2a**、**3423014B**。Manifest SHA256 **d488c6ee48b7cfa781f39905c4f08a61561e7bd02b234d2c60a6a1e93953497c**。
* 保存patchの独立check/apply各0、93変更と**742 intended files**のbyte一致を確認。独立reviewは3copy×93のSHA/bytes/mode、3copy×742のSHAを全件照合した。Apply時のtrailing whitespace＋blank-EOF、計5 whitespace diagnosticsは保持する。
* 利用可能な適用proof: `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`。Scoped689 available base＋53 newであり、full hydrated/tree-clean/history認証ではない。Missing26309/bulk31466、runtime/TeX非同梱を維持する。
* 先行92-path/741版`d6c72fb4…`はdepth修正の配送漏れにより**obsolete**。保存したまま、最終版は上記93に固定した。正しい実装作業copyはactual409の`versioned-renewal-env-20261023T185000Z/candidate-work`。初期M1の新root`a8890d4`は不採用履歴であり、候補の基点ではない。cache/tmpをblind-copyしない。

実装はHumanHEADc5b0d7cから開始し、途中Human Commit f84fcf5後は並列review/分担修正/固定source検証を行った。現在のcloseout・追加packet・入口は未commit。通常candidate/reconstruct Commit/Push、Productionアクセス拡大・採用は実行していない。

## 5. 次の単位（Human continuation後）

**pre-Architecture accepted-upstream訂正（DM022）の適用性・統合契約判断**をGeneral＋Exploreへ委任する。入力はfinal93と既存の狭いDM022 captureであり、Production mainの一般追従や再取得は不要。

1. actual93上で`EVIDENCE_REVIEWED`前後のaccepted Evidence/Views/Materiality/completeness/SelectionとState/checkpoint/Architecture境界を追い、既存の正規再生成・再開で処理可能かを確認する。
2. same-Stateのaccepted-upstream更新が必要なら、旧受理履歴を保持し、新しい受理とdownstream invalidationを通常工程へ接続する選択肢を比較する。今回のpost-VALIDATED renewalをそのまま流用する、accepted inputを上書きする、Hash一致だけで受理する案は不可。
3. 必要なDM016/017/Profile条件との依存・capability表、実装面/失敗再開/代表的品質の受入れ条件/追加維持費を示し、Astraが範囲を選び作者別の独立設計reviewを得る。未選択の実装や全22maintenance batchを先行しない。

その後も必要Profile/Retrospective/manual/direct-primary、代表的品質、一つの固定候補と七観点audit、Human採用・実運用、実測削減/旧通常経路廃止が残る。DM021/022をupstream CORE_FIXEDとはしない。

**Human Commit Pointで停止。Whole NOT_READY / step4B3 OPEN / audit未開始 / DM021+022 OPEN。**
