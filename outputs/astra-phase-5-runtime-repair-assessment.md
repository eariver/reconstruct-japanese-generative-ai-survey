# Phase 5 — Freeze/Release限定修復候補

日付: 2026-09-14 JST
状態: **ISOLATED REPAIR CANDIDATE / 58 TESTS COVERED WITH GIT-FIXTURE FOLLOW-UP / NO ADOPTION / NO CONDITIONAL 5-C**

## 1. 判断と範囲

前回選んだFreeze/Releaseの契約不整合について、reconstruct内で修復候補を実装した。新しい意味層・renderer・reader gateの実装には進んでいない。conditional 5-C A/B trialも未開始であり、この作業はPhase 5内の限定runtime保守候補である。

開始時のreconstruct local HEADとremote mainはHuman指定の`f5dffe5c3c748a545437b21f1e43a145a041ba4d`に一致し、working treeはclean。production mainをGETで確認した結果、前回と同じ`3e3eebe0cda3a32ac88ae764d279b37768f6bfca`だった。対象Shared Coreは未修復なので、同じ修復の重複実装を避けるための再調査をここで止めた。W34のState/PDF/Release metadataやIssueは再取得していない。前回のmain RELEASED / W34 branch FROZENという観測を新たな全chain検証と混同しない。

候補は[patch](../notes/phase-5-runtime-repair/candidate.patch)と[追加テスト](../notes/phase-5-runtime-repair/test_runtime_repair.py)に保存。変更するproductionコードはstage validatorとrelease checkpoint producerの二つ。既存release単体テスト一つを新report出力に合わせ、実際の接続は別の合成editionテストで検証する。production checkout、State、Human決定、PR/Issue、公開Releaseは変更していない。

## 2. 修復した接続

| 境界 | 候補の動作 | 保持する制約 |
|---|---|---|
| Human Preview → prior artifacts | approval pointerを専用schema/validatorで読み、承認されたexact Candidateへ直接進む。StateのHuman/機械checkpoint pointerが一致しない場合は拒否 | Stage Checkpointとして読むことも、pointerを単にskipして近くのCandidateを選ぶこともしない。Candidateのpublication/research profileもStateと照合 |
| Freezeのartifact集合 | runtimeもschemaと同じfreeze-record / release-manifest / visual-review-recordを受け取る | visualはCandidateにbindされた承認前recordのpath/SHA/byte count。承認後の新reviewを要求しない |
| Freezeの内容 | supplied Freeze/Manifest/approval/Candidate/VISUAL、source/PDF/pages、issue/profile/release identityを相互照合 | 同じPDF hashだけで別Candidate・別manifest・別pathを受容しない |
| FROZEN → RELEASED | compact validatorが外部処理後のlocal adoptionを検証し、既存CORE_STAGE_CONTRACT形式でState/Profile/contract/tool/artifactsにbindするreportを生成 | controllerの必須guardを維持。外部exact-byte reconciliationのRelease recordも別の既存reviewとして保持 |
| local adoptionの再試行 | 既にあるreport/checkpointは、現入力・State・Profile・契約・toolが一致する時に最初のrecorded_atとbytesを保持して再利用 | timestamp以外の差を無条件に受容しない。外部Releaseを作成・上書きしない |

`build_stage_report`は既存の検証→report生成部分を取り出した関数であり、検証なしのPASS emitterではない。従来の`validate_stage`は同じ結果をimmutableに書く公開入口として保持した。FROZENではRelease/Merge Verificationを、Stateが保持するFreeze/ManifestおよびHuman-approved Candidateへつなぐ。

Stage schemaにFROZENの新必須項目を遡及追加してはいない。古いRelease checkpointを新形式へ書き換えず、新producerがcurrent controllerの要求するreportを出すようにした。reportは既存controllerが要求していた種類であり、claim正本や追加Human Gateではない。

## 3. 検証とその意味

未修復baselineに同じ実行用fixture classを通すと、Weekly / Thematic Special / Retrospective Specialの全3条件で、schema-required visual-review-recordをruntimeがunexpectedとして拒否した。[baseline結果](../notes/phase-5-runtime-repair/baseline-results.json)。これは前回の抽出early guardだけのwitnessより広く、実際のschema/State/approval検証を通過した合成入力による失敗である。

候補の同じ正常系は、実際のstage validator → checkpoint builder → controller advanceでRELEASEDへ到達し、外部成功の固定recordとlocal checkpointを残してState advance前に中断したケースから、時刻が違う再呼出しでも同じcheckpoint bytesを保持して継続できた。

