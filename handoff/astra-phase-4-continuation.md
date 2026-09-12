# Phase 4 — fresh-session continuation

日付: 2026-09-13 JST

状態: **CURRENT RESUME ENTRY / PHASE 4-E COMPATIBILITY PROBE COMPLETE / PR #488 REFLECTED / NO ADOPTION**

## 1. 最小の再開入力

1. 本handoff。
2. [Phase 4-Eの判断](../outputs/astra-phase-4e-canonical-rendering-assessment.md) §1・§3–4・§6。§6が途中Push後のcurrent reality更新。
3. 必要なEvidenceだけ同判断書のindexから読む。4-D以前は履歴で、全chat/全source/旧lab再読は不要。

全体目的は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを少なくとも意図した水準で保ち、production・supervisory reasoning/review・repair/regeneration・CI/runtime・LLM・operational complexity・Human handoffを含むtotal lifecycle workを最小化すること。役割移転は削減ではなく、根拠ある長期投資は許容する。

## 2. 今回何が判断可能になったか

4-Dが特定した内部出力の生成欠陥に対して、既知W34の1 packageで限定的な互換性反証を行った。

- canonical Draft内の22意味境界を12 subject別日本語案へ、内部配置制約1件を既存omission dispositionへ表せた。full Draft schema/固定validator関数はPASS、20 distinct LIMITATION refsと元4本文blockを保持。新schema/storeは不要。
- ただし元ArchitectureにはWeekly helperが要求する`section_label`がなく、元入力では拒否。memory上の明示fixtureで後段だけを調べると、CLAIM_BOUNDARYのtextは出るが12/12 blockにcitationが付かない。新しいNOTEもcompact archiveの対応がないと拒否される。full production経路の成功ではない。
- 既存の別rendererにある`render_block`でcitation機構の部分再利用はできる。旧renderer全体はv2の入力fieldが異なり、内部source roleをbibliography noteへ出すため、drop-in置換は棄却。
- Grokの日時claimはDailyX rawの公式X観測を根拠と記すが、Cardのsource IDは編集後の案内ページだけを指す。**参照IDの機械的解決と、日時根拠への正しい対応は別**。元rawがrepo全体に無いとは判断していない。

結論: 日本語Draftを整えるだけで完成試験へ進まず、canonical source対応と実際に使う掲載経路を先に確かめる。不要な内部出力を防ぐ方向は維持するが、大きなarchitecture B、owner追加、新store、恒久telemetry、acceptance/staging/cacheを再開する根拠はない。

日本語案は著者照合まで。機械validatorは意味を逆転させた負例を通すことも確認した。全号のquality PASS、独立review、PDF/visual QA、full admission、Special互換、純費用削減は未実証。

## 3. Current production reality — PR #488後

2026-09-12 15:47 UTC / 09-13 00:47 JSTの[更新観測](../notes/phase-4e/production-refresh.json):

- main `658ae823987431e1f1098243dc2f88cfc0d4864a`。PR #488 merged。
- W34 `f50d229162b7402c504c0978f72dab4b33052f5e`。
- 内部status/materiality note除去はmainの`_bib_text`へ入り、W34文献欄も修復済み。41 key/順序/title/author/URL/urldateの値は保持、内部noteは0。**この部分を重複実装しない。** 旧4-D/E probeは歴史Evidenceとして残す。
- W34は新PDFとreader/quality/semantic/visual reviewを作り、Candidate recordは`READY_FOR_PUBLICATION_PREVIEW`。candidate SHA `dbd4c783947fbe6c4f3bc1fab151071f2cd8ed5cb8100fdfceaa7195a10a6fb8`。PDF metadataは`f7403b0a...`、340480 bytes、12 pages。Human Preview承認/Release完了とは解釈しない。
- Production Stateは今回の差分では不変で、旧`VALIDATED_DRAFT`のまま。Candidate recordと区別して読む。full State/Gate/candidate admissionの整合は今回未検証。
- sidecar reportはhard fail 164→0、既知MistralのREVIEW_REQUIRED 1件、NEEDS_REVIEWと報告する。そのSTOPはCandidate作成前の時点の記録。現在もCandidateが無いという4-D時点の説明を流用しない。
- 対象Architecture/Package/Draft/section20/main.texは差分で不変。新manuscriptは同じsection20 bytesを名指しし、内部配置注記が残る。最新semantic PUBLICATION_BOUNDARYは内部用語/修復履歴が無いとしてPASSするが、この本文の反例は解消していない。bibliography修復と全号意味品質を混同しない。

