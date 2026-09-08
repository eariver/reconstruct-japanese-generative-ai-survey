# Phase A continuation — architecture refinement

日付: 2026-09-09 JST  
状態: **architecture refinement 完了。production adoption・implementation は未実施。**

## 1. 今回の決定

推奨は **一つの編集責任、必要な範囲だけ生成する workers、短期の独立 challenge、既存の厳密な authority Core** である。三つの常駐 LLM が同じ号をそれぞれ理解し直す構成にはしない。

Phase A の五つの論理 product、semantic consumption の優先、generated resume view、exact Human/PDF/release boundary は維持する。一方、次の点を変更・限定する。

| Phase A の表現 | 今回の決定 | 理由 |
|---|---|---|
| Lead が原稿まで継続所有 | **所有と生成を分離。** Worker が accepted plan から原稿を生成し、Lead が意味・編集を受け入れる | Lead への全 token 集中は省力化にならない |
| Independent Reviewer を research/plan/publication に配置 | **通常は一つの短期 research/plan challenge。** 最終原稿/PDF は非著者の Lead が review。Lead が substantial prose を書いた場合は該当範囲を外部 review | 第三役を全工程の常駐 agent にしない。著者の自己承認を避ける |
| model/vendor independent role | 維持し、追加 critic の binding は **異なる model family を優先する比較対象** とする | Human の選好を反映するが、多様性自体を品質保証にしない |
| factual extraction を edition 間で再利用 | **過去の成果を次の判断への入力として再利用。authority acceptance は再利用しない** | 現行 Evidence Card は issue/task/Screening basis に結ばれる。新しい受理を省略する根拠はない |
| fine-grained invalidation | 初期は semantic unit の再作業範囲を提案するだけ。**正式な stage/Gate invalidation は現行のまま** | 隠れた依存をまだ十分検証していない |
| Grok/X を外部 source intake として扱う | **意味判断をする X research specialist** として topology と費用に明示 | 検索、ランキング、反対材料探索は既に推論作業。ただし一般的な独立 critic とは異なる |
| DVC 等の限定評価 | 当面は採用決定しない | 今回の未解決問題を外部 engine は解決しない |

この refinement は Phase A を置換せず、上記の点を具体化・修正する。衝突する箇所は本書の推奨を優先して読む。ただし、どちらも production authority ではない。

## 2. 今回使った証拠と追加調査の限界

[継続タスク](../instructions/ASTRA_CONTINUATION_AFTER_PHASE_A.md) と [Human/Sol discussion](../context/2026-09-09_post-phase-a-human-sol-discussion.md) を読んだ。ローカルには discussion までしか反映されていなかったため、継続タスクは workspace repository の GitHub Contents API から取得して同じ path に保存した。取得時の remote main は `0c6233fc040d062598d5ee1880e0235a0a411430`。ローカルの他ファイルや Git refs を同期・上書きする操作はしていない。

W34 の defect、状態重複、release mismatch は Phase A の固定証拠と独立 review に依拠し、再クロールしていない。追加の production 読取は、既知 main `0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc` の X intake policy/prompts と Evidence Card schema に絞った。これにより次を確認した。

- Grok の common prompt は候補探索、community significance、counter-signals、verification needed を要求する。Weekly overlay は lane 別探索、未選択候補の保持、ranking、coverage audit を要求する。既に semantic specialist である。[X common policy][X weekly overlay]
- Grok output は Discovery/community/adoption/reproduction の手掛かりとして扱い、technical specification 等の authority へ直結させない。Weekly は実行が必要、Special は applicability 判断がある。[X intake policy]
- 現行 Evidence Card は `issue_id`、`evidence_task_id`、task/Screening/prompt/contract hashes を持つ。これを別 edition にコピーして accepted authority とすることは、既存契約と整合しない。[Evidence schema]

最新モデルの優劣、料金、connector availability は今回調査していない。特定製品の性能を前提に設計せず、subscription 状況は Human-reported resource context としてのみ扱う。Human が報告した前回の 13m17s・allowance 43% も、一回の観測であり token 単価や今後の所要時間へ換算しない。

