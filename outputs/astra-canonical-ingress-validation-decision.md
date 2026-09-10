# Canonical入力の隔離検証と、次の優先境界

日付: 2026-09-10 JST  
状態: **ISOLATED EVIDENCE ACCEPTANCE EXERCISE COMPLETE / DESIGN REVISED / NO PRODUCTION ADOPTION**

## 1. 判断の更新

**canonical直接authoringを基準とする方針は維持する。ただし、次の実装投資を「便利なwriter追加」から「新しいcandidateに対する共通受理前検査＋検証問いの品質」へ移す。** 別semantic DSLや第二のState engineは依然不要である。

固定版Coreの実関数で、3 entities・4 metricsを持つcanonical Cardを、exact RawのSupplement付きで受理し、Weekly／Thematic／PeriodのViewへ接続できた。Cardの出力bytesは無変更で保存された。新しいmaterialization engineを要する不適合は、今回の範囲では見つからなかった。

一方、**直接の`accept_evidence_results`は、task target欠落・重複、claimの必須text欠落、重複JSON keyの4反例を受理した。** 試作したread-only事前検査はこれらを拒否する。この差は前回のAST抽出functionだけでなく、unmodified Coreのpackage検証・受理関数を含む隔離実行で確認した。ただしproductionのstage全体が通ることは検証していない。

source側では、保存Rawから必要な比較条件とlimitationsをcanonical形式へ記録できたが、元Taskのtargetは切れたDiscovery要約だった。lossless入力とschema PASSだけでは、何を解決したかを確定できない。**問いを改善せずにmaterializerだけ整備すると、形式上の完了と後段の再読が残る。**

今回到達したdecision surfaceは、以下の投資順を選べる状態である。

1. 同じ検査を全ての新規canonical入力が必ず通る受理境界を設計し、既存historical契約と切り分けて検証する。
2. 既存Screening `verification_targets`の使い方を改善し、source-backed candidateを非著者が問い・omission込みで評価する。
3. その後にactual callerを一つ切り替える提案を作る。便利なUI、Selection/Draftの全stage展開、恒久的な新payloadは先行させない。

これはproduction採用承認の依頼ではない。現在の成果は隔離prototypeと根拠であり、stage/trust接続・独立semantic品質・lifecycle経済性の条件は未達である。

## 2. 実施範囲とEvidenceの身元

起点は[前回判断](astra-phase-3-boundary-and-execution-decision.md)。Humanの続行指示に基づき、reconstruct内の実装・実験まで進めた。Phase番号を実装範囲の固定仕様にはしていない。

- reconstruct開始時HEAD: `d802c78bca588e441e3c8c3bbed485e89486c5f7`、開始時clean。
- read-only `ls-remote`でmain `6d748a962d57beff89da7c1b20cb5a9a86c8e261`、W34 `2b49ad77eafc4128f5d7dbf7004f767d8e29c078`を確認。前回から変更なし。
- productionのworking checkoutは`0a47a9b...`だったため、それを実装基準にはしなかった。固定mainを`git archive`でreconstruct内へexportした。fetch/pull/checkout変更なし。
- exportはscripts/schemas/config/docs/tests/.githubのみ、約5.8 MB。終了前に全627 regular filesを元Git archiveと比較し、改変なしを確認した。[manifest](../notes/phase4-lab-manifest.json)
- Rawは以前照合したW34 paper HTML、556,046 bytes、SHA-256 `0446cde9bbc8f861b63f0165afbe61d31caf0ceead8dcb069de2f4f8c3e75bac`。外部論文ページ・dataset・codeを新規取得していない。
- Windows Python 3.10で既存12試験を実行すると11件が初期State生成のpath検査で停止。`initial_state`の`str(relative_path)`とrepository-relative path検査の組合せによる環境差をコードで確認した。Coreは修正せず、WSL Ubuntu/Python 3.10.6で実行すると12件全て通過した。

これはWindows supportの全面監査ではない。今回の検証環境はLinuxへ合わせ、platform修復をarchitecture案に抱き合わせなかった。

