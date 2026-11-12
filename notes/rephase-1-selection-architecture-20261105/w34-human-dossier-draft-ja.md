# W34 人間向け Architecture ドラフト（案・未承認） — 2026-W34 週次誌

**位置づけ:** 著者 DATA 案のみ。独立 research/selection review・Architecture 承認・Human Gate・Draft/PDF は未了。原文状態は `EVIDENCE_REVIEWED` のみ。数値・日付の限定を隠さない。

## 対象と読み方

- 対象週: 2026-08-14 18:00-04:00 〜 08-21 18:00-04:00（UTC: 08-14T22:00Z 〜 08-21T22:00Z）。Aug14・Aug21 の日付のみ記述は 22Z 境界との前後が確定しないため、本文では「日付レベルのみ、時刻未確定」と明記し、週確定イベントとして断定しない。
- 証拠: Evidence 409（38 VERIFIED / 363 PARTIAL / 8 NEEDS_MORE）、Ledger 439、義務 3 LIMITED。VERIFIED/PARTIAL 等は既存ラベルであり、新規 PASS ではない。ベンダー数値は未再現、前提は本文の限定どおり。

## 今号の主張（案）

**W34 は「配布と統治の週」——新奇モデルより、使える場所・値段・支払い・協働・安全条件が動いた。**

1. フロンティアの届き方・値段が変わった（Bedrock 展開、Sol プロモ、DeepSeek 改定、Alibaba 台帳）。
2. エージェントの「払う・共働」が GA 化（Payments、Computer Use/Skills/Files、Slack Code、Agentic Search）。
3. 企業導入面が IDE/チャット/管理に着地（Computer History 拡張、Messages、Copilot 3点は snapshot 限定、Antigravity は束/追加を分離）。
4. 安全・統治が条件を締めた（Astra pacing、ZDR/Private Safety、Teens、KEV 台帳、CoSnitch は研究者報告限定、水印は日付限定）。
5. 資本・計算・創作流通が裏で動いた（PORTS-Pike 8GW、Stripe/OpenRouter、Firefly、Pika は日付限定）。

技術約6割・ビジネス約4割。ベンダー誇張（○倍・SOTA・安全-fashioned）は事実として採用しない。

## 目次案（16–18pp 想定）

- P1 フロンティア配布・価格 (4pp): Sol 料金 / Grok・GPT-5.6 の Bedrock / DeepSeek 改定 / Alibaba 台帳 / Imagen 移行。Qwen・Vision-Exp・地域処理・Grok 拡張は日付限定囲み。
- P2 エージェント基盤 GA (5pp): Payments / Computer Use / Slack Code / Agentic Search / Alipay・Dogwood・Runway。AgentCore 系は1囲みに統合。
- P3 企業開発面 (3pp): Computer History / Messages（範囲限定）/ Copilot 3点（9/8 snapshot 限定）/ Antigravity（8/20 束は確定、8/21 追加は限定）/ CLI・Replit。
- P4 安全・統治 (3pp): Astra / ZDR / Teens（観測日）/ KEV（台帳のみ）/ CoSnitch（研究者限定）/ 水印（日付限定）/ Defender 随想は枠外解説。
- P5  infra・経済・創作 (2pp): PORTS-Pike / Stripe 買収 / Firefly / Pika（日付限定）。
- Paper Watch: なし（319 arxiv は hash のみ・maker 報告・未再現のため。19x 集中は重複論文ではなく別体裁、数は十分性ではない）。

## 選ばなかったもの（負の空間）

- HOLD 10: Benchmarks 実体なし、Vera Rubin 一次なし、SenseNova 時期不確定、MediaTek 一次なし、MOU 本文なし、Kling 実体 51–79字のみ、Ox 仕様未確定など。いずれも一次証拠なしでは昇格しない。
- DROP 30: カバレッジ API ノイズ 5、重複 4（Grok 配布・Grok Build・Dogwood・Nemotron は代表に統合）、 carry-over C076/77（Music 3.0 8/13・H3 8/3 で週外、昇格・backfill なしをここで明示処分）、他 19 は週外・重複・定常ノイズ。
- CONTEXT 358: 319 arxiv＋39 非arxiv は背景として保持、特集化しない。GLM-5.3、科学論文、DSpark、UI-Mate 等は高信号でも日付・一次・範囲の限定が残る。

## 残る問い（Human が躊躇すべき点）

- Aug14/21 の時刻境界が日付のみで確定しない 11 件を表題化しない判断は妥当か。
- Copilot 3点・Antigravity 追加を「観測 snapshot」として載せる範囲は妥当か、落とすべきか。
- CoSnitch を研究者報告として載せるか、見送るか。
- Paper Watch なし（arxiv 追加パッケージ見送り）は妥当か、全面消費への投資を別途行うか。
- 不足一次（MSRC、Aug21 時刻ヘッダ、Copilot 当日 bytes、Aug21 一覧 bytes）を今取る必要があるか（案としては不要、限定付き掲載で足りると判断）。

## 次に必要なもの

独立 research/selection review を経て、正式 Architecture dossier（12 項目）を humaines に提示し、ARCHITECTURE_REVIEW の APPROVED/REQUEST_CHANGES を受ける。Draft/PDF は承認前は作らない。

*出典ピン・読解範囲は `w34-read-scope-and-pins.json`、全 DID 表は `w34-per-did-disposition-machine.json`、 substantive 根拠は `w34-selection-proposal.md`。*
