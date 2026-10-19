# R1 統合契約分析 — checked editorial admission / full-promotion / normal lifecycle return

> Worker（author/analysis）作成。root architecture reviewerの判断入力。独立reviewではない。runtime実装/test実行なし。復元DB `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60`（detached409/tree8ce+final21 21/21）のactual-source読解に基づく。旧分析の孫引きではない。
> 工具差異: `apply_patch` 不在のため `Write` で新規作成。

## 0. 結論先行（提案決定）

**bounded coherent extension（checked editorial admission最小一貫拡張）を条件付き選択し、R2 vertical implementation taskとして具体化する。現状維持（gap残置）とbroad authority置換（汎用権限再設計）は不採用。helper-only slice（新helper追加で終わり）は出口にしない。**

- 閉じる述語: reason/record-State binding、versioned reviewed target/live outputs、両receipt/Gate/manuscript/public validators、既存review責任/path同一性、install所有/window/失敗復旧、既存未採用Candidate衝突、postinstall通常QA/Candidate/Preview/Freeze/Releaseを**同一操作の契約**にする。
- 偽装禁止: `REVIEWED_CORE_CHANGE` の流用、State reset、accepted Draft書換え、同一SHAによるreview path付替え、generic pending bypass、未検証low-level成功の使用は不可。Candidate/semantic/publication/Human承認は区別する。
- DM022はmaterialだが別stage/別権限。共通原則（SHA-bound・append-only lineage・fail-closed・deterministic revalidation）を流用し、repairはbatch化しない。intake訂正（§6）を反映する。
- 次taskは下記§7の具体的API/schema/path変更面・fixture authority生成順・oracle・回帰とする。key述語を次分析へ丸投げしない。R2で通しの成功/負例/失敗時を実accepted合成fixtureで示し、fresh作者別設計reviewを経て判断する。

## 1. actual-sourceで確認した事実（復元DB基準）

### 1.1 lifecycle/Stateの硬直性

- `survey_production_v2.py:32-44 LIFECYCLE` は `ISSUE_INITIALIZED→…→EVIDENCE_REVIEWED→SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED→DRAFT_COMPLETE→VALIDATED_DRAFT→RELEASE_CANDIDATE→FROZEN→RELEASED`。`transition_state:935-985` は `target==current+1` のみ許可し、同State/後退を `non-monotonic transition refused` で拒否する。checkpoint `passed` とprovenanceのexact一致を要求する。**同State supersessionは現codeに存在しない。** これはDM021 post-VALIDATEDとDM022 pre-Architectureの共通の硬直点である。
- `survey_agent_control_v2.py:45 REVALIDATION_REASON_CLASSES={"REVIEWED_CORE_CHANGE"}` のみ。`_collect_pending_rows:711-743` は `state.checkpoint_provenance.validation` の `record["artifacts"]` 7行のみ走査し（`survey_agent_control_v2.py:726`）、reader JSON不在は自動でnoncanonical拒否にならない。既存revalidationはchanged surface rowsを `REVIEWED_CORE_CHANGE` で通すが、これはtruthful editorial authorityではない（P3S contract§2と一致。復元DBで再確認）。
- `survey_agent_control_v2.py:1900-1994` のpublication revalidation書込みは `manuscript+quality_bundle+semantic+visual+Reader-Surface Gate` のfresh QAを要求し、`publication_revalidation_provenance={path,sha256}` でStateを更新する（temp+replace・事前basis再検・rollback保存。`:2013-2098`）。reasonは `reason_class/reason` をrecordに持つが、現enumはCORE_CHANGEのみでeditorial reasonを表現できない。**reason/record-State bindingの欠落がここにある。**

### 1.2 P1/P2R/P2V/P3Sの到達点と境界

