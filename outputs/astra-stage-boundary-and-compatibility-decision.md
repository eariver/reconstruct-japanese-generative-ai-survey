# Stage境界・歴史互換・検証費の判断

日付: 2026-09-11 JST  
状態: **ISOLATED STAGE REPRODUCTION COMPLETE / EXPERIMENTAL PATCH / NO PRODUCTION ADOPTION**

## 1. 結論と次のdecision surface

**canonical直接authoringの前提として、Evidenceの共通入力・再検証境界を補強する狭いCore maintenanceを推奨する。新しいauthoring engineやsemantic DSLの設計を先行させない。**

前回の4反例は、直接acceptance関数だけでなく、隔離した実Git fixtureのstage検査と正規checkpoint更新も通過し、`EVIDENCE_REVIEWED`へ到達した。前回残した「別のstage検査が拒否するかもしれない」という留保は、今回のThematic fixtureでは解消した。

1 moduleの[比較用patch](../notes/phase5-evidence-boundary-proposal.patch)で、正しい候補のstage到達を保ち、4反例を受理前に拒否できた。新しいcanonical artifact、State、review roleを追加しなくても、この境界は補強できる。

ただし、これはそのままproductionへ適用する完成PRではない。特に次の方針を明示する必要がある。

- **新validatorはactiveな再検証にも適用する。** 既存acceptedという理由だけで不正なCardを許可しない。
- **歴史は当時のbytes・commit・contractで再現する。** 新validatorの拒否を消すために、旧Cardや旧approvalをbackfillしない。
- **検証費は意味reviewを省いて削減しない。** exact schema bytesに対応するcompiled validatorの再利用を、純粋な計算の最適化として別途統合評価する。

次に必要なのは、この狭いmaintenance候補に対するactual callers・既存歴史・trusted runtimeの回帰確認と、独立したsource/target品質評価である。広いarchitecture移行を承認する根拠にはまだ届いていない。採用・migration・進行中editionへの適用はHumanに残す。

## 2. Snapshotと調査の選択

起点: [前回のcanonical入力検証](astra-canonical-ingress-validation-decision.md)。reconstruct開始HEADは`4a403bf3bd6f04777cea1e287bf38514f5db9b36`、開始時clean。

- mainはread-only remote確認で`6d748a962d57beff89da7c1b20cb5a9a86c8e261`、変更なし。前回export済みの固定sourceを再利用した。
- W34は`498e45b5648f418e346e1a171dc588494dacf716`へ1 commit進んでいた。compareの変更一覧とStateだけを確認した。`ARCHITECTURE_ESTABLISHED`、Architecture Human Gate pending、`HUMAN_GATE_REACHED`。これは現在の固定snapshotであり、承認済みとは扱わない。
- W34の追加はeditionのArchitecture成果・実行記録・checkpoint/Stateで、main Coreの変更はなかった。今回の境界検証をArchitecture reviewへ拡張しなかった。
- productionへのwrite、fetch/pull/push、checkout変更はない。実験用Gitのinit/commitだけを独立temporary directory内で行った。reconstruct本体にもcommitしていない。

調査は、stageまでの再現、共通境界へのpatch、旧acceptedの新validator下での挙動、schema検査の小さい費用比較へ絞った。全repo監査・全paper再生成・新framework探索は実施していない。

## 3. 正規stage経路での反例再現

[stage probe](../notes/phase5_stage_probe.py)はLinux/Python 3.10.6、`jsonschema==4.23.0`、Coreが指定する`pypdf==6.16.2`で実行した。pypdfはstage moduleのimportに必要だっただけで、PDF生成・公開はしていない。

fixtureごとに固定sourceをcopyし、独立Git repoへcommitする。その実commit SHAでProfile/Stateを初期化した。前回の`4444...`実装identityから進め、次を実行した。

