# DM022 pre-Architecture — pre-code readiness assessment

2026-10-28、Astra author-side判定。**PRE_CODE_READY（具体設計・interface map限定）**。独立readiness reviewとAstraの最終確認を完了し、**このunitのHuman Commit Pointで停止**する。実装・runtime検証・Production採用の完了ではない。

## 1. 正本と読む順序

1. [選択済み契約 INCLUDING §11](rephase-1-dm022-prearchitecture-contract-decision.md)：SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`、31351B。不変。
2. [今回packet](../notes/rephase-1-dm022-prearchitecture-precode/README.md)：R3詳細→R4訂正＋literal schemas→R5 family map→R6 role mapの優先関係。
3. **[mandatory Astra resolution INCLUDING §5](../notes/rephase-1-dm022-prearchitecture-precode/astra-precode-gate-resolution.md)**：全文SHA256 **`0425c5300c9c7211e4468d3b842c4e3af1acb9f5bf1eba00e90f7ba72ef44a5a`**、13788B。旧37行`56b66880…`は§§1–4 snapshotのみ。
4. **[独立readiness review §§8–9](../notes/rephase-1-dm022-prearchitecture-precode/independent-readiness-review.md)**：§8.3の限定＋§9 FINAL-BINDING ROOT確認が必須。全文SHA256 `b3a3630a0c27d92e52c7cbcb0f44c8d9d3ad7aea9a892c6eb1c71b0d161afad1`、83057B。

初稿の作者完了表現やR1–R5のNOT_READYを削除・上書きせず、最終組合せだけを今回の判定対象とする。独立reviewは作者の実装承認やHuman承認ではない。

## 2. 今回閉じた設計面

| 面 | 確定した実装境界 |
|---|---|
| 受理操作 | exact `EVIDENCE_REVIEWED`窓、新immutable Evidence/Views＋versioned Ledger/Completeness、外部供給の独立判断、truthful同State checkpoint、既存3参照を同recordへco-update。forward履歴・Human権限維持 |
| LOW/HIGH | 新LOW `survey_research_authority_v2.py` はpath再読込・detached検証・pure計算・passive readiness。新HIGH `survey_prearchitecture_acceptance_v2.py` が全write/guard/State/clearを所有。public strict agent State検証はHIGH側で保持 |
| 具体schema/DAG | 5 standalone schema proposals、厳格なnested records/role registry/FILE対self-digest。prepare→存在するcandidateを外部decisionが束縛→proof/report→checkpoint→State→completion。future/self SHA循環なし |
| consumer/役割 | R4の40行caller inventory、17 schema関連site（2宣言・2payload validator・13file loader）＋8 branches。active四入力からSelection/Architecture/Draft/publicationまでのreadback。旧canonical Ledger/Completenessへのfallback不可 |
| guard/再開 | ANY guard下でnormal writer拒否、entry/prepublish確認。before-State＋7slot COPY保持、planned checkpoint、State旧/新/unknownの分類、exact旧slot clear、completion後guard release。unknown Stateをrollbackしない |
| 7slot | Matrix/Selection/Architecture/summary/attention/input archive/**audit**。通常runnerもauditを含めno-overwrite。後続再生成後のLIVE Stateやslot不在を古いcleanup receiptへ要求しない |
| source family | G67/G71/G76のliteral membershipと関数別owned-epoch分岐。pipeline67/71/76、replay50/63/70・新union73、canonical29/34→36/41は計画集合。新2module＋5schemaをclosureへ含める |
| Profile/義務 | genuine supported typeのみ、完全なProfile-initial∪Discovery-named obligation結果。DM016 map不一致・DM017広範supportの解決や全Profile受入れと同一視しない |

**研究checkpointとpublication activationは別型・別履歴。** R5が混同したpublication `_record_kind`/`supersedes`へのPREARCH追加はR6＋ROOTで撤回。PREARCHはupstream研究nodeとしてのみ読む。validation/freeze/release/selectionや`publication_revalidation_provenance`へ差し込んだらwrong-family拒否。forward Stage Checkpoint schemaに`prior_checkpoint`等を追加しない。pointer recordの分類用未信頼読込と、役割確認後の参照先authority消費を区別する。

G71→G76の限定mechanical compatibilityは、同じ研究/Profile/Architecture/Draft/reader authorityを保った既知source変更を通常renewalの全current proofで検査するためのもの。family名だけの移行・新upstream受理・post-Architecture訂正・任意schema/recipe migrationは許可しない。研究checkpointの過去report epochを後日のpublication tool HEADと同一にすることも要求しない。

## 3. Review経過と限定

- R1/R2：nested schema不足、direct reader/API不足、single-resolver過大主張、forward builder/no-State-arg guard、HEAD/tree条件等を訂正。
- R3：LOW書込み責任、schema registry、completion/readiness、source-family対応の不足を独立reviewで拒否。
- R4：五literal schemas・40行・guardを閉じたが、owned-epoch familyの関数別分岐が不足。
- R5：family分岐を具体化。ただしPREARCHをpublication chainへ広げる記述が残りNOT_READY。
- R6＋ROOT：17siteのexpected role/producer、publication側discriminator/walker/selector拒否を具体化。独立§8はPRE_CODE_READY、§9は全文ROOT§5の補正と同じ判定を最終確認。

ROOTが訂正したR6 row14は`editorial_correction:557`の**元validation checkpoint**（`DRAFT_COMPLETE→VALIDATED_DRAFT`）。Selection/Architecture/Draft graph rowとは別。publication mode probeの現`else CANONICAL`にPREARCH拒否が必要なこともactual sourceで確認した。これらは将来codeへ渡す具体predicateであり、既存sourceが既に修復済みという証拠ではない。

## 4. Source・作業状態・残課題

開始HumanHEAD **`ab84b4f`**、main。今回は資料作成とsource読取のみ。runtime module/schemaの配置・import・test/build・fixture・restore・network・ordinary Commit/Pushは行っていない。schema proposalsはnotes内の設計資料。

利用可能なread-only sourceは `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`、actual409/tree8ce＋93paths（40M53A）/742 intended files。完全DIRECT409 patch **f898d33b… /3423014B**とmanifest **d488c6ee…**の配送証拠は[前renewal packet](../notes/rephase-1-versioned-renewal-implementation/README.md)を引き継ぐ。旧57内包、overlay重ね不要。今回新たなfull93/742/inode証明はしていない。partialDB/missing26309/bulk31466、runtime/TeX非同梱、whitespace・過去失敗の限定を維持する。

前packetの**55 bare Gitlinks**は保持。54 child-untracked-only＋1 tracked-dirty fault fixture、全55 HEAD一致という情報は[前unitの観測](../notes/rephase-1-dm022-prearchitecture-contract/source-and-carryover-observation.md)であり、今回の再認証ではない。親Gitlink commitはchild DB/untracked bytesを同梱しない。cleanup/移動/index修復はしていない。`--ignore-submodules=all`での確認は親の限定確認で、nested cleanを意味しない。

**Whole NOT_READY / step4B3 OPEN / audit未開始 / DM021+022 OPEN**。閉じたのは契約B2/B4を含むpre-code map gate。実装、必要Profile、代表的研究/出版品質、固定候補の独立七観点audit、Human採用・実運用、総work削減は未完了。W40再現・upstream CORE_FIXEDではない。

## 5. 次のHuman continuationで行うこと

GeneralがROOT§5.2と契約§10に沿い、**whole prepare→外部decision→adopt/resume→通常再生成→後続lifecycle/readback**を実装・検証する。独立したfinal93由来source/fixture、disjoint担当面と固定実行snapshotを使い、source実装と別に必要な独立implementation reviewを行う。新しい必須reader/closure・契約矛盾が見つかったらAstraへ戻す。

必須witnessはWeekly＋Thematic、full four-artifact acceptance、affected/unaffected意味比較と完全obligation、7slot保持・audit no-overwrite・再生成、repeat、wrong-role拒否、後続Architecture/Draft/publication、history/current source分離、G71→G76 unchanged-upstream compatibility control、G76訂正→initial publication→later editorial/renewal。old/new/unknown State、guard/completion紛失、stale Raw/HEAD、ownership/close/replace fault、late seamの明示resumeを含める。synthetic reviewは真正承認ではない。旧test-count/PASSを新sourceへ転用しない。

**ここでHuman Commit Point。通常Commit/PushはHuman-owned。今回の継続許可を次unitの自動開始に使わない。**
