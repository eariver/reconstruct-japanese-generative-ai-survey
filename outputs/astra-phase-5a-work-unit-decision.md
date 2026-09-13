# Phase 5-A — 実仕事の比較単位と次の検証の選定

日付: 2026-09-13 JST  
状態: **PHASE 5 STARTED / 5-A BOUNDED INVESTIGATION COMPLETE / WORK DIFFERENCE NOT YET ESTABLISHED / NO ADOPTION**

## 1. 判断

Phase 5の主題を、**一つの読者の問いに答える際、同じ比較条件を研究・編集の途中で組み立て直す仕事が存在し、その一部を一度の共同検証にまとめられるか**に定める。保存Taskの統合や、新しい意味storeの設計から始めない。

今回の調査では、比較する価値のある仮説は絞れたが、二つの異なる実作業方式がすでに存在するとは確定できなかった。**新architecture BとA/B費用試験は選定しない。次のPhase 5-Bには、一つの問いの研究→本文→独立review→repairを使う、作業差の成立性の観測を選ぶ。** full canonical生成経路の完成をその前提にしない。

候補となる差を一文で記す:

> 同じsubject・source版・評価条件に対する比較可能性の判断を、候補別の調査を閉じる際と後段の横断編集時に再構成しているなら、sourceを横断して一度検証し、その結果を既存の候補別事実欄と編集上の比較理由へ引き継ぎ、後段の再構成を除く。

これは**検証する仮説**である。sourceごとの検証、事実と採否の別判断、独立reviewの再読は必要な異なる仕事であり、上の「再構成」に含めない。問いの共有、比較条件を十分に記すこと、継続owner、良い入力補助は共通条件であって、新Bの利益ではない。同じ便益を現方式へ適用すると作業が同じになるなら、共通改善として終え、対案を発明しない。

## 2. 引継ぎの基準とPhase 4の復元

開始時のlocal HEADとremote `origin/main`は、ともにHuman指定の`64b78ec6aa94c5c1a81b3a1dd14f6a958b99f962`。working treeはcleanだった。Pull/checkoutで状態を変えず、このPush済み内容を基準にした。[Phase 4 handoff](../handoff/astra-phase-4-continuation.md)と[closeout](astra-phase-4h-connection-and-closeout.md)を先に読み、4-C/4-D/比較基準と関係する固定資料だけを追加参照した。過去chatや旧labの再実行はしていない。

| Phase 4で判断可能になったこと | 未実証のまま残ること |
|---|---|
| 既存canonicalの意味欄でsource固有の帰属・比較条件・限界を表し、4-Cの4欠陥を修復→独立再reviewまで閉じられた | full canonical production baseline、全号の品質、費用優位 |
| 継続した監督責任、source消費確認、negative-space reviewはすでにgovernanceにある | 運用で必要なreview量や読解深度が最適であること |
| authorityにある情報をhelper/compact/参照変換で落とす経路と、内部注記が読者出力へ漏れる経路が具体化した | 新schema/storeの必要性、canonical直接著述の優位 |
| lossless compactと補助付きcanonicalは同じ意味欄へ収束し得る | 形式の違いだけで全role仕事が減ること |
| 4-HのURL集約はsource metadataを暗黙に先着採用できないという局所反例を得た | section生成成功、repair/regeneration、publication PASS。guardはlab上の選択で、production schema違反やsource矛盾の認定ではない |
| PR #488/#489の既存修復とW34 Candidate進行をbaselineへ反映できる | reconstructによる純削減、Preview承認、Release、意味品質完成 |

全体目的は、publication quality、provenance correctness、fail-close safety、Human authority、Weekly/Special generality、historical reproducibilityを意図した水準以上に保ち、production operations、supervisory review/reasoning、repair/regeneration、CI/runtime、LLM、operational complexity、Human handoff/manual burdenを含むtotal lifecycle workを最小化すること。移転は削減に数えない。初期投資、移行、二重保守、将来の再利用/修復も含む。Phase 3-Gの[目的関数と停止原則](astra-system-direction-reassessment.md)は継承する。

## 3. 今回得たEvidenceと、その限界

[Evidence記録](../notes/phase-5a/evidence.md)、[固定入力manifest](../notes/phase-5a/inputs.json)、[current観測](../notes/phase-5a/observation.json)に固定ref・hash・再取得入口を残す。コードは静的に読んだ。production runnerやvalidatorを実行した結果ではない。