## 3. Role topology を実際の仕事へ落とす

### 3.1 常駐するのは編集の継続 context 一つ

Lead の context は、Profile、coverage obligations、current accepted product references、重要な判断、未解決 findings を保持する。Raw 全件、worker の探索履歴、過去の修復全史は常時入れない。再開時は正本から生成した短い resume view を読み、必要な根拠に直接進む。

Workers は source cluster または manuscript section の bounded task を受ける。取得をすべての候補で別 agent に分けず、同じ source family や比較対象をまとめる。Research と drafting の context は必要な入力が違うため原則別にするが、仕事が小さく同じ context 内で済む場合に新規 session を強制しない。

Lead は重要度・採否・構成の意味を決めるが、その JSON、表、prose を全て自分で生成する必要はない。Worker が提案を作り、Lead が **変更した判断だけ** を受け入れ・修正し、Core が既存の各 artifact に投影する。Lead の承認コメントをまた Worker に言い換えさせ、再度 Lead が全文を読む往復をなくす。

Critic は恒常的な「第二編集部」ではなく、一号の research/plan challenge のための短期 context 一つ。通常は二段階で使う。

1. **Blind coverage pass:** Profile、期間/as-of、coverage obligations、必要な source access のみを渡す。生成側の shortlist、thesis、採否、過去 defect の答えは渡さず、独立に重要な候補・反例・未解決 lane を返させる。後から計測できるよう、この結果を固定する。
2. **Plan challenge:** 同じ critic に candidate disposition map、plan、Evidence units、選択的な Raw access を渡す。blind 結果との不足、強い omission、claim の薄さ、代案の成立性を調べ、findings を返す。完成号をもう一冊作らせない。

これを通常時の独立 challenge として残す。異常検出器が警報を出したときだけ呼ぶ設計は採らない。X の specialist が独立に検索しても、論文・公式発表・非Xの欠落全体を検証したことにはならない。

### 3.2 通常 Weekly の進行と handoff

| 順序 | 実行と入力 | 出力・境界 |
|---|---|---|
| 1 | Lead: Profile/状態、過去 carry-over を読む | research brief、coverage obligations、worker batch 方針。Grok と critic blind pass を依頼 |
| 2 | Workers: intake/Screening/Evidence。Grok: X-specific semantic search | 候補固有の claims、実際の消費範囲、gap。exact imported Grok output |
| 3 | Lead: 最初の重要 batch を source と突き合わせる | systemic placeholder を早期検出。抽出方式が良ければ残りへ。欠陥なら当該方式を止める |
| 4 | Worker proposals を受け Lead が materiality/selection/architecture を確定 | 正本 plan。projection と dossier は機械生成 |
| 5 | Critic: plan challenge。Lead: findings を裁定 | 必要な局所修復、disposition、Human に提示する residual risk |
| 6 | Human Architecture Review | exact commit/bundle への明示 decision |
| 7 | Draft workers: accepted Evidence + plan の該当範囲 | reader manuscript。Core が deterministic QA/build |
| 8 | Lead: final semantic/editorial review と exact PDF visual review | source/PDF-bound review。Human Preview へ |
| 9 | Human Publication Preview、Core Freeze/Release | exact bytes と承認履歴を維持 |

表の順序は barrier を毎回増やす指示ではない。blind pass と bulk intake は並行可能、Evidence の初期品質点検後は局所 batch を続けられる。Lead は未処理の重大 gap を final plan に残したまま Gate へ進めない。

最終原稿は Worker が著者、Lead が reviewer になるため、通常は publication のためだけに別の常駐 reviewer を追加しない。Lead 自身が substantial rewrite をした claim/section、controversial な比較、品質に異議が残る箇所は別 context の critic が該当範囲と全体への影響を読む。軽微な typo 修正まで第三者の全文再読にしない。ただし PDF が変われば exact PDF visual review と Preview identity は更新する。

