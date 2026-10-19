# R1 実source統合admission可否判断 — 2026-10-19

**Astra判断: 提出された最小拡張2案はNO-GO。R1は実現性評価・不採用判断として完了、implementation-ready contractとしては未成立。** 新たな訂正helper/実装は選択しない。次の実行単位は、現21sourceの**初回Weekly＋Thematic/Longformで実build→出力transfer→公開admissionを検証する統合witness**とする。DM021/022の通常訂正が必要な経路の全体完了条件は残す。

根拠: [ロードマップ](rephase-1-completion-roadmap-20261019.md)、[原初稿](../notes/rephase-1-roadmap-replan-20261019/admission/integrated-admission-contract-analysis.md)、[Astra一次review](../notes/rephase-1-roadmap-replan-20261019/admission/astra-first-review.md)、[別Worker訂正案](../notes/rephase-1-roadmap-replan-20261019/admission/integrated-admission-correction.md)。両案の選択/費用/具体APIの記述は本判断で上書きし、元文書は保存する。本書は作者側判断であり、独立reviewは別記録とする。

**独立closeout:** [fresh作者別review・必須§9](../notes/rephase-1-roadmap-replan-20261019/independent-roadmap-decision-review.md)で、replan/NO-GO/次taskに限るBOUNDED_PASS。§9は原reviewの「訂正案coherent/全解消」「全premise確認」「費用最適」の広すぎる表現を撤回/限定する。実装/候補全体/audit/採用のPASSではない。

## 1. 何を完了したか

1. 目標/完成線から全体を再計画し、最初のtaskを統合admissionの可否決定として実行した。
2. 消失していた一時copyの代わりに、保存4inputsから独立actual409を復元し、完全21patchを直接適用した実sourceを分析に使った。
3. 「3A/既存consumer無変更」「新reason＋3controller hunksで既存validator再利用」の2案について、成立しない具体的境界を特定し、不採用とした。Worker提案を実装・受入れと取り違えない。
4. 大きなauthority変更に投資する前の、独立して価値がある実build/初回経路統合witnessを次taskに選び直した。目的は新しいread-only部品の追加ではなく、**実際に読めるPDFと公開validatorの接続、および残る運用費**を得ること。

R1の出口としてロードマップで認めた「不成立理由＋代案/採否」を使う。NO-GOを設計PASSやDM021解決と表示しない。訂正の詳細契約が未成立であることは残余課題であり、R1分析の未実行を隠す表現ではない。

## 2. 現sourceと復元証拠の正確な範囲

- 新copy: `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`
- 実detached `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`＋21path（3M18A）。R11 static21 `1c0e339c`に全21のSHA256/bytes/modeが一致。
- 保存patch `e449d029c8775ee28ee610f224997a57b0cd68664194c6720a6038ce9a3012fa`、1,233,670B。4parent inputsは各固定SHAに一致。candidate新commitなし。
- 新current観測の[source/raw/exit](../notes/rephase-1-roadmap-replan-20261019/admission/current-source-verification-20261019T000525Z/README.md)はHEAD/tree/detached、status21、cached diff0、21pins、inert config、cache0を記録。reachable censusはpresent2376/missing26309、commit chain13。元cache84を再創作していない。
- **復元時commands/exitの原記録はtranscription/tool観測でraw/scriptは未保存。** [必須資格付け](../notes/rephase-1-roadmap-replan-20261019/admission/restoration-evidence-correction.md)。後発current観測は復元当時のfail-closed実行・連続無変更・完全隔離の遡及証明ではない。
- current checkerは観測用で汎用guard認証ではない。`status -z`は`--untracked-files=all`指定でなく、rawは今回21個別pathを示す。Gitエラー/設定/別inodeの全条件を機械assertするtoolではない。inode比較domainはrestored **pack files** 対durable inputs/reconstruct `.git/HEAD`であり、全Git entry対全objectの独立性証明ではない。rawには実git-dir/common-dir、別device、aliasなし等が見えるが、それをscope外へ拡張しない。
- source解析のための現在の利用可能性は支持する。runtime/fixture/全test/実PDF/真正承認/採用の証拠ではない。将来実装/testの独立copyはその時の新手順・全必要分離確認を要求する。

## 3. 不採用の技術的根拠

以下のsource pathは上記復元copy相対。Astraはcontrollerのrow/chain/record/State処理、Longform receipt全公開validation、P1 Candidate部分を直接読んだ。補助caller探索はExplore返却を用いたため、未直読callsiteまでroot実測としない。