```text
実fixture commit → Profile/State初期化
  → X NOT_REQUIRED manifest（Thematic試験の判断）
  → Discovery acceptance
  → validate_stage → build_stage_checkpoint → advance_with_checkpoint
  → Screening acceptance
  → validate_stage → build_stage_checkpoint → advance_with_checkpoint
  → Evidence candidate / acceptance / Views / Ledger / Completeness
  → validate_stage → build_stage_checkpoint → advance_with_checkpoint
  → EVIDENCE_REVIEWED（Human Gatesはpending）
```

validatorやState検査はmockしなかった。legacy helperをagent-first Stateから呼ぶ箇所では、productionの既存`current_stage_basis_override`を使った。これは今回独自にhash検査を無効化した処理ではない。

fixtureのclaimsとCompleteness判断はsyntheticで、実研究の完了宣言ではない。review rowsも実stage validatorの結果を参照する`DETERMINISTIC`のみであり、semantic reviewやHuman approvalを偽装していない。外部workflow admission、lease、GitHub上の権限、並行実行は試験していない。

### 結果

[stage結果](../notes/phase5-stage-results.json)には各fixtureの実commit、停止点、State／過去bytes不変性を保存した。

| Candidate | fixed main | 共通境界補強版 |
|---|---|---|
| 正常 | `EVIDENCE_REVIEWED` | `EVIDENCE_REVIEWED` |
| task targetを全削除 | 同上 | candidate受理前で拒否 |
| 同じtargetを重複記録 | 同上 | candidate受理前で拒否 |
| claimの必須`text`を削除 | 同上 | schema検査で受理前に拒否 |
| 同じ`status` JSON keyを2回記録 | 同上 | JSON読込で受理前に拒否 |

補強版の4失敗では、accepted directoryが作られず、拒否前後のState bytesも不変だった。正常caseのHuman Gatesはpendingのままで、Architecture以降には進めていない。

**この結果はmachine stage boundaryの具体的な欠落を示す。実際のpublished issueに同じ欠陥が存在すること、全runtimeで悪用可能なこと、semantic reviewを通過したことまでは示さない。**

初期harnessの調整も残す。pypdf不足、agent-first Stateにlegacy helperを直接当てたcheckpoint path不一致、旧unit fixture由来のCompleteness obligation ID／expansion count不一致で一度ずつ停止した。それぞれ指定依存の追加、既存runtime contextの使用、実Profile／Discovery由来のfixture値への修正で解決した。validatorを弱めて通したわけではない。

## 4. Patchの責任範囲と、まだ完成ではない点

[proposal patch](../notes/phase5-evidence-boundary-proposal.patch)の対象は`survey_evidence_v2.py`のみ。

- Card専用読込でduplicate keyと非objectを拒否する。
- repository contextがあるCard検査で既存schemaを検査する。
- exact task target集合を一度ずつ返すことを検査する。
- 新しいcandidate受理と、accepted Card再検証の両方で同じCard読込を使用する。

fixed mainのscriptsを検索すると、`validate_evidence_card`の呼出元はinteractive runner、Core受理、Core再検証で、いずれもrepository contextを渡していた。既存runnerは同じvalidatorを通るため、個別writerへ別の検査wrapperを増やさずに済む。dynamic／外部callerの不存在までは証明していない。`repo_root=None`の関数呼出は依然schema検査を行わず、単独でproduction受理APIとは扱わない。

既存Evidence moduleの12 unit testsは補強版でも通った。[互換結果](../notes/phase5-compatibility-results.json) これは全Core regression、全audit、workflow/trust試験の代替ではない。

**patchは検査位置を示す実行済みproposalである。** schemaの再読・再compile費、エラー診断の粒度、全set検査中の競合、checkとhash/copyの時間差、trusted runtime統合まで解いた完成版ではない。とくに`check`の結果だけを保存して後で別bytesを受理するAPIは作らない。次の実装レビューでは、検査したbytesと受理・hashしたbytesの関係、および既存lease／staging所有権を確認する。

## 5. Historical reproducibilityとactive eligibility