これは #485 の現在の必須 checkpoint を既に省略してよいという意味ではない。上記の統合 topology は shadow で比較し、正式 adoption まで production には適用しない。

### 3.3 Invocation と context の会計

ここで数える「呼出し」は、独立した仕事の依頼と結果返却の **logical assignment**。一つの interactive session 内に何回の inference/tool continuation があるかは harness ごとに異なり、logical assignment 数から実 API call 数や費用は導けない。

正常時の設計予算を次で表す。

- `b`: research batch assignments。内部で通常検索・gap-fill を完結できる単位。
- `d`: reader manuscript assignments。
- `x`: X specialist runs。Weekly は通常最小1、Special は rationale により0以上。
- `g`: 結果返却後の追加 research/draft repair assignments。
- `l`: Lead の decision windows。目安は brief、初期抽出、plan/findings 裁定、final publication の4。必要な gap/disagreement で増える。
- `c`: critic assignments。通常 blind + plan の2。重大 repair の再確認、Lead authored section の review で増える。

**LLM logical assignments = `b + d + x + g + l + c`。** 通常の目安は `b+d+x+6`。Critic二依頼を同じ session で行うので、fresh contexts の目安は `1 Lead + b research + d drafting + 1 critic + x specialist`。1 candidate = 1 context とする設計ではない。

例えば小さな Weekly を `b=3, d=2, x=1, g=0` で処理できるなら、12 assignments、8 contexts が設計上の例となる。このうち独立 critic は一 context・二 assignments、Lead は一 context・四 windows である。**測定値でも409件のW34に対する所要数予測でもない。** この例を quota にして候補や研究深度を削らない。

役割間の依頼→返却 pair は `b+d+x+g+c`、上の例なら8 pair。単方向 message 数ならその2倍。Core の生成・検証・build は LLM assignment に数えない。Human の二 Gate と、必要な Grok transport の操作は別会計にする。課金される inference 数、input/output tokens、credits、Human active time は実行ログで測る。

Special も同じ topology を使うが、b は source/lineage cluster、d は章群になる。blind pass は問い・反例・主要系譜、plan challenge は章を跨ぐ比較・総括を含む。長さによる追加 reviewer calls はあり得るが、全章を別々の editor に再設計させない。Profile が違うため、Weekly の b/d や判断基準を固定的に流用しない。

### 3.4 なぜ第三役の追加でも総仕事が減り得るか

費用削減は critic が安いことからは生じない。Worker の暫定成果と Lead の判断を二つの意味正本にせず、既に受け入れた source consumption を後段へ渡し、初期 batch で systematic defect を止めることから生じる。critic はその削減が omission を生まないための費用である。

比較する量は `除ける重複判断・再読・修復費 > criticの探索/読取 + packet準備/transport + 裁定/repair + 新しい保守費`。この不等式が成立しなければ提案は経済的には不合格。Lead/Worker の token 減少だけでなく、critic と Human の操作も足した総費用で判定する。

無料枠や既存 subscription の追加現金費がゼロでも、usage 制限、手動転送、待ち時間、コンテキスト作成、失敗 recovery は無料ではない。全体 elapsed time と各 role の active time を分け、並列実行の active time 合計を wall-clock と混同しない。

## 4. 独立性とモデル選択

### 4.1 独立性は仕事ごとに必要な範囲が違う

| 判断 | 必要な独立性 | 不十分な形 |
|---|---|---|
| Discovery の欠落 | generator inventory 外で検索し、blind 結果を先に固定 | 同じ shortlist に感想を付ける |
| Evidence consumption | high-impact/疑わしい source 本文を直接読む | extraction summary だけから PASS |
| Selection / compression | positive と negative disposition を見て、成立する代案を検討 | selected set のみ review |
| 原稿 fidelity | 著者以外が accepted claims/plan と prose を比較 | author の自己申告を validation と扱う |
| PDF 品質 | exact PDF の全体と該当 layout surfaces を見る能力 | TeX tokens、ページ数、marker の存在のみ |
| Human/Release authority | 決定権と trusted executor を分け exact bytes を検証 | model family が違うから承認成立とする |

