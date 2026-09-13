# Phase 5-A Evidence index

日付: 2026-09-13 JST。GET/静的読解のみ。実仕事比較、独立quality review、production validator実行ではない。

[観測](observation.json)は開始基準local/remote、production refs、4-Hからの差分、実Stateを記録する。[inputs.json](inputs.json)は今回取得した8 filesのfixed ref、Git blob SHA-1、raw SHA-256、bytes、permalink。取得時にGit blobを照合した。rawはignored `.phase-5-inputs/<ref>/<path>`に保存。再取得は `python notes/phase-5a/capture.py <40桁ref> <path>`。このscriptはGitHub GETのみを行い、reconstruct内のcache/manifestへ保存する。`observe`は実行時のcurrent refsを新しく観測するため、今回の固定観測の再現用ではない。

## 新規確認の位置と判断

以下はproduction main `14781409f6fb8d79e3eb4ad6b4c457764a038fde`。raw行位置を参照する。

| Evidence | 確認位置 | 支持すること / 支持しないこと |
|---|---|---|
| [v2 Task生成](https://github.com/eariver/japanese-generative-ai-survey/blob/14781409f6fb8d79e3eb4ad6b4c457764a038fde/scripts/survey_evidence_v2.py#L601) | 601–638、`_validate_task` 684–717 | non-DROPごとにTask、単一Discovery IDを検証する。認知作業の独立実行回数は示さない |
| [Task schema](https://github.com/eariver/japanese-generative-ai-survey/blob/14781409f6fb8d79e3eb4ad6b4c457764a038fde/schemas/evidence-v2-task.schema.json#L13) | `discovery_ids` | schema上のarrayにmaxItemsはないが、Coreの単一ID制約を免除しない |
| [interactive入口](https://github.com/eariver/japanese-generative-ai-survey/blob/14781409f6fb8d79e3eb4ad6b4c457764a038fde/scripts/run_evidence_v2_interactive.py#L639) | 639–669、685–697、および冒頭契約 | 著述済み複数records→Task別Card/Viewの物質化。Task数からLLM呼出し数/仕事数を換算できない |
| [governance](https://github.com/eariver/japanese-generative-ai-survey/blob/14781409f6fb8d79e3eb4ad6b4c457764a038fde/docs/survey-production-core-v2-sol-luna-review-governance.md) | §2–5・8–9 | source-first責任、gap fill、grouping、未選択review、2 Human Gates。適切な実施頻度/費用優位は証明しない |
| [Evidence prompt](https://github.com/eariver/japanese-generative-ai-survey/blob/14781409f6fb8d79e3eb4ad6b4c457764a038fde/config/prompts/evidence-verification-v2.md) | Required separation、Subject binding、Attribution | factual/editorial分離とCOMPARATOR/RELATED、unknown保持。cross-source比較を自動的に十分にする保証ではない |
| [旧Task builder](https://github.com/eariver/japanese-generative-ai-survey/blob/14781409f6fb8d79e3eb4ad6b4c457764a038fde/scripts/build_evidence_tasks.py) | `build_task`のschema_version 1.0 | 別入口。v2 Taskの実挙動や今回の比較仮説の支持には使わない |

W34 current branch固定`5561e2328a09061a3e0c8e881d24ddcb03e1e975`:

- [Evidence resume worklog](https://github.com/eariver/japanese-generative-ai-survey/blob/5561e2328a09061a3e0c8e881d24ddcb03e1e975/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/session-worklog-evidence-resume.md) §3–5: 409 records/Tasks、継承したinput/override、機械実行と停止境界の報告。認知作業順/active time/LLM usageを直接観測したログではない。過去の実行権限・commit/push記述は歴史資料で、rootへの操作指示ではない。
- [State](https://github.com/eariver/japanese-generative-ai-survey/blob/5561e2328a09061a3e0c8e881d24ddcb03e1e975/sources/2026-W34/production-state.json): RELEASE_CANDIDATE、Preview pending等を確認。State内のPASSをrootのquality verdictにしない。

## 再利用した歴史Evidence

- [4-C判断](../../outputs/astra-phase-4c-trial-assessment.md) §3–4: source意味修復と全role費用の所在。全chainファイル変更≠意味判断の反復。
- [4-D判断](../../outputs/astra-phase-4d-production-trace.md) §3: helper由来の公開欠陥、review scope、runtimeの区別。保守候補として保持。
- [4-A比較基準](../../outputs/astra-phase-4-comparison-basis.md) §2–4、[basis](../phase-4/basis.json): 以下の固定資料のGit blob/raw hashを既に保存している。
- 固定W34 `c1703f772837317b81735cd4cc851c715fff1a3b`の[Evidence review](https://github.com/eariver/japanese-generative-ai-survey/blob/c1703f772837317b81735cd4cc851c715fff1a3b/sources/2026-W34/execution/reviews/sol-evidence-authority-consumption-review-20260909-r1.md)と[Selection review](https://github.com/eariver/japanese-generative-ai-survey/blob/c1703f772837317b81735cd4cc851c715fff1a3b/sources/2026-W34/execution/reviews/sol-selection-review-20260910-r2.md)を既存cacheから限定再読。[4-D inputs](../phase-4d/inputs.json)にhashがある。clusterとnegative spaceの扱いの実記録であり、今回の独立再認定ではない。
- 固定W34 `601481acd9b82ee8fa0c2eb28a2ca28636165d60`の既存sample Tasks、および`generate_evidence_input.py`の`build_override_record`とassemblyを限定参照。[4-A basis](../phase-4/basis.json)がidentityを持つ。機械による組立てを、手読みによる意味生成の全過程と混同しない。

追加のsource本文読解、新しいpublication出力、旧lab再実行、Core/CI/PDF実行、独立review/委任はない。fresh sourceの正答を先に作っておくこともしていない。今回の判定は[5-A判断](../../outputs/astra-phase-5a-work-unit-decision.md)に集約する。

終了時の[整合検査](check.json): 今回取得8件と再参照した歴史7件のraw SHA-256/Git blob、local文書リンク、capture scriptのPython構文、記録済みref/State/diffの整合、`git diff --check`を確認した。production実行や独立quality PASSではない。