前回は「旧acceptedへの適用が未検証」だった。今回はsynthetic旧acceptedを後継commitのvalidatorで再検証するところまで進めた。

1. fixed main相当のfixtureで、正常／不正Cardを正規stageまで受理。
2. source・accepted artifacts・Stateをそのままにし、validatorだけを補強した後継fixture commitを作成。
3. 新process・新commit identityと既存runtime contextで`validate_evidence_acceptance`を実行。

正常Cardは通り、4不正Cardは拒否された。いずれもsource配下の全file hashは前後で不変だった。つまり、旧実装で通った結果を保存したまま、新実装下では利用不可と判定できる。**旧PASSを新PASSへ付け替える必要はない。**

加えて、既に分析したW34 C019／paper／C033、SP001-D008の4 actual Cardsに、strict decode・Card schema・exact target集合の追加検査を当てた。4件とも通過し、bytes hashは前回Evidenceと一致した。これは追加規則との標本互換であり、4件のfull historical authority replayでも全409件の検証でもない。

### 推奨policy

| 問い | 扱い |
|---|---|
| 当時何が受理／承認されたか | 当時のcommit・contract・Raw/Card/PDF・review/Gateを保存して検証する |
| 現在のcodeでactiveなstageを進められるか | 現在の検査を適用し、不正なら止める |
| 古いacceptedが新検査で失敗したら | editionへの影響を診断し、現行revision／再reviewを使う。無言のbackfillはしない |
| frozen/releasedな過去成果をどうするか | bytesと過去authorityを保持する。publication correctionの要否は別のHuman判断 |

全acceptedを常時grandfatherする案は採らない。新規writeだけstrictにしてactive再検証を旧仕様のままにすると、今回の欠落がstage境界に残る。一方、旧実行の再現まで新validatorで成功することを要求すると、過去を改変する圧力になる。保存された実行と現時点の利用可否を別に表示する方が、診断とHuman handoffの混乱を減らせる。

## 6. 検証費を増やさないための局所Evidence

共通validatorへschema検査を入れると、下流の再検証でもその費用が掛かる。前回のsource candidateを同じschemaで200回検査し、順序を入れ替えて2回比較した。[script](../notes/phase5_schema_cost_probe.py) / [結果](../notes/phase5-schema-cost-results.json)

| 操作 | 200回のelapsed time |
|---|---|
| 現行schema helperを毎回呼ぶ（schemaの読込・check・validator構築を含む） | 4.37秒、4.28秒 |
| schema bytesのSHAに対応するcompiled validatorを再利用し、Card自体は毎回検査 | 0.52秒、0.54秒 |

同じpathのschema bytesを変更した場合は別validatorを構築し、元Cardを拒否することも確認した。cache対象はschemaの処理系だけで、Card PASS、semantic review、Human approval、stage acceptanceではない。

これはsingle Cardのmicrobenchmarkで、stage全体やlifecycle workが約8倍改善するという意味ではない。一般のexternal `$ref`、並行実行、cache容量上限、全schemaへの適用は試験していない。実装するなら今回のlocal-ref Card schemaから始め、関連schemaを含むexact contract identityを誤ってcacheしないことを確認する。

**削減対象としての価値はある。** 安全検査を省略せず、その実行準備を共有できる。これが成立すれば共通境界の補強費を抑えられる。ただし現proposal patchにはcacheを入れていない。global schema helperを不用意に変えるより、実際のstage負荷と回帰を確認した上で適用範囲を選ぶ。

## 7. Total lifecycleの判断と実行経路

今回の結果は「別のsemantic engineが必要」という判断を支持しない。既存Coreの入出力境界を揃える方が、契約数とwriter別の検査重複を小さくできる。sourceの意味生成は別の問題として残る。