### E1. 保存Taskの単位は確認できるが、思考の完了単位は決まらない

current mainの`survey_evidence_v2.py`はnon-DROP DiscoveryごとにTaskを作り、`_validate_task`もDiscovery IDが一つであることを要求する。一方、schemaだけを見ると`discovery_ids`は複数を許す。この差から、schemaだけで「joint Taskがそのまま受理される」とは言えない。

current `run_evidence_v2_interactive.py`は複数の著述済みrecordsを一つの入力から受け取り、候補別Card/Viewを機械生成する。したがって**保存が候補別であることは、LLMが候補ごとに別sessionで調査を完了した証拠ではない**。候補別bindingを保ったまま研究作業をまとめる余地はある。実際にまとめた場合の費用・source混線・review品質は未検証。

`build_evidence_tasks.py`も取得したが、schema 1.0の別入口だったため、v2の実使用単位を示す根拠には採用しなかった。旧入口のgroupingをv2へ流用しない。

### E2. 横断比較と適応的な調査深度は、すでに現方式の中で可能

current governanceは、研究戦略、候補横断のmateriality/Selection、package grouping、source固有の不足に応じたgap fill、未選択候補のrisk-based inspectionを監督役へ置く。Evidence promptもCOMPARATOR/RELATEDを表現できる。よって「候補をまとめる」「採用前に比較する」「全件を同じ深度で読まない」だけでは差が成立しない。

W34の既存Evidence reviewは41 MATERIALを複数の編集clusterとして検討し、Selection reviewは368 HOLDをnegative spaceとして保持している。ただし、これらは当該production reviewの記録であり、今回全sourceを再検証したquality verdictではない。

### E3. 実記録は候補別の物質化を示すが、除ける意味再構成を示さない

W34のcurrent branchに保存されたEvidence resume worklogには409のtask-local records、手読みによるoverride、継承した一括input、canonical実行と監督役への停止境界がある。記録には「原文の同じ比較条件を何のために何度再構成したか」の対応も、role別active time/tokenもない。

4-Cで起きたsourceの表/本文不一致、帰属、baseline条件の修復は読解不足のEvidenceになる。しかし独立reviewの原文再読は誤り検出の仕事であり、重複として除けない。未使用metricのCard修復も事実欄の正しさの回復であって、本文から外せば無償になるわけではない。下流hashや複数ファイルの再生成を「同じ研究判断の反復」と数えない。

**結論:** 「候補別Task→後段grouping」というartifact上の順序は実在する。そこで避けられる認知作業が反復しているかはunknown。Task一括化の費用勝利を仮定するより、この未観測部分を一つの実仕事で直接見る方が次の情報価値が高い。

### E4. Current production reality

2026-09-13 06:33 UTC頃のGET観測:

