# Re:Phase 1 — Selection / Architecture準備評価

2026-11-06。**PARTIAL／実装上の依存関係で停止。** 両版のSelection・構成案を作成し、独立reviewと必要な追加資料確認を行った。正規の上流Evidence訂正producerが補足資料を引き継がないため、必要な訂正を受理してSelectionへ進む処理は未実行。両Stateは引き続き`EVIDENCE_REVIEWED`である。

読むもの: [packet](../notes/rephase-1-selection-architecture-20261105/README.md)、**[Astra決定全文](../notes/rephase-1-selection-architecture-20261105/astra-working-resolution.md)**、[実sourceの操作map](../notes/rephase-1-selection-architecture-20261105/actual-dm022-supplement-operation-map.md)、[独立capability review](../notes/rephase-1-selection-architecture-20261105/independent-correction-capability-review.md)、同packetの独立closeout確認。

## 1. W34 — 除外理由を再検討し、4件の研究論文を訂正対象にした

最初の41件／5packages案は、319論文や一部CONTEXTを未消費・一律の理由で除外しており、独立reviewでCHANGES_REQUIREDとなった。タイトル・abstractの全体triage、26件の保存済み本文読解、39件の非論文CONTEXTの個別理由を追加した。なお「作者報告であり再現・deploymentがない」ことだけで研究論文を除外する判断も退けた。

採用候補として根拠を補う対象は既存4件: `2608.15127`（agentic workload）、`2608.16096`（license/costの評価条件）、`2608.21100`（ReFrame安全性手法）、`2608.18389`（code-agent robustness）。保存済み補足Rawで読解でき、追加network取得は不要。現受理済みカードはabstract-triageに留まり、本文で得た技術的主張はまだ受理されていない。**本文read ledgerは新しいcheckpoint authorityではない。**

4-record訂正DATAと条件付き45件／5packages案（12 feature、12 section、21 supporting、15頁target／16頁max）を保存した。409 Matrix候補のうち残364をHOLD/NONE、30 non-Matrixは26 EXCLUDED＋4 DUPLICATEとして別に説明する。Carry-over処遇と時期未確定の制限を保持。これは正常生成済みSelectionでも承認済み構成でもない。

## 2. SP — Jevの歴史版本文を確認、受理済みEvidenceへの反映は未実施

初稿のDID推測・未検証件数・全MATERIALに近い選定・Jevの付録移動による義務免除を訂正した。D119のGenAI-Perfと未確認AIPerf、D162のsocial reception、DSparkのarchitectureと特定serving deploymentを分離した。Profileの必須Jev事例を省かず、as-of条件も維持する。

Humanの追加許可により、指定3 URLに限定してWebアーカイブを取得した。**3 index＋3 snapshotの論理要求、archive内redirect1を含む7 HTTP hops**。無制限探索・current-page再取得・D142 API取得はしていない。独立offline検査でgzip wire/decoded本文とCDX digestを確認した。

- launch本文: served `2026-09-21T03:30:22Z`。
- concepts本文: served `2026-09-21T04:13:55Z`。
- models本文: selected `20260921091419`からredirectし、実際のserved版は**`2026-09-20T20:50:53Z`**。後者のCDX rowとbytesが一致し、未取得の前者の本文として扱わない。

歴史版はtyped/parallel/RLCDというvendor説明、条件付きlatency/price/evaluation、`jev-1.13.0`とaliasを支持する。Nov現行版の1.14等を当時の証拠にしない。D071の255-cardinality等、歴史本文にない記述はas-of主張から外す。D142は未取得であり、schema/confidence数学・校正を検証済みにしない。RLCD内部と独立再現も未確認。O10は自動SATISFIEDにはならない。

D070/D071/D141のarchive束縛とD142の過大なverificationを直す4-record DATA、補足30entries案（27保持＋3置換）、有効IDのpreimage mapを保存した。条件付き構成はJev主章を戻した63頁target／85頁max＋別付録6頁案だが、採用・予算とも今後のreview対象である。新Rawはpacket DATAに留まり、active Evidence/supplementへ未適用。

## 3. 実sourceで確認した操作上の障害

`survey_prearchitecture_acceptance_v2.prepare_revision`はLOWの`build_revision_package_from_paths`を常に呼ぶ。現producerはOLD packageからprompt/contractsのみを引き継ぎ、packageの`authority_supplement`とtaskの`authority_supplement_source_ids`を作らない。request/manifestにsupplement ref欄があっても、その記録だけでは新packageに権威が渡らない。

W34の401/409 task、SPの28/160 taskはsupplement-boundであり、affectedだけでなく変更しないカードの根拠も失う。下位LOW関数で手動補足したpackageを扱うテストは存在するが、そのsupplemented成果物をHIGH prepare→adoptした証明ではない。独立source reviewもこのgapを確認した。

手動LOW組立＋完全なR manifest＋HIGH adoptという全ての構成が禁止だと断定はしない。ただし正常なwhole writerは存在せず、採用にはHIGH相当の組立・保証処理をoperator側で複製する必要がある。総工数の目的から、その回避策より**既存producerの限定修復**を選択した。

## 4. 保存状態と証拠の限定

Activeは同じ隔離e84 instance。W34 State `d7acd29b…`/CP `0979f9f7…`、SP State `180db8c3…`/CP `1233b1f6…`の受理済み研究を維持。新しいMatrix/Selection/Architecture、State遷移、Human Gate、Draft/PDFはない。shipping final139/771、DIRECT409 patch `de0af9cb…`とmanifest `c5a6b230…`は変更していない。

新規作業はpacket内の読解・提案・review・許可されたarchive取得である。通常Commit/Push、Human Commit readback、Production操作、shipping実装・project testsはしていない。全体品質非劣化・adoption・net savingsは未証明。初稿の誤り、過去のpre-code gateを誤って再開した分析、無根拠なLOW+HIGH route主張、無効なarchive source IDは履歴として保持し、現在の判断から除外する。

## 5. 次Human continuation後の具体task

**既存DM022受理済み上流訂正producerのsupplement carryを限定修復する。** 新module/schema/familyや汎用readerは前提にしない。

1. 現sourceの短い具体map: request supplement ref、package/task carry、contract、COPYからのtrue R/E、全Raw期待pin、affected/unaffected semantic保証、HIGH prepare→外部review→adopt/resume/readback、後続four-ref消費。Rootと独立scoped reviewerがsource変更前に確認する。旧B2/B4一般pre-code cycleを再開しない。
2. 隔離source workcopyでwhole selected pathを修復。既存LOW補足テストだけで完了とせず、実際のHIGH経路でunchanged/replaced補足・Raw drift/refusal・履歴保存・failure/resumeとWeekly DERIVED／Specialを検証する。必要なCURRENT proofと完全配送を新sourceに束縛する。
3. 修復sourceを実行環境へ正当に継続させ、保存した両版の訂正DATAを通常のsame-State操作で生成・独立review・adoptする。その後にSelection/Architecture案を再評価し、通常生成と必要reviewへ戻る。入力schema適合・新claimの実source消費は実行前に再確認する。

**Human Commit Point — ここで停止。** このunitはSelection/Architecture準備PARTIALと必要な次投資の選択であり、実装・Selection・Architectureの完了ではない。WholeNOT_READY／step4B3OPEN／auditunstarted／DM021+022OPEN／quality-adoption-savings OPEN。