| Work | 今回前進したこと | 未実証 |
|---|---|---|
| production | canonical候補をそのまま正規stageへ渡せる。構造不正を共通境界で拒否 | fresh source品質、実operatorの負担 |
| review/repair | source問題・入力構造・binding・stage失敗を切り分ける具体例 | independent omission review、修復時間の削減 |
| maintenance | 1 moduleの境界補強で複数known callerへ効く | 全caller／全contract／workflow回帰、broad audit費 |
| regeneration | 旧bytesを保持して新validatorで再評価できる | 全歴史の再現性、model再生成の同値性 |
| Human handoff | 当時の受理と現在の利用可否を分けて報告できる | 実運用での質問・裁定負担の減少 |
| compute | exact schema処理系の再利用に局所的な削減余地 | 全stage／全role／長期ROI |

### 次の実行単位

**A. 狭いboundary maintenanceの採用候補を完成させる。** 本patchと反例を起点に、actual agent-first caller／既存受理セットの適用影響、trusted runtimeとlease/staging、schema compile再利用、必要な広いregression・auditを確認する。old artifactを修正して互換性を作らない。独立した保守候補として提示でき、source authoring刷新の完成まで待たせる必然性はない。

**B. source authoringは問いと独立評価へ進める。** 前回paper candidateと、異なるfailureを問えるsourceで、既存`verification_targets`を具体化した場合のauthor/reviewer/operator workを比較する。canonical入力と明示source supportは維持するが、全候補に最大詳細を強制しない。今回も独立semantic reviewはしておらず、自分の再読を代替には数えていない。

この2つは依存の異なる仕事である。Aのmachine PASSをBの品質PASSに換算しない。Aが安全性を改善しても、Bの記録量増がreview/repairを減らさなければauthoring側は縮小する。総費用の測定なしに、review削減・global semantic cache・全stage移行を承認しない。

採用判断時には、対象future edition/Profile/stage、具体的差分、試験範囲、既存artifactでの失敗と対応、外す旧処理、rollback/invalidation、残る費用を提示する。Human承認前のproduction書換えはしない。現在のW34のHuman Gateやfrozenな過去editionを実験の都合で動かさない。

## 8. 再現と継続

前回の`phase4_prepare_lab.py`で固定snapshotを用意する。Linux依存は固定snapshotの`config/survey-production-v2-requirements.txt`に合わせる。Windows側のfixed-ref helperで4歴史標本を用意し、その後Linuxで実行する。

```text
python -B notes/phase5_stage_probe.py --prepare-history .phase4-lab-snapshot
python3 -B notes/phase5_stage_probe.py .phase4-lab-snapshot notes/phase5-stage-results.json
python3 -B notes/phase5_compatibility_probe.py .phase4-lab-snapshot notes/phase5-compatibility-results.json
python3 -B notes/phase5_schema_cost_probe.py .phase4-lab-snapshot notes/phase5-schema-cost-results.json
```

最初のcommandはproductionをread-onlyで読み、ignored snapshot配下へ分析用inputを作る。stage probeのlocal Git commitsは再実行時に変わる。結果のmodule SHAが検証対象codeを識別し、fixture commitはその回のState/checkpointを結び付ける。temporary path・測定秒数・commit SHAの一致を再現条件にしない。

今回追加したdurable成果は本書、proposal patch、3 scripts、3結果JSON。前回のignored labと依存は再利用して残しており、削除の再試行はしていない。今回作った独立Linux fixturesは各試験の終了時に通常のtemporary-directory cleanupで終了した。

**終了判断:** 反例がstageまで通るか、どこで共通拒否できるか、後継validatorが旧acceptedへ与える影響、検査費を安全に抑える候補まで具体化できた。同じsynthetic caseの追加は、独立品質評価やtrusted production admissionの不足を埋めないため停止する。

継続は本書§1・§5・§7から。前回の「stage未実行」は、**Thematic synthetic fixtureで正規stage/checkpoint実行済み、外部trusted workflow・lease・並行性と実production適用は未検証**へ更新する。production adoption/migration、State、Human decisions、Gates、Freeze、Release、reconstruct本体のcommit、通常Pull/Pushは行っていない。
