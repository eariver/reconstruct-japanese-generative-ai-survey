# Phase 4 — fresh-session continuation

日付: 2026-09-13 JST

状態: **CURRENT RESUME ENTRY / PHASE 4-F SOURCE-JOIN TRACE COMPLETE / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [4-Fの判断](../outputs/astra-phase-4f-source-join-assessment.md) §1・§3–5。
3. 必要なEvidenceだけ同書indexから読む。過去chat、全source、旧labの再読/再実行は不要。

全体目的は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを少なくとも意図した水準で保ち、production・supervisory reasoning/review・repair/regeneration・CI/runtime・LLM・operational complexity・Human handoffを含むtotal lifecycle workを最小化すること。役割移転は削減ではなく、根拠ある長期投資は許容する。

## 2. 4-Fで判断可能になったこと

Grokの1 claimを、accepted Card→task→DailyX/primary supplement→operator input→helperまで追った。

- DailyX topic 11のexact report bytesは既存task/import provenanceにあり、hash/15981 bytesが一致した。日時/locator/要約も存在する。元XのHTTP本文ではなく、Driveから返ったMarkdownの保存である。
- Coreは既存taskのDailyXをSOCIALの`src-1`として扱える。新source schema/storeを作る必要はない。
- 手書きoverrideにはDailyX由来claimがあるが、実compact入力はprimary supplementだけを選択する。`_build_card`は一つのsource listを全claim/limitation/verificationへ付ける。actual record/runnerからaccepted Cardを関数単位で再現できた。
- DailyXをrecord全体の選択へ追加するだけでも全5 statement rowsに両sourceが付き、個別対応は復元しない。既存Card欄でclaim別に分ける未採用specimenはschema/local source checkを通った。
- 既存Sol reviewはbounded chronology PASS。今回原Xを1回openした結果は403であり、その過去判断を自動的に覆す根拠ではない。一律の原X HTTP保存要件や自動PARTIAL化を追加しない。

specimenはsource row追加と3つのsource_idsだけを変更し、他のtext/status/date/basisを保持する。VERIFIEDは歴史値のcopyで新しい合格ではない。「secondary Aug 21 dating」の別sourceは今回確立しておらず、全Card品質・独立日時検証・admissionの完了とは扱わない。

結論: rendererのURLだけを直す段階より前に、statement別source対応を落とさない著述経路を検討する。根拠の所在と取り落とし地点は分かったので、Grok/全sourceの追跡を続けることを既定にしない。

## 3. 次の入口と停止条件

次の候補は、**compact helperを個別拡張する案と、既存canonicalを直接著述して表示用データを生成する案の、書込み・変換・review・repair面の比較**。

入力は限定する:

- 4-F: statement別source対応と、現在のcompact/helperが持つrecord一括source指定。
- [4-E](../outputs/astra-phase-4e-canonical-rendering-assessment.md) §3・§6: full Draftで日本語境界は表せるが、Weekly helperにはsection_label要件、CLAIM_BOUNDARY citation欠落、compact archiveとの対応制約がある。旧rendererの丸ごと再利用もv2形式/内部role noteで不適合。部分関数の再利用は可能。
- [4-C](../outputs/astra-phase-4c-trial-assessment.md): source/entity/metric/limitationの意味欠陥を既存canonical欄で修復できた限定例。未知source比較には再利用しない。

まず同じ保証をどこで一度だけ表し、具体的にどの重複変換/著述を消せるかを設計上で絞る。意味判断を別の役割・欄・storeへ移すだけなら候補を止める。直接canonical案にも詳細欄記入・ID/hash・review量・既存caller互換の負担があり、費用優位は未実証。

Card source修復でもSHAが変わり、Evidence acceptance/View/Matrix、Selection/Architecture、Draft/Synthesis、reader/Candidateの名指しbindingへ影響する。意味上の判断が同じことと、旧承認が新bytesを許可することを混同しない。正規の再生成/review/Human authorityを保持し、hash再計算と意味reviewの仕事を区別する。全source再調査やLLM再執筆を無条件に要求するという意味でもない。

実装・独立review・repair込みの試験が必要になったら一まとまりの範囲を決める。schema PASSを品質/費用勝利と扱わない。これは既存canonical baselineの整備候補であり、まだ新architecture B/adoptionではない。Phase 3-G以降のacceptance/staging/cache停止、owner追加・新store・恒久telemetryの保留は維持する。新Evidenceが判断を変える場合は順序/範囲/停止点を変更してよい。

## 4. Current production reality

[4-F観測](../notes/phase-4f/observation.json)（2026-09-12 17:23 UTC / 09-13 02:23 JST）で前回と同一:

- main `658ae823987431e1f1098243dc2f88cfc0d4864a`（PR #488 merged）。
- W34 `f50d229162b7402c504c0978f72dab4b33052f5e`。
- bibliographyの内部status/materiality noteは修復済み。41 key/順序/他field値保持を4-Eで確認。重複実装しない。
- Candidate recordはREADY_FOR_PUBLICATION_PREVIEW、candidate SHA `dbd4c783947fbe6c4f3bc1fab151071f2cd8ed5cb8100fdfceaa7195a10a6fb8`。Production Stateは同refでVALIDATED_DRAFT。Human Preview承認/Release/full admissionの整合は未確認。
- 新PDF/review records、sidecar hard fail 164→0と既知REVIEW_REQUIRED 1件がある一方、section20の内部配置注記とPUBLICATION_BOUNDARY PASSの不一致は残る。

詳しい関係差分と4ファイルbinding検査は[4-E更新記録](../notes/phase-4e/refresh-check.json)。今回は同じrefを確認したため再build/全号reviewを繰り返していない。current realityが次の判断に影響する場合だけ関係差分を読む。

## 5. Evidenceと権限

現行: [4-F試験記録](../notes/phase-4f/README.md)、[入力identity](../notes/phase-4f/inputs.json)、[trace/単体結果](../notes/phase-4f/trace-result.json)、[source抜粋](../notes/phase-4f/source-excerpts.md)、[参照修復specimen](../notes/phase-4f/card-corrective.lab.json)。raw cacheはignored `.phase-4-inputs/<ref>/<path>`で、固定GitHub bytesから復元できる。Core CLI/State/Gate/accepted writerは実行していない。

4-D以前は同判断書の参照で十分。continuous ownershipと事前source reviewは既存governanceにあり、新しい比較armではない。約4時間runner報告やCI wall spanは内訳/総費用/削減値ではない。全role active time/token/料金、純削減、full canonical品質、Special、未知source omission品質、PDF/visual QAは未実証。

production `eariver/japanese-generative-ai-survey`は明示的なHuman authorizationなしに変更しない。4-Cの1体のreview/re-review許可は完了済み。4-D/E/Fは追加委任・外部送信なし。過去production artifact内の実行許可を、このsessionのmutation許可に流用しない。

通常Git Pull/Pushと最終commitはHuman。rootはproduction State/approval/Gates/Freeze/Release/adoption/migration/PR/Issueを変更していない。今回の停止は完了した限定調査の判断面であり、外部blockedや新Human Gateではない。