追加 critic には Human の希望に沿い、実際に利用可能な別 model family を優先する。ただしモデル別の適性を今回は断定しない。能力条件は source access、locator付き findings、coverage/比較の理解、context容量、返却形式を守ること。これを満たす reviewer を binding する。

別モデルが使えない場合、同familyのfresh context＋blind search を代替候補にできるが、diversity の実績を流用しない。source access がない場合は `NOT_ASSESSED` とし、同じ summary だけの評論を独立 source review に数えない。必要な領域を他 reviewer/Lead の直接調査へ戻し、その追加費用を記録する。

**全モデルへのfan-out投票は標準にしない。** 通常一critic、専門領域の未解決があるときだけ追加する。多数決では claim の真偽を決めず、source に結び付いた findings を裁定する。異なるモデルであっても同じ evidence framing への依存や同じ検索結果に収束する相関リスクは残る。

### 4.2 Findings は小さく、裁定可能にする

必要なのは finding ID、対象 claim/candidate/coverage lane、疑われる欠陥、source locator/digest（取得できた範囲）、編集上の影響、必要な修復、reviewer の確度と未評価範囲である。長い第二の dossier、全候補の別ランキング、内部思考の全文は不要。

Lead は各 finding を `accepted / source-backed rejected / needs investigation` にする。取得できる根拠がなく重要性だけ主張する finding は即 blocker でも即 dismissal でもなく、限定調査対象にする。重要な unresolved finding は Gate readiness を止める。裁定が scope/価値判断に依存するなら Human に具体的代案を提示する。軽微な異議は disposition を残して進める。

既知の重大 finding を「critic一回という予算」で打ち切らない。一方、同じ疑義を証拠追加なしに繰り返す loop は止め、未解決の内容・影響・追加調査で変わり得る判断を明示する。critique は Human decision や承認 snapshot を直接生成できない。

## 5. Grok/X をどこへ置くか

**X research specialist は現状維持を基本に、入力と出力を共通 product へ接続する。** 既存の意味探索を再利用し、新たな X critic を毎号もう一度走らせない。

Grok への初回 brief は Profile/window、coverage lanes、carry-over の問いを渡す。予定している selected set を検索の上限にしない。現行 prompt の broad lanes、未選択候補、counter-signals、event date と momentum date の分離は保持する。[X weekly overlay]

返却後は repository importer が exact bytes を保存し、観測/推論/verification needed を分けて Discovery に反映する。Grok のランキングは X 内の salience の提案であり、号全体の materiality/selection の決定ではない。公式 post を含む場合も、Grok によるその紹介だけで technical Evidence とせず、現在の authority admission を通す。

コミュニティの具体的反応、adoption/reproductionの観測は、根拠付きでその種の claim として表現できる。すべてを無価値な「手掛かり」に戻す必要はない。ただし「特定の投稿がそう報告した」と「技術的に再現可能と確認した」は分ける。読者向け community disposition と quiet-week の扱いも残す。[X intake policy]

Grok が既に担当した候補・X lane を、同じ session のまま独立 critic が検証したと二重計上しない。別の広い critic はその X result を source product として参照し、独立 sweep は主に未担当の公式・論文・repo等を使う。X output が疑わしい、反応と公式説明が食い違う場合のみ targeted X follow-up を行う。

Grok を別の一般 critic として起用するなら、担当領域の重複、blind context の有無、source coverageを記録する。自分のX researchを自分で承認する reviewer として数えない。Special はXの役割が薄ければ `NOT_REQUIRED` rationale を採用し、モデル多様性のためだけにX作業を追加しない。

Drive は transport adapter として残す。prepared task の path を渡し exact result を取り込む現行方式を利用し、Human が長い prompt を再作成する必要をなくす。モデル変更で別 transport が必要なら adapter の問題として切り出す。今回 connector 導入・外部モデル呼出し・Drive 書込はしていない。