- P1 `survey_editorial_correction_proposal_v2.py:1-15` はread-only・no approval/no reason enum/no State adoptionを宣言し、`basis`（original checkpoint/active-before/State/reader/receipt/control）と `proposed`（authoring/reader/canonical digest/change_description）をmemory内で再導出する。`_compare_supplied_to_rederived:1710-1737` でBASIS_MISMATCH/PROPOSED_MISMATCHを厳密に検査する。**proposalはversioned reviewed targetの前半（basis+proposed）を既に持つが、reason enumとlive installを持たない。**
- P2R `capture_retention:851/verify_retention:1731` は `COPY_BEFORE_REPLACEMENT→retained_dest` と `KEEP_IMMUTABLE` の二政策でretained権威を作る。P3S verifierはこれを `COPY→State.profile→KEEP` で辿る（P3S assessment§1）。**retained権威はあるがcurrent eligibilityではない。**
- P2V `observe_current_authority:101` は `RESULT_SCOPE_BOUND=CURRENT_BASIS_OBSERVED_SCOPE_BOUND` を返し、live State/planとretained manifestのcross-binding（STATE_REF/BASIS/RETENTION/SCOPE_DRIFT検査）+ optional scope→FULL receipt再検を行う。writerはこれをinvocation内2回要求する。**live/current観測はあるがlive書換え権限（bearer）はない。**
- P3S `materialize_staged_source/verify_staged_source` はproposal-owned `staged-source/{main.tex,references.bib,jgaisurvey.sty,staged-source-manifest.json}` のみをone-shotで所有し、manifest-last・所有4file・固定37 replay deps・TOOL_DRIFTを強制する。schemaは `EDITORIAL_STAGED_SOURCE_V1/STAGED_ONLY/2.0-rc1`（実読157行）。**staged事実はあるがlive publicationとStateはhealthy/unchangedのまま。install/receipt/Gate/Candidate/Preview/Freeze/Releaseは未接続。**

### 1.3 両receipt/Gate/manuscript/public validatorsの所在

- Longform receipt: `survey_longform_generated_v2.py:606 build_receipt/665 validate_receipt`。public replayはpersisted semantic reviewをGateと独立にreloadし（`:685-697`）、reviewed reader input mismatch・accepted authority drift・canonical FILE-byte/path（`:723-732`）を検査する。`verify_tool_basis/verify_closure_at_commit:519-605` でrenderer commitのancestor性とclosureをpinする。
- Weekly側は `survey_weekly_derivation_v2.py` + `survey_reader_surface_gate_v2.py`（P3Sで `render_main/render_bibliography` として再利用）。Gateは `validate_reader_surface_gate:1931`（agent_control呼出し）でmanuscript path/State/issue/profileをbindする。
- manuscript: `reader.validate_manuscript_manifest:1904`、quality bundle: `quality.validate_bundle:1911`、semantic/visual: `reader.validate_review_record:1921/1925`（SEMANTIC_EDITORIAL/VISUAL kind固定）。**checked admissionはこれらをlive outputsに対して再実行しなければpublic readbackにならない。staged replayだけでは不足。**

### 1.4 既存review責任/path同一性

- Human Gate: `survey_human_gate_v2.py:605 record_architecture_approval/660 record_publication_preview_approval` がexact reviewed bytesに対するAPPROVED/REQUEST_CHANGESを記録し、`:1103 invalidate_pending_gate` はpending Gateのみ無効化でき、Architectureはpassed checkpoint必須（`:1132-1133`）、PUBLICATION_PREVIEWはactive Architecture承認を跨げない（`:1134-1135`）。review indexにrecordsがあれば無効化不可（`:1142-1144`）。**review pathの同一SHA付替えはここで禁止される。accepted Draftの上書きは不可。**
- scope review: P1 `_validate_scope` をP3Sがnarrow Session adapterで再利用する（S1）。semantic/visualは上記kind固定。**既存reviewのpathを同一SHAで付け替える設計は採らない。staged manifestの `scope_review_ref` はpath+SHAのpinであり、review bytesの再解釈ではない。**

### 1.5 install所有/window/失敗復旧の現状

- Freeze pair: `survey_publication_v2.py:171 _prepare_freeze_inputs/323 _preflight_freeze_pair/627 _install_freeze_pair` + `survey_profiled_freeze_v2.py:50 build_profiled_freeze`。Candidate path+approval pathからfreeze-record/manifestをpreflight→installする。DM001/019でexact approved Candidate path/hash・tag内部導出・wrapper State/gate guards・exclusive writer/snapshot・bounded partial/close/driftが実装済み（AGENTSのDM001/019 bounded repairを再利用）。
- revalidation State書込みは上記temp+replace・rollback保存・unknown disposition時のmanual recovery要求（`:2041-2098`）。**live TeX installには同等の所有/window/失敗復旧がない。P3Sの所有4file・manifest-last・partial保存はstagedのみでliveに適用されない。**
- install windowは「P2V SCOPE_BOUNDのfresh2回+stable-fact比較の間、live State/publication unchanged」の外にない。live-invalid interval（採用先行・readback後回し）を消すには、versioned pre-TeX target + checked transition + public post-adoption readbackを同一操作にする必要がある（P3S contract§2）。

