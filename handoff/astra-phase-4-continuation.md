# Phase 4 — fresh-session continuation

日付: 2026-09-12 JST  
状態: **CURRENT RESUME ENTRY / PHASE 4-C BOUNDED SLICE COMPLETE AFTER REPAIR / FULL CANONICAL PRODUCTION RUN UNTESTED**

## 1. 最小の再開入力

1. 本handoff。
2. [Phase 4-Cの判断](../outputs/astra-phase-4c-trial-assessment.md) §1・§3–5。
3. 必要なEvidenceだけ同判断書§2のindexから読む。全Raw・全chat・旧labの再読/再実行は不要。

Phase 4-Aは比較前提の調査、4-Bは次枠準備、4-Cは今回の研究・編集slice。Phase 3-Gで閉じたacceptance/staging/cache主経路を再開しない。旧「A」等の歴史phase名と今回のA単独comparatorを混同しない。

## 2. 最新結果と範囲

3候補/4一次source、一つのWeekly reader questionについて、rootがTask/Card/View・採否・package・日本語本文を作り、Humanが許可した**1体の非著者reviewer**がsource-first評価→初稿review→修復後再reviewを担当した。rootは事前評価を読まずr1を固定、finding後に原文を再確認して修復した。別model名だけを独立性の根拠にしない。

r1はschema/名指しbindingが通っても4件のblocking findingを含んだ。論文の要約倍率と表全体範囲の混同、研究/報告著者の欠落、DFlashの本文/表の分母不整合の確定扱い、P-EAGLEのcheckpoint/4層/受理長の比較条件不足。r2では全件を修復し、**独立再reviewはこの範囲で残るblocking output defectを認めなかった**。sourceの2つの不整合自体は未解決のまま、確定値として本文に使わない/範囲を限定することで閉じた。

実験はcanonicalの意味欄を用いたA単独slice。Human approval hashを偽装しないためSelection/Packageは非受理のlab envelopeで、full canonical baselineやproduction admissionは未実行。この制約は意味生成前のpreflightに明記。Task/Card/ViewとDraft Resultのschema適合、根拠参照、部分構造検査と、productionとしての受理は区別する。

C1は3月13日付P-EAGLE/vLLM報告＋2月の論文、C2は2月のDFlash v1を背景として採用。C3は3月30日付hidden-state抽出報告をHOLD。問いの週は3月9日～16日未満UTC。source取得は9月12日で、当時のblog bytes/head/patch公開状態は未証明。今後この既知source群を未知sourceのA/B試験に再利用しない。

## 3. Durable Evidenceと再検査

- [protocol r1](../notes/phase-4c/protocol.md)と[preflight](../notes/phase-4c/preflight.md)は出力前の記録。protocol冒頭のINPUT PREPARATIONは当時の状態として改変せず保持。
- [source manifest](../notes/phase-4c/source-manifest.json): Raw4件を名指し。派生text/extraction recipeも同dirに保存。
- [契約manifest](../notes/phase-4c/contract-manifest.json): 固定main由来6schema/2prompt。Git blobとSHA-256照合済み。
- [r1固定](../notes/phase-4c/r1-freeze.json) → [独立finding](../notes/phase-4c/review/r1-findings.md) → [r2固定](../notes/phase-4c/r2-freeze.json) → [独立再review](../notes/phase-4c/review/r2-rereview.md)。
- [修復disposition](../notes/phase-4c/r2/repair-record.json)、[最終読者本文](../notes/phase-4c/r2/manuscript.md)、[作業記録](../notes/phase-4c/work-record.md)。

再検査が判断上必要な場合のみ、Python + jsonschemaで `python notes/phase-4c/check.py r1` / `r2` を実行できる。Raw再取得やauthoring script再実行は不要。author_r1.py / draft_r1.py / repair_r2.pyは今回の著述/変換記録で、汎用authoring engineの提案ではない。固定版を上書きしない。ローカル検査は意味品質やCore受理を判定しない。

