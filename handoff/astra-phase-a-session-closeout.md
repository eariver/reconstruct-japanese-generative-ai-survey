# Astra Phase A / refinement session closeout

記録日: 2026-09-09 JST。これは現在の decision context の差分であり、将来の判断を拘束する指示ではない。新しい Evidence、production reality、より良い reasoning により自由に再検討できる。次 Phase の選定・開始はしていない。

主要な判断・仮説・反証条件は既に保存されている。新しい architecture 結論や未公開の代替設計はない。以下だけが、既存成果物から読み取りにくい調査の到達点と運用上の差分である。

## 1. 症状の特定と原因コードの特定は別

Already externalized: [Phase A report](../outputs/astra-phase-a-architecture-review.md) §4.1、§5、および [evidence ledger](../notes/phase-a-evidence.md)。

**EVIDENCE_DEPENDENCY / UNRESOLVED:** W34 について本文・Supplement・Card・plan の乖離は直接確認したが、どの生成スクリプト、prompt、手動判断、変換処理が古い limitation を残したかを、一つの原因行まで追跡したわけではない。したがって「Core が意味を消した」「Worker が本文を読まなかった」のいずれか一つへ原因を確定したと扱わない。残された artifact が十分な意味消費を示さないことが診断の根拠である。

**REVISIT_TRIGGER:** 将来、特定の変換処理が正しい抽出を失っていたと判明すれば、semantic product の必要性と、その修復を担う層・優先度を別々に再評価できる。この区別は、狭い修復を選ぶ場面で有用である。

## 2. Reviewer の実行可能性は未検証

Already externalized: [refinement](../outputs/astra-phase-a-architecture-refinement.md) §4、§5、§9.4。

**ASSUMPTION / UNRESOLVED:** 推奨 topology は、選ばれた critic が必要な exact source と plan を実際に読めることに依存する。本セッションでは外部 critic を一度も実行せず、private repository の参照、資料 packet の受渡し、source locator の往復、exact PDF の読取を end-to-end に試していない。Human-reported subscription availability は、これらの capability が揃う証拠ではない。

**REVISIT_TRIGGER:** packet 作成・手動転送・資料再取得が大きい場合、model 自体の推論費が低くても topology の総費用優位は失われ得る。これは model-family の品質比較とは分けて評価する必要がある。どの transport を採用するかは未決定である。

## 3. 「実装設計可能」は既存構造との対応調査を済ませた意味ではない

Already externalized: refinement §6、§7、§10。後続の Sol guards は [post-refinement discussion](../context/2026-09-09_post-refinement-human-sol-discussion.md) §3.5 に保存済み。

**UNRESOLVED:** 消費記録の概念を既存 source/Evidence のどの field に置くか、どの projection を追加すれば足りるかについて、網羅的な field-by-field mapping は作っていない。五つの logical products も新しい五組の保守対象を追加する承認ではない。設計上の境界は定まったが、最小の物理変更量は未確定である。

**EVIDENCE_DEPENDENCY:** 次にその論点が必要になったときは、当時の固定 schema ではなく、その時点の current schema/producer/consumer の対応が決定材料になる。調査時に見た source-consuming output の不足と、新しい正本を増やす必要性を同一視しない。

## 4. このセッションで有効だった読み方

**OPERATIONAL_LESSON:** 初期に複数の長い文書と広い path 一覧をまとめて出力した際、tool output が切れた。指定 path・function・artifact を絞った後の読み取りで必要な情報を得られた。将来は、調査済み領域の全文を先に再ロードするより、下記参照先から必要な節と固定 artifact を選ぶ方が、同じ探索を繰り返しにくい。

これは allowance 節約率を測定した結果ではない。セッション長、tool 数、token 数と credit 消費の対応は本セッションで計測しておらず、その因果を handoff から補完しない。Git の未同期回復とその後の検証は post-refinement discussion §1–2 に既に保存されているため、ここには再掲しない。

## Suggested selective reload order

1. **First:** 本ファイル。追加の未外部化された architecture 決定はないことと、上記の未検証範囲を確認する。
2. **Second:** [refinement](../outputs/astra-phase-a-architecture-refinement.md) §1・§10。具体的な問いに応じて §3–9 の該当節だけを読む。
3. **Review context が必要なとき:** [post-refinement discussion](../context/2026-09-09_post-refinement-human-sol-discussion.md) §3.5・§4。Sol の guards と Human の意図を、Astra の決定・production approval から区別する。
4. **Evidence または原診断を再検討するときだけ:** [evidence ledger](../notes/phase-a-evidence.md) → 必要な固定 upstream artifact。[Phase A report](../outputs/astra-phase-a-architecture-review.md) は該当する診断・代替案の節に限る。全 probe の再実行や全史の再読を開始条件にはしない。
