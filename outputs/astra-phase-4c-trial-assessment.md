# Phase 4-C — canonical欄を使う研究・編集sliceの判断

日付: 2026-09-12 JST  
状態: **BOUNDED RESEARCH/EDITORIAL SLICE COMPLETE AFTER REPAIR / FULL CANONICAL RUN UNTESTED / NO PRODUCTION ADOPTION**

## 1. 今回の判断範囲

Phase 4-Bから、未知の3候補・一つの問い・日本語本文について、source固定→Task/Card/View→採否/package→本文→非著者review→修復→再reviewを完了した。r1の機械検査は通ったが、独立reviewで4件のblocking findingが出た。rootが原文を再確認して全件を受け入れ、r2を固定した。**独立再reviewは、宣言済みの範囲で残るblocking output defectを認めなかった**。source内の未解決を残しつつ、その解決を必要としない根拠/本文に修復した。

これは**canonicalの意味欄を用いたA単独の研究・編集slice**であり、full canonical production runではない。Draft Packageの必須Human承認hashを偽装せず、Selection/Packageはcanonical部分構造を持つlab envelopeにした。この制約は[preflight](../notes/phase-4c/preflight.md)で意味出力前に宣言した。Task/Card/ViewとDraft Resultは完全な各schemaを検査したが、Draftの入力packageがproductionとして受理されたとは言わない。Phase 4-Bのfull canonical baselineを完了したことにも置き換えない。

全role費用の優位、publication全工程の同等保証、最終architectureは未判定。対案を新設する根拠にも、この方式が高価だから捨てる根拠にも足りない。

## 2. 実験とEvidence

読者の問いは、2026-03-09～03-16未満UTCの週について「P-EAGLE/vLLMの報告が何を確立し、他研究との速度/導入比較で何が言えないか」。9月に取得した一次sourceを使うlabであり、当時のJ-GAS号や完全な週内Discoveryを再現する試験ではない。[出力前protocol](../notes/phase-4c/protocol.md)を保持する。protocolのINPUT PREPARATIONは当時の状態で、現在状態は本書とhandoffが持つ。

| 対象 | 実施と採否 | 未証明 |
|---|---|---|
| C1: 3月13日付P-EAGLE/vLLM報告＋P-EAGLE論文v1 | 本文の主題。報告日、論文日、測定条件、baseline、専用学習、patchを分離 | 3月当時のblog bytes/head/patch公開履歴、独立性能再現 |
| C2: DFlash論文v1 | 2月の背景研究として同じ本文を支える。機構、serving評価、比較不能条件を消費 | P-EAGLEとの同条件の優劣。本文と表の一部対応は未解決 |
| C3: 3月30日付hidden-state抽出報告 | source固有の内容をCardに保持してHOLD。後日sourceを本文根拠へ入れない | cutoff前の実装公開の有無。3月30日に初めて存在したとも断定しない |

paperは明示v1、blogは取得時のbytes/表示日を固定。Raw4件、契約schema6件とprompt2件をhash付きで保存した。契約は固定main `005e598...`から取得/再利用しGit blobも照合した。新しいproduction HEAD/State観測は行っていない。HTML抽出は読むための補助で、script/UI/数式/表の抽出をもって完全読解とはしない。

Humanが許可した1体の非著者reviewerは、sourceとprotocolだけから[事前評価](../notes/phase-4c/review/source-expectations.md)を固定した。rootはr1固定前にこれを読んでいない。その後同じreviewerが全chainを検査し、本文や修正文は書かなかった。rootが修復し同じreviewerへ戻す構成。モデル名だけを独立性の根拠にせず、source再読とreview費用を加算対象として扱う。

Evidenceの入口:

- [sourcesと取得hash](../notes/phase-4c/source-manifest.json)、[契約のidentity](../notes/phase-4c/contract-manifest.json)。Rawはmanifest名指し先へ保存済み。
- [r1固定版](../notes/phase-4c/r1-freeze.json)、[独立finding](../notes/phase-4c/review/r1-findings.md)。成功した部分も失敗した部分も保持。
- [r2固定版](../notes/phase-4c/r2-freeze.json)、[修復disposition](../notes/phase-4c/r2/repair-record.json)、[r2読者本文](../notes/phase-4c/r2/manuscript.md)。
- [独立再review](../notes/phase-4c/review/r2-rereview.md): R1–R4解消、O1/O2対応。r2の16名指しhash・影響binding・34参照・本文一致を確認。
- [作業/費用観測](../notes/phase-4c/work-record.md)。

## 3. 何が失敗し、何を直したか

| finding | r1の誤り・不足 | r2の修復と残るsource不確実性 |
|---|---|---|
| R1 / P1 | P-EAGLEの要約1.10–1.36倍を表全体の結果と読める形にし、実測の低速化条件を落とした | 要約の範囲を限定。表/本文が一致する低K・C4の0.92倍を追加。C2の0.94/0.98不一致は未解決として保持 |
| R2 / P2 | site/artifact名はあるが、報告/研究の著者帰属を失った | blog team、P-EAGLE論文著者、DFlash著者を別々にCardへ保存し選択sourceの本文にも反映。C3 bylineもCardへ保持 |
| R3 / P2 | DFlash本文の対EAGLE-3 tree16比を表と整合済みとしてCardへ格納 | 不要な確定対応をmetricから外し、表と本文の集計/分母の未解決を明示。勝手にtree60へ訂正しない。元の読者本文はこのmetricを使っていなかったがCardも直した |
| R4 / P2 | P-EAGLEの公開vanilla checkpoint baseline、4層drafter、受理長改善の条件が本文で不足 | checkpointと容量/受理長の条件を追記し、生成順序だけの因果効果と読めないようにした |

