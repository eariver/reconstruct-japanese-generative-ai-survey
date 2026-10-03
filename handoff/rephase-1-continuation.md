# J-GAS reconstruction — Re:Phase continuation

更新: 2026-10-04 DM-001/019 closeout。**共同Freeze実装を222a37eで限定完了。3path差分、56methods成功、Astra＋作者別implementation/実復元HEAD resolution限定PASS。ここでHuman Commit Pointとして停止。次は固定222のDM-003 omitted-checkpoint/conflicting-authority witnessとdisposition、generic provenance変更の選択前に具体証拠を得る。step4/B3 OPEN / 全候補NOT_READY / canonical七観点audit未開始。**

## 次セッションの最初の行動

Context永続化確認（2026-09-30）: [closeout補足](../notes/rephase-1-r1-assembly/session-closeout.md)に、同一pathの`apply_patch`重複sectionで文書更新が一部残らなかった観測、ファイル保存/Commit済み/WSL `/tmp`内Git DB保全の区別を追加。主要判断・再開taskは保存済み。補足時点では今回assembly成果は未commitで、完全Git DBバックアップとしての復元性は未認定。欠落raw logは要約から再創作しない。

1. 本handoff、[共同Freeze完了/次task](../outputs/rephase-1-dm001-019-assessment.md)、[implementation packet](../notes/rephase-1-dm001-019-implementation/README.md)を入口にする。最終operational manifest、mandatory HEAD-binding/test-header補足を使う。後発Summaryは[保存済み最新版](../notes/rephase-1-deferred-intake-20261003/README.md)を再利用し、追加fetchしない。全旧履歴やproduction mainは再読しない。
2. **次は固定222のDM-003限定witness/disposition。** Generalがactive stage/prior-artifact経路を確認し、typed approvalが束縛する正確なCandidateとnamed mapに未登録のVALIDATED_DRAFT siblingの関係を、正常control・省略positive・stale/conflicting negativeで実validator検証。generic completeness全体を推測で修復せず、結果からAstraが必要な変更だけ選定する。filesystem scan/自動checkpoint登録/新authorityは選択していない。今回のFreeze実装・復旧・旧suite・Summaryは繰り返さない。下記3〜9は歴史候補記録で、旧 `/tmp` DBの現存主張ではない。
3. **固定B候補:** `c04f32ad46109403e8a63faaa8394a90ee6b869c`、tree `7dbcbbdb499ea6c7d33417a16144107320e1fd06`、親 `cb96ab97045b0d0767f38806809d33e383bac73d`。fixture `/tmp/jgas-rephase-increment-b-sol-implementation`、branch `codex/rephase-1-increment-b`、独立Git DB/inert origin。Aから13 runtime/schema/style＋8 test paths。[manifest](../notes/rephase-1-increment-b/candidate.json) / [patch](../notes/rephase-1-increment-b/increment-b.patch)（SHA-256 `bdff2c296867b31dbc2946526ec97490c054bc48c4ab9a8473eb5ded1248ab81`）。元A/f1とcb96 attemptは保存。
4. **最終check:** [14-module script](../notes/rephase-1-increment-b/final-matrix-c04f32a.sh) / [raw log](../notes/rephase-1-increment-b/final-matrix-c04f32a.log) / [exit](../notes/rephase-1-increment-b/final-matrix-c04f32a.exit)。132 methods / 534.724秒 / exit 0 / 131成功 / 1 skip。skipは未保存W34 commit `6f68fd09955302fd87e5ec0ce77ff06ccaec8448` が必要な既存case。source/HEAD変更がなければ成功済みchecksを繰り返さない。Solはrun開始後に利用上限停止したがprocess/結果はdurableに完了し、rootはtest実行を引き継いでいない。
5. **Bの独立reviewは完了。** [最終implementation review](../notes/rephase-1-increment-b/independent-implementation-completion-review.md)はfresh Astra自身が全B差分とtest oracleを確認した限定PASS。[2指摘resolution](../notes/rephase-1-increment-b/independent-resolution-review.md)と[最終test report](../notes/rephase-1-increment-b/final-test-report.md)も保存済み。元の[途中review](../notes/rephase-1-increment-b/independent-review.md)はそのまま保持し、最終承認へ読み替えない。担当の二重作成や成功済みtest再実行は不要。canonical七観点audit、application-ready、production採用は未達。
6. **最新CLI候補:** `e4c82692abee6acedbba07815b0d74ccefb80a7e`、tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`、親`6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`。独立fixture `/tmp/jgas-rephase-gate-cli`、branch `codex/rephase-1-gate-cli`、inert origin。BからCLI runtime 1＋test 1。[packet](../notes/rephase-1-gate-cli/README.md) / [manifest](../notes/rephase-1-gate-cli/candidate.json) / [32-method raw log](../notes/rephase-1-gate-cli/logs/candidate-relevant-tests-e4c8269.log) / [独立review](../notes/rephase-1-gate-cli/independent-review.md)。親再現3拒否＋API positive controls、test-oracle修正、元失敗と6d87eddを保存。レビュー担当はread-only指示に反して一時checkoutを行ったが開示修正済み、rootが最終HEAD/clean tracked bytes/コピーblobを再確認。patch統計をclean application証拠にしない。saved scriptsは上書き/warn-onlyのため再実行しない。
7. **今回のwitnessはshipping候補ではない。** `/tmp/jgas-rephase-witness-supp-20260927T160625Z`、S0 `48720ada77088ba16a4a8b1cc55fe76ff62e21b4` → S1 `6de6bbb7c9a87d254fafe7474096013ae8b4cc1d` → S2 `b41c58f2e1ac77cd4acfece08dd701ec2fb9e04d`。helperへコメントだけ変更し、別processでcurrent codeから旧receipt/Gate拒否→新receipt→実CLI Gate→既存CLI revalidation r1/r2→明示replayを確認。first/repeat/negative各phase exit 0はunittest件数でない。原runはPARTIAL、補足にも旧S0 Gate bytes欠落・弱いN1/N2汎用oracle等あり、raw実エラーと限定write-window assertionsだけを採用。9 artifactsを保存、S0 tree誤転記はroot修正・元値併記済み。実PDF生成/候補stage/運用writer/独立受入れを証明しない。rootはe4/BのHEADとtracked diff無変更を再確認。
8. **R1最終候補:** `b74db679f03908048db91420a8f262d412b8f58c`、tree `515b5e93a29ba82d87f6fa81c7ecbaf2c3701bb0`、parent `57853cb76d3189b862f1edabe46b83cfc0c7bd29`。fixture `/tmp/jgas-rephase-mechanical-r1-20260928T000710Z`、branch `codex/rephase-1-mechanical-r1-correction`、basis独立root `a1a4242adaddc42427b68c18ae367c04d6cd63b4`。34 refresh+31 revalidation+27 Gate+5 CLI =97成功、全raw logにHEAD/tree/hash/exit、[独立resolution](../notes/rephase-1-mechanical-refresh/correction/independent-resolution-b74db67.md)限定PASS。rootは7コピーblob一致を確認。既存41歴史data未検証・初回4 hook bypass・round3旧ログ上書き欠落は保持。[最終固有dir](../notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/manifest-final.json)を使い、以前の「final」表記やheuristic source scanを受入れ証拠へ流用しない。
9. **最新assembled候補:** `481dec0c0233d7871df79a07a88aa5fe2291daa3`、tree `657032438c6ed8b1c055d5a120b67b4b261a5092`、direct parent `e4c82692abee6acedbba07815b0d74ccefb80a7e`。fixture `/tmp/jgas-rephase-r1-assembly-20260929T143833Z`、branch `codex/rephase-1-r1-assembly`、own DB/inert origin。`git apply --check`/apply各exit 0、7mode/blob一致、A3+M4のみ。対象4 methodsは332.190s/exit 0、実DB diagnosticはcurrent closure PASS・旧e4 closure PASS・旧basis current replayの意図した拒否、[独立組立てreview](../notes/rephase-1-r1-assembly/independent-assembly-review.md)限定PASS。4test rawにHEAD/hash headerはなく、guarded runner/manifest/後続diagnosticで束縛する限界を採用範囲付きで記録。precopy stdout欠落、pip inventory失敗、hook実行の未証明、promisor/shallow/history未閉包は保持。97件が481で再実行されたとはしない。

## 最新候補 — 222a37e（DM-001/019限定完了）

- HEAD **222a37e9ee2aa96724a491f2c04c2583a86b9650**、tree **dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd**、parentff6c67f、chain222→ff→490→b40→固定774（shallowは774のみ）。3path: publication/profiled Freezeの2runtime＋専用test。新たなschema/stage/workflow/config変更なし。
- 元DB `/tmp/opencode/jgas-dm001019-impl-20261003T100801Z`、branch `codex/dm001019-freeze-implementation`。復元DB `/tmp/opencode/jgas-dm001019-chainrestore-20261003T150500Z/candidate-partial-b40de60`、branch `dm001019-final`、**actual HEAD222・index/worktree clean**。初回はrefだけ222/HEADb40だった限界を補足修正済み。
- [最終operational manifest](../notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/50-head-binding/final-operational-manifest.json)＋[pack/patch manifest](../notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-manifest.json)。b40 archiveに[successor pack](../notes/rephase-1-dm001-019-implementation/evidence-final-20261003T145621Z/20-packaging/successor-pack.pack)（46,164B、SHA256 `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99`）を足すことでavailable chain全体をoffline復元確認。20objectsは3commit/9tree/8blob、旧7objectsのみのdemoは不十分でsuperseded。元のmissing26309blobs/runtime非同梱限界は保持。
- 36専用＋8publication＋4profiled＋8stage=56成功。共通の開始HEAD/source観測を各module logへ載せており、module毎の再取得/dirty拒否/afterguardではない。[独立test-binding補足](../notes/rephase-1-dm001-019-implementation/independent-test-binding-qualification.md)を読む。synthetic研究/review/PDF/Human authorityであり、実出版/全Profile受入れではない。
- 両builderのVISUAL/Candidate/Profile slug束縛・full pair preflight・bytes保持retry・所有部分file処理・close/drift拒否を実装。初回490/ffのfindings・setup失敗・ref-only復元/誤count/弱いinode確認は残して修正。restore_chain.py/runnerは認証済み汎用復元toolでない。次回必要なら新しいhash-gated/absent-destination手順＋HEADswitch＋実identity/inode確認を使う。

## 保持する復旧親 — b40de60

- HEAD **`b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`**、tree **`657032438c6ed8b1c055d5a120b67b4b261a5092`**、direct parent **`774dd39a951c9ac3818e83dfffd4c7666efb0a20`**。旧481のtreeと同一だが新identity/新履歴。32path(21M+11A)、Freeze関連9pathは未変更。
- 元DB `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`、独立復元DB `/tmp/opencode/jgas-recovery-restore-20261003T0445Z`、branch `codex/rephase-candidate-recovery`、inert origin。実行Python `/tmp/opencode/candidate-recovery-tooling-20261003T0435Z/venv/bin/python` (3.12.14、記録済みpins)。
- [archive](../notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz): 5,152,199 bytes、SHA256 `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`。available部分DB＋686 materialized filesを独立offline復元確認済み。26,309 blobs欠落・baselineでshallow・venvは含まない。full-history/whole-application証明ではない。
- 最終identityはpacketの`corrections2-identity-20261003T0944Z/final-identity-binding.json`、scopeは`corrections-20261003T0456Z/recovery-manifest.json`。旧manifestのfindings-test blob誤記は原文を残して訂正。両correctionと[独立identity resolution](../notes/rephase-1-candidate-recovery/independent-identity-resolution.md)を読む。
- five methods成功、stage negative/CLIに各3subcases、current8-file closure正/負と復元先positive成功。suite単位guardのみ、per-test HEAD headerなし。stageは実recovered Gitを使うがdirect-primary CLIは未実行Weekly Git helperを使わない。setup/restore失敗、旧tar stderr/v1restore sourceの上書き欠落を保持。**保存restore.sh/runnerは再実行禁止**、復元成功はmanual補正後の実物検証による。DB消失時はarchiveから新しいfail-closed手順で復元しidentity/closureを確認する。

**独立指摘と修正（歴史B）:** B-IR-01は実accepted chainの2 Discovery IDを同じDraft Packageへ取り込み、archiveだけの差替えがResult refs不一致で拒否されるcaseを追加。B-IR-02は未宣言hyperref.styをreceipt/Gateが受け入れる実probeで確認し、canonical survey_rootの閉じたinventoryで修正。許可はmain.tex/references.bib/jgaisurvey.styとmain.pdf/main.log/main.pdf.sha256のみ。他entry/dir/symlink/aux/bblは拒否し、producer無書込み・receipt canonical path・Gate replayを確認する。自動削除やbuild frameworkは追加していない。実buildのaux整理/運用との接続は未証明。

**証明範囲:** 実accepted producer/checkpoint列による二段階Weekly生成、complete reader object、独立receipt再導出、generated Gate、VALIDATED_DRAFT、first/repeat metadata revalidationとactive readback、限定pending contextのnegativeを含む。研究・review・PDFはsyntheticで実Human判断/実出版ではない。10 omissions＋2 controlsとnonreader annotationはpure projectionの限定証拠、曖昧Evidence variantは実acceptance loaderを通すが別Stateへ採用していない。CLIはDRAFT_COMPLETE/no-overwriteのままなのでCore変更後CLI再生成や#495全運用は未証明。全Profile/support、Windows/Actions/application、純lifecycle削減も未証明。

最終runの依存一覧取得はpip不在で失敗しており、test成功とは分けて保存する。cb96の元131-method run（6 errors/1 skip/exit 1）、各fixture修正・probe・途中停止は[attempt](../notes/rephase-1-increment-b/attempts/README.md)、[B assessment](../outputs/rephase-1-increment-b-assessment.md)、implementation packetに保存。後のgreenで上書きしない。

## 固定点と権限

2026-10-04 DM-001/019 closeout: Human commit `066436d6d43a4fcf0b96ed1e8678e7f1edb082c2`・cleanから開始。Generalがdesign/独立DB実装/tests/pack復元、Astraが範囲選択・source/oracle/raw/実HEAD review、別Generalがinitial/correction/final/HEADbinding/testbinding限定review。source最終222、旧b40/490/ffは保存。今回packet/assessment/入口/byte保護は未commit。通常reconstruct Commit/PushはHuman担当、次DM-003 unitは未開始。

2026-10-03 recovery closeout: Human commit `fe17541212a057522922b8aabf6d66b5a594a079`・cleanから開始。Generalが固定baseline取得/独立candidate commit/限定tests/partial archive復元、Astraがmethod/oracle/source/raw/実identity review、別Generalがindependent reviewと2段階resolution。初回CHANGES_REQUIRED・Worker誤記・reviewerの全blob確認overclaimは保存して訂正。今回の復旧packet/assessment/入口/byte保護は未commit。通常Commit/PushはHuman担当、Freeze実装へ自動続行せずここで停止。

2026-10-03 intake/contract closeout: Human commit `a6d834be7da6828740bcddd9b63477064015de80`・cleanから開始。Generalが一文書取得とstatic分析、Exploreがread-only復旧inventory、Astraがsource/evidence reviewと範囲判断、別Generalが独立static reviewを担当。Worker初案の誤りは原文を残して[補足修正](../notes/rephase-1-dm001-contract/static-contract-corrections.md)に記録。今回の新packet/判断/入口/byte保護は未commit。通常Commit/PushはHuman担当。実コード/test/復旧には着手せず、このCommit Pointで停止する。

2026-09-30 assembly closeout: Human Push後のreconstruct HEAD `a22d69308e9bbfb84cee9d8530c258a2a911d059`・cleanから開始。独立byte-copy→7path組立て→限定fresh検証→作者別組立てreviewまで完了。今回の変更は新組立てpacket/assessment・入口・byte保護規則。通常reconstruct Commit/Pushは未実施。Humanは今後も区切りで**作業を中断してCommit Pointを提示**するよう明示したので、ここで停止し、次のDM-001 unitへ自動着手しない。

2026-09-29 R1 completion: Human再開後、初回返却はCHANGES_REQUIRED、修正後に作者別Generalが8aをreviewし追加指摘、全deltaをb74で限定解消確認。reconstruct HEADはd175600のまま、今回の新契約/元返却/修正/独立review/assessment/pause履歴と入口が未commit。原packet上書き逸脱は記録し、final-b74の固有packetを受入れ根拠とする。ここが今回のHuman commit/Push区切り。新しいassemblyは未開始。

2026-09-28 R1 safe pause: HumanのPush後、reconstruct `d17560028bd5db459636ca957888b7369b5d5cda`・cleanから開始。運用契約を確定しGeneralへ実装委任、Worker返却直後にHuman停止指示。現在は新契約・分析/実装packet・pause記録・入口/byte保護規則が未commit。新しいreviewerやtestを起動せず停止。通常reconstruct Commit/Pushは行っていない。返却test成功はWorker報告でありAstra受入れにしない。

2026-09-28 regeneration closeout: reconstructはHuman commit `d665af89ae4d741584020ea79e658322b11f37f2`・cleanから開始。Generalが分析/witness、Exploreがbuild transfer探索、Astraがsource/oracle/evidence reviewと限定判断を担当。原fixtureのreset/clean逸脱と欠落raw証拠は隠さず保存し、補足は新fixtureで実施。今回の変更は新packet・2 assessment/decision・入口/byte保護規則。shipping runtime未変更。通常reconstruct Commit/PushはHuman担当、ここが今回の区切り。

2026-09-27 CLI continuation: HumanのCommit/Push後、reconstruct HEAD `35a5b205c331e15744a909596c658c18a1c182e4`・clean・local tracking同期から開始。今回の成果はCLI候補packetと入口更新、`.gitattributes`のpacket `-text`追加。Generalが独立fixture内のみで2 review commitsを作成、通常reconstruct commit/Pushは行っていない。ここが今回のHuman commit/Pushの区切り。次の契約分析は未開始。

2026-09-27 continuation: reconstruct開始時HEADはHuman commit `34f78c7ee7f57489343eef6f9ae816413e6f068d`、worktree clean、`main...origin/main [ahead 1]`（fetchなしのlocal tracking観測）。A/B closeoutの未commit記述は下記の歴史観測。今回新規なのはstep-4分析/採否と入口更新のみで、コード/test変更なし。ここもHuman commit/Pushの区切り。次unitは選択済みだが未開始。

2026-09-27 closeout: reconstructの未commit変更には入口文書・assessment・A/Bの未追跡evidence packetを含む。`.gitattributes`へA/B packetの`-text`規則を追加し、commit/checkout時にも記録済みhashの元bytesを保持する。候補コード/test結果の変更ではない。Humanは区切りのよいCommit/Push時点の通知を希望している。通常のcommit/PushはHuman担当で、通知希望は代行許可ではない。

- Production baseline: **`774dd39a951c9ac3818e83dfffd4c7666efb0a20`**。明示rebaselineまで変更しない。
- f1: `bf32edf98ba8f605169d7188bbc764de74ee4f6e` / tree `ebd351479ec222a08b8ea67ae4aae64ad0eb927e`。親a1 `d38f023ce200619f7f49ce17a348755f05e0e021`。
- [候補manifest](../notes/rephase-1-freeze/candidate.json) / [固定baselineからの全patch](../notes/rephase-1-freeze/application.patch)。r2の5ファイル＋a1 test修正＋f1 runtime/testの計8ファイル。
- Increment A: `1a9649129d1745fed0b98db46ef15f014407e6fc` / tree `5e933aa54034ed227216252a2c8707a59f293acf`、親f1。[manifest](../notes/rephase-1-increment-a/candidate.json) / [f1差分](../notes/rephase-1-increment-a/increment-a.patch) / [固定baselineからの全patch](../notes/rephase-1-increment-a/application.patch)。元f1と過去packetは不変。
- 必要Git/Git-aware検証は独立DB/inert originで許可。production変更/投稿/採用/State/Gate/Release/Actions実行は未許可。通常のreconstruct最終commit/Pull/PushはHuman担当。
- 完了した限定unitの区切りでは作業を中断してCommit Pointを提示する。通知希望はCommit/Push代行許可ではなく、次unitへ自動続行する許可でもない。
- 新しいproduction mainの一般追従は禁止。今回の例外は指定Summary一文書のread-only取得だけ。取得済みcaptureを使い、定期refreshしない。

## 現在の判断

**r2:** 規則・live status分離を維持。新規execution indexからstatusコピー義務を外し、履歴・必須読解・正規authorityを残す。新規実行への適用案で、既存Released版の再生成/承認付け替えはしない。純lifecycle削減は未実測。

**f1:** B1 stage/schemaの3-artifact整合、B2 typed approval接続は限定修復済み。24 testsと独立reviewの範囲を保持。Weekly合成fixtureでlow-level approval→FROZENを接続したが、profile-aware Freeze、全Release workflow、全Profile、canonical durable Human Gate全往復の証明ではない。

**Increment A:** 両stageとpublication revalidationのexact Manuscript接続を限定修復。固定HEADで専用11 test methods（cardinality 6 subtestsを含む）+既存61 testsが成功。別f1で4経路の誤受入れを意図したfailureとして確認。[独立implementation review](../notes/rephase-1-increment-a/independent-review.md)と、後発の証拠表記だけを検証した[resolution supplement](../notes/rephase-1-increment-a/evidence-resolution-review.md)は限定PASSを支持。Astraはraw log・diff・test oracleをreview済み。canonical七観点auditではない。

**B3:** Aに続くBのcomplete reader input・独立derivation・限定pending revalidationは、対象test・Astra review・独立implementation reviewまで限定完了。全renderer引数をsemantic reviewへ束縛する旧試作は内部注記まで再review identityを変えるため不採用。Bはschema-validな新canonical inputを用いる。Aの旧reader fixtureは当時のpublisherに対して非validであり、Bの証拠へ流用しない。Bの限定完了と全B3・全Profileの受入れは別。

**A証拠の限界:** 初回clone失敗のexact argv/数値exit、初回fixture-error runの全文は未保存（tailは保存）。独立copyと最終test証拠は別に確認済み。full application patchはexact diff/hash一致だがtemporary-index apply checkがmissing promisor objectを出力し、exit 0でもclean適用証明としない。packet-verification.logのsize一覧は補足前のhistorical inventoryであり最終manifestではない。これらをgreen結果で上書きしない。

Bのreader/derivationとwitness/R1/481/b40復旧の歴史的限定結論を保持し、今回222でDM-001/019共同Freeze境界を実装/reviewした。部分DB/asset閉包やwhole application-readyは別。build transferの6名前は許可集合で全必須ではなく、現canonical PDFはsurvey_root/main.pdf。次DM-003は型付き承認によるCandidate取得と未登録checkpointの関係を実witnessでdispositionし、generic修復の要否を判断する。optional findings輸送、Special/support、DM-004は別。レビュー責任統合は選択していない。

**Bの選択済み契約:** routeはGate derivation blockに明示し、generated reviewed input内のroute/Profileと一致させる。既存semantic-review schema/役割を保持。既存source manifestをschema-validatedな唯一のreplay receiptとし、current State/checkpointからaccepted refsを検証してprojectionとmain/bib/styleを独立比較する（過去State hashはprovenanceのみ）。styleの表示文言もreader inputへ含め、他Profileの既存default/layoutを保持。bibliographyはacceptanceが束縛するcardだけを使い、非accepted `interactive-evidence.json`が必要な曖昧選択は停止。後段Publication Review/BIBLIOGRAPHY_METADATAをpre-TeX PASSへ流用しない。詳細・path・testsは契約判断に集約。

## 後発Summaryの扱い

**最新 2026-10-03:** [新capture/全20採否](../notes/rephase-1-deferred-intake-20261003/README.md)。取得commit `d6381568cc897a47d6de992189e20339350342b7`、Summary内部last-reviewed main `239ef2703a93fa802f232978c7166d04d6cc3d49`、baseline `774dd39a...`を区別。DM-016〜020追加、006/013拡充、001〜004/014等再発報告。DM-001/019を共同Freeze契約として選定し、Candidate-bound VISUAL・両builderのexact approved Candidate・validated Profile slug・書込み前preflightを要求する。DM-016/017 upstream Profile契約、018 rendered QA、020 semantic fidelityは別acceptance disposition。一次リンク/corpus未読、再現test未実施、CORE_FIXED判定なし。以下は前回intakeの歴史記録。

[読取・全15項目の採否表](../notes/rephase-1-session-transition/deferred-intake.md)。取得snapshot `f85539c31a079ab7a7fa86185f3cbb0fcad0485a`、Summary内last-reviewed main `0a0b0747...`、固定baseline `774dd39a...`は別の値。Summary記載の再現/修復状況は一次記録を再検証していない。

- DM-002はf1 B2と重なるがupstream CORE_FIXEDとはしない。
- DM-001はprofile-aware helperの別問題、DM-003はprovenance completeness、DM-004はRelease CLI。後のapplication-ready/audit前に個別dispositionが必要。B3へ自動追加しない。
- DM-014はr2のlive-copy除去方針を評価する後発Evidence。productionのrefresh提案をそのままr2へ戻さない。
- DM-005/006/010/011/012/013/015はB3のinterface/意味保持/引用/表示のacceptance入力。DM-007等の独立intake修復や15項目一括実装には進まない。

## 役割とEvidence

Astraはarchitecture・計画・task definition・成果物/evidence review・修正判断。実コード/test executionはCo-Worker。Generalは複数段階の分析/実装/test、Exploreは読取探索。**HumanはGeneralをMuse Spark 1.3、ExploreをDeepSeek v4.1 Flashへ設定したと報告し、各1回のsmoke callを了承。Generalの実モデル未確認、Exploreはruntime上`open-code-go/deepseek-v4.1-flash`と自己報告。能力比較は運用上必要になった時まで行わない。** 旧Sol/Luna選択規則を上書きするが過去の担当表記は変えない。独立Auditor/最終七観点auditは作者/WorkerおよびAstra author-side reviewと別。Worker停止時もrootが実装/testを引き継がない。

初期B3 Auditorはreport保存後に利用上限で停止。rootが2指摘を修正し、fresh Solがdesign/evidence上の対応のみを確認済み。実装reviewではない。[B3判断](../outputs/rephase-1-reader-boundary-assessment.md) / [限定対応確認](../notes/rephase-1-reader/resolution-auditor/review.md)。最終七観点auditは未開始。a1の広いtestは完了recordなしでINCOMPLETE、Windows/実Actions/歴史依存閉包等も未証明。

## 実行環境・履歴入口

[Restart context](../notes/rephase-1-session-transition/restart-context.md)に、実path、runtime pins、f1消失時の固定SHA+durable patch復元、再実行してはいけない旧script、既知failure、権限・role差分を集約した。`/tmp`は消え得る。新headに旧PASSを引き継がない。

旧handoffは[移行直前snapshot](../notes/rephase-1-session-transition/handoff-before-transition.md)へ保存した。必要時だけ[Freeze判断](../outputs/rephase-1-freeze-assessment.md)、[application NOT_READY](../outputs/rephase-1-application-assessment.md)、[全体方向](../outputs/rephase-1-direction-assessment.md)を参照。過去の「次」は現在のplanを上書きしない。