| 提出案の主張 | 実source/契約上の反例 | 判断 |
|---|---|---|
| 新State pointerを追加し既存source無変更で公開readback | Stateはstrict schema、現active resolverは`publication_revalidation_provenance`だけを消費（controller1090–1187）。新pointerは未消費。 | 初稿NO-GO。既存chain利用は有望だがenum追加だけでは足りない |
| live main/bib/styleをO_EXCLでinstall | healthy beforeには3fileが既存。P3Sの新規root所有規則は置換規則でない。 | 初稿NO-GO。置換か不変versioned経路を具体的に設計する必要 |
| Longform/Weekly receipt・Gateを無変更で使い、versioned early reviewを利用 | Longform receipt665–758はreview path/SHAとreaderを一致させ、strict State経由でauthored inputから再導出し、reader/archive/receiptをcanonical siblingsに限定（698–730）。proposed-readerへのreviewを同SHAのcanonical fileへ付替えても同一authorityでない。 | 訂正案もNO-GO。versioned targetを正式に認めるreceipt/Gate/loader契約なしには成立しない |
| authored archiveはKEEPのままreader inputだけ置換 | receipt再導出は`publication-semantic-input`のauthored bytes＋accepted Draftを消費（Longform698/734–742）。変更readerを旧authoredから出せるとは限らない。訂正案139行自身が未決定のまま方針を反転している。 | 版付き新authoringを参照する明示契約が必要。accepted Draftは改変しない |
| 既存revalidation chainに任意new pathsを載せれば足りる | controller847–949はoriginal checkpointの`(name,path)`集合、canonical path、prior SHAと完全unionを照合。役割だけ一致する別pathは拒否。952–1017は歴史リンクにも同条件。 | versioned案にはreason別row表現と歴史/active解決の変更が必要。Profile差替えだけでは足りない |
| 3operationのin-memory contextで長時間のreview/再開まで解決 | finishには外部で作成されたsemantic/visual review入力がなく、API内でreviewを「生成」する記述。検査項目PASSの自動生成はreviewではない。現在のpublic Longform validationにはそのchecked editorial contextも存在しない。 | runtimeがreviewを生む案は拒否。独立reviewによるpersisted inputsと厳密再検証を明示する必要 |
| live survey_rootで直接TeX buildし12–16filesのexpected-old/newで包む | compilerのaux/log等のwrite setと閉じたdirectory制約が未接続。reviewを待つinvalid-live windowを「minutes」とする根拠もない。 | 数値費用/時間の断定撤回。build-owner隔離とtransferを実物で先に検証する |
| 同bytesなら所有不明でもresume、approve validatorが失敗したCandidateならunadopted扱い | 同bytes≠所有。承認ファイルのinvalidは承認absenceの証拠でない。部分失敗を横断するmemory-only basisも復旧権限にならない。 | fail-closedの必要条件に反する。未知/壊れたauthorityは保留、黙示supersessionしない |
| Publication Candidate衝突は一律拒否/Selection gateで判定 | P1 822–862はhealthy-beforeと6ref一致する**unadopted publication Candidate**をCOPY保持対象として観測。SelectionのHOLD規則とは別。 | healthy unadoptedを安全に版更新する経路が必要。一律拒否では操作が完成しない |
| fixture F0にF0 SHA付きreceipt/QAを同時にcommitし、F1をrenderer basisにする | commitを含むself-referenceは構成不能。実source/contractの意味あるfixture commitが先、authority生成は後。currentEpochはclockの新しさではなくcontract/implementation/receipt関係の成立。 | 提案fixture手順は未実行・不採用。既存accepted fixtureから実生成する |

二案ともruntimeは変更・実行していないため、これらは**source/contractの矛盾**であり再現test failure数には数えない。

## 4. 比較結果と選択

| 選択肢 | 除去できる仕事 / 必要な追加費 | 今回の採否 |
|---|---|---|
| 無変更consumer＋小writer | 前記矛盾により通常工程へ戻れない。短いpath予算は見かけだけ | **不採用** |
| canonical live replacement＋durable checked install context＋既存consumerの明示拡張 | canonical callerの一部維持は可能。版付きreview target、after再導出、外部QA入力、owned recoveryと待ち時間中の不健全Stateを正式に扱う費用が必要 | 実装選択を保留。成立可能性まで否定しない |
| immutable versioned publication set＋reason-tagged active-role解決＋State pointer切替 | 旧publicationを保持しreview/buildを採用前に終えられる。row/schema/reader/receipt/Gate/stage/Preview等の固定path依存を列挙して改修する費用が必要 | 比較対象として保持。安全性の利点はあるが未完成設計を選択済みとしない |
| Profileのsource_root/survey_rootを差替えるshortcut | checkpoint/accepted refs/Profile hash・public slug（survey_root basename）へ波及。単なる出版先変更でない | **今回の採用案にしない**。探索提案を契約へ昇格させない |
| **先に現initial routesの実build→admissionを実証** | 既に限定実装済みの成果を実PDF・review可能な入力へ接続し、compiler所有/QA input/path/public readbackの共通費を明らかにする。通常制作にも単独の価値があり、訂正方式比較の入力になる | **次taskに選択** |

