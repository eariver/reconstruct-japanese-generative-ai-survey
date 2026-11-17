# W34 人間向け Architecture ドラフト（レビュー著者 DATA・未承認）— 2026-W34 週次誌

> SUPERSEDED R1: root §§1–2 により未採用。訂正版は `w34-architecture-dossier-ja-r2.md` + `w34-substantive-review-r2.md`。R1 は履歴として保存。

**位置づけ:** 独立 substantive レビュー著者 DATA。Human 承認ではない。R4・Production・Draft/PDF・品質非劣化の主張ではない。正準レビューコミットは NOT ESTABLISHED。承認依頼はしない。Root が stage dispatch 前に本書を審査する。実ソース実行コミット `3231a0c…` と将来の正準 Human レビュー対象コミットを区別する。

## 1. 正確なレビュー対象（exact review identity）

- 実インスタンス: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work`
- ソース: `3231a0c280287411513bba359f4d3d2b6703f591`（parent `ae0dd1ee…`、tree `ff01b73e…`、記録値、fresh Git 証明なし）
- State: `EVIDENCE_REVIEWED`（`a8586351…`）、PREARCH `73ab28ea…` R2、4 refs のみ（Evidence/Views/Ledger/Completeness）。旧 canonical は inactive。
- 出力 7 点は `READY_FOR_ARCHITECTURE_REVIEW`（Matrix/Selection/Architecture/Summary/Attention/Input/Audit）。Architecture は `PROPOSED`、human_review null、State は未進行。
- 将来の正準レビューコミットは未確定。現 3231 を Human 承認済みとして扱わない。

## 2. 調査カバレッジ（research coverage）

- Discovery 439、Screening 439（DROP 30/INSPECT 200/KEEP 73/MAYBE 136）、Evidence 409（VERIFIED 38/PARTIAL 363/NEEDS_MORE 8）、Views 409（MATERIAL 45/CONTEXT 354/HOLD 10）、Ledger 439。
- Window は UTC `[2026-08-14T22:00Z, 08-21T22:00Z)`。OUT_OF_WINDOW は正しく HOLD。
- 残差: 22:00Z の時刻精度が日付限定で UNRESOLVED のもの多数（§10 参照）。MSRC/NVD、Aug14/21 時刻、Sep8 entry bytes 等は確定見出し化に必要な場合のみ将来 scope。現 SUPPORTING 限定表示には不要。

## 3. 証拠品質・消費（evidence quality）

- 重要一次 41 は VERIFIED first-party として消費し PRIMARY に据えた。PARTIAL 11＋新規 4 は SUPPORTING に留め、status upgrade・表題化・配備主張なし。
- 4 紙（15127/16096/21100/18389）は AUTHOR_CLAIM のまま bounded box に留めた。本文は保持 captures のみ再利用（314048B/414077B/711224B/388712B、literal spans は既存 dossier で検証済み）。再現・有意性・holdout なしを明記。
- KEV HTML 281KB・MSRC 2717B は captured-but-unconsumed として区別。AUTHORITY_NOT_FOUND（Meta Mac 等）、RETRIEVAL_FAILED（Grok Vertex listing）、CAPTURED_BUT_UNCONSUMED、CONSUMED の 4 区分を維持。
- ~293 arxiv は hash-only であり full semantic PASS を主張しない。26 体読み＋triage を履歴として再利用。inventory scan ≠ full corpus read。

## 4. 主要候補マップ（major candidate map）

- SELECTED 45（24 PRIMARY＋21 SUPPORTING、単一配置、重複・HOLD 混入なし）。
- P1 配布・価格 12、P2 エージェント基盤GA 13、P3 企業面 8、P4 安全・統治 8、P5  infra・経済・創作 4。
- Memory JSON は P2 PRIMARY 単一、c102 は P3 SUPPORTING 単一、dual-role なし。4 紙は各1配置。
- 21095 Trustworthy RAG は明示 HOLD（箱余白なしの counterfactual）。

## 5. 負の空間・不採用理由（negative space）

- HOLD 364（不適格 10＋CONTEXT 354）＋nonMatrix 30。各 HOLD は lane/score/date/cluster/個別 body bytes を付す。機械的 HOLD ではない。
- 高 signal HOLD は時刻・典拠で明示遮断（GLM-5.3 時刻未確定、Mythos dual-use、DSpark vendor 計測、UI-Mate repo-first、Build locator 不一致、AutoDesign 有意性不足 等）。
- 汎用文の繰返しは残るが、個別 body/SHA・lane・cluster・日付で緩和。720 attention overflow は counts で計上し、50 shown のみ精読（§8 の方法を開示）。

## 6. 編集テーゼ（editorial thesis）

- W34 は配布と統治の週。新奇モデルより、使える場所・値段・支払い・協働・安全条件が動いた。VERIFIED core を置換せず、表題化せず、再現・配備を主張しない。

## 7. Architecture packages（順序・役割・境界）

- 順序 P1→P2→P3→P4→P5。P3 trio 締めは編集判断。Research-Notes 箱は 5 package 内の提示であり 6th package ではない。
- 各 package の must_cover・boundaries・section_label を継承 Evidence 境界とともに保持。PARTIAL の timing-UNRESOLVED、vendor 記述、X lead の限界を境界に明記。

## 8. ページ配分（page allocation）

- 3+4+2+3+2=14＋箱1＝15 target、max 16（0.5 overflow 許容）。算術正、provisional、未製本。
- 旧 2pp 圧縮基準を現品質 PASS として扱わない。実際 15pp は未描画。Draft/PDF/visual QA なし。

## 9. 対抗案（counterfactual）

- 6th 技術 package は補足箱になり得るが現 core を置換しない。Sparse 1-package は VERIFIED デルタ無視で棄却。21095 を次に足す案は HOLD のまま残す。

## 10. 既知の限界・リスク（limitations and risks）

- 時刻精度（Aug14/21 の 22:00Z 境界）、Sep8 snapshot の primary-date 化不可、Aug26 再日付ページの Aug21 典拠化不可、MSRC/NVD 未消費、KEV HTML 未消費、vendor 数値の methodology 非開示、~293 hash-only、720 overflow 未精読、lifecycle net UNKNOWN。
- 躊躇点: SUPPORTING 限定・Sep8 snapshot 範囲・CoSnitch 研究者限定・21095 次点・15/16 締めの妥当性。

## 11. Sol 所見（review finding）

- **EDITORIAL_READY_FOR_NORMAL_STAGE**（bounded substantive 判断）。BLOCKING の系統的 research 缺陥なし。CHANGES_REQUIRED なし。新規 fetch・source code 提案なし。
- Human/R4/Production/品質非劣化の承認ではない。Root 審査前の著者 DATA である。

## 12. Human 選択肢（将来の説明のみ、承認依頼ではない）

- 将来 Human ARCHITECTURE_REVIEW では `APPROVED` または `REQUEST_CHANGES` を選べる。通常 checkpoint 通過後に Root dispatch を経て提示される。本書はその事前 DATA であり、現時点で承認を求めない。
- 正準レビューコミット確定・Draft/PDF・R4 は本 unit の範囲外。Ordinary Commit/Push は Human 所有。Human Commit Point で停止。
