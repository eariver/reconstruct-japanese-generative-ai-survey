# Re:Phase 1 — 実資料Evidence訂正rehearsal評価

2026-11-05。**W34とSP-efficient-llm-2026の同stage Evidence訂正・再受理・独立review・通常stage遷移を限定完了。両StateはEVIDENCE_REVIEWED。** Selection以降、完成版品質、R4、採用、総工数削減は未完了。

正本は[packet](../notes/rephase-1-operational-rehearsal-resume-20261104/README.md)、**[Astra closeout全文](../notes/rephase-1-operational-rehearsal-resume-20261104/astra-closeout-resolution.md)**、同packetの独立closeout確認。途中の準備完了／失敗時のStateを現在状態と混同しない。

## 1. 実際に進んだこと

| 対象 | 最新生成物 | 内容reviewと現在状態 |
|---|---|---|
| 2026-W34 | Evidence409／Views409／Ledger439／義務3、LIMITED | 本文の根拠と週内時期の未確定を区別。38 VERIFIED／363 PARTIAL／8 NEEDS_MORE。独立BOUNDED_PROCEED後、通常APIでEVIDENCE_REVIEWED |
| SP-efficient-llm-2026 | Evidence160／Views160／Ledger165／義務15、LIMITED | 許可済み本文・版に束縛し直し、5 living docsは歴史版未確認のCONTEXT。8 VERIFIED／152 PARTIAL、義務2 SATISFIED／13 LIMITATION。D165の根拠記述も実カードで訂正後、独立BOUNDED_PROCEEDと通常stage遷移 |

既存の未受理canonical Ledger／Completenessだけを、所有性・現在参照・State・sourceを確認し、exclusive backupを検証してから退避した。旧content-addressed Evidence／Viewsと入力、履歴、一次資料は保存。通常writerを弱めず、`run_evidence_v2_interactive.run`で新しい受理集合とcanonical2ファイルを再生成した。fake REQUEST_CHANGES、State rollback、手動repin、force、shipping Core修正は用いていない。

W34では検証対象名の分割が実タスクの完全一致契約に反し、退避後の最初のrunがカード構築で拒否された。バックアップと未完状態を保存し、元の対象名を維持する入力へ修正。既存canonical coreによる全409カードの非公開preflightを経て、空のcanonical出力slotから正常継続した。旧slotの不在は途中状態であり、**現在は新canonicalファイルが存在する**。

## 2. Source／権限

使用instanceは引き続き `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`、隔離epoch `e84a82aca000c990597ea8cf60f548e2ff187bd1`（parent48082356）。Shipping final139／771files／DIRECT409 patch `de0af9cb…`、manifest `c5a6b230…`は不変。実行instanceのtest `d486809c…`対配送`7b862305…`という既知の1file差を維持し、他770を束縛した。Source全体の採用／新候補commitではない。

State初期化480の履歴とProfile／Contract8を保持し、新しい通常checkpoint/historyだけが実行epoch e84を記録する。Human Gatesは双方pending。新しいSelection／Architecture／Draft／PDFはない。

資料は既存の固定774/c8 captureと許可済み17 SP文書・必要metadataを再利用。今回の新規network／Production操作／通常Commit・Push・Human Commit readbackはない。以前の範囲外読取・readback逸脱の記録は引き続き保持し、履歴全体でゼロだったとは主張しない。

## 3. 証拠の限定と費用

独立reviewは、過去の本文消費reviewと変更箇所の実カード・根拠束縛・義務・Rawを合わせた限定判断である。全409／160の新たな全面semantic PASS、完全版品質非劣化、Human承認ではない。

多数の初稿harness／reviewに、誤hash、架空API引数、schemaのみのtarget判定、誤ったarchive path、検査の未実装・過大主張があった。root／独立指摘で修正し、原失敗を保存した。中断workerによる旧wrapper上書き、stage operatorの停止指示に反する局所再試行もcloseoutで明記する。正常最終結果で原過程をcleanに書き換えない。

実行例はSP最初の再生成27秒、D165訂正後27秒、W34最後のpreflight込みresume250秒。測定窓が異なり、速度比較・物理I/O削減・総労力削減の証明ではない。レビュー・訂正・toolingの費用が発生し、全role/token/並行保守/移行を含むnet savingsはUNKNOWN。Helper test数を合算したfullsuiteやshipping品質の証明にしない。

## 4. 現在の停止境界

両版の通常Evidence acceptanceまでを一つの整合したwork unitとして閉じる。**Human Commit Point。** 通常Commit/PushはHuman-owned。R4 auditや新機能を自動開始しない。

## 5. 次Human continuation後

保存された同instanceの**実質的SelectionとArchitecture準備**へ進む。最初に現在の2つのEVIDENCE_REVIEWED State、最新checkpointの四ref、source identityを確認し、旧CAND用runnerを再実行しない。

- W34: 439 effective（434 event＋5 accounting）、409 Evidence、30 DROPとcarry-overの処遇を説明。時期が未確定なPARTIALを、週内イベントとして無条件に昇格しない。41 MATERIAL／358 CONTEXT／10 HOLDを意味・重複・十分性で再評価。歴史baseline41選択／7packagesは比較資料であり新Selection承認ではない。
- SP: 132 MATERIAL／28 CONTEXT／5 EXCLUDED、13 limited obligationsと5 current-only文書を実際の論点・主張範囲へ運ぶ。PR bodyの数値はPROJECT_CLAIM、未束縛conversationはchronology review context。D165の再修正を失わない。必要な追加本文・歴史版が本当にload-bearingになった場合のみ、既存captureの十分性と許可範囲を確認して具体的に判断する。
- 必要な独立research／Selection reviewとHuman-facing Architecture dossierを作る。真正Architecture承認前のDraft作成やfake Gateはしない。汎用readerを自動必須gateへ戻さず、実需Specialを黙って除外しない。

WholeNOT_READY／step4B3OPEN／audit unstarted／DM021+022OPEN。品質・採用・削減はOPEN。