非blockingのO1（関連研究の比較方向/別設定）、O2（Kとdrafter/targetの短い説明）も同時に反映した。全ての新しい本文事実を先にCardへ保存し、Task、Card/View hash、package埋込み、Draft basis、根拠参照、本文を更新した。未解決source矛盾を隠すためにquality scopeを縮めたり、レビュー対象外のCardだから残すことはしなかった。

r1は27件、r2は34件の名指し参照を持ち、各版のschema/ローカルbinding検査を通った。checker校正ではwrong-subjectとstale hashを拒否した。これは**schemaが通っても意味が不足し得る具体例**であり、全schema/Core実装の検証結果ではない。独立reviewもr1の16名指しhash・埋込み・参照・本文一致を確認したが、schema checker自体の独立監査はしていない。

## 4. Total lifecycle workについて言えること

今回増えた仕事は、sourceの表/本文の突合、source別帰属/比較条件の整理、非著者のsource再読、修復判断とその伝播、接続補助、usage-limit後の再開、説明/handoffである。これらを他roleへ渡したことは削減に数えない。

観測できたのは作業の所在と局所的なcommand runtime、source-first reviewのwall span393.1秒、r1 reviewのwall span162.8秒、再reviewのwall span105.8秒等。role別token/料金・実働時間はunknown。rootはsource reader/editor/author/補助実装者を兼ねるため便宜的に按分しない。並行するspanも足さない。約1秒未満のJSON生成/検査commandから、意味生成が安いともruntime全体が非支配とも言えない。

repairでは意味を一度直してから複数のcanonical依存を再生成した。**複数ファイルが変わることと、意味を複数roleが再構成する仕事は同一ではない。** 今回は新しいstoreやDSLを設計せず既存欄で表現できた。一方、one-off authoring/check script準備の負担をproduction共通費から除外してAを安く見せることもできない。

現在の結果からは、何を外すと全roleの仕事が純減するかを特定できていない。R1–R4はsource読解/帰属/比較条件の不足であり、cache・staging・受理境界を追加して解消する問題ではなかった。だからといって全運用でmachine runtimeが支配しないという結論にはしない。

## 5. 方針と停止判断

再reviewまで閉じたため、この単位を判断面として区切る。**次のA/B主比較、新しい意味層、全件review基盤、telemetry基盤、acceptance/staging/cache改修はここでは始めない。** 時間枠を使い切るためでも、成功例を増やすためでもなく、差を与える具体的な仕事/順序の仮説と同等品質の測り方がまだ不足しているため。

単に「source reviewを早める」「継続ownerを置く」をBにしない。固定governanceの§4.2・§4.4・§5には、Evidence authority-consumption、採否/negative-space review、Architecture前の監督checkpointがすでにある（[固定資料](https://github.com/eariver/japanese-generative-ai-survey/blob/005e59841272464307386abfc11f5b09228f0814/docs/survey-production-core-v2-sol-luna-review-governance.md)）。今回の最終独立evaluatorは実験の品質確認であり、現行productionにreviewが無いことを示していない。

次の入口は、必要なら**実際の完成canonical実行の1ケースだけをread-onlyで確認し、上記source-consistency作業と監督checkpointが実際にどこで行われ、修復/再読/runtimeのどれが記録上繰り返されているかを判別すること**。Phase 4-A末尾で観測したW34 DRAFT_COMPLETEと約4時間のrunner worklogが候補。ただし現在状態を使うならrefを取り直し、本文/名指しreview/repair/runtimeの関係する差分だけを読む。旧4件を未知sourceの性能評価へ再利用しない。

この限定確認で、除ける具体的な仕事とその代替費用を示せるなら、共通の品質・役割・補助・review条件を保つ対案を一つ定義する。新しいA/B生成は、独立/順序効果と両armの修復・再reviewまで扱える条件が揃ってからにする。ログが不足するなら不足を保持し、推測による総額や大きな計測投資へ直結させない。価値のある差分がなければそこで止め、architectureを変えるためだけの新試験を作らない。

## 6. 未実証と権限

full canonical baseline、全号publication quality、全候補のomission sufficiency、Special一般性、production admission/CI/concurrency、Human Gates、PDF/visual QA、Freeze/Release、歴史互換、長期運用/修復費用、LLM費用、ROIは未実証。今回C3のHOLDが十分でも、週内の強い未選択候補全般の十分性は証明しない。rootのsource記憶を排除したfresh author実験でもない。

productionはread-onlyのまま。Human authorityの変更、採用・移行、State/Gates/承認、production PR/Issue、Pull/Push/final commitは実施していない。phaseの区切りは全体目標の完了宣言や追加Human Gateではない。
