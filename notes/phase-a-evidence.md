# Phase A evidence ledger

調査日: 2026-09-09 JST。GitHub PR metadata は `gh pr view --json number,title,body,mergedAt`、remote branch SHA は read-only `gh api .../branches/...`、コードと edition artifact はローカル Git object を固定 SHA 指定で参照した。production checkout/refs を変える fetch/checkout はしていない。

## 固定点

| ID | Repository ref | 用途 |
|---|---|---|
| MAIN | `0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc` | #485 統合後の current Core |
| W34 | `993583e871bcbfea7bfe700fe5c6f2648e8887c0` | remote work branch と一致した現在の調査対象 |
| W34-R2 | `bc0921724c96f70d3f1adda4ece5b80ab5d5dd1d` | Human Architecture r2 の reviewed commit |

## 主な evidence → 結論

| 証拠 | 直接観測 | 診断・留保 |
|---|---|---|
| [Config](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/config/survey-production-v2.json) | 11 states、two gates、全 stage handoff false、stage artifacts と rollback boundaries | 既に compact/agent-first。全面 orchestration 発明は不要 |
| [Governance](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/docs/survey-production-core-v2-sol-luna-review-governance.md)、[PR #485](https://github.com/eariver/japanese-generative-ai-survey/pull/485) | source consumption と independent review、圧縮監査、full dossier を要求。PR は5 docs の変更 | 文書規則が加わったことを runtime hard enforcement と混同しない |
| [初回 worklog](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/execution/luna/w34-evidence-through-architecture-r1/session-worklog.md) | 80 PARTIAL / MATERIAL 1 / SELECTED 1、formal stage PASS | structured validity と研究品質の乖離 |
| [W34 execution index](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/execution/index.md) | 本文追加後の status 変化、旧 active set と sparse selection | この index の「current」は最新ではない。各 historical artifact の意味として読む |
| [現在 State](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/production-state.json) | CANDIDATES_NORMALIZED、次は Evidence | 古い index の Architecture ready を現在状態に採用しない |
| [C019 Evidence card](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/evidence/v2/accepted/377134b62c98bf0b65a7cf8cda1ef538eac0e2afcd7aa9aeeeda0f1d09493ada/results/task-089aea0f0b318bee50b2.json) | VERIFIED、汎用 claim、本文未取得 limitation、target UNRESOLVED | status と substantive consumption は異なる |
| [Supplement](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/execution/luna/w34-core-repair-r1/evidence-authority-supplement.json)、[C019 Raw](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/execution/luna/w34-evidence-authority-expansion-r2/raw/c019-mistral-agentic-search.html) | 263,578 bytes の本文。HTML を text 化し、候補固有の説明があることを確認 | vendor claims の真偽や全 benchmark の妥当性を今回評価したのではない。card の「本文なし」を反証するサンプル |
| [過去 Architecture](https://github.com/eariver/japanese-generative-ai-survey/blob/bc0921724c96f70d3f1adda4ece5b80ab5d5dd1d/sources/2026-W34/architecture-v2.json) | target_pages 2 / max_pages 3 / package 1 | 二ページは planned architecture。公開済み PDF ではない |
| [Human r2 review](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/gates/reviews/architecture-r2.json) | REQUEST_CHANGES、ISSUE_INITIALIZED、coverage と本文消費の再調査要求 | 後の governance/research 修復の明示 authority |
| [Discovery r2 review](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/execution/reviews/sol-discovery-completeness-review-20260908-r2.md) | independent negative-space sweep、arXiv の full triage、score shortlist の非semantic性を認識 | Evidence repair だけでは coverage defect を直せない |
| [最新 Screening worklog](https://github.com/eariver/japanese-generative-ai-survey/blob/993583e871bcbfea7bfe700fe5c6f2648e8887c0/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/session-worklog-screening.md) | fresh screening 439 の処理 | 80件の過去 Evidence と409件の現在 non-DROPを同じ母集団として比較しない |
| [PR #484](https://github.com/eariver/japanese-generative-ai-survey/pull/484) | pre-Human invalidation と Supplement、exact historical evidence binding の保守修復 | operator の invalidation は Human REQUEST_CHANGES の偽装ではない |
| [PR #483](https://github.com/eariver/japanese-generative-ai-survey/pull/483) | 文書不一致・rollout 状態不一致で whole audit invalidation が記録 | status の多重記載と broad audit scope の増幅を示す。実働時間は不明 |
| [authority index](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/docs/survey-production-core-v2-authority.md)、[改善計画](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/docs/survey-production-core-v2-improvement-plan.md) | current 文言の中に過去 main / unmerged status が残る | stale prose を機械 truth にしない |
| [Core contract identity](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/scripts/survey_production_v2.py#L150)、[checkpoint consumer](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/scripts/survey_agent_control_v2.py#L680) | broad contract aggregate、exact execution identity、core stage report validation | 書類/契約/実装の provenance を保ったまま reuse key を分ける余地 |
| [Human Gate implementation](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/scripts/survey_human_gate_v2.py) | reachability、historical bytes、snapshots、依存 invalidation、cross-gate reopen | 既存安全機構をゼロから作り直さない |
| [PR #475](https://github.com/eariver/japanese-generative-ai-survey/pull/475) | SP001 の全ページ visual PASS 後に一段組回帰を Human が検出。mixed layout の明示 review を追加 | visual review record の存在は review quality ではない。今回 PDF 自体を独立評価したものではない |
| [PR #481](https://github.com/eariver/japanese-generative-ai-survey/pull/481)、[PR #482](https://github.com/eariver/japanese-generative-ai-survey/pull/482) | W33 11-page approved PDF、freeze alignment、release 後の checkpoint 修復 | exact bytes 防護は成功し、状態 adoption が失敗したと区別 |
| [PR #477](https://github.com/eariver/japanese-generative-ai-survey/pull/477)、[PR #478](https://github.com/eariver/japanese-generative-ai-survey/pull/478) | SP001 freeze と exact release、W33 と同じ missing core report | 同じ defect の二重 edition recovery |
| [release helper](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/scripts/survey_release_checkpoint_v2.py)、[workflow](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/.github/workflows/survey-production-v2-release.yml) | helper review は reconciliation のみ。workflow は helper を呼び consumer に進む | 静的に報告された mismatch を確認。release を起動したわけではない |
| [PR #398](https://github.com/eariver/japanese-generative-ai-survey/pull/398)、[PR #424](https://github.com/eariver/japanese-generative-ai-survey/pull/424) | execution preview と後の r6 fresh rebuild、bibliography hook の修正 | 繰り返し build の証拠。PR番号から費用や全試行回数は推計しない |
| [Historical invariants](https://github.com/eariver/japanese-generative-ai-survey/blob/0a47a9b85108c5a2e9644037e7c0fb48b5bd96dc/docs/survey-production-core-v2-historical-invariants.md) | #166 coverage、#191 entity/comparator、#172 ID localization、layout、exact bytes の起源を記録 | これは historical catalog。MISSING 等の当時 status を現行実装 status と混同しない |

## Probe

`python notes/inspect_snapshot.py` は upstream に対する `git ls-tree` / `git show` のみを呼ぶ。production module の import/実行はしない。出力は [snapshot-probe.json](snapshot-probe.json)、実装は [inspect_snapshot.py](inspect_snapshot.py)。Windows PowerShell の UTF-8出力に BOM が付く場合は `utf-8-sig` として読む。

- tree inventory: schemas 69 / scripts 210 / docs 127 / workflows 7。対象 prefix 配下の tracked files 数であり、active implementation 数でも稼働頻度でもない。
- config contract files: pipeline 62 / quality 3。`contract_identity()` は pipeline に config/Profile/State schema を追加する。
- 過去 accepted set `377134…`: 80 cards、VERIFIED 32 / PARTIAL 27 / NEEDS_MORE 14 / REJECTED 7。
- 全80件が claim 数2。VERIFIED32件中31件は全 verification targets が UNRESOLVED。機械的分布を採取したもので、全カードの意味的誤りを証明してはいない。
- C019 は本文と card を直接突き合わせた。全文の自動抽出システムを作ったり、replacement Evidence を編纂したりしていない。
- 最初の probe で status を誤って `verification.status` と読んだが、schema を実物に合わせ top-level `status` に修正し再集計した。最終出力だけを報告に使用した。

## 外部調査

公式の DVC run cache、Temporal Workflow Execution、W3C PROV Overview、GitHub secure pull_request_target を確認。詳細な適用判断と URL は main report §10 に置いた。製品 version/価格比較や大規模 framework 調査は行わなかった。構成を全面的に置き換える根拠がなく、追加調査の情報利得が小さいと判断したためである。

## 調査の終了基準

現行実装→固定受理artifact→source本文→Human revision の chain と、独立した二 edition の運用修復が揃った。根本判断は十分支持される。今後必要なのは広い閲覧ではなく、実働費用計測と新 inputs での品質/レビュー強度の比較であり、Phase A 後の明示タスクとして切り出した。