- main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`。
- W34 `5561e2328a09061a3e0c8e881d24ddcb03e1e975`。4-Hの`8480f4df`から1 commit、worklogのmerge ancestry修正1 pathのみ。
- 実Stateは`RELEASE_CANDIDATE`、`next_action=PUBLICATION_PREVIEW`。Preview pending、Human Preview provenance null、Freeze/Release pending。
- この差分ではState、Candidate、Evidence/Selection/Architecture/Draft/reader pathsは変わっていない。全State validation、binding閉包の再監査、PDF/visual QA、独立意味reviewは実施していない。

4-HのCandidate payload digest `dbd4c783…`とraw file hash `c45adaf7…`の区別は保持する。今回Candidate本体を再取得・再hashしたという意味ではない。内部注記/source接続の既知反例がこのadvanceで直ったというEvidenceもない。productionの新しい実装・反復負担の信号は今回増えておらず、renderer/citation/source-identity、acceptance/staging/cacheの保留を解除する理由にはしない。

## 4. 候補の取捨選択

| 候補 | 5-Aの扱いと理由 |
|---|---|
| 継続owner・source reviewの追加 | 現governanceと重なる。共通条件へ吸収 |
| compact対canonical、Card数/ファイル数の削減 | 意味欄と機械補助が同じなら処置が消える。比較armにしない |
| 選ばない候補を浅く処理する | 現方式もrisk-based。品質/negative-space義務を削って差を作らない |
| 候補別の完成を強制したA対、横断作業を許すB | 現方式へ不自然な禁止を足した対照になるため棄却 |
| source横断の比較検証を一度行い、後段の再構成を除く | **次に観測する唯一の仕事仮説**。必要な別判断/独立再読との区別、現方式との収束を先に検査 |
| renderer/citation/受理・cacheの実装 | 保守候補を保持。今回のEvidenceでは主投資を戻さない |

architectureを永久固定する判断ではない。実作業の差が見えた後、既存経路で実現できれば運用改善とする。Coreの単位を変える必要が出た場合に初めて、効果と導入/互換費を比較する。

## 5. Phase 5-B — 作業差の成立性を観測する一往復

これは次段階の選定であり、source選定・出力作成・独立reviewを実行済みとしない。5-Bは二armの性能試験でも、full canonical baselineを再度完成させる仕事でもない。

### 開始前に固定するもの

1. **一つの問いと3–4候補。** 未回答のsource群から、同じ比較軸を共有する異なるsubjectを含める。採用し得る候補と、期間/subject/source不確実性等からHOLD・除外となり得る強い対照を含む。採否の正答は先に決めない。W34、CAS、P-EAGLE/DFlash、旧labは新規性能標本にしない。
2. **共通の探索・品質義務。** 対象読者、Profile、cutoff、調査lane、主要な比較軸、候補が入る選定手順、許されるsource拡張、探索の終了理由を出力前に記す。schema上の必須欄だけに品質を縮めず、source固有の重要条件・反例を追加できる。発見で問いを変えたら版と準備費を残す。
3. **sourceと独立性。** URL/version/取得時点/raw bytes/hashを固定。非著者reviewerがauthor出力を見る前にsourceと問いから期待内容・omissionを記録する。authorはその答えを初稿固定前に読まない。reviewerは不足sourceを独立探索でき、費用を含める。取得可能な一次資料を消費するが、全sourceへ一律の元HTTP成功を課さない。
4. **観測可能性。** 使用環境で実際に取得できるoperation単位のusage/runtimeを小さく確認する。active time/token/料金が取れなければunknown。恒久telemetry、新agent基盤、大きなrunnerを作らない。全roleを分解できない場合、総計を勝手に按分しない。

独立reviewerは必要な実行条件である。現sessionでは追加委任なし。4-Cの一体review許可は完了済みで流用できず、今回の開始指示を一般的なsubagent許可とは解釈しない。独立構成を用意できない実行は自己点検までと明示し、品質比較の完了にしない。これは5-Aを止める追加Human Gateではない。

### 完了物と観測の単位

既存の意味分離を使い、候補別の事実・subject/source対応、全候補の採否と理由、packageの問い/coverage/境界、読者向け日本語本文と参照、独立finding、repair disposition、再reviewまでを一単位とする。省略するproduction admission/Human Gate/full issue synthesis/PDF等は§6の未実行費として明記し、架空のapproval/hashで埋めない。Card/Draftの上流修復をpublication-only revalidationへ押し込まない。

一時的な作業記録は、**意味判断を変更した時と、sourceへ戻った時だけ**次を記す。全文の思考過程や全tool操作の転記は不要。

`対象の問い・比較軸 / subject・source版 / role / 戻った理由 / 参照した既存結論 / 新たに決まったこと / 影響先 / 計測値またはunknown`

分類は、初回読解、新source/新要件、独立review、誤り修復、既存結論を利用できず行う再構成、機械再生成、に分ける。一つの比較軸の例は「同じbaseline・評価集合・実行条件の数字か」であり、sourceごとの事実を混ぜて一つの値にはしない。

**除ける仕事と認める条件:** 同じ問い・subject・source版・比較条件について既に使える結論があり、入力に新しいEvidence/品質要求がないのに、同じ結論へ戻る研究・編集作業が再発している。その再発が単なる表示/転記ではなく、独立reviewや別の編集判断でもない。さらに、一度の検証結果を利用できるようにする著述・参照・検査・保守費を名指せること。

rootの記録だけでこの認定を確定せず、review時に分類を点検する。未来に省ける作業の推測は反実仮想欄へ置き、実測削減とは分ける。ログの記入/review自体も初期観測費として数える。

### 5-Bの品質条件と停止

- reader questionへの回答、機構/変化の具体性、帰属、比較条件・反例・source固有の限界、強い未選択候補の処遇がsource-first reviewを通ること。VERIFIEDや機械PASSは代替にならない。
- provenanceはsubject/comparatorとsource occurrence/version/時点を保持。不明を事実へ昇格させず、未解決が結論を支えられなければHOLD/限定/修復へ戻す。
- blocking findingは修復して再review。最初の修復と一度の再reviewを観測上の一区切りとし、blockingが残れば不合格/残件として止める。追加roundは新しい診断が判断を変える時だけ選び、成功まで無制限に回して隠さない。
- 実質的な再構成が無い、または必要なsource検証/独立review/編集判断しか残らないなら、**仮説を棄却して一往復で終了**。新しいBを埋め合わせで作らない。
- 差が共通の良いauthoringで消えるなら共通改善。既知helper欠陥を残した対照を作らない。
- 観測できないものが中心なら「識別不能」で止める。巨大な計測基盤や全歴史探索を自動開始しない。

## 6. 全role費用と、Phase 5内の次段階

| 軸 | 観測/比較に含めるもの |
|---|---|
| production | source準備・探索・読解、比較、著述、参照/再開、補助の準備 |
| supervisory review/reasoning | source-first期待内容、negative-space、独立再読、finding判断、作業分類の点検 |
| repair/regeneration | source再確認、意味修復、依存先更新、再生成、再review。ファイル数から費用換算しない |
| CI/runtime | 実行したvalidation/build/runtimeと再試行。labで省くCore/admission/full publication/CIは未実行・unknownで、ゼロにしない |
| LLM | 準備/author/editor/reviewer/operator/再開contextの実測。wall span、文字数、アカウント残量をtokenへ換算しない |
| complexity | 作業パケット作成、対応関係の維持、追加欄/adapter、観測、互換/移行・二重保守 |
| Human | 実際の裁定・質問・説明・手作業。labでGateを通さないならHuman負担改善は未評価。Humanを無償reviewerにしない |

単位の違う分・token・料金・契約数を恣意的な一スコアに加算しない。同品質での軸別優劣をまず示し、tradeoffは単位を保つ。将来の回数もunknownのまま、`初期/移行費 + N × 1回あたり全role仕事 + 修復/保守/歴史利用費`の各項を埋める。Nや単価の根拠なしに回収時期を出さない。

**5-Cは条件付きの次段階。** 5-Bで実質的な再構成と代替費が確認できた場合だけ、現方式を不自然に制限しない処置を一つ固定し、fresh source・同等品質・修復後までの比較へ進む。同じauthorが同じsourceをA→Bで解いて学習分をBの勝利にしない。独立author/情報隔離、または別source群での順序入替を設計し、後者は難易度差を残すため小標本の因果効果を断定しない。author/role/model/補助を複数同時に変えない。

その比較で支持が出た後に、Specialの時間幅・系譜/前後関係・異なる採否義務、Weeklyの全体coverage/集約、歴史版の再現・修復、実publication要素/visual QA、正規admissionへの接続を反証対象にする。renderer/source/citationの保守候補が正規接続を阻む時には再開できる。これらの省略分を費用優位として先取りしない。最終architecture採用/production適用はHuman authorityの別判断である。

## 7. 5-Aの停止判断・未実証・権限

今回の停止理由は、契約・実使用入口・一つの運用記録から、**保存単位の差と実仕事の差を区別する次の検証条件が定まったこと**。さらに旧W34を読んでも欠けたactive workの観測は復元できない。新sourceを先に読んで次のauthor/reviewerへ答えを持ち込む準備も行わない。

5-Aの作業はrootによる引継ぎ復元、GETでのref/State/diff確認、契約/コード/worklogの限定読解、仮説の絞込み、durable記録と整合検査。初期に存在しない旧output/READMEへの参照を修正し、広すぎたtool一覧と長いstdoutを絞り直した。別versionのtask builderを調べた費用も含む。これはreconstructの調査費でありproductionの欠陥/運用費ではない。active time/token/料金はunknown。

未実証は、仮説の実作業差、削減量、full canonical baseline、全号publication quality、未知source/omissionの十分性、Special/Weekly全体一般性、全caller/歴史再現、PDF/visual QA、全role費用・長期純減。4-Cの限定独立reviewを今回へ拡張しない。4-H反例とlab修正Cardは歴史accepted chainから分離したまま。

productionへの書込み、PR/Issue/外部メッセージ、State/Gates/承認/Freeze/Release/adoption/migration、追加agent、Git Pull/Push/commitは実施していない。Phase 4はclosedのまま。継続入口は[Phase 5 handoff](../handoff/astra-phase-5-continuation.md)。