### 1.6 未採用Candidate衝突

- `candidate_selection_gate.py:57 suggested_role/100 HOLD-promotion禁止/123 validate` は `HOLD/INSPECT_MORE→HOLD_OUT` を強制し、HOLDのSELECTED昇格を拒否する。DM022 W40の `29 MATERIAL/4 HOLD/2 CONTEXT` とr10 `28 SELECTED`、Plan B `31 MATERIAL/30 SELECTED(proposed only)` はこのruleの下にある。
- DM021 admissionのlive install先（`survey_root/main.tex` 等のcanonical edition publication path。longform receipt `:723-730` のexpected path参照）は、既存未採用Candidate（FROZEN前のCandidate matrix/records）が存在すれば衝突する。**既存Candidateを黙って上書きせず、exact path+hash衝突検査と明示拒否/復旧が必要。** 現P3Sはlive survey_rootに書かないため衝突検査がない。

### 1.7 postinstall通常QA/Candidate/Preview/Freeze/Release

- 通常経路は `VALIDATED_DRAFT→RELEASE_CANDIDATE→FROZEN→RELEASED` に `publication_preview/freeze/release` checkpointsとHuman Gates（architecture approved→publication pending→…）を伴う。`_pending_conditions:700-708` はpending publicationがdownstream checkpoint/exceptionを禁じる。`built_checked_pending_publication_basis:784-808` はfresh contextをState/checkpoint/publication filesから作る。
- staged生成後に使うadmission先が未定ではbuild/writerを増やしても運用にならない（roadmap§6）。**R2はreview済み変更→checked install/State→public readback→fresh Candidate→通常Preview/Freeze/Release admissionまで接続しなければverticalではない。**

## 2. 未解決述語の同時解決（R1出口の定義）

下記を別helperに分散させず、同一操作 `admit_checked_editorial` の契約として閉じる:

1. **reason/record-State binding**: 新 `reason_class=EDITORIAL_CORRECTION`（仮称。`REVIEWED_CORE_CHANGE` と別enum）を導入し、`reason` 非空・`change_description` 一致・`proposal_id/issue/profile` 一致をrecordにbindし、Stateの `publication_revalidation_provenance` とは別の `editorial_admission_provenance={path,sha256}`（仮称）でStateにpinする。State resetなし、accepted Draft mutateなし。recordはappend-only（sequence衝突拒否。既存 `sequence+1/record_path.exists→collision` と同則）。
2. **versioned reviewed target/live outputs**: target=`proposal_ref+retention_manifest_ref+scope_review_ref+staged_manifest_ref（digest含む）+renderer commit+contract_identity+code_deps37`、live=`installed main/bib/styのpath/SHA/bytes + 更新後reader input/receipt` を同一recordにbindする。targetのdigestはP3S manifest_digest、liveはinstall直後のreadback bytes（read-after-write blessing禁止。expected bytesとの比較）。
3. **両receipt/Gate/manuscript/public validators**: live outputsに対して `Longform validate_receipt`（またはWeekly対応）+ `validate_reader_surface_gate` + `validate_manuscript_manifest` + `validate_bundle` + `validate_review_record(SEMANTIC/VISUAL)` を再実行し、全PASSをrecordにbindする。DIRECT_PRIMARY fallbackでgenerated correction契約を回避しない。pre-TeX scope reviewは重複semantic reviewを省く根拠にはなるが、live-invalid intervalの免除にはならない。
4. **既存review責任/path同一性**: scopeはnarrow Session adapterで実P1 `_validate_scope` をretained bytesで再実行し、semantic/visual/Humanは既存kind/pathの再検証のみで付替えなし。`producer_head` はprovenanceのみでHEAD一致を要求しない（P3S S5のartifact-only HEAD互換を継承）。
5. **install所有/window/失敗復旧**: live `survey_root` の3fileのみをone-shotで所有し、preflight（4 outputs/parent/schema/before bytes）→exclusive `O_CREAT|O_EXCL|O_NOFOLLOW`+fd/entry/ancestor bind→bytes→fsync/close/readback→manifest/record-lastの順序をliveに適用する。P2V×2のstable-fact比較をinstall前後に要求し、second mapのfull equalityは要求しない（P3S§5.6と同則）。失敗時はowned partials保存・phase/per-file/primary+secondary disposition・live originalsのmanual recovery要求。truncate/overwrite/rollback/cleanupなし。No global CAS/crash-atomicityの限定を継承する。
6. **未採用Candidate衝突**: install前に既存Candidate path/hashをexact検査し、衝突時は `CANDIDATE_COLLISION` で拒否する。衝突解消はowner decisionの明示操作のみ（自動上書き・黙示mergeなし）。existing Candidateのprovenanceは保持する。
7. **postinstall通常復帰**: install+public readback成功後にfresh Candidate生成→通常 `RELEASE_CANDIDATE→FROZEN→RELEASED` のPreview/Freeze/Release admissionへ接続する。既存 `build_profiled_freeze/_preflight/_install` と `survey_release_checkpoint/survey_stage_validation` を再利用し、新Human Gateは作らない。既存RELEASEDを再承認扱いにしない。