## 6. 最小の reusable semantic product contract

### 6.1 三層を混ぜない

五つの論理 product は維持し、その中の再利用対象を次の三層にする。大きな knowledge graph や新しい全体 status enum を作る必要はない。

| 層 | 最小必須情報 | 再利用の単位 |
|---|---|---|
| Source snapshot | locator、exact Raw path/digest、取得日時、既知の公開/更新日時、source kind、derived text と Raw の対応 | 取得した bytes と metadata。URL単位で最新に上書きしない |
| Consumption record | snapshot refs、調べた問い/対象範囲、読んだ本文位置、claim tuples、局所 limitation/未調査範囲、extractor/contract provenance、review disposition | **ある版のある範囲をある問いで読んだ結果** |
| Edition decision | edition scope/cutoff/as-of、event/variant identity、採用する claim refs、materiality rationale、selection/omit/merge、package/比較集合、残余 gap | 当該 edition の判断。自動 carry-forward しない |

Claim tuple の最小内容は `subject + statement + evidence_kind + source_support + temporal/applicability_qualifier`。比較なら comparator、metric なら単位・条件を省略できない。source_support は Raw の page/section/selector/span 等と、その範囲を再発見できる情報を持つ。HTML からの抽出位置は derived text の digest/抽出toolを結び、Raw を参照できるようにする。locator があることは entailment を証明しない。

Consumption record を「全文を消費済み」という一つの bool にしない。短い release note の全体を読んだ場合と、200-page paper の特定実験だけを読んだ場合を区別する。どちらも問いに対して十分なら利用できるが、新しい問いに無条件で再利用しない。claimを作れなかった場合にも source-backed 理由と未調査を区別する。

`NOT_FOUND / RETRIEVAL_FAILED / CAPTURED_UNCONSUMED / CONSUMED` は source/question の処理状態。`publisher claim / independently observed / inference` は statement の根拠種別。`MATERIAL / CONTEXT / ...` は号別重要度。`SELECTED / HOLD / ...` は編集採否。それぞれ異なる軸であり、全体 VERIFIED を一つ付けて代用しない。

### 6.2 C019 を使った説明（新しい production Evidence ではない）

Phase A の保存本文から、たとえば「発表者がmulti-step retrievalと五つの操作を説明している」という claim を、Mistral Agentic Search を主語に、publisher statement として source 本文位置へ結ぶことはできる。「性能が独立再現された」という claim は別物であり未検証と残す。

同じ記録から、次の Weekly は期間内の新規性、Special はretrieval方式の比較上の意味をそれぞれ評価できる。発表記事が読めるのに「本文未取得」とした旧 limitation を継承してはいけない。一方、本文が読めたことだけで benchmark の確からしさや号への採用を決めてはいけない。

この例は代表的な表現方法の説明であり、今回 claim の承認、Evidence acceptance、W34 repair を実施したものではない。固定根拠は [Phase A evidence ledger](../notes/phase-a-evidence.md) にある。

### 6.3 受理の軽さと保証の限界

Worker が consumption record を生成し、Core が必須 fields・参照・source/subject identityを検証する。Lead は重要/新方式/異常な record を直接読んで受理し、通常群は cluster 単位の review と明示された範囲のサンプルを使う。Critic は強い未採用、source-rich/claim-thin、negative-space を重点確認する。

全候補に三者の手動署名を要求しない。review disposition は「誰がどの範囲を何について見たか」を表し、未レビュー範囲に保証を拡張しない。重要 claim の欠陥を検出したら、同じ抽出方式/batch へ調査を広げる。機械的 pattern check は reviewer を誘導する警報であり、消費の意味を証明する validator にはしない。

## 7. 再利用と invalidation の規則

### 7.1 Reuse と acceptance を分離する

