# Phase 5 — reader review実行計画とruntime修復の優先順位

日付: 2026-09-14 JST
状態: **REVIEW PLAN CONCRETIZED / CURRENT RUNTIME MISMATCHES LOCALLY REPRODUCED / NEXT BOUNDED RUNTIME REPAIR CANDIDATE / NO CONDITIONAL 5-C TRIAL OR ADOPTION**

## 1. 今回の判断

**reader-surface review案を既存Human carry-forwardに合わせて具体化した。その比較試験は始めず、次のreconstruct作業はFreeze/Releaseのproducer–validator契約不整合を、局所修復候補として扱う。** 理由は、新しいreview gateの費用優位は未実証である一方、current runtimeの具体的な不整合と、それに伴う実行時調整・Release後の復旧が確認できたため。既存保守と重複するなら新実装を作らず、その修復をbaselineへ取り込む。

これは全体architectureの固定ではない。publication quality、provenance correctness、fail-close、Human authority、Weekly/Special generality、historical reproducibilityを保ち、production/review/repair/CI/LLM/complexity/Human burdenを含む総仕事を減らす目的は未達である。

開始reconstructはPush済み`0118a7c22291a026835c5ae1630695a4c057f2cf`でlocal/remote一致・clean。commit title `Astra work Phase 5-C (human commit)`はHumanの今回の補足に従いphase authorityにしない。前回はpublication review boundary investigation、5-A/5-Bのconditional 5-C A/B trialは未開始。commitの改名/履歴書換はしていない。

## 2. 前回から変えた前提

### Human carry-forwardは既に存在した

Freeze worklogを入口に必要性が生じたため、Issue #491の[承認コメント一件](https://github.com/eariver/japanese-generative-ai-survey/issues/491#issuecomment-5654102081)を確認した。HumanはW34をpublication qualityに達したとしてAPPROVEし、残る`Discovery observation`等をnon-blocking editorial debtとして受容。W34再生成を要求していない。

同じコメントはW35+に向け、**読者向けcanonical proseが現れた最早点で、TeX編集/生成より前に**狭いlexical lint、同じ本文のsemantic reader review、位置付きfindings、PASS時のみ下流へ進むgateをcarry-forwardしている。正当な技術語はallowlist/suppressionで扱い、audit/provenance欄は対象外とする。これは今回reconstructが新しく発案した改善ではない。

前回の「完成TeX一式を最初の高コストbuild前にreview」は、この要求に対して遅い。**入口をpre-TeXの宣言されたreader fieldsへ修正する。** また、狭いreader-field lint＋正当語の例外処理というHuman案と、前回退けた無差別な全文ブラックリストを同一視しない。ここで読んだ外部記録を、このreconstruct taskからproductionを変更する新authorizationとしては使わない。

### W34はmainでReleaseまで進んだ

観測mainは`3e3eebe0cda3a32ac88ae764d279b37768f6bfca`、W34 branchは`3bad8a57cf2b246c7f71cb749ba3105fa318b073`。branchはFROZEN / next `stage:release`だが、mainはPR #493のfrozen authority統合後、**RELEASED / next null / terminal COMPLETE**。両者を混同しない。

mainのCandidate raw `df376f47…` / payload `52c8d0bc…`とPDF `e93db71a…`はHuman-approved bytesと一致。Freeze/Release記録とcheckpointの局所bindingも確認した。公開Release `weekly/2026-W34`のmetadataはnon-draft/non-prerelease、asset338722 bytes、server-reported digestも同じPDF SHA。rootが公開assetを再downloadしたり、全State閉包/PDF品質/Release workflowを再実行したわけではない。[今回Evidence](../notes/phase-5-review-plan/evidence.md)参照。

## 3. 一回分のreader-surface実行計画

対象は将来の一つのWeekly authoring run。W34の既知欠陥を再発見する試験ではなく、実行前にissue/profile、正規authoring caller、input pathsと版、担当する既存独立reviewerを固定する。この4点はまだ新runに束縛していない。ここではproduction実行も新agent起動も行わない。