## 4. 全体方向と次の入口

目標はpublication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを保ちつつ、production・supervisory reasoning/review・repair・CI/runtime・LLM・複雑性・Human handoffを含むtotal lifecycle workを最小化すること。役割移転は削減ではなく、根拠ある長期投資は許容する。

今回、sourceを突き合わせる意味判断と非著者review/repairが必要だった。既存Card欄で全findingを表現・修復でき、新storeは必要なかった。ただしcanonical方式の費用優位やruntime非支配を証明したわけではない。role別token/料金/実働時間はunknown。記録済みreview wall spanや1秒未満のJSON assembly runtimeを全仕事の費用へ換算しない。

**次のA/B主比較やarchitecture実装は開始しない。** 現段階で除ける具体的な仕事と代替費用を示せていない。継続ownerもEvidence段階のsource/採否reviewも現行governanceにあるため、単に追加/前倒しするだけでは独立したBにならない。

次に継続指示がある場合の候補は、**実際の完成canonical実行の1ケースに限り、source-consistency作業/監督checkpointと、修復・再読・runtimeの反復をread-onlyで照合すること**。Phase 4-A末尾のW34 DRAFT_COMPLETEと約4時間runner worklogが入口候補。全repo crawlや全号再生成をせず、名指しreview/repair/本文/実行ログの関係だけ読む。current detailが必要ならHEAD/refを再観測する。ログ不足を費用0にせず、計測基盤新設へ自動的に進まない。

そこで除ける仕事/代替費用が具体化した場合だけ、共通の品質/role/補助/review条件と順序効果を扱える対案を一つ定義する。有用な差分がなければ停止する。今のsourceを知った同じauthorによる「Bの作り直し」を比較実証にしない。

この区切りは追加Human Gate、全体目標完了、usage不足によるblockedではない。次の入口は候補であり、fresh-sessionのEvidenceに応じて調査順/停止点を再判断してよい。

## 5. 過去Evidenceと未実証

Phase 4-A: [比較基準](../outputs/astra-phase-4-comparison-basis.md) §1/§3、[49入力のbasis/late observation](../notes/phase-4/basis.json)、[4件trace](../notes/phase-4/trace.json)。CASの未選択paperでは取得本文の限界が未消費、UI文字列混入、CONSUMED記録とのずれを確認した。採用すべきという判定ではない。4件は歴史校正例で未知source比較から除外。

Phase 4-B: [開始条件](../outputs/astra-phase-4-next-window-readiness.md)。同書のMAIN TRIAL NOT STARTEDはその時点の記録。A単独は費用優位を示さず、compact helperのMETRIC/coverage注意も保持。

最後のproduction観測（Phase 4-A末尾）はmain `005e59841272464307386abfc11f5b09228f0814`、W34 `899d3d6ab96c14bb82ea24b0ae12700e798a781f` / DRAFT_COMPLETE。4件分析refは `601481acd9b82ee8fa0c2eb28a2ca28636165d60`。4-Cは固定契約のGET/再利用だけで、current production Stateを更新観測していない。

未実証: full canonical baseline、全号publication/omission品質、Special一般性、全歴史互換、CI/並行admission、PDF/visual QA、Gates/Freeze/Release、all-role費用/ROI。C3の時間理由HOLDが十分でも、週内の強い未選択候補全般の十分性は証明しない。source記憶を排除したfresh-author試験でもない。

## 6. 権限

production `eariver/japanese-generative-ai-survey`は明示的なHuman authorizationなしに変更しない。今回の1体の独立reviewと再reviewはHumanが許可済みで完了した。これは追加agentや外部送信・production mutationへの包括許可ではない。同じ許可を再確認する必要もない。

通常Git Pull/Pushと最終commitはHuman。production State/approval/Gates/adoption/migration/PR/Issueは変更していない。