関連回帰は58種類を確認した。[初回結果](../notes/phase-5-runtime-repair/test-results.json)は52 PASS / 6 errors。6件はHuman Gateテスト用Git rootの設定不足で、fixture commit内のpathを解決できなかった。独立したGit rootと接続しないfixture-only originへ修正した[該当系統の再実行](../notes/phase-5-runtime-repair/git-aware-results.json)は8件すべてPASS。source/test bytesは同じであり、52件の成功済みtestは繰り返していない。初回840.874秒、該当系統205.703秒はテストelapsedで、全role費用ではない。

Git-aware既存テストが親reconstructのGitを継承した最初の実行では、fixture objectsとtest refが作成/更新された。HEAD/main/通常indexは不変、test refはcleanup後不在で、現在remoteにも同名branchはない。pre-test ref値は未記録。この環境不備と、独立Gitへの切替後にorigin未設定の試行を中断した経緯も[Evidence](../notes/phase-5-runtime-repair/README.md)に残した。後続はignored領域のテスト専用Gitだけを使い、guardを弱めて通していない。

追加テストはState/schema/publication/approval/stage/controller validatorをmockしない。既存publicationテストの合成本文・空白PDF・review fixtureと、明示的に構成した研究工程の歴史fixtureを使う。合成のHuman approvalもfixture内だけ。実際の研究、独立editorial判断、Human品質認定を実行したのではない。既存release producer単体テストは従来同様に依存をstubし、実stage結果を模したreportの構造を検証する。その単体テストと、validatorを通した接続テストを区別する。

候補作成中、fixtureが存在しないtop-level prompts directoryを要求していた誤りと、候補のVISUAL比較がbyte_countを含む型を二要素refとして比較していた誤りを検出・修正した。正常系が実際に通る前の負例成功だけで修復済みと判断していない。

## 4. 呼出し経路と未実証

current operator bridgeはrequestのartifact集合をstage validatorとcheckpoint builderへ渡す。Freeze requestはschemaが要求する三つを明示する必要がある。configの二つのcanonical artifactsはminimumであり、現在のschemaの全要求集合ではない。既存bridgeのrequest処理そのものは今回再実行していない。

current Release workflowは外部identity/assetの照合後、同じ`survey_release_checkpoint_v2.py`を呼ぶ。今回このhelperからcontrollerまでの接続を検証したが、Actionsのshell、実GitHub permissions、PR作成/merge、全dispatchは実行していない。Release Recordのfixtureは「外部照合が済んだ」という固定観測入力で、rootが外部downloadの真偽を独立実行したことにはならない。

**再試行の証明は固定済みRelease Recordからのlocal adoptionに限定する。** workflowが再dispatchされるとMerge Verification/Release Record builderにも新しい時刻が渡る。同一checkoutに旧recordが残る場合のそれらのimmutable write、main更新後のtarget identity、RELEASED後の再呼出しは、この候補で全て解消したと扱わない。公開Releaseを再作成して回避することもない。

legacy Action/Handoff handlerのfreeze validatorは別経路であり、今回のcompact agent-first修復に含めない。全Core互換、旧号の実データ再実行、全publication quality、全profileの任意caller、concurrent mutation、実workflow failure recoveryは未実証。既存historical revalidationテストと合成履歴維持の検証も、全歴史dataの再現保証ではない。

## 5. 総仕事への含意と停止条件

支持できる差は、標準的なartifact集合をruntime調整なしに検証でき、release producerがcontrollerに拒否される必須report欠落を除いたこと。必要なHuman判断・source確認・独立review・最終PDF reviewを別roleへ押し出した差ではない。ただし実行時の再検証/JSON/schema/hash処理、候補実装・テスト・review・導入・保守費も増える。処理時間を含む純lifecycle savingは未計測で、修復により実運用の手動復旧が何回減るかもまだ観測していない。

取得コストもある。今回はmodule graphと既存fixtureを得るため固定ref archive約554.6 MBを取得し、code/schema/config/test/docs等647 filesのみ展開した。全本文を読解したわけではないが取得範囲は過大だった。継続ではこのcacheと対象file manifestを再利用し、同じarchive取得や全test反復を既定作業にしない。全role active time/token/料金はunknown。

本単位の停止条件は、限定patch、修復前失敗/修復後正常系、authority drift等の負例、関連回帰、再現入力/限界をreview可能に揃えること。全architectureやfull shadow executionを作ることではない。修復候補の独立非著者review、production側への提案/適用・採用は未実施。4-C/5-Bの一体委任許可は再利用していない。

次の入口はこの候補の限定reviewと既存Shared Core保守への還元判断。再開時はcurrent Shared Coreが既に修復済みなら差分評価へ切り替え、重複実装しない。独立agentを起動する場合はこの具体物について別途明示許可が必要。production変更やPR/Issueへの投稿も本taskでは未許可である。reader review計画の作り直し、conditional 5-C、renderer等の保留課題の再開を次の既定作業にしない。

[継続handoff](../handoff/astra-phase-5-continuation.md)。通常Git Pull/Push/最終commitはHuman。