これはDM021を終わった扱いにする判断ではない。今回の実source分析で「設計が先なら小さな拡張で閉じる」という期待は支持されなかった。全体目的に戻り、次の投資を**実publication到達性**で評価する。無限に契約draftを増やすより、既存経路で実際に成立するbuild/QA境界を得る方を優先する。

## 5. 次task — initial-route build/admission統合witness

Co-Workerの通常実行taskとして以下を選択する。今回R1の次Commit Point後、Human continuationで開始する。必要コード修復は実測blockerに対してAstraがscopeを選択する。先に新admission writerは作らない。

### 入力と実行

1. 実available409＋final21を確認し、独立DB/inert origin/no共有の新fixtureを作る。既存copyがあれば再復元しない。必要source/contract/runtimeを検証し、意味あるfixture source commit後に研究/承認fixtureを生成する。ordinary candidate commitとは区別する。
2. 対象を **generated Weekly（初回）＋THEMATIC/LONGFORM_SPECIAL（初回）** に固定。既存real accepted fixture producerからDiscovery/Evidence/Selection/Architecture/Draftを生成し、既存2pass publisher→persisted pre-TeX review→source/receipt/Gateの順を使う。初回review記録をfixtureとして作る場合はtype/identity試験と表示し、内容reviewの代用にしない。
3. 既存build workflow/toolchainの必要部分だけをread-onlyで参照し、compiler/fonts/assetsの利用可能性を確認。**disposable build workspace**へ正確なTeX/Bib/styleを移し、auxはそこで閉じる。PDF/log/digest等、既存QAが本当に必要とする明示集合だけをpublication側へ所有付き転送する。既存closed-inventory validatorは弱めない。実buildを回す必要があるため、過去31/43/26等の再実行は入口条件にしない。
4. 実生成PDFについて出力hash/page-count/必要logsを束縛し、実sourceとPDFを使った作者別semantic/visual確認を受ける。test用PASS/type-fixtureはこれと別欄に記録する。Human Preview承認やPublication adoptionをAgent判断で作らない。
5. exact manuscript、receiptの独立replay、Gate両stage admission、quality bundle、publication Candidate、strict Stateと通常Freeze/Release **合成authority fixture**のreadbackを同じsource identityで接続する。実Actions/Release/真正Human承認は実行しない。途中blockerはrole/path/source根拠と最小修復案をAstraへ返す。

### 最小oracleと出口

- 正: 両routeで実PDFを生成し、public receipt/Gate/QA/Candidate/Stateへの受渡しが成立。reader inputとrendered出力の意味/引用/表示を独立確認する。
- 負: undeclared build input、転送PDF/source/hash差替え、wrong-manuscript、stale semantic/visual、build失敗/partial transferは意図した境界で拒否。単に先行fixture setupが壊れたfailureを負例PASSにしない。
- sourceの既存欠陥が阻む場合: rawを保存し必要差分/影響回帰/作者別reviewまで一つのtaskで閉じる。対象scopeを超えるauthority変更なら、正確なblocker付きNOT_READY結果を返す。
- 成果: 2routeの実PDF/入力/保存raw/固定source pins、明示transfer集合と失敗時の扱い、公開admissionの可否表、質的/得られる範囲の量的work比較。routeごとに実build/semantic/visual/type-fixture/Human未実行を区別する。
- 必要Retrospective/manual/direct-primary/upstream Profileの支持まで自動拡張しない。別途実使用から必要範囲を決め、必要経路が未対応なら全体完成保留。

## 6. ロードマップへの反映と残課題

新順序: **再計画 → R1可否判断（今回） → initial-route実build/admission → 訂正方式の統合選択/実装＋必要Profile/upstream訂正のdisposition → 固定候補・独立audit → Human採用/実運用 → 費用確認・旧経路廃止**。

DM022は固定sourceのforward-only/pending-Gate制約と対応する重要入力。pre-Architecture accepted upstreamとpost-VALIDATED readerを同じpermissionで直さず、実用的な訂正経路の必要性・失敗時負担として保持する。Summary/Issueの記載を実再現やCore修復に読み替えない。

whole NOT_READY / step4・B3 OPEN / canonical七観点audit未開始 / DM021・DM022 OPEN。ソース復元/設計No-Goは、旧P3S等の限定完了を取り消すものでも最終受入れを増やすものでもない。純削減未測定。Commit/Push・Production採用はHuman-owned。
