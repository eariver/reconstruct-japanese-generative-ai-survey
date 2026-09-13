# Phase 5 — review計画とruntime優先順位のEvidence

日付: 2026-09-14 JST。[現在判断](../../outputs/astra-phase-5-review-plan-and-runtime-priority.md)。旧conditional 5-C A/Bとは別の継続調査であり、review run/独立agent/実装修復を実行した記録ではない。

## 入力の範囲

- [observation](observation.json): reconstruct `0118a7c2…` local/remote一致・開始clean。Humanはcommit titleの5-C表記をphase authorityにしないと明示。前回はpublication review boundary investigation。
- [inputs](inputs.json): 固定ref/path/Git blob/raw SHA/bytes。rawはignored `.phase-5-inputs/<ref>/<path>`。必要時のみ既存`notes/phase-5b/capture.py`をimportしDESTを本directoryへ変更して復元する。`sys.dont_write_bytecode=True`で過去directoryに補助cacheを作らない。旧Evidenceを上書きしない。
- [main差分概要](main-diff.json) / [main head](main-head.json): 旧mainからのcompareはW34 historyのmergeを含み112 commits、300 filesの上限へ到達した。網羅的な差分監査には使わない。大きいpatch出力は調査上過剰だったので保存物を縮約し、旧execution指示を再読/実行する入口にしなかった。必要な4コード/contractの同一性は別にexact bytesで照合。
- [限定Issue検索](targeted-issue-index.json): freeze＋CORE_STAGE_CONTRACT、およびreader-surface gateだけ検索。0件を修復計画がどこにも無い証明にはしない。#400/#166の本文や過去repairは読まなかった。
- [Human carry-forward](human-carry-forward.json): #491の承認コメント5654102081のみ取得。Freeze worklogが参照し、実行計画の入口・W34再修復の可否を判断するため必要となった。

## Review計画の根拠

固定main `3e3eebe0cda3a32ac88ae764d279b37768f6bfca`のreader publication module、review contract、governance、Weekly publisherは前回main `74708eb2…`で取得したものとbyte-identical。新しいpre-TeX reader gateがこれらに既に実装されたとは言えない。

HumanコメントはW34をAPPROVEし、残るaudit語彙をnon-blocking carry-forwardとして受容。W35+の狭いreader-field lint、semantic review、位置付きfindings、下流開始前のfail-fastを推奨する。これは外部にあるproduction側Human意思の根拠であり、今回のreconstructからproduction変更する権限とは分ける。

[Weekly publisher](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_weekly_semantic_publication_v2.py#L285)の公開欄消費、[reader builder](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_reader_publication_v2.py#L433)の実PDF依存、[governance](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/docs/survey-production-core-v2-sol-luna-review-governance.md#L15)の独立責務を参照した。現最終reviewをpre-TeXのPASSとして偽装できない。別caller/Specialへのfield coverageは未検証。

## Freeze/Releaseの現在と不整合

W34 branch `3bad8a57…`はFROZEN。main `3e3eebe0…`はfrozen branchをPR #493で統合した`5c809346…`の後にRelease provenanceを記録しRELEASED / COMPLETE。branchの`stage:release`をcurrent mainへ流用しない。

[freeze audit](https://github.com/eariver/japanese-generative-ai-survey/blob/3bad8a57cf2b246c7f71cb749ba3105fa318b073/sources/2026-W34/publication/v2/freeze-audit-r3.json)は、Human approvalのStage解釈、Candidate authority喪失、visual artifact admissionの不整合に対する実行時調整を記録し、W33/SP001を先例とする。今回確認したのはW34とcurrent code。先行二号を独立再現してはいない。

[release recovery audit](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/sources/2026-W34/publication/v2/release-recovery-audit-r1.json)は、Release workflow `34769565399`で公開/exact asset確認は済んだが、checkpoint producerがCORE_STAGE_CONTRACTを欠きadvanceが失敗したと記録する。復旧後のState/Release record/checkpoint hashは[局所check](check.json)で照合した。公開Release metadataも[保存](public-release.json)し、server digest/sizeと現在repository PDFを比較。公開assetのdownloadやActions log全読解はしていない。

[runtime_witness.py](runtime_witness.py) / [結果](runtime-witness.json)は、current moduleをimport/実行せずASTから二つの実関数を抜き、早期guardだけを最小入力で実行する。productionのapproval/Stage schemaはrequired-field矛盾を静的確認する。全Core fixtureの成功/失敗と混同しない。

| Witness | 固定code位置 | 結果と範囲 |
|---|---|---|
| Human approvalとStage schema | [stage loader L124](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_stage_validation_v2.py#L124) | 全checkpoint pointerをStage schemaへ渡す。実approvalのrequired fields不足を確認。全loaderは未実行 |
| Freeze visual admission | [runtime L74](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_stage_validation_v2.py#L74) / [schema L222](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/schemas/stage-checkpoint-v2.schema.json#L222) | schemaの3 authority名を現_current_artifactsへ渡すとvisual-review-recordをunexpectedとして拒否。file validation到達前の実guard |
| Release missing review | [producer L66](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_release_checkpoint_v2.py#L66) / [controller L135](https://github.com/eariver/japanese-generative-ai-survey/blob/3e3eebe0cda3a32ac88ae764d279b37768f6bfca/scripts/survey_agent_control_v2.py#L135) | producerのliteral review IDを抽出しcontroller guardへ入力するとexactly one CORE_STAGE_CONTRACTで拒否。他のRelease品質/authority validationは実行せず |
| FROZEN未対応 | stage LOCAL_STAGES / REQUIRED_CURRENT | FROZENがないので既存compact validatorを呼ぶだけでは必須reportを作れない。external boundaryの規則が必要 |

これらは当該W34の正規復旧を否定する監査ではない。今後の通常経路から実行時調整/復旧仕事を除く修復対象を示す。guard削除、偽PASS、承認後の新VISUAL作成は解決に数えない。

## 確認限界とコスト

[check.py](check.py)は取得bytes、局所Freeze→Manifest→Release/Checkpoint、Candidate/approval/PDF、公開metadataのdigest、固定witness codeを照合。source TeX/visual実bytes/全依存閉包は今回再確認せず、visualの参照digestがapproved Candidateと一致する所まで。全State validator、PDF目視、全Core tests、外部Release実行/修復は未実施。

全role active time/token/費用、reader gate検出率、修復後の再発率/互換性/純削減はunknown。機械的producer/consumer不整合は実在しても、全lifecycle savingsはまだ計測していない。新しい実行時調整を別agent/Humanへ移すだけは改善ではない。

production GET以外の操作なし。新agentなし。通常Git Pull/Push/commitなし。今回の計画/witnessはreconstruct内のみ。次の入口は判断文書§5の限定修復候補で、reader計画の再作成やconditional 5-C試験ではない。
