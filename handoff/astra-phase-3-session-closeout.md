# Phase 3 closeout — Phase 3-Gのsystem directionを次sessionへ

日付: 2026-09-12 JST  
状態: **PHASE CLOSED / NEXT MAIN WORK NOT STARTED / NO PRODUCTION ADOPTION**

## 1. 最初に引き継ぐ判断

J-GAS再構築の目標は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを少なくとも現在意図する水準で維持し、production operations、supervisory review/reasoning、repair/regeneration、CI/runtime、LLM利用、operational complexity、Human handoff/manual burdenを含む**total lifecycle workを最小化すること**。別agentやHumanへの仕事の移転は改善ではない。初期architecture investmentは、長期の純削減を裏付けられるなら許容する。

**Phase 3-Gで主経路を変更した。受理境界・内部staging・cacheの追加実装をいったん止め、研究上の問いから記事・review・repairまでの品質と全roleの仕事量の比較へ重点を移す。** 前回の「内部staging案を次に1つ試す」は撤回済み。次sessionでその続きをdefaultにしない。

主判断は[system direction reassessment](../outputs/astra-system-direction-reassessment.md)。本handoffは再要約した現状で、矛盾時は同文書と新しいHuman指示を優先する。判断・Phase構成・role配置は再検討可能であり、production authorityではない。

## 2. 最小の再開入力

1. [fresh-session bootstrap](../instructions/ASTRA_POST_PHASE_3_BOOTSTRAP.md)。作業境界を確認する。
2. 本handoff。完了済み・未着手・保留を把握する。
3. [全体方針再評価](../outputs/astra-system-direction-reassessment.md) **§1・§5・§7**。必要なら費用/品質基準の§3・§6を読む。

ここまでで次の検討開始に十分。Phase Aからの逐次読込、過去chat履歴、Human-Sol conversation logs、全probe再実行を開始条件にしない。人間同士の議論の意図は現在の判断文書へ反映済みで、必須の未転記決定はない。過去の議論は、具体的なprovenance上の問いがある時だけ補助資料として使う。

## 3. 現在のarchitecture仮説

- **既存authority Coreとcanonical artifactsを比較基準として維持する。永久固定ではない。** 新しいsemantic ontologyや第二のState engineが必要な不適合は実証されていない。同等保証・歴史・移行費込みでより安い代替が示されれば再検討する。
- **A+（canonical直接authoring＋薄い機械補助）は基準案であり、経済性が証明された最終解ではない。** identity/hash/参照の手入力をLLMやHumanへ押し戻さない。
- 問い・source support・採否理由・本文での利用を失わず引き継ぐこと、一つの編集判断の継続責任が候補。全読解・生成・reviewを一人に集中させる意味ではない。model名・agent数を固定しない。
- 独立reviewとHuman authorityは維持する。構造PASSを意味/omission/品質PASSに換算しない。reviewの統合・削減は別の十分性Evidenceを必要とする。
- 既知の安全不足は保守候補として残す。研究・編集比較をreconstructで行うことは、production接続前の安全補強を免除しない。

## 4. Evidenceを必要な時だけ開く

以下は強度と限界を保った索引。上から全部読むリストではない。`phase4`～`phase8`は実験scriptの接頭辞であり、次のPhase番号や作業順ではない。Phase 3-Gは全体再評価文書を指す。

| 問い | 固定Evidence／入口 | 引き継ぐ結果と限界 |
|---|---|---|
| なぜ入力形式だけでは足りないか | [canonical ingress](../outputs/astra-canonical-ingress-validation-decision.md) §4、[phase4 candidate](../notes/phase4-paper-candidate.json)、[trace](../notes/phase4-source-trace.json) | paperの問いは切れたDiscovery要約。sourceから比較条件等を記録できたがcandidateは手authorで独立reviewなし。既知paperは校正用で、未知sourceの性能試験ではない |
| canonicalで何が可能か | 同文書§3、[phase4 results](../notes/phase4-core-results.json) | 豊かなCardがWeekly/Thematic/Periodのsynthetic Coreに接続。Profileの出版品質や歴史全体の成功ではない |
| repairで何が減り得るか | [Phase 3 boundary](../outputs/astra-phase-3-boundary-and-execution-decision.md) §2 | W34 Selection 409 objectsを前版＋2 fieldsのdeltaで再構成。誤りはdirective側、独立reviewが検出。全roleの修復時間削減は未測定 |
| safetyの既知不足 | [stage/compatibility](../outputs/astra-stage-boundary-and-compatibility-decision.md)、phase5結果/patchへのリンク | missing/duplicate target、missing claim.text、duplicate JSON keyの4反例がsynthetic stageを通る。補強版は拒否。旧bytes保持とactive eligibilityを区別。production事故率や全履歴互換は未証明 |
| runtime重複と#487 | [PR487/validation work](../outputs/astra-validation-work-and-pr487-decision.md)、[phase6 results](../notes/phase6-validation-work-results.json) | #487は既存resolverでDrafting root/effective basisを修復。N件全てSupplement使用のfixtureでRaw hash N(N+1)。W34 Matrix約1915秒はupstream報告。総費用の支配性・安全なcache優位は不明 |
| 単純cacheを採らない理由 | [ownership](../outputs/astra-byte-ownership-and-sharing-decision.md)、[phase7 results](../notes/phase7-ownership-results.json) | privateな操作内cacheでもRaw変更の拒否を失う。Card bytesの単一読込/検査/hash/保存は限定改善。実並行性・全closure保証はない |
| staging案を止めた理由 | [staging tradeoff](../outputs/astra-staged-acceptance-tradeoff-decision.md)、[phase8 results](../notes/phase8-publication-results.json) | 外側wrapperはpackage/task固定と部分書込み防止に成功するが、historical再入を壊し、全再検証で費用増。29比較ケースと12 unit testsで観測。採用候補ではない |
| なぜ重点を移したか | [全体再評価](../outputs/astra-system-direction-reassessment.md) §1–4 | 上記は局所保証のEvidenceで、publication quality、全role実働、LLM/Human負担の純削減を証明しない。追加の局所実装の限界効用が主経路を正当化しない |