## 3. 作ったものと実行結果

### 3.1 小さい受理前検査

[canonical_candidate_check.py](../notes/canonical_candidate_check.py)はcandidateを読むだけで、write/accept/advanceしない。

- prepare時に渡されたpackage SHAを確認する。
- 既存`validate_evidence_package_basis`でprofile/state/discovery/screening/task/Supplement等を検証する。
- JSONをduplicate key拒否でdecodeする。
- 既存Card schemaと`validate_evidence_card`を実行する。
- package内のtask一意対応、完全なtarget集合と重複禁止を確認する。

authorに別入力形式を要求せず、candidateの意味を補完しない。source選択やtarget finding、statusを機械が生成しない。このprototypeは入口に必要な検査の最小実験であり、trusted production APIではない。request/lease/commit admission、同時実行、check後のbytes変更への防御は実装していない。

### 3.2 実Coreによる受理の一往復

[実験script](../notes/phase4_core_experiment.py)はupstreamの`SurveyEvidenceV2Tests` fixtureを再利用する。コードの抽出やvalidatorのmockは行わず、exportした実moduleをimportした。fixtureのimplementation SHAはupstream試験と同じ`4444...4444`である。**この値は実commitのtrust admissionではない。**

次のchainを隔離fixtureで実行した。

```text
synthetic Profile/State/Discovery
  → Screening package/results acceptance（保存されたtargetを試験用taskへ渡す）
  → fixed paper Raw + exact Supplement
  → Evidence package
  → authored canonical candidateをfixtureのidentity/basisへ明示rebinding
  → read-only preflight
  → Core Evidence acceptance + revalidation
  → Profile別View acceptance + revalidation
```

rebindingは試験のための新しいidentityであり、W34の過去approvalの継承ではない。fixtureのView内容はテスト用で、paperをWeekly/Specialへ採用する編集判断ではない。stageは進めておらず、Stateは最初のbytesから不変である。

| Profile | 結果 | 一般化できないこと |
|---|---|---|
| WEEKLY | Card bytes保持、View受理・再検証、State不変 | 現行W34のstage readiness、Weekly記事としての十分性 |
| THEMATIC | 同じCard shapeで成功。固有annotationsを持つViewを受理 | lineage/branch判断の正しさ、SP001の歴史authority |
| RETROSPECTIVE_PERIOD | synthetic BOUNDED_PERIOD Profileと固有annotationsで成功 | 実Period editionのchronology・historical reproducibility全体 |

3 Profileとも、preflight前後にfixture全file hashが一致した。negative実験後、元の正しいaccepted Cardを再検証できた。これは当該fixtureの不変性であり、production全歴史の回帰検証ではない。

fixtureの期間・as-ofは契約の分岐を試すための値であり、このRawをその期間の研究に使ってよいことは検査していない。時点適合性は機械受理から推定しない。

### 3.3 反例による受理境界の差

[結果JSON](../notes/phase4-core-results.json)。各Profileで同じ9反例、計27 caseを確認した。下表の「受理」は`accept_evidence_results`が例外なく戻ったという意味で、stage/Human/semantic PASSではない。

| 反例 | 試作candidate check | 直接Core受理関数 | 含意 |
|---|---|---|---|
| 全target削除 | 拒否 | 受理 | 完全なtask対応を入口／共通境界で必須化する必要 |
| target重複 | 拒否 | 受理 | dict/set化で重複を隠さない |
| claim.text削除 | schemaで拒否 | 受理 | relational validator呼出だけではschema適合を保証しない |
| 同じ`status` JSON keyを2回記録 | decode時拒否 | 受理 | decode後のschemaだけでは曖昧な元JSONを検出できない |
| 未登録subject | 拒否 | 拒否 | 既存subject bindingを再利用できる |
| stale task hash | 拒否 | 拒否 | 既存exact basis制御を維持する |
| Supplement source title改変 | 拒否 | 拒否 | metadataのexact照合を維持する |
| Rawを同じbyte数のまま改変 | SHA照合で拒否 | SHA照合で拒否 | sizeだけの検査ではない |
| result directoryに余計なfile | 単一Cardとして通過 | 集合検査で拒否 | 単体preflightは全package acceptanceの代替にならない |