## 3. 3案比較（除去作業/追加コスト/failure cost基準。path数上限なし）

### 案A: 現状維持（gap残置。不採用）

- 除去作業ゼロ、追加コストゼロに見えるが、staged生成の後に使うadmission先が未定のまま残る。build/writerを増やしても運用にならない（roadmap§6）。訂正は通常publicationへ採用できず、二重維持（旧通常作業+未接続helper）が残る。総lifecycle workは減らない。DM022のaccepted-upstream訂正不能と同型の閉塞をDM021側に残す。**便益が「helperが増えた」だけなら追加投資を止める（roadmap§5）に反する。**

### 案B: bounded coherent extension（条件付き選択。推奨）

- 追加: 1 module（`survey_editorial_admission_v2.py` 仮称。`admit_checked_editorial` + `verify_editorial_admission` の2 API）+ 1 schema（`editorial-admission-record-v2`）+ 1 test拡張（existing testの修正ではなく新behavioral tests）。既存P1/P2R/P2V/P3S/receipt/Gate/controller/config/CLIの変更はblocker扱いでimplicit permissionにしない（P3S§7と同則）。route固有はLongform/Weeklyの差を具体化するが、共通所有/window/衝突/失敗復旧は共通実装とする。
- 除去: 旧 `REVIEWED_CORE_CHANGE` によるeditorial偽装経路を明示拒否に変える（code削除ではなくpolicy拒否。既存revalidationのhealthy rowsは保持）。重複semantic reviewのうちversioned pre-TeX targetで不要な部分を省く（P3S contract§2のversioned pre-TeX targetの趣旨）。未接続helperの追加で終わらせず、install→readback→Candidate→Freeze/Releaseを接続することで旧手作業（手書きstatus/別helper往復）を外す。
- failure cost: install windowの所有違反・衝突・partialはfail-closedで残るが、manual recovery手順が明示される。TOOL_DRIFT・SCOPE_BOUND・Candidate衝突の拒否は早期に失敗し、live-invalid intervalを作らない。定性的コストは「中〜大のうち小さい側」（R1 roadmapのR2見積り「大」の下限。P3S 3A/0Mと同規模+既存validator再利用のため、新規推論は最小）。
- 残る限定: 実PDF build・真正review/Human判断・全profile・migration・net savingsはR3/R4で扱う。no-CAS/crash/no-drift・synthetic≠genuineは継承する。

### 案C: broader authority replacement（汎用権限再設計。不採用）

- 例: `transition_state` の単調前進を緩和する汎用same-State書換え、Human Gateの汎用無効化、Candidate-as-publisher、pending bypassの一般化。
- 除去作業は大きい（frozen validator・State history・checkpoint provenance・review indexの再設計）が、DM021のpost-VALIDATEDとDM022のpre-Architectureのstage固有条件（review種別・受理表現・Human Gate位置・old→new lineage対象）を混同し、frozen authorityのspoiling・Gate偽装・accepted authorityのsilent editを招く。Summaryが求めるtightly gated append-only supersession（DM022 intake§§88-101）は別Core taskで扱うべきであり、edition production中の緩和は禁止されている。**必要閉包を超える権限拡大は、未知コストをゼロにしない（roadmap mission）に反する。**

