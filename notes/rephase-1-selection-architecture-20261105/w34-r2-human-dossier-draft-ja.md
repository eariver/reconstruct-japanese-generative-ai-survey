# W34 人間向け Architecture ドラフト r2（案・未承認） — 2026-W34 週次誌

**位置づけ:** 著者 DATA r2。v1 を保存し、独立指摘 F1–F5 を反映。独立 re-review・Architecture 承認・Human Gate・Draft/PDF は未了。38V/363P/8N 等は既存ラベルであり新規 PASS ではない。

## 対象と読み方（変更なし）

- 週: 2026-08-14 18:00-04:00 〜 08-21 18:00-04:00（UTC 08-14T22Z〜08-21T22Z）。Aug14・Aug21 日付のみは 22Z 前後未確定のため「日付レベルのみ」と明記し週確定として断定しない。Sep8 snapshot（Copilot 3点）・Aug21 追加（Antigravity）・研究者限定（CoSnitch）も表題化しない。

## 今号の主張 r2（分布と統治の週、14–15pp に締める）

**W34 は配布と統治の週。** 新奇モデルより、使える場所・値段・支払い・協働・安全条件が動いた。v1 16–18pp を 14–15pp に締め、資料・how-to 6点を P2 の1囲みに統合し、限定 11点を欄外・囲みに留める。

- P1 配布・価格 3–4pp: Sol 料金 / Grok・GPT-5.6 の Bedrock / DeepSeek 改定 / Alibaba 台帳 / Imagen 移行。Qwen・Vision-Exp・地域処理・Grok 拡張は日付限定囲み。
- P2 エージェント基盤 GA 4pp（最大）: Payments / Computer Use / Slack Code / Agentic Search / Alipay・Dogwood・Runway。AgentCore 系は1囲み。機構変化が最大のため最大配分。
- P3 企業面 2–3pp: Computer History 拡張 / Messages（範囲限定）/ Copilot 3点（9/8 snapshot 限定1囲み）/ Antigravity（束と追加を分離、単一 SUPPORTING）/ CLI・Replit。
- P4 安全・統治 3pp: Astra / ZDR / Teens（観測日）/ KEV（台帳のみ）/ CoSnitch（研究者限定）/ 水印（日付限定）。Defender 随想は枠外。
- P5 infra・経済・創作 2pp: PORTS-Pike / Stripe / Firefly / Pika（日付限定）。
- Paper Watch: なし。319 arxiv は全点 triage（ lane・score・日付・抄録で分類）＋26体本文読みの上で、手法知見としては確認したが週イベントとしての昇格なし。180集中は別論文の別体裁であり数は十分性ではない。将来の全面消費は補足箱にはなり得るが現 core を置き換えない。

## 負の空間 r2（本文で読んだ上で落とす）

- HOLD 10: 一次証拠なしでは昇格しない（Benchmarks 実体、Vera Rubin 一次、SenseNova 時期、MediaTek 一次、MOU 本文、Kling 実体 51–79字、Ox 仕様、Seedance 背景、恋愛詐欺イベント性、委任合成）。
- DROP 30（Matrix 外）: カバレッジ API 5、重複 4（c067 は c025 背景＋c066 限定に無損失で継承、他は代表に統合）、carry-over C076/77（8/13・8/03 週外をここで明示処分）、他 19 週外・重複・定常ノイズ。いずれも task なし、割当不可。
- CONTEXT 368（Matrix 内 HOLD）: 319 arxiv は分類別理由（符号・日付・重複）で保持、39 非arxiv は各点理由（GLM 旗艦日付、Mythos 成果、DSpark 速度、UI-Mate 出所、Build 対応、AutoDesign 分割等）。高信号も時期・出所・再現の限定が残るため表題化しない。
- 26体本文読みの要点: 経路選択・WAN・FZ-VLM・Agentic workload・Commercial-tax・memory 系・code 堅牢・eval・安全はいずれも手法として成立するが、 maker 報告・未再現・W34 配備なし。週イベント化に足る負荷は確認できず、昇格見送り。上流改訂が必要な材料はなし（昇格時に DID・主張・場所・SHA を添えて Root へ返す運用）。

## 残る問い（Human が躊躇すべき点、v1 踏襲）

- 限定 11点を囲みに留める判断は妥当か、落とすべきか。
- Copilot 3点・Antigravity 追加を snapshot として載せる範囲は妥当か。
- CoSnitch を研究者報告として載せるか。
- Paper Watch なしは妥当か、別途全面消費に投資するか。
- 不足一次（MSRC、Aug21 時刻、Copilot 当日 bytes、一覧 bytes）を今取る必要があるか（案としては不要）。

## 次に必要なもの

独立 re-review を経て正式 dossier（12項目）を提示し ARCHITECTURE_REVIEW に進む。承認前 Draft/PDF なし。Type 入力は意味 review 後。

*ピン・範囲は v1 `w34-read-scope-and-pins.json`＋ r2 triage・body ledger、 configur ation 計数は `w34-r2-counts.json`、全 DID は `w34-r2-per-did-disposition-machine.json`。*
