# Re:Phase 1 — 修復済み訂正rehearsal評価

2026-11-15。**実W34／SP訂正は限定完了、Selection／ArchitectureはPARTIAL／BLOCKED。** 同一EVIDENCE_REVIEWED Stateでの正常HIGH prepare→adopt／resume／readbackにより両版の研究訂正を完了し、PREARCH正本tripletへ切替えた。通常writer preflightは両版とも1200s timeout（W34 0/7、SP 3/7、stdout／stderrとも0B）。観測された実質的な繰返し検証costはbounded修復を支持するが、full-writer因果ボトルネックを断定的に特定したものではない。Selection／Architecture PASS、Human承認、Draft／PDF、R4、production PASS、net savingsはいずれもない。

読むもの: [packet](../notes/rephase-1-repaired-correction-rehearsal-20261112/README.md)、**[root運用決定全文](../notes/rephase-1-repaired-correction-rehearsal-20261112/astra-operation-resolution.md) §§1–21**、**[root closeout全文](../notes/rephase-1-repaired-correction-rehearsal-20261112/astra-closeout-resolution.md) FULL**、[採用結果独立確認](../notes/rephase-1-repaired-correction-rehearsal-20261112/adoption-outcome-independent-review.md)+[machine](../notes/rephase-1-repaired-correction-rehearsal-20261112/adoption-outcome-independent-review-machine.json)、[preflight実行報告](../notes/rephase-1-repaired-correction-rehearsal-20261112/selection-preflight-20261115T042533Z/selection-preflight-20261115T042533Z-execution-report.md)+machine、[診断報告](../notes/rephase-1-repaired-correction-rehearsal-20261112/diagnostic-20261115T051801Z/diagnostic-report.md)+machine、[独立scaling review](../notes/rephase-1-repaired-correction-rehearsal-20261112/independent-selection-scaling-review.md)+machine、証拠索引は[closeout-evidence-index](../notes/rephase-1-repaired-correction-rehearsal-20261112/closeout-evidence-index.md)、文書checkは[closeout-check](../notes/rephase-1-repaired-correction-rehearsal-20261112/closeout-check.md)＋machine。独立closeout `notes/rephase-1-repaired-correction-rehearsal-20261112/independent-closeout-review.md`＋machineは記録済み **BOUNDED_CLOSEOUT_PASS**（bounded実訂正／Selection PARTIAL closeout、文書確認のみ、新規full773 runtime再証明なし；WITH reviewer FINAL-BINDING — 本doc更新後の再確認はこれからであり、最終再確認済みと主張しない）を併読すること。

## 1. 実際に完了したこと

- W34 R2・SP R2の正常HIGH prepare→独立内容review→外部decision→正常adopt→resume→readbackを完了。両Stateは`EVIDENCE_REVIEWED`、初期化480・forward historyを保持し、Human承認は付与されていない（activeなpending Gate activationなし）。guardは両版ともabsent。旧canonical／旧受理集合・失敗したR1・未adopt R1は履歴として保存し、上書きしていない。
- 各版4件の実訂正を受理（W34: 既存4論文のbounded claims／materiality、SP: D070／D071／D141 archive束縛＋D142過大verification訂正＋O10 full 8-field closure訂正）。byte保存はW34 405件、SP 156件の未変更カード／Viewがbyte・JSON一致。残りは独立研究reviewを経た受理済みbounded変更のみ（Human承認ではない）。405／156の数え直しは本unitの独立終端確認ではなく既存semantic reviewの再利用であり、ここでは再countしていない。
- PREARCHは正しいsame-record triplet（Evidence／Materiality／Completeness→同一revision `checkpoint/record.json`、forward history不変、旧canonicalはactive refにしない）。active 7 slotsは両版ともabsent（no deletes）。shadowはW34 0/7、SP 3/7のみで、active authorityへcopyしていない。
- W34欠落blob `155b78cfd588eb9300349e4568ee7065ae498477` を固定774 capture（`a6e3eb30…`/2371B）とSHA256＋Git-blob-OIDの二重検査でexact復旧し、当該blobのみを独立DBへ追加。artifact-only childで既存2 Profileのみを記録し、partial-tree（`write-tree --missing-ok`＋通常commit）で他OIDを全保持。hydrationやreadback-validator bypassではない。
- Selection／Architecture入力（W34 409 assignments／45 selected／5 packages、SP 160／130 selected／9）は独立`PROPOSAL_READY_FOR_PREFLIGHT`（入力scopeのDATA判断）までであり、timeoutはその編集判断を無効化も昇格もしない。W34提案45／5は15頁target／16頁max、SP 130／9は60頁target／75頁maxの**提案入力scope**であり、quota・承認ではない。