直接関数には有効なidentity・package・fixtureが渡っている。そこで4例を受理したことは、試験環境の初期化失敗を成功に見せた結果ではない。逆に、既存production writerやstage validatorが他の箇所で拒否する可能性は残る。**公開事故、authority突破、全実経路の欠陥率は断定しない。**

## 4. 保存Rawからのcandidateと、新たに見えた制約

[paper candidate](../notes/phase4-paper-candidate.json)は本セッションで原文のS2/S4/S7/A6を読んで手でauthorしたもの。[source authoring script](../notes/phase4_source_candidate.py)内の文章はその記録であり、自動抽出器の学習済みルールではない。非著者の独立reviewは受けていない。

BeautifulSoup 4.13.5 / html.parserでsection IDを指定し、hidden/UI領域を除いた。指定regionの一意存在、正規化text hash・文字数、Raw hash、読んでいない範囲を[trace](../notes/phase4-source-trace.json)へ保存した。文字数capは設けなかったが、本文全体を消費したとは表示していない。

### 読み取ってcanonicalへ記録できたこと

- 主実験で同じsolverを使った4 protocolの比較というmethod。
- 主held-out 423件で、self-confidence gateとfrozen routerを区別したsolve率／平均token数と各信頼区間。値のsubjectはpolicy entityへbindした。
- solve区間の重なりを理由に「gateの正答率が優れる」とはしないという本文の境界。
- retrospective oracleはdeployable policyではないこと、token数と遅延・金額等が同じcost尺度ではないこと、problem-level bootstrapとfresh-run variabilityが異なること。
- Appendix Fにcompanion dataset archiveへのリンクがあるというbounded observation。リンク先の内容・利用可能性・再現性は確認していない。

以前の「code/model linkが見つからない」という狭い記述を、dataset linkの存在だけで虚偽と断定しない。ただし再現資産についてreviewする際、Appendix Fの明示リンクは有用な追加情報である。新たな外部factとして検証済みとはしていない。

Cardのprimary artifactはpaperであるため、二つのpolicy entityはpaperに対する`RELATED`、policy同士の比較は`comparison_subject_ids`へ記した。policyをpaper自体の比較対象と誤表示しない選択である。このrole解釈が下流review／Draftで十分かも独立評価の対象で、schema通過だけで解決済みとはしない。

### 既知UI defectだけを直して終了しない理由

Taskの`verification_targets[0]`は934文字のtriage metadata＋途中で切れたabstractで、最後は`biol`だった。新candidateはこのexact targetを保持しつつUNRESOLVEDとし、限定的な読解範囲と問いの再定義が必要なことをfindingへ記した。勝手にTaskやScreening acceptanceを変更していない。

**exact target coverageは必要だが、そのtargetが良い研究問いであることまでは保証しない。** 次は既存Screeningの`verification_targets`を、sourceから何を確かめるか・不明なら何を残すかが明瞭な項目としてauthorする。question qualityを単純な長さや疑問符で判定するparserは作らない。accepted Taskの修正は現行revision契約に従う。新しいTaskのauthoring改善に、追加のHuman Gateを一律設ける提案でもない。

この一件の本文読解は、source preparationとcanonical表現の具体的成立例である。unknown sourcesでの自動品質、全論文のomission率、model比較のEvidenceではない。UI phrase除去、locator存在、schema適合、機械受理のいずれもsemantic quality PASSへ換算しない。

## 5. Architectureの修正点

前回はwriterを薄くすることに重点を置いた。今回の実行から、**検査責任をwriterの都合で分散しないこと**を優先する。

### 新しいcandidateに対する共通境界の責任

1. 重複keyを拒否するcanonical JSON読込。
2. 当該contractのschema検査と既存関係検査。
3. task/record全件対応と重複禁止。
4. exact input/basis/Raw/contractと、現在のrequest/runtime/leaseの照合。
5. 全candidate setの検査完了後に限った受理。reviewされたcandidate bytesと実際に受理するbytesの一致。