## 4. 偽装禁止の具体則（actual-source根拠）

- `REVIEWED_CORE_CHANGE` 再利用禁止: `REVALIDATION_REASON_CLASSES` は現1enumのみ。editorialは新enum+non-empty reason+change_description一致を要求し、旧enumでの通過を `REASON_CLASS_MISMATCH` で拒否する。既存healthy revalidationのPASSを流用しない。
- State reset禁止: `transition_state` の `current+1` 以外を呼ばない。Stateの `lifecycle_state/history/machine_checkpoints/human_gates` を巻き戻さない。admissionは `VALIDATED_DRAFT` のまま `editorial_admission_provenance` を追加するのみで、lifecycle前進は通常Freeze/Releaseに委ねる。
- accepted Draft mutate禁止: `initialize:1002` のdestructive refusalと同則で、accepted Draft bytes（validation checkpoint artifacts・accepted_refs・archive）を上書きしない。proposedは `PROPOSED_ARCHIVE_DRIFT/PROFILE_DRIFT`（P1 `:1559-1565`）で拒否される。
- equalSHA rebind禁止: Human Gateのcanonical approval bytes照合（`:864`）とreview pathのexact bindを維持し、同一SHAの別pathへの付け替えを `PATH_IDENTITY_MISMATCH` で拒否する。`producer_head` のprovenanceのみ使用はP3S継承。
- generic pending bypass禁止: `_collect_pending_rows` の7行走査をeditorialの免除根拠にしない。staged 4fileはpending rows外のため、別途versioned target+live readbackを要求する。ordinary-without-block scopeの除去事例（P3S O7）はadmissionでは拒否に変える。
- unchecked low-level成功禁止: `validate-state` のexit0・GateのPASS・file存在のみでadmission成功にしない。full `manuscript+bundle+semantic+visual+Gate+receipt` のfresh QAとowned install/readback/Candidate衝突/partial分類を全て要求する。
- 役割分離: Candidate（SHA-bound selection decision）・semantic（persisted reviewの独立reload）・publication（manuscript/bundle/Gate）・Human（exact bytes承認/Preview）は別主体。typed approvalはC1 path+hash選択に留め、FROZEN admissionと混同しない（DM003-W1 bounded repairを再利用）。

## 5. DM022適用性（pre-Architecture frozen source。実装せず権限混同せず。新intake訂正必須）

DM022 intake（`notes/rephase-1-roadmap-replan-20261019/dm022-intake/`）は `c8d0ecc/blob0a0fe3eb/Issue562 open` に固定された3 GETであり、Production code/main一般追従・rebaselineではない。Worker初稿の「reconstruct影響なし」は訂正で撤回済み（roadmap§3）。以下を intake訂正（`intake-and-impact.md` §§168-201）に従い反映する。**ロードマップはDM022をmaterialとして保持し、「no impact」にしない。**