| 順序 | 担当・入力 | 実仕事と停止条件 |
|---|---|---|
| 1. 公開欄の確定 | 既存editorial責務。承認済Architectureと実際のauthoring caller | どの欄が読者に出るかをcallerの消費箇所と対応させる。既存authoringが既に同等の早期reviewを行うなら、新しい二重reviewを足さない |
| 2. 狭い静的確認 | production/tool役。完成したreader欄の固定bytes | 明白な内部参照を候補として検出。audit欄を走査しない。未登録の公開欄/不明な抽出結果をclean PASSにしない。正当な語はその出現箇所と理由に限定して扱う |
| 3. 既存独立reviewの消費 | supervisory role。同じreader text＋必要な根拠/限界のみ | 普通の技術読者が内部運用を知らず理解できるか、正規化で事実/限定を失わないかを判断。findingはpath/field/span/入力hashと修復案。正しいauditを改変して表面を整えない |
| 4. author repair | 原著述role。findingと元根拠 | 本文と、その同一性を要求される既存authoring入力を正規経路で修復。source facts/採否まで変わるなら上流境界へ戻す。既accepted Card/Draftをpublication-only rebindへ押し込まない |
| 5. 下流開始判定 | caller/tool。現reader入力集合とfinding disposition | 不足/未解決/入力driftなら下流を止める。修復でbytesが変わった箇所と影響範囲を再review。別Human Gateは追加しない |
| 6. materialization以後 | 既存production＋supervisory責務 | TeX/layout/PDF、全publication品質/変換の確認、exact final semantic/visual記録、Candidate、Human Previewを維持。早期gateを最終PASSやHuman approvalの代用にしない |

今のWeekly callerを使う場合、`survey_weekly_semantic_publication_v2._render_tex`が消費するreader欄はcover headline/deck/anchors、frontmatter heading/lede/scope_notes、Draft Result headline/deck/全`blocks[].text`（CLAIM_BOUNDARYを含む）、final_summary heading/paragraphs、表示されるkicker等。`boundary_dispositions`、IDs、basis hashes、audit rationaleを無差別に本文扱いしない。書誌の表示metadata/access provenanceも別の既存Core責務で確認する。#492修復は全比較の共通baseline。

これは**このcallerの対応表**であり、別のTeX著述経路/Specialへの網羅保証ではない。後続のTeX authoringで新しい読者文言を足すなら、その新しい出力にも適用が必要。前段PASSから後段自由著述を無条件に通さない。完成済み欄の早期チェックはできても、未完成欄を含むpublication全体PASSへ拡張しない。

### current Coreとの接続制約

現reader manifestはsource一式をbindできるが、最終semantic/visual review builderは実PDFを要求する。**pre-TeX gateを既存post-PDF review recordへ偽装してはならない。** 前回の「既存manifest/detailだけで十分」は調査/責務整理の範囲に限定する。実際のfail-fast強制には、publication callerでの開始抑止と、入力集合・rule/抽出版・finding dispositionに結びつく最小の早期結果表現が必要となる。

それは新しいclaim/meaning正本や新Human authorityではない。既存decision/report形式で表せるかを実装時に確認し、できなければ最小のtyped preflight結果に限定する。現行にそのguardが実装済みとは扱わない。早期結果の存在/古いhash/名前だけでPASSにしない。新stage/schemaを無条件に増やす案も採らない。

### 費用判定と実行停止

一回の観測では、原著述/修復/独立消費/lexical toolと例外判断/同期/再確認/全build/最終review/Human handoffを含める。前倒しした同じ読解は削減ではない。省けるのは実際に因果を説明できる追加周回であり、gateの実装/保守と毎回の入力抽出・消費費を差し引く。active time/token/金額が取れなければunknownを残す。

同じ本文を知った同じactorの二周や、既知W34の語を消すだけで効果測定しない。初期設定前に既存早期reviewとの重複が見つかれば追加案を止める。繰り返す修復でsource集合/問いが変わるなら新しい比較条件が要る。一回の実行計画はここまで具体化済みで、次sessionで同じ計画文書を作り直す必要はない。実run/比較は未選定・未実行、conditional 5-Cではない。

## 4. 優先順位を変えたruntime Evidence

Freeze auditはW33/SP001にもあったruntime alignmentをW34で再び行ったと記録する。先行二号の反復はこの報告に基づき、rootは再実行していない。さらに今回のRelease auditは、公開Releaseとexact bytes確認の後で、checkpoint producerの必須review不足によりcanonical advanceが失敗し、復旧したと記録する。

current mainの局所codeに対して[offline witness](../notes/phase-5-review-plan/runtime-witness.json)を実行した。