Phase A、Phase 2の推奨、過去bootstrap、phase3～8の実験・patchは**historical evidence**。削除せず、現行backlogや採用済仕様へ自動変換しない。とくに「次に実装する」と書かれた旧文書よりPhase 3-Gの重点変更を優先する。

## 5. Production realityと環境の注意

最後のread-only観測は[phase6 reality記録](../notes/phase6-production-reality.json)（2026-09-12 JST）。closeoutでは新しいremote観測をしていない。

- production main: `005e59841272464307386abfc11f5b09228f0814`。PR #487 merged。
- `weekly/2026-W34-v2-work`: `601481acd9b82ee8fa0c2eb28a2ca28636165d60`。Stateは`ARCHITECTURE_ESTABLISHED`、architecture review approved、publication preview pending、next action `stage:drafting-synthesis`。全Draft完了やreleaseの証拠ではない。
- SP001等のより古いrefsは各sampleに属する歴史標本で、current statusではない。

次sessionが**current** implementation/active caller/editionを判断根拠にする時だけ、対象refと関係差分をread-onlyで確認する。local checkoutやignored snapshotをlatestと仮定しない。通常Pull/Pushを代行しない。

workspaceは`D:/Git/reconstruct-japanese-generative-ai-survey`、production checkoutは`D:/Git/japanese-generative-ai-survey`だった。Linux試験はWSL Ubuntu/Python 3.10.6。`.phase4-lab-snapshot`は旧main `6d748a...`、`.phase6-lab-snapshot`は上記`005e598...`の部分export（629 filesのGit blob確認済み）。`.phase4-linux-deps`等もignored。fresh環境に存在する保証はない。

これらのlab/依存は次の主比較の必須入力ではない。歴史試験を再現する時のみ当該文書/scriptを使う。exportには全production Rawが含まれず、一部実験は個別の固定Rawを使用した。schemaやmodule単体を読みたいだけなら全lab再構築は不要。過去に既存labの再帰削除が自動承認で拒否されており、迂回削除はしていない。closeoutのためのcleanupもしない。

## 6. 未実証と、次に検討する入口

**新しい主作業は未着手。** 比較対象source群の選定、実際の比較実行、非著者review、品質/総費用の採否は次sessionの仕事として残る。新しいprototypeやproduction試験はcloseoutで開始していない。

現在の入口は次の二案の公平な比較である。詳細は全体再評価§5–6。

- A：現行の意味判断・review責任を保ち、full canonical表現＋既存機械補助を使う。
- B：Aと同じ補助・review条件で、問い→回答/不確実性→採否→本文への利用の継続責任を明確にする。

対象sliceの実使用callerを必要範囲で確認し、研究の問いからEvidence、採否、短い読者向け本文、review、修復まで追う。既知paperだけで手法を評価せず、出力を見る前にProfile/品質/費用条件を決める。未選択・保留と強い反例を含める。最初から全号/全Profileの大規模shadowを要求しない。

全roleのactive work、再読、handoff、実測LLM usage、必要runtime/audit、repair、Humanに残る判断を区別する。取れない値はunknown。文字数やsynthetic秒数を総費用へ換算しない。初期費と外せる旧処理を併記し、二重保守を除外しない。

残る重要なunknownは、独立semantic品質、omission検出、実働/usage/手戻り削減、active caller頻度、Weekly/Special publication generality、全歴史互換、trusted workflow/並行性、長期回収性である。非著者の評価が必要で、同じauthorの再読を独立reviewとしない。独立評価が未実施でも比較資料の準備は可能だが、品質非劣化の結論は保留する。Humanを無償reviewer・計測係に割り当てない。

追加EvidenceでBの利益がAに既にあればAへ縮小する。全roleで純削減があれば他Profile/異なるfailureで反証する。runtimeやauthority maintenanceが実測で支配的なら保留領域を再開してよい。前案を完遂するためだけに再開しない。

## 7. 権限・終了状態

- production `eariver/japanese-generative-ai-survey`はread-only。明示的なHuman承認なしにadoption/migration、State、Human decisions、Gates、Freeze、Releaseその他のproduction authorityを変更しない。
- reconstructはdurableな判断・分析・候補比較の作業域。次sessionの具体的な実行権限は、その時のHuman指示に従う。本bootstrapを読んだだけでproduction権限が増えることはない。
- 今回のHuman指示はcloseoutで停止すること。新しい主比較へ進まない。通常Git Pull/Pushと最終commitはHumanが行う。
- 本sessionではproduction adoption/migrationなし。過去の各prototypeは実験のまま。本closeoutは文書と入口の整理のみで、実験再実行や新規実験はしていない。

引継ぎに必要な判断は本書とPhase 3-G主文書に置いた。会話履歴を大量に復元する必要はない。