[refresh検査](../notes/phase-4e/refresh-check.json)では、Weekly rendererの関数AST差分が`_bib_text`のみと確認。Candidate→4ファイルのSHA/byte_count、manuscript→bib/section20も照合。PDF本体のdownload/目視、sidecar再実行、独立quality認定はしていない。新しいrefが判断に影響する場合だけ関係差分を追加で読む。

## 4. 次の入口と停止条件

次の候補は、**Grokの日時claim 1件を、accepted Cardからtask/source supplement/DailyX観測のexact bytesとlocatorまでread-onlyで追う**こと。

入口:

- package `w34-collaborative-agent-workflows-retrieval`
- task `evidence:2026-W34:589f97e8aee10bd1`
- Card SHA `c398b532b7d0c047154176eb579e9931d9c025b313649307f5585cddb47781c1`
- `claim-2`、source `supplement-src-6b3ce48a6c75d42b`
- embedded Evidence acceptanceのfilename `task-3ebd2dfa1c0a39c4f92a.json`
- [機械結果のchronology_source_join](../notes/phase-4e/probe-result.json)に該当claim/context/source/temporal/limitationsを収録。

日時根拠が既存authorityに存在して対応だけが欠けたのか、根拠そのものを十分に確立できていないのかを判定する。前者なら既存canonical fieldsでの修復地点と必要な再生成/rebinding/reviewを整理する。後者ならclaimの保留/限定を検討する。rendererがX URLを推測したり、編集後ページを時点根拠へ格上げしたりしない。

1反例で修復可能性と必要な仕事が判明したら全件監査へ広げず停止・再評価。実際の手著述/Weekly helper/既存経路のどれを基準にするかも、canonical参照を一度だけ正しく読者出力へ運び、再著述/手修復を増やさない条件で考える。全号PDF、新architecture、runtime最適化を先に作らない。

今回のW34や日本語案は既知入力であり、unknown-source A/B試験に使わない。全roleの準備/authoring/review/repair/運用保守を含めて純減を判断する。4-Eの日本語著述や試験scriptも費用で、改善そのものではない。次のAstraはfresh Evidenceに基づき順序・範囲・停止点を変更してよい。これは追加Human Gateや外部blockedの宣言ではない。

## 5. Evidence・履歴・権限

現行:

- [4-E試験記録と再実行入口](../notes/phase-4e/README.md)、[固定入力](../notes/phase-4e/used-inputs.json)、[追加/更新入力](../notes/phase-4e/inputs.json)。
- [lab Draft](../notes/phase-4e/draft-result.lab.json)、[日本語境界案](../notes/phase-4e/boundary-wording.lab.md)、[probe結果](../notes/phase-4e/probe-result.json)。
- [PR488後の差分](../notes/phase-4e/production-refresh.json)、[refresh検査](../notes/phase-4e/refresh-check.json)。
- raw cacheはignored `.phase-4-inputs/<ref>/<path>`。固定refでGitHub GET→manifestのblob/SHA照合により復元可能。probeは指定関数単位で、Core CLIやGateを実行しない。

履歴:

- [4-D](../outputs/astra-phase-4d-production-trace.md): 内部境界の自動連結・bib status note・review範囲の不一致を実W34で照合。約4時間runnerはworklog報告で内訳不明。入口は著述済み本文のcopy/derive/validateで、新規LLM執筆4時間とは言えない。関係CI wall spanも費用削減値ではない。
- [4-C](../outputs/astra-phase-4c-trial-assessment.md): 3候補/4sourceのsliceを独立review→4件修復→再reviewまで完了。Selection/Packageはlab envelopeで、full canonical成功baselineではない。
- [4-A](../outputs/astra-phase-4-comparison-basis.md) / [4-B](../outputs/astra-phase-4-next-window-readiness.md): continuous ownership/事前source reviewは既存governanceにあり、新比較armではない。旧予定は固定仕様でない。

production `eariver/japanese-generative-ai-survey`は明示的なHuman authorizationなしに変更しない。4-Cで許可された1体のreview/re-reviewは完了済み。4-D/Eは追加委任・外部送信なし。過去production artifactの実行許可をこのsessionのmutation許可に流用しない。

通常Git Pull/Pushと最終commitはHuman。rootはproduction State/approval/Gates/Freeze/Release/adoption/migration/PR/Issueを変更していない。
