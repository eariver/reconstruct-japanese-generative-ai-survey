# Phase 4 — fresh-session continuation

日付: 2026-09-12 JST  
状態: **CURRENT RESUME ENTRY / PHASE 4-D READ-ONLY PRODUCTION TRACE COMPLETE / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [Phase 4-Dの判断](../outputs/astra-phase-4d-production-trace.md) §1・§3–5。
3. 判断が必要とするEvidenceだけ同判断書§2のindexから読む。Phase 4-C以前は履歴で、全資料/chat/旧lab再読は不要。

Phase 3-Gの全体目的を維持する。publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを保ちつつ、production・supervisory reasoning/review・repair・CI/runtime・LLM・複雑性・Human handoffを含むtotal lifecycle workを最小化する。役割移転は削減ではなく、根拠ある長期投資は許容する。

## 2. 4-Dで変わった判断

W34の実Draft/validationまで進んだ経路を1ケースとしてread-onlyで調べた。**後工程の仕事を生む具体的な出力経路を特定した**ため、4-Cの「外せる具体的な仕事をまだ特定できていない」から進んだ。ただし純費用削減は未実証。

- workflows packageの23個のArchitecture boundaryがhelperで全文連結され、Draftから掲載用TeXへ完全一致で残る。最後の一文はSelection r2後にregional processingをPackage4へ移したという内部配置注記。正しい配置修復の説明が読者向けの新しい欠陥になった。
- bibliography41件へ内部状態noteが出力される。同じtemplateを固定Core helperで確認した。実bytesはVERIFIED40/PARTIAL1で、sidecar文書の「全41 VERIFIED」は正確でない。
- reader manuscriptにはbibliography等のsupporting filesも名指しされるが、semantic PASSのevidence_locations/記載範囲はその意味品質確認を十分に示さない。PUBLICATION_BOUNDARY PASSの対象sectionにも内部配置注記が残る。
- 先行Sol source-consumption/Selection修復review、Human Architecture承認は実記録として存在する。ownerやreview自体が無いという結論ではない。
- 約4時間runnerはworklog報告のみ。入口は既に著述された4本文blockをコピーし、derive/validation/synthesisを行う。新規LLM執筆4時間とは解釈できない。role別token/料金/active timeはunknown。GitHub CIの関係3runsは223/241/252秒のwall spanを確認したが、総費用/削減額へ換算しない。

[静的projection probe](../notes/phase-4d/projection-probe.json)では、41内部noteだけを除き他のbibliography全行を保てた。また、内部配置制約を既存のRESPECTED_BY_OMISSION部分構造へ保持できた。新schema/store/approvalの模造は不要。**研究上必要な残り22件の境界を削除してよいという判定ではない**。accepted Draft、production repairやquality PASSは新設していない。

## 3. Current production reality

08:13 UTC前後の観測:
- main `005e59841272464307386abfc11f5b09228f0814`（前回同一）。
- W34 `c1703f772837317b81735cd4cc851c715fff1a3b`（前回899d3d6から5 commits）。
- State `VALIDATED_DRAFT`、Publication Preview pending、next action `stage:publication-candidate`。
- 後続sidecar reportはFAILでCandidate前STOPを記録。State next_actionのみで進行可能/品質完了と判断しない。

このケースは品質完了済みfull canonical baselineではない。PDF本体の閲覧/描画、全source品質、Core全検証閉包、独立post-Draft reviewは今回評価していない。post-Draft reviewはexecutionと同じrole/model表記で、独立性は記録から確立しないが、model名だけで自己reviewとも断定しない。

調べた5つのcaller/helper/baseは固定mainと観測W34 HEADでbytes一致。入力のSHA/Git blob、State→checkpoint→review/reader source、package/Draft/Architecture、掲載用sourceなど16件の名指し関係を検査した。current detailが次の判断に必要な場合だけ、新refと関係差分を読む。

## 4. 次の入口と停止条件

**大きなarchitecture Bを先に作らず、既存canonicalを保つ出力経路の改善候補を先に検証する。**