## 2. Source／epoch／State

- active: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`。execution HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`、parent `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`、tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`。exact773／final141。DIRECT409 patch `171812f686c05d8494de8bd32a6c00e043dc5ff1aa7452204a8e35f16848600d`／manifest `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`。先行shippingは不変。
- shadow（preflight／診断専用copy）: `.rephase-1-editorial-runtime/selection-preflight-20261115T042533Z/candidate-work`（byte-copy、hardlink 0、inode相違、origin inert）。activeはこのshadow実験中 untouched。
- Source773: manifest `a7e40c47…`/202833B、BASE head `409b292`（BASE tree `8ce36998…`、runtime HEAD `ae0dd1e`とは区別）／tree `8ce36998…`、773／773がactive・shadow両runtimeに存在。spot HIGH `f312f02e…`/97844、LOW `7f5fc9e0…`/240969、runner `553bf22b…`/27766は不変。
- W34 State `a8586351b096fda65793dfc20604fae9404f9e9ea06e164c3b9f9c72b576e47d`/4162、PREARCH `73ab28ea79da8bb13d7083d30eda7fa3188f060f0dbaa96a65e2407daae3ac48`/6054。SP State `38a6341107a401128d32537cda101321b42b5ec9088d07baba43b2adc4014bde`/4266、PREARCH `2a528ed533010da6acc9efaef0e24fb59be62417724b00919e0c2f6983fec9f5`/6300。両版ともtyped `artifact_refs` 8件がcheckpoint記録とfile hash一致（full pinsはpreflight報告§1＋typed recordの実hashを正とし、proseのprefix typoは束縛に使わない）。lifecycleは `EVIDENCE_REVIEWED` のままであり、Human承認は付与されていない（activeなpending Gate activationなし）。

## 3. Preflight timeoutとbounded診断（Selection BLOCKEDの根拠）

- 別byte-copy（hardlink 0、inode相違、object 231／231、`.git` dir・commondir／alternates／worktreesなし、origin inert）上で既存writerを各版1回ずつ1200s実行。W34 0/7（stdout 0B／stderr 0B、exit124）、SP 3/7（matrix `2f62e2a8…`/239359、selection `4e6884d6…`/76603、architecture `4af84ab3…`/33219のみ、残り4 absent、stdout 0B／stderr 0B、exit124）。activeはHEAD `ae0dd1e`・status 33・773・7-absentのまま untouched。shadow partialをactiveへcopyしない。
- READY gate（`low.require_research_operation_ready`、preflight期間中のfirst-write前・FULL completion・override facadeなし）を選択し、各版1回・最大90sの非発行diagnosticのみ実行。W34-ready PID 740047 wall 85.01s exit124（内部alarm85＋外部timeout90）、SP-ready PID 747458 wall 27.98s exit0（READYはNoneを返す）。前後でsource／State／slotは不変（`after-check.txt NONE`、shadow 36＝active 33＋SP partial 3）。
- call-mapは有限DAG（READY＝2 AG、runner 8 gates＝16 AGを含むsource見積り）を確認。W34 pre-matrix 60 AG、SP post-Architecture 92 AG、full 162 AGはsource見積りであり、writer実測総数ではない（exact auditなし）。derived pass積算の詳細は省略する。preflight raw自体はstdout／stderrとも0Bでphase timingなし。

## 4. 必須限定（root適用の8件）

1. profiler W34は90s cap内で85.01sに停止した観測であり、**90s超を証明しない**。観測したEvidence callsは8件でpartialであり、SP 12件のcompleteとはscopeが異なる。両者ともprofiler計測下の観測であり、cProfile相対順序の保証はない（root限定が優先）。
2. READY probeはexactなfull-writer W34 timeout位置を特定しない。有限source DAGでcycle未発見は構造確認であり、runtime no-deadlock証明ではない。
3. 60／92／full162 AGはsource見積りである。独立reviewerはEU15倍率をspot-checkしたのみで、validator別exact totalsをauditしていない。
4. overhead-controlledなprofiler ranking・speedup・物理savingsはない。same-process rcharのみであり、child Gitは分離していない。
5. diagnostic-reportのparent表記 `…2168828…` はtypoで誤りであり、正は `…2164828…`（＝`cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`）。SP proposal review §0のparent `…2168282b…`・tree `…03d6b3e…`もtypoであり、正は同じcc1c／tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`（root §4.5明示）。diagnostic machineの`shadow`先頭spaceは整形上のもので影響なし。typed／machine hashesが正。
6. 「`validate_agent_state`はlighter provenance checks」は3 full AG（PREARCH same-recordでevidence／materiality／completeness各1 AG経由）を見落とす表現であり、そのまま使わない。
7. 既存schema-validator呼出しはそれ自体でmirrored stubではない。preflightはschemaを独立実行しておらず、complete outputsもない。
8. private再利用候補はState＋four-ref hashだけでなく、Raw／task／results／View／report／proof／decision／request／retention／COPY／Profile／DCP／SCP／own-epoch depsと**全logical write＋return**の完全transitive closureを対象としなければならない。second AG guardを盲目的に outerで外さない。