**Reuse:** 過去 consumption record を入力にし、同じ本文を不必要に読み直さず新しい仕事を行うこと。  
**Acceptance:** 今回の task/Profile/Screening/contract に対し、出力を検証・受理し active authority にすること。

前者を導入するために後者を省く必要はない。M1/M2 は既存 stage validator/checkpoint/Human Gate を通す。生成される current Evidence Card は current issue/task/basis を持ち、古い acceptance hash を新しい受理へ読み替えない。意味が同じという LLM の宣言で approved Gate を再使用しない。

### 7.2 変更を受けたときの判断表

| 変更 | 保存・再利用する情報 | 必ず再考する情報 |
|---|---|---|
| source bytes が変わる | 旧 snapshot と旧 claim を historical observation として保持 | 新版での support。軽微なサイトchrome変更でも該当範囲の同一性を確かめるまでは自動 current 化しない |
| bytes は同じだが時点/as-ofが進む | 「当時の source がそう述べた」事実 | current availability、現仕様、撤回/反証。freshness確認はclaim種別と重要度で決める |
| edition window/scopeが変わる | 一般的 source consumption | event inclusion、why-now、coverage obligations、materiality/selection |
| editorial question が変わる | 問いに合う既存 claim と対応箇所 | 以前読んでいない範囲、新しい limitation。source全体 consumed扱いをしない |
| comparator/set が変わる | 個々の局所 facts | superiority/ranking、対比、omission、全体balance、synthesis |
| 新しい evidence/contradiction | 旧根拠と判断の履歴 | contradictory claim、関連comparison、selected/omitted alternatives、plan |
| entity/variant/dateの修正 | 関係しないsnapshot | identity closureと関係claim。影響列挙が不明ならstage全体へ戻す |
| prose/layout の修正 | 無関係なfactual extraction | changed prose fidelity、paginationと全PDF、Preview identity |
| extraction/review contract の変更 | 過去 output を historical artifact として保持 | 新contractへの適合と意味保証。単なるprompt更新も結果同等とは仮定しない |

新規候補はそれまでの selected claim を偽にしなくても、選択しなかった理由と相対的構成を変える。従って Selection/Architecture は依存範囲の全体 review を残す。小さな factual record を再利用することと、planの再判断を省くことは別である。

当初の依存表は source→claim→candidate→package の直接参照と、edition-wideな scope/comparison/selection basis だけで足りる。自動の細粒度 DAG validity は導入しない。関連が曖昧なら現行のより広い regeneration boundary を選び、再利用できた factual work だけを再生成入力として使う。

## 8. 品質制御を仕事に比例させる

通常 review で残す最低限は、独立 coverage pass、selected の重大 claim、強い omission、systematic extraction anomaly、全体 thesis/長さ/代案、final source/PDF の非著者 review である。relevanceを見ずに全candidateを深掘りすることも、selectedだけ読むことも標準にしない。

初期 batch review は収集件数や一律claim数でなく、実際に本文の技術的内容が claims に移っているか、帰属が正しいか、limitation が今ある source と整合するかを確認する。ここが不合格なら template を全件へ適用しない。W34 型 defect の発見をfinal ArchitectureからEvidence中へ前倒しする。

機械警報には captured-but-unconsumed、同一limitation反復、sourceに比べ薄いclaim、VERIFIED/UNRESOLVEDの解釈不明、lane消失、極端なcompressionを使う。countやlengthは閾値を跨がないように出力を水増しする目標にはしない。未警報の低リスク群にも source/lane/採否を跨ぐaudit sampleを残す。sample率を今回数値で最適化したとは主張しない。

Grokとcriticの独立探索から新しい重大候補が出たらその候補を通常Evidence経路に入れる。結果を単にdossierの脚注へ追記して済ませない。重要な未解決を `LIMITED` と名付けたことだけで Gate ready にしない。

## 9. 最小の shadow evaluation

### 9.1 比較するものを絞る

比較対象 A は現行 #485 を満たす運用、B は本書の topology＋semantic products＋generated projections。初回から DVC、細粒度 authority invalidation、audit規則変更、renderer変更を同時投入しない。結果の改善/悪化の原因を混ぜないためである。

