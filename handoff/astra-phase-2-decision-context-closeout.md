# Astra Phase 2 — decision-context closeout

記録日: 2026-09-10 JST。Phase 2の判断文脈の補足。architecture authority、production approval、Phase 3の固定仕様ではない。新Evidenceにより変更・破棄できる。

主要な判断・代替案・反証条件は既に[architecture direction decision](../outputs/astra-architecture-direction-decision.md)へ保存済み。未公開の別architecture案や、採用済みのinterface仕様はない。本書はその再要約をせず、後続で判断を誤読しやすい点と調査の到達限界だけを残す。

## 1. 「再設計の理由」のEvidence強度を均さない

参照: [feasibility](../outputs/astra-semantic-handoff-feasibility.md) §4.2、direction decision §2。

判断の根拠には非対称性がある。paperは**persisted accepted outputまで到達した具体的なsemantic defect**を確認した。一方、Selectionのstage結合やDraftingの広いrefs/coverage付与は**現在コードの性質**を確認したもので、同じ強度のproduction事故を追加発見したわけではない。

部分再設計を支持したのは「事故を多数数えたから」ではなく、paper以外にも同種の境界設計を見つけ、局所patchだけでは残る問題と推論したからである。将来この推論を反証するには、全failure史を読み直すより、該当entrypointの実使用と、別経路が既に問題を解いているかを確かめる情報価値が高い。

**留保:** source treeに存在するrunnerと、今後も維持すべきactive callerの集合は同一と確認していない。Phase 2のpath一覧をそのまま置換backlogにしない。runtime callerの利用比率も測っていない。

## 2. A+対Bを不公平な比較にしない

参照: direction decision §3・§4・§8–9。A+は既存canonical形式への直接authoring、Bは共通materializationを伴う案。

A+を「モデルがhashや全boilerplateを一から手入力する不便な方式」に限定してBを勝たせてはいけない。既存resolverや機械的な補助を両案が利用できる条件で、**追加のsemantic入力形式／変換契約に、維持費を払うだけの価値があるか**が未決である。

この比較は別architecture同士の勝敗とは限らない。A+で十分なら、推奨した責任分離を維持したまま新しい入力DSLを作らずに済む。Bを縮小する結果はPhase 2の失敗ではない。

**最初に確かめたい仮説:** authorが意味的な判断だけを明示し、既存機械補助がidentity/basisを扱えば、狭い新DSLなしに必要な精度と使いやすさを両立できるのではないか。これは実行未検証で、採用判断ではない。

## 3. 最初のprototypeで混ぜたくない二つの問い

参照: feasibility §4–6、direction decision §9。

一つは「与えた意味payloadを無損失にcanonical outputへ渡せるか」、もう一つは「Rawから十分な意味payloadを作れるか」である。Phase 2で見たpaperは後者が壊れ、前者は保存に成功していた。

手で正したgold payloadからのround-tripだけを見れば、paper問題を解かずに新経路が成功して見える。逆にLLM抽出と変換を一度に替えると、改善・悪化の原因を分離できない。将来の局所検証では、どちらの問いに答えるEvidenceかを明示したい。これは新しいtest suiteの実装指示ではなく、比較時に失いたくない診断軸である。

**「lossless」の範囲にも留保:** 与えたpayloadの保持と、そのpayloadが研究上十分かは別。全Rawの全情報を必須fieldsへ展開することを意味しない。入力負担を増やして再読を減らしただけなら、全roleを含む費用比較が必要になる。

既知paperのUI phraseを取り除くだけの成功、locatorを付けるだけの成功、CONTEXTのままだから無害という評価は、この区別を飛ばすおそれがある。反対に、この一件からpaper全件の再実行や重大な公開事故を結論してもいけない。

## 4. 後続の調査を短くするための到達点

- **優先して読む入口:** direction decision §1・§8–9 → 問いに応じて§2または§4–7。4 sliceの実物対応が必要な場合だけfeasibility §4–5と[probe結果](../notes/semantic-handoff-probe-results.json)へ進む。Phase A全文や409件の再読を開始条件にしない。
- **probeの意味:** [補助script](../notes/semantic_handoff_probe.py)は固定refのreadと選択したhash/field照合。Core validator、stage revalidation、semantic評価を実行していない。結果の全booleanがtrueでも、quality PASSやcurrent authorityの採用可否を表さない。
- **snapshotの扱い:** helper内のmain/W34/SP001 SHAは固定値。temporary cacheは再取得の節約でありlatest remoteの証拠ではない。将来のcurrent realityは別途read-only確認し、関係する差分だけ追う。
- **原因追跡の深さ:** paperはRaw→edition generator→interactive input→accepted Cardまで追った。C019のhandread行には読解範囲を復元する記録が無い。SP001-D008の元semantic authoringの原因行は追っていない。後二者の未知を「同じparser defect」と補完しない。
- **対外的な事実検証の範囲:** 調べたのはSurvey repository内の表現・binding・生成経路であり、登場する全製品・論文のclaimを外部の最新情報と再照合した調査ではない。保存されたlocatorと検証済みの現時点の外部事実を区別する。
- **別問題として残したもの:** releaseの外部実行状態、全Core依存／監査費、criticのcapabilityと費用は、このPhaseで再実証していない。SP001 branchのFROZENだけから未公開／release阻害を推定しない。

## 5. Phase境界で残す運用上の意図

direction decisionの段階移行図は、全stageの新実装を一度に作る約束ではない。Phase 3で最初に欲しいのは、維持費を含めて成立する境界と、実際に減らせる旧作業があるかの判断である。共通化のために別の巨大なsemantic modelを作り始めた場合、または廃止対象を特定せず新wrapperだけ増えた場合は、進捗ではなく仮説の再評価点として扱いたい。

真剣に比較した代替構成と方向転換条件はdirection decisionに全て記録済みであり、ここに追加の採用優先順位はない。新しいarchitecture investigation、prototype、production対応は開始していない。Phase 2のhandoffをここで完了し、Phase 3の権限は後続のHuman指示で定める。