| 不整合 | 確認したこと |
|---|---|
| Human approvalをStage Checkpointとして読む | `_prior_artifacts`は全checkpoint pointerをStage schemaへ渡す。実approvalはその必須`from_state`/`artifacts`等を持たない。実際のschema/approvalで構造矛盾を確認（全loader実行ではない） |
| Freeze artifacts | schemaはfreeze-record/release-manifest/visual-review-recordを要求。runtimeは前二つだけを許容。抽出した現行`_current_artifacts`へ三つを渡すと`unexpected current stage artifacts: visual-review-record`を再現 |
| Release producer/consumer | producerが出すreview IDは`RELEASE_EXACT_BYTE_RECONCILIATION`のみ。抽出したcontrollerのguardは`CORE_STAGE_CONTRACT`欠落で拒否する。同じguard errorを再現 |
| 単純なreport追加の限界 | compact stage validatorのLOCAL_STAGES/REQUIRED_CURRENTにはFROZENがない。名前だけのPASS追加や既存validatorの無条件呼出しでは修復にならない |

二つの実行witnessは固定関数の早期guardを最小入力で分離したもの。production module graph、全Core/State/schema、実workflowのend-to-end試験ではない。現W34の復旧後authorityを否定せず、今後も標準経路で同じ人手調整を要する原因を特定した。

## 5. 次に実装投資するならこの境界

**次はreconstruct内のisolated candidateで、Freeze/Releaseのtyped authority解決とproducer/consumer契約を揃える小さい修復を検証する。** productionへの適用は別の明示Human authorizationが必要。先に同じShared Core修復が完了していれば取り込み/評価へ切り替え、重複実装しない。

必要な修復条件:

1. Human approval pointerを一般Stage Checkpointとして解釈しない。ただskipするだけでも不十分。approvalのexact path/hash/decision、そこにbindされたCandidate、そのCandidateがbindするpre-preview VISUAL/PDFを解決し、prior artifact収集へ適切に接続する。最新らしいCandidateへのfallbackは禁止。
2. Freeze runtime/schemaで同じartifact集合を扱う。visualは承認前にCandidateがbindした既存recordを使い、承認後の新しい意味reviewを捏造しない。既存のdrift/issue/profileチェックを弱めない。
3. Releaseの外部reconciliationと、local controllerが要求するexact State/Profile/contract/tool/artifact basisの報告を接続する。`CORE_STAGE_CONTRACT`の名前を足すだけ、必須guardの削除、一般的validation bypassは不可。
4. 外部Releaseが先に成立しlocal checkpointが失敗した状態からは、同じ公開identity/assetをread/reconcileして続行できるよう検証する。Releaseの再作成/上書きやexact bytes不一致の受容をしない。
5. 歴史記録を新schemaへ書き直さず保持。Weekly/Specialは同じauthority規則を使い、release identity/profileの違いをfixtureで確認する。

次の検証対象は、正常なapproval→freeze→release、approval/Candidate/PDF/visual drift、未承認/別号/別profile、曖昧なauthority、revalidation歴史境界、再実行時の不変性、external-success/local-failureからの復旧。外部効果はmock/固定fixtureに置く。まずこの範囲の失敗→修復後成功と負例維持を示し、全Core拡張や大規模shadow runを前提にしない。必要なShared Core独立reviewの委任許可は未取得で、4-C/5-B許可を再利用しない。

ここで挙げた修復の実装は**まだしていない**。本turnは、review実行計画を具体化し、新しいproduction Evidenceによって優先順位を再評価し、局所witnessで修復対象を確定する所まで進めて止める。計測されていない純削減を口実に広範な新architectureを作らない。

## 6. 残る限界と継続権限

reader gateの検出率/例外負担/純便益、runtime修復後の全profile互換/全運用費は未実証。W34のRelease成功やHuman品質判断をreconstruct全体のarchitecture採用/全号品質/歴史再現/ROIの達成へ拡張しない。今回の取得・局所読解・過大なmerge差分出力の縮約・404からの経路修正・witness/文書化も調査費に含まれる。

productionはread-only。Release/Gate/State/PR/Issue/commentを変更せず、追加agentなし。Git Pull/Push/最終commitはHuman。現入口は[handoff](../handoff/astra-phase-5-continuation.md)。前回commitのラベルは履歴に残し、conditional 5-Cの未開始は維持する。