prototypeが実装したのは1–3と既存package検査への委譲だけである。4–5のstage/trust/競合部分は、既存機構へ統合する必要がある。単なる「checkを先に呼んでください」という運用文書だけでは、呼び忘れやcheck後の変更を防げない。

実装候補は既存Evidence moduleの共通読込／candidate検証境界を使い、直接Card入力と現runnerがそれを共有する構成。適用範囲は新規入力の受理で、独自のaccepted storeは作らない。試作helperをそのまま別の常設wrapperとして積み増すことを推奨しない。

ただし、今回だけで`validate_evidence_card`を歴史を含め一律strict化するproduction patchは作らなかった。新しいreject規則が歴史再検証へどう作用するか、全callerがどこでschemaを検査するか、current agent-first stageとどう接続するかが未検証だからである。strict新規入力とhistorical verificationの区別はcommit/contractで説明できるようにし、旧accepted bytesの書換えやsilent grandfatheringで解消しない。

### A+ / B / その他への評価

- **A+: 維持。** 実際に豊かなCardを既存受理関数へ渡せた。新たなsemantic schemaは必要なかった。
- **Bの独立payload層: 引き続き保留。** 今回追加した仕事は共通validationとsource authoringで、別DSLでは減らせない。
- **producerごとの局所patchだけ: 不十分。** 正しいcallerだけがschema/target検査をする設計では、新入口追加時に同じ確認を繰り返す。
- **Core全体置換: 支持しない。** Raw/hash/subject/集合等の制御は実験で機能した。共通の入力境界を補強する問題である。
- **review削減: 見送る。** 研究問いの曖昧さ、source omission、比較解釈は残る。物理的な常駐agent数やmodel familyを固定する根拠もない。

## 6. Lifecycle workの評価

今回測れたのは「既存関数とcanonical形式でできる／できないこと」と具体的な操作である。LLM usage、人のactive time、CI費用を対照実験として計測していない。

paperの旧Cardは同じJSON整形で6,607 bytes、新candidateは11,334 bytes。entities/claims/metrics/limitationsはそれぞれ`1/3/0/3 → 3/4/4/4`。これは入力・記録量の増加で、token費用比や品質点数ではない。後段の再探索が減る可能性と、author/reviewerの負担増の両方を評価すべきである。

| Lifecycle部分 | 今回成立した削減候補 | 残る費用・検証 |
|---|---|---|
| production | 既存canonical形式をそのまま使い、新semantic変換を維持しない | source読解・問いの設計・入力の詳細化 |
| review | exact source region、比較subject、条件、未読範囲を提示できる | 独立omission review・意味判断は未実行 |
| repair | field/path単位でschema/binding/targetの失敗原因を返せる | semantic correction、accepted後のrevisionは別 |
| maintenance | 追加writerごとのschema/target検査の複製を共通化できる | common-boundary regression、historical互換、全caller接続 |
| regeneration | 保存Rawを再取得せず利用、受理時のCard bytes保持 | 新モデルの同文再生成は保証しない。原出力保存が必要 |
| Human handoff | 何が機械適合で、何が未reviewかを分けて提出できる | adoption/priority/Gatesの裁定はHumanに残す |

旧paper producerのnarrowingと一律VERIFIEDを外すには、新source authoring＋共通検査＋独立reviewの一往復が必要である。今回の候補はそのための具体的評価対象になったが、旧routeをproductionから外せると認定するには不足している。Selection/Draftへ拡大する前にこの一往復を閉じる。

## 7. 次の実行単位と採用条件

次は「新規Evidence入力の共通検査をstageへ接続した隔離candidate」と「問いを明確化したsource-backed authoringの非著者評価」を一つの限定単位として扱う。writer全体の刷新は含めない。

### 機械側で必要な追加Evidence