最初は **historical W34の較正＋fresh Weekly一つ＋fresh Special一つ**。これで全Profileに対する安全性を証明したとはしない。足りない場合だけ次の未見 input を追加し、過剰な factorial 比較を避ける。

1. W34較正: C019、sparse plan、未選択群、Discovery欠落を見つけられるか。既知答えのため安全性・効率の採用判定には使わない。
2. Fresh Weekly: 同じ cutoff/Profile/初期Raw corpusをA/Bへ渡し、互いの結果を見せず実行する。追加検索は同じaccess条件で許し、後からsource取得集合を比較する。検索の能力差も評価対象なので発見候補を事前に同一化しない。
3. Fresh Special: 問い/as-of/期待比較軸を固定し、A/Bに同じ起点を渡す。過去に双方がレビュー済みの完成原稿を新規inputと呼ばない。未検証のSpecial typeへの採用範囲は広げない。

全実験は隔離されたwritable評価領域で行い、production State/Gate/Releaseへ接続しない。未来のhuman approvalを作らず、Gate packageは評価用と明示する。本タスクでは実験を実行せず設計のみを定める。

### 9.2 汚染とgoldの偏りを避ける

A/Bはfresh contextを使い、他armのfindingsや既知修復answerを渡さない。元入力のdigestと開始時刻、使用可能sourceを固定する。実行順による学習を避けるため、可能なら独立実行、順次なら別contextとし順序を交替する。現行同一モデルbindingでまずworkflow差を比較する。

正解集合をAの出力だけにしない。A/Bが挙げたcandidate/findingsのunionに、独立した短いsource sweepと未選択sampleを足し、sourceを見て重要性を裁定する。Humanは匿名化・順序を変えたdossier/原稿を評価し、どちらの方式かを判断材料にしない。完全blindが不可能な差は記録する。評価のための追加裁定費は実験費として分け、本番見込費に紛れ込ませない。

### 9.3 記録するのは五群だけ

| 群 | 最小の測定 | 解釈 |
|---|---|---|
| 品質 | source-backed重要omission/誤帰属/未消費、最初の発見stage、最終reader品質 | discovered findings数が多いだけで高品質としない。残った欠陥と修復後を両方見る |
| 人とLLMの仕事 | Human active time、role別active time、provider usage（input/output tokens又はcredits）、elapsed/wait | 取得不能usageはunknown。subscription率をAPI token換算しない |
| 再読と再生成 | 同source digestを誰が何のために再読したか、重複抽出assignment、repair原因と対象範囲 | 必要な独立検証と無目的な重複を区別。delivered tokensと本人のread申告も分ける |
| 連携とtool | logical assignments、依頼/返却pair、手動transport時間、CI/build時間 | 短いcalls増加と総入力肥大化を捕捉 |
| authorityとreview負担 | hash/approval/State不一致、false-positive findingと裁定時間、未解決finding | 安全性を総合点の小さい減点にしない |

品質裁定は重大度を先に定義する。criticalはauthority誤り/公開bytes drift等、majorはreaderの重要な理解・採否を変えるomission/誤帰属/未消費、minorはそれに至らない欠陥。page count、候補数、top-level VERIFIED数は記述情報であり合否ではない。

### 9.4 Cross-family critic の比較は限定的に行う

workflow比較に加え、fresh caseの同じ固定planを **same-family fresh criticとcross-family critic** に別contextで渡し、同じsource access・budget条件でblind→planの順に評価する。比較結果はmain A/Bの原稿作成へ途中投入せず、critic topologyの追加価値として裁定する。

モデルの優劣だけでなく、source access制約、context転送費、false positives、実質的に新しく重要なfindingsを測る。異なるfamilyが常に有利とは仮定しない。全Gemini/Muse/Grok候補の総当たりはしない。まず利用可能な一つを試し、能力条件や費用で不合格なら次候補に替える。