- DM022の正確な問題: `CV2-DM-022 No lawful pre-Architecture same-State supersession of accepted Evidence/Views/Materiality`（`OPEN_CORE`）。W40 `EVIDENCE_REVIEWED` で37 Discovery/37 Screening/35 Cards/35 Views/37-row Materiality/LIMITED Completenessを受理後、2 HOLDのissuer-authored HF組織記事（host JSON-LD `2026-10-02T15:19/04:01Z`。hosted article eventでありweight/upload/再現/first-availabilityの証明ではない。HTML bytes未archive）が判明。Sol Plan Bはprovisional方向のみでcanonical Core Selection/Human Gateではない。frozen pipelineは `transition_state` 単調前進・`invalidate_pending_gate` のpending+Architecture条件・Candidate `HOLD→SELECTED` 拒否・SHA-bound checkpoint provenance・fixed history shapeによりsame-State置換を拒否する（intake§§50-59）。authoritative viewsは `29 MATERIAL/4 HOLD/2 CONTEXT`、r10 `28 SELECTED` のまま。Plan B `31 MATERIAL/30 SELECTED` はproposed only。edition-local continuityはCore-valid 28保持+reviewer-preview HOLD rationale修正+2 non-canonical supplements（NOT Core SELECTED/Architecture/publication appendices）に留まる。
- 共通原則（流用可）: SHA-bound authority・append-only lineage（old bytes保存+old→new SHA記録）・fail-closed refusal（stale HEAD/unsupported clock/role/ID mismatch/non-idempotent replay/unapproved review/post-Architecture editで閉じる）・deterministic revalidation（Evidence/Card/View/Materiality/Completeness再検証+Matrix/Selection preview強制）・original Discovery/Screening INSPECT保持（互換時のみ）・canonical checkpoint path/history schema/frozen SHA bindingの明示調整。no direct overwrite/manual rollback/forged REQUEST_CHANGES。
- stage固有差（混同禁止）: DM022は `EVIDENCE_REVIEWED` pre-Architecture・Selection前・両Human Gates前で、対象はEvidence/Cards/Views/Materiality/Completeness、allowlistはaffected-ID、決定はSol、HEAD/Tree/work HEAD guards付き。DM021は `VALIDATED_DRAFT` post-review・Architecture approved/publication pendingで、対象はreader bytes→staged TeX→live survey_root、reviewはscope+semantic/visual+Gate+Human Preview、installはTeX 3file所有・Candidate衝突・Freeze/Release復帰。stage・review・受理権限は別。repair batch化なし。Summary§8はproduction報告のrestart processであり、Human-authorized reconstruction planningの上位禁止ではない。継続はdelegatedでper-analysis承認gateを新設しない。
- 「Authoritative」の限定: 3 GETはcapture fidelity（exact Summary bytes+Issue state/text）のみ証明し、W40技術再現（host timestamps/authority counts/Sol実体/r12 outcome）を証明しない。`sources/2026-W40/execution/…` 7件・Sol r11実体・r12 outcome・#515・W41 Suggestion・`83f581eb` deltaはsecondary未読として扱い、authorityをadoptしない。r12 outcomeと `sources/2026-W40/…` は新explicit authorizationなしにfetchしない（pinned `c8d0ecc` をstanding refreshにしない）。
- R3までのDM022 disposition: 固定ソースで適用性と必要修復/既存代替の実効性を判断する（roadmap§3）。本R1ではDM021 admission契約に共通原則を反映し、DM022 repair自体は実装しない。

## 6.  scrutinized alternatives（旧案の再評価。実source基準）

- 「409をWeekly-first adoption候補に」: 不採用。409自身の実build/統合受入れ未証明であり、overlay21を捨てるとpost-review訂正gapが残り、必要Specialを外した二重維持になる（roadmap§2）。
- 「LF2I10+DM02111」: 分類誤り。LF2I時点9file、現21は累積。R11 static21を用いる（roadmap README採否）。
- 「新read-only部品をもう一つ」: 出口ではない（roadmap§6）。P3Sはstaged事実まででadmission先がない。本R1はhelper追加で閉じず、install→readback→Candidate→Freeze/Releaseを同一操作にする。
- 「reader-JSON-only staging」: P3S contractで不採用（P1機能重複）。staged TeX/Bib/styleのexact replayable setが必要。
- 「10-file変更はunreviewable」: 恣意的path上限を課さない。deferralはunresolved predicatesに従う（P3S contract§2）。R2の変更面はblockerとscope決定で決める。
- 「DM022無関係/分析禁止」: 誤りとして撤回済み。material入力として境界明示するが、stage権限は混同しない。
- 「3modifiedを読まずpin/patchで十分」: 不採用。統合設計には実base callerとfinal21全体が必要。本R1は復元後actual-sourceを使用した。

## 7. 次vertical implementation task（R2。具体形。key述語先送りなし）

### 7.1 変更面（path数上限なし。blockerはexactに）