- actual agent-first callerから受理までschema・strict decode・target検査を必ず通ること。今回の4反例を拒否し、既存正当入力を通すこと。
- check後のcandidate変更、basisの並行変更、誤runtime/request/lease、部分失敗でaccepted/Stateに不正な完了を残さないこと。
- 既存historical fixtureを当時のbytes/contractで検証でき、新入力規則への移行の扱いを説明できること。
- 1つのactual future callerについて、外す旧変換、追加する共通検査、残すhistorical pathを具体的差分で示すこと。

### 意味側で必要な追加Evidence

- このcandidateと少なくとも異なるfailureを問えるsourceを、非著者がRaw・問い・omission・比較条件を含めて確認する。件数を増やすこと自体を目的にしない。
- 対照は同じcanonical形式と既存補助を使う直接authoring。known bad keyword producerだけを対照にして改善を主張しない。
- 全roleの作業を記録し、単にauthorへ仕事を移したのか、review/repair/handoffを含め減ったのかを比較する。小標本で運用全体のROIを断定しない。

今回は独立reviewを実行していないため、実験者自身の再読を独立性として数えていない。必要なreviewが得られない間も機械側の隔離検証は可能だが、品質非劣化の採用条件は満たせない。

### 分岐

- shared境界の補強だけで十分なら、A+の薄い接続案へ収束させる。
- historical互換／stage接続が変更費を支配するなら、範囲を入口の限定に戻し、Core変更案と比較する。old contractを無言で再解釈しない。
- source作業量が増えるだけでreview/repairを減らせなければ、全候補に詳細metric/locatorを必須化せず、問いに必要な範囲へ縮小する。
- verification taskの品質が主要原因なら、Screening/task authoringへ優先を移す。新materializerで意味を推測補完しない。

十分な結果が揃った時点で、対象future edition/Profile/stage・差分・検証結果・廃止対象・rollbackをHumanへ提示する。明示採用前のproduction変更はしない。現行State、Human authority、Gates、Freeze、Release、fixed-head audit、exact PDFの扱いは維持する。

## 8. 再現・終了境界

再現は、reconstruct rootで`python -B notes/phase4_prepare_lab.py`を実行して固定sourceとRawをdisposableな`.phase4-lab-snapshot`へexportする。既存directoryがあれば拒否する。Linux環境へ`jsonschema==4.23.0`を用意し、次を実行する。

```text
python3 -B notes/phase4_core_experiment.py .phase4-lab-snapshot .phase4-lab-snapshot/analysis-paper.raw notes/phase4-core-results.json
```

今回の実行はWSLで、依存はworkspace内のdisposable targetへ配置した。source candidateは保存済みJSONを入力として使う。source authoring scriptの再実行には`beautifulsoup4==4.13.5`が必要で、観測時刻が更新されるため同じcandidate bytesのreplayとは別操作。Core実験は保存されたcandidateからreplayする。temporary pathやschema errorのpath文字列も環境依存で、結果JSON自体のbytes同一性は要求しない。

終了前にexported sourceの不変性、結果JSON、source trace、local linkを確認した。検証用snapshot・依存の3 directoryは、workspace内の実パスを確認した上で再帰削除を試みたが、自動承認レビューに`blocked by policy`として拒否された。削除は行わず、root `.gitignore`でこの3 pathだけを除外した。durableなscript／candidate／trace／結果／本書と区別する。既存labの再利用時はmanifestの固定source照合を行うか、別のfresh workspaceでprepareする。

ここで停止する理由は、canonical表現力と単純なacceptance接続の可否から、共通受理境界の互換設計と独立品質評価へ主要な不確実性が移ったためである。さらに同じsynthetic受理例を増やしても、trust/leaseやsemantic品質の根拠にはならない。

継続時は本書§1・§3.3・§7を起点にする。前回の「full Core未実行」は、**実moduleによる隔離Evidence/View受理は実行済み、stage/trust/production admissionは未実行**へ更新する。研究問いの改善、新入力の共通検査、historical互換を切り離さず、production採用可否を再判断する。

Git commit/Pull/Push、production repositoryの変更、production adoption/migration、State、Human decisions、Gates、Freeze、Releaseの変更は行っていない。