### 9.5 採否と停止条件

- critical回帰はゼロを要求し、一件でも出れば該当変更を停止。publication bytes/approvalの緩和とは交換しない。
- fresh casesでBにのみ残るmajor欠陥があればreviewを弱めるadoptionは不可。既知W34にだけ効く結果も不可。
- A/B双方のmajor欠陥、共通盲点、裁定未確定が残るなら勝者を決めず、共通修復か追加の限定caseへ進む。
- Bのreader品質・coverage・fidelityが少なくとも同等と判断され、全roleとHuman/CIを含む仕事の削減が見える場合に、**試したProfileと運用範囲に限る小規模pilot**へ進める。
- 経済性は原則Pareto改善（品質を落とさず総仕事削減）を求める。usageは減るがHuman負担が増すなどtrade-offがあるなら勝手に単一スコアへ換算せず、内訳をHumanの採用判断へ提示する。
- 一つずつのfresh Weekly/Specialはscreening evidenceであり統計的なnon-inferiorityの証明ではない。継続pilotで監視し、major escapeなら旧review強度へ戻す。小さい差しかない場合は測定誤差/号差を疑い、追加caseが採否を変えそうなときだけ増やす。

改善が大きくても、独立blind coverage、強いomission点検、exactHuman/PDF安全性はこの比較で削除対象にしない。削減対象は重複判断と全段階の再構成である。

## 10. 実装設計へ進める範囲と未確定範囲

| 範囲 | 今回の判断 | 次に必要なもの |
|---|---|---|
| Generated resume/current status | **実装設計可能** | machine authorityからのprojection仕様、stale/missing参照の表示、既存indexとの差分検証 |
| 少数の意味正本→既存artifacts | **adapterの実装設計可能** | materiality/selectionの概念を保つmapping、既存schemaとのround-trip、単一writer |
| Consumption record / context packet | **最小contractとshadow計測の設計可能** | 上記fieldsを既存source/cardにどこまで再利用できるかの狭いmapping |
| Release producer/consumer不一致 | **独立maintenance設計可能** | exact-byte publishとState adoptionのboundary regression。大再編の完了を待たせない |
| Focused reviewer / cross-family binding | **architecture候補として具体化済み、production採用にはevidence不足** | fresh比較、能力と総費用、major escapes |
| Semantic acceptanceのcache化、細粒度Gate reuse | **見送り** | hidden dependenciesとauthority equivalenceの独立実証 |
| 全Core audit緩和、DVC/Temporal置換 | **後続判断** | measured bottleneckと実証。今回の導入条件ではない |

モデル・課金・transportの最適binding、batchサイズ、sample率、号ごとの実costは未確定。これらを机上で固定するより、上記の小さい実験で選ぶ方が低コストである。architectureの責任・product・authority境界自体は、その比較を行える程度に明確になった。

実装設計へ進めるという判定は **次の明示タスクで設計してよい成熟度** を表す。本書を根拠にproduction implementationやmigrationを開始しない。

## 11. 終了判断

今回の追加証拠は、Grokが既にsemantic specialistであること、Evidence authorityがedition/taskに結ばれていることを明確にし、Phase Aの曖昧なrole常駐像と再利用の意味を修正するのに十分だった。さらに広くrepository/OSSを読むことより、fresh inputsでの比較の方が次の判断に有用である。

**推奨は、一つの編集責任と局所生成、独立blind→plan challenge、意味成果の入力再利用、現行authority acceptanceの維持。** 第三LLMの常駐化、モデル投票、semantic authorityの即時cache化は採らない。refinementをここで完了し、production側の変更には進まない。

[X common policy]: https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/config/prompts/grok/x-source-intake-base-v1.md
[X weekly overlay]: https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/config/prompts/grok/x-source-intake-weekly-v1.md
[X intake policy]: https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/docs/survey-production-core-v2-x-source-intake.md
[Evidence schema]: https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/schemas/evidence-v2-card.schema.json