- 新 `scripts/survey_editorial_admission_v2.py`（仮称）:
  - `admit_checked_editorial(root, state_path, staged_manifest_path, retention_manifest_path, proposal_path, scope_review_path, candidate_path=None, ...) -> result`
    - 内部で `verify_staged_source`（P3S）+ `verify_retention`（P2R）+ `observe_current_authority(scope)`（P2V fresh）を同一invocationで再実行し、refs/digests/stable-factsを照合する。earlier dict/enum/caller verified_setの持込み不可。P1 public validateはretention後不呼び出し（P3S継承）。
    - `reason_class=EDITORIAL_CORRECTION` を要求し、`reason` 非空・`change_description` 一致・`proposal_id/issue/profile/route` 一致を検査する。`REVIEWED_CORE_CHANGE` での通過を拒否する。
    - live `survey_root/{main.tex,references.bib,jgaisurvey.sty}`（canonical edition publication path。receipt `:723-730` 準拠）のbefore bytesをpinし、既存Candidate path/hash衝突をexact検査する。衝突時は `CANDIDATE_COLLISION` で拒否する。
    - live 3fileをexclusive所有（preflight→dirfd/no-follow→short-write handling→fsync/close/readback→record-last）。P3S§5のstaged順序をliveに適用し、失敗partials保存・primary+secondary disposition・manual recovery要求を継承する。
    - install直後に `validate_receipt+validate_reader_surface_gate+validate_manuscript_manifest+validate_bundle+validate_review_record×2` をlive outputsに対してfresh実行し、全PASSをrecordにbindする。DIRECT_PRIMARY回避禁止。
    - admission recordを `publication/v2/editorial-admission-{sequence}.json`（仮称。canonical pathは実装前に固定）にsequence+1でappend-only作成し、Stateに `editorial_admission_provenance={path,sha256}` をtemp+replaceでpinする。sequence衝突は拒否する。lifecycle前進なし。
  - `verify_editorial_admission(root, staged_manifest_path, admission_record_path) -> result`
    - retained/staged/admissionのconsistency+deterministic replay（P3S verifier拡張）。current State/P2V/HEAD一致を要求しない。TOOL_DRIFTはreplay前に拒否する。
- 新 `schemas/editorial-admission-record-v2.schema.json`（仮称）:
  - `schema_version/ kind=EDITORIAL_ADMISSION_V1 / status=ADMITTED_ONLY`（STAGED_ONLYと別。LEGACY receipt/Gateと混同しない）、`reason_class=EDITORIAL_CORRECTION` enum固定、strict `additionalProperties:false`、duplicate-key拒否、canonical serialization+self-digest（P3S manifestと同則）。
  - 必須binds: `staged_manifest_ref/proposal_ref/retention_manifest_ref/scope_review_ref`（path+SHA）、`issue/research/publication labels+route`、`before_live_refs`（3fileのold path/SHA/bytes）、`after_live_refs`（3fileのnew path/SHA/bytes）、`receipt_refs`（receipt/Gate/manuscript/bundle/semantic/visualのpath+SHA）、`old_to_new_lineage`（old live SHA→new live SHA+staged digest）、`candidate_collision_check`（checked path+hash+verdict）、`install_window`（P2V×2 HEADs+stable-facts+owned identities）、`code_deps`（P3S 37+admission自体。sorted unique exact一致）、`producer_head`（provenanceのみ）。
- 既存変更は原則なし。P1/P2R/P2V/receipt/Gate/schemaの変更が必要ならexact blockerとして返し、implicit permissionにしない。既存 `survey_agent_control/publication/production/human_gate` の呼出しはadmissionからの利用のみで書換えなし。
- testは新behavioral testsのみ（old13+1/25/26のtransferなし、decorative full-suiteなし）。Longform-primary/Weekly-envelope/R1のreal `P1 prepare/stage→P2R capture→genuine scope→P2V→P3S→admission` を通す。prose/envelope editsはexpected changed sourceを要求し、old live copyを許さない。

### 7.2 実fixtureのauthority生成順（source-committed fixture条件）

- fixture recipe（authoring inputs・scope review・archived refs・contract identity）は**implementation codeとは別のsource-committed fixture recipe**として先にcommitされ、authority（admission成功）の前に独立に存在しなければならない。uncommitted review worktreeをpositive committed renderer basisにしない（P3S§7と同則）。
- 順序: `fixture recipe commit→P1 proposal→P2R capture→scope→P2V SCOPE_BOUND→P3S staged→admission install→public readback→fresh Candidate→Preview/Freeze/Release admission`。各stepのrefsはhash-boundで持越し、second observationのmapを新baselineにしない。

### 7.3 oracle（成功/負例/失敗時。抜粋。実装前に固定）