CPU＋I/Oは観測scopeに留める（両probe約99% CPU-bound、W34 rchar Δ8.85GBに対しread_bytes Δ40KB、SP rchar Δ1.18GBに対し0B＝page-cache logical work、disk-wait証明ではない）。cProfile overheadは未分離であり、 hotspot相対順序の保証はない（root限定が優先）。timeout boundは観測上限であり、deadlock・普遍性能の証明ではない。

## 5. 失敗・逸脱・未証明（保存し、cleanに書換えない）

- 相対repo-root joinによる初回W34 refusal（R前にRaw 4＋requestのみ残存）、R1のrequest key-sortによる未変更View drift（`w34-supplied-decision-r1`撤回、order-preserving r6＋`core.json_bytes`でR2 byte保存を回復）、D142 routing pin 1字transcription error（r7 DATA訂正、c8 P2 capture 3751Bとhash一致）、SP 3-field closureのDM022 8-field拒否（r8で既存受理factual counter＋LIMITATIONをcopy、O10非SAT）。
- 診断のscope外broad probe（runtime Git DB 542＋他capture DB 2）をquarantineし、global absence証拠にしない。partialDB missing（`b797…`等）・missing26309／bulk31466・runtime／TeX非同梱は残存し、hydrationしない。
- 配置逸脱：post-prepare reviewがworkspace-root `reviews/` に置かれ、packet `reviews/` へのqualified copy／addendumで補正（原本保存）。reviewerのmisplaced files、SP authorの共有README書換え（stale setup／blocker文）はdraft保存の上、現README＋root決定を正とする。authorはedition-prefix DATAのみを書く。
- `2a8c…` live Profileと`155b…` recorded Profileの混同防止、helper `missing`表記とheader不一致、typo prose pinはtyped record・machine file hashを優先。outer-shell PIDとPython childの同一視をしない。preflight／diagnostic期間中のwriteに限れば、真のwriterはpreflight writerのみであり、diagnosticはcanonical artifactを作らない（unit全体では実際のadoptがStateを書換えた）。

## 6. 次Human continuation後（実装はしない）

root closeout §5／運用§21が選択したcoherent unit closeoutに従い、**bounded既存PREARCH／readiness／Selection scaling修復**を選択する。汎用precode whole cycle・新module／schema／family・汎用reader・CLI bypass・global／epoch cache・caller verified-dict・公開skip flag・third validator・mirrored stub・writer弱化・hydration-as-proofはしない。

1. 短いconcrete private-interface／full transitive caller／freshness／own-epoch／current-vs-history／logical-write＋return／closure／oracle mapを、実`ae0dd1e`＋final773上で作成する。private contextの型・lifetime・invalidation（State／checkpoint／guard／slot／own-epoch）、削減する重複AG／EU／P pathと残すfreshness recheck、各write境界のcheap check、import／digest／closure／write-set／failure oracle、除外するglobal／verified-dict／public flag／third validator／新familyの理由を明示する。
2. root＋独立scoped確認を**code前に**得る。確認なしにactive canonical生成・writer再実行・partial copy・cleanup・retryをしない。
3. その後のwhole repair、meaningful affected tests、実W34＋SP完了、fresh CURRENT proof、独立implementation reviewを経てCommit Pointへ戻る。

**Human Commit Point — ここで停止。通常Commit／PushはHuman-owned。** Whole NOT_READY／DM021+022OPEN／audit unstarted／quality-adoption-savings OPEN。

本評価は限定unitのauthor評価であり、R4七観点audit・Selection／Architecture PASS・Human承認・採用・削減証明ではない。独立closeout `independent-closeout-review.md`＋machineは記録済み **BOUNDED_CLOSEOUT_PASS**（文書確認のみ、新規full773 runtime再証明なし、WITH reviewer FINAL-BINDING — 本doc更新後の再確認はこれからであり、最終再確認済みと主張しない）。