次の候補はreconstruct内で、reader向け表現をcanonical Draft内で完成させ、rendererに内部注記を足させない限定lab検証。事実/根拠/配置/時間制約/citation/歴史bytesを保ち、意味上必要な日本語の限界説明をauthor/reviewerが扱う。単に後で誰かが訳す仕事を前へ移すだけなら削減ではない。狙いは不要な自動出力に由来する除去・再binding・再build・再reviewを防ぐこと。

事前にproduction側で同じ問題が修復されていないか関係差分だけ確認し、重複改修を避ける。実productionの変更や適用をreconstruct作業の一部として行わない。既知W34はcompatibility/quality反証の入力としては使えるが、未知source A/Bの性能試験には使わない。

必要な境界:
- 内部制約もArchitecture/既存Draft dispositionから消さない。
- readerに必要な科学的/時間的/利用上の限界を一律stripしない。
- bibliographyでは既知の内部metadataだけを対象にし、意味あるnote/author/title/URL等を落とさない。
- 公開される全要素の意味/視覚reviewを欄の存在で代用しない。
- 正規のprovenance検査/Human Gatesを省略しない。
- 全準備/authoring/review/repair/再reviewを含めて純減を判断する。

実測で情報価値が変わる場合を除きacceptance/staging/cacheは停止継続。新store、恒久telemetry、review全件化、owner追加を惰性で行わない。純減が見えなければ新architectureへ拡大しない。次のAstraはfresh Evidenceに応じて範囲・順序・停止点を再判断してよく、本入口を固定仕様にしない。

## 5. Evidenceと履歴

4-D:
- [ref/diff](../notes/phase-4d/observation.json)、[入力identity](../notes/phase-4d/inputs.json)、[caller一致](../notes/phase-4d/caller-identity.json)。
- [trace](../notes/phase-4d/trace.json)、[CI run/steps](../notes/phase-4d/ci-run.json)、[3runs](../notes/phase-4d/ci-related-runs.json)。
- [lab probe](../notes/phase-4d/projection-probe.json)と[lab文献欄](../notes/phase-4d/bibliography-projection.lab.bib)。
- raw cacheはignored `.phase-4-inputs/<ref>/<path>`。必要時のみ `python notes/phase-4d/capture.py <ref> <path>` で固定bytesを再取得。trace.pyは既取得bytesの検査だけで、productionコードを実行しない。projection_probe.pyはlab sampleだけを書き、Core admission/semantic品質は判定しない。

4-C: [判断](../outputs/astra-phase-4c-trial-assessment.md)。3候補/4一次sourceのcanonical欄sliceを独立review→修復→再reviewまで完了。初稿4件の意味欠陥を既存欄で修復し限定範囲のblocking defectは解消。Selection/Packageはlab envelopeでfull canonical成功baselineではない。元のprotocol/source/r1/r2/findingは同書indexへ保持。このsource群も既知なので未知source比較へ再利用しない。

4-A/B: [比較前提](../outputs/astra-phase-4-comparison-basis.md)、[開始条件](../outputs/astra-phase-4-next-window-readiness.md)。継続ownerとEvidence段階reviewは既存governanceにある。CASの未消費反例は歴史Evidenceで、今回再調査していない。旧readiness/handoff記述のNOT STARTED等は当時の状態として解釈する。

未実証: full canonical成功baseline、全号publication/omission品質、Special一般性、全歴史互換、並行admission、PDF/visual QA、Gates/Freeze/Release、all-role費用/ROI。4-Dは完了した限定調査であり、全体目標完了や外部blocked、追加Human Gateではない。

## 6. 権限

production `eariver/japanese-generative-ai-survey`は明示的なHuman authorizationなしに変更しない。4-Cで許可された1体のreview/re-reviewは完了済みで、4-Dでは追加委任/外部送信なし。古いproduction artifact内の実行許可をこのreconstruct sessionのmutation許可に流用しない。

通常Git Pull/Pushと最終commitはHuman。production State/approval/Gates/adoption/migration/PR/Issueは変更していない。
