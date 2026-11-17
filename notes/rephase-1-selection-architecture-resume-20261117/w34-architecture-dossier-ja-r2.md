# W34 人間向け Architecture ドラフト R2（レビュー著者 DATA・未承認）— 2026-W34 週次誌

**位置づけ:** 独立 substantive レビュー著者 DATA R2。R1 ドラフトの上書きではなく訂正版。Human 承認・R4・Production・Draft/PDF・品質非劣化の主張ではない。正準レビューコミット NOT ESTABLISHED。承認依頼なし。Root が stage dispatch 前に審査する。実ソース `3231a0c…` と将来正準 Human レビュー対象を区別する。R1 の「41 VERIFIED PRIMARY」「0.5 slack 合計」「c001 Aug18 要約」「720 counts のみ」は本 R2 §0/§1/§4/§5 で訂正し、R1 は superseded として保存する。

## 1. 正確なレビュー対象

- 実インスタンス: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`、ソース記録のみ `3231a0c…/ae0dd1e…/ff01b73…`。
- State `EVIDENCE_REVIEWED`（`a8586351…`）、PREARCH `73ab28ea…` R2、4 refs のみ。旧 canonical inactive。PREARCH cleanup completion と研究 completeness LIMITED は別物として保持。
- 7 点は `READY_FOR_ARCHITECTURE_REVIEW`（Matrix/Selection/Architecture/Summary/Attention/Input/Audit）。Architecture `PROPOSED`、human_review null。7 点 bytes+SHA は本 R2 で stdlib 再確認（§1 参照、R1 の matrix 誤記訂正）。
- 将来正準コミット未確定。現 3231 を承認済みとしない。

## 2. 調査カバレッジ

- Discovery 439、Screening 439（DROP30/INSPECT200/KEEP73/MAYBE136）、Evidence 409（VERIFIED38/PARTIAL363/NEEDS_MORE8）、Views 409（MATERIAL45/CONTEXT354/HOLD10）、Ledger 439。Window `[2026-08-14T22:00Z,08-21T22:00Z)`。
- 770 inventory はレビュー DATA `w34-attention-inventory-r2.json`（全行 stage/subject/DID/現 disposition/role/materiality/evidence/attention reason/shown-overflow/risk flag）。正準 attention 生成ではなく writer なし。shown50（MATERIALITY40＋SCREENING DROP10）、overflow720（SCREENING356＋SELECTION364）。counts のみではない。

## 3. 証拠品質・消費

- SELECTED 45 の実際: PRIMARY24 全 VERIFIED/MATERIAL、SUPPORTING21＝PARTIAL15＋VERIFIED6。合計 VERIFIED30＋PARTIAL15。vendor41＝24＋11＋6、残り4紙 PARTIAL。R1 の「41 VERIFIED PRIMARY」は誤りとして撤回。
- 4 紙は AUTHOR_CLAIM のまま bounded box（保持 captures 再利用、再現なし）。KEV/MSRC shell は captured-but-unconsumed。Meta Mac は NOT_FOUND、Grok Vertex は RETRIEVAL_FAILED（未取得からの推測なし）。c001 は Aug18 entry と Aug14 信号の差異＋22:00Z UNRESOLVED を正確に保持（R1 要約訂正）。
- 新規読み: 14 件の evidence task（claims/limitations/verification）＋matrix/selection 行。SHA の存在を消費としない。残り ~293 は hash-only で PASS 主張なし。inventory 列挙 ≠ 全文読了。

## 4. 主要候補マップ

- 45（24P＋21S、単一配置、重複・HOLD 混入なし）。P1 12、P2 13、P3 8、P4 8、P5 4。Memory JSON は P2 PRIMARY 単一、c102 は P3 SUPPORTING 単一。21095 は明示 HOLD。
- 高 signal HOLD 8 VERIFIED/CONTEXT（c027/c028/c029/c032/c034/c036/c046/c095）は背景に留め PRIMARY 化なし。不適格10 は NEEDS_MORE8＋PARTIAL/HOLD2。

## 5. 負の空間・不採用理由

- HOLD364＋nonMatrix30。各 HOLD は lane/score/date/cluster/個別 body bytes。c001/c009/c013/c015/c027/c028/c032/c050 および高 score arxiv 14927/15008/18591/19534/20999/21095 は evidence card で根拠化（§5 参照、timing・vendor 計測・repo-first・method-without-event 等）。汎用テンプレの繰返しは開示（screening は per-DID title 付き、selection HOLD は個別 prefix＋繰返し suffix、ledger HOLD は最小）。
- 未読 body から別 core があり得ないとは主張しない。compression は reviewed scope に限定した counterfactual のみ。

## 6. 編集テーゼ

- W34 は配布と統治の週。30 VERIFIED を核に、11 vendor PARTIAL＋6 VERIFIED box＋4 紙 box で補う。表題化・配備主張なし。

## 7. Architecture packages

- P1→P5 順序、P3 trio 締めは編集判断。箱は5 package 内提示。must_cover・boundaries・section_label を継承。PARTIAL の timing-UNRESOLVED、vendor 記述、X lead 限界を境界に明記。

## 8. ページ配分

- 3+4+2+3+2=14＋箱1＝15 target 正、max16 slack 合計1（package 0.5 許容は合計0.5ではない、R1 訂正）。未製本、旧2pp 基準を品質 PASS にしない。15pp 未描画。

## 9. 対抗案

- 6th 技術 box は補足に留まり core 置換なし（reviewed scope 限定）。Sparse 1-package 棄却。21095 次点 HOLD 維持。

## 10. 既知の限界・リスク

- 時刻精度、Sep8/Aug26 の primary-date 化不可、MSRC/NVD・KEV HTML 未消費、vendor 数値 methodology 非開示、~293 hash-only、720 overflow 未精読（列挙のみ）、lifecycle net UNKNOWN。
- 躊躇点: SUPPORTING 限定・snapshot 範囲・CoSnitch 研究者限定・21095・15/16 締め。

## 11. Sol 所見

- **EDITORIAL_READY_FOR_NORMAL_STAGE**（bounded、通常 validation/checkpoint への dispatch 可否のみ）。系統的缺陥の DID 返却なし、新規 fetch・source code 提案なし。Human/R4/Production/品質の承認ではない。

## 12. Human 選択肢（将来の説明のみ）

- 将来 ARCHITECTURE_REVIEW で `APPROVED`/`REQUEST_CHANGES` を選べる。通常 checkpoint 通過後に Root dispatch を経て提示。本書は事前 DATA で承認を求めない。正準コミット・Draft/PDF・R4 は範囲外。Ordinary Commit/Push は Human 所有。内部 unit のため追加 Human Commit Point は要しない（root §21）。