- 成功: Longform+Weekly+R1のadmission成功、live originals/State/retention unchanged以外のowned deltaのみ、exact 3file window、P1 destination-conflict継続、P2R/P2V共存、artifact-only HEAD互換、TOOL_DRIFT到達検査。
- 負例: reason空/`REVIEWED_CORE_CHANGE` 流用・scope ordinary-no-block・path/ref/schema/output/inventory tamper・malformed/stale-upstream・no-read alias/FIFO・drift before write/after helper/self-readback・root/file ownership replace・Candidate衝突・sequence衝突・DIRECT_PRIMARY回避は全て拒否コードで失敗する。
- 失敗時: short/zero/fsync/close/manifest write faultsで `INCOMPLETE/INDETERMINATE` 分類、owned partialsのexact範囲、primary保存secondary attach、live originals unchanged、manual recovery要求。complete valid bytesが残ってもinvocation成功にしない（P3S§5継承）。fault-present no-writeはtest snapshot+owned diagnosticsで証明し、module FINALと混同しない（supplement§5）。
- 回帰（必須）: DM001/019 Freeze pair（exact Candidate path/hash・exclusive writer・snapshot）、W1 approved-only Human/checkpoint equality（4行。healthy pending valid・stage backstop保持）、DM004 `validate-state` containment（read-only・JSON/exit・workflow呼出し不変）、LF-1/LF-2Iのscoped no-write・pure/schema/helper分離、P1/P2R/P2Vの既存PASSのpin-bound維持（transferなし）。新admissionが既存revalidationのhealthy rowsを壊さないことを示す。

### 7.4 却下時のreasoned alternative（実装不可能な場合の出口）

- もしlive installのowned windowが既存Freeze pairと両立しない、または両receipt/Gateのlive再実行がcanonical path制約で不能なら、「R2実装不可。残るblockerは○○のexact interface差異であり、代案は××（例: live installを別issueに分離するが、その場合はWeekly viabilityを失うため全体完成保留）」を根拠付き決定とし、次の分析へ丸投げしない。本R1はその判断点を残すためにある（roadmap R1出口）。

## 8. 技術/publication/migration limitsと定性的コスト（ fabricated runtime proofなし）

- 技術: no global CAS/crash-atomicity/power-loss・continuous no-driftなし・blind mkdir→earliest windowあり・tripwire≠hotpatch・sampled child-rawのみ・exact-run toolingのみ。missing26309/unbundled runtime残る。build/rendered受入れ・all-profile・migration互換・性能削減はR3/R4で扱う。test runtime/countの数値約束なし。
- publication: synthetic reviews/fixturesはgenuine approvalsではない。staged `VERIFIED`・admission `ADMITTED_ONLY` はbyte-consistency+replayのみで、publication admission・Gate/Candidate/Preview・rendered QA・Human Gateの代用にならない。既存RELEASEDを再承認扱いにしない。必要Special（Thematic/Longform/Retrospective/manual/direct-primary/upstream Profile）の要否は実使用とcallerで明示決定し、unsupportedがあれば全体完成保留（roadmap§1）。
- migration: State history/schema・checkpoint path binding・frozen SHA bindingの変更はR4移行base比較（Human許可後）で扱う。旧版履歴/除去対象/切戻し/採用手順はR4で揃える。現時点でProduction mutation/採用は未許可（Human-owned）。
- 定性的コスト: R2はP3S 3A/0Mと同規模+既存validator再利用のため「大の下限」。fixture recipeの独立commit・所有/window/衝突・両receipt再実行・fresh Candidate→Freeze/Release接続が主cost。R3（実TeX build・disposable build→transfer→strict admission・品質review）が現在最大の不確実性。暦日見積りはR1変更面確定後・R3環境確認後に更新する（roadmap§4）。未知はunknownとし、必要独立reviewを重複費として削らない。

## 9. rootへの検証依頼（fresh作者別設計reviewへ）

- 本分析の§§1–2（actual-source事実・述語定義）、§3（3案比較）、§5（DM022境界・intake訂正）、§7（R2具体形・oracle・回帰）の過不足を検証されたい。特に `EDITORIAL_CORRECTION` enum新設の要否、Stateの `editorial_admission_provenance` 追加の可否、live 3file所有とFreeze pairの両立、Candidate衝突拒否のowner decision範囲、Weekly/Longformのroute差の具体化漏れを指摘されたい。
- 設計PASSはimplementation/application acceptanceではない。R2実装選択はAstra return後に行い、本R1のCommit Pointで停止する。Workerは自身の独立PASSを宣言しない。
