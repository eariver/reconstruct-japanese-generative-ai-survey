# W34 人間向け dossier r3 ドラフト（BLOCKED・未承認） — 2026-W34 週次誌

**BLOCKED: 4紙の accepted Evidence 訂正が未了のため、本 dossier は採用不可。** 本ファイルは著者 DATA のみ。独立再 review・Architecture 承認・Human Gate・Draft/PDF は未了。正準 State/Ledger/Completeness/Selection/Architecture への書き込みは一切なし。旧提案（v1/r2 + 人間向け草案）はすべて保存され、上書きしていない。

## 現状

- EVIDENCE_REVIEWED のみ。HIGH 側の supplement carry 欠損（operation-map §1–§4、capability-review §§3–5 SOURCEGAP_CONFIRMED）により、通常 HIGH prepare→adopt での全 409 改訂は現行では実行不可。Option R の有界 producer 修理（pre-code map＋限定実装＋現行 4 枚のみの独立再 review）が先行条件。
- r2 固定 41 のままでは紙が「未読ゆえ除外」に戻るため、r3 として 45（41＋4 supporting）を DATA で用意した。採用は訂正 accepted 後のみ。

## r3 で足す 4 紙（いずれも PARTIAL AUTHOR_CLAIM、再現・配備の主張なし）

- P1 買い手注意: 16096 Commercial-tax（NV-Embed-v2 CC-BY-NC、13 embedder/8 maker、商用 floor・費用内訳・買い手 checklist）。P1 の値段・SOTA・throughput を修飾する欄外。
- P2 機構背景: 15127 Agentic workload（10 app＋計測、長時間 tool/state/I-O、非 LLM ボトルネック、pay-go 内訳）。P2 の pay-and-collaborate を裏付ける機構欄。
- P2 堅牢注意: 18389 Jagged frontier（SPT 変換で resolve率 最大 6.7pp 低下、6/16 有意、単純 scaffold が堅牢、順位は移転しない）。ベンダー GA 主張への counterweight、単一 P2 配置。
- P4 安全機構: 21100 ReFrame（Evidence 生成＋Rewrite-Routing＋Safe Inference、37.28→45.95 POPE/Math/Physics）。P4 条件部の機構メモ。
- 見送り（明示 HOLD）: 21095 Trustworthy RAG は P4 適性あるが今回は箱の余白なしで HOLD。14927 routing 否定結果・14967 WAN 解析は背景として考慮済み HOLD。

詳細の主張・制限・SHA・節は `w34-four-paper-correction-proposal.json` の replacement_records＋read_ledger（HTML 節・locator・SHA 引用）にある。新 Raw・fetch なし。405 は 15e87eef と同一、4 枚のみ差し替え（手で全 source 再構築しない）。

## 目次 r3（15 target/16 max）

- r2 ベース 14（P1 3＋P2 4＋P3 2＋P4 3＋P5 2、P3 を trio 統合で 2 に締め）に Research-Notes 1 箱（P1 0.5＋P2/P4 0.5、単一箱・最終順）を足して 15 target、overflow 見込みで max 16。自動 17pp ではない。限定 11＋新規 4 はいずれも表題化しない。

## 残る問い（r2 踏襲＋BLOCKED 追加）

- 限定 supporting を囲みに留める判断は妥当か。
- Copilot 3点・Antigravity を snapshot として載せる範囲は。
- CoSnitch を研究者報告として載せるか。
- 21095 を次に足すか、HOLD のままか。
- **BLOCKED を解くための Option R 修理に進むか（Root 指示が必要）。**

## 次に必要なもの

有界 producer 修理の pre-code map→限定実装→現行 4 枚のみ独立再 review→Selection 差分（HOLD→SUPPORTING＋1 箱）→正式 dossier→ARCHITECTURE_REVIEW。承認前 Draft/PDF なし。Type 入力は意味 review 後。

*ピン・範囲は v1 `w34-read-scope-and-pins.json`、r2 triage・body ledger、 configur 計数は `w34-r2-counts.json`、全 DID は `w34-r2-per-did-disposition-machine.json`、訂正 DATA は `w34-four-paper-correction-proposal.json`。*
